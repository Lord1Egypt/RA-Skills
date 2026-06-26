'use strict';

const { describe, it, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const repoRoot = path.resolve(__dirname, '..');

function read(rel) {
  return fs.readFileSync(path.join(repoRoot, rel), 'utf8');
}

async function withEnv(overrides, fn) {
  const orig = {};
  for (const k of Object.keys(overrides)) {
    orig[k] = process.env[k];
    if (overrides[k] === undefined) delete process.env[k];
    else process.env[k] = overrides[k];
  }
  try { return await fn(); }
  finally {
    for (const k of Object.keys(orig)) {
      if (orig[k] === undefined) delete process.env[k];
      else process.env[k] = orig[k];
    }
  }
}

function assertStrictDispatcher(opts) {
  assert.ok(opts && opts.dispatcher, 'hubFetch must attach a dispatcher in secure mode');
  const sym = Object.getOwnPropertySymbols(opts.dispatcher)
    .find((s) => s.toString() === 'Symbol(options)');
  const agentOpts = opts.dispatcher[sym];
  assert.equal(agentOpts && agentOpts.connect && agentOpts.connect.rejectUnauthorized, true,
    'dispatcher must pin connect.rejectUnauthorized=true');
}

function okResponse(body) {
  return {
    ok: true,
    status: 200,
    json: async () => body,
    text: async () => JSON.stringify(body),
  };
}

afterEach(() => {
  try { require('../src/gep/hubFetch')._setFetchImplForTest(null); } catch (_) {}
  for (const rel of [
    '../src/gep/a2aProtocol',
    '../src/atp/serviceHelper',
    '../src/gep/privacyClient',
    '../src/config',
  ]) {
    try { delete require.cache[require.resolve(rel)]; } catch (_) {}
  }
});

describe('Hub egress chokepoint coverage', () => {
  it('keeps reviewed Hub clients off bare fetch/native request paths', () => {
    const forbiddenFetch = /\bfetch\s*\(/;
    for (const rel of [
      'src/atp/serviceHelper.js',
      'src/gep/privacyClient.js',
      'src/gep/oauthLogin.js',
    ]) {
      const src = read(rel);
      assert.match(src, /hubFetch/, rel + ' must import/use hubFetch');
      assert.ok(!forbiddenFetch.test(src), rel + ' must not call bare fetch');
    }

    const atpExecute = read('src/atp/atpExecute.js');
    assert.match(atpExecute, /hubFetch/, 'atpExecute must publish/complete through hubFetch');
    assert.ok(!/\bhttps?\.request\s*\(/.test(atpExecute), 'atpExecute must not open native Hub sockets');

    const sessionEnd = read('src/adapters/scripts/evolver-session-end.js');
    assert.match(sessionEnd, /hubFetch/, 'session-end Hub recording must use hubFetch');
    assert.ok(!/require\(['"]https?['"]\)/.test(sessionEnd), 'session-end must not require native http/https');
    assert.ok(!/\bhttps?\.request\s*\(/.test(sessionEnd), 'session-end must not open native Hub sockets');

    const rootIndex = read('index.js');
    const fetchBranch = rootIndex.slice(
      rootIndex.indexOf("command === 'fetch'"),
      rootIndex.indexOf("command === 'sync'"),
    );
    assert.match(fetchBranch, /hubFetch/, 'evolver fetch must route Hub download through hubFetch');
    assert.ok(!/\bawait\s+fetch\s*\(/.test(fetchBranch), 'evolver fetch must not call bare fetch for Hub download');

    const syncBranch = rootIndex.slice(
      rootIndex.indexOf("command === 'sync'"),
      rootIndex.indexOf("command === 'asset-log'"),
    );
    assert.match(syncBranch, /hubFetch/, 'evolver sync must route Hub reads through hubFetch');
    assert.ok(!/\bawait\s+fetch\s*\(/.test(syncBranch), 'evolver sync must not call bare fetch for Hub reads');
  });

  it('serviceHelper publishService reaches Hub through hubFetch dispatcher', async () => {
    await withEnv({ EVOMAP_HUB_ALLOW_INSECURE: undefined }, async () => {
      const hubFetchMod = require('../src/gep/hubFetch');
      let captured = null;
      hubFetchMod._setFetchImplForTest(async (url, opts) => {
        captured = { url, opts };
        return okResponse({ listing_id: 'svc_1' });
      });

      const a2aPath = require.resolve('../src/gep/a2aProtocol');
      require.cache[a2aPath] = {
        id: a2aPath,
        filename: a2aPath,
        loaded: true,
        exports: {
          getNodeId: () => 'node_test',
          getHubUrl: () => 'https://hub.example',
          buildHubHeaders: () => ({ Authorization: 'Bearer test' }),
        },
      };
      delete require.cache[require.resolve('../src/atp/serviceHelper')];

      const { publishService } = require('../src/atp/serviceHelper');
      const res = await publishService({ title: 'Demo service', capabilities: ['x'] });

      assert.equal(res.ok, true);
      assert.equal(captured.url, 'https://hub.example/a2a/service/publish');
      assertStrictDispatcher(captured.opts);
    });
  });

  it('privacyClient submitPrivacyTask reaches Hub through hubFetch dispatcher', async () => {
    await withEnv({
      EVOMAP_HUB_ALLOW_INSECURE: undefined,
      A2A_HUB_URL: 'https://hub.example',
      EVOMAP_HUB_URL: undefined,
    }, async () => {
      const hubFetchMod = require('../src/gep/hubFetch');
      let captured = null;
      hubFetchMod._setFetchImplForTest(async (url, opts) => {
        captured = { url, opts };
        return okResponse({ taskId: 'privacy_1', status: 'queued' });
      });

      const a2aPath = require.resolve('../src/gep/a2aProtocol');
      require.cache[a2aPath] = {
        id: a2aPath,
        filename: a2aPath,
        loaded: true,
        exports: {
          getNodeId: () => 'node_test',
          buildHubHeaders: () => ({ Authorization: 'Bearer test' }),
        },
      };
      delete require.cache[require.resolve('../src/config')];
      delete require.cache[require.resolve('../src/gep/privacyClient')];

      const { submitPrivacyTask } = require('../src/gep/privacyClient');
      const res = await submitPrivacyTask({ title: 'Private task' });

      assert.deepEqual(res, { taskId: 'privacy_1', status: 'queued' });
      assert.equal(captured.url, 'https://hub.example/a2a/privacy/submit');
      assertStrictDispatcher(captured.opts);
    });
  });
});
