import { resolve } from "path";
import { existsSync, statSync, writeFileSync } from "fs";
import { MEMORIES_PATH, HISTORY_PATH, DATA_DIR, loadJson, debouncedSave } from "./persistence.ts";
import { autoExtractFromMemory } from "./fact-store.ts";
import { getParam } from "./auto-tune.ts";
import {
  initSQLite,
  sqliteAddMemory,
  sqliteUpdateMemory,
  sqliteFindByContent,
  sqliteGetAll,
  sqliteAddChatTurn,
  sqliteGetRecentHistory,
  sqliteTrimHistory
} from "./sqlite-store.ts";
import { addRelation } from "./graph.ts";
import {
  trigrams,
  trigramSimilarity,
  timeDecay,
  MAX_MEMORIES,
  MAX_HISTORY,
  INJECT_HISTORY,
  detectMemoryPoisoning,
  extractReasoning,
  defaultVisibility,
  emitCacheEvent,
  generateMemoryId,
  appendLineage,
  classifyConflict,
  contextAwareSimilarity
} from "./memory-utils.ts";
import { invalidateIDF, incrementalIDFUpdate, updateRecallIndex, rebuildRecallIndex } from "./memory-recall.ts";
import { invalidateFieldIDF } from "./activation-field.ts";
import {
  trigrams as trigrams2,
  trigramSimilarity as trigramSimilarity2,
  shuffleArray,
  compressMemory as compressMemory2,
  SYNONYM_MAP,
  MAX_MEMORIES as MAX_MEMORIES2,
  MAX_HISTORY as MAX_HISTORY2,
  INJECT_HISTORY as INJECT_HISTORY2,
  detectMemoryPoisoning as detectMemoryPoisoning2,
  extractReasoning as extractReasoning2,
  defaultVisibility as defaultVisibility2
} from "./memory-utils.ts";
import {
  recall,
  getCachedFusedRecall,
  invalidateIDF as invalidateIDF2,
  degradeMemoryConfidence,
  trackRecallImpact,
  getRecallImpactBoost,
  getRecallRate,
  recallStats,
  recallImpact,
  recallWithScores,
  updateRecallIndex as updateRecallIndex2,
  rebuildRecallIndex as rebuildRecallIndex2,
  incrementalIDFUpdate as incrementalIDFUpdate2
} from "./memory-recall.ts";
import {
  consolidateMemories,
  generateInsights,
  recallFeedbackLoop,
  triggerAssociativeRecall,
  getAssociativeRecall,
  parseMemoryCommands,
  executeMemoryCommands,
  getPendingSearchResults,
  scanForContradictions,
  predictiveRecall,
  generatePrediction,
  triggerSessionSummary,
  cleanupNetworkKnowledge,
  resolveNetworkConflicts,
  episodes,
  loadEpisodes,
  recordEpisode,
  recallEpisodes,
  buildEpisodeContext,
  processMemoryDecay,
  pruneExpiredMemories,
  compressOldMemories,
  reviveDecayedMemories,
  restoreArchivedMemories,
  sqliteMaintenance,
  getStorageStatus,
  auditMemoryHealth
} from "./memory-lifecycle.ts";
let _handlerState = null;
let _bodyMod = null;
let _signalsMod = null;
let _distillMod = null;
function getLazyModule(name) {
  switch (name) {
    case "handler-state":
      if (!_handlerState) {
        import("./handler-state.ts").then((m) => {
          _handlerState = m;
        }).catch((e) => {
          console.error(`[cc-soul] module load failed (handler-state): ${e.message}`);
        });
      }
      return _handlerState;
    case "body":
      if (!_bodyMod) {
        import("./body.ts").then((m) => {
          _bodyMod = m;
        }).catch((e) => {
          console.error(`[cc-soul] module load failed (body): ${e.message}`);
        });
      }
      return _bodyMod;
    case "signals":
      if (!_signalsMod) {
        import("./signals.ts").then((m) => {
          _signalsMod = m;
        }).catch((e) => {
          console.error(`[cc-soul] module load failed (signals): ${e.message}`);
        });
      }
      return _signalsMod;
    case "distill":
      if (!_distillMod) {
        import("./distill.ts").then((m) => {
          _distillMod = m;
        }).catch((e) => {
          console.error(`[cc-soul] module load failed (distill): ${e.message}`);
        });
      }
      return _distillMod;
    default:
      return null;
  }
}
setTimeout(() => {
  import("./handler-state.ts").then((m) => {
    _handlerState = m;
  }).catch((e) => {
    console.error(`[cc-soul] module load failed (handler-state): ${e.message}`);
  });
  import("./body.ts").then((m) => {
    _bodyMod = m;
  }).catch((e) => {
    console.error(`[cc-soul] module load failed (body): ${e.message}`);
  });
  import("./signals.ts").then((m) => {
    _signalsMod = m;
  }).catch((e) => {
    console.error(`[cc-soul] module load failed (signals): ${e.message}`);
  });
  import("./distill.ts").then((m) => {
    _distillMod = m;
  }).catch((e) => {
    console.error(`[cc-soul] module load failed (distill): ${e.message}`);
  });
}, 1e3);
let _currentSegmentId = 0;
function incrementSegment() {
  _currentSegmentId++;
}
function getCurrentSegmentId() {
  return _currentSegmentId;
}
const BAYES_DEFAULT_ALPHA = 2;
const BAYES_DEFAULT_BETA = 1;
function bayesConfidence(mem) {
  const a = mem.bayesAlpha ?? BAYES_DEFAULT_ALPHA;
  const b = mem.bayesBeta ?? BAYES_DEFAULT_BETA;
  return a / (a + b);
}
function ensureBayesFields(mem) {
  if (mem.bayesAlpha == null) {
    const c = mem.confidence ?? 0.67;
    const sum = BAYES_DEFAULT_ALPHA + BAYES_DEFAULT_BETA;
    mem.bayesAlpha = c * sum;
    mem.bayesBeta = (1 - c) * sum;
  }
  if (mem.bayesBeta == null) mem.bayesBeta = BAYES_DEFAULT_BETA;
}
function bayesBoost(mem, delta = 0.5) {
  ensureBayesFields(mem);
  mem.bayesAlpha += delta;
  mem.confidence = bayesConfidence(mem);
}
function bayesPenalize(mem, delta = 0.5) {
  ensureBayesFields(mem);
  mem.bayesBeta += delta;
  mem.confidence = bayesConfidence(mem);
}
function bayesCorrect(mem, delta = 2) {
  ensureBayesFields(mem);
  mem.bayesBeta += delta;
  mem.confidence = bayesConfidence(mem);
}
function syncToSQLite(mem, updates, findByContent) {
  if (!useSQLite) return;
  const found = sqliteFindByContent(findByContent || mem.content);
  if (found) {
    sqliteUpdateMemory(found.id, updates);
  }
}
let useSQLite = false;
let _memoriesLoaded = false;
let _sqliteInitDone = false;
function ensureSQLiteReady() {
  if (_sqliteInitDone) return useSQLite;
  _sqliteInitDone = true;
  const ok = initSQLite();
  if (ok) useSQLite = true;
  return ok;
}
function ensureMemoriesLoaded() {
  if (_memoriesLoaded) return;
  _memoriesLoaded = true;
  loadMemories();
}
const memoryState = {
  memories: [],
  chatHistory: []
};
const _recentWriteHashes = /* @__PURE__ */ new Set();
setInterval(() => {
  _recentWriteHashes.clear();
}, 3e5);
const scopeIndex = /* @__PURE__ */ new Map();
const contentIndex = /* @__PURE__ */ new Map();
function rebuildContentIndex() {
  contentIndex.clear();
  for (let i = 0; i < memoryState.memories.length; i++) {
    const key = memoryState.memories[i].content.slice(0, 50).toLowerCase();
    contentIndex.set(key, memoryState.memories[i].content);
  }
}
function rebuildScopeIndex() {
  scopeIndex.clear();
  for (const mem of memoryState.memories) {
    const arr = scopeIndex.get(mem.scope) || [];
    arr.push(mem);
    scopeIndex.set(mem.scope, arr);
  }
  rebuildContentIndex();
}
function getMemoriesByScope(scope) {
  return scopeIndex.get(scope) || [];
}
const MAX_WORKING = 20;
const MAX_WORKING_SESSIONS = 100;
const workingMemory = /* @__PURE__ */ new Map();
function addWorkingMemory(content, sessionKey) {
  if (!content || content.length < 5) return;
  let entries = workingMemory.get(sessionKey);
  if (entries) {
    workingMemory.delete(sessionKey);
  } else {
    entries = [];
  }
  workingMemory.set(sessionKey, entries);
  if (entries.some((e) => e.content === content)) return;
  entries.push({ content, sessionKey, addedAt: Date.now() });
  if (entries.length > MAX_WORKING) entries.splice(0, entries.length - MAX_WORKING);
  if (workingMemory.size > MAX_WORKING_SESSIONS) {
    const oldest = workingMemory.keys().next().value;
    if (oldest) workingMemory.delete(oldest);
  }
}
function buildWorkingMemoryContext(sessionKey) {
  const entries = workingMemory.get(sessionKey);
  if (!entries || entries.length === 0) return "";
  workingMemory.delete(sessionKey);
  workingMemory.set(sessionKey, entries);
  return `[Working Memory \u2014 this session]
${entries.map((e) => `- ${e.content}`).join("\n")}`;
}
function archiveWorkingMemory(sessionKey) {
  const entries = workingMemory.get(sessionKey);
  if (!entries || entries.length === 0) return;
  let archived = 0;
  for (const entry of entries) {
    if (entry.content.length < 50) continue;
    const hasSubstance = /[：:=→]|因为|所以|结论|发现|决定|计划|问题|解决|配置|版本|密码|账号|地址/.test(entry.content);
    if (!hasSubstance && entry.content.length < 100) continue;
    addMemory(entry.content, "event", void 0, "channel", sessionKey);
    archived++;
  }
  if (archived > 0) console.log(`[cc-soul][memory] archived ${archived}/${entries.length} working memory entries`);
  workingMemory.delete(sessionKey);
}
function cleanupWorkingMemory() {
  const cutoff = Date.now() - 6 * 36e5;
  for (const [key, entries] of workingMemory) {
    if (entries.length > 0 && entries[entries.length - 1].addedAt < cutoff) {
      archiveWorkingMemory(key);
    }
  }
}
const CORE_MEMORY_PATH = resolve(DATA_DIR, "core_memory.json");
const MAX_CORE_MEMORIES = 100;
let coreMemories = [];
function loadCoreMemories() {
  coreMemories = loadJson(CORE_MEMORY_PATH, []);
  console.log(`[cc-soul][core-memory] loaded ${coreMemories.length} core memories`);
}
function saveCoreMemories() {
  debouncedSave(CORE_MEMORY_PATH, coreMemories);
}
function promoteToCore(content, category, source = "auto") {
  if (coreMemories.some((m) => m.content === content)) return;
  const REJECT_PREFIXES = ["[goal completed]", "[Working Memory", "[\u5F53\u524D\u9762\u5411:", "[\u9690\u79C1\u6A21\u5F0F]", "[\u5F53\u524D\u5BF9\u8BDD\u8005]", "[\u5185\u90E8\u77DB\u76FE\u8B66\u544A]", "[System]", "[\u5B89\u5168\u8B66\u544A]", "Rating:", "\u2192 **Rating"];
  if (REJECT_PREFIXES.some((p) => content.includes(p))) {
    console.log(`[cc-soul][core-memory] REJECT (system augment): ${content.slice(0, 60)}`);
    return;
  }
  coreMemories.push({ content, category, addedAt: Date.now(), source });
  if (coreMemories.length > MAX_CORE_MEMORIES) {
    const autoIdx = coreMemories.findIndex((m) => m.source === "auto");
    if (autoIdx >= 0) coreMemories.splice(autoIdx, 1);
  }
  saveCoreMemories();
  console.log(`[cc-soul][core-memory] promoted: ${content.slice(0, 50)} [${category}]`);
}
function buildCoreMemoryContext() {
  if (coreMemories.length === 0) return "";
  let fullTextCount = 10, summaryCount = 20;
  try {
    const { computeBudget } = require("./context-budget.ts");
    const budget = computeBudget();
    fullTextCount = Math.min(10, Math.floor(budget.augmentBudget / 200));
    summaryCount = Math.min(20, Math.floor((budget.augmentBudget - fullTextCount * 200) / 50));
  } catch {
  }
  const sorted = [...coreMemories].sort((a, b) => {
    const memA = memoryState.memories.find((m) => m.content === a.content);
    const memB = memoryState.memories.find((m) => m.content === b.content);
    return (memB?.injectionEngagement ?? 0) - (memA?.injectionEngagement ?? 0);
  });
  const lines = [];
  for (let i = 0; i < sorted.length; i++) {
    if (i < fullTextCount) {
      lines.push(`- [${sorted[i].category}] ${sorted[i].content}`);
    } else if (i < fullTextCount + summaryCount) {
      lines.push(`- [${sorted[i].category}] ${sorted[i].content.slice(0, 20)}...`);
    } else {
      try {
        const { extractFacts } = require("./fact-store.ts");
        const facts = extractFacts(sorted[i].content);
        if (facts.length > 0) lines.push(`- ${facts.map((f) => `${f.predicate}:${f.object}`).join(",")}`);
      } catch {
      }
    }
  }
  return `[Core Memory \u2014 always available]
${lines.join("\n")}`;
}
function evaluateAndPromoteMemories() {
  if (coreMemories.length >= MAX_CORE_MEMORIES) return;
  for (const mem of memoryState.memories) {
    if (!mem || mem.scope === "expired" || mem.scope === "decayed") continue;
    const eng = mem.injectionEngagement ?? 0;
    const miss = mem.injectionMiss ?? 0;
    const engRate = eng / Math.max(1, eng + miss);
    const engSignal = engRate > 0.6 && eng >= 5 ? 1 : 0;
    let valueSignal = 0;
    if (mem.emotion === "important" || mem.emotion === "warm") valueSignal += 0.5;
    if ((mem.recallCount ?? 0) >= 3) valueSignal += 0.5;
    if (mem.scope === "preference" || mem.scope === "fact") valueSignal += 0.3;
    valueSignal = Math.min(1, valueSignal);
    let stacSignal = 0;
    const rc = mem.recallCount ?? 0;
    const ageDays = Math.max(1, (Date.now() - (mem.ts || Date.now())) / 864e5);
    const recallRate = rc / ageDays;
    if (recallRate > 0.5 && (mem.fsrs?.stability ?? 0) > 10) stacSignal = 1;
    const promoteScore = engSignal * 0.4 + valueSignal * 0.3 + stacSignal * 0.3;
    if (promoteScore > 0.5 && mem.scope !== "core_memory") {
      if (coreMemories.length >= MAX_CORE_MEMORIES) break;
      mem.scope = "core_memory";
      coreMemories.push({ content: mem.content, category: mem.scope === "preference" ? "preference" : "user_fact", addedAt: Date.now(), source: "auto" });
      try {
        require("./decision-log.ts").logDecision("unified_promote", (mem.content || "").slice(0, 30), `eng=${engSignal.toFixed(1)} val=${valueSignal.toFixed(1)} stac=${stacSignal.toFixed(1)} total=${promoteScore.toFixed(2)}`);
      } catch {
      }
      try {
        require("./memory-utils.ts").appendLineage(mem, { action: "promoted", ts: Date.now(), delta: `\u2192core_memory, score=${promoteScore.toFixed(2)}` });
      } catch {
      }
    }
    if (mem.scope === "core_memory" && eng > 0 && engRate < 0.2) {
      mem.scope = "fact";
      mem.injectionEngagement = Math.floor(eng / 2);
      mem.injectionMiss = Math.floor(miss / 2);
      coreMemories = coreMemories.filter((c) => c.content !== mem.content);
      try {
        require("./decision-log.ts").logDecision("unified_demote", (mem.content || "").slice(0, 30), `engRate=${engRate.toFixed(2)}`);
      } catch {
      }
    }
  }
}
function autoPromoteToCoreMemory() {
  evaluateAndPromoteMemories();
}
function addToHistory(user, assistant) {
  memoryState.chatHistory.push({
    user: user.slice(0, 1e3),
    assistant: assistant.slice(0, 2e3),
    ts: Date.now()
  });
  if (memoryState.chatHistory.length > MAX_HISTORY) {
    const trimmed = memoryState.chatHistory.slice(-MAX_HISTORY);
    memoryState.chatHistory.length = 0;
    memoryState.chatHistory.push(...trimmed);
  }
  if (useSQLite) {
    sqliteAddChatTurn(user, assistant);
    sqliteTrimHistory(MAX_HISTORY);
  }
  debouncedSave(HISTORY_PATH, memoryState.chatHistory);
}
function buildHistoryContext(maxTokens) {
  if (memoryState.chatHistory.length === 0) return "";
  let trimmed = memoryState.chatHistory;
  let historyBudget = maxTokens ?? 4e3;
  try {
    const { computeBudget, trimHistory } = require("./context-budget.ts");
    const budget = computeBudget();
    trimmed = trimHistory(memoryState.chatHistory, budget);
    historyBudget = budget.historyBudget;
  } catch {
    trimmed = memoryState.chatHistory.slice(-INJECT_HISTORY);
  }
  const lines = [];
  let totalTokens = 0;
  for (let i = trimmed.length - 1; i >= 0; i--) {
    const t = trimmed[i];
    const timeStr = new Date(t.ts).toLocaleTimeString("zh-CN", { hour: "2-digit", minute: "2-digit" });
    const line = `[${timeStr}] \u7528\u6237: ${t.user.slice(0, 200)}
\u52A9\u624B: ${t.assistant.slice(0, 400)}`;
    const lineTokens = Math.ceil(line.length * 0.8);
    if (totalTokens + lineTokens > historyBudget) break;
    lines.unshift(line);
    totalTokens += lineTokens;
  }
  if (lines.length === 0) return "";
  return `[\u5BF9\u8BDD\u5386\u53F2\uFF08\u6700\u8FD1${lines.length}\u8F6E\uFF09]
${lines.join("\n\n")}`;
}
const TECH_KEYWORDS = /* @__PURE__ */ new Set([
  "python",
  "javascript",
  "typescript",
  "rust",
  "golang",
  "swift",
  "kotlin",
  "java",
  "ruby",
  "php",
  "c++",
  "docker",
  "kubernetes",
  "k8s",
  "git",
  "github",
  "gitlab",
  "npm",
  "pip",
  "cargo",
  "webpack",
  "vite",
  "react",
  "vue",
  "angular",
  "svelte",
  "node",
  "deno",
  "bun",
  "flask",
  "django",
  "fastapi",
  "express",
  "nginx",
  "redis",
  "mysql",
  "postgres",
  "mongodb",
  "sqlite",
  "elasticsearch",
  "kafka",
  "rabbitmq",
  "grpc",
  "graphql",
  "rest",
  "api",
  "http",
  "https",
  "websocket",
  "tcp",
  "udp",
  "linux",
  "macos",
  "windows",
  "ios",
  "android",
  "arm64",
  "x86",
  "cpu",
  "gpu",
  "cuda",
  "llm",
  "gpt",
  "claude",
  "openai",
  "transformer",
  "embedding",
  "vector",
  "rag",
  "fine-tune",
  "lora",
  "bert",
  "ida",
  "frida",
  "mach-o",
  "elf",
  "dyld",
  "objc",
  "runtime",
  "ci",
  "cd",
  "aws",
  "gcp",
  "azure",
  "terraform",
  "ansible",
  "json",
  "yaml",
  "toml",
  "xml",
  "csv",
  "protobuf",
  "sql",
  "html",
  "css",
  "scss",
  "tailwind",
  "figma",
  "test",
  "debug",
  "deploy",
  "build",
  "compile",
  "lint",
  "async",
  "await",
  "promise",
  "thread",
  "mutex",
  "lock",
  "wechat",
  "telegram",
  "slack",
  "discord"
]);
function extractTagsLocal(content) {
  const tags = /* @__PURE__ */ new Set();
  const lower = content.toLowerCase();
  const zhMatches = content.match(/[\u4e00-\u9fff]{2,4}/g) || [];
  for (const w of zhMatches) {
    if (w.length >= 2) tags.add(w);
  }
  const enMatches = lower.match(/[a-z][a-z0-9._-]{2,}/g) || [];
  for (const w of enMatches) {
    if ([
      "the",
      "and",
      "for",
      "that",
      "this",
      "with",
      "from",
      "are",
      "was",
      "were",
      "been",
      "have",
      "has",
      "had",
      "not",
      "but",
      "what",
      "all",
      "can",
      "her",
      "his",
      "our",
      "their",
      "will",
      "would",
      "could",
      "should",
      "may",
      "might",
      "shall",
      "also",
      "into",
      "than",
      "then",
      "them",
      "these",
      "those",
      "very",
      "just",
      "about",
      "some",
      "other",
      "more",
      "only",
      "your",
      "how",
      "its",
      "let",
      "being",
      "both",
      "each",
      "few",
      "most",
      "such",
      "too",
      "any",
      "own",
      "same",
      "did",
      "does",
      "got"
    ].includes(w)) continue;
    tags.add(w);
  }
  for (const kw of TECH_KEYWORDS) {
    if (lower.includes(kw)) tags.add(kw);
  }
  const urlMatch = lower.match(/(?:https?:\/\/)?([a-z0-9.-]+\.[a-z]{2,})/g);
  if (urlMatch) {
    for (const u of urlMatch.slice(0, 2)) tags.add(u.replace(/^https?:\/\//, ""));
  }
  const sorted = [...tags].filter((t) => t.length >= 2 && t.length <= 20).sort((a, b) => a.length - b.length);
  return sorted.slice(0, 10);
}
const tagQueue = [];
let tagBatchTimer = null;
function queueForTagging(content, ts, index) {
  tagQueue.push({ content, ts, index });
  if (tagQueue.length >= 20) {
    flushTagQueue();
  } else if (!tagBatchTimer) {
    tagBatchTimer = setTimeout(flushTagQueue, 2e3);
  }
}
function flushTagQueue() {
  if (tagBatchTimer) {
    clearTimeout(tagBatchTimer);
    tagBatchTimer = null;
  }
  if (tagQueue.length === 0) return;
  const batch = tagQueue.splice(0, 50);
  let tagged = 0;
  for (const item of batch) {
    const tags = extractTagsLocal(item.content);
    if (tags.length < 2) continue;
    let target;
    if (item.ts) {
      target = memoryState.memories.find((m) => m.ts === item.ts && m.content === item.content && !m.tags);
    }
    if (!target && item.index !== void 0 && item.index >= 0 && item.index < memoryState.memories.length) {
      const candidate = memoryState.memories[item.index];
      if (candidate.content === item.content && !candidate.tags) {
        target = candidate;
      }
    }
    if (!target) {
      target = memoryState.memories.find((m) => m.content === item.content && !m.tags);
    }
    if (target) {
      target.tags = tags;
      tagged++;
    }
  }
  if (tagged > 0) saveMemories();
}
function batchTagUntaggedMemories() {
  const untagged = memoryState.memories.map((m, i) => ({ m, i })).filter(({ m }) => !m.tags || m.tags.length === 0).slice(0, 5);
  if (untagged.length === 0) return;
  console.log(`[cc-soul][tags] batch tagging ${untagged.length} untagged memories`);
  for (const { m, i } of untagged) {
    queueForTagging(m.content, m.ts, i);
  }
}
function decideMemoryAction(newContent, scope) {
  if (memoryState.memories.length === 0) return { action: "add", targetIndex: -1 };
  const shortKey = newContent.slice(0, 50).toLowerCase();
  const exactContent = contentIndex.get(shortKey);
  if (exactContent !== void 0 && exactContent === newContent) {
    const exactIdx = memoryState.memories.findIndex((m) => m.content === newContent);
    if (exactIdx >= 0) return { action: "skip", targetIndex: exactIdx };
  }
  const newTri = trigrams(newContent);
  const candidates = [];
  const startIdx = Math.max(0, memoryState.memories.length - 500);
  for (let i = startIdx; i < memoryState.memories.length; i++) {
    const mem = memoryState.memories[i];
    if (mem.scope === "expired") continue;
    if (mem.content === newContent) return { action: "skip", targetIndex: i };
    const memTri = trigrams(mem.content);
    const sim = trigramSimilarity(newTri, memTri);
    if (sim > 0.25) {
      candidates.push({ idx: i, sim });
    }
  }
  candidates.sort((a, b) => b.sim - a.sim);
  try {
    for (const c of candidates.slice(0, 5)) {
      const mem = memoryState.memories[c.idx];
      if (mem) {
        const ctxSim = contextAwareSimilarity({ content: newContent, ts: Date.now(), scope: scope || "fact" }, mem);
        c.sim = c.sim * 0.6 + ctxSim * 0.4;
      }
    }
    candidates.sort((a, b) => b.sim - a.sim);
  } catch {
  }
  const best = candidates[0];
  if (!best) return { action: "add", targetIndex: -1 };
  if (best.sim > 0.9) return { action: "update", targetIndex: best.idx };
  if (best.sim < 0.5) return { action: "add", targetIndex: -1 };
  const existingMem = memoryState.memories[best.idx];
  const dedupThreshold = getParam("memory.trigram_dedup_threshold");
  if (best.sim > dedupThreshold) {
    return { action: "update", targetIndex: best.idx };
  }
  const existingLen = existingMem.content.length;
  const newLen = newContent.length;
  const lengthRatio = Math.min(existingLen, newLen) / Math.max(existingLen, newLen);
  const scopeMatch = scope === existingMem.scope ? 1 : 0;
  const sameDay = Math.abs(Date.now() - existingMem.ts) < 864e5 ? 1 : 0;
  const dupScore = best.sim * 0.5 + scopeMatch * 0.2 + lengthRatio * 0.2 + sameDay * 0.1;
  if (dupScore > 0.75) {
    return { action: "skip", targetIndex: best.idx };
  }
  if (dupScore > 0.55) {
    return { action: "update", targetIndex: best.idx };
  }
  return { action: "add", targetIndex: -1 };
}
function updateMemory(index, newContent) {
  if (index < 0 || index >= memoryState.memories.length) return;
  const mem = memoryState.memories[index];
  const oldContent = mem.content;
  createMemoryVersion(oldContent, newContent, mem.scope);
  if (!mem.history) mem.history = [];
  mem.history.push({ content: oldContent, ts: mem.ts });
  if (mem.history.length > 5) mem.history.shift();
  const _MS = /* @__PURE__ */ new Set(["the", "and", "that", "this", "was", "for", "are", "but", "not", "you", "all", "can", "had", "her", "one", "our", "out", "day", "get", "has", "him", "his", "how", "its", "new", "now", "see", "way", "who", "did", "got", "say", "she", "too", "use", "with", "been", "from", "have", "just", "like", "make", "more", "much", "some", "than", "them", "then", "they", "very", "what", "when", "will", "your", "about", "after", "could", "first", "great", "into", "most", "over", "such", "take", "their", "these", "those", "time", "want", "would", "also", "back", "come", "each", "find", "give", "going", "good", "here", "know", "last", "long", "look", "made", "need", "only", "said", "tell", "went", "were", "well", "work", "really", "think", "because", "where", "there"]);
  const _oldW = new Set(((oldContent || "").toLowerCase().match(/[a-z]{4,}/g) || []).filter((w) => !_MS.has(w)));
  const _newW = new Set((newContent.toLowerCase().match(/[a-z]{4,}/g) || []).filter((w) => !_MS.has(w)));
  const _lost = [];
  for (const w of _oldW) {
    if (!_newW.has(w)) _lost.push(w);
  }
  if (_lost.length > 0) {
    mem._mergedKeywords = (mem._mergedKeywords || []).concat(_lost).slice(-10);
  }
  mem.content = newContent;
  mem.ts = Date.now();
  mem.lastAccessed = Date.now();
  mem.tags = void 0;
  try {
    const delta = newContent.length > oldContent.length ? `+${newContent.replace(oldContent, "").slice(0, 40)}` : `~${newContent.slice(0, 40)}`;
    appendLineage(mem, { action: "reshaped", ts: Date.now(), delta });
  } catch {
  }
  invalidateIDF();
  invalidateFieldIDF();
  rebuildScopeIndex();
  saveMemories();
  if (newContent.length > 10) {
    queueForTagging(newContent, mem.ts, index);
  }
  console.log(`[cc-soul][memory] updated: "${oldContent.slice(0, 40)}" \u2192 "${newContent.slice(0, 40)}"`);
}
function retroactiveInterference(oldMem, newContent, similarity) {
  if (similarity < 0.3 || similarity > 0.85) return false;
  if (oldMem.scope !== "fact" && oldMem.scope !== "preference") return false;
  const oldWords = new Set((oldMem.content.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map((w) => w.toLowerCase()));
  const newWords = new Set((newContent.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map((w) => w.toLowerCase()));
  const addedWords = [];
  for (const w of newWords) {
    if (!oldWords.has(w)) addedWords.push(w);
  }
  if (addedWords.length === 0) return false;
  if (!oldMem.history) oldMem.history = [];
  if (oldMem.history.length < 5) {
    oldMem.history.push({ content: oldMem.content, ts: Date.now() });
  }
  const supplement = addedWords.slice(0, 3).join("\u3001");
  oldMem.content = `${oldMem.content}\uFF08\u8865\u5145\uFF1A${supplement}\uFF09`;
  oldMem.confidence = Math.max(0.3, (oldMem.confidence ?? 0.7) * 0.85);
  oldMem.ts = Date.now();
  console.log(`[cc-soul][interference] reshaped: "${oldMem.content.slice(0, 50)}" (+${supplement})`);
  return true;
}
function metabolize(newContent, memories) {
  let extractFn;
  try {
    extractFn = require("./fact-store.ts").extractFacts;
  } catch {
    return { action: "PASS" };
  }
  const newFacts = extractFn(newContent);
  if (newFacts.length === 0) return { action: "PASS" };
  const newEntities = new Set(newFacts.map((f) => f.subject).concat(newFacts.map((f) => f.object)));
  const recent = memories.slice(-30).filter((m) => m.scope !== "expired" && m.scope !== "decayed");
  for (const old of recent) {
    const oldFacts = extractFn(old.content);
    if (oldFacts.length === 0) continue;
    const oldEntities = new Set(oldFacts.map((f) => f.subject).concat(oldFacts.map((f) => f.object)));
    const shared = [...newEntities].filter((e) => oldEntities.has(e));
    if (shared.length === 0) continue;
    const hasConflict = newFacts.some(
      (nf) => oldFacts.some((of) => of.subject === nf.subject && of.predicate === nf.predicate && of.object !== nf.object)
    );
    if (hasConflict) continue;
    const complement = newFacts.filter(
      (nf) => !oldFacts.some((of) => of.subject === nf.subject && of.predicate === nf.predicate)
    );
    if (complement.length > 0) {
      return { action: "ABSORB", target: old, newFacts: complement };
    }
  }
  for (const e of newEntities) {
    let count = 0;
    for (const m of recent) {
      if (m.content.includes(e)) count++;
    }
    if (count >= 3) {
      return { action: "CRYSTALLIZE", entity: e };
    }
  }
  return { action: "PASS" };
}
function markComplementCandidates(newMem, memories, maxCandidates = 3) {
  if (memories.length === 0 || !newMem.memoryId) return;
  let newEntities;
  try {
    const { findMentionedEntities } = require("./graph.ts");
    newEntities = new Set(findMentionedEntities(newMem.content));
  } catch {
    return;
  }
  if (newEntities.size === 0) return;
  const now = Date.now();
  const THIRTY_MIN = 30 * 60 * 1e3;
  const candidates = [];
  const recent = memories.slice(-50);
  for (const m of recent) {
    if (!m.memoryId || m.content === newMem.content) continue;
    if (m.scope === "expired" || m.scope === "decayed") continue;
    let mEntities;
    try {
      const { findMentionedEntities } = require("./graph.ts");
      mEntities = new Set(findMentionedEntities(m.content));
    } catch {
      continue;
    }
    let sharedEntities = 0;
    for (const e of newEntities) {
      if (mEntities.has(e)) sharedEntities++;
    }
    const timeDiff = Math.abs(now - m.ts);
    if (sharedEntities >= 1 && timeDiff < THIRTY_MIN) {
      candidates.push(m.memoryId);
      if (candidates.length >= maxCandidates) break;
      continue;
    }
    const sim = trigramSimilarity(trigrams(newMem.content), trigrams(m.content));
    if (sim >= 0.2 && sim < 0.6 && sharedEntities >= 1) {
      candidates.push(m.memoryId);
      if (candidates.length >= maxCandidates) break;
    }
  }
  if (candidates.length > 0) {
    newMem._complementOf = candidates;
    try {
      require("./decision-log.ts").logDecision("complement_mark", newMem.content.slice(0, 30), `candidates=${candidates.length}, entities=${[...newEntities].join("/")}`);
    } catch {
    }
  }
}
function suppressSimilarMemories(newMem) {
  const newTri = trigrams(newMem.content);
  const MIN_AGE_MS = 36e5;
  let suppressed = 0;
  let reshaped = 0;
  const startIdx = Math.max(0, memoryState.memories.length - 500);
  for (let i = startIdx; i < memoryState.memories.length - 1; i++) {
    const old = memoryState.memories[i];
    if (old.scope === "expired" || old.scope === "archived") continue;
    if (old.content === newMem.content) continue;
    if (Date.now() - old.ts < MIN_AGE_MS) continue;
    const relatedScope = old.scope === newMem.scope || newMem.scope === "correction" && old.scope === "fact" || newMem.scope === "fact" && old.scope === "fact";
    if (!relatedScope) continue;
    const oldTri = trigrams(old.content);
    const sim = trigramSimilarity(newTri, oldTri);
    if (sim > 0.6) {
      const oldContent = old.content;
      const wasReshaped = retroactiveInterference(old, newMem.content, sim);
      if (wasReshaped) {
        reshaped++;
        if (useSQLite) {
          const found = sqliteFindByContent(oldContent);
          if (found) sqliteUpdateMemory(found.id, { content: old.content, confidence: old.confidence, ts: old.ts });
        }
      } else {
        bayesPenalize(old, 1.5);
        if (old.confidence < 0.2) {
          old.scope = "expired";
          console.log(`[cc-soul][interference] expired: "${old.content.slice(0, 50)}" (suppressed by new memory)`);
        }
        suppressed++;
        syncToSQLite(old, { confidence: old.confidence, scope: old.scope });
      }
      if (suppressed + reshaped >= 5) break;
    }
  }
  if (suppressed > 0 || reshaped > 0) {
    console.log(`[cc-soul][interference] ${suppressed} suppressed, ${reshaped} reshaped`);
  }
}
function loadMemories() {
  _memoriesLoaded = true;
  const sqliteOk = initSQLite();
  _sqliteInitDone = true;
  if (sqliteOk) {
    const fromDb = sqliteGetAll(true);
    if (fromDb.length > 0) {
      useSQLite = true;
      memoryState.memories.length = 0;
      memoryState.memories.push(...fromDb);
    } else {
      useSQLite = true;
      console.log(`[cc-soul][memory] SQLite empty, starting fresh (independent db mode)`);
    }
    const historyFromDb = sqliteGetRecentHistory(MAX_HISTORY);
    memoryState.chatHistory.length = 0;
    memoryState.chatHistory.push(...historyFromDb);
    console.log(`[cc-soul][memory] loaded ${fromDb.length} memories from SQLite`);
  } else {
    const loaded = loadJson(MEMORIES_PATH, []);
    memoryState.memories.length = 0;
    memoryState.memories.push(...loaded);
    const loadedHistory = loadJson(HISTORY_PATH, []);
    memoryState.chatHistory.length = 0;
    memoryState.chatHistory.push(...loadedHistory);
    console.log(`[cc-soul][memory] loaded ${loaded.length} memories from JSON (SQLite unavailable)`);
  }
  let repaired = 0;
  const loadNow = Date.now();
  for (const mem of memoryState.memories) {
    if (!mem.ts || mem.ts === 0) {
      mem.ts = mem.lastAccessed || loadNow - Math.random() * 30 * 864e5;
      repaired++;
    }
  }
  if (repaired > 0) {
    console.log(`[cc-soul][memory] repaired ${repaired} memories with ts=0`);
    saveMemories();
  }
  const RECOVERY_FLAG = resolve(DATA_DIR, ".decay_recovered");
  if (!existsSync(RECOVERY_FLAG)) {
    let recovered = 0;
    for (const mem of memoryState.memories) {
      if (mem.scope === "decayed" && mem.ts > 0) {
        const age = Date.now() - mem.ts;
        if (age < 90 * 864e5) {
          mem.scope = "mid_term";
          mem.tier = "mid_term";
          recovered++;
        }
      }
    }
    if (recovered > 0) {
      console.log(`[cc-soul][memory] recovered ${recovered} wrongly-decayed memories`);
      saveMemories();
    }
    try {
      writeFileSync(RECOVERY_FLAG, Date.now().toString());
    } catch (e) {
      console.error(`[cc-soul][memory] failed to write recovery flag: ${e.message}`);
    }
  }
  rebuildScopeIndex();
  rebuildRecallIndex(memoryState.memories);
}
function saveMemories() {
  if (memoryState.memories.length === 0) {
    try {
      const { size } = statSync(MEMORIES_PATH);
      if (size > 2) {
        console.error(`[cc-soul][memory] BLOCKED: refusing to overwrite ${size}-byte file with empty array`);
        return;
      }
    } catch {
    }
  }
}
function createMemoryVersion(oldContent, newContent, scope) {
  const existing = memoryState.memories.find(
    (m) => m.content === oldContent && m.scope !== "expired" && (!m.validUntil || m.validUntil === 0)
  );
  if (!existing) {
    addMemory(newContent, scope || "fact");
    return;
  }
  existing.validUntil = Date.now();
  const history = [...existing.history || []];
  history.push({ content: existing.content, ts: existing.ts });
  if (history.length > 10) history.splice(0, history.length - 10);
  const newMem = {
    content: newContent,
    scope: existing.scope,
    ts: Date.now(),
    userId: existing.userId,
    visibility: existing.visibility,
    channelId: existing.channelId,
    confidence: existing.confidence ?? 0.7,
    lastAccessed: Date.now(),
    tier: existing.tier || "short_term",
    recallCount: 0,
    validFrom: Date.now(),
    validUntil: 0,
    tags: existing.tags,
    history
  };
  memoryState.memories.push(newMem);
  if (useSQLite) {
    sqliteAddMemory(newMem);
  }
  saveMemories();
}
function queryMemoryTimeline(keyword) {
  const results = [];
  for (const mem of memoryState.memories) {
    if (!mem.content.toLowerCase().includes(keyword.toLowerCase())) continue;
    if (typeof mem.validFrom === "number") {
      results.push({
        content: mem.content,
        from: mem.validFrom,
        until: mem.validUntil && mem.validUntil > 0 ? mem.validUntil : null
      });
    }
    if (mem.history) {
      for (const h of mem.history) {
        if (h.content.toLowerCase().includes(keyword.toLowerCase())) {
          results.push({ content: h.content, from: h.ts, until: mem.validFrom || mem.ts });
        }
      }
    }
  }
  results.sort((a, b) => b.from - a.from);
  return results;
}
function autoLinkMemories(newMem) {
  const recent = memoryState.memories.slice(-6, -1);
  if (recent.length === 0) return;
  const newTri = trigrams(newMem.content);
  const newLabel = newMem.content.slice(0, 20);
  for (const old of recent) {
    const oldTri = trigrams(old.content);
    const overlap = trigramSimilarity(newTri, oldTri);
    if (/因为|所以|导致|结果|于是|because|therefore/.test(newMem.content) && overlap > 0.15) {
      addRelation(newLabel, old.content.slice(0, 20), "caused_by");
      continue;
    }
    if (newMem.scope === "correction" && old.scope === "fact" && overlap > 0.3) {
      addRelation(newLabel, old.content.slice(0, 20), "contradicts");
      continue;
    }
    if (Math.abs(newMem.ts - (old.ts || 0)) < 3e5 && overlap > 0.2) {
      addRelation(newLabel, old.content.slice(0, 20), "follows");
    }
  }
}
function computeSurprise(content, scope, _userId) {
  let score = 5;
  if (/名字|叫我|职业|住在|工作|年龄|生日|毕业|my name|call me|i work|i live|birthday|graduated|i'm a/i.test(content)) score = 9;
  if (/喜欢|讨厌|偏好|习惯|最爱|受不了|i like|i love|i hate|i prefer|i enjoy|favorite|can't stand/i.test(content)) score = 7;
  if (/\bi (went|did|have|had|made|took)\b/i.test(content)) score = Math.max(score, 4);
  if (scope === "correction") score = 8;
  if (/[！!]{2,}|卧槽|崩溃|太开心|难受|焦虑|omg|fuck|shit|so happy|breaking down|anxious/i.test(content)) score += 2;
  if (/今天|刚才|现在|刚刚/i.test(content)) score -= 2;
  if (/today|just now|right now|earlier today/i.test(content)) score -= 1;
  if (/^(你好|嗯+|好的?|谢谢|哈哈+|ok|行吧?|收到|了解|明白|可以|没问题|好吧|哦+|是的?|嗯嗯|对的?|没事|算了|随便|都行|无所谓|不用了?|知道了)$/i.test(content.trim())) score = 1;
  if (/^.{0,15}(天气|堵车|迟到|周[一二三四五六日末]|终于.*休息|几点了|现在几点|路上)/.test(content) && content.length < 25) score = Math.min(score, 2);
  if (content.length < 10) score -= 1;
  if (content.length <= 4 && !/[a-zA-Z]{3,}/.test(content)) score = 1;
  return Math.max(1, Math.min(10, score));
}
const COREF_PRONOUN_VERB = /(^|[，,])(他|她)(说|让|要|觉得|认为|提到|问|给|跟)/g;
const COREF_DEMONSTRATIVE = /(这个人|那个人|那家伙)/g;
const COREF_PLURAL = /他们|她们/;
function resolveCoreferenceForStorage(content, chatHistory) {
  if (COREF_PLURAL.test(content)) {
    return { resolved: content, changed: false };
  }
  if (!COREF_PRONOUN_VERB.test(content) && !COREF_DEMONSTRATIVE.test(content)) {
    return { resolved: content, changed: false };
  }
  COREF_PRONOUN_VERB.lastIndex = 0;
  COREF_DEMONSTRATIVE.lastIndex = 0;
  let entities = [];
  try {
    const { findMentionedEntities: fme } = require("./graph.ts");
    const recentText = chatHistory.slice(-3).map((h) => h.user + (h.assistant || "")).join(" ");
    entities = fme(recentText);
  } catch {
  }
  if (entities.length !== 1) {
    return { resolved: content, changed: false };
  }
  const entity = entities[0];
  let resolved = content.replace(COREF_PRONOUN_VERB, (_, prefix, _pronoun, verb) => `${prefix}${entity}${verb}`).replace(COREF_DEMONSTRATIVE, entity);
  COREF_PRONOUN_VERB.lastIndex = 0;
  COREF_DEMONSTRATIVE.lastIndex = 0;
  const changed = resolved !== content;
  if (changed) {
    try {
      require("./decision-log.ts").logDecision("coreference", content.slice(0, 40), `\u2192 ${entity}: ${resolved.slice(0, 60)}`);
    } catch {
    }
  }
  return { resolved, changed, resolvedEntity: changed ? entity : void 0 };
}
function addMemory(content, scope, userId, visibility, channelId, situationCtx, skipAutoExtract) {
  try {
    const mod = getLazyModule("handler-state");
    const getSessionState = mod?.getSessionState;
    const getLastActiveSessionKey = mod?.getLastActiveSessionKey;
    const sess = getSessionState(getLastActiveSessionKey());
    if (sess?._skipNextMemory) {
      sess._skipNextMemory = false;
      console.log("[cc-soul][memory] skipped by user request (\u522B\u8BB0\u8FD9\u4E2A)");
      return;
    }
  } catch {
  }
  if (!content || content.length < 3) return;
  const REJECT_CONTENT_PATTERNS = [
    /^(嗯|好的?|ok|收到|谢谢|thx|thanks|明白|懂了|了解|got it|知道了|可以|行|对|没问题|好吧)[\s。！!.]*$/i,
    /^.{0,4}$/
    // 太短（<5字）无信息量
  ];
  if (scope !== "correction" && scope !== "preference") {
    for (const pat of REJECT_CONTENT_PATTERNS) {
      if (pat.test(content.trim())) {
        return;
      }
    }
  }
  const VALID_SCOPES = /* @__PURE__ */ new Set([
    "preference",
    "fact",
    "event",
    "opinion",
    "topic",
    "correction",
    "consolidated",
    "discovery",
    "task",
    "reflexion",
    "gratitude",
    "visual",
    "dream",
    "curiosity",
    "reflection",
    "proactive",
    "insight"
  ]);
  if (!VALID_SCOPES.has(scope)) scope = "fact";
  const dedupeKey = content.slice(0, 60) + "|" + scope;
  if (_recentWriteHashes.has(dedupeKey)) return;
  _recentWriteHashes.add(dedupeKey);
  if (_recentWriteHashes.size > 500) {
    const iterator = _recentWriteHashes.values();
    const remaining = [..._recentWriteHashes].slice(-400);
    _recentWriteHashes.clear();
    for (const k of remaining) _recentWriteHashes.add(k);
  }
  const SYSTEM_PREFIXES = ["[Working Memory", "[\u5F53\u524D\u9762\u5411:", "[\u9690\u79C1\u6A21\u5F0F]", "[System]", "[\u5B89\u5168\u8B66\u544A]", "[\u5143\u8BA4\u77E5\u8B66\u544A]"];
  if (SYSTEM_PREFIXES.some((p) => content.includes(p))) {
    console.log(`[cc-soul][memory-crud] REJECT (system augment): ${content.slice(0, 60)}`);
    return;
  }
  if (detectMemoryPoisoning(content)) {
    console.log(`[cc-soul][memory-integrity] REJECT (poisoning pattern): ${content.slice(0, 60)}`);
    return;
  }
  const decision = decideMemoryAction(content, scope);
  if (decision.action === "skip") {
    console.log(`[cc-soul][memory-crud] SKIP (duplicate): ${content.slice(0, 60)}`);
    return;
  }
  if (decision.action === "update") {
    console.log(`[cc-soul][memory-crud] UPDATE #${decision.targetIndex}: ${content.slice(0, 60)}`);
    updateMemory(decision.targetIndex, content);
    return;
  }
  let _supersededMemId;
  try {
    const { extractFacts, queryFacts } = require("./fact-store.ts");
    const newFacts = extractFacts(content);
    for (const f of newFacts) {
      const existing = queryFacts({ subject: f.subject, predicate: f.predicate });
      if (existing.length > 0 && existing[0].object !== f.object) {
        if (existing[0].ts && Date.now() < existing[0].ts) continue;
        const oldMem = memoryState.memories.find((m) => m.content && m.content.includes(existing[0].object));
        if (!oldMem) continue;
        const conflictType = classifyConflict([{ subject: f.subject, predicate: f.predicate, object: existing[0].object }], [f]);
        if (conflictType === "supersede") {
          _supersededMemId = oldMem.memoryId;
          oldMem.supersededBy = "pending";
          oldMem.scope = "historical";
          try {
            appendLineage(oldMem, { action: "superseded", ts: Date.now(), delta: `\u88AB\u53D6\u4EE3: ${f.object} \u66FF\u4EE3 ${existing[0].object}` });
          } catch {
          }
          try {
            const { logDecision } = require("./decision-log.ts");
            logDecision("supersede", (oldMem.content || "").slice(0, 30), `${f.predicate}: ${existing[0].object}\u2192${f.object}`);
          } catch {
          }
        } else {
          try {
            const { penalizeTruthfulness } = require("./smart-forget.ts");
            penalizeTruthfulness(oldMem, `\u88AB\u65B0\u4E8B\u5B9E\u8865\u5145: ${f.object}`);
          } catch {
          }
        }
      }
    }
  } catch {
  }
  const surprise = computeSurprise(content, scope, userId);
  if (surprise <= 1 && scope !== "correction" && scope !== "preference") {
    console.log(`[cc-soul][memory-crud] SKIP (low surprise=${surprise}): ${content.slice(0, 60)}`);
    return;
  }
  let autoSituationCtx = situationCtx;
  if (!autoSituationCtx) {
    try {
      const bodyMod = getLazyModule("body");
      const body = bodyMod?.body;
      if (body && typeof body.mood === "number") {
        autoSituationCtx = { mood: body.mood, energy: body.energy };
      }
    } catch {
    }
  }
  let _eventTime;
  try {
    const now = Date.now();
    const DAY = 864e5;
    const text = content;
    if (/昨天/.test(text)) _eventTime = now - DAY;
    else if (/前天/.test(text)) _eventTime = now - 2 * DAY;
    else if (/上周/.test(text)) _eventTime = now - 7 * DAY;
    else if (/上个月/.test(text)) _eventTime = now - 30 * DAY;
    else if (/去年/.test(text)) _eventTime = now - 365 * DAY;
    else {
      const cnDays = text.match(/(\d+)\s*天前/);
      if (cnDays) _eventTime = now - parseInt(cnDays[1]) * DAY;
      const cnMonths = text.match(/(\d+)\s*个月前/);
      if (cnMonths) _eventTime = now - parseInt(cnMonths[1]) * 30 * DAY;
    }
    if (!_eventTime) {
      if (/yesterday/i.test(text)) _eventTime = now - DAY;
      else if (/last\s+week/i.test(text)) _eventTime = now - 7 * DAY;
      else if (/last\s+month/i.test(text)) _eventTime = now - 30 * DAY;
      else if (/last\s+year/i.test(text)) _eventTime = now - 365 * DAY;
      else {
        const enAgo = text.match(/(\d+)\s+(days?|weeks?|months?|years?)\s+ago/i);
        if (enAgo) {
          const n = parseInt(enAgo[1]);
          const u = enAgo[2].toLowerCase();
          if (u.startsWith("day")) _eventTime = now - n * DAY;
          else if (u.startsWith("week")) _eventTime = now - n * 7 * DAY;
          else if (u.startsWith("month")) _eventTime = now - n * 30 * DAY;
          else if (u.startsWith("year")) _eventTime = now - n * 365 * DAY;
        }
      }
    }
  } catch {
  }
  const resolvedVisibility = visibility || defaultVisibility(scope);
  const newIndex = memoryState.memories.length;
  const FACT_SCOPES = ["fact", "preference", "correction", "discovery"];
  const autoSource = scope === "correction" || scope === "preference" || scope === "gratitude" ? "user_said" : scope === "fact" || scope === "event" || scope === "visual" ? "ai_observed" : scope === "reflexion" || scope === "curiosity" || scope === "dream" ? "ai_inferred" : "system";
  const autoNetwork = scope === "fact" && !/用户|我|你/.test(content) ? "world" : scope === "preference" || /喜欢|讨厌|觉得|偏好/.test(content) ? "opinion" : scope === "event" || autoSource === "ai_observed" ? "experience" : void 0;
  const autoEmotionIntensity = content.includes("\uFF01") || content.includes("!") ? 0.8 : scope === "correction" ? 0.7 : scope === "gratitude" ? 0.6 : 0.3;
  const generationBoost = autoSource === "user_said" || scope === "preference" || scope === "correction" ? 0.85 : autoSource === "ai_observed" || scope === "fact" ? 0.7 : scope === "reflexion" || scope === "insight" || scope === "consolidated" ? 0.6 : 0.7;
  let _corefHistory;
  const corefResult = resolveCoreferenceForStorage(content, memoryState.chatHistory);
  if (corefResult.changed) {
    _corefHistory = [{ content, ts: Date.now() }];
    content = corefResult.resolved;
  }
  const _corefContent = content;
  if (!corefResult.changed && /他|她|它|这个|那个/.test(content)) {
    try {
      const { hasLLM, spawnCLI } = require("./cli.ts");
      if (hasLLM()) {
        const recentContext = memoryState.chatHistory.slice(-3).map((h) => h.user).join("\n");
        spawnCLI(
          `\u4E0A\u4E0B\u6587\uFF1A
${recentContext}

\u5F53\u524D\u53E5\u5B50\uFF1A"${_corefContent}"

\u8BF7\u628A\u53E5\u5B50\u4E2D\u7684\u4EE3\u8BCD\uFF08\u4ED6/\u5979/\u5B83/\u8FD9\u4E2A/\u90A3\u4E2A\uFF09\u66FF\u6362\u4E3A\u5177\u4F53\u7684\u4EBA\u540D\u6216\u4E8B\u7269\u540D\u3002\u53EA\u8F93\u51FA\u66FF\u6362\u540E\u7684\u53E5\u5B50\uFF0C\u4E0D\u8981\u89E3\u91CA\u3002\u5982\u679C\u65E0\u6CD5\u786E\u5B9A\u6307\u4EE3\uFF0C\u539F\u6837\u8F93\u51FA\u3002`,
          (output) => {
            if (!output || output.length < 3) return;
            const resolved = output.trim().split("\n")[0];
            const mem = memoryState.memories.find((m) => m.content === _corefContent && Math.abs(m.ts - Date.now()) < 5e3);
            if (mem && resolved !== _corefContent) {
              if (!mem.history) mem.history = [];
              mem.history.push({ content: mem.content, ts: Date.now() });
              mem.content = resolved;
              try {
                const { sqliteFindByContent: sqliteFindByContent2, sqliteUpdateMemory: sqliteUpdateMemory2 } = require("./sqlite-store.ts");
                const found = sqliteFindByContent2(_corefContent);
                if (found) sqliteUpdateMemory2(found.id, { content: resolved });
              } catch {
              }
              try {
                updateRecallIndex(mem);
              } catch {
              }
              try {
                require("./decision-log.ts").logDecision("coreference_llm", resolved.slice(0, 30), `original: ${_corefContent.slice(0, 30)}`);
              } catch {
              }
            }
          },
          1e4
        );
      }
    } catch {
    }
  }
  const newMem = {
    memoryId: generateMemoryId(),
    content,
    scope,
    ts: Date.now(),
    userId,
    visibility: resolvedVisibility,
    channelId,
    bayesAlpha: BAYES_DEFAULT_ALPHA,
    bayesBeta: BAYES_DEFAULT_BETA,
    confidence: generationBoost,
    lastAccessed: Date.now(),
    tier: "short_term",
    recallCount: 0,
    lineage: [{ action: "created", ts: Date.now(), trigger: autoSource, delta: scope }],
    source: autoSource,
    network: autoNetwork,
    emotionIntensity: autoEmotionIntensity,
    importance: surprise,
    ...FACT_SCOPES.includes(scope) ? { validFrom: _eventTime || Date.now(), validUntil: 0 } : {},
    ...!FACT_SCOPES.includes(scope) && _eventTime ? { validFrom: _eventTime } : {},
    ...extractReasoning(content),
    ...autoSituationCtx ? { situationCtx: autoSituationCtx } : {},
    ..._corefHistory ? { history: _corefHistory } : {},
    _segmentId: getCurrentSegmentId()
  };
  try {
    const { expandQuery } = require("./aam.ts");
    const _ptWords = (content.match(/[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}/gi) || []).slice(0, 5);
    if (_ptWords.length >= 2) {
      const _ptLower = content.toLowerCase();
      const _ptExpanded = expandQuery(_ptWords.map((w) => w.toLowerCase()), 10);
      const _ptThreshold = _ptExpanded.length < 3 ? 0.3 : 0.5;
      const _ptTags = _ptExpanded.filter((e) => e.weight >= _ptThreshold && !_ptLower.includes(e.word) && e.word.length >= 2).map((e) => e.word).slice(0, 8);
      if (_ptTags.length > 0) newMem.prospectiveTags = _ptTags;
    }
  } catch {
  }
  try {
    const _ents = require("./graph.ts").findMentionedEntities(content);
    if (_ents.length > 0) newMem._entityIds = _ents.slice(0, 10);
  } catch {
  }
  if (autoEmotionIntensity >= 0.7) {
    let _bodyMod2 = null;
    try {
      _bodyMod2 = require("./body.ts");
    } catch {
    }
    const recentCtx = memoryState.chatHistory.slice(-3).map((h) => h.user.slice(0, 40)).join(" \u2192 ");
    let people = [];
    try {
      people = require("./graph.ts").findMentionedEntities(content).slice(0, 5);
    } catch {
    }
    try {
      require("./decision-log.ts").logDecision("flashbulb", content.slice(0, 30), `emotionIntensity=${autoEmotionIntensity.toFixed(2)}, mood=${_bodyMod2?.body?.mood?.toFixed(2) ?? "?"}`);
    } catch {
    }
    newMem.flashbulb = {
      surroundingContext: recentCtx || "(\u65E0\u4E0A\u4E0B\u6587)",
      bodyState: { mood: _bodyMod2?.body?.mood ?? 0, energy: _bodyMod2?.body?.energy ?? 0.5 },
      mentionedPeople: people,
      detailLevel: "full"
    };
  }
  const causalMatch = content.match(/(?:because|因为|由于|是因为|之所以.*?是|所以选.*?是因为)\s*[,，:：]?\s*(.{4,80}?)(?:[。.!！;；]|$)/i);
  if (causalMatch) newMem.because = causalMatch[1].trim();
  const PROSPECTIVE_PATTERNS = [
    { detect: /下周.*面试|面试.*下周|interview.*next week|next week.*interview/i, trigger: "\u9762\u8BD5|\u7D27\u5F20|\u51C6\u5907|interview|nervous|prepare", action: "\u4E3B\u52A8\u95EE\u9762\u8BD5\u51C6\u5907\u5F97\u600E\u4E48\u6837/ask about interview prep", days: 14 },
    { detect: /要出差|出差.*天|business trip|traveling for work/i, trigger: "\u51FA\u5DEE|\u673A\u573A|\u9152\u5E97|business trip|airport|hotel", action: "\u95EE\u51FA\u5DEE\u987A\u5229\u5417/ask how the trip went", days: 14 },
    { detect: /deadline|截止|交付|due date/i, trigger: "deadline|\u622A\u6B62|\u8FDB\u5EA6|progress|due", action: "\u95EE\u9879\u76EE\u8FDB\u5EA6/ask about progress", days: 14 },
    { detect: /搬家|要搬|moving house|relocating/i, trigger: "\u642C\u5BB6|\u65B0\u623F|\u5730\u5740|moving|new place|address", action: "\u95EE\u642C\u5BB6\u987A\u5229\u5417/ask how the move went", days: 30 },
    { detect: /考试|备考|exam|test prep/i, trigger: "\u8003\u8BD5|\u6210\u7EE9|\u901A\u8FC7|exam|results|passed", action: "\u95EE\u8003\u8BD5\u7ED3\u679C/ask about exam results", days: 30 }
  ];
  for (const p of PROSPECTIVE_PATTERNS) {
    if (p.detect.test(content)) {
      newMem.prospective = { trigger: p.trigger, expiresAt: Date.now() + p.days * 864e5, action: p.action };
      break;
    }
  }
  const metabolism = metabolize(content, memoryState.memories);
  if (metabolism.action === "ABSORB" && metabolism.target && metabolism.newFacts) {
    const factStr = metabolism.newFacts.map((f) => `${f.predicate === "likes" ? "\u559C\u6B22" : f.predicate}${f.object}`).join("\uFF0C");
    metabolism.target.content = `${metabolism.target.content}\uFF0C${factStr}`.slice(0, 200);
    metabolism.target.ts = Date.now();
    metabolism.target.lastAccessed = Date.now();
    try {
      appendLineage(metabolism.target, { action: "merged", ts: Date.now(), delta: `absorbed ${metabolism.newFacts.length} facts` });
    } catch {
    }
    try {
      require("./decision-log.ts").logDecision("metabolism_absorb", metabolism.target.content.slice(0, 30), `absorbed ${metabolism.newFacts.length} facts`);
    } catch {
    }
    syncToSQLite(metabolism.target, { content: metabolism.target.content, ts: metabolism.target.ts, lastAccessed: metabolism.target.lastAccessed });
    updateRecallIndex(metabolism.target);
    emitCacheEvent("memory_modified");
    saveMemories();
    return;
  }
  if (metabolism.action === "CRYSTALLIZE" && metabolism.entity) {
    try {
      require("./person-model.ts").crystallizeTraits?.();
    } catch {
    }
  }
  try {
    const { trigrams: trigrams3, trigramSimilarity: trigramSimilarity3 } = require("./memory-utils.ts");
    const newTri = trigrams3(content);
    for (const existing of memoryState.memories) {
      if (!existing.content || existing.scope === "expired") continue;
      const sim = trigramSimilarity3(newTri, trigrams3(existing.content));
      if (sim > 0.7) {
        if (content.length > existing.content.length) existing.content = content;
        existing.ts = Date.now();
        existing.lastAccessed = Date.now();
        existing.confidence = Math.min(1, (existing.confidence ?? 0.7) + 0.05);
        try {
          appendLineage(existing, { action: "dedup_merged", ts: Date.now(), delta: `merged similar: ${content.slice(0, 30)}` });
        } catch {
        }
        syncToSQLite(existing, { content: existing.content, ts: existing.ts, confidence: existing.confidence });
        updateRecallIndex(existing);
        console.log(`[cc-soul][memory-crud] dedup: merged into existing (sim=${sim.toFixed(2)}): ${content.slice(0, 40)}`);
        return;
      }
    }
  } catch {
  }
  if (useSQLite) {
    try {
      sqliteAddMemory(newMem);
    } catch (e) {
      console.error(`[cc-soul][memory-crud] SQLite write failed, skipping memory: ${e.message}`);
      return;
    }
  }
  memoryState.memories.push(newMem);
  updateRecallIndex(newMem);
  emitCacheEvent("memory_added");
  if (_supersededMemId && newMem.memoryId) {
    newMem.supersedes = _supersededMemId;
    const oldMem = memoryState.memories.find((m) => m.memoryId === _supersededMemId);
    if (oldMem) oldMem.supersededBy = newMem.memoryId;
    emitCacheEvent("identity_changed");
  }
  try {
    try {
      autoLinkMemories(newMem);
    } catch {
    }
    if (!skipAutoExtract) {
      try {
        autoExtractFromMemory(content, scope, autoSource);
      } catch {
      }
    }
    const _AAM_LEARN_SCOPES = /* @__PURE__ */ new Set(["preference", "fact", "event", "correction", "topic", "episode", "opinion"]);
    if (_AAM_LEARN_SCOPES.has(scope)) {
      try {
        import("./aam.ts").then((m) => m.learnAssociation(content, autoEmotionIntensity)).catch(() => {
        });
      } catch {
      }
    }
    if (scope === "correction") {
      try {
        const { getRecentTrace } = require("./activation-field.ts");
        const trace = getRecentTrace?.();
        const recentMem = trace?.traces?.[0]?.memory?.content;
        if (recentMem) {
          const recalledKw = (recentMem.match(/[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}/gi) || []).slice(0, 5);
          const correctKw = (content.match(/[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}/gi) || []).slice(0, 5);
          if (recalledKw.length > 0 && correctKw.length > 0) {
            import("./aam.ts").then((m) => m.learnAssociation(recalledKw.join(" ") + " " + correctKw.join(" "), 1)).catch(() => {
            });
          }
        }
      } catch {
      }
    }
    try {
      const CONFLICT_PAIRS = [
        [/喜欢|偏好|爱|like|love|prefer|enjoy/, /讨厌|不喜欢|不想|放弃|hate|dislike|don't like|quit|gave up/i],
        [/在.*工作|在.*上班|work at|working at|employed/, /离职|辞职|被裁|不干了|quit|fired|laid off|left the job|resigned/i],
        [/住在|住|live in|living in|reside/, /搬到|搬去|搬家|moved to|relocat|moving to/i],
        [/运动|跑步|健身|exercise|running|workout|gym/, /不运动|放弃运动|不跑了|stopped exercising|quit gym|no longer run/i],
        [/学|在学|studying|learning|taking a course/, /不学了|放弃了|学不动|stopped studying|dropped out|gave up learning/i]
      ];
      for (const [patternA, patternB] of CONFLICT_PAIRS) {
        const newMatchesB = patternB.test(content);
        if (!newMatchesB) continue;
        for (const existing of memoryState.memories) {
          if (existing.scope === "expired" || existing.scope === "decayed") continue;
          if (!patternA.test(existing.content)) continue;
          const existingWords = new Set((existing.content.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map((w) => w.toLowerCase()));
          const newWords = (content.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map((w) => w.toLowerCase());
          const overlap = newWords.filter((w) => existingWords.has(w)).length;
          if (overlap >= 1) {
            console.log(`[cc-soul][conflict] "${content.slice(0, 30)}" contradicts "${existing.content.slice(0, 30)}"`);
            existing.confidence = Math.max(0.1, (existing.confidence ?? 0.7) * 0.5);
            existing.scope = "expired";
            break;
          }
        }
      }
    } catch {
    }
    if (FACT_SCOPES.includes(scope)) {
      suppressSimilarMemories(newMem);
    }
    markComplementCandidates(newMem, memoryState.memories);
    if (memoryState.memories.length > MAX_MEMORIES) {
      const evictionScores = memoryState.memories.map((m, idx) => {
        const decay = timeDecay(m);
        const conf = m.confidence ?? 0.7;
        const emotionBoost = m.emotion === "important" ? 2 : m.emotion === "painful" ? 1.5 : 1;
        const scopeBoost = m.scope === "correction" || m.scope === "reflexion" || m.scope === "consolidated" ? 1.5 : 1;
        const tagBoost = m.tags && m.tags.length > 5 ? 1.3 : 1;
        const score = decay * conf * emotionBoost * scopeBoost * tagBoost;
        return { idx, score, scope: m.scope };
      });
      const scores = evictionScores.map((e) => e.score).sort((a, b) => a - b);
      const median = scores[Math.floor(scores.length / 2)] || 0.5;
      const evictionThreshold = median * 0.3;
      const scopeCounts = /* @__PURE__ */ new Map();
      for (const m of memoryState.memories) {
        scopeCounts.set(m.scope, (scopeCounts.get(m.scope) || 0) + 1);
      }
      const toEvict = /* @__PURE__ */ new Set();
      evictionScores.sort((a, b) => a.score - b.score);
      for (const e of evictionScores) {
        if (e.score >= evictionThreshold) break;
        const remaining = Math.max(0, (scopeCounts.get(e.scope) || 0) - [...toEvict].filter((i) => memoryState.memories[i]?.scope === e.scope).length);
        if (remaining <= 2) continue;
        toEvict.add(e.idx);
      }
      if (toEvict.size > 0) {
        const filtered = memoryState.memories.filter((_, i) => !toEvict.has(i));
        memoryState.memories.length = 0;
        memoryState.memories.push(...filtered);
        rebuildScopeIndex();
        rebuildRecallIndex(memoryState.memories);
      }
    } else {
      const arr = scopeIndex.get(scope) || [];
      arr.push(memoryState.memories[memoryState.memories.length - 1]);
      scopeIndex.set(scope, arr);
      const ck = content.slice(0, 50).toLowerCase();
      contentIndex.set(ck, content);
    }
    incrementalIDFUpdate(content);
    invalidateFieldIDF();
    if (content.length > 10) {
      const lastIdx = memoryState.memories.length - 1;
      if (lastIdx >= 0 && memoryState.memories[lastIdx].content === content && !memoryState.memories[lastIdx].tags) {
        queueForTagging(content, memoryState.memories[lastIdx].ts);
      }
    }
    try {
      const newIdx = memoryState.memories.length - 1;
      const newMem2 = memoryState.memories[newIdx];
      if (newMem2 && newMem2.content.length >= 15) {
        const newTri = trigrams(newMem2.content);
        const searchStart = Math.max(0, newIdx - 10);
        let bestSim = 0, bestIdx = -1;
        for (let i = searchStart; i < newIdx; i++) {
          const other = memoryState.memories[i];
          if (!other || other.scope === "expired" || other.scope === "historical") continue;
          if (Math.abs((newMem2.ts || 0) - (other.ts || 0)) > 3e5) continue;
          const sim = trigramSimilarity(newTri, trigrams(other.content));
          if (sim > bestSim) {
            bestSim = sim;
            bestIdx = i;
          }
        }
        if (bestSim > 0.4 && bestIdx >= 0) {
          const target = memoryState.memories[bestIdx];
          if (target.content.length >= newMem2.content.length) {
            target.content = target.content + " " + newMem2.content;
          } else {
            target.content = newMem2.content + " " + target.content;
          }
          target.confidence = Math.max(target.confidence || 0.7, newMem2.confidence || 0.7);
          target.recallCount = (target.recallCount || 0) + (newMem2.recallCount || 0);
          newMem2.scope = "expired";
          newMem2.content = `[merged\u2192${bestIdx}]`;
          console.log(`[cc-soul][micro-distill] merged memory #${newIdx} into #${bestIdx} (sim=${bestSim.toFixed(2)})`);
        }
      }
    } catch {
    }
  } finally {
    saveMemories();
  }
}
function addMemoryWithEmotion(content, scope, userId, visibility, channelId, emotion, skipAutoExtract) {
  addMemory(content, scope, userId, visibility, channelId, void 0, skipAutoExtract);
  const found = memoryState.memories.some((m) => m.content === content);
  if (!found) return;
  const target = memoryState.memories.length > 0 ? memoryState.memories.reduce(
    (best, m) => m.content === content && m.ts >= (best?.ts ?? 0) ? m : best,
    void 0
  ) : void 0;
  if (!target) return;
  if (emotion) {
    const validEmotions = ["neutral", "warm", "important", "painful", "funny"];
    const matched = validEmotions.find((e) => emotion.includes(e)) || "neutral";
    target.emotion = matched;
    if (!target.situationCtx) target.situationCtx = {};
    target.situationCtx.mood = matched === "warm" ? 0.5 : matched === "painful" ? -0.5 : 0;
    saveMemories();
  } else if (content.length > 20) {
    try {
      const sigMod = getLazyModule("signals");
      const detectEmotionLabel = sigMod?.detectEmotionLabel;
      const emotionLabelToLegacy = sigMod?.emotionLabelToLegacy;
      const detected = detectEmotionLabel(content);
      if (detected.confidence > 0.4) {
        target.emotion = emotionLabelToLegacy(detected.label);
        target.emotionLabel = detected.label;
        const emotionLabelToPADCN = sigMod?.emotionLabelToPADCN;
        if (emotionLabelToPADCN) {
          const padcn = emotionLabelToPADCN(detected.label);
          if (!target.situationCtx) target.situationCtx = {};
          target.situationCtx.mood = padcn.pleasure;
          target.situationCtx.energy = (padcn.arousal + 1) / 2;
        }
        saveMemories();
      }
    } catch {
    }
  }
}
export {
  INJECT_HISTORY2 as INJECT_HISTORY,
  MAX_HISTORY2 as MAX_HISTORY,
  MAX_MEMORIES2 as MAX_MEMORIES,
  SYNONYM_MAP,
  _memoriesLoaded,
  _recentWriteHashes,
  addMemory,
  addMemoryWithEmotion,
  addToHistory,
  addWorkingMemory,
  archiveWorkingMemory,
  auditMemoryHealth,
  autoPromoteToCoreMemory,
  batchTagUntaggedMemories,
  bayesBoost,
  bayesConfidence,
  bayesCorrect,
  bayesPenalize,
  buildCoreMemoryContext,
  buildEpisodeContext,
  buildHistoryContext,
  buildWorkingMemoryContext,
  cleanupNetworkKnowledge,
  cleanupWorkingMemory,
  compressMemory2 as compressMemory,
  compressOldMemories,
  consolidateMemories,
  coreMemories,
  createMemoryVersion,
  decideMemoryAction,
  defaultVisibility2 as defaultVisibility,
  degradeMemoryConfidence,
  detectMemoryPoisoning2 as detectMemoryPoisoning,
  ensureMemoriesLoaded,
  ensureSQLiteReady,
  episodes,
  evaluateAndPromoteMemories,
  executeMemoryCommands,
  extractReasoning2 as extractReasoning,
  extractTagsLocal,
  generateInsights,
  generatePrediction,
  getAssociativeRecall,
  getCachedFusedRecall,
  getCurrentSegmentId,
  getLazyModule,
  getMemoriesByScope,
  getPendingSearchResults,
  getRecallImpactBoost,
  getRecallRate,
  getStorageStatus,
  incrementSegment,
  incrementalIDFUpdate2 as incrementalIDFUpdate,
  invalidateIDF2 as invalidateIDF,
  loadCoreMemories,
  loadEpisodes,
  loadMemories,
  memoryState,
  parseMemoryCommands,
  predictiveRecall,
  processMemoryDecay,
  promoteToCore,
  pruneExpiredMemories,
  queryMemoryTimeline,
  rebuildRecallIndex2 as rebuildRecallIndex,
  rebuildScopeIndex,
  recall,
  recallEpisodes,
  recallFeedbackLoop,
  recallImpact,
  recallStats,
  recallWithScores,
  recordEpisode,
  resolveNetworkConflicts,
  restoreArchivedMemories,
  reviveDecayedMemories,
  saveMemories,
  scanForContradictions,
  scopeIndex,
  shuffleArray,
  sqliteMaintenance,
  syncToSQLite,
  trackRecallImpact,
  triggerAssociativeRecall,
  triggerSessionSummary,
  trigramSimilarity2 as trigramSimilarity,
  trigrams2 as trigrams,
  updateMemory,
  updateRecallIndex2 as updateRecallIndex,
  useSQLite
};
