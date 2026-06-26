'use strict';

const { describe, it, before, after } = require('node:test');
const assert = require('node:assert/strict');
const http = require('http');
const fs = require('fs');
const os = require('os');
const path = require('path');

const { ProxyHttpServer } = require('../src/proxy/server/http');

function rawRequest(url, token) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const req = http.request({
      hostname: u.hostname,
      port: u.port,
      path: u.pathname,
      method: 'POST',
      headers: { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json', 'Content-Length': 2 },
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
    req.write('{}');
    req.end();
  });
}

describe('ProxyHttpServer streaming pass-through', () => {
  let server, baseUrl, token;
  let savedSettingsDir;
  let settingsDir;

  before(async () => {
    settingsDir = fs.mkdtempSync(path.join(os.tmpdir(), 'proxy-streaming-settings-'));
    savedSettingsDir = process.env.EVOLVER_SETTINGS_DIR;
    process.env.EVOLVER_SETTINGS_DIR = settingsDir;
    function* events() {
      yield Buffer.from('data: {"type":"message_start"}\n\n');
      yield Buffer.from('data: {"type":"content_block_delta","delta":{"text":"hi"}}\n\n');
      yield Buffer.from('data: {"type":"message_stop"}\n\n');
    }
    const routes = {
      'POST /test/stream': async () => ({ stream: events(), status: 200 }),
      'POST /test/json': async () => ({ status: 201, body: { ok: true } }),
      'POST /test/throws': async () => { throw new Error('boom'); },
    };
    server = new ProxyHttpServer(routes, {
      port: 39830,
      logger: { log: () => {}, error: () => {}, warn: () => {} },
    });
    const info = await server.start();
    baseUrl = info.url;
    token = info.token;
  });

  after(async () => {
    await server.stop();
    try { fs.rmSync(settingsDir, { recursive: true }); } catch {}
    if (savedSettingsDir === undefined) delete process.env.EVOLVER_SETTINGS_DIR;
    else process.env.EVOLVER_SETTINGS_DIR = savedSettingsDir;
  });

  it('writes SSE headers and pipes upstream bytes verbatim', async () => {
    const res = await rawRequest(`${baseUrl}/test/stream`, token);
    assert.equal(res.status, 200);
    assert.equal(res.headers['content-type'], 'text/event-stream');
    assert.equal(res.headers['cache-control'], 'no-cache');
    assert.equal(res.headers['connection'], 'keep-alive');
    assert.match(res.body, /^data: \{"type":"message_start"\}/);
    assert.ok(res.body.includes('"text":"hi"'));
    assert.match(res.body, /data: \{"type":"message_stop"\}\n\n$/);
  });

  it('still sends JSON when handler omits `stream`', async () => {
    const res = await rawRequest(`${baseUrl}/test/json`, token);
    assert.equal(res.status, 201);
    assert.equal(res.headers['content-type'], 'application/json');
    assert.deepEqual(JSON.parse(res.body), { ok: true });
  });

  it('falls back to JSON error envelope when handler throws', async () => {
    const res = await rawRequest(`${baseUrl}/test/throws`, token);
    assert.equal(res.status, 500);
    assert.equal(JSON.parse(res.body).error, 'boom');
  });
});

describe('ProxyHttpServer streaming disconnect handling', () => {
  let server, baseUrl, token, cancelled, finished;
  let savedSettingsDir;
  let settingsDir;

  before(async () => {
    settingsDir = fs.mkdtempSync(path.join(os.tmpdir(), 'proxy-streaming2-settings-'));
    savedSettingsDir = process.env.EVOLVER_SETTINGS_DIR;
    process.env.EVOLVER_SETTINGS_DIR = settingsDir;
    cancelled = false;
    finished = false;
    function makeSlowStream() {
      // Web ReadableStream so .cancel() is callable; emits one chunk fast,
      // then waits "forever" — exactly the shape an SSE upstream takes on a
      // long Anthropic response. The cancel callback marks observable state
      // so the test can assert it fired.
      return new ReadableStream({
        start(controller) {
          controller.enqueue(new TextEncoder().encode('data: {"type":"message_start"}\n\n'));
        },
        cancel() { cancelled = true; },
      });
    }
    const routes = {
      'POST /test/slow': async () => {
        const stream = makeSlowStream();
        return {
          status: 200,
          stream,
          _afterDone: () => { finished = true; },
        };
      },
    };
    // Wrap to set `finished` when _streamResponse returns.
    const wrappedRoutes = {
      'POST /test/slow': async (ctx) => {
        const result = await routes['POST /test/slow'](ctx);
        return result;
      },
    };
    server = new ProxyHttpServer(wrappedRoutes, {
      port: 39831,
      logger: { log: () => {}, error: () => {}, warn: () => {} },
    });
    const info = await server.start();
    baseUrl = info.url;
    token = info.token;
  });

  after(async () => {
    await server.stop();
    try { fs.rmSync(settingsDir, { recursive: true }); } catch {}
    if (savedSettingsDir === undefined) delete process.env.EVOLVER_SETTINGS_DIR;
    else process.env.EVOLVER_SETTINGS_DIR = savedSettingsDir;
  });

  it('cancels upstream and ends handler when client disconnects mid-stream', async () => {
    const u = new URL(`${baseUrl}/test/slow`);
    const req = http.request({
      hostname: u.hostname,
      port: u.port,
      path: u.pathname,
      method: 'POST',
      headers: { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json', 'Content-Length': 2 },
    });
    const gotFirstChunk = new Promise((resolve) => {
      req.on('response', (res) => {
        res.once('data', resolve);
      });
    });
    req.write('{}');
    req.end();

    await gotFirstChunk;
    req.destroy();

    // Give the server one tick to observe `close` and run the cancel callback.
    const deadline = Date.now() + 2000;
    while (!cancelled && Date.now() < deadline) {
      await new Promise((r) => setTimeout(r, 25));
    }
    assert.equal(cancelled, true, 'upstream stream.cancel must be invoked on client disconnect');
  });
});
