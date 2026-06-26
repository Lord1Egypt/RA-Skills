/**
 * absence-detection.ts — 用户离开检测与回归欢迎
 *
 * 独立模块，跟踪用户离开时长，在用户回归时注入个性化欢迎 augment。
 * - 心跳周期：扫描所有用户 lastSeen，标记长时间离开
 * - Augment 注入：用户回来时生成欢迎回来提示
 * - 数据持久化：data/absence_detection.json
 */

import type { SoulModule } from './brain.ts'
import type { Augment } from './types.ts'
import { resolve } from 'path'
import { DATA_DIR, loadJson, debouncedSave } from './persistence.ts'
import { getProfile } from './user-profiles.ts'
import { estimateTokens } from './prompt-builder.ts'
import { memoryState, ensureMemoriesLoaded } from './memory.ts'

// ═══════════════════════════════════════════════════════════════════════════════
// DATA TYPES
// ═══════════════════════════════════════════════════════════════════════════════

interface AbsenceRecord {
  /** Last time user was seen active (ms timestamp) */
  lastSeen: number
  /** Whether user is currently considered absent */
  isAbsent: boolean
  /** When absence was first detected (ms timestamp), 0 if not absent */
  absentSince: number
  /** Whether we already showed welcome-back for this absence period */
  welcomeShown: boolean
  /** Total absence periods tracked (historical count) */
  totalAbsences: number
  /** Average absence duration in ms (EMA) */
  avgAbsenceDuration: number
}

type AbsenceState = Record<string, AbsenceRecord>

/** Topic absence entry — a topic the user used to discuss but stopped */
interface TopicAbsenceEntry {
  topic: string
  avgPerWeek: number
  lastSeenWeeksAgo: number
  detectedAt: number
}

interface TopicAbsenceData {
  entries: TopicAbsenceEntry[]
  lastRunDate: string
}

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTS
// ═══════════════════════════════════════════════════════════════════════════════

const ABSENCE_PATH = resolve(DATA_DIR, 'absence_detection.json')
const TOPIC_ABSENCE_PATH = resolve(DATA_DIR, 'topic_absence.json')
const DAY_MS = 86400_000
const WEEK_MS = 7 * DAY_MS

const TOPIC_STOP_WORDS = new Set([
  '的', '了', '是', '在', '我', '你', '他', '她', '它', '们', '这', '那', '有', '和',
  '不', '也', '就', '都', '会', '到', '说', '要', '去', '能', '把', '让', '被', '从',
  '上', '下', '中', '大', '小', '很', '好', '吗', '呢', '啊', '吧', '嗯', '哦',
  '什么', '怎么', '为什么', '可以', '知道', '觉得', '一个', '没有', '因为', '所以',
  '还是', '但是', '如果', '这个', '那个', '一下', '已经', '现在', '时候', '应该',
  'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
  'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'my', 'your',
  'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
  'that', 'this', 'do', 'did', 'have', 'has', 'had', 'not', 'no',
  'what', 'how', 'why', 'can', 'will', 'just', 'like', 'know', 'think',
])

/** Threshold to consider a user "absent" — 4 hours */
const ABSENCE_THRESHOLD_MS = 4 * 60 * 60 * 1000

/** Threshold for "long absence" — 3 days */
const LONG_ABSENCE_MS = 3 * 24 * 60 * 60 * 1000

/** Threshold for "very long absence" — 7 days */
const VERY_LONG_ABSENCE_MS = 7 * 24 * 60 * 60 * 1000

// ═══════════════════════════════════════════════════════════════════════════════
// PERSONALIZED ABSENCE THRESHOLD
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * 个性化缺席阈值：基于用户历史活跃模式动态计算
 * 每天发 50 条的用户，4 小时不回就不正常
 * 每周发 5 条的用户，3 天不回很正常
 */
function personalizedAbsenceThreshold(userId: string): { short: number; long: number; veryLong: number } {
  // 找到这个用户的活跃记录
  const record = state[userId]
  const avgGapMs = record?.avgAbsenceDuration || 14400000  // 默认 4h

  // 基于平均间隔计算阈值（倍数关系）
  return {
    short: Math.max(3600000, avgGapMs * 1.5),      // 1.5 倍平均间隔（至少 1h）
    long: Math.max(86400000, avgGapMs * 8),          // 8 倍（至少 1 天）
    veryLong: Math.max(259200000, avgGapMs * 24),    // 24 倍（至少 3 天）
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// STATE
// ═══════════════════════════════════════════════════════════════════════════════

let state: AbsenceState = {}

export function loadAbsenceState() {
  state = loadJson<AbsenceState>(ABSENCE_PATH, {})
}

function save() {
  debouncedSave(ABSENCE_PATH, state)
}

function getRecord(userId: string): AbsenceRecord {
  if (!state[userId]) {
    state[userId] = {
      lastSeen: 0,
      isAbsent: false,
      absentSince: 0,
      welcomeShown: false,
      totalAbsences: 0,
      avgAbsenceDuration: 0,
    }
  }
  return state[userId]
}

// ═══════════════════════════════════════════════════════════════════════════════
// HEARTBEAT — called during heartbeat cycle to scan for absent users
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Scan all tracked users and mark those who haven't been seen
 * for longer than ABSENCE_THRESHOLD_MS as absent.
 * Called by handler-heartbeat.ts during the heartbeat cycle.
 */
export function heartbeatScanAbsence(): void {
  const now = Date.now()
  let changed = false

  for (const [userId, record] of Object.entries(state)) {
    if (record.lastSeen <= 0) continue

    const silenceDuration = now - record.lastSeen

    const thresholds = personalizedAbsenceThreshold(userId)
    if (!record.isAbsent && silenceDuration > thresholds.short) {
      // User just became absent
      record.isAbsent = true
      record.absentSince = record.lastSeen
      record.welcomeShown = false
      changed = true
    }
  }

  if (changed) save()

  // Also run topic absence scan (max once per day)
  scanTopicAbsences()
}

// ═══════════════════════════════════════════════════════════════════════════════
// TOPIC ABSENCE SCAN — detect topics user stopped mentioning
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Scan memories from last 90 days. Build topic frequency map.
 * Find topics that appeared 3+ times in weeks 2-8 but 0 times in last 2 weeks.
 * Runs max once per day (dedup by date in persisted state).
 */
function scanTopicAbsences(): void {
  const today = new Date().toISOString().slice(0, 10)
  const existing = loadJson<TopicAbsenceData>(TOPIC_ABSENCE_PATH, { entries: [], lastRunDate: '' })
  if (existing.lastRunDate === today) return // already ran today

  const now = Date.now()
  const cutoff90d = now - 90 * DAY_MS
  const cutoff2w = now - 2 * WEEK_MS
  const cutoff8w = now - 8 * WEEK_MS

  ensureMemoriesLoaded()
  const memories = memoryState.memories.filter(m => m.ts >= cutoff90d)
  if (memories.length < 10) {
    debouncedSave(TOPIC_ABSENCE_PATH, { entries: [], lastRunDate: today })
    return
  }

  // Build topic -> timestamps map
  const topicTimestamps: Record<string, number[]> = {}

  for (const mem of memories) {
    const cjkWords = mem.content.match(/[\u4e00-\u9fff]{2,6}/g) || []
    const enWords = (mem.content.match(/[a-zA-Z]{3,}/g) || []).map(w => w.toLowerCase())
    const words = [...cjkWords, ...enWords].filter(w => !TOPIC_STOP_WORDS.has(w))
    const seen = new Set<string>()
    for (const w of words) {
      if (seen.has(w)) continue
      seen.add(w)
      if (!topicTimestamps[w]) topicTimestamps[w] = []
      topicTimestamps[w].push(mem.ts)
    }
  }

  // Find topics: 3+ occurrences in weeks 2-8, 0 in last 2 weeks
  const absences: TopicAbsenceEntry[] = []
  for (const [topic, timestamps] of Object.entries(topicTimestamps)) {
    const recentCount = timestamps.filter(t => t >= cutoff2w).length
    if (recentCount > 0) continue

    const olderCount = timestamps.filter(t => t >= cutoff8w && t < cutoff2w).length
    if (olderCount < 3) continue

    const weekSpan = Math.max(1, (cutoff2w - cutoff8w) / WEEK_MS)
    const avgPerWeek = Math.round(olderCount / weekSpan * 10) / 10
    const lastTs = Math.max(...timestamps)
    const lastSeenWeeksAgo = Math.round((now - lastTs) / WEEK_MS * 10) / 10

    absences.push({ topic, avgPerWeek, lastSeenWeeksAgo, detectedAt: now })
  }

  // Sort by frequency, keep max 5
  absences.sort((a, b) => b.avgPerWeek - a.avgPerWeek)
  const result: TopicAbsenceData = {
    entries: absences.slice(0, 5),
    lastRunDate: today,
  }
  debouncedSave(TOPIC_ABSENCE_PATH, result)
  if (result.entries.length > 0) {
    console.log(`[cc-soul][absence] detected ${result.entries.length} absent topics: ${result.entries.map(e => e.topic).join(', ')}`)
  }
}

/**
 * Get a topic absence hint augment.
 * Returns an Augment for topics the user stopped mentioning, or null.
 * Max 1 per conversation turn (dedup via _topicHintInjected flag).
 */
let _topicHintInjected = false
export function getTopicAbsenceAugment(): Augment | null {
  if (_topicHintInjected) return null

  const data = loadJson<TopicAbsenceData>(TOPIC_ABSENCE_PATH, { entries: [], lastRunDate: '' })
  if (data.entries.length === 0) return null

  const e = data.entries[0]
  const content = `[缺席检测] 用户最近没再提到「${e.topic}」（之前平均每周提${e.avgPerWeek}次，已经${Math.round(e.lastSeenWeeksAgo)}周没提了）。如果自然的话可以关心一下`

  _topicHintInjected = true
  return { content, priority: 6, tokens: estimateTokens(content) }
}

/** Reset per-turn dedup flag (call at start of each turn) */
export function resetTopicAbsenceFlag() { _topicHintInjected = false }

// ═══════════════════════════════════════════════════════════════════════════════
// USER ACTIVITY — called when a user sends a message
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Record that a user is active. Call this on every incoming message.
 * Returns absence duration in ms if the user was absent, 0 otherwise.
 */
export function recordUserActivity(userId: string): number {
  if (!userId) return 0

  const record = getRecord(userId)
  const now = Date.now()
  let absenceDuration = 0

  if (record.isAbsent && record.absentSince > 0) {
    absenceDuration = now - record.absentSince

    // Update EMA of absence duration
    if (record.totalAbsences === 0) {
      record.avgAbsenceDuration = absenceDuration
    } else {
      record.avgAbsenceDuration = record.avgAbsenceDuration * 0.8 + absenceDuration * 0.2
    }
    record.totalAbsences++
  }

  record.lastSeen = now
  record.isAbsent = false
  record.absentSince = 0
  // Don't reset welcomeShown here — it's reset in heartbeatScanAbsence when re-entering absence

  save()
  return absenceDuration
}

// ═══════════════════════════════════════════════════════════════════════════════
// AUGMENT INJECTION — called during augment building
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Generate a welcome-back augment if the user was absent.
 * Called by handler-augments.ts during augment building.
 * Returns an Augment or null if no welcome is needed.
 */
export function getAbsenceAugment(userId: string): Augment | null {
  if (!userId) return null

  const record = state[userId]
  if (!record) return null
  if (!record.isAbsent) return null
  if (record.welcomeShown) return null

  const now = Date.now()
  const absenceDuration = record.absentSince > 0 ? now - record.absentSince : 0
  const thresholds = personalizedAbsenceThreshold(userId)
  if (absenceDuration < thresholds.short) return null

  // Mark welcome as shown so we don't repeat it
  record.welcomeShown = true
  save()

  // Get user profile for personalization
  const profile = getProfile(userId)
  const name = profile.displayName || '用户'

  // Build context-aware welcome hint
  let hint: string
  const daysAway = Math.floor(absenceDuration / (24 * 60 * 60 * 1000))
  const hoursAway = Math.floor(absenceDuration / (60 * 60 * 1000))

  if (absenceDuration >= thresholds.veryLong) {
    // very long absence — warm, careful welcome
    hint = `[回归检测] ${name}已经离开了${daysAway}天。请自然地表达欢迎回来，简短提及上次聊天的话题（如果记得），不要过度热情或让用户感到压力。`
  } else if (absenceDuration >= thresholds.long) {
    // long absence — friendly note
    hint = `[回归检测] ${name}有${daysAway}天没来了。可以轻松地打个招呼，提到"好久不见"即可，不要刻意列举之前的对话。`
  } else {
    // short absence — subtle acknowledgment
    hint = `[回归检测] ${name}离开了约${hoursAway}小时。如果对话自然允许，可以简短问候一下，但不要刻意提及缺席。`
  }

  // Add pattern insight if we have enough data
  if (record.totalAbsences >= 3 && record.avgAbsenceDuration > 0) {
    const avgDays = Math.round(record.avgAbsenceDuration / (24 * 60 * 60 * 1000))
    if (avgDays >= 1) {
      hint += ` (用户平均每隔${avgDays}天回来一次，这是正常节奏)`
    }
  }

  return {
    content: hint,
    priority: 7, // moderately high — greeting matters but shouldn't override core context
    tokens: estimateTokens(hint),
  }
}

/**
 * Check if a user is currently absent (for external queries).
 */
export function isUserAbsent(userId: string): boolean {
  return state[userId]?.isAbsent ?? false
}

/**
 * Get absence duration in ms for a user (0 if not absent).
 */
export function getAbsenceDuration(userId: string): number {
  const record = state[userId]
  if (!record?.isAbsent || !record.absentSince) return 0
  return Date.now() - record.absentSince
}

// ═══════════════════════════════════════════════════════════════════════════════
// SOUL MODULE — brain-managed lifecycle
// ═══════════════════════════════════════════════════════════════════════════════

export const absenceDetectionModule: SoulModule = {
  id: 'absence-detection',
  name: '离开检测',
  priority: 40,

  init() {
    loadAbsenceState()
  },

  onHeartbeat() {
    heartbeatScanAbsence()
  },

  onPreprocessed(event: any): Augment[] | void {
    const senderId = event?.context?.senderId
    if (!senderId) return

    // Record activity (user just sent a message)
    recordUserActivity(senderId)

    // Check if we should inject a welcome-back augment
    const augment = getAbsenceAugment(senderId)
    if (augment) return [augment]
  },
}
