import type { GeResult, WugeRelation, WugeRelationDirection, Wuxing } from "./types.ts";

const SHULI_WUXING_MAP: Record<number, Wuxing> = {
  0: "水",
  1: "木",
  2: "木",
  3: "火",
  4: "火",
  5: "土",
  6: "土",
  7: "金",
  8: "金",
  9: "水",
};

const WUXING_SHENG: Record<Wuxing, Wuxing> = {
  金: "水",
  水: "木",
  木: "火",
  火: "土",
  土: "金",
};

const WUXING_KE: Record<Wuxing, Wuxing> = {
  金: "木",
  木: "土",
  土: "水",
  水: "火",
  火: "金",
};

export const LUCK_BY_NUMBER: Record<number, string> = {
  1: "吉",
  2: "凶",
  3: "吉",
  4: "凶",
  5: "吉",
  6: "吉",
  7: "吉",
  8: "吉",
  9: "凶",
  10: "凶",
  11: "吉",
  12: "凶",
  13: "吉",
  14: "凶",
  15: "吉",
  16: "吉",
  17: "吉",
  18: "吉",
  19: "凶",
  20: "凶",
  21: "吉",
  22: "凶",
  23: "吉",
  24: "吉",
  25: "吉",
  26: "凶带吉",
  27: "吉带凶",
  28: "凶",
  29: "吉",
  30: "吉带凶",
  31: "吉",
  32: "吉",
  33: "吉",
  34: "凶",
  35: "吉",
  36: "凶",
  37: "吉",
  38: "半吉",
  39: "吉",
  40: "凶",
  41: "吉",
  42: "吉带凶",
  43: "吉带凶",
  44: "凶",
  45: "吉",
  46: "凶",
  47: "吉",
  48: "吉",
  49: "凶",
  50: "凶",
  51: "吉带凶",
  52: "吉",
  53: "吉带凶",
  54: "凶",
  55: "吉带凶",
  56: "凶",
  57: "吉",
  58: "吉带凶",
  59: "凶",
  60: "凶",
  61: "吉",
  62: "凶",
  63: "吉",
  64: "凶",
  65: "吉",
  66: "凶",
  67: "吉",
  68: "吉",
  69: "凶",
  70: "凶",
  71: "吉带凶",
  72: "凶",
  73: "吉",
  74: "凶",
  75: "吉带凶",
  76: "凶",
  77: "吉凶各半",
  78: "吉帶凶",
  79: "凶",
  80: "凶",
  81: "吉",
};

export function getShuliWuxing(geNumber: number): Wuxing {
  return SHULI_WUXING_MAP[geNumber % 10];
}

export function getLuck(strokeCount: number): string {
  let index = strokeCount % 81;
  if (index === 0) {
    index = 81;
  }
  return LUCK_BY_NUMBER[index] ?? "未知";
}

export function getTiange(xingStrokeCounts: number[]): number {
  const total = xingStrokeCounts.reduce((sum, item) => sum + item, 0);
  return xingStrokeCounts.length === 1 ? total + 1 : total;
}

export function getRenge(xingStrokeCounts: number[], mingStrokeCounts: number[]): number {
  return xingStrokeCounts[xingStrokeCounts.length - 1] + mingStrokeCounts[0];
}

export function getDige(mingStrokeCounts: number[]): number {
  const total = mingStrokeCounts.reduce((sum, item) => sum + item, 0);
  return mingStrokeCounts.length === 1 ? total + 1 : total;
}

export function getZongge(xingStrokeCounts: number[], mingStrokeCounts: number[]): number {
  return [...xingStrokeCounts, ...mingStrokeCounts].reduce((sum, item) => sum + item, 0);
}

export function getWaige(xingStrokeCounts: number[], mingStrokeCounts: number[]): number {
  const tiange = getTiange(xingStrokeCounts);
  const renge = getRenge(xingStrokeCounts, mingStrokeCounts);
  const dige = getDige(mingStrokeCounts);
  return tiange + dige - renge;
}

export function buildGeObject(geCount: number): GeResult {
  return {
    number: geCount,
    luck: getLuck(geCount),
    wuxing: getShuliWuxing(geCount),
  };
}

export function getRelation(from: Wuxing, to: Wuxing): WugeRelation {
  if (from === to) {
    return "同";
  }
  if (WUXING_SHENG[from] === to) {
    return "生";
  }
  if (WUXING_KE[from] === to) {
    return "克";
  }
  if (WUXING_SHENG[to] === from) {
    return "泄";
  }
  return "耗";
}

export function getRelationDirection(from: Wuxing, to: Wuxing): WugeRelationDirection {
  if (from === to) {
    return "同";
  }
  if (WUXING_SHENG[from] === to) {
    return "我生";
  }
  if (WUXING_SHENG[to] === from) {
    return "生我";
  }
  if (WUXING_KE[from] === to) {
    return "我克";
  }
  return "克我";
}
