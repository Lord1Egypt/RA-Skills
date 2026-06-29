#!/usr/bin/env node
import X from"node:fs";import N from"node:path";const ce=new Set(["workflow","sequence","dataflow","lifecycle","architecture"]),de=new Set(["frontend","backend","database","cloud","security","messagebus","external","active","waiting","decision","success","failure","neutral","start","agent","model","memory","vectorstore","graphdb","tool","document","queue","browser","user","gateway"]),fe=new Set(["default","emphasis","security","dashed","return"]),ue=new Set(["default","terminal","blueprint","minimal","glass","warm","openai","editorial-dark"]),he=new Set(["control","data","read","write","async","feedback"]),W=$e(process.argv.slice(2));try{const e=V(W,"input"),t=V(W,"output"),r=V(W,"type"),n=W.format??"markdown";if(!ce.has(r))throw d("type",`Unsupported diagram type "${r}". Expected workflow, sequence, dataflow, lifecycle, or architecture.`);if(n!=="json"&&n!=="markdown")throw d("format",`Unsupported report format "${n}". Expected json or markdown.`);const a=pe(e);ge(a,r);const s=me(a,r),c="summary"in s?s.summary:[],u=ne(a.visual,"/visual"),h=Le(a.meta.title,a.meta.subtitle??"",s.svg,r,c,u);X.mkdirSync(N.dirname(N.resolve(t)),{recursive:!0}),X.writeFileSync(t,h,"utf8"),W.manifest&&(X.mkdirSync(N.dirname(N.resolve(W.manifest)),{recursive:!0}),X.writeFileSync(W.manifest,`${JSON.stringify(s.manifest,null,2)}
`,"utf8"));const y={ok:!0,type:r,input:e,output:t,manifest:W.manifest??null,nodes:s.manifest.boxes.length,connectors:s.manifest.connectors.length};Te(y,n)}catch(e){const t=e instanceof Error?e.message:String(e);W.format==="json"?console.log(JSON.stringify({ok:!1,error:t},null,2)):console.error(t),process.exitCode=1}function $e(e){const t={};for(let r=0;r<e.length;r+=1){const n=e[r];if(!n.startsWith("--"))throw d("argv",`Unexpected positional argument "${n}".`);const a=n.slice(2),s=e[r+1];if(!s||s.startsWith("--"))throw d(a,`Missing value for --${a}.`);t[a]=s,r+=1}return t}function V(e,t){const r=e[t];if(!r)throw d(t,`Missing required --${t}.`);return r}function pe(e){try{return JSON.parse(X.readFileSync(e,"utf8"))}catch(t){throw d("input",`Invalid JSON at /: ${t instanceof Error?t.message:String(t)}`)}}function ge(e,t){B(e,"/");const r=e;if(r.schema_version!==1)throw d("/schema_version","Expected schema_version to equal 1.");if(r.diagram_type!==t)throw d("/diagram_type",`Expected diagram_type to equal "${t}".`);B(r.meta,"/meta"),E(r.meta,"title","/meta/title"),ne(r.visual,"/visual")}function me(e,t){return t==="workflow"?Q(e,"nodes","edges"):t==="lifecycle"?Q(e,"states","transitions"):t==="sequence"?we(e):t==="architecture"?ye(e):ve(e)}function ye(e){const t=L(e.nodes,"/nodes"),r=L(e.connections,"/connections"),n=e.groups===void 0?[]:L(e.groups,"/groups"),a=new Set,s=new Map,c=[];for(const[i,o]of n.entries()){const p=S(o,"id",`/groups/${i}/id`);T(a,p,`/groups/${i}/id`);const k=E(o,"label",`/groups/${i}/label`),M=H(o.type,`/groups/${i}/type`),A={id:p,x:C(o,"x",`/groups/${i}/x`),y:C(o,"y",`/groups/${i}/y`),width:C(o,"width",`/groups/${i}/width`),height:C(o,"height",`/groups/${i}/height`),label:k,sublabel:"",type:M};c.push(A)}for(const[i,o]of t.entries()){const p=S(o,"id",`/nodes/${i}/id`);if(T(s,p,`/nodes/${i}/id`),typeof o.group=="string"&&!a.has(o.group))throw d(`/nodes/${i}/group`,`Unknown group "${o.group}".`);s.set(p,{id:p,x:C(o,"x",`/nodes/${i}/x`),y:C(o,"y",`/nodes/${i}/y`),width:typeof o.width=="number"?o.width:132,height:typeof o.height=="number"?o.height:62,label:E(o,"label",`/nodes/${i}/label`),sublabel:typeof o.sublabel=="string"?o.sublabel:"",type:H(o.type,`/nodes/${i}/type`)})}const u=[],h=new Set,y=r.map((i,o)=>{const p=S(i,"from",`/connections/${o}/from`),k=S(i,"to",`/connections/${o}/to`),M=s.get(p),A=s.get(k);if(!M)throw d(`/connections/${o}/from`,`Unknown endpoint "${p}".`);if(!A)throw d(`/connections/${o}/to`,`Unknown endpoint "${k}".`);const Y=J(i.variant,`/connections/${o}/variant`),D=ae(i.flow,`/connections/${o}/flow`);D&&h.add(D);const O=ze(M,A,i.waypoints,`/connections/${o}/waypoints`);return u.push({id:`${p}-${k}-${o}`,from:p,to:k,points:O}),R(O,Y,typeof i.label=="string"?i.label:"",D)}).join(`
`),v=[...c,...s.values()],z=Math.max(360,K(v,"y")+64),j=Ae(e.legend,[...s.values()]),$=De(e.flowLegend,[...h]),l=Math.max(88+j.length*118,88+$.length*128),f=Math.max(860,K(v,"x")+64,l),g=Ue(j,44,z-4),w=We($,44,z+(j.length>0?42:0)),b=z+(j.length>0?54:0)+($.length>0?54:0),q=c.map(be).join(`
`),U=[...s.values()].map(I).join(`
`);return{svg:G(f,b,`${q}
${y}
${U}
${g}
${w}`),manifest:P(f,b,v,u),summary:re(e.summary)}}function Q(e,t,r){const n=L(e.lanes,"/lanes"),a=L(e[t],`/${t}`),s=L(e[r],`/${r}`),c=t==="nodes",u=new Set;for(const[i,o]of n.entries()){B(o,`/lanes/${i}`);const p=S(o,"id",`/lanes/${i}/id`);E(o,"label",`/lanes/${i}/label`),T(u,p,`/lanes/${i}/id`)}const h=new Map,y=Math.max(0,...a.map((i,o)=>(B(i,`/${t}/${o}`),C(i,"col",`/${t}/${o}/col`)))),v=Math.max(780,190+(y+1)*180),z=Math.max(420,140+n.length*145),j=118,$=72,l=142,f=172,g=new Map(n.map((i,o)=>[String(i.id),o]));for(const[i,o]of a.entries()){const p=S(o,"id",`/${t}/${i}/id`);T(h,p,`/${t}/${i}/id`);const k=S(o,"lane",`/${t}/${i}/lane`);if(!u.has(k))throw d(`/${t}/${i}/lane`,`Unknown lane "${k}".`);const M=H(o.type,`/${t}/${i}/type`),A=E(o,"label",`/${t}/${i}/label`),Y=typeof o.sublabel=="string"?o.sublabel:"",D=C(o,"col",`/${t}/${i}/col`),O=typeof o.yOffset=="number"?o.yOffset:0,se=typeof o.width=="number"?o.width:Be(M,c),ie=typeof o.height=="number"?o.height:Ee(M,c),le={id:p,x:l+D*f,y:$+Number(g.get(k))*j+38+O,width:se,height:ie,label:A,sublabel:Y,type:M,actor:c&&typeof o.actor=="string"?o.actor:"",step:c?qe(o.step,i+1,`/${t}/${i}/step`):"",shape:c?je(M):"box"};h.set(p,le)}const w=[],b=s.map((i,o)=>{B(i,`/${r}/${o}`);const p=S(i,"from",`/${r}/${o}/from`),k=S(i,"to",`/${r}/${o}/to`),M=h.get(p),A=h.get(k);if(!M)throw d(`/${r}/${o}/from`,`Unknown endpoint "${p}".`);if(!A)throw d(`/${r}/${o}/to`,`Unknown endpoint "${k}".`);const Y=J(i.variant,`/${r}/${o}/variant`),D=i.waypoints===void 0?Z(M,A):ee(M,A,i.waypoints,`/${r}/${o}/waypoints`),O=`${p}-${k}-${o}`;return w.push({id:O,from:p,to:k,points:D}),R(D,Y,typeof i.label=="string"?i.label:"")}).join(`
`),q=n.map((i,o)=>{const p=$+o*j;return`<g class="lane"><rect x="34" y="${p}" width="${v-68}" height="${j-16}" rx="10"/><text x="52" y="${p+28}" class="label muted">${m(String(i.label))}</text></g>`}).join(`
`),U=[...h.values()].map(I).join(`
`);return{svg:G(v,z,`${q}
${b}
${U}`),manifest:P(v,z,[...h.values()],w),summary:c?re(e.summary):[]}}function we(e){const t=L(e.participants,"/participants"),r=L(e.messages,"/messages"),n=new Set,a=Math.max(760,160+t.length*170),s=Math.max(420,170+r.length*82),c=74,u=(a-160)/Math.max(1,t.length-1),h=new Map;for(const[l,f]of t.entries()){B(f,`/participants/${l}`);const g=S(f,"id",`/participants/${l}/id`);T(n,g,`/participants/${l}/id`);const w=H(f.type,`/participants/${l}/type`),b=E(f,"label",`/participants/${l}/label`),q=t.length===1?a/2-64:80+l*u-64;h.set(g,{id:g,x:q,y:c,width:128,height:56,label:b,sublabel:typeof f.sublabel=="string"?f.sublabel:"",type:w})}const y=[],v=[...h.values()].map(l=>`<line x1="${x(l)}" y1="${l.y+l.height}" x2="${x(l)}" y2="${s-56}" class="lifeline"/>`).join(`
`),z=r.map((l,f)=>{B(l,`/messages/${f}`);const g=S(l,"from",`/messages/${f}/from`),w=S(l,"to",`/messages/${f}/to`),b=h.get(g),q=h.get(w);if(!b)throw d(`/messages/${f}/from`,`Unknown endpoint "${g}".`);if(!q)throw d(`/messages/${f}/to`,`Unknown endpoint "${w}".`);const U=c+104+f*72,_=[[x(b),U],[x(q),U]],i=J(l.variant,`/messages/${f}/variant`);return y.push({id:`${g}-${w}-${f}`,from:g,to:w,points:_}),R(_,i,typeof l.label=="string"?l.label:"")}).join(`
`),j=[...h.values()].map(I).join(`
`);return{svg:G(a,s,`${v}
${z}
${j}`),manifest:P(a,s,[...h.values()],y)}}function ve(e){const t=L(e.stages,"/stages"),r=L(e.nodes,"/nodes"),n=L(e.flows,"/flows"),a=Math.max(860,150+t.length*180),s=Math.max(460,180+ke(r)*110),c=(a-84)/Math.max(1,t.length),u=new Map;for(const[$,l]of t.entries())B(l,`/stages/${$}`),E(l,"label",`/stages/${$}/label`);for(const[$,l]of r.entries()){B(l,`/nodes/${$}`);const f=S(l,"id",`/nodes/${$}/id`);T(u,f,`/nodes/${$}/id`);const g=C(l,"stage",`/nodes/${$}/stage`);if(g<0||g>=t.length)throw d(`/nodes/${$}/stage`,`Stage index ${g} is outside /stages.`);const w=typeof l.row=="number"?l.row:xe(r,$,g),b=H(l.type,`/nodes/${$}/type`);u.set(f,{id:f,x:54+g*c+Math.max(8,c/2-64),y:118+w*96,width:128,height:58,label:E(l,"label",`/nodes/${$}/label`),sublabel:typeof l.sublabel=="string"?l.sublabel:"",type:b})}const h=[],y=t.map(($,l)=>{const f=42+l*c;return`<g class="stage"><rect x="${f}" y="64" width="${c-10}" height="${s-118}" rx="12"/><text x="${f+18}" y="92" class="label muted">${m(String($.label))}</text></g>`}).join(`
`),v=n.map(($,l)=>{B($,`/flows/${l}`);const f=S($,"from",`/flows/${l}/from`),g=S($,"to",`/flows/${l}/to`),w=u.get(f),b=u.get(g);if(!w)throw d(`/flows/${l}/from`,`Unknown endpoint "${f}".`);if(!b)throw d(`/flows/${l}/to`,`Unknown endpoint "${g}".`);const q=J($.variant,`/flows/${l}/variant`),U=Z(w,b);return h.push({id:`${f}-${g}-${l}`,from:f,to:g,points:U}),R(U,q,typeof $.label=="string"?$.label:"")}).join(`
`),z=[...u.values()].map(I).join(`
`);return{svg:G(a,s,`${y}
${v}
${z}`),manifest:P(a,s,[...u.values()],h)}}function ke(e){const t=new Map;for(const r of e)typeof r.stage=="number"&&t.set(r.stage,(t.get(r.stage)??0)+1);return Math.max(1,...t.values())}function xe(e,t,r){let n=0;for(let a=0;a<t;a+=1)e[a].stage===r&&(n+=1);return n}function I(e){const t=He(e.label,18).slice(0,2),r=e.shape??"box",n=Oe(e.type),a=r==="diamond"?F(e)-(t.length>1?5:-3):e.y+(n?Math.max(30,e.height-24):23),s=t.map((v,z)=>`<text x="${x(e)}" y="${a+z*13}" class="label" text-anchor="middle">${m(v)}</text>`).join(`
`),c=e.sublabel?`<text x="${x(e)}" y="${e.y+e.height-13}" class="sublabel" text-anchor="middle">${m(e.sublabel)}</text>`:"",u=e.actor?`<text x="${x(e)}" y="${e.y-8}" class="actor" text-anchor="middle">${m(e.actor)}</text>`:"",h=e.step?`<g class="step-badge"><circle cx="${e.x+13}" cy="${e.y+13}" r="10"/><text x="${e.x+13}" y="${e.y+17}" text-anchor="middle">${m(e.step)}</text></g>`:"",y=Se(e)??(r==="diamond"?`<polygon points="${x(e)},${e.y} ${e.x+e.width},${F(e)} ${x(e)},${e.y+e.height} ${e.x},${F(e)}"/>`:`<rect x="${e.x}" y="${e.y}" width="${e.width}" height="${e.height}" rx="${r==="terminal"?Math.round(e.height/2):10}"/>`);return`<g class="node node-${e.type}">${u}
${y}
${h}
${s}
${c}</g>`}function Se(e){const t=x(e),r=F(e);if(e.type==="agent"){const n=Math.min(28,e.width*.18);return`<polygon points="${e.x+n},${e.y} ${e.x+e.width-n},${e.y} ${e.x+e.width},${r} ${e.x+e.width-n},${e.y+e.height} ${e.x+n},${e.y+e.height} ${e.x},${r}"/><rect x="${e.x+5}" y="${e.y+5}" width="${e.width-10}" height="${e.height-10}" rx="10" fill="none" opacity="0.45"/>`}if(e.type==="model")return`<rect x="${e.x}" y="${e.y}" width="${e.width}" height="${e.height}" rx="14"/><rect x="${e.x+5}" y="${e.y+5}" width="${e.width-10}" height="${e.height-10}" rx="10" fill="none" opacity="0.5"/><path d="M ${t-12} ${e.y+20} L ${t-4} ${e.y+20} L ${t} ${e.y+10} L ${t+4} ${e.y+20} L ${t+12} ${e.y+20} L ${t+6} ${e.y+27} L ${t+9} ${e.y+38} L ${t} ${e.y+31} L ${t-9} ${e.y+38} L ${t-6} ${e.y+27} Z" class="node-glyph"/>`;if(e.type==="memory")return`<rect x="${e.x}" y="${e.y}" width="${e.width}" height="${e.height}" rx="12" stroke-dasharray="6 4"/>`;if(e.type==="database"||e.type==="vectorstore"){const n=Math.min(14,e.height/5),a=e.type==="vectorstore"?`<ellipse cx="${t}" cy="${e.y+e.height*.45}" rx="${e.width/2}" ry="${n}" fill="none" opacity="0.45"/><ellipse cx="${t}" cy="${e.y+e.height*.66}" rx="${e.width/2}" ry="${n}" fill="none" opacity="0.32"/>`:"";return`<ellipse cx="${t}" cy="${e.y+n}" rx="${e.width/2}" ry="${n}"/><rect x="${e.x}" y="${e.y+n}" width="${e.width}" height="${e.height-n*2}" stroke="none"/><line x1="${e.x}" y1="${e.y+n}" x2="${e.x}" y2="${e.y+e.height-n}"/><line x1="${e.x+e.width}" y1="${e.y+n}" x2="${e.x+e.width}" y2="${e.y+e.height-n}"/>${a}<ellipse cx="${t}" cy="${e.y+e.height-n}" rx="${e.width/2}" ry="${n}"/>`}if(e.type==="graphdb")return`<rect x="${e.x}" y="${e.y}" width="${e.width}" height="${e.height}" rx="14"/><circle cx="${t-18}" cy="${r-2}" r="12" class="node-glyph-outline"/><circle cx="${t+8}" cy="${r-14}" r="10" class="node-glyph-outline"/><circle cx="${t+22}" cy="${r+10}" r="11" class="node-glyph-outline"/><line x1="${t-7}" y1="${r-7}" x2="${t}" y2="${r-12}" class="node-glyph-line"/><line x1="${t+16}" y1="${r-5}" x2="${t+20}" y2="${r}" class="node-glyph-line"/>`;if(e.type==="tool")return`<rect x="${e.x}" y="${e.y}" width="${e.width}" height="${e.height}" rx="10"/><circle cx="${t}" cy="${e.y+24}" r="9" class="node-glyph-outline"/><line x1="${t}" y1="${e.y+11}" x2="${t}" y2="${e.y+16}" class="node-glyph-line"/><line x1="${t}" y1="${e.y+32}" x2="${t}" y2="${e.y+37}" class="node-glyph-line"/><line x1="${t-13}" y1="${e.y+24}" x2="${t-8}" y2="${e.y+24}" class="node-glyph-line"/><line x1="${t+8}" y1="${e.y+24}" x2="${t+13}" y2="${e.y+24}" class="node-glyph-line"/>`;if(e.type==="document"){const n=Math.min(16,e.width*.16);return`<path d="M ${e.x} ${e.y} L ${e.x+e.width-n} ${e.y} L ${e.x+e.width} ${e.y+n} L ${e.x+e.width} ${e.y+e.height} L ${e.x} ${e.y+e.height} Z"/><path d="M ${e.x+e.width-n} ${e.y} L ${e.x+e.width-n} ${e.y+n} L ${e.x+e.width} ${e.y+n}" fill="none"/>`}if(e.type==="queue"){const n=Math.min(18,e.height/3);return`<ellipse cx="${e.x+n}" cy="${r}" rx="${n*.58}" ry="${n}"/><rect x="${e.x+n}" y="${r-n}" width="${e.width-n*2}" height="${n*2}" stroke="none"/><line x1="${e.x+n}" y1="${r-n}" x2="${e.x+e.width-n}" y2="${r-n}"/><line x1="${e.x+n}" y1="${r+n}" x2="${e.x+e.width-n}" y2="${r+n}"/><ellipse cx="${e.x+e.width-n}" cy="${r}" rx="${n*.58}" ry="${n}"/>`}if(e.type==="browser")return`<rect x="${e.x}" y="${e.y}" width="${e.width}" height="${e.height}" rx="10"/><rect x="${e.x}" y="${e.y}" width="${e.width}" height="20" rx="10" class="node-chrome"/><circle cx="${e.x+14}" cy="${e.y+10}" r="3" class="node-dot"/><circle cx="${e.x+26}" cy="${e.y+10}" r="3" class="node-dot"/><circle cx="${e.x+38}" cy="${e.y+10}" r="3" class="node-dot"/>`;if(e.type==="user")return`<rect x="${e.x}" y="${e.y}" width="${e.width}" height="${e.height}" rx="12"/><circle cx="${t}" cy="${e.y+22}" r="9" class="node-glyph-outline"/><path d="M ${t-16} ${e.y+43} Q ${t} ${e.y+28} ${t+16} ${e.y+43}" class="node-glyph-line"/>`;if(e.type==="gateway"){const n=Math.min(22,e.width*.18);return`<polygon points="${e.x+n},${e.y} ${e.x+e.width-n},${e.y} ${e.x+e.width},${r} ${e.x+e.width-n},${e.y+e.height} ${e.x+n},${e.y+e.height} ${e.x},${r}"/>`}return null}function be(e){return`<g class="group group-${e.type}"><rect x="${e.x}" y="${e.y}" width="${e.width}" height="${e.height}" rx="14"/><text x="${e.x+16}" y="${e.y+26}" class="label muted">${m(e.label)}</text></g>`}function R(e,t,r,n=""){const a=e.map(([h,y],v)=>`${v===0?"M":"L"} ${h} ${y}`).join(" "),s=e[Math.floor((e.length-1)/2)],c=r?`<text x="${s[0]}" y="${s[1]-8}" class="edge-label" text-anchor="middle">${m(r)}</text>`:"",u=n?`flow-${n}`:t==="return"?"default":t;return`<g class="edge edge-${t}${n?` flow-${n}`:""}"><path d="${a}" marker-end="url(#arrow-${u})"/>
${c}</g>`}function G(e,t,r){return`<svg class="tech-diagram" data-export-root="1" role="img" viewBox="0 0 ${e} ${t}" xmlns="http://www.w3.org/2000/svg">
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
  ${r}
</svg>`}function Le(e,t,r,n,a=[],s="default"){const c=Me(a);return`<!doctype html>
<html lang="en" data-theme="auto" data-visual-style="${m(s)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${m(e)}</title>
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
.label { fill: var(--text); font-weight: 650; font-size: 12px; }
.sublabel, .muted, .actor { fill: var(--muted); font-size: 10px; }
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
.edge-label { fill: var(--muted); font-size: 10px; paint-order: stroke; stroke: var(--surface); stroke-width: 5px; stroke-linejoin: round; }
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
      <h1>${m(e)}</h1>
      <p>${m(t||`${n} technical diagram`)}</p>
    </div>
    <div class="toolbar" aria-label="Diagram actions">
      <button type="button" data-action="theme">Toggle theme</button>
      <button type="button" data-action="svg">Download SVG</button>
      <button type="button" data-action="print">Print / Save PDF</button>
    </div>
  </header>
  <section class="diagram-frame" aria-label="${m(e)}">
${r}
  </section>
${c}
  <footer>Generated as a self-contained Frontend Craft HTML technical diagram. Export raster images from the browser after visual QA.</footer>
</main>
<script>
const root = document.documentElement;
const stored = localStorage.getItem("fec-tech-diagram-theme");
if (stored === "dark" || stored === "light") root.dataset.theme = stored;
document.querySelector('[data-action="theme"]').addEventListener("click", () => {
  const next = root.dataset.theme === "light" ? "dark" : "light";
  root.dataset.theme = next;
  localStorage.setItem("fec-tech-diagram-theme", next);
});
document.querySelector('[data-action="print"]').addEventListener("click", () => window.print());
document.querySelector('[data-action="svg"]').addEventListener("click", () => {
  const svg = document.querySelector("[data-export-root]");
  const source = new XMLSerializer().serializeToString(svg);
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
`}function Me(e){return e.length===0?"":`  <section class="summary-grid" aria-label="Diagram summary">
${e.map(t=>`    <article class="summary-card summary-${t.type}">
      <h2>${m(t.title)}</h2>
      <ul>${t.items.map(r=>`<li>${m(r)}</li>`).join("")}</ul>
    </article>`).join(`
`)}
  </section>`}function P(e,t,r,n){return{canvas:{width:e,height:t},boxes:r.map(({id:a,x:s,y:c,width:u,height:h,label:y})=>({id:a,x:s,y:c,width:u,height:h,label:y})),connectors:n}}function K(e,t){const r=t==="x"?"width":"height";return Math.max(0,...e.map(n=>n[t]+n[r]))}function ze(e,t,r,n){return ee(e,t,r,n)}function ee(e,t,r,n){if(r===void 0)return Z(e,t);if(!Array.isArray(r))throw d(n,"Expected array of [x, y] waypoints.");const a=r.map((u,h)=>{if(!Array.isArray(u)||u.length!==2||typeof u[0]!="number"||typeof u[1]!="number")throw d(`${n}/${h}`,"Expected [x, y] number tuple.");return[u[0],u[1]]}),s=a[0]??[x(t),F(t)],c=a[a.length-1]??[x(e),F(e)];return[te(e,s),...a,te(t,c)]}function Be(e,t){return t?e==="decision"?92:e==="start"||e==="success"||e==="failure"?128:132:132}function Ee(e,t){return t?e==="decision"?92:e==="start"||e==="success"||e==="failure"?46:58:58}function je(e){return e==="decision"?"diamond":e==="start"||e==="success"||e==="failure"?"terminal":"box"}function qe(e,t,r){if(e===void 0)return String(t);if(typeof e=="number"&&Number.isFinite(e))return String(e);if(typeof e=="string"&&e.length>0)return e;throw d(r,"Expected non-empty string or finite number.")}function te(e,t){const r=x(e),n=F(e),a=t[0]-r,s=t[1]-n;return Math.abs(a)/Math.max(1,e.width)>Math.abs(s)/Math.max(1,e.height)?[a>=0?e.x+e.width:e.x,n]:[r,s>=0?e.y+e.height:e.y]}function Ae(e,t){if(e===!1)return[];if(e!==void 0)return L(e,"/legend").map((s,c)=>({label:E(s,"label",`/legend/${c}/label`),type:H(s.type,`/legend/${c}/type`)}));const r=new Set,n=[];for(const a of t)r.has(a.type)||(r.add(a.type),n.push({label:Fe(a.type),type:a.type}));return n}function Ue(e,t,r){if(e.length===0)return"";const n=e.map((a,s)=>{const c=t+s*118;return`<g class="node node-${a.type}"><rect x="${c}" y="${r+16}" width="16" height="10" rx="2"/><text x="${c+24}" y="${r+25}" class="sublabel">${m(a.label)}</text></g>`}).join(`
`);return`<g class="legend"><text x="${t}" y="${r}" class="label">Legend</text>
${n}</g>`}function We(e,t,r){if(e.length===0)return"";const n=e.map((a,s)=>{const c=t+s*128;return`<g class="edge flow-${a.type}"><path d="M ${c} ${r+22} L ${c+28} ${r+22}" marker-end="url(#arrow-flow-${a.type})"/><text x="${c+38}" y="${r+26}" class="sublabel">${m(a.label)}</text></g>`}).join(`
`);return`<g class="flow-legend"><text x="${t}" y="${r}" class="label">Flow Legend</text>
${n}</g>`}function Fe(e){return{frontend:"Frontend",backend:"Backend",database:"Database",cloud:"Cloud",security:"Security",messagebus:"Message bus",external:"External",agent:"Agent",model:"Model",memory:"Memory",vectorstore:"Vector store",graphdb:"Graph DB",tool:"Tool",document:"Document",queue:"Queue",browser:"Browser",user:"User",gateway:"Gateway"}[e]??e}function Ce(e){return{control:"Control",data:"Data",read:"Read",write:"Write",async:"Async",feedback:"Feedback"}[e]??e}function De(e,t){return e===!1?[]:e!==void 0?L(e,"/flowLegend").map((n,a)=>({label:E(n,"label",`/flowLegend/${a}/label`),type:ae(n.type,`/flowLegend/${a}/type`)??"control"})):t.length<2?[]:t.map(r=>({label:Ce(r),type:r}))}function re(e){return e===void 0?[]:L(e,"/summary").slice(0,3).map((r,n)=>{const a=oe(r.items,`/summary/${n}/items`);return{title:E(r,"title",`/summary/${n}/title`),type:H(r.type,`/summary/${n}/type`),items:a.map((s,c)=>{if(typeof s!="string"||s.length===0)throw d(`/summary/${n}/items/${c}`,"Expected non-empty string.");return s})}})}function Z(e,t){const r=[x(e),F(e)],n=[x(t),F(t)];if(Math.abs(r[1]-n[1])<18)return[[e.x+e.width,r[1]],[t.x,n[1]]];const a=Math.round((r[0]+n[0])/2);return[[r[0],r[1]],[a,r[1]],[a,n[1]],[n[0],n[1]]]}function x(e){return e.x+e.width/2}function F(e){return e.y+e.height/2}function He(e,t){const r=e.split(/\s+/).filter(Boolean),n=[];let a="";for(const s of r)(a?`${a} ${s}`:s).length>t?(a&&n.push(a),a=s):a=a?`${a} ${s}`:s;return a&&n.push(a),n.length>0?n:[e]}function Oe(e){return["agent","model","memory","vectorstore","graphdb","tool","document","queue","browser","user","gateway"].includes(e)}function ne(e,t){if(e===void 0)return"default";B(e,t);const r=e.style;if(r===void 0)return"default";if(typeof r!="string"||!ue.has(r))throw d(`${t}/style`,`Unsupported visual style "${String(r)}".`);return r}function ae(e,t){if(e===void 0)return"";if(typeof e!="string"||!he.has(e))throw d(t,`Unsupported flow "${String(e)}".`);return e}function H(e,t){if(typeof e!="string")return"external";if(!de.has(e))throw d(t,`Unsupported node type "${e}".`);return e}function J(e,t){if(e===void 0)return"default";if(typeof e!="string"||!fe.has(e))throw d(t,`Unsupported edge variant "${String(e)}".`);return e}function B(e,t){if(!e||typeof e!="object"||Array.isArray(e))throw d(t,"Expected object.")}function oe(e,t){if(!Array.isArray(e))throw d(t,"Expected array.");return e}function L(e,t){const r=oe(e,t);for(const[n,a]of r.entries())B(a,`${t}/${n}`);return r}function E(e,t,r){const n=e[t];if(typeof n!="string"||n.length===0)throw d(r,"Expected non-empty string.");return n}function S(e,t,r){const n=E(e,t,r);if(!/^[a-zA-Z][a-zA-Z0-9_-]*$/.test(n))throw d(r,"Expected id to match ^[a-zA-Z][a-zA-Z0-9_-]*$.");return n}function C(e,t,r){const n=e[t];if(typeof n!="number"||!Number.isFinite(n))throw d(r,"Expected finite number.");return n}function T(e,t,r){if(e.has(t))throw d(r,`Duplicate id "${t}".`);e instanceof Set?e.add(t):e.set(t,void 0)}function d(e,t){return new Error(`${e}: ${t}`)}function m(e){return e.replace(/[&<>"']/g,t=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[t]??t)}function Te(e,t){if(t==="json"){console.log(JSON.stringify(e,null,2));return}console.log(`Rendered ${e.type} technical diagram`),console.log(`- Output: ${e.output}`),e.manifest&&console.log(`- Manifest: ${e.manifest}`),console.log(`- Nodes: ${e.nodes}`),console.log(`- Connectors: ${e.connectors}`)}
