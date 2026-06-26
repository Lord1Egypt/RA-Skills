'use strict';

const { createProxyTrace } = require('../trace/extractor');

const OPENAI_RESPONSE_HEADER_ALLOWLIST = new Set([
  'openai-processing-ms',
  'openai-version',
  'retry-after',
  'x-request-id',
]);

function hasOpenAIUpstreamCredential() {
  if (process.env.EVOMAP_OPENAI_API_KEY || process.env.OPENAI_API_KEY) return true;
  return false;
}

function upstreamStatus(err, fallback = 502) {
  const status = Number(err && err.statusCode);
  return Number.isFinite(status) ? status : fallback;
}

function safeOpenAIConfigDiagnostic(err) {
  const message = err && typeof err.message === 'string' ? err.message : '';
  if (message.startsWith('[proxy] EVOMAP_OPENAI_BASE_URL ')) return message;
  return '';
}

function asUpstreamError(err, fallback = 502) {
  if (err && err.statusCode && /^openai upstream /.test(err.message || '')) return err;
  const diagnostic = safeOpenAIConfigDiagnostic(err);
  const message = diagnostic
    ? `openai upstream request failed: ${diagnostic}`
    : 'openai upstream request failed';
  const out = new Error(message);
  out.statusCode = upstreamStatus(err, fallback);
  out.cause = err;
  return out;
}

function responseToBody(raw, status, headers, log) {
  if (!raw) return {};
  try {
    return JSON.parse(raw);
  } catch {
    log.warn?.(JSON.stringify({
      event: 'openai_responses_fallback',
      reason: 'upstream_non_json',
      upstream_status: status,
      content_type: headers && headers['content-type'] || '',
      response_bytes: Buffer.byteLength(raw),
    }));
    return { error: raw };
  }
}

function copyOpenAIResponseHeaders(headers = {}) {
  const out = {};
  for (const [name, value] of Object.entries(headers || {})) {
    const lower = String(name || '').toLowerCase();
    if (!OPENAI_RESPONSE_HEADER_ALLOWLIST.has(lower) && !lower.startsWith('x-ratelimit-')) continue;
    if (value === undefined || value === null) continue;
    const headerValue = Array.isArray(value) ? value.join(', ') : String(value);
    if (/[\r\n]/.test(headerValue)) continue;
    out[lower] = headerValue;
  }
  return out;
}

// Generic OpenAI passthrough handler. `upstreamPath` selects the OpenAI endpoint (/responses for codex's
// Responses API, /chat/completions for the Chat Completions API used by cursor's OpenAI mode + generic OpenAI
// clients). Both share the same upstream, auth, header allow-list, trace, and stream tee — the only difference
// is the path + the trace route label. No translation: each OpenAI dialect goes to its native OpenAI endpoint.
function buildResponsesHandler({ openAIProxy, logger, traceStore, onTraceQueued, upstreamPath = '/responses', traceRoute = 'POST /v1/responses' } = {}) {
  if (typeof openAIProxy !== 'function') {
    throw new Error('buildResponsesHandler requires openAIProxy(path, body, opts)');
  }
  const log = logger || console;

  return async ({ body, headers }) => {
    const inboundHeaders = headers || {};
    if (!hasOpenAIUpstreamCredential()) {
      throw Object.assign(new Error('openai api key required'), { statusCode: 401 });
    }

    const originalModel = body && typeof body.model === 'string' ? body.model : null;
    let trace = null;
    try {
      trace = createProxyTrace({
        route: traceRoute,
        headers: inboundHeaders,
        body,
        upstreamMode: 'openai',
        originalModel,
        chosenModel: originalModel,
        store: traceStore,
        logger: traceStore ? log : null,
        onTraceQueued,
      });
    } catch (_) { /* best-effort trace; never break the request */ }

    let upstream;
    try {
      upstream = await openAIProxy(upstreamPath, body, {
        inboundHeaders,
        upstreamMode: 'openai',
      });
    } catch (err) {
      const wrapped = asUpstreamError(err, upstreamStatus(err));
      trace?.record({ status: wrapped.statusCode, error: wrapped, upstreamMode: 'openai', model: originalModel });
      throw wrapped;
    }

    if (upstream.stream) {
      const forwardHeaders = copyOpenAIResponseHeaders(upstream.headers);
      const ct = upstream.headers && upstream.headers['content-type'];
      if (ct) forwardHeaders['Content-Type'] = ct;
      trace?.recordStreamStart({
        status: upstream.status,
        upstreamMode: 'openai',
        model: originalModel,
        headers: forwardHeaders,
      });
      return {
        status: upstream.status,
        // Tee the codex SSE body so the deferred trace captures usage + response.id from response.completed.
        // Bytes forward unchanged; emits once on stream end/cancel/error.
        stream: trace ? trace.observeStream(upstream.stream) : upstream.stream,
        headers: forwardHeaders,
      };
    }

    let raw = '';
    if (upstream.text) {
      try {
        raw = await upstream.text();
      } catch (err) {
        const wrapped = asUpstreamError(err, upstreamStatus(err));
        trace?.record({ status: wrapped.statusCode, error: wrapped, upstreamMode: 'openai', model: originalModel });
        throw wrapped;
      }
    }
    const respBody = responseToBody(raw, upstream.status, upstream.headers, log);
    trace?.record({
      status: upstream.status,
      responseBody: respBody,
      upstreamMode: 'openai',
      model: originalModel,
      headers: upstream.headers,
    });
    return {
      status: upstream.status,
      body: respBody,
      headers: copyOpenAIResponseHeaders(upstream.headers),
    };
  };
}

// OpenAI Chat Completions ingress (cursor's OpenAI mode + generic OpenAI clients). Same OpenAI upstream as the
// Responses handler, just the /chat/completions endpoint — point an OpenAI-Chat client's base URL at the proxy.
function buildChatCompletionsHandler(opts = {}) {
  return buildResponsesHandler({ ...opts, upstreamPath: '/chat/completions', traceRoute: 'POST /v1/chat/completions' });
}

module.exports = {
  buildResponsesHandler,
  buildChatCompletionsHandler,
  copyOpenAIResponseHeaders,
  hasOpenAIUpstreamCredential,
  responseToBody,
};
