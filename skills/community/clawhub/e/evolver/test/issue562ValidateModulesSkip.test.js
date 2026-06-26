// Regression for EvoMap/evolver#562 (point 4) — "Validation commands reference
// scripts/validate-modules.js which does not exist in project dir".
//
// Seed / self-evolution genes ship validation commands that target evolver's
// OWN tree (e.g. `node scripts/validate-modules.js ./src/gep/...`). When evolver
// runs in a user's project, repoRoot is that project and the script is absent,
// so the command could only ever fail with "Cannot find module" — wrongly
// tanking the gene's validation_pass_rate on an environment mismatch. A command
// that cannot resolve its own script validates nothing, so it is now skipped
// (excluded from the pass/fail tally) instead of failing the cycle.
const { describe, it } = require('node:test');
const assert = require('node:assert');
const path = require('path');
const fs = require('fs');
const os = require('os');

const { validationScriptPath, runValidations } = require('../src/gep/policyCheck');

describe('policyCheck#562 - validationScriptPath', () => {
  it('extracts the script from a `node <script> ...` command', () => {
    assert.strictEqual(validationScriptPath('node scripts/validate-modules.js ./src/gep'), 'scripts/validate-modules.js');
    assert.strictEqual(validationScriptPath('node ./canary.mjs'), './canary.mjs');
  });
  it('returns null when the command runs no local script', () => {
    assert.strictEqual(validationScriptPath('node --version'), null);
    assert.strictEqual(validationScriptPath('node -e "1"'), null); // first non-flag token is not a script
    assert.strictEqual(validationScriptPath('not-node foo.js'), null);
  });
});

describe('policyCheck#562 - runValidations skips commands whose script is absent', () => {
  function tmpRepo() {
    return fs.mkdtempSync(path.join(os.tmpdir(), 'pc562-'));
  }

  it('skips (does not fail) a command whose script is missing in repoRoot', () => {
    const repoRoot = tmpRepo();
    try {
      const gene = { id: 'gene_gep_repair_from_errors', type: 'Gene', validation: ['node scripts/validate-modules.js ./src/gep'] };
      const res = runValidations(gene, { repoRoot, timeoutMs: 5000 });
      assert.strictEqual(res.ok, true, 'a missing self-evolution script must not fail the cycle in a user project');
      assert.strictEqual(res.results.length, 0, 'the unresolvable command is excluded from the pass/fail tally');
    } finally {
      fs.rmSync(repoRoot, { recursive: true, force: true });
    }
  });

  it('still runs a command whose script DOES exist (no false skip)', () => {
    const repoRoot = tmpRepo();
    try {
      fs.writeFileSync(path.join(repoRoot, 'check.js'), 'process.exit(0)\n');
      const gene = { id: 'g', type: 'Gene', validation: ['node check.js'] };
      const res = runValidations(gene, { repoRoot, timeoutMs: 5000 });
      assert.strictEqual(res.ok, true);
      assert.strictEqual(res.results.length, 1, 'an existing script must actually run');
      assert.strictEqual(res.results[0].ok, true);
    } finally {
      fs.rmSync(repoRoot, { recursive: true, force: true });
    }
  });

  it('runs the present command and skips only the missing one in a mixed list', () => {
    const repoRoot = tmpRepo();
    try {
      fs.writeFileSync(path.join(repoRoot, 'present.js'), 'process.exit(0)\n');
      const gene = { id: 'g', type: 'Gene', validation: ['node scripts/validate-modules.js ./src', 'node present.js'] };
      const res = runValidations(gene, { repoRoot, timeoutMs: 5000 });
      assert.strictEqual(res.ok, true);
      assert.strictEqual(res.results.length, 1, 'only the resolvable command is tallied');
      assert.ok(res.results[0].cmd.includes('present.js'));
    } finally {
      fs.rmSync(repoRoot, { recursive: true, force: true });
    }
  });
});
