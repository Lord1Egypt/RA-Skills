'use strict';

const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const { spawn } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

const lifecycle = require('../src/ops/lifecycle');
const { writeSettings } = require('../src/proxy/server/settings');

function startStatusServer(mode, token) {
  const child = spawn(process.execPath, ['-e', `
const http = require('http');
const mode = process.env.TEST_PROXY_MODE;
const token = process.env.TEST_PROXY_TOKEN;
const server = http.createServer((req, res) => {
  if (mode === 'auth') {
    if (req.headers.authorization !== 'Bearer ' + token) {
      res.writeHead(401, { 'content-type': 'application/json' });
      res.end(JSON.stringify({ error: 'unauthorized' }));
      return;
    }
    res.writeHead(200, { 'content-type': 'application/json' });
    res.end(JSON.stringify({
      status: 'running',
      proxy_protocol_version: '1.0.0',
      schema_version: '1.0.0',
    }));
    return;
  }
  res.writeHead(200, { 'content-type': 'application/json' });
  res.end(JSON.stringify({ ok: true }));
});
server.listen(0, '127.0.0.1', () => {
  process.stdout.write('http://127.0.0.1:' + server.address().port + '\\n');
});
process.on('SIGTERM', () => server.close(() => process.exit(0)));
`], {
    env: { PATH: process.env.PATH, TEST_PROXY_MODE: mode, TEST_PROXY_TOKEN: token || '' },
    stdio: ['ignore', 'pipe', 'inherit'],
  });
  return new Promise((resolve, reject) => {
    let settled = false;
    child.once('error', reject);
    child.stdout.once('data', (chunk) => {
      settled = true;
      resolve({ child, url: String(chunk).trim() });
    });
    child.once('exit', (code) => {
      if (!settled) reject(new Error(`status server exited early: ${code}`));
    });
  });
}

function close(child) {
  return new Promise((resolve) => {
    if (child.exitCode !== null) {
      resolve();
      return;
    }
    child.once('exit', resolve);
    child.kill('SIGTERM');
  });
}

describe('ops lifecycle proxy health', () => {
  let tmpDir;
  let savedSettingsDir;

  beforeEach(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'lifecycle-proxy-'));
    savedSettingsDir = process.env.EVOLVER_SETTINGS_DIR;
    process.env.EVOLVER_SETTINGS_DIR = tmpDir;
  });

  afterEach(() => {
    lifecycle._resetProcessTableForTest();
    if (savedSettingsDir === undefined) delete process.env.EVOLVER_SETTINGS_DIR;
    else process.env.EVOLVER_SETTINGS_DIR = savedSettingsDir;
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  it('treats injected loopback client config as requiring proxy mode', () => {
    const env = {
      ANTHROPIC_BASE_URL: 'http://127.0.0.1:19820',
      EVOMAP_PROXY_AUTO_INJECTED: '1',
    };

    assert.equal(lifecycle.expectsProxy(env), true);
    assert.equal(lifecycle.prepareStartEnv(env).EVOMAP_PROXY, '1');
  });

  it('treats selected Codex loopback provider config as requiring proxy mode', () => {
    const codexDir = path.join(tmpDir, '.codex');
    fs.mkdirSync(codexDir, { recursive: true });
    fs.writeFileSync(path.join(codexDir, 'config.toml'), [
      'model_provider = "evomap-proxy"',
      '',
      '[model_providers.evomap-proxy]',
      'name = "EvoMap Proxy"',
      'base_url = "http://127.0.0.1:19820/v1"',
      'wire_api = "responses"',
      '',
    ].join('\n'), 'utf8');

    assert.equal(lifecycle.expectsProxy({ HOME: tmpDir }), true);
  });

  it('reports stale proxy pid unhealthy when proxy mode is expected', () => {
    writeSettings({
      proxy: {
        url: 'http://127.0.0.1:19820',
        token: 'test-token',
        pid: 42424242,
      },
    });

    const health = lifecycle.checkProxyHealth({
      ANTHROPIC_BASE_URL: 'http://127.0.0.1:19820',
    });

    assert.equal(health.healthy, false);
    assert.equal(health.reason, 'proxy_pid_stale');
    assert.equal(health.proxyPid, 42424242);
  });

  it('asks lifecycle start to restart a live loop when required proxy is unhealthy', () => {
    writeSettings({
      proxy: {
        url: 'http://127.0.0.1:19820',
        token: 'test-token',
        pid: 42424242,
      },
    });

    assert.equal(
      lifecycle.shouldRestartForProxy([process.pid], {
        ANTHROPIC_BASE_URL: 'http://127.0.0.1:19820',
      }),
      true
    );
  });

  it('does not treat another repo loop command as owned by this restart path', () => {
    const repoRoot = path.resolve(__dirname, '..');
    assert.equal(
      lifecycle.isCurrentLoopCommand(`${process.execPath} /tmp/other/index.js --loop`),
      false
    );
    assert.equal(
      lifecycle.isCurrentLoopCommand(`${process.execPath} ${path.join(repoRoot, 'index.js')} --loop`),
      true
    );
  });

  // These four cases assert how the proxy-health/owned-loop detection
  // classifies live `node index.js --loop` processes. They inject a synthetic
  // process table (lifecycle._setProcessTableForTest) instead of spawning real
  // processes and reading the host's actual ps/proc output: on CI runners and
  // on a live agent box there are unrelated real --loop processes, which made
  // the system-wide scan (getRunningPids/checkHealth/stopOwnedLoops) fail these
  // assertions and could even SIGTERM real production loops. The injected table
  // makes them hermetic and deterministic. Reset in afterEach.

  it('does not select a live unrelated node index.js --loop process as owned', () => {
    // Unrelated: an ABSOLUTE path to a different index.js, in another cwd.
    lifecycle._setProcessTableForTest([
      { pid: 990001, args: 'node /tmp/other-evolver/index.js --loop', cwd: '/tmp/other-evolver' },
    ]);
    assert.deepEqual(lifecycle.getOwnedLoopPids([990001]), []);
    assert.equal(lifecycle.stopOwnedLoops().status, 'not_running');
  });

  it('selects a live relative index.js --loop process from the current repo cwd as owned', () => {
    const repoRoot = path.resolve(__dirname, '..');
    lifecycle._setProcessTableForTest([
      { pid: 990002, args: 'node index.js --loop', cwd: repoRoot },
    ]);
    assert.deepEqual(lifecycle.getOwnedLoopPids([990002]), [990002]);
    // The system-wide scan also resolves it (the path the real failure hit).
    assert.deepEqual(lifecycle.getOwnedLoopPids(lifecycle.getRunningPids()), [990002]);
  });

  it('does not select a live relative index.js --loop process from another cwd as owned', () => {
    // Relative index.js but launched from an unrelated cwd -> not this repo's loop.
    lifecycle._setProcessTableForTest([
      { pid: 990003, args: 'node index.js --loop', cwd: '/tmp/other-evolver-relative' },
    ]);
    assert.deepEqual(lifecycle.getOwnedLoopPids([990003]), []);
    assert.equal(lifecycle.stopOwnedLoops().status, 'not_running');
  });

  it('reports not_running when only an unrelated node index.js --loop process exists', () => {
    lifecycle._setProcessTableForTest([
      { pid: 990004, args: 'node /tmp/other-evolver-health/index.js --loop', cwd: '/tmp/other-evolver-health' },
    ]);
    const health = lifecycle.checkHealth();
    assert.equal(health.healthy, false);
    assert.equal(health.reason, 'not_running');
  });

  it('reports missing proxy token as unhealthy when proxy mode is expected', () => {
    writeSettings({
      proxy: {
        url: 'http://127.0.0.1:19820',
        pid: process.pid,
      },
    });

    const health = lifecycle.checkProxyHealth({ EVOMAP_PROXY: '1' });

    assert.equal(health.healthy, false);
    assert.equal(health.reason, 'proxy_token_missing');
  });

  it('reports a 401 proxy status probe as unhealthy', async () => {
    const fixtureToken = 'fixture-proxy-token';
    const { child, url } = await startStatusServer('auth', fixtureToken);
    try {
      writeSettings({
        proxy: {
          url,
          token: 'wrong-fixture-token',
          pid: process.pid,
        },
      });

      const health = lifecycle.checkProxyHealth({ EVOMAP_PROXY: '1' });

      assert.equal(health.healthy, false);
      assert.equal(health.reason, 'proxy_unreachable');
    } finally {
      await close(child);
    }
  });

  it('reports a non-proxy 200 response as unhealthy', async () => {
    const { child, url } = await startStatusServer('non-proxy');
    try {
      writeSettings({
        proxy: {
          url,
          token: 'fixture-proxy-token',
          pid: process.pid,
        },
      });

      const health = lifecycle.checkProxyHealth({ EVOMAP_PROXY: '1' });

      assert.equal(health.healthy, false);
      assert.equal(health.reason, 'proxy_unreachable');
    } finally {
      await close(child);
    }
  });

  it('reports an authenticated Evolver proxy status response as healthy', async () => {
    const fixtureToken = 'fixture-proxy-token';
    const { child, url } = await startStatusServer('auth', fixtureToken);
    try {
      writeSettings({
        proxy: {
          url,
          token: fixtureToken,
          pid: process.pid,
        },
      });

      const health = lifecycle.checkProxyHealth({ EVOMAP_PROXY: '1' });

      assert.equal(health.healthy, true);
      assert.equal(health.expected, true);
    } finally {
      await close(child);
    }
  });
});
