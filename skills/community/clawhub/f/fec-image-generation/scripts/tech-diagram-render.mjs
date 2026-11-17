#!/usr/bin/env node
import J from"node:fs";import ee from"node:path";import{layoutText as H,fitNodeText as xe,routeConnector as fe,placeEdgeLabel as ue,overlaps as Me}from"./diagram-layout.mjs";const C=[],O=[];let I=[];const _=[],he=[];let le={width:0,height:0};const Le=new Set(["workflow","sequence","dataflow","lifecycle","architecture"]),ze=new Set(["frontend","backend","database","cloud","security","messagebus","external","active","waiting","decision","success","failure","neutral","start","agent","model","memory","vectorstore","graphdb","tool","document","queue","browser","user","gateway"]),Ee=new Set(["default","emphasis","security","dashed","return"]),qe=new Set(["default","terminal","blueprint","minimal","glass","warm","openai","editorial-dark"]),Be=new Set(["control","data","read","write","async","feedback"]),Y=je(process.argv.slice(2));try{const e=ce(Y,"input"),t=ce(Y,"output"),n=ce(Y,"type"),r=Y.format??"markdown";if(!Le.has(n))throw g("type",`Unsupported diagram type "${n}". Expected workflow, sequence, dataflow, lifecycle, or architecture.`);if(r!=="json"&&r!=="markdown")throw g("format",`Unsupported report format "${r}". Expected json or markdown.`);const a=Ae(e);Ue(a,n);const o=Ce(a,n),s="summary"in o?o.summary:[],u=ye(a.visual,"/visual"),d=De(a.meta.title,a.meta.subtitle??"",o.svg,n,s,u),b=((d.match(/<style>([\s\S]*?)<\/style>/)?.[1]??"").match(/[^{}]+\{[^{}]*\}/g)??[]).filter(p=>/^\s*(?:[:][r]oot|\[data-|\.node|\.edge|\.group|\.lane|\.legend|\.flow|\.label|\.sublabel|\.muted|\.actor|\.step|\.lifeline|\.tech-diagram|\.surface|\.stage|marker|#arrow)/.test(p)).join(`
`).replaceAll(":root","svg").replaceAll(/\[data-theme=/g,"svg[data-theme=").replaceAll(/\[data-visual-style=/g,"svg[data-visual-style="),E=d.replace('data-visual-style="default" data-export-root',`data-visual-style="${u}" data-export-root`).replace(/(<svg[^>]*>)/,`$1<style>${b}
svg{font-family:ui-sans-serif,system-ui,"Segoe UI",sans-serif;}svg[data-theme="dark"]{--surface:#172033;--text:#e2e8f0;--muted:#94a3b8;--line:#94a3b8;}svg[data-theme="light"]{--surface:#f8fafc;--text:#0f172a;--muted:#475569;--line:#475569;--frontend:#0369a1;--backend:#047857;--database:#0e7490;--external:#475569;--agent:#0e7490;--model:#7e22ce;--memory:#047857;--gateway:#a16207;--browser:#0369a1;--queue:#c2410c;--flow-control:#b45309;--flow-data:#0369a1;--flow-read:#047857;--flow-write:#15803d;--flow-async:#64748b;--flow-feedback:#7e22ce;}</style>`);J.mkdirSync(ee.dirname(ee.resolve(t)),{recursive:!0}),J.writeFileSync(t,E,"utf8"),Y.manifest&&(J.mkdirSync(ee.dirname(ee.resolve(Y.manifest)),{recursive:!0}),J.writeFileSync(Y.manifest,`${JSON.stringify(o.manifest,null,2)}
`,"utf8"));const m={ok:!0,type:n,input:e,output:t,manifest:Y.manifest??null,quality:{status:C.length?"partial":"estimated",issues:C},nodes:o.manifest.boxes.length,connectors:o.manifest.connectors.length};rt(m,r)}catch(e){const t=e instanceof Error?e.message:String(e);Y.format==="json"?console.log(JSON.stringify({ok:!1,error:t},null,2)):console.error(t),process.exitCode=1}function je(e){const t={};for(let n=0;n<e.length;n+=1){const r=e[n];if(!r.startsWith("--"))throw g("argv",`Unexpected positional argument "${r}".`);const a=r.slice(2),o=e[n+1];if(!o||o.startsWith("--"))throw g(a,`Missing value for --${a}.`);t[a]=o,n+=1}return t}function ce(e,t){const n=e[t];if(!n)throw g(t,`Missing required --${t}.`);return n}function Ae(e){try{return JSON.parse(J.readFileSync(e,"utf8"))}catch(t){throw g("input",`Invalid JSON at /: ${t instanceof Error?t.message:String(t)}`)}}function Ue(e,t){W(e,"/");const n=e;if(n.schema_version!==1)throw g("/schema_version","Expected schema_version to equal 1.");if(n.diagram_type!==t)throw g("/diagram_type",`Expected diagram_type to equal "${t}".`);W(n.meta,"/meta"),F(n.meta,"title","/meta/title"),ye(n.visual,"/visual")}function Ce(e,t){return t==="workflow"?pe(e,"nodes","edges"):t==="lifecycle"?pe(e,"states","transitions"):t==="sequence"?Fe(e):t==="architecture"?We(e):Ne(e)}function We(e){const t=A(e.nodes,"/nodes"),n=A(e.connections,"/connections"),r=e.groups===void 0?[]:A(e.groups,"/groups"),a=new Set,o=new Map,s=[];for(const[h,f]of r.entries()){const v=j(f,"id",`/groups/${h}/id`);G(a,v,`/groups/${h}/id`);const l=F(f,"label",`/groups/${h}/label`),i=R(f.type,`/groups/${h}/type`),x={id:v,x:X(f,"x",`/groups/${h}/x`),y:X(f,"y",`/groups/${h}/y`),width:X(f,"width",`/groups/${h}/width`),height:X(f,"height",`/groups/${h}/height`),label:l,sublabel:"",type:i,kind:"group"};s.push(x)}for(const[h,f]of t.entries()){const v=j(f,"id",`/nodes/${h}/id`);if(G(o,v,`/nodes/${h}/id`),typeof f.group=="string"&&!a.has(f.group))throw g(`/nodes/${h}/group`,`Unknown group "${f.group}".`);o.set(v,{id:v,x:X(f,"x",`/nodes/${h}/x`),y:X(f,"y",`/nodes/${h}/y`),width:typeof f.width=="number"?f.width:132,height:typeof f.height=="number"?f.height:62,label:F(f,"label",`/nodes/${h}/label`),sublabel:typeof f.sublabel=="string"?f.sublabel:"",type:R(f.type,`/nodes/${h}/type`)})}te(o,t);for(const h of t){const f=o.get(String(h.id)),v=s.find(l=>l.id===h.group);f&&v&&(f.x<v.x+12||f.y<v.y+32||f.x+f.width>v.x+v.width-12||f.y+f.height>v.y+v.height-12)&&C.push({code:"group-containment",id:f.id,message:`Node "${f.id}" exceeds group "${v.id}" content area.`})}const u=[],d=new Set,w=n.map((h,f)=>{const v=j(h,"from",`/connections/${f}/from`),l=j(h,"to",`/connections/${f}/to`),i=o.get(v),x=o.get(l);if(!i)throw g(`/connections/${f}/from`,`Unknown endpoint "${v}".`);if(!x)throw g(`/connections/${f}/to`,`Unknown endpoint "${l}".`);const U=se(h.variant,`/connections/${f}/variant`),k=we(h.flow,`/connections/${f}/flow`);k&&d.add(k);const L=_e(i,x,h.waypoints,`/connections/${f}/waypoints`);return u.push({id:`${v}-${l}-${f}`,from:v,to:l,points:L}),ne(L,U,typeof h.label=="string"?h.label:"",k)}).join(`
`),y=[...s,...o.values()],b=Math.max(360,ge(y,"y")+64),E=Ve(e.legend,[...o.values()]),m=et(e.flowLegend,[...d]),p=Math.max(860,ge(y,"x")+64),M=Math.max(1,Math.floor((p-88)/200)),c=E.length?30+Math.ceil(E.length/M)*72:0,$=m.length?30+Math.ceil(m.length/M)*72:0,S=Je(E,44,b-4,M),q=Ze(m,44,b+c,M),z=b+c+$+32,T=s.map(Ye).join(`
`),P=[...o.values()].map(re).join(`
`);return{svg:ae(p,z,`${T}
${w}
${P}
${S}
${q}`),manifest:oe(p,z,y,u),summary:$e(e.summary)}}function pe(e,t,n){const r=A(e.lanes,"/lanes"),a=A(e[t],`/${t}`),o=A(e[n],`/${n}`),s=t==="nodes",u=new Set;for(const[l,i]of r.entries()){W(i,`/lanes/${l}`);const x=j(i,"id",`/lanes/${l}/id`);F(i,"label",`/lanes/${l}/label`),G(u,x,`/lanes/${l}/id`)}const d=new Map,w=Math.max(0,...a.map((l,i)=>(W(l,`/${t}/${i}`),X(l,"col",`/${t}/${i}/col`))));let y=Math.max(780,190+(w+1)*180),b=Math.max(420,140+r.length*145);const E=118,m=72,p=142,M=172,c=new Map(r.map((l,i)=>[String(l.id),i]));for(const[l,i]of a.entries()){const x=j(i,"id",`/${t}/${l}/id`);G(d,x,`/${t}/${l}/id`);const U=j(i,"lane",`/${t}/${l}/lane`);if(!u.has(U))throw g(`/${t}/${l}/lane`,`Unknown lane "${U}".`);const k=R(i.type,`/${t}/${l}/type`),L=F(i,"label",`/${t}/${l}/label`),V=typeof i.sublabel=="string"?i.sublabel:"",K=X(i,"col",`/${t}/${l}/col`),ie=typeof i.yOffset=="number"?i.yOffset:0,ke=typeof i.width=="number"?i.width:Ie(k,s),Se=typeof i.height=="number"?i.height:Re(k,s),be={id:x,x:p+K*M,y:m+Number(c.get(U))*E+38+ie,width:ke,height:Se,label:L,sublabel:V,type:k,actor:s&&typeof i.actor=="string"?i.actor:"",step:s?Ge(i.step,l+1,`/${t}/${l}/step`):"",shape:s?Pe(k):"box"};d.set(x,be)}te(d,a);let $=72;const S=[],q=[...new Set(a.map(l=>Number(l.col)))].sort((l,i)=>l-i),z=new Map;let T=160;for(const l of q)z.set(l,T),T+=Math.max(0,...a.filter(i=>i.col===l).map(i=>d.get(String(i.id))?.width??0))+64;for(const l of r){const i=a.filter(k=>k.lane===l.id),x=new Map;for(const k of i){const L=d.get(String(k.id));if(!L)continue;L.x=Number(z.get(Number(k.col)));const V=x.get(k.col)??$+48;L.y=V+(typeof k.yOffset=="number"?k.yOffset:0),x.set(k.col,L.y+L.height+32)}const U=Math.max($+112,...i.map(k=>{const L=d.get(String(k.id));return L?L.y+L.height+24:$}));S.push({y:$,height:U-$}),$=U+32}y=Math.max(y,T+40),b=Math.max(b,$+40);const P=[],Q=o.map((l,i)=>{W(l,`/${n}/${i}`);const x=j(l,"from",`/${n}/${i}/from`),U=j(l,"to",`/${n}/${i}/to`),k=d.get(x),L=d.get(U);if(!k)throw g(`/${n}/${i}/from`,`Unknown endpoint "${x}".`);if(!L)throw g(`/${n}/${i}/to`,`Unknown endpoint "${U}".`);const V=se(l.variant,`/${n}/${i}/variant`),K=l.waypoints===void 0?de(k,L):me(k,L,l.waypoints,`/${n}/${i}/waypoints`),ie=`${x}-${U}-${i}`;return P.push({id:ie,from:x,to:U,points:K}),ne(K,V,typeof l.label=="string"?l.label:"")}).join(`
`),h=r.map((l,i)=>{const x=S[i].y;return`<g class="lane"><rect x="34" y="${x}" width="${y-68}" height="${S[i].height}" rx="10"/><text x="52" y="${x+28}" class="label muted">${N(String(l.label))}</text></g>`}).join(`
`),f=[...d.values()].map(re).join(`
`);return{svg:ae(y,b,`${h}
${Q}
${f}`),manifest:oe(y,b,[...d.values()],P),summary:s?$e(e.summary):[]}}function Fe(e){const t=A(e.participants,"/participants"),n=A(e.messages,"/messages"),r=new Set;let a=Math.max(760,160+t.length*170),o=Math.max(420,170+n.length*82);const s=74,u=(a-160)/Math.max(1,t.length-1),d=new Map;for(const[c,$]of t.entries()){W($,`/participants/${c}`);const S=j($,"id",`/participants/${c}/id`);G(r,S,`/participants/${c}/id`);const q=R($.type,`/participants/${c}/type`),z=F($,"label",`/participants/${c}/label`),T=t.length===1?a/2-64:80+c*u-64;d.set(S,{id:S,x:T,y:s,width:128,height:56,label:z,sublabel:typeof $.sublabel=="string"?$.sublabel:"",type:q})}te(d,t);const w=Math.max(280,...[...d.values()].map(c=>c.width+80),...n.map(c=>H(typeof c.label=="string"?c.label:"",260,12,16).width+60));a=Math.max(a,160+t.length*w),[...d.values()].forEach((c,$)=>{c.x=80+$*w+w/2-c.width/2});let y=Math.max(...[...d.values()].map(c=>c.y+c.height))+72;o=Math.max(o,y+n.length*108+80);const b=[],E=n.map((c,$)=>{if(W(c,`/messages/${$}`),["activation","activate","deactivate","fragment","alt","loop","par","async"].some(l=>l in c))throw g(`/messages/${$}`,"Complex sequence semantics require the Mermaid route; do not simplify activation/fragments/async fields.");const S=j(c,"from",`/messages/${$}/from`),q=j(c,"to",`/messages/${$}/to`),z=d.get(S),T=d.get(q);if(!z)throw g(`/messages/${$}/from`,`Unknown endpoint "${S}".`);if(!T)throw g(`/messages/${$}/to`,`Unknown endpoint "${q}".`);const P=typeof c.label=="string"?c.label:"",Q=H(P,190,12,16),h=y;y+=Math.max(72,Q.height+56+(S===q?32:0));const f=S===q?[[B(z),h],[B(z)+64,h],[B(z)+64,h+32],[B(z),h+32]]:[[B(z),h],[B(T),h]];_.push(f);const v=se(c.variant,`/messages/${$}/variant`);return b.push({id:`${S}-${q}-${$}`,from:S,to:q,points:f,kind:"sequence",self:S===q}),ne(f,v,typeof c.label=="string"?c.label:"")}).join(`
`),m=[...d.values()].map(re).join(`
`);o=Math.max(o,y+80);const p=[...d.values()].map(c=>`<line x1="${B(c)}" y1="${c.y+c.height}" x2="${B(c)}" y2="${o-56}" class="lifeline"/>`).join(`
`);return{svg:ae(a,o,`${p}
${E}
${m}`),manifest:oe(a,o,[...d.values()],b)}}function Ne(e){const t=A(e.stages,"/stages"),n=A(e.nodes,"/nodes"),r=A(e.flows,"/flows"),a=Math.max(860,150+t.length*180),o=Math.max(460,180+He(n)*110),s=(a-84)/Math.max(1,t.length),u=new Map;for(const[m,p]of t.entries())W(p,`/stages/${m}`),F(p,"label",`/stages/${m}/label`);for(const[m,p]of n.entries()){W(p,`/nodes/${m}`);const M=j(p,"id",`/nodes/${m}/id`);G(u,M,`/nodes/${m}/id`);const c=X(p,"stage",`/nodes/${m}/stage`);if(c<0||c>=t.length)throw g(`/nodes/${m}/stage`,`Stage index ${c} is outside /stages.`);const $=typeof p.row=="number"?p.row:Te(n,m,c),S=R(p.type,`/nodes/${m}/type`);u.set(M,{id:M,x:54+c*s+Math.max(8,s/2-64),y:118+$*96,width:128,height:58,label:F(p,"label",`/nodes/${m}/label`),sublabel:typeof p.sublabel=="string"?p.sublabel:"",type:S})}te(u,n);const d=[],w=t.map((m,p)=>{const M=42+p*s;return`<g class="stage"><rect x="${M}" y="64" width="${s-10}" height="${o-118}" rx="12"/><text x="${M+18}" y="92" class="label muted">${N(String(m.label))}</text></g>`}).join(`
`),y=r.map((m,p)=>{W(m,`/flows/${p}`);const M=j(m,"from",`/flows/${p}/from`),c=j(m,"to",`/flows/${p}/to`),$=u.get(M),S=u.get(c);if(!$)throw g(`/flows/${p}/from`,`Unknown endpoint "${M}".`);if(!S)throw g(`/flows/${p}/to`,`Unknown endpoint "${c}".`);const q=se(m.variant,`/flows/${p}/variant`),z=de($,S);return d.push({id:`${M}-${c}-${p}`,from:M,to:c,points:z}),ne(z,q,typeof m.label=="string"?m.label:"")}).join(`
`),b=[...u.values()].map(re).join(`
`);return{svg:ae(a,o,`${w}
${y}
${b}`),manifest:oe(a,o,[...u.values()],d)}}function He(e){const t=new Map;for(const n of e)typeof n.stage=="number"&&t.set(n.stage,(t.get(n.stage)??0)+1);return Math.max(1,...t.values())}function Te(e,t,n){let r=0;for(let a=0;a<t;a+=1)e[a].stage===n&&(r+=1);return r}function te(e,t){for(const[n,r]of e){const a=t.find(s=>s.id===n)??{},o=xe(r,{width:typeof a.width=="number",height:typeof a.height=="number"});e.set(n,o.box),C.push(...o.issues)}I=[...e.values()]}function D(e,t,n,r,a,o,s,u){return O.push({id:e,owner:t,kind:n,text:r,lines:a.lines,x:o-a.width/2,y:s,width:a.width,height:a.height}),`<text data-label-id="${N(e)}" x="${o}" y="${s+a.fontSize}" class="${u}" font-size="${a.fontSize}" text-anchor="middle">${a.lines.map((d,w)=>`<tspan x="${o}" dy="${w?a.lineHeight:0}">${N(d)}</tspan>`).join("")}</text>`}function re(e){const t=e.shape??"box",n=tt(e.type),r=t==="diamond"?e.width*.5-12:e.type==="queue"?e.width-64:e.width-32,a=H(e.label,r),o=H(e.sublabel,r,12,16),s=a.height+(e.sublabel?o.height+6:0),u=t==="diamond"?Z(e)-s/2:e.y+(["database","vectorstore"].includes(e.type)?30:e.type==="queue"?20:n?46:e.actor?40:20),d=D(e.id+"-label",e.id,"node",e.label,a,B(e),u,"label"),w=e.sublabel?D(e.id+"-sub",e.id,"node",e.sublabel,o,B(e),u+a.height+6,"sublabel"):"",y=H(e.actor??"",e.width-32,12,16),b=e.actor?D(e.id+"-actor",e.id,"group",e.actor,y,B(e),e.y-y.height-12,"actor"):"",E=H(e.step??"",Math.max(14,e.width-16),9,12),m=e.step?`<g class="step-badge"><circle cx="${e.x+13}" cy="${e.y+13}" r="${Math.max(10,E.width/2+4)}"/>${D(e.id+"-step",e.id,"group",e.step,E,e.x+13,e.y+7,"step-label")}</g>`:"",p=Oe(e)??(t==="diamond"?`<polygon points="${B(e)},${e.y} ${e.x+e.width},${Z(e)} ${B(e)},${e.y+e.height} ${e.x},${Z(e)}"/>`:`<rect x="${e.x}" y="${e.y}" width="${e.width}" height="${e.height}" rx="${t==="terminal"?Math.round(e.height/2):10}"/>`);return`<g data-node-id="${N(e.id)}" class="node node-${e.type}">${b}
${p}
${m}
${d}
${w}</g>`}function Oe(e){const t=B(e),n=Z(e);if(e.type==="agent"){const r=Math.min(28,e.width*.18);return`<polygon points="${e.x+r},${e.y} ${e.x+e.width-r},${e.y} ${e.x+e.width},${n} ${e.x+e.width-r},${e.y+e.height} ${e.x+r},${e.y+e.height} ${e.x},${n}"/><rect x="${e.x+5}" y="${e.y+5}" width="${e.width-10}" height="${e.height-10}" rx="10" fill="none" opacity="0.45"/>`}if(e.type==="model")return`<rect x="${e.x}" y="${e.y}" width="${e.width}" height="${e.height}" rx="14"/><rect x="${e.x+5}" y="${e.y+5}" width="${e.width-10}" height="${e.height-10}" rx="10" fill="none" opacity="0.5"/><path d="M ${t-12} ${e.y+20} L ${t-4} ${e.y+20} L ${t} ${e.y+10} L ${t+4} ${e.y+20} L ${t+12} ${e.y+20} L ${t+6} ${e.y+27} L ${t+9} ${e.y+38} L ${t} ${e.y+31} L ${t-9} ${e.y+38} L ${t-6} ${e.y+27} Z" class="node-glyph"/>`;if(e.type==="memory")return`<rect x="${e.x}" y="${e.y}" width="${e.width}" height="${e.height}" rx="12" stroke-dasharray="6 4"/>`;if(e.type==="database"||e.type==="vectorstore"){const r=Math.min(14,e.height/5),a=e.type==="vectorstore"?`<ellipse cx="${t}" cy="${e.y+e.height*.45}" rx="${e.width/2}" ry="${r}" fill="none" opacity="0.45"/><ellipse cx="${t}" cy="${e.y+e.height*.66}" rx="${e.width/2}" ry="${r}" fill="none" opacity="0.32"/>`:"";return`<ellipse cx="${t}" cy="${e.y+r}" rx="${e.width/2}" ry="${r}"/><rect x="${e.x}" y="${e.y+r}" width="${e.width}" height="${e.height-r*2}" stroke="none"/><line x1="${e.x}" y1="${e.y+r}" x2="${e.x}" y2="${e.y+e.height-r}"/><line x1="${e.x+e.width}" y1="${e.y+r}" x2="${e.x+e.width}" y2="${e.y+e.height-r}"/>${a}<ellipse cx="${t}" cy="${e.y+e.height-r}" rx="${e.width/2}" ry="${r}"/>`}if(e.type==="graphdb")return`<rect x="${e.x}" y="${e.y}" width="${e.width}" height="${e.height}" rx="14"/><circle cx="${t-18}" cy="${n-2}" r="12" class="node-glyph-outline"/><circle cx="${t+8}" cy="${n-14}" r="10" class="node-glyph-outline"/><circle cx="${t+22}" cy="${n+10}" r="11" class="node-glyph-outline"/><line x1="${t-7}" y1="${n-7}" x2="${t}" y2="${n-12}" class="node-glyph-line"/><line x1="${t+16}" y1="${n-5}" x2="${t+20}" y2="${n}" class="node-glyph-line"/>`;if(e.type==="tool")return`<rect x="${e.x}" y="${e.y}" width="${e.width}" height="${e.height}" rx="10"/><circle cx="${t}" cy="${e.y+24}" r="9" class="node-glyph-outline"/><line x1="${t}" y1="${e.y+11}" x2="${t}" y2="${e.y+16}" class="node-glyph-line"/><line x1="${t}" y1="${e.y+32}" x2="${t}" y2="${e.y+37}" class="node-glyph-line"/><line x1="${t-13}" y1="${e.y+24}" x2="${t-8}" y2="${e.y+24}" class="node-glyph-line"/><line x1="${t+8}" y1="${e.y+24}" x2="${t+13}" y2="${e.y+24}" class="node-glyph-line"/>`;if(e.type==="document"){const r=Math.min(16,e.width*.16);return`<path d="M ${e.x} ${e.y} L ${e.x+e.width-r} ${e.y} L ${e.x+e.width} ${e.y+r} L ${e.x+e.width} ${e.y+e.height} L ${e.x} ${e.y+e.height} Z"/><path d="M ${e.x+e.width-r} ${e.y} L ${e.x+e.width-r} ${e.y+r} L ${e.x+e.width} ${e.y+r}" fill="none"/>`}if(e.type==="queue"){const r=e.height/2,a=Math.min(18,e.width/6);return`<ellipse cx="${e.x+a}" cy="${n}" rx="${a}" ry="${r}"/><rect x="${e.x+a}" y="${n-r}" width="${e.width-a*2}" height="${r*2}" stroke="none"/><line x1="${e.x+a}" y1="${n-r}" x2="${e.x+e.width-a}" y2="${n-r}"/><line x1="${e.x+a}" y1="${n+r}" x2="${e.x+e.width-a}" y2="${n+r}"/><ellipse cx="${e.x+e.width-a}" cy="${n}" rx="${a}" ry="${r}"/>`}if(e.type==="browser")return`<rect x="${e.x}" y="${e.y}" width="${e.width}" height="${e.height}" rx="10"/><rect x="${e.x}" y="${e.y}" width="${e.width}" height="20" rx="10" class="node-chrome"/><circle cx="${e.x+14}" cy="${e.y+10}" r="3" class="node-dot"/><circle cx="${e.x+26}" cy="${e.y+10}" r="3" class="node-dot"/><circle cx="${e.x+38}" cy="${e.y+10}" r="3" class="node-dot"/>`;if(e.type==="user")return`<rect x="${e.x}" y="${e.y}" width="${e.width}" height="${e.height}" rx="12"/><circle cx="${t}" cy="${e.y+22}" r="9" class="node-glyph-outline"/><path d="M ${t-16} ${e.y+43} Q ${t} ${e.y+28} ${t+16} ${e.y+43}" class="node-glyph-line"/>`;if(e.type==="gateway"){const r=Math.min(22,e.width*.18);return`<polygon points="${e.x+r},${e.y} ${e.x+e.width-r},${e.y} ${e.x+e.width},${n} ${e.x+e.width-r},${e.y+e.height} ${e.x+r},${e.y+e.height} ${e.x},${n}"/>`}return null}function Ye(e){return`<g class="group group-${e.type}"><rect x="${e.x}" y="${e.y}" width="${e.width}" height="${e.height}" rx="14"/>${D(e.id+"-group",e.id,"group",e.label,H(e.label,e.width-32,12,16),e.x+e.width/2,e.y+10,"sublabel")}</g>`}function ne(e,t,n,r=""){const a=e.map(([y,b],E)=>`${E===0?"M":"L"} ${y} ${b}`).join(" "),o=H(n,190,12,16),s=ue(e,o,[...I,...O]),u=`edge-label-${O.length}`;n&&C.push(...s.issues.map(y=>({...y,id:u}))),n&&he.push({id:u,label:n,points:e});const d=n?D(u,u,"edge",n,o,s.rect.x+s.rect.width/2,s.rect.y,"edge-label"):"",w=r?`flow-${r}`:t==="return"?"default":t;return`<g class="edge edge-${t}${r?` flow-${r}`:""}"><path d="${a}" marker-end="url(#arrow-${w})"/>
${d}</g>`}function ae(e,t,n){for(let r=O.length-1;r>=0;r--)O[r].kind==="edge"&&O.splice(r,1);for(const{id:r,label:a,points:o}of he){const s=H(a,190,12,16),u=ue(o,s,[...I,...O],_);C.push(...u.issues);const d=D(r,r,"edge",a,s,u.rect.x+u.rect.width/2,u.rect.y,"edge-label");n=n.replace(new RegExp('<text data-label-id="'+r+'"[^>]*>[\\s\\S]*?</text>'),d)}return e=Math.ceil(Math.max(e,...I.map(r=>r.x+r.width+40),...O.map(r=>r.x+r.width+40),..._.flat().map(r=>r[0]+40))),t=Math.ceil(Math.max(t,...I.map(r=>r.y+r.height+40),...O.map(r=>r.y+r.height+40),..._.flat().map(r=>r[1]+40))),le={width:e,height:t},`<svg class="tech-diagram" data-theme="light" data-visual-style="default" data-export-root="1" role="img" viewBox="0 0 ${e} ${t}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow-default" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z"/></marker>
    <marker id="arrow-emphasis" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z"/></marker>
    <marker id="arrow-security" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z"/></marker>
    <marker id="arrow-dashed" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z"/></marker>
    <marker id="arrow-flow-control" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z"/></marker>
    <marker id="arrow-flow-data" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z"/></marker>
    <marker id="arrow-flow-read" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z"/></marker>
    <marker id="arrow-flow-write" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z"/></marker>
    <marker id="arrow-flow-async" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z"/></marker>
    <marker id="arrow-flow-feedback" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z"/></marker>
  </defs>
  <rect x="16" y="18" width="${e-32}" height="${t-36}" rx="18" class="surface"/>
  ${n}
</svg>`}function De(e,t,n,r,a=[],o="default"){const s=Xe(a);return`<!doctype html>
<html lang="en" data-theme="auto" data-visual-style="${N(o)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${N(e)}</title>
<style>
:root {
  color-scheme: dark light;
  --bg: #0f172a;
  --panel: #111827;
  --surface: #172033;
  --text: #f8fafc;
  --muted: #94a3b8;
  --line: #64748b;
  --frontend: #38bdf8;
  --backend: #34d399;
  --database: #a78bfa;
  --cloud: #fbbf24;
  --security: #fb7185;
  --messagebus: #fb923c;
  --external: #cbd5e1;
  --agent: #22d3ee;
  --model: #c084fc;
  --memory: #34d399;
  --vectorstore: #60a5fa;
  --graphdb: #f472b6;
  --tool: #f59e0b;
  --document: #cbd5e1;
  --queue: #fb923c;
  --browser: #38bdf8;
  --user: #fda4af;
  --gateway: #fbbf24;
  --flow-control: #f59e0b;
  --flow-data: #38bdf8;
  --flow-read: #34d399;
  --flow-write: #22c55e;
  --flow-async: #94a3b8;
  --flow-feedback: #c084fc;
}
[data-theme="light"] {
  --bg: #f8fafc;
  --panel: #ffffff;
  --surface: #eef2f7;
  --text: #0f172a;
  --muted: #64748b;
  --line: #475569;
}
[data-visual-style="terminal"] {
  --bg: #0b1020;
  --panel: #0f172a;
  --surface: #111827;
  --text: #e2e8f0;
  --muted: #94a3b8;
  --frontend: #38bdf8;
  --backend: #22c55e;
  --security: #f472b6;
}
[data-visual-style="blueprint"] {
  --bg: #082f49;
  --panel: #0b3b5e;
  --surface: #0c4a6e;
  --text: #e0f2fe;
  --muted: #7dd3fc;
  --line: #67e8f9;
  --frontend: #38bdf8;
  --backend: #67e8f9;
  --database: #fde047;
  --cloud: #bae6fd;
}
[data-visual-style="minimal"] {
  --bg: #f8fafc;
  --panel: #ffffff;
  --surface: #f1f5f9;
  --text: #111827;
  --muted: #64748b;
  --line: #94a3b8;
}
[data-visual-style="glass"] {
  --bg: #111827;
  --panel: color-mix(in srgb, #1f2937, transparent 18%);
  --surface: color-mix(in srgb, #334155, transparent 18%);
  --text: #f8fafc;
  --muted: #cbd5e1;
}
[data-visual-style="warm"] {
  --bg: #f8f6f3;
  --panel: #fffcf7;
  --surface: #f1ede6;
  --text: #141413;
  --muted: #7c756c;
  --line: #8b7355;
  --frontend: #d97757;
  --backend: #7b8b5c;
  --database: #8c6f5a;
  --cloud: #b45309;
}
[data-visual-style="openai"] {
  --bg: #ffffff;
  --panel: #ffffff;
  --surface: #f8fafc;
  --text: #0f172a;
  --muted: #64748b;
  --line: #10a37f;
  --frontend: #10a37f;
  --backend: #0f766e;
  --database: #0891b2;
}
[data-visual-style="editorial-dark"] {
  --bg: #0a0a0a;
  --panel: #111111;
  --surface: #181818;
  --text: #f5f0e8;
  --muted: #b8a88f;
  --line: #d4a574;
  --frontend: #38bdf8;
  --backend: #34d399;
  --database: #a78bfa;
  --cloud: #d4a574;
  --security: #fb7185;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  min-height: 100vh;
  background: var(--bg);
  color: var(--text);
  font: 14px/1.5 ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
main { width: min(1180px, calc(100vw - 32px)); margin: 0 auto; padding: 28px 0; }
header { display: flex; align-items: end; justify-content: space-between; gap: 20px; margin-bottom: 18px; }
h1 { font-size: 24px; margin: 0; letter-spacing: 0; }
p { margin: 6px 0 0; color: var(--muted); }
.toolbar { display: flex; gap: 8px; flex-wrap: wrap; }
button {
  border: 1px solid color-mix(in srgb, var(--muted), transparent 55%);
  background: var(--panel);
  color: var(--text);
  border-radius: 8px;
  padding: 8px 11px;
  cursor: pointer;
}
.diagram-frame { background: var(--panel); border: 1px solid color-mix(in srgb, var(--muted), transparent 70%); border-radius: 12px; overflow: auto; }
.tech-diagram { display: block; min-width: 720px; width: 100%; height: auto; }
.group rect { fill: color-mix(in srgb, currentColor, transparent 94%); stroke: currentColor; stroke-width: 1.2; stroke-dasharray: 8 5; }
.group-frontend { color: var(--frontend); }
.group-backend, .group-active, .group-start { color: var(--backend); }
.group-database { color: var(--database); }
.group-cloud, .group-decision { color: var(--cloud); }
.group-security, .group-failure, .group-waiting { color: var(--security); }
.group-messagebus { color: var(--messagebus); }
.group-external, .group-neutral, .group-success { color: var(--external); }
.surface { fill: var(--surface); stroke: color-mix(in srgb, var(--muted), transparent 70%); }
.lane rect, .stage rect { fill: color-mix(in srgb, var(--surface), transparent 25%); stroke: color-mix(in srgb, var(--muted), transparent 72%); }
.node rect, .node polygon, .node path, .node ellipse, .node line, .node circle { fill: color-mix(in srgb, currentColor, transparent 86%); stroke: currentColor; stroke-width: 1.6; }
.node-frontend { color: var(--frontend); }
.node-backend, .node-active, .node-start, .node-success { color: var(--backend); }
.node-database { color: var(--database); }
.node-cloud, .node-decision { color: var(--cloud); }
.node-security, .node-failure, .node-waiting { color: var(--security); }
.node-messagebus { color: var(--messagebus); }
.node-external, .node-neutral { color: var(--external); }
.node-agent { color: var(--agent); }
.node-model { color: var(--model); }
.node-memory { color: var(--memory); }
.node-vectorstore { color: var(--vectorstore); }
.node-graphdb { color: var(--graphdb); }
.node-tool { color: var(--tool); }
.node-document { color: var(--document); }
.node-queue { color: var(--queue); }
.node-browser { color: var(--browser); }
.node-user { color: var(--user); }
.node-gateway { color: var(--gateway); }
.node-glyph { fill: currentColor; stroke: none; }
.node-glyph-outline, .node-glyph-line { fill: none; stroke: currentColor; }
.node-chrome { fill: currentColor; opacity: 0.25; stroke: none; }
.node-dot { fill: currentColor; stroke: none; opacity: 0.65; }
.label { fill: var(--text); font-weight: 650; font-size: 14px; }
.sublabel, .muted, .actor { fill: var(--muted); font-size: 12px; }
.actor { font-weight: 650; }
.step-badge circle { fill: var(--panel); stroke: currentColor; stroke-width: 1.3; }
.step-badge text { fill: var(--text); font-size: 9px; font-weight: 750; }
.edge path { fill: none; stroke: var(--line); stroke-width: 1.6; }
.edge-emphasis path { stroke: var(--frontend); stroke-width: 2; }
.edge-security path { stroke: var(--security); stroke-dasharray: 5 4; }
.edge-dashed path, .edge-return path { stroke-dasharray: 5 4; }
.flow-control path { stroke: var(--flow-control); }
.flow-data path { stroke: var(--flow-data); stroke-width: 2; }
.flow-read path { stroke: var(--flow-read); }
.flow-write path { stroke: var(--flow-write); stroke-dasharray: 5 4; }
.flow-async path { stroke: var(--flow-async); stroke-dasharray: 4 4; }
.flow-feedback path { stroke: var(--flow-feedback); stroke-width: 2; }
.edge-label { fill: var(--muted); font-size: 12px; paint-order: stroke; stroke: var(--surface); stroke-width: 5px; stroke-linejoin: round; }
.lifeline { stroke: color-mix(in srgb, var(--muted), transparent 48%); stroke-dasharray: 4 5; }
.summary-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 10px; margin-top: 12px; }
.summary-card { background: var(--panel); border: 1px solid color-mix(in srgb, var(--muted), transparent 74%); border-radius: 8px; padding: 12px; }
.summary-card h2 { margin: 0 0 7px; font-size: 13px; letter-spacing: 0; }
.summary-card ul { margin: 0; padding-left: 18px; color: var(--muted); font-size: 12px; }
.summary-card li + li { margin-top: 4px; }
marker path { fill: var(--line); }
#arrow-emphasis path { fill: var(--frontend); }
#arrow-security path { fill: var(--security); }
#arrow-dashed path { fill: var(--line); }
#arrow-flow-control path { fill: var(--flow-control); }
#arrow-flow-data path { fill: var(--flow-data); }
#arrow-flow-read path { fill: var(--flow-read); }
#arrow-flow-write path { fill: var(--flow-write); }
#arrow-flow-async path { fill: var(--flow-async); }
#arrow-flow-feedback path { fill: var(--flow-feedback); }
footer { margin-top: 12px; color: var(--muted); font-size: 12px; }
@media print {
  body { background: #fff; }
  main { width: 100%; padding: 0; }
  .toolbar, footer { display: none; }
  .diagram-frame { border: 0; }
}
</style>
</head>
<body>
<main>
  <header>
    <div>
      <h1>${N(e)}</h1>
      <p>${N(t||`${r} technical diagram`)}</p>
    </div>
    <div class="toolbar" aria-label="Diagram actions">
      <button type="button" data-action="theme">Toggle theme</button>
      <button type="button" data-action="svg">Download SVG</button>
      <button type="button" data-action="print">Print / Save PDF</button>
    </div>
  </header>
  <section class="diagram-frame" aria-label="${N(e)}">
${n}
  </section>
${s}
  <footer>Generated as a self-contained Frontend Craft HTML technical diagram. Export raster images from the browser after visual QA.</footer>
</main>
<script>
const root = document.documentElement;
const stored = localStorage.getItem("fec-tech-diagram-theme");
const diagramSvg = document.querySelector("[data-export-root]");
root.dataset.theme = stored === "dark" ? "dark" : "light";
diagramSvg.dataset.theme = root.dataset.theme;
diagramSvg.dataset.visualStyle = root.dataset.visualStyle;
document.querySelector('[data-action="theme"]').addEventListener("click", () => {
  const next = root.dataset.theme === "light" ? "dark" : "light";
  root.dataset.theme = next;
  diagramSvg.dataset.theme = next;
  localStorage.setItem("fec-tech-diagram-theme", next);
});
document.querySelector('[data-action="print"]').addEventListener("click", () => window.print());
document.querySelector('[data-action="svg"]').addEventListener("click", () => {
  const svg = document.querySelector("[data-export-root]");
  const clone = svg.cloneNode(true);
  const originals = [svg, ...svg.querySelectorAll("*")];
  const copies = [clone, ...clone.querySelectorAll("*")];
  const properties = ["fill","stroke","stroke-width","stroke-dasharray","font-family","font-size","font-weight","color","opacity","paint-order","text-anchor"];
  originals.forEach((element,index) => { const computed=getComputedStyle(element); properties.forEach(property=>copies[index].style?.setProperty(property,computed.getPropertyValue(property))); });
  const source = new XMLSerializer().serializeToString(clone);
  const blob = new Blob([source], { type: "image/svg+xml" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = document.title.replace(/[^a-z0-9_-]+/gi, "-").replace(/^-|-$/g, "").toLowerCase() + ".svg";
  link.click();
  URL.revokeObjectURL(link.href);
});
<\/script>
</body>
</html>
`}function Xe(e){return e.length===0?"":`  <section class="summary-grid" aria-label="Diagram summary">
${e.map(t=>`    <article class="summary-card summary-${t.type}">
      <h2>${N(t.title)}</h2>
      <ul>${t.items.map(n=>`<li>${N(n)}</li>`).join("")}</ul>
    </article>`).join(`
`)}
  </section>`}function oe(e,t,n,r){for(const o of r)o.points.some(([s,u])=>s<0||u<0)&&C.push({code:"connector-out-of-bounds",id:o.id,message:`Connector "${o.id}" has negative explicit coordinates.`});const a=n.filter(o=>o.kind!=="group");for(const o of n)(o.x<0||o.y<0)&&C.push({code:"box-out-of-bounds",id:o.id,message:`Box "${o.id}" has negative coordinates.`});for(let o=0;o<a.length;o++)for(let s=o+1;s<a.length;s++)Me(a[o],a[s])&&C.push({code:"box-overlap",id:a[o].id,message:`Nodes "${a[o].id}" and "${a[s].id}" overlap.`});return{canvas:le.width?le:{width:e,height:t},boxes:n.map(({id:o,x:s,y:u,width:d,height:w,label:y,kind:b})=>({id:o,x:s,y:u,width:d,height:w,label:y,kind:b})),groups:n.filter(o=>o.kind==="group").map(o=>({...o})),connectors:r,labels:O,coordinateSpace:"svg",scale:1,measurement:"estimated",issues:C}}function ge(e,t){const n=t==="x"?"width":"height";return Math.max(0,...e.map(r=>r[t]+r[n]))}function _e(e,t,n,r){return me(e,t,n,r)}function me(e,t,n,r){if(n===void 0)return de(e,t);if(!Array.isArray(n))throw g(r,"Expected array of [x, y] waypoints.");const a=n.map((s,u)=>{if(!Array.isArray(s)||s.length!==2||typeof s[0]!="number"||typeof s[1]!="number"||!Number.isFinite(s[0])||!Number.isFinite(s[1]))throw g(`${r}/${u}`,"Expected [x, y] number tuple.");return[s[0],s[1]]}),o=fe(e,t,I.filter(s=>s.id!==e.id&&s.id!==t.id),_,a);return C.push(...o.issues),_.push(o.points),o.points}function Ie(e,t){return t?e==="decision"?92:e==="start"||e==="success"||e==="failure"?128:132:132}function Re(e,t){return t?e==="decision"?92:e==="start"||e==="success"||e==="failure"?46:58:58}function Pe(e){return e==="decision"?"diamond":e==="start"||e==="success"||e==="failure"?"terminal":"box"}function Ge(e,t,n){if(e===void 0)return String(t);if(typeof e=="number"&&Number.isFinite(e))return String(e);if(typeof e=="string"&&e.length>0)return e;throw g(n,"Expected non-empty string or finite number.")}function st(e,t){const n=B(e),r=Z(e),a=t[0]-n,o=t[1]-r;return Math.abs(a)/Math.max(1,e.width)>Math.abs(o)/Math.max(1,e.height)?[a>=0?e.x+e.width:e.x,r]:[n,o>=0?e.y+e.height:e.y]}function Ve(e,t){if(e===!1)return[];if(e!==void 0)return A(e,"/legend").map((o,s)=>({label:F(o,"label",`/legend/${s}/label`),type:R(o.type,`/legend/${s}/type`)}));const n=new Set,r=[];for(const a of t)n.has(a.type)||(n.add(a.type),r.push({label:Qe(a.type),type:a.type}));return r}function Je(e,t,n,r=4){if(e.length===0)return"";const a=e.map((o,s)=>{const u=t+s%r*200,d=n+Math.floor(s/r)*72,w=H(o.label,160,12,16);return`<g class="node node-${o.type}"><rect x="${u}" y="${d+16}" width="16" height="10" rx="2"/>${D("legend-"+s,"legend","group",o.label,w,u+24+w.width/2,d+14,"sublabel")}</g>`}).join(`
`);return`<g class="legend"><text x="${t}" y="${n}" class="label">Legend</text>
${a}</g>`}function Ze(e,t,n,r=4){if(e.length===0)return"";const a=e.map((o,s)=>{const u=t+s%r*200,d=n+Math.floor(s/r)*72,w=H(o.label,152,12,16);return`<g class="edge flow-${o.type}"><path d="M ${u} ${d+22} L ${u+28} ${d+22}" marker-end="url(#arrow-flow-${o.type})"/>${D("flow-legend-"+s,"flow-legend","group",o.label,w,u+38+w.width/2,d+14,"sublabel")}</g>`}).join(`
`);return`<g class="flow-legend"><text x="${t}" y="${n}" class="label">Flow Legend</text>
${a}</g>`}function Qe(e){return{frontend:"Frontend",backend:"Backend",database:"Database",cloud:"Cloud",security:"Security",messagebus:"Message bus",external:"External",agent:"Agent",model:"Model",memory:"Memory",vectorstore:"Vector store",graphdb:"Graph DB",tool:"Tool",document:"Document",queue:"Queue",browser:"Browser",user:"User",gateway:"Gateway"}[e]??e}function Ke(e){return{control:"Control",data:"Data",read:"Read",write:"Write",async:"Async",feedback:"Feedback"}[e]??e}function et(e,t){return e===!1?[]:e!==void 0?A(e,"/flowLegend").map((r,a)=>({label:F(r,"label",`/flowLegend/${a}/label`),type:we(r.type,`/flowLegend/${a}/type`)??"control"})):t.length<2?[]:t.map(n=>({label:Ke(n),type:n}))}function $e(e){return e===void 0?[]:A(e,"/summary").slice(0,3).map((n,r)=>{const a=ve(n.items,`/summary/${r}/items`);return{title:F(n,"title",`/summary/${r}/title`),type:R(n.type,`/summary/${r}/type`),items:a.map((o,s)=>{if(typeof o!="string"||o.length===0)throw g(`/summary/${r}/items/${s}`,"Expected non-empty string.");return o})}})}function de(e,t){const n=fe(e,t,I.filter(r=>r.id!==e.id&&r.id!==t.id),_);return C.push(...n.issues),_.push(n.points),n.points}function B(e){return e.x+e.width/2}function Z(e){return e.y+e.height/2}function it(e,t){const n=e.split(/\s+/).filter(Boolean),r=[];let a="";for(const o of n)(a?`${a} ${o}`:o).length>t?(a&&r.push(a),a=o):a=a?`${a} ${o}`:o;return a&&r.push(a),r.length>0?r:[e]}function tt(e){return["agent","model","memory","vectorstore","graphdb","tool","document","queue","browser","user","gateway"].includes(e)}function ye(e,t){if(e===void 0)return"default";W(e,t);const n=e.style;if(n===void 0)return"default";if(typeof n!="string"||!qe.has(n))throw g(`${t}/style`,`Unsupported visual style "${String(n)}".`);return n}function we(e,t){if(e===void 0)return"";if(typeof e!="string"||!Be.has(e))throw g(t,`Unsupported flow "${String(e)}".`);return e}function R(e,t){if(typeof e!="string")return"external";if(!ze.has(e))throw g(t,`Unsupported node type "${e}".`);return e}function se(e,t){if(e===void 0)return"default";if(typeof e!="string"||!Ee.has(e))throw g(t,`Unsupported edge variant "${String(e)}".`);return e}function W(e,t){if(!e||typeof e!="object"||Array.isArray(e))throw g(t,"Expected object.")}function ve(e,t){if(!Array.isArray(e))throw g(t,"Expected array.");return e}function A(e,t){const n=ve(e,t);for(const[r,a]of n.entries())W(a,`${t}/${r}`);return n}function F(e,t,n){const r=e[t];if(typeof r!="string"||r.length===0)throw g(n,"Expected non-empty string.");return r}function j(e,t,n){const r=F(e,t,n);if(!/^[a-zA-Z][a-zA-Z0-9_-]*$/.test(r))throw g(n,"Expected id to match ^[a-zA-Z][a-zA-Z0-9_-]*$.");return r}function X(e,t,n){const r=e[t];if(typeof r!="number"||!Number.isFinite(r))throw g(n,"Expected finite number.");return r}function G(e,t,n){if(e.has(t))throw g(n,`Duplicate id "${t}".`);e instanceof Set?e.add(t):e.set(t,void 0)}function g(e,t){return new Error(`${e}: ${t}`)}function N(e){return e.replace(/[&<>"']/g,t=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[t]??t)}function rt(e,t){if(t==="json"){console.log(JSON.stringify(e,null,2));return}console.log(`Rendered ${e.type} technical diagram`),console.log(`- Output: ${e.output}`),e.manifest&&console.log(`- Manifest: ${e.manifest}`),console.log(`- Nodes: ${e.nodes}`),console.log(`- Connectors: ${e.connectors}`)}
