import { addDaysToLocalDateTime, formatDurationMinutes, getLocalDurationMinutes } from "./utils.mjs";

const TRAIN_SCENE_ALIASES = new Set(["train", "rail", "railway", "station", "train_station"]);
const AIRPORT_SCENE_ALIASES = new Set(["airport", "flight"]);
const CITY_SCENE_ALIASES = new Set(["city", "downtown", "urban"]);

export function inferTransitSceneFromLocation(location) {
  const text = String(location || "").trim();
  if (!text) {
    return null;
  }

  if (/(高铁站|火车站|站内取还)/u.test(text)) {
    return "train_station";
  }

  if (/(机场|航站楼|T1|T2|T3)/u.test(text)) {
    return "airport";
  }

  return null;
}

export function normalizeTransitScene(value, locationHint = null) {
  const raw = String(value || "").trim().toLowerCase().replace(/[\s-]+/g, "_");
  if (!raw) {
    return inferTransitSceneFromLocation(locationHint);
  }

  if (TRAIN_SCENE_ALIASES.has(raw)) {
    return "train_station";
  }

  if (AIRPORT_SCENE_ALIASES.has(raw)) {
    return "airport";
  }

  if (CITY_SCENE_ALIASES.has(raw)) {
    return "city";
  }

  return inferTransitSceneFromLocation(locationHint);
}

export function parseOneHaiInventoryCount(text) {
  const match = String(text || "").match(/共有\s*(\d+)\s*种车型可以租用/u);
  if (!match) {
    return null;
  }

  return Number(match[1]);
}

export function parseOneHaiPeakRentalRule(text) {
  const source = String(text || "");
  const minimumDaysMatch = source.match(/租期延长至\s*(\d+)\s*天以上/u);
  if (!minimumDaysMatch) {
    return null;
  }

  const peakPeriodMatch = source.match(/(\d{4}年\d{2}月\d{2}日)\s*-\s*(\d{4}年\d{2}月\d{2}日)\s*为用车高峰期/u);
  return {
    minimumDays: Number(minimumDaysMatch[1]),
    peakStartDate: peakPeriodMatch?.[1] || null,
    peakEndDate: peakPeriodMatch?.[2] || null
  };
}

export function buildOneHaiPeakRentalHint(query, text) {
  const rule = parseOneHaiPeakRentalRule(text);
  if (!rule) {
    return null;
  }

  const currentDurationMinutes = getLocalDurationMinutes(query.pickupAt, query.dropoffAt);
  const minimumDurationMinutes = rule.minimumDays * 24 * 60;
  const periodPrefix = rule.peakStartDate && rule.peakEndDate
    ? `${rule.peakStartDate}-${rule.peakEndDate} 为用车高峰期，`
    : "当前是用车高峰期，";

  if (currentDurationMinutes < minimumDurationMinutes) {
    const suggestedDropoffAt = addDaysToLocalDateTime(query.pickupAt, rule.minimumDays);
    return {
      rule,
      suggestedDropoffAt,
      warning: `${periodPrefix}至少需租满 ${rule.minimumDays} 天；当前仅 ${formatDurationMinutes(currentDurationMinutes)}，建议还车时间不早于 ${suggestedDropoffAt}。`
    };
  }

  return {
    rule,
    suggestedDropoffAt: null,
    warning: `${periodPrefix}平台提示建议租满 ${rule.minimumDays} 天以上。`
  };
}
