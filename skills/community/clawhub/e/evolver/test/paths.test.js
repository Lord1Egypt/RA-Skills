const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');

function freshRequire(modulePath) {
  const resolved = require.resolve(modulePath);
  delete require.cache[resolved];
  return require(resolved);
}

function canonicalPath(value) {
  const resolved = path.resolve(value);
  try {
    return fs.realpathSync.native(resolved);
  } catch {
    try { return fs.realpathSync(resolved); } catch { return resolved; }
  }
}

function assertPathEqual(actual, expected, message) {
  assert.equal(canonicalPath(actual), canonicalPath(expected), message);
}

describe('getRepoRoot', () => {
  let tmpDir;
  const savedEnv = {};
  const envKeys = [
    'EVOLVER_REPO_ROOT', 'EVOLVER_USE_PARENT_GIT', 'EVOLVER_NO_PARENT_GIT',
    'EVOLVER_QUIET_PARENT_GIT',
    'OPENCLAW_WORKSPACE', 'MEMORY_DIR', 'EVOLUTION_DIR', 'GEP_ASSETS_DIR',
  ];

  beforeEach(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'paths-test-'));
    for (const k of envKeys) {
      savedEnv[k] = process.env[k];
      delete process.env[k];
    }
    process.env.EVOLVER_QUIET_PARENT_GIT = '1';
  });

  afterEach(() => {
    for (const k of envKeys) {
      if (savedEnv[k] === undefined) delete process.env[k];
      else process.env[k] = savedEnv[k];
    }
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  it('returns EVOLVER_REPO_ROOT when set', () => {
    process.env.EVOLVER_REPO_ROOT = tmpDir;
    const { getRepoRoot } = freshRequire('../src/gep/paths');
    assert.equal(getRepoRoot(), tmpDir);
  });

  // When CWD is inside the evolver repo itself (e.g. running tests),
  // the CWD walk finds the same .git as ownDir — both resolve to the
  // evolver repo.
  it('returns own directory when CWD is inside the evolver repo', () => {
    const ownDir = path.resolve(__dirname, '..');
    const { getRepoRoot } = freshRequire('../src/gep/paths');
    delete process.env.EVOLVER_REPO_ROOT;
    const result = getRepoRoot();
    assert.ok(typeof result === 'string' && result.length > 0);
    assert.equal(result, ownDir);
  });

  // CWD git repo takes precedence over evolver's own .git (the fix for
  // global installs where evolver happens to have .git but the user ran
  // it from a different project).
  it('prefers CWD git repo over evolver own .git', () => {
    // Simulate a global install that has .git (e.g. npm install from git).
    const globalDir = fs.mkdtempSync(path.join(os.tmpdir(), 'global-pkg-'));
    fs.mkdirSync(path.join(globalDir, '.git'));
    const fakeGepDir = path.join(globalDir, 'src', 'gep');
    fs.mkdirSync(fakeGepDir, { recursive: true });
    const pathsSrc = fs.readFileSync(
      path.resolve(__dirname, '..', 'src', 'gep', 'paths.js'),
      'utf8'
    );
    fs.writeFileSync(path.join(fakeGepDir, 'paths.js'), pathsSrc);

    // Create a separate user project with .git.
    const projectDir = fs.mkdtempSync(path.join(os.tmpdir(), 'project-'));
    fs.mkdirSync(path.join(projectDir, '.git'));

    const resolved = require.resolve(path.join(fakeGepDir, 'paths.js'));
    delete require.cache[resolved];
    const mod = require(resolved);

    const origCwd = process.cwd;
    process.cwd = () => projectDir;
    try {
      // CWD project should win over evolver's own .git.
      assert.equal(mod.getRepoRoot(), projectDir);
    } finally {
      process.cwd = origCwd;
      delete require.cache[resolved];
      fs.rmSync(globalDir, { recursive: true, force: true });
      fs.rmSync(projectDir, { recursive: true, force: true });
    }
  });

  it('EVOLVER_REPO_ROOT takes precedence over .git detection', () => {
    process.env.EVOLVER_REPO_ROOT = tmpDir;
    const { getRepoRoot } = freshRequire('../src/gep/paths');
    assert.equal(getRepoRoot(), tmpDir);
  });

  // Regression guard for 1.69.6:
  // When evolver is installed as an npm dependency or a skill (no .git in
  // its own directory), it MUST auto-detect the host workspace's .git so
  // that git diff can see Hand Agent edits. Before 1.69.6 the default was
  // to ignore the parent git, which caused hollow_commit failures on every
  // evolution cycle for npm-installed users.
  it('auto-detects parent .git when own directory has none', () => {
    const host = fs.mkdtempSync(path.join(os.tmpdir(), 'host-git-'));
    fs.mkdirSync(path.join(host, '.git'));
    // Simulate evolver living under node_modules/@scope/pkg/src/gep.
    const fakeGepDir = path.join(host, 'node_modules', '@evomap', 'evolver', 'src', 'gep');
    fs.mkdirSync(fakeGepDir, { recursive: true });
    const pathsSrc = fs.readFileSync(
      path.resolve(__dirname, '..', 'src', 'gep', 'paths.js'),
      'utf8'
    );
    fs.writeFileSync(path.join(fakeGepDir, 'paths.js'), pathsSrc);

    const resolved = require.resolve(path.join(fakeGepDir, 'paths.js'));
    delete require.cache[resolved];
    const mod = require(resolved);

    // The CWD walk must also point inside the host tree so it doesn't
    // find the real evolver repo on disk before the ownDir walk runs.
    const origCwd = process.cwd;
    process.cwd = () => path.join(host, 'node_modules', '@evomap', 'evolver');
    try {
      assert.equal(mod.getRepoRoot(), host);
    } finally {
      process.cwd = origCwd;
      delete require.cache[resolved];
      fs.rmSync(host, { recursive: true, force: true });
    }
  });

  it('respects EVOLVER_NO_PARENT_GIT=true as opt-out', () => {
    const host = fs.mkdtempSync(path.join(os.tmpdir(), 'host-git-'));
    fs.mkdirSync(path.join(host, '.git'));
    const fakeGepDir = path.join(host, 'node_modules', '@evomap', 'evolver', 'src', 'gep');
    fs.mkdirSync(fakeGepDir, { recursive: true });
    const pathsSrc = fs.readFileSync(
      path.resolve(__dirname, '..', 'src', 'gep', 'paths.js'),
      'utf8'
    );
    fs.writeFileSync(path.join(fakeGepDir, 'paths.js'), pathsSrc);

    process.env.EVOLVER_NO_PARENT_GIT = 'true';
    const resolved = require.resolve(path.join(fakeGepDir, 'paths.js'));
    delete require.cache[resolved];
    const { getRepoRoot } = require(resolved);
    // Opt-out: should fall back to ownDir (the fake package root), NOT host.
    const ownDir = path.resolve(fakeGepDir, '..', '..');
    assertPathEqual(getRepoRoot(), ownDir);

    delete require.cache[resolved];
    fs.rmSync(host, { recursive: true, force: true });
  });

  it('legacy EVOLVER_USE_PARENT_GIT=false still opts out', () => {
    const host = fs.mkdtempSync(path.join(os.tmpdir(), 'host-git-'));
    fs.mkdirSync(path.join(host, '.git'));
    const fakeGepDir = path.join(host, 'node_modules', '@evomap', 'evolver', 'src', 'gep');
    fs.mkdirSync(fakeGepDir, { recursive: true });
    const pathsSrc = fs.readFileSync(
      path.resolve(__dirname, '..', 'src', 'gep', 'paths.js'),
      'utf8'
    );
    fs.writeFileSync(path.join(fakeGepDir, 'paths.js'), pathsSrc);

    process.env.EVOLVER_USE_PARENT_GIT = 'false';
    const resolved = require.resolve(path.join(fakeGepDir, 'paths.js'));
    delete require.cache[resolved];
    const { getRepoRoot } = require(resolved);
    const ownDir = path.resolve(fakeGepDir, '..', '..');
    assertPathEqual(getRepoRoot(), ownDir);

    delete require.cache[resolved];
    fs.rmSync(host, { recursive: true, force: true });
  });

  // Regression guard for #526:
  // .env loading in index.js happens AFTER a first getRepoRoot() call
  // (used to locate the .env file). If EVOLVER_REPO_ROOT is set only by
  // that .env, we must re-read process.env on subsequent calls and
  // override the earlier .git-walk result. Caching the pre-dotenv value
  // would silently ignore the user's explicit override.
  it('honors EVOLVER_REPO_ROOT set AFTER an earlier getRepoRoot() call', () => {
    const host = fs.mkdtempSync(path.join(os.tmpdir(), 'host-git-'));
    fs.mkdirSync(path.join(host, '.git'));
    const override = fs.mkdtempSync(path.join(os.tmpdir(), 'override-root-'));

    const origCwd = process.cwd;
    process.cwd = () => host;
    try {
      const { getRepoRoot } = freshRequire('../src/gep/paths');
      // First call: no EVOLVER_REPO_ROOT -> finds host via .git walk.
      assert.equal(getRepoRoot(), host);
      // Simulate .env being loaded now and setting the override.
      process.env.EVOLVER_REPO_ROOT = override;
      // Second call must reflect the new env, not the cached value.
      assert.equal(getRepoRoot(), override);
    } finally {
      process.cwd = origCwd;
      fs.rmSync(host, { recursive: true, force: true });
      fs.rmSync(override, { recursive: true, force: true });
    }
  });
});

describe('getSessionScope', () => {
  let saved;

  beforeEach(() => {
    saved = process.env.EVOLVER_SESSION_SCOPE;
    delete process.env.EVOLVER_SESSION_SCOPE;
  });

  afterEach(() => {
    if (saved === undefined) delete process.env.EVOLVER_SESSION_SCOPE;
    else process.env.EVOLVER_SESSION_SCOPE = saved;
  });

  it('returns null when not set', () => {
    const { getSessionScope } = freshRequire('../src/gep/paths');
    assert.equal(getSessionScope(), null);
  });

  it('returns null for empty string', () => {
    process.env.EVOLVER_SESSION_SCOPE = '';
    const { getSessionScope } = freshRequire('../src/gep/paths');
    assert.equal(getSessionScope(), null);
  });

  it('returns null for whitespace-only', () => {
    process.env.EVOLVER_SESSION_SCOPE = '   ';
    const { getSessionScope } = freshRequire('../src/gep/paths');
    assert.equal(getSessionScope(), null);
  });

  it('returns sanitized value for valid scope', () => {
    process.env.EVOLVER_SESSION_SCOPE = 'channel-123';
    const { getSessionScope } = freshRequire('../src/gep/paths');
    assert.equal(getSessionScope(), 'channel-123');
  });

  it('sanitizes special characters', () => {
    process.env.EVOLVER_SESSION_SCOPE = 'my/scope\\with:bad*chars';
    const { getSessionScope } = freshRequire('../src/gep/paths');
    const result = getSessionScope();
    assert.ok(result);
    assert.ok(!/[\/\\:*]/.test(result), 'should not contain path-unsafe characters');
  });

  it('rejects path traversal attempts', () => {
    process.env.EVOLVER_SESSION_SCOPE = '..';
    const { getSessionScope } = freshRequire('../src/gep/paths');
    assert.equal(getSessionScope(), null);
  });

  it('rejects embedded path traversal', () => {
    process.env.EVOLVER_SESSION_SCOPE = 'foo..bar';
    const { getSessionScope } = freshRequire('../src/gep/paths');
    assert.equal(getSessionScope(), null);
  });

  it('truncates to 128 characters', () => {
    process.env.EVOLVER_SESSION_SCOPE = 'a'.repeat(200);
    const { getSessionScope } = freshRequire('../src/gep/paths');
    const result = getSessionScope();
    assert.ok(result);
    assert.ok(result.length <= 128);
  });
});

describe('getEvolutionDir', () => {
  let saved = {};
  const envKeys = ['EVOLUTION_DIR', 'EVOLVER_SESSION_SCOPE', 'MEMORY_DIR', 'OPENCLAW_WORKSPACE', 'EVOLVER_REPO_ROOT'];

  beforeEach(() => {
    for (const k of envKeys) { saved[k] = process.env[k]; delete process.env[k]; }
  });

  afterEach(() => {
    for (const k of envKeys) {
      if (saved[k] === undefined) delete process.env[k];
      else process.env[k] = saved[k];
    }
  });

  it('returns EVOLUTION_DIR when set', () => {
    process.env.EVOLUTION_DIR = '/custom/evo';
    const { getEvolutionDir } = freshRequire('../src/gep/paths');
    assert.equal(getEvolutionDir(), '/custom/evo');
  });

  it('appends scope subdirectory when session scope is set', () => {
    process.env.EVOLUTION_DIR = '/custom/evo';
    process.env.EVOLVER_SESSION_SCOPE = 'test-scope';
    const { getEvolutionDir } = freshRequire('../src/gep/paths');
    const result = getEvolutionDir();
    assert.ok(result.includes('scopes'));
    assert.ok(result.includes('test-scope'));
  });

  it('returns base dir when no scope set', () => {
    process.env.EVOLUTION_DIR = '/custom/evo';
    const { getEvolutionDir } = freshRequire('../src/gep/paths');
    assert.equal(getEvolutionDir(), '/custom/evo');
    assert.ok(!getEvolutionDir().includes('scopes'));
  });
});

describe('getGepAssetsDir', () => {
  let saved = {};
  let tmpDir;
  const envKeys = ['GEP_ASSETS_DIR', 'EVOLVER_SESSION_SCOPE', 'EVOLVER_REPO_ROOT', 'OPENCLAW_WORKSPACE'];

  beforeEach(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'gep-assets-dir-test-'));
    for (const k of envKeys) { saved[k] = process.env[k]; delete process.env[k]; }
  });

  afterEach(() => {
    for (const k of envKeys) {
      if (saved[k] === undefined) delete process.env[k];
      else process.env[k] = saved[k];
    }
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  it('returns GEP_ASSETS_DIR when set', () => {
    process.env.GEP_ASSETS_DIR = '/custom/assets';
    const { getGepAssetsDir } = freshRequire('../src/gep/paths');
    assert.equal(getGepAssetsDir(), '/custom/assets');
  });

  it('defaults runtime assets to the workspace .evolver/gep directory', () => {
    process.env.OPENCLAW_WORKSPACE = tmpDir;
    const { getGepAssetsDir } = freshRequire('../src/gep/paths');
    assert.equal(getGepAssetsDir(), path.join(tmpDir, '.evolver', 'gep'));
  });

  it('appends scope subdirectory when session scope is set', () => {
    process.env.GEP_ASSETS_DIR = '/custom/assets';
    process.env.EVOLVER_SESSION_SCOPE = 'my-project';
    const { getGepAssetsDir } = freshRequire('../src/gep/paths');
    const result = getGepAssetsDir();
    assert.ok(result.includes('scopes'));
    assert.ok(result.includes('my-project'));
  });
});

describe('getWorkspaceRoot', () => {
  let saved = {};
  let tmpDir;
  const envKeys = ['OPENCLAW_WORKSPACE', 'EVOLVER_REPO_ROOT'];

  beforeEach(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'ws-test-'));
    for (const k of envKeys) { saved[k] = process.env[k]; delete process.env[k]; }
  });

  afterEach(() => {
    for (const k of envKeys) {
      if (saved[k] === undefined) delete process.env[k];
      else process.env[k] = saved[k];
    }
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  it('returns OPENCLAW_WORKSPACE when set', () => {
    process.env.OPENCLAW_WORKSPACE = '/my/workspace';
    const { getWorkspaceRoot } = freshRequire('../src/gep/paths');
    assert.equal(getWorkspaceRoot(), '/my/workspace');
  });

  it('returns a string when no env vars set', () => {
    const { getWorkspaceRoot } = freshRequire('../src/gep/paths');
    const result = getWorkspaceRoot();
    assert.ok(typeof result === 'string' && result.length > 0);
  });

  it('returns repoRoot when no workspace/ dir exists (standalone/Cursor fix)', () => {
    process.env.EVOLVER_REPO_ROOT = tmpDir;
    const { getWorkspaceRoot, getRepoRoot } = freshRequire('../src/gep/paths');
    assert.equal(getWorkspaceRoot(), getRepoRoot());
  });

  it('does NOT resolve to a directory above repoRoot', () => {
    process.env.EVOLVER_REPO_ROOT = tmpDir;
    const { getWorkspaceRoot } = freshRequire('../src/gep/paths');
    const wsRoot = getWorkspaceRoot();
    assert.ok(
      wsRoot.startsWith(tmpDir),
      'workspaceRoot should be at or below repoRoot, got: ' + wsRoot
    );
  });

  it('returns workspace/ subdirectory when it exists inside repoRoot', () => {
    process.env.EVOLVER_REPO_ROOT = tmpDir;
    const wsDir = path.join(tmpDir, 'workspace');
    fs.mkdirSync(wsDir);
    const { getWorkspaceRoot } = freshRequire('../src/gep/paths');
    assert.equal(getWorkspaceRoot(), wsDir);
  });

  it('OPENCLAW_WORKSPACE takes precedence over workspace/ dir', () => {
    process.env.EVOLVER_REPO_ROOT = tmpDir;
    process.env.OPENCLAW_WORKSPACE = '/override/path';
    fs.mkdirSync(path.join(tmpDir, 'workspace'));
    const { getWorkspaceRoot } = freshRequire('../src/gep/paths');
    assert.equal(getWorkspaceRoot(), '/override/path');
  });

  it('derived paths (memoryDir, logsDir, skillsDir) resolve under workspaceRoot', () => {
    process.env.EVOLVER_REPO_ROOT = tmpDir;
    const { getWorkspaceRoot, getMemoryDir, getLogsDir, getSkillsDir } = freshRequire('../src/gep/paths');
    const ws = getWorkspaceRoot();
    assert.ok(getMemoryDir().startsWith(ws), 'memoryDir should be under workspaceRoot');
    assert.ok(getLogsDir().startsWith(ws), 'logsDir should be under workspaceRoot');
    assert.ok(getSkillsDir().startsWith(ws), 'skillsDir should be under workspaceRoot');
  });
});

describe('getAgentSessionsDir', () => {
  const savedEnv = {};
  const envKeys = ['AGENT_SESSIONS_DIR', 'AGENT_NAME', 'EVOLVER_SESSION_SCOPE', 'HOME'];

  beforeEach(() => {
    for (const k of envKeys) {
      savedEnv[k] = process.env[k];
      delete process.env[k];
    }
  });

  afterEach(() => {
    for (const k of envKeys) {
      if (savedEnv[k] === undefined) delete process.env[k];
      else process.env[k] = savedEnv[k];
    }
  });

  it('respects AGENT_SESSIONS_DIR override', () => {
    process.env.AGENT_SESSIONS_DIR = '/tmp/override/sessions';
    const { getAgentSessionsDir } = freshRequire('../src/gep/paths');
    assert.equal(getAgentSessionsDir(), '/tmp/override/sessions');
  });

  it('derives agent name from workspace-<name> scope', () => {
    process.env.HOME = '/tmp/home';
    process.env.EVOLVER_SESSION_SCOPE = 'workspace-helperclaw';
    const { getAgentSessionsDir } = freshRequire('../src/gep/paths');
    assert.equal(
      getAgentSessionsDir(),
      path.join('/tmp/home', '.openclaw', 'agents', 'helperclaw', 'sessions'),
    );
  });

  it('falls back to AGENT_NAME when scope has no workspace- prefix', () => {
    process.env.HOME = '/tmp/home';
    process.env.EVOLVER_SESSION_SCOPE = 'channel-123';
    process.env.AGENT_NAME = 'custom-agent';
    const { getAgentSessionsDir } = freshRequire('../src/gep/paths');
    assert.equal(
      getAgentSessionsDir(),
      path.join('/tmp/home', '.openclaw', 'agents', 'custom-agent', 'sessions'),
    );
  });

  it('defaults to main agent when neither scope nor AGENT_NAME is set', () => {
    process.env.HOME = '/tmp/home';
    const { getAgentSessionsDir } = freshRequire('../src/gep/paths');
    assert.equal(
      getAgentSessionsDir(),
      path.join('/tmp/home', '.openclaw', 'agents', 'main', 'sessions'),
    );
  });
});

describe('readSessionCwdFromHead', () => {
  let tmpDir;

  beforeEach(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'session-head-'));
  });

  afterEach(() => {
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  it('extracts cwd from the first record', () => {
    const file = path.join(tmpDir, 'session.jsonl');
    const header = JSON.stringify({
      type: 'session_start',
      cwd: '/Users/test/workspaces/helperclaw',
      id: 'c982d748',
    });
    const body = JSON.stringify({ type: 'user', text: 'hello' });
    fs.writeFileSync(file, header + '\n' + body + '\n');
    const { readSessionCwdFromHead } = freshRequire('../src/gep/paths');
    assert.equal(readSessionCwdFromHead(file), '/Users/test/workspaces/helperclaw');
  });

  it('returns null when the header has no cwd field', () => {
    const file = path.join(tmpDir, 'session.jsonl');
    fs.writeFileSync(file, JSON.stringify({ type: 'session_start' }) + '\n');
    const { readSessionCwdFromHead } = freshRequire('../src/gep/paths');
    assert.equal(readSessionCwdFromHead(file), null);
  });

  it('returns null when the file does not exist', () => {
    const { readSessionCwdFromHead } = freshRequire('../src/gep/paths');
    assert.equal(readSessionCwdFromHead(path.join(tmpDir, 'missing.jsonl')), null);
  });

  it('returns null when the first line is not valid JSON', () => {
    const file = path.join(tmpDir, 'session.jsonl');
    fs.writeFileSync(file, 'not-json\n{"type":"user"}\n');
    const { readSessionCwdFromHead } = freshRequire('../src/gep/paths');
    assert.equal(readSessionCwdFromHead(file), null);
  });

  it('caps read size to the configured maxBytes', () => {
    const file = path.join(tmpDir, 'session.jsonl');
    const header = JSON.stringify({ type: 'session_start', cwd: '/ok', pad: 'x'.repeat(2048) });
    fs.writeFileSync(file, header + '\n');
    const { readSessionCwdFromHead } = freshRequire('../src/gep/paths');
    // default 800-byte cap means the JSON slice won't parse; helper returns null
    assert.equal(readSessionCwdFromHead(file), null);
    // large enough cap recovers cwd
    assert.equal(readSessionCwdFromHead(file, 4096), '/ok');
  });
});

// ---------------------------------------------------------------------------
// #541 — getRepoRoot must not escape `node_modules` when walking upward from
// the evolver install. On macOS with Homebrew, the global install lives at
// `/opt/homebrew/lib/node_modules/@evomap/evolver` and `/opt/homebrew` is
// itself a git repo, so an unbounded upward walk used to resolve repoRoot
// to `/opt/homebrew` for any user who didn't `cd` into a git project first.
//
// These tests can't reuse the in-process `freshRequire('../src/gep/paths')`
// trick because that path's `__dirname` is always the real repo's
// `src/gep/`. We have to copy paths.js into a fake `node_modules` install
// layout and spawn a child node process so its `__dirname` lands inside the
// boundary we want to verify.
// ---------------------------------------------------------------------------
describe('getRepoRoot node_modules boundary (#541)', () => {
  const { spawnSync } = require('child_process');

  function setupFakeGlobalInstall() {
    // Layout mirroring `npm install -g @evomap/evolver` on macOS Homebrew:
    //   <root>/.git/                                        ← outer git that
    //                                                         must NOT be picked
    //   <root>/lib/node_modules/@evomap/evolver/             ← fake install
    //   <root>/lib/node_modules/@evomap/evolver/src/gep/paths.js
    const root = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-541-global-'));
    fs.mkdirSync(path.join(root, '.git'));
    const installDir = path.join(root, 'lib', 'node_modules', '@evomap', 'evolver');
    const gepDir = path.join(installDir, 'src', 'gep');
    fs.mkdirSync(gepDir, { recursive: true });
    fs.copyFileSync(
      path.resolve(__dirname, '..', 'src', 'gep', 'paths.js'),
      path.join(gepDir, 'paths.js')
    );
    return { root, installDir };
  }

  function setupFakeLocalInstall() {
    // Layout mirroring local `npm install @evomap/evolver` in a user project:
    //   <root>/.git/                                        ← user's project git
    //   <root>/node_modules/@evomap/evolver/                ← fake install
    //   <root>/node_modules/@evomap/evolver/src/gep/paths.js
    // Here we DO want the walk to find <root>/.git.
    const root = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-541-local-'));
    fs.mkdirSync(path.join(root, '.git'));
    const installDir = path.join(root, 'node_modules', '@evomap', 'evolver');
    const gepDir = path.join(installDir, 'src', 'gep');
    fs.mkdirSync(gepDir, { recursive: true });
    fs.copyFileSync(
      path.resolve(__dirname, '..', 'src', 'gep', 'paths.js'),
      path.join(gepDir, 'paths.js')
    );
    return { root, installDir };
  }

  function runGetRepoRootIn(installDir, cwd) {
    const script = `
      const { getRepoRoot } = require(${JSON.stringify(path.join(installDir, 'src', 'gep', 'paths.js'))});
      process.stdout.write(getRepoRoot());
    `;
    const env = { ...process.env };
    // Strip env that would short-circuit the upward walk we want to exercise.
    delete env.EVOLVER_REPO_ROOT;
    delete env.EVOLVER_USE_PARENT_GIT;
    delete env.EVOLVER_NO_PARENT_GIT;
    env.EVOLVER_QUIET_PARENT_GIT = '1';
    const res = spawnSync(process.execPath, ['-e', script], { cwd, env, encoding: 'utf8' });
    if (res.status !== 0) {
      throw new Error(`child failed: ${res.stderr || res.stdout}`);
    }
    return res.stdout;
  }

  it('global-install layout: does not escape past node_modules to outer .git', () => {
    const { root, installDir } = setupFakeGlobalInstall();
    // cwd is an isolated empty tmp dir with no `.git` anywhere up — guarantees
    // step 2 (cwd walk) returns nothing, so the test actually exercises step 3.
    const cwd = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-541-cwd-'));
    try {
      const resolved = runGetRepoRootIn(installDir, cwd);
      // #541 invariant: must NOT escape node_modules to the host .git at root.
      assert.notEqual(canonicalPath(resolved), canonicalPath(root),
        `regressed: walk escaped node_modules and picked outer .git at ${root}`);
      // #580 Bug 2: on a no-opt-out global install where no .git is found,
      // the fallback is now process.cwd() (where the user stands and should
      // `git init`), NOT the npm install dir. Still satisfies the #541
      // no-escape invariant above.
      assertPathEqual(resolved, cwd);
      assert.notEqual(canonicalPath(resolved), canonicalPath(installDir),
        'fallback must no longer be the npm install dir (#580 Bug 2)');
    } finally {
      fs.rmSync(root, { recursive: true, force: true });
      fs.rmSync(cwd, { recursive: true, force: true });
    }
  });

  it('local-install layout: still finds the user project .git just above node_modules', () => {
    const { root, installDir } = setupFakeLocalInstall();
    const cwd = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-541-cwd-'));
    try {
      const resolved = runGetRepoRootIn(installDir, cwd);
      // The boundary INCLUDES the parent of node_modules (i.e. the user's
      // project), so <root>/.git is reachable and must be picked.
      assertPathEqual(resolved, root,
        `regression: local install no longer finds the project's own .git`);
    } finally {
      fs.rmSync(root, { recursive: true, force: true });
      fs.rmSync(cwd, { recursive: true, force: true });
    }
  });

  it('reporter verify snippet: cwd INSIDE the install dir must not escape via cwd walk', () => {
    // The pre-fix step-3 boundary alone did not cover this case: the
    // reporter's exact reproduction (#541) did `cd` into the global
    // install dir before running, which made the cwd walk (step 2) find
    // `/opt/homebrew/.git` BEFORE the bounded step-3 walk could run.
    // Step 2 now applies the same node_modules boundary.
    const { root, installDir } = setupFakeGlobalInstall();
    try {
      // cwd == install dir, NOT an isolated tmp dir. Reproduces:
      //   cd /opt/homebrew/lib/node_modules/@evomap/evolver && evolver ...
      const resolved = runGetRepoRootIn(installDir, installDir);
      assert.notEqual(canonicalPath(resolved), canonicalPath(root),
        `regression: cwd walk escaped node_modules and picked outer .git at ${root}`);
      assertPathEqual(resolved, installDir);
    } finally {
      fs.rmSync(root, { recursive: true, force: true });
    }
  });

  it('#580: global install + no git anywhere falls back to cwd, not the npm install dir', () => {
    // The reporter's exact case: `npm i -g @evomap/evolver`, then run from a
    // non-git working directory. No outer .git exists (unlike the Homebrew
    // #541 layout). Pre-fix getRepoRoot fell back to the install dir
    // (<prefix>/node_modules/@evomap/evolver), so the daemon FATAL'd telling
    // the user to `git init` inside the global install dir. The fallback must
    // now be cwd (where the user stands and should actually `git init`).
    const installRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-580-install-'));
    const installDir = path.join(installRoot, 'node_modules', '@evomap', 'evolver');
    const gepDir = path.join(installDir, 'src', 'gep');
    fs.mkdirSync(gepDir, { recursive: true });
    fs.copyFileSync(
      path.resolve(__dirname, '..', 'src', 'gep', 'paths.js'),
      path.join(gepDir, 'paths.js')
    );
    // A user working directory with NO .git anywhere up the tree.
    const userDir = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-580-userdir-'));
    try {
      const resolved = runGetRepoRootIn(installDir, userDir);
      assertPathEqual(resolved, userDir);
      assert.notEqual(canonicalPath(resolved), canonicalPath(installDir),
        'fallback must NOT be the npm install dir (the original #580 bug)');
    } finally {
      fs.rmSync(installRoot, { recursive: true, force: true });
      fs.rmSync(userDir, { recursive: true, force: true });
    }
  });

  it('cwd inside a user-project node_modules sub-dir still resolves to the project root', () => {
    // Real-world case: user `cd`s into `<their-project>/node_modules/lodash`
    // (or any sub-dir of their project's node_modules). The boundary
    // includes the parent of node_modules, so the walk must still find
    // `<their-project>/.git`. Verifies the cwd-walk boundary doesn't
    // over-correct.
    const { root, installDir } = setupFakeLocalInstall();
    // Create a sibling package dir under the same node_modules to cd into.
    const sibling = path.join(root, 'node_modules', 'lodash');
    fs.mkdirSync(sibling, { recursive: true });
    try {
      const resolved = runGetRepoRootIn(installDir, sibling);
      assertPathEqual(resolved, root,
        `regression: user cd'd into project's node_modules sub-dir no longer finds the project root`);
    } finally {
      fs.rmSync(root, { recursive: true, force: true });
    }
  });
});
