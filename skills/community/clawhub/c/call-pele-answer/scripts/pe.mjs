#!/usr/bin/env node
// pe — call-pele-answer CLI. Thin shell over core/engine.mjs; every capability comes from the registry.
//   pe render <draft.md|->  [-o out] [--output html|markdown|json] [--theme pele] [--ste flavored|strict|off] [--lean]
//   pe check  <draft.md|->                       lint only, writes nothing
//   pe route  <answer.md|-> [-o draft.md] [--render out.html] [--router auto|…] [--device desktop|mobile] [--json]
//   pe answer <answer.md|-> [-o page.html] [--router …]   one pass: route + derive + render, no second writing pass
//   --annotate on|off  批注开关（默认开；也可配置 "annotate": false，或 PE_ANNOTATE=0，或稿件 annotate: off）
//   --palette on|off   调色器开关（默认开；也可在配置写 "palette": false，或 PE_PALETTE=0，或稿件 palette: off）
//   pe stats  [--last 50] [--json]               where the time goes (runs + agent hooks) and what to change
//   pe patch  <page.html> --panel "<title>"  < section.md
//   pe info                                      forms, routers, adapters, themes, outputs, rules, plugins
//   pe config [get | set <key> <value> | reset]  user config (~/.call-pele-answer/config.json)
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, resolve, join } from 'node:path';
import { homedir, tmpdir } from 'node:os';
import { fileURLToPath } from 'node:url';
import { createEngine, USER_CONFIG } from './core/engine.mjs';
import { createTrace } from './core/trace.mjs';
import { stats } from './core/stats.mjs';

const fmt = ([l, r, m, f]) => `L${l} [${r}] ${m}${f ? `  →  ${f}` : ''}`;
const readInput = p => (p === '-' || !p ? readFileSync(0, 'utf8') : readFileSync(p, 'utf8'));

function parseArgs(rest) {
  const opts = {}, pos = [];
  for (let k = 0; k < rest.length; k++) {
    const m = rest[k].match(/^--?([\w-]+)$/);
    if (m) opts[m[1]] = rest[k + 1] !== undefined && !rest[k + 1].startsWith('-') ? rest[++k] : true;
    else pos.push(rest[k]);
  }
  return { opts, pos };
}

function outPath(opts, title, ext) {
  if (opts.o) return resolve(opts.o);
  const slug = (title || 'page').replace(/[^\w\u4e00-\u9fff-]+/g, '-').slice(0, 40);
  const stamp = new Date().toISOString().replace(/[-:T]/g, '').slice(0, 14);
  for (const base of [join(homedir(), '.call-pele-answer', 'pages'), join(tmpdir(), 'call-pele-answer', 'pages')]) {
    try { mkdirSync(base, { recursive: true }); return join(base, `${stamp}-${slug}.${ext}`); } catch {}
  }
  return resolve(`${slug}.${ext}`);
}

async function build(engine, file, opts, { checkOnly = false } = {}) {
  const src = readInput(file);
  engine.trace.count('draft_chars', src.length);
  const r = engine.build(src, { output: opts.output || undefined, theme: opts.theme || undefined, ste: opts.ste || undefined, lean: !!opts.lean, palette: opts.palette === undefined ? undefined : !/^(off|0|false|no)$/i.test(String(opts.palette)), annotate: opts.annotate === undefined ? undefined : !/^(off|0|false|no)$/i.test(String(opts.annotate)) });
  if (r.errors.length) {
    console.log(`✗ 稿件有 ${r.errors.length} 处错误，没有生成输出：`);
    r.errors.forEach(e => console.log('  ' + fmt(e)));
    if (file === '-' || !file) { const p = join(tmpdir(), `call-pele-answer-draft-${Date.now()}.md`); writeFileSync(p, src); console.log(`  draft: ${p}  （行号对应这个文件；改完用 render ${p}）`); }
    return 1;
  }
  if (checkOnly) {
    r.warnings.forEach(w => console.log('! ' + fmt(w)));
    console.log(`# lang=${r.lang} panels=${r.doc.panels.length} warnings=${r.warnings.length}`);
    return r.warnings.length ? 1 : 0;
  }
  const out = outPath(opts, r.doc.meta.title, r.ext);
  engine.trace.span('write', () => { mkdirSync(dirname(out), { recursive: true }); writeFileSync(out, r.text); });
  console.log(`✓ ${out}`);
  if (r.embedded.length) console.log(`  embedded: ${r.embedded.join(', ')}  （输出含这些文件的代码，分享前告诉用户）`);
  const route = r.warnings.filter(w => w[1].startsWith('route/')), ste = r.warnings.filter(w => !w[1].startsWith('route/'));
  if (route.length) { console.log(`route ${route.length} warnings（形式选择）:`); route.forEach(w => console.log('  ' + fmt(w))); }
  if (ste.length) { console.log(`STE ${ste.length} warnings（文字）:`); ste.forEach(w => console.log('  ' + fmt(w))); }
  return 0;
}

async function route(engine, file, opts) {
  const res = await engine.route(readInput(file), { router: opts.router || undefined, policy: opts.device ? { device: opts.device } : {} });
  res.notes.forEach(n => console.error('! ' + n));
  if (opts.json) { console.log(JSON.stringify({ by: res.by, ms: res.ms, notes: res.notes, blocks: res.blocks.map(({ text, ...x }) => x) }, null, 2)); return 0; }
  const out = opts.o ? resolve(opts.o) : join(tmpdir(), `call-pele-answer-route-${Date.now()}.md`);
  writeFileSync(out, res.draft);
  console.log(`route ${res.blocks.length} 块 · ${res.by} · ${res.ms} ms`);
  res.blocks.forEach((b, i) => console.log(`  ${String(i + 1).padStart(2)} ${(b.title || b.text.slice(0, 18)).padEnd(18)} → ${b.family}${b.type && b.family !== 'prose' ? '/' + b.type : ''} (${b.confidence.toFixed(2)})${b.alternatives?.length ? '  alt: ' + b.alternatives.join(',') : ''}${b.gated ? '  · ' + b.gated : ''}${b.recomposed ? '  · ' + b.recomposed : ''}`));
  console.log(`  draft: ${out}`);
  if (opts.render) return build(engine, out, { ...opts, o: typeof opts.render === 'string' ? opts.render : undefined });
  return 0;
}

async function answer(engine, file, opts) {
  const res = await engine.route(readInput(file), { router: opts.router || undefined, policy: opts.device ? { device: opts.device } : {}, auto: true });
  res.notes.forEach(n => console.error('! ' + n));
  console.log(`route ${res.blocks.length} 块 · ${res.by} · ${res.ms} ms`);
  const tmp = join(tmpdir(), `call-pele-answer-answer-${Date.now()}.md`);
  writeFileSync(tmp, res.draft);
  return build(engine, tmp, { ...opts, quiet: true });
}

async function patch(engine, page, opts) {
  if (!page || !opts.panel) { console.error('✗ 用法：pe patch <page.html> --panel "<title>" < section.md'); return 2; }
  const m = readFileSync(page, 'utf8').match(/<script type="text\/markdown" id="pe-source">([\s\S]*?)<\/script>/);
  if (!m) { console.error('✗ 页面里没有原稿（#pe-source），不能 patch'); return 1; }
  const parts = m[1].replace(/<\\\/script>/g, '</script>').split(/(?=^##\s)/m);
  const k = parts.findIndex(p => p.match(/^##\s+(.*)$/m)?.[1].trim() === String(opts.panel).trim());
  if (k < 0) { console.error(`✗ 找不到块「${opts.panel}」`); return 1; }
  parts[k] = readFileSync(0, 'utf8').trim() + '\n' + (k < parts.length - 1 ? '\n' : '');
  const tmp = join(tmpdir(), `call-pele-answer-patch-${Date.now()}.md`);
  writeFileSync(tmp, parts.join(''));
  return build(engine, tmp, { ...opts, o: page });
}

const CONFIG_KEYS = { router: null, theme: null, output: ['html', 'markdown', 'json'], ste: ['flavored', 'strict', 'off'] };
function config(engine, action, pos) {
  let cfg = {}; try { cfg = JSON.parse(readFileSync(USER_CONFIG, 'utf8')); } catch {}
  if (!action || action === 'get') { console.log(JSON.stringify({ effective: engine.info().config, user: cfg }, null, 2)); return 0; }
  if (action === 'reset') { mkdirSync(dirname(USER_CONFIG), { recursive: true }); writeFileSync(USER_CONFIG, '{}\n'); console.log('✓ 已恢复默认'); return 0; }
  if (action === 'set') {
    const [k, v] = pos;
    const allowed = k === 'router' ? ['auto', ...engine.registry.routers()] : k === 'theme' ? engine.registry.themes() : CONFIG_KEYS[k];
    if (!(k in CONFIG_KEYS) || !allowed.includes(v)) { console.error(`✗ 用法：pe config set ${k in CONFIG_KEYS ? k : '<router|theme|output|ste>'} <${(allowed || []).join('|')}>`); return 2; }
    cfg[k] = v; mkdirSync(dirname(USER_CONFIG), { recursive: true }); writeFileSync(USER_CONFIG, JSON.stringify(cfg, null, 2) + '\n'); console.log(`✓ ${k} = ${v}`); return 0;
  }
  console.error('✗ 用法：pe config [get | set <key> <value> | reset]'); return 2;
}

async function main(argv) {
  const [cmd, ...rest] = argv;
  const { opts, pos } = parseArgs(rest);
  if (!cmd || cmd === 'help' || cmd === '-h') { console.log(readFileSync(fileURLToPath(import.meta.url), 'utf8').split('\n').slice(1, 11).join('\n')); return 0; }
  if (cmd === 'stats') return stats(opts);
  const trace = createTrace(cmd);
  const engine = await createEngine({ trace });
  try { return await run(cmd, engine, opts, pos); }
  finally { const r = trace.flush(); if (opts.trace && r) console.error(`trace ${JSON.stringify(r.phases)} total ${r.total_ms} ms`); }
}

async function run(cmd, engine, opts, pos) {
  switch (cmd) {
    case 'answer': return answer(engine, pos[0], opts);
    case 'render': return build(engine, pos[0], opts);
    case 'check': return build(engine, pos[0], opts, { checkOnly: true });
    case 'route': return route(engine, pos[0], opts);
    case 'patch': return patch(engine, pos[0], opts);
    case 'info': console.log(JSON.stringify(engine.info(), null, 2)); return 0;
    case 'config': return config(engine, pos[0], pos.slice(1));
    default: console.error(`✗ 未知命令：${cmd}`); return 2;
  }
}

main(process.argv.slice(2)).then(c => (process.exitCode = c), e => { console.error('✗ ' + (e.stack || e.message)); process.exitCode = 2; });
