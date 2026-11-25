#!/usr/bin/env node
import {isCLIEntry} from './cli-entry.mjs';
import {readFile,writeFile,mkdir,readdir,chmod} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
import {performance} from 'node:perf_hooks';
import {Bridge} from './bridge.mjs';
import {getPlatform} from './platforms.mjs';
import {validateBrowserMap} from './config.mjs';

const fail=code=>Object.assign(new Error(code),{code});
const sha=value=>createHash('sha256').update(value).digest('hex');
const number=(value,min,max,key)=>{if(!Number.isInteger(value)||value<min||value>max)throw fail('invalid_'+key);return value};
const safeCode=error=>/^[a-zA-Z][a-zA-Z0-9_-]{0,79}$/.test(error?.code||'')?error.code:'benchmark_case_failed';
const rounded=value=>Math.round(value*1000)/1000;
const mean=values=>({n:values.length,meanMs:values.length?rounded(values.reduce((a,b)=>a+b,0)/values.length):null});
const help='node scripts/benchmark.mjs --cases FILE --output EMPTY_DIR [--engine ABS_SEARCH_MODULE] [--repeat 1..3] [--browser-map PRIVATE_JSON]\nCases run sequentially; each runSearch controls its own browser concurrency. Reports contain timings/counts, not page text, URLs or browser identities.';

export function parseCLI(input){
 const args=[...input];if(args[0]==='benchmark')args.shift();const options={repeat:1};
 const keys={'--cases':'casesFile','--output':'output','--engine':'engine','--repeat':'repeat','--browser-map':'browserMapFile'};
 while(args.length){const arg=args.shift();if(arg==='--help'||arg==='-h')return {help:true};if(!keys[arg])throw fail('unknown_option');const value=args.shift();if(!value||value.startsWith('--'))throw fail('missing_option');if(Object.hasOwn(options,keys[arg])&&arg!=='--repeat')throw fail('duplicate_option');options[keys[arg]]=arg==='--repeat'?Number(value):value;}
 if(!options.casesFile||!options.output)throw fail('cases_and_output_required');number(options.repeat,1,3,'repeat');if(options.engine&&!path.isAbsolute(options.engine))throw fail('engine_must_be_absolute');return options;
}
export function validateCases(value){
 const cases=Array.isArray(value)?value:value?.schemaVersion===1?value.cases:null;
 if(!Array.isArray(cases)||!cases.length||cases.length>50)throw fail('invalid_cases');const names=new Set();
 return cases.map(entry=>{
  if(!entry||typeof entry.name!=='string'||!entry.name.trim()||entry.name.length>120||/[\r\n\x00-\x1f]/.test(entry.name)||names.has(entry.name))throw fail('invalid_case_name');names.add(entry.name);
  const o=entry.options;if(!o||Array.isArray(o)||typeof o!=='object')throw fail('invalid_case_options');
  if(Object.keys(o).some(key=>!['question','queries','platforms','limit','read','timeoutMs','concurrency','browserMap'].includes(key)))throw fail('unknown_case_option');
  if(!Array.isArray(o.queries)||o.queries.length<1||o.queries.length>5||o.queries.some(q=>typeof q!=='string'||!q.trim()||q.length>500)||new Set(o.queries).size!==o.queries.length)throw fail('invalid_queries');
  if(!Array.isArray(o.platforms)||o.platforms.length<1||o.platforms.length>20||o.platforms.some(id=>typeof id!=='string'))throw fail('invalid_platforms');
  const platforms=o.platforms.map(id=>getPlatform(id).id);if(new Set(platforms).size!==platforms.length)throw fail('invalid_platforms');
  if(o.question!==undefined&&(typeof o.question!=='string'||!o.question.trim()||o.question.length>2000))throw fail('invalid_question');
  return {name:entry.name,options:{...o,queries:[...o.queries],platforms,limit:number(o.limit??5,1,20,'limit'),read:number(o.read??3,0,10,'read'),timeoutMs:number(o.timeoutMs??18000,2000,60000,'timeoutMs'),concurrency:number(o.concurrency??3,1,4,'concurrency'),browserMap:validateBrowserMap(o.browserMap??{})}};
 });
}
function lazyBridge(){let pending;const get=()=>pending??=Bridge.connect();return Object.fromEntries(['browsers','command','evaluate'].map(method=>[method,async(...args)=>(await get())[method](...args)]));}
function observedBridge(base,metrics){
 const active=new Map();
 async function tracked(browserId,action,invoke){
  if(!['navigate','scroll','cdp','evaluate'].includes(action))return invoke();
  active.set(browserId,(active.get(browserId)||0)+1);metrics.used.add(browserId);metrics.calls++;
  metrics.maxConcurrentBrowserCalls=Math.max(metrics.maxConcurrentBrowserCalls,[...active.values()].reduce((a,b)=>a+b,0));metrics.maxConcurrentBrowsers=Math.max(metrics.maxConcurrentBrowsers,active.size);
  try{return await invoke()}finally{const left=active.get(browserId)-1;if(left)active.set(browserId,left);else active.delete(browserId)}
 }
 return {browsers:(...args)=>base.browsers(...args),command:(id,action,...args)=>tracked(id,action,()=>base.command(id,action,...args)),evaluate:(id,...args)=>tracked(id,'evaluate',()=>base.evaluate(id,...args))};
}
function cleanCleanup(value){
 if(!value||typeof value.verified!=='boolean'||!Array.isArray(value.remaining))return {verified:false,remaining:[{status:'cleanup_not_reported'}]};
 return {verified:value.verified,remaining:value.remaining.map(item=>({...(Number.isSafeInteger(item?.count)&&item.count>=0?{count:item.count}:{}),status:typeof item?.status==='string'&&/^[a-z_]{1,64}$/.test(item.status)?item.status:'remaining_pages'}))};
}
function counts(values){const out={};for(const value of values){const key=typeof value==='string'&&/^[a-z_]{1,64}$/.test(value)?value:'unknown';out[key]=(out[key]||0)+1;}return out;}
function markdown(report){
 const rows=['# easybrSearch benchmark','',`Samples: n=${report.runs.length}; repeat=${report.repeat}. Cases run sequentially.`, '', '| Case | Repeat | Status | wallMs | firstResultsMs | Results | Read | Search overlap | Browser I/O overlap | Cleanup |','| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |'];
 for(const r of report.runs)rows.push(`| ${r.name.replaceAll('|','\\|')} | ${r.repeat} | ${r.status} | ${r.wallMs} | ${r.firstResultsMs??'—'} | ${r.count} | ${r.read} | ${r.parallelism.maxActiveSearchTasks} | ${r.parallelism.maxConcurrentBrowsers} | ${r.cleanup.verified&&!r.cleanup.remaining.length?'verified':'unverified'} |`);
 rows.push('','## Means','', '| Case | n wall | Mean wallMs | n first-results | Mean firstResultsMs |','| --- | ---: | ---: | ---: | ---: |');
 for(const group of report.means)rows.push(`| ${group.name.replaceAll('|','\\|')} | ${group.wall.n} | ${group.wall.meanMs??'—'} | ${group.firstResults.n} | ${group.firstResults.meanMs??'—'} |`);
 rows.push('',`Overall wall mean: ${report.summary.wall.meanMs??'—'} ms (n=${report.summary.wall.n}); first-results mean: ${report.summary.firstResults.meanMs??'—'} ms (n=${report.summary.firstResults.n}).`,'',...report.measurementNotes.map(note=>'- '+note),'');return rows.join('\n');
}
export async function runBenchmark(options,{runSearch,bridge,now=()=>performance.now(),onProgress=()=>{}}={}){
 number(options.repeat??1,1,3,'repeat');if(!options.casesFile||!options.output)throw fail('cases_and_output_required');if(options.engine&&!path.isAbsolute(options.engine))throw fail('engine_must_be_absolute');
 const bytes=await readFile(path.resolve(options.casesFile));let parsed;try{parsed=JSON.parse(bytes)}catch{throw fail('cases_invalid_json')};const cases=validateCases(parsed);
 let browserMap,routeHash=null;if(options.browserMapFile){const raw=await readFile(path.resolve(options.browserMapFile));try{browserMap=validateBrowserMap(JSON.parse(raw))}catch{throw fail('browser_map_invalid')};routeHash=sha(raw);}
 const output=path.resolve(options.output);await mkdir(output,{recursive:true,mode:0o700});if((await readdir(output)).length)throw fail('output_directory_not_empty');await chmod(output,0o700);
 const engine=options.engine||fileURLToPath(new URL('./search.mjs',import.meta.url));const engineHash=sha(await readFile(engine));if(!runSearch){const module=await import(pathToFileURL(engine).href);runSearch=module.runSearch;}if(typeof runSearch!=='function')throw fail('engine_runSearch_required');
 const repeat=options.repeat??1,base=bridge??lazyBridge();const report={schemaVersion:1,startedAt:new Date().toISOString(),repeat,caseInputSha256:sha(bytes),browserMapSha256:routeHash,engine:{file:path.basename(engine),sha256:engineHash},caseExecution:'sequential',runs:[],aborted:false};
 outer:for(let index=0;index<cases.length;index++)for(let iteration=1;iteration<=repeat;iteration++){
  const entry=cases[index],child=path.join(output,`case-${String(index+1).padStart(2,'0')}-run-${iteration}`),start=now();let first=null,maxSearch=0,activeSearch=0;const jobs=new Map(),intervals=[],io={used:new Set(),calls:0,maxConcurrentBrowserCalls:0,maxConcurrentBrowsers:0};
  const progress=event=>{
   if(event.stage==='search'){activeSearch++;maxSearch=Math.max(maxSearch,activeSearch);const key=JSON.stringify([event.platform,event.query]);jobs.set(key,{platform:event.platform,startedMs:rounded(now()-start)});}
   if(event.stage==='searched'){const key=JSON.stringify([event.platform,event.query]),job=jobs.get(key);if(job){intervals.push({...job,finishedMs:rounded(now()-start)});jobs.delete(key);activeSearch--;}if(first===null&&event.status==='ok'&&event.count>0)first=rounded(now()-start);}
  };
  const row={name:entry.name,repeat:iteration,input:{platforms:entry.options.platforms,queryCount:entry.options.queries.length,limit:entry.options.limit,read:entry.options.read,timeoutMs:entry.options.timeoutMs,concurrency:entry.options.concurrency},evidenceDirectory:path.relative(output,child)};
  try{
   const returned=await runSearch({...entry.options,...(browserMap?{browserMap}:{}),output:child},{bridge:observedBridge(base,io),onProgress:progress});const result=returned?.report;
   if(!result||!Array.isArray(result.searches)||!Array.isArray(result.results))throw fail('engine_report_invalid');
   row.searches=result.searches.map(s=>({platform:s.platform,status:s.status,count:s.count,elapsedMs:s.elapsedMs}));row.count=result.results.length;row.read=result.results.filter(r=>r.readStatus==='read').length;row.readStatuses=counts(result.results.map(r=>r.readStatus));row.cleanup=cleanCleanup(result.cleanup);
   row.status=!row.count?'no_results':result.searches.some(s=>s.status!=='ok')||result.results.some(r=>!['read','not_read'].includes(r.readStatus))?'partial':'ok';
  }catch(error){Object.assign(row,{status:'error',errorCode:safeCode(error),count:0,read:0,searches:[],readStatuses:{},cleanup:{verified:false,remaining:[{status:'engine_failed_no_cleanup_report'}]}});}
  row.wallMs=rounded(now()-start);row.firstResultsMs=first;row.parallelism={configuredConcurrency:entry.options.concurrency,maxActiveSearchTasks:maxSearch,observedSearchOverlap:maxSearch>1,distinctBrowsersUsed:io.used.size,maxConcurrentBrowserCalls:io.maxConcurrentBrowserCalls,maxConcurrentBrowsers:io.maxConcurrentBrowsers,observedBrowserOverlap:io.maxConcurrentBrowsers>1,searchIntervals:intervals};
  if(!row.cleanup.verified||row.cleanup.remaining.length){row.status='cleanup_unverified';report.aborted=true;}
  report.runs.push(row);onProgress({case:row.name,repeat:iteration,status:row.status,wallMs:row.wallMs,firstResultsMs:first,count:row.count,read:row.read,cleanup:row.cleanup});
  if(report.aborted)break outer;
 }
 report.finishedAt=new Date().toISOString();report.means=cases.map(entry=>{const rows=report.runs.filter(r=>r.name===entry.name);return {name:entry.name,wall:mean(rows.map(r=>r.wallMs)),firstResults:mean(rows.map(r=>r.firstResultsMs).filter(x=>x!==null))};});report.summary={wall:mean(report.runs.map(r=>r.wallMs)),firstResults:mean(report.runs.map(r=>r.firstResultsMs).filter(x=>x!==null)),statuses:counts(report.runs.map(r=>r.status))};
 report.measurementNotes=['wallMs measures each runSearch call through return/failure, including inventory, waiting, reads and cleanup; shared Bridge initialization may affect the first run.','firstResultsMs is the first successful nonempty searched progress event, not browser paint or first token; absent observations remain null.','Search overlap is overlapping engine search tasks. Browser I/O overlap counts simultaneous navigate/evaluate/scroll/CDP requests on distinct browsers, not proof of network throughput.','Cases and repeats run sequentially; concurrency is delegated to the engine inside each case. Failed/no-result samples remain in wall means; first-results means state their separate n.','Small local samples depend on network, cache, login, page layout and machine load; these observations are not an SLA or universal speed claim.','Raw engine evidence remains in private per-run directories; benchmark summaries omit page text, URLs, browser mappings and identities.'];
 await writeFile(path.join(output,'benchmark.json'),JSON.stringify(report,null,2)+'\n',{mode:0o600});await writeFile(path.join(output,'benchmark.md'),markdown(report),{mode:0o600});return {output,report};
}
async function main(){const options=parseCLI(process.argv.slice(2));if(options.help){console.log(help);return;}const {report}=await runBenchmark(options,{onProgress:event=>console.error(JSON.stringify(event))});console.log(JSON.stringify({runs:report.runs.length,aborted:report.aborted,summary:report.summary},null,2));if(report.aborted)process.exitCode=2;}
if(isCLIEntry(import.meta.url))main().catch(error=>{console.error(JSON.stringify({error:safeCode(error)}));process.exitCode=2;});
