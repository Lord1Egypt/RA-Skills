#!/usr/bin/env node
/**
 * API Gateway — Smart proxy for external API calls
 *
 * Modes:
 *   --call <provider> <endpoint> [body]     → Make API call with retry/caching
 *   --call --dry-run <provider> <endpoint>  → Preview call without executing
 *   --keys                                  → List configured API keys (masked)
 *   --keys add <provider> <key> [--allow-domain <domain>]...
 *                                            → Add API key with allowlist
 *   --keys remove <provider>                → Remove API key
 *   --cache                                 → Show cache status (metadata-only)
 *   --cache --clear                         → Clear cache
 *   --cache-full <provider>                 → Enable full-body caching for a provider
 *   --log                                   → Show request log (coarse)
 *   --log --clear                           → Clear request log
 *   --rate <provider>                       → Check rate limit status
 *   --fallback <provider> <fallback>        → Set fallback provider
 *   --status                                → Gateway status overview
 *   --retention <seconds>                   → Set default cache/log TTL
 *
 * Security model:
 *   - Plaintext API keys in keys.json with chmod 0600 (POSIX)
 *   - Strict domain allowlist per provider (NOT a string contains check)
 *   - Metadata-only response cache by default; full body caching is opt-in
 *   - Coarse request log: provider, path, status class, timestamp, attempt (no query strings)
 *   - Env var auto-detection: PROVIDER_API_KEY overrides disk storage
 *   - No outbound Authorization header unless the URL hostname matches the allowlist
 */

const fs = require('fs');
const path = require('path');
const http = require('http');
const https = require('https');
const os = require('os');

const WORKSPACE = (() => {
  if (process.env.API_GATEWAY_DIR) return process.env.API_GATEWAY_DIR;
  let dir = __dirname;
  for (let i = 0; i < 10; i++) {
    if (fs.existsSync(path.join(dir, 'MEMORY.md'))) return dir;
    dir = path.resolve(dir, '..');
  }
  return path.resolve(__dirname, '..', '..');
})();

const DATA_DIR = path.join(WORKSPACE, 'memory', 'api-gateway');
const KEYS_FILE = path.join(DATA_DIR, 'keys.json');
const FALLBACKS_FILE = path.join(DATA_DIR, 'fallbacks.json');
const CACHE_FILE = path.join(DATA_DIR, 'cache.json');
const RATE_FILE = path.join(DATA_DIR, 'rate-limits.json');
const LOG_FILE = path.join(DATA_DIR, 'request-log.json');
const CIRCUIT_FILE = path.join(DATA_DIR, 'circuit-state.json');
const FULL_CACHE_FILE = path.join(DATA_DIR, 'full-cache-providers.json');

const DEFAULT_CACHE_TTL_MS = 5 * 60 * 1000; // 5 minutes
const LOG_RETENTION_ENTRIES = 1000;
const CACHE_RETENTION_ENTRIES = 5000;

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function loadJSON(file, fallback) {
  try {
    const data = fs.readFileSync(file, 'utf8');
    return JSON.parse(data);
  } catch { return fallback || {}; }
}

function saveJSON(file, data) {
  ensureDir(path.dirname(file));
  // Atomic write: temp + rename, then chmod 0600 for sensitive files
  const tmp = file + '.tmp.' + process.pid + '.' + Date.now();
  fs.writeFileSync(tmp, JSON.stringify(data, null, 2), 'utf8');
  fs.renameSync(tmp, file);
  // Sensitive files: lock down permissions on POSIX
  if (process.platform !== 'win32' && (file === KEYS_FILE || file === LOG_FILE)) {
    try { fs.chmodSync(file, 0o600); } catch (e) { /* best-effort */ }
  }
}

function getToday() {
  return new Date().toISOString().split('T')[0];
}

function maskKey(key) {
  if (!key || key.length < 8) return '****';
  return key.substring(0, 4) + '****' + key.substring(key.length - 4);
}

// ─── PROVIDER ALLOWLIST (strict domain match) ─────────────────────────────

/**
 * Check whether the URL hostname matches any of the allowlist entries.
 * Allowlist entries can be:
 *   - exact hostnames: "api.openai.com"
 *   - wildcards: "*.anthropic.com" (matches api.anthropic.com but NOT anthropic.com)
 */
function hostnameMatchesAllowlist(hostname, allowlist) {
  if (!allowlist || allowlist.length === 0) return false;
  const h = hostname.toLowerCase();
  for (const entry of allowlist) {
    const e = entry.toLowerCase();
    if (e.startsWith('*.')) {
      // Wildcard: *.example.com matches foo.example.com but NOT example.com
      const suffix = e.slice(1); // ".example.com"
      if (h.endsWith(suffix) && h.length > suffix.length) return true;
    } else {
      if (h === e) return true;
    }
  }
  return false;
}

/**
 * Extract the hostname from a URL safely.
 */
function getHostname(url) {
  try {
    return new URL(url).hostname.toLowerCase();
  } catch {
    return '';
  }
}

/**
 * Decide whether to attach the Authorization header.
 * Requires:
 *   1. The provider has at least one allowlist entry
 *   2. The URL hostname matches that allowlist
 *
 * Returns { attach: bool, reason: string }.
 */
function shouldAttachAuth(provider, endpoint, keys) {
  const providerKey = keys[provider];
  if (!providerKey) {
    return { attach: false, reason: 'no_key' };
  }
  const allowlist = (typeof providerKey === 'object') ? (providerKey.allowDomains || []) : [];
  if (allowlist.length === 0) {
    return { attach: false, reason: 'no_allowlist' };
  }
  const hostname = getHostname(endpoint);
  if (!hostname) {
    return { attach: false, reason: 'invalid_url' };
  }
  if (!hostnameMatchesAllowlist(hostname, allowlist)) {
    return { attach: false, reason: 'hostname_not_in_allowlist' };
  }
  return { attach: true, reason: 'ok' };
}

/**
 * Resolve the actual key string for a provider.
 * Checks env var PROVIDER_API_KEY first, then stored key.
 */
function resolveKey(provider, keys) {
  const envKey = process.env[`${provider.toUpperCase()}_API_KEY`];
  if (envKey) {
    return { key: envKey, source: 'env' };
  }
  const stored = keys[provider];
  if (typeof stored === 'string') {
    return { key: stored, source: 'disk_legacy' };
  }
  if (stored && typeof stored === 'object' && stored.key) {
    return { key: stored.key, source: 'disk' };
  }
  return { key: null, source: null };
}

// ─── HTTP REQUEST ──────────────────────────────────────────────────────────

function makeRequest(url, method, headers, body, timeout = 30000) {
  return new Promise((resolve, reject) => {
    // SECURITY: enforce HTTPS. Plain HTTP can expose bearer tokens / API keys
    // on the wire, so we refuse non-https endpoints unless explicitly opted in.
    if (!url.startsWith('https://')) {
      if (process.env.API_GATEWAY_ALLOW_HTTP !== '1') {
        return reject(new Error(
          `[api-gateway] REFUSED non-HTTPS request to "${url}". ` +
          `API Gateway only sends requests over HTTPS to protect credentials. ` +
          `If you must call a plaintext endpoint, set API_GATEWAY_ALLOW_HTTP=1 (not recommended for any call that attaches a key).`
        ));
      }
      console.log(`[api-gateway] ⚠️  SECURITY WARNING: sending request over plain HTTP to "${url}" (API_GATEWAY_ALLOW_HTTP=1). Credentials are NOT encrypted on the wire.`);
    }
    const isHttps = url.startsWith('https');
    const client = isHttps ? https : http;
    
    const options = {
      hostname: new URL(url).hostname,
      port: new URL(url).port || (isHttps ? 443 : 80),
      path: new URL(url).pathname + new URL(url).search,
      method,
      headers: { 'Content-Type': 'application/json', ...headers },
      timeout
    };
    
    const req = client.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve({ status: res.statusCode, headers: res.headers, body: JSON.parse(data) });
        } catch {
          resolve({ status: res.statusCode, headers: res.headers, body: data });
        }
      });
    });
    
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('Request timeout')); });
    
    if (body && typeof body === 'object') req.write(JSON.stringify(body));
    req.end();
  });
}

// ─── CACHE (metadata-only by default) ─────────────────────────────────────

function getFullCacheProviders() {
  return loadJSON(FULL_CACHE_FILE, []);
}

function isFullCacheEnabled(provider) {
  return getFullCacheProviders().includes(provider);
}

function redactHeaders(headers) {
  // Strip authorization, cookies, and other credential headers from cached headers
  const safe = { ...headers };
  for (const k of Object.keys(safe)) {
    if (/^(authorization|cookie|set-cookie|x-api-key|x-auth|password|secret|token)$/i.test(k)) {
      safe[k] = '[REDACTED]';
    }
  }
  return safe;
}

function evictExpiredCache(cache, ttl) {
  const now = Date.now();
  for (const k of Object.keys(cache)) {
    if (cache[k].timestamp && (now - cache[k].timestamp) > ttl) {
      delete cache[k];
    }
  }
  return cache;
}

function capCacheSize(cache, maxEntries) {
  const keys = Object.keys(cache);
  if (keys.length <= maxEntries) return cache;
  // Evict oldest first
  keys.sort((a, b) => (cache[a].timestamp || 0) - (cache[b].timestamp || 0));
  const toRemove = keys.length - maxEntries;
  for (let i = 0; i < toRemove; i++) delete cache[keys[i]];
  return cache;
}

// ─── CIRCUIT BREAKER ─────────────────────────────────────────────────────

function getCircuitState(provider) {
  const state = loadJSON(CIRCUIT_FILE, {});
  const providerState = state[provider] || { state: 'CLOSED', failures: 0, lastFailure: null, cooldownUntil: null };
  
  if (providerState.state === 'OPEN' && providerState.cooldownUntil) {
    if (new Date(providerState.cooldownUntil) <= new Date()) {
      providerState.state = 'HALF-OPEN';
      providerState.failures = 0;
      saveJSON(CIRCUIT_FILE, state);
    }
  }
  
  return providerState;
}

function recordFailure(provider) {
  const state = loadJSON(CIRCUIT_FILE, {});
  const providerState = state[provider] || { state: 'CLOSED', failures: 0, lastFailure: null, cooldownUntil: null };
  
  providerState.failures++;
  providerState.lastFailure = new Date().toISOString();
  
  if (providerState.failures >= 5) {
    providerState.state = 'OPEN';
    providerState.cooldownUntil = new Date(Date.now() + 30000).toISOString();
    console.log(`[api-gateway] ⚠️ Circuit OPEN for ${provider} — ${providerState.failures} consecutive failures`);
  } else {
    console.log(`[api-gateway] Failure ${providerState.failures}/5 for ${provider}`);
  }
  
  state[provider] = providerState;
  saveJSON(CIRCUIT_FILE, state);
}

function recordSuccess(provider) {
  const state = loadJSON(CIRCUIT_FILE, {});
  const providerState = state[provider] || { state: 'CLOSED', failures: 0 };
  
  if (providerState.state === 'HALF-OPEN') {
    providerState.state = 'CLOSED';
    providerState.failures = 0;
    console.log(`[api-gateway] ✅ Circuit CLOSED for ${provider} (recovered)`);
  } else if (providerState.state === 'OPEN') {
    return;
  }
  
  providerState.failures = 0;
  state[provider] = providerState;
  saveJSON(CIRCUIT_FILE, state);
}

function getCircuitStatus() {
  const state = loadJSON(CIRCUIT_FILE, {});
  const entries = Object.entries(state);
  
  if (entries.length === 0) {
    console.log('[api-gateway] No circuit breaker state recorded.');
    return;
  }
  
  console.log('[api-gateway] Circuit breaker states:\n');
  for (const [provider, s] of entries) {
    const icon = s.state === 'CLOSED' ? '✅' : s.state === 'OPEN' ? '🔴' : '🟡';
    const cooldown = s.state === 'OPEN' && s.cooldownUntil 
      ? ` (cooldown until ${s.cooldownUntil})` 
      : '';
    console.log(`  ${icon} ${provider}: ${s.state}${cooldown} (${s.failures} failures)`);
  }
}

function resetCircuit(provider) {
  const state = loadJSON(CIRCUIT_FILE, {});
  if (!state[provider]) {
    console.log(`[api-gateway] No circuit state for: ${provider}`);
    return;
  }
  state[provider] = { state: 'CLOSED', failures: 0, lastFailure: null, cooldownUntil: null };
  saveJSON(CIRCUIT_FILE, state);
  console.log(`[api-gateway] ✅ Circuit reset for ${provider}`);
}

// ─── CALL ──────────────────────────────────────────────────────────────────

function stripQueryString(endpoint) {
  try {
    const u = new URL(endpoint);
    return u.origin + u.pathname;
  } catch {
    return endpoint;
  }
}

function statusClass(status) {
  if (status >= 200 && status < 300) return '2xx';
  if (status >= 300 && status < 400) return '3xx';
  if (status >= 400 && status < 500) return '4xx';
  if (status >= 500 && status < 600) return '5xx';
  return 'unknown';
}

async function makeCall(provider, endpoint, body = null, dryRun = false) {
  const circuitState = getCircuitState(provider);
  if (circuitState.state === 'OPEN') {
    console.log(`[api-gateway] 🔴 Circuit OPEN for ${provider} — skipping request`);
    return { error: `Circuit open for ${provider} — try again in ~30s` };
  }
  if (circuitState.state === 'HALF-OPEN') {
    console.log(`[api-gateway] 🟡 Circuit HALF-OPEN for ${provider} — testing`);
  }
  const keys = loadJSON(KEYS_FILE, {});
  const fallbacks = loadJSON(FALLBACKS_FILE, {});
  const cache = loadJSON(CACHE_FILE, {});
  const rateLimits = loadJSON(RATE_FILE, {});
  
  // Check rate limits (key is provider:pathname without query string)
  const pathOnly = stripQueryString(endpoint);
  const key = `${provider}:${pathOnly}`;
  if (rateLimits[key]) {
    const { resetAt, remaining } = rateLimits[key];
    if (new Date(resetAt) > new Date()) {
      if (remaining <= 0) {
        console.log(`[api-gateway] Rate limited: ${provider} — resets at ${resetAt}`);
        if (fallbacks[provider]) {
          console.log(`[api-gateway] Using fallback: ${fallbacks[provider]}`);
          return makeCall(fallbacks[provider], endpoint, body, dryRun);
        }
        return { error: 'Rate limited, no fallback available' };
      }
    }
  }
  
  // Check cache (key based on path only, not query)
  const cacheKey = `${provider}:${pathOnly}:${JSON.stringify(body || {})}`;
  if (cache[cacheKey]) {
    const { timestamp, response } = cache[cacheKey];
    if (Date.now() - timestamp < DEFAULT_CACHE_TTL_MS) {
      console.log(`[api-gateway] Cache hit: ${provider}:${pathOnly}`);
      return response;
    }
    delete cache[cacheKey];
    saveJSON(CACHE_FILE, cache);
  }
  
  // Resolve key (env var takes precedence)
  const { key: apiKey, source: keySource } = resolveKey(provider, keys);
  if (!apiKey) {
    console.log(`[api-gateway] No API key configured for: ${provider}`);
    return { error: `No API key for ${provider}` };
  }
  
  // Decide whether to attach auth (strict allowlist check)
  // Apply allowlist to ALL keys (env-var or disk-stored) for consistent security.
  let authDecision = shouldAttachAuth(provider, endpoint, keys);
  if (!authDecision.attach && keySource === 'env') {
    // Env-key present but allowlist doesn't match — warn but still refuse.
    // The user should add an allowlist entry or use env var for the specific provider they intend.
    authDecision = { attach: false, reason: 'hostname_not_in_allowlist (env key also refused)' };
  }
  let authHeader = '';
  if (authDecision.attach) {
    authHeader = `Bearer ${apiKey}`;
    const targetHost = (() => { try { return new URL(endpoint).hostname; } catch { return endpoint; } })();
    console.log(`[api-gateway] ⚠️  SECURITY WARNING: sending a Bearer credential for '${provider}' to host '${targetHost}'.`);
    console.log(`[api-gateway]    Confirm '${targetHost}' is the intended, allowlisted endpoint. The credential is NOT sent to any non-allowlisted host.`);
  } else if (keySource && keySource.startsWith('disk')) {
    // Disk-stored key but no allowlist match — fail-closed
    console.log(`[api-gateway] ⚠️ Refusing to attach stored key: ${authDecision.reason}`);
    console.log(`[api-gateway]    Add an allowlist entry: --keys add ${provider} <key> --allow-domain <hostname>`);
    return { error: `Allowlist check failed: ${authDecision.reason}. Use env var (${provider.toUpperCase()}_API_KEY) or update allowlist.` };
  } else if (!authDecision.attach) {
    console.log(`[api-gateway] Auth not attached: ${authDecision.reason}`);
  }
  
  // Dry run
  if (dryRun) {
    console.log(`[api-gateway] Would call: ${stripQueryString(endpoint)}`);
    console.log(`[api-gateway] Provider: ${provider}`);
    console.log(`[api-gateway] Key: ${maskKey(apiKey)} (source: ${keySource})`);
    console.log(`[api-gateway] Auth: ${authDecision.attach ? 'will attach' : 'will NOT attach (' + authDecision.reason + ')'}`);
    if (body) console.log(`[api-gateway] Body: ${JSON.stringify(body).substring(0, 200)}`);
    return { dryRun: true };
  }
  
  // Make the call with retry
  let lastError;
  const maxRetries = 3;
  
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const response = await makeRequest(endpoint, 'POST', {
        'Authorization': authHeader,
        'Content-Type': 'application/json'
      }, body);
      
      // Update rate limit tracking
      if (response.headers['x-ratelimit-remaining']) {
        rateLimits[key] = {
          remaining: parseInt(response.headers['x-ratelimit-remaining']),
          resetAt: new Date().toISOString()
        };
      }
      saveJSON(RATE_FILE, rateLimits);
      
      // Cache response: metadata-only by default, full body if opted-in
      const fullBody = isFullCacheEnabled(provider);
      const cacheEntry = fullBody
        ? { timestamp: Date.now(), response }
        : {
            timestamp: Date.now(),
            response: {
              status: response.status,
              headers: redactHeaders(response.headers),
              bodyLength: typeof response.body === 'string' ? response.body.length : JSON.stringify(response.body).length,
              bodyPreview: fullBody ? response.body : '[metadata-only: full body not cached. Use --cache-full ' + provider + ' to enable.]'
            }
          };
      cache[cacheKey] = cacheEntry;
      let pruned = evictExpiredCache(cache, DEFAULT_CACHE_TTL_MS);
      pruned = capCacheSize(pruned, CACHE_RETENTION_ENTRIES);
      saveJSON(CACHE_FILE, pruned);
      
      // Log request — coarse: provider, status class, timestamp, path (no query string)
      const log = loadJSON(LOG_FILE, []);
      log.push({
        timestamp: new Date().toISOString(),
        provider,
        statusClass: statusClass(response.status),
        attempt
      });
      if (log.length > LOG_RETENTION_ENTRIES) log.splice(0, log.length - LOG_RETENTION_ENTRIES);
      saveJSON(LOG_FILE, log);
      
      console.log(`[api-gateway] Success: ${provider} → ${pathOnly} (${response.status}, ${fullBody ? 'cached full' : 'cached metadata'})`);
      recordSuccess(provider);
      return response;
    } catch (err) {
      lastError = err;
      if (attempt < maxRetries) {
        console.log(`[api-gateway] Attempt ${attempt}/${maxRetries} failed: ${err.message}`);
        await new Promise(r => setTimeout(r, 1000 * attempt));
      } else {
        recordFailure(provider);
      }
    }
  }
  
  if (fallbacks[provider]) {
    console.log(`[api-gateway] All retries failed. Using fallback: ${fallbacks[provider]}`);
    return makeCall(fallbacks[provider], endpoint, body, dryRun);
  }
  
  console.log(`[api-gateway] Failed after ${maxRetries} attempts: ${lastError.message}`);
  return { error: lastError.message };
}

// ─── KEYS ──────────────────────────────────────────────────────────────────

function listKeys() {
  const keys = loadJSON(KEYS_FILE, {});
  const entries = Object.entries(keys);
  
  // Also detect env-var-only providers
  const envProviders = Object.keys(process.env)
    .filter(k => k.endsWith('_API_KEY') && process.env[k])
    .map(k => k.replace(/_API_KEY$/, '').toLowerCase());
  
  if (entries.length === 0 && envProviders.length === 0) {
    console.log('[api-gateway] No API keys configured (disk or env).');
    return;
  }
  
  console.log(`[api-gateway] Configured API keys:\n`);
  console.log(`${'Provider'.padEnd(25)} ${'Key'.padEnd(25)} ${'Source'.padEnd(12)} ${'Allowlist'.padEnd(30)}`);
  console.log('-'.repeat(95));
  
  for (const [provider, stored] of entries) {
    let keyStr, allowStr;
    if (typeof stored === 'string') {
      keyStr = maskKey(stored);
      allowStr = '⚠️  none (legacy)';
    } else {
      keyStr = maskKey(stored.key);
      const domains = stored.allowDomains || [];
      allowStr = domains.length > 0 ? domains.join(', ') : '⚠️  none';
    }
    console.log(`${provider.padEnd(25)} ${keyStr.padEnd(25)} disk        ${allowStr}`);
  }
  
  for (const p of envProviders) {
    if (entries[p]) continue; // already shown
    console.log(`${p.padEnd(25)} ${maskKey(process.env[`${p.toUpperCase()}_API_KEY`] || '').padEnd(25)} env         (no disk; still requires a matching allowlist at call time)`);
  }
}

function addKey(provider, key, allowDomains) {
  const keys = loadJSON(KEYS_FILE, {});
  keys[provider] = {
    key,
    allowDomains: allowDomains || [],
    addedAt: new Date().toISOString()
  };
  saveJSON(KEYS_FILE, keys);
  // Explicit user warning: keys are stored in PLAINTEXT on disk (chmod 0600).
  console.log(`[api-gateway] ⚠️  SECURITY WARNING: the API key for '${provider}' is written to disk in PLAINTEXT at ${KEYS_FILE} (file perms 0600).`);
  console.log(`[api-gateway]    Anyone with shell access as this user can read it. For higher assurance use an env var: ${provider.toUpperCase()}_API_KEY=sk-... (no disk storage).`);
  if (allowDomains && allowDomains.length > 0) {
    console.log(`[api-gateway] Added key: ${provider} → ${maskKey(key)} (allowlist: ${allowDomains.join(', ')})`);
  } else {
    console.log(`[api-gateway] Added key: ${provider} → ${maskKey(key)} (NO ALLOWLIST — calls will fail until you add one)`);
  }
}

function removeKey(provider) {
  const keys = loadJSON(KEYS_FILE, {});
  if (keys[provider]) {
    delete keys[provider];
    saveJSON(KEYS_FILE, keys);
    console.log(`[api-gateway] Removed key: ${provider}`);
  } else {
    console.log(`[api-gateway] No key for: ${provider}`);
  }
}

// ─── CACHE / LOG ───────────────────────────────────────────────────────────

function showCache() {
  const cache = loadJSON(CACHE_FILE, {});
  const entries = Object.entries(cache);
  const fullCacheProviders = getFullCacheProviders();
  
  console.log(`[api-gateway] Cache: ${entries.length} entries`);
  if (fullCacheProviders.length > 0) {
    console.log(`  Full-body caching enabled for: ${fullCacheProviders.join(', ')}`);
  } else {
    console.log(`  Mode: metadata-only (use --cache-full <provider> to enable body caching)`);
  }
  for (const [key, data] of entries) {
    const age = Math.floor((Date.now() - data.timestamp) / 1000);
    const bodyInfo = data.response.bodyLength !== undefined 
      ? `body=${data.response.bodyLength}B` 
      : 'body=cached';
    console.log(`  ${key.substring(0, 60)}... (${age}s ago, ${bodyInfo})`);
  }
}

function clearCache() {
  saveJSON(CACHE_FILE, {});
  console.log('[api-gateway] Cache cleared.');
}

function showLog() {
  const log = loadJSON(LOG_FILE, []);
  console.log(`[api-gateway] Request log: ${log.length} entries (coarse: provider, status class, timestamp — no endpoint paths stored)`);
  const recent = log.slice(-10);
  console.log(`\n  Recent (last 10):`);
  for (const r of recent) {
    console.log(`    ${r.timestamp} ${r.provider} → ${r.statusClass} (attempt ${r.attempt})`);
  }
}

function clearLog() {
  saveJSON(LOG_FILE, []);
  console.log('[api-gateway] Request log cleared.');
}

function enableFullCache(provider) {
  const list = getFullCacheProviders();
  if (!list.includes(provider)) {
    list.push(provider);
    saveJSON(FULL_CACHE_FILE, list);
    console.log(`[api-gateway] ⚠️  SECURITY WARNING: full-body caching ENABLED for '${provider}'.`);
    console.log(`[api-gateway]    COMPLETE response bodies (which may contain secrets, tokens, personal data, or proprietary content) will be written to ${CACHE_FILE} on disk.`);
    console.log(`[api-gateway]    This is a local data-exposure risk if the host/workspace is shared or later exfiltrated. Disable with --cache --clear, or avoid --cache-full for sensitive providers.`);
  } else {
    console.log(`[api-gateway] Full-body caching already enabled for: ${provider}`);
  }
}

// ─── FALLBACK ──────────────────────────────────────────────────────────────

function setFallback(provider, fallback) {
  const fallbacks = loadJSON(FALLBACKS_FILE, {});
  fallbacks[provider] = fallback;
  saveJSON(FALLBACKS_FILE, fallbacks);
  console.log(`[api-gateway] Fallback set: ${provider} → ${fallback}`);
}

function listFallbacks() {
  const fallbacks = loadJSON(FALLBACKS_FILE, {});
  const entries = Object.entries(fallbacks);
  if (entries.length === 0) {
    console.log('[api-gateway] No fallbacks configured.');
    return;
  }
  console.log('[api-gateway] Fallback providers:');
  for (const [provider, fallback] of entries) {
    console.log(`  ${provider} → ${fallback}`);
  }
}

// ─── STATUS ────────────────────────────────────────────────────────────────

function showStatus() {
  const keys = loadJSON(KEYS_FILE, {});
  const fallbacks = loadJSON(FALLBACKS_FILE, {});
  const cache = loadJSON(CACHE_FILE, {});
  const log = loadJSON(LOG_FILE, []);
  const fullCacheProviders = getFullCacheProviders();
  
  // Count keys with allowlists
  const keyList = Object.entries(keys);
  const keysWithAllowlist = keyList.filter(([_, v]) => 
    typeof v === 'object' && v.allowDomains && v.allowDomains.length > 0
  ).length;
  
  console.log('[api-gateway] Status:\n');
  console.log(`  API keys configured: ${keyList.length} (${keysWithAllowlist} with allowlist)`);
  console.log(`  Fallback providers: ${Object.keys(fallbacks).length}`);
  console.log(`  Cache entries: ${Object.keys(cache).length} (mode: ${fullCacheProviders.length > 0 ? 'mixed (full for: ' + fullCacheProviders.join(',') + ')' : 'metadata-only'})`);
  console.log(`  Request log entries: ${log.length} (coarse)`);
  
  if (log.length > 0) {
    const recent = log.slice(-5);
    console.log('\n  Recent requests:');
    for (const r of recent) {
      console.log(`    ${r.provider} → ${r.statusClass}`);
    }
  }
}

// ─── CLI ───────────────────────────────────────────────────────────────────

function parseCLI() {
  const args = process.argv.slice(2);
  const result = {
    mode: 'status',
    positional: [],
    flags: {
      dryRun: false,
      clear: false,
      allowDomains: [],
      circuitStatus: false
    }
  };
  
  // Two-pass: first identify the primary mode, then parse modifiers
  // Pass 1: find the first recognized mode-flag (left-to-right)
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--call') { result.mode = 'call'; break; }
    else if (arg === '--keys') { result.mode = 'keys'; break; }
    else if (arg === '--cache') { result.mode = 'cache'; break; }
    else if (arg === '--log') { result.mode = 'log'; break; }
    else if (arg === '--rate') { result.mode = 'rate'; break; }
    else if (arg === '--fallback') { result.mode = 'fallback'; break; }
    else if (arg === '--status') { result.mode = 'status'; break; }
    else if (arg === '--circuit') { result.mode = 'circuit'; break; }
    else if (arg === '--cache-full') { result.mode = 'cache-full'; break; }
  }
  
  // Pass 2: collect positionals and flags (don't re-set mode)
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--dry-run') result.flags.dryRun = true;
    else if (arg === '--clear') result.flags.clear = true;
    else if (arg === '--allow-domain') {
      i++;
      if (i < args.length) result.flags.allowDomains.push(args[i]);
    }
    else if (arg === '--reset') result.flags.circuitReset = true;
    else if (arg === '--status' && result.mode === 'circuit') result.flags.circuitStatus = true;
    else if (arg === '--dir' && i + 1 < args.length) {
      process.env.API_GATEWAY_DIR = args[++i];
    }
    else if (arg === '--retention' && i + 1 < args.length) {
      result.flags.retention = parseInt(args[++i], 10);
    }
    else if (!arg.startsWith('--')) {
      // Detect --keys add/remove as sub-modes (consume the verb, don't push to positional)
      if (result.mode === 'keys' && (arg === 'add' || arg === 'remove')) {
        result.mode = (arg === 'add') ? 'keys-add' : 'keys-remove';
        result.verb = arg;
      } else {
        result.positional.push(arg);
      }
    }
    // Skip mode-flag args (already processed in pass 1)
    else if (['--call','--keys','--cache','--log','--rate','--fallback','--status','--circuit','--cache-full'].includes(arg)) {
      continue;
    }
  }
  
  return result;
}

(async () => {
  const parsed = parseCLI();
  const { mode, positional, flags } = parsed;
  
  switch (mode) {
    case 'call': {
      const provider = positional[0];
      const endpoint = positional[1];
      const body = positional[2] ? JSON.parse(positional[2]) : null;
      if (!provider || !endpoint) {
        console.log('Usage: api-gateway.js --call <provider> <endpoint> [body]');
      } else {
        await makeCall(provider, endpoint, body, flags.dryRun);
      }
      break;
    }
    case 'keys': {
      if (flags.clear) {
        // No-op, just informational
        console.log('Use --keys add/remove to modify keys.');
      } else {
        listKeys();
      }
      break;
    }
    case 'keys-add': {
      if (positional.length < 2) {
        console.log('Usage: api-gateway.js --keys add <provider> <key> [--allow-domain <domain>]...');
      } else {
        addKey(positional[0], positional[1], flags.allowDomains);
      }
      break;
    }
    case 'keys-remove': {
      if (positional.length < 1) {
        console.log('Usage: api-gateway.js --keys remove <provider>');
      } else {
        removeKey(positional[0]);
      }
      break;
    }
    case 'cache': {
      if (flags.clear) clearCache();
      else showCache();
      break;
    }
    case 'log': {
      if (flags.clear) clearLog();
      else showLog();
      break;
    }
    case 'cache-full': {
      if (positional.length < 1) {
        console.log('Usage: api-gateway.js --cache-full <provider>');
      } else {
        enableFullCache(positional[0]);
      }
      break;
    }
    case 'rate': {
      if (positional.length < 1) {
        console.log('Usage: api-gateway.js --rate <provider>');
      } else {
        const rateLimits = loadJSON(RATE_FILE, {});
        const matching = Object.entries(rateLimits).filter(([k]) => k.startsWith(positional[0] + ':'));
        if (matching.length === 0) {
          console.log(`[api-gateway] No rate limit data for: ${positional[0]}`);
        } else {
          for (const [k, data] of matching) {
            console.log(`  ${k}: ${data.remaining} remaining, resets ${data.resetAt}`);
          }
        }
      }
      break;
    }
    case 'fallback': {
      if (positional.length >= 2) {
        setFallback(positional[0], positional[1]);
      } else {
        listFallbacks();
      }
      break;
    }
    case 'circuit': {
      if (flags.circuitReset && positional[0]) {
        resetCircuit(positional[0]);
      } else {
        getCircuitStatus();
      }
      break;
    }
    default:
      showStatus();
      break;
  }
})();
