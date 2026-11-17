// COC 7e 掷骰 + 成功等级判定
// 纯函数模块，零依赖；RNG 默认走 node:crypto，可选 --seed 切换到确定性 PRNG

import crypto from "node:crypto";

// ---------- RNG ----------

/**
 * Mulberry32 — 简单快速的种子化 PRNG，返回 [0, 1) 浮点。
 * 同一种子产生同一序列，便于 PbP / 争议裁决时复现掷骰。
 */
function mulberry32(seed) {
  let a = seed >>> 0;
  return function () {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/**
 * 创建一个返回 [min, max] 闭区间整数的 RNG 函数。
 * 传 seed 切到 mulberry32；不传则用 crypto.randomInt（加密级随机）。
 */
export function makeRng(seed) {
  if (seed !== undefined && seed !== null && !Number.isNaN(Number(seed))) {
    const prng = mulberry32(Number(seed));
    return (min, max) => {
      const range = max - min + 1;
      return min + Math.floor(prng() * range);
    };
  }
  return (min, max) => crypto.randomInt(min, max + 1);
}

// ---------- 通用掷骰 ----------

/**
 * 解析掷骰表达式：3d6*5 / 2d6+3 / 1d100 / 1d20-2 / 8d6 / d20
 * 不支持混合运算（如 2d6+1d4），COC 7e 建卡用不到。
 */
export function parseDiceSpec(spec) {
  const m = /^(\d*)d(\d+)(?:([*])(\d+))?(?:([+-])(\d+))?$/.exec(
    spec.toLowerCase().trim(),
  );
  if (!m) throw new Error(`Invalid dice spec: ${spec}`);
  const count = m[1] ? parseInt(m[1], 10) : 1;
  const sides = parseInt(m[2], 10);
  if (count < 1 || sides < 1) throw new Error(`Invalid dice spec: ${spec}`);
  const multiplier = m[3] === "*" && m[4] ? parseInt(m[4], 10) : 1;
  const modifier =
    m[5] && m[6] ? parseInt(m[6], 10) * (m[5] === "-" ? -1 : 1) : 0;
  return { count, sides, multiplier, modifier, spec };
}

/**
 * 通用掷骰：投 count 个 sides 面骰，求和后乘以 multiplier 再加 modifier。
 */
export function rollDice(spec, rng = makeRng()) {
  const parsed = parseDiceSpec(spec);
  const rolls = [];
  for (let i = 0; i < parsed.count; i++) {
    rolls.push(rng(1, parsed.sides));
  }
  const sum = rolls.reduce((a, b) => a + b, 0);
  const total = sum * parsed.multiplier + parsed.modifier;
  return {
    spec: parsed.spec,
    count: parsed.count,
    sides: parsed.sides,
    rolls,
    sum,
    multiplier: parsed.multiplier,
    modifier: parsed.modifier,
    total,
  };
}

// ---------- COC 7e 成功等级 ----------

// 注意优先级：大成功 > 极难 > 困难 > 普通 > 失败 > 大失败
export const SUCCESS_LEVEL = {
  FUMBLE: "fumble",
  FAILURE: "failure",
  REGULAR: "regular",
  HARD: "hard",
  EXTREME: "extreme",
  CRITICAL: "critical",
};

export const SUCCESS_LEVEL_LABEL = {
  critical: "大成功 / Critical",
  extreme: "极难成功 / Extreme",
  hard: "困难成功 / Hard",
  regular: "普通成功 / Regular",
  failure: "失败 / Failure",
  fumble: "大失败 / Fumble",
};

// 成功等级数值排序（用于对抗检定比较）
export const SUCCESS_LEVEL_RANK = {
  fumble: 0,
  failure: 1,
  regular: 2,
  hard: 3,
  extreme: 4,
  critical: 5,
};

/**
 * 判定 COC 7e d100 检定的成功等级。
 *
 * 规则书（守秘人规则书）：
 *   - 骰出 01 → 大成功（不仅成功还有额外好运）
 *   - 骰出 ≤ 目标 × 1/5 → 极难成功
 *   - 骰出 ≤ 目标 × 1/2 → 困难成功
 *   - 骰出 ≤ 目标     → 普通成功
 *   - 骰出 > 目标     → 失败
 *   - 目标 < 50：骰出 96-100 均为大失败
 *   - 目标 ≥ 50：骰出 100 为大失败
 *
 * 可选规则（opts）：
 *   - criticalRange: [lo, hi]  大成功骰值范围（默认 [1,1]）
 *   - fumbleRange:   [lo, hi] | null  大失败骰值范围；
 *                   null → 自动（目标<50 → [96,100]；目标≥50 → [100,100]）
 *
 * 注意：大成功/大失败范围优先于普通成功/失败判定
 *       （即落在 criticalRange 内即使 > 目标也算大成功；
 *         落在 fumbleRange 内即使 ≤ 目标也算大失败）
 */
export function successLevel(roll, target, opts = {}) {
  if (target === undefined || target === null) return null;

  const criticalRange = opts.criticalRange || [1, 1];
  if (roll >= criticalRange[0] && roll <= criticalRange[1]) {
    return SUCCESS_LEVEL.CRITICAL;
  }

  // 大失败范围：显式 > 自动
  let fRange = opts.fumbleRange;
  if (!fRange) fRange = target < 50 ? [96, 100] : [100, 100];
  if (roll >= fRange[0] && roll <= fRange[1]) return SUCCESS_LEVEL.FUMBLE;

  const hard = Math.floor(target / 2);
  const extreme = Math.floor(target / 5);
  if (roll <= extreme) return SUCCESS_LEVEL.EXTREME;
  if (roll <= hard) return SUCCESS_LEVEL.HARD;
  if (roll <= target) return SUCCESS_LEVEL.REGULAR;
  return SUCCESS_LEVEL.FAILURE;
}

/**
 * 大失败阈值（用于显示）。
 * 若提供 opts.fumbleRange，则返回其下限；否则按目标值自动判定。
 */
export function fumbleThreshold(target, opts = {}) {
  if (opts.fumbleRange) return opts.fumbleRange[0];
  return target < 50 ? 96 : 100;
}

// ---------- 百分位掷骰（含奖励/惩罚骰） ----------

/**
 * 投 d100，可选多个奖励骰或惩罚骰（最多各 2 个）。
 *
 * COC 7e 规则：
 *   - 投一个个位骰 + (1 + |bonus-penalty|) 个十位骰
 *   - 奖励骰：取最小的十位值
 *   - 惩罚骰：取最大的十位值
 *   - 一个奖励骰与一个惩罚骰互相抵消
 *   - 个位骰共用
 *   - 00 + 0 = 100
 *
 * @param {object} opts
 * @param {number} [opts.target]    目标值
 * @param {number} [opts.bonus=0]   奖励骰数量
 * @param {number} [opts.penalty=0] 惩罚骰数量
 * @param {object} [opts.rng]
 * @param {number[]} [opts.criticalRange]  大成功骰值范围（默认 [1,1]）
 * @param {number[]|null} [opts.fumbleRange] 大失败骰值范围（默认 null → 自动）
 */
export function rollPercentile({
  target,
  bonus = 0,
  penalty = 0,
  rng = makeRng(),
  criticalRange,
  fumbleRange,
}) {
  if (bonus > 0 && penalty > 0) {
    // 先抵消
    const min = Math.min(bonus, penalty);
    bonus -= min;
    penalty -= min;
  }
  if (bonus > 2 || penalty > 2) {
    throw new Error("奖励骰/惩罚骰最多各 2 个");
  }

  const extraDice = Math.max(bonus, penalty);
  const tensDice = [];
  for (let i = 0; i < 1 + extraDice; i++) {
    tensDice.push(rng(0, 9) * 10);
  }

  let usedTensIndex = 0;
  if (bonus > 0) {
    // 取最小
    usedTensIndex = tensDice.indexOf(Math.min(...tensDice));
  } else if (penalty > 0) {
    // 取最大
    usedTensIndex = tensDice.indexOf(Math.max(...tensDice));
  }

  const ones = rng(0, 9);
  let total = tensDice[usedTensIndex] + ones;
  if (total === 0) total = 100; // 00 + 0 → 100

  const result = {
    tensDice,
    ones,
    total,
    usedTensIndex,
    bonus,
    penalty,
  };

  if (target !== undefined && target !== null) {
    const slOpts = {};
    if (criticalRange) slOpts.criticalRange = criticalRange;
    if (fumbleRange !== undefined) slOpts.fumbleRange = fumbleRange;
    result.target = target;
    result.hardTarget = Math.floor(target / 2);
    result.extremeTarget = Math.floor(target / 5);
    result.fumbleThreshold = fumbleThreshold(target, slOpts);
    result.level = successLevel(total, target, slOpts);
    result.levelLabel = SUCCESS_LEVEL_LABEL[result.level];
  }

  return result;
}

// ---------- 对抗检定 ----------

/**
 * 对抗检定（Opposed Roll）。
 *
 * COC 7e 规则：
 *   - 双方各掷 d100 vs 自己的目标值
 *   - 比较成功等级，高者胜
 *   - 平手时，目标值更高者胜
 *   - 仍平手则僵局（draw）
 *   - 对抗检定不能孤注一掷
 *
 * @param {object} a  { target, bonus?, penalty?, label? }
 * @param {object} b  { target, bonus?, penalty?, label? }
 * @param {object} [rng]
 */
export function opposedRoll(a, b, rng = makeRng()) {
  const rollA = rollPercentile({ ...a, rng });
  const rollB = rollPercentile({ ...b, rng });

  const rankA = SUCCESS_LEVEL_RANK[rollA.level];
  const rankB = SUCCESS_LEVEL_RANK[rollB.level];

  let winner = null;
  let reason = "";
  if (rankA > rankB) {
    winner = "a";
    reason = `${a.label || "A"} 成功等级更高`;
  } else if (rankB > rankA) {
    winner = "b";
    reason = `${b.label || "B"} 成功等级更高`;
  } else {
    // 平手：目标值高者胜
    if (a.target > b.target) {
      winner = "a";
      reason = `平手，${a.label || "A"} 目标值更高（${a.target} > ${b.target}）`;
    } else if (b.target > a.target) {
      winner = "b";
      reason = `平手，${b.label || "B"} 目标值更高（${b.target} > ${a.target}）`;
    } else {
      winner = "draw";
      reason = "完全平手，僵局";
    }
  }

  return { rollA, rollB, winner, reason };
}
