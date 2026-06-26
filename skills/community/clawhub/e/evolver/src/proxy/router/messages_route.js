'use strict';

// /v1/messages handler for Phase C. Three pipeline stages wrap _proxyAnthropic:
//   1. extract stateless features  (router/features.js)
//   2. pickForTurn → tier → concrete model (router/model_router.js + DEFAULT_TIER_MODELS)
//   3. rewriteModel preserving cache_control breakpoints (router/cache_passthrough.js)
//
// Each stage has its own fallback so a single bad input never breaks the
// passthrough: classifier throw → forward unmodified; rewriter throw →
// forward unmodified; upstream 5xx on a router-rewritten request → one
// retry with the client's original model (a one-hub/prism-style gateway
// may return 503 "no channel" for a tier-target model the upstream isn't
// configured for; falling back to the original model is more useful than
// a hard 503). All other non-2xx is relayed verbatim — we don't fabricate
// SSE error frames. Telemetry-style log lines record which fallback fired
// so the realized-vs-projected delta is measurable post-merge.

const { pickForTurn } = require('./model_router');
const { rewriteModel } = require('./cache_passthrough');
const { extractFeatures } = require('./features');
const { createProxyTrace } = require('../trace/extractor');

// Bedrock-resolvable global.* aliases as of 2026-05-25:
//   - opus-4-7    : bare alias OK
//   - haiku-4-5   : ONLY the dated form resolves; bare alias 400s
//                   ("ValidationException: invalid model identifier")
//   - sonnet-4-7  : not yet on Bedrock — sonnet-4-6 is the current global.*
//                   sonnet alias. The no-downgrade guard still blocks an
//                   inbound sonnet-4-7 → sonnet-4-6 rewrite, so callers
//                   pinned to 4-7 stay on 4-7.
const DEFAULT_TIER_MODELS = Object.freeze({
  cheap: 'global.anthropic.claude-opus-4-7',
  mid: 'global.anthropic.claude-opus-4-7',
  expensive: 'global.anthropic.claude-opus-4-7',
});

// No-downgrade guard: when the router rewrites a request to a different model
// inside the same Claude family (opus / sonnet / haiku), the chosen generation
// must be >= the original. This catches the 2026-05-25 /compact incident where
// EVOMAP_MODEL_EXPENSIVE was misconfigured to opus-4-1 while users sent
// opus-4-7 — every planning turn silently rewrote 4-7 → 4-1, hit Bedrock 5xx
// on the older endpoint, and stalled the user behind retries. Cross-family
// rewrites (opus → haiku for cheap tier) are the router's core function and
// stay allowed; this guard only blocks intra-family generational downgrades.
//
// Parsers below handle two ID shapes the proxy actually sees:
//   - global.anthropic.claude-{family}-{major}-{minor}
//   - us.anthropic.claude-{family}-{major}-{minor}-YYYYMMDD-v1:0  (Bedrock dated)
// Anything else (third-party, opaque alias) → null on both fields → guard
// returns false (allow). We only block when we can prove the comparison.
function parseClaudeId(modelId) {
  if (typeof modelId !== 'string') return null;
  const m = modelId.match(/claude-(opus|sonnet|haiku)-(\d+)-(\d+)/i);
  if (!m) return null;
  const major = Number(m[2]);
  const minor = Number(m[3]);
  if (!Number.isFinite(major) || !Number.isFinite(minor)) return null;
  return { family: m[1].toLowerCase(), major, minor };
}

function isIntraFamilyDowngrade(chosen, original) {
  const c = parseClaudeId(chosen);
  const o = parseClaudeId(original);
  if (!c || !o) return false;
  if (c.family !== o.family) return false;
  if (c.major !== o.major) return c.major < o.major;
  return c.minor < o.minor;
}

// Bedrock InvokeModel rejects bare short IDs like `claude-opus-4-7` with
// ValidationException — it only accepts the explicit ARN-shaped aliases
// below. CC clients and many SDKs route via short IDs since that's what
// api.anthropic.com expects, so when upstreamMode === 'bedrock' we
// canonicalize at the proxy boundary. Unknown / non-Claude IDs pass
// through untouched (Bedrock owns the rejection in that case).
//
// Map keys are `family/major/minor` from parseClaudeId. Add new entries
// here as Anthropic ships new Bedrock aliases.
const KNOWN_BEDROCK_ALIASES = Object.freeze({
  'opus/4/7': 'global.anthropic.claude-opus-4-7',
  'haiku/4/5': 'global.anthropic.claude-haiku-4-5-20251001-v1:0',
  'sonnet/4/6': 'global.anthropic.claude-sonnet-4-6',
});

function canonicalizeForBedrock(modelId) {
  const parsed = parseClaudeId(modelId);
  if (!parsed) return modelId;
  const key = `${parsed.family}/${parsed.major}/${parsed.minor}`;
  return KNOWN_BEDROCK_ALIASES[key] || modelId;
}

function supportsAdaptiveThinking(modelId) {
  const parsed = parseClaudeId(modelId);
  if (!parsed) return false;
  if (parsed.major > 4) return true;
  return parsed.major === 4 && parsed.minor >= 7;
}

function resolveTierModels() {
  return {
    cheap: process.env.EVOMAP_MODEL_CHEAP || DEFAULT_TIER_MODELS.cheap,
    mid: process.env.EVOMAP_MODEL_MID || DEFAULT_TIER_MODELS.mid,
    expensive: process.env.EVOMAP_MODEL_EXPENSIVE || DEFAULT_TIER_MODELS.expensive,
  };
}

function buildMessagesHandler({ anthropicProxy, logger, routerEnabled, traceStore, onTraceQueued } = {}) {
  if (typeof anthropicProxy !== 'function') {
    throw new Error('buildMessagesHandler requires anthropicProxy(path, body, opts)');
  }
  const log = logger || console;
  // Phase C slice 6: flag is read at handler construction (proxy start), not
  // per-request — flipping the env var requires a proxy restart, fine for an
  // MVP feature flag. Explicit boolean override wins so tests stay hermetic.
  const enabled = typeof routerEnabled === 'boolean'
    ? routerEnabled
    : process.env.EVOMAP_ROUTER_ENABLED === '1';

  // Degenerate-tier guard (#152). The shipped DEFAULT_TIER_MODELS pins all
  // three tiers to the same model on purpose: operators tuning tier mapping
  // run tier-uniform so the no-downgrade guard never engages and 5xx retries
  // always replay the same model (PR #135). Per-tier `EVOMAP_MODEL_*` env
  // overrides are how a real deployment opts into cost-saving. The trap is the
  // user who flips `EVOMAP_ROUTER_ENABLED=1` expecting savings (per README)
  // but leaves the overrides unset: every tier resolves to one model, so
  // routing is a silent no-op and — for anyone previously on a cheaper model —
  // a cost *increase*. Emit one loud boot WARN so the degenerate config is
  // visible in logs instead of manifesting as a surprise bill. Resolved at
  // construction (proxy start) to match how `enabled` is read.
  if (enabled) {
    const tiers = resolveTierModels();
    const distinct = new Set([tiers.cheap, tiers.mid, tiers.expensive]);
    if (distinct.size === 1) {
      log.warn?.(JSON.stringify({
        event: 'router_degenerate_tiers',
        message: 'router enabled but all tiers map to the same model — no '
          + 'cost-saving effect. Set EVOMAP_MODEL_CHEAP / EVOMAP_MODEL_MID / '
          + 'EVOMAP_MODEL_EXPENSIVE to enable tier-based routing.',
        model: tiers.cheap,
      }));
    }
  }

  return async ({ body, headers }) => {
    const inboundHeaders = headers || {};
    // x-api-key is satisfied by either the inbound header OR a proxy-side
    // ANTHROPIC_API_KEY / ANTHROPIC_AUTH_TOKEN env (token mediation, see
    // _proxyAnthropic). The proxy server itself has already auth-checked
    // `Authorization: Bearer <proxy_token>` before reaching this handler.
    //
    // Bedrock upstream uses SigV4 with AWS_* env, so neither inbound
    // x-api-key nor ANTHROPIC_* env are meaningful. Skip the check —
    // the real proxy gate is still the Bearer proxy_token enforced
    // upstream of this handler in ProxyHttpServer.
    // Read EVOMAP_UPSTREAM exactly once per request and thread it through to
    // the proxy callable via opts.upstreamMode. Reading it here AND in the
    // dispatch closure would let a mid-request env hot-swap make the two
    // decisions disagree (e.g. gate skipped on the assumption of bedrock,
    // but the request still hits _proxyAnthropic with no credentials).
    const upstreamMode = (process.env.EVOMAP_UPSTREAM || 'anthropic').toLowerCase();
    if (upstreamMode !== 'bedrock') {
      const hasInboundKey = !!inboundHeaders['x-api-key'];
      const hasProxyEnvCreds = !!(
        process.env.ANTHROPIC_API_KEY
        || process.env.EVOMAP_ANTHROPIC_AUTH_TOKEN
        || (process.env.EVOMAP_PROXY_AUTO_INJECTED === '1' ? '' : process.env.ANTHROPIC_AUTH_TOKEN)
      );
      if (!hasInboundKey && !hasProxyEnvCreds) {
        throw Object.assign(new Error('x-api-key required'), { statusCode: 401 });
      }
    }

    // Phase C ABC fix: in bedrock mode, normalize the inbound model to the
    // Bedrock-resolvable form up front. Client-side IDs like
    // `claude-opus-4-7` are valid on api.anthropic.com but Bedrock's
    // InvokeModel rejects them with ValidationException; the retry path
    // would replay that exact rejected ID and turn an upstream blip into
    // 100% failure. Canonicalizing here makes router decisions, the
    // outbound rewrite, the no-downgrade comparison, and the retry body
    // all see the same Bedrock-OK ID. anthropic mode passes through
    // unchanged so api.anthropic.com keeps accepting short IDs.
    const rawInboundModel = body && typeof body.model === 'string' ? body.model : null;
    const originalModel = upstreamMode === 'bedrock'
      ? canonicalizeForBedrock(rawInboundModel)
      : rawInboundModel;
    let chosenModel = originalModel;
    let decisionTier = null;
    let decisionReason = null;
    let fallback = null;

    if (enabled) {
      try {
        const features = extractFeatures(body);
        const decision = pickForTurn({
          features,
          router_state: { history: [], pinned: null },
          config: { default_tier: 'mid', disable: false, hard_pin_after_plan: false },
        });
        decisionTier = decision.tier;
        decisionReason = decision.reason;
        const tierModel = resolveTierModels()[decision.tier];
        if (tierModel) {
          if (isIntraFamilyDowngrade(tierModel, originalModel)) {
            // Intra-family downgrade detected (e.g. opus-4-7 -> opus-4-1).
            // Refuse the rewrite, keep the user's original model, and log a
            // structured fallback so misconfigured tier env vars are visible
            // in telemetry instead of manifesting as latency / 5xx stalls.
            fallback = 'downgrade_blocked';
            log.warn?.(JSON.stringify({
              event: 'router_fallback',
              reason: 'downgrade_blocked',
              original_model: originalModel,
              would_have_been: tierModel,
            }));
          } else {
            chosenModel = tierModel;
          }
        }
      } catch (err) {
        fallback = 'classifier_error';
        log.warn?.(JSON.stringify({
          event: 'router_fallback',
          reason: 'classifier_error',
          original_model: originalModel,
          would_have_been: null,
          error: err.message,
        }));
      }

    }

    let outboundBody = body;
    // Rewrite the outbound body when chosenModel differs from what the
    // CLIENT actually sent (rawInboundModel), not just from the canonical
    // originalModel. Otherwise bedrock-mode short-ID inbounds where the
    // router didn't change tier (chosenModel === canonical(rawInbound))
    // would forward the original body — leaking the short ID to Bedrock.
    if (enabled && chosenModel && chosenModel !== rawInboundModel) {
      try {
        outboundBody = rewriteModel(body, chosenModel);
      } catch (err) {
        fallback = fallback || 'rewrite_error';
        log.warn?.(JSON.stringify({
          event: 'router_fallback',
          reason: 'rewrite_error',
          original_model: originalModel,
          would_have_been: chosenModel,
          error: err.message,
        }));
        outboundBody = body;
        chosenModel = originalModel;
      }
    }

    if (enabled) {
      log.log?.(JSON.stringify({
        event: 'router_decision',
        tier: decisionTier,
        reason: decisionReason,
        original_model: originalModel,
        chosen_model: chosenModel,
        escalation_skipped: false,
        fallback,
      }));
    }

    // Trace extraction is best-effort observability — it must never break the
    // request. A throwing body accessor (e.g. the simulated classifier failure
    // in routerFeatureFlag) would otherwise propagate out of createProxyTrace /
    // extractCWD and 500 the call. Downstream uses `trace?.`, so null is safe.
    let trace = null;
    try {
      trace = createProxyTrace({
        route: 'POST /v1/messages',
        headers: inboundHeaders,
        body: outboundBody,
        upstreamMode,
        originalModel,
        chosenModel,
        store: traceStore,
        logger: traceStore ? log : null,
        onTraceQueued,
      });
    } catch (_) { /* best-effort trace; never break the request */ }

    let upstream;
    try {
      upstream = await anthropicProxy('/v1/messages', outboundBody, {
        inboundHeaders,
        upstreamMode,
      });
    } catch (err) {
      trace?.record({ status: 502, error: err, upstreamMode, model: chosenModel });
      throw err;
    }

    const recordStreamTrace = (result) => {
      trace?.recordStreamStart({ status: result.status, upstreamMode, model: chosenModel, headers: result.headers });
      // Tee the SSE body so the trace captures end-of-stream usage/finish/response-id. Bytes forward unchanged;
      // observeStream emits the deferred row once the stream ends/cancels/errors.
      if (trace && result.stream) result.stream = trace.observeStream(result.stream);
      return result;
    };

    if (upstream.stream) {
      const forwardHeaders = {};
      const ct = upstream.headers && upstream.headers['content-type'];
      if (ct) forwardHeaders['Content-Type'] = ct;
      return recordStreamTrace({
        status: upstream.status,
        stream: upstream.stream,
        headers: forwardHeaders,
      });
    }

    // First upstream returned non-stream. If it's a 5xx on a router-rewritten
    // request, retry once with the client's original model. This covers the
    // common one-hub/prism case where the chosen tier model has no channel
    // configured — a hard 503 is worse for the caller than a slightly more
    // expensive successful response. The retry may come back streaming when
    // the client originally sent stream:true (the first attempt errored out
    // as JSON before any SSE flowed, so streaming the second attempt is
    // still safe). The result-shape branch below handles both cases.
    let finalUpstream = upstream;
    let finalModel = chosenModel;
    if (
      enabled
      && upstream.status >= 500
      && chosenModel
      && chosenModel !== originalModel
    ) {
      log.warn?.(JSON.stringify({
        event: 'router_fallback',
        reason: 'upstream_5xx_retry',
        original_model: originalModel,
        would_have_been: chosenModel,
        upstream_status: upstream.status,
      }));
      // Drain the first upstream's body before retrying. fetch Response
      // bodies are single-read streams; if the retry succeeds, finalUpstream
      // moves to the retry response and the original `upstream` body is
      // never consumed, so undici keeps the underlying TCP socket pinned
      // in the awaiting-body state. Under sustained 5xx storms from the
      // rewritten model (the exact scenario this branch targets), every
      // successful retry leaks one socket out of the pool.
      //
      // We don't need the parsed body — text() reads the full body before
      // returning, which is enough to release the socket. If the retry
      // throws, finalUpstream stays pointing at the (now-drained) upstream
      // and the .text() at line 195 short-circuits on the empty Response
      // — but that loses the original 503 body, so cache it here too and
      // restore it on the throw path.
      let drainedFirst = '';
      if (upstream.text) {
        // Bound response-body drain to 10s to prevent hanging on large or
        // slow-streaming error responses. If the drain times out, log it
        // but continue — the original 5xx is still cached and will be
        // returned to the caller if the retry throws.
        //
        // Clear the timer when text() resolves first, otherwise the
        // setTimeout sits in the event loop for 10s holding a closure
        // reference. Under sustained 5xx storms (the exact scenario this
        // branch targets) one such timer per retry would accumulate.
        let drainTimer;
        try {
          drainedFirst = await Promise.race([
            upstream.text(),
            new Promise((_, reject) => {
              drainTimer = setTimeout(
                () => reject(new Error('response drain timeout')),
                10_000,
              );
            }),
          ]);
        } catch (e) {
          // socket already gone, timeout, or parse error. Log drain errors
          // and continue with empty body — the retry response will carry the
          // actual error to the caller.
          if (e?.message?.includes('timeout')) {
            log.warn?.(JSON.stringify({
              event: 'router_fallback',
              reason: 'upstream_5xx_drain_timeout',
              original_model: originalModel,
              would_have_been: chosenModel,
            }));
          }
        } finally {
          if (drainTimer) clearTimeout(drainTimer);
        }
      }
      try {
        const retryBody = rewriteModel(body, originalModel);
        finalUpstream = await anthropicProxy('/v1/messages', retryBody, {
          inboundHeaders,
          upstreamMode,
        });
        finalModel = originalModel;
      } catch (err) {
        // Replay the drained first response so the caller still sees the
        // original 503 + body, not an empty stream.
        finalUpstream = {
          status: upstream.status,
          headers: upstream.headers,
          stream: null,
          text: () => drainedFirst,
        };
        finalModel = chosenModel;
        log.warn?.(JSON.stringify({
          event: 'router_fallback',
          reason: 'upstream_5xx_retry_failed',
          original_model: originalModel,
          would_have_been: chosenModel,
          error: err.message,
        }));
      }
    }

    if (finalUpstream.stream) {
      const forwardHeaders = {};
      const ct = finalUpstream.headers && finalUpstream.headers['content-type'];
      if (ct) forwardHeaders['Content-Type'] = ct;
      trace?.recordStreamStart({
        status: finalUpstream.status,
        upstreamMode,
        model: finalModel,
        headers: forwardHeaders,
      });
      return {
        status: finalUpstream.status,
        stream: trace ? trace.observeStream(finalUpstream.stream) : finalUpstream.stream,
        headers: forwardHeaders,
      };
    }
    // Upstream is normally JSON, but a misconfigured local gateway (prism
    // without a route configured), a CDN 4xx page, or a load balancer 502
    // can return text/plain or HTML. Read the body as text (single
    // consumption — fetch Response bodies cannot be read twice) and parse
    // ourselves; on parse failure, wrap the raw text in an {error} envelope
    // so the client gets the real upstream status + a readable body
    // instead of a 500 "Unexpected non-whitespace character".
    // Default to {} not null: src/proxy/server/http.js wraps results as
    // `result.body || result`, and a falsy body would serialize the entire
    // internal {status, body} envelope to the client.
    let respBody = {};
    let raw = '';
    if (finalUpstream.text) {
      try { raw = await finalUpstream.text(); } catch { /* ignore */ }
    }
    if (raw.length > 0) {
      try {
        respBody = JSON.parse(raw);
      } catch {
        respBody = { error: raw };
        log.warn?.(JSON.stringify({
          event: 'router_fallback',
          reason: 'upstream_non_json',
          upstream_status: finalUpstream.status,
          content_type: finalUpstream.headers && finalUpstream.headers['content-type'] || '',
          response_bytes: Buffer.byteLength(raw),
        }));
      }
    }
    trace?.record({
      status: finalUpstream.status,
      responseBody: respBody,
      upstreamMode,
      model: finalModel,
      headers: finalUpstream.headers,
    });
    return { status: finalUpstream.status, body: respBody };
  };
}

module.exports = {
  buildMessagesHandler,
  DEFAULT_TIER_MODELS,
  resolveTierModels,
  parseClaudeId,
  isIntraFamilyDowngrade,
  canonicalizeForBedrock,
  supportsAdaptiveThinking,
  KNOWN_BEDROCK_ALIASES,
};
