import assert from "node:assert/strict";
import test from "node:test";

import {
  getAgentVersion,
  getMasterGatewayInfo,
  getSlaveGatewayInfo,
} from "../src/tools/commands.js";

test("getMasterGatewayInfo executes customer command and polls result", async () => {
  const calls = [];
  const result = await getMasterGatewayInfo(fakeCommandClient(calls), {
    device_identifier: "AA:BB:CC:DD:EE:FF",
  });

  assert.deepEqual(calls.slice(1, 3), [
    ["/bison.device.v1.DeviceService/ExecuteCMD", {
      deviceId: "device-id",
      command: {
        cmdType: "CMD_TYPE_GET_FMU_INFO",
        getFmuInfo: {},
      },
    }],
    ["/bison.device.v1.DeviceService/GetExecuteResult", {
      deviceId: "device-id",
      sequenceId: "seq-1",
    }],
  ]);
  assert.equal(result.data.status, "STATUS_SUCCESS");
});

test("getAgentVersion uses agent version command", async () => {
  const calls = [];
  await getAgentVersion(fakeCommandClient(calls), {
    device_identifier: "AA:BB:CC:DD:EE:FF",
  });

  assert.deepEqual(calls[1][1].command, {
    cmdType: "CMD_TYPE_GET_AGENT_VERSION",
    getAgentVersion: {},
  });
});

test("getSlaveGatewayInfo returns timeout with topology fallback", async () => {
  const calls = [];
  const result = await getSlaveGatewayInfo(fakeCommandClient(calls, { pending: true }), {
    device_identifier: "AA:BB:CC:DD:EE:FF",
    wait_timeout_ms: 0,
  });

  assert.equal(result.data.timed_out, true);
  assert.equal(result.data.sequence_id, "seq-1");
  assert.equal(result.data.fallback.title, "网络拓扑");
});

function fakeCommandClient(calls = [], options = {}) {
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
                kind: "DEVICE_KIND_MASTER",
              },
              alias: "客厅主网关",
            },
          ],
        };
      }
      if (procedure === "/bison.device.v1.DeviceService/ExecuteCMD") {
        return { sequenceId: "seq-1" };
      }
      if (procedure === "/bison.device.v1.DeviceService/GetExecuteResult") {
        if (options.pending) {
          const err = new Error("记录不存在");
          err.code = "invalid_argument";
          throw err;
        }
        return {
          command: body.command,
          result: {
            status: "STATUS_SUCCESS",
            cmdType: "CMD_TYPE_GET_FMU_INFO",
            contentType: "CONTENT_TYPE_JSON",
            result: { version: "1.0.0" },
          },
        };
      }
      if (procedure === "/bison.networkstats.v1.NetworkStatsService/ListNetworkTopology") {
        return {
          topology: {
            gateways: [{ mac: "AA:BB:CC:DD:EE:FF", online: true }],
            stations: [],
          },
        };
      }
      throw new Error(`unexpected procedure ${procedure}`);
    },
  };
}
