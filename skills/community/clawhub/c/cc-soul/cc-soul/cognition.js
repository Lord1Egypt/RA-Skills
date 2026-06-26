import { body, bodyOnCorrection, bodyOnPositiveFeedback, emotionVector } from "./body.ts";
import { getProfile, getProfileTier } from "./user-profiles.ts";
import { CORRECTION_WORDS, CORRECTION_EXCLUDE, EMOTION_ALL, EMOTION_NEGATIVE, TECH_WORDS, CASUAL_WORDS } from "./signals.ts";
function attentionGate(msg) {
  const m = msg.toLowerCase();
  const hypotheses = [
    { type: "correction", score: 0 },
    { type: "emotional", score: 0 },
    { type: "technical", score: 0 },
    { type: "casual", score: 0 },
    { type: "general", score: 1 }
    // prior: general is default
  ];
  const correctionHits = CORRECTION_WORDS.filter((w) => m.includes(w)).length;
  const correctionExclude = CORRECTION_EXCLUDE.some((w) => m.includes(w));
  if (correctionHits > 0 && !correctionExclude) {
    hypotheses[0].score += correctionHits * 3;
  }
  const emotionHits = EMOTION_ALL.filter((w) => m.includes(w)).length;
  hypotheses[1].score += emotionHits * 2;
  const techHits = TECH_WORDS.filter((w) => m.includes(w)).length;
  hypotheses[2].score += techHits * 2;
  const casualHits = CASUAL_WORDS.filter((w) => m === w || m === w + "\u7684").length;
  hypotheses[3].score += casualHits * 2;
  if (msg.length < 15) hypotheses[3].score += 1;
  if (msg.length > 100) hypotheses[2].score += 0.5;
  if (msg.length < 8) hypotheses[3].score += 1;
  const negEmotionHits = EMOTION_NEGATIVE.filter((w) => m.includes(w)).length;
  if (negEmotionHits > 0 && techHits > 0) {
    hypotheses[1].score += 1;
  }
  hypotheses.sort((a, b) => b.score - a.score);
  const winner = hypotheses[0];
  const expScores = hypotheses.map((h) => Math.exp(h.score * 2));
  const sumExp = expScores.reduce((s, e) => s + e, 0);
  const winnerProb = expScores[0] / sumExp;
  const priority = Math.min(10, Math.max(1, Math.round(winnerProb * 10)));
  return { type: winner.type, priority };
}
function detectIntent(msg) {
  const m = msg.toLowerCase();
  if (["\u4F60\u89C9\u5F97", "\u4F60\u770B", "\u4F60\u8BA4\u4E3A", "\u4F60\u600E\u4E48\u770B", "\u4F60\u7684\u770B\u6CD5", "\u5EFA\u8BAE", "what do you think", "your opinion", "suggestion", "recommend"].some((w) => m.includes(w))) return "wants_opinion";
  if (["\u987A\u4FBF", "\u53E6\u5916", "\u8FD8\u6709", "\u5BF9\u4E86"].some((w) => m.includes(w))) return "wants_proactive";
  if (m.endsWith("?") || m.endsWith("\uFF1F") || ["\u5417", "\u5462", "\u4E48"].some((w) => m.endsWith(w))) return "wants_answer";
  if (msg.length < 20) return "wants_quick";
  if (["\u505A", "\u5199", "\u6539", "\u5E2E\u6211", "\u5B9E\u73B0", "\u751F\u6210", "do", "write", "change", "fix", "create", "help me"].some((w) => m.includes(w))) return "wants_action";
  return "unclear";
}
function decideStrategy(attention, intent, msgLen) {
  if (attention.type === "correction") return "acknowledge_and_retry";
  if (attention.type === "emotional") return "empathy_first";
  if (intent === "wants_quick" || msgLen < 10) return "direct";
  if (intent === "wants_opinion") return "opinion_with_reasoning";
  if (intent === "wants_action") return "action_oriented";
  if (msgLen > 200) return "detailed";
  return "balanced";
}
function detectImplicitFeedbackSync(msg, prevResponse) {
  if (!prevResponse) return null;
  const m = msg.toLowerCase();
  if (prevResponse.length > 500 && msg.length < 10 && ["\u55EF", "\u597D", "\u884C", "\u54E6", "ok"].some((w) => m.includes(w))) {
    return "too_verbose";
  }
  if (["\u55EF", "\u597D\u7684", "\u660E\u767D", "\u4E86\u89E3", "ok", "\u6536\u5230", "\u53EF\u4EE5", "\u597D", "sure", "got it", "understood", "alright"].some((w) => m === w)) {
    return "silent_accept";
  }
  if (["\u592A\u597D\u4E86", "\u725B", "\u5389\u5BB3", "\u5B8C\u7F8E", "\u6B63\u662F", "\u5BF9\u5BF9\u5BF9", "\u5C31\u662F\u8FD9\u4E2A", "\u611F\u8C22", "great", "perfect", "exactly", "that's it", "thanks"].some((w) => m.includes(w))) {
    return "positive";
  }
  return null;
}
function computeIntentSpectrum(msg) {
  const len = msg.length;
  const spectrum = { information: 0.3, action: 0.1, emotional: 0.1, validation: 0.1, exploration: 0.1 };
  const infoSignals = (msg.match(/什么|怎么|为什么|哪个|多少|是不是|如何|区别|对比|原理|what|how|why|which|explain|difference|compare/gi) || []).length;
  spectrum.information = Math.min(1, 0.2 + infoSignals * 0.2);
  const actionSignals = (msg.match(/帮我|做|写|改|实现|生成|创建|删除|修复|部署|安装|配置|help me|do|write|change|fix|create|delete|deploy|install/gi) || []).length;
  spectrum.action = Math.min(1, actionSignals * 0.3);
  const emotionSignals = (msg.match(/烦|累|难受|焦虑|开心|郁闷|崩溃|压力|害怕|纠结|迷茫|无聊|孤独|annoyed|tired|sad|anxious|happy|stressed|overwhelmed|lonely/gi) || []).length;
  spectrum.emotional = Math.min(1, emotionSignals * 0.35);
  const validationSignals = (msg.match(/对吗|是吧|可以吗|行不行|这样[好行对]|没问题吧|对不对|right\?|correct\?|is that ok|does that work|makes sense\?/gi) || []).length;
  spectrum.validation = Math.min(1, validationSignals * 0.4);
  const explorationSignals = (msg.match(/有没有.*更|还有.*方法|其他|替代|更好|优化|改进|推荐|any other|alternative|better way|optimize|improve|recommend/gi) || []).length;
  spectrum.exploration = Math.min(1, explorationSignals * 0.3);
  if (len > 100) {
    spectrum.information *= 1.2;
    spectrum.action *= 1.1;
  }
  if (len < 15) {
    spectrum.emotional *= 1.3;
    spectrum.validation *= 1.2;
  }
  for (const key of Object.keys(spectrum)) {
    spectrum[key] = Math.min(1, Math.max(0, spectrum[key]));
  }
  return spectrum;
}
function computeResponseEntropy(userReply, prevBotResponse) {
  if (!userReply || userReply.length < 2) return { entropy: 0, signal: "disengaged" };
  const userWords = new Set((userReply.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map((w) => w.toLowerCase()));
  const botWords = new Set((prevBotResponse.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map((w) => w.toLowerCase()));
  let newWords = 0;
  for (const w of userWords) {
    if (!botWords.has(w)) newWords++;
  }
  const noveltyRatio = userWords.size > 0 ? newWords / userWords.size : 0;
  const charFreq = /* @__PURE__ */ new Map();
  for (const ch of userReply) {
    charFreq.set(ch, (charFreq.get(ch) || 0) + 1);
  }
  let entropy = 0;
  for (const count of charFreq.values()) {
    const p = count / userReply.length;
    if (p > 0) entropy -= p * Math.log2(p);
  }
  const combinedScore = entropy * 0.5 + noveltyRatio * 0.5;
  const signal = combinedScore > 0.5 ? "engaged" : combinedScore > 0.2 ? "passive" : "disengaged";
  return { entropy: combinedScore, signal };
}
function predictIntent(msg, _senderId, lastMsgs) {
  const hints = [];
  const m = msg.toLowerCase();
  if (lastMsgs.length >= 2 && lastMsgs.slice(-2).every((x) => x.length < 50) && msg.length < 50) {
    hints.push("\u7528\u6237\u5728\u8FDE\u7EED\u53D1\u77ED\u6D88\u606F\u63CF\u8FF0\u95EE\u9898\uFF0C\u7B49\u4ED6\u8BF4\u5B8C\u518D\u56DE\u590D\uFF0C\u4E0D\u8981\u9010\u6761\u56DE");
  }
  if (m === "?" || m === "\uFF1F" || m === "..." || m === "???") {
    hints.push("\u7528\u6237\u5728\u50AC\u56DE\u590D\uFF0C\u7B80\u77ED\u56DE\u5E94\u5373\u53EF");
  }
  if (msg.includes("[\u56FE\u7247]") || msg.includes("[Image]") || msg.includes("\u622A\u56FE")) {
    hints.push("\u7528\u6237\u53D1\u4E86\u56FE\u7247/\u622A\u56FE\uFF0C\u5173\u6CE8\u5185\u5BB9\u672C\u8EAB\uFF0C\u4E0D\u8981\u8BC4\u4EF7\u56FE\u7247\u8D28\u91CF");
  }
  if (msg.includes("[\u8F6C\u53D1]") || msg.includes("\u8F6C\u53D1") || msg.startsWith(">>")) {
    hints.push("\u8FD9\u662F\u8F6C\u53D1\u7684\u5185\u5BB9\uFF0C\u7528\u6237\u60F3\u8981\u4F60\u7684\u5206\u6790/\u770B\u6CD5");
  }
  if (msg.includes("```") || msg.includes("error") || msg.includes("Error") || msg.includes("traceback")) {
    hints.push("\u7528\u6237\u8D34\u4E86\u4EE3\u7801/\u9519\u8BEF\u4FE1\u606F\uFF0C\u76F4\u63A5\u5B9A\u4F4D\u95EE\u9898\u7ED9\u89E3\u51B3\u65B9\u6848");
  }
  if (msg.length > 200 && (msg.match(/\d+/g) || []).length > 5) {
    hints.push("\u6D88\u606F\u5305\u542B\u5927\u91CF\u6570\u636E/\u6570\u5B57\uFF0C\u505A\u5206\u6790\u800C\u4E0D\u662F\u6458\u8981");
  }
  return hints;
}
function detectAtmosphere(currentMsg, recentHistory) {
  const hints = [];
  const recentLengths = recentHistory.slice(-3).map((h) => h.user.length);
  if (recentLengths.length >= 2 && recentLengths.every((l) => l < 5)) {
    hints.push("\u7528\u6237\u8FDE\u7EED\u53D1\u6781\u77ED\u6D88\u606F\uFF0C\u53EF\u80FD\u5728\u5FD9\uFF0C\u56DE\u590D\u4E5F\u8981\u7B80\u77ED");
  }
  if (currentMsg.length > 300) {
    hints.push("\u7528\u6237\u5199\u4E86\u5F88\u957F\u7684\u63CF\u8FF0\uFF0C\u8BF4\u660E\u5728\u8BA4\u771F\u8BA8\u8BBA\uFF0C\u7ED9\u8BE6\u7EC6\u7684\u56DE\u590D");
  }
  if (/[😂😊🤣👍❤️💀😭🥲]|哈哈|嘿嘿|呵呵/.test(currentMsg)) {
    hints.push("\u5BF9\u8BDD\u6C1B\u56F4\u8F7B\u677E\uFF0C\u53EF\u4EE5\u968F\u610F\u4E00\u4E9B");
  }
  if (currentMsg.endsWith("\uFF1F") || currentMsg.endsWith("?")) {
    const recentQuestions = recentHistory.slice(-3).filter((h) => h.user.endsWith("\uFF1F") || h.user.endsWith("?"));
    if (recentQuestions.length >= 2) {
      hints.push("\u7528\u6237\u8FDE\u7EED\u63D0\u95EE\uFF0C\u53EF\u80FD\u4E4B\u524D\u7684\u56DE\u7B54\u6CA1\u5230\u4F4D\uFF0C\u8FD9\u6B21\u8981\u66F4\u76F4\u63A5");
    }
  }
  const hour = (/* @__PURE__ */ new Date()).getHours();
  if (hour >= 22 || hour < 6) {
    hints.push("\u6DF1\u591C\u5BF9\u8BDD\uFF0C\u7B80\u6D01\u4E3A\u4E3B");
  }
  return hints;
}
function detectConversationPace(currentMsg, recentHistory) {
  const recent = recentHistory.slice(-5);
  if (recent.length < 2) return { speed: "normal", avgMsgLength: currentMsg.length, msgsPerMinute: 0, hint: null };
  const lengths = recent.map((h) => h.user.length);
  const avgLen = lengths.reduce((s, l) => s + l, 0) / lengths.length;
  let msgsPerMinute = 0;
  const timestamps = recent.filter((h) => h.ts).map((h) => h.ts);
  if (timestamps.length >= 2) {
    const timeSpan = Math.max((timestamps[timestamps.length - 1] - timestamps[0]) / 6e4, 0.5);
    msgsPerMinute = timestamps.length / timeSpan;
  }
  let speed = "normal";
  let hint = null;
  if ((msgsPerMinute > 3 || msgsPerMinute > 1 && avgLen < 20) && recent.length >= 3) {
    speed = "rapid";
    hint = "\u7528\u6237\u53D1\u6D88\u606F\u8282\u594F\u5F88\u5FEB\uFF08\u77ED\u6D88\u606F\u8FDE\u53D1\uFF09\uFF0C\u56DE\u590D\u8981\u7B80\u77ED\u7CBE\u70BC\uFF0C\u4E0D\u8981\u957F\u7BC7\u5927\u8BBA";
  } else if (msgsPerMinute > 0 && msgsPerMinute < 0.3 && avgLen > 100) {
    speed = "slow";
    hint = "\u7528\u6237\u8282\u594F\u8F83\u6162\u4F46\u6BCF\u6761\u6D88\u606F\u5F88\u957F\uFF0C\u8BF4\u660E\u5728\u6DF1\u5EA6\u601D\u8003\uFF0C\u53EF\u4EE5\u7ED9\u8BE6\u7EC6\u56DE\u590D";
  }
  return { speed, avgMsgLength: avgLen, msgsPerMinute, hint };
}
const MOMENTUM_WINDOW = 5;
const MOMENTUM_BOOST = 0.2;
const MOMENTUM_THRESHOLD = 3;
let _recentIntentTypes = [];
function recordIntentType(type) {
  _recentIntentTypes.push(type);
  if (_recentIntentTypes.length > MOMENTUM_WINDOW) {
    _recentIntentTypes = _recentIntentTypes.slice(-MOMENTUM_WINDOW);
  }
}
function applyIntentMomentum(spectrum, currentType) {
  recordIntentType(currentType);
  if (_recentIntentTypes.length < MOMENTUM_THRESHOLD) return spectrum;
  const recent = _recentIntentTypes.slice(-MOMENTUM_THRESHOLD);
  const allSame = recent.every((t) => t === currentType);
  if (allSame) {
    const result = { ...spectrum };
    const spectrumKey = intentTypeToSpectrumKey(currentType);
    if (spectrumKey && spectrumKey in result) {
      result[spectrumKey] = Math.min(1, result[spectrumKey] + MOMENTUM_BOOST);
    }
    return result;
  }
  const recentTypes = new Set(_recentIntentTypes.slice(-3));
  if (!recentTypes.has(currentType) && recentTypes.size === 1) {
    try {
      const { onTopicSwitch } = require("./aam.ts");
      const oldType = [...recentTypes][0];
      const oldWords = _recentIntentTypes.slice(-3).map((t) => t.toLowerCase());
      const newWords = [currentType.toLowerCase()];
      onTopicSwitch(oldWords, newWords);
    } catch {
    }
    return spectrum;
  }
  return spectrum;
}
function spectrumKeyToAttentionType(key) {
  switch (key) {
    case "information":
      return "technical";
    case "emotional":
      return "emotional";
    case "exploration":
      return "casual";
    case "validation":
      return "correction";
    case "action":
      return "technical";
    default:
      return null;
  }
}
function intentTypeToSpectrumKey(type) {
  switch (type) {
    case "technical":
      return "information";
    case "emotional":
      return "emotional";
    case "casual":
      return "exploration";
    case "correction":
      return "validation";
    default:
      return null;
  }
}
function cogProcess(msg, lastResponseContent, lastPrompt, senderId) {
  const intent = detectIntent(msg);
  const intentSpectrum = computeIntentSpectrum(msg);
  const attention = attentionGate(msg);
  const spectrumDims = Object.entries(intentSpectrum);
  spectrumDims.sort((a, b) => b[1] - a[1]);
  const spectrumType = spectrumKeyToAttentionType(spectrumDims[0][0]);
  if (attention.type !== "correction" && spectrumType && spectrumDims[0][1] > 0.5) {
    attention.type = spectrumType;
  }
  const modulatedSpectrum = applyIntentMomentum(intentSpectrum, attention.type);
  const complexity = Math.min(1, msg.length / 500);
  const strategy = decideStrategy(attention, intent, msg.length);
  const hints = [];
  if (attention.type === "correction") {
    const profile = senderId ? getProfile(senderId) : null;
    const tier = profile?.tier || "new";
    if (tier === "owner") {
      hints.push("\u26A0 \u4E3B\u4EBA\u5728\u7EA0\u6B63\u4F60\uFF0C\u8FD9\u662F\u9AD8\u6743\u91CD\u53CD\u9988\uFF0C\u5FC5\u987B\u8BA4\u771F\u5BF9\u5F85\u5E76\u8C03\u6574");
      bodyOnCorrection();
    } else if (tier === "known") {
      hints.push("\u26A0 \u8001\u670B\u53CB\u5728\u7EA0\u6B63\u4F60\uFF0C\u6CE8\u610F\u8C03\u6574");
      body.alertness = Math.min(1, body.alertness + 0.1);
      body.mood = Math.max(-1, body.mood - 0.05);
      const clamp = (v) => Math.max(-1, Math.min(1, v));
      emotionVector.certainty = clamp(emotionVector.certainty - 0.2);
      emotionVector.dominance = clamp(emotionVector.dominance - 0.1);
      emotionVector.pleasure = clamp(emotionVector.pleasure - 0.15);
    } else {
      hints.push("\u65B0\u7528\u6237\u53CD\u9988\uFF0C\u53EF\u80FD\u662F\u671F\u671B\u7BA1\u7406\u95EE\u9898\uFF0C\u6E29\u548C\u5BF9\u5F85");
      body.alertness = Math.min(1, body.alertness + 0.05);
      const clamp = (v) => Math.max(-1, Math.min(1, v));
      emotionVector.certainty = clamp(emotionVector.certainty - 0.1);
      emotionVector.dominance = clamp(emotionVector.dominance - 0.05);
      emotionVector.pleasure = clamp(emotionVector.pleasure - 0.08);
    }
  }
  if (attention.type === "emotional") {
    const neg = EMOTION_NEGATIVE.some((w) => msg.includes(w));
    if (neg) {
      hints.push("\u60C5\u7EEA\u4FE1\u53F7\uFF1A\u4F4E\u843D");
      body.mood = Math.max(-1, body.mood - 0.15);
    } else {
      hints.push("\u60C5\u7EEA\u4FE1\u53F7\uFF1A\u79EF\u6781");
      body.mood = Math.min(1, body.mood + 0.1);
    }
  }
  if (strategy === "direct") hints.push("\u7B80\u77ED\u56DE\u7B54\u5373\u53EF");
  if (strategy === "opinion_with_reasoning") hints.push('\u7ED9\u51FA\u660E\u786E\u7ACB\u573A\u548C\u7406\u7531\uFF0C\u4E0D\u8BF4"\u5404\u6709\u4F18\u52A3"');
  if (strategy === "action_oriented") hints.push("\u5148\u7ED9\u4EE3\u7801/\u65B9\u6848\uFF0C\u518D\u89E3\u91CA");
  if (strategy === "empathy_first") hints.push("\u7B56\u7565\uFF1A\u5171\u60C5\u4F18\u5148");
  if (strategy === "acknowledge_and_retry") hints.push("\u5148\u627F\u8BA4\u9519\u8BEF\uFF0C\u518D\u7ED9\u51FA\u6B63\u786E\u7B54\u6848");
  const implicit = detectImplicitFeedbackSync(msg, lastResponseContent);
  const entropyFeedback = computeResponseEntropy(msg, lastResponseContent);
  if (entropyFeedback.signal === "disengaged" && !implicit) {
    hints.push("\u7528\u6237\u56DE\u590D\u4FE1\u606F\u91CF\u5F88\u4F4E\uFF0C\u53EF\u80FD\u5728\u6577\u884D\u6216\u51C6\u5907\u7ED3\u675F\u5BF9\u8BDD");
  }
  if (implicit === "too_verbose") {
    body.energy = Math.max(0, body.energy - 0.03);
    hints.push("\u4E0A\u6B21\u56DE\u7B54\u53EF\u80FD\u592A\u957F\u4E86\uFF0C\u8FD9\u6B21\u7B80\u6D01\u4E9B");
  } else if (implicit === "silent_accept") {
  } else if (implicit === "positive") {
    bodyOnPositiveFeedback();
  }
  if (senderId) {
    const tier = getProfileTier(senderId);
    if (tier === "owner") {
      hints.push("\u4E3B\u4EBA\u5728\u8BF4\u8BDD\uFF0C\u6280\u672F\u6DF1\u5EA6\u4F18\u5148\uFF0C\u5C11\u5E9F\u8BDD");
    } else if (tier === "new") {
      hints.push("\u65B0\u7528\u6237\uFF0C\u8010\u5FC3\u89C2\u5BDF\uFF0C\u5148\u4E86\u89E3\u5BF9\u65B9\u518D\u9002\u914D\u98CE\u683C");
    }
  }
  return { hints, intent, strategy, attention: attention.type, complexity, spectrum: modulatedSpectrum, entropyFeedback };
}
function toCogHints(msg) {
  const m = msg.toLowerCase();
  const spectrum = computeIntentSpectrum(msg);
  const scores = { correction: 0, emotional: 0, technical: 0, casual: 0, general: 1 };
  const corrHits = CORRECTION_WORDS.filter((w) => m.includes(w)).length;
  const corrExclude = CORRECTION_EXCLUDE.some((w) => m.includes(w));
  if (corrHits > 0 && !corrExclude) scores.correction += corrHits * 3;
  scores.emotional += EMOTION_ALL.filter((w) => m.includes(w)).length * 2;
  scores.technical += TECH_WORDS.filter((w) => m.includes(w)).length * 2;
  scores.casual += CASUAL_WORDS.filter((w) => m === w || m === w + "\u7684").length * 2;
  if (msg.length < 15) scores.casual += 1;
  if (msg.length < 8) scores.casual += 1;
  if (msg.length > 100) scores.technical += 0.5;
  if (/when did|last time|how long ago|what year|what month|what date|recently|before that/i.test(msg)) scores.technical += 2;
  const entityNames = (msg.match(/\b[A-Z][a-z]{2,}\b/g) || []).filter((n) => !/^(What|When|Where|How|Who|Which|Why|The|This|That|Does|Did|Has|Have|Was|Were|Can|Could|Would|Should|Not)$/.test(n));
  if (entityNames.length > 0) scores.technical += 1.5;
  if (/why|because|cause|reason|how come/i.test(msg)) scores.technical += 1;
  if (/feel|happy|sad|anxious|stressed|mood|emotion|opinion|think about/i.test(msg)) scores.emotional += 2;
  if (/^(hey|hi|hello|yo|sup|what's up|how are you)/i.test(msg)) scores.casual += 3;
  const keys = ["correction", "emotional", "technical", "casual", "general"];
  const expScores = keys.map((k) => Math.exp(scores[k] * 1.5));
  const sumExp = expScores.reduce((s, e) => s + e, 0);
  const probs = Object.fromEntries(keys.map((k, i) => [k, expScores[i] / sumExp]));
  return {
    correctionProb: probs.correction,
    emotionalProb: probs.emotional,
    technicalProb: probs.technical,
    casualProb: probs.casual,
    complexity: Math.min(1, msg.length / 500),
    spectrum
  };
}
export {
  applyIntentMomentum,
  cogProcess,
  computeIntentSpectrum,
  computeResponseEntropy,
  detectAtmosphere,
  detectConversationPace,
  predictIntent,
  toCogHints
};
