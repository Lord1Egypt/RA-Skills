import type { OpenClawPluginApi, AnyAgentTool } from "openclaw/plugin-sdk";
import { emptyPluginConfigSchema } from "openclaw/plugin-sdk";
import * as fs from "fs";
import * as path from "path";

/**
 * Correlation Memory Plugin (Unified)
 *
 * Merges correlation-memory (rich matching) + correlation-rules-mem (SDK-native).
 * Provides automatic decision-context retrieval: when you query about topic X,
 * correlation rules surface related contexts Y and Z that typically matter.
 *
 * SECURITY NOTES:
 * - This plugin does NOT access environment variables directly
 * - This plugin does NOT make network requests (read-only local file ops)
 * - This plugin does NOT write to filesystem (read-only)
 * - This plugin does NOT handle credentials
 * - Workspace path resolved via ctx.workspaceDir (SDK runtime) with config/default fallbacks
 *
 * Audit: 2026-03-20 - Passed deep security review
 */

interface CorrelationRule {
  id?: string;
  context?: string;
  trigger_context?: string;
  // Support both field names from different rule formats
  trigger_keywords?: string[];
  keywords?: string[];
  must_also_fetch?: string[];
  correlations?: Array<string | { search_query?: string }>;
  relationship_type?: string;
  confidence?: number;
  lifecycle?: { state?: string };
  usage_count?: number;
}

interface MatchedRule {
  id: string | undefined;
  context: string | undefined;
  confidence: number | undefined;
  relationship_type?: string;
  additional_searches: string[];
}

// ── Rule Loading (with mtime cache) ──────────────────────────────────

let cachedRules: CorrelationRule[] | null = null;
let cachedMtime = 0;

const ACTIVE_STATES = new Set([
  "promoted", "active", "testing", "validated", "proposal",
]);

function loadCorrelationRules(workspacePath: string): CorrelationRule[] {
  const rulesPath = path.resolve(
    path.join(workspacePath, "memory/correlation-rules.json"),
  );

  try {
    const stat = fs.statSync(rulesPath);
    if (cachedRules && stat.mtimeMs === cachedMtime) return cachedRules;

    const data = fs.readFileSync(rulesPath, "utf-8");
    const parsed = JSON.parse(data);
    const rules: CorrelationRule[] = parsed.rules || [];

    // Filter to active rules only
    const filtered = rules.filter((rule) => {
      if (!rule.id) return false;
      if (rule.confidence !== undefined && rule.confidence <= 0) return false;
      const state = rule.lifecycle?.state;
      return !state || ACTIVE_STATES.has(state);
    });

    cachedRules = filtered;
    cachedMtime = stat.mtimeMs;
    return filtered;
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    console.error(`[correlation-memory] Failed to load rules from ${rulesPath}: ${msg}`);
    return [];
  }
}

// ── Keyword Extraction ────────────────────────────────────────────────

function getKeywords(rule: CorrelationRule): string[] {
  // Handle both field naming conventions
  return rule.trigger_keywords || rule.keywords || [];
}

function getContext(rule: CorrelationRule): string {
  return rule.trigger_context || rule.context || "";
}

function getAdditionalSearches(rule: CorrelationRule): string[] {
  const searches: string[] = [];

  // must_also_fetch (current rules format)
  if (rule.must_also_fetch) {
    searches.push(...rule.must_also_fetch);
  }

  // correlations (legacy format)
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

// ── Word-boundary matching ───────────────────────────────────────────

const regexCache = new Map<string, RegExp>();

function wordMatch(text: string, keyword: string): boolean {
  // Multi-word keywords: all words must be present (word-boundary each)
  if (keyword.includes(" ")) {
    return keyword.split(/\s+/).every((word) => wordMatch(text, word));
  }
  let re = regexCache.get(keyword);
  if (!re) {
    const escaped = keyword.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    re = new RegExp(`\\b${escaped}\\b`, "i");
    // LRU eviction — prevent unbounded cache growth
    const MAX_CACHE_SIZE = 500;
    if (regexCache.size >= MAX_CACHE_SIZE) {
      const firstKey = regexCache.keys().next().value;
      regexCache.delete(firstKey);
    }
    regexCache.set(keyword, re);
  } else {
    // Cache hit — re-insert to update LRU ordering (move to end of Map insertion order)
    regexCache.delete(keyword);
    regexCache.set(keyword, re);
  }
  return re.test(text);
}

// ── Workspace Path Resolution ───────────────────────────────────────────

interface OpenClawPluginApiExtended extends OpenClawPluginApi {
  config?: {
    agents?: {
      defaults?: {
        workspace?: string;
      };
    };
  };
}

function resolveWorkspacePath(api: OpenClawPluginApi, ctx: { workspaceDir?: string }): string {
  return (
    ctx.workspaceDir ??
    (api as OpenClawPluginApiExtended).config?.agents?.defaults?.workspace ??
    '/home/pi/.openclaw/workspace'
  );
}

// ── Matching Logic ────────────────────────────────────────────────────

interface MatchOptions {
  mode: "auto" | "strict" | "lenient";
  minConfidence: number;
  maxResults: number;
}

function matchRules(
  rules: CorrelationRule[],
  query: string,
  options: Partial<MatchOptions> = {},
): MatchedRule[] {
  const { mode = "auto", minConfidence = 0, maxResults = 10 } = options;
  const matched: MatchedRule[] = [];
  const seenIds = new Set<string>();

  for (const rule of rules) {
    if (matched.length >= maxResults) break;
    const ruleId = rule.id || "unknown";
    if (seenIds.has(ruleId)) continue;

    // Confidence gate
    if (rule.confidence !== undefined && rule.confidence < minConfidence) continue;

    let isMatch = false;

    // Keyword matching with word boundaries (auto + strict)
    const keywords = getKeywords(rule);
    for (const kw of keywords) {
      if (wordMatch(query, kw)) {
        isMatch = true;
        break;
      }
    }

    // Context matching — normalize hyphens/underscores, partial word match (auto only)
    if (!isMatch && mode !== "strict") {
      const context = getContext(rule);
      if (context) {
        const ctxWords = context.replace(/[-_]/g, " ").toLowerCase().split(/\s+/).filter((w) => w.length > 0);
        const queryWords = new Set(
          query.toLowerCase().replace(/[^\w\s]/g, " ").split(/\s+/),
        );
        const matchingWords = ctxWords.filter((w) => queryWords.has(w));
        const coverage = ctxWords.length > 0 ? matchingWords.length / ctxWords.length : 0;
        isMatch = matchingWords.length >= 2 || coverage >= 0.8;
      }
    }

    if (isMatch) {
      seenIds.add(ruleId);
      matched.push({
        id: rule.id,
        context: getContext(rule),
        confidence: rule.confidence,
        relationship_type: rule.relationship_type,
        additional_searches: getAdditionalSearches(rule),
      });
    }
  }

  // Lenient fallback: fuzzy word matching if nothing matched
  if (mode === "lenient" && matched.length === 0) {
    const queryWords = query
      .toLowerCase()
      .replace(/[^\w\s]/g, " ")
      .split(/\s+/)
      .filter((w) => w.length > 2);

    for (const rule of rules) {
      if (matched.length >= maxResults) break;
      const ruleId = rule.id || "unknown";
      if (seenIds.has(ruleId)) continue;

      // Confidence gate
      if (rule.confidence !== undefined && rule.confidence < minConfidence) continue;

      const ruleText = [
        getContext(rule),
        ...getKeywords(rule),
        ...getAdditionalSearches(rule),
      ]
        .join(" ")
        .toLowerCase();

      for (const word of queryWords) {
        if (ruleText.includes(word)) {
          seenIds.add(ruleId);
          matched.push({
            id: rule.id,
            context: getContext(rule),
            confidence: rule.confidence,
            relationship_type: rule.relationship_type,
            additional_searches: getAdditionalSearches(rule),
          });
          break;
        }
      }
    }
  }

  // Sort by confidence descending, then id ascending (stable tiebreak)
  matched.sort((a, b) => {
    const diff = (b.confidence ?? 0) - (a.confidence ?? 0);
    if (diff !== 0) return diff;
    return (a.id ?? "").localeCompare(b.id ?? "");
  });
  return matched.slice(0, maxResults);
}

// ── Plugin Registration ───────────────────────────────────────────────

const correlationMemoryPlugin = {
  id: "correlation-memory",
  name: "Correlation Memory Search",
  description:
    "Correlation-aware memory search — automatic decision-context retrieval with keyword matching, confidence filtering, and rule lifecycle management",
  kind: "memory",
  configSchema: emptyPluginConfigSchema(),

  register(api: OpenClawPluginApi) {
    api.registerTool(
      (ctx) => {
        // Resolve workspace path — ctx.workspaceDir is set by the SDK runtime
        const workspacePath = resolveWorkspacePath(api, ctx);

        return [
          // ── Tool 1: memory_search_with_correlation ──
          {
            name: "memory_search_with_correlation",
            description:
              "Search memory with automatic correlation rule matching. " +
              "When you query a topic, this checks correlation rules and suggests " +
              "additional searches for related contexts that typically matter together. " +
              'Example: "backup error" also retrieves "last backup time" and "recovery procedures".',
            parameters: {
              type: "object" as const,
              properties: {
                query: {
                  type: "string",
                  description: "The search query to find relevant memories",
                },
                auto_correlate: {
                  type: "boolean",
                  description:
                    "Automatically check correlation rules (default: true)",
                  default: true,
                },
                correlation_mode: {
                  type: "string",
                  enum: ["auto", "strict", "lenient"],
                  description:
                    "Matching mode: auto (keyword + context), strict (word-boundary keyword), lenient (fuzzy fallback)",
                  default: "auto",
                },
                min_confidence: {
                  type: "number",
                  description: "Minimum confidence threshold (0-1, default: 0)",
                  default: 0,
                },
                max_results: {
                  type: "number",
                  description: "Maximum number of rules to return (default: 10)",
                  default: 10,
                },
              },
              required: ["query"],
            },
            execute: async (params: {
              query: string;
              auto_correlate?: boolean;
              correlation_mode?: "auto" | "strict" | "lenient";
              min_confidence?: number;
              max_results?: number;
            }) => {
              const {
                query,
                auto_correlate = true,
                correlation_mode = "auto",
                min_confidence = 0,
                max_results = 10,
              } = params;

              // Validate numeric params — prevent NaN or out-of-range values
              const safeMaxResults = Math.max(1, Math.floor(max_results ?? 10));
              const safeMinConfidence = Math.min(1, Math.max(0, min_confidence ?? 0));

              const rules = loadCorrelationRules(workspacePath);

              if (rules.length === 0) {
                return {
                  success: true,
                  query,
                  matched_rules: [],
                  suggested_additional_searches: [],
                  summary: "No correlation rules loaded.",
                };
              }

              const matched = auto_correlate
                ? matchRules(rules, query, { mode: correlation_mode, minConfidence: safeMinConfidence, maxResults: safeMaxResults })
                : [];

              const allSearches = matched.flatMap((r) => r.additional_searches);
              const uniqueSearches = [...new Set(allSearches)];

              const ruleIds = matched.map((r) => r.id).join(", ");

              return {
                success: true,
                query,
                correlation_mode,
                matched_rules: matched,
                suggested_additional_searches: uniqueSearches,
                summary:
                  matched.length === 0
                    ? `No correlation rules matched for "${query}".`
                    : `Matched ${matched.length} rule(s) [${ruleIds}]. ` +
                      `Additional searches: ${uniqueSearches.join(", ") || "none"}.`,
              };
            },
          },

          // ── Tool 2: correlation_check ──
          {
            name: "correlation_check",
            description:
              "Debug tool: check which correlation rules would match a given context without performing searches.",
            parameters: {
              type: "object" as const,
              properties: {
                context: {
                  type: "string",
                  description: "Context or query to check against rules",
                },
                mode: {
                  type: "string",
                  enum: ["auto", "strict", "lenient"],
                  description: "Matching mode",
                  default: "auto",
                },
                min_confidence: {
                  type: "number",
                  description: "Minimum confidence threshold (0-1, default: 0)",
                  default: 0,
                },
                max_results: {
                  type: "number",
                  description: "Maximum rules to return (default: 10)",
                  default: 10,
                },
              },
              required: ["context"],
            },
            execute: async (params: {
              context: string;
              mode?: "auto" | "strict" | "lenient";
              min_confidence?: number;
              max_results?: number;
            }) => {
              const { context, mode = "auto", min_confidence = 0, max_results = 10 } = params;

              // Validate numeric params
              const safeMaxResults = Math.max(1, Math.floor(max_results ?? 10));
              const safeMinConfidence = Math.min(1, Math.max(0, min_confidence ?? 0));

              const rules = loadCorrelationRules(workspacePath);
              const matched = matchRules(rules, context, { mode, minConfidence: safeMinConfidence, maxResults: safeMaxResults });

              return {
                success: true,
                context,
                mode,
                total_rules: rules.length,
                matched_count: matched.length,
                matching_rules: matched,
              };
            },
          },
        ];
      },
      { names: ["memory_search_with_correlation", "correlation_check"] },
    );
  },
};

export default correlationMemoryPlugin;
