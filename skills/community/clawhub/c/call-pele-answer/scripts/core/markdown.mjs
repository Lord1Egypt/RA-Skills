// markdown.mjs — draft → IR. The IR is plain JSON so any output (html, chat markdown, slides, an
// a React or note-app renderer) can consume it without re-parsing Markdown.
//
// IR v1
//   doc   { ir: 1, meta: {…}, lead: Node[], panels: Panel[], source: string }
//   Panel { title, line, nodes: Node[] }
//   Node  { kind: 'p', text, line }
//       | { kind: 'heading', level, text, line }
//       | { kind: 'list', ordered, items: [{ text, line }], line }
//       | { kind: 'table', head: string[], rows: string[][], line }
//       | { kind: 'quote', text, line }
//       | { kind: 'fence', lang, info, attrs, body: string[], line, form?, data?, children?: {label?, nodes}[] }
//       | { kind: 'raw', text, line }           (inside <!-- ste-off --> … <!-- ste-on -->: rendered, not linted)

export const attrs = s => Object.fromEntries([...String(s || '').matchAll(/(\w+)=("([^"]*)"|\S+)/g)].map(m => [m[1], m[3] ?? m[2]]));

// Split a fence body into sections by a separator; nested ~~~ fences are kept intact.
export function sections(body, sepRx) {
  const out = []; let cur = null; let inFence = false;
  body.forEach((ln, k) => {
    if (/^\s*(~~~|```)/.test(ln)) inFence = !inFence;
    const m = !inFence && ln.trim().match(sepRx);
    if (m) { cur = { head: m, lines: [], at: k + 1 }; out.push(cur); }
    else if (cur) cur.lines.push(ln);
    else if (ln.trim()) { cur = { head: null, lines: [ln], at: k }; out.push(cur); }
  });
  return out;
}

const BLOCK_START = /^(```|~~~|<!--|\||>|#{3,6}\s|[-*+]\s|\d+[.)]\s)/;

export function parseBody(lines, startLine, ctx) {
  const nodes = []; let i = 0;
  const L = k => startLine + k;
  while (i < lines.length) {
    const t = lines[i].trim();
    if (!t) { i++; continue; }
    if (t === '<!-- ste-off -->') {
      const j = lines.findIndex((x, k) => k > i && x.trim() === '<!-- ste-on -->');
      const end = j < 0 ? lines.length : j;
      for (const n of parseBody(lines.slice(i + 1, end), L(i + 1), ctx)) nodes.push({ ...n, quiet: true });
      i = end + 1; continue;
    }
    if (t.startsWith('<!--')) { while (i < lines.length && !/-->\s*$/.test(lines[i])) i++; i++; continue; }
    const fence = t.match(/^(```|~~~)\s*([\w-]*)\s*(.*)$/);
    if (fence) {
      const mark = fence[1]; let j = i + 1; const body = [];
      while (j < lines.length && !lines[j].trim().startsWith(mark)) body.push(lines[j++]);
      if (j >= lines.length) ctx.err(L(i), 'fence', '代码块没有闭合', `在末尾补一行 ${mark}`);
      const node = { kind: 'fence', lang: fence[2], info: fence[3], attrs: attrs(fence[3]), body, line: L(i) };
      const form = ctx.registry.formFor(node.lang);
      if (form) { node.form = form.name; if (form.parse) (ctx.trace || { span: (n, f) => f() }).span(`form:${form.name}`, () => form.parse(node, { ...ctx, parseBody: (ls, at) => parseBody(ls, at, ctx), helpers: { sections, attrs } })); (ctx.trace || { count() {} }).count(`n:${form.name}`); }
      nodes.push(node); i = j + 1; continue;
    }
    const h = t.match(/^(#{3,6})\s+(.*)$/);
    if (h) { nodes.push({ kind: 'heading', level: h[1].length, text: h[2], line: L(i) }); i++; continue; }
    if (t.startsWith('|')) {
      const rows = []; const at = i;
      while (i < lines.length && lines[i].trim().startsWith('|')) rows.push(lines[i++].trim());
      const split = r => r.replace(/^\||\|$/g, '').split('|').map(c => c.trim());
      const head = split(rows[0]);
      const body = rows.slice(rows[1] && /^[\s|:-]+$/.test(rows[1]) ? 2 : 1).map(split);
      nodes.push({ kind: 'table', head, rows: body, line: L(at) }); continue;
    }
    if (/^([-*+]|\d+[.)])\s+/.test(t)) {
      const ordered = /^\d/.test(t); const items = []; const at = i;
      while (i < lines.length) {
        const m = lines[i].trim().match(/^([-*+]|\d+[.)])\s+(.*)$/);
        if (!m) { if (lines[i].trim() && /^\s{2,}/.test(lines[i]) && items.length) { items[items.length - 1].text += ' ' + lines[i].trim(); i++; continue; } break; }
        items.push({ text: m[2], line: L(i) }); i++;
      }
      nodes.push({ kind: 'list', ordered, items, line: L(at) }); continue;
    }
    if (t.startsWith('>')) {
      const q = []; const at = i;
      while (i < lines.length && lines[i].trim().startsWith('>')) q.push(lines[i++].trim().replace(/^>\s?/, ''));
      nodes.push({ kind: 'quote', text: q.join(' '), line: L(at) }); continue;
    }
    const p = []; const at = i;
    while (i < lines.length && lines[i].trim() && !BLOCK_START.test(lines[i].trim())) p.push(lines[i++].trim());
    const joiner = /[\u4e00-\u9fff]$/.test(p[0] || '') ? '' : ' ';
    nodes.push({ kind: 'p', text: p.join(joiner), line: L(at) });
  }
  return nodes;
}

export function parseDraft(text, registry, trace) {
  const source = text.replace(/\r\n/g, '\n');
  const lines = source.split('\n');
  const meta = {}; let i = 0;
  if (lines[0]?.trim() === '---') {
    i = 1;
    while (i < lines.length && lines[i].trim() !== '---') { const m = lines[i].match(/^(\w[\w-]*):\s*(.*)$/); if (m) meta[m[1]] = m[2].replace(/^["']|["']$/g, ''); i++; }
    i++;
  }
  const errors = [], warns = [], embedded = [];
  const ctx = { registry, trace, err: (l, r, m, f) => errors.push([l, r, m, f]), warn: (l, r, m, f) => warns.push([l, r, m, f]), embedded };
  const leadStart = i; const leadLines = [];
  while (i < lines.length && !/^##\s/.test(lines[i])) leadLines.push(lines[i++]);
  const lead = parseBody(leadLines, leadStart + 1, ctx);
  const panels = [];
  while (i < lines.length) {
    const title = lines[i].replace(/^##\s+/, '').trim(); const at = i + 1; i++;
    const body = []; let inF = false;
    while (i < lines.length && (inF || !/^##\s/.test(lines[i]))) { if (/^\s*(```|~~~)/.test(lines[i])) inF = !inF; body.push(lines[i++]); }
    panels.push({ title, line: at, nodes: parseBody(body, at + 1, ctx) });
  }
  return { doc: { ir: 1, meta, lead, panels, source }, errors, warns, embedded };
}

// Depth-first walk over every node, including the nested nodes of interactive forms.
export function walk(nodes, fn, path = []) {
  for (const n of nodes) {
    fn(n, path);
    if (n.children) for (const c of n.children) walk(c.nodes, fn, [...path, n]);
  }
}
