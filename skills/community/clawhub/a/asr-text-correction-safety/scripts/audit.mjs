#!/usr/bin/env node
/**
 * Audits for a text-correction layer.
 *
 * Three checks that found real defects in a shipping dictation-correction layer. Point the
 * script at any module exporting `correct(text) -> { text }` (or a factory
 * `createCorrector() -> { correct }`) and it reports what the layer damages.
 *
 * Usage:
 *   node audit.mjs dict        [module]   # dictionary words corrupted  (needs /usr/share/dict/words)
 *   node audit.mjs idempotence [module]   # correct(correct(x)) !== correct(x)
 *   node audit.mjs collisions  [module]   # how many strings a rewrite can touch
 *   node audit.mjs all         [module]
 *
 * `module` defaults to ../lib/correct/index.js relative to this file. Exit code is 1 when
 * any check reports a defect, so it can gate CI.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));

/**
 * Module under test. Pass it explicitly (`node audit.mjs all /path/to/module.js`) — a
 * published skill cannot know where the user's layer lives. The default only exists so the
 * check runs inside this project's own layout.
 */
const argPath = process.argv[3];
const candidates = [
  argPath,
  path.join(HERE, '..', '..', '..', 'lib', 'correct', 'index.js'), // <repo>/skills/<skill>/scripts/
  path.join(HERE, '..', 'lib', 'correct', 'index.js'),              // co-located
].filter(Boolean);
const target = candidates.find(p => fs.existsSync(p)) || candidates[0];

/** Load the layer under test, accepting either a factory or a ready-made corrector. */
async function loadCorrector() {
  const mod = await import(pathToFileURL(target).href);
  if (typeof mod.createCorrector === 'function') {
    const c = mod.createCorrector();
    if (typeof c?.correct === 'function') return c;
  }
  if (typeof mod.correct === 'function') return mod;
  throw new Error(
    `${target} exports neither createCorrector() nor correct(). `
    + `Expected one of: { createCorrector }, { correct }.`,
  );
}

/** Case- and separator-insensitive content fingerprint. */
const fingerprint = (s) => String(s).toLowerCase().replace(/[^a-z0-9\u3400-\u4dbf\u4e00-\u9fff]/g, '');

/** Correct one string, tolerating both { text } and bare-string returns. */
function run(corrector, input) {
  const r = corrector.correct(input);
  return typeof r === 'string' ? r : r?.text ?? '';
}

const results = [];

function record(name, count, total, detail) {
  results.push({ name, count, total });
  const status = count === 0 ? 'CLEAN' : 'DEFECT';
  const pct = total ? ((count / total) * 100).toFixed(3) : '0';
  console.log(`\n[${status}] ${name}`);
  console.log(`  ${count} / ${total} (${pct}%)`);
  if (detail?.length) {
    console.log('  examples:');
    for (const d of detail.slice(0, 10)) console.log(`    ${d}`);
    if (detail.length > 10) console.log(`    … and ${detail.length - 10} more`);
  }
}

/** Dictionary scan: every real word the layer rewrites with changed content. */
async function dict(corrector) {
  const dictPath = '/usr/share/dict/words';
  if (!fs.existsSync(dictPath)) {
    console.log('\n[SKIP] dictionary scan — /usr/share/dict/words not present');
    return;
  }
  const words = fs.readFileSync(dictPath, 'utf8')
    .split('\n').map(w => w.trim()).filter(w => /^[a-z]{2,20}$/.test(w));
  const hits = [];
  for (const w of words) {
    const out = run(corrector, w);
    if (fingerprint(out) !== fingerprint(w)) hits.push(`${w} -> ${JSON.stringify(out)}`);
  }
  record('dictionary words whose content is changed', hits.length, words.length, hits);
}

/** Idempotence: applying the layer twice must equal applying it once. */
async function idempotence(corrector) {
  // Atoms drawn from a mixed CJK/Latin/emoji vocabulary, concatenated without separators —
  // the shape that exposed unbounded growth in the reference implementation.
  const atoms = [
    'cocos creator', 'CocosCreator', '工作台', '哈里斯', 'flcash', 'github', '插件',
    '那个', '嗯', '就是', '然后', 'deep seek', '差件', '任务', '🙂', 'a', '  ', '。', 'v1.2',
  ];
  const trials = 4000;
  const hits = [];
  // Deterministic PRNG so a reported failure can be reproduced.
  let seed = 0x2f6e2b1;
  const rnd = () => (seed = (seed * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff;

  for (let i = 0; i < trials; i++) {
    const n = 1 + Math.floor(rnd() * 3);
    let s = '';
    for (let j = 0; j < n; j++) s += atoms[Math.floor(rnd() * atoms.length)] + (rnd() < 0.3 ? ' ' : '');
    const once = run(corrector, s);
    const twice = run(corrector, once);
    const thrice = run(corrector, twice);
    if (twice !== once || thrice !== once) {
      hits.push(`${JSON.stringify(s)} -> ${JSON.stringify(once)} -> ${JSON.stringify(twice)} -> ${JSON.stringify(thrice)}`);
    }
  }
  record('non-idempotent inputs (one pass → two passes → three)', hits.length, trials, hits);
}

/**
 * Collision space: for each rewrite the layer performs, how many *other* strings does the
 * same rule also rewrite? A large number means the rule is matching on insufficient
 * evidence — the signature of phonetic rewriting.
 */
async function collisions(corrector) {
  const probes = [
    '人物', '任务', '一部', '异步', '信条', '心跳', '便衣', '编译', '接点', '接口',
    '配制', '配置', '变异', '文档', '代码', '输入', '输出', '服务器', '数据库', '一步',
  ];
  const hits = [];
  for (const p of probes) {
    const out = run(corrector, p);
    if (fingerprint(out) !== fingerprint(p)) hits.push(`${p} -> ${JSON.stringify(out)}`);
  }
  record(
    'common words rewritten (each hit means the rule matched on insufficient evidence)',
    hits.length, probes.length, hits,
  );
}

const which = (process.argv[2] || 'all').toLowerCase();
const corrector = await loadCorrector();
console.log(`module: ${target}`);
console.log(`check : ${which}`);

if (which === 'dict' || which === 'all') await dict(corrector);
if (which === 'idempotence' || which === 'all') await idempotence(corrector);
if (which === 'collisions' || which === 'all') await collisions(corrector);

const failed = results.filter(r => r.count > 0);
console.log(`\n${'='.repeat(60)}`);
if (failed.length) {
  console.log(`DEFECTS in ${failed.length} check(s): ${failed.map(f => f.name).join('; ')}`);
  console.log('Every line above is a case where already-correct text was changed.');
  console.log('Add each as a permanent regression test before fixing.');
  process.exit(1);
}
console.log('All checks clean against this module.');
