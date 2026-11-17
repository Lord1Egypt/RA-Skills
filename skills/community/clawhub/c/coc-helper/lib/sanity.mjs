// COC 7e 理智（SAN）系统
// 实现 SAN 检定、损失结算、发疯判定、恢复
// 规则来源：克苏鲁的呼唤 第七版 守秘人规则书 第八章

import { rollPercentile, rollDice, makeRng } from "./dice.mjs";

// 单次 SAN 损失 ≥ 5 → 触发临时性疯狂
export const TEMP_INSANITY_THRESHOLD = 5;

/**
 * 解析 SAN 损失表达式（`SAN X/Y` 格式）。
 *   - "1/1d4+1"  → successLoss="1", failLoss="1d4+1"
 *   - "0/1d4"    → successLoss="0", failLoss="1d4"
 *   - "1d10/1d100" → successLoss="1d10", failLoss="1d100"
 *
 * @param {string} expr  形如 "X/Y" 的损失表达式
 */
export function parseSanLoss(expr) {
  const parts = String(expr).split("/");
  if (parts.length !== 2)
    throw new Error(`Invalid SAN loss spec: ${expr} (expect X/Y)`);
  return { successLoss: parts[0].trim(), failLoss: parts[1].trim() };
}

/**
 * 计算掷骰表达式的最大可能值（用于大失败时取最大损失）。
 *   - "1d4"    → 4
 *   - "1d4+1"  → 5
 *   - "2d6+1"  → 13
 *   - "1d100"  → 100
 *   - "0"      → 0
 */
export function maxDiceValue(spec) {
  const m = /^(\d*)d(\d+)(?:([*])(\d+))?(?:([+-])(\d+))?$/.exec(
    String(spec).toLowerCase().trim(),
  );
  if (!m) {
    // 纯数字
    const n = Number(spec);
    if (Number.isFinite(n)) return Math.max(0, n);
    return 0;
  }
  const count = m[1] ? parseInt(m[1], 10) : 1;
  const sides = parseInt(m[2], 10);
  const multiplier = m[3] === "*" && m[4] ? parseInt(m[4], 10) : 1;
  const modifier =
    m[5] && m[6] ? parseInt(m[6], 10) * (m[5] === "-" ? -1 : 1) : 0;
  return count * sides * multiplier + modifier;
}

/**
 * 执行一次 SAN 检定。
 *
 * 规则书（第八章）：
 *   - 投 d100 vs currentSan
 *   - 成功（≤ currentSan）：损失 `successLoss` 指定的 SAN（通常为 0 或 1）
 *   - 失败（> currentSan）：损失 `failLoss` 指定的全量 SAN
 *   - 大失败：损失 `failLoss` 的**最大可能值**（"失去这次遭遇中能损失的最多理智值"）
 *   - 大成功（01）：无 SAN 损失（KP 裁定，常用房规）
 *
 * 疯狂触发：
 *   - 单次损失 ≥ 5 → 调查员进行 INT 检定；INT 失败则抑制记忆（不进入疯狂）；
 *     INT 成功则认识到所经历的意义，进入临时性疯狂，持续 1D10 小时
 *   - 疯狂发作（即时症状）持续 1D10 战斗轮（仅当有其他调查员在场）
 *   - 一天内累计损失 ≥ 1/5 当前 SAN → 不定性疯狂
 *
 * @param {object} opts
 * @param {number} opts.currentSan       当前 SAN 值
 * @param {string} opts.loss             SAN 损失表达式 "X/Y"，如 "1/1d4+1"
 *                                       （向后兼容：若传 lossDice 也支持，但推荐用 loss）
 * @param {string} [opts.lossDice]       失败时的损失骰（旧接口，等价于 loss="0/X"）
 * @param {number} [opts.successLoss]    成功时损失点数（旧接口；默认按 loss 解析）
 * @param {number} [opts.intScore]       调查员 INT 值，用于临时疯狂的 INT 检定；
 *                                       未提供则不进行 INT 检定（直接进入疯狂）
 * @param {object} [opts.rng]
 * @param {boolean} [opts.alwaysLossOnFail] 已弃用，保留兼容
 */
export function sanCheck({
  currentSan,
  loss,
  lossDice,
  successLoss: successLossOverride,
  intScore,
  rng = makeRng(),
  // 可选规则配置（来自 rules-config）
  tempInsanityThreshold = TEMP_INSANITY_THRESHOLD,
  indefiniteInsanitySingleLoss = 20,
  criticalRange,
  fumbleRange,
}) {
  // 解析损失表达式
  let successLossExpr = "0";
  let failLossExpr = "0";
  if (loss) {
    const parsed = parseSanLoss(loss);
    successLossExpr = parsed.successLoss;
    failLossExpr = parsed.failLoss;
  } else if (lossDice) {
    // 旧接口：成功 1 点，失败按 lossDice
    successLossExpr = "1";
    failLossExpr = lossDice;
  }

  // SAN 检定
  const check = rollPercentile({
    target: currentSan,
    rng,
    criticalRange,
    fumbleRange,
  });

  // 准备损失掷骰（支持纯数字固定值如 "1" 或 "0"，以及骰子表达式如 "1d4+1"）
  const lossRoll = (expr) => {
    const trimmed = String(expr).trim();
    if (/^-?\d+$/.test(trimmed)) {
      return { spec: trimmed, total: parseInt(trimmed, 10), fixed: true };
    }
    return rollDice(trimmed, rng);
  };
  let successLossRoll = null;
  let failLossRoll = null;
  if (successLossExpr !== "0") successLossRoll = lossRoll(successLossExpr);
  if (failLossExpr !== "0") failLossRoll = lossRoll(failLossExpr);

  let sanLoss = 0;
  let sanityBout = false; // 是否进入临时性疯狂
  let boutDuration = null; // 临时性疯狂持续时长（小时）
  let boutOnset = null; // 疯狂发作即时症状持续（轮）
  let intCheck = null; // INT 检定结果（触发时）
  let note = "";

  if (check.level === "fumble") {
    // 大失败：损失 failLoss 的最大可能值
    sanLoss = maxDiceValue(failLossExpr);
    note = `大失败：失去此次遭遇的最大可能损失 ${sanLoss} 点`;
  } else if (check.level === "failure") {
    sanLoss = failLossRoll ? failLossRoll.total : 0;
    note = `失败：损失 ${sanLoss} 点`;
  } else if (check.level === "critical") {
    sanLoss = 0;
    note = "大成功（01）：无损失";
  } else if (check.level === "extreme" || check.level === "hard") {
    sanLoss = successLossRoll ? successLossRoll.total : 0;
    note = `${check.level === "extreme" ? "极难" : "困难"}成功：损失 ${sanLoss} 点`;
  } else {
    // regular
    sanLoss = successLossRoll ? successLossRoll.total : 0;
    note = `普通成功：损失 ${sanLoss} 点`;
  }

  // 临时性疯狂判定：单次损失 ≥ 阈值（默认 5）
  if (sanLoss >= tempInsanityThreshold) {
    // 先进行 INT 检定（如提供了 INT）
    if (intScore !== undefined && intScore !== null) {
      intCheck = rollPercentile({
        target: intScore,
        rng,
        criticalRange,
        fumbleRange,
      });
      if (intCheck.level === "failure" || intCheck.level === "fumble") {
        // INT 失败：抑制记忆，不进入疯狂
        sanityBout = false;
        note += `；单次损失 ≥ ${tempInsanityThreshold}，但 INT 检定失败 → 抑制记忆，不进入疯狂`;
      } else {
        sanityBout = true;
        const dur = rollDice("1d10", rng);
        boutDuration = dur.total;
        // 疯狂发作（即时症状）持续 1D10 战斗轮
        const onset = rollDice("1d10", rng);
        boutOnset = onset.total;
        note += `；INT 检定成功 → 进入临时性疯狂，持续 ${boutDuration} 小时；疯狂发作 ${boutOnset} 战斗轮`;
      }
    } else {
      // 未提供 INT：直接进入临时性疯狂
      sanityBout = true;
      const dur = rollDice("1d10", rng);
      boutDuration = dur.total;
      const onset = rollDice("1d10", rng);
      boutOnset = onset.total;
      note += `；单次损失 ≥ ${tempInsanityThreshold} → 进入临时性疯狂，持续 ${boutDuration} 小时；疯狂发作 ${boutOnset} 战斗轮`;
    }
  }

  const newSan = Math.max(0, currentSan - sanLoss);
  const insanityThreshold = Math.floor(currentSan / 5);

  // 不定性疯狂判定（COC 7e 规则书）：
  //   - 单次损失 ≥ indefiniteInsanitySingleLoss（默认 20）→ 直接触发不定性疯狂（终极的宇宙恶意）
  //   - 一天内累计损失 ≥ 1/5 当前 SAN → 触发不定性疯狂（需调用方累计）
  // 单次跌破阈值不是规则规定的触发条件。
  const wentInsane = sanLoss >= indefiniteInsanitySingleLoss;
  if (wentInsane) {
    note += `；单次损失 ≥ ${indefiniteInsanitySingleLoss} → 直接触发不定性疯狂（终极的宇宙恶意）`;
  }

  return {
    currentSan,
    newSan,
    sanLoss,
    successLossRoll,
    failLossRoll,
    check,
    intCheck,
    sanityBout,
    boutDuration,
    boutOnset,
    note,
    insanityThreshold,
    // 单次 ≥ 20 点损失 → 不定性疯狂；
    // 一天内累计 ≥ 1/5 当前 SAN 的判定由调用方根据 sanLoss 累计决定。
    wentInsane,
    permanentInsanity: newSan === 0,
  };
}

/**
 * 团末恢复 SAN（投 d10，不能超过上限）。
 */
export function sanGain({ currentSan, maxSan, rng = makeRng() }) {
  const gain = rollDice("1d10", rng);
  const recovered = Math.min(gain.total, maxSan - currentSan);
  return {
    currentSan,
    newSan: currentSan + recovered,
    gained: recovered,
    gainRoll: gain,
    maxSan,
    capped: recovered < gain.total,
  };
}

/**
 * 私人/家庭护理治疗（每月一次）。
 * 投 d100：01–95（或低于精神分析技能）→ 恢复 1d3 SAN + 理智检定通过则脱离疯狂
 *         96–00 → 损失 1d6 SAN
 */
export function privateCare({
  currentSan,
  maxSan,
  psychoanalysis = 0,
  rng = makeRng(),
}) {
  const roll = rollPercentile({ rng });
  const successTarget = Math.max(psychoanalysis, 95);
  let result;
  if (roll.total <= successTarget) {
    const gain = rollDice("1d3", rng);
    const recovered = Math.min(gain.total, maxSan - currentSan);
    result = {
      outcome: "success",
      currentSan,
      newSan: currentSan + recovered,
      sanDelta: recovered,
      detail: `恢复 ${recovered} SAN`,
      roll,
      gainRoll: gain,
      exitsInsanity: true,
    };
  } else {
    const loss = rollDice("1d6", rng);
    const lost = Math.min(loss.total, currentSan);
    result = {
      outcome: "failure",
      currentSan,
      newSan: currentSan - lost,
      sanDelta: -lost,
      detail: `损失 ${lost} SAN`,
      roll,
      gainRoll: loss,
      exitsInsanity: false,
    };
  }
  return result;
}

/**
 * 收容机构治疗（每月一次）。
 * 投 d100：01–50 → 恢复 3 SAN + 理智检定通过则脱离
 *         51–95 → 无效
 *         96–00 → 损失 1d6 SAN
 */
export function institutionalCare({ currentSan, maxSan, rng = makeRng() }) {
  const roll = rollPercentile({ rng });
  let result;
  if (roll.total <= 50) {
    const recovered = Math.min(3, maxSan - currentSan);
    result = {
      outcome: "success",
      currentSan,
      newSan: currentSan + recovered,
      sanDelta: recovered,
      detail: `恢复 ${recovered} SAN`,
      roll,
      exitsInsanity: true,
    };
  } else if (roll.total <= 95) {
    result = {
      outcome: "no_effect",
      currentSan,
      newSan: currentSan,
      sanDelta: 0,
      detail: "无效",
      roll,
      exitsInsanity: false,
    };
  } else {
    const loss = rollDice("1d6", rng);
    const lost = Math.min(loss.total, currentSan);
    result = {
      outcome: "failure",
      currentSan,
      newSan: currentSan - lost,
      sanDelta: -lost,
      detail: `损失 ${lost} SAN`,
      roll,
      gainRoll: loss,
      exitsInsanity: false,
    };
  }
  return result;
}

/**
 * 显示当前 SAN 阈值信息。
 */
export function sanThreshold(currentSan, maxSan) {
  const insanityThreshold = Math.floor(currentSan / 5);
  return {
    currentSan,
    maxSan,
    insanityThreshold,
    notes:
      `当前 SAN ${currentSan}，临时发疯阈值（SAN/5）= ${insanityThreshold}。\n` +
      `若 SAN 跌破此阈值，进入不定性疯狂。\n` +
      `单次损失 ≥ 5 → 触发临时性疯狂（持续 1D10 小时）。\n` +
      `SAN 上限（99 - 克苏鲁神话）= ${maxSan}。`,
  };
}
