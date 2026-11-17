#!/usr/bin/env python3
"""Generate a self-contained, read-only semantic/mapping/evidence HTML explorer."""
import argparse
import json
from pathlib import Path
import sys
from _review import STYLE as REVIEW_STYLE, SCRIPT as REVIEW_SCRIPT
from _contract import (binding_errors, digest, load, object_digest,
                       ont_entities, ont_relations, ont_relation_id)


def ontology_view(model):
    """本体声明层 + 投影状态（静态对账结果，不做推理）。"""
    entities, relations = ont_entities(model), ont_relations(model)
    if not entities and not relations:
        return None
    projected_by = {}
    for ds in model.get("datasets", []) or []:
        if ds.get("ontology_ref"):
            projected_by.setdefault(ds["ontology_ref"], []).append(ds.get("name"))
    projected_rels = {r.get("ontology_ref") for r in model.get("relationships", []) or []
                      if r.get("ontology_ref")}
    return {
        "entities": [{**e, "projected_by": projected_by.get(e.get("name"), [])}
                     for e in entities],
        "relations": [{**r, "id": ont_relation_id(r),
                       "projected": ont_relation_id(r) in projected_rels}
                      for r in relations],
    }


def build_data(model_path, report_paths=(), session_path=None, history_path=None):
    model = load(model_path)
    reports = []
    for path in report_paths:
        report = load(path)
        reports.append({"name": Path(path).name, "binding_errors": binding_errors(report, model_path), "report": report})
    session = load(session_path) if session_path else None
    if session and object_digest(session["model"]) != object_digest(model):
        raise ValueError("session does not match this model")
    history = None
    if history_path:
        history = []
        with open(history_path, encoding="utf-8") as stream:
            for line in stream:
                line = line.strip()
                if line:
                    history.append(json.loads(line))
    return {"model": model, "sha256": digest(model_path), "reports": reports,
            "ontology": ontology_view(model), "history": history,
            "gaps": session.get("gaps", []) if session else [],
            "decisions": session.get("decisions", []) if session else [],
            "scenarios": session.get("scenarios", []) if session else []}


def render_html(data):
    payload = json.dumps(data, ensure_ascii=False, default=str).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    return PAGE.replace('__REVIEW_STYLE__', REVIEW_STYLE).replace('__REVIEW_SCRIPT__', REVIEW_SCRIPT).replace('__PAYLOAD__', payload)


PAGE = r'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; connect-src 'none'; base-uri 'none'; form-action 'none'">
<title>语义交付 · 模型与证据</title><style>
:root{color-scheme:light;
--ink:#15303c;--soft:#57707f;--faint:#8ba2ad;
--line:#dfe8ec;--line-soft:#edf2f4;--bg:#eef3f5;--panel:#fff;
--accent:#0d7377;--accent-deep:#0a5a5e;--accent-soft:rgba(13,115,119,.12);
--ont:#0f7b6c;--phys:#5b7aa8;
--amber:#d97706;--red:#c0392b;--ok:#157347;
--shadow:0 1px 2px rgba(15,42,53,.05),0 6px 18px rgba(15,42,53,.06);
--shadow-lift:0 2px 4px rgba(15,42,53,.07),0 10px 26px rgba(15,42,53,.10);
--radius:14px}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.65 system-ui,"Segoe UI","Microsoft YaHei",sans-serif;-webkit-font-smoothing:antialiased}
header{background:linear-gradient(115deg,#0a323d 0%,#0d5257 55%,#0f6e64 100%);color:#fff;padding:34px max(28px,calc((100vw - 1360px)/2)) 30px}
h1{font-size:26px;font-weight:700;letter-spacing:.5px;margin:0}
header p{color:rgba(255,255,255,.78);margin:9px 0 0;max-width:760px;font-size:14px}
main{max-width:1408px;margin:auto;padding:26px 24px 40px}
.bar{display:flex;gap:12px;flex-wrap:wrap;align-items:center;margin-bottom:22px}
input,select,button{font:inherit;border:1px solid #c3d2da;border-radius:10px;padding:9px 12px;background:#fff;color:var(--ink);transition:border-color .15s,box-shadow .15s,background .15s}
input:focus-visible,select:focus-visible,button:focus-visible{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-soft)}
input{flex:1;min-width:230px}
button{cursor:pointer}
button:hover{border-color:var(--accent)}
.bar label{color:var(--soft);font-size:14px}
.layout{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(290px,1fr);gap:22px}
.panel{background:var(--panel);border:1px solid #e6edf0;border-radius:var(--radius);padding:22px;margin-bottom:20px;box-shadow:var(--shadow)}
h2{font-size:17px;font-weight:650;margin:0 0 12px;letter-spacing:.2px}
h3{font-size:15px;font-weight:600;margin:0}
.muted{color:var(--soft);font-size:13px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px}
.card{text-align:left;display:block;width:100%;padding:15px 16px 15px 18px;background:#fff;border:1px solid var(--line);border-left:3px solid #c6d4dc;border-radius:12px;overflow-wrap:anywhere;transition:border-color .15s,transform .15s,box-shadow .15s}
.card:hover,.card:focus-visible{border-color:#bcd5d2;border-left-color:var(--accent);transform:translateY(-1px);box-shadow:var(--shadow-lift)}
.badge{display:inline-block;padding:2px 10px;border-radius:999px;font-size:12px;line-height:1.7;background:#e9f0f2;color:#48606e;margin:5px 6px 2px 0}
.bad{background:#fdeae2;color:#a0401a}
.good{background:#e0f2e8;color:#12714a}
pre{white-space:pre-wrap;overflow-wrap:anywhere;font:12.5px/1.65 ui-monospace,"Cascadia Code",Consolas,monospace;background:#f6f9fa;border:1px solid var(--line-soft);padding:14px;border-radius:10px;color:#27434f}
.edge,.item{padding:12px 4px;border-bottom:1px solid var(--line-soft);border-radius:8px;transition:background .15s}
.edge:hover,.item:hover{background:#f5f9f9}
.edge:last-child,.item:last-child{border-bottom:0}
.edge button,.item button{border:0;background:none;padding:0;color:var(--accent-deep);text-align:left;font-weight:550}
.edge button:hover,.item button:hover{color:var(--accent);text-decoration:underline}
#counts{margin-left:auto}
footer{color:var(--faint);font-size:12px;overflow-wrap:anywhere;padding:6px 2px 0}
.gbtn{padding:6px 14px;font-size:13px;border-radius:999px;background:#fff}
.gbtn:hover{background:#f0f7f6;border-color:var(--accent);color:var(--accent-deep)}
.efchip{display:inline-flex;align-items:center;gap:6px;margin:0 12px 6px 0;font-size:13px;color:var(--soft);cursor:pointer;padding:3px 10px 3px 6px;border:1px solid var(--line);border-radius:999px;background:#fff;transition:border-color .15s,background .15s}
.efchip:hover{border-color:var(--accent)}
.efchip input{accent-color:var(--accent);margin:0;flex:none;min-width:0;width:auto;padding:0}
.efdot{width:10px;height:10px;border-radius:3px;flex:none}
.chip{padding:4px 13px;font-size:13px;border-radius:999px;background:#fff;margin:0 8px 6px 0}
.chip.on{background:var(--accent);border-color:var(--accent);color:#fff}
g[data-node],[data-edge],[data-edgelabel]{transition:opacity .25s ease}
g[data-node]:hover rect.card{stroke:var(--accent);stroke-width:2.2}
g[data-node]:focus-visible{outline:none}
g[data-node]:focus-visible rect.card{stroke:var(--accent);stroke-width:2.4}
@media(max-width:850px){.layout{grid-template-columns:1fr}header{padding:26px 20px}.panel{padding:16px}main{padding:16px}}
__REVIEW_STYLE__
</style></head><body><header><h1>语义交付 · 人工核验</h1><p>从业务问题进入，核对定义、关系、映射与预期结果。此页是可离线阅读的交付快照；图不代表运行血缘或自动验收。</p></header>
<main><div class="bar"><label for="search">搜索</label><input id="search" placeholder="数据集、字段、指标或缺口"><label for="filter">显示</label><select id="filter"><option value="all">全部内容</option><option value="gaps">待补齐内容</option><option value="evidence">验证证据</option></select><span id="counts" class="muted"></span></div>
<div class="layout"><section><div class="panel" id="semantic"><h2>数据集与物理映射</h2><p class="muted">模型声明的 source 与 fields。未观测实际运行链路。</p><div id="datasets" class="cards"></div><h2 style="margin-top:24px">语义关系</h2><div id="relations"></div><h2 style="margin-top:24px">指标</h2><div id="metrics"></div></div><div class="panel" id="gapPanel"><h2>补齐与决策</h2><div id="gaps"></div></div><div class="panel" id="evidencePanel"><h2>验证证据</h2><div id="reports"></div></div></section><aside><div class="panel"><h2 id="detailTitle">选择对象查看详情</h2><p class="muted">来源、计算口径、确认依据和完整属性在此显示。</p><div id="detail"></div></div></aside></div>
<footer id="footer"></footer></main><script id="payload" type="application/json">__PAYLOAD__</script><script>
'use strict';
const data=JSON.parse(document.getElementById('payload').textContent), m=data.model;
const $=id=>document.getElementById(id);
function element(tag,text,cls){const e=document.createElement(tag);if(text!==undefined)e.textContent=String(text);if(cls)e.className=cls;return e}
document.head.append(element('style','aside .panel{position:sticky;top:16px;max-height:calc(100vh - 32px);overflow:auto}@media(max-width:850px){aside .panel{position:static;max-height:none}}'));
function inspect(title,obj){renderHumanDetails(title,obj)}
function matches(obj,q){return JSON.stringify(obj).toLowerCase().includes(q)}
function badge(text,ok){return element('span',text,'badge '+(ok?'good':'bad'))}
const graphPanel=element('div',undefined,'panel'),graphTitle=element('h2','语义图 · 本体层与合同投影'),graphNote=element('p','本体层（上，业务对象与谓词）与投影层（下，物理数据集）。实线=等值键，虚线=弱匹配，点线=纯语义，灰虚线=投影；节点描边=证据来源（绿粗=责任人确认，灰=数据观测，橙虚=模型推断）。点击节点聚焦邻接，双击空白复位，滚轮缩放、拖拽平移。','muted');
const svgNS='http://www.w3.org/2000/svg',graph=document.createElementNS(svgNS,'svg');
graph.setAttribute('role','img');graph.setAttribute('aria-label','本体与数据集关系图');graph.style.width='100%';graph.style.height='auto';graph.style.touchAction='none';graph.style.marginTop='6px';
const gtools=element('div');gtools.style.margin='2px 0 10px';
const zin=element('button','放大','gbtn'),zout=element('button','缩小','gbtn'),zreset=element('button','复位','gbtn'),zexp=element('button','导出 SVG','gbtn');
[zin,zout,zreset,zexp].forEach(b=>{b.style.marginRight='8px';gtools.append(b)});
const EDGE_KINDS=[['equi_key','等值键','#3f8f88'],['weak','弱匹配','#3f8f88'],['derived','推导','#3f8f88'],['semantic_only','纯语义','#3f8f88'],['projection','投影','#9fb3c1'],['contract','合同关系','#7d94b8']];
const edgeFilter={};EDGE_KINDS.forEach(k=>edgeFilter[k[0]]=true);
const efilterBar=element('div');efilterBar.style.margin='0 0 10px';
EDGE_KINDS.forEach(([kind,label,color])=>{const lab=element('label',undefined,'efchip');
 const cb=element('input');cb.type='checkbox';cb.checked=true;
 const dot=element('span',undefined,'efdot');dot.style.background=color;
 cb.addEventListener('change',()=>{edgeFilter[kind]=cb.checked;applyVisibility()});
 lab.append(cb,dot,label);efilterBar.append(lab)});
const domainBar=element('div');domainBar.style.margin='0 0 6px';
graphPanel.append(graphTitle,graphNote,gtools,efilterBar,domainBar,graph);$('semantic').before(graphPanel);
function svg(tag,attrs,text){const e=document.createElementNS(svgNS,tag);for(const [k,v] of Object.entries(attrs))e.setAttribute(k,v);if(text!==undefined)e.textContent=text;return e}
function textW(s,size){let w=0;for(const ch of String(s))w+=/[-⎿-〿㐀-鿿豈-﫿：·]/.test(ch)?size:size*0.56;return w}
const DASH={equi_key:'',weak:'7 5',derived:'12 5 3 5',semantic_only:'2 5'};
const EVIDENCE_STYLE={owner_confirmed:{stroke:'#157347',width:2.6,dash:''},user_provided:{stroke:null,width:1.5,dash:''},data_observed:{stroke:'#647d8c',width:1.6,dash:''},model_inferred:{stroke:'#e08a3c',width:1.8,dash:'5 3'}};
let vb={x:0,y:0,w:1160,h:400},focusId=null,edgePairs=[],nodeMeta={},activeDomain=null,fullH=400;
function setVB(){graph.setAttribute('viewBox',vb.x+' '+vb.y+' '+vb.w+' '+vb.h)}
zin.addEventListener('click',()=>{vb.w*=0.8;vb.h*=0.8;setVB()});
zout.addEventListener('click',()=>{vb.w*=1.25;vb.h*=1.25;setVB()});
zreset.addEventListener('click',()=>{focusId=null;activeDomain=null;drawDomainBar();drawGraph('')});
zexp.addEventListener('click',()=>{
 const clone=graph.cloneNode(true);clone.setAttribute('xmlns',svgNS);
 clone.setAttribute('viewBox','0 0 1160 '+fullH);clone.setAttribute('width','1160');clone.setAttribute('height',fullH);
 clone.setAttribute('font-family','system-ui,"Microsoft YaHei",sans-serif');
 const bg=svg('rect',{x:0,y:0,width:1160,height:fullH,fill:'#eef3f5'});clone.insertBefore(bg,clone.firstChild);
 const ta=element('textarea');ta.style.cssText='width:100%;height:160px;font:12px ui-monospace,monospace';
 ta.value='<?xml version="1.0" encoding="UTF-8"?>\n'+clone.outerHTML;
 $('detailTitle').textContent='导出 SVG · 全选复制保存为 .svg';$('detail').replaceChildren(ta);ta.select()});
graph.addEventListener('wheel',e=>{e.preventDefault();const f=e.deltaY<0?0.9:1.1;vb.w*=f;vb.h*=f;setVB()},{passive:false});
let pan=null;
graph.addEventListener('pointerdown',e=>{pan={x:e.clientX,y:e.clientY,vx:vb.x,vy:vb.y};try{graph.setPointerCapture(e.pointerId)}catch(_){}});
graph.addEventListener('pointermove',e=>{if(!pan)return;const k=vb.w/(graph.clientWidth||1160);vb.x=pan.vx-(e.clientX-pan.x)*k;vb.y=pan.vy-(e.clientY-pan.y)*k;setVB()});
graph.addEventListener('pointerup',()=>pan=null);
graph.addEventListener('dblclick',()=>{focusId=null;applyVisibility()});
function applyVisibility(){
 const q=$('search').value.toLowerCase().trim();
 const keep=new Set();
 if(focusId){keep.add(focusId);for(const p of edgePairs)if(p.a===focusId||p.b===focusId){keep.add(p.a);keep.add(p.b)}}
 for(const n of graph.querySelectorAll('[data-node]')){
  const id=n.getAttribute('data-node'),meta=nodeMeta[id]||{};
  let alpha=1;
  if(q&&!meta.matched)alpha=0.22;
  if(activeDomain&&meta.domain!==activeDomain)alpha=Math.min(alpha,0.10);
  if(focusId&&!keep.has(id))alpha=Math.min(alpha,0.18);
  n.style.opacity=alpha;
  const rect=n.querySelector('rect.card');
  if(rect&&q&&meta.matched){rect.setAttribute('stroke','#f59e0b');rect.setAttribute('stroke-width','3')}
  else if(rect&&meta.stroke){rect.setAttribute('stroke',meta.stroke);rect.setAttribute('stroke-width',meta.width)}
 }
 for(const e of graph.querySelectorAll('[data-edge]')){
  const [a,b]=e.getAttribute('data-edge').split('|'),kind=e.getAttribute('data-kind');
  let alpha=edgeFilter[kind]?1:0;
  if(alpha){const aa=nodeMeta[a]||{},bb=nodeMeta[b]||{};
   if(q&&(!aa.matched||!bb.matched))alpha=0.06;
   if(activeDomain&&(aa.domain!==activeDomain||bb.domain!==activeDomain))alpha=Math.min(alpha,0.08);
   if(focusId&&!(keep.has(a)&&keep.has(b)))alpha=Math.min(alpha,0.06)}
  e.style.opacity=alpha}
 for(const t of graph.querySelectorAll('[data-edgelabel]')){
  const [a,b]=t.getAttribute('data-edgelabel').split('|');let show=true;
  const aa=nodeMeta[a]||{},bb=nodeMeta[b]||{};
  if(q&&(!aa.matched||!bb.matched))show=false;
  if(activeDomain&&(aa.domain!==activeDomain||bb.domain!==activeDomain))show=false;
  if(focusId&&!(keep.has(a)&&keep.has(b)))show=false;
  t.style.opacity=show?1:0}
}
function drawDomainBar(){
 const domains=[...new Set(Object.values(nodeMeta).map(x=>x.domain).filter(Boolean))];
 domainBar.replaceChildren();
 if(!domains.length){domainBar.hidden=true;return}
 domainBar.hidden=false;domainBar.append(element('span','主题域：','muted'));
 const mk=(label,val)=>{const b=element('button',label,'chip'+(activeDomain===val?' on':''));
  b.addEventListener('click',()=>{activeDomain=activeDomain===val?null:val;drawDomainBar();applyVisibility()});return b};
 domainBar.append(mk('全部',null));domains.forEach(d=>domainBar.append(mk(d,d)));
}
function drawGraph(q){
 graph.replaceChildren();edgePairs=[];nodeMeta={};
 const ont=data.ontology,ents=ont?(ont.entities||[]):[],dss=(m.datasets||[]);
 const CW=270,RH=150,X0=170,eCols=Math.max(1,Math.min(4,Math.ceil(Math.sqrt(ents.length||1)))),ePos={};
 ents.forEach((e,i)=>ePos[e.name]={x:X0+(i%eCols)*CW,y:118+Math.floor(i/eCols)*RH});
 const eRows=Math.ceil(ents.length/eCols);
 const band1H=ents.length?eRows*RH+64:0;
 const band2Y=40+band1H+30;
 const dCols=Math.max(1,Math.min(4,Math.ceil(Math.sqrt(dss.length||1)))),dPos={};
 dss.forEach((d,i)=>dPos[d.name]={x:X0+(i%dCols)*CW,y:band2Y+70+Math.floor(i/dCols)*RH});
 const dRows=Math.ceil(dss.length/dCols);
 const band2H=dss.length?dRows*RH+64:0;
 const H=Math.max(band2Y+band2H+64,300);
 vb={x:0,y:0,w:1160,h:H};fullH=H;setVB();
 const defs=svg('defs',{});
 const flt=svg('filter',{id:'nshadow',x:'-30%',y:'-30%',width:'160%',height:'170%'});
 flt.append(svg('feDropShadow',{dx:0,dy:2,stdDeviation:3,'flood-color':'#0f2a35','flood-opacity':0.10}));defs.append(flt);
 const mk=(id,color)=>{const mkk=svg('marker',{id,viewBox:'0 0 10 10',refX:8.6,refY:5,markerWidth:6.6,markerHeight:6.6,orient:'auto-start-reverse'});mkk.append(svg('path',{d:'M 0 0 L 10 5 L 0 10 z',fill:color}));defs.append(mkk)};
 mk('arrowT','#3f8f88');mk('arrowB','#7d94b8');graph.append(defs);
 const band=(y,h,color,tint,label)=>{if(!h)return;
  graph.append(svg('rect',{x:22,y:y,width:1116,height:h,rx:18,fill:tint,stroke:color,'stroke-opacity':0.14,'stroke-width':1}));
  const cw=textW(label,12)+22;
  const g=svg('g',{});
  g.append(svg('rect',{x:38,y:y-13,width:cw,height:26,rx:13,fill:color}));
  g.append(svg('text',{x:38+cw/2,y:y+4,'text-anchor':'middle',fill:'#fff','font-size':12,'font-weight':600},label));
  graph.append(g)};
 band(40,band1H,'#0f7b6c','rgba(15,123,108,.055)','本体层 · 业务世界');
 band(band2Y,band2H,'#5b7aa8','rgba(91,122,168,.06)','投影层 · 物理数据');
 const label=(a,b,x,y,text)=>{const w=textW(text,11)+12;
  const g=svg('g',{'data-edgelabel':a+'|'+b});
  g.append(svg('rect',{x:x-w/2,y:y-9,width:w,height:17,rx:8.5,fill:'#fff','fill-opacity':0.92,stroke:'#dfe8ec','stroke-width':0.8}));
  g.append(svg('text',{x,y:y+3.5,fill:'#57707f','font-size':11,'text-anchor':'middle'},text));
  return g};
 const edge=(el,a,b,kind,obj,title)=>{el.setAttribute('data-edge',a+'|'+b);el.setAttribute('data-kind',kind);edgePairs.push({a,b});el.style.cursor='pointer';el.addEventListener('click',ev=>{ev.stopPropagation();inspect(title,obj)});graph.append(el)};
 if(ont)for(const r of ont.relations||[]){const a=ePos[r.from],b=ePos[r.to];if(!a||!b)continue;
  const dx=b.x-a.x,mx=(a.x+b.x)/2,my=(a.y+b.y)/2-Math.max(46,Math.abs(dx)*0.16);
  const p=svg('path',{d:`M ${a.x} ${a.y} Q ${mx} ${my} ${b.x} ${b.y}`,fill:'none',stroke:'#3f8f88','stroke-width':1.9,'stroke-dasharray':DASH[r.mapping]??'7 5','marker-end':'url(#arrowT)'});
  edge(p,'e:'+r.from,'e:'+r.to,r.mapping||'weak',r,'本体关系 · '+r.id);graph.append(label('e:'+r.from,'e:'+r.to,mx,my-2,(r.predicate||'')+(r.mapping&&r.mapping!=='equi_key'?' · '+r.mapping:'')))}
 for(const d of dss){const ref=d.ontology_ref;if(!ref||!ePos[ref])continue;const a=ePos[ref],b=dPos[d.name];
  const p=svg('path',{d:`M ${a.x} ${a.y+32} C ${a.x} ${a.y+86}, ${b.x} ${b.y-86}, ${b.x} ${b.y-32}`,fill:'none',stroke:'#9fb3c1','stroke-width':1.5,'stroke-dasharray':'3 4','stroke-linecap':'round'});
  edge(p,'e:'+ref,'d:'+d.name,'projection',{ontology_ref:ref,dataset:d.name},'投影 · '+ref+' → '+d.name)}
 for(const r of m.relationships||[]){const a=dPos[r.from],b=dPos[r.to];if(!a||!b)continue;
  const dx=Math.abs(b.x-a.x),mx=(a.x+b.x)/2,my=(a.y+b.y)/2-Math.max(24,dx*0.08);
  const p=svg('path',{d:`M ${a.x} ${a.y} Q ${mx} ${my} ${b.x} ${b.y}`,fill:'none',stroke:'#7d94b8','stroke-width':1.9,'marker-end':'url(#arrowB)'});
  edge(p,'d:'+r.from,'d:'+r.to,'contract',r,'关系 · '+(r.id||r.from+' → '+r.to));if(r.cardinality)graph.append(label('d:'+r.from,'d:'+r.to,mx,my-2,r.cardinality))}
 const node=(id,x,y,title,sub,barColor,dot,obj,kind,domain,evsrc)=>{
  const g=svg('g',{tabindex:0,role:'button','aria-label':title});g.setAttribute('data-node',id);g.style.cursor='pointer';
  const es=EVIDENCE_STYLE[evsrc]||{};
  const rStroke=es.stroke||'#ccd9e0',rWidth=es.width||1.5;
  const rect=svg('rect',{x:x-104,y:y-30,width:208,height:60,rx:12,fill:'#fff',stroke:rStroke,'stroke-width':rWidth,'class':'card',filter:'url(#nshadow)'});
  if(es.dash)rect.setAttribute('stroke-dasharray',es.dash);
  g.append(rect);
  g.append(svg('rect',{x:x-104,y:y-19,width:4,height:38,rx:2,fill:barColor}));
  if(dot)g.append(svg('circle',{cx:x+90,cy:y-16,r:6,fill:dot,stroke:'#fff','stroke-width':1.6}));
  g.append(svg('text',{x:x+4,y:y-4,'text-anchor':'middle',fill:'#15303c','font-size':14,'font-weight':600},title));
  if(sub)g.append(svg('text',{x:x+4,y:y+16,'text-anchor':'middle',fill:'#8ba2ad','font-size':11},sub));
  nodeMeta[id]={domain:domain||null,stroke:rStroke,width:rWidth,matched:!q||matches(obj,q)};
  const act=()=>{focusId=focusId===id?null:id;applyVisibility();inspect(kind+' · '+title,obj)};
  g.addEventListener('click',ev=>{ev.stopPropagation();act()});
  g.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();act()}});
  graph.append(g)};
 for(const e of ents){const p=ePos[e.name];
  node('e:'+e.name,p.x,p.y,e.cn||e.name,(e.is_a?'is_a '+e.is_a+' · ':'')+(e.attributes||[]).length+' 属性','#0f7b6c',e.projected_by.length?'#2e9e7b':(e.unprojected_reason?'#9aa7ad':'#e08a3c'),e,'本体实体',e.domain,(e.evidence||{}).source)}
 for(const d of dss){const p=dPos[d.name];
  node('d:'+d.name,p.x,p.y,d.cn||d.name,'source: '+(d.source||'待补充'),'#5b7aa8',null,d,'数据集',d.domain,(d.evidence||{}).source)}
 const ly=H-24;
 const lbar=svg('g',{});
 lbar.append(svg('rect',{x:22,y:ly-17,width:1116,height:36,rx:12,fill:'#fff',stroke:'#dfe8ec','stroke-width':1}));
 lbar.append(svg('text',{x:40,y:ly+6,fill:'#8ba2ad','font-size':11,'font-weight':600},'边类型'));
 [['等值键','#3f8f88',''],['弱匹配','#3f8f88','7 5'],['推导','#3f8f88','12 5 3 5'],['纯语义','#3f8f88','2 5'],['投影','#9fb3c1','3 4'],['合同','#7d94b8','']].forEach((it,i)=>{
  const x=96+i*86;
  lbar.append(svg('line',{x1:x,y1:ly+2,x2:x+24,y2:ly+2,stroke:it[1],'stroke-width':2,'stroke-dasharray':it[2]}));
  lbar.append(svg('text',{x:x+29,y:ly+6,fill:'#57707f','font-size':11},it[0]))});
 lbar.append(svg('text',{x:648,y:ly+6,fill:'#8ba2ad','font-size':11,'font-weight':600},'证据来源'));
 [['责任人确认','#157347',''],['用户提供','#ccd9e0',''],['数据观测','#647d8c',''],['模型推断','#e08a3c','5 3']].forEach((it,i)=>{
  const x=716+i*104;
  lbar.append(svg('rect',{x:x,y:ly-4,width:20,height:12,rx:3,fill:'#fff',stroke:it[1],'stroke-width':2,'stroke-dasharray':it[2]}));
  lbar.append(svg('text',{x:x+25,y:ly+6,fill:'#57707f','font-size':11},it[0]))});
 graph.append(lbar);drawDomainBar();applyVisibility();
}
const ontoPanel=element('div',undefined,'panel');
ontoPanel.append(element('h2','业务本体 · 声明层'),element('p','对象/属性/谓词/落地方式的声明式事实清单；系统不做推理，投影状态以标记显示。','muted'));
const ontEntities=element('div',undefined,'cards'),ontRelations=element('div'),ontRelTitle=element('h2','本体关系');
ontRelTitle.style.marginTop='24px';ontoPanel.append(ontEntities,ontRelTitle,ontRelations);
graphPanel.after(ontoPanel);
if(data.history&&data.history.length){
 const hp=element('div',undefined,'panel');
 hp.append(element('h2','质量趋势 · lint 历史'),element('p','每次 check_model --history 追加的一条记录（红=ERROR，黄=WARN）。门禁目标：ERROR 恒零、WARN 随 release 收敛。','muted'));
 const hs=document.createElementNS(svgNS,'svg');hs.style.width='100%';hs.style.height='auto';hs.setAttribute('viewBox','0 0 1160 156');
 const maxV=Math.max(1,...data.history.map(h=>Math.max(h.errors||0,h.warnings||0)));
 const base=118,top=22;
 [0,0.5,1].forEach(f=>{const y=base-(base-top)*f;
  hs.append(svg('line',{x1:44,y1:y,x2:1136,y2:y,stroke:f?'#eef3f5':'#d5e0e5','stroke-width':1}));
  hs.append(svg('text',{x:38,y:y+4,fill:'#8ba2ad','font-size':10,'text-anchor':'end'},Math.round(maxV*f)))});
 const step=Math.min(70,1060/data.history.length),bw=Math.max(10,step*0.34);
 data.history.forEach((h,i)=>{const x=56+i*step,eh=(h.errors||0)/maxV*(base-top),wh=(h.warnings||0)/maxV*(base-top);
  hs.append(svg('rect',{x,y:base-eh,width:bw,height:Math.max(eh,h.errors?2:0),rx:2,fill:'#d64541'}));
  hs.append(svg('rect',{x:x+bw+3,y:base-wh,width:bw,height:Math.max(wh,h.warnings?2:0),rx:2,fill:'#f0a03c'}));
  const t=svg('text',{x:x+bw,y:base+16,fill:'#8ba2ad','font-size':10,'text-anchor':'middle'},(h.at||'').slice(2,10));hs.append(t)});
 const hl=svg('g',{});
 hl.append(svg('rect',{x:950,y:8,width:10,height:10,rx:2,fill:'#d64541'}),svg('text',{x:965,y:17,fill:'#57707f','font-size':11},'ERROR'));
 hl.append(svg('rect',{x:1024,y:8,width:10,height:10,rx:2,fill:'#f0a03c'}),svg('text',{x:1039,y:17,fill:'#57707f','font-size':11},'WARN'));
 hs.append(hl);
 hp.append(hs);ontoPanel.after(hp);
}
function render(){const q=$('search').value.toLowerCase(), filter=$('filter').value;
 for(const id of ['datasets','relations','metrics','gaps','reports'])$(id).replaceChildren();
 let shown=0;
 const ont=data.ontology;
 ontoPanel.hidden=!ont||filter!=='all';
 ontEntities.replaceChildren();ontRelations.replaceChildren();
 if(ont){
  for(const e of ont.entities||[]){if(!matches(e,q))continue;const b=element('button',undefined,'card');
   b.append(element('h3',e.cn||e.name),element('div',(e.is_a?('is_a '+e.is_a+' · '):'')+(e.attributes||[]).length+' 个属性','muted'));
   b.append(e.projected_by.length?badge('投影 → '+e.projected_by.join('、'),true):(e.unprojected_reason?element('span','未投影（已说明）','badge'):badge('未投影（未说明）',false)));
   const EVL={owner_confirmed:'责任人确认',user_provided:'用户提供',data_observed:'数据观测',model_inferred:'模型推断'};
   const evs=(e.evidence||{}).source;if(evs)b.append(badge('证据：'+(EVL[evs]||evs),evs!=='model_inferred'));
   b.addEventListener('click',()=>inspect('本体实体 · '+e.name,e));ontEntities.append(b)}
  if(!ontEntities.children.length)ontEntities.append(element('p','无匹配本体实体。','muted'));
  for(const r of ont.relations||[]){if(!matches(r,q))continue;const row=element('div',undefined,'edge'),b=element('button',r.from+' → '+r.to+'  ·  '+(r.predicate||'?'));
   row.append(b,element('span',r.mapping||'?','badge'));
   row.append(r.projected?badge('已投影',true):(r.mapping==='equi_key'?badge('未投影',false):element('span','不投影（无键）','badge')));
   if(r.note)row.append(element('div',r.note,'muted'));
   b.addEventListener('click',()=>inspect('本体关系 · '+r.id,r));ontRelations.append(row)}
 }
 for(const d of m.datasets||[]){if(!matches(d,q))continue;shown++;const b=element('button',undefined,'card');b.append(element('h3',d.cn||d.name),element('div',d.name+' → '+(d.source||'待补充物理来源'),'muted'),element('div',d.grain||'粒度待确认'));if(d.ontology_ref)b.append(element('div','本体对象： '+d.ontology_ref,'muted'));b.addEventListener('click',()=>inspect('数据集 · '+d.name,d));$('datasets').append(b)}
 for(const r of m.relationships||[]){if(!matches(r,q))continue;const row=element('div',undefined,'edge'),b=element('button',r.from+' → '+r.to+'  ·  '+r.cardinality);b.addEventListener('click',()=>inspect('关系 · '+(r.id||r.from+' → '+r.to),r));row.append(b,element('div','键：'+JSON.stringify(r.from_columns||r.join_key||[])+' → '+JSON.stringify(r.to_columns||r.join_key||[]),'muted'));$('relations').append(row)}
 for(const metric of m.metrics||[]){if(!matches(metric,q))continue;const row=element('div',undefined,'item'),b=element('button',(metric.name||metric.id)+' · '+metric.id);b.addEventListener('click',()=>inspect('指标 · '+metric.id,metric));row.append(b);$('metrics').append(row)}
 for(const g of data.gaps){if(!matches(g,q)||(filter==='gaps'&&g.state==='confirmed'))continue;const row=element('div',undefined,'item'),b=element('button',g.question);row.append(badge(g.state,g.state==='confirmed'),b,element('div',g.object+' · '+g.owner_role,'muted'));b.addEventListener('click',()=>inspect('补齐 · '+g.id,{...g,decisions:data.decisions.filter(d=>d.gap_id===g.id)}));$('gaps').append(row)}
 if(!$('gaps').children.length)$('gaps').append(element('p',data.gaps.length?'当前筛选无缺口。':'未提供补齐会话；不能据此判断语义完整。','muted'));
 for(const r of data.reports){if(!matches(r,q))continue;const row=element('div',undefined,'item'),b=element('button',r.name),valid=!r.binding_errors.length;row.append(badge(valid?(r.report.decision||reviewStatus(r.report)):'证据失效 / 未绑定',valid&&r.report.status==='pass'),b,element('div',valid?('来源：'+reportSource(r.report)+(r.report.scope?' · 统计范围见详情':'')) :r.binding_errors.join('；'),'muted'));b.addEventListener('click',()=>inspect('证据 · '+r.name,r));$('reports').append(row)}
 if(!data.reports.length)$('reports').append(element('p','未提供验证报告；图形展示不代表数据验证通过。','muted'));
 $('semantic').hidden=filter!=='all';$('gapPanel').hidden=filter==='evidence';$('evidencePanel').hidden=filter==='gaps';
 $('counts').textContent=shown+' 个匹配数据集 · '+data.gaps.filter(g=>g.state!=='confirmed').length+' 个已登记待确认项';
 graphPanel.hidden=filter!=='all';drawGraph(q);
}
$('search').addEventListener('input',render);$('filter').addEventListener('change',render);$('footer').textContent='模型版本 '+(m.version||'未声明')+' · '+(data.fingerprint_kind||'模型文件SHA256')+' '+data.sha256+' · 本地只读快照；不代表国标符合性、运行血缘或生产验收。';render();
__REVIEW_SCRIPT__
</script></body></html>'''


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-f", "--model", required=True, help="semantic.yaml 路径（-f 与 check_model 对齐）")
    ap.add_argument("--session")
    ap.add_argument("--report", action="append", default=[])
    ap.add_argument("--history", help="check_model --history 产出的质量趋势 JSONL")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    try:
        data = build_data(args.model, args.report, args.session, args.history)
        output = Path(args.out)
        inputs = [args.model, args.session, *args.report]
        if output.resolve() in {Path(p).resolve() for p in inputs if p}:
            raise ValueError("output must not overwrite an input")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(render_html(data), encoding="utf-8")
        print(output)
        return 0
    except (ValueError, OSError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
