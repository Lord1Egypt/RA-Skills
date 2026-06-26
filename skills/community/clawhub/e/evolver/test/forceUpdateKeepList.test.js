const { describe, it, before, after, beforeEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');

// Strategy: forceUpdate.js destructures `execFileSync` at module load time.
// To inject a stub we must (a) mutate child_process.execFileSync before the
// first require, then (b) purge forceUpdate from cache between tests so each
// freshRequire picks up whatever stub is current.

const childProcess = require('child_process');
const origExecFileSync = childProcess.execFileSync;

const forceUpdateModPath = require.resolve('../src/forceUpdate');
const pathsModPath = require.resolve('../src/gep/paths');

let installRoot;

function freshRequireForceUpdate(execFileStub) {
  delete require.cache[forceUpdateModPath];
  require.cache[pathsModPath] = {
    id: pathsModPath, filename: pathsModPath, loaded: true,
    exports: { getEvolverInstallRoot: () => installRoot },
  };
  childProcess.execFileSync = execFileStub;
  try {
    return require('../src/forceUpdate');
  } finally {
    childProcess.execFileSync = origExecFileSync;
  }
}

// Fake degit: write a new-version package.json + index.js into TMP_TARGET.
// args layout: ['-y', 'degit', 'EvoMap/evolver', <TMP_TARGET>]
function makeSuccessfulDegit(version) {
  return function (_bin, args) {
    const tmpTarget = args[args.length - 1];
    fs.mkdirSync(tmpTarget, { recursive: true });
    fs.writeFileSync(
      path.join(tmpTarget, 'package.json'),
      JSON.stringify({ name: '@evomap/evolver', version }),
      'utf8',
    );
    fs.writeFileSync(path.join(tmpTarget, 'index.js'), '// v' + version, 'utf8');
  };
}

function makeDegitWithLocalStateFiles(version) {
  return function (_bin, args) {
    const tmpTarget = args[args.length - 1];
    fs.mkdirSync(tmpTarget, { recursive: true });
    fs.writeFileSync(
      path.join(tmpTarget, 'package.json'),
      JSON.stringify({ name: '@evomap/evolver', version }),
      'utf8',
    );
    fs.writeFileSync(path.join(tmpTarget, 'index.js'), '// v' + version, 'utf8');
    fs.writeFileSync(path.join(tmpTarget, '.env'), 'A2A_NODE_SECRET=from-release\n', 'utf8');
    fs.writeFileSync(path.join(tmpTarget, '.env.local'), 'DEBUG=from-release\n', 'utf8');
    fs.writeFileSync(path.join(tmpTarget, 'USER.md'), '# release user notes\n', 'utf8');
    fs.mkdirSync(path.join(tmpTarget, '.evolver'), { recursive: true });
    fs.writeFileSync(path.join(tmpTarget, '.evolver', 'config.json'), '{"workspaceId":"release"}', 'utf8');
    fs.mkdirSync(path.join(tmpTarget, 'memory'), { recursive: true });
    fs.writeFileSync(path.join(tmpTarget, 'memory', 'state.json'), '{"from":"release"}', 'utf8');
  };
}

function populateFakeInstall(root) {
  // Package identity (required by the guard at the top of executeForceUpdate)
  fs.writeFileSync(
    path.join(root, 'package.json'),
    JSON.stringify({ name: '@evomap/evolver', version: '1.0.0' }),
    'utf8',
  );
  // Old code that MUST be replaced
  fs.writeFileSync(path.join(root, 'index.js'), '// old', 'utf8');
  fs.mkdirSync(path.join(root, 'src'), { recursive: true });
  fs.writeFileSync(path.join(root, 'src', 'evolve.js'), '// old', 'utf8');
  // Classic keep-list entries (must survive)
  fs.mkdirSync(path.join(root, 'node_modules'), { recursive: true });
  fs.mkdirSync(path.join(root, 'memory'), { recursive: true });
  fs.mkdirSync(path.join(root, '.git'), { recursive: true });
  fs.writeFileSync(path.join(root, 'MEMORY.md'), '# mem\n', 'utf8');
  // New keep-list entries (must survive after this fix)
  fs.writeFileSync(path.join(root, '.env'), 'A2A_HUB_URL=https://hub.example.com\nA2A_NODE_SECRET=s3cr3t\n', 'utf8');
  fs.writeFileSync(path.join(root, '.env.local'), 'DEBUG=1\n', 'utf8');
  fs.writeFileSync(path.join(root, 'USER.md'), '# my notes\n', 'utf8');
  fs.mkdirSync(path.join(root, '.evolver'), { recursive: true });
  fs.writeFileSync(path.join(root, '.evolver', 'config.json'), '{"workspaceId":"wid_test"}', 'utf8');
}

describe('executeForceUpdate: keep-list preserves user config files', () => {
  before(() => {
    installRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-keeplist-'));
  });

  after(() => {
    childProcess.execFileSync = origExecFileSync;
    delete require.cache[pathsModPath];
    delete require.cache[forceUpdateModPath];
    try { fs.rmSync(installRoot, { recursive: true, force: true }); } catch (_) {}
  });

  beforeEach(() => {
    childProcess.execFileSync = origExecFileSync;
    try { fs.rmSync(installRoot, { recursive: true, force: true }); } catch (_) {}
    fs.mkdirSync(installRoot, { recursive: true });
  });

  it('preserves .env, .env.local, USER.md, .evolver/ and replaces old code files', () => {
    populateFakeInstall(installRoot);

    const { executeForceUpdate } = freshRequireForceUpdate(makeSuccessfulDegit('999.999.999'));
    // Match the stub's degit-returned version exactly: the version check in
    // src/forceUpdate.js is now `===` (no range matching) to prevent a
    // compromised hub from coercing an install with a permissive range like
    // '>=0.0.1'. The earlier '>=1.0.0' form encoded the pre-tightening
    // contract.
    const result = executeForceUpdate({ required_version: '999.999.999' });

    assert.equal(result, true, 'update should succeed');

    // --- new keep-list entries ---
    assert.ok(fs.existsSync(path.join(installRoot, '.env')),
      '.env must be preserved (contains hub credentials)');
    assert.equal(
      fs.readFileSync(path.join(installRoot, '.env'), 'utf8'),
      'A2A_HUB_URL=https://hub.example.com\nA2A_NODE_SECRET=s3cr3t\n',
      '.env content must be unchanged',
    );
    assert.ok(fs.existsSync(path.join(installRoot, '.env.local')),
      '.env.local must be preserved');
    assert.ok(fs.existsSync(path.join(installRoot, 'USER.md')),
      'USER.md must be preserved');
    assert.ok(fs.existsSync(path.join(installRoot, '.evolver', 'config.json')),
      '.evolver/config.json must be preserved');

    // --- classic keep-list entries still intact ---
    assert.ok(fs.existsSync(path.join(installRoot, 'node_modules')), 'node_modules/ preserved');
    assert.ok(fs.existsSync(path.join(installRoot, 'memory')), 'memory/ preserved');
    assert.ok(fs.existsSync(path.join(installRoot, '.git')), '.git/ preserved');
    assert.ok(fs.existsSync(path.join(installRoot, 'MEMORY.md')), 'MEMORY.md preserved');

    // --- old code must be replaced by new version ---
    assert.ok(fs.existsSync(path.join(installRoot, 'index.js')), 'index.js should exist after update');
    assert.equal(
      fs.readFileSync(path.join(installRoot, 'index.js'), 'utf8'),
      '// v999.999.999',
      'index.js must have new version content',
    );
    assert.ok(!fs.existsSync(path.join(installRoot, 'src', 'evolve.js')),
      'old src/evolve.js must be gone after update');
  });

  it('does NOT wipe .env when degit fails (update aborted)', () => {
    populateFakeInstall(installRoot);

    const { executeForceUpdate } = freshRequireForceUpdate(() => {
      throw new Error('simulated network failure');
    });
    // Use a version strictly NEWER than populateFakeInstall's '1.0.0' so we
    // bypass the idempotency short-circuit (which correctly returns true when
    // already at the required version) and actually exercise the degit
    // failure path that this test is asserting on.
    const result = executeForceUpdate({ required_version: '>=2.0.0' });

    assert.equal(result.ok, false, 'update should fail');
    assert.equal(result.code, 'degit_failed', 'degit network throw classified as degit_failed');
    // Deletion loop never runs when degit fails — .env must still be present
    assert.ok(fs.existsSync(path.join(installRoot, '.env')),
      '.env must survive a failed update');
    assert.ok(fs.existsSync(path.join(installRoot, 'index.js')),
      'old index.js must survive a failed update (no replacement happened)');
  });

  it('does NOT overwrite keep-list state even if the release archive contains those paths', () => {
    populateFakeInstall(installRoot);
    fs.writeFileSync(path.join(installRoot, 'memory', 'state.json'), '{"from":"local"}', 'utf8');

    const { executeForceUpdate } = freshRequireForceUpdate(makeDegitWithLocalStateFiles('2.0.0'));
    const result = executeForceUpdate({ required_version: '2.0.0' });

    assert.equal(result, true, 'update should succeed');
    assert.equal(
      fs.readFileSync(path.join(installRoot, '.env'), 'utf8'),
      'A2A_HUB_URL=https://hub.example.com\nA2A_NODE_SECRET=s3cr3t\n',
      '.env must remain local, not release-provided',
    );
    assert.equal(fs.readFileSync(path.join(installRoot, '.env.local'), 'utf8'), 'DEBUG=1\n');
    assert.equal(fs.readFileSync(path.join(installRoot, 'USER.md'), 'utf8'), '# my notes\n');
    assert.equal(
      fs.readFileSync(path.join(installRoot, '.evolver', 'config.json'), 'utf8'),
      '{"workspaceId":"wid_test"}',
    );
    assert.equal(fs.readFileSync(path.join(installRoot, 'memory', 'state.json'), 'utf8'), '{"from":"local"}');
  });
});
