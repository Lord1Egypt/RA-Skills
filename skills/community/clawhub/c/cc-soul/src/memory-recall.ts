/**
 * memory-recall.ts — Recall engine extracted from memory.ts
 * BM25 scoring, hybrid recall (tag + trigram + BM25 + vector + OpenClaw FTS),
 * recall stats/impact tracking, fused multi-modal recall.
 */

import { resolve } from 'path'
import { existsSync } from 'fs'
import { homedir } from 'os'
import type { Memory } from './types.ts'
import { DATA_DIR, debouncedSave, loadJson, MEMORIES_PATH } from './persistence.ts'
import { getParam } from './auto-tune.ts'
import {
  sqliteRecall as sqliteRecallAsync, tagRecall as sqliteTagRecall,
  sqliteFindByContent, sqliteUpdateMemory,
  isSQLiteReady,
} from './sqlite-store.ts'
import { findMentionedEntities, getRelatedEntities, graphWalkRecall } from './graph.ts'
import {
  memoryState, scopeIndex, useSQLite, _memoriesLoaded, ensureSQLiteReady,
  saveMemories, syncToSQLite, getLazyModule,
  bayesBoost, bayesPenalize, bayesCorrect,
  coreMemories,
} from './memory.ts'
import { queryFacts } from './fact-store.ts'
import {
  trigrams, trigramSimilarity, expandQueryWithSynonyms, shuffleArray, timeDecay,
  SYNONYM_MAP, onCacheEvent, tokenize as unifiedTokenize, WORD_PATTERN,
} from './memory-utils.ts'
import { learnAssociation, getTemporalSuccessors as _getTemporalSuccessors } from './aam.ts'
import { positiveEvidence as _posEvidence, negativeEvidence as _negEvidence, confidenceRecallModifier as _confModifier } from './confidence-cascade.ts'

// Event-Driven Cache Coherence：注册缓存失效
onCacheEvent('memory_added', () => { idfCache = null; lastIdfBuildTs = 0 })
onCacheEvent('memory_deleted', () => { idfCache = null; lastIdfBuildTs = 0; _bm25TokenCache.clear() })
onCacheEvent('consolidation', () => { idfCache = null; lastIdfBuildTs = 0; _bm25TokenCache.clear() })
onCacheEvent('identity_changed', () => { idfCache = null; lastIdfBuildTs = 0 })
onCacheEvent('fact_updated', () => { idfCache = null; lastIdfBuildTs = 0 })
onCacheEvent('correction_received', () => { _bm25TokenCache.clear() })

// ── P2a: 日期归一化（懒生成）──
const DATE_PATTERNS: Array<{ re: RegExp; replacer: (match: string, ...args: string[]) => string }> = [
  { re: /昨天|yesterday/gi, replacer: () => { const d = new Date(Date.now() - 86400000); return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}` } },
  { re: /前天/g, replacer: () => { const d = new Date(Date.now() - 2*86400000); return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}` } },
  { re: /今天|today/gi, replacer: () => { const d = new Date(); return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}` } },
  { re: /明天|tomorrow/gi, replacer: () => { const d = new Date(Date.now() + 86400000); return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}` } },
  { re: /上周|last week/gi, replacer: () => '7天前' },
  { re: /上个月|last month/gi, replacer: () => '30天前' },
]

/** 懒生成日期归一化内容。原始 content 不变，contentNormalized 用于召回和注入 */
export function getContentForRecall(mem: Memory): string {
  if (mem.contentNormalized !== undefined) return mem.contentNormalized
  // 检查是否包含相对日期
  let text = mem.content
  let changed = false
  for (const { re, replacer } of DATE_PATTERNS) {
    if (re.test(text)) {
      text = text.replace(re, replacer as any)
      changed = true
    }
  }
  if (changed) {
    mem.contentNormalized = text
  }
  return mem.contentNormalized ?? mem.content
}

// ── Persistent recall indices (avoid O(n) rebuild each recall) ──
const _contentMap = new Map<string, Memory>()      // content → Memory
export const _memLookup = new Map<string, Memory>()       // "content\0ts" → Memory

// ── 启动效应缓存（Priming Cache）──
// 最近 5 分钟内用户提到的词 → 降低相关记忆的识别阈值
export const _primingCache = new Map<string, number>()  // word → last mentioned timestamp

/** 更新启动缓存：从用户消息中提取词，记录提及时间 */
export function updatePrimingCache(userMsg: string): void {
  const now = Date.now()
  const words = (userMsg.match(WORD_PATTERN.CJK2_EN3) || [])
  for (const w of words) _primingCache.set(w.toLowerCase(), now)
  // 清理过期条目（>10 分钟）
  if (_primingCache.size > 200) {
    for (const [k, ts] of _primingCache) {
      if (now - ts > 10 * 60 * 1000) _primingCache.delete(k)
    }
  }
}

// ── 预测性启动缓存（Predictive Priming Cache）──
// 人脑原理：回忆 A 后，大脑自动预激活与 A 时序关联的 B（前瞻性记忆准备）
// cc-soul 原创：用 AAM 时序后继预测下一个话题，BM25 轻量匹配预热记忆
export const _predictivePrimingCache = new Map<string, { predictedRelevance: number; primedAt: number }>()
// key = memory content (用 content 做 key，因为 memory.id 不稳定)

const PREDICTIVE_PRIMING_WINDOW_MS = 5 * 60 * 1000  // 5 分钟过期
const PREDICTIVE_PRIMING_MAX = 30  // 最多缓存 30 条预热记忆

/** 预测性启动：召回后用 AAM 时序后继预热下轮可能需要的记忆 */
export function predictivePrime(recalledMemories: Memory[], allMemories: Memory[]): void {
  if (recalledMemories.length === 0 || allMemories.length === 0) return

  // 从召回结果中提取关键词
  const recalledWords = new Set<string>()
  for (const m of recalledMemories) {
    const words = (m.content.match(WORD_PATTERN.CJK2_EN3) || [])
    for (const w of words) recalledWords.add(w.toLowerCase())
  }

  // 用 AAM 时序后继预测下一轮话题关键词
  const predictedWords = new Map<string, number>()  // word → max successor count
  for (const w of recalledWords) {
    try {
      const successors = _getTemporalSuccessors(w, 3)
      for (const s of successors) {
        const existing = predictedWords.get(s.word) || 0
        if (s.count > existing) predictedWords.set(s.word, s.count)
      }
    } catch {}
  }

  // 没有后继 → 不浪费 cycle（冷启动保护）
  if (predictedWords.size === 0) return

  // 清理过期条目
  const now = Date.now()
  for (const [k, v] of _predictivePrimingCache) {
    if (now - v.primedAt > PREDICTIVE_PRIMING_WINDOW_MS) _predictivePrimingCache.delete(k)
  }

  // 轻量 BM25 匹配：对 allMemories 做 token overlap 打分
  const recalledContentSet = new Set(recalledMemories.map(m => m.content))
  const scored: { content: string; relevance: number }[] = []

  for (const mem of allMemories) {
    if (!mem || !mem.content || recalledContentSet.has(mem.content)) continue
    const tokens = bm25Tokenize(getContentForRecall(mem))
    if (tokens.length === 0) continue

    let matchScore = 0
    for (const t of tokens) {
      const succCount = predictedWords.get(t)
      if (succCount) matchScore += succCount
    }

    if (matchScore > 0) {
      // 归一化：token overlap 比率 × 后继强度
      const relevance = Math.min(1.0, matchScore / (tokens.length * 2))
      scored.push({ content: mem.content, relevance })
    }
  }

  // 取 top-N 存入缓存
  scored.sort((a, b) => b.relevance - a.relevance)
  const topPrimed = scored.slice(0, PREDICTIVE_PRIMING_MAX)

  for (const s of topPrimed) {
    _predictivePrimingCache.set(s.content, { predictedRelevance: s.relevance, primedAt: now })
  }

  if (topPrimed.length > 0) {
    try { require('./decision-log.ts').logDecision('predictive_prime', `${topPrimed.length} memories`, `predicted_words=${predictedWords.size}, top="${topPrimed[0].content.slice(0, 30)}"`) } catch {}
  }
}

// ── 指代消解：召回时查询扩展 ──
// 人脑原理：回忆时大脑自动将"他怎么样了"映射到具体的人
const COREF_QUERY_PRONOUNS = /他|她|它|这个|那个/
const COREF_QUERY_PLURAL = /他们|她们|它们/

function expandQueryWithCoreference(query: string, chatHistory: { user: string }[]): string {
  if (!COREF_QUERY_PRONOUNS.test(query) || COREF_QUERY_PLURAL.test(query)) return query
  let entities: string[] = []
  try {
    const { findMentionedEntities: fme } = require('./graph.ts')
    const recentText = chatHistory.slice(-3).map(h => h.user).join(' ')
    entities = fme(recentText)
  } catch {}
  if (entities.length === 0 || entities.length > 3) return query
  const expanded = query + ' ' + entities.join(' ')
  try { require('./decision-log.ts').logDecision('coreference_recall', query.slice(0, 30), `expanded: +${entities.join(',')}`) } catch {}
  return expanded
}

// ── 时间范围提取（Triple Query Decomposition 用）──

export interface TimeRange { fromMs: number; toMs: number }

export function extractTimeRange(query: string): TimeRange | null {
  const now = Date.now()
  const DAY = 86400000

  if (/昨天|yesterday/i.test(query)) return { fromMs: now - 2 * DAY, toMs: now - DAY }
  if (/前天/.test(query)) return { fromMs: now - 3 * DAY, toMs: now - 2 * DAY }
  if (/上周|last week/i.test(query)) return { fromMs: now - 14 * DAY, toMs: now - 7 * DAY }
  if (/上个月|last month/i.test(query)) return { fromMs: now - 60 * DAY, toMs: now - 30 * DAY }
  if (/最近|recently/i.test(query)) return { fromMs: now - 7 * DAY, toMs: now }
  if (/今天|today/i.test(query)) return { fromMs: now - DAY, toMs: now }
  if (/明天|tomorrow/i.test(query)) return { fromMs: now, toMs: now + DAY }

  const daysAgo = query.match(/(\d+)\s*(?:天前|days?\s*ago)/i)
  if (daysAgo) {
    const d = parseInt(daysAgo[1])
    return { fromMs: now - (d + 1) * DAY, toMs: now - (d - 1 < 0 ? 0 : d - 1) * DAY }
  }
  const weeksAgo = query.match(/(\d+)\s*(?:周前|weeks?\s*ago)/i)
  if (weeksAgo) {
    const w = parseInt(weeksAgo[1])
    return { fromMs: now - (w + 1) * 7 * DAY, toMs: now - (w - 1 < 0 ? 0 : w - 1) * 7 * DAY }
  }

  // "之前/以前/上次" → 不是精确时间，返回 null
  return null
}

// ═══════════════════════════════════════════════════════════════════════════════
// Route Filter — 量大时缩小候选集，量少时全量扫描
// ═══════════════════════════════════════════════════════════════════════════════

const ROUTE_THRESHOLD = 800  // 折中：大部分对话 <800，只在超大库才过滤
const ROUTE_MIN_CANDIDATES = 150  // 折中：过滤后至少保留 150

function routeMemories(memories: Memory[], query: string, userId?: string): Memory[] {
  if (memories.length < ROUTE_THRESHOLD) return memories

  let candidates = memories

  // 1. 用户过滤（多用户场景）
  if (userId) {
    const userMems = candidates.filter(m => !m.userId || m.userId === userId)
    if (userMems.length > 0) candidates = userMems
  }

  // 2. 时间过滤（用户说了"上周""昨天"等）
  const timeRange = extractTimeRange(query)
  if (timeRange) {
    const timeMems = candidates.filter(m => m.ts >= timeRange.fromMs && m.ts <= timeRange.toMs)
    if (timeMems.length >= 5) candidates = timeMems
  }

  // 3. 实体过滤（用户提到了具体的人/事物）
  // 只在记忆池很大时做（>500），且过滤后至少保留原来的 30%
  if (candidates.length > ROUTE_THRESHOLD) {
    try {
      const { findMentionedEntities } = require('./graph.ts')
      const entities: string[] = findMentionedEntities(query)
      if (entities.length > 0) {
        const entityMems = candidates.filter(m => entities.some(e => m.content?.includes(e)))
        // 至少保留 30% 的候选或 ROUTE_MIN_CANDIDATES，防止过度过滤
        const minKeep = Math.max(ROUTE_MIN_CANDIDATES, Math.floor(candidates.length * 0.3))
        if (entityMems.length >= minKeep) candidates = entityMems
      }
    } catch {}
  }

  // 4. 安全下限：至少保留 ROUTE_MIN_CANDIDATES 条
  if (candidates.length < ROUTE_MIN_CANDIDATES && memories.length > ROUTE_MIN_CANDIDATES) {
    const candidateSet = new Set(candidates)
    const recent = memories
      .filter(m => !candidateSet.has(m))
      .sort((a, b) => (b.ts || 0) - (a.ts || 0))
      .slice(0, ROUTE_MIN_CANDIDATES - candidates.length)
    candidates = [...candidates, ...recent]
  }

  return candidates
}

/** Call when a new memory is added to keep recall indices in sync */
export function updateRecallIndex(mem: Memory) {
  _contentMap.set(mem.content, mem)
  _memLookup.set(`${mem.content}\0${mem.ts}`, mem)
}

/** Full rebuild (call after eviction or bulk load) */
export function rebuildRecallIndex(memories: Memory[]) {
  _contentMap.clear()
  _memLookup.clear()
  for (const m of memories) {
    _contentMap.set(m.content, m)
    _memLookup.set(`${m.content}\0${m.ts}`, m)
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// P3: A/B 通道实验 — 每 20 次召回随机降权一个通道 50%，评估通道效用
// ═══════════════════════════════════════════════════════════════════════════════

const AB_INTERVAL = 20
const AB_TESTABLE_CHANNELS = ['rrfGraph', 'rrfDirichlet', 'rrfScope'] as const
let _abCounter = 0
let _abDisabledChannel: string | null = null
let _abEngagementWithChannel: number[] = []
let _abEngagementWithout: number[] = []


/** 每次 recall 调用时推进 A/B 计数器 */
function tickABExperiment(): void {
  _abCounter++
  if (_abCounter % AB_INTERVAL === 0) {
    // 结束上一轮实验
    if (_abDisabledChannel && _abEngagementWithout.length >= 5) {
      const withAvg = _abEngagementWithChannel.length > 0
        ? _abEngagementWithChannel.reduce((s, v) => s + v, 0) / _abEngagementWithChannel.length : 0.5
      const withoutAvg = _abEngagementWithout.reduce((s, v) => s + v, 0) / _abEngagementWithout.length
      const diff = withAvg - withoutAvg
      try {
        const { logDecision } = require('./decision-log.ts')
        logDecision('ab_test', _abDisabledChannel,
          `with=${withAvg.toFixed(3)}, without=${withoutAvg.toFixed(3)}, diff=${diff.toFixed(3)}, ${Math.abs(diff) < 0.05 ? '不显著' : diff > 0 ? '通道有用' : '通道可能有害'}`)
      } catch {}
    }

    // 开始新一轮：随机选通道降权 50%
    _abDisabledChannel = AB_TESTABLE_CHANNELS[Math.floor(Math.random() * AB_TESTABLE_CHANNELS.length)]
    _abEngagementWithChannel = []
    _abEngagementWithout = []
  }
}

/** 记录 A/B 实验期间的 engagement（由 P1a 的 feedbackMemoryEngagement 调用） */
export function recordABEngagement(engagementScore: number): void {
  if (_abDisabledChannel) {
    _abEngagementWithout.push(engagementScore)
  } else {
    _abEngagementWithChannel.push(engagementScore)
  }

  // A/B 归因：记录贡献 engaged 记忆的激活通道
  if (engagementScore > 0.3) {
    try {
      const { getRecentTrace } = require('./activation-field.ts')
      const { logDecision } = require('./decision-log.ts')
      const recent = getRecentTrace()
      if (recent?.traces?.length) {
        const topTrace = recent.traces[0]
        const topStep = topTrace.path?.[0]
        if (topStep) {
          logDecision('ab_test', `engaged_via_${topStep.via}`,
            `engagement=${engagementScore.toFixed(3)}, disabled=${_abDisabledChannel || 'none'}`,
            { via: topStep.via, score: topTrace.score })
        }
      }
    } catch {}
  }
}

// ── Recall rate tracking ──
export let recallStats = { total: 0, successful: 0, rate: 0 }
export function getRecallRate(): { total: number; successful: number; rate: number } {
  const rate = recallStats.total > 0
    ? (recallStats.successful / recallStats.total * 100)
    : (recallStats.rate * 100)  // use last-cycle rate after periodic reset
  return { total: recallStats.total, successful: recallStats.successful, rate }
}

// ── Recall impact tracking: which memories actually helped? ──
export const recallImpact = new Map<string, { recalled: number; helpedQuality: number; avgImpact: number }>()
let _lastImpactCleanup = 0

// ── Lazy-loaded smart-forget for adaptive decay feedback ──
let _smartForgetMod: any = null
function getSmartForget() {
  if (!_smartForgetMod) {
    try { _smartForgetMod = require('./smart-forget.ts') } catch {
      import('./smart-forget.ts').then(m => { _smartForgetMod = m }).catch((e: any) => { console.error(`[cc-soul] module load failed (smart-forget): ${e.message}`) })
    }
  }
  return _smartForgetMod
}

export function trackRecallImpact(recalledContents: string[], qualityScore: number) {
  // Adaptive decay feedback: track whether recalled memories were useful
  const sf = getSmartForget()
  if (sf) {
    const n = recalledContents.length
    if (qualityScore >= 5) {
      for (let i = 0; i < n; i++) sf.recordRecallHit()
    } else {
      for (let i = 0; i < n; i++) sf.recordRecallMiss()
    }
  }

  for (const content of recalledContents) {
    const key = content.slice(0, 80)
    const entry = recallImpact.get(key) || { recalled: 0, helpedQuality: 0, avgImpact: 0 }
    entry.recalled++
    entry.helpedQuality += qualityScore
    entry.avgImpact = entry.helpedQuality / entry.recalled
    recallImpact.set(key, entry)

    // ── Reinforcement feedback: propagate quality back to memory confidence ──
    // Good response (≥7) → this memory helped → boost confidence
    // Bad response (≤3) → this memory may have misled → reduce confidence
    if (entry.recalled >= 2) { // only after enough data points
      // O(1) lookup via _contentMap — try exact key first (covers most cases)
      const keyPrefix = key.slice(0, 40)
      let mem = _contentMap.get(key)
      if (!mem || mem.scope === 'expired') {
        // Fallback: prefix search on _contentMap (still faster than full memories scan)
        mem = undefined
        for (const [content, m] of _contentMap) {
          if (content.startsWith(keyPrefix) && m.scope !== 'expired') { mem = m; break }
        }
      }
      if (mem) {
        if (qualityScore >= 7) {
          bayesBoost(mem, 1)  // strong positive evidence: α += 1
        } else if (qualityScore <= 3) {
          bayesPenalize(mem, 1)  // negative evidence: β += 1
          if (mem.confidence < 0.2) {
            console.log(`[cc-soul][recall-feedback] low-quality memory demoted: "${content.slice(0, 50)}" (avgImpact=${entry.avgImpact.toFixed(1)})`)
          }
        }
        syncToSQLite(mem, { confidence: mem.confidence })
      }
    }
  }
  // Cap map size (debounced: at most once per 60s)
  if (recallImpact.size > 500 && Date.now() - _lastImpactCleanup > 60000) {
    _lastImpactCleanup = Date.now()
    const sorted = [...recallImpact.entries()].sort((a, b) => a[1].recalled - b[1].recalled)
    const deleteCount = recallImpact.size - 300
    for (const [key] of sorted.slice(0, deleteCount)) recallImpact.delete(key)
  }
}

export function getRecallImpactBoost(content: string): number {
  const key = content.slice(0, 80)
  const entry = recallImpact.get(key)
  if (!entry || entry.recalled < 3) return 1.0
  // High avg impact → boost, low → penalize
  if (entry.avgImpact >= 7) return 1.3
  if (entry.avgImpact >= 5) return 1.1
  if (entry.avgImpact < 3) return 0.7
  return 1.0
}

// ═══════════════════════════════════════════════════════════════════════════════
// BM25 scoring (replaces TF-IDF — better term frequency saturation + doc length normalization)
// ═══════════════════════════════════════════════════════════════════════════════

let idfCache: Map<string, number> | null = null
let avgDocLenCache: number | null = null
let lastIdfBuildTs = 0

// BM25 parameters — now tunable via auto-tune
function getBM25K1() { return getParam('memory.bm25_k1') }
function getBM25B() { return getParam('memory.bm25_b') }

// ── BM25 CJK n-gram tokenizer (2-gram + 3-gram) with stop-word filtering ──
const BM25_STOP_WORDS = new Set([...'的了是在我你他不有这那就也和但'.split(''), 'the', 'a', 'an', 'is', 'are', 'was', 'were', 'to', 'for', 'in', 'on', 'at', 'and', 'or', 'but', 'not'])

/** Tokenize for BM25 — 使用统一 tokenize('bm25') from memory-utils.ts */
function bm25Tokenize(text: string): string[] {
  return unifiedTokenize(text, 'bm25')
}

const IDF_CACHE_TTL = 300000 // 5 minutes

function buildIDF(): Map<string, number> {
  if (idfCache && idfCache.size > 0 && Date.now() - lastIdfBuildTs < IDF_CACHE_TTL) return idfCache
  const df = new Map<string, number>()
  const N = memoryState.memories.length || 1
  let totalDocLen = 0
  for (const mem of memoryState.memories) {
    const words = bm25Tokenize(getContentForRecall(mem))
    totalDocLen += words.length
    const unique = new Set(words)
    for (const w of unique) {
      df.set(w, (df.get(w) || 0) + 1)
    }
  }
  const idf = new Map<string, number>()
  for (const [word, count] of df) {
    idf.set(word, Math.log(N / (1 + count)))
  }
  idfCache = idf
  avgDocLenCache = N > 0 ? totalDocLen / N : 1
  lastIdfBuildTs = Date.now()
  return idf
}

// ── BM25 tokenization cache: avoid re-tokenizing the same doc content ──
const _bm25TokenCache = new Map<string, { words: string[]; tf: Map<string, number> }>()

function _getDocTokens(doc: string): { words: string[]; tf: Map<string, number> } {
  const cached = _bm25TokenCache.get(doc)
  if (cached) {
    // LRU: move to end of Map insertion order
    _bm25TokenCache.delete(doc)
    _bm25TokenCache.set(doc, cached)
    return cached
  }
  const words = bm25Tokenize(doc)
  const tf = new Map<string, number>()
  for (const w of words) tf.set(w, (tf.get(w) || 0) + 1)
  const entry = { words, tf }
  _bm25TokenCache.set(doc, entry)
  // LRU evict: delete oldest entries (front of Map) when over capacity
  if (_bm25TokenCache.size > 2000) {
    const evict = Math.floor(_bm25TokenCache.size * 0.2)
    const iter = _bm25TokenCache.keys()
    for (let i = 0; i < evict; i++) {
      const k = iter.next().value
      if (k !== undefined) _bm25TokenCache.delete(k)
    }
  }
  return entry
}

/** Invalidate BM25 token cache (call when memories change significantly) */
export function invalidateBM25TokenCache() { _bm25TokenCache.clear() }

// [DELETED] bm25Score — 被 P5g CMR 替换（词覆盖率 + AAM 语义扩展 + 上下文亲和度）

// ═══════════════════════════════════════════════════════════════════════════════
// Recall: tag-based (primary) + TF-IDF (fallback for untagged)
// ═══════════════════════════════════════════════════════════════════════════════

/** MMR (Maximal Marginal Relevance) — 去除召回结果中的语义重复 */
/**
 * P5i: Topic-based dedup（替换 MMR）
 * O(n) 而非 O(n²)。CMR 的 context affinity 已经隐式做了多样性。
 * 用 scope + 首词做 topic 签名，每个 topic 最多保留 3 条。
 */
function mmrRerank(candidates: (Memory & { score: number })[], topN: number, _lambda = 0.7): (Memory & { score: number })[] {
  if (candidates.length <= topN) return candidates
  const MAX_PER_TOPIC = 3
  const topicCounts = new Map<string, number>()

  const selected: (Memory & { score: number })[] = []
  // candidates 已按 score 降序排列
  for (const mem of candidates) {
    if (selected.length >= topN) break
    // topic 签名 = scope + 内容前 10 字（同 topic 的记忆内容开头通常相似）
    const topicKey = (mem.scope || 'other') + '|' + (mem.content || '').slice(0, 10)
    const count = topicCounts.get(topicKey) || 0
    if (count >= MAX_PER_TOPIC) continue  // 同 topic 已够，跳过
    topicCounts.set(topicKey, count + 1)
    selected.push(mem)
  }
  return selected
}

/** Internal recall that preserves `score` on returned memories (for fusion ranking). */
export function recallWithScores(msg: string, topN = 3, userId?: string, channelId?: string, moodCtx?: { mood: number; alertness: number }): (Memory & { score: number })[] {
  if (memoryState.memories.length === 0 || !msg) return []

  // Extract query keywords (Chinese 2+ char sequences + English 3+ char words)
  // 短查询（<10字）降低门槛到单字CJK，避免"我住哪""我有宠物吗"无词命中
  const cjkMinLen = msg.length < 10 ? 1 : 2
  const cjkPattern = cjkMinLen === 1 ? /[\u4e00-\u9fff]+/gi : /[\u4e00-\u9fff]{2,}/gi
  const rawWords = new Set(
    (msg.match(cjkPattern) || []).concat(msg.match(/[a-z]{3,}/gi) || []).map(w => w.toLowerCase())
  )
  // 短查询单字关键词扩展（"住" → "住在""住北京"，"宠物" 保持，"电脑" 保持）
  if (msg.length < 15) {
    const QUERY_EXPAND: Record<string, string[]> = {
      '住': ['住在', '北京', '上海', '深圳', '广州', '杭州', '地址'],
      '哪': [], // 疑问词不扩展
      '宠物': ['猫', '狗', '养了', '养'],
      '电脑': ['macbook', 'mac', 'thinkpad', '笔记本', '台式'],
      '饮料': ['咖啡', '茶', '酒', '喝'],
      '喝': ['咖啡', '茶', '酒', '饮料'],
      '工作': ['公司', '上班', '就职', '字节', '腾讯', '阿里'],
      '讨厌': ['不喜欢', '不想', '受不了'],
      '跑步': ['运动', '锻炼', '公里'],
      'live': ['住在', 'location', 'city', 'moved'],
      'pet': ['cat', 'dog', '猫', '狗', '养了'],
      'work': ['company', 'job', 'office', '公司', '上班'],
      'hate': ['dislike', "don't like", '讨厌', '不喜欢'],
      'like': ['love', 'enjoy', 'prefer', '喜欢'],
      'family': ['daughter', 'son', 'wife', 'husband', '女儿', '儿子'],
      'computer': ['macbook', 'mac', 'laptop', 'desktop', '电脑'],
      'drink': ['coffee', 'tea', '咖啡', '茶'],
      'run': ['exercise', 'workout', 'running', '跑步', '运动'],
    }
    for (const w of [...rawWords]) {
      const expand = QUERY_EXPAND[w]
      if (expand) for (const e of expand) rawWords.add(e)
    }
  }
  if (rawWords.size === 0) return []

  // Graph-augmented query expansion
  const mentionedEntities = findMentionedEntities(msg)
  const relatedEntities = mentionedEntities.length > 0
    ? getRelatedEntities(mentionedEntities, 2, 8)
    : []
  const expansionWords = new Set<string>()
  for (const entity of relatedEntities) {
    const words = (entity.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map((w: string) => w.toLowerCase())
    for (const w of words) {
      if (!rawWords.has(w)) expansionWords.add(w)
    }
  }

  // Expand with synonyms for broader semantic matching
  const queryWords = expandQueryWithSynonyms(rawWords)

  // Lazy-build IDF + avgDocLen only if needed (for BM25 scoring)
  let idf: Map<string, number> | null = null
  let avgDocLen = 1

  // Lazy-build trigrams for fuzzy matching (outside loop)
  let queryTrigrams: Set<string> | null = null

  // Lazy-build BM25 n-gram query tokens (matches bm25Tokenize output)
  let bm25QueryTokens: Set<string> | null = null

  // Use scopeIndex to skip expired/decayed scopes in bulk instead of per-item check
  const SKIP_SCOPES = new Set(['expired', 'decayed'])
  const activeMemories: Memory[] = []
  for (const [scope, mems] of scopeIndex) {
    if (SKIP_SCOPES.has(scope)) continue
    for (const m of mems) {
      // 学习型排除（原创）：被注入多次但用户从不理会 → 自动降权
      // 比规则排除更智能：每个用户的排除模式不同，从行为中学习
      const eng = m.injectionEngagement ?? 0
      const miss = m.injectionMiss ?? 0
      if (miss >= 5 && eng === 0) continue  // 注入 5 次全被忽视 → 跳过
      activeMemories.push(m)
    }
  }

  // Cache getParam results outside loop to avoid per-memory calls
  const _scopeBoostPref = getParam('recall.scope_boost_preference')
  const _scopeBoostCorr = getParam('recall.scope_boost_correction')
  const _emotionBoostImportant = getParam('recall.emotion_boost_important')
  const _emotionBoostPainful = getParam('recall.emotion_boost_painful')
  const _emotionBoostWarm = getParam('recall.emotion_boost_warm')
  const _userBoostSame = getParam('recall.user_boost_same')
  const _userBoostOther = getParam('recall.user_boost_other')
  const _tierWeightHot = getParam('recall.tier_weight_hot')
  const _tierWeightWarm = getParam('recall.tier_weight_warm')
  const _tierWeightCool = getParam('recall.tier_weight_cool')
  const _tierWeightCold = getParam('recall.tier_weight_cold')
  const _consolidatedBoost = getParam('recall.consolidated_boost')
  const _reflexionBoost = getParam('recall.reflexion_boost')
  const _flashbulbHigh = getParam('recall.flashbulb_high')
  const _flashbulbMedium = getParam('recall.flashbulb_medium')

  const scored: (Memory & { score: number })[] = []
  for (const mem of activeMemories) {
    // ── Visibility filter ──
    const vis = mem.visibility || 'global'
    if (vis === 'channel' && channelId && mem.channelId && mem.channelId !== channelId) continue
    if (vis === 'private' && userId && mem.userId && mem.userId !== userId) continue

    // ── 事实版本链：被取代的记忆默认不参与 recall ──
    // 除非用户问"之前/以前/曾经"（触发 historical 通道）
    if (mem.supersededBy && mem.scope === 'historical') {
      if (!/之前|以前|曾经|过去|原来|上次|before|previously|used to|in the past|last time/i.test(msg)) continue
    }
    // If no channelId provided (e.g. DM), include private + global (skip channel-scoped from other channels)
    let sim = 0

    // ═══════════════════════════════════════════════════════════════
    // P5g: CMR (Contextual Memory Retrieval) — 替换 BM25+Trigram+Dirichlet
    // 专为短文本对话记忆设计，不用 BM25 的文档长度归一化
    // ═══════════════════════════════════════════════════════════════

    // CMR Layer 1: 词覆盖率（替换 BM25，短文本不需要文档长度归一化）
    const memContent = getContentForRecall(mem)
    const memWords = new Set(
      (memContent.match(WORD_PATTERN.CJK2_EN3) || []).map((w: string) => w.toLowerCase())
    )

    if (mem.tags && mem.tags.length > 0) {
      // Tag 匹配：tag 命中算精确覆盖
      const tagStr = mem.tags.join('|').toLowerCase()
      let tagHits = 0
      for (const qw of queryWords) {
        if (tagStr.includes(qw)) { tagHits++; continue }
        if (mem.tags.some(t => qw.includes(t))) tagHits++
      }
      sim = tagHits / Math.max(1, queryWords.size)
    }

    // 词覆盖率（IDF 加权 + BM25+ delta）：不管有没有 tag 都算
    // 过滤疑问词（"什么""吗""呢"不应算入覆盖率分母）
    // BM25+ delta: 每个命中词至少贡献 delta，防止长文档被过度惩罚
    if (sim < 0.3) {
      if (!idf) { idf = buildIDF(); avgDocLen = avgDocLenCache || 1 }
      const QUESTION_STOPWORDS = new Set(['什么', '怎么', '哪个', '哪里', '多少', '为什么', '是否', '有没有', '是不是', '还', '记得', '知道', '叫', 'what', 'who', 'where', 'when', 'why', 'how', 'which', 'does', 'did', 'the', 'a', 'an', 'is', 'are', 'was', 'were', 'to', 'for', 'in', 'on', 'at', 'and', 'or', 'but', 'not'])
      const BM25_DELTA = 1.0  // BM25+ lower-bound correction
      let matchedWeight = 0, totalWeight = 0
      for (const qw of queryWords) {
        if (QUESTION_STOPWORDS.has(qw)) continue  // 跳过疑问词
        const w = idf.get(qw) ?? 1.0
        totalWeight += w
        if (memWords.has(qw)) matchedWeight += w + BM25_DELTA
      }
      // totalWeight 也加上 delta 对应的满分上限，保持比例正确
      const maxWeight = totalWeight + (queryWords.size * BM25_DELTA)
      const coverage = maxWeight > 0 ? matchedWeight / maxWeight : 0
      sim = Math.max(sim, coverage)

      // 反向覆盖：记忆中的关键词在查询中出现（"小雨"在问"女朋友叫什么"时不会出现，但"女朋友"会）
      // 如果正向覆盖低，试反向：记忆词命中查询词的比例
      if (sim < 0.3 && memWords.size > 0) {
        let reverseHits = 0
        for (const mw of memWords) {
          if (queryWords.has(mw)) reverseHits++
        }
        const reverseCoverage = reverseHits / memWords.size
        sim = Math.max(sim, reverseCoverage * 0.7)  // 反向覆盖打 0.7 折
      }
    }

    // CMR Layer 2: AAM 语义扩展（替换 Trigram 暴力匹配）
    // AAM 联想："Python" → "pip","venv"；trigram 做不到
    if (sim < 0.2) {
      try {
        const aamMod = require('./aam.ts')
        const queryTerms = [...queryWords].slice(0, 5)
        const expanded = aamMod.expandQuery(queryTerms, 3)
        let semanticMatch = 0
        for (const exp of expanded) {
          if (memWords.has(exp.word)) {
            semanticMatch += exp.weight * (idf?.get(exp.word) ?? 0.5)
          }
        }
        const semanticCoverage = expanded.length > 0 ? semanticMatch / expanded.length : 0
        sim = Math.max(sim, semanticCoverage * 0.8)
      } catch {}
    }

    // CMR Layer 3: 上下文亲和度（BM25/Trigram/Dirichlet 都没有的）
    // 利用记忆的 situationCtx 做语境匹配
    if (mem.situationCtx && moodCtx) {
      const moodDelta = Math.abs((mem.situationCtx.mood ?? 0) - (moodCtx.mood ?? 0))
      const ctxBonus = moodDelta < 0.3 ? 0.1 : 0  // 情绪相近 → 小加成
      sim += ctxBonus
    }

    // Trigram 兜底（极端情况：查询和记忆共享字符但不共享词）
    if (sim < 0.05) {
      if (!queryTrigrams) queryTrigrams = trigrams(msg)
      const memTri = trigrams(memContent)
      const triSim = trigramSimilarity(queryTrigrams, memTri)
      sim = Math.max(sim, triSim * 0.6)  // trigram 降权到 0.6（不再是主力）
    }

    // ── Reasoning field matching: context + conclusion also participate in scoring ──
    if (mem.reasoning) {
      const rText = `${mem.reasoning.context || ''} ${mem.reasoning.conclusion || ''}`.toLowerCase()
      if (rText.length > 5) {
        let rHits = 0
        for (const qw of queryWords) { if (rText.includes(qw)) rHits++ }
        const rSim = rHits / Math.max(1, queryWords.size) * 0.6
        if (rSim > 0) sim = Math.max(sim, sim + rSim * 0.5)
      }
    }

    // ── Causal Chain Enhancement: 当 query 含"为什么/原因/怎么回事"时，利用 reasoning 字段 ──
    if (mem.reasoning && mem.reasoning.conclusion && /为什么|因为|原因|怎么回事|why|because|导致|所以/.test(msg)) {
      const reasonWords = (mem.reasoning.context + ' ' + mem.reasoning.conclusion)
        .match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []
      let reasonHits = 0
      for (const rw of reasonWords) {
        if (queryWords.has(rw.toLowerCase())) reasonHits++
      }
      if (reasonHits > 0) {
        sim = Math.max(sim, sim + reasonHits * 0.12) // 因果内容命中加分
      }
    }
    // ── 如果记忆有 because 字段，也纳入相似度计算 ──
    if (mem.because && queryWords.size > 0) {
      const becauseWords = (mem.because.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map((w: string) => w.toLowerCase())
      const becauseHits = becauseWords.filter((w: string) => queryWords.has(w)).length
      if (becauseHits > 0) {
        sim += becauseHits * 0.08
      }
    }

    if (sim < 0.03) continue

    // ── Causal query boost: "为什么/因为/原因" queries boost memories with because/reasoning ──
    const _isCausalQuery = /为什么|因为|原因|怎么回事|why|because|caused|reason/i.test(msg)
    const causalBoost = _isCausalQuery && (mem.because || mem.reasoning) ? 1.5 : 1.0

    // Weighted scoring: recency (Weibull) + scope boost + emotion boost + userId boost + confidence
    // Unified Weibull decay model from smart-forget.ts (replaces exp(-age * rate))
    const recency = timeDecay(mem)
    // Bonus for recently recalled memories (tags indicate they've been useful)
    const usageBoost = (mem.tags && mem.tags.length > 5) ? 1.2 : 1.0
    const scopeBoost = (mem.scope === 'preference' || mem.scope === 'fact') ? _scopeBoostPref :
                       (mem.scope === 'correction') ? _scopeBoostCorr : 1.0
    let emotionBoost = 1.0
    // Legacy labels
    if (mem.emotion === 'important') emotionBoost = _emotionBoostImportant
    else if (mem.emotion === 'painful') emotionBoost = _emotionBoostPainful
    else if (mem.emotion === 'warm') emotionBoost = _emotionBoostWarm
    // New fine-grained labels (stored in emotionLabel)
    const eLabel = (mem as any).emotionLabel
    if (eLabel === 'anger' || eLabel === 'anxiety') emotionBoost = Math.max(emotionBoost, 1.4)
    else if (eLabel === 'pride' || eLabel === 'relief') emotionBoost = Math.max(emotionBoost, 1.3)
    else if (eLabel === 'frustration' || eLabel === 'sadness') emotionBoost = Math.max(emotionBoost, 1.3)
    // #5 Multi-user memory isolation: same user ×2.0, global ×1.0, other user's private → already filtered above
    const userBoost = (userId && mem.userId && mem.userId === userId) ? _userBoostSame
                    : (userId && mem.userId && mem.userId !== userId) ? _userBoostOther : 1.0
    // #3 HOT/WARM/COLD tier weighting
    const lastAcc = mem.lastAccessed || mem.ts || 0
    const accAgeDays = (Date.now() - lastAcc) / 86400000
    const tierWeight = ((accAgeDays <= 1 || (mem.recallCount ?? 0) >= 5) ? _tierWeightHot   // HOT
                      : (accAgeDays <= 7) ? _tierWeightWarm                                  // WARM
                      : (accAgeDays <= 30) ? _tierWeightCool : _tierWeightCold)              // COLD
    const consolidatedBoost = mem.scope === 'consolidated' ? _consolidatedBoost : mem.scope === 'pinned' ? 2.0 : 1.0
    const reflexionBoost = mem.scope === 'reflexion' ? _reflexionBoost : 1.0
    // Confidence factor (time decay removed — recency already covers age-based weighting)
    const confidenceWeight = mem.confidence ?? 0.7
    // Temporal validity: past facts (validUntil set and elapsed) get reduced weight but not zero
    const temporalWeight = (mem.validUntil && mem.validUntil > 0 && mem.validUntil < Date.now()) ? 0.3 : 1.0

    // Graph-augmented boost: memories mentioning related entities get a boost
    let graphBoost = 1.0
    if (expansionWords.size > 0) {
      const memLower = mem.content.toLowerCase()
      let graphHits = 0
      for (const w of expansionWords) {
        if (memLower.includes(w)) graphHits++
      }
      if (graphHits > 0) {
        graphBoost = 1.0 + Math.min(0.5, graphHits * 0.15)
      }
    }

    const impactBoost = getRecallImpactBoost(mem.content)
    // Archived memories participate in search but with reduced weight (DAG archive)
    const archiveWeight = mem.scope === 'archived' ? 0.3 : 1.0

    // ── Emotion-driven recall: mood/alertness influence memory scoring ──
    // Cognitive science: mood-congruent recall — your emotional state biases what you remember
    let moodMatchBoost = 1.0
    if (moodCtx) {
      // Strong mood congruence: emotional memories surface when mood matches
      if (moodCtx.mood > 0.3 && mem.emotion === 'warm') moodMatchBoost = 1.5
      else if (moodCtx.mood < -0.3 && mem.emotion === 'painful') moodMatchBoost = 1.5
      else if (moodCtx.mood < -0.3 && mem.emotion === 'warm') moodMatchBoost = 0.6  // happy memories suppressed when sad
      else if (moodCtx.mood > 0.3 && mem.emotion === 'painful') moodMatchBoost = 0.7  // painful suppressed when happy
      // High alertness: boost corrections and important memories (hyper-vigilant state)
      if (moodCtx.alertness > 0.7 && (mem.emotion === 'important' || mem.scope === 'correction')) moodMatchBoost *= 1.3

      // Fine-grained emotion congruence: same emotion type → boost
      if (eLabel && moodCtx) {
        try {
          const bodyM = getLazyModule('body'); const lastDetectedEmotion = bodyM?.lastDetectedEmotion
          if (lastDetectedEmotion && eLabel === lastDetectedEmotion.label) {
            moodMatchBoost *= 1.4 // same emotion state → strong context match
          }
        } catch {}
      }

      // Situational context match: same mood context at creation → boost
      if (mem.situationCtx?.mood !== undefined) {
        const moodDelta = Math.abs(moodCtx.mood - mem.situationCtx.mood)
        if (moodDelta < 0.3) moodMatchBoost *= 1.2 // similar mood state → context-dependent recall
      }
    }
    // Flashbulb memory effect: high emotional intensity → always easier to recall
    const ei = mem.emotionIntensity ?? 0
    if (ei >= 0.8) moodMatchBoost *= _flashbulbHigh  // "我永远记得那天..." 效应
    else if (ei >= 0.5) moodMatchBoost *= _flashbulbMedium

    // Weighted log-sum scoring (replaces multiplicative — avoids zero-product collapse)
    const _l = Math.log
    const _e = 0.01
    const logScore =
      getParam('recall.w_sim') * _l(sim + _e) + getParam('recall.w_recency') * _l(recency + _e) + getParam('recall.w_scope') * _l(scopeBoost)
      + getParam('recall.w_emotion') * _l(emotionBoost) + getParam('recall.w_user') * _l(userBoost) + getParam('recall.w_mood') * _l(consolidatedBoost)
      + 0.3 * _l(usageBoost) + 0.3 * _l(reflexionBoost) + getParam('recall.w_confidence') * _l(confidenceWeight + _e)
      + 0.5 * _l(temporalWeight + _e) + 0.7 * _l(graphBoost) + 0.3 * _l(tierWeight)
      + 0.3 * _l(impactBoost) + 0.2 * _l(archiveWeight) + getParam('recall.w_mood') * _l(moodMatchBoost)
      + 0.4 * _l(causalBoost)

    // ── State-Dependent Memory Gating (Godden & Baddeley 1975) ──
    // 在不同情绪/能量状态下，某些记忆更难被访问
    let stateGate = 1.0
    if (mem.situationCtx && moodCtx) {
      const moodDist = Math.abs((moodCtx.mood || 0) - (mem.situationCtx.mood || 0))
      const alertDist = Math.abs((moodCtx.alertness || 0) - (mem.situationCtx.alertness || 0))
      const stateDist = Math.sqrt(moodDist * moodDist + alertDist * alertDist)
      // sigmoid gate: 状态差异大 → gate 关闭
      stateGate = 1 / (1 + Math.exp(stateDist * 3 - 1.5))
      // 最低不低于 0.1（完全封锁太极端）
      stateGate = Math.max(0.1, stateGate)
    }

    // ── 编码特异性 (Encoding Specificity, Tulving 1983) ──
    // 如果当前话题和记忆创建时的话题相似 → boost
    // 不只看 mood 匹配，还看 topic/context 匹配
    let encodingBoost = 1.0
    if (mem.recallContexts && mem.recallContexts.length > 0) {
      // 用查询词和记忆的历史召回上下文比较
      const queryWordsStr = [...queryWords].join(' ')
      for (const ctx of mem.recallContexts) {
        const ctxWords = (ctx.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map((w: string) => w.toLowerCase())
        const overlap = ctxWords.filter((w: string) => queryWords.has(w)).length
        if (overlap >= 2) {
          encodingBoost = Math.max(encodingBoost, 1.0 + overlap * 0.1)  // 最高 1.5
          break
        }
      }
    }
    // 如果记忆有 tags 和当前查询高度匹配（编码时的标签 = 编码上下文）
    if (mem.tags && mem.tags.length > 0) {
      const tagHits = mem.tags.filter((t: string) => queryWords.has(t.toLowerCase())).length
      if (tagHits >= 3) encodingBoost = Math.max(encodingBoost, 1.3)
    }

    scored.push({ ...mem, score: logScore * stateGate * encodingBoost })
  }

  // ── Spreading Activation with IDF weighting: memories activate related memories ──
  // High-scoring memories "wake up" other memories that share keywords,
  // weighted by IDF so rare/distinctive words propagate more activation.
  if (scored.length >= 3) {
    // Pre-sort to pick top activators and limit spread candidates
    scored.sort((a, b) => b.score - a.score)
    const spreadLimit = Math.min(scored.length, topN * 3)
    const topActivators = scored.slice(0, 3).filter(s => s.score > 0.1)
    if (topActivators.length > 0) {
      // Build IDF-weighted activation map: word → IDF weight
      const idfMap = buildIDF()
      const activatedWordWeights = new Map<string, number>()
      for (const act of topActivators) {
        const words = (act.content.match(WORD_PATTERN.CJK24_EN3) || [])
        for (const w of words) {
          const wl = w.toLowerCase()
          const idfW = idfMap.get(wl) ?? 1.0
          activatedWordWeights.set(wl, Math.max(activatedWordWeights.get(wl) ?? 0, idfW))
        }
      }
      // Boost only top candidates with IDF-weighted activation score
      for (let si = 3; si < spreadLimit; si++) {
        const s = scored[si]
        const sWords = (s.content.match(WORD_PATTERN.CJK24_EN3) || []).map(w => w.toLowerCase())
        let activation = 0
        for (const w of sWords) {
          const wt = activatedWordWeights.get(w)
          if (wt !== undefined) activation += wt
        }
        if (activation > 0) {
          s.score *= (1 + Math.min(activation * 0.1, 0.5)) // IDF-weighted activation boost, capped +50%
        }
      }
    }
  }

  // ── 启动效应（Priming Effect）──
  // 人脑原理：刚看到"医生"，识别"护士"会更快（无意识激活扩散）
  // cc-soul 原创：最近 5 分钟内用户提到的词降低识别阈值，不是搜索而是启动
  const PRIMING_WINDOW_MS = 5 * 60 * 1000  // 5 分钟窗口
  const now = Date.now()
  if (_primingCache.size > 0) {
    for (const s of scored) {
      const sWords = (s.content.match(WORD_PATTERN.CJK2_EN3) || []).map(w => w.toLowerCase())
      let primingHits = 0
      for (const w of sWords) {
        const primedAt = _primingCache.get(w)
        if (primedAt && now - primedAt < PRIMING_WINDOW_MS) primingHits++
      }
      if (primingHits > 0 && sWords.length > 0) {
        const primingBoost = Math.min(0.3, primingHits / sWords.length)  // 最多 +30%
        s.score *= (1 + primingBoost)
      }
    }
  }

  scored.sort((a, b) => b.score - a.score)

  // ═══════════════════════════════════════════════════════════════════════════════
  // Dirichlet LM scoring (Bayesian smoothing language model, 2nd retrieval channel)
  // ═══════════════════════════════════════════════════════════════════════════════
  // Build corpus frequency map lazily for Dirichlet LM
  let _corpusFreq: Map<string, number> | null = null
  function getCorpusFreq(): Map<string, number> {
    if (_corpusFreq) return _corpusFreq
    _corpusFreq = new Map<string, number>()
    let total = 0
    for (const mem of activeMemories) {
      const tokens = bm25Tokenize(mem.content)
      for (const t of tokens) { _corpusFreq.set(t, (_corpusFreq.get(t) || 0) + 1); total++ }
    }
    _corpusFreq.set('__total__', total || 10000)
    return _corpusFreq
  }

  // ═══════════════════════════════════════════════════════════════════════════════
  // RRF (Reciprocal Rank Fusion) — multi-channel re-ranking
  // Each channel sorts independently, then fused via 1/(k+rank) to reduce
  // sensitivity to any single scoring dimension's scale.
  // ═══════════════════════════════════════════════════════════════════════════════
  if (scored.length >= 4) {
    // Build per-channel rank arrays using different sort keys
    // Channel 1: BM25/trigram sim (already primary factor in logScore, re-sort by sim component)
    const ch1 = scored.map((s, i) => ({ idx: i, key: s.score }))  // overall score as proxy for textual match
    // Channel 2: recency — newer memories ranked higher
    const ch2 = scored.map((s, i) => ({ idx: i, key: s.lastAccessed || s.ts || 0 }))
    ch2.sort((a, b) => b.key - a.key)
    // Channel 3: scope+emotion boost
    const ch3 = scored.map((s, i) => {
      const scopeW = (s.scope === 'correction') ? 3 : (s.scope === 'preference' || s.scope === 'fact') ? 2
        : (s.scope === 'consolidated') ? 2.5 : (s.scope === 'pinned') ? 4 : 1
      const emotionW = (s.emotion === 'important') ? 1.4 : (s.emotion === 'painful') ? 1.3 : 1.0
      const eiW = (s.emotionIntensity ?? 0) >= 0.8 ? 1.6 : (s.emotionIntensity ?? 0) >= 0.5 ? 1.2 : 1.0
      return { idx: i, key: scopeW * emotionW * eiW }
    })
    ch3.sort((a, b) => b.key - a.key)
    // Channel 4: graph/entity relevance (use graphBoost proxy — memories with expansion word hits)
    const ch4 = scored.map((s, i) => {
      let graphHits = 0
      if (expansionWords.size > 0) {
        const ml = s.content.toLowerCase()
        for (const w of expansionWords) { if (ml.includes(w)) graphHits++ }
      }
      return { idx: i, key: graphHits + (s.recallCount ?? 0) * 0.1 }
    })
    ch4.sort((a, b) => b.key - a.key)
    // Channel 5: Dirichlet LM — Bayesian language model scoring
    const cf = getCorpusFreq()
    const corpusSize = cf.get('__total__') || 10000
    const dirichletMu = 2000
    if (!bm25QueryTokens) bm25QueryTokens = new Set(bm25Tokenize(msg))
    const queryTermsArr = [...bm25QueryTokens]
    const ch5 = scored.map((s, i) => {
      const docTokens = _getDocTokens(s.content).words
      const docLen = docTokens.length
      if (docLen === 0) return { idx: i, key: -Infinity }
      let dlmScore = 0
      for (const qt of queryTermsArr) {
        const tf = docTokens.filter(t => t === qt).length
        const cfVal = cf.get(qt) || 1
        dlmScore += Math.log((tf + dirichletMu * cfVal / corpusSize) / (docLen + dirichletMu))
      }
      return { idx: i, key: dlmScore }
    })
    ch5.sort((a, b) => b.key - a.key)

    // Build rank maps: idx → rank (0-based)
    const rankMaps: Map<number, number>[] = []
    for (const channel of [ch1, ch2, ch3, ch4, ch5]) {
      const rm = new Map<number, number>()
      for (let r = 0; r < channel.length; r++) rm.set(channel[r].idx, r)
      rankMaps.push(rm)
    }

    // ── MAGMA 四图动态权重：根据查询意图调通道权重 ──
    const hasTimeKeyword = /上次|之前|昨天|上周|那次|上个月|以前/.test(msg)
    const isNegated = /不记得|忘了|想不起/.test(msg)
    const isCausalQuery = /为什么|怎么回事|原因|导致|因为/.test(msg)

    // 四图权重：[语义ch1, 时间ch2, scope/情绪ch3, 实体ch4, 语言模型ch5]
    let graphWeights = [0.3, 0.2, 0.2, 0.2, 0.1]  // 默认均匀
    if (hasTimeKeyword && !isNegated) {
      graphWeights = [0.1, 0.5, 0.1, 0.2, 0.1]  // 时间型查询
    } else if (isCausalQuery) {
      graphWeights = [0.1, 0.1, 0.1, 0.6, 0.1]  // 追因型 → 实体图（因果边在实体图上）
    } else if (cog?.spectrum?.information > 0.6) {
      graphWeights = [0.4, 0.1, 0.1, 0.3, 0.1]  // 信息型 → 语义+实体
    }

    // P5c: CWRF (Confidence-Weighted Rank Fusion) × MAGMA 图权重（两层加权）
    const RRF_K = 60
    const channelConfidences: number[] = []
    for (const channel of [ch1, ch2, ch3, ch4, ch5]) {
      if (channel.length >= 3) {
        const top1 = Math.max(0.001, channel[0]?.score ?? 0.001)
        const top2 = Math.max(0.001, channel[1]?.score ?? 0.001)
        channelConfidences.push(Math.min(3, top1 / top2))
      } else {
        channelConfidences.push(1.0)  // 样本不足，不加权
      }
    }

    for (let i = 0; i < scored.length; i++) {
      let cwrfScore = 0
      for (let c = 0; c < rankMaps.length; c++) {
        const rank = rankMaps[c].get(i) ?? scored.length
        cwrfScore += channelConfidences[c] * graphWeights[c] / (RRF_K + rank)
      }
      scored[i].score = 0.6 * scored[i].score + 0.4 * (cwrfScore * 1000)
    }
    scored.sort((a, b) => b.score - a.score)
  }

  const topResults = mmrRerank(scored.slice(0, topN * 3), topN)

  // ── Graph Walk Recall: supplement with memories reachable via entity graph BFS ──
  if (mentionedEntities.length > 0 && topResults.length < topN) {
    const topContents = new Set(topResults.map(r => r.content))
    for (const entity of mentionedEntities) {
      const walked = graphWalkRecall(entity, memoryState.memories, 2, 6)
      for (const wContent of walked) {
        if (topContents.has(wContent) || topResults.length >= topN) break
        const mem = _contentMap.get(wContent)
        if (mem) {
          topResults.push({ ...mem, score: 0 })
          topContents.add(wContent)
        }
      }
    }
  }

  // Boost confidence + update lastAccessed + recallCount on recalled memories
  for (const result of topResults) {
    const mem = _memLookup.get(`${result.content}\0${result.ts}`)
    if (mem) {
      mem.lastAccessed = Date.now()
      mem.recallCount = (mem.recallCount ?? 0) + 1
      mem.lastRecalled = Date.now()

      // ── 测试效应 (Testing Effect, Roediger 2006) ──
      // 越难回忆的记忆（score 越低），成功召回后强化越大
      // score 高 = 容易回忆 = 小幅强化（+0.01）
      // score 低 = 困难回忆 = 大幅强化（+0.05）
      const retrievalDifficulty = 1 - Math.min(1, result.score / 0.5)  // score 越低难度越高
      const testingBoost = 0.01 + retrievalDifficulty * 0.04  // 范围 [0.01, 0.05]
      // 用 testingBoost 作为 bayesBoost 的 delta（替代固定 0.5）
      bayesBoost(mem, 0.3 + retrievalDifficulty * 0.7)  // Bayesian posterior: 困难召回 → 更大 alpha 增量
      mem.confidence = Math.min(1.0, (mem.confidence ?? 0.7) + testingBoost)

      // FSRS 稳定度也受测试效应影响
      if (mem.fsrs) {
        const difficultyBonus = 1 + retrievalDifficulty * 0.5  // 困难召回 → stability 增长更多
        try {
          const { fsrsUpdate } = require('./smart-forget.ts')
          const ageDays = (Date.now() - (mem.ts || Date.now())) / 86400000
          const rating = difficultyBonus > 1.2 ? 4 : 3  // hard recall = stronger learning
          mem.fsrs = fsrsUpdate(mem.fsrs, rating, ageDays)
        } catch {
          mem.fsrs.stability *= difficultyBonus  // fallback
        }
      }

      syncToSQLite(mem, { confidence: mem.confidence, recallCount: mem.recallCount, lastAccessed: mem.lastAccessed, lastRecalled: mem.lastRecalled })
      // Memory reconsolidation: recalled memories absorb current context
      // Like human memory — each recall slightly modifies the memory
      if (!mem.recallContexts) mem.recallContexts = []
      const ctxSnippet = msg.slice(0, 40)
      if (!mem.recallContexts.includes(ctxSnippet)) {
        mem.recallContexts.push(ctxSnippet)
        if (mem.recallContexts.length > 5) mem.recallContexts.shift()
      }

      // Deep reconsolidation: after 5+ recalls in different contexts,
      // append a "[多次被提及]" marker to help LLM understand importance
      if ((mem.recallCount ?? 0) >= 5 && !mem.content.includes('[多次被提及]')) {
        const uniqueContexts = new Set(mem.recallContexts).size
        if (uniqueContexts >= 3) {
          // Save original to history before modifying
          if (!mem.history) mem.history = []
          mem.history.push({ content: mem.content, ts: Date.now() })
          mem.content = `[多次被提及] ${mem.content}`
          mem.tier = 'long_term'  // promote to long-term
          syncToSQLite(mem, { content: mem.content, tier: mem.tier })
        }
      }

      // ── 活性记忆网络：实时微蒸馏 (Living Memory Network) ──
      // 每次 recall 命中时，提取"为什么这条记忆和这个查询相关"的微连接
      // 零 LLM 调用，纯规则提取
      try {
        // 提取 query 和 memory 的共享关键词（这就是"为什么相关"的原因）
        const memWords = (result.content.match(WORD_PATTERN.CJK24_EN3) || []).map((w: string) => w.toLowerCase())
        const sharedWords = memWords.filter((w: string) => queryWords.has(w))

        if (sharedWords.length >= 1) {
          // 生成微连接：query_context → memory_topic → shared_keywords
          const microLink = {
            query: msg.slice(0, 40),
            memoryRef: result.content.slice(0, 40),
            sharedKeywords: sharedWords.slice(0, 5),
            ts: Date.now(),
          }

          // 存入记忆的 microLinks 数组
          if (!mem.microLinks) mem.microLinks = []
          mem.microLinks.push(microLink)
          if (mem.microLinks.length > 10) mem.microLinks.shift()  // 保留最近 10 条

          // 微连接累积检测：如果同一组关键词出现 3+ 次，涌现为话题标签
          const keywordFreq = new Map<string, number>()
          for (const link of mem.microLinks) {
            for (const kw of link.sharedKeywords) {
              keywordFreq.set(kw, (keywordFreq.get(kw) || 0) + 1)
            }
          }
          for (const [kw, freq] of keywordFreq) {
            if (freq >= 3 && mem.tags && !mem.tags.includes(kw)) {
              mem.tags.push(kw)
              console.log(`[cc-soul][living-network] emergent tag: "${kw}" on memory "${mem.content.slice(0, 30)}"`)
            }
          }
        }
      } catch {}
    }
  }
  if (topResults.length > 0) saveMemories()

  // ── Hybrid: merge with OpenClaw native memory (FTS5 full-text search) ──
  try {
    const ocMemDb = resolve(homedir(), '.openclaw/memory/main.sqlite')
    if (existsSync(ocMemDb)) {
      const { DatabaseSync } = require('node:sqlite')
      const db = new DatabaseSync(ocMemDb, { open: true, readOnly: true })
      const ftsResults = db.prepare(
        `SELECT text, path FROM chunks_fts WHERE chunks_fts MATCH ? ORDER BY rank LIMIT ?`
      ).all(msg.replace(/['"*(){}^~<>|\\]/g, '').replace(/\b(AND|OR|NOT|NEAR)\b/gi, ''), topN) as { text: string; path: string }[]
      db.close()

      if (ftsResults.length > 0) {
        // Merge: add OpenClaw results that aren't already in cc-soul results
        const existingContents = new Set(topResults.map(r => r.content.slice(0, 200)))
        for (const fts of ftsResults) {
          if (!existingContents.has(fts.text.slice(0, 200))) {
            topResults.push({
              content: fts.text,
              scope: 'fact',
              ts: Date.now(),
              source: 'openclaw-memory',
              confidence: 0.7,
              recallCount: 0,
              lastAccessed: Date.now(),
            } as Memory)
          }
        }
        console.log(`[cc-soul][memory-hybrid] merged ${ftsResults.length} OpenClaw FTS results`)
      }
    }
  } catch { /* OpenClaw memory unavailable — no problem, cc-soul recall is primary */ }

  // ── Track recall stats ──
  recallStats.total++
  if (topResults.length > 0) recallStats.successful++
  // P0-1: periodic reset to prevent unbounded growth
  if (recallStats.total > 1000) {
    recallStats.rate = recallStats.successful / recallStats.total
    recallStats.total = 0
    recallStats.successful = 0
  }

  return topResults
}

// ═══════════════════════════════════════════════════════════════════════════════
// Meta-memory: Tip-of-Tongue recall
// ═══════════════════════════════════════════════════════════════════════════════

/** Detect if user is explicitly asking about past memories */
const MEMORY_RECALL_TRIGGERS = /你还记得|你记不记得|之前说过|上次提到|我们聊过|你忘了吗|还记得吗|do you remember|did i mention|we talked about|you forgot/i

// ═══════════════════════════════════════════════════════════════════════════════
// 认知双通道召回 (Cognitive Dual-Channel Recall)
//
// System 1 (直觉，<5ms)：fact-store hash 查询 + core memory 精确匹配
//   → "我叫什么" "我在哪工作" "我喜欢什么" 这类问题秒回
//   → 90% 的日常查询在这里结束
//
// System 2 (推理，<50ms)：BM25 + trigram + 图谱 + 所有增强
//   → "上次聊的那个话题" "为什么选 Go" 这类复杂查询
//   → 只有 System 1 没命中时才走
//
// 自适应切换：查询复杂度 > 阈值 → 直接跳到 System 2
// ═══════════════════════════════════════════════════════════════════════════════

const SYSTEM2_KEYWORDS = /为什么|怎么看|如何|对比|区别|上次|之前|总结|分析|比较|回顾|why|how come|compare|difference|last time|before|summarize|analyze|review/i

/** Predicate → 中文可读标签 */
const PRED_LABELS: Record<string, string> = {
  likes: '喜欢', dislikes: '讨厌', works_at: '在', lives_in: '住在',
  uses: '用', has_pet: '养了', has_family: '有', habit: '习惯',
  occupation: '职业是', age: '年龄', educated_at: '毕业于',
  relationship: '的伴侣', uses_os: '用', prefers: '偏好', family_name: '的',
}

/** Fact query pattern → predicate 映射 */
const FACT_QUERY_PATTERNS: { pattern: RegExp; predicates: string[] }[] = [
  { pattern: /叫什么|我是谁|名字|what.?s my name|who am i|my name/i, predicates: [] },  // empty = all user facts
  { pattern: /工作|公司|在哪.*工作|上班|where do i work|my job|my company|what do i do/i, predicates: ['works_at', 'occupation'] },
  { pattern: /住哪|住在|地址|where do i live|my address|where.?m i based/i, predicates: ['lives_in'] },
  { pattern: /喜欢|偏好|最爱|what do i like|my favorite|my preference/i, predicates: ['likes', 'prefers'] },
  { pattern: /讨厌|不喜欢|受不了|what do i hate|what do i dislike/i, predicates: ['dislikes'] },
  { pattern: /职业|做什么的|my occupation|what.?s my job/i, predicates: ['occupation'] },
  { pattern: /多大|几岁|年龄|how old|my age/i, predicates: ['age'] },
  { pattern: /宠物|猫|狗|养|my pet|my cat|my dog/i, predicates: ['has_pet'] },
  { pattern: /家人|女儿|儿子|孩子|老婆|老公|my family|my daughter|my son|my kid|my wife|my husband/i, predicates: ['has_family', 'family_name', 'relationship'] },
  { pattern: /习惯|每天|my habit|my routine|daily/i, predicates: ['habit'] },
  { pattern: /用什么|电脑|设备|what do i use|my computer|my device/i, predicates: ['uses', 'uses_os'] },
  { pattern: /喝什么|饮料|咖啡|茶|what do i drink|coffee|tea/i, predicates: ['likes', 'dislikes'] },
  { pattern: /毕业|学校|大学|my school|my university|where did i graduate/i, predicates: ['educated_at'] },
]

function system1FastRecall(msg: string, topN: number, _userId?: string): Memory[] | null {
  // 长查询或含推理词 → 直接走 System 2
  if (msg.length > 30) return null
  if (SYSTEM2_KEYWORDS.test(msg)) return null

  const results: Memory[] = []

  // ── Channel A: Fact-Store Hash 查询（SQLite indexed / O(1) in-memory）──
  try {
    const matchedPredicates = new Set<string>()
    let matchedAny = false

    for (const { pattern, predicates } of FACT_QUERY_PATTERNS) {
      if (pattern.test(msg)) {
        matchedAny = true
        if (predicates.length === 0) {
          // 无具体 predicate → 查所有 user facts
          const allFacts = queryFacts({ subject: 'user' })
          for (const f of allFacts) {
            const label = PRED_LABELS[f.predicate] || f.predicate
            results.push({
              content: `用户${label}${f.object}`,
              scope: 'fact',
              ts: f.ts || Date.now(),
              confidence: f.confidence || 0.8,
              source: 'system1_fact',
            } as Memory)
          }
        } else {
          for (const pred of predicates) {
            if (matchedPredicates.has(pred)) continue
            matchedPredicates.add(pred)
            const facts = queryFacts({ subject: 'user', predicate: pred })
            for (const f of facts) {
              const label = PRED_LABELS[f.predicate] || f.predicate
              results.push({
                content: `用户${label}${f.object}`,
                scope: 'fact',
                ts: f.ts || Date.now(),
                confidence: f.confidence || 0.8,
                source: 'system1_fact',
              } as Memory)
            }
          }
        }
      }
    }

    if (!matchedAny) {
      // 没匹配到任何 pattern → Channel A 无结果，继续 Channel B
    }
  } catch { /* fact-store 不可用时静默降级 */ }

  // ── Channel B: Core Memory 精确匹配 ──
  try {
    if (coreMemories && coreMemories.length > 0) {
      const queryWords = (msg.match(/[\u4e00-\u9fff]+|[a-z]{3,}/gi) || []).map((w: string) => w.toLowerCase())
      if (queryWords.length > 0 && queryWords.length <= 3) {
        for (const cm of coreMemories) {
          const cmLower = (cm.content || '').toLowerCase()
          const hits = queryWords.filter((w: string) => cmLower.includes(w)).length
          if (hits >= 1) {
            // 避免与 Channel A 重复
            const dup = results.some(r => r.content.includes(cm.content.slice(0, 20)))
            if (!dup) {
              results.push({
                content: cm.content,
                scope: cm.category || 'fact',
                ts: cm.addedAt || Date.now(),
                confidence: 0.9,
                source: 'system1_core',
              } as Memory)
            }
          }
        }
      }
    }
  } catch { /* core memory 不可用时静默降级 */ }

  // System 1 命中判定：至少有 1 条结果才算命中
  if (results.length > 0) {
    console.log(`[cc-soul][recall] System 1 hit: ${results.length} results (dual-channel)`)
    return results.slice(0, topN)
  }

  return null  // System 1 未命中，降级到 System 2
}

/** Public recall — strips internal score field from results. Merges OpenClaw native memory if available. */
export function recall(msg: string, topN = 3, userId?: string, channelId?: string, moodCtx?: { mood: number; alertness: number }, opts?: { awaitVector?: boolean }, cogHints?: any): Memory[] {
  if (!msg || memoryState.memories.length === 0) return []

  // ── 认知负荷自适应：根据消息复杂度动态调整 topN ──
  // benchmark 环境跳过（benchmark 需要完整 top-K 评估召回质量）
  if (!process.env.CC_SOUL_BENCHMARK) {
    try {
      const { getInjectionStrategy, shouldInjectMemories } = require('./cognitive-load.ts')
      if (!shouldInjectMemories(msg)) return []
      const strategy = getInjectionStrategy(msg)
      if (strategy.topN < topN) topN = strategy.topN  // 只降不升（调用者的 topN 是上限）
    } catch {}
  }

  // P3: 推进 A/B 通道实验计数器（benchmark 跳过）
  if (!process.env.CC_SOUL_BENCHMARK) tickABExperiment()

  // 启动效应：记录用户刚提到的词，降低相关记忆的识别阈值
  updatePrimingCache(msg)

  // ── 指代消解：查询扩展（"他怎么样了" → "他怎么样了 张三"）──
  // benchmark 环境跳过（英文数据集无中文指代消解需求，反而可能加噪声）
  const _expandedMsg = process.env.CC_SOUL_BENCHMARK ? msg : expandQueryWithCoreference(msg, memoryState.chatHistory)

  // ── 路由过滤：量大时缩小候选集，量少时全量扫描 ──
  // benchmark 环境跳过路由过滤（全量扫描更精准）
  const candidates = process.env.CC_SOUL_BENCHMARK ? memoryState.memories : routeMemories(memoryState.memories, _expandedMsg, userId)

  // ── 统一激活场：唯一的召回路径 ──
  try {
    const { activationRecall } = require('./activation-field.ts')
    const results: Memory[] = activationRecall(
      candidates,
      _expandedMsg,
      topN,
      moodCtx?.mood || 0,
      moodCtx?.alertness || 0.5,
      cogHints || null,
    )
    if (results.length > 0) console.log(`[cc-soul][recall] activationRecall returned ${results.length} results, top: "${(results[0]?.content||'').slice(0,40)}"`)

    // ── Graveyard 复活：当结果不足时 fallback 查 graveyard ──
    if (results.length < 3) {
      try {
        const { reviveFromGraveyard } = require('./smart-forget.ts')
        const revived = reviveFromGraveyard(msg, memoryState.memories, 3 - results.length)
        if (revived.length > 0) {
          results.push(...revived)
        }
      } catch {}
    }

    // 更新召回统计
    recallStats.total++
    if (results.length > 0) recallStats.successful++
    if (recallStats.total > 1000) {
      recallStats.rate = recallStats.successful / recallStats.total
      recallStats.total = 0; recallStats.successful = 0
    }

    // 召回后更新记忆元数据（再固化）
    for (const mem of results) {
      const original = _memLookup.get(`${mem.content}\0${mem.ts}`) || _contentMap.get(mem.content)
      if (original) {
        original.lastAccessed = Date.now()
        original.recallCount = (original.recallCount ?? 0) + 1
        original.lastRecalled = Date.now()
        // Bayesian confidence update
        const idx = results.indexOf(mem)
        const difficulty = idx / Math.max(1, results.length)
        try {
          _posEvidence(original, difficulty)
        } catch {
          original.confidence = Math.min(1.0, (original.confidence ?? 0.7) + 0.02)
        }
        // FSRS update
        if ((original as any).fsrs) {
          try {
            const { fsrsUpdate } = require('./smart-forget.ts')
            const ageDays = (Date.now() - (original.ts || Date.now())) / 86400000
            const rating = difficulty < 0.3 ? 4 : difficulty < 0.7 ? 3 : 2
            ;(original as any).fsrs = fsrsUpdate((original as any).fsrs, rating, ageDays)
          } catch {}
        }

        // SQLite 同步（benchmark 跳过——不需要持久化，且是主要延迟源）
        if (!process.env.CC_SOUL_BENCHMARK) {
          syncToSQLite(original, { confidence: original.confidence, recallCount: original.recallCount, lastAccessed: original.lastAccessed, lastRecalled: original.lastRecalled })
        }

        // ── microLinks 写入（activationRecall 路径）：积累激活链结晶 ──
        try {
          const queryWords = new Set((_expandedMsg.match(WORD_PATTERN.CJK24_EN3) || []).map((w: string) => w.toLowerCase()))
          const memWords = (original.content.match(WORD_PATTERN.CJK24_EN3) || []).map((w: string) => w.toLowerCase())
          const shared = memWords.filter((w: string) => queryWords.has(w))
          if (shared.length >= 1) {
            if (!original.microLinks) original.microLinks = []
            original.microLinks.push({
              query: _expandedMsg.slice(0, 40),
              memoryRef: original.content.slice(0, 40),
              sharedKeywords: shared.slice(0, 5),
              ts: Date.now(),
            })
            if (original.microLinks.length > 10) original.microLinks.shift()
          }
        } catch {}
      }
    }
    // ── 检索诱发遗忘（Retrieval-Induced Forgetting）──
    // 人脑原理：回忆 A 会抑制跟 A 相关但未被选中的 B（Anderson et al. 1994）
    // cc-soul 原创：召回的记忆变强，竞争者轻微降权，让记忆库自然分化
    if (results.length > 0) {
      const recalledContents = new Set(results.map(r => r.content))
      const recalledWords = new Set<string>()
      for (const r of results) {
        const words = (r.content.match(WORD_PATTERN.CJK2_EN3) || [])
        for (const w of words) recalledWords.add(w.toLowerCase())
      }
      // 对未被选中但关键词重叠的记忆轻微抑制
      for (const m of memoryState.memories) {
        if (!m || !m.content || recalledContents.has(m.content)) continue
        if (m.scope === 'core_memory' || m.scope === 'correction') continue  // 核心和纠正不抑制
        const mWords = (m.content.match(WORD_PATTERN.CJK2_EN3) || [])
        let overlap = 0
        for (const w of mWords) { if (recalledWords.has(w.toLowerCase())) overlap++ }
        if (overlap >= 3 && mWords.length > 0 && overlap / mWords.length > 0.4) {
          // 高度相关但未被选中 → 轻微抑制（Bayesian negative evidence）
          const oldConf = m.confidence ?? 0.7
          try {
            _negEvidence(m, overlap / mWords.length * 0.3)  // strength proportional to overlap ratio, scaled down
          } catch {
            m.confidence = Math.max(0.1, oldConf - 0.02)
          }
          try { require('./decision-log.ts').logDecision('rif_suppress', (m.content || '').slice(0, 30) + '|' + m.ts, `conf=${oldConf.toFixed(2)}→${m.confidence.toFixed(2)}, overlap=${overlap}/${mWords.length}`) } catch {}
        }
      }
    }

    // ── 预热命中清理：清除 _preheated 标记，记录命中率 ──
    for (const m of memoryState.memories) {
      if (m && m._preheated) {
        const wasUsed = results.some(r => r.content === m.content)
        if (wasUsed) {
          try { require('./decision-log.ts').logDecision('preheat_hit', (m.content || '').slice(0, 30), 'preheated memory was recalled') } catch {}
        }
        delete m._preheated
      }
    }

    if (results.length > 0) saveMemories()

    // ── 预测性启动：用 AAM 时序后继为下一轮预热记忆 ──
    try { predictivePrime(results, memoryState.memories) } catch {}

    return results
  } catch (e: any) {
    console.log(`[cc-soul][recall] activation-field error: ${e.message}, fallback to legacy`)
  }

  // ── Fallback：只在激活场出错时走旧路径 ──
  // 保留 recallWithScores 作为紧急 fallback，但正常情况不会走到这里
  return recallWithScores(msg, topN, userId, channelId, moodCtx).map(({ score, ...rest }) => rest) as Memory[]
}

// Cache vector results from async search for synchronous use in next turn
let _lastVectorResults: Memory[] = []
let _lastVectorResultsKey = ''

// ── Read from OpenClaw native memory (cc.sqlite FTS) ──

let _openclawMemDb: any = null
let _openclawMemDbAttempted = false

function getOpenClawMemDb() {
  if (_openclawMemDbAttempted) return _openclawMemDb
  _openclawMemDbAttempted = true
  try {
    const Database = require('better-sqlite3')
    const dbPath = resolve(homedir(), '.openclaw/memory/cc.sqlite')
    if (existsSync(dbPath)) {
      _openclawMemDb = new Database(dbPath, { readonly: true, fileMustExist: true })
    }
  } catch (_) {
    // better-sqlite3 not available or db doesn't exist
  }
  return _openclawMemDb
}

/** Lightweight JSON file search — reads file, filters by keyword, no full memory load */
function recallFromJsonFile(msg: string, topN: number): Memory[] {
  try {
    const memPath = resolve(DATA_DIR, 'memories.json')
    if (!existsSync(memPath)) return []
    const data = loadJson(memPath, []) as Memory[]
    const keywords = (msg.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map(w => w.toLowerCase())
    if (keywords.length === 0) return []

    const scored: (Memory & { score: number })[] = []
    for (const m of data) {
      if (m.scope === 'expired' || m.scope === 'decayed') continue
      const content = m.content.toLowerCase()
      const tags = (m.tags || []).map((t: string) => t.toLowerCase())
      let hits = 0
      for (const kw of keywords) {
        if (content.includes(kw) || tags.some(t => t.includes(kw) || kw.includes(t))) hits++
      }
      if (hits === 0) continue
      const sim = hits / Math.max(1, keywords.length)
      const scopeBoost = m.scope === 'preference' || m.scope === 'fact' ? 1.3 : m.scope === 'correction' ? 1.5 : 1.0
      const archiveWeight = m.scope === 'archived' ? 0.3 : 1.0
      scored.push({ ...m, score: sim * scopeBoost * archiveWeight })
    }

    scored.sort((a, b) => b.score - a.score)
    return scored.slice(0, topN).map(({ score, ...rest }) => rest) as Memory[]
  } catch (e: any) {
    console.error(`[cc-soul][recall] JSON file search failed: ${e.message}`)
    return []
  }
}

function recallFromOpenClawMemory(msg: string, topN: number): Memory[] {
  const db = getOpenClawMemDb()
  if (!db) return []

  try {
    // Use FTS if available
    const results = db.prepare(
      `SELECT text, updated_at FROM chunks WHERE text LIKE ? ORDER BY updated_at DESC LIMIT ?`
    ).all(`%${msg.slice(0, 20)}%`, topN) as any[]

    return results.map((r: any) => ({
      content: r.text,
      scope: 'fact' as string,
      ts: r.updated_at || Date.now(),
      emotion: 'neutral' as string,
      confidence: 0.5,
      tier: 'long_term' as const,
    }))
  } catch (_) {
    return []
  }
}

/**
 * Multi-modal recall fusion: combines tag/trigram/BM25 (recall()) with SQLite vector search.
 * Results found by multiple strategies get a confidence boost (ensemble agreement).
 * Falls back to recall() when vector search is unavailable or errors.
 */
let cachedFusedRecall: { query: string; results: Memory[]; ts: number } | null = null

export function getCachedFusedRecall(): Memory[] {
  if (!cachedFusedRecall) return []
  if (Date.now() - cachedFusedRecall.ts > 300000) { // 5 min expiry
    cachedFusedRecall = null
    return []
  }
  return cachedFusedRecall.results
}

let idfInvalidateCount = 0
/** Incremental IDF update for a single new document — avoids full O(n) rebuild */
export function incrementalIDFUpdate(content: string) {
  if (!idfCache) return // no cache built yet, buildIDF() will do full build on next recall
  const words = (content.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map(w => w.toLowerCase())
  if (words.length === 0) return
  const N = memoryState.memories.length || 1
  const unique = new Set(words)
  for (const w of unique) {
    // Approximate: increment df, recompute idf for this word only
    const oldIdf = idfCache.get(w)
    const oldDf = oldIdf !== undefined ? Math.round(N / Math.exp(oldIdf)) - 1 : 0
    const newDf = oldDf + 1
    idfCache.set(w, Math.log(N / (1 + newDf)))
  }
  // Update avgDocLen incrementally
  if (avgDocLenCache !== null) {
    const prevTotal = avgDocLenCache * (N - 1)
    avgDocLenCache = (prevTotal + words.length) / N
  }
}
export function invalidateIDF() {
  // Throttle: don't invalidate if IDF was rebuilt less than 60s ago AND under 50 calls
  // This prevents O(n) rebuild on every addMemory when memories are added in bursts
  idfInvalidateCount++
  if (idfInvalidateCount < 50 && idfCache && (Date.now() - lastIdfBuildTs < 60000)) return
  idfCache = null
  avgDocLenCache = null
  idfInvalidateCount = 0
  _bm25TokenCache.clear()
}

/**
 * Degrade confidence of a memory when it's contradicted or corrected.
 * If confidence drops to ≤0.1, mark as expired (too unreliable).
 */
export function degradeMemoryConfidence(content: string) {
  const mem = memoryState.memories.find(m => m.content === content)
  if (mem) {
    bayesCorrect(mem, 2)  // strong negative: β += 2 (user correction)
    if (mem.confidence <= 0.1) {
      mem.scope = 'expired'
    }
    syncToSQLite(mem, { confidence: mem.confidence, scope: mem.scope })
    saveMemories()
    console.log(`[cc-soul][confidence] degraded: "${content.slice(0, 50)}" → ${mem.confidence.toFixed(2)}${mem.scope === 'expired' ? ' (expired)' : ''}`)
  }
}
