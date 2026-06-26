import { resolve } from "path";
import { DATA_DIR, loadJson, debouncedSave, adaptiveCooldown } from "./persistence.ts";
import { getParam } from "./auto-tune.ts";
import { spawnCLI } from "./cli.ts";
import {
  sqliteCleanupExpired,
  sqliteFindByContent,
  sqliteUpdateMemory,
  sqliteUpdateRawLine,
  getDb,
  sqliteCount
} from "./sqlite-store.ts";
import { findMentionedEntities, getRelatedEntities } from "./graph.ts";
import {
  memoryState,
  useSQLite,
  addMemory,
  saveMemories,
  rebuildScopeIndex,
  getLazyModule,
  compressMemory
} from "./memory.ts";
import { trigrams, trigramSimilarity, shuffleArray } from "./memory-utils.ts";
import { recall, invalidateIDF, rebuildRecallIndex, _memLookup } from "./memory-recall.ts";
import { invalidateFieldIDF } from "./activation-field.ts";
let lastConsolidationTs = 0;
const CONSOLIDATION_COOLDOWN_MS = (userId) => adaptiveCooldown(getParam("lifecycle.consolidation_cooldown_hours") * 3600 * 1e3, userId);
let consolidating = false;
function tfidfVector(doc, idfMap) {
  const words = (doc.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map((w) => w.toLowerCase());
  const tf = /* @__PURE__ */ new Map();
  for (const w of words) tf.set(w, (tf.get(w) || 0) + 1);
  const vec = /* @__PURE__ */ new Map();
  for (const [term, count] of tf) {
    vec.set(term, count * (idfMap.get(term) ?? 1));
  }
  return vec;
}
function cosineSim(a, b) {
  let dot = 0, normA = 0, normB = 0;
  for (const [k, v] of a) {
    normA += v * v;
    if (b.has(k)) dot += v * b.get(k);
  }
  for (const [, v] of b) normB += v * v;
  if (normA === 0 || normB === 0) return 0;
  return dot / (Math.sqrt(normA) * Math.sqrt(normB));
}
const SIMHASH_BITS = 64;
function fnv1a64(token) {
  let h = 14695981039346656037n;
  for (let i = 0; i < token.length; i++) {
    h ^= BigInt(token.charCodeAt(i));
    h = h * 1099511628211n & 0xFFFFFFFFFFFFFFFFn;
  }
  return h;
}
function simHash(tokens, idf, bits = SIMHASH_BITS) {
  const v = new Float64Array(bits);
  for (const token of tokens) {
    const weight = idf.get(token) ?? 0.01;
    const hash = fnv1a64(token);
    for (let i = 0; i < bits; i++) {
      if (hash >> BigInt(i) & 1n) v[i] += weight;
      else v[i] -= weight;
    }
  }
  let sig = 0n;
  const sorted = [...v].sort((a, b) => a - b);
  const median = sorted[Math.floor(sorted.length / 2)];
  for (let i = 0; i < bits; i++) {
    if (v[i] > median) sig |= 1n << BigInt(i);
  }
  return sig;
}
function simHashDistance(a, b, bits = SIMHASH_BITS) {
  let xor = a ^ b;
  let count = 0;
  while (xor > 0n) {
    count += Number(xor & 1n);
    xor >>= 1n;
  }
  if (bits === 0) return 0;
  return count / bits;
}
import { tokenize as _tokenize } from "./memory-utils.ts";
function tokenize(text) {
  return _tokenize(text, "bigram");
}
function clusterByTopic(mems) {
  const capped = mems.length > 200 ? mems.slice(-200) : mems;
  if (capped.length < 3) return [];
  const df = /* @__PURE__ */ new Map();
  const N = capped.length;
  for (const m of capped) {
    const words = new Set((m.content.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map((w) => w.toLowerCase()));
    for (const w of words) df.set(w, (df.get(w) || 0) + 1);
  }
  const idfMap = /* @__PURE__ */ new Map();
  for (const [word, count] of df) idfMap.set(word, Math.log(N / (1 + count)));
  const tokenLists = capped.map((m) => tokenize(m.content));
  const sigs = tokenLists.map((ts) => ts.length > 0 ? simHash(ts, idfMap) : 0n);
  const BUCKET_BITS = 8;
  const buckets = /* @__PURE__ */ new Map();
  for (let i = 0; i < sigs.length; i++) {
    const bucketKey = Number(sigs[i] >> BigInt(SIMHASH_BITS - BUCKET_BITS) & BigInt((1 << BUCKET_BITS) - 1));
    if (!buckets.has(bucketKey)) buckets.set(bucketKey, []);
    buckets.get(bucketKey).push(i);
  }
  const candidatePairs = /* @__PURE__ */ new Set();
  for (const [, indices] of buckets) {
    if (indices.length < 2 || indices.length > 50) continue;
    for (let a = 0; a < indices.length; a++) {
      for (let b = a + 1; b < indices.length; b++) {
        const key = indices[a] < indices[b] ? `${indices[a]}:${indices[b]}` : `${indices[b]}:${indices[a]}`;
        candidatePairs.add(key);
      }
    }
  }
  for (const [bk, indices] of buckets) {
    for (let bit = 0; bit < BUCKET_BITS; bit++) {
      const neighbor = bk ^ 1 << bit;
      const nIndices = buckets.get(neighbor);
      if (!nIndices) continue;
      for (const a of indices) {
        for (const b of nIndices) {
          if (a === b) continue;
          const key = a < b ? `${a}:${b}` : `${b}:${a}`;
          candidatePairs.add(key);
        }
      }
    }
  }
  const vecs = capped.map((m) => tfidfVector(m.content, idfMap));
  const parent = Array.from({ length: capped.length }, (_, i) => i);
  function find(x) {
    return parent[x] === x ? x : parent[x] = find(parent[x]);
  }
  function unite(a, b) {
    parent[find(a)] = find(b);
  }
  for (const pair of candidatePairs) {
    const [ai, bi] = pair.split(":").map(Number);
    if (find(ai) === find(bi)) continue;
    const dist = simHashDistance(sigs[ai], sigs[bi]);
    if (dist > 0.4) continue;
    if (cosineSim(vecs[ai], vecs[bi]) >= 0.25) unite(ai, bi);
  }
  const clusterMap = /* @__PURE__ */ new Map();
  for (let i = 0; i < capped.length; i++) {
    const root = find(i);
    if (!clusterMap.has(root)) clusterMap.set(root, []);
    clusterMap.get(root).push(capped[i]);
  }
  return [...clusterMap.values()].filter((c) => c.length >= 3);
}
function consolidateMemories() {
  if (consolidating && Date.now() - lastConsolidationTs > 5 * 60 * 1e3) {
    console.error("[cc-soul][consolidation] force-releasing stuck lock (>5min)");
    consolidating = false;
  }
  if (consolidating) return;
  const totalCount = useSQLite ? sqliteCount() : memoryState.memories.length;
  if (totalCount < 500) return;
  if (Date.now() - lastConsolidationTs < CONSOLIDATION_COOLDOWN_MS()) return;
  consolidating = true;
  lastConsolidationTs = Date.now();
  const groups = /* @__PURE__ */ new Map();
  for (const mem of memoryState.memories) {
    const key = mem.scope || "unknown";
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(mem);
  }
  let pendingCLICalls = 0;
  const allContentToRemove = /* @__PURE__ */ new Set();
  const allSummariesToAdd = [];
  for (const [scope, mems] of groups) {
    if (mems.length < 50) continue;
    if (scope === "consolidated") continue;
    const oldest = mems.sort((a, b) => a.ts - b.ts).slice(0, 20);
    const segmentGroups = /* @__PURE__ */ new Map();
    const noSegment = [];
    for (const m of oldest) {
      if (m._segmentId != null) {
        const g = segmentGroups.get(m._segmentId) || [];
        g.push(m);
        segmentGroups.set(m._segmentId, g);
      } else {
        noSegment.push(m);
      }
    }
    const segmentClusters = [...segmentGroups.values()].filter((g) => g.length >= 3);
    const remaining = noSegment.concat([...segmentGroups.values()].filter((g) => g.length < 3).flat());
    const simhashClusters = remaining.length >= 3 ? clusterByTopic(remaining) : [];
    const clusters = [...segmentClusters, ...simhashClusters];
    if (clusters.length === 0) continue;
    for (const cluster of clusters) {
      const contents = cluster.map((m) => compressMemory(m)).join("\n");
      pendingCLICalls++;
      try {
        const { zeroLLMDistill } = require("./distill.ts");
        const zeroResult = zeroLLMDistill(cluster.map((m) => m.content));
        if (zeroResult && zeroResult.length > 10) {
          pendingCLICalls--;
          const summaries = [zeroResult.slice(0, 200)];
          for (const o of cluster) allContentToRemove.add(`${o.content}\0${o.ts}`);
          for (const summary of summaries) {
            allSummariesToAdd.push({ content: compressMemory({ content: summary }), visibility: cluster[0]?.visibility || "global" });
          }
          console.log(`[cc-soul][memory] consolidated ${cluster.length} ${scope} memories (zero-LLM)`);
          if (pendingCLICalls <= 0) {
            let maxEngagement = 0, maxRecallCount = 0;
            for (const mem of memoryState.memories) {
              if (allContentToRemove.has(`${mem.content}\0${mem.ts}`)) {
                maxEngagement = Math.max(maxEngagement, mem.injectionEngagement ?? 0);
                maxRecallCount = Math.max(maxRecallCount, mem.recallCount ?? 0);
              }
            }
            memoryState.memories = memoryState.memories.filter((m) => !allContentToRemove.has(`${m.content}\0${m.ts}`));
            for (const s of allSummariesToAdd) {
              addMemory(s.content, "consolidated", void 0, s.visibility);
            }
            consolidating = false;
          }
          continue;
        }
      } catch {
      }
      spawnCLI(
        `\u4EE5\u4E0B\u662F${scope}\u7C7B\u578B\u7684${cluster.length}\u6761\u540C\u4E3B\u9898\u8BB0\u5FC6\uFF0C\u8BF7\u5408\u5E76\u4E3A1-2\u6761\u6458\u8981\uFF08\u4FDD\u7559\u5173\u952E\u4FE1\u606F\uFF09\uFF1A

${contents.slice(0, 1500)}

\u683C\u5F0F\uFF1A\u6BCF\u6761\u6458\u8981\u4E00\u884C`,
        (output) => {
          try {
            pendingCLICalls--;
            if (memoryState.memories.length === 0) {
              if (pendingCLICalls <= 0) consolidating = false;
              return;
            }
            if (!output || output.length < 10) {
              if (pendingCLICalls <= 0) consolidating = false;
              return;
            }
            const summaries = output.split("\n").filter((l) => l.trim().length > 5).slice(0, 3);
            for (const o of cluster) allContentToRemove.add(`${o.content}\0${o.ts}`);
            for (const summary of summaries) {
              allSummariesToAdd.push({
                content: compressMemory({ content: summary.trim() }),
                visibility: cluster[0]?.visibility || "global"
              });
            }
            console.log(`[cc-soul][memory] consolidated ${cluster.length} ${scope} memories -> ${summaries.length} summaries`);
            if (pendingCLICalls <= 0) {
              let maxEngagement = 0, maxRecallCount = 0;
              for (const mem of memoryState.memories) {
                if (allContentToRemove.has(`${mem.content}\0${mem.ts}`)) {
                  maxEngagement = Math.max(maxEngagement, mem.injectionEngagement ?? 0);
                  maxRecallCount = Math.max(maxRecallCount, mem.recallCount ?? 0);
                }
              }
              for (let i = memoryState.memories.length - 1; i >= 0; i--) {
                if (allContentToRemove.has(`${memoryState.memories[i].content}\0${memoryState.memories[i].ts}`)) {
                  memoryState.memories.splice(i, 1);
                }
              }
              for (const entry of allSummariesToAdd) {
                memoryState.memories.push({
                  content: entry.content,
                  scope: "consolidated",
                  ts: Date.now(),
                  visibility: entry.visibility,
                  confidence: 0.8,
                  recallCount: maxRecallCount,
                  injectionEngagement: maxEngagement,
                  lastAccessed: Date.now(),
                  tier: "long_term"
                });
              }
              rebuildScopeIndex();
              rebuildRecallIndex(memoryState.memories);
              saveMemories();
              invalidateIDF();
              invalidateFieldIDF();
              try {
                const { emitCacheEvent } = require("./memory-utils.ts");
                emitCacheEvent("consolidation");
              } catch {
              }
              consolidating = false;
            }
          } catch (e) {
            console.error(`[cc-soul][consolidation] callback error: ${e.message}`);
            pendingCLICalls = Math.max(0, pendingCLICalls);
            if (pendingCLICalls <= 0) consolidating = false;
          }
        }
      );
    }
  }
  if (pendingCLICalls === 0) consolidating = false;
  generateInsights();
}
const MAX_INSIGHTS = 20;
function generateInsights() {
  const sevenDaysAgo = Date.now() - 7 * 864e5;
  const recentMemories = memoryState.memories.filter(
    (m) => m.ts >= sevenDaysAgo && m.scope !== "expired" && m.scope !== "insight"
  );
  if (recentMemories.length < 5) return;
  const ruleInsights = [];
  const scopeCounts = /* @__PURE__ */ new Map();
  for (const m of recentMemories) scopeCounts.set(m.scope, (scopeCounts.get(m.scope) || 0) + 1);
  const topScope = [...scopeCounts.entries()].sort((a, b) => b[1] - a[1])[0];
  if (topScope && topScope[1] >= 5) ruleInsights.push(`\u6700\u8FD1${topScope[1]}\u6761\u8BB0\u5FC6\u90FD\u662F${topScope[0]}\u7C7B\u578B`);
  const negCount = recentMemories.filter((m) => m.emotion === "painful" || (m.situationCtx?.mood ?? 0) < -0.3).length;
  if (negCount >= 3) ruleInsights.push("\u6700\u8FD1\u60C5\u7EEA\u504F\u4F4E\u7684\u8BB0\u5FC6\u589E\u591A");
  const corrCount = recentMemories.filter((m) => m.scope === "correction").length;
  if (corrCount >= 3) ruleInsights.push(`\u67D0\u9886\u57DF\u88AB\u7EA0\u6B63${corrCount}\u6B21\uFF0C\u9700\u8981\u52A0\u5F3A`);
  if (ruleInsights.length > 0) {
    for (const insight of ruleInsights) addMemory(insight, "insight", void 0, "private");
    console.log(`[cc-soul][insights] rule-based: ${ruleInsights.length} insights generated (zero-LLM)`);
    return;
  }
  const digest = recentMemories.sort((a, b) => b.ts - a.ts).slice(0, 60).map((m) => `[${m.scope}] ${m.content.slice(0, 120)}`).join("\n");
  spawnCLI(
    `\u5206\u6790\u4EE5\u4E0B\u7528\u6237\u8FD1\u671F\u8BB0\u5FC6\uFF0C\u603B\u7ED31-3\u6761\u884C\u4E3A\u6A21\u5F0F\u6216\u504F\u597D\u6D1E\u5BDF\u3002\u6BCF\u6761\u4E00\u884C\uFF0C\u683C\u5F0F\uFF1A[\u6D1E\u5BDF] \u5185\u5BB9

${digest.slice(0, 2e3)}`,
    (output) => {
      if (!output || output.length < 10) return;
      const insights = output.split("\n").map((l) => l.trim()).filter((l) => l.startsWith("[\u6D1E\u5BDF]")).map((l) => l.replace(/^\[洞察\]\s*/, "").trim()).filter((l) => l.length >= 5).slice(0, 3);
      if (insights.length === 0) return;
      for (const insight of insights) {
        addMemory(insight, "insight", void 0, "private");
      }
      const allInsights = memoryState.memories.filter((m) => m.scope === "insight").sort((a, b) => a.ts - b.ts);
      if (allInsights.length > MAX_INSIGHTS) {
        const toRemoveKeys = new Set(
          allInsights.slice(0, allInsights.length - MAX_INSIGHTS).map((m) => `${m.content}\0${m.ts}`)
        );
        for (let i = memoryState.memories.length - 1; i >= 0; i--) {
          const m = memoryState.memories[i];
          if (toRemoveKeys.has(`${m.content}\0${m.ts}`)) {
            memoryState.memories.splice(i, 1);
          }
        }
        rebuildScopeIndex();
        rebuildRecallIndex(memoryState.memories);
        saveMemories();
      }
      console.log(`[cc-soul][insight] generated ${insights.length} insights from ${recentMemories.length} recent memories`);
    }
  );
}
let lastRecallFeedbackTs = 0;
const RECALL_FEEDBACK_COOLDOWN = 6e4;
function recallFeedbackLoop(userMsg, recalledContents) {
  const now = Date.now();
  if (now - lastRecallFeedbackTs < RECALL_FEEDBACK_COOLDOWN) return;
  if (memoryState.memories.length < 20) return;
  if (userMsg.length < 10) return;
  lastRecallFeedbackTs = now;
  const recalledSet = new Set(recalledContents);
  const candidates = shuffleArray(memoryState.memories.filter((m) => !recalledSet.has(m.content) && m.content.length > 15)).slice(0, 30);
  if (candidates.length === 0) return;
  const queryTri = trigrams(userMsg);
  const RELEVANCE_THRESHOLD = 0.08;
  const queryWords = (userMsg.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map((w) => w.toLowerCase()).slice(0, 8);
  if (queryWords.length === 0) return;
  let patched = 0;
  for (const mem of candidates) {
    const memTri = trigrams(mem.content);
    const sim = trigramSimilarity(queryTri, memTri);
    if (sim < RELEVANCE_THRESHOLD) continue;
    const memLower = mem.content.toLowerCase();
    const keywordHits = queryWords.filter((w) => memLower.includes(w)).length;
    if (sim < 0.12 && keywordHits === 0) continue;
    const real = _memLookup.get(`${mem.content}\0${mem.ts}`);
    if (!real) continue;
    if (!real.tags) real.tags = [];
    for (const w of queryWords) {
      if (!real.tags.includes(w)) {
        real.tags.push(w);
      }
    }
    if (real.tags.length > 25) real.tags = real.tags.slice(-25);
    patched++;
  }
  if (patched > 0) {
    saveMemories();
    console.log(`[cc-soul][recall-feedback] patched ${patched} memories with cross-tags (local trigram)`);
  }
}
function assessResponseQuality(userReply, replyDelayMs, prevTopic, currentTopic) {
  let score = 0.5;
  const reasons = [];
  const len = userReply.length;
  if (len > 50) {
    score += 0.12;
    reasons.push("\u957F\u56DE\u590D");
  } else if (len > 15) {
    score += 0.05;
  } else if (len < 5) {
    score -= 0.1;
    reasons.push("\u6781\u77ED\u56DE\u590D");
  }
  const delaySec = replyDelayMs / 1e3;
  if (delaySec < 5) {
    score += 0.1;
    reasons.push("\u5FEB\u901F\u56DE\u590D");
  } else if (delaySec > 120) {
    score -= 0.15;
    reasons.push("\u957F\u65F6\u95F4\u6C89\u9ED8");
  }
  if (/[？?]/.test(userReply) || /怎么|为什么|能不能|具体|详细/.test(userReply)) {
    score += 0.12;
    reasons.push("\u8FFD\u95EE");
  }
  if (/^(嗯|好的?|ok|谢谢|收到|明白|了解)\s*[。.!！]?\s*$/i.test(userReply.trim())) {
    score -= 0.05;
    reasons.push("\u7ED3\u675F\u8BED");
  }
  if (prevTopic && currentTopic && prevTopic !== currentTopic) {
    score -= 0.08;
    reasons.push("\u8BDD\u9898\u5207\u6362");
  }
  score = Math.max(0, Math.min(1, score));
  const signal = score > 0.6 ? "positive" : score < 0.35 ? "negative" : "neutral";
  return { quality: score, signal, reason: reasons.join("+") || "\u6B63\u5E38" };
}
let cachedAssociation = null;
const ASSOCIATION_COOLDOWN = 3e4;
function associateSync(userMsg, recalled, userId, channelId) {
  if (userMsg.length < 5 || recalled.length < 2) return [];
  const CJK_RE = /[\u4e00-\u9fff]{2,}|[a-z]{4,}/gi;
  const seenContents = new Set(recalled.map((m) => m.content.slice(0, 60)));
  const associationKeywords = /* @__PURE__ */ new Set();
  const mentioned = findMentionedEntities(userMsg);
  if (mentioned.length > 0) {
    const related = getRelatedEntities(mentioned, 2, 6);
    for (const entity of related) {
      const words = (entity.match(CJK_RE) || []).map((w) => w.toLowerCase());
      for (const w of words) associationKeywords.add(w);
    }
  }
  try {
    const distMod = getLazyModule("distill");
    const getRelevantTopics = distMod?.getRelevantTopics;
    const topics = getRelevantTopics(userMsg, userId, 3);
    for (const t of topics) {
      const words = ((t.topic + " " + t.summary).match(CJK_RE) || []).map((w) => w.toLowerCase());
      for (const w of words.slice(0, 3)) associationKeywords.add(w);
    }
  } catch {
  }
  for (const m of recalled.slice(0, 3)) {
    const words = (m.content.match(CJK_RE) || []).map((w) => w.toLowerCase());
    for (const w of words.slice(0, 2)) associationKeywords.add(w);
  }
  const userWords = new Set((userMsg.match(CJK_RE) || []).map((w) => w.toLowerCase()));
  for (const w of userWords) associationKeywords.delete(w);
  if (associationKeywords.size < 2) return [];
  const query = [...associationKeywords].slice(0, 8).join(" ");
  const associated = recall(query, 6, userId, channelId);
  const novel = associated.filter((m) => !seenContents.has(m.content.slice(0, 60)));
  if (novel.length > 0) {
    console.log(`[cc-soul][association] sync: "${query.slice(0, 30)}" \u2192 ${novel.length} associated memories`);
  }
  return novel.slice(0, 4);
}
function triggerAssociativeRecall(userMsg, topRecalled) {
  if (userMsg.length < 10) return;
  if (cachedAssociation && Date.now() - cachedAssociation.ts < ASSOCIATION_COOLDOWN) return;
  const recalledSet = new Set(topRecalled);
  const pool = shuffleArray(memoryState.memories.filter((m) => !recalledSet.has(m.content) && m.content.length > 15 && m.scope !== "proactive" && m.scope !== "expired" && m.scope !== "decayed")).slice(0, 20);
  if (pool.length < 3) return;
  const memList = pool.map((m, i) => `${i + 1}. ${m.content.slice(0, 80)}`).join("\n");
  spawnCLI(
    `\u7528\u6237\u8BF4: "${userMsg.slice(0, 200)}"

\u5DF2\u76F4\u63A5\u53EC\u56DE: ${topRecalled.slice(0, 3).map((r) => r.slice(0, 40)).join("; ")}

\u4EE5\u4E0B\u8BB0\u5FC6\u4E2D\uFF0C\u54EA\u4E9B\u548C\u7528\u6237\u8BDD\u9898\u6709\u9690\u542B\u5173\u8054\uFF1F\uFF08\u4E0D\u662F\u5B57\u9762\u5339\u914D\uFF0C\u662F\u6DF1\u5C42\u8054\u60F3\u2014\u2014\u6BD4\u5982\u8BDD\u9898\u76F8\u5173\u3001\u56E0\u679C\u94FE\u3001\u540C\u4E00\u65F6\u671F\u7684\u4E8B\uFF09
${memList}

\u90091-3\u6761\u6700\u76F8\u5173\u7684\uFF0C\u683C\u5F0F: "\u5E8F\u53F7. \u5185\u5BB9\u6458\u8981 \u2014 \u5173\u8054\u539F\u56E0"\u3002\u90FD\u4E0D\u76F8\u5173\u56DE\u7B54"\u65E0"`,
    (output) => {
      if (!output || output.includes("\u65E0") || output.length < 5) {
        cachedAssociation = null;
        return;
      }
      const nums = output.match(/(\d+)\./g)?.map((n) => parseInt(n)) || [];
      const referencedMems = nums.filter((n) => n >= 1 && n <= pool.length).map((n) => pool[n - 1].content.slice(0, 80));
      cachedAssociation = {
        query: userMsg.slice(0, 50),
        result: output.slice(0, 300),
        memories: referencedMems,
        ts: Date.now()
      };
      console.log(`[cc-soul][association] deep: ${referencedMems.length} hidden connections found`);
    }
  );
}
function getAssociativeRecall() {
  if (!cachedAssociation) return "";
  if (Date.now() - cachedAssociation.ts > 3e5) {
    cachedAssociation = null;
    return "";
  }
  return `[\u6DF1\u5C42\u8054\u60F3] ${cachedAssociation.result}`;
}
let lastSessionSummaryTs = 0;
const SESSION_SUMMARY_COOLDOWN = 18e5;
function parseMemoryCommands(responseText) {
  const commands = [];
  const rememberPattern = /[（(](?:记下了|记住|记下|save)[：:]\s*(.+?)[）)]/g;
  let match;
  while ((match = rememberPattern.exec(responseText)) !== null) {
    commands.push({ action: "remember", content: match[1].trim() });
  }
  const forgetPattern = /[（(](?:忘掉|忘记|forget|过时了)[：:]\s*(.+?)[）)]/g;
  while ((match = forgetPattern.exec(responseText)) !== null) {
    commands.push({ action: "forget", content: match[1].trim() });
  }
  const updatePattern = /[（(](?:更正记忆|更新记忆|update)[：:]\s*(.+?)\s*(?:→|->)+\s*(.+?)[）)]/g;
  while ((match = updatePattern.exec(responseText)) !== null) {
    commands.push({ action: "update", content: match[2].trim(), oldContent: match[1].trim() });
  }
  const searchPattern = /[（(](?:想查|查一下|search|回忆一下)[：:]\s*(.+?)[）)]/g;
  while ((match = searchPattern.exec(responseText)) !== null) {
    commands.push({ action: "search", content: match[1].trim() });
  }
  return commands;
}
let pendingSearchResults = [];
function getPendingSearchResults() {
  const results = [...pendingSearchResults];
  pendingSearchResults = [];
  return results;
}
function executeMemoryCommands(commands, userId, channelId) {
  for (const cmd of commands) {
    switch (cmd.action) {
      case "remember":
        addMemory(cmd.content, "fact", userId, "global", channelId);
        console.log(`[cc-soul][active-memory] REMEMBER: ${cmd.content.slice(0, 60)}`);
        break;
      case "forget": {
        const keyword = cmd.content.toLowerCase().trim();
        if (keyword.length < 4) {
          console.log(`[cc-soul][active-memory] FORGET blocked: keyword too short "${keyword}" (min 4 chars, anti-hallucination)`);
          break;
        }
        const MAX_FORGET_PER_CMD = 3;
        let forgotten = 0;
        for (const mem of memoryState.memories) {
          if (forgotten >= MAX_FORGET_PER_CMD) {
            console.log(`[cc-soul][active-memory] FORGET capped at ${MAX_FORGET_PER_CMD} (keyword: ${keyword.slice(0, 30)}), remaining untouched`);
            break;
          }
          if (mem.content.toLowerCase().includes(keyword) && mem.scope !== "consolidated" && mem.scope !== "expired") {
            mem.scope = "expired";
            forgotten++;
          }
        }
        if (forgotten > 0) {
          saveMemories();
          rebuildScopeIndex();
          console.log(`[cc-soul][active-memory] FORGET: marked ${forgotten} memories as expired (keyword: ${cmd.content.slice(0, 30)})`);
        }
        break;
      }
      case "update": {
        if (!cmd.oldContent) break;
        const oldKw = cmd.oldContent.toLowerCase();
        for (const mem of memoryState.memories) {
          if (mem.content.toLowerCase().includes(oldKw) && mem.scope !== "expired") {
            console.log(`[cc-soul][active-memory] UPDATE: "${mem.content.slice(0, 40)}" \u2192 "${cmd.content.slice(0, 40)}"`);
            mem.content = cmd.content;
            mem.ts = Date.now();
            mem.tags = void 0;
            break;
          }
        }
        saveMemories();
        rebuildScopeIndex();
        break;
      }
      case "search": {
        const results = recall(cmd.content, 5, userId, channelId);
        if (results.length > 0) {
          pendingSearchResults = results.map((m) => `- ${m.content}${m.emotion && m.emotion !== "neutral" ? ` (${m.emotion})` : ""}`);
          console.log(`[cc-soul][active-memory] SEARCH "${cmd.content.slice(0, 30)}": found ${results.length} results (cached for next turn)`);
        }
        break;
      }
    }
  }
}
let lastContradictionScan = 0;
const CONTRADICTION_SCAN_COOLDOWN = 24 * 36e5;
function scanForContradictions() {
  const now = Date.now();
  if (now - lastContradictionScan < CONTRADICTION_SCAN_COOLDOWN) return;
  if (memoryState.memories.length < 20) return;
  lastContradictionScan = now;
  const conflictScopes = ["fact", "preference", "correction"];
  const groups = /* @__PURE__ */ new Map();
  for (const mem of memoryState.memories) {
    if (!conflictScopes.includes(mem.scope)) continue;
    if (mem.scope === "expired") continue;
    if (!groups.has(mem.scope)) groups.set(mem.scope, []);
    groups.get(mem.scope).push(mem);
  }
  for (const [scope, mems] of groups) {
    if (mems.length < 5) continue;
    const sorted = [...mems].sort((a, b) => b.ts - a.ts);
    const recent = sorted.slice(0, 10);
    const older = sorted.slice(10, 20);
    if (older.length < 3) continue;
    let foundContradiction = false;
    try {
      const { extractFacts } = require("./fact-store.ts");
      const { classifyConflict } = require("./memory-utils.ts");
      for (const r of recent) {
        for (const o of older) {
          const rFacts = extractFacts(r.content);
          const oFacts = extractFacts(o.content);
          const conflict = classifyConflict(oFacts, rFacts);
          if (conflict === "supersede") {
            o.validUntil = o.validUntil || Date.now();
            foundContradiction = true;
            try {
              require("./decision-log.ts").logDecision("contradiction_zerollm", o.content.slice(0, 30), `superseded by ${r.content.slice(0, 30)}`);
            } catch {
            }
          }
        }
      }
    } catch {
    }
    if (foundContradiction) continue;
    const recentList = recent.map((m, i) => `\u65B0${i + 1}. ${m.content.slice(0, 80)}`).join("\n");
    const olderList = older.map((m, i) => `\u65E7${i + 1}. ${m.content.slice(0, 80)}`).join("\n");
    spawnCLI(
      `\u4EE5\u4E0B\u662F\u540C\u7C7B\u578B(${scope})\u7684\u65B0\u65E7\u8BB0\u5FC6\uFF0C\u68C0\u67E5\u662F\u5426\u6709\u77DB\u76FE\uFF08\u540C\u4E00\u4EF6\u4E8B\u8BF4\u6CD5\u4E0D\u540C\u3001\u524D\u540E\u4E0D\u4E00\u81F4\uFF09\u3002

\u6700\u8FD1\u7684\u8BB0\u5FC6:
${recentList}

\u8F83\u65E9\u7684\u8BB0\u5FC6:
${olderList}

\u5982\u679C\u6709\u77DB\u76FE\uFF0C\u8F93\u51FA\u683C\u5F0F: "\u65E7N \u4E0E \u65B0M \u77DB\u76FE: \u539F\u56E0"\uFF08\u53EF\u591A\u6761\uFF09
\u5982\u679C\u6CA1\u6709\u77DB\u76FE\uFF0C\u56DE\u7B54"\u65E0"`,
      (output) => {
        if (!output || output.includes("\u65E0")) return;
        const lines = output.split("\n").filter((l) => l.includes("\u77DB\u76FE"));
        let timeBounded = 0;
        for (const line of lines) {
          const oldMatch = line.match(/旧(\d+)/);
          if (oldMatch) {
            const idx = parseInt(oldMatch[1]) - 1;
            if (idx >= 0 && idx < older.length) {
              const memIdx = memoryState.memories.findIndex((m) => m.content === older[idx].content && m.ts === older[idx].ts);
              if (memIdx >= 0) {
                const mem = memoryState.memories[memIdx];
                mem.validUntil = Date.now();
                if (!mem.validFrom) mem.validFrom = mem.ts;
                timeBounded++;
              }
            }
          }
        }
        if (timeBounded > 0) {
          saveMemories();
          console.log(`[cc-soul][contradiction] time-bounded ${timeBounded} contradicted memories in scope "${scope}" (kept as historical)`);
        }
      }
    );
  }
}
let lastPredictionTs = 0;
let cachedPrediction = [];
function predictiveRecall(userId, channelId) {
  const now = Date.now();
  const results = [...cachedPrediction];
  cachedPrediction = [];
  return results;
}
function generatePrediction(recentTopics, userId) {
  if (recentTopics.length === 0) return;
  if (Date.now() - lastPredictionTs < 6e4) return;
  lastPredictionTs = Date.now();
  const topicStr = recentTopics.slice(-3).join("\u3001");
  const candidates = memoryState.memories.filter((m) => {
    if (m.scope === "expired" || m.scope === "proactive") return false;
    const content = m.content.toLowerCase();
    return recentTopics.some((t) => content.includes(t.toLowerCase()));
  }).sort((a, b) => b.ts - a.ts).slice(0, 5);
  if (candidates.length > 0) {
    cachedPrediction = candidates.map((m) => m.content);
    console.log(`[cc-soul][predictive] pre-loaded ${candidates.length} memories for topics: ${topicStr}`);
  }
}
function triggerSessionSummary(recentTurns) {
  const now = Date.now();
  if (now - lastSessionSummaryTs < SESSION_SUMMARY_COOLDOWN) return;
  if (memoryState.chatHistory.length < 3) return;
  lastSessionSummaryTs = now;
  const turns = memoryState.chatHistory.slice(-(recentTurns || 10));
  if (turns.length >= 2) {
    const firstTopic = turns[0].user.slice(0, 50);
    const lastPoint = turns[turns.length - 1].assistant.slice(0, 80);
    let entities = [];
    try {
      entities = require("./graph.ts").findMentionedEntities(turns.map((t) => t.user).join(" ")).slice(0, 3);
    } catch {
    }
    const extractive = `\u8BA8\u8BBA\u4E86${firstTopic}${entities.length > 0 ? "\uFF0C\u6D89\u53CA" + entities.join("/") : ""}\u3002${lastPoint}`;
    if (extractive.length > 30) {
      addMemory(`[\u4F1A\u8BDD\u6458\u8981] ${extractive.slice(0, 300)}`, "consolidated", void 0, "global");
      console.log(`[cc-soul][session-summary] extractive: ${extractive.slice(0, 80)}`);
      return;
    }
  }
  const conversation = turns.map((t) => `\u7528\u6237: ${t.user.slice(0, 200)}
\u52A9\u624B: ${t.assistant.slice(0, 200)}`).join("\n\n");
  spawnCLI(
    `\u4EE5\u4E0B\u662F\u4E00\u6BB5\u5B8C\u6574\u5BF9\u8BDD\uFF0C\u8BF7\u5199\u4E00\u6761\u9AD8\u8D28\u91CF\u7684\u4F1A\u8BDD\u6458\u8981\uFF082-3\u53E5\u8BDD\uFF09\uFF0C\u5305\u542B\uFF1A
1. \u8BA8\u8BBA\u4E86\u4EC0\u4E48\u4E3B\u9898
2. \u5173\u952E\u7ED3\u8BBA\u6216\u51B3\u5B9A
3. \u662F\u5426\u6709\u9057\u7559\u95EE\u9898
\u4E0D\u8981\u8BF4"\u7528\u6237\u548C\u52A9\u624B\u8BA8\u8BBA\u4E86..."\uFF0C\u76F4\u63A5\u5199\u5185\u5BB9\u3002

${conversation}`,
    (output) => {
      if (output && output.length > 20) {
        addMemory(`[\u4F1A\u8BDD\u6458\u8981] ${output.slice(0, 300)}`, "consolidated", void 0, "global");
        console.log(`[cc-soul][session-summary] ${output.slice(0, 80)}`);
      }
    }
  );
}
let lastNetworkCleanup = 0;
const NETWORK_CLEANUP_COOLDOWN = 24 * 36e5;
function cleanupNetworkKnowledge() {
  const now = Date.now();
  if (now - lastNetworkCleanup < NETWORK_CLEANUP_COOLDOWN) return;
  lastNetworkCleanup = now;
  let expired = 0;
  let downgraded = 0;
  for (const mem of memoryState.memories) {
    if (!mem.content.startsWith("[\u7F51\u7EDC\u77E5\u8BC6")) continue;
    if (mem.scope === "expired") continue;
    const ageDays = (now - mem.ts) / 864e5;
    if (ageDays > 90 && (!mem.tags || mem.tags.length === 0)) {
      mem.scope = "expired";
      expired++;
      continue;
    }
    if (mem.content.includes("\u4F4E\u53EF\u4FE1") && ageDays > 30) {
      mem.scope = "expired";
      expired++;
      continue;
    }
    if (mem.content.includes("\u5F85\u9A8C\u8BC1") && ageDays > 60) {
      mem.scope = "expired";
      downgraded++;
      continue;
    }
  }
  if (expired > 0 || downgraded > 0) {
    saveMemories();
    console.log(`[cc-soul][network-cleanup] expired ${expired}, downgraded ${downgraded} network memories`);
  }
}
const EPISODES_PATH = resolve(DATA_DIR, "episodes.json");
const MAX_EPISODES = 200;
let episodes = [];
function loadEpisodes() {
  episodes = loadJson(EPISODES_PATH, []);
  console.log(`[cc-soul][episodes] loaded ${episodes.length} episodes`);
}
function saveEpisodes() {
  debouncedSave(EPISODES_PATH, episodes);
}
function recordEpisode(topic, turns, correction, resolution = "resolved", frustrationPeak = 0, lesson) {
  const episode = {
    id: Date.now().toString(36) + Math.random().toString(36).slice(2, 4),
    timestamp: Date.now(),
    topic: topic.slice(0, 100),
    turns: turns.slice(-10).map((t) => ({ ...t, content: t.content.slice(0, 200) })),
    correction,
    resolution,
    lesson,
    frustrationPeak
  };
  episodes.push(episode);
  if (episodes.length > MAX_EPISODES) episodes = episodes.slice(-Math.floor(MAX_EPISODES * 0.8));
  saveEpisodes();
  console.log(`[cc-soul][episodes] recorded: ${topic.slice(0, 40)} [${resolution}]`);
}
function recallEpisodes(msg, topN = 2) {
  if (episodes.length === 0) return [];
  const words = new Set((msg.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map((w) => w.toLowerCase()));
  if (words.size === 0) return [];
  const scored = episodes.map((ep) => {
    const topicWords = (ep.topic.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map((w) => w.toLowerCase());
    const overlap = topicWords.filter((w) => words.has(w)).length;
    const correctionBoost = ep.correction ? 1.5 : 1;
    return { ep, score: overlap * correctionBoost };
  }).filter((s) => s.score > 0).sort((a, b) => b.score - a.score);
  return scored.slice(0, topN).map((s) => s.ep);
}
function buildEpisodeContext(msg) {
  const relevant = recallEpisodes(msg);
  if (relevant.length === 0) return "";
  const lines = relevant.map((ep) => {
    let desc = `[Episode] ${ep.topic}`;
    if (ep.correction) desc += ` \u2014 you made a mistake: ${ep.correction.what} (cause: ${ep.correction.cause})`;
    if (ep.lesson) desc += ` \u2014 lesson: ${ep.lesson}`;
    if (ep.frustrationPeak > 0.5) desc += ` \u2014 user was frustrated`;
    return desc;
  });
  return lines.join("\n");
}
const HOUR_MS = 36e5;
const DAY_MS = 864e5;
const SHORT_TERM_THRESHOLD = 24 * HOUR_MS;
const MID_TERM_THRESHOLD = 30 * DAY_MS;
const RECALL_UPGRADE_COUNT = 1;
let lastDecayTs = 0;
const DECAY_COOLDOWN = 6 * HOUR_MS;
function creativeForget(mem, ageDays) {
  if (mem.scope === "correction" || mem.scope === "pinned" || mem.scope === "consolidated") return { action: "keep" };
  if ((mem.importance ?? 5) >= 8) return { action: "keep" };
  if ((mem.recallCount ?? 0) >= 5) return { action: "keep" };
  if (ageDays < 30) return { action: "keep" };
  if (ageDays < 90) {
    let content = mem.content;
    content = content.replace(/\d{4}[年\-\/]\d{1,2}[月\-\/]\d{1,2}[日号]?/g, "");
    content = content.replace(/[上下]午\d{1,2}[点时:：]\d{0,2}分?/g, "");
    content = content.replace(/凌晨|早上|中午|傍晚|晚上\d{1,2}点/g, "");
    content = content.replace(/(\d{4,})(\s*元|块|万|千)/g, (_, n, unit) => {
      const num = parseInt(n);
      if (num >= 1e4) return `\u51E0${unit === "\u4E07" ? "\u4E07" : "\u4E07" + unit}`;
      if (num >= 1e3) return `\u51E0\u5343${unit}`;
      return `${n}${unit}`;
    });
    content = content.replace(/今天|昨天|前天|刚才|刚刚|方才/g, "\u4E4B\u524D");
    content = content.trim().replace(/\s{2,}/g, " ");
    if (content.length < 5) return { action: "keep" };
    return { action: "fade", content };
  }
  if (ageDays < 180) {
    const content = mem.content;
    const traits = [];
    if (/每天|经常|总是|习惯|一直/.test(content)) traits.push("\u6709\u89C4\u5F8B\u6027");
    if (/坚持|还是|虽然.*但|即使.*也/.test(content)) traits.push("\u610F\u5FD7\u529B\u5F3A");
    if (/喜欢|最爱|偏好|热爱/.test(content)) {
      const obj = content.match(/喜欢(.{2,8})/)?.[1] || "";
      if (obj) traits.push(`\u504F\u597D:${obj.replace(/[，。！？\s]+$/, "")}`);
    }
    if (/讨厌|不喜欢|受不了|反感/.test(content)) {
      const obj = content.match(/(?:讨厌|不喜欢)(.{2,8})/)?.[1] || "";
      if (obj) traits.push(`\u53CD\u611F:${obj.replace(/[，。！？\s]+$/, "")}`);
    }
    if (/焦虑|压力|紧张|担心/.test(content)) traits.push("\u6709\u538B\u529B");
    if (/学|研究|探索|尝试/.test(content)) traits.push("\u5B66\u4E60\u578B");
    if (/帮|支持|关心|照顾/.test(content)) traits.push("\u5173\u6000\u578B");
    if (/快|效率|优化|性能/.test(content)) traits.push("\u6548\u7387\u5BFC\u5411");
    if (/疼|不舒服|生病|失眠/.test(content)) traits.push("\u5065\u5EB7\u95EE\u9898");
    if (/开心|高兴|兴奋|满足/.test(content)) traits.push("\u6B63\u9762\u4F53\u9A8C");
    if (/难过|伤心|失望|沮丧/.test(content)) traits.push("\u8D1F\u9762\u4F53\u9A8C");
    if (traits.length === 0) {
      const keywords = (content.match(/[\u4e00-\u9fff]{2,4}|[a-zA-Z]{3,}/g) || []).slice(0, 5);
      if (keywords.length === 0) return { action: "keep" };
      return { action: "gist", content: `[\u6A21\u7CCA\u8BB0\u5FC6] ${keywords.join("\u3001")}` };
    }
    return { action: "gist", content: `[\u7279\u5F81\u7406\u89E3] ${traits.join("\u3001")}` };
  }
  return { action: "absorb" };
}
function processMemoryDecay() {
  const now = Date.now();
  if (now - lastDecayTs < DECAY_COOLDOWN) return;
  lastDecayTs = now;
  let tsRepaired = 0;
  for (const mem of memoryState.memories) {
    if (!mem.ts || mem.ts === 0) {
      mem.ts = mem.lastAccessed || now - Math.random() * 30 * DAY_MS;
      tsRepaired++;
    }
  }
  if (tsRepaired > 0) {
    console.log(`[cc-soul][memory-decay] repaired ${tsRepaired} memories with ts=0`);
  }
  let upgraded = 0;
  let decayed = 0;
  let compressed = 0;
  let faded = 0;
  let gisted = 0;
  let absorbed = 0;
  const useArchive = true;
  let archived = 0;
  const PROTECTED_SCOPES = /* @__PURE__ */ new Set([
    "fact",
    "wal",
    "preference",
    "event",
    "correction",
    "deep_feeling",
    "wisdom",
    "pinned"
  ]);
  for (const mem of memoryState.memories) {
    if (mem.scope === "expired" || mem.scope === "decayed" || mem.scope === "pinned" || mem.scope === "archived") continue;
    if (PROTECTED_SCOPES.has(mem.scope)) continue;
    if ((mem.utility ?? 0) > 0 && Math.random() < Math.min(0.7, (mem.utility ?? 0) * 0.15)) continue;
    if (mem.scope === "consolidated" && now - (mem.ts || 0) < 72 * 60 * 60 * 1e3) continue;
    const tier = mem.tier || "short_term";
    const age = now - (mem.ts || mem.lastAccessed || now);
    const recallCount = mem.recallCount ?? 0;
    const lastRecalled = mem.lastRecalled ?? 0;
    const ageDays = age / DAY_MS;
    const cf = creativeForget(mem, ageDays);
    if (cf.action === "fade" && cf.content && cf.content !== mem.content) {
      if (!mem.history) mem.history = [];
      if (mem.history.length < 5) mem.history.push({ content: mem.content, ts: now });
      mem.content = cf.content;
      mem.tier = "fading";
      faded++;
      continue;
    }
    if (cf.action === "gist" && cf.content) {
      if (!mem.history) mem.history = [];
      if (mem.history.length < 5) mem.history.push({ content: mem.content, ts: now });
      mem.content = cf.content;
      mem.tier = "gist";
      gisted++;
      continue;
    }
    if (cf.action === "absorb") {
      mem.scope = "expired";
      mem.tier = "absorbed";
      absorbed++;
      continue;
    }
    if (tier === "short_term" && age > SHORT_TERM_THRESHOLD) {
      const effectiveRecall = (mem.injectionEngagement ?? 0) >= 1 || recallCount >= RECALL_UPGRADE_COUNT;
      if (effectiveRecall) {
        mem.tier = "mid_term";
        upgraded++;
      } else if (useArchive) {
        archiveMemory(mem);
        archived++;
      } else {
        mem.scope = "decayed";
        mem.tier = "short_term";
        decayed++;
      }
    } else if (tier === "mid_term" && age > MID_TERM_THRESHOLD) {
      const recentlyRecalled = lastRecalled > 0 && now - lastRecalled < MID_TERM_THRESHOLD;
      if (!recentlyRecalled) {
        mem.tier = "long_term";
        if (mem.content.length > 120) {
          mem.content = mem.content.slice(0, 100).trimEnd() + "\u2026";
        }
        compressed++;
      }
    }
    if (mem.utility && Math.abs(mem.utility) > 0.01) {
      mem.utility *= 0.99;
      if (Math.abs(mem.utility) < 0.01) mem.utility = 0;
    }
  }
  if (upgraded > 0 || decayed > 0 || compressed > 0 || archived > 0 || faded > 0 || gisted > 0 || absorbed > 0) {
    rebuildScopeIndex();
    rebuildRecallIndex(memoryState.memories);
    saveMemories();
    console.log(`[cc-soul][memory-decay] upgraded=${upgraded} decayed=${decayed} compressed=${compressed} archived=${archived} faded=${faded} gisted=${gisted} absorbed=${absorbed}`);
  }
}
let lastPhysicalCleanup = 0;
const PHYSICAL_CLEANUP_COOLDOWN = 24 * 36e5;
function pruneExpiredMemories() {
  const now = Date.now();
  if (now - lastPhysicalCleanup < PHYSICAL_CLEANUP_COOLDOWN) return;
  lastPhysicalCleanup = now;
  if (useSQLite) {
    sqliteCleanupExpired();
  }
  const before = memoryState.memories.length;
  const EXPIRED_CUTOFF = 30 * 864e5;
  const DECAYED_CUTOFF = 90 * 864e5;
  const PROTECTED_SCOPES_DEL = /* @__PURE__ */ new Set([
    "fact",
    "wal",
    "preference",
    "event",
    "correction",
    "deep_feeling",
    "wisdom",
    "pinned"
  ]);
  memoryState.memories = memoryState.memories.filter((m) => {
    if (PROTECTED_SCOPES_DEL.has(m.scope)) return true;
    if (m.scope === "expired" && now - m.ts > EXPIRED_CUTOFF) return false;
    if (m.scope === "decayed" && now - m.ts > DECAYED_CUTOFF && (m.recallCount ?? 0) === 0) return false;
    return true;
  });
  const removed = before - memoryState.memories.length;
  if (removed > 0) {
    rebuildScopeIndex();
    rebuildRecallIndex(memoryState.memories);
    saveMemories();
    console.log(`[cc-soul][prune] physically removed ${removed} dead memories (${before} \u2192 ${memoryState.memories.length})`);
  }
}
let lastCompression = 0;
const COMPRESSION_COOLDOWN = 24 * 36e5;
function compressOldMemories() {
  const now = Date.now();
  if (now - lastCompression < COMPRESSION_COOLDOWN) return;
  lastCompression = now;
  const SKIP_SCOPES = /* @__PURE__ */ new Set(["correction", "consolidated", "expired", "decayed", "dream", "curiosity"]);
  const SEVEN_DAYS = 7 * 864e5;
  const THIRTY_DAYS = 30 * 864e5;
  let compressed = 0;
  for (const mem of memoryState.memories) {
    if (SKIP_SCOPES.has(mem.scope)) continue;
    if (mem.flashbulb?.detailLevel === "full") continue;
    const age = now - mem.ts;
    if (age > SEVEN_DAYS && mem.content.length > 100 && mem.tier !== "long_term") {
      const original = mem.content;
      const firstSentence = mem.content.split(/[。！？\n]/)[0];
      if (firstSentence && firstSentence.length < mem.content.length * 0.6) {
        if (!mem.history) mem.history = [];
        mem.history.push({ content: original, ts: now });
        mem.content = firstSentence.slice(0, 80);
        mem.tier = "mid_term";
        compressed++;
      }
    }
    if (age > THIRTY_DAYS && mem.content.length > 60 && mem.tier !== "long_term") {
      const original = mem.content;
      if (!mem.history) mem.history = [];
      if (!mem.history.some((h) => h.content === original)) {
        mem.history.push({ content: original, ts: now });
      }
      let gist = "";
      try {
        const { extractFacts } = require("./fact-store.ts");
        const facts = extractFacts(original);
        if (facts.length > 0) {
          gist = facts.slice(0, 3).map((f) => `${f.subject}${f.predicate}${f.object}`).join("\uFF0C");
        }
      } catch {
      }
      if (!gist) {
        gist = original.slice(0, 40) + "\u2026";
      }
      mem.content = gist;
      mem.tier = "long_term";
      compressed++;
    }
  }
  if (compressed > 0) {
    saveMemories();
    console.log(`[cc-soul][compress] compressed ${compressed} old memories`);
  }
}
let lastRevival = 0;
const REVIVAL_COOLDOWN = 12 * 36e5;
function reviveDecayedMemories() {
  const now = Date.now();
  if (now - lastRevival < REVIVAL_COOLDOWN) return;
  lastRevival = now;
  const candidates = memoryState.memories.filter(
    (m) => m.scope === "decayed" && m.tags && m.tags.length > 0 && (m.confidence ?? 0) > 0.5 && ((m.recallCount ?? 0) > 0 || m.emotion === "important" || m.emotion === "warm")
  );
  if (candidates.length === 0) return;
  candidates.sort((a, b) => {
    const scoreA = (a.recallCount ?? 0) * 2 + (a.confidence ?? 0) + (a.emotion === "important" ? 1 : 0);
    const scoreB = (b.recallCount ?? 0) * 2 + (b.confidence ?? 0) + (b.emotion === "important" ? 1 : 0);
    return scoreB - scoreA;
  });
  let revived = 0;
  for (const mem of candidates.slice(0, 20)) {
    mem.scope = "fact";
    mem.tier = "mid_term";
    mem.lastAccessed = now;
    revived++;
  }
  if (revived > 0) {
    rebuildScopeIndex();
    saveMemories();
    console.log(`[cc-soul][revival] revived ${revived} valuable decayed memories (from ${candidates.length} candidates)`);
  }
}
function archiveMemory(mem) {
  mem.raw_line = mem.content;
  const summary = mem.content.length > 50 ? mem.content.slice(0, 50).trimEnd() + "..." : mem.content;
  mem.content = summary;
  mem.scope = "archived";
  if (!mem._originalTier) mem._originalTier = mem.tier || "short_term";
  if (useSQLite) {
    const row = sqliteFindByContent(mem.raw_line);
    if (row) {
      sqliteUpdateMemory(row.id, { scope: "archived", content: summary });
      sqliteUpdateRawLine(row.id, mem.raw_line);
    }
  }
}
function restoreArchivedMemories(keyword) {
  const _db = getDb();
  if (!_db) return 0;
  const kw = `%${keyword}%`;
  const rows = _db.prepare("SELECT id, content, raw_line FROM memories WHERE scope = 'archived' AND (raw_line LIKE ? OR content LIKE ?) LIMIT 10").all(kw, kw);
  let restored = 0;
  for (const row of rows) {
    const newContent = row.raw_line || row.content;
    _db.prepare("UPDATE memories SET content = ?, scope = 'mid_term', tier = 'mid_term', lastAccessed = ?, raw_line = '' WHERE id = ?").run(newContent, Date.now(), row.id);
    restored++;
  }
  if (restored > 0) console.log(`[cc-soul][dag-archive] restored ${restored} memories matching "${keyword}"`);
  return restored;
}
function resolveNetworkConflicts() {
  const now = Date.now();
  const localFacts = memoryState.memories.filter(
    (m) => !m.content.startsWith("[\u7F51\u7EDC\u77E5\u8BC6") && (m.scope === "fact" || m.scope === "consolidated") && m.scope !== "expired"
  );
  const networkFacts = memoryState.memories.filter(
    (m) => m.content.startsWith("[\u7F51\u7EDC\u77E5\u8BC6") && m.scope !== "expired"
  );
  if (localFacts.length === 0 || networkFacts.length === 0) return;
  let resolved = 0;
  for (const net of networkFacts) {
    const netWords = new Set(
      (net.content.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map((w) => w.toLowerCase())
    );
    for (const local of localFacts) {
      const localWords = (local.content.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map((w) => w.toLowerCase());
      const overlap = localWords.filter((w) => netWords.has(w)).length;
      if (overlap >= 3 && local.content !== net.content.replace(/^\[网络知识[|｜][^\]]*\]\s*/, "")) {
        if (local.ts > net.ts) {
          net.scope = "expired";
          resolved++;
          break;
        }
      }
    }
  }
  if (resolved > 0) {
    saveMemories();
    console.log(`[cc-soul][network-conflicts] resolved ${resolved} network vs local conflicts (local wins)`);
  }
}
async function sqliteMaintenance() {
  if (!useSQLite) return;
  sqliteCleanupExpired();
  try {
    const now = Date.now();
    if (now - _lastVacuumTs > 864e5) {
      const sqlMod = require("./sqlite-store.ts");
      if (sqlMod?.isSQLiteReady?.()) {
        let db = null;
        try {
          db = require("./sqlite-store.ts").getDb?.();
        } catch {
        }
        if (db) {
          db.exec("VACUUM");
          _lastVacuumTs = now;
          console.log("[cc-soul][sqlite] VACUUM completed");
        }
      }
    }
  } catch {
  }
}
let _lastVacuumTs = 0;
function getStorageStatus() {
  return {
    backend: useSQLite ? "sqlite" : "json",
    vectorSearch: false
    // retired — activation field handles recall
  };
}
const AUDIT_PATH = resolve(DATA_DIR, "memory_audit.json");
let lastAuditTs = 0;
function auditMemoryHealth() {
  const now = Date.now();
  if (now - lastAuditTs < 864e5) return;
  lastAuditTs = now;
  const active = memoryState.memories.filter((m) => m.scope !== "expired" && m.scope !== "decayed");
  const sample = active.slice(0, 500);
  const duplicates = [];
  for (let i = 0; i < sample.length && duplicates.length < 20; i++) {
    const tA = trigrams(sample[i].content);
    for (let j = i + 1; j < sample.length && duplicates.length < 20; j++) {
      const sim = trigramSimilarity(tA, trigrams(sample[j].content));
      if (sim > 0.9) duplicates.push({ a: sample[i].content.slice(0, 60), b: sample[j].content.slice(0, 60), sim: +sim.toFixed(2) });
    }
  }
  const tooShort = active.filter((m) => m.content.length < 10).map((m) => m.content);
  const untagged = active.filter((m) => !m.tags || m.tags.length === 0).length;
  const lowConfidence = active.filter((m) => (m.confidence ?? 0.7) < 0.3).length;
  const thirtyDaysAgo = now - 30 * 864e5;
  const zombie = active.filter((m) => (m.recallCount ?? 0) === 0 && m.ts < thirtyDaysAgo).length;
  const staleExpiry = active.filter((m) => m.validUntil && m.validUntil < now).length;
  const parts = [];
  if (duplicates.length > 0) parts.push(`\u5EFA\u8BAE\u5408\u5E76 ${duplicates.length} \u7EC4\u91CD\u590D\u8BB0\u5FC6`);
  if (tooShort.length > 0) parts.push(`\u5EFA\u8BAE\u6E05\u7406 ${tooShort.length} \u6761\u8FC7\u77ED\u8BB0\u5FC6`);
  if (untagged > active.length * 0.3) parts.push(`${untagged} \u6761\u8BB0\u5FC6\u7F3A\u5C11\u6807\u7B7E\uFF0C\u5EFA\u8BAE\u6279\u91CF\u6253\u6807`);
  if (lowConfidence > 0) parts.push(`${lowConfidence} \u6761\u4F4E\u7F6E\u4FE1\u5EA6\u8BB0\u5FC6\uFF08<0.3\uFF09\uFF0C\u5EFA\u8BAE\u6E05\u7406`);
  if (zombie > 0) parts.push(`${zombie} \u6761\u50F5\u5C38\u8BB0\u5FC6\uFF0830\u5929\u96F6\u547D\u4E2D\uFF09\uFF0C\u5EFA\u8BAE\u6DD8\u6C70`);
  if (staleExpiry > 0) parts.push(`${staleExpiry} \u6761\u8BB0\u5FC6\u5DF2\u8FC7 validUntil \u4F46\u672A\u8FC7\u671F\uFF0C\u5EFA\u8BAE\u6E05\u7406`);
  const audit = { ts: now, duplicates, tooShort: tooShort.slice(0, 20), untagged, lowConfidence, zombie, staleExpiry, suggestions: parts.join("\uFF1B") || "\u8BB0\u5FC6\u72B6\u6001\u826F\u597D" };
  debouncedSave(AUDIT_PATH, audit);
  console.log(`[cc-soul][memory-audit] duplicates=${duplicates.length} short=${tooShort.length} untagged=${untagged} lowConf=${lowConfidence} zombie=${zombie} staleExpiry=${staleExpiry}`);
}
const CAUSAL_PATH = resolve(DATA_DIR, "causal_chains.json");
let causalChains = loadJson(CAUSAL_PATH, []);
function saveCausalChains() {
  debouncedSave(CAUSAL_PATH, causalChains);
}
function extractCausalChain(history) {
  if (history.length < 3) return null;
  const first = history[0];
  const last = history[history.length - 1];
  const isProblem = /问题|报错|出错|不行|怎么办|bug|error|crash|失败|异常/.test(first.user);
  if (!isProblem) return null;
  const isResolved = /解决|搞定|好了|找到|原来|明白了|谢谢|可以了/.test(last.user);
  const isUnresolved = /还是不行|放弃|算了|不管了/.test(last.user);
  if (!isResolved && !isUnresolved) return null;
  const steps = history.slice(0, -1).map((h) => {
    const actions = h.ai.match(/(?:检查|试试|确认|查看|运行|执行|修改|更新|重启|清除|添加|删除).{2,20}/g);
    return actions ? actions[0] : h.ai.slice(0, 30);
  }).filter(Boolean);
  if (steps.length === 0) return null;
  const chain = {
    trigger: first.user.slice(0, 60),
    steps,
    outcome: isResolved ? "resolved" : "unresolved",
    confidence: isResolved ? 0.7 : 0.3,
    ts: Date.now(),
    hitCount: 0
  };
  const existing = causalChains.find((c) => {
    const cWords = new Set((c.trigger.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map((w) => w.toLowerCase()));
    const newWords = (chain.trigger.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map((w) => w.toLowerCase());
    const overlap = newWords.filter((w) => cWords.has(w)).length;
    return overlap >= 2;
  });
  if (existing) {
    if (chain.outcome === "resolved") {
      existing.steps = chain.steps;
      existing.outcome = "resolved";
      existing.confidence = Math.min(0.95, existing.confidence + 0.1);
      existing.ts = Date.now();
    }
    saveCausalChains();
    return null;
  }
  causalChains.push(chain);
  if (causalChains.length > 50) {
    causalChains.sort((a, b) => b.hitCount * 10 + b.ts / 1e10 - (a.hitCount * 10 + a.ts / 1e10));
    causalChains = causalChains.slice(0, 50);
  }
  saveCausalChains();
  console.log(`[cc-soul][causal] new chain: "${chain.trigger.slice(0, 30)}" \u2192 ${chain.steps.length} steps \u2192 ${chain.outcome}`);
  return chain;
}
function queryCausalChain(problem) {
  const problemWords = new Set((problem.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map((w) => w.toLowerCase()));
  if (problemWords.size === 0) return null;
  let bestChain = null;
  let bestScore = 0;
  for (const chain of causalChains) {
    if (chain.outcome !== "resolved") continue;
    const chainWords = (chain.trigger.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map((w) => w.toLowerCase());
    const overlap = chainWords.filter((w) => problemWords.has(w)).length;
    const score = overlap / Math.max(1, problemWords.size) * chain.confidence;
    if (score > bestScore && score > 0.3) {
      bestScore = score;
      bestChain = chain;
    }
  }
  if (bestChain) {
    bestChain.hitCount++;
    saveCausalChains();
  }
  return bestChain;
}
function getCausalChainCount() {
  return causalChains.filter((c) => c.outcome === "resolved").length;
}
export {
  assessResponseQuality,
  associateSync,
  auditMemoryHealth,
  buildEpisodeContext,
  cleanupNetworkKnowledge,
  compressOldMemories,
  consolidateMemories,
  episodes,
  executeMemoryCommands,
  extractCausalChain,
  generateInsights,
  generatePrediction,
  getAssociativeRecall,
  getCausalChainCount,
  getPendingSearchResults,
  getStorageStatus,
  loadEpisodes,
  parseMemoryCommands,
  predictiveRecall,
  processMemoryDecay,
  pruneExpiredMemories,
  queryCausalChain,
  recallEpisodes,
  recallFeedbackLoop,
  recordEpisode,
  resolveNetworkConflicts,
  restoreArchivedMemories,
  reviveDecayedMemories,
  scanForContradictions,
  sqliteMaintenance,
  triggerAssociativeRecall,
  triggerSessionSummary
};
