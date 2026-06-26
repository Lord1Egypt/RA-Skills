'use strict';

const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const http = require('http');
const fs = require('fs');
const os = require('os');
const path = require('path');

const { EvoMapProxy } = require('../src/proxy');

function tmpDir() {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'proxy-trace-integration-'));
}

function postJson(url, token, body) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const payload = JSON.stringify(body || {});
    const req = http.request({
      hostname: u.hostname,
      port: u.port,
      path: u.pathname,
      method: 'POST',
      headers: {
        Authorization: 'Bearer ' + token,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload),
        'x-api-key': 'sk-test',
      },
    }, (res) => {
      const chunks = [];
      res.on('data', (c) => chunks.push(c));
      res.on('end', () => resolve({
        status: res.statusCode,
        body: Buffer.concat(chunks).toString(),
      }));
    });
    req.on('error', reject);
    req.write(payload);
    req.end();
  });
}

function readJsonl(file) {
  return fs.readFileSync(file, 'utf8').trim().split('\n').map((line) => JSON.parse(line));
}

async function waitFor(fn) {
  const deadline = Date.now() + 1000;
  while (Date.now() < deadline) {
    if (fn()) return true;
    await new Promise((resolve) => setTimeout(resolve, 10));
  }
  return fn();
}

function encryptedTrace(ciphertext) {
  return {
    encrypted: true,
    algorithm: 'aes-256-gcm',
    payload_schema: 'prism_trace_row',
    iv: 'aXYxMjM0NTY3ODkw',
    tag: 'dGFnMTIzNDU2Nzg5MA==',
    ciphertext,
  };
}

describe('EvoMapProxy proxy trace integration', () => {
  let dir;
  let proxy;
  let savedSettingsDir;
  let savedEvolverHome;
  let savedTrace;
  let savedTraceFile;
  let savedTraceEncryption;
  let savedMaxPendingUploads;
  let savedBackfillMaxRows;
  let savedNodeSecret;
  let savedAnthropicKey;
  let savedA2aHubUrl;
  let savedEvomapHubUrl;
  let savedDefaultHubUrl;
  let savedHubAllowInsecure;

  beforeEach(() => {
    dir = tmpDir();
    savedSettingsDir = process.env.EVOLVER_SETTINGS_DIR;
    savedEvolverHome = process.env.EVOLVER_HOME;
    savedTrace = process.env.EVOMAP_PROXY_TRACE;
    savedTraceFile = process.env.EVOMAP_PROXY_TRACE_FILE;
    savedTraceEncryption = process.env.EVOMAP_PROXY_TRACE_ENCRYPTION;
    savedMaxPendingUploads = process.env.EVOMAP_PROXY_TRACE_MAX_PENDING_UPLOADS;
    savedBackfillMaxRows = process.env.EVOMAP_PROXY_TRACE_BACKFILL_MAX_ROWS;
    savedNodeSecret = process.env.A2A_NODE_SECRET;
    savedAnthropicKey = process.env.ANTHROPIC_API_KEY;
    savedA2aHubUrl = process.env.A2A_HUB_URL;
    savedEvomapHubUrl = process.env.EVOMAP_HUB_URL;
    savedDefaultHubUrl = process.env.EVOLVER_DEFAULT_HUB_URL;
    savedHubAllowInsecure = process.env.EVOMAP_HUB_ALLOW_INSECURE;
    process.env.EVOLVER_SETTINGS_DIR = path.join(dir, 'settings');
    process.env.EVOLVER_HOME = path.join(dir, 'evomap');
    process.env.EVOMAP_PROXY_TRACE = 'full';
    process.env.EVOMAP_PROXY_TRACE_FILE = path.join(dir, 'proxy-traces.jsonl');
    process.env.EVOMAP_PROXY_TRACE_ENCRYPTION = '1';
    process.env.A2A_NODE_SECRET = 'c'.repeat(64);
    delete process.env.ANTHROPIC_API_KEY;
    delete process.env.A2A_HUB_URL;
    delete process.env.EVOMAP_HUB_URL;
    delete process.env.EVOLVER_DEFAULT_HUB_URL;
    delete process.env.EVOMAP_HUB_ALLOW_INSECURE;
  });

  afterEach(async () => {
    if (proxy) {
      try { await proxy.stop(); } catch {}
      proxy = null;
    }
    try { fs.rmSync(dir, { recursive: true }); } catch {}
    if (savedSettingsDir === undefined) delete process.env.EVOLVER_SETTINGS_DIR;
    else process.env.EVOLVER_SETTINGS_DIR = savedSettingsDir;
    if (savedEvolverHome === undefined) delete process.env.EVOLVER_HOME;
    else process.env.EVOLVER_HOME = savedEvolverHome;
    if (savedTrace === undefined) delete process.env.EVOMAP_PROXY_TRACE;
    else process.env.EVOMAP_PROXY_TRACE = savedTrace;
    if (savedTraceFile === undefined) delete process.env.EVOMAP_PROXY_TRACE_FILE;
    else process.env.EVOMAP_PROXY_TRACE_FILE = savedTraceFile;
    if (savedTraceEncryption === undefined) delete process.env.EVOMAP_PROXY_TRACE_ENCRYPTION;
    else process.env.EVOMAP_PROXY_TRACE_ENCRYPTION = savedTraceEncryption;
    if (savedMaxPendingUploads === undefined) delete process.env.EVOMAP_PROXY_TRACE_MAX_PENDING_UPLOADS;
    else process.env.EVOMAP_PROXY_TRACE_MAX_PENDING_UPLOADS = savedMaxPendingUploads;
    if (savedBackfillMaxRows === undefined) delete process.env.EVOMAP_PROXY_TRACE_BACKFILL_MAX_ROWS;
    else process.env.EVOMAP_PROXY_TRACE_BACKFILL_MAX_ROWS = savedBackfillMaxRows;
    if (savedNodeSecret === undefined) delete process.env.A2A_NODE_SECRET;
    else process.env.A2A_NODE_SECRET = savedNodeSecret;
    if (savedAnthropicKey === undefined) delete process.env.ANTHROPIC_API_KEY;
    else process.env.ANTHROPIC_API_KEY = savedAnthropicKey;
    if (savedA2aHubUrl === undefined) delete process.env.A2A_HUB_URL;
    else process.env.A2A_HUB_URL = savedA2aHubUrl;
    if (savedEvomapHubUrl === undefined) delete process.env.EVOMAP_HUB_URL;
    else process.env.EVOMAP_HUB_URL = savedEvomapHubUrl;
    if (savedDefaultHubUrl === undefined) delete process.env.EVOLVER_DEFAULT_HUB_URL;
    else process.env.EVOLVER_DEFAULT_HUB_URL = savedDefaultHubUrl;
    if (savedHubAllowInsecure === undefined) delete process.env.EVOMAP_HUB_ALLOW_INSECURE;
    else process.env.EVOMAP_HUB_ALLOW_INSECURE = savedHubAllowInsecure;
  });

  it('captures /v1/messages into local trace file and outbound proxy_trace mailbox', async () => {
    proxy = new EvoMapProxy({
      dataDir: path.join(dir, 'mailbox'),
      port: 39920,
      logger: { log: () => {}, warn: () => {}, error: () => {} },
    });
    proxy.hubUrl = '';
    proxy._proxyAnthropic = async () => ({
      status: 200,
      headers: { 'content-type': 'application/json' },
      stream: null,
      text: () => JSON.stringify({ id: 'msg_integration', usage: { input_tokens: 3, output_tokens: 4 } }),
    });

    const info = await proxy.start();
    let notifyCount = 0;
    proxy.sync.notifyNewOutbound = () => { notifyCount++; };

    const res = await postJson(`${info.url}/v1/messages`, proxy.server.token, {
      model: 'claude-test',
      messages: [{ role: 'user', content: 'integration trace upload' }],
    });

    assert.equal(res.status, 200);
    assert.equal(await waitFor(() => notifyCount === 1), true);
    let pending = [];
    assert.equal(await waitFor(() => {
      pending = proxy.store.list({
        type: 'proxy_trace',
        direction: 'outbound',
        status: 'pending',
        limit: 10,
      });
      return pending.length === 1;
    }), true);
    assert.equal(pending.length, 1);
    assert.equal(pending[0].payload.schema, 'prism_trace_row.v1');
    assert.equal(pending[0].payload.encrypted, true);
    assert.equal(pending[0].payload.trace.encrypted, true);
    assert.equal(notifyCount, 1);
    assert.equal(await waitFor(() => fs.existsSync(process.env.EVOMAP_PROXY_TRACE_FILE)
      && fs.readFileSync(process.env.EVOMAP_PROXY_TRACE_FILE, 'utf8').trim()), true);
    const [localTrace] = readJsonl(process.env.EVOMAP_PROXY_TRACE_FILE);
    assert.equal(localTrace.encrypted, true);
  });

  it('queues existing local trace rows on proxy startup', async () => {
    fs.writeFileSync(process.env.EVOMAP_PROXY_TRACE_FILE, JSON.stringify(encryptedTrace('c3RhcnR1cC1iYWNrZmlsbA==')) + '\n', 'utf8');
    proxy = new EvoMapProxy({
      dataDir: path.join(dir, 'mailbox-startup-backfill'),
      port: 39921,
      logger: { log: () => {}, warn: () => {}, error: () => {} },
    });
    proxy.hubUrl = '';

    await proxy.start();

    const pending = proxy.store.list({
      type: 'proxy_trace',
      direction: 'outbound',
      status: 'pending',
      limit: 10,
    });
    assert.equal(pending.length, 1);
    assert.equal(pending[0].payload.schema, 'prism_trace_row.v1');
    assert.equal(pending[0].payload.trace.ciphertext, 'c3RhcnR1cC1iYWNrZmlsbA==');
    assert.ok(String(pending[0].ref_id || '').startsWith('proxy_trace:'));
  });

  it('queues remaining startup trace rows after outbound capacity frees', async () => {
    process.env.EVOMAP_PROXY_TRACE_MAX_PENDING_UPLOADS = '100';
    process.env.EVOMAP_PROXY_TRACE_BACKFILL_MAX_ROWS = '100';
    const traces = Array.from({ length: 101 }, (_, i) => encryptedTrace(Buffer.from(`startup-drain-${i}`).toString('base64')));
    fs.writeFileSync(process.env.EVOMAP_PROXY_TRACE_FILE, traces.map((row) => JSON.stringify(row)).join('\n') + '\n', 'utf8');
    proxy = new EvoMapProxy({
      dataDir: path.join(dir, 'mailbox-startup-drain'),
      port: 39922,
      logger: { log: () => {}, warn: () => {}, error: () => {} },
    });
    proxy.hubUrl = '';

    await proxy.start();

    let pending = proxy.store.list({
      type: 'proxy_trace',
      direction: 'outbound',
      status: 'pending',
      limit: 100,
    });
    assert.equal(pending.length, 100);
    assert.equal(pending.some((row) => row.payload.trace.ciphertext === traces[100].ciphertext), false);

    for (const row of pending) proxy.store.updateStatus(row.id, 'synced');
    proxy.sync.onOutboundFlushed({ sent: 100 });

    pending = proxy.store.list({
      type: 'proxy_trace',
      direction: 'outbound',
      status: 'pending',
      limit: 100,
    });
    assert.equal(pending.length, 1);
    assert.equal(pending[0].payload.trace.ciphertext, traces[100].ciphertext);
  });
});
