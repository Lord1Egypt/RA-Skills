'use strict';

const { describe, it, before, after, beforeEach } = require('node:test');
const assert = require('node:assert/strict');
const http = require('http');
const fs = require('fs');
const os = require('os');
const path = require('path');

const { MailboxStore } = require('../src/proxy/mailbox/store');
const { ProxyHttpServer, DEFAULT_PORT } = require('../src/proxy/server/http');
const { buildRoutes } = require('../src/proxy/server/routes');

function tmpDataDir() {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'proxy-test-'));
}

function request(url, method, body, token) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const payload = body ? JSON.stringify(body) : '';
    const headers = {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(payload),
    };
    if (token) headers['Authorization'] = 'Bearer ' + token;
    const req = http.request({
      hostname: u.hostname,
      port: u.port,
      path: u.pathname + u.search,
      method,
      headers,
    }, (res) => {
      const chunks = [];
      res.on('data', c => chunks.push(c));
      res.on('end', () => {
        const raw = Buffer.concat(chunks).toString();
        try { resolve({ status: res.statusCode, body: JSON.parse(raw) }); }
        catch { resolve({ status: res.statusCode, body: raw }); }
      });
    });
    req.on('error', reject);
    if (payload) req.write(payload);
    req.end();
  });
}

describe('ProxyHttpServer', () => {
  let store, server, baseUrl, dataDir, serverToken;
  let authedReq;
  let savedSettingsDir;
  let settingsDir;

  before(async () => {
    dataDir = tmpDataDir();
    store = new MailboxStore(dataDir);
    // Redirect proxy settings into a temp dir so server.start() does not
    // write to the shared ~/.evolver/settings.json and race with the webui
    // observer test running in a parallel worker.
    settingsDir = fs.mkdtempSync(path.join(os.tmpdir(), 'proxy-settings-'));
    savedSettingsDir = process.env.EVOLVER_SETTINGS_DIR;
    process.env.EVOLVER_SETTINGS_DIR = settingsDir;

    const mockProxyHandlers = {
      assetFetch: async (body) => ({ assets: [], query: body }),
      assetSearch: async (body) => ({ results: [], query: body }),
      assetValidate: async (body) => ({ valid: true, asset_id: body.asset_id || 'test' }),
      assetPublish: async (body) => ({
        published: (body.assets || []).length,
        total: (body.assets || []).length,
        results: (body.assets || []).map(() => ({ ok: true, gene_asset_id: 'sha256:test', capsule_asset_id: 'sha256:test' })),
      }),
    };

    const routes = buildRoutes(store, mockProxyHandlers, null, {});

    server = new ProxyHttpServer(routes, { port: 39820, logger: { log: () => {}, error: () => {}, warn: () => {} } });
    const info = await server.start();
    baseUrl = info.url;
    serverToken = info.token;
    authedReq = (url, method, body) => request(url, method, body, serverToken);
  });

  after(async () => {
    await server.stop();
    store.close();
    try { fs.rmSync(dataDir, { recursive: true }); } catch {}
    try { fs.rmSync(settingsDir, { recursive: true }); } catch {}
    if (savedSettingsDir === undefined) delete process.env.EVOLVER_SETTINGS_DIR;
    else process.env.EVOLVER_SETTINGS_DIR = savedSettingsDir;
  });

  describe('POST /mailbox/send', () => {
    it('sends a message and returns message_id', async () => {
      const res = await authedReq(`${baseUrl}/mailbox/send`, 'POST', {
        type: 'asset_submit',
        payload: { data: 'test' },
      });
      assert.equal(res.status, 200);
      assert.ok(res.body.message_id);
      assert.equal(res.body.status, 'pending');
    });

    it('rejects missing type', async () => {
      const res = await authedReq(`${baseUrl}/mailbox/send`, 'POST', {
        payload: { data: 'test' },
      });
      assert.equal(res.status, 400);
    });

    it('rejects missing payload', async () => {
      const res = await authedReq(`${baseUrl}/mailbox/send`, 'POST', {
        type: 'test',
      });
      assert.equal(res.status, 400);
    });
  });

  describe('POST /mailbox/poll', () => {
    it('returns inbound messages', async () => {
      store.writeInbound({ type: 'poll_test', payload: { x: 1 } });
      const res = await authedReq(`${baseUrl}/mailbox/poll`, 'POST', {
        type: 'poll_test',
      });
      assert.equal(res.status, 200);
      assert.ok(res.body.messages.length >= 1);
    });
  });

  describe('POST /mailbox/ack', () => {
    it('acknowledges messages', async () => {
      const id = store.writeInbound({ type: 'ack_test', payload: {} });
      const res = await authedReq(`${baseUrl}/mailbox/ack`, 'POST', {
        message_ids: [id],
      });
      assert.equal(res.status, 200);
      assert.equal(res.body.acknowledged, 1);
    });

    it('rejects missing message_ids', async () => {
      const res = await authedReq(`${baseUrl}/mailbox/ack`, 'POST', {});
      assert.equal(res.status, 400);
    });
  });

  describe('GET /mailbox/status/:id', () => {
    it('returns message details', async () => {
      const { message_id } = store.send({ type: 'status_test', payload: { test: true } });
      const res = await authedReq(`${baseUrl}/mailbox/status/${message_id}`, 'GET');
      assert.equal(res.status, 200);
      assert.equal(res.body.id, message_id);
      assert.equal(res.body.type, 'status_test');
    });

    it('returns 404 for unknown id', async () => {
      const res = await authedReq(`${baseUrl}/mailbox/status/nonexistent`, 'GET');
      assert.equal(res.status, 404);
    });
  });

  describe('GET /mailbox/list', () => {
    it('lists messages by type', async () => {
      store.send({ type: 'list_http_test', payload: {} });
      const res = await authedReq(`${baseUrl}/mailbox/list?type=list_http_test`, 'GET');
      assert.equal(res.status, 200);
      assert.ok(res.body.messages.length >= 1);
    });

    it('requires type query param', async () => {
      const res = await authedReq(`${baseUrl}/mailbox/list`, 'GET');
      assert.equal(res.status, 400);
    });
  });

  describe('POST /asset/submit', () => {
    it('publishes asset submission via the /a2a/publish bundle path', async () => {
      const res = await authedReq(`${baseUrl}/asset/submit`, 'POST', {
        assets: [{ type: 'Gene', content: 'test' }],
      });
      assert.equal(res.status, 200);
      // No longer the gated mailbox path (which returned a queued message_id);
      // routes through proxyHandlers.assetPublish → POST /a2a/publish.
      assert.equal(res.body.published, 1);
      assert.ok(Array.isArray(res.body.results));
    });

    it('rejects missing assets and asset_id', async () => {
      const res = await authedReq(`${baseUrl}/asset/submit`, 'POST', {
        priority: 'high',
      });
      assert.equal(res.status, 400);
    });
  });

  describe('POST /conversation/distill', () => {
    const validConversation = {
      summary: 'Reusable Evolver distill endpoint compatibility workflow for MCP plugin bridges.',
      assistant_summary: 'Added a Proxy conversation distillation bridge so Codex, Claude Code, Cursor, WorkBuddy, and Antigravity plugins can publish Genes and Capsules without hitting a 404.',
      strategy: [
        'Verify each plugin bridge calls the same Proxy route before changing repository code.',
        'Keep the Proxy route on the current signed asset publish path instead of the old mailbox submit path.',
        'Add focused tests for draft distillation, publish forwarding, and low quality skipped inputs.',
      ],
      artifacts: ['src/proxy/server/routes.js', 'src/gep/conversationDistiller.js'],
      validation: ['node --test test/proxyServer.test.js'],
      signals: ['distill_endpoint', 'proxy_compatibility', 'test_verified'],
    };

    it('distills a high-confidence conversation as a draft when publish and persist are disabled', async () => {
      const res = await authedReq(`${baseUrl}/conversation/distill`, 'POST', {
        ...validConversation,
        persist: false,
        publish: false,
      });
      assert.equal(res.status, 200);
      assert.equal(res.body.ok, true);
      assert.equal(res.body.status, 'draft');
      assert.equal(res.body.published, false);
      assert.equal(res.body.publish_result, null);
      assert.equal(res.body.gene.type, 'Gene');
      assert.equal(res.body.capsule.type, 'Capsule');
      assert.deepEqual(res.body.capsule.blast_radius, { files: 1, lines: 1 });
      assert.equal(typeof res.body.capsule.content, 'string');
      assert.equal(typeof res.body.capsule.diff, 'string');
      assert.equal(typeof res.body.capsule.reused_asset_id, 'string');
      assert.equal(typeof res.body.capsule.env_fingerprint, 'object');
    });

    it('publishes distilled Gene and Capsule through the current asset publish handler', async () => {
      const res = await authedReq(`${baseUrl}/conversation/distill`, 'POST', {
        ...validConversation,
        persist: false,
      });
      assert.equal(res.status, 200);
      assert.equal(res.body.ok, true);
      assert.equal(res.body.published, true);
      assert.equal(res.body.publish_result.published, 2);
      assert.equal(res.body.publish_result.total, 2);
    });

    it('skips low-signal conversations instead of publishing noise', async () => {
      const res = await authedReq(`${baseUrl}/conversation/distill`, 'POST', {
        summary: 'too short',
        publish: false,
      });
      assert.equal(res.status, 200);
      assert.equal(res.body.ok, false);
      assert.equal(res.body.status, 'skipped');
    });
  });

  describe('POST /asset/validate', () => {
    it('validates asset via proxy', async () => {
      const res = await authedReq(`${baseUrl}/asset/validate`, 'POST', {
        asset_id: 'sha256:abc',
      });
      assert.equal(res.status, 200);
      assert.equal(res.body.valid, true);
    });

    it('rejects missing asset_id and assets', async () => {
      const res = await authedReq(`${baseUrl}/asset/validate`, 'POST', {});
      assert.equal(res.status, 400);
    });
  });

  describe('GET /asset/submissions', () => {
    it('lists asset submissions with results', async () => {
      store.send({ type: 'asset_submit', payload: { assets: [{ type: 'Gene' }] } });
      const res = await authedReq(`${baseUrl}/asset/submissions`, 'GET');
      assert.equal(res.status, 200);
      assert.ok(Array.isArray(res.body.submissions));
      assert.ok(res.body.count >= 1);
    });
  });

  describe('POST /asset/fetch', () => {
    it('proxies fetch request (mock)', async () => {
      const res = await authedReq(`${baseUrl}/asset/fetch`, 'POST', {
        asset_ids: ['sha256:abc'],
      });
      assert.equal(res.status, 200);
      assert.ok(res.body.assets);
    });
  });

  describe('POST /asset/search', () => {
    it('proxies search request (mock)', async () => {
      const res = await authedReq(`${baseUrl}/asset/search`, 'POST', {
        signals: ['log_error'],
        mode: 'semantic',
      });
      assert.equal(res.status, 200);
      assert.ok(res.body.results);
    });
  });

  describe('Task routes', () => {
    it('POST /task/subscribe returns message_id', async () => {
      const res = await authedReq(`${baseUrl}/task/subscribe`, 'POST', {});
      assert.equal(res.status, 200);
      assert.ok(res.body.message_id);
    });

    it('POST /task/claim requires task_id', async () => {
      const res = await authedReq(`${baseUrl}/task/claim`, 'POST', {});
      assert.equal(res.status, 400);
    });

    it('POST /task/claim accepts valid task_id', async () => {
      const res = await authedReq(`${baseUrl}/task/claim`, 'POST', { task_id: 'task_123' });
      assert.equal(res.status, 200);
      assert.ok(res.body.message_id);
    });

    it('POST /task/complete requires task_id', async () => {
      const res = await authedReq(`${baseUrl}/task/complete`, 'POST', {});
      assert.equal(res.status, 400);
    });

    it('POST /task/complete accepts valid data', async () => {
      const res = await authedReq(`${baseUrl}/task/complete`, 'POST', {
        task_id: 'task_123',
        asset_id: 'sha256:abc',
      });
      assert.equal(res.status, 200);
      assert.ok(res.body.message_id);
    });
  });

  describe('GET /task/metrics', () => {
    it('returns task metrics (null monitor)', async () => {
      const res = await authedReq(`${baseUrl}/task/metrics`, 'GET');
      assert.equal(res.status, 200);
      assert.equal(res.body.subscribed, false);
    });
  });

  describe('DM routes', () => {
    it('POST /dm/send sends a direct message', async () => {
      const res = await authedReq(`${baseUrl}/dm/send`, 'POST', {
        recipient_node_id: 'node_xyz',
        content: 'Hello from test',
      });
      assert.equal(res.status, 200);
      assert.ok(res.body.message_id);
    });

    it('POST /dm/send rejects missing recipient', async () => {
      const res = await authedReq(`${baseUrl}/dm/send`, 'POST', {
        content: 'Hello',
      });
      assert.equal(res.status, 400);
    });

    it('POST /dm/send rejects missing content', async () => {
      const res = await authedReq(`${baseUrl}/dm/send`, 'POST', {
        recipient_node_id: 'node_xyz',
      });
      assert.equal(res.status, 400);
    });

    it('POST /dm/poll returns DM messages', async () => {
      store.writeInbound({ type: 'dm', payload: { content: 'test dm' } });
      const res = await authedReq(`${baseUrl}/dm/poll`, 'POST', {});
      assert.equal(res.status, 200);
      assert.ok(Array.isArray(res.body.messages));
    });

    it('GET /dm/list lists DM history', async () => {
      const res = await authedReq(`${baseUrl}/dm/list`, 'GET');
      assert.equal(res.status, 200);
      assert.ok(Array.isArray(res.body.messages));
    });
  });

  describe('GET /proxy/status', () => {
    it('returns proxy status with version info', async () => {
      const res = await authedReq(`${baseUrl}/proxy/status`, 'GET');
      assert.equal(res.status, 200);
      assert.equal(res.body.status, 'running');
      assert.ok('outbound_pending' in res.body);
      assert.ok('inbound_pending' in res.body);
      assert.ok(res.body.proxy_protocol_version, 'should include proxy_protocol_version');
      assert.ok(res.body.schema_version, 'should include schema_version');
      assert.match(res.body.proxy_protocol_version, /^\d+\.\d+\.\d+$/);
    });

    it('surfaces sync and auth diagnostics for local bridge clients', async () => {
      store.setState('last_sync_error', 'hub_401');
      store.setState('hub_auth_status', 'unauthorized');
      store.setState('reauth_backoff_until', '2026-06-15T12:00:00.000Z');
      store.setState('hello_rate_limit_until', '2026-06-15T12:01:00.000Z');

      const res = await authedReq(`${baseUrl}/proxy/status`, 'GET');
      assert.equal(res.status, 200);
      assert.equal(res.body.last_sync_error, 'hub_401');
      assert.equal(res.body.hub_auth_status, 'unauthorized');
      assert.equal(res.body.reauth_backoff_until, '2026-06-15T12:00:00.000Z');
      assert.equal(res.body.hello_rate_limit_until, '2026-06-15T12:01:00.000Z');
    });
  });

  describe('404 handling', () => {
    it('returns 404 for unknown routes', async () => {
      const res = await authedReq(`${baseUrl}/nonexistent`, 'GET');
      assert.equal(res.status, 404);
    });
  });

  describe('auth (C3)', () => {
    it('returns 401 with no token', async () => {
      const res = await request(`${baseUrl}/proxy/status`, 'GET');
      assert.equal(res.status, 401);
    });

    it('returns 401 with wrong token', async () => {
      const res = await request(`${baseUrl}/proxy/status`, 'GET', null, 'wrong-token');
      assert.equal(res.status, 401);
    });

    it('returns 200 with correct token', async () => {
      const res = await authedReq(`${baseUrl}/proxy/status`, 'GET');
      assert.equal(res.status, 200);
    });

    it('server.token accessor returns the same token written to settings', () => {
      assert.ok(server.token, 'server.token must be set after start()');
      assert.equal(typeof server.token, 'string');
      assert.equal(server.token.length, 64, 'token is 32 random bytes hex-encoded');
      assert.equal(server.token, serverToken);
    });
  });

  describe('body size cap (GHSA-7xp7-m392-h92c)', () => {
    // The proxy binds to 127.0.0.1 but any local process (other users on a
    // shared dev box, sibling containers sharing the netns, malicious
    // postinstall scripts) can still hit it. Without a cap, /mailbox/send and
    // /asset/submit would persist multi-GB payloads into messages.jsonl and
    // exhaust disk / OOM the daemon on every restart.
    it('rejects content-length headers above the default cap with 413', async () => {
      // 2 MiB body, default cap is 1 MiB.
      const big = 'x'.repeat(2 * 1024 * 1024);
      const res = await authedReq(`${baseUrl}/mailbox/send`, 'POST', {
        type: 'hub_event',
        payload: { blob: big },
      });
      assert.equal(res.status, 413, 'oversized body must 413');
      assert.ok(res.body && /too large/i.test(res.body.error || ''),
        'response should explain body too large');
    });

    it('rejects streaming bodies that exceed the cap even when Content-Length lies', async () => {
      // Chunked upload without declared Content-Length: the per-chunk counter
      // must still fire.
      const u = new URL(`${baseUrl}/mailbox/send`);
      const payload = JSON.stringify({ type: 'hub_event', payload: { blob: 'x'.repeat(2 * 1024 * 1024) } });
      const result = await new Promise((resolve, reject) => {
        const req = http.request({
          hostname: u.hostname,
          port: u.port,
          path: u.pathname,
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Transfer-Encoding': 'chunked',
            'Authorization': 'Bearer ' + serverToken,
          },
        }, (res) => {
          const chunks = [];
          res.on('data', c => chunks.push(c));
          res.on('end', () => {
            const raw = Buffer.concat(chunks).toString();
            try { resolve({ status: res.statusCode, body: JSON.parse(raw) }); }
            catch { resolve({ status: res.statusCode, body: raw }); }
          });
        });
        req.on('error', (e) => {
          // The server destroys the socket when the cap is hit. Map socket
          // hang-up into the expected reject-by-413 shape for this assertion.
          if (e.code === 'ECONNRESET' || e.code === 'EPIPE') return resolve({ status: 413, body: { error: 'aborted' } });
          reject(e);
        });
        req.write(payload);
        req.end();
      });
      assert.equal(result.status, 413, 'streaming oversized body must 413 or be aborted');
    });

    it('accepts bodies within the cap', async () => {
      const res = await authedReq(`${baseUrl}/mailbox/send`, 'POST', {
        type: 'hub_event',
        payload: { ok: true },
      });
      assert.ok(res.status === 200 || res.status === 201,
        'small bodies must still pass: got ' + res.status);
    });
  });
});

describe('EvoMapProxy._buildBundleFromLooseAsset', () => {
  const { EvoMapProxy } = require('../src/proxy');
  const build = (raw) => EvoMapProxy.prototype._buildBundleFromLooseAsset.call({}, raw);

  it('turns a loose MCP asset into a Hub-valid Gene+Capsule bundle', () => {
    const { gene, capsule } = build({
      type: 'Gene',
      content: 'A reusable approach long enough to clear the fifty character substance minimum the Hub enforces on assets.',
      signals: ['test_failure'],
    });
    assert.equal(gene.type, 'Gene');
    assert.ok(gene.strategy.length >= 2, 'gene strategy needs >=2 steps');
    assert.match(gene.validation[0], /^node |^npm |^npx /, 'validation must be node/npm/npx');
    assert.doesNotMatch(gene.validation[0], /process\.exit\(0\)/, 'validation must be a real assertion');
    assert.equal(capsule.gene, gene.id, 'capsule references the gene');
    assert.ok(Array.isArray(capsule.trigger), 'capsule trigger is an array');
    assert.ok(capsule.blast_radius.files >= 1 && capsule.blast_radius.lines >= 1);
    assert.ok(capsule.env_fingerprint.platform && capsule.env_fingerprint.arch);
    assert.ok(capsule.content.length >= 50, 'capsule needs >=50 chars of substance');
  });

  it('rejects an asset with no substantive content', () => {
    assert.throws(() => build({ type: 'Gene', summary: 'too short' }), /content|strategy/);
  });

  it('preserves caller-supplied strategy and category', () => {
    const { gene } = build({
      type: 'Gene', category: 'optimize',
      strategy: ['Step one that is long enough to count', 'Step two that is also long enough to count'],
      signals: ['perf_bottleneck'],
    });
    assert.equal(gene.category, 'optimize');
    assert.equal(gene.strategy.length, 2);
    assert.deepEqual(gene.signals_match, ['perf_bottleneck']);
  });

  it('rejects caller strategy whose steps are under 15 chars (Hub gate)', () => {
    assert.throws(() => build({ type: 'Gene', strategy: ['short', 'tiny'], signals: ['x'] }), /strategy.*15 chars/);
  });

  it('rejects when capsule content resolves below 50 chars', () => {
    // strategy passes (2 steps >=15 chars) but summary + steps still < 50 chars.
    assert.throws(
      () => build({ type: 'Gene', summary: 'hi', strategy: ['aaaaaaaaaaaaaaaa', 'bbbbbbbbbbbbbbbb'] }),
      /content resolves to <50|50 chars/,
    );
  });
});
