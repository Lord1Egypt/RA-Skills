import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
import {parseCLI,validateCases,runBenchmark} from '../scripts/benchmark.mjs';

const cli=fileURLToPath(new URL('../scripts/benchmark.mjs',import.meta.url));
const options={queries:['Manim quickstart'],platforms:['bilibili'],limit:4,read:2,timeoutMs:18000,concurrency:3};
async function fixture(t,cases=[{name:'one',options}]){
 const root=await fs.mkdtemp(path.join(os.tmpdir(),'easybr-benchmark-'));t.after(()=>fs.rm(root,{recursive:true,force:true}));
 const casesFile=path.join(root,'cases.json'),output=path.join(root,'report');await fs.writeFile(casesFile,JSON.stringify({schemaVersion:1,cases}));return {root,casesFile,output,repeat:1};
}
const report=(platform='bilibili')=>({searches:[{platform,status:'ok',count:1,elapsedMs:3}],results:[{readStatus:'read',title:'private body must not escape',url:'https://example.test/?token=secret'}],cleanup:{verified:true,remaining:[]}});

test('CLI accepts comparison engine and private map, with strict numeric bounds and required paths',()=>{
 assert.deepEqual(parseCLI(['benchmark','--cases','a.json','--output','out','--engine','/tmp/search.mjs','--repeat','2','--browser-map','private.json']),{repeat:2,casesFile:'a.json',output:'out',engine:'/tmp/search.mjs',browserMapFile:'private.json'});
 for(const args of [[],['--cases','a'],['--cases','a','--output','out','--repeat','0'],['--cases','a','--output','out','--repeat','4'],['--cases','a','--output','out','--repeat','1.5'],['--cases','a','--output','out','--engine','relative.mjs'],['--cases','a','--output','out','--unknown','x'],['--cases','a','--output','--read']])assert.throws(()=>parseCLI(args));
});
test('cases require an explicit platform scope and bounded search budgets before any engine work',()=>{
 assert.deepEqual(validateCases([{name:'bili-only',options}])[0].options.platforms,['bilibili']);
 for(const mutation of [o=>delete o.platforms,o=>o.platforms=[],o=>o.platforms=['unknown-platform'],o=>o.read=11,o=>o.limit=0,o=>o.timeoutMs=100,o=>o.concurrency=5,o=>o.queries=[],o=>o.queries=['same','same'],o=>o.output='/tmp/not-owned',o=>o.browserMap={bilibili:42}]){
  const value=structuredClone(options);mutation(value);assert.throws(()=>validateCases([{name:'bad',options:value}]));
 }
 assert.throws(()=>validateCases([{name:'duplicate',options},{name:'duplicate',options}]));
});
test('invalid scope leaves no output and never invokes the engine',async t=>{
 const f=await fixture(t,[{name:'bad',options:{...options,platforms:[]}}]);let called=false;
 await assert.rejects(runBenchmark(f,{runSearch:async()=>{called=true;}}),{code:'invalid_platforms'});assert.equal(called,false);await assert.rejects(fs.access(f.output));
});
test('nonempty output refuses before engine calls and preserves existing files',async t=>{
 const f=await fixture(t);await fs.mkdir(f.output);await fs.writeFile(path.join(f.output,'keep'),'unchanged');let called=false;
 await assert.rejects(runBenchmark(f,{runSearch:async()=>{called=true;}}),{code:'output_directory_not_empty'});assert.equal(called,false);assert.equal(await fs.readFile(path.join(f.output,'keep'),'utf8'),'unchanged');
});
test('cases/repeats are sequential, private routing overrides case maps, summaries exclude sensitive inputs',async t=>{
 const f=await fixture(t,[{name:'one',options:{...options,browserMap:{bilibili:'case-private-identity'}}},{name:'two',options}]);f.repeat=2;
 f.browserMapFile=path.join(f.root,'routes.json');await fs.writeFile(f.browserMapFile,JSON.stringify({bilibili:'mapped-private-identity'}));
 let active=0,peak=0,clock=0;const calls=[];
 const {report:result}=await runBenchmark(f,{now:()=>clock,runSearch:async(input,{onProgress})=>{
  active++;peak=Math.max(peak,active);calls.push(input);assert.deepEqual(input.platforms,['bilibili']);assert.equal(input.browserMap.bilibili,'mapped-private-identity');clock+=4;
  onProgress({stage:'search',platform:'bilibili',query:input.queries[0]});clock+=7;onProgress({stage:'searched',platform:'bilibili',query:input.queries[0],status:'ok',count:1});clock+=9;
  await Promise.resolve();active--;return {output:input.output,report:report()};
 }});
 assert.equal(peak,1);assert.equal(calls.length,4);assert.equal(new Set(calls.map(x=>x.output)).size,4);assert.deepEqual(result.runs.map(r=>r.firstResultsMs),[11,11,11,11]);assert.equal(result.summary.wall.n,4);assert.equal(result.summary.wall.meanMs,20);assert.equal(result.means[0].wall.n,2);
 const publicFiles=(await fs.readFile(path.join(f.output,'benchmark.json'),'utf8'))+(await fs.readFile(path.join(f.output,'benchmark.md'),'utf8'));
 for(const secret of ['mapped-private-identity','case-private-identity','token=secret','private body must not escape'])assert.ok(!publicFiles.includes(secret));
});
test('instrumentation records actual overlapping browser I/O and searches without exposing identities',async t=>{
 const f=await fixture(t,[{name:'parallel',options:{...options,platforms:['baidu','google']}}]);const realBridge={command:async()=>new Promise(resolve=>setTimeout(resolve,12)),evaluate:async()=>null,browsers:async()=>[]};
 const {report:result}=await runBenchmark(f,{bridge:realBridge,runSearch:async(input,{bridge,onProgress})=>{
  await Promise.all(input.platforms.map(async(platform,i)=>{onProgress({stage:'search',platform,query:'q'});await bridge.command('private-browser-'+i,'navigate',{url:'private-signed-url'});onProgress({stage:'searched',platform,query:'q',status:'ok',count:1});}));return {report:report('baidu')};
 }});
 const p=result.runs[0].parallelism;assert.equal(p.maxActiveSearchTasks,2);assert.equal(p.maxConcurrentBrowsers,2);assert.equal(p.maxConcurrentBrowserCalls,2);assert.equal(p.searchIntervals.length,2);assert.ok(p.observedSearchOverlap&&p.observedBrowserOverlap);assert.ok(!JSON.stringify(result).includes('private-browser'));
});
test('no-result samples remain in wall mean but never fabricate a first-result time',async t=>{
 const f=await fixture(t);const {report:result}=await runBenchmark(f,{runSearch:async()=>({report:{searches:[{platform:'bilibili',status:'challenge',count:0,elapsedMs:1}],results:[],cleanup:{verified:true,remaining:[]}}})});
 assert.equal(result.runs[0].status,'no_results');assert.equal(result.runs[0].firstResultsMs,null);assert.equal(result.summary.wall.n,1);assert.deepEqual(result.summary.firstResults,{n:0,meanMs:null});assert.equal(result.aborted,false);
});
test('partial platform failures and failed reads stay visible in recorded statuses',async t=>{
 const f=await fixture(t);const r=report();r.searches.push({platform:'csdn',status:'challenge',count:0,elapsedMs:7});r.results.push({readStatus:'content_unavailable'});
 const {report:result}=await runBenchmark(f,{runSearch:async()=>({report:r})});assert.equal(result.runs[0].status,'partial');assert.equal(result.runs[0].read,1);assert.equal(result.runs[0].readStatuses.content_unavailable,1);assert.equal(result.runs[0].searches[1].status,'challenge');
});
test('unverified cleanup stops later cases and strips browser/tab details from summary',async t=>{
 const f=await fixture(t,[{name:'one',options},{name:'must-not-run',options}]);let called=0;
 const {report:result}=await runBenchmark(f,{runSearch:async()=>{called++;const r=report();r.cleanup={verified:false,remaining:[{browserId:'private-route',tabId:991,count:1,status:'unverified'}]};return {report:r};}});
 assert.equal(called,1);assert.equal(result.aborted,true);assert.equal(result.runs[0].status,'cleanup_unverified');assert.deepEqual(result.runs[0].cleanup.remaining,[{count:1,status:'unverified'}]);assert.ok(!JSON.stringify(result).includes('private-route'));assert.equal(result.means[1].wall.n,0);
});
test('engine errors are recorded without raw messages and stop because cleanup cannot be verified',async t=>{
 const f=await fixture(t);const {report:result}=await runBenchmark(f,{runSearch:async()=>{throw new Error('secret token and private body');}});assert.equal(result.runs[0].errorCode,'benchmark_case_failed');assert.equal(result.aborted,true);assert.ok(!JSON.stringify(result).includes('secret token'));
});
test('real CLI can import a frozen fixture engine without needing Bridge credentials',async t=>{
 const f=await fixture(t);const engine=path.join(f.root,'frozen-search.mjs');await fs.writeFile(engine,`export async function runSearch(input,{onProgress}){if(input.platforms.join(',')!=='bilibili')throw Error('scope changed');onProgress({stage:'search',platform:'bilibili',query:'q'});onProgress({stage:'searched',platform:'bilibili',query:'q',status:'ok',count:1});return {output:input.output,report:${JSON.stringify(report())}}}`);
 const result=spawnSync(process.execPath,[cli,'--cases',f.casesFile,'--output',f.output,'--engine',engine,'--repeat','1'],{encoding:'utf8',env:{PATH:process.env.PATH,HOME:f.root}});assert.equal(result.status,0,result.stderr);assert.equal(JSON.parse(await fs.readFile(path.join(f.output,'benchmark.json'))).engine.file,'frozen-search.mjs');
 const bad=spawnSync(process.execPath,[cli,'--cases',f.casesFile,'--output',path.join(f.root,'bad'),'--repeat','4'],{encoding:'utf8'});assert.equal(bad.status,2);assert.match(bad.stderr,/invalid_repeat/);assert.ok(!bad.stderr.includes(' at '));
});
