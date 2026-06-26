#!/usr/bin/env node
import BlueairAwsApi from "./api/blueairAwsClient.js";
import { Region } from "./api/config.js";
import fs from "fs";
import path from "path";
import os from "os";

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

async function main() {
    try {
        const client = await getApi();
        const devices = await client.getDevices();
        if (!accountUuid) {
            accountUuid = devices[0]?.name;
        }
        const uuids = devices.map((d: any) => d.uuid);
        const statuses = await client.getDeviceStatus(accountUuid!, uuids);

        console.log(JSON.stringify(statuses, null, 2));
    } catch (error: any) {
        console.error(`Error fetching device statuses: ${error.message}`);
        process.exit(1);
    }
}

main();
