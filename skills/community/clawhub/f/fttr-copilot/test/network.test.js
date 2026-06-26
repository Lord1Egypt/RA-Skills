import assert from "node:assert/strict";
import test from "node:test";

import {
  getNetworkExperience,
  getNetworkTopology,
  getStationExperience,
  getStationStats,
} from "../src/tools/network.js";

test("getNetworkTopology resolves alias and formats topology", async () => {
  const calls = [];
  const result = await getNetworkTopology(fakeNetworkClient(calls), {
    device_identifier: "客厅主网关",
  });

  assert.deepEqual(calls.slice(0, 2), [
    ["/bison.device.v1.DeviceService/ListMyDevices", {}],
    ["/bison.networkstats.v1.NetworkStatsService/ListNetworkTopology", {
      mac: "AA:BB:CC:DD:EE:FF",
    }],
  ]);
  assert.equal(result.data.topology.gateways.length, 1);
  assert.equal(result.data.topology.stations.length, 1);
  assert.match(result.summary, /1 个网关和 1 个下挂设备/);
});

test("getStationStats filters one station by MAC", async () => {
  const result = await getStationStats(fakeNetworkClient(), {
    device_identifier: "AA:BB:CC:DD:EE:FF",
    sta_mac: "11-22-33-44-55-66",
  });

  assert.equal(result.data.stats.length, 1);
  assert.equal(result.data.stats[0].station.mac, "11:22:33:44:55:66");
  assert.equal(result.data.stats[0].stats.rssi, -55);
});

test("getNetworkExperience formats score and trends", async () => {
  const result = await getNetworkExperience(fakeNetworkClient(), {
    device_identifier: "AA:BB:CC:DD:EE:FF",
  });

  assert.equal(result.data.experience.network_score, 87);
  assert.equal(result.data.experience.bandwidth_serialize[0].down, 2048);
  assert.match(result.summary, /87/);
});

test("getStationExperience requires station mac", async () => {
  await assert.rejects(
    () => getStationExperience(fakeNetworkClient(), {
      device_identifier: "AA:BB:CC:DD:EE:FF",
    }),
    /sta_mac 不能为空/,
  );
});

test("getStationExperience formats RSSI points", async () => {
  const calls = [];
  const result = await getStationExperience(fakeNetworkClient(calls), {
    device_identifier: "AA:BB:CC:DD:EE:FF",
    sta_mac: "11:22:33:44:55:66",
  });

  assert.deepEqual(calls.at(-1), [
    "/bison.networkstats.v1.NetworkStatsService/GetStationExperience",
    {
      mac: "AA:BB:CC:DD:EE:FF",
      staMac: "11:22:33:44:55:66",
    },
  ]);
  assert.equal(result.data.rssi.length, 1);
  assert.equal(result.data.rssi[0].avg, -55);
});

test("network tools resolve UUID by device detail to obtain MAC", async () => {
  const calls = [];
  await getNetworkTopology(fakeNetworkClient(calls), {
    device_identifier: "123e4567-e89b-12d3-a456-426614174000",
  });

  assert.deepEqual(calls.slice(0, 2), [
    ["/bison.device.v1.DeviceService/GetDeviceDetail", {
      deviceId: "123e4567-e89b-12d3-a456-426614174000",
    }],
    ["/bison.networkstats.v1.NetworkStatsService/ListNetworkTopology", {
      mac: "AA:BB:CC:DD:EE:FF",
    }],
  ]);
});

function fakeNetworkClient(calls = []) {
  return {
    async unary(procedure, body) {
      calls.push([procedure, body]);
      if (procedure === "/bison.device.v1.DeviceService/ListMyDevices") {
        return {
          devices: [
            {
              device: {
                id: "device-id",
                mac: "AA:BB:CC:DD:EE:FF",
                sn: "SN001",
                kind: "KIND_MASTER",
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
            sn: "SN001",
            kind: "KIND_MASTER",
          },
        };
      }
      if (procedure === "/bison.networkstats.v1.NetworkStatsService/ListNetworkTopology") {
        return {
          topology: {
            gateways: [
              {
                type: "NODE_TYPE_MASTER",
                mac: "AA:BB:CC:DD:EE:FF",
                name: "主网关",
                online: true,
              },
            ],
            stations: [
              {
                type: "NODE_TYPE_STATION",
                mac: "11:22:33:44:55:66",
                name: "手机",
                parentMac: "AA:BB:CC:DD:EE:FF",
                online: true,
              },
            ],
            stats: [
              stationStats(),
            ],
          },
        };
      }
      if (procedure === "/bison.networkstats.v1.NetworkStatsService/GetStationStats") {
        return {
          stats: [
            {
              station: {
                type: "phone",
                mac: "11:22:33:44:55:66",
                name: "手机",
                parentMac: "AA:BB:CC:DD:EE:FF",
                online: true,
              },
              stats: stationStats(),
            },
          ],
        };
      }
      if (procedure === "/bison.networkstats.v1.NetworkStatsService/GetNetworkExperience") {
        return {
          experienceStats: {
            networkScore: 87,
            experienceSerialize: [
              { timeWindow: "2026-05-15T08:00:00Z", numGood: 8, numBad: 1, numNormal: 2 },
            ],
            bandwidthSerialize: [
              { timeWindow: "2026-05-15T08:00:00Z", up: 1024, down: 2048 },
            ],
            rssiSerialize: [
              { timeWindow: "2026-05-15T08:00:00Z", avg: -55, min: -70, max: -40 },
            ],
          },
        };
      }
      if (procedure === "/bison.networkstats.v1.NetworkStatsService/GetStationExperience") {
        return {
          staMac: body.staMac,
          rssiSerialize: [
            { timeWindow: "2026-05-15T08:00:00Z", avg: -55, min: -70, max: -40 },
          ],
        };
      }
      throw new Error(`unexpected procedure ${procedure}`);
    },
  };
}

function stationStats() {
  return {
    mac: "11:22:33:44:55:66",
    pingDelay: 5,
    rssi: -55,
    upSpeed: 100,
    downSpeed: 200,
    upLinkNegotiationRate: 866,
    downLinkNegotiationRate: 866,
    rxFlow: 1000,
    txFlow: 2000,
    rxPktFail: 1,
    txPktFail: 2,
  };
}
