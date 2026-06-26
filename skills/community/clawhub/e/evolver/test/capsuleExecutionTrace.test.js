// 2026-05-02: regression guard for the Capsule.execution_trace shape the Hub
// expects. Before this, solidify() emitted Capsule payloads without any
// execution_trace at all, triggering 100% trace_empty flags at the Hub. The
// contract tested here mirrors evomap-hub/src/services/capsuleTraceQualityService.js
// so a shape drift on either side will break this test immediately instead of
// silently inflating "Capsule trace missing" alerts in prod.

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const { buildCapsuleTraceSteps } = require('../src/gep/solidify');

// Mirror of Hub's assessCapsuleTraceQuality shape gates:
//   - Array.isArray(trace) && trace.length > 0
//   - every step is an object with string `stage` and string `cmd`
//   - at least one stage/cmd matches validate/verify/check/test
//   - outcome.success implies no step reports non-zero exit
const VALIDATION_KEYWORDS = ['validate', 'verify', 'check', 'test'];

function assertHubShape(trace, { outcomeSuccess }) {
  assert.ok(Array.isArray(trace), 'trace must be an array');
  assert.ok(trace.length > 0, 'trace must have at least one step');
  for (const step of trace) {
    assert.equal(typeof step, 'object', 'step must be an object');
    assert.ok(step !== null, 'step must not be null');
    assert.equal(typeof step.stage, 'string', 'step.stage must be string');
    assert.ok(step.stage.trim().length > 0, 'step.stage must be non-empty');
    assert.equal(typeof step.cmd, 'string', 'step.cmd must be string');
    assert.ok(step.cmd.trim().length > 0, 'step.cmd must be non-empty');
  }
  const hasValidationStage = trace.some((s) => {
    const stage = String(s.stage || '').toLowerCase();
    const cmd = String(s.cmd || '').toLowerCase();
    return VALIDATION_KEYWORDS.some((kw) => stage.includes(kw) || cmd.includes(kw));
  });
  assert.ok(
    hasValidationStage,
    'trace must include at least one validate/verify/check/test step',
  );
  if (outcomeSuccess) {
    const hasNonZeroExit = trace.some(
      (s) => typeof s.exit === 'number' && s.exit !== 0,
    );
    assert.equal(
      hasNonZeroExit,
      false,
      'success outcome must not contain non-zero exits',
    );
  }
}

describe('buildCapsuleTraceSteps - Hub shape contract', () => {
  it('success path with validation results: build + validate steps, all exit=0', () => {
    const trace = buildCapsuleTraceSteps({
      blast: { files: 2, lines: 14 },
      validation: {
        ok: true,
        results: [
          { cmd: 'npm test', ok: true },
          { cmd: 'npm run lint', ok: true },
        ],
      },
      canary: { ok: true, skipped: false },
      outcomeStatus: 'success',
    });
    assertHubShape(trace, { outcomeSuccess: true });
    assert.equal(trace.length, 4, 'build + 2 validate + canary');
    assert.equal(trace[0].stage, 'build');
    assert.equal(trace[1].stage, 'validate');
    assert.equal(trace[1].cmd, 'npm test');
    assert.equal(trace[1].exit, 0);
    assert.equal(trace[3].stage, 'canary');
  });

  it('failed validation: exit=1 on failing step, consistent with outcomeStatus=failed', () => {
    const trace = buildCapsuleTraceSteps({
      blast: { files: 1, lines: 3 },
      validation: {
        ok: false,
        results: [
          { cmd: 'npm test', ok: false, err: 'Error: expected 1 received 0' },
        ],
      },
      canary: { skipped: true },
      outcomeStatus: 'failed',
    });
    assertHubShape(trace, { outcomeSuccess: false });
    const validateStep = trace.find((s) => s.stage === 'validate');
    assert.ok(validateStep, 'validate step present');
    assert.equal(validateStep.exit, 1);
  });

  it('no blast and no validation results: still emits fallback step that passes shape check', () => {
    const trace = buildCapsuleTraceSteps({
      blast: { files: 0, lines: 0 },
      validation: { ok: true, results: [] },
      canary: { skipped: true },
      outcomeStatus: 'success',
    });
    assertHubShape(trace, { outcomeSuccess: true });
    assert.equal(trace.length, 1, 'single fallback step');
    assert.equal(trace[0].stage, 'validate');
    assert.equal(trace[0].exit, 0);
  });

  it('fallback step under failed outcome reports non-zero exit so Hub exit-consistency stays honest', () => {
    const trace = buildCapsuleTraceSteps({
      blast: { files: 0, lines: 0 },
      validation: null,
      canary: null,
      outcomeStatus: 'failed',
    });
    assertHubShape(trace, { outcomeSuccess: false });
    assert.equal(trace[0].exit, 1);
  });

  it('drops validation entries with blank cmd but keeps the rest valid', () => {
    const trace = buildCapsuleTraceSteps({
      blast: { files: 0, lines: 0 },
      validation: {
        ok: true,
        results: [
          { cmd: '', ok: true },
          { cmd: '   ', ok: true },
          { cmd: 'npm test', ok: true },
        ],
      },
      canary: null,
      outcomeStatus: 'success',
    });
    assertHubShape(trace, { outcomeSuccess: true });
    const cmds = trace.map((s) => s.cmd);
    assert.ok(cmds.includes('npm test'));
    assert.ok(!cmds.includes(''));
    assert.ok(!cmds.includes('   '));
  });

  it('truncates excessively long cmd strings to guard against hub payload limits', () => {
    const longCmd = 'npm test ' + 'a'.repeat(500);
    const trace = buildCapsuleTraceSteps({
      blast: { files: 0, lines: 0 },
      validation: { ok: true, results: [{ cmd: longCmd, ok: true }] },
      canary: null,
      outcomeStatus: 'success',
    });
    const validateStep = trace.find((s) => s.cmd.startsWith('npm test'));
    assert.ok(validateStep);
    assert.ok(validateStep.cmd.length <= 200, 'cmd truncated');
  });

  it('canary failure step reports exit=1 regardless of overall outcome', () => {
    const trace = buildCapsuleTraceSteps({
      blast: { files: 1, lines: 5 },
      validation: { ok: true, results: [{ cmd: 'npm test', ok: true }] },
      canary: { ok: false, skipped: false },
      outcomeStatus: 'failed',
    });
    assertHubShape(trace, { outcomeSuccess: false });
    const canaryStep = trace.find((s) => s.stage === 'canary');
    assert.ok(canaryStep);
    assert.equal(canaryStep.exit, 1);
  });

  it('numbers steps sequentially starting at 1 for downstream audit ordering', () => {
    const trace = buildCapsuleTraceSteps({
      blast: { files: 2, lines: 14 },
      validation: {
        ok: true,
        results: [
          { cmd: 'npm test', ok: true },
          { cmd: 'npm run lint', ok: true },
        ],
      },
      canary: { ok: true, skipped: false },
      outcomeStatus: 'success',
    });
    trace.forEach((step, idx) => {
      assert.equal(step.step, idx + 1, `step ${idx} has sequential index`);
    });
  });
});
