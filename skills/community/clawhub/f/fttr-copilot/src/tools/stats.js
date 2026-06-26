import { getDeviceDetail, listMyDevices, resolveDevice } from "./devices.js";

export async function getDeviceStats(client) {
  const devicesResult = await listMyDevices(client);
  const devices = devicesResult.data.devices;
  const details = await loadDeviceDetails(client, devices);
  const online = details.filter((item) => item.detail.online_status_label === "在线").length;
  const offline = details.filter((item) => item.detail.online_status_label === "离线").length;
  const faulty = details.filter((item) => item.detail.system_profile.fault_codes.length > 0).length;

  return {
    title: "Customer 绑定设备统计",
    summary: `当前账号绑定 ${devices.length} 台设备，在线 ${online} 台，离线 ${offline} 台，存在故障码 ${faulty} 台。`,
    data: {
      scope: "customer_bound_devices",
      total: devices.length,
      online,
      offline,
      unknown: Math.max(devices.length - online - offline, 0),
      faulty,
      master_devices: devices.filter((item) => String(item.kind).includes("MASTER")).length,
      slave_count: devices.reduce((sum, item) => sum + Number(item.slave_count || 0), 0),
      devices: details.map(({ device, detail }) => ({
        id: device.id,
        mac: detail.mac || device.mac,
        alias: device.alias,
        kind: device.kind,
        online_status: detail.online_status_label,
        fault_codes: detail.system_profile.fault_codes,
      })),
    },
    suggestions: faulty > 0
      ? ["存在故障码设备时，可继续调用 get_fault_counter 或针对单台设备调用 get_device_load。"]
      : ["可继续查询网络拓扑、体验评分或下挂设备指标。"],
  };
}

export async function getDeviceLoad(client, args = {}) {
  const detailResult = await getDeviceDetail(client, args);
  const detail = detailResult.data.detail;
  const profile = detail.system_profile;

  return {
    title: "设备基础负载",
    summary: `设备 ${detail.alias || detail.mac || detail.id} CPU ${profile.cpu_occupation || "未知"}，内存 ${profile.memory_occupation || "未知"}。`,
    data: {
      device_identifier: args.device_identifier,
      resolved_device: detailResult.data.resolved_device,
      load_type: "basic",
      online_status: detail.online_status_label,
      cpu_occupation: profile.cpu_occupation,
      memory_occupation: profile.memory_occupation,
      last_reset_reason: profile.last_reset_reason,
      last_reset_terminal: profile.last_reset_terminal,
      last_offline_reason: profile.last_offline_reason,
      fault_codes: profile.fault_codes,
      raw: detailResult.data.raw,
    },
    suggestions: profile.fault_codes.length > 0
      ? ["设备存在故障码，建议结合最近告警和离线原因继续排查。"]
      : ["基础负载无明显故障码时，可继续查询网络体验或下挂设备指标。"],
  };
}

export async function getFaultCounter(client) {
  const devicesResult = await listMyDevices(client);
  const devices = devicesResult.data.devices;
  const details = await loadDeviceDetails(client, devices);
  const counters = new Map();

  for (const { detail } of details) {
    for (const code of detail.system_profile.fault_codes) {
      const key = String(code);
      counters.set(key, (counters.get(key) || 0) + 1);
    }
  }

  const faultCounters = [...counters.entries()]
    .sort(([left], [right]) => left.localeCompare(right))
    .map(([code, deviceCount]) => ({ code, device_count: deviceCount }));
  const faultyDevices = details.filter((item) => item.detail.system_profile.fault_codes.length > 0);

  return {
    title: "Customer 绑定设备故障统计",
    summary: faultyDevices.length === 0
      ? "当前账号绑定设备未返回故障码。"
      : `发现 ${faultyDevices.length} 台设备存在故障码，共 ${faultCounters.length} 类故障码。`,
    data: {
      scope: "customer_bound_devices",
      faulty_device_count: faultyDevices.length,
      counters: faultCounters,
      devices: faultyDevices.map(({ device, detail }) => ({
        id: device.id,
        mac: detail.mac || device.mac,
        alias: device.alias,
        fault_codes: detail.system_profile.fault_codes,
      })),
    },
    suggestions: faultyDevices.length > 0
      ? ["可针对存在故障码的设备调用 get_device_detail、get_device_load 或 diagnose_device_offline。"]
      : ["如果现场仍有异常，继续查询告警、拓扑和网络体验。"],
  };
}

async function loadDeviceDetails(client, devices) {
  const details = [];
  for (const device of devices) {
    try {
      const resolved = device.id ? { id: device.id, mac: device.mac, alias: device.alias } : await resolveDevice(client, device.mac);
      const detailResult = await getDeviceDetail(client, { device_identifier: resolved.id || device.mac });
      details.push({ device, detail: detailResult.data.detail });
    } catch (error) {
      details.push({
        device,
        detail: {
          id: device.id,
          mac: device.mac,
          alias: device.alias,
          online_status_label: "未知",
          system_profile: {
            cpu_occupation: "",
            memory_occupation: "",
            last_reset_reason: "",
            last_reset_terminal: "",
            last_offline_reason: "",
            fault_codes: [],
          },
          error: error.message,
        },
      });
    }
  }
  return details;
}
