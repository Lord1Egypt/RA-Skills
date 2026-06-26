import assert from "node:assert/strict";
import test from "node:test";

import {
  getDeviceDetail,
  getDeviceOnlineStatus,
  listDevices,
  resolveDevice,
} from "../src/tools/devices.js";

test("listDevices sends admin list request with filters", async () => {
  const calls = [];
  const result = await listDevices(fakeDeviceClient(calls), {
    region_code: "440000",
    online_status: "OFFLINE",
    kind: "MASTER",
    limit: 10,
  });

  assert.deepEqual(calls[0], [
    "/bison.admin.device.v1.DeviceService/ListDevices",
    {
      pagination: { page: 1, limit: 10 },
      regionCode: "440000",
      onlineStatus: "ONLINE_STATUS_OFFLINE",
      kind: "DEVICE_KIND_MASTER",
    },
  ]);
  assert.equal(result.data.devices.length, 1);
  assert.equal(result.data.devices[0].online_status_label, "离线");
});

test("getDeviceDetail supports MAC identifier", async () => {
  const calls = [];
  const result = await getDeviceDetail(fakeDeviceClient(calls), {
    device_identifier: "aa-bb-cc-dd-ee-ff",
  });

  assert.deepEqual(calls[0], [
    "/bison.admin.device.v1.DeviceService/GetDeviceDetail",
    { mac: "AABBCCDDEEFF" },
  ]);
  assert.equal(result.data.detail.mac, "AABBCCDDEEFF");
});

test("getDeviceDetail resolves SN identifier through list", async () => {
  const calls = [];
  await getDeviceDetail(fakeDeviceClient(calls), {
    device_identifier: "SN001",
  });

  assert.deepEqual(calls.map((call) => call[0]), [
    "/bison.admin.device.v1.DeviceService/ListDevices",
    "/bison.admin.device.v1.DeviceService/GetDeviceDetail",
  ]);
  assert.deepEqual(calls[1][1], { id: "device-id" });
});

test("getDeviceOnlineStatus returns compact status", async () => {
  const result = await getDeviceOnlineStatus(fakeDeviceClient(), {
    device_identifier: "AABBCCDDEEFF",
  });

  assert.equal(result.data.online_status_label, "离线");
});

test("resolveDevice resolves SN through admin list", async () => {
  const calls = [];
  const result = await resolveDevice(fakeDeviceClient(calls), "SN001");

  assert.equal(result.id, "device-id");
  assert.equal(result.matched_by, "sn");
});

function fakeDeviceClient(calls = []) {
  return {
    async unary(procedure, body) {
      calls.push([procedure, body]);
      if (procedure === "/bison.admin.device.v1.DeviceService/ListDevices") {
        return {
          items: [
            {
              devices: {
                id: "device-id",
                mac: "AABBCCDDEEFF",
                sn: "SN001",
                kind: "DEVICE_KIND_MASTER",
              },
              connectStatus: {
                onlineStatus: "ONLINE_STATUS_OFFLINE",
              },
              systemProfile: {
                faultCodes: ["101"],
              },
            },
          ],
          totalCount: 1,
        };
      }
      if (procedure === "/bison.admin.device.v1.DeviceService/GetDeviceDetail") {
        return {
          device: {
            id: body.id || "device-id",
            mac: body.mac || "AABBCCDDEEFF",
            sn: "SN001",
            kind: "DEVICE_KIND_MASTER",
          },
          connectStatus: {
            onlineStatus: "ONLINE_STATUS_OFFLINE",
          },
          systemProfile: {
            faultCodes: ["101"],
          },
        };
      }
      throw new Error(`unexpected procedure ${procedure}`);
    },
  };
}
