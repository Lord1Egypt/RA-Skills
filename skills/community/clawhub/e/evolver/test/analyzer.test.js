const { describe, it, before, after, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { analyzeFailures } = require('../src/gep/analyzer');

describe('analyzeFailures', () => {
  let tmpDir;
  let originalCwd;

  beforeEach(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'analyzer-test-'));
    originalCwd = process.cwd();
    process.chdir(tmpDir);
  });

  afterEach(() => {
    process.chdir(originalCwd);
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  it('returns skipped status when MEMORY.md is absent', () => {
    const result = analyzeFailures();
    assert.equal(result.status, 'skipped');
    assert.equal(result.reason, 'no_memory');
  });

  it('returns success with empty failures when MEMORY.md has no matching entries', () => {
    fs.writeFileSync(path.join(tmpDir, 'MEMORY.md'), '# Memory\n\nNo failures yet.\n');
    const result = analyzeFailures();
    assert.equal(result.status, 'success');
    assert.equal(result.count, 0);
    assert.deepEqual(result.failures, []);
  });

  it('parses a single failure entry from the canonical table row format', () => {
    const content = [
      '# Memory',
      '',
      '| ID | Kind | Summary | Detail |',
      '| --- | --- | --- | --- |',
      '| **F1** | Fix | timeout during solidify | **RateLimited** (429 response from hub) |',
      '',
    ].join('\n');
    fs.writeFileSync(path.join(tmpDir, 'MEMORY.md'), content);

    const result = analyzeFailures();
    assert.equal(result.status, 'success');
    assert.equal(result.count, 1);
    assert.equal(result.failures.length, 1);
    assert.equal(result.failures[0].summary, 'timeout during solidify');
    assert.equal(result.failures[0].detail, 'RateLimited');
  });

  it('returns only the top 3 failures in the failures field', () => {
    const rows = [];
    for (let i = 1; i <= 7; i++) {
      rows.push(`| **F${i}** | Fix | summary ${i} | **Detail${i}** (extra ${i}) |`);
    }
    const content = ['# Memory', '', ...rows].join('\n');
    fs.writeFileSync(path.join(tmpDir, 'MEMORY.md'), content);

    const result = analyzeFailures();
    assert.equal(result.status, 'success');
    assert.equal(result.count, 7);
    assert.equal(result.failures.length, 3);
    assert.equal(result.failures[0].summary, 'summary 1');
    assert.equal(result.failures[2].summary, 'summary 3');
  });

  it('trims whitespace from summary and detail', () => {
    const content = [
      '# Memory',
      '',
      '|   **F1**  |  Fix  |    padded summary    |    **PaddedDetail**   (note)  |',
    ].join('\n');
    fs.writeFileSync(path.join(tmpDir, 'MEMORY.md'), content);

    const result = analyzeFailures();
    assert.equal(result.failures[0].summary, 'padded summary');
    assert.equal(result.failures[0].detail, 'PaddedDetail');
  });

  it('ignores rows that do not match the F<N>/Fix pattern', () => {
    const content = [
      '# Memory',
      '',
      '| **W1** | Warn | should be ignored | **Info** (warning) |',
      '| **F1** | Fix | real failure | **Error** (detail) |',
      '| **F2** | Review | wrong kind | **Review** (note) |',
    ].join('\n');
    fs.writeFileSync(path.join(tmpDir, 'MEMORY.md'), content);

    const result = analyzeFailures();
    assert.equal(result.count, 1);
    assert.equal(result.failures[0].summary, 'real failure');
  });

  it('handles multi-digit F-numbers', () => {
    const content = [
      '# Memory',
      '',
      '| **F12** | Fix | twelfth failure | **ErrA** (x) |',
      '| **F999** | Fix | nine-nine-nine | **ErrB** (y) |',
    ].join('\n');
    fs.writeFileSync(path.join(tmpDir, 'MEMORY.md'), content);

    const result = analyzeFailures();
    assert.equal(result.count, 2);
    assert.equal(result.failures[0].summary, 'twelfth failure');
    assert.equal(result.failures[1].summary, 'nine-nine-nine');
  });

  it('does not throw when MEMORY.md is empty', () => {
    fs.writeFileSync(path.join(tmpDir, 'MEMORY.md'), '');
    const result = analyzeFailures();
    assert.equal(result.status, 'success');
    assert.equal(result.count, 0);
  });
});
