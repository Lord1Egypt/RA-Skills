'use strict';
const graphWorker=typeof WorkerGlobalScope!=='undefined'&&self instanceof WorkerGlobalScope;
if(graphWorker)importScripts('/vendor/elk.bundled.js');
/* Geometry only. ELK is vendored locally; no input is sent to any service. */
(function(root,factory){
  const api=factory(typeof module==='object'&&module.exports?require('./vendor/elk.bundled.js'):root.ELK);
  if(typeof module==='object'&&module.exports)module.exports=api;
  else root.SemanticGraphLayout=api;
})(typeof window==='object'?window:globalThis,function(ELK){
  const GAP=16, FONT=12, LINE=17;
  const round=v=>Math.round(v*100)/100;
  const rect=(p,n,pad=0)=>({x:p.x-pad,y:p.y-pad,width:(n.width||172)+pad*2,height:(n.height||68)+pad*2});
  const overlap=(a,b,gap=0)=>a.x<b.x+b.width+gap&&a.x+a.width+gap>b.x&&a.y<b.y+b.height+gap&&a.y+a.height+gap>b.y;
  const inside=(p,r)=>p.x>r.x+.01&&p.x<r.x+r.width-.01&&p.y>r.y+.01&&p.y<r.y+r.height-.01;
  const same=(a,b)=>Math.abs(a.x-b.x)<.01&&Math.abs(a.y-b.y)<.01;
  const textWidth=text=>Array.from(text).reduce((w,c)=>w+(/[\u0000-\u00ff]/.test(c)?7.1:12.5),0);
  function labelSize(text){
    text=String(text||'');if(!text)return null;
    const lines=[];let line='';
    for(const char of text){if(char==='\n'){lines.push(line);line='';continue;}if(line&&textWidth(line+char)>154){lines.push(line);line='';}line+=char;}
    if(line||!lines.length)lines.push(line);
    return {text,lines,width:Math.ceil(Math.max(...lines.map(textWidth)))+14,height:lines.length*LINE+8};
  }
  function simplify(points){const out=[];for(const p of points){const q={x:round(p.x),y:round(p.y)};if(out.length&&same(out.at(-1),q))continue;while(out.length>1){const a=out.at(-2),b=out.at(-1);if((Math.abs(a.x-b.x)<.01&&Math.abs(b.x-q.x)<.01)||(Math.abs(a.y-b.y)<.01&&Math.abs(b.y-q.y)<.01))out.pop();else break;}out.push(q);}return out;}
  function blockedSegment(a,b,obstacles){
    if(Math.abs(a.x-b.x)<.01)return obstacles.some(r=>a.x>r.x+.01&&a.x<r.x+r.width-.01&&Math.max(a.y,b.y)>r.y+.01&&Math.min(a.y,b.y)<r.y+r.height-.01);
    if(Math.abs(a.y-b.y)<.01)return obstacles.some(r=>a.y>r.y+.01&&a.y<r.y+r.height-.01&&Math.max(a.x,b.x)>r.x+.01&&Math.min(a.x,b.x)<r.x+r.width-.01);
    return true;
  }
  function bounds(nodes,positions,routes){
    let left=Infinity,top=Infinity,right=-Infinity,bottom=-Infinity;
    const add=(x,y,w=0,h=0)=>{left=Math.min(left,x);top=Math.min(top,y);right=Math.max(right,x+w);bottom=Math.max(bottom,y+h);};
    for(const n of nodes){const p=positions[n.id];if(p)add(p.x,p.y,n.width||172,n.height||68);}
    for(const r of Object.values(routes)){for(const p of r.points)add(p.x,p.y);if(r.label)add(r.label.x,r.label.y,r.label.width,r.label.height);}
    if(!Number.isFinite(left))return {left:0,top:0,right:1,bottom:1};
    return {left:round(Math.min(0,left-24)),top:round(Math.min(0,top-24)),right:round(right+24),bottom:round(bottom+24)};
  }
  function segments(points){return points.slice(1).map((p,i)=>[points[i],p]);}
  function lineRectHits(a,b,r){return blockedSegment(a,b,[r]);}
  function chooseLabels(nodes,edges,positions,routes){
    const boxes=nodes.map(n=>rect(positions[n.id],n,7)),used=[];
    const allLines=Object.entries(routes).flatMap(([id,r])=>segments(r.points).map(s=>({id,s})));
    for(const e of edges){
      const r=routes[e.id],size=labelSize(e.label);if(!r||!size){if(r)r.label=null;continue;}
      const candidates=[];
      if(r.label)candidates.push({...size,x:r.label.x,y:r.label.y,preferred:true});
      for(const [a,b] of segments(r.points)){
        const horizontal=Math.abs(a.y-b.y)<.01,length=Math.abs(a.x-b.x)+Math.abs(a.y-b.y);
        if(horizontal&&length<size.width+8)continue;if(!horizontal&&length<size.height+8)continue;
        for(const t of [.5,.3,.7,.15,.85]){
          const x=a.x+(b.x-a.x)*t,y=a.y+(b.y-a.y)*t;
          if(horizontal){for(const side of [-1,1])candidates.push({...size,x:x-size.width/2,y:side<0?y-size.height-5:y+5});}
          else{for(const side of [-1,1])candidates.push({...size,x:side<0?x-size.width-7:x+7,y:y-size.height/2});}
        }
      }
      let best=null,bestScore=Infinity;
      for(const c of candidates){
        if(c.x<4||c.y<4||boxes.some(b=>overlap(c,b))||used.some(b=>overlap(c,b,5)))continue;
        const crossings=allLines.filter(l=>l.id!==e.id&&lineRectHits(l.s[0],l.s[1],c)).length;
        const score=crossings*400+(c.preferred?-20:0)+Math.abs(c.x-r.points[Math.floor(r.points.length/2)].x)*.002;
        if(score<bestScore){best=c;bestScore=score;}
      }
      // A small free-space nudge prevents a white label background from hiding
      // a crossing dependency line. Keep the original relation identifiable.
      if(best&&bestScore>=380){
        const original={...best};let clear=null;
        for(const distance of [6,12,18,24,36,48]){
          for(const [dx,dy] of [[0,-distance],[0,distance],[-distance,0],[distance,0],[-distance,-distance],[distance,distance]]){
            const c={...size,x:original.x+dx,y:original.y+dy};
            if(c.x<4||c.y<4||boxes.some(b=>overlap(c,b))||used.some(b=>overlap(c,b,5))||allLines.some(l=>l.id!==e.id&&lineRectHits(l.s[0],l.s[1],c)))continue;
            clear=c;break;
          }
          if(clear)break;
        }
        if(clear)best=clear;
      }
      if(!best){
        const bound=bounds(nodes,positions,routes),anchor=r.points[Math.floor(r.points.length/2)];
        for(let ring=0;!best&&ring<100;ring++){
          for(const side of [1,-1]){
            const c={...size,x:Math.max(4,anchor.x-size.width/2+side*ring*24),y:Math.max(4,anchor.y-size.height-10-ring*22)};
            if(!boxes.some(b=>overlap(c,b))&&!used.some(b=>overlap(c,b,5))){best=c;break;}
          }
        }
        if(!best)best={...size,x:bound.right+8,y:Math.max(4,anchor.y)};
        const center={x:best.x+best.width/2,y:best.y+best.height/2};
        best.leader=[anchor,center];
      }
      delete best.preferred;r.label=best;used.push(best);
    }
  }
  function port(p,n,side,offset=0){
    const w=n.width||172,h=n.height||68,cx=p.x+w/2,cy=p.y+h/2;
    if(side==='L')return [{x:p.x,y:cy+offset},{x:p.x-GAP,y:cy+offset}];
    if(side==='R')return [{x:p.x+w,y:cy+offset},{x:p.x+w+GAP,y:cy+offset}];
    if(side==='T')return [{x:cx+offset,y:p.y},{x:cx+offset,y:p.y-GAP}];
    return [{x:cx+offset,y:p.y+h},{x:cx+offset,y:p.y+h+GAP}];
  }
  class Heap{
    constructor(){this.a=[];}push(v){const a=this.a;let i=a.length;a.push(v);while(i){const j=(i-1)>>1;if(a[j].f<=v.f)break;a[i]=a[j];i=j;}a[i]=v;}
    pop(){const a=this.a,r=a[0],v=a.pop();if(a.length){let i=0;while(i*2+1<a.length){let j=i*2+1;if(j+1<a.length&&a[j+1].f<a[j].f)j++;if(a[j].f>=v.f)break;a[i]=a[j];i=j;}a[i]=v;}return r;}
    get length(){return this.a.length;}
  }
  function findPath(start,end,obstacles,extraLines=[]){
    const xs=[start.x,end.x],ys=[start.y,end.y];
    for(const r of obstacles){xs.push(r.x,r.x+r.width);ys.push(r.y,r.y+r.height);}
    xs.push(Math.min(...xs)-36,Math.max(...xs)+36);ys.push(Math.min(...ys)-36,Math.max(...ys)+36);
    const X=[...new Set(xs.map(round))].sort((a,b)=>a-b),Y=[...new Set(ys.map(round))].sort((a,b)=>a-b),w=X.length;
    const sx=X.indexOf(round(start.x)),sy=Y.indexOf(round(start.y)),ex=X.indexOf(round(end.x)),ey=Y.indexOf(round(end.y));
    const blocked=new Set();for(let y=0;y<Y.length;y++)for(let x=0;x<w;x++)if(obstacles.some(r=>inside({x:X[x],y:Y[y]},r)))blocked.add(y*w+x);
    const at=(x,y)=>({x:X[x],y:Y[y]}),key=(x,y,d)=>(y*w+x)*3+d;
    const q=new Heap(),cost=new Map(),previous=new Map();let target=null;
    q.push({x:sx,y:sy,d:0,g:0,f:0,k:key(sx,sy,0)});cost.set(key(sx,sy,0),0);
    while(q.length){const a=q.pop();if(a.g!==cost.get(a.k))continue;if(a.x===ex&&a.y===ey){target=a;break;}
      for(const [dx,dy,d] of [[1,0,1],[-1,0,1],[0,1,2],[0,-1,2]]){
        const nx=a.x+dx,ny=a.y+dy;if(nx<0||ny<0||nx>=w||ny>=Y.length||blocked.has(ny*w+nx))continue;
        const p=at(a.x,a.y),r=at(nx,ny);if(blockedSegment(p,r,obstacles))continue;
        let cross=0,shared=0;for(const [c,b] of extraLines){if(d===1&&Math.abs(c.x-b.x)<.01&&c.x>Math.min(p.x,r.x)&&c.x<Math.max(p.x,r.x)&&p.y>Math.min(c.y,b.y)&&p.y<Math.max(c.y,b.y))cross++;else if(d===2&&Math.abs(c.y-b.y)<.01&&c.y>Math.min(p.y,r.y)&&c.y<Math.max(p.y,r.y)&&p.x>Math.min(c.x,b.x)&&p.x<Math.max(c.x,b.x))cross++;else if(d===1&&Math.abs(c.y-b.y)<.01&&Math.abs(c.y-p.y)<6)shared+=Math.max(0,Math.min(Math.max(p.x,r.x),Math.max(c.x,b.x))-Math.max(Math.min(p.x,r.x),Math.min(c.x,b.x)));else if(d===2&&Math.abs(c.x-b.x)<.01&&Math.abs(c.x-p.x)<6)shared+=Math.max(0,Math.min(Math.max(p.y,r.y),Math.max(c.y,b.y))-Math.max(Math.min(p.y,r.y),Math.min(c.y,b.y)));}
        const g=a.g+Math.abs(p.x-r.x)+Math.abs(p.y-r.y)+(a.d&&a.d!==d?28:0)+cross*70+shared*4,k=key(nx,ny,d);
        if(g>=(cost.get(k)??Infinity))continue;cost.set(k,g);previous.set(k,a);q.push({x:nx,y:ny,d,g,k,f:g+Math.abs(X[nx]-end.x)+Math.abs(Y[ny]-end.y)});
      }
    }
    if(!target)return null;const path=[];while(target){path.push(at(target.x,target.y));target=previous.get(target.k);}return simplify(path.reverse());
  }
  function route({nodes=[],edges=[],positions={}}){
    const byId=new Map(nodes.map(n=>[n.id,n])),routes=Object.create(null),lines=[],obstacles=nodes.map(n=>rect(positions[n.id],n,12));
    const portUses=new Map();
    for(const e of edges){const a=byId.get(e.from),b=byId.get(e.to);if(!a||!b)continue;
      const pa=positions[a.id],pb=positions[b.id];if(!pa||!pb)continue;
      const dx=pb.x-pa.x,dy=pb.y-pa.y;
      const horizontal=Math.abs(dx)/(a.width||172)>=Math.abs(dy)/(a.height||68);
      const preferred=a.id===b.id?[['R','T']]:horizontal?[[dx>=0?'R':'L',dx>=0?'L':'R'],[dy>=0?'B':'T',dy>=0?'T':'B']]:[[dy>=0?'B':'T',dy>=0?'T':'B'],[dx>=0?'R':'L',dx>=0?'L':'R']];
      preferred.push(['R','R'],['L','L'],['T','T'],['B','B']);let best=null,score=Infinity;
      for(const [s,t] of preferred){
        const slot=(id,side)=>{const use=portUses.get(id+':'+side)||0;return use===0?0:(use%2?1:-1)*Math.ceil(use/2)*9;};
        const as=slot(a.id,s),bs=slot(b.id,t),[start,out]=port(pa,a,s,Math.max(-22,Math.min(22,as))),[end,into]=port(pb,b,t,Math.max(-22,Math.min(22,bs)));
        const path=findPath(out,into,obstacles,lines);if(!path)continue;
        const points=simplify([start,...path,end]);
        if(segments(points).some(([p,q])=>blockedSegment(p,q,nodes.filter(n=>n.id!==a.id&&n.id!==b.id).map(n=>rect(positions[n.id],n,2)))))continue;
        const len=segments(points).reduce((v,[p,q])=>v+Math.abs(p.x-q.x)+Math.abs(p.y-q.y),0)+points.length*25;
        if(len<score){score=len;best={points,s,t};}
      }
      if(!best)throw Error('无法在当前固定节点之间布置关系：'+(e.label||e.id)+'；请移动重叠节点或重新自动布局。');
      routes[e.id]={points:best.points,label:null};lines.push(...segments(best.points));
      portUses.set(a.id+':'+best.s,(portUses.get(a.id+':'+best.s)||0)+1);portUses.set(b.id+':'+best.t,(portUses.get(b.id+':'+best.t)||0)+1);
    }
    chooseLabels(nodes,edges,positions,routes);return {positions,routes,bounds:bounds(nodes,positions,routes)};
  }
  // A long directional chain can waste most of a wide canvas. Keep ELK as the
  // first candidate, then compare an aspect-aware compact placement. Its slot
  // assignment minimizes actual graph distances and crossings, not input order.
  function compactPositions(nodes,edges,width,height,seedPositions,packing={}){
    const nodeWidth=Math.max(...nodes.map(n=>n.width||172)),nodeHeight=Math.max(...nodes.map(n=>n.height||68));
    const stepX=nodeWidth+(packing.gapX??104),stepY=nodeHeight+(packing.gapY??86);
    const cols=packing.columns||Math.max(2,Math.min(nodes.length,Math.round(Math.sqrt(nodes.length*(width/height)*(stepY/stepX)))));
    const rows=Math.ceil(nodes.length/cols),slots=[];
    for(let y=0;y<rows;y++)for(let x=0;x<cols;x++)slots.push({x:40+x*stepX,y:40+y*stepY});
    const ids=nodes.map(n=>n.id),index=new Map(ids.map((id,i)=>[id,i]));
    const edgePairs=edges.map(e=>[index.get(e.from),index.get(e.to),e.reference?.4:1]);
    const ordered=nodes.slice().sort((a,b)=>(seedPositions[a.id].y-seedPositions[b.id].y)||seedPositions[a.id].x-seedPositions[b.id].x);
    const assignment=ids.map(id=>ordered.findIndex(n=>n.id===id));
    const crossing=(a,b,c,d)=>{const cross=(p,q,r)=>(q.x-p.x)*(r.y-p.y)-(q.y-p.y)*(r.x-p.x);return cross(a,b,c)*cross(a,b,d)<0&&cross(c,d,a)*cross(c,d,b)<0;};
    const score=()=>{
      let value=0;
      for(const [a,b,weight] of edgePairs){const p=slots[assignment[a]],q=slots[assignment[b]];const dx=(p.x-q.x)/stepX,dy=(p.y-q.y)/stepY;value+=(dx*dx+dy*dy)*weight;}
      for(let i=0;i<edgePairs.length;i++)for(let j=i+1;j<edgePairs.length;j++){
        const [a,b,wa]=edgePairs[i],[c,d,wb]=edgePairs[j];if(new Set([a,b,c,d]).size<4)continue;
        if(crossing(slots[assignment[a]],slots[assignment[b]],slots[assignment[c]],slots[assignment[d]]))value+=9*wa*wb;
      }
      return value;
    };
    let state=1234567,random=()=>{state=(Math.imul(state,1664525)+1013904223)>>>0;return state/4294967296;};
    let current=score(),best=current,bestAssignment=assignment.slice();const iterations=Math.min(6500,900+nodes.length*110);
    for(let k=0;k<iterations;k++){
      const a=Math.floor(random()*nodes.length),b=Math.floor(random()*slots.length),other=assignment.indexOf(b),old=assignment[a];if(old===b)continue;
      assignment[a]=b;if(other>=0)assignment[other]=old;
      const value=score(),temp=3*(1-k/iterations);
      if(value<current||random()<Math.exp((current-value)/Math.max(.02,temp))){current=value;if(value<best){best=value;bestAssignment=assignment.slice();}}
      else{assignment[a]=old;if(other>=0)assignment[other]=b;}
    }
    const out=Object.create(null);ids.forEach((id,i)=>out[id]={...slots[bestAssignment[i]]});return out;
  }
  function crossingCount(edges,routes){
    let count=0;
    for(let i=0;i<edges.length;i++)for(let j=i+1;j<edges.length;j++){
      const e=edges[i],f=edges[j];if(new Set([e.from,e.to,f.from,f.to]).size<4)continue;
      for(const [a,b] of segments(routes[e.id]?.points||[]))for(const [c,d] of segments(routes[f.id]?.points||[])){
        const cross=(p,q,r)=>(q.x-p.x)*(r.y-p.y)-(q.y-p.y)*(r.x-p.x);
        if(cross(a,b,c)*cross(a,b,d)<0&&cross(c,d,a)*cross(c,d,b)<0)count++;
      }
    }
    return count;
  }
  let elk=null;
  async function candidate(nodes,edges,direction){
    if(!ELK)throw Error('本地图布局组件未加载，请刷新后重试。');if(!elk)elk=new ELK();
    const graph={id:'root',layoutOptions:{'elk.algorithm':'layered','elk.direction':direction,'elk.edgeRouting':'ORTHOGONAL','elk.padding':'[top=36,left=36,bottom=36,right=36]','elk.spacing.nodeNode':'40','elk.spacing.edgeNode':'18','elk.spacing.edgeEdge':'14','elk.layered.spacing.nodeNodeBetweenLayers':'70','elk.layered.spacing.edgeNodeBetweenLayers':'16','elk.layered.spacing.edgeEdgeBetweenLayers':'16','elk.layered.crossingMinimization.strategy':'LAYER_SWEEP','elk.layered.nodePlacement.strategy':'BRANDES_KOEPF','elk.layered.nodePlacement.bk.fixedAlignment':'BALANCED','elk.layered.mergeEdges':'false','elk.separateConnectedComponents':'true','elk.spacing.componentComponent':'48','elk.aspectRatio':'1.7','elk.randomSeed':'1'},children:nodes.map(n=>({id:n.id,width:n.width||172,height:n.height||68})),edges:edges.map(e=>{const l=labelSize(e.label);return {id:e.id,sources:[e.from],targets:[e.to],...(l?{labels:[{id:e.id+':label',text:e.label,width:l.width,height:l.height}]}:{})};})};
    const out=await elk.layout(graph),positions=Object.create(null),routes=Object.create(null);
    for(const n of out.children)positions[n.id]={x:round(n.x),y:round(n.y)};
    for(const e of out.edges||[]){const sect=e.sections?.[0];if(!sect)continue;const label=e.labels?.[0];routes[e.id]={points:simplify([sect.startPoint,...(sect.bendPoints||[]),sect.endPoint]),label:label?{...labelSize(edges.find(x=>x.id===e.id).label),x:round(label.x),y:round(label.y)}:null};}
    chooseLabels(nodes,edges,positions,routes);return {positions,routes,bounds:bounds(nodes,positions,routes),direction};
  }
  async function layout({nodes=[],edges=[],width=1000,height=620,positions={},fixed=[]}){
    const ids=new Set(nodes.map(n=>n.id));edges=edges.filter(e=>ids.has(e.from)&&ids.has(e.to));
    if(!nodes.length)return {positions:{},routes:{},bounds:{left:0,top:0,right:1,bottom:1}};
    const variants=[];for(const direction of ['RIGHT','DOWN'])variants.push(await candidate(nodes,edges,direction));
    const score=g=>Math.min(width/(g.bounds.right-g.bounds.left),height/(g.bounds.bottom-g.bounds.top));
    variants.sort((a,b)=>score(b)-score(a));let chosen=variants[0];
    if(nodes.length<=40&&score(chosen)<.9){
      const seed=chosen.positions;
      // Prioritize readable scale; reject a compact view when its crossings
      // overwhelm the gain. The detailed routing still avoids node interiors.
      const quality=g=>score(g)/(1+crossingCount(edges,g.routes)*.018);
      const packings=[{}];
      if(nodes.length>16){
        const wide=Math.max(3,Math.ceil(Math.sqrt(nodes.length*(width/height)*.6)));
        packings.push({columns:wide,gapX:88,gapY:67},{columns:wide+1,gapX:88,gapY:67});
      }
      for(const packing of packings){
        const compact=route({nodes,edges,positions:compactPositions(nodes,edges,width,height,seed,packing)});
        if(quality(compact)>quality(chosen))chosen={...compact,direction:'COMPACT'};
      }
    }
    const pinned=new Set(fixed.filter(id=>ids.has(id)&&positions[id]));
    if(pinned.size){
      const result={...chosen.positions};for(const id of pinned)result[id]={...positions[id]};
      const occupied=nodes.filter(n=>pinned.has(n.id)).map(n=>rect(result[n.id],n,16));
      for(const n of nodes.filter(n=>!pinned.has(n.id))){let p={...result[n.id]},found=false;const origin={...p};for(let ring=0;!found&&ring<300;ring++){for(const [dx,dy] of [[ring*32,0],[0,ring*32],[-ring*32,0],[0,-ring*32]]){const q={x:Math.max(24,origin.x+dx),y:Math.max(24,origin.y+dy)};if(!occupied.some(b=>overlap(rect(q,n,8),b))){p=q;found=true;break;}}}if(!found)throw Error('固定位置附近没有足够空间，请解除固定后重试');result[n.id]=p;occupied.push(rect(p,n,16));}
      chosen=route({nodes,edges,positions:result});
    }
    return chosen;
  }
  // The temporary overview uses straight edges until the worker finishes detailed routing.
  function overview({nodes,edges,positions}){
    const sizes=new Map(nodes.map(n=>[n.id,n])),routes=Object.create(null);
    for(const edge of edges){
      const from=positions[edge.from],to=positions[edge.to];
      const source=sizes.get(edge.from),target=sizes.get(edge.to);
      const start={x:from.x+source.width,y:from.y+source.height/2},end={x:to.x,y:to.y+target.height/2};
      const label=labelSize(edge.label);
      if(label){label.x=(start.x+end.x-label.width)/2;label.y=(start.y+end.y-label.height)/2;}
      routes[edge.id]={points:[start,end],label};
    }
    return {positions,routes,bounds:bounds(nodes,positions,routes)};
  }
  return {layout,route,overview,labelSize};
});
if(graphWorker)self.onmessage=async({data})=>{
  try{const plan=await self.SemanticGraphLayout[data.routeOnly?'route':'layout'](data.input);self.postMessage({plan});}
  catch(error){self.postMessage({error:error.message});}
};
