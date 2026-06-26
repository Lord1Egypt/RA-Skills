/**
 * behavioral-phase-space.ts — 行为相空间（Behavioral Phase Space）
 *
 * 原创算法：统一 behavior-engine + behavior-prediction
 *
 * 用户行为是多维空间中的一条轨迹。
 * 连续维度（mood, engagement）→ 加权线性外推
 * 离散有序维度（style）→ 众数投票
 * 离散无序维度（topic）→ PPM 转移概率
 *
 * 同时保留：
 * - behavior-engine 的情景→响应模式匹配
 * - behavior-prediction 的 PPM Markov 链和 domain belief
 * - 两者共享同一个 BehavioralState 数据结构
 *
 * cc-soul 原创核心算法
 */

import { DATA_DIR, loadJson, debouncedSave } from './persistence.ts'
import { resolve } from 'path'
import { detectDomain } from './epistemic.ts'

// ═══════════════════════════════════════════════════════════════════════════════
// UNIFIED DATA STRUCTURES
// ═══════════════════════════════════════════════════════════════════════════════

export type TimeSlot = 'early_morning' | 'morning' | 'afternoon' | 'evening' | 'late_night'
type MoodBucket = 'positive' | 'negative' | 'neutral'

export interface BehavioralState {
  topic: string          // 当前话题域（离散）
  mood: number           // [-1, 1]（连续）
  engagement: number     // [0, 1]（连续）
  style: string          // 当前响应风格（离散有序）
  timeSlot: TimeSlot
  afterEvent?: string    // 'correction' | 'rapid_fire' | 'topic_switch'
  ts: number
}

interface BehaviorPattern {
  id: string
  condition: { timeSlot?: TimeSlot; topicDomain?: string; mood?: MoodBucket; afterEvent?: string; dayType?: 'weekday' | 'weekend' }
  action: { style: string; hint: string }
  hits: number; misses: number
  lastHit: number; createdAt: number
  source: 'learned' | 'seeded'
}

interface DomainBelief {
  alpha: number; beta: number; lastSeen: number
}

// PPM Trie for topic prediction
interface PPMNode {
  children: Record<string, PPMNode>
  counts: Record<string, number>
  total: number; escape: number
}

// ═══════════════════════════════════════════════════════════════════════════════
// STATE
// ═══════════════════════════════════════════════════════════════════════════════

const STATE_PATH = resolve(DATA_DIR, 'behavioral_phase_space.json')
const PATTERNS_PATH = resolve(DATA_DIR, 'behavior_patterns.json')

// Trajectory: last N behavioral states
const MAX_TRAJECTORY = 30
let trajectory: BehavioralState[] = []

// Patterns (from old behavior-engine)
let patterns: BehaviorPattern[] = (() => {
  const loaded = loadJson<BehaviorPattern[]>(PATTERNS_PATH, [])
  return Array.isArray(loaded) ? loaded : []
})()

// Domain beliefs (from old behavior-prediction)
let domainBeliefs: Record<string, DomainBelief> = {}

// PPM trie (topic prediction)
let ppmRoot: PPMNode = { children: {}, counts: {}, total: 0, escape: 0 }

// Observations buffer
interface Observation {
  state: BehavioralState
  reaction: 'satisfied' | 'corrected' | 'follow_up' | 'topic_switch' | 'neutral'
  ts: number
}
let observations: Observation[] = []

// Load saved state
try {
  const saved = loadJson<any>(STATE_PATH, {})
  if (saved.trajectory) trajectory = saved.trajectory
  if (saved.domainBeliefs) domainBeliefs = saved.domainBeliefs
  if (saved.ppmRoot) ppmRoot = saved.ppmRoot
  if (saved.observations) observations = saved.observations
} catch {}

function save() {
  debouncedSave(STATE_PATH, { trajectory, domainBeliefs, ppmRoot, observations: observations.slice(-100) }, 5000)
}

// ═══════════════════════════════════════════════════════════════════════════════
// SITUATION DETECTION (unified from behavior-engine)
// ═══════════════════════════════════════════════════════════════════════════════

export function getTimeSlot(): TimeSlot {
  const h = new Date().getHours()
  if (h >= 0 && h < 6) return 'late_night'
  if (h >= 6 && h < 9) return 'early_morning'
  if (h >= 9 && h < 12) return 'morning'
  if (h >= 12 && h < 18) return 'afternoon'
  if (h >= 18 && h < 23) return 'evening'
  return 'late_night'
}

function getMoodBucket(mood: number): MoodBucket {
  if (mood > 0.3) return 'positive'
  if (mood < -0.3) return 'negative'
  return 'neutral'
}

function detectTopicDomain(msg: string): string {
  // Prioritize epistemic domain detection
  try { const d = detectDomain(msg); if (d && d !== 'general' && d !== '通用') return d } catch {}
  const m = msg.toLowerCase()
  if (/python|\.py|pip|django|flask/.test(m)) return 'python'
  if (/javascript|node|react|vue|typescript/.test(m)) return 'javascript'
  if (/swift|ios|xcode/.test(m)) return 'ios'
  if (/docker|k8s|deploy|nginx/.test(m)) return 'devops'
  if (/面试|简历|跳槽|工作|职场|老板/.test(m)) return 'career'
  if (/代码|函数|编程|bug|算法/.test(m)) return 'tech'
  return 'general'
}

// ═══════════════════════════════════════════════════════════════════════════════
// TRAJECTORY MANAGEMENT
// ═══════════════════════════════════════════════════════════════════════════════

/** Record current behavioral state into trajectory */
export function recordState(userMsg: string, mood: number, session?: any): BehavioralState {
  const state: BehavioralState = {
    topic: detectTopicDomain(userMsg),
    mood,
    engagement: estimateEngagement(userMsg, session),
    style: 'balanced',
    timeSlot: getTimeSlot(),
    afterEvent: session?._pendingCorrectionVerify ? 'correction' : session?.turnCount >= 3 ? 'rapid_fire' : undefined,
    ts: Date.now(),
  }
  trajectory.push(state)
  if (trajectory.length > MAX_TRAJECTORY) trajectory = trajectory.slice(-MAX_TRAJECTORY)

  // Update domain beliefs (from old behavior-prediction)
  updateDomainBelief(state.topic)

  save()
  return state
}

function estimateEngagement(msg: string, session?: any): number {
  let e = 0.5
  if (msg.length > 100) e += 0.2   // long message = engaged
  if (msg.length < 10) e -= 0.2    // short = disengaged
  if (/？|\?/.test(msg)) e += 0.1  // questions = engaged
  if (session?.turnCount > 5) e += 0.1  // staying = engaged
  return Math.max(0, Math.min(1, e))
}

// ═══════════════════════════════════════════════════════════════════════════════
// TRAJECTORY PROJECTION — predict next state
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * 核心原创算法：从轨迹预测下一个状态
 * 连续维度 → 加权线性外推
 * 离散有序维度 → 众数投票
 * 离散无序维度 → PPM 转移概率
 */
export function predictNext(): {
  topic: { predicted: string; confidence: number }
  style: { predicted: string; confidence: number }
  engagement: { predicted: number; confidence: number }
  mood: { predicted: number; confidence: number }
} {
  const recent = trajectory.slice(-5)
  if (recent.length < 2) {
    return {
      topic: { predicted: 'general', confidence: 0 },
      style: { predicted: 'balanced', confidence: 0 },
      engagement: { predicted: 0.5, confidence: 0 },
      mood: { predicted: 0, confidence: 0 },
    }
  }

  // 连续维度：加权线性外推（最近 3 点，权重 0.5/0.3/0.2）
  const weights = [0.5, 0.3, 0.2]
  const lastN = recent.slice(-3)

  const predictContinuous = (getValue: (s: BehavioralState) => number): { predicted: number; confidence: number } => {
    if (lastN.length < 2) return { predicted: getValue(lastN[0]), confidence: 0.3 }
    let weightedSum = 0, totalWeight = 0
    for (let i = 0; i < lastN.length; i++) {
      const w = weights[i] ?? 0.1
      weightedSum += getValue(lastN[i]) * w
      totalWeight += w
    }
    const predicted = weightedSum / totalWeight
    // 置信度 = 1 - 方差（值越稳定越自信）
    const values = lastN.map(getValue)
    const mean = values.reduce((s, v) => s + v, 0) / values.length
    const variance = values.reduce((s, v) => s + (v - mean) ** 2, 0) / values.length
    const confidence = Math.max(0.1, Math.min(0.9, 1 - variance * 4))
    return { predicted, confidence }
  }

  // style：众数投票（离散有序）
  const styleCounts = new Map<string, number>()
  for (const s of lastN) {
    styleCounts.set(s.style, (styleCounts.get(s.style) ?? 0) + 1)
  }
  let bestStyle = 'balanced', bestStyleCount = 0
  for (const [style, count] of styleCounts) {
    if (count > bestStyleCount) { bestStyle = style; bestStyleCount = count }
  }

  // topic：PPM 转移概率（离散无序）
  const topicPrediction = ppmPredict(recent.map(s => s.topic))

  return {
    topic: topicPrediction ?? { predicted: recent[recent.length - 1].topic, confidence: 0.3 },
    style: { predicted: bestStyle, confidence: bestStyleCount / lastN.length },
    engagement: predictContinuous(s => s.engagement),
    mood: predictContinuous(s => s.mood),
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// PATTERN MATCHING (from behavior-engine, simplified)
// ═══════════════════════════════════════════════════════════════════════════════

export function getBehaviorEngineHint(userMsg: string, mood: number, session?: any): string | null {
  const state = trajectory[trajectory.length - 1] ?? recordState(userMsg, mood, session)
  const moodBucket = getMoodBucket(mood)
  const day = new Date().getDay()
  const dayType = (day === 0 || day === 6) ? 'weekend' : 'weekday'

  // Match patterns
  const matched = patterns.filter(p => {
    let score = 0
    if (p.condition.timeSlot && p.condition.timeSlot === state.timeSlot) score++
    if (p.condition.topicDomain && p.condition.topicDomain === state.topic) score++
    if (p.condition.mood && p.condition.mood === moodBucket) score++
    if (p.condition.afterEvent && p.condition.afterEvent === state.afterEvent) score++
    if (p.condition.dayType && p.condition.dayType === dayType) score++
    return score > 0
  }).filter(p => {
    const conf = (p.hits + 1) / (p.hits + p.misses + 2)
    return conf > 0.4
  }).sort((a, b) => {
    const confA = (a.hits + 1) / (a.hits + a.misses + 2)
    const confB = (b.hits + 1) / (b.hits + b.misses + 2)
    return confB - confA
  })

  if (matched.length === 0) return null
  const best = matched[0]
  const conf = (best.hits + 1) / (best.hits + best.misses + 2)
  return `[行为模式] ${best.action.hint} (${conf > 0.8 ? '高' : conf > 0.5 ? '中' : '低'}置信)`
}

// ═══════════════════════════════════════════════════════════════════════════════
// OBSERVATION & LEARNING (from behavior-engine)
// ═══════════════════════════════════════════════════════════════════════════════

export function recordObservation(userMsg: string, mood: number, session: any, reaction: string, responseStyle: string): void {
  const state = trajectory[trajectory.length - 1] ?? recordState(userMsg, mood, session)
  state.style = responseStyle
  observations.push({ state, reaction: reaction as any, ts: Date.now() })
  if (observations.length > 200) observations = observations.slice(-200)
  save()
}

export function learnFromObservations(): void {
  if (observations.length < 5) return
  const recent = observations.slice(-50)

  // Group by situation → find consistent reaction→style mappings
  const groups = new Map<string, { style: string; satisfied: number; total: number }[]>()
  for (const obs of recent) {
    const key = `${obs.state.timeSlot}|${obs.state.topic}|${getMoodBucket(obs.state.mood)}`
    if (!groups.has(key)) groups.set(key, [])
    groups.get(key)!.push({
      style: obs.state.style,
      satisfied: obs.reaction === 'satisfied' ? 1 : 0,
      total: 1,
    })
  }

  // Extract patterns from groups with 3+ observations
  for (const [key, entries] of groups) {
    if (entries.length < 3) continue
    const [timeSlot, topic, mood] = key.split('|')
    const bestStyle = entries.reduce((best, e) => e.satisfied > best.satisfied ? e : best, entries[0])
    const hits = entries.filter(e => e.satisfied > 0).length
    const misses = entries.length - hits
    if (hits / (hits + misses) < 0.4) continue

    const existing = patterns.find(p =>
      p.condition.timeSlot === timeSlot && p.condition.topicDomain === topic
    )
    if (existing) {
      existing.hits += hits
      existing.misses += misses
      existing.lastHit = Date.now()
    } else {
      patterns.push({
        id: `learned_${Date.now()}_${Math.random().toString(36).slice(2, 6)}`,
        condition: { timeSlot: timeSlot as TimeSlot, topicDomain: topic, mood: mood as MoodBucket },
        action: { style: bestStyle.style, hint: `${timeSlot}+${topic}+${mood}时用${bestStyle.style}风格` },
        hits, misses, lastHit: Date.now(), createdAt: Date.now(), source: 'learned',
      })
    }
  }

  // Prune: remove patterns with Beta confidence < 0.3 and age > 30 days
  const now = Date.now()
  patterns = patterns.filter(p => {
    const age = now - p.createdAt
    const conf = (p.hits + 1) / (p.hits + p.misses + 2)
    return age < 30 * 86400000 || conf > 0.3
  })

  debouncedSave(PATTERNS_PATH, patterns, 5000)
  save()
}

// ═══════════════════════════════════════════════════════════════════════════════
// DOMAIN BELIEF (from behavior-prediction, Beta-Bernoulli)
// ═══════════════════════════════════════════════════════════════════════════════

function updateDomainBelief(domain: string): void {
  if (!domainBeliefs[domain]) domainBeliefs[domain] = { alpha: 1, beta: 1, lastSeen: 0 }
  const b = domainBeliefs[domain]

  // Time decay: 7天衰减
  const ageDays = (Date.now() - b.lastSeen) / 86400000
  if (ageDays > 7) {
    const decay = Math.pow(0.95, ageDays / 7)
    b.alpha = Math.max(1, b.alpha * decay)
    b.beta = Math.max(1, b.beta * decay)
  }

  b.alpha++
  b.lastSeen = Date.now()

  // Update beta for non-appearing domains
  for (const [d, belief] of Object.entries(domainBeliefs)) {
    if (d !== domain) belief.beta += 0.1
  }
}

export function predictDomainProbability(domain: string): number {
  const b = domainBeliefs[domain]
  if (!b) return 0.1
  return b.alpha / (b.alpha + b.beta)
}

export function getTopPredictions(topN = 3): Array<{ domain: string; probability: number }> {
  return Object.entries(domainBeliefs)
    .map(([domain, b]) => ({ domain, probability: b.alpha / (b.alpha + b.beta) }))
    .sort((a, b) => b.probability - a.probability)
    .slice(0, topN)
}

// ═══════════════════════════════════════════════════════════════════════════════
// PPM MARKOV CHAIN + 心理状态条件（原创增强）
// 同一话题序列在不同心情下有不同转移概率
// ═══════════════════════════════════════════════════════════════════════════════

// mood 分 2 桶起步（数据够了可扩到 3 桶）
type MoodCondition = 'positive' | 'non_positive'
function getMoodCondition(mood: number): MoodCondition {
  return mood > 0.2 ? 'positive' : 'non_positive'
}

// 心理状态条件 PPM：每个 mood 桶有独立的 trie
const ppmByMood: Record<MoodCondition, PPMNode> = {
  positive: { children: {}, counts: {}, total: 0, escape: 0 },
  non_positive: { children: {}, counts: {}, total: 0, escape: 0 },
}

function ppmUpdate(context: string[], next: string, maxOrder = 3, mood?: number, weight = 1.0): void {
  // 全局 PPM（保持向后兼容）
  let node = ppmRoot
  const ctx = context.slice(-maxOrder)
  node.counts[next] = (node.counts[next] || 0) + weight
  node.total += weight
  for (const symbol of ctx) {
    if (!node.children[symbol]) node.children[symbol] = { children: {}, counts: {}, total: 0, escape: 0 }
    node = node.children[symbol]
    node.counts[next] = (node.counts[next] || 0) + weight
    node.total += weight
  }

  // 心理状态条件 PPM
  if (mood !== undefined) {
    const condition = getMoodCondition(mood)
    let moodNode = ppmByMood[condition]
    moodNode.counts[next] = (moodNode.counts[next] || 0) + weight
    moodNode.total += weight
    for (const symbol of ctx) {
      if (!moodNode.children[symbol]) moodNode.children[symbol] = { children: {}, counts: {}, total: 0, escape: 0 }
      moodNode = moodNode.children[symbol]
      moodNode.counts[next] = (moodNode.counts[next] || 0) + weight
      moodNode.total += weight
    }
  }
}

function ppmPredict(context: string[], mood?: number): { predicted: string; confidence: number } | null {
  const ctx = context.slice(-3)

  // 优先用心理状态条件 PPM（如果该桶有足够数据）
  if (mood !== undefined) {
    const condition = getMoodCondition(mood)
    const moodRoot = ppmByMood[condition]
    if (moodRoot.total >= 5) {
      const result = ppmPredictFromRoot(moodRoot, ctx)
      if (result) return result
    }
  }

  // Fallback: 全局 PPM
  return ppmPredictFromRoot(ppmRoot, ctx)
}

function ppmPredictFromRoot(root: PPMNode, ctx: string[]): { predicted: string; confidence: number } | null {
  for (let order = ctx.length; order >= 0; order--) {
    let node = root
    for (let i = ctx.length - order; i < ctx.length; i++) {
      if (!node.children[ctx[i]]) { node = root; break }
      node = node.children[ctx[i]]
    }
    if (node.total > 0) {
      let best = '', bestCount = 0
      for (const [topic, count] of Object.entries(node.counts)) {
        if (count > bestCount) { best = topic; bestCount = count }
      }
      if (best && bestCount >= 2) {
        return { predicted: best, confidence: bestCount / node.total }
      }
    }
  }
  return null
}

export function updateMarkov(topicSequence: string[], mood?: number, intentScores?: number[]): void {
  for (let i = 1; i < topicSequence.length; i++) {
    const weight = intentScores?.[i] ?? 1.0
    ppmUpdate(topicSequence.slice(0, i), topicSequence[i], 3, mood, weight)
  }
  save()
}

export function predictNextTopic(recentTopics: string[], mood?: number): { topic: string; confidence: number } | null {
  return ppmPredict(recentTopics, mood)
}

// ═══════════════════════════════════════════════════════════════════════════════
// PREDICTION AUGMENTS (compatibility with behavior-prediction API)
// ═══════════════════════════════════════════════════════════════════════════════

export function getBehaviorPrediction(userMsg: string, memories: any[]): string | null {
  const pred = predictNext()
  if (pred.topic.confidence < 0.3 && pred.mood.confidence < 0.3) return null

  const parts: string[] = []
  if (pred.topic.confidence >= 0.4) parts.push(`可能接下来聊${pred.topic.predicted}`)
  if (pred.engagement.predicted < 0.3) parts.push(`参与度在降低`)
  if (pred.mood.predicted < -0.3) parts.push(`情绪可能变差`)
  if (parts.length === 0) return null
  return `[行为预测] ${parts.join('，')}`
}

export function getTimeSlotPrediction(chatHistory: { user: string; ts: number }[]): string | null {
  const ts = getTimeSlot()
  const topDomains = getTopPredictions(2)
  if (topDomains.length === 0 || topDomains[0].probability < 0.3) return null
  return `[时段习惯] ${ts}时段，用户通常聊${topDomains.map(d => d.domain).join('/')}`
}

export function isDecisionQuestion(msg: string): boolean {
  return /该不该|要不要|选.*还是|A.*还是.*B|哪个好|怎么选|纠结/i.test(msg)
}

export function predictUserDecision(situation: string, memories: any[], userId?: string): string | null {
  // Simplified: use trajectory style prediction
  const pred = predictNext()
  if (pred.style.confidence < 0.5) return null
  return `用户倾向${pred.style.predicted}风格的建议`
}

// ═══════════════════════════════════════════════════════════════════════════════
// UNIFIED BEHAVIOR HINT — 合并 getBehaviorEngineHint + getBehaviorPrediction
// handler-augments 只需调这一个入口
// ═══════════════════════════════════════════════════════════════════════════════

export function getUnifiedBehaviorHint(userMsg: string, mood: number, session?: any, memories?: any[]): string | null {
  const parts: string[] = []

  // 1. 场景模式匹配（原 getBehaviorEngineHint）
  const engineHint = getBehaviorEngineHint(userMsg, mood, session)
  if (engineHint) {
    // 去掉 [行为模式] 标签，只取内容
    parts.push(engineHint.replace(/^\[行为模式\]\s*/, ''))
  }

  // 2. 轨迹预测（原 getBehaviorPrediction）
  const pred = predictNext()
  if (pred.topic.confidence >= 0.4) parts.push(`可能接下来聊${pred.topic.predicted}`)
  if (pred.engagement.predicted < 0.3) parts.push('参与度在降低')
  if (pred.mood.predicted < -0.3) parts.push('情绪可能变差')

  // 3. 时段习惯
  const ts = getTimeSlot()
  const topDomains = getTopPredictions(1)
  if (topDomains.length > 0 && topDomains[0].probability >= 0.5) {
    parts.push(`${ts}时段常聊${topDomains[0].domain}`)
  }

  if (parts.length === 0) return null
  return `[行为分析] ${parts.join('，')}`
}

// ═══════════════════════════════════════════════════════════════════════════════
// COMPATIBILITY EXPORTS (keep old API working)
// ═══════════════════════════════════════════════════════════════════════════════

export function checkPredictions(userMsg: string): { hitAugment: string | null } {
  const domain = detectTopicDomain(userMsg)
  const prob = predictDomainProbability(domain)
  if (prob > 0.5) {
    return { hitAugment: `[预测命中] 预测到你会聊${domain}（概率${(prob * 100).toFixed(0)}%）` }
  }
  return { hitAugment: null }
}

export function generateNewPredictions(chatHistory: { user: string }[], intentScores?: number[]): void {
  const topics = chatHistory.slice(-10).map(h => detectTopicDomain(h.user))
  updateMarkov(topics, undefined, intentScores)
}

export function updateAllDomainBeliefs(detectedDomain: string | null): void {
  if (detectedDomain) updateDomainBelief(detectedDomain)
}

// detectSituation 已内联到本模块的 recordState 中，不再从旧文件 re-export
export function getPatternCount(): number { return patterns.length }
export function getLearnedPatternCount(): number { return patterns.filter(p => p.source === 'learned').length }
export function getLearnedPatterns(): Array<{ condition: string; action: string; hits: number; misses: number; confidence: number }> {
  return patterns
    .filter(p => p.source === 'learned' && p.hits >= 3)
    .map(p => ({
      condition: [p.condition.timeSlot, p.condition.topicDomain, p.condition.mood, p.condition.afterEvent, p.condition.dayType].filter(Boolean).join('+'),
      action: p.action.style || p.action.hint,
      hits: p.hits,
      misses: p.misses,
      confidence: p.hits / Math.max(1, p.hits + p.misses),
    }))
}
