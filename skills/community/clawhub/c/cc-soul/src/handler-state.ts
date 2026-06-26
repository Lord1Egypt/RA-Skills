/**
 * handler-state.ts — 全局状态、metrics、stats、session state
 *
 * 从 handler.ts 提取的所有共享可变状态。
 * 可变 let 变量通过 getter/setter 函数导出，避免 re-export 限制。
 */

import type { InteractionStats } from './types.ts'
import { loadJson, saveJson, debouncedSave, STATS_PATH } from './persistence.ts'
import { spawnCLI } from './cli.ts'
import { innerState, getRecentJournal } from './inner-life.ts'
import { setNarrativeCache, narrativeCache } from './prompt-builder.ts'

// ── Cached regexes (avoid per-call allocation) ──
export const CJK_TOPIC_REGEX = /[\u4e00-\u9fff]{3,}/g
export const CJK_WORD_REGEX = /[\u4e00-\u9fff]{2,4}/g

// ── #14 语音朗读标志 ──
let _readAloudPending = false
export function getReadAloudPending(): boolean { return _readAloudPending }
export function setReadAloudPending(v: boolean) { _readAloudPending = v }

// ── Metrics: lightweight observability counters ──
export const metrics = {
  /** @deprecated Use stats.totalMessages — this getter avoids double counting */
  get totalMessages() { return stats.totalMessages },
  avgResponseTimeMs: 0,
  recallCalls: 0,
  cliCalls: 0,
  augmentsInjected: 0,
  lastHeartbeat: 0,
  uptime: Date.now(),
  // internal: rolling average helper
  _responseTimeSum: 0,
  _responseTimeCount: 0,
  // ── Context compression tracking ──
  totalAugmentTokens: 0,         // cumulative augment tokens injected
  totalConversationTokens: 0,    // estimated full-context tokens if no augment compression
}

/** Record a response cycle's elapsed time */
export function metricsRecordResponseTime(ms: number) {
  metrics._responseTimeSum += ms
  metrics._responseTimeCount++
  metrics.avgResponseTimeMs = Math.round(metrics._responseTimeSum / metrics._responseTimeCount)
}

/** Record augment injection token stats for compression rate tracking */
export function metricsRecordAugmentTokens(augmentTokens: number, conversationTokens: number) {
  metrics.totalAugmentTokens += augmentTokens
  metrics.totalConversationTokens += conversationTokens
}

/** Get compression rate: 1 - (augmentTokens / conversationTokens) */
export function getCompressionRate(): { rate: number; augmentTokens: number; conversationTokens: number; saved: number } {
  const a = metrics.totalAugmentTokens
  const c = metrics.totalConversationTokens
  if (c === 0) return { rate: 0, augmentTokens: a, conversationTokens: c, saved: 0 }
  const rate = 1 - (a / c)
  return { rate, augmentTokens: a, conversationTokens: c, saved: c - a }
}

/** Format metrics for display */
export function formatMetrics(): string {
  const uptimeH = ((Date.now() - metrics.uptime) / 3600000).toFixed(1)
  const lastHbAgo = metrics.lastHeartbeat > 0 ? Math.round((Date.now() - metrics.lastHeartbeat) / 60000) : -1
  const comp = getCompressionRate()
  const compLine = comp.conversationTokens > 0
    ? `Context compression: ${(comp.rate * 100).toFixed(1)}% (saved ~${comp.saved} tokens)`
    : `Context compression: N/A (no data yet)`
  return [
    `cc-soul Metrics`,
    `───────────────────`,
    `Uptime: ${uptimeH}h`,
    `Total messages: ${metrics.totalMessages}`,
    `Avg response time: ${metrics.avgResponseTimeMs}ms`,
    `Recall calls: ${metrics.recallCalls}`,
    `CLI calls: ${metrics.cliCalls}`,
    `Augments injected: ${metrics.augmentsInjected}`,
    compLine,
    `Last heartbeat: ${lastHbAgo >= 0 ? lastHbAgo + 'min ago' : 'never'}`,
  ].join('\n')
}

// ── Stats (lives in handler — read/written by many modules) ──
export const stats: InteractionStats = {
  totalMessages: 0,
  firstSeen: 0,
  corrections: 0,
  positiveFeedback: 0,
  tasks: 0,
  topics: new Set(),
  driftCount: 0,
}

export function loadStats() {
  const raw = loadJson<any>(STATS_PATH, null)
  if (raw) {
    stats.totalMessages = raw.totalMessages || 0
    stats.firstSeen = raw.firstSeen || Date.now()
    stats.corrections = raw.corrections || 0
    stats.positiveFeedback = raw.positiveFeedback || 0
    stats.tasks = raw.tasks || 0
    stats.topics = new Set(raw.topics || [])
    stats.driftCount = raw.driftCount || 0
  } else {
    stats.firstSeen = Date.now()
  }
}

export function saveStats() {
  debouncedSave(STATS_PATH, {
    totalMessages: stats.totalMessages,
    firstSeen: stats.firstSeen,
    corrections: stats.corrections,
    positiveFeedback: stats.positiveFeedback,
    tasks: stats.tasks,
    topics: [...stats.topics].slice(-100),
    driftCount: stats.driftCount,
  })
}

/**
 * Returns a snapshot of interaction stats.
 * Use this instead of importing `stats` directly to avoid circular deps.
 */
export function getStats(): { totalMessages: number; corrections: number; firstSeen: number } {
  return { totalMessages: stats.totalMessages, corrections: stats.corrections, firstSeen: stats.firstSeen }
}

// ── Response tracking (per-session to prevent cross-session pollution) ──

export interface SessionState {
  lastPrompt: string
  lastResponseContent: string
  lastSenderId: string
  lastChannelId: string
  lastAugmentsUsed: string[]
  lastRecalledContents: string[]
  lastMatchedRuleTexts: string[]  // rule text strings for per-rule quality tracking
  lastAccessed: number  // P0-4: LRU timestamp for eviction
  turnCount: number     // turns since last session reset
  lastTopicKeywords: string[]  // keywords from last turn for topic-shift detection
  lastQualityScore: number  // previous turn quality score (0-10), for feedback loop
  _pendingCorrectionVerify?: boolean
  _lastAnalyzedPrompt?: string
  _skipNextMemory?: boolean
  _rawUserMsg?: string  // clean user message before augment injection
  startMood?: number    // 会话首条消息时的 mood，用于情绪弧线匹配
}

// ── Soul Mode: when enabled, all replies come from avatar (灵魂模式) ──
let soulMode = false
let soulModeSpeaker = ''  // who is currently talking to the soul

export function getSoulMode(): { active: boolean; speaker: string } {
  return { active: soulMode, speaker: soulModeSpeaker }
}
export function setSoulMode(active: boolean, speaker?: string) {
  soulMode = active
  soulModeSpeaker = speaker || ''
  console.log(`[cc-soul][soul-mode] ${active ? `ON (speaker: ${soulModeSpeaker})` : 'OFF'}`)
}
const sessionStates = new Map<string, SessionState>()
const MAX_SESSIONS = 20

export function getSessionState(sessionKey: string): SessionState {
  let state = sessionStates.get(sessionKey)
  if (!state) {
    state = { lastPrompt: '', lastResponseContent: '', lastSenderId: '', lastChannelId: '', lastAugmentsUsed: [], lastRecalledContents: [], lastMatchedRuleTexts: [], lastAccessed: Date.now(), turnCount: 0, lastTopicKeywords: [], lastQualityScore: -1 }
    sessionStates.set(sessionKey, state)
    // LRU evict: Map front = least recently used (oldest insertion/re-set order)
    if (sessionStates.size > MAX_SESSIONS) {
      const oldestKey = sessionStates.keys().next().value
      if (oldestKey !== undefined && oldestKey !== sessionKey) sessionStates.delete(oldestKey)
    }
  } else {
    // LRU: move to end of Map insertion order
    sessionStates.delete(sessionKey)
    state.lastAccessed = Date.now()
    sessionStates.set(sessionKey, state)
  }
  return state
}

// ── Topic-shift detection & CLI session reset ──

const TOPIC_SHIFT_MIN_TURNS = 3       // don't reset if < 3 turns in session
const TOPIC_SHIFT_THRESHOLD = 0.15    // jaccard overlap below this = topic shift
const GREETING_PATTERNS = /^(你好|hi|hello|hey|嗨|哈喽|早|晚上好|下午好|在吗|在不在)/i

/**
 * Extract topic keywords from a message (CJK 3+ chars + latin words 4+ chars).
 */
function extractTopicKeywords(msg: string): string[] {
  const cjk = msg.match(/[\u4e00-\u9fff]{2,}/g) || []
  const latin = msg.match(/[a-zA-Z]{4,}/gi) || []
  return [...cjk, ...latin.map(w => w.toLowerCase())]
}

/**
 * Jaccard similarity between two keyword sets.
 */
function keywordOverlap(a: string[], b: string[]): number {
  if (a.length === 0 || b.length === 0) return 0
  const setA = new Set(a)
  const setB = new Set(b)
  let intersection = 0
  for (const w of setA) if (setB.has(w)) intersection++
  const union = new Set([...a, ...b]).size
  return union > 0 ? intersection / union : 0
}

/**
 * Detect topic shift and reset CLI session if needed.
 * Returns true if session was reset.
 */
export function detectTopicShiftAndReset(session: SessionState, userMsg: string, sessionKey: string): boolean {
  const currentKeywords = extractTopicKeywords(userMsg)

  // Greeting always triggers reset if there's accumulated context
  const isGreeting = GREETING_PATTERNS.test(userMsg.trim()) && userMsg.trim().length < 20

  const shouldReset = session.turnCount >= TOPIC_SHIFT_MIN_TURNS && (
    isGreeting ||
    (session.lastTopicKeywords.length > 0 && keywordOverlap(currentKeywords, session.lastTopicKeywords) < TOPIC_SHIFT_THRESHOLD)
  )

  // Update keywords for next turn
  if (currentKeywords.length > 0) {
    session.lastTopicKeywords = currentKeywords.slice(0, 20)
  }
  session.turnCount++

  if (shouldReset) {
    resetCliSession(sessionKey)
    session.turnCount = 0
    session.lastTopicKeywords = currentKeywords.slice(0, 20)
    return true
  }
  return false
}

/**
 * Clear the Claude CLI session ID from openclaw's session store,
 * forcing openclaw to start a fresh claude session on next call.
 */
async function resetCliSession(sessionKey: string): Promise<void> {
  try {
    const { readFileSync, writeFileSync } = await import('fs')
    const { resolve } = await import('path')
    const home = process.env.HOME || process.env.USERPROFILE || ''
    // Derive agent ID from sessionKey (format: "agent:<agentId>:<alias>")
    const parts = sessionKey.split(':')
    const agentId = parts.length >= 2 ? parts[1] : 'cc'
    const storePath = resolve(home, '.openclaw', 'agents', agentId, 'sessions', 'sessions.json')

    const raw = readFileSync(storePath, 'utf-8')
    const store = JSON.parse(raw)
    const entry = store[sessionKey]
    if (!entry) return

    let changed = false
    if (entry.claudeCliSessionId) {
      delete entry.claudeCliSessionId
      changed = true
    }
    if (entry.cliSessionIds) {
      for (const key of Object.keys(entry.cliSessionIds)) {
        if (key.includes('claude')) {
          delete entry.cliSessionIds[key]
          changed = true
        }
      }
      if (Object.keys(entry.cliSessionIds).length === 0) {
        delete entry.cliSessionIds
      }
    }
    if (changed) {
      entry.updatedAt = Date.now()
      writeFileSync(storePath, JSON.stringify(store, null, 2))
      console.log(`[cc-soul][topic-shift] CLI session reset for ${sessionKey}`)
    }
  } catch (err) {
    // Session store might not exist or be locked — non-fatal
    console.log(`[cc-soul][topic-shift] reset failed: ${err}`)
  }
}

// ── Last active session key (for background tasks like heartbeat journal) ──
let lastActiveSessionKey = '_default'
export function getLastActiveSessionKey(): string { return lastActiveSessionKey }
export function setLastActiveSessionKey(v: string) { lastActiveSessionKey = v }

// ── Privacy mode (Feature 2) — persisted to file for cross-process sharing ──
import { resolve as _resolve } from 'path'
import { homedir as _homedir } from 'os'
import { existsSync as _existsSync, readFileSync as _readFileSync, writeFileSync as _writeFileSync } from 'fs'
const _privacyLockPath = _resolve(_homedir(), '.openclaw/plugins/cc-soul/data/.privacy-mode')
let privacyMode = (() => { try { return _existsSync(_privacyLockPath) } catch { return false } })()
export function getPrivacyMode(): boolean { return privacyMode }
export function setPrivacyMode(v: boolean) {
  privacyMode = v
  try {
    if (v) _writeFileSync(_privacyLockPath, '1', 'utf-8')
    else try { import('fs').then(({ unlinkSync }) => unlinkSync(_privacyLockPath)).catch(() => {}) } catch {} // intentionally silent — file cleanup
  } catch {}
}

// ── Quick shortcuts (Feature 3) ──
export const shortcuts: Record<string, string> = {
  's': '功能状态',
  'm': '记忆图谱',
  '?': '最近在聊什么',
  '!': '紧急模式',
}

// ── Initialization flags ──
let initialized = false
export function getInitialized(): boolean { return initialized }
export function setInitialized(v: boolean) { initialized = v }

let heartbeatRunning = false
export function getHeartbeatRunning(): boolean { return heartbeatRunning }
export function setHeartbeatRunning(v: boolean) { heartbeatRunning = v }

let heartbeatStartedAt = 0
export function getHeartbeatStartedAt(): number { return heartbeatStartedAt }
export function setHeartbeatStartedAt(v: number) { heartbeatStartedAt = v }

let heartbeatInterval: ReturnType<typeof setInterval> | null = null
export function getHeartbeatInterval(): ReturnType<typeof setInterval> | null { return heartbeatInterval }
export function setHeartbeatInterval(v: ReturnType<typeof setInterval> | null) { heartbeatInterval = v }

// ── Narrative refresh (bridges CLI + prompt-builder cache) ──

const NARRATIVE_CACHE_MS = 3600 * 1000

export function refreshNarrativeAsync() {
  if (narrativeCache.text && Date.now() - narrativeCache.ts < NARRATIVE_CACHE_MS) return

  const daysKnown = Math.max(1, Math.floor((Date.now() - stats.firstSeen) / 86400000))
  const facts = [
    `互动${stats.totalMessages}次，认识${daysKnown}天`,
    `被纠正${stats.corrections}次，完成${stats.tasks}个任务`,
    innerState.userModel ? `理解: ${innerState.userModel.slice(0, 200)}` : '',
    getRecentJournal(3),
  ].filter(Boolean).join('\n')

  const prompt = `根据以下信息，用第一人称写2-3句话描述你和这个用户的关系。要有感情，像写给自己看的日记。不要说"作为AI"。\n\n${facts}`

  spawnCLI(prompt, (output) => {
    if (output && output.length > 20) {
      setNarrativeCache(output.slice(0, 500))
    }
  })
}
