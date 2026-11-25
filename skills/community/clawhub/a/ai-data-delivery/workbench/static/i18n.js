'use strict';
/* Only source-code UI strings are translated. Asset values, quotes and identifiers
   are never passed through this catalogue. No network translation service. */
window.UIText=(()=>{
  const params=new URLSearchParams(location.search);
  let stored;try{stored=localStorage.getItem('ai-data-delivery:language');}catch(_){}
  const language=/^zh(?:-|$)/i.test(params.get('lang')||stored||navigator.language)?'zh':'en';
  const catalog=window.UI_EN||{};
  const pattern=/[^<>="'\n{}]*[\u3400-\u9fff][^<>="'\n{}]*/gu;
  function translate(text){
    if(language==='zh')return text;
    if(Object.hasOwn(catalog,text))return catalog[text];
    return text.replace(pattern,part=>{const key=part.trim();return Object.hasOwn(catalog,key)?part.replace(key,catalog[key]):part;});
  }
  function t(strings,...values){
    if(typeof strings==='string')return translate(strings);
    if(!Array.isArray(strings))return String(strings??'');
    return strings.reduce((result,part,i)=>result+translate(part)+(i<values.length?values[i]:''),'');
  }
  const codes={CONTEXT_TRUNCATED:'Read and combine the remaining context pages',APPLICABILITY_UNKNOWN:'No explicit evidence covers the requested business date',OUTSIDE_KNOWN_INTERVAL:'The business date falls outside the known interval',MISSING_DEFINITION:'Complete this definition before confirming',MISSING_PROPERTY:'Complete this required property before confirming',MISSING_RELATION_DEFINITION:'Complete the relationship definition',INVALID_RELATION_TYPE:'Choose a supported relationship type',INVALID_RELATION_ENDPOINT:'Check the relationship type and choose compatible source and target types',INVALID_FOREIGN_KEY:'Use nonempty source and target field lists of equal length, in matching order',CLASSIFICATION_CYCLE:'Remove the cycle in the classification hierarchy',IDENTITY_REVIEW:'Compare these same-kind identities, then merge or record why they remain separate',MISSING_DEPENDENCY:'Restore or correct the missing required dependency',MISSING_EVIDENCE:'Add supporting evidence',STALE_EVIDENCE:'Review the changed source evidence',NOT_CONFIRMED:'Review and confirm the required knowledge',RETIRED_DEPENDENCY:'Replace or restore the retired dependency',NO_DATA_CONNECTOR:'No data connector is available',NO_ACTION_EXECUTOR:'No action executor is available'};
  function issue(value){
    if(language==='zh')return value.message||value.code;
    const text=codes[value.code];
    return text?[value.asset_name||value.asset_id||value.id,text,value.field?'('+value.field+')':''].filter(Boolean).join(': '):translate(value.message||value.code||'');
  }
  function error(body){
    if(language==='zh')return body.error||'操作失败';
    const issues=body.details?.issues||[];
    if(issues.length)return issues.map(issue).join('\n');
    const result=translate(body.error||'操作失败');
    return /[\u3400-\u9fff]/u.test(result)?'Request could not be completed. Original diagnostic: '+result:result;
  }
  function mount(){
    document.documentElement.lang=language==='zh'?'zh-CN':'en';
    document.title=t('图谱编辑器 · AI Data Delivery');
    document.querySelectorAll('[data-ui]').forEach(el=>el.textContent=t(el.dataset.ui));
    document.querySelectorAll('[data-ui-aria]').forEach(el=>el.setAttribute('aria-label',t(el.dataset.uiAria)));
    const select=document.getElementById('ui-language');select.value=language;
    select.addEventListener('change',()=>{
      // A language change reloads presentation code; never discard an open edit.
      const dirty=[...document.querySelectorAll('input:not([type=hidden]),textarea')].some(el=>!el.closest('dialog:not([open])')&&!el.readOnly&&!el.disabled&&(el.type==='file'?el.files.length:el.type==='checkbox'||el.type==='radio'?el.checked!==el.defaultChecked:el.value!==el.defaultValue));
      if(document.querySelector('dialog[open]')||dirty||window.ScenarioWorkbench?.isDirty()||window.MetadataWorkbench?.isDirty()){select.value=language;const toast=document.getElementById('toast');toast.textContent=language==='zh'?'请先保存或清除当前输入，并关闭弹窗，再切换语言；输入已保留。':'Save or clear your current input and close the dialog before switching language. Your input is retained.';toast.classList.add('show');setTimeout(()=>toast.classList.remove('show'),6500);return;}
      try{localStorage.setItem('ai-data-delivery:language',select.value);}catch(_){}
      const url=new URL(location.href);url.searchParams.set('lang',select.value);location.assign(url);
    });
  }
  return {t,language,mount,error,issue};
})();
window.UIText.mount();
