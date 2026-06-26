import assert from "node:assert/strict";
import test from "node:test";

import {
  diagnoseDeviceOffline,
  diagnoseNetworkSlow,
  explainFttraiCopilotUsage,
} from "../src/tools/diagnostics.js";

test("diagnoseDeviceOffline combines detail and related alerts", async () => {
  const result = await diagnoseDeviceOffline(fakeDiagnosticClient(), {
    device_identifier: "AA:BB:CC:DD:EE:FF",
  });

  assert.equal(result.title, "设备离线诊断");
  assert.equal(result.data.recent_alerts.length, 1);
  assert.match(result.summary, /离线/);
});

test("diagnoseNetworkSlow lists devices when identifier is missing", async () => {
  const result = await diagnoseNetworkSlow(fakeDiagnosticClient(), {});

  assert.equal(result.data.devices.length, 1);
  assert.match(result.summary, /缺少设备标识/);
});

test("diagnoseNetworkSlow combines network signals", async () => {
  const result = await diagnoseNetworkSlow(fakeDiagnosticClient(), {
    device_identifier: "AA:BB:CC:DD:EE:FF",
    symptom: "卧室网慢",
  });

  assert.equal(result.data.experience.network_score, 65);
  assert.equal(result.data.station_stats.length, 1);
  assert.match(result.summary, /卧室网慢/);
});

test("explainFttraiCopilotUsage returns customer guidance", async () => {
  const result = await explainFttraiCopilotUsage(null, {
    user_goal: "排查离线",
  });

  assert.equal(result.data.identity, "Customer");
  assert.match(result.summary, /排查离线/);
});

function fakeDiagnosticClient() {
  return {
    async unary(procedure, body) {
      if (procedure === "/bison.device.v1.DeviceService/ListMyDevices") {
        return {
          devices: [
            {
              device: {
                id: "device-id",
                mac: "AA:BB:CC:DD:EE:FF",
                kind: "DEVICE_KIND_MASTER",
              },
              alias: "客厅主网关",
            },
          ],
        };
      }
      if (procedure === "/bison.device.v1.DeviceService/GetDeviceDetail") {
        return {
          device: {
            id: body.deviceId,
            mac: "AA:BB:CC:DD:EE:FF",
            kind: "DEVICE_KIND_MASTER",
          },
          connectStatus: {
            onlineStatus: "ONLINE_STATUS_OFFLINE",
            lastSeen: "2026-05-15T08:00:00Z",
          },
          systemProfile: {
            lastOfflineReason: "LOS",
            faultCodes: ["101"],
          },
        };
      }
      if (procedure === "/bison.device.v1.DeviceService/ListDeviceAlerts") {
        return {
          items: [
            {
              alertContent: {
                id: "alert-id",
                eventName: { code: "LOS", name: "光链路告警" },
                eventType: "EVENT_TYPE_ALARM",
                eventTarget: { deviceId: "AA:BB:CC:DD:EE:FF" },
                displayMessage: "光链路中断",
              },
              device: { id: "device-id", mac: "AA:BB:CC:DD:EE:FF" },
            },
          ],
        };
      }
      if (procedure === "/bison.networkstats.v1.NetworkStatsService/ListNetworkTopology") {
        return {
          topology: {
            gateways: [{ mac: "AA:BB:CC:DD:EE:FF", online: true }],
            stations: [{ mac: "11:22:33:44:55:66", online: true }],
          },
        };
      }
      if (procedure === "/bison.networkstats.v1.NetworkStatsService/GetNetworkExperience") {
        return {
          experienceStats: {
            networkScore: 65,
          },
        };
      }
      if (procedure === "/bison.networkstats.v1.NetworkStatsService/GetStationStats") {
        return {
          stats: [
            {
              station: { mac: "11:22:33:44:55:66", online: true },
              stats: { mac: "11:22:33:44:55:66", rssi: -75, rxPktFail: 1 },
            },
          ],
        };
      }
      throw new Error(`unexpected procedure ${procedure}`);
    },
  };
}
