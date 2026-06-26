/**
 * EkyBot Companion API Client
 *
 * Reads EKYBOT_APP_URL and EKYBOT_COMPANION_TOKEN (or EKYBOT_COMPANION_API_KEY)
 * from the local .env.ekybot_companion file to authenticate with the EkyBot
 * cloud API at https://www.ekybot.com.
 *
 * Network calls made by this module (all to EKYBOT_APP_URL):
 * - POST   /api/companion/machines                          — register machine (enrollment)
 * - GET    /api/companion/machines                          — list enrolled machines
 * - POST   /api/companion/machines/:id/heartbeat            — machine health telemetry (see SKILL.md "Telemetry & Privacy")
 * - POST   /api/companion/machines/:id/inventory            — sync agent list to dashboard
 * - GET    /api/companion/machines/:id/inventory             — fetch current agent inventory
 * - GET    /api/companion/machines/:id/desired-state         — pull agent config changes from dashboard
 * - POST   /api/companion/machines/:id/memory               — sync workspace memory files (see "Memory Sync")
 * - GET    /api/companion/machines/:id/relay                 — poll for pending @mention messages
 * - PATCH  /api/companion/machines/:id/relay                 — acknowledge/claim relay notifications
 * - POST   /api/companion/machines/:id/relay/messages        — post agent reply back to dashboard
 * - POST   /api/companion/machines/:id/budget-alert          — report budget threshold breach
 * - PATCH  /api/companion/machines/:id/operations/:opId      — update operation status
 *
 * No API keys, raw conversation content, or files outside the agent workspace
 * are transmitted. See references/security.md for the full data disclosure.
 */
const chalk = require('chalk');

const fetchImpl = global.fetch
  ? (...args) => global.fetch(...args)
  : (...args) => require('node-fetch')(...args);

const desiredStateCache = new Map();

function resolveDesiredStateCacheKey(baseUrl, machineId) {
  return `${String(baseUrl || '').replace(/\/$/, '')}:${machineId}`;
}

class EkybotCompanionApiClient {
  constructor(options = {}) {
    this.baseUrl = (options.baseUrl || process.env.EKYBOT_APP_URL || 'https://www.ekybot.com')
      .replace(/\/$/, '');
    this.userAgent = options.userAgent || 'ekybot-companion/0.1.0';
    this.userBearerToken = options.userBearerToken || process.env.EKYBOT_USER_BEARER_TOKEN || null;
    this.machineApiKey = options.machineApiKey || process.env.EKYBOT_COMPANION_API_KEY || null;
    this.registrationToken =
      options.registrationToken || process.env.EKYBOT_COMPANION_REGISTRATION_TOKEN || null;
    const envTimeout = parseInt(process.env.EKYBOT_COMPANION_API_TIMEOUT_MS, 10);
    this.requestTimeoutMs = (options.requestTimeoutMs || (Number.isFinite(envTimeout) && envTimeout > 0 ? envTimeout : 30000));
  }

  buildHeaders(extraHeaders = {}, authModeOverride = null) {
    const headers = {
      'Content-Type': 'application/json',
      'User-Agent': this.userAgent,
      ...extraHeaders,
    };

    const authMode = authModeOverride || this.getAuthMode();

    if (authMode === 'machine_api_key' && this.machineApiKey) {
      headers['x-companion-api-key'] = this.machineApiKey;
    } else if (authMode === 'registration_token' && this.registrationToken) {
      headers['x-companion-registration-token'] = this.registrationToken;
    } else if (authMode === 'user_bearer_token' && this.userBearerToken) {
      headers.Authorization = `Bearer ${this.userBearerToken}`;
    }

    return headers;
  }

  getAuthMode() {
    if (this.machineApiKey) {
      return 'machine_api_key';
    }
    if (this.registrationToken) {
      return 'registration_token';
    }
    if (this.userBearerToken) {
      return 'user_bearer_token';
    }
    return 'anonymous';
  }

  async request(method, pathname, data = null, extraHeaders = {}, authModeOverride = null) {
    const controller = new AbortController();
    const timeoutMs = this.requestTimeoutMs;
    const timeoutId = setTimeout(() => controller.abort(), timeoutMs);
    let response;
    try {
      response = await fetchImpl(`${this.baseUrl}${pathname}`, {
        method,
        headers: this.buildHeaders(extraHeaders, authModeOverride),
        body: data ? JSON.stringify(data) : undefined,
        signal: controller.signal,
      });
    } catch (err) {
      clearTimeout(timeoutId);
      if (err.name === 'AbortError') {
        throw new Error(`Companion API request timeout on ${method} ${pathname} (${Math.round(timeoutMs / 1000)}s)`);
      }
      throw err;
    }
    clearTimeout(timeoutId);

    const rawText = await response.text();
    const contentType = response.headers.get('content-type') || '';
    const isJson = contentType.toLowerCase().includes('application/json');
    let payload = null;
    if (rawText && isJson) {
      try {
        payload = JSON.parse(rawText);
      } catch (error) {
        throw new Error(
          `Companion API request failed on ${method} ${pathname}: invalid JSON response (${contentType})`
        );
      }
    }

    if (!response.ok) {
      if (!isJson) {
        const preview = rawText.replace(/\s+/g, ' ').slice(0, 160);
        throw new Error(
          `Companion API request failed on ${method} ${pathname}: ${response.status} ${response.statusText} (content-type: ${contentType || 'unknown'}, auth: ${this.getAuthMode()}, body: ${preview})`
        );
      }
      const message = payload?.error || payload?.message || `${response.status} ${response.statusText}`;
      const details = payload?.details ? ` | details: ${JSON.stringify(payload.details)}` : '';
      throw new Error(`Companion API request failed on ${method} ${pathname}: ${message}${details}`);
    }

    if (rawText && !isJson) {
      const preview = rawText.replace(/\s+/g, ' ').slice(0, 160);
      throw new Error(
        `Companion API request failed on ${method} ${pathname}: expected JSON but received ${contentType || 'unknown'} (auth: ${this.getAuthMode()}, body: ${preview})`
      );
    }

    return payload;
  }

  async registerMachine(registration) {
    const authMode = this.registrationToken ? 'registration_token' : this.getAuthMode();
    return this.request('POST', '/api/companion/machines', registration, {}, authMode);
  }

  async listMachines() {
    return this.request('GET', '/api/companion/machines');
  }

  async sendHeartbeat(machineId, heartbeat) {
    return this.request('POST', `/api/companion/machines/${machineId}/heartbeat`, heartbeat);
  }

  async uploadInventory(machineId, inventory) {
    return this.request('POST', `/api/companion/machines/${machineId}/inventory`, inventory);
  }

  async fetchInventory(machineId) {
    return this.request('GET', `/api/companion/machines/${machineId}/inventory`);
  }

  async fetchDesiredState(machineId) {
    const cacheKey = resolveDesiredStateCacheKey(this.baseUrl, machineId);
    const cachedEntry = desiredStateCache.get(cacheKey);
    const extraHeaders = {};

    if (cachedEntry?.etag) {
      extraHeaders['If-None-Match'] = cachedEntry.etag;
    }

    const controller = new AbortController();
    const timeoutMs = this.requestTimeoutMs;
    const timeoutId = setTimeout(() => controller.abort(), timeoutMs);
    let response;

    try {
      response = await fetchImpl(`${this.baseUrl}/api/companion/machines/${machineId}/desired-state`, {
        method: 'GET',
        headers: this.buildHeaders(extraHeaders),
        signal: controller.signal,
      });
    } catch (err) {
      clearTimeout(timeoutId);
      if (err.name === 'AbortError') {
        throw new Error(`Companion API request timeout on GET /api/companion/machines/${machineId}/desired-state (${Math.round(timeoutMs / 1000)}s)`);
      }
      throw err;
    }

    clearTimeout(timeoutId);

    if (response.status === 304 && cachedEntry?.payload) {
      desiredStateCache.set(cacheKey, {
        ...cachedEntry,
        cachedAt: Date.now(),
      });
      return cachedEntry.payload;
    }

    const rawText = await response.text();
    const contentType = response.headers.get('content-type') || '';
    const isJson = contentType.toLowerCase().includes('application/json');
    let payload = null;
    if (rawText && isJson) {
      try {
        payload = JSON.parse(rawText);
      } catch (_error) {
        throw new Error(
          `Companion API request failed on GET /api/companion/machines/${machineId}/desired-state: invalid JSON response (${contentType})`
        );
      }
    }

    if (!response.ok) {
      if (!isJson) {
        const preview = rawText.replace(/\s+/g, ' ').slice(0, 160);
        throw new Error(
          `Companion API request failed on GET /api/companion/machines/${machineId}/desired-state: ${response.status} ${response.statusText} (content-type: ${contentType || 'unknown'}, auth: ${this.getAuthMode()}, body: ${preview})`
        );
      }
      const message = payload?.error || payload?.message || `${response.status} ${response.statusText}`;
      const details = payload?.details ? ` | details: ${JSON.stringify(payload.details)}` : '';
      throw new Error(
        `Companion API request failed on GET /api/companion/machines/${machineId}/desired-state: ${message}${details}`
      );
    }

    if (rawText && !isJson) {
      const preview = rawText.replace(/\s+/g, ' ').slice(0, 160);
      throw new Error(
        `Companion API request failed on GET /api/companion/machines/${machineId}/desired-state: expected JSON but received ${contentType || 'unknown'} (auth: ${this.getAuthMode()}, body: ${preview})`
      );
    }

    desiredStateCache.set(cacheKey, {
      payload,
      cachedAt: Date.now(),
      etag: response.headers.get('etag'),
    });

    return payload;
  }

  async fetchDesiredStateCached(machineId, options = {}) {
    const { maxAgeMs = 0, forceRefresh = false } = options;
    const cacheKey = resolveDesiredStateCacheKey(this.baseUrl, machineId);
    const cachedEntry = desiredStateCache.get(cacheKey);

    if (
      !forceRefresh &&
      maxAgeMs > 0 &&
      cachedEntry &&
      Date.now() - cachedEntry.cachedAt < maxAgeMs
    ) {
      return cachedEntry.payload;
    }

    const payload = await this.fetchDesiredState(machineId);
    desiredStateCache.set(cacheKey, {
      payload,
      cachedAt: Date.now(),
    });
    return payload;
  }

  invalidateDesiredStateCache(machineId) {
    EkybotCompanionApiClient.invalidateDesiredStateCache(this.baseUrl, machineId);
  }

  static invalidateDesiredStateCache(baseUrl, machineId) {
    desiredStateCache.delete(resolveDesiredStateCacheKey(baseUrl, machineId));
  }

  async syncMachineMemory(machineId, payload) {
    return this.request('POST', `/api/companion/machines/${machineId}/memory`, payload);
  }

  async fetchRelayNotifications(machineId, { limit = 20 } = {}) {
    return this.request(
      'GET',
      `/api/companion/machines/${machineId}/relay?limit=${encodeURIComponent(String(limit))}`
    );
  }

  async updateRelayNotifications(machineId, payload) {
    return this.request('PATCH', `/api/companion/machines/${machineId}/relay`, payload);
  }

  async sendBudgetAlert(machineId, payload) {
    return this.request('POST', `/api/companion/machines/${machineId}/budget-alert`, payload);
  }

  async postRelayMessage(machineId, payload) {
    return this.request('POST', `/api/companion/machines/${machineId}/relay/messages`, payload);
  }

  async updateOperation(machineId, operationId, payload) {
    return this.request(
      'PATCH',
      `/api/companion/machines/${machineId}/operations/${operationId}`,
      payload
    );
  }

  async ping() {
    try {
      const machines = await this.listMachines();
      return {
        status: 'ok',
        details: `reachable (${Array.isArray(machines?.machines) ? machines.machines.length : 0} machines visible)`,
      };
    } catch (error) {
      console.error(chalk.red(`Companion API ping failed: ${error.message}`));
      return { status: 'error', details: error.message };
    }
  }
}

module.exports = EkybotCompanionApiClient;
