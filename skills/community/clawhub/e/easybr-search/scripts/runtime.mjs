import {mkdir,readFile,writeFile,readdir,chmod,rename} from 'node:fs/promises';
import path from 'node:path';
import {randomUUID,createHash} from 'node:crypto';
import {Bridge} from './bridge.mjs';
import {getPlatform} from './platforms.mjs';
import {publicURL} from './results.mjs';

export const pause=ms=>new Promise(r=>setTimeout(r,ms));
export const fail=code=>Object.assign(new Error(code),{code});
export const number=(v,low,high,name)=>{const n=Number(v);if(!Number.isInteger(n)||n<low||n>high)throw fail('invalid_'+name);return n};
export const backgroundCapability=value=>typeof value==='boolean'?value:typeof value?.default==='boolean'?value.default:null;
export const tabsOf=x=>Array.isArray(x)?x:x?.tabs||[];
export const safeCode=e=>typeof e?.code==='string'&&/^[a-zA-Z0-9_-]{1,80}$/.test(e.code)?e.code:'search_step_failed';
export function matchesHost(url,hosts){try{const h=new URL(url).hostname;return hosts.some(x=>h===x||h.endsWith('.'+x))}catch{return false}}
export async function inventory(bridge){
 const online=(await bridge.browsers()).filter(x=>x.online);
 return Promise.all(online.map(async b=>{try{return {...b,tabs:tabsOf(await bridge.command(b.browserId,'list_tabs',{}))}}catch{return {...b,tabs:[],inventoryUnavailable:true}}}));
}
export function selectBrowser(platform,browsers,map={},loads=new Map()){
 const explicit=map[platform.id]||map['*'];
 if(explicit){const matches=browsers.filter(b=>b.browserId===explicit||b.displayName===explicit);if(matches.length!==1)throw fail('configured_browser_not_unique_or_online');return {browser:matches[0],source:'explicit'}}
 let pool=browsers.filter(b=>!b.inventoryUnavailable);
 // General engines are public searches: distribute them over ordinary connected
 // browsers when possible. Native account routes keep their existing-tab affinity.
 const ordinary=pool.filter(b=>/^(?:chrome|edge|chromium|qq浏览器|豆包浏览器)$/i.test(b.displayName));
 if(platform.kind==='web'&&ordinary.length)pool=ordinary;
 const choices=pool.map((b,i)=>({browser:b,affinity:b.tabs.filter(t=>matchesHost(t.url,platform.hosts)).length,score:(platform.kind==='web'?-(loads.get(b.browserId)||0)*10000:0)+b.tabs.filter(t=>matchesHost(t.url,platform.hosts)).length*100+(/chrome/i.test(b.displayName)?10:0)-i/100})).sort((a,b)=>b.score-a.score);
 if(!choices.length)throw fail('no_online_browser');const c=choices[0];
 return {browser:c.browser,source:platform.kind==='web'&&loads.size?'public_search_load_balanced':c.affinity?'existing_platform_tab':'public_search_browser',warning:choices.filter(x=>x.affinity).length>1?'multiple_platform_browsers_identity_not_verified':null};
}
export function searchLocation(expected,actual){
 try{const a=new URL(actual),e=new URL(expected),google=getPlatform('google').hosts;const inGoogle=h=>google.some(x=>h===x||h==='www.'+x);const same=a.hostname===e.hostname||(inGoogle(a.hostname)&&inGoogle(e.hostname))||(['bing.com','baidu.com'].some(x=>(a.hostname===x||a.hostname.endsWith('.'+x))&&(e.hostname===x||e.hostname.endsWith('.'+x))));
 if(!same||a.pathname.replace(/\/$/,'')!==e.pathname.replace(/\/$/,''))return false;
 for(const [k,v] of e.searchParams)if(['q','keyword','search_query','wd','text','query'].includes(k)&&a.searchParams.get(k)!==v)return false;return true}catch{return false}
}
export function providerRedirect(value){try{const u=new URL(value),google=getPlatform('google').hosts.some(h=>u.hostname===h||u.hostname==='www.'+h);return (['www.baidu.com','baidu.com'].includes(u.hostname)&&u.pathname==='/link'&&u.searchParams.has('url'))||(google&&['/url','/goto'].includes(u.pathname)&&(u.searchParams.has('url')||u.searchParams.has('q')))||(['www.bing.com','cn.bing.com'].includes(u.hostname)&&u.pathname==='/ck/a')}catch{return false}}
export function detailLocation(expected,page){try{if(providerRedirect(page.url))return false;const e=new URL(publicURL(expected)),a=new URL(publicURL(page.url));if(a.hostname!==e.hostname)return providerRedirect(expected)&&!!publicURL(page.url);if(a.pathname!==e.pathname)return publicURL(page.canonicalUrl)===e.href;e.searchParams.sort();a.searchParams.sort();return e.search===a.search}catch{return false}}
export const stateOf=page=>page?.state?.captcha?'challenge':page?.state?.loginRequired?'login_required':null;
export function hasReadableText(page){return String(page?.text||'').trim().length>=(page?.extraction?.primaryContent?20:80)}
export async function boundedPage(bridge,browserId,tabId,expression,{expectedURL,timeoutMs,deadline=Date.now()+timeoutMs,detail=false}={}){
 const started=Date.now();let latest,frameRetries=0,polls=0,evaluationMs=0,stableSince=null,previous='';
 function done(extra={}){return {...latest,...extra,polling:{polls,evaluationMs,waitMs:Date.now()-started,earlyStop:extra.earlyStop||null}}}
 while(Date.now()<deadline){
  const before=Date.now();if(latest&&deadline-before<200)return done({timedOut:true});
  try{latest=await bridge.evaluate(browserId,tabId,expression,Math.min(15000,Math.max(1,deadline-Date.now())));polls++}catch(e){if(e.frameChanged&&frameRetries++<2){await pause(Math.min(250,Math.max(0,deadline-Date.now())));continue}if(latest&&(e.timeout||Date.now()>=deadline-300))return done({timedOut:true,lastPollingError:safeCode(e)});throw e}
  evaluationMs+=Date.now()-before;
  if(typeof latest==='string'){try{latest=JSON.parse(latest)}catch{throw fail('page_extraction_invalid')}}
  if(!latest||typeof latest!=='object')throw fail('page_extraction_invalid');
  if(stateOf(latest)&&latest.readyState!=='loading')return done();
  const right=detail?detailLocation(expectedURL,latest):searchLocation(expectedURL,latest.url);
  if(right&&latest.readyState!=='loading'){
   if(detail&&hasReadableText(latest))return done();
   if(!detail&&latest.items?.length)return done();
   if(latest.state?.empty)return done();
   if(detail&&latest.readyState==='complete'&&!latest.state?.loading){
    const fingerprint=String(latest.url)+'|'+String(latest.title)+'|'+String(latest.text||'');
    if(fingerprint!==previous){previous=fingerprint;stableSince=Date.now()}
    if(stableSince!==null&&Date.now()-stableSince>=2500)return done({earlyStop:'stable_no_readable_content'});
   }else stableSince=null;
  }
  await pause(Math.min(polls<3?250:450,Math.max(0,deadline-Date.now())));
 }
 return done({timedOut:true});
}
export async function saveJSON(file,value){await writeFile(file,JSON.stringify(value,null,2)+'\n',{mode:0o600});await chmod(file,0o600)}
export async function parallelGroups(tasks,key,concurrency,work){
 const grouped=new Map();for(const t of tasks){const k=key(t);if(!grouped.has(k))grouped.set(k,[]);grouped.get(k).push(t)}
 const groups=[...grouped.values()];let next=0,stopped=false,failure;
 await Promise.all(Array.from({length:Math.min(concurrency,groups.length)},async()=>{
  while(!stopped&&next<groups.length){const group=groups[next++];for(const task of group){if(stopped)break;try{await work(task)}catch(e){if(!stopped)failure=e;stopped=true;break}}}
 }));
 if(stopped)throw failure;
}
export async function createRun(options,{bridge}={}){
 const started=Date.now();bridge=bridge||await Bridge.connect();
 const output=path.resolve(options.output||path.join(process.cwd(),'.local','easybr-search',new Date().toISOString().replace(/[:.]/g,'-')));
 await mkdir(output,{recursive:true,mode:0o700});if((await readdir(output)).length)throw fail('output_directory_not_empty');await chmod(output,0o700);await mkdir(path.join(output,'sources'),{mode:0o700});
 const before=Date.now(),browsers=await inventory(bridge),inventoryMs=Date.now()-before;if(!browsers.length)throw fail('no_online_browser');
 const codeFiles=['search.mjs','runtime.mjs','read.mjs','bridge.mjs','results.mjs','platforms.mjs','extract.mjs','config.mjs','doctor.mjs','handoff.mjs'];
 const hashes=await Promise.all(codeFiles.map(async f=>[f,createHash('sha256').update(await readFile(new URL(f,import.meta.url))).digest('hex')]));
 const privateRun={schemaVersion:1,runId:randomUUID().slice(0,8),codeFingerprint:Object.fromEntries(hashes),startedAt:new Date(started).toISOString(),routes:[],candidates:[],navigation:[],cleanup:[]};
 const contexts=new Map(),loads=new Map();let queue=Promise.resolve();
 const atomic=(name,value)=>{const snapshot=structuredClone(value);queue=queue.then(async()=>{const temp=path.join(output,name+'.tmp');await saveJSON(temp,snapshot);await rename(temp,path.join(output,name))});return queue};
 const journal=()=>atomic('private-run.json',privateRun);
 function route(profile,map={}){
  const selected=selectBrowser(profile,browsers,map,loads),b=selected.browser;
  loads.set(b.browserId,(loads.get(b.browserId)||0)+1);
  if(!contexts.has(b.browserId))contexts.set(b.browserId,{browser:b,session:'easybr-search-'+privateRun.runId+'-'+contexts.size,tabId:null,owned:new Set(),started:false,unknownNavigation:false});
  privateRun.routes.push({platform:profile.id,browserId:b.browserId,browserName:b.displayName,selectionSource:selected.source,warning:selected.warning||null});return contexts.get(b.browserId);
 }
 async function initialize(){
  await Promise.all([...contexts.values()].map(async ctx=>{let backgroundExecution=null;try{const c=await bridge.command(ctx.browser.browserId,'capabilities',{});backgroundExecution=backgroundCapability(c.features?.backgroundExecution)}catch{}privateRun.routes.filter(r=>r.browserId===ctx.browser.browserId).forEach(r=>{r.backgroundExecution=backgroundExecution})}));await journal();
 }
 async function navigate(ctx,url,{newTab=false,timeoutMs=18000}={}){
  if(!publicURL(url))throw fail('unsafe_navigation_url');ctx.started=true;ctx.unknownNavigation=true;await journal();
  const d=await bridge.command(ctx.browser.browserId,'navigate',{url,session:ctx.session,groupTitle:'easybrSearch 搜索',...((newTab||!ctx.tabId)?{newTab:true}:{})},Math.min(20000,timeoutMs));
  const id=d.tabId||d.tab?.id;if(!Number.isSafeInteger(id))throw fail('navigation_tab_missing');ctx.unknownNavigation=false;ctx.tabId=id;ctx.owned.add(id);privateRun.navigation.push({browserId:ctx.browser.browserId,session:ctx.session,tabId:id,url});await journal();return id;
 }
 async function cleanup(){
  const summary={remaining:[],verified:true};
  for(const ctx of contexts.values()){
   if(!ctx.started)continue;let closed=false;const browserIndex=[...contexts.keys()].indexOf(ctx.browser.browserId);
   if(ctx.unknownNavigation){summary.verified=false;summary.remaining.push({browserIndex,status:'navigation_outcome_unverified'})}
   try{await bridge.command(ctx.browser.browserId,'close_session',{session:ctx.session});closed=true}catch{}
   try{let tabs=tabsOf(await bridge.command(ctx.browser.browserId,'list_tabs',{}));for(const t of tabs.filter(t=>ctx.owned.has(t.id??t.tabId))){try{await bridge.command(ctx.browser.browserId,'close_tab',{tabId:t.id??t.tabId})}catch{}}
    tabs=tabsOf(await bridge.command(ctx.browser.browserId,'list_tabs',{}));const remaining=tabs.filter(t=>ctx.owned.has(t.id??t.tabId));if(remaining.length)summary.remaining.push({browserIndex,count:remaining.length});privateRun.cleanup.push({browserId:ctx.browser.browserId,session:ctx.session,closeAcknowledged:closed,remaining:remaining.map(t=>t.id??t.tabId)});
   }catch{summary.verified=false;summary.remaining.push({browserIndex,status:'unverified'})}
  }
  await journal();return summary;
 }
 return {bridge,output,started,inventoryMs,privateRun,contexts,atomic,journal,route,initialize,navigate,cleanup};
}
