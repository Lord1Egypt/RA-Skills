import assert from "node:assert/strict";
import test from "node:test";

import { listDeviceAlerts } from "../src/tools/alerts.js";

test("listDeviceAlerts sends customer device alert list request", async () => {
  const calls = [];
  const result = await listDeviceAlerts(fakeAlertClient(calls), {
    event_type: "ALERT",
    event_code: "LOS",
    limit: 10,
  });

  assert.deepEqual(calls, [
    ["/bison.device.v1.DeviceService/ListDeviceAlerts", {
      pagination: { limit: 10 },
      eventCode: "LOS",
      eventType: "EVENT_TYPE_ALARM",
    }],
  ]);
  assert.equal(result.data.alerts.length, 1);
  assert.equal(result.data.alerts[0].event_name.code, "LOS");
  assert.equal(result.data.next_cursor, "cursor-2");
});

test("listDeviceAlerts supports cursor and clamps page size", async () => {
  const calls = [];
  await listDeviceAlerts(fakeAlertClient(calls), {
    cursor: "cursor-1",
    event_type: "EVENT",
    limit: 999,
  });

  assert.deepEqual(calls, [
    ["/bison.device.v1.DeviceService/ListDeviceAlerts", {
      pagination: { limit: 100, cursor: "cursor-1" },
      eventType: "EVENT_TYPE_EVENT",
    }],
  ]);
});

test("listDeviceAlerts rejects unsupported event type", async () => {
  await assert.rejects(
    () => listDeviceAlerts(fakeAlertClient(), { event_type: "NOTICE" }),
    /event_type 仅支持 ALARM\/ALERT 或 EVENT/,
  );
});

function fakeAlertClient(calls = []) {
  return {
    async unary(procedure, body) {
      calls.push([procedure, body]);
      if (procedure === "/bison.device.v1.DeviceService/ListDeviceAlerts") {
        return {
          items: [
            {
              alertContent: alertContent(),
              device: { id: "device-id", mac: "AA:BB:CC:DD:EE:FF", kind: "KIND_MASTER" },
            },
          ],
          nextCursor: "cursor-2",
        };
      }
      throw new Error(`unexpected procedure ${procedure}`);
    },
  };
}

function alertContent() {
  return {
    id: "alert-id",
    eventName: { code: "LOS", name: "光链路告警" },
    eventType: "EVENT_TYPE_ALARM",
    parameters: "{}",
    eventTime: "2026-05-15T08:00:00Z",
    eventTarget: {
      deviceId: "AA:BB:CC:DD:EE:FF",
      deviceName: "",
    },
    displayMessage: "光链路中断",
    recordAt: "2026-05-15T08:00:01Z",
  };
}
