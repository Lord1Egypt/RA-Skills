// COC 7e 规则配置（可变规则 / 可选阈值）
// 持久化到 session.json 的 rules 字段，跨命令保持
// 设计：默认值对齐规则书基础规则；KP 可通过 `config` 命令切换变体或单项设置

import fs from "node:fs";
import path from "node:path";

const SESSION_FILE = path.join(import.meta.dirname, "..", "session.json");

/**
 * 默认规则配置（规则书基础规则）。
 *
 * - 大成功/大失败范围：COC 7e 守秘人规则书基础为 1 / 100
 *   规则书另提供可选规则：1-5 / 96-100（更戏剧化）
 *   两者通常成组使用：strict = 1/100，lenient = 1-5/96-100
 *
 * - SAN 系统阈值：
 *   - tempInsanityThreshold：单次损失触发临时性疯狂（规则书 5）
 *   - indefiniteInsanitySingleLoss：单次损失触发不定性疯狂（规则书 20+）
 *   - indefiniteInsanityDailyFraction：一天累计损失触发不定性疯狂（规则书 1/5 = 0.2）
 */
export const DEFAULT_RULES = {
  // 大成功骰值范围（含两端）
  criticalRange: [1, 1],
  // 大失败骰值范围（含两端）；若为 null 则按目标值自动判定（<50 → 96-100；≥50 → 100）
  fumbleRange: null,

  // 单次 SAN 损失 ≥ 此值 → 触发临时性疯狂（需 INT 检定）
  tempInsanityThreshold: 5,
  // 单次 SAN 损失 ≥ 此值 → 直接触发不定性疯狂
  indefiniteInsanitySingleLoss: 20,
  // 一天内累计 SAN 损失 ≥ 当前 SAN × 此分数 → 触发不定性疯狂
  indefiniteInsanityDailyFraction: 0.2,
};

/**
 * 预设规则变体。
 *
 * - strict：规则书基础（1/100，标准阈值）
 * - lenient：戏剧化变体（1-5/96-100，更易大成功/大失败）
 *
 * 注意：变体只覆盖部分字段，未覆盖字段保留默认值或用户已设值。
 */
export const RULE_VARIANTS = {
  strict: {
    label: "严格（规则书基础：1/100）",
    patch: { criticalRange: [1, 1], fumbleRange: null },
  },
  lenient: {
    label: "宽松（戏剧化：1-5/96-100）",
    patch: { criticalRange: [1, 5], fumbleRange: [96, 100] },
  },
};

/**
 * 读取 session.json（仅返回 rules 字段，缺失则返回空对象）。
 */
function readSessionRules() {
  if (!fs.existsSync(SESSION_FILE)) return {};
  try {
    const data = JSON.parse(fs.readFileSync(SESSION_FILE, "utf8"));
    return (data && data.rules) || {};
  } catch {
    return {};
  }
}

/**
 * 写入 rules 字段到 session.json（保留其他字段）。
 */
function writeSessionRules(rules) {
  let data = {};
  if (fs.existsSync(SESSION_FILE)) {
    try {
      data = JSON.parse(fs.readFileSync(SESSION_FILE, "utf8")) || {};
    } catch {
      data = {};
    }
  }
  data.rules = rules;
  const tmp = SESSION_FILE + ".tmp";
  fs.writeFileSync(tmp, JSON.stringify(data, null, 2));
  fs.renameSync(tmp, SESSION_FILE);
}

/**
 * 加载当前规则配置（默认值 + session 覆盖）。
 * @returns {object} 合并后的完整规则配置
 */
export function loadRules() {
  const saved = readSessionRules();
  return mergeRules(DEFAULT_RULES, saved);
}

/**
 * 保存规则配置（合并到 session）。
 */
export function saveRules(patch) {
  const current = loadRules();
  const next = mergeRules(current, patch);
  writeSessionRules(next);
  return next;
}

/**
 * 重置为默认规则配置。
 */
export function resetRules() {
  writeSessionRules({});
  return { ...DEFAULT_RULES };
}

/**
 * 应用预设变体。
 */
export function applyVariant(variantName) {
  const variant = RULE_VARIANTS[variantName];
  if (!variant) {
    throw new Error(
      `未知规则变体: ${variantName}（可选：${Object.keys(RULE_VARIANTS).join(", ")}）`,
    );
  }
  return saveRules(variant.patch);
}

/**
 * 合并规则（深层合并数组与标量；null 表示"自动"）。
 */
function mergeRules(base, patch) {
  const result = { ...base };
  for (const [k, v] of Object.entries(patch || {})) {
    if (Array.isArray(v)) {
      result[k] = [...v];
    } else {
      result[k] = v;
    }
  }
  return result;
}

/**
 * 解析范围字符串为 [min, max]。
 *   "1" → [1, 1]
 *   "1-5" → [1, 5]
 *   "96-100" → [96, 100]
 *   "100" → [100, 100]
 */
export function parseRange(str) {
  const s = String(str).trim();
  const m = /^(\d+)(?:-(\d+))?$/.exec(s);
  if (!m) throw new Error(`无效范围: ${str}（格式：1 或 1-5 或 96-100）`);
  const lo = parseInt(m[1], 10);
  const hi = m[2] ? parseInt(m[2], 10) : lo;
  if (hi < lo) throw new Error(`无效范围: ${str}（上限 < 下限）`);
  return [lo, hi];
}

/**
 * 格式化范围为字符串。
 */
export function formatRange(range) {
  if (!range) return "自动（目标<50 → 96-100；目标≥50 → 100）";
  const [lo, hi] = range;
  return lo === hi ? `${lo}` : `${lo}-${hi}`;
}
