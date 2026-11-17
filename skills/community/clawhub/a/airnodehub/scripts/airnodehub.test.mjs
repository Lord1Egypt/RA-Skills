import test from 'node:test';
import assert from 'node:assert/strict';
import { generatePrivateKey, privateKeyToAccount } from 'viem/accounts';
import { encodePacked, keccak256, toHex } from 'viem';
import { callFree, deriveRequestHash, inspectAirnode, isPublicAddress, safeFetch, resolveIntent } from './airnodehub.mjs';

const account = privateKeyToAccount(generatePrivateKey());
const url = 'https://airnode-example.fly.dev/';
const input = { airnodeUrl:url, expectedAddress:account.address, operation:'quote', parameters:{base:'EUR'} };
const variant = {properties:{operation:{const:'quote'},parameters:{properties:{base:{type:'string'}},required:['base']}}};
const document = {'x-airnode':{address:account.address},paths:{}};
document.paths['/'] = {post:{requestBody:{content:{'application/json':{schema:{oneOf:[variant]}}}}}};
function transport({alter = x => x, price, status = 200} = {}) {
  const calls=[];
  const fetcher=async (endpoint, init={}) => {
    calls.push([String(endpoint),init]);
    if (String(endpoint).endsWith('/llms.txt')) return {ok:true,text:async()=>'- [Example]('+url+'): test'};
    if (!init.method) {
      const doc=structuredClone(document);
      if(price !== undefined) doc['x-airnode'].payment={prices:{quote:price}};
      return {ok:true,json:async()=>doc};
    }
    if(status!==200) return {ok:false,status};
    const req=JSON.parse(init.body);
    const body={airnode:account.address,requestHash:deriveRequestHash(req.operation,req.parameters,req.responseProjection),timestamp:'1780000000',data:{price:1.2}};
    body.signature=await account.signMessage({message:{raw:keccak256(encodePacked(['bytes32','uint256','bytes'],[body.requestHash,BigInt(body.timestamp),toHex(JSON.stringify(body.data))]))}});
    return {ok:true,json:async()=>alter(body)};
  };
  return {fetcher,calls};
}
test('free call verifies a real ephemeral signature',async()=>assert.equal((await callFree(input,transport())).state,'verified'));
test('projection is transmitted and bound',async()=>{
 const t=transport(); const projection={price:'/price'};
 const result=await callFree({...input,responseProjection:projection},t);
 assert.deepEqual(result.responseProjection,projection);
 assert.deepEqual(JSON.parse(t.calls.at(-1)[1].body).responseProjection,projection);
 assert.notEqual(result.attestation.requestHash,deriveRequestHash(input.operation,input.parameters));
});
test('tampered data is rejected',async()=>assert.rejects(callFree(input,transport({alter:b=>({...b,data:{price:100}})}))));
test('wrong request is rejected',async()=>assert.rejects(callFree(input,transport({alter:b=>({...b,requestHash:deriveRequestHash('other',{})})}))));
test('wrong projection is rejected',async()=>assert.rejects(callFree({...input,responseProjection:{x:'/x'}},transport({alter:b=>({...b,requestHash:deriveRequestHash(input.operation,input.parameters,{y:'/y'})})}))));
test('wrong listed signer stops before POST',async()=>{
 const t=transport();
 await assert.rejects(callFree({...input,expectedAddress:'0x0000000000000000000000000000000000000001'},t));
 assert.ok(!t.calls.some(([,i])=>i.method==='POST'));
});
test('priced operation stops before POST',async()=>{
 const t=transport({price:'0.01'});
 assert.equal((await callFree(input,t)).state,'needs-payment-authorisation');
 assert.ok(!t.calls.some(([,i])=>i.method==='POST'));
});
test('provider errors are not verified success',async()=>{for(const status of [402,429,500,502]) await assert.rejects(callFree(input,transport({status})),new RegExp(String(status)));});
test('malformed signature fails',async()=>assert.rejects(callFree(input,transport({alter:b=>({...b,signature:'0x12'})}))));
test('unlisted URL is never contacted',async()=>{
 const t=transport(); await assert.rejects(inspectAirnode('https://unlisted.example/',t),/absent/);
 assert.equal(t.calls.length,1);
});
test('unsafe URL components rejected before transport',async()=>{
 for(const bad of ['http://example.com/','https://example.com:444/','https://example.com/?x=1','https://example.com/#x']){
  const t=transport();await assert.rejects(inspectAirnode(bad,t));assert.equal(t.calls.length,0);
 }
});
test('private and reserved addresses rejected, public addresses accepted',()=>{
 for(const ip of ['127.0.0.1','10.0.0.1','169.254.169.254','172.16.1.1','192.168.1.1','100.64.0.1','0.0.0.0','224.0.0.1','::1','fc00::1','fe80::1','::ffff:127.0.0.1','2001:db8::1','2002:7f00:1::']) assert.equal(isPublicAddress(ip),false,ip);
 for(const ip of ['1.1.1.1','8.8.8.8','2606:4700:4700::1111']) assert.equal(isPublicAddress(ip),true,ip);
});
test('literal loopback and localhost DNS blocked at network layer',async()=>{
 await assert.rejects(safeFetch('https://127.0.0.1/'),/non-public/);
 await assert.rejects(safeFetch('https://localhost/'),/non-public/);
});
test('canonical object ordering stable; arrays preserve order',()=>{
 assert.equal(deriveRequestHash('x',{b:2,a:1}),deriveRequestHash('x',{a:1,b:2}));
 assert.notEqual(deriveRequestHash('x',{a:[1,2]}),deriveRequestHash('x',{a:[2,1]}));
});
test('resolver keeps missing inputs and optional provenance',async()=>{
 const value={intent:'x',candidates:[],unresolvedInputs:['chain'],outcome:'unsupported'};
 assert.deepEqual(await resolveIntent('x',{fetcher:async()=>({ok:true,json:async()=>value})}),value);
});
