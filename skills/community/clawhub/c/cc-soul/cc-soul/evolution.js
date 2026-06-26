import { createHash } from "crypto";
import { existsSync, mkdirSync, writeFileSync, readFileSync, readdirSync } from "fs";
import { resolve } from "path";
import { RULES_PATH, HYPOTHESES_PATH, DATA_DIR, loadJson, debouncedSave } from "./persistence.ts";
import { addMemory, trigrams, trigramSimilarity } from "./memory.ts";
import { notifySoulActivity } from "./notify.ts";
import { queueLLMTask } from "./cli.ts";
import { extractJSON } from "./utils.ts";
import { getParam } from "./auto-tune.ts";
import { detectDomain } from "./epistemic.ts";
function betaMean(alpha, beta) {
  return alpha / (alpha + beta);
}
function betaLowerBound(alpha, beta, z = 1.96) {
  const n = alpha + beta - 2;
  if (n <= 0) return 0;
  const p = (alpha - 1) / n;
  return (p + z * z / (2 * n) - z * Math.sqrt((p * (1 - p) + z * z / (4 * n)) / n)) / (1 + z * z / n);
}
function isSignificant(alpha, beta, minSamples = 8) {
  return alpha + beta - 2 >= minSamples;
}
const MAX_RULES = 50;
let rules = [];
let hypotheses = [];
function getRules() {
  return rules;
}
function md5(s) {
  return createHash("md5").update(s).digest("hex").slice(0, 16);
}
function loadRules() {
  rules = loadJson(RULES_PATH, []);
}
function saveRules() {
  debouncedSave(RULES_PATH, rules);
}
function compressRules() {
  const MERGE_THRESHOLD = 0.6;
  const merged = /* @__PURE__ */ new Set();
  for (let i = 0; i < rules.length; i++) {
    if (merged.has(i)) continue;
    const triA = trigrams(rules[i].rule);
    for (let j = i + 1; j < rules.length; j++) {
      if (merged.has(j)) continue;
      const triB = trigrams(rules[j].rule);
      if (trigramSimilarity(triA, triB) > MERGE_THRESHOLD) {
        const [keep, drop] = rules[i].hits >= rules[j].hits ? [i, j] : [j, i];
        rules[keep].hits += rules[drop].hits;
        rules[keep].rule = rules[keep].rule.length >= rules[drop].rule.length ? rules[keep].rule : rules[drop].rule;
        merged.add(drop);
        console.log(`[cc-soul][evolve] rule compress: merged "${rules[drop].rule.slice(0, 30)}" into "${rules[keep].rule.slice(0, 30)}"`);
        if (drop === i) break;
      }
    }
  }
  if (merged.size > 0) {
    const before = rules.length;
    const kept = rules.filter((_, idx) => !merged.has(idx));
    rules.length = 0;
    rules.push(...kept);
    console.log(`[cc-soul][evolve] rule compress: ${before} \u2192 ${rules.length} (merged ${merged.size})`);
  }
}
const DOMAIN_GENERALIZATION = {
  python: "\u56DE\u7B54 Python \u76F8\u5173\u95EE\u9898\u65F6\u8981\u7279\u522B\u8C28\u614E\uFF0C\u5148\u786E\u8BA4\u7248\u672C\u53F7\u548C\u5177\u4F53\u7279\u6027\u518D\u56DE\u7B54",
  javascript: "\u56DE\u7B54 JS/TS \u76F8\u5173\u95EE\u9898\u65F6\u6CE8\u610F\u533A\u5206\u8FD0\u884C\u65F6\u548C\u6846\u67B6\u7248\u672C\u5DEE\u5F02",
  swift: "\u56DE\u7B54 Swift \u76F8\u5173\u95EE\u9898\u65F6\u6CE8\u610F\u533A\u5206 Swift \u7248\u672C\u548C API \u53D8\u66F4",
  "ios-reverse": "\u56DE\u7B54 iOS \u9006\u5411\u95EE\u9898\u65F6\u6CE8\u610F\u5DE5\u5177\u7248\u672C\u548C\u7CFB\u7EDF\u517C\u5BB9\u6027",
  rust: "\u56DE\u7B54 Rust \u95EE\u9898\u65F6\u6CE8\u610F edition \u548C API \u7A33\u5B9A\u6027\u5DEE\u5F02",
  golang: "\u56DE\u7B54 Go \u95EE\u9898\u65F6\u6CE8\u610F\u7248\u672C\u548C\u6A21\u5757\u7CFB\u7EDF\u5DEE\u5F02",
  database: "\u56DE\u7B54\u6570\u636E\u5E93\u95EE\u9898\u65F6\u6CE8\u610F\u5F15\u64CE\u5DEE\u5F02\u548C\u7248\u672C\u517C\u5BB9",
  devops: "\u56DE\u7B54\u8FD0\u7EF4\u95EE\u9898\u65F6\u6CE8\u610F\u53D1\u884C\u7248\u548C\u5DE5\u5177\u7248\u672C\u5DEE\u5F02",
  git: "\u56DE\u7B54 Git \u95EE\u9898\u65F6\u6CE8\u610F\u4E0D\u540C\u5E73\u53F0\u548C\u7248\u672C\u7684\u884C\u4E3A\u5DEE\u5F02"
};
function distillRules(ruleList) {
  if (ruleList.length < 2) return null;
  try {
    const { extractFacts } = require("./fact-store.ts");
    const allFacts = ruleList.flatMap((r) => extractFacts(r.rule || r.text || ""));
    const predCounts = /* @__PURE__ */ new Map();
    for (const f of allFacts) {
      const key = `${f.subject}:${f.predicate}`;
      predCounts.set(key, (predCounts.get(key) || 0) + 1);
    }
    const common = [...predCounts.entries()].filter(([, c]) => c >= 2).map(([k]) => k.replace(":", " \u2192 "));
    if (common.length > 0) return `[\u89C4\u5219\u5171\u6027] ${common.join("; ")}`;
  } catch {
  }
  const wordSets = ruleList.map((r) => {
    const text = r.rule || r.text || "";
    return new Set((text.match(/[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}/gi) || []).map((w) => w.toLowerCase()));
  });
  let intersection = new Set(wordSets[0] || []);
  for (let i = 1; i < wordSets.length; i++) {
    intersection = new Set([...intersection].filter((w) => wordSets[i].has(w)));
  }
  if (intersection.size >= 2) return `[${[...intersection].slice(0, 3).join("/")}] \u6CE8\u610F\u76F8\u5173\u95EE\u9898`;
  return null;
}
function generalizeRules(newRuleText) {
  const domain = detectDomain(newRuleText);
  const template = DOMAIN_GENERALIZATION[domain];
  if (!template) return;
  const sameDomain = rules.filter((r) => detectDomain(r.rule) === domain && r.source !== "generalized");
  if (sameDomain.length < 2) return;
  const distilled = distillRules(sameDomain);
  const ruleText = distilled || template;
  const existing = rules.find((r) => r.rule === ruleText);
  if (existing) {
    existing.hits = Math.max(existing.hits, ...sameDomain.map((r) => r.hits)) + 1;
    return;
  }
  const maxHits = Math.max(...sameDomain.map((r) => r.hits), 1);
  rules.push({ rule: ruleText, source: "generalized", ts: Date.now(), hits: maxHits + 1 });
  console.log(`[cc-soul][evolve] generalized rule for domain=${domain}: "${ruleText.slice(0, 50)}"`);
}
function addRule(rule, source) {
  if (!rule || rule.length < 5) return;
  if (rules.some((r) => r.rule === rule)) return;
  const newTrigrams = trigrams(rule);
  const similar = rules.find((r) => trigramSimilarity(trigrams(r.rule), newTrigrams) > getParam("evolution.rule_dedup_threshold"));
  if (similar) {
    similar.hits++;
    console.log(`[cc-soul][evolve] rule dedup: "${rule.slice(0, 40)}" merged into "${similar.rule.slice(0, 40)}"`);
    saveRules();
    return;
  }
  const CJK_RE = /[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi;
  const conditions = (rule.match(CJK_RE) || []).map((w) => w.toLowerCase()).slice(0, 5);
  rules.push({
    rule,
    source: source.slice(0, 100),
    ts: Date.now(),
    hits: 0,
    cause: source.includes("\u7EA0\u6B63") || source.includes("correction") ? source.slice(0, 80) : void 0,
    conditions: conditions.length > 0 ? conditions : void 0
  });
  generalizeRules(rule);
  if (rules.length > 40) {
    compressRules();
  }
  if (rules.length > MAX_RULES) {
    rules.sort((a, b) => b.hits * 10 + b.ts / 1e10 - (a.hits * 10 + a.ts / 1e10) || b.ts - a.ts);
    rules.length = MAX_RULES;
  }
  saveRules();
}
function getRelevantRules(msg, topN = 3, trackHits = true) {
  if (rules.length === 0) return [];
  const msgWords = new Set((msg.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map((w) => w.toLowerCase()));
  if (msgWords.size === 0) return rules.slice(0, topN);
  const scored = rules.map((r) => {
    const ruleWords = (r.rule.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map((w) => w.toLowerCase());
    const overlap = ruleWords.filter((w) => msgWords.has(w)).length;
    let conditionBoost = 0;
    if (r.conditions && r.conditions.length > 0) {
      const condHits = r.conditions.filter((c) => msgWords.has(c)).length;
      conditionBoost = condHits / r.conditions.length;
      if (condHits === 0 && r.conditions.length >= 2) conditionBoost = -0.5;
    }
    let qualityBoost = 0;
    if (r.matchedCount && r.matchedCount >= 3 && r.matchedQualitySum) {
      const avgQuality = r.matchedQualitySum / r.matchedCount;
      qualityBoost = avgQuality >= 7 ? 0.5 : avgQuality <= 3 ? -0.5 : 0;
    }
    return { ...r, score: overlap + r.hits * 0.1 + conditionBoost + qualityBoost };
  });
  scored.sort((a, b) => b.score - a.score);
  const relevant = scored.filter((r) => r.score > 0).slice(0, topN);
  if (trackHits) {
    for (const r of relevant) {
      const orig = rules.find((o) => o.rule === r.rule);
      if (orig) {
        orig.hits++;
        orig.matchedCount = (orig.matchedCount || 0) + 1;
      }
    }
  }
  return relevant;
}
function loadHypotheses() {
  hypotheses = loadJson(HYPOTHESES_PATH, []);
  for (const h of hypotheses) {
    if (h.alpha === void 0 || h.beta === void 0) {
      h.alpha = 1 + (h.evidence_for || 0);
      h.beta = 1 + (h.evidence_against || 0);
    }
  }
}
function formHypothesis(pattern, observation) {
  const id = md5(pattern);
  if (hypotheses.some((h) => h.id === id)) return;
  hypotheses.push({
    id,
    description: `\u5F53\u9047\u5230"${pattern.slice(0, 30)}"\u65F6: ${observation.slice(0, 60)}`,
    alpha: 2,
    // prior Beta(1,1) + 1 initial success observation
    beta: 1,
    status: "active",
    created: Date.now(),
    verifyCount: 0
  });
  if (hypotheses.length > 30) {
    const kept = hypotheses.filter((h) => h.status !== "rejected").sort((a, b) => betaMean(b.alpha, b.beta) - betaMean(a.alpha, a.beta) || b.created - a.created).slice(0, 25);
    hypotheses.length = 0;
    hypotheses.push(...kept);
  }
  saveHypothesesSafe();
  console.log(`[cc-soul][evolve] \u65B0\u5047\u8BBE: ${pattern.slice(0, 30)} \u2192 ${observation.slice(0, 40)}`);
  notifySoulActivity(`\u{1F9EC} \u65B0\u5047\u8BBE: ${pattern.slice(0, 30)} \u2192 ${observation.slice(0, 40)}`).catch(() => {
  });
}
function saveHypothesesSafe() {
  if (hypotheses === void 0 || hypotheses === null) return;
  debouncedSave(HYPOTHESES_PATH, hypotheses);
}
let _verifyingHypotheses = false;
function verifyHypothesis(situation, wasCorrect) {
  if (_verifyingHypotheses) return;
  _verifyingHypotheses = true;
  try {
    if (hypotheses.length === 0) {
      try {
        loadHypotheses();
      } catch {
      }
    }
    if (hypotheses.length === 0) {
      _verifyingHypotheses = false;
      return;
    }
    _verifyHypothesisInner(situation, wasCorrect);
  } finally {
    _verifyingHypotheses = false;
  }
}
function _verifyHypothesisInner(situation, wasCorrect) {
  for (const h of hypotheses) {
    if (h.status === "rejected" || h.status === "verified") continue;
    const sim = trigramSimilarity(trigrams(h.description), trigrams(situation));
    if (sim < 0.2) continue;
    if (!h.verifyCount) h.verifyCount = 0;
    if (wasCorrect) {
      h.alpha++;
    } else {
      h.beta++;
    }
    const mean = betaMean(h.alpha, h.beta);
    console.log(`[cc-soul][evolve] \u5047\u8BBE\u9A8C\u8BC1: "${h.description.slice(0, 40)}" sim=${sim.toFixed(2)} correct=${wasCorrect} verify=${h.verifyCount} \u03B1=${h.alpha} \u03B2=${h.beta}`);
    if (wasCorrect) {
      h.verifyCount++;
    } else {
      h.verifyCount = 0;
    }
    if (wasCorrect && h.verifyCount >= 3 && h.status === "active") {
      h.status = "verified";
      addRule(h.description, "hypothesis_solidified");
      console.log(`[cc-soul][evolve] \u89C4\u5219\u56FA\u5316: ${h.description.slice(0, 40)} (\u9A8C\u8BC1${h.verifyCount}\u6B21)`);
      notifySoulActivity(`\u{1F512} \u89C4\u5219\u56FA\u5316: ${h.description.slice(0, 40)}`).catch(() => {
      });
      continue;
    }
    if (h.status === "active" && isSignificant(h.alpha, h.beta) && 1 - betaLowerBound(h.beta, h.alpha) < getParam("evolution.hypothesis_reject_ci_ub")) {
      h.status = "rejected";
      console.log(`[cc-soul][evolve] \u5047\u8BBE\u88AB\u5426\u5B9A: ${h.description.slice(0, 40)} (mean=${mean.toFixed(3)})`);
      notifySoulActivity(`\u274C \u5047\u8BBE\u5426\u5B9A: ${h.description.slice(0, 40)}`).catch(() => {
      });
    }
  }
  saveHypothesesSafe();
}
function onCorrectionEvolution(userMsg) {
  const patterns = [
    /不要(.{2,30})/,
    /别(.{2,20})/,
    /应该(.{2,30})/,
    /正确的是(.{2,30})/
  ];
  for (const p of patterns) {
    const m = userMsg.match(p);
    if (m) {
      addRule(m[0], userMsg.slice(0, 80));
      break;
    }
  }
  addMemory(`\u7EA0\u6B63: ${userMsg.slice(0, 60)}`, "correction");
}
function onCorrectionAdvanced(userMsg, lastResponse) {
  onCorrectionEvolution(userMsg);
  const causalPatterns = [
    { pattern: /太长|太啰嗦|简洁/, cause: "\u56DE\u7B54\u592A\u5197\u957F\uFF0C\u7528\u6237\u8981\u7B80\u6D01" },
    { pattern: /跑偏|离题|不是问/, cause: "\u7406\u89E3\u504F\u4E86\uFF0C\u6CA1\u56DE\u7B54\u5230\u70B9\u4E0A" },
    { pattern: /不准|不对|错误/, cause: "\u4FE1\u606F\u4E0D\u51C6\u786E" },
    { pattern: /口气|语气|态度/, cause: "\u8BED\u6C14\u4E0D\u5BF9" },
    { pattern: /太简单|没深度|浅/, cause: "\u56DE\u7B54\u592A\u6D45" }
  ];
  for (const { pattern, cause } of causalPatterns) {
    if (pattern.test(userMsg)) {
      formHypothesis(userMsg.slice(0, 50), cause);
      break;
    }
  }
  verifyHypothesis(lastResponse, false);
}
function attributeCorrection(userMsg, lastResponse, augmentsUsed) {
  queueLLMTask(
    `\u4E0A\u4E00\u6B21\u56DE\u590D: "${lastResponse.slice(0, 300)}"
\u6CE8\u5165\u7684\u4E0A\u4E0B\u6587: ${augmentsUsed.slice(0, 3).join("; ").slice(0, 200)}
\u7528\u6237\u7EA0\u6B63: "${userMsg.slice(0, 200)}"

\u5224\u65AD\u56DE\u590D\u51FA\u9519\u7684\u539F\u56E0\uFF08\u53EA\u9009\u4E00\u4E2A\uFF09:
1=\u6A21\u578B\u5E7B\u89C9 2=\u8BB0\u5FC6\u8BEF\u5BFC 3=\u89C4\u5219\u51B2\u7A81 4=\u7406\u89E3\u504F\u5DEE 5=\u9886\u57DF\u4E0D\u8DB3
\u683C\u5F0F: {"cause":N,"detail":"\u4E00\u53E5\u8BDD"}`,
    (output) => {
      try {
        const result = extractJSON(output);
        if (result) {
          const causeNames = ["", "\u6A21\u578B\u5E7B\u89C9", "\u8BB0\u5FC6\u8BEF\u5BFC", "\u89C4\u5219\u51B2\u7A81", "\u7406\u89E3\u504F\u5DEE", "\u9886\u57DF\u4E0D\u8DB3"];
          const causeName = causeNames[result.cause] || "\u672A\u77E5";
          console.log(`[cc-soul][attribution] cause=${causeName}: ${result.detail}`);
          addMemory(`[\u7EA0\u6B63\u5F52\u56E0] ${causeName}: ${result.detail}`, "correction");
        }
      } catch (e) {
        console.error(`[cc-soul][attribution] parse error: ${e.message}`);
      }
    },
    3,
    "attribution"
  );
}
function recordRuleQuality(matchedRules, qualityScore) {
  for (const r of matchedRules) {
    const orig = rules.find((o) => o.rule === r.rule);
    if (orig) {
      orig.matchedQualitySum = (orig.matchedQualitySum || 0) + qualityScore;
    }
  }
  saveRules();
}
function exportEvolutionAssets(stats) {
  const exportDir = resolve(DATA_DIR, "export");
  if (!existsSync(exportDir)) mkdirSync(exportDir, { recursive: true });
  const solidifiedCount = hypotheses.filter((h) => h.status === "verified").length;
  const skillsDir = resolve(DATA_DIR, "skills/auto");
  let skillNames = [];
  try {
    if (existsSync(skillsDir)) {
      skillNames = readdirSync(skillsDir).filter((f) => f.endsWith(".md"));
    }
  } catch {
  }
  const growthVectors = [];
  const data = {
    version: "1.0",
    format: "GEP",
    exportedAt: (/* @__PURE__ */ new Date()).toISOString(),
    agent: "cc-soul",
    assets: {
      rules: rules.map((r) => ({ ...r })),
      hypotheses: hypotheses.map((h) => ({ ...h })),
      skills: skillNames,
      stats: {
        totalMessages: stats.totalMessages,
        corrections: stats.corrections,
        rulesSolidified: solidifiedCount
      },
      // legacy fields for backward compat
      corrections: stats.corrections,
      growthVectors,
      metadata: {
        totalMessages: stats.totalMessages,
        firstSeen: stats.firstSeen,
        rulesSolidified: solidifiedCount
      }
    }
  };
  const today = (/* @__PURE__ */ new Date()).toISOString().slice(0, 10);
  const exportPath = resolve(exportDir, `evolution_assets_${today}.json`);
  writeFileSync(exportPath, JSON.stringify(data, null, 2), "utf-8");
  console.log(`[cc-soul][gep] exported ${rules.length} rules + ${hypotheses.length} hypotheses to ${exportPath}`);
  return { data, path: exportPath };
}
function importEvolutionAssets(filePath) {
  const raw = readFileSync(filePath, "utf-8");
  const data = JSON.parse(raw);
  if (!data.version || !data.assets) {
    throw new Error("Invalid GEP format: missing version or assets");
  }
  let rulesAdded = 0;
  let hypothesesAdded = 0;
  if (Array.isArray(data.assets.rules)) {
    for (const r of data.assets.rules) {
      if (!r.rule || r.rule.length < 5) continue;
      if (rules.some((existing) => existing.rule === r.rule)) continue;
      rules.push({
        rule: r.rule,
        source: r.source || "gep_import",
        ts: r.ts || Date.now(),
        hits: r.hits || 0,
        matchedCount: r.matchedCount,
        matchedQualitySum: r.matchedQualitySum
      });
      rulesAdded++;
    }
    if (rules.length > MAX_RULES) {
      rules.sort((a, b) => b.hits * 10 + b.ts / 1e10 - (a.hits * 10 + a.ts / 1e10) || b.ts - a.ts);
      rules.length = MAX_RULES;
    }
    saveRules();
  }
  if (Array.isArray(data.assets.hypotheses)) {
    for (const h of data.assets.hypotheses) {
      if (!h.id || !h.description) continue;
      if (hypotheses.some((existing) => existing.id === h.id)) continue;
      hypotheses.push({
        id: h.id,
        description: h.description,
        alpha: h.alpha ?? 2,
        beta: h.beta ?? 1,
        status: h.status || "active",
        created: h.created || Date.now(),
        verifyCount: h.verifyCount || 0
      });
      hypothesesAdded++;
    }
    if (hypotheses.length > 30) {
      const kept = hypotheses.filter((h) => h.status !== "rejected").sort((a, b) => b.alpha / (b.alpha + b.beta) - a.alpha / (a.alpha + a.beta) || b.created - a.created).slice(0, 25);
      hypotheses.length = 0;
      hypotheses.push(...kept);
    }
    saveHypothesesSafe();
  }
  console.log(`[cc-soul][gep] imported ${rulesAdded} rules + ${hypothesesAdded} hypotheses from ${filePath}`);
  return { rulesAdded, hypothesesAdded };
}
const EVOLUTIONS_PATH = resolve(DATA_DIR, "evolutions.json");
let evolutions = loadJson(EVOLUTIONS_PATH, []);
function loadEvolutions() {
  evolutions = loadJson(EVOLUTIONS_PATH, []);
}
function startEvolution(goal, phaseDescriptions, phaseDurationDays = 2) {
  const id = `evo_${Date.now()}`;
  const phases = phaseDescriptions.map((desc, i) => ({
    phase: i + 1,
    description: desc,
    status: i === 0 ? "active" : "pending",
    startedAt: i === 0 ? Date.now() : 0,
    duration: phaseDurationDays * 864e5,
    metrics: null
  }));
  evolutions.push({ id, goal, phases, currentPhase: 0, startedAt: Date.now(), status: "in_progress" });
  debouncedSave(EVOLUTIONS_PATH, evolutions);
  return id;
}
function checkEvolutionProgress() {
  const now = Date.now();
  for (const evo of evolutions) {
    if (evo.status !== "in_progress") continue;
    const current = evo.phases[evo.currentPhase];
    if (!current || current.status !== "active") continue;
    if (now - current.startedAt < current.duration) continue;
    current.status = "completed";
    const next = evo.phases[evo.currentPhase + 1];
    if (next) {
      next.status = "active";
      next.startedAt = now;
      evo.currentPhase++;
    } else {
      evo.status = "completed";
    }
    debouncedSave(EVOLUTIONS_PATH, evolutions);
  }
}
function getEvolutionSummary() {
  const active = evolutions.filter((e) => e.status === "in_progress");
  if (active.length === 0) return "";
  return active.map((e) => {
    const p = e.phases[e.currentPhase];
    return `\u8FDB\u5316: ${e.goal} \u2014 \u9636\u6BB5 ${p?.phase ?? "?"}/${e.phases.length}: ${p?.description ?? "?"}`;
  }).join("\n");
}
const evolutionModule = {
  id: "evolution",
  name: "\u8FDB\u5316\u5F15\u64CE",
  dependencies: ["memory"],
  priority: 50,
  init() {
    loadRules();
    loadHypotheses();
    loadEvolutions();
  }
};
export {
  addRule,
  attributeCorrection,
  checkEvolutionProgress,
  evolutionModule,
  exportEvolutionAssets,
  formHypothesis,
  generalizeRules,
  getEvolutionSummary,
  getRelevantRules,
  getRules,
  hypotheses,
  importEvolutionAssets,
  loadEvolutions,
  loadHypotheses,
  loadRules,
  onCorrectionAdvanced,
  recordRuleQuality,
  rules,
  startEvolution,
  verifyHypothesis
};
