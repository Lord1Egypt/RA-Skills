/**
 * semantic-drift.ts — Semantic Drift Detector（语义漂移检测器）
 *
 * cc-soul 原创算法。零 LLM 兴趣漂移检测。
 *
 * 解决的问题：
 *   用户兴趣会随时间变化（换工作、新恋情、季节性兴趣）
 *   静态权重无法适应这种变化
 *   向量系统只能看到"当前查询 vs 历史内容"的相似度，看不到兴趣趋势
 *
 * 算法：
 *   1. 每条消息提取话题词，累积到 7 天和 30 天两个滑动窗口
 *   2. 用 Jensen-Shannon 散度比较两个窗口的分布差异
 *   3. JSD > 阈值 → 检测到漂移 → 输出漂移方向（哪些话题在上升/下降）
 *   4. 上升话题 → boost recall weight；下降话题 → 不惩罚但不再主动推送
 */

import type { Memory } from './types.ts'
import { tokenize } from './memory-utils.ts'
import { isKnownWord } from './aam.ts'
import { DATA_DIR, debouncedSave } from './persistence.ts'
import { resolve } from 'path'
import { existsSync, readFileSync } from 'fs'

// ── Types ──

interface TopicDistribution {
  [topic: string]: number  // normalized frequency, sums to 1
}

interface DriftSignal {
  jsd: number              // Jensen-Shannon divergence (0=identical, 1=completely different)
  rising: string[]         // topics gaining interest
  falling: string[]        // topics losing interest
  stable: string[]         // core interests (always present)
  driftLevel: 'none' | 'mild' | 'moderate' | 'significant'
}

interface WindowEntry {
  topic: string
  ts: number
}

// Internal state
interface DriftState {
  shortWindow: WindowEntry[]  // 7-day
  longWindow: WindowEntry[]   // 30-day
  lastJSD: number
  lastCheck: number
}

// ── Constants ──

const SHORT_WINDOW_MS = 7 * 86_400_000   // 7 days
const LONG_WINDOW_MS = 30 * 86_400_000   // 30 days
const CHECK_INTERVAL_MS = 3_600_000       // persist every hour
const MIN_SHORT_SAMPLES = 10
const MIN_LONG_SAMPLES = 20
const SHORT_CAP = 500                     // max entries in short window (disk)
const LONG_CAP = 2000                     // max entries in long window (disk)

// Drift thresholds (JSD is bounded [0, 1])
const THRESH_MILD = 0.05
const THRESH_MODERATE = 0.15
const THRESH_SIGNIFICANT = 0.3

// Topic classification thresholds
const RISING_RATIO = 2.0                  // short/long > 2x → rising
const FALLING_RATIO = 0.3                 // short/long < 0.3x → falling
const FALLING_MIN_LONG_FREQ = 0.02        // only flag falling if it was meaningful in long window
const STABLE_MIN_FREQ = 0.01              // present in both windows above this threshold
const MAX_TOPICS_PER_CATEGORY = 10

// ── State ──

const STATE_FILE = resolve(DATA_DIR, 'semantic_drift.json')
let _state: DriftState = { shortWindow: [], longWindow: [], lastJSD: 0, lastCheck: 0 }

// Cache: avoid recomputing signal on every call within same second
let _cachedSignal: DriftSignal | null = null
let _cacheTs = 0
const CACHE_TTL_MS = 60_000  // 1 minute

// ── Public API ──

/**
 * Feed a message into the drift detector.
 * Called on every user message.
 */
export function trackMessage(msg: string, ts?: number): void {
  const now = ts || Date.now()

  // Extract meaningful topic words (filter noise via AAM vocabulary)
  const tokens = tokenize(msg)
  const topics = tokens.filter(t => t.length >= 2 && isKnownWord(t))

  if (topics.length === 0) return

  for (const topic of topics) {
    _state.shortWindow.push({ topic, ts: now })
    _state.longWindow.push({ topic, ts: now })
  }

  // Prune expired entries
  _state.shortWindow = _state.shortWindow.filter(e => now - e.ts < SHORT_WINDOW_MS)
  _state.longWindow = _state.longWindow.filter(e => now - e.ts < LONG_WINDOW_MS)

  // Invalidate cache
  _cachedSignal = null

  // Periodic save (not every message — debounced + hourly gate)
  if (now - _state.lastCheck > CHECK_INTERVAL_MS) {
    _state.lastCheck = now
    saveDriftState()
  }
}

/**
 * Compute current drift signal.
 * Returns null if insufficient data in either window.
 */
export function getDriftSignal(): DriftSignal | null {
  const now = Date.now()
  if (_cachedSignal && now - _cacheTs < CACHE_TTL_MS) return _cachedSignal

  if (_state.shortWindow.length < MIN_SHORT_SAMPLES ||
      _state.longWindow.length < MIN_LONG_SAMPLES) {
    return null
  }

  const shortDist = buildDistribution(_state.shortWindow.map(e => e.topic))
  const longDist = buildDistribution(_state.longWindow.map(e => e.topic))

  const jsd = jensenShannonDivergence(shortDist, longDist)
  _state.lastJSD = jsd

  // Classify topics by comparing short-term vs long-term frequency
  const rising: string[] = []
  const falling: string[] = []
  const stable: string[] = []

  const allTopics = new Set([...Object.keys(shortDist), ...Object.keys(longDist)])
  for (const topic of allTopics) {
    const sf = shortDist[topic] || 0
    const lf = longDist[topic] || 0

    // Ratio of short-term to long-term frequency
    // Guard: if long-term freq is negligible, any short-term presence is "new"
    const ratio = lf > 0.001 ? sf / lf : (sf > 0 ? 10 : 0)

    if (ratio > RISING_RATIO) {
      rising.push(topic)
    } else if (ratio < FALLING_RATIO && lf > FALLING_MIN_LONG_FREQ) {
      falling.push(topic)
    } else if (sf > STABLE_MIN_FREQ && lf > STABLE_MIN_FREQ) {
      stable.push(topic)
    }
  }

  // Sort by magnitude of frequency in the relevant window
  rising.sort((a, b) => (shortDist[b] || 0) - (shortDist[a] || 0))
  falling.sort((a, b) => (longDist[b] || 0) - (longDist[a] || 0))
  stable.sort((a, b) => {
    // Stable topics sorted by combined frequency
    const aSum = (shortDist[a] || 0) + (longDist[a] || 0)
    const bSum = (shortDist[b] || 0) + (longDist[b] || 0)
    return bSum - aSum
  })

  let driftLevel: DriftSignal['driftLevel'] = 'none'
  if (jsd > THRESH_SIGNIFICANT) driftLevel = 'significant'
  else if (jsd > THRESH_MODERATE) driftLevel = 'moderate'
  else if (jsd > THRESH_MILD) driftLevel = 'mild'

  const signal: DriftSignal = {
    jsd,
    rising: rising.slice(0, MAX_TOPICS_PER_CATEGORY),
    falling: falling.slice(0, MAX_TOPICS_PER_CATEGORY),
    stable: stable.slice(0, MAX_TOPICS_PER_CATEGORY),
    driftLevel,
  }

  _cachedSignal = signal
  _cacheTs = now
  return signal
}

/**
 * Get recall weight modifier for a given topic.
 *
 * Rising topics get a boost, falling topics get a slight reduction,
 * stable (core) topics get a tiny boost.
 *
 * Returns a multiplier in range [0.8, 1.3].
 */
export function getTopicRecallModifier(topic: string): number {
  const signal = getDriftSignal()
  if (!signal || signal.driftLevel === 'none') return 1.0

  const t = topic.toLowerCase()
  if (signal.rising.includes(t)) return 1.0 + Math.min(0.3, signal.jsd)
  if (signal.falling.includes(t)) return 1.0 - Math.min(0.2, signal.jsd * 0.5)
  if (signal.stable.includes(t)) return 1.05
  return 1.0
}

/**
 * Get a compact summary string for prompt injection or logging.
 */
export function getDriftSummary(): string {
  const signal = getDriftSignal()
  if (!signal) return ''
  if (signal.driftLevel === 'none') return ''

  const parts: string[] = [`drift=${signal.driftLevel}(${signal.jsd.toFixed(3)})`]
  if (signal.rising.length) parts.push(`↑${signal.rising.slice(0, 5).join(',')}`)
  if (signal.falling.length) parts.push(`↓${signal.falling.slice(0, 5).join(',')}`)
  return parts.join(' ')
}

// ── Internal: Distribution & Divergence ──

/**
 * Build a normalized probability distribution from a list of topics.
 * Each topic's probability = count / total.
 */
function buildDistribution(topics: string[]): TopicDistribution {
  const counts: Record<string, number> = {}
  for (const t of topics) counts[t] = (counts[t] || 0) + 1
  const total = topics.length
  if (total === 0) return {}
  const dist: TopicDistribution = {}
  for (const [k, v] of Object.entries(counts)) dist[k] = v / total
  return dist
}

/**
 * Jensen-Shannon Divergence — symmetric, bounded [0, 1] when using log base 2.
 *
 * JSD(P, Q) = 0.5 * KL(P || M) + 0.5 * KL(Q || M)
 * where M = 0.5 * (P + Q)
 *
 * Properties:
 *   - Symmetric: JSD(P,Q) = JSD(Q,P)
 *   - Bounded: 0 ≤ JSD ≤ 1 (with log₂)
 *   - JSD = 0 iff P = Q
 *   - The square root of JSD is a true metric (satisfies triangle inequality)
 *
 * Unlike raw KL divergence, JSD is always defined (no division by zero)
 * because M is guaranteed to be > 0 wherever P or Q is > 0.
 */
function jensenShannonDivergence(p: TopicDistribution, q: TopicDistribution): number {
  const allKeys = new Set([...Object.keys(p), ...Object.keys(q)])
  if (allKeys.size === 0) return 0

  // Build midpoint distribution M = 0.5 * (P + Q)
  const m: TopicDistribution = {}
  for (const k of allKeys) {
    m[k] = 0.5 * ((p[k] || 0) + (q[k] || 0))
  }

  let klPM = 0
  let klQM = 0

  for (const k of allKeys) {
    const pk = p[k] || 0
    const qk = q[k] || 0
    const mk = m[k]!  // guaranteed > 0 since at least one of pk/qk > 0

    // KL(P || M) contribution: p(x) * log2(p(x) / m(x))
    // Skip when p(x) = 0 because 0 * log(0/m) = 0 by convention
    if (pk > 0) klPM += pk * Math.log2(pk / mk)

    // KL(Q || M) contribution
    if (qk > 0) klQM += qk * Math.log2(qk / mk)
  }

  // Clamp to [0, 1] to handle floating-point rounding artifacts
  return Math.max(0, Math.min(1, 0.5 * klPM + 0.5 * klQM))
}

// ── Internal: Persistence ──

function saveDriftState(): void {
  try {
    debouncedSave(STATE_FILE, {
      shortWindow: _state.shortWindow.slice(-SHORT_CAP),
      longWindow: _state.longWindow.slice(-LONG_CAP),
      lastJSD: _state.lastJSD,
      lastCheck: _state.lastCheck,
    })
  } catch { /* non-critical — will rebuild from messages */ }
}

function loadDriftState(): void {
  try {
    if (existsSync(STATE_FILE)) {
      const raw = readFileSync(STATE_FILE, 'utf-8')
      const data = JSON.parse(raw)
      if (data && Array.isArray(data.shortWindow) && Array.isArray(data.longWindow)) {
        _state = {
          shortWindow: data.shortWindow,
          longWindow: data.longWindow,
          lastJSD: data.lastJSD || 0,
          lastCheck: data.lastCheck || 0,
        }
      }
    }
  } catch { /* first run or corrupt file — start fresh */ }
}

// Auto-load persisted state on module init
loadDriftState()
