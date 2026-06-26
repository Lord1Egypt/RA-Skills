import { normalizeMac, resolveDevice } from "./devices.js";

const GET_DEVICE_SUMMARY_STATS = "/bison.admin.devicestats.v1.DeviceStatsService/GetDeviceSummaryStats";
const GET_DEVICE_FAULT_STATS = "/bison.admin.devicestats.v1.DeviceStatsService/GetDeviceFaultStats";
const FETCH_DEVICE_LOAD = "/bison.admin.charts.v1.ChartsService/FetchDeviceLoad";

export async function getDeviceStats(client, args = {}) {
  const request = {};
  if (args.region_code) request.regionCode = String(args.region_code);
  if (args.region_source) request.regionSource = normalizeRegionSource(args.region_source);

  const response = await client.unary(GET_DEVICE_SUMMARY_STATS, request);
  const regionStats = Array.isArray(response.regionStats)
    ? response.regionStats.map(formatRegionStats)
    : Array.isArray(response.region_stats)
      ? response.region_stats.map(formatRegionStats)
      : [];

  return {
    title: "Operator 设备汇总统计",
    summary: `总设备 ${numberField(response.totalDevicesCount ?? response.total_devices_count)} 台，已注册 ${numberField(response.registeredDevicesCount ?? response.registered_devices_count)} 台，在线 ${numberField(response.onlineDevicesCount ?? response.online_devices_count)} 台。`,
    data: {
      filters: request,
      total_devices_count: numberField(response.totalDevicesCount ?? response.total_devices_count),
      registered_devices_count: numberField(response.registeredDevicesCount ?? response.registered_devices_count),
      online_devices_count: numberField(response.onlineDevicesCount ?? response.online_devices_count),
      region_stats: regionStats,
      raw: response,
    },
    suggestions: regionStats.length > 0
      ? ["可指定 region_code 下钻区域，或继续查询故障统计。"]
      : ["可继续查询故障统计、在线状态统计或设备列表。"],
  };
}

export async function getFaultCounter(client, args = {}) {
  const request = {};
  if (args.region_code) request.regionCode = String(args.region_code);
  if (args.region_source) request.regionSource = normalizeRegionSource(args.region_source);

  const response = await client.unary(GET_DEVICE_FAULT_STATS, request);
  const stats = Array.isArray(response.faultStats)
    ? response.faultStats.map(formatFaultStats)
    : Array.isArray(response.fault_stats)
      ? response.fault_stats.map(formatFaultStats)
      : [];
  const faulty = stats.reduce((sum, item) => sum + item.devices_with_any_errors, 0);

  return {
    title: "Operator 设备故障统计",
    summary: stats.length === 0
      ? "暂无设备故障统计数据。"
      : `查询到 ${stats.length} 个区域统计，故障设备 ${faulty} 台。`,
    data: {
      filters: request,
      last_update_time: response.lastUpdateTime || response.last_update_time || null,
      fault_stats: stats,
      raw: response,
    },
    suggestions: faulty > 0
      ? ["可按 region_code 下钻，或用 fault_code 过滤设备列表定位故障设备。"]
      : ["当前统计范围没有故障设备。"],
  };
}

export async function getDeviceLoad(client, args = {}) {
  const resolved = await resolveDevice(client, args.device_identifier);
  const request = buildFetchDeviceLoadRequest(resolved.mac, args);
  const response = await client.unary(FETCH_DEVICE_LOAD, request);
  const loadType = normalizeLoadType(args.load_type || "basic");

  return {
    title: "Operator 设备负载趋势",
    summary: `已查询设备 ${resolved.mac} 的 ${loadType} 负载数据。`,
    data: {
      device_identifier: args.device_identifier,
      resolved_device: resolved,
      load_type: loadType,
      time_range: {
        datetime_gte: request.datetimeGte,
        datetime_lte: request.datetimeLte,
      },
      load: formatDeviceLoad(response),
      raw: response,
    },
    suggestions: ["可调整 start_time/end_time 查询最近 30 天内的趋势，或切换 load_type 查询 optic、wireless_rssi、wireless_loads、station_rssi、station_counter。"],
  };
}

function buildFetchDeviceLoadRequest(mac, args) {
  const loadType = normalizeLoadType(args.load_type || "basic");
  const now = new Date();
  const end = args.end_time ? new Date(args.end_time) : now;
  const start = args.start_time ? new Date(args.start_time) : new Date(end.getTime() - 24 * 60 * 60 * 1000);
  const request = {
    networkId: normalizeMac(mac),
    datetimeGte: start.toISOString(),
    datetimeLte: end.toISOString(),
  };
  if (args.slave_mac) request.slaveMac = normalizeMac(args.slave_mac);

  if (loadType === "basic") request.basic = {};
  if (loadType === "optic") request.optic = {};
  if (loadType === "wireless_rssi") request.wireless = { rssi: true };
  if (loadType === "wireless_loads") request.wireless = { loads: true };
  if (loadType === "station_rssi") request.station = { rssi: true };
  if (loadType === "station_counter") request.station = { counter: true };
  return request;
}

function formatDeviceLoad(response) {
  return {
    basic_loads: response.basicLoads || response.basic_loads || null,
    optic_loads: response.opticLoads || response.optic_loads || null,
    wireless_loads: response.wirelessLoads || response.wireless_loads || null,
    station_loads: response.stationLoads || response.station_loads || null,
  };
}

function formatRegionStats(item) {
  return {
    region_code: item.regionCode || item.region_code || "",
    registered_devices_count: numberField(item.registeredDevicesCount ?? item.registered_devices_count),
    online_devices_count: numberField(item.onlineDevicesCount ?? item.online_devices_count),
    total_devices_count: numberField(item.totalDevicesCount ?? item.total_devices_count),
    new_devices_count: numberField(item.newDevicesCount ?? item.new_devices_count),
    new_registered_devices_count: numberField(item.newRegisteredDevicesCount ?? item.new_registered_devices_count),
  };
}

function formatFaultStats(item) {
  return {
    region_code: item.regionCode || item.region_code || "",
    master_devices_count: numberField(item.masterDevicesCount ?? item.master_devices_count),
    devices_with_any_errors: numberField(item.devicesWithAnyErrors ?? item.devices_with_any_errors),
    devices_with_err1: numberField(item.devicesWithErr1 ?? item.devices_with_err1),
    devices_with_err2: numberField(item.devicesWithErr2 ?? item.devices_with_err2),
    devices_with_err3: numberField(item.devicesWithErr3 ?? item.devices_with_err3),
    devices_with_err4: numberField(item.devicesWithErr4 ?? item.devices_with_err4),
    devices_with_err5: numberField(item.devicesWithErr5 ?? item.devices_with_err5),
    devices_with_err6: numberField(item.devicesWithErr6 ?? item.devices_with_err6),
    devices_with_err7: numberField(item.devicesWithErr7 ?? item.devices_with_err7),
    devices_with_err8: numberField(item.devicesWithErr8 ?? item.devices_with_err8),
    devices_with_err9: numberField(item.devicesWithErr9 ?? item.devices_with_err9),
    devices_with_err10: numberField(item.devicesWithErr10 ?? item.devices_with_err10),
  };
}

function normalizeLoadType(value) {
  const normalized = String(value).trim().toLowerCase();
  const supported = new Set(["basic", "optic", "wireless_rssi", "wireless_loads", "station_rssi", "station_counter"]);
  if (supported.has(normalized)) return normalized;
  const err = new Error("load_type 仅支持 basic/optic/wireless_rssi/wireless_loads/station_rssi/station_counter");
  err.code = "invalid_argument";
  throw err;
}

function normalizeRegionSource(value) {
  const normalized = String(value).trim().toUpperCase();
  if (["REGISTERED_IP", "REGION_SOURCE_REGISTERED_IP"].includes(normalized)) return "REGION_SOURCE_REGISTERED_IP";
  if (["DELIVERY", "REGION_SOURCE_DELIVERY"].includes(normalized)) return "REGION_SOURCE_DELIVERY";
  return normalized;
}

function numberField(value) {
  const number = Number(value || 0);
  return Number.isFinite(number) ? number : 0;
}
