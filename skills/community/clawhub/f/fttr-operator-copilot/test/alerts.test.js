import assert from "node:assert/strict";
import test from "node:test";

import {
  calculateAlertNumber,
  getAlertDetail,
  listDeviceAlerts,
  markAlertsAsRead,
} from "../src/tools/alerts.js";

test("listDeviceAlerts calls operator alert API with region filters", async () => {
  const calls = [];
  const result = await listDeviceAlerts(fakeAlertClient(calls), {
    region_code: "440000",
    event_type: "ALARM",
    limit: 10,
  });

  assert.deepEqual(calls[0], [
    "/bison.admin.fttrmanage.v1.FttrManageService/ListAlerts",
    {
      pagination: { limit: 10 },
      regionCode: "440000",
      eventType: "EVENT_TYPE_ALARM",
    },
  ]);
  assert.equal(result.data.alerts.length, 1);
});

test("getAlertDetail formats operator alert detail", async () => {
  const result = await getAlertDetail(fakeAlertClient(), {
    alert_id: "alert-id",
  });

  assert.equal(result.data.alert.id, "alert-id");
});

test("calculateAlertNumber resolves device identifiers", async () => {
  const calls = [];
  const result = await calculateAlertNumber(fakeAlertClient(calls), {
    device_identifiers: ["AA:BB:CC:DD:EE:FF"],
  });

  assert.equal(calls.at(-1)[0], "/bison.admin.fttrmanage.v1.FttrManageService/CalculateAlertNumber");
  assert.deepEqual(calls.at(-1)[1], { deviceIds: ["device-id"] });
  assert.equal(result.data.unread, 1);
});

test("markAlertsAsRead writes operator alert IDs", async () => {
  const calls = [];
  await markAlertsAsRead(fakeAlertClient(calls), {
    alert_ids: ["alert-id", "alert-id", "alert-2"],
  });

  assert.deepEqual(calls, [
    ["/bison.admin.fttrmanage.v1.FttrManageService/MarkAlertsAsRead", {
      alertsIds: ["alert-id", "alert-2"],
    }],
  ]);
});

function fakeAlertClient(calls = []) {
  return {
    async unary(procedure, body) {
      calls.push([procedure, body]);
      if (procedure === "/bison.admin.fttrmanage.v1.FttrManageService/ListAlerts") {
        return {
          items: [{ alertContent: alertContent(), device: device(), hasRead: false }],
        };
      }
      if (procedure === "/bison.admin.fttrmanage.v1.FttrManageService/GetAlertDetail") {
        return { item: { alertContent: alertContent(body.id), device: device(), hasRead: false } };
      }
      if (procedure === "/bison.admin.device.v1.DeviceService/GetDeviceDetail") {
        return { device: device() };
      }
      if (procedure === "/bison.admin.fttrmanage.v1.FttrManageService/CalculateAlertNumber") {
        return { counters: { "device-id": { total: 3, unread: 1 } } };
      }
      if (procedure === "/bison.admin.fttrmanage.v1.FttrManageService/MarkAlertsAsRead") {
        return {};
      }
      throw new Error(`unexpected procedure ${procedure}`);
    },
  };
}

function device() {
  return {
    id: "device-id",
    mac: "AABBCCDDEEFF",
    sn: "SN001",
    kind: "DEVICE_KIND_MASTER",
  };
}

function alertContent(id = "alert-id") {
  return {
    id,
    eventName: { code: "LOS", name: "光链路告警" },
    eventType: "EVENT_TYPE_ALARM",
    eventTarget: { deviceId: "device-id" },
    displayMessage: "光链路中断",
  };
}
