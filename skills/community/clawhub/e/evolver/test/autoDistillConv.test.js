'use strict';

const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawn } = require('node:child_process');

// fake claude: emits a result envelope whose `result` is the given gene object
// (or garbage / structural-invalid per mode), then exits 0 (or nonzero).
function geneEnvelope(geneObj) {
  return JSON.stringify({ type: 'result', is_error: false, result: JSON.stringify(geneObj) });
}
function fakeSpawn(emit, counter, exitCode) {
  return (bin, args, opts) => {
    if (counter) counter.n++;
    const code = `process.stdout.write(${JSON.stringify(emit)}); process.exit(${exitCode || 0});`;
    return spawn(process.execPath, ['-e', code], { ...opts });
  };
}
const GOOD_GENE = {
  type: 'Gene', id: 'gene_distilled_publish-feishu-doc', category: 'innovate',
  signals_match: ['publish_feishu', 'feishu_doc', 'lark_doc'],
  preconditions: ['operator supplies a lark token'],
  strategy: ['Step 1: render markdown', 'Step 2: lark-cli docs +create', 'Step 3: verify url'],
  constraints: { max_files: 3, forbidden_paths: ['.git', 'node_modules'] },
  validation: ['node --version'], schema_version: '1.6.0',
  summary: 'Publish a markdown file as a Feishu doc via lark-cli and return the url.',
};

let tmpRoot, prevEnv;
const ENV = ['EVOLVER_REPO_ROOT', 'EVOLVER_CONV_DISTILL_ENABLED', 'CONV_SLUG_COOLDOWN_MS', 'EVOLVE_DISTILL_VALIDATION_TIMEOUT_MS', 'EVOLVE_DISTILL_TIMEOUT_MS', 'A2A_HUB_URL', 'EVOLVER_CONV_DISTILL_DUP_JACCARD'];

beforeEach(() => {
  prevEnv = {}; for (const k of ENV) prevEnv[k] = process.env[k];
  tmpRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'p2-'));
  process.env.EVOLVER_REPO_ROOT = tmpRoot;
  process.env.A2A_HUB_URL = '';
  fs.mkdirSync(path.join(tmpRoot, '.evolver', 'gep'), { recursive: true });
  fs.writeFileSync(path.join(tmpRoot, '.evolver', 'gep', 'genes.json'), JSON.stringify({ version: 1, genes: [] }));
});
afterEach(() => {
  for (const k of ENV) { if (prevEnv[k] === undefined) delete process.env[k]; else process.env[k] = prevEnv[k]; }
  try { fs.rmSync(tmpRoot, { recursive: true, force: true }); } catch (_) {}
});

function fresh() {
  for (const m of ['paths', 'skillDistiller', 'assetStore', 'autoDistillLlm', 'execBridge', 'policyCheck', 'autoDistillConv']) {
    try { delete require.cache[require.resolve('../src/gep/' + m)]; } catch (_) {}
  }
  return require('../src/gep/autoDistillConv');
}
function seedQueue(mod, cands) { mod.enqueueCandidate(cands); }
function genesOnDisk() { try { return JSON.parse(fs.readFileSync(path.join(tmpRoot, '.evolver', 'gep', 'genes.json'), 'utf8')).genes || []; } catch (_) { return []; } }
function convState() { try { return (JSON.parse(fs.readFileSync(path.join(tmpRoot, 'memory', 'distiller_state.json'), 'utf8')).conv_distill) || {}; } catch (_) { return {}; } }
function fullState() { try { return JSON.parse(fs.readFileSync(path.join(tmpRoot, 'memory', 'distiller_state.json'), 'utf8')); } catch (_) { return {}; } }
const C = (over) => Object.assign({ capability: 'publish-feishu-doc', matched: 'lark-cli', snippet: 'used lark-cli to publish a feishu doc, verified', hash: 'h1' }, over);

describe('autoDistillConv — prompt builder', () => {
  const sd = require('../src/gep/skillDistiller');
  it('includes slug, matched, snippet, light VALIDATION; leaks no full gene bodies', () => {
    const p = sd.buildConversationDistillPrompt(C(), [{ id: 'g_old', category: 'optimize', signals_match: ['x'], strategy: ['SECRET STEP'] }]);
    assert.ok(p.includes('publish-feishu-doc'));
    assert.ok(p.includes('used lark-cli to publish'));
    assert.ok(p.includes('node --version'));
    assert.ok(p.includes('gene_distilled_'));
    assert.ok(!p.includes('SECRET STEP'), 'must not leak existing gene strategy bodies (only id/category/signals)');
  });
});

describe('autoDistillConv — flow', () => {
  it('off mode: disabled', async () => {
    const m = fresh();
    const r = await m.autoDistillConversation({ mode: 'off' });
    assert.equal(r.reason, 'disabled');
  });

  it('queue empty -> queue_empty', async () => {
    const m = fresh();
    const r = await m.autoDistillConversation({ mode: 'shadow' });
    assert.equal(r.reason, 'queue_empty');
  });

  it('happy shadow: synthesize candidate, log, record shadowed_at, NEVER upsert', async () => {
    const m = fresh(); seedQueue(m, C());
    const r = await m.autoDistillConversation({ mode: 'shadow', spawnFn: fakeSpawn(geneEnvelope(GOOD_GENE)) });
    assert.equal(r.ok, true, 'reason=' + r.reason);
    assert.equal(r.mode, 'shadow');
    assert.equal(genesOnDisk().length, 0, 'shadow MUST NOT upsert');
    assert.ok(convState().by_hash.h1.shadowed_at, 'shadowed_at recorded');
  });

  it('enforce is downgraded to shadow in v1 (no upsert)', async () => {
    const m = fresh(); seedQueue(m, C());
    const r = await m.autoDistillConversation({ mode: 'enforce', spawnFn: fakeSpawn(geneEnvelope(GOOD_GENE)) });
    assert.equal(r.mode, 'shadow', 'enforce downgraded to shadow');
    assert.equal(genesOnDisk().length, 0, 'still no upsert');
  });

  it('idempotency: same (slug,snippet) hash not re-spawned after shadow', async () => {
    const m = fresh(); seedQueue(m, C());
    await m.autoDistillConversation({ mode: 'shadow', spawnFn: fakeSpawn(geneEnvelope(GOOD_GENE)) });
    const c = { n: 0 };
    seedQueue(m, C()); // re-enqueue same hash
    const r2 = await m.autoDistillConversation({ mode: 'shadow', spawnFn: fakeSpawn(geneEnvelope(GOOD_GENE), c) });
    assert.equal(r2.reason, 'nothing_ready');
    assert.equal(c.n, 0, 'already-shadowed hash must not re-spawn');
  });

  it('per-slug cooldown: same slug, different snippet within cooldown -> not spawned', async () => {
    process.env.CONV_SLUG_COOLDOWN_MS = '600000';
    const m = fresh();
    seedQueue(m, C({ hash: 'h1', snippet: 'first snippet' }));
    await m.autoDistillConversation({ mode: 'shadow', spawnFn: fakeSpawn(geneEnvelope(GOOD_GENE)) });
    const c = { n: 0 };
    seedQueue(m, C({ hash: 'h2', snippet: 'different snippet same slug' }));
    const r2 = await m.autoDistillConversation({ mode: 'shadow', spawnFn: fakeSpawn(geneEnvelope(GOOD_GENE), c) });
    assert.equal(r2.reason, 'nothing_ready');
    assert.equal(c.n, 0, 'per-slug cooldown blocks 2nd snippet of same capability');
  });

  it('garbage LLM output -> no_gene_in_response, failed_attempts bumped, no upsert', async () => {
    const m = fresh(); seedQueue(m, C());
    const r = await m.autoDistillConversation({ mode: 'shadow', spawnFn: fakeSpawn(JSON.stringify({ type: 'result', is_error: false, result: 'not json here' })) });
    assert.equal(r.reason, 'no_gene_in_response');
    assert.equal(convState().by_hash.h1.failed_attempts, 1);
    assert.equal(genesOnDisk().length, 0);
  });

  it('structural-invalid gene -> validation_failed', async () => {
    const m = fresh(); seedQueue(m, C());
    const r = await m.autoDistillConversation({ mode: 'shadow', spawnFn: fakeSpawn(geneEnvelope({ type: 'Gene', id: 'x' })) });
    assert.equal(r.reason, 'validation_failed');
    assert.equal(genesOnDisk().length, 0);
  });

  it('nonzero claude exit -> claude_nonzero_exit, no upsert', async () => {
    const m = fresh(); seedQueue(m, C());
    const r = await m.autoDistillConversation({ mode: 'shadow', spawnFn: fakeSpawn(geneEnvelope(GOOD_GENE), null, 3) });
    assert.equal(r.reason, 'claude_nonzero_exit');
    assert.equal(genesOnDisk().length, 0);
  });

  it('L1 isolation: P2 never touches p3_llm or the shared scalars', async () => {
    const m = fresh(); seedQueue(m, C());
    await m.autoDistillConversation({ mode: 'shadow', spawnFn: fakeSpawn(geneEnvelope(GOOD_GENE)) });
    const st = fullState();
    assert.ok(!st.p3_llm, 'p3_llm untouched');
    assert.ok(!st.last_data_hash, 'shared last_data_hash untouched');
    assert.ok(!st.last_distillation_at, 'shared last_distillation_at untouched');
  });

  it('near-duplicate (overlapping, NOT identical signals) of an existing gene -> near_duplicate', async () => {
    // existing gene shares 3 of GOOD_GENE's 3 signals + 1 extra => sets NOT
    // identical (passes validateSynthesizedGene's exact-set check) but Jaccard
    // overlap 3/4=0.75. Set the dup threshold to 0.7 so this trips the near-dup
    // gate (proving the Jaccard path runs after structural validation).
    process.env.EVOLVER_CONV_DISTILL_DUP_JACCARD = '0.7';
    const m = fresh();
    fs.writeFileSync(path.join(tmpRoot, '.evolver', 'gep', 'genes.json'), JSON.stringify({ version: 1, genes: [{ id: 'gene_existing', category: 'innovate', signals_match: ['publish_feishu', 'feishu_doc', 'lark_doc', 'extra_signal_x'] }] }));
    seedQueue(m, C());
    const r = await m.autoDistillConversation({ mode: 'shadow', spawnFn: fakeSpawn(geneEnvelope(GOOD_GENE)) });
    delete process.env.EVOLVER_CONV_DISTILL_DUP_JACCARD;
    assert.equal(r.reason, 'near_duplicate');
    assert.equal(genesOnDisk().length, 1, 'no new gene added');
  });
});

describe('autoDistillConv — enqueue/queue', () => {
  it('enqueueCandidate writes one jsonl line per candidate with the snippet', () => {
    const m = fresh();
    m.enqueueCandidate([C({ hash: 'q1' }), C({ hash: 'q2', snippet: 'second' })]);
    const q = m._readQueue();
    assert.equal(q.length, 2);
    assert.ok(q[0].snippet && q[1].snippet, 'snippet carried into queue');
    assert.equal(q[1].hash, 'q2');
  });
});
