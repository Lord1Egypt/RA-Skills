'use strict';
const { describe, it, before, after, beforeEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execSync } = require('child_process');
const { getRepoRoot } = require('../src/gep/paths');

// ---------------------------------------------------------------------------
// Minimal env setup — redirect all path-sensitive modules to tmpDir before
// requiring solidify so module-level reads pick up the right locations.
// ---------------------------------------------------------------------------
let tmpDir;
let origEnv;
const ENV_KEYS = [
  'EVOLVER_REPO_ROOT', 'GEP_ASSETS_DIR', 'EVOLUTION_DIR',
  'MEMORY_DIR', 'EVOLVER_SOLIDIFY_VERIFY', 'EVOLVER_LLM_REVIEW',
  'A2A_HUB_URL', 'A2A_NODE_SECRET', 'HUB_DRY_RUN',
  'EVOLVER_SESSION_SCOPE', 'NODE_ENV',
  'EVOLVER_AUTO_PUBLISH', 'EVOLVER_PUBLISH_ANTI_PATTERNS',
  'EVOLVER_DEFAULT_VISIBILITY', 'EVOLVER_LEAK_CHECK',
];

let gitAvailable = true;

// Minimal seed gene with no validation commands so runValidations returns ok instantly.
// Declared at module level so beforeEach can reset genes.json to clean state.
const SEED_GENE = {
  type: 'Gene',
  id: 'gene_test_solidify',
  category: 'repair',
  signals_match: ['test'],
  strategy: ['step 1', 'step 2', 'step 3'],
  validation: [],
  epigenetic_marks: [],
  learning_history: [],
  anti_patterns: [],
  constraints: { max_files: 20, max_lines: 500, forbidden_paths: [] },
};
const SEED_GENES_JSON = JSON.stringify({ version: 1, genes: [SEED_GENE] }, null, 2);
const SEED_CAPSULES_JSON = JSON.stringify({ version: 1, capsules: [] }, null, 2);

function setupTmpRepo() {
  origEnv = {};
  gitAvailable = true;
  tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-solidify-test-'));
  const gepDir = path.join(tmpDir, 'assets', 'gep');
  const evolutionDir = path.join(tmpDir, 'evolution');
  const memoryDir = path.join(tmpDir, 'memory');
  fs.mkdirSync(gepDir, { recursive: true });
  fs.mkdirSync(evolutionDir, { recursive: true });
  fs.mkdirSync(memoryDir, { recursive: true });

  fs.writeFileSync(path.join(gepDir, 'genes.json'), SEED_GENES_JSON, 'utf8');
  fs.writeFileSync(path.join(gepDir, 'capsules.json'), SEED_CAPSULES_JSON, 'utf8');
  fs.writeFileSync(path.join(gepDir, 'events.jsonl'), '', 'utf8');

  // Init git repo with one commit so isGitRepo() + blast radius work.
  // -c commit.gpgsign=false prevents failures on machines with global GPG signing.
  try {
    execSync('git init', { cwd: tmpDir, stdio: 'ignore' });
    execSync('git config user.email "test@test.com"', { cwd: tmpDir, stdio: 'ignore' });
    execSync('git config user.name "Test"', { cwd: tmpDir, stdio: 'ignore' });
    fs.writeFileSync(path.join(tmpDir, 'README.md'), 'test repo\n', 'utf8');
    execSync('git add -A', { cwd: tmpDir, stdio: 'ignore' });
    execSync('git -c commit.gpgsign=false commit -m "init"', { cwd: tmpDir, stdio: 'ignore' });
  } catch (_e) {
    // git not available or misconfigured — tests will be skipped individually.
    gitAvailable = false;
  }

  // Save and override env
  for (const k of ENV_KEYS) origEnv[k] = process.env[k];
  process.env.EVOLVER_REPO_ROOT = tmpDir;
  process.env.GEP_ASSETS_DIR = gepDir;
  process.env.EVOLUTION_DIR = evolutionDir;
  process.env.MEMORY_DIR = memoryDir;
  process.env.NODE_ENV = 'test';
  process.env.EVOLVER_SOLIDIFY_VERIFY = 'off';
  process.env.EVOLVER_LLM_REVIEW = 'false';
  process.env.HUB_DRY_RUN = '1';
  process.env.A2A_HUB_URL = 'http://localhost:0';
  delete process.env.EVOLVER_SESSION_SCOPE;
  process.env.A2A_NODE_SECRET = 'a'.repeat(64);
  process.env.EVOLVER_AUTO_PUBLISH = 'false';
  process.env.EVOLVER_PUBLISH_ANTI_PATTERNS = 'false';
  process.env.EVOLVER_DEFAULT_VISIBILITY = 'private';
  process.env.EVOLVER_LEAK_CHECK = 'off';
}

function teardownTmpRepo() {
  for (const k of ENV_KEYS) {
    if (origEnv[k] === undefined) delete process.env[k];
    else process.env[k] = origEnv[k];
  }
  try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (_) {}
}

function writeLastRun(evolutionDir, overrides = {}) {
  const lastRun = {
    selected_gene_id: 'gene_test_solidify',
    signals: ['test', 'area:testing'],
    mutation: {
      type: 'Mutation',
      id: 'mut_test_solidify',
      category: 'repair',
      trigger_signals: ['test'],
      target: 'behavior:test_coverage',
      expected_effect: 'improved test coverage',
      risk_level: 'low',
    },
    personality_state: {
      type: 'PersonalityState',
      rigor: 0.8,
      creativity: 0.5,
      verbosity: 0.5,
      risk_tolerance: 0.2,
      obedience: 0.8,
    },
    parent_event_id: null,
    ...overrides,
  };
  const statePath = path.join(evolutionDir, 'evolution_solidify_state.json');
  fs.writeFileSync(statePath, JSON.stringify({ last_run: lastRun }, null, 2), 'utf8');
  return lastRun;
}

// Require solidify AFTER env is set (paths bake in on first require).
// We do a fresh require inside each describe block's before() instead of at
// module load time so EVOLVER_REPO_ROOT is already set.
// NOTE: getRepoRoot() in paths.js always checks EVOLVER_REPO_ROOT first, so
// per-test overrides work safely. However, if the env var is cleared mid-test
// the module-level cache kicks in and returns the previously resolved path —
// keep overrides set (or restore them) rather than deleting the key outright.
// NOTE: Run this file in isolation (node --test-isolation=process or separate
// npm script) to prevent module-level state cached by earlier test files from
// leaking into solidify/a2aProtocol.
let solidify;
let a2aProtocol;

describe('solidify() integration', () => {
  before(() => {
    setupTmpRepo();
    solidify = require('../src/gep/solidify').solidify;
    a2aProtocol = require('../src/gep/a2aProtocol');
    // Reset module-level flag so HUB_DRY_RUN warning fires on first call
    // regardless of which test file ran before this one in the same process.
    a2aProtocol._testing._resetDryRunWarnedForTesting();
  });

  after(teardownTmpRepo);

  beforeEach(() => {
    // Reset shared mutable state before each test so order doesn't matter.
    const gepDir = process.env.GEP_ASSETS_DIR;
    fs.writeFileSync(path.join(gepDir, 'events.jsonl'), '', 'utf8');
    const statePath = path.join(process.env.EVOLUTION_DIR, 'evolution_solidify_state.json');
    try { fs.rmSync(statePath, { force: true }); } catch (_) {}
    // Restore GEP asset files to seed state so upsertGene/upsertCapsule
    // side-effects from previous tests don't leave dirty tracked files that
    // would skew blast radius detection in subsequent tests.
    fs.writeFileSync(path.join(gepDir, 'genes.json'), SEED_GENES_JSON, 'utf8');
    fs.writeFileSync(path.join(gepDir, 'capsules.json'), SEED_CAPSULES_JSON, 'utf8');
    // Stage the resets so git treats them as clean (same content as committed).
    try {
      execSync('git add assets/gep/genes.json assets/gep/capsules.json', { cwd: tmpDir, stdio: 'ignore' });
      execSync('git -c commit.gpgsign=false commit -m "beforeEach reset"', { cwd: tmpDir, stdio: 'ignore' });
    } catch (_) {}
  });

  it('returns ok:false when not a git repo', async (t) => {
    if (!gitAvailable) return t.skip('git not available in this environment');
    // All four path-sensitive env vars are redirected into nonGitDir so the
    // override is unambiguous — solidify cannot accidentally use the git-
    // initialized tmpDir for any path check.
    const nonGitDir = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-nogit-'));
    const ngGepDir = path.join(nonGitDir, 'assets', 'gep');
    const ngEvoDir = path.join(nonGitDir, 'evolution');
    const ngMemDir = path.join(nonGitDir, 'memory');
    fs.mkdirSync(ngGepDir, { recursive: true });
    fs.mkdirSync(ngEvoDir, { recursive: true });
    fs.mkdirSync(ngMemDir, { recursive: true });
    fs.writeFileSync(path.join(ngGepDir, 'genes.json'), JSON.stringify([]), 'utf8');
    fs.writeFileSync(path.join(ngGepDir, 'capsules.json'), JSON.stringify([]), 'utf8');
    fs.writeFileSync(path.join(ngGepDir, 'events.jsonl'), '', 'utf8');
    const origRoot = process.env.EVOLVER_REPO_ROOT;
    const origGep = process.env.GEP_ASSETS_DIR;
    const origEvo = process.env.EVOLUTION_DIR;
    const origMem = process.env.MEMORY_DIR;
    process.env.EVOLVER_REPO_ROOT = nonGitDir;
    process.env.GEP_ASSETS_DIR = ngGepDir;
    process.env.EVOLUTION_DIR = ngEvoDir;
    process.env.MEMORY_DIR = ngMemDir;
    try {
      // Pin the contract: getRepoRoot() must re-read EVOLVER_REPO_ROOT on every
      // call, not cache at module load. If paths.js ever caches at load time this
      // assertion fires before solidify() is called, making the failure obvious.
      assert.equal(getRepoRoot(), nonGitDir, 'getRepoRoot must re-read env on each call');
      const result = await solidify();
      assert.equal(result.ok, false);
      assert.equal(result.failure_reason, 'not_a_git_repository');
    } finally {
      process.env.EVOLVER_REPO_ROOT = origRoot;
      process.env.GEP_ASSETS_DIR = origGep;
      process.env.EVOLUTION_DIR = origEvo;
      process.env.MEMORY_DIR = origMem;
      fs.rmSync(nonGitDir, { recursive: true, force: true });
    }
  });

  it('first run with no prior state fails cleanly and writes an event', async (t) => {
    if (!gitAvailable) return t.skip('git not available in this environment');
    const eventsPath = path.join(process.env.GEP_ASSETS_DIR, 'events.jsonl');
    const linesBefore = fs.readFileSync(eventsPath, 'utf8').trim().split('\n').filter(Boolean).length;

    // No last_run state — solidify should still complete, emitting a failed
    // outcome (missing mutation/personality) but writing an event to disk.
    const result = await solidify({ dryRun: false });
    assert.ok(typeof result === 'object' && result !== null, 'solidify returned an object');
    assert.ok('ok' in result, 'result has ok field');
    // With no last_run, protocolViolations fire → outcome is failed but no crash.
    assert.equal(result.ok, false);

    const linesAfter = fs.readFileSync(eventsPath, 'utf8').trim().split('\n').filter(Boolean);
    assert.ok(linesAfter.length > linesBefore, 'solidify should have written at least one new event');
  });

  it('valid session with lastRun state persists a capsule to disk', async (t) => {
    if (!gitAvailable) return t.skip('git not available in this environment');
    const evolutionDir = process.env.EVOLUTION_DIR;
    const gepDir = process.env.GEP_ASSETS_DIR;
    writeLastRun(evolutionDir);
    // Create a real untracked .js file under src/ (included prefix) so blast
    // radius has at least one constraint-counted file — without this the
    // hollow-commit guard fires when the session only touches GEP metadata.
    const srcDir = path.join(tmpDir, 'src');
    fs.mkdirSync(srcDir, { recursive: true });
    const testFile = path.join(srcDir, 'test_session_change.js');
    fs.writeFileSync(testFile, 'exports.x = 1;\n', 'utf8');
    try {
      const result = await solidify({ dryRun: false });
      assert.ok(result, 'solidify returned result');
      assert.equal(result.ok, true, 'solidify should succeed with valid lastRun: ' + JSON.stringify(result.constraintCheck && result.constraintCheck.violations));
      const stored = JSON.parse(fs.readFileSync(path.join(gepDir, 'capsules.json'), 'utf8'));
      const capsules = Array.isArray(stored.capsules) ? stored.capsules : (Array.isArray(stored) ? stored : []);
      assert.ok(capsules.length > 0, 'at least one capsule persisted to capsules.json');
    } finally {
      try { fs.rmSync(testFile, { force: true }); } catch (_) {}
    }
  });

  it('rejects when blast radius exceeds gene max_files constraint', async (t) => {
    if (!gitAvailable) return t.skip('git not available in this environment');
    const evolutionDir = process.env.EVOLUTION_DIR;
    writeLastRun(evolutionDir);
    // Create 25 untracked .js files — exceeds the seed gene's max_files: 20 constraint.
    const blastDir = path.join(tmpDir, 'blast_test_files');
    fs.mkdirSync(blastDir, { recursive: true });
    try {
      for (let i = 0; i < 25; i++) {
        fs.writeFileSync(path.join(blastDir, `f${i}.js`), `exports.n = ${i};\n`, 'utf8');
      }
      const result = await solidify({ dryRun: false });
      assert.ok(result, 'solidify returned result');
      assert.equal(result.ok, false, 'solidify should reject when blast radius exceeds max_files');
      const violations = result.constraintCheck && result.constraintCheck.violations || [];
      assert.ok(
        violations.some(function (v) { return /max_files|exceeded|OVERRUN/.test(String(v)); }),
        'constraint violation should reference blast radius limit: ' + JSON.stringify(violations)
      );
    } finally {
      try { fs.rmSync(blastDir, { recursive: true, force: true }); } catch (_) {}
    }
  });

  it('second run has parent_event_id pointing to first run event (event chain)', async (t) => {
    if (!gitAvailable) return t.skip('git not available in this environment');
    const evolutionDir = process.env.EVOLUTION_DIR;
    const eventsPath = path.join(process.env.GEP_ASSETS_DIR, 'events.jsonl');

    writeLastRun(evolutionDir);

    const result1 = await solidify({ dryRun: false });
    assert.ok(result1, 'first solidify returned result');

    const lines1 = fs.readFileSync(eventsPath, 'utf8').trim().split('\n').filter(Boolean);
    assert.ok(lines1.length >= 1, 'first run wrote an event');
    const event1 = JSON.parse(lines1[lines1.length - 1]);
    assert.ok(event1.id, 'first event has an id');

    // Set up second run pointing at event1
    writeLastRun(evolutionDir, { parent_event_id: event1.id });
    const result2 = await solidify({ dryRun: false });
    assert.ok(result2, 'second solidify returned result');

    const lines2 = fs.readFileSync(eventsPath, 'utf8').trim().split('\n').filter(Boolean);
    assert.ok(lines2.length >= 2, 'second run wrote another event');
    const event2 = JSON.parse(lines2[lines2.length - 1]);
    assert.equal(event2.parent, event1.id, 'second event parent chains to first event id');
  });
});
