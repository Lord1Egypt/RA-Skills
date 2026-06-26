'use strict';

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const { createGene, validateGene, VALID_CATEGORIES } = require('../src/gep/schemas/gene');

describe('createGene', () => {
  it('returns a fully-formed Gene with all defaults when called with empty object', () => {
    const g = createGene({});
    assert.equal(g.type, 'Gene');
    assert.equal(g.category, 'innovate');
    assert.deepEqual(g.signals_match, []);
    assert.deepEqual(g.strategy, []);
    assert.deepEqual(g.validation, []);
    assert.deepEqual(g.preconditions, []);
    assert.deepEqual(g.epigenetic_marks, []);
    assert.deepEqual(g.learning_history, []);
    assert.deepEqual(g.anti_patterns, []);
    assert.equal(g.constraints.max_files, 20);
    assert.ok(g.constraints.forbidden_paths.includes('.git'));
    assert.equal(g.schema_version, '1.6.0');
    assert.equal(g.summary, '');
  });

  it('preserves provided fields', () => {
    const g = createGene({ id: 'g1', category: 'repair', signals_match: ['log_error'], summary: 'Fix bugs' });
    assert.equal(g.id, 'g1');
    assert.equal(g.category, 'repair');
    assert.deepEqual(g.signals_match, ['log_error']);
    assert.equal(g.summary, 'Fix bugs');
  });

  it('is idempotent — createGene(createGene(x)) equals createGene(x)', () => {
    const input = { id: 'g2', category: 'optimize', signals_match: ['perf'], strategy: ['step1'] };
    const once = createGene(input);
    const twice = createGene(once);
    assert.deepEqual(once, twice);
  });

  it('normalizes invalid category to default', () => {
    const g = createGene({ category: 'unknown_cat' });
    assert.equal(g.category, 'innovate');
  });

  it('normalizes null/missing category to default', () => {
    const g = createGene({ category: null });
    assert.equal(g.category, 'innovate');
  });

  it('normalizes non-array signals_match to []', () => {
    const g = createGene({ signals_match: 'not-an-array' });
    assert.deepEqual(g.signals_match, []);
  });

  it('normalizes missing constraints to defaults', () => {
    const g = createGene({ constraints: null });
    assert.equal(g.constraints.max_files, 20);
    assert.ok(g.constraints.forbidden_paths.includes('.git'));
  });

  it('merges partial constraints with defaults', () => {
    const g = createGene({ constraints: { max_files: 5 } });
    assert.equal(g.constraints.max_files, 5);
    assert.ok(g.constraints.forbidden_paths.includes('.git'));
  });

  it('normalizes empty forbidden_paths to default', () => {
    const g = createGene({ constraints: { forbidden_paths: [] } });
    assert.ok(g.constraints.forbidden_paths.includes('.git'));
  });

  it('accepts all valid categories', () => {
    for (const cat of VALID_CATEGORIES) {
      const g = createGene({ category: cat });
      assert.equal(g.category, cat);
    }
  });

  it('returns independent array instances — mutation does not contaminate other genes', () => {
    const g1 = createGene({ id: 'g1' });
    const g2 = createGene({ id: 'g2' });
    g1.epigenetic_marks.push({ context: 'test', boost: -0.5 });
    g1.learning_history.push({ result: 'success' });
    g1.anti_patterns.push('bad_pattern');
    assert.deepEqual(g2.epigenetic_marks, [], 'epigenetic_marks should be independent');
    assert.deepEqual(g2.learning_history, [], 'learning_history should be independent');
    assert.deepEqual(g2.anti_patterns, [], 'anti_patterns should be independent');
  });

  it('returns independent array instances even when partial provides arrays', () => {
    const shared = ['log_error'];
    const g1 = createGene({ signals_match: shared });
    const g2 = createGene({ signals_match: shared });
    g1.signals_match.push('new_signal');
    assert.equal(g2.signals_match.length, 1, 'signals_match arrays should not share references');
    assert.equal(shared.length, 1, 'original partial array should not be mutated');
  });

  // routing_hint / tool_policy are the EvoX-side optional fields wired
  // through `crates/evox-evo-session/src/lifecycle.rs`. Field name and
  // enum string drift here would silently degrade to "no opinion" on
  // the Rust side rather than throw — guard against that here.
  it('defaults routing_hint and tool_policy to null when omitted', () => {
    const g = createGene({});
    assert.equal(g.routing_hint, null);
    assert.equal(g.tool_policy, null);
  });

  it('preserves a well-formed routing_hint', () => {
    const g = createGene({ routing_hint: { tier: 'cheap', reasoning_level: 'low' } });
    assert.deepEqual(g.routing_hint, { tier: 'cheap', reasoning_level: 'low' });
  });

  it('drops unknown tier values to null (no silent fallback to a default tier)', () => {
    // The Rust enum match in lifecycle.rs is exhaustive; a stray tier
    // would simply be ignored and the gene would emit no hint. Mirror
    // that here so the JSON written to disk does not mislead.
    const g = createGene({ routing_hint: { tier: 'ultra', reasoning_level: 'low' } });
    assert.deepEqual(g.routing_hint, { reasoning_level: 'low' });
  });

  it('drops empty routing_hint object to null', () => {
    const g = createGene({ routing_hint: {} });
    assert.equal(g.routing_hint, null);
  });

  it('preserves a tool_policy with allow_only + severity', () => {
    const g = createGene({ tool_policy: { allow_only: ['read', 'grep'], severity: 'block' } });
    assert.deepEqual(g.tool_policy, { allow_only: ['read', 'grep'], severity: 'block' });
  });

  it('defaults tool_policy.severity to "warn" when omitted but a list is present', () => {
    const g = createGene({ tool_policy: { deny: ['git_force_push'] } });
    assert.deepEqual(g.tool_policy, { deny: ['git_force_push'], severity: 'warn' });
  });

  it('drops a tool_policy with no allow_only or deny to null', () => {
    const g = createGene({ tool_policy: { severity: 'block' } });
    assert.equal(g.tool_policy, null);
  });

  it('drops empty allow_only after filtering, even when deny has entries (Bugbot 66d2145c)', () => {
    // String-falsy entries (`''`) get filtered out and the surviving
    // empty array must NOT leak into the output. On the Rust executor
    // gate an `allow_only: []` reads as "allow zero tools" and silently
    // blocks every tool call when the gene only intended a deny list.
    const g = createGene({
      tool_policy: {
        allow_only: ['', ''],
        deny: ['rm', '-rf'],
        severity: 'block',
      },
    });
    assert.deepEqual(g.tool_policy, { deny: ['rm', '-rf'], severity: 'block' });
    assert.equal(g.tool_policy.allow_only, undefined);
  });

  it('drops empty deny after filtering, even when allow_only has entries (Bugbot 66d2145c)', () => {
    const g = createGene({
      tool_policy: {
        allow_only: ['read'],
        deny: ['', ''],
        severity: 'warn',
      },
    });
    assert.deepEqual(g.tool_policy, { allow_only: ['read'], severity: 'warn' });
    assert.equal(g.tool_policy.deny, undefined);
  });

  it('drops a tool_policy whose lists are present but all-empty after filter', () => {
    const g = createGene({
      tool_policy: { allow_only: [''], deny: [''], severity: 'block' },
    });
    assert.equal(g.tool_policy, null);
  });

  it('routing_hint and tool_policy survive idempotent createGene', () => {
    const input = { id: 'g-rt', category: 'repair', strategy: ['x'],
                    routing_hint: { tier: 'mid' },
                    tool_policy: { deny: ['rm'], severity: 'block' } };
    const once = createGene(input);
    const twice = createGene(once);
    assert.deepEqual(once.routing_hint, twice.routing_hint);
    assert.deepEqual(once.tool_policy, twice.tool_policy);
  });
});

describe('validateGene', () => {
  function validGene(overrides) {
    return createGene({ id: 'g-valid', category: 'repair', strategy: ['do it'], ...overrides });
  }

  it('passes for a valid Gene', () => {
    assert.doesNotThrow(() => validateGene(validGene()));
  });

  it('throws when gene is null', () => {
    assert.throws(() => validateGene(null), /must be an object/);
  });

  it('throws when type is not "Gene"', () => {
    assert.throws(() => validateGene(validGene({ type: 'Capsule' })), /type must be "Gene"/);
  });

  it('throws when id is missing', () => {
    assert.throws(() => validateGene(validGene({ id: null })), /id is required/);
  });

  it('throws when id is empty string', () => {
    assert.throws(() => validateGene(validGene({ id: '' })), /id is required/);
  });

  it('throws when category is invalid', () => {
    // pass raw object — bypasses createGene normalization
    assert.throws(() => validateGene({ type: 'Gene', id: 'g1', category: 'bad', signals_match: [], strategy: [] }), /category must be one of/);
  });

  it('throws when signals_match is not an array', () => {
    assert.throws(() => validateGene({ type: 'Gene', id: 'g1', category: 'repair', signals_match: 'oops', strategy: [] }), /signals_match must be an array/);
  });

  it('throws when strategy is not an array', () => {
    assert.throws(() => validateGene({ type: 'Gene', id: 'g1', category: 'repair', signals_match: [], strategy: 'oops' }), /strategy must be an array/);
  });

  it('returns true on success', () => {
    assert.equal(validateGene(validGene()), true);
  });
});
