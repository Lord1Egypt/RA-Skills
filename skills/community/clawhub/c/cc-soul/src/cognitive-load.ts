/**
 * cognitive-load.ts — Cognitive Load Adaptive Injection（认知负荷自适应注入）
 *
 * cc-soul 原创算法。根据对话复杂度动态调整记忆注入量。
 *
 * 解决的问题：
 *   固定 topN=5 在所有场景下都不合适
 *   复杂技术讨论注入太多记忆 → 干扰 LLM 推理
 *   简单闲聊注入太少 → 错失展示对用户了解的机会
 *   向量系统没有这个概念——它们只管 top-K 不管场景
 *
 * 算法：
 *   1. 从消息特征估算认知负荷（0-1）
 *      - 消息长度：长消息 = 高负荷
 *      - 问题复杂度：多个子问题 = 高负荷
 *      - 代码存在：有代码 = 高负荷（留 token 给代码理解）
 *      - 话题数量：多话题 = 高负荷
 *      - 情绪强度：高情绪 = 中等负荷（需要共情空间）
 *   2. 负荷 → 注入策略映射
 *      - 低负荷（闲聊）→ topN=5, budget=2000
 *      - 中负荷（常规问答）→ topN=3, budget=1500
 *      - 高负荷（技术讨论）→ topN=2, budget=800
 *      - 极高负荷（调试/长代码）→ topN=1, budget=400
 */

import type { Memory } from './types.ts'

export interface InjectionStrategy {
  topN: number           // recommended number of memories to recall
  tokenBudget: number    // max tokens for memory injection
  cognitiveLoad: number  // estimated load 0-1
  loadLevel: 'low' | 'medium' | 'high' | 'extreme'
  reason: string         // brief explanation
}

/**
 * Estimate cognitive load and return injection strategy
 */
export function getInjectionStrategy(
  msg: string,
  recentMessages?: string[],  // last 3-5 messages for context
  emotionIntensity?: number,
): InjectionStrategy {
  let load = 0
  const reasons: string[] = []

  // Factor 1: Message length (normalized, caps at 500 chars)
  const lenFactor = Math.min(1, msg.length / 500) * 0.2
  load += lenFactor
  if (msg.length > 300) reasons.push('long message')

  // Factor 2: Question complexity (count question marks and sub-questions)
  const questions = (msg.match(/[？?]/g) || []).length
  const subQuestions = (msg.match(/还有|另外|以及|还|and also|additionally|besides/gi) || []).length
  const qFactor = Math.min(1, (questions + subQuestions) / 3) * 0.2
  load += qFactor
  if (questions > 1) reasons.push(`${questions} questions`)

  // Factor 3: Code presence
  const hasCode = /```|`[^`]+`|function\s|const\s|let\s|var\s|import\s|class\s|def\s|if\s*\(/.test(msg)
  if (hasCode) {
    load += 0.25
    reasons.push('code detected')
  }

  // Factor 4: Topic count (rough estimate from keyword diversity)
  const topicWords = new Set(
    (msg.match(/[\u4e00-\u9fff]{2,4}|[a-zA-Z]{4,}/gi) || [])
      .map(w => w.toLowerCase())
  )
  const topicFactor = Math.min(1, topicWords.size / 15) * 0.15
  load += topicFactor
  if (topicWords.size > 10) reasons.push(`${topicWords.size} topics`)

  // Factor 5: Emotion intensity (moderate load — need empathy space)
  if (emotionIntensity && emotionIntensity > 0.5) {
    load += emotionIntensity * 0.1
    reasons.push('emotional')
  }

  // Factor 6: Conversation momentum (many recent long messages = sustained high load)
  if (recentMessages && recentMessages.length >= 3) {
    const avgLen = recentMessages.reduce((s, m) => s + m.length, 0) / recentMessages.length
    if (avgLen > 200) {
      load += 0.1
      reasons.push('sustained complexity')
    }
  }

  // Clamp to [0, 1]
  load = Math.max(0, Math.min(1, load))

  // Map load to strategy
  let topN: number, tokenBudget: number, loadLevel: InjectionStrategy['loadLevel']

  if (load < 0.2) {
    topN = 5; tokenBudget = 2000; loadLevel = 'low'
  } else if (load < 0.45) {
    topN = 3; tokenBudget = 1500; loadLevel = 'medium'
  } else if (load < 0.7) {
    topN = 2; tokenBudget = 800; loadLevel = 'high'
  } else {
    topN = 1; tokenBudget = 400; loadLevel = 'extreme'
  }

  return {
    topN,
    tokenBudget,
    cognitiveLoad: Math.round(load * 100) / 100,
    loadLevel,
    reason: reasons.join(', ') || 'normal conversation',
  }
}

/**
 * Quick check: should we inject memories at all?
 * Some messages don't benefit from memory injection
 */
export function shouldInjectMemories(msg: string): boolean {
  // Skip memory injection for:
  // 1. Very short acknowledgments
  if (msg.length < 5 && /^(ok|好|嗯|哦|行|是|对|恩|mm|hm|yeah|yep|sure|got it)/i.test(msg)) return false
  // 2. Pure code blocks (user pasting code for review)
  if (msg.startsWith('```') && msg.endsWith('```') && msg.split('\n').length > 10) return false
  // 3. System/bot commands
  if (/^[!/]/.test(msg.trim())) return false
  return true
}

/**
 * Trim memories to fit within token budget
 * Prioritizes shorter, more relevant memories
 */
export function trimToTokenBudget(memories: Memory[], tokenBudget: number): Memory[] {
  // Rough token estimate: 1 CJK char ≈ 1.5 tokens, 1 English word ≈ 1.3 tokens
  const estimateTokens = (text: string): number => {
    const cjk = (text.match(/[\u4e00-\u9fff]/g) || []).length
    const words = (text.match(/[a-zA-Z]+/g) || []).length
    return cjk * 1.5 + words * 1.3 + 10  // +10 for overhead per memory
  }

  const result: Memory[] = []
  let usedTokens = 0

  for (const mem of memories) {
    const tokens = estimateTokens(mem.content || '')
    if (usedTokens + tokens > tokenBudget) break
    result.push(mem)
    usedTokens += tokens
  }

  return result
}
