'use strict';

// Smoke for the `evolver reset-local-secret` CLI helper. Verifies that
// running it against a controlled fake $HOME wipes:
//   - mailbox/state.json node_secret + source/version/suppression state
//   - legacy ~/.evomap/node_secret, node_secret_version, source, and suppression files
// and prints the unset-node-secret-env hint when any secret env var is set.

const test = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');

const REPO_ROOT = path.resolve(__dirname, '..');
const INDEX_JS = path.join(REPO_ROOT, 'index.js');
const SUPPRESSION_MARKER = 'sha256:' + '0'.repeat(64);

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
    env: { ...process.env, HOME: home, ...env },
    encoding: 'utf8',
    timeout: 20_000,
  });
}

function deleteNodeSecretEnv(env) {
  delete env.A2A_NODE_SECRET;
  delete env.A2A_NODE_SECRET_VERSION;
  delete env.EVOMAP_NODE_SECRET;
  delete env.EVOMAP_NODE_SECRET_VERSION;
}

test('reset-local-secret: clears mailbox state and legacy file', () => {
  const home = makeFakeHome(({ mailboxDir, evomapDir }) => {
    fs.writeFileSync(
      path.join(mailboxDir, 'state.json'),
      JSON.stringify({
        _schema_version: 1,
        node_secret: 'a'.repeat(64),
        node_secret_source: 'hub_rotate',
        node_secret_version: '3',
        node_secret_env_suppressed: SUPPRESSION_MARKER,
        node_id: 'node_test',
      }, null, 2)
    );
    fs.writeFileSync(path.join(evomapDir, 'node_secret'), 'b'.repeat(64));
    fs.writeFileSync(path.join(evomapDir, 'node_secret_version'), '3');
    fs.writeFileSync(path.join(evomapDir, 'node_secret_source'), 'hub_rotate');
    fs.writeFileSync(path.join(evomapDir, 'node_secret_env_suppressed'), SUPPRESSION_MARKER);
  });
  try {
    // Spawn child WITHOUT node secret env vars so the unset-hint branch is not
    // taken (separate test below covers that).
    const cleanEnv = { ...process.env, HOME: home, EVOLVER_HOME: path.join(home, '.evomap') };
    deleteNodeSecretEnv(cleanEnv);
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
    assert.strictEqual(stateAfter.node_secret_version, '', 'node_secret_version must be cleared');
    assert.strictEqual(stateAfter.node_secret_env_suppressed, '', 'env suppression marker must be cleared');
    assert.strictEqual(stateAfter.node_id, 'node_test', 'node_id must NOT be touched');
    assert.ok(
      !fs.existsSync(path.join(home, '.evomap', 'node_secret')),
      'legacy ~/.evomap/node_secret must be deleted'
    );
    assert.ok(
      !fs.existsSync(path.join(home, '.evomap', 'node_secret_version')),
      'legacy ~/.evomap/node_secret_version must be deleted'
    );
    assert.ok(
      !fs.existsSync(path.join(home, '.evomap', 'node_secret_source')),
      'legacy ~/.evomap/node_secret_source must be deleted'
    );
    assert.ok(
      !fs.existsSync(path.join(home, '.evomap', 'node_secret_env_suppressed')),
      'legacy ~/.evomap/node_secret_env_suppressed must be deleted'
    );
    assert.match(res.stdout, /Node secret env vars are not set in env/, 'should confirm env is clean');
    assert.match(res.stdout, /5 location\(s\) cleared/, 'duplicate HOME/EVOLVER_HOME path must only count once');
  } finally {
    rmrf(home);
  }
});

test('reset-local-secret: clears separate EVOLVER_HOME stores without touching real home', () => {
  const realHome = os.homedir();
  const home = makeFakeHome(({ evomapDir }) => {
    fs.writeFileSync(path.join(evomapDir, 'node_secret_source'), 'env_seed');
  });
  const evolverHome = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-reset-home-test-'));
  const evolverMailboxDir = path.join(evolverHome, 'mailbox');
  fs.mkdirSync(evolverMailboxDir, { recursive: true });
  fs.writeFileSync(
    path.join(evolverMailboxDir, 'state.json'),
    JSON.stringify({
      node_secret_source: 'hub_rotate',
      node_secret_env_suppressed: SUPPRESSION_MARKER,
      node_id: 'node_test',
    }, null, 2)
  );
  fs.writeFileSync(path.join(evolverHome, 'node_secret_source'), 'hub_rotate');
  fs.writeFileSync(path.join(evolverHome, 'node_secret_env_suppressed'), SUPPRESSION_MARKER);

  try {
    assert.notStrictEqual(path.join(home, '.evomap'), evolverHome, 'test requires distinct stores');
    const cleanEnv = { ...process.env, HOME: home, EVOLVER_HOME: evolverHome };
    deleteNodeSecretEnv(cleanEnv);
    const res = spawnSync(process.execPath, [INDEX_JS, 'reset-local-secret'], {
      env: cleanEnv,
      encoding: 'utf8',
      timeout: 20_000,
    });
    assert.strictEqual(res.status, 0, `exit 0 expected, stderr: ${res.stderr}`);

    assert.ok(
      !fs.existsSync(path.join(home, '.evomap', 'node_secret_source')),
      'legacy HOME node_secret_source must be deleted'
    );
    assert.ok(
      !fs.existsSync(path.join(evolverHome, 'node_secret_source')),
      'legacy EVOLVER_HOME node_secret_source must be deleted'
    );
    assert.ok(
      !fs.existsSync(path.join(evolverHome, 'node_secret_env_suppressed')),
      'legacy EVOLVER_HOME suppression marker must be deleted'
    );

    const stateAfter = JSON.parse(
      fs.readFileSync(path.join(evolverMailboxDir, 'state.json'), 'utf8')
    );
    assert.strictEqual(stateAfter.node_secret_source, '', 'EVOLVER_HOME source state must be cleared');
    assert.strictEqual(stateAfter.node_secret_env_suppressed, '', 'EVOLVER_HOME suppression state must be cleared');
    assert.strictEqual(stateAfter.node_id, 'node_test', 'EVOLVER_HOME node_id must NOT be touched');
    assert.ok(!res.stdout.includes(realHome), 'command output must not reference the real home directory');
  } finally {
    rmrf(home);
    rmrf(evolverHome);
  }
});

test('reset-local-secret: warns about node secret env vars still set in shell', () => {
  const home = makeFakeHome(({ mailboxDir }) => {
    fs.writeFileSync(
      path.join(mailboxDir, 'state.json'),
      JSON.stringify({ node_secret: 'a'.repeat(64) }, null, 2)
    );
  });
  try {
    const env = {
      ...process.env,
      HOME: home,
      A2A_NODE_SECRET: 'c'.repeat(64),
      A2A_NODE_SECRET_VERSION: '3',
      EVOMAP_NODE_SECRET: 'd'.repeat(64),
      EVOMAP_NODE_SECRET_VERSION: '4',
    };
    const res = spawnSync(process.execPath, [INDEX_JS, 'reset-local-secret'], {
      env,
      encoding: 'utf8',
      timeout: 20_000,
    });
    assert.strictEqual(res.status, 0, `exit 0, stderr: ${res.stderr}`);
    assert.match(res.stdout, /Node secret env vars are still set/, 'should print stale-env warning');
    assert.match(res.stdout, /A2A_NODE_SECRET_VERSION/, 'should list version env vars');
    assert.match(
      res.stdout,
      /unset A2A_NODE_SECRET A2A_NODE_SECRET_VERSION EVOMAP_NODE_SECRET EVOMAP_NODE_SECRET_VERSION/,
      'should print full unset hint'
    );
  } finally {
    rmrf(home);
  }
});

test('reset-local-secret: idempotent on already-empty environment', () => {
  const home = makeFakeHome(() => { /* no files written */ });
  try {
    const cleanEnv = { ...process.env, HOME: home };
    deleteNodeSecretEnv(cleanEnv);
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
