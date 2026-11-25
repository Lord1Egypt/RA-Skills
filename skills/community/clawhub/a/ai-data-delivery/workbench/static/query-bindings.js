'use strict';
/* Edit the existing metric declaration. No duplicate model or query execution. */
window.QueryBindings = (() => {
  const t=(zh,en)=>window.UIText?.language==='zh'?zh:en;
  const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const clone=v=>JSON.parse(JSON.stringify(v));
  const functions=()=>({count_distinct:t('去重计数','Count distinct'),count:t('非空值计数','Count values'),sum:t('求和','Sum'),min:t('最小值','Minimum'),max:t('最大值','Maximum')});
  const operators=()=>({eq:'=',ne:'≠',gt:'>',gte:'≥',lt:'<',lte:'≤',is_null:t('为空','Is NULL'),not_null:t('非空','Is not NULL')});
  const select=(key,choices,value)=>`<select data-qb="${key}">${Object.entries(choices).map(([id,label])=>`<option value="${esc(id)}" ${id===value?'selected':''}>${esc(label)}</option>`).join('')}</select>`;
  function supported(p){
    const keys=['dataset_id','column_ids','grain_ids','relation_ids','mapping_ids','rule_ids','aggregation','filters','null_policy','time_scope','semantic_fingerprint'];
    return p&&Object.keys(p).sort().join()===keys.sort().join()&&['column_ids','grain_ids','relation_ids','mapping_ids','rule_ids'].every(k=>Array.isArray(p[k]))&&p.aggregation&&Object.keys(p.aggregation).sort().join()==='field_id,function'&&functions()[p.aggregation.function]&&['exclude','preserve'].includes(p.null_policy)&&Array.isArray(p.filters)&&p.filters.every(f=>f&&Object.keys(f).sort().join()==='field_id,op,value'&&operators()[f.op]&&(f.value===null||['string','number','boolean'].includes(typeof f.value)));
  }
  function filterRow(f,fields){
    const type=f.value===null?'null':typeof f.value;
    return `<div class="qb-filter"><label>${t('字段','Field')}${select('filter-field',fields,f.field_id)}</label><label>${t('条件','Condition')}${select('filter-op',operators(),f.op)}</label><label>${t('值类型','Value type')}${select('filter-type',{string:t('文字','Text'),number:t('数字','Number'),boolean:t('是/否','Boolean'),null:t('空值','NULL')},type)}</label><label>${t('值','Value')}<input data-qb="filter-value" value="${esc(f.value===null?'':String(f.value))}" aria-label="${t('过滤值','Filter value')}"></label><button type="button" data-qb-action="remove">${t('移除条件','Remove condition')}</button></div>`;
  }
  function render(asset,assets){
    const p=asset.properties?.query_plan;
    if(!supported(p))return {editable:false,html:`<p>${t('此指标尚无可编辑的单数据集查询约定，或包含当前表单不支持的表达式。请让宿主 Agent 根据原文补齐或修订候选，再回这里核对；现有内容保持原样。','This metric has no editable single-dataset declaration, or uses unsupported expressions. Ask the host Agent to propose evidence-linked bindings, then review here. Existing content is preserved.')}</p>`};
    const fields=Object.fromEntries(assets.filter(a=>a.kind==='field'&&(a.refs||[]).includes(p.dataset_id)).map(a=>[a.id,a.name]));
    const referenced=[...p.column_ids,...p.grain_ids,p.aggregation.field_id,...p.filters.map(f=>f.field_id)];
    for(const id of referenced)if(!fields[id])fields[id]=t('待修复字段：','Unresolved field: ')+id;
    const name=id=>assets.find(a=>a.id===id)?.name||id;
    return {editable:true,fields,html:`<section data-testid="binding-review"><p class="sub">${esc(asset.definition)}</p><p>${t('数据集','Dataset')}: <b>${esc(name(p.dataset_id))}</b></p><div class="notice">${t('依据下方原文核对。保存会修改这个指标的查询约定，并使相关问题记录待复验；不会执行查询。','Compare the sources below. Saving changes this metric and invalidates related observations; it does not execute a query.')}</div><div class="grid cols2"><label>${t('怎样统计','Aggregation')}${select('aggregation',functions(),p.aggregation.function)}</label><label>${t('统计哪个字段','Aggregation field')}${select('aggregation-field',fields,p.aggregation.field_id)}</label></div><fieldset><legend>${t('统计粒度对应的字段','Fields defining the grain')}</legend><div class="sq-options">${Object.entries(fields).map(([id,label])=>`<label class="sq-option"><input type="checkbox" data-qb-grain="${esc(id)}" ${p.grain_ids.includes(id)?'checked':''}>${esc(label)}</label>`).join('')}</div></fieldset><h3>${t('只包含满足全部条件的记录','Include records meeting every condition')}</h3><p class="privacy">${t('本表单只支持“并且”。或条件、跨表与复杂表达式请交给 Agent 保留原意处理。','This form supports AND only. Preserve OR, joins and complex expressions for the Agent to review.')}</p><div id="qb-filters">${p.filters.map(f=>filterRow(f,fields)).join('')}</div><button type="button" data-qb-action="add">${t('添加条件','Add condition')}</button><div class="grid cols2"><label>${t('数据时间范围','Data time scope')}<input data-qb="time" value="${esc(p.time_scope)}"></label><label>${t('空值处理约定','NULL policy')}${select('null-policy',{exclude:t('排除空值','Exclude NULL'),preserve:t('保留空值','Preserve NULL')},p.null_policy)}</label></div><p class="privacy">${t('修改时间范围会同步本指标的时间说明；请与定义正文核对一致。','The metric time description changes with this field; check it against the definition.')}</p><details><summary>${t('已有映射、规则与关系','Existing mappings, rules and relations')}</summary>${['mapping_ids','rule_ids','relation_ids'].map(k=>`<p>${p[k].map(id=>esc(name(id))).join(' · ')||'—'}</p>`).join('')}<p class="privacy">${t('这些引用保留不变。需要改变数据集或业务关系时，请先修订原指标及映射。','These references are preserved. Revise the metric and mappings first to change datasets or relationships.')}</p></details><label>${t('本次核对依据与修改理由','Evidence checked and reason for changes')}<textarea data-qb="reason" rows="3" required></textarea></label></section>`};
  }
  function wire(container,fields){
    container.addEventListener('click',e=>{
      const button=e.target.closest('[data-qb-action]');if(!button)return;
      if(button.dataset.qbAction==='remove')button.closest('.qb-filter').remove();
      else {const target=container.querySelector('#qb-filters');target.insertAdjacentHTML('beforeend',filterRow({field_id:'',op:'eq',value:''},{'':t('请选择字段','Choose a field'),...fields}));target.lastElementChild.querySelector('select').focus();}
    });
  }
  function read(container,original){
    const get=(el,key)=>el.querySelector(`[data-qb="${key}"]`).value;
    const asset=clone(original),p=asset.properties.query_plan;
    if(!supported(p))throw Error(t('此约定不能在本表单中修改','This declaration cannot be edited here'));
    p.aggregation={function:get(container,'aggregation'),field_id:get(container,'aggregation-field')};
    p.grain_ids=[...container.querySelectorAll('[data-qb-grain]:checked')].map(el=>el.dataset.qbGrain);
    p.filters=[...container.querySelectorAll('.qb-filter')].map(el=>{
      const field_id=get(el,'filter-field'),op=get(el,'filter-op'),type=get(el,'filter-type'),raw=get(el,'filter-value');let value=raw;
      if(!field_id)throw Error(t('请选择每条条件的字段','Select a field for every condition'));
      if(type==='number'){if(!raw.trim()||!Number.isFinite(Number(raw)))throw Error(t('数字条件需要有效数值','A numeric condition needs a finite number'));value=Number(raw);}
      if(type==='boolean'){if(!['true','false'].includes(raw.trim()))throw Error(t('是/否条件填写 true 或 false','Use true or false for a boolean condition'));value=raw.trim()==='true';}
      if(type==='null'){if(raw.trim())throw Error(t('空值条件不能填写其他值','A NULL condition cannot contain another value'));value=null;}
      if(['is_null','not_null'].includes(op)!==(value===null))throw Error(t('空值请同时选择“为空/非空”和“空值”类型','Use a NULL operator with the NULL value type'));
      return {field_id,op,value};
    });
    if(!p.grain_ids.length)throw Error(t('请明确统计粒度字段','Select the grain fields'));
    p.column_ids=[...new Set([...p.column_ids,...p.grain_ids,p.aggregation.field_id,...p.filters.map(f=>f.field_id)])];
    p.time_scope=get(container,'time').trim();if(!p.time_scope)throw Error(t('请明确数据时间范围','Specify the data time scope'));
    asset.properties.time_scope=p.time_scope;p.null_policy=get(container,'null-policy');
    const reason=get(container,'reason').trim();if(!reason)throw Error(t('请记录核对依据与修改理由','Record the evidence checked and reason for changes'));
    return {asset,confirm:true,review_query_plan:true,plan_review_reason:reason};
  }
  return {render,wire,read,supported};
})();
