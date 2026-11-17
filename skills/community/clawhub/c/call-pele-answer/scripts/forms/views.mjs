// views — the same content in several representations (图 / 表 / 原文); the reader switches.
// Unlike tabs (different answers), views are equivalent: the first view is the composer's pick.
export default {
  name: 'views',
  fences: ['views'],
  parse(node, ctx) {
    node.children = ctx.helpers.sections(node.body, /^===\s*(.+)$/).filter(s => s.head).map(s => ({ label: s.head[1], nodes: ctx.parseBody(s.lines, node.line + 1 + s.at) }));
    const d = node.children.findIndex(c => c.label === node.attrs.default);
    node.data = { def: d < 0 ? 0 : d };
  },
  render: {
    html: (n, r) => `<div class="pe-views"><div class="pe-seg" role="tablist" aria-label="换一种看法">${n.children.map((c, k) => `<button type="button" role="tab" aria-selected="${k === n.data.def}">${r.inline(c.label)}</button>`).join('')}</div>${n.children.map((c, k) => `<div class="pe-view" role="tabpanel"${k === n.data.def ? '' : ' hidden'}>${r.nodes(c.nodes)}</div>`).join('')}</div>`,
    // chat has no switcher: show the composer's pick only
    markdown: (n, r) => r.nodes(n.children[n.data.def].nodes),
  },
  lint(node, report) { if (node.children.length < 2) report(node.line, 'route/views', 'views 只有一种看法', '只有一种就直接写，不要包 views'); },
  assets: {
    css: `.pe-views{position:relative;margin:.5rem 0}.pe-seg{display:inline-flex;border:1px solid var(--pe-border);border-radius:var(--pe-radius);overflow:hidden;margin-bottom:.25rem;float:right;position:relative;z-index:1}
.pe-seg button{border:0;border-radius:0;height:1.6rem;min-width:auto;padding:0 .55rem;font:11px var(--pe-mono);color:var(--pe-muted);background:var(--pe-paper)}
.pe-seg button+button{border-left:1px solid var(--pe-border)}.pe-seg button[aria-selected=true]{color:var(--pe-ink);background:var(--pe-surface)}
.pe-view{clear:both}`,
    js: `document.querySelectorAll('.pe-views').forEach(w=>{const bs=[...w.querySelectorAll('.pe-seg button')],ps=[...w.querySelectorAll(':scope>.pe-view')];bs.forEach((b,k)=>b.addEventListener('click',()=>{bs.forEach((x,j)=>x.setAttribute('aria-selected',j===k));ps.forEach((p,j)=>p.hidden=j!==k)}))});`,
  },
};
