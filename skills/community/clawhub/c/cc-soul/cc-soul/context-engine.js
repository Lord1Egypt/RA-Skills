import { buildSoulPrompt } from "./prompt-builder.ts";
import { memoryState, addMemory, addMemoryWithEmotion, parseMemoryCommands, executeMemoryCommands, recall } from "./memory.ts";
import { bodyOnPositiveFeedback } from "./body.ts";
import { addEntitiesFromAnalysis } from "./graph.ts";
import { runPostResponseAnalysis, setAgentBusy, killGatewayClaude } from "./cli.ts";
import { notifyOwnerDM } from "./notify.ts";
import { taskState } from "./tasks.ts";
import { trackQuality } from "./quality.ts";
import { getSessionState, getLastActiveSessionKey } from "./handler-state.ts";
let trackPersonaStyle = () => {
};
let updateBeliefFromMessage = () => {
};
let trackRecallImpact = () => {
};
let getActivePersona = () => null;
import("./persona-drift.ts").then((m) => {
  trackPersonaStyle = m.trackPersonaStyle;
}).catch((e) => {
  console.error(`[cc-soul] module load failed (persona-drift): ${e.message}`);
});
import("./person-model.ts").then((m) => {
  updateBeliefFromMessage = m.updateBeliefFromMessage;
}).catch((e) => {
  console.error(`[cc-soul] module load failed (person-model/tom): ${e.message}`);
});
import("./memory.ts").then((m) => {
  trackRecallImpact = m.trackRecallImpact;
}).catch((e) => {
  console.error(`[cc-soul] module load failed (memory): ${e.message}`);
});
import("./persona.ts").then((m) => {
  getActivePersona = m.getActivePersona;
}).catch((e) => {
  console.error(`[cc-soul] module load failed (persona): ${e.message}`);
});
function syncResponseToSession(sessionKey, content) {
  try {
    const sk = sessionKey || getLastActiveSessionKey();
    const sess = getSessionState(sk);
    if (sess) sess.lastResponseContent = content;
  } catch (_) {
  }
}
const _state = {
  lastUserMsg: "",
  lastBotResponse: "",
  lastSenderId: "",
  lastAugments: [],
  _sessionFile: ""
};
function setLastSenderId(id) {
  _state.lastSenderId = id;
}
function setLastAugments(augments) {
  _state.lastAugments = augments;
}
let statsAccessor = () => ({
  totalMessages: 0,
  corrections: 0,
  firstSeen: Date.now()
});
function setStatsAccessor(fn) {
  statsAccessor = fn;
}
function createCcSoulContextEngine() {
  return {
    info: {
      id: "cc-soul",
      name: "cc-soul Context Engine",
      version: "1.3.0",
      ownsCompaction: false
      // delegate compaction to OpenClaw runtime
    },
    async bootstrap(_params) {
      console.log(`[cc-soul][context-engine] bootstrap`);
      _state._sessionFile = _params.sessionFile;
      return { bootstrapped: true };
    },
    async ingest(params) {
      if (params.message.role === "user" && typeof params.message.content === "string") {
        _state.lastUserMsg = params.message.content;
      }
      if (params.message.role === "assistant" && typeof params.message.content === "string") {
        _state.lastBotResponse = params.message.content;
        syncResponseToSession(params.sessionKey, params.message.content);
      }
      return { ingested: true };
    },
    async ingestBatch(params) {
      for (const msg of params.messages) {
        if (msg.role === "user" && typeof msg.content === "string") _state.lastUserMsg = msg.content;
        if (msg.role === "assistant" && typeof msg.content === "string") _state.lastBotResponse = msg.content;
      }
      return { ingestedCount: params.messages.length };
    },
    /**
     * afterTurn — always fires after a turn, solving message:sent unreliability.
     */
    async afterTurn(params) {
      setAgentBusy(false);
      killGatewayClaude();
      if (params.isHeartbeat) return;
      if (!_state.lastUserMsg || !_state.lastBotResponse) {
        if (params.messages?.length > 0) {
          for (let i = params.messages.length - 1; i >= 0; i--) {
            const m = params.messages[i];
            let text = "";
            if (typeof m.content === "string") {
              text = m.content;
            } else if (Array.isArray(m.content)) {
              text = m.content.filter((p) => p?.type === "text").map((p) => p.text || "").join(" ");
            }
            if (!text) continue;
            if (m.role === "assistant" && !_state.lastBotResponse) {
              _state.lastBotResponse = text;
            }
            if (m.role === "user" && !_state.lastUserMsg) {
              const cleaned = text.replace(/^Conversation info[\s\S]*?```\n*/m, "").replace(/^Sender[\s\S]*?```\n*/m, "").trim();
              if (cleaned) _state.lastUserMsg = cleaned;
            }
            if (_state.lastUserMsg && _state.lastBotResponse) break;
          }
        }
      }
      if (!_state.lastUserMsg || !_state.lastBotResponse) return;
      const userMsg = _state.lastUserMsg;
      const botResponse = _state.lastBotResponse;
      _afterTurnCalled = true;
      console.log(`[cc-soul][context-engine] afterTurn: post-response analysis (${userMsg.slice(0, 30)}...)`);
      const LEAK_PATTERNS = [
        /^.*?(?:用户说|用户在|用户想|用户需要|用户问).{2,30}(?:这是|说明|表明|意味)/m,
        /^.*?这是(?:一个|在).{2,20}(?:请求|时刻|场景|测试|信号)/m,
        /^.*?我应该(?:先|表示|给予|提供)/m
      ];
      for (const pat of LEAK_PATTERNS) {
        if (pat.test(botResponse)) {
          console.error(`[cc-soul][LEAK] \u68C0\u6D4B\u5230\u56DE\u590D\u6CC4\u6F0F\u5185\u90E8\u5206\u6790: "${botResponse.match(pat)?.[0]?.slice(0, 60)}"`);
          try {
            (await import("./decision-log.ts")).logDecision("response_leak", botResponse.match(pat)?.[0]?.slice(0, 40) || "?", `pattern=${pat.source.slice(0, 30)}`);
          } catch {
          }
          break;
        }
      }
      try {
        const { getSessionState: getSessionState2, getLastActiveSessionKey: getLastActiveSessionKey2 } = await import("./handler-state.ts");
        const sk = getLastActiveSessionKey2();
        const sess = getSessionState2(sk);
        if (sess) {
          sess.lastResponseContent = botResponse;
        }
      } catch {
      }
      try {
        const { selfCheckSync } = await import("./quality.ts");
        const { scoreResponse } = await import("./quality.ts");
        if (userMsg.length > 5 && botResponse.length > 20) {
          const selfIssue = selfCheckSync(userMsg, botResponse);
          if (selfIssue) {
            const scScore = scoreResponse(userMsg, botResponse);
            if (scScore <= 3) {
              notifyOwnerDM(`\u26A0\uFE0F \u521A\u624D\u7684\u56DE\u7B54\u53EF\u80FD\u6709\u8BEF\uFF1A${selfIssue}\u3002\u8BC4\u5206 ${scScore}/10`).catch(() => {
              });
              console.log(`[cc-soul][self-correction] issue: ${selfIssue} (score=${scScore})`);
            }
          }
        }
      } catch {
      }
      try {
        const { checkPersonaDrift } = await import("./persona-drift.ts");
        const { getActivePersona: getActivePersona2 } = await import("./persona.ts");
        const persona = getActivePersona2();
        if (persona) {
          checkPersonaDrift(botResponse, persona.id, persona.name, persona.tone, persona.idealVector);
        }
      } catch {
      }
      try {
        const { recordTurnUsage } = await import("./cost-tracker.ts");
        recordTurnUsage(userMsg, botResponse, 0);
      } catch {
      }
      try {
        const { brain } = await import("./brain.ts");
        brain.fire("onSent", { userMessage: userMsg, botReply: botResponse, senderId: _state.lastSenderId });
      } catch {
      }
      {
        const memCommands = parseMemoryCommands(botResponse);
        if (memCommands.length > 0) {
          executeMemoryCommands(memCommands, _state.lastSenderId);
        }
      }
      runPostResponseAnalysis(userMsg, botResponse, (result) => {
        for (const m of result.memories) {
          addMemoryWithEmotion(m.content, m.scope, _state.lastSenderId, m.visibility, void 0, result.emotion, true);
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
              if (deleted > 0) console.log(`[cc-soul][memory-ops] DELETE ${deleted} (keyword: ${op.keyword}, reason: ${op.reason})`);
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
        if (result.satisfaction === "POSITIVE") bodyOnPositiveFeedback();
        trackQuality(result.quality.score);
        if (result.reflection) addMemory(`[\u53CD\u601D] ${result.reflection}`, "reflection", _state.lastSenderId, "private");
        console.log(`[cc-soul][context-engine] afterTurn complete: sat=${result.satisfaction} q=${result.quality.score}`);
        try {
          trackPersonaStyle(botResponse, getActivePersona()?.id ?? "default");
        } catch (_) {
        }
        try {
          updateBeliefFromMessage(userMsg, botResponse);
        } catch (_) {
        }
        try {
          trackRecallImpact([], result.quality.score);
        } catch (_) {
        }
      });
      _state.lastUserMsg = "";
      _state.lastBotResponse = "";
    },
    /**
     * assemble — inject soul prompt as systemPromptAddition (first-class, never truncated).
     */
    async assemble(params) {
      console.log("[cc-soul][context-engine] \u2605\u2605\u2605 assemble() CALLED \u2605\u2605\u2605");
      const s = statsAccessor();
      const soulPrompt = buildSoulPrompt(
        s.totalMessages,
        s.corrections,
        s.firstSeen,
        taskState.workflows
      );
      if (!_state.lastUserMsg && params.messages?.length > 0) {
        for (let i = params.messages.length - 1; i >= 0; i--) {
          const m = params.messages[i];
          if (m.role !== "user") continue;
          let text = "";
          if (typeof m.content === "string") {
            text = m.content;
          } else if (Array.isArray(m.content)) {
            text = m.content.filter((p) => p?.type === "text").map((p) => p.text || "").join(" ");
          }
          if (text.length > 0) {
            let cleaned = text;
            const lastBacktick = text.lastIndexOf("```");
            if (lastBacktick !== -1) {
              cleaned = text.slice(lastBacktick + 3).trim();
            }
            cleaned = cleaned.replace(/^\[message_id:\s*\S+\]\s*/i, "");
            cleaned = cleaned.replace(/^[a-zA-Z0-9_\u4e00-\u9fff]{1,20}:\s/, "");
            cleaned = cleaned.trim();
            if (cleaned) {
              _state.lastUserMsg = cleaned;
              break;
            }
          }
        }
        if (_state.lastUserMsg) {
          console.log(`[cc-soul][context-engine] assemble: extracted lastUserMsg="${_state.lastUserMsg.slice(0, 40)}"`);
          try {
            const { routeCommandDirect, wasHandledByDirect } = await import("./handler-commands.ts");
            if (typeof routeCommandDirect === "function") {
              const rawMsg = _state.lastUserMsg.replace(/^\[message_id:\s*\S+\]\s*/i, "").replace(/^[a-zA-Z0-9_\u4e00-\u9fff]{1,20}:\s/, "").trim();
              if (!wasHandledByDirect(rawMsg)) {
                routeCommandDirect(rawMsg, params);
              }
            }
          } catch (_) {
          }
        }
      }
      let augmentsToUse = _state.lastAugments;
      if (_state.lastUserMsg) {
        try {
          let _ceHints = null;
          try {
            _ceHints = require("./cognition.ts").toCogHints(_state.lastUserMsg);
          } catch {
          }
          const recalled = recall(_state.lastUserMsg, 8, _state.lastSenderId || void 0, void 0, void 0, void 0, _ceHints);
          if (recalled.length > 0) {
            const memAugment = "[\u76F8\u5173\u8BB0\u5FC6] " + recalled.map((m) => {
              const emotionTag = m.emotion && m.emotion !== "neutral" ? ` (${m.emotion})` : "";
              return m.content.slice(0, 80) + emotionTag;
            }).join("\uFF1B");
            augmentsToUse = augmentsToUse.filter((a) => !/^\[记忆\]|\[相关记忆\]|\[相关事实\]/.test(a));
            augmentsToUse.push(memAugment);
            console.log(`[cc-soul][context-engine] assemble: sync recall injected ${recalled.length} memories for "${_state.lastUserMsg.slice(0, 30)}"`);
          }
        } catch {
        }
      }
      const cleanedAugments = augmentsToUse.map((a) => {
        let c = a.replace(/^\[([^\]]+)\]\s*/, "");
        c = c.replace(/^用户(说了?|提到|指出|表示|认为|觉得|想要|需要|在|的|问)/g, "\u4F60$1");
        c = c.replace(/用户(情绪|心情|状态|风格|偏好)/g, "\u4F60\u7684$1");
        c = c.replace(/该用户/g, "\u8FD9\u4E2A\u4EBA");
        c = c.replace(/当前用户/g, "\u5BF9\u65B9");
        c = c.replace(/^(检测到|发现|分析|注意到|观察到|识别到)\s*/g, "");
        return c;
      });
      const parts = [soulPrompt];
      if (cleanedAugments.length > 0) {
        parts.push(cleanedAugments.join("\n"));
      }
      const fullPrompt = parts.join("\n\n");
      console.log(`[cc-soul][context-engine] assemble: ${soulPrompt.length} chars soul + ${augmentsToUse.length} augments = ${fullPrompt.length} chars total`);
      if (augmentsToUse.length > 0) {
        console.log(`[cc-soul][context-engine] augment preview: ${augmentsToUse.map((a) => a.slice(0, 60)).join(" | ")}`);
        const hasMemory = augmentsToUse.some((a) => a.includes("[\u76F8\u5173\u8BB0\u5FC6]"));
        console.log(`[cc-soul][context-engine] assemble: has [\u76F8\u5173\u8BB0\u5FC6]=${hasMemory}`);
      }
      return {
        messages: params.messages,
        estimatedTokens: 0,
        systemPromptAddition: fullPrompt
      };
    },
    /**
     * compact — delegate to runtime with soul-aware instructions.
     */
    async compact(params) {
      const coreHints = memoryState.memories.filter((m) => m.scope === "core" || m.scope === "important").slice(0, 10).map((m) => m.content.slice(0, 50)).join("; ");
      const soulInstructions = coreHints ? `IMPORTANT: Preserve these key user facts during compaction: ${coreHints}` : void 0;
      const merged = [params.customInstructions, soulInstructions].filter(Boolean).join("\n\n");
      try {
        const mod = await import("openclaw/plugin-sdk");
        return await mod.delegateCompactionToRuntime({
          ...params,
          customInstructions: merged || params.customInstructions
        });
      } catch {
        console.log("[cc-soul][context-engine] delegateCompactionToRuntime unavailable");
        return { ok: true, compacted: false, reason: "delegate unavailable" };
      }
    },
    async dispose() {
      console.log("[cc-soul][context-engine] dispose");
      if (!_state.lastBotResponse && _state._sessionFile) {
        try {
          const { readFileSync, existsSync } = await import("fs");
          if (existsSync(_state._sessionFile)) {
            const lines = readFileSync(_state._sessionFile, "utf-8").split("\n").filter((l) => l.trim());
            for (let i = lines.length - 1; i >= 0; i--) {
              try {
                const entry = JSON.parse(lines[i]);
                if (entry?.type === "message" && entry?.message?.role === "assistant") {
                  const content = entry.message.content;
                  if (typeof content === "string") {
                    _state.lastBotResponse = content;
                  } else if (Array.isArray(content)) {
                    const texts = content.filter((p) => p?.type === "text").map((p) => p.text || "");
                    _state.lastBotResponse = texts.join(" ");
                  }
                  if (_state.lastBotResponse) break;
                }
              } catch (_) {
              }
            }
            if (_state.lastBotResponse) {
              console.log(`[cc-soul][context-engine] dispose: recovered bot response from session (${_state.lastBotResponse.length} chars)`);
            }
          }
        } catch (_) {
        }
      }
      if (_state.lastUserMsg && _state.lastBotResponse) {
        console.log(`[cc-soul][context-engine] dispose: triggering afterTurn fallback (user=${_state.lastUserMsg.slice(0, 30)}, bot=${_state.lastBotResponse.slice(0, 30)})`);
        const userMsg = _state.lastUserMsg;
        const botResponse = _state.lastBotResponse;
        {
          const memCommands = parseMemoryCommands(botResponse);
          if (memCommands.length > 0) {
            executeMemoryCommands(memCommands, _state.lastSenderId);
          }
        }
        runPostResponseAnalysis(userMsg, botResponse, (result) => {
          for (const m of result.memories) {
            addMemoryWithEmotion(m.content, m.scope, _state.lastSenderId, m.visibility, void 0, result.emotion, true);
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
                    mem.content = op.newContent;
                    mem.ts = Date.now();
                    mem.tags = void 0;
                    break;
                  }
                }
              }
            }
          }
          if (result.satisfaction === "POSITIVE") bodyOnPositiveFeedback();
          trackQuality(result.quality.score);
          if (result.reflection) addMemory(`[\u53CD\u601D] ${result.reflection}`, "reflection", _state.lastSenderId, "private");
          console.log(`[cc-soul][context-engine] dispose-afterTurn complete: sat=${result.satisfaction} q=${result.quality.score}`);
          try {
            trackPersonaStyle(botResponse, getActivePersona()?.id ?? "default");
          } catch (_) {
          }
          try {
            updateBeliefFromMessage(userMsg, botResponse);
          } catch (_) {
          }
        });
        _state.lastUserMsg = "";
        _state.lastBotResponse = "";
      }
    }
  };
}
let _registered = false;
let _afterTurnCalled = false;
async function tryRegisterContextEngine() {
  if (_registered) return true;
  try {
    const { registerContextEngine } = await import("openclaw/plugin-sdk");
    const result = registerContextEngine("cc-soul", () => createCcSoulContextEngine());
    if (result.ok) {
      _registered = true;
      console.log("[cc-soul][context-engine] \u2705 registered as Context Engine");
      return true;
    }
    console.log(`[cc-soul][context-engine] registration blocked: ${result.existingOwner}`);
    return false;
  } catch (e) {
    console.log(`[cc-soul][context-engine] not available (${e.message?.slice(0, 60)}), hook mode`);
    return false;
  }
}
function isContextEngineActive() {
  return _registered && _afterTurnCalled;
}
function isContextEngineRegistered() {
  return _registered;
}
export {
  createCcSoulContextEngine,
  isContextEngineActive,
  isContextEngineRegistered,
  setLastAugments,
  setLastSenderId,
  setStatsAccessor,
  tryRegisterContextEngine
};
