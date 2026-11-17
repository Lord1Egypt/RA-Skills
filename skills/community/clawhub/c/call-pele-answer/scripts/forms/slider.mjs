// slider — "what happens if I change this parameter". Discrete stops ("@ value"), each with its own
// result; nothing is evaluated in the page, so no formula from the draft ever runs in the browser.
export default {
  name: 'slider',
  fences: ['slider'],
  routes: ['slider'],
  parse(node, ctx) {
    node.children = ctx.helpers.sections(node.body, /^@\s*(.+)$/).filter(s => s.head).map(s => ({ label: s.head[1], nodes: ctx.parseBody(s.lines, node.line + 1 + s.at) }));
    node.data = { label: node.attrs.label || '参数', def: Math.max(0, node.children.findIndex(c => c.label === node.attrs.default)) };
  },
  render: {
    html: (n, r) => { const d = n.data.def, v = n.children.map(c => c.label); return `<div class="pe-slider"><label class="pe-w-title">${r.inline(n.data.label)}：<output>${r.esc(v[d] ?? '')}</output></label><input type="range" min="0" max="${Math.max(0, v.length - 1)}" step="1" value="${d}" aria-label="${r.esc(n.data.label)}" data-values='${r.esc(JSON.stringify(v))}'><div class="pe-ticks">${v.map(x => `<span>${r.esc(x)}</span>`).join('')}</div>${n.children.map((c, k) => `<div class="pe-stop"${k === d ? '' : ' hidden'}>${r.nodes(c.nodes)}</div>`).join('')}</div>`; },
    markdown: (n, r) => n.children.map(c => `**${n.data.label} = ${c.label}**\n\n${r.nodes(c.nodes)}`).join('\n\n'),
  },
  lint(node, report) { if (node.children.length < 2) report(node.line, 'route/slider', 'slider 少于 2 个取值', '至少给 2 个 @ 取值'); },
  assets: {
    css: `input[type=range]{width:100%;accent-color:var(--pe-accent)}.pe-ticks{display:flex;justify-content:space-between;font:11px var(--pe-mono);color:var(--pe-muted);margin:-.1rem 0 .5rem}`,
    js: `document.querySelectorAll('.pe-slider').forEach(w=>{const r=w.querySelector('input'),o=w.querySelector('output'),s=[...w.querySelectorAll('.pe-stop')],v=JSON.parse(r.dataset.values);r.addEventListener('input',()=>{s.forEach((x,j)=>x.hidden=j!=r.value);o.textContent=v[r.value]})});`,
  },
};
