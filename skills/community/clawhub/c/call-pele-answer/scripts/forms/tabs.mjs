// tabs — two to five alternative answers, one visible at a time. Sections start with "=== label".
export default {
  name: 'tabs',
  fences: ['tabs'],
  routes: ['tabs'],
  parse(node, ctx) {
    node.children = ctx.helpers.sections(node.body, /^===\s*(.+)$/).filter(s => s.head).map(s => ({ label: s.head[1], nodes: ctx.parseBody(s.lines, node.line + 1 + s.at) }));
  },
  render: {
    html: (n, r) => `<div class="pe-tabs"><div class="pe-tablist" role="tablist">${n.children.map((c, k) => `<button type="button" role="tab" aria-selected="${!k}">${r.inline(c.label)}</button>`).join('')}</div>${n.children.map((c, k) => `<div class="pe-tab" role="tabpanel"${k ? ' hidden' : ''}>${r.nodes(c.nodes)}</div>`).join('')}</div>`,
    markdown: (n, r) => n.children.map(c => `**${c.label}**\n\n${r.nodes(c.nodes)}`).join('\n\n'),
  },
  lint(node, report) { if (node.children.length < 2 || node.children.length > 5) report(node.line, 'route/tabs', `tabs 有 ${node.children.length} 个标签`, '2–5 个；只有一个就直接写，超过 5 个改成表格'); },
  assets: {
    css: `.pe-tablist{display:flex;gap:.25rem;border-bottom:1px solid var(--pe-border);margin:-.25rem 0 .75rem}.pe-tablist button{border:0;border-radius:0;background:none;color:var(--pe-muted);padding:0 .6rem;border-bottom:2px solid transparent;margin-bottom:-1px}.pe-tablist button[aria-selected=true]{color:var(--pe-ink);border-bottom-color:var(--pe-accent)}`,
    js: `document.querySelectorAll('.pe-tabs').forEach(w=>{const bs=[...w.querySelectorAll('[role=tab]')],ps=[...w.querySelectorAll('.pe-tab')];bs.forEach((b,k)=>b.addEventListener('click',()=>{bs.forEach((x,j)=>x.setAttribute('aria-selected',j===k));ps.forEach((p,j)=>p.hidden=j!==k)}))});`,
  },
};
