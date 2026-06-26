'use strict';

// Ollama native passthrough (local/self-hosted model server). Native paths POST /api/chat and /api/generate are
// forwarded verbatim to the Ollama upstream (EVOMAP_OLLAMA_BASE_URL, default 127.0.0.1:11434). Format-aware, no
// translation: an Ollama-shaped request goes to Ollama. Streaming is newline-delimited JSON (NDJSON), not SSE —
// the trace tee scans it the same way. apiPath is fixed per registration (/api/chat vs /api/generate). Ollama is
// typically auth-less; an optional bearer (EVOMAP_OLLAMA_API_KEY) covers a remote/protected instance.

const { createProxyTrace } = require('../trace/extractor');

function upstreamStatus(err, fallback = 502) {
  const status = Number(err && err.statusCode);
  return Number.isFinite(status) ? status : fallback;
}

function asUpstreamError(err, fallback = 502) {
  if (err && err.statusCode && /^ollama upstream /.test(err.message || '')) return err;
  const out = new Error('ollama upstream request failed');
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
      event: 'ollama_fallback',
      reason: 'upstream_non_json',
      upstream_status: status,
      content_type: (headers && headers['content-type']) || '',
      response_bytes: Buffer.byteLength(raw),
    }));
    return { error: raw };
  }
}

function buildOllamaHandler({ ollamaProxy, logger, traceStore, onTraceQueued, apiPath = '/api/chat' } = {}) {
  if (typeof ollamaProxy !== 'function') {
    throw new Error('buildOllamaHandler requires ollamaProxy(path, body, opts)');
  }
  const log = logger || console;

  return async ({ body, headers }) => {
    const inboundHeaders = headers || {};
    const originalModel = body && typeof body.model === 'string' ? body.model : null;

    let trace = null;
    try {
      trace = createProxyTrace({
        route: `POST ${apiPath}`,
        headers: inboundHeaders,
        body,
        upstreamMode: 'ollama',
        originalModel,
        chosenModel: originalModel,
        store: traceStore,
        logger: traceStore ? log : null,
        onTraceQueued,
      });
    } catch (_) { /* best-effort trace; never break the request */ }

    let upstream;
    try {
      upstream = await ollamaProxy(apiPath, body, { inboundHeaders, upstreamMode: 'ollama' });
    } catch (err) {
      const wrapped = asUpstreamError(err, upstreamStatus(err));
      trace?.record({ status: wrapped.statusCode, error: wrapped, upstreamMode: 'ollama', model: originalModel });
      throw wrapped;
    }

    if (upstream.stream) {
      const forwardHeaders = {};
      const ct = upstream.headers && upstream.headers['content-type'];
      if (ct) forwardHeaders['Content-Type'] = ct;
      trace?.recordStreamStart({ status: upstream.status, upstreamMode: 'ollama', model: originalModel, headers: forwardHeaders });
      return {
        status: upstream.status,
        // Tee the NDJSON body so the deferred trace captures the final chunk's eval counts + done_reason. Bytes unchanged.
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
        trace?.record({ status: wrapped.statusCode, error: wrapped, upstreamMode: 'ollama', model: originalModel });
        throw wrapped;
      }
    }
    const respBody = responseToBody(raw, upstream.status, upstream.headers, log);
    trace?.record({ status: upstream.status, responseBody: respBody, upstreamMode: 'ollama', model: originalModel, headers: upstream.headers });
    return { status: upstream.status, body: respBody };
  };
}

module.exports = { buildOllamaHandler, responseToBody };
