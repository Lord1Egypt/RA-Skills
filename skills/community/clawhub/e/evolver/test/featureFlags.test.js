// test/featureFlags.test.js
// Tests for src/gep/featureFlags.js: persistent storage + read/write semantics,
// and the three-tier resolution in validator.isValidatorEnabled().
'use strict';

const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');

function freshRequire(id) {
  delete require.cache[require.resolve(id)];
  return require(id);
}

describe('featureFlags persistence', function () {
  // #114: redirect ~/.evomap by setting EVOLVER_HOME instead of monkey-patching
  // `os.homedir`. The global monkey-patch was fragile (parallel-test hostile;
  // affected any module that read homedir during the patch window).
  let tmpHome;
  let originalEvolverHome;

  beforeEach(() => {
    tmpHome = fs.mkdtempSync(path.join(os.tmpdir(), 'evomap-flags-'));
    originalEvolverHome = process.env.EVOLVER_HOME;
    process.env.EVOLVER_HOME = tmpHome;
  });

  afterEach(() => {
    if (originalEvolverHome === undefined) delete process.env.EVOLVER_HOME;
    else process.env.EVOLVER_HOME = originalEvolverHome;
    try { fs.rmSync(tmpHome, { recursive: true, force: true }); } catch (_) {}
  });

  it('returns undefined for unset key', function () {
    const ff = freshRequire('../src/gep/featureFlags');
    assert.equal(ff.readFeatureFlag('validator_enabled'), undefined);
  });

  it('persists value across cache resets', function () {
    const ff = freshRequire('../src/gep/featureFlags');
    assert.equal(ff.writeFeatureFlag('validator_enabled', true, 'hub_mailbox'), true);

    const ff2 = freshRequire('../src/gep/featureFlags');
    assert.equal(ff2.readFeatureFlag('validator_enabled'), true);

    const all = ff2.getAllFeatureFlags();
    assert.equal(all.validator_enabled.value, true);
    assert.equal(all.validator_enabled.source, 'hub_mailbox');
    assert.ok(all.validator_enabled.updatedAt);
  });

  it('rejects empty / non-string keys', function () {
    const ff = freshRequire('../src/gep/featureFlags');
    assert.equal(ff.writeFeatureFlag('', true, 'src'), false);
    assert.equal(ff.writeFeatureFlag(null, true, 'src'), false);
    assert.equal(ff.readFeatureFlag(''), undefined);
  });
});

describe('isValidatorEnabled three-tier resolution', function () {
  let tmpHome;
  const originalEnv = { ...process.env };

  beforeEach(() => {
    tmpHome = fs.mkdtempSync(path.join(os.tmpdir(), 'evomap-flags-'));
    process.env.EVOLVER_HOME = tmpHome;
    delete process.env.EVOLVER_VALIDATOR_ENABLED;
  });

  afterEach(() => {
    try { fs.rmSync(tmpHome, { recursive: true, force: true }); } catch (_) {}
    for (const k of Object.keys(process.env)) {
      if (!(k in originalEnv)) delete process.env[k];
    }
    Object.assign(process.env, originalEnv);
  });

  it('defaults to true when env unset and no persisted flag', function () {
    freshRequire('../src/gep/featureFlags');
    const v = freshRequire('../src/gep/validator');
    assert.equal(v.isValidatorEnabled(), true);
  });

  it('env=0 wins over persisted flag=true', function () {
    const ff = freshRequire('../src/gep/featureFlags');
    ff.writeFeatureFlag('validator_enabled', true, 'hub_mailbox');
    process.env.EVOLVER_VALIDATOR_ENABLED = '0';
    const v = freshRequire('../src/gep/validator');
    assert.equal(v.isValidatorEnabled(), false);
  });

  it('env=1 wins over persisted flag=false', function () {
    const ff = freshRequire('../src/gep/featureFlags');
    ff.writeFeatureFlag('validator_enabled', false, 'hub_mailbox');
    process.env.EVOLVER_VALIDATOR_ENABLED = '1';
    const v = freshRequire('../src/gep/validator');
    assert.equal(v.isValidatorEnabled(), true);
  });

  it('persisted flag=false applied when env unset', function () {
    const ff = freshRequire('../src/gep/featureFlags');
    ff.writeFeatureFlag('validator_enabled', false, 'hub_mailbox');
    const v = freshRequire('../src/gep/validator');
    assert.equal(v.isValidatorEnabled(), false);
  });

  it('accepts off/false/no aliases for env opt-out', function () {
    for (const val of ['off', 'false', 'no', 'OFF', 'False']) {
      process.env.EVOLVER_VALIDATOR_ENABLED = val;
      const v = freshRequire('../src/gep/validator');
      assert.equal(v.isValidatorEnabled(), false, 'value=' + val);
    }
  });
});
