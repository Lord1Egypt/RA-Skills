// Arena Agent - WebSocket Client
// Connects to /ws/arena with API key auth for real-time bidirectional gameplay.
// Modeled on tools/hal/hal-client.js PlayerConnection but with Arena API key auth.

import { EventEmitter } from 'events';
import WebSocket from 'ws';
import { ARENA_API_URL, ARENA_API_KEY } from './config.js';

export class ArenaWebSocketClient extends EventEmitter {
  constructor(apiUrl = ARENA_API_URL, apiKey = ARENA_API_KEY, playerId = '') {
    super();
    this.apiUrl = apiUrl.replace(/\/$/, '');
    this.apiKey = apiKey;
    this.playerId = playerId;
    this.ws = null;
    this.gameState = null;
    this.pendingRequests = new Map();
    this._requestCounter = 0;
    this._reconnectAttempts = 0;
    this._maxReconnectAttempts = 10;
    this._reconnectDelay = 1000;
    this._shouldReconnect = true;
    this._connected = false;
  }

  // ── Connection ────────────────────────────────────────────────────────

  async connect() {
    return new Promise((resolve, reject) => {
      const wsUrl = this.apiUrl.replace(/^http/, 'ws') + '/ws/arena';

      this.ws = new WebSocket(wsUrl, {
        headers: {
          'Authorization': `Bearer ${this.apiKey}`,
          'X-Arena-Player-Id': this.playerId,
        },
        maxPayload: 1024 * 1024, // 1MB max inbound
      });

      this.ws.on('open', () => {
        this._connected = true;
        this._reconnectAttempts = 0;
        this._reconnectDelay = 1000;
        this.emit('connected');
      });

      this.ws.on('message', (raw) => {
        try {
          const data = JSON.parse(raw.toString());
          this._handleMessage(data, resolve);
        } catch (e) {
          this.emit('error', new Error(`Invalid JSON: ${e.message}`));
        }
      });

      this.ws.on('close', (code, reason) => {
        this._connected = false;
        this.emit('disconnected', { code, reason: reason?.toString() });
        this._rejectAllPending('Connection closed');

        if (this._shouldReconnect && code !== 4000) {
          this._tryReconnect();
        }
      });

      this.ws.on('error', (err) => {
        this.emit('error', err);
        if (!this._connected) {
          reject(err);
        }
      });

      // Timeout for initial connection
      setTimeout(() => {
        if (!this._connected) {
          this.ws?.terminate();
          reject(new Error('Connection timeout'));
        }
      }, 15000);
    });
  }

  disconnect() {
    this._shouldReconnect = false;
    if (this.ws) {
      this.ws.close(1000, 'Client disconnect');
      this.ws = null;
    }
    this._connected = false;
    this._rejectAllPending('Disconnected');
  }

  get connected() {
    return this._connected && this.ws?.readyState === WebSocket.OPEN;
  }

  // ── Send actions ──────────────────────────────────────────────────────

  /**
   * Send a game action and wait for the response.
   * @param {string} action - Action name (e.g., 'cook', 'buy_gear')
   * @param {object} params - Action parameters
   * @param {string} reasoning - LLM reasoning for this action
   * @param {string} llmModel - LLM model used for this decision
   * @returns {Promise<object>} Action result from server
   */
  async send(action, params = {}, reasoning = '', llmModel = '') {
    if (!this.connected) {
      throw new Error('Not connected');
    }

    const requestId = `r_${++this._requestCounter}_${Date.now()}`;

    const msg = {
      action,
      request_id: requestId,
      ...params,
    };
    if (reasoning) msg.reasoning = reasoning;
    if (llmModel) msg.llm_model = llmModel;

    return new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        this.pendingRequests.delete(requestId);
        reject(new Error(`Action '${action}' timed out after 30s`));
      }, 30000);

      this.pendingRequests.set(requestId, { resolve, reject, timeout, action });

      this.ws.send(JSON.stringify(msg), (err) => {
        if (err) {
          clearTimeout(timeout);
          this.pendingRequests.delete(requestId);
          reject(err);
        }
      });
    });
  }

  // ── Message handling ──────────────────────────────────────────────────

  _handleMessage(data, authResolve) {
    const type = data.type;

    switch (type) {
      case 'auth_ok':
        this.gameState = data;
        this.emit('authenticated', data);
        if (authResolve) authResolve(data);
        break;

      case 'action_result':
        this._handleActionResult(data);
        break;

      case 'tick':
        this._mergeTick(data);
        this.emit('tick', data);
        break;

      case 'deferred_state':
        this._mergeDeferredState(data);
        this.emit('deferred_state', data);
        break;

      case 'notification':
        this._mergeNotification(data);
        this.emit('notification', data);
        break;

      case 'travel_event':
        this.emit('travel_event', data);
        break;

      case 'crew_invite':
        this.emit('crew_invite', data);
        break;

      case 'error':
        if (data.code === 'SESSION_REPLACED') {
          this._shouldReconnect = false;
          this.emit('session_replaced');
        } else {
          this.emit('server_error', data);
        }
        break;

      default:
        this.emit('message', data);
    }
  }

  _handleActionResult(data) {
    const requestId = data.request_id;
    if (requestId && this.pendingRequests.has(requestId)) {
      const pending = this.pendingRequests.get(requestId);
      clearTimeout(pending.timeout);
      this.pendingRequests.delete(requestId);

      if (data.success) {
        pending.resolve(data);
      } else {
        const err = new Error(data.message || data.error || 'Action failed');
        err.code = data.code;
        err.suggestion = data.suggestion;
        err.alternatives = data.alternatives;
        err.data = data;
        pending.reject(err);
      }
    } else {
      // Broadcast action result (e.g., from another player's action affecting us)
      this.emit('action_result', data);
    }
  }

  // ── State merging ─────────────────────────────────────────────────────

  _mergeTick(tick) {
    if (!this.gameState) return;

    // Merge player delta
    if (tick.player_delta && this.gameState.player) {
      Object.assign(this.gameState.player, tick.player_delta);
    }

    // Replace arrays
    if (tick.cook_queue) this.gameState.cook_queue = tick.cook_queue;
    if (tick.dealers) this.gameState.dealers = tick.dealers;
    if (tick.inventory) this.gameState.inventory = tick.inventory;
    if (tick.turfs) this.gameState.turfs = tick.turfs;
    if (tick.gear) this.gameState.gear = tick.gear;
    if (tick.market) this.gameState.market = tick.market;
  }

  _mergeDeferredState(deferred) {
    if (!this.gameState) return;
    for (const [key, value] of Object.entries(deferred)) {
      if (key !== 'type') {
        this.gameState[key] = value;
      }
    }
  }

  _mergeNotification(notif) {
    if (!this.gameState) return;

    const kind = notif.kind || notif.event;
    switch (kind) {
      case 'rank_up':
        if (this.gameState.player && notif.new_rank !== undefined) {
          this.gameState.player.reputation_rank = notif.new_rank;
          if (notif.new_xp !== undefined) this.gameState.player.reputation_xp = notif.new_xp;
        }
        break;
      case 'travel_arrived':
        if (this.gameState.player && notif.district) {
          this.gameState.player.current_district = notif.district;
          this.gameState.player.travel_to = null;
          this.gameState.player.travel_arrival_at = null;
        }
        break;
      case 'busted':
        if (this.gameState.player) {
          this.gameState.player.prison_until = notif.prison_until;
        }
        break;
    }
  }

  // ── Reconnection ──────────────────────────────────────────────────────

  _tryReconnect() {
    if (this._reconnectAttempts >= this._maxReconnectAttempts) {
      this.emit('reconnect_failed', { attempts: this._reconnectAttempts });
      return;
    }

    this._reconnectAttempts++;
    const delay = Math.min(this._reconnectDelay * Math.pow(1.5, this._reconnectAttempts - 1), 30000);

    this.emit('reconnecting', { attempt: this._reconnectAttempts, delay });

    setTimeout(async () => {
      try {
        await this.connect();
      } catch (err) {
        this.emit('error', err);
        // connect() rejection will trigger close → _tryReconnect again
      }
    }, delay);
  }

  _rejectAllPending(reason) {
    for (const [id, pending] of this.pendingRequests) {
      clearTimeout(pending.timeout);
      pending.reject(new Error(reason));
    }
    this.pendingRequests.clear();
  }
}
