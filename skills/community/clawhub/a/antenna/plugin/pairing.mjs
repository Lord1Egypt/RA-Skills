#!/usr/bin/env node
import {operatorAuth} from './operator-auth.mjs';
// Offline receiver-authored contact exchange. Never grants inbound/outbound permission.
import {hooksWarning} from './migration-warning.mjs';
import fs from 'node:fs';
import path from 'node:path';
import {createPublicKey,randomUUID} from 'node:crypto';
import {PROFILE,endpoint} from './transport.mjs';
const [command,rootArg,...args]=process.argv.slice(2),root=path.resolve(rootArg??'.');
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const resolve=p=>path.resolve(root,p);
const need=(v,m)=>{if(!v)throw Error(m);};
try{
 const peersFile=resolve('antenna-peers.json'),raw=fs.readFileSync(peersFile,'utf8'),peers=JSON.parse(raw);
 if(command==='export'){
  const [hostPath,output]=args,host=read(hostPath),c=host.plugins?.entries?.antenna?.config;
  const self=Object.entries(peers).filter(([,p])=>p.self===true);need(self.length===1&&self[0][0]===c?.receiver,'receiver identity mismatch');
  need(typeof c.bearer==='string'&&c.bearer.length>=32,'Antenna bearer required');
  operatorAuth(host,[c.bearer]);
  const p=self[0][1];endpoint(p.url,p.allow_http===true);
  const key=createPublicKey(fs.readFileSync(resolve(p.signing_public_key_file)));need(key.asymmetricKeyType==='ed25519','Ed25519 identity required');
  const bundle={schema_version:3,bundle_type:'antenna-plugin-contact',transport_profile:PROFILE,peer:c.receiver,origin:p.url,allow_http:p.allow_http===true,public_key:key.export({type:'spki',format:'pem'}),antenna_bearer:c.bearer,destinations:Object.keys(c.destinations),expires_at:new Date(Date.now()+86400000).toISOString()};
  fs.writeFileSync(output,JSON.stringify(bundle)+'\n',{flag:'wx',mode:0o600});
  console.log(JSON.stringify({written:true,encrypted:false,warnings:host.hooks?.enabled===false?[]:[hooksWarning],note:'Private credential-bearing contact; transfer through an authenticated encrypted channel.'}));
 }else if(command==='import'){
  const [file,expectedPeer,defaultTarget]=args,st=fs.lstatSync(file);need(st.isFile()&&!(st.mode&0o077)&&st.size<=16384,'private bounded contact file required');
  const b=read(file);
  need(b.schema_version===3&&b.bundle_type==='antenna-plugin-contact'&&b.transport_profile===PROFILE,'unsupported contact; no legacy reinterpretation');
  need(typeof expectedPeer==='string'&&/^[a-z0-9][a-z0-9._-]{0,63}$/.test(expectedPeer)&&b.peer===expectedPeer&&!peers[expectedPeer]?.self,'expected remote identity required');
  const expires=Date.parse(b.expires_at);need(Number.isFinite(expires)&&expires>Date.now()&&expires<=Date.now()+86400000,'expired or invalid contact');
  endpoint(b.origin,b.allow_http===true);
  need(typeof b.antenna_bearer==='string'&&b.antenna_bearer.length>=32&&!/[\r\n]/.test(b.antenna_bearer),'invalid Antenna bearer');
  need(Array.isArray(b.destinations)&&b.destinations.includes(defaultTarget)&&typeof defaultTarget==='string','explicit advertised destination required');
  const key=createPublicKey(b.public_key);need(key.asymmetricKeyType==='ed25519','Ed25519 pin required');
  const pem=key.export({type:'spki',format:'pem'});
  if(peers[expectedPeer]?.signing_public_key_file)need(createPublicKey(fs.readFileSync(resolve(peers[expectedPeer].signing_public_key_file))).export({type:'spki',format:'pem'})===pem,'signing pin changed; explicit re-pair required');
  // Fresh inert credential/key files first; only the final peers rename selects them.
  const lock=peersFile+'.lock';fs.mkdirSync(lock,{mode:0o700});
  try{
   need(fs.readFileSync(peersFile,'utf8')===raw,'peer configuration changed');
   const dir=resolve('secrets');fs.mkdirSync(dir,{recursive:true,mode:0o700});
   const id=randomUUID(),token=path.join(dir,`plugin-${id}.token`),pin=path.join(dir,`plugin-${id}.pem`);
   fs.writeFileSync(token,b.antenna_bearer,{flag:'wx',mode:0o600});fs.writeFileSync(pin,pem,{flag:'wx',mode:0o600});
   peers[expectedPeer]={...peers[expectedPeer],url:b.origin,allow_http:b.allow_http===true,transport_profile:PROFILE,default_target:defaultTarget,auth_mode:'ed25519-v1',token_file:token,signing_public_key_file:pin};
   const tmp=peersFile+'.'+id;fs.writeFileSync(tmp,JSON.stringify(peers,null,2)+'\n',{flag:'wx',mode:0o600});fs.renameSync(tmp,peersFile);
  }finally{fs.rmdirSync(lock);}
  console.log(JSON.stringify({imported:expectedPeer,permissions:'unchanged',inboundPluginPin:'unchanged; review separately'}));
 }else throw Error('export ROOT HOST OUTPUT | import ROOT CONTACT EXPECTED_PEER DEFAULT_TARGET');
}catch(e){console.error(JSON.stringify({status:'blocked',reason:e.message}));process.exitCode=1;}
