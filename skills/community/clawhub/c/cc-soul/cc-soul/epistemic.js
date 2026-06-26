import { resolve } from "path";
import { DATA_DIR, loadJson, debouncedSave } from "./persistence.ts";
const EPISTEMIC_PATH = resolve(DATA_DIR, "epistemic.json");
const domains = /* @__PURE__ */ new Map();
let _domainCache = null;
const DOMAIN_KEYWORDS = [
  { domain: "ios-reverse", words: ["frida", "hook", "ida", "mach-o", "dyld", "arm64", "objc", "\u9006\u5411", "\u7838\u58F3", "tweak", "substrate", "theos", "cycript", "reverse engineering", "binary analysis"], specificity: 0.95 },
  { domain: "rust", words: ["rust", "cargo", ".rs", "lifetime", "borrow checker"], specificity: 0.9 },
  { domain: "swift", words: ["swift", "xcode", "swiftui", "uikit", "cocoa", "appkit"], specificity: 0.85 },
  { domain: "golang", words: ["go ", "golang", "goroutine", ".go", "func "], specificity: 0.85 },
  { domain: "python", words: ["python", "pip", "flask", "django", "def ", "import ", ".py", "asyncio", "pandas"], specificity: 0.7 },
  { domain: "javascript", words: ["typescript", "javascript", "node", "react", "vue", ".ts", ".js", "npm", "pnpm", "bun"], specificity: 0.7 },
  { domain: "devops", words: ["docker", "k8s", "kubernetes", "nginx", "linux", "bash", "shell", "systemd", "ssh"], specificity: 0.75 },
  { domain: "database", words: ["sql", "mysql", "postgres", "mongodb", "\u6570\u636E\u5E93", "redis", "sqlite", "database", "query", "index", "schema"], specificity: 0.8 },
  { domain: "\u56FE\u7247\u8BC6\u522B", words: ["\u56FE\u7247", "ocr", "\u8BC6\u522B", "\u7167\u7247", "\u622A\u56FE", "\u770B\u770B\u8FD9\u4E2A", "\u8FD9\u5F20\u56FE", "image recognition", "computer vision"], specificity: 0.85 },
  { domain: "git", words: ["git", "github", "pr", "merge", "branch", "commit", "rebase"], specificity: 0.8 }
];
function detectDomain(msg) {
  if (_domainCache?.msg === msg) return _domainCache.result;
  const m = msg.toLowerCase();
  let bestDomain = "\u901A\u7528";
  let bestScore = 0;
  for (const { domain, words, specificity } of DOMAIN_KEYWORDS) {
    const hits = words.filter((w) => m.includes(w)).length;
    if (hits > 0) {
      const score = hits * specificity;
      if (score > bestScore) {
        bestScore = score;
        bestDomain = domain;
      }
    }
  }
  if (bestDomain === "\u901A\u7528") {
    try {
      const { getCooccurrence } = require("./aam.ts");
      const msgWords = (m.match(/[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}/gi) || []).map((w) => w.toLowerCase());
      for (const mw of msgWords) {
        for (const { domain, words } of DOMAIN_KEYWORDS) {
          for (const dw of words.slice(0, 3)) {
            if (getCooccurrence(mw, dw) >= 5) {
              bestDomain = domain;
              break;
            }
          }
          if (bestDomain !== "\u901A\u7528") break;
        }
        if (bestDomain !== "\u901A\u7528") break;
      }
    } catch {
    }
  }
  if (bestDomain === "\u901A\u7528") {
    if (msg.length < 20) bestDomain = "\u95F2\u804A";
    else if (["\u600E\u4E48\u770B", "\u4F60\u89C9\u5F97", "\u5EFA\u8BAE", "\u5E94\u8BE5", "\u63A8\u8350", "what do you think", "advice", "suggest", "recommend", "should i", "consultation"].some((w) => m.includes(w))) bestDomain = "\u54A8\u8BE2";
    else if (["chat", "casual", "hey", "hi ", "hello", "sup", "what's up"].some((w) => m.includes(w)) && msg.length < 30) bestDomain = "\u95F2\u804A";
  }
  _domainCache = { msg, result: bestDomain };
  return bestDomain;
}
function loadEpistemic() {
  const raw = loadJson(EPISTEMIC_PATH, {});
  domains.clear();
  for (const [k, v] of Object.entries(raw)) {
    domains.set(k, v);
  }
  console.log(`[cc-soul][epistemic] loaded ${domains.size} domains`);
}
function saveEpistemic() {
  const obj = {};
  for (const [k, v] of domains) {
    obj[k] = v;
  }
  debouncedSave(EPISTEMIC_PATH, obj);
}
function ensureDomain(domain) {
  let d = domains.get(domain);
  if (!d) {
    d = { domain, totalResponses: 0, qualitySum: 0, corrections: 0, avgQuality: 5, correctionRate: 0 };
    domains.set(domain, d);
  }
  return d;
}
function recompute(d) {
  d.avgQuality = d.totalResponses > 0 ? Math.round(d.qualitySum / d.totalResponses * 10) / 10 : 5;
  d.correctionRate = d.totalResponses > 0 ? Math.round((d.corrections + 1) / (d.totalResponses + 2) * 1e3) / 10 : 0;
}
function trackDomainQuality(msg, score) {
  const domain = detectDomain(msg);
  const d = ensureDomain(domain);
  d.totalResponses++;
  d.qualitySum += score;
  recompute(d);
  saveEpistemic();
}
function trackDomainCorrection(msg) {
  const domain = detectDomain(msg);
  const d = ensureDomain(domain);
  d.corrections++;
  recompute(d);
  saveEpistemic();
}
function computeKnowledgeDecay(domain, domainData) {
  const total = domainData?.totalResponses || 0;
  const corrections = domainData?.corrections || 0;
  const avgQuality = total > 0 ? (domainData?.qualitySum || 5 * total) / total : 5;
  const lastCorrectionTs = domainData?.lastCorrectionTs || 0;
  const daysSinceCorrection = lastCorrectionTs > 0 ? (Date.now() - lastCorrectionTs) / 864e5 : 999;
  const base = 1 / (1 + Math.exp(-(avgQuality - 5) * 0.8));
  const correctionRate = total > 0 ? (corrections + 1) / (total + 2) : 0;
  const halfLife = Math.max(3, 30 * (1 - correctionRate));
  const decay = correctionRate > 0 ? 0.3 * Math.exp(-daysSinceCorrection / halfLife) : 0;
  const confidence = Math.max(0.1, Math.min(0.95, base * (1 - decay)));
  let trend = "stable";
  if (total >= 5) {
    if (daysSinceCorrection < 3) trend = "degrading";
    else if (daysSinceCorrection > 14 && correctionRate < 0.1) trend = "improving";
  }
  return { domain, confidence, trend, halfLife, lastCorrection: daysSinceCorrection };
}
function getDomainConfidence(msg) {
  const domain = detectDomain(msg);
  const d = domains.get(domain);
  if (!d || d.totalResponses < 3) {
    return { domain, confidence: "medium", hint: "" };
  }
  const kd = computeKnowledgeDecay(domain, d);
  const confLabel = kd.confidence > 0.7 ? "high" : kd.confidence > 0.4 ? "medium" : "low";
  const hint = confLabel === "low" ? `[\u77E5\u8BC6\u8FB9\u754C] "${domain}" \u7F6E\u4FE1\u5EA6${(kd.confidence * 100).toFixed(0)}%\uFF0C${kd.trend === "degrading" ? "\u6700\u8FD1\u88AB\u7EA0\u6B63\u8FC7" : "\u5386\u53F2\u51C6\u786E\u7387\u4F4E"}\uFF0C\u8BF7\u4ED4\u7EC6\u6838\u5B9E` : "";
  return { domain, confidence: confLabel, hint, decay: kd };
}
function getWeakDomains() {
  return [...domains.values()].filter((d) => d.totalResponses >= 5 && (d.correctionRate > 10 || d.avgQuality < 5)).sort((a, b) => b.correctionRate - a.correctionRate).map((d) => d.domain);
}
function getCapabilityScore() {
  if (domains.size === 0) return "\u{1F3AF} \u80FD\u529B\u8BC4\u5206\n\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\n\u6682\u65E0\u6570\u636E\uFF0C\u9700\u8981\u66F4\u591A\u5BF9\u8BDD\u6765\u5EFA\u7ACB\u57DF\u7F6E\u4FE1\u5EA6\u3002";
  const entries = [...domains.values()].filter((d) => d.totalResponses >= 2).sort((a, b) => b.totalResponses - a.totalResponses);
  if (entries.length === 0) return "\u{1F3AF} \u80FD\u529B\u8BC4\u5206\n\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\n\u6837\u672C\u4E0D\u8DB3\uFF0C\u81F3\u5C11\u6BCF\u4E2A\u9886\u57DF 2 \u6B21\u5BF9\u8BDD\u3002";
  const lines = [
    "\u{1F3AF} \u80FD\u529B\u8BC4\u5206",
    "\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550",
    `${"\u57DF".padEnd(15)} ${"\u8D28\u91CF".padStart(5)} ${"\u7EA0\u6B63\u7387".padStart(7)} ${"\u6837\u672C".padStart(5)}`,
    "\u2500".repeat(35)
  ];
  for (const d of entries) {
    const bar = d.avgQuality >= 7 ? "\u2713" : d.avgQuality < 5 ? "\u2717" : "~";
    lines.push(`${bar} ${d.domain.padEnd(13)} ${d.avgQuality.toFixed(1).padStart(5)} ${(d.correctionRate + "%").padStart(7)} ${d.totalResponses.toString().padStart(5)}`);
  }
  const overall = entries.reduce((s, d) => s + d.qualitySum, 0) / Math.max(1, entries.reduce((s, d) => s + d.totalResponses, 0));
  lines.push("\u2500".repeat(35));
  lines.push(`\u7EFC\u5408\u8D28\u91CF: ${overall.toFixed(1)}/10`);
  return lines.join("\n");
}
function getEpistemicSummary() {
  if (domains.size === 0) return "";
  const entries = [...domains.values()].filter((d) => d.totalResponses >= 3).sort((a, b) => b.totalResponses - a.totalResponses);
  if (entries.length === 0) return "";
  const lines = [];
  const weak = entries.filter(
    (d) => d.correctionRate > 10 && d.totalResponses >= 5 || d.avgQuality < 5 && d.totalResponses >= 5
  );
  if (weak.length > 0) {
    lines.push("\u26A0 \u8584\u5F31\u9886\u57DF\uFF08\u56DE\u7B54\u524D\u8981\u683C\u5916\u8C28\u614E\uFF09\uFF1A");
    for (const d of weak) {
      lines.push(`- ${d.domain}: \u8D28\u91CF${d.avgQuality}/10, \u7EA0\u6B63\u7387${d.correctionRate}%, \u6837\u672C${d.totalResponses}`);
    }
  }
  const strong = entries.filter((d) => d.avgQuality > 7 && d.totalResponses >= 10);
  if (strong.length > 0) {
    lines.push("\u2713 \u64C5\u957F\u9886\u57DF\uFF1A");
    for (const d of strong) {
      lines.push(`- ${d.domain}: \u8D28\u91CF${d.avgQuality}/10, \u6837\u672C${d.totalResponses}`);
    }
  }
  return lines.join("\n");
}
function getGrowthVectors() {
  let rules = [];
  let stats = { totalMessages: 0, corrections: 0 };
  let getDbFn = () => null;
  try {
    rules = require("./evolution.ts").getRules?.() || [];
  } catch {
  }
  try {
    stats = require("./handler-state.ts").stats || stats;
  } catch {
  }
  try {
    const { getDb } = require("./sqlite-store.ts");
    getDbFn = getDb;
  } catch {
  }
  const vectors = [];
  const now = Date.now();
  const WEEK = 7 * 864e5;
  try {
    const db = getDbFn();
    if (db) {
      const cur7d = db.prepare("SELECT COUNT(*) as c FROM memories WHERE scope = 'correction' AND ts > ?").get(now - WEEK)?.c || 0;
      const prev7d = db.prepare("SELECT COUNT(*) as c FROM memories WHERE scope = 'correction' AND ts > ? AND ts <= ?").get(now - 2 * WEEK, now - WEEK)?.c || 0;
      const curChats = db.prepare("SELECT COUNT(*) as c FROM chat_history WHERE ts > ?").get(now - WEEK)?.c || 1;
      const prevChats = db.prepare("SELECT COUNT(*) as c FROM chat_history WHERE ts > ? AND ts <= ?").get(now - 2 * WEEK, now - WEEK)?.c || 1;
      const curRate = cur7d / curChats;
      const prevRate = prev7d / prevChats;
      const trend = curRate < prevRate - 0.02 ? "up" : curRate > prevRate + 0.02 ? "down" : "stable";
      vectors.push({
        dimension: "correction_rate",
        current: Math.round(curRate * 1e3) / 10,
        trend,
        label: `\u7EA0\u6B63\u7387 ${(curRate * 100).toFixed(1)}%${trend === "up" ? " (\u6539\u5584\u4E2D)" : trend === "down" ? " (\u9700\u6CE8\u610F)" : ""}`
      });
    }
  } catch {
  }
  try {
    const ruleCount = rules.length;
    const recentRules = rules.filter((r) => now - r.ts < WEEK).length;
    const trend = recentRules >= 3 ? "up" : recentRules === 0 ? "stable" : "stable";
    vectors.push({
      dimension: "rule_count",
      current: ruleCount,
      trend,
      label: `\u89C4\u5219 ${ruleCount} \u6761 (\u672C\u5468+${recentRules})`
    });
  } catch {
  }
  try {
    const db = getDbFn();
    if (db) {
      const curAvg = db.prepare("SELECT AVG(confidence) as avg FROM memories WHERE scope != 'expired' AND scope != 'decayed' AND ts > ?").get(now - WEEK)?.avg;
      const prevAvg = db.prepare("SELECT AVG(confidence) as avg FROM memories WHERE scope != 'expired' AND scope != 'decayed' AND ts > ? AND ts <= ?").get(now - 2 * WEEK, now - WEEK)?.avg;
      if (curAvg != null) {
        const cur = Math.round(curAvg * 100) / 100;
        const trend = prevAvg != null ? curAvg > prevAvg + 0.03 ? "up" : curAvg < prevAvg - 0.03 ? "down" : "stable" : "stable";
        vectors.push({
          dimension: "memory_quality",
          current: cur,
          trend,
          label: `\u8BB0\u5FC6\u8D28\u91CF ${cur.toFixed(2)}${trend === "up" ? " (\u63D0\u5347)" : trend === "down" ? " (\u4E0B\u964D)" : ""}`
        });
      }
    }
  } catch {
  }
  try {
    const db = getDbFn();
    if (db) {
      const totalRecalled = db.prepare("SELECT COUNT(*) as c FROM memories WHERE recallCount > 0 AND scope != 'expired'").get()?.c || 0;
      const highRecall = db.prepare("SELECT COUNT(*) as c FROM memories WHERE recallCount >= 3 AND scope != 'expired'").get()?.c || 0;
      const accuracy = totalRecalled > 0 ? highRecall / totalRecalled : 0;
      vectors.push({
        dimension: "recall_accuracy",
        current: Math.round(accuracy * 100),
        trend: accuracy > 0.3 ? "up" : accuracy < 0.1 ? "down" : "stable",
        label: `\u53EC\u56DE\u51C6\u786E\u7387 ${(accuracy * 100).toFixed(0)}% (\u9AD8\u9891\u547D\u4E2D ${highRecall}/${totalRecalled})`
      });
    }
  } catch {
  }
  try {
    const domainCount = domains.size;
    const activeDomains = [...domains.values()].filter((d) => d.totalResponses >= 3).length;
    vectors.push({
      dimension: "domain_breadth",
      current: activeDomains,
      trend: activeDomains > 5 ? "up" : "stable",
      label: `\u9886\u57DF\u8986\u76D6 ${activeDomains} \u4E2A\u6D3B\u8DC3\u9886\u57DF (\u5171 ${domainCount})`
    });
  } catch {
  }
  return vectors;
}
function formatGrowthVectors() {
  const vectors = getGrowthVectors();
  if (vectors.length === 0) return "\u6210\u957F\u8F68\u8FF9: \u6570\u636E\u4E0D\u8DB3\uFF0C\u9700\u8981\u66F4\u591A\u5BF9\u8BDD\u79EF\u7D2F\u3002";
  const trendIcon = (t) => t === "up" ? "\u{1F4C8}" : t === "down" ? "\u{1F4C9}" : "\u27A1\uFE0F";
  const lines = [
    "\u{1F331} \u6210\u957F\u8F68\u8FF9",
    "\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550",
    ...vectors.map((v) => `  ${trendIcon(v.trend)} ${v.label}`)
  ];
  return lines.join("\n");
}
const PENDING_Q_PATH = resolve(DATA_DIR, "pending_questions.json");
const DOMAIN_QUESTIONS = {
  python: ["Python \u7248\u672C\u7528 3.x \u54EA\u4E2A\uFF1F", "\u5199\u6D4B\u8BD5\u7528 pytest \u8FD8\u662F unittest\uFF1F", "\u5305\u7BA1\u7406\u7528 pip/poetry/uv\uFF1F", "IDE \u7528\u4EC0\u4E48\uFF1FPyCharm/VS Code\uFF1F"],
  devops: ["CI/CD \u7528\u4EC0\u4E48\uFF1FGitHub Actions/Jenkins\uFF1F", "\u5BB9\u5668\u5316\u4E86\u5417\uFF1FDocker/Podman\uFF1F", "\u4E91\u670D\u52A1\u5546\u7528\u54EA\u5BB6\uFF1F"],
  database: ["\u4E3B\u529B\u6570\u636E\u5E93\u7528\u4EC0\u4E48\uFF1F", "\u7528 ORM \u8FD8\u662F\u88F8 SQL\uFF1F", "\u5907\u4EFD\u7B56\u7565\u662F\u4EC0\u4E48\u6837\u7684\uFF1F"],
  javascript: ["\u524D\u7AEF\u6846\u67B6\u7528 React/Vue/\u5176\u4ED6\uFF1F", "\u6784\u5EFA\u5DE5\u5177\u7528 Vite/Webpack\uFF1F", "\u72B6\u6001\u7BA1\u7406\u7528\u4EC0\u4E48\u65B9\u6848\uFF1F"],
  swift: ["SwiftUI \u8FD8\u662F UIKit \u4E3A\u4E3B\uFF1F", "Xcode \u7248\u672C\uFF1F", "\u5305\u7BA1\u7406\u7528 SPM \u8FD8\u662F CocoaPods\uFF1F"],
  git: ["Git \u5DE5\u4F5C\u6D41\u7528\u4EC0\u4E48\uFF1FGitFlow/Trunk-based\uFF1F", "Code review \u6D41\u7A0B\u662F\u600E\u6837\u7684\uFF1F"]
};
let pendingQuestions = loadJson(PENDING_Q_PATH, []);
function scanBlindSpotQuestions() {
  let pm = null;
  try {
    pm = require("./person-model.ts").getPersonModel?.();
  } catch {
  }
  const knownText = pm ? JSON.stringify(pm).toLowerCase() : "";
  const active = [...domains.values()].filter((d) => d.totalResponses >= 5).sort((a, b) => b.totalResponses - a.totalResponses);
  const SEVEN_DAYS = 7 * 864e5;
  pendingQuestions = pendingQuestions.filter((q) => !q.askedAt || Date.now() - q.askedAt < SEVEN_DAYS);
  for (const d of active) {
    if (pendingQuestions.filter((q) => !q.askedAt).length >= 3) break;
    const templates = DOMAIN_QUESTIONS[d.domain];
    if (!templates) continue;
    for (const tpl of templates) {
      if (pendingQuestions.some((q) => q.question === tpl)) continue;
      const keywords = tpl.match(/[\u4e00-\u9fa5a-zA-Z]{2,}/g) || [];
      if (keywords.some((k) => knownText.includes(k.toLowerCase()))) continue;
      pendingQuestions.push({ domain: d.domain, question: tpl, createdAt: Date.now() });
      break;
    }
  }
  debouncedSave(PENDING_Q_PATH, pendingQuestions);
}
function popBlindSpotQuestion() {
  const q = pendingQuestions.find((q2) => !q2.askedAt);
  if (!q) return null;
  q.askedAt = Date.now();
  debouncedSave(PENDING_Q_PATH, pendingQuestions);
  return `[\u4E3B\u52A8\u63D0\u95EE] \u7528\u6237\u7ECF\u5E38\u804A ${q.domain} \u4F46\u4ECE\u6CA1\u63D0\u8FC7\u76F8\u5173\u504F\u597D\uFF0C\u53EF\u4EE5\u81EA\u7136\u5730\u95EE\u4E00\u4E0B\uFF1A${q.question}`;
}
const epistemicModule = {
  id: "epistemic",
  name: "\u77E5\u8BC6\u8FB9\u754C\u81EA\u89C9",
  priority: 50,
  init() {
    loadEpistemic();
  }
};
export {
  computeKnowledgeDecay,
  detectDomain,
  epistemicModule,
  formatGrowthVectors,
  getCapabilityScore,
  getDomainConfidence,
  getEpistemicSummary,
  getGrowthVectors,
  getWeakDomains,
  loadEpistemic,
  popBlindSpotQuestion,
  scanBlindSpotQuestions,
  trackDomainCorrection,
  trackDomainQuality
};
