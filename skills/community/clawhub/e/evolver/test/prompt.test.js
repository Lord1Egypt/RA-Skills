const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const path = require('path');

const savedEnv = {};
const envKeys = ['EVOLVER_REPO_ROOT', 'WORKSPACE_DIR', 'OPENCLAW_WORKSPACE', 'MEMORY_DIR', 'EVOLUTION_DIR'];

beforeEach(() => {
  for (const k of envKeys) { savedEnv[k] = process.env[k]; }
  process.env.EVOLVER_REPO_ROOT = path.resolve(__dirname, '..');
});

afterEach(() => {
  for (const k of envKeys) {
    if (savedEnv[k] === undefined) delete process.env[k];
    else process.env[k] = savedEnv[k];
  }
});

function buildMinimalPrompt(overrides) {
  const { buildGepPrompt } = require('../src/gep/prompt');
  return buildGepPrompt({
    nowIso: '2026-01-01T00:00:00.000Z',
    context: '',
    signals: ['test_signal'],
    selector: { selectedBy: 'test' },
    parentEventId: null,
    selectedGene: null,
    capsuleCandidates: '(none)',
    genesPreview: '[]',
    capsulesPreview: '[]',
    capabilityCandidatesPreview: '(none)',
    externalCandidatesPreview: '(none)',
    hubMatchedBlock: '',
    cycleId: '0001',
    recentHistory: '',
    failedCapsules: [],
    hubLessons: [],
    strategyPolicy: null,
    initialUserPrompt: null,
    ...overrides,
  });
}

describe('buildGepPrompt -- prompt does not contain inline status write', () => {
  it('does not embed node -e status file command in prompt', () => {
    const prompt = buildMinimalPrompt();
    assert.ok(!prompt.includes('mkdirSync'), 'prompt should NOT contain mkdirSync (status write moved to wrapper)');
    assert.ok(!prompt.includes('writeFileSync'), 'prompt should NOT contain writeFileSync');
    assert.ok(!prompt.includes('status_'), 'prompt should NOT contain status file references');
  });

  it('does not contain POST-SOLIDIFY block', () => {
    const prompt = buildMinimalPrompt();
    assert.ok(!prompt.includes('POST-SOLIDIFY'), 'prompt should NOT contain POST-SOLIDIFY block');
    assert.ok(!prompt.includes('Wrapper Authority'), 'prompt should NOT contain Wrapper Authority header');
  });

  it('does not contain bash heredoc patterns', () => {
    const prompt = buildMinimalPrompt();
    assert.ok(!prompt.includes('cat >'), 'prompt should NOT contain bash cat > redirect');
    assert.ok(!prompt.includes('STATUSEOF'), 'prompt should NOT contain heredoc delimiter');
    assert.ok(!prompt.includes('<< '), 'prompt should NOT contain heredoc operator');
  });
});

describe('buildGepPrompt -- structure', () => {
  it('contains GEP protocol header', () => {
    const prompt = buildMinimalPrompt();
    assert.ok(prompt.includes('GEP'), 'prompt should contain GEP header');
    assert.ok(prompt.includes('GENOME EVOLUTION PROTOCOL'), 'prompt should contain full protocol name');
  });

  it('contains mandatory object model section', () => {
    const prompt = buildMinimalPrompt();
    assert.ok(prompt.includes('Mutation'), 'prompt should contain Mutation object');
    assert.ok(prompt.includes('PersonalityState'), 'prompt should contain PersonalityState');
    assert.ok(prompt.includes('EvolutionEvent'), 'prompt should contain EvolutionEvent');
    assert.ok(prompt.includes('Gene'), 'prompt should contain Gene');
    assert.ok(prompt.includes('Capsule'), 'prompt should contain Capsule');
  });

  it('contains constitutional ethics section', () => {
    const prompt = buildMinimalPrompt();
    assert.ok(prompt.includes('CONSTITUTIONAL ETHICS'), 'prompt should contain ethics section');
    assert.ok(prompt.includes('HUMAN WELFARE'), 'prompt should contain human welfare principle');
  });

  it('contains cycle ID in report requirement', () => {
    const prompt = buildMinimalPrompt({ cycleId: '0099' });
    assert.ok(prompt.includes('0099'), 'prompt should reference cycle ID');
  });
});

describe('buildGepPrompt -- Context [Execution] is preserved under preview bloat (public issue #552)', () => {
  // Public issue EvoMap/evolver#552: when Gene/Capsule preview entries
  // carried large fields (capsule.diff ~8KB+ each, gene.learning_history
  // and anti_patterns), the prompt prefix overflowed maxChars (default
  // 50_000) and the truncation step zeroed out Context [Execution] —
  // subagents received no execution instructions.
  //
  // Two-part fix:
  //   1. PREVIEW_STRIP_FIELDS removes the bloated fields before formatting
  //      so a normal load no longer needs to truncate at all.
  //   2. An Execution-context floor in the truncator: even if the prefix
  //      still exceeds the budget, Context [Execution] gets at least
  //      EXEC_FLOOR (8000) chars — the prefix is truncated instead.

  const HEAVY_DIFF = 'a'.repeat(9000); // matches the ~8.5KB the reporter measured

  // Mirrors the production shape from src/evolve/pipeline/dispatch.js:182-183
  // exactly — ```json\n<pretty>\n``` markdown code fence. Bugbot PR #162
  // HIGH: a raw JSON.stringify(...) input slipped past the strip because
  // JSON.parse threw on the fences and the catch silently returned the
  // bloated string. These helpers and the assertions below ensure the
  // fenced production format is exercised end-to-end.
  function fencedJson(arr) {
    return '```json\n' + JSON.stringify(arr, null, 2) + '\n```';
  }

  function bloatedCapsules(count) {
    return fencedJson(
      Array.from({ length: count }, (_, i) => ({
        type: 'Capsule',
        id: 'cap_' + i,
        summary: 'cap summary ' + i,
        diff: HEAVY_DIFF,                  // stripped by fix
        compact_diff: HEAVY_DIFF,          // stripped by fix
        execution_trace: HEAVY_DIFF,       // stripped by fix
      })),
    );
  }

  function bloatedGenes(count) {
    return fencedJson(
      Array.from({ length: count }, (_, i) => ({
        type: 'Gene',
        id: 'gene_' + i,
        summary: 'gene summary ' + i,
        learning_history: HEAVY_DIFF,      // stripped by fix
        anti_patterns: HEAVY_DIFF,         // stripped by fix
        evolution_history: HEAVY_DIFF,     // stripped by fix
      })),
    );
  }

  it('does NOT inline capsule.diff / gene.learning_history into the prompt', () => {
    const prompt = buildMinimalPrompt({
      capsulesPreview: bloatedCapsules(3),
      genesPreview: bloatedGenes(2),
    });
    assert.ok(!prompt.includes(HEAVY_DIFF),
      'prompt MUST NOT include the bloated diff/learning_history payload');
    // The lightweight summary fields still survive — strategy phase still
    // sees the asset identities.
    assert.ok(prompt.includes('cap summary 0'), 'capsule summary still present');
    assert.ok(prompt.includes('gene summary 0'), 'gene summary still present');
  });

  it('keeps Context [Execution] non-empty under heavy preview bloat (#552 regression)', () => {
    // Distinctive execution-context payload we can assert survives.
    const execMarker = 'EXEC_MARKER_PRESERVED_UNDER_BLOAT';
    const prompt = buildMinimalPrompt({
      context: execMarker + '\n' + 'x'.repeat(2000),
      capsulesPreview: bloatedCapsules(5),
      genesPreview: bloatedGenes(5),
    });

    const execIndex = prompt.indexOf('Context [Execution]:');
    assert.ok(execIndex !== -1, 'Context [Execution] header must be present');
    const execSection = prompt.slice(execIndex + 'Context [Execution]:'.length);
    assert.ok(execSection.length > 50,
      'Execution section MUST contain substantive content, not just "...[TRUNCATED]..." (#552)');
    assert.ok(execSection.includes(execMarker),
      'the execution context payload MUST survive — got: ' + execSection.slice(0, 200));
  });

  it('_compactPreviewForPrompt strips diff from dispatch.js markdown-fenced input (Bugbot PR #162 HIGH)', () => {
    // src/evolve/pipeline/dispatch.js:182-183 wraps previews as
    //   `\`\`\`json\n${JSON.stringify(arr, null, 2)}\n\`\`\``
    // Pre-fix, _compactPreviewForPrompt naive-JSON.parse'd that fenced
    // string, threw, and the catch silently returned the original bloated
    // string. The strip was a no-op in production while the older tests
    // passed on raw-JSON inputs.
    //
    // Test the helper DIRECTLY rather than through buildGepPrompt — the
    // downstream truncator's prefix-floor can incidentally cut off
    // HEAVY_DIFF and mask a broken strip when asserted at the prompt level.
    const { __internals } = require('../src/gep/prompt');
    const productionShape = '```json\n' + JSON.stringify([
      { type: 'Capsule', id: 'cap_prod', summary: 's', diff: HEAVY_DIFF },
    ], null, 2) + '\n```';
    const compacted = __internals.compactPreviewForPrompt(productionShape);
    assert.ok(typeof compacted === 'string', 'string in → string out');
    assert.ok(!compacted.includes(HEAVY_DIFF),
      'diff MUST be stripped from the fenced production-shape input — pre-fix this was a silent no-op');
    assert.ok(compacted.includes('cap_prod'),
      'lightweight id must still appear after the strip');
    assert.ok(compacted.startsWith('```json') && compacted.endsWith('```'),
      'fence wrapper must be preserved so the LLM still sees a markdown code block — got first 30 chars: ' + JSON.stringify(compacted.slice(0, 30)));
  });

  it('floor protection truncates the prefix, not Execution, when maxChars is tight', () => {
    // Force a tight budget and a pre-bloated prefix that the strip helper
    // alone would not bring under budget. The floor must still preserve
    // Execution by truncating the prefix.
    const origMax = process.env.GEP_PROMPT_MAX_CHARS;
    process.env.GEP_PROMPT_MAX_CHARS = '15000'; // smaller than typical prefix
    try {
      const execMarker = 'FLOOR_PROTECTION_EXEC_MARKER';
      const prompt = buildMinimalPrompt({
        context: execMarker + '\n' + 'y'.repeat(5000),
        capsulesPreview: bloatedCapsules(3),
        genesPreview: bloatedGenes(3),
      });

      const execIndex = prompt.indexOf('Context [Execution]:');
      assert.ok(execIndex !== -1, 'Execution header must survive');
      const execSection = prompt.slice(execIndex + 'Context [Execution]:'.length);
      assert.ok(execSection.includes(execMarker),
        'floor protection MUST preserve the start of Execution content even under a tight maxChars budget');

      // The CONTEXT_TRUNCATED marker is the signal that floor protection
      // truncated the PREFIX (not the Execution).
      assert.ok(prompt.includes('CONTEXT_TRUNCATED_TO_PRESERVE_EXECUTION'),
        'expected the prefix-truncation marker to appear');
    } finally {
      if (origMax === undefined) delete process.env.GEP_PROMPT_MAX_CHARS;
      else process.env.GEP_PROMPT_MAX_CHARS = origMax;
    }
  });
});
