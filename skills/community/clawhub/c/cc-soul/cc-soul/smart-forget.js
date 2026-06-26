import { resolve } from "path";
import { existsSync } from "fs";
import { getParam } from "./auto-tune.ts";
import { trigrams, trigramSimilarity, detectPolarityFlip, WORD_PATTERN, TRIGRAM_THRESHOLD } from "./memory-utils.ts";
import { loadJson } from "./persistence.ts";
import { logDecision } from "./decision-log.ts";
import { emitCacheEvent } from "./memory-utils.ts";
const FSRS_W = [0.4, 0.6, 2.4, 5.8, 4.93, 0.94, 0.86, 0.01, 1.49, 0.14, 0.94, 2.18, 0.05, 0.34, 1.26, 0.29, 2.61, 0.12, 0.1];
function fsrsRetrievability(elapsedDays, stability) {
  if (stability <= 0 || !isFinite(stability)) return 1;
  if (elapsedDays <= 0) return 1;
  return Math.pow(1 + elapsedDays / (9 * stability), -1);
}
function fsrsUpdate(state, rating, elapsedDays) {
  const s = { ...state };
  const r = fsrsRetrievability(elapsedDays, s.stability);
  if (rating >= 3) {
    const growthFactor = 1 + Math.exp(FSRS_W[8]) * (11 - s.difficulty * 10) * Math.pow(s.stability, -FSRS_W[9]) * (Math.exp((1 - r) * FSRS_W[10]) - 1);
    s.stability = Math.max(0.1, s.stability * growthFactor);
    s.reps++;
    s.difficulty = Math.max(0, Math.min(1, s.difficulty - 0.02 * (rating - 2)));
  } else {
    s.stability = Math.max(0.1, s.stability * Math.pow(FSRS_W[11], s.difficulty * 10 - 1));
    s.lapses++;
    s.reps++;
    s.difficulty = Math.max(0, Math.min(1, s.difficulty + 0.1 * (2 - rating)));
  }
  try {
    const { dbAddFSRSTraining } = require("./sqlite-store.ts");
    dbAddFSRSTraining(elapsedDays, state.stability, rating >= 3);
  } catch {
  }
  return s;
}
function fsrsInit(scope) {
  const difficultyMap = {
    correction: 0.1,
    fact: 0.3,
    preference: 0.25,
    episode: 0.4,
    emotion: 0.5
  };
  return {
    stability: scope === "correction" ? 365 : 1,
    // 1 day initial stability (corrections: 1 year)
    difficulty: difficultyMap[scope || "fact"] ?? 0.3,
    reps: 0,
    lapses: 0
  };
}
function bcmAdaptiveThreshold(baseThreshold, recentActivityLevel) {
  const meanActivity = 0.3;
  const alpha = 0.5;
  const shift = alpha * (recentActivityLevel - meanActivity);
  return Math.max(0.05, Math.min(0.3, baseThreshold + shift));
}
const MS_PER_DAY = 864e5;
const WEIBULL_K_DEFAULT = {
  fact: 1.2,
  preference: 0.9,
  episode: 1.4,
  correction: Infinity
  // corrections never decay
};
function getWeibullK(scope) {
  const s = scope || "fact";
  if (_decayParams.scopeK && _decayParams.scopeK[s] !== void 0) return _decayParams.scopeK[s];
  const paramKey = `forget.weibull_k_${s}`;
  const tuned = getParam(paramKey);
  if (tuned > 0) return tuned;
  return WEIBULL_K_DEFAULT[s] ?? getParam("forget.weibull_k_fact");
}
const WEIBULL_K = 1.2;
function getWeibullLambda(scope) {
  if (scope === "correction") return Infinity;
  const paramKey = `forget.weibull_lambda_${scope}`;
  const tuned = getParam(paramKey);
  if (tuned > 0) return tuned;
  const LEGACY_LAMBDA = { emotion: 7 };
  return LEGACY_LAMBDA[scope] ?? getParam("forget.weibull_lambda_fact");
}
function getActRDecay() {
  return getParam("forget.act_r_decay");
}
function getSurvivalForgetThreshold() {
  return getParam("forget.survival_threshold");
}
function getActivationForgetThreshold() {
  return getParam("forget.activation_threshold");
}
function getSurvivalConsolidateThreshold() {
  return getParam("forget.consolidation_threshold_survival");
}
function getActivationConsolidateThreshold() {
  return getParam("forget.consolidation_threshold_activation");
}
const DECAY_PARAMS_FILENAME = "decay_params.json";
let _decayParams = { recallHits: 0, recallMisses: 0, lambdaMultiplier: 1, lastAdjustTs: 0 };
let _decayParamsPath = "";
function loadDecayParams(dataDir) {
  _decayParamsPath = resolve(dataDir, DECAY_PARAMS_FILENAME);
  try {
    const sqlMod = require("./sqlite-store.ts");
    if (sqlMod?.dbLoadDecayParams) {
      const loaded = sqlMod.dbLoadDecayParams(null);
      if (loaded) {
        Object.assign(_decayParams, loaded);
        return;
      }
    }
  } catch {
  }
  try {
    const loaded = loadJson(_decayParamsPath, null);
    if (loaded) Object.assign(_decayParams, loaded);
  } catch {
  }
}
function saveDecayParams() {
  try {
    const sqlMod = require("./sqlite-store.ts");
    if (sqlMod?.dbSaveDecayParams) sqlMod.dbSaveDecayParams(_decayParams);
  } catch {
  }
}
function getEMAAlpha() {
  return getParam("forget.ema_alpha");
}
function clampMultiplier(v) {
  return Math.max(0.5, Math.min(2, v));
}
function recordRecallHit(scope, mem) {
  _decayParams.recallHits++;
  _decayParams.lambdaMultiplier = clampMultiplier(
    _decayParams.lambdaMultiplier * (1 - getEMAAlpha()) + 1.05 * getEMAAlpha()
  );
  if (scope && _decayParams.scopeK && _decayParams.scopeK[scope] !== void 0) {
    const kTarget = (WEIBULL_K_DEFAULT[scope] ?? 1.2) * 0.97;
    _decayParams.scopeK[scope] = _decayParams.scopeK[scope] * (1 - getEMAAlpha()) + kTarget * getEMAAlpha();
  }
  _decayParams.lastAdjustTs = Date.now();
  saveDecayParams();
}
function recordRecallMiss(scope, mem) {
  _decayParams.recallMisses++;
  _decayParams.lambdaMultiplier = clampMultiplier(
    _decayParams.lambdaMultiplier * (1 - getEMAAlpha()) + 0.95 * getEMAAlpha()
  );
  if (scope && _decayParams.scopeK && _decayParams.scopeK[scope] !== void 0) {
    const kDefault = WEIBULL_K_DEFAULT[scope] ?? 1.2;
    _decayParams.scopeK[scope] = _decayParams.scopeK[scope] * (1 - getEMAAlpha()) + kDefault * 1.03 * getEMAAlpha();
  }
  _decayParams.lastAdjustTs = Date.now();
  saveDecayParams();
}
function getLambdaMultiplier() {
  return _decayParams.lambdaMultiplier;
}
function weibullSurvival(ageDays, lambda, k) {
  if (!isFinite(lambda)) return 1;
  if (ageDays <= 0) return 1;
  if (lambda <= 0) return 0;
  return Math.exp(-Math.pow(ageDays / lambda, k));
}
function effectiveLambda(scope, recallCount, emotionIntensity) {
  const baseLambda = getWeibullLambda(scope);
  if (!isFinite(baseLambda)) return Infinity;
  const recallMultiplier = Math.min(1 + recallCount * getParam("forget.recall_increment_percent") / 100, getParam("forget.lambda_max_multiplier"));
  const ei = emotionIntensity ?? 0;
  const emotionAlpha = 1.5;
  const emotionBeta = 2;
  const emotionMultiplier = 1 + emotionAlpha * Math.pow(ei, emotionBeta);
  return baseLambda * recallMultiplier * emotionMultiplier * _decayParams.lambdaMultiplier;
}
function actRActivation(mem, now) {
  const n = Math.max(mem.recallCount, 1);
  const createdAgo = Math.max((now - mem.ts) / 1e3, 1);
  const lastAgo = Math.max((now - mem.lastAccessed) / 1e3, 1);
  let sum = 0;
  if (n === 1) {
    sum = Math.pow(lastAgo, -getActRDecay());
  } else {
    const cap = Math.min(n, getParam("forget.actr_max_iterations"));
    for (let i = 0; i < cap; i++) {
      const fraction = cap === 1 ? 1 : i / (cap - 1);
      const accessAgo = createdAgo - fraction * (createdAgo - lastAgo);
      const t = Math.max(accessAgo, 1);
      sum += Math.pow(t, -getActRDecay());
    }
  }
  return sum > 0 ? Math.log(sum) : -Infinity;
}
function ensureFSRS(mem) {
  if (mem.fsrs) return mem.fsrs;
  const ageDays = (Date.now() - (mem.ts || Date.now())) / MS_PER_DAY;
  const scope = mem.scope || "fact";
  let stability = scope === "correction" ? 365 : scope === "preference" ? 60 : scope === "episode" ? 7 : 30;
  let difficulty = scope === "correction" ? 1 : scope === "preference" ? 3 : scope === "episode" ? 7 : 5;
  const recalls = mem.recallCount || 0;
  if (recalls > 0) stability *= 1 + recalls * 0.3;
  return { stability, difficulty };
}
let _memoryStateMod = null;
function semanticInterference(memContent) {
  if (!_memoryStateMod) {
    try {
      _memoryStateMod = require("./memory.ts");
    } catch {
      return 1;
    }
  }
  const allMems = _memoryStateMod?.memoryState?.memories;
  if (!allMems || allMems.length < 5) return 1;
  const memTri = trigrams(memContent);
  if (memTri.size === 0) return 1;
  let totalSim = 0;
  let count = 0;
  let contradictionPenalty = 0;
  const memWords = new Set((memContent.match(WORD_PATTERN.CJK2_EN3) || []).map((w) => w.toLowerCase()));
  const recent = allMems.slice(-100);
  for (const other of recent) {
    if (!other || other.scope === "expired" || other.content === memContent) continue;
    const otherTri = trigrams(other.content);
    const sim = trigramSimilarity(memTri, otherTri);
    if (sim < 0.15) continue;
    const otherWords = (other.content.match(WORD_PATTERN.CJK2_EN3) || []).map((w) => w.toLowerCase());
    let newWordCount = 0;
    for (const w of otherWords) {
      if (!memWords.has(w)) newWordCount++;
    }
    const infoGain = otherWords.length > 0 ? newWordCount / otherWords.length : 0;
    totalSim += sim * (1 - infoGain * 0.5);
    count++;
    if (detectPolarityFlip(memContent, other.content)) contradictionPenalty += 0.2;
  }
  if (count === 0) return 1;
  const avgSim = totalSim / count;
  const clustering = avgSim * Math.log1p(count) + contradictionPenalty;
  return 1 / (1 + clustering * 0.3);
}
function computeForgetScore(mem) {
  const now = Date.now();
  const ageDays = (now - mem.ts) / MS_PER_DAY;
  const fsrs = ensureFSRS(mem);
  const interference = semanticInterference(mem.content || "");
  const effectiveStability = fsrs.stability * interference;
  const survival = fsrsRetrievability(ageDays, effectiveStability);
  const activation = actRActivation(mem, now);
  const conf = mem.confidence ?? 0.5;
  const confidenceBonus = conf * 0.2;
  const sigmoid = 1 / (1 + Math.exp(activation));
  const rawForget = (1 - survival - confidenceBonus) * sigmoid;
  return Math.max(0, Math.min(1, rawForget));
}
function computeStructuralImportance(mem) {
  let I = 1;
  try {
    const { findMentionedEntities } = require("./graph.ts");
    const entities = findMentionedEntities(mem.content || "");
    I *= 1 + entities.length * 0.3;
  } catch {
  }
  const ei = mem.emotionIntensity ?? 0;
  I *= 1 + ei * 0.5;
  if (mem.reasoning) I *= 1.3;
  if (mem.because) I *= 1.2;
  const imp = mem.importance ?? mem.surprise ?? 5;
  I *= 0.5 + imp / 10;
  if (mem.scope === "correction") I *= 2;
  else if (mem.scope === "preference" || mem.scope === "fact") I *= 1.3;
  const network = mem.network;
  if (network === "world") I = Math.max(I, 0.5);
  else if (network === "experience") I *= 0.8;
  return Math.max(0.1, I);
}
const _crdBindings = /* @__PURE__ */ new Map();
function computeContextBinding(mem, currentTopics) {
  const key = (mem.content || "").slice(0, 40) + "|" + mem.ts;
  const now = Date.now();
  if (_crdBindings.size > 5e3) {
    const sorted = [..._crdBindings.entries()].sort((a, b) => a[1].bindingStrength - b[1].bindingStrength);
    const toDelete = 2e3;
    for (let i = 0; i < toDelete; i++) _crdBindings.delete(sorted[i][0]);
  }
  if (!_crdBindings.has(key)) {
    _crdBindings.set(key, { bindingStrength: 0.5, lastContextMatch: mem.lastAccessed || mem.ts });
  }
  const state = _crdBindings.get(key);
  if (currentTopics.length === 0) {
    const hoursSince = (now - state.lastContextMatch) / 36e5;
    state.bindingStrength *= Math.exp(-0.35 * hoursSince);
    return state.bindingStrength;
  }
  const memWords = new Set(((mem.content || "").match(WORD_PATTERN.CJK2_EN3) || []).map((w) => w.toLowerCase()));
  const topicWords = new Set(currentTopics.flatMap((t) => (t.match(WORD_PATTERN.CJK2_EN3) || []).map((w) => w.toLowerCase())));
  let overlap = 0;
  for (const w of memWords) {
    if (topicWords.has(w)) overlap++;
  }
  const overlapRatio = memWords.size > 0 ? overlap / memWords.size : 0;
  if (overlapRatio > 0.2) {
    state.bindingStrength = Math.min(1, state.bindingStrength + 0.2);
    state.lastContextMatch = now;
  } else {
    const hoursSince = (now - state.lastContextMatch) / 36e5;
    state.bindingStrength *= Math.exp(-0.35 * hoursSince);
  }
  try {
    const { getMomentumBoost } = require("./activation-field.ts");
    const momentum = getMomentumBoost(mem.content || "");
    if (momentum > 0.1) {
      state.bindingStrength = Math.max(state.bindingStrength, momentum);
    }
  } catch {
  }
  return state.bindingStrength;
}
function getCurrentTopics() {
  try {
    const { getSessionState, getLastActiveSessionKey } = require("./handler-state.ts");
    const sess = getSessionState(getLastActiveSessionKey());
    if (!sess) return [];
    const lastActivity = sess.lastMessageTs || 0;
    if (Date.now() - lastActivity > 6 * 36e5) return [];
    const recentMsgs = (sess.recentMessages || []).slice(-3);
    const topics = recentMsgs.map((m) => (m.content || m.user || "").slice(0, 100));
    return topics;
  } catch {
    return [];
  }
}
let P0_DEPLOY_TS = 0;
function getP0DeployTs() {
  if (P0_DEPLOY_TS > 0) return P0_DEPLOY_TS;
  try {
    const { loadJson: loadJson2, saveJson, DATA_DIR: DATA_DIR2 } = require("./persistence.ts");
    const { resolve: resolve2 } = require("path");
    const path = resolve2(DATA_DIR2, "distill_state.json");
    const state = loadJson2(path, {});
    if (state.p0DeployTs) {
      P0_DEPLOY_TS = state.p0DeployTs;
    } else {
      P0_DEPLOY_TS = Date.now();
      state.p0DeployTs = P0_DEPLOY_TS;
      saveJson(path, state);
    }
  } catch {
    P0_DEPLOY_TS = Date.now();
  }
  return P0_DEPLOY_TS;
}
const GRAVEYARD_GRACE_PERIOD = 7 * 864e5;
const GRAVEYARD_PURGE_AGE = 180 * 864e5;
function computeDerivability(mem) {
  const content = mem.content || "";
  if (!content || content.length < 5) return 0.5;
  if (mem.scope === "correction") return 0;
  let d = 0;
  try {
    const { findMentionedEntities } = require("./graph.ts");
    const entities = findMentionedEntities(content);
    if (entities.length > 0) d += 0.2;
  } catch {
  }
  try {
    const { extractFacts, queryFacts } = require("./fact-store.ts");
    const facts = extractFacts(content);
    let existingCount = 0;
    for (const f of facts) {
      const existing = queryFacts({ subject: f.subject, predicate: f.predicate });
      if (existing && existing.length > 0) existingCount++;
    }
    if (facts.length > 0) d += 0.3 * (existingCount / facts.length);
  } catch {
  }
  try {
    const { getRelevantTopics } = require("./distill.ts");
    const topics = getRelevantTopics(content, mem.userId, 1);
    if (topics.length > 0) d += 0.2;
  } catch {
  }
  try {
    const { getMentalModel } = require("./distill.ts");
    const model = getMentalModel(mem.userId);
    if (model) {
      const modelWords = new Set((model.match(WORD_PATTERN.CJK2_EN3) || []).map((w) => w.toLowerCase()));
      const memWords = (content.match(WORD_PATTERN.CJK2_EN3) || []).map((w) => w.toLowerCase());
      let overlap = 0;
      for (const w of memWords) if (modelWords.has(w)) overlap++;
      if (memWords.length > 0 && overlap / memWords.length > 0.4) d += 0.2;
    }
  } catch {
  }
  return Math.min(0.9, d);
}
function decideForget(mem, activityLevel) {
  const I = computeStructuralImportance(mem);
  const currentTopics = getCurrentTopics();
  const B = computeContextBinding(mem, currentTopics);
  const R = Math.min(1, I * 0.3 + B * 0.7);
  const alpha = mem.bayesAlpha ?? 2;
  const beta = mem.bayesBeta ?? 1;
  const C = alpha / (alpha + beta);
  const \u03B8 = bcmAdaptiveThreshold(getSurvivalForgetThreshold(), activityLevel);
  let action;
  let reason;
  if (R >= \u03B8 && C >= 0.3) {
    action = "keep";
    reason = `R=${R.toFixed(2)}(I=${I.toFixed(1)},B=${B.toFixed(2)})\u2265\u03B8=${\u03B8.toFixed(2)}, C=${C.toFixed(2)}\u22650.3`;
  } else if (R >= \u03B8 && C < 0.3) {
    action = "verify";
    reason = `R=${R.toFixed(2)}\u2265\u03B8=${\u03B8.toFixed(2)}, C=${C.toFixed(2)}<0.3 \u76F8\u5173\u4F46\u53EF\u7591`;
  } else {
    const d = computeDerivability(mem);
    const R_adjusted = R * (1 - d * 0.3);
    if (R_adjusted < \u03B8 && C >= 0.3) {
      action = "demote";
      reason = `R=${R.toFixed(2)}\u2192R_adj=${R_adjusted.toFixed(2)}(d=${d.toFixed(2)})<\u03B8=${\u03B8.toFixed(2)}, C=${C.toFixed(2)}\u22650.3 \u53EF\u4FE1\u4F46\u53EF\u63A8\u5BFC`;
    } else if (R_adjusted < \u03B8 && C < 0.3) {
      action = "graveyard";
      reason = `R=${R.toFixed(2)}\u2192R_adj=${R_adjusted.toFixed(2)}(d=${d.toFixed(2)})<\u03B8=${\u03B8.toFixed(2)}, C=${C.toFixed(2)}<0.3`;
    } else {
      action = "keep";
      reason = `R=${R.toFixed(2)}<\u03B8 but R_adj=${R_adjusted.toFixed(2)}\u2265\u03B8 (d=${d.toFixed(2)} low=\u72EC\u6709\u4FE1\u606F)`;
    }
  }
  return { retrievability: R, truthfulness: C, threshold: \u03B8, action, reason };
}
function reviveFromGraveyard(query, memories, maxRevive = 2) {
  const revived = [];
  const queryTri = trigrams(query);
  if (queryTri.size === 0) return revived;
  for (const m of memories) {
    if (!m || m.tier !== "graveyard") continue;
    const memTri = trigrams(m.content || "");
    const sim = trigramSimilarity(queryTri, memTri);
    if (sim > TRIGRAM_THRESHOLD.GRAVEYARD_REVIVE) {
      m.tier = "short_term";
      m.scope = m._graveyardOriginalScope || "fact";
      m.fsrs = fsrsInit(m.scope);
      m.lastAccessed = Date.now();
      delete m._graveyardOriginalScope;
      revived.push(m);
      logDecision(
        "revive",
        (m.content || "").slice(0, 30) + "|" + m.ts,
        `trigramSim=${sim.toFixed(2)}>${TRIGRAM_THRESHOLD.GRAVEYARD_REVIVE}, query="${query.slice(0, 20)}"`
      );
      if (revived.length >= maxRevive) break;
    }
  }
  return revived;
}
function purgeGraveyard(memories) {
  const now = Date.now();
  let purged = 0;
  for (let i = memories.length - 1; i >= 0; i--) {
    const m = memories[i];
    if (!m || m.tier !== "graveyard") continue;
    const graveyardAge = now - (m._graveyardTs || m.ts);
    const neverRevived = !m.lastAccessed || m.lastAccessed <= (m._graveyardTs || m.ts);
    if (graveyardAge > GRAVEYARD_PURGE_AGE && neverRevived) {
      const key = (m.content || "").slice(0, 30) + "|" + m.ts;
      logDecision("purge", key, `graveyardAge=${(graveyardAge / 864e5).toFixed(0)}d>180d, neverRevived`);
      memories.splice(i, 1);
      purged++;
    }
  }
  return purged;
}
function penalizeTruthfulness(mem, reason) {
  mem.bayesBeta = (mem.bayesBeta ?? 1) + 1;
  const C = (mem.bayesAlpha ?? 2) / ((mem.bayesAlpha ?? 2) + mem.bayesBeta);
  logDecision(
    "bayes_penalty",
    (mem.content || "").slice(0, 30) + "|" + mem.ts,
    `bayesBeta++\u2192${mem.bayesBeta}, C=${C.toFixed(2)}, reason=${reason}`
  );
}
function extractGistBeforeForget(mem) {
  const content = mem.content || "";
  if (content.length < 10) return null;
  let facts = [];
  let entities = [];
  try {
    const factStore = require("./fact-store.ts");
    facts = factStore.extractFacts(content);
  } catch {
  }
  try {
    const graph = require("./graph.ts");
    entities = graph.findMentionedEntities(content);
  } catch {
  }
  const hasCausal = !!mem.reasoning || !!mem.because;
  if (facts.length === 0 && entities.length === 0 && !hasCausal) {
    return null;
  }
  return {
    entities,
    facts: facts.map((f) => ({ subject: f.subject, predicate: f.predicate, object: f.object })),
    causal: mem.reasoning ?? null,
    because: mem.because ?? null,
    originalScope: mem.scope,
    originalTs: mem.ts,
    forgottenAt: Date.now()
  };
}
function processDecayedGists(gists) {
  if (gists.length < 2) return;
  const clusters = [];
  const assigned = /* @__PURE__ */ new Set();
  for (let i = 0; i < gists.length; i++) {
    if (assigned.has(i)) continue;
    const cluster = [gists[i]];
    assigned.add(i);
    for (let j = i + 1; j < gists.length; j++) {
      if (assigned.has(j)) continue;
      const shared = gists[i].entities.filter((e) => gists[j].entities.includes(e));
      if (shared.length > 0) {
        cluster.push(gists[j]);
        assigned.add(j);
      }
    }
    clusters.push(cluster);
  }
  try {
    const distillMod = require("./distill.ts");
    let llmCalls = 0;
    for (const cluster of clusters) {
      if (cluster.length < 2) continue;
      const contents = cluster.map((g) => {
        const parts = [];
        if (g.facts.length > 0) parts.push(g.facts.map((f) => `${f.subject}${f.predicate}${f.object}`).join("\uFF0C"));
        if (g.entities.length > 0) parts.push(`\u6D89\u53CA\uFF1A${g.entities.join("\u3001")}`);
        if (g.because) parts.push(`\u539F\u56E0\uFF1A${g.because}`);
        return parts.join("\uFF1B") || `[${g.originalScope}] \u9057\u5FD8\u4E8E${new Date(g.forgottenAt).toISOString().slice(0, 10)}`;
      });
      if (!distillMod.distillState) continue;
      const pending = distillMod.distillState.pendingDecayDistill ?? [];
      pending.push({ contents, clusteredAt: Date.now() });
      if (pending.length > 10) pending.splice(0, pending.length - 10);
      distillMod.distillState.pendingDecayDistill = pending;
    }
  } catch {
  }
}
function smartForgetSweep(memories) {
  const now = Date.now();
  const toForget = [];
  const toConsolidate = [];
  const oneDayAgo = now - 864e5;
  const recentCount = memories.filter((m) => m && m.ts > oneDayAgo && m.scope !== "expired").length;
  const activityLevel = Math.min(1, recentCount / 100);
  for (let i = 0; i < memories.length; i++) {
    const m = memories[i];
    if (!m || typeof m.ts !== "number") continue;
    if (m.scope === "expired" || m.tier === "graveyard") continue;
    const mem = {
      ts: m.ts ?? now,
      recallCount: m.recallCount ?? m.recall_count ?? 0,
      lastAccessed: m.lastAccessed ?? m.last_accessed ?? m.ts ?? now,
      scope: m.scope ?? m.type ?? "fact",
      confidence: m.confidence,
      fsrs: m.fsrs,
      bayesAlpha: m.bayesAlpha,
      bayesBeta: m.bayesBeta
    };
    const decision = decideForget(mem, activityLevel);
    const key = (m.content || "").slice(0, 30) + "|" + m.ts;
    switch (decision.action) {
      case "graveyard":
        toForget.push(i);
        logDecision("graveyard", key, decision.reason);
        break;
      case "demote":
        if (m.tier !== "fading") {
          m.tier = "fading";
          logDecision("demote", key, decision.reason);
        }
        break;
      case "verify":
        if (!m._needsVerification) {
          m._needsVerification = true;
          logDecision("verify", key, decision.reason);
        }
        break;
      case "keep":
        if (decision.retrievability > getSurvivalConsolidateThreshold() && decision.truthfulness > 0.7) {
          toConsolidate.push(i);
        }
        break;
    }
  }
  return { toForget, toConsolidate };
}
function getRecallRecommendations(memories, maxCount = 3) {
  const now = Date.now();
  const candidates = [];
  for (const m of memories) {
    if (!m || m.scope === "expired" || m.scope === "decayed" || m.scope === "consolidated") continue;
    const importance = m.importance ?? 5;
    if (importance < 6) continue;
    const fsrs = m.fsrs || { stability: 30, difficulty: 5 };
    const ageDays = (now - (m.ts || now)) / MS_PER_DAY;
    const retrievability = Math.pow(1 + ageDays / (9 * fsrs.stability), -1);
    if (retrievability >= 0.3 && retrievability <= 0.6) {
      const urgency = (0.6 - retrievability) / 0.3;
      candidates.push({ mem: m, retrievability, importance, urgency });
    }
  }
  candidates.sort((a, b) => b.urgency * b.importance - a.urgency * a.importance);
  return candidates.slice(0, maxCount).map((c) => ({
    content: c.mem.content.slice(0, 80),
    urgency: c.urgency
  }));
}
const stats = {
  lastSweepTs: 0,
  lastSweepForget: 0,
  lastSweepConsolidate: 0,
  totalSweeps: 0
};
const smartForgetModule = {
  id: "smart-forget",
  name: "\u667A\u80FD\u9057\u5FD8\u5F15\u64CE",
  priority: 20,
  async init() {
    try {
      const { DATA_DIR: DATA_DIR2 } = await import("./persistence.ts");
      loadDecayParams(DATA_DIR2);
    } catch {
      try {
        const { homedir } = await import("os");
        const p = resolve(homedir(), ".openclaw/plugins/cc-soul/data");
        if (existsSync(p)) loadDecayParams(p);
      } catch {
      }
    }
    if (!_decayParams.scopeK) {
      _decayParams.scopeK = { ...WEIBULL_K_DEFAULT };
      saveDecayParams();
    }
    console.log(`[smart-forget] initialized \u2014 FSRS-7 + LECTOR interference, ACT-R d=0.5, \u03BB-multiplier=${_decayParams.lambdaMultiplier.toFixed(3)} (EMA \u03B1=${getEMAAlpha()})`);
  },
  dispose() {
  },
  /** Periodic sweep during heartbeat */
  async onHeartbeat() {
    let memories = [];
    try {
      const memModule = await import("./memory.ts");
      memories = memModule?.memoryState?.memories ?? [];
    } catch {
      return;
    }
    if (memories.length === 0) return;
    const result = smartForgetSweep(memories);
    stats.lastSweepTs = Date.now();
    stats.lastSweepForget = result.toForget.length;
    stats.lastSweepConsolidate = result.toConsolidate.length;
    stats.totalSweeps++;
    if (result.toForget.length > 0) {
      const maxPerSweep = getParam("forget.max_per_sweep");
      const toForget = result.toForget.slice(0, maxPerSweep);
      const isGracePeriod = Date.now() - getP0DeployTs() < GRAVEYARD_GRACE_PERIOD;
      const gists = [];
      for (let i = toForget.length - 1; i >= 0; i--) {
        const idx = toForget[i];
        if (idx >= 0 && idx < memories.length && memories[idx].tier !== "graveyard") {
          const m = memories[idx];
          const gist = extractGistBeforeForget(m);
          if (gist) gists.push(gist);
          m._graveyardOriginalScope = m.scope;
          m._graveyardTs = Date.now();
          m.tier = "graveyard";
          m.scope = "expired";
          try {
            const { appendLineage } = require("./memory-utils.ts");
            appendLineage(m, { action: "gisted", ts: Date.now(), delta: `\u2192graveyard, from:${(m.content || "").length}` });
          } catch {
          }
          if (!isGracePeriod) {
            m.content = (m.content || "").slice(0, 50);
          }
        }
      }
      if (gists.length >= 2) {
        processDecayedGists(gists);
      }
      emitCacheEvent("memory_deleted");
    }
    if (result.toConsolidate.length > 0) {
      for (const idx of result.toConsolidate) {
        if (idx >= 0 && idx < memories.length && memories[idx].scope !== "consolidated") {
          memories[idx].scope = "consolidated";
        }
      }
    }
    purgeGraveyard(memories);
    if (result.toForget.length > 0 || result.toConsolidate.length > 0) {
      try {
        const memModule = await import("./memory.ts");
        memModule.saveMemories();
      } catch {
      }
      console.log(
        `[smart-forget] sweep #${stats.totalSweeps}: ${result.toForget.length} forgotten, ${result.toConsolidate.length} consolidated (out of ${memories.length} memories)`
      );
    }
  }
};
export {
  WEIBULL_K,
  computeContextBinding,
  computeForgetScore,
  computeStructuralImportance,
  decideForget,
  effectiveLambda,
  extractGistBeforeForget,
  fsrsInit,
  fsrsRetrievability,
  fsrsUpdate,
  getCurrentTopics,
  getLambdaMultiplier,
  getRecallRecommendations,
  getWeibullK,
  penalizeTruthfulness,
  processDecayedGists,
  purgeGraveyard,
  recordRecallHit,
  recordRecallMiss,
  reviveFromGraveyard,
  smartForgetModule,
  smartForgetSweep,
  weibullSurvival
};
