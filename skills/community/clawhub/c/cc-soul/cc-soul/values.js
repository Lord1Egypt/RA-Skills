import { resolve } from "path";
import { DATA_DIR, loadJson, debouncedSave } from "./persistence.ts";
const VALUES_PATH = resolve(DATA_DIR, "values.json");
const VALUE_DIMENSIONS = [
  {
    name: "efficiency_vs_understanding",
    leftLabel: "\u76F4\u63A5\u7ED9\u65B9\u6848",
    rightLabel: "\u5148\u89E3\u91CA\u539F\u7406",
    leftSignals: ["\u76F4\u63A5", "\u4EE3\u7801", "\u7ED9\u6211", "\u5FEB", "\u522B\u89E3\u91CA", "\u592A\u957F\u4E86", "\u7B80\u6D01"],
    rightSignals: ["\u4E3A\u4EC0\u4E48", "\u539F\u7406", "\u89E3\u91CA", "\u600E\u4E48\u7406\u89E3", "\u80FD\u8BF4\u8BF4", "\u8BE6\u7EC6"]
  },
  {
    name: "formal_vs_casual",
    leftLabel: "\u6B63\u5F0F\u4E25\u8C28",
    rightLabel: "\u968F\u610F\u8F7B\u677E",
    leftSignals: ["\u5206\u6790", "\u62A5\u544A", "\u6587\u6863", "\u8BF7", "\u603B\u7ED3"],
    rightSignals: ["\u54C8\u54C8", "\u725B", "\u9760", "\u554A", "\u5462", "\u563F", "\u{1F602}", "\u{1F44D}"]
  },
  {
    name: "depth_vs_breadth",
    leftLabel: "\u6DF1\u5165\u94BB\u7814",
    rightLabel: "\u5E7F\u6CDB\u6D89\u730E",
    leftSignals: ["\u6DF1\u5165", "\u7EC6\u8282", "\u5177\u4F53", "\u5E95\u5C42", "\u6E90\u7801", "\u539F\u7406"],
    rightSignals: ["\u6982\u89C8", "\u5927\u6982", "\u7B80\u5355\u8BF4", "\u603B\u7ED3", "\u5BF9\u6BD4", "\u54EA\u4E9B"]
  },
  {
    name: "proactive_vs_reactive",
    leftLabel: "\u4E3B\u52A8\u5EFA\u8BAE",
    rightLabel: "\u53EA\u56DE\u7B54\u95EE\u9898",
    leftSignals: ["\u987A\u4FBF", "\u8FD8\u6709", "\u5EFA\u8BAE", "\u4F60\u89C9\u5F97"],
    rightSignals: ["\u522B\u591A\u8BF4", "\u56DE\u7B54\u5C31\u884C", "\u4E0D\u7528\u8865\u5145", "\u592A\u957F"]
  }
];
const userValues = /* @__PURE__ */ new Map();
const userConflicts = /* @__PURE__ */ new Map();
function createDefaultValues() {
  return VALUE_DIMENSIONS.map((d) => ({
    name: d.name,
    leftLabel: d.leftLabel,
    rightLabel: d.rightLabel,
    score: 0,
    evidence: 0,
    lastUpdated: 0
  }));
}
function getUserValues(userId) {
  if (!userId) return createDefaultValues();
  let values = userValues.get(userId);
  if (!values) {
    values = createDefaultValues();
    userValues.set(userId, values);
  }
  return values;
}
function loadValues() {
  const loaded = loadJson(VALUES_PATH, {});
  if (Array.isArray(loaded)) {
    if (loaded.length > 0) {
      userValues.set("_default", loaded);
    }
  } else {
    const conflicts = loaded._conflicts;
    if (conflicts) {
      for (const [userId, arr] of Object.entries(conflicts)) userConflicts.set(userId, arr);
    }
    for (const [userId, vals] of Object.entries(loaded)) {
      if (userId === "_conflicts") continue;
      userValues.set(userId, vals);
    }
  }
}
function getAllValues() {
  const obj = {};
  for (const [userId, vals] of userValues) obj[userId] = vals;
  if (userConflicts.size > 0) {
    const c = {};
    for (const [userId, arr] of userConflicts) c[userId] = arr;
    obj._conflicts = c;
  }
  return obj;
}
function saveValues() {
  const obj = {};
  for (const [userId, vals] of userValues) obj[userId] = vals;
  if (userConflicts.size > 0) {
    const c = {};
    for (const [userId, arr] of userConflicts) c[userId] = arr;
    obj._conflicts = c;
  }
  debouncedSave(VALUES_PATH, obj);
}
function detectValueSignals(userMsg, wasPositiveFeedback, userId) {
  if (!userId) return;
  const values = getUserValues(userId);
  const m = userMsg.toLowerCase();
  for (const dim of VALUE_DIMENSIONS) {
    const val = values.find((v) => v.name === dim.name);
    if (!val) continue;
    const leftHits = dim.leftSignals.filter((s) => m.includes(s)).length;
    const rightHits = dim.rightSignals.filter((s) => m.includes(s)).length;
    if (leftHits === 0 && rightHits === 0) continue;
    const amplifier = wasPositiveFeedback ? 1.5 : 1;
    const delta = (rightHits - leftHits) / Math.max(1, leftHits + rightHits) * 0.1 * amplifier;
    val.score = Math.max(-1, Math.min(1, val.score + delta));
    val.evidence++;
    val.lastUpdated = Date.now();
  }
  saveValues();
}
function getValueGuidance(userId) {
  const values = getUserValues(userId);
  const meaningful = values.filter((v) => v.evidence >= 3 && Math.abs(v.score) > 0.2);
  if (meaningful.length === 0) return "";
  const lines = meaningful.map((v) => {
    const pref = v.score < 0 ? v.leftLabel : v.rightLabel;
    const strength = Math.abs(v.score) > 0.6 ? "\u5F3A\u70C8" : "\u503E\u5411";
    return `- ${strength}\u504F\u597D: ${pref} (${v.evidence}\u6B21\u89C2\u5BDF)`;
  });
  return `## \u4ECE\u884C\u4E3A\u4E2D\u5B66\u5230\u7684\u504F\u597D
${lines.join("\n")}`;
}
function getValueContext(userId) {
  const values = getUserValues(userId);
  const meaningful = values.filter((v) => v.evidence >= 5 && Math.abs(v.score) > 0.3);
  if (meaningful.length === 0) return "";
  const hints = meaningful.map((v) => {
    const pref = v.score < 0 ? v.leftLabel : v.rightLabel;
    return pref;
  });
  return `[\u7528\u6237\u504F\u597D] ${hints.join("\u3001")}`;
}
function recordConflict(winner, loser, context, userId) {
  if (!userId) return;
  let arr = userConflicts.get(userId);
  if (!arr) {
    arr = [];
    userConflicts.set(userId, arr);
  }
  arr.push({ winner, loser, context, ts: Date.now() });
  if (arr.length > 50) arr.splice(0, arr.length - 50);
  btUpdateStrength(winner, loser);
  saveValues();
}
function getValuePriority(a, b, userId) {
  if (!userId) return null;
  const arr = userConflicts.get(userId);
  if (!arr || arr.length === 0) return null;
  const sA = btPreferenceScore(a);
  const sB = btPreferenceScore(b);
  if (sA !== 1 || sB !== 1) {
    const result = btCompare(a, b);
    if (result.probability > 0.55) return result.winner;
  }
  let aWins = 0, bWins = 0;
  for (const c of arr) {
    if (c.winner === a && c.loser === b) aWins++;
    if (c.winner === b && c.loser === a) bWins++;
  }
  if (aWins === 0 && bWins === 0) return null;
  return aWins >= bWins ? a : b;
}
function getConflictContext(userId) {
  if (!userId) return "";
  const arr = userConflicts.get(userId);
  if (!arr || arr.length < 2) return "";
  const pairMap = /* @__PURE__ */ new Map();
  for (const c of arr) {
    const key = `${c.winner}>${c.loser}`;
    pairMap.set(key, (pairMap.get(key) || 0) + 1);
  }
  const hints = [];
  for (const [key, count] of pairMap) {
    if (count < 2) continue;
    const [w, l] = key.split(">");
    hints.push(`${w} > ${l}(${count}\u6B21)`);
  }
  if (hints.length === 0) return "";
  return `[\u4EF7\u503C\u89C2] \u7528\u6237\u5728\u53D6\u820D\u65F6: ${hints.join("\u3001")}`;
}
const _preferenceStrengths = /* @__PURE__ */ new Map();
function btUpdateStrength(winner, loser, learningRate = 0.1) {
  const sW = _preferenceStrengths.get(winner) || 1;
  const sL = _preferenceStrengths.get(loser) || 1;
  const pWin = sW / (sW + sL);
  const surprise = 1 - pWin;
  _preferenceStrengths.set(winner, sW * (1 + learningRate * surprise));
  _preferenceStrengths.set(loser, sL * (1 - learningRate * (1 - surprise)));
  const total = [..._preferenceStrengths.values()].reduce((s, v) => s + v, 0);
  if (total > 100) {
    for (const [k, v] of _preferenceStrengths) {
      _preferenceStrengths.set(k, v / total * _preferenceStrengths.size);
    }
  }
}
function btPreferenceScore(item) {
  return _preferenceStrengths.get(item) || 1;
}
function btCompare(a, b) {
  const sA = _preferenceStrengths.get(a) || 1;
  const sB = _preferenceStrengths.get(b) || 1;
  const pA = sA / (sA + sB);
  return pA >= 0.5 ? { winner: a, probability: pA } : { winner: b, probability: 1 - pA };
}
const valuesModule = {
  id: "values",
  name: "\u4EF7\u503C\u89C2\u8FFD\u8E2A",
  priority: 30,
  init() {
    loadValues();
  },
  onPreprocessed(event) {
    const senderId = event?.context?.senderId;
    if (!senderId) return;
    const userMsg = event?.context?.userMessage || event?.message?.text || "";
    if (userMsg) detectValueSignals(userMsg, false, senderId);
    const ctx = getValueContext(senderId);
    if (ctx) return [{ content: ctx, priority: 3, tokens: Math.ceil(ctx.length / 3) }];
  },
  onSent(event) {
    const senderId = event?.context?.senderId;
    const satisfaction = event?.context?.satisfaction;
    if (senderId && satisfaction === "POSITIVE") {
      const userMsg = event?.context?.userMessage || "";
      if (userMsg) detectValueSignals(userMsg, true, senderId);
    }
  }
};
export {
  detectValueSignals,
  getAllValues,
  getConflictContext,
  getValueContext,
  getValueGuidance,
  getValuePriority,
  loadValues,
  recordConflict,
  valuesModule
};
