'use strict';

const { describe, it, before, after, beforeEach } = require('node:test');
const assert = require('node:assert/strict');
const http = require('http');
const fs = require('fs');
const os = require('os');
const path = require('path');

const { ProxyHttpServer } = require('../src/proxy/server/http');
const { buildMessagesHandler } = require('../src/proxy/router/messages_route');

function rawPost(url, token, body) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const payload = JSON.stringify(body || {});
    const req = http.request({
      hostname: u.hostname,
      port: u.port,
      path: u.pathname,
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload),
        'x-api-key': 'sk-test',
        'anthropic-version': '2023-06-01',
      },
    }, (res) => {
      const chunks = [];
      res.on('data', (c) => chunks.push(c));
      res.on('end', () => resolve({
        status: res.statusCode,
        headers: res.headers,
        body: Buffer.concat(chunks).toString(),
      }));
    });
    req.on('error', reject);
    req.write(payload);
    req.end();
  });
}

function startStubAnthropic(handler) {
  return new Promise((resolve) => {
    const server = http.createServer(handler);
    server.listen(0, '127.0.0.1', () => {
      const { port } = server.address();
      resolve({ server, baseUrl: `http://127.0.0.1:${port}` });
    });
  });
}

describe('POST /v1/messages — router rewrite + egress', () => {
  let proxyServer, anthropicStub, baseUrl, token, captured;
  let savedSettingsDir;
  let savedCheap, savedMid, savedExpensive;
  let settingsDir;

  before(async () => {
    settingsDir = fs.mkdtempSync(path.join(os.tmpdir(), 'v1msg-settings-'));
    savedSettingsDir = process.env.EVOLVER_SETTINGS_DIR;
    process.env.EVOLVER_SETTINGS_DIR = settingsDir;
    savedCheap = process.env.EVOMAP_MODEL_CHEAP;
    savedMid = process.env.EVOMAP_MODEL_MID;
    savedExpensive = process.env.EVOMAP_MODEL_EXPENSIVE;
    process.env.EVOMAP_MODEL_CHEAP = 'global.anthropic.claude-haiku-4-5-20251001-v1:0';
    process.env.EVOMAP_MODEL_MID = 'global.anthropic.claude-sonnet-4-6';
    process.env.EVOMAP_MODEL_EXPENSIVE = 'global.anthropic.claude-opus-4-7';
    captured = [];
    anthropicStub = await startStubAnthropic((req, res) => {
      const chunks = [];
      req.on('data', (c) => chunks.push(c));
      req.on('end', () => {
        const raw = Buffer.concat(chunks).toString();
        let parsed = null;
        try { parsed = JSON.parse(raw); } catch { /* ignore */ }
        captured.push({ headers: req.headers, body: parsed });
        if (req.headers['x-test-mode'] === '503') {
          res.writeHead(503, { 'content-type': 'application/json' });
          res.end(JSON.stringify({ error: 'overloaded' }));
          return;
        }
        if (req.headers['x-test-mode'] === 'text-plain-404') {
          // Mirrors prism returning "404 page not found" for an unconfigured
          // path — non-JSON body that would crash a naive JSON parser.
          res.writeHead(404, { 'content-type': 'text/plain' });
          res.end('404 page not found\n');
          return;
        }
        if (req.headers['x-test-mode'] === '503-then-throw') {
          if (captured.length === 1) {
            res.writeHead(503, { 'content-type': 'application/json' });
            res.end(JSON.stringify({ error: 'no channel' }));
            return;
          }
          // Drop the connection mid-response so the retry's fetch rejects.
          // Mirrors a real upstream socket drop during the second leg.
          req.socket.destroy();
          return;
        }
        if (req.headers['x-test-mode'] === '503-then-200') {
          // captured.push happened above, so length === request index + 1.
          if (captured.length === 1) {
            res.writeHead(503, { 'content-type': 'application/json' });
            res.end(JSON.stringify({ error: 'no channel' }));
            return;
          }
          if (parsed && parsed.stream === true) {
            res.writeHead(200, {
              'content-type': 'text/event-stream',
              'cache-control': 'no-cache',
            });
            res.write('data: {"type":"message_start"}\n\n');
            res.write('data: {"type":"message_stop"}\n\n');
            res.end();
            return;
          }
          res.writeHead(200, { 'content-type': 'application/json' });
          res.end(JSON.stringify({
            id: 'msg_retry',
            model: (parsed && parsed.model) || 'unknown',
            content: [{ type: 'text', text: 'retried ok' }],
          }));
          return;
        }
        if (parsed && parsed.stream === true) {
          res.writeHead(200, {
            'content-type': 'text/event-stream',
            'cache-control': 'no-cache',
          });
          res.write('data: {"type":"message_start"}\n\n');
          res.write('data: {"type":"message_stop"}\n\n');
          res.end();
          return;
        }
        res.writeHead(200, { 'content-type': 'application/json' });
        res.end(JSON.stringify({
          id: 'msg_1',
          model: (parsed && parsed.model) || 'unknown',
          content: [{ type: 'text', text: 'ok' }],
        }));
      });
    });

    const anthropicProxy = async (reqPath, body, opts) => {
      const inbound = opts.inboundHeaders || {};
      const fwd = { 'content-type': 'application/json' };
      for (const [k, v] of Object.entries(inbound)) {
        const lk = k.toLowerCase();
        if (lk === 'x-api-key' || lk === 'anthropic-version' || lk.startsWith('anthropic-') || lk === 'x-test-mode') {
          fwd[lk] = v;
        }
      }
      const upstream = await fetch(`${anthropicStub.baseUrl}${reqPath}`, {
        method: 'POST',
        headers: fwd,
        body: JSON.stringify(body || {}),
      });
      const ct = (upstream.headers.get('content-type') || '').toLowerCase();
      const isStream = ct.includes('text/event-stream');
      return {
        status: upstream.status,
        headers: Object.fromEntries(upstream.headers.entries()),
        stream: isStream ? upstream.body : null,
        json: isStream ? null : () => upstream.json(),
        text: () => upstream.text(),
      };
    };

    const messagesHandler = buildMessagesHandler({
      anthropicProxy,
      logger: { log: () => {}, warn: () => {}, error: () => {} },
      routerEnabled: true,
    });

    const routes = { 'POST /v1/messages': messagesHandler };
    proxyServer = new ProxyHttpServer(routes, {
      port: 39840,
      logger: { log: () => {}, warn: () => {}, error: () => {} },
    });
    const info = await proxyServer.start();
    baseUrl = info.url;
    token = info.token;
  });

  after(async () => {
    await proxyServer.stop();
    await new Promise((resolve) => anthropicStub.server.close(resolve));
    try { fs.rmSync(settingsDir, { recursive: true }); } catch {}
    if (savedSettingsDir === undefined) delete process.env.EVOLVER_SETTINGS_DIR;
    else process.env.EVOLVER_SETTINGS_DIR = savedSettingsDir;
    if (savedCheap === undefined) delete process.env.EVOMAP_MODEL_CHEAP;
    else process.env.EVOMAP_MODEL_CHEAP = savedCheap;
    if (savedMid === undefined) delete process.env.EVOMAP_MODEL_MID;
    else process.env.EVOMAP_MODEL_MID = savedMid;
    if (savedExpensive === undefined) delete process.env.EVOMAP_MODEL_EXPENSIVE;
    else process.env.EVOMAP_MODEL_EXPENSIVE = savedExpensive;
  });

  beforeEach(() => { captured.length = 0; });

  it('rewrites model to cheap on post-tool-result synthesis turns', async () => {
    const res = await rawPost(`${baseUrl}/v1/messages`, token, {
      model: 'global.anthropic.claude-opus-4-7',
      messages: [
        { role: 'user', content: 'do the thing' },
        {
          role: 'assistant',
          content: [{ type: 'tool_use', id: 't1', name: 'do_thing', input: {} }],
        },
        {
          role: 'user',
          content: [{ type: 'tool_result', tool_use_id: 't1', content: 'done' }],
        },
      ],
    });
    assert.equal(res.status, 200);
    const sentModel = captured[0]?.body?.model;
    assert.equal(sentModel, 'global.anthropic.claude-haiku-4-5-20251001-v1:0', 'expected cheap tier model rewrite');
    const json = JSON.parse(res.body);
    assert.equal(json.model, 'global.anthropic.claude-haiku-4-5-20251001-v1:0');
  });

  it('rewrites model to cheap on trivial lookups', async () => {
    const res = await rawPost(`${baseUrl}/v1/messages`, token, {
      model: 'global.anthropic.claude-opus-4-7',
      messages: [{ role: 'user', content: 'what is npm?' }],
    });
    assert.equal(res.status, 200);
    assert.equal(captured[0]?.body?.model, 'global.anthropic.claude-haiku-4-5-20251001-v1:0');
  });

  it('rewrites model to expensive on planning keywords', async () => {
    const res = await rawPost(`${baseUrl}/v1/messages`, token, {
      model: 'global.anthropic.claude-sonnet-4-7',
      messages: [{ role: 'user', content: "Let's plan the migration in detail across the three services." }],
    });
    assert.equal(res.status, 200);
    assert.equal(captured[0]?.body?.model, 'global.anthropic.claude-opus-4-7');
  });

  it('accepts request without x-api-key when proxy has ANTHROPIC_API_KEY env (token mediation)', async () => {
    const prevKey = process.env.ANTHROPIC_API_KEY;
    const prevTok = process.env.ANTHROPIC_AUTH_TOKEN;
    process.env.ANTHROPIC_API_KEY = 'sk-proxy-env';
    delete process.env.ANTHROPIC_AUTH_TOKEN;
    try {
      const u = new URL(`${baseUrl}/v1/messages`);
      const payload = JSON.stringify({ model: 'global.anthropic.claude-opus-4-7', messages: [{ role: 'user', content: 'hi' }] });
      const res = await new Promise((resolve, reject) => {
        const req = http.request({
          hostname: u.hostname,
          port: u.port,
          path: u.pathname,
          method: 'POST',
          headers: {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(payload),
            'anthropic-version': '2023-06-01',
          },
        }, (resp) => {
          const chunks = [];
          resp.on('data', (c) => chunks.push(c));
          resp.on('end', () => resolve({ status: resp.statusCode, body: Buffer.concat(chunks).toString() }));
        });
        req.on('error', reject);
        req.write(payload);
        req.end();
      });
      assert.equal(res.status, 200, 'mediated request should not 401');
    } finally {
      if (prevKey === undefined) delete process.env.ANTHROPIC_API_KEY;
      else process.env.ANTHROPIC_API_KEY = prevKey;
      if (prevTok !== undefined) process.env.ANTHROPIC_AUTH_TOKEN = prevTok;
    }
  });

  it('returns 401 when x-api-key is missing and proxy has no env creds', async () => {
    const prevKey = process.env.ANTHROPIC_API_KEY;
    const prevTok = process.env.ANTHROPIC_AUTH_TOKEN;
    delete process.env.ANTHROPIC_API_KEY;
    delete process.env.ANTHROPIC_AUTH_TOKEN;
    try {
      const u = new URL(`${baseUrl}/v1/messages`);
      const payload = JSON.stringify({ model: 'm', messages: [{ role: 'user', content: 'hi' }] });
      const res = await new Promise((resolve, reject) => {
        const req = http.request({
          hostname: u.hostname,
          port: u.port,
          path: u.pathname,
          method: 'POST',
          headers: {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(payload),
          },
        }, (resp) => {
          const chunks = [];
          resp.on('data', (c) => chunks.push(c));
          resp.on('end', () => resolve({ status: resp.statusCode, body: Buffer.concat(chunks).toString() }));
        });
        req.on('error', reject);
        req.write(payload);
        req.end();
      });
      assert.equal(res.status, 401);
      assert.equal(JSON.parse(res.body).error, 'x-api-key required');
    } finally {
      if (prevKey !== undefined) process.env.ANTHROPIC_API_KEY = prevKey;
      if (prevTok !== undefined) process.env.ANTHROPIC_AUTH_TOKEN = prevTok;
    }
  });

  it('passes through streaming responses with SSE bytes verbatim', async () => {
    const res = await rawPost(`${baseUrl}/v1/messages`, token, {
      model: 'global.anthropic.claude-opus-4-7',
      stream: true,
      messages: [{ role: 'user', content: 'hi' }],
    });
    assert.equal(res.status, 200);
    assert.equal(res.headers['content-type'], 'text/event-stream');
    assert.match(res.body, /data: \{"type":"message_start"\}/);
    assert.match(res.body, /data: \{"type":"message_stop"\}/);
  });

  it('retries with original_model when upstream returns 5xx on a router-rewritten request', async () => {
    // trivial_lookup → router rewrites opus → cheap (haiku). Stub first returns
    // 503 (simulating "no channel for haiku" in a one-hub gateway); shim should
    // retry once with the original model and surface the 200 to the client.
    const u = new URL(`${baseUrl}/v1/messages`);
    const payload = JSON.stringify({
      model: 'global.anthropic.claude-opus-4-7',
      messages: [{ role: 'user', content: 'what is npm?' }],
    });
    const res = await new Promise((resolve, reject) => {
      const req = http.request({
        hostname: u.hostname,
        port: u.port,
        path: u.pathname,
        method: 'POST',
        headers: {
          'Authorization': 'Bearer ' + token,
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(payload),
          'x-api-key': 'sk-test',
          'x-test-mode': '503-then-200',
        },
      }, (resp) => {
        const chunks = [];
        resp.on('data', (c) => chunks.push(c));
        resp.on('end', () => resolve({ status: resp.statusCode, body: Buffer.concat(chunks).toString() }));
      });
      req.on('error', reject);
      req.write(payload);
      req.end();
    });
    assert.equal(res.status, 200, 'retry should surface 200 to client');
    assert.equal(captured.length, 2, 'should make exactly two upstream calls');
    assert.equal(captured[0].body.model, 'global.anthropic.claude-haiku-4-5-20251001-v1:0', 'first call uses router-chosen model');
    assert.equal(captured[1].body.model, 'global.anthropic.claude-opus-4-7', 'retry uses original model');
    const json = JSON.parse(res.body);
    assert.equal(json.model, 'global.anthropic.claude-opus-4-7');
  });

  it('does not retry when router did not rewrite the model', async () => {
    // Send sonnet-4-7 with a long non-planning message → router lands on
    // default_tier=mid → sonnet-4-7, so chosenModel === originalModel
    // and the 5xx fallback branch must be skipped (single upstream call).
    // Message must be >80 chars to avoid trivial_lookup classification.
    const u = new URL(`${baseUrl}/v1/messages`);
    const payload = JSON.stringify({
      model: 'global.anthropic.claude-sonnet-4-7',
      messages: [{
        role: 'user',
        content: 'Could you walk me through how the request handling layer connects to the storage subsystem and which module owns retries here.',
      }],
    });
    const res = await new Promise((resolve, reject) => {
      const req = http.request({
        hostname: u.hostname,
        port: u.port,
        path: u.pathname,
        method: 'POST',
        headers: {
          'Authorization': 'Bearer ' + token,
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(payload),
          'x-api-key': 'sk-test',
          'x-test-mode': '503-then-200',
        },
      }, (resp) => {
        const chunks = [];
        resp.on('data', (c) => chunks.push(c));
        resp.on('end', () => resolve({ status: resp.statusCode, body: Buffer.concat(chunks).toString() }));
      });
      req.on('error', reject);
      req.write(payload);
      req.end();
    });
    assert.equal(res.status, 503, 'no rewrite → no retry → 503 surfaces verbatim');
    assert.equal(captured.length, 1, 'should make exactly one upstream call');
  });

  it('retries streaming request with original_model when upstream returns 5xx after rewrite', async () => {
    // Mirrors the JSON-retry test but with stream:true. The classifier picks
    // cheap (haiku) for the trivial lookup; first call gets a JSON 503 (no
    // SSE has flowed yet); shim retries with the original opus model and the
    // stub returns SSE on the second hit. The route must surface that stream
    // to the client — Bugbot PR #83 caught a `!retryUpstream.stream` guard
    // that silently dropped it.
    const u = new URL(`${baseUrl}/v1/messages`);
    const payload = JSON.stringify({
      model: 'global.anthropic.claude-opus-4-7',
      stream: true,
      messages: [{ role: 'user', content: 'what is npm?' }],
    });
    const res = await new Promise((resolve, reject) => {
      const req = http.request({
        hostname: u.hostname,
        port: u.port,
        path: u.pathname,
        method: 'POST',
        headers: {
          'Authorization': 'Bearer ' + token,
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(payload),
          'x-api-key': 'sk-test',
          'x-test-mode': '503-then-200',
        },
      }, (resp) => {
        const chunks = [];
        resp.on('data', (c) => chunks.push(c));
        resp.on('end', () => resolve({
          status: resp.statusCode,
          headers: resp.headers,
          body: Buffer.concat(chunks).toString(),
        }));
      });
      req.on('error', reject);
      req.write(payload);
      req.end();
    });
    assert.equal(res.status, 200, 'streaming retry should surface 200 to client');
    assert.equal(res.headers['content-type'], 'text/event-stream');
    assert.match(res.body, /data: \{"type":"message_start"\}/);
    assert.match(res.body, /data: \{"type":"message_stop"\}/);
    assert.equal(captured.length, 2, 'should make exactly two upstream calls');
    assert.equal(captured[0].body.model, 'global.anthropic.claude-haiku-4-5-20251001-v1:0', 'first call uses router-chosen model');
    assert.equal(captured[1].body.model, 'global.anthropic.claude-opus-4-7', 'retry uses original model');
  });

  it('replays drained 5xx body when retry itself throws', async () => {
    // Bugbot follow-up: the drain we add to release undici's socket reads
    // upstream.text() exactly once. If the retry fetch then rejects (real
    // upstream socket drop), finalUpstream falls back to a cached replay
    // so the client still sees the original 503 + body — not an empty
    // result that the HTTP layer's `result.body || result` fallback would
    // turn into a leaked envelope.
    const u = new URL(`${baseUrl}/v1/messages`);
    const payload = JSON.stringify({
      model: 'global.anthropic.claude-opus-4-7',
      messages: [{ role: 'user', content: 'what is npm?' }],
    });
    const res = await new Promise((resolve, reject) => {
      const req = http.request({
        hostname: u.hostname,
        port: u.port,
        path: u.pathname,
        method: 'POST',
        headers: {
          'Authorization': 'Bearer ' + token,
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(payload),
          'x-api-key': 'sk-test',
          'x-test-mode': '503-then-throw',
        },
      }, (resp) => {
        const chunks = [];
        resp.on('data', (c) => chunks.push(c));
        resp.on('end', () => resolve({ status: resp.statusCode, body: Buffer.concat(chunks).toString() }));
      });
      req.on('error', reject);
      req.write(payload);
      req.end();
    });
    assert.equal(res.status, 503, 'retry-throw should surface the original 503');
    assert.equal(JSON.parse(res.body).error, 'no channel', 'drained body must round-trip');
    assert.equal(captured.length, 2, 'first 503 + retry that destroyed socket');
  });

  it('relays Anthropic 5xx verbatim, no SSE synthesis', async () => {
    const u = new URL(`${baseUrl}/v1/messages`);
    const payload = JSON.stringify({ model: 'm', messages: [{ role: 'user', content: 'hi' }] });
    const res = await new Promise((resolve, reject) => {
      const req = http.request({
        hostname: u.hostname,
        port: u.port,
        path: u.pathname,
        method: 'POST',
        headers: {
          'Authorization': 'Bearer ' + token,
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(payload),
          'x-api-key': 'sk-test',
          'x-test-mode': '503',
        },
      }, (resp) => {
        const chunks = [];
        resp.on('data', (c) => chunks.push(c));
        resp.on('end', () => resolve({ status: resp.statusCode, body: Buffer.concat(chunks).toString() }));
      });
      req.on('error', reject);
      req.write(payload);
      req.end();
    });
    assert.equal(res.status, 503);
    assert.equal(JSON.parse(res.body).error, 'overloaded');
  });

  it('wraps non-JSON upstream response in {error} envelope instead of 500', async () => {
    // Caught during Phase C smoke against a local gateway (prism) that
    // returned "404 page not found" as text/plain — naive .json() on that
    // throws SyntaxError and the route used to surface 500 with a
    // "Unexpected non-whitespace character" body. The fix wraps the raw
    // text in {error} so the client sees the actual upstream status code
    // plus a readable body.
    const u = new URL(`${baseUrl}/v1/messages`);
    const payload = JSON.stringify({ model: 'm', messages: [{ role: 'user', content: 'hi' }] });
    const res = await new Promise((resolve, reject) => {
      const req = http.request({
        hostname: u.hostname,
        port: u.port,
        path: u.pathname,
        method: 'POST',
        headers: {
          'Authorization': 'Bearer ' + token,
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(payload),
          'x-api-key': 'sk-test',
          'x-test-mode': 'text-plain-404',
        },
      }, (resp) => {
        const chunks = [];
        resp.on('data', (c) => chunks.push(c));
        resp.on('end', () => resolve({ status: resp.statusCode, body: Buffer.concat(chunks).toString() }));
      });
      req.on('error', reject);
      req.write(payload);
      req.end();
    });
    assert.equal(res.status, 404, 'real upstream status surfaces, not 500');
    const parsed = JSON.parse(res.body);
    assert.match(parsed.error, /404 page not found/, 'raw upstream text surfaces in error envelope');
  });
});
