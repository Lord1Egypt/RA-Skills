import { resolve } from "path";
import { DATA_DIR, loadJson, debouncedSave } from "./persistence.ts";
const DRIFT_PATH = resolve(DATA_DIR, "persona_drift.json");
const WINDOW_SIZE = 20;
const BUCKET_COUNT = 5;
const ENTROPY_THRESHOLD = 1.5;
const WARNING_COOLDOWN = 6e5;
const DIMENSION_KEYS = [
  "length",
  "questionFreq",
  "codeFreq",
  "formality",
  "depth"
];
let state = {
  windows: {},
  lastEntropy: {},
  lastWarningTs: 0
};
function load() {
  state = loadJson(DRIFT_PATH, {
    windows: {},
    lastEntropy: {},
    lastWarningTs: 0
  });
}
function save() {
  debouncedSave(DRIFT_PATH, state);
}
function sentences(text) {
  return text.split(/[.!?。！？]+/).filter((s) => s.trim().length > 0);
}
function extractStyle(text) {
  const len = text.length;
  const sents = sentences(text);
  const sentCount = Math.max(sents.length, 1);
  const questionMarks = (text.match(/[?？]/g) || []).length;
  const questionFreq = Math.min(questionMarks / sentCount, 1);
  let codeChars = 0;
  const codeBlocks = text.match(/```[\s\S]*?```/g) || [];
  for (const block of codeBlocks) codeChars += block.length;
  const codeFreq = len > 0 ? Math.min(codeChars / len, 1) : 0;
  const formalMarkers = (text.match(/\b(therefore|furthermore|consequently|however|nevertheless|regarding|accordingly|hence|thus|moreover)\b/gi) || []).length;
  const casualMarkers = (text.match(/\b(yeah|ok|cool|lol|haha|gonna|wanna|kinda|btw|nah)\b/gi) || []).length;
  const totalMarkers = formalMarkers + casualMarkers;
  const formality = totalMarkers > 0 ? formalMarkers / totalMarkers : 0.5;
  const longSents = sents.filter((s) => s.trim().length > 80).length;
  const depth = longSents / sentCount;
  return {
    length: len,
    questionFreq,
    codeFreq,
    formality,
    depth
  };
}
function dimensionEntropy(values) {
  if (values.length < 2) return 0;
  const min = Math.min(...values);
  const max = Math.max(...values);
  const range = max - min;
  if (range === 0) return 0;
  const counts = new Array(BUCKET_COUNT).fill(0);
  for (const v of values) {
    let bucket = Math.floor((v - min) / range * BUCKET_COUNT);
    if (bucket >= BUCKET_COUNT) bucket = BUCKET_COUNT - 1;
    counts[bucket]++;
  }
  const n = values.length;
  let entropy = 0;
  for (const c of counts) {
    if (c === 0) continue;
    const p = c / n;
    entropy -= p * Math.log2(p);
  }
  return entropy;
}
function computeEntropy(entries) {
  if (entries.length < 3) return 0;
  let totalEntropy = 0;
  for (const dim of DIMENSION_KEYS) {
    const values = entries.map((e) => e.vector[dim]);
    const normValues = dim === "length" ? (() => {
      const mx = Math.max(...values, 1);
      return values.map((v) => v / mx);
    })() : values;
    totalEntropy += dimensionEntropy(normValues);
  }
  return totalEntropy / DIMENSION_KEYS.length;
}
function trackPersonaStyle(responseText, personaId) {
  if (!responseText || responseText.length < 10) return;
  const vector = extractStyle(responseText);
  const entry = { ts: Date.now(), personaId, vector };
  if (!state.windows[personaId]) state.windows[personaId] = [];
  const win = state.windows[personaId];
  win.push(entry);
  if (win.length > WINDOW_SIZE) {
    state.windows[personaId] = win.slice(-WINDOW_SIZE);
  }
  state.lastEntropy[personaId] = computeEntropy(state.windows[personaId]);
  save();
}
function getPersonaDriftWarning() {
  const now = Date.now();
  if (now - state.lastWarningTs < WARNING_COOLDOWN) return null;
  for (const [pid, entropy] of Object.entries(state.lastEntropy)) {
    if (entropy > ENTROPY_THRESHOLD) {
      const win = state.windows[pid];
      const sampleSize = win?.length ?? 0;
      state.lastWarningTs = now;
      save();
      return `[persona-drift] \u26A0 persona "${pid}" entropy=${entropy.toFixed(3)} (threshold ${ENTROPY_THRESHOLD}, window=${sampleSize}) \u2014 style is unstable, consider anchoring persona traits`;
    }
  }
  return null;
}
const COMFORTER_EMPATHY = /(?:理解|明白|辛苦|不容易|没关系|别担心|慢慢来|陪你|心疼|加油|抱抱|放心|支持你|感同身受|understand|sorry|hear you|it's ok|hang in there)/i;
const SOCRATIC_QUESTION = /[?？]/g;
const MENTOR_MIN_LENGTH = 50;
const PERSONA_RULES = [
  {
    id: "comforter",
    check: (text) => COMFORTER_EMPATHY.test(text) ? 0 : 0.7
  },
  {
    id: "socratic",
    check: (text) => {
      const qCount = (text.match(SOCRATIC_QUESTION) || []).length;
      return qCount > 0 ? 0 : 0.8;
    }
  },
  {
    id: "mentor",
    check: (text) => text.length < MENTOR_MIN_LENGTH ? 0.6 : 0
  }
];
function vectorDriftScore(replyVector, idealVector) {
  let sumSq = 0;
  const dims = ["length", "questionFreq", "codeFreq", "formality", "depth"];
  for (const d of dims) {
    const diff = (replyVector[d] || 0) - (idealVector[d] || 0);
    sumSq += diff * diff;
  }
  return Math.sqrt(sumSq) / 2.236;
}
let driftCount = 0;
function getDriftCount() {
  return driftCount;
}
let _pendingReinforcement = null;
function checkPersonaDrift(replyText, personaId, personaName, personaTone, idealVector) {
  if (!replyText || replyText.length < 10) return 0;
  const replyVector = extractStyle(replyText);
  let score = 0;
  const rule = PERSONA_RULES.find((r) => r.id === personaId);
  if (rule) {
    score = Math.max(score, rule.check(replyText, replyVector));
  }
  if (idealVector) {
    const vScore = vectorDriftScore(replyVector, idealVector);
    score = Math.max(score, vScore);
  }
  if (score > 0.5) {
    driftCount++;
    _pendingReinforcement = `[\u4EBA\u683C\u589E\u5F3A] \u4F60\u5F53\u524D\u89D2\u8272\u662F\u300C${personaName}\u300D\uFF0C\u8BF7\u4FDD\u6301\u300C${personaTone}\u300D\u98CE\u683C\u3002drift_score=${score.toFixed(2)}`;
    console.log(`[persona-drift] rule-based drift detected: persona=${personaId} score=${score.toFixed(2)} driftCount=${driftCount}`);
  }
  return score;
}
function getPersonaDriftReinforcement() {
  const msg = _pendingReinforcement;
  _pendingReinforcement = null;
  return msg;
}
const personaDriftModule = {
  id: "persona-drift",
  name: "\u4EBA\u683C\u6F02\u79FB\u68C0\u6D4B",
  priority: 30,
  init() {
    load();
    console.log(`[persona-drift] loaded \u2014 tracking ${Object.keys(state.windows).length} persona(s)`);
  },
  dispose() {
    debouncedSave(DRIFT_PATH, state, 0);
  },
  /** Inject drift warning into bootstrap if detected */
  onBootstrap() {
    const warning = getPersonaDriftWarning();
    if (warning) return warning;
  },
  /** After each reply, track style (if personaId available in event) */
  onSent(event) {
    const text = event?.response ?? event?.assistantMessage ?? "";
    const pid = event?.personaId ?? event?.persona ?? "default";
    if (text) trackPersonaStyle(text, pid);
  }
};
export {
  checkPersonaDrift,
  getDriftCount,
  getPersonaDriftReinforcement,
  getPersonaDriftWarning,
  personaDriftModule,
  trackPersonaStyle
};
