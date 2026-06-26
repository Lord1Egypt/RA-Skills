'use strict';

// Guard: router must never rewrite to a strictly older intra-family model.
// Triggered the 2026-05-25 /compact stall when EVOMAP_MODEL_EXPENSIVE was
// set to opus-4-1 while users sent opus-4-7 — every planning turn silently
// downgraded a generation, hit Bedrock 5xx, then absorbed the cost via
// retry. The guard makes that misconfiguration loud (downgrade_blocked log
// line) instead of silent (latency / occasional 503 leak).

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');

const {
  parseClaudeId,
  isIntraFamilyDowngrade,
} = require('../src/proxy/router/messages_route');

describe('parseClaudeId', () => {
  it('parses global.* IDs', () => {
    assert.deepEqual(parseClaudeId('global.anthropic.claude-opus-4-7'),
      { family: 'opus', major: 4, minor: 7 });
    assert.deepEqual(parseClaudeId('global.anthropic.claude-sonnet-4-7'),
      { family: 'sonnet', major: 4, minor: 7 });
    assert.deepEqual(parseClaudeId('global.anthropic.claude-haiku-4-5'),
      { family: 'haiku', major: 4, minor: 5 });
  });

  it('parses Bedrock dated IDs (us.* prefix + suffix)', () => {
    assert.deepEqual(parseClaudeId('us.anthropic.claude-opus-4-1-20250805-v1:0'),
      { family: 'opus', major: 4, minor: 1 });
    assert.deepEqual(parseClaudeId('us.anthropic.claude-haiku-4-5-20251001-v1:0'),
      { family: 'haiku', major: 4, minor: 5 });
  });

  it('returns null for non-claude / opaque IDs', () => {
    assert.equal(parseClaudeId('gpt-4'), null);
    assert.equal(parseClaudeId('mistral-large-2'), null);
    assert.equal(parseClaudeId(null), null);
    assert.equal(parseClaudeId(undefined), null);
    assert.equal(parseClaudeId(123), null);
  });
});

describe('isIntraFamilyDowngrade', () => {
  it('blocks opus-4-7 -> opus-4-1 (the May incident)', () => {
    assert.equal(isIntraFamilyDowngrade(
      'us.anthropic.claude-opus-4-1-20250805-v1:0',
      'global.anthropic.claude-opus-4-7',
    ), true);
  });

  it('allows opus-4-7 -> opus-4-7 (no-op)', () => {
    assert.equal(isIntraFamilyDowngrade(
      'global.anthropic.claude-opus-4-7',
      'global.anthropic.claude-opus-4-7',
    ), false);
  });

  it('allows opus-4-1 -> opus-4-7 (upgrade)', () => {
    assert.equal(isIntraFamilyDowngrade(
      'global.anthropic.claude-opus-4-7',
      'global.anthropic.claude-opus-4-1-20250805-v1:0',
    ), false);
  });

  it('allows cross-family rewrites (cheap tier core function)', () => {
    // The router's whole point: opus -> haiku for trivial lookups.
    // Cross-family is never a "downgrade" — different generation curves.
    assert.equal(isIntraFamilyDowngrade(
      'global.anthropic.claude-haiku-4-5',
      'global.anthropic.claude-opus-4-7',
    ), false);
    assert.equal(isIntraFamilyDowngrade(
      'global.anthropic.claude-sonnet-4-7',
      'global.anthropic.claude-opus-4-7',
    ), false);
  });

  it('allows rewrites when one side is unparseable (only block what we can prove)', () => {
    assert.equal(isIntraFamilyDowngrade('opaque-vendor-model', 'global.anthropic.claude-opus-4-7'), false);
    assert.equal(isIntraFamilyDowngrade('global.anthropic.claude-opus-4-7', 'opaque-vendor-model'), false);
    assert.equal(isIntraFamilyDowngrade(null, 'global.anthropic.claude-opus-4-7'), false);
  });

  it('handles major-version downgrade (hypothetical claude-5 era)', () => {
    assert.equal(isIntraFamilyDowngrade(
      'global.anthropic.claude-opus-4-7',
      'global.anthropic.claude-opus-5-1',
    ), true);
    assert.equal(isIntraFamilyDowngrade(
      'global.anthropic.claude-opus-5-1',
      'global.anthropic.claude-opus-4-7',
    ), false);
  });
});
