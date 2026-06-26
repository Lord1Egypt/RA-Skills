import { spawnCLI } from "./cli.ts";
import { memoryState, addMemory } from "./memory.ts";
import { extractJSON } from "./utils.ts";
import { getParam } from "./auto-tune.ts";
import { isEndSignal as dynamicIsEndSignal } from "./dynamic-extractor.ts";
const _frustrationHistory = /* @__PURE__ */ new Map();
function computeFrustrationDynamics(flowKey, msgLength, prevMsgLength, turnCount, hasQuestionMark, hasNegativeWords) {
  if (!_frustrationHistory.has(flowKey)) _frustrationHistory.set(flowKey, []);
  const history = _frustrationHistory.get(flowKey);
  let signal = 0;
  if (prevMsgLength > 0 && msgLength < prevMsgLength * 0.5) signal += 0.2;
  if (hasQuestionMark && turnCount > 3) signal += 0.15;
  if (hasNegativeWords) signal += 0.3;
  signal += Math.min(0.15, turnCount * 0.02);
  if (msgLength > prevMsgLength * 1.2) signal -= 0.15;
  if (!hasQuestionMark && !hasNegativeWords) signal -= 0.05;
  signal = Math.max(-0.2, Math.min(0.5, signal));
  history.push(signal);
  if (history.length > 50) history.splice(0, history.length - 50);
  if (_frustrationHistory.size > 200) {
    const keys = [..._frustrationHistory.keys()];
    for (let i = 0; i < 100; i++) _frustrationHistory.delete(keys[i]);
  }
  let current = 0;
  let weight = 1;
  for (let i = history.length - 1; i >= 0; i--) {
    current += history[i] * weight;
    weight *= 0.7;
  }
  current = Math.max(0, Math.min(1, current));
  const recentSlice = history.slice(-3);
  const velocity = recentSlice.length >= 2 ? (recentSlice[recentSlice.length - 1] - recentSlice[0]) / recentSlice.length : 0;
  let turnsToAbandon = null;
  if (current > 0.3 && velocity > 0) {
    turnsToAbandon = Math.ceil((0.8 - current) / velocity);
    if (turnsToAbandon > 10 || turnsToAbandon < 0) turnsToAbandon = null;
  }
  return { current, velocity, turnsToAbandon };
}
let _coupledPressure = {
  frustration: 0,
  frustrationVelocity: 0,
  stress: 0,
  stressVelocity: 0,
  couplingStrength: 0.3,
  // 初始弱耦合（不是 0，让系统有机会发现耦合关系）
  phase: "calm",
  turnsToBreakdown: null
};
function updateCoupledPressure(frustrationSignal, stressSignals) {
  const p = _coupledPressure;
  const effectiveFrustration = frustrationSignal * (1 + p.stress * p.couplingStrength);
  p.frustration = Math.max(0, Math.min(1, p.frustration * 0.9 + effectiveFrustration * 0.3));
  p.frustrationVelocity = effectiveFrustration;
  let stressForce = 0;
  if (stressSignals.msgLen < 10) stressForce += 0.15;
  if (stressSignals.hasNegWord) stressForce += 0.25;
  if (stressSignals.timeSinceLastMsg < 1e4) stressForce += 0.1;
  const effectiveStressForce = stressForce + p.frustration * p.couplingStrength * 0.1;
  const k = 0.15, \u03B3 = 0.3;
  p.stressVelocity += -k * p.stress + effectiveStressForce - \u03B3 * p.stressVelocity;
  p.stress = Math.max(0, Math.min(1, p.stress + p.stressVelocity));
  p.stressVelocity = Math.max(-0.5, Math.min(0.5, p.stressVelocity));
  if (p.frustration > 0.5 && p.stress > 0.5) {
    p.couplingStrength = Math.min(1, p.couplingStrength + 0.05);
  } else {
    p.couplingStrength = Math.max(0.1, p.couplingStrength * 0.99);
  }
  const prevPhase = p.phase;
  const maxPressure = Math.max(p.frustration, p.stress);
  if (maxPressure > 0.7) p.phase = "critical";
  else if (maxPressure > 0.4 && (p.frustrationVelocity > 0 || p.stressVelocity > 0)) p.phase = "building";
  else if (maxPressure > 0.3 && p.stressVelocity < -0.05) p.phase = "recovering";
  else p.phase = "calm";
  if (p.phase !== prevPhase) {
    try {
      const { emitCacheEvent } = require("./memory-utils.ts");
      emitCacheEvent("emotion_shifted");
    } catch {
    }
  }
  if (p.phase === "critical") {
    p.turnsToBreakdown = 0;
  } else {
    const maxVelocity = Math.max(p.frustrationVelocity, p.stressVelocity);
    if (maxVelocity > 0.03 && maxPressure > 0.3) {
      p.turnsToBreakdown = Math.ceil((0.8 - maxPressure) / maxVelocity);
      if (p.turnsToBreakdown > 10 || p.turnsToBreakdown < 0) p.turnsToBreakdown = null;
    } else {
      p.turnsToBreakdown = null;
    }
  }
  return { ...p };
}
function getCoupledPressure() {
  return { ..._coupledPressure };
}
function getCoupledPressureContext() {
  const p = _coupledPressure;
  if (p.phase === "calm" && p.frustration < 0.15 && p.stress < 0.15) return null;
  const parts = [];
  if (p.phase !== "calm") parts.push(`\u538B\u529B\u9636\u6BB5\uFF1A${p.phase}`);
  if (p.frustration > 0.3) parts.push(`\u632B\u8D25\u611F${(p.frustration * 100).toFixed(0)}%`);
  else if (p.frustration > 0.15) parts.push(`\u8F7B\u5FAE\u53D7\u632B`);
  if (p.stress > 0.3) parts.push(`\u957F\u671F\u538B\u529B${(p.stress * 100).toFixed(0)}%`);
  else if (p.stress > 0.15) parts.push(`\u6709\u70B9\u75B2\u60EB`);
  if (p.couplingStrength > 0.5) parts.push(`\u538B\u529B\u8026\u5408\u5F3A`);
  if (p.turnsToBreakdown === 0) parts.push(`\u5DF2\u4E34\u754C\uFF0C\u7ACB\u5373\u5E72\u9884`);
  else if (p.turnsToBreakdown !== null) parts.push(`\u9884\u8BA1${p.turnsToBreakdown}\u8F6E\u540E\u4E34\u754C`);
  if (parts.length === 0 && (p.frustration > 0.1 || p.stress > 0.1)) {
    parts.push("\u60C5\u7EEA\uFF1A\u7565\u4F4E");
  }
  if (parts.length === 0) return null;
  return `[\u538B\u529B\u52A8\u6001] ${parts.join("\uFF0C")}`;
}
let _eventSegments = [];
let _currentEvent = null;
function updateEventSegment(userMsg, topic, flowKey) {
  const now = Date.now();
  const isEndSignal = dynamicIsEndSignal(userMsg);
  if (_currentEvent) {
    const timeSinceLastUpdate = now - _currentEvent.endTs;
    const topicChanged = _currentEvent.topic !== topic && topic !== "general";
    if (isEndSignal) {
      _currentEvent.outcome = "resolved";
      _currentEvent.endTs = now;
      _currentEvent = null;
    } else if (timeSinceLastUpdate > 30 * 60 * 1e3) {
      _currentEvent.outcome = _currentEvent.turnCount > 5 ? "unresolved" : "abandoned";
      _currentEvent.endTs = now;
      _currentEvent = null;
    } else if (topicChanged) {
      _currentEvent.outcome = "unresolved";
      _currentEvent.endTs = now;
      const oldId = _currentEvent.id;
      _currentEvent = null;
      startNewEvent(topic, now);
      if (_currentEvent) {
        _currentEvent.causalLinks.push({ targetEventId: oldId, type: "led_to" });
      }
      return;
    } else {
      _currentEvent.endTs = now;
      _currentEvent.turnCount++;
      _currentEvent.memoryKeys.push(userMsg.slice(0, 40) + "|" + now);
      if (_currentEvent.memoryKeys.length > 20) _currentEvent.memoryKeys = _currentEvent.memoryKeys.slice(-20);
      return;
    }
  }
  if (!_currentEvent) startNewEvent(topic, now);
}
function startNewEvent(topic, ts) {
  _currentEvent = {
    id: `evt_${ts}_${Math.random().toString(36).slice(2, 6)}`,
    topic,
    memoryKeys: [],
    startTs: ts,
    endTs: ts,
    outcome: "ongoing",
    causalLinks: [],
    turnCount: 1
  };
  _eventSegments.push(_currentEvent);
  if (_eventSegments.length > 100) _eventSegments = _eventSegments.slice(-100);
}
function getCurrentEvent() {
  return _currentEvent;
}
function getRecentEvents(n = 5) {
  return _eventSegments.slice(-n);
}
function searchEvents(query) {
  const words = new Set((query.match(/[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}/gi) || []).map((w) => w.toLowerCase()));
  return _eventSegments.filter((e) => {
    const topicWords = new Set((e.topic.match(/[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}/gi) || []).map((w) => w.toLowerCase()));
    let overlap = 0;
    for (const w of words) if (topicWords.has(w)) overlap++;
    return overlap > 0;
  }).slice(-5);
}
const lastResolvedFlows = /* @__PURE__ */ new Map();
function createEmptyFlow() {
  return {
    topic: "",
    turnCount: 0,
    frustration: 0,
    resolved: false,
    depth: "shallow",
    lastMsgLengths: [],
    topicKeywords: [],
    lastUpdate: Date.now()
  };
}
const flows = /* @__PURE__ */ new Map();
const MAX_FLOWS = 50;
let onSessionResolved = null;
function setOnSessionResolved(cb) {
  onSessionResolved = cb;
}
function updateFlow(userMsg, botResponse, flowKey) {
  let flow = flows.get(flowKey) || createEmptyFlow();
  const msgWords = (userMsg.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map((w) => w.toLowerCase());
  const overlap = flow.topicKeywords.filter((w) => msgWords.includes(w)).length;
  const isSameTopic = overlap >= 2 || flow.turnCount > 0 && overlap >= 1 && userMsg.length < 50;
  if (isSameTopic) {
    flow.turnCount++;
    for (const w of msgWords.slice(0, 5)) {
      if (!flow.topicKeywords.includes(w)) flow.topicKeywords.push(w);
    }
    if (flow.topicKeywords.length > 15) flow.topicKeywords = flow.topicKeywords.slice(-10);
    try {
      const { learnEndSignal } = require("./dynamic-extractor.ts");
      const prevMsg = flow.topicKeywords.join(" ");
      learnEndSignal(prevMsg, "continue");
    } catch {
    }
  } else {
    try {
      const { learnEndSignal } = require("./dynamic-extractor.ts");
      learnEndSignal(userMsg, "topic_switch");
    } catch {
    }
    flow = {
      topic: userMsg.slice(0, 50),
      turnCount: 1,
      frustration: 0,
      resolved: false,
      depth: "shallow",
      lastMsgLengths: [],
      topicKeywords: msgWords.slice(0, 8),
      lastUpdate: Date.now()
    };
  }
  flow.lastMsgLengths.push(userMsg.length);
  if (flow.lastMsgLengths.length > 5) flow.lastMsgLengths.shift();
  if (flow.lastMsgLengths.length >= 3) {
    const lengths = flow.lastMsgLengths;
    const trend = lengths[lengths.length - 1] - lengths[0];
    if (trend < -50) flow.frustration = Math.min(1, flow.frustration + getParam("flow.frustration_shortening_rate"));
    if (userMsg.length < 10 && flow.turnCount > 3) flow.frustration = Math.min(1, flow.frustration + getParam("flow.frustration_terse"));
  }
  if (["\u7B97\u4E86", "\u4E0D\u5BF9", "\u8FD8\u662F\u4E0D\u884C", "\u600E\u4E48\u53C8", "\u8BF4\u4E86\u591A\u5C11\u904D", "forget it", "still not working", "why again", "how many times"].some((w) => userMsg.toLowerCase().includes(w))) {
    flow.frustration = Math.min(1, flow.frustration + getParam("flow.frustration_keyword_rate"));
  }
  const questionMarks = (userMsg.match(/[？?]/g) || []).length;
  if (questionMarks >= 2) {
    flow.frustration = Math.min(1, flow.frustration + getParam("flow.frustration_question_rate") * questionMarks);
  }
  if (flow.turnCount >= 2 && flow.topicKeywords.length > 0) {
    const repeated = msgWords.filter((w) => flow.topicKeywords.includes(w)).length;
    const repeatRatio = repeated / Math.max(1, msgWords.length);
    if (repeatRatio > 0.6 && flow.turnCount > 3) {
      flow.frustration = Math.min(1, flow.frustration + getParam("flow.frustration_repetition"));
    }
  }
  if (flow.lastMsgLengths.length > 0) {
    flow.frustration = Math.max(0, flow.frustration - getParam("flow.frustration_decay_per_turn"));
  }
  const prevMsgLen = flow.lastMsgLengths.length >= 2 ? flow.lastMsgLengths[flow.lastMsgLengths.length - 2] : 0;
  const hasQuestionMark = /[？?]/.test(userMsg);
  const hasNegativeWords = ["\u7B97\u4E86", "\u4E0D\u5BF9", "\u8FD8\u662F\u4E0D\u884C", "\u600E\u4E48\u53C8", "\u8BF4\u4E86\u591A\u5C11\u904D", "\u70E6", "\u7D2F", "annoyed", "tired", "forget it", "whatever", "give up"].some((w) => userMsg.toLowerCase().includes(w));
  flow.frustrationTrajectory = computeFrustrationDynamics(flowKey, userMsg.length, prevMsgLen, flow.turnCount, hasQuestionMark, hasNegativeWords);
  const timeSinceLastMsg = flow.lastMsgLengths.length >= 2 ? Date.now() - flow._lastMsgTs || 3e4 : 3e4;
  flow._lastMsgTs = Date.now();
  updateCoupledPressure(flow.frustrationTrajectory.current, {
    msgLen: userMsg.length,
    hasNegWord: hasNegativeWords,
    timeSinceLastMsg
  });
  if (["\u641E\u5B9A", "\u53EF\u4EE5\u4E86", "\u597D\u4E86", "\u89E3\u51B3\u4E86", "\u8C22\u8C22", "thanks", "\u6210\u529F\u4E86", "fixed", "done", "solved", "got it", "success", "works now"].some((w) => userMsg.toLowerCase().includes(w))) {
    flow.resolved = true;
    flow.frustration = Math.max(0, flow.frustration - 0.3);
    if (typeof onSessionResolved === "function") onSessionResolved();
    if (!lastResolvedFlows.has(flowKey)) {
      lastResolvedFlows.set(flowKey, {
        resolvedAt: Date.now(),
        summarized: false,
        topic: flow.topic,
        turnCount: flow.turnCount
      });
    }
  }
  if (flow.turnCount <= 2) flow.depth = "shallow";
  else if (flow.turnCount <= 6 && flow.frustration < getParam("flow.stuck_threshold")) flow.depth = "deep";
  else if (flow.turnCount > 6 || flow.frustration >= getParam("flow.stuck_threshold")) flow.depth = "stuck";
  flow.lastUpdate = Date.now();
  flows.set(flowKey, flow);
  try {
    const topic = flow.topic || flow.topicKeywords.slice(0, 3).join(" ") || "general";
    updateEventSegment(userMsg, topic, flowKey);
  } catch {
  }
  if (flows.size > MAX_FLOWS) {
    const oldest = [...flows.entries()].sort((a, b) => a[1].lastUpdate - b[1].lastUpdate)[0];
    if (oldest) flows.delete(oldest[0]);
  }
  const OLD_THRESHOLD = 24 * 36e5;
  for (const [key, resolved] of lastResolvedFlows) {
    if (Date.now() - resolved.resolvedAt > OLD_THRESHOLD) {
      lastResolvedFlows.delete(key);
    }
  }
  return flow;
}
function getFlowHints(flowKey) {
  const flow = flows.get(flowKey);
  if (!flow) return [];
  const hints = [];
  if (flow.depth === "stuck") {
    hints.push(`\u5DF2\u7ECF\u8BA8\u8BBA${flow.turnCount}\u8F6E\u4E86\uFF0C\u53EF\u80FD\u9677\u5165\u50F5\u5C40\u3002\u8BD5\u8BD5\u6362\u4E2A\u601D\u8DEF\u6216\u76F4\u63A5\u7ED9\u6700\u7EC8\u65B9\u6848`);
  }
  if (flow.frustration >= 0.6) {
    hints.push("\u7528\u6237\u53EF\u80FD\u8D8A\u6765\u8D8A\u4E0D\u8010\u70E6\u4E86\uFF0C\u7B80\u5316\u56DE\u7B54\uFF0C\u76F4\u63A5\u7ED9\u65B9\u6848");
  }
  if (flow.frustrationTrajectory) {
    const ft = flow.frustrationTrajectory;
    if (ft.turnsToAbandon !== null && ft.turnsToAbandon <= 3) {
      hints.push(`\u26A0 \u9884\u6D4B\u7528\u6237\u53EF\u80FD\u5728${ft.turnsToAbandon}\u8F6E\u5185\u653E\u5F03\uFF0C\u7ACB\u5373\u7ED9\u51FA\u6700\u7EC8\u65B9\u6848`);
    } else if (ft.velocity > 0.1 && ft.current > 0.2) {
      hints.push("\u632B\u8D25\u611F\u6B63\u5728\u5FEB\u901F\u4E0A\u5347\uFF0C\u6CE8\u610F\u8C03\u6574\u7B56\u7565");
    }
  }
  if (flow.resolved) {
    hints.push("\u95EE\u9898\u4F3C\u4E4E\u5DF2\u89E3\u51B3\uFF0C\u81EA\u7136\u6536\u5C3E\u5373\u53EF");
  }
  if (flow.turnCount >= 4 && !flow.resolved && flow.frustration < 0.3) {
    hints.push(`\u8BA8\u8BBA\u5DF2${flow.turnCount}\u8F6E\uFF0C\u7528\u6237\u5F88\u6709\u8010\u5FC3\uFF0C\u53EF\u4EE5\u7EE7\u7EED\u6DF1\u5165`);
  }
  return hints;
}
function getFlowContext(flowKey) {
  const flow = flows.get(flowKey);
  if (!flow || flow.turnCount <= 1) return "";
  return `[\u5BF9\u8BDD\u6D41] \u5F53\u524D\u8BDD\u9898\u5DF2${flow.turnCount}\u8F6E | \u6DF1\u5EA6:${flow.depth} | \u7528\u6237\u8010\u5FC3:${(1 - flow.frustration).toFixed(1)} | ${flow.resolved ? "\u5DF2\u89E3\u51B3" : "\u8FDB\u884C\u4E2D"}`;
}
function getCurrentFlowDepth() {
  let worst = "shallow";
  for (const flow of flows.values()) {
    if (flow.depth === "stuck") return "stuck";
    if (flow.depth === "deep") worst = "deep";
  }
  return worst;
}
function getAvgFrustration() {
  if (flows.size === 0) return 0;
  let sum = 0;
  for (const flow of flows.values()) sum += flow.frustration;
  return Math.round(sum / flows.size * 100) / 100;
}
function getUnresolvedTopics() {
  const topics = [];
  const now = Date.now();
  for (const flow of flows.values()) {
    if (flow.topic && !flow.resolved && now - flow.lastUpdate < 864e5) {
      topics.push(flow.topic);
    }
  }
  return topics;
}
function resetFlow(flowKey) {
  if (flowKey) {
    flows.delete(flowKey);
  } else {
    flows.clear();
  }
}
function checkSessionEnd(flowKey) {
  const resolved = lastResolvedFlows.get(flowKey);
  if (!resolved) return null;
  if (resolved.summarized) return null;
  if (Date.now() - resolved.resolvedAt > 5 * 60 * 1e3) {
    resolved.summarized = true;
    return { ended: true, topic: resolved.topic, turnCount: resolved.turnCount };
  }
  return null;
}
function checkAllSessionEnds() {
  const ended = [];
  for (const [key] of lastResolvedFlows) {
    const result = checkSessionEnd(key);
    if (result) {
      ended.push({ flowKey: key, topic: result.topic, turnCount: result.turnCount });
    }
  }
  return ended;
}
function generateSessionSummary(topic, turnCount, _flowKey) {
  const chatHistory = memoryState.chatHistory;
  const recentHistory = chatHistory.slice(-(turnCount * 2));
  const historyText = recentHistory.map(
    (t) => `\u7528\u6237: ${t.user.slice(0, 100)}
\u52A9\u624B: ${t.assistant.slice(0, 100)}`
  ).join("\n\n");
  spawnCLI(
    `\u4EE5\u4E0B\u662F\u4E00\u6BB5${turnCount}\u8F6E\u7684\u5BF9\u8BDD\uFF08\u8BDD\u9898: ${topic}\uFF09\u3002\u8BF7\u603B\u7ED3\uFF1A
1. \u804A\u4E86\u4EC0\u4E48
2. \u7528\u6237\u6EE1\u610F\u5417
3. \u6709\u6CA1\u6709\u9057\u7559\u95EE\u9898
4. \u503C\u5F97\u8BB0\u4F4F\u7684\u4E8B\u5B9E/\u504F\u597D

${historyText.slice(0, 2e3)}

\u683C\u5F0F: {"summary":"\u4E00\u6BB5\u8BDD\u603B\u7ED3","facts":["\u503C\u5F97\u8BB0\u4F4F\u7684\u4E8B\u5B9E"],"satisfied":true/false,"pending":"\u9057\u7559\u95EE\u9898\u6216null"}`,
    (output) => {
      try {
        const result = extractJSON(output);
        if (result) {
          if (result.summary) {
            addMemory(`[\u4F1A\u8BDD\u603B\u7ED3] ${topic}: ${result.summary}`, "consolidated");
          }
          for (const fact of result.facts || []) {
            addMemory(fact, "fact");
          }
          if (result.pending) {
            addMemory(`[\u9057\u7559\u95EE\u9898] ${result.pending}`, "task");
          }
          console.log(`[cc-soul][session] summarized: ${topic} (${turnCount} turns, satisfied=${result.satisfied})`);
        }
      } catch (e) {
        console.error(`[cc-soul][session] summary parse error: ${e.message}`);
      }
    }
  );
}
const flowModule = {
  id: "flow",
  name: "\u5BF9\u8BDD\u6D41\u7BA1\u7406",
  priority: 50
};
export {
  checkAllSessionEnds,
  checkSessionEnd,
  computeFrustrationDynamics,
  flowModule,
  generateSessionSummary,
  getAvgFrustration,
  getCoupledPressure,
  getCoupledPressureContext,
  getCurrentEvent,
  getCurrentFlowDepth,
  getFlowContext,
  getFlowHints,
  getRecentEvents,
  getUnresolvedTopics,
  resetFlow,
  searchEvents,
  setOnSessionResolved,
  updateCoupledPressure,
  updateEventSegment,
  updateFlow
};
