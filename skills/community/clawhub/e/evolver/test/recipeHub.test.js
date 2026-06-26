// P4c — evolver hub recipe helpers. These are plain REST wrappers around the
// hub recipe endpoints (NOT a2a-envelope messages), so VALID_MESSAGE_TYPES is
// unchanged. We exercise them under HUB_DRY_RUN so no network call is made and
// assert the dry-run contract (build defaults to draft: create only, no publish).

const { describe, it, before } = require('node:test');
const assert = require('node:assert/strict');

if (!process.env.A2A_NODE_SECRET) process.env.A2A_NODE_SECRET = 'a'.repeat(64);
process.env.HUB_DRY_RUN = '1';
process.env.A2A_HUB_URL = process.env.A2A_HUB_URL || 'https://dev.evomap.ai';

const {
  VALID_MESSAGE_TYPES,
  hubCreateRecipe,
  hubPublishRecipe,
  hubGetRecipe,
  hubExpressRecipe,
  rotateNodeSecret,
} = require('../src/gep/a2aProtocol');

describe('recipe hub helpers (P4c)', () => {
  it('does NOT add a recipe message type (recipe is plain REST, not a2a envelope)', () => {
    assert.equal(VALID_MESSAGE_TYPES.length, 6);
    assert.ok(!VALID_MESSAGE_TYPES.includes('recipe'));
    assert.ok(!VALID_MESSAGE_TYPES.includes('buildRecipe'));
  });

  it('hubCreateRecipe resolves (dry-run, no network)', async () => {
    const res = await hubCreateRecipe({
      title: 'Test Recipe',
      steps: [{ asset_id: 'sha256:' + 'a'.repeat(64), asset_type: 'Gene', position: 0 }],
    });
    assert.equal(res.ok, true);
    assert.equal(res.dry_run, true);
  });

  it('hubPublishRecipe / hubGetRecipe / hubExpressRecipe resolve (dry-run)', async () => {
    for (const r of [
      await hubPublishRecipe('recipe-1'),
      await hubGetRecipe('recipe-1'),
      await hubExpressRecipe('recipe-1', { foo: 'bar' }),
    ]) {
      assert.equal(r.ok, true);
      assert.equal(r.dry_run, true);
    }
  });

  it('all four helpers are exported as functions', () => {
    for (const fn of [hubCreateRecipe, hubPublishRecipe, hubGetRecipe, hubExpressRecipe]) {
      assert.equal(typeof fn, 'function');
    }
  });

  it('rotateNodeSecret is exported (used by the recipe CLI stale-secret retry)', () => {
    assert.equal(typeof rotateNodeSecret, 'function');
  });
});
