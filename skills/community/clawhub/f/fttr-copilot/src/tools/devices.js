const LIST_MY_DEVICES = "/bison.device.v1.DeviceService/ListMyDevices";
const GET_DEVICE_DETAIL = "/bison.device.v1.DeviceService/GetDeviceDetail";
const UPDATE_DEVICE_ALIAS = "/bison.device.v1.DeviceService/UpdateDeviceAlias";

export async function listMyDevices(client) {
  const response = await client.unary(LIST_MY_DEVICES, {});
  const devices = Array.isArray(response.devices) ? response.devices.map(formatMyDevice) : [];

  return {
    title: "绑定设备列表",
    summary: devices.length === 0 ? "当前账号没有绑定设备。" : `当前账号绑定了 ${devices.length} 个设备。`,
    data: {
      devices,
      raw: response,
    },
    suggestions: devices.length === 0
      ? ["确认当前 token 对应的 FTTRAI 用户是否已绑定 FTTR 设备。"]
      : ["后续查询设备详情、拓扑或诊断时，可使用设备 ID、MAC 或别名。"],
  };
}

export async function getDeviceDetail(client, args = {}) {
  const resolved = await resolveDevice(client, args.device_identifier);
  const response = await client.unary(GET_DEVICE_DETAIL, { deviceId: resolved.id });
  const detail = formatDeviceDetail(response, resolved);

  return {
    title: "设备详情",
    summary: buildDeviceDetailSummary(detail),
    data: {
      device_identifier: args.device_identifier,
      resolved_device: resolved,
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
    title: "设备在线状态",
    summary: `设备 ${detail.alias || detail.mac || detail.id} 当前状态: ${detail.online_status_label}`,
    data: {
      device_identifier: args.device_identifier,
      resolved_device: result.data.resolved_device,
      online_status: detail.online_status,
      online_status_label: detail.online_status_label,
      last_seen: detail.last_seen,
      ip_addr: detail.ip_addr,
      raw: result.data.raw,
    },
    suggestions: detail.online_status_label === "离线"
      ? ["设备离线时，建议继续执行离线诊断，结合最近告警和链路状态排查。"]
      : ["如用户仍反馈异常，继续查询网络拓扑、下挂设备指标或最近告警。"],
  };
}

export async function updateDeviceAlias(client, args = {}) {
  const newAlias = String(args.new_alias || "").trim();
  if (!newAlias) {
    const err = new Error("new_alias 不能为空");
    err.code = "invalid_argument";
    throw err;
  }
  if (newAlias.length > 20) {
    const err = new Error("new_alias 不能超过 20 个字符");
    err.code = "invalid_argument";
    throw err;
  }

  const resolved = await resolveDevice(client, args.device_identifier);
  await client.unary(UPDATE_DEVICE_ALIAS, {
    deviceId: resolved.id,
    alias: newAlias,
  });

  return {
    title: "设备别名已更新",
    summary: `设备 ${resolved.mac || resolved.id} 的别名已更新为「${newAlias}」。`,
    data: {
      device_identifier: args.device_identifier,
      resolved_device: resolved,
      new_alias: newAlias,
    },
    suggestions: ["后续可使用新的设备别名查询详情、拓扑或发起诊断。"],
  };
}

export async function resolveDevice(client, identifier) {
  const trimmed = String(identifier || "").trim();
  if (!trimmed) {
    const err = new Error("device_identifier 不能为空");
    err.code = "invalid_argument";
    throw err;
  }

  if (isUuid(trimmed)) {
    return {
      id: trimmed,
      mac: "",
      alias: "",
      matched_by: "id",
    };
  }

  const response = await client.unary(LIST_MY_DEVICES, {});
  const devices = Array.isArray(response.devices) ? response.devices.map(formatMyDevice) : [];
  const normalized = normalizeDeviceIdentifier(trimmed);

  for (const device of devices) {
    if (normalizeDeviceIdentifier(device.id) === normalized) {
      return { ...device, matched_by: "id" };
    }
    if (normalizeDeviceIdentifier(device.mac) === normalized) {
      return { ...device, matched_by: "mac" };
    }
    if (String(device.alias || "").trim().toLowerCase() === trimmed.toLowerCase()) {
      return { ...device, matched_by: "alias" };
    }
  }

  const err = new Error(`未找到设备: ${trimmed}`);
  err.code = "not_found";
  throw err;
}

function formatMyDevice(item) {
  const device = item.device || {};
  return {
    id: device.id || "",
    mac: device.mac || "",
    sn: device.sn || "",
    kind: device.kind || "",
    alias: item.alias || "",
    role: item.role || "",
    slave_count: item.slaveCount ?? item.slave_count ?? 0,
    bind_at: item.bindAt || item.bind_at || null,
  };
}

function formatDeviceDetail(response, resolved) {
  const device = response.device || {};
  const factoryInfo = response.factoryInfo || response.factory_info || {};
  const connectStatus = response.connectStatus || response.connect_status || {};
  const systemProfile = response.systemProfile || response.system_profile || {};

  const onlineStatus = connectStatus.onlineStatus ?? connectStatus.online_status ?? "";

  return {
    id: device.id || resolved.id || "",
    mac: device.mac || resolved.mac || "",
    sn: device.sn || "",
    kind: device.kind || "",
    alias: resolved.alias || "",
    online_status: onlineStatus,
    online_status_label: onlineStatusLabel(onlineStatus),
    last_seen: connectStatus.lastSeen || connectStatus.last_seen || null,
    ip_addr: connectStatus.ipAddr || connectStatus.ip_addr || "",
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
  };
}

function buildDeviceDetailSummary(detail) {
  const name = detail.alias || detail.mac || detail.id;
  return `设备 ${name} 当前状态: ${detail.online_status_label}。`;
}

function buildDeviceDetailSuggestions(detail) {
  if (detail.online_status_label === "离线") {
    return ["建议继续查询最近告警，或执行离线诊断工作流。"];
  }
  if (detail.system_profile?.fault_codes?.length > 0) {
    return ["设备存在故障码，建议继续查询告警详情或故障统计。"];
  }
  return ["可继续查询网络拓扑、下挂设备指标或网络体验评分。"];
}

function onlineStatusLabel(value) {
  if (value === 1 || value === "1" || value === "ONLINE_STATUS_ONLINE") {
    return "在线";
  }
  if (value === 2 || value === "2" || value === "ONLINE_STATUS_OFFLINE") {
    return "离线";
  }
  return "未知";
}

function normalizeDeviceIdentifier(value) {
  return String(value || "").trim().toLowerCase().replace(/[:.\-\s]/g, "");
}

function isUuid(value) {
  return /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(value);
}
