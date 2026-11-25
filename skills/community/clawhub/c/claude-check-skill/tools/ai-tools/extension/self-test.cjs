const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync(__dirname + '/check.js','utf8');
const uuid = '11111111-1111-1111-1111-111111111111';
async function run(replies, origin='https://claude.ai') {
  const calls=[];
  const context={location:{origin},AbortController,setTimeout,clearTimeout,TypeError,
    fetch:async (url,options)=>{
      calls.push(url);
      assert.equal(options.method,'GET'); assert.equal(options.credentials,'same-origin');
      assert.equal(options.redirect,'error'); assert.ok(url.startsWith('https://claude.ai/api/organizations'));
      const r=replies.shift();
      if (r instanceof Error) throw r;
      return {ok:!r.http,status:r.http||200,json:async()=>{if(r.invalid)throw new SyntaxError();return r.body;}};
    }};
  vm.createContext(context);
  const result=await vm.runInContext(source+';checkKyc()',context);
  return {result,calls};
}
(async()=>{
  let x=await run([], 'https://example.com'); assert.equal(x.calls.length,0);assert.match(x.result.error,/claude.ai/);
  x=await run([{body:[]}]);assert.match(x.result.error,/没有返回/);
  x=await run([{body:Array(11).fill({uuid})}]);assert.match(x.result.error,/超过 10/);assert.equal(x.calls.length,1);
  x=await run([{body:{error:'bad'}}]);assert.match(x.result.error,/预期为数组/);
  for(const http of [401,403,404,429,500]){x=await run([{http}]);assert.match(x.result.error,new RegExp(String(http)));}
  x=await run([{invalid:true}]);assert.match(x.result.error,/JSON/);
  x=await run([new TypeError('failed')]);assert.match(x.result.error,/网络/);
  x=await run([{body:[{name:'A',uuid},{name:'B',uuid},{name:'C',uuid}]},{body:{status:'not_required'}},{http:403},{body:{status:'new_value'}}]);
  assert.equal(x.result.rows.length,3);assert.equal(x.result.rows[0].status,'not_required');assert.match(x.result.rows[1].error,/403/);assert.equal(x.result.rows[2].status,'new_value');
  x=await run([{body:[null,{uuid:'../../bad'}]}]);assert.equal(x.calls.length,1);assert.ok(x.result.rows.every(r=>r.error));
  for(const body of [null,{}, {status:''}, {status:123}]){x=await run([{body:[{uuid}]},{body}]);assert.match(x.result.rows[0].error,/status/);}
  console.log('PASS: host restriction, HTTP errors, network error, invalid JSON, empty/invalid organizations, UUID validation, partial failures, unknown/missing status');
})().catch(e=>{console.error(e);process.exitCode=1;});
