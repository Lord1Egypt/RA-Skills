/**
 * temporal-anchor.ts — Temporal Anchor Inference（时间锚推理）
 *
 * cc-soul 原创算法。零 LLM 时间推理。
 *
 * 解决的问题：
 *   "上个月说了什么" → 只靠 extractTimeRange 的正则太弱
 *   "Caroline 什么时候去的 support group" → 需要从 "yesterday" + session 日期推算
 *
 * 算法：
 *   1. 从 fact-store 三元组推理隐含时间（works_at 的 validUntil → 离职时间）
 *   2. 用 flashbulb 记忆（高情绪强度）作为时间锚点
 *   3. 相对时间推理："那之后" → 找最近的锚点往后搜
 *   4. 事件序列推理：A 发生�� B 之前 → A.ts < B.ts
 */

import type { Memory } from './types.ts'

// ═══════════════════════════════════════════════════════════════
// 时间锚点（Temporal Anchors）
// ═══════════════════════════════════════════════════════════════

interface TemporalAnchor {
  description: string   // "去成都旅游"
  timestamp: number     // 精确时间
  confidence: number    // 0-1
  source: 'explicit' | 'inferred' | 'flashbulb'
}

/**
 * 从记忆池提取时间锚点
 * 优先用 flashbulb 记忆���高情绪 = 时间记忆更准确，Cahill & McGaugh 1995）
 */
export function extractAnchors(memories: Memory[]): TemporalAnchor[] {
  const anchors: TemporalAnchor[] = []

  for (const mem of memories) {
    if (!mem.content || !mem.ts) continue

    // 高情绪记忆 = 强锚点（闪光灯记忆时间最准确）
    const ei = (mem as any).emotionIntensity || 0
    if (ei >= 0.7) {
      anchors.push({
        description: mem.content.slice(0, 50),
        timestamp: mem.ts,
        confidence: 0.9,
        source: 'flashbulb',
      })
      continue
    }

    // 高重要性记忆 = 中强锚点（summary/核心事实，时间可靠）
    if ((mem.importance || 0) >= 8) {
      anchors.push({
        description: mem.content.slice(0, 50),
        timestamp: mem.ts,
        confidence: 0.75,
        source: 'explicit',
      })
      continue
    }

    // 含明确时间词的记忆 = 中等锚点（中英文时间表达）
    const timeMatch = mem.content.match(
      /(\d{4})年|(\d{1,2})月(\d{1,2})[日号]|去年|今年|上个月|上周|前天|昨天|当时|那时候|那年|january|february|march|april|may|june|july|august|september|october|november|december|\d{1,2}\s+\w+\s+\d{4}|last\s+(week|month|year|time|night|summer|winter|spring|fall)|a\s+(few|couple)\s+(days|weeks|months|years)\s+ago|back\s+(in|when)|recently|the\s+other\s+day|earlier\s+this|years?\s+ago|months?\s+ago|weeks?\s+ago/i
    )
    if (timeMatch) {
      anchors.push({
        description: mem.content.slice(0, 50),
        timestamp: mem.ts,
        confidence: 0.7,
        source: 'explicit',
      })
    }
  }

  // 按时间排序
  anchors.sort((a, b) => a.timestamp - b.timestamp)
  return anchors
}

/**
 * 相对时间推理：从查询中的相对时间词推断目标时间范围
 * "那之后发生了什么" → 找最近的锚点，返回 [anchor.ts, now]
 * "在那之前" → 返回 [0, anchor.ts]
 */
export function inferTimeRange(
  query: string,
  anchors: TemporalAnchor[],
  recentContext?: string,
): { from: number; to: number } | null {
  if (anchors.length === 0) return null

  const now = Date.now()

  // 相对时间推理
  if (/那之后|后来|然后|接着|after that|since then|afterwards/.test(query)) {
    // 找最近被提到的锚点
    const recent = findReferencedAnchor(query, anchors, recentContext)
    if (recent) return { from: recent.timestamp, to: now }
  }

  if (/那之前|以前|曾经|before that|prior to|previously/.test(query)) {
    const recent = findReferencedAnchor(query, anchors, recentContext)
    if (recent) return { from: 0, to: recent.timestamp }
  }

  // "同一时期" / "那段时间"
  if (/同一时期|那段时间|那时候|那会儿|around that time|back then/.test(query)) {
    const recent = findReferencedAnchor(query, anchors, recentContext)
    if (recent) {
      const window = 30 * 86400000  // ±30 天
      return { from: recent.timestamp - window, to: recent.timestamp + window }
    }
  }

  return null
}

/**
 * 从查询或上下文中找到被引用的锚点
 */
function findReferencedAnchor(
  query: string,
  anchors: TemporalAnchor[],
  recentContext?: string,
): TemporalAnchor | null {
  const searchText = (query + ' ' + (recentContext || '')).toLowerCase()

  // 找描述文本跟查询/上下文有关键词重叠的锚点
  let bestAnchor: TemporalAnchor | null = null
  let bestOverlap = 0

  for (const anchor of anchors) {
    const anchorWords = anchor.description.toLowerCase().match(/[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}/g) || []
    let overlap = 0
    for (const w of anchorWords) {
      if (searchText.includes(w)) overlap++
    }
    if (overlap > bestOverlap) {
      bestOverlap = overlap
      bestAnchor = anchor
    }
  }

  // 如果没找到匹配的锚点，返回最近的 flashbulb
  if (!bestAnchor) {
    bestAnchor = anchors.filter(a => a.source === 'flashbulb').pop() || null
  }

  return bestAnchor
}

/**
 * 从 fact-store 的版本链推理隐含时间
 * works_at(Google, validUntil=1700000000) → 2023-11 之前在 Google
 * works_at(Meta, ts=1700100000) → 2023-11 之后在 Meta
 */
export function inferFactTimeline(facts: any[]): Map<string, { from: number; to: number }> {
  const timeline = new Map<string, { from: number; to: number }>()

  // 按 subject+predicate 分组
  const groups = new Map<string, any[]>()
  for (const fact of facts) {
    const key = `${fact.subject}:${fact.predicate}`
    if (!groups.has(key)) groups.set(key, [])
    groups.get(key)!.push(fact)
  }

  for (const [key, factsGroup] of groups) {
    // 按时间排序
    factsGroup.sort((a: any, b: any) => (a.ts || 0) - (b.ts || 0))

    for (let i = 0; i < factsGroup.length; i++) {
      const fact = factsGroup[i]
      const nextFact = factsGroup[i + 1]
      const factKey = `${key}:${fact.object}`

      timeline.set(factKey, {
        from: fact.ts || 0,
        to: fact.validUntil && fact.validUntil > 0
          ? fact.validUntil
          : nextFact ? nextFact.ts : Date.now(),
      })
    }
  }

  return timeline
}
