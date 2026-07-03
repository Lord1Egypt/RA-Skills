'use strict';

const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');
const os = require('os');

const skill2recipes = require('../src/gep/skill2recipes');

// A SKILL.md whose validation section uses a node-only command, so it survives
// the GEP validation allow-list (node/npm/npx) AND runs successfully in a temp
// repoRoot (node --version always exits 0). `--version` is genuinely runnable,
// so the strict-mode "no fallback validation" check passes too.
// Write a real script INTO repoRoot that exits non-zero. policyCheck skips a
// `node <relative>.js` whose target is absent from repoRoot (EvoMap/evolver#562),
// so a missing script "validates nothing" rather than failing -- we need the
// script to actually exist and exit 1 to exercise the failure path.
function writeFailingScript(repoRoot) {
  fs.writeFileSync(path.join(repoRoot, 'fail.js'), 'process.exit(1);\n', 'utf8');
  return 'node fail.js';
}

function writeSkill(dir, name, validationCmd) {
  fs.mkdirSync(dir, { recursive: true });
  // Derive UNIQUE signals from the skill name. assetStore seeds a fresh
  // GEP_ASSETS_DIR from ~11 bundled starter genes on first run, and
  // synthesizeGene rejects a draft whose signals_match fully overlaps an
  // existing gene. Distinct per-skill signals keep every test gene novel.
  const slug = String(name).replace(/[^a-z0-9]+/gi, '_').toLowerCase();
  const sigs = [slug + '_alpha', slug + '_beta', slug + '_gamma'].join(', ');
  const md = [
    '---',
    'name: ' + name,
    'description: Repair ' + name + ' flow. Triggers: ' + sigs + '.',
    '---',
    '',
    '# ' + name,
    '',
    '## When to use',
    'Use when: ' + sigs + ' appear in logs.',
    '',
    '## Workflow',
    '1. Inspect the failing assertion and locate the rounding step.',
    '2. Apply the smallest targeted fix to the total computation.',
    '3. Re-run the validation command and abort if it fails.',
    '',
    '## Avoid',
    '- Do not refactor unrelated modules in the same change.',
    '',
    '## Validation',
    '```bash',
    validationCmd,
    '```',
    '',
  ].join('\n');
  fs.writeFileSync(path.join(dir, 'SKILL.md'), md, 'utf8');
}

let tmpDir;
const saved = {};
const ENV_KEYS = ['GEP_ASSETS_DIR', 'MEMORY_DIR', 'EVOLUTION_DIR', 'EVOLVER_REPO_ROOT', 'A2A_NODE_ID', 'A2A_HUB_URL', 'SOLIDIFY_MAX_RETRIES'];

function setup() {
  tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 's2r-test-'));
  ENV_KEYS.forEach((k) => { saved[k] = process.env[k]; });
  process.env.GEP_ASSETS_DIR = path.join(tmpDir, 'assets');
  process.env.MEMORY_DIR = path.join(tmpDir, 'memory');
  process.env.EVOLUTION_DIR = path.join(tmpDir, 'memory', 'evolution');
  process.env.EVOLVER_REPO_ROOT = tmpDir;
  process.env.A2A_NODE_ID = 'node_' + 'a'.repeat(12);
  // Don't retry-sleep on intentionally-failing validation commands in tests.
  process.env.SOLIDIFY_MAX_RETRIES = '0';
  // No hub URL -> all network paths short-circuit to no_hub_url; we drive with
  // publish:false anyway, so nothing hits the network.
  delete process.env.A2A_HUB_URL;
}

function teardown() {
  ENV_KEYS.forEach((k) => {
    if (saved[k] === undefined) delete process.env[k];
    else process.env[k] = saved[k];
  });
  try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (_) {}
}

describe('skill2recipes.normalizeManifest', () => {
  it('accepts a bare array of paths', () => {
    const m = skill2recipes.normalizeManifest(['./a', './b'], { title: 'My Recipe' });
    assert.equal(m.title, 'My Recipe');
    assert.equal(m.steps.length, 2);
    assert.equal(m.steps[0].skill_path, './a');
    assert.equal(m.steps[0].position, 0);
    assert.equal(m.steps[1].position, 1);
  });

  it('preserves optional/condition and assigns positions', () => {
    const m = skill2recipes.normalizeManifest({
      title: 'R',
      steps: [
        { skill_path: './a' },
        { skill_path: './b', optional: true, condition: 'if x' },
      ],
    });
    assert.equal(m.steps[1].optional, true);
    assert.equal(m.steps[1].condition, 'if x');
    assert.equal(m.steps[1].position, 1);
  });

  it('lets opts override manifest title/price', () => {
    const m = skill2recipes.normalizeManifest({ title: 'old', price_per_execution: 5 }, { title: 'new', pricePerExecution: 99 });
    assert.equal(m.title, 'new');
    assert.equal(m.price_per_execution, 99);
  });
});

describe('skill2recipes.hydrolyzeAndVerify', () => {
  beforeEach(setup);
  afterEach(teardown);

  it('hydrolyzes a skill into a Gene and verifies it with a real trace', () => {
    const dir = path.join(tmpDir, 'skills', 'fix');
    writeSkill(dir, 'fix-checkout', 'node --version');
    const res = skill2recipes.hydrolyzeAndVerify({ skill_path: dir, optional: false }, { repoRoot: tmpDir });
    assert.equal(res.ok, true, JSON.stringify(res.diagnostic));
    assert.equal(res.gene.type, 'Gene');
    assert.equal(res.capsule.type, 'Capsule');
    assert.equal(res.execution.status, 'success');
    // The capsule's trace must cover the gene's validation (skill2gep coverage).
    const traceCmds = res.capsule.execution_trace.map((t) => t.cmd);
    assert.ok(traceCmds.includes('node --version'));
  });

  it('fails a required step whose validation command exits non-zero', () => {
    const dir = path.join(tmpDir, 'skills', 'broken');
    // node -e with a non-zero exit is allowed by the prefix check but fails.
    const failCmd = writeFailingScript(tmpDir);
    writeSkill(dir, 'broken-fix', failCmd);
    const res = skill2recipes.hydrolyzeAndVerify({ skill_path: dir, optional: false }, { repoRoot: tmpDir });
    assert.equal(res.ok, false);
    assert.equal(res.diagnostic.reason, 'validation_failed');
  });

  it('reports skill_path_missing for a nonexistent path', () => {
    const res = skill2recipes.hydrolyzeAndVerify({ skill_path: path.join(tmpDir, 'nope') }, { repoRoot: tmpDir });
    assert.equal(res.ok, false);
    assert.equal(res.diagnostic.reason, 'skill_path_missing');
  });
});

describe('skill2recipes.composeRecipeFromSkills (dry run, publish:false)', () => {
  beforeEach(setup);
  afterEach(teardown);

  it('builds recipe steps referencing Gene asset_ids without touching the network', async () => {
    const a = path.join(tmpDir, 'skills', 'a');
    const b = path.join(tmpDir, 'skills', 'b');
    writeSkill(a, 'step-a', 'node --version');
    writeSkill(b, 'step-b', 'node --version');

    const res = await skill2recipes.composeRecipeFromSkills(
      { title: 'Two Step Pipeline', steps: [{ skill_path: a }, { skill_path: b }] },
      { publish: false, repoRoot: tmpDir },
    );

    // publish:false -> postRecipe is skipped; recipe.publish is skipped marker.
    // ok reflects recipe creation which we did not perform, so assert on steps.
    assert.equal(res.steps.length, 2);
    res.steps.forEach((s) => {
      assert.equal(s.asset_type, 'Gene');
      assert.match(s.asset_id, /^sha256:[a-f0-9]{64}$/);
      assert.match(s.capsule_asset_id, /^sha256:[a-f0-9]{64}$/);
    });
    assert.notEqual(res.steps[0].asset_id, res.steps[1].asset_id);
  });

  it('aborts the whole recipe when a required step fails to verify', async () => {
    const good = path.join(tmpDir, 'skills', 'good');
    const bad = path.join(tmpDir, 'skills', 'bad');
    writeSkill(good, 'good-step', 'node --version');
    writeSkill(bad, 'bad-step', writeFailingScript(tmpDir));

    const res = await skill2recipes.composeRecipeFromSkills(
      { title: 'Has A Bad Step', steps: [{ skill_path: good }, { skill_path: bad }] },
      { publish: false, repoRoot: tmpDir },
    );
    assert.equal(res.ok, false);
    assert.equal(res.reason, 'step_failed');
    assert.equal(res.skill_path, bad);
  });

  it('skips an optional step that fails instead of aborting', async () => {
    const good = path.join(tmpDir, 'skills', 'good2');
    const bad = path.join(tmpDir, 'skills', 'bad2');
    writeSkill(good, 'good-step2', 'node --version');
    writeSkill(bad, 'bad-step2', writeFailingScript(tmpDir));

    const res = await skill2recipes.composeRecipeFromSkills(
      { title: 'Optional Bad Step', steps: [{ skill_path: good }, { skill_path: bad, optional: true }] },
      { publish: false, repoRoot: tmpDir },
    );
    assert.equal(res.steps.length, 1);
    assert.equal(res.skipped.length, 1);
    assert.equal(res.skipped[0].skill_path, bad);
  });

  it('rejects a recipe with a too-short title', async () => {
    const res = await skill2recipes.composeRecipeFromSkills({ title: 'ab', steps: ['./x'] }, { publish: false, repoRoot: tmpDir });
    assert.equal(res.ok, false);
    assert.equal(res.reason, 'title_min_3_chars');
  });
});
