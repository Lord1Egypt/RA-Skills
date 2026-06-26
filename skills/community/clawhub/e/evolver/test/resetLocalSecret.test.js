'use strict';

// Smoke for the `evolver reset-local-secret` CLI helper. Verifies that
// running it against a controlled fake $HOME wipes:
//   - mailbox/state.json node_secret + node_secret_source
//   - legacy ~/.evomap/node_secret file
// and prints the unset-A2A_NODE_SECRET hint when the env var is set.

const test = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');

const REPO_ROOT = path.resolve(__dirname, '..');
const INDEX_JS = path.join(REPO_ROOT, 'index.js');

function makeFakeHome(setupFn) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-reset-test-'));
  const evomapDir = path.join(dir, '.evomap');
  const mailboxDir = path.join(evomapDir, 'mailbox');
  fs.mkdirSync(mailboxDir, { recursive: true });
  setupFn({ home: dir, evomapDir, mailboxDir });
  return dir;
}

function rmrf(p) {
  try { fs.rmSync(p, { recursive: true, force: true }); } catch {}
}

function runCli(home, env = {}) {
  return spawnSync(process.execPath, [INDEX_JS, 'reset-local-secret'], {
    env: { ...process.env, HOME: home, ...env, A2A_NODE_SECRET: env.A2A_NODE_SECRET },
    encoding: 'utf8',
    timeout: 20_000,
  });
}

test('reset-local-secret: clears mailbox state and legacy file', () => {
  const home = makeFakeHome(({ mailboxDir, evomapDir }) => {
    fs.writeFileSync(
      path.join(mailboxDir, 'state.json'),
      JSON.stringify({
        _schema_version: 1,
        node_secret: 'a'.repeat(64),
        node_secret_source: 'hub_rotate',
        node_id: 'node_test',
      }, null, 2)
    );
    fs.writeFileSync(path.join(evomapDir, 'node_secret'), 'b'.repeat(64));
  });
  try {
    // Spawn child WITHOUT A2A_NODE_SECRET so the unset-hint branch is not
    // taken (separate test below covers that).
    const cleanEnv = { ...process.env, HOME: home };
    delete cleanEnv.A2A_NODE_SECRET;
    const res = spawnSync(process.execPath, [INDEX_JS, 'reset-local-secret'], {
      env: cleanEnv,
      encoding: 'utf8',
      timeout: 20_000,
    });
    assert.strictEqual(res.status, 0, `exit 0 expected, stderr: ${res.stderr}`);

    const stateAfter = JSON.parse(
      fs.readFileSync(path.join(home, '.evomap', 'mailbox', 'state.json'), 'utf8')
    );
    assert.strictEqual(stateAfter.node_secret, '', 'node_secret must be cleared');
    assert.strictEqual(stateAfter.node_secret_source, '', 'source tag must be cleared');
    assert.strictEqual(stateAfter.node_id, 'node_test', 'node_id must NOT be touched');
    assert.ok(
      !fs.existsSync(path.join(home, '.evomap', 'node_secret')),
      'legacy ~/.evomap/node_secret must be deleted'
    );
    assert.match(res.stdout, /A2A_NODE_SECRET is not set in env/, 'should confirm env is clean');
  } finally {
    rmrf(home);
  }
});

test('reset-local-secret: warns about A2A_NODE_SECRET still set in shell', () => {
  const home = makeFakeHome(({ mailboxDir }) => {
    fs.writeFileSync(
      path.join(mailboxDir, 'state.json'),
      JSON.stringify({ node_secret: 'a'.repeat(64) }, null, 2)
    );
  });
  try {
    const env = { ...process.env, HOME: home, A2A_NODE_SECRET: 'c'.repeat(64) };
    const res = spawnSync(process.execPath, [INDEX_JS, 'reset-local-secret'], {
      env,
      encoding: 'utf8',
      timeout: 20_000,
    });
    assert.strictEqual(res.status, 0, `exit 0, stderr: ${res.stderr}`);
    assert.match(res.stdout, /A2A_NODE_SECRET is still set/, 'should print stale-env warning');
    assert.match(res.stdout, /unset A2A_NODE_SECRET/, 'should print unset hint');
  } finally {
    rmrf(home);
  }
});

test('reset-local-secret: idempotent on already-empty environment', () => {
  const home = makeFakeHome(() => { /* no files written */ });
  try {
    const cleanEnv = { ...process.env, HOME: home };
    delete cleanEnv.A2A_NODE_SECRET;
    const res = spawnSync(process.execPath, [INDEX_JS, 'reset-local-secret'], {
      env: cleanEnv,
      encoding: 'utf8',
      timeout: 20_000,
    });
    assert.strictEqual(res.status, 0, `exit 0, stderr: ${res.stderr}`);
    assert.match(res.stdout, /0 location\(s\) cleared/, 'should report nothing to clear');
  } finally {
    rmrf(home);
  }
});
