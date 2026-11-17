import http from 'node:http';
import https from 'node:https';
import {sign,randomUUID,createPrivateKey} from 'node:crypto';
import {canonical,parse} from './envelope.mjs';
export const PROFILE='antenna-plugin-v2';
export function endpoint(value,allowHttp=false){
 const u=new URL(value);
 if(u.username||u.password||u.search||u.hash||!/^\/(?:[A-Za-z0-9_-]+\/)*[A-Za-z0-9_-]*$/.test(u.pathname)||!(u.protocol==='https:'||(allowHttp&&u.protocol==='http:')))throw Error('explicit HTTPS origin required (HTTP requires opt-in)');
 return u.origin+u.pathname.replace(/\/$/,'')+'/antenna/v1/receive';
}
export function buildMessage({from,to,target,body,privateKey,subject,replyTo,replySession,user}){
 const key=createPrivateKey(privateKey);if(key.asymmetricKeyType!=='ed25519')throw Error('Ed25519 identity required');
 const fields={protocol:'antenna-ed25519-v2',from,to,timestamp:new Date().toISOString().replace(/\.\d{3}Z$/,'Z'),message_id:randomUUID(),target_session:target};
 for(const [k,v] of Object.entries({subject,reply_to:replyTo,reply_session:replySession,user}))if(v!==undefined&&v!=='')fields[k]=v;
 fields.body=body;fields.signature='ed25519-v1:'+sign(null,canonical(fields),key).toString('base64');
 const wire='[ANTENNA_RELAY]\n'+Object.entries(fields).filter(([k])=>k!=='body').map(([k,v])=>`${k}: ${v}`).join('\n')+'\n\n'+body+'\n[/ANTENNA_RELAY]';
 parse(Buffer.from(wire),1000000); // Same validation as receive; never rewrite body.
 return wire;
}
export function sendEnvelope({origin,profile,bearer,allowHttp=false},wire,{timeoutMs=35000}={}){
 if(profile!==PROFILE)throw Error('unsupported or unmigrated target; no legacy fallback');
 const url=new URL(endpoint(origin,allowHttp));
 if(typeof bearer!=='string'||bearer.length<32||/[\r\n]/.test(bearer))throw Error('invalid Antenna bearer');
 parse(Buffer.from(wire),1000000);
 return new Promise(resolve=>{
  let settled=false;const done=result=>{if(settled)return;settled=true;clearTimeout(timer);resolve(result);};
  const req=(url.protocol==='https:'?https:http).request(url,{method:'POST',headers:{'Content-Type':'text/plain; charset=utf-8','Content-Length':Buffer.byteLength(wire),Authorization:`Bearer ${bearer}`}},res=>{
   let size=0;const parts=[];
   res.on('data',b=>{size+=b.length;if(size>65536){res.destroy();done({status:'unknown',reason:'invalid_confirmation'});}else parts.push(b);});
   res.on('end',()=>{
    try{
     const r=JSON.parse(Buffer.concat(parts).toString('utf8'));
     const valid=res.statusCode===202&&['held','submitted'].includes(r.status)||res.statusCode===504&&r.status==='unknown'||res.statusCode>=400&&res.statusCode<500&&['rejected','unsupported'].includes(r.status)||res.statusCode===503&&r.status==='unavailable';
     if(!valid)throw Error();
     // Remote explanations are not trusted output; retain only bounded status metadata.
     const out={status:r.status,httpCode:res.statusCode};
     if(typeof r.id==='string'&&/^[0-9a-f-]{36}$/.test(r.id))out.id=r.id;
     if(Number.isSafeInteger(r.accepted)&&r.accepted>=0&&Number.isSafeInteger(r.failed)&&r.failed>=0)out.response={accepted:r.accepted,failed:r.failed};
     done(out);
    }catch{done({status:'unknown',reason:'invalid_confirmation',httpCode:res.statusCode});}
   });
   res.on('error',()=>done({status:'unknown',reason:'confirmation_unavailable'}));
  });
  const timer=setTimeout(()=>{req.destroy();done({status:'unknown',reason:'confirmation_unavailable'});},timeoutMs);
  req.on('error',()=>done({status:'unknown',reason:'confirmation_unavailable'}));req.end(wire);
 });
}
