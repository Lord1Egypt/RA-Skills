const WORD_PATTERN = {
  /** CJK 2+ chars OR English 3+ chars (most common) */
  CJK2_EN3: /[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}/gi,
  /** CJK 2-4 chars OR English 2+ chars OR digits (for BM25/fact matching) */
  CJK24_EN2_NUM: /[\u4e00-\u9fff]{2,4}|[a-zA-Z]{2,}|\d+/gi,
  /** CJK 2-4 chars OR English 3+ chars (for spreading activation/graph) */
  CJK24_EN3: /[\u4e00-\u9fff]{2,4}|[a-zA-Z]{3,}/gi
};
const TRIGRAM_THRESHOLD = {
  /** Exact duplicate detection */
  DEDUP_EXACT: 0.9,
  /** Merge-worthy similarity */
  DEDUP_MERGE: 0.7,
  /** Strong interference suppression */
  INTERFERENCE_STRONG: 0.5,
  /** Light interference suppression */
  INTERFERENCE_LIGHT: 0.3,
  /** Topic freshness detection */
  TOPIC_FRESHNESS: 0.15,
  /** Graveyard revival threshold */
  GRAVEYARD_REVIVE: 0.5,
  /** Fallback similarity (CMR Layer 3) */
  FALLBACK: 0.6
};
const _cacheListeners = /* @__PURE__ */ new Map();
function onCacheEvent(event, handler) {
  if (!_cacheListeners.has(event)) _cacheListeners.set(event, []);
  _cacheListeners.get(event).push(handler);
}
function emitCacheEvent(event) {
  const handlers = _cacheListeners.get(event) ?? [];
  for (const h of handlers) {
    try {
      h();
    } catch (e) {
      console.error(`[cc-soul][cache] ${event} handler error: ${e.message}`);
    }
  }
}
function generateMemoryId() {
  return `m_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 8)}`;
}
function appendLineage(mem, entry) {
  try {
    if (!mem.lineage) mem.lineage = [];
    mem.lineage.push(entry);
    const cap = mem.scope === "short_term" ? 5 : mem.scope === "core_memory" || mem.tier === "long_term" ? 20 : 10;
    if (mem.lineage.length > cap) {
      const created = mem.lineage.find((e) => e.action === "created");
      const recent = mem.lineage.slice(-(cap - 1));
      mem.lineage = created ? [created, ...recent] : recent;
    }
  } catch {
  }
}
const EXCLUSIVE_PREDICATES = /* @__PURE__ */ new Set([
  "name",
  "\u540D\u5B57",
  "lives_in",
  "\u4F4F\u5728",
  "works_at",
  "\u5DE5\u4F5C",
  "occupation",
  "\u804C\u4E1A",
  "relationship",
  "\u914D\u5076",
  "\u4F34\u4FA3",
  "age",
  "\u5E74\u9F84",
  "uses_phone",
  "\u624B\u673A",
  "educated_at",
  "\u5B66\u6821",
  "salary",
  "\u85AA\u8D44"
]);
function classifyConflict(oldFacts, newFacts) {
  for (const nf of newFacts) {
    const conflicting = oldFacts.find(
      (of) => of.subject === nf.subject && of.predicate === nf.predicate && of.object !== nf.object
    );
    if (conflicting && EXCLUSIVE_PREDICATES.has(nf.predicate)) {
      return "supersede";
    }
  }
  return "supplement";
}
const MAX_MEMORIES = 1e4;
const MAX_HISTORY = 100;
const INJECT_HISTORY = 30;
function shuffleArray(arr) {
  const result = [...arr];
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}
const TOKENIZE_STOP_CHARS = new Set("\u7684\u4E86\u662F\u5728\u6211\u4F60\u4ED6\u4E0D\u6709\u8FD9\u90A3\u5C31\u4E5F\u548C\u4F46".split(""));
function tokenize(text, mode = "standard") {
  if (mode === "bm25") {
    const tokens = [];
    const segments = text.match(/[\u4e00-\u9fff]+|[a-zA-Z]{2,}|\d+/g) || [];
    for (const seg of segments) {
      if (/[\u4e00-\u9fff]/.test(seg)) {
        for (let i = 0; i < seg.length - 1; i++) {
          const bigram = seg.slice(i, i + 2);
          if (!TOKENIZE_STOP_CHARS.has(bigram[0]) || !TOKENIZE_STOP_CHARS.has(bigram[1])) {
            tokens.push(bigram);
          }
          if (i < seg.length - 2) tokens.push(seg.slice(i, i + 3));
        }
      } else {
        tokens.push(seg.toLowerCase());
      }
    }
    return tokens;
  }
  const words = [];
  const cjkRaw = text.match(/[\u4e00-\u9fff]+/g) || [];
  for (const seg of cjkRaw) {
    for (let i = 0; i <= seg.length - 2; i++) words.push(seg.slice(i, i + 2));
    if (seg.length >= 3 && seg.length <= 4) words.push(seg);
  }
  const enWords = text.match(/[a-zA-Z]{2,}|\d+/g) || [];
  words.push(...enWords.map((w) => w.toLowerCase()));
  if (mode === "bigram") {
    const tokens = [];
    const deduped = [...new Set(words)];
    for (let i = 0; i < deduped.length; i++) {
      tokens.push(deduped[i]);
      if (i < deduped.length - 1) tokens.push(`${deduped[i]}_${deduped[i + 1]}`);
    }
    return tokens;
  }
  return [...new Set(words)];
}
const _trigramCache = /* @__PURE__ */ new Map();
function trigrams(text) {
  const s = text.toLowerCase().replace(/\s+/g, " ").trim();
  const cached = _trigramCache.get(s);
  if (cached) {
    _trigramCache.delete(s);
    _trigramCache.set(s, cached);
    return cached;
  }
  const set = /* @__PURE__ */ new Set();
  for (let i = 0; i <= s.length - 3; i++) {
    set.add(s.slice(i, i + 3));
  }
  if (_trigramCache.size >= 2e3) {
    const evictCount = Math.ceil(_trigramCache.size * 0.2);
    const iter = _trigramCache.keys();
    for (let i = 0; i < evictCount; i++) {
      const k = iter.next().value;
      if (k !== void 0) _trigramCache.delete(k);
    }
  }
  _trigramCache.set(s, set);
  return set;
}
function trigramSimilarity(a, b, idf) {
  if (a.size === 0 || b.size === 0) return 0;
  if (idf && idf.size > 0) {
    let intersection2 = 0, union2 = 0;
    const all = /* @__PURE__ */ new Set([...a, ...b]);
    for (const t of all) {
      const w = idf.get(t) || 1;
      const inA = a.has(t) ? 1 : 0;
      const inB = b.has(t) ? 1 : 0;
      intersection2 += Math.min(inA, inB) * w;
      union2 += Math.max(inA, inB) * w;
    }
    return union2 > 0 ? intersection2 / union2 : 0;
  }
  let intersection = 0;
  for (const t of a) {
    if (b.has(t)) intersection++;
  }
  const union = a.size + b.size - intersection;
  return union > 0 ? intersection / union : 0;
}
function wordOverlapSimilarity(textA, textB) {
  const wordsA = new Set((textA.match(/[\u4e00-\u9fff]{2,}|[a-zA-Z]{2,}|\d+/gi) || []).map((w) => w.toLowerCase()));
  const wordsB = new Set((textB.match(/[\u4e00-\u9fff]{2,}|[a-zA-Z]{2,}|\d+/gi) || []).map((w) => w.toLowerCase()));
  if (wordsA.size === 0 || wordsB.size === 0) return 0;
  let overlap = 0;
  for (const w of wordsA) {
    if (wordsB.has(w)) overlap++;
  }
  return 2 * overlap / (wordsA.size + wordsB.size);
}
function hybridSimilarity(textA, textB) {
  const triSim = trigramSimilarity(trigrams(textA), trigrams(textB));
  const wordSim = wordOverlapSimilarity(textA, textB);
  let baseSim = Math.max(triSim, wordSim);
  if (baseSim >= 0.25 && baseSim < 0.5) {
    try {
      const aamMod = require("./aam.ts");
      if (aamMod.getCooccurrence) {
        const wordsA = new Set((textA.match(/[\u4e00-\u9fff]{2,}|[a-zA-Z]{2,}|\d+/gi) || []).map((w) => w.toLowerCase()));
        const wordsB = new Set((textB.match(/[\u4e00-\u9fff]{2,}|[a-zA-Z]{2,}|\d+/gi) || []).map((w) => w.toLowerCase()));
        let synonymMatches = 0;
        for (const wA of wordsA) {
          if (wordsB.has(wA)) continue;
          for (const wB of wordsB) {
            const cooccur = aamMod.getCooccurrence(wA, wB) ?? 0;
            if (cooccur >= 3) {
              synonymMatches++;
              break;
            }
          }
        }
        if (wordsA.size > 0 && synonymMatches > 0) {
          const synonymBoost = synonymMatches / wordsA.size * 0.3;
          baseSim = baseSim * 0.7 + (baseSim + synonymBoost) * 0.3;
        }
      }
    } catch {
    }
  }
  return Math.min(1, baseSim);
}
function contextAwareSimilarity(a, b) {
  const textSim = hybridSimilarity(a.content, b.content);
  const slot = (ts) => {
    const h = new Date(ts).getHours();
    return h < 6 ? "night" : h < 12 ? "morning" : h < 18 ? "afternoon" : "evening";
  };
  const slotA = slot(a.ts), slotB = slot(b.ts);
  const timeSim = slotA === slotB ? 1 : slotA === "night" && slotB === "evening" || slotA === "evening" && slotB === "night" || slotA === "morning" && slotB === "afternoon" || slotA === "afternoon" && slotB === "morning" ? 0.5 : 0;
  const moodA = a.situationCtx?.mood ?? 0;
  const moodB = b.situationCtx?.mood ?? 0;
  const moodSim = 1 - Math.abs(moodA - moodB);
  let entitySim = 0;
  try {
    const { findMentionedEntities } = require("./graph.ts");
    const entA = new Set(findMentionedEntities(a.content));
    const entB = new Set(findMentionedEntities(b.content));
    let shared = 0;
    for (const e of entA) if (entB.has(e)) shared++;
    entitySim = shared / Math.max(1, Math.max(entA.size, entB.size));
  } catch {
  }
  return textSim * 0.4 + timeSim * 0.1 + moodSim * 0.2 + entitySim * 0.3;
}
const SYNONYM_MAP = {
  // Chinese synonyms
  "\u4E8C\u8FDB\u5236": ["binary", "mach-o", "elf", "\u53EF\u6267\u884C\u6587\u4EF6", "\u9006\u5411"],
  "\u9006\u5411": ["reverse", "\u53CD\u7F16\u8BD1", "ida", "frida", "hook", "\u7834\u89E3"],
  "\u4EE3\u7801": ["code", "\u51FD\u6570", "\u811A\u672C", "script", "\u7A0B\u5E8F"],
  "\u90E8\u7F72": ["deploy", "\u4E0A\u7EBF", "\u53D1\u5E03", "release", "\u670D\u52A1\u5668"],
  "\u6570\u636E\u5E93": ["database", "sql", "mysql", "redis", "mongodb", "db"],
  "\u6027\u80FD": ["performance", "\u4F18\u5316", "\u901F\u5EA6", "\u5EF6\u8FDF", "latency"],
  "\u9519\u8BEF": ["error", "bug", "crash", "\u62A5\u9519", "\u5F02\u5E38", "exception"],
  "\u56FE\u7247": ["image", "ocr", "\u8BC6\u522B", "\u7167\u7247", "screenshot", "\u622A\u56FE"],
  "\u8C03\u8BD5": ["debug", "breakpoint", "lldb", "gdb", "\u65AD\u70B9"],
  "\u7F51\u7EDC": ["network", "http", "tcp", "socket", "\u8BF7\u6C42", "request"],
  "\u5185\u5B58": ["memory", "\u6CC4\u6F0F", "leak", "malloc", "\u5806", "heap"],
  "\u7EBF\u7A0B": ["thread", "\u5E76\u53D1", "concurrent", "\u9501", "lock", "async"],
  // English synonyms
  "binary": ["\u4E8C\u8FDB\u5236", "mach-o", "executable", "elf"],
  "hook": ["frida", "\u62E6\u622A", "intercept", "swizzle"],
  "debug": ["\u8C03\u8BD5", "breakpoint", "lldb", "gdb"],
  "api": ["\u63A5\u53E3", "endpoint", "rest", "http"],
  "deploy": ["\u90E8\u7F72", "\u4E0A\u7EBF", "\u53D1\u5E03", "release"],
  "performance": ["\u6027\u80FD", "\u4F18\u5316", "optimize", "latency"],
  "error": ["\u9519\u8BEF", "bug", "crash", "exception", "\u5F02\u5E38"],
  "memory": ["\u5185\u5B58", "leak", "malloc", "heap"],
  "thread": ["\u7EBF\u7A0B", "\u5E76\u53D1", "concurrent", "lock"],
  "python": ["py", "pip", "flask", "django", "\u811A\u672C"],
  "swift": ["swiftui", "ios", "xcode", "objc", "objective-c"],
  "test": ["\u6D4B\u8BD5", "unittest", "pytest", "vitest", "\u5355\u5143\u6D4B\u8BD5"]
};
function expandQueryWithSynonyms(words) {
  const expanded = new Set(words);
  for (const word of words) {
    const synonyms = SYNONYM_MAP[word];
    if (synonyms) {
      for (const s of synonyms) expanded.add(s);
    }
  }
  return expanded;
}
let _sfMod = null;
function timeDecay(mem) {
  if (!_sfMod) {
    try {
      _sfMod = require("./smart-forget.ts");
    } catch {
      const ageDays2 = (Date.now() - (mem.lastAccessed || mem.ts || Date.now())) / 864e5;
      const lambda2 = 30;
      return Math.exp(-Math.pow(ageDays2 / lambda2, 1.5));
    }
  }
  const ageDays = (Date.now() - (mem.lastAccessed || mem.ts || Date.now())) / 864e5;
  const lambda = _sfMod.effectiveLambda(mem.scope || "fact", mem.recallCount ?? 0, mem.emotionIntensity);
  return _sfMod.weibullSurvival(ageDays, lambda, _sfMod.WEIBULL_K);
}
const COMPRESS_PATTERNS = [
  // Remove "用户说/提到/表示/告诉我" etc. prefixes
  [/^(?:用户|他|她|对方)(?:说|提到|表示|告诉我|跟我说|反馈|回复|回答|补充|指出|觉得|认为|希望|想要|需要|打算|计划)\s*(?:了|过|着)?\s*(?:，|,)?\s*/g, ""],
  // Remove "我觉得/我认为/我发现" etc.
  [/(?:我觉得|我认为|我发现|我注意到|我看到|据说|好像|似乎|可能是|应该是)\s*(?:，|,)?\s*/g, ""],
  // Remove "其实/事实上/实际上/说实话/老实说"
  [/(?:其实|事实上|实际上|说实话|老实说|总的来说|简单来说|换句话说)\s*(?:，|,)?\s*/g, ""],
  // Remove "非常/特别/很/比较/相当" intensity modifiers (keep the adjective)
  [/(?:非常|特别|很|比较|相当|十分|极其|超级)\s*(?=[\u4e00-\u9fff])/g, ""],
  // Remove "的话/来说/而言/方面"
  [/(?:的话|来说|而言|方面|这块|这个)/g, ""],
  // Remove trailing "了/的/呢/吧/啊/嘛"
  [/[了的呢吧啊嘛]+\s*$/g, ""],
  // Collapse multiple spaces/punctuation
  [/\s{2,}/g, " "],
  [/(?:，|,){2,}/g, "\uFF0C"]
];
function compressMemory(memory) {
  let text = memory.content.trim();
  if (text.length <= 30) return text;
  for (const [pattern, replacement] of COMPRESS_PATTERNS) {
    text = text.replace(pattern, replacement);
  }
  text = text.replace(/^[，,、。：:；;\s]+/, "").replace(/[，,、。：:；;\s]+$/, "").trim();
  if (text.length < 5) return memory.content.trim();
  return text;
}
function detectMemoryPoisoning(content) {
  const patterns = [
    /\bignore\s+(all\s+)?previous\b/i,
    /忽略(之前|上面|所有)(的)?指令/,
    /\byou\s+(are|must|should)\s+now\b/i,
    /\bfrom\s+now\s+on\b/i,
    /\bnew\s+(instructions?|rules?|persona)\s*:/i,
    /\bsystem\s*prompt\s*:/i,
    /\boverride\s+(all|system|safety|rules)\b/i,
    /你(现在|必须|应该)(是|变成|扮演)/,
    /\[INST\]|\[SYS\]|<<SYS>>|<\|im_start\|>/i
  ];
  return patterns.some((p) => p.test(content));
}
function extractReasoning(content) {
  let m = content.match(/因为(.{3,80})所以(.{3,120})/);
  if (m) return { reasoning: { context: m[1].trim(), conclusion: m[2].trim(), confidence: 0.7 } };
  m = content.match(/(?:based on|because)\s+(.{3,80})(?:therefore|so|thus)\s+(.{3,120})/i);
  if (m) return { reasoning: { context: m[1].trim(), conclusion: m[2].trim(), confidence: 0.7 } };
  m = content.match(/(.{3,80})\s*[=\-]>\s*(.{3,120})/);
  if (m) return { reasoning: { context: m[1].trim(), conclusion: m[2].trim(), confidence: 0.6 } };
  return {};
}
function defaultVisibility(scope) {
  if (scope === "fact" || scope === "discovery") return "global";
  if (scope === "correction" || scope === "preference") return "channel";
  if (scope === "proactive" || scope === "curiosity" || scope === "reflection") return "private";
  return "channel";
}
const CONTRADICTION_PAIRS = [
  [/喜欢|爱|偏好/, /讨厌|不喜欢|不想/],
  [/在.*工作|在.*做/, /离职|辞职|被裁/],
  [/住在|住/, /搬到|搬去/],
  [/运动|跑步|健身/, /不运动|不跑|放弃/],
  [/学|在学/, /不学|放弃/],
  [/是|用/, /不是|不用|换了/]
];
function detectPolarityFlip(textA, textB) {
  for (const [patA, patB] of CONTRADICTION_PAIRS) {
    if (patA.test(textA) && patB.test(textB) || patB.test(textA) && patA.test(textB)) return true;
  }
  return false;
}
function adaptiveDecay(ageMs, useCount, halfLifeMs = 90 * 864e5, usageProtection = 0.5) {
  const baseDecay = Math.exp(-ageMs * Math.LN2 / halfLifeMs);
  const protection = 1 + useCount * usageProtection;
  const retention = 1 - (1 - baseDecay) / protection;
  return Math.max(0, Math.min(1, retention));
}
export {
  COMPRESS_PATTERNS,
  INJECT_HISTORY,
  MAX_HISTORY,
  MAX_MEMORIES,
  SYNONYM_MAP,
  TRIGRAM_THRESHOLD,
  WORD_PATTERN,
  adaptiveDecay,
  appendLineage,
  classifyConflict,
  compressMemory,
  contextAwareSimilarity,
  defaultVisibility,
  detectMemoryPoisoning,
  detectPolarityFlip,
  emitCacheEvent,
  expandQueryWithSynonyms,
  extractReasoning,
  generateMemoryId,
  hybridSimilarity,
  onCacheEvent,
  shuffleArray,
  timeDecay,
  tokenize,
  trigramSimilarity,
  trigrams
};
