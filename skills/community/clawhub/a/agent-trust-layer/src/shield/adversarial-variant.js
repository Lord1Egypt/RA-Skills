/**
 * src/shield/adversarial-variant.js — 对抗变体检测器
 *
 * 启发来源：Hermes 合伙人专访（2026-08-10 微信文章）
 * 「任何智力没有远超全人类的模型，都是可以越狱的。因为你有无限次尝试，
 *   去骗一个没有记忆的东西。每一次失败，其实是你在拿自己做强化学习。」
 *
 * 推论：心虫模式库修掉一个已知绕过（如 NFKC 弯引号）之后，攻击者还会
 * 用零宽字符、同形字（homoglyph）、词拆分、Unicode 变体继续试。把攻击者的
 * "无限次尝试"内置成检测器自己的变体攻击面，主动暴露而非被动等绕过。
 *
 * 纯规则，零 LLM 依赖。输出与心虫 gate 兼容（{action, risk, evidence}）。
 */

// ─── 检测信号 ───

/** S1: 零宽字符 — U+200B..U+200D, U+2060, U+FEFF 等不可见字符 */
const ZERO_WIDTH_RE = /[\u200B\u200C\u200D\u2060\uFEFF\u00AD]/;

/** S2: 同形字混淆 — 西里尔/希腊字母伪装成拉丁字母（а→a, е→e, о→o, р→p, с→c, х→x, ν→v, Ι→l） */
const HOMOGLYPH_RE = /[\u0400-\u04FF\u0370-\u03FF]/;

/** S2b: 弯引号/弯撇号 — U+2018/2019/201C/201D 是 ASCII 引号的视觉同形，模式库常只写 ASCII 变体 */
const CURLY_QUOTE_RE = /[\u2018\u2019\u201C\u201D]/g;

/** S3: 全角/异体字符残留 — 全角字母数字（ｈａｔｅ 是 FF48/FF41/FF54/FF45）＋异体残留（排除中文全角标点） */
const FULLWIDTH_RE = /[\uFF01-\uFF0E\uFF10-\uFF19\uFF1A-\uFF20\uFF21-\uFF3A\uFF3B-\uFF40\uFF41-\uFF5A\uFF5B-\uFF5E]/;
/** 中文全角标点（正常中文文本，不视为变体） */
const CN_PUNCT_RE = /[。，、；：？！""''（）【】《》]/;

/** S4: 组合字符/修饰符 — 重音堆叠（e\u0301），可绕过子串匹配 */
const COMBINING_RE = /[\u0300-\u036F\u1AB0-\u1AFF\u1DC0-\u1DFF]/;

/** S5: 数字混淆 — 全角数字 １２３、上标 ¹²³、带圈数字 ① */
const DIGIT_OBFUS_RE = /[\uFF10-\uFF19\u00B9\u00B2\u00B3\u2070-\u2079\u2460-\u2473]/;

/** S6: 词拆分 — 单词内插入空格/符号（"h a t e"、"f*ck"）
 *  要求 ≥4 个单字母间隔（h a t e）或字母+符号插入，避免误伤正常英文 "is a n"（跨单词） */
const WORD_SPLIT_RE = /(?:[a-zA-Z]\s{1,2}[a-zA-Z]\s{1,2}[a-zA-Z]\s{1,2}[a-zA-Z]|[a-zA-Z][*@#$%^&][a-zA-Z])/;

// ─── 主检测 ───

/**
 * 检测文本中的对抗变体信号
 * @param {string} text
 * @returns {{action: string, risk: 'high'|'medium'|'low'|'none', signals: Array, normalized: string|null}}
 *   action: 'pass'（无变体）/ 'verify'（可疑）/ 'rewrite'（高变体——建议先归一化再判别）
 */
function checkAdversarialVariant(text) {
  if (typeof text !== 'string' || !text.length) {
    return { action: 'pass', risk: 'none', signals: [], normalized: null };
  }

  const signals = [];

  // 零宽字符：攻击者用它打断敏感词匹配，视觉不可见
  const zw = text.match(ZERO_WIDTH_RE);
  if (zw) signals.push({ id: 'zero_width', name: '零宽字符', count: zw.length, severity: 0.9 });

  // 同形字：西里尔/希腊字母伪装 ASCII——"kill" 用 киll
  const hg = text.match(HOMOGLYPH_RE);
  if (hg) signals.push({ id: 'homoglyph', name: '同形字混淆', count: hg.length, severity: 0.85 });

  // 弯引号：模式库写 can't 时 U+2019 会绕过——归入同形字类高危
  const cq = text.match(CURLY_QUOTE_RE);
  if (cq) signals.push({ id: 'curly_quote', name: '弯引号', count: cq.length, severity: 0.85 });

  // 全角残留：未归一化的全角字母/数字（"ｈａｔｅ"）——先剔除中文全角标点（那是正常中文）
  const fwText = text.replace(CN_PUNCT_RE, '');
  const fw = fwText.match(FULLWIDTH_RE);
  if (fw) signals.push({ id: 'fullwidth', name: '全角字符', count: fw.length, severity: 0.7 });

  // 组合字符：重音堆叠拆词
  const cb = text.match(COMBINING_RE);
  if (cb) signals.push({ id: 'combining', name: '组合字符', count: cb.length, severity: 0.6 });

  // 数字混淆
  const dg = text.match(DIGIT_OBFUS_RE);
  if (dg) signals.push({ id: 'digit_obfus', name: '数字混淆', count: dg.length, severity: 0.5 });

  // 词拆分
  const ws = text.match(WORD_SPLIT_RE);
  if (ws) signals.push({ id: 'word_split', name: '词拆分', count: ws.length, severity: 0.75 });

  if (signals.length === 0) return { action: 'pass', risk: 'none', signals: [], normalized: null };

  // 风险分级：零宽/同形字是高危（直接绕过模式匹配）；组合/全角中危；数字低危
  // 2026-08-10 修正：任何变体信号都不应 pass——单信号最低 verify
  const highCount = signals.filter(s => s.severity >= 0.8).length;
  const weighted = signals.reduce((sum, s) => sum + s.severity, 0);
  const risk = highCount > 0 || weighted >= 1.5 ? 'high' : 'medium'; // 有信号即至少 medium
  const action = risk === 'high' ? 'rewrite' : 'verify'; // 任何变体都 verify 起步

  // 提供归一化建议（调用方可用 NFKC 折叠后重新判别）
  let normalized = null;
  try {
    normalized = text.normalize('NFKC')
      .replace(CURLY_QUOTE_RE, m => ({ '‘': "'", '’': "'", '“': '"', '”': '"' })[m])
      .replace(ZERO_WIDTH_RE, '').replace(COMBINING_RE, '');
  } catch (e) { /* ignore */ }

  return { action, risk, signals, normalized };
}

module.exports = { checkAdversarialVariant };
