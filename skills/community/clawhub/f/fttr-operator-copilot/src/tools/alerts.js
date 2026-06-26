import { resolveDevice } from "./devices.js";

const LIST_ALERTS = "/bison.admin.fttrmanage.v1.FttrManageService/ListAlerts";
const GET_ALERT_DETAIL = "/bison.admin.fttrmanage.v1.FttrManageService/GetAlertDetail";
const CALCULATE_ALERT_NUMBER = "/bison.admin.fttrmanage.v1.FttrManageService/CalculateAlertNumber";
const MARK_ALERTS_AS_READ = "/bison.admin.fttrmanage.v1.FttrManageService/MarkAlertsAsRead";

export async function listDeviceAlerts(client, args = {}) {
  const request = {
    pagination: {
      limit: clampLimit(args.limit, 20),
    },
  };

  if (args.cursor) request.pagination.cursor = String(args.cursor);
  if (args.region_code) request.regionCode = String(args.region_code);
  if (args.event_code) request.eventCode = String(args.event_code);
  if (args.event_type) request.eventType = normalizeEventType(args.event_type);

  let resolved = null;
  if (String(args.device_identifier || "").trim()) {
    resolved = await resolveDevice(client, args.device_identifier);
    request.mac = resolved.mac;
  } else if (args.mac) {
    request.mac = String(args.mac).trim();
  }

  const response = await client.unary(LIST_ALERTS, request);
  const alerts = Array.isArray(response.items) ? response.items.map(formatAlertItem) : [];

  return {
    title: "Operator 设备告警列表",
    summary: alerts.length === 0 ? "未查询到告警记录。" : `查询到 ${alerts.length} 条告警记录。`,
    data: {
      filters: {
        device_identifier: args.device_identifier || "",
        region_code: request.regionCode || "",
        event_type: request.eventType || "",
        event_code: request.eventCode || "",
      },
      resolved_device: resolved,
      alerts,
      next_cursor: response.nextCursor || response.next_cursor || "",
      raw: response,
    },
    suggestions: alerts.length === 0
      ? ["可放宽设备、区域、事件类型或分页条件后重试。"]
      : ["可继续调用 get_alert_detail 查看详情，或调用 mark_alerts_as_read 标记已读。"],
  };
}

export async function getAlertDetail(client, args = {}) {
  const alertID = requiredString(args.alert_id, "alert_id");
  const response = await client.unary(GET_ALERT_DETAIL, { id: alertID });
  const item = formatAlertItem(response.item || {});

  return {
    title: "Operator 告警详情",
    summary: item.display_message || item.event_name.name || item.event_name.code || `告警 ${alertID}`,
    data: {
      alert_id: alertID,
      alert: item,
      raw: response,
    },
    suggestions: item.has_read
      ? ["该告警已读；可结合设备详情、拓扑、负载或网络体验继续分析。"]
      : ["确认告警后，可调用 mark_alerts_as_read 标记为已读。"],
  };
}

export async function calculateAlertNumber(client, args = {}) {
  const identifiers = args.device_identifiers;
  if (!Array.isArray(identifiers) || identifiers.length === 0) {
    const err = new Error("device_identifiers 必须是非空数组");
    err.code = "invalid_argument";
    throw err;
  }

  const resolvedDevices = [];
  for (const identifier of identifiers) {
    resolvedDevices.push(await resolveDevice(client, identifier));
  }
  const deviceIds = [...new Set(resolvedDevices.map((device) => device.id).filter(Boolean))];
  const response = await client.unary(CALCULATE_ALERT_NUMBER, { deviceIds });
  const counters = formatCounters(response.counters || {});
  const total = counters.reduce((sum, counter) => sum + counter.total, 0);
  const unread = counters.reduce((sum, counter) => sum + counter.unread, 0);

  return {
    title: "Operator 告警数量统计",
    summary: `共统计 ${deviceIds.length} 台设备，告警 ${total} 条，其中未读 ${unread} 条。`,
    data: {
      requested_identifiers: identifiers,
      resolved_devices: resolvedDevices,
      counters,
      total,
      unread,
      raw: response,
    },
    suggestions: unread > 0
      ? ["可查询未读告警详情，确认后调用 mark_alerts_as_read 标记已读。"]
      : ["当前统计范围内没有未读告警。"],
  };
}

export async function markAlertsAsRead(client, args = {}) {
  const alertIDs = args.alert_ids;
  if (!Array.isArray(alertIDs) || alertIDs.length === 0) {
    const err = new Error("alert_ids 必须是非空数组");
    err.code = "invalid_argument";
    throw err;
  }

  const normalizedIDs = [...new Set(alertIDs.map((id) => String(id).trim()).filter(Boolean))];
  if (normalizedIDs.length === 0) {
    const err = new Error("alert_ids 不能全为空");
    err.code = "invalid_argument";
    throw err;
  }

  await client.unary(MARK_ALERTS_AS_READ, { alertsIds: normalizedIDs });

  return {
    title: "Operator 告警已标记为已读",
    summary: `已标记 ${normalizedIDs.length} 条告警为已读。`,
    data: {
      alert_ids: normalizedIDs,
    },
    suggestions: ["可重新查询告警数量，确认未读数量是否已更新。"],
  };
}

export function formatAlertItem(item) {
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

function formatCounters(counters) {
  return Object.entries(counters).map(([deviceID, counter]) => ({
    device_id: deviceID,
    total: Number(counter.total || 0),
    unread: Number(counter.unread || 0),
  }));
}

function normalizeEventType(value) {
  const normalized = String(value).trim().toUpperCase();
  if (["ALARM", "ALERT", "EVENT_TYPE_ALARM"].includes(normalized)) return "EVENT_TYPE_ALARM";
  if (["EVENT", "EVENT_TYPE_EVENT"].includes(normalized)) return "EVENT_TYPE_EVENT";
  if (["UNSPECIFIED", "EVENT_TYPE_UNSPECIFIED"].includes(normalized)) return "EVENT_TYPE_UNSPECIFIED";

  const err = new Error("event_type 仅支持 ALARM/ALERT 或 EVENT");
  err.code = "invalid_argument";
  throw err;
}

function clampLimit(value, fallback) {
  const parsed = Number.parseInt(String(value || ""), 10);
  if (!Number.isFinite(parsed) || parsed <= 0) return fallback;
  return Math.min(parsed, 100);
}

function requiredString(value, fieldName) {
  const trimmed = String(value || "").trim();
  if (!trimmed) {
    const err = new Error(`${fieldName} 不能为空`);
    err.code = "invalid_argument";
    throw err;
  }
  return trimmed;
}
