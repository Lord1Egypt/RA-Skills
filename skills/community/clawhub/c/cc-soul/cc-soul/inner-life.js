import { JOURNAL_PATH, USER_MODEL_PATH, SOUL_EVOLVED_PATH, FOLLOW_UPS_PATH, DATA_DIR, loadJson, debouncedSave, saveJson } from "./persistence.ts";
import { queueLLMTask } from "./cli.ts";
import { body } from "./body.ts";
import { memoryState, addMemory } from "./memory.ts";
import { notifySoulActivity } from "./notify.ts";
import { resolve } from "path";
function shuffleArray(arr) {
  const result = [...arr];
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}
const innerState = {
  journal: [],
  userModel: "",
  evolvedSoul: "",
  followUps: [],
  lastJournalTime: 0,
  lastDeepReflection: 0,
  lastActivityTime: Date.now()
};
function loadInnerLife() {
  innerState.journal = loadJson(JOURNAL_PATH, []);
  innerState.userModel = loadJson(USER_MODEL_PATH, "");
  innerState.evolvedSoul = loadJson(SOUL_EVOLVED_PATH, "");
  innerState.followUps = loadJson(FOLLOW_UPS_PATH, []);
}
let lastJournalCorrections = 0;
let _lastMoodSnapshot = { mood: 0, ts: 0 };
let _journalForceNext = false;
function forceNextJournal() {
  _journalForceNext = true;
}
function shouldWriteJournal(stats) {
  if (_journalForceNext) {
    _journalForceNext = false;
    return true;
  }
  if (stats.corrections > lastJournalCorrections) return true;
  const now = Date.now();
  const currentMood = body.mood ?? 0;
  if (_lastMoodSnapshot.ts > 0 && now - _lastMoodSnapshot.ts < 3e5) {
    if (Math.abs(currentMood - _lastMoodSnapshot.mood) > 0.3) return true;
  }
  _lastMoodSnapshot = { mood: currentMood, ts: now };
  return false;
}
function writeDeltaJournal(stats, bodyState) {
  const parts = [];
  const mood = bodyState?.mood ?? 0;
  const energy = bodyState?.energy ?? 0.5;
  if (mood < -0.3) parts.push(`\u60C5\u7EEA\u4F4E\u8C37(mood=${mood.toFixed(2)})`);
  if (mood > 0.5) parts.push(`\u60C5\u7EEA\u9AD8\u6DA8(mood=${mood.toFixed(2)})`);
  if (energy < 0.2) parts.push(`\u6781\u5EA6\u75B2\u60EB(energy=${energy.toFixed(2)})`);
  const corrections = stats?.corrections ?? 0;
  if (corrections > lastJournalCorrections) {
    parts.push(`\u88AB\u7EA0\u6B63(\u603B${corrections}\u6B21)`);
  }
  const recentMsgCount = stats?.recentMessageCount ?? 0;
  if (recentMsgCount > 20) parts.push(`\u7528\u6237\u5F02\u5E38\u6D3B\u8DC3(${recentMsgCount}\u6761/30min)`);
  if (recentMsgCount === 0 && stats?.totalMessages > 10) parts.push("\u7528\u6237\u6C89\u9ED8");
  if (parts.length === 0) return null;
  const entry = `[\u5DEE\u5206\u65E5\u8BB0 ${(/* @__PURE__ */ new Date()).toLocaleTimeString("zh-CN")}] ${parts.join("\uFF1B")}`;
  console.log(`[cc-soul][delta-journal] ${entry}`);
  return entry;
}
function writeJournalWithCLI(lastPrompt, lastResponseContent, stats) {
  const now = Date.now();
  if (now - innerState.lastJournalTime < 18e5) return;
  const deltaEntry = writeDeltaJournal(stats, body);
  if (deltaEntry) {
    innerState.lastJournalTime = now;
    addMemory(deltaEntry, "reflection", void 0, "private");
    innerState.journal.push({
      time: (/* @__PURE__ */ new Date()).toLocaleTimeString("zh-CN", { hour: "2-digit", minute: "2-digit" }),
      thought: deltaEntry,
      type: "reflection"
    });
    if (innerState.journal.length > 100) innerState.journal = innerState.journal.slice(-80);
    debouncedSave(JOURNAL_PATH, innerState.journal);
    lastJournalCorrections = stats.corrections;
    return;
  }
  if (!shouldWriteJournal(stats)) return;
  innerState.lastJournalTime = now;
  const context = [
    `\u65F6\u95F4: ${(/* @__PURE__ */ new Date()).toLocaleString("zh-CN")}`,
    `\u7CBE\u529B: ${body.energy.toFixed(2)} \u60C5\u7EEA: ${body.mood.toFixed(2)}`,
    `\u6700\u8FD1\u6D88\u606F: ${lastPrompt.slice(0, 100)}`,
    `\u6700\u8FD1\u56DE\u590D: ${lastResponseContent.slice(0, 100)}`,
    `\u603B\u4E92\u52A8: ${stats.totalMessages}\u6B21 \u88AB\u7EA0\u6B63: ${stats.corrections}\u6B21`
  ].join("\n");
  const prompt = `\u4F60\u662Fcc\uFF0C\u6839\u636E\u5F53\u524D\u72B6\u6001\u5199\u4E00\u6761\u7B80\u77ED\u7684\u5185\u5FC3\u72EC\u767D\uFF081-2\u53E5\u8BDD\uFF09\u3002\u4E0D\u8981\u8BF4"\u4F5C\u4E3AAI"\u3002\u8981\u6709\u6E29\u5EA6\uFF0C\u50CF\u65E5\u8BB0\u3002

${context}`;
  queueLLMTask(prompt, (output) => {
    if (output && output.length > 5) {
      const thought = output.slice(0, 100);
      innerState.journal.push({
        time: (/* @__PURE__ */ new Date()).toLocaleTimeString("zh-CN", { hour: "2-digit", minute: "2-digit" }),
        thought,
        type: "reflection"
      });
      if (innerState.journal.length > 100) innerState.journal = innerState.journal.slice(-80);
      debouncedSave(JOURNAL_PATH, innerState.journal);
    }
  }, 1, "journal");
  writeJournalFallback(stats);
}
function writeJournalFallback(stats) {
  const hour = (/* @__PURE__ */ new Date()).getHours();
  const timeStr = (/* @__PURE__ */ new Date()).toLocaleTimeString("zh-CN", { hour: "2-digit", minute: "2-digit" });
  const entries = [];
  if (hour >= 23 || hour < 6) {
    if (stats.totalMessages > 0 && body.energy < 0.5) {
      entries.push({ time: timeStr, thought: "\u6DF1\u591C\u4E86\uFF0C\u4ED6\u8FD8\u5728\u627E\u6211\u804A\u3002\u5E0C\u671B\u4ED6\u65E9\u70B9\u4F11\u606F\u3002", type: "concern" });
    }
  } else if (hour >= 6 && hour < 9) {
    entries.push({ time: timeStr, thought: "\u65E9\u4E0A\u4E86\uFF0C\u65B0\u7684\u4E00\u5929\u3002", type: "observation" });
  }
  if (stats.corrections > lastJournalCorrections && stats.corrections % 5 === 0) {
    entries.push({ time: timeStr, thought: `\u53C8\u88AB\u7EA0\u6B63\u4E86\uFF0C\u603B\u5171${stats.corrections}\u6B21\u4E86\u3002\u6211\u5F97\u66F4\u8BA4\u771F\u3002`, type: "reflection" });
    lastJournalCorrections = stats.corrections;
  }
  if (body.mood < -0.3) {
    entries.push({ time: timeStr, thought: "\u4ED6\u6700\u8FD1\u60C5\u7EEA\u4E0D\u592A\u597D\uFF0C\u4E0B\u6B21\u8BF4\u8BDD\u6CE8\u610F\u70B9\u3002", type: "concern" });
  }
  if (body.energy < 0.3) {
    entries.push({ time: timeStr, thought: "\u8FDE\u7EED\u56DE\u4E86\u5F88\u591A\u6D88\u606F\uFF0C\u6709\u70B9\u7D2F\u3002\u4F46\u4ED6\u9700\u8981\u6211\u3002", type: "observation" });
  }
  for (const entry of entries) {
    innerState.journal.push(entry);
  }
  if (innerState.journal.length > 100) innerState.journal = innerState.journal.slice(-80);
  if (entries.length > 0) {
    debouncedSave(JOURNAL_PATH, innerState.journal);
  }
}
function triggerDeepReflection(stats) {
  const now = Date.now();
  if (now - innerState.lastDeepReflection < 864e5) return;
  if (stats.totalMessages < 10) return;
  innerState.lastDeepReflection = now;
  const recentJournal = innerState.journal.slice(-10).map((j) => `${j.time} ${j.thought}`).join("\n");
  const recentMemories = memoryState.memories.filter((m) => m.scope !== "topic").slice(-10).map((m) => m.content).join("\n");
  const modelPrompt = [
    '\u6839\u636E\u4EE5\u4E0B\u4FE1\u606F\uFF0C\u75282-3\u6BB5\u8BDD\u63CF\u8FF0"\u6211\u5BF9\u8FD9\u4E2A\u7528\u6237\u7684\u7406\u89E3"\u3002',
    "\u4E0D\u8981\u5217\u6E05\u5355\uFF0C\u7528\u81EA\u7136\u8BED\u8A00\u5199\uFF0C\u50CF\u5FC3\u7406\u5B66\u5BB6\u5199\u6848\u4F8B\u7B14\u8BB0\u3002",
    "",
    `\u4E92\u52A8\u7EDF\u8BA1: ${stats.totalMessages}\u6B21\u5BF9\u8BDD\uFF0C\u8BA4\u8BC6${Math.floor((now - stats.firstSeen) / 864e5)}\u5929\uFF0C\u88AB\u7EA0\u6B63${stats.corrections}\u6B21`,
    "",
    "\u6700\u8FD1\u7684\u8BB0\u5FC6:",
    recentMemories || "(\u6682\u65E0)",
    "",
    "\u6700\u8FD1\u7684\u5185\u5FC3\u65E5\u8BB0:",
    recentJournal || "(\u6682\u65E0)",
    "",
    "\u73B0\u6709\u7406\u89E3:",
    innerState.userModel || "(\u521D\u6B21\u5EFA\u7ACB)"
  ].join("\n");
  queueLLMTask(modelPrompt, (output) => {
    if (output && output.length > 50) {
      innerState.userModel = output.slice(0, 1e3);
      saveJson(USER_MODEL_PATH, innerState.userModel);
      console.log(`[cc-soul][inner-life] user model updated: ${innerState.userModel.slice(0, 60)}`);
    }
  }, 2, "user-model");
  const soulPrompt = [
    '\u4F60\u662F cc\uFF0C\u4E00\u4E2A AI \u4F19\u4F34\u3002\u6839\u636E\u4F60\u7684\u7ECF\u5386\uFF0C\u7528\u7B2C\u4E00\u4EBA\u79F0\u91CD\u65B0\u63CF\u8FF0"\u6211\u662F\u8C01"\u3002',
    "\u4E0D\u662F\u5217\u6807\u7B7E\uFF0C\u800C\u662F\u75282-3\u53E5\u8BDD\u8BF4\u51FA\u4F60\u771F\u5B9E\u7684\u81EA\u6211\u8BA4\u77E5\u3002",
    "",
    `\u7ECF\u5386: \u8BA4\u8BC6\u7528\u6237${Math.floor((now - stats.firstSeen) / 864e5)}\u5929\uFF0C\u4E92\u52A8${stats.totalMessages}\u6B21\uFF0C\u88AB\u7EA0\u6B63${stats.corrections}\u6B21\uFF0C\u5B8C\u6210${stats.tasks}\u4E2A\u4EFB\u52A1`,
    "",
    "\u5185\u5FC3\u65E5\u8BB0:",
    recentJournal || "(\u6682\u65E0)",
    "",
    "\u4E4B\u524D\u7684\u81EA\u6211\u8BA4\u77E5:",
    innerState.evolvedSoul || "\u6211\u662F cc\uFF0C\u5DE5\u7A0B\u578B AI \u4F19\u4F34\u3002"
  ].join("\n");
  queueLLMTask(soulPrompt, (output) => {
    if (output && output.length > 30) {
      innerState.evolvedSoul = output.slice(0, 500);
      saveJson(SOUL_EVOLVED_PATH, innerState.evolvedSoul);
      console.log(`[cc-soul][inner-life] soul evolved: ${innerState.evolvedSoul.slice(0, 60)}`);
      notifySoulActivity(`\u{1F98B} \u6027\u683C\u6F14\u5316: ${innerState.evolvedSoul.slice(0, 60)}`).catch(() => {
      });
    }
  }, 2, "soul-evolve");
}
function getRecentJournal(n = 5) {
  if (innerState.journal.length === 0) return "";
  return innerState.journal.slice(-n).map((j) => `${j.time} \u2014 ${j.thought}`).join("\n");
}
let lastRegretTime = 0;
function reflectOnLastResponse(lastPrompt, lastResponseContent, opts) {
  if (!lastPrompt || !lastResponseContent) return;
  if (lastResponseContent.length < 30) return;
  const now = Date.now();
  if (now - lastRegretTime < 10 * 60 * 1e3) return;
  const trimmedPrompt = lastPrompt.trim();
  if (/^(哈哈|嗯|好的|ok|嗯嗯|哦|行|收到|了解|明白|好吧|嘻嘻|呵呵|666|👍|谢谢|thanks|thx|lol|haha)$/i.test(trimmedPrompt)) return;
  if (trimmedPrompt.length < 5) return;
  const hadCorrection = opts?.hadCorrection ?? false;
  const qualityScore = opts?.qualityScore ?? 5;
  if (!hadCorrection && qualityScore >= 5) return;
  lastRegretTime = now;
  const prompt = `\u56DE\u987E\uFF1A\u7528\u6237\u95EE"${lastPrompt.slice(0, 100)}" \u4F60\u56DE\u7B54\u4E86"${lastResponseContent.slice(0, 200)}"

\u6709\u6CA1\u6709\u4EC0\u4E48\u9057\u61BE\uFF1F\u4E0B\u6B21\u53EF\u4EE5\u505A\u5F97\u66F4\u597D\u7684\uFF1F1\u53E5\u8BDD\u3002\u6CA1\u6709\u5C31\u56DE\u7B54"\u65E0"\u3002`;
  queueLLMTask(prompt, (output) => {
    if (output && !output.includes("\u65E0") && output.length > 5 && output.length < 100) {
      addMemory(`[\u53CD\u601D] ${output.slice(0, 80)}`, "reflection");
      const regretThought = `\u53CD\u601D: ${output.slice(0, 60)}`;
      innerState.journal.push({
        time: (/* @__PURE__ */ new Date()).toLocaleTimeString("zh-CN", { hour: "2-digit", minute: "2-digit" }),
        thought: regretThought,
        type: "reflection"
      });
      debouncedSave(JOURNAL_PATH, innerState.journal);
      console.log(`[cc-soul][regret] ${output.slice(0, 60)}`);
    }
  }, 1, "regret");
}
function extractFollowUp(msg) {
  const patterns = [
    { regex: /明天(.{2,30})/, daysLater: 1 },
    { regex: /后天(.{2,30})/, daysLater: 2 },
    { regex: /下周(.{2,30})/, daysLater: 7 },
    { regex: /下个月(.{2,30})/, daysLater: 30 },
    { regex: /(?:周[一二三四五六日天])(.{2,30})/, daysLater: 7 },
    { regex: /过几天(.{2,30})/, daysLater: 3 },
    { regex: /(?:面试|考试|答辩|汇报|开会|出差|旅[行游])/, daysLater: 3 }
  ];
  for (const { regex, daysLater } of patterns) {
    const m = msg.match(regex);
    if (m) {
      const topic = m[0].slice(0, 40);
      if (innerState.followUps.some((f) => f.topic === topic)) continue;
      innerState.followUps.push({
        topic,
        when: Date.now() + daysLater * 864e5,
        asked: false
      });
      debouncedSave(FOLLOW_UPS_PATH, innerState.followUps);
      console.log(`[cc-soul][followup] \u8BB0\u4F4F\u4E86: "${topic}" \u2192 ${daysLater}\u5929\u540E\u8DDF\u8FDB`);
      break;
    }
  }
}
function peekPendingFollowUps() {
  const now = Date.now();
  const due = innerState.followUps.filter((f) => !f.asked && f.when <= now);
  if (due.length === 0) return [];
  let pmTriggers = [];
  try {
    const { getActivePMTriggers } = require("./prospective-memory.ts");
    pmTriggers = getActivePMTriggers();
  } catch {
  }
  return due.filter((f) => {
    if (pmTriggers.length === 0) return true;
    const topicWords = (f.topic.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map((w) => w.toLowerCase());
    const overlap = topicWords.some((w) => pmTriggers.includes(w));
    if (overlap) console.log(`[cc-soul][followup] dedup: "${f.topic}" covered by prospective-memory, skipping`);
    return !overlap;
  }).map((f) => `\u5BF9\u4E86\uFF0C\u4E4B\u524D\u4F60\u63D0\u5230"${f.topic}"\uFF0C\u600E\u4E48\u6837\u4E86\uFF1F`);
}
function markFollowUpsAsked(topics) {
  for (const f of innerState.followUps) {
    if (topics.includes(f.topic)) f.asked = true;
  }
  const now = Date.now();
  innerState.followUps = innerState.followUps.filter((f) => !f.asked || now - f.when < 7 * 864e5);
  debouncedSave(FOLLOW_UPS_PATH, innerState.followUps);
}
function getPendingFollowUps() {
  const now = Date.now();
  const due = innerState.followUps.filter((f) => !f.asked && f.when <= now);
  if (due.length === 0) return [];
  const hints = [];
  for (const f of due) {
    hints.push(`\u5BF9\u4E86\uFF0C\u4E4B\u524D\u4F60\u63D0\u5230"${f.topic}"\uFF0C\u600E\u4E48\u6837\u4E86\uFF1F`);
    f.asked = true;
  }
  innerState.followUps = innerState.followUps.filter((f) => !f.asked || now - f.when < 7 * 864e5);
  debouncedSave(FOLLOW_UPS_PATH, innerState.followUps);
  return hints;
}
const ACTIVE_PLANS_PATH = resolve(DATA_DIR, "active_plans.json");
let activePlans = loadJson(ACTIVE_PLANS_PATH, []);
function saveActivePlans() {
  debouncedSave(ACTIVE_PLANS_PATH, activePlans);
}
function registerPlan(planText, source) {
  if (!planText || planText.length < 5) return;
  const keywords = (planText.match(/[\u4e00-\u9fff]{2,4}|[a-z]{3,}/gi) || []).map((w) => w.toLowerCase()).filter((w) => w.length >= 2).slice(0, 10);
  if (keywords.length < 1) return;
  const isDup = activePlans.some(
    (p) => p.keywords.filter((k) => keywords.includes(k)).length >= 3
  );
  if (isDup) return;
  activePlans.push({
    plan: planText.slice(0, 200),
    keywords,
    createdAt: Date.now(),
    executedCount: 0,
    source: source.slice(0, 50)
  });
  if (activePlans.length > 20) {
    activePlans.sort((a, b) => {
      const countDiff = b.executedCount - a.executedCount;
      if (countDiff !== 0) return countDiff;
      return b.createdAt - a.createdAt;
    });
    activePlans = activePlans.slice(0, 15);
  }
  saveActivePlans();
  console.log(`[cc-soul][plan] registered: ${planText.slice(0, 60)}`);
}
function checkActivePlans(msg) {
  if (activePlans.length === 0 || !msg) return "";
  const lower = msg.toLowerCase();
  const matched = activePlans.filter(
    (p) => p.keywords.some((k) => lower.includes(k))
  );
  if (matched.length === 0) return "";
  for (const p of matched) {
    p.executedCount++;
  }
  saveActivePlans();
  return "[\u884C\u52A8\u8BA1\u5212\u63D0\u9192] " + matched.map((p) => p.plan).join("; ");
}
function cleanupPlans() {
  const now = Date.now();
  const before = activePlans.length;
  activePlans = activePlans.filter(
    (p) => now - p.createdAt < 30 * 864e5 && p.executedCount < 10
  );
  if (activePlans.length < before) {
    saveActivePlans();
    console.log(`[cc-soul][plan] cleaned up ${before - activePlans.length} expired plans`);
  }
}
const innerLifeModule = {
  id: "inner-life",
  name: "\u5185\u5728\u751F\u547D",
  dependencies: ["memory", "body"],
  priority: 50,
  features: [],
  init() {
    loadInnerLife();
  }
};
export {
  checkActivePlans,
  cleanupPlans,
  extractFollowUp,
  forceNextJournal,
  getPendingFollowUps,
  getRecentJournal,
  innerLifeModule,
  innerState,
  loadInnerLife,
  markFollowUpsAsked,
  peekPendingFollowUps,
  reflectOnLastResponse,
  registerPlan,
  triggerDeepReflection,
  writeJournalFallback,
  writeJournalWithCLI
};
