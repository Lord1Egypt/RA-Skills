import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp,rm,readFile,mkdir,readdir} from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import {defaultCheckPlatforms,parseCheckCLI,runPlatformCheck,summarizeCheck,probeFirstVisibleCard,checkMarkdown} from '../scripts/platform-check.mjs';

test('reusable CLI chooses only the requested scope and rejects ambiguous missing options',()=>{
 assert.deepEqual(defaultCheckPlatforms(),['baidu','google','bing','douyin','xiaohongshu']);
 assert.deepEqual(parseCheckCLI(['--platforms','bili,xhs','--query','AI动画','--output','.local/test']),{platforms:['bili','xhs'],queries:['AI动画'],output:'.local/test'});
 assert.throws(()=>parseCheckCLI(['--platforms','bili,']),{code:'invalid_platforms'});
 assert.throws(()=>parseCheckCLI(['--output']),{code:'missing_option'});
 assert.deepEqual(parseCheckCLI(['--observe-results']),{observeResults:true});
});
function fixture(){return {startedAt:'2026-01-01',finishedAt:'2026-01-01',queries:['Manim'],searches:[{platform:'xiaohongshu',query:'Manim',method:'native',status:'ok',count:1,elapsedMs:42}],results:[{platform:'xiaohongshu',query:'Manim',title:'教程结果',url:'https://www.xiaohongshu.com/explore/0123456789abcdef01234567?xsec_token=fixture-secret&utm_source=test',snippet:'不要进入摘要的正文',contentType:'post',browserId:'never-public'}],execution:{browserCount:2,searchConcurrency:2,sameBrowser:'serial'},cleanup:{verified:true,remaining:[]},timings:{totalMs:50}}}

test('coverage samples have no browser routes, source body or signed search-navigation parameters',()=>{
 const input=fixture();input.results.push({platform:'xiaohongshu',query:'Manim',title:'未解析结果',url:'https://www.google.com.hk/goto?url=fixture-opaque',snippet:'private snippet'});
 const r=summarizeCheck(input);const s=JSON.stringify(r);
 assert.ok(!/fixture-secret|fixture-opaque|browserId|不要进入|private snippet/.test(s));assert.equal(r.observations[0].samples[1].url,null);assert.equal(r.observations[0].samples[1].unresolvedRedirect,true);
 assert.equal(r.cleanup.verified,true);
});

test('one batched run delegates serialization, forces read0/limit3 and creates a reusable coverage pair',async t=>{
 const base=await mkdtemp(path.join(os.tmpdir(),'easybr-check-'));t.after(()=>rm(base,{recursive:true,force:true}));let seen;
 const output=path.join(base,'.local','run');
 const r=await runPlatformCheck({platforms:['xhs'],queries:['Manim'],output,read:10,limit:20},{runSearchImpl:async(o)=>{seen=o;return {report:fixture()}}});
 assert.equal(seen.read,0);assert.equal(seen.limit,3);assert.deepEqual(seen.platforms,['xiaohongshu']);assert.equal(seen.timeoutMs,8000);
 assert.equal(r.report.counts.ok,1);assert.ok((await readFile(path.join(output,'coverage.md'),'utf8')).includes('平台覆盖观察'));
});

test('blocking states never cause extra browser diagnostics; unrecognized complete pages get private reusable diagnostics',async t=>{
 const base=await mkdtemp(path.join(os.tmpdir(),'easybr-check-'));t.after(()=>rm(base,{recursive:true,force:true}));let reads=0;
 const output=path.join(base,'.local','run');
 await runPlatformCheck({platforms:['xiaohongshu'],output,observeResults:true},{runSearchImpl:async(o,{onSearchPage})=>{
  const bridge={evaluate:async()=>{reads++;return {bodyText:'private DOM text',links:[{href:'https://example.com?token=fixture-secret'}]}}};
  const args={platform:'xiaohongshu',query:'Manim',browserId:'private-browser',tabId:1,bridge};
  await onSearchPage({...args,page:{readyState:'complete',state:{captcha:true},items:[]}});
  await onSearchPage({...args,page:{readyState:'complete',state:{loginRequired:true},items:[]}});assert.equal(reads,0);
  await onSearchPage({...args,page:{readyState:'complete',state:{},items:[{title:'可见结果'}]}});assert.equal(reads,1);return {report:fixture()};
 }});
 assert.equal((await readdir(path.join(output,'diagnostics'))).length,1);
 assert.ok(!/private DOM text|fixture-secret|private-browser/.test(await readFile(path.join(output,'coverage.json'),'utf8')));
});


test('an extraction error can collect one bounded private DOM diagnostic even without a last page snapshot',async t=>{
 const base=await mkdtemp(path.join(os.tmpdir(),'easybr-check-'));t.after(()=>rm(base,{recursive:true,force:true}));let reads=0;
 const output=path.join(base,'.local','run');
 await runPlatformCheck({platforms:['douyin'],output},{runSearchImpl:async(o,{onSearchPage})=>{
  await onSearchPage({platform:'douyin',query:'Manim',browserId:'private-id',tabId:1,page:{},errorCode:'bridge_command_failed',errorPhase:'extract',bridge:{evaluate:async()=>{reads++;return {url:'https://www.douyin.com/search/Manim',readyState:'complete',bodyText:'private shell evidence'}}}});
  const report=fixture();report.searches=[{platform:'douyin',query:'Manim',status:'unavailable',count:0,errorCode:'bridge_command_failed',errorPhase:'extract'}];report.results=[];return {report};
 }});
 assert.equal(reads,1);const files=await readdir(path.join(output,'diagnostics'));const diagnostic=JSON.parse(await readFile(path.join(output,'diagnostics',files[0]),'utf8'));
 assert.equal(diagnostic.errorPhase,'extract');assert.ok(!/private shell evidence|private-id/.test(await readFile(path.join(output,'coverage.json'),'utf8')));
});


test('the explicit single-card DOM probe verifies the real modal URL without activating or inventing a direct video route',async()=>{
 const calls=[];const tabs=[{id:1,windowId:1,active:true},{id:2,windowId:1,active:false}];let reads=0;
 const bridge={command:async(id,action,args)=>{calls.push({action,args});return action==='list_tabs'?tabs:{}},evaluate:async()=>++reads===1?{id:'1234567890123456789',selector:'#waterfall_item_1234567890123456789 .search-result-card',url:'https://www.douyin.com/search/Manim'}:{url:'https://www.douyin.com/search/Manim?modal_id=1234567890123456789',readyState:'complete'}};
 const r=await probeFirstVisibleCard({bridge,browserId:'private',tabId:2,wait:async()=>{}});
 assert.equal(r.status,'route_verified');assert.equal(r.routeMatched,true);assert.ok(r.actualURL.includes('/search/Manim?modal_id='));assert.equal(calls.filter(x=>x.action==='click').length,1);assert.equal(calls.find(x=>x.action==='click').args.mode,'dom');assert.ok(!calls.some(x=>x.action==='activate_tab'));assert.equal(r.cleanupVerified,true);
});

test('single-card passive new-tab selection only restores with focus false and closes the proven task child',async()=>{
 const calls=[];let lists=0,reads=0;const before=[{id:1,windowId:1,active:true},{id:2,windowId:1,active:false}];
 const child={id:3,windowId:1,openerTabId:2,active:true,url:'https://www.douyin.com/video/1234567890123456789'};
 const bridge={command:async(id,action,args)=>{calls.push({action,args});return action==='list_tabs'?(++lists===2?[...before.map(t=>({...t,active:false})),child]:before):{}},evaluate:async()=>++reads===1?{id:'1234567890123456789',selector:'#waterfall_item_1234567890123456789 .search-result-card',url:'https://www.douyin.com/search/Manim'}:{url:'https://www.douyin.com/search/Manim',readyState:'complete'}};
 const r=await probeFirstVisibleCard({bridge,browserId:'private',tabId:2,wait:async()=>{}});
 assert.equal(r.status,'route_verified');assert.equal(r.passiveSelection,true);assert.equal(r.selectionRestored,true);assert.equal(r.closedNewCount,1);
 assert.deepEqual(calls.find(x=>x.action==='activate_tab').args,{tabId:1,focus:false,restoreSelection:true});assert.deepEqual(calls.find(x=>x.action==='close_tab').args,{tabId:3});assert.equal(calls.filter(x=>x.action==='click').length,1);
});


test('an explicit minimal CDP probe preserves safe diagnostic failure evidence without page body in public coverage',async t=>{
 const base=await mkdtemp(path.join(os.tmpdir(),'easybr-check-'));t.after(()=>rm(base,{recursive:true,force:true}));let reads=0;const output=path.join(base,'.local','run');
 await runPlatformCheck({platforms:['reddit'],output,probeCDP:true},{runSearchImpl:async(o,{onSearchPage})=>{
  await onSearchPage({platform:'reddit',query:'Manim',browserId:'private-id',tabId:1,page:{},errorCode:'bridge_command_failed',errorPhase:'extract',bridge:{evaluate:async()=>{if(++reads===1)throw Object.assign(new Error('private bridge detail'),{code:'bridge_command_failed'});return {url:'https://www.reddit.com/search/?q=Manim',readyState:'complete',linkCount:0,textLength:10}}}});return {report:fixture()};
 }});
 const files=await readdir(path.join(output,'diagnostics'));const d=JSON.parse(await readFile(path.join(output,'diagnostics',files[0]),'utf8'));assert.equal(reads,2);assert.equal(d.diagnosticErrorCode,'bridge_command_failed');assert.equal(d.channel.readyState,'complete');assert.ok(!/private bridge detail|private-id|textLength/.test(await readFile(path.join(output,'coverage.json'),'utf8')));
});


test('coverage marks titles-only cards as a search page rather than a verified detail link',()=>{
 const report=fixture();report.searches=[{platform:'douyin',query:'Manim',status:'titles_only',count:1}];report.results=[{platform:'douyin',query:'Manim',title:'实际搜索卡片标题',url:'https://www.douyin.com/search/Manim?type=general',linkStatus:'search_page_only',contentType:'search-card'}];
 const summary=summarizeCheck(report);assert.equal(summary.observations[0].samples[0].linkStatus,'search_page_only');assert.ok(checkMarkdown(summary).includes('仅搜索页，无详情直链'));
});
