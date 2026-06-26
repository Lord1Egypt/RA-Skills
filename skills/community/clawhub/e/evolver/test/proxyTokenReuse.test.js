'use strict';

// Daemon restart used to mint a fresh `proxy.token` every time, which 401'd
// every long-lived shell that had already exported ANTHROPIC_AUTH_TOKEN from
// .bashrc auto-source. The fix in src/proxy/server/http.js reuses the token
// the previous owner wrote to settings.json, unless that owner is detected as
// dead (clearIfStale) — in which case we treat it as a fresh start and mint
// a new one.

const { describe, it, before, after, beforeEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');

const { MailboxStore } = require('../src/proxy/mailbox/store');
const { ProxyHttpServer } = require('../src/proxy/server/http');
const { buildRoutes } = require('../src/proxy/server/routes');
const { readSettings, writeSettings } = require('../src/proxy/server/settings');

function tmpDataDir() {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'proxy-tok-'));
}

function makeServer(port) {
  const store = new MailboxStore(tmpDataDir());
  const routes = buildRoutes(store, {
    assetFetch: async () => ({ assets: [] }),
    assetSearch: async () => ({ results: [] }),
    assetValidate: async () => ({ valid: true }),
  }, null, {});
  const server = new ProxyHttpServer(routes, {
    port,
    logger: { log: () => {}, error: () => {}, warn: () => {} },
  });
  return { server, store };
}

describe('ProxyHttpServer token reuse', () => {
  let savedSettingsDir;
  let settingsDir;

  before(() => {
    settingsDir = fs.mkdtempSync(path.join(os.tmpdir(), 'proxy-tok-settings-'));
    savedSettingsDir = process.env.EVOLVER_SETTINGS_DIR;
    process.env.EVOLVER_SETTINGS_DIR = settingsDir;
  });

  after(() => {
    try { fs.rmSync(settingsDir, { recursive: true }); } catch {}
    if (savedSettingsDir === undefined) delete process.env.EVOLVER_SETTINGS_DIR;
    else process.env.EVOLVER_SETTINGS_DIR = savedSettingsDir;
  });

  beforeEach(() => {
    // Wipe settings between tests so each one controls the precondition.
    try { fs.rmSync(path.join(settingsDir, 'settings.json')); } catch {}
  });

  it('reuses token from a stale-but-still-on-disk settings file', async () => {
    // Simulate the real-world case: a previous daemon wrote settings.json,
    // then died, leaving a dead PID + a token that long-lived shells already
    // exported. clearIfStale will wipe the proxy block; the new daemon must
    // still pick up the prior token before the wipe.
    const ghostPid = 999999;  // a pid that almost certainly does not exist
    try { process.kill(ghostPid, 0); throw new Error('test pid is alive'); } catch (e) {
      if (e.code !== 'ESRCH') {
        // Skip if the pid happens to exist on this box — the test premise
        // requires a dead pid to exercise the stale branch.
        return;
      }
    }
    writeSettings({
      proxy: {
        url: 'http://127.0.0.1:39830',
        pid: ghostPid,
        started_at: new Date().toISOString(),
        token: 'a'.repeat(64),
      },
    });

    const { server, store } = makeServer(39830);
    const info = await server.start();
    try {
      assert.equal(info.token, 'a'.repeat(64), 'must reuse prior token across restart');
      assert.equal(readSettings().proxy.token, 'a'.repeat(64));
    } finally {
      await server.stop();
      store.close();
    }
  });

  it('mints a new token when settings.json has no proxy block', async () => {
    const { server, store } = makeServer(39831);
    const info = await server.start();
    try {
      assert.equal(typeof info.token, 'string');
      assert.equal(info.token.length, 64, 'fresh token is 32 random bytes hex-encoded');
      assert.notEqual(info.token, 'a'.repeat(64));
    } finally {
      await server.stop();
      store.close();
    }
  });

  it('preserves previous_tokens across restart (writeSettings overwrite guard)', async () => {
    // Without explicit preservation, start()'s writeSettings({proxy:{...}})
    // would shallow-merge and drop previous_tokens — this guards against
    // grace tokens silently disappearing on every daemon restart.
    const lostToken = 'e'.repeat(64);
    writeSettings({
      proxy: {
        url: 'http://127.0.0.1:39836',
        pid: 999998,
        started_at: new Date().toISOString(),
        token: 'f'.repeat(64),
        previous_tokens: [lostToken],
      },
    });

    const { server, store } = makeServer(39836);
    await server.start();
    try {
      assert.deepEqual(
        readSettings().proxy.previous_tokens,
        [lostToken],
        'previous_tokens must survive daemon restart',
      );
    } finally {
      await server.stop();
      store.close();
    }
  });

  it('accepts grace tokens listed in settings.previous_tokens', async () => {
    // Recovery path: settings.json was wiped externally (logout / manual rm)
    // while a long-lived CC session still holds the pre-wipe token in its
    // fork-time env. Operator pastes that lost token into previous_tokens so
    // the session keeps working until it dies naturally.
    const lostToken = 'b'.repeat(64);
    const { server, store } = makeServer(39834);
    const info = await server.start();
    try {
      writeSettings({
        proxy: {
          ...readSettings().proxy,
          previous_tokens: [lostToken],
        },
      });

      const port = info.port;
      const baseHeaders = { 'Content-Type': 'application/json' };

      const ok1 = await fetch(`http://127.0.0.1:${port}/proxy/status`, {
        headers: { ...baseHeaders, 'Authorization': `Bearer ${info.token}` },
      });
      assert.equal(ok1.status, 200, 'primary token still accepted');

      const ok2 = await fetch(`http://127.0.0.1:${port}/proxy/status`, {
        headers: { ...baseHeaders, 'Authorization': `Bearer ${lostToken}` },
      });
      assert.equal(ok2.status, 200, 'previous_tokens entry accepted');

      const bad = await fetch(`http://127.0.0.1:${port}/proxy/status`, {
        headers: { ...baseHeaders, 'Authorization': `Bearer ${'c'.repeat(64)}` },
      });
      assert.equal(bad.status, 401, 'unrelated token still rejected');
    } finally {
      await server.stop();
      store.close();
    }
  });

  it('non-string entries in previous_tokens are dropped (do not crash auth)', async () => {
    // settings.json is operator-edited. If someone pastes a malformed entry
    // (number, bool, null, object) into previous_tokens, Buffer.from would
    // throw ERR_INVALID_ARG_TYPE inside the auth loop and unhandled-reject
    // the daemon down. This guards both the persistence path (start) and
    // the read path (_handleRequest).
    const goodGrace = 'g'.repeat(64);
    const { server, store } = makeServer(39837);
    const info = await server.start();
    try {
      writeSettings({
        proxy: {
          ...readSettings().proxy,
          previous_tokens: [goodGrace, 12345, null, { token: 'x' }, '', false],
        },
      });

      const port = info.port;
      const auth = (tok) => fetch(`http://127.0.0.1:${port}/proxy/status`, {
        headers: { 'Authorization': `Bearer ${tok}` },
      });

      const ok = await auth(goodGrace);
      assert.equal(ok.status, 200, 'string grace token still accepted');

      const bad = await auth('h'.repeat(64));
      assert.equal(bad.status, 401, 'unrelated token rejected without crashing');

      const primary = await auth(info.token);
      assert.equal(primary.status, 200, 'daemon survived malformed entries');
    } finally {
      await server.stop();
      store.close();
    }
  });

  it('start() filters non-strings before persisting previous_tokens', async () => {
    // If start() persists garbage from a hand-edited settings.json, the next
    // restart loads it back and we're back to the same crash risk. start()
    // must scrub the list as it writes.
    writeSettings({
      proxy: {
        url: 'http://127.0.0.1:39838',
        pid: 999997,
        started_at: new Date().toISOString(),
        token: 'i'.repeat(64),
        previous_tokens: ['j'.repeat(64), 42, null, false, '', { x: 1 }],
      },
    });

    const { server, store } = makeServer(39838);
    await server.start();
    try {
      const persisted = readSettings().proxy.previous_tokens;
      assert.deepEqual(persisted, ['j'.repeat(64)],
        'only the string entry survives the round-trip');
    } finally {
      await server.stop();
      store.close();
    }
  });

  it('clean stop wipes previous_tokens along with proxy block', async () => {
    // Guard against grace tokens leaking past a clean shutdown — clearSettings
    // drops the whole proxy block, which includes previous_tokens by design.
    const first = makeServer(39835);
    const firstInfo = await first.server.start();
    writeSettings({
      proxy: {
        ...readSettings().proxy,
        previous_tokens: ['d'.repeat(64)],
      },
    });
    await first.server.stop();
    first.store.close();

    assert.equal(readSettings().proxy, undefined, 'clean stop drops proxy block');
  });

  it('mints a new token after a clean shutdown', async () => {
    // server.stop() calls clearSettings() so the proxy block is gone;
    // the next start has nothing to reuse and must mint a fresh token.
    // This guards against accidentally persisting tokens past a clean stop.
    const first = makeServer(39832);
    const firstInfo = await first.server.start();
    const firstToken = firstInfo.token;
    await first.server.stop();
    first.store.close();

    const second = makeServer(39833);
    const secondInfo = await second.server.start();
    try {
      assert.equal(typeof secondInfo.token, 'string');
      assert.equal(secondInfo.token.length, 64);
      assert.notEqual(secondInfo.token, firstToken, 'clean stop must not leak token');
    } finally {
      await second.server.stop();
      second.store.close();
    }
  });
});
