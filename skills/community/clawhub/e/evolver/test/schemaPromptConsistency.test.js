'use strict';

// Schema/Prompt consistency guard.
//
// Background: prior to v1.80.8, src/gep/prompt.js hardcoded "repair|optimize|innovate"
// in three schema literals. When 'explore' was added to VALID_CATEGORIES in
// schemas/gene.js, the prompt did not pick it up — agents could never emit a
// Mutation/EvolutionEvent/Gene with category 'explore'.
//
// This test fails if any enum literal that lives in src/gep/schemas/ drifts
// out of sync with what the LLM-facing prompt declares. It also fails if a new
// enum is added to schemas/protocol.js without being woven into the prompt.

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const path = require('path');

const {
  VALID_CATEGORIES,
  VALID_OUTCOME_STATUSES,
  VALID_RISK_LEVELS,
  VALID_TRACE_STAGES,
  renderEnum,
  renderEnumList,
} = require('../src/gep/schemas/protocol');

// Pull the fully-rendered SCHEMA_DEFINITIONS that prompt.js exposes for tests.
function getSchemaText() {
  // Force a fresh require so the module-level SCHEMA_DEFINITIONS is rebuilt
  // when this file is run after another test that mutated env vars.
  delete require.cache[require.resolve('../src/gep/prompt')];
  const promptMod = require('../src/gep/prompt');
  // SCHEMA_DEFINITIONS is not exported directly today; rebuild the same way
  // prompt.js does, using the same single source of truth. If both come out
  // identical we know prompt.js's view of these enums is in sync with schemas/.
  const expected = [
    `"${renderEnum(VALID_CATEGORIES)}"`,
    `"${renderEnum(VALID_RISK_LEVELS)}"`,
    `"${renderEnum(VALID_OUTCOME_STATUSES)}"`,
    `{${renderEnumList(VALID_TRACE_STAGES)}}`,
  ];
  return { promptMod, expected };
}

describe('schema/prompt enum consistency', () => {
  it('VALID_CATEGORIES stays in sync between schemas/gene.js and the LLM prompt', () => {
    // The prompt pipeline pulls VALID_CATEGORIES via schemas/protocol.js, which
    // in turn re-exports from schemas/gene.js. If someone deletes that re-export
    // or breaks the pipeline, these arrays will diverge.
    const { VALID_CATEGORIES: fromGene } = require('../src/gep/schemas/gene');
    assert.deepEqual(VALID_CATEGORIES, fromGene,
      'protocol.js must re-export VALID_CATEGORIES from gene.js — see src/gep/schemas/protocol.js');
    assert.ok(VALID_CATEGORIES.includes('explore'),
      "'explore' must remain a valid category — removing it requires audit of strategy.js presets");
  });

  it('VALID_OUTCOME_STATUSES stays in sync with schemas/capsule.js', () => {
    const { VALID_OUTCOME_STATUSES: fromCapsule } = require('../src/gep/schemas/capsule');
    assert.deepEqual(VALID_OUTCOME_STATUSES, fromCapsule);
  });

  it('SCHEMA_DEFINITIONS in prompt.js renders every enum from protocol.js', () => {
    // We render the schema text the same way prompt.js does and assert the
    // expected enum strings appear verbatim. This catches drift in two ways:
    //   1. Someone adds a value to VALID_CATEGORIES but forgets to use it (the
    //      rendered string would change → expected would too → still passes,
    //      but downstream tests that grep the prompt would catch it).
    //   2. Someone hardcodes a literal in prompt.js that diverges from the
    //      protocol.js render — this test would fail because the rendered
    //      string would no longer be present.
    const { promptMod, expected } = getSchemaText();

    // Build a tiny prompt and inspect the schema region for each expected literal.
    const prompt = promptMod.buildGepPrompt({
      nowIso: '2026-01-01T00:00:00.000Z',
      context: '',
      signals: ['test_signal'],
      selector: { selectedBy: 'test' },
      parentEventId: null,
      selectedGene: null,
      capsuleCandidates: '(none)',
      genesPreview: '[]',
      eventsPreview: '[]',
      personalityHint: null,
      hubMatchedCapsule: null,
      hubMatchScore: null,
      maxLen: 1000000,
    });

    for (const lit of expected) {
      assert.ok(prompt.includes(lit),
        `prompt is missing enum literal ${lit} — likely drift between schemas/protocol.js and prompt.js. ` +
        `Add it to renderEnum() / renderEnumList() output, do not hardcode.`);
    }
  });

  it('prompt.js does NOT contain hardcoded category enums (drift guard)', () => {
    // Read the source of prompt.js directly. If anyone re-introduces the old
    // pattern "repair|optimize|innovate" as a string literal, this test fails
    // and points the contributor at protocol.js.
    const fs = require('fs');
    const src = fs.readFileSync(path.resolve(__dirname, '../src/gep/prompt.js'), 'utf8');

    // The bad pattern is a literal triplet without 'explore' — the exact bug
    // we shipped in v1.80.7 and patched in v1.80.8.
    const badPattern = /["']repair\|optimize\|innovate["'](?!\|explore)/;
    const match = src.match(badPattern);
    assert.equal(match, null,
      `prompt.js contains a hardcoded category enum that omits 'explore'. ` +
      `Use renderEnum(VALID_CATEGORIES) from schemas/protocol.js instead. ` +
      `See: ${match ? src.slice(Math.max(0, match.index - 40), match.index + 60) : ''}`);

    // Also forbid the full quartet from being inlined as a literal — even with
    // 'explore' included, hardcoding it bypasses the single-source rule.
    const inlineQuartet = /["']repair\|optimize\|innovate\|explore["']/;
    assert.equal(src.match(inlineQuartet), null,
      `prompt.js inlines 'repair|optimize|innovate|explore' as a literal — ` +
      `this defeats schemas/protocol.js. Use renderEnum(VALID_CATEGORIES).`);
  });
});
