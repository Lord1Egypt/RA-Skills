// palette-ui — the 调色器 for html output: CSS + JS built from the registered palettes.
// Pick mode outlines every component (lead, panel, figure, table, views, steps, …); click one, click a
// swatch, and only that component re-tints, live (diagrams read the same CSS tokens, so no re-render).
// Page presets swap the whole page. Choices persist in localStorage and copy out as one front-matter line
//   palette: page=warm s2=tomato s3.1=cobalt
// which the next render bakes in, so an agent regenerating the page keeps the reader's colours.
const COMP = '.pe-views,.pe-fig,.pe-table,.pe-callout,.pe-steps,.pe-slider,.pe-tabs,.pe-code';

export function parsePalette(str = '') {
  const out = {}; for (const kv of String(str).split(/[\s,;]+/)) { const m = kv.match(/^([\w.~-]+)=([\w-]+)$/); if (m) out[m[1]] = m[2]; } return out;
}

export function paletteCss(registry) {
  const pages = registry.palettes('page');
  const decl = o => Object.entries(o).map(([k, v]) => `${k}:${v}`).join(';');
  const pageCss = pages.filter(p => Object.keys(p.light || {}).length).map(p =>
    `html[data-pal=${p.name}]{${decl(p.light)}}@media (prefers-color-scheme:dark){html[data-pal=${p.name}]:not([data-theme=light]){${decl(p.dark || {})}}}html[data-pal=${p.name}][data-theme=dark]{${decl(p.dark || {})}}`).join('\n');
  const tint = `--pe-accent:var(--pk-m);--pe-blue:var(--pk-m);--pe-surface:color-mix(in srgb,var(--pk-l) 22%,var(--pe-paper));--pe-surface-2:color-mix(in srgb,var(--pk-l) 42%,var(--pe-paper));--pe-border:color-mix(in srgb,var(--pk-m) 45%,var(--pe-paper))`;
  const tintDark = `--pe-accent:var(--pk-l);--pe-blue:var(--pk-l);--pe-surface:color-mix(in srgb,var(--pk-d) 55%,var(--pe-paper));--pe-surface-2:color-mix(in srgb,var(--pk-d) 80%,var(--pe-paper));--pe-border:color-mix(in srgb,var(--pk-l) 35%,var(--pe-paper))`;
  return `${pageCss}
[data-pk]{${tint}}
@media (prefers-color-scheme:dark){html:not([data-theme=light]) [data-pk]{${tintDark}}}
html[data-theme=dark] [data-pk]{${tintDark}}
[data-pk]>h2 .pe-n{color:var(--pe-accent)}
[data-pk] th{color:var(--pe-accent);background:var(--pe-surface)}[data-pk] th:first-child{padding-left:.5rem}[data-pk] td:first-child{padding-left:.5rem}
.pe-callout[data-pk]{border-left-color:var(--pe-accent);background:var(--pe-surface)}
.pe-fig[data-pk],.pe-views[data-pk]{border-color:var(--pe-border)}
.pe-pal{margin-left:0;height:1.6rem;min-width:auto;padding:0 .5rem;font:11px var(--pe-mono);color:var(--pe-muted)}
.pe-pal[aria-pressed=true]{color:var(--pe-ink);border-color:var(--pe-ink)}
.pe-picking [data-pe-id]{cursor:crosshair}
.pe-picking [data-pe-hov]:not(svg *){outline:1.5px dashed var(--pe-muted);outline-offset:3px}
.pe-picking [data-pe-sel]:not(svg *){outline:2px solid var(--pe-ink)!important;outline-offset:3px}
.pe-picking svg [data-pe-hov]>:is(rect,circle,ellipse,polygon),.pe-picking svg path[data-pe-hov]{stroke:var(--pe-muted);stroke-width:2;stroke-dasharray:4 3}
.pe-picking svg [data-pe-sel]>:is(rect,circle,ellipse,polygon),.pe-picking svg path[data-pe-sel]{stroke:var(--pe-ink)!important;stroke-width:2.5;stroke-dasharray:5 3}
:is(p,li,blockquote,h2,td,th)[data-pk]:not(svg *){color:var(--pk-m)}
@media (prefers-color-scheme:dark){html:not([data-theme=light]) :is(p,li,blockquote,h2,td,th)[data-pk]{color:var(--pk-l)}}
html[data-theme=dark] :is(p,li,blockquote,h2,td,th)[data-pk]{color:var(--pk-l)}
tr[data-pk]>*,thead[data-pk] th{color:var(--pk-m)}
[data-pb]{--pb:color-mix(in srgb,var(--pb-l) 42%,var(--pe-paper));background:var(--pb)!important;box-shadow:0 0 0 .45rem var(--pb);border-radius:2px}
@media (prefers-color-scheme:dark){html:not([data-theme=light]) [data-pb]{--pb:color-mix(in srgb,var(--pb-d) 75%,var(--pe-paper))}}
html[data-theme=dark] [data-pb]{--pb:color-mix(in srgb,var(--pb-d) 75%,var(--pe-paper))}
:is(tr,thead,tbody)[data-pb]{box-shadow:none;background:none!important}:is(tr,thead)[data-pb]>*,thead[data-pb] th{background:var(--pb)!important}
:is(td,th)[data-pb]{box-shadow:none;border-radius:0}
svg [data-pk]>:is(rect,circle,ellipse,polygon),svg path.pele-slice[data-pk],svg [data-pk]>path:not(.pele-edge):not(.pele-marker){fill:var(--pk-m)}
svg [data-pk]>:is(rect,polygon,ellipse)[fill="var(--_s)"],svg [data-pk]>:is(rect,polygon,ellipse)[fill="var(--_a)"],svg [data-pk]>:is(rect,polygon,ellipse)[fill="var(--_bg)"]{fill:var(--pk-l);stroke:var(--pk-m)}
svg [data-pk]>text[fill="var(--_bg)"]{fill:#fff}
svg [data-pk]>rect[fill-opacity]{fill-opacity:.45}
.pe-st-mode{display:inline-flex;margin-left:auto}.pe-st-mode button{height:1.4rem;padding:0 .45rem;font-size:11px;border-radius:0}.pe-st-mode button[aria-pressed=true]{background:var(--pe-ink);color:var(--pe-paper);border-color:var(--pe-ink)}
.pe-st-mode button+button{margin-left:-1px}
.pe-st-hd{display:flex;align-items:center;gap:.35rem;margin:.7rem 0 .35rem;font:11px var(--pe-mono);color:var(--pe-muted)}
.pe-st-up{height:1.4rem;padding:0 .4rem;font-size:11px}
.pe-st-hint{font-size:11px;color:var(--pe-muted);margin-top:.35rem}
.pe-studio{position:fixed;right:1rem;bottom:1rem;width:19rem;max-height:calc(100vh - 2rem);overflow:auto;z-index:10;background:var(--pe-paper);color:var(--pe-ink);border:1px solid var(--pe-ink);border-radius:var(--pe-radius);padding:.85rem .9rem;font-size:.8125rem;box-shadow:4px 4px 0 color-mix(in srgb,var(--pe-ink) 14%,transparent)}
.pe-studio[hidden]{display:none}
.pe-studio h3{margin:0 0 .6rem;font:600 12px var(--pe-mono);letter-spacing:.04em;display:flex;justify-content:space-between;align-items:center}
.pe-studio h3 button{height:1.5rem;min-width:1.5rem;border:0;font-size:14px}
.pe-st-l{font:11px var(--pe-mono);color:var(--pe-muted);margin:.7rem 0 .35rem}
.pe-st-tgt{color:var(--pe-ink);font-family:var(--pe-font)}
.pe-st-row{display:flex;flex-wrap:wrap;gap:.35rem}
.pe-st-page{height:auto;padding:.3rem .5rem;display:flex;gap:.4rem;align-items:center;font-size:12px}
.pe-st-page i{display:flex;gap:2px}.pe-st-page i b{width:.55rem;height:.55rem;border-radius:1px;border:1px solid color-mix(in srgb,var(--pe-ink) 25%,transparent)}
.pe-sw{width:2.6rem;height:auto;min-width:0;padding:.25rem .2rem .2rem;display:flex;flex-direction:column;align-items:center;gap:.2rem;font-size:10px;color:var(--pe-muted)}
.pe-sw i{display:flex;flex-direction:column;width:1.6rem;height:1.6rem;border:1px solid var(--pe-ink);border-radius:2px;overflow:hidden}
.pe-sw i b{flex:1}
.pe-sw[aria-pressed=true],.pe-st-page[aria-pressed=true]{border-color:var(--pe-ink);color:var(--pe-ink);box-shadow:inset 0 0 0 1px var(--pe-ink)}
.pe-sw:disabled{opacity:.35;cursor:default}
.pe-st-foot{display:flex;gap:.4rem;margin-top:.85rem;padding-top:.7rem;border-top:1px solid var(--pe-border)}
.pe-st-foot button{height:1.7rem;padding:0 .55rem;font-size:12px}
@media (max-width:640px){.pe-studio{left:.5rem;right:.5rem;bottom:.5rem;width:auto;max-height:55vh}}
.nojs .pe-pal{display:none}
@media print{.pe-pal,.pe-studio{display:none!important}[data-pe-sel],[data-pe-hov]{outline:0!important}}`;
}

export function paletteJs(registry) {
  const data = { pages: registry.palettes('page').map(p => ({ n: p.name, t: p.label, c: [p.light?.['--pe-paper'] || '#FFFCF0', p.light?.['--pe-ink'] || '#100F0F', p.light?.['--pe-accent'] || '#205EA6'] })),
    sw: registry.palettes('swatch').map(s => ({ n: s.name, t: s.label, l: s.l, m: s.m, d: s.d })) };
  // Targets, coarse → fine: lead / section (sN) → component (sN.M) → part. Parts: heading (.h), paragraph or
  // list item (.pK), table header (.hd), row (.rK), cell (.rKcJ), diagram shape (.gK: a node, a timeline
  // period or event, a pie slice and its legend entry). Click picks the finest; "上一层" widens.
  // Each target takes a main colour (key id) and, unless it is a diagram shape, a background (key id~bg).
  return `(()=>{const D=${JSON.stringify(data)},d=document.documentElement,btn=document.querySelector('.pe-pal');if(!btn)return;
const SW=Object.fromEntries(D.sw.map(s=>[s.n,s])),KIND={'pe-views':'多视图','pe-fig':'图','pe-table':'表','pe-callout':'提示','pe-steps':'步骤','pe-slider':'滑杆','pe-tabs':'标签页','pe-code':'代码'};
const main=document.querySelector('main')||document.body,cut=t=>(t||'').trim().replace(/\\s+/g,' ').slice(0,12);
const tag=(e,id,name)=>{e.dataset.peId=id;e.dataset.peName=name};
const lead=document.querySelector('.pe-lead');if(lead)tag(lead,'lead','导语');
document.querySelectorAll('section.pe-panel').forEach((s,k)=>{const h=s.querySelector('h2')?.textContent.replace(/^\\d+/,'')||'';tag(s,'s'+(k+1),h);
  [...s.querySelectorAll('${COMP}')].filter(e=>e.parentElement.closest('${COMP}')===null).forEach((c,j)=>tag(c,'s'+(k+1)+'.'+(j+1),h+' · '+(KIND[[...c.classList].find(x=>KIND[x])]||'组件')+(j+1)))});
const own=e=>e.parentElement&&e.parentElement.closest('[data-pe-id]'),cnt=new Map(),next=(o,k)=>{const key=o.dataset.peId+k,n=(cnt.get(key)||0)+1;cnt.set(key,n);return n};
main.querySelectorAll('h2,p,li,blockquote,table').forEach(e=>{if(e.closest('.pe-head,.pe-foot,.pe-studio,svg,[data-pe-id="'+'"]'))return;const o=own(e);if(!o||e===o)return;const O=o.dataset.peId,N=o.dataset.peName;
  if(e.tagName==='H2'){if(o.tagName==='SECTION'&&e.parentElement===o)tag(e,O+'.h',N+' · 标题');return}
  if(e.tagName==='TABLE'){const hd=e.tHead,n=next(o,'t'),T=n>1?'t'+n:'';if(hd){tag(hd,O+'.'+T+'hd',N+' · 表头');[...hd.rows[0]?.cells||[]].forEach((c,j)=>tag(c,O+'.'+T+'r0c'+(j+1),N+' · 表头「'+cut(c.textContent)+'」'))}
    [...(e.tBodies[0]?.rows||[])].forEach((r,i)=>{tag(r,O+'.'+T+'r'+(i+1),N+' · 第'+(i+1)+'行');[...r.cells].forEach((c,j)=>tag(c,O+'.'+T+'r'+(i+1)+'c'+(j+1),N+' · 「'+cut(c.textContent)+'」'))});return}
  if(e.tagName==='P'&&e.parentElement.closest('li,blockquote'))return;const n=next(o,'p');tag(e,O+'.p'+n,N+' · '+(e.tagName==='LI'?'列表项':'段落')+n+'「'+cut(e.textContent)+'」')});
document.querySelectorAll('[data-pe-id]').forEach(f=>{const svgs=[...f.querySelectorAll(':scope svg.pele')].filter(v=>v.parentElement.closest('[data-pe-id]')===f);if(!svgs.length)return;const ids=new Map();
  svgs.forEach(v=>v.querySelectorAll('.pele-node[data-id],.pele-slice[data-id],.pele-node.pele-event').forEach(g=>{const p=g.parentElement.closest('.pele-node[data-id]'),k=(g.classList.contains('pele-event')&&!g.dataset.id?(p?.dataset.id||'')+'/ev':g.dataset.id);if(!ids.has(k))ids.set(k,ids.size+1);
    const nm=cut(g.querySelector('text')?.textContent||g.dataset.id||'');tag(g,f.dataset.peId+'.g'+ids.get(k),f.dataset.peName+' · '+(nm||'图形'+ids.get(k)));
    if(g.classList.contains('pele-slice'))v.querySelectorAll('.pele-legend-item').forEach(li=>{if(li.dataset.id===g.dataset.id)tag(li,g.dataset.peId,g.dataset.peName)})}))});
const key='pe-pal:'+location.pathname+':'+document.title;
const parse=s=>Object.fromEntries(String(s||'').split(/[\\s,;]+/).map(x=>x.split('=')).filter(x=>x.length===2&&x[1]));
let st=(()=>{try{const v=localStorage.getItem(key);if(v)return JSON.parse(v)}catch(e){}return parse(d.dataset.palette)})();
const els=id=>document.querySelectorAll('[data-pe-id="'+id+'"]'),isG=e=>!!e&&e instanceof SVGElement;
const paint=(e,n,bg)=>{const s=SW[n],a=bg?'pb':'pk';if(!s){e.removeAttribute('data-'+a);['l','m','d'].forEach(v=>e.style.removeProperty('--'+a+'-'+v));return}e.setAttribute('data-'+a,n);e.style.setProperty('--'+a+'-l',s.l);e.style.setProperty('--'+a+'-m',s.m);e.style.setProperty('--'+a+'-d',s.d)};
const apply=()=>{if(st.page&&st.page!=='ink')d.dataset.pal=st.page;else d.removeAttribute('data-pal');document.querySelectorAll('[data-pk]').forEach(e=>paint(e,null));document.querySelectorAll('[data-pb]').forEach(e=>paint(e,null,1));
  for(const[k,v]of Object.entries(st)){if(k==='page')continue;const bg=k.endsWith('~bg');els(bg?k.slice(0,-3):k).forEach(e=>{if(!(bg&&isG(e)))paint(e,v,bg)})}};
const save=()=>{try{localStorage.setItem(key,JSON.stringify(st))}catch(e){}};
const line=()=>'palette: '+Object.entries(st).map(([k,v])=>k+'='+v).join(' ');
apply();
const P=document.createElement('div');P.className='pe-studio';P.hidden=true;P.setAttribute('role','dialog');P.setAttribute('aria-label','调色器');
const b=(cls,html,attrs={})=>{const x=document.createElement('button');x.type='button';x.className=cls;x.innerHTML=html;for(const[k,v]of Object.entries(attrs))x.setAttribute(k,v);return x};
P.innerHTML='<h3>调色器<button type="button" aria-label="关闭">×</button></h3><div class="pe-st-l">页面</div><div class="pe-st-row pe-st-pages"></div><div class="pe-st-hd">选中 · <span class="pe-st-tgt">点选页面上的任一块</span></div><div class="pe-st-hd"><button type="button" class="pe-st-up" title="选中外面一层">↖ 上一层</button><span class="pe-st-mode"><button type="button" data-m="">主色</button><button type="button" data-m="bg">背景</button></span></div><div class="pe-st-row pe-st-sws"></div><div class="pe-st-hint">点得越准选得越细：段落、表格的一行或一格、图里的一个节点都能单独上色。</div><div class="pe-st-foot"></div>';
const pages=P.querySelector('.pe-st-pages'),sws=P.querySelector('.pe-st-sws'),tgt=P.querySelector('.pe-st-tgt'),foot=P.querySelector('.pe-st-foot'),up=P.querySelector('.pe-st-up'),modes=P.querySelector('.pe-st-mode');
D.pages.forEach(p=>{const x=b('pe-st-page','<i>'+p.c.map(c=>'<b style="background:'+c+'"></b>').join('')+'</i>'+p.t,{'data-n':p.n});x.onclick=()=>{st.page=p.n;apply();save();sync()};pages.append(x)});
const none=b('pe-sw','<i><b style="background:var(--pe-surface)"></b><b style="background:var(--pe-paper)"></b><b style="background:var(--pe-surface-2)"></b></i>默认',{'data-n':''});sws.append(none);
D.sw.forEach(s=>sws.append(b('pe-sw','<i><b style="background:'+s.l+'"></b><b style="background:'+s.m+'"></b><b style="background:'+s.d+'"></b></i>'+s.t,{'data-n':s.n,'aria-label':s.t})));
let sel=null,mode='';const k=()=>sel.dataset.peId+(mode&&!isG(sel)?'~bg':'');
sws.addEventListener('click',e=>{const x=e.target.closest('.pe-sw');if(!x||!sel)return;const n=x.dataset.n;if(n)st[k()]=n;else delete st[k()];apply();save();sync()});
modes.addEventListener('click',e=>{const x=e.target.closest('button');if(!x)return;mode=x.dataset.m;sync()});
const choose=t=>{document.querySelectorAll('[data-pe-sel]').forEach(e=>e.removeAttribute('data-pe-sel'));sel=t;if(t)els(t.dataset.peId).forEach(e=>e.setAttribute('data-pe-sel',''));sync()};
up.onclick=()=>{if(sel&&own(sel))choose(own(sel))};
const copy=b('','复制配色');copy.onclick=()=>{navigator.clipboard?.writeText(line());copy.textContent='已复制'; setTimeout(()=>copy.textContent='复制配色',1200)};
const reset=b('','重置全部');reset.onclick=()=>{st={};apply();save();sync()};foot.append(copy,reset);
const sync=()=>{pages.querySelectorAll('button').forEach(x=>x.setAttribute('aria-pressed',String((st.page||'ink')===x.dataset.n)));const g=isG(sel);
  modes.querySelector('[data-m=bg]').hidden=g;modes.querySelector('[data-m=""]').textContent=g?'填充':'主色';modes.querySelectorAll('button').forEach(x=>x.setAttribute('aria-pressed',String((g?'':mode)===x.dataset.m)));up.disabled=!(sel&&own(sel));
  const cur=sel&&st[k()]||'';sws.querySelectorAll('button').forEach(x=>{x.disabled=!sel;x.setAttribute('aria-pressed',String(!!sel&&x.dataset.n===cur))});tgt.textContent=sel?sel.dataset.peName:'点选页面上的任一块'};
const inPick=e=>d.classList.contains('pe-picking')&&!P.contains(e.target)&&!e.target.closest('.pe-head');
const pick=e=>{if(!inPick(e))return;const t=e.target.closest('[data-pe-id]');if(!t)return;const ctl=e.target.closest('button,a[href],input,select,textarea,label,summary,[role=tab],[role=button],.pe-an-btn');if(!(ctl&&t.contains(ctl))){e.preventDefault();e.stopPropagation()}choose(t)};
let hov=null;const hover=e=>{const t=inPick(e)?e.target.closest('[data-pe-id]'):null;if(t===hov)return;hov?.removeAttribute('data-pe-hov');hov=t;t?.setAttribute('data-pe-hov','')};
const open=o=>{P.hidden=!o;d.classList.toggle('pe-picking',o);btn.setAttribute('aria-pressed',String(o));if(!o){choose(null);hov?.removeAttribute('data-pe-hov');hov=null}sync()};
document.addEventListener('click',pick,true);document.addEventListener('mouseover',hover);
P.querySelector('h3 button').onclick=()=>open(false);btn.onclick=()=>open(P.hidden);
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!P.hidden)open(false)});
document.body.append(P);sync();})();`;
}
