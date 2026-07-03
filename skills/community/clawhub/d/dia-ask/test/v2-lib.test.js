'use strict';
const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { buildPrompt, parseArgs, findOutput, FMT } = require('../v2-lib');

let pass = 0, fail = 0;
function t(name, fn) {
  try { fn(); pass++; console.log(`ok - ${name}`); }
  catch (e) { fail++; console.log(`FAIL - ${name}\n   ${e.message}`); }
}

// ---- buildPrompt ----------------------------------------------------------

t('buildPrompt: filename uses the requested format extension', () => {
  const { fname } = buildPrompt('hola', 'csv', 1700000000000);
  assert.strictEqual(fname, 'dia_out_1700000000000.csv');
});

t('buildPrompt: unknown format falls back to md', () => {
  const { fname, ext } = buildPrompt('hola', 'xml', 1700000000000);
  assert.strictEqual(ext, 'md');
  assert.strictEqual(fname, 'dia_out_1700000000000.md');
});

t('buildPrompt: strips Spanish accents but keeps ñ (shell locale safety)', () => {
  const { fullPrompt } = buildPrompt('cuánto está el dólar señor', 'md', 1);
  assert.ok(!/[áéíóúüÁÉÍÓÚÜ]/.test(fullPrompt), 'must have no accented vowels');
  assert.ok(/cuanto esta el dolar/.test(fullPrompt), 'accented vowels stripped');
  assert.ok(/señor/.test(fullPrompt), 'ñ is preserved (not an accent)');
});

t('buildPrompt: includes the exact filename instruction and the user prompt', () => {
  const { fullPrompt, fname } = buildPrompt('listame 3 cosas', 'txt', 42);
  assert.ok(fullPrompt.includes('listame 3 cosas'), 'contains user prompt');
  assert.ok(fullPrompt.includes(fname), 'contains the exact filename');
  assert.ok(!fullPrompt.includes('"'), 'no double-quote char (a dead key on some layouts; breaks keycode typing)');
  assert.ok(fullPrompt.includes(FMT.txt), 'mentions the human format name');
});

t('buildPrompt: leads with the "Dia," address so it routes conversational', () => {
  const { fullPrompt } = buildPrompt('algo', 'md', 1);
  assert.ok(fullPrompt.startsWith('Dia,'), 'must start with "Dia,"');
});

// ---- parseArgs ------------------------------------------------------------

t('parseArgs: defaults', () => {
  const a = parseArgs([]);
  assert.strictEqual(a.format, 'md');
  assert.strictEqual(a.timeout, 300);
  assert.strictEqual(a.debug, false);
  assert.strictEqual(a.noFallback, false);
  assert.strictEqual(a.prompt, '');
});

t('parseArgs: collects positional words into the prompt', () => {
  const a = parseArgs(['hola', 'que', 'tal']);
  assert.strictEqual(a.prompt, 'hola que tal');
});

t('parseArgs: flags parsed, prompt preserved around them', () => {
  const a = parseArgs(['cuanto', 'es', '2+2', '--format', 'json', '--timeout', '120', '--debug']);
  assert.strictEqual(a.format, 'json');
  assert.strictEqual(a.timeout, 120);
  assert.strictEqual(a.debug, true);
  assert.strictEqual(a.prompt, 'cuanto es 2+2');
});

t('parseArgs: --no-fallback disables the v1 fallback path', () => {
  const a = parseArgs(['x', '--no-fallback']);
  assert.strictEqual(a.noFallback, true);
});

// ---- findOutput -----------------------------------------------------------

function mkTmpContexts() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'diav2-'));
  const ctx = path.join(root, 'ctxA', 'work');
  fs.mkdirSync(ctx, { recursive: true });
  return { root, ctx };
}

t('findOutput: returns the exact-named file when present', () => {
  const { root, ctx } = mkTmpContexts();
  const target = path.join(ctx, 'dia_out_99.md');
  fs.writeFileSync(target, 'hello');
  const got = findOutput('dia_out_99.md', Date.now() - 5000, root);
  assert.strictEqual(got, target);
  fs.rmSync(root, { recursive: true, force: true });
});

t('findOutput: ignores files older than sinceMs', () => {
  const { root, ctx } = mkTmpContexts();
  const old = path.join(ctx, 'dia_out_old.md');
  fs.writeFileSync(old, 'stale');
  const past = Date.now() - 1000;
  // set mtime well before the cutoff
  fs.utimesSync(old, new Date(past - 60000) / 1000, new Date(past - 60000) / 1000);
  const got = findOutput('dia_out_old.md', past, root);
  assert.strictEqual(got, null);
  fs.rmSync(root, { recursive: true, force: true });
});

t('findOutput: onlyCtxs restricts the scan to the given context dirs', () => {
  const { root } = mkTmpContexts();                 // creates ctxA/work
  const ctxBwork = path.join(root, 'ctxB', 'work');
  fs.mkdirSync(ctxBwork, { recursive: true });
  const inA = path.join(root, 'ctxA', 'work', 'dia_out_77.md');
  const inB = path.join(ctxBwork, 'dia_out_77.md');
  fs.writeFileSync(inA, 'a'); fs.writeFileSync(inB, 'b');
  const since = Date.now() - 5000;
  // restricted to ctxB -> must return the one in ctxB, never ctxA's
  assert.strictEqual(findOutput('dia_out_77.md', since, root, ['ctxB']), inB);
  // a restriction that matches nothing -> no match (no silent full-scan)
  assert.strictEqual(findOutput('dia_out_77.md', since, root, ['ctxZ']), null);
  fs.rmSync(root, { recursive: true, force: true });
});

t('findOutput: falls back to newest non-artifact file when name absent', () => {
  const { root, ctx } = mkTmpContexts();
  const a = path.join(ctx, 'one.md');
  const b = path.join(ctx, 'two.md');
  const art = path.join(ctx, 'artifacts', 'noise.md');
  fs.mkdirSync(path.dirname(art), { recursive: true });
  fs.writeFileSync(a, 'a'); fs.writeFileSync(art, 'noise');
  fs.writeFileSync(b, 'b');
  const base = Date.now() - 10000;
  fs.utimesSync(a, (base) / 1000, (base) / 1000);
  fs.utimesSync(b, (base + 5000) / 1000, (base + 5000) / 1000);
  fs.utimesSync(art, (base + 9000) / 1000, (base + 9000) / 1000); // newest but artifact
  const got = findOutput('not_there.md', base - 1000, root);
  assert.strictEqual(got, b, 'newest non-artifact wins, artifacts excluded');
  fs.rmSync(root, { recursive: true, force: true });
});

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
