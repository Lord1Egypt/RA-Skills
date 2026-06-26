/**
 * answer-affinity.ts — Answer Affinity Scoring（答案亲和度评分）
 *
 * cc-soul 原创算法。记忆注入后的闭环反馈。
 *
 * 解决的问题：
 *   注入的记忆是否真的帮到了回答？没有反馈 = 无法自我优化
 *   向量系统只看"查询 vs 记忆"的相似度，不看"记忆 vs 回答"的贡献度
 *   好的记忆系统应该像推荐系统一样有 implicit feedback
 *
 * 算法：
 *   1. 回答生成后，计算每条注入记忆与回答的 trigram 重叠度
 *   2. 高重叠 = 记忆被有效使用 → positive feedback → 强化 AAM 关联
 *   3. 零重叠 = 记忆无用 → negative feedback → 弱化 AAM 关联
 *   4. 用户后续回复的情绪/长度 → engagement signal
 *   5. 综合评分写入 memory.injectionEngagement/injectionMiss
 */

import type { Memory } from './types.ts'
import { trigrams, trigramSimilarity, tokenize } from './memory-utils.ts'

interface AffinityResult {
  memory: Memory
  affinity: number      // 0-1, how much this memory contributed
  signal: 'used' | 'partial' | 'unused'
}

/**
 * Score how well injected memories contributed to the response
 * Call this after response generation
 */
export function scoreAffinity(
  injectedMemories: Memory[],
  response: string,
  query: string,
): AffinityResult[] {
  if (!response || injectedMemories.length === 0) return []

  const responseLower = response.toLowerCase()
  const results: AffinityResult[] = []

  for (const mem of injectedMemories) {
    const content = (mem.content || '').toLowerCase()
    if (!content) continue

    // Method 1: Trigram similarity (structural overlap)
    const triSim = trigramSimilarity(trigrams(content), trigrams(responseLower))

    // Method 2: Keyword overlap (semantic contribution)
    const memWords = new Set(tokenize(content).filter(w => w.length >= 2))
    const respWords = new Set(tokenize(responseLower).filter(w => w.length >= 2))
    let keywordOverlap = 0
    for (const w of memWords) {
      if (respWords.has(w)) keywordOverlap++
    }
    const kwScore = memWords.size > 0 ? keywordOverlap / memWords.size : 0

    // Method 3: Entity transfer (did named entities from memory appear in response?)
    const entities = content.match(/[A-Z][a-zA-Z]+|[\u4e00-\u9fff]{2,4}/g) || []
    let entityHits = 0
    for (const e of entities) {
      if (responseLower.includes(e.toLowerCase())) entityHits++
    }
    const entityScore = entities.length > 0 ? entityHits / entities.length : 0

    // Weighted combination
    const affinity = triSim * 0.3 + kwScore * 0.4 + entityScore * 0.3

    let signal: AffinityResult['signal'] = 'unused'
    if (affinity > 0.15) signal = 'used'
    else if (affinity > 0.05) signal = 'partial'

    results.push({ memory: mem, affinity, signal })
  }

  return results
}

/**
 * Apply affinity feedback to memories
 * Updates injectionEngagement/injectionMiss counters
 */
export function applyAffinityFeedback(results: AffinityResult[]): void {
  for (const r of results) {
    if (r.signal === 'used') {
      r.memory.injectionEngagement = (r.memory.injectionEngagement || 0) + 1
    } else if (r.signal === 'unused') {
      r.memory.injectionMiss = (r.memory.injectionMiss || 0) + 1
    }
  }
}

/**
 * Score user engagement with the response
 * Call this when the user sends their next message
 * Returns engagement level based on response characteristics
 */
export function scoreEngagement(
  userReply: string,
  previousResponse: string,
): number {
  if (!userReply) return 0

  let engagement = 0.5  // neutral baseline

  // Length ratio: longer reply = more engaged
  const lenRatio = userReply.length / Math.max(1, previousResponse.length)
  if (lenRatio > 0.5) engagement += 0.15
  if (lenRatio > 1.0) engagement += 0.1

  // Follow-up questions = engaged
  if (/[？?]/.test(userReply)) engagement += 0.1

  // Positive signals
  if (/谢|感谢|棒|好的|对|没错|exactly|thanks|great|yes|right|correct/i.test(userReply)) engagement += 0.15

  // Negative signals
  if (/不对|错了|不是|wrong|no|incorrect/i.test(userReply)) engagement -= 0.2

  // Very short dismissive reply = disengaged
  if (userReply.length < 5 && /嗯|哦|ok|mm|hm/i.test(userReply)) engagement -= 0.15

  return Math.max(0, Math.min(1, engagement))
}

/**
 * Get memory injection effectiveness ratio
 * Used for self-monitoring and optimization decisions
 */
export function getInjectionEffectiveness(memories: Memory[]): {
  totalInjections: number
  engagedCount: number
  missCount: number
  effectivenessRate: number
} {
  let totalInjections = 0, engagedCount = 0, missCount = 0
  for (const mem of memories) {
    const eng = mem.injectionEngagement || 0
    const miss = mem.injectionMiss || 0
    if (eng + miss > 0) {
      totalInjections += eng + miss
      engagedCount += eng
      missCount += miss
    }
  }
  return {
    totalInjections,
    engagedCount,
    missCount,
    effectivenessRate: totalInjections > 0 ? engagedCount / totalInjections : 0,
  }
}
