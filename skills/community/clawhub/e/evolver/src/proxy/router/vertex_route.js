'use strict';

// Vertex AI Gemini passthrough (enterprise GCP). Same Gemini request/response body as the AI Studio route, but
// the native Vertex path — POST /v1/projects/<project>/locations/<location>/publishers/google/models/<model>:
// generateContent | :streamGenerateContent — a region-specific upstream (<location>-aiplatform.googleapis.com),
// and OAuth Bearer auth (EVOMAP_VERTEX_ACCESS_TOKEN). Forwarded verbatim, no translation. Trace reuses the Gemini
// shape (usageMetadata + candidates[].finishReason), so only the path + base + auth differ from the AI Studio route.

const { createProxyTrace } = require('../trace/extractor');
const { parseModelAction } = require('./gemini_route');

function upstreamStatus(err, fallback = 502) {
  const status = Number(err && err.statusCode);
  return Number.isFinite(status) ? status : fallback;
}

function asUpstreamError(err, fallback = 502) {
  if (err && err.statusCode && /^vertex /.test(err.message || '')) return err;
  const out = new Error('vertex upstream request failed');
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
      event: 'vertex_fallback', reason: 'upstream_non_json', upstream_status: status,
      content_type: (headers && headers['content-type']) || '', response_bytes: Buffer.byteLength(raw),
    }));
    return { error: raw };
  }
}

// Region-specific Vertex base. EVOMAP_VERTEX_BASE_URL overrides (e.g. the global aiplatform endpoint); otherwise
// derive <location>-aiplatform.googleapis.com. `global` uses the un-prefixed host.
function vertexBaseUrl(location) {
  const override = (process.env.EVOMAP_VERTEX_BASE_URL || '').trim();
  if (override) return override.replace(/\/+$/, '');
  const loc = String(location || '').trim();
  if (!loc || loc === 'global') return 'https://aiplatform.googleapis.com';
  return `https://${loc}-aiplatform.googleapis.com`;
}

function buildVertexHandler({ vertexProxy, logger, traceStore, onTraceQueued } = {}) {
  if (typeof vertexProxy !== 'function') {
    throw new Error('buildVertexHandler requires vertexProxy(path, body, opts)');
  }
  const log = logger || console;

  return async ({ body, headers, params, query }) => {
    const inboundHeaders = headers || {};
    const project = (params && params.project) || '';
    const location = (params && params.location) || '';
    const modelAction = (params && params.modelAction) || '';
    const { model } = parseModelAction(modelAction);
    const baseUrl = vertexBaseUrl(location);
    const qs = query && Object.keys(query).length ? '?' + new URLSearchParams(query).toString() : '';
    const reqPath = `/v1/projects/${project}/locations/${location}/publishers/google/models/${modelAction}${qs}`;

    let trace = null;
    try {
      trace = createProxyTrace({
        route: `POST /v1/projects/${project}/locations/${location}/publishers/google/models/${modelAction}`,
        headers: inboundHeaders, body, upstreamMode: 'vertex', originalModel: model, chosenModel: model,
        store: traceStore, logger: traceStore ? log : null, onTraceQueued,
      });
    } catch (_) { /* best-effort trace */ }

    let upstream;
    try {
      upstream = await vertexProxy(reqPath, body, { baseUrl, inboundHeaders, upstreamMode: 'vertex' });
    } catch (err) {
      const wrapped = asUpstreamError(err, upstreamStatus(err));
      trace?.record({ status: wrapped.statusCode, error: wrapped, upstreamMode: 'vertex', model });
      throw wrapped;
    }

    if (upstream.stream) {
      const forwardHeaders = {};
      const ct = upstream.headers && upstream.headers['content-type'];
      if (ct) forwardHeaders['Content-Type'] = ct;
      trace?.recordStreamStart({ status: upstream.status, upstreamMode: 'vertex', model, headers: forwardHeaders });
      return {
        status: upstream.status,
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
        trace?.record({ status: wrapped.statusCode, error: wrapped, upstreamMode: 'vertex', model });
        throw wrapped;
      }
    }
    const respBody = responseToBody(raw, upstream.status, upstream.headers, log);
    trace?.record({ status: upstream.status, responseBody: respBody, upstreamMode: 'vertex', model, headers: upstream.headers });
    return { status: upstream.status, body: respBody };
  };
}

module.exports = { buildVertexHandler, vertexBaseUrl };
