import { resolve } from 'path'
import { existsSync, writeFileSync } from 'fs'
import type { SoulModule } from './brain.ts'
import { getParam } from './auto-tune.ts'
import { trigrams, trigramSimilarity, detectPolarityFlip, WORD_PATTERN, TRIGRAM_THRESHOLD } from './memory-utils.ts'
import { DATA_DIR, loadJson, debouncedSave } from './persistence.ts'
import { logDecision } from './decision-log.ts'
import { emitCacheEvent } from './memory-utils.ts'

/**
 * smart-forget.ts — Intelligent Memory Forgetting (Weibull + ACT-R)
 *
 * Combines two cognitive models to decide which memories should be forgotten:
 *
 * 1. Weibull survival model — age-based decay with shape k=1.5, scope-dependent
 *    scale lambda. Survival probability: S(t) = exp(-(t/λ)^k)
 *
 * 2. ACT-R base-level activation — B = ln(Σ t_i^(-d)), where t_i are time
 *    intervals since each access, d=0.5. Models memory strengthening via
 *    repeated retrieval.
 *
 * Decision rule:
 *   - Forget when: survival < 0.1 AND activation < -1.0
 *   - Consolidate when: survival > 0.8 AND activation > 2.0
 *
 * This module is read-only: it never mutates memory data, only returns
 * suggestions (indices to forget / consolidate).
 *
 * Exported API:
 *   computeForgetScore(mem) → 0-1 forget probability
 *   smartForgetSweep(memories) → { toForget, toConsolidate }
 *   smartForgetModule — SoulModule for brain.ts
 */

// ═══════════════════════════════════════════════════════════════════════════════
// FSRS-4.5 — Free Spaced Repetition Scheduler (replaces Weibull for new memories)
// Paper: https://arxiv.org/abs/2402.07345
// ═══════════════════════════════════════════════════════════════════════════════

export interface FSRSState {
  stability: number    // 记忆稳定度（天数）— 90% 检索概率对应的间隔
  difficulty: number   // 记忆难度 0-1 — 越难越容易忘
  reps: number         // 复习/召回次数
  lapses: number       // 遗忘次数
}

/** FSRS-7 default weights (extended from FSRS-4.5 with w[17] same-day review discount, w[18] curve shape) */
const FSRS_W = [0.4, 0.6, 2.4, 5.8, 4.93, 0.94, 0.86, 0.01, 1.49, 0.14, 0.94, 2.18, 0.05, 0.34, 1.26, 0.29, 2.61, 0.12, 0.1]

/** Retrievability: probability of recall after elapsedDays, given stability S.
 *  R(t,S) = (1 + t/(9·S))^(-1)  — power-law decay, not exponential. */
export function fsrsRetrievability(elapsedDays: number, stability: number): number {
  if (stability <= 0 || !isFinite(stability)) return 1.0
  if (elapsedDays <= 0) return 1.0
  return Math.pow(1 + elapsedDays / (9 * stability), -1)
}

/** Update FSRS state after a recall event.
 *  rating: 1=again(forgot), 2=hard, 3=good, 4=easy */
export function fsrsUpdate(state: FSRSState, rating: 1 | 2 | 3 | 4, elapsedDays: number): FSRSState {
  const s = { ...state }
  const r = fsrsRetrievability(elapsedDays, s.stability)

  if (rating >= 3) {
    // Successful recall → stability grows
    const growthFactor = 1 + Math.exp(FSRS_W[8]) * (11 - s.difficulty * 10) *
      Math.pow(s.stability, -FSRS_W[9]) *
      (Math.exp((1 - r) * FSRS_W[10]) - 1)
    s.stability = Math.max(0.1, s.stability * growthFactor)
    s.reps++
    // Difficulty eases slightly on successful recall
    s.difficulty = Math.max(0, Math.min(1, s.difficulty - 0.02 * (rating - 2)))
  } else {
    // Failed recall / hard → stability shrinks
    s.stability = Math.max(0.1, s.stability * Math.pow(FSRS_W[11], s.difficulty * 10 - 1))
    s.lapses++
    s.reps++
    // Difficulty increases on failure
    s.difficulty = Math.max(0, Math.min(1, s.difficulty + 0.1 * (2 - rating)))
  }

  // Accumulate training data for personalization
  try {
    const { dbAddFSRSTraining } = require('./sqlite-store.ts')
    dbAddFSRSTraining(elapsedDays, state.stability, rating >= 3)
  } catch {}

  return s
}

/** Create initial FSRS state for a new memory */
export function fsrsInit(scope?: string): FSRSState {
  // scope-based initial difficulty: corrections are "easy" (never forget), episodes are harder
  const difficultyMap: Record<string, number> = {
    correction: 0.1, fact: 0.3, preference: 0.25, episode: 0.4, emotion: 0.5,
  }
  return {
    stability: scope === 'correction' ? 365 : 1.0,  // 1 day initial stability (corrections: 1 year)
    difficulty: difficultyMap[scope || 'fact'] ?? 0.3,
    reps: 0,
    lapses: 0,
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// BCM 元可塑性 (Metaplasticity) — 动态遗忘阈值
// Bienenstock-Cooper-Munro (1982)：突触可塑性阈值随整体活动水平滑动
// 活跃度高（用户频繁交互）→ 阈值升高 → 只有重要记忆才保留
// 活跃度低（用户不活跃）→ 阈值降低 → 更多记忆被保留（因为每条都珍贵）
// ═══════════════════════════════════════════════════════════════════════════════

function bcmAdaptiveThreshold(
  baseThreshold: number,
  recentActivityLevel: number  // 最近的消息频率，归一化到 [0, 1]
): number {
  // BCM 滑动阈值：θ = θ_base × (1 + α × (activity - mean_activity))
  // activity > mean → 阈值升高；activity < mean → 阈值降低
  const meanActivity = 0.3  // 基线活跃度（每天约 10 条消息）
  const alpha = 0.5  // 调节灵敏度
  const shift = alpha * (recentActivityLevel - meanActivity)
  return Math.max(0.05, Math.min(0.3, baseThreshold + shift))
}

// ═══════════════════════════════════════════════════════════════════════════════
// TYPES
// ═══════════════════════════════════════════════════════════════════════════════

export interface MemoryInput {
  ts: number
  recallCount: number
  lastAccessed: number
  scope: string
  confidence?: number
  fsrs?: FSRSState
  // 扩展字段（减少 as any 强转）
  content?: string
  bayesAlpha?: number
  bayesBeta?: number
  network?: 'world' | 'experience' | 'opinion' | 'entity'
  emotionIntensity?: number
  importance?: number
  surprise?: number
  reasoning?: { context: string; conclusion: string; confidence: number }
  because?: string
  emotion?: string
  userId?: string
  injectionEngagement?: number
  injectionMiss?: number
  prospective?: { trigger: string; expiresAt: number; action: string }
}

interface SweepResult {
  /** Indices of memories recommended for forgetting */
  toForget: number[]
  /** Indices of memories recommended for consolidation */
  toConsolidate: number[]
}

interface ForgetStats {
  lastSweepTs: number
  lastSweepForget: number
  lastSweepConsolidate: number
  totalSweeps: number
}

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTS
// ═══════════════════════════════════════════════════════════════════════════════

const MS_PER_DAY = 86400000

/** Weibull shape parameter — per-scope, read from tunable params (auto-tune.ts) */
const WEIBULL_K_DEFAULT: Record<string, number> = {
  fact: 1.2,
  preference: 0.9,
  episode: 1.4,
  correction: Infinity,  // corrections never decay
}

/** Get Weibull k for a scope (learnable EMA → tunable params → hardcoded defaults) */
export function getWeibullK(scope?: string): number {
  const s = scope || 'fact'
  // Check learned EMA params first
  if (_decayParams.scopeK && _decayParams.scopeK[s] !== undefined) return _decayParams.scopeK[s]
  // Then tunable params
  const paramKey = `forget.weibull_k_${s}`
  const tuned = getParam(paramKey)
  if (tuned > 0) return tuned
  return WEIBULL_K_DEFAULT[s] ?? getParam('forget.weibull_k_fact')
}

/** Backward-compatible constant (uses 'fact' default) */
export const WEIBULL_K = 1.2

/** Weibull scale (lambda) in days, by scope — now reads from tunable params */
function getWeibullLambda(scope: string): number {
  if (scope === 'correction') return Infinity
  const paramKey = `forget.weibull_lambda_${scope}`
  const tuned = getParam(paramKey)
  if (tuned > 0) return tuned
  // Fallback for scopes without dedicated param (e.g. emotion)
  const LEGACY_LAMBDA: Record<string, number> = { emotion: 7 }
  return LEGACY_LAMBDA[scope] ?? getParam('forget.weibull_lambda_fact')
}

/** ACT-R decay exponent — tunable */
function getActRDecay(): number { return getParam('forget.act_r_decay') }

/** Forget thresholds — tunable */
function getSurvivalForgetThreshold(): number { return getParam('forget.survival_threshold') }
function getActivationForgetThreshold(): number { return getParam('forget.activation_threshold') }

/** Consolidation thresholds — tunable */
function getSurvivalConsolidateThreshold(): number { return getParam('forget.consolidation_threshold_survival') }
function getActivationConsolidateThreshold(): number { return getParam('forget.consolidation_threshold_activation') }

// ═══════════════════════════════════════════════════════════════════════════════
// ADAPTIVE DECAY — learn lambda multiplier from recall hit/miss feedback
// ═══════════════════════════════════════════════════════════════════════════════

interface DecayParams {
  recallHits: number
  recallMisses: number
  lambdaMultiplier: number
  lastAdjustTs: number
  /** Per-scope learnable Weibull k values */
  scopeK?: Record<string, number>
}

const DECAY_PARAMS_FILENAME = 'decay_params.json'

let _decayParams: DecayParams = { recallHits: 0, recallMisses: 0, lambdaMultiplier: 1.0, lastAdjustTs: 0 }
let _decayParamsPath = ''

function loadDecayParams(dataDir: string) {
  _decayParamsPath = resolve(dataDir, DECAY_PARAMS_FILENAME)
  // 优先 SQLite
  try {
    const sqlMod = require('./sqlite-store.ts')
    if (sqlMod?.dbLoadDecayParams) {
      const loaded = sqlMod.dbLoadDecayParams(null)
      if (loaded) { Object.assign(_decayParams, loaded); return }
    }
  } catch {}
  // JSON fallback
  try {
    const loaded = loadJson(_decayParamsPath, null)
    if (loaded) Object.assign(_decayParams, loaded)
  } catch {}
}

function saveDecayParams() {
  // SQLite 主存储
  try {
    const sqlMod = require('./sqlite-store.ts')
    if (sqlMod?.dbSaveDecayParams) sqlMod.dbSaveDecayParams(_decayParams)
  } catch {}
  // JSON 双写已移除——SQLite 是唯一数据源
}

/** EMA alpha for adaptive lambda adjustment — now reads from auto-tune */
function getEMAAlpha(): number { return getParam('forget.ema_alpha') }

/** Clamp lambda multiplier to [0.5, 2.0] range */
function clampMultiplier(v: number): number { return Math.max(0.5, Math.min(2.0, v)) }

/** Record a recall hit (user later referenced the recalled memory) */
export function recordRecallHit(scope?: string, mem?: any) {
  _decayParams.recallHits++
  // EMA: nudge lambda multiplier toward 1.05 on hit (memory was useful → slow decay)
  _decayParams.lambdaMultiplier = clampMultiplier(
    _decayParams.lambdaMultiplier * (1 - getEMAAlpha()) + 1.05 * getEMAAlpha()
  )
  // EMA: nudge k downward on hit (lower k → flatter hazard → slower forget)
  if (scope && _decayParams.scopeK && _decayParams.scopeK[scope] !== undefined) {
    const kTarget = (WEIBULL_K_DEFAULT[scope] ?? 1.2) * 0.97  // target: 3% lower than default
    _decayParams.scopeK[scope] = _decayParams.scopeK[scope] * (1 - getEMAAlpha()) + kTarget * getEMAAlpha()
  }
  _decayParams.lastAdjustTs = Date.now()
  saveDecayParams()

}

/** Record a recall miss (recalled memory was ignored by user) */
export function recordRecallMiss(scope?: string, mem?: any) {
  _decayParams.recallMisses++
  // EMA: nudge lambda multiplier toward 0.95 on miss (memory was useless → faster decay)
  _decayParams.lambdaMultiplier = clampMultiplier(
    _decayParams.lambdaMultiplier * (1 - getEMAAlpha()) + 0.95 * getEMAAlpha()
  )
  // EMA: nudge k upward on miss (higher k → steeper hazard → faster forget)
  if (scope && _decayParams.scopeK && _decayParams.scopeK[scope] !== undefined) {
    const kDefault = WEIBULL_K_DEFAULT[scope] ?? 1.2
    _decayParams.scopeK[scope] = _decayParams.scopeK[scope] * (1 - getEMAAlpha()) + (kDefault * 1.03) * getEMAAlpha()
  }
  _decayParams.lastAdjustTs = Date.now()
  saveDecayParams()

}

/** Get current adaptive lambda multiplier */
export function getLambdaMultiplier(): number {
  return _decayParams.lambdaMultiplier
}

// ═══════════════════════════════════════════════════════════════════════════════
// WEIBULL SURVIVAL MODEL
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Weibull survival probability: S(t) = exp(-(t/λ)^k)
 *
 * @param ageDays — age of memory in days
 * @param lambda — scale parameter in days
 * @param k — shape parameter (>1 means increasing hazard)
 * @returns survival probability in [0, 1]
 */
export function weibullSurvival(ageDays: number, lambda: number, k: number): number {
  if (!isFinite(lambda)) return 1.0  // e.g. correction scope → never decays
  if (ageDays <= 0) return 1.0
  if (lambda <= 0) return 0.0
  return Math.exp(-Math.pow(ageDays / lambda, k))
}

/**
 * Get Weibull lambda for a given scope, adjusted by recall count.
 * More recalls → longer effective half-life (up to 3x).
 */
export function effectiveLambda(scope: string, recallCount: number, emotionIntensity?: number): number {
  const baseLambda = getWeibullLambda(scope)
  if (!isFinite(baseLambda)) return Infinity
  // Each recall extends lambda, capped at configurable max
  const recallMultiplier = Math.min(1 + recallCount * getParam('forget.recall_increment_percent') / 100, getParam('forget.lambda_max_multiplier'))
  // 连续情绪-记忆耦合（替代阶梯乘数）
  // λ(ei) = 1 + α × ei^β，其中 α=1.5, β=2.0
  // ei=0 → 1.0（无影响）
  // ei=0.5 → 1.375（轻微延长）
  // ei=0.8 → 1.96（接近2x）
  // ei=1.0 → 2.5（极强记忆）
  const ei = emotionIntensity ?? 0
  const emotionAlpha = 1.5  // 最大增强幅度
  const emotionBeta = 2.0   // 非线性指数（越大越需要高情绪才有效）
  const emotionMultiplier = 1 + emotionAlpha * Math.pow(ei, emotionBeta)
  return baseLambda * recallMultiplier * emotionMultiplier * _decayParams.lambdaMultiplier
}

// ═══════════════════════════════════════════════════════════════════════════════
// ACT-R BASE-LEVEL ACTIVATION
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * ACT-R base-level activation: B = ln(Σ t_i^(-d))
 *
 * We approximate access history by distributing `recallCount` accesses
 * evenly between creation and last access time.
 *
 * @param mem — memory record
 * @param now — current timestamp
 * @returns activation value (higher = more accessible)
 */
function actRActivation(mem: MemoryInput, now: number): number {
  const n = Math.max(mem.recallCount, 1)
  const createdAgo = Math.max((now - mem.ts) / 1000, 1)            // seconds ago
  const lastAgo = Math.max((now - mem.lastAccessed) / 1000, 1)     // seconds ago

  let sum = 0

  if (n === 1) {
    // Single access at lastAccessed time
    sum = Math.pow(lastAgo, -getActRDecay())
  } else {
    // Distribute accesses evenly from creation to lastAccessed (cap at configurable iterations)
    const cap = Math.min(n, getParam('forget.actr_max_iterations'))
    for (let i = 0; i < cap; i++) {
      const fraction = cap === 1 ? 1 : i / (cap - 1)
      const accessAgo = createdAgo - fraction * (createdAgo - lastAgo)
      const t = Math.max(accessAgo, 1)
      sum += Math.pow(t, -getActRDecay())
    }
  }

  return sum > 0 ? Math.log(sum) : -Infinity
}

// ═══════════════════════════════════════════════════════════════════════════════
// PUBLIC API
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Ensure all memories have FSRS state — auto-initialize for legacy memories without fsrs field.
 * Uses scope and age to produce reasonable initial stability/difficulty.
 */
function ensureFSRS(mem: MemoryInput): { stability: number; difficulty: number } {
  if (mem.fsrs) return mem.fsrs
  // 旧记忆：根据 scope 和年龄初始化 FSRS
  const ageDays = (Date.now() - (mem.ts || Date.now())) / MS_PER_DAY
  const scope = mem.scope || 'fact'
  let stability = scope === 'correction' ? 365 : scope === 'preference' ? 60 : scope === 'episode' ? 7 : 30
  let difficulty = scope === 'correction' ? 1 : scope === 'preference' ? 3 : scope === 'episode' ? 7 : 5
  // 根据 recallCount 调整：被多次召回的记忆更稳定
  const recalls = mem.recallCount || 0
  if (recalls > 0) stability *= (1 + recalls * 0.3)
  return { stability, difficulty }
}

// ═══════════════════════════════════════════════════════════════════════════════
// LECTOR 语义干扰 (Proactive Interference)
// 相似记忆越多 → 干扰越强 → stability 折扣
// ═══════════════════════════════════════════════════════════════════════════════

/** Lazy reference to memoryState (avoid circular import at module level) */
let _memoryStateMod: any = null

function semanticInterference(memContent: string): number {
  // Lazy-load memoryState to avoid circular dependency
  if (!_memoryStateMod) {
    try { _memoryStateMod = require('./memory.ts') } catch { return 1.0 }
  }
  const allMems = _memoryStateMod?.memoryState?.memories
  if (!allMems || allMems.length < 5) return 1.0

  const memTri = trigrams(memContent)
  if (memTri.size === 0) return 1.0

  // 语义空间聚集度：不只数个数，还考虑平均相似度 × 聚集密度
  let totalSim = 0
  let count = 0
  let contradictionPenalty = 0
  // A4: build memWords ONCE outside the loop for information gain weighting
  const memWords = new Set((memContent.match(WORD_PATTERN.CJK2_EN3) || []).map((w: string) => w.toLowerCase()))
  // Check last 100 memories for interference
  const recent = allMems.slice(-100)
  for (const other of recent) {
    if (!other || other.scope === 'expired' || other.content === memContent) continue
    const otherTri = trigrams(other.content)
    const sim = trigramSimilarity(memTri, otherTri)
    if (sim < 0.15) continue  // 降低阈值，捕获更多弱关联

    // A4: information gain weighted interference — similar but novel content interferes less
    const otherWords = (other.content.match(WORD_PATTERN.CJK2_EN3) || []).map((w: string) => w.toLowerCase())
    let newWordCount = 0
    for (const w of otherWords) { if (!memWords.has(w)) newWordCount++ }
    const infoGain = otherWords.length > 0 ? newWordCount / otherWords.length : 0
    totalSim += sim * (1 - infoGain * 0.5)
    count++

    // 矛盾记忆额外惩罚
    if (detectPolarityFlip(memContent, other.content)) contradictionPenalty += 0.2
  }

  if (count === 0) return 1.0  // 独特记忆，无干扰

  // 聚集度 = 平均相似度 × log(相似记忆数) → 越聚集干扰越强
  const avgSim = totalSim / count
  const clustering = avgSim * Math.log1p(count) + contradictionPenalty
  return 1 / (1 + clustering * 0.3)
}

// detectContradictionSignals → replaced by detectPolarityFlip from memory-utils.ts

/**
 * @deprecated 使用 decideForget() 替代。此函数保留仅供测试兼容。
 * 新代码应使用领地划分模型（decideForget）而非加权融合。
 *
 * Compute a composite forget score for a single memory.
 *
 * @returns 0-1 probability of forgetting (1 = definitely forget)
 */
export function computeForgetScore(mem: MemoryInput): number {
  const now = Date.now()
  const ageDays = (now - mem.ts) / MS_PER_DAY

  // ── 统一 FSRS 路径：所有记忆（含旧记忆）都走 FSRS ──
  const fsrs = ensureFSRS(mem)
  // LECTOR: 语义干扰折扣 — 相似记忆越多，stability 越低
  const interference = semanticInterference(mem.content || '')
  const effectiveStability = fsrs.stability * interference
  const survival = fsrsRetrievability(ageDays, effectiveStability)

  // ACT-R activation
  const activation = actRActivation(mem, now)

  // Confidence bonus: high confidence memories are harder to forget
  const conf = mem.confidence ?? 0.5
  const confidenceBonus = conf * 0.2  // up to 0.2 survival boost

  // Combine: forget probability = (1 - survival) * sigmoid(-activation)
  // sigmoid maps activation → 0-1 (lower activation → higher forget)
  const sigmoid = 1 / (1 + Math.exp(activation))
  const rawForget = (1 - survival - confidenceBonus) * sigmoid

  // Clamp to [0, 1]
  return Math.max(0, Math.min(1, rawForget))
}

// ═══════════════════════════════════════════════════════════════════════════════
// TERRITORY DIVISION — 模型领地划分
//
// structuralImportance → I(m) ∈ [0.1, ∞)：这条记忆有多重要（缓慢变化）
// contextBinding       → B ∈ [0, 1]：跟当前语境有多相关（快速变化）
// R = I × 0.3 + B × 0.7：综合相关性（保底层 + 动态层）
// Bayes → C ∈ [0,1]：是不是真的
// BCM → θ ∈ [0.05,0.3]：标准多严
// ═══════════════════════════════════════════════════════════════════════════════

export interface ForgetDecision {
  retrievability: number   // R = I×0.3 + B×0.7
  truthfulness: number     // C = α/(α+β)
  threshold: number        // BCM θ
  action: 'keep' | 'demote' | 'verify' | 'graveyard'
  reason: string
}

// ── P5a: structuralImportance — 记忆的固有重要性 ──

/**
 * 计算记忆的结构重要性 I(m)
 * I = graphDegree × emotionWeight × causalDepth × uniqueness
 * 最小值 clamp 到 0.1（防止 graph 为空时 I=0）
 */
export function computeStructuralImportance(mem: any): number {
  let I = 1.0

  // 知识图谱度数：被更多实体关联的记忆更重要
  try {
    const { findMentionedEntities } = require('./graph.ts')
    const entities = findMentionedEntities(mem.content || '')
    I *= (1 + entities.length * 0.3)  // 每个实体 +30%
  } catch {}

  // 情绪权重：高情绪强度的记忆更重要
  const ei = mem.emotionIntensity ?? 0
  I *= (1 + ei * 0.5)  // emotionIntensity=1 → +50%

  // 因果深度：有 reasoning 或 because 的记忆更重要
  if (mem.reasoning) I *= 1.3
  if (mem.because) I *= 1.2

  // 信息增益/独特性：importance/surprise 高的记忆更重要
  const imp = mem.importance ?? mem.surprise ?? 5
  I *= (0.5 + imp / 10)  // importance=10 → ×1.5, importance=1 → ×0.6

  // scope 加权：correction 最重要
  if (mem.scope === 'correction') I *= 2.0
  else if (mem.scope === 'preference' || mem.scope === 'fact') I *= 1.3

  // Hindsight 认知网络加权：不同网络衰减策略不同
  const network = mem.network
  if (network === 'world') I = Math.max(I, 0.5)          // 客观事实不轻易忘
  else if (network === 'experience') I *= 0.8              // 经历衰减较快
  // opinion 不加权（由 Bayes C 值控制）


  return Math.max(0.1, I)  // 最小 0.1，防止 graph 空时完全归零
}

// ── P5a: contextBinding — 语境绑定度 ──

// 每条记忆的 CRD 状态缓存（内存中，不持久化）
const _crdBindings = new Map<string, { bindingStrength: number; lastContextMatch: number }>()

/**
 * 计算记忆的语境绑定度 B
 * 话题匹配 → B 升高，话题不匹配 → B 指数衰减（半衰期 2 小时）
 */
export function computeContextBinding(mem: any, currentTopics: string[]): number {
  const key = (mem.content || '').slice(0, 40) + '|' + mem.ts
  const now = Date.now()

  // OOM protection: evict 2000 weakest bindings when exceeding cap
  if (_crdBindings.size > 5000) {
    const sorted = [..._crdBindings.entries()]
      .sort((a, b) => a[1].bindingStrength - b[1].bindingStrength)
    const toDelete = 2000
    for (let i = 0; i < toDelete; i++) _crdBindings.delete(sorted[i][0])
  }

  if (!_crdBindings.has(key)) {
    _crdBindings.set(key, { bindingStrength: 0.5, lastContextMatch: mem.lastAccessed || mem.ts })
  }
  const state = _crdBindings.get(key)!

  if (currentTopics.length === 0) {
    // 无活跃话题（用户不在线 > 6小时）→ 纯衰减
    const hoursSince = (now - state.lastContextMatch) / 3600000
    state.bindingStrength *= Math.exp(-0.35 * hoursSince)
    return state.bindingStrength
  }

  // 话题匹配：记忆内容与 currentTopics 的关键词重叠
  const memWords = new Set(((mem.content || '').match(WORD_PATTERN.CJK2_EN3) || []).map((w: string) => w.toLowerCase()))
  const topicWords = new Set(currentTopics.flatMap(t => (t.match(WORD_PATTERN.CJK2_EN3) || []).map((w: string) => w.toLowerCase())))

  let overlap = 0
  for (const w of memWords) { if (topicWords.has(w)) overlap++ }
  const overlapRatio = memWords.size > 0 ? overlap / memWords.size : 0

  if (overlapRatio > 0.2) {
    // 话题匹配 → binding 刷新
    state.bindingStrength = Math.min(1, state.bindingStrength + 0.2)
    state.lastContextMatch = now
  } else {
    // 话题不匹配 → 指数衰减（半衰期 2 小时）
    const hoursSince = (now - state.lastContextMatch) / 3600000
    state.bindingStrength *= Math.exp(-0.35 * hoursSince)
  }

  // 对话惯性保底：momentum 高的记忆不会被完全遗忘
  try {
    const { getMomentumBoost } = require('./activation-field.ts')
    const momentum = getMomentumBoost(mem.content || '')
    if (momentum > 0.1) {
      state.bindingStrength = Math.max(state.bindingStrength, momentum)
    }
  } catch {}

  return state.bindingStrength
}

/**
 * 获取当前话题签名（heartbeat 时调用）
 * 优先用最近 session 话题，距今 > 6小时返回空数组
 */
export function getCurrentTopics(): string[] {
  try {
    const { getSessionState, getLastActiveSessionKey } = require('./handler-state.ts')
    const sess = getSessionState(getLastActiveSessionKey())
    if (!sess) return []
    // session 距今 > 6小时 → 无活跃话题
    const lastActivity = sess.lastMessageTs || 0
    if (Date.now() - lastActivity > 6 * 3600000) return []
    // 从 session 的最近消息提取话题关键词
    const recentMsgs = (sess.recentMessages || []).slice(-3)
    const topics = recentMsgs.map((m: any) => (m.content || m.user || '').slice(0, 100))
    return topics
  } catch {
    return []
  }
}

// P0 部署时间戳 — 用于 graveyard grace period（7 天内保留完整 content）
// 持久化到 distill_state.json，避免进程重启后 grace period 重置
let P0_DEPLOY_TS = 0
function getP0DeployTs(): number {
  if (P0_DEPLOY_TS > 0) return P0_DEPLOY_TS
  try {
    const { loadJson, saveJson, DATA_DIR } = require('./persistence.ts')
    const { resolve } = require('path')
    const path = resolve(DATA_DIR, 'distill_state.json')
    const state = loadJson(path, {})
    if (state.p0DeployTs) {
      P0_DEPLOY_TS = state.p0DeployTs
    } else {
      P0_DEPLOY_TS = Date.now()
      state.p0DeployTs = P0_DEPLOY_TS
      saveJson(path, state)
    }
  } catch {
    P0_DEPLOY_TS = Date.now()
  }
  return P0_DEPLOY_TS
}
const GRAVEYARD_GRACE_PERIOD = 7 * 86400000  // 7 天
const GRAVEYARD_PURGE_AGE = 180 * 86400000   // 180 天彻底清除

// ═══════════════════════════════════════════════════════════════════════════════
// Derivability Decay — 信息可推导性衰减（原创算法）
// 一条记忆的信息能否从其他系统推导出来？可推导 → 优先遗忘，独有 → 保护
// ═══════════════════════════════════════════════════════════════════════════════

function computeDerivability(mem: MemoryInput): number {
  const content = mem.content || ''
  if (!content || content.length < 5) return 0.5
  if (mem.scope === 'correction') return 0  // 纠正永远不可推导

  let d = 0

  // 1. 知识图谱已有这些实体？
  try {
    const { findMentionedEntities } = require('./graph.ts')
    const entities = findMentionedEntities(content)
    if (entities.length > 0) d += 0.2
  } catch {}

  // 2. fact-store 已有同样的三元组？
  try {
    const { extractFacts, queryFacts } = require('./fact-store.ts')
    const facts = extractFacts(content)
    let existingCount = 0
    for (const f of facts) {
      const existing = queryFacts({ subject: f.subject, predicate: f.predicate })
      if (existing && existing.length > 0) existingCount++
    }
    if (facts.length > 0) d += 0.3 * (existingCount / facts.length)
  } catch {}

  // 3. topic node 已覆盖？
  try {
    const { getRelevantTopics } = require('./distill.ts')
    const topics = getRelevantTopics(content, mem.userId, 1)
    if (topics.length > 0) d += 0.2
  } catch {}

  // 4. L3 mental model 已包含？
  try {
    const { getMentalModel } = require('./distill.ts')
    const model = getMentalModel(mem.userId)
    if (model) {
      const modelWords = new Set((model.match(WORD_PATTERN.CJK2_EN3) || []).map((w: string) => w.toLowerCase()))
      const memWords = (content.match(WORD_PATTERN.CJK2_EN3) || []).map((w: string) => w.toLowerCase())
      let overlap = 0
      for (const w of memWords) if (modelWords.has(w)) overlap++
      if (memWords.length > 0 && overlap / memWords.length > 0.4) d += 0.2
    }
  } catch {}

  return Math.min(0.9, d)
}

/**
 * 领地划分遗忘判定（P5a 升级版）
 *
 * R = I(m) × 0.3 + B × 0.7（结构重要性保底 + 语境绑定动态层）
 * C = Bayes α/(α+β)（可信度）
 * θ = BCM 自适应阈值（遗忘标准）
 */
export function decideForget(mem: MemoryInput, activityLevel: number): ForgetDecision {
  // ── I: structuralImportance（有多重要）──
  const I = computeStructuralImportance(mem)

  // ── B: contextBinding（跟当前话题多相关）──
  const currentTopics = getCurrentTopics()
  const B = computeContextBinding(mem, currentTopics)

  // ── R: 综合相关性 = 保底层 + 动态层 ──
  const R = Math.min(1, I * 0.3 + B * 0.7)

  // ── C: Bayes truthfulness（是不是真的）──
  const alpha = mem.bayesAlpha ?? 2
  const beta = mem.bayesBeta ?? 1
  const C = alpha / (alpha + beta)

  // ── θ: BCM adaptive threshold（标准多严）──
  const θ = bcmAdaptiveThreshold(getSurvivalForgetThreshold(), activityLevel)

  // ── 四分支判定 ──
  let action: ForgetDecision['action']
  let reason: string

  if (R >= θ && C >= 0.3) {
    action = 'keep'
    reason = `R=${R.toFixed(2)}(I=${I.toFixed(1)},B=${B.toFixed(2)})≥θ=${θ.toFixed(2)}, C=${C.toFixed(2)}≥0.3`
  } else if (R >= θ && C < 0.3) {
    action = 'verify'
    reason = `R=${R.toFixed(2)}≥θ=${θ.toFixed(2)}, C=${C.toFixed(2)}<0.3 相关但可疑`
  } else {
    // ── Derivability Decay（惰性计算：只对即将 demote/graveyard 的记忆算）──
    // 可推导的记忆优先遗忘，独有信息被保护
    const d = computeDerivability(mem)
    const R_adjusted = R * (1 - d * 0.3)  // 最多打 73 折

    if (R_adjusted < θ && C >= 0.3) {
      action = 'demote'
      reason = `R=${R.toFixed(2)}→R_adj=${R_adjusted.toFixed(2)}(d=${d.toFixed(2)})<θ=${θ.toFixed(2)}, C=${C.toFixed(2)}≥0.3 可信但可推导`
    } else if (R_adjusted < θ && C < 0.3) {
      action = 'graveyard'
      reason = `R=${R.toFixed(2)}→R_adj=${R_adjusted.toFixed(2)}(d=${d.toFixed(2)})<θ=${θ.toFixed(2)}, C=${C.toFixed(2)}<0.3`
    } else {
      // derivability 救了它：原本要 demote 但不可推导
      action = 'keep'
      reason = `R=${R.toFixed(2)}<θ but R_adj=${R_adjusted.toFixed(2)}≥θ (d=${d.toFixed(2)} low=独有信息)`
    }
  }

  return { retrievability: R, truthfulness: C, threshold: θ, action, reason }
}

/**
 * Graveyard 复活：当 recall 结果不足时，fallback 查 graveyard
 * trigram 匹配 > 0.5 → 复活为 short_term，FSRS 重新初始化
 */
export function reviveFromGraveyard(query: string, memories: any[], maxRevive: number = 2): any[] {
  const revived: any[] = []
  const queryTri = trigrams(query)
  if (queryTri.size === 0) return revived

  for (const m of memories) {
    if (!m || m.tier !== 'graveyard') continue
    const memTri = trigrams(m.content || '')
    const sim = trigramSimilarity(queryTri, memTri)
    if (sim > TRIGRAM_THRESHOLD.GRAVEYARD_REVIVE) {
      m.tier = 'short_term'
      m.scope = m._graveyardOriginalScope || 'fact'
      m.fsrs = fsrsInit(m.scope)
      m.lastAccessed = Date.now()
      delete m._graveyardOriginalScope
      revived.push(m)
      logDecision('revive', (m.content || '').slice(0, 30) + '|' + m.ts,
        `trigramSim=${sim.toFixed(2)}>${TRIGRAM_THRESHOLD.GRAVEYARD_REVIVE}, query="${query.slice(0, 20)}"`)
      if (revived.length >= maxRevive) break
    }
  }
  return revived
}

/**
 * Graveyard 彻底清除：age > 180天 且从未被复活查询命中
 */
export function purgeGraveyard(memories: any[]): number {
  const now = Date.now()
  let purged = 0
  for (let i = memories.length - 1; i >= 0; i--) {
    const m = memories[i]
    if (!m || m.tier !== 'graveyard') continue
    const graveyardAge = now - (m._graveyardTs || m.ts)
    // 只清除：age > 180天 且从未被复活命中（lastAccessed 未更新过）
    const neverRevived = !m.lastAccessed || m.lastAccessed <= (m._graveyardTs || m.ts)
    if (graveyardAge > GRAVEYARD_PURGE_AGE && neverRevived) {
      const key = (m.content || '').slice(0, 30) + '|' + m.ts
      logDecision('purge', key, `graveyardAge=${(graveyardAge / 86400000).toFixed(0)}d>180d, neverRevived`)
      memories.splice(i, 1)
      purged++
    }
  }
  return purged
}

// ═══════════════════════════════════════════════════════════════════════════════
// P2b: Contradiction → Bayes（矛盾检测命中时降低 truthfulness）
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * 当蒸馏系统检测到矛盾时调用：降低旧记忆的 Bayes 可信度
 */
export function penalizeTruthfulness(mem: any, reason: string): void {
  mem.bayesBeta = (mem.bayesBeta ?? 1) + 1
  const C = (mem.bayesAlpha ?? 2) / ((mem.bayesAlpha ?? 2) + mem.bayesBeta)
  logDecision('bayes_penalty', (mem.content || '').slice(0, 30) + '|' + mem.ts,
    `bayesBeta++→${mem.bayesBeta}, C=${C.toFixed(2)}, reason=${reason}`)
}

// ═══════════════════════════════════════════════════════════════════════════════
// P2c: 遗忘即蒸馏 — decay 产生 gist，积累后触发 L2 蒸馏
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * 从即将遗忘的记忆中提取结构化 gist（零 LLM）
 * 提取实体、事实三元组、因果链
 */
export function extractGistBeforeForget(mem: any): any | null {
  const content = mem.content || ''
  if (content.length < 10) return null

  let facts: any[] = []
  let entities: string[] = []
  try {
    const factStore = require('./fact-store.ts')
    facts = factStore.extractFacts(content)
  } catch {}
  try {
    const graph = require('./graph.ts')
    entities = graph.findMentionedEntities(content)
  } catch {}

  const hasCausal = !!mem.reasoning || !!mem.because
  if (facts.length === 0 && entities.length === 0 && !hasCausal) {
    return null  // 纯废话，不值得提取 gist
  }

  return {
    entities,
    facts: facts.map((f: any) => ({ subject: f.subject, predicate: f.predicate, object: f.object })),
    causal: mem.reasoning ?? null,
    because: mem.because ?? null,
    originalScope: mem.scope,
    originalTs: mem.ts,
    forgottenAt: Date.now(),
  }
}

/**
 * 收集 decay sweep 中的 gist，聚类后触发蒸馏
 * 每轮最多 3 次 LLM 调用，超限排入 distill_state.json.pendingDecayDistill
 */
export function processDecayedGists(gists: any[]): void {
  if (gists.length < 2) return

  // 按共享实体聚类（简单版）
  const clusters: any[][] = []
  const assigned = new Set<number>()

  for (let i = 0; i < gists.length; i++) {
    if (assigned.has(i)) continue
    const cluster = [gists[i]]
    assigned.add(i)

    for (let j = i + 1; j < gists.length; j++) {
      if (assigned.has(j)) continue
      // 共享实体 → 同簇
      const shared = gists[i].entities.filter((e: string) => gists[j].entities.includes(e))
      if (shared.length > 0) {
        cluster.push(gists[j])
        assigned.add(j)
      }
    }
    clusters.push(cluster)
  }

  // 每个簇触发零 LLM 蒸馏（通过 distill.ts 的 zeroLLMDistill）
  try {
    const distillMod = require('./distill.ts')
    let llmCalls = 0
    for (const cluster of clusters) {
      if (cluster.length < 2) continue
      const contents = cluster.map((g: any) => {
        const parts: string[] = []
        if (g.facts.length > 0) parts.push(g.facts.map((f: any) => `${f.subject}${f.predicate}${f.object}`).join('，'))
        if (g.entities.length > 0) parts.push(`涉及：${g.entities.join('、')}`)
        if (g.because) parts.push(`原因：${g.because}`)
        return parts.join('；') || `[${g.originalScope}] 遗忘于${new Date(g.forgottenAt).toISOString().slice(0,10)}`
      })

      // 排入蒸馏队列（不直接调 LLM，让 distillL1toL2 处理）
      if (!distillMod.distillState) continue
      const pending = distillMod.distillState.pendingDecayDistill ?? []
      pending.push({ contents, clusteredAt: Date.now() })
      // 限流：最多保留 10 个 pending
      if (pending.length > 10) pending.splice(0, pending.length - 10)
      distillMod.distillState.pendingDecayDistill = pending
    }
  } catch {}
}

/**
 * Batch-scan memories using territory division (R/C/θ if-else).
 * Returns indices categorized by action. Does NOT mutate the input array.
 */
export function smartForgetSweep(memories: any[]): SweepResult {
  const now = Date.now()
  const toForget: number[] = []
  const toConsolidate: number[] = []

  // ── BCM: 计算活跃度（唯一用途：决定遗忘标准多严）──
  const oneDayAgo = now - 86400000
  const recentCount = memories.filter(m => m && m.ts > oneDayAgo && m.scope !== 'expired').length
  const activityLevel = Math.min(1, recentCount / 100)

  for (let i = 0; i < memories.length; i++) {
    const m = memories[i]
    if (!m || typeof m.ts !== 'number') continue
    // 跳过已处理的
    if (m.scope === 'expired' || m.tier === 'graveyard') continue

    const mem: MemoryInput & { bayesAlpha?: number; bayesBeta?: number } = {
      ts: m.ts ?? now,
      recallCount: m.recallCount ?? m.recall_count ?? 0,
      lastAccessed: m.lastAccessed ?? m.last_accessed ?? m.ts ?? now,
      scope: m.scope ?? m.type ?? 'fact',
      confidence: m.confidence,
      fsrs: m.fsrs,
      bayesAlpha: m.bayesAlpha,
      bayesBeta: m.bayesBeta,
    }

    // ── 领地划分判定 ──
    const decision = decideForget(mem, activityLevel)
    const key = (m.content || '').slice(0, 30) + '|' + m.ts

    switch (decision.action) {
      case 'graveyard':
        toForget.push(i)
        logDecision('graveyard', key, decision.reason)
        break
      case 'demote':
        // 降级 tier 但不删除
        if (m.tier !== 'fading') {
          m.tier = 'fading'
          logDecision('demote', key, decision.reason)
        }
        break
      case 'verify':
        // 标记待验证（可信度低但还记得）
        if (!m._needsVerification) {
          m._needsVerification = true
          logDecision('verify', key, decision.reason)
        }
        break
      case 'keep':
        // 健康记忆，检查是否值得巩固
        if (decision.retrievability > getSurvivalConsolidateThreshold() &&
            decision.truthfulness > 0.7) {
          toConsolidate.push(i)
        }
        break
    }
  }

  return { toForget, toConsolidate }
}

// ═══════════════════════════════════════════════════════════════════════════════
// FSRS 主动回顾推荐 (Active Recall Recommendation)
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * FSRS 主动回顾推荐：找出即将被遗忘但值得保留的记忆
 * 在最佳时机（retrievability 接近遗忘阈值但还没忘）推荐回顾
 *
 * 选择标准：
 * 1. retrievability 在 0.3-0.6 之间（即将忘但还没完全忘）
 * 2. importance >= 6（值得保留的记忆）
 * 3. 不是 expired/decayed/consolidated
 */
export function getRecallRecommendations(memories: any[], maxCount: number = 3): { content: string; urgency: number }[] {
  const now = Date.now()
  const candidates: { mem: any; retrievability: number; importance: number; urgency: number }[] = []

  for (const m of memories) {
    if (!m || m.scope === 'expired' || m.scope === 'decayed' || m.scope === 'consolidated') continue
    const importance = m.importance ?? 5
    if (importance < 6) continue  // 不重要的不推荐

    const fsrs = m.fsrs || { stability: 30, difficulty: 5 }
    const ageDays = (now - (m.ts || now)) / MS_PER_DAY
    const retrievability = Math.pow(1 + ageDays / (9 * fsrs.stability), -1)

    // 最佳回顾窗口：retrievability 在 0.3-0.6 之间
    if (retrievability >= 0.3 && retrievability <= 0.6) {
      const urgency = (0.6 - retrievability) / 0.3  // 0→1，越接近忘越紧急
      candidates.push({ mem: m, retrievability, importance, urgency })
    }
  }

  // 按紧急度 × 重要度排序
  candidates.sort((a, b) => (b.urgency * b.importance) - (a.urgency * a.importance))

  return candidates.slice(0, maxCount).map(c => ({
    content: c.mem.content.slice(0, 80),
    urgency: c.urgency,
  }))
}

// ═══════════════════════════════════════════════════════════════════════════════
// INTERNAL STATS
// ═══════════════════════════════════════════════════════════════════════════════

const stats: ForgetStats = {
  lastSweepTs: 0,
  lastSweepForget: 0,
  lastSweepConsolidate: 0,
  totalSweeps: 0,
}

// ═══════════════════════════════════════════════════════════════════════════════
// SOUL MODULE
// ═══════════════════════════════════════════════════════════════════════════════

export const smartForgetModule: SoulModule = {
  id: 'smart-forget',
  name: '智能遗忘引擎',
  priority: 20,

  async init(): Promise<void> {
    // Load adaptive decay params
    try {
      const { DATA_DIR } = await import('./persistence.ts')
      loadDecayParams(DATA_DIR)
    } catch {
      // Fallback: homedir-based path
      try {
        const { homedir } = await import('os')
        const p = resolve(homedir(), '.openclaw/plugins/cc-soul/data')
        if (existsSync(p)) loadDecayParams(p)
      } catch {}
    }
    // Initialize per-scope k defaults if not yet stored
    if (!_decayParams.scopeK) {
      _decayParams.scopeK = { ...WEIBULL_K_DEFAULT }
      saveDecayParams()
    }
    console.log(`[smart-forget] initialized — FSRS-7 + LECTOR interference, ACT-R d=0.5, λ-multiplier=${_decayParams.lambdaMultiplier.toFixed(3)} (EMA α=${getEMAAlpha()})`)
  },

  dispose(): void {
    // Nothing to clean up — stateless module
  },

  /** Periodic sweep during heartbeat */
  async onHeartbeat(): Promise<void> {
    // Lazy-import memory state to avoid circular dependency at module level
    let memories: any[] = []
    try {
      // Dynamic import to avoid side-effects at module level
      const memModule = await import('./memory.ts')
      memories = memModule?.memoryState?.memories ?? []
    } catch {
      // If memory module not available, skip
      return
    }

    if (memories.length === 0) return

    const result = smartForgetSweep(memories)
    stats.lastSweepTs = Date.now()
    stats.lastSweepForget = result.toForget.length
    stats.lastSweepConsolidate = result.toConsolidate.length
    stats.totalSweeps++

    // Execute forget: move to graveyard + extract gist (P2c)
    if (result.toForget.length > 0) {
      const maxPerSweep = getParam('forget.max_per_sweep')
      const toForget = result.toForget.slice(0, maxPerSweep)
      const isGracePeriod = Date.now() - getP0DeployTs() < GRAVEYARD_GRACE_PERIOD
      const gists: any[] = []
      for (let i = toForget.length - 1; i >= 0; i--) {
        const idx = toForget[i]
        if (idx >= 0 && idx < memories.length && memories[idx].tier !== 'graveyard') {
          const m = memories[idx]
          // P2c: 遗忘前提取 gist
          const gist = extractGistBeforeForget(m)
          if (gist) gists.push(gist)

          m._graveyardOriginalScope = m.scope
          m._graveyardTs = Date.now()
          m.tier = 'graveyard'
          m.scope = 'expired'
          // 溯源链
          try { const { appendLineage } = require('./memory-utils.ts'); appendLineage(m, { action: 'gisted', ts: Date.now(), delta: `→graveyard, from:${(m.content||'').length}` }) } catch {}
          // Grace period: 前 7 天保留完整 content，之后压缩到 50 字
          if (!isGracePeriod) {
            m.content = (m.content || '').slice(0, 50)
          }
        }
      }
      // P2c: 收集 gists 触发蒸馏
      if (gists.length >= 2) {
        processDecayedGists(gists)
      }
      // 缓存失效通知
      emitCacheEvent('memory_deleted')
    }

    // Execute consolidate: promote scope
    if (result.toConsolidate.length > 0) {
      for (const idx of result.toConsolidate) {
        if (idx >= 0 && idx < memories.length && memories[idx].scope !== 'consolidated') {
          memories[idx].scope = 'consolidated'
        }
      }
    }

    // Graveyard 定期清除：age > 180天
    purgeGraveyard(memories)

    if (result.toForget.length > 0 || result.toConsolidate.length > 0) {
      // Persist changes
      try {
        const memModule = await import('./memory.ts')
        memModule.saveMemories()
      } catch {}

      console.log(
        `[smart-forget] sweep #${stats.totalSweeps}: ` +
        `${result.toForget.length} forgotten, ${result.toConsolidate.length} consolidated ` +
        `(out of ${memories.length} memories)`
      )
    }
  },
}
