const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execSync } = require('child_process');

const {
  isInsideEvolverRepo,
  buildHostAwareValidation,
} = require('../src/gep/solidify');
const { rollbackNewUntrackedFiles } = require('../src/gep/gitOps');

// ---------------------------------------------------------------------------
// Fixture helpers
// ---------------------------------------------------------------------------
function makeTmpRepo({ pkgName, initGit = false } = {}) {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-rb-'));
  if (pkgName !== undefined) {
    fs.writeFileSync(
      path.join(tmp, 'package.json'),
      JSON.stringify({ name: pkgName, version: '0.0.0' }, null, 2)
    );
  }
  if (initGit) {
    execSync('git init -q', { cwd: tmp });
    execSync('git config user.email test@test', { cwd: tmp });
    execSync('git config user.name test', { cwd: tmp });
  }
  return tmp;
}

function rmTmp(p) {
  try { fs.rmSync(p, { recursive: true, force: true }); } catch (_) { /* ignore */ }
}

// ---------------------------------------------------------------------------
// A. Repo identity confusion guard
// ---------------------------------------------------------------------------
describe('isInsideEvolverRepo', () => {
  it('returns true when package.json name === "@evomap/evolver"', () => {
    const tmp = makeTmpRepo({ pkgName: '@evomap/evolver' });
    try {
      assert.equal(isInsideEvolverRepo(tmp), true);
    } finally { rmTmp(tmp); }
  });

  it('returns false for any other package name', () => {
    const tmp = makeTmpRepo({ pkgName: 'some-user-project' });
    try {
      assert.equal(isInsideEvolverRepo(tmp), false);
    } finally { rmTmp(tmp); }
  });

  it('returns false when package.json is missing', () => {
    const tmp = makeTmpRepo();
    try {
      assert.equal(isInsideEvolverRepo(tmp), false);
    } finally { rmTmp(tmp); }
  });

  it('returns false when package.json is malformed', () => {
    const tmp = makeTmpRepo();
    fs.writeFileSync(path.join(tmp, 'package.json'), '{not valid json');
    try {
      assert.equal(isInsideEvolverRepo(tmp), false);
    } finally { rmTmp(tmp); }
  });
});

describe('buildHostAwareValidation', () => {
  it('returns evolver-internal validation suite when run inside @evomap/evolver', () => {
    const tmp = makeTmpRepo({ pkgName: '@evomap/evolver' });
    try {
      const v = buildHostAwareValidation(tmp);
      assert.ok(Array.isArray(v));
      assert.ok(v.some(c => c.includes('validate-modules.js')));
      assert.ok(v.some(c => c.includes('validate-suite.js')));
    } finally { rmTmp(tmp); }
  });

  it('returns a portable single-command fallback in non-evolver host repos', () => {
    const tmp = makeTmpRepo({ pkgName: 'host-app' });
    try {
      const v = buildHostAwareValidation(tmp);
      assert.deepEqual(v, ['git diff --check']);
    } finally { rmTmp(tmp); }
  });
});

// ---------------------------------------------------------------------------
// B. Rollback default (EVOLVER_ROLLBACK_MODE)
//
// Source-level assertion: the runtime mode resolution captures the env var
// once via a closure that's hard to mock without re-loading the module fresh.
// Reading the source directly is robust and unambiguous about what the
// default actually is.
// ---------------------------------------------------------------------------
describe('rollbackTracked default mode', () => {
  it('source declares "stash" as the default for EVOLVER_ROLLBACK_MODE', () => {
    const src = fs.readFileSync(require.resolve('../src/gep/gitOps'), 'utf8');
    assert.match(
      src,
      /process\.env\.EVOLVER_ROLLBACK_MODE\s*\|\|\s*['"]stash['"]/,
      'rollbackTracked must default EVOLVER_ROLLBACK_MODE to "stash"'
    );
    assert.doesNotMatch(
      src,
      /process\.env\.EVOLVER_ROLLBACK_MODE\s*\|\|\s*['"]hard['"]/,
      'legacy "hard" default must not be present'
    );
  });
});

// ---------------------------------------------------------------------------
// C. Cycle-boundary mtime guard
// ---------------------------------------------------------------------------
describe('rollbackNewUntrackedFiles mtime guard', () => {
  it('preserves files whose mtime predates cycleStartedAt', async () => {
    const tmp = makeTmpRepo({ initGit: true });
    try {
      // Pre-cycle file (e.g. a user edit that escaped the baseline because of
      // a race between baseline capture and first edit).
      fs.writeFileSync(path.join(tmp, 'user-edit.txt'), 'pre-cycle');
      const oldStat = fs.statSync(path.join(tmp, 'user-edit.txt'));
      const cycleStartMs = oldStat.mtimeMs + 50;

      // Wait so the cycle-produced file's mtime is strictly after cycleStart.
      await new Promise(r => setTimeout(r, 100));

      fs.writeFileSync(path.join(tmp, 'evolver-output.txt'), 'cycle artefact');

      const result = rollbackNewUntrackedFiles({
        repoRoot: tmp,
        baselineUntracked: [],
        cycleStartedAt: cycleStartMs,
      });

      assert.equal(
        fs.existsSync(path.join(tmp, 'user-edit.txt')),
        true,
        'pre-cycle file must NOT be deleted'
      );
      assert.equal(
        fs.existsSync(path.join(tmp, 'evolver-output.txt')),
        false,
        'cycle-produced file should be deleted'
      );
      assert.deepEqual(result.deleted, ['evolver-output.txt']);
    } finally { rmTmp(tmp); }
  });

  it('falls back to baseline-only filter when cycleStartedAt is omitted', () => {
    const tmp = makeTmpRepo({ initGit: true });
    try {
      fs.writeFileSync(path.join(tmp, 'a.txt'), 'A');
      fs.writeFileSync(path.join(tmp, 'b.txt'), 'B');
      const result = rollbackNewUntrackedFiles({
        repoRoot: tmp,
        baselineUntracked: ['a.txt'],
        // cycleStartedAt deliberately omitted -- exercise legacy path
      });
      assert.equal(fs.existsSync(path.join(tmp, 'a.txt')), true);
      assert.equal(fs.existsSync(path.join(tmp, 'b.txt')), false);
      assert.deepEqual(result.deleted, ['b.txt']);
    } finally { rmTmp(tmp); }
  });

  it('accepts ISO string for cycleStartedAt (matches dispatch.js last_run.created_at)', async () => {
    const tmp = makeTmpRepo({ initGit: true });
    try {
      fs.writeFileSync(path.join(tmp, 'pre.txt'), 'P');
      const oldStat = fs.statSync(path.join(tmp, 'pre.txt'));
      const cycleStartIso = new Date(oldStat.mtimeMs + 50).toISOString();
      await new Promise(r => setTimeout(r, 100));
      fs.writeFileSync(path.join(tmp, 'post.txt'), 'Q');

      rollbackNewUntrackedFiles({
        repoRoot: tmp,
        baselineUntracked: [],
        cycleStartedAt: cycleStartIso,
      });

      assert.equal(fs.existsSync(path.join(tmp, 'pre.txt')), true);
      assert.equal(fs.existsSync(path.join(tmp, 'post.txt')), false);
    } finally { rmTmp(tmp); }
  });
});
