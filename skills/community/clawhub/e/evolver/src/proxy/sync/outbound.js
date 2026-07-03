'use strict';

const { PROXY_PROTOCOL_VERSION } = require('../mailbox/store');
const { AuthError } = require('../lifecycle/manager');
const { isProxyTraceUploadPayloadAllowed, resolveTraceMode } = require('../trace/extractor');
const {
  hubFetch,
  hubUnreachableBackoffMs,
  isHubUnreachableError,
  readHubResponseJson,
  readHubResponseText,
  sanitizeHubResponseForLog,
  throwIfHubUnreachableResponse,
} = require('../../gep/hubFetch');
const { redactString } = require('../../gep/sanitize');

const MAX_BATCH = 50;
const MAX_RETRIES = 10;
const DEFAULT_MAX_OUTBOUND_BODY_BYTES = 4 * 1024 * 1024;
const MIN_ADAPTIVE_OUTBOUND_BODY_BYTES = 16 * 1024;
const OUTBOUND_BODY_BYTES_STATE_KEY = 'outbound_sync_max_body_bytes';

function sanitizeHubErrorMessage(value) {
  if (typeof sanitizeHubResponseForLog === 'function') {
    return sanitizeHubResponseForLog(value);
  }

  let text;
  if (typeof value === 'string') {
    text = value;
  } else if (value && typeof value.message === 'string') {
    text = value.message;
  } else {
    try { text = JSON.stringify(value); } catch { text = String(value || ''); }
  }
  return redactString(String(text || ''));
}

function resolveHardOutboundBodyBytes(env = process.env) {
  const raw = Number(env.EVOMAP_OUTBOUND_SYNC_MAX_BODY_BYTES || env.EVOMAP_MAILBOX_OUTBOUND_MAX_BODY_BYTES);
  const max = Number.isFinite(raw) && raw > 0
    ? Math.floor(raw)
    : DEFAULT_MAX_OUTBOUND_BODY_BYTES;
  return Math.max(1, max);
}

function resolveMaxOutboundBodyBytes(env = process.env, store = null) {
  let max = resolveHardOutboundBodyBytes(env);
  try {
    const adaptive = Number(store && typeof store.getState === 'function'
      ? store.getState(OUTBOUND_BODY_BYTES_STATE_KEY)
      : null);
    if (Number.isFinite(adaptive) && adaptive > 0) max = Math.min(max, Math.floor(adaptive));
  } catch { /* adaptive state is best-effort */ }
  return Math.max(1, max);
}

function hubMessage(m) {
  return {
    id: m.id,
    type: m.type,
    payload: m.payload,
    priority: m.priority,
    ref_id: m.ref_id,
    created_at: m.created_at,
  };
}

function serializeOutboundBody(senderId, messages) {
  return JSON.stringify({
    sender_id: senderId,
    proxy_protocol_version: PROXY_PROTOCOL_VERSION,
    messages: messages.map(hubMessage),
  });
}

function outboundEndpoint(hubUrl, senderId) {
  const endpoint = new URL(`${String(hubUrl || '').replace(/\/+$/, '')}/a2a/mailbox/outbound`);
  if (senderId) endpoint.searchParams.set('sender_id', senderId);
  return endpoint.toString();
}

function outboundBodyBytes(senderId, messages) {
  return Buffer.byteLength(serializeOutboundBody(senderId, messages), 'utf8');
}

function buildSizedOutboundBatch(senderId, messages, maxBodyBytes, hardMaxBodyBytes = maxBodyBytes) {
  const selected = [];
  const rejected = [];
  let body = serializeOutboundBody(senderId, selected);
  let bodyBytes = Buffer.byteLength(body, 'utf8');

  for (const m of messages) {
    const singleBytes = outboundBodyBytes(senderId, [m]);
    if (singleBytes > hardMaxBodyBytes) {
      rejected.push({
        id: m.id,
        status: 'rejected',
        error: `outbound message exceeds max body bytes (${singleBytes} > ${hardMaxBodyBytes})`,
      });
      continue;
    }
    if (selected.length === 0 && singleBytes > maxBodyBytes) {
      selected.push(m);
      body = serializeOutboundBody(senderId, selected);
      bodyBytes = Buffer.byteLength(body, 'utf8');
      break;
    }

    const candidate = selected.concat(m);
    const candidateBody = serializeOutboundBody(senderId, candidate);
    const candidateBytes = Buffer.byteLength(candidateBody, 'utf8');
    if (candidateBytes > maxBodyBytes) break;

    selected.push(m);
    body = candidateBody;
    bodyBytes = candidateBytes;
  }

  return { selected, rejected, body, bodyBytes, maxBodyBytes };
}

class OutboundSync {
  constructor({ store, hubUrl, getHeaders, logger }) {
    this.store = store;
    this.hubUrl = hubUrl;
    this.logger = logger || console;
    this.getHeaders = getHeaders;
    this._hubUnreachableFailures = 0;
    this._hubUnreachableUntil = 0;
  }

  _hubUnreachableWaitMs() {
    return Math.max(0, this._hubUnreachableUntil - Date.now());
  }

  _recordHubReachable() {
    this._hubUnreachableFailures = 0;
    this._hubUnreachableUntil = 0;
  }

  _recordHubUnreachable(err) {
    this._hubUnreachableFailures += 1;
    const retryAfterMs = hubUnreachableBackoffMs(this._hubUnreachableFailures);
    this._hubUnreachableUntil = Date.now() + retryAfterMs;
    this.logger.warn?.(
      `[outbound] Hub unreachable; backing off for ${Math.ceil(retryAfterMs / 1000)}s: ` +
        `${err && err.message || err}`
    );
    return retryAfterMs;
  }

  async flush(channel = 'evomap-hub') {
    const waitMs = this._hubUnreachableWaitMs();
    if (waitMs > 0) {
      return {
        sent: 0,
        error: 'hub_unreachable_backoff',
        hubUnreachable: true,
        retryAfterMs: waitMs,
      };
    }

    const pendingBatch = this.store.pollOutbound({ channel, limit: MAX_BATCH });
    if (pendingBatch.length === 0) return { sent: 0 };

    let pending = pendingBatch;
    const rejectedTraceUploads = [];
    const traceUploadEnabled = resolveTraceMode(process.env, { store: this.store });
    for (const m of pendingBatch) {
      if (m.type !== 'proxy_trace') continue;
      if (!traceUploadEnabled) {
        rejectedTraceUploads.push({ id: m.id, error: 'proxy trace upload disabled' });
      } else if (!isProxyTraceUploadPayloadAllowed(m.payload, process.env, { store: this.store })) {
        rejectedTraceUploads.push({ id: m.id, error: 'proxy trace payload rejected' });
      }
    }
    if (rejectedTraceUploads.length > 0) {
      this.store.updateStatusBatch(rejectedTraceUploads.map(m => ({
        id: m.id,
        status: 'rejected',
        error: m.error,
      })));
      const rejectedIds = new Set(rejectedTraceUploads.map(m => m.id));
      pending = pendingBatch.filter(m => !rejectedIds.has(m.id));
      if (pending.length === 0) return { sent: 0, dropped: rejectedTraceUploads.length };
    }
    let dropped = rejectedTraceUploads.length;

    try {
      const senderId = this.store.getState('node_id');
      const endpoint = outboundEndpoint(this.hubUrl, senderId);
      const prepared = buildSizedOutboundBatch(
        senderId,
        pending,
        resolveMaxOutboundBodyBytes(process.env, this.store),
        resolveHardOutboundBodyBytes(process.env)
      );
      if (prepared.rejected.length > 0) {
        this.store.updateStatusBatch(prepared.rejected);
        dropped += prepared.rejected.length;
      }
      pending = prepared.selected;
      if (pending.length === 0) return { sent: 0, dropped };

      const res = await hubFetch(endpoint, {
        method: 'POST',
        headers: this.getHeaders(),
        body: prepared.body,
        signal: AbortSignal.timeout(30_000),
      });

      if (res.status === 413) {
        const errText = sanitizeHubErrorMessage(
          await readHubResponseText(res).catch(() => 'request entity too large')
        );
        const error = `Hub 413 outbound payload too large: ${errText}`;
        if (pending.length <= 1) {
          this.store.updateStatusBatch(pending.map(m => ({
            id: m.id,
            status: 'rejected',
            error,
          })));
          const result = {
            sent: 0,
            error: 'hub_payload_too_large',
            payloadTooLarge: true,
            dropped: dropped + pending.length,
          };
          return result;
        }
        const currentCeiling = Math.min(prepared.maxBodyBytes, Math.max(1, prepared.bodyBytes - 1));
        const nextMax = currentCeiling > MIN_ADAPTIVE_OUTBOUND_BODY_BYTES
          ? Math.max(MIN_ADAPTIVE_OUTBOUND_BODY_BYTES, Math.floor(currentCeiling / 2))
          : Math.max(1, Math.floor(currentCeiling / 2));
        try { this.store.setState(OUTBOUND_BODY_BYTES_STATE_KEY, nextMax); } catch { /* best effort */ }
        this.logger.warn?.(
          `[outbound] Hub 413 for ${pending.length} messages (${prepared.bodyBytes} bytes); ` +
            `reducing outbound batch budget to ${nextMax} bytes`
        );
        const result = { sent: 0, error: 'hub_payload_too_large', payloadTooLarge: true };
        if (dropped > 0) result.dropped = dropped;
        return result;
      }

      await throwIfHubUnreachableResponse(res, 'outbound flush');
      this._recordHubReachable();

      if (res.status === 403 || res.status === 401) {
        const errText = sanitizeHubErrorMessage(await readHubResponseText(res).catch(() => 'unknown'));
        throw new AuthError(`Hub ${res.status}: ${errText}`, res.status);
      }

      if (!res.ok) {
        const errText = sanitizeHubErrorMessage(await readHubResponseText(res).catch(() => 'unknown'));
        throw new Error(`Hub returned ${res.status}: ${errText}`);
      }

      const data = await readHubResponseJson(res);
      const results = data.results || [];

      const updates = [];
      const inboundMessages = [];

      for (const r of results) {
        if (r.status === 'accepted' || r.status === 'ok') {
          updates.push({ id: r.id, status: 'synced' });
        } else if (r.status === 'failed' || r.status === 'rejected') {
          const msg = pending.find(m => m.id === r.id);
          const error = sanitizeHubErrorMessage(r.error || 'rejected by hub');
          if (msg && msg.retry_count < MAX_RETRIES) {
            this.store.incrementRetry(r.id, error);
          } else {
            updates.push({ id: r.id, status: 'failed', error: sanitizeHubErrorMessage(r.error || 'max retries') });
          }
        }

        if (r.response) {
          inboundMessages.push({
            type: `${r.original_type || 'unknown'}_result`,
            payload: r.response,
            refId: r.id,
            channel,
          });
        }
      }

      if (updates.length > 0) this.store.updateStatusBatch(updates);
      if (inboundMessages.length > 0) this.store.writeInboundBatch(inboundMessages);

      this.store.setState('last_sync_at', new Date().toISOString());
      const result = { sent: pending.length, synced: updates.length, responses: inboundMessages.length };
      if (dropped > 0) result.dropped = dropped;
      return result;
    } catch (err) {
      if (err instanceof AuthError) throw err;
      if (isHubUnreachableError(err)) {
        const retryAfterMs = this._recordHubUnreachable(err);
        const result = {
          sent: 0,
          error: 'hub_unreachable',
          hubUnreachable: true,
          retryAfterMs,
        };
        if (dropped > 0) result.dropped = dropped;
        return result;
      }
      const errMessage = sanitizeHubErrorMessage(err);
      this.logger.error(`[outbound] flush failed: ${errMessage}`);
      for (const m of pending) {
        this.store.incrementRetry(m.id, errMessage);
      }
      const result = { sent: 0, error: errMessage };
      if (dropped > 0) result.dropped = dropped;
      return result;
    }
  }
}

module.exports = { OutboundSync, MAX_BATCH, MAX_RETRIES };
