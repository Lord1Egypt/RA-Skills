import assert from "node:assert/strict";
import test from "node:test";

import {
  getDeviceDetail,
  getDeviceOnlineStatus,
  listMyDevices,
  resolveDevice,
  updateDeviceAlias,
} from "../src/tools/devices.js";

test("listMyDevices formats Connect JSON response", async () => {
  const client = {
    async unary(procedure, body) {
      assert.equal(procedure, "/bison.device.v1.DeviceService/ListMyDevices");
      assert.deepEqual(body, {});
      return {
        devices: [
          {
            device: {
              id: "device-id",
              mac: "AA:BB:CC:DD:EE:FF",
              sn: "SN001",
              kind: "DEVICE_KIND_MASTER",
            },
            alias: "客厅主网关",
            role: "BIND_ROLE_OWNER",
            slaveCount: 2,
          },
        ],
      };
    },
  };

  const result = await listMyDevices(client);

  assert.equal(result.title, "绑定设备列表");
  assert.equal(result.data.devices.length, 1);
  assert.deepEqual(result.data.devices[0], {
    id: "device-id",
    mac: "AA:BB:CC:DD:EE:FF",
    sn: "SN001",
    kind: "DEVICE_KIND_MASTER",
    alias: "客厅主网关",
    role: "BIND_ROLE_OWNER",
    slave_count: 2,
    bind_at: null,
  });
});

test("listMyDevices handles empty device list", async () => {
  const result = await listMyDevices({
    async unary() {
      return { devices: [] };
    },
  });

  assert.match(result.summary, /没有绑定设备/);
  assert.equal(result.data.devices.length, 0);
});

test("resolveDevice matches MAC address from bound devices", async () => {
  const resolved = await resolveDevice(fakeDeviceClient(), "aa-bb-cc-dd-ee-ff");

  assert.equal(resolved.id, "device-id");
  assert.equal(resolved.mac, "AA:BB:CC:DD:EE:FF");
  assert.equal(resolved.alias, "客厅主网关");
  assert.equal(resolved.matched_by, "mac");
});

test("resolveDevice accepts UUID without list lookup", async () => {
  const uuid = "123e4567-e89b-12d3-a456-426614174000";
  const resolved = await resolveDevice({
    async unary() {
      throw new Error("should not list devices for UUID");
    },
  }, uuid);

  assert.deepEqual(resolved, {
    id: uuid,
    mac: "",
    alias: "",
    matched_by: "id",
  });
});

test("getDeviceDetail resolves alias and formats detail", async () => {
  const calls = [];
  const result = await getDeviceDetail(fakeDeviceClient(calls), {
    device_identifier: "客厅主网关",
  });

  assert.deepEqual(calls, [
    ["/bison.device.v1.DeviceService/ListMyDevices", {}],
    ["/bison.device.v1.DeviceService/GetDeviceDetail", { deviceId: "device-id" }],
  ]);
  assert.equal(result.data.detail.online_status_label, "在线");
  assert.equal(result.data.detail.factory_info.software_ver, "1.0.0");
  assert.match(result.summary, /在线/);
});

test("getDeviceOnlineStatus returns compact status payload", async () => {
  const result = await getDeviceOnlineStatus(fakeDeviceClient(), {
    device_identifier: "AA:BB:CC:DD:EE:FF",
  });

  assert.equal(result.title, "设备在线状态");
  assert.equal(result.data.online_status_label, "在线");
  assert.equal(result.data.ip_addr, "192.0.2.10");
});

test("updateDeviceAlias validates alias length", async () => {
  await assert.rejects(
    () => updateDeviceAlias(fakeDeviceClient(), {
      device_identifier: "AA:BB:CC:DD:EE:FF",
      new_alias: "123456789012345678901",
    }),
    /不能超过 20 个字符/,
  );
});

test("updateDeviceAlias resolves identifier and writes alias", async () => {
  const calls = [];
  const result = await updateDeviceAlias(fakeDeviceClient(calls), {
    device_identifier: "AA:BB:CC:DD:EE:FF",
    new_alias: "书房主网关",
  });

  assert.deepEqual(calls, [
    ["/bison.device.v1.DeviceService/ListMyDevices", {}],
    ["/bison.device.v1.DeviceService/UpdateDeviceAlias", {
      deviceId: "device-id",
      alias: "书房主网关",
    }],
  ]);
  assert.match(result.summary, /书房主网关/);
});

function fakeDeviceClient(calls = []) {
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
              role: "BIND_ROLE_OWNER",
              slaveCount: 2,
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
          connectStatus: {
            onlineStatus: "ONLINE_STATUS_ONLINE",
            lastSeen: "2026-05-15T08:00:00Z",
            ipAddr: "192.0.2.10",
          },
          factoryInfo: {
            softwareVer: "1.0.0",
            hardwareVer: "A1",
            productClass: "FTTR",
          },
          systemProfile: {
            cpuOccupation: "12",
            memoryOccupation: "30",
            faultCodes: [],
          },
        };
      }
      if (procedure === "/bison.device.v1.DeviceService/UpdateDeviceAlias") {
        return {};
      }
      throw new Error(`unexpected procedure ${procedure}`);
    },
  };
}
