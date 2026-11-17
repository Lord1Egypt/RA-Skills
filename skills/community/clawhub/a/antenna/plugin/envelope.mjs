import {verify,createPublicKey} from 'node:crypto';
export class Refusal extends Error {
 constructor(code,status,reason){super(reason);this.code=code;this.result={status,reason};}
}
const reject=(reason='malformed',code=400)=>{throw new Refusal(code,'rejected',reason);};
const caps={protocol:32,from:64,to:64,timestamp:32,message_id:36,target_session:128,user:64,reply_to:256,reply_session:128,subject:200,signature:128};
const required=['protocol','from','to','timestamp','message_id','target_session','signature'];
const order=['protocol','from','to','timestamp','message_id','target_session','user','reply_to','reply_session','subject','body'];
export function canonical(fields){return Buffer.concat(order.map(name=>{const value=Buffer.from(fields[name]??'','utf8');return Buffer.concat([Buffer.from(`${name}:${value.length}:`),value,Buffer.from('\n')]);}));}
export function parse(raw,maxBodyChars){
 if(raw.length>4*maxBodyChars+4096)reject('too_large',413);
 let text;try{text=new TextDecoder('utf-8',{fatal:true,ignoreBOM:true}).decode(raw);}catch{reject();}
 if(/[\r\0]/u.test(text))reject();
 if(text.endsWith('\n'))text=text.slice(0,-1);
 const opening='[ANTENNA_RELAY]',closing='[/ANTENNA_RELAY]';
 if(!text.startsWith(opening+'\n')||!text.endsWith('\n'+closing)||text.split(opening).length!==2||text.split(closing).length!==2)reject();
 const inner=text.slice(opening.length+1,-closing.length-1),split=inner.indexOf('\n\n');
 if(split<0)reject();
 const fields=Object.create(null);
 for(const line of inner.slice(0,split).split('\n')){
  const at=line.indexOf(': ');if(at<1)reject();
  const name=line.slice(0,at),value=line.slice(at+2);
  if(!Object.hasOwn(caps,name)||Object.hasOwn(fields,name)||!value||value!==value.trim()||/\p{C}/u.test(value)||Buffer.byteLength(value)>caps[name])reject();
  fields[name]=value;
 }
 if(required.some(k=>!Object.hasOwn(fields,k)))reject();
 if(fields.protocol!=='antenna-ed25519-v2')throw new Refusal(422,'unsupported','protocol');
 if(!/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/.test(fields.message_id))reject();
 const t=fields.timestamp;
 if(!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:[0-5]\dZ$/.test(t)||!Number.isFinite(Date.parse(t))||new Date(t).toISOString()!==t.slice(0,-1)+'.000Z')reject();
 if(!/^ed25519-v1:[A-Za-z0-9+/]{86}==$/.test(fields.signature))reject();
 const sig=Buffer.from(fields.signature.slice(11),'base64');
 if(sig.length!==64||sig.toString('base64')!==fields.signature.slice(11))reject();
 fields.body=inner.slice(split+2);
 if([...fields.body].length>maxBodyChars)reject('too_large',413);
 return fields;
}
export function authenticate(fields,config,now=Date.now()){
 const peer=Object.hasOwn(config.peers,fields.from)?config.peers[fields.from]:null;
 if(!peer)reject('unauthenticated',401);
 let key;try{key=createPublicKey(peer.publicKey);}catch{throw new Refusal(503,'unavailable','runtime_unavailable');}
 if(key.asymmetricKeyType!=='ed25519'||!verify(null,canonical(fields),key,Buffer.from(fields.signature.slice(11),'base64')))reject('unauthenticated',401);
 const age=now-Date.parse(fields.timestamp);
 if(age>300000||age< -60000)reject('not_permitted',403);
 if(fields.to!==config.receiver||!peer.destinations.includes(fields.target_session)||!Object.hasOwn(config.destinations,fields.target_session))reject('not_permitted',403);
 return config.destinations[fields.target_session];
}
