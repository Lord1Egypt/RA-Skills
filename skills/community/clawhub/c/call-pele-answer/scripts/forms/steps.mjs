// steps — a mechanism revealed one beat at a time (explainer "video" level 0). Beats split on ---.
export default {
  name: 'steps',
  fences: ['steps'],
  routes: ['steps'],
  parse(node, ctx) {
    const { sections } = ctx.helpers;
    node.children = sections(node.body, /^---+$/).map(b => ({ nodes: ctx.parseBody(b.lines, node.line + 1 + b.at) }));
    node.data = { title: node.attrs.title || '', ms: Number(node.attrs.ms) || 3200, autoplay: node.attrs.autoplay !== 'off' };
  },
  render: {
    html: (n, r) => { const k = n.children.length; return `<div class="pe-steps" data-autoplay="${n.data.autoplay ? 1 : 0}" data-ms="${n.data.ms}">${n.data.title ? `<div class="pe-w-title">${r.inline(n.data.title)}</div>` : ''}<div class="pe-stage">${n.children.map((c, i) => `<section class="pe-beat"${i ? ' hidden' : ''} aria-label="${i + 1}/${k}">${r.nodes(c.nodes)}</section>`).join('')}</div><div class="pe-bar"><button type="button" data-act="prev" aria-label="上一步">‹</button><button type="button" data-act="play" aria-label="播放/暂停">▶</button><button type="button" data-act="next" aria-label="下一步">›</button><span class="pe-count">1 / ${k}</span><span class="pe-track"><i style="width:${100 / k}%"></i></span></div></div>`; },
    markdown: (n, r) => (n.data.title ? `**${n.data.title}**\n\n` : '') + n.children.map((c, i) => `**第 ${i + 1} 步**\n\n${r.nodes(c.nodes)}`).join('\n\n'),
  },
  lint(node, report) { if (node.children.length < 2) report(node.line, 'route/steps', 'steps 少于 2 拍', '只有一拍就用普通图'); },
  assets: {
    css: `.pe-bar{display:flex;align-items:center;gap:.4rem;margin-top:.75rem;font:12px var(--pe-mono);color:var(--pe-muted)}.pe-track{flex:1;height:2px;background:var(--pe-border);margin-left:.5rem}.pe-track i{display:block;height:2px;background:var(--pe-accent);transition:width .2s}`,
    js: `document.querySelectorAll('.pe-steps').forEach(w=>{const b=[...w.querySelectorAll('.pe-beat')],c=w.querySelector('.pe-count'),bar=w.querySelector('.pe-track i'),pl=w.querySelector('[data-act=play]');let i=0,t=null;
 const go=k=>{i=(k+b.length)%b.length;b.forEach((x,j)=>x.hidden=j!==i);c.textContent=(i+1)+' / '+b.length;bar.style.width=((i+1)/b.length*100)+'%'};
 const stop=()=>{clearInterval(t);t=null;pl.textContent='▶'};
 const play=()=>{if(t)return stop();pl.textContent='❚❚';t=setInterval(()=>{if(i===b.length-1)return stop();go(i+1)},+w.dataset.ms)};
 w.addEventListener('click',e=>{const a=e.target.closest('button')?.dataset.act;if(a==='prev'){stop();go(i-1)}if(a==='next'){stop();go(i+1)}if(a==='play')play()});
 w.tabIndex=0;w.addEventListener('keydown',e=>{if(e.key==='ArrowRight'){stop();go(i+1)}if(e.key==='ArrowLeft'){stop();go(i-1)}if(e.key===' '){e.preventDefault();play()}});
 if(w.dataset.autoplay==='1'&&!PE.reduce&&'IntersectionObserver'in window){const io=new IntersectionObserver(es=>{if(es[0].isIntersecting){play();io.disconnect()}},{threshold:.6});io.observe(w)}});`,
  },
};
