'use strict';

const crypto = require('crypto');
const http = require('http');
const { writeSettings, readSettings, clearSettings, clearIfStale } = require('./settings');

const MAX_PORT_ATTEMPTS = 100;
const DEFAULT_PORT = 19820;

// GHSA-7xp7-m392-h92c: cap request body at 1 MiB. The proxy's HTTP surface is
// bound to 127.0.0.1 but still reachable by any local process (other users on
// a shared dev host, container neighbors sharing the host netns, malicious
// postinstall scripts). Without a cap, /asset/submit and /mailbox/send write
// the full body verbatim into messages.jsonl, so an attacker can fill the
// disk and make the daemon OOM on every restart (readFileSync over a multi-
// GB JSONL). Tune via EVOMAP_PROXY_MAX_BODY_BYTES if a legitimate workload
// truly needs bigger bodies.
const DEFAULT_MAX_BODY_BYTES = 1 * 1024 * 1024;
function resolveMaxBodyBytes() {
  const raw = Number(process.env.EVOMAP_PROXY_MAX_BODY_BYTES);
  if (Number.isFinite(raw) && raw > 0) return Math.floor(raw);
  return DEFAULT_MAX_BODY_BYTES;
}

function parseBody(req, opts) {
  const maxBytes = (opts && Number.isFinite(opts.maxBytes) && opts.maxBytes > 0)
    ? opts.maxBytes
    : resolveMaxBodyBytes();
  return new Promise((resolve, reject) => {
    const declared = Number(req.headers['content-length']);
    if (Number.isFinite(declared) && declared > maxBytes) {
      const err = new Error('Request body too large');
      err.statusCode = 413;
      return reject(err);
    }
    const chunks = [];
    let received = 0;
    let settled = false;
    const fail = (err) => {
      if (settled) return;
      settled = true;
      try { req.destroy(); } catch { /* ignore */ }
      reject(err);
    };
    req.on('data', (c) => {
      if (settled) return;
      received += c.length;
      if (received > maxBytes) {
        const err = new Error('Request body too large');
        err.statusCode = 413;
        return fail(err);
      }
      chunks.push(c);
    });
    req.on('end', () => {
      if (settled) return;
      settled = true;
      const raw = Buffer.concat(chunks).toString();
      if (!raw) return resolve({});
      try { resolve(JSON.parse(raw)); }
      catch (e) { reject(new Error('Invalid JSON body')); }
    });
    req.on('error', fail);
  });
}

function sendJson(res, status, body, extraHeaders = {}) {
  const payload = JSON.stringify(body);
  const headers = {
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(payload),
  };
  for (const [name, value] of Object.entries(extraHeaders || {})) {
    if (value === undefined || value === null) continue;
    const lower = String(name).toLowerCase();
    if (lower === 'content-length' || lower === 'transfer-encoding' || lower === 'connection') continue;
    const headerValue = Array.isArray(value) ? value.join(', ') : String(value);
    if (/[\r\n]/.test(headerValue)) continue;
    headers[name] = headerValue;
  }
  res.writeHead(status, headers);
  res.end(payload);
}

function tryListen(server, port) {
  return new Promise((resolve, reject) => {
    server.once('error', (err) => {
      if (err.code === 'EADDRINUSE') return resolve(false);
      reject(err);
    });
    server.listen(port, '127.0.0.1', () => resolve(true));
  });
}

class ProxyHttpServer {
  constructor(routes, { port, logger } = {}) {
    this.routes = routes;
    this.basePort = port || Number(process.env.EVOMAP_PROXY_PORT) || DEFAULT_PORT;
    this.actualPort = null;
    this.logger = logger || console;
    this.server = null;
    this.token = null;
  }

  async start() {
    // Capture the prior token before clearIfStale wipes it. Daemon restarts
    // routinely fall into the stale branch (the previous PID is gone), and
    // rotating `proxy.token` on every restart invalidates ANTHROPIC_AUTH_TOKEN
    // already exported into long-lived shells (the .bashrc auto-source only
    // runs once per terminal).
    const priorProxy = readSettings().proxy || {};
    const previous = typeof priorProxy.token === 'string' ? priorProxy.token : null;
    // settings.json is operator-edited; previous_tokens may contain non-strings
    // (numbers, booleans, objects) that would later crash Buffer.from(cand, 'utf8')
    // in _handleRequest as ERR_INVALID_ARG_TYPE — an unhandled rejection that
    // takes the daemon down under default --unhandled-rejections=throw.
    const priorPreviousTokens = Array.isArray(priorProxy.previous_tokens)
      ? priorProxy.previous_tokens.filter((t) => typeof t === 'string' && t.length > 0)
      : [];
    clearIfStale();
    this.token = previous || crypto.randomBytes(32).toString('hex');
    this._priorPreviousTokens = priorPreviousTokens;
    this.server = http.createServer((req, res) => this._handleRequest(req, res));

    let port = this.basePort;
    for (let i = 0; i < MAX_PORT_ATTEMPTS; i++) {
      const ok = await tryListen(this.server, port);
      if (ok) {
        this.actualPort = port;
        const url = `http://127.0.0.1:${port}`;
        const proxyBlock = {
          url,
          pid: process.pid,
          started_at: new Date().toISOString(),
          token: this.token,
        };
        if (this._priorPreviousTokens && this._priorPreviousTokens.length) {
          proxyBlock.previous_tokens = this._priorPreviousTokens;
        }
        writeSettings({ proxy: proxyBlock });
        this.logger.log(`[proxy] HTTP server listening on ${url}`);
        return { port, url, token: this.token };
      }
      port++;
    }
    throw new Error(`Could not find free port after ${MAX_PORT_ATTEMPTS} attempts starting from ${this.basePort}`);
  }

  async stop() {
    if (this.server) {
      await new Promise((resolve) => this.server.close(resolve));
      this.server = null;
    }
    clearSettings();
  }

  async _handleRequest(req, res) {
    const authHeader = req.headers['authorization'] || '';
    const provided = authHeader.startsWith('Bearer ') ? authHeader.slice(7) : '';
    const provBuf = Buffer.from(provided, 'utf8');
    // Primary token plus any grace tokens from settings.json::proxy.previous_tokens.
    // The grace list is the recovery path for the rare case where settings.json was
    // wiped externally (logout, manual rm) while long-lived CC sessions still hold
    // the pre-wipe token in their fork-time env. Operator writes the lost token into
    // previous_tokens; once those sessions close, the operator can clear the array.
    // Reading directly from settings.json (instead of an env shim) keeps the
    // single source of truth on disk — no python bridge in the daemon hook.
    // Defense in depth: even though start() filters non-strings before persisting,
    // settings.json can be hand-edited between requests, so re-validate every read.
    // A non-string slipping into Buffer.from below would throw ERR_INVALID_ARG_TYPE
    // and unhandled-reject through the auth path.
    const previous = readSettings().proxy?.previous_tokens;
    const extras = Array.isArray(previous)
      ? previous.filter((t) => typeof t === 'string' && t.length > 0)
      : [];
    const candidates = [this.token, ...extras].filter((t) => typeof t === 'string' && t.length > 0);
    let valid = false;
    for (const cand of candidates) {
      const expBuf = Buffer.from(cand, 'utf8');
      if (provBuf.length === expBuf.length && crypto.timingSafeEqual(provBuf, expBuf)) {
        valid = true;
        break;
      }
    }
    if (!valid) {
      return sendJson(res, 401, { error: 'Unauthorized' });
    }

    const url = new URL(req.url, `http://127.0.0.1:${this.actualPort}`);
    const routeKey = `${req.method} ${url.pathname}`;

    const paramMatch = this._matchRoute(req.method, url.pathname);

    if (!paramMatch) {
      return sendJson(res, 404, { error: 'Not found', path: url.pathname });
    }

    const { handler, params } = paramMatch;

    try {
      const body = (req.method === 'POST' || req.method === 'PUT') ? await parseBody(req) : {};
      const query = Object.fromEntries(url.searchParams);
      const headers = req.headers;
      const result = await handler({ body, query, params, headers });
      if (result && result.stream) {
        await this._streamResponse(res, result);
      } else {
        sendJson(res, result.status || 200, result.body || result, result.headers);
      }
    } catch (err) {
      this.logger.error(`[proxy] ${routeKey} error:`, err.message);
      if (res.headersSent) {
        try { res.end(); } catch { /* ignore */ }
      } else {
        sendJson(res, err.statusCode || 500, {
          error: err.message || 'Internal error',
        });
      }
    }
  }

  // SSE / pass-through streaming path used by /v1/messages (slice 5).
  // `result.stream` may be any async iterable yielding Buffer or string
  // chunks (Web ReadableStream from fetch, or a Node Readable). Headers
  // default to text/event-stream so Anthropic-style SSE bytes piped
  // through reach the client unmodified. The caller owns producing
  // correctly-framed SSE; this method only relays bytes.
  async _streamResponse(res, result) {
    const headers = Object.assign({
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    }, result.headers || {});
    res.writeHead(result.status || 200, headers);

    // Browsers, network blips, and Ctrl-C all close the SSE socket mid-stream.
    // If we await `drain` without watching for `close`, the drain event never
    // fires on a destroyed socket and this coroutine hangs forever — which
    // also pins the upstream fetch body open (real Anthropic socket leak, not
    // just coroutine leak). For Web ReadableStream upstreams we read via an
    // explicit reader so cancellation can go through the same lock; for sync
    // generators / Node Readables we fall back to for-await.
    const stream = result.stream;
    const reader = stream && typeof stream.getReader === 'function' ? stream.getReader() : null;

    let clientGone = false;
    const onClose = () => {
      clientGone = true;
      if (reader) {
        reader.cancel().catch(() => { /* upstream already settled */ });
      } else if (stream && typeof stream.destroy === 'function') {
        try { stream.destroy(); } catch { /* ignore */ }
      }
    };
    res.once('close', onClose);

    const awaitBackpressure = () => new Promise((resolve) => {
      let settled = false;
      const onDrain = () => {
        if (settled) return;
        settled = true;
        res.off('close', onCloseInner);
        resolve();
      };
      const onCloseInner = () => {
        if (settled) return;
        settled = true;
        res.off('drain', onDrain);
        resolve();
      };
      res.once('drain', onDrain);
      res.once('close', onCloseInner);
    });

    try {
      if (reader) {
        for (;;) {
          const { value, done } = await reader.read();
          if (done || clientGone) break;
          if (!res.write(value)) {
            await awaitBackpressure();
            if (clientGone) break;
          }
        }
      } else {
        for await (const chunk of stream) {
          if (clientGone) break;
          if (!res.write(chunk)) {
            await awaitBackpressure();
            if (clientGone) break;
          }
        }
      }
    } finally {
      res.off('close', onClose);
      try { res.end(); } catch { /* socket may already be destroyed */ }
    }
  }

  _matchRoute(method, pathname) {
    for (const [pattern, handler] of Object.entries(this.routes)) {
      const [routeMethod, routePath] = pattern.split(' ');
      if (routeMethod !== method) continue;

      const params = matchPath(routePath, pathname);
      if (params !== null) return { handler, params };
    }
    return null;
  }
}

function matchPath(pattern, pathname) {
  const patternParts = pattern.split('/');
  const pathParts = pathname.split('/');

  if (patternParts.length !== pathParts.length) return null;

  const params = {};
  for (let i = 0; i < patternParts.length; i++) {
    if (patternParts[i].startsWith(':')) {
      params[patternParts[i].slice(1)] = pathParts[i];
    } else if (patternParts[i] !== pathParts[i]) {
      return null;
    }
  }
  return params;
}

module.exports = { ProxyHttpServer, parseBody, sendJson, DEFAULT_PORT, DEFAULT_MAX_BODY_BYTES, resolveMaxBodyBytes };
