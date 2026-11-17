#!/usr/bin/env node
import {LIMITS} from './limits.mjs';
import fs from 'node:fs';
import path from 'node:path';
import {snapshot,replaceJSON} from './config-write.mjs';
import {validateConfig,modes} from './policy.mjs';
import {resolveScanner,gatewayScan} from './smart.mjs';
import {loadRuleset} from './ruleset.mjs';
import {Inbox} from './inbox.mjs';
const args=process.argv.slice(2),configPath=args.shift(),command=args.shift();
const help='Usage: antenna-plugin <openclaw.json> status|init <policy.json>|mode <off|dumb|smart|both> [peer]|check <registered-model-or-alias>|select <registered-model-or-alias>|rules validate|select <absolute-file>|inbox list|show|release|discard|approve-ordinary [id] [acknowledgements JSON]';
try{
 if(!configPath||!command)throw Error(help);
 if(['mcs','migrate'].includes(command))throw Error(command==='mcs'?'Diagnostics kit not bundled. See OPTIONAL-KITS.md; run its standalone CLI with this host path. Nothing downloaded or run.':'Migration is a separate version-matched app; see OPTIONAL-KITS.md. No files changed.');
 const original=snapshot(configPath),host=original.value;
 const entry=host.plugins?.entries?.antenna;
 let c=entry?.config;
 function save(next){
  const validated=validateConfig(next,{requireReady:true,host});
  const copy=structuredClone(host);copy.plugins??={};copy.plugins.entries??={};
  copy.plugins.entries.antenna={...(copy.plugins.entries.antenna??{enabled:false}),config:validated};
  console.log(JSON.stringify(replaceJSON(original,copy)));

 }
 if(command==='init'){
  if(entry)throw Error('Antenna entry exists; use mode/select or explicit migration');
  save(JSON.parse(fs.readFileSync(args[0],'utf8')));
 }else{
  c=validateConfig(c);
  if(command==='status'){
   let p;try{p=resolveScanner(c.scannerModel,host);}catch{}
   const items=new Inbox(c.inboxFile,{readOnly:true}).read().items;
   const stateCounts=Object.fromEntries(['scanning','held','dispatching','submitted','unknown','discarded'].map(state=>[state,items.filter(r=>r.state===state).length]));
   console.log(JSON.stringify({stateCounts,limits:LIMITS,maxActiveSmart:c.maxActiveSmart,schemaVersion:2,mcs:c.mcs,inbox:c.inbox,peers:Object.fromEntries(Object.entries(c.peers).map(([k,v])=>[k,{configured:v.mcs??'default',effective:!v.mcs||v.mcs==='default'?c.mcs:v.mcs}])),scanner:p?{model:p.model,modelId:p.modelId,ready:p.identity===c.scannerIdentity}:null,ruleset:{file:c.rulesetFile??'bundled',hash:loadRuleset(c.rulesetFile).hash}}));
  }else if(command==='mode'){
   const [mode,peer]=args;
   if(!modes.includes(mode)&&!(peer&&mode==='default'))throw Error('invalid mode');
   if(peer){if(!Object.hasOwn(c.peers,peer))throw Error('unknown peer');c.peers[peer].mcs=mode;}else c.mcs=mode;
   save(c);
  }else if(command==='rules'){
   const [action,file]=args;if(!['validate','select'].includes(action)||!file)throw Error('rules validate|select /absolute/file.json');
   const rules=loadRuleset(file);
   if(action==='select'){c.rulesetFile=file;save(c);}else console.log(JSON.stringify({valid:true,rules:rules.rules.length,hash:rules.hash,qualityAccepted:false}));
  }else if(command==='check'||command==='select'){
   const p=resolveScanner(args[0],host);
   const result=await gatewayScan(host,p,'Please review tomorrow’s meeting agenda.');
   if(result.verdict!=='pass')throw Error('scanner compatibility check failed: '+(result.reason??result.verdict));
   if(command==='select'){delete c.scannerProfile;c.scannerModel=p.model;c.scannerIdentity=p.identity;save(c);}
   else console.log(JSON.stringify({compatible:true,model:p.modelId,qualityAccepted:false,activated:false}));
  }else if(command==='inbox'){
   const [action,id,ack='[]']=args,inbox=new Inbox(c.inboxFile);
   if(action==='list')console.log(JSON.stringify(inbox.read().items.map(r=>({id:r.id,state:r.state,reasons:r.reasons}))));
   else if(action==='show')console.log(JSON.stringify(inbox.get(id))); // JSON escaping keeps controls inert.
   else if(action==='discard')console.log(JSON.stringify({state:inbox.discard(id).state}));
   else{
    // Do not recover state in a second operator process while the gateway scans.
    const {makeFlow}=await import('./runtime.mjs'),flow=makeFlow(c,host);
    let result;
    if(action==='release')result=await flow.release(id,JSON.parse(ack));
    else if(action==='approve-ordinary')result=await flow.approveOrdinary();
    else throw Error('unknown inbox action');
    console.log(JSON.stringify(result));
   }
  }else throw Error(help);
 }
}catch(e){console.error(JSON.stringify({status:'error',reason:e instanceof SyntaxError?'invalid JSON input':e.message}));process.exitCode=1;}
