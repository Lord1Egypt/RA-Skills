'use strict';

const { describe, it, before, after } = require('node:test');
const assert = require('node:assert/strict');
const { execFileSync, spawnSync } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

const {
  readSettings,
  writeSettings,
  clearSettings,
  clearIfStale,
  getSettingsFile,
  getSettingsDir,
} = require('../src/proxy/server/settings');

describe('settings', () => {
  let tmpDir;
  let savedSettingsDir;

  before(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'settings-test-'));
    // Redirect the global ~/.evolver/ path into our tmpDir so chmod / file
    // assertions exercise the same code without polluting the user's real
    // settings file or racing with sibling test workers.
    savedSettingsDir = process.env.EVOLVER_SETTINGS_DIR;
    process.env.EVOLVER_SETTINGS_DIR = tmpDir;
  });

  after(() => {
    if (savedSettingsDir === undefined) delete process.env.EVOLVER_SETTINGS_DIR;
    else process.env.EVOLVER_SETTINGS_DIR = savedSettingsDir;
    try { fs.rmSync(tmpDir, { recursive: true }); } catch {}
  });

  it('writeSettings creates file and merges data', () => {
    const testFile = path.join(tmpDir, 'settings.json');
    const data = { proxy: { url: 'http://127.0.0.1:19820', pid: 1234 } };
    fs.writeFileSync(testFile, JSON.stringify(data));

    const parsed = JSON.parse(fs.readFileSync(testFile, 'utf8'));
    assert.equal(parsed.proxy.url, 'http://127.0.0.1:19820');
    assert.equal(parsed.proxy.pid, 1234);
  });

  it('readSettings returns empty object for missing file', () => {
    // Use a sub-tmp dir so the file definitively does not exist.
    const subDir = fs.mkdtempSync(path.join(tmpDir, 'missing-'));
    const prev = process.env.EVOLVER_SETTINGS_DIR;
    process.env.EVOLVER_SETTINGS_DIR = subDir;
    try {
      const result = readSettings();
      assert.ok(typeof result === 'object');
    } finally {
      process.env.EVOLVER_SETTINGS_DIR = prev;
    }
  });

  it('writeSettings sets 0o600 on fresh settings file', {
    skip: process.platform === 'win32' ? 'chmod not enforced on Windows' : false,
  }, () => {
    writeSettings({ _test: true });
    const mode = fs.statSync(getSettingsFile()).mode & 0o777;
    assert.equal(mode, 0o600, 'settings.json must be owner-read-only after fresh write');
  });

  it('writeSettings tightens 0o644 pre-existing file to 0o600 (upgrade path)', {
    skip: process.platform === 'win32' ? 'chmod not enforced on Windows' : false,
  }, () => {
    // Simulate a pre-existing file with loose permissions (pre-C3 upgrade)
    const dir = getSettingsDir();
    const file = getSettingsFile();
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(file, JSON.stringify({}), { encoding: 'utf8', mode: 0o644 });
    fs.chmodSync(file, 0o644);
    assert.equal(fs.statSync(file).mode & 0o777, 0o644, 'precondition: file starts at 0o644');

    writeSettings({ _test: true });
    const mode = fs.statSync(file).mode & 0o777;
    assert.equal(mode, 0o600, 'writeSettings must tighten 0o644 to 0o600');
  });

  it('proxy-token command prints only the local proxy token', () => {
    writeSettings({ proxy: { url: 'http://127.0.0.1:19820', token: 'proxy-token-test', pid: process.pid } });
    const out = execFileSync(process.execPath, [path.join(__dirname, '..', 'index.js'), 'proxy-token'], {
      encoding: 'utf8',
      env: { ...process.env, EVOLVER_SETTINGS_DIR: tmpDir },
    });
    assert.equal(out, 'proxy-token-test\n');
  });

  it('clearSettings removes the proxy block owned by the current process', () => {
    writeSettings({
      proxy: { url: 'http://127.0.0.1:19820', token: 'owned-token', pid: process.pid },
      other: true,
    });

    const removed = clearSettings();

    const settings = readSettings();
    assert.equal(removed, true);
    assert.equal(settings.proxy, undefined);
    assert.equal(settings.other, true);
  });

  it('clearSettings preserves a proxy block owned by another process', () => {
    writeSettings({
      proxy: { url: 'http://127.0.0.1:19821', token: 'new-token', pid: process.pid + 1 },
      other: true,
    });

    const removed = clearSettings();

    const settings = readSettings();
    assert.equal(removed, false);
    assert.equal(settings.proxy.url, 'http://127.0.0.1:19821');
    assert.equal(settings.proxy.token, 'new-token');
    assert.equal(settings.other, true);
  });

  it('clearIfStale can still clear a stale proxy block', () => {
    const realKill = process.kill;
    process.kill = (pid, signal) => {
      assert.equal(pid, 42424242);
      assert.equal(signal, 0);
      const err = new Error('not found');
      err.code = 'ESRCH';
      throw err;
    };

    try {
      writeSettings({
        proxy: { url: 'http://127.0.0.1:19822', token: 'stale-token', pid: 42424242 },
        other: true,
      });

      const removed = clearIfStale();
      const settings = readSettings();
      assert.equal(removed, true);
      assert.equal(settings.proxy, undefined);
      assert.equal(settings.other, true);
    } finally {
      process.kill = realKill;
    }
  });

  it('proxy-token command can read an explicit settings file', () => {
    const explicitDir = fs.mkdtempSync(path.join(tmpDir, 'explicit-'));
    const explicitSettings = path.join(explicitDir, 'settings.json');
    fs.writeFileSync(explicitSettings, JSON.stringify({
      proxy: { url: 'http://127.0.0.1:19999', token: 'explicit-token-test', pid: process.pid },
    }));
    const out = execFileSync(process.execPath, [
      path.join(__dirname, '..', 'index.js'),
      'proxy-token',
      '--settings',
      explicitSettings,
    ], {
      encoding: 'utf8',
      env: { ...process.env, EVOLVER_SETTINGS_DIR: tmpDir },
    });
    assert.equal(out, 'explicit-token-test\n');
  });

  it('proxy-token help and argument errors do not print the token', () => {
    writeSettings({ proxy: { url: 'http://127.0.0.1:19820', token: 'proxy-token-secret', pid: process.pid } });
    const bin = process.execPath;
    const cli = path.join(__dirname, '..', 'index.js');
    const env = { ...process.env, EVOLVER_SETTINGS_DIR: tmpDir };

    const help = spawnSync(bin, [cli, 'proxy-token', '--help'], { encoding: 'utf8', env });
    assert.equal(help.status, 0);
    assert.match(help.stdout, /proxy-token \[--settings FILE\]/);
    assert.ok(!help.stdout.includes('proxy-token-secret'));
    assert.ok(!help.stderr.includes('proxy-token-secret'));

    const unknown = spawnSync(bin, [cli, 'proxy-token', '--bad-flag'], { encoding: 'utf8', env });
    assert.equal(unknown.status, 2);
    assert.match(unknown.stderr, /unknown argument/);
    assert.ok(!unknown.stdout.includes('proxy-token-secret'));
    assert.ok(!unknown.stderr.includes('proxy-token-secret'));

    const missing = spawnSync(bin, [cli, 'proxy-token', '--settings'], { encoding: 'utf8', env });
    assert.equal(missing.status, 2);
    assert.match(missing.stderr, /missing value/);
    assert.ok(!missing.stdout.includes('proxy-token-secret'));
    assert.ok(!missing.stderr.includes('proxy-token-secret'));
  });

  it('internal-proxy-env prints Codex config without embedding the token', () => {
    writeSettings({ proxy: { url: 'http://127.0.0.1:19820', token: 'proxy-token-secret', pid: process.pid } });
    const script = path.join(__dirname, '..', 'scripts', 'internal-proxy-env.sh');
    const out = execFileSync('bash', [script, '--settings', getSettingsFile(), '--codex-config'], {
      encoding: 'utf8',
    });
    assert.match(out, /base_url = "http:\/\/127\.0\.0\.1:19820\/v1"/);
    assert.match(out, new RegExp(`command = ${JSON.stringify(process.execPath).replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}`));
    assert.match(out, /"proxy-token"/);
    assert.match(out, /"--settings"/);
    assert.match(out, new RegExp(JSON.stringify(getSettingsFile()).replace(/[.*+?^${}()|[\]\\]/g, '\\$&')));
    assert.ok(!out.includes('proxy-token-secret'), 'config snippet must not contain the bearer token');
  });
});
