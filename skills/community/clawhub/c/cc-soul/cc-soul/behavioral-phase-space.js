import { DATA_DIR, loadJson, debouncedSave } from "./persistence.ts";
import { resolve } from "path";
import { detectDomain } from "./epistemic.ts";
const STATE_PATH = resolve(DATA_DIR, "behavioral_phase_space.json");
const PATTERNS_PATH = resolve(DATA_DIR, "behavior_patterns.json");
const MAX_TRAJECTORY = 30;
let trajectory = [];
let patterns = (() => {
  const loaded = loadJson(PATTERNS_PATH, []);
  return Array.isArray(loaded) ? loaded : [];
})();
let domainBeliefs = {};
let ppmRoot = { children: {}, counts: {}, total: 0, escape: 0 };
let observations = [];
try {
  const saved = loadJson(STATE_PATH, {});
  if (saved.trajectory) trajectory = saved.trajectory;
  if (saved.domainBeliefs) domainBeliefs = saved.domainBeliefs;
  if (saved.ppmRoot) ppmRoot = saved.ppmRoot;
  if (saved.observations) observations = saved.observations;
} catch {
}
function save() {
  debouncedSave(STATE_PATH, { trajectory, domainBeliefs, ppmRoot, observations: observations.slice(-100) }, 5e3);
}
function getTimeSlot() {
  const h = (/* @__PURE__ */ new Date()).getHours();
  if (h >= 0 && h < 6) return "late_night";
  if (h >= 6 && h < 9) return "early_morning";
  if (h >= 9 && h < 12) return "morning";
  if (h >= 12 && h < 18) return "afternoon";
  if (h >= 18 && h < 23) return "evening";
  return "late_night";
}
function getMoodBucket(mood) {
  if (mood > 0.3) return "positive";
  if (mood < -0.3) return "negative";
  return "neutral";
}
function detectTopicDomain(msg) {
  try {
    const d = detectDomain(msg);
    if (d && d !== "general" && d !== "\u901A\u7528") return d;
  } catch {
  }
  const m = msg.toLowerCase();
  if (/python|\.py|pip|django|flask/.test(m)) return "python";
  if (/javascript|node|react|vue|typescript/.test(m)) return "javascript";
  if (/swift|ios|xcode/.test(m)) return "ios";
  if (/docker|k8s|deploy|nginx/.test(m)) return "devops";
  if (/面试|简历|跳槽|工作|职场|老板/.test(m)) return "career";
  if (/代码|函数|编程|bug|算法/.test(m)) return "tech";
  return "general";
}
function recordState(userMsg, mood, session) {
  const state = {
    topic: detectTopicDomain(userMsg),
    mood,
    engagement: estimateEngagement(userMsg, session),
    style: "balanced",
    timeSlot: getTimeSlot(),
    afterEvent: session?._pendingCorrectionVerify ? "correction" : session?.turnCount >= 3 ? "rapid_fire" : void 0,
    ts: Date.now()
  };
  trajectory.push(state);
  if (trajectory.length > MAX_TRAJECTORY) trajectory = trajectory.slice(-MAX_TRAJECTORY);
  updateDomainBelief(state.topic);
  save();
  return state;
}
function estimateEngagement(msg, session) {
  let e = 0.5;
  if (msg.length > 100) e += 0.2;
  if (msg.length < 10) e -= 0.2;
  if (/？|\?/.test(msg)) e += 0.1;
  if (session?.turnCount > 5) e += 0.1;
  return Math.max(0, Math.min(1, e));
}
function predictNext() {
  const recent = trajectory.slice(-5);
  if (recent.length < 2) {
    return {
      topic: { predicted: "general", confidence: 0 },
      style: { predicted: "balanced", confidence: 0 },
      engagement: { predicted: 0.5, confidence: 0 },
      mood: { predicted: 0, confidence: 0 }
    };
  }
  const weights = [0.5, 0.3, 0.2];
  const lastN = recent.slice(-3);
  const predictContinuous = (getValue) => {
    if (lastN.length < 2) return { predicted: getValue(lastN[0]), confidence: 0.3 };
    let weightedSum = 0, totalWeight = 0;
    for (let i = 0; i < lastN.length; i++) {
      const w = weights[i] ?? 0.1;
      weightedSum += getValue(lastN[i]) * w;
      totalWeight += w;
    }
    const predicted = weightedSum / totalWeight;
    const values = lastN.map(getValue);
    const mean = values.reduce((s, v) => s + v, 0) / values.length;
    const variance = values.reduce((s, v) => s + (v - mean) ** 2, 0) / values.length;
    const confidence = Math.max(0.1, Math.min(0.9, 1 - variance * 4));
    return { predicted, confidence };
  };
  const styleCounts = /* @__PURE__ */ new Map();
  for (const s of lastN) {
    styleCounts.set(s.style, (styleCounts.get(s.style) ?? 0) + 1);
  }
  let bestStyle = "balanced", bestStyleCount = 0;
  for (const [style, count] of styleCounts) {
    if (count > bestStyleCount) {
      bestStyle = style;
      bestStyleCount = count;
    }
  }
  const topicPrediction = ppmPredict(recent.map((s) => s.topic));
  return {
    topic: topicPrediction ?? { predicted: recent[recent.length - 1].topic, confidence: 0.3 },
    style: { predicted: bestStyle, confidence: bestStyleCount / lastN.length },
    engagement: predictContinuous((s) => s.engagement),
    mood: predictContinuous((s) => s.mood)
  };
}
function getBehaviorEngineHint(userMsg, mood, session) {
  const state = trajectory[trajectory.length - 1] ?? recordState(userMsg, mood, session);
  const moodBucket = getMoodBucket(mood);
  const day = (/* @__PURE__ */ new Date()).getDay();
  const dayType = day === 0 || day === 6 ? "weekend" : "weekday";
  const matched = patterns.filter((p) => {
    let score = 0;
    if (p.condition.timeSlot && p.condition.timeSlot === state.timeSlot) score++;
    if (p.condition.topicDomain && p.condition.topicDomain === state.topic) score++;
    if (p.condition.mood && p.condition.mood === moodBucket) score++;
    if (p.condition.afterEvent && p.condition.afterEvent === state.afterEvent) score++;
    if (p.condition.dayType && p.condition.dayType === dayType) score++;
    return score > 0;
  }).filter((p) => {
    const conf2 = (p.hits + 1) / (p.hits + p.misses + 2);
    return conf2 > 0.4;
  }).sort((a, b) => {
    const confA = (a.hits + 1) / (a.hits + a.misses + 2);
    const confB = (b.hits + 1) / (b.hits + b.misses + 2);
    return confB - confA;
  });
  if (matched.length === 0) return null;
  const best = matched[0];
  const conf = (best.hits + 1) / (best.hits + best.misses + 2);
  return `[\u884C\u4E3A\u6A21\u5F0F] ${best.action.hint} (${conf > 0.8 ? "\u9AD8" : conf > 0.5 ? "\u4E2D" : "\u4F4E"}\u7F6E\u4FE1)`;
}
function recordObservation(userMsg, mood, session, reaction, responseStyle) {
  const state = trajectory[trajectory.length - 1] ?? recordState(userMsg, mood, session);
  state.style = responseStyle;
  observations.push({ state, reaction, ts: Date.now() });
  if (observations.length > 200) observations = observations.slice(-200);
  save();
}
function learnFromObservations() {
  if (observations.length < 5) return;
  const recent = observations.slice(-50);
  const groups = /* @__PURE__ */ new Map();
  for (const obs of recent) {
    const key = `${obs.state.timeSlot}|${obs.state.topic}|${getMoodBucket(obs.state.mood)}`;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push({
      style: obs.state.style,
      satisfied: obs.reaction === "satisfied" ? 1 : 0,
      total: 1
    });
  }
  for (const [key, entries] of groups) {
    if (entries.length < 3) continue;
    const [timeSlot, topic, mood] = key.split("|");
    const bestStyle = entries.reduce((best, e) => e.satisfied > best.satisfied ? e : best, entries[0]);
    const hits = entries.filter((e) => e.satisfied > 0).length;
    const misses = entries.length - hits;
    if (hits / (hits + misses) < 0.4) continue;
    const existing = patterns.find(
      (p) => p.condition.timeSlot === timeSlot && p.condition.topicDomain === topic
    );
    if (existing) {
      existing.hits += hits;
      existing.misses += misses;
      existing.lastHit = Date.now();
    } else {
      patterns.push({
        id: `learned_${Date.now()}_${Math.random().toString(36).slice(2, 6)}`,
        condition: { timeSlot, topicDomain: topic, mood },
        action: { style: bestStyle.style, hint: `${timeSlot}+${topic}+${mood}\u65F6\u7528${bestStyle.style}\u98CE\u683C` },
        hits,
        misses,
        lastHit: Date.now(),
        createdAt: Date.now(),
        source: "learned"
      });
    }
  }
  const now = Date.now();
  patterns = patterns.filter((p) => {
    const age = now - p.createdAt;
    const conf = (p.hits + 1) / (p.hits + p.misses + 2);
    return age < 30 * 864e5 || conf > 0.3;
  });
  debouncedSave(PATTERNS_PATH, patterns, 5e3);
  save();
}
function updateDomainBelief(domain) {
  if (!domainBeliefs[domain]) domainBeliefs[domain] = { alpha: 1, beta: 1, lastSeen: 0 };
  const b = domainBeliefs[domain];
  const ageDays = (Date.now() - b.lastSeen) / 864e5;
  if (ageDays > 7) {
    const decay = Math.pow(0.95, ageDays / 7);
    b.alpha = Math.max(1, b.alpha * decay);
    b.beta = Math.max(1, b.beta * decay);
  }
  b.alpha++;
  b.lastSeen = Date.now();
  for (const [d, belief] of Object.entries(domainBeliefs)) {
    if (d !== domain) belief.beta += 0.1;
  }
}
function predictDomainProbability(domain) {
  const b = domainBeliefs[domain];
  if (!b) return 0.1;
  return b.alpha / (b.alpha + b.beta);
}
function getTopPredictions(topN = 3) {
  return Object.entries(domainBeliefs).map(([domain, b]) => ({ domain, probability: b.alpha / (b.alpha + b.beta) })).sort((a, b) => b.probability - a.probability).slice(0, topN);
}
function getMoodCondition(mood) {
  return mood > 0.2 ? "positive" : "non_positive";
}
const ppmByMood = {
  positive: { children: {}, counts: {}, total: 0, escape: 0 },
  non_positive: { children: {}, counts: {}, total: 0, escape: 0 }
};
function ppmUpdate(context, next, maxOrder = 3, mood, weight = 1) {
  let node = ppmRoot;
  const ctx = context.slice(-maxOrder);
  node.counts[next] = (node.counts[next] || 0) + weight;
  node.total += weight;
  for (const symbol of ctx) {
    if (!node.children[symbol]) node.children[symbol] = { children: {}, counts: {}, total: 0, escape: 0 };
    node = node.children[symbol];
    node.counts[next] = (node.counts[next] || 0) + weight;
    node.total += weight;
  }
  if (mood !== void 0) {
    const condition = getMoodCondition(mood);
    let moodNode = ppmByMood[condition];
    moodNode.counts[next] = (moodNode.counts[next] || 0) + weight;
    moodNode.total += weight;
    for (const symbol of ctx) {
      if (!moodNode.children[symbol]) moodNode.children[symbol] = { children: {}, counts: {}, total: 0, escape: 0 };
      moodNode = moodNode.children[symbol];
      moodNode.counts[next] = (moodNode.counts[next] || 0) + weight;
      moodNode.total += weight;
    }
  }
}
function ppmPredict(context, mood) {
  const ctx = context.slice(-3);
  if (mood !== void 0) {
    const condition = getMoodCondition(mood);
    const moodRoot = ppmByMood[condition];
    if (moodRoot.total >= 5) {
      const result = ppmPredictFromRoot(moodRoot, ctx);
      if (result) return result;
    }
  }
  return ppmPredictFromRoot(ppmRoot, ctx);
}
function ppmPredictFromRoot(root, ctx) {
  for (let order = ctx.length; order >= 0; order--) {
    let node = root;
    for (let i = ctx.length - order; i < ctx.length; i++) {
      if (!node.children[ctx[i]]) {
        node = root;
        break;
      }
      node = node.children[ctx[i]];
    }
    if (node.total > 0) {
      let best = "", bestCount = 0;
      for (const [topic, count] of Object.entries(node.counts)) {
        if (count > bestCount) {
          best = topic;
          bestCount = count;
        }
      }
      if (best && bestCount >= 2) {
        return { predicted: best, confidence: bestCount / node.total };
      }
    }
  }
  return null;
}
function updateMarkov(topicSequence, mood, intentScores) {
  for (let i = 1; i < topicSequence.length; i++) {
    const weight = intentScores?.[i] ?? 1;
    ppmUpdate(topicSequence.slice(0, i), topicSequence[i], 3, mood, weight);
  }
  save();
}
function predictNextTopic(recentTopics, mood) {
  return ppmPredict(recentTopics, mood);
}
function getBehaviorPrediction(userMsg, memories) {
  const pred = predictNext();
  if (pred.topic.confidence < 0.3 && pred.mood.confidence < 0.3) return null;
  const parts = [];
  if (pred.topic.confidence >= 0.4) parts.push(`\u53EF\u80FD\u63A5\u4E0B\u6765\u804A${pred.topic.predicted}`);
  if (pred.engagement.predicted < 0.3) parts.push(`\u53C2\u4E0E\u5EA6\u5728\u964D\u4F4E`);
  if (pred.mood.predicted < -0.3) parts.push(`\u60C5\u7EEA\u53EF\u80FD\u53D8\u5DEE`);
  if (parts.length === 0) return null;
  return `[\u884C\u4E3A\u9884\u6D4B] ${parts.join("\uFF0C")}`;
}
function getTimeSlotPrediction(chatHistory) {
  const ts = getTimeSlot();
  const topDomains = getTopPredictions(2);
  if (topDomains.length === 0 || topDomains[0].probability < 0.3) return null;
  return `[\u65F6\u6BB5\u4E60\u60EF] ${ts}\u65F6\u6BB5\uFF0C\u7528\u6237\u901A\u5E38\u804A${topDomains.map((d) => d.domain).join("/")}`;
}
function isDecisionQuestion(msg) {
  return /该不该|要不要|选.*还是|A.*还是.*B|哪个好|怎么选|纠结/i.test(msg);
}
function predictUserDecision(situation, memories, userId) {
  const pred = predictNext();
  if (pred.style.confidence < 0.5) return null;
  return `\u7528\u6237\u503E\u5411${pred.style.predicted}\u98CE\u683C\u7684\u5EFA\u8BAE`;
}
function getUnifiedBehaviorHint(userMsg, mood, session, memories) {
  const parts = [];
  const engineHint = getBehaviorEngineHint(userMsg, mood, session);
  if (engineHint) {
    parts.push(engineHint.replace(/^\[行为模式\]\s*/, ""));
  }
  const pred = predictNext();
  if (pred.topic.confidence >= 0.4) parts.push(`\u53EF\u80FD\u63A5\u4E0B\u6765\u804A${pred.topic.predicted}`);
  if (pred.engagement.predicted < 0.3) parts.push("\u53C2\u4E0E\u5EA6\u5728\u964D\u4F4E");
  if (pred.mood.predicted < -0.3) parts.push("\u60C5\u7EEA\u53EF\u80FD\u53D8\u5DEE");
  const ts = getTimeSlot();
  const topDomains = getTopPredictions(1);
  if (topDomains.length > 0 && topDomains[0].probability >= 0.5) {
    parts.push(`${ts}\u65F6\u6BB5\u5E38\u804A${topDomains[0].domain}`);
  }
  if (parts.length === 0) return null;
  return `[\u884C\u4E3A\u5206\u6790] ${parts.join("\uFF0C")}`;
}
function checkPredictions(userMsg) {
  const domain = detectTopicDomain(userMsg);
  const prob = predictDomainProbability(domain);
  if (prob > 0.5) {
    return { hitAugment: `[\u9884\u6D4B\u547D\u4E2D] \u9884\u6D4B\u5230\u4F60\u4F1A\u804A${domain}\uFF08\u6982\u7387${(prob * 100).toFixed(0)}%\uFF09` };
  }
  return { hitAugment: null };
}
function generateNewPredictions(chatHistory, intentScores) {
  const topics = chatHistory.slice(-10).map((h) => detectTopicDomain(h.user));
  updateMarkov(topics, void 0, intentScores);
}
function updateAllDomainBeliefs(detectedDomain) {
  if (detectedDomain) updateDomainBelief(detectedDomain);
}
function getPatternCount() {
  return patterns.length;
}
function getLearnedPatternCount() {
  return patterns.filter((p) => p.source === "learned").length;
}
function getLearnedPatterns() {
  return patterns.filter((p) => p.source === "learned" && p.hits >= 3).map((p) => ({
    condition: [p.condition.timeSlot, p.condition.topicDomain, p.condition.mood, p.condition.afterEvent, p.condition.dayType].filter(Boolean).join("+"),
    action: p.action.style || p.action.hint,
    hits: p.hits,
    misses: p.misses,
    confidence: p.hits / Math.max(1, p.hits + p.misses)
  }));
}
export {
  checkPredictions,
  generateNewPredictions,
  getBehaviorEngineHint,
  getBehaviorPrediction,
  getLearnedPatternCount,
  getLearnedPatterns,
  getPatternCount,
  getTimeSlot,
  getTimeSlotPrediction,
  getTopPredictions,
  getUnifiedBehaviorHint,
  isDecisionQuestion,
  learnFromObservations,
  predictDomainProbability,
  predictNext,
  predictNextTopic,
  predictUserDecision,
  recordObservation,
  recordState,
  updateAllDomainBeliefs,
  updateMarkov
};
