import { getParam } from "./auto-tune.ts";
import { onCacheEvent } from "./memory-utils.ts";
onCacheEvent("memory_deleted", () => invalidateEntityMemoryIndex());
onCacheEvent("consolidation", () => {
  invalidateEntityMemoryIndex();
  _pageRankDirty = true;
});
onCacheEvent("identity_changed", () => {
  invalidateEntityMemoryIndex();
  _pageRankDirty = true;
});
onCacheEvent("correction_received", () => {
  _pageRankDirty = true;
});
import {
  dbGetEntities,
  dbAddEntity,
  dbUpdateEntity,
  dbGetRelations,
  dbAddRelation,
  dbInvalidateEntity,
  dbTrimEntities,
  dbTrimRelations,
  dbInvalidateStaleRelations,
  isSQLiteReady
} from "./sqlite-store.ts";
function getStaleThresholdMs() {
  return getParam("graph.stale_days") * 24 * 60 * 60 * 1e3;
}
const graphState = {
  entities: [],
  relations: [],
  ranks: /* @__PURE__ */ new Map()
};
let _entityToMemIdx = null;
let _indexedMemCount = 0;
function ensureEntityMemoryIndex(memories) {
  const entityNames = graphState.entities.filter((e) => e.invalid_at === null && e.name.length >= 2).map((e) => e.name);
  if (!_entityToMemIdx) {
    _entityToMemIdx = /* @__PURE__ */ new Map();
    for (const name of entityNames) _entityToMemIdx.set(name, /* @__PURE__ */ new Set());
    for (let i = 0; i < memories.length; i++) {
      const mem = memories[i];
      if (mem.scope === "expired" || mem.scope === "decayed") continue;
      for (const name of entityNames) {
        if (mem.content.includes(name)) {
          _entityToMemIdx.get(name).add(i);
        }
      }
    }
    _indexedMemCount = memories.length;
  } else if (memories.length > _indexedMemCount) {
    for (let i = _indexedMemCount; i < memories.length; i++) {
      const mem = memories[i];
      if (mem.scope === "expired" || mem.scope === "decayed") continue;
      for (const name of entityNames) {
        if (mem.content.includes(name)) {
          if (!_entityToMemIdx.has(name)) _entityToMemIdx.set(name, /* @__PURE__ */ new Set());
          _entityToMemIdx.get(name).add(i);
        }
      }
    }
    for (const name of entityNames) {
      if (!_entityToMemIdx.has(name)) {
        const s = /* @__PURE__ */ new Set();
        for (let i = 0; i < memories.length; i++) {
          const mem = memories[i];
          if (mem.scope !== "expired" && mem.scope !== "decayed" && mem.content.includes(name)) s.add(i);
        }
        _entityToMemIdx.set(name, s);
      }
    }
    _indexedMemCount = memories.length;
  }
  return _entityToMemIdx;
}
function invalidateEntityMemoryIndex() {
  _entityToMemIdx = null;
  _indexedMemCount = 0;
}
let _pageRankDirty = true;
function loadGraph() {
  if (!isSQLiteReady()) return;
  const entities = dbGetEntities();
  const relations = dbGetRelations();
  graphState.entities.length = 0;
  graphState.entities.push(...entities);
  graphState.relations.length = 0;
  graphState.relations.push(...relations);
}
function syncFromDb() {
  if (!isSQLiteReady()) return;
  graphState.entities.length = 0;
  graphState.entities.push(...dbGetEntities());
  graphState.relations.length = 0;
  graphState.relations.push(...dbGetRelations());
}
function addEntity(name, type, attrs = []) {
  if (!name || name.length < 2) return;
  dbAddEntity(name, type, attrs);
  dbTrimEntities(800);
  syncFromDb();
  _pageRankDirty = true;
  invalidateEntityMemoryIndex();
}
function addRelation(source, target, type) {
  if (!source || !target) return;
  dbAddRelation(source, target, type);
  dbTrimRelations(800);
  syncFromDb();
  _pageRankDirty = true;
}
function addEntitiesFromAnalysis(entities) {
  for (const e of entities) {
    if (e.name && e.name.length >= 2) {
      dbAddEntity(e.name, e.type);
      if (e.relation) dbAddRelation(e.name, "\u7528\u6237", e.relation.slice(0, 30));
    }
  }
  dbTrimEntities(800);
  dbTrimRelations(800);
  syncFromDb();
  _pageRankDirty = true;
  invalidateEntityMemoryIndex();
}
function invalidateEntity(name) {
  dbInvalidateEntity(name);
  syncFromDb();
  _pageRankDirty = true;
  invalidateEntityMemoryIndex();
}
function invalidateStaleEntities() {
  const now = Date.now();
  let count = 0;
  for (const entity of graphState.entities) {
    if (entity.invalid_at !== null) continue;
    const lastActivity = Math.max(entity.valid_at || 0, entity.firstSeen || 0);
    if (now - lastActivity > getStaleThresholdMs() && entity.mentions <= 1) {
      dbUpdateEntity(entity.name, { invalid_at: now });
      count++;
    }
  }
  if (count > 0) syncFromDb();
  return count;
}
function invalidateStaleRelations() {
  const now = Date.now();
  const thresholdMs = getStaleThresholdMs();
  let count = 0;
  for (const r of graphState.relations) {
    if (r.invalid_at !== null) continue;
    const lastActivity = Math.max(r.valid_at || 0, r.ts || 0);
    if (now - lastActivity > thresholdMs) {
      r.invalid_at = now;
      count++;
    }
  }
  if (count > 0) {
    if (isSQLiteReady()) {
      dbInvalidateStaleRelations(thresholdMs);
    }
    _pageRankDirty = true;
  }
  return count;
}
function findMentionedEntities(msg) {
  const mentioned = graphState.entities.filter((e) => e.invalid_at === null && e.name.length >= 3 && new RegExp("(?:^|[^a-zA-Z\\u4e00-\\u9fff])" + e.name.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "(?:[^a-zA-Z\\u4e00-\\u9fff]|$)", "i").test(msg)).sort((a, b) => b.mentions - a.mentions).slice(0, 5);
  const _COMMON_CAPS = /* @__PURE__ */ new Set(["The", "This", "That", "What", "When", "Where", "How", "Who", "Which", "Why", "Yes", "No", "And", "But", "For", "Not", "Are", "Was", "Were", "Has", "Have", "Had", "Does", "Did", "Will", "Can", "May", "She", "Her", "His", "They", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]);
  const enNames = msg.match(/\b([A-Z][a-z]{2,})\b/g) || [];
  const mentionedNames = new Set(mentioned.map((e) => e.name.toLowerCase()));
  for (const name of enNames) {
    if (!_COMMON_CAPS.has(name) && !mentionedNames.has(name.toLowerCase())) {
      const existing = graphState.entities.find((e) => e.name.toLowerCase() === name.toLowerCase());
      if (existing) {
        existing.mentions++;
        mentioned.push(existing);
      } else {
        const newEntity = { name, type: "person", mentions: 1, activation: 0.3, created_at: Date.now(), lastMentionedAt: Date.now(), lastActivatedAt: Date.now(), invalid_at: null, attrs: {} };
        graphState.entities.push(newEntity);
        mentioned.push(newEntity);
      }
      mentionedNames.add(name.toLowerCase());
    }
  }
  for (const e of mentioned) {
    e.activation = Math.min(1, (e.activation ?? 0) + 0.3);
    e.lastActivatedAt = Date.now();
    for (const r of graphState.relations) {
      if (r.invalid_at !== null) continue;
      const neighbor = r.source === e.name ? r.target : r.target === e.name ? r.source : null;
      if (!neighbor) continue;
      const ne = graphState.entities.find((n) => n.name === neighbor && n.invalid_at === null);
      if (ne) {
        ne.activation = Math.min(1, (ne.activation ?? 0) + 0.1);
        ne.lastActivatedAt = Date.now();
      }
    }
  }
  return mentioned.map((e) => e.name);
}
function decayActivations(factor = 0.92) {
  for (const e of graphState.entities) {
    if (e.activation && e.activation > 0.01) {
      e.activation *= factor;
      if (e.activation < 0.01) e.activation = 0;
    }
  }
}
const RELATION_WEIGHTS = {
  caused_by: 1.5,
  depends_on: 1.3,
  contradicts: 0.5,
  uses: 1,
  works_at: 1,
  knows: 0.8,
  part_of: 0.9,
  related_to: 0.7,
  follows: 0.6,
  prefers_over: 1.1,
  triggers: 1.2,
  learned_from: 1.3
};
function temporalGravity(relation, now) {
  const age = now - (relation.valid_at || relation.ts || 0);
  const ageDays = age / 864e5;
  return Math.max(0.3, Math.exp(-ageDays / 90));
}
function getRelatedEntities(mentionedEntities, maxHops = 2, maxResults = 10) {
  const now = Date.now();
  const visited = new Set(mentionedEntities);
  let frontier = [...mentionedEntities];
  for (let hop = 0; hop < maxHops; hop++) {
    const candidates = [];
    for (const entity of frontier) {
      for (const r of graphState.relations) {
        if (r.invalid_at !== null) continue;
        const neighbor = r.source === entity ? r.target : r.target === entity ? r.source : null;
        if (!neighbor || visited.has(neighbor)) continue;
        const relWeight = (r.weight ?? 1) * (RELATION_WEIGHTS[r.type] ?? 0.8) * temporalGravity(r, now);
        candidates.push({ name: neighbor, weight: relWeight });
      }
    }
    candidates.sort((a, b) => b.weight - a.weight);
    const nextFrontier = [];
    for (const c of candidates) {
      if (visited.has(c.name)) continue;
      visited.add(c.name);
      nextFrontier.push(c.name);
      if (visited.size >= maxResults + mentionedEntities.length) break;
    }
    frontier = nextFrontier;
    if (visited.size >= maxResults + mentionedEntities.length) break;
  }
  for (const m of mentionedEntities) visited.delete(m);
  return [...visited].slice(0, maxResults);
}
function graphWalkRecall(startEntity, memories, maxDepth = 2, maxNodes = 10) {
  const visited = /* @__PURE__ */ new Set([startEntity]);
  let frontier = [startEntity];
  for (let depth = 0; depth < maxDepth && frontier.length > 0; depth++) {
    const next = [];
    for (const entity of frontier) {
      for (const r of graphState.relations) {
        if (r.invalid_at !== null) continue;
        const neighbor = r.source === entity ? r.target : r.target === entity ? r.source : null;
        if (neighbor && !visited.has(neighbor)) {
          visited.add(neighbor);
          next.push(neighbor);
          if (visited.size >= maxNodes + 1) break;
        }
      }
      if (visited.size >= maxNodes + 1) break;
    }
    frontier = next;
  }
  visited.delete(startEntity);
  if (visited.size === 0) return [];
  const results = [];
  const walkedNames = [...visited];
  for (const mem of memories) {
    if (mem.scope === "expired" || mem.scope === "decayed") continue;
    for (const name of walkedNames) {
      if (mem.content.includes(name)) {
        results.push(mem.content);
        break;
      }
    }
    if (results.length >= maxNodes) break;
  }
  return results;
}
function personalizedPageRank(seeds, alpha = 0.15, maxIter = 20) {
  if (seeds.length === 0) return /* @__PURE__ */ new Map();
  const activeEntities = new Set(
    graphState.entities.filter((e) => e.invalid_at === null).map((e) => e.name)
  );
  const validSeeds = seeds.filter((s) => activeEntities.has(s));
  if (validSeeds.length === 0) return /* @__PURE__ */ new Map();
  const ranks = /* @__PURE__ */ new Map();
  for (const s of validSeeds) ranks.set(s, 1 / validSeeds.length);
  const outEdges = /* @__PURE__ */ new Map();
  const now = Date.now();
  for (const name of activeEntities) outEdges.set(name, []);
  for (const r of graphState.relations) {
    if (r.invalid_at !== null) continue;
    if (!activeEntities.has(r.source) || !activeEntities.has(r.target)) continue;
    const relTypeWeight = RELATION_WEIGHTS[r.type] ?? 0.8;
    const w = (r.weight ?? 1) * (r.confidence ?? 0.7) * relTypeWeight * temporalGravity(r, now);
    outEdges.get(r.source).push({ target: r.target, weight: w });
  }
  for (let iter = 0; iter < maxIter; iter++) {
    const newRanks = /* @__PURE__ */ new Map();
    for (const s of validSeeds) newRanks.set(s, alpha / validSeeds.length);
    for (const [node, rank] of ranks) {
      const edges = outEdges.get(node);
      if (!edges || edges.length === 0) continue;
      const totalWeight = edges.reduce((s, e) => s + e.weight, 0);
      if (totalWeight <= 0) continue;
      for (const e of edges) {
        const share = (1 - alpha) * rank * (e.weight / totalWeight);
        newRanks.set(e.target, (newRanks.get(e.target) || 0) + share);
      }
    }
    ranks.clear();
    for (const [k, v] of newRanks) ranks.set(k, v);
  }
  return ranks;
}
function spreadingActivation(seeds, graphStateRef, maxIter = 3, decayFactor = 0.5) {
  const activation = /* @__PURE__ */ new Map();
  for (const s of seeds) activation.set(s, 1);
  for (let iter = 0; iter < maxIter; iter++) {
    const newActivation = /* @__PURE__ */ new Map();
    for (const [node, act] of activation) {
      if (act < 0.01) continue;
      const edges = graphStateRef.relations.filter(
        (r) => (r.source === node || r.target === node) && !r.invalid_at
      );
      for (const e of edges) {
        const neighbor = e.source === node ? e.target : e.source;
        const edgeWeight = (e.weight || 1) * (RELATION_WEIGHTS[e.type] || 0.7);
        const spread = act * decayFactor * edgeWeight;
        newActivation.set(neighbor, (newActivation.get(neighbor) || 0) + spread);
      }
    }
    for (const [k, v] of newActivation) {
      activation.set(k, (activation.get(k) || 0) + v);
    }
  }
  return activation;
}
function graphWalkRecallScored(startEntities, memories, maxDepth = 2, maxResults = 8) {
  const pprRanks = personalizedPageRank(startEntities, 0.15, Math.min(maxDepth * 5, 20));
  const entityScores = /* @__PURE__ */ new Map();
  for (const start of startEntities) entityScores.set(start, 1);
  for (const [entity, pprScore] of pprRanks) {
    if (entityScores.has(entity)) continue;
    const gravityBoost = _neighborCache.has(startEntities[0]) && _neighborCache.get(startEntities[0]).has(entity) ? 0.3 : 0;
    entityScores.set(entity, pprScore + gravityBoost);
    if (entityScores.size >= maxResults * 3) break;
  }
  for (const s of startEntities) entityScores.delete(s);
  if (entityScores.size === 0) return [];
  const idx = ensureEntityMemoryIndex(memories);
  const memScoreMap = /* @__PURE__ */ new Map();
  for (const [entityName, entityScore] of entityScores) {
    const memIndices = idx.get(entityName);
    if (!memIndices) continue;
    for (const i of memIndices) {
      memScoreMap.set(i, (memScoreMap.get(i) || 0) + entityScore);
    }
  }
  const results = [];
  for (const [i, score] of memScoreMap) {
    if (i < memories.length) {
      results.push({ content: memories[i].content, graphScore: score });
    }
  }
  results.sort((a, b) => b.graphScore - a.graphScore);
  return results.slice(0, maxResults);
}
function generateEntitySummary(entityName) {
  const entity = graphState.entities.find((e) => e.name === entityName && e.invalid_at === null);
  if (!entity) return null;
  const rels = graphState.relations.filter((r) => r.invalid_at === null && (r.source === entityName || r.target === entityName)).map((r) => r.source === entityName ? `${r.type} \u2192 ${r.target}` : `${r.source} ${r.type} \u2192`);
  const parts = [`[${entity.type}] ${entityName} (\u63D0\u53CA${entity.mentions}\u6B21)`];
  if (entity.attrs.length > 0) parts.push(`\u5C5E\u6027: ${entity.attrs.join(", ")}`);
  if (rels.length > 0) parts.push(`\u5173\u7CFB: ${rels.slice(0, 8).join("; ")}`);
  return parts.join(" | ");
}
function queryEntityContext(msg) {
  const mentionedNames = [];
  const results = [];
  for (const entity of graphState.entities) {
    if (entity.invalid_at !== null) continue;
    if (msg.includes(entity.name)) mentionedNames.push(entity.name);
  }
  const pprRanks = mentionedNames.length > 0 ? spreadingActivation(mentionedNames, graphState, 3, 0.5) : graphState.ranks;
  for (const entity of graphState.entities) {
    if (entity.invalid_at !== null) continue;
    if (!msg.includes(entity.name)) continue;
    const rels = graphState.relations.filter(
      (r) => r.invalid_at === null && (r.source === entity.name || r.target === entity.name)
    );
    const rank = pprRanks.get(entity.name) || 0;
    if (rels.length > 0) {
      const relStr = rels.map((r) => `${r.source} ${r.type} ${r.target}`).join(", ");
      results.push({ text: `[${entity.type}] ${entity.name}: ${relStr}`, rank });
    } else if (entity.attrs.length > 0) {
      results.push({ text: `[${entity.type}] ${entity.name}: ${entity.attrs.join(", ")}`, rank });
    }
  }
  results.sort((a, b) => b.rank - a.rank);
  return results.slice(0, 3).map((r) => r.text);
}
const _neighborCache = /* @__PURE__ */ new Map();
function computeEntityRanks() {
  computePageRank();
}
function computePageRank(iterations = 3, dampingFactor = 0.85) {
  if (!_pageRankDirty && graphState.ranks.size > 0) return;
  const activeEntities = graphState.entities.filter((e) => e.invalid_at === null);
  const N = activeEntities.length;
  if (N === 0) {
    graphState.ranks.clear();
    return;
  }
  const now = Date.now();
  const names = new Set(activeEntities.map((e) => e.name));
  const ranks = /* @__PURE__ */ new Map();
  for (const entity of activeEntities) {
    const refTs = entity.lastActivatedAt || entity.firstSeen || entity.valid_at || now;
    const ageDays = Math.max(0, (now - refTs) / 864e5);
    const recencyFactor = Math.exp(-ageDays / 30);
    const emotionalCharge = 1 + (entity.activation ?? 0) * 0.5;
    const M = Math.max(0.01, entity.mentions * recencyFactor * emotionalCharge);
    ranks.set(entity.name, M);
  }
  _neighborCache.clear();
  const adjacency = /* @__PURE__ */ new Map();
  for (const name of names) adjacency.set(name, /* @__PURE__ */ new Set());
  for (const r of graphState.relations) {
    if (r.invalid_at !== null) continue;
    if (!names.has(r.source) || !names.has(r.target)) continue;
    adjacency.get(r.source).add(r.target);
    adjacency.get(r.target).add(r.source);
  }
  for (const name of names) {
    const hop1 = adjacency.get(name) || /* @__PURE__ */ new Set();
    const hop2 = new Set(hop1);
    for (const n1 of hop1) {
      const n1Neighbors = adjacency.get(n1) || /* @__PURE__ */ new Set();
      for (const n2 of n1Neighbors) {
        if (n2 !== name) hop2.add(n2);
      }
    }
    _neighborCache.set(name, hop2);
  }
  graphState.ranks = ranks;
  _pageRankDirty = false;
  console.log(`[cc-soul][graph] contextualEntityRank: ${N} entities, ${_neighborCache.size} neighbor caches`);
}
const ROLE_PATTERNS = /老板|领导|boss|同事|colleague|朋友|女朋友|男朋友|老婆|老公|爸|妈|哥|姐|弟|妹|老师|客户/g;
function detectMentionedPeople(msg) {
  const roles = msg.match(ROLE_PATTERNS) || [];
  const names = msg.match(/[小大老][A-Z\u4e00-\u9fff]/g) || [];
  return [.../* @__PURE__ */ new Set([...roles, ...names])];
}
function updateSocialGraph(msg, mood) {
  const people = detectMentionedPeople(msg);
  for (const name of people) {
    let entity = graphState.entities.find((e) => e.name === name && e.type === "person");
    if (!entity) {
      entity = {
        name,
        type: "person",
        attrs: [],
        firstSeen: Date.now(),
        mentions: 0,
        valid_at: Date.now(),
        invalid_at: null
      };
      graphState.entities.push(entity);
      _pageRankDirty = true;
    }
    entity.mentions++;
    entity.lastActivatedAt = Date.now();
    entity.activation = Math.min(1, (entity.activation ?? 0) + 0.3);
    try {
      const { inferRelationship } = require("./dynamic-extractor.ts");
      const rel = inferRelationship(name);
      if (rel !== "unknown" && !entity.attrs.includes(`role:${rel}`)) {
        entity.attrs = entity.attrs.filter((a) => !a.startsWith("role:"));
        entity.attrs.push(`role:${rel}`);
      }
    } catch {
    }
    const moodLabel = mood > 0.2 ? "positive_interaction" : mood < -0.2 ? "negative_interaction" : "neutral_interaction";
    const topic = msg.replace(new RegExp(name, "g"), "").match(/[\u4e00-\u9fff]{2,4}/)?.[0];
    entity.attrs.push(moodLabel);
    if (entity.attrs.length > 20) entity.attrs = entity.attrs.slice(-20);
    const formalRe = /请问|您|汇报|报告|会议|安排|deadline|项目|审批|review|领导|老板|boss|客户/i;
    const casualRe = /哈哈|lol|hhh|卧槽|牛逼|nb|6{2,}|yyds|绝了|离谱|兄弟|哥们|姐妹|朋友/i;
    if (formalRe.test(msg) && !entity.attrs.includes("tone:formal")) entity.attrs.push("tone:formal");
    if (casualRe.test(msg) && !entity.attrs.includes("tone:casual")) entity.attrs.push("tone:casual");
    if (people.length >= 2) {
      for (const other of people) {
        if (other === name) continue;
        const hasAlias = graphState.relations.some(
          (r) => r.type === "alias_of" && (r.source === name && r.target === other || r.source === other && r.target === name)
        );
        if (!hasAlias && msg.includes(name) && msg.includes(other) && Math.abs(msg.indexOf(name) - msg.indexOf(other)) < 10) {
          addRelation(name, other, "alias_of");
        }
      }
    }
    if (topic) {
      const hasTopicRel = graphState.relations.some(
        (r) => r.source === name && r.target === topic && r.type === "mentioned_with"
      );
      if (!hasTopicRel) addRelation(name, topic, "mentioned_with");
    }
  }
  if (people.length > 0) {
    for (const name of people) {
      const entity = graphState.entities.find((e) => e.name === name && e.type === "person");
      if (entity) try {
        dbUpdateEntity(entity.name, { mentions: entity.mentions, attrs: entity.attrs });
      } catch {
      }
    }
    _pageRankDirty = true;
  }
}
function getSocialContext(msg) {
  const people = detectMentionedPeople(msg);
  if (people.length === 0) return null;
  const hints = [];
  for (const name of people) {
    const entity = graphState.entities.find((e) => e.name === name && e.type === "person");
    if (!entity || entity.mentions < 2) continue;
    const posCount = entity.attrs.filter((a) => a === "positive_interaction").length;
    const negCount = entity.attrs.filter((a) => a === "negative_interaction").length;
    const emotionLabel = posCount + negCount < 2 ? "\u6570\u636E\u4E0D\u8DB3" : negCount > posCount * 2 ? "\u660E\u663E\u7126\u8651/\u538B\u529B" : posCount > negCount * 2 ? "\u79EF\u6781/\u5F00\u5FC3" : "\u6DF7\u5408\u60C5\u7EEA";
    const tone = entity.attrs.includes("tone:formal") ? "\u6B63\u5F0F" : entity.attrs.includes("tone:casual") ? "\u8F7B\u677E" : "\u6DF7\u5408";
    const related = _neighborCache.get(name);
    const relatedHint = related && related.size > 0 ? `\uFF0C\u5173\u8054\uFF1A${[...related].slice(0, 3).join("/")}` : "";
    hints.push(`${name}\uFF1A\u63D0\u5230${entity.mentions}\u6B21\uFF0C\u60C5\u7EEA${emotionLabel}\uFF0C\u8BED\u5883${tone}${relatedHint}`);
  }
  if (hints.length === 0) return null;
  return `[\u5173\u7CFB\u56FE\u8C31] ${hints.join("\uFF1B")}`;
}
function _resetSocialGraph() {
  graphState.entities = graphState.entities.filter((e) => e.type !== "person");
}
const CAUSE_TYPES = /* @__PURE__ */ new Set(["caused_by", "depends_on", "learned_from"]);
const EFFECT_TYPES = /* @__PURE__ */ new Set(["triggers", "leads_to"]);
function traceDirection(start, relTypes, direction, maxHops) {
  const visited = /* @__PURE__ */ new Set([start]);
  const results = [];
  let frontier = [start];
  for (let hop = 0; hop < maxHops && frontier.length > 0; hop++) {
    const next = [];
    for (const current of frontier) {
      for (const r of graphState.relations) {
        if (r.invalid_at !== null) continue;
        if (!relTypes.has(r.type)) continue;
        let neighbor = null;
        if (direction === "up" && r.target === current && !visited.has(r.source)) {
          neighbor = r.source;
        } else if (direction === "down" && r.source === current && !visited.has(r.target)) {
          neighbor = r.target;
        }
        if (!neighbor) continue;
        const strength = (r.confidence ?? 0.7) * (r.weight ?? 1) / (hop + 1);
        visited.add(neighbor);
        results.push({ entity: neighbor, type: r.type, strength });
        next.push(neighbor);
      }
    }
    frontier = next;
  }
  return results.sort((a, b) => b.strength - a.strength);
}
function traceCausalChain(startEntities, maxHops = 3) {
  const chains = [];
  for (const start of startEntities.slice(0, 3)) {
    const causes = traceDirection(start, CAUSE_TYPES, "up", maxHops);
    if (causes.length > 0) {
      const causeStr = causes.slice(0, 3).map((c) => `${c.entity}(${c.type},s=${c.strength.toFixed(2)})`).join(" \u2190 ");
      chains.push(`${start} \u7684\u539F\u56E0\uFF1A${causeStr}`);
    }
    const effects = traceDirection(start, EFFECT_TYPES, "down", maxHops);
    if (effects.length > 0) {
      const effectStr = effects.slice(0, 3).map((e) => `${e.entity}(${e.type},s=${e.strength.toFixed(2)})`).join(" \u2192 ");
      chains.push(`${start} \u7684\u5F71\u54CD\uFF1A${effectStr}`);
    }
  }
  return chains;
}
function enrichCausalFromMemories() {
  try {
    const { memoryState } = require("./memory.ts");
    const memories = memoryState?.memories;
    if (!memories) return;
    let added = 0;
    for (const m of memories) {
      if (!m.because || m.scope === "expired") continue;
      const effectEntities = findMentionedEntities(m.content);
      const causeEntities = findMentionedEntities(m.because);
      if (effectEntities.length === 0 || causeEntities.length === 0) continue;
      for (const cause of causeEntities) {
        for (const effect of effectEntities) {
          if (cause === effect) continue;
          const exists = graphState.relations.some(
            (r) => r.source === effect && r.target === cause && r.type === "caused_by" && r.invalid_at === null
          );
          if (!exists) {
            addRelation(effect, cause, "caused_by");
            added++;
          }
        }
      }
      if (added >= 10) break;
    }
    if (added > 0) console.log(`[cc-soul][graph] enriched ${added} causal edges from memory.because`);
  } catch {
  }
}
const graphModule = {
  id: "graph",
  name: "\u77E5\u8BC6\u56FE\u8C31",
  priority: 50,
  init() {
    loadGraph();
  }
};
export {
  _resetSocialGraph,
  addEntitiesFromAnalysis,
  addEntity,
  addRelation,
  computeEntityRanks,
  computePageRank,
  decayActivations,
  detectMentionedPeople,
  enrichCausalFromMemories,
  findMentionedEntities,
  generateEntitySummary,
  getRelatedEntities,
  getSocialContext,
  graphModule,
  graphState,
  graphWalkRecall,
  graphWalkRecallScored,
  invalidateEntity,
  invalidateEntityMemoryIndex,
  invalidateStaleEntities,
  invalidateStaleRelations,
  loadGraph,
  personalizedPageRank,
  queryEntityContext,
  spreadingActivation,
  traceCausalChain,
  updateSocialGraph
};
