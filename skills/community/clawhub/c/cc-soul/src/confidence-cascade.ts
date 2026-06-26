/**
 * confidence-cascade.ts — Memory Confidence Cascade（记忆置信级联）
 *
 * cc-soul 原创算法。贝叶斯记忆置信度建模。
 *
 * 解决的问题：
 *   简单的 confidence += 0.02 没有方向性
 *   无法区分"经常被验证"和"刚创建未验证"的记忆
 *   correction 只能一刀切砍 confidence，不知道要砍多少
 *
 * 算法：
 *   1. 每条记忆用 Beta(α, β) 建模置信度
 *   2. 初始 α=2, β=1 → 先验偏乐观 (E=0.67)
 *   3. 正向证据（召回+未被纠正）→ α += Δ（Δ与召回难度成正比）
 *   4. 负向证据（被纠正/矛盾）→ β += Δ（Δ与证据强度成正比）
 *   5. 时间衰减：长期未召回 → β += tiny_amount（遗忘 = 被动失去信任）
 *   6. 输出：confidence = α/(α+β), variance = αβ/((α+β)²(α+β+1))
 *   7. 高 variance = 不确定 → 可能需要验证（提供给 cognition.ts 的 curiosity 引擎）
 */

import type { Memory } from './types.ts'

/**
 * Initialize Beta parameters for a new memory
 */
export function initBeta(mem: Memory): void {
  if (mem.bayesAlpha === undefined) mem.bayesAlpha = 2
  if (mem.bayesBeta === undefined) mem.bayesBeta = 1
}

/**
 * Record positive evidence (memory was recalled and not corrected)
 * @param difficulty 0-1, how hard the recall was (harder recall = stronger evidence)
 */
export function positiveEvidence(mem: Memory, difficulty: number = 0.5): void {
  initBeta(mem)
  // Harder recalls provide stronger evidence (testing effect)
  const delta = 0.3 + difficulty * 0.7  // range: 0.3 - 1.0
  mem.bayesAlpha! += delta
  mem.confidence = betaMean(mem)
}

/**
 * Record negative evidence (memory was corrected or contradicted)
 * @param strength 0-1, how strong the contradiction is
 */
export function negativeEvidence(mem: Memory, strength: number = 0.5): void {
  initBeta(mem)
  const delta = 0.5 + strength * 1.5  // range: 0.5 - 2.0 (corrections hit harder)
  mem.bayesBeta! += delta
  mem.confidence = betaMean(mem)
}

/**
 * Apply time-based decay (call periodically, e.g., daily)
 * Memories not recalled for a long time slowly lose confidence
 */
export function timeDecay(mem: Memory, daysSinceRecall: number): void {
  initBeta(mem)
  if (daysSinceRecall <= 1) return  // no decay within 1 day

  // Logarithmic decay: gentle at first, accelerates with time
  // Max decay: 0.1 per call (prevents cliff-edge drops)
  const decay = Math.min(0.1, Math.log2(daysSinceRecall) * 0.02)
  mem.bayesBeta! += decay
  mem.confidence = betaMean(mem)
}

/**
 * Get the Beta distribution mean (= confidence)
 */
export function betaMean(mem: Memory): number {
  const alpha = mem.bayesAlpha ?? 2
  const beta = mem.bayesBeta ?? 1
  return alpha / (alpha + beta)
}

/**
 * Get the Beta distribution variance (= uncertainty)
 * High variance = we're unsure about this memory
 */
export function betaVariance(mem: Memory): number {
  const a = mem.bayesAlpha ?? 2
  const b = mem.bayesBeta ?? 1
  return (a * b) / ((a + b) ** 2 * (a + b + 1))
}

/**
 * Is this memory uncertain enough to warrant verification?
 * Returns true if variance is high AND confidence isn't extreme
 */
export function needsVerification(mem: Memory): boolean {
  const v = betaVariance(mem)
  const c = betaMean(mem)
  // High variance AND moderate confidence = uncertain
  return v > 0.03 && c > 0.3 && c < 0.8
}

/**
 * Batch update: apply time decay to all memories
 * Call this from heartbeat (hourly or daily)
 */
export function batchTimeDecay(memories: Memory[]): number {
  const now = Date.now()
  let updated = 0
  for (const mem of memories) {
    const lastRecall = mem.lastRecalled || mem.lastAccessed || mem.ts || now
    const daysSince = (now - lastRecall) / 86400000
    if (daysSince > 1) {
      timeDecay(mem, daysSince)
      updated++
    }
  }
  return updated
}

/**
 * Get confidence tier for display/decision-making
 */
export function confidenceTier(mem: Memory): 'verified' | 'probable' | 'uncertain' | 'dubious' {
  const c = betaMean(mem)
  const v = betaVariance(mem)
  if (c >= 0.85 && v < 0.02) return 'verified'
  if (c >= 0.6) return 'probable'
  if (c >= 0.4) return 'uncertain'
  return 'dubious'
}

/**
 * Calculate recall weight modifier based on confidence
 * High confidence memories get boosted, low confidence get penalized
 * But uncertain memories get a slight boost (curiosity-driven recall)
 */
export function confidenceRecallModifier(mem: Memory): number {
  const c = betaMean(mem)
  const v = betaVariance(mem)

  // Base modifier from confidence
  let modifier = 0.5 + c * 0.5  // range: 0.5 - 1.0

  // Curiosity bonus: uncertain memories get a small boost
  // (we want to recall them to gather more evidence)
  if (v > 0.03 && c > 0.3) {
    modifier += 0.1
  }

  return Math.max(0.3, Math.min(1.3, modifier))
}
