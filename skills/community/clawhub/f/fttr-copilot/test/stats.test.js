import assert from "node:assert/strict";
import test from "node:test";

import {
  getDeviceLoad,
  getDeviceStats,
  getFaultCounter,
} from "../src/tools/stats.js";

test("getDeviceStats aggregates customer bound devices", async () => {
  const result = await getDeviceStats(fakeStatsClient());

  assert.equal(result.data.total, 2);
  assert.equal(result.data.online, 1);
  assert.equal(result.data.offline, 1);
  assert.equal(result.data.faulty, 1);
});

test("getDeviceLoad returns basic system profile", async () => {
  const result = await getDeviceLoad(fakeStatsClient(), {
    device_identifier: "AA:BB:CC:DD:EE:FF",
  });

  assert.equal(result.data.cpu_occupation, "12");
  assert.equal(result.data.memory_occupation, "30");
  assert.deepEqual(result.data.fault_codes, ["101", "102"]);
});

test("getFaultCounter aggregates fault codes", async () => {
  const result = await getFaultCounter(fakeStatsClient());

  assert.deepEqual(result.data.counters, [
    { code: "101", device_count: 1 },
    { code: "102", device_count: 1 },
  ]);
});

function fakeStatsClient() {
  return {
    async unary(procedure, body) {
      if (procedure === "/bison.device.v1.DeviceService/ListMyDevices") {
        return {
          devices: [
            {
              device: { id: "device-1", mac: "AA:BB:CC:DD:EE:FF", kind: "DEVICE_KIND_MASTER" },
              alias: "客厅主网关",
              slaveCount: 1,
            },
            {
              device: { id: "device-2", mac: "AA:BB:CC:DD:EE:00", kind: "DEVICE_KIND_MASTER" },
              alias: "书房主网关",
              slaveCount: 0,
            },
          ],
        };
      }
      if (procedure === "/bison.device.v1.DeviceService/GetDeviceDetail") {
        const first = body.deviceId === "device-1";
        return {
          device: {
            id: body.deviceId,
            mac: first ? "AA:BB:CC:DD:EE:FF" : "AA:BB:CC:DD:EE:00",
            kind: "DEVICE_KIND_MASTER",
          },
          connectStatus: {
            onlineStatus: first ? "ONLINE_STATUS_ONLINE" : "ONLINE_STATUS_OFFLINE",
          },
          systemProfile: {
            cpuOccupation: first ? "12" : "8",
            memoryOccupation: first ? "30" : "20",
            lastOfflineReason: first ? "" : "POWER_OFF",
            faultCodes: first ? ["101", "102"] : [],
          },
        };
      }
      throw new Error(`unexpected procedure ${procedure}`);
    },
  };
}
