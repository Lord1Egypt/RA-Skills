import assert from "node:assert/strict";
import test from "node:test";

import {
  getAgentVersion,
  getMasterGatewayInfo,
} from "../src/tools/commands.js";

test("getMasterGatewayInfo uses operator non-stream command API", async () => {
  const calls = [];
  const result = await getMasterGatewayInfo(fakeCommandClient(calls), {
    device_identifier: "AA:BB:CC:DD:EE:FF",
  });

  assert.equal(calls[1][0], "/bison.admin.fttrmanage.v1.FttrManageService/ExecuteCMDNonStream");
  assert.deepEqual(calls[1][1], {
    mac: "AABBCCDDEEFF",
    command: {
      cmdType: "CMD_TYPE_GET_FMU_INFO",
      getFmuInfo: {},
    },
  });
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

function fakeCommandClient(calls = []) {
  return {
    async unary(procedure, body) {
      calls.push([procedure, body]);
      if (procedure === "/bison.admin.device.v1.DeviceService/GetDeviceDetail") {
        return { device: { id: "device-id", mac: "AABBCCDDEEFF" } };
      }
      if (procedure === "/bison.admin.fttrmanage.v1.FttrManageService/ExecuteCMDNonStream") {
        return { sequenceId: "seq-1" };
      }
      if (procedure === "/bison.admin.fttrmanage.v1.FttrManageService/GetExecuteResult") {
        return { result: { status: "STATUS_SUCCESS", result: { ok: true } } };
      }
      throw new Error(`unexpected procedure ${procedure}`);
    },
  };
}
