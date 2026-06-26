// Tests for the v1.69.7 default LEAK_CHECK_MODE flip from 'warn' to 'strict'.
//
// Before v1.69.7 the pre-publish leak scanner only logged a warning when it
// detected suspicious content in a capsule/gene payload and continued to
// publish. Private-repo users can now opt back into that behavior by setting
// EVOLVER_LEAK_CHECK=warn, but the compile-time default is 'strict'.

const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');

function freshConfig() {
  const resolved = require.resolve('../src/config');
  delete require.cache[resolved];
  return require(resolved);
}

describe('config.LEAK_CHECK_MODE', () => {
  let savedEnv;

  beforeEach(() => {
    savedEnv = process.env.EVOLVER_LEAK_CHECK;
    delete process.env.EVOLVER_LEAK_CHECK;
  });

  afterEach(() => {
    if (savedEnv === undefined) {
      delete process.env.EVOLVER_LEAK_CHECK;
    } else {
      process.env.EVOLVER_LEAK_CHECK = savedEnv;
    }
  });

  it('defaults to strict when EVOLVER_LEAK_CHECK is unset', () => {
    const { LEAK_CHECK_MODE } = freshConfig();
    assert.equal(LEAK_CHECK_MODE, 'strict');
  });

  it('respects EVOLVER_LEAK_CHECK=warn opt-out', () => {
    process.env.EVOLVER_LEAK_CHECK = 'warn';
    const { LEAK_CHECK_MODE } = freshConfig();
    assert.equal(LEAK_CHECK_MODE, 'warn');
  });

  it('respects EVOLVER_LEAK_CHECK=off opt-out', () => {
    process.env.EVOLVER_LEAK_CHECK = 'off';
    const { LEAK_CHECK_MODE } = freshConfig();
    assert.equal(LEAK_CHECK_MODE, 'off');
  });

  it('treats empty string the same as unset (falls back to strict default)', () => {
    process.env.EVOLVER_LEAK_CHECK = '';
    const { LEAK_CHECK_MODE } = freshConfig();
    assert.equal(LEAK_CHECK_MODE, 'strict');
  });
});
