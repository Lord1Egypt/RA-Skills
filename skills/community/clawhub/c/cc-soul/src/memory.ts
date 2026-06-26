/**
 * memory.ts — Memory System (barrel + core CRUD)
 *
 * Sub-modules:
 *   memory-utils.ts      — trigrams, synonyms, compression, constants
 *   memory-recall.ts     — BM25 + recall engine + stats
 *   memory-lifecycle.ts  — consolidation, decay, episodes, association, commands, audit
 */

import { resolve } from 'path'
import { existsSync, statSync, writeFileSync } from 'fs'

import type { Memory } from './types.ts'
import { MEMORIES_PATH, HISTORY_PATH, DATA_DIR, loadJson, debouncedSave } from './persistence.ts'
// spawnCLI import removed — AUDN gray zone now uses local multi-signal voting
import { autoExtractFromMemory } from './fact-store.ts'
import { getParam } from './auto-tune.ts'
import {
  initSQLite, migrateFromJSON, migrateHistoryFromJSON,
  sqliteAddMemory, sqliteUpdateMemory,
  sqliteFindByContent, sqliteCount, sqliteGetAll,
  sqliteAddChatTurn, sqliteGetRecentHistory, sqliteTrimHistory,
} from './sqlite-store.ts'
// audit.ts removed
import { addRelation } from './graph.ts'

// ── Imports from sub-modules ──
import {
  trigrams, trigramSimilarity, timeDecay,
  MAX_MEMORIES, MAX_HISTORY, INJECT_HISTORY,
  compressMemory, detectMemoryPoisoning, extractReasoning, defaultVisibility,
  emitCacheEvent, generateMemoryId, appendLineage, classifyConflict, contextAwareSimilarity,
} from './memory-utils.ts'
import { invalidateIDF, incrementalIDFUpdate, updateRecallIndex, rebuildRecallIndex } from './memory-recall.ts'
import { invalidateFieldIDF } from './activation-field.ts'

// ── Re-exports (barrel) ──
export {
  trigrams, trigramSimilarity, shuffleArray, compressMemory,
  SYNONYM_MAP, MAX_MEMORIES, MAX_HISTORY, INJECT_HISTORY,
  detectMemoryPoisoning, extractReasoning, defaultVisibility,
} from './memory-utils.ts'
export {
  recall, getCachedFusedRecall, invalidateIDF, degradeMemoryConfidence,
  trackRecallImpact, getRecallImpactBoost, getRecallRate, recallStats, recallImpact,
  recallWithScores, updateRecallIndex, rebuildRecallIndex, incrementalIDFUpdate,
} from './memory-recall.ts'
export {
  consolidateMemories, generateInsights, recallFeedbackLoop,
  triggerAssociativeRecall, getAssociativeRecall,
  parseMemoryCommands, executeMemoryCommands, getPendingSearchResults,
  scanForContradictions,
  predictiveRecall, generatePrediction, triggerSessionSummary,
  cleanupNetworkKnowledge, resolveNetworkConflicts,
  episodes, loadEpisodes, recordEpisode, recallEpisodes, buildEpisodeContext,
  processMemoryDecay, pruneExpiredMemories, compressOldMemories, reviveDecayedMemories,
  restoreArchivedMemories,
  sqliteMaintenance, getStorageStatus,
  auditMemoryHealth,
} from './memory-lifecycle.ts'

// Lazy-loaded modules (avoid circular deps + ESM require issues)
let _handlerState: any = null
let _bodyMod: any = null
let _signalsMod: any = null
let _distillMod: any = null

export function getLazyModule(name: string) {
  switch (name) {
    case 'handler-state':
      if (!_handlerState) { import('./handler-state.ts').then(m => { _handlerState = m }).catch((e: any) => { console.error(`[cc-soul] module load failed (handler-state): ${e.message}`) }) }
      return _handlerState
    case 'body':
      if (!_bodyMod) { import('./body.ts').then(m => { _bodyMod = m }).catch((e: any) => { console.error(`[cc-soul] module load failed (body): ${e.message}`) }) }
      return _bodyMod
    case 'signals':
      if (!_signalsMod) { import('./signals.ts').then(m => { _signalsMod = m }).catch((e: any) => { console.error(`[cc-soul] module load failed (signals): ${e.message}`) }) }
      return _signalsMod
    case 'distill':
      if (!_distillMod) { import('./distill.ts').then(m => { _distillMod = m }).catch((e: any) => { console.error(`[cc-soul] module load failed (distill): ${e.message}`) }) }
      return _distillMod
    default: return null
  }
}
// Pre-load lazily in background
setTimeout(() => {
  import('./handler-state.ts').then(m => { _handlerState = m }).catch((e: any) => { console.error(`[cc-soul] module load failed (handler-state): ${e.message}`) })
  import('./body.ts').then(m => { _bodyMod = m }).catch((e: any) => { console.error(`[cc-soul] module load failed (body): ${e.message}`) })
  import('./signals.ts').then(m => { _signalsMod = m }).catch((e: any) => { console.error(`[cc-soul] module load failed (signals): ${e.message}`) })
  import('./distill.ts').then(m => { _distillMod = m }).catch((e: any) => { console.error(`[cc-soul] module load failed (distill): ${e.message}`) })
}, 1000)

// ═══════════════════════════════════════════════════════════════════════════════
// Topic River — 话题河流：segment ID 追踪
// ═══════════════════════════════════════════════════════════════════════════════

let _currentSegmentId = 0
export function incrementSegment(): void { _currentSegmentId++ }
export function getCurrentSegmentId(): number { return _currentSegmentId }

// ═══════════════════════════════════════════════════════════════════════════════
// BAYESIAN CONFIDENCE — Beta distribution posterior update
// ═══════════════════════════════════════════════════════════════════════════════

const BAYES_DEFAULT_ALPHA = 2
const BAYES_DEFAULT_BETA = 1

/** Compute confidence from Beta distribution: α / (α + β) */
export function bayesConfidence(mem: Memory): number {
  const a = mem.bayesAlpha ?? BAYES_DEFAULT_ALPHA
  const b = mem.bayesBeta ?? BAYES_DEFAULT_BETA
  return a / (a + b)
}

/** Ensure Bayes fields exist on a memory (backward-compatible init) */
function ensureBayesFields(mem: Memory) {
  if (mem.bayesAlpha == null) {
    // Reverse-engineer from existing confidence if present
    const c = mem.confidence ?? 0.67
    // alpha / (alpha + beta) ≈ c, keep sum ≈ 3 for prior strength
    const sum = BAYES_DEFAULT_ALPHA + BAYES_DEFAULT_BETA
    mem.bayesAlpha = c * sum
    mem.bayesBeta = (1 - c) * sum
  }
  if (mem.bayesBeta == null) mem.bayesBeta = BAYES_DEFAULT_BETA
}

/** Positive evidence: recall confirmed by user context */
export function bayesBoost(mem: Memory, delta = 0.5) {
  ensureBayesFields(mem)
  mem.bayesAlpha! += delta
  mem.confidence = bayesConfidence(mem)
}

/** Negative evidence: recall ignored by user */
export function bayesPenalize(mem: Memory, delta = 0.5) {
  ensureBayesFields(mem)
  mem.bayesBeta! += delta
  mem.confidence = bayesConfidence(mem)
}

/** Strong negative: user corrected this memory */
export function bayesCorrect(mem: Memory, delta = 2) {
  ensureBayesFields(mem)
  mem.bayesBeta! += delta
  mem.confidence = bayesConfidence(mem)
}

/**
 * Sync memory confidence/scope changes to SQLite.
 * Call this whenever you modify mem.confidence or mem.scope in-memory.
 */
export function syncToSQLite(mem: Memory, updates: { confidence?: number; scope?: string; tier?: string; recallCount?: number; lastAccessed?: number; lastRecalled?: number }, findByContent?: string) {
  if (!useSQLite) return
  // 优先用 findByContent（旧内容），fallback 到 mem.content（当前内容）
  // 防止 content 被修改后 SQLite 找不到记录
  const found = sqliteFindByContent(findByContent || mem.content)
  if (found) {
    sqliteUpdateMemory(found.id, updates)
  }
}

/** Whether SQLite is the active storage backend (vs JSON fallback) */
export let useSQLite = false

/** Whether memories have been loaded into memoryState (lazy) */
export let _memoriesLoaded = false

/** Whether SQLite has been initialized for direct queries (lightweight) */
let _sqliteInitDone = false

/**
 * Ensure SQLite is initialized for direct queries (no memory loading).
 * This is cheap (~10ms) and enables recall() to work without loadMemories().
 */
export function ensureSQLiteReady(): boolean {
  if (_sqliteInitDone) return useSQLite
  _sqliteInitDone = true
  const ok = initSQLite()
  if (ok) useSQLite = true
  return ok
}

/**
 * Ensure memoryState.memories is populated (lazy load).
 * Call this only when you actually need the in-memory array.
 */
export function ensureMemoriesLoaded(): void {
  if (_memoriesLoaded) return
  _memoriesLoaded = true
  loadMemories()
}


// ═══════════════════════════════════════════════════════════════════════════════
// Mutable state — exported as object so ESM consumers can read live values
// ═══════════════════════════════════════════════════════════════════════════════

interface ChatTurn { user: string; assistant: string; ts: number }

export const memoryState = {
  memories: [] as Memory[],
  chatHistory: [] as ChatTurn[],
}

// ── 写入去重集合（5分钟 TTL，防止同一内容短时间内重复存储）──
export const _recentWriteHashes = new Set<string>()
// 5 分钟后自动清除（通过 heartbeat 或 setTimeout）
setInterval(() => { _recentWriteHashes.clear() }, 300000)

// ═══════════════════════════════════════════════════════════════════════════════
// MEMORY INDEX — O(1) lookup by scope (maintained on add/remove)
// ═══════════════════════════════════════════════════════════════════════════════

export const scopeIndex = new Map<string, Memory[]>()

// ── Content hash index for O(1) exact-match dedup in decideMemoryAction ──
const contentIndex = new Map<string, string>() // content前50字符(lowercase) → full content (stable across splices)

function rebuildContentIndex() {
  contentIndex.clear()
  for (let i = 0; i < memoryState.memories.length; i++) {
    const key = memoryState.memories[i].content.slice(0, 50).toLowerCase()
    contentIndex.set(key, memoryState.memories[i].content)
  }
}

export function rebuildScopeIndex() {
  scopeIndex.clear()
  for (const mem of memoryState.memories) {
    const arr = scopeIndex.get(mem.scope) || []
    arr.push(mem)
    scopeIndex.set(mem.scope, arr)
  }
  rebuildContentIndex()
}

export function getMemoriesByScope(scope: string): Memory[] {
  return scopeIndex.get(scope) || []
}

// ═══════════════════════════════════════════════════════════════════════════════
// WORKING MEMORY — per-session context, auto-cleared between sessions
// ═══════════════════════════════════════════════════════════════════════════════

interface WorkingMemoryEntry {
  content: string
  sessionKey: string    // which session this belongs to
  addedAt: number
}

const MAX_WORKING = 20  // max entries per session
const MAX_WORKING_SESSIONS = 100  // P0-2: cap total sessions to prevent unbounded Map growth
const workingMemory = new Map<string, WorkingMemoryEntry[]>()

/**
 * Add to working memory for current session.
 * This stays in memory (not persisted) and is cleared when session ends.
 */
export function addWorkingMemory(content: string, sessionKey: string) {
  if (!content || content.length < 5) return
  // 真 LRU：每次访问 delete + re-set（Map 按插入顺序迭代，最近 set 的在末尾）
  let entries = workingMemory.get(sessionKey)
  if (entries) {
    workingMemory.delete(sessionKey)  // 先删
  } else {
    entries = []
  }
  workingMemory.set(sessionKey, entries)  // 重插到末尾（= 最近访问）
  // Dedup
  if (entries.some(e => e.content === content)) return
  entries.push({ content, sessionKey, addedAt: Date.now() })
  // Trim per-session entries
  if (entries.length > MAX_WORKING) entries.splice(0, entries.length - MAX_WORKING)
  // LRU eviction — cap total sessions（keys().next() 现在是真正最久没访问的）
  if (workingMemory.size > MAX_WORKING_SESSIONS) {
    const oldest = workingMemory.keys().next().value
    if (oldest) workingMemory.delete(oldest)
  }
}

/**
 * Get working memory context for current session.
 * Always injected — no recall needed.
 */
export function buildWorkingMemoryContext(sessionKey: string): string {
  const entries = workingMemory.get(sessionKey)
  if (!entries || entries.length === 0) return ''
  // LRU touch：读取也算访问
  workingMemory.delete(sessionKey)
  workingMemory.set(sessionKey, entries)
  return `[Working Memory — this session]\n${entries.map(e => `- ${e.content}`).join('\n')}`
}

/**
 * Clear working memory for a session (called on session end/reset).
 * Important facts get archived to regular memories before clearing.
 */
export function archiveWorkingMemory(sessionKey: string) {
  const entries = workingMemory.get(sessionKey)
  if (!entries || entries.length === 0) return

  let archived = 0
  for (const entry of entries) {
    // Only archive entries that are likely important
    if (entry.content.length < 50) continue // too short to be meaningful
    // Check if it contains actionable/factual content (simple heuristic)
    const hasSubstance = /[：:=→]|因为|所以|结论|发现|决定|计划|问题|解决|配置|版本|密码|账号|地址/.test(entry.content)
    if (!hasSubstance && entry.content.length < 100) continue

    addMemory(entry.content, 'event', undefined, 'channel', sessionKey)
    archived++
  }
  if (archived > 0) console.log(`[cc-soul][memory] archived ${archived}/${entries.length} working memory entries`)
  workingMemory.delete(sessionKey)
}

/**
 * Cleanup stale working memory (sessions older than 6 hours).
 */
export function cleanupWorkingMemory() {
  const cutoff = Date.now() - 6 * 3600000
  for (const [key, entries] of workingMemory) {
    if (entries.length > 0 && entries[entries.length - 1].addedAt < cutoff) {
      archiveWorkingMemory(key)
    }
  }
}

// ═══════════════════════════════════════════════════════════════════════════════

// ═══════════════════════════════════════════════════════════════════════════════
// CORE MEMORY — always-available critical knowledge (MemGPT-inspired tiering)
// ═══════════════════════════════════════════════════════════════════════════════

const CORE_MEMORY_PATH = resolve(DATA_DIR, 'core_memory.json')
const MAX_CORE_MEMORIES = 100

interface CoreMemory {
  content: string
  category: 'user_fact' | 'preference' | 'rule' | 'identity' | 'relationship'
  addedAt: number
  source: string  // how it got promoted: "auto" | "manual" | "reflection"
}

export let coreMemories: CoreMemory[] = []

export function loadCoreMemories() {
  coreMemories = loadJson<CoreMemory[]>(CORE_MEMORY_PATH, [])
  console.log(`[cc-soul][core-memory] loaded ${coreMemories.length} core memories`)
}

function saveCoreMemories() {
  debouncedSave(CORE_MEMORY_PATH, coreMemories)
}

/**
 * Promote a regular memory to core (always-available, never evicted).
 */
export function promoteToCore(content: string, category: CoreMemory['category'], source = 'auto') {
  // Dedup
  if (coreMemories.some(m => m.content === content)) return

  // Reject system augment content that shouldn't be in core memory
  const REJECT_PREFIXES = ['[goal completed]', '[Working Memory', '[当前面向:', '[隐私模式]', '[当前对话者]', '[内部矛盾警告]', '[System]', '[安全警告]', 'Rating:', '→ **Rating']
  if (REJECT_PREFIXES.some(p => content.includes(p))) {
    console.log(`[cc-soul][core-memory] REJECT (system augment): ${content.slice(0, 60)}`)
    return
  }

  coreMemories.push({ content, category, addedAt: Date.now(), source })

  // If over limit, remove oldest auto-promoted (keep manual ones)
  if (coreMemories.length > MAX_CORE_MEMORIES) {
    const autoIdx = coreMemories.findIndex(m => m.source === 'auto')
    if (autoIdx >= 0) coreMemories.splice(autoIdx, 1)
  }

  saveCoreMemories()
  console.log(`[cc-soul][core-memory] promoted: ${content.slice(0, 50)} [${category}]`)
}

/**
 * Build core memory context for prompt injection (always included, no recall needed).
 */
export function buildCoreMemoryContext(): string {
  if (coreMemories.length === 0) return ''

  // 梯度压缩注入（ChatGPT 启发）：按 engagement 排序，热的全文，冷的压缩
  let fullTextCount = 10, summaryCount = 20
  try {
    const { computeBudget } = require('./context-budget.ts')
    const budget = computeBudget()
    fullTextCount = Math.min(10, Math.floor(budget.augmentBudget / 200))
    summaryCount = Math.min(20, Math.floor((budget.augmentBudget - fullTextCount * 200) / 50))
  } catch {}

  // 按 engagement 排序（从 memories 中找对应的 engagement 数据）
  const sorted = [...coreMemories].sort((a, b) => {
    const memA = memoryState.memories.find(m => m.content === a.content)
    const memB = memoryState.memories.find(m => m.content === b.content)
    return (memB?.injectionEngagement ?? 0) - (memA?.injectionEngagement ?? 0)
  })

  const lines: string[] = []
  for (let i = 0; i < sorted.length; i++) {
    if (i < fullTextCount) {
      lines.push(`- [${sorted[i].category}] ${sorted[i].content}`)
    } else if (i < fullTextCount + summaryCount) {
      lines.push(`- [${sorted[i].category}] ${sorted[i].content.slice(0, 20)}...`)
    } else {
      // 骨架：只保留三元组
      try {
        const { extractFacts } = require('./fact-store.ts')
        const facts = extractFacts(sorted[i].content)
        if (facts.length > 0) lines.push(`- ${facts.map((f: any) => `${f.predicate}:${f.object}`).join(',')}`)
      } catch {}
    }
  }
  return `[Core Memory — always available]\n${lines.join('\n')}`
}

/**
 * 统一记忆晋升/降级评估（合并 autoPromoteToCoreMemory + heatPromotion + STAC）
 * 三个信号源加权决策，避免独立系统震荡
 */
export function evaluateAndPromoteMemories() {
  if (coreMemories.length >= MAX_CORE_MEMORIES) return

  for (const mem of memoryState.memories) {
    if (!mem || mem.scope === 'expired' || mem.scope === 'decayed') continue

    // Signal 1: engagement rate (from heatPromotion)
    const eng = mem.injectionEngagement ?? 0
    const miss = mem.injectionMiss ?? 0
    const engRate = eng / Math.max(1, eng + miss)
    const engSignal = (engRate > 0.6 && eng >= 5) ? 1.0 : 0

    // Signal 2: intrinsic value (from autoPromoteToCoreMemory)
    let valueSignal = 0
    if (mem.emotion === 'important' || mem.emotion === 'warm') valueSignal += 0.5
    if ((mem.recallCount ?? 0) >= 3) valueSignal += 0.5
    if (mem.scope === 'preference' || mem.scope === 'fact') valueSignal += 0.3
    valueSignal = Math.min(1.0, valueSignal)

    // Signal 3: FSRS stability trend (STAC original)
    let stacSignal = 0
    const rc = mem.recallCount ?? 0
    const ageDays = Math.max(1, (Date.now() - (mem.ts || Date.now())) / 86400000)
    const recallRate = rc / ageDays
    if (recallRate > 0.5 && (mem.fsrs?.stability ?? 0) > 10) stacSignal = 1.0

    // Weighted decision
    const promoteScore = engSignal * 0.4 + valueSignal * 0.3 + stacSignal * 0.3

    // Promote: score > 0.5 and not already core
    if (promoteScore > 0.5 && mem.scope !== 'core_memory') {
      if (coreMemories.length >= MAX_CORE_MEMORIES) break
      mem.scope = 'core_memory'
      coreMemories.push({ content: mem.content, category: mem.scope === 'preference' ? 'preference' : 'user_fact', addedAt: Date.now(), source: 'auto' })
      try { require('./decision-log.ts').logDecision('unified_promote', (mem.content || '').slice(0, 30), `eng=${engSignal.toFixed(1)} val=${valueSignal.toFixed(1)} stac=${stacSignal.toFixed(1)} total=${promoteScore.toFixed(2)}`) } catch {}
      try { require('./memory-utils.ts').appendLineage(mem, { action: 'promoted', ts: Date.now(), delta: `→core_memory, score=${promoteScore.toFixed(2)}` }) } catch {}
    }

    // Demote: core but engagement persistently low
    if (mem.scope === 'core_memory' && eng > 0 && engRate < 0.2) {
      mem.scope = 'fact'
      mem.injectionEngagement = Math.floor(eng / 2)
      mem.injectionMiss = Math.floor(miss / 2)
      coreMemories = coreMemories.filter(c => c.content !== mem.content)
      try { require('./decision-log.ts').logDecision('unified_demote', (mem.content || '').slice(0, 30), `engRate=${engRate.toFixed(2)}`) } catch {}
    }
  }
}

/** @deprecated Use evaluateAndPromoteMemories() — kept for backward compatibility */
export function autoPromoteToCoreMemory() { evaluateAndPromoteMemories() }

// ═══════════════════════════════════════════════════════════════════════════════
// Chat History
// ═══════════════════════════════════════════════════════════════════════════════

export function addToHistory(user: string, assistant: string) {
  memoryState.chatHistory.push({
    user: user.slice(0, 1000),
    assistant: assistant.slice(0, 2000),
    ts: Date.now(),
  })
  // 超过上限：保留最近的
  if (memoryState.chatHistory.length > MAX_HISTORY) {
    const trimmed = memoryState.chatHistory.slice(-MAX_HISTORY)
    memoryState.chatHistory.length = 0
    memoryState.chatHistory.push(...trimmed)
  }
  // Write to SQLite + JSON
  if (useSQLite) {
    sqliteAddChatTurn(user, assistant)
    sqliteTrimHistory(MAX_HISTORY)
  }
  debouncedSave(HISTORY_PATH, memoryState.chatHistory)
}

export function buildHistoryContext(maxTokens?: number): string {
  if (memoryState.chatHistory.length === 0) return ''

  // 自适应 context budget：根据后端 window 动态决定历史轮数和截断
  let trimmed = memoryState.chatHistory
  let historyBudget = maxTokens ?? 4000

  try {
    const { computeBudget, trimHistory } = require('./context-budget.ts')
    const budget = computeBudget()
    trimmed = trimHistory(memoryState.chatHistory, budget)
    historyBudget = budget.historyBudget
  } catch {
    // fallback：用旧的硬编码逻辑
    trimmed = memoryState.chatHistory.slice(-INJECT_HISTORY)
  }

  const lines: string[] = []
  let totalTokens = 0

  // Build from most recent backward, stop when budget exceeded
  for (let i = trimmed.length - 1; i >= 0; i--) {
    const t = trimmed[i]
    const timeStr = new Date(t.ts).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
    const line = `[${timeStr}] 用户: ${t.user.slice(0, 200)}\n助手: ${t.assistant.slice(0, 400)}`
    const lineTokens = Math.ceil(line.length * 0.8)
    if (totalTokens + lineTokens > historyBudget) break
    lines.unshift(line)
    totalTokens += lineTokens
  }

  if (lines.length === 0) return ''
  return `[对话历史（最近${lines.length}轮）]\n${lines.join('\n\n')}`
}

// ═══════════════════════════════════════════════════════════════════════════════
// Semantic Tag Generation (local extraction — no LLM needed)
// ═══════════════════════════════════════════════════════════════════════════════

/** Well-known tech keywords for tag extraction */
const TECH_KEYWORDS = new Set([
  'python', 'javascript', 'typescript', 'rust', 'golang', 'swift', 'kotlin',
  'java', 'ruby', 'php', 'c++', 'docker', 'kubernetes', 'k8s', 'git',
  'github', 'gitlab', 'npm', 'pip', 'cargo', 'webpack', 'vite', 'react',
  'vue', 'angular', 'svelte', 'node', 'deno', 'bun', 'flask', 'django',
  'fastapi', 'express', 'nginx', 'redis', 'mysql', 'postgres', 'mongodb',
  'sqlite', 'elasticsearch', 'kafka', 'rabbitmq', 'grpc', 'graphql',
  'rest', 'api', 'http', 'https', 'websocket', 'tcp', 'udp',
  'linux', 'macos', 'windows', 'ios', 'android', 'arm64', 'x86',
  'cpu', 'gpu', 'cuda', 'llm', 'gpt', 'claude', 'openai', 'transformer',
  'embedding', 'vector', 'rag', 'fine-tune', 'lora', 'bert',
  'ida', 'frida', 'mach-o', 'elf', 'dyld', 'objc', 'runtime',
  'ci', 'cd', 'aws', 'gcp', 'azure', 'terraform', 'ansible',
  'json', 'yaml', 'toml', 'xml', 'csv', 'protobuf', 'sql',
  'html', 'css', 'scss', 'tailwind', 'figma',
  'test', 'debug', 'deploy', 'build', 'compile', 'lint',
  'async', 'await', 'promise', 'thread', 'mutex', 'lock',
  'wechat', 'telegram', 'slack', 'discord',
])

/**
 * Extract tags from text locally — no LLM call needed.
 * Extracts: Chinese 2-4 char words, English 3+ letter words, tech keywords.
 * Returns 5-10 unique tags.
 */
export function extractTagsLocal(content: string): string[] {
  const tags = new Set<string>()
  const lower = content.toLowerCase()

  // 1. Chinese word extraction: 2-4 char continuous CJK sequences
  const zhMatches = content.match(/[\u4e00-\u9fff]{2,4}/g) || []
  for (const w of zhMatches) {
    if (w.length >= 2) tags.add(w)
  }

  // 2. English/Latin words: 3+ letters, lowercased
  const enMatches = lower.match(/[a-z][a-z0-9._-]{2,}/g) || []
  for (const w of enMatches) {
    // Skip very common stopwords
    if (['the', 'and', 'for', 'that', 'this', 'with', 'from', 'are', 'was', 'were',
         'been', 'have', 'has', 'had', 'not', 'but', 'what', 'all', 'can', 'her',
         'his', 'our', 'their', 'will', 'would', 'could', 'should', 'may', 'might',
         'shall', 'also', 'into', 'than', 'then', 'them', 'these', 'those',
         'very', 'just', 'about', 'some', 'other', 'more', 'only', 'your',
         'how', 'its', 'let', 'being', 'both', 'each', 'few', 'most',
         'such', 'too', 'any', 'own', 'same', 'did', 'does', 'got'].includes(w)) continue
    tags.add(w)
  }

  // 3. Tech keywords: boost priority by adding them regardless of stopword filter
  for (const kw of TECH_KEYWORDS) {
    if (lower.includes(kw)) tags.add(kw)
  }

  // 4. Scope-like patterns: URLs, file paths, version numbers
  const urlMatch = lower.match(/(?:https?:\/\/)?([a-z0-9.-]+\.[a-z]{2,})/g)
  if (urlMatch) {
    for (const u of urlMatch.slice(0, 2)) tags.add(u.replace(/^https?:\/\//, ''))
  }

  // Deduplicate and limit to 5-10 tags, preferring shorter (more specific) tags
  const sorted = [...tags]
    .filter(t => t.length >= 2 && t.length <= 20)
    .sort((a, b) => a.length - b.length)
  return sorted.slice(0, 10)
}

/**
 * Batch tag queue — tags are extracted locally, no CLI call needed.
 */
const tagQueue: { content: string; ts?: number; index?: number }[] = []
let tagBatchTimer: ReturnType<typeof setTimeout> | null = null

function queueForTagging(content: string, ts?: number, index?: number) {
  tagQueue.push({ content, ts, index })
  // Batch every 2 seconds or when queue reaches 20 (local is fast, can handle more)
  if (tagQueue.length >= 20) {
    flushTagQueue()
  } else if (!tagBatchTimer) {
    tagBatchTimer = setTimeout(flushTagQueue, 2000)
  }
}

function flushTagQueue() {
  if (tagBatchTimer) { clearTimeout(tagBatchTimer); tagBatchTimer = null }
  if (tagQueue.length === 0) return

  const batch = tagQueue.splice(0, 50) // local extraction is fast — take up to 50
  let tagged = 0

  for (const item of batch) {
    const tags = extractTagsLocal(item.content)
    if (tags.length < 2) continue

    let target: typeof memoryState.memories[0] | undefined
    // Primary: ts exact match (ts is unique timestamp)
    if (item.ts) {
      target = memoryState.memories.find(m => m.ts === item.ts && m.content === item.content && !m.tags)
    }
    // Fallback: index + content verification
    if (!target && item.index !== undefined && item.index >= 0 && item.index < memoryState.memories.length) {
      const candidate = memoryState.memories[item.index]
      if (candidate.content === item.content && !candidate.tags) {
        target = candidate
      }
    }
    // Last resort: content-only match
    if (!target) {
      target = memoryState.memories.find(m => m.content === item.content && !m.tags)
    }
    if (target) {
      target.tags = tags
      tagged++
    }
  }

  if (tagged > 0) saveMemories()
}

/**
 * Batch-tag untagged memories in background with throttling.
 * Called from handler.ts initialization with a delay.
 */
export function batchTagUntaggedMemories() {
  const untagged = memoryState.memories
    .map((m, i) => ({ m, i }))
    .filter(({ m }) => !m.tags || m.tags.length === 0)
    .slice(0, 5) // small batch — CLI concurrency is limited

  if (untagged.length === 0) return
  console.log(`[cc-soul][tags] batch tagging ${untagged.length} untagged memories`)

  for (const { m, i } of untagged) {
    queueForTagging(m.content, m.ts, i)
  }
}


// ═══════════════════════════════════════════════════════════════════════════════
// Memory Smart CRUD — decide add/update/skip before writing
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * AUDN Decision Gate — Decide whether to ADD, UPDATE, DELETE, or NOOP a new memory.
 *
 * Three-tier decision:
 *   Fast path (rules):  exact match → NOOP, trigram > 0.9 → UPDATE, trigram < 0.3 → ADD
 *   Medium path (rules): trigram 0.3-0.9 + same scope → UPDATE (merge)
 *   Slow path (LLM):     fact/preference/correction in gray zone → async LLM arbitration
 *
 * Inspired by mem0's AUDN cycle but with rule-first approach to minimize LLM calls.
 */
export function decideMemoryAction(newContent: string, scope?: string): { action: 'add' | 'update' | 'skip'; targetIndex: number } {
  if (memoryState.memories.length === 0) return { action: 'add', targetIndex: -1 }

  // O(1) exact-match via content hash index
  const shortKey = newContent.slice(0, 50).toLowerCase()
  const exactContent = contentIndex.get(shortKey)
  if (exactContent !== undefined && exactContent === newContent) {
    const exactIdx = memoryState.memories.findIndex(m => m.content === newContent)
    if (exactIdx >= 0) return { action: 'skip', targetIndex: exactIdx }
  }

  // Trigram scan — find top 3 similar memories (not just top 1)
  const newTri = trigrams(newContent)
  const candidates: { idx: number; sim: number }[] = []
  const startIdx = Math.max(0, memoryState.memories.length - 500)

  for (let i = startIdx; i < memoryState.memories.length; i++) {
    const mem = memoryState.memories[i]
    if (mem.scope === 'expired') continue

    // Exact match → NOOP
    if (mem.content === newContent) return { action: 'skip', targetIndex: i }

    const memTri = trigrams(mem.content)
    const sim = trigramSimilarity(newTri, memTri)
    if (sim > 0.25) {
      candidates.push({ idx: i, sim })
    }
  }

  candidates.sort((a, b) => b.sim - a.sim)

  // Context-Aware Similarity 增强：trigram 候选用语境相似度精排
  try {
    // contextAwareSimilarity imported at top level
    for (const c of candidates.slice(0, 5)) {
      const mem = memoryState.memories[c.idx]
      if (mem) {
        const ctxSim = contextAwareSimilarity({ content: newContent, ts: Date.now(), scope: scope || 'fact' } as any, mem)
        c.sim = c.sim * 0.6 + ctxSim * 0.4  // 融合：trigram 60% + 语境 40%
      }
    }
    candidates.sort((a, b) => b.sim - a.sim)
  } catch {}

  const best = candidates[0]

  if (!best) return { action: 'add', targetIndex: -1 }

  // Fast path: very high similarity → UPDATE (near-duplicate)
  if (best.sim > 0.9) return { action: 'update', targetIndex: best.idx }

  // Fast path: low similarity → ADD (clearly new)
  if (best.sim < 0.5) return { action: 'add', targetIndex: -1 }

  // Medium path: moderate similarity — scope-aware decision
  const existingMem = memoryState.memories[best.idx]
  const dedupThreshold = getParam('memory.trigram_dedup_threshold')

  if (best.sim > dedupThreshold) {
    return { action: 'update', targetIndex: best.idx }
  }

  // Gray zone (0.5-0.8): local multi-signal voting (replaces async LLM arbitration)
  const existingLen = existingMem.content.length
  const newLen = newContent.length
  const lengthRatio = Math.min(existingLen, newLen) / Math.max(existingLen, newLen)
  const scopeMatch = (scope === existingMem.scope) ? 1 : 0
  const sameDay = Math.abs(Date.now() - existingMem.ts) < 86400000 ? 1 : 0

  const dupScore = best.sim * 0.5 + scopeMatch * 0.2 + lengthRatio * 0.2 + sameDay * 0.1
  if (dupScore > 0.75) {
    return { action: 'skip', targetIndex: best.idx }  // high confidence duplicate
  }
  if (dupScore > 0.55) {
    return { action: 'update', targetIndex: best.idx }  // merge into existing
  }
  return { action: 'add', targetIndex: -1 }  // sufficiently different, add
}

/**
 * Update an existing memory's content and timestamp, reset tags for re-tagging.
 */
export function updateMemory(index: number, newContent: string) {
  if (index < 0 || index >= memoryState.memories.length) return
  const mem = memoryState.memories[index]
  const oldContent = mem.content
  // Bi-temporal version tracking
  createMemoryVersion(oldContent, newContent, mem.scope)
  // P1-#9: 语义版本化 — 保留旧版本
  if (!mem.history) mem.history = []
  mem.history.push({ content: oldContent, ts: mem.ts })
  if (mem.history.length > 5) mem.history.shift()

  // ── Information-Preserving Merge：保留旧内容中被覆盖的独特关键词 ──
  // update 直接替换 content 会丢失旧内容的关键信息（如 "adoption agencies"）
  // 提取旧内容中新内容不包含的实质性词汇，存为 _mergedKeywords 供 BM25 匹配
  const _MS = new Set(['the','and','that','this','was','for','are','but','not','you','all','can','had','her','one','our','out','day','get','has','him','his','how','its','new','now','see','way','who','did','got','say','she','too','use','with','been','from','have','just','like','make','more','much','some','than','them','then','they','very','what','when','will','your','about','after','could','first','great','into','most','over','such','take','their','these','those','time','want','would','also','back','come','each','find','give','going','good','here','know','last','long','look','made','need','only','said','tell','went','were','well','work','really','think','because','where','there'])
  const _oldW = new Set(((oldContent || '').toLowerCase().match(/[a-z]{4,}/g) || []).filter(w => !_MS.has(w)))
  const _newW = new Set((newContent.toLowerCase().match(/[a-z]{4,}/g) || []).filter(w => !_MS.has(w)))
  const _lost: string[] = []
  for (const w of _oldW) { if (!_newW.has(w)) _lost.push(w) }
  if (_lost.length > 0) {
    (mem as any)._mergedKeywords = ((mem as any)._mergedKeywords || []).concat(_lost).slice(-10)
  }

  mem.content = newContent
  mem.ts = Date.now()
  mem.lastAccessed = Date.now()
  mem.tags = undefined // re-tag on next cycle

  // 溯源链：记录 reshape
  try {
    // appendLineage imported at top level
    const delta = newContent.length > oldContent.length
      ? `+${newContent.replace(oldContent, '').slice(0, 40)}`
      : `~${newContent.slice(0, 40)}`
    appendLineage(mem, { action: 'reshaped', ts: Date.now(), delta })
  } catch {}

  invalidateIDF()
  invalidateFieldIDF()
  rebuildScopeIndex()
  saveMemories()

  // Async re-tag
  if (newContent.length > 10) {
    queueForTagging(newContent, mem.ts, index)
  }
  console.log(`[cc-soul][memory] updated: "${oldContent.slice(0, 40)}" → "${newContent.slice(0, 40)}"`)
}

// ═══════════════════════════════════════════════════════════════════════════════
// Retroactive Interference — new memories reshape (not just suppress) similar old memories
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * 记忆干涉演化：新信息重塑旧记忆而非替换
 * 基于 Retroactive Interference Theory
 */
function retroactiveInterference(oldMem: Memory, newContent: string, similarity: number): boolean {
  // 只对中等相似度的记忆做干涉（太相似=重复，太不相似=无关）
  if (similarity < 0.3 || similarity > 0.85) return false
  // 只对 fact 和 preference 做干涉
  if (oldMem.scope !== 'fact' && oldMem.scope !== 'preference') return false

  // 提取新旧记忆的差异部分
  const oldWords = new Set((oldMem.content.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map(w => w.toLowerCase()))
  const newWords = new Set((newContent.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map(w => w.toLowerCase()))

  // 找出新增的关键词
  const addedWords: string[] = []
  for (const w of newWords) {
    if (!oldWords.has(w)) addedWords.push(w)
  }

  if (addedWords.length === 0) return false

  // 保存原文到 history
  if (!oldMem.history) oldMem.history = []
  if (oldMem.history.length < 5) {
    oldMem.history.push({ content: oldMem.content, ts: Date.now() })
  }

  // 重塑：在旧记忆后面追加新条件/补充
  const supplement = addedWords.slice(0, 3).join('、')
  oldMem.content = `${oldMem.content}（补充：${supplement}）`
  oldMem.confidence = Math.max(0.3, (oldMem.confidence ?? 0.7) * 0.85) // 置信度轻微降低
  oldMem.ts = Date.now() // 更新时间戳（重塑=部分重建）

  console.log(`[cc-soul][interference] reshaped: "${oldMem.content.slice(0, 50)}" (+${supplement})`)
  return true
}

/**
 * Memory Metabolism — 记忆代谢
 *
 * When a new memory shares entities with an existing memory but has complementary
 * (non-conflicting) facts, the old memory ABSORBS the new info instead of storing
 * two separate memories.
 *
 * Actions:
 *   ABSORB:      shared entity + different predicates → old memory absorbs new facts
 *   SUPERSEDE:   already handled by existing conflict resolution — skip
 *   CRYSTALLIZE: same entity appears in ≥3 recent memories → trigger trait crystallization
 *   PASS:        no relation → normal write
 */
interface MetabolismAction {
  action: 'ABSORB' | 'SUPERSEDE' | 'CRYSTALLIZE' | 'PASS'
  target?: Memory
  newFacts?: any[]
  entity?: string
}

function metabolize(newContent: string, memories: Memory[]): MetabolismAction {
  let extractFn: any
  try { extractFn = require('./fact-store.ts').extractFacts } catch { return { action: 'PASS' } }

  const newFacts = extractFn(newContent)
  if (newFacts.length === 0) return { action: 'PASS' }

  const newEntities = new Set(newFacts.map((f: any) => f.subject).concat(newFacts.map((f: any) => f.object)))

  // Scan recent 30 memories for shared entities
  const recent = memories.slice(-30).filter(m => m.scope !== 'expired' && m.scope !== 'decayed')

  for (const old of recent) {
    const oldFacts = extractFn(old.content)
    if (oldFacts.length === 0) continue

    // Find shared entities
    const oldEntities = new Set(oldFacts.map((f: any) => f.subject).concat(oldFacts.map((f: any) => f.object)))
    const shared = [...newEntities].filter(e => oldEntities.has(e))
    if (shared.length === 0) continue

    // Check for predicate conflict (SUPERSEDE) — already handled by existing conflict resolution
    const hasConflict = newFacts.some((nf: any) =>
      oldFacts.some((of: any) => of.subject === nf.subject && of.predicate === nf.predicate && of.object !== nf.object)
    )
    if (hasConflict) continue  // Let existing SUPERSEDE logic handle it

    // Check for complementary facts (ABSORB)
    const complement = newFacts.filter((nf: any) =>
      !oldFacts.some((of: any) => of.subject === nf.subject && of.predicate === nf.predicate)
    )
    if (complement.length > 0) {
      return { action: 'ABSORB', target: old, newFacts: complement }
    }
  }

  // Check for CRYSTALLIZE: same entity in ≥3 recent memories
  for (const e of newEntities) {
    let count = 0
    for (const m of recent) {
      if (m.content.includes(e as string)) count++
    }
    if (count >= 3) {
      return { action: 'CRYSTALLIZE', entity: e as string }
    }
  }

  return { action: 'PASS' }
}

/**
 * When a new fact/preference/correction is added, suppress or reshape
 * similar older memories. This prevents the 60K memory pile-up.
 *
 * Online semantic complement marking — 写入时标记互补候选
 * 条件 A: 共享实体 + 30 分钟内时间邻近
 * 条件 B: 中等 trigram 相似度(0.2-0.6) + 实体重叠
 * heartbeat 消费 _complementOf 做深度融合
 */
function markComplementCandidates(newMem: Memory, memories: Memory[], maxCandidates: number = 3): void {
  if (memories.length === 0 || !newMem.memoryId) return

  let newEntities: Set<string>
  try {
    const { findMentionedEntities } = require('./graph.ts')
    newEntities = new Set(findMentionedEntities(newMem.content))
  } catch { return }
  if (newEntities.size === 0) return

  const now = Date.now()
  const THIRTY_MIN = 30 * 60 * 1000
  const candidates: string[] = []

  // Only scan recent 50 memories (performance protection)
  const recent = memories.slice(-50)

  for (const m of recent) {
    if (!m.memoryId || m.content === newMem.content) continue
    if (m.scope === 'expired' || m.scope === 'decayed') continue

    // Condition A: shared entities + time proximity
    let mEntities: Set<string>
    try {
      const { findMentionedEntities } = require('./graph.ts')
      mEntities = new Set(findMentionedEntities(m.content))
    } catch { continue }

    let sharedEntities = 0
    for (const e of newEntities) { if (mEntities.has(e)) sharedEntities++ }

    const timeDiff = Math.abs(now - m.ts)

    if (sharedEntities >= 1 && timeDiff < THIRTY_MIN) {
      candidates.push(m.memoryId)
      if (candidates.length >= maxCandidates) break
      continue
    }

    // Condition B: medium trigram similarity + entity overlap
    const sim = trigramSimilarity(trigrams(newMem.content), trigrams(m.content))
    if (sim >= 0.2 && sim < 0.6 && sharedEntities >= 1) {
      candidates.push(m.memoryId)
      if (candidates.length >= maxCandidates) break
    }
  }

  if (candidates.length > 0) {
    newMem._complementOf = candidates
    try { require('./decision-log.ts').logDecision('complement_mark', newMem.content.slice(0, 30), `candidates=${candidates.length}, entities=${[...newEntities].join('/')}`) } catch {}
  }
}

/**
 * Mechanism: trigram similarity > 0.6 with same scope →
 *   1. Try retroactive interference (reshape) for medium similarity (0.3-0.85)
 *   2. Fall back to confidence penalty if reshape not applicable
 * If confidence drops below 0.2 → mark as expired (effectively forgotten).
 * Only suppresses memories older than 1 hour (avoid self-interference).
 */
function suppressSimilarMemories(newMem: Memory) {
  const newTri = trigrams(newMem.content)
  const MIN_AGE_MS = 3600000 // 1 hour — don't suppress very recent memories
  let suppressed = 0
  let reshaped = 0

  const startIdx = Math.max(0, memoryState.memories.length - 500)
  for (let i = startIdx; i < memoryState.memories.length - 1; i++) { // -1 to skip the just-added one
    const old = memoryState.memories[i]
    if (old.scope === 'expired' || old.scope === 'archived') continue
    if (old.content === newMem.content) continue
    if (Date.now() - old.ts < MIN_AGE_MS) continue

    // Only suppress within same or related scopes
    const relatedScope = old.scope === newMem.scope ||
      (newMem.scope === 'correction' && old.scope === 'fact') ||
      (newMem.scope === 'fact' && old.scope === 'fact')
    if (!relatedScope) continue

    const oldTri = trigrams(old.content)
    const sim = trigramSimilarity(newTri, oldTri)

    if (sim > 0.6) {
      const oldContent = old.content // 记住旧 content 用于 SQLite 查找
      // 先尝试 retroactive interference（重塑而非压制）
      const wasReshaped = retroactiveInterference(old, newMem.content, sim)
      if (wasReshaped) {
        reshaped++
        // reshaped 后 old.content 已变，需用旧 content 查 SQLite 再更新
        if (useSQLite) {
          const found = sqliteFindByContent(oldContent)
          if (found) sqliteUpdateMemory(found.id, { content: old.content, confidence: old.confidence, ts: old.ts } as any)
        }
      } else {
        // 如果没有被重塑（不适用），维持原有的 confidence 降低
        bayesPenalize(old, 1.5)  // interference suppression: β += 1.5
        if (old.confidence < 0.2) {
          old.scope = 'expired'
          console.log(`[cc-soul][interference] expired: "${old.content.slice(0, 50)}" (suppressed by new memory)`)
        }
        suppressed++
        syncToSQLite(old, { confidence: old.confidence, scope: old.scope })
      }
      if (suppressed + reshaped >= 5) break // cap per new memory
    }
  }

  if (suppressed > 0 || reshaped > 0) {
    console.log(`[cc-soul][interference] ${suppressed} suppressed, ${reshaped} reshaped`)
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// Memory CRUD
// ═══════════════════════════════════════════════════════════════════════════════

export function loadMemories() {
  _memoriesLoaded = true
  // Try SQLite first, fall back to JSON
  const sqliteOk = initSQLite()
  _sqliteInitDone = true
  if (sqliteOk) {
    // migrateFromJSON() — 独立数据库模式，不从 JSON 导入旧数据
    // migrateHistoryFromJSON(HISTORY_PATH) — 独立数据库模式，不从 JSON 导入旧历史

    // Load from SQLite — if empty, fall back to JSON (migration may have failed)
    const fromDb = sqliteGetAll(true)
    if (fromDb.length > 0) {
      useSQLite = true
      memoryState.memories.length = 0
      memoryState.memories.push(...fromDb)
    } else {
      // SQLite empty — 始终用 SQLite（独立数据库模式，不回退到 JSON）
      useSQLite = true
      console.log(`[cc-soul][memory] SQLite empty, starting fresh (independent db mode)`)
    }

    const historyFromDb = sqliteGetRecentHistory(MAX_HISTORY)
    memoryState.chatHistory.length = 0
    memoryState.chatHistory.push(...historyFromDb)

    console.log(`[cc-soul][memory] loaded ${fromDb.length} memories from SQLite`)

    // vector embedder removed — activation field handles semantic recall
  } else {
    // JSON fallback
    const loaded = loadJson<Memory[]>(MEMORIES_PATH, [])
    memoryState.memories.length = 0
    memoryState.memories.push(...loaded)

    const loadedHistory = loadJson<ChatTurn[]>(HISTORY_PATH, [])
    memoryState.chatHistory.length = 0
    memoryState.chatHistory.push(...loadedHistory)

    console.log(`[cc-soul][memory] loaded ${loaded.length} memories from JSON (SQLite unavailable)`)
  }

  // One-time fix: repair ts=0 memories on load
  let repaired = 0
  const loadNow = Date.now()
  for (const mem of memoryState.memories) {
    if (!mem.ts || mem.ts === 0) {
      mem.ts = mem.lastAccessed || (loadNow - Math.random() * 30 * 86400000)
      repaired++
    }
  }
  if (repaired > 0) {
    console.log(`[cc-soul][memory] repaired ${repaired} memories with ts=0`)
    saveMemories()
  }

  // One-time recovery: re-evaluate decayed memories after ts repair
  // Memories were wrongly decayed because ts=0 made age appear infinite
  const RECOVERY_FLAG = resolve(DATA_DIR, '.decay_recovered')
  if (!existsSync(RECOVERY_FLAG)) {
    let recovered = 0
    for (const mem of memoryState.memories) {
      if (mem.scope === 'decayed' && mem.ts > 0) {
        const age = Date.now() - mem.ts
        if (age < 90 * 86400000) {
          mem.scope = 'mid_term'
          mem.tier = 'mid_term'
          recovered++
        }
      }
    }
    if (recovered > 0) {
      console.log(`[cc-soul][memory] recovered ${recovered} wrongly-decayed memories`)
      saveMemories()
    }
    try { writeFileSync(RECOVERY_FLAG, Date.now().toString()) } catch (e: any) { console.error(`[cc-soul][memory] failed to write recovery flag: ${e.message}`) }
  }

  rebuildScopeIndex()
  rebuildRecallIndex(memoryState.memories)
}

export function saveMemories() {
  // Safety: never overwrite a non-empty file with an empty array
  if (memoryState.memories.length === 0) {
    try {
      const { size } = statSync(MEMORIES_PATH)
      if (size > 2) {
        console.error(`[cc-soul][memory] BLOCKED: refusing to overwrite ${size}-byte file with empty array`)
        return
      }
    } catch { /* file doesn't exist, ok to write */ }
  }
  // JSON 双写已移除——SQLite 是唯一数据源（memories 表）
}

// defaultVisibility + extractReasoning → memory-utils.ts

/**
 * Create a new version of an existing memory (bi-temporal update).
 * Old version gets validUntil=now, new version gets validFrom=now.
 * Preserves version chain in history field.
 */
export function createMemoryVersion(oldContent: string, newContent: string, scope?: string) {
  const existing = memoryState.memories.find(m =>
    m.content === oldContent && m.scope !== 'expired' && (!m.validUntil || m.validUntil === 0)
  )
  if (!existing) {
    // No existing memory found, just add new one
    addMemory(newContent, scope || 'fact')
    return
  }

  // Close old version
  existing.validUntil = Date.now()

  // Carry forward history chain
  const history = [...(existing.history || [])]
  history.push({ content: existing.content, ts: existing.ts })
  // Limit history to 10 versions
  if (history.length > 10) history.splice(0, history.length - 10)

  // Create new version
  const newMem: Memory = {
    content: newContent,
    scope: existing.scope,
    ts: Date.now(),
    userId: existing.userId,
    visibility: existing.visibility,
    channelId: existing.channelId,
    confidence: existing.confidence ?? 0.7,
    lastAccessed: Date.now(),
    tier: existing.tier || 'short_term',
    recallCount: 0,
    validFrom: Date.now(),
    validUntil: 0,
    tags: existing.tags,
    history,
  }
  memoryState.memories.push(newMem)
  if (useSQLite) { sqliteAddMemory(newMem) }
  saveMemories()

}

/**
 * Query memory timeline: what was the state of a fact at a given point in time?
 */
export function queryMemoryTimeline(keyword: string): { content: string; from: number; until: number | null }[] {
  const results: { content: string; from: number; until: number | null }[] = []
  for (const mem of memoryState.memories) {
    if (!mem.content.toLowerCase().includes(keyword.toLowerCase())) continue
    if (typeof mem.validFrom === 'number') {
      results.push({
        content: mem.content,
        from: mem.validFrom,
        until: (mem.validUntil && mem.validUntil > 0) ? mem.validUntil : null,
      })
    }
    // Also check history chain
    if (mem.history) {
      for (const h of mem.history) {
        if (h.content.toLowerCase().includes(keyword.toLowerCase())) {
          results.push({ content: h.content, from: h.ts, until: mem.validFrom || mem.ts })
        }
      }
    }
  }
  results.sort((a, b) => b.from - a.from) // newest first
  return results
}

// detectMemoryPoisoning → memory-utils.ts

// ── #15 记忆图谱化：自动在新记忆和最近记忆之间建立关系边 ──
function autoLinkMemories(newMem: Memory) {
  const recent = memoryState.memories.slice(-6, -1) // 最近5条（不含自己）
  if (recent.length === 0) return
  const newTri = trigrams(newMem.content)
  const newLabel = newMem.content.slice(0, 20)
  for (const old of recent) {
    const oldTri = trigrams(old.content)
    const overlap = trigramSimilarity(newTri, oldTri)
    // 因果关系：新记忆包含因果关键词 + 话题重叠
    if (/因为|所以|导致|结果|于是|because|therefore/.test(newMem.content) && overlap > 0.15) {
      addRelation(newLabel, old.content.slice(0, 20), 'caused_by')
      continue // 一条旧记忆只建一种关系
    }
    // 矛盾关系：correction 覆盖 fact，内容高度相似
    if (newMem.scope === 'correction' && old.scope === 'fact' && overlap > 0.3) {
      addRelation(newLabel, old.content.slice(0, 20), 'contradicts')
      continue
    }
    // 时序关系：同一话题、时间间隔 < 5分钟
    if (Math.abs(newMem.ts - (old.ts || 0)) < 300000 && overlap > 0.2) {
      addRelation(newLabel, old.content.slice(0, 20), 'follows')
    }
  }
}

/**
 * 预期违背编码：只有出乎预料的信息才值得记忆
 * 基于 Predictive Coding Theory (Friston 2005)
 */
function computeSurprise(content: string, scope: string, _userId?: string): number {
  let score = 5 // 默认中等

  // 身份信息 → 高 surprise（重要但稀少）
  if (/名字|叫我|职业|住在|工作|年龄|生日|毕业|my name|call me|i work|i live|birthday|graduated|i'm a/i.test(content)) score = 9
  // 偏好信息 → 中高
  if (/喜欢|讨厌|偏好|习惯|最爱|受不了|i like|i love|i hate|i prefer|i enjoy|favorite|can't stand/i.test(content)) score = 7
  // 英文个人经历 → 至少中等（"I went/did/have/had/made/took"）
  if (/\bi (went|did|have|had|made|took)\b/i.test(content)) score = Math.max(score, 4)
  // 纠正 → 高（意味着之前的理解错了）
  if (scope === 'correction') score = 8
  // 情绪爆发 → 高
  if (/[！!]{2,}|卧槽|崩溃|太开心|难受|焦虑|omg|fuck|shit|so happy|breaking down|anxious/i.test(content)) score += 2
  // 时效性信息 → 降级（中文时效词 -2，英文时效词只 -1 避免过度惩罚）
  if (/今天|刚才|现在|刚刚/i.test(content)) score -= 2
  if (/today|just now|right now|earlier today/i.test(content)) score -= 1
  // 常见寒暄/无信息量回复 → 极低
  if (/^(你好|嗯+|好的?|谢谢|哈哈+|ok|行吧?|收到|了解|明白|可以|没问题|好吧|哦+|是的?|嗯嗯|对的?|没事|算了|随便|都行|无所谓|不用了?|知道了)$/i.test(content.trim())) score = 1
  // 日常闲聊/无决策价值 → 降级
  if (/^.{0,15}(天气|堵车|迟到|周[一二三四五六日末]|终于.*休息|几点了|现在几点|路上)/.test(content) && content.length < 25) score = Math.min(score, 2)
  // 短内容 → 降级
  if (content.length < 10) score -= 1
  // 极短且无实质内容 → 直接最低
  if (content.length <= 4 && !/[a-zA-Z]{3,}/.test(content)) score = 1

  return Math.max(1, Math.min(10, score))
}

// ═══════════════════════════════════════════════════════════════════════════════
// Coreference Resolution（指代消解）— 写入时将代词替换为实体名
// 人脑原理：存入长期记忆时自动补全上下文，不会存"他说了什么"而不知道他是谁
// ═══════════════════════════════════════════════════════════════════════════════

/** 代词→实体名替换（句首 / 逗号后） */
const COREF_PRONOUN_VERB = /(^|[，,])(他|她)(说|让|要|觉得|认为|提到|问|给|跟)/g
/** 指示代词→实体名 */
const COREF_DEMONSTRATIVE = /(这个人|那个人|那家伙)/g
/** 复数代词 → 不处理 */
const COREF_PLURAL = /他们|她们/

function resolveCoreferenceForStorage(
  content: string,
  chatHistory: { user: string; assistant?: string }[],
): { resolved: string; changed: boolean; resolvedEntity?: string } {
  // 复数代词 → 跳过
  if (COREF_PLURAL.test(content)) {
    return { resolved: content, changed: false }
  }
  // 没有需要消解的代词 → 跳过
  if (!COREF_PRONOUN_VERB.test(content) && !COREF_DEMONSTRATIVE.test(content)) {
    return { resolved: content, changed: false }
  }
  // Reset lastIndex after test()
  COREF_PRONOUN_VERB.lastIndex = 0
  COREF_DEMONSTRATIVE.lastIndex = 0

  // 从最近 3 轮对话中提取人物实体
  let entities: string[] = []
  try {
    const { findMentionedEntities: fme } = require('./graph.ts')
    const recentText = chatHistory.slice(-3).map(h => h.user + (h.assistant || '')).join(' ')
    entities = fme(recentText)
  } catch {}

  // 安全规则：恰好 1 个人物实体才替换，0 或 2+ 不动
  if (entities.length !== 1) {
    return { resolved: content, changed: false }
  }

  const entity = entities[0]
  let resolved = content
    .replace(COREF_PRONOUN_VERB, (_, prefix, _pronoun, verb) => `${prefix}${entity}${verb}`)
    .replace(COREF_DEMONSTRATIVE, entity)

  // Reset lastIndex
  COREF_PRONOUN_VERB.lastIndex = 0
  COREF_DEMONSTRATIVE.lastIndex = 0

  const changed = resolved !== content
  if (changed) {
    try { require('./decision-log.ts').logDecision('coreference', content.slice(0, 40), `→ ${entity}: ${resolved.slice(0, 60)}`) } catch {}
  }
  return { resolved, changed, resolvedEntity: changed ? entity : undefined }
}

export function addMemory(content: string, scope: string, userId?: string, visibility?: 'global' | 'channel' | 'private', channelId?: string, situationCtx?: Memory['situationCtx'], skipAutoExtract?: boolean) {
  // Check skip flag from session (inclusion/exclusion control)
  try {
    const mod = getLazyModule('handler-state'); const getSessionState = mod?.getSessionState; const getLastActiveSessionKey = mod?.getLastActiveSessionKey
    const sess = getSessionState(getLastActiveSessionKey())
    if (sess?._skipNextMemory) {
      sess._skipNextMemory = false
      console.log('[cc-soul][memory] skipped by user request (别记这个)')
      return
    }
  } catch {}

  if (!content || content.length < 3) return

  // ── 排除性设计：What NOT to save（学自 Claude Code memdir）──
  // 纯确认性回复、临时信息、太短无信息量的内容不值得存储
  const REJECT_CONTENT_PATTERNS = [
    /^(嗯|好的?|ok|收到|谢谢|thx|thanks|明白|懂了|了解|got it|知道了|可以|行|对|没问题|好吧)[\s。！!.]*$/i,
    /^.{0,4}$/,  // 太短（<5字）无信息量
  ]
  if (scope !== 'correction' && scope !== 'preference') {
    for (const pat of REJECT_CONTENT_PATTERNS) {
      if (pat.test(content.trim())) {
        return  // 静默拒绝，不打日志（太频繁）
      }
    }
  }

  // ── scope 白名单验证（学自 Claude Code 闭合分类法）──
  const VALID_SCOPES = new Set([
    'preference', 'fact', 'event', 'opinion', 'topic', 'correction',
    'consolidated', 'discovery', 'task', 'reflexion', 'gratitude',
    'visual', 'dream', 'curiosity', 'reflection', 'proactive', 'insight',
  ])
  if (!VALID_SCOPES.has(scope)) scope = 'fact'  // 未知 scope 降级为 fact

  // ── 写入去重互斥（学自 Claude Code extractMemories UUID 游标）──
  const dedupeKey = content.slice(0, 60) + '|' + scope
  if (_recentWriteHashes.has(dedupeKey)) return  // 5 分钟内相同内容不重复存
  _recentWriteHashes.add(dedupeKey)
  if (_recentWriteHashes.size > 500) {
    // 防止集合无限增长
    const iterator = _recentWriteHashes.values()
    // Set 没有 shift，用 clear + 重建（保留最近 400 个）
    const remaining = [..._recentWriteHashes].slice(-400)
    _recentWriteHashes.clear()
    for (const k of remaining) _recentWriteHashes.add(k)
  }

  // Reject system augment content that was accidentally fed back as memory
  const SYSTEM_PREFIXES = ['[Working Memory', '[当前面向:', '[隐私模式]', '[System]', '[安全警告]', '[元认知警告]']
  if (SYSTEM_PREFIXES.some(p => content.includes(p))) {
    console.log(`[cc-soul][memory-crud] REJECT (system augment): ${content.slice(0, 60)}`)
    return
  }

  // Memory integrity check: reject suspicious content (poisoning defense)
  if (detectMemoryPoisoning(content)) {
    console.log(`[cc-soul][memory-integrity] REJECT (poisoning pattern): ${content.slice(0, 60)}`)
    return
  }

  // Smart dedup: decide add/update/skip based on trigram similarity
  const decision = decideMemoryAction(content, scope)
  if (decision.action === 'skip') {
    console.log(`[cc-soul][memory-crud] SKIP (duplicate): ${content.slice(0, 60)}`)
    return
  }
  if (decision.action === 'update') {
    console.log(`[cc-soul][memory-crud] UPDATE #${decision.targetIndex}: ${content.slice(0, 60)}`)
    updateMemory(decision.targetIndex, content)
    return
  }

  // ── 写入时冲突解决 + 事实版本链（Mem0 借鉴 + Zep 启发，零 LLM）──
  // supersede: 排他性谓语变化 → 建版本链（旧→historical）
  // supplement: 非排他性 → 旧的 reshape 降权
  let _supersededMemId: string | undefined
  try {
    const { extractFacts, queryFacts } = require('./fact-store.ts')
    // classifyConflict imported at top level
    const newFacts = extractFacts(content)
    for (const f of newFacts) {
      const existing = queryFacts({ subject: f.subject, predicate: f.predicate })
      if (existing.length > 0 && existing[0].object !== f.object) {
        if (existing[0].ts && Date.now() < existing[0].ts) continue
        const oldMem = memoryState.memories.find((m: any) => m.content && m.content.includes(existing[0].object))
        if (!oldMem) continue

        const conflictType = classifyConflict([{ subject: f.subject, predicate: f.predicate, object: existing[0].object }], [f])

        if (conflictType === 'supersede') {
          // 排他性取代 → 建版本链
          _supersededMemId = oldMem.memoryId
          oldMem.supersededBy = 'pending'  // 新记忆创建后回填
          oldMem.scope = 'historical'
          try {
            // appendLineage imported at top level
            appendLineage(oldMem, { action: 'superseded', ts: Date.now(), delta: `被取代: ${f.object} 替代 ${existing[0].object}` })
          } catch {}
          try { const { logDecision } = require('./decision-log.ts'); logDecision('supersede', (oldMem.content||'').slice(0,30), `${f.predicate}: ${existing[0].object}→${f.object}`) } catch {}
        } else {
          // 非排他性 → 降权（保留原有行为）
          try {
            const { penalizeTruthfulness } = require('./smart-forget.ts')
            penalizeTruthfulness(oldMem, `被新事实补充: ${f.object}`)
          } catch {}
        }
      }
    }
  } catch {}

  // ── Surprise-Only Encoding (Predictive Coding Theory, Friston 2005) ──
  // 只有出乎预料的信息才值得记忆
  const surprise = computeSurprise(content, scope, userId)
  if (surprise <= 1 && scope !== 'correction' && scope !== 'preference') {
    console.log(`[cc-soul][memory-crud] SKIP (low surprise=${surprise}): ${content.slice(0, 60)}`)
    return // 太平凡了，不存储
  }

  // Auto-attach current emotional state to every memory
  let autoSituationCtx = situationCtx
  if (!autoSituationCtx) {
    try {
      const bodyMod = getLazyModule('body'); const body = bodyMod?.body
      if (body && typeof body.mood === 'number') {
        autoSituationCtx = { mood: body.mood, energy: body.energy }
      }
    } catch {}
  }

  // ── S4: Temporal Fact Anchoring — 写入时解析相对时间→绝对时间 ──
  // Zep 双时间模型启发：event time T（事件发生时间）vs ingestion time T'（录入时间）
  // ts = 录入时间，validFrom = 事件实际发生时间（如果能解析）
  let _eventTime: number | undefined
  try {
    const now = Date.now()
    const DAY = 86400000
    const text = content
    // 中文
    if (/昨天/.test(text)) _eventTime = now - DAY
    else if (/前天/.test(text)) _eventTime = now - 2 * DAY
    else if (/上周/.test(text)) _eventTime = now - 7 * DAY
    else if (/上个月/.test(text)) _eventTime = now - 30 * DAY
    else if (/去年/.test(text)) _eventTime = now - 365 * DAY
    else {
      const cnDays = text.match(/(\d+)\s*天前/); if (cnDays) _eventTime = now - parseInt(cnDays[1]) * DAY
      const cnMonths = text.match(/(\d+)\s*个月前/); if (cnMonths) _eventTime = now - parseInt(cnMonths[1]) * 30 * DAY
    }
    // 英文
    if (!_eventTime) {
      if (/yesterday/i.test(text)) _eventTime = now - DAY
      else if (/last\s+week/i.test(text)) _eventTime = now - 7 * DAY
      else if (/last\s+month/i.test(text)) _eventTime = now - 30 * DAY
      else if (/last\s+year/i.test(text)) _eventTime = now - 365 * DAY
      else {
        const enAgo = text.match(/(\d+)\s+(days?|weeks?|months?|years?)\s+ago/i)
        if (enAgo) {
          const n = parseInt(enAgo[1])
          const u = enAgo[2].toLowerCase()
          if (u.startsWith('day')) _eventTime = now - n * DAY
          else if (u.startsWith('week')) _eventTime = now - n * 7 * DAY
          else if (u.startsWith('month')) _eventTime = now - n * 30 * DAY
          else if (u.startsWith('year')) _eventTime = now - n * 365 * DAY
        }
      }
    }
  } catch {}

  const resolvedVisibility = visibility || defaultVisibility(scope)
  const newIndex = memoryState.memories.length
  const FACT_SCOPES = ['fact', 'preference', 'correction', 'discovery']

  // Auto-detect memory source: user_said (from user message), ai_inferred (from LLM analysis), system
  const autoSource: Memory['source'] =
    scope === 'correction' || scope === 'preference' || scope === 'gratitude' ? 'user_said'
    : scope === 'fact' || scope === 'event' || scope === 'visual' ? 'ai_observed'
    : scope === 'reflexion' || scope === 'curiosity' || scope === 'dream' ? 'ai_inferred'
    : 'system'
  // ── Hindsight 认知网络自动分类（必须在 autoSource 之后）──
  const autoNetwork: Memory['network'] =
    (scope === 'fact' && !/用户|我|你/.test(content)) ? 'world'
    : (scope === 'preference' || /喜欢|讨厌|觉得|偏好/.test(content)) ? 'opinion'
    : (scope === 'event' || autoSource === 'ai_observed') ? 'experience'
    : undefined
  // Auto-detect emotional intensity from emotion tag + scope
  const autoEmotionIntensity =
    content.includes('！') || content.includes('!') ? 0.8
    : scope === 'correction' ? 0.7  // corrections are emotionally significant
    : scope === 'gratitude' ? 0.6
    : 0.3  // default low intensity
  // ── 生成效应 (Generation Effect, Slamecka 1978) ──
  // 用户主动说出的 → 更高初始 confidence
  // AI 推断的 → 标准 confidence
  // 系统自动生成的 → 较低 confidence
  const generationBoost =
    (autoSource === 'user_said' || scope === 'preference' || scope === 'correction') ? 0.85  // 用户主动表达
    : (autoSource === 'ai_observed' || scope === 'fact') ? 0.7                                // AI 观察到的
    : (scope === 'reflexion' || scope === 'insight' || scope === 'consolidated') ? 0.6        // 系统生成的
    : 0.7  // 默认

  // ── 指代消解：写入前将"他/她"替换为实体名 ──
  let _corefHistory: { content: string; ts: number }[] | undefined
  const corefResult = resolveCoreferenceForStorage(content, memoryState.chatHistory)
  if (corefResult.changed) {
    _corefHistory = [{ content, ts: Date.now() }]  // 保存原文
    content = corefResult.resolved
  }

  // LLM fallback for coreference: if regex didn't resolve and content has pronouns
  const _corefContent = content  // capture for async closure
  if (!corefResult.changed && /他|她|它|这个|那个/.test(content)) {
    try {
      const { hasLLM, spawnCLI } = require('./cli.ts')
      if (hasLLM()) {
        const recentContext = memoryState.chatHistory.slice(-3).map(h => h.user).join('\n')
        spawnCLI(
          `上下文：\n${recentContext}\n\n当前句子："${_corefContent}"\n\n请把句子中的代词（他/她/它/这个/那个）替换为具体的人名或事物名。只输出替换后的句子，不要解释。如果无法确定指代，原样输出。`,
          (output: string) => {
            if (!output || output.length < 3) return
            const resolved = output.trim().split('\n')[0]  // take first line only
            // Update the memory that was just stored
            const mem = memoryState.memories.find(m => m.content === _corefContent && Math.abs(m.ts - Date.now()) < 5000)
            if (mem && resolved !== _corefContent) {
              if (!mem.history) mem.history = []
              mem.history.push({ content: mem.content, ts: Date.now() })
              mem.content = resolved
              // Sync to SQLite (use old content _corefContent to find the record, then update)
              try {
                const { sqliteFindByContent, sqliteUpdateMemory } = require('./sqlite-store.ts')
                const found = sqliteFindByContent(_corefContent)
                if (found) sqliteUpdateMemory(found.id, { content: resolved })
              } catch {}
              try { updateRecallIndex(mem) } catch {}
              try { require('./decision-log.ts').logDecision('coreference_llm', resolved.slice(0, 30), `original: ${_corefContent.slice(0, 30)}`) } catch {}
            }
          },
          10000
        )
      }
    } catch {}
  }

  // generateMemoryId, appendLineage imported at top level

  const newMem: Memory = {
    memoryId: generateMemoryId(),
    content, scope, ts: Date.now(), userId, visibility: resolvedVisibility, channelId,
    bayesAlpha: BAYES_DEFAULT_ALPHA, bayesBeta: BAYES_DEFAULT_BETA,
    confidence: generationBoost,
    lastAccessed: Date.now(),
    tier: 'short_term',
    recallCount: 0,
    lineage: [{ action: 'created', ts: Date.now(), trigger: autoSource, delta: scope }],
    source: autoSource,
    network: autoNetwork,
    emotionIntensity: autoEmotionIntensity,
    importance: surprise,
    ...(FACT_SCOPES.includes(scope) ? { validFrom: _eventTime || Date.now(), validUntil: 0 } : {}),
    ...(!FACT_SCOPES.includes(scope) && _eventTime ? { validFrom: _eventTime } : {}),
    ...extractReasoning(content),
    ...(autoSituationCtx ? { situationCtx: autoSituationCtx } : {}),
    ...(_corefHistory ? { history: _corefHistory } : {}),
    _segmentId: getCurrentSegmentId(),
  }
  // ── 前瞻性标签（Prospective Tags）：AAM 预测未来查询词（零 LLM doc2query）──
  try {
    const { expandQuery } = require('./aam.ts')
    const _ptWords = (content.match(/[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}/gi) || []).slice(0, 5)
    if (_ptWords.length >= 2) {
      const _ptLower = content.toLowerCase()
      const _ptExpanded = expandQuery(_ptWords.map((w: string) => w.toLowerCase()), 10)
      const _ptThreshold = _ptExpanded.length < 3 ? 0.3 : 0.5
      const _ptTags = _ptExpanded
        .filter((e: any) => e.weight >= _ptThreshold && !_ptLower.includes(e.word) && e.word.length >= 2)
        .map((e: any) => e.word).slice(0, 8)
      if (_ptTags.length > 0) newMem.prospectiveTags = _ptTags
    }
  } catch {}

  // ── Write-time entity extraction（为 slotization 提供精确数据）──
  try {
    const _ents = require('./graph.ts').findMentionedEntities(content)
    if (_ents.length > 0) newMem._entityIds = _ents.slice(0, 10)
  } catch {}

  // ── 闪光灯记忆（Flashbulb Memory）：高情绪事件深度编码 ──
  // 人脑原理：极端情绪事件形成超详细记忆（911 你记得你在做什么）
  // cc-soul 原创：emotionIntensity ≥ 0.7 自动触发，零 LLM，存当时完整上下文
  if (autoEmotionIntensity >= 0.7) {
    let _bodyMod: any = null
    try { _bodyMod = require('./body.ts') } catch {}
    const recentCtx = memoryState.chatHistory.slice(-3).map(h => h.user.slice(0, 40)).join(' → ')
    let people: string[] = []
    try { people = require('./graph.ts').findMentionedEntities(content).slice(0, 5) } catch {}
    try { require('./decision-log.ts').logDecision('flashbulb', content.slice(0, 30), `emotionIntensity=${autoEmotionIntensity.toFixed(2)}, mood=${_bodyMod?.body?.mood?.toFixed(2) ?? '?'}`) } catch {}
    newMem.flashbulb = {
      surroundingContext: recentCtx || '(无上下文)',
      bodyState: { mood: _bodyMod?.body?.mood ?? 0, energy: _bodyMod?.body?.energy ?? 0.5 },
      mentionedPeople: people,
      detailLevel: 'full',
    }
  }

  // ── Decision causal recording: extract WHY from causal keywords ──
  const causalMatch = content.match(/(?:because|因为|由于|是因为|之所以.*?是|所以选.*?是因为)\s*[,，:：]?\s*(.{4,80}?)(?:[。.!！;；]|$)/i)
  if (causalMatch) newMem.because = causalMatch[1].trim()

  // ── 前瞻锚定（Prospective Anchoring）：检测前瞻信号并嵌入 Memory ──
  const PROSPECTIVE_PATTERNS: Array<{ detect: RegExp; trigger: string; action: string; days: number }> = [
    { detect: /下周.*面试|面试.*下周|interview.*next week|next week.*interview/i, trigger: '面试|紧张|准备|interview|nervous|prepare', action: '主动问面试准备得怎么样/ask about interview prep', days: 14 },
    { detect: /要出差|出差.*天|business trip|traveling for work/i, trigger: '出差|机场|酒店|business trip|airport|hotel', action: '问出差顺利吗/ask how the trip went', days: 14 },
    { detect: /deadline|截止|交付|due date/i, trigger: 'deadline|截止|进度|progress|due', action: '问项目进度/ask about progress', days: 14 },
    { detect: /搬家|要搬|moving house|relocating/i, trigger: '搬家|新房|地址|moving|new place|address', action: '问搬家顺利吗/ask how the move went', days: 30 },
    { detect: /考试|备考|exam|test prep/i, trigger: '考试|成绩|通过|exam|results|passed', action: '问考试结果/ask about exam results', days: 30 },
  ]
  for (const p of PROSPECTIVE_PATTERNS) {
    if (p.detect.test(content)) {
      newMem.prospective = { trigger: p.trigger, expiresAt: Date.now() + p.days * 86400000, action: p.action }
      break
    }
  }

  // ── Memory Metabolism: check if new memory should be absorbed into existing ──
  const metabolism = metabolize(content, memoryState.memories)
  if (metabolism.action === 'ABSORB' && metabolism.target && metabolism.newFacts) {
    // Absorb: append new facts to old memory
    const factStr = metabolism.newFacts.map((f: any) => `${f.predicate === 'likes' ? '喜欢' : f.predicate}${f.object}`).join('，')
    metabolism.target.content = `${metabolism.target.content}，${factStr}`.slice(0, 200)
    metabolism.target.ts = Date.now()
    metabolism.target.lastAccessed = Date.now()
    try { appendLineage(metabolism.target, { action: 'merged', ts: Date.now(), delta: `absorbed ${metabolism.newFacts.length} facts` }) } catch {}
    try { require('./decision-log.ts').logDecision('metabolism_absorb', metabolism.target.content.slice(0, 30), `absorbed ${metabolism.newFacts.length} facts`) } catch {}
    // 同步到 SQLite + 更新索引（P3 bug fix: 之前直接 return 导致索引不同步）
    syncToSQLite(metabolism.target, { content: metabolism.target.content, ts: metabolism.target.ts, lastAccessed: metabolism.target.lastAccessed })
    updateRecallIndex(metabolism.target)
    emitCacheEvent('memory_modified')
    saveMemories()
    return
  }
  if (metabolism.action === 'CRYSTALLIZE' && metabolism.entity) {
    try { require('./person-model.ts').crystallizeTraits?.() } catch {}
  }
  // PASS and SUPERSEDE: continue normal flow

  // ── 语义近似去重：新记忆与已有记忆 trigram 相似度 > 0.7 → 合并而非新增 ──
  // 解决"我住上海"和"我住在上海浦东"作为两条独立记忆互相竞争 top-3 的问题
  // 这是记忆池膨胀导致召回率下降（800条78%→1200条68%）的根因之一
  try {
    const { trigrams, trigramSimilarity } = require('./memory-utils.ts')
    const newTri = trigrams(content)
    for (const existing of memoryState.memories) {
      if (!existing.content || existing.scope === 'expired') continue
      const sim = trigramSimilarity(newTri, trigrams(existing.content))
      if (sim > 0.7) {
        // 高度相似 → 更新已有记忆而不是新增
        // 保留更长的版本（信息更丰富），更新时间戳
        if (content.length > existing.content.length) existing.content = content
        existing.ts = Date.now()
        existing.lastAccessed = Date.now()
        existing.confidence = Math.min(1.0, (existing.confidence ?? 0.7) + 0.05)  // 重复提及 → 更可信
        try { appendLineage(existing, { action: 'dedup_merged', ts: Date.now(), delta: `merged similar: ${content.slice(0, 30)}` }) } catch {}
        syncToSQLite(existing, { content: existing.content, ts: existing.ts, confidence: existing.confidence })
        updateRecallIndex(existing)
        console.log(`[cc-soul][memory-crud] dedup: merged into existing (sim=${sim.toFixed(2)}): ${content.slice(0, 40)}`)
        return  // 不新增，已合并到现有记忆
      }
    }
  } catch {}

  // 写入后才更新索引（学自 Claude Code strict write discipline）
  // SQLite 写入优先，失败则不更新内存索引
  if (useSQLite) {
    try {
      sqliteAddMemory(newMem)
    } catch (e: any) {
      console.error(`[cc-soul][memory-crud] SQLite write failed, skipping memory: ${e.message}`)
      return  // SQLite 写失败 → 不添加到内存，保持一致性
    }
  }

  memoryState.memories.push(newMem)
  updateRecallIndex(newMem)
  emitCacheEvent('memory_added')

  // 事实版本链：回填 supersedes 关系
  if (_supersededMemId && newMem.memoryId) {
    newMem.supersedes = _supersededMemId
    const oldMem = memoryState.memories.find((m: any) => m.memoryId === _supersededMemId)
    if (oldMem) oldMem.supersededBy = newMem.memoryId
    // 身份信息变更广播：通知各缓存层（如 L3、entity crystal）失效
    emitCacheEvent('identity_changed')
  }

  try {
    // #15 记忆图谱化：自动建立记忆间关系边
    try { autoLinkMemories(newMem) } catch {}

    // Auto-extract structured facts (Mem0-style key-value triples)
    // Skip when memories already come from LLM extraction (runPostResponseAnalysis)
    if (!skipAutoExtract) {
      try { autoExtractFromMemory(content, scope, autoSource) } catch {}
    }

    // AAM: 只从用户内容和事实学习，反思/分析/系统文本不进 AAM（避免风格污染）
    const _AAM_LEARN_SCOPES = new Set(['preference', 'fact', 'event', 'correction', 'topic', 'episode', 'opinion'])
    if (_AAM_LEARN_SCOPES.has(scope)) {
      try {
        import('./aam.ts').then(m => m.learnAssociation(content, autoEmotionIntensity)).catch(() => {})
      } catch {}
    }

    // ── N1: 质量分反向训练——correction 和最近召回记忆配对学习 ──
    // 用户纠正时，把纠正内容和最近被召回的记忆关键词建立关联
    // 注：ActivationTrace 没有 query 字段，用最近召回记忆的 content 近似
    if (scope === 'correction') {
      try {
        const { getRecentTrace } = require('./activation-field.ts')
        const trace = getRecentTrace?.()
        const recentMem = trace?.traces?.[0]?.memory?.content
        if (recentMem) {
          const recalledKw = (recentMem.match(/[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}/gi) || []).slice(0, 5)
          const correctKw = (content.match(/[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}/gi) || []).slice(0, 5)
          if (recalledKw.length > 0 && correctKw.length > 0) {
            import('./aam.ts').then(m => m.learnAssociation(recalledKw.join(' ') + ' ' + correctKw.join(' '), 1.0)).catch(() => {})
          }
        }
      } catch {}
    }

    // ── 即时冲突感知：检测新记忆是否和已有特征矛盾 ──
    // 例："用户不运动了" vs 已有"运动型" → 冲突 → 更新旧记忆
    try {
      const CONFLICT_PAIRS: [RegExp, RegExp][] = [
        [/喜欢|偏好|爱|like|love|prefer|enjoy/, /讨厌|不喜欢|不想|放弃|hate|dislike|don't like|quit|gave up/i],
        [/在.*工作|在.*上班|work at|working at|employed/, /离职|辞职|被裁|不干了|quit|fired|laid off|left the job|resigned/i],
        [/住在|住|live in|living in|reside/, /搬到|搬去|搬家|moved to|relocat|moving to/i],
        [/运动|跑步|健身|exercise|running|workout|gym/, /不运动|放弃运动|不跑了|stopped exercising|quit gym|no longer run/i],
        [/学|在学|studying|learning|taking a course/, /不学了|放弃了|学不动|stopped studying|dropped out|gave up learning/i],
      ]

      for (const [patternA, patternB] of CONFLICT_PAIRS) {
        const newMatchesB = patternB.test(content)
        if (!newMatchesB) continue

        // 新记忆匹配了 B 模式（否定面），搜索已有记忆中匹配 A 模式的
        for (const existing of memoryState.memories) {
          if (existing.scope === 'expired' || existing.scope === 'decayed') continue
          if (!patternA.test(existing.content)) continue

          // 确认是同一主题（至少有 1 个共同关键词）
          const existingWords = new Set((existing.content.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map((w: string) => w.toLowerCase()))
          const newWords = (content.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map((w: string) => w.toLowerCase())
          const overlap = newWords.filter((w: string) => existingWords.has(w)).length

          if (overlap >= 1) {
            // 冲突！旧记忆降级
            console.log(`[cc-soul][conflict] "${content.slice(0, 30)}" contradicts "${existing.content.slice(0, 30)}"`)
            existing.confidence = Math.max(0.1, (existing.confidence ?? 0.7) * 0.5)
            existing.scope = 'expired'
            break
          }
        }
      }
    } catch {}

    // ── Interference forgetting: new memory suppresses similar old memories ──
    if (FACT_SCOPES.includes(scope)) {
      suppressSimilarMemories(newMem)
    }

    // ── Online semantic complement marking ──
    markComplementCandidates(newMem, memoryState.memories)

    // Smart eviction: dynamic threshold + topic protection
    if (memoryState.memories.length > MAX_MEMORIES) {
      // Score each memory: low score = eviction candidate
      const evictionScores = memoryState.memories.map((m, idx) => {
        const decay = timeDecay(m)
        const conf = m.confidence ?? 0.7
        const emotionBoost = m.emotion === 'important' ? 2.0 : m.emotion === 'painful' ? 1.5 : 1.0
        const scopeBoost = (m.scope === 'correction' || m.scope === 'reflexion' || m.scope === 'consolidated') ? 1.5 : 1.0
        const tagBoost = (m.tags && m.tags.length > 5) ? 1.3 : 1.0
        const score = decay * conf * emotionBoost * scopeBoost * tagBoost
        return { idx, score, scope: m.scope }
      })
      // Dynamic threshold: only evict memories scoring below median * 0.3
      const scores = evictionScores.map(e => e.score).sort((a, b) => a - b)
      const median = scores[Math.floor(scores.length / 2)] || 0.5
      const evictionThreshold = median * 0.3

      // Count memories per scope for topic protection
      const scopeCounts = new Map<string, number>()
      for (const m of memoryState.memories) {
        scopeCounts.set(m.scope, (scopeCounts.get(m.scope) || 0) + 1)
      }

      const toEvict = new Set<number>()
      // Sort ascending — lowest scores first
      evictionScores.sort((a, b) => a.score - b.score)
      for (const e of evictionScores) {
        if (e.score >= evictionThreshold) break // dynamic: stop once above threshold
        // Topic protection: if this scope has ≤2 remaining, don't evict
        const remaining = Math.max(0, (scopeCounts.get(e.scope) || 0) - [...toEvict].filter(i => memoryState.memories[i]?.scope === e.scope).length)
        if (remaining <= 2) continue
        toEvict.add(e.idx)
      }

      if (toEvict.size > 0) {
        const filtered = memoryState.memories.filter((_, i) => !toEvict.has(i))
        memoryState.memories.length = 0
        memoryState.memories.push(...filtered)
        rebuildScopeIndex() // full rebuild after eviction
        rebuildRecallIndex(memoryState.memories)
      }
    } else {
      // Incremental index update
      const arr = scopeIndex.get(scope) || []
      arr.push(memoryState.memories[memoryState.memories.length - 1])
      scopeIndex.set(scope, arr)
      // Incremental content index update
      const ck = content.slice(0, 50).toLowerCase()
      contentIndex.set(ck, content)
    }
    incrementalIDFUpdate(content)
    invalidateFieldIDF()

    // Async: queue semantic tag generation for the new memory (batched)
    // Bug #8 fix: don't pass index — eviction may shift it; use content+ts for stable lookup
    if (content.length > 10) {
      const lastIdx = memoryState.memories.length - 1
      if (lastIdx >= 0 && memoryState.memories[lastIdx].content === content && !memoryState.memories[lastIdx].tags) {
        queueForTagging(content, memoryState.memories[lastIdx].ts)
      }
    }

    // ── 微蒸馏（Real-time Micro-Distillation，原创）──
    // 新记忆存入后，检查最近 10 条有没有 trigram > 0.4 + 时间相近(5min) 的可合并记忆
    // 轻活实时干：合并相似记忆减少碎片，深度蒸馏(6h)做全局整理
    try {
      const newIdx = memoryState.memories.length - 1
      const newMem = memoryState.memories[newIdx]
      if (newMem && newMem.content.length >= 15) {
        const newTri = trigrams(newMem.content)
        const searchStart = Math.max(0, newIdx - 10)
        let bestSim = 0, bestIdx = -1
        for (let i = searchStart; i < newIdx; i++) {
          const other = memoryState.memories[i]
          if (!other || other.scope === 'expired' || other.scope === 'historical') continue
          if (Math.abs((newMem.ts || 0) - (other.ts || 0)) > 300000) continue  // >5min apart, skip
          const sim = trigramSimilarity(newTri, trigrams(other.content))
          if (sim > bestSim) { bestSim = sim; bestIdx = i }
        }
        if (bestSim > 0.4 && bestIdx >= 0) {
          const target = memoryState.memories[bestIdx]
          // 合并：保留较长的作为 base，追加较短的新信息
          if (target.content.length >= newMem.content.length) {
            target.content = target.content + ' ' + newMem.content
          } else {
            target.content = newMem.content + ' ' + target.content
          }
          target.confidence = Math.max(target.confidence || 0.7, newMem.confidence || 0.7)
          target.recallCount = (target.recallCount || 0) + (newMem.recallCount || 0)
          // 标记新记忆为已合并（不删除，让 eviction 自然清理）
          newMem.scope = 'expired'
          newMem.content = `[merged→${bestIdx}]`
          console.log(`[cc-soul][micro-distill] merged memory #${newIdx} into #${bestIdx} (sim=${bestSim.toFixed(2)})`)
        }
      }
    } catch {}
  } finally {
    saveMemories()
  }
}

// ── Emotional memory tags: CLI judges emotional weight ──
export function addMemoryWithEmotion(content: string, scope: string, userId?: string, visibility?: 'global' | 'channel' | 'private', channelId?: string, emotion?: string, skipAutoExtract?: boolean) {
  addMemory(content, scope, userId, visibility, channelId, undefined, skipAutoExtract)

  // Bug #9 fix: only set emotion if addMemory actually added/updated a new entry (not dedup skip)
  // Check if any memory has this content — handles both new-add and update scenarios
  const found = memoryState.memories.some(m => m.content === content)
  if (!found) return

  // Find the newly added memory (last one with matching content)
  const target = memoryState.memories.length > 0
    ? memoryState.memories.reduce<Memory | undefined>((best, m) =>
        m.content === content && m.ts >= (best?.ts ?? 0) ? m : best,
        undefined)
    : undefined
  if (!target) return

  if (emotion) {
    // Use provided emotion directly, skip CLI call
    const validEmotions = ['neutral', 'warm', 'important', 'painful', 'funny']
    const matched = validEmotions.find(e => emotion.includes(e)) || 'neutral'
    target.emotion = matched
    // 粗粒度 mood 映射：warm→正面，painful→负面，其余中性
    if (!target.situationCtx) target.situationCtx = {}
    target.situationCtx.mood = matched === 'warm' ? 0.5 : matched === 'painful' ? -0.5 : 0
    saveMemories()
  } else if (content.length > 20) {
    // Use rule-based emotion detection (no LLM call needed)
    try {
      const sigMod = getLazyModule('signals'); const detectEmotionLabel = sigMod?.detectEmotionLabel; const emotionLabelToLegacy = sigMod?.emotionLabelToLegacy
      const detected = detectEmotionLabel(content)
      if (detected.confidence > 0.4) {
        target.emotion = emotionLabelToLegacy(detected.label)
        // Store fine-grained label as well
        ;(target as any).emotionLabel = detected.label
        // 写入 situationCtx.mood 供 S3 emotionResonance 状态门控使用
        // emotionLabelToPADCN 的 pleasure 值 [-0.7, 0.6] 作为 mood
        const emotionLabelToPADCN = sigMod?.emotionLabelToPADCN
        if (emotionLabelToPADCN) {
          const padcn = emotionLabelToPADCN(detected.label)
          if (!target.situationCtx) target.situationCtx = {}
          target.situationCtx.mood = padcn.pleasure
          target.situationCtx.energy = (padcn.arousal + 1) / 2  // arousal [-1,1] → energy [0,1]
        }
        saveMemories()
      }
    } catch {}
  }
}

