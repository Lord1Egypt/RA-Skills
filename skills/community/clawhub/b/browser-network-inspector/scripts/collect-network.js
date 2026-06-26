(() => {
  const existing = !!window.__bniInstalled;

  const defaults = {
    maxText: 2000,
    includeHosts: [],
    excludeHosts: [],
    captureWebSocket: true,
  };

  const priorConfig = window.__bniConfig || {};
  const config = { ...defaults, ...priorConfig };
  const logs = window.__bniLogs || [];
  const SENSITIVE_KEYS = new Set([
    'authorization', 'cookie', 'set-cookie', 'password', 'token',
    'accesstoken', 'refreshtoken', 'session', 'csrf', 'x-csrf-token'
  ]);

  function truncate(value, max = config.maxText) {
    if (value == null) return value;
    const str = typeof value === 'string' ? value : JSON.stringify(value);
    return str.length > max ? str.slice(0, max) + '…<truncated>' : str;
  }

  function redactValue(key, value) {
    if (!key) return truncate(value);
    const normalized = String(key).toLowerCase();
    if (SENSITIVE_KEYS.has(normalized) || normalized.includes('token') || normalized.includes('cookie') || normalized.includes('pass') || normalized.includes('secret')) {
      return '<REDACTED>';
    }
    return truncate(value);
  }

  function redactObject(input) {
    if (!input || typeof input !== 'object') return input;
    const out = Array.isArray(input) ? [] : {};
    for (const [key, value] of Object.entries(input)) {
      if (value && typeof value === 'object' && !Array.isArray(value)) {
        out[key] = redactObject(value);
      } else if (Array.isArray(value)) {
        out[key] = value.map(v => (v && typeof v === 'object' ? redactObject(v) : redactValue(key, v)));
      } else {
        out[key] = redactValue(key, value);
      }
    }
    return out;
  }

  function tryParseJson(text) {
    if (!text || typeof text !== 'string') return null;
    try {
      return JSON.parse(text);
    } catch {
      return null;
    }
  }

  function normalizeHeaders(headersLike) {
    const out = {};
    if (!headersLike) return out;

    if (headersLike instanceof Headers) {
      for (const [key, value] of headersLike.entries()) out[key] = redactValue(key, value);
      return out;
    }

    if (Array.isArray(headersLike)) {
      for (const pair of headersLike) {
        if (Array.isArray(pair) && pair.length >= 2) out[pair[0]] = redactValue(pair[0], pair[1]);
      }
      return out;
    }

    if (typeof headersLike === 'object') {
      for (const [key, value] of Object.entries(headersLike)) out[key] = redactValue(key, value);
    }

    return out;
  }

  function normalizeBody(body) {
    if (body == null) return null;
    if (typeof body === 'string') {
      const parsed = tryParseJson(body);
      return parsed ? redactObject(parsed) : truncate(body);
    }
    if (body instanceof URLSearchParams) {
      const obj = {};
      for (const [key, value] of body.entries()) obj[key] = redactValue(key, value);
      return obj;
    }
    if (body instanceof FormData) {
      const obj = {};
      for (const [key, value] of body.entries()) {
        obj[key] = value instanceof File ? `<File:${value.name}>` : redactValue(key, value);
      }
      return obj;
    }
    if (typeof body === 'object') return redactObject(body);
    return truncate(String(body));
  }

  function hostOf(url) {
    try {
      return new URL(url, location.href).host;
    } catch {
      return '';
    }
  }

  function matchesHostRule(host, rules) {
    if (!rules || !rules.length) return false;
    return rules.some(rule => host === rule || host.endsWith(`.${rule}`));
  }

  function shouldCapture(url) {
    const host = hostOf(url);
    if (!host) return true;
    if (config.includeHosts?.length && !matchesHostRule(host, config.includeHosts)) return false;
    if (config.excludeHosts?.length && matchesHostRule(host, config.excludeHosts)) return false;
    return true;
  }

  function pushLog(entry) {
    if (entry?.url && !shouldCapture(entry.url)) return;
    logs.push({ ts: new Date().toISOString(), ...entry });
  }

  if (!existing) {
    const originalFetch = window.fetch.bind(window);
    window.fetch = async function bniFetch(input, init = {}) {
      const startedAt = Date.now();
      const url = typeof input === 'string' ? input : input?.url;
      const method = init.method || (typeof input !== 'string' && input?.method) || 'GET';
      const requestHeaders = normalizeHeaders(init.headers || (typeof input !== 'string' ? input?.headers : undefined));
      const requestBody = normalizeBody(init.body);

      try {
        const response = await originalFetch(input, init);
        const cloned = response.clone();
        let responseText = null;
        try { responseText = await cloned.text(); } catch {}
        const parsed = tryParseJson(responseText);

        pushLog({
          source: 'fetch', url, method, durationMs: Date.now() - startedAt,
          requestHeaders, requestBody, status: response.status, ok: response.ok,
          responseHeaders: normalizeHeaders(response.headers),
          responseBody: parsed ? redactObject(parsed) : truncate(responseText),
        });

        return response;
      } catch (error) {
        pushLog({
          source: 'fetch', url, method, durationMs: Date.now() - startedAt,
          requestHeaders, requestBody, error: String(error),
        });
        throw error;
      }
    };

    const originalOpen = XMLHttpRequest.prototype.open;
    const originalSend = XMLHttpRequest.prototype.send;
    const originalSetRequestHeader = XMLHttpRequest.prototype.setRequestHeader;

    XMLHttpRequest.prototype.open = function bniOpen(method, url, ...rest) {
      this.__bni = { method, url, headers: {}, startedAt: 0, body: null };
      return originalOpen.call(this, method, url, ...rest);
    };

    XMLHttpRequest.prototype.setRequestHeader = function bniSetRequestHeader(key, value) {
      if (this.__bni) this.__bni.headers[key] = redactValue(key, value);
      return originalSetRequestHeader.call(this, key, value);
    };

    XMLHttpRequest.prototype.send = function bniSend(body) {
      if (this.__bni) {
        this.__bni.startedAt = Date.now();
        this.__bni.body = normalizeBody(body);
      }

      this.addEventListener('loadend', () => {
        const meta = this.__bni || {};
        const allHeaders = this.getAllResponseHeaders?.() || '';
        const responseHeaders = {};
        allHeaders.trim().split(/\r?\n/).forEach(line => {
          if (!line) return;
          const idx = line.indexOf(':');
          if (idx === -1) return;
          const key = line.slice(0, idx).trim();
          const value = line.slice(idx + 1).trim();
          responseHeaders[key] = redactValue(key, value);
        });

        let responseBody = null;
        try {
          if (typeof this.responseText === 'string') {
            const parsed = tryParseJson(this.responseText);
            responseBody = parsed ? redactObject(parsed) : truncate(this.responseText);
          }
        } catch {}

        pushLog({
          source: 'xhr', url: meta.url, method: meta.method || 'GET',
          durationMs: meta.startedAt ? Date.now() - meta.startedAt : null,
          requestHeaders: meta.headers || {}, requestBody: meta.body,
          status: this.status, ok: this.status >= 200 && this.status < 300,
          responseHeaders, responseBody,
        });
      }, { once: true });

      return originalSend.call(this, body);
    };

    if (config.captureWebSocket && 'WebSocket' in window) {
      const NativeWebSocket = window.WebSocket;
      window.WebSocket = function BNIWebSocket(url, protocols) {
        const startedAt = Date.now();
        const ws = protocols ? new NativeWebSocket(url, protocols) : new NativeWebSocket(url);

        pushLog({ source: 'websocket', phase: 'open-call', url, method: 'WS', durationMs: 0 });

        ws.addEventListener('open', () => {
          pushLog({ source: 'websocket', phase: 'open', url, method: 'WS', durationMs: Date.now() - startedAt, ok: true });
        });

        ws.addEventListener('message', event => {
          pushLog({ source: 'websocket', phase: 'message-in', url, method: 'WS', message: truncate(event.data) });
        });

        ws.addEventListener('close', event => {
          pushLog({ source: 'websocket', phase: 'close', url, method: 'WS', code: event.code, reason: truncate(event.reason), ok: event.wasClean });
        });

        ws.addEventListener('error', () => {
          pushLog({ source: 'websocket', phase: 'error', url, method: 'WS', error: 'WebSocket error' });
        });

        const nativeSend = ws.send.bind(ws);
        ws.send = function bniSend(data) {
          pushLog({ source: 'websocket', phase: 'message-out', url, method: 'WS', message: truncate(data) });
          return nativeSend(data);
        };

        return ws;
      };
      window.WebSocket.prototype = NativeWebSocket.prototype;
    }
  }

  window.__bniLogs = logs;
  window.__bniConfig = config;
  window.__bniSetConfig = (patch = {}) => Object.assign(window.__bniConfig, patch || {});
  window.__bniExport = () => JSON.parse(JSON.stringify(logs));
  window.__bniClear = () => { logs.length = 0; return true; };
  window.__bniInstalled = true;

  return existing ? 'browser-network-inspector reconfigured' : 'browser-network-inspector installed';
})();
