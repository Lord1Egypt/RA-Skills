'use strict';

const { PROXY_PROTOCOL_VERSION } = require('../mailbox/store');
const { AuthError } = require('../lifecycle/manager');
const {
  drainHubResponse,
  hubFetch,
  hubUnreachableBackoffMs,
  isHubUnreachableError,
  readHubResponseJson,
  readHubResponseText,
  sanitizeHubResponseForLog,
  throwIfHubUnreachableResponse,
} = require('../../gep/hubFetch');

const DEFAULT_POLL_INTERVAL_ACTIVE = 10_000;
const DEFAULT_POLL_INTERVAL_IDLE = 60_000;

function toInboundStoreMessage(m, channel) {
  return {
    id: m.id,
    type: m.type,
    payload: m.payload,
    channel,
    priority: m.priority || 'normal',
    refId: m.ref_id,
    expiresAt: m.expires_at,
  };
}

class InboundSync {
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
      `[inbound] Hub unreachable; backing off for ${Math.ceil(retryAfterMs / 1000)}s: ` +
        `${err && err.message || err}`
    );
    return retryAfterMs;
  }

  async pull(channel = 'evomap-hub', limit = 50) {
    const waitMs = this._hubUnreachableWaitMs();
    if (waitMs > 0) {
      return {
        received: 0,
        error: 'hub_unreachable_backoff',
        hubUnreachable: true,
        retryAfterMs: waitMs,
      };
    }

    const cursorKey = `${channel}:inbound_cursor`;
    const cursor = this.store.getCursor(cursorKey);

    const endpoint = `${this.hubUrl}/a2a/mailbox/inbound`;

    try {
      const senderId = this.store.getState('node_id');
      const res = await hubFetch(endpoint, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify({ sender_id: senderId, proxy_protocol_version: PROXY_PROTOCOL_VERSION, cursor, limit }),
        signal: AbortSignal.timeout(35_000),
      });

      await throwIfHubUnreachableResponse(res, 'inbound pull');
      this._recordHubReachable();

      if (res.status === 403 || res.status === 401) {
        const errText = await readHubResponseText(res).catch(() => 'unknown');
        throw new AuthError(`Hub ${res.status}: ${sanitizeHubResponseForLog(errText)}`, res.status);
      }

      if (!res.ok) {
        const errText = await readHubResponseText(res).catch(() => 'unknown');
        throw new Error(`Hub returned ${res.status}: ${sanitizeHubResponseForLog(errText)}`);
      }

      const data = await readHubResponseJson(res);
      const messages = data.messages || [];
      let stored = 0;
      let dropped = 0;

      if (messages.length > 0) {
        for (const m of messages) {
          try {
            this.store.writeInbound(toInboundStoreMessage(m, channel));
            stored++;
          } catch (err) {
            if (err && err.code === 'MAILBOX_JSONL_LINE_TOO_LARGE') {
              dropped++;
              const msgId = m && m.id ? String(m.id) : '(missing id)';
              this.logger.warn?.(`[inbound] dropped oversized inbound message ${msgId}: ${err.message}`);
              continue;
            }
            throw err;
          }
        }
      }

      if (data.next_cursor) {
        this.store.setCursor(cursorKey, data.next_cursor);
      }

      const result = { received: stored, cursor: data.next_cursor || cursor };
      if (dropped > 0) result.dropped = dropped;
      return result;
    } catch (err) {
      if (err instanceof AuthError) throw err;
      if (isHubUnreachableError(err)) {
        const retryAfterMs = this._recordHubUnreachable(err);
        return {
          received: 0,
          error: 'hub_unreachable',
          hubUnreachable: true,
          retryAfterMs,
        };
      }
      this.logger.error(`[inbound] pull failed: ${err.message}`);
      return { received: 0, error: err.message };
    }
  }

  async ackDelivered(channel = 'evomap-hub') {
    const waitMs = this._hubUnreachableWaitMs();
    if (waitMs > 0) {
      return {
        acked: 0,
        error: 'hub_unreachable_backoff',
        hubUnreachable: true,
        retryAfterMs: waitMs,
      };
    }

    const delivered = this.store.list({
      type: '%',
      direction: 'inbound',
      status: 'delivered',
      limit: 100,
    }).filter(m => m.channel === channel);

    if (delivered.length === 0) return { acked: 0 };

    const endpoint = `${this.hubUrl}/a2a/mailbox/ack`;

    try {
      const senderId = this.store.getState('node_id');
      // Round-8 (§21.5): drain the response body so the undici long-poll
      // dispatcher pool is not leaked one socket per ack. ackDelivered
      // is called every inbound poll cycle (default 1-10s); the
      // pre-round-8 code captured no reference to res and never called
      // .json()/.text()/body.cancel(), so each ack pinned a socket
      // until GC. After a few minutes of activity the strict-pool was
      // exhausted and proxy-mode heartbeats hung on next acquire --
      // matches the "alive once then dead" user symptom in proxy mode.
      const res = await hubFetch(endpoint, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify({ sender_id: senderId, message_ids: delivered.map(m => m.id) }),
        signal: AbortSignal.timeout(10_000),
      });
      await throwIfHubUnreachableResponse(res, 'inbound ack');
      this._recordHubReachable();
      if (res.status === 403 || res.status === 401) {
        const errText = await readHubResponseText(res).catch(() => 'unknown');
        throw new AuthError(`Hub ${res.status}: ${sanitizeHubResponseForLog(errText)}`, res.status);
      }
      if (!res.ok) {
        const errText = await readHubResponseText(res).catch(() => 'unknown');
        throw new Error(`Hub returned ${res.status}: ${sanitizeHubResponseForLog(errText)}`);
      }
      await drainHubResponse(res);
      return { acked: delivered.length };
    } catch (err) {
      if (err instanceof AuthError) throw err;
      if (isHubUnreachableError(err)) {
        const retryAfterMs = this._recordHubUnreachable(err);
        return {
          acked: 0,
          error: 'hub_unreachable',
          hubUnreachable: true,
          retryAfterMs,
        };
      }
      this.logger.error(`[inbound] ack failed: ${err.message}`);
      return { acked: 0, error: err.message };
    }
  }
}

module.exports = { InboundSync, DEFAULT_POLL_INTERVAL_ACTIVE, DEFAULT_POLL_INTERVAL_IDLE };
