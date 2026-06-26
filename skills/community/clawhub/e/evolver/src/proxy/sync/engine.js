'use strict';

const { OutboundSync } = require('./outbound');
const { InboundSync, DEFAULT_POLL_INTERVAL_ACTIVE, DEFAULT_POLL_INTERVAL_IDLE } = require('./inbound');
const { AuthError } = require('../lifecycle/manager');

const DEFAULT_OUTBOUND_INTERVAL = 5_000;
const IDLE_THRESHOLD = 5 * 60_000;

class SyncEngine {
  constructor({ store, hubUrl, getHeaders, logger, onInboundReceived, onAuthError, onOutboundFlushed }) {
    this.store = store;
    this.hubUrl = hubUrl;
    this.logger = logger || console;
    this.getHeaders = getHeaders;
    this.onInboundReceived = onInboundReceived || null;
    this.onAuthError = onAuthError || null;
    this.onOutboundFlushed = onOutboundFlushed || null;

    this.outbound = new OutboundSync({ store, hubUrl, getHeaders, logger });
    this.inbound = new InboundSync({ store, hubUrl, getHeaders, logger });

    this._outTimer = null;
    this._inTimer = null;
    this._running = false;
    this._lastActivity = Date.now();
  }

  start() {
    if (this._running) return;
    this._running = true;
    this._lastActivity = Date.now();
    this._scheduleOutbound(500);
    this._scheduleInbound(1_000);
    this.logger.log('[sync] engine started');
  }

  stop() {
    this._running = false;
    if (this._outTimer) { clearTimeout(this._outTimer); this._outTimer = null; }
    if (this._inTimer) { clearTimeout(this._inTimer); this._inTimer = null; }
    this.logger.log('[sync] engine stopped');
  }

  notifyNewOutbound() {
    this._lastActivity = Date.now();
    if (this._running && !this._outPending) {
      if (this._outTimer) clearTimeout(this._outTimer);
      this._scheduleOutbound(100);
    }
  }

  _isIdle() {
    return (Date.now() - this._lastActivity) > IDLE_THRESHOLD;
  }

  async _handleAuthError(source) {
    this.logger.error(`[sync] auth error from ${source}, triggering re-authentication`);
    if (typeof this.onAuthError === 'function') {
      try { await this.onAuthError(); } catch (e) {
        this.logger.error(`[sync] onAuthError callback failed: ${e.message}`);
      }
    }
  }

  _scheduleOutbound(delayMs) {
    if (!this._running) return;
    this._outTimer = setTimeout(async () => {
      // Defence-in-depth: a throw from this.outbound.flush(),
      // this.store.countPending(), or any post-flush bookkeeping used
      // to escape the setTimeout callback. Node logs the unhandled
      // rejection and the next setTimeout was never armed — the
      // outbound sync loop silently died until the process restarted,
      // while `_running` stayed true (no signal to the caller).
      //
      // Mirrors the heartbeat-loop fix in PR #147 (issue #544): wrap
      // the whole tick, schedule the next iteration in `finally` so a
      // surprise throw cannot park the loop.
      let nextDelay = DEFAULT_OUTBOUND_INTERVAL;
      let hubRetryAfterMs = 0;
      try {
        if (!this._running) return;
        this._outPending = true;
        try {
          const result = await this.outbound.flush();
          if (result.sent > 0) this._lastActivity = Date.now();
          if (result.retryAfterMs > 0) hubRetryAfterMs = result.retryAfterMs;
          if ((result.sent > 0 || result.dropped > 0) && typeof this.onOutboundFlushed === 'function') {
            try { this.onOutboundFlushed(result); } catch (e) {
              this.logger.warn?.('[sync] onOutboundFlushed callback failed:', e.message);
            }
          }
        } catch (err) {
          if (err instanceof AuthError) {
            await this._handleAuthError('outbound');
          } else {
            this.logger.error(`[sync] outbound error: ${err.message}`);
          }
        }
        this._outPending = false;
        if (hubRetryAfterMs > 0) {
          nextDelay = Math.max(1_000, hubRetryAfterMs);
        } else {
          try {
            const pending = this.store.countPending({ direction: 'outbound' });
            if (pending > 0) nextDelay = 1_000;
          } catch (err) {
            // countPending threw (corrupt store, FS hiccup): keep the
            // default cadence rather than parking the loop.
            this.logger.error(`[sync] countPending threw (non-fatal): ${err && err.message}`);
          }
        }
      } catch (err) {
        // Anything that escaped the inner blocks above. Log and let
        // finally re-arm the timer.
        this.logger.error(`[sync] outbound tick threw (non-fatal): ${err && err.message}`);
        this._outPending = false;
      } finally {
        if (this._running) this._scheduleOutbound(nextDelay);
      }
    }, delayMs);
    if (this._outTimer.unref) this._outTimer.unref();
  }

  _scheduleInbound(delayMs) {
    if (!this._running) return;
    this._inTimer = setTimeout(async () => {
      // Same defence-in-depth pattern as _scheduleOutbound: a throw
      // from inbound.pull / ackDelivered / _isIdle used to escape the
      // setTimeout callback and silently park the inbound loop.
      let nextDelay = DEFAULT_POLL_INTERVAL_ACTIVE;
      let hubRetryAfterMs = 0;
      try {
        if (!this._running) return;
        try {
          const result = await this.inbound.pull();
          if (result.retryAfterMs > 0) {
            hubRetryAfterMs = result.retryAfterMs;
          } else if (result.received > 0) {
            this._lastActivity = Date.now();
            if (typeof this.onInboundReceived === 'function') {
              try { this.onInboundReceived(result.received); } catch (e) {
                this.logger.warn?.('[sync] onInboundReceived callback failed:', e.message);
              }
            }
          }
          if (!hubRetryAfterMs) {
            const ack = await this.inbound.ackDelivered();
            if (ack.retryAfterMs > 0) hubRetryAfterMs = ack.retryAfterMs;
          }
        } catch (err) {
          if (err instanceof AuthError) {
            await this._handleAuthError('inbound');
          } else {
            this.logger.error(`[sync] inbound error: ${err.message}`);
          }
        }
        if (hubRetryAfterMs > 0) {
          nextDelay = Math.max(1_000, hubRetryAfterMs);
        } else {
          try {
            nextDelay = this._isIdle()
              ? DEFAULT_POLL_INTERVAL_IDLE
              : DEFAULT_POLL_INTERVAL_ACTIVE;
          } catch (err) {
            this.logger.error(`[sync] _isIdle threw (non-fatal): ${err && err.message}`);
          }
        }
      } catch (err) {
        this.logger.error(`[sync] inbound tick threw (non-fatal): ${err && err.message}`);
      } finally {
        if (this._running) this._scheduleInbound(nextDelay);
      }
    }, delayMs);
    if (this._inTimer.unref) this._inTimer.unref();
  }
}

module.exports = { SyncEngine, DEFAULT_OUTBOUND_INTERVAL };
