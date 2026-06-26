const LIST_DEVICES = "/bison.admin.device.v1.DeviceService/ListDevices";
const GET_DEVICE_DETAIL = "/bison.admin.device.v1.DeviceService/GetDeviceDetail";

export async function listDevices(client, args = {}) {
  const request = buildListDevicesRequest(args);
  const response = await client.unary(LIST_DEVICES, request);
  const devices = Array.isArray(response.items) ? response.items.map(formatListDeviceItem) : [];

  return {
    title: "Operator 设备列表",
    summary: `查询到 ${devices.length} 台设备，总数 ${response.totalCount ?? response.total_count ?? devices.length}。`,
    data: {
      filters: request,
      devices,
      total_count: response.totalCount ?? response.total_count ?? devices.length,
      raw: response,
    },
    suggestions: devices.length === 0
      ? ["可放宽区域、在线状态、MAC、SN 或设备类型过滤条件。"]
      : ["后续可使用设备 ID、MAC 或 SN 查询详情、告警、拓扑或下发实时查询命令。"],
  };
}

export async function getDeviceDetail(client, args = {}) {
  const request = await detailRequestFromIdentifier(client, args.device_identifier);
  const response = await client.unary(GET_DEVICE_DETAIL, request);
  const detail = formatDeviceDetail(response, {
    id: request.id || "",
    mac: request.mac || "",
  });

  return {
    title: "Operator 设备详情",
    summary: buildDeviceDetailSummary(detail),
    data: {
      device_identifier: args.device_identifier,
      resolved_device: {
        id: detail.id,
        mac: detail.mac,
        sn: detail.sn,
        matched_by: request.id ? "id" : "mac",
      },
      detail,
      raw: response,
    },
    suggestions: buildDeviceDetailSuggestions(detail),
  };
}

export async function getDeviceOnlineStatus(client, args = {}) {
  const result = await getDeviceDetail(client, args);
  const detail = result.data.detail;

  return {
    title: "Operator 设备在线状态",
    summary: `设备 ${detail.mac || detail.id} 当前状态: ${detail.online_status_label}`,
    data: {
      device_identifier: args.device_identifier,
      resolved_device: result.data.resolved_device,
      online_status: detail.online_status,
      online_status_label: detail.online_status_label,
      last_seen: detail.last_seen,
      last_online_ip: detail.last_online_ip,
      raw: result.data.raw,
    },
    suggestions: detail.online_status_label === "离线"
      ? ["设备离线时，建议继续查询最近告警、故障统计或下发实时查询命令确认。"]
      : ["如仍有现场异常，可继续查询网络拓扑、下挂设备指标或最近告警。"],
  };
}

export async function resolveDevice(client, identifier) {
  const trimmed = requiredString(identifier, "device_identifier");

  if (isUuid(trimmed)) {
    const response = await client.unary(GET_DEVICE_DETAIL, { id: trimmed });
    const detail = formatDeviceDetail(response, { id: trimmed });
    return {
      id: detail.id || trimmed,
      mac: detail.mac,
      sn: detail.sn,
      kind: detail.kind,
      matched_by: "id",
    };
  }

  if (looksLikeMac(trimmed)) {
    const mac = normalizeMac(trimmed);
    const response = await client.unary(GET_DEVICE_DETAIL, { mac });
    const detail = formatDeviceDetail(response, { mac });
    return {
      id: detail.id,
      mac: detail.mac || mac,
      sn: detail.sn,
      kind: detail.kind,
      matched_by: "mac",
    };
  }

  const response = await client.unary(LIST_DEVICES, {
    pagination: { page: 1, limit: 10 },
    sn: trimmed,
  });
  const devices = Array.isArray(response.items) ? response.items.map(formatListDeviceItem) : [];
  if (devices.length > 0) {
    return {
      id: devices[0].id,
      mac: devices[0].mac,
      sn: devices[0].sn,
      kind: devices[0].kind,
      matched_by: "sn",
    };
  }

  const err = new Error(`未找到设备: ${trimmed}`);
  err.code = "not_found";
  throw err;
}

function buildListDevicesRequest(args) {
  const request = {
    pagination: {
      page: positiveInt(args.page, 1),
      limit: clampLimit(args.limit, 20),
    },
  };

  copyString(args, request, "mac", "mac", normalizeMacIfPresent);
  copyString(args, request, "region_code", "regionCode");
  copyString(args, request, "online_status", "onlineStatus", normalizeOnlineStatus);
  copyString(args, request, "kind", "kind", normalizeDeviceKind);
  copyString(args, request, "pppoe_account", "pppoeAccount");
  copyString(args, request, "sn", "sn");
  copyString(args, request, "product_class", "productClass");
  copyString(args, request, "hardware_version", "hardwareVersion");
  copyString(args, request, "software_version", "softwareVersion");
  copyString(args, request, "software_date", "softwareDate");
  copyString(args, request, "activation_state", "activationState");
  copyString(args, request, "region_source", "regionSource", normalizeRegionSource);

  if (args.fault_code !== undefined && args.fault_code !== "") {
    request.faultCode = Number.parseInt(String(args.fault_code), 10);
  }
  if (args.only_cross_region !== undefined) {
    request.onlyCrossRegion = Boolean(args.only_cross_region);
  }
  return request;
}

async function detailRequestFromIdentifier(client, identifier) {
  const trimmed = requiredString(identifier, "device_identifier");
  if (isUuid(trimmed)) {
    return { id: trimmed };
  }
  if (looksLikeMac(trimmed)) {
    return { mac: normalizeMac(trimmed) };
  }
  const resolved = await resolveDevice(client, trimmed);
  return resolved.id ? { id: resolved.id } : { mac: resolved.mac };
}

function formatListDeviceItem(item) {
  const device = item.devices || item.device || {};
  const detail = formatDeviceDetail({
    device,
    factoryInfo: item.factoryInfo || item.factory_info,
    connectStatus: item.connectStatus || item.connect_status,
    systemProfile: item.systemProfile || item.system_profile,
    region: item.region,
    lastOnlineRegion: item.ipRegion || item.ip_region,
    activationState: item.activationState || item.activation_state,
  }, {});
  return {
    ...detail,
    activation_state: item.activationState || item.activation_state || detail.activation_state,
  };
}

function formatDeviceDetail(response, resolved) {
  const device = response.device || {};
  const factoryInfo = response.factoryInfo || response.factory_info || {};
  const connectStatus = response.connectStatus || response.connect_status || {};
  const systemProfile = response.systemProfile || response.system_profile || {};
  const region = response.region || {};
  const lastOnlineRegion = response.lastOnlineRegion || response.last_online_region || response.ipRegion || response.ip_region || {};
  const onlineStatus = connectStatus.onlineStatus ?? connectStatus.online_status ?? "";

  return {
    id: device.id || resolved.id || "",
    mac: device.mac || resolved.mac || "",
    sn: device.sn || "",
    kind: device.kind || "",
    online_status: onlineStatus,
    online_status_label: onlineStatusLabel(onlineStatus),
    last_seen: connectStatus.lastSeen || connectStatus.last_seen || null,
    last_online_ip: response.lastOnlineIp || response.last_online_ip || connectStatus.ipAddr || connectStatus.ip_addr || "",
    region: formatRegion(region),
    last_online_region: formatRegion(lastOnlineRegion),
    factory_info: {
      vendor: factoryInfo.vendor || "",
      firmware_ver: factoryInfo.firmwareVer || factoryInfo.firmware_ver || "",
      hardware_ver: factoryInfo.hardwareVer || factoryInfo.hardware_ver || "",
      software_ver: factoryInfo.softwareVer || factoryInfo.software_ver || "",
      manufacturer: factoryInfo.manufacturer || "",
      product_class: factoryInfo.productClass || factoryInfo.product_class || "",
      wifi_bands_capability: factoryInfo.wifiBandsCapability || factoryInfo.wifi_bands_capability || "",
      uplink_type: factoryInfo.uplinkType || factoryInfo.uplink_type || "",
    },
    system_profile: {
      cpu_occupation: systemProfile.cpuOccupation || systemProfile.cpu_occupation || "",
      memory_occupation: systemProfile.memoryOccupation || systemProfile.memory_occupation || "",
      last_reset_reason: systemProfile.lastResetReason || systemProfile.last_reset_reason || "",
      last_reset_terminal: systemProfile.lastResetTerminal || systemProfile.last_reset_terminal || "",
      last_offline_reason: systemProfile.lastOfflineReason || systemProfile.last_offline_reason || "",
      fault_codes: systemProfile.faultCodes || systemProfile.fault_codes || [],
    },
    first_register_at: response.firstRegisterAt || response.first_register_at || null,
    activation_state: response.activationState || response.activation_state || "",
  };
}

function formatRegion(region) {
  return {
    code: region.code || region.regionCode || region.region_code || "",
    name: region.name || region.regionName || region.region_name || "",
    full_name: region.fullName || region.full_name || "",
  };
}

function buildDeviceDetailSummary(detail) {
  return `设备 ${detail.mac || detail.id} 当前状态: ${detail.online_status_label}。`;
}

function buildDeviceDetailSuggestions(detail) {
  if (detail.online_status_label === "离线") {
    return ["建议继续查询最近告警、故障统计或命令历史。"];
  }
  if (detail.system_profile?.fault_codes?.length > 0) {
    return ["设备存在故障码，建议继续查询告警详情或故障统计。"];
  }
  return ["可继续查询网络拓扑、下挂设备指标、负载趋势或网络体验评分。"];
}

function copyString(source, target, sourceKey, targetKey, normalize = String) {
  const value = source[sourceKey];
  if (value !== undefined && value !== null && String(value).trim() !== "") {
    target[targetKey] = normalize(value);
  }
}

function normalizeOnlineStatus(value) {
  const normalized = String(value).trim().toUpperCase();
  if (["ONLINE", "ONLINE_STATUS_ONLINE", "1"].includes(normalized)) return "ONLINE_STATUS_ONLINE";
  if (["OFFLINE", "ONLINE_STATUS_OFFLINE", "2"].includes(normalized)) return "ONLINE_STATUS_OFFLINE";
  return normalized;
}

function normalizeDeviceKind(value) {
  const normalized = String(value).trim().toUpperCase();
  if (["MASTER", "DEVICE_KIND_MASTER", "1"].includes(normalized)) return "DEVICE_KIND_MASTER";
  if (["SLAVE", "DEVICE_KIND_SLAVE", "2"].includes(normalized)) return "DEVICE_KIND_SLAVE";
  return normalized;
}

function normalizeRegionSource(value) {
  const normalized = String(value).trim().toUpperCase();
  if (["REGISTERED_IP", "REGION_SOURCE_REGISTERED_IP"].includes(normalized)) return "REGION_SOURCE_REGISTERED_IP";
  if (["DELIVERY", "REGION_SOURCE_DELIVERY"].includes(normalized)) return "REGION_SOURCE_DELIVERY";
  return normalized;
}

function onlineStatusLabel(value) {
  if (value === 1 || value === "1" || value === "ONLINE_STATUS_ONLINE") return "在线";
  if (value === 2 || value === "2" || value === "ONLINE_STATUS_OFFLINE") return "离线";
  return "未知";
}

function normalizeMacIfPresent(value) {
  return looksLikeMac(value) ? normalizeMac(value) : String(value).trim();
}

export function normalizeMac(value) {
  return String(value || "").trim().toUpperCase().replace(/[:.\-\s]/g, "");
}

function looksLikeMac(value) {
  return /^[0-9a-f:.\-\s]{12,20}$/i.test(String(value || "").trim()) && normalizeMac(value).length === 12;
}

function positiveInt(value, fallback) {
  const parsed = Number.parseInt(String(value || ""), 10);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : fallback;
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

function isUuid(value) {
  return /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{12}$/i.test(value);
}
