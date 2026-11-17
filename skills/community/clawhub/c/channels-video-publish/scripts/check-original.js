#!/usr/bin/env node
/**
 * 核查视频号已发布内容的「原创声明」状态
 *
 * 原理：打开 /platform/post/list，用 Network 域捕获页面自己发出的
 *   micro/content/cgi-bin/mmfinderassistant-bin/post/post_list 请求，
 *   然后把 pageSize 改成 100 重放一次，读 originalInfo.isDeclared。
 *
 * 用法: node check-original.js [--all]
 *   --all  输出全部条目（默认只输出未声明原创的）
 *
 * 重要事实：已发布条目**不能补声明原创**（发布后没有该入口）；
 *   超过 6 个月的条目连「修改并重新发表」都没有，只能删旧重发。
 */
const WebSocket = require('ws');
const http = require('http');
function getJSON(p){return new Promise((res,rej)=>{http.get({host:'127.0.0.1',port:9222,path:p,headers:{Host:'127.0.0.1:9222'}},r=>{let d='';r.on('data',c=>d+=c);r.on('end',()=>res(JSON.parse(d)));}).on('error',rej);});}
const sleep = ms => new Promise(r => setTimeout(r, ms));
const SHOW_ALL = process.argv.includes('--all');

(async () => {
  const ver = await getJSON('/json/version');
  const ws = new WebSocket(ver.webSocketDebuggerUrl);
  let id = 1; const pending = new Map(); let ps = null; const reqs = [];
  const send = (s, m, p) => new Promise((res, rej) => {
    const i = id++; pending.set(i, { res, rej });
    const msg = { id: i, method: m, params: p || {} }; if (s) msg.sessionId = s;
    ws.send(JSON.stringify(msg));
    setTimeout(() => { if (pending.has(i)) { pending.delete(i); rej(new Error('timeout ' + m)); } }, 30000);
  });
  ws.on('message', m => {
    const o = JSON.parse(m);
    if (o.id && pending.has(o.id)) { const p = pending.get(o.id); pending.delete(o.id); if (o.error) p.rej(new Error(o.error.message)); else p.res(o.result); return; }
    if (o.method && o.sessionId === ps && o.method === 'Network.requestWillBeSent' && /post_list/.test((o.params.request || {}).url || ''))
      reqs.push({ url: o.params.request.url, method: o.params.request.method, postData: o.params.request.postData || '' });
  });
  await new Promise(r => ws.on('open', r));
  const cr = await send(null, 'Target.createTarget', { url: 'https://channels.weixin.qq.com/platform/post/list' });
  const at = await send(null, 'Target.attachToTarget', { targetId: cr.targetId, flatten: true });
  ps = at.sessionId;
  await send(null, 'Target.activateTarget', { targetId: cr.targetId }).catch(() => {});
  await send(ps, 'Page.enable'); await send(ps, 'Runtime.enable'); await send(ps, 'Network.enable');
  await sleep(11000);
  const cand = reqs[0];
  if (!cand) { console.error('未捕获到 post_list 请求'); ws.close(); process.exit(1); }
  const body = (cand.postData || '')
    .replace(/("pageSize"\s*:\s*)\d+/g, '$1100')
    .replace(/pageSize=(\d+)/g, 'pageSize=100');
  const expr = `(function(){
    return fetch(${JSON.stringify(cand.url)},{method:${JSON.stringify(cand.method)},headers:{'Content-Type':'application/json'},body:${cand.method === 'POST' ? JSON.stringify(body) : 'undefined'},credentials:'include'})
      .then(r=>r.text()).then(function(t){
        var j=JSON.parse(t); var list=(j.data&&j.data.list)||[];
        function strings(o,out,depth){ if(depth>5||!o)return;
          if(typeof o==='string'){ if(/[\\u4e00-\\u9fa5]/.test(o)&&o.length>=2) out.push(o.slice(0,70)); return;}
          if(Array.isArray(o)){o.forEach(function(x){strings(x,out,depth+1);});return;}
          if(typeof o==='object'){Object.keys(o).forEach(function(k){strings(o[k],out,depth+1);});}}
        var rows=list.map(function(it){
          var ss=[]; strings(it,ss,0);
          var seen={},uniq=[]; ss.forEach(function(s){if(!seen[s]){seen[s]=1;uniq.push(s);}});
          uniq.sort(function(a,b){return b.length-a.length;});
          return {declared:(it.originalInfo||{}).isDeclared,
                  date:it.createTime?new Date(it.createTime*1000).toISOString().slice(0,10):'',
                  read:it.readCount, like:it.likeCount,
                  id:(it.objectId||'').slice(-12),
                  top:uniq.slice(0,4)};
        });
        return JSON.stringify({total:list.length,
          undeclared:rows.filter(function(x){return x.declared===0;}).length,
          rows: rows},null,1);
      });})()`;
  const r = await send(ps, 'Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true });
  if (r.exceptionDetails) { console.error('ERR', JSON.stringify(r.exceptionDetails).slice(0, 400)); ws.close(); process.exit(1); }
  const data = JSON.parse(r.result.value);
  console.log(`总条目 ${data.total}｜未声明原创 ${data.undeclared}`);
  const show = SHOW_ALL ? data.rows : data.rows.filter(x => x.declared === 0);
  show.forEach(x => {
    console.log(`\n${x.declared === 0 ? '❌' : '✅'} ${x.date}  播放${x.read} 赞${x.like}  id=${x.id}`);
    x.top.forEach(t => console.log('   · ' + t.replace(/\n/g, ' ').slice(0, 60)));
  });
  ws.close(); process.exit(0);
})().catch(e => { console.error('FATAL', e.stack); process.exit(1); });
