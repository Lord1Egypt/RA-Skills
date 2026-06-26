/**
 * metacognition.ts — Adaptive Cognitive Arbitration Engine
 *
 * Self-adaptive augment conflict detection, interaction quality tracking,
 * and cascading conflict resolution with learned conflict pairs.
 *
 * Upgrades from static opposition list to a learning system that discovers
 * conflict patterns from correction history while preserving backward compat.
 */

import { resolve } from 'path'
import type { SoulModule } from './brain.ts'
import { DATA_DIR, loadJson, debouncedSave } from './persistence.ts'

// ═══════════════════════════════════════════════════════════════════════════════
// TYPES
// ═══════════════════════════════════════════════════════════════════════════════

interface ConflictPair {
  a: string
  b: string
  source: 'seed' | 'learned'
  coOccurrences: number
  correctionCount: number
  /** correctionCount / coOccurrences — auto-computed (legacy, kept for compat) */
  correctionRate: number
  /** EWMA: 最近 20 次 co-occurrence 的 0/1 序列 */
  recentCorrections?: number[]
}

interface AugmentInteraction {
  pairKey: string
  coOccurrences: number
  qualitySum: number
  avgQuality: number
  correctionCount: number
}

interface MetacognitionData {
  conflictPairs: ConflictPair[]
  interactions: AugmentInteraction[]
}

interface ConflictResolution {
  demote: string
  reason: string
}

// ═══════════════════════════════════════════════════════════════════════════════
// PRIORITY HIERARCHY — for cascading conflict resolution
// ═══════════════════════════════════════════════════════════════════════════════

/** Lower index = higher authority. When two augments conflict, the lower-priority one gets demoted. */
const PRIORITY_TIERS: string[][] = [
  ['规则', '注意规则', '纠正'],                         // Tier 0: rules
  ['计划', '行动计划', '策略'],                          // Tier 1: plans
  ['知识边界', '不擅长', '擅长领域', '确定性'],           // Tier 2: epistemic
  ['记忆', '相关记忆', '确定性知识', '历史'],             // Tier 3: memory
]

function getTier(text: string): number {
  const lower = text.toLowerCase()
  for (let i = 0; i < PRIORITY_TIERS.length; i++) {
    if (PRIORITY_TIERS[i].some(kw => lower.includes(kw))) return i
  }
  return PRIORITY_TIERS.length // default tier (lowest)
}

// ═══════════════════════════════════════════════════════════════════════════════
// STATE
// ═══════════════════════════════════════════════════════════════════════════════

const META_PATH = resolve(DATA_DIR, 'metacognition.json')
const MAX_CONFLICT_PAIRS = 50
const MAX_INTERACTIONS = 100
const LEARNED_CONFLICT_THRESHOLD = 0.3
const LEARNED_CONFLICT_MIN_SAMPLES = 5

const SEED_PAIRS: [string, string][] = [
  ['简洁', '详细'],
  ['简短', '展开'],
  ['不擅长', '擅长'],
  ['不确定', '确定'],
  ['谨慎', '果断'],
  ['先共情', '直接给方案'],
]

let data: MetacognitionData = { conflictPairs: [], interactions: [] }
let lastAugmentSnapshot: string[] = []
let initialized = false

// ═══════════════════════════════════════════════════════════════════════════════
// INIT / PERSISTENCE
// ═══════════════════════════════════════════════════════════════════════════════

export function loadMetacognition(): void {
  const saved = loadJson<MetacognitionData>(META_PATH, { conflictPairs: [], interactions: [] })
  data = saved

  // Ensure seed pairs exist
  for (const [a, b] of SEED_PAIRS) {
    const key = pairKey(a, b)
    const exists = data.conflictPairs.some(p => pairKey(p.a, p.b) === key)
    if (!exists) {
      data.conflictPairs.push({
        a, b,
        source: 'seed',
        coOccurrences: 0,
        correctionCount: 0,
        correctionRate: 0,
      })
    }
  }

  initialized = true
  console.log(`[cc-soul][metacognition] loaded: ${data.conflictPairs.length} conflict pairs, ${data.interactions.length} interactions`)
}

function ensureInit(): void {
  if (!initialized) loadMetacognition()
}

function persist(): void {
  debouncedSave(META_PATH, data)
}

// ═══════════════════════════════════════════════════════════════════════════════
// HELPERS
// ═══════════════════════════════════════════════════════════════════════════════

function pairKey(a: string, b: string): string {
  return [a, b].sort().join('::')
}

/**
 * EWMA 纠正率：最近的纠正权重更大，老的逐渐失效
 * 替代简单频率 correctionCount / coOccurrences
 */
function ewmaCorrectionRate(pair: ConflictPair): number {
  if (!pair.recentCorrections || pair.recentCorrections.length === 0) {
    // 回退到简单频率（兼容旧数据）
    return pair.coOccurrences > 0 ? pair.correctionCount / pair.coOccurrences : 0
  }
  const alpha = 0.15  // EWMA 系数
  let ewma = 0.5  // 先验
  for (const wasCorrection of pair.recentCorrections) {
    ewma = alpha * (wasCorrection ? 1 : 0) + (1 - alpha) * ewma
  }
  return ewma
}

/** Extract a rough "type tag" from augment content for interaction tracking */
function extractType(content: string): string {
  // Try to match bracketed tags like [相关记忆], [注意规则], etc.
  const match = content.match(/\[([^\]]{2,12})\]/)
  if (match) return match[1]
  // Fallback: first 6 chars of content
  return content.slice(0, 6).replace(/\s+/g, '')
}

/** Generate all unique pairs from a list */
function allPairs<T>(items: T[]): [T, T][] {
  const result: [T, T][] = []
  for (let i = 0; i < items.length; i++) {
    for (let j = i + 1; j < items.length; j++) {
      result.push([items[i], items[j]])
    }
  }
  return result
}

// ═══════════════════════════════════════════════════════════════════════════════
// 1. DYNAMIC CONFLICT LEARNING
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Learn conflict patterns from correction events.
 * Call this after a user correction with the augment types that were active.
 * When a pair's correction rate exceeds 30% (min 5 samples), it auto-promotes to conflict.
 */
export function learnConflict(augmentsUsed: string[], wasCorrected: boolean): void {
  ensureInit()
  if (augmentsUsed.length < 2) return

  const types = augmentsUsed.map(extractType)
  const pairs = allPairs(types)

  for (const [a, b] of pairs) {
    const key = pairKey(a, b)
    let existing = data.conflictPairs.find(p => pairKey(p.a, p.b) === key)

    if (!existing) {
      // Create candidate entry (not yet a confirmed conflict — tracked for stats)
      existing = {
        a, b,
        source: 'learned',
        coOccurrences: 0,
        correctionCount: 0,
        correctionRate: 0,
      }
      data.conflictPairs.push(existing)
    }

    existing.coOccurrences++
    if (wasCorrected) existing.correctionCount++

    // EWMA 序列追踪
    if (!existing.recentCorrections) existing.recentCorrections = []
    existing.recentCorrections.push(wasCorrected ? 1 : 0)
    if (existing.recentCorrections.length > 20) existing.recentCorrections.shift()

    // 更新 correctionRate（使用 EWMA，兼容旧字段）
    existing.correctionRate = ewmaCorrectionRate(existing)
  }

  // Trim to max
  trimConflictPairs()
  persist()
}

function trimConflictPairs(): void {
  if (data.conflictPairs.length <= MAX_CONFLICT_PAIRS) return
  // Keep seeds first, then sort learned by correctionCount desc
  const seeds = data.conflictPairs.filter(p => p.source === 'seed')
  const learned = data.conflictPairs
    .filter(p => p.source === 'learned')
    .sort((a, b) => b.correctionCount - a.correctionCount)
  data.conflictPairs = [...seeds, ...learned].slice(0, MAX_CONFLICT_PAIRS)
}

/** Get active conflict pairs (seeds + learned that meet threshold) */
function getActiveConflicts(): ConflictPair[] {
  ensureInit()
  return data.conflictPairs.filter(p =>
    p.source === 'seed' ||
    (ewmaCorrectionRate(p) >= LEARNED_CONFLICT_THRESHOLD && p.coOccurrences >= LEARNED_CONFLICT_MIN_SAMPLES)
  )
}

// ═══════════════════════════════════════════════════════════════════════════════
// 2. AUGMENT INTERACTION MATRIX
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Record quality of augment combination after a response.
 * quality: 0-1 score (1 = perfect, 0 = fully corrected)
 */
export function recordInteraction(augmentTypes: string[], quality: number, wasCorrected: boolean): void {
  ensureInit()
  if (augmentTypes.length < 2) return

  const types = augmentTypes.map(extractType)
  const pairs = allPairs(types)

  for (const [a, b] of pairs) {
    const key = pairKey(a, b)
    let entry = data.interactions.find(i => i.pairKey === key)

    if (!entry) {
      entry = { pairKey: key, coOccurrences: 0, qualitySum: 0, avgQuality: 0, correctionCount: 0 }
      data.interactions.push(entry)
    }

    entry.coOccurrences++
    entry.qualitySum += quality
    entry.avgQuality = entry.qualitySum / entry.coOccurrences
    if (wasCorrected) entry.correctionCount++
  }

  // Trim: keep top 100 by coOccurrences
  if (data.interactions.length > MAX_INTERACTIONS) {
    data.interactions.sort((a, b) => b.coOccurrences - a.coOccurrences)
    data.interactions = data.interactions.slice(0, MAX_INTERACTIONS)
  }

  persist()
}

/**
 * Return a human-readable insight about augment synergies and anti-synergies.
 */
export function getInteractionInsight(): string {
  ensureInit()
  if (data.interactions.length === 0) return ''

  const MIN_SAMPLES = 3
  const qualified = data.interactions.filter(i => i.coOccurrences >= MIN_SAMPLES)
  if (qualified.length === 0) return ''

  const sorted = [...qualified].sort((a, b) => a.avgQuality - b.avgQuality)

  const lines: string[] = []

  // Worst combos (anti-synergy)
  const worst = sorted.filter(i => i.avgQuality < 0.5).slice(0, 3)
  if (worst.length > 0) {
    lines.push('减效组合: ' + worst.map(i =>
      `${i.pairKey.replace('::', '+')}(质量${(i.avgQuality * 100).toFixed(0)}%, n=${i.coOccurrences})`
    ).join('，'))
  }

  // Best combos (synergy)
  const best = sorted.filter(i => i.avgQuality >= 0.7).slice(-3).reverse()
  if (best.length > 0) {
    lines.push('增效组合: ' + best.map(i =>
      `${i.pairKey.replace('::', '+')}(质量${(i.avgQuality * 100).toFixed(0)}%, n=${i.coOccurrences})`
    ).join('，'))
  }

  return lines.length > 0 ? `[交互矩阵] ${lines.join('；')}` : ''
}

// ═══════════════════════════════════════════════════════════════════════════════
// 3. CASCADING CONFLICT RESOLUTION
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Core conflict check — backward compatible.
 * Returns warning string (empty if no conflict), now enriched with arbitration advice.
 */
export function checkAugmentConsistency(augments: { content: string; priority: number }[]): string {
  ensureInit()
  if (augments.length < 2) return ''

  const issues: string[] = []
  const texts = augments.map(a => a.content.toLowerCase())
  const activeConflicts = getActiveConflicts()

  // Check all active conflict pairs (seeds + learned)
  for (const pair of activeConflicts) {
    const hasA = texts.some(t => t.includes(pair.a))
    const hasB = texts.some(t => t.includes(pair.b))
    if (hasA && hasB) {
      const suffix = pair.source === 'learned'
        ? `(学习发现, 纠正率${(pair.correctionRate * 100).toFixed(0)}%)`
        : ''
      issues.push(`"${pair.a}" vs "${pair.b}"${suffix}`)
    }
  }

  // Plan contradicting knowledge boundary (preserved from original)
  const hasPlanSayDontKnow = texts.some(t => t.includes('不擅长') || t.includes('说不确定'))
  const hasHighConfidence = texts.some(t => t.includes('擅长领域') || t.includes('高信心'))
  if (hasPlanSayDontKnow && hasHighConfidence) {
    issues.push('计划说"不擅长"但知识边界说"高信心"——以最新计划为准')
  }

  // Memory vs correction overlap check (preserved from original)
  const memoryTexts = texts.filter(t => t.includes('[相关记忆]') || t.includes('[确定性知识]'))
  const correctionTexts = texts.filter(t => t.includes('[注意规则]') || t.includes('[行动计划'))
  if (memoryTexts.length > 0 && correctionTexts.length > 0) {
    for (const mem of memoryTexts) {
      for (const corr of correctionTexts) {
        const memWords = new Set(mem.match(/[\u4e00-\u9fff]{2,}/g) || [])
        const corrWords = new Set(corr.match(/[\u4e00-\u9fff]{2,}/g) || [])
        const overlap = [...memWords].filter(w => corrWords.has(w)).length
        if (overlap >= 3) {
          issues.push('记忆和规则可能涉及同一话题——以规则/计划为准')
          break
        }
      }
    }
  }

  if (issues.length === 0) return ''

  // Enrich with arbitration summary
  const resolutions = getConflictResolutions(augments)
  const resText = resolutions.length > 0
    ? ` 仲裁建议: ${resolutions.map(r => `降权"${r.demote}"(${r.reason})`).join('；')}`
    : ''

  return `[元认知警告] 注入上下文有潜在冲突: ${issues.join('；')}。请以最新信息和规则为准。${resText}`
}

/**
 * Return specific demotion recommendations for conflicting augments.
 * Uses priority hierarchy: 规则 > 计划 > 知识边界 > 记忆 > 默认
 */
export function getConflictResolutions(augments: { content: string; priority: number }[]): ConflictResolution[] {
  ensureInit()
  if (augments.length < 2) return []

  const resolutions: ConflictResolution[] = []
  const activeConflicts = getActiveConflicts()

  for (const pair of activeConflicts) {
    // Find augments matching each side
    const matchA = augments.filter(a => a.content.toLowerCase().includes(pair.a))
    const matchB = augments.filter(a => a.content.toLowerCase().includes(pair.b))

    if (matchA.length === 0 || matchB.length === 0) continue

    // Compare tiers — pick one representative from each side
    for (const augA of matchA) {
      for (const augB of matchB) {
        const tierA = getTier(augA.content)
        const tierB = getTier(augB.content)

        if (tierA === tierB) {
          // Same tier: demote the one with lower numeric priority
          const loser = augA.priority >= augB.priority ? augB : augA
          const loserKeyword = loser === augA ? pair.a : pair.b
          resolutions.push({
            demote: loserKeyword,
            reason: `同层冲突，优先级较低(${loser.priority})`,
          })
        } else if (tierA < tierB) {
          // A has higher authority, demote B
          resolutions.push({
            demote: pair.b,
            reason: `${PRIORITY_TIERS[tierA]?.[0] || '高层'}优先于${PRIORITY_TIERS[tierB]?.[0] || '低层'}`,
          })
        } else {
          // B has higher authority, demote A
          resolutions.push({
            demote: pair.a,
            reason: `${PRIORITY_TIERS[tierB]?.[0] || '高层'}优先于${PRIORITY_TIERS[tierA]?.[0] || '低层'}`,
          })
        }
      }
    }
  }

  // Deduplicate by demote target
  const seen = new Set<string>()
  return resolutions.filter(r => {
    if (seen.has(r.demote)) return false
    seen.add(r.demote)
    return true
  })
}

// ═══════════════════════════════════════════════════════════════════════════════
// SNAPSHOT (backward compat)
// ═══════════════════════════════════════════════════════════════════════════════

export function snapshotAugments(augmentContents: string[]): void {
  lastAugmentSnapshot = [...augmentContents]
}

export function getLastAugmentSnapshot(): string[] {
  return lastAugmentSnapshot
}

// ── SoulModule ──
export const metacognitionModule: SoulModule = {
  id: 'metacognition',
  name: '认知仲裁引擎',
  priority: 50,
  features: ['metacognition'],
  init() { loadMetacognition() },
}
