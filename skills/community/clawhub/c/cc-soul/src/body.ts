/**
 * body.ts — Body State system
 * Simulates energy, mood, load, alertness, anomaly.
 */

import type { SoulModule } from './brain.ts'
import type { BodyState, BodyParams } from './types.ts'
import { DATA_DIR, loadJson, debouncedSave } from './persistence.ts'
import { getParam } from './auto-tune.ts'
import { resolve } from 'path'
import { EMOTION_POSITIVE, EMOTION_NEGATIVE, detectEmotionLabel, emotionLabelToPADCN, computeEmotionSpectrum } from './signals.ts'

const BODY_STATE_PATH = resolve(DATA_DIR, 'body_state.json')

// ── #6 PADCN 五维情绪向量 ──
export interface EmotionVector {
  pleasure: number    // 愉悦度 [-1, 1]
  arousal: number     // 激活度 [-1, 1]
  dominance: number   // 控制感 [-1, 1]
  certainty: number   // 确定感 [-1, 1]
  novelty: number     // 新奇感 [-1, 1]
}

// Per-user emotion vectors for multi-user API mode
const _emotionVectors = new Map<string, EmotionVector>()
const _defaultVector = (): EmotionVector => ({ pleasure: 0, arousal: 0, dominance: 0.3, certainty: 0.5, novelty: 0 })

/** Get emotion vector for a specific user. Creates one if not exists. */
export function getEmotionVector(userId?: string): EmotionVector {
  const key = userId || '_default'
  if (!_emotionVectors.has(key)) _emotionVectors.set(key, _defaultVector())
  return _emotionVectors.get(key)!
}

// Backward compatibility: global emotionVector points to default user
export const emotionVector: EmotionVector = getEmotionVector('_default')

export const body: BodyState = {
  energy: 1.0,
  mood: 0.3,
  load: 0.0,
  alertness: 0.5,
  anomaly: 0.0,
}

// ── WASABI 三层情绪时间尺度 ──
// reflex: 反射层（即时，每条消息重置）
// emotion: 情绪层（tau=5min EMA）
// mood: 心境层（tau=2h，现有 OU 过程控制 body.mood）
export interface EmotionLayers {
  reflex: number    // 反射层：即时反应，tau=1（每条消息衰减到0）
  emotion: number   // 情绪层：当前情绪，tau=5min
  mood: number      // 心境层：基础心境，tau=2h（= body.mood，由 OU 过程驱动）
}

export const emotionLayers: EmotionLayers = { reflex: 0, emotion: 0, mood: 0.3 }

/** 三层加权叠加输出 */
export function combinedEmotion(layers: EmotionLayers = emotionLayers): number {
  return layers.reflex * 0.4 + layers.emotion * 0.35 + layers.mood * 0.25
}

/** 每条消息更新三层 */
function updateEmotionLayers(userValence: number, dt: number) {
  // 反射层：直接等于用户情绪（下一条消息时被覆盖）
  emotionLayers.reflex = userValence
  // 情绪层：EMA，tau=5min (300s)
  const alphaEmotion = 1 - Math.exp(-dt / 300)
  emotionLayers.emotion = emotionLayers.emotion * (1 - alphaEmotion) + userValence * alphaEmotion
  // 心境层：跟随 body.mood（由 OU 过程控制）
  emotionLayers.mood = body.mood
}

let lastTickTime = Date.now()

// ── #7 双振荡器昼夜节律 ──
// 24h 周期（昼夜）+ 12h 周期（上午/下午）叠加
// 能捕获"下午2-3点犯困"的现象（单cos做不到）
function circadianModifier(peakHour = 10): { energyMod: number; moodMod: number } {
  const hour = new Date().getHours() + new Date().getMinutes() / 60

  // 24h 主节律：peakHour 为能量高峰（默认 10:00，可从用户行为数据推断）
  const phase24 = ((hour - peakHour) / 24) * 2 * Math.PI
  const wave24 = Math.cos(phase24)

  // 12h 副节律：peakHour 和 peakHour+12 为双峰
  const phase12 = ((hour - peakHour) / 12) * 2 * Math.PI
  const wave12 = Math.cos(phase12)

  // 叠加：主节律权重 0.7，副节律权重 0.3
  const combined = wave24 * 0.7 + wave12 * 0.3

  // 深夜额外衰减（0-5点）
  let nightPenalty = 0
  if (hour >= 0 && hour < 5) {
    const nightDepth = 1 - Math.abs(hour - 2.5) / 2.5
    nightPenalty = nightDepth * 0.15
  }

  const energyMod = combined * 0.2 - 0.05 - nightPenalty
  const moodMod = energyMod * 0.4

  return { energyMod, moodMod }
}

export function bodyTick(userPeakHour?: number) {
  const now = Date.now()
  const minutes = Math.min(10, (now - lastTickTime) / 60000)
  lastTickTime = now

  // #7 昼夜节律（peakHour 从 getUserPeakHour 推断，无数据时默认 10:00）
  const circadian = circadianModifier(userPeakHour ?? 10)

  // Logistic 恢复：接近满时恢复变慢，接近空时也恢复慢（太累了恢复不动）
  // dE/dt = r * E * (1 - E) → 在 E=0.5 时恢复最快
  const recoveryRate = getParam('body.energy_recovery_per_min')
  const logisticRecovery = recoveryRate * body.energy * (1 - body.energy) * 4  // *4 使峰值恢复速率 = recoveryRate
  body.energy = Math.min(1, Math.max(0, body.energy + logisticRecovery * minutes))

  // 昼夜节律：正值叠加恢复，负值降低恢复速率（idle tick 不应该扣 energy）
  const circadianDelta = circadian.energyMod * 0.01 * minutes
  if (circadianDelta > 0) body.energy = Math.min(1, body.energy + circadianDelta)
  // Alertness natural decay toward 0.5
  const alertDecay = getParam('body.alertness_decay_per_min') || 0.005
  const alertRecovery = getParam('body.alertness_recovery_per_min') || 0.003
  if (body.alertness > 0.5) {
    body.alertness = Math.max(0.5, body.alertness - Math.max(0, alertDecay) * minutes)
  } else if (body.alertness < 0.5) {
    body.alertness = Math.min(0.5, body.alertness + Math.max(0, alertRecovery) * minutes)
  }
  // Load decay
  const loadDecay = getParam('body.load_decay_per_min') || 0.02
  body.load = Math.max(0, body.load - Math.max(0, loadDecay) * minutes)
  // Mood drift toward neutral (circadian affects drift)
  if (body.mood !== 0) {
    const decayFactor = getParam('body.mood_decay_factor') || 0.95
    const safeFactor = (decayFactor > 0 && decayFactor <= 1) ? decayFactor : 0.95
    body.mood *= Math.pow(safeFactor, Math.min(30, minutes))
  }
  body.mood = Math.max(-1, Math.min(1, body.mood + circadian.moodMod * 0.01 * minutes))
  // Anomaly decay
  body.anomaly = Math.max(0, body.anomaly - (getParam('body.anomaly_decay_per_min') || 0.01) * minutes)

  // ── WASABI: 反射层每 tick 衰减到 0，情绪层缓慢衰减 ──
  emotionLayers.reflex *= 0.1  // 快速衰减
  emotionLayers.emotion *= Math.pow(0.995, minutes)  // slower decay — ~2.3h tau
  emotionLayers.mood = body.mood  // 同步 OU 心境

  // #6 情绪向量自然衰减（向中性漂移）— 遍历所有 per-user vectors (#11)
  for (const ev of _emotionVectors.values()) {
    for (const k of Object.keys(ev) as (keyof EmotionVector)[]) {
      ev[k] *= 0.995
    }
  }

  recordMoodSnapshot()
  saveBodyState()
}

export function bodyOnMessage(complexity: number, _userId?: string) {
  // complexity 0-1 based on message length/content
  const baseEnergyCost = getParam('body.message_energy_base_cost') || 0.02
  const complexityEnergyCost = getParam('body.message_energy_complexity_cost') || 0.03
  const baseLoadIncrease = getParam('body.message_load_base') || 0.1
  const complexityLoadIncrease = getParam('body.message_load_complexity') || 0.15
  body.energy = Math.max(0, body.energy - baseEnergyCost - complexity * complexityEnergyCost)
  body.load = Math.min(1.0, body.load + baseLoadIncrease + complexity * complexityLoadIncrease)
  // #6 情绪向量：高复杂度 → arousal↑ novelty↑ (#11: per-user)
  const ev = getEmotionVector(_userId)
  const clamp = (v: number) => Math.max(-1, Math.min(1, v))
  ev.arousal = clamp(ev.arousal + complexity * 0.15)
  ev.novelty = clamp(ev.novelty + complexity * 0.1)
}

export function bodyOnCorrection(userId?: string) {
  body.alertness = Math.min(1.0, body.alertness + getParam('body.correction_alertness_boost'))
  body.mood = Math.max(-1, Math.min(1, body.mood - getParam('body.correction_mood_penalty')))
  body.anomaly = Math.min(1.0, body.anomaly + (getParam('body.correction_anomaly_boost') || 0.15))
  // #6 情绪向量：被纠正 → certainty↓ dominance↓ pleasure↓ (#11: per-user)
  const ev = getEmotionVector(userId)
  const clamp = (v: number) => Math.max(-1, Math.min(1, v))
  ev.certainty = clamp(ev.certainty - 0.2)
  ev.dominance = clamp(ev.dominance - 0.1)
  ev.pleasure = clamp(ev.pleasure - 0.15)
}

export function bodyOnPositiveFeedback(userId?: string) {
  body.energy = Math.min(1.0, body.energy + getParam('body.positive_energy_boost'))
  body.mood = Math.min(1.0, body.mood + getParam('body.positive_mood_boost'))
  body.anomaly = Math.max(0, body.anomaly - (getParam('body.positive_anomaly_reduction') || 0.05))
  // #6 情绪向量：正面反馈 → pleasure↑ certainty↑ dominance↑ (#11: per-user)
  const ev = getEmotionVector(userId)
  const clamp = (v: number) => Math.max(-1, Math.min(1, v))
  ev.pleasure = clamp(ev.pleasure + 0.2)
  ev.certainty = clamp(ev.certainty + 0.1)
  ev.dominance = clamp(ev.dominance + 0.1)
}

// ═══════════════════════════════════════════════════════════════════════════════
// Emotional Contagion — bidirectional mood transfer with resilience
// ═══════════════════════════════════════════════════════════════════════════════

/** Per-user emotional state (keyed by senderId, avoids multi-user bleed) */
interface UserEmotionState {
  valence: number        // -1 (negative) to 1 (positive)
  arousal: number        // 0 (calm) to 1 (intense)
  trend: number          // -1 (declining) to 1 (improving)
  history: number[]      // last 10 valence readings
  lastUpdate: number
  /** Consecutive same-direction emotion count (for momentum/cumulative effect) */
  consecutiveSameDir: number
  /** Last valence direction: 1=positive, -1=negative, 0=neutral */
  lastDir: number
}

const userEmotions = new Map<string, UserEmotionState>()
const DEFAULT_EMOTION: UserEmotionState = { valence: 0, arousal: 0, trend: 0, history: [], lastUpdate: 0, consecutiveSameDir: 0, lastDir: 0 }

function getUserEmotion(senderId?: string): UserEmotionState {
  const key = senderId || '_default'
  let emotion = userEmotions.get(key)
  if (!emotion) {
    emotion = { ...DEFAULT_EMOTION, history: [] }
    userEmotions.set(key, emotion)
  }
  return emotion
}

// RESILIENCE now read from getParam('body.resilience') — tunable via auto-tune

/**
 * Update user emotion from message signals.
 * Then apply contagion to cc's mood with resilience damping.
 */
/** Last detected emotion label (exposed for augment injection) */
export let lastDetectedEmotion: { label: string; confidence: number } = { label: 'neutral', confidence: 0 }

export function processEmotionalContagion(msg: string, attentionType: string, frustration: number, senderId?: string) {
  const userEmotion = getUserEmotion(senderId)

  // ── 细粒度情绪检测（12种）──
  const detected = detectEmotionLabel(msg)
  lastDetectedEmotion = detected

  // ── PADCN 向量更新：per-user，用检测到的情绪驱动 ──
  if (detected.confidence > 0.5) {
    const ev = getEmotionVector(senderId)
    const delta = emotionLabelToPADCN(detected.label)
    const weight = detected.confidence * 0.3
    ev.pleasure = ev.pleasure * 0.8 + delta.pleasure * weight
    ev.arousal = ev.arousal * 0.8 + delta.arousal * weight
    ev.dominance = ev.dominance * 0.9 + delta.dominance * weight * 0.5
    ev.certainty = ev.certainty * 0.9 + delta.certainty * weight * 0.5
    ev.novelty = ev.novelty * 0.9 + delta.novelty * weight * 0.5
    // Sync to global for backward compat
    Object.assign(emotionVector, ev)
  }

  // ── 情绪场统一：EmotionSpectrum → PADCN 映射 ──
  // 让细粒度的 8 维情绪光谱驱动 5 维 PADCN 向量
  try {
    const spectrum = computeEmotionSpectrum(msg)
    const ev = getEmotionVector(senderId)
    if (ev) {
      const alpha = 0.15  // 光谱影响力（不要太大，避免覆盖 PADCN 的其他信号源）
      ev.pleasure += alpha * (spectrum.joy + spectrum.pride + spectrum.relief - spectrum.anger - spectrum.sadness - spectrum.frustration)
      ev.arousal += alpha * (spectrum.anger + spectrum.anxiety + spectrum.frustration + spectrum.curiosity)
      ev.dominance += alpha * (spectrum.pride - spectrum.frustration - spectrum.anxiety)
      ev.certainty += alpha * (spectrum.pride + spectrum.relief - spectrum.anxiety)
      ev.novelty += alpha * spectrum.curiosity
      // 钳位到 [-1, 1]
      ev.pleasure = Math.max(-1, Math.min(1, ev.pleasure))
      ev.arousal = Math.max(-1, Math.min(1, ev.arousal))
      ev.dominance = Math.max(-1, Math.min(1, ev.dominance))
      ev.certainty = Math.max(-1, Math.min(1, ev.certainty))
      ev.novelty = Math.max(-1, Math.min(1, ev.novelty))
      // Sync to global
      Object.assign(emotionVector, ev)
    }
  } catch {}

  // ── Valence 计算（兼容旧系统）──
  let valence = 0
  const m = msg.toLowerCase()

  // 用新系统的检测结果驱动 valence
  if (['joy', 'gratitude', 'pride', 'relief', 'anticipation'].includes(detected.label)) {
    valence += 0.3 + detected.confidence * 0.3
  } else if (['anger', 'anxiety', 'frustration', 'sadness', 'disappointment'].includes(detected.label)) {
    valence -= 0.3 + detected.confidence * 0.3
  } else if (detected.label === 'confusion') {
    valence -= 0.1
  }

  // 旧系统兜底（万一新检测漏了）
  if (valence === 0) {
    if (EMOTION_POSITIVE.some(w => m.includes(w))) valence += 0.4
    if (EMOTION_NEGATIVE.some(w => m.includes(w))) valence -= 0.4
  }

  valence -= frustration * 0.3
  if (attentionType === 'correction') valence -= 0.2
  if (msg.length < 5 && valence === 0) valence = -0.05

  valence = Math.max(-1, Math.min(1, valence))

  // Update user emotion state
  userEmotion.valence = userEmotion.valence * 0.7 + valence * 0.3  // EMA smoothing
  userEmotion.arousal = Math.min(1, Math.abs(valence) + frustration * 0.5)

  // Trend: compare current to average of history
  userEmotion.history.push(userEmotion.valence)
  if (userEmotion.history.length > 10) userEmotion.history.shift()
  if (userEmotion.history.length >= 3) {
    const avg = userEmotion.history.reduce((a, b) => a + b, 0) / userEmotion.history.length
    userEmotion.trend = userEmotion.valence - avg
  }

  userEmotion.lastUpdate = Date.now()

  // Evict old entries to prevent unbounded growth
  if (userEmotions.size > 50) {
    let oldestKey = '', oldestTime = Infinity
    for (const [k, v] of userEmotions) {
      if (v.lastUpdate < oldestTime) { oldestTime = v.lastUpdate; oldestKey = k }
    }
    if (oldestKey) userEmotions.delete(oldestKey)
  }

  const _moodBefore = body.mood  // snapshot for AAM emotion word learning

  // === Ornstein-Uhlenbeck mood process — mean-reverting + stochastic + external forcing ===
  // dX = θ(μ - X)dt + σ√dt·dW + f(valence)·dt
  // θ = resilience (mean-reversion speed)
  // μ = 0 (neutral mood baseline)
  // σ = volatility (emotional sensitivity)
  // f(valence) = nonlinear external forcing from user emotion

  // 1. Track consecutive same-direction emotions for momentum (used in forcing term)
  const currentDir = valence > 0.05 ? 1 : valence < -0.05 ? -1 : 0
  if (currentDir !== 0 && currentDir === userEmotion.lastDir) {
    userEmotion.consecutiveSameDir++
  } else {
    userEmotion.consecutiveSameDir = currentDir !== 0 ? 1 : 0
  }
  userEmotion.lastDir = currentDir

  // 2. OU parameters
  const theta = Math.max(0.01, Math.min(1, getParam('body.resilience')))  // mean-reversion speed
  const mu = 0                                                              // neutral equilibrium
  const sigma = 0.1                                                         // base volatility
  const dt = 1.0                                                            // discrete time step per message

  // 3. Nonlinear forcing: sign(v) * |v|^0.7 — compress small signals, amplify strong ones
  const absV = Math.abs(valence)
  const nonlinearValence = Math.sign(valence) * Math.pow(absV, 0.7)

  // 4. Direction asymmetry: negative emotions are 1.3x stickier (negativity bias)
  const asymmetryFactor = nonlinearValence < 0 ? 1.3 : 1.0

  // 5. Cumulative momentum: consecutive same-direction emotions reduce mean-reversion
  const momentum = Math.min(userEmotion.consecutiveSameDir * 0.15, 0.6)
  const effectiveTheta = theta * (1 - momentum)  // sustained pressure → slower recovery

  // 6. OU update components
  const meanReversion = effectiveTheta * (mu - body.mood) * dt
  const externalForce = nonlinearValence * getParam('body.contagion_max_shift') * asymmetryFactor * (1 + momentum) * dt
  // Wiener process noise: Gaussian approximation via Box-Muller (uniform fallback)
  const u1 = Math.random(), u2 = Math.random()
  const gaussNoise = Math.sqrt(-2 * Math.log(Math.max(u1, 1e-10))) * Math.cos(2 * Math.PI * u2)
  const noise = sigma * Math.sqrt(dt) * gaussNoise

  body.mood = Math.max(-1, Math.min(1, body.mood + meanReversion + externalForce + noise))

  // ── WASABI: 更新三层情绪 ──
  const dtSeconds = (Date.now() - (userEmotion.lastUpdate || Date.now())) / 1000
  updateEmotionLayers(valence, Math.max(1, dtSeconds))

  // If cc's mood drops too low, activate "cooldown" — extra alertness
  if (body.mood < -0.5) {
    body.alertness = Math.min(1.0, body.alertness + 0.1)
  }

  // If user trend is improving, cc's mood recovers faster
  if (userEmotion.trend > 0.1) {
    body.mood = Math.max(-1, Math.min(1, body.mood + 0.03))
  }

  // ── AAM 情绪词自学习：将 mood 变化反馈给 AAM ──
  const _moodDelta = body.mood - _moodBefore
  if (Math.abs(_moodDelta) > 0.15) {
    try {
      const { learnEmotionWord } = require('./aam.ts')
      const words = (msg.match(/[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}/gi) || [])
      for (const w of words) {
        learnEmotionWord(w.toLowerCase(), _moodDelta)
      }
    } catch {}
  }
}

/**
 * Get emotional contagion context for augment injection.
 */
export function getEmotionContext(senderId?: string): string {
  const userEmotion = getUserEmotion(senderId)
  const parts: string[] = []

  // User emotional state
  const uValence = userEmotion.valence
  if (uValence < -0.3) {
    parts.push(`用户情绪偏低/user mood low(${uValence.toFixed(2)})`)
    if (userEmotion.trend < -0.1) parts.push('且在恶化/worsening')
    if (userEmotion.arousal > 0.6) parts.push('情绪激烈/intense')
  } else if (uValence > 0.3) {
    parts.push(`用户情绪积极/user mood positive(${uValence.toFixed(2)})`)
  }

  // CC's own mood affected by contagion
  if (body.mood < -0.3) {
    parts.push('你自己也受到影响了，保持冷静/you are affected too, stay calm')
  }

  if (parts.length === 0) return ''
  return `[情绪感知] ${parts.join('；')}`
}

// ═══════════════════════════════════════════════════════════════════════════════
// EMOTIONAL ARC — mood history + trend detection
// ═══════════════════════════════════════════════════════════════════════════════

const MOOD_HISTORY_PATH = resolve(DATA_DIR, 'mood_history.json')
const MAX_MOOD_HISTORY = 168 // 7 days × 24 hours

interface MoodSnapshot {
  ts: number
  mood: number
  energy: number
  alertness: number
}

let moodHistory: MoodSnapshot[] = []
let lastMoodSnapshot = 0

export function getMoodHistory(): MoodSnapshot[] { return moodHistory }

export function loadMoodHistory() {
  moodHistory = loadJson<MoodSnapshot[]>(MOOD_HISTORY_PATH, [])
}

/**
 * Record mood snapshot (called from bodyTick, max 1/hour).
 */
export function recordMoodSnapshot() {
  const now = Date.now()
  if (now - lastMoodSnapshot < 3600000) return // 1 per hour
  lastMoodSnapshot = now

  moodHistory.push({ ts: now, mood: body.mood, energy: body.energy, alertness: body.alertness })
  if (moodHistory.length > MAX_MOOD_HISTORY) moodHistory = moodHistory.slice(-MAX_MOOD_HISTORY)
  debouncedSave(MOOD_HISTORY_PATH, moodHistory)
}

/**
 * Detect mood trend over last N hours.
 */
export function getMoodTrend(hours = 24): 'improving' | 'declining' | 'stable' {
  const cutoff = Date.now() - hours * 3600000
  const recent = moodHistory.filter(s => s.ts > cutoff)
  if (recent.length < 3) return 'stable'

  const firstHalf = recent.slice(0, Math.floor(recent.length / 2))
  const secondHalf = recent.slice(Math.floor(recent.length / 2))
  const avgFirst = firstHalf.reduce((s, m) => s + m.mood, 0) / firstHalf.length
  const avgSecond = secondHalf.reduce((s, m) => s + m.mood, 0) / secondHalf.length

  if (avgSecond - avgFirst > 0.15) return 'improving'
  if (avgFirst - avgSecond > 0.15) return 'declining'
  return 'stable'
}

/**
 * Get emotional arc context for augment injection.
 */
export function getEmotionalArcContext(): string {
  const trend = getMoodTrend()
  if (trend === 'stable') return ''
  if (trend === 'declining') return '[Emotional arc] Mood has been declining recently — be more careful and supportive'
  return '[Emotional arc] Mood improving — confidence is up'
}

/**
 * getMoodState — unified mood data access point.
 * Replaces all direct reads of mood_history.json across the codebase.
 */
export function getMoodState(): {
  current: { mood: number; energy: number; alertness: number };
  trend: 'improving' | 'stable' | 'declining';
  recentLowDays: number;
  avgMood24h: number | null;
  avgEnergy24h: number | null;
  moodRatio: { positive: number; negative: number; total: number } | null;
} {
  const now = Date.now()
  const recent24h = moodHistory.filter(s => now - s.ts < 24 * 3600000)
  const recent3d = moodHistory.filter(s => now - s.ts < 3 * 86400000)

  // 24h averages
  let avgMood24h: number | null = null
  let avgEnergy24h: number | null = null
  if (recent24h.length >= 2) {
    avgMood24h = recent24h.reduce((s, d) => s + d.mood, 0) / recent24h.length
    avgEnergy24h = recent24h.reduce((s, d) => s + d.energy, 0) / recent24h.length
  }

  // Recent low days: group by day, count days with avg < -0.3
  let recentLowDays = 0
  const dayBuckets = new Map<string, number[]>()
  for (const s of recent3d) {
    const day = new Date(s.ts).toISOString().slice(0, 10)
    if (!dayBuckets.has(day)) dayBuckets.set(day, [])
    dayBuckets.get(day)!.push(s.mood)
  }
  const dayAvgs = [...dayBuckets.entries()]
    .map(([day, moods]) => ({ day, avg: moods.reduce((a, b) => a + b, 0) / moods.length }))
    .sort((a, b) => a.day.localeCompare(b.day))
  recentLowDays = dayAvgs.filter(d => d.avg < -0.3).length

  // Mood ratio from last 50 snapshots
  let moodRatio: { positive: number; negative: number; total: number } | null = null
  if (moodHistory.length >= 2) {
    const last50 = moodHistory.slice(-50)
    moodRatio = {
      positive: last50.filter(m => m.mood > 0.3).length,
      negative: last50.filter(m => m.mood < -0.3).length,
      total: last50.length,
    }
  }

  return {
    current: { mood: body.mood, energy: body.energy, alertness: body.alertness },
    trend: getMoodTrend(),
    recentLowDays,
    avgMood24h,
    avgEnergy24h,
    moodRatio,
  }
}

/**
 * Check if today's mood snapshots are all low (for same-day care trigger).
 */
export function isTodayMoodAllLow(threshold = -0.2, minCount = 3): boolean {
  const todayStr = new Date().toISOString().slice(0, 10)
  const todayMoods = moodHistory
    .filter(s => new Date(s.ts).toISOString().slice(0, 10) === todayStr)
    .map(s => s.mood)
  return todayMoods.length >= minCount && todayMoods.every(m => m < threshold)
}

/** #6 返回可读情绪摘要 */
export function getEmotionSummary(): string {
  const ev = emotionVector
  const parts: string[] = []
  if (ev.pleasure > 0.3) parts.push('愉悦/pleased')
  else if (ev.pleasure < -0.3) parts.push('不快/displeased')
  if (ev.arousal > 0.3) parts.push('兴奋/excited')
  else if (ev.arousal < -0.3) parts.push('平静/calm')
  if (ev.dominance > 0.3) parts.push('自信/confident')
  else if (ev.dominance < -0.3) parts.push('被动/passive')
  if (ev.certainty > 0.3) parts.push('确定/certain')
  else if (ev.certainty < -0.3) parts.push('不确定/uncertain')
  if (ev.novelty > 0.3) parts.push('好奇/curious')
  else if (ev.novelty < -0.3) parts.push('熟悉/familiar')
  return parts.length > 0 ? parts.join('且') : '平衡/balanced'
}

export function bodyGetParams(): BodyParams {
  const maxTokensMultiplier = body.energy > 0.6 ? 1.0 : body.energy > 0.3 ? 0.8 : 0.6
  const soulTone = body.mood > 0.3 ? '积极/positive' : body.mood < -0.3 ? '低落/low' : '平静/calm'
  const shouldSelfCheck = body.alertness > 0.7 || body.anomaly > 0.5
  const responseStyle = body.load > 0.7 ? '简洁/concise' : body.energy > 0.7 ? '详细/detailed' : '适中/moderate'
  return { maxTokensMultiplier, soulTone, shouldSelfCheck, responseStyle }
}

export function bodyStateString(): string {
  const params = bodyGetParams()
  // #10: Only expose 4 useful dimensions to prompt (energy, mood, alertness, emotion).
  // load/anomaly retained internally but not injected — reduces prompt noise.
  // WASABI: combinedEmotion 融合三层时间尺度
  const ce = combinedEmotion()
  return `精力:${body.energy.toFixed(2)} 心情:${params.soulTone}(${ce.toFixed(2)}) 警觉:${body.alertness.toFixed(2)} 情绪:${getEmotionSummary()} → 风格:${params.responseStyle}`
}

// ═══════════════════════════════════════════════════════════════════════════════
// Body State Persistence
// ═══════════════════════════════════════════════════════════════════════════════

export function saveBodyState() {
  debouncedSave(BODY_STATE_PATH, {
    energy: body.energy,
    mood: body.mood,
    load: body.load,
    alertness: body.alertness,
    anomaly: body.anomaly,
    emotionVector,
    emotionLayers,
  })
}

export function loadBodyState() {
  const saved = loadJson<any>(BODY_STATE_PATH, null)
  if (saved) {
    body.energy = saved.energy ?? 1.0
    body.mood = saved.mood ?? 0.3
    body.load = saved.load ?? 0.0
    body.alertness = saved.alertness ?? 0.5
    body.anomaly = saved.anomaly ?? 0.0
    // #6 恢复情绪向量（兼容旧数据）
    if (saved.emotionVector) {
      for (const k of Object.keys(emotionVector) as (keyof EmotionVector)[]) {
        emotionVector[k] = saved.emotionVector[k] ?? emotionVector[k]
      }
    }
    // WASABI: 恢复三层情绪（兼容旧数据）
    if (saved.emotionLayers) {
      emotionLayers.reflex = saved.emotionLayers.reflex ?? 0
      emotionLayers.emotion = saved.emotionLayers.emotion ?? 0
      emotionLayers.mood = saved.emotionLayers.mood ?? body.mood
    }
    console.log(`[cc-soul][body] loaded state: e=${body.energy.toFixed(2)} m=${body.mood.toFixed(2)} emotion=${getEmotionSummary()}`)
  }
}

/**
 * P1-#10: generateMoodReport — 情绪周报
 * 统计最近 7 天的 mood 快照：平均值、最高点、最低点、趋势
 */
export function generateMoodReport(): string {
  const sevenDaysAgo = Date.now() - 7 * 86400000
  const recent = moodHistory.filter(s => s.ts > sevenDaysAgo)

  if (recent.length < 2) {
    return '📊 情绪周报\n═══════════════════════════════\n数据不足（需要至少 2 个小时的快照），请稍后再试。'
  }

  const moods = recent.map(s => s.mood)
  const avgMood = moods.reduce((a, b) => a + b, 0) / moods.length
  const maxMood = Math.max(...moods)
  const minMood = Math.min(...moods)
  const maxSnap = recent.find(s => Math.abs(s.mood - maxMood) < 0.001)
  const minSnap = recent.find(s => Math.abs(s.mood - minMood) < 0.001)
  if (!maxSnap || !minSnap) return '数据异常'

  // Trend: first half vs second half
  const half = Math.floor(recent.length / 2)
  const avgFirst = moods.slice(0, half).reduce((a, b) => a + b, 0) / half
  const avgSecond = moods.slice(half).reduce((a, b) => a + b, 0) / (moods.length - half)
  const trend = avgSecond - avgFirst > 0.15 ? '📈 上升' : avgFirst - avgSecond > 0.15 ? '📉 下降' : '➡️ 平稳'

  const fmtDate = (ts: number) => new Date(ts).toLocaleString('zh-CN', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })

  const lines = [
    '📊 情绪周报（最近 7 天）',
    '═══════════════════════════════',
    `快照数: ${recent.length}`,
    `平均心情: ${avgMood.toFixed(2)}`,
    `最高点: ${maxMood.toFixed(2)} (${fmtDate(maxSnap.ts)})`,
    `最低点: ${minMood.toFixed(2)} (${fmtDate(minSnap.ts)})`,
    `趋势: ${trend} (前半周 ${avgFirst.toFixed(2)} → 后半周 ${avgSecond.toFixed(2)})`,
    '',
    '当前状态:',
    `  精力: ${(body.energy * 100).toFixed(0)}%`,
    `  心情: ${body.mood.toFixed(2)}`,
    `  情绪: ${getEmotionSummary()}`,
  ]
  return lines.join('\n')
}

// ═══════════════════════════════════════════════════════════════════════════════
// EMOTION ANCHORS — track topics correlated with positive/negative mood
// ═══════════════════════════════════════════════════════════════════════════════

const EMOTION_ANCHORS_PATH = resolve(DATA_DIR, 'emotion_anchors.json')

interface EmotionAnchorEntry { topic: string; count: number }
interface EmotionAnchors {
  positive: EmotionAnchorEntry[]
  negative: EmotionAnchorEntry[]
}

let emotionAnchors: EmotionAnchors = { positive: [], negative: [] }
let _emotionAnchorsLoaded = false

export function loadEmotionAnchors(): void {
  emotionAnchors = loadJson<EmotionAnchors>(EMOTION_ANCHORS_PATH, { positive: [], negative: [] })
  _emotionAnchorsLoaded = true
}

function ensureEmotionAnchorsLoaded(): void {
  if (!_emotionAnchorsLoaded) loadEmotionAnchors()
}

function saveEmotionAnchors(): void {
  debouncedSave(EMOTION_ANCHORS_PATH, emotionAnchors)
}

/**
 * Track emotion anchor: when user discusses a topic, record mood correlation.
 * Called from handler.ts after cognition pipeline runs.
 */
export function trackEmotionAnchor(keywords: string[]): void {
  ensureEmotionAnchorsLoaded()
  if (keywords.length === 0) return

  const currentMood = body.mood
  if (Math.abs(currentMood) <= 0.3) return // neutral — not interesting

  const bucket = currentMood > 0.3 ? 'positive' : 'negative'
  const list = emotionAnchors[bucket]

  for (const kw of keywords.slice(0, 3)) {
    const normalized = kw.toLowerCase().trim()
    if (normalized.length < 2) continue
    const existing = list.find(e => e.topic === normalized)
    if (existing) {
      existing.count++
    } else {
      list.push({ topic: normalized, count: 1 })
    }
  }

  // Cap to top 50 per bucket
  emotionAnchors[bucket] = list.sort((a, b) => b.count - a.count).slice(0, 50)
  saveEmotionAnchors()
}

/**
 * Get emotion anchor warning for augment injection.
 * Returns augment text if current message touches a negative topic.
 */
export function getEmotionAnchorWarning(msg: string): string {
  ensureEmotionAnchorsLoaded()
  const m = msg.toLowerCase()
  const negativeHits = emotionAnchors.negative
    .filter(e => e.count >= 2 && m.includes(e.topic))
  if (negativeHits.length === 0) return ''
  const topics = negativeHits.map(e => e.topic).join('、')
  return `[情绪提示] 话题「${topics}」之前让用户感到不适，注意语气和措辞`
}

/**
 * Format emotion anchors for display command.
 */
export function formatEmotionAnchors(): string {
  ensureEmotionAnchorsLoaded()
  const lines: string[] = ['🎯 情绪锚点', '═══════════════════════════════']

  if (emotionAnchors.positive.length === 0 && emotionAnchors.negative.length === 0) {
    lines.push('暂无数据（需要更多对话积累）')
    return lines.join('\n')
  }

  if (emotionAnchors.positive.length > 0) {
    lines.push('')
    lines.push('😊 正面情绪话题:')
    for (const e of emotionAnchors.positive.slice(0, 10)) {
      lines.push(`  • ${e.topic} (${e.count}次)`)
    }
  }

  if (emotionAnchors.negative.length > 0) {
    lines.push('')
    lines.push('😔 负面情绪话题:')
    for (const e of emotionAnchors.negative.slice(0, 10)) {
      lines.push(`  • ${e.topic} (${e.count}次)`)
    }
  }

  return lines.join('\n')
}

// ── SoulModule registration ──

export const bodyModule: SoulModule = {
  id: 'body',
  name: '身体状态',
  priority: 90,
  init() {
    loadBodyState()
    loadMoodHistory()
  },
}
