import { getDeviceDetail, resolveDevice } from "./devices.js";

const LIST_NETWORK_TOPOLOGY = "/bison.networkstats.v1.NetworkStatsService/ListNetworkTopology";
const GET_STATION_STATS = "/bison.networkstats.v1.NetworkStatsService/GetStationStats";
const GET_NETWORK_EXPERIENCE = "/bison.networkstats.v1.NetworkStatsService/GetNetworkExperience";
const GET_STATION_EXPERIENCE = "/bison.networkstats.v1.NetworkStatsService/GetStationExperience";

export async function getNetworkTopology(client, args = {}) {
  const resolved = await resolveDeviceForMac(client, args.device_identifier);
  const response = await client.unary(LIST_NETWORK_TOPOLOGY, { mac: resolved.mac });
  const topology = formatTopology(response.topology || {});

  return {
    title: "网络拓扑",
    summary: `拓扑包含 ${topology.gateways.length} 个网关和 ${topology.stations.length} 个下挂设备。`,
    data: {
      device_identifier: args.device_identifier,
      resolved_device: resolved,
      topology,
      raw: response,
    },
    suggestions: topology.stations.length === 0
      ? ["当前拓扑未返回下挂设备，可继续确认终端是否已接入或查询设备在线状态。"]
      : ["可继续查询下挂设备指标，重点关注 RSSI、协商速率和收发包失败数。"],
  };
}

export async function getStationStats(client, args = {}) {
  const resolved = await resolveDeviceForMac(client, args.device_identifier);
  const response = await client.unary(GET_STATION_STATS, { mac: resolved.mac });
  const allStats = Array.isArray(response.stats) ? response.stats.map(formatStationStat) : [];
  const staMac = String(args.sta_mac || args.station_mac || "").trim();
  const stats = staMac
    ? allStats.filter((item) => sameMac(item.station.mac, staMac))
    : allStats;

  return {
    title: staMac ? "下挂设备指标" : "下挂设备指标列表",
    summary: stats.length === 0
      ? "未查询到下挂设备指标。"
      : `查询到 ${stats.length} 个下挂设备的指标。`,
    data: {
      device_identifier: args.device_identifier,
      resolved_device: resolved,
      sta_mac: staMac,
      stats,
      raw: response,
    },
    suggestions: stats.length === 0
      ? ["确认下挂设备 MAC 是否正确，或先查询网络拓扑获取下挂设备列表。"]
      : ["优先关注 RSSI 低、协商速率低、上下行速率异常或收发包失败数高的终端。"],
  };
}

export async function getNetworkExperience(client, args = {}) {
  const resolved = await resolveDeviceForMac(client, args.device_identifier);
  const response = await client.unary(GET_NETWORK_EXPERIENCE, { mac: resolved.mac });
  const experience = formatExperienceStats(response.experienceStats || response.experience_stats || {});

  return {
    title: "网络体验",
    summary: `网络体验评分: ${experience.network_score}`,
    data: {
      device_identifier: args.device_identifier,
      resolved_device: resolved,
      experience,
      raw: response,
    },
    suggestions: experience.network_score <= 0
      ? ["体验评分为空或为 0 时，建议结合拓扑和下挂设备指标判断是否为采集缺失。"]
      : ["可结合带宽趋势、RSSI 趋势和下挂设备指标定位网慢原因。"],
  };
}

export async function getStationExperience(client, args = {}) {
  const resolved = await resolveDeviceForMac(client, args.device_identifier);
  const staMac = requiredString(args.sta_mac || args.station_mac, "sta_mac");
  const response = await client.unary(GET_STATION_EXPERIENCE, {
    mac: resolved.mac,
    staMac,
  });
  const rssi = Array.isArray(response.rssiSerialize)
    ? response.rssiSerialize.map(formatRssiPoint)
    : Array.isArray(response.rssi_serialize)
      ? response.rssi_serialize.map(formatRssiPoint)
      : [];

  return {
    title: "下挂设备体验",
    summary: `下挂设备 ${response.staMac || response.sta_mac || staMac} 返回 ${rssi.length} 个 RSSI 数据点。`,
    data: {
      device_identifier: args.device_identifier,
      resolved_device: resolved,
      sta_mac: response.staMac || response.sta_mac || staMac,
      rssi,
      raw: response,
    },
    suggestions: rssi.length === 0
      ? ["没有 RSSI 历史数据时，可查询实时下挂设备指标或确认该终端是否在线。"]
      : ["RSSI 长期偏低或波动大时，优先检查终端位置、从网关拓扑和无线覆盖。"],
  };
}

async function resolveDeviceForMac(client, identifier) {
  const resolved = await resolveDevice(client, identifier);
  if (resolved.mac) {
    return resolved;
  }

  const detail = await getDeviceDetail(client, { device_identifier: resolved.id });
  const mac = detail.data?.detail?.mac || "";
  if (!mac) {
    const err = new Error(`设备 ${identifier} 未返回 MAC，无法查询网络统计`);
    err.code = "invalid_argument";
    throw err;
  }
  return {
    ...resolved,
    mac,
  };
}

function formatTopology(topology) {
  return {
    gateways: Array.isArray(topology.gateways) ? topology.gateways.map(formatNode) : [],
    stations: Array.isArray(topology.stations) ? topology.stations.map(formatNode) : [],
    stats: Array.isArray(topology.stats) ? topology.stats.map(formatStationStats) : [],
  };
}

function formatNode(node) {
  return {
    type: node.type || "",
    mac: node.mac || "",
    name: node.name || "",
    ip: node.ip || "",
    interface: node.interface || "",
    ratio: node.ratio || "",
    standard: node.standard || "",
    parent_mac: node.parentMac || node.parent_mac || "",
    online: Boolean(node.online),
    station_type: node.stationType || node.station_type || "",
    first_see_time: node.firstSeeTime || node.first_see_time || null,
    up_link_negotiation_rate: numberField(node.upLinkNegotiationRate ?? node.up_link_negotiation_rate),
    down_link_negotiation_rate: numberField(node.downLinkNegotiationRate ?? node.down_link_negotiation_rate),
    brand: node.brand || "",
  };
}

function formatStationStat(item) {
  return {
    station: formatStation(item.station || {}),
    stats: formatStationStats(item.stats || {}),
  };
}

function formatStation(station) {
  return {
    type: station.type || "",
    mac: station.mac || "",
    name: station.name || "",
    ip: station.ip || "",
    interface: station.interface || "",
    ratio: station.ratio || "",
    standard: station.standard || "",
    parent_mac: station.parentMac || station.parent_mac || "",
    online: Boolean(station.online),
    first_see_time: station.firstSeeTime || station.first_see_time || null,
    up_link_negotiation_rate: numberField(station.upLinkNegotiationRate ?? station.up_link_negotiation_rate),
    down_link_negotiation_rate: numberField(station.downLinkNegotiationRate ?? station.down_link_negotiation_rate),
    brand: station.brand || "",
  };
}

function formatStationStats(stats) {
  return {
    mac: stats.mac || "",
    ping_delay: numberField(stats.pingDelay ?? stats.ping_delay),
    rssi: numberField(stats.rssi),
    up_speed: numberField(stats.upSpeed ?? stats.up_speed),
    down_speed: numberField(stats.downSpeed ?? stats.down_speed),
    up_link_negotiation_rate: numberField(stats.upLinkNegotiationRate ?? stats.up_link_negotiation_rate),
    down_link_negotiation_rate: numberField(stats.downLinkNegotiationRate ?? stats.down_link_negotiation_rate),
    rx_flow: numberField(stats.rxFlow ?? stats.rx_flow),
    tx_flow: numberField(stats.txFlow ?? stats.tx_flow),
    rx_pkt_total: numberField(stats.rxPktTotal ?? stats.rx_pkt_total),
    tx_pkt_total: numberField(stats.txPktTotal ?? stats.tx_pkt_total),
    rx_pkt_retry: numberField(stats.rxPktRetry ?? stats.rx_pkt_retry),
    tx_pkt_retry: numberField(stats.txPktRetry ?? stats.tx_pkt_retry),
    rx_pkt_fail: numberField(stats.rxPktFail ?? stats.rx_pkt_fail),
    tx_pkt_fail: numberField(stats.txPktFail ?? stats.tx_pkt_fail),
    pkt_total: numberField(stats.pktTotal ?? stats.pkt_total),
    pkt_loss: numberField(stats.pktLoss ?? stats.pkt_loss),
    delay_avg: numberField(stats.delayAvg ?? stats.delay_avg),
  };
}

function formatExperienceStats(experience) {
  return {
    network_score: numberField(experience.networkScore ?? experience.network_score),
    experience_serialize: arrayField(experience.experienceSerialize ?? experience.experience_serialize).map((item) => ({
      time_window: item.timeWindow || item.time_window || null,
      num_good: numberField(item.numGood ?? item.num_good),
      num_bad: numberField(item.numBad ?? item.num_bad),
      num_normal: numberField(item.numNormal ?? item.num_normal),
    })),
    bandwidth_serialize: arrayField(experience.bandwidthSerialize ?? experience.bandwidth_serialize).map((item) => ({
      time_window: item.timeWindow || item.time_window || null,
      up: numberField(item.up),
      down: numberField(item.down),
    })),
    rssi_serialize: arrayField(experience.rssiSerialize ?? experience.rssi_serialize).map(formatRssiPoint),
  };
}

function formatRssiPoint(item) {
  return {
    time_window: item.timeWindow || item.time_window || null,
    avg: numberField(item.avg),
    min: numberField(item.min),
    max: numberField(item.max),
  };
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

function sameMac(left, right) {
  return normalizeMac(left) === normalizeMac(right);
}

function normalizeMac(value) {
  return String(value || "").trim().toLowerCase().replace(/[:.\-\s]/g, "");
}

function numberField(value) {
  const number = Number(value || 0);
  return Number.isFinite(number) ? number : 0;
}

function arrayField(value) {
  return Array.isArray(value) ? value : [];
}
