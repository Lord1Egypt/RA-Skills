/**
 * auto-tune.ts — Parameter auto-tuning via Thompson Sampling bandit
 *
 * Each tunable parameter is discretized into 5 arms (0.5x..1.5x of default).
 * A Beta distribution tracks success/failure for each arm. Thompson Sampling
 * selects which arm to play. Learns online from every response quality signal.
 *
 * Replaces the old fixed-duration A/B experiment approach with continuous
 * Bayesian optimization that converges faster and handles non-stationarity.
 */

import { resolve } from 'path'
import { DATA_DIR, loadJson, saveJson, debouncedSave } from './persistence.ts'
import { notifyOwnerDM } from './notify.ts'
import { computeEval } from './quality.ts'
import type { InteractionStats } from './types.ts'

// ══════════════════════════════════════════════════════════════════════════════
// TUNABLE PARAMETERS — centralized config (replaces hardcoded constants)
// ══════════════════════════════════════════════════════════════════════════════

const PARAMS_PATH = resolve(DATA_DIR, 'tunable_params.json')
const TUNE_STATE_PATH = resolve(DATA_DIR, 'auto_tune_state.json')

/** Default values — exactly matching current hardcoded constants */
const DEFAULT_PARAMS: Record<string, number> = {
  // memory.ts
  'memory.recall_top_n': 3,
  'memory.age_decay_rate': 0.02,
  'memory.consolidation_cooldown_hours': 24,
  'memory.session_summary_cooldown_min': 30,
  'memory.contradiction_scan_cooldown_hours': 24,

  // body.ts
  'body.energy_recovery_per_min': 0.015,
  'body.alertness_decay_per_min': 0.008,
  'body.alertness_recovery_per_min': 0.005,
  'body.load_decay_per_min': 0.02,
  'body.mood_decay_factor': 0.995,
  'body.correction_alertness_boost': 0.2,
  'body.correction_mood_penalty': 0.1,
  'body.positive_energy_boost': 0.05,
  'body.positive_mood_boost': 0.08,
  'body.positive_anomaly_reduction': 0.05,
  'body.resilience': 0.3,
  'body.message_energy_base_cost': 0.02,
  'body.message_energy_complexity_cost': 0.03,
  'body.message_load_base': 0.1,
  'body.message_load_complexity': 0.15,
  'body.correction_anomaly_boost': 0.15,
  'body.anomaly_decay_per_min': 0.01,

  // cognition.ts
  'cognition.casual_max_length': 15,
  'cognition.quick_intent_max_length': 20,
  'cognition.detailed_min_length': 200,

  // quality.ts
  'quality.medium_length_bonus': 0.5,
  'quality.long_length_bonus': 0.5,
  'quality.reasoning_bonus': 1.0,
  'quality.code_bonus': 0.5,
  'quality.ai_exposure_penalty': 2.0,
  'quality.relevance_weight': 1.5,

  // activation-field.ts — 聚合查询检测
  'recall.aggregation_dropoff': 0.3,

  // flow.ts
  'flow.frustration_shortening_rate': 0.2,
  'flow.frustration_terse': 0.15,
  'flow.frustration_keyword_rate': 0.3,
  'flow.frustration_question_rate': 0.1,
  'flow.frustration_repetition': 0.15,
  'flow.frustration_decay_per_turn': 0.05,
  'flow.stuck_threshold': 0.5,

  // prompt-builder.ts
  'prompt.augment_budget': 3500,


  // evolution.ts
  'evolution.hypothesis_verify_threshold': 5,
  'evolution.hypothesis_reject_threshold': 3,
  'evolution.max_rules': 50,

  // inner-life.ts
  'inner.journal_cooldown_min': 30,
  'inner.reflection_cooldown_hours': 24,

  // memory.ts — fusion weights
  'memory.fusion_text_weight': 0.5,
  'memory.fusion_vec_weight': 0.5,
  'memory.fusion_multi_source_boost': 1.3,

  // memory.ts — recall scoring
  'memory.trigram_dedup_threshold': 0.7,
  'memory.bm25_k1': 1.2,
  'memory.bm25_b': 0.75,
  'memory.time_decay_halflife_days': 90,

  // evolution.ts — hypothesis thresholds
  'evolution.rule_dedup_threshold': 0.45,
  'evolution.hypothesis_verify_ci_lb': 0.6,
  'evolution.hypothesis_reject_ci_ub': 0.4,
  'evolution.hypothesis_match_min_sim': 0.2,
  'evolution.reflexion_sim_threshold': 0.3,

  // body.ts — emotional contagion
  'body.contagion_max_shift': 0.15,

  // graph.ts — stale entity threshold
  'graph.stale_days': 90,

  // persona.ts — blend thresholds
  'persona.blend_gap_threshold': 0.3,
  'persona.attention_trigger_bonus': 0.2,

  // smart-forget — Weibull k (shape) per scope
  'forget.weibull_k_fact': 1.2,
  'forget.weibull_k_preference': 0.9,
  'forget.weibull_k_episode': 1.4,
  // smart-forget — Weibull lambda (scale) per scope
  'forget.weibull_lambda_fact': 30,
  'forget.weibull_lambda_preference': 90,
  'forget.weibull_lambda_episode': 14,
  // smart-forget — ACT-R & thresholds
  'forget.act_r_decay': 0.5,
  'forget.survival_threshold': 0.1,
  'forget.activation_threshold': -1.0,
  'forget.consolidation_threshold_survival': 0.8,
  'forget.consolidation_threshold_activation': 2.0,

  // recall — weighted log-sum weights
  'recall.w_sim': 3.0,
  'recall.w_recency': 1.5,
  'recall.w_scope': 1.0,
  'recall.w_emotion': 0.8,
  'recall.w_user': 0.8,
  'recall.w_confidence': 1.0,
  'recall.w_mood': 0.5,

  // lifecycle — cooldowns (hours)
  'lifecycle.consolidation_cooldown_hours': 24,
  'lifecycle.distill_l1_hours': 6,
  'lifecycle.distill_l2_hours': 12,
  'lifecycle.decay_scan_hours': 6,

  // capacity limits
  'capacity.core_memory_max': 100,
  'capacity.working_memory_max': 20,
  'capacity.entity_max': 800,
  'capacity.relation_max': 1600,
  'capacity.augment_budget': 3500,

  // 遗忘模型（smart-forget 相关）
  'forget.ema_alpha': 0.05,
  'forget.lambda_max_multiplier': 3.0,
  'forget.recall_increment_percent': 15,
  'forget.emotion_high_multiplier': 2.0,
  'forget.emotion_medium_multiplier': 1.5,
  'forget.max_per_sweep': 20,
  'forget.actr_max_iterations': 50,

  // 召回 boost 系数
  'recall.scope_boost_preference': 1.3,
  'recall.scope_boost_correction': 1.5,
  'recall.emotion_boost_important': 1.4,
  'recall.emotion_boost_painful': 1.3,
  'recall.emotion_boost_warm': 1.2,
  'recall.user_boost_same': 2.0,
  'recall.user_boost_other': 0.7,
  'recall.tier_weight_hot': 1.5,
  'recall.tier_weight_warm': 1.0,
  'recall.tier_weight_cool': 0.8,
  'recall.tier_weight_cold': 0.5,
  'recall.consolidated_boost': 1.5,
  'recall.reflexion_boost': 2.0,
  'recall.flashbulb_high': 1.6,
  'recall.flashbulb_medium': 1.2,
  'recall.mmr_lambda': 0.7,

  // 生命周期
  'lifecycle.recall_feedback_cooldown_ms': 60000,
  'lifecycle.association_cooldown_ms': 30000,
  'lifecycle.session_summary_cooldown_ms': 1800000,
  'lifecycle.contradiction_scan_cooldown_ms': 86400000,
  'lifecycle.decay_cooldown_ms': 21600000,
  'lifecycle.max_insights': 20,
  'lifecycle.max_episodes': 200,

  // 容量
  'memory.max_memories': 10000,
  'memory.max_history': 100,
  'memory.inject_history': 30,
  'memory.trigram_cache_max': 2000,

  // 认知
  'cognition.correction_weight': 3,
  'cognition.emotion_weight': 2,
  'cognition.tech_weight': 2,

  // 其他
  'persona.cooldown_ms': 120000,
  'quality.repetition_sim_threshold': 0.7,
  'metacognition.conflict_threshold': 0.3,
  'metacognition.min_samples': 5,
}

/** The live params — loaded from disk, falls back to defaults */
let params: Record<string, number> = { ...DEFAULT_PARAMS }

export function loadTunableParams() {
  const saved = loadJson<Record<string, number>>(PARAMS_PATH, {})
  params = { ...DEFAULT_PARAMS, ...saved }
  // Save back to add any new default keys
  saveJson(PARAMS_PATH, params)
}

/** Get a tunable parameter value (used by other modules) */
export function getParam(key: string): number {
  return params[key] ?? DEFAULT_PARAMS[key] ?? 0
}

/** Set a parameter (for experiment or manual override) */
export function setParam(key: string, value: number) {
  params[key] = value
  debouncedSave(PARAMS_PATH, params)
}

/** Reset a param to default */
export function resetParam(key: string) {
  params[key] = DEFAULT_PARAMS[key] ?? 0
  debouncedSave(PARAMS_PATH, params)
}

// ══════════════════════════════════════════════════════════════════════════════
// LEGACY STATE — kept for backward compatibility (old experiment history)
// ══════════════════════════════════════════════════════════════════════════════

interface TuneExperiment {
  paramKey: string
  originalValue: number
  testValue: number
  startedAt: number
  endsAt: number
  preMetrics: { avgQuality: number; correctionRate: number; messages: number }
  postMetrics: { avgQuality: number; correctionRate: number; messages: number }
  status: 'running' | 'adopted' | 'reverted' | 'insufficient_data'
}

interface TuneState {
  currentExperiment: TuneExperiment | null
  history: TuneExperiment[]
  lastTuneCheck: number
  paramQueue: string[]
}

let tuneState: TuneState = loadJson(TUNE_STATE_PATH, {
  currentExperiment: null,
  history: [],
  lastTuneCheck: 0,
  paramQueue: [],
})

function saveTuneState() {
  debouncedSave(TUNE_STATE_PATH, tuneState)
}

// ══════════════════════════════════════════════════════════════════════════════
// THOMPSON SAMPLING BANDIT — data structures
// ══════════════════════════════════════════════════════════════════════════════

interface BanditArm {
  value: number
  alpha: number  // successes + 1 (Beta prior)
  beta: number   // failures + 1 (Beta prior)
  pulls: number
}

interface ParamBanditState {
  key: string
  arms: BanditArm[]
  currentArm: number  // index of currently active arm
  totalPulls: number
  phase: 1 | 2          // hierarchical search phase
  winnerMultiplier?: number  // Phase 1 winner direction (for Phase 2 refinement)
}

const BANDIT_STATE_PATH = resolve(DATA_DIR, 'bandit_state.json')
let banditState: Record<string, ParamBanditState> = {}

// ══════════════════════════════════════════════════════════════════════════════
// CONTEXTUAL THOMPSON SAMPLING — context-aware arm selection layer
// ══════════════════════════════════════════════════════════════════════════════

interface ContextualArm {
  contextKey: string  // e.g. "morning:tech:neutral"
  alpha: number
  beta: number
}

/** Per-param contextual bandit state — layered on top of global bandit */
interface ContextualBanditState {
  arms: Record<string, ContextualArm[]>  // paramKey → contextKey → per-arm Beta
}

const CTX_BANDIT_PATH = resolve(DATA_DIR, 'ctx_bandit_state.json')
let ctxBanditState: ContextualBanditState = { arms: {} }

function loadCtxBanditState() {
  ctxBanditState = loadJson<ContextualBanditState>(CTX_BANDIT_PATH, { arms: {} })
}

function saveCtxBanditState() {
  debouncedSave(CTX_BANDIT_PATH, ctxBanditState)
}

/** Build context key from current environment */
function buildContextKey(timeSlot?: string, domain?: string, mood?: string): string {
  const ts = timeSlot || getTimeSlot(new Date().getHours())
  const d = domain || 'general'
  const m = mood || 'neutral'
  return `${ts}:${d}:${m}`
}

function getTimeSlot(hour: number): string {
  if (hour >= 6 && hour < 12) return 'morning'
  if (hour >= 12 && hour < 18) return 'afternoon'
  if (hour >= 18 && hour < 23) return 'evening'
  return 'night'
}

/** Context-aware arm selection: use context-specific Beta if enough data, else fall back to global */
function selectArmContextual(state: ParamBanditState, ctxKey: string): number {
  const ctxArms = ctxBanditState.arms[state.key]
  if (ctxArms) {
    // Find arms matching this context with enough samples
    const matching = ctxArms.filter(a => a.contextKey === ctxKey)
    if (matching.length >= state.arms.length) {
      const totalPulls = matching.reduce((s, a) => s + a.alpha + a.beta - 2, 0)
      if (totalPulls >= 5) {
        // Use contextual Beta distributions
        let bestIdx = 0, bestSample = -1
        for (let i = 0; i < Math.min(matching.length, state.arms.length); i++) {
          const sample = betaSample(matching[i].alpha, matching[i].beta)
          if (sample > bestSample) { bestSample = sample; bestIdx = i }
        }
        return bestIdx
      }
    }
  }
  // Fall back to global Thompson Sampling
  return selectArm(state)
}

/** Update contextual bandit reward */
function updateCtxBanditReward(paramKey: string, armIdx: number, reward: number, ctxKey: string) {
  if (!ctxBanditState.arms[paramKey]) ctxBanditState.arms[paramKey] = []
  const arms = ctxBanditState.arms[paramKey]

  // Ensure enough arms for this context
  while (arms.filter(a => a.contextKey === ctxKey).length < (banditState[paramKey]?.arms.length || 3)) {
    arms.push({ contextKey: ctxKey, alpha: 1, beta: 1 })
  }

  const matching = arms.filter(a => a.contextKey === ctxKey)
  if (armIdx < matching.length) {
    // 多维 reward 缩放（与全局 bandit 一致）
    const REWARD_SCALE = 5
    matching[armIdx].alpha += reward * REWARD_SCALE
    matching[armIdx].beta += (1 - reward) * REWARD_SCALE

    // Discount old observations to adapt to non-stationary preferences
    const DISCOUNT_FACTOR = 0.995
    const ctxArm = matching[armIdx]
    ctxArm.alpha *= DISCOUNT_FACTOR
    ctxArm.beta *= DISCOUNT_FACTOR
    if (ctxArm.alpha + ctxArm.beta < 2) {
      ctxArm.alpha = Math.max(ctxArm.alpha, 1)
      ctxArm.beta = Math.max(ctxArm.beta, 1)
    }
  }

  // Prune: keep max 200 context entries per param to bound memory
  if (arms.length > 200) {
    const sorted = arms.sort((a, b) => (a.alpha + a.beta) - (b.alpha + b.beta))
    ctxBanditState.arms[paramKey] = sorted.slice(-150)
  }
}

// Current context key (set per-message from handler)
let _currentCtxKey = 'afternoon:general:neutral'

// ══════════════════════════════════════════════════════════════════════════════
// THOMPSON SAMPLING MATH — pure JS, no dependencies
// ══════════════════════════════════════════════════════════════════════════════

/** Standard normal sample via Box-Muller */
function randn(): number {
  const u1 = Math.random(), u2 = Math.random()
  return Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2)
}

/** Gamma distribution sample via Marsaglia-Tsang method */
function gammaSample(shape: number): number {
  shape = Math.max(0.01, shape)  // guard against NaN from zero/negative shape
  if (shape < 1) return gammaSample(shape + 1) * Math.pow(Math.random(), 1 / shape)
  const d = shape - 1 / 3
  const c = 1 / Math.sqrt(9 * d)
  while (true) {
    let x: number, v: number
    do { x = randn(); v = 1 + c * x } while (v <= 0)
    v = v * v * v
    const u = Math.random()
    if (u < 1 - 0.0331 * x * x * x * x) return d * v
    if (Math.log(u) < 0.5 * x * x + d * (1 - v + Math.log(v))) return d * v
  }
}

/** Beta distribution sample via two Gamma samples */
function betaSample(alpha: number, beta: number): number {
  const safeAlpha = Math.max(0.01, alpha)
  const safeBeta = Math.max(0.01, beta)
  const x = gammaSample(safeAlpha)
  const y = gammaSample(safeBeta)
  return x / (x + y)
}

/** Thompson Sampling: draw from each arm's posterior, pick the max */
function selectArm(state: ParamBanditState): number {
  let bestIdx = state.currentArm, bestSample = -1
  for (let i = 0; i < state.arms.length; i++) {
    const sample = betaSample(state.arms[i].alpha, state.arms[i].beta)
    if (sample > bestSample) {
      bestSample = sample
      bestIdx = i
    }
  }
  return bestIdx
}

// ══════════════════════════════════════════════════════════════════════════════
// BANDIT INITIALIZATION & PERSISTENCE
// ══════════════════════════════════════════════════════════════════════════════

/** Check if a param key is integer-like */
function isIntegerParam(key: string): boolean {
  return key.includes('cooldown') || key.includes('threshold') ||
         key.includes('max_') || key.includes('top_n') || key.includes('min_')
}

/** Create bandit state for a single parameter — Phase 1: 3 arms [0.8x, 1.0x, 1.2x] */
function initBanditForParam(key: string): ParamBanditState | null {
  const defaultVal = DEFAULT_PARAMS[key]
  if (defaultVal === undefined) return null

  const multipliers = [0.8, 1.0, 1.2]  // Phase 1: coarse search
  const isInt = isIntegerParam(key)

  return {
    key,
    arms: multipliers.map(m => ({
      value: isInt ? Math.max(1, Math.round(defaultVal * m)) : Math.max(0.001, +(defaultVal * m).toFixed(4)),
      alpha: 1,  // uniform prior
      beta: 1,
      pulls: 0,
    })),
    currentArm: 1, // index 1 = 1.0x = default value
    totalPulls: 0,
    phase: 1 as const,
  }
}

/** Phase 2 refinement: zoom into winner direction with 3 finer arms */
const PHASE2_THRESHOLD = 30  // samples needed to lock Phase 1 winner

function maybePromoteToPhase2(state: ParamBanditState): boolean {
  if (state.phase === 2) return false

  // Find arm with most pulls that crossed threshold
  const winnerArm = state.arms.reduce((best, arm, i) =>
    arm.pulls > best.pulls ? { ...arm, idx: i, pulls: arm.pulls } : best,
    { idx: 0, pulls: 0, value: 0, alpha: 1, beta: 1 } as BanditArm & { idx: number }
  )
  if (winnerArm.pulls < PHASE2_THRESHOLD) return false

  // Confirm winner via win rate (must be best)
  const winRates = state.arms.map(a => a.alpha / (a.alpha + a.beta))
  const bestIdx = winRates.indexOf(Math.max(...winRates))
  if (state.arms[bestIdx].pulls < PHASE2_THRESHOLD) return false

  const defaultVal = DEFAULT_PARAMS[state.key]
  if (defaultVal === undefined) return false

  // Determine Phase 2 multipliers based on winner direction
  const winnerMultiplier = state.arms[bestIdx].value / defaultVal
  let phase2Multipliers: number[]
  if (winnerMultiplier >= 1.15) {
    phase2Multipliers = [1.1, 1.2, 1.3]  // winner was 1.2x → refine upward
  } else if (winnerMultiplier <= 0.85) {
    phase2Multipliers = [0.7, 0.8, 0.9]  // winner was 0.8x → refine downward
  } else {
    phase2Multipliers = [0.9, 1.0, 1.1]  // winner was 1.0x → refine around center
  }

  const isInt = isIntegerParam(state.key)
  state.arms = phase2Multipliers.map(m => ({
    value: isInt ? Math.max(1, Math.round(defaultVal * m)) : Math.max(0.001, +(defaultVal * m).toFixed(4)),
    alpha: 1,
    beta: 1,
    pulls: 0,
  }))
  state.currentArm = 1
  state.phase = 2
  state.winnerMultiplier = winnerMultiplier
  state.totalPulls = 0  // reset for Phase 2
  console.log(`[cc-soul][auto-tune] ${state.key} promoted to Phase 2: winner=${winnerMultiplier.toFixed(2)}x → refine [${phase2Multipliers}]`)
  return true
}

function loadBanditState() {
  banditState = loadJson<Record<string, ParamBanditState>>(BANDIT_STATE_PATH, {})
  // Migrate legacy 5-arm states → Phase 1 (3-arm) on next init; existing states get phase=1 default
  for (const state of Object.values(banditState)) {
    if (!state.phase) state.phase = state.arms.length <= 3 ? 1 : 1  // treat old 5-arm as phase 1 too
  }
  loadCtxBanditState()
  console.log(`[cc-soul][auto-tune] bandit state loaded: ${Object.keys(banditState).length} params tracked, ctx bins: ${Object.keys(ctxBanditState.arms).length}`)
}

function saveBanditState() {
  debouncedSave(BANDIT_STATE_PATH, banditState)
}

// ══════════════════════════════════════════════════════════════════════════════
// HIGH-IMPACT PARAMS — prioritized for exploration
// ══════════════════════════════════════════════════════════════════════════════

const HIGH_IMPACT_PARAMS = [
  'memory.recall_top_n',
  'memory.age_decay_rate',
  'body.energy_recovery_per_min',
  'body.resilience',
  'body.mood_decay_factor',
  'quality.reasoning_bonus',
  'quality.relevance_weight',
  'flow.stuck_threshold',
  'flow.frustration_decay_per_turn',
  'prompt.augment_budget',
  'voice.impulse_threshold',
  'evolution.hypothesis_verify_threshold',
  'memory.trigram_dedup_threshold',
  'memory.bm25_k1',
  'evolution.rule_dedup_threshold',
  'body.contagion_max_shift',
  'graph.stale_days',
  // forget & recall — high impact on memory quality
  'forget.weibull_lambda_fact',
  'forget.weibull_lambda_episode',
  'forget.survival_threshold',
  'recall.w_sim',
  'recall.w_recency',
]

// ══════════════════════════════════════════════════════════════════════════════
// MAIN LOOP — Thompson Sampling replaces fixed A/B experiments
// ══════════════════════════════════════════════════════════════════════════════

const TUNE_CHECK_INTERVAL = 86400000 // check once per day

export function checkAutoTune(stats: InteractionStats) {
  const now = Date.now()

  // ── Finish any legacy running experiment first ──
  if (tuneState.currentExperiment) {
    const exp = tuneState.currentExperiment
    if (now >= exp.endsAt) {
      evaluateLegacyExperiment(stats)
    }
    return
  }

  // ── Cooldown ──
  if (now - tuneState.lastTuneCheck < TUNE_CHECK_INTERVAL) return

  // ── Need enough data ──
  if (stats.totalMessages < 50) return

  tuneState.lastTuneCheck = now

  // ── Initialize bandit state if needed ──
  if (Object.keys(banditState).length === 0) {
    loadBanditState()
  }

  // ── Build candidate list, excluding quality.* params (self-learning in quality.ts) ──
  const allKeys = Object.keys(DEFAULT_PARAMS).filter(k => !k.startsWith('quality.'))
  const exploreCount = 2

  // Ensure all params have bandit state
  for (const key of allKeys) {
    if (!banditState[key]) {
      const state = initBanditForParam(key)
      if (state) banditState[key] = state
    }
  }

  // Sort by fewest pulls (explore least-tested first), HIGH_IMPACT first
  const candidates = allKeys
    .filter(key => banditState[key])
    .map(key => ({ key, pulls: banditState[key].totalPulls }))
    .sort((a, b) => a.pulls - b.pulls)

  const highImpact = candidates.filter(c => HIGH_IMPACT_PARAMS.includes(c.key))
  const others = candidates.filter(c => !HIGH_IMPACT_PARAMS.includes(c.key))

  const toExplore: string[] = []
  for (const c of [...highImpact, ...others]) {
    if (toExplore.length >= exploreCount) break
    toExplore.push(c.key)
  }

  // ── Thompson Sampling: select arm for explored params (context-aware) ──
  for (const key of toExplore) {
    const state = banditState[key]
    if (!state) continue
    const armIdx = selectArmContextual(state, _currentCtxKey)
    state.currentArm = armIdx
    setParam(key, state.arms[armIdx].value)
    console.log(`[cc-soul][auto-tune] bandit explore: ${key} → arm[${armIdx}] = ${state.arms[armIdx].value} (ctx=${_currentCtxKey}, pulls=${state.totalPulls})`)
  }

  saveBanditState()
  saveTuneState()
}

// ══════════════════════════════════════════════════════════════════════════════
// BANDIT REWARD UPDATE — called from handler.ts after each response
// ══════════════════════════════════════════════════════════════════════════════

/**
 * Update bandit rewards after each response.
 * Called from handler.ts with quality score and correction flag.
 */
/**
 * 多维 reward Thompson Sampling（原创增强）
 * 不再只用 qualityScore，融合 quality + body + engagement 三维信号
 * reward 连续 [0,1]，用 k=5 的缩放因子加速学习
 */
export function updateBanditReward(qualityScore: number, wasCorrection: boolean, bodyResonance?: number, engagementSignal?: number) {
  if (Object.keys(banditState).length === 0) return

  // 多维 reward 融合
  const qualityReward = Math.max(0, Math.min(1, (qualityScore - 1) / 9))
  const bodyReward = bodyResonance ?? 0.5  // 默认中性
  const engReward = engagementSignal ?? 0.5

  let successProb = qualityReward * 0.5 + bodyReward * 0.2 + engReward * 0.3

  // Correction penalty
  if (wasCorrection) {
    successProb = Math.min(successProb, 0.2)
  }

  const reward = Math.max(0, Math.min(1, successProb))
  const REWARD_SCALE = 5  // 放大因子：好/差的回答贡献更多证据，加速学习

  for (const [key, state] of Object.entries(banditState)) {
    const armIdx = state.currentArm
    if (armIdx < 0 || armIdx >= state.arms.length) continue

    state.arms[armIdx].pulls++
    state.totalPulls++
    // 多维 reward 连续 Beta 更新（缩放因子加速学习）
    state.arms[armIdx].alpha += reward * REWARD_SCALE
    state.arms[armIdx].beta += (1 - reward) * REWARD_SCALE

    // Discount old observations to adapt to non-stationary preferences
    const DISCOUNT_FACTOR = 0.995
    const arm = state.arms[armIdx]
    arm.alpha *= DISCOUNT_FACTOR
    arm.beta *= DISCOUNT_FACTOR
    // 防止 alpha+beta 缩到太小（保持至少 prior=1）
    if (arm.alpha + arm.beta < 2) {
      arm.alpha = Math.max(arm.alpha, 1)
      arm.beta = Math.max(arm.beta, 1)
    }

    // Contextual update
    updateCtxBanditReward(key, armIdx, reward, _currentCtxKey)

    // Hierarchical search: check if Phase 1 winner is ready for Phase 2 refinement
    if (state.phase === 1) maybePromoteToPhase2(state)
  }

  saveBanditState()
  saveCtxBanditState()
}

// ══════════════════════════════════════════════════════════════════════════════
// LEGACY EXPERIMENT EVALUATE — handles old running experiments during migration
// ══════════════════════════════════════════════════════════════════════════════

function evaluateLegacyExperiment(stats: InteractionStats) {
  const exp = tuneState.currentExperiment
  if (!exp) return

  const currentEval = computeEval(stats.totalMessages, stats.corrections)
  const windowMessages = stats.totalMessages - exp.preMetrics.messages

  exp.postMetrics = {
    avgQuality: currentEval.avgQuality,
    correctionRate: currentEval.correctionRate,
    messages: windowMessages,
  }

  if (windowMessages < 10) {
    exp.status = 'insufficient_data'
    setParam(exp.paramKey, exp.originalValue)
    notifyOwnerDM(
      `⏳ 调参实验数据不足（${windowMessages} 条消息），已恢复 ${exp.paramKey} = ${exp.originalValue}`
    ).catch(() => {}) // intentionally silent — notification
  } else {
    const qualityDelta = currentEval.avgQuality - exp.preMetrics.avgQuality
    const correctionDelta = currentEval.correctionRate - exp.preMetrics.correctionRate
    const improved = qualityDelta > 0.2 || correctionDelta < -2
    const regressed = qualityDelta < -0.5 || correctionDelta > 3

    if (improved && !regressed) {
      exp.status = 'adopted'
      notifyOwnerDM(
        `✅ 调参实验成功！\n` +
        `参数: ${exp.paramKey}\n` +
        `${exp.originalValue} → ${exp.testValue} (已采用)\n` +
        `质量: ${exp.preMetrics.avgQuality.toFixed(1)} → ${currentEval.avgQuality.toFixed(1)} (${qualityDelta >= 0 ? '+' : ''}${qualityDelta.toFixed(1)})\n` +
        `纠正率: ${exp.preMetrics.correctionRate.toFixed(1)}% → ${currentEval.correctionRate.toFixed(1)}%`
      ).catch(() => {}) // intentionally silent — notification
    } else {
      exp.status = 'reverted'
      setParam(exp.paramKey, exp.originalValue)
      notifyOwnerDM(
        `↩️ 调参实验未改善，已恢复\n` +
        `参数: ${exp.paramKey} = ${exp.originalValue}\n` +
        `质量: ${qualityDelta >= 0 ? '+' : ''}${qualityDelta.toFixed(1)}, 纠正率: ${correctionDelta >= 0 ? '+' : ''}${correctionDelta.toFixed(1)}%`
      ).catch(() => {}) // intentionally silent — notification
    }
  }

  tuneState.history.push({ ...exp })
  if (tuneState.history.length > 100) tuneState.history = tuneState.history.slice(-100)
  tuneState.currentExperiment = null
  saveTuneState()

  console.log(`[cc-soul][auto-tune] legacy experiment ended: ${exp.paramKey} → ${exp.status}`)
}

// ══════════════════════════════════════════════════════════════════════════════
// COMMAND HANDLER — "调参状态" / "调参历史" / "调参 key=value"
// ══════════════════════════════════════════════════════════════════════════════

export function handleTuneCommand(msg: string): boolean {
  const m = msg.trim()

  // "tune" or "调整" alone → show status summary
  if (m === 'tune' || m === '调整') {
    const tracked = Object.keys(banditState).length
    const totalPulls = Object.values(banditState).reduce((s: number, st: any) => s + (st.totalPulls || 0), 0)
    console.log(`[cc-soul][auto-tune] status: ${tracked} params, ${totalPulls} pulls`)
    return true
  }

  if (m === '调参状态' || m === 'tune status') {
    // Legacy experiment status
    const exp = tuneState.currentExperiment
    if (exp) {
      const daysLeft = Math.ceil((exp.endsAt - Date.now()) / 86400000)
      console.log(`[cc-soul][auto-tune] legacy experiment running: ${exp.paramKey} ${exp.originalValue}→${exp.testValue}, ${daysLeft}d left`)
    }

    // Bandit status
    const tracked = Object.keys(banditState).length
    if (tracked > 0) {
      const totalPulls = Object.values(banditState).reduce((s, st) => s + st.totalPulls, 0)
      console.log(`[cc-soul][auto-tune] bandit: ${tracked} params tracked, ${totalPulls} total pulls`)

      // Show top 5 most-pulled params with their best arm
      const sorted = Object.values(banditState)
        .filter(st => st.totalPulls > 0)
        .sort((a, b) => b.totalPulls - a.totalPulls)
        .slice(0, 5)
      for (const st of sorted) {
        const bestArm = st.arms.reduce((best, arm, i) =>
          (arm.alpha / (arm.alpha + arm.beta)) > (best.ratio) ? { idx: i, ratio: arm.alpha / (arm.alpha + arm.beta) } : best,
          { idx: 0, ratio: 0 }
        )
        const current = st.arms[st.currentArm]
        console.log(`  ${st.key}: arm[${st.currentArm}]=${current.value} (pulls=${st.totalPulls}, best=arm[${bestArm.idx}] p=${bestArm.ratio.toFixed(2)})`)
      }
    } else {
      console.log(`[cc-soul][auto-tune] bandit: not yet initialized`)
    }
    return true
  }

  if (m === '调参历史' || m === 'tune history') {
    const recent = tuneState.history.slice(-10)
    if (recent.length === 0) {
      console.log('[cc-soul][auto-tune] 无历史记录')
    } else {
      for (const h of recent) {
        const icon = h.status === 'adopted' ? '✅' : h.status === 'reverted' ? '↩️' : '⏳'
        console.log(`  ${icon} ${h.paramKey}: ${h.originalValue}→${h.testValue} (${h.status})`)
      }
    }
    return true
  }

  if (m === 'bandit status' || m === '臂机状态') {
    if (Object.keys(banditState).length === 0) {
      console.log('[cc-soul][auto-tune] bandit state empty (not yet initialized)')
      return true
    }
    for (const [key, state] of Object.entries(banditState)) {
      const arms = state.arms.map((a, i) => {
        const marker = i === state.currentArm ? '*' : ' '
        const winRate = (a.alpha / (a.alpha + a.beta)).toFixed(2)
        return `${marker}[${i}] ${a.value} α=${a.alpha} β=${a.beta} p=${winRate} n=${a.pulls}`
      }).join('  ')
      console.log(`  ${key}: ${arms}`)
    }
    return true
  }

  if (m === '参数列表' || m === 'params' || m === 'tune params') {
    const lines = Object.entries(params)
      .map(([k, v]) => {
        const def = DEFAULT_PARAMS[k]
        const changed = def !== undefined && v !== def ? ` (默认: ${def})` : ''
        return `  ${k} = ${v}${changed}`
      })
    console.log(`[cc-soul][auto-tune] 当前参数:\n${lines.join('\n')}`)
    return true
  }

  // Manual override: "调参 key=value"
  const tuneMatch = m.match(/^调参\s+([\w.]+)\s*=\s*([\d.]+)$/)
  if (tuneMatch) {
    const key = tuneMatch[1]
    const value = parseFloat(tuneMatch[2])
    if (key in params && !isNaN(value)) {
      const old = params[key]
      setParam(key, value)
      notifyOwnerDM(`🔧 手动调参: ${key} = ${old} → ${value}`).catch(() => {}) // intentionally silent — notification
      return true
    }
  }

  // Reset: "重置参数 key"
  const resetMatch = m.match(/^重置参数\s+([\w.]+)$/)
  if (resetMatch && resetMatch[1] in DEFAULT_PARAMS) {
    resetParam(resetMatch[1])
    notifyOwnerDM(`🔄 已重置: ${resetMatch[1]} = ${DEFAULT_PARAMS[resetMatch[1]]}`).catch(() => {}) // intentionally silent — notification
    return true
  }

  return false
}

// ══════════════════════════════════════════════════════════════════════════════
// INIT
// ══════════════════════════════════════════════════════════════════════════════

loadTunableParams()
