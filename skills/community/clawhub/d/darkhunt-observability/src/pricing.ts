// Bedrock model resolution and cost calculation
// Pricing last verified: 2026-03-13
// Sources: aws.amazon.com/bedrock/pricing, pricepertoken.com/endpoints/bedrock

// ── Types ───────────────────────────────────────────────────────────

export interface ModelPricing {
  inputPer1M: number;
  outputPer1M: number;
  cacheReadPer1M?: number;
  cacheWritePer1M?: number;
}

export interface ResolvedModel {
  friendlyName: string;
  rawModel: string;
  region?: string;
  pricing?: ModelPricing;
}

export interface CostBreakdown {
  total: number;
  input: number;
  output: number;
  cacheRead?: number;
  cacheWrite?: number;
}

// Same shape as PluginConfig.model_pricing — single type, no conversion needed
export type ConfigPricing = Record<string, { input: number; output: number; cacheRead?: number; cacheWrite?: number }>;

// ── Built-in pricing table (per 1M tokens, USD) ────────────────────

/** Anthropic prompt caching: 10% of input for reads, 125% of input for writes */
function withAnthropicCache(inputPer1M: number, outputPer1M: number): ModelPricing {
  return {
    inputPer1M,
    outputPer1M,
    cacheReadPer1M: inputPer1M * 0.1,
    cacheWritePer1M: inputPer1M * 1.25,
  };
}

const BEDROCK_PRICING = new Map<string, ModelPricing>([
  // ── Anthropic Claude ──────────────────────────────────────────
  ['claude-sonnet-4-6',            withAnthropicCache(3.00, 15.00)],
  ['claude-sonnet-4-20250514',     withAnthropicCache(3.00, 15.00)],
  ['claude-sonnet-4',              withAnthropicCache(3.00, 15.00)],
  ['claude-opus-4-6',              withAnthropicCache(5.00, 25.00)],
  ['claude-opus-4',                withAnthropicCache(15.00, 75.00)],
  ['claude-haiku-4-5',             withAnthropicCache(0.80, 4.00)],
  ['claude-haiku-4-5:eu-west-1',   withAnthropicCache(1.00, 5.00)],
  ['claude-3-5-sonnet',            withAnthropicCache(3.00, 15.00)],
  ['claude-3-sonnet',              withAnthropicCache(3.00, 15.00)],
  ['claude-3-haiku',               withAnthropicCache(0.25, 1.25)],
  ['claude-3-opus',                withAnthropicCache(15.00, 75.00)],

  // ── Amazon Nova ───────────────────────────────────────────────
  ['nova-micro',    { inputPer1M: 0.035, outputPer1M: 0.14 }],
  ['nova-lite',     { inputPer1M: 0.06,  outputPer1M: 0.24 }],
  ['nova-pro',      { inputPer1M: 0.80,  outputPer1M: 3.20 }],
  ['nova-premier',  { inputPer1M: 2.40,  outputPer1M: 9.60 }],

  // ── Meta Llama ────────────────────────────────────────────────
  ['llama3-2-1b',   { inputPer1M: 0.10, outputPer1M: 0.10 }],
  ['llama3-2-3b',   { inputPer1M: 0.15, outputPer1M: 0.15 }],
  ['llama3-2-11b',  { inputPer1M: 0.35, outputPer1M: 0.35 }],
  ['llama3-2-90b',  { inputPer1M: 2.00, outputPer1M: 2.00 }],
  ['llama3-3-70b',  { inputPer1M: 2.00, outputPer1M: 2.00 }],

  // ── Mistral ───────────────────────────────────────────────────
  ['mistral-7b',    { inputPer1M: 0.15, outputPer1M: 0.20 }],
  ['mixtral-8x7b',  { inputPer1M: 0.45, outputPer1M: 0.70 }],
  ['mistral-large', { inputPer1M: 8.00, outputPer1M: 24.00 }],

  // ── Cohere ────────────────────────────────────────────────────
  ['command-r-plus', { inputPer1M: 2.50, outputPer1M: 10.00 }],
  ['command-r',      { inputPer1M: 0.50, outputPer1M: 1.50 }],
]);

// ── Known model name patterns in Bedrock ARNs ──────────────────────
// Maps regex patterns found in ARN model IDs to friendly names
const ARN_MODEL_PATTERNS: [RegExp, string][] = [
  [/anthropic\.claude-sonnet-4-6/i,              'claude-sonnet-4-6'],
  [/anthropic\.claude-sonnet-4-20250514/i,       'claude-sonnet-4-20250514'],
  [/anthropic\.claude-sonnet-4(?![\d-])/i,       'claude-sonnet-4'],
  [/anthropic\.claude-opus-4-6/i,                'claude-opus-4-6'],
  [/anthropic\.claude-opus-4(?![\d-])/i,         'claude-opus-4'],
  [/anthropic\.claude-haiku-4-5/i,               'claude-haiku-4-5'],
  [/anthropic\.claude-3-5-sonnet/i,              'claude-3-5-sonnet'],
  [/anthropic\.claude-3-sonnet/i,                'claude-3-sonnet'],
  [/anthropic\.claude-3-haiku/i,                 'claude-3-haiku'],
  [/anthropic\.claude-3-opus/i,                  'claude-3-opus'],
  [/amazon\.nova-micro/i,                        'nova-micro'],
  [/amazon\.nova-lite/i,                         'nova-lite'],
  [/amazon\.nova-pro/i,                          'nova-pro'],
  [/amazon\.nova-premier/i,                      'nova-premier'],
  [/meta\.llama3-3-70b/i,                        'llama3-3-70b'],
  [/meta\.llama3-2-90b/i,                        'llama3-2-90b'],
  [/meta\.llama3-2-11b/i,                        'llama3-2-11b'],
  [/meta\.llama3-2-3b/i,                         'llama3-2-3b'],
  [/meta\.llama3-2-1b/i,                         'llama3-2-1b'],
  [/mistral\.mistral-large/i,                    'mistral-large'],
  [/mistral\.mixtral-8x7b/i,                     'mixtral-8x7b'],
  [/mistral\.mistral-7b/i,                       'mistral-7b'],
  [/cohere\.command-r-plus/i,                    'command-r-plus'],
  [/cohere\.command-r(?!-)/i,                    'command-r'],
];

// ── Resolution cache ────────────────────────────────────────────────
// Bounded to prevent unbounded growth. In practice there are <50 unique
// models per deployment, but we cap at 500 as a safety valve.
const CACHE_MAX_SIZE = 500;
const resolveCache = new Map<string, ResolvedModel>();

/** Clear the resolution cache (for testing or after config reload) */
export function clearResolveCache(): void {
  resolveCache.clear();
}

// ── Model resolution ────────────────────────────────────────────────

export function resolveModel(
  rawModel: string,
  modelMap?: Record<string, string>,
  configPricing?: ConfigPricing,
): ResolvedModel {
  if (!rawModel) {
    return { friendlyName: '', rawModel: '' };
  }

  // Cache keyed by rawModel. modelMap and configPricing are stable per
  // plugin lifetime (set once in register(), passed as closures).
  const cached = resolveCache.get(rawModel);
  if (cached) return cached;

  let result: ResolvedModel;

  // Not a Bedrock ARN — try direct pricing lookup and return as-is
  if (!rawModel.includes('arn:aws:bedrock')) {
    const pricing = lookupPricing(rawModel, undefined, configPricing);
    result = { friendlyName: rawModel, rawModel, pricing };
  } else {
    // Extract region from ARN: arn:aws:bedrock:{region}:{accountId}:...
    const arnParts = rawModel.split(':');
    const region = arnParts.length >= 4 ? arnParts[3] : undefined;

    result = resolveFromArn(rawModel, region, modelMap, configPricing);
  }

  // Evict entire cache if it grows too large (simpler than LRU for <500 entries)
  if (resolveCache.size >= CACHE_MAX_SIZE) {
    resolveCache.clear();
  }
  resolveCache.set(rawModel, result);
  return result;
}

function resolveFromArn(
  rawModel: string,
  region: string | undefined,
  modelMap?: Record<string, string>,
  configPricing?: ConfigPricing,
): ResolvedModel {
  // 1. Check user's model_map — longest key match wins to avoid
  //    short keys (e.g. "claude") accidentally matching unrelated ARNs
  if (modelMap) {
    const sorted = Object.entries(modelMap).sort((a, b) => b[0].length - a[0].length);
    for (const [pattern, friendlyName] of sorted) {
      if (rawModel.includes(pattern)) {
        const pricing = lookupPricing(friendlyName, region, configPricing);
        return { friendlyName, rawModel, region, pricing };
      }
    }
  }

  // 2. Try to extract known model name from the ARN itself
  for (const [regex, friendlyName] of ARN_MODEL_PATTERNS) {
    if (regex.test(rawModel)) {
      const pricing = lookupPricing(friendlyName, region, configPricing);
      return { friendlyName, rawModel, region, pricing };
    }
  }

  // 3. No match — return the raw ARN as-is (no pricing)
  return { friendlyName: rawModel, rawModel, region };
}

// ── Pricing lookup (region-aware) ───────────────────────────────────

function lookupPricing(modelName: string, region?: string, configPricing?: ConfigPricing): ModelPricing | undefined {
  // 1. Config pricing overrides take highest priority
  if (configPricing) {
    // Try region-specific key first
    if (region) {
      const regionEntry = configPricing[`${modelName}:${region}`];
      if (regionEntry) return configToModelPricing(regionEntry);
    }
    const entry = configPricing[modelName];
    if (entry) return configToModelPricing(entry);
  }

  // 2. Built-in pricing table
  if (region) {
    const regionKey = `${modelName}:${region}`;
    const regionPricing = BEDROCK_PRICING.get(regionKey);
    if (regionPricing) return regionPricing;
  }

  return BEDROCK_PRICING.get(modelName);
}

function configToModelPricing(entry: { input: number; output: number; cacheRead?: number; cacheWrite?: number }): ModelPricing {
  return {
    inputPer1M: entry.input,
    outputPer1M: entry.output,
    // Only set cache pricing when explicitly provided — don't assume Anthropic's
    // cache ratios apply to all models (Llama, Mistral, Nova have no prompt caching)
    ...(entry.cacheRead != null ? { cacheReadPer1M: entry.cacheRead } : {}),
    ...(entry.cacheWrite != null ? { cacheWritePer1M: entry.cacheWrite } : {}),
  };
}

// ── Cost fallback ───────────────────────────────────────────────────
// Single entry point for cost resolution, used by both hooks-adapter
// (traces) and log-hooks (logs) to avoid divergent cost logic.

export interface CostFallbackResult {
  costTotal?: number;
  costBreakdown?: CostBreakdown;
}

/**
 * Compute cost: use reportedCost if available, otherwise calculate from
 * token counts and model pricing.
 *
 * Token count assumption: inputTokens is the NON-CACHED input token count
 * (as reported by Anthropic/Bedrock). Cache read/write tokens are separate
 * fields. If a provider folds cached tokens into inputTokens, costs will be
 * slightly over-reported for cached requests.
 */
export function costFallback(
  reportedCost: number | undefined,
  pricing: ModelPricing | undefined,
  inputTokens: number,
  outputTokens: number,
  cacheReadTokens?: number,
  cacheWriteTokens?: number,
): CostFallbackResult {
  if (reportedCost != null && reportedCost > 0) {
    return { costTotal: reportedCost };
  }

  if (!pricing || (inputTokens <= 0 && outputTokens <= 0)) {
    return {};
  }

  const breakdown = calculateCost(inputTokens, outputTokens, pricing, cacheReadTokens, cacheWriteTokens);
  return { costTotal: breakdown.total, costBreakdown: breakdown };
}

// ── Cost calculation ────────────────────────────────────────────────

export function calculateCost(
  inputTokens: number,
  outputTokens: number,
  pricing: ModelPricing,
  cacheReadTokens?: number,
  cacheWriteTokens?: number,
): CostBreakdown {
  const input = (inputTokens / 1_000_000) * pricing.inputPer1M;
  const output = (outputTokens / 1_000_000) * pricing.outputPer1M;

  let cacheRead: number | undefined;
  if (cacheReadTokens != null && cacheReadTokens > 0 && pricing.cacheReadPer1M != null) {
    cacheRead = (cacheReadTokens / 1_000_000) * pricing.cacheReadPer1M;
  }

  let cacheWrite: number | undefined;
  if (cacheWriteTokens != null && cacheWriteTokens > 0 && pricing.cacheWritePer1M != null) {
    cacheWrite = (cacheWriteTokens / 1_000_000) * pricing.cacheWritePer1M;
  }

  const total = input + output + (cacheRead ?? 0) + (cacheWrite ?? 0);

  return {
    total: round6(total),
    input: round6(input),
    output: round6(output),
    ...(cacheRead != null ? { cacheRead: round6(cacheRead) } : {}),
    ...(cacheWrite != null ? { cacheWrite: round6(cacheWrite) } : {}),
  };
}

function round6(n: number): number {
  return Math.round(n * 1_000_000) / 1_000_000;
}

// ── Exports for wizard/CLI ───────────────────────────────────────────

/** Returns all built-in model names (keys from BEDROCK_PRICING). */
export function getBuiltinModelNames(): string[] {
  return Array.from(BEDROCK_PRICING.keys());
}

/** Returns built-in pricing for a model name (or undefined). */
export function getBuiltinPricing(modelName: string): ModelPricing | undefined {
  return BEDROCK_PRICING.get(modelName);
}
