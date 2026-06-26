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

async function test() {
    const config = loadConfig();
    const username = config.username;
    const password = config.password;

    console.log("Testing with username:", username);

    try {
        console.log("Attempting auto-detect login...");
        const result = await BlueairAwsApi.loginWithAutoDetect(username, password);
        console.log("Login Success!");
        console.log("Region detected:", result.region);
        console.log("Account UUID:", result.accountUuid);

        const api = new BlueairAwsApi(username, password, result.region);
        api['accessToken'] = result.accessToken;
        api['last_login'] = Date.now();

        console.log("Fetching devices...");
        const devices = await api.getDevices();
        console.log("Devices:", JSON.stringify(devices, null, 2));

        if (devices.length > 0) {
            console.log("Fetching statuses...");
            const statuses = await api.getDeviceStatus(result.accountUuid, devices.map((d: any) => d.uuid));
            console.log("Statuses:", JSON.stringify(statuses, null, 2));
        }
    } catch (e: any) {
        console.error("Test Failed:", e.message);
        if (e.stack) console.error(e.stack);
    }
}

test();
