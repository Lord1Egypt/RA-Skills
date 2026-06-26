/**
 * memory-utils.ts — Pure utility functions extracted from memory.ts
 * Trigrams, synonyms, time decay, compression, poisoning detection, etc.
 */

import type { Memory } from './types.ts'

/** Unified word extraction patterns — use these instead of inline regex */
export const WORD_PATTERN = {
  /** CJK 2+ chars OR English 3+ chars (most common) */
  CJK2_EN3: /[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}/gi,
  /** CJK 2-4 chars OR English 2+ chars OR digits (for BM25/fact matching) */
  CJK24_EN2_NUM: /[\u4e00-\u9fff]{2,4}|[a-zA-Z]{2,}|\d+/gi,
  /** CJK 2-4 chars OR English 3+ chars (for spreading activation/graph) */
  CJK24_EN3: /[\u4e00-\u9fff]{2,4}|[a-zA-Z]{3,}/gi,
}

/** Unified trigram similarity thresholds */
export const TRIGRAM_THRESHOLD = {
  /** Exact duplicate detection */
  DEDUP_EXACT: 0.9,
  /** Merge-worthy similarity */
  DEDUP_MERGE: 0.7,
  /** Strong interference suppression */
  INTERFERENCE_STRONG: 0.5,
  /** Light interference suppression */
  INTERFERENCE_LIGHT: 0.3,
  /** Topic freshness detection */
  TOPIC_FRESHNESS: 0.15,
  /** Graveyard revival threshold */
  GRAVEYARD_REVIVE: 0.5,
  /** Fallback similarity (CMR Layer 3) */
  FALLBACK: 0.6,
}

// ═══════════════════════════════════════════════════════════════════════════════
// Event-Driven Cache Coherence（原创算法）
// 各缓存注册自己关心的事件，事件发生时自动失效
// ═══════════════════════════════════════════════════════════════════════════════

export type CacheEvent =
  | 'memory_added' | 'memory_deleted' | 'memory_updated' | 'consolidation' | 'heartbeat'
  // 用户画像事件广播（保持分层但通气）
  | 'identity_changed'   // 身份信息变更（公司/城市/职业）
  | 'fact_updated'       // 事实更新（任何 fact-store 变更）
  | 'emotion_shifted'    // 情绪状态变化（压力/情绪切换）
  | 'correction_received' // 收到纠正

const _cacheListeners = new Map<CacheEvent, Array<() => void>>()

/** 注册缓存失效处理器 */
export function onCacheEvent(event: CacheEvent, handler: () => void): void {
  if (!_cacheListeners.has(event)) _cacheListeners.set(event, [])
  _cacheListeners.get(event)!.push(handler)
}

/** 触发缓存事件 */
export function emitCacheEvent(event: CacheEvent): void {
  const handlers = _cacheListeners.get(event) ?? []
  for (const h of handlers) {
    try { h() } catch (e: any) {
      console.error(`[cc-soul][cache] ${event} handler error: ${e.message}`)
    }
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// Memory ID + Lineage 工具
// ═══════════════════════════════════════════════════════════════════════════════

/** 生成唯一 memoryId（轻量，不依赖 nanoid） */
export function generateMemoryId(): string {
  return `m_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 8)}`
}

/** 追加 lineage 记录。cap 按 scope 分级：short_term=5, long_term/core=20, 其他=10 */
export function appendLineage(mem: any, entry: { action: string; ts: number; trigger?: string; delta?: string; from?: number; to?: number }): void {
  try {
    if (!mem.lineage) mem.lineage = []
    mem.lineage.push(entry)

    // Cap 按 scope 分级
    const cap = mem.scope === 'short_term' ? 5
      : (mem.scope === 'core_memory' || mem.tier === 'long_term') ? 20
      : 10

    if (mem.lineage.length > cap) {
      const created = mem.lineage.find((e: any) => e.action === 'created')
      const recent = mem.lineage.slice(-(cap - 1))
      mem.lineage = created ? [created, ...recent] : recent
    }
  } catch {}
}

// ═══════════════════════════════════════════════════════════════════════════════
// 排他性谓语表（事实版本链用）
// ═══════════════════════════════════════════════════════════════════════════════

/** 排他性谓语：同一主语只能有一个有效值。变化时建 supersedes 链 */
const EXCLUSIVE_PREDICATES = new Set([
  'name', '名字',
  'lives_in', '住在',
  'works_at', '工作',
  'occupation', '职业',
  'relationship', '配偶', '伴侣',
  'age', '年龄',
  'uses_phone', '手机',
  'educated_at', '学校',
  'salary', '薪资',
])

/** 判断冲突类型：supersede（取代）还是 supplement（补充） */
export function classifyConflict(oldFacts: any[], newFacts: any[]): 'supersede' | 'supplement' | 'refine' {
  for (const nf of newFacts) {
    const conflicting = oldFacts.find((of: any) =>
      of.subject === nf.subject && of.predicate === nf.predicate && of.object !== nf.object
    )
    if (conflicting && EXCLUSIVE_PREDICATES.has(nf.predicate)) {
      return 'supersede'  // 排他性谓语 + 同主语同谓语不同宾语 = 取代
    }
  }
  return 'supplement'  // 默认安全：不建链
}

// ═══════════════════════════════════════════════════════════════════════════════
// Constants — now backed by auto-tune, with legacy const for backward compat
// ═══════════════════════════════════════════════════════════════════════════════

// 保留旧的 const 作为向后兼容
export const MAX_MEMORIES = 10000
export const MAX_HISTORY = 100      // 保留最近 100 轮完整历史
export const INJECT_HISTORY = 30    // 注入最近 30 轮到 prompt（token 限制）

// ═══════════════════════════════════════════════════════════════════════════════
// Fisher-Yates Shuffle
// ═══════════════════════════════════════════════════════════════════════════════

/** Fisher-Yates shuffle — unbiased random ordering */
export function shuffleArray<T>(arr: T[]): T[] {
  const result = [...arr]
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]]
  }
  return result
}

// ═══════════════════════════════════════════════════════════════════════════════
// Unified Tokenizer — 合并 aam/memory-lifecycle/memory-recall 三套分词
// ═══════════════════════════════════════════════════════════════════════════════

const TOKENIZE_STOP_CHARS = new Set('的了是在我你他不有这那就也和但'.split(''))

/**
 * 统一分词函数（替代三套独立实现）
 * mode:
 *   'standard' — CJK 2-char 滑动窗口 + 3-4 char 整段 + 英文 3+ 字符，去重（原 aam.ts）
 *   'bigram'   — standard + 相邻词对 w1_w2（原 memory-lifecycle.ts SimHash 用）
 *   'bm25'     — CJK 2-gram + 3-gram + 停用词过滤（原 memory-recall.ts BM25 用）
 */
export function tokenize(text: string, mode: 'standard' | 'bigram' | 'bm25' = 'standard'): string[] {
  if (mode === 'bm25') {
    const tokens: string[] = []
    const segments = text.match(/[\u4e00-\u9fff]+|[a-zA-Z]{2,}|\d+/g) || []
    for (const seg of segments) {
      if (/[\u4e00-\u9fff]/.test(seg)) {
        for (let i = 0; i < seg.length - 1; i++) {
          const bigram = seg.slice(i, i + 2)
          if (!TOKENIZE_STOP_CHARS.has(bigram[0]) || !TOKENIZE_STOP_CHARS.has(bigram[1])) {
            tokens.push(bigram)
          }
          if (i < seg.length - 2) tokens.push(seg.slice(i, i + 3))
        }
      } else {
        tokens.push(seg.toLowerCase())
      }
    }
    return tokens
  }

  // standard + bigram 共用基础分词
  const words: string[] = []
  const cjkRaw = text.match(/[\u4e00-\u9fff]+/g) || []
  for (const seg of cjkRaw) {
    for (let i = 0; i <= seg.length - 2; i++) words.push(seg.slice(i, i + 2))
    if (seg.length >= 3 && seg.length <= 4) words.push(seg)
  }
  const enWords = text.match(/[a-zA-Z]{2,}|\d+/g) || []
  words.push(...enWords.map(w => w.toLowerCase()))

  if (mode === 'bigram') {
    const tokens: string[] = []
    const deduped = [...new Set(words)]
    for (let i = 0; i < deduped.length; i++) {
      tokens.push(deduped[i])
      if (i < deduped.length - 1) tokens.push(`${deduped[i]}_${deduped[i + 1]}`)
    }
    return tokens
  }

  return [...new Set(words)]
}

// ═══════════════════════════════════════════════════════════════════════════════
// Trigram Fuzzy Matching — fills the gap between exact-tag and TF-IDF
// ═══════════════════════════════════════════════════════════════════════════════

/** Extract character trigrams from text (works for CJK + Latin) — LRU cached (max 2000, evict oldest on overflow) */
const _trigramCache = new Map<string, Set<string>>()
export function trigrams(text: string): Set<string> {
  const s = text.toLowerCase().replace(/\s+/g, ' ').trim()
  const cached = _trigramCache.get(s)
  if (cached) {
    // LRU: move to end of Map insertion order
    _trigramCache.delete(s)
    _trigramCache.set(s, cached)
    return cached
  }
  const set = new Set<string>()
  for (let i = 0; i <= s.length - 3; i++) {
    set.add(s.slice(i, i + 3))
  }
  // LRU evict: delete oldest entries (front of Map) when over capacity
  if (_trigramCache.size >= 2000) {
    const evictCount = Math.ceil(_trigramCache.size * 0.2)
    const iter = _trigramCache.keys()
    for (let i = 0; i < evictCount; i++) {
      const k = iter.next().value
      if (k !== undefined) _trigramCache.delete(k)
    }
  }
  _trigramCache.set(s, set)
  return set
}

/** Jaccard similarity between two trigram sets: |A∩B| / |A∪B| — supports optional IDF weighting */
export function trigramSimilarity(a: Set<string>, b: Set<string>, idf?: Map<string, number>): number {
  if (a.size === 0 || b.size === 0) return 0

  // IDF-weighted Jaccard when idf map provided
  if (idf && idf.size > 0) {
    let intersection = 0, union = 0
    const all = new Set([...a, ...b])
    for (const t of all) {
      const w = idf.get(t) || 1.0
      const inA = a.has(t) ? 1 : 0
      const inB = b.has(t) ? 1 : 0
      intersection += Math.min(inA, inB) * w
      union += Math.max(inA, inB) * w
    }
    return union > 0 ? intersection / union : 0
  }

  // Plain Jaccard (original behavior when no idf)
  let intersection = 0
  for (const t of a) {
    if (b.has(t)) intersection++
  }
  const union = a.size + b.size - intersection
  return union > 0 ? intersection / union : 0
}

/**
 * 词级语义匹配：专门处理短文本去重（三角字对短文本不灵）
 * "用户住北京" vs "用户住在北京朝阳" → 词级重叠 = {"住":1, "北京":1} / total = 高
 * 补充 trigramSimilarity 对短文本的不足
 */
function wordOverlapSimilarity(textA: string, textB: string): number {
  const wordsA = new Set((textA.match(/[\u4e00-\u9fff]{2,}|[a-zA-Z]{2,}|\d+/gi) || []).map(w => w.toLowerCase()))
  const wordsB = new Set((textB.match(/[\u4e00-\u9fff]{2,}|[a-zA-Z]{2,}|\d+/gi) || []).map(w => w.toLowerCase()))
  if (wordsA.size === 0 || wordsB.size === 0) return 0
  let overlap = 0
  for (const w of wordsA) {
    if (wordsB.has(w)) overlap++
  }
  // Dice coefficient: 2*|A∩B| / (|A| + |B|) — 比 Jaccard 对短文本更友好
  return (2 * overlap) / (wordsA.size + wordsB.size)
}

/** 混合相似度：三角字 + 词级匹配 + AAM 同义词融合（短文本自动增强）*/
export function hybridSimilarity(textA: string, textB: string): number {
  const triSim = trigramSimilarity(trigrams(textA), trigrams(textB))
  const wordSim = wordOverlapSimilarity(textA, textB)
  let baseSim = Math.max(triSim, wordSim)

  // AAM 同义词融合：baseSim 在 0.25-0.5 的模糊区间时，查 AAM 共现补充
  if (baseSim >= 0.25 && baseSim < 0.5) {
    try {
      const aamMod = require('./aam.ts')
      if (aamMod.getCooccurrence) {
        const wordsA = new Set((textA.match(/[\u4e00-\u9fff]{2,}|[a-zA-Z]{2,}|\d+/gi) || []).map((w: string) => w.toLowerCase()))
        const wordsB = new Set((textB.match(/[\u4e00-\u9fff]{2,}|[a-zA-Z]{2,}|\d+/gi) || []).map((w: string) => w.toLowerCase()))
        let synonymMatches = 0
        for (const wA of wordsA) {
          if (wordsB.has(wA)) continue  // 已直接匹配
          // 查 AAM：wA 有没有跟 wordsB 中某个词高频共现？
          for (const wB of wordsB) {
            const cooccur = aamMod.getCooccurrence(wA, wB) ?? 0
            if (cooccur >= 3) { synonymMatches++; break }  // 共现 3+ 次视为同义
          }
        }
        if (wordsA.size > 0 && synonymMatches > 0) {
          const synonymBoost = (synonymMatches / wordsA.size) * 0.3
          baseSim = baseSim * 0.7 + (baseSim + synonymBoost) * 0.3
        }
      }
    } catch {}
  }

  return Math.min(1, baseSim)
}

/**
 * Context-Aware Similarity（原创算法）
 * 不只比较文本，还比较语境：时段、情绪、共享实体
 *
 * 用途：召回排序、联想触发。不用于 consolidation 聚类（聚类用 SimHash+cosine）。
 */
export function contextAwareSimilarity(a: Memory, b: Memory): number {
  // 文本相似度
  const textSim = hybridSimilarity(a.content, b.content)

  // 时间语境：是否在同一活跃时段
  const slot = (ts: number) => {
    const h = new Date(ts).getHours()
    return h < 6 ? 'night' : h < 12 ? 'morning' : h < 18 ? 'afternoon' : 'evening'
  }
  const slotA = slot(a.ts), slotB = slot(b.ts)
  const timeSim = slotA === slotB ? 1.0
    : ((slotA === 'night' && slotB === 'evening') || (slotA === 'evening' && slotB === 'night') ||
       (slotA === 'morning' && slotB === 'afternoon') || (slotA === 'afternoon' && slotB === 'morning')) ? 0.5
    : 0.0

  // 情绪语境
  const moodA = a.situationCtx?.mood ?? 0
  const moodB = b.situationCtx?.mood ?? 0
  const moodSim = 1 - Math.abs(moodA - moodB)

  // 实体共享度（懒加载 graph.ts）
  let entitySim = 0
  try {
    const { findMentionedEntities } = require('./graph.ts') as any
    const entA = new Set(findMentionedEntities(a.content) as string[])
    const entB = new Set(findMentionedEntities(b.content) as string[])
    let shared = 0
    for (const e of entA) if (entB.has(e)) shared++
    entitySim = shared / Math.max(1, Math.max(entA.size, entB.size))
  } catch {}

  return textSim * 0.4 + timeSim * 0.1 + moodSim * 0.2 + entitySim * 0.3
}


// ═══════════════════════════════════════════════════════════════════════════════
// Synonym Map — lightweight semantic expansion for tag matching
// ═══════════════════════════════════════════════════════════════════════════════

export const SYNONYM_MAP: Record<string, string[]> = {
  // Chinese synonyms
  '二进制': ['binary', 'mach-o', 'elf', '可执行文件', '逆向'],
  '逆向': ['reverse', '反编译', 'ida', 'frida', 'hook', '破解'],
  '代码': ['code', '函数', '脚本', 'script', '程序'],
  '部署': ['deploy', '上线', '发布', 'release', '服务器'],
  '数据库': ['database', 'sql', 'mysql', 'redis', 'mongodb', 'db'],
  '性能': ['performance', '优化', '速度', '延迟', 'latency'],
  '错误': ['error', 'bug', 'crash', '报错', '异常', 'exception'],
  '图片': ['image', 'ocr', '识别', '照片', 'screenshot', '截图'],
  '调试': ['debug', 'breakpoint', 'lldb', 'gdb', '断点'],
  '网络': ['network', 'http', 'tcp', 'socket', '请求', 'request'],
  '内存': ['memory', '泄漏', 'leak', 'malloc', '堆', 'heap'],
  '线程': ['thread', '并发', 'concurrent', '锁', 'lock', 'async'],
  // English synonyms
  'binary': ['二进制', 'mach-o', 'executable', 'elf'],
  'hook': ['frida', '拦截', 'intercept', 'swizzle'],
  'debug': ['调试', 'breakpoint', 'lldb', 'gdb'],
  'api': ['接口', 'endpoint', 'rest', 'http'],
  'deploy': ['部署', '上线', '发布', 'release'],
  'performance': ['性能', '优化', 'optimize', 'latency'],
  'error': ['错误', 'bug', 'crash', 'exception', '异常'],
  'memory': ['内存', 'leak', 'malloc', 'heap'],
  'thread': ['线程', '并发', 'concurrent', 'lock'],
  'python': ['py', 'pip', 'flask', 'django', '脚本'],
  'swift': ['swiftui', 'ios', 'xcode', 'objc', 'objective-c'],
  'test': ['测试', 'unittest', 'pytest', 'vitest', '单元测试'],
}


export function expandQueryWithSynonyms(words: Set<string>): Set<string> {
  const expanded = new Set(words)
  for (const word of words) {
    const synonyms = SYNONYM_MAP[word]
    if (synonyms) {
      for (const s of synonyms) expanded.add(s)
    }
  }
  return expanded
}

// ═══════════════════════════════════════════════════════════════════════════════
// Time Decay — unified Weibull model (delegates to smart-forget.ts)
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Unified time decay using Weibull survival model from smart-forget.ts.
 * Replaces the old exp(half-life) model for consistency across the codebase.
 */
let _sfMod: any = null
export function timeDecay(mem: Memory): number {
  // Lazy import (cached) to avoid circular dependency at module level
  if (!_sfMod) {
    try { _sfMod = require('./smart-forget.ts') } catch {
      // ESM fallback: use inline Weibull (same formula as smart-forget.ts)
      const ageDays = (Date.now() - (mem.lastAccessed || mem.ts || Date.now())) / 86400000
      const lambda = 30 // default fact scope
      return Math.exp(-Math.pow(ageDays / lambda, 1.5))
    }
  }
  const ageDays = (Date.now() - (mem.lastAccessed || mem.ts || Date.now())) / 86400000
  const lambda = _sfMod.effectiveLambda(mem.scope || 'fact', mem.recallCount ?? 0, mem.emotionIntensity)
  return _sfMod.weibullSurvival(ageDays, lambda, _sfMod.WEIBULL_K)
}

// ═══════════════════════════════════════════════════════════════════════════════
// Memory Semantic Compression — condense verbose memories into compact facts
// ═══════════════════════════════════════════════════════════════════════════════

/** Redundant prefixes/fillers to strip from memory text */
export const COMPRESS_PATTERNS: [RegExp, string][] = [
  // Remove "用户说/提到/表示/告诉我" etc. prefixes
  [/^(?:用户|他|她|对方)(?:说|提到|表示|告诉我|跟我说|反馈|回复|回答|补充|指出|觉得|认为|希望|想要|需要|打算|计划)\s*(?:了|过|着)?\s*(?:，|,)?\s*/g, ''],
  // Remove "我觉得/我认为/我发现" etc.
  [/(?:我觉得|我认为|我发现|我注意到|我看到|据说|好像|似乎|可能是|应该是)\s*(?:，|,)?\s*/g, ''],
  // Remove "其实/事实上/实际上/说实话/老实说"
  [/(?:其实|事实上|实际上|说实话|老实说|总的来说|简单来说|换句话说)\s*(?:，|,)?\s*/g, ''],
  // Remove "非常/特别/很/比较/相当" intensity modifiers (keep the adjective)
  [/(?:非常|特别|很|比较|相当|十分|极其|超级)\s*(?=[\u4e00-\u9fff])/g, ''],
  // Remove "的话/来说/而言/方面"
  [/(?:的话|来说|而言|方面|这块|这个)/g, ''],
  // Remove trailing "了/的/呢/吧/啊/嘛"
  [/[了的呢吧啊嘛]+\s*$/g, ''],
  // Collapse multiple spaces/punctuation
  [/\s{2,}/g, ' '],
  [/(?:，|,){2,}/g, '，'],
]

/**
 * Compress a verbose memory into a compact factual statement.
 * Pure text rules — no LLM call.
 */
export function compressMemory(memory: Memory): string {
  let text = memory.content.trim()

  // Short enough already — don't compress
  if (text.length <= 30) return text

  // Apply pattern-based compression
  for (const [pattern, replacement] of COMPRESS_PATTERNS) {
    text = text.replace(pattern, replacement)
  }

  // Trim leading/trailing punctuation
  text = text.replace(/^[，,、。：:；;\s]+/, '').replace(/[，,、。：:；;\s]+$/, '').trim()

  // If compression removed too much, return original
  if (text.length < 5) return memory.content.trim()

  return text
}

// ═══════════════════════════════════════════════════════════════════════════════
// Memory Poisoning Detection
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Memory poisoning defense: detect attempts to inject malicious content into memory store.
 * Checks for patterns that could manipulate future behavior via stored memories.
 */
export function detectMemoryPoisoning(content: string): boolean {
  const patterns = [
    /\bignore\s+(all\s+)?previous\b/i,
    /忽略(之前|上面|所有)(的)?指令/,
    /\byou\s+(are|must|should)\s+now\b/i,
    /\bfrom\s+now\s+on\b/i,
    /\bnew\s+(instructions?|rules?|persona)\s*:/i,
    /\bsystem\s*prompt\s*:/i,
    /\boverride\s+(all|system|safety|rules)\b/i,
    /你(现在|必须|应该)(是|变成|扮演)/,
    /\[INST\]|\[SYS\]|<<SYS>>|<\|im_start\|>/i,
  ]
  return patterns.some(p => p.test(content))
}

// ═══════════════════════════════════════════════════════════════════════════════
// Chain-of-Thought Reasoning Extraction
// ═══════════════════════════════════════════════════════════════════════════════

// ── Chain-of-Thought reasoning extraction ──
export function extractReasoning(content: string): { reasoning?: Memory['reasoning'] } {
  // Chinese: 因为X所以Y
  let m = content.match(/因为(.{3,80})所以(.{3,120})/)
  if (m) return { reasoning: { context: m[1].trim(), conclusion: m[2].trim(), confidence: 0.7 } }
  // English: based on X therefore Y / because X therefore Y
  m = content.match(/(?:based on|because)\s+(.{3,80})(?:therefore|so|thus)\s+(.{3,120})/i)
  if (m) return { reasoning: { context: m[1].trim(), conclusion: m[2].trim(), confidence: 0.7 } }
  // X → Y / X => Y (arrow notation)
  m = content.match(/(.{3,80})\s*[=\-]>\s*(.{3,120})/)
  if (m) return { reasoning: { context: m[1].trim(), conclusion: m[2].trim(), confidence: 0.6 } }
  return {}
}

// ═══════════════════════════════════════════════════════════════════════════════
// Default Visibility
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Default visibility based on scope:
 * - fact/discovery → global (technical facts everyone can use)
 * - correction/preference → channel (specific to where it happened)
 * - proactive/curiosity/reflection → private
 * - others → channel
 */
export function defaultVisibility(scope: string): 'global' | 'channel' | 'private' {
  if (scope === 'fact' || scope === 'discovery') return 'global'
  if (scope === 'correction' || scope === 'preference') return 'channel'
  if (scope === 'proactive' || scope === 'curiosity' || scope === 'reflection') return 'private'
  return 'channel'
}

// ═══════════════════════════════════════════════════════════════════════════════
// Polarity Flip Detection — 共享矛盾信号检测（smart-forget + distill 复用）
// ═══════════════════════════════════════════════════════════════════════════════

const CONTRADICTION_PAIRS: [RegExp, RegExp][] = [
  [/喜欢|爱|偏好/, /讨厌|不喜欢|不想/],
  [/在.*工作|在.*做/, /离职|辞职|被裁/],
  [/住在|住/, /搬到|搬去/],
  [/运动|跑步|健身/, /不运动|不跑|放弃/],
  [/学|在学/, /不学|放弃/],
  [/是|用/, /不是|不用|换了/],
]

/**
 * 检测两段文本之间是否存在极性翻转（矛盾信号）
 * 合并自 smart-forget.ts detectContradictionSignals + distill.ts 时序矛盾检测
 */
export function detectPolarityFlip(textA: string, textB: string): boolean {
  for (const [patA, patB] of CONTRADICTION_PAIRS) {
    if ((patA.test(textA) && patB.test(textB)) || (patB.test(textA) && patA.test(textB))) return true
  }
  return false
}

// ═══════════════════════════════════════════════════════════════════════════════
// Adaptive Decay — 通用自适应衰减（供 epistemic.ts 等复用）
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * 通用自适应衰减：年龄 + 使用频率 二维衰减
 * 供 epistemic.ts (知识衰减) 等复用
 *
 * @param ageMs - 距上次使用的毫秒数
 * @param useCount - 使用/命中次数
 * @param halfLifeMs - 基础半衰期（毫秒）
 * @param usageProtection - 每次使用降低衰减的系数（默认 0.5）
 * @returns 衰减后的保留率 [0, 1]
 */
export function adaptiveDecay(
  ageMs: number,
  useCount: number,
  halfLifeMs: number = 90 * 86400000,  // 默认 90 天
  usageProtection: number = 0.5,
): number {
  // 基础衰减：指数衰减
  const baseDecay = Math.exp(-ageMs * Math.LN2 / halfLifeMs)

  // 使用频率保护：hitCount 越高，衰减越慢
  const protection = 1 + useCount * usageProtection

  // 最终保留率
  const retention = 1 - (1 - baseDecay) / protection

  return Math.max(0, Math.min(1, retention))
}

