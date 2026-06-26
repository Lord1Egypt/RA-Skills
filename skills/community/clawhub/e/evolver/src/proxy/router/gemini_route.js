'use strict';

// Gemini passthrough handler (format-aware routing, NO translation). A Gemini-shaped request — Google's native
// `/v1beta/models/<model>:generateContent` | `:streamGenerateContent` path, body `{contents, generationConfig,
// systemInstruction, tools}` — is forwarded verbatim to the Gemini upstream. The model + action live in the
// PATH (not the body), so we reconstruct the path (+ query like ?alt=sse) and pass it through. Trace capture
// mirrors the other providers (usage/finish/stream tee). Point the Gemini CLI/SDK's base URL at the proxy and
// it works unmodified — no Anthropic/OpenAI conversion (lossy translation is deliberately avoided).

const { createProxyTrace } = require('../trace/extractor');

const GEMINI_RESPONSE_HEADER_ALLOWLIST = new Set([
  'content-type',
  'retry-after',
  'x-request-id',
]);

function hasGeminiUpstreamCredential() {
  return !!(process.env.EVOMAP_GEMINI_API_KEY || process.env.GEMINI_API_KEY || process.env.GOOGLE_API_KEY);
}

function upstreamStatus(err, fallback = 502) {
  const status = Number(err && err.statusCode);
  return Number.isFinite(status) ? status : fallback;
}

function asUpstreamError(err, fallback = 502) {
  if (err && err.statusCode && /^gemini upstream /.test(err.message || '')) return err;
  const out = new Error('gemini upstream request failed');
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
      event: 'gemini_fallback',
      reason: 'upstream_non_json',
      upstream_status: status,
      content_type: (headers && headers['content-type']) || '',
      response_bytes: Buffer.byteLength(raw),
    }));
    return { error: raw };
  }
}

function copyGeminiResponseHeaders(headers = {}) {
  const out = {};
  for (const [name, value] of Object.entries(headers || {})) {
    const lower = String(name || '').toLowerCase();
    if (!GEMINI_RESPONSE_HEADER_ALLOWLIST.has(lower) && !lower.startsWith('x-goog-')) continue;
    if (value === undefined || value === null) continue;
    const headerValue = Array.isArray(value) ? value.join(', ') : String(value);
    if (/[\r\n]/.test(headerValue)) continue;
    out[lower] = headerValue;
  }
  return out;
}

// `<model>:<action>` — the model can contain dots/dashes; the action is the part after the LAST colon
// (generateContent | streamGenerateContent | countTokens | ...). Returns {model, action} (action '' if absent).
function parseModelAction(modelAction) {
  const s = String(modelAction || '');
  const idx = s.lastIndexOf(':');
  if (idx === -1) return { model: s, action: '' };
  return { model: s.slice(0, idx), action: s.slice(idx + 1) };
}

function buildGeminiHandler({ geminiProxy, logger, traceStore, onTraceQueued } = {}) {
  if (typeof geminiProxy !== 'function') {
    throw new Error('buildGeminiHandler requires geminiProxy(path, body, opts)');
  }
  const log = logger || console;

  return async ({ body, headers, params, query }) => {
    const inboundHeaders = headers || {};
    if (!hasGeminiUpstreamCredential()) {
      throw Object.assign(new Error('gemini api key required'), { statusCode: 401 });
    }

    const modelAction = (params && params.modelAction) || '';
    const { model, action } = parseModelAction(modelAction);
    // Reconstruct the native Gemini path + query (e.g. ?alt=sse for streaming) and forward verbatim.
    const qs = query && Object.keys(query).length ? '?' + new URLSearchParams(query).toString() : '';
    const reqPath = `/v1beta/models/${modelAction}${qs}`;

    let trace = null;
    try {
      trace = createProxyTrace({
        route: `POST /v1beta/models/${modelAction}`,
        headers: inboundHeaders,
        body,
        upstreamMode: 'gemini',
        originalModel: model,
        chosenModel: model,
        store: traceStore,
        logger: traceStore ? log : null,
        onTraceQueued,
      });
    } catch (_) { /* best-effort trace; never break the request */ }

    let upstream;
    try {
      upstream = await geminiProxy(reqPath, body, { inboundHeaders, upstreamMode: 'gemini' });
    } catch (err) {
      const wrapped = asUpstreamError(err, upstreamStatus(err));
      trace?.record({ status: wrapped.statusCode, error: wrapped, upstreamMode: 'gemini', model });
      throw wrapped;
    }

    if (upstream.stream) {
      const forwardHeaders = copyGeminiResponseHeaders(upstream.headers);
      const ct = upstream.headers && upstream.headers['content-type'];
      if (ct) forwardHeaders['Content-Type'] = ct;
      trace?.recordStreamStart({ status: upstream.status, upstreamMode: 'gemini', model, headers: forwardHeaders });
      return {
        status: upstream.status,
        // Tee the Gemini SSE body so the deferred trace captures usageMetadata + finishReason. Bytes unchanged.
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
        trace?.record({ status: wrapped.statusCode, error: wrapped, upstreamMode: 'gemini', model });
        throw wrapped;
      }
    }
    const respBody = responseToBody(raw, upstream.status, upstream.headers, log);
    trace?.record({ status: upstream.status, responseBody: respBody, upstreamMode: 'gemini', model, headers: upstream.headers });
    return {
      status: upstream.status,
      body: respBody,
      headers: copyGeminiResponseHeaders(upstream.headers),
    };
  };
}

module.exports = {
  buildGeminiHandler,
  copyGeminiResponseHeaders,
  hasGeminiUpstreamCredential,
  responseToBody,
  parseModelAction,
};
