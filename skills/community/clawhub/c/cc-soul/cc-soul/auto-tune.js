import { resolve } from "path";
import { DATA_DIR, loadJson, saveJson, debouncedSave } from "./persistence.ts";
import { notifyOwnerDM } from "./notify.ts";
import { computeEval } from "./quality.ts";
const PARAMS_PATH = resolve(DATA_DIR, "tunable_params.json");
const TUNE_STATE_PATH = resolve(DATA_DIR, "auto_tune_state.json");
const DEFAULT_PARAMS = {
  // memory.ts
  "memory.recall_top_n": 3,
  "memory.age_decay_rate": 0.02,
  "memory.consolidation_cooldown_hours": 24,
  "memory.session_summary_cooldown_min": 30,
  "memory.contradiction_scan_cooldown_hours": 24,
  // body.ts
  "body.energy_recovery_per_min": 0.015,
  "body.alertness_decay_per_min": 8e-3,
  "body.alertness_recovery_per_min": 5e-3,
  "body.load_decay_per_min": 0.02,
  "body.mood_decay_factor": 0.995,
  "body.correction_alertness_boost": 0.2,
  "body.correction_mood_penalty": 0.1,
  "body.positive_energy_boost": 0.05,
  "body.positive_mood_boost": 0.08,
  "body.positive_anomaly_reduction": 0.05,
  "body.resilience": 0.3,
  "body.message_energy_base_cost": 0.02,
  "body.message_energy_complexity_cost": 0.03,
  "body.message_load_base": 0.1,
  "body.message_load_complexity": 0.15,
  "body.correction_anomaly_boost": 0.15,
  "body.anomaly_decay_per_min": 0.01,
  // cognition.ts
  "cognition.casual_max_length": 15,
  "cognition.quick_intent_max_length": 20,
  "cognition.detailed_min_length": 200,
  // quality.ts
  "quality.medium_length_bonus": 0.5,
  "quality.long_length_bonus": 0.5,
  "quality.reasoning_bonus": 1,
  "quality.code_bonus": 0.5,
  "quality.ai_exposure_penalty": 2,
  "quality.relevance_weight": 1.5,
  // activation-field.ts — 聚合查询检测
  "recall.aggregation_dropoff": 0.3,
  // flow.ts
  "flow.frustration_shortening_rate": 0.2,
  "flow.frustration_terse": 0.15,
  "flow.frustration_keyword_rate": 0.3,
  "flow.frustration_question_rate": 0.1,
  "flow.frustration_repetition": 0.15,
  "flow.frustration_decay_per_turn": 0.05,
  "flow.stuck_threshold": 0.5,
  // prompt-builder.ts
  "prompt.augment_budget": 3500,
  // evolution.ts
  "evolution.hypothesis_verify_threshold": 5,
  "evolution.hypothesis_reject_threshold": 3,
  "evolution.max_rules": 50,
  // inner-life.ts
  "inner.journal_cooldown_min": 30,
  "inner.reflection_cooldown_hours": 24,
  // memory.ts — fusion weights
  "memory.fusion_text_weight": 0.5,
  "memory.fusion_vec_weight": 0.5,
  "memory.fusion_multi_source_boost": 1.3,
  // memory.ts — recall scoring
  "memory.trigram_dedup_threshold": 0.7,
  "memory.bm25_k1": 1.2,
  "memory.bm25_b": 0.75,
  "memory.time_decay_halflife_days": 90,
  // evolution.ts — hypothesis thresholds
  "evolution.rule_dedup_threshold": 0.45,
  "evolution.hypothesis_verify_ci_lb": 0.6,
  "evolution.hypothesis_reject_ci_ub": 0.4,
  "evolution.hypothesis_match_min_sim": 0.2,
  "evolution.reflexion_sim_threshold": 0.3,
  // body.ts — emotional contagion
  "body.contagion_max_shift": 0.15,
  // graph.ts — stale entity threshold
  "graph.stale_days": 90,
  // persona.ts — blend thresholds
  "persona.blend_gap_threshold": 0.3,
  "persona.attention_trigger_bonus": 0.2,
  // smart-forget — Weibull k (shape) per scope
  "forget.weibull_k_fact": 1.2,
  "forget.weibull_k_preference": 0.9,
  "forget.weibull_k_episode": 1.4,
  // smart-forget — Weibull lambda (scale) per scope
  "forget.weibull_lambda_fact": 30,
  "forget.weibull_lambda_preference": 90,
  "forget.weibull_lambda_episode": 14,
  // smart-forget — ACT-R & thresholds
  "forget.act_r_decay": 0.5,
  "forget.survival_threshold": 0.1,
  "forget.activation_threshold": -1,
  "forget.consolidation_threshold_survival": 0.8,
  "forget.consolidation_threshold_activation": 2,
  // recall — weighted log-sum weights
  "recall.w_sim": 3,
  "recall.w_recency": 1.5,
  "recall.w_scope": 1,
  "recall.w_emotion": 0.8,
  "recall.w_user": 0.8,
  "recall.w_confidence": 1,
  "recall.w_mood": 0.5,
  // lifecycle — cooldowns (hours)
  "lifecycle.consolidation_cooldown_hours": 24,
  "lifecycle.distill_l1_hours": 6,
  "lifecycle.distill_l2_hours": 12,
  "lifecycle.decay_scan_hours": 6,
  // capacity limits
  "capacity.core_memory_max": 100,
  "capacity.working_memory_max": 20,
  "capacity.entity_max": 800,
  "capacity.relation_max": 1600,
  "capacity.augment_budget": 3500,
  // 遗忘模型（smart-forget 相关）
  "forget.ema_alpha": 0.05,
  "forget.lambda_max_multiplier": 3,
  "forget.recall_increment_percent": 15,
  "forget.emotion_high_multiplier": 2,
  "forget.emotion_medium_multiplier": 1.5,
  "forget.max_per_sweep": 20,
  "forget.actr_max_iterations": 50,
  // 召回 boost 系数
  "recall.scope_boost_preference": 1.3,
  "recall.scope_boost_correction": 1.5,
  "recall.emotion_boost_important": 1.4,
  "recall.emotion_boost_painful": 1.3,
  "recall.emotion_boost_warm": 1.2,
  "recall.user_boost_same": 2,
  "recall.user_boost_other": 0.7,
  "recall.tier_weight_hot": 1.5,
  "recall.tier_weight_warm": 1,
  "recall.tier_weight_cool": 0.8,
  "recall.tier_weight_cold": 0.5,
  "recall.consolidated_boost": 1.5,
  "recall.reflexion_boost": 2,
  "recall.flashbulb_high": 1.6,
  "recall.flashbulb_medium": 1.2,
  "recall.mmr_lambda": 0.7,
  // 生命周期
  "lifecycle.recall_feedback_cooldown_ms": 6e4,
  "lifecycle.association_cooldown_ms": 3e4,
  "lifecycle.session_summary_cooldown_ms": 18e5,
  "lifecycle.contradiction_scan_cooldown_ms": 864e5,
  "lifecycle.decay_cooldown_ms": 216e5,
  "lifecycle.max_insights": 20,
  "lifecycle.max_episodes": 200,
  // 容量
  "memory.max_memories": 1e4,
  "memory.max_history": 100,
  "memory.inject_history": 30,
  "memory.trigram_cache_max": 2e3,
  // 认知
  "cognition.correction_weight": 3,
  "cognition.emotion_weight": 2,
  "cognition.tech_weight": 2,
  // 其他
  "persona.cooldown_ms": 12e4,
  "quality.repetition_sim_threshold": 0.7,
  "metacognition.conflict_threshold": 0.3,
  "metacognition.min_samples": 5
};
let params = { ...DEFAULT_PARAMS };
function loadTunableParams() {
  const saved = loadJson(PARAMS_PATH, {});
  params = { ...DEFAULT_PARAMS, ...saved };
  saveJson(PARAMS_PATH, params);
}
function getParam(key) {
  return params[key] ?? DEFAULT_PARAMS[key] ?? 0;
}
function setParam(key, value) {
  params[key] = value;
  debouncedSave(PARAMS_PATH, params);
}
function resetParam(key) {
  params[key] = DEFAULT_PARAMS[key] ?? 0;
  debouncedSave(PARAMS_PATH, params);
}
let tuneState = loadJson(TUNE_STATE_PATH, {
  currentExperiment: null,
  history: [],
  lastTuneCheck: 0,
  paramQueue: []
});
function saveTuneState() {
  debouncedSave(TUNE_STATE_PATH, tuneState);
}
const BANDIT_STATE_PATH = resolve(DATA_DIR, "bandit_state.json");
let banditState = {};
const CTX_BANDIT_PATH = resolve(DATA_DIR, "ctx_bandit_state.json");
let ctxBanditState = { arms: {} };
function loadCtxBanditState() {
  ctxBanditState = loadJson(CTX_BANDIT_PATH, { arms: {} });
}
function saveCtxBanditState() {
  debouncedSave(CTX_BANDIT_PATH, ctxBanditState);
}
function buildContextKey(timeSlot, domain, mood) {
  const ts = timeSlot || getTimeSlot((/* @__PURE__ */ new Date()).getHours());
  const d = domain || "general";
  const m = mood || "neutral";
  return `${ts}:${d}:${m}`;
}
function getTimeSlot(hour) {
  if (hour >= 6 && hour < 12) return "morning";
  if (hour >= 12 && hour < 18) return "afternoon";
  if (hour >= 18 && hour < 23) return "evening";
  return "night";
}
function selectArmContextual(state, ctxKey) {
  const ctxArms = ctxBanditState.arms[state.key];
  if (ctxArms) {
    const matching = ctxArms.filter((a) => a.contextKey === ctxKey);
    if (matching.length >= state.arms.length) {
      const totalPulls = matching.reduce((s, a) => s + a.alpha + a.beta - 2, 0);
      if (totalPulls >= 5) {
        let bestIdx = 0, bestSample = -1;
        for (let i = 0; i < Math.min(matching.length, state.arms.length); i++) {
          const sample = betaSample(matching[i].alpha, matching[i].beta);
          if (sample > bestSample) {
            bestSample = sample;
            bestIdx = i;
          }
        }
        return bestIdx;
      }
    }
  }
  return selectArm(state);
}
function updateCtxBanditReward(paramKey, armIdx, reward, ctxKey) {
  if (!ctxBanditState.arms[paramKey]) ctxBanditState.arms[paramKey] = [];
  const arms = ctxBanditState.arms[paramKey];
  while (arms.filter((a) => a.contextKey === ctxKey).length < (banditState[paramKey]?.arms.length || 3)) {
    arms.push({ contextKey: ctxKey, alpha: 1, beta: 1 });
  }
  const matching = arms.filter((a) => a.contextKey === ctxKey);
  if (armIdx < matching.length) {
    const REWARD_SCALE = 5;
    matching[armIdx].alpha += reward * REWARD_SCALE;
    matching[armIdx].beta += (1 - reward) * REWARD_SCALE;
    const DISCOUNT_FACTOR = 0.995;
    const ctxArm = matching[armIdx];
    ctxArm.alpha *= DISCOUNT_FACTOR;
    ctxArm.beta *= DISCOUNT_FACTOR;
    if (ctxArm.alpha + ctxArm.beta < 2) {
      ctxArm.alpha = Math.max(ctxArm.alpha, 1);
      ctxArm.beta = Math.max(ctxArm.beta, 1);
    }
  }
  if (arms.length > 200) {
    const sorted = arms.sort((a, b) => a.alpha + a.beta - (b.alpha + b.beta));
    ctxBanditState.arms[paramKey] = sorted.slice(-150);
  }
}
let _currentCtxKey = "afternoon:general:neutral";
function randn() {
  const u1 = Math.random(), u2 = Math.random();
  return Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
}
function gammaSample(shape) {
  shape = Math.max(0.01, shape);
  if (shape < 1) return gammaSample(shape + 1) * Math.pow(Math.random(), 1 / shape);
  const d = shape - 1 / 3;
  const c = 1 / Math.sqrt(9 * d);
  while (true) {
    let x, v;
    do {
      x = randn();
      v = 1 + c * x;
    } while (v <= 0);
    v = v * v * v;
    const u = Math.random();
    if (u < 1 - 0.0331 * x * x * x * x) return d * v;
    if (Math.log(u) < 0.5 * x * x + d * (1 - v + Math.log(v))) return d * v;
  }
}
function betaSample(alpha, beta) {
  const safeAlpha = Math.max(0.01, alpha);
  const safeBeta = Math.max(0.01, beta);
  const x = gammaSample(safeAlpha);
  const y = gammaSample(safeBeta);
  return x / (x + y);
}
function selectArm(state) {
  let bestIdx = state.currentArm, bestSample = -1;
  for (let i = 0; i < state.arms.length; i++) {
    const sample = betaSample(state.arms[i].alpha, state.arms[i].beta);
    if (sample > bestSample) {
      bestSample = sample;
      bestIdx = i;
    }
  }
  return bestIdx;
}
function isIntegerParam(key) {
  return key.includes("cooldown") || key.includes("threshold") || key.includes("max_") || key.includes("top_n") || key.includes("min_");
}
function initBanditForParam(key) {
  const defaultVal = DEFAULT_PARAMS[key];
  if (defaultVal === void 0) return null;
  const multipliers = [0.8, 1, 1.2];
  const isInt = isIntegerParam(key);
  return {
    key,
    arms: multipliers.map((m) => ({
      value: isInt ? Math.max(1, Math.round(defaultVal * m)) : Math.max(1e-3, +(defaultVal * m).toFixed(4)),
      alpha: 1,
      // uniform prior
      beta: 1,
      pulls: 0
    })),
    currentArm: 1,
    // index 1 = 1.0x = default value
    totalPulls: 0,
    phase: 1
  };
}
const PHASE2_THRESHOLD = 30;
function maybePromoteToPhase2(state) {
  if (state.phase === 2) return false;
  const winnerArm = state.arms.reduce(
    (best, arm, i) => arm.pulls > best.pulls ? { ...arm, idx: i, pulls: arm.pulls } : best,
    { idx: 0, pulls: 0, value: 0, alpha: 1, beta: 1 }
  );
  if (winnerArm.pulls < PHASE2_THRESHOLD) return false;
  const winRates = state.arms.map((a) => a.alpha / (a.alpha + a.beta));
  const bestIdx = winRates.indexOf(Math.max(...winRates));
  if (state.arms[bestIdx].pulls < PHASE2_THRESHOLD) return false;
  const defaultVal = DEFAULT_PARAMS[state.key];
  if (defaultVal === void 0) return false;
  const winnerMultiplier = state.arms[bestIdx].value / defaultVal;
  let phase2Multipliers;
  if (winnerMultiplier >= 1.15) {
    phase2Multipliers = [1.1, 1.2, 1.3];
  } else if (winnerMultiplier <= 0.85) {
    phase2Multipliers = [0.7, 0.8, 0.9];
  } else {
    phase2Multipliers = [0.9, 1, 1.1];
  }
  const isInt = isIntegerParam(state.key);
  state.arms = phase2Multipliers.map((m) => ({
    value: isInt ? Math.max(1, Math.round(defaultVal * m)) : Math.max(1e-3, +(defaultVal * m).toFixed(4)),
    alpha: 1,
    beta: 1,
    pulls: 0
  }));
  state.currentArm = 1;
  state.phase = 2;
  state.winnerMultiplier = winnerMultiplier;
  state.totalPulls = 0;
  console.log(`[cc-soul][auto-tune] ${state.key} promoted to Phase 2: winner=${winnerMultiplier.toFixed(2)}x \u2192 refine [${phase2Multipliers}]`);
  return true;
}
function loadBanditState() {
  banditState = loadJson(BANDIT_STATE_PATH, {});
  for (const state of Object.values(banditState)) {
    if (!state.phase) state.phase = state.arms.length <= 3 ? 1 : 1;
  }
  loadCtxBanditState();
  console.log(`[cc-soul][auto-tune] bandit state loaded: ${Object.keys(banditState).length} params tracked, ctx bins: ${Object.keys(ctxBanditState.arms).length}`);
}
function saveBanditState() {
  debouncedSave(BANDIT_STATE_PATH, banditState);
}
const HIGH_IMPACT_PARAMS = [
  "memory.recall_top_n",
  "memory.age_decay_rate",
  "body.energy_recovery_per_min",
  "body.resilience",
  "body.mood_decay_factor",
  "quality.reasoning_bonus",
  "quality.relevance_weight",
  "flow.stuck_threshold",
  "flow.frustration_decay_per_turn",
  "prompt.augment_budget",
  "voice.impulse_threshold",
  "evolution.hypothesis_verify_threshold",
  "memory.trigram_dedup_threshold",
  "memory.bm25_k1",
  "evolution.rule_dedup_threshold",
  "body.contagion_max_shift",
  "graph.stale_days",
  // forget & recall — high impact on memory quality
  "forget.weibull_lambda_fact",
  "forget.weibull_lambda_episode",
  "forget.survival_threshold",
  "recall.w_sim",
  "recall.w_recency"
];
const TUNE_CHECK_INTERVAL = 864e5;
function checkAutoTune(stats) {
  const now = Date.now();
  if (tuneState.currentExperiment) {
    const exp = tuneState.currentExperiment;
    if (now >= exp.endsAt) {
      evaluateLegacyExperiment(stats);
    }
    return;
  }
  if (now - tuneState.lastTuneCheck < TUNE_CHECK_INTERVAL) return;
  if (stats.totalMessages < 50) return;
  tuneState.lastTuneCheck = now;
  if (Object.keys(banditState).length === 0) {
    loadBanditState();
  }
  const allKeys = Object.keys(DEFAULT_PARAMS).filter((k) => !k.startsWith("quality."));
  const exploreCount = 2;
  for (const key of allKeys) {
    if (!banditState[key]) {
      const state = initBanditForParam(key);
      if (state) banditState[key] = state;
    }
  }
  const candidates = allKeys.filter((key) => banditState[key]).map((key) => ({ key, pulls: banditState[key].totalPulls })).sort((a, b) => a.pulls - b.pulls);
  const highImpact = candidates.filter((c) => HIGH_IMPACT_PARAMS.includes(c.key));
  const others = candidates.filter((c) => !HIGH_IMPACT_PARAMS.includes(c.key));
  const toExplore = [];
  for (const c of [...highImpact, ...others]) {
    if (toExplore.length >= exploreCount) break;
    toExplore.push(c.key);
  }
  for (const key of toExplore) {
    const state = banditState[key];
    if (!state) continue;
    const armIdx = selectArmContextual(state, _currentCtxKey);
    state.currentArm = armIdx;
    setParam(key, state.arms[armIdx].value);
    console.log(`[cc-soul][auto-tune] bandit explore: ${key} \u2192 arm[${armIdx}] = ${state.arms[armIdx].value} (ctx=${_currentCtxKey}, pulls=${state.totalPulls})`);
  }
  saveBanditState();
  saveTuneState();
}
function updateBanditReward(qualityScore, wasCorrection, bodyResonance, engagementSignal) {
  if (Object.keys(banditState).length === 0) return;
  const qualityReward = Math.max(0, Math.min(1, (qualityScore - 1) / 9));
  const bodyReward = bodyResonance ?? 0.5;
  const engReward = engagementSignal ?? 0.5;
  let successProb = qualityReward * 0.5 + bodyReward * 0.2 + engReward * 0.3;
  if (wasCorrection) {
    successProb = Math.min(successProb, 0.2);
  }
  const reward = Math.max(0, Math.min(1, successProb));
  const REWARD_SCALE = 5;
  for (const [key, state] of Object.entries(banditState)) {
    const armIdx = state.currentArm;
    if (armIdx < 0 || armIdx >= state.arms.length) continue;
    state.arms[armIdx].pulls++;
    state.totalPulls++;
    state.arms[armIdx].alpha += reward * REWARD_SCALE;
    state.arms[armIdx].beta += (1 - reward) * REWARD_SCALE;
    const DISCOUNT_FACTOR = 0.995;
    const arm = state.arms[armIdx];
    arm.alpha *= DISCOUNT_FACTOR;
    arm.beta *= DISCOUNT_FACTOR;
    if (arm.alpha + arm.beta < 2) {
      arm.alpha = Math.max(arm.alpha, 1);
      arm.beta = Math.max(arm.beta, 1);
    }
    updateCtxBanditReward(key, armIdx, reward, _currentCtxKey);
    if (state.phase === 1) maybePromoteToPhase2(state);
  }
  saveBanditState();
  saveCtxBanditState();
}
function evaluateLegacyExperiment(stats) {
  const exp = tuneState.currentExperiment;
  if (!exp) return;
  const currentEval = computeEval(stats.totalMessages, stats.corrections);
  const windowMessages = stats.totalMessages - exp.preMetrics.messages;
  exp.postMetrics = {
    avgQuality: currentEval.avgQuality,
    correctionRate: currentEval.correctionRate,
    messages: windowMessages
  };
  if (windowMessages < 10) {
    exp.status = "insufficient_data";
    setParam(exp.paramKey, exp.originalValue);
    notifyOwnerDM(
      `\u23F3 \u8C03\u53C2\u5B9E\u9A8C\u6570\u636E\u4E0D\u8DB3\uFF08${windowMessages} \u6761\u6D88\u606F\uFF09\uFF0C\u5DF2\u6062\u590D ${exp.paramKey} = ${exp.originalValue}`
    ).catch(() => {
    });
  } else {
    const qualityDelta = currentEval.avgQuality - exp.preMetrics.avgQuality;
    const correctionDelta = currentEval.correctionRate - exp.preMetrics.correctionRate;
    const improved = qualityDelta > 0.2 || correctionDelta < -2;
    const regressed = qualityDelta < -0.5 || correctionDelta > 3;
    if (improved && !regressed) {
      exp.status = "adopted";
      notifyOwnerDM(
        `\u2705 \u8C03\u53C2\u5B9E\u9A8C\u6210\u529F\uFF01
\u53C2\u6570: ${exp.paramKey}
${exp.originalValue} \u2192 ${exp.testValue} (\u5DF2\u91C7\u7528)
\u8D28\u91CF: ${exp.preMetrics.avgQuality.toFixed(1)} \u2192 ${currentEval.avgQuality.toFixed(1)} (${qualityDelta >= 0 ? "+" : ""}${qualityDelta.toFixed(1)})
\u7EA0\u6B63\u7387: ${exp.preMetrics.correctionRate.toFixed(1)}% \u2192 ${currentEval.correctionRate.toFixed(1)}%`
      ).catch(() => {
      });
    } else {
      exp.status = "reverted";
      setParam(exp.paramKey, exp.originalValue);
      notifyOwnerDM(
        `\u21A9\uFE0F \u8C03\u53C2\u5B9E\u9A8C\u672A\u6539\u5584\uFF0C\u5DF2\u6062\u590D
\u53C2\u6570: ${exp.paramKey} = ${exp.originalValue}
\u8D28\u91CF: ${qualityDelta >= 0 ? "+" : ""}${qualityDelta.toFixed(1)}, \u7EA0\u6B63\u7387: ${correctionDelta >= 0 ? "+" : ""}${correctionDelta.toFixed(1)}%`
      ).catch(() => {
      });
    }
  }
  tuneState.history.push({ ...exp });
  if (tuneState.history.length > 100) tuneState.history = tuneState.history.slice(-100);
  tuneState.currentExperiment = null;
  saveTuneState();
  console.log(`[cc-soul][auto-tune] legacy experiment ended: ${exp.paramKey} \u2192 ${exp.status}`);
}
function handleTuneCommand(msg) {
  const m = msg.trim();
  if (m === "tune" || m === "\u8C03\u6574") {
    const tracked = Object.keys(banditState).length;
    const totalPulls = Object.values(banditState).reduce((s, st) => s + (st.totalPulls || 0), 0);
    console.log(`[cc-soul][auto-tune] status: ${tracked} params, ${totalPulls} pulls`);
    return true;
  }
  if (m === "\u8C03\u53C2\u72B6\u6001" || m === "tune status") {
    const exp = tuneState.currentExperiment;
    if (exp) {
      const daysLeft = Math.ceil((exp.endsAt - Date.now()) / 864e5);
      console.log(`[cc-soul][auto-tune] legacy experiment running: ${exp.paramKey} ${exp.originalValue}\u2192${exp.testValue}, ${daysLeft}d left`);
    }
    const tracked = Object.keys(banditState).length;
    if (tracked > 0) {
      const totalPulls = Object.values(banditState).reduce((s, st) => s + st.totalPulls, 0);
      console.log(`[cc-soul][auto-tune] bandit: ${tracked} params tracked, ${totalPulls} total pulls`);
      const sorted = Object.values(banditState).filter((st) => st.totalPulls > 0).sort((a, b) => b.totalPulls - a.totalPulls).slice(0, 5);
      for (const st of sorted) {
        const bestArm = st.arms.reduce(
          (best, arm, i) => arm.alpha / (arm.alpha + arm.beta) > best.ratio ? { idx: i, ratio: arm.alpha / (arm.alpha + arm.beta) } : best,
          { idx: 0, ratio: 0 }
        );
        const current = st.arms[st.currentArm];
        console.log(`  ${st.key}: arm[${st.currentArm}]=${current.value} (pulls=${st.totalPulls}, best=arm[${bestArm.idx}] p=${bestArm.ratio.toFixed(2)})`);
      }
    } else {
      console.log(`[cc-soul][auto-tune] bandit: not yet initialized`);
    }
    return true;
  }
  if (m === "\u8C03\u53C2\u5386\u53F2" || m === "tune history") {
    const recent = tuneState.history.slice(-10);
    if (recent.length === 0) {
      console.log("[cc-soul][auto-tune] \u65E0\u5386\u53F2\u8BB0\u5F55");
    } else {
      for (const h of recent) {
        const icon = h.status === "adopted" ? "\u2705" : h.status === "reverted" ? "\u21A9\uFE0F" : "\u23F3";
        console.log(`  ${icon} ${h.paramKey}: ${h.originalValue}\u2192${h.testValue} (${h.status})`);
      }
    }
    return true;
  }
  if (m === "bandit status" || m === "\u81C2\u673A\u72B6\u6001") {
    if (Object.keys(banditState).length === 0) {
      console.log("[cc-soul][auto-tune] bandit state empty (not yet initialized)");
      return true;
    }
    for (const [key, state] of Object.entries(banditState)) {
      const arms = state.arms.map((a, i) => {
        const marker = i === state.currentArm ? "*" : " ";
        const winRate = (a.alpha / (a.alpha + a.beta)).toFixed(2);
        return `${marker}[${i}] ${a.value} \u03B1=${a.alpha} \u03B2=${a.beta} p=${winRate} n=${a.pulls}`;
      }).join("  ");
      console.log(`  ${key}: ${arms}`);
    }
    return true;
  }
  if (m === "\u53C2\u6570\u5217\u8868" || m === "params" || m === "tune params") {
    const lines = Object.entries(params).map(([k, v]) => {
      const def = DEFAULT_PARAMS[k];
      const changed = def !== void 0 && v !== def ? ` (\u9ED8\u8BA4: ${def})` : "";
      return `  ${k} = ${v}${changed}`;
    });
    console.log(`[cc-soul][auto-tune] \u5F53\u524D\u53C2\u6570:
${lines.join("\n")}`);
    return true;
  }
  const tuneMatch = m.match(/^调参\s+([\w.]+)\s*=\s*([\d.]+)$/);
  if (tuneMatch) {
    const key = tuneMatch[1];
    const value = parseFloat(tuneMatch[2]);
    if (key in params && !isNaN(value)) {
      const old = params[key];
      setParam(key, value);
      notifyOwnerDM(`\u{1F527} \u624B\u52A8\u8C03\u53C2: ${key} = ${old} \u2192 ${value}`).catch(() => {
      });
      return true;
    }
  }
  const resetMatch = m.match(/^重置参数\s+([\w.]+)$/);
  if (resetMatch && resetMatch[1] in DEFAULT_PARAMS) {
    resetParam(resetMatch[1]);
    notifyOwnerDM(`\u{1F504} \u5DF2\u91CD\u7F6E: ${resetMatch[1]} = ${DEFAULT_PARAMS[resetMatch[1]]}`).catch(() => {
    });
    return true;
  }
  return false;
}
loadTunableParams();
export {
  checkAutoTune,
  getParam,
  handleTuneCommand,
  loadTunableParams,
  resetParam,
  setParam,
  updateBanditReward
};
