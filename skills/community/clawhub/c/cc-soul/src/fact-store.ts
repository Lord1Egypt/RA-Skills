/**
 * fact-store.ts — Structured Fact Extraction & Storage
 *
 * Mem0-style key-value fact store. Extracts subject-predicate-object triples
 * from natural language memories for precise querying.
 *
 * Two extraction modes:
 *   1. Rule-based (instant, zero LLM cost) — pattern matching
 *   2. LLM-based (async, via spawnCLI) — deep extraction on heartbeat
 */

import type { StructuredFact } from './types.ts'
import { DATA_DIR, loadJson, debouncedSave } from './persistence.ts'
import { resolve } from 'path'
import {
  isSQLiteReady, sqliteAddFact, sqliteQueryFacts,
  sqliteInvalidateFacts, sqliteFactCount, sqliteGetFactsBySubject,
  sqliteLoadAllFacts,
} from './sqlite-store.ts'

const FACTS_PATH = resolve(DATA_DIR, 'structured_facts.json')
// Load from SQLite if available, otherwise fall back to JSON
let facts: StructuredFact[] = isSQLiteReady()
  ? sqliteLoadAllFacts()
  : loadJson<StructuredFact[]>(FACTS_PATH, [])
// saveFacts is now a no-op: all writes go through sqliteAddFact in addFacts()
function saveFacts() { /* no-op: data persisted via SQLite */ }

// ═══════════════════════════════════════════════════════════════════════════════
// RULE-BASED EXTRACTION — instant, zero cost
// ═══════════════════════════════════════════════════════════════════════════════

interface ExtractionRule {
  pattern: RegExp
  extract: (match: RegExpMatchArray, content: string) => StructuredFact | null
}

const RULES: ExtractionRule[] = [
  // "我叫X" / "我是X" / "我名字叫X" / "大家叫我X" / "my name is X" / "call me X" → name
  { pattern: /(?:我叫|我名字(?:是|叫)|大家(?:都)?叫我|我的名字(?:是|叫)?|my name is|i'm called|call me|i am)\s*([^\s，。！？,;；\n]{1,8})/i, extract: (m) => {
    const name = m[1].trim()
    // 排除疑问句："我叫什么名字" / "我叫什么" 不是在告诉名字
    if (/^(什么|啥|谁|哪|吗|呢|嘛)/.test(name)) return null
    // 排除英文常见非名字词（"i am fine" / "i am tired" 等不是名字）
    if (/^(fine|good|ok|okay|tired|happy|sad|sorry|here|back|done|sure|ready|not|just|also|very|so|a|an|the|doing|going|trying|using|looking|working|from)\b/i.test(name)) return null
    if (name.length < 1) return null
    return { subject: 'user', predicate: 'name', object: name,
      confidence: 0.95, source: 'user_said', ts: Date.now(), validUntil: 0 }
  }},
  // "我喜欢X" / "我爱X" / "我偏好X" — stop at punctuation or conjunctions
  { pattern: /我(?:喜欢|爱|偏好|特别喜欢|超喜欢)(?:用)?\s*([^，。！？,;；\n]{2,15})/, extract: (m) => ({
    subject: 'user', predicate: 'likes', object: m[1].trim(),
    confidence: 0.85, source: 'user_said', ts: Date.now(), validUntil: 0,
  })},
  // "我不喜欢X" / "我讨厌X" / "我不爱X" / "i don't like" / "i hate" / "i dislike"
  { pattern: /(?:我(?:不喜欢|讨厌|不爱|不想用|受不了)|i don'?t like|i hate|i dislike|can'?t stand)\s*(.{2,20})/i, extract: (m) => ({
    subject: 'user', predicate: 'dislikes', object: m[1].replace(/[。，！？\s]+$/, ''),
    confidence: 0.85, source: 'user_said', ts: Date.now(), validUntil: 0,
  })},
  // "我用X" / "我在用X" / "我常用X" / "i use" / "i'm using"
  { pattern: /(?:我(?:用|在用|常用|一直用)|i use|i'm using|i usually use)\s*(.{2,20})/i, extract: (m) => ({
    subject: 'user', predicate: 'uses', object: m[1].replace(/[。，！？\s]+$/, ''),
    confidence: 0.8, source: 'user_said', ts: Date.now(), validUntil: 0,
  })},
  // "我在X工作" / "我在X做Y" / "我是X的" / "i work at" / "i work for" / "employed at"
  { pattern: /(?:我(?:在|是)\s*(.{2,15})(?:工作|上班|就职|的员工|做\S{2,10})|(?:i work (?:at|for)|employed at)\s*(.{2,15}))/i, extract: (m) => ({
    subject: 'user', predicate: 'works_at', object: (m[2] || m[0].replace(/^我(?:在|是)\s*/, '')).replace(/^(?:i work (?:at|for)|employed at)\s*/i, '').replace(/[。，！？\s]+$/, ''),
    confidence: 0.9, source: 'user_said', ts: Date.now(), validUntil: 0,
  })},
  // "我住在X" / "i live in" / "i'm based in" / "i'm from" — only match explicit residence, not "我在X工作"
  { pattern: /(?:我(?:住在|住|搬到|搬去|移居|去了)\s*|已经(?:搬|到)了?\s*|i live in\s*|i'm based in\s*|i'm from\s*)([^，。！？,;；\n]{2,10})/i, extract: (m) => {
    const place = m[1].trim()
    if (place.length < 2 || /^(这|那|哪|什么|怎么)/.test(place)) return null
    if (/工作|上班|就职/.test(place)) return null  // "住在X工作" → skip
    return { subject: 'user', predicate: 'lives_in', object: place,
      confidence: 0.7, source: 'user_said', ts: Date.now(), validUntil: 0 }
  }},
  // "我是做X的" / "我是X工程师/开发/设计师" / "i'm a X" / "i work as" / "my job is"
  { pattern: /(?:我是(?:做)?(.{2,15})(?:的|工程师|开发|设计师|产品|运营)|(?:i'm a|i work as|my job is)\s*(.{2,15}))/i, extract: (m) => ({
    subject: 'user', predicate: 'occupation', object: (m[2] || m[1]).replace(/[。，！？\s]+$/, ''),
    confidence: 0.85, source: 'user_said', ts: Date.now(), validUntil: 0,
  })},
  // "X比Y好" / "X比Y快" — preference
  { pattern: /(.{2,10})比(.{2,10})(?:好|快|强|稳定|方便|简单|简洁|好用|舒服|靠谱)/, extract: (m) => ({
    subject: 'user', predicate: 'prefers', object: `${m[1].trim()} over ${m[2].trim()}`,
    confidence: 0.7, source: 'ai_inferred', ts: Date.now(), validUntil: 0,
  })},
  // "我X岁" / "我今年X" / "i'm X years old" / "i am X" → age
  { pattern: /(?:我(?:今年)?(\d{1,3})岁|i(?:'m| am)\s*(\d{1,3})\s*(?:years?\s*old)?)/i, extract: (m) => ({
    subject: 'user', predicate: 'age', object: m[1] || m[2],
    confidence: 0.9, source: 'user_said', ts: Date.now(), validUntil: 0,
  })},
  // "我养了一只猫叫X" / "我家有一条狗" / "i have a pet" / "my cat" / "my dog" → has_pet（匹配到句尾，保留名字）
  { pattern: /(?:我们?(?:养了|家有|有一只|有一条|有一个)|i have a pet|i own a|my cat|my dog)\s*([^，。！？,;；\n]{2,20})/i, extract: (m) => {
    let obj = m[1].trim().replace(/[。，！？\s]+$/, '')
    if (obj.length < 2 || /^(什么|哪|这|那)/.test(obj)) return null
    return { subject: 'user', predicate: 'has_pet', object: obj,
      confidence: 0.8, source: 'user_said', ts: Date.now(), validUntil: 0 }
  }},
  // "我有个女儿/儿子/孩子" / "我有X个孩子" / "i have a daughter/son" / "my kid" → has_family
  { pattern: /(?:我有(?:个|一个|两个|三个)?\s*([^，。！？,;；\n]{1,10}?)(?:女儿|儿子|孩子|闺女|宝宝|小孩|老婆|老公|丈夫|妻子|爸|妈|哥|姐|弟|妹)|i have a\s*(daughter|son|kid|child)|my\s*(kid|child|son|daughter))/i, extract: (m) => ({
    subject: 'user', predicate: 'has_family', object: (m[2] || m[3] || m[0].replace(/^我有(?:个|一个|两个|三个)?\s*/, '').replace(/^(?:i have a|my)\s*/i, '')).replace(/[。，！？\s]+$/, ''),
    confidence: 0.9, source: 'user_said', ts: Date.now(), validUntil: 0,
  })},
  // "我女儿/儿子叫X" → family_name
  { pattern: /我(?:女儿|儿子|孩子|闺女|宝宝|老婆|老公)叫\s*([^，。！？,;；\n]{1,8})/, extract: (m) => ({
    subject: 'user', predicate: 'family_name', object: m[0].replace(/^我/, '').replace(/[。，！？\s]+$/, ''),
    confidence: 0.9, source: 'user_said', ts: Date.now(), validUntil: 0,
  })},
  // "我每天X" / "我习惯X" / "i always" / "every day i" / "my daily" → habit
  { pattern: /(?:我(?:每天|习惯|一般都|通常|经常)|i always|every day i|my daily)\s*([^，。！？,;；\n]{2,20})/i, extract: (m) => ({
    subject: 'user', predicate: 'habit', object: m[1].replace(/[。，！？\s]+$/, ''),
    confidence: 0.75, source: 'user_said', ts: Date.now(), validUntil: 0,
  })},
  // "我毕业于X" / "我读的X大学" / "i graduated from" / "i went to" / "my school" / "my university" → educated_at
  { pattern: /(?:我(?:毕业于|毕业|读的|上的)|i graduated from|i went to|my school is|my university is)\s*([^，。！？,;；\n]{2,15})(?:大学|学院|学校)?/i, extract: (m) => ({
    subject: 'user', predicate: 'educated_at', object: m[1].replace(/[。，！？\s]+$/, ''),
    confidence: 0.85, source: 'user_said', ts: Date.now(), validUntil: 0,
  })},
  // "我老婆/老公/女朋友/男朋友" / "my wife/husband/girlfriend/boyfriend" → relationship
  { pattern: /(?:我(?:老婆|老公|女朋友|男朋友|媳妇|对象|另一半|爱人)|my (?:wife|husband|girlfriend|boyfriend|partner|spouse))\s*([^，。！？,;；\n\s]{0,8})/i, extract: (m, content) => {
    const relType = m[0].match(/老婆|老公|女朋友|男朋友|媳妇|对象|另一半|爱人|wife|husband|girlfriend|boyfriend|partner|spouse/i)?.[0] || 'partner'
    const detail = m[1]?.trim()
    // 过滤隐式疑问：捕获内容含"什么/哪/谁/怎么/叫什么" = 在提问不是在陈述
    if (detail && /什么|哪|谁|怎么|吗$|呢$/.test(detail)) return null
    return { subject: 'user', predicate: 'relationship', object: detail ? `${relType}：${detail}` : relType,
      confidence: 0.85, source: 'user_said', ts: Date.now(), validUntil: 0 }
  }},
  // "我住X楼/X层" → lives_in (floor)
  { pattern: /我住(?:在)?(\d{1,3})(?:楼|层)/, extract: (m) => ({
    subject: 'user', predicate: 'lives_in', object: `${m[1]}楼`,
    confidence: 0.7, source: 'user_said', ts: Date.now(), validUntil: 0,
  })},
  // "我用Mac/Windows/Linux" → uses_os
  { pattern: /我(?:用|在用|一直用)\s*(Mac|MacBook|Windows|Linux|Ubuntu|macOS|win|WSL)/i, extract: (m) => ({
    subject: 'user', predicate: 'uses_os', object: m[1],
    confidence: 0.85, source: 'user_said', ts: Date.now(), validUntil: 0,
  })},
]

/**
 * Extract structured facts from a text string (rule-based, instant).
 * Returns new facts not already in the store.
 */
export function extractFacts(content: string, source: StructuredFact['source'] = 'user_said', userId?: string): StructuredFact[] {
  const extracted: StructuredFact[] = []

  // 疑问句整体过滤：提问不是在陈述事实
  const trimmed = content.trim()
  const isQuestion = /[？?]$/.test(trimmed) ||              // 问号结尾
    /(.)\1不\1/.test(trimmed) ||                             // 动词重叠（是不是/有没有）
    /[吗呢吧嘛]$/.test(trimmed) ||                           // 语气词结尾
    /^.{0,6}(?:什么|哪个|哪里|谁|怎么|为什么)/.test(trimmed) || // 开头附近有疑问代词
    /(?:叫|是|做|在|有)(?:什么|哪个|谁|怎么)/.test(trimmed) || // 动词+疑问代词（"叫什么""做什么""是谁"）
    /(?:什么|哪|谁|怎么|多少|几)(?:时候|地方|样|个|种|岁|楼)/.test(trimmed) || // 疑问代词+量词/名词
    /^(?:what|who|where|when|why|how|which|do you|does|did|is|are|was|were|can|could|will|would)\b/i.test(trimmed) || // English question starters
    /\b(?:what is|who is|what's my|where do i|what do i)\b/i.test(trimmed) // English question phrases
  if (isQuestion) {
    return extracted
  }

  // LLM 分析内容过滤：方括号标签开头的内容是系统生成的分析，不是用户说的事实
  // 动态判断：用户说话不会以 [标签] 开头
  if (/^\[.{1,10}\]/.test(trimmed)) {
    return extracted
  }

  // 获取当前话题段 ID（话题河流关联）
  let _currentSegmentId = 0
  try { _currentSegmentId = require('./memory.ts').getCurrentSegmentId?.() ?? 0 } catch {}

  // ── 动态引擎提取（优先）──
  try {
    const { dynamicExtract, updateStructureStrength } = require('./dynamic-extractor.ts')
    const dynamicResults = dynamicExtract(content, userId)
    for (const r of dynamicResults) {
      const exists = facts.some(f =>
        f.subject === r.subject && f.predicate === r.predicate &&
        f.object === r.object && f.validUntil === 0
      )
      if (!exists) {
        // P1 fix: 加入 segmentId 关联话题河流
        let _segId: number | undefined
        try { _segId = require('./memory.ts').getCurrentSegmentId?.() } catch {}
        const fact: StructuredFact = {
          subject: r.subject, predicate: r.predicate, object: r.object,
          confidence: r.confidence, source: r.source as any,
          ts: Date.now(), validUntil: 0, memoryRef: content.slice(0, 60), segmentId: _segId ?? _currentSegmentId,
        }
        extracted.push(fact)
        // 反馈强度学习
        if (userId) updateStructureStrength(r.structureWord, userId, true)
      }
    }
  } catch {}

  // ── 旧正则规则（种子兜底）——动态提取器已覆盖的 predicate 跳过 ──
  const dynamicPredicates = new Set(extracted.map(e => e.predicate))
  for (const rule of RULES) {
    const match = content.match(rule.pattern)
    if (match) {
      const fact = rule.extract(match, content)
      if (fact) {
        // 动态提取器已提取了同 predicate → 跳过正则（动态结果更准）
        if (dynamicPredicates.has(fact.predicate)) continue
        fact.source = source
        fact.memoryRef = content.slice(0, 60)
        // Dedup: skip if same subject+predicate+object already extracted
        const exists = facts.some(f =>
          f.subject === fact.subject && f.predicate === fact.predicate &&
          f.object === fact.object && f.validUntil === 0
        ) || extracted.some(e =>
          e.subject === fact.subject && e.predicate === fact.predicate &&
          e.object === fact.object
        )
        if (!exists) extracted.push(fact)
      }
    }
  }
  // ── LLM 兜底提取（正则+动态引擎都没提取到 + 消息够长 + 有 LLM）──
  if (extracted.length === 0 && content.length > 15) {
    try {
      const { hasLLM, spawnCLI } = require('./cli.ts')
      if (hasLLM()) {
        const { getCurrentSegmentId } = require('./memory.ts')
        const _segId = getCurrentSegmentId?.() ?? 0
        spawnCLI(
          `从这句话提取事实三元组。输出JSON数组：[{"subject":"主语","predicate":"谓语","object":"宾语"}]。没有事实就输出[]。\nExtract fact triples from this sentence. Output JSON array: [{"subject":"subject","predicate":"predicate","object":"object"}]. If no facts, output [].\n\n"${content.slice(0, 200)}"`,
          (output: string) => {
            try {
              const parsed = JSON.parse(output.match(/\[[\s\S]*\]/)?.[0] || '[]')
              if (parsed.length > 0) {
                const llmFacts: StructuredFact[] = parsed.slice(0, 3).map((f: any) => ({
                  subject: f.subject || 'user', predicate: f.predicate, object: f.object,
                  confidence: 0.7, source: 'ai_inferred' as any, ts: Date.now(), validUntil: 0,
                  memoryRef: content.slice(0, 60), segmentId: _segId,
                }))
                addFacts(llmFacts)
                try { require('./decision-log.ts').logDecision('llm_fact_extract', content.slice(0, 30), `${llmFacts.length} facts extracted by LLM`) } catch {}
              }
            } catch {}
          },
          15000
        )
      }
    } catch {}
  }

  return extracted
}

/**
 * Add facts to the store. Auto-invalidates conflicting old facts.
 */
export function addFacts(newFacts: StructuredFact[]) {
  for (const nf of newFacts) {
    // 完全重复去重：同 subject+predicate+object 的 active fact 已存在则跳过
    const exactDup = facts.some(f =>
      f.subject === nf.subject && f.predicate === nf.predicate &&
      f.object === nf.object && f.validUntil === 0
    )
    if (exactDup) continue

    // 质量过滤：新 fact 比旧 fact 信息量更少时不做 supersede
    // 防止"我养了宠物 叫什么来着"→ has_pet=宠物 覆盖 has_pet=一只叫豆豆的猫
    let shouldSupersede = true
    for (const old of facts) {
      if (old.subject === nf.subject && old.predicate === nf.predicate &&
          old.object !== nf.object && old.validUntil === 0) {
        // 非排他性谓语（learning/likes/habit）：追加而不是 supersede
        // 排他性谓语（name/lives_in/works_at/relationship）：正常 supersede
        const NON_EXCLUSIVE = new Set(['learning', 'likes', 'dislikes', 'habit', 'prefers'])
        if (NON_EXCLUSIVE.has(nf.predicate)) {
          shouldSupersede = false  // 不 supersede，直接追加
          break
        }
        // 排他性谓语：新 object 比旧 object 短 50%+ 且旧的 confidence 更高 → 不覆盖
        if (nf.object.length < old.object.length * 0.5 && (old.confidence ?? 0) >= (nf.confidence ?? 0)) {
          console.log(`[cc-soul][facts] skip supersede (info loss): "${nf.object}" < "${old.object}"`)
          ;(nf as any)._skipReason = 'info_loss'
          shouldSupersede = false
          break
        }
      }
    }
    // Invalidate conflicting facts (same subject+predicate, different object)
    if (shouldSupersede) {
      for (const old of facts) {
        if (old.subject === nf.subject && old.predicate === nf.predicate &&
            old.object !== nf.object && old.validUntil === 0) {
          old.validUntil = Date.now()
          nf.supersedes = old.object  // 事实版本链：记录被取代的旧值
          console.log(`[cc-soul][facts] superseded: ${old.subject}.${old.predicate}="${old.object}" → "${nf.object}"`)
        }
      }
    } else if (nf._skipReason === 'info_loss') {
      continue  // 真正的低质量 → 跳过
    }
    // 非排他性谓语不 supersede 但仍然追加（likes/learning/habit 可以有多个值）
    facts.push(nf)

    // 交叉学习：只学 object，不学元词（subject 通常是 "user"，predicate 是 "likes/uses"）
    // 元词进 AAM 会成为高频锚点污染 PMI
    try {
      if (nf.object && nf.object.length >= 2) {
        const { learnAssociation } = require('./aam.ts')
        learnAssociation(nf.object, 0, 0.8)
      }
    } catch {}

    // Dual-write to SQLite (indexed queries)
    if (isSQLiteReady()) {
      try {
        sqliteInvalidateFacts(nf.subject, nf.predicate, nf.object)
        sqliteAddFact(nf)
      } catch { /* JSON fallback still works */ }
    }
  }
  if (newFacts.length > 0) {
    saveFacts()
    console.log(`[cc-soul][facts] added ${newFacts.length} structured facts`)
    try { const { emitCacheEvent } = require('./memory-utils.ts'); emitCacheEvent('fact_updated') } catch {}
  }
}

/**
 * Query facts by subject and/or predicate.
 * Only returns valid (non-expired) facts.
 */
export function queryFacts(opts: { subject?: string; predicate?: string; object?: string }): StructuredFact[] {
  // Prefer SQLite: uses idx_fact_subj_pred index → O(log n)
  if (isSQLiteReady()) {
    try {
      const results = sqliteQueryFacts(opts)
      if (results.length > 0) return results
    } catch { /* fallback to in-memory */ }
  }

  // Fallback: in-memory array scan
  return facts.filter(f => {
    if (f.validUntil > 0) return false  // expired
    if (opts.subject && f.subject !== opts.subject) return false
    if (opts.predicate && f.predicate !== opts.predicate) return false
    if (opts.object && !f.object.includes(opts.object)) return false
    return true
  })
}

/**
 * 事实演化时间线（Zep 启发）：同一 subject+predicate 的所有版本按时间排列
 * 返回最新版 + 变化轨迹。用户问"以前"时返回历史版本。
 */
export function queryFactTimeline(subject: string, predicate: string): Array<{ object: string; validFrom: number; validUntil: number; confidence: number; source: string }> {
  // 包含已失效的版本（validUntil > 0）
  const allVersions = facts.filter(f =>
    f.subject === subject && f.predicate === predicate
  ).sort((a, b) => a.ts - b.ts)

  // SQLite 补充
  if (isSQLiteReady() && allVersions.length === 0) {
    try {
      const results = sqliteQueryFacts({ subject, predicate })
      // SQLite 版本只返回有效的，还需要查过期的
      // 暂用内存版本
    } catch {}
  }

  return allVersions.map(f => ({
    object: f.object,
    validFrom: f.ts,
    validUntil: f.validUntil,
    confidence: f.confidence,
    source: f.source,
  }))
}

/**
 * 格式化事实时间线为可读字符串
 */
export function formatFactTimeline(subject: string, predicate: string): string | null {
  const timeline = queryFactTimeline(subject, predicate)
  if (timeline.length <= 1) return null  // 无变化历史

  const current = timeline.find(v => v.validUntil === 0) ?? timeline[timeline.length - 1]
  const history = timeline.filter(v => v.validUntil > 0)

  if (history.length === 0) return null

  const historyStr = history.map(v => {
    const date = new Date(v.validFrom).toLocaleDateString('zh-CN')
    return `${date}:${v.object}`
  }).join(' → ')

  return `${predicate}: ${historyStr} → 现在:${current.object}`
}

/**
 * Get all valid facts for a subject (usually "user"), formatted as readable string.
 */
export function getFactSummary(subject = 'user'): string {
  let valid: StructuredFact[]
  if (isSQLiteReady()) {
    try { valid = sqliteGetFactsBySubject(subject) } catch { valid = [] }
  } else {
    valid = facts.filter(f => f.subject === subject && f.validUntil === 0)
  }
  if (valid.length === 0) return ''

  const grouped: Record<string, string[]> = {}
  for (const f of valid) {
    if (!grouped[f.predicate]) grouped[f.predicate] = []
    grouped[f.predicate].push(f.object)
  }

  const LABELS: Record<string, string> = {
    name: '名字', likes: '喜欢', dislikes: '不喜欢', uses: '使用', works_at: '工作于',
    lives_in: '住在', occupation: '职业', prefers: '偏好', has: '拥有',
    age: '年龄', has_pet: '养宠', has_family: '家人', habit: '习惯', educated_at: '毕业于',
    relationship: '伴侣', family_name: '家人名字', learning: '在学', uses_os: '操作系统',
  }

  return Object.entries(grouped)
    .map(([pred, objs]) => `${LABELS[pred] || pred}: ${objs.join('、')}`)
    .join('；')
}

/**
 * Auto-extract facts from a memory being added.
 * Call this from addMemory() in memory.ts.
 */
export function autoExtractFromMemory(content: string, scope: string, source?: StructuredFact['source']) {
  // Only extract from user-facing scopes
  if (['expired', 'decayed', 'dream', 'curiosity', 'system'].includes(scope)) return
  const autoSource = source || (scope === 'correction' || scope === 'preference' ? 'user_said' : 'ai_observed')
  const newFacts = extractFacts(content, autoSource)
  if (newFacts.length > 0) addFacts(newFacts)
}

export function getAllFacts(): StructuredFact[] { return facts }

/** 清空所有事实（benchmark per-conv 隔离用）*/
export function clearFacts(): void {
  facts.length = 0
}
export function getFactCount(): number {
  if (isSQLiteReady()) { try { return sqliteFactCount() } catch { /* fallback */ } }
  return facts.filter(f => f.validUntil === 0).length
}
