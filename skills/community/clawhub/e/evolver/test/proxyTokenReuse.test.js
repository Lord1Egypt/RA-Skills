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

const RUNTIME_ENV_KEYS = [
  'ANTHROPIC_BASE_URL',
  'ANTHROPIC_AUTH_TOKEN',
  'EVOMAP_ANTHROPIC_BASE_URL',
  'EVOMAP_ANTHROPIC_AUTH_TOKEN',
  'EVOMAP_ANTHROPIC_API_KEY',
  'EVOMAP_PROXY_AUTO_INJECT',
  'EVOMAP_PROXY_AUTO_INJECTED',
];

function fakeHexToken(seed) {
  return seed.repeat(64).slice(0, 64);
}

function tmpDataDir() {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'proxy-tok-'));
}

function makeServer(port, opts = {}) {
  const store = new MailboxStore(tmpDataDir());
  const routes = buildRoutes(store, {
    assetFetch: async () => ({ assets: [] }),
    assetSearch: async () => ({ results: [] }),
    assetValidate: async () => ({ valid: true }),
  }, null, {});
  const server = new ProxyHttpServer(routes, {
    port,
    logger: { log: () => {}, error: () => {}, warn: () => {} },
    clientSettings: opts.clientSettings,
  });
  return { server, store };
}

describe('ProxyHttpServer token reuse', () => {
  let savedSettingsDir;
  let savedClaudeSettingsFile;
  let savedEvomapClaudeSettingsFile;
  let savedHome;
  let settingsDir;
  let claudeSettingsFile;
  let savedRuntimeEnv;

  before(() => {
    settingsDir = fs.mkdtempSync(path.join(os.tmpdir(), 'proxy-tok-settings-'));
    claudeSettingsFile = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'proxy-tok-claude-')), 'settings.json');
    savedSettingsDir = process.env.EVOLVER_SETTINGS_DIR;
    savedClaudeSettingsFile = process.env.CLAUDE_SETTINGS_FILE;
    savedEvomapClaudeSettingsFile = process.env.EVOMAP_CLAUDE_SETTINGS_FILE;
    savedHome = process.env.HOME;
    savedRuntimeEnv = Object.fromEntries(RUNTIME_ENV_KEYS.map((key) => [key, process.env[key]]));
    process.env.EVOLVER_SETTINGS_DIR = settingsDir;
    process.env.CLAUDE_SETTINGS_FILE = claudeSettingsFile;
  });

  after(() => {
    try { fs.rmSync(settingsDir, { recursive: true }); } catch {}
    try { fs.rmSync(path.dirname(claudeSettingsFile), { recursive: true }); } catch {}
    if (savedSettingsDir === undefined) delete process.env.EVOLVER_SETTINGS_DIR;
    else process.env.EVOLVER_SETTINGS_DIR = savedSettingsDir;
    if (savedClaudeSettingsFile === undefined) delete process.env.CLAUDE_SETTINGS_FILE;
    else process.env.CLAUDE_SETTINGS_FILE = savedClaudeSettingsFile;
    if (savedEvomapClaudeSettingsFile === undefined) delete process.env.EVOMAP_CLAUDE_SETTINGS_FILE;
    else process.env.EVOMAP_CLAUDE_SETTINGS_FILE = savedEvomapClaudeSettingsFile;
    if (savedHome === undefined) delete process.env.HOME;
    else process.env.HOME = savedHome;
    for (const key of RUNTIME_ENV_KEYS) {
      if (savedRuntimeEnv[key] === undefined) delete process.env[key];
      else process.env[key] = savedRuntimeEnv[key];
    }
  });

  beforeEach(() => {
    // Wipe settings between tests so each one controls the precondition.
    try { fs.rmSync(path.join(settingsDir, 'settings.json')); } catch {}
    try { fs.rmSync(claudeSettingsFile); } catch {}
    try { fs.rmSync(path.join(path.dirname(claudeSettingsFile), 'backups'), { recursive: true }); } catch {}
    for (const key of RUNTIME_ENV_KEYS) delete process.env[key];
    process.env.CLAUDE_SETTINGS_FILE = claudeSettingsFile;
    delete process.env.EVOMAP_CLAUDE_SETTINGS_FILE;
    if (savedHome === undefined) delete process.env.HOME;
    else process.env.HOME = savedHome;
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

  it('recovers token from Claude client settings when proxy settings were wiped', async () => {
    const oldToken = fakeHexToken('1a');
    fs.mkdirSync(path.dirname(claudeSettingsFile), { recursive: true });
    fs.writeFileSync(claudeSettingsFile, JSON.stringify({
      env: {
        ANTHROPIC_BASE_URL: 'http://127.0.0.1:39839',
        ANTHROPIC_AUTH_TOKEN: oldToken,
        EVOMAP_ANTHROPIC_BASE_URL: 'https://sub2api-api.evomap.work',
        EVOMAP_ANTHROPIC_AUTH_TOKEN: 'upstream-token',
      },
      _evomap_proxy_client_env: { managed_by: 'evomap-proxy' },
    }, null, 2), 'utf8');

    const { server, store } = makeServer(39839, { clientSettings: { file: claudeSettingsFile } });
    const info = await server.start();
    try {
      assert.equal(info.token, oldToken, 'client-held local proxy token must survive proxy settings loss');
      assert.equal(readSettings().proxy.token, oldToken);
      const clientSettings = JSON.parse(fs.readFileSync(claudeSettingsFile, 'utf8'));
      assert.equal(clientSettings.env.ANTHROPIC_BASE_URL, 'http://127.0.0.1:39839');
      assert.equal(clientSettings.env.ANTHROPIC_AUTH_TOKEN, oldToken);
      assert.equal(clientSettings.env.EVOMAP_ANTHROPIC_BASE_URL, 'https://sub2api-api.evomap.work');
      assert.equal(clientSettings.env.EVOMAP_ANTHROPIC_AUTH_TOKEN, 'upstream-token');
      assert.equal(clientSettings._evomap_proxy_client_env.managed_by, 'evomap-proxy');
    } finally {
      await server.stop();
      store.close();
    }
  });

  it('does not reuse or write proxy token when CLAUDE_SETTINGS_FILE points inside a workspace', async () => {
    const workspace = fs.mkdtempSync(path.join(os.tmpdir(), 'proxy-tok-workspace-'));
    const unsafeSettingsFile = path.join(workspace, '.claude', 'settings.json');
    const plantedToken = fakeHexToken('12');
    process.env.CLAUDE_SETTINGS_FILE = unsafeSettingsFile;
    fs.mkdirSync(path.dirname(unsafeSettingsFile), { recursive: true });
    fs.writeFileSync(unsafeSettingsFile, JSON.stringify({
      env: {
        ANTHROPIC_BASE_URL: 'http://127.0.0.1:39847',
        ANTHROPIC_AUTH_TOKEN: plantedToken,
        EVOMAP_PROXY_URL: 'http://127.0.0.1:39847',
      },
      _evomap_proxy_client_env: { managed_by: 'evomap-proxy' },
    }, null, 2), 'utf8');

    const before = fs.readFileSync(unsafeSettingsFile, 'utf8');
    const { server, store } = makeServer(39847, { clientSettings: true });
    const info = await server.start();
    try {
      assert.equal(typeof info.token, 'string');
      assert.equal(info.token.length, 64);
      assert.notEqual(info.token, plantedToken, 'env-controlled workspace token must not be reused');
      assert.equal(fs.readFileSync(unsafeSettingsFile, 'utf8'), before, 'env-controlled workspace file must not be rewritten');
      assert.equal(readSettings().proxy.token, info.token);
    } finally {
      await server.stop();
      store.close();
      try { fs.rmSync(workspace, { recursive: true }); } catch {}
    }
  });

  it('syncs default Claude client settings under HOME when env path override is absent', async () => {
    const home = fs.mkdtempSync(path.join(os.tmpdir(), 'proxy-tok-home-'));
    delete process.env.CLAUDE_SETTINGS_FILE;
    delete process.env.EVOMAP_CLAUDE_SETTINGS_FILE;
    process.env.HOME = home;
    const defaultSettingsFile = path.join(home, '.claude', 'settings.json');

    const { server, store } = makeServer(39848, { clientSettings: true });
    const info = await server.start();
    try {
      const clientSettings = JSON.parse(fs.readFileSync(defaultSettingsFile, 'utf8'));
      assert.equal(clientSettings.env.ANTHROPIC_BASE_URL, info.url);
      assert.equal(clientSettings.env.ANTHROPIC_AUTH_TOKEN, info.token);
      assert.equal(clientSettings.env.CUSTOM_API_KEY, info.token);
      assert.equal(clientSettings.env.EVOMAP_PROXY_URL, info.url);
      assert.equal(clientSettings._evomap_proxy_client_env.managed_by, 'evomap-proxy');
    } finally {
      await server.stop();
      store.close();
      try { fs.rmSync(home, { recursive: true }); } catch {}
    }
  });

  it('does not recover token from unmarked loopback Claude client settings', async () => {
    const oldToken = fakeHexToken('2b');
    fs.mkdirSync(path.dirname(claudeSettingsFile), { recursive: true });
    fs.writeFileSync(claudeSettingsFile, JSON.stringify({
      env: {
        ANTHROPIC_BASE_URL: 'http://127.0.0.1:39843',
        ANTHROPIC_AUTH_TOKEN: oldToken,
      },
    }, null, 2), 'utf8');

    const { server, store } = makeServer(39843, { clientSettings: { file: claudeSettingsFile } });
    const info = await server.start();
    try {
      assert.equal(typeof info.token, 'string');
      assert.equal(info.token.length, 64);
      assert.notEqual(info.token, oldToken, 'bare loopback client token must not be promoted');
      assert.equal(readSettings().proxy.token, info.token);
    } finally {
      await server.stop();
      store.close();
    }
  });

  it('recovers token from auto-injected loopback Claude client settings', async () => {
    const oldToken = fakeHexToken('3c');
    fs.mkdirSync(path.dirname(claudeSettingsFile), { recursive: true });
    fs.writeFileSync(claudeSettingsFile, JSON.stringify({
      env: {
        ANTHROPIC_BASE_URL: 'http://127.0.0.1:39844',
        ANTHROPIC_AUTH_TOKEN: oldToken,
        EVOMAP_PROXY_AUTO_INJECTED: '1',
      },
    }, null, 2), 'utf8');

    const { server, store } = makeServer(39844, { clientSettings: { file: claudeSettingsFile } });
    const info = await server.start();
    try {
      assert.equal(info.token, oldToken, 'auto-injected loopback client token should be reused');
      assert.equal(readSettings().proxy.token, oldToken);
    } finally {
      await server.stop();
      store.close();
    }
  });

  it('recovers token from Claude client settings with EVOMAP_PROXY_URL loopback', async () => {
    const oldToken = fakeHexToken('4d');
    fs.mkdirSync(path.dirname(claudeSettingsFile), { recursive: true });
    fs.writeFileSync(claudeSettingsFile, JSON.stringify({
      env: {
        ANTHROPIC_BASE_URL: 'http://127.0.0.1:39845',
        ANTHROPIC_AUTH_TOKEN: oldToken,
        EVOMAP_PROXY_URL: 'http://127.0.0.1:39845',
      },
    }, null, 2), 'utf8');

    const { server, store } = makeServer(39845, { clientSettings: { file: claudeSettingsFile } });
    const info = await server.start();
    try {
      assert.equal(info.token, oldToken, 'EVOMAP_PROXY_URL loopback client token should be reused');
      assert.equal(readSettings().proxy.token, oldToken);
    } finally {
      await server.stop();
      store.close();
    }
  });

  it('syncs Claude client settings to the active proxy and preserves upstream credentials', async () => {
    fs.mkdirSync(path.dirname(claudeSettingsFile), { recursive: true });
    fs.writeFileSync(claudeSettingsFile, JSON.stringify({
      env: {
        ANTHROPIC_BASE_URL: 'https://sub2api-api.evomap.work',
        ANTHROPIC_AUTH_TOKEN: 'upstream-token',
        ANTHROPIC_API_KEY: 'sk-upstream-api-key',
      },
    }, null, 2), 'utf8');

    const { server, store } = makeServer(39840, { clientSettings: { file: claudeSettingsFile } });
    const info = await server.start();
    try {
      const clientSettings = JSON.parse(fs.readFileSync(claudeSettingsFile, 'utf8'));
      assert.equal(clientSettings.env.ANTHROPIC_BASE_URL, info.url);
      assert.equal(clientSettings.env.ANTHROPIC_AUTH_TOKEN, info.token);
      assert.equal(clientSettings.env.CUSTOM_API_KEY, info.token);
      assert.equal(clientSettings.env.EVOMAP_PROXY_URL, info.url);
      assert.equal(clientSettings.env.EVOMAP_PROXY_AUTO_INJECTED, '1');
      assert.equal(clientSettings.env.EVOMAP_ANTHROPIC_BASE_URL, 'https://sub2api-api.evomap.work');
      assert.equal(clientSettings.env.EVOMAP_ANTHROPIC_AUTH_TOKEN, 'upstream-token');
      assert.equal(clientSettings.env.EVOMAP_ANTHROPIC_API_KEY, 'sk-upstream-api-key');
      assert.equal(clientSettings.env.ANTHROPIC_API_KEY, undefined);
      assert.equal(clientSettings._evomap_proxy_client_env.managed_by, 'evomap-proxy');
      assert.equal(process.env.EVOMAP_ANTHROPIC_BASE_URL, 'https://sub2api-api.evomap.work');
      assert.equal(process.env.EVOMAP_ANTHROPIC_AUTH_TOKEN, 'upstream-token');
      assert.equal(process.env.EVOMAP_ANTHROPIC_API_KEY, 'sk-upstream-api-key');
      assert.equal(process.env.EVOMAP_PROXY_AUTO_INJECTED, '1');
      assert.equal(process.env.ANTHROPIC_BASE_URL, undefined);
      assert.equal(process.env.ANTHROPIC_AUTH_TOKEN, undefined);
    } finally {
      await server.stop();
      store.close();
    }
  });

  it('preserves unmarked loopback Anthropic-compatible upstream credentials', async () => {
    fs.mkdirSync(path.dirname(claudeSettingsFile), { recursive: true });
    fs.writeFileSync(claudeSettingsFile, JSON.stringify({
      env: {
        ANTHROPIC_BASE_URL: 'http://127.0.0.1:19888',
        ANTHROPIC_AUTH_TOKEN: 'local-upstream-token',
      },
    }, null, 2), 'utf8');

    const { server, store } = makeServer(19820, { clientSettings: { file: claudeSettingsFile } });
    const info = await server.start();
    try {
      assert.notEqual(info.token, 'local-upstream-token', 'bare loopback upstream token must not be reused as proxy token');
      const clientSettings = JSON.parse(fs.readFileSync(claudeSettingsFile, 'utf8'));
      assert.equal(clientSettings.env.ANTHROPIC_BASE_URL, info.url);
      assert.equal(clientSettings.env.ANTHROPIC_AUTH_TOKEN, info.token);
      assert.equal(clientSettings.env.EVOMAP_ANTHROPIC_BASE_URL, 'http://127.0.0.1:19888');
      assert.equal(clientSettings.env.EVOMAP_ANTHROPIC_AUTH_TOKEN, 'local-upstream-token');
      assert.equal(process.env.EVOMAP_ANTHROPIC_BASE_URL, 'http://127.0.0.1:19888');
      assert.equal(process.env.EVOMAP_ANTHROPIC_AUTH_TOKEN, 'local-upstream-token');
    } finally {
      await server.stop();
      store.close();
    }
  });

  it('does not overwrite runtime upstream credentials while syncing client settings', async () => {
    process.env.EVOMAP_ANTHROPIC_BASE_URL = 'https://runtime-upstream.example';
    process.env.EVOMAP_ANTHROPIC_AUTH_TOKEN = 'runtime-upstream-token';
    process.env.EVOMAP_ANTHROPIC_API_KEY = 'sk-runtime-upstream';

    fs.mkdirSync(path.dirname(claudeSettingsFile), { recursive: true });
    fs.writeFileSync(claudeSettingsFile, JSON.stringify({
      env: {
        ANTHROPIC_BASE_URL: 'https://settings-upstream.example',
        ANTHROPIC_AUTH_TOKEN: 'settings-upstream-token',
        ANTHROPIC_API_KEY: 'sk-settings-upstream',
      },
    }, null, 2), 'utf8');

    const { server, store } = makeServer(39846, { clientSettings: { file: claudeSettingsFile } });
    await server.start();
    try {
      const clientSettings = JSON.parse(fs.readFileSync(claudeSettingsFile, 'utf8'));
      assert.equal(clientSettings.env.EVOMAP_ANTHROPIC_BASE_URL, 'https://settings-upstream.example');
      assert.equal(clientSettings.env.EVOMAP_ANTHROPIC_AUTH_TOKEN, 'settings-upstream-token');
      assert.equal(clientSettings.env.EVOMAP_ANTHROPIC_API_KEY, 'sk-settings-upstream');
      assert.equal(process.env.EVOMAP_ANTHROPIC_BASE_URL, 'https://runtime-upstream.example');
      assert.equal(process.env.EVOMAP_ANTHROPIC_AUTH_TOKEN, 'runtime-upstream-token');
      assert.equal(process.env.EVOMAP_ANTHROPIC_API_KEY, 'sk-runtime-upstream');
      assert.equal(process.env.ANTHROPIC_BASE_URL, undefined);
      assert.equal(process.env.ANTHROPIC_AUTH_TOKEN, undefined);
    } finally {
      await server.stop();
      store.close();
    }
  });

  it('does not combine a runtime upstream base URL with credentials migrated from settings', async () => {
    process.env.EVOMAP_ANTHROPIC_BASE_URL = 'https://runtime-upstream.example';

    fs.mkdirSync(path.dirname(claudeSettingsFile), { recursive: true });
    fs.writeFileSync(claudeSettingsFile, JSON.stringify({
      env: {
        ANTHROPIC_BASE_URL: 'https://settings-upstream.example',
        ANTHROPIC_AUTH_TOKEN: 'settings-upstream-token',
        ANTHROPIC_API_KEY: 'sk-settings-upstream',
      },
    }, null, 2), 'utf8');

    const { server, store } = makeServer(39849, { clientSettings: { file: claudeSettingsFile } });
    await server.start();
    try {
      const clientSettings = JSON.parse(fs.readFileSync(claudeSettingsFile, 'utf8'));
      assert.equal(clientSettings.env.EVOMAP_ANTHROPIC_BASE_URL, 'https://settings-upstream.example');
      assert.equal(clientSettings.env.EVOMAP_ANTHROPIC_AUTH_TOKEN, 'settings-upstream-token');
      assert.equal(clientSettings.env.EVOMAP_ANTHROPIC_API_KEY, 'sk-settings-upstream');
      assert.equal(process.env.EVOMAP_ANTHROPIC_BASE_URL, 'https://runtime-upstream.example');
      assert.equal(process.env.EVOMAP_ANTHROPIC_AUTH_TOKEN, undefined);
      assert.equal(process.env.EVOMAP_ANTHROPIC_API_KEY, undefined);
      assert.equal(process.env.EVOMAP_PROXY_AUTO_INJECTED, undefined);
      assert.equal(process.env.ANTHROPIC_BASE_URL, undefined);
      assert.equal(process.env.ANTHROPIC_AUTH_TOKEN, undefined);
    } finally {
      await server.stop();
      store.close();
    }
  });

  it('keeps stored loopback upstream after settings become proxy-managed', async () => {
    fs.mkdirSync(path.dirname(claudeSettingsFile), { recursive: true });
    fs.writeFileSync(claudeSettingsFile, JSON.stringify({
      env: {
        ANTHROPIC_BASE_URL: 'http://127.0.0.1:19820',
        ANTHROPIC_AUTH_TOKEN: fakeHexToken('6f'),
        EVOMAP_PROXY_AUTO_INJECTED: '1',
        EVOMAP_PROXY_URL: 'http://127.0.0.1:19820',
        EVOMAP_ANTHROPIC_BASE_URL: 'http://127.0.0.1:19888',
        EVOMAP_ANTHROPIC_AUTH_TOKEN: 'local-upstream-token',
      },
      _evomap_proxy_client_env: { managed_by: 'evomap-proxy' },
    }, null, 2), 'utf8');

    const { server, store } = makeServer(19820, { clientSettings: { file: claudeSettingsFile } });
    await server.start();
    try {
      assert.equal(process.env.EVOMAP_ANTHROPIC_BASE_URL, 'http://127.0.0.1:19888');
      assert.equal(process.env.EVOMAP_ANTHROPIC_AUTH_TOKEN, 'local-upstream-token');
    } finally {
      await server.stop();
      store.close();
    }
  });

  it('does not overwrite corrupt Claude client settings', async () => {
    const corruptSettings = '{ "env": { "ANTHROPIC_BASE_URL": ';
    fs.mkdirSync(path.dirname(claudeSettingsFile), { recursive: true });
    fs.writeFileSync(claudeSettingsFile, corruptSettings, 'utf8');

    const { server, store } = makeServer(39842, { clientSettings: { file: claudeSettingsFile } });
    const info = await server.start();
    try {
      assert.equal(typeof info.token, 'string');
      assert.equal(fs.readFileSync(claudeSettingsFile, 'utf8'), corruptSettings);

      const backupDir = path.join(path.dirname(claudeSettingsFile), 'backups');
      const backups = fs.readdirSync(backupDir)
        .filter((name) => name.startsWith('settings.json.pre-evomap-proxy-sync-'));
      assert.equal(backups.length, 1);
      assert.equal(fs.readFileSync(path.join(backupDir, backups[0]), 'utf8'), corruptSettings);
    } finally {
      await server.stop();
      store.close();
    }
  });

  it('removes an explicitly managed old local proxy token from upstream credentials', async () => {
    const staleProxyToken = fakeHexToken('5e');
    fs.mkdirSync(path.dirname(claudeSettingsFile), { recursive: true });
    fs.writeFileSync(claudeSettingsFile, JSON.stringify({
      env: {
        ANTHROPIC_BASE_URL: 'http://127.0.0.1:39700',
        ANTHROPIC_AUTH_TOKEN: staleProxyToken,
        EVOMAP_PROXY_AUTO_INJECTED: '1',
        EVOMAP_PROXY_URL: 'http://127.0.0.1:39700',
        EVOMAP_ANTHROPIC_BASE_URL: 'http://127.0.0.1:39700',
        EVOMAP_ANTHROPIC_AUTH_TOKEN: staleProxyToken,
      },
      _evomap_proxy_client_env: { managed_by: 'evomap-proxy' },
    }, null, 2), 'utf8');

    const { server, store } = makeServer(39841, { clientSettings: { file: claudeSettingsFile } });
    const info = await server.start();
    try {
      const clientSettings = JSON.parse(fs.readFileSync(claudeSettingsFile, 'utf8'));
      assert.equal(clientSettings.env.ANTHROPIC_BASE_URL, 'http://127.0.0.1:39841');
      assert.equal(clientSettings.env.ANTHROPIC_AUTH_TOKEN, info.token);
      assert.equal(clientSettings.env.EVOMAP_ANTHROPIC_BASE_URL, undefined);
      assert.equal(clientSettings.env.EVOMAP_ANTHROPIC_AUTH_TOKEN, undefined);
      assert.equal(process.env.EVOMAP_ANTHROPIC_BASE_URL, undefined);
      assert.equal(process.env.EVOMAP_ANTHROPIC_AUTH_TOKEN, undefined);
    } finally {
      await server.stop();
      store.close();
    }
  });

  it('removes an explicitly managed old local proxy API key from upstream credentials', async () => {
    const staleProxyToken = fakeHexToken('7a');
    fs.mkdirSync(path.dirname(claudeSettingsFile), { recursive: true });
    fs.writeFileSync(claudeSettingsFile, JSON.stringify({
      env: {
        ANTHROPIC_BASE_URL: 'http://127.0.0.1:39710',
        ANTHROPIC_AUTH_TOKEN: staleProxyToken,
        EVOMAP_PROXY_AUTO_INJECTED: '1',
        EVOMAP_PROXY_URL: 'http://127.0.0.1:39710',
        EVOMAP_ANTHROPIC_BASE_URL: 'http://127.0.0.1:39710',
        EVOMAP_ANTHROPIC_API_KEY: staleProxyToken,
      },
      _evomap_proxy_client_env: { managed_by: 'evomap-proxy' },
    }, null, 2), 'utf8');

    const { server, store } = makeServer(39850, { clientSettings: { file: claudeSettingsFile } });
    const info = await server.start();
    try {
      const clientSettings = JSON.parse(fs.readFileSync(claudeSettingsFile, 'utf8'));
      assert.equal(clientSettings.env.ANTHROPIC_BASE_URL, 'http://127.0.0.1:39850');
      assert.equal(clientSettings.env.ANTHROPIC_AUTH_TOKEN, info.token);
      assert.equal(clientSettings.env.EVOMAP_ANTHROPIC_BASE_URL, undefined);
      assert.equal(clientSettings.env.EVOMAP_ANTHROPIC_API_KEY, undefined);
      assert.equal(process.env.EVOMAP_ANTHROPIC_BASE_URL, undefined);
      assert.equal(process.env.EVOMAP_ANTHROPIC_API_KEY, undefined);
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
    const goodGrace = fakeHexToken('6f');
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

      const bad = await auth(fakeHexToken('70'));
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
        token: fakeHexToken('81'),
        previous_tokens: [fakeHexToken('92'), 42, null, false, '', { x: 1 }],
      },
    });

    const { server, store } = makeServer(39838);
    await server.start();
    try {
      const persisted = readSettings().proxy.previous_tokens;
      assert.deepEqual(persisted, [fakeHexToken('92')],
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
