'use strict';
const $ = s => document.querySelector(s), $$ = s => [...document.querySelectorAll(s)];
const esc = v => String(v ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const token = $('meta[name="session-token"]').content;
const menus = [['home','场景与工作台'],['data','数据与资料'],['model','语义建模'],['check','检查与试算'],['delivery','交付与版本'],['issues','问题与演进']];
const names = {datasets:'数据集',entities:'业务对象',relationships:'数据关联',relations:'业务关系',metrics:'指标',templates:'明细模板',concepts:'业务概念',constraints:'数据约束'};
const states = {pass:'已通过',fail:'未通过',error:'执行错误',blocked:'存在阻断',review:'待核对',not_ready:'尚未验证',attention:'需关注',computed_only:'仅完成计算',declared:'已声明',declared_only:'仅结构声明',needs_input:'待补齐',unknown:'证据不足',executed_only:'已调用，待核对',model_mismatch:'引擎模型不一致'};
Object.assign(states,{selected:'已选择，未执行',consumer_not_completed:'消费者未完成'});
let state, page = location.hash.slice(1) || 'home', graphMode = 'entities', activeKind = 'entities', selected = null, connection = null, positions = {}, report = null, assetEdit = null;
let fieldRows = [];
let bundleForm={metric:'',columns:[],limit:50,offset:0,expected:''};
const clone = v => JSON.parse(JSON.stringify(v));
const comma = v => Array.isArray(v)?v.join(','):v&&typeof v==='object'?Object.keys(v).join(','):String(v||'');
function notify(msg) { $('#toast').textContent = msg; $('#toast').classList.add('show'); clearTimeout(notify.timer); notify.timer=setTimeout(()=>$('#toast').classList.remove('show'),4500); }
async function api(path, data) {
  const res = await fetch('/api/'+path, {method:data===undefined?'GET':'POST',headers:{'X-Workbench-Token':token,...(data===undefined?{}:{'Content-Type':'application/json'})},body:data===undefined?undefined:JSON.stringify(data)});
  const body = await res.json(); if (!res.ok) throw new Error(body.error || '操作失败'); return body;
}
async function reload() { state=await api('state'); if(report?.id){const saved=state.runs.find(r=>r.id===report.id);if(saved)report={...saved.report,id:saved.id,stale:saved.stale};}else if(report?.source_revision!==undefined){report.stale=report.source_revision!==state.revision;} positions=state.layout; $('#project-name').textContent=state.document.name; $('#revision').textContent='项目版本 '+state.revision; render(); }
async function mutate(path,data) { const r=await api(path,{revision:state.revision,...data}); await reload(); return r; }
const badge = (value, label) => `<span class="badge ${esc(value)}">${esc(label || states[value] || value)}</span>`;
const btn = (label, action, extra='', cls='') => `<button class="${cls}" data-action="${action}" ${extra}>${label}</button>`;
const empty = (title, detail, action='') => `<div class="empty"><b>${title}</b><p>${detail}</p>${action}</div>`;
function assets(kind) { return kind==='entities'||kind==='relations' ? state.document.model.ontology?.[kind]||[] : state.document.model[kind]||[]; }
function ident(kind,x) { if(kind==='entities')return x.uid||x.name; if(kind==='relations')return x.id||`${x.from}->${x.to}:${x.predicate}`; if(kind==='relationships')return x.id||`${x.from}->${x.to}:${(Array.isArray(x.join_key)?x.join_key:[x.join_key||'']).join(',')}`; return x[{datasets:'name',concepts:'term'}[kind]||'id']; }
const attr = (kind,key) => `data-kind="${kind}" data-key="${esc(key||'')}"`;
const title = (heading, sub, action='') => `<div class="page-head"><div><span class="eyebrow">SEMANTIC WORKSPACE</span><h1>${heading}</h1><div class="sub">${sub}</div></div>${action}</div>`;
function go(next) { page=next;location.hash=next;selected=null;connection=null;render(); }
function render() {
  if(!state)return;
  if(!menus.some(x=>x[0]===page))page='home';
  $('nav').innerHTML=menus.map(([id,label],i)=>btn(`<span class="num">0${i+1}</span><span class="nav-label">${label}</span>`,'navigate',`data-page="${id}"`,id===page?'active':'')).join('');
  $('#breadcrumb').textContent='工作空间 / '+menus.find(x=>x[0]===page)[1];
  $('#main').innerHTML=({home:homePage,data:dataPage,model:modelPage,check:checkPage,delivery:deliveryPage,issues:issuesPage}[page])();
  if(state.document.sample?.provenance==='demo')$('#main').insertAdjacentHTML('afterbegin','<div class="notice warning">当前数据是模拟 / 演示快照，计算结果仅供练习或工具核对，不代表真实业务数据。</div>');
  if(page==='model')drawGraph();
}
function homePage() {
  const scenes=state.scenarios;
  return title('从一个问题，建立业务语义','导入已有结构，确认业务含义，再用数据和预期结果逐步验证。',btn('＋ 新建场景','scene','','primary'))+
    firstTaskCard()+
    `<div class="grid cols4">${[['业务对象',assets('entities').length,'表达业务身份与属性'],['数据集',assets('datasets').length,'映射已有表与字段'],['指标',assets('metrics').length,'保留计算与业务口径'],['待补齐',state.gaps.length,'有责任角色的具体问题']].map(([l,n,d])=>`<div class="card metric-card"><span>${l}</span><strong>${n}</strong><small>${d}</small></div>`).join('')}</div>`+
    `<div class="section-title"><h2>当前场景</h2><span class="muted">从问题圈定本次范围</span></div>`+
    (scenes.length?`<div class="grid cols2">${scenes.map(s=>`<div class="card scene-card">${badge(s.status)}<h3>${esc(state.profiles[s.profile].label)}</h3><p class="question">${esc(s.question)}</p><div class="privacy">${esc(s.datasets?.join(' · ')||'尚未绑定数据集')}</div>${s.missing.length?`<ul>${s.missing.slice(0,3).map(x=>`<li>${esc(x)}</li>`).join('')}</ul><div class="privacy">共 ${s.missing.length} 项待补齐</div>`:`<p class="privacy">${esc(s.runtime)}</p>`}${btn('编辑场景','scene',`data-id="${s.id}"`,'small')}</div>`).join('')}</div>`:`<div class="card">${empty('你希望数据帮助谁，完成什么？','可分别建立指标问数、自由问数、办事、政策适用和分析决策场景。',btn('建立第一个场景','scene'))}</div>`)+
    `<div class="section-title"><h2>工作路径</h2></div><div class="steps">${[['01','带入资料','导入结构、业务定义和演示快照','data'],['02','组织语义','编辑对象、属性和关系，补齐口径','model'],['03','核对证据','检查关联、约束和完整预期结果','check'],['04','交付与迭代','导出模型、字典、证据和项目备份','delivery']].map(([i,t,d,p])=>`<div class="step"><span>STEP ${i}</span><h3>${t}</h3><p>${d}</p>${btn('打开 →','navigate',`data-page="${p}"`,'quiet')}</div>`).join('')}</div>`;
}
function firstTaskCard(){
 const tutorial=state.document.tutorial,canCompute=assets('metrics').length&&state.document.sample;
 if(tutorial)return `<div class="hero"><div><span class="eyebrow">合成练习 · 已准备模型与快照</span><h2>${tutorial.kind==='traffic'?'为什么同一份数据会得到 3、2、1？':'130 元来自哪两笔订单？'}</h2><p>${tutorial.kind==='traffic'?'A、A、空值三条输入记录：记录行数、字段非空数、去重非空数含义不同。先看数值和明细，再查看指标定义。':'练习限定 T1 主体和已支付订单；退款单与其他主体排除。先看数值和明细，再查看指标定义。'}</p>${btn('开始数值与明细练习','first-query','','primary')}<p class="privacy">这是学习样例；没有填写独立预期时，只记计算完成。</p></div></div>`;
 return `<div class="hero"><div><span class="eyebrow">先完成一个业务问题</span><h2>${canCompute?'查看一个指标的数值和明细':assets('datasets').length?'已有结构，补齐当前问题需要的定义':'带入你手上的资料'}</h2><p>${canCompute?'选择一个已有指标，核对它包含哪些记录，再交付给应用或 Agent。':'可以先提供业务问题和已有资料。工作台可导入模型、SQLite/MySQL DDL；其他文档先交给使用本 skill 的 Agent 整理。'}</p>${canCompute?btn('选择指标开始核对','first-query','','primary'):btn(assets('datasets').length?'进入语义建模':'导入已有资料','navigate',`data-page="${assets('datasets').length?'model':'data'}"`,'primary')}<p class="privacy">交给 Agent 的一句话：我要解决【业务问题】，已有资料在【路径】，请先复用已知内容，只问影响结果的缺口。</p></div></div>`;
}
function dataPage() {
  return title('数据与资料','保留原始输入与来源。导入结构不会自动确认业务口径，也不会执行上传的 SQL。')+
    `<div class="grid cols2">${[['ddl','数据库结构','SQLite / MySQL CREATE TABLE 文件','.sql'],['model','已有语义模型','semantic.yaml，扩展字段完整保留','.yaml,.yml,.json'],['sample','数据快照','独立 SQLite 一致快照，最大 32 MB','.db,.sqlite,.sqlite3'],['inventory','指标、规则或案例清单','JSON 清单保留为原始资料，由 skill 对齐到模型','.json']].map(([k,t,d,accept])=>`<div class="card"><h3>${t}</h3><p class="sub">${d}</p><div class="import-card"><input type="file" id="file-${k}" aria-label="选择${t}文件" accept="${accept}">${['ddl','model'].includes(k)?`<label><input type="checkbox" id="replace-${k}"> 替换当前模型（保留历史版本）</label>`:''}${k==='sample'?`<label>数据来源<select id="provenance"><option value="unknown">来源待核实</option><option value="demo">模拟 / 演示数据</option><option value="deidentified">生产脱敏快照（用户声明）</option><option value="production">生产数据（用户声明）</option></select></label><p class="sub">请先用 SQLite backup / checkpoint 导出一致快照，不要只复制仍在 WAL 写入的主库文件。</p>`:''}${btn('导入'+t,'import',`data-kind="${k}"`,'primary small')}</div></div>`).join('')}</div>`+
    `<div class="notice">SQLite 是本地项目的统一存储。模型、修改记录、资料与测试证据在同一个项目中；导出的 YAML 是交付快照。</div><div class="section-title"><h2>已导入资料</h2><span class="muted">${state.document.sources.length} 份</span></div><div class="card">${state.document.sources.length?`<div class="table-wrap"><table><thead><tr><th>文件</th><th>类型 / 来源</th><th>指纹</th><th>导入说明</th></tr></thead><tbody>${state.document.sources.map(s=>`<tr><td>${esc(s.filename)}</td><td>${esc(s.kind)}${s.provenance?' / '+esc(s.provenance):''}</td><td><code>${esc(s.sha256.slice(0,12))}</code></td><td>${esc(s.snapshot_note||s.note||s.tables?.join('、')||'已保留原始资料')}${s.parse_failures?.length?`<p class="error">${s.parse_failures.length} 张表解析失败；请核查原 DDL</p>`:''}</td></tr>`).join('')}</tbody></table></div>`:empty('还没有导入资料','先导入一份 DDL 或已有模型。')}</div>`;
}
function modelPage() {
  return title('语义建模','把业务对象与物理数据对齐。虚线表示未落地的业务关系；数据连线需要明确键与基数。','<div class=header-actions>'+btn('从元数据补充语义草案','derive','','small')+btn('＋ '+names[graphMode],'edit',attr(graphMode,''),'primary')+'</div>')+
    `<div class="graph-shell"><div class="graph-main"><div class="toolbar"><div class="toggle">${btn('业务视图','graph-mode','data-mode="entities"',graphMode==='entities'?'active':'')}${btn('数据视图','graph-mode','data-mode="datasets"',graphMode==='datasets'?'active':'')}</div>${btn(connection?'取消连线':'连线','connect','','small')}<input id="graph-search" placeholder="查找对象或数据集" aria-label="查找图中节点" style="width:175px"><span class="spacer"></span>${btn('整理布局','arrange','','quiet small')}</div><div class="graph-wrap"><svg id="graph" aria-label="可编辑语义图"></svg></div><div class="graph-hint">拖动节点调整布局 · 点击查看属性 · 双击编辑 · 从节点圆点拖到另一节点建立关系</div></div><aside class="graph-side" id="inspector"></aside></div>`+
    `<div class="asset-tabs">${Object.entries(names).map(([k,n])=>btn(`${n} <small>${assets(k).length}</small>`,'asset-tab',`data-kind="${k}"`,activeKind===k?'active':'')).join('')}</div><div class="card slim"><div class="row between"><h3>${names[activeKind]}</h3>${btn('＋ 新建','edit',attr(activeKind,''),'small')}</div>${assetTable(activeKind)}</div>`+
    `<div class="section-title"><h2>下一步补齐</h2><span class="muted">${state.gaps.length} 个具体问题</span></div><div class="card">${state.gaps.length?state.gaps.slice(0,20).map(g=>`<div class="gap"><div><span class="privacy">${esc(names[g.kind])} · ${esc(g.key)} · ${esc(g.role)}</span><h3>${esc(g.question)}</h3></div>${btn('填写答案','answer',`data-gap="${g.id}"`,'small')}</div>`).join('')+(state.gaps.length>20?'<p class="muted">先显示前 20 项，完成后继续展示。</p>':''):empty('基础语义缺口已补齐','继续检查具体场景的适用条件、数据质量与预期结果。')}</div>`;
}
function assetTable(kind) {
  const rows=assets(kind);
  return rows.length?`<div class="table-wrap"><table class="asset-table"><thead><tr><th>名称 / 标识</th><th>说明 / 映射</th><th></th></tr></thead><tbody>${rows.map(x=>`<tr><td>${esc(x.name||x.term||x.predicate||ident(kind,x))}<div class="privacy">${esc(ident(kind,x))}</div></td><td>${esc(x.grain||x.note||x.caliber?.note||x.dataset||[x.from,x.to].filter(Boolean).join(' → ')||'待补充')}</td><td>${btn('编辑','edit',attr(kind,ident(kind,x)),'small')}</td></tr>`).join('')}</tbody></table></div>`:empty('还没有'+names[kind],'可以先建立草案，再逐步补齐。');
}
function checkPage() {
  const runs=state.runs, latest=runs.find(r=>r.kind==='check');
  return title('检查与试算','先核对一个指标的数值与明细；模型、数据和消费者检查按需要展开。')+bundleCard()+'<details class="advanced-checks"><summary>进阶检查：模型与数据、单独指标、现有问数引擎</summary>'+btn('运行模型与数据检查','check','','small')+
    `<div class="grid cols3">${[['模型结构',latest?.report.model.status,'静态声明、引用与口径'],['数据质量',latest?.report.data.status,'已声明约束的快照扫描'],['关联关系',latest?.report.links.status,'键、基数与显式查询路径']].map(([t,s,d])=>`<div class="card"><div class="row between"><h3>${t}</h3>${badge(latest?.stale?'not_ready':s||'not_ready',latest?.stale?'证据已过期':null)}</div><p class="sub">${d}</p></div>`).join('')}</div>`+
    `<div class="grid cols2" style="margin-top:20px"><div class="card"><h2>指标直算</h2><p class="sub">执行指标已声明的完整口径。时间、组织等范围以指标定义为准。</p><label>选择指标<select id="query-metric"><option value="">选择…</option>${assets('metrics').map(m=>`<option value="${esc(m.id)}">${esc(m.name||m.id)}</option>`).join('')}</select></label><label>预期数值（可留空）<input id="query-expected" placeholder="如 0.6667；完整结果可填 [[11,25]]"></label>${btn('执行并核对','query','','primary small')}<p class="privacy">未填写预期只记为“完成计算”，不记为验证通过。</p></div><div class="card"><h2>现有问数引擎</h2><p class="sub">连接本机 Java 演示接口 /api/model 与 /api/ask，核对模型和完整结果。</p><label>本机地址<input id="consumer-endpoint" placeholder="http://127.0.0.1:17100"></label><label>业务问题<input id="consumer-question" placeholder="输入完整问题"></label><label>完整预期结果（可留空）<input id="consumer-expected" placeholder="如 [[11,25]]"></label>${btn('调用并核对','consumer','','small')}</div></div>`+
    `</details><div id="current-report">${report?renderReport(report):''}</div><div class="section-title"><h2>历史证据</h2><span class="privacy">修改语义后重新验证</span></div><div class="card">${runs.length?runs.map(r=>`<div class="gap"><div><h3>${esc({check:'模型与数据检查',query:'指标直算',bundle:'指标与明细核对',consumer:'消费者核对'}[r.kind]||r.kind)} ${badge(r.stale?'not_ready':r.report.status,r.stale?'已过期':null)}</h3><p>版本 ${r.revision} · ${esc(r.created.slice(0,19))} · ${esc(r.report.metric||r.report.question||'声明范围')}</p></div>${btn('查看报告','report',`data-id="${r.id}"`,'small')}</div>`).join(''):empty('尚无检查记录','导入模型与快照后，运行上方检查。')}</div>`;
}
function bundleCard() {
  const source=assets('datasets').find(d=>d.name===assets('metrics').find(m=>m.id===bundleForm.metric)?.dataset);
  const fieldOptions=(source?.fields||[]).map(f=>`<option value="${esc(f.name)}" ${bundleForm.columns.includes(f.name)?'selected':''}>${esc(f.cn||f.name)} (${esc(f.name)})</option>`).join('');
  return `<section class="card" style="margin-top:20px"><h2>指标与明细核对</h2><p class="sub">按同一口径、同一快照计算数值并读取贡献明细。去重计数不等于明细行数；分页只限制明细展示。</p><div class="grid cols2"><div><label>指标 *<select id="bundle-metric"><option value="">选择…</option>${assets('metrics').map(m=>`<option value="${esc(m.id)}" ${m.id===bundleForm.metric?'selected':''}>${esc(m.name||m.id)}</option>`).join('')}</select></label><label>返回字段 *<select id="bundle-columns" multiple size="5" aria-describedby="bundle-field-help">${fieldOptions}</select></label><p id="bundle-field-help" class="privacy">先选指标，再选其来源字段；可用 Ctrl / Shift 多选。本工具不授予数据权限。</p></div><div><div class="grid cols2"><label>每页条数<input id="bundle-limit" type="number" min="1" max="500" value="${bundleForm.limit}"></label><label>跳过条数<input id="bundle-offset" type="number" min="0" value="${bundleForm.offset}"></label></div><label>独立预期（可留空，JSON）<textarea id="bundle-expected" placeholder='{"metric_value":1,"matched_row_count":3,"detail_rows":[["A"],["A"],[null]]}'>${esc(bundleForm.expected)}</textarea></label><p class="privacy">预期须独立准备；留空只记计算完成。明细按来源声明的唯一主键排序。</p></div></div><div class="row">${btn('执行数值与明细核对','bundle','','primary')}${btn('查看供 Agent 使用的上下文','context','','')}</div></section>`;
}
function bundleRequest(){return {metric:$('#bundle-metric').value,columns:[...$('#bundle-columns').selectedOptions].map(o=>o.value),limit:Number($('#bundle-limit').value),offset:Number($('#bundle-offset').value)};}
function renderReport(r) {
  return `<div class="card report"><div class="row between"><h2>${r.context?'上下文选择结果':'执行结果'}</h2>${badge(r.stale?'not_ready':r.status,r.stale?'证据已过期':null)}</div>${r.stale?'<p class="notice warning">模型、数据或场景已变化；此报告只记录当时结果，请重新核对当前版本。</p>':''}${r.error?`<p class="notice warning">${esc(r.error.code)}：${esc(r.error.message)}</p>`:''}${r.detail_rows?`<p>指标值：<strong>${esc(r.metric_value??'NULL')}</strong>${r.metric_unit?" "+esc(r.metric_unit):""} · 符合条件记录：${esc(r.matched_row_count)} 条 · 本页 ${r.detail_rows.length} 条</p><div class="table-wrap"><table><thead><tr>${r.detail_columns.map(c=>`<th>${esc(c)}</th>`).join('')}</tr></thead><tbody>${r.detail_rows.map(row=>`<tr>${row.map(v=>`<td>${esc(v??'NULL')}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`:''}${r.context?`<p>只含当前指标及声明依赖。来源模式：快照；引用 ${r.citations.length} 处。</p><ul>${r.boundaries.map(x=>`<li>${esc(x)}</li>`).join('')}</ul>`:''}${r.model?`<div class="grid cols2"><div><h3>模型诊断</h3><ul class="list">${[...r.model.errors,...r.model.warnings].map(x=>`<li>${esc(x)}</li>`).join('')||'<li>没有发现结构诊断项</li>'}</ul></div><div><h3>下一步</h3><ul class="list">${r.next.map(x=>`<li>${esc(x)}</li>`).join('')||'<li>继续核对业务问题的预期结果与适用范围</li>'}</ul></div></div><h3>数据约束</h3>${r.data.records.length?`<div class="table-wrap"><table><thead><tr><th>规则</th><th>状态</th><th>检查行 / 违规</th><th>说明</th></tr></thead><tbody>${r.data.records.map(x=>`<tr><td>${esc(x.id)}</td><td>${badge(x.status)}</td><td>${x.checked_rows??'—'} / ${x.violation_count??'—'}</td><td>${esc(x.detail||'')}</td></tr>`).join('')}</tbody></table></div>`:'<p class="muted">没有执行约束检查，不能据此证明数据干净。</p>'}`:`<p>${esc(r.detail||(typeof r.scope==='string'?r.scope:r.scope?.detail_meaning)||'')}</p>${r.rows?`<h3>完整结果</h3><pre class="code">${esc(JSON.stringify(r.rows))}</pre>`:''}${r.display_value!==undefined?`<p>展示值：<strong>${esc(Number(r.display_value).toLocaleString('zh-CN',{maximumFractionDigits:4}))} ${esc(r.unit)}</strong></p>`:''}${r.expected?`<p>预期：<code>${esc(JSON.stringify(r.expected))}</code></p>`:''}${r.model_match!==undefined?`<p>消费者模型：${r.model_match?'已知字段投影相符':'与当前项目不同：'+esc(r.mismatch_sections.join('、'))}</p>`:''}`}
    <p class="privacy">${esc(r.boundary||'结果仅对应所选模型与本地快照，不能代替生产验收。')}</p><details><summary>查看完整证据与执行范围</summary><pre class="code">${esc(JSON.stringify(r,null,2))}</pre></details></div>`;
}
function deliveryPage() {
  return title('交付与版本','交付包从当前模型生成。证据是否过期、检查覆盖到哪里，随包保留。')+
    `<div class="grid cols2"><div class="card"><span class="eyebrow">DELIVERY</span><h2>语义交付包</h2><p class="sub">可离线打开的人工核验页（思维导图、业务说明与结果核对），以及模型、字典、场景、记录和证据。</p><div class="notice">不包含原始资料和数据快照。模型与报告仍可能包含业务信息，分享前请按接收方范围审阅。</div>${btn('下载交付 ZIP','download','data-type="export"','primary')} ${btn('下载可视化验收页','download','data-type="review"')}</div><div class="card"><span class="eyebrow">BACKUP</span><h2>可继续编辑的项目备份</h2><p class="sub">包含 project.sqlite：模型历史、图布局、原始资料、数据快照与证据。</p><div class="notice warning">这是私人项目备份。恢复时解压到新目录，用该目录启动工作台。</div>${btn('下载私人项目备份','download','data-type="backup"')}</div></div>`+
    `<div class="section-title"><h2>版本记录</h2><span class="privacy">恢复会建立新版本，后续历史仍保留</span></div><div class="card"><table><thead><tr><th>版本</th><th>变更</th><th>时间 / 操作者</th><th></th></tr></thead><tbody>${state.history.map(h=>`<tr><td>v${h.revision}</td><td>${esc(h.summary)}</td><td>${esc(h.created.slice(0,19))} · ${esc(h.actor)}</td><td>${h.revision!==state.revision?btn('恢复此版本','restore',`data-target="${h.revision}"`,'small'):badge('pass','当前')}</td></tr>`).join('')}</tbody></table></div>`;
}
function issuesPage() {
  return title('问题与演进','记录卡住的业务问题、影响范围和负责处理的人。问题随项目版本保存，进入交付包。')+
    `<div class="card"><label>发现的问题<textarea id="issue-text" placeholder="例如：两个来源对“办结”的定义不同，影响任务完成率；请业务负责人确认包含哪些状态。"></textarea></label>${btn('记录问题','feedback','','primary')}</div><div class="section-title"><h2>待处理问题</h2><span class="muted">${state.document.feedback.filter(f=>f.status==='open').length} 项</span></div><div class="card">${state.document.feedback.filter(f=>f.status==='open').length?state.document.feedback.filter(f=>f.status==='open').map(f=>`<div class="gap"><div><h3>${esc(f.text)}</h3><p>发现于版本 ${f.revision} · ${esc(f.created.slice(0,19))}</p></div>${btn('记录处理结果','resolve-feedback',`data-id="${f.id}"`,'small')}</div>`).join(''):empty('尚未记录问题','模型冲突、业务未定、数据未到位和消费者异常，都可在这里留痕。')}</div><div class="section-title"><h2>已处理问题</h2></div><div class="card">${state.document.feedback.filter(f=>f.status==='resolved').map(f=>`<div class="gap"><div><h3>${esc(f.text)}</h3><p>处理：${esc(f.resolution)} · ${esc(f.resolved_by)}</p></div>${badge('pass','已关闭')}</div>`).join('')||'<p class="muted">尚无已关闭问题。</p>'}</div><div class="section-title"><h2>语义确认记录</h2></div><div class="card">${state.document.decisions.length?state.document.decisions.map(d=>`<div class="gap"><div><h3>${esc(d.key)} · ${esc(d.property)}</h3><p>答案：${esc(JSON.stringify(d.value))}</p><p>${esc(d.actor)} / ${esc(d.role)} · 依据：${esc(d.basis)}</p></div></div>`).join(''):empty('尚无补齐确认记录','在语义建模中回答缺口问题，保存责任人和依据。')}</div>`;
}
function graphKey(x) {return graphMode+':'+ident(graphMode,x);}
function point(x,i) {return positions[graphKey(x)]||{x:35+(i%3)*245,y:35+Math.floor(i/3)*142};}
function drawGraph() {
  if(!$('#graph'))return;
  const nodes=assets(graphMode),kind=graphMode==='entities'?'relations':'relationships',edges=assets(kind), map=new Map();
  nodes.forEach((x,i)=>{map.set(x.name,{...point(x,i),item:x});if(x.uid)map.set(x.uid,map.get(x.name));});
  const width=Math.max(800,...[...map.values()].map(p=>p.x+245)),height=Math.max(540,...[...map.values()].map(p=>p.y+140));
  $('#graph').setAttribute('viewBox',`0 0 ${width} ${height}`);$('#graph').style.height=height+'px';$('#graph').style.minWidth=width+'px';
  $('#graph').innerHTML=`<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#8ba990"/></marker></defs>`+
    edges.map(r=>{const a=map.get(r.from),b=map.get(r.to);if(!a||!b)return '';return `<path class="edge ${r.mapping&&r.mapping!=='equi_key'?'semantic':''}" data-edge="${esc(ident(kind,r))}" d="M${a.x+190},${a.y+38} C${a.x+235},${a.y+38} ${b.x-45},${b.y+38} ${b.x},${b.y+38}" marker-end="url(#arrow)"/><text class="edge-label" x="${(a.x+b.x+190)/2}" y="${(a.y+b.y)/2+29}" text-anchor="middle">${esc(r.predicate||r.cardinality||'待定义')}</text>`;}).join('')+
    nodes.map((x,i)=>{const p=point(x,i),key=ident(graphMode,x);return `<g class="node ${selected===key?'selected':''}" data-node="${esc(key)}" transform="translate(${p.x},${p.y})" tabindex="0" role="button" aria-label="编辑 ${esc(x.cn||x.name)}"><rect width="190" height="79" rx="9"/><text x="14" y="25">${esc((x.cn||x.name).slice(0,14))}</text><text class="node-meta" x="14" y="45">${esc(graphMode==='datasets'?x.name:'业务对象 · '+(x.attributes?.length||0)+' 个属性')}</text><text class="node-meta" x="14" y="63">${esc((x.grain||x.note||'点击补充含义').slice(0,16)+'…')}</text><circle class="port" cx="190" cy="38" r="6"/></g>`;}).join('')+(!nodes.length?'<text x="50" y="100" fill="#7b917b" font-size="15">先创建业务对象，或切换到数据视图查看已导入的表。</text>':'');
  drawInspector();
}
function drawInspector() {
  const chosen=assets(graphMode).find(x=>ident(graphMode,x)===selected);
  $('#inspector').innerHTML=chosen?`<span class="eyebrow">SELECTED ASSET</span><h3>${esc(chosen.cn||chosen.name)}</h3><p class="privacy">${esc(ident(graphMode,chosen))}</p><div class="notice">${esc(chosen.grain||chosen.note||'业务含义待补充')}</div>${btn('编辑属性','edit',attr(graphMode,selected),'primary small')}<div class="section-title"><h3>${graphMode==='datasets'?'字段':'业务属性'}</h3></div>${(chosen.fields||chosen.attributes||[]).map(f=>`<p><b>${esc(f.cn||f.name)}</b><br><span class="privacy">${esc(f.name)} · ${esc(f.role||f.value_type||'待定')}</span></p>`).join('')}`:`<span class="eyebrow">GRAPH INSPECTOR</span><h3>${connection?'选择第二个节点':'查看与编辑'}</h3><p class="sub">${connection?'点击两个节点建立关系，也可拖动节点右侧圆点连线。':'点击节点查看属性。业务视图表达对象和关系，数据视图表达物理表与关联键。'}</p><div class="notice">无数据键的业务关系可以保留，但不作为可执行关联。</div>`;
}
function options(items,value,blank='请选择…') {return (blank===null?'':`<option value="">${blank}</option>`)+items.map(x=>{const [v,l]=Array.isArray(x)?x:[x,x];return `<option value="${esc(v)}" ${String(v)===String(value)?'selected':''}>${esc(l)}</option>`;}).join('');}
function input(label,key,value='',type='text',readonly=false) {return `<label>${label}<input name="${key}" type="${type}" value="${esc(value)}" ${readonly?'readonly':''}></label>`;}
function text(label,key,value='') {return `<label>${label}<textarea name="${key}">${esc(value)}</textarea></label>`;}
function select(label,key,items,value='',blank='请选择…') {return `<label>${label}<select name="${key}">${options(items,value,blank)}</select></label>`;}
function dialog(title,html,onSave,kind=null,key=null) {
  assetEdit={onSave,kind,key};$('#editor-title').textContent=title;$('#editor-fields').innerHTML=html;$('#form-error').textContent='';$('#delete-asset').hidden=!key||!kind;$('#editor').showModal();
}
function fieldEditor(rows,entity=false) {
  fieldRows=clone(rows);return `<div class="section-title"><h3>${entity?'业务属性':'字段'}</h3>${btn('＋ 添加','field-add',`data-entity="${entity}"`,'small')}</div><div class="table-wrap"><table class="edit-fields"><thead><tr>${(entity?['属性名','类型','取值 / 枚举','含义','']:['字段名','中文含义','角色','类型','枚举（逗号分隔）','敏感','']).map(x=>`<th>${x}</th>`).join('')}</tr></thead><tbody id="field-rows">${fieldRows.map((f,i)=>fieldRow(f,i,entity)).join('')}</tbody></table></div>`;
}
function fieldRow(f,i,entity) {
  const v=(key,value)=>`<input data-field="${key}" value="${esc(value||'')}" aria-label="${key}">`;
  return `<tr data-index="${i}" data-entity="${entity}"><td>${v('name',f.name)}</td>${entity?`<td><select data-field="value_type">${options(['string','number','boolean','date','enum','entity'],f.value_type||'string',null)}</select></td><td>${v('values',comma(f.values))}</td><td>${v('note',f.note)}</td>`:`<td>${v('cn',f.cn)}</td><td><select data-field="role">${options(['pk','fk','dim','measure','time','attr'],f.role||'attr',null)}</select></td><td>${v('type',f.type)}</td><td>${v('enum',comma(f.enum))}</td><td><input type="checkbox" data-field="sensitive" aria-label="敏感字段" ${f.sensitive?'checked':''}></td>`}<td>${btn('×','field-remove','','quiet')}</td></tr>`;
}
function readFields() {return $$('#field-rows tr').map(tr=>{const f=clone(fieldRows[+tr.dataset.index]||{});tr.querySelectorAll('[data-field]').forEach(el=>{const k=el.dataset.field;f[k]=el.type==='checkbox'?el.checked:['enum','values'].includes(k)?el.value.split(/[,，]/).map(x=>x.trim()).filter(Boolean):el.value.trim();});if(f.enum && fieldRows[+tr.dataset.index]?.enum && !Array.isArray(fieldRows[+tr.dataset.index].enum) && comma(f.enum)===comma(fieldRows[+tr.dataset.index].enum))f.enum=clone(fieldRows[+tr.dataset.index].enum);return f;}).filter(f=>f.name);}
function value(key) {return $(`#edit-form [name="${key}"]`)?.value.trim()||'';}
function list(key) {return value(key).split(/[,，]/).map(x=>x.trim()).filter(Boolean);}
function editAsset(kind,key='',prefill={}) {
  const old=key?assets(kind).find(x=>ident(kind,x)===key):null,x=clone(old||prefill),ds=assets('datasets'),entities=assets('entities');let html='';
  if(kind==='datasets')html=`<div class="grid cols2">${input('稳定数据集名','name',x.name,'text',!!old)}${input('显示名称','cn',x.cn||x.display_name||x.displayName)}${input('物理表 / 视图','source',x.source)}${input('主键（复合键用逗号分隔）','primary_key',Array.isArray(x.primary_key)?x.primary_key.join(','):x.primary_key)}</div>${input('行粒度：一行代表什么','grain',x.grain)}${text('可回答范围与边界','instructions',x.ai?.instructions)}<div class="grid cols2">${select('数据时间形态','temporal',[["current","当前状态"],["event","发生事件"],["snapshot","定期快照"]],x.temporal?.kind)}${select('映射业务对象','ontology_ref',entities.map(e=>[e.uid||e.name,e.name]),x.ontology_ref)}</div>${fieldEditor(x.fields||[])}`;
  if(kind==='entities')html=`<div class="grid cols2">${input('业务对象名称','name',x.name)}${select('属于哪一类对象','is_a',entities.filter(e=>e.name!==x.name).map(e=>e.name),x.is_a)}</div>${text('业务含义','note',x.note)}${text('尚未映射到数据的原因','unprojected_reason',x.unprojected_reason)}${fieldEditor(x.attributes||[],true)}`;
  if(kind==='relationships'||kind==='relations') {
    const ns=(kind==='relations'?entities:ds).map(e=>[e.name,e.cn||e.name]);
    html=`<div class="grid cols2">${select('关系起点','from',ns,x.from)}${select('关系终点','to',ns,x.to)}</div>`;
    if(kind==='relations')html+=`${input('关系含义（如：触发、修读、归属）','predicate',x.predicate)}${select('数据落地方式','mapping',[['semantic_only','仅业务语义'],['equi_key','可按等值键关联'],['weak','弱关联'],['derived','派生关系']],x.mapping||'semantic_only')}`;
    else html+=`<div class="grid cols2">${input('起点字段（复合键逗号分隔）','from_columns',(x.from_columns||x.join_key_from||x.join_key||[]).toString())}${input('终点字段（顺序与起点对应）','to_columns',(x.to_columns||x.join_key_to||x.join_key||[]).toString())}${select('声明基数','cardinality',['1:1','N:1','1:N','N:M'],x.cardinality)}${select('是否允许遍历','traversable',[['false','暂不允许'],['true','允许']],String(x.traversable===true),null)}</div><p class="privacy">起点字段：<span id="from-hint"></span><br>终点字段：<span id="to-hint"></span></p>`;
    html+=text('依据、限制或未落地原因','note',x.note);
  }
  if(kind==='metrics')html=`<div class="grid cols2">${input('指标 ID','id',x.id,'text',!!old)}${input('业务名称','name',x.name)}${select('挂载数据集','dataset',ds.map(d=>[d.name,d.cn||d.name]),x.dataset)}${select('聚合类型','type',[['count','计数'],['sum','求和'],['avg','平均'],['min','最小值'],['max','最大值'],['ratio','比率'],...(x.type==='list'?[['list','旧版明细指标（保留）']]:[])],x.type||'count',null)}${input('单位','unit',x.unit)}${select('时间范围','time_requirement',[["","待明确"],["current","当前状态，不按时间统计"],["field","按业务时间字段统计"]],x.time_requirement||(x.time_field?'field':''),null)}${input('时间字段（按时间统计时填写）','time_field',x.time_field)}</div>${text('业务口径：范围、包含与排除','caliber',x.caliber?.note)}${input('同义问法（逗号分隔）','synonyms',x.synonyms?.join(','))}<div class="grid cols2">${select('计算设置','formula_mode',[["keep","保留现有完整表达式"],["simple","按字段生成聚合表达式"]],old?'keep':'simple',null)}${input('聚合字段（计数可填 *）','field','*')}</div><div class="grid cols2">${input('比率分子字段（求和）','numerator_field','')}${input('比率分母字段（求和）','denominator_field','')}${select('分母为零','zero',[['','待确认'],['null','返回空值'],['zero','返回零'],['error','报错']],x.on_zero_denominator||'',null)}${input('展示乘数（如百分比 100）','scale',x.display_scale||'','number')}</div><details><summary>现有表达式与高级设置（由 FDE / skill 辅助）</summary>${text('完整聚合表达式','expr',x.expr)}${text('分子表达式','numerator',x.numerator?.expr)}${text('分母表达式','denominator',x.denominator?.expr)}${text('附加过滤条件','extra_where',x.extra_where)}<p class="privacy">原有 filters 与其他扩展字段完整保留；简单字段模式也保留已有过滤。</p></details>`;
  if(kind==='constraints')html=`<div class="grid cols2">${input('规则 ID','id',x.id,'text',!!old)}${select('约束种类','kind',[['unique','唯一性'],['not_null','非空'],['allowed_values','枚举范围'],['range','数值范围'],['referential','引用完整'],['date_order','日期先后']],x.kind||'unique',null)}${select('数据集','dataset',ds.map(d=>d.name),x.dataset)}${input('字段（多个按顺序逗号分隔）','columns',(x.columns||x.field||'').toString())}${select('空值处理','null_policy',[['forbid','不允许空值'],['ignore','忽略空值'],['unknown','遇到空值记为证据不足']],x.null_policy||'unknown',null)}${input('允许的枚举值','values',x.values?.join(','))}${input('最小值','min',x.min??'','number')}${input('最大值','max',x.max??'','number')}${select('引用目标数据集','ref_dataset',ds.map(d=>d.name),x.references?.dataset)}${input('目标字段','ref_columns',x.references?.columns?.join(','))}</div>`;
  if(kind==='templates')html=`<div class="grid cols2">${input('模板 ID','id',x.id,'text',!!old)}${input('模板名称','name',x.name)}${select('数据集','dataset',ds.map(d=>d.name),x.dataset)}${select('时间范围','time_requirement',[["","待明确"],["current","当前状态，不按时间统计"],["field","按业务时间字段统计"]],x.time_requirement||(x.time_field?'field':''),null)}${input('时间字段（按时间统计时填写）','time_field',x.time_field)}</div>${input('输出字段（逗号分隔）','columns',x.columns?.join(','))}${input('同义问法','synonyms',x.synonyms?.join(','))}${text('用途与边界','note',x.note)}<details><summary>过滤条件（FDE / skill 辅助）</summary>${text('过滤表达式','extra_where',x.extra_where)}</details>`;
  if(kind==='concepts')html=`${input('业务概念','term',x.term,'text',!!old)}${input('同义词（逗号分隔）','synonyms',x.synonyms?.join(','))}<div class="grid cols2">${select('展开到哪个数据集','dataset',ds.map(d=>d.name),x.expand?.dataset)}${input('展开字段','field',x.expand?.field)}</div>${input('对应取值（逗号分隔）','values',x.expand?.values?.join(','))}${text('概念说明','note',x.note)}`;
  dialog((old?'编辑':'新建')+names[kind],html,async()=>{
    let p={};
    if(kind==='datasets')p={name:value('name'),cn:value('cn'),source:value('source'),grain:value('grain'),primary_key:list('primary_key'),ai:{instructions:value('instructions')},fields:readFields(),ontology_ref:value('ontology_ref')||null,temporal:{kind:value('temporal')}};
    if(kind==='entities')p={name:value('name'),note:value('note'),is_a:value('is_a')||null,unprojected_reason:value('unprojected_reason'),attributes:readFields()};
    if(kind==='relations')p={from:value('from'),to:value('to'),predicate:value('predicate'),mapping:value('mapping'),note:value('note')};
    if(kind==='relationships'){
      p={from:value('from'),to:value('to'),from_columns:list('from_columns'),to_columns:list('to_columns'),cardinality:value('cardinality'),traversable:value('traversable')==='true',note:value('note')};
      if(x.join_key_from!==undefined)p.join_key_from=p.from_columns.length===1?p.from_columns[0]:p.from_columns;
      if(x.join_key_to!==undefined)p.join_key_to=p.to_columns.length===1?p.to_columns[0]:p.to_columns;
    }
    if(kind==='metrics'){
      p={id:value('id')||undefined,name:value('name'),dataset:value('dataset'),type:value('type'),unit:value('unit'),time_requirement:value('time_requirement'),time_field:value('time_requirement')==='current'?null:value('time_field'),synonyms:list('synonyms'),caliber:{note:value('caliber')},extra_where:value('extra_where')};
      if(value('formula_mode')==='simple'){
        const field=value('field');const allowed=new Set(ds.find(d=>d.name===p.dataset)?.fields?.map(f=>f.name)||[]);const q=f=>'"'+f.replaceAll('"','""')+'"';
        if(p.type==='ratio'){if(!allowed.has(value('numerator_field'))||!allowed.has(value('denominator_field')))throw Error('请选择已声明的分子、分母字段');p.numerator={expr:`SUM(${q(value('numerator_field'))})`};p.denominator={expr:`SUM(${q(value('denominator_field'))})`};p.expr=null;}
        else {if(!allowed.has(field)&&!(field==='*'&&p.type==='count'))throw Error('聚合字段不在所选数据集中');p.expr=`${p.type.toUpperCase()}(${field==='*'?'*':q(field)})`;}
        p.structured=true;
      }else {p.expr=value('expr')||null;if(value('numerator'))p.numerator={expr:value('numerator')};if(value('denominator'))p.denominator={expr:value('denominator')};}
      if(value('zero'))p.on_zero_denominator=value('zero');if(value('scale'))p.display_scale=Number(value('scale'));
    }
    if(kind==='constraints'){p={id:value('id')||undefined,kind:value('kind'),dataset:value('dataset'),columns:list('columns'),null_policy:value('null_policy')};if(p.kind==='allowed_values')p.values=list('values');if(p.kind==='range'){if(value('min')!=='')p.min=+value('min');if(value('max')!=='')p.max=+value('max');}if(p.kind==='referential')p.references={dataset:value('ref_dataset'),columns:list('ref_columns')};}
    if(kind==='templates')p={id:value('id')||undefined,name:value('name'),dataset:value('dataset'),columns:list('columns'),time_requirement:value('time_requirement'),time_field:value('time_requirement')==='current'?null:value('time_field'),synonyms:list('synonyms'),note:value('note'),extra_where:value('extra_where')};
    if(kind==='concepts')p={term:value('term'),synonyms:list('synonyms'),note:value('note'),expand:{dataset:value('dataset'),field:value('field'),values:list('values')}};
    await mutate('edit',{kind,key:key||null,patch:p});
  },kind,key);
  if(kind==='metrics'||kind==='templates'){const timeControl=$('#editor-fields [name=time_requirement]'),timeField=$('#editor-fields [name=time_field]');const showTime=()=>{timeField.closest('label').hidden=timeControl.value==='current';};timeControl.addEventListener('change',showTime);showTime();}
  if(kind==='relationships'){const hints=()=>{for(const k of ['from','to'])$('#'+k+'-hint').textContent=ds.find(d=>d.name===value(k))?.fields?.map(f=>f.name).join('、')||'请选择数据集';};$$('#editor-fields select').forEach(el=>el.addEventListener('change',hints));hints();}
}
function sceneDialog(id) {
  const s=clone(state.document.scenarios.find(x=>x.id===id)||{profile:'metric',requirements:{}});
  const fields=profile=>state.profiles[profile].required.map(k=>text(state.labels[k],k,s.requirements[k]||'')).join('');
  dialog('场景与验收约定',`${select('应用类型','profile',Object.entries(state.profiles).map(([k,p])=>[k,p.label]),s.profile,null)}${text('具体业务问题','question',s.question)}${input('涉及的数据集（逗号分隔）','datasets',s.datasets?.join(','))}<p class="privacy">可选：${esc(assets('datasets').map(d=>d.name).join('、'))}</p>${input('涉及的指标 ID（逗号分隔）','metrics',s.metrics?.join(','))}<div id="scene-requirements">${fields(s.profile)}</div><div class="notice">办事、政策适用、分析决策先保存可交接的场景合同；本版不执行外部办理、政策裁决或预测优化。</div>`,async()=>{
    const profile=value('profile'),requirements={...s.requirements};state.profiles[profile].required.forEach(k=>requirements[k]=value(k));
    await mutate('scene',{scene:{...s,profile,question:value('question'),datasets:list('datasets'),metrics:list('metrics'),requirements}});
  });
  $('[name=profile]').addEventListener('change',()=>{$$('#scene-requirements textarea').forEach(t=>s.requirements[t.name]=t.value);$('#scene-requirements').innerHTML=fields(value('profile'));});
}
function answerDialog(gid) {
  const g=state.gaps.find(x=>x.id===gid);
  dialog('补齐：'+g.key,`<h3>${esc(g.question)}</h3>${g.options?select('答案','answer',g.options,''):text('答案','answer','')}${input('确认人','actor','')}${input('责任角色','role',g.role,'text',true)}${text('依据：来源、讨论结论或规则位置','basis','')}<p class="privacy">确认人和角色为本地审计记录，不代表系统完成身份或权限认证。</p>`,async()=>{await mutate('answer',{gap:gid,value:value('answer'),actor:value('actor'),role:g.role,basis:value('basis')});});
}
function expected(id) {const text=$(id).value.trim();if(!text)return {};const v=JSON.parse(text);return {expected:Array.isArray(v)?v:[[v]]};}
async function action(button) {
  const a=button.dataset.action;
  if(a==='navigate')return go(button.dataset.page);
  if(a==='derive'){if(!confirm('复用现有表、字段和关系键，只补缺少的对象及投影。已有语义不覆盖；生成结果仍需核对业务含义，不会发布或授权。'))return;await mutate('derive',{});notify('语义候选已保存，请核对对象含义与关系谓词');return;}
  if(a==='edit')return editAsset(button.dataset.kind,button.dataset.key);
  if(a==='scene')return sceneDialog(button.dataset.id);
  if(a==='answer')return answerDialog(button.dataset.gap);
  if(a==='graph-mode'){graphMode=button.dataset.mode;activeKind=graphMode;selected=null;connection=null;return render();}
  if(a==='first-query'){const t=state.document.tutorial;const m=assets('metrics').find(x=>x.id===t?.metric)||assets('metrics')[0];const ds=assets('datasets').find(d=>d.name===m?.dataset);const allowed=new Set(ds?.fields?.map(f=>f.name)||[]);bundleForm={metric:m?.id||'',columns:(t?.columns||[]).filter(c=>allowed.has(c)),limit:50,offset:0,expected:''};go('check');return;}
  if(a==='asset-tab'){activeKind=button.dataset.kind;return render();}
  if(a==='connect'){connection=connection?null:{start:null};return render();}
  if(a==='arrange'){assets(graphMode).forEach((x,i)=>positions[graphKey(x)]={x:35+(i%3)*245,y:35+Math.floor(i/3)*142});await api('layout',{positions});drawGraph();return;}
  if(a==='field-add'){const e=button.dataset.entity==='true';const i=fieldRows.push({})-1;$('#field-rows').insertAdjacentHTML('beforeend',fieldRow({},i,e));return;}
  if(a==='field-remove'){button.closest('tr').remove();return;}
  if(a==='report'){const saved=state.runs.find(r=>r.id===button.dataset.id);report=saved?{...saved.report,id:saved.id,stale:saved.stale}:null;render();$('#current-report').scrollIntoView({behavior:'smooth'});return;}
  if(a==='import'){
    const kind=button.dataset.kind,file=$('#file-'+kind).files[0];if(!file)throw Error('请先选择文件');if(file.size>32*1024*1024)throw Error('文件不能超过 32 MB');
    const bytes=new Uint8Array(await file.arrayBuffer());let binary='';for(let i=0;i<bytes.length;i+=8192)binary+=String.fromCharCode(...bytes.subarray(i,i+8192));
    await mutate('import',{kind,filename:file.name,content:btoa(binary),replace:$('#replace-'+kind)?.checked||false,provenance:$('#provenance')?.value||'unknown'});notify('资料已导入并保存版本');return;
  }
  if(a==='check'){report=await api('check',{});await reload();notify('检查完成，请查看各项证据');return;}
  if(a==='query'){report=await api('query',{metric:$('#query-metric').value,...expected('#query-expected')});await reload();return;}
  if(a==='consumer'){report=await api('consumer',{endpoint:$('#consumer-endpoint').value,question:$('#consumer-question').value,...expected('#consumer-expected')});await reload();return;}
  if(a==='bundle'||a==='context'){const req=bundleRequest();bundleForm={...req,expected:$('#bundle-expected').value};if(a==='bundle'&&$('#bundle-expected').value.trim())req.expected=JSON.parse($('#bundle-expected').value);report=await api(a,req);await reload();$('#current-report')?.scrollIntoView({block:'start'});return;}
  if(a==='feedback'){await mutate('feedback',{text:$('#issue-text').value.trim()});notify('问题已记录');return;}
  if(a==='resolve-feedback'){const resolution=prompt('处理结果与依据（会写入项目历史）');if(!resolution)return;const actor=prompt('处理责任人');if(!actor)return;await mutate('resolve-feedback',{id:button.dataset.id,resolution,actor});notify('问题已关闭并留痕');return;}
  if(a==='restore'){const target=+button.dataset.target;if(!confirm(`将版本 ${target} 恢复为新的当前版本？现有历史仍会保留。`))return;await mutate('restore',{target});report=null;notify('版本已恢复，旧证据需重新核对');return;}
  if(a==='download'){
    const res=await fetch('/api/'+button.dataset.type,{headers:{'X-Workbench-Token':token}});if(!res.ok)throw Error((await res.json()).error);
    const u=URL.createObjectURL(await res.blob()),link=document.createElement('a');link.href=u;link.download=button.dataset.type==='backup'?'project-backup.zip':button.dataset.type==='review'?'human-review.html':'semantic-delivery.zip';link.click();setTimeout(()=>URL.revokeObjectURL(u),1000);notify('交付文件已生成');
  }
}
document.addEventListener('click',async e=>{const b=e.target.closest('[data-action]');if(!b)return;try{b.disabled=true;await action(b);}catch(err){notify(err.message);}finally{b.disabled=false;}});
document.addEventListener('click',e=>{if(e.target.closest('[data-close]'))$('#editor').close();const edge=e.target.closest('[data-edge]');if(edge)editAsset(graphMode==='entities'?'relations':'relationships',edge.dataset.edge);});
$('#refresh').addEventListener('click',()=>reload().catch(e=>notify(e.message)));
$('#edit-form').addEventListener('submit',async e=>{e.preventDefault();const b=$('#edit-form button[type=submit]');b.disabled=true;try{await assetEdit.onSave();$('#editor').close();notify('修改已保存');}catch(err){$('#form-error').textContent=err.message;}finally{b.disabled=false;}});
$('#delete-asset').addEventListener('click',async()=>{if(!confirm('删除这个资产？存在已知引用时会阻止删除。'))return;try{await mutate('edit',{kind:assetEdit.kind,key:assetEdit.key,remove:true});$('#editor').close();notify('资产已删除，历史版本仍保留');}catch(err){$('#form-error').textContent=err.message;}});
window.addEventListener('hashchange',()=>{page=location.hash.slice(1)||'home';render();});
document.addEventListener('input',e=>{if(e.target.id==='graph-search'){const q=e.target.value.toLowerCase();$$('#graph .node').forEach(n=>n.style.opacity=!q||n.textContent.toLowerCase().includes(q)?1:.22);}});
document.addEventListener('change',e=>{if(e.target.id==='bundle-metric'){
 const old=assets('metrics').find(m=>m.id===bundleForm.metric),next=assets('metrics').find(m=>m.id===e.target.value),d=assets('datasets').find(d=>d.name===next?.dataset);
 const selected=old?.dataset===next?.dataset?[...$('#bundle-columns').selectedOptions].map(o=>o.value):[];
 const valid=new Set(d?.fields?.map(f=>f.name)||[]);
 bundleForm.metric=e.target.value;bundleForm.columns=selected.filter(c=>valid.has(c));bundleForm.expected='';bundleForm.offset=0;
 $('#bundle-columns').innerHTML=(d?.fields||[]).map(f=>`<option value="${esc(f.name)}" ${bundleForm.columns.includes(f.name)?'selected':''}>${esc(f.cn||f.name)} (${esc(f.name)})</option>`).join('');
 $('#bundle-expected').value='';$('#bundle-offset').value='0';
}});
function connectNodes(start,end) {if(start===end)return;const from=assets(graphMode).find(x=>ident(graphMode,x)===start),to=assets(graphMode).find(x=>ident(graphMode,x)===end);connection=null;render();editAsset(graphMode==='entities'?'relations':'relationships','',{from:from.name,to:to.name});}
let drag=null;
function svgPoint(e) {const svg=$('#graph'),p=svg.createSVGPoint();p.x=e.clientX;p.y=e.clientY;return p.matrixTransform(svg.getScreenCTM().inverse());}
document.addEventListener('pointerdown',e=>{
  const node=e.target.closest('#graph [data-node]');if(!node)return;
  const id=node.dataset.node;selected=id;const p=svgPoint(e),item=assets(graphMode).find(x=>ident(graphMode,x)===id),base=point(item,assets(graphMode).indexOf(item));
  if(connection){if(connection.start)connectNodes(connection.start,id);else{connection.start=id;drawGraph();notify('再点击另一个节点');}return;}
  drag={id,start:p,base,port:e.target.classList.contains('port'),moved:false};e.preventDefault();drawInspector();$$('#graph .node').forEach(n=>n.classList.toggle('selected',n.dataset.node===id));
});
document.addEventListener('pointermove',e=>{if(!drag||!$('#graph'))return;const p=svgPoint(e);drag.moved=drag.moved||Math.abs(p.x-drag.start.x)+Math.abs(p.y-drag.start.y)>5;if(drag.port){$('#temp-edge')?.remove();$('#graph').insertAdjacentHTML('beforeend',`<path id="temp-edge" d="M${drag.base.x+190},${drag.base.y+38} L${p.x},${p.y}" stroke="#227352" fill="none" stroke-dasharray="5 4" pointer-events="none"/>`);}else if(drag.moved){positions[graphMode+':'+drag.id]={x:Math.max(5,drag.base.x+p.x-drag.start.x),y:Math.max(5,drag.base.y+p.y-drag.start.y)};drawGraph();}});
document.addEventListener('pointerup',async e=>{if(!drag)return;const d=drag;drag=null;$('#temp-edge')?.remove();if(d.port){const target=document.elementFromPoint(e.clientX,e.clientY)?.closest('[data-node]');if(target)connectNodes(d.id,target.dataset.node);}else if(d.moved){try{await api('layout',{positions});}catch(err){notify(err.message);}}});
document.addEventListener('dblclick',e=>{const n=e.target.closest('#graph [data-node]');if(n)editAsset(graphMode,n.dataset.node);});
document.addEventListener('keydown',e=>{const n=e.target.closest('#graph [data-node]');if(n&&e.key==='Enter')editAsset(graphMode,n.dataset.node);});
reload().catch(e=>{$('#main').innerHTML=empty('无法读取项目',esc(e.message));});
