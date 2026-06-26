import { existsSync, readFileSync, writeFileSync, mkdirSync, readdirSync } from "fs";
import { exec } from "child_process";
import { homedir } from "os";
import { resolve } from "path";
import {
  stats,
  formatMetrics,
  shortcuts,
  getPrivacyMode,
  setPrivacyMode,
  getSoulMode,
  setSoulMode
} from "./handler-state.ts";
import { loadJson, saveJson, DATA_DIR } from "./persistence.ts";
import { dbAddContextReminder, getDb } from "./sqlite-store.ts";
import { handleFeatureCommand } from "./features.ts";
import {
  memoryState,
  recall,
  addMemory,
  saveMemories,
  queryMemoryTimeline,
  ensureMemoriesLoaded,
  restoreArchivedMemories,
  trigrams,
  trigramSimilarity
} from "./memory.ts";
import { generateMoodReport, formatEmotionAnchors } from "./body.ts";
import { getCapabilityScore } from "./epistemic.ts";
const handleDashboardCommand = () => "\u8BE5\u529F\u80FD\u5DF2\u505C\u7528";
const generateMemoryMapHTML = () => "";
const generateDashboardHTML = () => "";
let _exportEvolutionAssets = null;
let _importEvolutionAssets = null;
import("./evolution.ts").then((m) => {
  _exportEvolutionAssets = m.exportEvolutionAssets;
  _importEvolutionAssets = m.importEvolutionAssets;
}).catch((e) => {
  console.error(`[cc-soul] module load failed (evolution): ${e.message}`);
});
import { handleTuneCommand } from "./auto-tune.ts";
import { ingestFile } from "./rag.ts";
import { getAllValues } from "./values.ts";
import { getActivePersona } from "./persona.ts";
import { checkTaskConfirmation } from "./tasks.ts";
import { replySender } from "./notify.ts";
import { executeSearch, executeMyMemories, executeStats, executeHealth, executeFeatures } from "./command-core.ts";
let getCostSummary = () => "\u6210\u672C\u8FFD\u8E2A\u6A21\u5757\u672A\u52A0\u8F7D";
import("./cost-tracker.ts").then((m) => {
  getCostSummary = m.getCostSummary;
}).catch((e) => {
  console.error(`[cc-soul] module load failed (cost-tracker): ${e.message}`);
});
let _lastDirectCmd = { content: "", ts: 0 };
function wasHandledByDirect(msg) {
  return _lastDirectCmd.content === msg.trim() && Date.now() - _lastDirectCmd.ts < 8e3;
}
function markHandledByDirect(msg) {
  _lastDirectCmd = { content: msg.trim(), ts: Date.now() };
}
function _sanitize(obj) {
  const s = JSON.stringify(obj).replace(/\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g, "[REDACTED]").replace(/\b(?:sk-|api[_-]?key|token|secret|password)[=:]\s*\S+/gi, "[REDACTED]");
  return JSON.parse(s);
}
function _readJson(p) {
  return loadJson(p, null);
}
function _fullBackup() {
  const d = DATA_DIR + "/export";
  if (!existsSync(d)) mkdirSync(d, { recursive: true });
  const files = {
    memories: "memories.json",
    rules: "rules.json",
    hypotheses: "hypotheses.json",
    personModel: "user_model.json",
    values: "values.json",
    features: "features.json",
    coreMemories: "core_memories.json",
    userProfiles: "user_profiles.json",
    theoryOfMind: "theory_of_mind.json",
    body: "body_state.json",
    emotionAnchors: "emotion_anchors.json",
    graph: "graph.json",
    lorebook: "lorebook.json",
    journal: "journal.json",
    workflows: "workflows.json",
    plans: "plans.json"
  };
  const bundle = { _meta: { version: 1, exportedAt: (/* @__PURE__ */ new Date()).toISOString(), source: "cc-soul" } };
  const counts = {};
  for (const [key, file] of Object.entries(files)) {
    const raw = _readJson(resolve(DATA_DIR, file));
    if (raw != null) {
      bundle[key] = raw;
      counts[key] = Array.isArray(raw) ? raw.length : Object.keys(raw).length;
    }
  }
  const apDir = resolve(DATA_DIR, "avatar_profiles");
  if (existsSync(apDir)) {
    const ap = {};
    for (const f of readdirSync(apDir).filter((f2) => f2.endsWith(".json"))) {
      const d2 = _readJson(resolve(apDir, f));
      if (d2) ap[f.replace(".json", "")] = d2;
    }
    if (Object.keys(ap).length) {
      bundle.avatarProfiles = ap;
      counts.avatarProfiles = Object.keys(ap).length;
    }
  }
  const sanitized = _sanitize(bundle);
  const ts = (/* @__PURE__ */ new Date()).toISOString().slice(0, 10);
  const outPath = `${d}/full_backup_${ts}.json`;
  writeFileSync(outPath, JSON.stringify(sanitized, null, 2), "utf-8");
  return { path: outPath, counts };
}
function _fullRestore(filePath) {
  const raw = JSON.parse(readFileSync(filePath, "utf-8"));
  if (!raw._meta?.source) throw new Error("\u4E0D\u662F\u6709\u6548\u7684 cc-soul \u5168\u91CF\u5907\u4EFD\u6587\u4EF6");
  const fileMap = {
    memories: "memories.json",
    rules: "rules.json",
    hypotheses: "hypotheses.json",
    personModel: "user_model.json",
    values: "values.json",
    features: "features.json",
    coreMemories: "core_memories.json",
    userProfiles: "user_profiles.json",
    theoryOfMind: "theory_of_mind.json",
    body: "body_state.json",
    emotionAnchors: "emotion_anchors.json",
    graph: "graph.json",
    lorebook: "lorebook.json",
    journal: "journal.json",
    workflows: "workflows.json",
    plans: "plans.json"
  };
  const counts = {};
  for (const [key, file] of Object.entries(fileMap)) {
    if (raw[key] != null) {
      writeFileSync(resolve(DATA_DIR, file), JSON.stringify(raw[key], null, 2), "utf-8");
      counts[key] = Array.isArray(raw[key]) ? raw[key].length : Object.keys(raw[key]).length;
    }
  }
  if (raw.avatarProfiles) {
    const apDir = resolve(DATA_DIR, "avatar_profiles");
    if (!existsSync(apDir)) mkdirSync(apDir, { recursive: true });
    for (const [uid, data] of Object.entries(raw.avatarProfiles)) {
      saveJson(resolve(apDir, `${uid}.json`), data);
    }
    counts.avatarProfiles = Object.keys(raw.avatarProfiles).length;
  }
  return counts;
}
let _replyCfg = null;
function setReplyCfg(cfg) {
  _replyCfg = cfg;
}
function cmdReply(ctx, event, session, text, userMsg) {
  session.lastPrompt = userMsg;
  console.log(`[cc-soul][cmdReply] sending reply (${text.length} chars): ${text.slice(0, 50)}...`);
  if (typeof ctx.reply === "function") ctx.reply(text);
  const evCtx = event?.context || {};
  const to = event?._replyTo || evCtx.conversationId || evCtx.chatId || "";
  replySender(to, text, _replyCfg || event?._replyCfg).then(() => console.log(`[cc-soul][cmdReply] sent OK`)).catch((e) => console.error(`[cc-soul][cmdReply] failed: ${e.message}`));
  ctx.bodyForAgent = "[\u7CFB\u7EDF] \u547D\u4EE4\u5DF2\u5904\u7406\uFF0C\u7ED3\u679C\u5DF2\u53D1\u9001\u3002";
}
const HELP_TEXT_FULL = `cc-soul \u547D\u4EE4\u6307\u5357

\u2501\u2501 \u81EA\u52A8\u8FD0\u884C\uFF08\u65E0\u9700\u64CD\u4F5C\uFF09 \u2501\u2501
\u2022 \u8BB0\u5FC6\uFF1A\u6BCF\u6761\u5BF9\u8BDD\u81EA\u52A8\u8BB0\u5F55\u3001\u53BB\u91CD\u3001\u8870\u51CF\u3001\u77DB\u76FE\u68C0\u6D4B
\u2022 \u4EBA\u683C\uFF1A11\u79CD\u4EBA\u683C\u6839\u636E\u5BF9\u8BDD\u5185\u5BB9\u81EA\u52A8\u5207\u6362\uFF08\u5DE5\u7A0B\u5E08/\u670B\u53CB/\u4E25\u5E08/\u5206\u6790\u5E08/\u5B89\u629A\u8005/\u519B\u5E08/\u63A2\u7D22\u8005/\u6267\u884C\u8005/\u5BFC\u5E08/\u9B54\u9B3C\u4EE3\u8A00\u4EBA/\u82CF\u683C\u62C9\u5E95\uFF09
\u2022 \u60C5\u7EEA\uFF1A\u5B9E\u65F6\u8FFD\u8E2A\u4F60\u7684\u60C5\u7EEA\uFF0C\u81EA\u52A8\u8C03\u6574\u56DE\u5E94\u98CE\u683C
\u2022 \u5B66\u4E60\uFF1A\u4ECE\u4F60\u7684\u7EA0\u6B63\u4E2D\u5B66\u4E60\u89C4\u5219\uFF0C3\u6B21\u9A8C\u8BC1\u540E\u6C38\u4E45\u751F\u6548
\u2022 \u4E3E\u4E00\u53CD\u4E09\uFF1A\u56DE\u7B54\u95EE\u9898\u65F6\u81EA\u52A8\u8865\u5145\u4F60\u53EF\u80FD\u9700\u8981\u7684\u76F8\u5173\u4FE1\u606F

\u2501\u2501 \u89E6\u53D1\u8BCD\uFF08\u8BF4\u51FA\u5373\u751F\u6548\uFF09 \u2501\u2501
\u2022 "\u5E2E\u6211\u7406\u89E3" / "\u5F15\u5BFC\u6211" / "\u522B\u544A\u8BC9\u6211\u7B54\u6848" \u2192 \u82CF\u683C\u62C9\u5E95\u6A21\u5F0F\uFF08\u7528\u63D0\u95EE\u5F15\u5BFC\u4F60\uFF09
\u2022 "\u9690\u79C1\u6A21\u5F0F" / "\u522B\u8BB0\u4E86" \u2192 \u6682\u505C\u8BB0\u5FC6 | "\u53EF\u4EE5\u4E86" \u2192 \u6062\u590D
\u2022 "\u4E0A\u6B21\u804A..." / "\u63A5\u7740\u804A..." \u2192 \u81EA\u52A8\u56DE\u5FC6\u76F8\u5173\u8BDD\u9898

\u2501\u2501 \u8BB0\u5FC6\u7BA1\u7406 \u2501\u2501
\u2022 \u6211\u7684\u8BB0\u5FC6 / my memories          \u2014 \u67E5\u770B\u6700\u8FD1\u8BB0\u5FC6
\u2022 \u641C\u7D22\u8BB0\u5FC6 <\u5173\u952E\u8BCD>               \u2014 \u641C\u7D22\u8BB0\u5FC6
\u2022 \u5220\u9664\u8BB0\u5FC6 <\u5173\u952E\u8BCD>               \u2014 \u5220\u9664\u5339\u914D\u8BB0\u5FC6
\u2022 pin \u8BB0\u5FC6 <\u5173\u952E\u8BCD>               \u2014 \u9489\u9009\uFF08\u6C38\u4E0D\u8870\u51CF\uFF09
\u2022 unpin \u8BB0\u5FC6 <\u5173\u952E\u8BCD>             \u2014 \u53D6\u6D88\u9489\u9009
\u2022 \u8BB0\u5FC6\u65F6\u95F4\u7EBF <\u5173\u952E\u8BCD>             \u2014 \u67E5\u770B\u53D8\u5316\u5386\u53F2
\u2022 \u8BB0\u5FC6\u5065\u5EB7                        \u2014 \u8BB0\u5FC6\u7EDF\u8BA1\u62A5\u544A
\u2022 \u8BB0\u5FC6\u5BA1\u8BA1                        \u2014 \u68C0\u67E5\u91CD\u590D/\u5F02\u5E38
\u2022 \u6062\u590D\u8BB0\u5FC6 <\u5173\u952E\u8BCD>               \u2014 \u6062\u590D\u5F52\u6863\u8BB0\u5FC6

\u2501\u2501 \u5BFC\u5165\u5BFC\u51FA \u2501\u2501
\u2022 \u5BFC\u51FA\u5168\u90E8 / export all / full backup \u2014 \u5168\u91CF\u5907\u4EFD\uFF08\u5DF2\u53BB\u654F\uFF09
\u2022 \u5BFC\u5165\u5168\u90E8 <\u8DEF\u5F84> / import all <path> \u2014 \u4ECE\u5168\u91CF\u5907\u4EFD\u6062\u590D
\u2022 \u5BFC\u51FAlorebook                    \u2014 \u5BFC\u51FA\u77E5\u8BC6\u5E93\uFF08\u53BB\u654F\uFF09
\u2022 \u5BFC\u51FA\u8FDB\u5316 / export evolution      \u2014 \u5BFC\u51FA GEP \u683C\u5F0F\u8FDB\u5316\u8D44\u4EA7
\u2022 \u5BFC\u5165\u8FDB\u5316 <\u8DEF\u5F84>                  \u2014 \u5BFC\u5165 GEP \u683C\u5F0F\u8FDB\u5316\u8D44\u4EA7
\u2022 \u6444\u5165\u6587\u6863 <\u8DEF\u5F84> / ingest <path> \u2014 \u5BFC\u5165\u6587\u6863\u5230\u8BB0\u5FC6

\u2501\u2501 \u72B6\u6001\u67E5\u770B \u2501\u2501
\u2022 stats                           \u2014 \u4E2A\u4EBA\u4EEA\u8868\u76D8
\u2022 soul state                      \u2014 AI \u80FD\u91CF/\u5FC3\u60C5/\u60C5\u7EEA
\u2022 \u60C5\u7EEA\u5468\u62A5 / mood report          \u2014 7\u5929\u60C5\u7EEA\u8D8B\u52BF
\u2022 \u80FD\u529B\u8BC4\u5206 / capability score     \u2014 \u5404\u9886\u57DF\u80FD\u529B\u8BC4\u5206
\u2022 \u6211\u7684\u6280\u80FD / my skills            \u2014 \u81EA\u52A8\u751F\u6210\u7684\u6280\u80FD\u5217\u8868
\u2022 metrics / \u76D1\u63A7                  \u2014 \u7CFB\u7EDF\u8FD0\u884C\u6307\u6807
\u2022 cost / \u6210\u672C                     \u2014 Token \u4F7F\u7528\u7EDF\u8BA1
\u2022 dashboard / \u4EEA\u8868\u76D8              \u2014 \u6253\u5F00\u7F51\u9875\u4EEA\u8868\u76D8
\u2022 \u8BB0\u5FC6\u56FE\u8C31 html                   \u2014 \u6253\u5F00\u8BB0\u5FC6\u53EF\u89C6\u5316
\u2022 \u5BF9\u8BDD\u6458\u8981                        \u2014 \u6700\u8FD1\u5BF9\u8BDD\u6458\u8981

\u2501\u2501 \u8BB0\u5FC6\u6D1E\u5BDF \u2501\u2501
\u2022 \u65F6\u95F4\u65C5\u884C <\u5173\u952E\u8BCD>               \u2014 \u8FFD\u8E2A\u67D0\u4E2A\u8BDD\u9898\u7684\u89C2\u70B9\u6F14\u53D8
\u2022 \u63A8\u7406\u94FE / reasoning chain        \u2014 \u67E5\u770B\u4E0A\u6B21\u56DE\u590D\u7528\u4E86\u54EA\u4E9B\u8BB0\u5FC6
\u2022 \u60C5\u7EEA\u951A\u70B9 / emotion anchors      \u2014 \u67E5\u770B\u8BDD\u9898\u4E0E\u60C5\u7EEA\u7684\u5173\u8054
\u2022 \u8BB0\u5FC6\u94FE\u8DEF <\u5173\u952E\u8BCD>               \u2014 \u641C\u7D22\u76F8\u5173\u8BB0\u5FC6\u5E76\u5C55\u793A\u5173\u8054\u94FE

\u2501\u2501 \u4F53\u9A8C\u529F\u80FD \u2501\u2501
\u2022 \u4FDD\u5B58\u8BDD\u9898 / save topic           \u2014 \u4FDD\u5B58\u5F53\u524D\u5BF9\u8BDD\u4E0A\u4E0B\u6587\u4E3A\u8BDD\u9898\u5206\u652F
\u2022 \u5207\u6362\u8BDD\u9898 <\u540D\u79F0> / switch topic  \u2014 \u6062\u590D\u4FDD\u5B58\u7684\u8BDD\u9898\u5206\u652F
\u2022 \u8BDD\u9898\u5217\u8868 / topic list           \u2014 \u67E5\u770B\u6240\u6709\u8BDD\u9898\u5206\u652F
\u2022 \u5171\u4EAB\u8BB0\u5FC6 <\u5173\u952E\u8BCD>               \u2014 \u5C06\u5339\u914D\u8BB0\u5FC6\u8BBE\u4E3A\u5168\u5C40\u5171\u4EAB
\u2022 \u79C1\u6709\u8BB0\u5FC6 <\u5173\u952E\u8BCD>               \u2014 \u5C06\u5339\u914D\u8BB0\u5FC6\u8BBE\u4E3A\u79C1\u6709

\u2501\u2501 \u9AD8\u7EA7\u529F\u80FD \u2501\u2501
\u2022 \u529F\u80FD\u72B6\u6001 / features             \u2014 \u67E5\u770B\u6240\u6709\u529F\u80FD\u5F00\u5173
\u2022 \u5F00\u542F <\u529F\u80FD> / \u5173\u95ED <\u529F\u80FD>       \u2014 \u5F00\u5173\u529F\u80FD
\u2022 \u5F00\u59CB\u5B9E\u9A8C <\u63CF\u8FF0>                 \u2014 \u542F\u52A8 A/B \u5B9E\u9A8C

\u5411\u91CF\u641C\u7D22\u5DF2\u9000\u5F79\uFF0CNAM \u8BB0\u5FC6\u5F15\u64CE\u5DF2\u8986\u76D6\u8BED\u4E49\u5339\u914D\u3002`;
const HELP_TEXT_DIRECT = `cc-soul \u547D\u4EE4\u6307\u5357

\u2501\u2501 \u81EA\u52A8\u8FD0\u884C\uFF08\u65E0\u9700\u64CD\u4F5C\uFF09 \u2501\u2501
\u2022 \u8BB0\u5FC6/\u4EBA\u683C/\u60C5\u7EEA/\u5B66\u4E60/\u4E3E\u4E00\u53CD\u4E09 \u5168\u81EA\u52A8

\u2501\u2501 \u547D\u4EE4 \u2501\u2501
\u5E2E\u52A9 \u2014 \u663E\u793A\u6B64\u6307\u5357
\u641C\u7D22\u8BB0\u5FC6 <\u5173\u952E\u8BCD> \u2014 \u641C\u7D22\u8BB0\u5FC6
\u6211\u7684\u8BB0\u5FC6 \u2014 \u67E5\u770B\u6700\u8FD1\u8BB0\u5FC6
stats \u2014 \u4E2A\u4EBA\u4EEA\u8868\u76D8
soul state \u2014 AI \u80FD\u91CF/\u5FC3\u60C5
\u60C5\u7EEA\u5468\u62A5 \u2014 7\u5929\u60C5\u7EEA\u8D8B\u52BF
\u80FD\u529B\u8BC4\u5206 \u2014 \u5404\u9886\u57DF\u8BC4\u5206
\u529F\u80FD\u72B6\u6001 \u2014 \u529F\u80FD\u5F00\u5173
\u8BB0\u5FC6\u5065\u5EB7 \u2014 \u8BB0\u5FC6\u7EDF\u8BA1
\u5BFC\u51FA\u5168\u90E8 / export all \u2014 \u5168\u91CF\u5907\u4EFD
\u5BFC\u5165\u5168\u90E8 <\u8DEF\u5F84> / import all \u2014 \u5168\u91CF\u6062\u590D
\u5BFC\u51FA\u8FDB\u5316 \u2014 \u5BFC\u51FA GEP \u683C\u5F0F\u8FDB\u5316\u8D44\u4EA7
\u5BFC\u5165\u8FDB\u5316 <\u8DEF\u5F84> \u2014 \u5BFC\u5165 GEP \u683C\u5F0F

\u2501\u2501 \u89E6\u53D1\u8BCD \u2501\u2501
"\u522B\u8BB0\u4E86" \u2192 \u6682\u505C\u8BB0\u5FC6 | "\u53EF\u4EE5\u4E86" \u2192 \u6062\u590D
"\u5E2E\u6211\u7406\u89E3" \u2192 \u82CF\u683C\u62C9\u5E95\u6A21\u5F0F`;
const COMMANDS = [
  // ── Help ──
  {
    pattern: /^(help|帮助|命令列表|commands)$/i,
    mode: "both",
    execute: () => HELP_TEXT_FULL
    // routeCommandDirect overrides with HELP_TEXT_DIRECT
  },
  // ── Privacy mode ON ──
  {
    pattern: /^(别记了|隐私模式|privacy mode)$/i,
    mode: "both",
    execute: () => {
      setPrivacyMode(true);
      console.log("[cc-soul] privacy mode ON");
      return '\u9690\u79C1\u6A21\u5F0F\u5DF2\u5F00\u542F\uFF0C\u5BF9\u8BDD\u5185\u5BB9\u4E0D\u4F1A\u88AB\u8BB0\u5FC6\u3002\u8BF4"\u53EF\u4EE5\u4E86"\u6062\u590D\u3002';
    }
  },
  // ── Privacy mode OFF ──
  {
    pattern: /^(可以了|关闭隐私|恢复记忆)$/i,
    mode: "both",
    execute: () => {
      if (!getPrivacyMode()) return null;
      setPrivacyMode(false);
      console.log("[cc-soul] privacy mode OFF");
      return "\u9690\u79C1\u6A21\u5F0F\u5DF2\u5173\u95ED\uFF0C\u6062\u590D\u8BB0\u5FC6\u3002";
    }
  },
  // ── Document ingest ──
  {
    pattern: /^(摄入文档|ingest)\s+(.+)$/i,
    mode: "write",
    execute: (m, c) => {
      const filePath = m[2].trim();
      const resolvedPath = resolve(filePath.replace(/^~/, homedir()));
      const safeRoots = [homedir(), "/tmp"];
      if (!safeRoots.some((root) => resolvedPath.startsWith(root))) {
        return "\u5B89\u5168\u9650\u5236\uFF1A\u53EA\u80FD\u5BFC\u5165\u5BB6\u76EE\u5F55\u6216 /tmp \u4E0B\u7684\u6587\u4EF6\u3002";
      }
      const count = ingestFile(filePath, c.senderId, c.channelId);
      if (count >= 0) {
        return `\u5DF2\u6444\u5165 ${count} \u4E2A\u7247\u6BB5\uFF0C\u6765\u6E90: "${filePath}"`;
      } else {
        return `\u6587\u4EF6\u8BFB\u53D6\u5931\u8D25: "${filePath}"\uFF0C\u8BF7\u68C0\u67E5\u8DEF\u5F84\u548C\u6743\u9650\u3002`;
      }
    }
  },
  // ── Metrics / 监控 ──
  {
    pattern: /^(metrics|监控|运行状态)$/i,
    mode: "write",
    execute: () => formatMetrics()
  },
  // ── Dashboard ──
  {
    pattern: /^(dashboard|仪表盘)$/i,
    mode: "write",
    execute: () => {
      const htmlPath = generateDashboardHTML();
      exec(`open "${htmlPath}"`);
      return `Dashboard generated and opened: ${htmlPath}`;
    }
  },
  // ── 记忆图谱 HTML ──
  {
    pattern: /^(记忆图谱\s*html|memory map\s*html)$/i,
    mode: "write",
    execute: () => {
      const htmlPath = generateMemoryMapHTML();
      exec(`open "${htmlPath}"`);
      return `\u5DF2\u751F\u6210\u8BB0\u5FC6\u56FE\u8C31 HTML \u5E76\u6253\u5F00: ${htmlPath}`;
    }
  },
  // ── 情绪周报 ──
  {
    pattern: /^(情绪周报|mood report)$/i,
    mode: "both",
    execute: () => {
      try {
        const report = generateMoodReport();
        return report || "\u6682\u65E0\u8DB3\u591F\u6570\u636E\u751F\u6210\u60C5\u7EEA\u5468\u62A5\u3002";
      } catch (_) {
        return "\u60C5\u7EEA\u5468\u62A5\u6682\u4E0D\u53EF\u7528";
      }
    }
  },
  // ── 能力评分 ──
  {
    pattern: /^(能力评分|capability score|capability)$/i,
    mode: "both",
    execute: () => {
      try {
        const score = getCapabilityScore();
        return typeof score === "string" ? score : JSON.stringify(score, null, 2);
      } catch (_) {
        return "\u80FD\u529B\u8BC4\u5206\u6682\u4E0D\u53EF\u7528";
      }
    }
  },
  // ── Cost / Token usage ──
  {
    pattern: /^(cost|token cost|token使用|成本)$/i,
    mode: "both",
    execute: () => getCostSummary()
  },
  // ── 开始实验 ──
  {
    pattern: /^开始实验(.*)$/i,
    mode: "write",
    execute: () => "\u5B9E\u9A8C\u529F\u80FD\u5DF2\u9000\u5F79\u3002\u53C2\u6570\u8C03\u4F18\u5DF2\u7531 auto-tune \u81EA\u52A8\u5904\u7406\u3002"
  },
  // ── 向量搜索退役提示 ──
  {
    pattern: /^(安装向量|install vector|向量状态|vector status)$/i,
    mode: "write",
    execute: () => "\u5411\u91CF\u641C\u7D22\u5DF2\u9000\u5F79\uFF0CNAM \u8BB0\u5FC6\u5F15\u64CE\u5DF2\u8986\u76D6\u8BED\u4E49\u5339\u914D\uFF0C\u65E0\u9700\u989D\u5916\u5B89\u88C5\u3002"
  },
  // ── 我的技能 ──
  {
    pattern: /^(我的技能|my skills)$/i,
    mode: "write",
    execute: () => {
      try {
        const skillsPath = resolve(DATA_DIR, "skills.json");
        const skills = loadJson(skillsPath, []);
        if (skills.length === 0) return "\u8FD8\u6CA1\u6709\u53D1\u73B0\u6280\u80FD\u3002\u591A\u804A\u51E0\u8F6E\u540E\u4F1A\u81EA\u52A8\u751F\u6210\u3002";
        const list = skills.slice(0, 10).map((s, i) => `${i + 1}. ${s.name || s.pattern || s.content?.slice(0, 40) || "\u672A\u547D\u540D"}`).join("\n");
        return `\u4F60\u7684\u6280\u80FD\uFF08${skills.length} \u4E2A\uFF09\uFF1A
${list}`;
      } catch {
        return "\u6280\u80FD\u5217\u8868\u6682\u4E0D\u53EF\u7528\u3002";
      }
    }
  },
  // ── 灵魂模式 ON ──
  {
    pattern: /^[\/]?灵魂模式\s*(.*)$/i,
    mode: "write",
    execute: (m) => {
      const speaker = m[1]?.trim() || "";
      setSoulMode(true, speaker);
      return speaker ? `\u7075\u9B42\u6A21\u5F0F\u5DF2\u5F00\u542F\uFF08\u8EAB\u4EFD\uFF1A${speaker}\uFF09\u3002\u53D1 /\u9000\u51FA\u7075\u9B42 \u53EF\u5173\u95ED\u3002` : `\u7075\u9B42\u6A21\u5F0F\u5DF2\u5F00\u542F\uFF0C\u4F1A\u81EA\u52A8\u8BC6\u522B\u5BF9\u65B9\u8EAB\u4EFD\u3002\u53D1 /\u9000\u51FA\u7075\u9B42 \u53EF\u5173\u95ED\uFF0C\u53D1 /\u6211\u662F <\u540D\u5B57> \u53EF\u6307\u5B9A\u8EAB\u4EFD\u3002`;
    }
  },
  // ── 灵魂模式 OFF ──
  {
    pattern: /^[\/]?(退出灵魂|关闭灵魂|灵魂模式关|soul.mode.off)$/i,
    mode: "write",
    execute: () => {
      setSoulMode(false);
      return `\u7075\u9B42\u6A21\u5F0F\u5DF2\u5173\u95ED\uFF0C\u6062\u590D\u6B63\u5E38\u5BF9\u8BDD\u3002`;
    }
  },
  // ── 灵魂模式切换身份 ──
  {
    pattern: /^[\/]?我是\s+(.+)$/i,
    mode: "write",
    execute: (m) => {
      if (!getSoulMode().active) return null;
      const newSpeaker = m[1].trim();
      setSoulMode(true, newSpeaker);
      return `\u597D\u7684\uFF0C\u73B0\u5728\u4F60\u662F\u300C${newSpeaker}\u300D\u3002`;
    }
  },
  // ── 我的记忆 ──
  {
    pattern: /^(我的记忆|my memories)$/i,
    mode: "both",
    execute: (_m, c) => executeMyMemories(c.senderId)
  },
  // ── 搜索记忆 ──
  {
    pattern: /^(搜索记忆|search memory)\s+(.+)$/i,
    mode: "both",
    execute: (m, c) => executeSearch(m[2].trim(), c.senderId)
  },
  // ── 删除记忆 ──
  {
    pattern: /^(删除记忆|delete memory)\s+(.+)$/i,
    mode: "write",
    execute: (m, c) => {
      const keyword = m[2].trim();
      const results = recall(keyword, 10, c.senderId);
      if (results.length === 0) return `\u6CA1\u6709\u627E\u5230\u5339\u914D\u300C${keyword}\u300D\u7684\u8BB0\u5FC6\u53EF\u5220\u9664\u3002`;
      ensureMemoriesLoaded();
      let expired = 0;
      for (const r of results) {
        const idx = memoryState.memories.findIndex((m2) => m2.ts === r.ts && m2.content === r.content);
        if (idx >= 0) {
          memoryState.memories[idx].scope = "expired";
          expired++;
        }
      }
      if (expired > 0) saveMemories();
      return `\u5DF2\u6807\u8BB0 ${expired} \u6761\u5339\u914D "${keyword}" \u7684\u8BB0\u5FC6\u4E3A\u8FC7\u671F\u3002`;
    }
  },
  // ── 导出 lorebook ──
  {
    pattern: /^(导出lorebook|export lorebook)$/i,
    mode: "write",
    execute: () => {
      const exportDir = DATA_DIR + "/export";
      if (!existsSync(exportDir)) mkdirSync(exportDir, { recursive: true });
      const lorebookPath = resolve(DATA_DIR, "lorebook.json");
      let raw = [];
      try {
        raw = loadJson(lorebookPath, []);
      } catch {
      }
      const sanitized = raw.filter((e) => e.enabled !== false).map((e) => ({
        keywords: e.keywords || [],
        content: (e.content || "").replace(/\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g, "[REDACTED]").replace(/\b(?:sk-|api[_-]?key|token|secret|password)[=:]\s*\S+/gi, "[REDACTED]"),
        category: e.category || "fact",
        priority: e.priority || 5
      }));
      const exportPath = `${exportDir}/lorebook_share.json`;
      writeFileSync(exportPath, JSON.stringify({ knowledge: sanitized, version: 1, exportedAt: (/* @__PURE__ */ new Date()).toISOString() }, null, 2), "utf-8");
      return `\u5DF2\u5BFC\u51FA ${sanitized.length} \u6761 lorebook \u5230 ${exportPath}\uFF08\u5DF2\u53BB\u654F\uFF0C\u517C\u5BB9 ClawHub knowledge \u683C\u5F0F\uFF09`;
    }
  },
  // ── 导出进化 ──
  {
    pattern: /^(导出进化|export evolution)$/i,
    mode: "both",
    execute: async () => {
      try {
        if (!_exportEvolutionAssets) {
          try {
            const mod = await import("./evolution.ts");
            _exportEvolutionAssets = mod.exportEvolutionAssets;
          } catch (_) {
          }
        }
        if (!_exportEvolutionAssets) return "\u8FDB\u5316\u6A21\u5757\u672A\u52A0\u8F7D";
        const { data, path } = _exportEvolutionAssets({ totalMessages: stats.totalMessages, firstSeen: stats.firstSeen, corrections: stats.corrections });
        return `\u8FDB\u5316\u8D44\u4EA7\u5DF2\u5BFC\u51FA (GEP v${data.version})
  \u89C4\u5219: ${data.assets.rules.length}
  \u5047\u8BBE: ${data.assets.hypotheses.length}
  \u6280\u80FD: ${data.assets.skills?.length ?? 0}
  \u5DF2\u56FA\u5316: ${data.assets.metadata.rulesSolidified}
\u8DEF\u5F84: ${path}`;
      } catch (e) {
        return `\u5BFC\u51FA\u8FDB\u5316\u5931\u8D25: ${e.message}`;
      }
    }
  },
  // ── 导入进化 ──
  {
    pattern: /^(导入进化|import evolution)\s+(.+)$/i,
    mode: "both",
    execute: async (m) => {
      const filePath = m[2].trim().replace(/^~/, homedir());
      try {
        if (!existsSync(filePath)) return `\u6587\u4EF6\u4E0D\u5B58\u5728: ${filePath}`;
        if (!filePath.startsWith(homedir()) && !filePath.startsWith("/tmp")) return "\u5B89\u5168\u9650\u5236\uFF1A\u53EA\u80FD\u5BFC\u5165\u5BB6\u76EE\u5F55\u6216 /tmp \u4E0B\u7684\u6587\u4EF6\u3002";
        if (!_importEvolutionAssets) {
          try {
            const mod = await import("./evolution.ts");
            _importEvolutionAssets = mod.importEvolutionAssets;
          } catch (_) {
          }
        }
        if (!_importEvolutionAssets) return "\u8FDB\u5316\u6A21\u5757\u672A\u52A0\u8F7D";
        const { rulesAdded, hypothesesAdded } = _importEvolutionAssets(filePath);
        return `\u8FDB\u5316\u8D44\u4EA7\u5DF2\u5BFC\u5165 (GEP)
  \u65B0\u589E\u89C4\u5219: ${rulesAdded}
  \u65B0\u589E\u5047\u8BBE: ${hypothesesAdded}`;
      } catch (e) {
        return `\u5BFC\u5165\u8FDB\u5316\u5931\u8D25: ${e.message}`;
      }
    }
  },
  // ── 导出全部 ──
  {
    pattern: /^(导出全部|export all|full backup)$/i,
    mode: "both",
    execute: () => {
      try {
        const { path, counts } = _fullBackup();
        const lines = Object.entries(counts).map(([k, v]) => `  ${k}: ${v}`);
        return `\u5168\u91CF\u5907\u4EFD\u5DF2\u5BFC\u51FA\uFF08\u5DF2\u53BB\u654F\uFF09
${lines.join("\n")}
\u8DEF\u5F84: ${path}`;
      } catch (e) {
        return `\u5168\u91CF\u5907\u4EFD\u5931\u8D25: ${e.message}`;
      }
    }
  },
  // ── 导入全部 ──
  {
    pattern: /^(导入全部|import all)\s+(.+)$/i,
    mode: "both",
    execute: (m) => {
      const fp = m[2].trim().replace(/^~/, homedir());
      try {
        if (!existsSync(fp)) return `\u6587\u4EF6\u4E0D\u5B58\u5728: ${fp}`;
        if (!fp.startsWith(homedir()) && !fp.startsWith("/tmp")) return "\u5B89\u5168\u9650\u5236\uFF1A\u53EA\u80FD\u5BFC\u5165\u5BB6\u76EE\u5F55\u6216 /tmp \u4E0B\u7684\u6587\u4EF6\u3002";
        const counts = _fullRestore(fp);
        const lines = Object.entries(counts).map(([k, v]) => `  ${k}: ${v}`);
        return `\u5168\u91CF\u6062\u590D\u5B8C\u6210\uFF08\u9700\u91CD\u542F\u751F\u6548\uFF09
${lines.join("\n")}`;
      } catch (e) {
        return `\u5168\u91CF\u6062\u590D\u5931\u8D25: ${e.message}`;
      }
    }
  },
  // ── 记忆链路 ──
  {
    pattern: /^(记忆链路|memory chain)\s+(.+)$/i,
    mode: "both",
    execute: (m) => {
      try {
        return generateMemoryChain(m[2].trim());
      } catch (e) {
        return "\u8BB0\u5FC6\u94FE\u8DEF\u751F\u6210\u5931\u8D25: " + e.message;
      }
    }
  },
  // ── 保存话题 ──
  {
    pattern: /^(保存话题|save topic)$/i,
    mode: "write",
    execute: () => {
      try {
        const branchDir = resolve(DATA_DIR, "branches");
        if (!existsSync(branchDir)) mkdirSync(branchDir, { recursive: true });
        const recentMsgs = memoryState.chatHistory.slice(-10);
        const topicWords = recentMsgs.flatMap((h) => (h.user || "").match(/[\u4e00-\u9fff]{2,4}|[A-Za-z]{3,}/g) || []);
        const freq = /* @__PURE__ */ new Map();
        for (const w of topicWords) {
          const k = w.toLowerCase();
          freq.set(k, (freq.get(k) || 0) + 1);
        }
        const topicLabel = [...freq.entries()].sort((a, b) => b[1] - a[1])[0]?.[0] || `topic_${Date.now()}`;
        const branchData = {
          topic: topicLabel,
          savedAt: Date.now(),
          chatHistory: recentMsgs,
          persona: getActivePersona().id
        };
        const branchPath = resolve(branchDir, `${topicLabel}.json`);
        writeFileSync(branchPath, JSON.stringify(branchData, null, 2), "utf-8");
        return `\u8BDD\u9898\u5DF2\u4FDD\u5B58\uFF1A\u300C${topicLabel}\u300D\uFF08${recentMsgs.length} \u8F6E\u5BF9\u8BDD\uFF09
\u8DEF\u5F84: ${branchPath}`;
      } catch (e) {
        return "\u4FDD\u5B58\u8BDD\u9898\u5931\u8D25: " + e.message;
      }
    }
  },
  // ── 切换话题 ──
  {
    pattern: /^(切换话题|switch topic)\s+(.+)$/i,
    mode: "write",
    execute: (m) => {
      try {
        const topicName = m[2].trim();
        const branchDir = resolve(DATA_DIR, "branches");
        const branchPath = resolve(branchDir, `${topicName}.json`);
        if (!branchPath.startsWith(branchDir)) return "\u65E0\u6548\u7684\u8BDD\u9898\u540D\u79F0\u3002";
        if (memoryState.chatHistory.length > 0) {
          if (!existsSync(branchDir)) mkdirSync(branchDir, { recursive: true });
          const currentTopic = `_autosave_${Date.now()}`;
          const currentBranch = { topic: currentTopic, savedAt: Date.now(), chatHistory: memoryState.chatHistory.slice(-50) };
          saveJson(resolve(branchDir, `${currentTopic}.json`), currentBranch);
        }
        if (!existsSync(branchPath)) return `\u8BDD\u9898\u300C${topicName}\u300D\u4E0D\u5B58\u5728\uFF0C\u7528"\u8BDD\u9898\u5217\u8868"\u67E5\u770B\u53EF\u7528\u8BDD\u9898\u3002`;
        const branchData = loadJson(branchPath, {});
        if (branchData.chatHistory && Array.isArray(branchData.chatHistory)) {
          memoryState.chatHistory.length = 0;
          memoryState.chatHistory.push(...branchData.chatHistory);
        }
        const persona = branchData.persona || "unknown";
        return `\u5DF2\u5207\u6362\u5230\u8BDD\u9898\u300C${topicName}\u300D\uFF08\u6062\u590D ${branchData.chatHistory?.length || 0} \u8F6E\u5BF9\u8BDD\uFF0C\u4EBA\u683C: ${persona}\uFF09`;
      } catch (e) {
        return "\u5207\u6362\u8BDD\u9898\u5931\u8D25: " + e.message;
      }
    }
  },
  // ── 话题列表 ──
  {
    pattern: /^(话题列表|topic list)$/i,
    mode: "both",
    execute: () => {
      try {
        const branchDir = resolve(DATA_DIR, "branches");
        if (!existsSync(branchDir)) return "\u6682\u65E0\u4FDD\u5B58\u7684\u8BDD\u9898\u3002";
        const files = readdirSync(branchDir).filter((f) => f.endsWith(".json"));
        if (files.length === 0) return "\u6682\u65E0\u4FDD\u5B58\u7684\u8BDD\u9898\u3002";
        const lines = [`\u8BDD\u9898\u5217\u8868\uFF08${files.length} \u4E2A\uFF09\uFF1A`];
        for (const f of files) {
          try {
            const data = loadJson(resolve(branchDir, f), {});
            const age = Math.floor((Date.now() - (data.savedAt || 0)) / 864e5);
            const ageStr = age === 0 ? "\u4ECA\u5929" : `${age}\u5929\u524D`;
            lines.push(`\u2022 ${data.topic || f.replace(".json", "")} \u2014 ${data.chatHistory?.length || 0} \u8F6E\u5BF9\u8BDD\uFF08${ageStr}\uFF09`);
          } catch {
            lines.push(`\u2022 ${f.replace(".json", "")} \u2014 \u6570\u636E\u635F\u574F`);
          }
        }
        return lines.join("\n");
      } catch (e) {
        return "\u8BDD\u9898\u5217\u8868\u8BFB\u53D6\u5931\u8D25: " + e.message;
      }
    }
  },
  // ── 共享记忆 ──
  {
    pattern: /^(共享记忆|share memory)\s+(.+)$/i,
    mode: "write",
    execute: (m) => {
      try {
        const keyword = m[2].trim();
        const _db = getDb();
        if (!_db) return "\u6570\u636E\u5E93\u672A\u5C31\u7EEA\u3002";
        const kw = `%${keyword.toLowerCase()}%`;
        const stmt = _db.prepare("UPDATE memories SET visibility = 'global' WHERE scope != 'expired' AND scope != 'decayed' AND (LOWER(content) LIKE ? OR LOWER(tags) LIKE ?)");
        const result = stmt.run(kw, kw);
        const changed = result.changes || 0;
        return changed > 0 ? `\u5DF2\u5C06 ${changed} \u6761\u5339\u914D\u300C${keyword}\u300D\u7684\u8BB0\u5FC6\u8BBE\u4E3A\u5168\u5C40\u5171\u4EAB\u3002` : `\u6CA1\u6709\u627E\u5230\u5339\u914D\u300C${keyword}\u300D\u7684\u8BB0\u5FC6\u3002`;
      } catch (e) {
        return "\u5171\u4EAB\u8BB0\u5FC6\u5931\u8D25: " + e.message;
      }
    }
  },
  // ── 私有记忆 ──
  {
    pattern: /^(私有记忆|private memory)\s+(.+)$/i,
    mode: "write",
    execute: (m) => {
      try {
        const keyword = m[2].trim();
        const _db = getDb();
        if (!_db) return "\u6570\u636E\u5E93\u672A\u5C31\u7EEA\u3002";
        const kw = `%${keyword.toLowerCase()}%`;
        const stmt = _db.prepare("UPDATE memories SET visibility = 'private' WHERE scope != 'expired' AND scope != 'decayed' AND (LOWER(content) LIKE ? OR LOWER(tags) LIKE ?)");
        const result = stmt.run(kw, kw);
        const changed = result.changes || 0;
        return changed > 0 ? `\u5DF2\u5C06 ${changed} \u6761\u5339\u914D\u300C${keyword}\u300D\u7684\u8BB0\u5FC6\u8BBE\u4E3A\u79C1\u6709\u3002` : `\u6CA1\u6709\u627E\u5230\u5339\u914D\u300C${keyword}\u300D\u7684\u8BB0\u5FC6\u3002`;
      } catch (e) {
        return "\u79C1\u6709\u8BB0\u5FC6\u5931\u8D25: " + e.message;
      }
    }
  },
  // ── 对话摘要 ──
  {
    pattern: /^(对话摘要|conversation summary)$/i,
    mode: "write",
    execute: () => {
      let allHistory = memoryState.chatHistory;
      if (allHistory.length === 0) {
        try {
          const histPath = resolve(DATA_DIR, "history.json");
          allHistory = loadJson(histPath, []);
        } catch (_) {
        }
      }
      const recent = allHistory.slice(-25);
      const sessions = [];
      let cur = [];
      for (const turn of recent) {
        if (cur.length > 0 && turn.ts - cur[cur.length - 1].ts > 18e5) {
          sessions.push({ start: cur[0].ts, turns: cur, summary: "" });
          cur = [];
        }
        cur.push(turn);
      }
      if (cur.length > 0) sessions.push({ start: cur[0].ts, turns: cur, summary: "" });
      const lines = sessions.slice(-5).map((s, i) => {
        const date = new Date(s.start).toLocaleString("zh-CN", { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
        const topics = s.turns.slice(0, 3).map((t) => t.user.slice(0, 30)).join(" \u2192 ");
        return `${i + 1}. [${date}] ${s.turns.length} \u8F6E | ${topics}...`;
      });
      return `\u6700\u8FD1\u5BF9\u8BDD\u6458\u8981\uFF08${sessions.length} \u4E2A\u4F1A\u8BDD\uFF09\uFF1A
${lines.join("\n") || "\u6682\u65E0\u8BB0\u5F55"}`;
    }
  },
  // ── 记忆健康 ──
  {
    pattern: /^(记忆健康|memory health)$/i,
    mode: "both",
    execute: () => executeHealth()
  },
  // ── 记忆审计 ──
  {
    pattern: /^(记忆审计|memory audit)$/i,
    mode: "write",
    execute: () => {
      const auditPath = resolve(DATA_DIR, "memory_audit.json");
      const audit = loadJson(auditPath, null);
      if (!audit) return "\u6682\u65E0\u5BA1\u8BA1\u62A5\u544A\uFF0C\u7B49\u5F85\u4E0B\u6B21\u5FC3\u8DF3\u81EA\u52A8\u751F\u6210";
      const lines = [
        `\u8BB0\u5FC6\u5BA1\u8BA1\u62A5\u544A\uFF08${new Date(audit.ts).toLocaleString()}\uFF09`,
        `\u91CD\u590D\u8BB0\u5FC6: ${audit.duplicates?.length ?? 0} \u7EC4`,
        `\u6781\u77ED\u8BB0\u5FC6(<10\u5B57): ${audit.tooShort?.length ?? 0} \u6761`,
        `\u65E0\u6807\u7B7E\u6D3B\u8DC3\u8BB0\u5FC6: ${audit.untagged ?? 0} \u6761`,
        audit.suggestions ? `\u5EFA\u8BAE: ${audit.suggestions}` : ""
      ].filter(Boolean);
      return `\u8BB0\u5FC6\u5BA1\u8BA1\u7ED3\u679C\uFF1A
${lines.join("\n")}`;
    }
  },
  // ── Pin / Unpin 记忆 ──
  {
    pattern: /^(pin|unpin)\s*(记忆|memory)\s+(.+)$/i,
    mode: "write",
    execute: (m, c) => {
      const action = m[1].toLowerCase();
      const keyword = m[3].trim();
      const results = recall(keyword, 10, c.senderId);
      if (results.length === 0) return `\u6CA1\u6709\u627E\u5230\u5339\u914D "${keyword}" \u7684\u8BB0\u5FC6\u3002`;
      ensureMemoriesLoaded();
      let changed = 0;
      const newScope = action === "pin" ? "pinned" : "mid_term";
      for (const r of results) {
        const mem = memoryState.memories.find((m2) => m2.content === r.content && m2.ts === r.ts);
        if (mem && mem.scope !== newScope) {
          mem.scope = newScope;
          changed++;
        }
      }
      if (changed > 0) saveMemories();
      return action === "pin" ? `\u5DF2\u9489\u9009 ${changed} \u6761\u5339\u914D "${keyword}" \u7684\u8BB0\u5FC6\uFF08\u4E0D\u4F1A\u88AB\u8870\u51CF\u6DD8\u6C70\uFF09` : `\u5DF2\u53D6\u6D88\u9489\u9009 ${changed} \u6761\u5339\u914D "${keyword}" \u7684\u8BB0\u5FC6\uFF08\u6062\u590D\u4E3A mid_term\uFF09`;
    }
  },
  // ── 恢复记忆 ──
  {
    pattern: /^(?:恢复记忆|restore memory)\s+(.+)$/i,
    mode: "write",
    execute: (m) => {
      try {
        const keyword = m[1].trim();
        const count = restoreArchivedMemories(keyword);
        return count > 0 ? `\u5DF2\u6062\u590D ${count} \u6761\u5339\u914D "${keyword}" \u7684\u5F52\u6863\u8BB0\u5FC6\u3002` : `\u6CA1\u6709\u627E\u5230\u5339\u914D "${keyword}" \u7684\u5F52\u6863\u8BB0\u5FC6\u3002`;
      } catch (e) {
        return `\u6062\u590D\u5931\u8D25: ${e.message}`;
      }
    }
  },
  // ── 记忆时间线 ──
  {
    pattern: /^(记忆时间线|时间线|memory timeline)\s+(.+)$/i,
    mode: "write",
    execute: (m) => {
      const keyword = m[2].trim();
      const results = queryMemoryTimeline(keyword);
      if (results.length === 0) return `\u6CA1\u6709\u627E\u5230\u5173\u952E\u8BCD "${keyword}" \u7684\u8BB0\u5FC6\u65F6\u95F4\u7EBF\u3002`;
      const lines = results.map((r) => {
        const from = new Date(r.from).toLocaleString();
        const until = r.until ? new Date(r.until).toLocaleString() : "\u81F3\u4ECA";
        return `- [${from} ~ ${until}] ${r.content.slice(0, 80)}`;
      });
      return `\u8BB0\u5FC6\u65F6\u95F4\u7EBF "${keyword}"\uFF08${results.length} \u6761\uFF09\uFF1A
${lines.join("\n")}`;
    }
  },
  // ── 时间旅行 ──
  {
    pattern: /^(?:时间旅行|time travel)\s+(.+)$/i,
    mode: "write",
    execute: (m) => {
      const keyword = m[1].trim();
      try {
        const _db = getDb();
        if (!_db) return "\u6570\u636E\u5E93\u672A\u5C31\u7EEA\uFF0C\u65E0\u6CD5\u67E5\u8BE2\u3002";
        const kw = `%${keyword.toLowerCase()}%`;
        const rows = _db.prepare(
          "SELECT content, scope, ts FROM memories WHERE LOWER(content) LIKE ? AND scope != 'expired' AND scope != 'decayed' ORDER BY ts ASC LIMIT 30"
        ).all(kw);
        if (rows.length === 0) return `\u6CA1\u6709\u627E\u5230\u5173\u4E8E\u300C${keyword}\u300D\u7684\u8BB0\u5FC6\u6F14\u53D8\u3002`;
        const lines = rows.map((r) => {
          const date = new Date(r.ts).toLocaleDateString("zh-CN", { month: "numeric", day: "numeric" });
          return `  [${date}] ${r.content.slice(0, 80)}`;
        });
        let trend = "\u2192 \u6301\u7EED\u5173\u6CE8\u4E2D";
        if (rows.length >= 3) {
          const first = rows[0].content.toLowerCase();
          const last = rows[rows.length - 1].content.toLowerCase();
          if (first.includes("\u5B66") && last.includes("\u7406\u89E3")) trend = "\u2192 \u4ECE\u5165\u95E8\u5230\u6DF1\u5165\uFF0C\u6301\u7EED\u63A8\u8FDB\u4E2D";
          else if (last.includes("\u5B8C\u6210") || last.includes("done")) trend = "\u2192 \u5DF2\u5B8C\u6210";
          else if (last.includes("\u653E\u5F03") || last.includes("\u7B97\u4E86")) trend = "\u2192 \u5DF2\u653E\u5F03";
        }
        return `\u{1F570} \u300C${keyword}\u300D\u89C2\u70B9\u6F14\u53D8\uFF08${rows.length} \u6761\uFF09
${lines.join("\n")}

${trend}`;
      } catch (e) {
        return `\u65F6\u95F4\u65C5\u884C\u67E5\u8BE2\u5931\u8D25: ${e.message}`;
      }
    }
  },
  // ── 推理链 ──
  {
    pattern: /^(推理链|reasoning chain)$/i,
    mode: "write",
    execute: (_m, c) => {
      const recalled = c.session.lastRecalledContents;
      if (recalled.length === 0) return "\u4E0A\u4E00\u6B21\u56DE\u590D\u6CA1\u6709\u53EC\u56DE\u4EFB\u4F55\u8BB0\u5FC6\u3002";
      const lines = recalled.map((ct, i) => `  ${i + 1}. ${ct.slice(0, 100)}`);
      const causalLines = [];
      const DAY_MS = 24 * 36e5;
      const allMems = memoryState.memories;
      const recalledMems = recalled.map((ct) => allMems.find((m) => m.content === ct)).filter(Boolean);
      const correctionMems = recalledMems.filter((m) => m.scope === "correction" || m.scope === "event");
      for (const mem of correctionMems.slice(0, 3)) {
        const memTrigrams = trigrams(mem.content);
        const nearby = allMems.filter(
          (m) => m !== mem && Math.abs(m.ts - mem.ts) < DAY_MS && trigramSimilarity(trigrams(m.content), memTrigrams) > 0.15
        ).sort((a, b) => a.ts - b.ts);
        if (nearby.length > 0) {
          const rootCause = nearby[0];
          const fmtD = (ts) => new Date(ts).toLocaleDateString("zh-CN", { month: "numeric", day: "numeric" });
          causalLines.push(`  \u7ED3\u679C: ${mem.content.slice(0, 60)} (${fmtD(mem.ts)})`);
          causalLines.push(`    \u2190 \u539F\u56E0: ${nearby[nearby.length > 1 ? 1 : 0].content.slice(0, 60)} (${fmtD(nearby[0].ts)})`);
          causalLines.push(`    \u2190 \u6839\u56E0: ${rootCause.content.slice(0, 60)}`);
          const rootSnippet = rootCause.content.slice(0, 40).replace(/[。.!！？?]$/, "");
          causalLines.push(`  \u{1F4AD} \u53CD\u4E8B\u5B9E: \u5982\u679C\u5F53\u65F6\u6CA1\u6709\u300C${rootSnippet}\u300D\uFF0C\u8FD9\u4E2A\u95EE\u9898\u53EF\u80FD\u4E0D\u4F1A\u53D1\u751F`);
          causalLines.push("");
        }
      }
      let display = `\u{1F9E0} \u4E0A\u6B21\u56DE\u590D\u7684\u63A8\u7406\u94FE\uFF08\u53EC\u56DE ${recalled.length} \u6761\u8BB0\u5FC6\uFF09\uFF1A
${lines.join("\n")}`;
      if (causalLines.length > 0) {
        display += `

\u{1F517} \u56E0\u679C\u8FFD\u6EAF\uFF1A
${causalLines.join("\n")}`;
      }
      return display;
    }
  },
  // ── 情绪锚点 ──
  {
    pattern: /^(情绪锚点|emotion anchors?)$/i,
    mode: "write",
    execute: () => formatEmotionAnchors()
  },
  // ── "别记这个" — skip next memory ──
  {
    pattern: /^(别记了?这[个条]?|别记住|don't remember|forget this|不要记)/i,
    mode: "write",
    execute: (_m, c) => {
      c.session._skipNextMemory = true;
      return "\u{1F507} \u6536\u5230\uFF0C\u8FD9\u6761\u5BF9\u8BDD\u4E0D\u4F1A\u88AB\u8BB0\u5FC6\u3002";
    }
  },
  // ── stats (write path) ──
  {
    pattern: /^(stats)$/i,
    mode: "both",
    execute: () => executeStats()
  },
  // ── 功能状态 ──
  {
    pattern: /^(功能状态|features|feature status)$/i,
    mode: "both",
    execute: () => executeFeatures()
  },
  // ── 功能开关 toggle ──
  {
    pattern: /^(?:开启|启用|enable|关闭|禁用|disable)\s+\S+$/i,
    mode: "both",
    execute: (m) => {
      const result = handleFeatureCommand(m[0]);
      if (result) return typeof result === "string" ? result : "\u529F\u80FD\u5F00\u5173\u5DF2\u66F4\u65B0\u3002";
      return null;
    }
  },
  // ── 灵魂状态 ──
  {
    pattern: /^(soul state|灵魂状态|内心状态)$/i,
    mode: "read",
    execute: async () => {
      try {
        const { body } = await import("./body.ts");
        return `\u7075\u9B42\u72B6\u6001
Energy: ${(body.energy * 100).toFixed(0)}%
Mood: ${body.mood.toFixed(2)}
Emotion: ${body.emotion}`;
      } catch (_) {
        return "\u7075\u9B42\u72B6\u6001\u6682\u4E0D\u53EF\u7528";
      }
    }
  },
  // ── 人格列表 ──
  {
    pattern: /^(人格列表|personas?)$/i,
    mode: "read",
    execute: async () => {
      try {
        const { PERSONAS: PERSONAS2 } = await import("./persona.ts");
        const lines = PERSONAS2.map((p) => `\u2022 ${p.name} \u2014 ${p.tone?.slice(0, 40) || ""}`);
        return `\u4EBA\u683C\u5217\u8868\uFF1A
${lines.join("\n")}`;
      } catch (_) {
        return "\u4EBA\u683C\u5217\u8868\u4E0D\u53EF\u7528";
      }
    }
  },
  // ── 价值观 ──
  {
    pattern: /^(价值观|values)$/i,
    mode: "read",
    execute: () => {
      try {
        const vals = getAllValues();
        return typeof vals === "string" ? vals : JSON.stringify(vals, null, 2).slice(0, 500);
      } catch (_) {
        return "\u4EF7\u503C\u89C2\u6A21\u5757\u4E0D\u53EF\u7528";
      }
    }
  }
  // LLM 配置命令已移除 — 通过 system prompt 注入指引，让 OpenClaw 的 LLM 自然引导用户编辑 ai_config.json
];
function matchCommand(msg, allowWrite) {
  for (const cmd of COMMANDS) {
    if (!allowWrite && cmd.mode === "write") continue;
    const m = msg.trim().match(cmd.pattern);
    if (m) return { cmd, match: m };
  }
  return null;
}
function routeCommand(userMsg, ctx, session, senderId, channelId, event) {
  console.log(`[cc-soul][routeCommand] v2 msg="${userMsg.slice(0, 30)}"`);
  if (wasHandledByDirect(userMsg)) {
    console.log(`[cc-soul][routeCommand] skipped: already handled by routeCommandDirect`);
    ctx.bodyForAgent = "[\u7CFB\u7EDF] \u547D\u4EE4\u5DF2\u5904\u7406\uFF0C\u7ED3\u679C\u5DF2\u53D1\u9001\u3002";
    return true;
  }
  if (!getPrivacyMode()) {
    const imageMatch = userMsg.match(/\[(?:Image|图片|Screenshot|截图)[:\s]([^\]]+)\]/i);
    if (imageMatch) {
      addMemory(`[\u89C6\u89C9\u8BB0\u5FC6] ${imageMatch[1].slice(0, 200)}`, "visual", senderId, "channel", channelId);
      console.log(`[cc-soul][visual] stored image memory: ${imageMatch[1].slice(0, 60)}`);
    }
  }
  const featureResult = handleFeatureCommand(userMsg);
  if (featureResult) {
    cmdReply(ctx, event, session, typeof featureResult === "string" ? featureResult : "\u529F\u80FD\u5F00\u5173\u5DF2\u66F4\u65B0\u3002", userMsg);
    return true;
  }
  const shortcutCmd = shortcuts[userMsg.trim()];
  if (shortcutCmd) {
    if (shortcutCmd === "\u529F\u80FD\u72B6\u6001") {
      const result = handleFeatureCommand("\u529F\u80FD\u72B6\u6001");
      cmdReply(ctx, event, session, typeof result === "string" ? result : "\u529F\u80FD\u5F00\u5173\u5DF2\u66F4\u65B0\u3002", userMsg);
      return true;
    }
    if (shortcutCmd === "\u8BB0\u5FC6\u56FE\u8C31") {
      cmdReply(ctx, event, session, "\u8BB0\u5FC6\u56FE\u8C31\u529F\u80FD\u5DF2\u89E6\u53D1\uFF0C\u8BF7\u7A0D\u5019\u3002", userMsg);
      return true;
    }
    if (shortcutCmd === "\u6700\u8FD1\u5728\u804A\u4EC0\u4E48") {
      const recentTopics = memoryState.chatHistory.slice(-5).map((h) => h.user.slice(0, 30)).join(" \u2192 ");
      cmdReply(ctx, event, session, `\u6700\u8FD1\u8BDD\u9898\u8F68\u8FF9: ${recentTopics || "\u6682\u65E0\u8BB0\u5F55"}`, userMsg);
      return true;
    }
    if (shortcutCmd === "\u7D27\u6025\u6A21\u5F0F") {
      cmdReply(ctx, event, session, "\u7D27\u6025\u6A21\u5F0F\u5DF2\u5F00\u542F\uFF0C\u5C06\u63D0\u4F9B\u5FEB\u901F\u7CBE\u51C6\u7684\u56DE\u7B54\u3002", userMsg);
      return true;
    }
  }
  if (handleTuneCommand(userMsg)) {
    cmdReply(ctx, event, session, "\u8C03\u53C2\u6307\u4EE4\u5DF2\u6267\u884C\u3002", userMsg);
    return true;
  }
  const matched = matchCommand(userMsg, true);
  if (matched) {
    const cmdCtx = { senderId, channelId, session, ctx, event };
    const result = matched.cmd.execute(matched.match, cmdCtx);
    if (result instanceof Promise) {
      result.then((text) => {
        if (text != null) cmdReply(ctx, event, session, text, userMsg);
      }).catch((e) => {
        cmdReply(ctx, event, session, `\u547D\u4EE4\u6267\u884C\u5931\u8D25: ${e.message}`, userMsg);
      });
      ctx.bodyForAgent = "[\u7CFB\u7EDF] \u547D\u4EE4\u5DF2\u5904\u7406\uFF0C\u7ED3\u679C\u5DF2\u53D1\u9001\u3002";
      return true;
    }
    if (result != null) {
      cmdReply(ctx, event, session, result, userMsg);
      return true;
    }
  }
  {
    const ctxMatch1 = userMsg.match(/^当聊到\s*(.+?)\s*时?提醒我\s+(.+)$/);
    const ctxMatch2 = userMsg.match(/^remind\s+me\s+(.+?)\s+when\s+(?:we\s+)?talk(?:ing)?\s+about\s+(.+)$/i);
    const ctxMatch3 = userMsg.match(/^when\s+(?:we\s+)?talk(?:ing)?\s+about\s+(.+?)\s+remind\s+me\s+(.+)$/i);
    if (ctxMatch1) {
      const keyword = ctxMatch1[1].trim();
      const reminderContent = ctxMatch1[2].trim();
      if (keyword.length >= 2 && reminderContent.length >= 2) {
        const id = dbAddContextReminder(keyword, reminderContent, senderId);
        cmdReply(ctx, event, session, `\u5DF2\u6DFB\u52A0\u4E0A\u4E0B\u6587\u63D0\u9192\uFF1A\u5F53\u804A\u5230\u300C${keyword}\u300D\u65F6\u63D0\u9192\u4F60\u300C${reminderContent}\u300D(id=${id})`, userMsg);
        return true;
      }
    } else if (ctxMatch2) {
      const reminderContent = ctxMatch2[1].trim();
      const keyword = ctxMatch2[2].trim();
      if (keyword.length >= 2 && reminderContent.length >= 2) {
        const id = dbAddContextReminder(keyword, reminderContent, senderId);
        cmdReply(ctx, event, session, `\u5DF2\u6DFB\u52A0\u4E0A\u4E0B\u6587\u63D0\u9192\uFF1A\u5F53\u804A\u5230\u300C${keyword}\u300D\u65F6\u63D0\u9192\u4F60\u300C${reminderContent}\u300D(id=${id})`, userMsg);
        return true;
      }
    } else if (ctxMatch3) {
      const keyword = ctxMatch3[1].trim();
      const reminderContent = ctxMatch3[2].trim();
      if (keyword.length >= 2 && reminderContent.length >= 2) {
        const id = dbAddContextReminder(keyword, reminderContent, senderId);
        cmdReply(ctx, event, session, `\u5DF2\u6DFB\u52A0\u4E0A\u4E0B\u6587\u63D0\u9192\uFF1A\u5F53\u804A\u5230\u300C${keyword}\u300D\u65F6\u63D0\u9192\u4F60\u300C${reminderContent}\u300D(id=${id})`, userMsg);
        return true;
      }
    }
  }
  const chatId = ctx.conversationId || event.sessionKey || "";
  if (checkTaskConfirmation(userMsg, chatId)) {
    cmdReply(ctx, event, session, "\u4EFB\u52A1\u5DF2\u6D3E\u53D1\u7ED9\u6267\u884C\u5F15\u64CE\uFF0C\u6B63\u5728\u5904\u7406\u4E2D...", userMsg);
    return true;
  }
  if (isCommand(userMsg)) {
    const evCtx = event?.context || {};
    const to = evCtx.conversationId || evCtx.chatId || "";
    routeCommandDirect(userMsg, { to, cfg: _replyCfg, event }).then((handled) => {
      if (handled) {
        markHandledByDirect(userMsg);
        console.log(`[cc-soul][routeCommand] fallback to routeCommandDirect: handled`);
      }
    }).catch(() => {
    });
    ctx.bodyForAgent = "[\u7CFB\u7EDF] \u547D\u4EE4\u5DF2\u5904\u7406\uFF0C\u7ED3\u679C\u5DF2\u53D1\u9001\u3002";
    return true;
  }
  return false;
}
async function routeCommandDirect(userMsg, params) {
  if (!userMsg) return false;
  const _to = params?.to || "";
  const _cfg = params?.cfg || _replyCfg;
  const _replyCallback = params?.replyCallback;
  const reply = (text) => {
    if (typeof _replyCallback === "function") _replyCallback(text);
    return replySender(_to, text, _cfg).catch(() => {
    });
  };
  if (/^(help|帮助|命令列表|commands)$/i.test(userMsg.trim())) {
    reply(HELP_TEXT_DIRECT);
    return true;
  }
  const matched = matchCommand(userMsg, false);
  if (matched) {
    const cmdCtx = { senderId: "", channelId: "", session: {}, ctx: {}, event: params?.event };
    const result = matched.cmd.execute(matched.match, cmdCtx);
    const text = result instanceof Promise ? await result : result;
    if (text != null) {
      reply(text);
      return true;
    }
  }
  return false;
}
const CMD_PATTERNS = [
  /^(help|帮助|命令列表|commands)$/i,
  /^(搜索记忆|search memory)\s+/i,
  /^(我的记忆|my memories)$/i,
  /^(stats)$/i,
  /^(soul state|灵魂状态|内心状态)$/i,
  /^(情绪周报|mood report)$/i,
  /^(能力评分|capability)$/i,
  /^(功能状态|features)$/i,
  /^(记忆健康|memory health)$/i,
  /^(功能|feature)\s+/i,
  /^(人格列表|personas?)$/i,
  /^(导出|export)/i,
  /^(导入|import)/i,
  /^full backup$/i,
  /^(实验|experiment)/i,
  /^(tune|调整)/i,
  /^(ingest|导入文件)/i,
  /^(价值观|values)$/i,
  /^(cost|成本)$/i,
  /^(sync|同步)/i,
  /^(upgrade|更新)/i,
  /^(radar|竞品)/i,
  /^(dashboard|仪表盘|记忆地图|stats|soul state|灵魂状态|情绪周报|能力评分|metrics|cost)/i,
  /^(我的技能|my skills)$/i,
  /^(时间旅行|time travel)\s+/i,
  /^(推理链|reasoning chain)$/i,
  /^(情绪锚点|emotion anchors?)$/i,
  /^(记忆链路|memory chain)\s+/i,
  /^(保存话题|save topic)$/i,
  /^(切换话题|switch topic)\s+/i,
  /^(话题列表|topic list)$/i,
  /^(共享记忆|share memory)\s+/i,
  /^(私有记忆|private memory)\s+/i,
  /^(别记了?这[个条]?|别记住|don't remember|forget this|不要记)$/i
];
const PRIVACY_TRIGGERS_RE = /^(别记了|隐私模式|privacy mode|可以了|关闭隐私|恢复记忆)$/i;
function isCommand(msg) {
  const trimmed = (msg || "").trim();
  if (!trimmed) return false;
  if (CMD_PATTERNS.some((p) => p.test(trimmed))) return true;
  if (PRIVACY_TRIGGERS_RE.test(trimmed)) return true;
  return false;
}
async function handleCommandInbound(msg, to, cfg, event) {
  setReplyCfg(cfg);
  try {
    const handled = await routeCommandDirect(msg.trim(), { to, cfg, event });
    if (handled) markHandledByDirect(msg);
    return handled;
  } catch (e) {
    console.error(`[cc-soul][handleCommandInbound] error: ${e.message}`);
    return false;
  }
}
function generateMemoryChain(keyword) {
  const db = getDb();
  if (!db) return `\u{1F517} \u8BB0\u5FC6\u94FE\u8DEF\u300C${keyword}\u300D
\u6570\u636E\u5E93\u521D\u59CB\u5316\u4E2D\uFF0C\u8BF7\u7A0D\u540E\u91CD\u8BD5\u3002`;
  const kw = `%${keyword.toLowerCase()}%`;
  let memories = [];
  try {
    memories = db.prepare(
      "SELECT content, scope, ts, tags FROM memories WHERE scope != 'expired' AND scope != 'decayed' AND (LOWER(content) LIKE ? OR LOWER(tags) LIKE ?) ORDER BY ts ASC LIMIT 30"
    ).all(kw, kw);
  } catch {
    return `\u{1F517} \u8BB0\u5FC6\u94FE\u8DEF\u300C${keyword}\u300D
\u67E5\u8BE2\u5931\u8D25\u3002`;
  }
  if (memories.length === 0) return `\u{1F517} \u8BB0\u5FC6\u94FE\u8DEF\u300C${keyword}\u300D
\u6CA1\u6709\u627E\u5230\u76F8\u5173\u8BB0\u5FC6\u3002`;
  const lines = [`\u{1F517} \u8BB0\u5FC6\u94FE\u8DEF\u300C${keyword}\u300D`];
  const scopeDepth = {
    "preference": 0,
    "fact": 0,
    "event": 0,
    "topic": 0,
    "correction": 1,
    "discovery": 1,
    "proactive": 1,
    "reflection": 2,
    "reflexion": 2
  };
  let prevDate = "";
  for (const m of memories) {
    const date = new Date(m.ts).toLocaleDateString("zh-CN", { month: "numeric", day: "numeric" });
    const depth = scopeDepth[m.scope] ?? 0;
    const indent = "  ".repeat(depth);
    const connector = depth > 0 ? "\u2514\u2192 " : "";
    const snippet = (m.content || "").slice(0, 50).replace(/\n/g, " ");
    const dateTag = date !== prevDate ? ` (${date})` : "";
    prevDate = date;
    lines.push(`  ${indent}${connector}[${snippet}${m.content.length > 50 ? "..." : ""}] ${m.scope}${dateTag}`);
  }
  return lines.join("\n");
}
export {
  COMMANDS,
  isCommand,
  matchCommand,
  routeCommand,
  routeCommandDirect,
  wasHandledByDirect
};
