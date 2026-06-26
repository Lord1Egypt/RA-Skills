'use strict';

// GET /v1/models — model-list probe passthrough (format-aware routing, no translation). Many clients (codex,
// opencode, cursor in OpenAI mode, OpenAI/Anthropic SDKs) hit GET /v1/models on startup to validate the endpoint
// and list models; without a route they get a 404 and may fail to initialize or fall back. Route by the client's
// intended provider: Anthropic clients send the `anthropic-version` header → Anthropic /v1/models; everyone else
// → OpenAI /v1/models (the convention's home). Forwarded verbatim to the native upstream, no body, no translation.
// Not traced: it is a metadata probe, not an LLM call.

function detectModelsProvider(headers = {}) {
  const lower = {};
  for (const [k, v] of Object.entries(headers || {})) lower[String(k).toLowerCase()] = v;
  // anthropic-version (and anthropic-beta) are sent by every Anthropic SDK request and by nothing else.
  if (lower['anthropic-version'] || lower['anthropic-beta']) return 'anthropic';
  return 'openai';
}

function buildModelsHandler({ anthropicProxy, openAIProxy, logger } = {}) {
  if (typeof anthropicProxy !== 'function' || typeof openAIProxy !== 'function') {
    throw new Error('buildModelsHandler requires anthropicProxy(path,body,opts) + openAIProxy(path,body,opts)');
  }
  const log = logger || console;

  return async ({ headers }) => {
    const inboundHeaders = headers || {};
    const provider = detectModelsProvider(inboundHeaders);
    const [proxyFn, reqPath, mode] = provider === 'anthropic'
      ? [anthropicProxy, '/v1/models', 'anthropic']
      : [openAIProxy, '/models', 'openai'];

    let up;
    try {
      up = await proxyFn(reqPath, null, { method: 'GET', inboundHeaders, upstreamMode: mode });
    } catch (err) {
      const status = Number(err && err.statusCode) || 502;
      return { status, body: { error: (err && err.message) || 'models upstream request failed' } };
    }

    let raw = '';
    try { raw = up.text ? await up.text() : ''; } catch { raw = ''; }
    let body;
    try {
      body = raw ? JSON.parse(raw) : {};
    } catch {
      log.warn?.(JSON.stringify({ event: 'models_fallback', reason: 'upstream_non_json', upstream_status: up.status }));
      body = { error: raw };
    }
    return { status: up.status, body };
  };
}

module.exports = { buildModelsHandler, detectModelsProvider };
