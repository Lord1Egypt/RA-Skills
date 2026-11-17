#!/usr/bin/env node
import {operatorAuth} from './operator-auth.mjs';
import {hooksWarning} from './migration-warning.mjs';
import {resolveScanner} from './smart.mjs';
import fs from 'node:fs';
import path from 'node:path';
import {validateConfig} from './policy.mjs';
import {PROFILE} from './transport.mjs';
try{
 const [command,file,root]=process.argv.slice(2),read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
 if(command==='doctor'){
  const old=read(path.join(root,'antenna-config.json'));
  if(old.transport_profile!==PROFILE)throw Error('Legacy installation detected. Use the separate version-matched migration app described in OPTIONAL-KITS.md; old setup and policy restoration are retired. No changes made.');
  const host=read(file),peers=read(path.join(root,'antenna-peers.json'));
  const c=validateConfig(host.plugins?.entries?.antenna?.config),self=Object.values(peers).filter(p=>p.self===true);
  if(self.length!==1)throw Error('ambiguous retained identity');
  const legacyBearer=fs.readFileSync(path.resolve(root,self[0].token_file),'utf8').trim(),problems=[];
  if(old.transport_profile!==PROFILE)problems.push('legacy send/writer controls not switched');
  if(!host.plugins?.entries?.antenna?.enabled||(host.plugins?.allow?.length&&!host.plugins.allow.includes('antenna'))||host.plugins?.deny?.includes('antenna'))problems.push('plugin disabled or not allowlisted');
  const warnings=host.hooks?.enabled===false?[]:[hooksWarning];
  try{operatorAuth(host,[legacyBearer,c.bearer]);}catch{problems.push('operator credential separation not established');}
  const relay=old.relay_agent_id??'antenna';
  if(host.agents?.list?.some(a=>a.id===relay)||Object.hasOwn(host.agents?.entries??{},relay))problems.push('legacy relay agent still provisioned; review ownership before removal');
  if(host.hooks?.mappings?.some(m=>JSON.stringify(m).includes('antenna')))problems.push('possible old Antenna mapping remains; review manually');
  if([c.mcs,...Object.values(c.peers).map(p=>p.mcs)].some(m=>['smart','both'].includes(m))){try{if(resolveScanner(c.scannerModel,host).identity!==c.scannerIdentity)throw Error();}catch{problems.push('registered scanner selection not validated');}}
  console.log(JSON.stringify({staticChecksPassed:problems.length===0,liveIngressVerified:false,problems,warnings,required:'After explicit restart, verify signed plugin admission and denial of operator access using peer credentials. If hooks were rotated or disabled, also verify old hook access is denied; otherwise retained hook access is outside Antenna checks.'}));if(problems.length)process.exitCode=1;
 }else throw Error('doctor HOST COMPANION_ROOT');
}catch(e){console.error(JSON.stringify({status:'blocked',reason:e instanceof SyntaxError?'invalid JSON input':e.message}));process.exitCode=1;}
