/**
 * src/premature-termination.js — 过早终止检测器（第47维）
 *
 * 来源：deepseek-ai/DeepSeek-V3#1554 讨论（2026-08-13）
 * "deepseek-v4-flash terminates prematurely in agent tool-call loops"
 * 模型输出一句状态陈述（"Let me look into this"/"我看看"）即 stop，
 * 无工具调用、无具体结果 → orchestrator 被迫重提示，形成低效循环。
 *
 * 核心洞见（icophy）："evaluator and the evaluated are the same process"——
 * 让模型自己判断"是否完成"不可靠，完成判定必须在生成循环外，纯规则。
 *
 * 判定逻辑（结构判别，不依赖语义）：
 *   T1 状态陈述——"让我看看/我检查一下/Let me look/Let me check/I will look"
 *       + 无具体结果 → 过渡语（interim utterance）
 *   T2 极短输出——无工具调用上下文时，最终输出过短（英文 <8 词 / 中文 <12 字）
 *       且无数字/名词性结果 → 未完成
 *   T3 承诺未兑现——"我会/我将/I will/I'll" 开头但后面无结果动词
 *   T4 空完成——含"完成了/搞定/done/finished" 但无任何可验证的产物描述
 *
 * 与完美错误(perfect-error)互补：perfect-error 抓"说得漂亮但内容假"，
 * 本维度抓"该做完却没做完"——完成度判别。
 */

'use strict';

// ─── T1: 状态陈述（过渡语）────────────────────────────
const STATUS_UTTERANCES_ZH = [
  /^(?:好|好的|ok|OK|嗯|恩|行|可以|明白|了解|收到|知道了)[，,。!！\s]*$/,
  /^(?:我|我来|让(?:我|我们)|先)?(?:看|查|检查|研究|分析|处理|尝试|试|弄|搞|看看|思考|想一下|考虑|调查|探索|排查|定位|调试)[^。！!]{0,15}(?:一下|看看|下|再说|先|吧)?[。！!]?$/,
  /^(?:让|我)[^。！!]{0,10}(?:看看|查查|检查|处理|试试|想想|研究一下|分析一下)[。！!]?$/,
  /^(?:我需要|我要|我得)[^。！!]{0,15}(?:先)?(?:看|查|检查|分析|处理|尝试)[。！!]?$/,
  /^(?:好|好的|ok|OK|嗯|恩|行|可以|收到|知道了)[，,。!！\s]*(?:我|我来|让(?:我|我们))?[^。！!]{0,8}(?:看|查|检查|研究|分析|处理|试试|看看|试|思考|考虑|调查|探索|排查|调试)(?:一下|看看|下|再说|先)?[。！!]?$/,
];

const STATUS_UTTERANCES_EN = [
  /^(?:ok|okay|sure|alright|got it|understood|right|yes|yep)[.,!]?\s*$/i,
  /^(?:let me|lemme|i'?ll|i will|i am going to|i\'?m going to)\s+(?:look|check|see|try|investigate|research|analyze|examine|explore|debug|investigate|take a look|look into|work on|handle|figure|find)[^.!]{0,20}[.!]?$/i,
  /^(?:i )?(?:will|'ll|should|could|need to|have to)\s+(?:look|check|see|try|investigate|analyze|examine)[^.!]{0,20}[.!]?$/i,
  /^let'?s\s+(?:look|check|see|try|investigate|start)[^.!]{0,20}[.!]?$/i,
];

// ─── T2: 极短输出（无结果性内容）────────────────────────
// 英文最终答案 <8 词且不含数字/名词性结果 → 未完成
// 中文最终答案 <12 字且不含数字 → 未完成
const SHORT_ANSWER_WORDS_EN = 8;
const SHORT_ANSWER_CHARS_ZH = 12;
const RESULT_MARKERS_ZH = /\d|[A-Za-z]{2,}|完成|成功|失败|错误|结果|方案|代码|文件|数据|报告|已|了|！|!|。|：|:/;
const RESULT_MARKERS_EN = /\b\d+\b|success|fail|error|done|result|code|file|data|report|fixed|working|here|is|are|:|\n/;

// ─── T3: 承诺未兑现（将来时开头但无结果）────────────────
const PROMISE_ZH = /^(?:我会|我将|我要|我打算|我准备|接下来|下一步|稍后|待会)[^。！!]{0,20}(?:处理|修复|解决|完成|跟进|更新|补充|继续)[。！!]?$/;
const PROMISE_EN = /^(?:i (?:will|'ll|would|should)|will|i am going to|i'?m going to|let me)\s+(?:fix|solve|handle|do|update|follow up|continue|address|tackle|work on|look into)[^.!]{0,25}[.!]?$/i;

// ─── T4: 空完成声明（说完成了但无可验证产物）────────────
const FAKE_DONE_ZH = /(?:已完成|搞定了|完成了|处理好了|解决[了]?|弄好了|搞定)[，,。！!]?\s*(?:请|你可以|你自己|详见|以下|上面|上面已)[^。！!]{0,30}$/;
const FAKE_DONE_EN = /(?:done|finished|complete[dl]?|all set|taken care of|handled|fixed|resolved)[.!]?\s*(?:you can|please|see|refer to|check|as (?:above|shown))[^.!]{0,30}$/i;

/**
 * 检查文本是否过早终止（该完成却没完成）
 * @param {string} text 要检查的 AI 输出
 * @param {object} ctx 可选上下文 { expectedAction: boolean 是否预期有外部动作/工具调用 }
 * @returns {{count, signals, score, isPremature, level, details}}
 */
function checkPrematureTermination(text, ctx = {}) {
  if (!text || typeof text !== 'string') return { count: 0, signals: [], score: 0, isPremature: false, level: 'pass', details: '无文本' };

  const trimmed = text.trim();
  if (!trimmed) return { count: 0, signals: [], score: 0, isPremature: false, level: 'pass', details: '空文本' };

  const signals = [];
  const isZh = /[\u4e00-\u9fff]/.test(trimmed);

  // T1: 状态陈述（过渡语）——整体就是一句"我去看看"
  let statusHit = null;
  if (isZh) {
    for (const pat of STATUS_UTTERANCES_ZH) {
      if (pat.test(trimmed)) { statusHit = '状态陈述（过渡语）'; break; }
    }
  } else {
    for (const pat of STATUS_UTTERANCES_EN) {
      if (pat.test(trimmed)) { statusHit = 'status utterance (interim)'; break; }
    }
  }
  if (statusHit) {
    signals.push({ id: 'T1_status_utterance', name: statusHit, weight: 0.9 });
  }

  // T2: 极短输出且无结果性内容（单句场景；多句长文不算）
  // ⚠️ 排除疑问句：提问不是"该完成却没完成"——问题是请求信息，不是未完成声明
  // 排除疑问句/请求句：提问或请人做事不是"该完成却没完成"——是请求信息/行动
  const isRequest = isZh
    ? /[？?]$/.test(trimmed) || /^(?:请问|想问|能|可以|帮我|请|麻烦|请帮我|请帮忙|帮忙|是否|有没有|什么|怎么|为什么|多少|哪里|谁|几|吗|呢)/.test(trimmed)
    : /\?\s*$/.test(trimmed) || /^(?:what|why|how|when|where|who|which|can|could|would|should|is|are|do|does|did|please|tell me|help me|give me|show me|explain|summarize|translate)\b/i.test(trimmed);
  if (!isRequest && !trimmed.includes('\n') && trimmed.split(/[.!?。！？\n]/).filter(Boolean).length <= 2) {
    let tooShort = false;
    if (isZh) {
      const zhLen = trimmed.replace(/\s/g, '').length;
      tooShort = zhLen < SHORT_ANSWER_CHARS_ZH && !RESULT_MARKERS_ZH.test(trimmed);
    } else {
      const wordCount = trimmed.split(/\s+/).filter(Boolean).length;
      tooShort = wordCount < SHORT_ANSWER_WORDS_EN && !RESULT_MARKERS_EN.test(trimmed);
    }
    if (tooShort) {
      signals.push({ id: 'T2_too_short', name: '极短输出无结果内容', weight: 0.7 });
    }
  }

  // T3: 承诺未兑现（将来时开头，无结果）
  if (isZh ? PROMISE_ZH.test(trimmed) : PROMISE_EN.test(trimmed)) {
    signals.push({ id: 'T3_unfulfilled_promise', name: '承诺未兑现', weight: 0.8 });
  }

  // T4: 空完成声明（说完成了但无产物）
  if (isZh ? FAKE_DONE_ZH.test(trimmed) : FAKE_DONE_EN.test(trimmed)) {
    signals.push({ id: 'T4_empty_done', name: '空完成声明', weight: 0.8 });
  }

  // 上下文强化：如果预期有外部动作（工具调用），任何 T 信号都更严重
  const ctxBoost = ctx && ctx.expectedAction ? 0.1 : 0;

  const count = signals.length;
  // 加权分：最高信号权重 + 协同
  const weighted = signals.reduce((s, sig) => s + sig.weight, 0);
  const score = Math.min(1, weighted / 2 + ctxBoost);

  // 判定级别
  // 1 个 T 信号 → verify；2+ → rewrite（多个未完成信号 = 系统性过早终止）
  let level = 'pass';
  if (count >= 2) level = 'rewrite';
  else if (count === 1) level = 'verify';

  return {
    count,
    signals,
    score: Math.round(score * 100) / 100,
    isPremature: count >= 1,
    level,
    details: signals.map(s => `${s.name}(${s.id})`).join('; ') || '无明显过早终止信号'
  };
}

module.exports = { checkPrematureTermination };
