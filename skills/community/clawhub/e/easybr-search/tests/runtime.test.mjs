import test from 'node:test';import assert from 'node:assert/strict';
import {parallelGroups,selectBrowser,hasReadableText} from '../scripts/runtime.mjs';
import {getPlatform} from '../scripts/platforms.mjs';
test('a browser lane is serial while separate browsers can overlap',async()=>{
 const active=new Set(),seen=[];let release;const gate=new Promise(r=>release=r);
 await parallelGroups([{browser:'a',id:1},{browser:'a',id:2},{browser:'b',id:3}],t=>t.browser,2,async task=>{assert.ok(!active.has(task.browser));active.add(task.browser);seen.push(task.id);if(active.size===2)release();if(task.id!==2)await gate;active.delete(task.browser)});
 assert.ok(seen.indexOf(1)<seen.indexOf(2));assert.ok(seen.includes(3));
});
test('public engines balance ordinary browsers but explicit account routing wins',()=>{
 const browsers=[{browserId:'a',displayName:'chrome',tabs:[]},{browserId:'b',displayName:'edge',tabs:[]},{browserId:'c',displayName:'专用账号',tabs:[]}],loads=new Map();
 const first=selectBrowser(getPlatform('baidu'),browsers,{},loads);loads.set(first.browser.browserId,1);
 const second=selectBrowser(getPlatform('google'),browsers,{},loads);assert.notEqual(first.browser.browserId,second.browser.browserId);assert.equal(selectBrowser(getPlatform('google'),browsers,{google:'a'},loads).browser.browserId,'a');
});
test('short text needs a verified primary content container',()=>{
 assert.equal(hasReadableText({text:'短视频的详细说明正文内容够二十个字但不到八十字',extraction:{primaryContent:true}}),true);
 assert.equal(hasReadableText({text:'菜单首页注册登录和推荐文章',extraction:{primaryContent:false}}),false);
});

test('deadline-edge extraction failures preserve the latest observed page',async()=>{
 const {boundedPage}=await import('../scripts/runtime.mjs');let calls=0;
 const bridge={async evaluate(){calls++;if(calls===1)return {url:'https://www.google.com/search?q=x',readyState:'complete',items:[],state:{}};await new Promise(r=>setTimeout(r,150));throw Object.assign(Error('expired'),{code:'bridge_command_failed'})}};
 const page=await boundedPage(bridge,'browser',1,'expression',{expectedURL:'https://www.google.com/search?q=x',timeoutMs:500});assert.equal(page.timedOut,true);assert.equal(page.url,'https://www.google.com/search?q=x');assert.ok(page.polling.polls>=1);
});
