// callout — a conclusion, warning or error that must not be missed. ```callout warn 标题
export default {
  name: 'callout',
  fences: ['callout'],
  parse(node, ctx) {
    const [kind = 'info', ...title] = node.info.split(/\s+/);
    node.data = { kind: ['info', 'ok', 'warn', 'err'].includes(kind) ? kind : 'info', title: title.join(' ') };
    node.children = [{ nodes: ctx.parseBody(node.body, node.line + 1) }];
  },
  render: {
    html: (n, r) => `<aside class="pe-callout pe-${n.data.kind}">${n.data.title ? `<b>${r.inline(n.data.title)}</b>` : ''}${r.nodes(n.children[0].nodes)}</aside>`,
    markdown: (n, r) => { const body = r.nodes(n.children[0].nodes).split('\n').map(l => '> ' + l).join('\n'); return `> **${n.data.title || { info: '说明', ok: '结论', warn: '注意', err: '风险' }[n.data.kind]}**\n${body}`; },
  },
  assets: { css: `aside.pe-callout{margin:1rem 0;padding:.7rem 1rem;border-left:3px solid var(--c);background:color-mix(in srgb,var(--c) 7%,var(--pe-paper));border-radius:0 var(--pe-radius) var(--pe-radius) 0;--c:var(--pe-blue)}
aside.pe-callout>b{display:block;color:var(--c);font-weight:650;margin-bottom:.15rem}aside.pe-callout p{margin:.2rem 0}
aside.pe-ok{--c:var(--pe-green)}aside.pe-warn{--c:var(--pe-yellow)}aside.pe-err{--c:var(--pe-red)}` },
};
