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
  throwIfHubUnreachableResponse,
} = require('../../gep/hubFetch');

const MAX_BATCH = 50;
const MAX_RETRIES = 10;

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
      } else if (!isProxyTraceUploadPayloadAllowed(m.payload, process.env)) {
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
    const dropped = rejectedTraceUploads.length;

    const endpoint = `${this.hubUrl}/a2a/mailbox/outbound`;

    try {
      const senderId = this.store.getState('node_id');
      const res = await hubFetch(endpoint, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify({
          sender_id: senderId,
          proxy_protocol_version: PROXY_PROTOCOL_VERSION,
          messages: pending.map(m => ({
            id: m.id,
            type: m.type,
            payload: m.payload,
            priority: m.priority,
            ref_id: m.ref_id,
            created_at: m.created_at,
          })),
        }),
        signal: AbortSignal.timeout(30_000),
      });

      await throwIfHubUnreachableResponse(res, 'outbound flush');
      this._recordHubReachable();

      if (res.status === 403 || res.status === 401) {
        const errText = await readHubResponseText(res).catch(() => 'unknown');
        throw new AuthError(`Hub ${res.status}: ${errText}`, res.status);
      }

      if (!res.ok) {
        const errText = await readHubResponseText(res).catch(() => 'unknown');
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
          if (msg && msg.retry_count < MAX_RETRIES) {
            this.store.incrementRetry(r.id, r.error || 'rejected by hub');
          } else {
            updates.push({ id: r.id, status: 'failed', error: r.error || 'max retries' });
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
      this.logger.error(`[outbound] flush failed: ${err.message}`);
      for (const m of pending) {
        this.store.incrementRetry(m.id, err.message);
      }
      const result = { sent: 0, error: err.message };
      if (dropped > 0) result.dropped = dropped;
      return result;
    }
  }
}

module.exports = { OutboundSync, MAX_BATCH, MAX_RETRIES };
