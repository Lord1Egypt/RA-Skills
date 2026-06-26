#!/usr/bin/env node

import { loadConfig } from "./config.js";
import { ConnectClient } from "./connect.js";
import { fail, ok, printJson } from "./output.js";
import {
  calculateAlertNumber,
  getAlertDetail,
  listDeviceAlerts,
  markAlertsAsRead,
} from "./tools/alerts.js";
import {
  getAgentVersion,
  getMasterGatewayInfo,
  getSlaveGatewayInfo,
} from "./tools/commands.js";
import {
  getDeviceDetail,
  getDeviceOnlineStatus,
  listDevices,
} from "./tools/devices.js";
import {
  diagnoseDeviceOffline,
  diagnoseNetworkSlow,
  explainFttraiCopilotUsage,
} from "./tools/diagnostics.js";
import {
  getNetworkExperience,
  getNetworkTopology,
  getStationExperience,
  getStationStats,
} from "./tools/network.js";
import {
  getDeviceLoad,
  getDeviceStats,
  getFaultCounter,
} from "./tools/stats.js";

const tools = {
  list_devices: async (client, args) => ok(await listDevices(client, args)),
  get_device_detail: async (client, args) => ok(await getDeviceDetail(client, args)),
  get_device_online_status: async (client, args) => ok(await getDeviceOnlineStatus(client, args)),
  list_device_alerts: async (client, args) => ok(await listDeviceAlerts(client, args)),
  get_alert_detail: async (client, args) => ok(await getAlertDetail(client, args)),
  calculate_alert_number: async (client, args) => ok(await calculateAlertNumber(client, args)),
  mark_alerts_as_read: async (client, args) => ok(await markAlertsAsRead(client, args)),
  get_network_topology: async (client, args) => ok(await getNetworkTopology(client, args)),
  get_station_stats: async (client, args) => ok(await getStationStats(client, args)),
  get_station_metrics: async (client, args) => ok(await getStationStats(client, args)),
  get_network_experience: async (client, args) => ok(await getNetworkExperience(client, args)),
  get_station_experience: async (client, args) => ok(await getStationExperience(client, args)),
  get_device_stats: async (client, args) => ok(await getDeviceStats(client, args)),
  get_device_load: async (client, args) => ok(await getDeviceLoad(client, args)),
  get_fault_counter: async (client, args) => ok(await getFaultCounter(client, args)),
  get_master_gateway_info: async (client, args) => ok(await getMasterGatewayInfo(client, args)),
  get_slave_gateway_info: async (client, args) => ok(await getSlaveGatewayInfo(client, args)),
  get_agent_version: async (client, args) => ok(await getAgentVersion(client, args)),
  diagnose_device_offline: async (client, args) => ok(await diagnoseDeviceOffline(client, args)),
  diagnose_network_slow: async (client, args) => ok(await diagnoseNetworkSlow(client, args)),
  explain_fttrai_copilot_usage: async (client, args) => ok(await explainFttraiCopilotUsage(client, args)),
};

async function main(argv) {
  const [toolName, rawArgs] = argv;

  if (!toolName || toolName === "--help" || toolName === "-h") {
    printHelp();
    return 0;
  }

  if (!Object.hasOwn(tools, toolName)) {
    const err = new Error(`未知工具: ${toolName}`);
    err.code = "unknown_tool";
    printJson(fail(err));
    return 2;
  }

  try {
    const args = parseArguments(rawArgs);
    const config = loadConfig();
    const client = new ConnectClient(config);
    const result = await tools[toolName](client, args);
    printJson(result);
    return 0;
  } catch (error) {
    printJson(fail(error));
    return 1;
  }
}

function parseArguments(rawArgs) {
  if (rawArgs === undefined || rawArgs.trim() === "") return {};
  try {
    return JSON.parse(rawArgs);
  } catch {
    const err = new Error("参数必须是 JSON 字符串");
    err.code = "invalid_argument";
    throw err;
  }
}

function printHelp() {
  process.stdout.write(`FTTR Operator Copilot OpenClaw skill CLI

Usage:
  node src/cli.js <tool> [json-arguments]

Available tools:
  list_devices '{"region_code":"<optional>","online_status":"ONLINE|OFFLINE","limit":20}'
  get_device_detail '{"device_identifier":"<device-id|mac|sn>"}'
  get_device_online_status '{"device_identifier":"<device-id|mac|sn>"}'
  list_device_alerts '{"device_identifier":"<optional>","region_code":"<optional>","event_type":"ALARM","limit":20}'
  get_alert_detail '{"alert_id":"<alert-id>"}'
  calculate_alert_number '{"device_identifiers":["<device-id|mac|sn>"]}'
  mark_alerts_as_read '{"alert_ids":["<alert-id>"]}'
  get_network_topology '{"device_identifier":"<device-id|mac|sn>"}'
  get_station_stats '{"device_identifier":"<device-id|mac|sn>","sta_mac":"<optional>"}'
  get_station_metrics '{"device_identifier":"<device-id|mac|sn>","sta_mac":"<optional>"}'
  get_network_experience '{"device_identifier":"<device-id|mac|sn>"}'
  get_station_experience '{"device_identifier":"<device-id|mac|sn>","sta_mac":"<sta-mac>"}'
  get_device_stats '{"region_code":"<optional>"}'
  get_device_load '{"device_identifier":"<device-id|mac|sn>","load_type":"basic"}'
  get_fault_counter '{"region_code":"<optional>"}'
  get_master_gateway_info '{"device_identifier":"<device-id|mac|sn>"}'
  get_slave_gateway_info '{"device_identifier":"<device-id|mac|sn>"}'
  get_agent_version '{"device_identifier":"<device-id|mac|sn>"}'
  diagnose_device_offline '{"device_identifier":"<device-id|mac|sn>"}'
  diagnose_network_slow '{"device_identifier":"<device-id|mac|sn>","symptom":"<optional>"}'
  explain_fttrai_copilot_usage '{"user_goal":"<optional>"}'

Required environment:
  FTTRAI_OPERATOR_AUTH_TOKEN

Optional environment:
  FTTRAI_RPC_URL (default: https://fms-main.fttrai.com/api/)

`);
}

main(process.argv.slice(2)).then((code) => {
  process.exitCode = code;
});
