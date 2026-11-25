import test from 'node:test';import assert from 'node:assert/strict';
import {mkdtemp,readFile,readdir,stat,rm} from 'node:fs/promises';import os from 'node:os';import path from 'node:path';
import {publicURL,rankResults,reportMarkdown} from '../scripts/results.mjs';
import {selectBrowser,runSearch} from '../scripts/search.mjs';
import {Bridge,loopbackURL} from '../scripts/bridge.mjs';

test('canonical URLs hide content signatures while retaining distinct functional ids',()=>{
 assert.equal(publicURL('https://www.youtube.com/watch?v=one&p=2&utm_source=x&token=private#x'),'https://www.youtube.com/watch?v=one&p=2');
 assert.equal(publicURL('https://www.xiaohongshu.com/search_result/0123456789abcdef01234567?xsec_token=private'),publicURL('https://www.xiaohongshu.com/explore/0123456789abcdef01234567'));
 for(const v of ['file:///etc/passwd','https://user:pass@example.com/x','http://127.0.0.1:17777/','http://192.168.2.3/x'])assert.equal(publicURL(v),null);
 assert.notEqual(publicURL('https://youtube.com/watch?v=one'),publicURL('https://youtube.com/watch?v=two'));
});
test('dedup retains a read source and its multiple discovery queries',()=>{
 const a={id:'a',url:'https://example.com/a',title:'动画',snippet:'',platform:'web',query:'a',position:1,readStatus:'not_read'};
 const rows=rankResults([a,{...a,id:'b',query:'b',readStatus:'read',contentFile:'sources/b.json'}],['动画']);assert.equal(rows.length,1);assert.equal(rows[0].contentFile,'sources/b.json');assert.deepEqual(rows[0].discoveredBy,['a','b']);
});
test('specific tool names outrank broad AI beginner terms and Latin tokens respect word boundaries',()=>{
 const rows=rankResults([
  {url:'https://example.com/illustrator',title:'AI 入门 Adobe Illustrator 教程',snippet:'设计基础',query:'AI Manim 入门',position:0},
  {url:'https://example.com/manim',title:'Manim + Cursor 数学动画',snippet:'AI辅助写代码',query:'AI Manim 入门',position:1},
 ],['AI Manim 入门']);assert.equal(rows[0].url,'https://example.com/manim');
 const exact=rankResults([{url:'https://example.com/chain',title:'chain tutorial',snippet:'',query:'AI',position:0},{url:'https://example.com/ai',title:'AI coding',snippet:'',query:'AI',position:1}],['AI']);assert.equal(exact[0].url,'https://example.com/ai');
});
test('an explicit offline or ambiguous browser cannot silently select another account',()=>{
 const p={id:'x',hosts:['example.com'],kind:'social'},b=[{browserId:'a',displayName:'Chrome',tabs:[]},{browserId:'b',displayName:'Chrome',tabs:[]}];
 assert.throws(()=>selectBrowser(p,b,{x:'missing'}),/configured_browser/);assert.throws(()=>selectBrowser(p,b,{x:'Chrome'}),/configured_browser/);assert.equal(selectBrowser(p,b,{x:'b'}).browser.browserId,'b');
});
test('Bridge credentials are limited to the loopback transport and parsed CDP values',async()=>{
 assert.throws(()=>loopbackURL('https://example.com'),/bridge_must_be_local/);assert.throws(()=>loopbackURL('http://private@127.0.0.1:17777'),/bridge_must_be_local/);
 let request;const bridge=new Bridge({token:'private-test-token',fetchImpl:async(url,options)=>{request={url,options};return new Response(JSON.stringify({ok:true,result:{result:{type:'object',value:{ok:1}}}}))}});
 assert.deepEqual(await bridge.evaluate('browser',1,'({ok:1})'),{ok:1});assert.equal(request.options.headers.Authorization,'Bearer private-test-token');assert.equal(new URL(request.url).hostname,'127.0.0.1');
 await assert.rejects(bridge.command('browser','activate_tab',{}),/action_not_readonly_search/);
});
class FakeBridge {
 constructor({login=false,unknown=false}={}){this.login=login;this.unknown=unknown;this.next=100;this.tabs=new Map([['one',new Map([[1,{id:1,url:'https://user.example/original'}]])],['two',new Map([[2,{id:2,url:'https://user.example/other'}]])]]);this.sessions=new Map();this.calls=[];}
 async browsers(){return [{browserId:'one',displayName:'chrome',online:true},{browserId:'two',displayName:'edge',online:true}]}
 async command(b,a,args){this.calls.push({b,a,args});if(a==='list_tabs')return [...this.tabs.get(b).values()];if(a==='scroll')return {};if(a==='navigate'){
  let id=args.newTab?++this.next:this.sessions.get(b+args.session);if(!id)id=++this.next;this.sessions.set(b+args.session,id);const group=[...(this.sessions.get(args.session)||[])];group.push([b,id]);this.sessions.set(args.session,group);this.tabs.get(b).set(id,{id,url:args.url});
  if(this.unknown)throw Object.assign(Error('unknown'),{code:'navigation_timeout'});return {tabId:id,groupId:999};
 }if(a==='close_session'){for(const [browser,id] of this.sessions.get(args.session)||[])this.tabs.get(browser).delete(id);return {closed:1}}if(a==='close_tab'){this.tabs.get(b).delete(args.tabId);return {}}throw Error('Unexpected action '+a)}
 async evaluate(b,id){await new Promise(r=>setTimeout(r,4));const url=this.tabs.get(b).get(id).url;const u=new URL(url),search=u.hostname.includes('search.bilibili')||u.hostname==='so.csdn.net'||u.hostname.endsWith('google.com');
  if(search){const google=u.hostname.endsWith('google.com');const final=google?url.replace('www.google.com','www.google.com.hk'):url;return {url:final,title:'query results',readyState:'complete',state:{loginRequired:this.login&&b==='two'},items:[{title:'Gemini 动画教程',url:b==='one'?'https://www.bilibili.com/video/BV1234?xsec_token=private-content-signature':'https://blog.csdn.net/author/article/details/1234',snippet:'写代码生成动画',contentType:'article'}]}}
  return {url,title:'真实正文',readyState:'complete',text:'This is source evidence, including the exact author discussion of a useful code animation workflow. '.repeat(3),state:{}};
 }
}
async function fixture(t){const root=await mkdtemp(path.join(os.tmpdir(),'easybr-search-'));t.after(()=>rm(root,{recursive:true,force:true}));return path.join(root,'run')}
test('parallel browser search keeps unique evidence, read statuses, and user-owned tabs',async t=>{
 const bridge=new FakeBridge(),output=await fixture(t);const {report}=await runSearch({queries:['Gemini 动画','代码动画'],platforms:['bilibili','csdn'],browserMap:{bilibili:'one',csdn:'two'},read:2,output},{bridge});
 assert.equal(report.searches.length,4);assert.equal(report.results.length,2);assert.equal(report.results.filter(x=>x.readStatus==='read').length,2);assert.equal(new Set(report.searches.map(x=>x.evidenceFile)).size,4);
 for(const s of report.searches)assert.ok((await readFile(path.join(output,s.evidenceFile),'utf8')).includes(s.query));
 assert.equal((await stat(path.join(output,'private-run.json'))).mode&0o777,0o600);
 const publicText=await readFile(path.join(output,'results.json'),'utf8');assert.ok(!publicText.includes('private-content-signature'));assert.ok(!publicText.includes('browserId'));
 assert.deepEqual([...bridge.tabs.get('one').keys()],[1]);assert.deepEqual([...bridge.tabs.get('two').keys()],[2]);assert.equal(report.cleanup.verified,true);
});
test('a blocked platform stays blocked while another platform returns usable results',async t=>{
 const bridge=new FakeBridge({login:true});const {report}=await runSearch({queries:['动画'],platforms:['bilibili','csdn'],browserMap:{bilibili:'one',csdn:'two'},read:0,output:await fixture(t)},{bridge});
 assert.equal(report.searches.find(x=>x.platform==='csdn').status,'login_required');assert.equal(report.results.length,1);assert.equal(report.results[0].platform,'bilibili');
});
test('Google regional redirects are still the requested search, not a false failure',async t=>{
 const bridge=new FakeBridge();const {report}=await runSearch({queries:['动画'],platforms:['google'],browserMap:{google:'one'},read:0,output:await fixture(t)},{bridge});assert.equal(report.searches[0].status,'ok');assert.equal(report.results.length,1);
});
test('opaque engine result redirects are read in a fresh task tab and retained as actual source URLs',async t=>{
 const bridge=new FakeBridge();
 bridge.evaluate=async(b,id)=>{
  const url=bridge.tabs.get(b).get(id).url;
  if(url.includes('/search?'))return {url,title:'results',readyState:'complete',state:{},items:[{title:'HTML animation lesson',url:'https://www.google.com.hk/goto?url=FAKE_OPAQUE',snippet:'HTML animation'}]};
  return {url:'https://www.youtube.com/watch?v=example',title:'HTML animation lesson',readyState:'complete',state:{},contentType:'video',text:'This page is a video title and description, not a transcript or video playback. '.repeat(3)};
 };
 const {report}=await runSearch({queries:['HTML animation'],platforms:['google'],browserMap:{google:'one'},read:1,output:await fixture(t)},{bridge});
 const navigations=bridge.calls.filter(x=>x.a==='navigate');assert.equal(navigations.length,2);assert.equal(navigations[1].args.newTab,true);
 assert.equal(report.results[0].url,'https://www.youtube.com/watch?v=example');assert.equal(report.results[0].contentType,'video');assert.match(report.results[0].readCoverage,/未播放或转录/);assert.deepEqual(report.scope.platforms,['google']);
 assert.deepEqual([...bridge.tabs.get('one').keys()],[1]);
});
test('a resolved source URL remains useful even when its article body cannot be read',async t=>{
 const bridge=new FakeBridge();bridge.evaluate=async(b,id)=>{
  const url=bridge.tabs.get(b).get(id).url;
  return url.includes('/search?')?{url,title:'results',readyState:'complete',state:{},items:[{title:'A useful video tutorial',url:'https://www.google.com.hk/goto?url=FAKE_OPAQUE'}]}:{url:'https://www.youtube.com/watch?v=example',title:'A useful video tutorial',readyState:'complete',text:'',contentType:'video',state:{empty:true}};
 };
 const {report}=await runSearch({queries:['video tutorial'],platforms:['google'],browserMap:{google:'one'},read:1,output:await fixture(t)},{bridge});
 assert.equal(report.results[0].url,'https://www.youtube.com/watch?v=example');assert.equal(report.results[0].readStatus,'content_unavailable');assert.equal(report.results[0].contentType,'video');assert.equal(report.cleanup.verified,true);
});
test('an uncertain navigation still closes only its own session and reports uncertainty',async t=>{
 const bridge=new FakeBridge({unknown:true});const {report}=await runSearch({queries:['动画'],platforms:['bilibili'],browserMap:{bilibili:'one'},read:0,output:await fixture(t)},{bridge});assert.ok(bridge.calls.some(x=>x.a==='close_session'));assert.equal(report.cleanup.verified,false);assert.deepEqual([...bridge.tabs.get('one').keys()],[1]);
});

test('fast platform candidates stream before the slow platform finishes', {timeout:5000}, async t=>{
 const bridge=new FakeBridge(),original=bridge.evaluate.bind(bridge);let release;const gate=new Promise(r=>release=r);let first=false;
 bridge.evaluate=async(b,id,...rest)=>{if(b==='two'&&bridge.tabs.get(b).get(id).url.includes('so.csdn'))await gate;return original(b,id,...rest)};
 const output=await fixture(t),{report}=await runSearch({queries:['动画'],platforms:['bilibili','csdn'],browserMap:{bilibili:'one',csdn:'two'},limit:1,read:0,output},{bridge,onProgress:event=>{if(event.stage==='results'&&event.platform==='bilibili'){first=true;assert.equal(event.items.length,1);assert.ok(!JSON.stringify(event).includes('private-content-signature'));release()}}});
 assert.equal(first,true);assert.equal(report.searches.length,2);assert.ok(report.timings.firstResultsMs<=report.timings.searchWallMs+report.timings.inventoryMs+500);
 const events=(await readFile(path.join(output,'events.ndjson'),'utf8')).trim().split('\n').map(JSON.parse);assert.ok(events.some(e=>e.stage==='results'));assert.equal(JSON.parse(await readFile(path.join(output,'partial-results.json'),'utf8')).status,'completed');
});
test('detail reads overlap across browsers while retaining per-browser task isolation',{timeout:5000},async t=>{
 const bridge=new FakeBridge(),original=bridge.evaluate.bind(bridge);let release;const gate=new Promise(r=>release=r),starts=[];
 bridge.evaluate=async(b,id,...rest)=>{const url=bridge.tabs.get(b).get(id).url;if(!url.includes('search')&&!url.includes('so.csdn'))await gate;return original(b,id,...rest)};
 const {report}=await runSearch({queries:['动画'],platforms:['bilibili','csdn'],browserMap:{bilibili:'one',csdn:'two'},limit:1,read:2,output:await fixture(t)},{bridge,onProgress:e=>{if(e.stage==='read'){starts.push(e.platform);if(starts.length===2)release()}}});
 assert.equal(starts.length,2);assert.equal(report.reads.filter(r=>r.status==='read').length,2);assert.equal(report.execution.readConcurrency,2);assert.equal(report.cleanup.verified,true);
});
test('selected source reading reuses private navigation without re-running search, then can reuse evidence offline',async t=>{
 const {runRead}=await import('../scripts/read.mjs'),bridge=new FakeBridge(),initial=await fixture(t);
 const first=await runSearch({queries:['动画'],platforms:['bilibili'],browserMap:{bilibili:'one'},limit:1,read:0,output:initial},{bridge});
 const reader=new FakeBridge(),readOutput=path.join(path.dirname(initial),'read'),id=first.report.results[0].id;
 const second=await runRead({from:initial,ids:[id],output:readOutput},{bridge:reader});
 assert.equal(second.report.results[0].readStatus,'read');assert.equal(second.report.searches.length,0);
 const navigations=reader.calls.filter(c=>c.a==='navigate');assert.equal(navigations.length,1);assert.ok(navigations[0].args.url.includes('private-content-signature'));
 assert.ok(!(await readFile(path.join(readOutput,'results.json'),'utf8')).includes('private-content-signature'));
 const offline={browsers(){throw Error('must not connect')}};
 const reused=await runRead({from:readOutput,ids:[id],output:path.join(path.dirname(initial),'reused')},{bridge:offline});
 assert.equal(reused.report.execution.evidenceReused,1);assert.equal(reused.report.execution.browserCount,0);assert.equal(reused.report.results[0].evidenceReuse.kind,'same_run_evidence');
});
test('read rejects unsafe URLs and unknown IDs before opening a page',async t=>{
 const {runRead}=await import('../scripts/read.mjs');await assert.rejects(runRead({urls:['http://127.0.0.1:17777/']}),/unsafe_navigation_url/);
 const first=await runSearch({queries:['动画'],platforms:['bilibili'],browserMap:{bilibili:'one'},limit:1,read:0,output:await fixture(t)},{bridge:new FakeBridge()});
 await assert.rejects(runRead({from:first.output,ids:['00000000000000'],output:first.output+'-read'}),/unknown_source_id/);
});

test('cached evidence identity and content hashes must match before reuse',async t=>{
 const {runRead}=await import('../scripts/read.mjs');const output=await fixture(t);
 const first=await runSearch({queries:['动画'],platforms:['bilibili'],browserMap:{bilibili:'one'},limit:1,read:1,output},{bridge:new FakeBridge()});
 const item=first.report.results[0],file=path.join(output,item.contentFile),source=JSON.parse(await readFile(file,'utf8'));
 const {writeFile}=await import('node:fs/promises');await writeFile(file,JSON.stringify({...source,text:source.text+'tampered'}));
 await assert.rejects(runRead({from:output,ids:[item.id],output:output+'-reuse'}),/source_evidence_hash_mismatch/);
 await writeFile(file,JSON.stringify({...source,id:'other-source'}));
 await assert.rejects(runRead({from:output,ids:[item.id],output:output+'-reuse'}),/source_evidence_identity_mismatch/);
});

test('evidence-only reuse preserves its original browser route for a later explicit refresh',async t=>{
 const {runRead}=await import('../scripts/read.mjs'),root=await fixture(t);
 const initial=await runSearch({queries:['动画'],platforms:['bilibili'],browserMap:{bilibili:'one'},limit:1,read:1,output:root},{bridge:new FakeBridge()});
 const id=initial.report.results[0].id,reusedOutput=path.join(path.dirname(root),'reused');
 await runRead({from:root,ids:[id],output:reusedOutput},{bridge:{browsers(){throw Error('offline cache must not connect')}}});
 const journal=JSON.parse(await readFile(path.join(reusedOutput,'private-run.json'),'utf8'));assert.equal(journal.routes[0].browserId,'one');assert.deepEqual(journal.navigation,[]);
 const refreshBridge=new FakeBridge();refreshBridge.browsers=async()=>[{browserId:'two',displayName:'chrome',online:true}];
 const unavailable=await runRead({from:reusedOutput,ids:[id],refresh:true,output:path.join(path.dirname(root),'refreshed')},{bridge:refreshBridge});assert.equal(unavailable.report.results[0].readStatus,'route_unavailable');assert.equal(unavailable.report.results[0].readError,'configured_browser_not_unique_or_online');
 assert.ok(!refreshBridge.calls.some(c=>c.a==='navigate'));
});

test('malformed imported source IDs cannot escape the output directory',async t=>{
 const {runRead}=await import('../scripts/read.mjs'),{writeFile}=await import('node:fs/promises'),root=await fixture(t),base=path.dirname(root);
 await writeFile(path.join(base,'victim.json'),'original');const file=path.join(base,'malformed.json');
 await writeFile(file,JSON.stringify({schemaVersion:1,results:[{id:'../../victim',platform:'bilibili',url:'https://www.bilibili.com/video/BV1234',readStatus:'read',contentFile:'does-not-matter.json'}]}));
 await assert.rejects(runRead({from:file,ids:['../../victim'],output:root}),/invalid_source_id/);assert.equal(await readFile(path.join(base,'victim.json'),'utf8'),'original');
});
test('a failed progress consumer drains active workers before cleanup and rejection',{timeout:5000},async t=>{
 const bridge=new FakeBridge(),original=bridge.evaluate.bind(bridge);let releaseSlow,signalFailure;const slow=new Promise(r=>releaseSlow=r),failure=new Promise(r=>signalFailure=r);
 bridge.evaluate=async(b,id,...args)=>{if(b==='two')await slow;return original(b,id,...args)};
 let settled=false;
 const running=runSearch({queries:['动画'],platforms:['bilibili','csdn'],browserMap:{bilibili:'one',csdn:'two'},limit:1,read:0,output:await fixture(t)},{bridge,onProgress:e=>{if(e.stage==='searched'&&e.platform==='bilibili'){signalFailure();throw Object.assign(Error('consumer failed'),{code:'consumer_failed'})}}});
 const observed=running.then(()=>{settled=true;return null},e=>{settled=true;return e});
 await failure;await new Promise(r=>setImmediate(r));assert.equal(settled,false);releaseSlow();const error=await observed;assert.equal(error.code,'consumer_failed');
 assert.deepEqual([...bridge.tabs.get('one').keys()],[1]);assert.deepEqual([...bridge.tabs.get('two').keys()],[2]);
});

test('one unavailable configured platform does not stop other authorized platforms',async t=>{
 const bridge=new FakeBridge();const {report}=await runSearch({queries:['动画'],platforms:['bilibili','csdn'],browserMap:{bilibili:'offline-account',csdn:'two'},limit:1,read:0,output:await fixture(t)},{bridge});
 assert.equal(report.searches.find(s=>s.platform==='bilibili').errorPhase,'route');assert.equal(report.searches.find(s=>s.platform==='csdn').status,'ok');assert.equal(report.results.length,1);assert.equal(report.outcome,'partial');assert.ok(bridge.calls.filter(c=>c.a==='navigate').every(c=>c.b==='two'));
});
test('same-path functional query changes cannot be attributed to the requested article',async t=>{
 const {runRead}=await import('../scripts/read.mjs'),bridge=new FakeBridge();bridge.evaluate=async()=>({url:'https://example.com/article?article=two',title:'Different article',readyState:'complete',text:'This is a different document and must not be saved under the requested article source. '.repeat(3),state:{empty:true}});
 const {report}=await runRead({urls:['https://example.com/article?article=one'],timeoutMs:2000,output:await fixture(t)},{bridge});assert.notEqual(report.results[0].readStatus,'read');assert.equal(report.results[0].contentFile,undefined);assert.equal(report.outcome,'no_content');
});

test('unlinked search cards remain distinct, never become fabricated content URLs, and do not trigger automatic reads',async t=>{
 const bridge=new FakeBridge();bridge.evaluate=async(b,id)=>{const url=bridge.tabs.get(b).get(id).url;return {url,title:'search cards',readyState:'complete',state:{},items:[{title:'Manim 数学动画教程一',url,linkStatus:'search_page_only',domContentId:'7662444976264989993',contentType:'search-card'},{title:'Manim 数学动画教程二',url,linkStatus:'search_page_only',domContentId:'7662444976264989994',contentType:'search-card'}]}};
 const output=await fixture(t),first=await runSearch({queries:['Manim'],platforms:['douyin'],browserMap:{douyin:'one'},limit:2,read:3,output},{bridge});
 assert.equal(first.report.searches[0].status,'titles_only');assert.equal(first.report.results.length,2);assert.notEqual(first.report.results[0].id,first.report.results[1].id);assert.equal(bridge.calls.filter(c=>c.a==='navigate').length,1);
 for(const item of first.report.results){assert.equal(item.contentURL,null);assert.equal(item.linkStatus,'search_page_only');assert.equal(item.readStatus,'link_unavailable');assert.ok(!item.url.includes('modal_id'));}
 const {runRead}=await import('../scripts/read.mjs');const read=await runRead({from:output,ids:[first.report.results[0].id],output:path.join(path.dirname(output),'no-detail')},{bridge:{browsers(){throw Error('must not connect')}}});
 assert.equal(read.report.outcome,'no_content');assert.equal(read.report.execution.browserCount,0);assert.equal(read.report.execution.evidenceReused,0);assert.equal(read.report.attention[0].status,'link_unavailable');
});
test('failed platform handoffs are actionable and exclude private browser routes',async t=>{
 const {report,output}=await runSearch({queries:['动画'],platforms:['bilibili','csdn'],browserMap:{bilibili:'one',csdn:'two'},limit:1,read:0,output:await fixture(t)},{bridge:new FakeBridge({login:true})});
 assert.equal(report.attention.length,1);assert.equal(report.attention[0].status,'login_required');assert.equal(report.attention[0].required,true);assert.ok(report.attention[0].url.includes('so.csdn.net'));
 const handoff=await readFile(path.join(output,'handoff.json'),'utf8');assert.ok(!handoff.includes('browserId'));assert.equal(JSON.parse(handoff).required,true);
});

test('only passive-tab restoration is allowed and cannot focus the browser window',async()=>{
 let request;const bridge=new Bridge({token:'private-test-token',fetchImpl:async(url,options)=>{request=JSON.parse(options.body);return new Response(JSON.stringify({ok:true,result:{restored:true}}))}});
 await assert.rejects(bridge.command('browser','activate_tab',{tabId:1,focus:true,restoreSelection:true}),/action_not_readonly_search/);
 await assert.rejects(bridge.command('browser','activate_tab',{tabId:1,focus:false}),/action_not_readonly_search/);
 await bridge.command('browser','activate_tab',{tabId:1,focus:false,restoreSelection:true});assert.deepEqual(request.args,{tabId:1,focus:false});
 await assert.rejects(bridge.command('browser','click',{tabId:1,selector:'.card',focus:true}),/action_not_readonly_search/);
});

test('a thumbnail duration is not returned as an article headline',async()=>{
 const {normalizeItem}=await import('../scripts/results.mjs');assert.equal(normalizeItem({url:'https://example.com/video',title:'07:16'},{platform:'baidu',query:'AI动画'}),null);
});
