import { listDeviceAlerts } from "./alerts.js";
import { getDeviceDetail, listDevices } from "./devices.js";
import { getNetworkExperience, getNetworkTopology, getStationStats } from "./network.js";

export async function diagnoseDeviceOffline(client, args = {}) {
  const deviceIdentifier = requiredString(args.device_identifier, "device_identifier");
  const detail = await getDeviceDetail(client, { device_identifier: deviceIdentifier });
  const alerts = await listDeviceAlerts(client, { event_type: "ALERT", limit: args.alert_limit || 10 });
  const relatedAlerts = filterAlertsForDevice(alerts.data.alerts, detail.data.detail);

  return {
    title: "设备离线诊断",
    summary: buildOfflineSummary(detail.data.detail, relatedAlerts),
    data: {
      device_identifier: deviceIdentifier,
      device_detail: compactResult(detail),
      recent_alerts: relatedAlerts,
      checked_scope: "operator_managed_devices",
    },
    suggestions: buildOfflineSuggestions(detail.data.detail, relatedAlerts),
    trace: [
      stepTrace("get_device_detail", detail),
      stepTrace("list_device_alerts", alerts),
    ],
  };
}

export async function diagnoseNetworkSlow(client, args = {}) {
  const deviceIdentifier = String(args.device_identifier || "").trim();
  if (!deviceIdentifier) {
    const devices = await listDevices(client, { limit: 10 });
    return {
      title: "网络慢诊断",
      summary: "缺少设备标识，已先列出当前 Operator 可管理设备。",
      data: {
        devices: devices.data.devices,
      },
      suggestions: ["选择一个主网关后，带上 device_identifier 重新发起诊断。"],
      trace: [stepTrace("list_devices", devices)],
    };
  }

  const detail = await getDeviceDetail(client, { device_identifier: deviceIdentifier });
  const topology = await getNetworkTopology(client, { device_identifier: deviceIdentifier });
  const experience = await getNetworkExperience(client, { device_identifier: deviceIdentifier });
  const stationStats = await getStationStats(client, { device_identifier: deviceIdentifier });
  const symptom = String(args.symptom || "").trim();

  return {
    title: "网络慢诊断",
    summary: buildNetworkSlowSummary(detail, topology, experience, stationStats, symptom),
    data: {
      device_identifier: deviceIdentifier,
      symptom,
      device_detail: compactResult(detail),
      topology: topology.data.topology,
      experience: experience.data.experience,
      station_stats: stationStats.data.stats,
    },
    suggestions: buildNetworkSlowSuggestions(experience.data.experience, stationStats.data.stats),
    trace: [
      stepTrace("get_device_detail", detail),
      stepTrace("get_network_topology", topology),
      stepTrace("get_network_experience", experience),
      stepTrace("get_station_stats", stationStats),
    ],
  };
}

export async function explainFttraiCopilotUsage(_client, args = {}) {
  const goal = String(args.user_goal || "").trim();
  const summary = goal
    ? `针对“${goal}”，建议先提供设备 ID、MAC、SN 或区域编码；我会优先查询 Operator 管理范围内的设备、告警、拓扑、统计和体验数据。`
    : "可以直接描述要查询或排查的问题；不知道设备标识时，先列出可管理设备。";

  return {
    title: "FTTR Copilot 使用说明",
    summary,
    data: {
      user_goal: goal,
      identity: "Operator",
      capabilities: [
        "设备：按区域、MAC、SN、在线状态、故障码等条件列出设备，查看详情和在线状态。",
        "告警：查询 Operator 管理范围内的告警列表、详情、数量统计，并可标记已读。",
        "网络：查询拓扑、下挂设备指标、网络体验和终端 RSSI 历史。",
        "统计：查询区域设备汇总、故障统计和设备负载趋势。",
        "实时命令：查询主网关、从网关和 Agent 版本，命令结果可能异步返回 sequence_id。",
        "诊断：组合状态、告警、拓扑和体验数据输出离线或网慢诊断建议。",
      ],
      examples: [
        "列出 440000 区域的离线主网关。",
        "查询 AA:BB:CC:DD:EE:FF 的在线状态。",
        "帮我诊断 AA:BB:CC:DD:EE:FF 为什么离线。",
        "这个网关网速慢，帮我检查拓扑和下挂设备指标。",
        "统计 440000 区域设备告警数量。",
        "查询主网关 Agent 版本。",
      ],
      required_info: [
        "设备 ID、MAC 地址、SN 或区域编码。",
        "问题现象和影响范围，例如全屋慢、某房间弱覆盖、某台手机卡顿。",
        "如果涉及历史问题，补充大致发生时间。",
      ],
    },
    suggestions: ["不知道设备标识时，先调用 list_devices。"],
  };
}

function filterAlertsForDevice(alerts, detail) {
  const candidates = new Set([
    normalize(detail.id),
    normalize(detail.mac),
  ].filter(Boolean));

  return alerts.filter((alert) => {
    const values = [
      alert.device?.id,
      alert.device?.mac,
      alert.event_target?.device_id,
    ].map(normalize);
    return values.some((value) => candidates.has(value));
  });
}

function buildOfflineSummary(detail, alerts) {
  const name = detail.alias || detail.mac || detail.id;
  if (detail.online_status_label === "在线") {
    return `设备 ${name} 当前在线；如用户反馈离线，可能是短时离线已恢复或现场感知问题。`;
  }
  if (detail.online_status_label === "离线") {
    return alerts.length > 0
      ? `设备 ${name} 当前离线，并发现 ${alerts.length} 条相关告警。`
      : `设备 ${name} 当前离线，Operator 告警列表中未匹配到相关告警。`;
  }
  return `设备 ${name} 当前在线状态未知，需结合告警和现场信息继续确认。`;
}

function buildOfflineSuggestions(detail, alerts) {
  if (detail.online_status_label === "在线") {
    return ["核对用户反馈时间与最近告警时间，确认是否为短时离线后恢复。"];
  }
  const suggestions = [
    "优先检查设备供电、光纤链路、上联连接和指示灯状态。",
    "结合 last_offline_reason、fault_codes 和最近告警判断是否为链路中断或设备异常重启。",
  ];
  if (alerts.length === 0) {
    suggestions.push("未匹配到相关告警时，可继续查询主网关实时信息或联系平台侧确认采集是否正常。");
  }
  return suggestions;
}

function buildNetworkSlowSummary(detail, topology, experience, stationStats, symptom) {
  const score = experience.data.experience.network_score;
  const stations = stationStats.data.stats.length;
  const weakStations = stationStats.data.stats.filter((item) => item.stats.rssi && item.stats.rssi < -70).length;
  const symptomText = symptom ? `针对“${symptom}”，` : "";
  return `${symptomText}设备状态 ${detail.data.detail.online_status_label}，网络评分 ${score}，拓扑下挂 ${topology.data.topology.stations.length} 个终端，返回 ${stations} 个终端指标，其中弱信号 ${weakStations} 个。`;
}

function buildNetworkSlowSuggestions(experience, stationStats) {
  const suggestions = [];
  if (experience.network_score > 0 && experience.network_score < 70) {
    suggestions.push("网络体验评分偏低，优先检查带宽趋势、RSSI 趋势和异常终端。");
  }
  const weakStations = stationStats.filter((item) => item.stats.rssi && item.stats.rssi < -70);
  if (weakStations.length > 0) {
    suggestions.push("存在 RSSI 低于 -70 的终端，优先检查终端位置、漫游和从网关覆盖。");
  }
  const failedPackets = stationStats.filter((item) => item.stats.rx_pkt_fail > 0 || item.stats.tx_pkt_fail > 0);
  if (failedPackets.length > 0) {
    suggestions.push("存在收发包失败的终端，建议结合协商速率、RSSI 和连接频段排查无线质量。");
  }
  if (suggestions.length === 0) {
    suggestions.push("当前指标未显示明显弱信号或丢包，可继续结合用户发生时间查询体验趋势。");
  }
  return suggestions;
}

function compactResult(result) {
  return {
    title: result.title,
    summary: result.summary,
    data: result.data,
  };
}

function stepTrace(tool, result) {
  return {
    tool,
    title: result.title,
    summary: result.summary,
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

function normalize(value) {
  return String(value || "").trim().toLowerCase().replace(/[:.\-\s]/g, "");
}
