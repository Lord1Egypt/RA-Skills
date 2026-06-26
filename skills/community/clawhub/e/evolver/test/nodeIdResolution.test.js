// Tests for getNodeId resolution chain:
//   1. A2A_NODE_ID env (with format validation, warn on malformed but still use)
//   2. Persisted ~/.evomap/node_id (accepts 12-32 hex)
//   3. Project-local .evomap_node_id fallback
//   4. Random fallback (12 hex), persisted on first call
//
// Regression targets:
//   - NODE_ID_RE must accept 16-hex hub-issued IDs (was stuck at /{12}$/)
//   - When persisted file has valid 16-hex ID, do NOT overwrite with fallback
//   - Two installs with identical device fingerprint must produce different
//     IDs on first run (clone-collision fix, #71)
const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');

function freshRequire(id) {
  delete require.cache[require.resolve(id)];
  return require(id);
}

function withTempHome(run) {
  const tmpHome = fs.mkdtempSync(path.join(os.tmpdir(), 'evomap-nodeid-'));
  const originalHome = process.env.HOME;
  const originalUserProfile = process.env.USERPROFILE;
  process.env.HOME = tmpHome;
  process.env.USERPROFILE = tmpHome;

  // Also hide the project-local .evomap_node_id fallback so a pre-existing
  // file from a real run (where evolver was exercised in this checkout)
  // does not short-circuit _loadPersistedNodeId() and bypass the tmpHome
  // persist path under test. We stash it and restore in finally.
  const LOCAL_NODE_ID_FILE = path.resolve(__dirname, '..', '.evomap_node_id');
  const LOCAL_STASH = LOCAL_NODE_ID_FILE + '.test-stash';
  let stashed = false;
  try {
    if (fs.existsSync(LOCAL_NODE_ID_FILE)) {
      fs.renameSync(LOCAL_NODE_ID_FILE, LOCAL_STASH);
      stashed = true;
    }
  } catch { /* best effort */ }

  try {
    return run(tmpHome);
  } finally {
    if (originalHome === undefined) delete process.env.HOME;
    else process.env.HOME = originalHome;
    if (originalUserProfile === undefined) delete process.env.USERPROFILE;
    else process.env.USERPROFILE = originalUserProfile;
    try { fs.rmSync(tmpHome, { recursive: true, force: true }); } catch {}
    if (stashed) {
      try {
        // Clean any spurious node_id written during the test so restore wins.
        if (fs.existsSync(LOCAL_NODE_ID_FILE)) fs.rmSync(LOCAL_NODE_ID_FILE);
        fs.renameSync(LOCAL_STASH, LOCAL_NODE_ID_FILE);
      } catch { /* best effort */ }
    } else {
      // No pre-existing file, but test may have written one via the
      // LOCAL_NODE_ID_FILE fallback. Clean it up so we leave no trace.
      try { if (fs.existsSync(LOCAL_NODE_ID_FILE)) fs.rmSync(LOCAL_NODE_ID_FILE); } catch {}
    }
  }
}

describe('getNodeId resolution', () => {
  let savedEnv;

  beforeEach(() => {
    savedEnv = {
      A2A_NODE_ID: process.env.A2A_NODE_ID,
      AGENT_NAME: process.env.AGENT_NAME,
      EVOMAP_DEVICE_ID: process.env.EVOMAP_DEVICE_ID,
    };
    delete process.env.A2A_NODE_ID;
    delete process.env.AGENT_NAME;
    delete process.env.EVOMAP_DEVICE_ID;
  });

  afterEach(() => {
    for (const k of Object.keys(savedEnv)) {
      if (savedEnv[k] === undefined) delete process.env[k];
      else process.env[k] = savedEnv[k];
    }
  });

  it('returns A2A_NODE_ID env verbatim when format is valid (12 hex)', () => {
    process.env.A2A_NODE_ID = 'node_abcdef012345';
    const { getNodeId } = freshRequire('../src/gep/a2aProtocol');
    assert.equal(getNodeId(), 'node_abcdef012345');
  });

  it('returns A2A_NODE_ID env verbatim when format is valid (16 hex, hub-issued)', () => {
    process.env.A2A_NODE_ID = 'node_71c0a711a894cbf3';
    const { getNodeId } = freshRequire('../src/gep/a2aProtocol');
    assert.equal(getNodeId(), 'node_71c0a711a894cbf3');
  });

  it('accepts A2A_NODE_ID env with odd format but warns (does not crash)', () => {
    process.env.A2A_NODE_ID = 'test-node';
    const warns = [];
    const origWarn = console.warn;
    console.warn = (msg) => warns.push(String(msg));
    try {
      const { getNodeId } = freshRequire('../src/gep/a2aProtocol');
      assert.equal(getNodeId(), 'test-node');
      assert.ok(warns.some((m) => m.includes('unexpected format')), 'should warn');
    } finally {
      console.warn = origWarn;
    }
  });

  it('loads persisted 12-hex node_id from ~/.evomap/node_id', () => {
    withTempHome((tmpHome) => {
      const dir = path.join(tmpHome, '.evomap');
      fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
      fs.writeFileSync(path.join(dir, 'node_id'), 'node_112233445566', 'utf8');
      const { getNodeId } = freshRequire('../src/gep/a2aProtocol');
      assert.equal(getNodeId(), 'node_112233445566');
    });
  });

  it('loads persisted 16-hex node_id from ~/.evomap/node_id (hub-issued format, regression fix)', () => {
    withTempHome((tmpHome) => {
      const dir = path.join(tmpHome, '.evomap');
      fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
      fs.writeFileSync(path.join(dir, 'node_id'), 'node_71c0a711a894cbf3', 'utf8');
      const { getNodeId } = freshRequire('../src/gep/a2aProtocol');
      assert.equal(getNodeId(), 'node_71c0a711a894cbf3',
        'Must not discard valid 16-hex node_id and regenerate a 12-hex fallback');
    });
  });

  it('rejects obviously malformed persisted value and falls back to a fresh random id', () => {
    withTempHome((tmpHome) => {
      const dir = path.join(tmpHome, '.evomap');
      fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
      fs.writeFileSync(path.join(dir, 'node_id'), 'not-a-valid-id', 'utf8');
      const { getNodeId } = freshRequire('../src/gep/a2aProtocol');
      const id = getNodeId();
      assert.match(id, /^node_[a-f0-9]{12}$/, 'fallback should be 12-hex');
    });
  });

  it('fallback writes 12-hex node_id to ~/.evomap/node_id and is stable across repeated calls', () => {
    withTempHome((tmpHome) => {
      const mod1 = freshRequire('../src/gep/a2aProtocol');
      const first = mod1.getNodeId();
      assert.match(first, /^node_[a-f0-9]{12}$/);

      const persistedPath = path.join(tmpHome, '.evomap', 'node_id');
      assert.ok(fs.existsSync(persistedPath), 'fallback should persist node_id');
      assert.equal(fs.readFileSync(persistedPath, 'utf8').trim(), first);

      const mod2 = freshRequire('../src/gep/a2aProtocol');
      assert.equal(mod2.getNodeId(), first, 'second process should reuse persisted id');
    });
  });

  it('two installs with identical device fingerprint produce different node ids (clone-collision fix)', () => {
    // Simulate: a container image is built and cloned to two hosts before
    // evolver has ever run. Both hosts inherit the same hostname / MAC /
    // agent name / cwd. The deterministic hash would have collided; the
    // random fallback must not.
    const ids = [];
    for (let i = 0; i < 2; i++) {
      withTempHome(() => {
        process.env.EVOMAP_DEVICE_ID = 'a'.repeat(32);
        process.env.AGENT_NAME = 'default';
        const { getNodeId } = freshRequire('../src/gep/a2aProtocol');
        ids.push(getNodeId());
      });
    }
    assert.match(ids[0], /^node_[a-f0-9]{12}$/);
    assert.match(ids[1], /^node_[a-f0-9]{12}$/);
    assert.notEqual(ids[0], ids[1], 'identical fingerprint must not yield identical node id');
  });
});
