import { resolve } from "path";
import { DATA_DIR, loadJson, debouncedSave } from "./persistence.ts";
const PRIORITY_TIERS = [
  ["\u89C4\u5219", "\u6CE8\u610F\u89C4\u5219", "\u7EA0\u6B63"],
  // Tier 0: rules
  ["\u8BA1\u5212", "\u884C\u52A8\u8BA1\u5212", "\u7B56\u7565"],
  // Tier 1: plans
  ["\u77E5\u8BC6\u8FB9\u754C", "\u4E0D\u64C5\u957F", "\u64C5\u957F\u9886\u57DF", "\u786E\u5B9A\u6027"],
  // Tier 2: epistemic
  ["\u8BB0\u5FC6", "\u76F8\u5173\u8BB0\u5FC6", "\u786E\u5B9A\u6027\u77E5\u8BC6", "\u5386\u53F2"]
  // Tier 3: memory
];
function getTier(text) {
  const lower = text.toLowerCase();
  for (let i = 0; i < PRIORITY_TIERS.length; i++) {
    if (PRIORITY_TIERS[i].some((kw) => lower.includes(kw))) return i;
  }
  return PRIORITY_TIERS.length;
}
const META_PATH = resolve(DATA_DIR, "metacognition.json");
const MAX_CONFLICT_PAIRS = 50;
const MAX_INTERACTIONS = 100;
const LEARNED_CONFLICT_THRESHOLD = 0.3;
const LEARNED_CONFLICT_MIN_SAMPLES = 5;
const SEED_PAIRS = [
  ["\u7B80\u6D01", "\u8BE6\u7EC6"],
  ["\u7B80\u77ED", "\u5C55\u5F00"],
  ["\u4E0D\u64C5\u957F", "\u64C5\u957F"],
  ["\u4E0D\u786E\u5B9A", "\u786E\u5B9A"],
  ["\u8C28\u614E", "\u679C\u65AD"],
  ["\u5148\u5171\u60C5", "\u76F4\u63A5\u7ED9\u65B9\u6848"]
];
let data = { conflictPairs: [], interactions: [] };
let lastAugmentSnapshot = [];
let initialized = false;
function loadMetacognition() {
  const saved = loadJson(META_PATH, { conflictPairs: [], interactions: [] });
  data = saved;
  for (const [a, b] of SEED_PAIRS) {
    const key = pairKey(a, b);
    const exists = data.conflictPairs.some((p) => pairKey(p.a, p.b) === key);
    if (!exists) {
      data.conflictPairs.push({
        a,
        b,
        source: "seed",
        coOccurrences: 0,
        correctionCount: 0,
        correctionRate: 0
      });
    }
  }
  initialized = true;
  console.log(`[cc-soul][metacognition] loaded: ${data.conflictPairs.length} conflict pairs, ${data.interactions.length} interactions`);
}
function ensureInit() {
  if (!initialized) loadMetacognition();
}
function persist() {
  debouncedSave(META_PATH, data);
}
function pairKey(a, b) {
  return [a, b].sort().join("::");
}
function ewmaCorrectionRate(pair) {
  if (!pair.recentCorrections || pair.recentCorrections.length === 0) {
    return pair.coOccurrences > 0 ? pair.correctionCount / pair.coOccurrences : 0;
  }
  const alpha = 0.15;
  let ewma = 0.5;
  for (const wasCorrection of pair.recentCorrections) {
    ewma = alpha * (wasCorrection ? 1 : 0) + (1 - alpha) * ewma;
  }
  return ewma;
}
function extractType(content) {
  const match = content.match(/\[([^\]]{2,12})\]/);
  if (match) return match[1];
  return content.slice(0, 6).replace(/\s+/g, "");
}
function allPairs(items) {
  const result = [];
  for (let i = 0; i < items.length; i++) {
    for (let j = i + 1; j < items.length; j++) {
      result.push([items[i], items[j]]);
    }
  }
  return result;
}
function learnConflict(augmentsUsed, wasCorrected) {
  ensureInit();
  if (augmentsUsed.length < 2) return;
  const types = augmentsUsed.map(extractType);
  const pairs = allPairs(types);
  for (const [a, b] of pairs) {
    const key = pairKey(a, b);
    let existing = data.conflictPairs.find((p) => pairKey(p.a, p.b) === key);
    if (!existing) {
      existing = {
        a,
        b,
        source: "learned",
        coOccurrences: 0,
        correctionCount: 0,
        correctionRate: 0
      };
      data.conflictPairs.push(existing);
    }
    existing.coOccurrences++;
    if (wasCorrected) existing.correctionCount++;
    if (!existing.recentCorrections) existing.recentCorrections = [];
    existing.recentCorrections.push(wasCorrected ? 1 : 0);
    if (existing.recentCorrections.length > 20) existing.recentCorrections.shift();
    existing.correctionRate = ewmaCorrectionRate(existing);
  }
  trimConflictPairs();
  persist();
}
function trimConflictPairs() {
  if (data.conflictPairs.length <= MAX_CONFLICT_PAIRS) return;
  const seeds = data.conflictPairs.filter((p) => p.source === "seed");
  const learned = data.conflictPairs.filter((p) => p.source === "learned").sort((a, b) => b.correctionCount - a.correctionCount);
  data.conflictPairs = [...seeds, ...learned].slice(0, MAX_CONFLICT_PAIRS);
}
function getActiveConflicts() {
  ensureInit();
  return data.conflictPairs.filter(
    (p) => p.source === "seed" || ewmaCorrectionRate(p) >= LEARNED_CONFLICT_THRESHOLD && p.coOccurrences >= LEARNED_CONFLICT_MIN_SAMPLES
  );
}
function recordInteraction(augmentTypes, quality, wasCorrected) {
  ensureInit();
  if (augmentTypes.length < 2) return;
  const types = augmentTypes.map(extractType);
  const pairs = allPairs(types);
  for (const [a, b] of pairs) {
    const key = pairKey(a, b);
    let entry = data.interactions.find((i) => i.pairKey === key);
    if (!entry) {
      entry = { pairKey: key, coOccurrences: 0, qualitySum: 0, avgQuality: 0, correctionCount: 0 };
      data.interactions.push(entry);
    }
    entry.coOccurrences++;
    entry.qualitySum += quality;
    entry.avgQuality = entry.qualitySum / entry.coOccurrences;
    if (wasCorrected) entry.correctionCount++;
  }
  if (data.interactions.length > MAX_INTERACTIONS) {
    data.interactions.sort((a, b) => b.coOccurrences - a.coOccurrences);
    data.interactions = data.interactions.slice(0, MAX_INTERACTIONS);
  }
  persist();
}
function getInteractionInsight() {
  ensureInit();
  if (data.interactions.length === 0) return "";
  const MIN_SAMPLES = 3;
  const qualified = data.interactions.filter((i) => i.coOccurrences >= MIN_SAMPLES);
  if (qualified.length === 0) return "";
  const sorted = [...qualified].sort((a, b) => a.avgQuality - b.avgQuality);
  const lines = [];
  const worst = sorted.filter((i) => i.avgQuality < 0.5).slice(0, 3);
  if (worst.length > 0) {
    lines.push("\u51CF\u6548\u7EC4\u5408: " + worst.map(
      (i) => `${i.pairKey.replace("::", "+")}(\u8D28\u91CF${(i.avgQuality * 100).toFixed(0)}%, n=${i.coOccurrences})`
    ).join("\uFF0C"));
  }
  const best = sorted.filter((i) => i.avgQuality >= 0.7).slice(-3).reverse();
  if (best.length > 0) {
    lines.push("\u589E\u6548\u7EC4\u5408: " + best.map(
      (i) => `${i.pairKey.replace("::", "+")}(\u8D28\u91CF${(i.avgQuality * 100).toFixed(0)}%, n=${i.coOccurrences})`
    ).join("\uFF0C"));
  }
  return lines.length > 0 ? `[\u4EA4\u4E92\u77E9\u9635] ${lines.join("\uFF1B")}` : "";
}
function checkAugmentConsistency(augments) {
  ensureInit();
  if (augments.length < 2) return "";
  const issues = [];
  const texts = augments.map((a) => a.content.toLowerCase());
  const activeConflicts = getActiveConflicts();
  for (const pair of activeConflicts) {
    const hasA = texts.some((t) => t.includes(pair.a));
    const hasB = texts.some((t) => t.includes(pair.b));
    if (hasA && hasB) {
      const suffix = pair.source === "learned" ? `(\u5B66\u4E60\u53D1\u73B0, \u7EA0\u6B63\u7387${(pair.correctionRate * 100).toFixed(0)}%)` : "";
      issues.push(`"${pair.a}" vs "${pair.b}"${suffix}`);
    }
  }
  const hasPlanSayDontKnow = texts.some((t) => t.includes("\u4E0D\u64C5\u957F") || t.includes("\u8BF4\u4E0D\u786E\u5B9A"));
  const hasHighConfidence = texts.some((t) => t.includes("\u64C5\u957F\u9886\u57DF") || t.includes("\u9AD8\u4FE1\u5FC3"));
  if (hasPlanSayDontKnow && hasHighConfidence) {
    issues.push('\u8BA1\u5212\u8BF4"\u4E0D\u64C5\u957F"\u4F46\u77E5\u8BC6\u8FB9\u754C\u8BF4"\u9AD8\u4FE1\u5FC3"\u2014\u2014\u4EE5\u6700\u65B0\u8BA1\u5212\u4E3A\u51C6');
  }
  const memoryTexts = texts.filter((t) => t.includes("[\u76F8\u5173\u8BB0\u5FC6]") || t.includes("[\u786E\u5B9A\u6027\u77E5\u8BC6]"));
  const correctionTexts = texts.filter((t) => t.includes("[\u6CE8\u610F\u89C4\u5219]") || t.includes("[\u884C\u52A8\u8BA1\u5212"));
  if (memoryTexts.length > 0 && correctionTexts.length > 0) {
    for (const mem of memoryTexts) {
      for (const corr of correctionTexts) {
        const memWords = new Set(mem.match(/[\u4e00-\u9fff]{2,}/g) || []);
        const corrWords = new Set(corr.match(/[\u4e00-\u9fff]{2,}/g) || []);
        const overlap = [...memWords].filter((w) => corrWords.has(w)).length;
        if (overlap >= 3) {
          issues.push("\u8BB0\u5FC6\u548C\u89C4\u5219\u53EF\u80FD\u6D89\u53CA\u540C\u4E00\u8BDD\u9898\u2014\u2014\u4EE5\u89C4\u5219/\u8BA1\u5212\u4E3A\u51C6");
          break;
        }
      }
    }
  }
  if (issues.length === 0) return "";
  const resolutions = getConflictResolutions(augments);
  const resText = resolutions.length > 0 ? ` \u4EF2\u88C1\u5EFA\u8BAE: ${resolutions.map((r) => `\u964D\u6743"${r.demote}"(${r.reason})`).join("\uFF1B")}` : "";
  return `[\u5143\u8BA4\u77E5\u8B66\u544A] \u6CE8\u5165\u4E0A\u4E0B\u6587\u6709\u6F5C\u5728\u51B2\u7A81: ${issues.join("\uFF1B")}\u3002\u8BF7\u4EE5\u6700\u65B0\u4FE1\u606F\u548C\u89C4\u5219\u4E3A\u51C6\u3002${resText}`;
}
function getConflictResolutions(augments) {
  ensureInit();
  if (augments.length < 2) return [];
  const resolutions = [];
  const activeConflicts = getActiveConflicts();
  for (const pair of activeConflicts) {
    const matchA = augments.filter((a) => a.content.toLowerCase().includes(pair.a));
    const matchB = augments.filter((a) => a.content.toLowerCase().includes(pair.b));
    if (matchA.length === 0 || matchB.length === 0) continue;
    for (const augA of matchA) {
      for (const augB of matchB) {
        const tierA = getTier(augA.content);
        const tierB = getTier(augB.content);
        if (tierA === tierB) {
          const loser = augA.priority >= augB.priority ? augB : augA;
          const loserKeyword = loser === augA ? pair.a : pair.b;
          resolutions.push({
            demote: loserKeyword,
            reason: `\u540C\u5C42\u51B2\u7A81\uFF0C\u4F18\u5148\u7EA7\u8F83\u4F4E(${loser.priority})`
          });
        } else if (tierA < tierB) {
          resolutions.push({
            demote: pair.b,
            reason: `${PRIORITY_TIERS[tierA]?.[0] || "\u9AD8\u5C42"}\u4F18\u5148\u4E8E${PRIORITY_TIERS[tierB]?.[0] || "\u4F4E\u5C42"}`
          });
        } else {
          resolutions.push({
            demote: pair.a,
            reason: `${PRIORITY_TIERS[tierB]?.[0] || "\u9AD8\u5C42"}\u4F18\u5148\u4E8E${PRIORITY_TIERS[tierA]?.[0] || "\u4F4E\u5C42"}`
          });
        }
      }
    }
  }
  const seen = /* @__PURE__ */ new Set();
  return resolutions.filter((r) => {
    if (seen.has(r.demote)) return false;
    seen.add(r.demote);
    return true;
  });
}
function snapshotAugments(augmentContents) {
  lastAugmentSnapshot = [...augmentContents];
}
function getLastAugmentSnapshot() {
  return lastAugmentSnapshot;
}
const metacognitionModule = {
  id: "metacognition",
  name: "\u8BA4\u77E5\u4EF2\u88C1\u5F15\u64CE",
  priority: 50,
  features: ["metacognition"],
  init() {
    loadMetacognition();
  }
};
export {
  checkAugmentConsistency,
  getConflictResolutions,
  getInteractionInsight,
  getLastAugmentSnapshot,
  learnConflict,
  loadMetacognition,
  metacognitionModule,
  recordInteraction,
  snapshotAugments
};
