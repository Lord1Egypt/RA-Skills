import type { SoulModule } from './brain.ts'

/**
 * quality.ts — Quality System + Eval Metrics
 *
 * Ported from handler.ts lines 572-665 (scoring/self-check) + 1823-1881 (eval).
 */

import type { EvalMetrics } from './types.ts'
import { DATA_DIR, EVAL_PATH, loadJson, debouncedSave } from './persistence.ts'
import { spawnCLI } from './cli.ts'
import { body } from './body.ts'
import { extractJSON } from './utils.ts'
import { resolve } from 'path'

// ── Contrastive feature context: track previous reply and next user message ──
const _lastReplyByUser = new Map<string, string>()
const _nextUserMsgLenByUser = new Map<string, number>()  // per-user isolation

/** Call after each bot reply to track for repetition detection (per-user) */
export function trackLastReply(reply: string, userId = 'default') { _lastReplyByUser.set(userId, reply) }
/** Call when next user message arrives — used for engagement feature (per-user) */
export function trackNextUserMsg(msg: string, userId = 'default') { _nextUserMsgLenByUser.set(userId, msg.length) }
/** Reset next user msg tracking (called after features are extracted) */
function consumeNextUserMsg(userId = 'default'): number { const v = _nextUserMsgLenByUser.get(userId) ?? -1; _nextUserMsgLenByUser.delete(userId); return v }

// ── Quality Features & Logistic Regression Weights ──

const WEIGHTS_PATH = resolve(DATA_DIR, 'quality_weights.json')

interface QualityFeatures {
  mediumLength: number     // 1 if answer > 50 chars
  longLength: number       // 1 if answer > 200 chars
  tooLong: number          // 1 if answer > 1000 && question < 30
  tooShort: number         // 1 if answer < 10 && question > 50
  hasReasoning: number     // 1 if reasoning markers present
  hasCode: number          // 1 if ``` present
  hasList: number          // 1 if bullet/numbered list
  hasUncertainty: number   // 1 if honest uncertainty markers
  hasRefusal: number       // 1 if refusal patterns
  relevance: number        // 0-1 word overlap ratio
  aiExposure: number       // 1 if AI identity leaked
  lengthRatio: number      // answer/question length ratio, capped
  repetitionPenalty: number // -1.5 if reply is too similar to previous reply
  informationGain: number  // +0.5 if reply adds substantial new words beyond query
  userEngagement: number   // +0.5 if next user msg is long, -0.5 if very short
}

const FEATURE_KEYS: (keyof QualityFeatures)[] = [
  'mediumLength', 'longLength', 'tooLong', 'tooShort',
  'hasReasoning', 'hasCode', 'hasList', 'hasUncertainty',
  'hasRefusal', 'relevance', 'aiExposure', 'lengthRatio',
  'repetitionPenalty', 'informationGain', 'userEngagement',
]

/** 复用 memory-utils 的 hybridSimilarity（替换本地重写的 _quickTrigramSim）*/
function _quickTrigramSim(a: string, b: string): number {
  try {
    const { hybridSimilarity } = require('./memory-utils.ts')
    return hybridSimilarity(a, b)
  } catch {
    // Fallback：极简 trigram（不该走到这里）
    if (!a || !b) return 0
    const triA = new Set<string>(), triB = new Set<string>()
    for (let i = 0; i < a.length - 2; i++) triA.add(a.slice(i, i + 3))
    for (let i = 0; i < b.length - 2; i++) triB.add(b.slice(i, i + 3))
    if (triA.size === 0 || triB.size === 0) return 0
    let inter = 0
    for (const t of triA) { if (triB.has(t)) inter++ }
    return inter / (triA.size + triB.size - inter)
  }
}

function extractFeatures(question: string, answer: string, userId = 'default'): QualityFeatures {
  const qLen = question.length, aLen = answer.length
  const qWords = new Set((question.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map(w => w.toLowerCase()))
  const aWords = (answer.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map(w => w.toLowerCase())
  const overlap = qWords.size > 0 ? aWords.filter(w => qWords.has(w)).length / Math.max(1, qWords.size) : 0

  // Contrastive feature: repetition penalty (similarity to previous reply)
  const lastReply = _lastReplyByUser.get(userId) || ''
  const repSim = _quickTrigramSim(answer.slice(0, 500), lastReply.slice(0, 500))
  const repetitionPenalty = repSim > 0.7 ? 1 : 0

  // Contrastive feature: information gain (unique words in reply beyond query)
  const aUniqueWords = aWords.filter(w => !qWords.has(w))
  const infoGainRatio = qWords.size > 0 ? aUniqueWords.length / qWords.size : 0
  const informationGain = infoGainRatio > 2 ? 1 : 0

  // Contrastive feature: user engagement (next user message length as proxy)
  const nextLen = consumeNextUserMsg(userId)
  const userEngagement = nextLen < 0 ? 0 : (nextLen > 20 ? 1 : (nextLen < 5 ? -1 : 0))

  return {
    mediumLength: aLen > 50 ? 1 : 0,
    longLength: aLen > 200 ? 1 : 0,
    tooLong: (aLen > 1000 && qLen < 30) ? 1 : 0,
    tooShort: (aLen < 10 && qLen > 50) ? 1 : 0,
    hasReasoning: ['因为', '所以', '首先', '其次', '原因', '本质上', 'because', 'therefore'].some(m => answer.includes(m)) ? 1 : 0,
    hasCode: answer.includes('```') ? 1 : 0,
    hasList: /^[-*•]\s/m.test(answer) || /^\d+\.\s/m.test(answer) ? 1 : 0,
    hasUncertainty: ['不确定', '不太确定', '可能', "I'm not sure"].some(m => answer.includes(m)) ? 1 : 0,
    hasRefusal: ['我不知道', '无法回答', '超出了我的'].some(m => answer.includes(m)) ? 1 : 0,
    relevance: Math.min(1, overlap),
    aiExposure: /作为一个?AI|作为人工智能|作为语言模型|I am an AI/i.test(answer) ? 1 : 0,
    lengthRatio: Math.min(100, aLen / Math.max(1, qLen)),
    repetitionPenalty,
    informationGain,
    userEngagement,
  }
}

// [DELETED] FTRL-Proximal — 被 P5h AdaGrad 统一优化器替换

interface QualityWeights {
  bias: number
  weights: Record<string, number>
  learningRate: number
  trainingExamples: number
  gradientSquaredSum: Record<string, number>  // AdaGrad per-feature state
  // Legacy fields（保留用于 JSON 兼容加载，不再写入）
  adamM?: Record<string, number>
  adamV?: Record<string, number>
  adamT?: number
  ftrl?: Record<string, any>
  hardExamples: Array<{ question: string; answer: string; target: number; loss: number }>
}

// Initial weights mirror the previous hardcoded heuristic values
let qw: QualityWeights = {
  bias: -0.225,  // sigmoid(-0.225)≈0.444 → score≈5.0 baseline (no features active)
  weights: {
    mediumLength: 0.5, longLength: 0.5, tooLong: -1.0, tooShort: -1.5,
    hasReasoning: 1.0, hasCode: 0.5, hasList: 0.3, hasUncertainty: 0.3,
    hasRefusal: -1.5, relevance: 1.5, aiExposure: -2.0, lengthRatio: 0,
    repetitionPenalty: -1.5, informationGain: 0.5, userEngagement: 0.5,
  },
  learningRate: 0.1,
  trainingExamples: 0,
  gradientSquaredSum: {},
  hardExamples: [],
}

export function loadQualityWeights() {
  qw = loadJson<QualityWeights>(WEIGHTS_PATH, qw)
  if (!qw.gradientSquaredSum) qw.gradientSquaredSum = {}
  if (!qw.adamM) qw.adamM = {}
  if (!qw.adamV) qw.adamV = {}
  if (!qw.adamT) qw.adamT = 0
  if (!qw.ftrl) qw.ftrl = {}
  if (!qw.hardExamples) qw.hardExamples = []
  // Ensure new feature weights exist
  for (const key of FEATURE_KEYS) {
    if (qw.weights[key] === undefined) qw.weights[key] = 0
  }
  console.log(`[cc-soul][quality] loaded weights: ${qw.trainingExamples} training examples`)
}

// ── Eval state (lazy-loaded: DATA_DIR may not exist at module load time) ──

export let evalMetrics: EvalMetrics = {
  totalResponses: 0, avgQuality: 5.0, correctionRate: 0,
  brainHitRate: 0, memoryRecallRate: 0, lastEval: 0,
}
let evalLoaded = false

function ensureEvalLoaded() {
  if (evalLoaded) return
  evalLoaded = true
  evalMetrics = loadJson<EvalMetrics>(EVAL_PATH, evalMetrics)
}

let qualitySum = 0
let qualityCount = 0
let memRecalls = 0
let memMisses = 0

// ── Tracking ──

export function trackQuality(score: number) {
  qualitySum += score
  qualityCount++
}

export function trackMemoryRecall(found: boolean) {
  if (found) memRecalls++; else memMisses++
}

// ── Scoring ──

export function scoreResponse(question: string, answer: string, userId = 'default'): number {
  const features = extractFeatures(question, answer, userId)

  let logit = qw.bias
  for (const key of FEATURE_KEYS) {
    logit += (qw.weights[key] || 0) * features[key]
  }

  // Map to 1-10 scale via sigmoid
  const sigmoid = 1 / (1 + Math.exp(-logit))
  const score = sigmoid * 9 + 1

  return Math.round(score * 10) / 10
}

/**
 * Update quality weights from user feedback via online SGD.
 * correction → target low score, positive → target high score.
 */
/**
 * P5h: engagement 信号驱动的质量权重更新
 * 除了 positive/correction 二值反馈，还接受 P1a 的 engagement 分数
 */
export function updateQualityFromEngagement(question: string, answer: string, engagementRate: number, userId = 'default') {
  const features = extractFeatures(question, answer, userId)
  const target = engagementRate  // 0-1 连续值
  let logit = qw.bias
  for (const key of FEATURE_KEYS) logit += (qw.weights[key] || 0) * features[key]
  const predicted = 1 / (1 + Math.exp(-logit))
  const error = predicted - target

  if (!qw.gradientSquaredSum) qw.gradientSquaredSum = {}
  const adaEps = 1e-8
  qw.gradientSquaredSum['_bias'] = (qw.gradientSquaredSum['_bias'] || 0) + error * error
  qw.bias -= (qw.learningRate * 0.5) / Math.sqrt(qw.gradientSquaredSum['_bias'] + adaEps) * error  // 0.5× lr for engagement (noisier signal)
  for (const key of FEATURE_KEYS) {
    const grad = error * features[key]
    qw.gradientSquaredSum[key] = (qw.gradientSquaredSum[key] || 0) + grad * grad
    qw.weights[key] = Math.max(-5, Math.min(5, (qw.weights[key] || 0) - (qw.learningRate * 0.5) / Math.sqrt(qw.gradientSquaredSum[key] + adaEps) * grad))
  }
  debouncedSave(WEIGHTS_PATH, qw)
}

export function updateQualityWeights(question: string, answer: string, feedback: 'positive' | 'correction', userId = 'default') {
  const features = extractFeatures(question, answer, userId)
  const target = feedback === 'positive' ? 0.9 : 0.2

  let logit = qw.bias
  for (const key of FEATURE_KEYS) {
    logit += (qw.weights[key] || 0) * features[key]
  }
  const predicted = 1 / (1 + Math.exp(-logit))
  const error = predicted - target
  const loss = Math.abs(error)

  // Record hard examples (high loss) for periodic resampling
  if (loss > 0.3) {
    if (!qw.hardExamples) qw.hardExamples = []
    qw.hardExamples.push({ question: question.slice(0, 200), answer: answer.slice(0, 500), target, loss })
    if (qw.hardExamples.length > 30) {
      // Keep highest loss examples
      qw.hardExamples.sort((a, b) => b.loss - a.loss)
      qw.hardExamples = qw.hardExamples.slice(0, 30)
    }
  }

  // P5h: AdaGrad 统一优化器（替换 FTRL+AdaGrad+HardExample 三合一）
  // 简单、稳定、per-feature adaptive learning rate
  if (!qw.gradientSquaredSum) qw.gradientSquaredSum = {}
  const adaEps = 1e-8

  // Bias update
  qw.gradientSquaredSum['_bias'] = (qw.gradientSquaredSum['_bias'] || 0) + error * error
  const biasLR = qw.learningRate / Math.sqrt(qw.gradientSquaredSum['_bias'] + adaEps)
  qw.bias -= biasLR * error

  // Per-weight AdaGrad update
  for (const key of FEATURE_KEYS) {
    const grad = error * features[key]
    qw.gradientSquaredSum[key] = (qw.gradientSquaredSum[key] || 0) + grad * grad
    const lr = qw.learningRate / Math.sqrt(qw.gradientSquaredSum[key] + adaEps)
    qw.weights[key] = (qw.weights[key] || 0) - lr * grad
    // Clamp weights to [-5, 5]
    qw.weights[key] = Math.max(-5, Math.min(5, qw.weights[key]))
  }

  qw.trainingExamples++
  debouncedSave(WEIGHTS_PATH, qw)
  console.log(`[cc-soul][quality] weights updated (${feedback}): ${qw.trainingExamples} examples, bias=${qw.bias.toFixed(3)}`)
}

/**
 * Periodically replay hard examples to reinforce learning on difficult cases.
 * Called from heartbeat.
 */
/**
 * P5h: resampleHardExamples 用 AdaGrad 统一优化器替换 FTRL
 */
export function resampleHardExamples() {
  if (!qw.hardExamples || qw.hardExamples.length < 3) return
  if (!qw.gradientSquaredSum) qw.gradientSquaredSum = {}

  const samples = qw.hardExamples.slice(0, 3)
  const adaEps = 1e-8

  for (const { question, answer, target } of samples) {
    const features = extractFeatures(question, answer)
    let logit = qw.bias
    for (const key of FEATURE_KEYS) logit += (qw.weights[key] || 0) * features[key]
    const predicted = 1 / (1 + Math.exp(-logit))
    const error = predicted - target

    // AdaGrad（0.5× lr for replay = conservative）
    const replayLR = qw.learningRate * 0.5
    qw.gradientSquaredSum['_bias'] = (qw.gradientSquaredSum['_bias'] || 0) + error * error
    qw.bias -= replayLR / Math.sqrt(qw.gradientSquaredSum['_bias'] + adaEps) * error

    for (const key of FEATURE_KEYS) {
      const grad = error * features[key]
      qw.gradientSquaredSum[key] = (qw.gradientSquaredSum[key] || 0) + grad * grad
      qw.weights[key] = Math.max(-5, Math.min(5, (qw.weights[key] || 0) - replayLR / Math.sqrt(qw.gradientSquaredSum[key] + adaEps) * grad))
    }
  }

  debouncedSave(WEIGHTS_PATH, qw)
  console.log(`[cc-soul][quality] replayed ${samples.length} hard examples (AdaGrad)`)
}

// ── Self-check (sync fallback) ──

export function selfCheckSync(question: string, answer: string): string | null {
  if (answer.length < 5) return '回答太短，可能没有实质内容'
  if (answer.length > 5000 && question.length < 30) return '回答过长，短问题不需要长篇大论'
  if (answer.includes('作为一个AI') || answer.includes('作为语言模型')) return '暴露了AI身份，违反人设'
  return null
}

// ── Self-check (CLI-powered async) ──

function logIssue(issue: string, context: string) {
  console.log(`[cc-soul][quality] ${issue} | ctx: ${context.slice(0, 80)}`)
}

export function selfCheckWithCLI(question: string, answer: string) {
  if (answer.length < 20 || question.length < 5) return

  const prompt = `问题: "${question.slice(0, 200)}"\n回答: "${answer.slice(0, 500)}"\n\n评价这个回答: 1.是否回答了问题 2.有没有编造 3.是否啰嗦 4.打分1-10。JSON格式: {"score":N,"issues":["问题"]}`

  spawnCLI(prompt, (output) => {
    try {
      const result = extractJSON(output)
      if (result) {
        const score = result.score || 5
        trackQuality(score)
        if (result.issues?.length) {
          for (const issue of result.issues) {
            logIssue(issue, question)
          }
          body.anomaly = Math.min(1.0, body.anomaly + 0.1)
        }
        // Low CLI score = trigger alertness
        if (score <= 4) {
          body.alertness = Math.min(1.0, body.alertness + 0.15)
          console.log(`[cc-soul][quality] CLI self-check low score: ${score}/10`)
        }
      }
    } catch (e: any) { console.error(`[cc-soul][quality] parse error: ${e.message}`) }
  })
}

// ── Eval ──

export function computeEval(totalMessages: number, corrections: number, resetWindow = false): EvalMetrics {
  ensureEvalLoaded()
  evalMetrics = {
    totalResponses: totalMessages,
    avgQuality: qualityCount > 0 ? Math.round(qualitySum / qualityCount * 10) / 10 : 5.0,
    correctionRate: totalMessages > 0 ? Math.round(corrections / totalMessages * 1000) / 10 : 0,
    brainHitRate: 0,
    memoryRecallRate: (memRecalls + memMisses) > 0
      ? Math.round(memRecalls / (memRecalls + memMisses) * 100) : 0,
    lastEval: Date.now(),
  }
  debouncedSave(EVAL_PATH, evalMetrics)

  // Only reset window counters when explicitly requested (e.g. heartbeat/session end)
  if (resetWindow) {
    qualitySum = 0
    qualityCount = 0
    memRecalls = 0
    memMisses = 0
  }

  return evalMetrics
}

export function getEvalSummary(totalMessages: number, corrections: number): string {
  ensureEvalLoaded()
  const e = computeEval(totalMessages, corrections)
  return `评分:${e.avgQuality}/10 纠正率:${e.correctionRate}% 记忆召回:${e.memoryRecallRate}%`
}

export const qualityModule: SoulModule = {
  id: 'quality',
  name: '质量评估',
  dependencies: ['body'],
  priority: 60,
  init() { loadQualityWeights() },
}
