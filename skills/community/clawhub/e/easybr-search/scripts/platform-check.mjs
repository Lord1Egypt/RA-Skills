#!/usr/bin/env node
import {isCLIEntry} from './cli-entry.mjs';
/** Repeatable read-only platform checks; private diagnostics stay under .local/. */
import {mkdir,writeFile,chmod} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {runSearch} from './search.mjs';
import {getPlatform} from './platforms.mjs';
import {resolveOptions} from './config.mjs';
import {publicURL,shortText} from './results.mjs';
import {number,providerRedirect,safeCode,tabsOf,pause} from './runtime.mjs';

export const defaultCheckPlatforms=()=>['baidu','google','bing','douyin','xiaohongshu'];
function fail(code){return Object.assign(new Error(code),{code})}
const safeURL=value=>{if(providerRedirect(value))return null;const text=publicURL(value);if(!text)return null;const u=new URL(text);for(const key of [...u.searchParams.keys()])if(/^(?:searchId|request_id|ops_request_misc|refer_flag|biz_id|pp)$/i.test(key))u.searchParams.delete(key);return u.href};
function diagnosticExpression(profile,searchQuery=''){
 const hints=JSON.stringify(profile.selectors.cards||[]);
 return `(() => {const q=s=>{try{return [...document.querySelectorAll(s)]}catch{return []}},v=n=>!n.hidden&&(!n.getClientRects||n.getClientRects().length>0),t=n=>String(n?.innerText??n?.textContent??'').replace(/\\s+/g,' ').trim(),a=n=>({title:(n.getAttribute('title')||t(n)).slice(0,200),href:n.href||n.getAttribute('href'),className:n.className||'',heading:n.closest('h2,h3,h4')?.textContent?.slice(0,180)||null,ancestors:Array.from({length:8},(_,i)=>{let x=n;for(let k=0;k<=i;k++)x=x?.parentElement;return x}).filter(Boolean).map(x=>({tag:x.tagName,className:x.className||'',tpl:x.getAttribute('tpl'),dataTpl:x.getAttribute('data-tpl')}))}),sels=${hints},term=${JSON.stringify(searchQuery.toLowerCase())};return {url:location.href,title:document.title,readyState:document.readyState,bodyText:t(document.body).slice(0,3500),headings:q('h1,h2,h3').filter(v).slice(0,12).map(n=>t(n).slice(0,180)),inputs:q('input,textarea,[role="searchbox"]').filter(v).filter(n=>!['password','hidden'].includes(n.getAttribute('type'))).slice(0,12).map(n=>({tag:n.tagName,type:n.getAttribute('type'),id:n.id,name:n.getAttribute('name'),placeholder:n.getAttribute('placeholder'),ariaLabel:n.getAttribute('aria-label'),ancestors:Array.from({length:6},(_,i)=>{let x=n;for(let k=0;k<=i;k++)x=x?.parentElement;return x}).filter(Boolean).map(x=>({tag:x.tagName,className:x.className||'',role:x.getAttribute('role'),ariaModal:x.getAttribute('aria-modal')}))})),dialogs:q('[role="dialog"],[aria-modal="true"],[class*="Modal"],[class*="modal"]').filter(v).slice(0,12).map(n=>({tag:n.tagName,className:n.className,text:t(n).slice(0,600),role:n.getAttribute('role'),ariaModal:n.getAttribute('aria-modal')})),textMatches:q('*').slice(0,6000).filter(n=>!n.children.length&&v(n)&&t(n).length>8&&t(n).length<400&&t(n).toLowerCase().includes(term)).slice(0,12).map(n=>({text:t(n),ancestors:Array.from({length:8},(_,i)=>{let x=n;for(let k=0;k<i;k++)x=x?.parentElement;return x}).filter(Boolean).map(x=>({tag:x.tagName,className:x.className||'',attrs:Object.fromEntries(['id','data-e2e','data-id','data-aweme-id','data-video-id','role','href'].map(k=>[k,x.getAttribute(k)]))}))})),nonLinkItems:q('li').filter(v).filter(n=>!n.closest('nav,header,footer')&&t(n).length>40).slice(0,12).map(n=>({tag:n.tagName,className:n.className,text:t(n).slice(0,700),attrs:Object.fromEntries(['id','data-e2e','data-id','data-aweme-id','data-video-id','role'].map(k=>[k,n.getAttribute(k)])),children:[...n.children].slice(0,8).map(x=>({tag:x.tagName,className:x.className,attrs:Object.fromEntries(['id','data-e2e','data-id','data-aweme-id','data-video-id','role'].map(k=>[k,x.getAttribute(k)]))}))})),cards:q(sels.join(',')).filter(v).slice(0,8).map(n=>({tag:n.tagName,id:n.id,className:n.className,tpl:n.getAttribute('tpl'),dataTpl:n.getAttribute('data-tpl'),text:t(n).slice(0,1200),links:[...n.querySelectorAll('a[href]')].slice(0,8).map(a)})),links:q('a[href]').filter(v).slice(0,80).map(a)}})()`;
}

// Explicit diagnostic only: one normal DOM click; default checks never click.
export async function probeFirstVisibleCard({bridge,browserId,tabId,wait=pause}){
 const before=tabsOf(await bridge.command(browserId,'list_tabs',{}));
 const known=new Set(before.map(t=>t.id??t.tabId));const source=before.find(t=>(t.id??t.tabId)===tabId);
 const original=before.find(t=>t.active&&(source?.windowId===undefined||t.windowId===source.windowId));
 const card=await bridge.evaluate(browserId,tabId,`(() => {const nodes=[...document.querySelectorAll('.search-result-card')];for(const n of nodes){if(!n.getClientRects().length)continue;const p=n.closest('[id^="waterfall_item_"]');const m=p?.id.match(/^waterfall_item_([0-9]{10,24})$/);if(m)return {id:m[1],selector:'#'+p.id+' .search-result-card',title:String(n.innerText||'').slice(0,400),url:location.href}}return null})()`,4000);
 if(!card)return {status:'no_public_dom_card',clicked:false};
 const result={status:'unresolved',clicked:false,domId:card.id,selector:card.selector,sourceURL:card.url,actualURL:null,routeMatched:false,clickMode:'dom',requestedFocus:false,originalActiveTabs:before.filter(t=>t.active).map(t=>({tabId:t.id??t.tabId,windowId:t.windowId??null})),passiveSelection:false,selectionRestored:true,createdCount:0,closedNewCount:0,cleanupVerified:true};let after=[],owned=[];
 try{
  await bridge.command(browserId,'click',{tabId,selector:card.selector,mode:'dom'},5000);result.clicked=true;
  for(let i=0;i<8;i++){
   await wait(250);const page=await bridge.evaluate(browserId,tabId,'({url:location.href,title:document.title,readyState:document.readyState})',3000);
   result.actualURL=page.url;const u=new URL(page.url);result.routeMatched=(u.hostname==='douyin.com'||u.hostname.endsWith('.douyin.com'))&&(u.searchParams.get('modal_id')===card.id||new RegExp('^/(?:video|note)/'+card.id+'/?$').test(u.pathname));
   if(result.routeMatched){result.status='route_verified';break}
  }
 }catch(e){result.errorCode=safeCode(e)}finally{
  after=tabsOf(await bridge.command(browserId,'list_tabs',{}));result.afterActiveTabs=after.filter(t=>t.active).map(t=>({tabId:t.id??t.tabId,windowId:t.windowId??null}));
  owned=after.filter(t=>!known.has(t.id??t.tabId)&&(t.openerTabId===tabId||(()=>{try{const u=new URL(t.url);return /^(?:www\.)?douyin\.com$/.test(u.hostname)&&(u.searchParams.get('modal_id')===card.id||new RegExp('^/(?:video|note)/'+card.id+'/?$').test(u.pathname))}catch{return false}})()));result.createdCount=owned.length;
  for(const t of owned){try{const u=new URL(t.url);if((u.hostname==='douyin.com'||u.hostname.endsWith('.douyin.com'))&&(u.searchParams.get('modal_id')===card.id||new RegExp('^/(?:video|note)/'+card.id+'/?$').test(u.pathname))){result.actualURL=t.url;result.routeMatched=true;result.status='route_verified'}}catch{}}
  const passive=owned.find(t=>t.active);result.passiveSelection=!!passive;if(passive)result.selectionRestored=false;
  if(passive&&original){try{await bridge.command(browserId,'activate_tab',{tabId:original.id??original.tabId,focus:false,restoreSelection:true});result.selectionRestored=true}catch(e){result.selectionRestored=false;result.restoreError=safeCode(e)}}
  for(const t of owned){try{await bridge.command(browserId,'close_tab',{tabId:t.id??t.tabId});result.closedNewCount++}catch{result.cleanupVerified=false}}
  const remaining=tabsOf(await bridge.command(browserId,'list_tabs',{}));result.finalActiveTabs=remaining.filter(t=>t.active).map(t=>({tabId:t.id??t.tabId,windowId:t.windowId??null}));if(owned.some(t=>remaining.some(r=>(r.id??r.tabId)===(t.id??t.tabId))))result.cleanupVerified=false;
 }
 return result;
}

export function summarizeCheck(report,{requestedPlatforms,diagnostics=[]}={}){
 const observations=(report.searches||[]).map(s=>{
  const samples=(report.results||[]).filter(r=>r.platform===s.platform&&(r.query===s.query||r.discoveredBy?.includes(s.query))).slice(0,3).map(r=>({title:r.contentType==='post'?'帖子（仅列来源链接，不复制正文）':shortText(r.title,180),url:safeURL(r.url),linkStatus:r.linkStatus||'content_link',unresolvedRedirect:providerRedirect(r.url),contentType:shortText(r.contentType,40)}));
  return {platform:s.platform,label:getPlatform(s.platform).label,query:shortText(s.query,500),method:s.method,status:s.status,candidateCount:s.count||0,...(s.errorCode?{errorCode:s.errorCode,errorPhase:s.errorPhase||null}:{}),elapsedMs:s.elapsedMs||0,navigationMs:s.navigationMs??null,diagnosticMs:diagnostics.find(d=>d.platform===s.platform&&d.query===s.query)?.elapsedMs??0,samples};
 });
 const counts={};for(const x of observations)counts[x.status]=(counts[x.status]||0)+1;
 return {schemaVersion:1,operation:'platform-check',startedAt:report.startedAt,finishedAt:report.finishedAt,requestedPlatforms:requestedPlatforms||[...new Set(observations.map(x=>x.platform))],queryCount:report.queries?.length||0,counts,observations,timings:report.timings||{},execution:{browserCount:report.execution?.browserCount??null,searchConcurrency:report.execution?.searchConcurrency??null,sameBrowser:report.execution?.sameBrowser==='serial'?'serial':'unspecified'},cleanup:{verified:report.cleanup?.verified===true,remainingCount:(report.cleanup?.remaining||[]).reduce((n,x)=>n+(x.count||1),0)},limits:['一次只读搜索观察不等于全部账号和浏览器均已验证。','登录或挑战不继续该分支；无结果未必是空结果，也可能需要DOM适配。','诊断DOM和实际路由仅保存在本机.local目录，不进入本摘要。']};
}
export function checkMarkdown(report){
 const md=v=>shortText(v,240).replace(/[|\[\]<>\n]/g,' ');
 return ['# easybrSearch 平台覆盖观察','',`执行 ${report.observations.length} 项只读搜索；清理核验：${report.cleanup.verified?'通过':'未完全核验'}。`,'','| 平台 | 查询 | 状态 | 候选数 | 耗时 ms |','| --- | --- | --- | ---: | ---: |',...report.observations.map(x=>`| ${md(x.label)} | ${md(x.query)} | ${md(x.status)} | ${x.candidateCount} | ${x.elapsedMs} |`),'','## 候选样例','',...report.observations.flatMap(x=>x.samples.map(s=>`- ${md(x.label)}：${md(s.title)}${s.url?(s.linkStatus==='search_page_only'?' — 仅搜索页，无详情直链：':' — ')+s.url:' — 未解析的搜索跳转，尚无可公开落地URL。'}`)),'','只汇报当次实际状态。未提取、登录受限、验证码、加载超时和真实空结果分别保留。',''].join('\n');
}
export async function runPlatformCheck(input={}, {runSearchImpl=runSearch,bridge,now=Date.now}={}){
 const platforms=[...new Set((input.platforms||defaultCheckPlatforms()).map(id=>getPlatform(id).id))];
 const queries=input.queries||[input.query||'Manim'];
 const output=path.resolve(input.output||path.join('.local','platform-check',new Date().toISOString().replace(/[:.]/g,'-')));
 const diagnostics=[],seen=new Set();let probed=false;
 const mayObserve=input.diagnostics!==false&&output.split(path.sep).includes('.local');
 if(input.probeFirstCard&&(input.probeFirstCard!=='douyin'||!mayObserve||!platforms.includes('douyin')))throw fail('invalid_probe_scope');
 async function onSearchPage({platform,query,browserId,tabId,page,bridge:activeBridge,errorCode,errorPhase}){
  if(!mayObserve||(!input.observeResults&&(page?.items?.length||page?.state?.empty))||page?.state?.captcha||page?.state?.loginRequired||(!errorCode&&!['interactive','complete'].includes(page?.readyState)))return;
  const key=platform+'\0'+query;if(seen.has(key))return;seen.add(key);
  const started=now(),folder=path.join(output,'diagnostics');await mkdir(folder,{recursive:true,mode:0o700});await chmod(folder,0o700);
  let result;try{result=await activeBridge.evaluate(browserId,tabId,diagnosticExpression(getPlatform(platform),query),5000)}catch(e){result={diagnosticErrorCode:safeCode(e)}}
  if(input.probeCDP){try{result.channel=await activeBridge.evaluate(browserId,tabId,'({url:location.href,title:document.title,readyState:document.readyState,linkCount:document.querySelectorAll(\"a[href]\").length,textLength:document.documentElement?.textContent?.length||0})',2000)}catch(e){result.channel={errorCode:safeCode(e)}}}
  const file=path.join(folder,platform.replace(/[^a-z0-9-]/g,'_')+'-'+seen.size+'.json');
  await writeFile(file,JSON.stringify({platform,query,observedAt:new Date().toISOString(),untrustedSource:true,...(errorCode?{errorCode,errorPhase}:{}),...result},null,2)+'\n',{mode:0o600});
  diagnostics.push({platform,query,elapsedMs:now()-started});
  if(input.probeFirstCard===platform&&!probed&&!page?.state?.captcha&&!page?.state?.loginRequired){probed=true;const probe=await probeFirstVisibleCard({bridge:activeBridge,browserId,tabId});await writeFile(path.join(folder,'douyin-card-probe.json'),JSON.stringify(probe,null,2)+'\n',{mode:0o600})}
 }
 const options={...input,platforms,queries,output,limit:3,read:0,timeoutMs:number(input.timeoutMs??8000,2000,60000,'timeout'),concurrency:number(input.concurrency??3,1,4,'concurrency')};
 const {report}=await runSearchImpl(options,{bridge,onSearchPage,onProgress:()=>{}});
 const summary=summarizeCheck(report,{requestedPlatforms:platforms,diagnostics});
 await mkdir(output,{recursive:true,mode:0o700});await chmod(output,0o700);
 await writeFile(path.join(output,'coverage.json'),JSON.stringify(summary,null,2)+'\n',{mode:0o600});
 await writeFile(path.join(output,'coverage.md'),checkMarkdown(summary),{mode:0o600});
 return {output,report:summary};
}
export function parseCheckCLI(input){
 const options={};const args=[...input];
 const named={'--output':'output','--browser-map':'browserMapFile','--config':'configFile','--timeout-ms':'timeoutMs','--concurrency':'concurrency','--probe-first-card':'probeFirstCard'};
 while(args.length){const flag=args.shift();if(flag==='--help'||flag==='-h')return {help:true};if(flag==='--no-diagnostics'){options.diagnostics=false;continue}if(flag==='--observe-results'){options.observeResults=true;continue}if(flag==='--probe-cdp'){options.probeCDP=true;continue}
  const v=args.shift();if(!v||v.startsWith('--'))throw fail('missing_option');
  if(flag==='--platforms'){if(v.split(',').some(s=>!s.trim()))throw fail('invalid_platforms');options.platforms=v.split(',').map(s=>s.trim())}
  else if(flag==='--query')(options.queries??=[]).push(v);
  else if(named[flag])options[named[flag]]=v;else throw fail('unknown_option');
 }
 return options;
}
async function main(){
 const args=parseCheckCLI(process.argv.slice(2));
 if(args.help){console.log('node scripts/platform-check.mjs --platforms bilibili,xiaohongshu --query "AI动画" --output .local/platform-check/run1 [--browser-map FILE] [--timeout-ms 8000] [--concurrency 3] [--observe-results]\n默认检查百度、Google、Bing、抖音、小红书5个核心平台，limit3/read0；同浏览器串行、不同浏览器并行。失败的正常搜索页可保存本机DOM诊断；登录/挑战立即停止该分支。');return}
 const resolved=await resolveOptions({...args,platforms:args.platforms||defaultCheckPlatforms(),timeoutMs:args.timeoutMs??8000,concurrency:args.concurrency??3});
 const {output,report}=await runPlatformCheck(resolved);console.log(JSON.stringify({output,counts:report.counts,timings:report.timings,cleanup:report.cleanup},null,2));
}
if(isCLIEntry(import.meta.url))main().catch(e=>{console.error(JSON.stringify({error:safeCode(e)}));process.exitCode=1});
