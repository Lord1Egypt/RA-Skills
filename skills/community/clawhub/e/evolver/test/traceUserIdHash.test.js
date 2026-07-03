'use strict';

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');

const { extractUserIdHash } = require('../src/proxy/trace/extractor');

function claudeUserId(account, session) {
  return `user_${account}_account__session_${session}`;
}

describe('extractUserIdHash (FIX-1 stable cross-session account fingerprint)', () => {
  it('same account, different sessions -> same user_id_hash', () => {
    const account = 'a1b2c3d4e5f6';
    const bodyA = { metadata: { user_id: claudeUserId(account, '11111111-2222-3333-4444-555555555555') } };
    const bodyB = { metadata: { user_id: claudeUserId(account, 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee') } };
    const hashA = extractUserIdHash({}, bodyA);
    const hashB = extractUserIdHash({}, bodyB);
    assert.ok(hashA, 'hash should be non-empty');
    assert.match(hashA, /^user_id_sha256:[0-9a-f]{16}$/);
    assert.equal(hashA, hashB, 'same account across sessions must collapse to one hash');
  });

  it('different accounts -> different user_id_hash', () => {
    const session = '11111111-2222-3333-4444-555555555555';
    const hashA = extractUserIdHash({}, { metadata: { user_id: claudeUserId('account-aaaa', session) } });
    const hashB = extractUserIdHash({}, { metadata: { user_id: claudeUserId('account-bbbb', session) } });
    assert.ok(hashA && hashB);
    assert.notEqual(hashA, hashB);
  });

  it('does not leak the plaintext account id', () => {
    const account = 'super-secret-account-1234';
    const hash = extractUserIdHash({}, { metadata: { user_id: claudeUserId(account, 'sess-uuid-00000000') } });
    assert.ok(!hash.includes(account));
  });

  it('JSON-string user_id is supported (Claude Code packs identity as a JSON object string)', () => {
    const account = 'json-account-xyz';
    const a = extractUserIdHash({}, { metadata: { user_id: JSON.stringify({ user_id: claudeUserId(account, 'sess-1-aaaaaaaa'), session_id: 'sess-1-aaaaaaaa' }) } });
    const b = extractUserIdHash({}, { metadata: { user_id: JSON.stringify({ user_id: claudeUserId(account, 'sess-2-bbbbbbbb'), session_id: 'sess-2-bbbbbbbb' }) } });
    assert.ok(a);
    assert.equal(a, b);
  });

  it('non-Claude shapes fall back to the whole identity (still deterministic)', () => {
    const a = extractUserIdHash({}, { user: 'plain-user-id-42' });
    const b = extractUserIdHash({}, { user: 'plain-user-id-42' });
    assert.ok(a);
    assert.equal(a, b);
    assert.notEqual(a, extractUserIdHash({}, { user: 'plain-user-id-43' }));
  });

  it('falls back to account headers when body carries no identity', () => {
    const a = extractUserIdHash({ 'x-account-id': 'acct-77' }, {});
    const b = extractUserIdHash({ 'x-account-id': 'acct-77' }, {});
    assert.ok(a);
    assert.equal(a, b);
  });

  it('returns empty string when no identity is present', () => {
    assert.equal(extractUserIdHash({}, {}), '');
    assert.equal(extractUserIdHash({}, { metadata: {} }), '');
  });

  it('does NOT over-truncate a single-underscore _session_ inside a non-Claude account segment', () => {
    // A non-Claude provider whose account ids literally contain `_session_` (single underscore). The old
    // `/_{1,2}session_.*$/i` rule split here too, collapsing distinct accounts onto one hash. Only the
    // double-underscore `__session_` boundary must trigger stripping, so these two accounts stay distinct.
    const a = extractUserIdHash({}, { user: 'acct_session_alpha_region_us' });
    const b = extractUserIdHash({}, { user: 'acct_session_bravo_region_eu' });
    assert.ok(a && b);
    assert.match(a, /^user_id_sha256:[0-9a-f]{16}$/);
    assert.notEqual(a, b, 'single-underscore _session_ accounts must not collapse to the same hash');
  });

  it('still strips the __session_ suffix for real Claude Code ids even when the account also has _session_ text', () => {
    // Account segment itself contains a single-underscore `_session_` token; the rotating suffix is the
    // double-underscore `__session_<uuid>`. Two sessions of the same account must still collapse to one hash.
    const account = 'team_session_pool_9f3a';
    const a = extractUserIdHash({}, { metadata: { user_id: claudeUserId(account, '11111111-2222-3333-4444-555555555555') } });
    const b = extractUserIdHash({}, { metadata: { user_id: claudeUserId(account, 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee') } });
    assert.ok(a && b);
    assert.equal(a, b, 'same account across sessions must still collapse despite an inner _session_ token');
    // And a different account with the same inner token stays distinct.
    const c = extractUserIdHash({}, { metadata: { user_id: claudeUserId('other_session_pool_1c2d', '11111111-2222-3333-4444-555555555555') } });
    assert.notEqual(a, c);
  });
});
