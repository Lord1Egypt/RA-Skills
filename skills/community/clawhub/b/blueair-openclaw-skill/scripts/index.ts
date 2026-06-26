import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
    CallToolRequestSchema,
    ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import BlueairAwsApi from "./api/blueairAwsClient.js";
import { Region } from "./api/config.js";
import fs from "fs";
import path from "path";
import os from "os";

// 1. Initial State & Config Loading
const CONFIG_PATH = path.join(os.homedir(), ".blueair", "config.json");

function loadConfig() {
    if (fs.existsSync(CONFIG_PATH)) {
        try {
            return JSON.parse(fs.readFileSync(CONFIG_PATH, "utf-8"));
        } catch (e) {
            console.error("Error parsing config file:", e);
        }
    }
    return {};
}

let api: BlueairAwsApi | null = null;
let accountUuid: string | null = null;

async function getApi() {
    if (api) return api;

    const config = loadConfig();
    const username = config.username || process.env.BLUEAIR_USERNAME;
    const password = config.password || process.env.BLUEAIR_PASSWORD;
    const regionString = config.region || process.env.BLUEAIR_REGION || "EU";

    if (!username || !password) {
        throw new Error("Credentials missing. Please set BLUEAIR_USERNAME/PASSWORD or configure ~/.blueair/config.json");
    }

    // Map string region to Enum
    const regionMap: Record<string, Region> = {
        "USA": Region.US,
        "US": Region.US,
        "EU": Region.EU,
        "Australia": Region.AU,
        "AU": Region.AU,
        "China": Region.CN,
        "CN": Region.CN,
        "Russia": Region.RU,
        "RU": Region.RU,
    };
    const region = regionMap[regionString] || Region.EU;

    if (config.accountUuid && config.region) {
        api = new BlueairAwsApi(username, password, region);
    } else {
        const result = await BlueairAwsApi.loginWithAutoDetect(username, password);
        api = new BlueairAwsApi(username, password, result.region);
        accountUuid = result.accountUuid;
    }

    return api;
}

// 2. Setup MCP Server
const server = new Server(
    {
        name: "blueair-mcp-server",
        version: "1.0.0",
    },
    {
        capabilities: {
            tools: {},
        },
    }
);

// 3. Define Tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
        tools: [
            {
                name: "blueair_get_all_statuses",
                description: "Get the real-time status and sensor data for all Blueair devices in the account.",
                inputSchema: { type: "object", properties: {} },
            },
            {
                name: "blueair_set_state",
                description: "Control a specific Blueair device attribute (fan speed, power, etc.).",
                inputSchema: {
                    type: "object",
                    properties: {
                        uuid: { type: "string", description: "The UUID of the device" },
                        attribute: {
                            type: "string",
                            enum: ["fanspeed", "standby", "automode", "childlock", "nightmode"],
                            description: "The attribute to change"
                        },
                        value: {
                            type: ["number", "boolean"],
                            description: "The new value (number for fanspeed, boolean for others)"
                        },
                    },
                    required: ["uuid", "attribute", "value"],
                },
            },
        ],
    };
});

// 4. Handle Tool Calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
    try {
        const client = await getApi();
        const { name, arguments: args } = request.params;

        if (name === "blueair_get_all_statuses") {
            const devices = await client.getDevices();
            if (!accountUuid) {
                // If we don't have accountUuid from config, use the one from the first device's name (common pattern in this API)
                accountUuid = devices[0]?.name;
            }
            const uuids = devices.map((d: any) => d.uuid);
            const statuses = await client.getDeviceStatus(accountUuid!, uuids);

            return {
                content: [{ type: "text", text: JSON.stringify(statuses, null, 2) }],
            };
        }

        if (name === "blueair_set_state") {
            const { uuid, attribute, value } = args as { uuid: string; attribute: string; value: any };
            await client.setDeviceStatus(uuid, attribute, value);
            return {
                content: [{ type: "text", text: `Successfully set ${attribute} to ${value} for device ${uuid}` }],
            };
        }

        throw new Error(`Tool not found: ${name}`);
    } catch (error: any) {
        return {
            content: [{ type: "text", text: `Error: ${error.message}` }],
            isError: true,
        };
    }
});

// 5. Start Server
async function main() {
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error("Blueair MCP Server running on stdio");
}

main().catch((error) => {
    console.error("Fatal error in main():", error);
    process.exit(1);
});
