// annotate-ui — 批注 for html output. Every block of the page can take a note: the lead's paragraphs,
// each section (via its title), and each block inside a section (paragraph, list item, quote, code,
// table, figure, views, steps …). A note has a kind (疑问 / 建议 / 认可 / 顾虑) and optional text.
// Notes persist in localStorage; a bar copies them all as one Markdown reply the reader pastes back to
// the agent, each note quoting its section and the start of its block so the agent knows what to fix.
// Kinds are registered like any other part (api.annotation), so a team can add its own.

export const DEFAULT_KINDS = [
  { name: 'ask', label: '疑问', color: '#5A82C6' },
  { name: 'suggest', label: '建议', color: '#B8860F' },
  { name: 'keep', label: '认可', color: '#3E8E66' },
  { name: 'concern', label: '顾虑', color: '#CF5038' },
];

export function annotateCss(kinds = DEFAULT_KINDS) {
  const k = kinds.map(x => `[data-an-k="${x.name}"]{--an:${x.color}}`).join('');
  return `${k}
main{position:relative}
.pe-an-host{position:relative}
.pe-an-btn{position:absolute;left:-2.1rem;top:.1rem;width:1.5rem;height:1.5rem;min-width:0;padding:0;border-radius:999px;font-size:12px;line-height:1;opacity:0;color:var(--pe-muted);background:var(--pe-paper);border:1px solid var(--pe-border);transition:opacity .15s}
.pe-an-host:hover>.pe-an-btn,.pe-an-host:focus-within>.pe-an-btn,.pe-an-btn:focus-visible{opacity:1}
section.pe-panel>h2.pe-an-host>.pe-an-btn{top:.2rem}
@media (hover:none){.pe-an-btn{opacity:.55}}
@media (max-width:760px){.pe-an-btn{left:auto;right:-.25rem;top:-.4rem}}
.pe-an-on{box-shadow:-.55rem 0 0 -.3rem var(--an,var(--pe-accent));background:color-mix(in srgb,var(--an,var(--pe-accent)) 7%,transparent);border-radius:2px}
.pe-an-on>.pe-an-btn{opacity:1;color:#fff;background:var(--an);border-color:var(--an)}
.pe-an-pop{position:absolute;z-index:11;width:min(20rem,calc(100vw - 1.5rem));background:var(--pe-paper);color:var(--pe-ink);border:1px solid var(--pe-ink);border-radius:12px;padding:.7rem;font-size:.8125rem;box-shadow:4px 4px 0 color-mix(in srgb,var(--pe-ink) 14%,transparent)}
.pe-an-pop[hidden]{display:none}
.pe-an-q{font:11px var(--pe-mono);color:var(--pe-muted);margin:0 0 .5rem;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.pe-an-kinds{display:flex;flex-wrap:wrap;gap:.35rem;margin-bottom:.5rem}
.pe-an-kinds button{height:1.7rem;min-width:0;padding:0 .7rem;border-radius:999px;font-size:12px;border:1px solid color-mix(in srgb,var(--an) 55%,transparent);background:color-mix(in srgb,var(--an) 14%,var(--pe-paper));color:var(--pe-ink)}
.pe-an-kinds button[aria-pressed=true]{background:var(--an);border-color:var(--an);color:#fff}
.pe-an-pop textarea{width:100%;box-sizing:border-box;min-height:4.2rem;resize:vertical;font:inherit;color:inherit;background:var(--pe-surface,transparent);border:1px solid var(--pe-border);border-radius:8px;padding:.4rem .5rem}
.pe-an-act{display:flex;gap:.4rem;justify-content:flex-end;margin-top:.5rem}
.pe-an-act button{height:1.7rem;padding:0 .7rem;font-size:12px;border-radius:999px}
.pe-an-act .pe-an-save{background:var(--pe-ink);color:var(--pe-paper);border-color:var(--pe-ink)}
.pe-an-note{display:block;margin:.3rem 0 0;font-size:.8125rem;color:var(--pe-muted)}
.pe-an-note b{color:var(--an);font-weight:600;margin-right:.35rem}
.pe-an-bar{position:fixed;left:50%;bottom:1rem;transform:translateX(-50%);z-index:9;display:flex;gap:.5rem;align-items:center;background:var(--pe-paper);border:1px solid var(--pe-ink);border-radius:999px;padding:.3rem .35rem .3rem .9rem;font-size:12px;box-shadow:3px 3px 0 color-mix(in srgb,var(--pe-ink) 14%,transparent)}
.pe-an-bar[hidden]{display:none}
.pe-an-bar i{font-style:normal;display:flex;gap:.25rem}.pe-an-bar i span{padding:0 .45rem;border-radius:999px;background:color-mix(in srgb,var(--an) 18%,var(--pe-paper))}
.pe-an-bar button{height:1.7rem;padding:0 .75rem;font-size:12px;border-radius:999px}
.pe-an-bar .pe-an-copy{background:var(--pe-ink);color:var(--pe-paper);border-color:var(--pe-ink)}
.pe-picking .pe-an-btn,.pe-picking .pe-an-bar{pointer-events:none;opacity:.25}
.nojs .pe-an-btn,.nojs .pe-an-bar{display:none}
@media print{.pe-an-btn,.pe-an-pop,.pe-an-bar{display:none!important}.pe-an-on{box-shadow:none;background:none}}`;
}

export function annotateJs(kinds = DEFAULT_KINDS) {
  const K = kinds.map(({ name, label }) => ({ n: name, t: label }));
  return `(()=>{const K=${JSON.stringify(K)},KT=Object.fromEntries(K.map(k=>[k.n,k.t])),d=document;
const hosts=[];const add=(e,id,where)=>{if(!e||e.dataset.anId)return;e.dataset.anId=id;e.dataset.anWhere=where;hosts.push(e)};
const units=(root,pre,where)=>{let n=0;[...root.children].forEach(c=>{if(/^H[1-6]$/.test(c.tagName))return;
  if(c.tagName==='UL'||c.tagName==='OL'){[...c.children].forEach(li=>add(li,pre+'.'+(++n),where))}else add(c,pre+'.'+(++n),where)})};
const lead=d.querySelector('.pe-lead');if(lead)units(lead,'lead','导语');
d.querySelectorAll('section.pe-panel').forEach((s,k)=>{const h=s.querySelector(':scope>h2');const t=(h?.textContent||'').replace(/^\\d+/,'').trim();const w='§'+String(k+1).padStart(2,'0')+' '+t;
  if(h)add(h,'s'+(k+1),w);units(s,'s'+(k+1),w)});
const key='pe-an:'+location.pathname+':'+d.title;let st={};try{st=JSON.parse(localStorage.getItem(key)||'{}')}catch(e){}
const save=()=>{try{localStorage.setItem(key,JSON.stringify(st))}catch(e){}};
const quote=e=>{if(e.tagName==='H2')return '（整节）';const c=e.cloneNode(true);c.querySelectorAll('.pe-an-btn,.pe-an-note,svg,.pe-seg,button').forEach(x=>x.remove());let q=c.textContent.replace(/\\s+/g,' ').trim();
  if(!q){const f=e.querySelector('figcaption,.pe-fig,table,pre');q=f?(f.tagName==='TABLE'?'（表）':f.tagName==='PRE'?'（代码）':'（图）'):'（组件）'}return q.length>40?q.slice(0,40)+'…':q};
const byId=id=>d.querySelector('[data-an-id="'+id+'"]');
const paint=e=>{const a=st[e.dataset.anId];e.classList.toggle('pe-an-on',!!a);if(a)e.dataset.anK=a.k;else delete e.dataset.anK;
  let n=e.querySelector(':scope>.pe-an-note');if(a&&a.t&&e.tagName!=='H2'){if(!n){n=d.createElement('span');n.className='pe-an-note';e.append(n)}n.innerHTML='';const b=d.createElement('b');b.textContent=KT[a.k]||a.k;n.append(b,d.createTextNode(a.t))}else n?.remove();
  const btn=e.querySelector(':scope>.pe-an-btn');if(btn){btn.textContent=a?'✓':'✎';btn.title=a?(KT[a.k]+(a.t?'：'+a.t:'')):'批注';btn.setAttribute('aria-label',btn.title)}};
hosts.forEach(e=>{e.classList.add('pe-an-host');const b=d.createElement('button');b.type='button';b.className='pe-an-btn';e.prepend(b);paint(e)});
const pop=d.createElement('div');pop.className='pe-an-pop';pop.hidden=true;pop.setAttribute('role','dialog');pop.setAttribute('aria-label','批注');
pop.innerHTML='<p class="pe-an-q"></p><div class="pe-an-kinds"></div><textarea placeholder="写点什么（可留空）"></textarea><div class="pe-an-act"><button type="button" class="pe-an-del">删除</button><button type="button" class="pe-an-x">取消</button><button type="button" class="pe-an-save">保存</button></div>';
const kinds=pop.querySelector('.pe-an-kinds'),ta=pop.querySelector('textarea'),q=pop.querySelector('.pe-an-q');let cur=null,kind=K[0].n;
K.forEach(k=>{const b=d.createElement('button');b.type='button';b.textContent=k.t;b.dataset.anK=k.n;b.onclick=()=>{kind=k.n;syncK()};kinds.append(b)});
const syncK=()=>kinds.querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.anK===kind)));
const close=()=>{pop.hidden=true;cur=null};
const open=e=>{cur=e;const a=st[e.dataset.anId];kind=a?.k||K[0].n;ta.value=a?.t||'';q.textContent=e.dataset.anWhere+' › '+quote(e);pop.querySelector('.pe-an-del').hidden=!a;syncK();
  const r=e.getBoundingClientRect(),m=d.querySelector('main').getBoundingClientRect();pop.hidden=false;pop.style.top=(r.top-m.top+Math.min(r.height,28)+6)+'px';pop.style.left=Math.max(0,Math.min(r.left-m.left,m.width-pop.offsetWidth))+'px';ta.focus()};
pop.querySelector('.pe-an-save').onclick=()=>{st[cur.dataset.anId]={k:kind,t:ta.value.trim(),w:cur.dataset.anWhere,q:quote(cur),at:Date.now()};save();paint(cur);bar();close()};
pop.querySelector('.pe-an-del').onclick=()=>{delete st[cur.dataset.anId];save();paint(cur);bar();close()};
pop.querySelector('.pe-an-x').onclick=close;
d.addEventListener('click',e=>{const b=e.target.closest('.pe-an-btn');if(b){e.preventDefault();e.stopPropagation();const h=b.parentElement;cur===h&&!pop.hidden?close():open(h)}});
d.addEventListener('keydown',e=>{if(e.key==='Escape'&&!pop.hidden)close();if((e.metaKey||e.ctrlKey)&&e.key==='Enter'&&!pop.hidden)pop.querySelector('.pe-an-save').click()});
const B=d.createElement('div');B.className='pe-an-bar';B.hidden=true;
B.innerHTML='<span>批注</span><i></i><button type="button" class="pe-an-copy">复制给 Agent</button><button type="button" class="pe-an-clr">清空</button>';
const order=Object.fromEntries(hosts.map((h,i)=>[h.dataset.anId,i]));
const reply=()=>{const ids=Object.keys(st).sort((a,b)=>(order[a]??1e9)-(order[b]??1e9));
  return '## 对《'+d.title+'》的批注\\n\\n'+ids.map((id,i)=>{const a=st[id];return (i+1)+'. ['+(KT[a.k]||a.k)+'] '+a.w+' › “'+a.q+'”（'+id+'）'+(a.t?'\\n   > '+a.t.replace(/\\n/g,'\\n   > '):'')}).join('\\n')+'\\n'};
const bar=()=>{const v=Object.values(st);B.hidden=!v.length;const c={};v.forEach(a=>c[a.k]=(c[a.k]||0)+1);
  B.querySelector('i').innerHTML=K.filter(k=>c[k.n]).map(k=>'<span data-an-k="'+k.n+'">'+k.t+' '+c[k.n]+'</span>').join('')};
B.querySelector('.pe-an-copy').onclick=e=>{navigator.clipboard?.writeText(reply());e.target.textContent='已复制';setTimeout(()=>e.target.textContent='复制给 Agent',1200)};
B.querySelector('.pe-an-clr').onclick=()=>{if(!confirm('清空本页全部批注？'))return;st={};save();hosts.forEach(paint);bar()};
window.PE=Object.assign(window.PE||{},{annotations:()=>reply()});
d.querySelector('main').append(pop);d.body.append(B);bar();})();`;
}
