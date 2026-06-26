/**
 * CoVe (Chain of Verification) — Orchestrator
 *
 * Extracts factual claims from an LLM response, verifies each against
 * the user's knowledge sources (memory, workspace, web search), and
 * optionally rewrites the response with corrections.
 *
 * Works standalone or with OpenClaw. If an LLM API key is configured
 * (GEMINI_API_KEY, ANTHROPIC_API_KEY, or OPENAI_API_KEY), calls the
 * provider directly. Otherwise routes through the OpenClaw sidecar proxy.
 */

const http = require('http');
const https = require('https');
const { loadKnowledge } = require('./knowledge');
const { searchWeb } = require('./web_search');
const { queryVectorStore } = require('./vector_store');
const { loadConfig } = require('./config');
const { logResult } = require('./csm-logger');

// ── LLM helper ──────────────────────────────────────────────────────────────

/**
 * Provider-specific API configurations.
 * Each provider defines how to build the request for its API.
 */
const PROVIDERS = {
  gemini: {
    hostname: 'generativelanguage.googleapis.com',
    buildPath: (model, apiKey) =>
      `/v1beta/models/${model}:generateContent?key=${apiKey}`,
    defaultModel: 'gemini-2.0-flash',
    buildBody: (messages, options) => ({
      contents: messages.map(m => ({
        role: m.role === 'assistant' ? 'model' : 'user',
        parts: [{ text: m.content }],
      })),
      generationConfig: {
        maxOutputTokens: options.maxTokens || 2048,
        temperature: options.temperature ?? 0.1,
      },
    }),
    extractContent: (data) => {
      if (data.error) throw new Error(data.error.message || JSON.stringify(data.error));
      return data.candidates?.[0]?.content?.parts?.[0]?.text || '';
    },
  },

  anthropic: {
    hostname: 'api.anthropic.com',
    buildPath: () => '/v1/messages',
    defaultModel: 'claude-sonnet-4-6-20250514',
    buildHeaders: (apiKey) => ({
      'x-api-key': apiKey,
      'anthropic-version': '2023-06-01',
    }),
    buildBody: (messages, options, model) => {
      // Anthropic expects system as a top-level field, not in messages
      const system = messages.filter(m => m.role === 'system').map(m => m.content).join('\n');
      const msgs = messages.filter(m => m.role !== 'system');
      return {
        model,
        max_tokens: options.maxTokens || 2048,
        temperature: options.temperature ?? 0.1,
        ...(system ? { system } : {}),
        messages: msgs,
      };
    },
    extractContent: (data) => {
      if (data.error) throw new Error(data.error.message || JSON.stringify(data.error));
      return data.content?.[0]?.text || '';
    },
  },

  openai: {
    hostname: 'api.openai.com',
    buildPath: () => '/v1/chat/completions',
    defaultModel: 'gpt-4o-mini',
    buildHeaders: (apiKey) => ({ Authorization: `Bearer ${apiKey}` }),
    buildBody: (messages, options, model) => ({
      model,
      messages,
      max_tokens: options.maxTokens || 2048,
      temperature: options.temperature ?? 0.1,
    }),
    extractContent: (data) => {
      if (data.error) throw new Error(data.error.message || JSON.stringify(data.error));
      return data.choices?.[0]?.message?.content || '';
    },
  },
};

/**
 * Make an HTTPS request and return the parsed JSON response.
 */
function httpsPost(hostname, path, headers, body, timeout) {
  return new Promise((resolve, reject) => {
    const payload = JSON.stringify(body);
    const req = https.request({
      hostname,
      port: 443,
      path,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload),
        ...headers,
      },
    }, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch { reject(new Error(`Failed to parse response: ${data.slice(0, 300)}`)); }
      });
    });
    req.on('error', reject);
    req.setTimeout(timeout, () => { req.destroy(); reject(new Error('LLM request timed out')); });
    req.write(payload);
    req.end();
  });
}

/**
 * Call the LLM — routes to a direct provider API or the OpenClaw sidecar proxy.
 *
 * If config.llm_provider is set (gemini/anthropic/openai), calls the provider
 * API directly using config.llm_api_key. Otherwise, routes through the local
 * sidecar proxy at localhost:{proxy_port}.
 *
 * @param {Array} messages - Chat messages.
 * @param {object} options - Request options (maxTokens, temperature, timeout).
 * @param {object} config  - Resolved config from config.js.
 */
async function callLLM(messages, options = {}, config = {}) {
  const timeout = options.timeout || 30000;
  const provider = PROVIDERS[config.llm_provider];

  // Direct API mode
  if (provider && config.llm_api_key) {
    const model = options.model || config.model || provider.defaultModel;
    const path = provider.buildPath(model, config.llm_api_key);
    const headers = provider.buildHeaders ? provider.buildHeaders(config.llm_api_key) : {};
    const body = provider.buildBody(messages, options, model);
    const data = await httpsPost(provider.hostname, path, headers, body, timeout);
    return provider.extractContent(data);
  }

  // Sidecar proxy mode (original behavior)
  return new Promise((resolve, reject) => {
    const proxyKey = config.proxy_key || '';
    const port = config.proxy_port || 8888;
    const model = options.model || config.model || 'gemini-2.0-flash';

    const body = JSON.stringify({
      model,
      messages,
      max_tokens: options.maxTokens || 2048,
      temperature: options.temperature ?? 0.1,
    });

    const req = http.request({
      hostname: '127.0.0.1',
      port,
      path: '/v1/chat/completions',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(proxyKey ? { Authorization: `Bearer ${proxyKey}` } : {}),
        'Content-Length': Buffer.byteLength(body),
      },
    }, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          if (parsed.error) return reject(new Error(parsed.error.message || JSON.stringify(parsed.error)));
          const content = parsed.choices?.[0]?.message?.content || '';
          resolve(content);
        } catch (e) {
          reject(new Error(`Failed to parse LLM response: ${data.slice(0, 300)}`));
        }
      });
    });

    req.on('error', reject);
    req.setTimeout(timeout, () => { req.destroy(); reject(new Error('LLM request timed out')); });
    req.write(body);
    req.end();
  });
}

// ── Step 1: Extract claims ──────────────────────────────────────────────────

const EXTRACTION_PROMPT = `You are an expert fact-extractor implementing Chain of Verification (CoVe).
Break down the input text into atomic, verifiable factual claims.

Extract claims that involve:
- Names, dates, numbers, amounts, percentages, statistics
- Product/service details, pricing, tiers, features
- Customer or person information, status, relationships
- Policies, procedures, deadlines, SLAs
- Historical events, decisions, outcomes

Do NOT extract:
- Opinions, suggestions, recommendations, or speculation
- General knowledge or widely-known facts
- Greetings, pleasantries, or conversational filler
- Questions asked by the author
- Creative content or brainstorming ideas

Return ONLY a JSON array — no markdown, no explanation:
[{"id": 1, "claim": "exact claim text"}, ...]

If there are no verifiable claims, return: []`;

async function extractClaims(response, config) {
  const result = await callLLM([
    { role: 'system', content: EXTRACTION_PROMPT },
    { role: 'user', content: response },
  ], {}, config);

  const match = result.match(/\[[\s\S]*\]/);
  if (!match) return [];
  try {
    const claims = JSON.parse(match[0]);
    return Array.isArray(claims) ? claims : [];
  } catch {
    return [];
  }
}

// ── Step 2: Verify claims ───────────────────────────────────────────────────

const VERIFICATION_PROMPT = `You are a fact-checking agent implementing Chain of Verification (CoVe).
You will receive a list of claims and a knowledge base. For each claim, determine:

- **verified**: The knowledge base explicitly supports this claim.
- **inaccurate**: The knowledge base explicitly contradicts this claim. Provide the correct information.
- **unverifiable**: The claim cannot be confirmed or denied from available sources.

Be precise and conservative:
- Only mark "verified" if there is clear supporting evidence.
- Only mark "inaccurate" if the knowledge base clearly contradicts the claim.
- Mark "unverifiable" if the information is simply absent.

Return ONLY a JSON array — no markdown, no explanation:
[{
  "id": 1,
  "claim": "the claim text",
  "status": "verified|inaccurate|unverifiable",
  "source": "filename or source where evidence was found, or null",
  "evidence": "brief quote or reference supporting the verdict",
  "correction": "correct information if inaccurate, otherwise null"
}]`;

async function verifyClaims(claims, knowledgeContext, webContext, config) {
  let context = knowledgeContext;
  if (webContext) {
    context += '\n\n--- WEB SEARCH RESULTS ---\n' + webContext;
  }

  const result = await callLLM([
    { role: 'system', content: VERIFICATION_PROMPT },
    { role: 'user', content: `Claims to verify:\n${JSON.stringify(claims, null, 2)}\n\nKnowledge Base:\n${context}` },
  ], {}, config);

  const match = result.match(/\[[\s\S]*\]/);
  if (!match) return claims.map(c => ({ ...c, status: 'unverifiable', source: null, evidence: null, correction: null }));
  try {
    const parsed = JSON.parse(match[0]);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return claims.map(c => ({ ...c, status: 'unverifiable', source: null, evidence: null, correction: null }));
  }
}

// ── Step 3: Correction loop ─────────────────────────────────────────────────

const CORRECTION_PROMPT = `You are a precise editor. You will receive an original response and a list of
factual inaccuracies with their corrections. Rewrite the response so that all
inaccurate claims are replaced with the correct information.

Rules:
- Preserve the original tone, style, and structure as much as possible.
- Only change the parts that are factually wrong.
- Do NOT add disclaimers, notes, or meta-commentary about corrections.
- Do NOT mention that corrections were made.
- Return ONLY the corrected response text.`;

async function performCorrectionLoop(originalResponse, inaccuracies, config) {
  if (!config.auto_correct) return null;

  const corrections = inaccuracies.map(i =>
    `- WRONG: "${i.claim}" → CORRECT: ${i.correction || 'Unknown'} (source: ${i.source || 'N/A'})`
  ).join('\n');

  let attempts = 0;
  let corrected = originalResponse;
  const maxAttempts = config.max_correction_attempts || 1;

  while (attempts < maxAttempts) {
    attempts++;
    corrected = await callLLM([
      { role: 'system', content: CORRECTION_PROMPT },
      { role: 'user', content: `Original response:\n${corrected}\n\nInaccuracies found:\n${corrections}` },
    ], {}, config);
  }

  return corrected;
}

// ── Main orchestrator ───────────────────────────────────────────────────────

/**
 * Run the full CoVe pipeline on an LLM response.
 *
 * @param {string} originalResponse - The LLM response to verify.
 * @param {object} [overrides] - Optional config overrides.
 * @returns {object} Verification report with optional corrected response.
 */
async function verifyResponse(originalResponse, overrides = {}) {
  const config = { ...loadConfig(), ...overrides };
  const startTime = Date.now();

  // Step 1: Extract claims
  const claims = await extractClaims(originalResponse, config);
  if (claims.length === 0) {
    const report = {
      verified: true,
      originalResponse,
      correctedResponse: null,
      claims: [],
      summary: { total: 0, verified: 0, inaccurate: 0, unverifiable: 0 },
      durationMs: Date.now() - startTime,
    };
    logResult(report, config);
    return report;
  }

  // Step 2: Gather knowledge context
  const knowledgeContext = loadKnowledge(config);

  // Step 2b: Vector store search if configured
  let vectorContext = null;
  if (config.vector_store && config.vector_store.provider) {
    const searchQueries = claims.map(c => c.claim);
    vectorContext = await queryVectorStore(searchQueries, config);
  }

  // Step 2c: Web search if policy allows
  let webContext = null;
  if (config.policy === 'standard' || config.policy === 'deep') {
    const searchQueries = claims.map(c => c.claim);
    webContext = await searchWeb(searchQueries, config);
  }

  // Step 3: Verify claims — combine all knowledge sources
  let combinedContext = knowledgeContext;
  if (vectorContext) {
    combinedContext += '\n\n--- VECTOR STORE RESULTS ---\n' + vectorContext;
  }

  const results = await verifyClaims(claims, combinedContext, webContext, config);

  // Step 4: Categorize
  const verified = results.filter(r => r.status === 'verified');
  const inaccurate = results.filter(r => r.status === 'inaccurate');
  const unverifiable = results.filter(r => r.status === 'unverifiable');

  // Step 5: Correct if needed
  let correctedResponse = null;
  if (inaccurate.length > 0 && config.auto_correct) {
    correctedResponse = await performCorrectionLoop(originalResponse, inaccurate, config);
  }

  const report = {
    verified: inaccurate.length === 0,
    originalResponse,
    correctedResponse,
    claims: results,
    summary: {
      total: results.length,
      verified: verified.length,
      inaccurate: inaccurate.length,
      unverifiable: unverifiable.length,
    },
    durationMs: Date.now() - startTime,
  };

  logResult(report, config);
  return report;
}

module.exports = { verifyResponse, extractClaims, verifyClaims, callLLM };
