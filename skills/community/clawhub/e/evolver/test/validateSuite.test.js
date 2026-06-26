'use strict';

// Regression tests for scripts/validate-suite.js (community PR #514).
//
// Two behavioral guarantees:
//   1. The script accepts a single test-file path in addition to a glob-style
//      directory pattern. Before the fix, `validate-suite.js test/foo.test.js`
//      crashed because expandTestGlob treated the argument as a directory and
//      called fs.readdirSync on a file.
//   2. The child-process call uses execFileSync with an explicit argv array
//      instead of execSync + shell interpolation, so a test file name can
//      never be interpreted as a shell command.

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const REPO_ROOT = path.join(__dirname, '..');

describe('scripts/validate-suite.js (community PR #514)', () => {
  it('source uses execFileSync and not shell-interpolated execSync', () => {
    const src = fs.readFileSync(path.join(REPO_ROOT, 'scripts', 'validate-suite.js'), 'utf8');
    assert.ok(/require\('child_process'\)/.test(src), 'must require child_process');
    assert.ok(/execFileSync/.test(src),
      'must use execFileSync (PR #514 hardening)');
    assert.ok(!/\bexecSync\b/.test(src),
      'must not fall back to execSync (shell interpretation risk)');
    assert.ok(/process\.execPath/.test(src),
      'must spawn node via process.execPath, not a "node --test ..." string');
  });

  it('accepts a single test file path as its argument', () => {
    // Pick a small existing test file that does not require external services.
    // proxySettings.test.js is self-contained and fast.
    const targetTest = path.join('test', 'proxySettings.test.js');
    assert.ok(fs.existsSync(path.join(REPO_ROOT, targetTest)),
      'probe test file must exist: ' + targetTest);

    const output = execFileSync(process.execPath, [
      'scripts/validate-suite.js',
      targetTest,
    ], {
      cwd: REPO_ROOT,
      encoding: 'utf8',
      timeout: 60_000,
    });
    assert.ok(/ok: \d+ test\(s\) passed/.test(output),
      'single-file invocation must produce the ok summary line, got:\n' + output);
  });

  it('still rejects non-matching patterns with a clear FAIL message', () => {
    let threw = null;
    try {
      execFileSync(process.execPath, [
        'scripts/validate-suite.js',
        'test/__definitely_does_not_exist__.test.js',
      ], {
        cwd: REPO_ROOT,
        encoding: 'utf8',
        timeout: 30_000,
      });
    } catch (e) { threw = e; }
    assert.ok(threw, 'missing file must exit non-zero');
    const stderr = String(threw.stderr || '') + String(threw.stdout || '');
    assert.ok(/no tests found/.test(stderr),
      'missing file must emit "no tests found", got:\n' + stderr);
  });
});
