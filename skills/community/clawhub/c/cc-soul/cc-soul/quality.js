import { DATA_DIR, EVAL_PATH, loadJson, debouncedSave } from "./persistence.ts";
import { spawnCLI } from "./cli.ts";
import { body } from "./body.ts";
import { extractJSON } from "./utils.ts";
import { resolve } from "path";
const _lastReplyByUser = /* @__PURE__ */ new Map();
const _nextUserMsgLenByUser = /* @__PURE__ */ new Map();
function trackLastReply(reply, userId = "default") {
  _lastReplyByUser.set(userId, reply);
}
function trackNextUserMsg(msg, userId = "default") {
  _nextUserMsgLenByUser.set(userId, msg.length);
}
function consumeNextUserMsg(userId = "default") {
  const v = _nextUserMsgLenByUser.get(userId) ?? -1;
  _nextUserMsgLenByUser.delete(userId);
  return v;
}
const WEIGHTS_PATH = resolve(DATA_DIR, "quality_weights.json");
const FEATURE_KEYS = [
  "mediumLength",
  "longLength",
  "tooLong",
  "tooShort",
  "hasReasoning",
  "hasCode",
  "hasList",
  "hasUncertainty",
  "hasRefusal",
  "relevance",
  "aiExposure",
  "lengthRatio",
  "repetitionPenalty",
  "informationGain",
  "userEngagement"
];
function _quickTrigramSim(a, b) {
  try {
    const { hybridSimilarity } = require("./memory-utils.ts");
    return hybridSimilarity(a, b);
  } catch {
    if (!a || !b) return 0;
    const triA = /* @__PURE__ */ new Set(), triB = /* @__PURE__ */ new Set();
    for (let i = 0; i < a.length - 2; i++) triA.add(a.slice(i, i + 3));
    for (let i = 0; i < b.length - 2; i++) triB.add(b.slice(i, i + 3));
    if (triA.size === 0 || triB.size === 0) return 0;
    let inter = 0;
    for (const t of triA) {
      if (triB.has(t)) inter++;
    }
    return inter / (triA.size + triB.size - inter);
  }
}
function extractFeatures(question, answer, userId = "default") {
  const qLen = question.length, aLen = answer.length;
  const qWords = new Set((question.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map((w) => w.toLowerCase()));
  const aWords = (answer.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map((w) => w.toLowerCase());
  const overlap = qWords.size > 0 ? aWords.filter((w) => qWords.has(w)).length / Math.max(1, qWords.size) : 0;
  const lastReply = _lastReplyByUser.get(userId) || "";
  const repSim = _quickTrigramSim(answer.slice(0, 500), lastReply.slice(0, 500));
  const repetitionPenalty = repSim > 0.7 ? 1 : 0;
  const aUniqueWords = aWords.filter((w) => !qWords.has(w));
  const infoGainRatio = qWords.size > 0 ? aUniqueWords.length / qWords.size : 0;
  const informationGain = infoGainRatio > 2 ? 1 : 0;
  const nextLen = consumeNextUserMsg(userId);
  const userEngagement = nextLen < 0 ? 0 : nextLen > 20 ? 1 : nextLen < 5 ? -1 : 0;
  return {
    mediumLength: aLen > 50 ? 1 : 0,
    longLength: aLen > 200 ? 1 : 0,
    tooLong: aLen > 1e3 && qLen < 30 ? 1 : 0,
    tooShort: aLen < 10 && qLen > 50 ? 1 : 0,
    hasReasoning: ["\u56E0\u4E3A", "\u6240\u4EE5", "\u9996\u5148", "\u5176\u6B21", "\u539F\u56E0", "\u672C\u8D28\u4E0A", "because", "therefore"].some((m) => answer.includes(m)) ? 1 : 0,
    hasCode: answer.includes("```") ? 1 : 0,
    hasList: /^[-*•]\s/m.test(answer) || /^\d+\.\s/m.test(answer) ? 1 : 0,
    hasUncertainty: ["\u4E0D\u786E\u5B9A", "\u4E0D\u592A\u786E\u5B9A", "\u53EF\u80FD", "I'm not sure"].some((m) => answer.includes(m)) ? 1 : 0,
    hasRefusal: ["\u6211\u4E0D\u77E5\u9053", "\u65E0\u6CD5\u56DE\u7B54", "\u8D85\u51FA\u4E86\u6211\u7684"].some((m) => answer.includes(m)) ? 1 : 0,
    relevance: Math.min(1, overlap),
    aiExposure: /作为一个?AI|作为人工智能|作为语言模型|I am an AI/i.test(answer) ? 1 : 0,
    lengthRatio: Math.min(100, aLen / Math.max(1, qLen)),
    repetitionPenalty,
    informationGain,
    userEngagement
  };
}
let qw = {
  bias: -0.225,
  // sigmoid(-0.225)≈0.444 → score≈5.0 baseline (no features active)
  weights: {
    mediumLength: 0.5,
    longLength: 0.5,
    tooLong: -1,
    tooShort: -1.5,
    hasReasoning: 1,
    hasCode: 0.5,
    hasList: 0.3,
    hasUncertainty: 0.3,
    hasRefusal: -1.5,
    relevance: 1.5,
    aiExposure: -2,
    lengthRatio: 0,
    repetitionPenalty: -1.5,
    informationGain: 0.5,
    userEngagement: 0.5
  },
  learningRate: 0.1,
  trainingExamples: 0,
  gradientSquaredSum: {},
  hardExamples: []
};
function loadQualityWeights() {
  qw = loadJson(WEIGHTS_PATH, qw);
  if (!qw.gradientSquaredSum) qw.gradientSquaredSum = {};
  if (!qw.adamM) qw.adamM = {};
  if (!qw.adamV) qw.adamV = {};
  if (!qw.adamT) qw.adamT = 0;
  if (!qw.ftrl) qw.ftrl = {};
  if (!qw.hardExamples) qw.hardExamples = [];
  for (const key of FEATURE_KEYS) {
    if (qw.weights[key] === void 0) qw.weights[key] = 0;
  }
  console.log(`[cc-soul][quality] loaded weights: ${qw.trainingExamples} training examples`);
}
let evalMetrics = {
  totalResponses: 0,
  avgQuality: 5,
  correctionRate: 0,
  brainHitRate: 0,
  memoryRecallRate: 0,
  lastEval: 0
};
let evalLoaded = false;
function ensureEvalLoaded() {
  if (evalLoaded) return;
  evalLoaded = true;
  evalMetrics = loadJson(EVAL_PATH, evalMetrics);
}
let qualitySum = 0;
let qualityCount = 0;
let memRecalls = 0;
let memMisses = 0;
function trackQuality(score) {
  qualitySum += score;
  qualityCount++;
}
function trackMemoryRecall(found) {
  if (found) memRecalls++;
  else memMisses++;
}
function scoreResponse(question, answer, userId = "default") {
  const features = extractFeatures(question, answer, userId);
  let logit = qw.bias;
  for (const key of FEATURE_KEYS) {
    logit += (qw.weights[key] || 0) * features[key];
  }
  const sigmoid = 1 / (1 + Math.exp(-logit));
  const score = sigmoid * 9 + 1;
  return Math.round(score * 10) / 10;
}
function updateQualityFromEngagement(question, answer, engagementRate, userId = "default") {
  const features = extractFeatures(question, answer, userId);
  const target = engagementRate;
  let logit = qw.bias;
  for (const key of FEATURE_KEYS) logit += (qw.weights[key] || 0) * features[key];
  const predicted = 1 / (1 + Math.exp(-logit));
  const error = predicted - target;
  if (!qw.gradientSquaredSum) qw.gradientSquaredSum = {};
  const adaEps = 1e-8;
  qw.gradientSquaredSum["_bias"] = (qw.gradientSquaredSum["_bias"] || 0) + error * error;
  qw.bias -= qw.learningRate * 0.5 / Math.sqrt(qw.gradientSquaredSum["_bias"] + adaEps) * error;
  for (const key of FEATURE_KEYS) {
    const grad = error * features[key];
    qw.gradientSquaredSum[key] = (qw.gradientSquaredSum[key] || 0) + grad * grad;
    qw.weights[key] = Math.max(-5, Math.min(5, (qw.weights[key] || 0) - qw.learningRate * 0.5 / Math.sqrt(qw.gradientSquaredSum[key] + adaEps) * grad));
  }
  debouncedSave(WEIGHTS_PATH, qw);
}
function updateQualityWeights(question, answer, feedback, userId = "default") {
  const features = extractFeatures(question, answer, userId);
  const target = feedback === "positive" ? 0.9 : 0.2;
  let logit = qw.bias;
  for (const key of FEATURE_KEYS) {
    logit += (qw.weights[key] || 0) * features[key];
  }
  const predicted = 1 / (1 + Math.exp(-logit));
  const error = predicted - target;
  const loss = Math.abs(error);
  if (loss > 0.3) {
    if (!qw.hardExamples) qw.hardExamples = [];
    qw.hardExamples.push({ question: question.slice(0, 200), answer: answer.slice(0, 500), target, loss });
    if (qw.hardExamples.length > 30) {
      qw.hardExamples.sort((a, b) => b.loss - a.loss);
      qw.hardExamples = qw.hardExamples.slice(0, 30);
    }
  }
  if (!qw.gradientSquaredSum) qw.gradientSquaredSum = {};
  const adaEps = 1e-8;
  qw.gradientSquaredSum["_bias"] = (qw.gradientSquaredSum["_bias"] || 0) + error * error;
  const biasLR = qw.learningRate / Math.sqrt(qw.gradientSquaredSum["_bias"] + adaEps);
  qw.bias -= biasLR * error;
  for (const key of FEATURE_KEYS) {
    const grad = error * features[key];
    qw.gradientSquaredSum[key] = (qw.gradientSquaredSum[key] || 0) + grad * grad;
    const lr = qw.learningRate / Math.sqrt(qw.gradientSquaredSum[key] + adaEps);
    qw.weights[key] = (qw.weights[key] || 0) - lr * grad;
    qw.weights[key] = Math.max(-5, Math.min(5, qw.weights[key]));
  }
  qw.trainingExamples++;
  debouncedSave(WEIGHTS_PATH, qw);
  console.log(`[cc-soul][quality] weights updated (${feedback}): ${qw.trainingExamples} examples, bias=${qw.bias.toFixed(3)}`);
}
function resampleHardExamples() {
  if (!qw.hardExamples || qw.hardExamples.length < 3) return;
  if (!qw.gradientSquaredSum) qw.gradientSquaredSum = {};
  const samples = qw.hardExamples.slice(0, 3);
  const adaEps = 1e-8;
  for (const { question, answer, target } of samples) {
    const features = extractFeatures(question, answer);
    let logit = qw.bias;
    for (const key of FEATURE_KEYS) logit += (qw.weights[key] || 0) * features[key];
    const predicted = 1 / (1 + Math.exp(-logit));
    const error = predicted - target;
    const replayLR = qw.learningRate * 0.5;
    qw.gradientSquaredSum["_bias"] = (qw.gradientSquaredSum["_bias"] || 0) + error * error;
    qw.bias -= replayLR / Math.sqrt(qw.gradientSquaredSum["_bias"] + adaEps) * error;
    for (const key of FEATURE_KEYS) {
      const grad = error * features[key];
      qw.gradientSquaredSum[key] = (qw.gradientSquaredSum[key] || 0) + grad * grad;
      qw.weights[key] = Math.max(-5, Math.min(5, (qw.weights[key] || 0) - replayLR / Math.sqrt(qw.gradientSquaredSum[key] + adaEps) * grad));
    }
  }
  debouncedSave(WEIGHTS_PATH, qw);
  console.log(`[cc-soul][quality] replayed ${samples.length} hard examples (AdaGrad)`);
}
function selfCheckSync(question, answer) {
  if (answer.length < 5) return "\u56DE\u7B54\u592A\u77ED\uFF0C\u53EF\u80FD\u6CA1\u6709\u5B9E\u8D28\u5185\u5BB9";
  if (answer.length > 5e3 && question.length < 30) return "\u56DE\u7B54\u8FC7\u957F\uFF0C\u77ED\u95EE\u9898\u4E0D\u9700\u8981\u957F\u7BC7\u5927\u8BBA";
  if (answer.includes("\u4F5C\u4E3A\u4E00\u4E2AAI") || answer.includes("\u4F5C\u4E3A\u8BED\u8A00\u6A21\u578B")) return "\u66B4\u9732\u4E86AI\u8EAB\u4EFD\uFF0C\u8FDD\u53CD\u4EBA\u8BBE";
  return null;
}
function logIssue(issue, context) {
  console.log(`[cc-soul][quality] ${issue} | ctx: ${context.slice(0, 80)}`);
}
function selfCheckWithCLI(question, answer) {
  if (answer.length < 20 || question.length < 5) return;
  const prompt = `\u95EE\u9898: "${question.slice(0, 200)}"
\u56DE\u7B54: "${answer.slice(0, 500)}"

\u8BC4\u4EF7\u8FD9\u4E2A\u56DE\u7B54: 1.\u662F\u5426\u56DE\u7B54\u4E86\u95EE\u9898 2.\u6709\u6CA1\u6709\u7F16\u9020 3.\u662F\u5426\u5570\u55E6 4.\u6253\u52061-10\u3002JSON\u683C\u5F0F: {"score":N,"issues":["\u95EE\u9898"]}`;
  spawnCLI(prompt, (output) => {
    try {
      const result = extractJSON(output);
      if (result) {
        const score = result.score || 5;
        trackQuality(score);
        if (result.issues?.length) {
          for (const issue of result.issues) {
            logIssue(issue, question);
          }
          body.anomaly = Math.min(1, body.anomaly + 0.1);
        }
        if (score <= 4) {
          body.alertness = Math.min(1, body.alertness + 0.15);
          console.log(`[cc-soul][quality] CLI self-check low score: ${score}/10`);
        }
      }
    } catch (e) {
      console.error(`[cc-soul][quality] parse error: ${e.message}`);
    }
  });
}
function computeEval(totalMessages, corrections, resetWindow = false) {
  ensureEvalLoaded();
  evalMetrics = {
    totalResponses: totalMessages,
    avgQuality: qualityCount > 0 ? Math.round(qualitySum / qualityCount * 10) / 10 : 5,
    correctionRate: totalMessages > 0 ? Math.round(corrections / totalMessages * 1e3) / 10 : 0,
    brainHitRate: 0,
    memoryRecallRate: memRecalls + memMisses > 0 ? Math.round(memRecalls / (memRecalls + memMisses) * 100) : 0,
    lastEval: Date.now()
  };
  debouncedSave(EVAL_PATH, evalMetrics);
  if (resetWindow) {
    qualitySum = 0;
    qualityCount = 0;
    memRecalls = 0;
    memMisses = 0;
  }
  return evalMetrics;
}
function getEvalSummary(totalMessages, corrections) {
  ensureEvalLoaded();
  const e = computeEval(totalMessages, corrections);
  return `\u8BC4\u5206:${e.avgQuality}/10 \u7EA0\u6B63\u7387:${e.correctionRate}% \u8BB0\u5FC6\u53EC\u56DE:${e.memoryRecallRate}%`;
}
const qualityModule = {
  id: "quality",
  name: "\u8D28\u91CF\u8BC4\u4F30",
  dependencies: ["body"],
  priority: 60,
  init() {
    loadQualityWeights();
  }
};
export {
  computeEval,
  evalMetrics,
  getEvalSummary,
  loadQualityWeights,
  qualityModule,
  resampleHardExamples,
  scoreResponse,
  selfCheckSync,
  selfCheckWithCLI,
  trackLastReply,
  trackMemoryRecall,
  trackNextUserMsg,
  trackQuality,
  updateQualityFromEngagement,
  updateQualityWeights
};
