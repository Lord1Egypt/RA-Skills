import { existsSync, readFileSync, readdirSync, mkdirSync } from "fs";
import { execFile } from "child_process";
import { platform, homedir } from "os";
import { resolve } from "path";
import {
  metrics,
  stats,
  saveStats,
  metricsRecordResponseTime,
  getSessionState,
  setLastActiveSessionKey,
  getLastActiveSessionKey,
  getPrivacyMode,
  getReadAloudPending,
  setReadAloudPending,
  CJK_TOPIC_REGEX,
  CJK_WORD_REGEX,
  refreshNarrativeAsync,
  detectTopicShiftAndReset
} from "./handler-state.ts";
import { routeCommand } from "./handler-commands.ts";
import { buildAndSelectAugments } from "./handler-augments.ts";
import { brain } from "./brain.ts";
import {
  loadJson,
  saveJson,
  debouncedSave,
  flushAll,
  DATA_DIR
} from "./persistence.ts";
import { runPostResponseAnalysis, setAgentBusy, killGatewayClaude } from "./cli.ts";
import { notifyOwnerDM } from "./notify.ts";
import { body, bodyTick, bodyOnMessage, bodyOnPositiveFeedback, processEmotionalContagion, trackEmotionAnchor } from "./body.ts";
import {
  memoryState,
  addMemory,
  addMemoryWithEmotion,
  addToHistory,
  buildHistoryContext,
  recallFeedbackLoop,
  triggerSessionSummary,
  triggerAssociativeRecall,
  parseMemoryCommands,
  executeMemoryCommands,
  generatePrediction,
  recordEpisode,
  addWorkingMemory,
  trackRecallImpact
} from "./memory.ts";
import { graphState, addEntitiesFromAnalysis } from "./graph.ts";
import { cogProcess, predictIntent, detectAtmosphere } from "./cognition.ts";
import {
  rules,
  onCorrectionAdvanced,
  verifyHypothesis,
  attributeCorrection,
  recordRuleQuality
} from "./evolution.ts";
import {
  scoreResponse,
  selfCheckSync,
  trackQuality,
  computeEval,
  getEvalSummary
} from "./quality.ts";
import {
  innerState,
  writeJournalWithCLI,
  triggerDeepReflection,
  extractFollowUp,
  peekPendingFollowUps
} from "./inner-life.ts";
let trackPersonaStyle = () => {
};
let getPersonaDriftWarning = () => null;
let checkPersonaDrift = () => 0;
let getPersonaDriftReinforcement = () => null;
let getDriftCount = () => 0;
let smartForgetSweep = () => ({ toForget: [], toConsolidate: [] });
let compressAugments = (a) => a;
let buildDebateAugment = () => null;
let updateBeliefFromMessage = () => {
};
let getToMContext = () => "";
let detectMisconception = () => null;
let recordTurnUsage = () => {
};
import("./cost-tracker.ts").then((m) => {
  recordTurnUsage = m.recordTurnUsage;
}).catch((e) => {
  console.error(`[cc-soul] module load failed (cost-tracker): ${e.message}`);
});
import("./persona-drift.ts").then((m) => {
  trackPersonaStyle = m.trackPersonaStyle;
  getPersonaDriftWarning = m.getPersonaDriftWarning;
  checkPersonaDrift = m.checkPersonaDrift;
  getPersonaDriftReinforcement = m.getPersonaDriftReinforcement;
  getDriftCount = m.getDriftCount;
}).catch((e) => {
  console.error(`[cc-soul] module load failed (persona-drift): ${e.message}`);
});
import("./smart-forget.ts").then((m) => {
  smartForgetSweep = m.smartForgetSweep;
}).catch((e) => {
  console.error(`[cc-soul] module load failed (smart-forget): ${e.message}`);
});
import("./context-compress.ts").then((m) => {
  compressAugments = m.compressAugments;
}).catch((e) => {
  console.error(`[cc-soul] module load failed (context-compress): ${e.message}`);
});
import("./person-model.ts").then((m) => {
  updateBeliefFromMessage = m.updateBeliefFromMessage;
  getToMContext = m.getToMContext;
  detectMisconception = m.detectMisconception;
}).catch((e) => {
  console.error(`[cc-soul] module load failed (person-model/tom): ${e.message}`);
});
import { buildSoulPrompt, estimateTokens } from "./prompt-builder.ts";
import {
  taskState,
  detectAndDelegateTask,
  trackRequestPattern,
  detectWorkflowOpportunity,
  autoExtractSkill
} from "./tasks.ts";
import { updateProfileOnMessage, updateProfileOnCorrection, updateRelationship, trackGratitude, trackPersonaUsage } from "./user-profiles.ts";
import { trackDomainQuality, trackDomainCorrection } from "./epistemic.ts";
import { updateFlow, checkAllSessionEnds, generateSessionSummary } from "./flow.ts";
import { detectValueSignals } from "./values.ts";
import { selectPersona, getActivePersona, updateUserStylePreference } from "./persona.ts";
import { learnConflict, recordInteraction } from "./metacognition.ts";
import { isEnabled } from "./features.ts";
const handleDashboardCommand = () => "\u8BE5\u529F\u80FD\u5DF2\u505C\u7528";
const generateMemoryMapHTML = () => "";
const generateDashboardHTML = () => "";
import { collectAvatarData } from "./avatar.ts";
import { recordModuleError, recordModuleActivity, postReplyCleanup } from "./health.ts";
import { updateBanditReward } from "./auto-tune.ts";
import { isContextEngineActive, setLastAugments } from "./context-engine.ts";
let agentBusyTimer = null;
import { initializeSoul as initializeSoul2, getInitialized as getInitialized2, setInitialized } from "./init.ts";
function handleBootstrap(event) {
  if (!getInitialized()) initializeSoul();
  const ctx = event.context || {};
  const files = ctx.bootstrapFiles;
  if (files) {
    const soulPrompt = buildSoulPrompt(
      stats.totalMessages,
      stats.corrections,
      stats.firstSeen,
      taskState.workflows
    );
    files.push({ path: "CC_SOUL.md", content: soulPrompt });
    console.log(`[cc-soul] bootstrap: injected soul (e=${body.energy.toFixed(2)}, m=${body.mood.toFixed(2)}, prompt=${soulPrompt.length} chars, ~${Math.round(soulPrompt.length * 0.4)} tokens)`);
  }
}
let _lastPreprocessedId = "";
let _lastPreprocessedTs = 0;
const _RECENT_REPLIES_PATH = resolve(DATA_DIR, "recent_replies.json");
let _recentRepliesObj = loadJson(_RECENT_REPLIES_PATH, {});
for (const [k, v] of Object.entries(_recentRepliesObj)) {
  if (Date.now() - v.ts > 36e5) delete _recentRepliesObj[k];
}
const _recentReplies = {
  get(key) {
    return _recentRepliesObj[key];
  },
  set(key, val) {
    _recentRepliesObj[key] = val;
    debouncedSave(_RECENT_REPLIES_PATH, _recentRepliesObj);
  },
  delete(key) {
    delete _recentRepliesObj[key];
  },
  [Symbol.iterator]: function* () {
    for (const [k, v] of Object.entries(_recentRepliesObj)) yield [k, v];
  }
};
async function handlePreprocessed(event) {
  if (!getInitialized()) initializeSoul();
  const eventId = event?.context?.messageId || event?.messageId || "";
  const now = Date.now();
  if (eventId && eventId === _lastPreprocessedId && now - _lastPreprocessedTs < 5e3) {
    return;
  }
  if (eventId) {
    _lastPreprocessedId = eventId;
    _lastPreprocessedTs = now;
  }
  {
    const ctx0 = event.context || {};
    const raw0 = ctx0.body || "";
    const msg0 = raw0.replace(/^\[message_id:\s*\S+\]\s*/i, "").replace(/^[a-zA-Z0-9_\u4e00-\u9fff]{1,20}:\s*/, "").trim();
    if (!msg0) return;
    if (/^[\[(（]?(对话历史|当前面向|认知|相关记忆|Working Memory|内部矛盾|隐私模式|Goal|Intent|用户档案|情绪|举一反三|回答完主问题)/i.test(msg0)) {
      console.log(`[cc-soul][preprocessed] skipped system augment content: ${msg0.slice(0, 40)}...`);
      return;
    }
  }
  killGatewayClaude();
  setAgentBusy(true);
  if (agentBusyTimer) clearTimeout(agentBusyTimer);
  agentBusyTimer = setTimeout(() => {
    agentBusyTimer = null;
    setAgentBusy(false);
    console.log("[cc-soul] agentBusy auto-released (60s safety timeout)");
  }, 6e4);
  const ctx = event.context || {};
  const rawMsg = ctx.bodyForAgent || ctx.body || "";
  const userMsg = rawMsg.replace(/^\[message_id:\s*\S+\]\s*/i, "").replace(/^[a-zA-Z0-9_\u4e00-\u9fff]{1,20}:\s*/, "").trim();
  if (!userMsg) {
    setAgentBusy(false);
    return;
  }
  if (!eventId) {
    const contentKey = userMsg.slice(0, 50);
    if (contentKey === _lastPreprocessedId && now - _lastPreprocessedTs < 3e3) {
      return;
    }
    _lastPreprocessedId = contentKey;
    _lastPreprocessedTs = now;
  }
  setReadAloudPending(userMsg.startsWith("\u6717\u8BFB") || userMsg.toLowerCase().startsWith("read aloud"));
  const _metricsStart = Date.now();
  bodyTick();
  recordModuleActivity("memory");
  recordModuleActivity("cognition");
  recordModuleActivity("prompt-builder");
  const senderId = ctx.senderId || "";
  const channelId = ctx.conversationId || event.sessionKey || "";
  updateProfileOnMessage(senderId, userMsg);
  const sessionKey = event.sessionKey || channelId || senderId || "_default";
  const session = getSessionState(sessionKey);
  setLastActiveSessionKey(sessionKey);
  if (session.lastPrompt && !session.lastResponseContent && Array.isArray(event.messages)) {
    for (let i = event.messages.length - 1; i >= 0; i--) {
      const msg = event.messages[i];
      if (msg?.role === "assistant" && typeof msg?.content === "string" && msg.content.length > 5) {
        session.lastResponseContent = msg.content;
        console.log(`[cc-soul][sync] recovered lastResponse (${msg.content.length} chars)`);
        break;
      }
    }
  }
  const topicShifted = detectTopicShiftAndReset(session, userMsg, sessionKey);
  if (topicShifted) {
    console.log(`[cc-soul][topic-shift] detected for ${sessionKey}, CLI session cleared`);
    {
      try {
        const branchDir = resolve(DATA_DIR, "branches");
        if (!existsSync(branchDir)) mkdirSync(branchDir, { recursive: true });
        const recentMsgs = memoryState.chatHistory.slice(-10);
        if (recentMsgs.length >= 2) {
          const topicWordList = recentMsgs.flatMap((h) => (h.user || "").match(/[\u4e00-\u9fff]{2,4}|[A-Za-z]{3,}/g) || []);
          const freq = /* @__PURE__ */ new Map();
          for (const w of topicWordList) {
            const k = w.toLowerCase();
            freq.set(k, (freq.get(k) || 0) + 1);
          }
          const topicLabel = [...freq.entries()].sort((a, b) => b[1] - a[1])[0]?.[0] || `topic_${Date.now()}`;
          const branchData = {
            topic: topicLabel,
            savedAt: Date.now(),
            autoSaved: true,
            chatHistory: recentMsgs,
            persona: getActivePersona()?.id || "default"
          };
          const branchPath = resolve(branchDir, `${topicLabel}.json`);
          saveJson(branchPath, branchData);
          console.log(`[cc-soul][auto-topic-save] saved topic\u300C${topicLabel}\u300D(${recentMsgs.length} turns) \u2192 ${branchPath}`);
        }
      } catch (e) {
        console.log(`[cc-soul][auto-topic-save] failed: ${e.message}`);
      }
    }
    {
      try {
        const recentHistory = memoryState.chatHistory.slice(-10);
        if (recentHistory.length >= 2) {
          const turns = recentHistory.map((h) => [
            { role: "user", content: h.user },
            { role: "assistant", content: h.bot }
          ]).flat();
          const topicWords2 = recentHistory.flatMap((h) => (h.user || "").match(/[\u4e00-\u9fff]{2,4}|[A-Za-z]{3,}/g) || []);
          const freq = /* @__PURE__ */ new Map();
          for (const w of topicWords2) {
            const k = w.toLowerCase();
            freq.set(k, (freq.get(k) || 0) + 1);
          }
          const topicLabel = [...freq.entries()].sort((a, b) => b[1] - a[1]).slice(0, 3).map((e) => e[0]).join(" ") || "general";
          const hadCorrection = recentHistory.some((h) => /不对|错了|不是这样|纠正|其实/.test(h.user));
          const correction = hadCorrection ? { what: "\u4E0A\u4E00\u8F6E\u5BF9\u8BDD\u4E2D\u88AB\u7EA0\u6B63", cause: "\u9700\u8981\u4ECE episode \u4E2D\u5B66\u4E60" } : void 0;
          recordEpisode(topicLabel, turns, correction, "resolved", 0);
        }
      } catch (e) {
        console.log(`[cc-soul][episodic] record failed: ${e.message}`);
      }
    }
  }
  let prevScore = -1;
  if (session.lastPrompt && session.lastResponseContent && session.lastResponseContent.length > 5) {
    addToHistory(session.lastPrompt, session.lastResponseContent);
  }
  if (session.lastPrompt && session.lastResponseContent && session.lastResponseContent.length > 20) {
    prevScore = scoreResponse(session.lastPrompt, session.lastResponseContent);
    trackQuality(prevScore);
    trackDomainQuality(session.lastPrompt, prevScore);
    const prevIssue = selfCheckSync(session.lastPrompt, session.lastResponseContent);
    if (prevIssue) {
      console.log(`[cc-soul][quality] ${prevIssue} | ctx: ${session.lastPrompt.slice(0, 80)}`);
      body.anomaly = Math.min(1, body.anomaly + 0.1);
    }
    verifyHypothesis(session.lastPrompt, true);
    extractFollowUp(session.lastPrompt);
    trackRequestPattern(session.lastPrompt);
    detectAndDelegateTask(session.lastPrompt, session.lastResponseContent, event);
    try {
      trackPersonaStyle(session.lastResponseContent, getActivePersona()?.id ?? "default");
    } catch (_) {
    }
    try {
      updateBeliefFromMessage(session.lastPrompt, session.lastResponseContent);
    } catch (_) {
    }
    try {
      trackUserPattern(session.lastPrompt, prevScore >= 5);
    } catch (_) {
    }
    try {
      trackRecallImpact(session.lastRecalledContents, prevScore);
    } catch (_) {
    }
    if (!getPrivacyMode()) {
      const snapPrompt = session.lastPrompt;
      const snapResponse = session.lastResponseContent;
      const snapSenderId = session.lastSenderId;
      const snapChannelId = session.lastChannelId;
      session._lastAnalyzedPrompt = snapPrompt;
      metrics.cliCalls++;
      runPostResponseAnalysis(snapPrompt, snapResponse, (result) => {
        for (const m of result.memories) {
          addMemoryWithEmotion(m.content, m.scope, snapSenderId, m.visibility, snapChannelId, result.emotion, true);
        }
        addEntitiesFromAnalysis(result.entities);
        if (result.memoryOps && result.memoryOps.length > 0) {
          for (const op of result.memoryOps) {
            if (!op.keyword || op.keyword.length < 4) continue;
            if (!op.reason || op.reason.length < 3) continue;
            const kw = op.keyword.toLowerCase();
            if (op.action === "delete") {
              let deleted = 0;
              for (const mem of memoryState.memories) {
                if (deleted >= 2) break;
                if (mem.content.toLowerCase().includes(kw) && mem.scope !== "expired") {
                  mem.scope = "expired";
                  deleted++;
                }
              }
              if (deleted > 0) console.log(`[cc-soul][memory-ops] DELETE ${deleted} (keyword: ${op.keyword})`);
            } else if (op.action === "update" && op.newContent) {
              for (const mem of memoryState.memories) {
                if (mem.content.toLowerCase().includes(kw) && mem.scope !== "expired") {
                  console.log(`[cc-soul][memory-ops] UPDATE: "${mem.content.slice(0, 40)}" \u2192 "${op.newContent.slice(0, 40)}"`);
                  mem.content = op.newContent;
                  mem.ts = Date.now();
                  mem.tags = void 0;
                  break;
                }
              }
            }
          }
        }
        if (result.satisfaction === "POSITIVE") {
          bodyOnPositiveFeedback();
          stats.positiveFeedback++;
        }
        if (result.reflection && result.quality.score < 5) addMemory(`[\u53CD\u601D] ${result.reflection}`, "reflection", snapSenderId, "private", snapChannelId);
        const codeBlocks = snapResponse.match(/```(\w+)?\n([\s\S]*?)```/g);
        if (codeBlocks && codeBlocks.length > 0) {
          const lang = snapResponse.match(/```(\w+)/)?.[1] || "unknown";
          addMemory(`[\u4EE3\u7801\u6A21\u5F0F] \u8BED\u8A00:${lang} | ${snapPrompt.slice(0, 50)}`, "code_pattern", snapSenderId);
        }
        console.log(`[cc-soul][post-analysis] sat=${result.satisfaction} q=${result.quality.score} mem=${result.memories.length} ops=${result.memoryOps?.length || 0}`);
        brain.fire("onSent", { userMessage: snapPrompt, botReply: snapResponse, senderId: snapSenderId, channelId: snapChannelId, quality: result.quality });
      });
    }
  }
  if (routeCommand(userMsg, ctx, session, senderId, channelId, event)) {
    return;
  }
  if (!getPrivacyMode()) {
    try {
      const walEntries = [];
      const prefPatterns = [
        /我(?:比较)?喜欢(.{2,30})/g,
        /我(?:不|讨厌|很少|从不)喜欢(.{2,30})/g,
        /我是(.{2,20})/g,
        /我住在(.{2,20})/g,
        /我的(.{2,20}?)(?:是|叫|在)(.{2,20})/g,
        /(?:my |i (?:like|prefer|love|hate|am|live in) )(.{2,40})/gi
      ];
      for (const pat of prefPatterns) {
        pat.lastIndex = 0;
        let m;
        while ((m = pat.exec(userMsg)) !== null) {
          const extracted = m[0].trim();
          if (extracted.length >= 4 && extracted.length <= 80) {
            walEntries.push({ content: `[WAL\u504F\u597D] ${extracted}`, type: "preference" });
          }
        }
      }
      const factPatterns = [
        /(?:明天|后天|下周|下个月|今天|今晚|周[一二三四五六日天]|(?:\d{1,2}月\d{1,2}[日号])|(?:\d{4}[-/]\d{1,2}[-/]\d{1,2}))(.{2,40})/g,
        /(?:deadline|due|meeting|会议|截止|到期|出发|航班|考试|面试|约了)(.{2,30})/gi
      ];
      for (const pat of factPatterns) {
        pat.lastIndex = 0;
        let m;
        while ((m = pat.exec(userMsg)) !== null) {
          const extracted = m[0].trim();
          if (extracted.length >= 4 && extracted.length <= 80) {
            walEntries.push({ content: `[WAL\u4E8B\u5B9E] ${extracted}`, type: "fact" });
          }
        }
      }
      const seen = /* @__PURE__ */ new Set();
      let written = 0;
      for (const entry of walEntries) {
        if (written >= 3) break;
        const key = entry.content.slice(0, 40);
        if (seen.has(key)) continue;
        seen.add(key);
        addMemory(entry.content, "wal", senderId, "private", channelId);
        written++;
      }
      console.log(`[cc-soul][wal] checked: ${walEntries.length} extracted, ${written} written from "${userMsg.slice(0, 30)}"`);
    } catch (e) {
      console.log(`[cc-soul][wal] error: ${e.message}`);
    }
  }
  const followUpHints = peekPendingFollowUps();
  const workingMemKey = channelId || senderId || "_default";
  addWorkingMemory(userMsg.slice(0, 100), workingMemKey);
  const cog = cogProcess(userMsg, session.lastResponseContent, session.lastPrompt, senderId);
  bodyOnMessage(cog.complexity);
  if (session.lastAugmentsUsed.length > 0 && prevScore >= 0) {
    const wasCorrected = cog.attention === "correction";
    learnConflict(session.lastAugmentsUsed, wasCorrected);
    recordInteraction(session.lastAugmentsUsed, prevScore, wasCorrected);
  }
  const recentUserMsgs = memoryState.chatHistory.slice(-3).map((h) => h.user);
  const intentHints = predictIntent(userMsg, senderId, recentUserMsgs);
  if (intentHints.length > 0) cog.hints.push(...intentHints);
  const atmosphere = detectAtmosphere(userMsg, memoryState.chatHistory.slice(-5));
  if (atmosphere.length > 0) cog.hints.push(...atmosphere);
  const flowKey = senderId ? channelId ? channelId + ":" + senderId : senderId : channelId || "_default";
  const flow = updateFlow(userMsg, session.lastResponseContent, flowKey);
  processEmotionalContagion(userMsg, cog.attention, flow.frustration, senderId);
  const persona = selectPersona(cog.attention, flow.frustration, senderId, cog.intent, userMsg);
  if (persona) {
    console.log(`[cc-soul][persona] selected: ${persona.id} (${persona.name}) | trigger: ${cog.attention}/${cog.intent}`);
    if (senderId) trackPersonaUsage(senderId, persona.id);
  }
  const endedSessions = checkAllSessionEnds();
  for (const s of endedSessions) {
    generateSessionSummary(s.topic, s.turnCount, s.flowKey);
  }
  if (cog.attention === "correction") {
    stats.corrections++;
    updateProfileOnCorrection(senderId);
    updateRelationship(senderId, "correction");
    onCorrectionAdvanced(userMsg, session.lastResponseContent);
    trackDomainCorrection(userMsg);
    attributeCorrection(userMsg, session.lastResponseContent, session.lastAugmentsUsed);
    if (session.lastResponseContent) {
      try {
        recordEpisode(
          userMsg.slice(0, 80),
          [{ role: "assistant", content: session.lastResponseContent.slice(0, 200) }, { role: "user", content: userMsg.slice(0, 200) }],
          { what: userMsg.slice(0, 100), cause: "\u7528\u6237\u7EA0\u6B63\u4E86\u4E0A\u4E00\u8F6E\u56DE\u590D" },
          "resolved",
          0.4,
          `\u88AB\u7EA0\u6B63: ${userMsg.slice(0, 80)}`
        );
      } catch (_) {
      }
    }
    session._pendingCorrectionVerify = true;
  }
  if (cog.attention !== "correction") {
    verifyHypothesis(userMsg, true);
  } else {
    verifyHypothesis(userMsg, false);
  }
  CJK_TOPIC_REGEX.lastIndex = 0;
  const topicWords = userMsg.match(CJK_TOPIC_REGEX);
  if (topicWords) {
    topicWords.slice(0, 3).forEach((w) => stats.topics.add(w));
  }
  if (topicWords && topicWords.length > 0) {
    try {
      trackEmotionAnchor(topicWords.slice(0, 3));
    } catch (_) {
    }
  }
  stats.totalMessages++;
  if (stats.firstSeen === 0) stats.firstSeen = Date.now();
  saveStats();
  detectValueSignals(userMsg, false, senderId);
  let _extraAugments = [];
  try {
    const tomCtx = getToMContext();
    if (tomCtx) _extraAugments.push(tomCtx);
  } catch (_) {
  }
  try {
    const driftWarn = getPersonaDriftWarning();
    if (driftWarn) _extraAugments.push(`[\u4EBA\u683C\u6F02\u79FB\u8B66\u544A] ${driftWarn}`);
  } catch (_) {
  }
  try {
    const debateAug = buildDebateAugment(userMsg);
    if (debateAug) _extraAugments.push(debateAug.content);
  } catch (_) {
  }
  try {
    const skillSug = getSkillSuggestion();
    if (skillSug) _extraAugments.push(skillSug);
  } catch (_) {
  }
  try {
    const misconception = detectMisconception(userMsg);
    if (misconception) _extraAugments.push(`[\u8BA4\u77E5\u504F\u5DEE] ${misconception}`);
  } catch (_) {
  }
  try {
    const reinforcement = getPersonaDriftReinforcement();
    if (reinforcement) _extraAugments.push(reinforcement);
  } catch (_) {
  }
  const _userMsgKey = userMsg.slice(0, 100).toLowerCase().trim();
  const _prevReply = _recentReplies.get(_userMsgKey);
  let _dupHint = null;
  if (_prevReply && Date.now() - _prevReply.ts < 36e5) {
    _dupHint = `[\u91CD\u8981] \u7528\u6237\u521A\u624D\u53D1\u4E86\u548C\u4E4B\u524D\u4E00\u6837\u7684\u6D88\u606F\u3002\u4E0A\u6B21\u7684\u56DE\u590D\u6458\u8981\uFF1A"${_prevReply.reply.slice(0, 100)}"\u3002\u4E0D\u8981\u91CD\u590D\u4E0A\u6B21\u7684\u56DE\u7B54\uFF0C\u53EF\u4EE5\u8BF4"\u8FD9\u4E2A\u521A\u8BF4\u8FC7"\u6216\u6362\u4E2A\u89D2\u5EA6\u56DE\u7B54\u3002`;
  }
  const { selected, associated } = await buildAndSelectAugments({
    userMsg,
    session,
    senderId,
    channelId,
    cog,
    flow,
    flowKey,
    followUpHints,
    workingMemKey
  });
  if (_dupHint) selected.unshift(`[\u91CD\u590D\u6D88\u606F\u68C0\u6D4B] ${_dupHint}`);
  if (_extraAugments.length > 0) selected.push(..._extraAugments);
  try {
    const brainAugments = brain.firePreprocessed({ userMessage: userMsg, senderId, channelId, cog, augments: selected });
    for (const aug of brainAugments) {
      if (aug.content) selected.push(aug.content);
    }
  } catch (_) {
  }
  session.lastAugmentsUsed = selected;
  setLastAugments(selected);
  const augNames = selected.map((s) => {
    const m = s.match(/^\[([^\]]+)\]/);
    return m ? m[1] : s.slice(0, 20);
  });
  console.log(`[cc-soul][augment-inject] ${selected.length} augments: ${augNames.join(", ")}`);
  const historyCtx = buildHistoryContext();
  const cleanedSelected = selected.map((s) => s.replace(/^\[([^\]]+)\]\s*/, ""));
  const extraThinkIdx = cleanedSelected.findIndex((s) => s.includes("\u987A\u4FBF\u8BF4\u4E00\u4E0B") || s.includes("\u4E3E\u4E00\u53CD\u4E09"));
  let extraThinkItem = null;
  if (extraThinkIdx !== -1) {
    extraThinkItem = cleanedSelected.splice(extraThinkIdx, 1)[0];
  }
  const allContext = [historyCtx, ...cleanedSelected, extraThinkItem].filter(Boolean);
  if (allContext.length > 0) {
    const suffix = "\n\n---\n";
    const postfix = "";
    const injected = allContext.join("\n\n") + suffix + userMsg + postfix;
    ctx.bodyForAgent = injected;
    if (event.context) event.context.bodyForAgent = injected;
    console.log(`[cc-soul][bodyForAgent] set ${injected.length} chars on ctx + event.context`);
  } else {
    console.log(`[cc-soul][bodyForAgent] EMPTY \u2014 no augments to inject`);
  }
  try {
    const workspaceDir = resolve(homedir(), ".openclaw/workspace");
    const soulPath = resolve(workspaceDir, "SOUL.md");
    const baseSoul = buildSoulPrompt(stats.totalMessages, stats.corrections, stats.firstSeen, taskState.workflows);
    const augmentSection = cleanedSelected.length > 0 ? "\n\n## \u5185\u90E8\u6307\u4EE4\uFF08\u4EC5\u672C\u8F6E\u6709\u6548\uFF09\n" + cleanedSelected.join("\n") : "";
    let tipsSection = "";
    console.log(`[cc-soul] prompt built: ${cleanedSelected.length} augments${tipsSection ? " + \u4E3E\u4E00\u53CD\u4E09" : ""}`);
  } catch (e) {
    console.log(`[cc-soul] SOUL.md dynamic update failed: ${e.message}`);
  }
  triggerDeepReflection(stats);
  metrics.augmentsInjected += selected.length;
  metrics.recallCalls++;
  metricsRecordResponseTime(Date.now() - _metricsStart);
  session.lastPrompt = userMsg;
  session.lastSenderId = senderId;
  session.lastChannelId = channelId;
  session.lastResponseContent = "";
  session._dedupKey = userMsg.slice(0, 100).toLowerCase().trim();
  {
    let raw = (event.context || {}).body || userMsg;
    raw = raw.replace(/^\[message_id:\s*\S+\]\s*/i, "");
    raw = raw.replace(/^[a-zA-Z0-9_\u4e00-\u9fff]{1,20}:\s*/, "");
    raw = raw.replace(/^\n+/, "").trim();
    session._rawUserMsg = raw || userMsg;
  }
  innerState.lastActivityTime = Date.now();
  const _snapPrompt = userMsg;
  const _snapRawMsg = session._rawUserMsg;
  const _snapSenderId = senderId;
  const _snapChannelId = channelId;
  const _isCasual = /^(哈哈|嗯|好的?|ok|早|晚安|谢谢|收到|了解|明白|懂了)$/i.test(userMsg.trim());
  if (!_isCasual && userMsg.length >= 5) {
    setTimeout(async () => {
      try {
        const currentSession = getSessionState(getLastActiveSessionKey());
        if (currentSession.lastPrompt && currentSession.lastPrompt !== _snapPrompt) return;
        const sessionDir = resolve(homedir(), ".openclaw/agents/cc/sessions");
        const files = readdirSync(sessionDir).filter((f) => f.endsWith(".jsonl")).sort();
        if (files.length === 0) return;
        const lastFile = resolve(sessionDir, files[files.length - 1]);
        const lines = readFileSync(lastFile, "utf-8").trim().split("\n");
        let botResponse = "";
        for (let i = lines.length - 1; i >= 0; i--) {
          try {
            const obj = JSON.parse(lines[i]);
            if (obj?.message?.role === "assistant") {
              botResponse = Array.isArray(obj.message.content) ? obj.message.content.filter((c) => c?.type === "text").map((c) => c.text || "").join("") : obj.message.content || "";
              break;
            }
          } catch {
          }
        }
        if (!botResponse || botResponse.length < 20) return;
        session.lastResponseContent = botResponse;
        console.log(`[cc-soul][delayed-post] processing response (${botResponse.length} chars) for "${_snapPrompt.slice(0, 30)}"`);
        if (isEnabled("self_correction")) {
          const selfIssue = selfCheckSync(_snapPrompt, botResponse);
          if (selfIssue) {
            const scScore = scoreResponse(_snapPrompt, botResponse);
            if (scScore <= 3) {
              notifyOwnerDM(`\u26A0\uFE0F \u521A\u624D\u7684\u56DE\u7B54\u53EF\u80FD\u6709\u8BEF\uFF1A${selfIssue}\u3002\u8BC4\u5206 ${scScore}/10`).catch(() => {
              });
              console.log(`[cc-soul][delayed-post] self-correction: ${selfIssue} (score=${scScore})`);
            }
          }
        }
        try {
          const persona2 = getActivePersona();
          if (persona2) {
            const driftScore = checkPersonaDrift(botResponse, persona2.id, persona2.name, persona2.tone, persona2.idealVector);
            if (driftScore > 0.5) {
              stats.driftCount++;
              saveStats();
            }
          }
        } catch {
        }
        try {
          recordTurnUsage(_snapPrompt, botResponse, 0);
        } catch {
        }
        try {
          brain.fire("onSent", { userMessage: _snapPrompt, botReply: botResponse, senderId: _snapSenderId, channelId: _snapChannelId });
        } catch {
        }
        {
          const memCmds = parseMemoryCommands(botResponse);
          if (memCmds.length > 0) executeMemoryCommands(memCmds, _snapSenderId, _snapChannelId);
        }
        addToHistory(_snapPrompt, botResponse);
        const prevScore2 = scoreResponse(_snapPrompt, botResponse);
        trackQuality(prevScore2);
        if (!getPrivacyMode()) {
          runPostResponseAnalysis(_snapPrompt, botResponse, (result) => {
            for (const m of result.memories) {
              addMemoryWithEmotion(m.content, m.scope, _snapSenderId, m.visibility, _snapChannelId, result.emotion, true);
            }
            addEntitiesFromAnalysis(result.entities);
            if (result.satisfaction === "POSITIVE") bodyOnPositiveFeedback();
            console.log(`[cc-soul][delayed-post] analysis done: sat=${result.satisfaction} q=${result.quality.score} mem=${result.memories.length}`);
          });
        }
        try {
          collectAvatarData(_snapRawMsg || _snapPrompt, botResponse, _snapSenderId);
        } catch (_) {
        }
      } catch (e) {
        console.log(`[cc-soul][delayed-post] error: ${e.message}`);
      }
    }, 45e3);
  }
}
function handleSent(event) {
  if (!getInitialized()) initializeSoul();
  setAgentBusy(false);
  killGatewayClaude();
  postReplyCleanup().catch(() => {
  });
  const sentSessionKey = event.sessionKey || getLastActiveSessionKey();
  const session = getSessionState(sentSessionKey);
  const content = event.context?.content || event.content || event.text || "";
  console.log(`[cc-soul][handleSent] content=${content.length} chars, keys=${Object.keys(event).join(",")}`);
  if (content) {
    session.lastResponseContent = content;
    {
      const _sentMsgKey = session._dedupKey || (session.lastPrompt || "").slice(0, 100).toLowerCase().trim();
      if (_sentMsgKey) {
        _recentReplies.set(_sentMsgKey, { reply: content.slice(0, 200), ts: Date.now() });
        for (const [k, v] of Object.entries(_recentRepliesObj)) {
          if (Date.now() - v.ts > 36e5) _recentReplies.delete(k);
        }
      }
    }
    try {
      if (session.lastRecalledContents.length > 0 && content.length > 20) {
        const { scoreAffinity } = require("./answer-affinity.ts");
        const stubMemories = session.lastRecalledContents.map((c) => ({ content: c, ts: Date.now(), scope: "recalled" }));
        const affinityResults = scoreAffinity(stubMemories, content, session.lastPrompt || "");
        const usedCount = affinityResults.filter((r) => r.signal === "used").length;
        if (usedCount > 0 || affinityResults.length > 0) {
          console.log(`[cc-soul][affinity] ${usedCount}/${affinityResults.length} memories contributed to response`);
        }
      }
    } catch {
    }
    {
      const augTokens = session.lastAugmentsUsed.reduce((sum, a) => sum + estimateTokens(a), 0);
      try {
        recordTurnUsage(session.lastPrompt || "", content, augTokens);
      } catch (_) {
      }
    }
    if (getReadAloudPending() && platform() === "darwin") {
      setReadAloudPending(false);
      const safeText = content.replace(/["`$\\]/g, "").slice(0, 2e3);
      execFile("say", [safeText], (err) => {
        if (err) console.log(`[cc-soul][tts] say failed: ${err.message}`);
      });
    }
    setReadAloudPending(false);
    try {
      const persona = getActivePersona();
      if (persona) {
        const driftScore = checkPersonaDrift(content, persona.id, persona.name, persona.tone, persona.idealVector);
        if (driftScore > 0.5) {
          stats.driftCount++;
          saveStats();
        }
      }
    } catch (_) {
    }
    if (isEnabled("self_correction") && session.lastPrompt && content.length > 20) {
      const selfIssue = selfCheckSync(session.lastPrompt, content);
      if (selfIssue) {
        const scScore = scoreResponse(session.lastPrompt, content);
        if (scScore <= 3) {
          notifyOwnerDM(`\u26A0\uFE0F \u521A\u624D\u7684\u56DE\u7B54\u53EF\u80FD\u6709\u8BEF\uFF1A${selfIssue}\u3002\u8865\u5145\uFF1A\u56DE\u590D\u8D28\u91CF\u8BC4\u5206 ${scScore}/10\uFF0C\u95EE\u9898="${session.lastPrompt.slice(0, 60)}"`).catch(() => {
          });
          console.log(`[cc-soul][self-correction] issue detected (score=${scScore}): ${selfIssue}`);
        }
      }
    }
    {
      const memCommands = parseMemoryCommands(content);
      if (memCommands.length > 0) {
        executeMemoryCommands(memCommands, session.lastSenderId, session.lastChannelId);
      }
    }
    if (session.lastRecalledContents.length > 0) {
      const timeStr = (/* @__PURE__ */ new Date()).toLocaleTimeString("zh-CN", { hour: "2-digit", minute: "2-digit" });
      innerState.journal.push({
        time: timeStr,
        thought: `[\u63A8\u7406\u94FE] \u56DE\u590D\u300C${session.lastPrompt.slice(0, 30)}\u300D\u65F6\u53EC\u56DE ${session.lastRecalledContents.length} \u6761\u8BB0\u5FC6: ${session.lastRecalledContents.slice(0, 3).map((c) => c.slice(0, 40)).join("; ")}`,
        type: "observation"
      });
    }
    const snapPrompt = session.lastPrompt;
    const snapResponse = session.lastResponseContent;
    const snapSenderId = session.lastSenderId;
    const snapChannelId = session.lastChannelId;
    const snapRecalled = [...session.lastRecalledContents];
    const snapMatchedRules = [...session.lastMatchedRuleTexts];
    setTimeout(() => {
      if (session._lastAnalyzedPrompt === snapPrompt) return;
      if (snapPrompt && snapResponse && !getPrivacyMode()) {
        session._lastAnalyzedPrompt = snapPrompt;
        metrics.cliCalls++;
        runPostResponseAnalysis(snapPrompt, snapResponse, (result) => {
          for (const m of result.memories) {
            addMemoryWithEmotion(m.content, m.scope, snapSenderId, m.visibility, snapChannelId, result.emotion, true);
          }
          addEntitiesFromAnalysis(result.entities);
          if (result.memoryOps && result.memoryOps.length > 0) {
            const MAX_OPS_PER_TURN = 3;
            const MAX_DELETE_PER_OP = 2;
            let opsExecuted = 0;
            for (const op of result.memoryOps) {
              if (opsExecuted >= MAX_OPS_PER_TURN) {
                console.log(`[cc-soul][memory-ops] CAPPED at ${MAX_OPS_PER_TURN} ops (anti-hallucination)`);
                break;
              }
              if (!op.keyword || op.keyword.length < 4) {
                console.log(`[cc-soul][memory-ops] SKIP: keyword too short "${op.keyword}" (anti-hallucination)`);
                continue;
              }
              if (!op.reason || op.reason.length < 3) {
                console.log(`[cc-soul][memory-ops] SKIP: no valid reason for ${op.action} "${op.keyword}" (anti-hallucination)`);
                continue;
              }
              const kw = op.keyword.toLowerCase();
              if (op.action === "delete") {
                let deleted = 0;
                const mems = memoryState.memories;
                for (let i = 0; i < mems.length && deleted < MAX_DELETE_PER_OP; i++) {
                  if (mems[i].content.toLowerCase().includes(kw) && mems[i].scope !== "expired") {
                    mems[i].scope = "expired";
                    deleted++;
                  }
                }
                if (deleted > 0) console.log(`[cc-soul][memory-ops] DELETE ${deleted} memories (keyword: ${op.keyword}, reason: ${op.reason})`);
              } else if (op.action === "update" && op.newContent) {
                const idx = memoryState.memories.findIndex((m) => m.content.toLowerCase().includes(kw) && m.scope !== "expired");
                if (idx >= 0) {
                  const mem = memoryState.memories[idx];
                  console.log(`[cc-soul][memory-ops] UPDATE: "${mem.content.slice(0, 40)}" \u2192 "${op.newContent.slice(0, 40)}" (reason: ${op.reason})`);
                  mem.content = op.newContent;
                  mem.ts = Date.now();
                  mem.tags = void 0;
                }
              }
              opsExecuted++;
            }
          }
          if (result.satisfaction === "POSITIVE") {
            bodyOnPositiveFeedback();
            detectValueSignals(snapPrompt, true, snapSenderId);
            updateRelationship(snapSenderId, "positive");
            stats.positiveFeedback++;
            trackGratitude(snapPrompt, snapResponse, snapSenderId);
            updateUserStylePreference(snapSenderId, snapResponse, true);
          } else if (result.satisfaction === "NEGATIVE") {
            updateUserStylePreference(snapSenderId, snapResponse, false);
          }
          const qScore = Math.max(1, Math.min(10, result.quality.score));
          trackQuality(qScore);
          if (snapRecalled.length > 0) trackRecallImpact(snapRecalled, qScore);
          updateBanditReward(qScore, result.satisfaction === "NEGATIVE");
          if (qScore <= 4) {
            body.alertness = Math.min(1, body.alertness + 0.08);
          }
          if (snapMatchedRules.length > 0) {
            const matchedRuleObjs = rules.filter((r) => snapMatchedRules.includes(r.rule));
            if (matchedRuleObjs.length > 0) {
              recordRuleQuality(matchedRuleObjs, result.quality.score);
            }
          }
          if (result.reflection && result.quality.score < 5) {
            addMemory(`[\u53CD\u601D] ${result.reflection}`, "reflection", snapSenderId, "private", snapChannelId);
          }
        });
        recallFeedbackLoop(snapPrompt, snapRecalled);
        triggerAssociativeRecall(snapPrompt, snapRecalled);
        writeJournalWithCLI(snapPrompt, snapResponse, stats);
        detectWorkflowOpportunity(snapPrompt, snapResponse);
        CJK_WORD_REGEX.lastIndex = 0;
        const recentTopicWords = (snapPrompt.match(CJK_WORD_REGEX) || []).slice(0, 5);
        generatePrediction(recentTopicWords, snapSenderId);
        if (isEnabled("skill_library")) autoExtractSkill(snapPrompt, snapResponse);
        refreshNarrativeAsync();
        try {
          const ap = getActivePersona();
          trackPersonaStyle(snapResponse, ap?.id ?? "default");
        } catch (_) {
        }
        try {
          updateBeliefFromMessage(snapPrompt, snapResponse);
        } catch (_) {
        }
        if (isEnabled("memory_session_summary") && (stats.totalMessages % 10 === 0 || memoryState.chatHistory.length >= 8)) {
          triggerSessionSummary();
        }
        try {
          collectAvatarData(session._rawUserMsg || snapPrompt, snapResponse, snapSenderId);
        } catch (_) {
        }
        innerState.lastActivityTime = Date.now();
      }
    }, 2e3);
  }
}
function handleCommand(event) {
  if (!getInitialized()) initializeSoul();
  flushAll();
  computeEval(stats.totalMessages, stats.corrections, true);
  console.log(
    `[cc-soul] session ${event.action} | mem:${memoryState.memories.length} rules:${rules.length} entities:${graphState.entities.length} | msgs:${stats.totalMessages} corrections:${stats.corrections} tasks:${stats.tasks} | eval: ${getEvalSummary(stats.totalMessages, stats.corrections)} | body: e=${body.energy.toFixed(2)} m=${body.mood.toFixed(2)} a=${body.alertness.toFixed(2)}`
  );
}
const handler = async (event) => {
  if (!getInitialized()) initializeSoul();
  try {
    if (event.type === "agent" && event.action === "bootstrap") {
      if (isContextEngineActive()) return;
      handleBootstrap(event);
      return;
    }
    if (event.type === "message" && event.action === "preprocessed") {
      handlePreprocessed(event);
      return;
    }
    if (event.type === "message" && event.action === "sent") {
      handleSent(event);
      return;
    }
    if (event.type === "command") {
      handleCommand(event);
    }
  } catch (err) {
    recordModuleError("handler", err?.message || String(err));
    console.error("[cc-soul] error:", err?.message || err);
  }
};
var handler_default = handler;
import { runHeartbeat as runHeartbeat2 } from "./handler-heartbeat.ts";
import { getStats, metrics as metrics2, formatMetrics } from "./handler-state.ts";
export {
  handler_default as default,
  formatMetrics,
  getInitialized2 as getInitialized,
  getStats,
  handleBootstrap,
  handleCommand,
  handlePreprocessed,
  handleSent,
  initializeSoul2 as initializeSoul,
  metrics2 as metrics,
  runHeartbeat2 as runHeartbeat,
  setInitialized
};
