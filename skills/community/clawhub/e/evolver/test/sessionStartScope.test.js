const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const path = require('path');
const fs = require('fs');
const os = require('os');
const { execFileSync, spawn } = require('child_process');

const repoRoot = path.resolve(__dirname, '..');
const scriptPath = path.join(repoRoot, 'src', 'adapters', 'scripts', 'evolver-session-start.js');

function makeTmpDir() {
  return fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-sstart-scope-')));
}
function cleanup(dir) {
  try { fs.rmSync(dir, { recursive: true, force: true }); } catch {}
}

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
    res.end(JSON.stringify({ status: 'running', proxy_protocol_version: '1.0.0' }));
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

// Build a memory graph file with the given entries (one JSON object per line).
function writeGraph(file, entries) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, entries.map(e => JSON.stringify(e)).join('\n') + '\n');
}

// A "good" recent successful outcome that passes filterRelevantOutcomes
// (status success, score >= 0.5, timestamped now), tagged with a workspace.
function outcome(note, { workspace_id, cwd } = {}) {
  const e = {
    timestamp: new Date().toISOString(),
    gene_id: 'ad_hoc',
    signals: ['stable_success_plateau'],
    outcome: { status: 'success', score: 0.8, note },
  };
  if (workspace_id !== undefined) e.workspace_id = workspace_id;
  if (cwd !== undefined) e.cwd = cwd;
  return e;
}

function runStart(env) {
  const out = execFileSync('node', [scriptPath], {
    env: { PATH: process.env.PATH, ...env },
    input: '{}',
    encoding: 'utf8',
    timeout: 15000,
  });
  try { return JSON.parse(out); } catch { return null; }
}

function baseEnv(extra) {
  return {
    HOME: extra.HOME,
    EVOLVER_ROOT: repoRoot,
    EVOLVER_SESSION_AUTO_RESTART: '0',
    // Force dedup off (default) so every run injects.
    EVOLVER_SESSION_START_DEDUP: '',
    ...extra,
  };
}

// Make a temp dir that is a real, self-owned git work tree, and return a
// CLAUDE_PROJECT_DIR pointing at it. Without this, the hook resolves a non-git
// (or dubious-ownership) project dir and prepends a one-time "not a git
// repository" notice — which breaks assertions that expect exact output. A
// freshly `git init`-ed temp dir is owned by the test process, so it passes
// `git rev-parse --is-inside-work-tree` even when the subprocess HOME lacks a
// safe.directory exception for the checkout.
function makeGitWorkspace() {
  const dir = makeTmpDir();
  execFileSync('git', ['init', '-q'], { cwd: dir });
  return dir;
}

describe('evolver-session-start workspace scoping', () => {
  it('injects only the current workspace\'s outcomes, not other projects\'', () => {
    const home = makeTmpDir();
    try {
      const graph = path.join(home, '.evolver', 'memory', 'evolution', 'memory_graph.jsonl');
      // 6 entries from "other" workspace, then 1 from "mine". A tail-5 read
      // would miss "mine" entirely; scope-first must surface it.
      const entries = [];
      for (let i = 0; i < 6; i++) entries.push(outcome(`other-${i}`, { workspace_id: 'ws-other' }));
      entries.push(outcome('mine-1', { workspace_id: 'ws-mine' }));
      writeGraph(graph, entries);

      const env = baseEnv({
        HOME: home,
        MEMORY_GRAPH_PATH: graph,
        EVOLVER_WORKSPACE_ID: 'ws-mine',
      });
      const result = runStart(env);
      assert.ok(result && typeof result.additionalContext === 'string',
        `expected an injection, got ${JSON.stringify(result)}`);
      assert.match(result.additionalContext, /mine-1/, 'must include current workspace outcome');
      assert.doesNotMatch(result.additionalContext, /other-/,
        'must NOT leak other workspace outcomes');
    } finally { cleanup(home); }
  });

  it('surfaces this workspace\'s recent entries even behind many newer other-workspace entries', () => {
    const home = makeTmpDir();
    try {
      const graph = path.join(home, '.evolver', 'memory', 'evolution', 'memory_graph.jsonl');
      // This workspace's entries come FIRST (older), then a large run of other-
      // workspace entries (newer). A tail-N read would see only 'other'; the
      // bounded scan-from-end must walk past them to collect ours — without
      // parsing being capped at N total (it stops at N *matches*, not N lines).
      const entries = [];
      entries.push(outcome('mine-old', { workspace_id: 'ws-mine' }));
      for (let i = 0; i < 200; i++) entries.push(outcome(`other-${i}`, { workspace_id: 'ws-other' }));
      entries.push(outcome('mine-new', { workspace_id: 'ws-mine' }));
      writeGraph(graph, entries);

      const env = baseEnv({ HOME: home, MEMORY_GRAPH_PATH: graph, EVOLVER_WORKSPACE_ID: 'ws-mine' });
      const result = runStart(env);
      assert.ok(result && typeof result.additionalContext === 'string',
        `expected an injection, got ${JSON.stringify(result)}`);
      assert.match(result.additionalContext, /mine-new/, 'most recent own entry must show');
      assert.doesNotMatch(result.additionalContext, /other-/, 'no other-workspace leak');
    } finally { cleanup(home); }
  });

  it('emits nothing when only other workspaces have outcomes', () => {
    // Use a real git workspace so the (incidental) non-git notice can't fire and
    // mask the actual assertion: only other-workspace outcomes exist, so the
    // hook must emit exactly nothing.
    const home = makeGitWorkspace();
    try {
      const graph = path.join(home, '.evolver', 'memory', 'evolution', 'memory_graph.jsonl');
      writeGraph(graph, [outcome('other', { workspace_id: 'ws-other' })]);
      const env = baseEnv({ HOME: home, MEMORY_GRAPH_PATH: graph, EVOLVER_WORKSPACE_ID: 'ws-mine', CLAUDE_PROJECT_DIR: home });
      const result = runStart(env);
      assert.deepEqual(result, {}, `expected empty (no own outcomes), got ${JSON.stringify(result)}`);
    } finally { cleanup(home); }
  });

  // belongsToWorkspace is the scoping predicate. Unit-test its branches
  // directly (deterministic) — the end-to-end tests above cover the wired path.
  describe('belongsToWorkspace predicate', () => {
    const {
      belongsToWorkspace,
      _isLoopbackProxyUrl,
      _proxyExpected,
      _proxyReachable,
      _proxyHealthyIfExpected,
    } = require('../src/adapters/scripts/evolver-session-start');

    it('unresolved current id -> tagged entries are NOT hidden (no regression)', () => {
      assert.equal(belongsToWorkspace({ workspace_id: 'ws-other' }, null, null), true);
    });
    it('resolved id -> exact match required', () => {
      assert.equal(belongsToWorkspace({ workspace_id: 'ws-mine' }, 'ws-mine', null), true);
      assert.equal(belongsToWorkspace({ workspace_id: 'ws-other' }, 'ws-mine', null), false);
    });
    it('untagged legacy entry -> always included', () => {
      assert.equal(belongsToWorkspace({}, 'ws-mine', '/some/dir'), true);
    });
    it('cwd fallback when no workspace_id', () => {
      assert.equal(belongsToWorkspace({ cwd: '/p' }, null, '/p'), true);
      assert.equal(belongsToWorkspace({ cwd: '/q' }, null, '/p'), false);
    });

    it('detects managed loopback proxy settings as proxy-required', () => {
      assert.equal(_isLoopbackProxyUrl('http://127.0.0.1:19820'), true);
      assert.equal(_isLoopbackProxyUrl('https://evomap.ai'), false);

      const prevBase = process.env.ANTHROPIC_BASE_URL;
      process.env.ANTHROPIC_BASE_URL = 'http://127.0.0.1:19820';
      try {
        assert.equal(_proxyExpected(), true);
      } finally {
        if (prevBase === undefined) delete process.env.ANTHROPIC_BASE_URL;
        else process.env.ANTHROPIC_BASE_URL = prevBase;
      }
    });

    it('detects selected Codex loopback provider config as proxy-required', () => {
      const tmp = makeTmpDir();
      const configFile = path.join(tmp, '.codex', 'config.toml');
      fs.mkdirSync(path.dirname(configFile), { recursive: true });
      fs.writeFileSync(configFile, [
        'model_provider = "evomap-proxy"',
        '',
        '[model_providers.evomap-proxy]',
        'base_url = "http://127.0.0.1:19820/v1"',
        'wire_api = "responses"',
        '',
      ].join('\n'), 'utf8');

      const saved = {
        CODEX_CONFIG_FILE: process.env.CODEX_CONFIG_FILE,
        EVOMAP_PROXY: process.env.EVOMAP_PROXY,
        A2A_TRANSPORT: process.env.A2A_TRANSPORT,
        EVOMAP_PROXY_URL: process.env.EVOMAP_PROXY_URL,
        ANTHROPIC_BASE_URL: process.env.ANTHROPIC_BASE_URL,
        CLAUDE_SETTINGS_FILE: process.env.CLAUDE_SETTINGS_FILE,
        EVOMAP_CLAUDE_SETTINGS_FILE: process.env.EVOMAP_CLAUDE_SETTINGS_FILE,
      };
      process.env.CODEX_CONFIG_FILE = configFile;
      delete process.env.EVOMAP_PROXY;
      delete process.env.A2A_TRANSPORT;
      delete process.env.EVOMAP_PROXY_URL;
      delete process.env.ANTHROPIC_BASE_URL;
      delete process.env.CLAUDE_SETTINGS_FILE;
      delete process.env.EVOMAP_CLAUDE_SETTINGS_FILE;
      try {
        assert.equal(_proxyExpected(), true);
      } finally {
        for (const [key, value] of Object.entries(saved)) {
          if (value === undefined) delete process.env[key];
          else process.env[key] = value;
        }
        cleanup(tmp);
      }
    });

    it('treats missing proxy settings as unhealthy when proxy is expected', () => {
      const prevBase = process.env.ANTHROPIC_BASE_URL;
      const prevDir = process.env.EVOLVER_SETTINGS_DIR;
      const tmp = makeTmpDir();
      process.env.ANTHROPIC_BASE_URL = 'http://127.0.0.1:19820';
      process.env.EVOLVER_SETTINGS_DIR = tmp;
      try {
        assert.equal(_proxyHealthyIfExpected(), false);
      } finally {
        if (prevBase === undefined) delete process.env.ANTHROPIC_BASE_URL;
        else process.env.ANTHROPIC_BASE_URL = prevBase;
        if (prevDir === undefined) delete process.env.EVOLVER_SETTINGS_DIR;
        else process.env.EVOLVER_SETTINGS_DIR = prevDir;
        cleanup(tmp);
      }
    });

    it('requires an authenticated Evolver proxy status response', async () => {
      const fixtureToken = 'fixture-proxy-token';
      const { child: authServer, url: authUrl } = await startStatusServer('auth', fixtureToken);
      try {
        assert.equal(_proxyReachable(authUrl, 'wrong-fixture-token'), false);
        assert.equal(_proxyReachable(authUrl, fixtureToken), true);
      } finally {
        await close(authServer);
      }

      const { child: nonProxyServer, url: nonProxyUrl } = await startStatusServer('non-proxy');
      try {
        assert.equal(_proxyReachable(nonProxyUrl, fixtureToken), false);
      } finally {
        await close(nonProxyServer);
      }
    });
  });

  it('passes through legacy entries that carry no workspace tag', () => {
    const home = makeTmpDir();
    try {
      const graph = path.join(home, '.evolver', 'memory', 'evolution', 'memory_graph.jsonl');
      // Untagged legacy entry (pre-hardening) + a tagged other-workspace one.
      writeGraph(graph, [outcome('legacy'), outcome('other', { workspace_id: 'ws-other' })]);
      const env = baseEnv({ HOME: home, MEMORY_GRAPH_PATH: graph, EVOLVER_WORKSPACE_ID: 'ws-mine' });
      const result = runStart(env);
      assert.ok(result && typeof result.additionalContext === 'string');
      assert.match(result.additionalContext, /legacy/, 'untagged legacy entries must not be hidden');
      assert.doesNotMatch(result.additionalContext, /other/, 'tagged other-workspace entry still excluded');
    } finally { cleanup(home); }
  });

  it('matches on cwd when an entry has cwd but no workspace_id', () => {
    const home = makeTmpDir();
    const projectDir = makeTmpDir();
    try {
      const graph = path.join(home, '.evolver', 'memory', 'evolution', 'memory_graph.jsonl');
      writeGraph(graph, [
        outcome('mine-cwd', { cwd: projectDir }),
        outcome('other-cwd', { cwd: path.join(projectDir, 'nope') }),
      ]);
      const env = baseEnv({
        HOME: home,
        MEMORY_GRAPH_PATH: graph,
        // id unresolved -> falls to cwd matching; point project dir at ours
        CURSOR_PROJECT_DIR: projectDir,
      });
      delete env.EVOLVER_WORKSPACE_ID;
      const result = runStart(env);
      // currentId is null here, so workspace_id-less entries are matched by cwd
      // only when currentId is null AND we have currentDir. Both entries lack
      // workspace_id; belongsToWorkspace falls to cwd compare against projectDir.
      assert.ok(result && typeof result.additionalContext === 'string');
      assert.match(result.additionalContext, /mine-cwd/);
      assert.doesNotMatch(result.additionalContext, /other-cwd/);
    } finally { cleanup(home); cleanup(projectDir); }
  });
});

describe('evolver-session-start non-git notice', () => {
  const { execFileSync: x } = require('child_process');
  const gitInit = (d) => x('git', ['init', '-q'], { cwd: d });

  it('surfaces a notice in a non-git folder (first time)', () => {
    const home = makeTmpDir(); const proj = makeTmpDir();
    try {
      const env = baseEnv({ HOME: home, CURSOR_PROJECT_DIR: proj,
        MEMORY_GRAPH_PATH: path.join(home, 'g.jsonl') });
      const r = runStart(env);
      assert.ok(r && typeof r.additionalContext === 'string', 'expected a notice');
      assert.match(r.additionalContext, /not a git repository/);
    } finally { cleanup(home); cleanup(proj); }
  });

  it('throttles the notice on the second run in the same folder', () => {
    const home = makeTmpDir(); const proj = makeTmpDir();
    try {
      const env = baseEnv({ HOME: home, CURSOR_PROJECT_DIR: proj,
        MEMORY_GRAPH_PATH: path.join(home, 'g.jsonl') });
      const first = runStart(env);
      assert.match(first.additionalContext, /not a git repository/);
      const second = runStart(env);
      assert.deepEqual(second, {}, 'second run within TTL must be silent');
    } finally { cleanup(home); cleanup(proj); }
  });

  it('does NOT show the notice in a git workspace', () => {
    const home = makeTmpDir(); const proj = makeTmpDir();
    try {
      gitInit(proj);
      const env = baseEnv({ HOME: home, CURSOR_PROJECT_DIR: proj,
        MEMORY_GRAPH_PATH: path.join(home, 'g.jsonl') });
      const r = runStart(env);
      // No memory + git repo -> empty; in any case never the non-git notice.
      if (r && r.additionalContext) {
        assert.doesNotMatch(r.additionalContext, /not a git repository/);
      }
    } finally { cleanup(home); cleanup(proj); }
  });

  it('shows BOTH the notice and memory when a non-git folder has cwd-tagged outcomes', () => {
    const home = makeTmpDir(); const proj = makeTmpDir();
    try {
      const graph = path.join(home, '.evolver', 'memory', 'evolution', 'memory_graph.jsonl');
      // cwd-tagged success outcome for this non-git folder (workspace_id null).
      writeGraph(graph, [outcome('nongit-mem', { cwd: proj })]);
      const env = baseEnv({ HOME: home, CURSOR_PROJECT_DIR: proj, MEMORY_GRAPH_PATH: graph });
      delete env.EVOLVER_WORKSPACE_ID;
      const r = runStart(env);
      assert.ok(r && typeof r.additionalContext === 'string');
      assert.match(r.additionalContext, /not a git repository/, 'notice present');
      assert.match(r.additionalContext, /nongit-mem/, 'memory still injected');
    } finally { cleanup(home); cleanup(proj); }
  });
});
