/**
 * benchmark-locomo.ts — LOCOMO-MC10 基准测试
 *
 * 两层测试：
 *   Layer 1: 召回质量（Hit@K, MRR）— 测 NAM 引擎本身
 *   Layer 2: 端到端准确率（10 选 1）— 测 NAM + 答案选择
 *
 * 用法: npx tsx cc-soul/benchmark-locomo.ts [--conv N] [--type TYPE] [--top-k K] [--verbose] [--limit N]
 *       npx tsx cc-soul/benchmark-locomo.ts --recall-only [--conv N] [--type TYPE] [--top-k K]
 *       npx tsx cc-soul/benchmark-locomo.ts --llm [--conv N] [--limit 200]
 */

import { readFileSync, existsSync } from 'fs'
import { resolve, dirname, join } from 'path'
import { createRequire } from 'module'
import { fileURLToPath } from 'url'
import type { Memory } from './types.ts'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)
const require = createRequire(import.meta.url)
;(globalThis as any).require = require
process.env.CC_SOUL_BENCHMARK = "1"

// Suppress noisy logs during benchmark
const _origLog = console.log
const _origWarn = console.warn
let suppressLogs = false
console.log = (...args: any[]) => { if (!suppressLogs) _origLog(...args) }
console.warn = (...args: any[]) => { if (!suppressLogs) _origWarn(...args) }
const print = _origLog  // always prints

// Lazy-load modules
const { activationRecall, activationRecallWithScores, getIdfCache } = require('./activation-field.ts')
const { learnAssociation } = require('./aam.ts')
const { trigrams, trigramSimilarity } = require('./memory-utils.ts')
const { toCogHints } = require('./cognition.ts')

// ═══════════════════════════════════════════════════════════════
// DATA TYPES
// ═══════════════════════════════════════════════════════════════

interface LocomoQuestion {
  question_id: string
  question: string
  question_type: string
  answer: string
  correct_choice_index: number
  num_choices: number
  num_sessions: number
  choices: string[]
  haystack_session_ids: string[]
  haystack_session_summaries: string[]
  haystack_session_datetimes: string[]
  haystack_sessions: Array<Array<{ role: string; content: string }>>
}

// ═══════════════════════════════════════════════════════════════
// DATA LOADING
// ═══════════════════════════════════════════════════════════════

function loadDataset(): LocomoQuestion[] {
  const dataPath = resolve(__dirname, '../data/locomo_mc10.json')
  const raw = readFileSync(dataPath, 'utf-8')
  const questions: LocomoQuestion[] = []
  for (const line of raw.split('\n')) {
    const trimmed = line.trim()
    if (trimmed) questions.push(JSON.parse(trimmed))
  }
  return questions
}

// ═══════════════════════════════════════════════════════════════
// MEMORY CONSTRUCTION
// ═══════════════════════════════════════════════════════════════

function buildMemories(q: LocomoQuestion): Memory[] {
  const memories: Memory[] = []

  // ── 时间归一化：保持 session 间的相对间隔，平移到最近 ──
  // LOCOMO 对话来自 2023 年，ACT-R 对 3 年前的记忆给出 ≈0 的基础激活。
  // 真实场景下记忆是持续更新的。我们保持对话间的相对时间间隔，
  // 但把最后一个 session 的时间设为"1天前"，其余按比例回推。
  const originalTimestamps = q.haystack_session_datetimes.map(d => new Date(d).getTime())
  const minTs = Math.min(...originalTimestamps)
  const maxTs = Math.max(...originalTimestamps)
  const timeSpan = Math.max(maxTs - minTs, 1)
  const now = Date.now()
  // 映射：最早的 session → N 天前，最晚的 → 1 小时前
  // 压缩到最近 14 天内（ACT-R 对超过 30 天的记忆激活值趋零）
  const TARGET_SPAN = 30 * 86400000  // 30 天（ACT-R 对 14 天前记忆激活值趋零，30 天分化更好）
  const TARGET_END = now - 3600000   // 1 小时前

  function normalizeTs(originalTs: number): number {
    const ratio = (originalTs - minTs) / timeSpan  // 0 = earliest, 1 = latest
    return TARGET_END - TARGET_SPAN * (1 - ratio)
  }

  for (let si = 0; si < q.haystack_sessions.length; si++) {
    const session = q.haystack_sessions[si]
    const baseTs = normalizeTs(originalTimestamps[si])

    // Session summary → high-level distilled memory
    // Summary 代表蒸馏知识，在真实系统中会被持续访问（每次 recall 都可能触及）
    const summary = q.haystack_session_summaries[si]
    if (summary) {
      memories.push({
        content: summary,
        scope: 'fact',
        ts: baseTs,
        confidence: 0.95,
        recallCount: 10,
        lastAccessed: now - 3600000,
        importance: 8,
        tags: ['summary'],
        _segmentId: si,
      } as Memory)
    }

    // Each turn → episode memory（带精确日期前缀 + 原始事件时间）
    const _epDatePrefix = `[${new Date(originalTimestamps[si]).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}]`
    for (let ti = 0; ti < session.length; ti++) {
      const turn = session[ti]
      const content = turn?.content
      if (!content || content.length < 10) continue
      const role = turn?.role || 'unknown'

      const memTs = baseTs + ti * 60000
      memories.push({
        content: `${_epDatePrefix} ${content}`,
        scope: 'episode',
        ts: memTs,
        confidence: 0.8,
        recallCount: 3,
        lastAccessed: Math.min(now - 7200000, memTs + 86400000),
        importance: 5,
        tags: [`speaker:${role}`, `session:${si}`],
        _segmentId: si,
        _eventDate: originalTimestamps[si] + ti * 60000,
      } as Memory)
    }

    // ── Sliding Window Memory Merging：步长 2 跳步合并，减少记忆膨胀 ──
    for (let ti = 0; ti < session.length - 1; ti += 2) {  // 步长 2 不重叠
      const turns = session.slice(ti, ti + 3).filter(t => t?.content?.length >= 10)
      if (turns.length >= 2) {
        const merged = turns.map(t => t.content).join(' ')
        if (merged.length > 30 && merged.length < 500) {
          const memTs = baseTs + ti * 60000 + 30000
          memories.push({
            content: `${_epDatePrefix} ${merged}`,
            scope: 'episode',
            ts: memTs,
            confidence: 0.75,
            recallCount: 2,
            lastAccessed: Math.min(now - 7200000, memTs + 86400000),
            importance: 3,
            tags: [`merged:${ti}`, `session:${si}`],
            _segmentId: si,
            _eventDate: originalTimestamps[si] + ti * 60000 + 30000,
          } as Memory)
        }
      }
    }
  }

  // ── Gist Trace：情节要旨痕迹（原创，Fuzzy Trace Theory 启发）──
  // 不改 content（Document Expansion 验证伤分），而是存独立的 gist 结构
  // 匹配在 gist 层做，作为 activation field 的独立信号，不污染 BM25
  // 提取：动词骨架 + 情感极性 + 抽象主题标签
  const POSITIVE_WORDS = new Set(['happy','excited','love','great','amazing','wonderful','enjoy','fun','glad','proud','beautiful','awesome','fantastic','celebrate','perfect','thrilled','delighted'])
  const NEGATIVE_WORDS = new Set(['sad','angry','frustrated','stressed','worried','anxious','tired','upset','disappointed','hurt','scared','lonely','overwhelmed','painful','annoyed','difficult','struggled'])
  const ABSTRACT_MAP: Record<string, string[]> = {
    'moved': ['relocation','change'], 'travel': ['journey','adventure'], 'bought': ['acquisition','purchase'],
    'lost': ['loss','misfortune'], 'won': ['achievement','success'], 'failed': ['setback','failure'],
    'married': ['relationship','milestone'], 'graduated': ['education','achievement'], 'hired': ['career','opportunity'],
    'fired': ['career','setback'], 'adopted': ['family','decision'], 'volunteered': ['community','service'],
    'painted': ['art','hobby'], 'hiked': ['outdoor','activity'], 'camped': ['outdoor','adventure'],
    'cooked': ['food','hobby'], 'read': ['reading','learning'], 'played': ['music','hobby','activity'],
  }
  for (const mem of memories) {
    const c = (mem.content || '').toLowerCase()
    const words = c.match(/[a-z]{3,}/g) || []
    // 情感极性
    const posHits = words.filter(w => POSITIVE_WORDS.has(w)).length
    const negHits = words.filter(w => NEGATIVE_WORDS.has(w)).length
    const polarity = posHits > negHits ? 1 : negHits > posHits ? -1 : 0
    // 抽象标签
    const abstractTags = new Set<string>()
    for (const w of words) {
      const mapped = ABSTRACT_MAP[w]
      if (mapped) for (const t of mapped) abstractTags.add(t)
    }
    if (abstractTags.size > 0 || polarity !== 0) {
      ;(mem as any)._gist = { polarity, abstractTags: [...abstractTags].slice(0, 6) }
    }
  }

  return memories
}

/**
 * Online 模式：逐轮 addMemory，走完整记忆管道
 * (addMemory → dedup → conflict resolution → surprise encoding → fact extraction → AAM learning)
 */
function buildMemoriesOnline(q: LocomoQuestion): Memory[] {
  const { addMemory, memoryState, scopeIndex, _recentWriteHashes } = require('./memory.ts')

  // 抑制 addMemory 内部日志
  const _prevSuppress = suppressLogs
  suppressLogs = true

  // 清空之前的记忆（每个 conv 隔离）
  memoryState.memories.length = 0
  memoryState.chatHistory.length = 0
  scopeIndex.clear()
  _recentWriteHashes.clear()  // 清空去重集合，避免跨 conv 误判

  // 时间归一化（同 offline 模式）
  const originalTimestamps = q.haystack_session_datetimes.map((d: string) => new Date(d).getTime())
  const minTs = Math.min(...originalTimestamps)
  const maxTs = Math.max(...originalTimestamps)
  const timeSpan = Math.max(maxTs - minTs, 1)
  const now = Date.now()
  const TARGET_SPAN = 30 * 86400000
  const TARGET_END = now - 3600000
  function normalizeTs(originalTs: number): number {
    const ratio = (originalTs - minTs) / timeSpan
    return TARGET_END - TARGET_SPAN * (1 - ratio)
  }

  let totalAdded = 0, totalSkipped = 0

  for (let si = 0; si < q.haystack_sessions.length; si++) {
    const session = q.haystack_sessions[si]
    const baseTs = normalizeTs(originalTimestamps[si])

    // 1. 逐轮喂入对话消息（episode 记忆）
    const _epDatePrefix = `[${new Date(originalTimestamps[si]).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}]`
    for (let ti = 0; ti < session.length; ti++) {
      const turn = session[ti]
      const content = turn?.content
      if (!content || content.length < 10) continue

      // 模拟时间推进
      const _mockNow = baseTs + ti * 60000
      const beforeCount = memoryState.memories.length

      try {
        addMemory(`${_epDatePrefix} ${content}`, 'event', 'benchmark-user')
      } catch {}

      if (memoryState.memories.length > beforeCount) {
        const newMem = memoryState.memories[memoryState.memories.length - 1]
        newMem.ts = _mockNow
        newMem.lastAccessed = Math.min(now - 7200000, _mockNow + 86400000)
        newMem._segmentId = si
        if (!newMem.tags) newMem.tags = []
        newMem.tags.push(`session:${si}`)
        totalAdded++
      } else {
        totalSkipped++
      }
    }

    // 2. Session summary 作为蒸馏知识
    const summary = q.haystack_session_summaries[si]
    if (summary) {
      const beforeCount = memoryState.memories.length
      try {
        addMemory(summary, 'fact', 'benchmark-user')
      } catch {}
      if (memoryState.memories.length > beforeCount) {
        const newMem = memoryState.memories[memoryState.memories.length - 1]
        newMem.ts = baseTs
        newMem.confidence = 0.95
        newMem.recallCount = 10
        newMem.lastAccessed = now - 3600000
        newMem.importance = 8
        if (!newMem.tags) newMem.tags = []
        newMem.tags.push('summary')
        newMem._segmentId = si
        totalAdded++
      }
    }
  }

  // 3. Sliding Window Merged Memories — 步长 2 合并相邻记忆（复制 offline 策略）
  // 直接推入 memoryState，不走 addMemory（避免被 dedup 过滤）
  let mergedCount = 0
  const episodeMemories = memoryState.memories.filter(m => !m.tags?.includes('summary'))
  for (let i = 0; i < episodeMemories.length - 1; i += 2) {
    const m1 = episodeMemories[i], m2 = episodeMemories[i + 1]
    if (!m1 || !m2) continue
    const timeDiff = Math.abs((m2.ts || 0) - (m1.ts || 0))
    if (timeDiff > 300000) continue  // 超过 5 分钟的不合并
    const merged = (m1.content || '') + ' ' + (m2.content || '')
    if (merged.length > 30 && merged.length < 800) {
      memoryState.memories.push({
        content: merged,
        scope: 'event',
        ts: m1.ts,
        confidence: 0.75,
        recallCount: 2,
        lastAccessed: Math.min(now - 7200000, (m1.ts || now) + 86400000),
        importance: 3,
        tags: [`merged:${i}`, `session:${m1._segmentId ?? 0}`],
        _segmentId: m1._segmentId,
      } as Memory)
      mergedCount++
    }
  }

  // 4. Gist Trace — 情感极性 + 抽象主题标签（零 LLM，Fuzzy Trace Theory）
  const POSITIVE_WORDS = new Set(['happy','excited','love','great','amazing','wonderful','enjoy','fun','glad','proud','beautiful','awesome','fantastic','celebrate','perfect','thrilled','delighted'])
  const NEGATIVE_WORDS = new Set(['sad','angry','frustrated','stressed','worried','anxious','tired','upset','disappointed','hurt','scared','lonely','overwhelmed','painful','annoyed','difficult','struggled'])
  const ABSTRACT_MAP: Record<string, string[]> = {
    'moved': ['relocation','change'], 'travel': ['journey','adventure'], 'bought': ['acquisition','purchase'],
    'lost': ['loss','misfortune'], 'won': ['achievement','success'], 'failed': ['setback','failure'],
    'married': ['relationship','milestone'], 'graduated': ['education','achievement'], 'hired': ['career','opportunity'],
    'fired': ['career','setback'], 'adopted': ['family','decision'], 'volunteered': ['community','service'],
    'painted': ['art','hobby'], 'hiked': ['outdoor','activity'], 'camped': ['outdoor','adventure'],
    'cooked': ['food','hobby'], 'read': ['reading','learning'], 'played': ['music','hobby','activity'],
  }
  for (const mem of memoryState.memories) {
    const c = (mem.content || '').toLowerCase()
    const words = c.match(/[a-z]{3,}/g) || []
    const posHits = words.filter(w => POSITIVE_WORDS.has(w)).length
    const negHits = words.filter(w => NEGATIVE_WORDS.has(w)).length
    const polarity = posHits > negHits ? 1 : negHits > posHits ? -1 : 0
    const abstractTags = new Set<string>()
    for (const w of words) {
      const mapped = ABSTRACT_MAP[w]
      if (mapped) for (const t of mapped) abstractTags.add(t)
    }
    if (abstractTags.size > 0 || polarity !== 0) {
      ;(mem as any)._gist = { polarity, abstractTags: [...abstractTags].slice(0, 6) }
    }
  }

  suppressLogs = _prevSuppress
  _origLog(`  [online] ${totalAdded} memories added, ${totalSkipped} skipped, ${mergedCount} merged windows`)
  return memoryState.memories
}

/**
 * API 模式：通过 HTTP API 存取记忆（走完整 Query Rewrite + LLM Rerank + Consensus Recall）
 * 需要 standalone 服务先启动：npx tsx cc-soul/standalone.ts
 */
async function buildMemoriesAPI(q: LocomoQuestion, apiPort: number): Promise<void> {
  const baseUrl = `http://localhost:${apiPort}`

  // 清空之前的记忆（直接调内部方法，API 没有 clear 端点）
  try {
    const { memoryState, scopeIndex, _recentWriteHashes } = require('./memory.ts')
    memoryState.memories.length = 0
    memoryState.chatHistory.length = 0
    scopeIndex.clear()
    _recentWriteHashes.clear()
    try { require('./aam.ts').resetLearnedData?.() } catch {}
    try { require('./fact-store.ts').clearFacts?.() } catch {}
  } catch {}

  const originalTimestamps = q.haystack_session_datetimes.map((d: string) => new Date(d).getTime())
  let totalAdded = 0, totalSkipped = 0

  for (let si = 0; si < q.haystack_sessions.length; si++) {
    const session = q.haystack_sessions[si]
    const _epDatePrefix = `[${new Date(originalTimestamps[si]).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}]`

    // 逐轮通过 API 存入
    for (let ti = 0; ti < session.length; ti++) {
      const turn = session[ti]
      const content = turn?.content
      if (!content || content.length < 10) continue

      try {
        const resp = await fetch(`${baseUrl}/memories`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ content: `${_epDatePrefix} ${content}`, scope: 'event', user_id: 'benchmark-user' }),
        })
        const result = await resp.json() as any
        if (result.stored) totalAdded++
        else totalSkipped++
      } catch { totalSkipped++ }
    }

    // Summary
    const summary = q.haystack_session_summaries[si]
    if (summary) {
      try {
        await fetch(`${baseUrl}/memories`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ content: summary, scope: 'fact', user_id: 'benchmark-user' }),
        })
        totalAdded++
      } catch {}
    }
  }

  _origLog(`  [api] ${totalAdded} memories stored via API, ${totalSkipped} skipped`)
}

/** API 模式召回：通过 /search 端点（含 Query Rewrite + LLM Rerank） */
async function recallViaAPI(query: string, topK: number, apiPort: number): Promise<Memory[]> {
  const baseUrl = `http://localhost:${apiPort}`
  try {
    const resp = await fetch(`${baseUrl}/search`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, top_n: topK, user_id: 'benchmark-user' }),
    })
    const result = await resp.json() as any
    // 转换为 Memory 格式
    return (result.memories || []).map((m: any) => ({
      content: m.content || '',
      scope: m.scope || 'fact',
      ts: m.ts || Date.now(),
      confidence: m.confidence || 0.7,
      tags: m.tags || [],
    } as Memory))
  } catch (e: any) {
    _origLog(`  [api] search error: ${e.message}`)
    return []
  }
}

/**
 * 从 LOCOMO summary 提取英文结构化事实（轻量正则，不依赖 LLM）
 * 原创双通道架构：NAM 模糊召回 + fact-store 精确匹配
 */
function extractFactsFromSummaries(memories: Memory[]): void {
  try {
    const factStore = require('./fact-store.ts')
    const summaries = memories.filter(m => m.tags?.includes('summary'))
    let totalFacts = 0

    for (const mem of summaries) {
      const text = mem.content || ''
      // 按句子拆分
      const sentences = text.split(/[.!?]\s+/).filter(s => s.length > 10)

      for (const sent of sentences) {
        // 提取主语（大写开头的名字）
        const nameMatch = sent.match(/^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b/)
        const subject = nameMatch ? nameMatch[1] : 'speaker'

        // 模式匹配：主语 + 动词 + 宾语
        const patterns = [
          // "X works as/at Y" / "X is a Y"
          { re: /\b(?:works?\s+(?:as|at|in|for)|is\s+a)\s+(.+?)(?:\.|,|and\s|$)/i, pred: 'occupation' },
          // "X lives in/moved to Y"
          { re: /\b(?:lives?\s+in|moved?\s+to|relocated\s+to|from)\s+(.+?)(?:\.|,|and\s|$)/i, pred: 'location' },
          // "X has/have/owns Y" (pets, children, etc.)
          { re: /\b(?:has|have|owns?|adopted)\s+(?:a\s+)?(.+?)(?:\.|,|and\s|$)/i, pred: 'has' },
          // "X enjoys/likes/loves Y"
          { re: /\b(?:enjoys?|likes?|loves?|passionate\s+about|interested\s+in)\s+(.+?)(?:\.|,|and\s|$)/i, pred: 'likes' },
          // "X volunteers/participates/attends Y"
          { re: /\b(?:volunteers?\s+at|participates?\s+in|attends?|joined)\s+(.+?)(?:\.|,|and\s|$)/i, pred: 'participates' },
          // "X plays/practices Y" (instruments, sports)
          { re: /\b(?:plays?|practices?|performs?)\s+(?:the\s+)?(.+?)(?:\.|,|and\s|$)/i, pred: 'plays' },
          // "X studied/majored/graduated Y"
          { re: /\b(?:studied|majored\s+in|graduated\s+(?:from|with)|degree\s+in)\s+(.+?)(?:\.|,|and\s|$)/i, pred: 'education' },
          // "X is married to / dating / in a relationship with Y"
          { re: /\b(?:married\s+to|dating|in\s+a\s+relationship\s+with|partner\s+is|spouse\s+is)\s+(.+?)(?:\.|,|and\s|$)/i, pred: 'relationship' },
          // "X reads/read Y"
          { re: /\b(?:reads?|has\s+read|been\s+reading)\s+(.+?)(?:\.|,|and\s|$)/i, pred: 'reads' },
          // "X traveled/visited/went to Y"
          { re: /\b(?:traveled\s+to|visited|went\s+to|been\s+to|trip\s+to)\s+(.+?)(?:\.|,|and\s|$)/i, pred: 'traveled' },
          // "X bought/purchased Y"
          { re: /\b(?:bought|purchased|got)\s+(?:a\s+)?(.+?)(?:\.|,|and\s|$)/i, pred: 'bought' },
          // "X made/created/painted Y"
          { re: /\b(?:made|created|painted|built|designed|wrote)\s+(?:a\s+)?(.+?)(?:\.|,|and\s|$)/i, pred: 'created' },
          // Generic: "X's Y is Z" / "X's Y"
          { re: /\b([A-Z][a-z]+)'s\s+(\w+(?:\s+\w+)?)\s+(?:is|are|was|were)\s+(.+?)(?:\.|,|$)/i, pred: '_possessive' },
        ]

        for (const { re, pred } of patterns) {
          const match = sent.match(re)
          if (match) {
            let object = (match[1] || match[3] || '').trim()
            let predicate = pred
            // _possessive 特殊处理：X's pets are Y → pred="pets", obj="Y"
            if (pred === '_possessive' && match[2]) {
              predicate = match[2].toLowerCase()
              object = (match[3] || '').trim()
            }
            if (object.length >= 2 && object.length <= 100) {
              factStore.addFacts([{
                subject: subject.toLowerCase(),
                predicate,
                object,
                confidence: 0.85,
                source: 'ai_observed',
                ts: mem.ts || Date.now(),
                validUntil: 0,
              }])
              totalFacts++
            }
          }
        }
      }
    }
    if (totalFacts > 0) {
      suppressLogs = false
      print(`  [fact-store] extracted ${totalFacts} facts from ${summaries.length} summaries`)
      suppressLogs = true
    }
  } catch (e: any) {
    // fact extraction 失败不影响 benchmark
  }
}

// ═══════════════════════════════════════════════════════════════
// LAYER 1: RECALL QUALITY (Hit@K, MRR)
// ═══════════════════════════════════════════════════════════════

/**
 * Check if any recalled memory contains the answer.
 * Dynamic matching: tries exact substring, then token overlap, then fuzzy.
 */
function answerInRecalled(recalled: Memory[], answer: string): { hit: boolean; rank: number } {
  const ansLower = answer.toLowerCase().trim()

  // Skip "Not answerable" — recall test doesn't apply
  if (/not answerable|cannot be answered|unanswerable/i.test(answer)) {
    return { hit: false, rank: -1 }
  }

  // Tokenize answer for flexible matching
  const ansTokens = ansLower.split(/\s+/).filter(t => t.length >= 2)
  const ansTri = trigrams(ansLower)

  for (let i = 0; i < recalled.length; i++) {
    const memLower = recalled[i].content.toLowerCase()

    // Strategy 1: exact substring
    if (memLower.includes(ansLower)) return { hit: true, rank: i + 1 }

    // Strategy 2: token coverage（动态阈值 + stemming）
    if (ansTokens.length > 0) {
      let tokenHits = 0
      for (const t of ansTokens) {
        if (memLower.includes(t)) { tokenHits++; continue }
        // Stemmed fallback: "camped"↔"camping", "played"↔"playing"
        if (t.length >= 4 && /^[a-z]+$/.test(t)) {
          const stem = t.replace(/ing$|ed$|s$|er$|est$|ly$/, '')
          if (stem.length >= 3 && memLower.includes(stem)) { tokenHits++; continue }
          // 反向：memory 里的词 stem 后匹配 answer token
          const memWords = memLower.match(/[a-z]{4,}/g) || []
          for (const mw of memWords) {
            const mStem = mw.replace(/ing$|ed$|s$|er$|est$|ly$/, '')
            if (mStem === stem || mw.startsWith(stem) || stem.startsWith(mw.slice(0, -1))) { tokenHits++; break }
          }
        }
      }
      const coverage = tokenHits / ansTokens.length
      const threshold = ansTokens.length <= 3 ? 0.9
        : ansTokens.length <= 6 ? 0.8
        : 0.6
      if (coverage >= threshold) return { hit: true, rank: i + 1 }
    }

    // Strategy 3: trigram similarity (fuzzy match for names, dates, etc.)
    const memTri = trigrams(memLower)
    const triSim = trigramSimilarity(ansTri, memTri)
    if (triSim > 0.4 && ansLower.length >= 4) return { hit: true, rank: i + 1 }

    // Strategy 4: 实体名 + 内容词组合匹配（更严格）
    const ansNames = answer.match(/\b[A-Z][a-z]{2,}\b/g)?.filter(n => !/^(The|This|That|What|When|Where|How|Who|Not|Yes|And|But)$/.test(n)) || []
    if (ansNames.length >= 1 && ansTokens.length >= 3) {
      const nameHits = ansNames.filter(n => memLower.includes(n.toLowerCase())).length
      const contentTokenHits = ansTokens.filter(t => t.length >= 4 && memLower.includes(t)).length
      // 至少 1 个名字 + 2 个内容词同时匹配
      if (nameHits >= 1 && contentTokenHits >= 2) return { hit: true, rank: i + 1 }
    }
  }

  // Strategy 5: 跨记忆累计匹配——答案碎片分散在多条记忆中
  // 合并 top-K 记忆文本，再做 token coverage（rank = 最后一条贡献者的位置）
  if (ansTokens.length >= 3 && recalled.length >= 2) {
    let accumulated = ''
    for (let i = 0; i < recalled.length; i++) {
      accumulated += ' ' + recalled[i].content.toLowerCase()
      // 每加一条新记忆就检查累计匹配
      let tokenHits = 0
      for (const t of ansTokens) {
        if (accumulated.includes(t)) { tokenHits++; continue }
        if (t.length >= 4 && /^[a-z]+$/.test(t)) {
          const stem = t.replace(/ing$|ed$|s$|er$|est$|ly$/, '')
          if (stem.length >= 3 && accumulated.includes(stem)) tokenHits++
        }
      }
      const coverage = tokenHits / ansTokens.length
      // 跨记忆匹配要求更严格的阈值（避免 false positive）
      if (coverage >= 0.85 && i >= 1) return { hit: true, rank: i + 1 }
    }
  }

  return { hit: false, rank: -1 }
}

// ═══════════════════════════════════════════════════════════════
// LAYER 2: ANSWER SELECTION (10-choice)
// ═══════════════════════════════════════════════════════════════

function selectAnswer(recalled: Memory[], choices: string[], question?: string): { choiceIndex: number; confidence: number } {
  if (recalled.length === 0) {
    const naIdx = choices.findIndex(c => /not answerable|cannot be answered|unanswerable/i.test(c))
    return { choiceIndex: naIdx >= 0 ? naIdx : 0, confidence: 0 }
  }

  const context = recalled.map(m => m.content).join(' ').toLowerCase()

  const idfMap: Map<string, number> = getIdfCache?.() || new Map()
  if (!(selectAnswer as any)._idfLogged) {
    (selectAnswer as any)._idfLogged = true
    _origLog(`  [selectAnswer] IDF cache: ${idfMap.size > 0 ? idfMap.size + ' terms' : 'EMPTY (fallback mode)'}`)
  }

  const qLower = (question || '').toLowerCase()
  const qaType = /^who\b|who (?:is|was|does|did|has|had)\b/.test(qLower) ? 'who'
    : /^when\b|what (?:date|time|year|month|day)\b/.test(qLower) ? 'when'
    : /^where\b|what (?:place|location|city|country|address)\b/.test(qLower) ? 'where'
    : /^how many\b|how much\b|what (?:number|amount|count)\b/.test(qLower) ? 'howmany'
    : null

  // S0: Extract entities from recalled memories for precise matching
  const entitySet = new Set<string>()
  const allRecalledText = recalled.map(m => m.content).join(' ')
  const dateMatches = allRecalledText.match(/\d{1,2}\s+\w+\s+\d{4}/g) || []
  for (const d of dateMatches) entitySet.add(d.toLowerCase())
  const numMatches = allRecalledText.match(/\b\d{2,}\b/g) || []
  for (const n of numMatches) entitySet.add(n)
  const nameMatches = allRecalledText.match(/[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*/g) || []
  for (const name of nameMatches) {
    entitySet.add(name.toLowerCase())
    for (const part of name.split(/\s+/)) {
      if (part.length >= 2) entitySet.add(part.toLowerCase())
    }
  }

  const scores = choices.map((choice, idx) => {
    const choiceLower = choice.toLowerCase().trim()
    let score = 0

    // S0: entity exact matching (cleaned entities)
    if (entitySet.size > 0) {
      let entityHits = 0
      for (const entity of entitySet) if (choiceLower.includes(entity)) entityHits++
      if (entityHits > 0) score = Math.max(score, Math.min(1.0, entityHits / Math.max(3, entitySet.size) * 1.5))
    }

    // S1: exact substring
    if (context.includes(choiceLower)) score = Math.max(score, 1.0)

    // S2: IDF-weighted token coverage (B4)
    const tokens = choiceLower.split(/\s+/).filter(t => t.length >= 2)
    if (tokens.length > 0) {
      if (idfMap.size > 0) {
        let weightedHits = 0, weightedTotal = 0
        for (const t of tokens) {
          const idfW = idfMap.get(t) ?? (t.length >= 4 ? 0.7 : 0.3)
          weightedTotal += idfW
          if (context.includes(t)) { weightedHits += idfW; continue }
          if (t.length >= 4 && /^[a-z]+$/.test(t)) {
            const stem = t.replace(/ing$|ed$|s$|er$|est$|ly$/, '')
            if (stem.length >= 3 && context.includes(stem)) weightedHits += idfW * 0.8
          }
        }
        if (weightedTotal > 0) score = Math.max(score, (weightedHits / weightedTotal) * 0.8)
      } else {
        let hits = 0
        for (const t of tokens) {
          if (context.includes(t)) { hits++; continue }
          if (t.length >= 4 && /^[a-z]+$/.test(t)) {
            const stem = t.replace(/ing$|ed$|s$|er$|est$|ly$/, '')
            if (stem.length >= 3 && context.includes(stem)) hits++
          }
        }
        score = Math.max(score, hits / tokens.length * 0.8)
      }
    }

    // S3: per-memory trigram (fuzzy)
    const choiceTri = trigrams(choiceLower)
    for (const mem of recalled) {
      const sim = trigramSimilarity(choiceTri, trigrams(mem.content.toLowerCase()))
      score = Math.max(score, sim * 0.6)
    }

    // B5: QA Type bonus
    if (qaType) {
      if (qaType === 'who' && /[A-Z][a-z]{2,}/.test(choice)) score += 0.08
      else if (qaType === 'when' && /\d{4}|\b\d{1,2}\s+\w+\b|january|february|march|april|may|june|july|august|september|october|november|december/i.test(choice)) score += 0.08
      else if (qaType === 'where' && /[A-Z][a-z]{2,}/.test(choice)) score += 0.05
      else if (qaType === 'howmany' && /\d+/.test(choice)) score += 0.08
    }

    return { idx, score }
  })

  scores.sort((a, b) => b.score - a.score)

  // ── Dynamic Abstain + C3 Negative Evidence ──
  const _ABSTAIN_STOPS = new Set(['what','when','where','how','who','which','why','the','this','that','does','did','has','have','was','were','can','could','would','should','not','are','its','his','her','she','they','been','being','had','with','from','for','and','but','about','after','before','into','over','than','then','some','any','all','both','each','more','most','many','much','very','also','just','only','still'])
  const qKeywords = ((question || '').toLowerCase().match(/[a-z]{3,}/g) || []).filter(w => !_ABSTAIN_STOPS.has(w))
  const recalledText = recalled.map(m => m.content).join(' ').toLowerCase()
  const evidenceCoverage = qKeywords.length > 0 ? qKeywords.filter(w => recalledText.includes(w)).length / qKeywords.length : 0
  const margin = scores[0].score > 0 && scores.length >= 2 ? (scores[0].score - scores[1].score) / Math.max(scores[0].score, 0.01) : 0
  const qEntities = ((question || '').match(/\b[A-Z][a-z]{2,}\b/g) || []).filter(n => !/^(What|When|Where|How|Who|Which|Why|The|This|That|Does|Did|Has|Have|Was|Were|Can|Could|Would|Should|Not)$/.test(n))
  const entityCoverage = qEntities.length > 0 ? qEntities.filter(n => recalledText.includes(n.toLowerCase())).length / qEntities.length : 1

  const topicPresence = entityCoverage > 0.5
  const topChoiceTokens = choices[scores[0].idx]?.toLowerCase().match(/[a-z]{3,}/g) || []
  const detailHits = topChoiceTokens.filter(t => !_ABSTAIN_STOPS.has(t) && recalledText.includes(t)).length
  const detailSufficiency = scores[0].score > 0.3 && (topChoiceTokens.length === 0 || detailHits / Math.max(1, topChoiceTokens.length) > 0.3)

  const answerability = evidenceCoverage * (0.3 + 0.7 * margin) * entityCoverage
  const groundingScore = topicPresence ? (detailSufficiency ? 1.0 : 0.3) : 0.1

  const naIdx = choices.findIndex(c => /not answerable|cannot be answered|unanswerable/i.test(c))
  if (naIdx >= 0 && (answerability < 0.15 || groundingScore < 0.2)) return { choiceIndex: naIdx, confidence: Math.min(answerability, groundingScore) }
  if (scores[0].score < 0.15 && naIdx >= 0) return { choiceIndex: naIdx, confidence: scores[0].score }

  return { choiceIndex: scores[0].idx, confidence: scores[0].score }
}

// ═══════════════════════════════════════════════════════════════
// RUNNER
// ═══════════════════════════════════════════════════════════════

function parseArgs() {
  const args = process.argv.slice(2)
  let conv: number | undefined, type: string | undefined, topK = 10, verbose = false, limit = 0
  let recallOnly = false, llm = false, online = false, api = false, apiPort = 18800, sample = false, mini = false
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--conv' && args[i + 1]) conv = parseInt(args[++i])
    if (args[i] === '--type' && args[i + 1]) type = args[++i]
    if (args[i] === '--top-k' && args[i + 1]) topK = parseInt(args[++i])
    if (args[i] === '--limit' && args[i + 1]) limit = parseInt(args[++i])
    if (args[i] === '--verbose') verbose = true
    if (args[i] === '--recall-only') recallOnly = true
    if (args[i] === '--llm') llm = true
    if (args[i] === '--online') online = true
    if (args[i] === '--api') { api = true; online = true }
    if (args[i] === '--api-port' && args[i + 1]) apiPort = parseInt(args[++i])
    if (args[i] === '--sample') sample = true  // 3-conv 快速采样（小/中/大库）
    if (args[i] === '--mini') mini = true       // 单 conv 快速验证
  }
  return { conv, type, topK, verbose, limit, recallOnly, llm, online, api, apiPort, sample, mini }
}

// ═══════════════════════════════════════════════════════════════
// LLM ANSWER SELECTION (Kimi k2.5)
// ═══════════════════════════════════════════════════════════════

function loadLLMKey(): string {
  if (process.env.LLM_PROVIDER === 'claude') return process.env.ANTHROPIC_KEY || ''
  if (process.env.LLM_PROVIDER === 'gemini') return process.env.GEMINI_KEY || ''
  return 'sk-2d29b4fb236b40908c54a9517f86d504'
}

async function selectAnswerWithLLM(
  recalled: Memory[],
  question: string,
  choices: string[],
  apiKey: string,
): Promise<{ choiceIndex: number; raw: string }> {
  const letters = 'ABCDEFGHIJ'
  const choiceBlock = choices.map((c, i) => `${letters[i]}. ${c}`).join('\n')

  // 过滤 merged 记忆（只用于 recall 辅助，不展示给 LLM 避免冗余）
  const llmRecalled = recalled.filter(m => !m.tags?.some((t: string) => t.startsWith('merged:')))
  const displayRecalled = llmRecalled.length >= 3 ? llmRecalled : recalled  // fallback if too few


  // 结构化 context：按 session 分组展示（B2：让 LLM 更容易定位时间和实体）
  const sessionGroups = new Map<string, { idx: number; content: string }[]>()
  for (let i = 0; i < displayRecalled.length; i++) {
    const sessionTag = displayRecalled[i].tags?.find((t: string) => t.startsWith('session:')) || 'other'
    if (!sessionGroups.has(sessionTag)) sessionGroups.set(sessionTag, [])
    sessionGroups.get(sessionTag)!.push({ idx: i + 1, content: displayRecalled[i].content })
  }
  let structuredContext = ''
  if (sessionGroups.size > 1) {
    // 多 session：分组展示
    for (const [session, mems] of sessionGroups) {
      structuredContext += `\n[${session}]\n`
      for (const m of mems) structuredContext += `  ${m.idx}. ${m.content}\n`
    }
  } else {
    // 单 session：扁平列表
    structuredContext = recalled.map((m, i) => `[${i + 1}] ${m.content}`).join('\n')
  }

  // ── FOK (Feeling of Knowing) 元记忆信号（原创，Metamemory 理论）──
  // 用可获取的信号判断系统对问题的了解程度
  const _fokQEnts = (question.match(/\b[A-Z][a-z]{2,}\b/g) || []).filter(n => !/^(What|When|Where|How|Who|Which|Why|The|This|That|Does|Did|Has|Have|Was|Were|Can|Could|Would|Should|Not)$/.test(n))
  const _fokRecalledText = recalled.map(m => (m.content || '').toLowerCase()).join(' ')
  const _fokEntityPresent = _fokQEnts.length === 0 || _fokQEnts.some(n => _fokRecalledText.includes(n.toLowerCase()))
  // QPP 信号：查询关键词在 recalled 中覆盖率
  const _fokQWords = (question.toLowerCase().match(/[a-z]{4,}/g) || []).filter(w => !/^(what|when|where|how|who|which|why|does|did|has|have|was|were|would|could|should|about|their|with|from|been|this|that|they|them|most|more)$/.test(w))
  const _fokWordCoverage = _fokQWords.length > 0 ? _fokQWords.filter(w => _fokRecalledText.includes(w)).length / _fokQWords.length : 0
  const _fokConfidence = !_fokEntityPresent ? 'LOW' : _fokWordCoverage < 0.3 ? 'LOW' : _fokWordCoverage < 0.6 ? 'MEDIUM' : 'HIGH'

  // 检测是否有 "Not answerable" 选项
  const hasNA = choices.some(c => /not answerable|cannot be answered|unanswerable/i.test(c))
  // 计算记忆与问题的词汇重叠度（作为置信度信号传给 LLM）
  const qWords = new Set(question.toLowerCase().match(/[a-z]{3,}/g) || [])
  const mWords = new Set(recalled.flatMap(m => (m.content || '').toLowerCase().match(/[a-z]{3,}/g) || []))
  let overlap = 0
  for (const w of qWords) if (mWords.has(w)) overlap++
  const relevanceHint = qWords.size > 0 ? (overlap / qWords.size) : 0

  const systemPrompt = `You are answering a multiple-choice question about a person's life based on conversation memories.

Rules:
1. If a choice matches specific details (names, numbers, dates, activities) mentioned in the memories, prefer it.
2. Pay attention to WHO said what — the question asks about a specific person.
3. For date/time questions: look at the [date] prefix on each memory for exact dates. Match the specific month/year mentioned in memories, not your general knowledge. Pick the closest date rather than "Not answerable".
4. For multi-step questions: combine information from multiple memories. If memory A says "X happened" and memory B mentions "during August", connect them.
${hasNA ? (_fokConfidence === 'LOW'
  ? `5. Memory confidence is LOW. Choose "Not answerable" unless you find SPECIFIC, DIRECT evidence in the memories. Specifically:
   - If NO memory contains the exact detail the question asks about → "Not answerable"
   - Vague topic overlap is NOT sufficient — you need concrete facts/dates/names that directly answer the question
   - When in doubt, prefer "Not answerable" over guessing`
  : `4. Choose "Not answerable" when the memories do NOT contain information relevant to the question topic. Specifically:
   - If the question asks about a topic/person/event that is never mentioned in any memory → "Not answerable"
   - If the memories mention the topic but don't contain enough detail to pick a specific answer → still pick the best match, NOT "Not answerable"
   - When in doubt between a specific answer and "Not answerable", check if ANY memory discusses the same topic as the question`)
  : '5. Pick the best matching answer based on the memories.'}`

  const fokNote = _fokConfidence === 'LOW' ? '\n[System note: Memory confidence is LOW — the topic may not be covered in these memories. Prefer "Not answerable" unless you see direct evidence.]\n' : ''
  const userPrompt = `Memories (relevance: ${(relevanceHint * 100).toFixed(0)}%, confidence: ${_fokConfidence}):${fokNote}
${structuredContext}

Question: ${question}

Choices:
${choiceBlock}

Answer with ONLY one letter (A-J).`

  // 动态选择 LLM API：Claude / Gemini / DeepSeek
  const useClaude = process.env.LLM_PROVIDER === 'claude'
  const useGemini = process.env.LLM_PROVIDER === 'gemini'
  const resp = useGemini
    ? await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{ parts: [{ text: systemPrompt + '\n\n' + userPrompt }] }],
          generationConfig: { temperature: 0, maxOutputTokens: 10 },
        }),
      })
    : useClaude
    ? await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': apiKey,
          'anthropic-version': '2023-06-01',
        },
        body: JSON.stringify({
          model: 'claude-sonnet-4-20250514',
          system: systemPrompt + '\n\nIMPORTANT: Respond with ONLY a single letter (A-J). No explanation, no reasoning, just the letter.',
          messages: [{ role: 'user', content: userPrompt }],
          temperature: 0,
          max_tokens: 3,
        }),
      })
    : await fetch('https://api.deepseek.com/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${apiKey}`,
        },
        body: JSON.stringify({
          model: 'deepseek-chat',
          messages: [
            { role: 'system', content: systemPrompt },
            { role: 'user', content: userPrompt },
          ],
          temperature: 0,
          max_tokens: 5,
        }),
      })

  if (!resp.ok) {
    const body = await resp.text()
    throw new Error(`LLM API ${resp.status}: ${body.slice(0, 200)}`)
  }

  const json = await resp.json() as any
  // Gemini: candidates[0].content.parts[0].text, Claude: content[0].text, DeepSeek: choices[0].message.content
  let raw = ''
  if (useGemini) {
    raw = (json.candidates?.[0]?.content?.parts?.[0]?.text || '').trim()
  } else if (useClaude) {
    raw = (json.content?.[0]?.text || '').trim()
  } else {
    raw = (json.choices?.[0]?.message?.content || '').trim()
  }

  // 提取答案字母
  let letter = ''
  // 特殊处理：LLM 直接输出 "Not answerable" 而非选项字母
  if (/not answerable|cannot be answered|unanswerable/i.test(raw)) {
    const naChoiceIdx = choices.findIndex(c => /not answerable|cannot be answered|unanswerable/i.test(c))
    if (naChoiceIdx >= 0) letter = letters[naChoiceIdx]
  }
  if (!letter) {
  const directMatch = raw.match(/^([A-J])\b/)
  if (directMatch) {
    letter = directMatch[1]
  } else {
    const answerMatch = raw.match(/(?:answer|choice|select|pick|choose)[:\s]+\*?\*?([A-J])\b/i)
      || raw.match(/ANSWER\s*:\s*\*?\*?\s*([A-J])\b/i)
      || raw.match(/\b([A-J])\.\s/)
      || raw.match(/\*\*([A-J])\*\*/)
      || raw.match(/\b([A-J])$/m)
    if (answerMatch) letter = answerMatch[1]
    else {
      // Last resort: scan entire raw output for any A-J letter
      const anyLetter = raw.match(/\b([A-J])\b/)
      if (anyLetter) letter = anyLetter[1]
      else letter = raw.charAt(0).toUpperCase()
    }
  }
  }  // end if (!letter)
  let idx = letters.indexOf(letter)
  // Fallback: trigram matching raw text against choices (handles verbose LLM output)
  if (idx < 0 && raw.length > 1) {
    const rawLower = raw.toLowerCase()
    let bestSim = 0, bestIdx = -1
    for (let ci = 0; ci < choices.length; ci++) {
      const choiceLower = choices[ci].toLowerCase()
      // Exact substring match
      if (rawLower.includes(choiceLower) || choiceLower.includes(rawLower)) {
        bestIdx = ci; break
      }
      const sim = trigramSimilarity(trigrams(rawLower), trigrams(choiceLower))
      if (sim > bestSim) { bestSim = sim; bestIdx = ci }
    }
    if (bestIdx >= 0 && (bestSim > 0.3 || bestIdx >= 0)) idx = bestIdx
  }
  return { choiceIndex: idx >= 0 ? idx : -1, raw }
}

const sleep = (ms: number) => new Promise(r => setTimeout(r, ms))

async function run() {
  const opts = parseArgs()
  const mode = opts.recallOnly ? 'recall-only' : opts.llm ? 'llm' : opts.api ? 'api' : opts.online ? 'online' : 'default'

  print('═══════════════════════════════════════════════════════════')
  print('  cc-soul NAM × LOCOMO-MC10 Benchmark')
  print('═══════════════════════════════════════════════════════════')
  print(`  mode: ${mode}  top-K: ${opts.topK}  conv: ${opts.conv ?? 'all'}  type: ${opts.type ?? 'all'}  limit: ${opts.limit || 'none'}`)
  print()

  // Pre-load LLM key if needed
  let apiKey = ''
  if (opts.llm) {
    try {
      apiKey = loadLLMKey()
      print('  DeepSeek API key loaded')
    } catch (e: any) {
      print(`  ERROR: ${e.message}`)
      return
    }
  }

  const allQuestions = loadDataset()
  print(`  Loaded ${allQuestions.length} questions`)

  // Group by conversation
  const convMap = new Map<string, LocomoQuestion[]>()
  for (const q of allQuestions) {
    const convId = q.question_id.split('_')[0]
    if (!convMap.has(convId)) convMap.set(convId, [])
    convMap.get(convId)!.push(q)
  }
  const convIds = [...convMap.keys()].sort()
  print(`  ${convIds.length} conversations`)
  print()

  // Filter
  let questions = allQuestions
  if (opts.mini) {
    // 单 conv 快速验证：conv-4（中等大小）→ ~200 题，3-5 分钟
    const miniConv = convIds[4] || convIds[0]
    questions = allQuestions.filter(q => q.question_id.split('_')[0] === miniConv)
    print(`  Mini mode: ${miniConv} → ${questions.length} questions`)
  } else if (opts.sample) {
    // 3-conv 快速采样：小库(conv-0)、中库(conv-4)、大库(conv-9) → ~500 题，2 分钟
    const sampleConvs = [convIds[0], convIds[4], convIds[9]].filter(Boolean)
    questions = allQuestions.filter(q => sampleConvs.includes(q.question_id.split('_')[0]))
    print(`  Sample mode: ${sampleConvs.join(', ')} → ${questions.length} questions`)
  } else if (opts.conv !== undefined) {
    const targetConv = convIds[opts.conv]
    if (!targetConv) { print(`  Invalid conv index: ${opts.conv}`); return }
    questions = convMap.get(targetConv) || []
    print(`  Filtered to conv ${targetConv}: ${questions.length} questions`)
  }
  if (opts.type) {
    questions = questions.filter(q => q.question_type === opts.type)
    print(`  Filtered to type ${opts.type}: ${questions.length} questions`)
  }
  if (opts.limit > 0) {
    questions = questions.slice(0, opts.limit)
    print(`  Limited to first ${questions.length} questions`)
  }

  if (questions.length === 0) { print('  No questions.'); return }

  // Memory cache per conversation
  const memoryCache = new Map<string, Memory[]>()
  const learnedConvs = new Set<string>()

  // ── 论文维度：按对话长度分组 + 延迟追踪 + 存储统计 ──
  const convMemoryCount = new Map<string, number>()  // convId → memory count
  const perQueryLatency: number[] = []               // ms per query
  let totalMemoryBytes = 0                           // 所有记忆的原始文本大小
  // Per-question result for bucketing by conversation size
  const perQuestionResult: { convId: string; hit: boolean; mcCorrect: boolean; isAdversarial: boolean }[] = []

  // Trackers — extended for recall-only Hit@1/3/5/10
  const typeStats: Record<string, {
    recallTotal: number,
    hitAt1: number, hitAt3: number, hitAt5: number, hitAt10: number,
    mrrSum: number,
    mcCorrect: number, mcTotal: number,       // Layer 2 (string-match)
    llmCorrect: number, llmTotal: number,     // Layer 2 (LLM)
    llmFail: number,                          // LLM parse failures
  }> = {}
  function getStat(type: string) {
    if (!typeStats[type]) typeStats[type] = {
      recallTotal: 0, hitAt1: 0, hitAt3: 0, hitAt5: 0, hitAt10: 0, mrrSum: 0,
      mcCorrect: 0, mcTotal: 0, llmCorrect: 0, llmTotal: 0, llmFail: 0,
    }
    return typeStats[type]
  }

  const startTime = Date.now()
  suppressLogs = true

  let _lastConvId = ''

  for (let qi = 0; qi < questions.length; qi++) {
    const q = questions[qi]
    const convId = q.question_id.split('_')[0]

    // ── Per-conv 数据隔离：清空上一个 conv 的学习数据 ──
    if (convId !== _lastConvId && _lastConvId !== '') {
      try { require('./aam.ts').resetLearnedData?.() } catch {}
      try { require('./fact-store.ts').clearFacts?.() } catch {}
    }
    _lastConvId = convId

    // Build memories (cached)
    if (!memoryCache.has(convId)) {
      // API 模式也用 buildMemoriesOnline（走 addMemory 完整管道含微蒸馏），
      // 区别在于召回时更新元数据（模拟 recall() 的再固化）
      const memories = opts.online ? buildMemoriesOnline(q) : buildMemories(q)
      memoryCache.set(convId, memories)
      if (!learnedConvs.has(convId)) {
        // ── T1: 跨轮关联学习——Q-A 对的词自动共现，建立语义桥梁 ──
        for (let mi = 0; mi < memories.length; mi++) {
          learnAssociation(memories[mi].content, 0.2)
          // 相邻消息配对：Q 里的 "instruments" 和 A 里的 "ukulele" 产生共现
          if (mi + 1 < memories.length) {
            const timeDiff = Math.abs((memories[mi + 1].ts || 0) - (memories[mi].ts || 0))
            if (timeDiff < 120000) {
              const w1 = (memories[mi].content || '').match(/[a-zA-Z]{3,}/gi) || []
              const w2 = (memories[mi + 1].content || '').match(/[a-zA-Z]{3,}/gi) || []
              if (w1.length > 0 && w2.length > 0) {
                learnAssociation(w1.slice(0, 8).join(' ') + ' ' + w2.slice(0, 8).join(' '), 0.4, 1.0, true)
              }
            }
          }
        }
        // Summary 强化学习（高权重 + 二次拆分 + SVO 三元组）
        for (const mem of memories) {
          if (mem.tags?.includes('summary')) {
            learnAssociation(mem.content, 0.8)  // 4x 权重
            const sentences = mem.content.split(/[.!?;]\s+/).filter(s => s.length > 10)
            for (const sent of sentences) {
              learnAssociation(sent, 0.5)
              // ── SVO 三元组学习：提取 主语-动词-宾语 做 fullPair ──
              // 解决词汇鸿沟："Caroline researched adoption agencies" → caroline+researched+adoption 共现
              // 正则提取英文 SVO：大写名 + 动词 + 后续名词短语
              const svoMatch = sent.match(/\b([A-Z][a-z]+)\b.*?\b([a-z]{4,}(?:ed|s|ing)?)\b\s+(?:the\s+|a\s+|an\s+)?([a-z]{3,}(?:\s+[a-z]{3,})?)/i)
              if (svoMatch) {
                const svo = `${svoMatch[1]} ${svoMatch[2]} ${svoMatch[3]}`
                learnAssociation(svo, 0.3, 1.0, true)  // fullPair：保证三者互相共现
              }
            }
          }
        }
        // S2: fact-store 暂关（验证：限量融合仍 -2.2% Hit@10，facts 挤占 top-10）
        if (false) try {
          const { extractFacts, addFacts } = require('./fact-store.ts')
          let factCount = 0
          for (const mem of memories) {
            if (mem.scope === 'episode' && mem.content && mem.content.length > 20) {
              const facts = extractFacts(mem.content, 'user_said')
              if (facts.length > 0) { addFacts(facts); factCount += facts.length }
            }
          }
          if (factCount > 0) {
            suppressLogs = false
            print(`  [fact-store] extracted ${factCount} facts from episodes`)
            suppressLogs = true
          }
        } catch {}
        // G1: 从记忆内容构建图谱实体关系（让 Signal 4 + graph fusion 在 benchmark 里生效）
        try {
          const graph = require('./graph.ts')

          // G1-pre: 从 speaker 标签和 summary 预注册实体（解决 findMentionedEntities 只认 Title Case 的问题）
          const _preRegistered = new Set<string>()
          for (const mem of memories) {
            // Speaker 名（全大写格式 [MELANIE]:）
            const speakerMatch = mem.content.match(/^\[([A-Z]{2,})\]:/)
            if (speakerMatch) {
              const name = speakerMatch[1].charAt(0) + speakerMatch[1].slice(1).toLowerCase() // MELANIE → Melanie
              if (!_preRegistered.has(name)) {
                graph.findMentionedEntities(name) // 触发自动注册
                _preRegistered.add(name)
              }
            }
            // Summary 中 "X and Y caught up" / "X shared with Y" 格式的人名
            if (mem.tags?.includes('summary')) {
              const summaryNames = mem.content.match(/\b([A-Z][a-z]{2,})\b/g) || []
              for (const n of summaryNames) {
                if (!/^(The|This|That|What|When|Where|How|Who|Which|Why|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|January|February|March|April|May|June|July|August|September|October|November|December|Since|During|After|Before|Caroline|She|Her|His|They)$/.test(n)) {
                  // 不排除 Caroline 等人名（上面的排除列表只排非名词）
                }
                if (!_preRegistered.has(n) && !/^(The|This|That|Since|During|After|Before)$/.test(n)) {
                  graph.findMentionedEntities(n)
                  _preRegistered.add(n)
                }
              }
            }
          }

          // 两遍：先从 summary（信息密度高，多人名共现），再从 episode
          const summaries = memories.filter(m => m.tags?.includes('summary'))
          const episodes = memories.filter(m => !m.tags?.includes('summary'))
          for (const mem of [...summaries, ...episodes]) {
            const entities = graph.findMentionedEntities(mem.content)
            if (entities.length >= 2) {
              for (let ei = 0; ei < entities.length; ei++) {
                for (let ej = ei + 1; ej < entities.length; ej++) {
                  try {
                    graph.addRelation?.(entities[ei], entities[ej], 'co_mentioned')
                  } catch {}
                }
              }
            }
          }
          const entCount = graph.graphState?.entities?.length || 0
          const relCount = graph.graphState?.relations?.length || 0
          if (entCount > 0) {
            suppressLogs = false
            print(`  [graph] built ${entCount} entities, ${relCount} relations`)
            suppressLogs = true
          }
        } catch {}
        // ── 前瞻性标签：AAM 学习完后，为每条记忆预测未来查询词（零 LLM doc2query）──
        try {
          const { expandQuery } = require('./aam.ts')
          let tagged = 0
          for (const mem of memories) {
            if ((mem as any).prospectiveTags) continue
            const words = (mem.content || '').match(/[a-zA-Z]{3,}/gi)
            if (!words || words.length < 2) continue
            const contentLower = (mem.content || '').toLowerCase()
            const expanded = expandQuery(words.slice(0, 5).map((w: string) => w.toLowerCase()), 10)
            const threshold = expanded.length < 3 ? 0.15 : 0.3  // 放宽阈值，让更多扩展词参与（原 0.3/0.5）
            const tags = expanded
              .filter((e: any) => e.weight >= threshold && !contentLower.includes(e.word) && e.word.length >= 2)
              .map((e: any) => e.word)
              .slice(0, 8)
            if (tags.length > 0) { (mem as any).prospectiveTags = tags; tagged++ }
          }
          if (tagged > 0) { suppressLogs = false; print(`  [prospective-tags] ${tagged}/${memories.length} memories tagged`); suppressLogs = true }
        } catch {}
        learnedConvs.add(convId)
        convMemoryCount.set(convId, memories.length)
        totalMemoryBytes += memories.reduce((s, m) => s + (m.content || '').length * 2, 0)  // UTF-16 approx
        suppressLogs = false
        print(`  [${convId}] ${memories.length} memories loaded`)
        suppressLogs = true
      }
    }
    const memories = memoryCache.get(convId)!

    // Recall (with latency tracking)
    const _qStart = Date.now()
    const _cogHints = toCogHints(q.question)
    let recalled: Memory[]
    if (opts.api) {
      // API 模式：用 recall()（完整管道：指代消解+启动效应+路由+元数据更新+graveyard）
      const { recall: fullRecall } = require('./memory-recall.ts')
      recalled = fullRecall(q.question, opts.topK, 'benchmark-user', undefined, { mood: 0, alertness: 0.5 }, undefined, _cogHints) || []
    } else {
      recalled = activationRecall(memories, q.question, opts.topK, 0, 0.5, _cogHints)
    }
    perQueryLatency.push(Date.now() - _qStart)

    // ── Recall-Driven AAM Learning：模拟真实使用中 query↔recall 共现（增强版）──
    if (recalled.length > 0) {
      try {
        const queryKw = (q.question.match(/[a-zA-Z]{3,}/gi) || []).slice(0, 8)
        // 从 top-5 recalled 提取关键词（更广泛的学习窗口）
        const recallKw = recalled.slice(0, 5).flatMap(m => (m.content.match(/[a-zA-Z]{3,}/gi) || [])).slice(0, 15)
        const combined = queryKw.join(' ') + ' ' + recallKw.join(' ')
        learnAssociation(combined, 0.6)
        // Summary 记忆的内容词额外学习（summary 是聚合知识，关联质量高）
        for (const mem of recalled.slice(0, 3)) {
          if (mem.tags?.includes('summary')) {
            learnAssociation(queryKw.join(' ') + ' ' + (mem.content.match(/[a-zA-Z]{4,}/gi) || []).slice(0, 10).join(' '), 0.8)
          }
        }
      } catch {}
    }

    // ── 增量前瞻标签：把 query 关键词注入到被召回记忆的 prospectiveTags ──
    // 跳过推理型查询（"Would X..."、"Is it likely..."）——推理词注入会引入噪声
    const _isInferenceQ = /^(would|could|is it|are there|might|should|do you think)/i.test(q.question.trim())
    if (recalled.length > 0 && !_isInferenceQ) {
      try {
        const qContentWords = (q.question.match(/[a-zA-Z]{4,}/gi) || [])
          .map((w: string) => w.toLowerCase())
          .filter(w => !/^(what|when|where|how|who|which|why|does|did|has|have|was|were|can|could|would|should)$/.test(w))
          .slice(0, 5)
        for (const mem of recalled.slice(0, 3)) {
          const pt = (mem as any).prospectiveTags || []
          for (const w of qContentWords) {
            if (!pt.includes(w) && !(mem.content || '').toLowerCase().includes(w)) {
              pt.push(w)
            }
          }
          if (pt.length > 0) (mem as any).prospectiveTags = pt.slice(0, 12)
        }
      } catch {}
    }

    const stat = getStat(q.question_type)

    // Layer 1: Recall quality (always computed for non-adversarial)
    const isAdversarial = /not answerable|cannot be answered|unanswerable/i.test(q.answer)
    let _qHit = false
    if (!isAdversarial) {
      stat.recallTotal++
      const { hit, rank } = answerInRecalled(recalled, q.answer)
      _qHit = hit
      if (hit) {
        if (rank <= 1) stat.hitAt1++
        if (rank <= 3) stat.hitAt3++
        if (rank <= 5) stat.hitAt5++
        if (rank <= 10) stat.hitAt10++
        stat.mrrSum += 1 / rank
      }
    }

    // Layer 2: skip for recall-only
    let _qMCCorrect = false
    if (!opts.recallOnly) {
      // String-match answer selection (always run)
      stat.mcTotal++
      const { choiceIndex, confidence } = selectAnswer(recalled, q.choices, q.question)
      _qMCCorrect = choiceIndex === q.correct_choice_index
      if (_qMCCorrect) stat.mcCorrect++

      // LLM answer selection
      if (opts.llm) {
        stat.llmTotal++
        try {
          const { choiceIndex: llmIdx, raw } = await selectAnswerWithLLM(recalled, q.question, q.choices, apiKey)
          if (llmIdx >= 0 && llmIdx === q.correct_choice_index) stat.llmCorrect++
          if (llmIdx < 0) stat.llmFail++

          if (opts.verbose) {
            const smOk = choiceIndex === q.correct_choice_index
            const llmOk = llmIdx === q.correct_choice_index
            suppressLogs = false
            print(`  SM:${smOk ? 'O' : 'X'} LLM:${llmOk ? 'O' : 'X'} [${q.question_type.padEnd(20)}] ${q.question.slice(0, 50)}`)
            if (!llmOk) {
              print(`     want: ${q.choices[q.correct_choice_index]?.slice(0, 50)}`)
              print(`     llm:  ${llmIdx >= 0 ? q.choices[llmIdx]?.slice(0, 50) : `parse fail: ${raw}`}`)
            }
            suppressLogs = true
          }

          await sleep(500)  // rate limit
        } catch (e: any) {
          stat.llmFail++
          suppressLogs = false
          print(`  LLM error: ${e.message.slice(0, 100)}`)
          suppressLogs = true
          await sleep(1000)  // back off on error
        }
      } else if (opts.verbose) {
        // Default verbose (no LLM)
        const mcOk = choiceIndex === q.correct_choice_index
        suppressLogs = false
        print(`  ${mcOk ? 'OK' : 'XX'} [${q.question_type.padEnd(20)}] ${q.question.slice(0, 55)}`)
        if (!mcOk) {
          print(`     want: ${q.answer.slice(0, 50)}`)
          print(`     got:  ${q.choices[choiceIndex]?.slice(0, 50)} (conf=${confidence.toFixed(2)})`)
        }
        suppressLogs = true
      }
    } else if (opts.verbose && !isAdversarial) {
      // recall-only verbose
      const { hit, rank } = answerInRecalled(recalled, q.answer)
      suppressLogs = false
      print(`  ${hit ? 'HIT' : 'MISS'}@${rank > 0 ? rank : '-'} [${q.question_type.padEnd(20)}] ${q.question.slice(0, 55)}`)
      suppressLogs = true
    }

    // Record per-question result for conv-size bucketing
    perQuestionResult.push({ convId, hit: _qHit, mcCorrect: _qMCCorrect, isAdversarial })

    // Progress
    if ((qi + 1) % 50 === 0) {
      suppressLogs = false
      const elapsed = (Date.now() - startTime) / 1000
      print(`  ... ${qi + 1}/${questions.length} (${(elapsed).toFixed(0)}s)`)
      suppressLogs = true
    }
  }

  suppressLogs = false
  const elapsed = (Date.now() - startTime) / 1000
  const typeOrder = ['single_hop', 'multi_hop', 'temporal_reasoning', 'open_domain', 'adversarial']

  // ═══════════════════════════════════════════════════════════════
  // RESULTS: RECALL
  // ═══════════════════════════════════════════════════════════════

  print()
  print('═══════════════════════════════════════════════════════════')
  print(`  Layer 1: Recall Quality${opts.recallOnly ? ' (recall-only mode)' : ''}`)
  print('═══════════════════════════════════════════════════════════')
  print()

  if (opts.recallOnly) {
    // Detailed Hit@K breakdown
    print('  Type                    Hit@1   Hit@3   Hit@5  Hit@10    MRR     N')
    print('  ──────────────────────  ──────  ──────  ──────  ──────  ──────  ────')
    let tN = 0, t1 = 0, t3 = 0, t5 = 0, t10 = 0, tMRR = 0
    for (const type of typeOrder) {
      const s = typeStats[type]
      if (!s || s.recallTotal === 0) continue
      const n = s.recallTotal
      const h1 = (s.hitAt1 / n * 100).toFixed(1)
      const h3 = (s.hitAt3 / n * 100).toFixed(1)
      const h5 = (s.hitAt5 / n * 100).toFixed(1)
      const h10 = (s.hitAt10 / n * 100).toFixed(1)
      const mrr = (s.mrrSum / n).toFixed(3)
      print(`  ${type.padEnd(24)} ${h1.padStart(5)}%  ${h3.padStart(5)}%  ${h5.padStart(5)}%  ${h10.padStart(5)}%  ${mrr.padStart(6)}  ${String(n).padStart(4)}`)
      tN += n; t1 += s.hitAt1; t3 += s.hitAt3; t5 += s.hitAt5; t10 += s.hitAt10; tMRR += s.mrrSum
    }
    if (tN > 0) {
      print('  ──────────────────────  ──────  ──────  ──────  ──────  ──────  ────')
      print(`  ${'TOTAL'.padEnd(24)} ${(t1/tN*100).toFixed(1).padStart(5)}%  ${(t3/tN*100).toFixed(1).padStart(5)}%  ${(t5/tN*100).toFixed(1).padStart(5)}%  ${(t10/tN*100).toFixed(1).padStart(5)}%  ${(tMRR/tN).toFixed(3).padStart(6)}  ${String(tN).padStart(4)}`)
    }
  } else {
    // Compact Hit@K (original style, but now with Hit@10 = hitAt10)
    print('  Type                    Hit@K    MRR     N')
    print('  ──────────────────────  ──────  ──────  ────')
    let totalRecallHits = 0, totalRecallN = 0, totalMRR = 0
    for (const type of typeOrder) {
      const s = typeStats[type]
      if (!s || s.recallTotal === 0) continue
      const hitRate = (s.hitAt10 / s.recallTotal * 100).toFixed(1)
      const mrr = (s.mrrSum / s.recallTotal).toFixed(3)
      print(`  ${type.padEnd(24)} ${hitRate.padStart(5)}%  ${mrr.padStart(6)}  ${String(s.recallTotal).padStart(4)}`)
      totalRecallHits += s.hitAt10
      totalRecallN += s.recallTotal
      totalMRR += s.mrrSum
    }
    if (totalRecallN > 0) {
      print('  ──────────────────────  ──────  ──────  ────')
      print(`  ${'TOTAL'.padEnd(24)} ${(totalRecallHits / totalRecallN * 100).toFixed(1).padStart(5)}%  ${(totalMRR / totalRecallN).toFixed(3).padStart(6)}  ${String(totalRecallN).padStart(4)}`)
    }
  }

  // ═══════════════════════════════════════════════════════════════
  // RESULTS: MC ACCURACY (skip for recall-only)
  // ═══════════════════════════════════════════════════════════════

  if (!opts.recallOnly) {
    print()
    print('═══════════════════════════════════════════════════════════')
    print('  Layer 2: MC Accuracy (10 选 1)')
    print('═══════════════════════════════════════════════════════════')
    print()

    if (opts.llm) {
      // Side-by-side: string-match vs LLM
      print('  Type                    SM Acc   LLM Acc    N   (fail)')
      print('  ──────────────────────  ──────  ────────  ────  ──────')
      let tMC = 0, tSM = 0, tLLM = 0, tFail = 0
      for (const type of typeOrder) {
        const s = typeStats[type]
        if (!s || s.mcTotal === 0) continue
        const smAcc = (s.mcCorrect / s.mcTotal * 100).toFixed(1)
        const llmAcc = s.llmTotal > 0 ? (s.llmCorrect / s.llmTotal * 100).toFixed(1) : ' N/A'
        print(`  ${type.padEnd(24)} ${smAcc.padStart(5)}%  ${llmAcc.padStart(6)}%  ${String(s.mcTotal).padStart(4)}  ${String(s.llmFail).padStart(5)}`)
        tMC += s.mcTotal; tSM += s.mcCorrect; tLLM += s.llmCorrect; tFail += s.llmFail
      }
      if (tMC > 0) {
        print('  ──────────────────────  ──────  ────────  ────  ──────')
        print(`  ${'TOTAL'.padEnd(24)} ${(tSM/tMC*100).toFixed(1).padStart(5)}%  ${(tLLM/tMC*100).toFixed(1).padStart(6)}%  ${String(tMC).padStart(4)}  ${String(tFail).padStart(5)}`)
      }
    } else {
      // Original string-match only
      print('  Type                    Acc      N')
      print('  ──────────────────────  ──────  ────')
      let totalMC = 0, totalMCCorrect = 0
      for (const type of typeOrder) {
        const s = typeStats[type]
        if (!s || s.mcTotal === 0) continue
        const acc = (s.mcCorrect / s.mcTotal * 100).toFixed(1)
        print(`  ${type.padEnd(24)} ${acc.padStart(5)}%  ${String(s.mcTotal).padStart(4)}`)
        totalMC += s.mcTotal
        totalMCCorrect += s.mcCorrect
      }
      if (totalMC > 0) {
        print('  ──────────────────────  ──────  ────')
        print(`  ${'TOTAL'.padEnd(24)} ${(totalMCCorrect / totalMC * 100).toFixed(1).padStart(5)}%  ${String(totalMC).padStart(4)}`)
      }
    }
  }

  // ═══════════════════════════════════════════════════════════════
  // RESULTS: LATENCY STATISTICS
  // ═══════════════════════════════════════════════════════════════

  print()
  print('═══════════════════════════════════════════════════════════')
  print('  Layer 3: Latency & Storage')
  print('═══════════════════════════════════════════════════════════')
  print()

  if (perQueryLatency.length > 0) {
    const sorted = [...perQueryLatency].sort((a, b) => a - b)
    const p50 = sorted[Math.floor(sorted.length * 0.5)]
    const p95 = sorted[Math.floor(sorted.length * 0.95)]
    const p99 = sorted[Math.floor(sorted.length * 0.99)]
    const avg = sorted.reduce((a, b) => a + b, 0) / sorted.length
    print(`  Recall Latency (${sorted.length} queries):`)
    print(`    avg=${avg.toFixed(1)}ms  p50=${p50}ms  p95=${p95}ms  p99=${p99}ms`)
    print(`    throughput: ${(questions.length / elapsed).toFixed(1)} q/s`)
  }

  // Storage comparison: NAM vs Vector
  if (totalMemoryBytes > 0) {
    const namStorageKB = totalMemoryBytes / 1024
    // Vector embedding estimate: 1536-dim float32 per memory (OpenAI ada-002 standard)
    const totalMemories = [...convMemoryCount.values()].reduce((a, b) => a + b, 0)
    const vectorStorageKB = totalMemories * 1536 * 4 / 1024  // 1536 dims × 4 bytes/float32
    const aamStorageKB = 2300  // AAM cooccur ~2.3MB (from real data)
    print()
    print(`  Storage Comparison (${totalMemories} memories):`)
    print(`    NAM (text + AAM + SQLite):  ${((namStorageKB + aamStorageKB) / 1024).toFixed(1)} MB`)
    print(`    Vector (ada-002 1536d):     ${(vectorStorageKB / 1024).toFixed(1)} MB  (embeddings only, +index)`)
    print(`    Ratio: NAM is ${(vectorStorageKB / (namStorageKB + aamStorageKB)).toFixed(1)}x smaller`)
    print(`    External API calls: NAM=0  Vector=N (embedding generation)`)
  }

  // ═══════════════════════════════════════════════════════════════
  // RESULTS: RECALL BY CONVERSATION LENGTH
  // ═══════════════════════════════════════════════════════════════

  // Group per-question results by conversation memory pool size
  function getBucket(memCount: number): string {
    if (memCount <= 200) return 'small (≤200)'
    if (memCount <= 400) return 'medium (201-400)'
    if (memCount <= 600) return 'large (401-600)'
    return 'xlarge (600+)'
  }

  const lengthBuckets: Record<string, { hit: number; total: number; mcCorrect: number; mcTotal: number }> = {}
  for (const r of perQuestionResult) {
    const memCount = convMemoryCount.get(r.convId) || 0
    const bucket = getBucket(memCount)
    if (!lengthBuckets[bucket]) lengthBuckets[bucket] = { hit: 0, total: 0, mcCorrect: 0, mcTotal: 0 }
    const b = lengthBuckets[bucket]
    if (!r.isAdversarial) {
      b.total++
      if (r.hit) b.hit++
    }
    if (!opts.recallOnly) {
      b.mcTotal++
      if (r.mcCorrect) b.mcCorrect++
    }
  }

  print()
  print('═══════════════════════════════════════════════════════════')
  print('  Layer 4: Recall by Conversation Size')
  print('═══════════════════════════════════════════════════════════')
  print()

  // Per-conversation breakdown
  print('  Conv ID     Memories   Questions   Size Bucket')
  print('  ─────────  ────────  ──────────  ──────────────')
  for (const convId of convIds) {
    const memCount = convMemoryCount.get(convId) || 0
    const qCount = convMap.get(convId)?.length || 0
    if (memCount > 0) {
      print(`  ${convId.padEnd(10)} ${String(memCount).padStart(7)}   ${String(qCount).padStart(9)}   ${getBucket(memCount)}`)
    }
  }

  // Bucketed recall stats
  const bucketOrder = ['small (≤200)', 'medium (201-400)', 'large (401-600)', 'xlarge (600+)']
  print()
  print(`  Size Bucket          Hit@10    ${opts.recallOnly ? '' : 'MC Acc    '}N`)
  print(`  ───────────────────  ──────  ${opts.recallOnly ? '' : '──────  '}────`)
  for (const bucket of bucketOrder) {
    const b = lengthBuckets[bucket]
    if (!b || b.total === 0) continue
    const hitRate = (b.hit / b.total * 100).toFixed(1)
    const mcRate = b.mcTotal > 0 ? (b.mcCorrect / b.mcTotal * 100).toFixed(1) : '-'
    if (opts.recallOnly) {
      print(`  ${bucket.padEnd(21)} ${hitRate.padStart(5)}%  ${String(b.total).padStart(4)}`)
    } else {
      print(`  ${bucket.padEnd(21)} ${hitRate.padStart(5)}%  ${mcRate.padStart(5)}%  ${String(b.total).padStart(4)}`)
    }
  }

  // ═══════════════════════════════════════════════════════════════
  // Layer 5: 记忆量 vs 召回精度（按记忆池大小升序，证明"记忆越多不会变笨"）
  // ═══════════════════════════════════════════════════════════════

  print()
  print('═══════════════════════════════════════════════════════════')
  print('  Layer 5: Memory Pool Size vs Recall Accuracy')
  print('═══════════════════════════════════════════════════════════')
  print()

  // 按记忆量升序排列 conv
  const convsBySize = convIds
    .filter(id => convMemoryCount.get(id))
    .map(id => ({ id, memCount: convMemoryCount.get(id)!, questions: perQuestionResult.filter(r => r.convId === id) }))
    .sort((a, b) => a.memCount - b.memCount)

  print(`  Memories   Conv ID    Hit@10   ${opts.recallOnly ? '' : 'MC Acc   '}Questions`)
  print(`  ────────  ─────────  ──────  ${opts.recallOnly ? '' : '──────  '}─────────`)
  for (const conv of convsBySize) {
    const nonAdv = conv.questions.filter(r => !r.isAdversarial)
    const hits = nonAdv.filter(r => r.hit).length
    const total = nonAdv.length
    const hitRate = total > 0 ? (hits / total * 100).toFixed(1) : '-'
    if (opts.recallOnly) {
      print(`  ${String(conv.memCount).padStart(7)}   ${conv.id.padEnd(10)} ${hitRate.padStart(5)}%  ${String(total).padStart(8)}`)
    } else {
      const mcHits = conv.questions.filter(r => r.mcCorrect).length
      const mcTotal = conv.questions.length
      const mcRate = mcTotal > 0 ? (mcHits / mcTotal * 100).toFixed(1) : '-'
      print(`  ${String(conv.memCount).padStart(7)}   ${conv.id.padEnd(10)} ${hitRate.padStart(5)}%  ${mcRate.padStart(5)}%  ${String(total).padStart(8)}`)
    }
  }

  print()
  print(`  Random baseline: 10.0%`)
  print(`  Time: ${elapsed.toFixed(1)}s (${(questions.length / elapsed).toFixed(0)} q/s)`)
  print(`  Isolation: per-conv (AAM + fact-store reset between conversations)`)
  print()
}

run()
