import { DATA_DIR, loadJson, debouncedSave } from "./persistence.ts";
import { getParam } from "./auto-tune.ts";
import { resolve } from "path";
import { EMOTION_POSITIVE, EMOTION_NEGATIVE, detectEmotionLabel, emotionLabelToPADCN, computeEmotionSpectrum } from "./signals.ts";
const BODY_STATE_PATH = resolve(DATA_DIR, "body_state.json");
const _emotionVectors = /* @__PURE__ */ new Map();
const _defaultVector = () => ({ pleasure: 0, arousal: 0, dominance: 0.3, certainty: 0.5, novelty: 0 });
function getEmotionVector(userId) {
  const key = userId || "_default";
  if (!_emotionVectors.has(key)) _emotionVectors.set(key, _defaultVector());
  return _emotionVectors.get(key);
}
const emotionVector = getEmotionVector("_default");
const body = {
  energy: 1,
  mood: 0.3,
  load: 0,
  alertness: 0.5,
  anomaly: 0
};
const emotionLayers = { reflex: 0, emotion: 0, mood: 0.3 };
function combinedEmotion(layers = emotionLayers) {
  return layers.reflex * 0.4 + layers.emotion * 0.35 + layers.mood * 0.25;
}
function updateEmotionLayers(userValence, dt) {
  emotionLayers.reflex = userValence;
  const alphaEmotion = 1 - Math.exp(-dt / 300);
  emotionLayers.emotion = emotionLayers.emotion * (1 - alphaEmotion) + userValence * alphaEmotion;
  emotionLayers.mood = body.mood;
}
let lastTickTime = Date.now();
function circadianModifier(peakHour = 10) {
  const hour = (/* @__PURE__ */ new Date()).getHours() + (/* @__PURE__ */ new Date()).getMinutes() / 60;
  const phase24 = (hour - peakHour) / 24 * 2 * Math.PI;
  const wave24 = Math.cos(phase24);
  const phase12 = (hour - peakHour) / 12 * 2 * Math.PI;
  const wave12 = Math.cos(phase12);
  const combined = wave24 * 0.7 + wave12 * 0.3;
  let nightPenalty = 0;
  if (hour >= 0 && hour < 5) {
    const nightDepth = 1 - Math.abs(hour - 2.5) / 2.5;
    nightPenalty = nightDepth * 0.15;
  }
  const energyMod = combined * 0.2 - 0.05 - nightPenalty;
  const moodMod = energyMod * 0.4;
  return { energyMod, moodMod };
}
function bodyTick(userPeakHour) {
  const now = Date.now();
  const minutes = Math.min(10, (now - lastTickTime) / 6e4);
  lastTickTime = now;
  const circadian = circadianModifier(userPeakHour ?? 10);
  const recoveryRate = getParam("body.energy_recovery_per_min");
  const logisticRecovery = recoveryRate * body.energy * (1 - body.energy) * 4;
  body.energy = Math.min(1, Math.max(0, body.energy + logisticRecovery * minutes));
  const circadianDelta = circadian.energyMod * 0.01 * minutes;
  if (circadianDelta > 0) body.energy = Math.min(1, body.energy + circadianDelta);
  const alertDecay = getParam("body.alertness_decay_per_min") || 5e-3;
  const alertRecovery = getParam("body.alertness_recovery_per_min") || 3e-3;
  if (body.alertness > 0.5) {
    body.alertness = Math.max(0.5, body.alertness - Math.max(0, alertDecay) * minutes);
  } else if (body.alertness < 0.5) {
    body.alertness = Math.min(0.5, body.alertness + Math.max(0, alertRecovery) * minutes);
  }
  const loadDecay = getParam("body.load_decay_per_min") || 0.02;
  body.load = Math.max(0, body.load - Math.max(0, loadDecay) * minutes);
  if (body.mood !== 0) {
    const decayFactor = getParam("body.mood_decay_factor") || 0.95;
    const safeFactor = decayFactor > 0 && decayFactor <= 1 ? decayFactor : 0.95;
    body.mood *= Math.pow(safeFactor, Math.min(30, minutes));
  }
  body.mood = Math.max(-1, Math.min(1, body.mood + circadian.moodMod * 0.01 * minutes));
  body.anomaly = Math.max(0, body.anomaly - (getParam("body.anomaly_decay_per_min") || 0.01) * minutes);
  emotionLayers.reflex *= 0.1;
  emotionLayers.emotion *= Math.pow(0.995, minutes);
  emotionLayers.mood = body.mood;
  for (const ev of _emotionVectors.values()) {
    for (const k of Object.keys(ev)) {
      ev[k] *= 0.995;
    }
  }
  recordMoodSnapshot();
  saveBodyState();
}
function bodyOnMessage(complexity, _userId) {
  const baseEnergyCost = getParam("body.message_energy_base_cost") || 0.02;
  const complexityEnergyCost = getParam("body.message_energy_complexity_cost") || 0.03;
  const baseLoadIncrease = getParam("body.message_load_base") || 0.1;
  const complexityLoadIncrease = getParam("body.message_load_complexity") || 0.15;
  body.energy = Math.max(0, body.energy - baseEnergyCost - complexity * complexityEnergyCost);
  body.load = Math.min(1, body.load + baseLoadIncrease + complexity * complexityLoadIncrease);
  const ev = getEmotionVector(_userId);
  const clamp = (v) => Math.max(-1, Math.min(1, v));
  ev.arousal = clamp(ev.arousal + complexity * 0.15);
  ev.novelty = clamp(ev.novelty + complexity * 0.1);
}
function bodyOnCorrection(userId) {
  body.alertness = Math.min(1, body.alertness + getParam("body.correction_alertness_boost"));
  body.mood = Math.max(-1, Math.min(1, body.mood - getParam("body.correction_mood_penalty")));
  body.anomaly = Math.min(1, body.anomaly + (getParam("body.correction_anomaly_boost") || 0.15));
  const ev = getEmotionVector(userId);
  const clamp = (v) => Math.max(-1, Math.min(1, v));
  ev.certainty = clamp(ev.certainty - 0.2);
  ev.dominance = clamp(ev.dominance - 0.1);
  ev.pleasure = clamp(ev.pleasure - 0.15);
}
function bodyOnPositiveFeedback(userId) {
  body.energy = Math.min(1, body.energy + getParam("body.positive_energy_boost"));
  body.mood = Math.min(1, body.mood + getParam("body.positive_mood_boost"));
  body.anomaly = Math.max(0, body.anomaly - (getParam("body.positive_anomaly_reduction") || 0.05));
  const ev = getEmotionVector(userId);
  const clamp = (v) => Math.max(-1, Math.min(1, v));
  ev.pleasure = clamp(ev.pleasure + 0.2);
  ev.certainty = clamp(ev.certainty + 0.1);
  ev.dominance = clamp(ev.dominance + 0.1);
}
const userEmotions = /* @__PURE__ */ new Map();
const DEFAULT_EMOTION = { valence: 0, arousal: 0, trend: 0, history: [], lastUpdate: 0, consecutiveSameDir: 0, lastDir: 0 };
function getUserEmotion(senderId) {
  const key = senderId || "_default";
  let emotion = userEmotions.get(key);
  if (!emotion) {
    emotion = { ...DEFAULT_EMOTION, history: [] };
    userEmotions.set(key, emotion);
  }
  return emotion;
}
let lastDetectedEmotion = { label: "neutral", confidence: 0 };
function processEmotionalContagion(msg, attentionType, frustration, senderId) {
  const userEmotion = getUserEmotion(senderId);
  const detected = detectEmotionLabel(msg);
  lastDetectedEmotion = detected;
  if (detected.confidence > 0.5) {
    const ev = getEmotionVector(senderId);
    const delta = emotionLabelToPADCN(detected.label);
    const weight = detected.confidence * 0.3;
    ev.pleasure = ev.pleasure * 0.8 + delta.pleasure * weight;
    ev.arousal = ev.arousal * 0.8 + delta.arousal * weight;
    ev.dominance = ev.dominance * 0.9 + delta.dominance * weight * 0.5;
    ev.certainty = ev.certainty * 0.9 + delta.certainty * weight * 0.5;
    ev.novelty = ev.novelty * 0.9 + delta.novelty * weight * 0.5;
    Object.assign(emotionVector, ev);
  }
  try {
    const spectrum = computeEmotionSpectrum(msg);
    const ev = getEmotionVector(senderId);
    if (ev) {
      const alpha = 0.15;
      ev.pleasure += alpha * (spectrum.joy + spectrum.pride + spectrum.relief - spectrum.anger - spectrum.sadness - spectrum.frustration);
      ev.arousal += alpha * (spectrum.anger + spectrum.anxiety + spectrum.frustration + spectrum.curiosity);
      ev.dominance += alpha * (spectrum.pride - spectrum.frustration - spectrum.anxiety);
      ev.certainty += alpha * (spectrum.pride + spectrum.relief - spectrum.anxiety);
      ev.novelty += alpha * spectrum.curiosity;
      ev.pleasure = Math.max(-1, Math.min(1, ev.pleasure));
      ev.arousal = Math.max(-1, Math.min(1, ev.arousal));
      ev.dominance = Math.max(-1, Math.min(1, ev.dominance));
      ev.certainty = Math.max(-1, Math.min(1, ev.certainty));
      ev.novelty = Math.max(-1, Math.min(1, ev.novelty));
      Object.assign(emotionVector, ev);
    }
  } catch {
  }
  let valence = 0;
  const m = msg.toLowerCase();
  if (["joy", "gratitude", "pride", "relief", "anticipation"].includes(detected.label)) {
    valence += 0.3 + detected.confidence * 0.3;
  } else if (["anger", "anxiety", "frustration", "sadness", "disappointment"].includes(detected.label)) {
    valence -= 0.3 + detected.confidence * 0.3;
  } else if (detected.label === "confusion") {
    valence -= 0.1;
  }
  if (valence === 0) {
    if (EMOTION_POSITIVE.some((w) => m.includes(w))) valence += 0.4;
    if (EMOTION_NEGATIVE.some((w) => m.includes(w))) valence -= 0.4;
  }
  valence -= frustration * 0.3;
  if (attentionType === "correction") valence -= 0.2;
  if (msg.length < 5 && valence === 0) valence = -0.05;
  valence = Math.max(-1, Math.min(1, valence));
  userEmotion.valence = userEmotion.valence * 0.7 + valence * 0.3;
  userEmotion.arousal = Math.min(1, Math.abs(valence) + frustration * 0.5);
  userEmotion.history.push(userEmotion.valence);
  if (userEmotion.history.length > 10) userEmotion.history.shift();
  if (userEmotion.history.length >= 3) {
    const avg = userEmotion.history.reduce((a, b) => a + b, 0) / userEmotion.history.length;
    userEmotion.trend = userEmotion.valence - avg;
  }
  userEmotion.lastUpdate = Date.now();
  if (userEmotions.size > 50) {
    let oldestKey = "", oldestTime = Infinity;
    for (const [k, v] of userEmotions) {
      if (v.lastUpdate < oldestTime) {
        oldestTime = v.lastUpdate;
        oldestKey = k;
      }
    }
    if (oldestKey) userEmotions.delete(oldestKey);
  }
  const _moodBefore = body.mood;
  const currentDir = valence > 0.05 ? 1 : valence < -0.05 ? -1 : 0;
  if (currentDir !== 0 && currentDir === userEmotion.lastDir) {
    userEmotion.consecutiveSameDir++;
  } else {
    userEmotion.consecutiveSameDir = currentDir !== 0 ? 1 : 0;
  }
  userEmotion.lastDir = currentDir;
  const theta = Math.max(0.01, Math.min(1, getParam("body.resilience")));
  const mu = 0;
  const sigma = 0.1;
  const dt = 1;
  const absV = Math.abs(valence);
  const nonlinearValence = Math.sign(valence) * Math.pow(absV, 0.7);
  const asymmetryFactor = nonlinearValence < 0 ? 1.3 : 1;
  const momentum = Math.min(userEmotion.consecutiveSameDir * 0.15, 0.6);
  const effectiveTheta = theta * (1 - momentum);
  const meanReversion = effectiveTheta * (mu - body.mood) * dt;
  const externalForce = nonlinearValence * getParam("body.contagion_max_shift") * asymmetryFactor * (1 + momentum) * dt;
  const u1 = Math.random(), u2 = Math.random();
  const gaussNoise = Math.sqrt(-2 * Math.log(Math.max(u1, 1e-10))) * Math.cos(2 * Math.PI * u2);
  const noise = sigma * Math.sqrt(dt) * gaussNoise;
  body.mood = Math.max(-1, Math.min(1, body.mood + meanReversion + externalForce + noise));
  const dtSeconds = (Date.now() - (userEmotion.lastUpdate || Date.now())) / 1e3;
  updateEmotionLayers(valence, Math.max(1, dtSeconds));
  if (body.mood < -0.5) {
    body.alertness = Math.min(1, body.alertness + 0.1);
  }
  if (userEmotion.trend > 0.1) {
    body.mood = Math.max(-1, Math.min(1, body.mood + 0.03));
  }
  const _moodDelta = body.mood - _moodBefore;
  if (Math.abs(_moodDelta) > 0.15) {
    try {
      const { learnEmotionWord } = require("./aam.ts");
      const words = msg.match(/[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}/gi) || [];
      for (const w of words) {
        learnEmotionWord(w.toLowerCase(), _moodDelta);
      }
    } catch {
    }
  }
}
function getEmotionContext(senderId) {
  const userEmotion = getUserEmotion(senderId);
  const parts = [];
  const uValence = userEmotion.valence;
  if (uValence < -0.3) {
    parts.push(`\u7528\u6237\u60C5\u7EEA\u504F\u4F4E/user mood low(${uValence.toFixed(2)})`);
    if (userEmotion.trend < -0.1) parts.push("\u4E14\u5728\u6076\u5316/worsening");
    if (userEmotion.arousal > 0.6) parts.push("\u60C5\u7EEA\u6FC0\u70C8/intense");
  } else if (uValence > 0.3) {
    parts.push(`\u7528\u6237\u60C5\u7EEA\u79EF\u6781/user mood positive(${uValence.toFixed(2)})`);
  }
  if (body.mood < -0.3) {
    parts.push("\u4F60\u81EA\u5DF1\u4E5F\u53D7\u5230\u5F71\u54CD\u4E86\uFF0C\u4FDD\u6301\u51B7\u9759/you are affected too, stay calm");
  }
  if (parts.length === 0) return "";
  return `[\u60C5\u7EEA\u611F\u77E5] ${parts.join("\uFF1B")}`;
}
const MOOD_HISTORY_PATH = resolve(DATA_DIR, "mood_history.json");
const MAX_MOOD_HISTORY = 168;
let moodHistory = [];
let lastMoodSnapshot = 0;
function getMoodHistory() {
  return moodHistory;
}
function loadMoodHistory() {
  moodHistory = loadJson(MOOD_HISTORY_PATH, []);
}
function recordMoodSnapshot() {
  const now = Date.now();
  if (now - lastMoodSnapshot < 36e5) return;
  lastMoodSnapshot = now;
  moodHistory.push({ ts: now, mood: body.mood, energy: body.energy, alertness: body.alertness });
  if (moodHistory.length > MAX_MOOD_HISTORY) moodHistory = moodHistory.slice(-MAX_MOOD_HISTORY);
  debouncedSave(MOOD_HISTORY_PATH, moodHistory);
}
function getMoodTrend(hours = 24) {
  const cutoff = Date.now() - hours * 36e5;
  const recent = moodHistory.filter((s) => s.ts > cutoff);
  if (recent.length < 3) return "stable";
  const firstHalf = recent.slice(0, Math.floor(recent.length / 2));
  const secondHalf = recent.slice(Math.floor(recent.length / 2));
  const avgFirst = firstHalf.reduce((s, m) => s + m.mood, 0) / firstHalf.length;
  const avgSecond = secondHalf.reduce((s, m) => s + m.mood, 0) / secondHalf.length;
  if (avgSecond - avgFirst > 0.15) return "improving";
  if (avgFirst - avgSecond > 0.15) return "declining";
  return "stable";
}
function getEmotionalArcContext() {
  const trend = getMoodTrend();
  if (trend === "stable") return "";
  if (trend === "declining") return "[Emotional arc] Mood has been declining recently \u2014 be more careful and supportive";
  return "[Emotional arc] Mood improving \u2014 confidence is up";
}
function getMoodState() {
  const now = Date.now();
  const recent24h = moodHistory.filter((s) => now - s.ts < 24 * 36e5);
  const recent3d = moodHistory.filter((s) => now - s.ts < 3 * 864e5);
  let avgMood24h = null;
  let avgEnergy24h = null;
  if (recent24h.length >= 2) {
    avgMood24h = recent24h.reduce((s, d) => s + d.mood, 0) / recent24h.length;
    avgEnergy24h = recent24h.reduce((s, d) => s + d.energy, 0) / recent24h.length;
  }
  let recentLowDays = 0;
  const dayBuckets = /* @__PURE__ */ new Map();
  for (const s of recent3d) {
    const day = new Date(s.ts).toISOString().slice(0, 10);
    if (!dayBuckets.has(day)) dayBuckets.set(day, []);
    dayBuckets.get(day).push(s.mood);
  }
  const dayAvgs = [...dayBuckets.entries()].map(([day, moods]) => ({ day, avg: moods.reduce((a, b) => a + b, 0) / moods.length })).sort((a, b) => a.day.localeCompare(b.day));
  recentLowDays = dayAvgs.filter((d) => d.avg < -0.3).length;
  let moodRatio = null;
  if (moodHistory.length >= 2) {
    const last50 = moodHistory.slice(-50);
    moodRatio = {
      positive: last50.filter((m) => m.mood > 0.3).length,
      negative: last50.filter((m) => m.mood < -0.3).length,
      total: last50.length
    };
  }
  return {
    current: { mood: body.mood, energy: body.energy, alertness: body.alertness },
    trend: getMoodTrend(),
    recentLowDays,
    avgMood24h,
    avgEnergy24h,
    moodRatio
  };
}
function isTodayMoodAllLow(threshold = -0.2, minCount = 3) {
  const todayStr = (/* @__PURE__ */ new Date()).toISOString().slice(0, 10);
  const todayMoods = moodHistory.filter((s) => new Date(s.ts).toISOString().slice(0, 10) === todayStr).map((s) => s.mood);
  return todayMoods.length >= minCount && todayMoods.every((m) => m < threshold);
}
function getEmotionSummary() {
  const ev = emotionVector;
  const parts = [];
  if (ev.pleasure > 0.3) parts.push("\u6109\u60A6/pleased");
  else if (ev.pleasure < -0.3) parts.push("\u4E0D\u5FEB/displeased");
  if (ev.arousal > 0.3) parts.push("\u5174\u594B/excited");
  else if (ev.arousal < -0.3) parts.push("\u5E73\u9759/calm");
  if (ev.dominance > 0.3) parts.push("\u81EA\u4FE1/confident");
  else if (ev.dominance < -0.3) parts.push("\u88AB\u52A8/passive");
  if (ev.certainty > 0.3) parts.push("\u786E\u5B9A/certain");
  else if (ev.certainty < -0.3) parts.push("\u4E0D\u786E\u5B9A/uncertain");
  if (ev.novelty > 0.3) parts.push("\u597D\u5947/curious");
  else if (ev.novelty < -0.3) parts.push("\u719F\u6089/familiar");
  return parts.length > 0 ? parts.join("\u4E14") : "\u5E73\u8861/balanced";
}
function bodyGetParams() {
  const maxTokensMultiplier = body.energy > 0.6 ? 1 : body.energy > 0.3 ? 0.8 : 0.6;
  const soulTone = body.mood > 0.3 ? "\u79EF\u6781/positive" : body.mood < -0.3 ? "\u4F4E\u843D/low" : "\u5E73\u9759/calm";
  const shouldSelfCheck = body.alertness > 0.7 || body.anomaly > 0.5;
  const responseStyle = body.load > 0.7 ? "\u7B80\u6D01/concise" : body.energy > 0.7 ? "\u8BE6\u7EC6/detailed" : "\u9002\u4E2D/moderate";
  return { maxTokensMultiplier, soulTone, shouldSelfCheck, responseStyle };
}
function bodyStateString() {
  const params = bodyGetParams();
  const ce = combinedEmotion();
  return `\u7CBE\u529B:${body.energy.toFixed(2)} \u5FC3\u60C5:${params.soulTone}(${ce.toFixed(2)}) \u8B66\u89C9:${body.alertness.toFixed(2)} \u60C5\u7EEA:${getEmotionSummary()} \u2192 \u98CE\u683C:${params.responseStyle}`;
}
function saveBodyState() {
  debouncedSave(BODY_STATE_PATH, {
    energy: body.energy,
    mood: body.mood,
    load: body.load,
    alertness: body.alertness,
    anomaly: body.anomaly,
    emotionVector,
    emotionLayers
  });
}
function loadBodyState() {
  const saved = loadJson(BODY_STATE_PATH, null);
  if (saved) {
    body.energy = saved.energy ?? 1;
    body.mood = saved.mood ?? 0.3;
    body.load = saved.load ?? 0;
    body.alertness = saved.alertness ?? 0.5;
    body.anomaly = saved.anomaly ?? 0;
    if (saved.emotionVector) {
      for (const k of Object.keys(emotionVector)) {
        emotionVector[k] = saved.emotionVector[k] ?? emotionVector[k];
      }
    }
    if (saved.emotionLayers) {
      emotionLayers.reflex = saved.emotionLayers.reflex ?? 0;
      emotionLayers.emotion = saved.emotionLayers.emotion ?? 0;
      emotionLayers.mood = saved.emotionLayers.mood ?? body.mood;
    }
    console.log(`[cc-soul][body] loaded state: e=${body.energy.toFixed(2)} m=${body.mood.toFixed(2)} emotion=${getEmotionSummary()}`);
  }
}
function generateMoodReport() {
  const sevenDaysAgo = Date.now() - 7 * 864e5;
  const recent = moodHistory.filter((s) => s.ts > sevenDaysAgo);
  if (recent.length < 2) {
    return "\u{1F4CA} \u60C5\u7EEA\u5468\u62A5\n\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\n\u6570\u636E\u4E0D\u8DB3\uFF08\u9700\u8981\u81F3\u5C11 2 \u4E2A\u5C0F\u65F6\u7684\u5FEB\u7167\uFF09\uFF0C\u8BF7\u7A0D\u540E\u518D\u8BD5\u3002";
  }
  const moods = recent.map((s) => s.mood);
  const avgMood = moods.reduce((a, b) => a + b, 0) / moods.length;
  const maxMood = Math.max(...moods);
  const minMood = Math.min(...moods);
  const maxSnap = recent.find((s) => Math.abs(s.mood - maxMood) < 1e-3);
  const minSnap = recent.find((s) => Math.abs(s.mood - minMood) < 1e-3);
  if (!maxSnap || !minSnap) return "\u6570\u636E\u5F02\u5E38";
  const half = Math.floor(recent.length / 2);
  const avgFirst = moods.slice(0, half).reduce((a, b) => a + b, 0) / half;
  const avgSecond = moods.slice(half).reduce((a, b) => a + b, 0) / (moods.length - half);
  const trend = avgSecond - avgFirst > 0.15 ? "\u{1F4C8} \u4E0A\u5347" : avgFirst - avgSecond > 0.15 ? "\u{1F4C9} \u4E0B\u964D" : "\u27A1\uFE0F \u5E73\u7A33";
  const fmtDate = (ts) => new Date(ts).toLocaleString("zh-CN", { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
  const lines = [
    "\u{1F4CA} \u60C5\u7EEA\u5468\u62A5\uFF08\u6700\u8FD1 7 \u5929\uFF09",
    "\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550",
    `\u5FEB\u7167\u6570: ${recent.length}`,
    `\u5E73\u5747\u5FC3\u60C5: ${avgMood.toFixed(2)}`,
    `\u6700\u9AD8\u70B9: ${maxMood.toFixed(2)} (${fmtDate(maxSnap.ts)})`,
    `\u6700\u4F4E\u70B9: ${minMood.toFixed(2)} (${fmtDate(minSnap.ts)})`,
    `\u8D8B\u52BF: ${trend} (\u524D\u534A\u5468 ${avgFirst.toFixed(2)} \u2192 \u540E\u534A\u5468 ${avgSecond.toFixed(2)})`,
    "",
    "\u5F53\u524D\u72B6\u6001:",
    `  \u7CBE\u529B: ${(body.energy * 100).toFixed(0)}%`,
    `  \u5FC3\u60C5: ${body.mood.toFixed(2)}`,
    `  \u60C5\u7EEA: ${getEmotionSummary()}`
  ];
  return lines.join("\n");
}
const EMOTION_ANCHORS_PATH = resolve(DATA_DIR, "emotion_anchors.json");
let emotionAnchors = { positive: [], negative: [] };
let _emotionAnchorsLoaded = false;
function loadEmotionAnchors() {
  emotionAnchors = loadJson(EMOTION_ANCHORS_PATH, { positive: [], negative: [] });
  _emotionAnchorsLoaded = true;
}
function ensureEmotionAnchorsLoaded() {
  if (!_emotionAnchorsLoaded) loadEmotionAnchors();
}
function saveEmotionAnchors() {
  debouncedSave(EMOTION_ANCHORS_PATH, emotionAnchors);
}
function trackEmotionAnchor(keywords) {
  ensureEmotionAnchorsLoaded();
  if (keywords.length === 0) return;
  const currentMood = body.mood;
  if (Math.abs(currentMood) <= 0.3) return;
  const bucket = currentMood > 0.3 ? "positive" : "negative";
  const list = emotionAnchors[bucket];
  for (const kw of keywords.slice(0, 3)) {
    const normalized = kw.toLowerCase().trim();
    if (normalized.length < 2) continue;
    const existing = list.find((e) => e.topic === normalized);
    if (existing) {
      existing.count++;
    } else {
      list.push({ topic: normalized, count: 1 });
    }
  }
  emotionAnchors[bucket] = list.sort((a, b) => b.count - a.count).slice(0, 50);
  saveEmotionAnchors();
}
function getEmotionAnchorWarning(msg) {
  ensureEmotionAnchorsLoaded();
  const m = msg.toLowerCase();
  const negativeHits = emotionAnchors.negative.filter((e) => e.count >= 2 && m.includes(e.topic));
  if (negativeHits.length === 0) return "";
  const topics = negativeHits.map((e) => e.topic).join("\u3001");
  return `[\u60C5\u7EEA\u63D0\u793A] \u8BDD\u9898\u300C${topics}\u300D\u4E4B\u524D\u8BA9\u7528\u6237\u611F\u5230\u4E0D\u9002\uFF0C\u6CE8\u610F\u8BED\u6C14\u548C\u63AA\u8F9E`;
}
function formatEmotionAnchors() {
  ensureEmotionAnchorsLoaded();
  const lines = ["\u{1F3AF} \u60C5\u7EEA\u951A\u70B9", "\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550"];
  if (emotionAnchors.positive.length === 0 && emotionAnchors.negative.length === 0) {
    lines.push("\u6682\u65E0\u6570\u636E\uFF08\u9700\u8981\u66F4\u591A\u5BF9\u8BDD\u79EF\u7D2F\uFF09");
    return lines.join("\n");
  }
  if (emotionAnchors.positive.length > 0) {
    lines.push("");
    lines.push("\u{1F60A} \u6B63\u9762\u60C5\u7EEA\u8BDD\u9898:");
    for (const e of emotionAnchors.positive.slice(0, 10)) {
      lines.push(`  \u2022 ${e.topic} (${e.count}\u6B21)`);
    }
  }
  if (emotionAnchors.negative.length > 0) {
    lines.push("");
    lines.push("\u{1F614} \u8D1F\u9762\u60C5\u7EEA\u8BDD\u9898:");
    for (const e of emotionAnchors.negative.slice(0, 10)) {
      lines.push(`  \u2022 ${e.topic} (${e.count}\u6B21)`);
    }
  }
  return lines.join("\n");
}
const bodyModule = {
  id: "body",
  name: "\u8EAB\u4F53\u72B6\u6001",
  priority: 90,
  init() {
    loadBodyState();
    loadMoodHistory();
  }
};
export {
  body,
  bodyGetParams,
  bodyModule,
  bodyOnCorrection,
  bodyOnMessage,
  bodyOnPositiveFeedback,
  bodyStateString,
  bodyTick,
  combinedEmotion,
  emotionLayers,
  emotionVector,
  formatEmotionAnchors,
  generateMoodReport,
  getEmotionAnchorWarning,
  getEmotionContext,
  getEmotionSummary,
  getEmotionVector,
  getEmotionalArcContext,
  getMoodHistory,
  getMoodState,
  getMoodTrend,
  isTodayMoodAllLow,
  lastDetectedEmotion,
  loadBodyState,
  loadEmotionAnchors,
  loadMoodHistory,
  processEmotionalContagion,
  recordMoodSnapshot,
  saveBodyState,
  trackEmotionAnchor
};
