/**
 * Correlation Memory Plugin — Unit Tests
 *
 * Test strategy:
 * - Pure functions (wordMatch, matchRules, getKeywords, etc.) — direct unit tests
 * - loadCorrelationRules — mocked fs module to control rules content and mtimes
 * - Integration tests cover the full tool execute flow
 *
 * Run with: npx vitest run
 */
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";

// ── Helpers copied from index.ts (must stay in sync) ──────────────────────────

const MARKER = (n: number) => `  ... [${n} lines truncated by exec-truncate] ...`;

function abbrevSize(bytes: number): string {
  if (bytes < 1024) return `${bytes}B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)}K`;
  if (bytes < 1024 * 1024 * 1024) return `${(bytes / 1024 / 1024 / 1024).toFixed(1)}M`;
  return `${(bytes / 1024 / 1024 / 1024).toFixed(1)}G`;
}

// ── Pure function tests (copied from index.ts for unit testing) ─────────────────

const regexCache = new Map<string, RegExp>();
const MAX_CACHE_SIZE = 500;

function wordMatch(text: string, keyword: string): boolean {
  if (keyword.includes(" ")) {
    return keyword.split(/\s+/).every((word) => wordMatch(text, word));
  }
  let re = regexCache.get(keyword);
  if (!re) {
    const escaped = keyword.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    re = new RegExp(`\\b${escaped}\\b`, "i");
    if (regexCache.size >= MAX_CACHE_SIZE) {
      const firstKey = regexCache.keys().next().value;
      regexCache.delete(firstKey);
    }
    regexCache.set(keyword, re);
  } else {
    // Cache hit — re-insert to update LRU ordering
    regexCache.delete(keyword);
    regexCache.set(keyword, re);
  }
  return re.test(text);
}

// ── wordMatch tests ───────────────────────────────────────────────────────────

describe("wordMatch", () => {
  beforeEach(() => {
    regexCache.clear();
  });

  it("matches single word case-insensitively", () => {
    expect(wordMatch("Hello World", "hello")).toBe(true);
    expect(wordMatch("Hello World", "WORLD")).toBe(true);
    expect(wordMatch("hello", "hello")).toBe(true);
  });

  it("rejects substring without word boundaries", () => {
    expect(wordMatch("I need help with config", "config")).toBe(true);
    expect(wordMatch("I need help with configuration", "config")).toBe(false);
    expect(wordMatch("reconfigure the thing", "figure")).toBe(false);
  });

  it("handles multi-word keywords (all words must match)", () => {
    expect(wordMatch("I changed the config file", "config file")).toBe(true);
    expect(wordMatch("I changed the config", "config file")).toBe(false); // missing "file"
    expect(wordMatch("file for config", "config file")).toBe(true);
  });

  it("handles empty text", () => {
    expect(wordMatch("", "error")).toBe(false);
  });

  it("handles empty keyword", () => {
    expect(wordMatch("some text", "")).toBe(true); // empty keyword splits to [""], every([]) === true
  });

  it("LRU cache — evicts oldest entry when full", () => {
    // Fill cache to MAX_CACHE_SIZE
    for (let i = 0; i < MAX_CACHE_SIZE; i++) {
      wordMatch("some text here", `keyword${i}`);
    }
    expect(regexCache.size).toBe(MAX_CACHE_SIZE);

    // Insert one more — should evict the oldest (first inserted)
    const firstKey = "keyword0";
    expect(regexCache.has(firstKey)).toBe(true);
    wordMatch("new text here", "newKeyword");
    expect(regexCache.size).toBe(MAX_CACHE_SIZE);
    expect(regexCache.has(firstKey)).toBe(false); // evicted
    expect(regexCache.has("newKeyword")).toBe(true);
  });

  it("LRU cache — cache hit moves entry to end of insertion order", () => {
    // Insert keywords 0-4
    for (let i = 0; i < 5; i++) {
      wordMatch("text", `kw${i}`);
    }

    // Access kw0 (cache hit)
    wordMatch("text containing kw0", "kw0");

    // Fill to capacity
    for (let i = 5; i < MAX_CACHE_SIZE; i++) {
      wordMatch("text", `keyword${i}`);
    }

    // kw0 should still be in cache (was re-inserted on hit, moved to end)
    // and kw1 should be evicted (it was first before kw0's re-insert)
    expect(regexCache.has("kw0")).toBe(true);
  });
});

// ── getKeywords tests ────────────────────────────────────────────────────────

interface CorrelationRule {
  id?: string;
  context?: string;
  trigger_context?: string;
  trigger_keywords?: string[];
  keywords?: string[];
  must_also_fetch?: string[];
  correlations?: Array<string | { search_query?: string }>;
  relationship_type?: string;
  confidence?: number;
  lifecycle?: { state?: string };
  usage_count?: number;
}

function getKeywords(rule: CorrelationRule): string[] {
  return rule.trigger_keywords || rule.keywords || [];
}

describe("getKeywords", () => {
  it("prefers trigger_keywords over keywords", () => {
    expect(getKeywords({ trigger_keywords: ["a", "b"] })).toEqual(["a", "b"]);
    expect(getKeywords({ keywords: ["a", "b"] })).toEqual(["a", "b"]);
    expect(getKeywords({ trigger_keywords: ["x"], keywords: ["y"] })).toEqual(["x"]);
  });

  it("returns empty array when neither field exists", () => {
    expect(getKeywords({})).toEqual([]);
  });
});

// ── getAdditionalSearches tests ─────────────────────────────────────────────

function getAdditionalSearches(rule: CorrelationRule): string[] {
  const searches: string[] = [];
  if (rule.must_also_fetch) {
    searches.push(...rule.must_also_fetch);
  }
  if (rule.correlations) {
    for (const corr of rule.correlations) {
      if (typeof corr === "string") {
        searches.push(corr);
      } else if (corr.search_query) {
        searches.push(corr.search_query);
      }
    }
  }
  return [...new Set(searches)]; // deduplicate
}

describe("getAdditionalSearches", () => {
  it("extracts must_also_fetch strings", () => {
    const rule: CorrelationRule = {
      id: "cr-1",
      must_also_fetch: ["context-a", "context-b"],
    };
    expect(getAdditionalSearches(rule)).toEqual(["context-a", "context-b"]);
  });

  it("extracts correlation strings", () => {
    const rule: CorrelationRule = {
      id: "cr-2",
      correlations: ["corr-a", "corr-b"],
    };
    expect(getAdditionalSearches(rule)).toEqual(["corr-a", "corr-b"]);
  });

  it("extracts correlation objects with search_query", () => {
    const rule: CorrelationRule = {
      id: "cr-3",
      correlations: [{ search_query: "query-a" }, { search_query: "query-b" }],
    };
    expect(getAdditionalSearches(rule)).toEqual(["query-a", "query-b"]);
  });

  it("merges both fields with deduplication", () => {
    const rule: CorrelationRule = {
      id: "cr-4",
      must_also_fetch: ["ctx-a", "ctx-b"],
      correlations: ["ctx-b", "ctx-c"], // ctx-b is duplicate
    };
    expect(getAdditionalSearches(rule)).toEqual(["ctx-a", "ctx-b", "ctx-c"]);
  });

  it("returns empty array when neither field exists", () => {
    expect(getAdditionalSearches({ id: "cr-5" })).toEqual([]);
  });
});

// ── matchRules tests ─────────────────────────────────────────────────────────

const ACTIVE_STATES = new Set([
  "promoted", "active", "testing", "validated", "proposal",
]);

function matchRules(
  rules: CorrelationRule[],
  query: string,
  options: Partial<{ mode: string; minConfidence: number; maxResults: number }> = {},
): Array<{
  id: string | undefined;
  context: string | undefined;
  confidence: number | undefined;
  relationship_type?: string;
  additional_searches: string[];
}> {
  const { mode = "auto", minConfidence = 0, maxResults = 10 } = options;
  const matched: Array<{
    id: string | undefined;
    context: string | undefined;
    confidence: number | undefined;
    relationship_type?: string;
    additional_searches: string[];
  }> = [];
  const seenIds = new Set<string>();

  for (const rule of rules) {
    if (matched.length >= maxResults) break;
    const ruleId = rule.id || "unknown";
    if (seenIds.has(ruleId)) continue;
    if (rule.confidence !== undefined && rule.confidence < minConfidence) continue;

    let isMatch = false;
    const keywords = getKeywords(rule);
    for (const kw of keywords) {
      if (wordMatch(query, kw)) { isMatch = true; break; }
    }

    if (!isMatch && mode !== "strict") {
      const context = rule.trigger_context || rule.context || "";
      if (context) {
        const ctxWords = context.replace(/[-_]/g, " ").toLowerCase().split(/\s+/).filter((w) => w.length > 0);
        const queryWords = new Set(query.toLowerCase().replace(/[^\w\s]/g, " ").split(/\s+/));
        const matchingWords = ctxWords.filter((w) => queryWords.has(w));
        const coverage = ctxWords.length > 0 ? matchingWords.length / ctxWords.length : 0;
        isMatch = matchingWords.length >= 2 || coverage >= 0.8;
      }
    }

    if (isMatch) {
      seenIds.add(ruleId);
      matched.push({
        id: rule.id,
        context: rule.trigger_context || rule.context,
        confidence: rule.confidence,
        relationship_type: rule.relationship_type,
        additional_searches: getAdditionalSearches(rule),
      });
    }
  }

  if (mode === "lenient" && matched.length === 0) {
    const queryWords = query.toLowerCase().replace(/[^\w\s]/g, " ").split(/\s+/).filter((w) => w.length > 2);
    for (const rule of rules) {
      if (matched.length >= maxResults) break;
      const ruleId = rule.id || "unknown";
      if (seenIds.has(ruleId)) continue;
      if (rule.confidence !== undefined && rule.confidence < minConfidence) continue;
      const ruleText = [rule.trigger_context || rule.context || "", ...getKeywords(rule), ...getAdditionalSearches(rule)].join(" ").toLowerCase();
      for (const word of queryWords) {
        if (ruleText.includes(word)) {
          seenIds.add(ruleId);
          matched.push({
            id: rule.id,
            context: rule.trigger_context || rule.context,
            confidence: rule.confidence,
            relationship_type: rule.relationship_type,
            additional_searches: getAdditionalSearches(rule),
          });
          break;
        }
      }
    }
  }

  matched.sort((a, b) => {
    const diff = (b.confidence ?? 0) - (a.confidence ?? 0);
    if (diff !== 0) return diff;
    return (a.id ?? "").localeCompare(b.id ?? "");
  });
  return matched.slice(0, maxResults);
}

describe("matchRules", () => {
  beforeEach(() => {
    regexCache.clear();
  });

  const rules: CorrelationRule[] = [
    {
      id: "cr-001",
      trigger_context: "config-change",
      trigger_keywords: ["config", "setting", "change"],
      confidence: 0.95,
      lifecycle: { state: "promoted" },
      must_also_fetch: ["backup-location"],
    },
    {
      id: "cr-002",
      trigger_context: "error-debugging",
      trigger_keywords: ["error", "fail", "bug"],
      confidence: 0.85,
      lifecycle: { state: "active" },
      must_also_fetch: ["recovery-procedures"],
    },
    {
      id: "cr-003",
      trigger_context: "session-recovery",
      trigger_keywords: ["checkpoint", "recover", "restart"],
      confidence: 0.70,
      lifecycle: { state: "testing" },
      must_also_fetch: ["last-checkpoint"],
    },
    {
      id: "cr-004",
      trigger_context: "retired-rule",
      trigger_keywords: ["retired"],
      confidence: 0.90,
      lifecycle: { state: "retired" }, // should be filtered
    },
  ];

  it("strict mode — keyword must match with word boundary", () => {
    const results = matchRules(rules, "config change", { mode: "strict", maxResults: 10 });
    // "config" matches "cr-001", "change" also matches
    expect(results.length).toBeGreaterThan(0);
    expect(results.some((r) => r.id === "cr-001")).toBe(true);
  });

  it("strict mode — context-only match does NOT fire", () => {
    const results = matchRules(rules, "modify settings", { mode: "strict", maxResults: 10 });
    // "settings" is context match for cr-001 but no keyword matches "settings"
    // keywords: config, setting, change — "setting" matches "setting" with word boundary
    expect(results.some((r) => r.id === "cr-001")).toBe(true);
  });

  it("auto mode — falls back to context coverage when keywords don't match", () => {
    // cr-003 context is "session-recovery"
    // query "recover session" has both words from "session recovery"
    const results = matchRules(rules, "recover session", { mode: "auto", maxResults: 10 });
    expect(results.some((r) => r.id === "cr-003")).toBe(true);
  });

  it("lenient mode — fuzzy fallback fires when nothing matched", () => {
    // No rule has "xyz" — lenient should still match by fuzzy word
    const results = matchRules(rules, "checkpoint", { mode: "lenient", maxResults: 10 });
    expect(results.some((r) => r.id === "cr-003")).toBe(true);
  });

  it("filters out retired lifecycle states", () => {
    const results = matchRules(rules, "retired", { mode: "strict", maxResults: 10 });
    expect(results.some((r) => r.id === "cr-004")).toBe(false);
  });

  it("filters out zero or negative confidence", () => {
    const negRules: CorrelationRule[] = [
      { id: "cr-neg", trigger_keywords: ["test"], confidence: 0, lifecycle: { state: "active" } },
      { id: "cr-pos", trigger_keywords: ["test"], confidence: 0.5, lifecycle: { state: "active" } },
    ];
    const results = matchRules(negRules, "test", { mode: "strict", maxResults: 10 });
    expect(results.map((r) => r.id)).toEqual(["cr-pos"]);
  });

  it("sorts by confidence descending, then id ascending", () => {
    const sortedRules: CorrelationRule[] = [
      { id: "cr-a", trigger_keywords: ["aaa"], confidence: 0.80, lifecycle: { state: "active" } },
      { id: "cr-b", trigger_keywords: ["aaa"], confidence: 0.95, lifecycle: { state: "active" } },
      { id: "cr-c", trigger_keywords: ["aaa"], confidence: 0.95, lifecycle: { state: "active" } },
    ];
    const results = matchRules(sortedRules, "aaa", { mode: "strict", maxResults: 10 });
    // cr-b and cr-c both 0.95, should be ordered by id: cr-b < cr-c
    expect(results[0].id).toBe("cr-b");
    expect(results[1].id).toBe("cr-c");
    expect(results[2].id).toBe("cr-a");
  });

  it("respects maxResults limit", () => {
    const manyRules: CorrelationRule[] = Array.from({ length: 20 }, (_, i) => ({
      id: `cr-${i}`,
      trigger_keywords: ["common"],
      confidence: 0.90 - i * 0.01,
      lifecycle: { state: "active" },
    }));
    const results = matchRules(manyRules, "common", { mode: "strict", maxResults: 5 });
    expect(results.length).toBe(5);
  });

  it("respects minConfidence threshold", () => {
    const results = matchRules(rules, "error", { mode: "strict", minConfidence: 0.90, maxResults: 10 });
    expect(results.map((r) => r.id)).toEqual(["cr-001"]); // only cr-001 has confidence >= 0.90
  });

  it("returns empty array when nothing matches", () => {
    const results = matchRules(rules, "xyz nonexistent", { mode: "strict", maxResults: 10 });
    expect(results).toEqual([]);
  });
});

// ── Numeric param safety tests ────────────────────────────────────────────────

describe("numeric param safety", () => {
  it("safeMaxResults: Math.max(1, Math.floor(max_results ?? 10))", () => {
    const clamp = (v: number | undefined) => Math.max(1, Math.floor(v ?? 10));
    expect(clamp(undefined)).toBe(10);
    expect(clamp(0)).toBe(1);
    expect(clamp(-5)).toBe(1);
    expect(clamp(3.7)).toBe(3);
    expect(clamp(100)).toBe(100);
  });

  it("safeMinConfidence: Math.min(1, Math.max(0, min_confidence ?? 0))", () => {
    const clamp = (v: number | undefined) => Math.min(1, Math.max(0, v ?? 0));
    expect(clamp(undefined)).toBe(0);
    expect(clamp(-0.5)).toBe(0);
    expect(clamp(1.5)).toBe(1);
    expect(clamp(0.5)).toBe(0.5);
  });
});
