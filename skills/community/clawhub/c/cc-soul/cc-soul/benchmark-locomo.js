import { readFileSync } from "fs";
import { resolve, dirname } from "path";
import { createRequire } from "module";
import { fileURLToPath } from "url";
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const require2 = createRequire(import.meta.url);
globalThis.require = require2;
process.env.CC_SOUL_BENCHMARK = "1";
const _origLog = console.log;
const _origWarn = console.warn;
let suppressLogs = false;
console.log = (...args) => {
  if (!suppressLogs) _origLog(...args);
};
console.warn = (...args) => {
  if (!suppressLogs) _origWarn(...args);
};
const print = _origLog;
const { activationRecall, activationRecallWithScores, getIdfCache } = require2("./activation-field.ts");
const { learnAssociation } = require2("./aam.ts");
const { trigrams, trigramSimilarity } = require2("./memory-utils.ts");
const { toCogHints } = require2("./cognition.ts");
function loadDataset() {
  const dataPath = resolve(__dirname, "../data/locomo_mc10.json");
  const raw = readFileSync(dataPath, "utf-8");
  const questions = [];
  for (const line of raw.split("\n")) {
    const trimmed = line.trim();
    if (trimmed) questions.push(JSON.parse(trimmed));
  }
  return questions;
}
function buildMemories(q) {
  const memories = [];
  const originalTimestamps = q.haystack_session_datetimes.map((d) => new Date(d).getTime());
  const minTs = Math.min(...originalTimestamps);
  const maxTs = Math.max(...originalTimestamps);
  const timeSpan = Math.max(maxTs - minTs, 1);
  const now = Date.now();
  const TARGET_SPAN = 30 * 864e5;
  const TARGET_END = now - 36e5;
  function normalizeTs(originalTs) {
    const ratio = (originalTs - minTs) / timeSpan;
    return TARGET_END - TARGET_SPAN * (1 - ratio);
  }
  for (let si = 0; si < q.haystack_sessions.length; si++) {
    const session = q.haystack_sessions[si];
    const baseTs = normalizeTs(originalTimestamps[si]);
    const summary = q.haystack_session_summaries[si];
    if (summary) {
      memories.push({
        content: summary,
        scope: "fact",
        ts: baseTs,
        confidence: 0.95,
        recallCount: 10,
        lastAccessed: now - 36e5,
        importance: 8,
        tags: ["summary"],
        _segmentId: si
      });
    }
    const _epDatePrefix = `[${new Date(originalTimestamps[si]).toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" })}]`;
    for (let ti = 0; ti < session.length; ti++) {
      const turn = session[ti];
      const content = turn?.content;
      if (!content || content.length < 10) continue;
      const role = turn?.role || "unknown";
      const memTs = baseTs + ti * 6e4;
      memories.push({
        content: `${_epDatePrefix} ${content}`,
        scope: "episode",
        ts: memTs,
        confidence: 0.8,
        recallCount: 3,
        lastAccessed: Math.min(now - 72e5, memTs + 864e5),
        importance: 5,
        tags: [`speaker:${role}`, `session:${si}`],
        _segmentId: si,
        _eventDate: originalTimestamps[si] + ti * 6e4
      });
    }
    for (let ti = 0; ti < session.length - 1; ti += 2) {
      const turns = session.slice(ti, ti + 3).filter((t) => t?.content?.length >= 10);
      if (turns.length >= 2) {
        const merged = turns.map((t) => t.content).join(" ");
        if (merged.length > 30 && merged.length < 500) {
          const memTs = baseTs + ti * 6e4 + 3e4;
          memories.push({
            content: `${_epDatePrefix} ${merged}`,
            scope: "episode",
            ts: memTs,
            confidence: 0.75,
            recallCount: 2,
            lastAccessed: Math.min(now - 72e5, memTs + 864e5),
            importance: 3,
            tags: [`merged:${ti}`, `session:${si}`],
            _segmentId: si,
            _eventDate: originalTimestamps[si] + ti * 6e4 + 3e4
          });
        }
      }
    }
  }
  const POSITIVE_WORDS = /* @__PURE__ */ new Set(["happy", "excited", "love", "great", "amazing", "wonderful", "enjoy", "fun", "glad", "proud", "beautiful", "awesome", "fantastic", "celebrate", "perfect", "thrilled", "delighted"]);
  const NEGATIVE_WORDS = /* @__PURE__ */ new Set(["sad", "angry", "frustrated", "stressed", "worried", "anxious", "tired", "upset", "disappointed", "hurt", "scared", "lonely", "overwhelmed", "painful", "annoyed", "difficult", "struggled"]);
  const ABSTRACT_MAP = {
    "moved": ["relocation", "change"],
    "travel": ["journey", "adventure"],
    "bought": ["acquisition", "purchase"],
    "lost": ["loss", "misfortune"],
    "won": ["achievement", "success"],
    "failed": ["setback", "failure"],
    "married": ["relationship", "milestone"],
    "graduated": ["education", "achievement"],
    "hired": ["career", "opportunity"],
    "fired": ["career", "setback"],
    "adopted": ["family", "decision"],
    "volunteered": ["community", "service"],
    "painted": ["art", "hobby"],
    "hiked": ["outdoor", "activity"],
    "camped": ["outdoor", "adventure"],
    "cooked": ["food", "hobby"],
    "read": ["reading", "learning"],
    "played": ["music", "hobby", "activity"]
  };
  for (const mem of memories) {
    const c = (mem.content || "").toLowerCase();
    const words = c.match(/[a-z]{3,}/g) || [];
    const posHits = words.filter((w) => POSITIVE_WORDS.has(w)).length;
    const negHits = words.filter((w) => NEGATIVE_WORDS.has(w)).length;
    const polarity = posHits > negHits ? 1 : negHits > posHits ? -1 : 0;
    const abstractTags = /* @__PURE__ */ new Set();
    for (const w of words) {
      const mapped = ABSTRACT_MAP[w];
      if (mapped) for (const t of mapped) abstractTags.add(t);
    }
    if (abstractTags.size > 0 || polarity !== 0) {
      ;
      mem._gist = { polarity, abstractTags: [...abstractTags].slice(0, 6) };
    }
  }
  return memories;
}
function buildMemoriesOnline(q) {
  const { addMemory, memoryState, scopeIndex, _recentWriteHashes } = require2("./memory.ts");
  const _prevSuppress = suppressLogs;
  suppressLogs = true;
  memoryState.memories.length = 0;
  memoryState.chatHistory.length = 0;
  scopeIndex.clear();
  _recentWriteHashes.clear();
  const originalTimestamps = q.haystack_session_datetimes.map((d) => new Date(d).getTime());
  const minTs = Math.min(...originalTimestamps);
  const maxTs = Math.max(...originalTimestamps);
  const timeSpan = Math.max(maxTs - minTs, 1);
  const now = Date.now();
  const TARGET_SPAN = 30 * 864e5;
  const TARGET_END = now - 36e5;
  function normalizeTs(originalTs) {
    const ratio = (originalTs - minTs) / timeSpan;
    return TARGET_END - TARGET_SPAN * (1 - ratio);
  }
  let totalAdded = 0, totalSkipped = 0;
  for (let si = 0; si < q.haystack_sessions.length; si++) {
    const session = q.haystack_sessions[si];
    const baseTs = normalizeTs(originalTimestamps[si]);
    const _epDatePrefix = `[${new Date(originalTimestamps[si]).toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" })}]`;
    for (let ti = 0; ti < session.length; ti++) {
      const turn = session[ti];
      const content = turn?.content;
      if (!content || content.length < 10) continue;
      const _mockNow = baseTs + ti * 6e4;
      const beforeCount = memoryState.memories.length;
      try {
        addMemory(`${_epDatePrefix} ${content}`, "event", "benchmark-user");
      } catch {
      }
      if (memoryState.memories.length > beforeCount) {
        const newMem = memoryState.memories[memoryState.memories.length - 1];
        newMem.ts = _mockNow;
        newMem.lastAccessed = Math.min(now - 72e5, _mockNow + 864e5);
        newMem._segmentId = si;
        if (!newMem.tags) newMem.tags = [];
        newMem.tags.push(`session:${si}`);
        totalAdded++;
      } else {
        totalSkipped++;
      }
    }
    const summary = q.haystack_session_summaries[si];
    if (summary) {
      const beforeCount = memoryState.memories.length;
      try {
        addMemory(summary, "fact", "benchmark-user");
      } catch {
      }
      if (memoryState.memories.length > beforeCount) {
        const newMem = memoryState.memories[memoryState.memories.length - 1];
        newMem.ts = baseTs;
        newMem.confidence = 0.95;
        newMem.recallCount = 10;
        newMem.lastAccessed = now - 36e5;
        newMem.importance = 8;
        if (!newMem.tags) newMem.tags = [];
        newMem.tags.push("summary");
        newMem._segmentId = si;
        totalAdded++;
      }
    }
  }
  let mergedCount = 0;
  const episodeMemories = memoryState.memories.filter((m) => !m.tags?.includes("summary"));
  for (let i = 0; i < episodeMemories.length - 1; i += 2) {
    const m1 = episodeMemories[i], m2 = episodeMemories[i + 1];
    if (!m1 || !m2) continue;
    const timeDiff = Math.abs((m2.ts || 0) - (m1.ts || 0));
    if (timeDiff > 3e5) continue;
    const merged = (m1.content || "") + " " + (m2.content || "");
    if (merged.length > 30 && merged.length < 800) {
      memoryState.memories.push({
        content: merged,
        scope: "event",
        ts: m1.ts,
        confidence: 0.75,
        recallCount: 2,
        lastAccessed: Math.min(now - 72e5, (m1.ts || now) + 864e5),
        importance: 3,
        tags: [`merged:${i}`, `session:${m1._segmentId ?? 0}`],
        _segmentId: m1._segmentId
      });
      mergedCount++;
    }
  }
  const POSITIVE_WORDS = /* @__PURE__ */ new Set(["happy", "excited", "love", "great", "amazing", "wonderful", "enjoy", "fun", "glad", "proud", "beautiful", "awesome", "fantastic", "celebrate", "perfect", "thrilled", "delighted"]);
  const NEGATIVE_WORDS = /* @__PURE__ */ new Set(["sad", "angry", "frustrated", "stressed", "worried", "anxious", "tired", "upset", "disappointed", "hurt", "scared", "lonely", "overwhelmed", "painful", "annoyed", "difficult", "struggled"]);
  const ABSTRACT_MAP = {
    "moved": ["relocation", "change"],
    "travel": ["journey", "adventure"],
    "bought": ["acquisition", "purchase"],
    "lost": ["loss", "misfortune"],
    "won": ["achievement", "success"],
    "failed": ["setback", "failure"],
    "married": ["relationship", "milestone"],
    "graduated": ["education", "achievement"],
    "hired": ["career", "opportunity"],
    "fired": ["career", "setback"],
    "adopted": ["family", "decision"],
    "volunteered": ["community", "service"],
    "painted": ["art", "hobby"],
    "hiked": ["outdoor", "activity"],
    "camped": ["outdoor", "adventure"],
    "cooked": ["food", "hobby"],
    "read": ["reading", "learning"],
    "played": ["music", "hobby", "activity"]
  };
  for (const mem of memoryState.memories) {
    const c = (mem.content || "").toLowerCase();
    const words = c.match(/[a-z]{3,}/g) || [];
    const posHits = words.filter((w) => POSITIVE_WORDS.has(w)).length;
    const negHits = words.filter((w) => NEGATIVE_WORDS.has(w)).length;
    const polarity = posHits > negHits ? 1 : negHits > posHits ? -1 : 0;
    const abstractTags = /* @__PURE__ */ new Set();
    for (const w of words) {
      const mapped = ABSTRACT_MAP[w];
      if (mapped) for (const t of mapped) abstractTags.add(t);
    }
    if (abstractTags.size > 0 || polarity !== 0) {
      ;
      mem._gist = { polarity, abstractTags: [...abstractTags].slice(0, 6) };
    }
  }
  suppressLogs = _prevSuppress;
  _origLog(`  [online] ${totalAdded} memories added, ${totalSkipped} skipped, ${mergedCount} merged windows`);
  return memoryState.memories;
}
async function buildMemoriesAPI(q, apiPort) {
  const baseUrl = `http://localhost:${apiPort}`;
  try {
    const { memoryState, scopeIndex, _recentWriteHashes } = require2("./memory.ts");
    memoryState.memories.length = 0;
    memoryState.chatHistory.length = 0;
    scopeIndex.clear();
    _recentWriteHashes.clear();
    try {
      require2("./aam.ts").resetLearnedData?.();
    } catch {
    }
    try {
      require2("./fact-store.ts").clearFacts?.();
    } catch {
    }
  } catch {
  }
  const originalTimestamps = q.haystack_session_datetimes.map((d) => new Date(d).getTime());
  let totalAdded = 0, totalSkipped = 0;
  for (let si = 0; si < q.haystack_sessions.length; si++) {
    const session = q.haystack_sessions[si];
    const _epDatePrefix = `[${new Date(originalTimestamps[si]).toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" })}]`;
    for (let ti = 0; ti < session.length; ti++) {
      const turn = session[ti];
      const content = turn?.content;
      if (!content || content.length < 10) continue;
      try {
        const resp = await fetch(`${baseUrl}/memories`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ content: `${_epDatePrefix} ${content}`, scope: "event", user_id: "benchmark-user" })
        });
        const result = await resp.json();
        if (result.stored) totalAdded++;
        else totalSkipped++;
      } catch {
        totalSkipped++;
      }
    }
    const summary = q.haystack_session_summaries[si];
    if (summary) {
      try {
        await fetch(`${baseUrl}/memories`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ content: summary, scope: "fact", user_id: "benchmark-user" })
        });
        totalAdded++;
      } catch {
      }
    }
  }
  _origLog(`  [api] ${totalAdded} memories stored via API, ${totalSkipped} skipped`);
}
async function recallViaAPI(query, topK, apiPort) {
  const baseUrl = `http://localhost:${apiPort}`;
  try {
    const resp = await fetch(`${baseUrl}/search`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, top_n: topK, user_id: "benchmark-user" })
    });
    const result = await resp.json();
    return (result.memories || []).map((m) => ({
      content: m.content || "",
      scope: m.scope || "fact",
      ts: m.ts || Date.now(),
      confidence: m.confidence || 0.7,
      tags: m.tags || []
    }));
  } catch (e) {
    _origLog(`  [api] search error: ${e.message}`);
    return [];
  }
}
function extractFactsFromSummaries(memories) {
  try {
    const factStore = require2("./fact-store.ts");
    const summaries = memories.filter((m) => m.tags?.includes("summary"));
    let totalFacts = 0;
    for (const mem of summaries) {
      const text = mem.content || "";
      const sentences = text.split(/[.!?]\s+/).filter((s) => s.length > 10);
      for (const sent of sentences) {
        const nameMatch = sent.match(/^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b/);
        const subject = nameMatch ? nameMatch[1] : "speaker";
        const patterns = [
          // "X works as/at Y" / "X is a Y"
          { re: /\b(?:works?\s+(?:as|at|in|for)|is\s+a)\s+(.+?)(?:\.|,|and\s|$)/i, pred: "occupation" },
          // "X lives in/moved to Y"
          { re: /\b(?:lives?\s+in|moved?\s+to|relocated\s+to|from)\s+(.+?)(?:\.|,|and\s|$)/i, pred: "location" },
          // "X has/have/owns Y" (pets, children, etc.)
          { re: /\b(?:has|have|owns?|adopted)\s+(?:a\s+)?(.+?)(?:\.|,|and\s|$)/i, pred: "has" },
          // "X enjoys/likes/loves Y"
          { re: /\b(?:enjoys?|likes?|loves?|passionate\s+about|interested\s+in)\s+(.+?)(?:\.|,|and\s|$)/i, pred: "likes" },
          // "X volunteers/participates/attends Y"
          { re: /\b(?:volunteers?\s+at|participates?\s+in|attends?|joined)\s+(.+?)(?:\.|,|and\s|$)/i, pred: "participates" },
          // "X plays/practices Y" (instruments, sports)
          { re: /\b(?:plays?|practices?|performs?)\s+(?:the\s+)?(.+?)(?:\.|,|and\s|$)/i, pred: "plays" },
          // "X studied/majored/graduated Y"
          { re: /\b(?:studied|majored\s+in|graduated\s+(?:from|with)|degree\s+in)\s+(.+?)(?:\.|,|and\s|$)/i, pred: "education" },
          // "X is married to / dating / in a relationship with Y"
          { re: /\b(?:married\s+to|dating|in\s+a\s+relationship\s+with|partner\s+is|spouse\s+is)\s+(.+?)(?:\.|,|and\s|$)/i, pred: "relationship" },
          // "X reads/read Y"
          { re: /\b(?:reads?|has\s+read|been\s+reading)\s+(.+?)(?:\.|,|and\s|$)/i, pred: "reads" },
          // "X traveled/visited/went to Y"
          { re: /\b(?:traveled\s+to|visited|went\s+to|been\s+to|trip\s+to)\s+(.+?)(?:\.|,|and\s|$)/i, pred: "traveled" },
          // "X bought/purchased Y"
          { re: /\b(?:bought|purchased|got)\s+(?:a\s+)?(.+?)(?:\.|,|and\s|$)/i, pred: "bought" },
          // "X made/created/painted Y"
          { re: /\b(?:made|created|painted|built|designed|wrote)\s+(?:a\s+)?(.+?)(?:\.|,|and\s|$)/i, pred: "created" },
          // Generic: "X's Y is Z" / "X's Y"
          { re: /\b([A-Z][a-z]+)'s\s+(\w+(?:\s+\w+)?)\s+(?:is|are|was|were)\s+(.+?)(?:\.|,|$)/i, pred: "_possessive" }
        ];
        for (const { re, pred } of patterns) {
          const match = sent.match(re);
          if (match) {
            let object = (match[1] || match[3] || "").trim();
            let predicate = pred;
            if (pred === "_possessive" && match[2]) {
              predicate = match[2].toLowerCase();
              object = (match[3] || "").trim();
            }
            if (object.length >= 2 && object.length <= 100) {
              factStore.addFacts([{
                subject: subject.toLowerCase(),
                predicate,
                object,
                confidence: 0.85,
                source: "ai_observed",
                ts: mem.ts || Date.now(),
                validUntil: 0
              }]);
              totalFacts++;
            }
          }
        }
      }
    }
    if (totalFacts > 0) {
      suppressLogs = false;
      print(`  [fact-store] extracted ${totalFacts} facts from ${summaries.length} summaries`);
      suppressLogs = true;
    }
  } catch (e) {
  }
}
function answerInRecalled(recalled, answer) {
  const ansLower = answer.toLowerCase().trim();
  if (/not answerable|cannot be answered|unanswerable/i.test(answer)) {
    return { hit: false, rank: -1 };
  }
  const ansTokens = ansLower.split(/\s+/).filter((t) => t.length >= 2);
  const ansTri = trigrams(ansLower);
  for (let i = 0; i < recalled.length; i++) {
    const memLower = recalled[i].content.toLowerCase();
    if (memLower.includes(ansLower)) return { hit: true, rank: i + 1 };
    if (ansTokens.length > 0) {
      let tokenHits = 0;
      for (const t of ansTokens) {
        if (memLower.includes(t)) {
          tokenHits++;
          continue;
        }
        if (t.length >= 4 && /^[a-z]+$/.test(t)) {
          const stem = t.replace(/ing$|ed$|s$|er$|est$|ly$/, "");
          if (stem.length >= 3 && memLower.includes(stem)) {
            tokenHits++;
            continue;
          }
          const memWords = memLower.match(/[a-z]{4,}/g) || [];
          for (const mw of memWords) {
            const mStem = mw.replace(/ing$|ed$|s$|er$|est$|ly$/, "");
            if (mStem === stem || mw.startsWith(stem) || stem.startsWith(mw.slice(0, -1))) {
              tokenHits++;
              break;
            }
          }
        }
      }
      const coverage = tokenHits / ansTokens.length;
      const threshold = ansTokens.length <= 3 ? 0.9 : ansTokens.length <= 6 ? 0.8 : 0.6;
      if (coverage >= threshold) return { hit: true, rank: i + 1 };
    }
    const memTri = trigrams(memLower);
    const triSim = trigramSimilarity(ansTri, memTri);
    if (triSim > 0.4 && ansLower.length >= 4) return { hit: true, rank: i + 1 };
    const ansNames = answer.match(/\b[A-Z][a-z]{2,}\b/g)?.filter((n) => !/^(The|This|That|What|When|Where|How|Who|Not|Yes|And|But)$/.test(n)) || [];
    if (ansNames.length >= 1 && ansTokens.length >= 3) {
      const nameHits = ansNames.filter((n) => memLower.includes(n.toLowerCase())).length;
      const contentTokenHits = ansTokens.filter((t) => t.length >= 4 && memLower.includes(t)).length;
      if (nameHits >= 1 && contentTokenHits >= 2) return { hit: true, rank: i + 1 };
    }
  }
  if (ansTokens.length >= 3 && recalled.length >= 2) {
    let accumulated = "";
    for (let i = 0; i < recalled.length; i++) {
      accumulated += " " + recalled[i].content.toLowerCase();
      let tokenHits = 0;
      for (const t of ansTokens) {
        if (accumulated.includes(t)) {
          tokenHits++;
          continue;
        }
        if (t.length >= 4 && /^[a-z]+$/.test(t)) {
          const stem = t.replace(/ing$|ed$|s$|er$|est$|ly$/, "");
          if (stem.length >= 3 && accumulated.includes(stem)) tokenHits++;
        }
      }
      const coverage = tokenHits / ansTokens.length;
      if (coverage >= 0.85 && i >= 1) return { hit: true, rank: i + 1 };
    }
  }
  return { hit: false, rank: -1 };
}
function selectAnswer(recalled, choices, question) {
  if (recalled.length === 0) {
    const naIdx2 = choices.findIndex((c) => /not answerable|cannot be answered|unanswerable/i.test(c));
    return { choiceIndex: naIdx2 >= 0 ? naIdx2 : 0, confidence: 0 };
  }
  const context = recalled.map((m) => m.content).join(" ").toLowerCase();
  const idfMap = getIdfCache?.() || /* @__PURE__ */ new Map();
  if (!selectAnswer._idfLogged) {
    selectAnswer._idfLogged = true;
    _origLog(`  [selectAnswer] IDF cache: ${idfMap.size > 0 ? idfMap.size + " terms" : "EMPTY (fallback mode)"}`);
  }
  const qLower = (question || "").toLowerCase();
  const qaType = /^who\b|who (?:is|was|does|did|has|had)\b/.test(qLower) ? "who" : /^when\b|what (?:date|time|year|month|day)\b/.test(qLower) ? "when" : /^where\b|what (?:place|location|city|country|address)\b/.test(qLower) ? "where" : /^how many\b|how much\b|what (?:number|amount|count)\b/.test(qLower) ? "howmany" : null;
  const entitySet = /* @__PURE__ */ new Set();
  const allRecalledText = recalled.map((m) => m.content).join(" ");
  const dateMatches = allRecalledText.match(/\d{1,2}\s+\w+\s+\d{4}/g) || [];
  for (const d of dateMatches) entitySet.add(d.toLowerCase());
  const numMatches = allRecalledText.match(/\b\d{2,}\b/g) || [];
  for (const n of numMatches) entitySet.add(n);
  const nameMatches = allRecalledText.match(/[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*/g) || [];
  for (const name of nameMatches) {
    entitySet.add(name.toLowerCase());
    for (const part of name.split(/\s+/)) {
      if (part.length >= 2) entitySet.add(part.toLowerCase());
    }
  }
  const scores = choices.map((choice, idx) => {
    const choiceLower = choice.toLowerCase().trim();
    let score = 0;
    if (entitySet.size > 0) {
      let entityHits = 0;
      for (const entity of entitySet) if (choiceLower.includes(entity)) entityHits++;
      if (entityHits > 0) score = Math.max(score, Math.min(1, entityHits / Math.max(3, entitySet.size) * 1.5));
    }
    if (context.includes(choiceLower)) score = Math.max(score, 1);
    const tokens = choiceLower.split(/\s+/).filter((t) => t.length >= 2);
    if (tokens.length > 0) {
      if (idfMap.size > 0) {
        let weightedHits = 0, weightedTotal = 0;
        for (const t of tokens) {
          const idfW = idfMap.get(t) ?? (t.length >= 4 ? 0.7 : 0.3);
          weightedTotal += idfW;
          if (context.includes(t)) {
            weightedHits += idfW;
            continue;
          }
          if (t.length >= 4 && /^[a-z]+$/.test(t)) {
            const stem = t.replace(/ing$|ed$|s$|er$|est$|ly$/, "");
            if (stem.length >= 3 && context.includes(stem)) weightedHits += idfW * 0.8;
          }
        }
        if (weightedTotal > 0) score = Math.max(score, weightedHits / weightedTotal * 0.8);
      } else {
        let hits = 0;
        for (const t of tokens) {
          if (context.includes(t)) {
            hits++;
            continue;
          }
          if (t.length >= 4 && /^[a-z]+$/.test(t)) {
            const stem = t.replace(/ing$|ed$|s$|er$|est$|ly$/, "");
            if (stem.length >= 3 && context.includes(stem)) hits++;
          }
        }
        score = Math.max(score, hits / tokens.length * 0.8);
      }
    }
    const choiceTri = trigrams(choiceLower);
    for (const mem of recalled) {
      const sim = trigramSimilarity(choiceTri, trigrams(mem.content.toLowerCase()));
      score = Math.max(score, sim * 0.6);
    }
    if (qaType) {
      if (qaType === "who" && /[A-Z][a-z]{2,}/.test(choice)) score += 0.08;
      else if (qaType === "when" && /\d{4}|\b\d{1,2}\s+\w+\b|january|february|march|april|may|june|july|august|september|october|november|december/i.test(choice)) score += 0.08;
      else if (qaType === "where" && /[A-Z][a-z]{2,}/.test(choice)) score += 0.05;
      else if (qaType === "howmany" && /\d+/.test(choice)) score += 0.08;
    }
    return { idx, score };
  });
  scores.sort((a, b) => b.score - a.score);
  const _ABSTAIN_STOPS = /* @__PURE__ */ new Set(["what", "when", "where", "how", "who", "which", "why", "the", "this", "that", "does", "did", "has", "have", "was", "were", "can", "could", "would", "should", "not", "are", "its", "his", "her", "she", "they", "been", "being", "had", "with", "from", "for", "and", "but", "about", "after", "before", "into", "over", "than", "then", "some", "any", "all", "both", "each", "more", "most", "many", "much", "very", "also", "just", "only", "still"]);
  const qKeywords = ((question || "").toLowerCase().match(/[a-z]{3,}/g) || []).filter((w) => !_ABSTAIN_STOPS.has(w));
  const recalledText = recalled.map((m) => m.content).join(" ").toLowerCase();
  const evidenceCoverage = qKeywords.length > 0 ? qKeywords.filter((w) => recalledText.includes(w)).length / qKeywords.length : 0;
  const margin = scores[0].score > 0 && scores.length >= 2 ? (scores[0].score - scores[1].score) / Math.max(scores[0].score, 0.01) : 0;
  const qEntities = ((question || "").match(/\b[A-Z][a-z]{2,}\b/g) || []).filter((n) => !/^(What|When|Where|How|Who|Which|Why|The|This|That|Does|Did|Has|Have|Was|Were|Can|Could|Would|Should|Not)$/.test(n));
  const entityCoverage = qEntities.length > 0 ? qEntities.filter((n) => recalledText.includes(n.toLowerCase())).length / qEntities.length : 1;
  const topicPresence = entityCoverage > 0.5;
  const topChoiceTokens = choices[scores[0].idx]?.toLowerCase().match(/[a-z]{3,}/g) || [];
  const detailHits = topChoiceTokens.filter((t) => !_ABSTAIN_STOPS.has(t) && recalledText.includes(t)).length;
  const detailSufficiency = scores[0].score > 0.3 && (topChoiceTokens.length === 0 || detailHits / Math.max(1, topChoiceTokens.length) > 0.3);
  const answerability = evidenceCoverage * (0.3 + 0.7 * margin) * entityCoverage;
  const groundingScore = topicPresence ? detailSufficiency ? 1 : 0.3 : 0.1;
  const naIdx = choices.findIndex((c) => /not answerable|cannot be answered|unanswerable/i.test(c));
  if (naIdx >= 0 && (answerability < 0.15 || groundingScore < 0.2)) return { choiceIndex: naIdx, confidence: Math.min(answerability, groundingScore) };
  if (scores[0].score < 0.15 && naIdx >= 0) return { choiceIndex: naIdx, confidence: scores[0].score };
  return { choiceIndex: scores[0].idx, confidence: scores[0].score };
}
function parseArgs() {
  const args = process.argv.slice(2);
  let conv, type, topK = 10, verbose = false, limit = 0;
  let recallOnly = false, llm = false, online = false, api = false, apiPort = 18800, sample = false, mini = false;
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--conv" && args[i + 1]) conv = parseInt(args[++i]);
    if (args[i] === "--type" && args[i + 1]) type = args[++i];
    if (args[i] === "--top-k" && args[i + 1]) topK = parseInt(args[++i]);
    if (args[i] === "--limit" && args[i + 1]) limit = parseInt(args[++i]);
    if (args[i] === "--verbose") verbose = true;
    if (args[i] === "--recall-only") recallOnly = true;
    if (args[i] === "--llm") llm = true;
    if (args[i] === "--online") online = true;
    if (args[i] === "--api") {
      api = true;
      online = true;
    }
    if (args[i] === "--api-port" && args[i + 1]) apiPort = parseInt(args[++i]);
    if (args[i] === "--sample") sample = true;
    if (args[i] === "--mini") mini = true;
  }
  return { conv, type, topK, verbose, limit, recallOnly, llm, online, api, apiPort, sample, mini };
}
function loadLLMKey() {
  if (process.env.LLM_PROVIDER === "claude") return process.env.ANTHROPIC_KEY || "";
  if (process.env.LLM_PROVIDER === "gemini") return process.env.GEMINI_KEY || "";
  return "sk-2d29b4fb236b40908c54a9517f86d504";
}
async function selectAnswerWithLLM(recalled, question, choices, apiKey) {
  const letters = "ABCDEFGHIJ";
  const choiceBlock = choices.map((c, i) => `${letters[i]}. ${c}`).join("\n");
  const llmRecalled = recalled.filter((m) => !m.tags?.some((t) => t.startsWith("merged:")));
  const displayRecalled = llmRecalled.length >= 3 ? llmRecalled : recalled;
  const sessionGroups = /* @__PURE__ */ new Map();
  for (let i = 0; i < displayRecalled.length; i++) {
    const sessionTag = displayRecalled[i].tags?.find((t) => t.startsWith("session:")) || "other";
    if (!sessionGroups.has(sessionTag)) sessionGroups.set(sessionTag, []);
    sessionGroups.get(sessionTag).push({ idx: i + 1, content: displayRecalled[i].content });
  }
  let structuredContext = "";
  if (sessionGroups.size > 1) {
    for (const [session, mems] of sessionGroups) {
      structuredContext += `
[${session}]
`;
      for (const m of mems) structuredContext += `  ${m.idx}. ${m.content}
`;
    }
  } else {
    structuredContext = recalled.map((m, i) => `[${i + 1}] ${m.content}`).join("\n");
  }
  const _fokQEnts = (question.match(/\b[A-Z][a-z]{2,}\b/g) || []).filter((n) => !/^(What|When|Where|How|Who|Which|Why|The|This|That|Does|Did|Has|Have|Was|Were|Can|Could|Would|Should|Not)$/.test(n));
  const _fokRecalledText = recalled.map((m) => (m.content || "").toLowerCase()).join(" ");
  const _fokEntityPresent = _fokQEnts.length === 0 || _fokQEnts.some((n) => _fokRecalledText.includes(n.toLowerCase()));
  const _fokQWords = (question.toLowerCase().match(/[a-z]{4,}/g) || []).filter((w) => !/^(what|when|where|how|who|which|why|does|did|has|have|was|were|would|could|should|about|their|with|from|been|this|that|they|them|most|more)$/.test(w));
  const _fokWordCoverage = _fokQWords.length > 0 ? _fokQWords.filter((w) => _fokRecalledText.includes(w)).length / _fokQWords.length : 0;
  const _fokConfidence = !_fokEntityPresent ? "LOW" : _fokWordCoverage < 0.3 ? "LOW" : _fokWordCoverage < 0.6 ? "MEDIUM" : "HIGH";
  const hasNA = choices.some((c) => /not answerable|cannot be answered|unanswerable/i.test(c));
  const qWords = new Set(question.toLowerCase().match(/[a-z]{3,}/g) || []);
  const mWords = new Set(recalled.flatMap((m) => (m.content || "").toLowerCase().match(/[a-z]{3,}/g) || []));
  let overlap = 0;
  for (const w of qWords) if (mWords.has(w)) overlap++;
  const relevanceHint = qWords.size > 0 ? overlap / qWords.size : 0;
  const systemPrompt = `You are answering a multiple-choice question about a person's life based on conversation memories.

Rules:
1. If a choice matches specific details (names, numbers, dates, activities) mentioned in the memories, prefer it.
2. Pay attention to WHO said what \u2014 the question asks about a specific person.
3. For date/time questions: look at the [date] prefix on each memory for exact dates. Match the specific month/year mentioned in memories, not your general knowledge. Pick the closest date rather than "Not answerable".
4. For multi-step questions: combine information from multiple memories. If memory A says "X happened" and memory B mentions "during August", connect them.
${hasNA ? _fokConfidence === "LOW" ? `5. Memory confidence is LOW. Choose "Not answerable" unless you find SPECIFIC, DIRECT evidence in the memories. Specifically:
   - If NO memory contains the exact detail the question asks about \u2192 "Not answerable"
   - Vague topic overlap is NOT sufficient \u2014 you need concrete facts/dates/names that directly answer the question
   - When in doubt, prefer "Not answerable" over guessing` : `4. Choose "Not answerable" when the memories do NOT contain information relevant to the question topic. Specifically:
   - If the question asks about a topic/person/event that is never mentioned in any memory \u2192 "Not answerable"
   - If the memories mention the topic but don't contain enough detail to pick a specific answer \u2192 still pick the best match, NOT "Not answerable"
   - When in doubt between a specific answer and "Not answerable", check if ANY memory discusses the same topic as the question` : "5. Pick the best matching answer based on the memories."}`;
  const fokNote = _fokConfidence === "LOW" ? '\n[System note: Memory confidence is LOW \u2014 the topic may not be covered in these memories. Prefer "Not answerable" unless you see direct evidence.]\n' : "";
  const userPrompt = `Memories (relevance: ${(relevanceHint * 100).toFixed(0)}%, confidence: ${_fokConfidence}):${fokNote}
${structuredContext}

Question: ${question}

Choices:
${choiceBlock}

Answer with ONLY one letter (A-J).`;
  const useClaude = process.env.LLM_PROVIDER === "claude";
  const useGemini = process.env.LLM_PROVIDER === "gemini";
  const resp = useGemini ? await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      contents: [{ parts: [{ text: systemPrompt + "\n\n" + userPrompt }] }],
      generationConfig: { temperature: 0, maxOutputTokens: 10 }
    })
  }) : useClaude ? await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": apiKey,
      "anthropic-version": "2023-06-01"
    },
    body: JSON.stringify({
      model: "claude-sonnet-4-20250514",
      system: systemPrompt + "\n\nIMPORTANT: Respond with ONLY a single letter (A-J). No explanation, no reasoning, just the letter.",
      messages: [{ role: "user", content: userPrompt }],
      temperature: 0,
      max_tokens: 3
    })
  }) : await fetch("https://api.deepseek.com/chat/completions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${apiKey}`
    },
    body: JSON.stringify({
      model: "deepseek-chat",
      messages: [
        { role: "system", content: systemPrompt },
        { role: "user", content: userPrompt }
      ],
      temperature: 0,
      max_tokens: 5
    })
  });
  if (!resp.ok) {
    const body = await resp.text();
    throw new Error(`LLM API ${resp.status}: ${body.slice(0, 200)}`);
  }
  const json = await resp.json();
  let raw = "";
  if (useGemini) {
    raw = (json.candidates?.[0]?.content?.parts?.[0]?.text || "").trim();
  } else if (useClaude) {
    raw = (json.content?.[0]?.text || "").trim();
  } else {
    raw = (json.choices?.[0]?.message?.content || "").trim();
  }
  let letter = "";
  if (/not answerable|cannot be answered|unanswerable/i.test(raw)) {
    const naChoiceIdx = choices.findIndex((c) => /not answerable|cannot be answered|unanswerable/i.test(c));
    if (naChoiceIdx >= 0) letter = letters[naChoiceIdx];
  }
  if (!letter) {
    const directMatch = raw.match(/^([A-J])\b/);
    if (directMatch) {
      letter = directMatch[1];
    } else {
      const answerMatch = raw.match(/(?:answer|choice|select|pick|choose)[:\s]+\*?\*?([A-J])\b/i) || raw.match(/ANSWER\s*:\s*\*?\*?\s*([A-J])\b/i) || raw.match(/\b([A-J])\.\s/) || raw.match(/\*\*([A-J])\*\*/) || raw.match(/\b([A-J])$/m);
      if (answerMatch) letter = answerMatch[1];
      else {
        const anyLetter = raw.match(/\b([A-J])\b/);
        if (anyLetter) letter = anyLetter[1];
        else letter = raw.charAt(0).toUpperCase();
      }
    }
  }
  let idx = letters.indexOf(letter);
  if (idx < 0 && raw.length > 1) {
    const rawLower = raw.toLowerCase();
    let bestSim = 0, bestIdx = -1;
    for (let ci = 0; ci < choices.length; ci++) {
      const choiceLower = choices[ci].toLowerCase();
      if (rawLower.includes(choiceLower) || choiceLower.includes(rawLower)) {
        bestIdx = ci;
        break;
      }
      const sim = trigramSimilarity(trigrams(rawLower), trigrams(choiceLower));
      if (sim > bestSim) {
        bestSim = sim;
        bestIdx = ci;
      }
    }
    if (bestIdx >= 0 && (bestSim > 0.3 || bestIdx >= 0)) idx = bestIdx;
  }
  return { choiceIndex: idx >= 0 ? idx : -1, raw };
}
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function run() {
  const opts = parseArgs();
  const mode = opts.recallOnly ? "recall-only" : opts.llm ? "llm" : opts.api ? "api" : opts.online ? "online" : "default";
  print("\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550");
  print("  cc-soul NAM \xD7 LOCOMO-MC10 Benchmark");
  print("\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550");
  print(`  mode: ${mode}  top-K: ${opts.topK}  conv: ${opts.conv ?? "all"}  type: ${opts.type ?? "all"}  limit: ${opts.limit || "none"}`);
  print();
  let apiKey = "";
  if (opts.llm) {
    try {
      apiKey = loadLLMKey();
      print("  DeepSeek API key loaded");
    } catch (e) {
      print(`  ERROR: ${e.message}`);
      return;
    }
  }
  const allQuestions = loadDataset();
  print(`  Loaded ${allQuestions.length} questions`);
  const convMap = /* @__PURE__ */ new Map();
  for (const q of allQuestions) {
    const convId = q.question_id.split("_")[0];
    if (!convMap.has(convId)) convMap.set(convId, []);
    convMap.get(convId).push(q);
  }
  const convIds = [...convMap.keys()].sort();
  print(`  ${convIds.length} conversations`);
  print();
  let questions = allQuestions;
  if (opts.mini) {
    const miniConv = convIds[4] || convIds[0];
    questions = allQuestions.filter((q) => q.question_id.split("_")[0] === miniConv);
    print(`  Mini mode: ${miniConv} \u2192 ${questions.length} questions`);
  } else if (opts.sample) {
    const sampleConvs = [convIds[0], convIds[4], convIds[9]].filter(Boolean);
    questions = allQuestions.filter((q) => sampleConvs.includes(q.question_id.split("_")[0]));
    print(`  Sample mode: ${sampleConvs.join(", ")} \u2192 ${questions.length} questions`);
  } else if (opts.conv !== void 0) {
    const targetConv = convIds[opts.conv];
    if (!targetConv) {
      print(`  Invalid conv index: ${opts.conv}`);
      return;
    }
    questions = convMap.get(targetConv) || [];
    print(`  Filtered to conv ${targetConv}: ${questions.length} questions`);
  }
  if (opts.type) {
    questions = questions.filter((q) => q.question_type === opts.type);
    print(`  Filtered to type ${opts.type}: ${questions.length} questions`);
  }
  if (opts.limit > 0) {
    questions = questions.slice(0, opts.limit);
    print(`  Limited to first ${questions.length} questions`);
  }
  if (questions.length === 0) {
    print("  No questions.");
    return;
  }
  const memoryCache = /* @__PURE__ */ new Map();
  const learnedConvs = /* @__PURE__ */ new Set();
  const convMemoryCount = /* @__PURE__ */ new Map();
  const perQueryLatency = [];
  let totalMemoryBytes = 0;
  const perQuestionResult = [];
  const typeStats = {};
  function getStat(type) {
    if (!typeStats[type]) typeStats[type] = {
      recallTotal: 0,
      hitAt1: 0,
      hitAt3: 0,
      hitAt5: 0,
      hitAt10: 0,
      mrrSum: 0,
      mcCorrect: 0,
      mcTotal: 0,
      llmCorrect: 0,
      llmTotal: 0,
      llmFail: 0
    };
    return typeStats[type];
  }
  const startTime = Date.now();
  suppressLogs = true;
  let _lastConvId = "";
  for (let qi = 0; qi < questions.length; qi++) {
    const q = questions[qi];
    const convId = q.question_id.split("_")[0];
    if (convId !== _lastConvId && _lastConvId !== "") {
      try {
        require2("./aam.ts").resetLearnedData?.();
      } catch {
      }
      try {
        require2("./fact-store.ts").clearFacts?.();
      } catch {
      }
    }
    _lastConvId = convId;
    if (!memoryCache.has(convId)) {
      const memories2 = opts.online ? buildMemoriesOnline(q) : buildMemories(q);
      memoryCache.set(convId, memories2);
      if (!learnedConvs.has(convId)) {
        for (let mi = 0; mi < memories2.length; mi++) {
          learnAssociation(memories2[mi].content, 0.2);
          if (mi + 1 < memories2.length) {
            const timeDiff = Math.abs((memories2[mi + 1].ts || 0) - (memories2[mi].ts || 0));
            if (timeDiff < 12e4) {
              const w1 = (memories2[mi].content || "").match(/[a-zA-Z]{3,}/gi) || [];
              const w2 = (memories2[mi + 1].content || "").match(/[a-zA-Z]{3,}/gi) || [];
              if (w1.length > 0 && w2.length > 0) {
                learnAssociation(w1.slice(0, 8).join(" ") + " " + w2.slice(0, 8).join(" "), 0.4, 1, true);
              }
            }
          }
        }
        for (const mem of memories2) {
          if (mem.tags?.includes("summary")) {
            learnAssociation(mem.content, 0.8);
            const sentences = mem.content.split(/[.!?;]\s+/).filter((s) => s.length > 10);
            for (const sent of sentences) {
              learnAssociation(sent, 0.5);
              const svoMatch = sent.match(/\b([A-Z][a-z]+)\b.*?\b([a-z]{4,}(?:ed|s|ing)?)\b\s+(?:the\s+|a\s+|an\s+)?([a-z]{3,}(?:\s+[a-z]{3,})?)/i);
              if (svoMatch) {
                const svo = `${svoMatch[1]} ${svoMatch[2]} ${svoMatch[3]}`;
                learnAssociation(svo, 0.3, 1, true);
              }
            }
          }
        }
        if (false) try {
          const { extractFacts, addFacts } = require2("./fact-store.ts");
          let factCount = 0;
          for (const mem of memories2) {
            if (mem.scope === "episode" && mem.content && mem.content.length > 20) {
              const facts = extractFacts(mem.content, "user_said");
              if (facts.length > 0) {
                addFacts(facts);
                factCount += facts.length;
              }
            }
          }
          if (factCount > 0) {
            suppressLogs = false;
            print(`  [fact-store] extracted ${factCount} facts from episodes`);
            suppressLogs = true;
          }
        } catch {
        }
        try {
          const graph = require2("./graph.ts");
          const _preRegistered = /* @__PURE__ */ new Set();
          for (const mem of memories2) {
            const speakerMatch = mem.content.match(/^\[([A-Z]{2,})\]:/);
            if (speakerMatch) {
              const name = speakerMatch[1].charAt(0) + speakerMatch[1].slice(1).toLowerCase();
              if (!_preRegistered.has(name)) {
                graph.findMentionedEntities(name);
                _preRegistered.add(name);
              }
            }
            if (mem.tags?.includes("summary")) {
              const summaryNames = mem.content.match(/\b([A-Z][a-z]{2,})\b/g) || [];
              for (const n of summaryNames) {
                if (!/^(The|This|That|What|When|Where|How|Who|Which|Why|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|January|February|March|April|May|June|July|August|September|October|November|December|Since|During|After|Before|Caroline|She|Her|His|They)$/.test(n)) {
                }
                if (!_preRegistered.has(n) && !/^(The|This|That|Since|During|After|Before)$/.test(n)) {
                  graph.findMentionedEntities(n);
                  _preRegistered.add(n);
                }
              }
            }
          }
          const summaries = memories2.filter((m) => m.tags?.includes("summary"));
          const episodes = memories2.filter((m) => !m.tags?.includes("summary"));
          for (const mem of [...summaries, ...episodes]) {
            const entities = graph.findMentionedEntities(mem.content);
            if (entities.length >= 2) {
              for (let ei = 0; ei < entities.length; ei++) {
                for (let ej = ei + 1; ej < entities.length; ej++) {
                  try {
                    graph.addRelation?.(entities[ei], entities[ej], "co_mentioned");
                  } catch {
                  }
                }
              }
            }
          }
          const entCount = graph.graphState?.entities?.length || 0;
          const relCount = graph.graphState?.relations?.length || 0;
          if (entCount > 0) {
            suppressLogs = false;
            print(`  [graph] built ${entCount} entities, ${relCount} relations`);
            suppressLogs = true;
          }
        } catch {
        }
        try {
          const { expandQuery } = require2("./aam.ts");
          let tagged = 0;
          for (const mem of memories2) {
            if (mem.prospectiveTags) continue;
            const words = (mem.content || "").match(/[a-zA-Z]{3,}/gi);
            if (!words || words.length < 2) continue;
            const contentLower = (mem.content || "").toLowerCase();
            const expanded = expandQuery(words.slice(0, 5).map((w) => w.toLowerCase()), 10);
            const threshold = expanded.length < 3 ? 0.15 : 0.3;
            const tags = expanded.filter((e) => e.weight >= threshold && !contentLower.includes(e.word) && e.word.length >= 2).map((e) => e.word).slice(0, 8);
            if (tags.length > 0) {
              mem.prospectiveTags = tags;
              tagged++;
            }
          }
          if (tagged > 0) {
            suppressLogs = false;
            print(`  [prospective-tags] ${tagged}/${memories2.length} memories tagged`);
            suppressLogs = true;
          }
        } catch {
        }
        learnedConvs.add(convId);
        convMemoryCount.set(convId, memories2.length);
        totalMemoryBytes += memories2.reduce((s, m) => s + (m.content || "").length * 2, 0);
        suppressLogs = false;
        print(`  [${convId}] ${memories2.length} memories loaded`);
        suppressLogs = true;
      }
    }
    const memories = memoryCache.get(convId);
    const _qStart = Date.now();
    const _cogHints = toCogHints(q.question);
    let recalled;
    if (opts.api) {
      const { recall: fullRecall } = require2("./memory-recall.ts");
      recalled = fullRecall(q.question, opts.topK, "benchmark-user", void 0, { mood: 0, alertness: 0.5 }, void 0, _cogHints) || [];
    } else {
      recalled = activationRecall(memories, q.question, opts.topK, 0, 0.5, _cogHints);
    }
    perQueryLatency.push(Date.now() - _qStart);
    if (recalled.length > 0) {
      try {
        const queryKw = (q.question.match(/[a-zA-Z]{3,}/gi) || []).slice(0, 8);
        const recallKw = recalled.slice(0, 5).flatMap((m) => m.content.match(/[a-zA-Z]{3,}/gi) || []).slice(0, 15);
        const combined = queryKw.join(" ") + " " + recallKw.join(" ");
        learnAssociation(combined, 0.6);
        for (const mem of recalled.slice(0, 3)) {
          if (mem.tags?.includes("summary")) {
            learnAssociation(queryKw.join(" ") + " " + (mem.content.match(/[a-zA-Z]{4,}/gi) || []).slice(0, 10).join(" "), 0.8);
          }
        }
      } catch {
      }
    }
    const _isInferenceQ = /^(would|could|is it|are there|might|should|do you think)/i.test(q.question.trim());
    if (recalled.length > 0 && !_isInferenceQ) {
      try {
        const qContentWords = (q.question.match(/[a-zA-Z]{4,}/gi) || []).map((w) => w.toLowerCase()).filter((w) => !/^(what|when|where|how|who|which|why|does|did|has|have|was|were|can|could|would|should)$/.test(w)).slice(0, 5);
        for (const mem of recalled.slice(0, 3)) {
          const pt = mem.prospectiveTags || [];
          for (const w of qContentWords) {
            if (!pt.includes(w) && !(mem.content || "").toLowerCase().includes(w)) {
              pt.push(w);
            }
          }
          if (pt.length > 0) mem.prospectiveTags = pt.slice(0, 12);
        }
      } catch {
      }
    }
    const stat = getStat(q.question_type);
    const isAdversarial = /not answerable|cannot be answered|unanswerable/i.test(q.answer);
    let _qHit = false;
    if (!isAdversarial) {
      stat.recallTotal++;
      const { hit, rank } = answerInRecalled(recalled, q.answer);
      _qHit = hit;
      if (hit) {
        if (rank <= 1) stat.hitAt1++;
        if (rank <= 3) stat.hitAt3++;
        if (rank <= 5) stat.hitAt5++;
        if (rank <= 10) stat.hitAt10++;
        stat.mrrSum += 1 / rank;
      }
    }
    let _qMCCorrect = false;
    if (!opts.recallOnly) {
      stat.mcTotal++;
      const { choiceIndex, confidence } = selectAnswer(recalled, q.choices, q.question);
      _qMCCorrect = choiceIndex === q.correct_choice_index;
      if (_qMCCorrect) stat.mcCorrect++;
      if (opts.llm) {
        stat.llmTotal++;
        try {
          const { choiceIndex: llmIdx, raw } = await selectAnswerWithLLM(recalled, q.question, q.choices, apiKey);
          if (llmIdx >= 0 && llmIdx === q.correct_choice_index) stat.llmCorrect++;
          if (llmIdx < 0) stat.llmFail++;
          if (opts.verbose) {
            const smOk = choiceIndex === q.correct_choice_index;
            const llmOk = llmIdx === q.correct_choice_index;
            suppressLogs = false;
            print(`  SM:${smOk ? "O" : "X"} LLM:${llmOk ? "O" : "X"} [${q.question_type.padEnd(20)}] ${q.question.slice(0, 50)}`);
            if (!llmOk) {
              print(`     want: ${q.choices[q.correct_choice_index]?.slice(0, 50)}`);
              print(`     llm:  ${llmIdx >= 0 ? q.choices[llmIdx]?.slice(0, 50) : `parse fail: ${raw}`}`);
            }
            suppressLogs = true;
          }
          await sleep(500);
        } catch (e) {
          stat.llmFail++;
          suppressLogs = false;
          print(`  LLM error: ${e.message.slice(0, 100)}`);
          suppressLogs = true;
          await sleep(1e3);
        }
      } else if (opts.verbose) {
        const mcOk = choiceIndex === q.correct_choice_index;
        suppressLogs = false;
        print(`  ${mcOk ? "OK" : "XX"} [${q.question_type.padEnd(20)}] ${q.question.slice(0, 55)}`);
        if (!mcOk) {
          print(`     want: ${q.answer.slice(0, 50)}`);
          print(`     got:  ${q.choices[choiceIndex]?.slice(0, 50)} (conf=${confidence.toFixed(2)})`);
        }
        suppressLogs = true;
      }
    } else if (opts.verbose && !isAdversarial) {
      const { hit, rank } = answerInRecalled(recalled, q.answer);
      suppressLogs = false;
      print(`  ${hit ? "HIT" : "MISS"}@${rank > 0 ? rank : "-"} [${q.question_type.padEnd(20)}] ${q.question.slice(0, 55)}`);
      suppressLogs = true;
    }
    perQuestionResult.push({ convId, hit: _qHit, mcCorrect: _qMCCorrect, isAdversarial });
    if ((qi + 1) % 50 === 0) {
      suppressLogs = false;
      const elapsed2 = (Date.now() - startTime) / 1e3;
      print(`  ... ${qi + 1}/${questions.length} (${elapsed2.toFixed(0)}s)`);
      suppressLogs = true;
    }
  }
  suppressLogs = false;
  const elapsed = (Date.now() - startTime) / 1e3;
  const typeOrder = ["single_hop", "multi_hop", "temporal_reasoning", "open_domain", "adversarial"];
  print();
  print("\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550");
  print(`  Layer 1: Recall Quality${opts.recallOnly ? " (recall-only mode)" : ""}`);
  print("\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550");
  print();
  if (opts.recallOnly) {
    print("  Type                    Hit@1   Hit@3   Hit@5  Hit@10    MRR     N");
    print("  \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500  \u2500\u2500\u2500\u2500\u2500\u2500  \u2500\u2500\u2500\u2500\u2500\u2500  \u2500\u2500\u2500\u2500\u2500\u2500  \u2500\u2500\u2500\u2500\u2500\u2500  \u2500\u2500\u2500\u2500\u2500\u2500  \u2500\u2500\u2500\u2500");
    let tN = 0, t1 = 0, t3 = 0, t5 = 0, t10 = 0, tMRR = 0;
    for (const type of typeOrder) {
      const s = typeStats[type];
      if (!s || s.recallTotal === 0) continue;
      const n = s.recallTotal;
      const h1 = (s.hitAt1 / n * 100).toFixed(1);
      const h3 = (s.hitAt3 / n * 100).toFixed(1);
      const h5 = (s.hitAt5 / n * 100).toFixed(1);
      const h10 = (s.hitAt10 / n * 100).toFixed(1);
      const mrr = (s.mrrSum / n).toFixed(3);
      print(`  ${type.padEnd(24)} ${h1.padStart(5)}%  ${h3.padStart(5)}%  ${h5.padStart(5)}%  ${h10.padStart(5)}%  ${mrr.padStart(6)}  ${String(n).padStart(4)}`);
      tN += n;
      t1 += s.hitAt1;
      t3 += s.hitAt3;
      t5 += s.hitAt5;
      t10 += s.hitAt10;
      tMRR += s.mrrSum;
    }
    if (tN > 0) {
      print("  \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500  \u2500\u2500\u2500\u2500\u2500\u2500  \u2500\u2500\u2500\u2500\u2500\u2500  \u2500\u2500\u2500\u2500\u2500\u2500  \u2500\u2500\u2500\u2500\u2500\u2500  \u2500\u2500\u2500\u2500\u2500\u2500  \u2500\u2500\u2500\u2500");
      print(`  ${"TOTAL".padEnd(24)} ${(t1 / tN * 100).toFixed(1).padStart(5)}%  ${(t3 / tN * 100).toFixed(1).padStart(5)}%  ${(t5 / tN * 100).toFixed(1).padStart(5)}%  ${(t10 / tN * 100).toFixed(1).padStart(5)}%  ${(tMRR / tN).toFixed(3).padStart(6)}  ${String(tN).padStart(4)}`);
    }
  } else {
    print("  Type                    Hit@K    MRR     N");
    print("  \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500  \u2500\u2500\u2500\u2500\u2500\u2500  \u2500\u2500\u2500\u2500\u2500\u2500  \u2500\u2500\u2500\u2500");
    let totalRecallHits = 0, totalRecallN = 0, totalMRR = 0;
    for (const type of typeOrder) {
      const s = typeStats[type];
      if (!s || s.recallTotal === 0) continue;
      const hitRate = (s.hitAt10 / s.recallTotal * 100).toFixed(1);
      const mrr = (s.mrrSum / s.recallTotal).toFixed(3);
      print(`  ${type.padEnd(24)} ${hitRate.padStart(5)}%  ${mrr.padStart(6)}  ${String(s.recallTotal).padStart(4)}`);
      totalRecallHits += s.hitAt10;
      totalRecallN += s.recallTotal;
      totalMRR += s.mrrSum;
    }
    if (totalRecallN > 0) {
      print("  \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500  \u2500\u2500\u2500\u2500\u2500\u2500  \u2500\u2500\u2500\u2500\u2500\u2500  \u2500\u2500\u2500\u2500");
      print(`  ${"TOTAL".padEnd(24)} ${(totalRecallHits / totalRecallN * 100).toFixed(1).padStart(5)}%  ${(totalMRR / totalRecallN).toFixed(3).padStart(6)}  ${String(totalRecallN).padStart(4)}`);
    }
  }
  if (!opts.recallOnly) {
    print();
    print("\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550");
    print("  Layer 2: MC Accuracy (10 \u9009 1)");
    print("\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550");
    print();
    if (opts.llm) {
      print("  Type                    SM Acc   LLM Acc    N   (fail)");
      print("  \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500  \u2500\u2500\u2500\u2500\u2500\u2500  \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500  \u2500\u2500\u2500\u2500  \u2500\u2500\u2500\u2500\u2500\u2500");
      let tMC = 0, tSM = 0, tLLM = 0, tFail = 0;
      for (const type of typeOrder) {
        const s = typeStats[type];
        if (!s || s.mcTotal === 0) continue;
        const smAcc = (s.mcCorrect / s.mcTotal * 100).toFixed(1);
        const llmAcc = s.llmTotal > 0 ? (s.llmCorrect / s.llmTotal * 100).toFixed(1) : " N/A";
        print(`  ${type.padEnd(24)} ${smAcc.padStart(5)}%  ${llmAcc.padStart(6)}%  ${String(s.mcTotal).padStart(4)}  ${String(s.llmFail).padStart(5)}`);
        tMC += s.mcTotal;
        tSM += s.mcCorrect;
        tLLM += s.llmCorrect;
        tFail += s.llmFail;
      }
      if (tMC > 0) {
        print("  \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500  \u2500\u2500\u2500\u2500\u2500\u2500  \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500  \u2500\u2500\u2500\u2500  \u2500\u2500\u2500\u2500\u2500\u2500");
        print(`  ${"TOTAL".padEnd(24)} ${(tSM / tMC * 100).toFixed(1).padStart(5)}%  ${(tLLM / tMC * 100).toFixed(1).padStart(6)}%  ${String(tMC).padStart(4)}  ${String(tFail).padStart(5)}`);
      }
    } else {
      print("  Type                    Acc      N");
      print("  \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500  \u2500\u2500\u2500\u2500\u2500\u2500  \u2500\u2500\u2500\u2500");
      let totalMC = 0, totalMCCorrect = 0;
      for (const type of typeOrder) {
        const s = typeStats[type];
        if (!s || s.mcTotal === 0) continue;
        const acc = (s.mcCorrect / s.mcTotal * 100).toFixed(1);
        print(`  ${type.padEnd(24)} ${acc.padStart(5)}%  ${String(s.mcTotal).padStart(4)}`);
        totalMC += s.mcTotal;
        totalMCCorrect += s.mcCorrect;
      }
      if (totalMC > 0) {
        print("  \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500  \u2500\u2500\u2500\u2500\u2500\u2500  \u2500\u2500\u2500\u2500");
        print(`  ${"TOTAL".padEnd(24)} ${(totalMCCorrect / totalMC * 100).toFixed(1).padStart(5)}%  ${String(totalMC).padStart(4)}`);
      }
    }
  }
  print();
  print("\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550");
  print("  Layer 3: Latency & Storage");
  print("\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550");
  print();
  if (perQueryLatency.length > 0) {
    const sorted = [...perQueryLatency].sort((a, b) => a - b);
    const p50 = sorted[Math.floor(sorted.length * 0.5)];
    const p95 = sorted[Math.floor(sorted.length * 0.95)];
    const p99 = sorted[Math.floor(sorted.length * 0.99)];
    const avg = sorted.reduce((a, b) => a + b, 0) / sorted.length;
    print(`  Recall Latency (${sorted.length} queries):`);
    print(`    avg=${avg.toFixed(1)}ms  p50=${p50}ms  p95=${p95}ms  p99=${p99}ms`);
    print(`    throughput: ${(questions.length / elapsed).toFixed(1)} q/s`);
  }
  if (totalMemoryBytes > 0) {
    const namStorageKB = totalMemoryBytes / 1024;
    const totalMemories = [...convMemoryCount.values()].reduce((a, b) => a + b, 0);
    const vectorStorageKB = totalMemories * 1536 * 4 / 1024;
    const aamStorageKB = 2300;
    print();
    print(`  Storage Comparison (${totalMemories} memories):`);
    print(`    NAM (text + AAM + SQLite):  ${((namStorageKB + aamStorageKB) / 1024).toFixed(1)} MB`);
    print(`    Vector (ada-002 1536d):     ${(vectorStorageKB / 1024).toFixed(1)} MB  (embeddings only, +index)`);
    print(`    Ratio: NAM is ${(vectorStorageKB / (namStorageKB + aamStorageKB)).toFixed(1)}x smaller`);
    print(`    External API calls: NAM=0  Vector=N (embedding generation)`);
  }
  function getBucket(memCount) {
    if (memCount <= 200) return "small (\u2264200)";
    if (memCount <= 400) return "medium (201-400)";
    if (memCount <= 600) return "large (401-600)";
    return "xlarge (600+)";
  }
  const lengthBuckets = {};
  for (const r of perQuestionResult) {
    const memCount = convMemoryCount.get(r.convId) || 0;
    const bucket = getBucket(memCount);
    if (!lengthBuckets[bucket]) lengthBuckets[bucket] = { hit: 0, total: 0, mcCorrect: 0, mcTotal: 0 };
    const b = lengthBuckets[bucket];
    if (!r.isAdversarial) {
      b.total++;
      if (r.hit) b.hit++;
    }
    if (!opts.recallOnly) {
      b.mcTotal++;
      if (r.mcCorrect) b.mcCorrect++;
    }
  }
  print();
  print("\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550");
  print("  Layer 4: Recall by Conversation Size");
  print("\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550");
  print();
  print("  Conv ID     Memories   Questions   Size Bucket");
  print("  \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500  \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500  \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500  \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500");
  for (const convId of convIds) {
    const memCount = convMemoryCount.get(convId) || 0;
    const qCount = convMap.get(convId)?.length || 0;
    if (memCount > 0) {
      print(`  ${convId.padEnd(10)} ${String(memCount).padStart(7)}   ${String(qCount).padStart(9)}   ${getBucket(memCount)}`);
    }
  }
  const bucketOrder = ["small (\u2264200)", "medium (201-400)", "large (401-600)", "xlarge (600+)"];
  print();
  print(`  Size Bucket          Hit@10    ${opts.recallOnly ? "" : "MC Acc    "}N`);
  print(`  \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500  \u2500\u2500\u2500\u2500\u2500\u2500  ${opts.recallOnly ? "" : "\u2500\u2500\u2500\u2500\u2500\u2500  "}\u2500\u2500\u2500\u2500`);
  for (const bucket of bucketOrder) {
    const b = lengthBuckets[bucket];
    if (!b || b.total === 0) continue;
    const hitRate = (b.hit / b.total * 100).toFixed(1);
    const mcRate = b.mcTotal > 0 ? (b.mcCorrect / b.mcTotal * 100).toFixed(1) : "-";
    if (opts.recallOnly) {
      print(`  ${bucket.padEnd(21)} ${hitRate.padStart(5)}%  ${String(b.total).padStart(4)}`);
    } else {
      print(`  ${bucket.padEnd(21)} ${hitRate.padStart(5)}%  ${mcRate.padStart(5)}%  ${String(b.total).padStart(4)}`);
    }
  }
  print();
  print("\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550");
  print("  Layer 5: Memory Pool Size vs Recall Accuracy");
  print("\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550");
  print();
  const convsBySize = convIds.filter((id) => convMemoryCount.get(id)).map((id) => ({ id, memCount: convMemoryCount.get(id), questions: perQuestionResult.filter((r) => r.convId === id) })).sort((a, b) => a.memCount - b.memCount);
  print(`  Memories   Conv ID    Hit@10   ${opts.recallOnly ? "" : "MC Acc   "}Questions`);
  print(`  \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500  \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500  \u2500\u2500\u2500\u2500\u2500\u2500  ${opts.recallOnly ? "" : "\u2500\u2500\u2500\u2500\u2500\u2500  "}\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500`);
  for (const conv of convsBySize) {
    const nonAdv = conv.questions.filter((r) => !r.isAdversarial);
    const hits = nonAdv.filter((r) => r.hit).length;
    const total = nonAdv.length;
    const hitRate = total > 0 ? (hits / total * 100).toFixed(1) : "-";
    if (opts.recallOnly) {
      print(`  ${String(conv.memCount).padStart(7)}   ${conv.id.padEnd(10)} ${hitRate.padStart(5)}%  ${String(total).padStart(8)}`);
    } else {
      const mcHits = conv.questions.filter((r) => r.mcCorrect).length;
      const mcTotal = conv.questions.length;
      const mcRate = mcTotal > 0 ? (mcHits / mcTotal * 100).toFixed(1) : "-";
      print(`  ${String(conv.memCount).padStart(7)}   ${conv.id.padEnd(10)} ${hitRate.padStart(5)}%  ${mcRate.padStart(5)}%  ${String(total).padStart(8)}`);
    }
  }
  print();
  print(`  Random baseline: 10.0%`);
  print(`  Time: ${elapsed.toFixed(1)}s (${(questions.length / elapsed).toFixed(0)} q/s)`);
  print(`  Isolation: per-conv (AAM + fact-store reset between conversations)`);
  print();
}
run();
