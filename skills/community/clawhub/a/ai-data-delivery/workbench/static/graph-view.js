(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const params = new URLSearchParams(location.search);
  const snapshot = $('snapshot') ? JSON.parse($('snapshot').textContent) : null;
  const lang = snapshot?.language || params.get('lang') || 'en';
  const t = (zh, en) => lang === 'zh' ? zh : en;
  const names = {relation:t('关系','Relationship'), mapping:t('映射','Mapping'), entity:t('业务对象','Object'), term:t('术语','Term'), attribute:t('属性','Attribute'),
    field:t('字段','Column'), dataset:t('表','Dataset'), rule:t('规则','Rule'), metric:t('指标','Metric')};
  const statuses = {draft:t('草稿','Draft'), confirmed:t('已确认','Confirmed'), needs_review:t('待核对','Needs review')};
  const colors = {entity:'#45967a', term:'#9b78bd', attribute:'#64a09a', field:'#7898ad',
    dataset:'#527fae', metric:'#bc8b33', rule:'#9870ad'};
  let data, graph, selected, nodes, adjacent, labels = [], busy = false;
  let sameNames, sameDomainNames, pageIndex = 0, frameDistance = 0;
  const pageSize = 20;
  const stage = $('stage');
  const width = () => stage.clientWidth, height = () => stage.clientHeight;
  document.documentElement.lang = lang;
  $('heading').textContent = t('3D 关系图','3D connections');
  $('choose').textContent = t('选择对象','Select an object');
  $('relations-heading').textContent = t('直接关系','Direct connections');
  $('editor').textContent = t('在 2D 编辑器查看','View in 2D editor');
  $('near').textContent = t('只看这个对象的直接关系','Show this neighborhood');
  $('expand').textContent = t('展开全部直接邻居','Show all direct neighbors');
  $('find').placeholder = t('搜索对象、关系或业务域','Search objects, links or domains');
  $('find').setAttribute('aria-label',$('find').placeholder);
  $('previous').textContent=t('上一页','Previous');
  $('next').textContent=t('下一页','Next');
  $('find').oninput=()=>{pageIndex=0;showConnections();};
  $('previous').onclick=()=>{pageIndex--;showConnections();};
  $('next').onclick=()=>{pageIndex++;showConnections();};
  function neighborhood(id, all){
    if(!snapshot){
      const url=new URL(location.href);
      if(all)url.searchParams.set('scope','neighbors');else url.searchParams.delete('scope');
      url.searchParams.set('focus',id);
      location.assign(url);return;
    }
    if(!snapshot.data.full)return;
    const ids=new Set([id]);
    for(const edge of snapshot.data.edges){
      if(edge.source===id)ids.add(edge.target);
      if(edge.target===id)ids.add(edge.source);
    }
    const visible=all?ids:new Set([...ids].slice(0,80));
    render({...snapshot.data,full:false,center:id,focus:id,eligible:ids.size,changeRevision:null,
      nodes:snapshot.data.nodes.filter(n=>visible.has(n.id)),
      edges:snapshot.data.edges.filter(e=>visible.has(e.source)&&visible.has(e.target))});
  }
  $('near').onclick=()=>neighborhood(selected,false);
  $('expand').onclick=()=>neighborhood(data.focus,true);
  $('objects').onchange = () => select($('objects').value);
  function labelFor(e) {
    if (e.kind === 'owner') return t('所属表','Belongs to table');
    if (e.kind === 'from') return t('关系起点','Source endpoint');
    if (e.kind === 'to') return t('关系终点','Target endpoint');
    if (e.kind === 'ref') return t('引用','References');
    return e.label;
  }
  function place(list, edges, center, full) {
    if (list.length <= 18) {
      const owners = new Map(edges.filter(e=>e.kind==='owner').map(e=>[e.source,e.target]));
      const rest = list.filter(n => n.id !== center);
      if(full)rest.sort((a,b)=>(owners.get(a.id)||a.id).localeCompare(owners.get(b.id)||b.id) || a.id.localeCompare(b.id));
      rest.forEach((n,i) => {const a = 2*Math.PI*i/rest.length;
        Object.assign(n,{fx:225*Math.cos(a), fy:151*Math.sin(a), fz:50*Math.sin(2*a+.3)});});
      const root = list.find(n=>n.id===center);
      if(root) Object.assign(root,{fx:0,fy:0,fz:0});
      return;
    }
    const owners = new Map(edges.filter(e=>e.kind==='owner').map(e=>[e.source,e.target]));
    const groups = new Map();
    for(const n of list){const key=owners.get(n.id)||n.id;
      if(!groups.has(key))groups.set(key,[]); groups.get(key).push(n);}
    let i=0;
    for(const key of [...groups.keys()].sort()){
      const z=1-2*(i+.5)/groups.size, a=2.399963*i++, r=320*Math.sqrt(1-z*z);
      for(const n of groups.get(key)){
        let h=2166136261;
        for(const c of n.id)h=Math.imul(h^c.charCodeAt(0),16777619);
        const offset=k=>n.id===key?0:(((h>>>k)&255)/255-.5)*(list.length<=100?110:34);
        Object.assign(n,{fx:r*Math.cos(a)+offset(0),fy:r*Math.sin(a)+offset(8),fz:215*z+offset(16)});
      }
    }
  }
  function positionLabels(){
    if(!graph)return;
    const used=[], w=width(), h=height(), hintTop=$('hint').offsetTop;
    for(const label of labels){
      const {n,span,line}=label;
      const p=graph.graph2ScreenCoords(n.fx,n.fy,n.fz);
      const x=Math.round(p.x), y=Math.round(p.y), anchorY=y+9;
      const boxWidth=label.w, boxHeight=label.h;
      const maxY=(hintTop>h/2?hintTop:h)-boxHeight-4;
      let best;
      if(x>=0&&x<=w&&y>=0&&y<=h&&maxY>=4){
        const step=boxHeight+4, side=boxWidth/2+10;
        for(const [dx,dy] of [[0,0],[0,-step-10],[side,-step/2],[-side,-step/2],[0,step],[0,-2*step],[side,step],[-side,step],[side,-2*step],[-side,-2*step],[0,2*step],[0,-3*step],[side,2*step],[-side,2*step]]){
          const left=Math.round(Math.max(4,Math.min(w-boxWidth-4,x-boxWidth/2+dx)));
          const top=Math.round(Math.max(4,Math.min(maxY,anchorY+dy)));
          const rect={left,top,right:left+boxWidth,bottom:top+boxHeight};
          if(!used.some(r=>rect.left<r.right+3&&rect.right+3>r.left&&rect.top<r.bottom+2&&rect.bottom+2>r.top)){
            best=rect;break;
          }
        }
      }
      span.hidden=!best;line.style.display='none';
      if(!best)continue;
      used.push(best);
      span.style.transform='translate('+x+'px,'+anchorY+'px) translateX(-50%)';
      span.style.marginLeft=Math.round(best.left+boxWidth/2-x)+'px';
      span.style.marginTop=(best.top-anchorY)+'px';
      const endX=Math.max(best.left,Math.min(x,best.right));
      const endY=Math.max(best.top,Math.min(y,best.bottom));
      if(Math.hypot(endX-x,endY-y)>16){
        line.setAttribute('x1',x);line.setAttribute('y1',y);line.setAttribute('x2',endX);line.setAttribute('y2',endY);
        line.style.display='';
      }
    }
  }
  function trackCamera(){
    // Orbit damping and the first resize can finish after the input event.
    // Update screen-space labels against the matrices actually used for drawing.
    const previous = new Float64Array(32);
    function frame(){
      const camera = graph.camera();
      const world = camera.matrixWorld.elements, projection = camera.projectionMatrix.elements;
      let changed = false;
      for(let i=0;i<16;i++){
        if(previous[i]!==world[i] || previous[i+16]!==projection[i]) changed=true;
        previous[i]=world[i]; previous[i+16]=projection[i];
      }
      if(changed)positionLabels();
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }
  function displayName(n){
    if(!sameNames.has(n.label))return n.label;
    const qualifier=[n.domain,(!n.domain||sameDomainNames.has(JSON.stringify([n.label,n.domain])))?n.id:null].filter(Boolean);
    return n.label+' · '+qualifier.join(' · ');
  }
  function entry(dl,title,value){
    if(!value || (Array.isArray(value)&&!value.length))return;
    const dt=document.createElement('dt'),dd=document.createElement('dd');
    dt.textContent=title;
    if(Array.isArray(value)){
      for(const text of value){const p=document.createElement('p');p.textContent=text;dd.append(p);}
    }else dd.textContent=value;
    dl.append(dt,dd);
  }
  function showMeaning(dl,a,foldSource=false){
    entry(dl,t('业务域','Domain'),a.domain);
    entry(dl,t('业务定义','Definition'),a.definition);
    entry(dl,t('适用范围','Scope'),a.scopeText);
    entry(dl,t('粒度','Grain'),a.grain);
    entry(dl,t('包含','Includes'),a.inclusions);
    entry(dl,t('不含','Excludes'),a.exclusions);
    const evidence=(a.evidence||[]).map(e=>{
      const source=[e.source_id,e.revision!=null?'r'+e.revision:null,e.fragment_id].filter(Boolean).join(' · ');
      return [e.quote,source||e.type].filter(Boolean).join(' — ');
    }).filter(Boolean);
    entry(dl,t('待核实','Open questions'),a.gaps);
    let sources=dl;
    if(foldSource){
      const dt=document.createElement('dt'),dd=document.createElement('dd');
      const details=document.createElement('details'),summary=document.createElement('summary');
      dt.className='visually-hidden';
      dt.textContent=t('来源详情','Source details');
      summary.textContent=evidence.length?t('查看依据与标识','Show evidence and ID')+' · '+evidence.length:t('查看标识','Show ID');
      sources=document.createElement('dl');
      details.append(summary,sources);dd.append(details);dl.append(dt,dd);
    }
    entry(sources,t('依据','Evidence'),evidence);
    entry(sources,t('标识','ID'),a.id);
  }
  function showConnections(){
    const list=$('relations'),neighbors=adjacent.get(selected)||[],query=$('find').value.trim().toLocaleLowerCase();
    const matches=query?neighbors.filter(([e,id])=>{
      const n=nodes.get(id);
      return [n.label,n.domain,n.id,labelFor(e),e.domain,e.id].some(v=>v&&String(v).toLocaleLowerCase().includes(query));
    }):neighbors;
    const start=pageIndex*pageSize, end=Math.min(start+pageSize,matches.length);
    list.replaceChildren();
    for(const [e,other,out] of matches.slice(start,end)){
      const item=document.createElement('li'),button=document.createElement('button');
      button.textContent=(out?'→ ':'← ')+labelFor(e)+' · '+displayName(nodes.get(other))+
        (e.status?' · '+(statuses[e.status]||e.status):'')+(e.changed?' · '+t('已改动','Changed'):'');
      button.onclick=()=>select(other);item.append(button);
      if(e.kind==='relation'||e.kind==='mapping'){
        const detail=document.createElement('details'),summary=document.createElement('summary'),dl=document.createElement('dl');
        summary.textContent=t('查看关系依据','Inspect this link');
        showMeaning(dl,e);detail.append(summary,dl);item.append(detail);
      }
      list.append(item);
    }
    $('pages').hidden=matches.length<=pageSize;
    $('previous').disabled=!pageIndex;
    $('next').disabled=end>=matches.length;
    $('find').hidden=!neighbors.length;
    $('overflow').textContent=!neighbors.length?t('当前视图没有直接连线。','No direct connections in this view.'):
      !matches.length?t('没有匹配的关系。','No connections match your search.'):
      t('显示 '+(start+1)+'–'+end+' 条，共 '+matches.length+' 条','Showing '+(start+1)+'–'+end+' of '+matches.length);
  }
  function select(id){
    selected=id;
    const n=nodes.get(id);
    $('meaning').replaceChildren();$('labels').replaceChildren();$('leaders').replaceChildren();labels=[];
    pageIndex=0;$('find').value='';showConnections();
    if(!n){$('name').textContent='';$('status').textContent='';return;}
    $('objects').value=id;$('name').textContent=n.label;
    $('status').textContent=[names[n.kind]||n.kind,n.domain,statuses[n.status]||n.status,n.changed?t('本次有改动','Changed'):null].filter(Boolean).join(' · ');
    showMeaning($('meaning'),n,true);
    const neighbors=adjacent.get(id)||[];
    if(!snapshot){
      const back=new URL('/',location.origin);back.searchParams.set('lang',lang);back.searchParams.set('focus',id);
      back.searchParams.set('revision',data.revision);back.hash='graph';$('editor').href=back.href;
    }
    const ids=[id,...(data.nodes.length<=14?data.nodes.map(x=>x.id):neighbors.slice(0,6).map(x=>x[1]))];
    for(const key of new Set(ids)){
      const asset=nodes.get(key),span=document.createElement('span');
      span.textContent=displayName(asset);span.className='label'+(key===id?' active':'');
      const line=document.createElementNS('http://www.w3.org/2000/svg','line');
      $('labels').append(span);$('leaders').append(line);
      labels.push({n:asset,span,line});
    }
    if(graph){
      for(const label of labels){label.w=label.span.offsetWidth;label.h=label.span.offsetHeight;}
      positionLabels();
    }else{$('labels').replaceChildren();$('leaders').replaceChildren();}
  }
  function render(next){
    data=next;
    const {nodes:list,edges}=data;
    place(list,edges,data.center,data.full);
    nodes=new Map(list.map(n=>[n.id,n]));adjacent=new Map();
    function connect(a,b,e,out){if(!adjacent.has(a))adjacent.set(a,[]);adjacent.get(a).push([e,b,out]);}
    for(const e of edges){connect(e.source,e.target,e,true);if(e.source!==e.target)connect(e.target,e.source,e,false);}
    sameNames=new Set();sameDomainNames=new Set();
    const knownNames=new Set(),knownDomainNames=new Set();
    for(const n of list){
      const pair=JSON.stringify([n.label,n.domain]);
      if(knownNames.has(n.label))sameNames.add(n.label);
      if(knownDomainNames.has(pair))sameDomainNames.add(pair);
      knownNames.add(n.label);knownDomainNames.add(pair);
    }
    const menu=document.createDocumentFragment();
    for(const n of list){const o=document.createElement('option');o.value=n.id;o.textContent=displayName(n);menu.append(o);}
    $('objects').replaceChildren(menu);$('objects').disabled=!list.length;
    $('scope').textContent=(data.full?t('全量','Full model'):data.focus?t('对象及直接关系','Object and neighbors'):
      data.changeRevision?t('变更视图','Changes'):t('局部图','Local view'))+t(' · 模型 r',' · Model r')+data.revision;
    const summary=[list.length+t(' 个对象',' objects')+' · '+edges.length+t(' 条连线',' links')];
    if(!data.full&&data.eligible>list.length)summary.push(t('局部共 ','Local scope: ')+data.eligible+t(' 个对象，已限量显示',' objects; display capped'));
    if(data.changeRevision)summary.push(t('上次变更 r','Last change r')+data.changeRevision+' · '+data.changedCount+t(' 项',' assets'));
    if(data.inactiveCount)summary.push(t('已停用或移除 ','Retired or removed: ')+data.inactiveCount+' · '+data.inactiveNames.join(', '));
    $('summary').textContent=summary.join(' / ');
    $('near').hidden=!data.full||!list.length;
    const clipped=!data.full&&data.eligible>list.length;
    $('expand').hidden=!clipped||!data.focus||Boolean(snapshot&&!snapshot.data.full);
    $('limit').hidden=!clipped;
    if(clipped){
      if(snapshot&&!snapshot.data.full){
        const args=data.focus?'--id '+data.focus+' --all-neighbors':'--all';
        $('limit').textContent=t('这份离线图只包含 '+list.length+' / '+data.eligible+' 个对象。要查看余下对象，请从原语义包重新导出，加上 '+args+'。',
          'This offline file contains '+list.length+' of '+data.eligible+' objects. Re-export the source package with '+args+' to see the rest.');
      }else{
        $('limit').textContent=data.focus?t('需要看更多邻居？可展开此对象的全部直接关系。','Expand to see every direct neighbor of this object.'):
          t('切换到全量图可以查看其余对象。','Show the full model to inspect the remaining objects.');
      }
    }
    if(snapshot?.data.full){
      $('switch').hidden=data.full;$('switch').textContent=t('返回全量图','Back to full graph');
      $('switch').onclick=()=>{const id=selected;render(snapshot.data);if(nodes.has(id)&&selected!==id)select(id);};
    }
    if(!snapshot){
      $('switch').hidden=false;$('switch').textContent=data.full?t('看局部图','Show local view'):t('浏览全量图','Browse full model');
      $('switch').onclick=()=>{const url=new URL(location.href);
        if(data.full){url.searchParams.delete('scope');if(selected)url.searchParams.set('focus',selected);}
        else{url.searchParams.set('scope','all');url.searchParams.delete('focus');}
        location.assign(url);
      };
      $('editor').hidden=false;$('editor').href='/?lang='+encodeURIComponent(lang)+'#graph';
    }
    const gesture=window.matchMedia('(pointer: coarse)').matches
      ? t('单指旋转 · 双指缩放 · 轻点查看关系','Drag to rotate · Pinch to zoom · Tap to inspect')
      : t('拖动旋转 · 滚轮缩放 · 点击对象看关系','Drag to rotate · Scroll to zoom · Click to inspect');
    $('hint').textContent=list.length?gesture:
      t('这次没有可显示的有效对象。','No active objects to show here.');
    if(list.length){
      try{
        if(!graph){
          graph=new ForceGraph3D($('graph'),{controlType:'orbit',rendererConfig:{antialias:true}});
          graph.showNavInfo(false).backgroundColor('#f4f8f6').nodeLabel(()=>null).linkLabel(()=>null)
            .nodeOpacity(1).nodeRelSize(1).linkWidth(0).linkOpacity(.78).cooldownTicks(0)
            .nodeColor(n=>colors[n.kind]||'#758b84').onNodeClick(n=>select(n.id));
          trackCamera();
          new ResizeObserver(()=>{
            const distance=fitDistance();
            if(graph.width()===width()&&graph.height()===height()&&distance===frameDistance)return;
            graph.width(width()).height(height());
            if(frameDistance){
              const camera=graph.camera(),target=graph.controls().target;
              camera.position.sub(target).multiplyScalar(distance/frameDistance).add(target);
              camera.updateMatrixWorld();
            }
            frameDistance=distance;positionLabels();
          }).observe(stage);
        }
        const dense=list.length>80;
        const radius=n=>dense?(n.kind==='field'?1.6:3):(n.id===data.center?14:7);
        graph.width(width()).height(height()).nodeVal(n=>radius(n)**3).nodeResolution(dense?5:14)
          .linkColor(e=>e.changed&&!dense?'#9e6c31':'#597b72').linkCurvature(e=>e.self ? 0.55 : 0)
          .linkDirectionalArrowLength(dense?0:3)
          .graphData({nodes:list,links:edges.map(e=>({...e,self:e.source===e.target}))});
        frameDistance=fitDistance();
        graph.cameraPosition({x:0,y:0,z:frameDistance},{x:0,y:0,z:0},0);
        graph.camera().updateMatrixWorld();
      }catch(error){$('hint').textContent=t('当前浏览器无法绘制 3D，可在右侧查看对象和关系。','3D unavailable. Explore objects and connections in the list.');}
    }else if(graph)graph.graphData({nodes:[],links:[]});
    select(nodes.has(data.center)?data.center:list[0]?.id);
  }
  function fitDistance(){
    return (data.nodes.length<=18?585:900)*Math.max(1,height()/Math.max(1,width())*1.28);
  }
  async function api(path){
    const res=await fetch(path,{headers:{'X-Workbench-Token':document.querySelector('meta[name=session-token]').content}});
    const body=await res.json();if(!res.ok)throw Error(body.error||res.statusText);return body;
  }
  async function update(check){
    if(busy)return;
    busy=true;
    try{
      if(check&&data&&(await api('/api/knowledge/revision')).revision===data.revision)return;
      const query=new URLSearchParams(params);if(query.get('scope')==='all')query.delete('focus');
      const next=await api('/api/knowledge/graph-view?'+query);
      if(check && data && next.changeRevision!=null && next.changeRevision===data.changeRevision){
        data.revision=next.revision;
        $('scope').textContent=$('scope').textContent.replace(/r[0-9]+$/,'r'+next.revision);
        return;
      }
      render(next);
    }catch(error){
      $('hint').textContent=error.message;
      if(!data){
        const url=new URL(location.href);
        $('editor').hidden=false;$('editor').href='/?lang='+encodeURIComponent(lang)+'#graph';
        if(params.has('focus')){
          $('switch').hidden=false;$('switch').textContent=t('浏览全量图','Browse full model');
          $('switch').onclick=()=>{url.searchParams.delete('focus');url.searchParams.set('scope','all');location.assign(url);};
        }
      }
      if(data)$('summary').textContent=t('仍显示上次读取的修订 ','Showing the last loaded revision ')+data.revision;
    }
    finally{busy=false;}
  }
  if(snapshot)render(snapshot.data);
  else{update(false);if(!params.has('revision'))setInterval(()=>{if(!document.hidden)update(true);},2500);}
})();
