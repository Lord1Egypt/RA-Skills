'use strict';

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const { createCapsule, validateCapsule, VALID_OUTCOME_STATUSES } = require('../src/gep/schemas/capsule');

describe('createCapsule', () => {
  it('returns a fully-formed Capsule with all defaults when called with empty object', () => {
    const c = createCapsule({});
    assert.equal(c.type, 'Capsule');
    assert.equal(c.id, null);
    assert.deepEqual(c.trigger, []);
    assert.deepEqual(c.strategy, []);
    assert.deepEqual(c.execution_trace, []);
    assert.equal(c.summary, '');
    assert.equal(c.confidence, 0);
    assert.deepEqual(c.blast_radius, { files: 0, lines: 0 });
    assert.deepEqual(c.outcome, { status: 'failed', score: 0 });
    assert.deepEqual(c.a2a, { eligible_to_broadcast: false });
    assert.equal(c.success_streak, 0);
    assert.equal(c.asset_id, null);
    assert.equal(typeof c.schema_version, 'string');
  });

  it('preserves provided fields', () => {
    const c = createCapsule({
      id: 'cap1',
      summary: 'Fixed it',
      confidence: 0.9,
      outcome: { status: 'success', score: 0.9 },
    });
    assert.equal(c.id, 'cap1');
    assert.equal(c.summary, 'Fixed it');
    assert.equal(c.confidence, 0.9);
    assert.equal(c.outcome.status, 'success');
    assert.equal(c.outcome.score, 0.9);
  });

  it('is idempotent — createCapsule(createCapsule(x)) equals createCapsule(x)', () => {
    const input = { id: 'cap2', summary: 'ok', outcome: { status: 'success', score: 0.8 }, trigger: ['err'] };
    const once = createCapsule(input);
    const twice = createCapsule(once);
    assert.deepEqual(once, twice);
  });

  it('normalizes null/missing outcome to default', () => {
    const c = createCapsule({ outcome: null });
    assert.deepEqual(c.outcome, { status: 'failed', score: 0 });
  });

  it('normalizes invalid outcome.status to "failed"', () => {
    const c = createCapsule({ outcome: { status: 'unknown', score: 0.5 } });
    assert.equal(c.outcome.status, 'failed');
  });

  it('merges partial outcome with defaults', () => {
    const c = createCapsule({ outcome: { status: 'success' } });
    assert.equal(c.outcome.status, 'success');
    assert.equal(c.outcome.score, 0);
  });

  it('normalizes non-array trigger to []', () => {
    const c = createCapsule({ trigger: 'not-an-array' });
    assert.deepEqual(c.trigger, []);
  });

  it('normalizes null blast_radius to default', () => {
    const c = createCapsule({ blast_radius: null });
    assert.deepEqual(c.blast_radius, { files: 0, lines: 0 });
  });

  it('merges partial blast_radius with defaults', () => {
    const c = createCapsule({ blast_radius: { files: 5 } });
    assert.equal(c.blast_radius.files, 5);
    assert.equal(c.blast_radius.lines, 0);
  });

  it('normalizes null a2a to default', () => {
    const c = createCapsule({ a2a: null });
    assert.deepEqual(c.a2a, { eligible_to_broadcast: false });
  });

  it('merges partial a2a with defaults', () => {
    const c = createCapsule({ a2a: { eligible_to_broadcast: true } });
    assert.equal(c.a2a.eligible_to_broadcast, true);
  });

  it('normalizes non-string summary to empty string', () => {
    const c = createCapsule({ summary: 42 });
    assert.equal(c.summary, '');
  });

  it('normalizes non-number confidence to 0', () => {
    const c = createCapsule({ confidence: 'high' });
    assert.equal(c.confidence, 0);
  });

  it('accepts all valid outcome statuses', () => {
    for (const status of VALID_OUTCOME_STATUSES) {
      const c = createCapsule({ outcome: { status, score: 0.5 } });
      assert.equal(c.outcome.status, status);
    }
  });

  it('returns independent array instances — mutation does not contaminate other capsules', () => {
    const c1 = createCapsule({ id: 'c1' });
    const c2 = createCapsule({ id: 'c2' });
    c1.trigger.push('signal_a');
    c1.execution_trace.push({ step: 'run' });
    assert.deepEqual(c2.trigger, [], 'trigger should be independent');
    assert.deepEqual(c2.execution_trace, [], 'execution_trace should be independent');
  });

  it('returns independent array instances even when partial provides arrays', () => {
    const shared = ['log_error'];
    const c1 = createCapsule({ trigger: shared });
    const c2 = createCapsule({ trigger: shared });
    c1.trigger.push('new_signal');
    assert.equal(c2.trigger.length, 1, 'trigger arrays should not share references');
    assert.equal(shared.length, 1, 'original partial array should not be mutated');
  });

  it('passes through extra fields not in defaults (e.g. diff_snapshot, failure_reason)', () => {
    const c = createCapsule({ id: 'f1', diff_snapshot: 'diff', failure_reason: 'timeout' });
    assert.equal(c.diff_snapshot, 'diff');
    assert.equal(c.failure_reason, 'timeout');
  });
});

describe('validateCapsule', () => {
  function validCapsule(overrides) {
    return createCapsule({
      id: 'cap-valid',
      outcome: { status: 'success', score: 0.8 },
      trigger: ['error'],
      execution_trace: [{ step: 'apply' }],
      ...overrides,
    });
  }

  it('passes for a valid Capsule', () => {
    assert.doesNotThrow(() => validateCapsule(validCapsule()));
  });

  it('throws when capsule is null', () => {
    assert.throws(() => validateCapsule(null), /must be an object/);
  });

  it('throws when type is not "Capsule"', () => {
    assert.throws(() => validateCapsule(validCapsule({ type: 'Gene' })), /type must be "Capsule"/);
  });

  it('throws when id is missing', () => {
    assert.throws(() => validateCapsule(validCapsule({ id: null })), /id is required/);
  });

  it('throws when id is empty string', () => {
    assert.throws(() => validateCapsule(validCapsule({ id: '' })), /id is required/);
  });

  it('throws when outcome is missing', () => {
    assert.throws(
      () => validateCapsule({ type: 'Capsule', id: 'c1', outcome: null, trigger: [], execution_trace: [] }),
      /outcome must be an object/,
    );
  });

  it('throws when outcome.status is invalid', () => {
    assert.throws(
      () => validateCapsule({ type: 'Capsule', id: 'c1', outcome: { status: 'pending', score: 0 }, trigger: [], execution_trace: [] }),
      /outcome\.status must be one of/,
    );
  });

  it('throws when trigger is not an array', () => {
    assert.throws(
      () => validateCapsule({ type: 'Capsule', id: 'c1', outcome: { status: 'success', score: 0.8 }, trigger: 'oops', execution_trace: [] }),
      /trigger must be an array/,
    );
  });

  it('throws when execution_trace is not an array', () => {
    assert.throws(
      () => validateCapsule({ type: 'Capsule', id: 'c1', outcome: { status: 'success', score: 0.8 }, trigger: [], execution_trace: 'oops' }),
      /execution_trace must be an array/,
    );
  });

  it('returns true on success', () => {
    assert.equal(validateCapsule(validCapsule()), true);
  });
});

describe('createCapsule — spec 1.8.0 §Appendix C user-authored fields', () => {
  it('defaults visibility/scope/cost_tier/pack_of/author to null', () => {
    const c = createCapsule({});
    assert.equal(c.visibility, null);
    assert.equal(c.scope, null);
    assert.equal(c.cost_tier, null);
    assert.equal(c.pack_of, null);
    assert.equal(c.author, null);
  });

  it('preserves valid visibility values', () => {
    for (const v of ['private', 'unlisted', 'public']) {
      assert.equal(createCapsule({ visibility: v }).visibility, v);
    }
  });

  it('coerces invalid visibility to null', () => {
    assert.equal(createCapsule({ visibility: 'leaky' }).visibility, null);
  });

  it('preserves scope as a fresh array copy', () => {
    const shared = ['rust', 'debug'];
    const c1 = createCapsule({ scope: shared });
    const c2 = createCapsule({ scope: shared });
    c1.scope.push('extra');
    assert.equal(c2.scope.length, 2, 'scope arrays must not share references');
  });

  it('coerces non-array scope to null', () => {
    assert.equal(createCapsule({ scope: 'not-an-array' }).scope, null);
  });

  it('preserves valid cost_tier values', () => {
    for (const t of ['cheap', 'standard', 'premium']) {
      assert.equal(createCapsule({ cost_tier: t }).cost_tier, t);
    }
  });

  it('coerces invalid cost_tier to null', () => {
    assert.equal(createCapsule({ cost_tier: 'free' }).cost_tier, null);
  });

  it('preserves valid author object', () => {
    const c = createCapsule({ author: { handle: 'evox', evox_install_id: 'evox_install_x' } });
    assert.deepEqual(c.author, { handle: 'evox', evox_install_id: 'evox_install_x' });
  });

  it('drops author when handle is missing', () => {
    assert.equal(createCapsule({ author: { evox_install_id: 'x' } }).author, null);
  });

  it('drops author when evox_install_id is missing', () => {
    // Schema declares both fields required when author is present.
    // A partial pair would be written half-formed and fail validation
    // downstream — drop the field entirely.
    assert.equal(createCapsule({ author: { handle: 'alice' } }).author, null);
  });

  it('strips extra keys from author object (additionalProperties:false guard)', () => {
    const c = createCapsule({
      author: { handle: 'evox', evox_install_id: 'x', extra: 'should-be-stripped' },
    });
    assert.deepEqual(c.author, { handle: 'evox', evox_install_id: 'x' });
  });
});
