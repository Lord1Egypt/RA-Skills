'use strict';

const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const crypto = require('crypto');
const fs = require('fs');
const os = require('os');
const path = require('path');

const {
  SCHEMA_VERSION,
  buildHeartbeatAntiAbuseTelemetry,
  collectIntegrityHashes,
  hmacPseudonym,
} = require('../src/gep/antiAbuseTelemetry');

function tmpRepo() {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'anti-abuse-telemetry-'));
  fs.writeFileSync(path.join(dir, 'package.json'), JSON.stringify({
    name: 'test-evolver',
    version: '0.0.0',
    bin: { evolver: 'index.js' },
  }) + '\n');
  fs.writeFileSync(path.join(dir, 'index.js'), "console.log('ok');\n");
  return dir;
}

function sha256(s) {
  return crypto.createHash('sha256').update(s).digest('hex');
}

describe('anti abuse telemetry', () => {
  let repoDir;
  let settingsDir;

  beforeEach(() => {
    repoDir = tmpRepo();
    settingsDir = fs.mkdtempSync(path.join(os.tmpdir(), 'anti-abuse-settings-'));
  });

  afterEach(() => {
    fs.rmSync(repoDir, { recursive: true, force: true });
    fs.rmSync(settingsDir, { recursive: true, force: true });
  });

  it('builds deterministic pseudonyms only when a salt is available', () => {
    const a = hmacPseudonym('device-raw', { salt: 'test-salt', purpose: 'device' });
    const b = hmacPseudonym('device-raw', { salt: 'test-salt', purpose: 'device' });
    const c = hmacPseudonym('device-raw', { salt: 'test-salt', purpose: 'workspace' });
    assert.equal(a, b);
    assert.notEqual(a, c);
    assert.equal(hmacPseudonym('device-raw', { purpose: 'device' }), null);
  });

  it('collects low-sensitive heartbeat summary and explicit unavailable fields', () => {
    const fp = {
      device_id: 'raw-device-id',
      node_version: 'v22.12.0',
      platform: 'darwin',
      arch: 'arm64',
      os_release: '25.0.0',
      hostname: 'hashed-host',
      evolver_version: '1.2.3',
      client: 'evolver',
      client_version: '1.2.3',
      model: 'test-model',
      region: 'us',
      cwd: 'hashed-cwd',
      container: false,
    };
    const payload = buildHeartbeatAntiAbuseTelemetry({
      source: 'evolver-client',
      nodeId: 'node_test',
      envFingerprint: fp,
      packageRoot: repoDir,
      now: '2026-06-08T00:00:00.000Z',
      env: {
        EVOLVER_ANTI_ABUSE_SALT: 'test-salt',
        EVOLVER_ANTI_ABUSE_SALT_ID: 'salt-v1',
        EVOLVER_ANTI_ABUSE_POLICY_VERSION: 'policy-test',
        EVOLVER_ANTI_ABUSE_TTL_DAYS: '30',
        EVOLVER_SETTINGS_DIR: settingsDir,
      },
      taskMeta: {
        task_metrics: {
          pending: '2',
          claimed: 3,
          completed: 4,
          failed: 1,
          avg_completion_ms: 1250,
        },
      },
    });

    assert.equal(payload.schema_version, SCHEMA_VERSION);
    assert.equal(payload.event_type, 'node.heartbeat');
    assert.equal(payload.policy_version, 'policy-test');
    assert.equal(payload.retention_ttl_days, 30);
    assert.equal(payload.identity.node_id, 'node_test');
    assert.equal(payload.device.pseudonym_salt_id, 'salt-v1');
    assert.match(payload.device.device_pseudonym, /^[a-f0-9]{32}$/);
    assert.match(payload.device.workspace_pseudonym, /^[a-f0-9]{32}$/);
    assert.equal(payload.device.platform, 'darwin');
    assert.equal(payload.source_confidence.network_source, 'server_observed_required');
    assert.equal(payload.task_timing.pending, 2);
    assert.equal(payload.integrity.package_json_hash, sha256(fs.readFileSync(path.join(repoDir, 'package.json'))));
    assert.equal(payload.local_security_boundary.settings_permission_class, 'missing');

    const serialized = JSON.stringify(payload);
    assert.equal(serialized.includes('test-salt'), false);
    assert.equal(serialized.includes('raw-device-id'), false);
    assert.ok(payload.unavailable_fields.some((f) => f.field === 'client_ip' && f.expected_source === 'hub_edge'));
    assert.ok(payload.unavailable_fields.some((f) => f.field === 'payout_method_token'));
  });

  it('does not invent pseudonyms without a configured salt', () => {
    const payload = buildHeartbeatAntiAbuseTelemetry({
      source: 'evolver-client',
      nodeId: 'node_test',
      envFingerprint: {
        device_id: 'raw-device-id',
        node_version: 'v22.12.0',
        platform: 'linux',
        arch: 'x64',
        client: 'evolver',
        client_version: '1.2.3',
        container: true,
      },
      packageRoot: repoDir,
      env: { EVOLVER_SETTINGS_DIR: settingsDir },
    });

    assert.equal(payload.device.device_pseudonym, null);
    assert.equal(payload.device.workspace_pseudonym, null);
    assert.ok(payload.unavailable_fields.some((f) => f.field === 'device_pseudonym' && f.reason === 'anti_abuse_salt_missing'));
  });

  it('hashes only bounded integrity files', () => {
    const hashes = collectIntegrityHashes(repoDir);
    assert.equal(hashes.package_json_hash, sha256(fs.readFileSync(path.join(repoDir, 'package.json'))));
    assert.equal(hashes.cli_entry_hash, sha256(fs.readFileSync(path.join(repoDir, 'index.js'))));
    assert.deepEqual(hashes.lockfile_hashes, {});
  });

  it('refuses to hash a bin entry that escapes the package root (traversal)', () => {
    const outside = path.join(os.tmpdir(), 'anti-abuse-outside-' + process.pid + '.js');
    fs.writeFileSync(outside, 'secret-host-file\n');
    try {
      fs.writeFileSync(path.join(repoDir, 'package.json'), JSON.stringify({
        name: 'test-evolver', version: '0.0.0',
        bin: { evolver: path.relative(repoDir, outside) },
      }));
      const hashes = collectIntegrityHashes(repoDir);
      assert.equal(hashes.cli_entry_hash, null,
        'a traversal bin path must not produce an out-of-tree file digest');
    } finally { fs.rmSync(outside, { force: true }); }
  });

  it('refuses to hash a bin entry that is a symlink escaping the package root', (t) => {
    const outside = path.join(os.tmpdir(), 'anti-abuse-symlink-target-' + process.pid + '.js');
    fs.writeFileSync(outside, 'secret-host-file\n');
    try {
      try {
        fs.symlinkSync(outside, path.join(repoDir, 'link.js'));
      } catch (e) {
        t.skip('symlinks unavailable: ' + (e && e.code)); // e.g. Windows without privilege
        return;
      }
      fs.writeFileSync(path.join(repoDir, 'package.json'), JSON.stringify({
        name: 'test-evolver', version: '0.0.0',
        bin: { evolver: 'link.js' },
      }));
      const hashes = collectIntegrityHashes(repoDir);
      assert.equal(hashes.cli_entry_hash, null,
        'a symlink escaping the tree must not produce an out-of-tree file digest');
    } finally { fs.rmSync(outside, { force: true }); }
  });

  it('omits a symlinked lockfile that escapes the package root', (t) => {
    const outside = path.join(os.tmpdir(), 'anti-abuse-lock-outside-' + process.pid + '.json');
    fs.writeFileSync(outside, '{"lockfileVersion":3}\n');
    try {
      try {
        fs.symlinkSync(outside, path.join(repoDir, 'package-lock.json'));
      } catch (e) {
        t.skip('symlinks unavailable: ' + (e && e.code));
        return;
      }
      const hashes = collectIntegrityHashes(repoDir);
      assert.deepEqual(hashes.lockfile_hashes, {},
        'an escaping lockfile symlink must not produce an out-of-tree digest');
    } finally { fs.rmSync(outside, { force: true }); }
  });

  it('nulls package_json_hash when package.json is a symlink escaping the root', (t) => {
    const outside = path.join(os.tmpdir(), 'anti-abuse-pkg-outside-' + process.pid + '.json');
    fs.writeFileSync(outside, JSON.stringify({ name: 'evil', bin: { evolver: '/etc/hostname' } }));
    try {
      const pkgPath = path.join(repoDir, 'package.json');
      fs.rmSync(pkgPath, { force: true });
      try {
        fs.symlinkSync(outside, pkgPath);
      } catch (e) {
        t.skip('symlinks unavailable: ' + (e && e.code));
        return;
      }
      const hashes = collectIntegrityHashes(repoDir);
      assert.equal(hashes.package_json_hash, null);
      assert.equal(hashes.cli_entry_hash, null);
    } finally { fs.rmSync(outside, { force: true }); }
  });

  it('proxyPortConfigured override beats env sniffing', () => {
    const base = {
      envFingerprint: { device_id: 'd', container: false },
      packageRoot: repoDir,
      env: { EVOLVER_SETTINGS_DIR: settingsDir },
    };
    const on = buildHeartbeatAntiAbuseTelemetry(Object.assign({}, base, { proxyPortConfigured: true }));
    assert.equal(on.local_security_boundary.proxy_port_configured, true);
    const off = buildHeartbeatAntiAbuseTelemetry(Object.assign({}, base, { proxyPortConfigured: false, env: { EVOLVER_SETTINGS_DIR: settingsDir, EVOMAP_PROXY_PORT: '19820' } }));
    assert.equal(off.local_security_boundary.proxy_port_configured, false,
      'an explicit false must not be overridden by env sniffing');
    const fallback = buildHeartbeatAntiAbuseTelemetry(Object.assign({}, base, { env: { EVOLVER_SETTINGS_DIR: settingsDir, EVOMAP_PROXY_PORT: '19820' } }));
    assert.equal(fallback.local_security_boundary.proxy_port_configured, true);
  });

  it('default root is the evolver package itself, not the user project', () => {
    const hashes = collectIntegrityHashes();
    // This test runs from the evolver repo, so the package root == repo root;
    // the property that matters is that the default hashes THIS package's
    // manifest (bin: index.js) rather than whatever cwd's project contains.
    const expectedPkg = sha256(fs.readFileSync(path.resolve(__dirname, '..', 'package.json')));
    assert.equal(hashes.package_json_hash, expectedPkg);
    assert.equal(hashes.cli_entry_hash, sha256(fs.readFileSync(path.resolve(__dirname, '..', 'index.js'))));
  });
});
