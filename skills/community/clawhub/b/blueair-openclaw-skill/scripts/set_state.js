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
        }
        catch (e) {
            console.error("Error parsing config file:", e);
        }
    }
    return {};
}
let api = null;
let accountUuid = null;
async function getApi() {
    if (api)
        return api;
    const config = loadConfig();
    const username = config.username || process.env.BLUEAIR_USERNAME;
    const password = config.password || process.env.BLUEAIR_PASSWORD;
    const regionString = config.region || process.env.BLUEAIR_REGION || "EU";
    if (!username || !password) {
        throw new Error("Credentials missing. Please set BLUEAIR_USERNAME/PASSWORD or configure ~/.blueair/config.json");
    }
    const regionMap = {
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
    }
    else {
        const result = await BlueairAwsApi.loginWithAutoDetect(username, password);
        api = new BlueairAwsApi(username, password, result.region);
        accountUuid = result.accountUuid;
    }
    return api;
}
async function main() {
    const args = process.argv.slice(2);
    if (args.length < 3) {
        console.error("Usage: node set_state.js <uuid> <attribute> <value>");
        process.exit(1);
    }
    const uuid = args[0];
    const attribute = args[1];
    let value = args[2];
    // Ensure types matches what the API expects (number or boolean)
    if (value === "true")
        value = true;
    else if (value === "false")
        value = false;
    else if (!isNaN(Number(value)))
        value = Number(value);
    try {
        const client = await getApi();
        await client.setDeviceStatus(uuid, attribute, value);
        console.log(`Successfully set ${attribute} to ${value} for device ${uuid}`);
    }
    catch (error) {
        console.error(`Error setting device status: ${error.message}`);
        process.exit(1);
    }
}
main();
