import "./persistence.ts";
const _lastPenalizeTs = /* @__PURE__ */ new Map();
const _dedupCache = /* @__PURE__ */ new Map();
let _crossTurnLastMsg = {};
const DEDUP_TTL = 36e5;
function cleanDedup() {
  const now = Date.now();
  for (const [k, v] of _dedupCache) {
    if (now - v.ts > DEDUP_TTL) _dedupCache.delete(k);
  }
}
async function safeCompute(fn, fallback, context) {
  try {
    return await fn();
  } catch (e) {
    try {
      const { logDecision } = require("./decision-log.ts");
      logDecision("degraded", context, e.message);
    } catch {
    }
    console.warn(`[cc-soul][${context}] degraded: ${e.message}`);
    return fallback;
  }
}
async function handleProcess(body) {
  try {
    (await import("./cli.ts")).hotReloadIfChanged();
  } catch {
  }
  const message = body.message || "";
  const userId = body.user_id || body.userId || "default";
  const agentId = body.agent_id || body.agentId || "default";
  const customPrompt = body.system_prompt || "";
  if (body.context_window && typeof body.context_window === "number") {
    try {
      const { setContextWindow } = await import("./context-budget.ts");
      setContextWindow(body.context_window);
    } catch {
    }
  }
  try {
    (await import("./memory.ts")).ensureMemoriesLoaded();
  } catch {
  }
  let turnSnapshot2 = null;
  try {
    const { memoryState } = await import("./memory.ts");
    turnSnapshot2 = /* @__PURE__ */ new Map();
    for (const m of memoryState.memories) {
      if (m.memoryId) turnSnapshot2.set(m.memoryId, m.lineage?.length ?? 0);
    }
  } catch {
  }
  if (agentId !== "default") {
    try {
      const { setActiveAgent } = await import("./persistence.ts");
      setActiveAgent(agentId);
    } catch {
    }
  }
  let isPrivacy = false;
  try {
    const { getPrivacyMode } = await import("./handler-state.ts");
    isPrivacy = getPrivacyMode();
  } catch {
  }
  if (!message) {
    try {
      const { ensureDataDir } = await import("./persistence.ts");
      ensureDataDir();
      try {
        (await import("./memory.ts")).ensureSQLiteReady();
      } catch {
      }
    } catch {
    }
    try {
      (await import("./handler.ts")).initializeSoul();
    } catch {
    }
    let soulPrompt2 = "";
    try {
      const { buildSoulPrompt } = await import("./prompt-builder.ts");
      const { stats } = await import("./handler-state.ts");
      soulPrompt2 = buildSoulPrompt(stats.totalMessages, stats.corrections, stats.firstSeen, []);
    } catch {
    }
    return { system_prompt: customPrompt ? customPrompt + "\n\n" + soulPrompt2 : soulPrompt2, augments: [] };
  }
  try {
    const { routeCommand, routeCommandDirect } = await import("./handler-commands.ts");
    const { getSessionState } = await import("./handler-state.ts");
    const session = getSessionState(userId);
    let cmdReply = "";
    const replyFn = (t) => {
      cmdReply = t;
    };
    const cmdCtx = { bodyForAgent: "", reply: replyFn };
    const handled = routeCommand(message, cmdCtx, session, userId, "", { context: { senderId: userId } });
    if (handled && cmdReply) {
      return { command: true, command_reply: cmdReply };
    }
    if (!cmdReply) {
      const directHandled = await routeCommandDirect(message, { replyCallback: replyFn });
      if (directHandled && cmdReply) {
        return { command: true, command_reply: cmdReply };
      }
    }
  } catch (cmdErr) {
    console.error(`[cc-soul][api] command detection error: ${cmdErr.message}`);
  }
  try {
    (await import("./persistence.ts")).ensureDataDir();
    try {
      (await import("./memory.ts")).ensureSQLiteReady();
    } catch {
    }
  } catch {
  }
  try {
    (await import("./handler.ts")).initializeSoul();
  } catch {
  }
  try {
    (await import("./aam.ts")).learnAssociation(message);
  } catch {
  }
  try {
    const _uid = senderId || "default";
    if (!_crossTurnLastMsg) _crossTurnLastMsg = {};
    const lastMsg = _crossTurnLastMsg[_uid] || "";
    if (lastMsg.length > 10 && message.length > 10) {
      const prev = (lastMsg.match(/[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}/gi) || []).slice(0, 8);
      const curr = (message.match(/[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}/gi) || []).slice(0, 8);
      if (prev.length > 0 && curr.length > 0) {
        (await import("./aam.ts")).learnAssociation(prev.join(" ") + " " + curr.join(" "), 0.3);
      }
    }
    _crossTurnLastMsg[_uid] = message;
  } catch {
  }
  try {
    (await import("./semantic-drift.ts")).trackMessage(message);
  } catch {
  }
  try {
    (await import("./aam.ts")).maybeTranslateSeedsForLanguage(message);
  } catch {
  }
  const bodyFallback = { mood: 0, energy: 0.5, alertness: 0.5 };
  const bodyResult = await safeCompute(async () => {
    const bodyMod = await import("./body.ts");
    try {
      bodyMod.loadBodyState();
    } catch {
    }
    let peakHour;
    try {
      peakHour = (await import("./user-profiles.ts")).getUserPeakHour(userId);
      if (peakHour === -1) peakHour = void 0;
    } catch {
    }
    bodyMod.bodyTick(peakHour);
    bodyMod.bodyOnMessage(message.length > 50 ? 0.6 : 0.3);
    return { mood: bodyMod.body.mood, energy: bodyMod.body.energy, alertness: bodyMod.body.alertness ?? 0.5 };
  }, bodyFallback, "body-tick");
  let moodScore = bodyResult.mood, energyScore = bodyResult.energy, emotion = "neutral";
  const cogFallback = { attention: "general", intent: "wants_answer", strategy: "balanced", complexity: 0.3, hints: [], spectrum: { information: 0.5, action: 0.2, emotional: 0.2, validation: 0.1, exploration: 0.2 } };
  let cogResult = await safeCompute(async () => {
    const { cogProcess } = await import("./cognition.ts");
    const { getSessionState: _getSess } = await import("./handler-state.ts");
    const _sess = _getSess(userId);
    const result = cogProcess(message, _sess.lastResponseContent || "", _sess.lastPrompt || "", userId);
    if (result.attention === "correction") {
      try {
        (await import("./user-profiles.ts")).updateProfileOnCorrection(userId);
        (await import("./body.ts")).bodyOnCorrection();
        const { emitCacheEvent } = require("./memory-utils.ts");
        emitCacheEvent("correction_received");
      } catch {
      }
    }
    return result;
  }, cogFallback, "cognition");
  let flow = null;
  try {
    flow = (await import("./flow.ts")).updateFlow(message, "", userId);
  } catch {
  }
  if (flow?.turnCount === 1) {
    try {
      (await import("./memory.ts")).incrementSegment();
    } catch {
    }
  }
  try {
    const bodyMod = await import("./body.ts");
    const attention = cogResult?.attention || "general";
    const frustration = flow?.frustrationTrajectory?.current ?? flow?.frustration ?? 0;
    bodyMod.processEmotionalContagion(message, attention, frustration, userId);
    moodScore = bodyMod.body.mood;
    energyScore = bodyMod.body.energy;
    emotion = moodScore > 0.3 ? "positive" : moodScore < -0.3 ? "negative" : "neutral";
  } catch {
  }
  let _sharedFacts = [];
  try {
    const { extractFacts } = await import("./fact-store.ts");
    _sharedFacts = extractFacts(message, "user_said", userId);
    globalThis.__ccSoulSharedFacts = _sharedFacts;
    globalThis.__ccSoulSharedFactsTs = Date.now();
  } catch {
  }
  try {
    (await import("./user-profiles.ts")).updateProfileOnMessage(userId, message);
  } catch {
  }
  if (!isPrivacy) {
    try {
      const { addMemory } = await import("./memory.ts");
      const walEntries = [];
      const prefMatch = message.match(/我(?:最|特别|超|很|比较)?(?:喜欢|不喜欢|讨厌|爱|偏好|住在?|是|养了?|有|擅长|从事|叫|在.{1,10}(?:工作|上班|做))(.{2,40})/g);
      if (prefMatch) for (const p of prefMatch.slice(0, 3)) {
        const trimmed = message.trim();
        const isQuestion = /[？?]$/.test(trimmed) || // 问号结尾
        /(.)\1不\1/.test(trimmed) || // 动词重叠疑问（是不是/有没有）
        /[吗呢吧嘛]$/.test(trimmed) || // 语气词结尾
        /[？?]/.test(p);
        if (isQuestion) continue;
        if (p.length < message.length * 0.2 && p.length < 8) continue;
        walEntries.push(p.slice(0, 60));
      }
      const rememberMatch = message.match(/(?:记住|帮我记|你要知道)[：:，,\s]*(.{4,60})/g);
      if (rememberMatch) for (const r of rememberMatch.slice(0, 3)) walEntries.push(r.slice(0, 60));
      for (const entry of walEntries) addMemory(`[WAL\u4E8B\u5B9E] ${entry}`, "wal", userId, "private");
      if (walEntries.length > 0) console.log(`[cc-soul][api] WAL: ${walEntries.length} entries`);
    } catch {
    }
    try {
      if (_sharedFacts.length > 0) {
        const { addFacts } = await import("./fact-store.ts");
        addFacts(_sharedFacts);
      }
    } catch {
    }
    try {
      (await import("./avatar.ts")).collectAvatarData(message, "", userId);
    } catch {
    }
  }
  try {
    const { generateProactiveItems } = await import("./soul-proactive.ts");
    const hints = await generateProactiveItems();
    if (hints.length > 0) {
      const { addWorkingMemory } = await import("./memory.ts");
      addWorkingMemory(`[\u81EA\u52A8\u6D1E\u5BDF]
${hints.map((h) => h.message).join("\n")}`, userId);
    }
  } catch {
  }
  let dupHint = "";
  try {
    cleanDedup();
    const dedupKey = message.slice(0, 100).toLowerCase().trim();
    const prev = _dedupCache.get(dedupKey);
    if (prev && Date.now() - prev.ts < DEDUP_TTL) {
      const replyHint = prev.reply ? `\u4E0A\u6B21\u7684\u56DE\u590D\u6458\u8981\uFF1A"${prev.reply.slice(0, 100)}"\u3002` : "";
      dupHint = `[\u91CD\u8981] \u7528\u6237\u53D1\u4E86\u548C\u4E4B\u524D\u4E00\u6837\u7684\u6D88\u606F\uFF1A"${message.slice(0, 50)}"\u3002${replyHint}\u4E0D\u8981\u91CD\u590D\u4E0A\u6B21\u7684\u56DE\u7B54\uFF0C\u6362\u4E2A\u89D2\u5EA6\u6216\u8BF4"\u8FD9\u4E2A\u521A\u8BF4\u8FC7\uFF0C\u8FD8\u6709\u4EC0\u4E48\u4E0D\u6E05\u695A\u7684\uFF1F"\u3002`;
    }
    if (!_dedupCache.has(dedupKey)) {
      _dedupCache.set(dedupKey, { reply: "", ts: Date.now() });
    } else {
      _dedupCache.get(dedupKey).ts = Date.now();
    }
  } catch {
  }
  let selected = [];
  let augmentObjects = [];
  let recalled = [];
  try {
    const { buildAndSelectAugments } = await import("./handler-augments.ts");
    const { getSessionState } = await import("./handler-state.ts");
    const session = getSessionState(userId);
    session.lastPrompt = message;
    session.lastSenderId = userId;
    let _cogHints = null;
    try {
      _cogHints = (await import("./cognition.ts")).toCogHints(message);
    } catch {
    }
    const result = await buildAndSelectAugments({
      userMsg: message,
      session,
      senderId: userId,
      channelId: "",
      cog: cogResult || { attention: "general", intent: "wants_answer", strategy: "balanced", complexity: 0.3, hints: [] },
      cogHints: _cogHints,
      flow: flow || { turnCount: 0, frustration: 0 },
      flowKey: userId,
      followUpHints: [],
      workingMemKey: userId
    });
    selected = result.selected || [];
    if (dupHint) selected.unshift(`[\u91CD\u590D\u6D88\u606F\u68C0\u6D4B] ${dupHint}`);
    augmentObjects = (result.augments || []).map((a) => ({
      content: a.content || "",
      priority: a.priority || 0,
      tokens: a.tokens || 0
    }));
    recalled = (result.augments || []).filter((a) => a.content?.includes("\u8BB0\u5FC6") || a.content?.includes("recall")).map((a) => ({ content: a.content, scope: "recalled" }));
  } catch (e) {
    console.log(`[cc-soul][api] augment build error: ${e.message}`);
  }
  let soulPrompt = "";
  try {
    const { buildSoulPrompt } = await import("./prompt-builder.ts");
    const { stats } = await import("./handler-state.ts");
    soulPrompt = buildSoulPrompt(stats.totalMessages, stats.corrections, stats.firstSeen, []);
  } catch {
  }
  const staticPrompt = soulPrompt;
  const dynamicPrompt = selected.join("\n\n");
  return {
    system_prompt: customPrompt ? customPrompt + "\n\n" + staticPrompt : staticPrompt,
    // 新增：分段输出，让调用方可以分别处理 static/dynamic
    static_prompt: staticPrompt,
    dynamic_prompt: dynamicPrompt,
    augments: dynamicPrompt,
    augments_array: augmentObjects,
    memories: recalled.map((m) => ({ content: m.content, scope: m.scope, emotion: m.emotion })),
    mood: moodScore,
    energy: energyScore,
    emotion,
    cognition: cogResult ? {
      attention: cogResult.attention,
      intent: cogResult.intent,
      strategy: cogResult.strategy,
      complexity: cogResult.complexity
    } : null
  };
}
async function handleFeedback(body) {
  const userMessage = body.user_message || "";
  const aiReply = body.ai_reply || "";
  const userId = body.user_id || body.userId || "default";
  const agentId = body.agent_id || body.agentId || "default";
  const satisfaction = body.satisfaction || "";
  if (agentId !== "default") {
    try {
      const { setActiveAgent } = await import("./persistence.ts");
      setActiveAgent(agentId);
    } catch {
    }
  }
  if (!userMessage || !aiReply) return { error: "user_message and ai_reply required" };
  try {
    const { getPrivacyMode } = await import("./handler-state.ts");
    if (getPrivacyMode()) return { learned: false, reason: "privacy_mode" };
  } catch {
  }
  try {
    const dedupKey = userMessage.slice(0, 100).toLowerCase().trim();
    _dedupCache.set(dedupKey, { reply: aiReply.slice(0, 200), ts: Date.now() });
    cleanDedup();
  } catch {
  }
  try {
    (await import("./memory.ts")).addToHistory(userMessage, aiReply);
  } catch {
  }
  try {
    (await import("./avatar.ts")).collectAvatarData(userMessage, aiReply, userId);
  } catch {
  }
  let qualityScore = -1;
  try {
    const { scoreResponse, trackQuality } = await import("./quality.ts");
    qualityScore = scoreResponse(userMessage, aiReply);
    trackQuality(qualityScore);
    const { getSessionState, getLastActiveSessionKey } = await import("./handler-state.ts");
    const sess = getSessionState(getLastActiveSessionKey());
    if (sess) sess.lastQualityScore = qualityScore;
  } catch {
  }
  try {
    const { bodyOnPositiveFeedback, bodyOnCorrection } = await import("./body.ts");
    if (satisfaction === "positive") {
      bodyOnPositiveFeedback();
      try {
        const { confirmTruthfulness } = await import("./smart-forget.ts");
        const { memoryState } = await import("./memory.ts");
        const recentInjected = memoryState.memories.filter(
          (m) => m && (m.injectionEngagement ?? 0) > 0 && Date.now() - (m.lastAccessed || 0) < 6e5
        ).slice(0, 3);
        for (const m of recentInjected) {
          confirmTruthfulness(m, `\u7528\u6237\u6B63\u9762\u53CD\u9988(satisfaction=positive)`);
        }
      } catch {
      }
    }
    if (satisfaction === "negative") bodyOnCorrection();
  } catch {
  }
  try {
    (await import("./user-profiles.ts")).trackGratitude(userMessage, aiReply, userId);
  } catch {
  }
  try {
    const { addMemory } = await import("./memory.ts");
    addMemory(`[\u5BF9\u8BDD] \u7528\u6237: ${userMessage.slice(0, 60)} \u2192 AI: ${aiReply.slice(0, 60)}`, "fact", userId, "private");
    const { autoExtractFromMemory } = await import("./fact-store.ts");
    autoExtractFromMemory(userMessage, "fact", "user_said");
  } catch {
  }
  try {
    const { updateLivingProfile } = await import("./person-model.ts");
    const importance = /名字|叫我|工作|公司|住|女儿|儿子|老婆|喜欢|讨厌|每天|习惯/.test(userMessage) ? 8 : 5;
    updateLivingProfile(userMessage, "fact", importance);
  } catch {
  }
  try {
    const { runPostResponseAnalysis } = await import("./cli.ts");
    const { addMemoryWithEmotion } = await import("./memory.ts");
    const { addEntitiesFromAnalysis } = await import("./graph.ts");
    const analysisPromise = new Promise((resolve) => {
      const timeout = setTimeout(() => {
        console.log(`[cc-soul][api] feedback analysis timed out`);
        resolve();
      }, 2e4);
      runPostResponseAnalysis(userMessage, aiReply, (result) => {
        clearTimeout(timeout);
        try {
          for (const m of result.memories || []) {
            const memKeywords = (m.content.match(/[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}/gi) || []).map((w) => w.toLowerCase());
            const msgKeywords = new Set((userMessage.match(/[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}/gi) || []).map((w) => w.toLowerCase()));
            const grounded = memKeywords.filter((w) => msgKeywords.has(w)).length;
            if (memKeywords.length > 0 && grounded === 0 && m.scope === "fact") {
              console.log(`[cc-soul][anti-hallucination] SKIP ungrounded fact: ${m.content.slice(0, 50)}`);
              continue;
            }
            addMemoryWithEmotion(m.content, m.scope, userId, m.visibility, "", result.emotion, true);
          }
          if (result.entities) addEntitiesFromAnalysis(result.entities);
          if (result.memoryOps?.length > 0) {
            import("./memory.ts").then(({ executeMemoryCommands }) => {
              executeMemoryCommands(result.memoryOps.slice(0, 3), userId, "");
            }).catch((e) => {
              console.error(`[cc-soul] module load failed (memory): ${e.message}`);
            });
          }
          try {
            const { dynamicExtract, updateStructureStrength } = require("./dynamic-extractor.ts");
            for (const m of result.memories || []) {
              const tier1Results = dynamicExtract(m.content, userId);
              if (tier1Results.length > 0) {
                for (const r of tier1Results) updateStructureStrength(r.structureWord, userId, true);
              } else {
                const cjkPhrases = m.content.match(/[\u4e00-\u9fff]{2,3}/g) || [];
                for (const phrase of cjkPhrases.slice(0, 3)) {
                  try {
                    const aamMod = require("./aam.ts");
                    const bodyMod = require("./body.ts");
                    aamMod.learnAssociation?.(`${phrase} ${m.scope}`, Math.abs(bodyMod?.body?.mood ?? 0));
                  } catch {
                  }
                }
              }
            }
          } catch {
          }
          console.log(`[cc-soul][api] feedback: ${(result.memories || []).length} memories`);
        } catch {
        }
        resolve();
      });
    });
    analysisPromise.catch(() => {
    });
  } catch (e) {
    console.log(`[cc-soul][api] feedback error: ${e.message}`);
  }
  try {
    const { hebbianUpdate } = await import("./aam.ts");
    const { decayAllActivations } = await import("./activation-field.ts");
    decayAllActivations(0.995);
    if (qualityScore > 6) {
      hebbianUpdate({ lexical: 0.5, temporal: 0.3, emotional: 0.3, entity: 0.3, behavioral: 0.2, factual: 0.4, causal: 0.2, sequence: 0.2 }, true);
    } else if (qualityScore >= 0 && qualityScore < 4) {
      hebbianUpdate({ lexical: 0.5, temporal: 0.3, emotional: 0.3, entity: 0.3, behavioral: 0.2, factual: 0.4, causal: 0.2, sequence: 0.2 }, false);
    }
  } catch {
  }
  try {
    const { feedbackDistillQuality, feedbackMemoryEngagement } = await import("./handler-augments.ts");
    if (qualityScore >= 0) feedbackDistillQuality(qualityScore);
    feedbackMemoryEngagement(userMessage, userId);
    try {
      const aamMod = await import("./aam.ts");
      aamMod.learnTemporalLink?.(userMessage);
    } catch {
    }
  } catch {
  }
  try {
    const isMemoryStale = (mem) => {
      if (!turnSnapshot || !mem.memoryId) return false;
      const snapLen = turnSnapshot.get(mem.memoryId);
      return snapLen !== void 0 && (mem.lineage?.length ?? 0) !== snapLen;
    };
    const UPDATE_SIGNALS = [
      /(?:之前|以前).*?(?:现在|目前|最近)/,
      // "之前X现在Y" → 事实变化
      /(?:不过|但是).*?(?:看来|似乎|好像)/,
      // "不过看来X" → 修正
      /(?:原来|其实).*?(?:是|应该是)/
      // "原来是X" → 纠正
    ];
    const { memoryState } = await import("./memory.ts");
    const { penalizeTruthfulness } = await import("./smart-forget.ts");
    const { findMentionedEntities } = await import("./graph.ts");
    const { getLastAugmentSnapshot } = await import("./metacognition.ts");
    const injected = getLastAugmentSnapshot();
    for (const signal of UPDATE_SIGNALS) {
      if (!signal.test(aiReply)) continue;
      for (const augContent of injected) {
        const memEntities = findMentionedEntities(augContent);
        const replyMentionsEntity = memEntities.some((e) => aiReply.includes(e));
        if (replyMentionsEntity) {
          const mem = memoryState.memories.find(
            (m) => m && m.content && augContent.includes(m.content.slice(0, 30))
          );
          if (mem) {
            if (isMemoryStale(mem)) continue;
            const penalizeKey = mem.memoryId || (mem.content || "").slice(0, 30);
            const lastTs = _lastPenalizeTs.get(penalizeKey) ?? 0;
            if (Date.now() - lastTs < 5e3) continue;
            _lastPenalizeTs.set(penalizeKey, Date.now());
            if (_lastPenalizeTs.size > 100) {
              let oldest = Infinity, oldestKey = "";
              for (const [k, v] of _lastPenalizeTs) {
                if (v < oldest) {
                  oldest = v;
                  oldestKey = k;
                }
              }
              if (oldestKey) _lastPenalizeTs.delete(oldestKey);
            }
            penalizeTruthfulness(mem, "AI \u56DE\u590D\u6697\u793A\u4FEE\u6B63");
            try {
              const { logDecision } = require("./decision-log.ts");
              logDecision("active_reconstruct", (mem.content || "").slice(0, 30), `AI\u56DE\u590D\u542B\u4FEE\u6B63\u4FE1\u53F7`);
            } catch {
            }
          }
          break;
        }
      }
      break;
    }
  } catch {
  }
  try {
    const { updateQualityFromEngagement } = await import("./quality.ts");
    if (qualityScore >= 0) {
      updateQualityFromEngagement(userMessage, aiReply, qualityScore / 10);
    }
  } catch {
  }
  try {
    const { recordObservation } = await import("./behavioral-phase-space.ts");
    const { getSessionState, getLastActiveSessionKey } = await import("./handler-state.ts");
    const { body: bodyState } = await import("./body.ts");
    const sess = getSessionState(getLastActiveSessionKey());
    const reaction = satisfaction === "positive" ? "satisfied" : satisfaction === "negative" ? "corrected" : "neutral";
    recordObservation(userMessage, bodyState.mood, sess, reaction, "balanced");
  } catch {
  }
  return { learned: true };
}
