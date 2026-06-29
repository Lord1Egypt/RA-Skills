#!/usr/bin/env node
import{spawnSync as S}from"node:child_process";import{parseArgs as E,printOrWrite as T,readText as C,snap as h,writeText as N,xmlEscape as i}from"./studio-core.mjs";const m=140,x=64,v="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;",D="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;",$=[["#dae8fc","#6c8ebf"],["#d5e8d4","#82b366"],["#ffe6cc","#d79b00"],["#e1d5e7","#9673a6"],["#fff2cc","#d6b656"],["#f8cecc","#b85450"]];function G(e){const n=[`digraph G { rankdir=${String(e.direction??"TB").toUpperCase()==="LR"?"LR":"TB"}; splines=ortho; node [shape=box fixedsize=true];`];for(const r of e.nodes)n.push(`"${u(r.id)}" [width=${Number(r.width??m)/72} height=${Number(r.height??x)/72}];`);for(const r of e.edges??[])n.push(`"${u(r.source)}" -> "${u(r.target)}";`);return n.push("}"),n.join(`
`)}function L(e){const t=S("dot",["-Tplain"],{input:e,encoding:"utf8"});if(t.error?.code==="ENOENT")throw new Error("Graphviz `dot` not found on PATH");if(t.status!==0)throw new Error(`Graphviz failed: ${t.stderr.trim()}`);const n=new Map;let r=0;for(const d of t.stdout.split(/\r?\n/)){const s=O(d);s[0]==="graph"&&(r=Number(s[3])),s[0]==="node"&&n.set(s[1],{x:Number(s[2]),y:Number(s[3])})}return{height:r,pos:n}}function A(e,t){const n=[...new Set((e.nodes??[]).map(o=>o.group).filter(Boolean))],r=o=>$[Math.max(0,n.indexOf(o))%$.length],d=[],s={nodes:{},edges:e.edges??[]};for(const o of e.nodes??[]){const a=t.pos.get(o.id);if(!a)continue;const c=Number(o.width??m),p=Number(o.height??x),g=h(a.x*72-c/2+40),f=h((t.height-a.y)*72-p/2+40),b=o.style??(o.group?j(r(o.group)):v);s.nodes[o.id]={x:g,y:f,width:c,height:p,group:o.group??null},d.push(`        <mxCell id="${i(o.id)}" value="${i(o.label??o.id)}" style="${i(b)}" vertex="1" parent="1">
          <mxGeometry x="${g}" y="${f}" width="${c}" height="${p}" as="geometry"/>
        </mxCell>`)}let y=0;for(const o of e.edges??[])d.push(`        <mxCell id="edge_${y++}" value="${i(o.label??"")}" style="${D}" edge="1" parent="1" source="${i(o.source)}" target="${i(o.target)}">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>`);return{manifest:s,xml:`<mxfile host="drawio">
  <diagram name="Page-1">
    <mxGraphModel grid="1" gridSize="10" page="1" pageWidth="1100" pageHeight="850">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
${d.join(`
`)}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
`}}function j([e,t]){return`rounded=1;whiteSpace=wrap;html=1;fillColor=${e};strokeColor=${t};`}function u(e){return String(e).replaceAll("\\","\\\\").replaceAll('"','\\"')}function O(e){return e.match(/"[^"]*"|\S+/g)?.map(t=>t.replace(/^"|"$/g,""))??[]}const l=E(process.argv.slice(2)),w=l._[0];w||(console.error("usage: node layout-graph.mjs graph.json --output diagram.drawio [--manifest layout.json]"),process.exit(2));try{const e=JSON.parse(C(w)),t=A(e,L(G(e)));T(t.xml,l.output),l.manifest&&N(l.manifest,`${JSON.stringify(t.manifest,null,2)}
`),l.output||process.stderr.write(`rendered ${e.nodes.length} nodes
`)}catch(e){console.error(`error: ${e.message}`),process.exit(1)}export{G as buildDot,A as graphToDrawio,L as runDot};
