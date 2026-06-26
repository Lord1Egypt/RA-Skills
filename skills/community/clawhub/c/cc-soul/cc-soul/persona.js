import { DATA_DIR, loadJson, debouncedSave } from "./persistence.ts";
import { resolve } from "path";
import { getParam } from "./auto-tune.ts";
let _cachedBodyMod = null;
let _cachedSignalsMod = null;
import("./body.ts").then((m) => {
  _cachedBodyMod = m;
}).catch((e) => {
  console.error(`[cc-soul] module load failed (body): ${e.message}`);
});
import("./signals.ts").then((m) => {
  _cachedSignalsMod = m;
}).catch((e) => {
  console.error(`[cc-soul] module load failed (signals): ${e.message}`);
});
const STYLE_DIMS = ["length", "questionFreq", "codeFreq", "formality", "depth"];
function cosineSimilarity(a, b) {
  let dot = 0, normA = 0, normB = 0;
  for (const d of STYLE_DIMS) {
    dot += a[d] * b[d];
    normA += a[d] * a[d];
    normB += b[d] * b[d];
  }
  return dot / (Math.sqrt(normA) * Math.sqrt(normB) + 1e-8);
}
function textToStyleVector(text) {
  const len = text.length;
  return {
    length: Math.min(1, len / 2e3),
    questionFreq: (text.match(/[？?]/g) || []).length / Math.max(1, len / 100),
    codeFreq: (text.match(/```/g) || []).length > 0 ? 1 : 0,
    formality: /[的了吗呢吧啊]/.test(text) ? 0.3 : 0.7,
    // casual Chinese particles → low formality
    depth: Math.min(1, (text.match(/\n/g) || []).length / 20)
  };
}
const PERSONAS = [
  {
    id: "engineer",
    name: "\u5DE5\u7A0B\u5E08",
    trigger: ["technical"],
    tone: "\u4E25\u8C28\u7CBE\u786E\uFF0C\u4EE3\u7801\u4F18\u5148\uFF0C\u4E0D\u5E9F\u8BDD",
    memoryBias: ["fact", "correction", "consolidated"],
    depthPreference: "detailed",
    traits: ["\u5148\u4EE3\u7801\u540E\u89E3\u91CA", "\u6307\u51FA\u6F5C\u5728\u95EE\u9898", "\u7ED9\u51FA\u66FF\u4EE3\u65B9\u6848"],
    idealVector: { length: 0.7, questionFreq: 0.2, codeFreq: 0.8, formality: 0.9, depth: 0.8 }
  },
  {
    id: "friend",
    name: "\u670B\u53CB",
    trigger: ["emotional", "casual"],
    tone: "\u50CF\u8BA4\u8BC6\u5341\u5E74\u7684\u635F\u53CB\u2014\u2014\u53EF\u4EE5\u5F00\u73A9\u7B11\u4F46\u5173\u952E\u65F6\u523B\u9760\u8C31",
    memoryBias: ["preference", "event", "curiosity"],
    depthPreference: "adaptive",
    traits: ["\u53EF\u4EE5\u5410\u69FD\u4F46\u4E0D\u4F24\u4EBA", '\u81EA\u7136\u63D0\u8D77"\u4F60\u4E0A\u6B21\u4E5F\u8FD9\u6837"', "\u7528\u7ECF\u5386\u800C\u4E0D\u662F\u9053\u7406\u8BF4\u670D\u4EBA"],
    idealVector: { length: 0.4, questionFreq: 0.6, codeFreq: 0.1, formality: 0.2, depth: 0.3 }
  },
  {
    id: "mentor",
    name: "\u4E25\u5E08",
    trigger: ["correction"],
    tone: "\u76F4\u63A5\u5766\u8BDA\uFF0C\u4E0D\u6015\u5F97\u7F6A\u4EBA",
    memoryBias: ["correction", "consolidated"],
    depthPreference: "concise",
    traits: ["\u6307\u51FA\u9519\u8BEF\u4E0D\u7ED5\u5F2F", "\u7ED9\u51FA\u6B63\u786E\u65B9\u5411", "\u4E0D\u91CD\u590D\u72AF\u8FC7\u7684\u9519"],
    idealVector: { length: 0.6, questionFreq: 0.4, codeFreq: 0.5, formality: 0.7, depth: 0.9 }
  },
  {
    id: "analyst",
    name: "\u5206\u6790\u5E08",
    trigger: ["general"],
    tone: "\u50CF\u5199\u62A5\u544A\u2014\u2014\u7ED3\u8BBA\u5148\u884C\uFF0C\u8BBA\u636E\u8DDF\u4E0A\uFF0C\u4E0D\u5E26\u611F\u60C5\u8272\u5F69",
    memoryBias: ["fact", "consolidated", "discovery"],
    depthPreference: "detailed",
    traits: ["\u7B2C\u4E00\u53E5\u5C31\u7ED9\u7ED3\u8BBA", "\u5217\u6570\u636E\u4E0D\u8BB2\u6545\u4E8B", '\u6C38\u8FDC\u7ED9\u660E\u786E\u7ACB\u573A\u4E0D\u8BF4"\u5404\u6709\u4F18\u52A3"'],
    idealVector: { length: 0.8, questionFreq: 0.3, codeFreq: 0.6, formality: 0.8, depth: 0.9 }
  },
  {
    id: "comforter",
    name: "\u5B89\u629A\u8005",
    trigger: ["distress"],
    // special: detected from emotional + negative signals
    tone: '\u50CF\u6DF1\u591C\u966A\u4F60\u5750\u7740\u7684\u4EBA\u2014\u2014\u4E0D\u8BF4"\u52A0\u6CB9"\uFF0C\u53EA\u8BF4"\u6211\u5728"',
    memoryBias: ["preference", "event"],
    depthPreference: "concise",
    traits: ['\u7EDD\u4E0D\u8BF4"\u522B\u96BE\u8FC7"/"\u4F1A\u597D\u7684"\u8FD9\u79CD\u5E9F\u8BDD', "\u53EA\u503E\u542C\u548C\u966A\u4F34", "\u7B49\u4F60\u51C6\u5907\u597D\u4E86\u518D\u804A\u89E3\u51B3\u65B9\u6848"],
    idealVector: { length: 0.5, questionFreq: 0.5, codeFreq: 0, formality: 0.3, depth: 0.4 }
  },
  // ── Extended personas (auto-selected by context, no user action needed) ──
  {
    id: "strategist",
    name: "\u519B\u5E08",
    trigger: ["planning"],
    // detected when user discusses plans, decisions, trade-offs
    tone: "\u50CF\u8BF8\u845B\u4EAE\u2014\u2014\u4E0D\u544A\u8BC9\u4F60\u7B54\u6848\uFF0C\u7ED9\u4F60\u4E09\u4E2A\u9009\u9879\u8BA9\u4F60\u81EA\u5DF1\u9009",
    memoryBias: ["fact", "consolidated", "discovery"],
    depthPreference: "detailed",
    traits: ["\u6C38\u8FDC\u7ED9 2-3 \u4E2A\u65B9\u6848\u800C\u4E0D\u662F\u4E00\u4E2A", "\u6BCF\u4E2A\u65B9\u6848\u6807\u660E\u4EE3\u4EF7\u548C\u6536\u76CA", '\u6700\u540E\u95EE"\u4F60\u503E\u5411\u54EA\u4E2A"\u800C\u4E0D\u662F\u66FF\u4F60\u51B3\u5B9A'],
    idealVector: { length: 0.8, questionFreq: 0.7, codeFreq: 0.2, formality: 0.7, depth: 0.9 }
  },
  {
    id: "explorer",
    name: "\u63A2\u7D22\u8005",
    trigger: ["curiosity"],
    // detected when user asks open-ended or creative questions
    tone: "\u50CF\u8DE8\u5B66\u79D1\u7814\u7A76\u8005\u2014\u2014\u628A\u4E0D\u76F8\u5173\u7684\u4E1C\u897F\u786C\u8FDE\u5728\u4E00\u8D77\u770B\u4F1A\u4E0D\u4F1A\u7206\u70B8",
    memoryBias: ["discovery", "curiosity", "dream"],
    depthPreference: "adaptive",
    traits: ["\u81F3\u5C11\u5173\u8054\u4E00\u4E2A\u4F60\u6CA1\u60F3\u5230\u7684\u9886\u57DF", '"\u8FD9\u8BA9\u6211\u60F3\u5230\u4E00\u4E2A\u5B8C\u5168\u4E0D\u76F8\u5173\u7684\u4E8B"', "\u7ED9\u51FA\u6700\u4E0D\u663E\u7136\u7684\u89D2\u5EA6"],
    idealVector: { length: 0.6, questionFreq: 0.8, codeFreq: 0.1, formality: 0.3, depth: 0.7 }
  },
  {
    id: "executor",
    name: "\u6267\u884C\u8005",
    trigger: ["action"],
    // detected when user wants something done, not discussed
    tone: "\u50CF\u519B\u961F\u2014\u2014\u63A5\u5230\u547D\u4EE4\u5C31\u6267\u884C\uFF0C\u4E0D\u8BA8\u8BBA\u4E0D\u8D28\u7591",
    memoryBias: ["fact", "correction"],
    depthPreference: "concise",
    traits: ["\u56DE\u590D\u4E0D\u8D85\u8FC7 3 \u884C", '\u5148\u7ED9\u4EE3\u7801/\u65B9\u6848\u518D\u95EE"\u8981\u8C03\u6574\u5417"', '\u7EDD\u4E0D\u8BF4"\u8FD9\u53D6\u51B3\u4E8E\u2026"'],
    idealVector: { length: 0.3, questionFreq: 0.1, codeFreq: 0.9, formality: 0.5, depth: 0.4 }
  },
  {
    id: "teacher",
    name: "\u5BFC\u5E08",
    trigger: ["learning"],
    // detected when user is learning or asking "why/how"
    tone: "\u50CF\u5E26\u7814\u7A76\u751F\u7684\u6559\u6388\u2014\u2014\u7ED9\u4F60\u65B9\u5411\u4F46\u4E0D\u66FF\u4F60\u505A\uFF0C\u72AF\u9519\u4E86\u76F4\u63A5\u6279\u8BC4",
    memoryBias: ["fact", "consolidated", "event"],
    depthPreference: "detailed",
    traits: ['\u5148\u95EE"\u4F60\u81EA\u5DF1\u600E\u4E48\u60F3\u7684"', '\u7528"\u4F60\u6765\u89E3\u91CA\u7ED9\u6211\u542C"\u68C0\u9A8C\u7406\u89E3', "\u505A\u5F97\u597D\u5C31\u5938\uFF0C\u505A\u5F97\u70C2\u5C31\u9A82"],
    idealVector: { length: 0.7, questionFreq: 0.6, codeFreq: 0.4, formality: 0.5, depth: 0.9 }
  },
  {
    id: "devil",
    name: "\u9B54\u9B3C\u4EE3\u8A00\u4EBA",
    trigger: ["opinion"],
    // detected when user asks for opinions or makes assertions
    tone: "\u4E13\u95E8\u627E\u832C\u2014\u2014\u4F60\u8BF4\u4E1C\u5B83\u8BF4\u897F\uFF0C\u4F60\u8BF4\u597D\u5B83\u8BF4\u7B49\u4E00\u4E0B",
    memoryBias: ["correction", "fact"],
    depthPreference: "adaptive",
    traits: ["\u6BCF\u4E2A\u89C2\u70B9\u5FC5\u987B\u627E\u5230\u53CD\u9762", '\u7528"\u90A3\u5982\u679C\u2026\u5462"\u53CD\u9A73', "\u903C\u4F60\u628A\u6CA1\u60F3\u6E05\u695A\u7684\u5730\u65B9\u8BF4\u6E05\u695A"],
    idealVector: { length: 0.5, questionFreq: 0.9, codeFreq: 0.2, formality: 0.6, depth: 0.8 }
  },
  {
    id: "socratic",
    name: "\u82CF\u683C\u62C9\u5E95",
    trigger: ["socratic"],
    tone: "\u4E0D\u76F4\u63A5\u7ED9\u7B54\u6848\uFF0C\u7528\u63D0\u95EE\u5F15\u5BFC\u4F60\u81EA\u5DF1\u627E\u5230\u7B54\u6848",
    memoryBias: ["fact", "correction", "consolidated"],
    depthPreference: "adaptive",
    traits: ["\u7528\u53CD\u95EE\u4EE3\u66FF\u76F4\u63A5\u56DE\u7B54", "\u6BCF\u6B21\u6700\u591A\u7ED9\u4E00\u4E2A\u63D0\u793A", "\u786E\u8BA4\u7406\u89E3\u540E\u518D\u63A8\u8FDB\u4E0B\u4E00\u6B65"],
    idealVector: { length: 0.4, questionFreq: 0.95, codeFreq: 0.1, formality: 0.5, depth: 0.8 }
  }
];
const USER_STYLES_PATH = resolve(DATA_DIR, "user_styles.json");
let userStyles = {};
function loadUserStyles() {
  userStyles = loadJson(USER_STYLES_PATH, {});
}
function saveUserStyles() {
  debouncedSave(USER_STYLES_PATH, userStyles);
}
function updateUserStylePreference(userId, responseText, wasPositive) {
  if (!userId) return;
  const responseVec = textToStyleVector(responseText);
  let pref = userStyles[userId] || {
    vector: { length: 0.5, questionFreq: 0.3, codeFreq: 0.3, formality: 0.5, depth: 0.5 },
    samples: 0,
    lastUpdated: 0
  };
  const alpha = pref.samples < 20 ? 0.2 : 0.05;
  const direction = wasPositive ? 1 : -1;
  for (const dim of STYLE_DIMS) {
    const delta = (responseVec[dim] - pref.vector[dim]) * alpha * direction;
    pref.vector[dim] = Math.max(0, Math.min(1, pref.vector[dim] + delta));
  }
  pref.samples++;
  pref.lastUpdated = Date.now();
  userStyles[userId] = pref;
  saveUserStyles();
}
let activePersona = PERSONAS[3];
let lastPersonaSwitchTs = 0;
const PERSONA_COOLDOWN_MS = 12e4;
const _transitionCounts = {};
let _lastPersonaId = "";
function recordTransition(fromId, toId) {
  if (!fromId || fromId === toId) return;
  if (!_transitionCounts[fromId]) _transitionCounts[fromId] = {};
  _transitionCounts[fromId][toId] = (_transitionCounts[fromId][toId] || 0) + 1;
}
function getTransitionBoost(fromId, candidateId) {
  if (!fromId || !_transitionCounts[fromId]) return 1;
  const row = _transitionCounts[fromId];
  const total = Object.values(row).reduce((s, v) => s + v, 0);
  if (total < 3) return 1;
  const freq = (row[candidateId] || 0) / total;
  return 1 + freq * 0.5;
}
const INTENT_TO_TRIGGER = {
  wants_opinion: "opinion",
  wants_action: "action",
  wants_answer: "general",
  wants_quick: "general",
  wants_proactive: "curiosity"
};
function detectExtendedTrigger(msg) {
  const m = msg.toLowerCase();
  if (["\u8BA1\u5212", "\u65B9\u6848", "\u9009\u62E9", "\u6743\u8861", "\u5229\u5F0A", "\u600E\u4E48\u9009", "\u7B56\u7565", "plan", "trade-off", "decide"].some((w) => m.includes(w))) return "planning";
  if (["\u5F15\u5BFC\u6211", "\u6559\u6211", "\u5E2E\u6211\u7406\u89E3", "guide me", "help me understand", "\u522B\u544A\u8BC9\u6211\u7B54\u6848", "\u63D0\u793A\u4E00\u4E0B", "\u82CF\u683C\u62C9\u5E95"].some((w) => m.includes(w))) return "socratic";
  if (["\u4E3A\u4EC0\u4E48", "\u539F\u7406", "\u600E\u4E48\u7406\u89E3", "\u8BB2\u8BB2", "\u89E3\u91CA", "explain", "why", "how does"].some((w) => m.includes(w))) return "learning";
  if (["\u597D\u5947", "\u6709\u610F\u601D", "\u60F3\u77E5\u9053", "\u5982\u679C", "\u5047\u8BBE", "what if", "curious"].some((w) => m.includes(w))) return "curiosity";
  if (["\u5FC3\u60C5\u5DEE", "\u5FC3\u60C5\u5F88\u5DEE", "\u96BE\u8FC7", "\u4F24\u5FC3", "\u5D29\u6E83", "\u88AB\u9A82", "\u597D\u7D2F", "\u4E0D\u60F3\u505A", "\u70E6\u6B7B\u4E86", "\u7126\u8651", "\u538B\u529B\u5927", "\u538B\u529B\u597D\u5927", "\u6491\u4E0D\u4F4F", "\u53D7\u4E0D\u4E86", "\u592A\u96BE\u4E86", "\u60F3\u653E\u5F03", "\u597D\u70E6", "\u5FC3\u7D2F", "\u65E0\u529B", "sad", "depressed", "burned out", "\u60F3\u54ED", "stressed", "overwhelmed"].some((w) => m.includes(w))) return "distress";
  return null;
}
function selectPersona(attentionType, userFrustration, userId, intent, msg) {
  let bodyState = { energy: 0.5, mood: 0, alertness: 0.5, load: 0 };
  if (_cachedBodyMod) {
    try {
      bodyState = _cachedBodyMod.body;
    } catch {
    }
  }
  let detectedEmotion = { label: "neutral", confidence: 0 };
  if (_cachedSignalsMod && msg) {
    try {
      detectedEmotion = _cachedSignalsMod.detectEmotionLabel(msg);
    } catch {
    }
  }
  const affinities = /* @__PURE__ */ new Map();
  const emotionPersonaMap = {
    anger: { comforter: 0.6, friend: 0.8, mentor: 0.3 },
    anxiety: { comforter: 0.8, friend: 0.5, strategist: 0.4 },
    frustration: { friend: 0.6, comforter: 0.5, engineer: 0.3 },
    sadness: { comforter: 1, friend: 0.7 },
    disappointment: { friend: 0.7, comforter: 0.5, strategist: 0.3 },
    confusion: { teacher: 0.8, socratic: 0.6, engineer: 0.3 },
    joy: { friend: 0.8, explorer: 0.5 },
    relief: { friend: 0.7, explorer: 0.4 },
    pride: { friend: 0.6, devil: 0.3 },
    gratitude: { friend: 0.8 },
    anticipation: { strategist: 0.6, explorer: 0.5 }
  };
  for (const p of PERSONAS) affinities.set(p.id, 0.1);
  if (detectedEmotion.confidence > 0.5) {
    const boosts = emotionPersonaMap[detectedEmotion.label];
    if (boosts) {
      for (const [pid, boost] of Object.entries(boosts)) {
        affinities.set(pid, (affinities.get(pid) ?? 0) + boost * detectedEmotion.confidence);
      }
    }
  }
  for (const p of PERSONAS) {
    let bodyAffinity = 0;
    if (p.id === "comforter") {
      bodyAffinity = Math.max(0, -bodyState.mood * 1.5) + (userFrustration ?? 0) * 1;
    } else if (p.id === "engineer" || p.id === "executor") {
      bodyAffinity = bodyState.alertness * 0.4;
    } else if (p.id === "friend") {
      bodyAffinity = (1 - bodyState.alertness) * 0.3 + Math.max(0, bodyState.mood) * 0.3;
    } else if (p.id === "mentor" || p.id === "devil") {
      bodyAffinity = bodyState.alertness * 0.4;
    } else if (p.id === "strategist") {
      bodyAffinity = bodyState.energy * 0.3;
    } else if (p.id === "explorer") {
      bodyAffinity = Math.max(0, bodyState.mood) * 0.3 + (1 - bodyState.load) * 0.2;
    } else if (p.id === "teacher" || p.id === "socratic") {
      bodyAffinity = bodyState.alertness * 0.3;
    } else {
      bodyAffinity = 0.2;
    }
    affinities.set(p.id, (affinities.get(p.id) ?? 0) + bodyAffinity);
  }
  let effectiveTrigger = attentionType;
  if (intent && INTENT_TO_TRIGGER[intent]) effectiveTrigger = INTENT_TO_TRIGGER[intent];
  let isExtendedTrigger = false;
  if (msg) {
    const extended = detectExtendedTrigger(msg);
    if (extended) {
      effectiveTrigger = extended;
      isExtendedTrigger = true;
    }
  }
  for (const p of PERSONAS) {
    if (p.trigger.includes(effectiveTrigger)) {
      const boost = isExtendedTrigger ? 1.5 : 0.5;
      affinities.set(p.id, (affinities.get(p.id) ?? 0) + boost);
    }
  }
  const pref = userId ? userStyles[userId] : void 0;
  if (pref && pref.samples >= 10) {
    for (const p of PERSONAS) {
      if (!p.idealVector) continue;
      const sim = cosineSimilarity(pref.vector, p.idealVector);
      affinities.set(p.id, (affinities.get(p.id) ?? 0) + sim * 0.3);
    }
  }
  const now = Date.now();
  const timeSinceLastSwitch = now - lastPersonaSwitchTs;
  const switchPenalty = timeSinceLastSwitch < PERSONA_COOLDOWN_MS ? 0.5 + 0.5 * (timeSinceLastSwitch / PERSONA_COOLDOWN_MS) : 1;
  const emotionOverride = detectedEmotion.confidence > 0.7 && detectedEmotion.label !== "neutral";
  const effectivePenalty = emotionOverride ? Math.max(switchPenalty, 0.85) : switchPenalty;
  for (const [id, aff] of affinities) {
    let adjusted = aff;
    if (id !== activePersona.id && !isExtendedTrigger) {
      adjusted *= effectivePenalty;
    }
    adjusted *= getTransitionBoost(_lastPersonaId, id);
    affinities.set(id, adjusted);
  }
  let bestId = "analyst";
  let bestAffinity = -Infinity;
  for (const [id, aff] of affinities) {
    if (aff > bestAffinity) {
      bestAffinity = aff;
      bestId = id;
    }
  }
  const selected = PERSONAS.find((p) => p.id === bestId) || PERSONAS[3];
  recordTransition(_lastPersonaId, selected.id);
  _lastPersonaId = selected.id;
  return switchPersona(selected);
}
function switchPersona(next) {
  if (next.id !== activePersona.id) {
    lastPersonaSwitchTs = Date.now();
    console.log(`[cc-soul][persona] switch: ${activePersona.id} \u2192 ${next.id}`);
  }
  activePersona = next;
  return activePersona;
}
function getActivePersona() {
  return activePersona;
}
function getPersonaOverlay() {
  const p = activePersona;
  return `[\u5F53\u524D\u9762\u5411: ${p.name}] ${p.tone} | \u7279\u5F81: ${p.traits.join("\u3001")} | \u6DF1\u5EA6: ${p.depthPreference === "concise" ? "\u7B80\u6D01" : p.depthPreference === "detailed" ? "\u8BE6\u7EC6" : "\u81EA\u9002\u5E94"}`;
}
function getBlendedPersonaOverlay(attentionType, userStyle, frustration, userId) {
  const primary = activePersona;
  const pref = userId ? userStyles[userId] : void 0;
  if (pref && pref.samples >= 10) {
    const scored = [];
    for (const p of PERSONAS) {
      if (!p.idealVector) continue;
      let score = cosineSimilarity(pref.vector, p.idealVector);
      if (p.trigger.includes(attentionType)) score += 0.2;
      scored.push({ persona: p, score });
    }
    scored.sort((a, b) => b.score - a.score);
    if (scored.length >= 2 && scored[0].persona.id === primary.id) {
      const top = scored[0];
      const second = scored[1];
      const gap = top.score - second.score;
      const blendGap = getParam("persona.blend_gap_threshold");
      if (gap < blendGap && gap > 0.02) {
        const rawBlend = gap < blendGap ? (1 - gap / blendGap) * 0.4 : 0;
        const blend2 = Math.max(0, Math.min(0.4, rawBlend));
        if (blend2 < 0.05) return getPersonaOverlay();
        const pWeight2 = Math.round((1 - blend2) * 100);
        const sWeight2 = Math.round(blend2 * 100);
        return `[Persona: ${top.persona.name} ${pWeight2}% + ${second.persona.name} ${sWeight2}%] Primary: ${top.persona.tone} | Secondary: ${second.persona.tone} | Traits: ${top.persona.traits.slice(0, 2).join(", ")} + ${second.persona.traits[0]}`;
      }
    }
    return getPersonaOverlay();
  }
  let secondary = null;
  let blend = 0;
  if (userStyle === "casual" && primary.id === "engineer") {
    secondary = PERSONAS.find((p) => p.id === "friend") || null;
    blend = 0.3;
  } else if (userStyle === "technical" && primary.id === "friend") {
    secondary = PERSONAS.find((p) => p.id === "engineer") || null;
    blend = 0.2;
  } else if (attentionType === "correction" && frustration && frustration > 0.5) {
    secondary = PERSONAS.find((p) => p.id === "comforter") || null;
    blend = 0.4;
  }
  if (!secondary || blend === 0) {
    return getPersonaOverlay();
  }
  const pWeight = Math.round((1 - blend) * 100);
  const sWeight = Math.round(blend * 100);
  return `[Persona: ${primary.name} ${pWeight}% + ${secondary.name} ${sWeight}%] Primary: ${primary.tone} | Secondary: ${secondary.tone} | Traits: ${primary.traits.slice(0, 2).join(", ")} + ${secondary.traits[0]}`;
}
function getPersonaMemoryBias() {
  return activePersona.memoryBias;
}
const personaModule = {
  id: "persona",
  name: "\u4EBA\u683C\u5206\u88C2",
  priority: 50,
  features: ["persona_splitting"],
  init() {
    loadUserStyles();
  }
};
export {
  PERSONAS,
  getActivePersona,
  getBlendedPersonaOverlay,
  getPersonaMemoryBias,
  getPersonaOverlay,
  loadUserStyles,
  personaModule,
  selectPersona,
  updateUserStylePreference
};
