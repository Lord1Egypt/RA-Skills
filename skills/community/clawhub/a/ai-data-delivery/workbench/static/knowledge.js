'use strict';
/* The semantic workbench uses one canonical API. The older numeric tools stay in app.js. */
window.KnowledgeWorkbench = (() => {
  const tr=(s,...v)=>window.UIText?window.UIText.t(s,...v):typeof s==='string'?s:s.reduce((r,p,i)=>r+p+(i<v.length?v[i]:''),'');
  const say=(zh,en)=>window.UIText?.language==='en'?en:zh;

  const $ = s => document.querySelector(s), $$ = s => [...document.querySelectorAll(s)];
  const esc = v => String(v ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const copy = v => JSON.parse(JSON.stringify(v));
  const kinds = {entity:tr('业务对象'),term:tr('术语'),attribute:tr('业务属性'),relation:tr('关系'),metric:tr('指标'),rule:tr('规则与职责'),dataset:tr('数据集'),field:tr('数据字段'),mapping:tr('数据映射')};
  const statuses = {draft:tr('草稿'),confirmed:tr('已确认'),needs_review:tr('需复核'),retired:tr('已停用'),pending:tr('待处理'),running:tr('处理中'),review:tr('待核对'),partial:tr('部分完成'),failed:tr('失败'),cancelled:tr('已取消'),accepted:tr('已接纳'),rejected:tr('已拒绝'),deferred:tr('已暂缓'),stale:tr('需重新核对'),complete:tr('解析完成'),needs_conversion:tr('待转换')};
  const relationTypes = {business:tr('业务关系'),is_a:tr('分类属于'),denotes:tr('术语指称'),has_attribute:tr('拥有属性'),measures:tr('衡量对象'),applies_to:tr('规则适用'),depends_on:tr('依赖定义'),maps_to:tr('映射数据'),physical_fk:tr('物理外键')};
  const propertyFields = {
    entity:[], term:[], dataset:[['source',tr('物理表或视图')]],
    attribute:[['value_type',tr('值类型')],['unit',tr('单位')],['values',tr('枚举说明')]],
    field:[['value_type',tr('值类型')],['column',tr('物理字段')],['unit',tr('单位')]],
    metric:[['grain',tr('统计粒度')],['unit',tr('单位')],['inclusions',tr('包含范围')],['exclusions',tr('排除范围')],['time_scope',tr('业务时间范围')],['expression',tr('计算表达式（如已有）')]],
    rule:[['condition',tr('成立前提')],['requirement',tr('判断、职责或动作要求')],['exceptions',tr('例外（未知请留空）')]],
    relation:[['condition',tr('适用条件')],['cardinality',say('数量关系（如一对多）','Cardinality (e.g. one to many)')]],
    mapping:[['transformation',tr('映射、换算或过滤说明')]]
  };
  let C, S = {assets:[],sources:[],groups:[],batches:[],problems:[],history:[],snapshots:[],layout:{}}, activePage = 'knowledge';
  const pending = new Map(), drafts = new Map(), taskTexts = new Map();
  const assetDrafts=new Map();
  let importDraft = {name:tr('业务说明.txt'),text:'',domain:'',scope:'',source_id:'',distinct:false}, selectedFiles = [], importResults = [];
  let reviewPageIndex=0;const candidatePages=new Map(),refPools=new Map();
  let reviewFilter='pending', reviewBatch='', deliverySelection=new Set(), publishResult=null, publishExecution=false, scopedDelivery=false;
  let G={view:'all',mode:'graph',fieldsExpanded:false,domain:'',kind:'',status:'',query:'',selected:null,limit:80,zoom:1,fixed:[],focus:null,expanded:false,inspector:false};
  const NODE_WIDTH=172, NODE_HEIGHT=68;
  const COLUMN_STEP=250, ROW_STEP=135;
  let virtualPositions={}, graphPlan=null, layoutPending=false, autoPendingKey=null, plotOffset={key:null,x:0,y:0};
  const automaticPlans=new Map(), routedPlans=new Map();
  let runningWorker=null;
  const denseGraph=input=>typeof Worker==='function'&&(input.nodes.length>=24||input.edges.length>=32);
  function layoutButton(){
    const button=$('[data-kw="arrange"]');if(!button)return;
    button.disabled=layoutPending&&!runningWorker;
    button.textContent=runningWorker?say('取消布局','Cancel layout'):layoutPending?tr('布局中…'):tr('自动布局');
    if(button.dataset)button.dataset.layoutAction=runningWorker?'cancel':'arrange';
  }
  function runLayout(input,key,routeOnly){
    if(!denseGraph(input))return window.SemanticGraphLayout.layout(input);
    return new Promise((resolve,reject)=>{
      const worker=new Worker('/graph-layout.js');
      const finish=(plan,error)=>{
        worker.terminate();runningWorker=null;
        if(error)reject(error);else resolve(plan);
      };
      runningWorker={key,cancel:()=>finish(null)};
      layoutButton();
      worker.onmessage=({data})=>finish(data.plan,data.error?new Error(data.error):null);
      worker.onerror=e=>finish(null,new Error(e.message));
      worker.postMessage({input,routeOnly});
    });
  }
  let layoutUndo=[], drag=null, connection=null, dialog=null;
  const badge = value => `<span class="badge kw-status-${esc(value)}">${esc(statuses[value]||value||tr('未说明'))}</span>`;
  const button = (label, action, attrs='', cls='') => `<button type="button" class="${cls}" data-kw="${action}" ${attrs}>${label}</button>`;
  const options = (items,value,blank=tr('请选择')) => (blank===null?'':`<option value="">${esc(blank)}</option>`)+items.map(([v,l])=>`<option value="${esc(v)}" ${String(value)===String(v)?'selected':''}>${esc(l)}</option>`).join('');
  const alwaysFields=new Set(['name','from','to','relation_type','predicate']);
  const mark=(when)=>' <small class="kw-field-mark">'+(when?say('确认时必填','To confirm'):say('必填','Required'))+'</small>';
  const field = (label,key,value='',multiline=false,confirmOnly=false) => `<label>${esc(label)}${alwaysFields.has(key)?mark(false):(confirmOnly||['definition','scope'].includes(key))?mark(true):''}${multiline?`<textarea data-field="${esc(key)}">${esc(value)}</textarea>`:`<input ${alwaysFields.has(key)?'required':''} data-field="${esc(key)}" value="${esc(value)}">`}</label>`;
  const scopeText = value => value===null?tr('未明确'):Array.isArray(value)?value.map(scopeText).join('、'):typeof value==='object'?Object.entries(value).map(([k,v])=>`${k}：${scopeText(v)}`).join('；'):typeof value==='boolean'?(value?tr('是'):tr('否')):String(value??'');
  function scopeFields(scope){
    if(!scope||typeof scope!=='object')return field(tr('适用范围'),'scope',scope);
    const leaves=(value,path=[])=>{
      if(value!==null&&typeof value==='object')return Object.keys(value).length?Object.entries(value).map(([k,v])=>leaves(v,[...path,k])).join(''):tr`<p>${esc(path.join(' / '))}：未列出分项</p>`;
      const label=path.join(' / '),attrs=`data-scope-path="${esc(JSON.stringify(path))}" data-scope-type="${typeof value}" data-scope-label="${esc(label)}"`;
      if(value===null)return tr`<p>${esc(label)}：尚未明确</p>`;
      return `<label>${esc(label)}${typeof value==='boolean'?tr`<select ${attrs}><option value="true" ${value?'selected':''}>是</option><option value="false" ${value?'':'selected'}>否</option></select>`:typeof value==='number'?`<input ${attrs} type="number" step="any" required value="${value}">`:`<textarea ${attrs}>${esc(value)}</textarea>`}</label>`;
    };
    return tr`<fieldset class="kw-scope-fields"><legend>适用范围（分项）</legend>${leaves(scope)}</fieldset>`;
  }
  function readScope(container,original,strict=true){
    const value=copy(original);
    for(const el of container.querySelectorAll('[data-scope-path]')){
      const path=JSON.parse(el.dataset.scopePath);let parent=value;
      for(const key of path.slice(0,-1)){if(!parent||!Object.hasOwn(parent,key))throw Error(tr('范围分项已变化，请重新核对'));parent=parent[key];}
      const key=path.at(-1);if(!parent||!Object.hasOwn(parent,key))throw Error(tr('范围分项已变化，请重新核对'));
      let next=el.value;
      if(el.dataset.scopeType==='number'){
        if(!el.value.trim()||!Number.isFinite(Number(el.value))){if(strict)throw Error(tr('适用范围“')+el.dataset.scopeLabel+tr('”需要有效数值'));continue;}
        next=Number(el.value);
      }else if(el.dataset.scopeType==='boolean')next=el.value==='true';
      parent[key]=next;
    }
    return value;
  }
  const searchProperties = ['condition','requirement','unit','grain','inclusions','exclusions','time_scope','expression','value_type','knowledge_gaps'];
  const searchValue = value => value == null ? '' : typeof value === 'object' ? Object.values(value).map(searchValue).join(' ') : String(value);
  const semanticSearchText = a => [a.name,a.aliases,a.definition,a.domain,a.scope,a.predicate,a.relation_type,...searchProperties.map(k=>a.properties?.[k])].map(searchValue).join(' ').toLowerCase();
  const heading = (title,subtitle,actions='') => `<div class="page-head"><div><span class="eyebrow">SEMANTIC WORKSPACE</span><h1>${title}</h1><p class="sub">${subtitle}</p></div><div class="header-actions">${actions}</div></div>`;
  const empty = (title,detail,actions='') => `<div class="empty"><b>${title}</b><p>${detail}</p>${actions}</div>`;
  const asset = id => S.assets.find(a=>a.id===id);
  const nameOf = id => asset(id)?.name || id || tr('未指定');
  const byId = (collection,id) => (S[collection]||[]).find(x=>x.id===id);
  const uid = () => crypto.randomUUID();
  function fmt(value){
    if(Array.isArray(value))return value.map(fmt).join(' / ');
    if(value===null||value===undefined||value==='')return tr('位置未说明');
    if(typeof value!=='object')return String(value);
    const labels={page:tr('页'),line:tr('行'),start_line:tr('起始行'),end_line:tr('结束行'),line_start:tr('起始行'),line_end:tr('结束行'),headings:tr('章节'),type:tr('内容类型'),part:tr('部分'),table:tr('表'),columns:tr('列'),column_start:tr('起始列'),column_end:tr('结束列'),sheet:tr('工作表'),row:tr('行'),column:tr('列'),paragraph:tr('段落'),statement:tr('语句'),cell:tr('单元格'),claims:say('双方主张','Claims'),claim:say('口径','Claim'),applicability:say('适用范围','Applicability'),previous:say('原冲突','Original conflict'),decision:say('裁决','Decision'),source_id:say('来源','Source')};
    const types={text:tr('文本'),ddl:tr('表结构'),paragraph:tr('段落'),cell:tr('单元格'),foreign_key:tr('外键'),column:tr('字段'),table:tr('表')};
    return Object.entries(value).filter(([,v])=>v!==null&&v!==''&&(!Array.isArray(v)||v.length)).map(([k,v])=>(labels[k]||k)+' '+(k==='type'&&typeof v==='string'&&types[v]||fmt(v))).join(' · ');
  }
  function configure(context) { C=context; }
  let latestDelta=null, missingFocus='', requestedRevision=null;
  function modelDelta(next, previous) {
    const events=(next.change_events||[]).filter(e=>e.changed_asset_ids?.length && (!previous||e.revision>previous.revision));
    const relevant=previous?events:events.slice(-1);
    const revisions=new Map();let items;
    if(relevant.length){
      for(const event of relevant)for(const id of event.changed_asset_ids)revisions.set(id,event.revision);
      items=next.assets.filter(a=>revisions.has(a.id));
    }else if(previous){
      const before=new Map(previous.assets.map(a=>[a.id,a]));
      items=next.assets.filter(a=>JSON.stringify(a)!==JSON.stringify(before.get(a.id)));
    }else return null;
    const rank=a=>['relation','mapping'].includes(a.kind)?0:a.kind==='field'?2:1;
    return items.length?{revision:next.revision,total:items.length,items:items.filter(a=>a.status!=='retired').sort((a,b)=>rank(a)-rank(b)||(revisions.get(b.id)||0)-(revisions.get(a.id)||0)).slice(0,4)}:null;
  }
  function explorerLink(label, focus, revision){
    const q=new URLSearchParams({view:'3d',lang:window.UIText?.language||'zh'});
    if(focus)q.set('focus',focus);
    if(revision!=null)q.set('revision',revision);
    return '<a class="kw-explorer-link" href="/?'+esc(q.toString())+'" target="_blank" rel="noopener">'+esc(label)+'</a>';
  }
  function changeLinks(delta,newTab=false){
    if(!delta?.total)return '';
    return `<div class="kw-change" role="status"><strong>r${esc(delta.revision)}</strong> ${delta.items.map(a=>{
      const edge=['relation','mapping'].includes(a.kind);
      const label=(edge?say('查看刚改的关系','View changed relation'):say('查看变更','View change'))+' · '+a.name;
      if(!newTab)return button(esc(label),'locate-change',`data-id="${esc(a.id)}"`,'quiet small');
      const url=new URL(window.location.href);
      url.searchParams.set('focus',a.id);url.searchParams.set('revision',delta.revision);url.hash='graph';
      return `<a href="${esc(url.href)}" target="_blank" rel="noopener">${esc(label)} · ${say('新标签页','New tab')}</a>`;
    }).join(' ')} ${explorerLink(say('看本次变更的 3D 图','View this change in 3D'),null,delta.revision)}</div>`;
  }
  function graphLocation(id){
    if(!window.history||!window.location?.href)return;
    const url=new URL(window.location.href);url.hash='graph';url.searchParams.delete('domain');
    if(id){url.searchParams.set('focus',id);url.searchParams.set('revision',S.revision);}
    else{url.searchParams.delete('focus');url.searchParams.delete('revision');}
    requestedRevision=null;missingFocus='';window.history.replaceState(null,'',url);
  }
  function previewExternal(next){
    const holder=$('#kw-dialog[open] #kw-external-change');
    if(holder&&holder.dataset.revision!==String(next.revision)){
      holder.innerHTML=changeLinks(modelDelta(next,S),true);
      holder.dataset.revision=String(next.revision);
    }
  }
  function update(state) {
    window.ScenarioWorkbench?.update(state);
    window.MetadataWorkbench?.update(state);
    const previous=S,first=!S.project_id; S={assets:[],sources:[],groups:[],batches:[],problems:[],history:[],snapshots:[],layout:{},...state};
    if(first||S.revision>previous.revision)latestDelta=modelDelta(S,first?null:previous)||latestDelta;
    if(first)try{for(const [key,value] of JSON.parse(sessionStorage.getItem('kw-pending:'+S.project_id)||'[]')){pending.set(key,value);if(value.path==='edit'&&value.request.asset)assetDrafts.set(key.replace(/^edit:/,''),{asset:value.request.asset,declaration:'',baseRevision:value.request.revision});if(value.path==='review'&&value.request.group_id)drafts.set(value.request.group_id,{assets:value.request.assets||[],reason:value.request.reason||''});}}catch(_){}
    if(first)try{const saved=JSON.parse(localStorage.getItem('kw-view:'+S.project_id)||'null');if(saved){
      G={...G,...saved,hasSavedView:true};
      if(saved.fieldsExpanded===undefined)G.fieldsExpanded=S.assets.some(a=>a.kind==='field'&&S.layout['semantic:'+G.view+':'+a.id]);
    }}catch(_){}
    if(first&&window.location?.search){const q=new URLSearchParams(window.location.search), focus=q.get('focus'), domain=q.get('domain');requestedRevision=q.get('revision');
      if(focus&&S.assets.some(a=>a.id===focus))Object.assign(G,{view:'all',query:'',domain:'',kind:'',status:'',mode:'graph',selected:focus,focus,inspector:true,limit:80});
      else if(focus){missingFocus=focus;Object.assign(G,{view:'all',domain:'',query:'',kind:'',status:'',mode:'graph',selected:null,focus:null,inspector:false});}
      else if(domain&&S.assets.some(a=>a.domain===domain))Object.assign(G,{view:'all',domain,query:'',kind:'',status:'',mode:'graph',selected:null,focus:null,inspector:false,limit:80});
    }
    if(first)try{const saved=JSON.parse(sessionStorage.getItem('kw-delivery:'+S.project_id)||'null');if(saved){deliverySelection=new Set(saved.ids);scopedDelivery=!!saved.scoped;}}catch(_){}
  }
  function saveView(){try{localStorage.setItem('kw-view:'+S.project_id,JSON.stringify(G));}catch(_){}}
  function rerender(){const main=$('#main');if(!main)return;main.innerHTML=render(activePage);mount();}
  function persistPending(){
    try{const saved=[...pending].map(([key,op])=>{const value=copy(op);if(value.request.content_base64){delete value.request.content_base64;value.needsMaterial=true;}if(value.request.text?.length>200000){delete value.request.text;value.needsMaterial=true;}return [key,value];});sessionStorage.setItem('kw-pending:'+S.project_id,JSON.stringify(saved));}catch(_){C.notify(tr('浏览器暂时无法保存提交恢复记录，请保持此页并先查询提交结果。'));}
  }
  async function payloadSignature(payload){const digest=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(JSON.stringify(payload)));return [...new Uint8Array(digest)].map(x=>x.toString(16).padStart(2,'0')).join('');}
  async function receiptFor(key){const op=pending.get(key);if(!op)return null;const result=await C.api('knowledge/operation/'+encodeURIComponent(op.request.operation_id));if(result.found){pending.delete(key);if(op.path==='edit')assetDrafts.delete(key.replace(/^edit:/,''));if(op.path==='review')drafts.delete(op.request.group_id);persistPending();if(op.path==='publish')publishResult=result.receipt.result;await C.reload();return result.receipt;}op.checked=true;persistPending();return null;}
  async function transact(key,path,payload,baseRevision) {
    if(path==='import'||path==='task')payload={language:window.UIText?.language||'zh',...payload};
    const signature=await payloadSignature(payload);let op=pending.get(key);
    if(op){const receipt=await receiptFor(key);if(receipt){if(op.signature!==signature)throw Error(tr('上次提交已完成并已读回；当前修改尚未提交，请对照最新结果后再次保存。'));return receipt.result??receipt;}if(op.signature!==signature)throw Error(tr('上次提交结果尚未确认。请到项目历史查询结果，或保持原输入重试；本次修改已保留。'));op.request={...payload,revision:op.request.revision,operation_id:op.request.operation_id};op.needsMaterial=false;}
    else{op={signature,path,request:{...payload,revision:baseRevision??S.revision,operation_id:uid()}};pending.set(key,op);}
    persistPending();let response;
    try{response=await C.api('knowledge/'+path,op.request);}catch(e){if(e.status&&e.status<500){pending.delete(key);persistPending();}else e.message+=tr('。提交结果尚未确认，请在项目历史先查询结果或重试原提交。');throw e;}
    pending.delete(key);if(op.path==='edit')assetDrafts.delete(key.replace(/^edit:/,''));if(op.path==='review')drafts.delete(op.request.group_id);persistPending();
    try{await C.reload();}catch(e){C.notify(tr('操作已保存，但列表刷新失败：')+e.message+tr('。请刷新读取结果。'));}
    return response.result??response;
  }
  function pendingHtml(){return pending.size?tr`<div class="notice warning"><b>${pending.size} 项提交尚待确认回执</b><p>输入与操作身份已保留；刷新页面不会自动重发。</p>${button(tr('查询与恢复提交'),'go','data-page="history"','small')}</div>`:'';}
  function pendingRows(){return [...pending].map(([key,op])=>`<div class="gap"><div><b>${esc(({edit:tr('保存知识'),review:tr('候选组处置'),publish:tr('发布快照'),import:tr('保存材料'),merge:tr('合并身份'),separate:tr('保持分离'),'review-source':tr('复核来源')}[op.path]||tr('知识维护'))+' · '+(op.request.asset?.name||op.request.filename||op.request.group_id||''))}</b><p>${op.checked?tr('尚无完成回执；重试会沿用同一操作身份。'):tr('先查询已保存结果，再决定是否重试。')}${op.needsMaterial?tr('原件需重新选择，不能在此自动重发。'):''}</p></div><div class="row">${button(tr('查询结果'),'pending-query',`data-key="${esc(key)}"`,'small')}${op.checked&&!op.needsMaterial?button(tr('重试原提交'),'pending-retry',`data-key="${esc(key)}"`,'small'):''}</div></div>`).join('');}
  function resolveSource(id,revision,fragmentId,extractionId){
    const source=byId('sources',id);if(!source)throw Error(tr('找不到这份来源，请刷新项目'));
    const r=source.revisions?.find(x=>String(x.revision)===String(revision??source.current_revision));if(!r)throw Error(tr('指定的来源修订不存在，不能改读最新修订'));
    const parses=r.extractions?.length?r.extractions:[{id:null,parsed:r.parsed}];let extraction;
    if(extractionId){extraction=parses.find(x=>x.id===extractionId);if(!extraction)throw Error(tr('指定的提取结果不存在，请修复依据身份'));}
    else if(fragmentId){const matches=parses.filter(x=>x.parsed?.fragments?.some(f=>f.id===fragmentId));if(!matches.length)throw Error(tr('原依据片段不存在，请修复来源定位'));const values=matches.map(x=>x.parsed.fragments.find(f=>f.id===fragmentId));if(new Set(values.map(x=>JSON.stringify(x))).size>1)throw Error(tr('多次提取的同名片段存在差异，请明确原依据的提取身份'));extraction=matches[0];}
    else extraction=parses.find(x=>x.id===r.current_extraction)||parses.at(-1);
    const fragment=fragmentId?extraction?.parsed?.fragments?.find(f=>f.id===fragmentId):null;if(fragmentId&&!fragment)throw Error(tr('指定提取结果中没有原依据片段'));
    return {source,revision:{...r,parsed:extraction?.parsed||r.parsed},extraction_id:extraction?.id,fragment};
  }
  function issuesHtml(issues=[]){return issues.map(x=>`<div class="kw-publish-issue"><b>${esc(nameOf(x.asset_id||x.id)||tr('交付范围'))}</b><p>${esc(window.UIText?window.UIText.issue(x):(x.message||x.code))}</p>${x.asset_id?button(tr('定位并修正'),'locate',`data-id="${esc(x.asset_id)}"`,'small'):''}</div>`).join('');}
  function scopeHtml(m){if(!m)return '';const x=m.scope||{};return tr`<div class="notice"><b>${m.draft?tr('草稿快照'):tr('确认快照')} · ${m.complete?tr('本范围完整'):tr('仍有待补缺口')}</b><p>实际包含 ${(x.included_ids||[]).length} 项，自动补入 ${(x.dependency_ids||[]).length} 项必需依赖。</p><p>${x.include_execution?tr('附带数据映射与执行声明'):tr('未附带执行声明；必要物理依赖仍保留')}。范围外 ${x.omitted_asset_count||0} 项。</p>${x.dependency_ids?.length?tr`<details><summary>查看补入依赖</summary><p>${esc(x.dependency_ids.map(nameOf).join('、'))}</p></details>`:''}${m.issues?.length?issuesHtml(m.issues):''}</div>`;}
  function evidenceHtml(evidence=[]) {
    if(!evidence.length)return `<p class="muted">${say('尚未记录依据','No evidence attached yet')}</p>`;
    return evidence.map(e=>{
      if(e.type==='manual')return tr`<div class="kw-evidence"><span class="privacy">${say('人工说明','Explanation')} · ${esc(e.actor||tr('本地操作者'))}</span><blockquote>${esc(e.quote||'')}</blockquote></div>`;
      let resolved;try{resolved=resolveSource(e.source_id,e.revision,e.fragment_id,e.extraction_id);}catch(error){return tr`<div class="kw-evidence error"><b>来源定位需修复</b><p>${esc(error.message)}</p><blockquote>${esc(e.quote)}</blockquote></div>`;}const {source,fragment}=resolved;
      return tr`<div class="kw-evidence"><div class="row between"><b>${esc(source?.name||e.source_id)}</b>${button(tr('查看原文'),'source',`data-id="${esc(e.source_id)}" data-revision="${e.revision}" data-fragment="${esc(e.fragment_id||'')}" data-extraction="${esc(e.extraction_id||'')}"`,'quiet small')}</div><span class="privacy">修订 ${esc(e.revision)} · ${esc(fmt(fragment?.location))}</span><blockquote>${esc(e.quote||fragment?.text||tr('片段不可用'))}</blockquote></div>`;
    }).join('');
  }
  function render(page){if(page!=='graph')connection=null;activePage=page;return pendingHtml()+({knowledge:materialsPage,review:reviewPage,graph:graphPage,publish:publishPage,history:historyPage}[page]||materialsPage)();}
  let canvasObserver=null,keepFitted=true,fitAllNodes=false;
  function watchCanvas(){
    canvasObserver?.disconnect();canvasObserver=null;
    const canvas=$('#kw-canvas');
    if(!canvas||typeof ResizeObserver==='undefined')return;
    let width=canvas.clientWidth,height=canvas.clientHeight;
    canvasObserver=new ResizeObserver(()=>{
      if(activePage!=='graph'||!canvas.isConnected||drag||!canvas.clientWidth||!canvas.clientHeight)return;
      if(canvas.clientWidth===width&&canvas.clientHeight===height)return;
      width=canvas.clientWidth;height=canvas.clientHeight;
      const box=canvas.getBoundingClientRect();
      const visible=()=>Array.from(canvas.querySelectorAll('[data-kw-node]')).some(node=>{
        const r=node.getBoundingClientRect();
        return r.right>box.left&&r.left<box.right&&r.bottom>box.top&&r.top<box.bottom;
      });
      drawGraph(keepFitted||!visible());
    });
    canvasObserver.observe(canvas);
  }
  function mount(){$$('details.kw-candidate[open]').forEach(hydrateCandidate);if(activePage==='graph'){drawGraph();drawInspector();}watchCanvas();if(dialog?.conflict)showConflict();}

  function exampleGuide(){
    if(C?.legacyState?.()?.model_only || !S.document?.semantic_example)return '';
    return tr`<section class="card kw-example"><h2>设备借用建模练习</h2><p>这是预先编写的合成样例，不是自动 AI 抽取。先核对 DDL 结构组；接纳后回到这里准备业务候选，再核对业务定义、范围和映射。</p><div class="row">${button(tr('先核对表结构'),'go','data-page="review"')}${button(tr('准备练习业务候选'),'example','','primary')}</div><p>完成核对后打开图谱、编辑一项定义并保存，再到交付页发布语义包。独立 Agent 应解释可借条件，并指出缺少库存记录，不能给出当前台数或办理借用。</p></section>`;
  }
  function materialsPage(){return heading(tr('导入 SQL 或资料'),tr('空模型可直接生成结构草稿。已有模型的新增材料保留为候选，避免覆盖你的修改。'),button(tr('连接数据库'),'go','data-page="connections"'))+exampleGuide()+
    tr`<section class="card tool-import"><h2>选择文件</h2><p class="sub">SQL 建表语句可生成表、字段和显式外键。也支持文本、CSV / XLSX、DOCX、文本层 PDF、YAML / JSON。</p><div class="import-card"><label>选择文件（每份不超过 32 MB）<input id="kw-files" type="file" multiple accept=".txt,.md,.sql,.ddl,.csv,.xlsx,.docx,.pdf,.yaml,.yml,.json"></label><p class="privacy">${selectedFiles.length?esc(selectedFiles.map(f=>f.name).join('、')):tr('原件留在本机；不执行文件中的脚本或外部链接。')}</p>${!S.assets.length?tr('<label class="kw-inline-check"><input id="kw-seed-draft" type="checkbox" checked> 将 SQL 中明确的表、字段、外键写入初始草稿（不确认业务含义）</label>'):''}<details><summary>${say('文件编码与表格范围','Encoding and spreadsheet range')}</summary><label>${say('文本文件编码','Text file encoding')}<select id="kw-encoding" data-import="encoding">${options([['',say('自动（UTF-8 或 UTF-16 BOM）','Automatic (UTF-8 or UTF-16 BOM)')],['gb18030','GBK / GB18030'],['utf-16','UTF-16']],importDraft.encoding||'',null)}</select></label><div class="grid cols2"><label>工作表名<input id="kw-sheet" placeholder="留空读取全部工作表"></label><label>表头行<input id="kw-header" type="number" min="1" value="1"></label></div><label>单元格范围<input id="kw-range" placeholder="例如 A1:F30；留空读取全部"></label></details>${button(tr('导入所选文件'),'import-files','','primary')}</div><div id="kw-import-results">${importResults.map(r=>`<p class="${r.ok?'':'error'}">${esc(r.name)}：${esc(r.message)}</p>`).join('')}</div><p class="privacy">扫描页或不支持的语句会保留提示；草稿不等于已核实的业务定义。</p></section>`+
    tr`<details class="card tool-secondary"><summary>补充文字说明或指定来源</summary><label>材料名称<input id="kw-import-name" data-import="name" value="${esc(importDraft.name)}"></label><div class="grid cols2"><label>业务领域<input id="kw-import-domain" data-import="domain" value="${esc(importDraft.domain)}"></label><label>适用范围<input id="kw-import-scope" data-import="scope" value="${esc(importDraft.scope)}"></label></div><label>原文<textarea id="kw-import-text" data-import="text" rows="5">${esc(importDraft.text)}</textarea></label>${sourceChoice()}${button(tr('保存材料'),'import-text','','primary')}<p id="kw-import-error" class="error" role="alert"></p></details>`+
    tr`<details class="card tool-secondary"><summary>已有材料与解析提示（${S.sources.length}）</summary>${S.sources.length?S.sources.map(sourceRow).join(''):empty(tr('还没有材料'),tr('上传一份表结构即可开始。'))}</details><details class="card tool-secondary"><summary>让 Agent 补充业务含义</summary><p class="sub">需要理解业务文档时，再将原文和当前模型交给宿主 Agent。仅维护表结构无需执行此步骤。</p>${S.batches.length?S.batches.slice().reverse().map(batchRow).join(''):tr('<p>请先导入一份材料。</p>')}</details>`;}
  function sourceChoice(){return tr`<label>这次材料的来源<select id="kw-import-source" data-import="source_id">${options(S.sources.map(s=>[s.id,s.name]),importDraft.source_id,tr('作为新材料加入'))}</select></label><label class="kw-inline-check"><input type="checkbox" data-import="distinct" ${importDraft.distinct?'checked':''}> 内容相同但出处不同，保留独立来源</label>`;}
  function sourceRow(s){const r=s.revisions?.find(x=>x.revision===s.current_revision)||s.revisions?.at(-1),p=r?.parsed||{};return tr`<div class="gap"><div><h3>${esc(s.name)} ${badge(p.status)}</h3><p>${esc(s.domain||tr('领域待说明'))} · ${esc(s.format||p.format)} · 来源修订 ${esc(s.current_revision)} · ${p.fragments?.length||0} 个片段</p>${(p.warnings||[]).map(w=>`<p class="kw-warning">${esc(typeof w==='object'?w.message||fmt(w):w)}</p>`).join('')}</div><div class="row">${button(tr('查看原文'),'source',`data-id="${esc(s.id)}"`,'small')}${button(tr('更新材料'),'update-source',`data-id="${esc(s.id)}"`,'small')}</div></div>`;}
  function batchRow(b){const names=(b.sources||[]).map(r=>byId('sources',r.source_id)?.name||r.source_id).join('、');return `<div class="gap"><div><h3>${esc(names||tr('知识处理任务'))} ${badge(b.status)}</h3><p class="privacy">${esc(b.id)} · ${esc(b.created||'')}</p>${taskTexts.has(b.id)?tr`<div class="kw-task"><b>等待宿主处理</b><p>把下面指令交给当前 Agent；候选返回后点击刷新，再进入核对。</p><textarea readonly aria-label="宿主处理指令">${esc(taskTexts.get(b.id))}</textarea>${button(tr('复制指令'),'copy-task',`data-id="${esc(b.id)}"`,'small')}</div>`:''}</div><div class="row">${button(tr('准备 Agent 任务'),'prepare',`data-id="${esc(b.id)}"`,'small')}${button(tr('查看候选'),'batch-review',`data-id="${esc(b.id)}"`,'small')}${b.status==='cancelled'?button(tr('恢复任务'),'resume',`data-id="${esc(b.id)}"`,'small'):button(tr('取消任务'),'cancel-task',`data-id="${esc(b.id)}"`,'quiet small')}</div></div>`;}

  function reviewPage(){const groups=S.groups.filter(g=>(!reviewBatch||g.batch_id===reviewBatch)&&(reviewFilter==='all'||reviewFilter==='pending'?reviewFilter==='all'||(!g.superseded_by&&['pending','deferred','stale'].includes(g.status)):g.status===reviewFilter)).slice().reverse();reviewPageIndex=Math.min(reviewPageIndex,Math.max(0,Math.ceil(groups.length/10)-1));const visible=groups.slice(reviewPageIndex*10,reviewPageIndex*10+10),pages=Math.max(1,Math.ceil(groups.length/10));
    return heading(tr('把候选变成共同定义'),tr('按一组相关变化核对当前定义、建议和原文。接纳前可以直接修正。'),(C?.legacyState?.()?.model_only?'':button(tr('项目问题'),'legacy','data-page="issues"','small')))+
      tr`<div class="toolbar kw-toolbar"><label>处置状态<select id="kw-review-filter">${options([['pending',tr('待处理与暂缓')],['accepted',tr('已接纳')],['rejected',tr('已拒绝')],['all',tr('全部')]],reviewFilter,null)}</select></label><label>处理批次<select id="kw-review-batch">${options(S.batches.map(b=>[b.id,(b.sources||[]).map(r=>byId('sources',r.source_id)?.name||r.source_id).join('、')||b.id]),reviewBatch,tr('所有批次'))}</select></label><span class="spacer"></span><span class="privacy">${groups.length} 组变化</span></div>`+
      tr`<div class="row">${button(tr('上一页组'),'review-page',`data-page-index="${reviewPageIndex-1}" ${reviewPageIndex===0?'disabled':''}`,'small')}<span class="privacy">第 ${reviewPageIndex+1} / ${pages} 页 · 每页最多 10 组</span>${button(tr('下一页组'),'review-page',`data-page-index="${reviewPageIndex+1}" ${reviewPageIndex+1>=pages?'disabled':''}`,'small')}</div>${groups.length?visible.map(groupCard).join(''):empty(tr('当前没有待核对变化'),tr('可以先加入资料并准备宿主任务，或手工创建知识。'),button(tr('加入资料'),'go','data-page="knowledge"','primary'))}`+
      tr`<div class="section-title"><h2>需复核的知识</h2></div><div class="card">${S.assets.filter(a=>a.status==='needs_review').map(a=>`<div class="gap"><div><h3>${esc(a.name)} ${badge(a.status)}</h3><p>${esc(a.definition)}</p></div>${button(tr('对照来源并复核'),'review-source',`data-id="${esc(a.id)}"`,'small')}</div>`).join('')||tr('<p class="muted">没有来源更新引起的待复核知识。</p>')}</div>`;
  }
  function groupDraft(g){if(!drafts.has(g.id))drafts.set(g.id,{assets:g.candidates.map(c=>copy(c.asset||asset(c.target_id)||{})),reason:g.reason||''});return drafts.get(g.id);}
  function groupCard(g){const d=groupDraft(g),locked=!!g.superseded_by||['accepted','rejected'].includes(g.status),start=Math.min(candidatePages.get(g.id)||0,Math.max(0,Math.ceil(g.candidates.length/20)-1))*20;return tr`<section class="card kw-group" data-group="${esc(g.id)}"><div class="row between"><div><h2>${esc(g.summary||tr('候选变化'))} ${badge(g.status)}</h2><p class="privacy">${g.candidates.length} 项变化 · ${esc(g.id)}</p></div>${button(tr('刷新并核对当前状态'),'refresh','','quiet small')}${button(tr('重新准备宿主任务'),'prepare',`data-id="${esc(g.batch_id)}"`,'quiet small')}</div>${g.superseded_by?tr`<div class="notice">此组已由新的候选组替代，仅保留核对历史。${button(tr('查看接替候选'),'show-group',`data-id="${esc(g.superseded_by)}"`,'small')}</div>`:''}${g.reason?tr`<div class="notice">处置说明：${esc(g.reason)}</div>`:''}${candidatePager(g,start)}${g.candidates.slice(start,start+20).map((c,offset)=>{const i=start+offset;
      const a=d.assets[i],current=asset(c.target_id||a.id);return tr`<details class="kw-candidate" data-candidate-index="${i}" ${g.candidates.length<4?'open':''}><summary><span>${esc(kinds[a.kind]||c.op)} · ${esc(a.name||current?.name||c.target_id||tr('未命名'))}</span><span class="privacy">${esc(c.op==='retire'?tr('建议停用'):c.op==='merge'?tr('建议合并'):current?tr('修改已有定义'):tr('新增定义'))}</span></summary><div class="kw-diff"><div><span class="eyebrow">当前</span>${current?`<h3>${esc(current.name)}</h3><p>${esc(current.definition)}</p><p class="privacy">${esc(current.domain||tr('领域未说明'))} · ${esc(scopeText(current.scope||tr('范围未说明')))}</p>`:tr('<p class="muted">图谱中尚无对应资产</p>')}<p>${esc(c.reason||'')}</p>${evidenceHtml(c.evidence?.length?c.evidence:a.evidence)}</div><div><span class="eyebrow">${locked?tr('已处置候选'):tr('候选 · 可直接修正')}</span><p class="kw-meaning">${esc(a.definition||tr("尚无定义"))}</p><dl class="kw-meaning-properties">${(propertyFields[a.kind]||[]).filter(([key])=>a.properties?.[key]!==undefined&&a.properties[key]!=="" ).map(([key,label])=>`<dt>${esc(label)}</dt><dd>${esc(typeof a.properties[key]==="object"?fmt(a.properties[key]):a.properties[key])}</dd>`).join("")}</dl><p class="privacy">${esc(a.domain)} · ${esc(scopeText(a.scope))}</p><details class="kw-candidate-edit"><summary>${tr("修改含义与详细配置")}</summary><fieldset data-candidate="${i}" data-readonly="${locked}"></fieldset></details></div></div></details>`;}).join('')}${candidatePager(g,start)}<label>处置理由<textarea data-group-reason ${locked?'readonly':''} placeholder="拒绝或暂缓时说明原因；接纳时可记录判断。">${esc(d.reason)}</textarea></label><div class="row">${locked?'':button(tr('接纳整组'),'review-action',`data-id="${esc(g.id)}" data-mode="accept"`,'primary')+button(tr('暂缓'),'review-action',`data-id="${esc(g.id)}" data-mode="defer"`)+button(tr('拒绝'),'review-action',`data-id="${esc(g.id)}" data-mode="reject"`,'danger')}<span class="privacy">接纳整组会写入全部 ${g.candidates.length} 项，包含未展开与其他页候选；请逐项展开核对。当前目标变化时请重新准备宿主任务。</span></div><p class="error kw-group-error" role="alert"></p></section>`;}

  function candidatePager(g,start){return g.candidates.length>20?tr`<div class="row kw-candidate-pages">${button(tr('上一段候选'),'candidate-page',`data-id="${esc(g.id)}" data-offset="${start-20}" ${start===0?'disabled':''}`,'small')}<span class="privacy">本段 ${start+1}–${Math.min(start+20,g.candidates.length)} / 共 ${g.candidates.length} 项</span>${button(tr('下一段候选'),'candidate-page',`data-id="${esc(g.id)}" data-offset="${start+20}" ${start+20>=g.candidates.length?'disabled':''}`,'small')}</div>`:'';}
  function hydrateCandidate(details){const holder=details.querySelector('[data-candidate]');if(!holder||holder.dataset.loaded)return;const g=byId('groups',details.closest('[data-group]').dataset.group),d=groupDraft(g);holder.innerHTML=assetFields(d.assets[Number(holder.dataset.candidate)],{candidate:true,extraAssets:d.assets});holder.dataset.loaded='true';previewRelation(holder);if(holder.dataset.readonly==='true')holder.querySelectorAll('input:not(.kw-option-search),textarea,select').forEach(x=>x.disabled=true);}
  function captureGroups(){for(const group of $$('[data-group]')){const g=byId('groups',group.dataset.group),d=groupDraft(g);for(const holder of group.querySelectorAll('[data-candidate][data-loaded]'))d.assets[Number(holder.dataset.candidate)]=readAsset(holder,d.assets[Number(holder.dataset.candidate)]);d.reason=group.querySelector('[data-group-reason]').value;}}
  function referenceSelector(a,others){const key=uid(),selected=new Set(a.refs||[]),items=[...others,...(a.refs||[]).filter(id=>!others.some(x=>x.id===id)).map(id=>({id,name:nameOf(id),kind:'',domain:tr('待定位引用')}))];refPools.set(key,{items,selected,query:'',limit:100});return `<details class="kw-multiselect" data-ref-pool="${key}"><summary>${say('这项定义依赖哪些内容？','Which items does this definition rely on?')} <span class="privacy kw-ref-count">${tr('已选 ')}${selected.size}${tr(' 项')}</span></summary><input class="kw-option-search" placeholder="${say('按名称查找','Find by name')}" aria-label="${say('查找依赖项','Find dependencies')}"><div class="kw-options"></div><div class="kw-reference-footer"></div></details>`;}
  function renderReferences(details){const p=refPools.get(details.dataset.refPool);if(!p)return;const matches=p.items.filter(x=>(x.name+' '+x.domain+' '+x.id).toLowerCase().includes(p.query));details.querySelector('.kw-options').innerHTML=matches.slice(0,p.limit).map(x=>`<label><input type="checkbox" data-ref="${esc(x.id)}" ${p.selected.has(x.id)?'checked':''} ${details.closest('[data-readonly="true"]')?'disabled':''}> ${esc(x.name)} <span class="privacy">${esc(kinds[x.kind]||'')} · ${esc(x.domain||'')}</span></label>`).join('')||tr('<p class="muted">没有匹配的可引用知识。</p>');details.querySelector('.kw-reference-footer').innerHTML=tr`<p class="privacy">显示 ${Math.min(matches.length,p.limit)} / ${matches.length} 项；未显示的已选引用仍保留。</p>${matches.length>p.limit?button(tr('显示更多引用'),'refs-more',`data-pool="${esc(details.dataset.refPool)}"`,'small'):''}`;details.querySelector('.kw-ref-count').textContent=tr('已选 ')+p.selected.size+tr(' 项');}
  function captureReference(el){if(!el.dataset.ref)return;const details=el.closest('[data-ref-pool]'),p=refPools.get(details?.dataset.refPool);if(p){el.checked?p.selected.add(el.dataset.ref):p.selected.delete(el.dataset.ref);details.querySelector('.kw-ref-count').textContent=tr('已选 ')+p.selected.size+tr(' 项');}}
  function domainField(value){
    const id='kw-domains-'+uid(), domains=[...new Set(S.assets.map(x=>x.domain).filter(Boolean))].sort();
    return `<label>${say('业务分类','Business area')}${mark(true)}<input data-field="domain" list="${id}" value="${esc(value)}" placeholder="${say('例如：投诉处理、车辆管理','Choose or enter a business domain')}"><datalist id="${id}">${options(domains.map(d=>[d,d]),'',null)}</datalist></label>`;
  }
  function allowedEnds(type,side,item){const rule=S.editor_contract?.ends?.[type];return !rule||rule[side].includes(item.kind);}
  function endpointLabel(item,duplicate=false){
    const origin=item.evidence?.[0];
    const source=origin?.source_id?byId('sources',origin.source_id)?.name:origin?.type==='manual'?say('人工说明','Operator statement'):'';
    const role=item.properties?.role||item.definition;
    return [item.name,kinds[item.kind],typeof role==='string'?role.slice(0,72):'',source,duplicate?item.id:''].filter(Boolean).join(' · ');
  }
  function endpointCreator(key,side,type){
    return `<details data-end-create="${key}" ${allowedEnds(type,side,{kind:'entity'})?'':'hidden'}><summary>${say('找不到？新建对象','Missing an object? Add it')}</summary><label>${say('新对象名称','New object name')}<input data-end-name></label>${button(say('创建草稿并选用','Create draft and select'),'add-end',`data-side="${key}"`,'small')}</details>`;
  }
  function previewRelation(form){
    const result=form.querySelector('[data-relation-preview]');
    if(!result)return;
    const from=form.querySelector('[data-field="from"]').value,to=form.querySelector('[data-field="to"]').value;
    const verb=form.querySelector('[data-field="predicate"]').value.trim();
    const label=id=>asset(id)?.name||[...form.querySelector('[data-field="from"]').options].find(o=>o.value===id)?.text||id;
    result.textContent=[from?label(from):say('起点','From'),verb||say('关系','relationship'),to?label(to):say('终点','To')].join(' → ');
  }
  function updateEnds(container){
    const type=container.querySelector('[data-field="relation_type"]')?.value;
    const broad=container.querySelector('[data-all-ends]')?.checked??true;
    const query=container.querySelector('[data-end-search]')?.value.trim().toLowerCase()||''; const toggle=container.querySelector('[data-end-toggle]');if(toggle)toggle.hidden=type!=='business';
    ['from','to'].forEach((key,side)=>{const el=container.querySelector('[data-field="'+key+'"]');if(!el)return;
      const create=container.querySelector('[data-end-create="'+key+'"]');if(create)create.hidden=!allowedEnds(type,side,{kind:'entity'});
      for(const opt of el.options){const k=opt.dataset.kind;if(!k)continue;opt.disabled=!allowedEnds(type,side,{kind:k})||(type==='business'&&!broad&&['dataset','field'].includes(k));opt.hidden=opt.disabled||(!opt.selected&&!!query&&!opt.text.toLowerCase().includes(query));}
      if(el.selectedOptions[0]?.disabled)el.value='';
    });
    previewRelation(container);
  }
  function assetFields(a,{candidate=false,extraAssets=[],allowNewEnds=false}={}) {
    const p=a.properties||{},kind=a.kind||'entity',pool=[...new Map([...S.assets,...extraAssets].filter(x=>x.id).map(x=>[x.id,x])).values()],others=pool.filter(x=>x.id!==a.id&&x.status!=='retired');
    const endpoints=['relation','mapping'].includes(kind)?others.filter(x=>!['relation','mapping'].includes(x.kind)||[a.from,a.to].includes(x.id)):[];
    const names=new Set(),duplicate=new Set();
    for(const x of endpoints){if(names.has(x.name))duplicate.add(x.name);else names.add(x.name);}
    const ends=endpoints.map(x=>[x.id,endpointLabel(x,duplicate.has(x.name)),x.kind]);[a.from,a.to].filter(Boolean).forEach(id=>{if(!ends.some(x=>x[0]===id))ends.push([id,nameOf(id)]);});
    const reltype=a.relation_type||(kind==='mapping'?'maps_to':'business');
    const broad=ends.some(([id,,k])=>[a.from,a.to].includes(id)&&['dataset','field'].includes(k));
    const endOptions=(side,value)=>options([],'')+ends.map(([id,name,k])=>`<option value="${esc(id)}" data-kind="${esc(k)}" ${id===value?'selected':''} ${(k&&!allowedEnds(reltype,side,{kind:k})||reltype==='business'&&!broad&&['dataset','field'].includes(k))?'hidden disabled':''}>${esc(name)}</option>`).join('');
    const linked=['relation','mapping'].includes(kind);
    const onlyForEditor=allowNewEnds;
    const more=say('更多设置','More options');
    const typeSelect=`<label>${say('类型','Type')}<select data-field="kind" ${a.id?'disabled':''}>${options(Object.entries(kinds),kind,null)}</select></label>`;
    const alias=field(tr('别名（用逗号分隔）'),'aliases',(a.aliases||[]).join('，'));
    const coreName=linked&&onlyForEditor
      ? `<label>${say('单独给关系命名（选填）','Separate relationship name (optional)')}<input data-field="name" data-use-predicate placeholder="${say('默认使用关系动词','Defaults to the relationship verb')}" value="${esc(a.name)}"></label>`
      : field(say('名称','Name'),'name',a.name);
    const end=(key,side)=>`<div class="kw-endpoint"><label>${side?say('终点对象','To object'):say('起点对象','From object')}${mark(false)}<select required data-field="${key}">${endOptions(side,a[key])}</select></label>${allowNewEnds?endpointCreator(key,side,reltype):''}</div>`;
    const typeSettings=`<label>${say('关系类型','Relationship type')}<select required data-field="relation_type">${options(Object.entries(relationTypes),reltype,null)}</select></label><label data-end-toggle ${reltype!=='business'?'hidden':''}><span><input type="checkbox" data-all-ends ${broad?'checked':''}> ${say('可连接数据库表和字段','Include database tables and fields')}</span></label>`;
    const relationship=linked?`<div class="kw-relation-fields">${end('from',0)}<label>${say('它们是什么关系？','How are they related?')}${mark(false)}<input required data-field="predicate" placeholder="${say('例如：负责整改','e.g. resolves')}" value="${esc(a.predicate)}"></label>${end('to',1)}</div>
      <div class="kw-relation-readback"><output data-relation-preview aria-live="polite"></output>${button(say('交换两端','Swap ends'),'swap-ends','','small')}</div>
      ${ends.length>24?`<label class="kw-end-search">${say('查找两端可选的对象','Filter available objects')}<input type="search" data-end-search placeholder="${say('按名称、角色或来源查找','Search name, role or source')}"></label>`:''}
      <div data-physical ${reltype==='physical_fk'?'':'hidden'}><p class="privacy">${say('两端字段都要填写。按外键顺序填写字段名，用逗号分隔。','Both field lists are required. List foreign key fields in order, separated by commas.')}</p><div class="grid cols2">${field(tr('起点字段'),'properties.from_fields',(p.from_fields||[]).join('，'))}${field(tr('终点字段'),'properties.to_fields',(p.to_fields||[]).join('，'))}</div></div>`:'';
    const properties=(propertyFields[kind]||[]).map(([key,label])=>field(label,'properties.'+key,Array.isArray(p[key])?p[key].join('，'):p[key]??'',!['unit','value_type','source','column'].includes(key),(S.editor_contract?.confirm_fields?.[kind]||[]).includes(key))).join('');
    const details=`<div class="grid cols2">${domainField(a.domain)}${scopeFields(a.scope)}</div><div class="kw-property-fields">${properties}</div>`;
    const needsReview=p.assertion_basis==='model_inferred'||(Array.isArray(p.unresolved_conflicts)?p.unresolved_conflicts.length:!!p.unresolved_conflicts);
    const extras=`${typeSelect}${linked?typeSettings:''}${linked&&onlyForEditor?coreName:''}${alias}${needsReview?'':reviewFields(p)}${field(say('待核对的问题（每行一项）','Open questions (one per line)'),'properties.knowledge_gaps',(p.knowledge_gaps||[]).join('\n'),true)}${referenceSelector(a,others)}
      <details><summary>${say('生效和截止日期','Effective dates')}</summary><div class="grid cols2">${field(tr('生效日期'),'effective_from',a.effective_from)}${field(tr('截止日期'),'effective_to',a.effective_to)}</div></details>`;
    return `${linked&&onlyForEditor?'':coreName}${relationship}${field(say('业务说明','Description'),'definition',a.definition,true)}
      <details class="kw-form-section" data-confirm-fields ${a.id||!onlyForEditor?'open':''}><summary>${say('适用范围与业务口径','Scope and business details')}</summary>${details}</details>
      ${needsReview?reviewFields(p):''}
      <details class="kw-form-section" data-extra-settings ${onlyForEditor?'':'open'}><summary>${more}</summary>${extras}</details>`;
  }
  function readAsset(container,original,strict=true){const a=copy(original||{});if(!container||!container.querySelector('[data-field]'))return a;a.properties={...(a.properties||{})};container.querySelectorAll('[data-field]').forEach(el=>{const key=el.dataset.field;if(key==='properties.knowledge_gaps'){const gaps=[...new Set(el.value.split(/\r?\n/).map(x=>x.trim()).filter(Boolean))];if(gaps.length)a.properties.knowledge_gaps=gaps;else delete a.properties.knowledge_gaps;}else if(['properties.from_fields','properties.to_fields'].includes(key)){if(el.value.trim())a.properties[key.slice(11)]=el.value.split(/[,，]/).map(x=>x.trim()).filter(Boolean);else delete a.properties[key.slice(11)];}else if(key==='properties.assertion_basis'&&!el.value)delete a.properties.assertion_basis;else if(key.startsWith('properties.'))a.properties[key.slice(11)]=el.value.trim();else if(key==='aliases')a.aliases=el.value.split(/[,，\n]/).map(x=>x.trim()).filter(Boolean);else a[key]=el.value.trim();});if(!a.name&&container.querySelector('[data-use-predicate]'))a.name=a.predicate||'';if(original?.scope&&typeof original.scope==='object')a.scope=readScope(container,original.scope,strict);const decision=container.querySelector('[data-conflict-decision]')?.value.trim();if(decision&&a.properties.unresolved_conflicts){a.properties.conflict_resolutions=[...(a.properties.conflict_resolutions||[]),{previous:a.properties.unresolved_conflicts,decision}];delete a.properties.unresolved_conflicts;a.evidence=[...(a.evidence||[]),{type:'manual',actor:'local',quote:decision}];}const refPool=container.querySelector('[data-ref-pool]');a.refs=refPool?[...(refPools.get(refPool.dataset.refPool)?.selected||[])]:[...container.querySelectorAll('[data-ref]:checked')].map(el=>el.dataset.ref);return a;}

  function reviewPrompt(){
    const event=S.change_events?.at(-1),step=event?.guidance;
    if(!step)return '';
    const issue=step.attention;
    if(!issue && step.next_action!=='choose_business_question_or_export')return '';
    if(!issue)return '<p class="notice">'+say('结构草稿已保存。现在可以导出，或告诉 Agent 你希望这张图解释哪个业务问题。','Structure saved. Export this draft or tell your Agent which business question it should explain.')+'</p>';
    const labels={conflicting_sources:['两份依据的口径是否适用于同一范围？','Do the competing definitions apply to the same scope?'],confirm_inference:['哪份业务材料或人工观察支持这条推断？','Which source or operator observation supports this inference?'],source_changed:['依据已变，原定义仍然适用吗？','Does the definition still apply after the source change?'],missing_evidence:['还缺哪项业务依据？','Which business evidence is missing?'],review_relationship:['两侧记录如何配对，会重复累计吗？','How are the records joined, and can that duplicate counts?']};
    const target=asset(issue.asset_id);
    return '<div class="notice" role="status"><b>'+esc(say(...(labels[issue.kind]||labels.missing_evidence)))+'</b> '+esc(issue.detail||'')+' '+(target?button(esc(target.name),'locate-change',`data-id="${esc(target.id)}"`,'small'):'')+'</div>';
  }
  function graphToolbar(){
    const graph=G.mode==='graph',searchId=G.expanded?'kw-canvas-search':'kw-graph-search';
    const filters=[G.domain,G.kind,G.status].filter(Boolean).length;
    return `<div class="toolbar kw-editor-tools"><div class="kw-tool-group">
      ${button(say('新建对象','New object'),'create','data-kind="entity"','primary')}
      ${graph?button(say('连线','Connect'),'connect',`aria-pressed="${!!connection}"`):button(say('新建关系','New relation'),'create','data-kind="relation"')}
      <details class="kw-tool-menu"><summary>${say('更多类型','More types')}</summary><div class="kw-tool-menu-panel">
      ${['relation','rule','metric','term','attribute','dataset','field','mapping'].map(k=>button(esc(kinds[k]),'create',`data-kind="${k}"`,'quiet')).join('')}</div></details></div>
      <input type="search" id="${searchId}" value="${esc(G.query)}" placeholder="${say('搜索名称或关键词','Search names or keywords')}" aria-label="${say('搜索图谱','Search graph')}">
      <details class="kw-tool-menu"><summary>${say('筛选','Filters')}<span id="kw-filter-count">${filters?' · '+filters:''}</span></summary><div class="kw-tool-menu-panel">
      <label>${say('业务域','Domain')}<select id="kw-domain">${options([...new Set(S.assets.map(a=>a.domain).filter(Boolean))].map(v=>[v,v]),G.domain,say('全部领域','All domains'))}</select></label>
      <label>${say('类型','Type')}<select id="kw-kind">${options(Object.entries(kinds),G.kind,say('全部类型','All types'))}</select></label>
      <label>${say('状态','Status')}<select id="kw-status">${options(['draft','confirmed','needs_review','retired'].map(v=>[v,statuses[v]]),G.status,say('全部在用项','All active'))}</select></label>
      ${button(say('清除筛选','Clear filters'),'clear-graph-filter','','quiet small')}</div></details>
      ${button(graph?say('看列表','List view'):say('看图','Graph view'),'toggle-view','','small')}</div>`;
  }
  function canvasTools(){
    return `<div class="toolbar kw-canvas-tools"><select id="kw-canvas-view" aria-label="${say('图上显示','Show on canvas')}">${options([['all',say('全部内容','Everything')],['business',say('业务对象和关系','Objects and relationships')],['rules',say('指标和规则','Metrics and rules')],['data',say('表和字段','Tables and fields')]],G.view,null)}</select>
      ${fieldIndex().foldable.size?button(say('展开字段','Show columns'),'toggle-fields',`aria-pressed="${G.fieldsExpanded}"`,'small'):''}<span class="spacer"></span><div class="kw-tool-group kw-zoom-tools">
      ${button('−','zoom',`data-delta="-0.15" aria-label="${say('缩小','Zoom out')}"`,'small')}<span class="kw-zoom-value" id="kw-zoom-value">100%</span>${button('＋','zoom',`data-delta="0.15" aria-label="${say('放大','Zoom in')}"`,'small')}</div>
      ${explorerLink(say('3D 关系图','3D connections'),G.focus||G.selected,null)}
      ${button(say('适应画布','Fit to view'),'fit-canvas','','small')}
      <div class="kw-tool-group kw-layout-tools">${button(tr('自动布局'),'arrange','','small')}
      <details class="kw-tool-menu"><summary aria-label="${say('布局选项','Layout options')}">▾</summary><div class="kw-tool-menu-panel">${button(say('撤销上次布局','Undo last layout'),'undo-layout',layoutUndo.length?'':'disabled','quiet small')}</div></details></div>
      ${button(G.expanded?say('退出全屏','Exit full screen'):say('全屏','Full screen'),'expand-canvas',`aria-expanded="${G.expanded}" aria-controls="kw-canvas"`,'small')}
      ${G.expanded?button(G.inspector?say('收起详情','Hide details'):say('显示详情','Show details'),'toggle-inspector','','small'):''}</div>`;
  }
  function connectionMessage(){
    if(!connection)return '';
    return connection.start?say('从「'+nameOf(connection.start)+'」连到哪里？点选终点。','Starting at “'+nameOf(connection.start)+'”. Choose the destination.'):say('先点起点，再点终点。','Choose the source, then the destination.');
  }
  function relationHintsPrompt(){
    if(!S.project_directory)return '';
    const sourceIds=new Set(S.sources.filter(s=>['ddl','metadata'].includes(s.format)).map(s=>s.id));
    const active=S.assets.filter(a=>a.status==='draft'||a.status==='confirmed');
    const physicalTables=new Set(active.filter(a=>a.kind==='dataset'&&a.evidence?.some(e=>sourceIds.has(e.source_id))).map(a=>a.id));
    const foreignKeys=active.filter(a=>a.kind==='relation'&&a.relation_type==='physical_fk'&&physicalTables.has(a.from)&&physicalTables.has(a.to));
    if(!physicalTables.size||foreignKeys.length*4>physicalTables.size)return '';
    const project=JSON.stringify(S.project_directory);
    const text=say(
      '请使用 ai-data-delivery 检查项目 '+project+'。将此项目路径用作 --project 的参数，运行 knowledge.py 的 relation-hints 子命令。列出值得核对的字段及依据。',
      'Use ai-data-delivery to check project '+project+'. Pass this project path to --project and run the knowledge.py relation-hints subcommand. List the fields and evidence worth reviewing.');
    return `<details class="kw-task"><summary>${say('查找可核对的关系线索','Find relationship leads to review')}</summary><textarea readonly aria-label="${say('关系核对指令','Relationship review prompt')}">${esc(text)}</textarea>${button(say('复制给 Agent','Copy for Agent'),'copy-relation-hints','','quiet small')}</details>`;
  }
  function graphPage(){
    const title=say('图谱编辑器','Graph editor');
    const head=`<header class="kw-editor-head"><h1>${title}</h1></header>`;
    if(!S.assets.length)return head+`<section class="card tool-empty"><h2>${say('从哪里开始？','Where would you like to start?')}</h2><p>${say('可以导入已有的表和字段，也可以先画一个业务对象。','Import existing tables and fields, or add your first business object.')}</p><div class="row">${button(say('新建对象','New object'),'create','data-kind="entity"','primary')}${button(say('导入 SQL 或文档','Import SQL or documents'),'go','data-page="knowledge"')}${button(say('连接数据库','Connect a database'),'go','data-page="connections"')}</div></section>`;
    const graph=G.mode==='graph',revisionNote=requestedRevision&&String(S.revision)!==requestedRevision?say('链接指向版本','Linked revision')+' '+requestedRevision+' · '+say('当前版本','Current revision')+' '+S.revision:'';
    return head+(revisionNote?'<p class="notice">'+esc(revisionNote)+'</p>':'')+(missingFocus?'<p class="notice" role="status">'+esc(say('没找到这个对象，已显示全图。','This object could not be found. Showing the full graph.'))+' '+esc(missingFocus)+'</p>':'')+
      (S.change_events?.at(-1)?.guidance?.attention?reviewPrompt():'')+(G.expanded?'':relationHintsPrompt())+`<div class="kw-graph-layout ${G.expanded&&graph?'kw-canvas-expanded':''} ${G.inspector?'kw-inspector-visible':''}"><section class="kw-graph-main">${graphToolbar()}${graph?canvasTools()+
      `<div class="kw-connect-hint" id="kw-connect-hint" ${connection?'':'hidden'} role="status"><span id="kw-connect-message">${esc(connectionMessage())}</span> ${button(say('取消','Cancel'),'cancel-connect','','quiet small')}</div>
      <div class="kw-canvas ${connection?'is-connecting':''}" id="kw-canvas"><svg id="kw-graph" aria-label="${say('图谱，使用 Tab 选择对象或连线','Graph, use Tab to reach objects and relationships')}"></svg></div>
      <div class="graph-hint"><span id="kw-graph-count" class="privacy"></span><span class="kw-graph-legend"><span><i class="kw-legend-line"></i>${say('关系','Relationship')}</span><span><i class="kw-legend-line reference"></i>${say('引用','Reference')}</span></span></div>`:'<div id="kw-asset-table"></div>'}
      <div class="kw-more">${G.focus?button(say('返回全图','Back to full graph'),'clear-focus','','quiet small'):''}${button(say('显示更多','Show more'),'more','','quiet small')}${button(say('清空搜索和筛选','Clear search and filters'),'clear-graph-filter','id="kw-clear-search" hidden','quiet small')}</div>
      ${latestDelta?.items.some(a=>!['dataset','field'].includes(a.kind)&&a.relation_type!=='physical_fk')?changeLinks(latestDelta):''}</section><aside class="kw-inspector" id="kw-inspector"></aside></div>
      ${S.problems.length?'<details><summary>'+say('待核对的问题','Items to review')+' ('+S.problems.length+')</summary><div class="card" id="kw-problems">'+problemsHtml()+'</div></details>':''}`;
  }
  function filteredAssets(){let list=S.assets.filter(a=>(!G.domain||a.domain===G.domain)&&(!G.kind||a.kind===G.kind)&&(G.status?a.status===G.status:a.status!=='retired'));const allowed={business:['entity','term','attribute','relation'],rules:['entity','term','metric','rule','relation','attribute'],data:['entity','attribute','dataset','field','mapping','relation'],all:Object.keys(kinds)}[G.view];list=list.filter(a=>allowed.includes(a.kind)&&(!['business','rules'].includes(G.view)||a.relation_type!=='physical_fk'));if(G.query){const q=G.query.toLowerCase();list=list.filter(a=>semanticSearchText(a).includes(q));}if(G.focus){const ids=new Set([G.focus]);S.assets.forEach(a=>{if(a.from===G.focus||a.to===G.focus){ids.add(a.id);ids.add(a.from);ids.add(a.to);}if(a.id===G.focus){[a.from,a.to,...(a.refs||[])].filter(Boolean).forEach(x=>ids.add(x));}if((a.refs||[]).includes(G.focus))ids.add(a.id);});list=list.filter(a=>ids.has(a.id));}return list;}
  function currentLayout(){const positions=copy(S.layout);graphData().nodes.forEach((a,i)=>{positions['semantic:'+G.view+':'+a.id]={...point(a,i)};});return positions;}
  function defaultPoint(index){return {x:40+(index%3)*COLUMN_STEP,y:40+Math.floor(index/3)*ROW_STEP};}
  function point(a,index){return S.layout['semantic:'+G.view+':'+a.id]||virtualPositions[a.id]||defaultPoint(index);}
  let fieldCache=null;
  function fieldIndex(){
    if(fieldCache?.state===S)return fieldCache;
    const active=S.assets.filter(a=>a.status!=='retired'),tables=new Set(active.filter(a=>a.kind==='dataset').map(a=>a.id));
    const byTable=new Map(),foldable=new Set();
    const linked=new Set();
    for(const item of active){
      if(item.relation_type==='physical_fk'||['dataset','field'].includes(item.kind))continue;
      for(const ref of [item.from,item.to,...(item.refs||[])])if(ref)linked.add(ref);
    }
    for(const field of active){
      if(field.kind!=='field')continue;
      const owners=(field.refs||[]).filter(id=>tables.has(id));
      for(const owner of owners){if(!byTable.has(owner))byTable.set(owner,[]);byTable.get(owner).push(field);}
      if(owners.length===1&&field.refs.length===1&&!linked.has(field.id))foldable.add(field.id);
    }
    return fieldCache={state:S,byTable,foldable};
  }
  function tableFields(id){return fieldIndex().byTable.get(id)||[];}
  function fieldDetailRequested(){return !!(G.focus||G.query||G.kind||G.domain||G.status);}
  function graphData(){
    const pool=filteredAssets(),fold=(!G.fieldsExpanded&&!fieldDetailRequested())?fieldIndex().foldable:null;
    const matched=fold?pool.filter(a=>!fold.has(a.id)):pool;
    if(G.view==='all'&&matched.length>G.limit){
      // Reserve one place per kind so paging through fields cannot conceal tables or metrics.
      const firstByKind=new Map();
      for(const a of matched)if(!firstByKind.has(a.kind))firstByKind.set(a.kind,a.id);
      const representatives=new Set(firstByKind.values());
      matched.sort((a,b)=>Number(representatives.has(b.id))-Number(representatives.has(a.id)) || Number(a.kind==='field')-Number(b.kind==='field'));
    }
    if(G.focus)matched.sort((a,b)=>Number(b.id===G.focus)-Number(a.id===G.focus));
    const visible=matched.slice(0,G.limit),ids=new Set(visible.map(a=>a.id));
    const edges=matched.filter(a=>['relation','mapping'].includes(a.kind)&&(ids.has(a.id)||(ids.has(a.from)&&ids.has(a.to))))
      .sort((a,b)=>Number(ids.has(b.id))-Number(ids.has(a.id))).slice(0,G.limit);
    edges.forEach(e=>{[e.from,e.to].forEach(id=>{if(id)ids.add(id);});});
    return {matched,foldedCount:pool.length-matched.length,nodes:S.assets.filter(a=>ids.has(a.id)&&!['relation','mapping'].includes(a.kind)),edges};
  }
  function graphInput(data){
    const nodes=data.nodes.map(a=>({id:a.id,width:NODE_WIDTH,height:NODE_HEIGHT}));
    const ids=new Set(nodes.map(n=>n.id)),pairs=new Set(),edges=[];
    const pair=(a,b)=>JSON.stringify([a,b].sort());
    for(const e of data.edges){if(!ids.has(e.from)||!ids.has(e.to))continue;edges.push({id:e.id,from:e.from,to:e.to,label:e.predicate||relationTypes[e.relation_type]||tr('待定义'),reference:false});pairs.add(pair(e.from,e.to));}
    for(const a of data.nodes)for(const id of a.refs||[]){if(id===a.id||!ids.has(id)||pairs.has(pair(a.id,id)))continue;pairs.add(pair(a.id,id));edges.push({id:'$ref:'+a.id+':'+id,from:a.id,to:id,label:'',reference:true});}
    return {nodes,edges};
  }
  function diagramKey(input){return JSON.stringify([S.project_id,G.view,input]);}
  function positionSignature(input,positions){return JSON.stringify(['0.2.2',input,positions]);}
  function cachePlan(input,plan){
    const signature=positionSignature(input,plan.positions);routedPlans.set(signature,plan);
    if(routedPlans.size>12)routedPlans.delete(routedPlans.keys().next().value);
    try{localStorage.setItem('kw-routes:'+S.project_id+':'+G.view,JSON.stringify({signature,plan}));}catch(_){}
  }
  function checkedPlan(plan,input){
    const finite=p=>p&&Number.isFinite(p.x)&&Number.isFinite(p.y)&&Math.max(Math.abs(p.x),Math.abs(p.y))<100000;
    return plan&&input.nodes.every(n=>finite(plan.positions?.[n.id]))&&input.edges.every(e=>{
      const r=plan.routes?.[e.id],l=r?.label;
      return r&&r.points?.length>=2&&r.points.every(finite)&&(!l||(finite(l)&&Number.isFinite(l.width)&&Number.isFinite(l.height)&&l.text===e.label&&l.lines?.join('')===e.label.replace(/\n/g,'')));
    })&&['left','top','right','bottom'].every(k=>Number.isFinite(plan.bounds?.[k]));
  }
  function routesFor(input,positions){
    const signature=positionSignature(input,positions);if(routedPlans.has(signature))return routedPlans.get(signature);
    try{const saved=JSON.parse(localStorage.getItem('kw-routes:'+S.project_id+':'+G.view)||'null');if(saved?.signature===signature&&checkedPlan(saved.plan,input)){routedPlans.set(signature,saved.plan);return saved.plan;}}catch(_){}
    if(denseGraph(input))return window.SemanticGraphLayout.overview({...input,positions});
    const result=window.SemanticGraphLayout.route({...input,positions});routedPlans.set(signature,result);return result;
  }
  async function arrangeGraph(save=true,routeOnly=false){
    if(layoutPending)return;const data=graphData(),input=graphInput(data),key=diagramKey(input),canvas=$('#kw-canvas');
    if(!input.nodes.length)return;
    if(!window.SemanticGraphLayout)throw Error(tr('布局组件未加载，请刷新工作台后重试。'));
    const before=currentLayout(),positions=Object.fromEntries(data.nodes.map((a,i)=>[a.id,point(a,i)]));
    layoutPending=true;layoutButton();
    try{
      const plan=await runLayout({...input,width:canvas?.clientWidth||1000,height:canvas?.clientHeight||600,positions,fixed:G.fixed},key,routeOnly);
      if(!plan)return;
      if(activePage!=='graph'||diagramKey(graphInput(graphData()))!==key){C.notify(tr('图谱范围已变化，本次布局未应用。'));return;}
      if(save){const next=copy(S.layout);for(const [id,pos] of Object.entries(plan.positions))next['semantic:'+G.view+':'+id]=pos;await C.api('layout',{positions:next});S.layout=next;layoutUndo.push(before);}
      automaticPlans.set(key,plan);virtualPositions=plan.positions;cachePlan(input,plan);graphPlan=plan;drawGraph(true);
      if(save)C.notify(tr('自动布局已保存；知识定义与关系保持不变。'));
    }finally{layoutPending=false;layoutButton();if(activePage==='graph'&&diagramKey(graphInput(graphData()))!==key)drawGraph();}
  }
  function edgePath(points){return points.map((p,i)=>(i?'L':'M')+Number(p.x)+','+Number(p.y)).join(' ');}
  function graphEdges(edges,plan,labels=false){
    const selected=asset(G.selected)?G.selected:null,active=e=>selected&&(e.id===selected||e.from===selected||e.to===selected);
    return [...edges.filter(e=>!active(e)),...edges.filter(active)].map(e=>{
      const r=plan.routes[e.id];if(!r)return '';
      const a=asset(e.id),tone=a?.status==='needs_review'?'review':active(e)?'focus':'normal';
      const attrs=e.reference?'':`data-kw-edge="${esc(e.id)}" ${labels?'aria-hidden="true"':'tabindex="0" role="button" aria-label="'+esc(nameOf(e.from)+' → '+e.label+' → '+nameOf(e.to))+'"'}`;
      const cls=`kw-edge-group ${e.reference?'reference':''} ${active(e)?'related':selected?'dimmed':''} ${selected===e.id?'selected':''}`;
      if(labels){const l=r.label;if(!l)return '';return `<g class="${cls}" ${attrs} data-render-edge="${esc(e.id)}"><g class="kw-edge-label">${l.leader?`<path class="kw-label-leader" d="${edgePath(l.leader)}"/>`:''}<rect x="${l.x}" y="${l.y}" width="${l.width}" height="${l.height}" rx="4"/><text x="${l.x+l.width/2}" y="${l.y+17}" text-anchor="middle">${(l.lines||[l.text]).map((line,i)=>`<tspan x="${l.x+l.width/2}" dy="${i?17:0}">${esc(line)}</tspan>`).join('')}</text><title>${esc(nameOf(e.from)+' → '+e.label+' → '+nameOf(e.to))}</title></g></g>`;}
      return `<g class="${cls}" ${attrs} data-render-edge="${esc(e.id)}"><path class="kw-edge-hit" d="${edgePath(r.points)}"/><path class="${e.reference?'kw-ref-edge':'kw-edge'} ${tone}" d="${edgePath(r.points)}" marker-end="url(#kw-arrow-${e.reference?'reference':tone})"/><title>${esc(nameOf(e.from)+' → '+(e.label||tr('定义引用'))+' → '+nameOf(e.to))}</title></g>`;
    }).join('');
  }
  function nodeNameLines(name){
    const width=text=>Array.from(text).reduce((n,c)=>n+(c.codePointAt(0)>255?14:7),0),parts=String(name).match(/[^\s\u3400-\u9fff]+\s*|[\u3400-\u9fff]/gu)||[],lines=[];let line='';
    for(const part of parts){if(line&&width(line+part)>146){lines.push(line.trim());line='';}for(const char of part){if(width(line+char)>146){lines.push(line.trim());line='';}line+=char;}}
    if(line.trim())lines.push(line.trim());if(lines.length>2){lines[1]=Array.from(lines[1]).slice(0,-1).join('')+'…';lines.length=2;}return lines.length?lines:[''];
  }
  function nodeDisplayLines(a){
    const p=a.properties||{},table=p.metadata_table,column=p.column;
    // Catalog names include a shared connection prefix. Keep the distinguishing
    // column/table visible; full identity remains in the title and inspector.
    // Explicitly renamed display names keep their author's wording.
    const clip=(text,end=false)=>{let chars=Array.from(text);const width=()=>chars.reduce((n,c)=>n+(c.codePointAt(0)>255?14:7),0);if(width()<=146)return text;while(chars.length&&width()>132){if(end)chars.shift();else chars.pop();}return end?'…'+chars.join(''):chars.join('')+'…';};
    if(p.metadata_connection&&typeof table==='string'){
      if(a.kind==='field'&&typeof column==='string'&&a.name.endsWith('.'+column))return [clip(column),clip(table,true)];
      if(a.kind==='dataset'&&a.name.endsWith('.'+table))return nodeNameLines(table);
    }
    return nodeNameLines(a.name);
  }
  const origins={
    ddl:['SQL 表结构','SQL schema'],metadata:['数据库目录','Database catalog'],document:['业务材料','Document'],
    operator_statement:['人员说明','Explanation'],model_inferred:['Agent 推测','Agent suggestion'],
    mixed:['多种依据','Mixed'],unattributed:['待补依据','Unattributed']
  };
  function originLabel(a){const key=S.evidence_origins?.[a.id] || (a.properties?.assertion_basis==='model_inferred'?'model_inferred':'unattributed');return say(...(origins[key]||origins.unattributed));}
  function reviewFields(p){
    const conflicts=p.unresolved_conflicts;
    const hasConflicts=Array.isArray(conflicts)?conflicts.length>0:!!conflicts;
    const inferred=`<details class="kw-form-section" ${p.assertion_basis==='model_inferred'?'open':''}><summary>${say('需要验证的推测','Assumptions to check')}</summary><label>${say('这项判断的来源','Basis for this statement')}<select data-field="properties.assertion_basis">${options([['',say('来自原文或人员说明','Document or explanation')],['model_inferred',say('由 Agent 推测，仍需核对','Agent suggestion, pending review')]],p.assertion_basis||'',null)}</select></label></details>`;
    if(!hasConflicts)return inferred;
    return `<fieldset><legend>${say('材料里的说法不一致','Sources disagree')}</legend>${claimList(conflicts)}<label>${say('采用哪种说法？写明适用范围和理由','Which wording applies? Record its scope and your reason')}<textarea data-conflict-decision></textarea></label></fieldset>`+inferred;
  }
  function nodeMarkup(a,i){const p=point(a,i),lines=nodeDisplayLines(a),nodeKind=a.kind==='dataset'&&tableFields(a.id).length?(say('表 · ','Table · ')+tableFields(a.id).length+say(' 个字段',' columns')):({rule:tr('规则'),field:tr('字段')})[a.kind]||kinds[a.kind];
    return `<g data-kw-node="${esc(a.id)}" class="kw-node ${G.selected===a.id?'selected':''} ${connection?.start===a.id?'connection-start':''} kind-${esc(a.kind)} status-${esc(a.status)}" transform="translate(${p.x},${p.y})" tabindex="0" role="button" aria-label="${esc(a.name)}"><rect width="${NODE_WIDTH}" height="${NODE_HEIGHT}" rx="9"/><title>${esc(a.name+' · '+a.definition)}</title>${lines.map((line,j)=>`<text x="12" y="${lines.length>1?21+j*17:27}" class="kw-node-name">${esc(line)}</text>`).join('')}<text x="12" y="56">${esc(nodeKind)} · ${esc(statuses[a.status]||a.status)} · ${esc(originLabel(a))}${G.fixed.includes(a.id)?tr(' · 固定'):''}</text><circle class="kw-port" cx="${NODE_WIDTH}" cy="${NODE_HEIGHT/2}" r="5"/></g>`;
  }
  function drawGraph(fit=false){if(activePage!=='graph')return;const data=G.mode==='graph'?graphData():null,found=data?data.matched:filteredAssets(),more=$('[data-kw="more"]');if(more){more.disabled=found.length<=G.limit;more.hidden=more.disabled;}
    const reset=$('#kw-clear-search');if(reset)reset.hidden=!(G.query||G.kind||G.status||G.domain);
    const filterCount=$('#kw-filter-count'),count=[G.kind,G.status,G.domain].filter(Boolean).length;if(filterCount)filterCount.textContent=count?' · '+count:'';
    const undo=$('[data-kw="undo-layout"]');if(undo)undo.disabled=!layoutUndo.length;
    if(G.mode==='table'){
      const rows=found.slice(0,G.limit).map(a=>`<tr data-kw="select" data-id="${esc(a.id)}" tabindex="0" class="${G.selected===a.id?'selected':''}"><td><b>${esc(a.name)}</b><small>${esc(kinds[a.kind])}</small></td><td>${esc(a.domain)}<small>${esc(scopeText(a.scope))}</small></td><td>${esc(a.definition)}</td><td>${badge(a.status)}</td></tr>`).join('');
      $('#kw-asset-table').innerHTML=`<p class="privacy">${say('显示 '+Math.min(found.length,G.limit)+' / '+found.length+' 项','Showing '+Math.min(found.length,G.limit)+' of '+found.length+' items')}</p><table><thead><tr><th>${say('名称','Name')}</th><th>${say('业务分类与适用范围','Business area and scope')}</th><th>${say('业务说明','Description')}</th><th>${say('状态','Status')}</th></tr></thead><tbody>${rows}</tbody></table>${!found.length?empty(say('没有找到匹配的内容','No matches'),say('换个关键词，或清除筛选。','Try another keyword or clear the filters.')):''}`;
      return;
    }
    const svg=$('#kw-graph');if(!svg)return;
    const fieldToggle=$('[data-kw="toggle-fields"]');
    if(fieldToggle){
      const automatic=fieldDetailRequested(),expanded=automatic||G.fieldsExpanded;
      fieldToggle.hidden=!['all','data'].includes(G.view);
      fieldToggle.disabled=automatic;
      fieldToggle.textContent=automatic?say('已显示匹配字段','Matching columns shown'):expanded?say('收起字段','Hide columns'):say('展开字段','Show columns');
      fieldToggle.setAttribute('aria-pressed',String(expanded));
    }
    const {nodes,edges}=data,input=graphInput(data),key=diagramKey(input),canvas=$('#kw-canvas');
    virtualPositions=automaticPlans.get(key)?.positions||{};
    if(runningWorker&&runningWorker.key!==key)runningWorker.cancel();
    layoutButton();
    const savedPositions=nodes.some(n=>S.layout['semantic:'+G.view+':'+n.id]);
    if(nodes.length&&(!savedPositions||denseGraph(input))&&!automaticPlans.has(key)&&autoPendingKey!==key&&!layoutPending&&window.SemanticGraphLayout){autoPendingKey=key;arrangeGraph(false,savedPositions).catch(e=>C.notify(tr('自动布局未完成：')+e.message));}
    const positions=Object.fromEntries(nodes.map((a,i)=>[a.id,point(a,i)]));
    if(!window.SemanticGraphLayout){svg.innerHTML=tr('<text x="30" y="50">布局组件未加载，请刷新重试。</text>');return;}
    graphPlan=routesFor(input,positions);const bounds=graphPlan.bounds,padding=16,bw=Math.max(1,bounds.right-bounds.left),bh=Math.max(1,bounds.bottom-bounds.top);
    let readingAnchor;
    if(fit&&nodes.length&&canvas.clientWidth>0&&canvas.clientHeight>0){
      const fitZoom=Math.min(1.3,(canvas.clientWidth-padding*2)/bw,(canvas.clientHeight-padding*2)/bh);
      // Start a large diagram at a legible scale around an actual relationship.
      // The explicit Fit command still includes the entire displayed graph.
      if(!fitAllNodes&&nodes.length>=24&&fitZoom<0.85){
        readingAnchor=positions[G.selected]||positions[edges[0]?.from]||positions[nodes[0].id];
      }
      G.zoom=readingAnchor ? 0.85 : fitZoom;
      saveView();
    }
    const minX=Math.min(0,bounds.left),minY=Math.min(0,bounds.top),width=Math.max(bounds.right-minX,Math.max(1,canvas.clientWidth-2)/G.zoom),height=Math.max(bounds.bottom-minY,Math.max(1,canvas.clientHeight-2)/G.zoom);
    if(fit||plotOffset.key!==key)plotOffset={key,x:fit?(width-bw)/2-bounds.left:Math.max(0,-minX),y:fit?(height-bh)/2-bounds.top:Math.max(0,-minY)};
    const offsetX=plotOffset.x,offsetY=plotOffset.y;
    svg.setAttribute('viewBox',`0 0 ${width} ${height}`);svg.style.width=Math.floor(width*G.zoom)+'px';svg.style.height=Math.floor(height*G.zoom)+'px';
    svg.dataset.offsetX=offsetX;svg.dataset.offsetY=offsetY;
    const level=$('#kw-zoom-value');if(level)level.textContent=Math.round(G.zoom*100)+'%';
    if(fit){
      keepFitted=true;
      canvas.scrollLeft=readingAnchor?Math.max(0,(readingAnchor.x+offsetX+NODE_WIDTH/2)*G.zoom-canvas.clientWidth/2):0;
      canvas.scrollTop=readingAnchor?Math.max(0,(readingAnchor.y+offsetY+NODE_HEIGHT/2)*G.zoom-canvas.clientHeight/2):0;
    }
    const refs=input.edges.filter(e=>e.reference).length,active=S.assets.filter(a=>a.status!=='retired').length;
    const matches=found.length+data.foldedCount!==active?say(' · 匹配 ',' · Matching: ')+found.length:found.length>G.limit?say(' · 共 ',' · Total: ')+found.length+say(' 项',' items'):'';
    const tableOverview=data.foldedCount>0&&nodes.length>0&&nodes.every(a=>a.kind==='dataset')&&!fieldDetailRequested();
    const tableCount=tableOverview?found.filter(a=>a.kind==='dataset').length:0;
    const shown=tableOverview?say(`显示 ${nodes.length} / ${tableCount} 张表 · ${edges.length} 条关系`,`Showing ${nodes.length} of ${tableCount} tables · ${edges.length} relationships`):tr`${nodes.length} 个节点 · ${edges.length} 条关系${refs?' · '+refs+tr(' 项引用'):''}`+matches;
    $('#kw-graph-count').textContent=shown+(data.foldedCount?say(' · 已收起 ',' · Hidden: ')+data.foldedCount+say(' 个表字段',' table columns'):'');
    const markers=[['normal','#668f7b'],['focus','#176c56'],['review','#b9842e'],['reference','#a4b4aa']].map(([tone,color])=>`<marker id="kw-arrow-${tone}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="${color}"/></marker>`).join('');
    svg.innerHTML=`<defs>${markers}</defs><g class="kw-graph-content" transform="translate(${offsetX},${offsetY})">`+graphEdges(input.edges,graphPlan)+nodes.map(nodeMarkup).join('')+graphEdges(input.edges,graphPlan,true)+(!nodes.length?('<text x="24" y="46" class="kw-empty-graph">'+say('没有匹配的对象。试试其他关键词或清除筛选。','No matching objects. Try another search or clear filters.')+'</text>'):'')+'</g>';
  }
  let lastGraphClick=null;
  function activateGraphAsset(id){const now=Date.now(),double=lastGraphClick?.id===id&&now-lastGraphClick.time<450;lastGraphClick={id,time:now};if(double){lastGraphClick=null;openAsset(id);}else selectGraphAsset(id);}
  function selectGraphAsset(id){if(id&&G.query){locate(id);drawGraph(true);return;}const wasInspector=G.inspector;G.selected=id;G.inspector=!!id;saveView();if(G.expanded){rerender();if(wasInspector!==G.inspector)drawGraph(true);}else{$('.kw-graph-layout')?.classList.toggle('kw-inspector-visible',G.inspector);drawGraph();drawInspector();}const problems=$('#kw-problems');if(problems)problems.innerHTML=problemsHtml();}
  function claimList(value){
    const entries=Array.isArray(value)?value:Array.isArray(value?.claims)?value.claims:[value];
    return entries.filter(Boolean).map(item=>{
      if(Array.isArray(item?.claims))return claimList(item.claims);
      const source=item?.source_id&&byId('sources',item.source_id);
      const wording=typeof item==='string'?item:item.claim||item.quote||fmt(item);
      return `<div class="kw-claim">${source?`<b>${esc(source.name)}</b>`:''}<p>${esc(wording)}</p>${item.applicability?`<small>${esc(scopeText(item.applicability))}</small>`:''}</div>`;
    }).join('');
  }
  function displayTableFields(holder,table){
    const query=(holder.querySelector('[data-table-field-search]')?.value||'').trim().toLowerCase();
    const all=tableFields(table.id);
    const matched=all.filter(f=>(f.name+' '+(f.properties?.column||'')).toLowerCase().includes(query));
    const limit=Number(holder.dataset.limit||12);
    holder.querySelector('[data-table-field-rows]').innerHTML=matched.slice(0,limit).map(f=>{
      const name=f.properties?.column||f.name, type=f.properties?.raw_type||f.properties?.value_type||'';
      return button(`<span>${esc(name)}</span><small>${esc(type)}</small>`,'locate-change',`data-id="${esc(f.id)}"`,'kw-table-field');
    }).join('')||`<p class="muted">${say('没有匹配的字段','No matching fields')}</p>`;
    const more=holder.querySelector('[data-kw="more-table-fields"]');
    more.hidden=matched.length<=limit;
    more.textContent=say('再看 ','Show ')+Math.min(12,Math.max(0,matched.length-limit))+say(' 个字段',' more fields');
  }
  function drawInspector(){
    const el=$('#kw-inspector');if(!el)return;
    const a=asset(G.selected);
    if(!a){
      el.innerHTML=`<h2>${say('查看详情','Details')}</h2><p class="sub">${connection?say('依次点选要连接的两个对象。','Select the two objects to connect, in order.'):say('点一个对象或一条线，查看它的含义和原文。','Select an object or a line to see its meaning and source.')}</p>`;
      return;
    }
    const incoming=S.assets.filter(x=>x.from===a.id||x.to===a.id||(x.refs||[]).includes(a.id));
    const fields=a.kind==='dataset'?tableFields(a.id):[];
    const fieldIds=new Set(fields.map(x=>x.id));
    const refs=incoming.filter(x=>!fieldIds.has(x.id));
    const p=a.properties||{},meta=[a.domain,scopeText(a.scope||'')].filter(Boolean);
    const details=(propertyFields[a.kind]||[]).filter(([key])=>p[key]!==undefined&&p[key]!=='');
    const gaps=p.knowledge_gaps||[];
    let keySummary='';
    if(a.kind==='dataset'&&Array.isArray(p.primary_key)){
      const columns=p.primary_key;
      const label=p.primary_key_invalid?say('主键声明有误，请核对建表原文','Invalid primary key declaration; check the source SQL')
        : columns.length ? (columns.length>1?say('联合主键','Composite primary key'):say('主键','Primary key'))+' · '+columns.join(' + ')
        : p.columns_complete===false?say('表结构未读全，主键待核对','Partial table structure; check the primary key')
        : say('来源未声明主键','No primary key declared in the source');
      keySummary='<p class="privacy">'+esc(label)+'</p>';
    }
    const listFields=fields.length?`<section class="kw-table-fields" data-table-fields><h3>${say('表字段','Table columns')} · ${fields.length}</h3>
      ${fields.length>12?`<input type="search" data-table-field-search aria-label="${say('查找表字段','Find a column')}" placeholder="${say('输入字段名','Filter by column name')}">`:''}
      <div data-table-field-rows></div>${button(say('查看更多字段','More columns'),'more-table-fields','','quiet small')}</section>`:'';
    const disagreements=p.unresolved_conflicts&&(Array.isArray(p.unresolved_conflicts)?p.unresolved_conflicts.length:true);
    const id=`data-id="${esc(a.id)}"`;
    el.innerHTML=`<span class="eyebrow">${esc(kinds[a.kind])}</span><div class="row between"><h2>${esc(a.name)}</h2>${badge(a.status)}</div>
      ${a.from?`<div class="kw-relation-readback">${esc(nameOf(a.from))} → ${esc(a.predicate)} → ${esc(nameOf(a.to))}</div>`:''}
      ${a.definition?`<p class="kw-definition">${esc(a.definition)}</p>`:''}${meta.length?`<p class="privacy">${esc(meta.join(' · '))}</p>`:''}
      <div class="row">${button(say('编辑','Edit'),'edit',id,'primary small')}${button(say('只看相关项','Show connections'),'focus',id,'small')}</div>
      ${keySummary}${listFields}${details.length?`<dl class="kw-properties">${details.map(([key,label])=>`<dt>${esc(label)}</dt><dd>${esc(fmt(p[key]))}</dd>`).join('')}</dl>`:''}
      ${disagreements?`<h3>${say('待核对的说法','Claims to review')}</h3>${claimList(p.unresolved_conflicts)}`:''}
      ${Array.isArray(p.conflict_resolutions)&&p.conflict_resolutions.length?`<h3>${say('已采用的说法','Recorded decisions')}</h3>${p.conflict_resolutions.map(r=>`<p>${esc(r?.decision||fmt(r))}</p>`).join('')}`:''}
      ${gaps.length?`<h3>${say('还需要核对','Open questions')}</h3><p>${esc(fmt(gaps))}</p>`:''}
      <h3>${say('依据','Evidence')}${a.evidence?.length?' · '+esc(originLabel(a)):''}</h3>
      ${a.evidence?.length?evidenceHtml(a.evidence):`<p class="muted">${say('确认前，点“编辑”引用原文或补一条说明。','Before confirming, choose Edit to add a quotation or an explanation.')}</p>`}
      ${a.status==='needs_review'?button(say('核对更新后的材料','Review updated source'),'review-source',id,'primary small'):''}
      ${refs.length?`<details><summary>${say('引用这项内容的地方','Used by')} · ${refs.length}</summary>${refs.map(r=>button(esc(r.name||r.predicate),'select',`data-id="${esc(r.id)}"`,'quiet small')).join('')}</details>`:''}
      <details class="kw-inspector-more"><summary>${say('更多信息和操作','More details and actions')}</summary>
        <p class="privacy">${say('标识','ID')} · ${esc(a.id)}</p>${a.aliases?.length?`<p>${say('别名','Aliases')} · ${esc(a.aliases.join('、'))}</p>`:''}
        ${Object.keys(p).length?`<details><summary>${say('查看全部属性','View all properties')}</summary><dl class="kw-properties">${Object.entries(p).map(([k,v])=>`<dt>${esc((propertyFields[a.kind]||[]).find(row=>row[0]===k)?.[1]||k)}</dt><dd>${esc(fmt(v))}</dd>`).join('')}</dl></details>`:''}
        ${(S.separations||[]).filter(x=>x.left_id===a.id||x.right_id===a.id).map(x=>`<p>${say('已与以下同名项区分','Distinct from')} · ${esc(nameOf(x.left_id===a.id?x.right_id:x.left_id))}<br>${esc(x.reason)}</p>`).join('')}
        <div class="row kw-maintenance">${button(G.fixed.includes(a.id)?tr('取消固定'):tr('固定位置'),'fix',id,'small')}${button(say('处理同名项','Review matching names'),'resolve-identity',id,'small')}${button(a.status==='draft'?tr('删除草稿'):tr('停用'),'retire',id,'danger small')}</div>
      </details>`;
    if(fields.length)displayTableFields(el.querySelector('[data-table-fields]'),a);
  }
  function problemsHtml(){let p=S.problems||[];if(G.selected)p=p.filter(x=>[x.asset_id,x.id,...(x.asset_ids||[])].includes(G.selected));return p.length?p.map(x=>{const id=x.asset_id||x.asset_ids?.[0]||x.target_id;return `<div class="gap"><div><h3>${esc(x.message||x.detail||x.title||x.code||tr('需核对'))}</h3><p>${esc(x.next||x.reason||tr('请查看相关定义与原文。'))}</p></div>${id?button(tr('定位知识'),'select',`data-id="${esc(id)}"`,'small'):''}</div>`;}).join(''):tr('<p class="muted">当前范围没有已报告问题。未发现问题不等于业务含义已被证明正确。</p>');}

  function backupButton(){
    return C?.legacyState?.()?.model_only
      ? '<button type="button" class="small" data-action="download" data-type="backup">'+say('下载私人项目备份（含原始资料）','Back up private project including sources')+'</button>'
      :button(tr('私人项目备份'),'legacy','data-page="delivery"','small');
  }
  function publishPage(){const chosen=S.assets.filter(a=>deliverySelection.has(a.id));return (scopedDelivery?tr`<div class="notice">交付范围来自当前问题，刷新后保留。取消所有选择不会扩大为全库。${button(tr('明确切换为全部模型'),'reset-delivery','','small')}</div>`:'')+heading(tr('导出模型'),tr('生成可离线读取的语义包。草稿保留未确认状态；保存的快照不会随编辑变化。'),backupButton())+
    tr`<div class="grid cols2"><section class="card"><h2>选择交付范围</h2><p class="sub">不勾选时导出全部有效模型，包含表、字段与外键；勾选后只导出所选内容及必需依赖。</p><details class="kw-multiselect" open><summary id="kw-selected-count">已选 ${chosen.length} 项${!chosen.length?tr(scopedDelivery?' · 尚未选择定义':' · 全部模型')+(scopedDelivery?'':' ('+S.assets.filter(a=>a.status!=='retired').length+')'):''}</summary><input id="kw-publish-search" class="kw-option-search" placeholder="搜索知识名称" aria-label="搜索交付知识"><div class="kw-options kw-delivery-options">${S.assets.map(a=>`<label data-option-label="${esc((a.name+' '+a.domain).toLowerCase())}"><input type="checkbox" data-publish-id="${esc(a.id)}" ${deliverySelection.has(a.id)?'checked':''}> ${esc(a.name)} <span class="privacy">${esc(kinds[a.kind])} · ${esc(a.domain)} · ${esc(statuses[a.status])}</span></label>`).join('')}</div></details><label class="kw-inline-check"><input id="kw-include-execution" type="checkbox" ${publishExecution?'checked':''}> 附带数据映射与执行声明</label><div class="notice">需复核、未确认的必需定义、已停用依赖或缺失依据会阻止确认发布。草稿会明确标识缺口。</div><div class="row">${button(tr('发布确认快照'),'publish','','primary')}${button(tr('导出草稿供讨论'),'publish','data-draft="true"')}</div><div id="kw-publish-error" class="error" role="alert"></div></section><section class="card"><h2>交付与调用</h2>${publishResult?tr`<div class="notice"><b>快照已保存</b><p>${esc(publishResult.snapshot_id||publishResult.manifest?.snapshot_id)}</p></div>${button(tr('下载语义包'),'download',`data-url="${esc(publishResult.download_url||'/api/knowledge/download/'+publishResult.snapshot_id)}" data-filename="${esc(publishResult.filename||'semantic-package.zip')}"`,'primary')}${button('Neo4j (CSV + Cypher)','download',`data-url="/api/knowledge/download/${esc(publishResult.snapshot_id)}?format=neo4j" data-filename="neo4j-import.zip"`)}${scopeHtml(publishResult.manifest)}<p>包内附独立读取命令和人工核验页。解压或通过只读工具打开即可使用。</p>`:tr('<p class="sub">确认快照包含模型、必要证据片段、清单、人工核验页和调用说明。</p><p>交给另一个 Agent 后，请它报告所用快照，先搜索、消歧，再用 context 读取必需定义、业务范围、依据及缺口。</p>')}<div class="notice">旧快照保持不变。当前知识修改后，请发布新快照；离线文件不能自动知道有更新。</div><h3>本次选择</h3><p id="kw-selection-summary">${esc(chosen.length?chosen.map(a=>a.name).join('、'):tr(scopedDelivery?'尚未选择定义':'全部有效模型（自动补齐必需依赖）'))}</p></section></div><div class="section-title"><h2>已保存快照</h2></div><div class="card">${(S.snapshots||[]).length?S.snapshots.slice().reverse().map(s=>tr`<div class="gap"><div><h3>${esc(s.snapshot_id||s.id)} ${badge(s.draft?'draft':'confirmed')}</h3><p class="privacy">来源修订 ${esc(s.source_revision??s.revision)}</p><details><summary>实际范围与缺口</summary>${scopeHtml(s)}</details></div>${button(tr('下载'),'download',`data-url="/api/knowledge/download/${esc(s.snapshot_id||s.id)}" data-filename="${esc(s.filename||'semantic-package.zip')}"`,'small')}${button('Neo4j','download',`data-url="/api/knowledge/download/${esc(s.snapshot_id||s.id)}?format=neo4j" data-filename="neo4j-import.zip"`,'small')}</div>`).join(''):empty(tr('尚未发布'),tr('先核对知识，再生成可独立读取的语义包。'))}</div>`;}
  function historyPage(){return heading(tr('项目历史'),tr('知识修改保留修订；布局移动独立保存。撤回会新增修订，不抹掉历史。'),(C?.legacyState?.()?.model_only?'':button(tr('数值验证历史'),'legacy','data-page="check"','small'))+backupButton())+tr`${pending.size?tr`<section class="card"><h2>待确认提交</h2>${pendingRows()}</section>`:''}<section class="card"><table><thead><tr><th>修订</th><th>变化</th><th>时间 / 操作者</th><th></th></tr></thead><tbody>${(S.history||[]).map(h=>`<tr><td>${esc(h.revision)}</td><td>${esc(tr(h.summary))}</td><td>${esc(h.created||'')}<small>${esc(h.actor||'')}</small></td><td>${button(tr('检查并撤回'),'undo',`data-revision="${h.revision}"`,'small')}</td></tr>`).join('')}</tbody></table></section>`;}

  function openDialog(title,body,onSave,{confirmLabel=tr('保存'),draft=false,assetOriginal=null}={}) {
    let el=$('#kw-dialog');if(!el){el=document.createElement('dialog');el.id='kw-dialog';document.body.append(el);}
    dialog={id:uid(),onSave,baseRevision:S.revision,assetOriginal,conflict:false};
    const keepConfirmed=assetOriginal?.status==='confirmed';
    const draftButton=draft?`<button type="submit" value="draft" class="${keepConfirmed?'':'primary'}">${tr('保存草稿')}</button>`:'';
    const confirmButton=onSave?`<button type="submit" value="confirm" class="${draft&&!keepConfirmed?'':'primary'}">${esc(confirmLabel)}</button>`:'';
    const actions=keepConfirmed?confirmButton+draftButton:draftButton+confirmButton;
    el.innerHTML=tr`<form id="kw-form"><div class="dialog-head"><div><h2>${esc(title)}</h2></div>${button('×','close-dialog',`aria-label="${tr('关闭')}"`,'quiet')}</div><div class="kw-dialog-body">${body}</div><div class="kw-dialog-error"><div id="kw-external-change"></div><p id="kw-dialog-error" class="error" role="alert"></p><div id="kw-conflict"></div></div><footer class="kw-dialog-actions"><span class="spacer"></span>${button(tr('取消'),'close-dialog')}${actions}</footer></form>`;
    el.oncancel=()=>{if(dialog?.assetDraftKey)assetDrafts.delete(dialog.assetDraftKey);dialog=null;};
    el.showModal();$('#kw-form').addEventListener('submit',async event=>{event.preventDefault();const buttons=[...el.querySelectorAll('button')];buttons.forEach(b=>b.disabled=true);try{await dialog.onSave(event.submitter?event.submitter.value!=='draft':!draft||keepConfirmed,dialog);el.close();dialog=null;}catch(e){$('#kw-dialog-error').textContent=e.message;if(e.status===409){dialog.conflict=true;showConflict();}}finally{buttons.forEach(b=>b.disabled=false);}});
  }
  function showConflict(){const el=$('#kw-conflict');if(el)el.innerHTML=tr('<p class="privacy">输入已保留。先刷新并查看最新定义，再决定如何继续。</p>')+button(tr('读取最新状态并核对'),'dialog-refresh','','small');}
  function newAssetTitle(kind){return say('新建','New ')+kinds[kind];}
  function openAsset(id,prefill={}) {const draftKey=id||'new:'+JSON.stringify(prefill),savedDraft=assetDrafts.get(draftKey);const original=copy(savedDraft?.asset||asset(id)||{kind:'entity',name:'',definition:'',domain:importDraft.domain||'',scope:importDraft.scope||'',aliases:[],properties:{},refs:[],evidence:[],...prefill});openDialog(id?tr('编辑 ')+original.name:newAssetTitle(original.kind),tr`<div id="kw-asset-fields">${assetFields(original,{allowNewEnds:true})}</div><div class="kw-evidence-entry"><section id="kw-metric-check" hidden><h3>${say('对照原文，哪些记录算进去？','Compare the metric with its source')}</h3><dl class="kw-properties"><dt>${say('计入','Include')}</dt><dd data-compare="inclusions"></dd><dt>${say('排除','Exclude')}</dt><dd data-compare="exclusions"></dd></dl></section>${original.evidence?.length?`<h3>${say('已附依据','Attached evidence')}</h3>${evidenceHtml(original.evidence)}`:''}
      <details class="kw-form-section" data-citation><summary>${say('引用文件中的原文','Quote a source document')}</summary>
      ${S.sources.length?'':`<p class="muted">${say('还没有导入材料。可以先存草稿，稍后导入文件再回来引用。','No documents yet. Save a draft, import a file, then return to cite it.')}</p>`}
      <label>${say('文件','Document')}<select id="kw-cite-source">${options(S.sources.map(s=>[s.id,s.name]),'')}</select></label><label>${say('原文段落','Passage')}<select id="kw-cite-fragment" disabled></select></label><label>${say('要引用的原句','Exact quotation')}<textarea id="kw-cite-quote"></textarea></label></details>
      <details class="kw-form-section"><summary>${say('记录业务人员的说明','Add a business owner’s explanation')}</summary><label>${say('说明内容','Explanation')}<textarea id="kw-manual-evidence" placeholder="${say('写下谁说明了什么，以及适用条件','Record who explained what and when it applies')}">${esc(savedDraft?.declaration||'')}</textarea></label></details></div>`,async(confirmed,d)=>{const form=$('#kw-asset-fields'),changed=readAsset(form,original);
      if(confirmed){for(const key of ['definition','domain','scope',...(S.editor_contract?.confirm_fields?.[changed.kind]||[]).map(k=>'properties.'+k)]){const el=form.querySelector('[data-field="'+key+'"]');if(el&&!el.value.trim()){el.closest('details')?.setAttribute('open','');el.focus();const label=el.closest('label').firstChild.textContent.trim();throw Error(say('要标为已确认，请填写','To confirm, fill in ')+label+say('。也可以先保存草稿。','. You can also save a draft.'));}}}
      const selected=$('#kw-cite-source'),frag=$('#kw-cite-fragment'),quote=$('#kw-cite-quote').value.trim();
      if(selected.value){if(!frag.value){frag.closest('details').open=true;frag.focus();throw Error(say('请选择要引用的原文段落','Choose a passage to quote'));}const r=resolveSource(selected.value,frag.dataset.revision,frag.value,frag.dataset.extraction);
        if(!quote||!r.fragment.text.includes(quote)){const input=$('#kw-cite-quote');input.closest('details').open=true;input.focus();throw Error(say('请从选中的段落复制一段连续原文。','Copy a continuous quotation from the selected passage.'));}
        changed.evidence=[...(changed.evidence||[]),{source_id:r.source.id,revision:r.revision.revision,extraction_id:r.extraction_id,fragment_id:r.fragment.id,quote}];}
      const declaration=$('#kw-manual-evidence').value.trim();
      if(confirmed&&!changed.evidence?.length&&!declaration){const area=S.sources.length?$('#kw-cite-source'):$('#kw-manual-evidence');area.closest('details').open=true;area.focus();throw Error(say('要标为已确认，请引用原文或写下业务人员的说明。也可以先保存草稿。','To confirm, quote a document or record an explanation. You can also save a draft.'));}
      if(declaration)changed.evidence=[...(changed.evidence||[]),{type:'manual',quote:declaration,actor:'local'}];const saved=await transact('edit:'+draftKey,'edit',{asset:changed,confirm:confirmed},d.baseRevision);G.selected=saved.asset_id||changed.id||null;
      if(G.selected&&activePage==='graph')locate(G.selected);
      assetDrafts.delete(draftKey);if(activePage==='graph'){drawGraph();drawInspector();}C.notify(confirmed?tr('知识已保存并确认'):tr('草稿已保存'));},{confirmLabel:tr('保存并确认'),draft:true,assetOriginal:original});dialog.assetDraftKey=draftKey;
    const fields=$('#kw-asset-fields');previewRelation(fields);
    const compareMetric=()=>{
      const card=$('#kw-metric-check');
      card.hidden=fields.querySelector('[data-field="kind"]').value!=='metric';
      if(card.hidden)return;
      for(const item of card.querySelectorAll('[data-compare]')){
        item.textContent=fields.querySelector('[data-field="properties.'+item.dataset.compare+'"]')?.value.trim()||say('待填写','To be specified');
      }
    };
    compareMetric();
    fields.oninput=compareMetric;
    fields.onchange=()=>queueMicrotask(compareMetric);
    const first=['relation','mapping'].includes(original.kind)?(original.from&&original.to?'predicate':'from'):'name';
    fields.querySelector('[data-field="'+first+'"]')?.focus();
    if(savedDraft?.baseRevision!==undefined)dialog.baseRevision=savedDraft.baseRevision;}
  function openSource(id,revision,fragmentId,extractionId){const resolved=resolveSource(id,revision||undefined,fragmentId||undefined,extractionId||undefined),s=resolved.source,r=resolved.revision;let viewer=$('#kw-source-dialog');if(!viewer){viewer=document.createElement('dialog');viewer.id='kw-source-dialog';document.body.append(viewer);}viewer.innerHTML=tr`<div class="dialog-head"><h2>${esc(s.name)}</h2>${button('×','close-source','','quiet')}</div><div class="kw-dialog-body"><div class="row"><b>来源修订 ${esc(r?.revision)}</b>${badge(r?.parsed?.status)}<span class="privacy">${esc(s.id)}</span></div><div class="row">${(s.revisions||[]).map(x=>button(tr('修订 ')+x.revision,'source-version',`data-id="${esc(id)}" data-revision="${x.revision}"`,'small')).join('')}${(r.extractions||[]).length>1?r.extractions.map((x,i)=>button(tr('提取 ')+(i+1),'source-version',`data-id="${esc(id)}" data-revision="${r.revision}" data-extraction="${esc(x.id)}"`,'small')).join(''):''}${r?.attachment_id?button(tr('下载原件'),'download',`data-url="/api/knowledge/source/${esc(r.attachment_id)}" data-filename="${esc(s.name)}"`,'small'):''}</div>${(r?.parsed?.warnings||[]).map(w=>`<div class="notice warning">${esc(typeof w==='object'?w.message||fmt(w):w)}</div>`).join('')}<div class="kw-fragments">${(r?.parsed?.fragments||[]).map(f=>`<section class="kw-fragment ${f.id===fragmentId?'target':''}" id="fragment-${esc(f.id)}"><h3>${esc(fmt(f.location))}</h3><pre>${esc(f.text)}</pre></section>`).join('')||tr('<p>这份修订没有可读取的文本片段，请查看解析结果或补充可读资料。</p>')}</div></div><footer>${button(tr('关闭原文'),'close-source')}</footer>`;if(!viewer.open)viewer.showModal();if(fragmentId)viewer.querySelector('.kw-fragment.target')?.scrollIntoView({block:'center'});}

  async function importText(){const text=$('#kw-import-text').value;if(!text.trim())throw Error(tr('请先填写材料原文'));const payload={filename:importDraft.name||tr('业务说明.txt'),text,domain:importDraft.domain,scope:importDraft.scope,...(importDraft.source_id?{source_id:importDraft.source_id}:{}),distinct_source:importDraft.distinct};const r=await transact('text-import','import',payload);importDraft.text='';importDraft.source_id='';rerender();C.notify(tr('材料已保存。请准备 Agent 任务或核对结构候选。'));return r;}
  async function importFiles(){if(!selectedFiles.length)throw Error(tr('请先选择文件'));if(importDraft.source_id&&selectedFiles.length>1)throw Error(tr('更新一份来源时请只选择一个文件；多份新材料请改为新来源'));const seedDraft=!!$('#kw-seed-draft')?.checked;let seeded=false;const config={encoding:importDraft.encoding||undefined,sheet:$('#kw-sheet')?.value||undefined,header:Number($('#kw-header')?.value||1),range:$('#kw-range')?.value||undefined};importResults=[];const succeeded=[];for(const file of selectedFiles){if(file.size>32*1024*1024){importResults.push({name:file.name,ok:false,message:tr('超过 32 MB，请缩小文件后重试')});continue;}try{const bytes=new Uint8Array(await file.arrayBuffer());let binary='';for(let i=0;i<bytes.length;i+=8192)binary+=String.fromCharCode(...bytes.subarray(i,i+8192));const result=await transact('file:'+file.name,'import',{filename:file.name,content_base64:btoa(binary),domain:importDraft.domain,scope:importDraft.scope,source_id:importDraft.source_id||undefined,distinct_source:importDraft.distinct,options:config,seed_draft:seedDraft&&!S.assets.length&&/\.(sql|ddl)$/i.test(file.name)});seeded=seeded||!!result.seeded;succeeded.push(file);importResults.push({name:file.name,ok:true,message:(result.parsed?.warnings||[]).length?result.parsed.warnings.join(' · '):tr('已保存，请查看解析范围与候选')});}catch(e){importResults.push({name:file.name,ok:false,message:e.message});}}selectedFiles=selectedFiles.filter(f=>!succeeded.includes(f));if(seeded&&importResults.every(r=>r.ok)&&importResults.every(r=>r.message===tr('已保存，请查看解析范围与候选'))){C.go('graph');C.notify(tr('结构草稿已生成，可直接编辑或导出。'));}else rerender();}
  async function download(url,filename){if(url.startsWith('/api/knowledge/download/')){const link=document.createElement('a');link.href=url;link.download=filename||'semantic-package.zip';document.body.append(link);link.click();link.remove();C.notify(tr('下载请求已发出，请查看浏览器保存结果'));return;}const result=await fetch(url,{headers:{'X-Workbench-Token':$('meta[name="session-token"]').content}});if(!result.ok){let body;try{body=await result.json();}catch(_){}throw Error(body?.error||tr('下载失败，请重试'));}const object=URL.createObjectURL(await result.blob()),a=document.createElement('a');a.href=object;a.download=filename||'semantic-package.zip';a.hidden=true;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(object),60000);C.notify(tr('下载请求已发出，请查看浏览器保存结果'));}
  async function act(b){const a=b.dataset.kw,id=b.dataset.id;
    if(a==='more-table-fields'){
      const holder=b.closest('[data-table-fields]');holder.dataset.limit=String(Number(holder.dataset.limit||12)+12);
      displayTableFields(holder,asset(G.selected));return;
    }
    if(a==='swap-ends'){
      const form=b.closest('[data-candidate],#kw-asset-fields,#kw-source-asset,#kw-merged-fields'),from=form.querySelector('[data-field="from"]'),to=form.querySelector('[data-field="to"]');
      if(form.closest('[data-readonly="true"]'))return;
      if(!from.value||!to.value){C.notify(say('先选好两端，再交换方向','Choose both objects before swapping'));return;}
      if([...from.options].find(o=>o.value===to.value)?.disabled||[...to.options].find(o=>o.value===from.value)?.disabled){C.notify(say('这种关系限制两端类型，不能交换','This relationship type fixes the endpoint types'));return;}
      const before=from.value;from.value=to.value;to.value=before;
      const left=form.querySelector('[data-field="properties.from_fields"]'),right=form.querySelector('[data-field="properties.to_fields"]');
      if(form.querySelector('[data-field="relation_type"]').value==='physical_fk'&&left&&right){const keys=left.value;left.value=right.value;right.value=keys;}
      to.dispatchEvent(new Event('input',{bubbles:true}));updateEnds(form);return;
    }
    if(a==='add-end'){
      const side=b.dataset.side,form=$('#kw-asset-fields'),editor=dialog,group=b.closest('[data-end-create]');
      const input=group.querySelector('[data-end-name]'),name=input.value.trim();
      if(!name){input.focus();throw Error(say('请输入可识别的对象名称','Enter an identifiable object name'));}
      const base=editor.baseRevision;
      const result=await transact('endpoint:'+editor.id+':'+side+':'+base,'edit',{asset:{kind:'entity',name,domain:form.querySelector('[data-field="domain"]').value.trim()},confirm:false},base);
      if(dialog!==editor)return;
      const item=asset(result.asset_id);
      if(!item)throw Error(say('对象已保存，请刷新后选用','Object saved. Refresh to select it.'));
      editor.baseRevision=base+1;
      for(const key of ['from','to']){
        const select=form.querySelector('[data-field="'+key+'"]');
        const option=new Option(endpointLabel(item,true),item.id);option.dataset.kind=item.kind;select.add(option);
        if(key===side)select.value=item.id;
      }
      updateEnds(form);group.open=false;input.value='';
      form.querySelector('[data-field="'+side+'"]').dispatchEvent(new Event('change',{bubbles:true}));
      $('#kw-dialog-error').textContent='';C.notify(say('已创建并选用对象草稿','Created and selected the draft object'));return;
    }
    if(a==='show-group'){const g=byId('groups',id);if(!g)throw Error(tr('接替候选尚未读回，请刷新项目'));reviewBatch=g.batch_id;reviewFilter='all';const groups=S.groups.filter(x=>x.batch_id===reviewBatch).slice().reverse();reviewPageIndex=Math.floor(groups.findIndex(x=>x.id===id)/10);C.go('review');$('[data-group="'+id+'"]')?.scrollIntoView({block:'start'});return;}
    if(a==='review-page'){captureGroups();reviewPageIndex=Number(b.dataset.pageIndex);rerender();return;}
    if(a==='candidate-page'){captureGroups();candidatePages.set(id,Number(b.dataset.offset)/20);rerender();return;}
    if(a==='refs-more'){const pool=refPools.get(b.dataset.pool);if(pool){pool.limit+=100;renderReferences($('[data-ref-pool="'+b.dataset.pool+'"]'));}return;}
    if(a==='pending-query'){const result=await receiptFor(b.dataset.key);rerender();C.notify(result?tr('已读取上次完成结果，没有重复执行'):tr('尚无完成回执；可重试原提交，系统仍会防重复'));return;}
    if(a==='pending-retry'){const op=pending.get(b.dataset.key);if(!op||op.needsMaterial)throw Error(tr('请从材料入口重新选择同一原件'));const {revision,operation_id,...payload}=op.request;await transact(b.dataset.key,op.path,payload,revision);rerender();C.notify(tr('已确认原提交的结果'));return;}
    if(a==='locate')return locate(id);
    if(a==='go'||a==='legacy')return C.go(b.dataset.page);
    if(a==='refresh')return C.reload();
    if(a==='close-source'){$('#kw-source-dialog').close();return;}
    if(a==='close-dialog'){if(dialog?.assetDraftKey)assetDrafts.delete(dialog.assetDraftKey);$('#kw-dialog').close();dialog=null;return;}
    if(a==='create')return openAsset(null,b.dataset.kind?{kind:b.dataset.kind,domain:G.domain||asset(G.selected)?.domain||''}:{});
    if(a==='edit')return openAsset(id);
    if(a==='source'||a==='source-version')return openSource(id,b.dataset.revision,b.dataset.fragment,b.dataset.extraction);
    if(a==='update-source'){const source=byId('sources',id);importDraft={...importDraft,source_id:id,name:source.name,domain:source.domain||'',scope:source.scope||'',text:''};C.go('knowledge');$('#kw-import-source').focus();C.notify(tr('已选更新来源。粘贴新原文或选择新文件。'));return;}
    if(a==='import-text')return importText();
    if(a==='import-files')return importFiles();
    if(a==='example'){await transact('example','example',{});C.go('review');return;}
    if(a==='prepare'){const r=await transact('prepare:'+id,'task',{batch_id:id,action:'prepare',language:window.UIText?.language||'en'});taskTexts.set(id,(r.host_instruction?(r.host_instruction+'\n\n'+(r.instruction||'')):null)||tr`请使用 ai-data-delivery 处理项目「${S.project_directory||S.document?.name||S.project_id}」的批次 ${id}。读取本批次原文及现有知识，提出带来源的候选并提交；不要将推测写成已确认知识。`);if(activePage!=='knowledge')C.go('knowledge');else rerender();return;}
    if(a==='copy-task'){const value=taskTexts.get(id);try{await navigator.clipboard.writeText(value);C.notify(tr('宿主指令已复制'));}catch(_){b.closest('.kw-task').querySelector('textarea').select();C.notify(tr('已选中指令，请按 Ctrl+C 复制'));}return;}
    if(a==='copy-relation-hints'){const input=b.closest('.kw-task').querySelector('textarea');try{await navigator.clipboard.writeText(input.value);C.notify(say('已复制关系核对指令','Relationship review prompt copied'));}catch(_){input.select();C.notify(say('已选中指令，请按 Ctrl+C 复制','Prompt selected. Press Ctrl+C to copy.'));}return;}
    if(a==='cancel-task'||a==='resume'){await transact('task:'+id,'task',{batch_id:id,action:a==='resume'?'resume':'cancel'});C.notify(a==='resume'?tr('任务已恢复，可继续剩余范围'):tr('任务已取消，已返回候选仍保留'));return;}
    if(a==='batch-review'){reviewPageIndex=0;reviewBatch=id;reviewFilter='all';return C.go('review');}
    if(a==='review-action'){const g=byId('groups',id),el=b.closest('[data-group]'),d=groupDraft(g);d.assets=g.candidates.map((c,i)=>readAsset(el.querySelector(`[data-candidate="${i}"]`),d.assets[i]));d.reason=el.querySelector('[data-group-reason]').value;await transact('group:'+id,'review',{group_id:id,action:b.dataset.mode,reason:d.reason,assets:d.assets});drafts.delete(id);C.notify(tr('本组处置已保存'));return;}
    if(a==='locate-change'){locate(id);return;}
    if(a==='select'){selectGraphAsset(id);return;}
    if(a==='view'){drag=null;G.view=b.dataset.view;G.limit=80;G.focus=null;connection=null;saveView();rerender();return;}
    if(a==='toggle-fields'){if(fieldDetailRequested())return;setConnection(null);G.fieldsExpanded=!G.fieldsExpanded;G.limit=80;
      if(!G.fieldsExpanded&&fieldIndex().foldable.has(G.selected)){
        G.selected=asset(G.selected)?.refs?.[0]||null;
      }
      saveView();drawGraph(true);drawInspector();return;}
    if(a==='toggle-view'){connection=null;G.expanded=false;G.mode=G.mode==='graph'?'table':'graph';saveView();rerender();return;}
    if(a==='focus'){G.focus=id;G.limit=80;G.query='';graphLocation(id);saveView();rerender();return;}
    if(a==='clear-focus'){G.focus=null;G.limit=80;graphLocation(null);saveView();rerender();drawGraph(true);return;}
    if(a==='more'){G.limit+=80;drawGraph();return;}
    if(a==='fix'){if(G.fixed.includes(id))G.fixed=G.fixed.filter(x=>x!==id);else{const positions=currentLayout();await C.api('layout',{positions});S.layout=positions;G.fixed=[...G.fixed,id];}saveView();drawGraph();drawInspector();return;}
    if(a==='zoom'){zoomCanvas(1+Number(b.dataset.delta));return;}
    if(a==='fit-canvas'){fitAllNodes=true;drawGraph(true);return;}
    if(a==='expand-canvas'){G.expanded=!G.expanded;G.inspector=false;saveView();rerender();drawGraph(true);$('[data-kw="expand-canvas"]')?.focus();return;}
    if(a==='toggle-inspector'){G.inspector=!G.inspector;saveView();rerender();drawGraph(true);return;}
    if(a==='arrange'){if(b.dataset.layoutAction==='cancel'){autoPendingKey=diagramKey(graphInput(graphData()));runningWorker?.cancel();layoutButton();return;}await arrangeGraph(true);return;}
    if(a==='undo-layout'){if(!layoutUndo.length)throw Error(tr('当前会话没有可撤销的布局操作'));const old=layoutUndo.at(-1);await C.api('layout',{positions:old});S.layout=old;layoutUndo.pop();drawGraph();return;}
    if(a==='connect'||a==='cancel-connect'){
      const start=a==='connect'&&!connection;setConnection(start?{start:null}:null);
      if(start)$('#kw-graph [data-kw-node]')?.focus();else $('[data-kw="connect"]')?.focus();return;
    }
    if(a==='clear-graph-filter'){setConnection(null);Object.assign(G,{query:'',kind:'',status:'',domain:'',focus:null,selected:null,inspector:false,view:'all',limit:80});graphLocation(null);saveView();rerender();drawGraph(true);return;}
    if(a==='download')return download(b.dataset.url,b.dataset.filename);
    if(a==='reset-delivery'){deliverySelection=new Set();scopedDelivery=false;saveDelivery();rerender();return;}
    if(a==='publish'){if(scopedDelivery&&!deliverySelection.size)throw Error(tr('当前问题没有选择定义，请先选择，或明确切换为全部模型。'));publishResult=await transact('publish','publish',{asset_ids:deliverySelection.size?[...deliverySelection]:S.assets.filter(x=>x.status!=='retired').map(x=>x.id),draft:b.dataset.draft==='true',include_execution:publishExecution});rerender();C.notify(tr('快照已保存，可下载回读'));return;}
    if(a==='undo'){if(!confirm(tr('检查并撤回这一语义事务？有后续冲突时会保留当前内容并提示。')))return;await transact('undo:'+b.dataset.revision,'undo',{target_revision:Number(b.dataset.revision)});C.notify(tr('语义事务已撤回，历史仍保留'));return;}
    if(a==='retire')return retireDialog(id);
    if(a==='resolve-identity')return identityDialog(id);
    if(a==='review-source')return sourceReviewDialog(id);
    if(a==='dialog-refresh'){const current=dialog;await C.reload();const latest=asset(current.assetOriginal?.id);$('#kw-conflict').innerHTML=tr`<div class="notice"><b>最新定义</b><p>${esc(latest?.definition||tr('对象已不存在或此次操作不绑定单个对象'))}</p><p>项目修订 ${S.revision}。上方输入未被覆盖，请对照后继续。</p></div>${button(tr('已核对最新状态，继续使用保留输入'),'dialog-rebase','','small')}`;return;}
    if(a==='dialog-rebase'){dialog.baseRevision=S.revision;if(assetDrafts.has(dialog.assetDraftKey))assetDrafts.get(dialog.assetDraftKey).baseRevision=S.revision;dialog.conflict=false;$('#kw-conflict').innerHTML=tr('<p class="privacy">已按当前修订继续；提交时仍会重检。</p>');return;}
  }
  function retireDialog(id){const a=asset(id);openDialog((a.status==='draft'?tr('删除或停用 '):tr('停用 '))+a.name,tr`<p>系统会检查所有引用，包含当前图上隐藏的知识。</p><label>处理方式<select id="kw-retire-mode">${options([['retire',tr('停用并保留历史')],...(a.status==='draft'?[['delete',tr('删除未引用、未发布的草稿')]]:[])],'retire',null)}</select></label><label>原因<textarea id="kw-retire-reason"></textarea></label>`,async(_,d)=>{await transact('retire:'+id,'retire',{asset_id:id,reason:$('#kw-retire-reason').value,action:$('#kw-retire-mode').value},d.baseRevision);C.notify(tr('处理已保存'));},{confirmLabel:tr('确认处理'),assetOriginal:a});}
  function identityDialog(id){const a=asset(id);openDialog(tr('核对身份：')+a.name,tr`<p>先选另一对象并比较定义。合并会更新引用；保持分离会保存两者不同的理由。</p><label>另一项知识<select id="kw-identity-target">${options(S.assets.filter(x=>x.id!==id&&x.kind===a.kind&&x.status!=='retired').map(x=>[x.id,`${x.name} · ${x.domain}`]),'')}</select></label><div id="kw-identity-comparison"></div><label>处理方式<select id="kw-identity-mode">${options([['separate',tr('保持分离')],['merge',tr('合并到当前对象（保留当前 ID）')]],'separate',null)}</select></label><details id="kw-merged-fields" hidden open><summary>合并后的完整定义（逐项核对）</summary>${assetFields(a)}</details><label>判断理由<textarea id="kw-identity-reason"></textarea></label>`,async(_,d)=>{const other=$('#kw-identity-target').value,reason=$('#kw-identity-reason').value;if(!other)throw Error(tr('请选择另一项知识'));if(!reason.trim())throw Error(tr('请说明身份判断的理由'));if($('#kw-identity-mode').value==='separate')await transact('identity:'+id,'separate',{left_id:id,right_id:other,reason},d.baseRevision);else {const otherAsset=asset(other),resolved=readAsset($('#kw-merged-fields'),a);resolved.aliases=[...new Set([...(resolved.aliases||[]),otherAsset.name,...(otherAsset.aliases||[])])];resolved.evidence=[...(a.evidence||[]),...(otherAsset.evidence||[])];await transact('identity:'+id,'merge',{survivor_id:id,merged_id:other,resolved_asset:resolved,reason},d.baseRevision);}C.notify(tr('身份判断已保存'));},{confirmLabel:tr('保存身份判断'),assetOriginal:a});}
  function sourceReviewDialog(id){const a=asset(id);openDialog(tr('复核来源：')+a.name,tr`<h3>原定义</h3><p>${esc(a.definition)}</p>${evidenceHtml(a.evidence)}<h3>来源的新修订</h3>${[...new Map((a.evidence||[]).filter(e=>e.source_id).map(e=>[e.source_id,e])).values()].map(e=>{const s=byId('sources',e.source_id),r=s?.revisions?.find(v=>v.revision===s.current_revision);return tr`<details open><summary>${esc(s?.name)} · 修订 ${esc(r?.revision)}</summary>${(r?.parsed?.fragments||[]).map(f=>`<label class="kw-source-choice"><input type="checkbox" data-new-evidence="${esc(JSON.stringify({source_id:s.id,revision:r.revision,extraction_id:r.current_extraction,fragment_id:f.id,quote:f.text}))}"><b>${esc(fmt(f.location))}</b><blockquote>${esc(f.text)}</blockquote></label>`).join('')}</details>`;}).join('')}<label>复核决定<select id="kw-source-action">${options([['retain',tr('原定义仍适用，保留原依据')],['adopt',tr('采用来源修订并调整定义')]],'retain',null)}</select></label><div id="kw-source-asset" hidden>${assetFields(a)}</div><label>复核理由<textarea id="kw-source-reason" placeholder="说明原定义为何仍适用，或本次采用了什么变化。"></textarea></label>`,async(_,d)=>{const action=$('#kw-source-action').value,reason=$('#kw-source-reason').value,changed=readAsset($('#kw-source-asset'),a);if(!reason.trim())throw Error(tr('请填写复核理由'));if(action==='adopt'){const selected=[...$('#kw-dialog').querySelectorAll('[data-new-evidence]:checked')].map(x=>JSON.parse(x.dataset.newEvidence));if(!selected.length)throw Error(tr('采用修订时，请勾选本次定义实际使用的新原文片段'));const selectedSources=new Set(selected.map(e=>e.source_id));changed.evidence=[...(a.evidence||[]).filter(e=>!e.source_id||(!selectedSources.has(e.source_id)&&e.revision===byId('sources',e.source_id)?.current_revision)),...selected];}await transact('source-review:'+id,'review-source',{asset_id:id,action,reason,...(action==='adopt'?{asset:changed}:{})},d.baseRevision);C.notify(tr('来源复核已保存'));},{confirmLabel:tr('保存复核结论'),assetOriginal:a});}

  document.addEventListener('toggle',e=>{if(!e.target.open)return;if(e.target.matches('.kw-candidate'))hydrateCandidate(e.target);if(e.target.matches('[data-ref-pool]'))renderReferences(e.target);},true);
  document.addEventListener('click',async e=>{const b=e.target.closest('[data-kw]');if(!b)return;try{b.disabled=true;await act(b);}catch(err){const target=b.closest('[data-group]')?.querySelector('.kw-group-error')||(['import-text','import-files'].includes(b.dataset.kw)?$('#kw-import-error'):b.dataset.kw==='publish'?$('#kw-publish-error'):$('#kw-dialog[open] #kw-dialog-error'));if(target){target.textContent=err.message;const issues=err.details?.details?.issues||err.details?.issues;if(issues?.length)target.insertAdjacentHTML('beforeend',issuesHtml(issues));}else C.notify(err.message);}finally{b.disabled=false;}});
  document.addEventListener('input',e=>{const el=e.target;captureReference(el);
    if(el.matches('[data-table-field-search]')){const holder=el.closest('[data-table-fields]');holder.dataset.limit='12';displayTableFields(holder,asset(G.selected));return;}

    const fields=el.closest('[data-candidate],#kw-asset-fields,#kw-source-asset,#kw-merged-fields');
    if(fields&&el.matches('[data-end-search]'))updateEnds(fields);
    if(fields&&el.matches('[data-field=from],[data-field=to],[data-field=predicate]'))previewRelation(fields);
    if(dialog?.assetDraftKey!==undefined&&el.closest('#kw-form'))assetDrafts.set(dialog.assetDraftKey,{asset:readAsset($('#kw-asset-fields'),dialog.assetOriginal,false),declaration:$('#kw-manual-evidence').value,baseRevision:dialog.baseRevision});if(el.dataset.import){importDraft[el.dataset.import]=el.type==='checkbox'?el.checked:el.value;}
    if(el.matches('.kw-option-search')){const q=el.value.toLowerCase(),details=el.closest('.kw-multiselect');if(details.dataset.refPool){const pool=refPools.get(details.dataset.refPool);pool.query=q;pool.limit=100;renderReferences(details);}else details.querySelectorAll('[data-option-label]').forEach(x=>x.hidden=!x.dataset.optionLabel.includes(q));}
    if(el.id==='kw-graph-search'||el.id==='kw-canvas-search'){setConnection(null);G.query=el.value;if(G.query&&G.focus){G.focus=null;graphLocation(null);}G.limit=80;saveView();drawGraph();}
    const group=el.closest('[data-group]');if(group){const g=byId('groups',group.dataset.group),d=groupDraft(g),f=el.closest('[data-candidate]');if(f)d.assets[Number(f.dataset.candidate)]=readAsset(f,d.assets[Number(f.dataset.candidate)],false);if(el.hasAttribute('data-group-reason'))d.reason=el.value;}
  });
  document.addEventListener('change',e=>{const el=e.target;if(el.dataset.import)importDraft[el.dataset.import]=el.type==='checkbox'?el.checked:el.value;if(el.id==='kw-files'){selectedFiles=[...el.files];return;}if(el.dataset.publishId){el.checked?deliverySelection.add(el.dataset.publishId):deliverySelection.delete(el.dataset.publishId);saveDelivery();const chosen=S.assets.filter(a=>deliverySelection.has(a.id));$('#kw-selected-count').textContent=tr('已选 ')+chosen.length+tr(' 项')+(!chosen.length?tr(scopedDelivery?' · 尚未选择定义':' · 全部模型')+(scopedDelivery?'':' ('+S.assets.filter(a=>a.status!=='retired').length+')'):'');$('#kw-selection-summary').textContent=chosen.length?chosen.map(a=>a.name).join('、'):tr(scopedDelivery?'尚未选择定义':'全部有效模型（自动补齐必需依赖）');return;}if(el.id==='kw-include-execution')publishExecution=el.checked;
    if(el.id==='kw-cite-source'){const f=$('#kw-cite-fragment');f.innerHTML='';f.disabled=!el.value;$('#kw-cite-quote').value='';if(el.value){const r=resolveSource(el.value);f.dataset.revision=r.revision.revision;f.dataset.extraction=r.extraction_id||'';f.innerHTML=options((r.revision.parsed?.fragments||[]).map((p,i)=>[p.id,(i+1)+'. '+p.text.slice(0,90)]),'');}return;}
    if(el.id==='kw-cite-fragment'){const s=$('#kw-cite-source').value;$('#kw-cite-quote').value=el.value?resolveSource(s,el.dataset.revision,el.value,el.dataset.extraction).fragment.text:'';return;}
    if(el.id==='kw-canvas-view'){graphLocation(null);drag=null;connection=null;G.view=el.value;G.focus=null;G.selected=null;G.inspector=false;G.limit=80;saveView();rerender();drawGraph(true);return;}
    if(el.hasAttribute('data-all-ends')){const holder=el.closest('[data-candidate],#kw-asset-fields,#kw-source-asset,#kw-merged-fields');if(holder)updateEnds(holder);}
    if(el.dataset.field==='relation_type'){const holder=el.closest('[data-candidate],#kw-asset-fields,#kw-source-asset,#kw-merged-fields');if(holder)updateEnds(holder);if(holder?.querySelector('[data-physical]'))holder.querySelector('[data-physical]').hidden=el.value!=='physical_fk';}
    if(el.id==='kw-source-action')$('#kw-source-asset').hidden=el.value!=='adopt';
    if(el.id==='kw-review-filter'){reviewPageIndex=0;reviewFilter=el.value;rerender();}if(el.id==='kw-review-batch'){reviewPageIndex=0;reviewBatch=el.value;rerender();}
    const graphField={'kw-domain':'domain','kw-kind':'kind','kw-status':'status'}[el.id];if(graphField){setConnection(null);G[graphField]=el.value;G.limit=80;saveView();drawGraph();}
    if(dialog?.assetDraftKey!==undefined&&el.closest('#kw-form'))assetDrafts.set(dialog.assetDraftKey,{asset:readAsset($('#kw-asset-fields'),dialog.assetOriginal,false),declaration:$('#kw-manual-evidence').value,baseRevision:dialog.baseRevision});
    if(el.matches('#kw-asset-fields [data-field="kind"]')){const fields=$('#kw-asset-fields'),a=readAsset(fields,dialog.assetOriginal);fields.innerHTML=assetFields(a,{allowNewEnds:true});$('#kw-dialog .dialog-head h2').textContent=newAssetTitle(a.kind);previewRelation(fields);}
    if(el.id==='kw-identity-mode')$('#kw-merged-fields').hidden=el.value!=='merge';
    if(el.id==='kw-identity-target'){const a=asset(el.value);$('#kw-identity-comparison').innerHTML=a?tr`<div class="notice"><b>${esc(a.name)} · ${esc(a.domain)}</b><p>${esc(a.definition)}</p><p>范围：${esc(scopeText(a.scope))}</p><dl>${Object.entries(a.properties||{}).map(([k,v])=>`<dt>${esc((propertyFields[a.kind]||[]).find(x=>x[0]===k)?.[1]||(k==='knowledge_gaps'?tr('仍待明确的问题'):k==='unresolved_conflicts'?say('待裁决的冲突','Unresolved conflict'):k==='conflict_resolutions'?say('裁决记录','Recorded decisions'):k))}</dt><dd>${esc(typeof v==='object'?fmt(v):v)}</dd>`).join('')}</dl><p>引用此项的定义：${S.assets.filter(x=>x.from===a.id||x.to===a.id||(x.refs||[]).includes(a.id)).length} 项</p></div>`:'';}
  });
  function svgPoint(e){const s=$('#kw-graph'),p=s.createSVGPoint();p.x=e.clientX;p.y=e.clientY;const result=p.matrixTransform(s.getScreenCTM().inverse());result.x-=Number(s.dataset.offsetX||0);result.y-=Number(s.dataset.offsetY||0);return result;}
  function setConnection(next){
    if(!connection&&!next)return;
    connection=next;lastGraphClick=null;
    const hint=$('#kw-connect-hint'),message=$('#kw-connect-message');
    if(hint)hint.hidden=!next;if(message)message.textContent=connectionMessage();
    $('#kw-canvas')?.classList?.toggle('is-connecting',!!next);
    $('[data-kw="connect"]')?.setAttribute('aria-pressed',String(!!next));
    for(const node of $$('#kw-graph [data-kw-node]'))node.classList.toggle('connection-start',node.dataset.kwNode===next?.start);
  }
  function chooseEndpoint(id){
    if(!connection)return;
    if(connection.start)connect(connection.start,id);
    else setConnection({start:id});
  }
  function connect(start,end){
    setConnection(null);const a=asset(start),b=asset(end);if(!a||!b)return;
    openAsset(null,{kind:'relation',from:start,to:end,domain:a.domain||b.domain||'',scope:a.scope||'',relation_type:'business'});
  }
  function zoomCanvas(factor,clientX,clientY){
    const canvas=$('#kw-canvas'),svg=$('#kw-graph');
    if(!canvas||!svg)return;
    const old=G.zoom,next=Math.max(Math.min(.05,old),Math.min(3,old*factor));
    if(Math.abs(next-old)<.00001)return;
    const rect=canvas.getBoundingClientRect?.(),x=rect&&clientX!==undefined?clientX-rect.left:canvas.clientWidth/2,
      y=rect&&clientY!==undefined?clientY-rect.top:canvas.clientHeight/2;
    const localX=(canvas.scrollLeft+x)/old-Number(svg.dataset.offsetX||0),localY=(canvas.scrollTop+y)/old-Number(svg.dataset.offsetY||0);
    keepFitted=false;fitAllNodes=false;G.zoom=next;saveView();drawGraph();
    canvas.scrollLeft=Math.max(0,(localX+Number(svg.dataset.offsetX||0))*next-x);
    canvas.scrollTop=Math.max(0,(localY+Number(svg.dataset.offsetY||0))*next-y);
  }
  document.addEventListener('wheel',e=>{
    if(!(e.ctrlKey||e.metaKey)||!e.target.closest?.('#kw-canvas')||!e.deltaY)return;
    e.preventDefault();const pixels=e.deltaY*(e.deltaMode===1?16:e.deltaMode===2?250:1);
    zoomCanvas(Math.exp(-Math.max(-160,Math.min(160,pixels))*.0025),e.clientX,e.clientY);
  },{passive:false});
  document.addEventListener('pointerdown',e=>{
    for(const menu of $$('details.kw-tool-menu[open]')){
      if(!menu.contains(e.target))menu.open=false;
    }
    const canvas=e.target.closest('#kw-canvas');if(!canvas||e.button>1||drag)return;
    const node=e.target.closest('[data-kw-node]'),edge=e.target.closest('[data-kw-edge]');
    if(connection&&e.button!==1){
      if(node)chooseEndpoint(node.dataset.kwNode);
      e.preventDefault();return;
    }
    if(edge&&e.button!==1){activateGraphAsset(edge.dataset.kwEdge);return;}
    canvas.setPointerCapture?.(e.pointerId);
    if(!node||e.button===1){drag={pan:true,pointerId:e.pointerId,x:e.clientX,y:e.clientY,left:canvas.scrollLeft,top:canvas.scrollTop,middle:e.button===1};e.preventDefault();return;}
    const id=node.dataset.kwNode,item=asset(id),nodes=graphData().nodes;
    drag={id,pointerId:e.pointerId,start:svgPoint(e),base:point(item,nodes.indexOf(item)),port:e.target.classList.contains('kw-port'),moved:false,before:currentLayout()};
    e.preventDefault();
  });
  document.addEventListener('click',e=>{
    const item=e.target.closest('details.kw-tool-menu button');
    if(item)item.closest('details.kw-tool-menu').open=false;
  });
  function previewDraggedNode(position){
    const svg=$('#kw-graph'),nodes=svg.querySelectorAll('[data-kw-node]');
    const moving=[...nodes].find(node=>node.dataset.kwNode===drag.id);
    moving?.setAttribute('transform',`translate(${position.x},${position.y})`);
    if(!drag.incident){
      const input=graphInput(graphData());
      const incident=input.edges.filter(edge=>edge.from===drag.id||edge.to===drag.id);
      const parts=new Map(incident.map(edge=>[edge.id,[]]));
      for(const group of svg.querySelectorAll('[data-render-edge]'))parts.get(group.dataset.renderEdge)?.push(group);
      drag.incident=incident.map(edge=>({edge,parts:parts.get(edge.id)}));
    }
    for(const {edge,parts} of drag.incident){
      const get=id=>S.layout['semantic:'+G.view+':'+id]||drag.before['semantic:'+G.view+':'+id];
      const from=get(edge.from),to=get(edge.to),route=graphPlan.routes[edge.id];
      if(!route||!from||!to)continue;
      const dx=position.x-drag.base.x,dy=position.y-drag.base.y;
      const points=route.points.map((p,i)=>((i===0&&edge.from===drag.id)||(i===route.points.length-1&&edge.to===drag.id))?{x:p.x+dx,y:p.y+dy}:p);
      for(const group of parts){
        for(const path of group.querySelectorAll('.kw-edge,.kw-edge-hit,.kw-ref-edge'))path.setAttribute('d',edgePath(points));
        group.querySelector('.kw-edge-label')?.setAttribute('transform',`translate(${dx/2},${dy/2})`);
      }
    }
  }
  document.addEventListener('pointermove',e=>{
    if(!drag||e.pointerId!==drag.pointerId||!$('#kw-graph'))return;
    if(drag.pan){const c=$('#kw-canvas');if(Math.abs(drag.x-e.clientX)+Math.abs(drag.y-e.clientY)>4)keepFitted=false;c.scrollLeft=drag.left+drag.x-e.clientX;c.scrollTop=drag.top+drag.y-e.clientY;return;}
    const p=svgPoint(e);drag.moved=drag.moved||Math.abs(p.x-drag.start.x)+Math.abs(p.y-drag.start.y)>4;
    if(!drag.moved)return;
    if(drag.port){
      $('#kw-temp-edge')?.remove();
      const content=$('#kw-graph .kw-graph-content');
      content?.insertAdjacentHTML('beforeend',`<path id="kw-temp-edge" d="M${drag.base.x+NODE_WIDTH},${drag.base.y+NODE_HEIGHT/2} L${p.x},${p.y}" stroke="#176c56" fill="none" stroke-dasharray="5 4" pointer-events="none"/>`);
    }else{
      const position={x:Math.max(8,drag.base.x+p.x-drag.start.x),y:Math.max(8,drag.base.y+p.y-drag.start.y)};
      if(!drag.incident)S.layout={...drag.before,...S.layout};
      S.layout['semantic:'+G.view+':'+drag.id]=position;previewDraggedNode(position);
    }
  });
  document.addEventListener('pointerup',async e=>{
    if(!drag||e.pointerId!==drag.pointerId)return;
    const d=drag;drag=null;$('#kw-temp-edge')?.remove();
    if(d.pan){if(!d.middle&&Math.abs(d.x-e.clientX)+Math.abs(d.y-e.clientY)<=4)selectGraphAsset(null);return;}
    if(d.port){
      const end=document.elementFromPoint(e.clientX,e.clientY)?.closest('[data-kw-node]')?.dataset.kwNode;
      if(d.moved&&end)connect(d.id,end);else setConnection({start:d.id});
    }else if(d.moved){
      try{await C.api('layout',{positions:S.layout});layoutUndo.push(d.before);drawGraph();cachePlan(graphInput(graphData()),graphPlan);}
      catch(err){S.layout=d.before;drawGraph();C.notify(say('位置保存失败，已恢复。','Could not save the position. The previous layout was restored.')+' '+err.message);}
    }else activateGraphAsset(d.id);
  });
  document.addEventListener('pointercancel',e=>{if(drag&&drag.pointerId===e.pointerId){if(drag.id&&!drag.port&&drag.moved)S.layout=drag.before;drag=null;$('#kw-temp-edge')?.remove();drawGraph();}});
  document.addEventListener('dblclick',e=>{
    if(connection||document.querySelector('dialog[open]'))return;
    const node=e.target.closest('[data-kw-node]'),edge=e.target.closest('[data-kw-edge]');
    if(node||edge)openAsset(node?.dataset.kwNode||edge.dataset.kwEdge);
  });
  document.addEventListener('keydown',e=>{
    if(activePage!=='graph'||document.querySelector('dialog[open]'))return;
    if(e.key==='Enter'&&(e.target.id==='kw-graph-search'||e.target.id==='kw-canvas-search')&&G.query){
      const matches=filteredAssets();
      if(matches.length===1){e.preventDefault();selectGraphAsset(matches[0].id);}
      return;
    }
    if(e.key==='Escape'){
      if(connection){e.preventDefault();setConnection(null);$('[data-kw="connect"]')?.focus();return;}
      const menu=$('details.kw-tool-menu[open]');if(menu){e.preventDefault();menu.open=false;menu.querySelector('summary')?.focus();return;}
      if(G.expanded){G.expanded=false;G.inspector=false;saveView();rerender();drawGraph(true);$('[data-kw="expand-canvas"]')?.focus();}
      return;
    }
    if(e.key!=='Enter'&&e.key!==' ')return;
    const node=e.target.closest('[data-kw-node]'),edge=e.target.closest('[data-kw-edge]'),row=e.target.closest('tr[data-kw="select"]');
    if(!node&&!edge&&!row)return;
    e.preventDefault();
    if(connection){if(node)chooseEndpoint(node.dataset.kwNode);return;}
    const id=node?.dataset.kwNode||edge?.dataset.kwEdge||row?.dataset.id;
    if(e.key==='Enter'&&!row)openAsset(id);else{
      selectGraphAsset(id);
      const selected=Array.from(document.querySelectorAll('[data-kw-node],[data-kw-edge][tabindex],tr[data-kw="select"]')).find(el=>(el.dataset.kwNode||el.dataset.kwEdge||el.dataset.id)===id);
      selected?.focus();
    }
  });
  function saveDelivery(){try{sessionStorage.setItem('kw-delivery:'+S.project_id,JSON.stringify({ids:[...deliverySelection],scoped:scopedDelivery}));}catch(_){C.notify(tr('当前交付选择无法在刷新后恢复，请保持此页完成交付。'));}}
  function deliver(ids){deliverySelection=new Set(ids);scopedDelivery=true;saveDelivery();publishResult=null;C.go('publish');}
  function locate(id){graphLocation(id);Object.assign(G,{selected:id,focus:id,inspector:true,view:'all',mode:'graph',domain:'',kind:'',status:'',query:'',limit:80});saveView();C.go('graph');}
  function bindings(id){
    const current=asset(id);
    if(!current||current.kind!=='metric')throw Error('Choose a metric / 请选择指标');
    const original=copy(current),view=window.QueryBindings.render(original,S.assets);
    const t=(zh,en)=>window.UIText?.language==='zh'?zh:en;
    openDialog(t('核对查询口径 · ','Review query meaning · ')+original.name,
      view.html+`<h3>${t('原文与依据','Sources and evidence')}</h3>`+evidenceHtml(original.evidence),
      view.editable?async(confirmed,d)=>{
        if(JSON.stringify(asset(id))!==JSON.stringify(original))throw Error(t('指标已变化。输入保留，请先核对最新定义；重新打开本表单后再修改，避免覆盖他人修改。','The metric changed. Inputs are retained; inspect the latest definition and reopen this review before editing to avoid overwriting changes.'));
        const payload=window.QueryBindings.read($('#kw-form'),original);
        await transact('binding:'+id,'edit',payload,d.baseRevision);
        C.notify(t('口径已保存，请重新检查相关问题','Bindings saved; recheck affected questions'));
      }:null,{confirmLabel:t('确认口径并保存','Confirm meaning and save'),assetOriginal:original});
    if(view.editable)window.QueryBindings.wire($('#kw-form'),view.fields);
  }
  return {cancelLayout:()=>runningWorker?.cancel(),previewExternal,idle:()=>!drag&&!connection&&!$('#kw-dialog[open]')&&!pending.size,revision:()=>S.revision,configure,update,render,mount,transact,pendingHtml,scopeFields,readScope,scopeText,deliver,locate,bindings};
})();
