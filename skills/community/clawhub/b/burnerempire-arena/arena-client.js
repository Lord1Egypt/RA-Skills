// Arena Agent - REST API Client
// Wraps all Burner Empire AI Arena HTTP endpoints

import { ARENA_API_URL, ARENA_API_KEY } from './config.js';

export class ArenaClient {
  constructor(apiUrl = ARENA_API_URL, apiKey = ARENA_API_KEY) {
    this.apiUrl = apiUrl.replace(/\/$/, '');
    this.apiKey = apiKey;
  }

  // ── Internal ─────────────────────────────────────────────────────────

  async _request(method, path, body = null) {
    const url = `${this.apiUrl}${path}`;
    const headers = { 'Content-Type': 'application/json' };
    if (this.apiKey) {
      headers['Authorization'] = `Bearer ${this.apiKey}`;
    }

    const opts = { method, headers };
    if (body) opts.body = JSON.stringify(body);

    const res = await fetch(url, opts);

    // Read body once as text to avoid "Body has already been read" errors
    const text = await res.text();

    if (!res.ok) {
      let errorBody;
      try { errorBody = JSON.parse(text); } catch { errorBody = text; }
      const msg = errorBody?.error || errorBody?.message || JSON.stringify(errorBody);
      throw new ArenaError(msg, res.status, errorBody);
    }

    try {
      return JSON.parse(text);
    } catch {
      throw new ArenaError(`Invalid JSON response: ${text.slice(0, 200)}`, res.status, text);
    }
  }

  async _get(path) { return this._request('GET', path); }
  async _post(path, body) { return this._request('POST', path, body); }

  // ── Registration (no auth) ──────────────────────────────────────────

  async register(ownerName) {
    // Temporarily clear key for registration (no auth needed)
    const savedKey = this.apiKey;
    this.apiKey = '';
    try {
      const result = await this._post('/api/arena/register', { owner_name: ownerName });
      // Auto-set the returned key
      if (result.api_key) {
        this.apiKey = result.api_key;
      }
      return result;
    } finally {
      if (!this.apiKey) this.apiKey = savedKey;
    }
  }

  // ── Authenticated Endpoints ─────────────────────────────────────────

  async getMe() {
    return this._get('/api/arena/me');
  }

  async createPlayer(username, llmModel, strategy = '') {
    return this._post('/api/arena/players', {
      username,
      llm_model: llmModel,
      strategy,
    });
  }

  async getState(playerId) {
    return this._get(`/api/arena/state/${playerId}`);
  }

  async executeAction(playerId, action, data = {}, reasoning = '', llmModel = '') {
    const body = { action, data, reasoning };
    if (llmModel) body.llm_model = llmModel;
    return this._post(`/api/arena/action/${playerId}`, body);
  }

  async getNotifications(playerId) {
    return this._get(`/api/arena/notifications/${playerId}`);
  }

  // ── Public Spectator Endpoints ──────────────────────────────────────

  async getLeaderboard(limit = 25) {
    return this._get(`/api/arena/leaderboard?limit=${limit}`);
  }

  async getFeed(limit = 50, sinceId = null) {
    let url = `/api/arena/feed?limit=${limit}`;
    if (sinceId) url += `&since=${sinceId}`;
    return this._get(url);
  }

  async getStats() {
    return this._get('/api/arena/stats');
  }

  async getAgentProfile(username) {
    return this._get(`/api/arena/agent/${username}`);
  }

  async getLlmRankings() {
    return this._get('/api/arena/llm-rankings');
  }
}

// ── SSE Stream Client ─────────────────────────────────────────────────
// Maintains a persistent Server-Sent Events connection for real-time
// state/tick/notification delivery. No npm deps — uses Node.js fetch.

export class ArenaStreamClient {
  constructor(apiUrl = ARENA_API_URL, apiKey = ARENA_API_KEY) {
    this.apiUrl = apiUrl.replace(/\/$/, '');
    this.apiKey = apiKey;
    this.gameState = null;
    this.connected = false;
    this._listeners = {};
    this._abortController = null;
    this._reconnectDelay = 1000;
    this._maxReconnectDelay = 30000;
    this._shouldReconnect = true;
  }

  on(event, fn) {
    if (!this._listeners[event]) this._listeners[event] = [];
    this._listeners[event].push(fn);
  }

  _emit(event, data) {
    for (const fn of (this._listeners[event] || [])) {
      try { fn(data); } catch {}
    }
  }

  async connect(playerId) {
    this.playerId = playerId;
    this._shouldReconnect = true;
    this._reconnectDelay = 1000;
    await this._connect();
  }

  disconnect() {
    this._shouldReconnect = false;
    if (this._abortController) {
      this._abortController.abort();
      this._abortController = null;
    }
    this.connected = false;
  }

  async _connect() {
    if (this._abortController) {
      this._abortController.abort();
    }
    this._abortController = new AbortController();

    const url = `${this.apiUrl}/api/arena/stream/${this.playerId}`;
    try {
      const res = await fetch(url, {
        headers: { 'Authorization': `Bearer ${this.apiKey}` },
        signal: this._abortController.signal,
      });

      if (!res.ok) {
        const text = await res.text().catch(() => '');
        throw new ArenaError(`SSE connect failed: ${res.status}`, res.status, text);
      }

      this.connected = true;
      this._reconnectDelay = 1000;
      this._emit('connected', null);

      await this._readStream(res.body);
    } catch (err) {
      if (err.name === 'AbortError') return;
      this.connected = false;
      this._emit('error', err);

      if (this._shouldReconnect) {
        const delay = this._reconnectDelay;
        this._reconnectDelay = Math.min(this._reconnectDelay * 2, this._maxReconnectDelay);
        this._emit('reconnecting', { delay });
        await new Promise(r => setTimeout(r, delay));
        if (this._shouldReconnect) await this._connect();
      }
    }
  }

  async _readStream(body) {
    const decoder = new TextDecoder();
    let buffer = '';
    let currentEvent = 'message';
    let currentData = '';

    for await (const chunk of body) {
      if (!this._shouldReconnect) break;

      buffer += decoder.decode(chunk, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop(); // keep incomplete line

      for (const line of lines) {
        if (line.startsWith('event:')) {
          currentEvent = line.slice(6).trim();
        } else if (line.startsWith('data:')) {
          currentData += (currentData ? '\n' : '') + line.slice(5).trim();
        } else if (line === '') {
          // Empty line = end of event
          if (currentData) {
            this._handleEvent(currentEvent, currentData);
          }
          currentEvent = 'message';
          currentData = '';
        }
        // Lines starting with ':' are comments (keepalive), ignore
      }
    }

    // Stream ended
    this.connected = false;
    this._emit('disconnected', null);

    if (this._shouldReconnect) {
      const delay = this._reconnectDelay;
      this._reconnectDelay = Math.min(this._reconnectDelay * 2, this._maxReconnectDelay);
      this._emit('reconnecting', { delay });
      await new Promise(r => setTimeout(r, delay));
      if (this._shouldReconnect) await this._connect();
    }
  }

  _handleEvent(event, data) {
    let parsed;
    try { parsed = JSON.parse(data); } catch { return; }

    switch (event) {
      case 'state':
        this.gameState = parsed;
        this._emit('state', parsed);
        break;
      case 'tick':
        this._mergeTick(parsed);
        this._emit('tick', parsed);
        break;
      case 'notification':
        this._mergeNotification(parsed);
        this._emit('notification', parsed);
        break;
      default:
        this._emit('message', parsed);
    }
  }

  _mergeTick(tick) {
    if (!this.gameState) return;
    // Merge player delta
    if (tick.player_delta && this.gameState.player) {
      Object.assign(this.gameState.player, tick.player_delta);
    }
    // Replace arrays if present
    if (tick.cook_queue) this.gameState.cook_queue = tick.cook_queue;
    if (tick.dealers) this.gameState.dealers = tick.dealers;
    if (tick.inventory) this.gameState.inventory = tick.inventory;
    if (tick.active_events) this.gameState.active_events = tick.active_events;
    if (tick.turfs) this.gameState.turfs = tick.turfs;
  }

  _mergeNotification(notif) {
    if (!this.gameState) return;
    // Handle specific notification types that affect state
    const kind = notif.kind || notif.event;
    if (kind === 'prison_released' && this.gameState.player) {
      this.gameState.player.prison_until = null;
      this.gameState.player.in_prison = false;
    } else if (kind === 'laying_low_ended' && this.gameState.player) {
      this.gameState.player.laying_low_until = null;
    } else if (kind === 'shaken_ended' && this.gameState.player) {
      this.gameState.player.shaken_until = null;
      this.gameState.player.is_shaken = false;
    } else if (kind === 'travel_arrived' && this.gameState.player) {
      this.gameState.player.travel_to = null;
      this.gameState.player.travel_arrival_at = null;
      if (notif.district) this.gameState.player.current_district = notif.district;
    }
    // Update contracts_completed_today from contract notifications
    if (notif.contracts_completed_today !== undefined) {
      this.gameState.contracts_completed_today = notif.contracts_completed_today;
    }
  }
}

export class ArenaError extends Error {
  constructor(message, status, body) {
    super(message);
    this.name = 'ArenaError';
    this.status = status;
    this.body = body;
  }
}
