const LIST_DEVICE_ALERTS = "/bison.device.v1.DeviceService/ListDeviceAlerts";

export async function listDeviceAlerts(client, args = {}) {
  const request = {
    pagination: {
      limit: clampLimit(args.limit, 20),
    },
  };

  if (args.cursor) {
    request.pagination.cursor = String(args.cursor);
  }
  if (args.event_code) {
    request.eventCode = String(args.event_code);
  }
  if (args.event_type) {
    request.eventType = normalizeEventType(args.event_type);
  }

  const response = await client.unary(LIST_DEVICE_ALERTS, request);
  const alerts = Array.isArray(response.items) ? response.items.map(formatAlertItem) : [];

  return {
    title: "设备告警列表",
    summary: alerts.length === 0 ? "未查询到告警记录。" : `查询到 ${alerts.length} 条告警记录。`,
    data: {
      filters: {
        event_type: request.eventType || "",
        event_code: request.eventCode || "",
      },
      alerts,
      next_cursor: response.nextCursor || response.next_cursor || "",
      raw: response,
    },
    suggestions: alerts.length === 0
      ? ["可放宽事件类型、事件编码或分页条件后重试。"]
      : ["如需排查告警对应设备，可使用告警中的设备 MAC 查询设备详情或网络拓扑。"],
  };
}

function formatAlertItem(item) {
  const alert = item.alertContent || item.alert_content || {};
  const device = item.device || {};
  const eventName = alert.eventName || alert.event_name || {};
  const eventTarget = alert.eventTarget || alert.event_target || {};

  return {
    id: alert.id || "",
    event_name: {
      code: eventName.code || "",
      name: eventName.name || "",
    },
    event_type: alert.eventType || alert.event_type || "",
    parameters: alert.parameters || "",
    event_time: alert.eventTime || alert.event_time || null,
    time_interval: alert.timeInterval || alert.time_interval || null,
    event_target: {
      device_id: eventTarget.deviceId || eventTarget.device_id || "",
      device_name: eventTarget.deviceName || eventTarget.device_name || "",
    },
    display_message: alert.displayMessage || alert.display_message || "",
    record_at: alert.recordAt || alert.record_at || null,
    has_read: Boolean(item.hasRead ?? item.has_read),
    device: {
      id: device.id || "",
      mac: device.mac || "",
      sn: device.sn || "",
      kind: device.kind || "",
    },
  };
}

function normalizeEventType(value) {
  const normalized = String(value).trim().toUpperCase();
  if (["ALARM", "ALERT", "EVENT_TYPE_ALARM"].includes(normalized)) {
    return "EVENT_TYPE_ALARM";
  }
  if (["EVENT", "EVENT_TYPE_EVENT"].includes(normalized)) {
    return "EVENT_TYPE_EVENT";
  }
  if (["UNSPECIFIED", "EVENT_TYPE_UNSPECIFIED"].includes(normalized)) {
    return "EVENT_TYPE_UNSPECIFIED";
  }

  const err = new Error("event_type 仅支持 ALARM/ALERT 或 EVENT");
  err.code = "invalid_argument";
  throw err;
}

function clampLimit(value, fallback) {
  const parsed = Number.parseInt(String(value || ""), 10);
  if (!Number.isFinite(parsed) || parsed <= 0) {
    return fallback;
  }
  return Math.min(parsed, 100);
}
