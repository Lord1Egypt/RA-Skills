/**
 * llm-client.js — Shared LLM client for skill-evolver scripts.
 * 
 * Multi-platform LLM resolution with three-tier fallback:
 *   Tier 1: EVOLVER_API_KEY + EVOLVER_BASE_URL + EVOLVER_MODEL env vars (any platform)
 *   Tier 2: Platform adapter's detectLLM() (OpenClaw openclaw.json)
 *   Tier 3: CLI subagent fallback (openclaw agent / claude-internal -p / claude -p)
 * 
 * For explicit "provider/model" specs (e.g. "anthropic/claude-sonnet-4.6"), the client
 * tries to resolve from the host platform's config (OpenClaw openclaw.json).
 * This only works on platforms that have such config; other platforms should
 * use env vars or evolver-config.json instead.
 * 
 * Recommendation: configure EVOLVER_* env vars or evolver-config.json for
 * cross-platform compatibility. Platform-specific config is auto-detected
 * but not portable.
 * 
 * Usage:
 *   const { createLLMClient } = require('./lib/llm-client');
 *   const llm = createLLMClient('anthropic/claude-sonnet-4.6');  // explicit provider
 *   const llm = createLLMClient();                       // auto-detect (cross-platform)
 *   const llm = createLLMClient('subagent');              // force subagent
 *   const result = await llm.call(systemPrompt, userPrompt, { maxTokens: 2048 });
 *   console.log(llm.mode);    // 'direct' | 'subagent'
 *   console.log(llm.model);   // 'anthropic/claude-sonnet-4.6' | 'subagent'
 */

'use strict';

const fs = require('fs');
const path = require('path');
const http = require('http');
const https = require('https');

// ─── Config Loader ─────────────────────────────────────────────

let _configCache = null;

/**
 * Try to load OpenClaw config (openclaw.json). Returns null if not found.
 * This is OpenClaw-specific; other platforms won't have this file.
 */
function loadOpenClawConfig() {
  if (_configCache) return _configCache;
  
  const home = process.env.HOME || '';
  const configPaths = [
    process.env.OPENCLAW_CONFIG,
    home && path.join(home, '.openclaw', 'openclaw.json'),
    // Common OpenClaw project locations
    process.env.OPENCLAW_STATE_DIR && path.join(process.env.OPENCLAW_STATE_DIR, '..', 'openclaw.json'),
    path.join(process.cwd(), 'openclaw.json'),
    path.join(process.cwd(), '.openclaw', 'openclaw.json'),
  ].filter(Boolean);
  
  // Deduplicate paths (resolve to absolute)
  const seen = new Set();
  const uniquePaths = [];
  for (const p of configPaths) {
    const abs = path.resolve(p);
    if (!seen.has(abs)) { seen.add(abs); uniquePaths.push(abs); }
  }
  
  // Track search results for debugging
  const searchLog = [];
  
  for (const p of uniquePaths) {
    if (fs.existsSync(p)) {
      const raw = fs.readFileSync(p, 'utf8');
      let cfg;
      try {
        // Try json5 first (OpenClaw uses it)
        let json5;
        try { json5 = require('json5'); } catch {}
        cfg = json5 ? json5.parse(raw) : JSON.parse(raw);
      } catch {
        try { cfg = JSON.parse(raw); } catch {
          searchLog.push({ path: p, status: 'parse_error' });
          continue;
        }
      }
      searchLog.push({ path: p, status: 'found' });
      _configCache = { cfg, path: p, searchLog };
      return _configCache;
    } else {
      searchLog.push({ path: p, status: 'not_found' });
    }
  }
  
  // Not found — this is normal on non-OpenClaw platforms
  // Don't cache not-found: env may change between calls
  return { cfg: null, path: null, searchLog };
}

// ─── Auto-Detection ────────────────────────────────────────────

/**
 * Auto-detect the best available LLM configuration.
 * 
 * Three-tier priority (cross-platform):
 *   Tier 1: EVOLVER_API_KEY + EVOLVER_BASE_URL + EVOLVER_MODEL env vars
 *           Platform-independent. Any framework can set these.
 *   Tier 2: Platform adapter's detectLLM()
 *           Reads the current platform's native LLM config:
 *           - OpenClaw: openclaw.json providers
 *           - Claude Code: null (OAuth, cannot auto-detect)
 *   Tier 3: Subagent fallback (`openclaw agent` CLI)
 *           Only works on OpenClaw. Last resort.
 */
function autoDetectModel() {
  // Tier 1: explicit env vars (highest priority, platform-independent)
  if (process.env.EVOLVER_API_KEY && process.env.EVOLVER_BASE_URL && process.env.EVOLVER_MODEL) {
    console.error(`[llm] Tier 1: env vars → ${process.env.EVOLVER_MODEL} (direct HTTP)`);
    return `__env__/${process.env.EVOLVER_MODEL}`;
  }
  
  // Tier 2: platform adapter's native LLM config
  try {
    const { getAdapter } = require('./platform-detect');
    const adapter = getAdapter();
    const llmConfig = adapter.detectLLM();
    if (llmConfig) {
      console.error(`[llm] Tier 2: ${llmConfig.source || adapter.name} → ${llmConfig.model} (direct HTTP)`);
      return `__platform__/${llmConfig.model}`;
    }
  } catch (err) {
    console.error(`[llm] Tier 2: adapter LLM detection failed: ${err.message}`);
  }
  
  // Tier 3: CLI subagent fallback — detect which platform CLI is available
  const { execFileSync } = require('child_process');
  
  // 3a: OpenClaw CLI
  try {
    execFileSync('which', ['openclaw'], { encoding: 'utf8', timeout: 3000 });
    console.error(`[llm] Tier 3: openclaw CLI found → subagent mode`);
    return 'subagent:openclaw';
  } catch {}
  
  // 3b: Claude Code CLI (claude-internal for Tencent internal fork, claude for official)
  for (const bin of ['claude-internal', 'claude']) {
    try {
      execFileSync('which', [bin], { encoding: 'utf8', timeout: 3000 });
      console.error(`[llm] Tier 3: ${bin} CLI found → subagent mode`);
      return `subagent:${bin}`;
    } catch {}
  }
  
  console.error(`[llm] No LLM config and no known CLI found. LLM calls will fail.`);
  console.error(`[llm] 💡 Set EVOLVER_API_KEY + EVOLVER_BASE_URL + EVOLVER_MODEL env vars to fix.`);
  return 'subagent:none';
}

/**
 * Cache for platform LLM config (avoid re-reading config files per call).
 */
let _platformLLMCache = undefined;
function _getPlatformLLM() {
  if (_platformLLMCache !== undefined) return _platformLLMCache;
  try {
    const { getAdapter } = require('./platform-detect');
    _platformLLMCache = getAdapter().detectLLM();
  } catch {
    _platformLLMCache = null;
  }
  return _platformLLMCache;
}

// ─── Provider Resolution ───────────────────────────────────────

function resolveProvider(modelSpec) {
  const slash = modelSpec.indexOf('/');
  if (slash < 0) throw new Error(`Model spec must be "provider/model-id", got: "${modelSpec}"`);
  
  const providerName = modelSpec.substring(0, slash);
  const modelId = modelSpec.substring(slash + 1);
  
  // Tier 1: env var provider
  if (providerName === '__env__') {
    const baseUrl = process.env.EVOLVER_BASE_URL.replace(/\/+$/, '');
    const apiKey = process.env.EVOLVER_API_KEY;
    const api = process.env.EVOLVER_API_FORMAT || 'openai-completions';
    console.error(`[llm] Provider: env vars (${baseUrl})`);
    console.error(`[llm] Model: ${modelId}`);
    return {
      baseUrl, apiKey, modelId, providerName: 'env',
      api,
      maxTokensField: 'max_tokens',
      extraHeaders: {},
      toJSON() { return { baseUrl, modelId, providerName: 'env', api, key: apiKey.slice(0, 4) + '***' }; },
      [Symbol.for('nodejs.util.inspect.custom')]() { return `Provider<env/${modelId}>`; },
    };
  }
  
  // Tier 2: platform adapter's native LLM config
  if (providerName === '__platform__') {
    const llm = _getPlatformLLM();
    if (!llm) throw new Error('Platform LLM config was detected but is no longer available');
    const baseUrl = llm.baseUrl.replace(/\/+$/, '');
    console.error(`[llm] Provider: ${llm.source || 'platform'} (${baseUrl})`);
    console.error(`[llm] Model: ${modelId}`);
    return {
      baseUrl, apiKey: llm.apiKey, modelId, providerName: llm.providerName || 'platform',
      api: llm.api || 'openai-completions',
      maxTokensField: 'max_tokens',
      extraHeaders: {},
      toJSON() { return { baseUrl, modelId, providerName: llm.providerName || 'platform', api: llm.api, key: llm.apiKey.slice(0, 4) + '***' }; },
      [Symbol.for('nodejs.util.inspect.custom')]() { return `Provider<${llm.providerName || 'platform'}/${modelId}>`; },
    };
  }
  
  // Tier 3: Host platform config (OpenClaw openclaw.json providers)
  const ocConfig = loadOpenClawConfig();
  if (!ocConfig) {
    throw new Error(
      `Explicit provider spec "${modelSpec}" requires a platform config file (e.g. openclaw.json). ` +
      `Not found. Use EVOLVER_API_KEY/EVOLVER_BASE_URL/EVOLVER_MODEL env vars or evolver-config.json instead.`
    );
  }
  const { cfg, path: configPath } = ocConfig;
  
  const provider = cfg.models?.providers?.[providerName];
  if (!provider) {
    const available = Object.keys(cfg.models?.providers || {}).join(', ');
    throw new Error(`Provider "${providerName}" not found in platform config. Available: ${available}`);
  }
  
  if (!provider.baseUrl) throw new Error(`Provider "${providerName}" has no baseUrl`);
  if (!provider.apiKey) throw new Error(`Provider "${providerName}" has no apiKey. Configure it in your platform config or use evolver-config.json`);
  
  const knownModels = (provider.models || []).map(m => m.id);
  if (knownModels.length > 0 && !knownModels.includes(modelId)) {
    console.error(`  [llm] Warning: model "${modelId}" not in known models: ${knownModels.join(', ')}`);
  }
  
  console.error(`[llm] Provider: ${providerName} (${provider.baseUrl})`);
  console.error(`[llm] Model: ${modelId}`);
  console.error(`[llm] Config: ${configPath}`);
  
  const apiKey = provider.apiKey;
  const modelMeta = provider.models?.find(m => m.id === modelId);
  return {
    baseUrl: provider.baseUrl.replace(/\/+$/, ''),
    apiKey,
    modelId,
    providerName,
    // "anthropic-messages" → /v1/messages format; anything else → /chat/completions (OpenAI)
    api: provider.api || 'openai-completions',
    maxTokensField: modelMeta?.compat?.maxTokensField || 'max_tokens',
    extraHeaders: modelMeta?.headers || {},
    // Prevent accidental key leakage in logs/JSON.stringify
    toJSON() { return { baseUrl: this.baseUrl, modelId, providerName, api: this.api, key: apiKey.slice(0, 4) + '***' }; },
    [Symbol.for('nodejs.util.inspect.custom')]() { return `Provider<${providerName}/${modelId}>`; },
  };
}

// ─── Raw HTTP Call ──────────────────────────────────────────────

// Build request params based on provider.api format
function _buildRequest(provider, system, user, { maxTokens = 2048, temperature = 0.3 } = {}) {
  if (provider.api === 'anthropic-messages') {
    // Anthropic native format: POST /v1/messages
    const payload = JSON.stringify({
      model: provider.modelId,
      max_tokens: maxTokens,
      system,
      messages: [{ role: 'user', content: user }],
    });
    const url = new URL(provider.baseUrl + '/v1/messages');
    return {
      url,
      payload,
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': provider.apiKey,
        'anthropic-version': '2023-06-01',
        'Content-Length': Buffer.byteLength(payload),
        ...provider.extraHeaders,
      },
      parseResponse(result) {
        // Anthropic: content is array of blocks
        const block = result.content?.find(b => b.type === 'text');
        return block?.text || null;
      },
      logUsage(result) {
        const u = result.usage;
        if (u) console.error(`  [llm] tokens: in=${u.input_tokens} out=${u.output_tokens}`);
      },
    };
  }

  // Default: OpenAI-compatible /chat/completions
  const payload = JSON.stringify({
    model: provider.modelId,
    messages: [
      { role: 'system', content: system },
      { role: 'user', content: user },
    ],
    [provider.maxTokensField]: maxTokens,
    temperature,
  });
  const url = new URL(provider.baseUrl + '/chat/completions');
  return {
    url,
    payload,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${provider.apiKey}`,
      'Content-Length': Buffer.byteLength(payload),
      ...provider.extraHeaders,
    },
    parseResponse(result) {
      return result.choices?.[0]?.message?.content || null;
    },
    logUsage(result) {
      const u = result.usage;
      if (u) console.error(`  [llm] tokens: in=${u.prompt_tokens} out=${u.completion_tokens}`);
    },
  };
}

function _callRaw(provider, system, user, opts = {}) {
  return new Promise((resolve, reject) => {
    const req_cfg = _buildRequest(provider, system, user, opts);
    const { url, payload, headers, parseResponse, logUsage } = req_cfg;

    const isHttps = url.protocol === 'https:';
    const lib = isHttps ? https : http;

    const req = lib.request({
      hostname: url.hostname,
      port: url.port || (isHttps ? 443 : 80),
      path: url.pathname,
      method: 'POST',
      headers,
      timeout: 120000,
    }, res => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        if (res.statusCode === 429) {
          const retryAfter = res.headers['retry-after'];
          return reject(Object.assign(
            new Error(`Rate limited (429) by ${provider.providerName}. Retry-After: ${retryAfter || 'unknown'}`),
            { retryable: true, retryAfterMs: retryAfter ? parseInt(retryAfter) * 1000 : 5000 }
          ));
        }
        if (res.statusCode >= 500) {
          return reject(Object.assign(
            new Error(`Server error ${res.statusCode} from ${provider.providerName}: ${body.substring(0, 200)}`),
            { retryable: true, retryAfterMs: 3000 }
          ));
        }
        if (res.statusCode !== 200) {
          return reject(new Error(`LLM API ${res.statusCode} (${provider.providerName}): ${body.substring(0, 300)}`));
        }
        try {
          const result = JSON.parse(body);
          const content = parseResponse(result);
          if (!content) {
            return reject(new Error(`LLM returned empty content: ${JSON.stringify(result).substring(0, 200)}`));
          }
          logUsage(result);
          resolve(content);
        } catch (e) {
          reject(new Error(`Parse error: ${e.message}\nBody: ${body.substring(0, 200)}`));
        }
      });
    });
    req.on('error', e => reject(Object.assign(e, { retryable: true, retryAfterMs: 2000 })));
    req.on('timeout', () => { req.destroy(); reject(Object.assign(new Error('LLM request timeout (120s)'), { retryable: true, retryAfterMs: 5000 })); });
    req.write(payload);
    req.end();
  });
}

// ─── Subagent CLI Call ─────────────────────────────────────────

function _callSubagent(system, user) {
  const { execFileSync } = require('child_process');
  
  const combinedPrompt = `IMPORTANT: You are being used as a pure LLM for text generation. Do NOT use any tools. Do NOT access any files. Just process the following prompt and respond with ONLY the requested output.

=== SYSTEM INSTRUCTIONS ===
${system}

=== INPUT ===
${user}`;
  
  const sessionId = `evolver-llm-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
  
  // Use execFileSync with argument array to avoid shell interpolation entirely.
  // This prevents command injection via $(), backticks, or other shell metacharacters
  // that JSON.stringify does not escape.
  const result = execFileSync('openclaw', [
    'agent', '--session-id', sessionId, '--json', '--timeout', '120', '--message', combinedPrompt,
  ], { encoding: 'utf8', timeout: 130000, maxBuffer: 10 * 1024 * 1024 });
  
  let parsed;
  // Defense: openclaw agent --json may prefix channel init logs before the JSON object.
  // Strip any non-JSON prefix lines (e.g. [openclaw-wecom-bot] ...) before parsing.
  let cleanResult = result;
  const jsonStart = result.indexOf('{\n');
  if (jsonStart > 0) {
    console.error(`[llm] Stripping ${jsonStart} bytes of non-JSON prefix from subagent output`);
    cleanResult = result.substring(jsonStart);
  } else if (result.indexOf('{') > 0) {
    // Fallback: find first { even without newline
    const idx = result.indexOf('{');
    console.error(`[llm] Stripping ${idx} bytes of non-JSON prefix from subagent output`);
    cleanResult = result.substring(idx);
  }
  try {
    parsed = JSON.parse(cleanResult);
  } catch (e) {
    console.error(`[llm] Subagent returned non-JSON (first 200 chars): ${(result || '').slice(0, 200)}`);
    console.error(`[llm] Cleaned attempt (first 200 chars): ${(cleanResult || '').slice(0, 200)}`);
    throw new Error(`Subagent returned unparseable output: ${e.message}`);
  }
  if (parsed.status !== 'ok') {
    throw new Error(`Subagent returned status: ${parsed.status}`);
  }
  
  const text = parsed.result?.payloads?.[0]?.text;
  if (!text) throw new Error('Subagent returned empty text');
  
  const usage = parsed.result?.meta?.agentMeta?.usage;
  if (usage) {
    const parts = [`in=${usage.input || 0}`];
    if (usage.cacheRead) parts.push(`cached=${usage.cacheRead}`);
    parts.push(`out=${usage.output || 0}`);
    console.error(`  [llm:subagent] tokens: ${parts.join(' ')}`);
  }
  
  return text;
}

// ─── Claude Code CLI Call ─────────────────────────────────────

/**
 * Call Claude Code CLI (claude-internal or claude) in print mode.
 * Uses -p --output-format json for non-interactive structured output.
 * 
 * @param {string} bin - CLI binary name ('claude-internal' or 'claude')
 * @param {string} system - system prompt
 * @param {string} user - user prompt
 * @returns {string} response text
 */
function _callClaudeCodeCLI(bin, system, user) {
  const { execFileSync } = require('child_process');
  
  const combinedPrompt = `IMPORTANT: You are being used as a pure LLM for text generation. Do NOT use any tools. Do NOT access any files. Just process the following prompt and respond with ONLY the requested output.

=== SYSTEM INSTRUCTIONS ===
${system}

=== INPUT ===
${user}`;
  
  // claude -p "prompt" --output-format json --no-session-persistence --allowedTools ""
  // --no-session-persistence: don't save this throwaway session
  // --allowedTools with empty: disable all tools (pure LLM mode)
  const args = [
    '-p', combinedPrompt,
    '--output-format', 'json',
    '--no-session-persistence',
    '--allowedTools', '',
  ];
  
  console.error(`  [llm:claude-cli] Calling ${bin} -p ...`);
  const result = execFileSync(bin, args, {
    encoding: 'utf8',
    timeout: 180000,  // 3 minutes (Claude Code can be slow to start)
    maxBuffer: 10 * 1024 * 1024,
    env: { ...process.env },
  });
  
  // Output format: JSON with result field
  // Try to parse as JSON first
  try {
    const parsed = JSON.parse(result);
    // Claude Code --output-format json returns { result: "text", ... }
    const text = parsed.result || parsed.text || parsed.content;
    if (text) {
      if (parsed.usage || parsed.cost_usd) {
        console.error(`  [llm:claude-cli] cost: $${parsed.cost_usd || '?'}`);
      }
      return text;
    }
  } catch {
    // Not JSON — might be plain text output
  }
  
  // Fallback: treat entire output as text (strip trailing newline)
  const text = result.trim();
  if (!text) throw new Error(`${bin} returned empty output`);
  return text;
}

// ─── Public API ────────────────────────────────────────────────

/**
 * Create an LLM client instance.
 * @param {string|null} modelSpec - "provider/model-id", "subagent", or null (auto-detect)
 * @returns {{ call, mode, model }}
 */
function createLLMClient(modelSpec = null) {
  if (!modelSpec) {
    modelSpec = autoDetectModel();
  }
  
  if (modelSpec === 'subagent') {
    // Legacy compat: bare 'subagent' defaults to openclaw
    modelSpec = 'subagent:openclaw';
  }
  
  if (modelSpec.startsWith('subagent:')) {
    const backend = modelSpec.split(':')[1];
    
    if (backend === 'none') {
      return {
        mode: 'subagent',
        model: 'none',
        async call() {
          throw new Error(
            'No LLM available. Set EVOLVER_API_KEY + EVOLVER_BASE_URL + EVOLVER_MODEL env vars, ' +
            'or install a supported CLI (openclaw, claude-internal, claude).'
          );
        },
      };
    }
    
    if (backend === 'openclaw') {
      return {
        mode: 'subagent',
        model: 'openclaw-agent',
        async call(system, user, opts = {}) {
          return _callSubagent(system, user);
        },
      };
    }
    
    // claude-internal or claude
    return {
      mode: 'subagent',
      model: `${backend}-cli`,
      async call(system, user, opts = {}) {
        return _callClaudeCodeCLI(backend, system, user);
      },
    };
  }
  
  const provider = resolveProvider(modelSpec);
  
  return {
    mode: 'direct',
    model: modelSpec,
    async call(system, user, opts = {}) {
      const maxRetries = 2;
      let lastErr;
      
      for (let attempt = 0; attempt <= maxRetries; attempt++) {
        try {
          return await _callRaw(provider, system, user, opts);
        } catch (err) {
          lastErr = err;
          if (err.retryable && attempt < maxRetries) {
            const waitMs = err.retryAfterMs || 3000;
            console.error(`  [llm] Retryable error (attempt ${attempt + 1}/${maxRetries + 1}): ${err.message}. Waiting ${waitMs}ms...`);
            await new Promise(r => setTimeout(r, waitMs));
            continue;
          }
          throw err;
        }
      }
      throw lastErr;
    },
  };
}

module.exports = { createLLMClient, loadOpenClawConfig, autoDetectModel, resolveProvider };
