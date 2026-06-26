import assert from "node:assert/strict";
import test from "node:test";

import {
  getDeviceLoad,
  getDeviceStats,
  getFaultCounter,
} from "../src/tools/stats.js";

test("getDeviceStats calls admin summary stats", async () => {
  const calls = [];
  const result = await getDeviceStats(fakeStatsClient(calls), {
    region_code: "440000",
  });

  assert.deepEqual(calls[0], [
    "/bison.admin.devicestats.v1.DeviceStatsService/GetDeviceSummaryStats",
    { regionCode: "440000" },
  ]);
  assert.equal(result.data.total_devices_count, 10);
});

test("getFaultCounter calls admin fault stats", async () => {
  const result = await getFaultCounter(fakeStatsClient(), {
    region_code: "440000",
  });

  assert.equal(result.data.fault_stats[0].devices_with_any_errors, 2);
});

test("getDeviceLoad calls admin charts load API", async () => {
  const calls = [];
  await getDeviceLoad(fakeStatsClient(calls), {
    device_identifier: "AA:BB:CC:DD:EE:FF",
    load_type: "basic",
    start_time: "2026-05-14T00:00:00.000Z",
    end_time: "2026-05-15T00:00:00.000Z",
  });

  assert.equal(calls.at(-1)[0], "/bison.admin.charts.v1.ChartsService/FetchDeviceLoad");
  assert.equal(calls.at(-1)[1].networkId, "AABBCCDDEEFF");
  assert.deepEqual(calls.at(-1)[1].basic, {});
});

function fakeStatsClient(calls = []) {
  return {
    async unary(procedure, body) {
      calls.push([procedure, body]);
      if (procedure === "/bison.admin.devicestats.v1.DeviceStatsService/GetDeviceSummaryStats") {
        return {
          totalDevicesCount: 10,
          registeredDevicesCount: 8,
          onlineDevicesCount: 6,
        };
      }
      if (procedure === "/bison.admin.devicestats.v1.DeviceStatsService/GetDeviceFaultStats") {
        return {
          faultStats: [
            { regionCode: "440000", masterDevicesCount: 10, devicesWithAnyErrors: 2 },
          ],
        };
      }
      if (procedure === "/bison.admin.device.v1.DeviceService/GetDeviceDetail") {
        return { device: { id: "device-id", mac: "AABBCCDDEEFF" } };
      }
      if (procedure === "/bison.admin.charts.v1.ChartsService/FetchDeviceLoad") {
        return { basicLoads: { serializes: [] } };
      }
      throw new Error(`unexpected procedure ${procedure}`);
    },
  };
}
