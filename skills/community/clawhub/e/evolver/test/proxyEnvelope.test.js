'use strict';

// Regression tests for the GEP-A2A envelope wrapping in the proxy.
//
// Background: the hub's /a2a/fetch and /a2a/validate are strict protocol
// endpoints -- they run isValidProtocolMessage server-side and reject bare
// bodies ({asset_ids: [...]}) with 400 invalid_protocol_message. The proxy
// used to forward MCP-bridge bodies verbatim, so evolver_fetch_asset was
// 100% broken against the public hub. The GET /a2a/assets/search path is
// lenient REST and must keep going out envelope-free.

const { describe, it, before, after } = require('node:test');
const assert = require('node:assert/strict');
const http = require('http');
const fs = require('fs');
const os = require('os');
const path = require('path');

const { buildEnvelope, ensureEnvelope, PROTOCOL_NAME, PROTOCOL_VERSION } = require('../src/proxy/envelope');
const { startProxy } = require('../src/proxy');

// hubFetch enforces https; the in-process mock hub only speaks the
// non-https form. node --test gives each file its own worker process, so
// this env var does not leak to sibling test files.
const _origInsecure = process.env.EVOMAP_HUB_ALLOW_INSECURE;
process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';
after(() => {
  if (_origInsecure === undefined) delete process.env.EVOMAP_HUB_ALLOW_INSECURE;
  else process.env.EVOMAP_HUB_ALLOW_INSECURE = _origInsecure;
});

const silentLogger = { log: () => {}, warn: () => {}, error: () => {} };

describe('buildEnvelope', () => {
  it('produces a complete GEP-A2A envelope', () => {
    const env = buildEnvelope('fetch', { asset_ids: ['sha256:abc'] }, 'node_abcdef123456');
    assert.equal(env.protocol, PROTOCOL_NAME);
    assert.equal(env.protocol_version, PROTOCOL_VERSION);
    assert.equal(env.message_type, 'fetch');
    assert.match(env.message_id, /^msg_\d+_[0-9a-f]{8}$/);
    assert.equal(env.sender_id, 'node_abcdef123456');
    assert.ok(!Number.isNaN(Date.parse(env.timestamp)));
    assert.deepEqual(env.payload, { asset_ids: ['sha256:abc'] });
  });

  it('defaults payload to {} and sender_id to null', () => {
    const env = buildEnvelope('validate');
    assert.deepEqual(env.payload, {});
    assert.equal(env.sender_id, null);
  });

  it('generates unique message_ids', () => {
    const a = buildEnvelope('fetch', {}, 'node_a');
    const b = buildEnvelope('fetch', {}, 'node_a');
    assert.notEqual(a.message_id, b.message_id);
  });

  it('rejects a missing messageType', () => {
    assert.throws(() => buildEnvelope(''), /messageType is required/);
    assert.throws(() => buildEnvelope(null), /messageType is required/);
  });
});

describe('ensureEnvelope', () => {
  it('wraps a bare body as the payload', () => {
    const env = ensureEnvelope('fetch', { asset_ids: ['sha256:a', 'sha256:b'] }, 'node_123456789abc');
    assert.equal(env.protocol, PROTOCOL_NAME);
    assert.equal(env.message_type, 'fetch');
    assert.equal(env.sender_id, 'node_123456789abc');
    assert.deepEqual(env.payload, { asset_ids: ['sha256:a', 'sha256:b'] });
  });

  it('wraps a null/empty body with an empty payload', () => {
    const env = ensureEnvelope('validate', null, 'node_123456789abc');
    assert.deepEqual(env.payload, {});
  });

  it('passes a pre-built envelope through but forces sender_id', () => {
    const pre = buildEnvelope('fetch', { asset_ids: ['sha256:x'] }, 'node_impersonated');
    const env = ensureEnvelope('fetch', pre, 'node_proxy_own_id');
    assert.equal(env.sender_id, 'node_proxy_own_id');
    assert.equal(env.message_id, pre.message_id);
    assert.deepEqual(env.payload, pre.payload);
  });

  it('keeps the original sender_id when the proxy has none yet', () => {
    const pre = buildEnvelope('fetch', {}, 'node_original');
    const env = ensureEnvelope('fetch', pre, null);
    assert.equal(env.sender_id, 'node_original');
  });
});

// --- End-to-end: proxy routes -> _proxyHttp -> mock hub ---------------------

// Mirrors the hub's isValidProtocolMessage (src/lib/a2aProtocol.js in
// evomap-hub) plus the validateProtocol message_type check.
function hubValidate(msg, allowedTypes) {
  if (!msg || typeof msg !== 'object') return 'invalid_protocol_message';
  if (msg.protocol !== 'gep-a2a') return 'invalid_protocol_message';
  if (!msg.message_type) return 'invalid_protocol_message';
  if (!msg.message_id || typeof msg.message_id !== 'string') return 'invalid_protocol_message';
  if (!msg.timestamp || typeof msg.timestamp !== 'string') return 'invalid_protocol_message';
  if (!allowedTypes.includes(msg.message_type)) return 'message_type_mismatch';
  if (!msg.sender_id) return 'sender_id_required';
  return null;
}

function readBody(req) {
  return new Promise((resolve) => {
    const chunks = [];
    req.on('data', (c) => chunks.push(c));
    req.on('end', () => {
      try { resolve(JSON.parse(Buffer.concat(chunks).toString() || '{}')); }
      catch { resolve({}); }
    });
  });
}

describe('proxy /asset/* -> hub envelope wrapping (e2e)', () => {
  let hub, hubUrl, proxy, proxyUrl, dataDir;
  let savedSettingsDir;
  const seen = { fetch: [], validate: [], search: [], record: [] };

  before(async () => {
    hub = http.createServer(async (req, res) => {
      const body = await readBody(req);
      const respond = (status, obj) => {
        res.writeHead(status, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(obj));
      };
      if (req.url === '/a2a/hello') {
        const err = hubValidate(body, ['hello']);
        if (err) return respond(400, { error: err });
        return respond(200, {
          protocol: 'gep-a2a',
          message_type: 'hello',
          payload: { node_secret: 'a'.repeat(64) },
        });
      }
      if (req.url === '/a2a/fetch') {
        seen.fetch.push(body);
        const err = hubValidate(body, ['fetch']);
        if (err) return respond(400, { error: err });
        const ids = Array.isArray(body.payload.asset_ids) ? body.payload.asset_ids : [];
        return respond(200, {
          protocol: 'gep-a2a',
          message_type: 'fetch',
          payload: {
            results: ids.map((id) => ({ asset_id: id, type: 'Gene', content: 'x' })),
            count: ids.length,
          },
        });
      }
      if (req.url === '/a2a/validate') {
        seen.validate.push(body);
        const err = hubValidate(body, ['validate', 'publish']);
        if (err) return respond(400, { error: err });
        return respond(200, { protocol: 'gep-a2a', message_type: 'validate', payload: { valid: true } });
      }
      if (req.url === '/a2a/memory/record') {
        seen.record.push(body);
        // The hub reads a FLAT top-level body here (not the GEP envelope):
        // it 400s on missing/empty top-level signals.
        if (!body || !Array.isArray(body.signals) || body.signals.length === 0) {
          return respond(400, { error: 'signals required' });
        }
        return respond(200, { ok: true, recorded: 'mge_test' });
      }
      const parsedUrl = new URL(req.url, 'http://localhost');
      if (parsedUrl.pathname === '/a2a/assets/search') {
        // Mirrors the real hub: the route is registered GET-only, so any
        // other method gets the router's 404.
        if (req.method !== 'GET') return respond(404, { error: 'route_not_found' });
        seen.search.push({
          method: req.method,
          query: Object.fromEntries(parsedUrl.searchParams),
          body,
        });
        return respond(200, { results: [], count: 0 });
      }
      respond(200, {});
    });
    await new Promise((resolve) => hub.listen(0, '127.0.0.1', resolve));
    hubUrl = `http://127.0.0.1:${hub.address().port}`;

    dataDir = fs.mkdtempSync(path.join(os.tmpdir(), 'proxy-envelope-test-'));
    savedSettingsDir = process.env.EVOLVER_SETTINGS_DIR;
    process.env.EVOLVER_SETTINGS_DIR = path.join(dataDir, 'settings');
    const started = await startProxy({ hubUrl, dataDir, port: 39832, logger: silentLogger });
    proxy = started.proxy;
    proxyUrl = started.url;
  });

  after(async () => {
    await proxy?.stop();
    await new Promise((resolve) => hub.close(resolve));
    if (savedSettingsDir === undefined) delete process.env.EVOLVER_SETTINGS_DIR;
    else process.env.EVOLVER_SETTINGS_DIR = savedSettingsDir;
    try { fs.rmSync(dataDir, { recursive: true }); } catch {}
  });

  async function post(p, body) {
    const res = await fetch(`${proxyUrl}${p}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${proxy.server.token}`,
      },
      body: JSON.stringify(body),
    });
    return { status: res.status, body: await res.json() };
  }

  it('POST /asset/fetch with a single bare asset_id passes hub protocol validation', async () => {
    const res = await post('/asset/fetch', { asset_ids: ['sha256:single'] });
    assert.equal(res.status, 200);
    assert.equal(res.body.payload.count, 1);
    assert.equal(res.body.payload.results[0].asset_id, 'sha256:single');

    const sent = seen.fetch.at(-1);
    assert.equal(hubValidate(sent, ['fetch']), null);
    assert.equal(sent.sender_id, proxy.store.getState('node_id'));
    assert.deepEqual(sent.payload, { asset_ids: ['sha256:single'] });
  });

  it('POST /asset/fetch with multiple asset_ids passes hub protocol validation', async () => {
    const ids = ['sha256:a', 'sha256:b', 'sha256:c'];
    const res = await post('/asset/fetch', { asset_ids: ids });
    assert.equal(res.status, 200);
    assert.equal(res.body.payload.count, 3);
    assert.deepEqual(seen.fetch.at(-1).payload, { asset_ids: ids });
  });

  it('POST /asset/validate wraps the body with message_type "validate"', async () => {
    const res = await post('/asset/validate', { asset_id: 'sha256:v' });
    assert.equal(res.status, 200);
    assert.equal(res.body.payload.valid, true);

    const sent = seen.validate.at(-1);
    assert.equal(sent.message_type, 'validate');
    assert.equal(hubValidate(sent, ['validate', 'publish']), null);
    assert.deepEqual(sent.payload, { asset_id: 'sha256:v' });
  });

  it('POST /asset/search stays a bare GET -- no envelope, signals comma-joined', async () => {
    const res = await post('/asset/search', {
      signals: ['log_error', 'timeout'],
      limit: 5,
    });
    assert.equal(res.status, 200);

    const sent = seen.search.at(-1);
    assert.equal(sent.method, 'GET');
    // GET requests carry no body -- and in particular no envelope.
    assert.deepEqual(sent.body, {});
    // The proxy stamps its own node_id for hub-side attribution (bulkFetchGuard
    // / per-node metering), alongside the comma-joined signals.
    assert.deepEqual(sent.query, {
      signals: 'log_error,timeout',
      limit: '5',
      node_id: proxy.store.getState('node_id'),
    });
  });

  it('POST /asset/report-reuse forwards a FLAT (non-enveloped) body to /a2a/memory/record', async () => {
    const res = await post('/asset/report-reuse', {
      used_asset_ids: ['sha256:r1', 'sha256:r2'],
      status: 'success',
    });
    assert.equal(res.status, 200);
    assert.equal(res.body.ok, true);
    assert.equal(res.body.recorded, 'mge_test');

    const sent = seen.record.at(-1);
    // FLAT body: sender_id/signals/status/used_asset_ids live at the TOP level,
    // NOT under .payload -- the hub's /a2a/memory/record reads them top-level,
    // so envelope-wrapping (like fetch/validate) would make the record 400.
    assert.equal(sent.payload, undefined, 'must NOT be a GEP envelope');
    assert.equal(sent.sender_id, proxy.store.getState('node_id'));
    assert.equal(sent.status, 'success');
    assert.deepEqual(sent.used_asset_ids, ['sha256:r1', 'sha256:r2']);
    assert.ok(Array.isArray(sent.signals) && sent.signals.length > 0, 'non-empty signals default applied');
  });
});
