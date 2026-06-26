import { resolve } from "path";
import { DATA_DIR, loadJson, debouncedSave } from "./persistence.ts";
import { memoryState, ensureMemoriesLoaded } from "./memory.ts";
import { getPersonModel } from "./person-model.ts";
const DU_PATH = resolve(DATA_DIR, "deep_understand.json");
const DEFAULTS = {
  temporal: { peakHours: [], stressDay: null, lateNightFrequency: 0 },
  sayDo: { gaps: [] },
  growth: { direction: "plateauing", details: "" },
  unspoken: { needs: [] },
  cognitive: { load: "normal", indicator: "" },
  stress: { stressLevel: 0, signals: [] },
  dynamicProfile: "",
  updatedAt: 0
};
let state = loadJson(DU_PATH, { ...DEFAULTS });
function analyzeTemporalPatterns() {
  const history = memoryState.chatHistory;
  if (history.length < 10) return state.temporal;
  const hourCounts = new Array(24).fill(0);
  const dayMood = /* @__PURE__ */ new Map();
  let lateNight = 0;
  for (const h of history) {
    const d = new Date(h.ts), hr = d.getHours();
    hourCounts[hr]++;
    if (hr >= 23 || hr < 4) lateNight++;
    const day = d.getDay();
    if (!dayMood.has(day)) dayMood.set(day, []);
    dayMood.get(day).push(h.user.length < 10 && (hr >= 22 || hr < 6) ? -1 : 0);
  }
  const peakHours = hourCounts.map((c, i) => ({ h: i, c })).sort((a, b) => b.c - a.c).slice(0, 3).filter((x) => x.c > 0).map((x) => x.h);
  let stressDay = null, worstAvg = 0;
  const dayNames = ["\u5468\u65E5", "\u5468\u4E00", "\u5468\u4E8C", "\u5468\u4E09", "\u5468\u56DB", "\u5468\u4E94", "\u5468\u516D"];
  for (const [day, moods] of dayMood) {
    if (moods.length < 3) continue;
    const avg = moods.reduce((a, b) => a + b, 0) / moods.length;
    if (avg < worstAvg) {
      worstAvg = avg;
      stressDay = dayNames[day];
    }
  }
  return { peakHours, stressDay, lateNightFrequency: lateNight / history.length };
}
function analyzeSayDoGap() {
  ensureMemoriesLoaded();
  const history = memoryState.chatHistory;
  const intents = memoryState.memories.filter((m) => /我要|我打算|我会|我准备|I will|I'm going to/i.test(m.content) && m.scope !== "expired");
  const gaps = [];
  for (const intent of intents.slice(-10)) {
    const c = intent.content.toLowerCase();
    if (/早睡|早点睡|sleep early/.test(c)) {
      const after = history.filter((h) => h.ts > intent.ts);
      const late = after.filter((h) => {
        const hr = new Date(h.ts).getHours();
        return hr >= 0 && hr < 5;
      }).length;
      if (after.length > 5 && late / after.length > 0.3)
        gaps.push({ stated: "\u65E9\u7761", actual: `${Math.round(late / after.length * 100)}%\u6D88\u606F\u5728\u51CC\u6668`, frequency: late });
    }
    if (/少加班|多休息|放松|rest more|take break/.test(c)) {
      const wknd = history.filter((h) => {
        const d = new Date(h.ts);
        return h.ts > intent.ts && (d.getDay() === 0 || d.getDay() === 6);
      }).length;
      if (wknd > 10) gaps.push({ stated: "\u591A\u4F11\u606F", actual: `\u5468\u672B\u4ECD\u6709${wknd}\u6761\u6D88\u606F`, frequency: wknd });
    }
  }
  return { gaps: gaps.slice(0, 5) };
}
function analyzeGrowth() {
  const history = memoryState.chatHistory;
  if (history.length < 20) return { direction: "plateauing", details: "\u6570\u636E\u4E0D\u8DB3" };
  const half = Math.floor(history.length / 2);
  const first = history.slice(0, half), second = history.slice(half);
  const avgLen = (a) => a.reduce((s, h) => s + h.user.length, 0) / a.length;
  const l1 = avgLen(first), l2 = avgLen(second);
  const techRe = /async|await|deploy|refactor|pipeline|架构|重构|微服务|并发|索引|缓存/gi;
  const techCount = (a) => {
    const s = /* @__PURE__ */ new Set();
    for (const h of a) {
      const m = h.user.match(techRe);
      if (m) m.forEach((w) => s.add(w.toLowerCase()));
    }
    return s.size;
  };
  const t1 = techCount(first), t2 = techCount(second);
  if (l2 > l1 * 1.3 && t2 > t1) return { direction: "growing", details: `\u957F\u5EA6+${Math.round((l2 / l1 - 1) * 100)}%\uFF0C\u8BCD\u6C47${t1}\u2192${t2}` };
  if (l2 < l1 * 0.7 || t2 < t1 * 0.5) return { direction: "struggling", details: "\u6D88\u606F\u53D8\u77ED\u6216\u8BCD\u6C47\u51CF\u5C11" };
  return { direction: "plateauing", details: "\u6A21\u5F0F\u7A33\u5B9A" };
}
function fitLearningCurve(history) {
  if (history.length < 10) return { growthRate: 0, currentLevel: 0.5, plateau: false, prediction: "\u6570\u636E\u4E0D\u8DB3" };
  const windowSize = 5;
  const dataPoints = [];
  for (let i = 0; i <= history.length - windowSize; i += windowSize) {
    const window = history.slice(i, i + windowSize);
    const avgLen = window.reduce((s, h) => s + h.user.length, 0) / windowSize;
    const allWords = window.map((h) => h.user.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).flat();
    const unique = new Set(allWords.map((w) => w.toLowerCase()));
    const richness = allWords.length > 0 ? unique.size / allWords.length : 0;
    const level = Math.min(1, avgLen / 100 * 0.4 + richness * 0.6);
    dataPoints.push({ t: i / windowSize + 1, level });
  }
  if (dataPoints.length < 3) return { growthRate: 0, currentLevel: 0.5, plateau: false, prediction: "\u6570\u636E\u4E0D\u8DB3" };
  const xs = dataPoints.map((d) => Math.log(d.t + 1));
  const ys = dataPoints.map((d) => Math.log(Math.max(0.01, d.level)));
  const n = xs.length;
  const sumX = xs.reduce((s, x) => s + x, 0);
  const sumY = ys.reduce((s, y) => s + y, 0);
  const sumXY = xs.reduce((s, x, i) => s + x * ys[i], 0);
  const sumXX = xs.reduce((s, x) => s + x * x, 0);
  const b = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX + 1e-9);
  const currentLevel = dataPoints[dataPoints.length - 1].level;
  const plateau = Math.abs(b) < 0.05 && dataPoints.length >= 5;
  let prediction = "";
  if (b > 0.15) prediction = "\u5FEB\u901F\u6210\u957F\u671F\uFF0C\u4FDD\u6301\u8282\u594F";
  else if (b > 0.05) prediction = "\u7A33\u6B65\u63D0\u5347\u4E2D";
  else if (b > -0.05) prediction = "\u5E73\u53F0\u671F\uFF0C\u53EF\u80FD\u9700\u8981\u65B0\u6311\u6218";
  else prediction = "\u6709\u6240\u4E0B\u6ED1\uFF0C\u5EFA\u8BAE\u8C03\u6574\u65B9\u5411";
  return { growthRate: b, currentLevel, plateau, prediction };
}
function analyzeUnspokenNeeds() {
  const recent = memoryState.chatHistory.filter((h) => h.ts > Date.now() - 7 * 864e5);
  const domains = [
    ["\u7F16\u7A0B/coding", /代码|bug|error|函数|class|api|编程|开发|调试|debug|code|programming|development|compile|runtime|stack/i],
    ["\u804C\u573A/career", /工作|老板|同事|面试|加班|薪|绩效|晋升|job|boss|colleague|interview|overtime|salary|promotion|workplace|career/i],
    ["\u5065\u5EB7/health", /睡眠|运动|头疼|累|健身|饮食|体检|sleep|exercise|headache|tired|fitness|diet|medical|workout/i],
    ["\u60C5\u611F/emotion", /感觉|心情|焦虑|压力|开心|难过|孤独|feeling|mood|anxious|stress|happy|sad|lonely|depressed/i],
    ["\u5B66\u4E60/learning", /学习|考试|课程|教程|理解|掌握|study|exam|course|tutorial|understand|learn|education/i]
  ];
  const counts = /* @__PURE__ */ new Map();
  for (const h of recent) for (const [d, re] of domains) if (re.test(h.user)) counts.set(d, (counts.get(d) || 0) + 1);
  const needs = [...counts.entries()].filter(([, n]) => n >= 3).map(([d, n]) => ({ domain: d, confidence: Math.min(1, n / 10), evidence: `\u672C\u5468${n}\u6B21` })).sort((a, b) => b.confidence - a.confidence).slice(0, 5);
  return { needs };
}
function analyzeCognitiveLoad() {
  const history = memoryState.chatHistory;
  if (history.length < 5) return { load: "normal", indicator: "" };
  const allAvg = history.reduce((s, h) => s + h.user.length, 0) / history.length;
  const r5 = history.slice(-5);
  const rAvg = r5.reduce((s, h) => s + h.user.length, 0) / r5.length;
  if (rAvg < allAvg * 0.4 && rAvg < 20) return { load: "high", indicator: `\u5747${Math.round(rAvg)}\u5B57(\u5386\u53F2${Math.round(allAvg)})` };
  if (rAvg > allAvg * 1.5 && rAvg > 80) return { load: "low", indicator: `\u8BE6\u7EC6\u6A21\u5F0F${Math.round(rAvg)}\u5B57` };
  return { load: "normal", indicator: "" };
}
function analyzeStress() {
  const history = memoryState.chatHistory;
  if (history.length < 5) return { stressLevel: 0, signals: [] };
  const recent = history.slice(-10), signals = [];
  let score = 0;
  const rAvg = recent.reduce((s, h) => s + h.user.length, 0) / recent.length;
  const hAvg = history.reduce((s, h) => s + h.user.length, 0) / history.length;
  if (rAvg < hAvg * 0.5 && rAvg < 15) {
    score += 0.3;
    signals.push("\u788E\u7247\u5316");
  }
  if (recent.reduce((s, h) => s + (h.user.match(/[?？!！.。…]{2,}/g) || []).length, 0) >= 3) {
    score += 0.2;
    signals.push("\u6807\u70B9\u6FC0\u589E");
  }
  if (recent.filter((h) => /算了|随便|fuck|shit|烦|累|不管了|懒得|无所谓|操|靠|妈的|whatever|tired|give up|don't care|screw it|damn|crap|ugh|fed up|sick of|over it/.test(h.user)).length >= 2) {
    score += 0.3;
    signals.push("\u538B\u529B\u8BCD/stress words");
  }
  if (recent.filter((h) => {
    const hr = new Date(h.ts).getHours();
    return hr >= 1 && hr < 5;
  }).length >= 2) {
    score += 0.2;
    signals.push("\u6DF1\u591C");
  }
  return { stressLevel: Math.min(1, score), signals };
}
function analyzeStressDynamics(history) {
  if (history.length < 5) return { level: 0, velocity: 0, phase: "calm", turnsToBreakdown: null, resilience: 0.5 };
  const recent = history.slice(-15);
  const signals = [];
  for (let i = 0; i < recent.length; i++) {
    const msg = recent[i].user;
    let signal = 0;
    if (msg.length < 10) signal += 0.15;
    else if (msg.length > 80) signal -= 0.1;
    if (/烦|累|崩|急|压力|焦虑|受不了|算了|不想|头疼|烦死|frustrated|stressed|overwhelmed|exhausted|annoyed|ugh|burnout/.test(msg)) signal += 0.25;
    if (/谢|好的|明白|解决|搞定|不错|太好|thanks|got it|solved|fixed|great|awesome|nice/.test(msg)) signal -= 0.15;
    if (/[！!]{2,}|[？?]{2,}/.test(msg)) signal += 0.1;
    if (i > 0) {
      const gap = recent[i].ts - recent[i - 1].ts;
      if (gap < 1e4) signal += 0.1;
    }
    signals.push(Math.max(-0.3, Math.min(0.5, signal)));
  }
  let x = 0;
  let v = 0;
  const k = 0.15;
  const gamma = 0.3;
  const dt = 1;
  for (const F of signals) {
    const a = -k * x + F - gamma * v;
    v += a * dt;
    x += v * dt;
    x = Math.max(0, Math.min(1, x));
    v = Math.max(-0.5, Math.min(0.5, v));
  }
  let phase = "calm";
  if (x > 0.6 && v > 0) phase = "peak";
  else if (x > 0.3 && v > 0.05) phase = "accumulating";
  else if (x > 0.3 && v < -0.05) phase = "releasing";
  let turnsToBreakdown = null;
  if (v > 0.03 && x > 0.3) {
    turnsToBreakdown = Math.ceil((0.8 - x) / v);
    if (turnsToBreakdown > 10 || turnsToBreakdown < 0) turnsToBreakdown = null;
  }
  const resilience = Math.max(0.1, Math.min(0.9, k + (1 - x) * 0.3));
  return { level: x, velocity: v, phase, turnsToBreakdown, resilience };
}
function synthesizeProfile() {
  const pm = getPersonModel(), parts = [];
  const { temporal: t, growth: g, stress: s, cognitive: c, sayDo: sd, unspoken: u } = state;
  if (t.peakHours.length > 0) parts.push(`\u6D3B\u8DC3${t.peakHours.join("/")}\u65F6`);
  if (t.lateNightFrequency > 0.3) parts.push("\u591C\u732B\u5B50");
  if (g.direction === "growing") parts.push("\u4E0A\u5347\u671F");
  else if (g.direction === "struggling") parts.push("\u74F6\u9888\u671F");
  if (s.stressLevel > 0.5) parts.push(`\u538B\u529B\u9AD8(${s.signals.join("+")})`);
  let pressureAdded = false;
  try {
    const { getCoupledPressure } = require("./flow.ts");
    const cp = getCoupledPressure();
    if (cp && (cp.frustration > 0.3 || cp.stress > 0.3)) {
      if (cp.phase === "building" || cp.phase === "critical") parts.push(`\u538B\u529B${cp.phase === "critical" ? "\u4E34\u754C" : "\u79EF\u7D2F\u4E2D"}(\u632B\u8D25${(cp.frustration * 100).toFixed(0)}%,\u538B\u529B${(cp.stress * 100).toFixed(0)}%,\u8026\u5408${(cp.couplingStrength * 100).toFixed(0)}%)`);
      if (cp.turnsToBreakdown !== null) parts.push(`\u9884\u8BA1${cp.turnsToBreakdown}\u8F6E\u540E\u53EF\u80FD\u7206\u53D1`);
      if (cp.phase === "recovering") parts.push("\u538B\u529B\u91CA\u653E\u4E2D");
      pressureAdded = true;
    }
  } catch {
  }
  if (!pressureAdded) {
    const stressDyn = analyzeStressDynamics(memoryState.chatHistory);
    if (stressDyn.phase === "accumulating") parts.push(`\u538B\u529B\u79EF\u7D2F\u4E2D(${(stressDyn.level * 100).toFixed(0)}%)`);
    if (stressDyn.turnsToBreakdown !== null) parts.push(`\u9884\u8BA1${stressDyn.turnsToBreakdown}\u8F6E\u540E\u53EF\u80FD\u7206\u53D1`);
    if (stressDyn.phase === "releasing") parts.push("\u538B\u529B\u91CA\u653E\u4E2D");
  }
  const lc = fitLearningCurve(memoryState.chatHistory);
  if (lc.prediction && lc.prediction !== "\u6570\u636E\u4E0D\u8DB3") parts.push(lc.prediction);
  if (c.load === "high") parts.push("\u8D1F\u8377\u9AD8\u2192\u7B80\u6D01");
  else if (c.load === "low") parts.push("\u4E13\u6CE8\u2192\u53EF\u6DF1\u5165");
  if (sd.gaps.length > 0) parts.push(`\u8A00\u884C\u4E0D\u4E00:${sd.gaps[0].stated}`);
  if (u.needs[0]?.confidence > 0.5) parts.push(`\u6F5C\u5728\u9700\u6C42:${u.needs[0].domain}`);
  if (pm.identity) parts.push(pm.identity.slice(0, 60));
  return parts.join("\uFF1B");
}
function updateDeepUnderstand() {
  ensureMemoriesLoaded();
  if (memoryState.chatHistory.length < 10) return;
  state.temporal = analyzeTemporalPatterns();
  state.sayDo = analyzeSayDoGap();
  state.growth = analyzeGrowth();
  state.unspoken = analyzeUnspokenNeeds();
  state.cognitive = analyzeCognitiveLoad();
  state.stress = analyzeStress();
  state.dynamicProfile = synthesizeProfile();
  state.updatedAt = Date.now();
  debouncedSave(DU_PATH, state);
}
function getDeepUnderstandContext() {
  if (!state.updatedAt) return "";
  const parts = [];
  const { stress: s, cognitive: c, growth: g, unspoken: u, sayDo: sd, temporal: t } = state;
  if (s.stressLevel > 0.4) parts.push(`\u538B\u529B${(s.stressLevel * 10).toFixed(0)}/10(${s.signals.join(",")})`);
  if (c.load !== "normal") parts.push(c.load === "high" ? "\u8BA4\u77E5\u8D1F\u8377\u9AD8\u2192\u7B80\u6D01\u56DE\u590D" : "\u4E13\u6CE8\u6A21\u5F0F\u2192\u53EF\u6DF1\u5165");
  if (g.direction !== "plateauing") parts.push(g.direction === "growing" ? "\u6210\u957F\u671F\u2192\u9002\u5F53\u63D0\u9AD8\u96BE\u5EA6" : "\u74F6\u9888\u671F\u2192\u591A\u9F13\u52B1");
  if (u.needs[0]?.confidence > 0.5) parts.push(`\u53EF\u80FD\u9700\u8981${u.needs[0].domain}\u65B9\u9762\u7684\u5E2E\u52A9`);
  if (sd.gaps[0]) parts.push(`\u8BF4"${sd.gaps[0].stated}"\u4F46${sd.gaps[0].actual}\u2192\u6E29\u548C\u5F15\u5BFC`);
  if (t.lateNightFrequency > 0.4) parts.push("\u7ECF\u5E38\u6DF1\u591C\u6D3B\u8DC3");
  if (parts.length === 0) return "";
  return "[\u6DF1\u5C42\u7406\u89E3] " + parts.join("\uFF1B");
}
export {
  analyzeStressDynamics,
  fitLearningCurve,
  getDeepUnderstandContext,
  updateDeepUnderstand
};
