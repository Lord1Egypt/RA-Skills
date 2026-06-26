/**
 * cognition.ts — Cognition Pipeline (SYNC)
 *
 * Attention gate, intent detection, strategy selection, implicit feedback.
 * Ported from handler.ts lines 444-570 with attention gate false-positive fix.
 */

import type { CogResult, CogHints, IntentSpectrum, EntropyFeedbackResult } from './types.ts'
import { body, bodyOnCorrection, bodyOnPositiveFeedback, emotionVector } from './body.ts'
import { getProfile, getProfileTier } from './user-profiles.ts'
import { CORRECTION_WORDS, CORRECTION_EXCLUDE, EMOTION_ALL, EMOTION_NEGATIVE, TECH_WORDS, CASUAL_WORDS } from './signals.ts'
import { DATA_DIR, loadJson, debouncedSave } from './persistence.ts'
import { resolve } from 'path'

// ── Layer 0: Bayesian Attention Gate ──
// Instead of first-match-wins, compute probability for ALL intent types simultaneously.
// Human analogy: when you hear "这段代码让我很烦", you simultaneously consider:
//   technical (代码) + emotional (烦) + correction (implicit frustration)
// The old if-else would pick just one. Bayesian picks the strongest signal.

interface AttentionHypothesis { type: string; score: number }

function attentionGate(msg: string): { type: string; priority: number } {
  const m = msg.toLowerCase()
  const hypotheses: AttentionHypothesis[] = [
    { type: 'correction', score: 0 },
    { type: 'emotional', score: 0 },
    { type: 'technical', score: 0 },
    { type: 'casual', score: 0 },
    { type: 'general', score: 1 }, // prior: general is default
  ]

  // Accumulate evidence for each hypothesis (not first-match-wins)
  const correctionHits = CORRECTION_WORDS.filter(w => m.includes(w)).length
  const correctionExclude = CORRECTION_EXCLUDE.some(w => m.includes(w))
  if (correctionHits > 0 && !correctionExclude) {
    hypotheses[0].score += correctionHits * 3 // strong signal
  }

  const emotionHits = EMOTION_ALL.filter(w => m.includes(w)).length
  hypotheses[1].score += emotionHits * 2

  const techHits = TECH_WORDS.filter(w => m.includes(w)).length
  hypotheses[2].score += techHits * 2

  const casualHits = CASUAL_WORDS.filter(w => m === w || m === w + '的').length
  hypotheses[3].score += casualHits * 2
  if (msg.length < 15) hypotheses[3].score += 1 // short messages lean casual

  // Length-based priors
  if (msg.length > 100) hypotheses[2].score += 0.5 // long messages lean technical
  if (msg.length < 8) hypotheses[3].score += 1 // very short lean casual

  // Negative emotion + technical = still emotional (not just technical)
  const negEmotionHits = EMOTION_NEGATIVE.filter(w => m.includes(w)).length
  if (negEmotionHits > 0 && techHits > 0) {
    hypotheses[1].score += 1 // boost emotional even when technical words present
  }


  // Pick winner via softmax — 分数差距大时高优先级，差距小时中性
  hypotheses.sort((a, b) => b.score - a.score)
  const winner = hypotheses[0]
  const expScores = hypotheses.map(h => Math.exp(h.score * 2))
  const sumExp = expScores.reduce((s, e) => s + e, 0)
  const winnerProb = expScores[0] / sumExp
  const priority = Math.min(10, Math.max(1, Math.round(winnerProb * 10)))
  return { type: winner.type, priority }
}

// ── Layer 1: Intent Detection ──

function detectIntent(msg: string): string {
  const m = msg.toLowerCase()
  if (['你觉得', '你看', '你认为', '你怎么看', '你的看法', '建议', 'what do you think', 'your opinion', 'suggestion', 'recommend'].some(w => m.includes(w))) return 'wants_opinion'
  if (['顺便', '另外', '还有', '对了'].some(w => m.includes(w))) return 'wants_proactive'
  if (m.endsWith('?') || m.endsWith('？') || ['吗', '呢', '么'].some(w => m.endsWith(w))) return 'wants_answer'
  if (msg.length < 20) return 'wants_quick'
  if (['做', '写', '改', '帮我', '实现', '生成', 'do', 'write', 'change', 'fix', 'create', 'help me'].some(w => m.includes(w))) return 'wants_action'
  return 'unclear'
}

// ── Layer 2: Strategy ──

function decideStrategy(attention: { type: string; priority: number }, intent: string, msgLen: number): string {
  if (attention.type === 'correction') return 'acknowledge_and_retry'
  if (attention.type === 'emotional') return 'empathy_first'
  if (intent === 'wants_quick' || msgLen < 10) return 'direct'
  if (intent === 'wants_opinion') return 'opinion_with_reasoning'
  if (intent === 'wants_action') return 'action_oriented'
  if (msgLen > 200) return 'detailed'
  return 'balanced'
}

// ── SYNC implicit feedback (fast keyword-based for immediate body state) ──

function detectImplicitFeedbackSync(msg: string, prevResponse: string): string | null {
  if (!prevResponse) return null
  const m = msg.toLowerCase()

  // Short reply after long answer = too verbose
  if (prevResponse.length > 500 && msg.length < 10 && ['嗯', '好', '行', '哦', 'ok'].some(w => m.includes(w))) {
    return 'too_verbose'
  }

  // Brief acknowledgment = silent accept
  if (['嗯', '好的', '明白', '了解', 'ok', '收到', '可以', '好', 'sure', 'got it', 'understood', 'alright'].some(w => m === w)) {
    return 'silent_accept'
  }

  // Enthusiastic response = positive
  if (['太好了', '牛', '厉害', '完美', '正是', '对对对', '就是这个', '感谢', 'great', 'perfect', 'exactly', "that's it", 'thanks'].some(w => m.includes(w))) {
    return 'positive'
  }

  return null
}

// ── Algorithm: Intent Spectrum (意图光谱) ──
// 不是分类为单一意图，而是输出连续多维评分
// 每个维度独立评分 [0-1]，可以同时有多种需求
// 认知科学基础：人的意图不是离散的分类，是连续的需求组合

export function computeIntentSpectrum(msg: string): IntentSpectrum {
  const len = msg.length
  const spectrum: IntentSpectrum = { information: 0.3, action: 0.1, emotional: 0.1, validation: 0.1, exploration: 0.1 }

  // 信息需求信号
  const infoSignals = (msg.match(/什么|怎么|为什么|哪个|多少|是不是|如何|区别|对比|原理|what|how|why|which|explain|difference|compare/gi) || []).length
  spectrum.information = Math.min(1, 0.2 + infoSignals * 0.2)

  // 行动需求信号
  const actionSignals = (msg.match(/帮我|做|写|改|实现|生成|创建|删除|修复|部署|安装|配置|help me|do|write|change|fix|create|delete|deploy|install/gi) || []).length
  spectrum.action = Math.min(1, actionSignals * 0.3)

  // 情感需求信号
  const emotionSignals = (msg.match(/烦|累|难受|焦虑|开心|郁闷|崩溃|压力|害怕|纠结|迷茫|无聊|孤独|annoyed|tired|sad|anxious|happy|stressed|overwhelmed|lonely/gi) || []).length
  spectrum.emotional = Math.min(1, emotionSignals * 0.35)

  // 验证需求信号
  const validationSignals = (msg.match(/对吗|是吧|可以吗|行不行|这样[好行对]|没问题吧|对不对|right\?|correct\?|is that ok|does that work|makes sense\?/gi) || []).length
  spectrum.validation = Math.min(1, validationSignals * 0.4)

  // 探索需求信号
  const explorationSignals = (msg.match(/有没有.*更|还有.*方法|其他|替代|更好|优化|改进|推荐|any other|alternative|better way|optimize|improve|recommend/gi) || []).length
  spectrum.exploration = Math.min(1, explorationSignals * 0.3)

  // 消息长度调节：长消息通常信息/行动需求高
  if (len > 100) { spectrum.information *= 1.2; spectrum.action *= 1.1 }
  // 短消息通常情感/验证需求高
  if (len < 15) { spectrum.emotional *= 1.3; spectrum.validation *= 1.2 }

  // 归一化到 [0, 1]
  for (const key of Object.keys(spectrum) as (keyof IntentSpectrum)[]) {
    spectrum[key] = Math.min(1, Math.max(0, spectrum[key]))
  }

  return spectrum
}

// ── Algorithm: Entropy Feedback (信息熵隐式反馈) ──
// 用信息论量化用户回复的"信息量"
// 高熵 = 用户给了很多新信息 = 对话有效
// 低熵 = "嗯""好""谢谢" = 可能结束或不满意
// 零 = 无回复 = 明确不满
// 基于 Shannon entropy: H = -Σ p(x) log₂ p(x)

export function computeResponseEntropy(userReply: string, prevBotResponse: string): EntropyFeedbackResult {
  if (!userReply || userReply.length < 2) return { entropy: 0, signal: 'disengaged' }

  // 提取用户回复中的独立词汇
  const userWords = new Set((userReply.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map(w => w.toLowerCase()))
  // 提取 bot 回复中的词汇
  const botWords = new Set((prevBotResponse.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map(w => w.toLowerCase()))

  // 计算用户回复中的"新信息"比例（不在 bot 回复中的词）
  let newWords = 0
  for (const w of userWords) {
    if (!botWords.has(w)) newWords++
  }
  const noveltyRatio = userWords.size > 0 ? newWords / userWords.size : 0

  // 字符级 Shannon 熵
  const charFreq = new Map<string, number>()
  for (const ch of userReply) {
    charFreq.set(ch, (charFreq.get(ch) || 0) + 1)
  }
  let entropy = 0
  for (const count of charFreq.values()) {
    const p = count / userReply.length
    if (p > 0) entropy -= p * Math.log2(p)
  }

  // 综合评分
  const combinedScore = entropy * 0.5 + noveltyRatio * 0.5

  // 判定
  const signal = combinedScore > 0.5 ? 'engaged'
    : combinedScore > 0.2 ? 'passive'
    : 'disengaged'

  return { entropy: combinedScore, signal }
}

// ── Intent Prediction from Behavioral Patterns ──

export function predictIntent(msg: string, _senderId: string, lastMsgs: string[]): string[] {
  const hints: string[] = []
  const m = msg.toLowerCase()

  // Pattern: Multiple short messages in sequence → user is describing a problem piece by piece
  if (lastMsgs.length >= 2 && lastMsgs.slice(-2).every(x => x.length < 50) && msg.length < 50) {
    hints.push('用户在连续发短消息描述问题，等他说完再回复，不要逐条回')
  }

  // Pattern: Single "?" or "？" → user is waiting for a response, urgent
  if (m === '?' || m === '？' || m === '...' || m === '???') {
    hints.push('用户在催回复，简短回应即可')
  }

  // Pattern: Screenshot/image sent → user wants you to LOOK at content, not praise
  if (msg.includes('[图片]') || msg.includes('[Image]') || msg.includes('截图')) {
    hints.push('用户发了图片/截图，关注内容本身，不要评价图片质量')
  }

  // Pattern: Message starts with forwarded content marker → user wants analysis
  if (msg.includes('[转发]') || msg.includes('转发') || msg.startsWith('>>')) {
    hints.push('这是转发的内容，用户想要你的分析/看法')
  }

  // Pattern: Code paste → user has a specific technical problem
  if (msg.includes('```') || msg.includes('error') || msg.includes('Error') || msg.includes('traceback')) {
    hints.push('用户贴了代码/错误信息，直接定位问题给解决方案')
  }

  // Pattern: Long message with numbers/data → user wants analysis not summary
  if (msg.length > 200 && (msg.match(/\d+/g) || []).length > 5) {
    hints.push('消息包含大量数据/数字，做分析而不是摘要')
  }

  return hints
}

// ── Atmosphere Sensing: overall conversation vibe from patterns ──

export function detectAtmosphere(
  currentMsg: string,
  recentHistory: { user: string }[]
): string[] {
  const hints: string[] = []

  // Pattern 1: User sending very short messages (1-5 chars) → busy/distracted
  const recentLengths = recentHistory.slice(-3).map(h => h.user.length)
  if (recentLengths.length >= 2 && recentLengths.every(l => l < 5)) {
    hints.push('用户连续发极短消息，可能在忙，回复也要简短')
  }

  // Pattern 2: Long detailed message → serious/focused
  if (currentMsg.length > 300) {
    hints.push('用户写了很长的描述，说明在认真讨论，给详细的回复')
  }

  // Pattern 3: Emoji/casual markers → relaxed
  if (/[😂😊🤣👍❤️💀😭🥲]|哈哈|嘿嘿|呵呵/.test(currentMsg)) {
    hints.push('对话氛围轻松，可以随意一些')
  }

  // Pattern 4: Questions piling up without cc answering → user waiting
  if (currentMsg.endsWith('？') || currentMsg.endsWith('?')) {
    const recentQuestions = recentHistory.slice(-3).filter(h => h.user.endsWith('？') || h.user.endsWith('?'))
    if (recentQuestions.length >= 2) {
      hints.push('用户连续提问，可能之前的回答没到位，这次要更直接')
    }
  }

  // Pattern 5: Time-based atmosphere
  const hour = new Date().getHours()
  if (hour >= 22 || hour < 6) {
    hints.push('深夜对话，简洁为主')
  }

  return hints
}

// ── Conversation Pace Sensing ──

export interface ConversationPace {
  speed: 'rapid' | 'normal' | 'slow'
  avgMsgLength: number
  msgsPerMinute: number
  hint: string | null
}

/**
 * Detect conversation pace from recent message history.
 * Adjusts response verbosity: rapid pace → shorter replies, slow pace → can be detailed.
 */
export function detectConversationPace(
  currentMsg: string,
  recentHistory: { user: string; ts?: number }[],
): ConversationPace {
  const recent = recentHistory.slice(-5)
  if (recent.length < 2) return { speed: 'normal', avgMsgLength: currentMsg.length, msgsPerMinute: 0, hint: null }

  // Average message length
  const lengths = recent.map(h => h.user.length)
  const avgLen = lengths.reduce((s, l) => s + l, 0) / lengths.length

  // Messages per minute (if timestamps available)
  let msgsPerMinute = 0
  const timestamps = recent.filter(h => h.ts).map(h => h.ts!)
  if (timestamps.length >= 2) {
    const timeSpan = Math.max((timestamps[timestamps.length - 1] - timestamps[0]) / 60000, 0.5)
    msgsPerMinute = timestamps.length / timeSpan
  }

  // Determine pace
  let speed: 'rapid' | 'normal' | 'slow' = 'normal'
  let hint: string | null = null

  if ((msgsPerMinute > 3 || (msgsPerMinute > 1 && avgLen < 20)) && recent.length >= 3) {
    speed = 'rapid'
    hint = '用户发消息节奏很快（短消息连发），回复要简短精炼，不要长篇大论'
  } else if (msgsPerMinute > 0 && msgsPerMinute < 0.3 && avgLen > 100) {
    speed = 'slow'
    hint = '用户节奏较慢但每条消息很长，说明在深度思考，可以给详细回复'
  }

  return { speed, avgMsgLength: avgLen, msgsPerMinute, hint }
}

// ═══════════════════════════════════════════════════════════════════════════════
// P5b: Intent Momentum（替换 NB + PA 分类器）
// 对话惯性：连续同类意图 → 该维度加强，突然切换 → reset
// ═══════════════════════════════════════════════════════════════════════════════

const MOMENTUM_WINDOW = 5  // 看最近 5 轮的意图历史
const MOMENTUM_BOOST = 0.2  // 惯性加成
const MOMENTUM_THRESHOLD = 3  // 连续 3 次同类才触发惯性

let _recentIntentTypes: string[] = []  // 最近的 attention types

/** 记录本轮意图类型，维护滑动窗口 */
function recordIntentType(type: string): void {
  _recentIntentTypes.push(type)
  if (_recentIntentTypes.length > MOMENTUM_WINDOW) {
    _recentIntentTypes = _recentIntentTypes.slice(-MOMENTUM_WINDOW)
  }
}

/**
 * P5b: applyIntentMomentum — 对话惯性调制 Intent Spectrum
 *
 * 连续 3 条同类意图 → 该维度惯性 +0.2
 * 突然话题切换（当前类型与最近 3 条都不同）→ 全维度 reset to base
 */
export function applyIntentMomentum(spectrum: IntentSpectrum, currentType: string): IntentSpectrum {
  recordIntentType(currentType)

  if (_recentIntentTypes.length < MOMENTUM_THRESHOLD) return spectrum

  const recent = _recentIntentTypes.slice(-MOMENTUM_THRESHOLD)
  const allSame = recent.every(t => t === currentType)

  if (allSame) {
    // 连续同类 → 惯性加成
    const result = { ...spectrum }
    const spectrumKey = intentTypeToSpectrumKey(currentType)
    if (spectrumKey && spectrumKey in result) {
      result[spectrumKey] = Math.min(1, result[spectrumKey] + MOMENTUM_BOOST)
    }
    return result
  }

  // 检测突然切换：当前类型与最近几条完全不同
  const recentTypes = new Set(_recentIntentTypes.slice(-3))
  if (!recentTypes.has(currentType) && recentTypes.size === 1) {
    // 突然从一个稳定话题切换 → 通知 AAM 做 damping
    try {
      const { onTopicSwitch } = require('./aam.ts')
      // 旧话题：最近稳定的意图类型对应的词
      const oldType = [...recentTypes][0]
      const oldWords = _recentIntentTypes.slice(-3).map(t => t.toLowerCase())
      const newWords = [currentType.toLowerCase()]
      onTopicSwitch(oldWords, newWords)
    } catch {}
    return spectrum
  }

  return spectrum
}

/** Spectrum key → attention type（反向映射，用于 Intent Superposition） */
function spectrumKeyToAttentionType(key: string): string | null {
  switch (key) {
    case 'information': return 'technical'
    case 'emotional': return 'emotional'
    case 'exploration': return 'casual'
    case 'validation': return 'correction'
    case 'action': return 'technical'
    default: return null
  }
}

function intentTypeToSpectrumKey(type: string): keyof IntentSpectrum | null {
  switch (type) {
    case 'technical': return 'information'
    case 'emotional': return 'emotional'
    case 'casual': return 'exploration'
    case 'correction': return 'validation'
    default: return null
  }
}


// ── Main Entry ──

export function cogProcess(msg: string, lastResponseContent: string, lastPrompt: string, senderId?: string): CogResult {
  // Intent Superposition：先算连续光谱，再从光谱派生离散标签（兼容旧消费者）
  const intent = detectIntent(msg)
  const intentSpectrum = computeIntentSpectrum(msg)

  // 从光谱派生 attention type（替代独立的 attentionGate 分类）
  // 保留 attentionGate 处理 correction 检测（关键词精确匹配比光谱更可靠）
  const attention = attentionGate(msg)
  // 光谱叠加：如果光谱最强维度跟 attentionGate 不一致，用光谱的
  const spectrumDims = Object.entries(intentSpectrum) as [string, number][]
  spectrumDims.sort((a, b) => b[1] - a[1])
  const spectrumType = spectrumKeyToAttentionType(spectrumDims[0][0])
  // correction 由 attentionGate 权威判定（关键词精确匹配），其他维度由 spectrum 判定
  if (attention.type !== 'correction' && spectrumType && spectrumDims[0][1] > 0.5) {
    attention.type = spectrumType
  }

  // P5b: 对话惯性调制
  const modulatedSpectrum = applyIntentMomentum(intentSpectrum, attention.type)
  const complexity = Math.min(1, msg.length / 500)
  const strategy = decideStrategy(attention, intent, msg.length)
  const hints: string[] = []

  // Correction handling — weighted by user tier
  if (attention.type === 'correction') {
    const profile = senderId ? getProfile(senderId) : null
    const tier = profile?.tier || 'new'

    if (tier === 'owner') {
      hints.push('⚠ 主人在纠正你，这是高权重反馈，必须认真对待并调整')
      bodyOnCorrection() // full correction impact
    } else if (tier === 'known') {
      hints.push('⚠ 老朋友在纠正你，注意调整')
      // Moderate correction — lighter than full bodyOnCorrection
      body.alertness = Math.min(1.0, body.alertness + 0.1)
      body.mood = Math.max(-1, body.mood - 0.05)
      // Sync emotionVector (mirrors bodyOnCorrection but without double body state update)
      const clamp = (v: number) => Math.max(-1, Math.min(1, v))
      emotionVector.certainty = clamp(emotionVector.certainty - 0.2)
      emotionVector.dominance = clamp(emotionVector.dominance - 0.1)
      emotionVector.pleasure = clamp(emotionVector.pleasure - 0.15)
    } else {
      hints.push('新用户反馈，可能是期望管理问题，温和对待')
      // Minimal impact — might just be expectation mismatch
      body.alertness = Math.min(1.0, body.alertness + 0.05)
      // Sync emotionVector (lighter — halved deltas for new user)
      const clamp = (v: number) => Math.max(-1, Math.min(1, v))
      emotionVector.certainty = clamp(emotionVector.certainty - 0.1)
      emotionVector.dominance = clamp(emotionVector.dominance - 0.05)
      emotionVector.pleasure = clamp(emotionVector.pleasure - 0.08)
    }
    // brain + patterns.ts removed — success tracking retired
  }

  // Emotional handling
  if (attention.type === 'emotional') {
    const neg = EMOTION_NEGATIVE.some(w => msg.includes(w))
    if (neg) {
      hints.push('情绪信号：低落')
      body.mood = Math.max(-1, body.mood - 0.15)
    } else {
      hints.push('情绪信号：积极')
      body.mood = Math.min(1, body.mood + 0.1)
    }
  }

  // Strategy hints
  if (strategy === 'direct') hints.push('简短回答即可')
  if (strategy === 'opinion_with_reasoning') hints.push('给出明确立场和理由，不说"各有优劣"')
  if (strategy === 'action_oriented') hints.push('先给代码/方案，再解释')
  if (strategy === 'empathy_first') hints.push('策略：共情优先')
  if (strategy === 'acknowledge_and_retry') hints.push('先承认错误，再给出正确答案')

  // SYNC implicit feedback (fast, for immediate body state)
  const implicit = detectImplicitFeedbackSync(msg, lastResponseContent)
  const entropyFeedback = computeResponseEntropy(msg, lastResponseContent)
  // Entropy feedback supplements implicit feedback: low entropy + disengaged = additional verbosity signal
  if (entropyFeedback.signal === 'disengaged' && !implicit) {
    hints.push('用户回复信息量很低，可能在敷衍或准备结束对话')
  }
  if (implicit === 'too_verbose') {
    body.energy = Math.max(0, body.energy - 0.03)
    hints.push('上次回答可能太长了，这次简洁些')
  } else if (implicit === 'silent_accept') {
    // brain removed
  } else if (implicit === 'positive') {
    bodyOnPositiveFeedback()
    // brain removed
  }

  // Tier-based strategy adjustment
  if (senderId) {
    const tier = getProfileTier(senderId)
    if (tier === 'owner') {
      hints.push('主人在说话，技术深度优先，少废话')
    } else if (tier === 'new') {
      hints.push('新用户，耐心观察，先了解对方再适配风格')
    }
  }

  return { hints, intent, strategy, attention: attention.type, complexity, spectrum: modulatedSpectrum, entropyFeedback }
}

/**
 * CGAF: 从 CogResult 提取 Bayesian 概率作为 activation-field 信号调制器。
 * 独立函数，benchmark 可以直接调用 computeIntentSpectrum + toCogHints（不需要完整 cogProcess）
 */
export function toCogHints(msg: string): CogHints {
  const m = msg.toLowerCase()
  const spectrum = computeIntentSpectrum(msg)

  // 复用 attentionGate 的 Bayesian 逻辑（但提取概率分布而非离散标签）
  const scores = { correction: 0, emotional: 0, technical: 0, casual: 0, general: 1 }

  // correction 信号
  const corrHits = CORRECTION_WORDS.filter(w => m.includes(w)).length
  const corrExclude = CORRECTION_EXCLUDE.some(w => m.includes(w))
  if (corrHits > 0 && !corrExclude) scores.correction += corrHits * 3

  // emotion 信号
  scores.emotional += EMOTION_ALL.filter(w => m.includes(w)).length * 2

  // technical 信号
  scores.technical += TECH_WORDS.filter(w => m.includes(w)).length * 2

  // casual 信号
  scores.casual += CASUAL_WORDS.filter(w => m === w || m === w + '的').length * 2
  if (msg.length < 15) scores.casual += 1
  if (msg.length < 8) scores.casual += 1

  // length priors
  if (msg.length > 100) scores.technical += 0.5

  // LOCOMO 英文补充信号（中文词表覆盖不足时的 fallback）
  // temporal 信号映射到 technical（需要精确召回）
  if (/when did|last time|how long ago|what year|what month|what date|recently|before that/i.test(msg)) scores.technical += 2
  // entity 查询信号
  const entityNames = (msg.match(/\b[A-Z][a-z]{2,}\b/g) || []).filter(n => !/^(What|When|Where|How|Who|Which|Why|The|This|That|Does|Did|Has|Have|Was|Were|Can|Could|Would|Should|Not)$/.test(n))
  if (entityNames.length > 0) scores.technical += 1.5
  // why/cause 查询信号
  if (/why|because|cause|reason|how come/i.test(msg)) scores.technical += 1
  // opinion/feeling 查询
  if (/feel|happy|sad|anxious|stressed|mood|emotion|opinion|think about/i.test(msg)) scores.emotional += 2
  // casual 英文
  if (/^(hey|hi|hello|yo|sup|what's up|how are you)/i.test(msg)) scores.casual += 3

  // Softmax → 概率分布
  const keys = ['correction', 'emotional', 'technical', 'casual', 'general'] as const
  const expScores = keys.map(k => Math.exp(scores[k] * 1.5))
  const sumExp = expScores.reduce((s, e) => s + e, 0)
  const probs = Object.fromEntries(keys.map((k, i) => [k, expScores[i] / sumExp])) as Record<string, number>

  return {
    correctionProb: probs.correction,
    emotionalProb: probs.emotional,
    technicalProb: probs.technical,
    casualProb: probs.casual,
    complexity: Math.min(1, msg.length / 500),
    spectrum,
  }
}
