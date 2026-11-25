// admit.mjs — which registered components may be offered for each block, with evidence.
// The script checks hard conditions; System One (JEV) answers each component's soft yes/no question in
// one call per block. Passing components become b.options. No combination is decided here: the agent
// picks from the options and assembles them with `pe assemble`.
//
// Thresholds tune themselves from use: `pe tune` reads what was offered vs what the agent actually wrote
// and writes per-component overrides to ~/.call-pele-answer/admission.json.
import { readFileSync, existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { appendPrivate, writePrivate } from './files.mjs';
import { join, dirname } from 'node:path';
import { homedir } from 'node:os';
import { CHECKS } from './components.mjs';
import { deformat, tablesIn, tableShape } from './tableshape.mjs';

export const STATE_DIR = join(homedir(), '.call-pele-answer');
export const ADMISSION = join(STATE_DIR, 'admission.json');
export const OFFERS = join(STATE_DIR, 'offers.jsonl');
export const USAGE = join(STATE_DIR, 'usage.jsonl');
const readJson = p => { try { return JSON.parse(readFileSync(p, 'utf8')); } catch { return {}; } };
const readLines = p => { try { return readFileSync(p, 'utf8').split('\n').filter(Boolean).map(l => JSON.parse(l)); } catch { return []; } };
const append = (p, o) => { try { appendPrivate(p, JSON.stringify(o) + '\n'); } catch {} };
// logs keep a short hash of each block title, enough to pair an offer with its use, never the text
const tid = s => createHash('sha256').update(s || '').digest('hex').slice(0, 12);

function hard(c, text, raw) {
  const ev = [];
  for (const r of c.requires || []) { const fn = typeof r === 'function' ? r : CHECKS[r]; if (!fn) continue; const e = fn(text, raw); if (!e) return null; ev.push(e); }
  return ev;
}

export async function admit(blocks, components, adapter, { overrides = readJson(ADMISSION), log = true } = {}) {
  // judge content, not markup: a table already in the draft is turned back into facts first, so it is
  // never its own evidence for `table`
  const flat = blocks.map(b => deformat(b.text));
  const pre = blocks.map((b, i) => components.map(c => ({ c, ev: hard(c, flat[i], b.text) })).filter(x => x.ev));
  let answers = null, note = null;
  // the facets router already judged every block: its candidates are the JEV side of admission
  const judged = blocks.every(b => Array.isArray(b.cands));
  if (judged) answers = blocks.map(b => Object.fromEntries(components.map(c => [`cmp_${c.name}`, { noul: b.cands.includes(c.name) ? 1 : 0 }])));
  else if (adapter) {
    const questions = {};
    for (const c of components) if (c.ask) questions[`cmp_${c.name}`] = { type: 'noul', instructions: c.ask };
    try { answers = await adapter.ask(flat, questions); } catch (e) { note = `组件准入没有 JEV（${e.message}），只用脚本条件`; }
  }
  blocks.forEach((b, i) => {
    const opts = [], near = [];
    for (const { c, ev } of pre[i]) {
      const p = answers?.[i]?.[`cmp_${c.name}`]?.noul;
      const min = overrides[c.name] ?? c.min ?? 0.8;
      if (answers) { if (p != null && p < min && p >= min - 0.1) near.push({ name: c.name, p: +p.toFixed(2), min, evidence: ev.join('，'), desc: c.desc }); if (p == null || p < min) continue; }
      else if (!(c.requires || []).length) continue; // offline: only components a script can vouch for
      opts.push({ name: c.name, p: p == null ? null : +p.toFixed(2), evidence: ev.join('，'), desc: c.desc });
    }
    b.options = judged ? opts.sort((x, y) => b.cands.indexOf(x.name) - b.cands.indexOf(y.name)) : opts.sort((x, y) => (y.p ?? 0) - (x.p ?? 0));
    b.near = near.sort((x, y) => y.p - x.p); // conditions met, JEV just under the bar: the agent may still use one
    b.tables = tablesIn(b.text).map(t => ({ rows: t.rows.length, cols: t.head.length, ...tableShape(t) }));
  });
  if (log) append(OFFERS, { ts: Date.now(), blocks: blocks.map(b => ({ title: tid(b.title), options: b.options.map(o => o.name) })) });
  return note;
}

// What the agent actually wrote in each block: a component counts as used when its fence (or, for
// mermaid, the first word of its skeleton) appears in the block.
export function usedComponents(blockText, components) {
  const used = new Set();
  const heads = [...blockText.matchAll(/^\s*(?:```|~~~)mermaid[^\n]*\n\s*([^\s\n]+)([^\n]*)?(?:\n([\s\S]*?))?(?:```|~~~)/gm)];
  for (const h of heads) {
    const word = h[1]; const body = h[3] || '';
    for (const c of components) {
      if (c.fence !== 'mermaid') continue;
      const w = c.skeleton.split(/\s/)[0];
      if (w === 'xychart') { if (word.startsWith('xychart') && new RegExp(`^\\s*${c.name}\\s*\\[`, 'm').test(body)) used.add(c.name); continue; }
      if (word === w || (w === 'flowchart' && word === 'graph') || (w.startsWith('stateDiagram') && word.startsWith('stateDiagram'))) used.add(c.name);
    }
  }
  for (const c of components) {
    if (c.fence === 'table' && /^\s*\|[\s:-]*-{3,}[\s:|-]*\|?\s*$/m.test(blockText)) used.add(c.name);
    else if (c.fence !== 'mermaid' && c.fence !== 'table' && new RegExp(`^\\s*(\`\`\`|~~~)${c.fence}\\b`, 'm').test(blockText)) used.add(c.name);
  }
  return [...used];
}

export function logUsage(draft, components) {
  const parts = draft.split(/^(?=##\s)/m).filter(p => /^##\s/.test(p));
  if (!parts.length) return;
  append(USAGE, { ts: Date.now(), blocks: parts.map(p => ({ title: tid(p.match(/^##\s+(.*)$/m)[1].trim()), used: usedComponents(p, components) })) });
}

// Offered but rarely used → raise its bar; used but not offered → lower it. Small steps, bounded.
export function tune(components, { minSeen = 8, step = 0.03 } = {}) {
  const offers = readLines(OFFERS), usage = readLines(USAGE), cur = readJson(ADMISSION);
  const lastOffer = new Map();
  const stat = Object.fromEntries(components.map(c => [c.name, { offered: 0, used: 0, missed: 0 }]));
  const events = [...offers.map(o => ({ ...o, k: 'o' })), ...usage.map(u => ({ ...u, k: 'u' }))].sort((a, b) => a.ts - b.ts);
  for (const e of events) for (const b of e.blocks) {
    if (e.k === 'o') { lastOffer.set(b.title, b.options); continue; }
    const off = lastOffer.get(b.title); if (!off) continue;
    for (const n of off) if (stat[n]) { stat[n].offered++; if (b.used.includes(n)) stat[n].used++; }
    for (const n of b.used) if (stat[n] && !off.includes(n)) stat[n].missed++;
    lastOffer.delete(b.title);
  }
  const changes = [];
  for (const c of components) {
    const s = stat[c.name], base = cur[c.name] ?? c.min ?? 0.8; let v = base;
    if (s.offered >= minSeen && s.used / s.offered < 0.1) v = Math.min(0.97, base + step);
    if (s.missed >= 3) v = Math.max(0.6, base - step);
    if (v !== base) { cur[c.name] = +v.toFixed(2); changes.push({ name: c.name, from: base, to: cur[c.name], ...s }); }
  }
  if (changes.length) writePrivate(ADMISSION, JSON.stringify(cur, null, 2) + '\n');
  return { stat, changes };
}

// Insert chosen components' skeletons into one block of a draft.
//   as=views  the block body becomes the last view (原文) and each component a view before it
//   as=stack  each component's fence is appended after the body
export function assemble(draft, { block, use, as = 'views' }, components) {
  const parts = draft.split(/^(?=##\s)/m);
  const idx = parts.map((p, i) => [p, i]).filter(([p]) => /^##\s/.test(p));
  const hit = /^\d+$/.test(String(block)) ? idx[Number(block) - 1] : idx.find(([p]) => p.match(/^##\s+(.*)$/m)[1].includes(String(block)));
  if (!hit) throw new Error(`找不到块「${block}」`);
  const [part, i] = hit;
  const [head, ...rest] = part.split('\n'); const body = rest.join('\n').trim();
  const byName = new Map(components.map(c => [c.name, c]));
  const missing = use.filter(n => !byName.has(n)); if (missing.length) throw new Error(`未知组件：${missing.join(', ')}（pe options 列出可选组件）`);
  const fenceOf = (c, f) => (c.fence === 'mermaid' ? `${f}mermaid\n${c.skeleton}\n${f}` : c.fence === 'table' ? c.skeleton : c.fence === 'code' ? `${f}bash\n${c.skeleton}\n${f}` : `${f}${c.fence}\n${c.skeleton}\n${f}`);
  let out;
  if (as === 'stack') out = [body, ...use.map(n => fenceOf(byName.get(n), '```'))].filter(Boolean).join('\n\n');
  else out = '```views\n' + [...use.map(n => `=== ${n}\n${fenceOf(byName.get(n), '~~~')}`), `=== 原文\n${body.replace(/```/g, '~~~')}`].join('\n') + '\n```';
  // the marker records a deliberate choice: lint lets a marked table-only block through table-heavy
  parts[i] = `${head}\n<!-- pe:use ${use.join(',')} -->\n${out}\n\n`;
  return parts.join('');
}
