// test/claimNudge.test.js
// Unit tests for src/gep/claimNudge.js: cooldown, disk persistence, opt-out.
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

describe('claimNudge', function () {
  let tmpHome;
  let origEvolverHome;
  let capturedLogs;
  let origConsoleLog;
  let origDisable;

  beforeEach(() => {
    tmpHome = fs.mkdtempSync(path.join(os.tmpdir(), 'evomap-claim-'));
    origEvolverHome = process.env.EVOLVER_HOME;
    process.env.EVOLVER_HOME = tmpHome;
    origDisable = process.env.EVOLVER_DISABLE_CLAIM_NUDGE;
    delete process.env.EVOLVER_DISABLE_CLAIM_NUDGE;
    capturedLogs = [];
    origConsoleLog = console.log;
    console.log = (...args) => { capturedLogs.push(args.join(' ')); };
  });

  afterEach(() => {
    console.log = origConsoleLog;
    if (origEvolverHome === undefined) delete process.env.EVOLVER_HOME;
    else process.env.EVOLVER_HOME = origEvolverHome;
    if (origDisable === undefined) delete process.env.EVOLVER_DISABLE_CLAIM_NUDGE;
    else process.env.EVOLVER_DISABLE_CLAIM_NUDGE = origDisable;
    try { fs.rmSync(tmpHome, { recursive: true, force: true }); } catch (_) {}
  });

  it('prints nudge when claim_code + claim_url present', function () {
    const nudge = freshRequire('../src/gep/claimNudge');
    nudge._resetForTests();
    const printed = nudge.maybePrintClaimNudge({
      claim_code: 'TEST-1234',
      claim_url: 'https://evomap.ai/claim/TEST-1234',
    });
    assert.equal(printed, true);
    const joined = capturedLogs.join('\n');
    assert.ok(joined.includes('TEST-1234'));
    assert.ok(joined.includes('https://evomap.ai/claim/TEST-1234'));
  });

  it('skips when EVOLVER_DISABLE_CLAIM_NUDGE=1', function () {
    process.env.EVOLVER_DISABLE_CLAIM_NUDGE = '1';
    const nudge = freshRequire('../src/gep/claimNudge');
    nudge._resetForTests();
    const printed = nudge.maybePrintClaimNudge({
      claim_code: 'TEST-OFF',
      claim_url: 'https://evomap.ai/claim/TEST-OFF',
    });
    assert.equal(printed, false);
    assert.equal(capturedLogs.length, 0);
  });

  it('skips second call for same code within cooldown', function () {
    const nudge = freshRequire('../src/gep/claimNudge');
    nudge._resetForTests();
    const p1 = nudge.maybePrintClaimNudge({ claim_code: 'CD-1', claim_url: 'https://evomap.ai/claim/CD-1' });
    const p2 = nudge.maybePrintClaimNudge({ claim_code: 'CD-1', claim_url: 'https://evomap.ai/claim/CD-1' });
    assert.equal(p1, true);
    assert.equal(p2, false);
  });

  it('prints again for a different claim_code (new cycle)', function () {
    const nudge = freshRequire('../src/gep/claimNudge');
    nudge._resetForTests();
    const p1 = nudge.maybePrintClaimNudge({ claim_code: 'CA-1', claim_url: 'https://evomap.ai/claim/CA-1' });
    const p2 = nudge.maybePrintClaimNudge({ claim_code: 'CA-2', claim_url: 'https://evomap.ai/claim/CA-2' });
    assert.equal(p1, true);
    assert.equal(p2, true);
  });

  it('does nothing when claim_code missing', function () {
    const nudge = freshRequire('../src/gep/claimNudge');
    nudge._resetForTests();
    const printed = nudge.maybePrintClaimNudge({ claim_url: 'https://evomap.ai/claim/NO-CODE' });
    assert.equal(printed, false);
    assert.equal(capturedLogs.length, 0);
  });

  it('persists state so a second process does not re-nudge within cooldown', function () {
    const nudge1 = freshRequire('../src/gep/claimNudge');
    nudge1._resetForTests();
    const p1 = nudge1.maybePrintClaimNudge({ claim_code: 'PR-1', claim_url: 'https://evomap.ai/claim/PR-1' });
    assert.equal(p1, true);

    const nudge2 = freshRequire('../src/gep/claimNudge');
    const p2 = nudge2.maybePrintClaimNudge({ claim_code: 'PR-1', claim_url: 'https://evomap.ai/claim/PR-1' });
    assert.equal(p2, false);
  });
});
