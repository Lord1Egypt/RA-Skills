import {readFile,writeFile,mkdir,readdir,chmod,realpath} from 'node:fs/promises';
import path from 'node:path';
import {createHash,randomUUID} from 'node:crypto';
import {getPlatform,inferPlatform} from './platforms.mjs';
import {handoffTask} from './handoff.mjs';
import {buildDetailExtractExpression} from './extract.mjs';
import {publicURL,shortText,normalizeItem,reportMarkdown} from './results.mjs';
import {fail,number,safeCode,createRun,parallelGroups,boundedPage,stateOf,hasReadableText,detailLocation,providerRedirect,matchesHost,saveJSON} from './runtime.mjs';

export async function readItem(run,target,options,onProgress=()=>{}){
 const {item,rawURL,ctx,profile}=target,started=Date.now();
 delete item.readError;delete item.evidenceReuse;delete item.contentFile;delete item.readCoverage;
 let phase='navigate';
 const entry={id:item.id,platform:item.platform,status:'read_failed',elapsedMs:0};
 onProgress({stage:'read',platform:item.platform,id:item.id,title:item.title});
 try{
  const tab=await run.navigate(ctx,rawURL,{newTab:providerRedirect(rawURL),timeoutMs:options.timeoutMs});entry.navigationMs=Date.now()-started;phase='extract';
  const page=await boundedPage(run.bridge,ctx.browser.browserId,tab,buildDetailExtractExpression(profile.id,{maxText:16000}),{expectedURL:rawURL,deadline:started+options.timeoutMs,detail:true});entry.polling=page.polling;
  const blocked=stateOf(page);
  if(blocked)item.readStatus=blocked;
  else {
   const valid=publicURL(page.url)&&detailLocation(rawURL,page)&&(!providerRedirect(rawURL)?matchesHost(page.url,[new URL(rawURL).hostname,...(profile.kind==='web'?[]:profile.hosts)]):true);
   if(!valid)item.readStatus=page.timedOut?'content_unavailable':'unexpected_page';
   else {
    if(providerRedirect(rawURL)){item.resolvedFrom=publicURL(rawURL);item.url=publicURL(page.url)}
    item.contentType=page.contentType||item.contentType;
    if(!hasReadableText(page))item.readStatus='content_unavailable';
    else {
     item.readStatus='read';item.readTitle=shortText(page.title,300);item.title=item.method==='direct'?item.readTitle||item.title:item.title;
     item.author=item.author||shortText(page.author,100)||null;item.publishedAt=item.publishedAt||shortText(page.publishedAt,100)||null;
     item.readCoverage=item.contentType==='video'?'视频页面标题与描述；未播放或转录':'已呈现页面正文';item.contentFile='sources/'+item.id+'.json';
     const text=String(page.text).slice(0,16000);
     await saveJSON(path.join(run.output,item.contentFile),{id:item.id,url:item.url,title:item.readTitle,text,textSha256:createHash('sha256').update(text).digest('hex'),truncated:text.length>=16000,extractionMethod:'dom',extraction:page.extraction||null,readCoverage:item.readCoverage,publishedAt:shortText(page.publishedAt,100)||null,observedAt:new Date().toISOString(),untrustedSource:true});
    }
   }
  }
 }catch(e){item.readStatus='read_failed';item.readError=safeCode(e);entry.errorPhase=phase}
 entry.status=item.readStatus;entry.elapsedMs=Date.now()-started;onProgress({...entry,stage:'read_done'});return entry;
}
async function localJSON(file,max=4*1024*1024){const buffer=await readFile(file);if(buffer.length>max)throw fail('input_too_large');try{return JSON.parse(buffer.toString())}catch{throw fail('input_invalid_json')}}
export async function prepareRead(input){
 const o={...input,timeoutMs:number(input.timeoutMs??18000,2000,60000,'timeout'),concurrency:number(input.concurrency??3,1,4,'concurrency')};
 if(!!o.from===!!o.urls?.length)throw fail('read_requires_from_or_urls');
 const selected=[];let originalMap={};
 if(o.from){
  const file=path.resolve(o.from.endsWith('.json')?o.from:path.join(o.from,'results.json')),base=path.dirname(file),report=await localJSON(file);
  if(report.schemaVersion!==1||!Array.isArray(report.results))throw fail('invalid_source_report');
  if(!Array.isArray(o.ids)||!o.ids.length||o.ids.length>10||o.ids.some(id=>typeof id!=='string'||!id))throw fail('read_requires_selected_ids');
  if(o.ids.some(id=>!/^[a-f0-9]{14}$/.test(id)))throw fail('invalid_source_id');
  let journal={};try{journal=await localJSON(path.join(base,'private-run.json'))}catch(e){if(e.code!=='ENOENT')throw e}
  for(const route of journal.routes||[])if(typeof route.platform==='string'&&typeof (route.browserId||route.requestedRoute)==='string')originalMap[route.platform]=route.browserId||route.requestedRoute;
  for(const id of new Set(o.ids)){
   const found=report.results.find(x=>x.id===id);if(!found||!publicURL(found.url))throw fail('unknown_source_id');
   const item=structuredClone(found),profile=getPlatform(item.platform),privateSource=(journal.candidates||[]).find(x=>x.id===id&&x.platform===item.platform);
   const rawURL=privateSource?.url&&publicURL(privateSource.url)===publicURL(item.url)?privateSource.url:item.url;
   if(!publicURL(rawURL))throw fail('unsafe_navigation_url');
   let cached;
   if(!o.refresh&&item.readStatus==='read'&&item.contentFile){
    const resolved=await realpath(path.resolve(base,item.contentFile)),safeBase=await realpath(base);
    if(!resolved.startsWith(safeBase+path.sep))throw fail('source_file_outside_run');cached=await localJSON(resolved);
    if(cached.id!==item.id||publicURL(cached.url)!==publicURL(item.url))throw fail('source_evidence_identity_mismatch');
    if(typeof cached.text!=='string'||createHash('sha256').update(cached.text).digest('hex')!==cached.textSha256)throw fail('source_evidence_hash_mismatch');
   }
   selected.push({item,profile,rawURL,cached});
  }
 }else{
  if(o.ids?.length||o.urls.length>10)throw fail('invalid_read_urls');
  for(const rawURL of new Set(o.urls)){
   const url=publicURL(rawURL);if(!url)throw fail('unsafe_navigation_url');const profile=getPlatform(inferPlatform(url)||'google');
   const item=normalizeItem({url,title:new URL(url).hostname,contentType:'page'},{platform:profile.id,query:'直接读取',method:'direct'});selected.push({item,profile,rawURL});
  }
 }
 return {options:o,selected,originalMap,browserMap:{...originalMap,...o.browserMap}};
}
export async function runRead(input,{bridge,onProgress=()=>{}}={}){
 const prepared=await prepareRead(input),{options:o,selected,browserMap}=prepared,started=Date.now(),reads=[];
 let run,cleanup={remaining:[],verified:true},output;
 const pending=selected.filter(x=>!x.cached&&x.item.linkStatus!=='search_page_only');
 for(const target of selected.filter(x=>x.item.linkStatus==='search_page_only')){target.item.readStatus='link_unavailable';reads.push({id:target.item.id,platform:target.item.platform,status:'link_unavailable',elapsedMs:0});onProgress({stage:'read_done',...reads.at(-1)})}
 if(pending.length){
  run=await createRun(o,{bridge});output=run.output;
  for(const target of pending){try{target.ctx=run.route(target.profile,browserMap)}catch(e){target.item.readStatus='route_unavailable';target.item.readError=safeCode(e);reads.push({id:target.item.id,platform:target.item.platform,status:'route_unavailable',elapsedMs:0,errorCode:safeCode(e)});run.privateRun.routes.push({platform:target.profile.id,requestedRoute:browserMap[target.profile.id]||browserMap['*']||null,selectionSource:'unavailable'});onProgress({stage:'read_done',...reads.at(-1)})}}
  for(const target of selected)run.privateRun.candidates.push({id:target.item.id,platform:target.profile.id,url:target.rawURL});
  for(const target of selected.filter(t=>t.cached)){const browserId=prepared.originalMap[target.profile.id];if(browserId)run.privateRun.routes.push({platform:target.profile.id,browserId,selectionSource:'source_evidence_reuse'})}
 }else{
  output=path.resolve(o.output||path.join(process.cwd(),'.local','easybr-search','read-'+new Date().toISOString().replace(/[:.]/g,'-')));
  await mkdir(output,{recursive:true,mode:0o700});if((await readdir(output)).length)throw fail('output_directory_not_empty');await chmod(output,0o700);await mkdir(path.join(output,'sources'),{mode:0o700});
  await saveJSON(path.join(output,'private-run.json'),{schemaVersion:1,runId:randomUUID().slice(0,8),operation:selected.every(t=>t.cached)?'evidence_reuse':'read_unavailable',startedAt:new Date(started).toISOString(),routes:[...new Set(selected.map(t=>t.profile.id))].filter(platform=>prepared.originalMap[platform]).map(platform=>({platform,browserId:prepared.originalMap[platform],selectionSource:'source_evidence_reuse'})),candidates:selected.map(t=>({id:t.item.id,platform:t.profile.id,url:t.rawURL})),navigation:[],cleanup:[]});
 }
 for(const target of selected.filter(x=>x.cached)){
  target.item.contentFile='sources/'+target.item.id+'.json';await saveJSON(path.join(output,target.item.contentFile),target.cached);
  target.item.evidenceReuse={kind:'same_run_evidence',observedAt:target.cached.observedAt||null};reads.push({id:target.item.id,platform:target.item.platform,status:'read',elapsedMs:0,reused:true});onProgress({stage:'read_done',...reads.at(-1)});
 }
 let cleanupMs=0;
 try{if(run){await run.initialize();await parallelGroups(pending.filter(t=>t.ctx),t=>t.ctx.browser.browserId,o.concurrency,async t=>{reads.push(await readItem(run,t,o,onProgress))})}}
 finally{if(run){const before=Date.now();cleanup=await run.cleanup();cleanupMs=Date.now()-before}}
 const report={schemaVersion:1,operation:'read',status:'completed',outcome:selected.every(t=>t.item.readStatus==='read')?'ok':selected.some(t=>t.item.readStatus==='read')?'partial':'no_content',scope:{platforms:[...new Set(selected.map(x=>x.item.platform))],read:selected.length},question:o.question||'读取已选来源',queries:[],startedAt:new Date(started).toISOString(),finishedAt:new Date().toISOString(),searches:[],reads,results:selected.map(x=>x.item),cleanup,timings:{totalMs:Date.now()-started,inventoryMs:run?.inventoryMs||0,cleanupMs},execution:{browserCount:run?.contexts.size||0,readConcurrency:Math.min(o.concurrency,run?.contexts.size||0),evidenceReused:selected.filter(t=>t.cached).length},limitations:['重复读取同一运行的已保存证据会沿用其采集时间；需要重新访问时使用 --refresh。','视频页面描述不等于播放或转录。']};
 report.attention=selected.map(t=>handoffTask({platform:t.item.platform,status:t.item.readStatus,id:t.item.id,url:t.item.searchURL||t.item.url,errorCode:t.item.readError})).filter(Boolean);
 await saveJSON(path.join(output,'handoff.json'),{required:report.attention.some(t=>t.required),tasks:report.attention});await saveJSON(path.join(output,'results.json'),report);await writeFile(path.join(output,'results.md'),reportMarkdown(report),{mode:0o600});return {output,report};
}
