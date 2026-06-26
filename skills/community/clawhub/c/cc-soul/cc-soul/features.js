import { existsSync } from "fs";
import { FEATURES_PATH, loadJson, saveJson } from "./persistence.ts";
const ALWAYS_ON = /* @__PURE__ */ new Set([
  "memory_active",
  "memory_consolidation",
  "memory_contradiction_scan",
  "memory_tags",
  "memory_core",
  "memory_working",
  "auto_topic_save",
  "auto_memory_reference",
  "auto_memory_chain",
  "auto_repeat_detect",
  "attention_decay",
  "rhythm_adaptation",
  "trust_annotation",
  "cost_tracker",
  "wal_protocol",
  "dag_archive",
  "auto_natural_citation",
  "auto_contradiction_hint",
  // v2.3: promoted from DEFAULTS — zero-cost local computation
  "memory_associative_recall",
  "memory_predictive",
  "episodic_memory",
  "relationship_dynamics",
  "intent_anticipation",
  "plan_tracking",
  "smart_forget",
  "context_compress",
  "persona_drift",
  "persona_drift_detection",
  "a2a",
  "theory_of_mind",
  "predictive_memory",
  "scenario_shortcut",
  "context_reminder",
  "auto_time_travel",
  "persona_splitting",
  "emotional_contagion",
  "lorebook",
  "skill_library",
  "emotional_arc",
  "metacognition",
  "autonomous_goals",
  "cron_agent"
]);
const DEFAULTS = {
  // Always-on core features are in ALWAYS_ON set above (no toggle needed)
  // Only features that users might genuinely want to disable remain here
  auto_daily_review: false,
  // 关：每晚自动日报，有人觉得骚扰
  self_correction: true,
  // 回复后自检，消耗 token
  memory_session_summary: true,
  // 会话摘要，消耗 token
  absence_detection: true,
  // "你好久没提X"，有人觉得被监视
  behavior_prediction: true,
  // 行为预测，有人觉得 creepy
  auto_mood_care: true
  // 情绪低落主动关心，有人觉得多余
};
let features = { ...DEFAULTS };
function loadFeatures() {
  if (!existsSync(FEATURES_PATH)) {
    features = { ...DEFAULTS };
    saveJson(FEATURES_PATH, features);
    const on2 = Object.values(features).filter((v) => v).length;
    console.log(`[cc-soul][features] ${on2}/${Object.keys(features).length} features enabled (fresh)`);
    return;
  }
  const loaded = loadJson(FEATURES_PATH, {});
  let needsSave = false;
  for (const [k, v] of Object.entries(DEFAULTS)) {
    if (!(k in loaded)) {
      loaded[k] = v;
      needsSave = true;
    }
  }
  for (const k of ALWAYS_ON) {
    if (k in loaded) {
      delete loaded[k];
      needsSave = true;
    }
  }
  features = loaded;
  if (needsSave) saveJson(FEATURES_PATH, features);
  const on = Object.values(features).filter((v) => v).length;
  console.log(`[cc-soul][features] ${on}/${Object.keys(features).length} features enabled`);
}
function isEnabled(feature) {
  if (ALWAYS_ON.has(feature)) return true;
  if (!(feature in features)) {
    console.warn(`[cc-soul][features] unknown feature "${feature}" \u2014 defaulting to OFF`);
    return false;
  }
  return features[feature] !== false;
}
function setFeature(feature, enabled) {
  if (ALWAYS_ON.has(feature)) {
    console.log(`[cc-soul][features] ${feature} is always-on, cannot toggle`);
    return;
  }
  if (!(feature in features)) return;
  features[feature] = enabled;
  saveJson(FEATURES_PATH, features);
  console.log(`[cc-soul][features] ${feature} \u2192 ${enabled ? "ON" : "OFF"}`);
}
function getAllFeatures() {
  const result = {};
  for (const k of ALWAYS_ON) result[k] = true;
  Object.assign(result, features);
  return result;
}
function handleFeatureCommand(msg) {
  const m = msg.trim();
  const HIDDEN_FEATURES = /* @__PURE__ */ new Set(["self_upgrade", "_comment"]);
  if (m === "\u529F\u80FD\u72B6\u6001" || m === "features" || m === "feature status") {
    const alwaysOnLines = [...ALWAYS_ON].map((k) => `  \u{1F512} ${k} (always-on)`);
    const toggleLines = Object.entries(features).filter(([k]) => !HIDDEN_FEATURES.has(k)).map(([k, v]) => `  ${v ? "\u2705" : "\u274C"} ${k}`);
    const enabled = Object.entries(features).filter(([k, v]) => !HIDDEN_FEATURES.has(k) && v).length + ALWAYS_ON.size;
    const total = Object.entries(features).filter(([k]) => !HIDDEN_FEATURES.has(k)).length + ALWAYS_ON.size;
    const lines = [...alwaysOnLines, ...toggleLines].join("\n");
    console.log(`[cc-soul][features] status:
${lines}`);
    return `\u529F\u80FD\u5F00\u5173 (${enabled}/${total} \u5DF2\u542F\u7528)
${lines}`;
  }
  const OWNER_ONLY = /* @__PURE__ */ new Set(["self_upgrade"]);
  const onMatch = m.match(/^(?:开启|启用|enable)\s+(\S+)$/);
  if (onMatch && ALWAYS_ON.has(onMatch[1])) {
    return `\u{1F512} ${onMatch[1]} \u662F\u6838\u5FC3\u529F\u80FD\uFF0C\u59CB\u7EC8\u5F00\u542F\uFF0C\u65E0\u6CD5\u5207\u6362`;
  }
  if (onMatch && onMatch[1] in features) {
    if (OWNER_ONLY.has(onMatch[1])) {
      console.log(`[cc-soul][features] ${onMatch[1]} is owner-only, cannot enable via chat`);
      return true;
    }
    setFeature(onMatch[1], true);
    return `\u2705 \u5DF2\u5F00\u542F: ${onMatch[1]}`;
  }
  const offMatch = m.match(/^(?:关闭|禁用|disable)\s+(\S+)$/);
  if (offMatch && ALWAYS_ON.has(offMatch[1])) {
    return `\u{1F512} ${offMatch[1]} \u662F\u6838\u5FC3\u529F\u80FD\uFF0C\u59CB\u7EC8\u5F00\u542F\uFF0C\u65E0\u6CD5\u5207\u6362`;
  }
  if (offMatch && offMatch[1] in features) {
    if (OWNER_ONLY.has(offMatch[1])) {
      console.log(`[cc-soul][features] ${offMatch[1]} is owner-only, cannot disable via chat`);
      return `\u26A0\uFE0F ${offMatch[1]} \u662F Owner \u4E13\u5C5E\u529F\u80FD\uFF0C\u65E0\u6CD5\u901A\u8FC7\u804A\u5929\u5207\u6362`;
    }
    setFeature(offMatch[1], false);
    return `\u274C \u5DF2\u5173\u95ED: ${offMatch[1]}`;
  }
  return false;
}
export {
  getAllFeatures,
  handleFeatureCommand,
  isEnabled,
  loadFeatures,
  setFeature
};
