#!/usr/bin/env node
// Assembles an executor brief from a small JSON spec and a template, so the orchestrator writes
// rulings, not boilerplate. It fails closed: an unknown template, a missing value, an excerpt or
// convention keyword that matches nothing, or an unknown checklist area stops it with no output.
//
// Usage: node scripts/brief.mjs <spec.json> [--out <file>]     (default: print to stdout)
//
// Spec (paths are relative to "root", default the current directory):
// {
//   "template": "brief" | "fix-brief" | "integration-brief" | "<path to a template>",
//   "root": "/path/to/worktree",
//   "budgetKb": 12,                      // warn on stderr above this size (guideline, not a limit)
//   "values": { "SHA": "abc123", "RULINGS": ["R1 ...", "R2 ..."], "STRUCTURAL_RULING": "", ... },
//   "excerpts": [{ "file": "src/a.ts", "regex": "export function foo", "lines": 40 }],
//   "conventions": { "source": "docs/conventions", "keywords": ["error", "zod"] },
//   "checklist": { "source": "docs/conventions/review-checklist.md", "areas": ["Input", "Tests"] },
//   "gatePrefix": "~/.claude/skills/agentic-maestro/scripts/gate.sh"
// }
// Every {{KEY}} in the template must get a value; pass "" to leave one empty on purpose. Arrays are
// joined one item per line. Computed keys (do not put them in "values"): RULES (templates/_rules.md),
// EXCERPTS, CONVENTIONS, CHECKLIST_AREAS; GATE_COMMANDS gets each line prefixed with gatePrefix.
// The checklist source defaults to the skill's references/checklist.md; areas are its "## " headings.
// Exit: 0 written; 1 a value, excerpt, keyword or area is missing; 2 usage or unreadable input.
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { resolve, dirname, join, isAbsolute } from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { homedir } from 'node:os';

const SKILL = dirname(dirname(fileURLToPath(import.meta.url)));
const fail = (code, msg) => {
  console.error(`brief.mjs: ${msg}`);
  process.exit(code);
};

const args = process.argv.slice(2);
let specPath = null;
let outPath = null;
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--out') {
    if (i + 1 >= args.length) fail(2, '--out needs a file');
    outPath = args[++i];
  } else if (!specPath) specPath = args[i];
  else fail(2, `unexpected argument '${args[i]}'`);
}
if (!specPath) fail(2, 'usage: node scripts/brief.mjs <spec.json> [--out <file>]');

let spec;
try {
  spec = JSON.parse(readFileSync(specPath, 'utf8'));
} catch (e) {
  fail(2, `cannot read spec ${specPath}: ${e.message}`);
}
const root = resolve(spec.root ?? '.');
const expand = (p) => (p.startsWith('~/') ? join(homedir(), p.slice(2)) : p);
const at = (p) => (isAbsolute(expand(p)) ? expand(p) : join(root, p));
// Helpers run with cwd = root and get root-relative paths, so quoted file names stay short.
const rel = (p) => (isAbsolute(expand(p)) ? expand(p) : p);

const tplName = spec.template ?? 'brief';
const tplPath = /[/.]/.test(tplName) ? at(tplName) : join(SKILL, 'templates', `${tplName}.md`);
if (!existsSync(tplPath)) fail(2, `no such template: ${tplPath}`);
let out = readFileSync(tplPath, 'utf8');

const values = { ...(spec.values ?? {}) };
const COMPUTED = ['RULES', 'EXCERPTS', 'CONVENTIONS', 'CHECKLIST_AREAS'];
for (const k of COMPUTED) if (k in values) fail(2, `${k} is computed; remove it from "values"`);
const used = new Set([...out.matchAll(/\{\{([A-Z0-9_]+)\}\}/g)].map((m) => m[1]));
const run = (cmd, argv) => {
  try {
    return { ok: true, text: execFileSync(cmd, argv, { cwd: root, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }) };
  } catch (e) {
    return { ok: false, code: e.status, text: `${e.stdout ?? ''}${e.stderr ?? ''}`.trim() };
  }
};

if (used.has('RULES')) values.RULES = readFileSync(join(SKILL, 'templates', '_rules.md'), 'utf8').trimEnd();

if (used.has('EXCERPTS')) {
  const list = spec.excerpts ?? [];
  if (list.length === 0) fail(1, 'the template needs EXCERPTS: give "excerpts": [{file, regex, lines}] (or use a template without them)');
  const parts = [];
  for (const x of list) {
    if (!x.file || !x.regex) fail(2, 'each excerpt needs "file" and "regex"');
    const r = run('bash', [join(SKILL, 'scripts', 'excerpt.sh'), rel(x.file), x.regex, String(x.lines ?? 40)]);
    if (!r.ok) fail(1, `excerpt failed for ${x.file} /${x.regex}/: ${r.text}`);
    parts.push(r.text.trimEnd());
  }
  values.EXCERPTS = parts.join('\n\n');
}

if (used.has('CONVENTIONS')) {
  const c = spec.conventions;
  if (!c || !c.source || !Array.isArray(c.keywords) || c.keywords.length === 0) {
    fail(1, 'the template needs CONVENTIONS: give "conventions": {source, keywords[]}');
  }
  const r = run('bash', [join(SKILL, 'scripts', 'conv.sh'), rel(c.source), ...c.keywords]);
  if (!r.ok) fail(1, `conventions failed: ${r.text}`);
  values.CONVENTIONS = r.text.trimEnd();
}

if (used.has('CHECKLIST_AREAS')) {
  const c = spec.checklist;
  if (!c || !Array.isArray(c.areas) || c.areas.length === 0) fail(1, 'the template needs CHECKLIST_AREAS: give "checklist": {areas[], source?}');
  const src = c.source ? at(c.source) : join(SKILL, 'references', 'checklist.md');
  if (!existsSync(src)) fail(2, `no such checklist: ${src}`);
  const sections = new Map();
  let cur = null;
  for (const line of readFileSync(src, 'utf8').split('\n')) {
    const h = line.match(/^## (.+?)\s*$/);
    if (h) {
      cur = h[1].toLowerCase();
      sections.set(cur, [`${h[1]}:`]);
    } else if (/^#{1,2} /.test(line)) cur = null;
    else if (cur && line.trim()) sections.get(cur).push(line);
  }
  const picked = [];
  for (const a of c.areas) {
    const s = sections.get(String(a).toLowerCase());
    if (!s) fail(1, `checklist area '${a}' not found in ${src} (have: ${[...sections.keys()].join(', ')})`);
    picked.push(s.join('\n'));
  }
  values.CHECKLIST_AREAS = picked.join('\n');
}

if ('GATE_COMMANDS' in values && spec.gatePrefix) {
  const lines = Array.isArray(values.GATE_COMMANDS) ? values.GATE_COMMANDS : String(values.GATE_COMMANDS).split('\n');
  values.GATE_COMMANDS = lines.filter((l) => l.trim()).map((l) => `${spec.gatePrefix} ${l}`);
}

const missing = [...used].filter((k) => !(k in values));
if (missing.length) fail(1, `no value for: ${missing.join(', ')} (pass "" to leave one empty on purpose)`);
const unused = Object.keys(values).filter((k) => !used.has(k) && !COMPUTED.includes(k));
if (unused.length) console.error(`brief.mjs: warning: values not used by this template: ${unused.join(', ')}`);

const render = (v) => (Array.isArray(v) ? v.map(String).join('\n') : String(v));
// One pass with a function replacer, so a value that itself contains {{...}} or $& is inserted literally.
out = out.replace(/\{\{([A-Z0-9_]+)\}\}/g, (_, k) => render(values[k]));
out = out.replace(/\n{3,}/g, '\n\n');

const budget = (spec.budgetKb ?? 12) * 1024;
const size = Buffer.byteLength(out);
if (size > budget) console.error(`brief.mjs: warning: brief is ${(size / 1024).toFixed(1)} KB, over the ${spec.budgetKb ?? 12} KB guideline; trim excerpts or conventions`);

if (outPath) {
  mkdirSync(dirname(resolve(outPath)), { recursive: true });
  writeFileSync(outPath, out);
  console.error(`brief.mjs: wrote ${outPath} (${(size / 1024).toFixed(1)} KB)`);
} else process.stdout.write(out);
