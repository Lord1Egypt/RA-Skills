'use strict';

const fs = require('fs');
const path = require('path');
const os = require('os');
const readline = require('readline');
const lockfile = require('proper-lockfile');

// ─── Constants ────────────────────────────────────────────────────────────────

const PROVIDERS = Object.freeze({ GEMINI: 'gemini', BRAVE: 'brave' });
const VALID_PROVIDERS = [PROVIDERS.GEMINI, PROVIDERS.BRAVE];
const MAX_QUERY_LENGTH = 1000;
const MAX_PROVIDER_LENGTH = 32;      // cap forceProvider length before logging
const MAX_RESPONSE_SIZE = 10_000;    // characters; prevents flooding the model context window
const WEB_FETCH_MIN_DELAY_MS = 2000; // minimum gap between calls to the same engine

// Explicit allowlist — avoids relying on urlTemplates key lookup as implicit guard
const ALLOWED_ENGINES = Object.freeze(['google', 'bing', 'duckduckgo']);

// File paths — computed once at startup
const quotaPath = process.env.SEARCH_QUOTA_PATH ||
  path.join(os.homedir(), '.openclaw', 'workspace', 'shared', 'search-quota.json');
const logsDir = path.join(path.dirname(quotaPath), 'logs');

// Finance/time-sensitive keywords — module-level defaults; config may override via finance_keywords.
const DEFAULT_FINANCE_KEYWORDS = [
  'stock', 'share price', 'nse', 'bse', 'wse', 'nyse', 'nasdaq',
  'earnings', 'ipo', 'dividend', 'funding round', 'acquisition',
  'merger', 'valuation', 'competitor', 'market share', 'breaking',
  'just announced', 'today', 'hours ago', 'spearfox', 'fifthspear'
];

// Space/astronomy keywords for Brave routing — module-level defaults; config may override via brave_keywords.
const DEFAULT_BRAVE_KEYWORDS = ['space', 'astronomy', 'nasa', 'esa', 'cosmos'];

// Prompt injection patterns — stripped from all provider results before returning to the agent
const INJECTION_PATTERN =
  /ignore\s+(?:previous\s+)?instructions?|system\s+prompt|you\s+are\s+now\s+|forget\s+your\s+instructions?|new\s+instructions?|\[INST\]|<\|system\|>|<\|user\|>|<\|assistant\|>/gi;

// ─── Security helpers ─────────────────────────────────────────────────────────

// Returns false if the URL resolves to an RFC-1918 / loopback / link-local address.
// Defends against SSRF in case templates change or the harness follows redirects.
function isSafeUrl(url) {
  try {
    const { hostname, protocol } = new URL(url);
    if (protocol !== 'https:' && protocol !== 'http:') return false;
    const h = hostname.toLowerCase();
    if (h === 'localhost' || h === '::1' || h === '0.0.0.0') return false;
    if (/^127\./.test(h)) return false;                        // 127.0.0.0/8  loopback
    if (/^10\./.test(h)) return false;                         // 10.0.0.0/8   private
    if (/^192\.168\./.test(h)) return false;                   // 192.168.0.0/16 private
    if (/^169\.254\./.test(h)) return false;                   // 169.254.0.0/16 APIPA
    if (/^172\.(1[6-9]|2\d|3[01])\./.test(h)) return false;  // 172.16.0.0/12 private
    if (/^(fc|fd)[0-9a-f]{2}:/i.test(h)) return false;       // fc00::/7 IPv6 ULA
    return true;
  } catch {
    return false;
  }
}

// Strips common prompt-injection patterns from provider results before they
// reach the calling agent. Prevents search results from hijacking agent behaviour.
function stripInjection(text) {
  if (typeof text !== 'string') return text;
  return text.replace(INJECTION_PATTERN, '[REMOVED]');
}

// ─── Circuit breaker ──────────────────────────────────────────────────────────
// In-memory per-provider circuit breaker. Opens after CIRCUIT_THRESHOLD
// consecutive failures; auto-resets after CIRCUIT_RESET_MS. Prevents hammering
// a provider that is already down across multiple sequential calls.

const CIRCUIT_THRESHOLD = 3;
const CIRCUIT_RESET_MS  = 60_000;

const _circuit = {
  gemini: { failures: 0, openUntil: 0 },
  brave:  { failures: 0, openUntil: 0 }
};

function isCircuitOpen(provider) {
  const c = _circuit[provider];
  if (!c) return false;
  if (c.openUntil > Date.now()) return true;
  if (c.openUntil > 0) { c.failures = 0; c.openUntil = 0; } // auto-reset on expiry
  return false;
}

function recordProviderSuccess(provider) {
  if (_circuit[provider]) { _circuit[provider].failures = 0; _circuit[provider].openUntil = 0; }
}

function recordProviderFailure(provider) {
  const c = _circuit[provider];
  if (!c) return;
  c.failures += 1;
  if (c.failures >= CIRCUIT_THRESHOLD && c.openUntil === 0) {
    c.openUntil = Date.now() + CIRCUIT_RESET_MS;
    console.error(`[circuit] ${provider} circuit opened for ${CIRCUIT_RESET_MS / 1000}s after ${c.failures} failures.`);
  }
}

// ─── Retry utility ────────────────────────────────────────────────────────────
// Standalone exponential-backoff retry with jitter. maxAttempts, baseDelay, and
// maxDelay are all configurable — callers pass options from config so behaviour
// can be tuned without touching code. Non-retryable errors short-circuit immediately.

async function withRetry(fn, { maxAttempts = 3, baseDelay = 500, maxDelay = 8000 } = {}) {
  let lastErr;
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (err) {
      if (err.retryable === false) throw err;
      lastErr = err;
      if (attempt < maxAttempts) {
        const delay = Math.min(
          baseDelay * 2 ** (attempt - 1) + Math.floor(Math.random() * 200),
          maxDelay
        );
        console.error(`[retry] Attempt ${attempt}/${maxAttempts} failed: ${err.message}. Retrying in ${delay}ms.`);
        await new Promise(r => setTimeout(r, delay));
      }
    }
  }
  throw lastErr;
}

// ─── Default quota factory ────────────────────────────────────────────────────
// Produces minimal schema with no hardcoded agent names.
// reconcileConfig is the single source of truth for populating agent_allocations.
// Function (not constant) so the date is always fresh — avoids stale date if
// the process runs past midnight before the first quota file creation.

function makeDefaultQuota() {
  return {
    date: new Date().toISOString().slice(0, 10),
    providers: {
      gemini: { daily_limit: 0, remaining: 0, used: 0, shared_pool: 0 },
      brave:  { daily_limit: 0, remaining: 0, used: 0, shared_pool: 0 }
    },
    agent_allocations: {}
  };
}

// ─── Shared stdin reader ──────────────────────────────────────────────────────
// Single readline interface for the process lifetime. main() reads the first
// line (the command), callWebFetch reads subsequent lines (tool responses).
// Creating multiple readline interfaces on the same stdin causes buffering
// races where the second interface misses data consumed by the first.
//
// waiters holds {resolve, reject} pairs so pending reads can be rejected
// if stdin closes or errors — prevents the process hanging forever.

const _stdin = { rl: null, lines: [], waiters: [] };

function _initStdin() {
  if (_stdin.rl) return;
  _stdin.rl = readline.createInterface({ input: process.stdin, crlfDelay: Infinity });

  _stdin.rl.on('line', (line) => {
    if (_stdin.waiters.length > 0) {
      _stdin.waiters.shift().resolve(line);
    } else {
      _stdin.lines.push(line);
    }
  });

  // Reject all pending reads if stdin closes or errors — prevents hung process
  const _rejectAll = (err) => {
    for (const { reject } of _stdin.waiters.splice(0)) reject(err);
  };
  _stdin.rl.on('close', () => _rejectAll(new Error('stdin closed unexpectedly')));
  _stdin.rl.on('error', (err) => _rejectAll(err));
}

function readNextLine() {
  _initStdin();
  return new Promise((resolve, reject) => {
    if (_stdin.lines.length > 0) {
      resolve(_stdin.lines.shift());
    } else {
      _stdin.waiters.push({ resolve, reject });
    }
  });
}

// ─── Result factories ─────────────────────────────────────────────────────────

// Builds the web_fetch success result — avoids copy-pasting the same shape 3×
function makeWebFetchResult(result, engine, queriesRemaining) {
  return {
    results: result,
    provider_used: 'web_fetch',
    queries_remaining: queriesRemaining,
    quota_source: 'none',
    fallback_used: true,
    warning: 'Result retrieved via web scraping. Quality may be lower than API results.',
    web_fetch_engine: engine
  };
}

// Builds the API success result — avoids copy-pasting the same shape in
// executeScheduledSearch steps 1 and 2 (differ only in provider and isFallback)
function makeApiResult(results, provider, quota, agentId, source, isFallback) {
  const providerUsed = `${provider}_used`;
  return {
    results,
    provider_used: provider,
    queries_remaining: Math.max(
      0,
      quota.agent_allocations[agentId][provider] - (quota.agent_allocations[agentId][providerUsed] || 0)
    ),
    quota_source: source,
    fallback_used: isFallback,
    warning: null,
    web_fetch_engine: null,
    updatedQuota: quota
  };
}

// ─── Config ───────────────────────────────────────────────────────────────────

// reads openclaw.json, returns { geminiKey, braveKey, geminiModel, dailyLimits,
//   agentAllocations, financeKeywords, braveKeywords, defaultProvider,
//   strictAgents, retryMaxAttempts, retryBaseDelay }
function loadConfig() {
  const configPath = process.env.OPENCLAW_CONFIG_PATH ||
    path.join(os.homedir(), '.openclaw', 'openclaw.json');

  try {
    const raw = fs.readFileSync(configPath, 'utf8');
    const config = JSON.parse(raw);
    const skillCfg = config.skills?.['smart-search'] || {};
    return {
      geminiKey:        config.env?.GEMINI_API_KEY || null,
      braveKey:         config.env?.BRAVE_API_KEY  || null,
      geminiModel:      skillCfg.gemini_model || 'gemini-2.0-flash',
      dailyLimits: {
        gemini: skillCfg.providers?.gemini?.daily_limit ?? 0,
        brave:  skillCfg.providers?.brave?.daily_limit  ?? 0
      },
      agentAllocations: skillCfg.agent_allocations || {},
      financeKeywords:  skillCfg.finance_keywords  || DEFAULT_FINANCE_KEYWORDS,
      braveKeywords:    skillCfg.brave_keywords    || DEFAULT_BRAVE_KEYWORDS,
      defaultProvider:  VALID_PROVIDERS.includes(skillCfg.default_provider)
                          ? skillCfg.default_provider
                          : PROVIDERS.BRAVE,
      strictAgents:     skillCfg.strict_agents     ?? false,
      retryMaxAttempts: skillCfg.retry_max_attempts ?? 3,
      retryBaseDelay:   skillCfg.retry_base_delay   ?? 500
    };
  } catch (err) {
    console.error(`[config] Failed to load config: ${err.code || err.message}`);
    throw new Error('Cannot read openclaw.json. Check OPENCLAW_CONFIG_PATH.');
  }
}

// ─── Routing ──────────────────────────────────────────────────────────────────

// returns true if query matches finance/time-sensitive keywords
function isFinanceQuery(query, config) {
  const keywords = config?.financeKeywords || DEFAULT_FINANCE_KEYWORDS;
  const q = query.toLowerCase();
  return keywords.some(keyword => q.includes(keyword));
}

// returns "gemini" or "brave" based on keywords — falls back to config.defaultProvider
function routeToProvider(query, config) {
  if (isFinanceQuery(query, config)) return PROVIDERS.GEMINI;
  const keywords = config?.braveKeywords || DEFAULT_BRAVE_KEYWORDS;
  const q = query.toLowerCase();
  if (keywords.some(keyword => q.includes(keyword))) return PROVIDERS.BRAVE;
  return config?.defaultProvider || PROVIDERS.BRAVE;
}

// ─── Quota file I/O ───────────────────────────────────────────────────────────

// reads quota JSON file, returns quota object
async function loadQuota() {
  try { fs.mkdirSync(path.dirname(quotaPath), { recursive: true }); } catch (_) {}
  try { fs.mkdirSync(logsDir, { recursive: true }); } catch (_) {}

  // Read directly — avoids TOCTOU race from existsSync + readFileSync
  let raw;
  try {
    raw = fs.readFileSync(quotaPath, 'utf8');
  } catch (err) {
    if (err.code === 'ENOENT') {
      const fresh = makeDefaultQuota();
      fs.writeFileSync(quotaPath, JSON.stringify(fresh, null, 2));
      console.error('[quota] File not found. Created default.');
      return fresh;
    }
    throw err;
  }

  let parsed;
  try {
    parsed = JSON.parse(raw);
  } catch (_) {
    fs.unlinkSync(quotaPath);
    const fresh = makeDefaultQuota();
    fs.writeFileSync(quotaPath, JSON.stringify(fresh, null, 2));
    console.error('[quota] Corrupted. Reset to defaults.');
    return fresh;
  }

  // Migrate old single-used counter to per-provider counters
  for (const agentId in parsed.agent_allocations) {
    const agent = parsed.agent_allocations[agentId];
    if ('used' in agent && !('gemini_used' in agent)) {
      agent.gemini_used = agent.used;
      agent.brave_used = 0;
      delete agent.used;
      console.error(`[quota] Migrated agent ${agentId} to per-provider usage counters.`);
    }
  }

  // Integrity check — clamp any negative counters that could indicate file corruption
  for (const provider of VALID_PROVIDERS) {
    const p = parsed.providers?.[provider];
    if (p) {
      if (p.used        < 0) { p.used        = 0; console.error(`[quota] Clamped negative used for ${provider}.`); }
      if (p.remaining   < 0) { p.remaining   = 0; console.error(`[quota] Clamped negative remaining for ${provider}.`); }
      if (p.shared_pool < 0) { p.shared_pool = 0; console.error(`[quota] Clamped negative shared_pool for ${provider}.`); }
    }
  }
  for (const agentId in parsed.agent_allocations) {
    const a = parsed.agent_allocations[agentId];
    if ((a.gemini_used || 0) < 0) { a.gemini_used = 0; console.error(`[quota] Clamped negative gemini_used for ${agentId}.`); }
    if ((a.brave_used  || 0) < 0) { a.brave_used  = 0; console.error(`[quota] Clamped negative brave_used for ${agentId}.`); }
  }

  return parsed;
}

// writes quota object to file with lock
async function saveQuota(quota) {
  let release;
  try {
    release = await lockfile.lock(quotaPath, { retries: 3, minTimeout: 100, stale: 5000 });
  } catch (_) {
    throw new Error('Quota file is locked. Try again.');
  }
  try {
    fs.writeFileSync(quotaPath, JSON.stringify(quota, null, 2));
    console.error('[quota] Saved.');
  } finally {
    await release();
  }
}

// ─── Quota logic ──────────────────────────────────────────────────────────────

// resets quota counters if date has changed
function resetIfNewDay(quota, config) {
  const today = new Date().toISOString().slice(0, 10);
  if (quota.date === today) return quota;

  quota.date = today;
  for (const provider in quota.providers) {
    const limit = config.dailyLimits[provider] ?? quota.providers[provider].daily_limit;
    quota.providers[provider].daily_limit = limit;
    quota.providers[provider].remaining = limit;
    quota.providers[provider].used = 0;
    quota.providers[provider].shared_pool = 0;
  }
  for (const agentId in quota.agent_allocations) {
    quota.agent_allocations[agentId].gemini_used = 0;
    quota.agent_allocations[agentId].brave_used = 0;
    quota.agent_allocations[agentId].completed = false;
  }
  console.error(`[quota] Daily reset performed for ${today}`);
  return quota;
}

// syncs config allocations into quota file
function reconcileConfig(config, quota) {
  for (const provider of VALID_PROVIDERS) {
    if (config.dailyLimits[provider] !== quota.providers[provider].daily_limit) {
      quota.providers[provider].daily_limit = config.dailyLimits[provider];
      quota.providers[provider].remaining = Math.max(
        0, config.dailyLimits[provider] - quota.providers[provider].used
      );
      console.error(`[config] Daily limit for ${provider} updated to ${config.dailyLimits[provider]}`);
    }
  }
  for (const agentId in config.agentAllocations) {
    if (!(agentId in quota.agent_allocations)) {
      quota.agent_allocations[agentId] = {
        gemini: config.agentAllocations[agentId].gemini,
        brave:  config.agentAllocations[agentId].brave,
        gemini_used: 0,
        brave_used: 0,
        completed: false
      };
      console.error(`[config] New agent ${agentId} added to quota tracking`);
    } else if (
      config.agentAllocations[agentId].gemini !== quota.agent_allocations[agentId].gemini ||
      config.agentAllocations[agentId].brave  !== quota.agent_allocations[agentId].brave
    ) {
      quota.agent_allocations[agentId].gemini = config.agentAllocations[agentId].gemini;
      quota.agent_allocations[agentId].brave  = config.agentAllocations[agentId].brave;
      console.error(`[config] Allocation for ${agentId} updated to ${JSON.stringify(config.agentAllocations[agentId])}`);
    }
  }
  return quota;
}

// Ensures an agent entry exists in quota — extracted so getAvailableAllocation
// and deductFromQuota are not responsible for side effects independently.
function _ensureAgent(quota, agentId) {
  if (!(agentId in quota.agent_allocations)) {
    quota.agent_allocations[agentId] = { gemini: 5, brave: 0, gemini_used: 0, brave_used: 0, completed: false };
    console.error(`[quota] Unknown agent ${agentId} added with default allocation.`);
  }
}

// returns available quota — { source, amount }
// Pure inspection: does NOT mutate quota. Call _ensureAgent first if needed.
function getAvailableAllocation(quota, agentId, provider) {
  if (!(agentId in quota.agent_allocations)) {
    return { source: 'none', amount: 0 };
  }

  const agent = quota.agent_allocations[agentId];
  const providerUsed = `${provider}_used`;
  const agentRemaining = agent[provider] - (agent[providerUsed] || 0);
  if (agentRemaining > 0) return { source: 'agent_allocation', amount: agentRemaining };

  if (quota.providers[provider].shared_pool > 0)
    return { source: 'shared_pool', amount: quota.providers[provider].shared_pool };

  if (quota.providers[provider].remaining > 0)
    return { source: 'provider_direct', amount: quota.providers[provider].remaining };

  return { source: 'none', amount: 0 };
}

// deducts one unit from the correct source, returns updated quota
function deductFromQuota(quota, agentId, provider, source) {
  _ensureAgent(quota, agentId); // guarantees agent exists before writing
  const providerUsed = `${provider}_used`;
  if (source === 'agent_allocation') quota.agent_allocations[agentId][providerUsed] += 1;
  if (source === 'shared_pool') quota.providers[provider].shared_pool -= 1;
  return quota;
}

// ─── API providers ────────────────────────────────────────────────────────────

// calls Gemini API, returns sanitised result string
async function callGemini(query, config) {
  if (!config.geminiKey) {
    const err = new Error('GEMINI_API_KEY is not configured in openclaw.json.');
    err.retryable = false;
    throw err;
  }

  const endpoint = `https://generativelanguage.googleapis.com/v1beta/models/${config.geminiModel}:generateContent?key=${config.geminiKey}`;
  const body = {
    tools: [{ google_search: {} }],
    contents: [{ parts: [{ text: query }] }]
  };

  let response;
  try {
    response = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(15000)
    });
  } catch (err) {
    err.retryable = true;
    throw err;
  }

  if (response.status === 404) {
    const err = new Error(`Gemini model ${config.geminiModel} is unavailable. Update gemini_model in openclaw.json.`);
    err.retryable = false;
    throw err;
  }
  if (response.status >= 400 && response.status < 500 && response.status !== 429) {
    const err = new Error(`Gemini API error: ${response.status}`);
    err.retryable = false;
    throw err;
  }
  if (!response.ok) {
    const err = new Error(`Gemini API error: ${response.status}`);
    err.retryable = true;
    throw err;
  }

  const data = await response.json();
  const answer = data.candidates?.[0]?.content?.parts?.[0]?.text;
  if (!answer) throw new Error('Gemini returned an empty response.');
  return stripInjection(answer);
}

// calls Brave API, returns sanitised results array
async function callBrave(query, config) {
  if (!config.braveKey) {
    const err = new Error('Brave Search is not configured. Add BRAVE_API_KEY to openclaw.json to enable it.');
    err.retryable = false;
    throw err;
  }

  const encoded = encodeURIComponent(query);
  const endpoint = `https://api.search.brave.com/res/v1/web/search?q=${encoded}`;

  let response;
  try {
    response = await fetch(endpoint, {
      method: 'GET',
      headers: { 'X-Subscription-Token': config.braveKey },
      signal: AbortSignal.timeout(15000)
    });
  } catch (err) {
    err.retryable = true;
    throw err;
  }

  if (response.status >= 400 && response.status < 500 && response.status !== 429) {
    const err = new Error(`Brave API error: ${response.status}`);
    err.retryable = false;
    throw err;
  }
  if (!response.ok) {
    const err = new Error(`Brave API error: ${response.status}`);
    err.retryable = true;
    throw err;
  }

  const data = await response.json();
  const results = data.web?.results;
  if (!results || !Array.isArray(results) || results.length === 0) {
    throw new Error('Brave returned no results.');
  }
  return results.map(r => ({
    title:       stripInjection(r.title),
    url:         r.url,
    description: stripInjection(r.description)
  }));
}

// Rate-limit tracker — enforces WEB_FETCH_MIN_DELAY_MS between calls per engine
const _lastWebFetch = {};

// calls OpenClaw web_fetch tool via shared stdin/stdout protocol, returns sanitised text
async function callWebFetch(query, engine) {
  // Explicit allowlist check — defence-in-depth beyond the urlTemplates key guard
  if (!ALLOWED_ENGINES.includes(engine)) {
    throw new Error(`Unknown web_fetch engine: ${engine}`);
  }

  const urlTemplates = {
    google:     `https://www.google.com/search?q=${encodeURIComponent(query)}`,
    bing:       `https://www.bing.com/search?q=${encodeURIComponent(query)}`,
    duckduckgo: `https://duckduckgo.com/html/?q=${encodeURIComponent(query)}`
  };

  const url = urlTemplates[engine];

  // SSRF guard — validates the target URL is not an internal/private address
  if (!isSafeUrl(url)) {
    throw new Error(`Blocked unsafe URL for engine: ${engine}`);
  }

  // Rate limiting — enforce minimum gap between calls to the same engine
  const now = Date.now();
  const elapsed = now - (_lastWebFetch[engine] || 0);
  if (elapsed < WEB_FETCH_MIN_DELAY_MS) {
    const wait = WEB_FETCH_MIN_DELAY_MS - elapsed;
    console.error(`[smart-search] Rate limiting ${engine}: waiting ${wait}ms`);
    await new Promise(r => setTimeout(r, wait));
  }
  _lastWebFetch[engine] = Date.now();

  console.error(`[smart-search] web_fetch using ${engine}: ${url}`);
  process.stdout.write(JSON.stringify({ tool: 'web_fetch', args: { url } }) + '\n');

  const line = await readNextLine();
  let parsed;
  try {
    parsed = JSON.parse(line);
  } catch (_) {
    throw new Error(`web_fetch returned invalid JSON for engine: ${engine}`);
  }
  if (!parsed.result) throw new Error(`web_fetch returned empty result for engine: ${engine}`);

  // Cap response size to prevent flooding the model context window
  let result = parsed.result;
  if (result.length > MAX_RESPONSE_SIZE) {
    result = result.slice(0, MAX_RESPONSE_SIZE) + '\n[TRUNCATED]';
    console.error(`[smart-search] web_fetch response truncated to ${MAX_RESPONSE_SIZE} chars`);
  }

  return stripInjection(result);
}

// ─── Logging ──────────────────────────────────────────────────────────────────

// appends entry to daily .jsonl log file with 30-day retention
async function logSearch(entry) {
  try { fs.mkdirSync(logsDir, { recursive: true }); } catch (_) {}

  const today = new Date().toISOString().slice(0, 10);
  const logPath = path.join(logsDir, `search-${today}.jsonl`);

  const entryCopy = { ...entry };
  if (entryCopy.response_summary && entryCopy.response_summary.length > 500) {
    entryCopy.response_summary = entryCopy.response_summary.slice(0, 500);
  }

  fs.appendFileSync(logPath, JSON.stringify(entryCopy) + '\n');

  // Retention cleanup — uses filename date, not filesystem mtime
  try {
    const todayDate = new Date();
    for (const file of fs.readdirSync(logsDir)) {
      const match = file.match(/^search-(\d{4})-(\d{2})-(\d{2})\.jsonl$/);
      if (!match) continue;
      const fileDate = new Date(match[1], match[2] - 1, match[3]);
      const diffDays = Math.floor((todayDate - fileDate) / (1000 * 60 * 60 * 24));
      if (diffDays > 30) {
        fs.unlinkSync(path.join(logsDir, file));
        console.error(`[log] Deleted old log: ${file}`);
      }
    }
  } catch (_) {}
}

// ─── Search strategies ────────────────────────────────────────────────────────

// Strategy B: general agent — web_fetch first to preserve API quota, API as last resort
async function executeGeneralSearch(query, config, quota) {
  const agentAlloc = quota.agent_allocations['general'] || { gemini: 0, gemini_used: 0 };
  const queriesRemaining = Math.max(0, agentAlloc.gemini - (agentAlloc.gemini_used || 0));

  // Step 1: Try Google web_fetch
  try {
    const result = await callWebFetch(query, 'google');
    if (result) {
      console.error('[smart-search] Google web_fetch succeeded for general agent');
      return makeWebFetchResult(result, 'google', queriesRemaining);
    }
  } catch (err) {
    console.error(`[smart-search] Google web_fetch failed: ${err.message}`);
  }

  // Step 2: Try Bing web_fetch
  try {
    const result = await callWebFetch(query, 'bing');
    if (result) {
      console.error('[smart-search] Bing web_fetch succeeded for general agent');
      return makeWebFetchResult(result, 'bing', queriesRemaining);
    }
  } catch (err) {
    console.error(`[smart-search] Bing web_fetch failed: ${err.message}`);
  }

  // Step 3: Both web_fetch failed — fall back to API
  console.error('[smart-search] Both web_fetch failed for general agent, falling back to API');
  const provider = routeToProvider(query, config);

  if (isCircuitOpen(provider)) throw new Error(`${provider} circuit is open. Try again later.`);

  _ensureAgent(quota, 'general');
  const alloc = getAvailableAllocation(quota, 'general', provider);
  if (alloc.source === 'none') throw new Error('All search providers exhausted or unavailable.');

  let apiResult;
  try {
    apiResult = provider === PROVIDERS.GEMINI
      ? await callGemini(query, config)
      : await callBrave(query, config);
    recordProviderSuccess(provider);
  } catch (err) {
    recordProviderFailure(provider);
    // Log the real cause before throwing the generic caller-facing message
    console.error(`[smart-search] API fallback failed: ${err.message}`);
    throw new Error('All search providers exhausted or unavailable.');
  }

  quota = deductFromQuota(quota, 'general', provider, alloc.source);
  quota.providers[provider].remaining -= 1;
  quota.providers[provider].used += 1;

  return makeApiResult(apiResult, provider, quota, 'general', alloc.source, false);
}

// Strategy A: scheduled agents — API first, web_fetch DuckDuckGo as last resort
async function executeScheduledSearch(query, agentId, provider, config, quota) {
  const retryOptions = { maxAttempts: config.retryMaxAttempts, baseDelay: config.retryBaseDelay };

  // Wraps a provider call with circuit-breaker check, withRetry, and success/failure recording.
  const tryProvider = async (prov) => {
    if (isCircuitOpen(prov)) {
      const err = new Error(`${prov} circuit is open. Skipping.`);
      err.retryable = false;
      throw err;
    }
    try {
      const result = await withRetry(
        () => prov === PROVIDERS.GEMINI ? callGemini(query, config) : callBrave(query, config),
        retryOptions
      );
      recordProviderSuccess(prov);
      return result;
    } catch (err) {
      recordProviderFailure(prov);
      throw err;
    }
  };

  // Step 1: Try primary provider
  _ensureAgent(quota, agentId);
  const alloc = getAvailableAllocation(quota, agentId, provider);
  if (alloc.source !== 'none') {
    try {
      const result = await tryProvider(provider);
      quota = deductFromQuota(quota, agentId, provider, alloc.source);
      quota.providers[provider].remaining -= 1;
      quota.providers[provider].used += 1;
      return makeApiResult(result, provider, quota, agentId, alloc.source, false);
    } catch (err) {
      console.error(`[smart-search] Primary provider ${provider} failed: ${err.message}`);
    }
  }

  // Step 2: Try fallback provider
  const fallbackProvider = provider === PROVIDERS.GEMINI ? PROVIDERS.BRAVE : PROVIDERS.GEMINI;
  const fallbackAlloc = getAvailableAllocation(quota, agentId, fallbackProvider);
  if (fallbackAlloc.source !== 'none') {
    try {
      const result = await tryProvider(fallbackProvider);
      quota = deductFromQuota(quota, agentId, fallbackProvider, fallbackAlloc.source);
      quota.providers[fallbackProvider].remaining -= 1;
      quota.providers[fallbackProvider].used += 1;
      return makeApiResult(result, fallbackProvider, quota, agentId, fallbackAlloc.source, true);
    } catch (err) {
      console.error(`[smart-search] Fallback provider ${fallbackProvider} failed: ${err.message}`);
    }
  }

  // Step 3: web_fetch DuckDuckGo — blocked for finance queries
  if (isFinanceQuery(query, config)) {
    throw new Error(
      'Finance and time-sensitive queries require Gemini or Brave API. ' +
      'web_fetch fallback is not permitted for this query type.'
    );
  }

  try {
    const result = await callWebFetch(query, 'duckduckgo');
    if (result) {
      const wfResult = makeWebFetchResult(result, 'duckduckgo', 0);
      wfResult.updatedQuota = quota;
      return wfResult;
    }
  } catch (err) {
    console.error(`[smart-search] DuckDuckGo web_fetch failed: ${err.message}`);
  }

  // Step 4: Total failure
  throw new Error('All search providers exhausted or unavailable.');
}

// ─── Tool handlers ────────────────────────────────────────────────────────────

// marks agent done, releases unused quota to shared pool
async function searchMarkAgentComplete(agentId) {
  if (!agentId || !/^[a-z0-9-]+$/.test(agentId)) {
    return { error: 'agent_id must contain only lowercase letters, numbers, and hyphens.' };
  }
  const quota = await loadQuota();
  if (!(agentId in quota.agent_allocations)) {
    return { error: `Agent ${agentId} not found in quota.` };
  }

  const agent = quota.agent_allocations[agentId];

  // Guard against double-release: a second call on the same day would release
  // the same remaining quota again, inflating the shared pool incorrectly.
  if (agent.completed) {
    return { error: `Agent ${agentId} is already marked complete for today.` };
  }

  const releasedGemini = Math.max(0, agent.gemini - (agent.gemini_used || 0));
  const releasedBrave  = Math.max(0, agent.brave  - (agent.brave_used  || 0));

  quota.providers.gemini.shared_pool += releasedGemini;
  quota.providers.brave.shared_pool  += releasedBrave;
  quota.agent_allocations[agentId].completed = true;

  await saveQuota(quota);

  return {
    agent_id: agentId,
    released: { gemini: releasedGemini, brave: releasedBrave },
    message: `Agent marked complete. ${releasedGemini} Gemini calls released to shared pool.`
  };
}

// returns quota status for one agent or the full quota object
async function searchQuotaStatus(agentId) {
  if (agentId && !/^[a-z0-9-]+$/.test(agentId)) {
    return { error: 'agent_id must contain only lowercase letters, numbers, and hyphens.' };
  }
  const quota = await loadQuota();

  if (!agentId) return quota;

  if (!(agentId in quota.agent_allocations)) {
    return { error: `Agent ${agentId} not found.` };
  }

  const agent = quota.agent_allocations[agentId];
  const geminiUsed = agent.gemini_used || 0;
  const braveUsed  = agent.brave_used  || 0;
  return {
    agent_id: agentId,
    gemini: {
      allocated: agent.gemini,
      used: geminiUsed,
      remaining: Math.max(0, agent.gemini - geminiUsed)
    },
    brave: {
      allocated: agent.brave,
      used: braveUsed,
      remaining: Math.max(0, agent.brave - braveUsed)
    },
    completed: agent.completed
  };
}

// main tool: validates input, detects strategy, executes search, logs, returns result
async function smartSearch(query, agentId, forceProvider) {
  // Input validation — fail fast with clean errors instead of crashing mid-execution
  if (!query || typeof query !== 'string' || query.trim() === '') {
    return { error: 'query is required and must be a non-empty string.' };
  }
  if (query.length > MAX_QUERY_LENGTH) {
    return { error: `query exceeds maximum length of ${MAX_QUERY_LENGTH} characters.` };
  }
  // Reject control characters (null bytes etc.) that could corrupt logs or downstream systems
  if (/[\x00-\x08\x0b\x0c\x0e-\x1f]/.test(query)) {
    return { error: 'query contains invalid control characters.' };
  }
  if (!agentId || typeof agentId !== 'string') {
    return { error: 'agent_id is required and must be a non-empty string.' };
  }
  // Sanitize agentId — prevents arbitrary strings flowing into console interpolations
  if (!/^[a-z0-9-]+$/.test(agentId)) {
    return { error: 'agent_id must contain only lowercase letters, numbers, and hyphens.' };
  }

  let config;
  try {
    config = loadConfig();
  } catch (err) {
    return { error: err.message };
  }

  // Strict agent mode — reject agents not defined in config to prevent quota drift
  if (config.strictAgents && agentId !== 'general' && !(agentId in config.agentAllocations)) {
    return { error: `Unknown agent: "${agentId}". Add it to openclaw.json to use it.` };
  }

  let quota = await loadQuota();
  quota = resetIfNewDay(quota, config);
  quota = reconcileConfig(config, quota);
  await saveQuota(quota);

  if (forceProvider) {
    // Cap before logging to prevent log injection via a long forceProvider string
    const fp = String(forceProvider).slice(0, MAX_PROVIDER_LENGTH);
    if (!VALID_PROVIDERS.includes(fp)) {
      const hint = fp === 'perplexity' ? 'Perplexity is not yet implemented.' : 'Use "gemini" or "brave".';
      return { error: `Invalid force_provider: "${fp}". ${hint}` };
    }
  }

  const provider = forceProvider || routeToProvider(query, config);
  console.error(`[smart-search] Routing "${query.slice(0, 50)}" to ${provider}`);

  let result;
  try {
    if (agentId === 'general' && !forceProvider) {
      result = await executeGeneralSearch(query, config, quota);
    } else {
      result = await executeScheduledSearch(query, agentId, provider, config, quota);
    }
    if (result.updatedQuota) {
      await saveQuota(result.updatedQuota);
      delete result.updatedQuota;
    }
  } catch (err) {
    result = {
      results: null,
      provider_used: null,
      queries_remaining: 0,
      quota_source: 'none',
      fallback_used: false,
      warning: null,
      web_fetch_engine: null,
      error: err.message
    };
  }

  const entry = {
    timestamp: new Date().toISOString(),
    agent_id: agentId,
    query: query,
    provider_used: result.provider_used || null,
    force_provider: forceProvider || null,
    quota_source: result.quota_source || 'none',
    queries_remaining: result.queries_remaining ?? 0,
    success: !result.error,
    response_summary: result.results ? String(result.results).slice(0, 500) : null,
    error: result.error || null,
    fallback_used: result.fallback_used || false,
    web_fetch_engine: result.web_fetch_engine || null
  };

  // Log failure must never swallow the search result
  try {
    await logSearch(entry);
  } catch (err) {
    console.error(`[smart-search] logSearch failed (result preserved): ${err.message}`);
  }

  return result;
}

// ─── Entry point ──────────────────────────────────────────────────────────────

// reads stdin (one JSON line), routes to correct tool, writes result to stdout
async function main() {
  try {
    const line = await readNextLine();

    let parsed;
    try {
      parsed = JSON.parse(line);
    } catch (_) {
      process.stdout.write(JSON.stringify({ error: 'Invalid JSON input.' }) + '\n');
      return;
    }

    const { tool, args = {} } = parsed;
    let result;

    if (tool === 'smart_search') {
      result = await smartSearch(args.query, args.agent_id, args.force_provider || null);
    } else if (tool === 'search_quota_status') {
      result = await searchQuotaStatus(args.agent_id || null);
    } else if (tool === 'search_mark_agent_complete') {
      result = await searchMarkAgentComplete(args.agent_id);
    } else {
      result = { error: `Unknown tool: ${tool}` };
    }

    process.stdout.write(JSON.stringify(result) + '\n');
  } catch (err) {
    process.stdout.write(JSON.stringify({ error: err.message }) + '\n');
  }
}

// ─── Process-level error guards ───────────────────────────────────────────────
// Prevent silent process hangs if an unhandled rejection or exception escapes main().
// Writes a clean JSON error to stdout so the harness always receives a valid response.

process.on('uncaughtException', (err) => {
  console.error(`[fatal] Uncaught exception: ${err.message}`);
  try { process.stdout.write(JSON.stringify({ error: 'Internal error.' }) + '\n'); } catch (_) {}
  process.exit(1);
});

process.on('unhandledRejection', (reason) => {
  console.error(`[fatal] Unhandled rejection: ${reason instanceof Error ? reason.message : reason}`);
  try { process.stdout.write(JSON.stringify({ error: 'Internal error.' }) + '\n'); } catch (_) {}
  process.exit(1);
});

// ─── Exports (for unit testing) ───────────────────────────────────────────────

module.exports = {
  loadConfig, isFinanceQuery, routeToProvider,
  loadQuota, saveQuota, resetIfNewDay, reconcileConfig,
  getAvailableAllocation, deductFromQuota,
  callGemini, callBrave, callWebFetch,
  logSearch, executeGeneralSearch, executeScheduledSearch,
  searchMarkAgentComplete, searchQuotaStatus, smartSearch, main,
  // Exported for unit testing
  withRetry, isCircuitOpen, recordProviderSuccess, recordProviderFailure, _circuit,
  isSafeUrl, stripInjection
};

// Run when invoked directly — guard prevents main() firing on require('./index')
if (require.main === module) {
  main();
}
