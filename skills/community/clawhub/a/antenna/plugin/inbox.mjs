import {LIMITS} from './limits.mjs';
import fs from 'node:fs';
import path from 'node:path';
import {createHash, randomUUID} from 'node:crypto';

export const digest = value => createHash('sha256').update(value).digest('hex');
export const reasons = Object.freeze({approval:'Awaiting approval', flagged:'MCS flagged', incomplete:'Scan incomplete'});
const states = new Set(['scanning','held','dispatching','submitted','unknown','discarded']);
export class InboxError extends Error {}

// Prototype schema deliberately cannot be consumed as the legacy array queue.
// One file holds one payload per item; no receipt store or automatic drain.
export class Inbox {
 constructor(file, {maxItems=LIMITS.inboxItems,maxBytes=LIMITS.inboxBytes,pendingLimit=LIMITS.pending,readOnly=false}={}) {
  if(!Number.isInteger(maxItems)||maxItems<1||maxItems>LIMITS.inboxItems||!Number.isInteger(maxBytes)||maxBytes<1||maxBytes>LIMITS.inboxBytes||!Number.isInteger(pendingLimit)||pendingLimit<1||pendingLimit>LIMITS.pending)throw new InboxError('invalid inbox limits');
  this.file=file; this.maxItems=maxItems; this.maxBytes=maxBytes;this.pendingLimit=pendingLimit;this.readOnly=readOnly;
  if(!readOnly)fs.mkdirSync(path.dirname(file),{recursive:true,mode:0o700});
 }
 read() {
  if(!fs.existsSync(this.file))return {schema:2,items:[]};
  const stat=fs.lstatSync(this.file);
  if(!stat.isFile()||stat.size>this.maxBytes)throw new InboxError('invalid inbox');
  const db=JSON.parse(fs.readFileSync(this.file,'utf8'));
  if(db.schema!==2||!Array.isArray(db.items)||db.items.length>this.maxItems)throw new InboxError('invalid inbox');
  const ids=new Set();
  for(const r of db.items){
   if(typeof r.id!=='string'||ids.has(r.id)||!states.has(r.state)||!r.fields||typeof r.fields.body!=='string'||r.bodyDigest!==digest(r.fields.body)||r.envelopeDigest!==digest(JSON.stringify(r.fields))||typeof r.target!=='string'||!Array.isArray(r.reasons)||r.reasons.some(x=>!Object.values(reasons).includes(x)))throw new InboxError('invalid inbox item');
   ids.add(r.id);
  }
  return db;
 }
 transaction(fn) {
  if(this.readOnly)throw new InboxError('read-only inbox');
  // Cross-process exclusion without a lock spanning scanner or runtime awaits.
  // A stale lock fails closed; no automatic lock stealing/recovery service.
  const lock=this.file+'.lock'; fs.mkdirSync(lock,{mode:0o700});
  const temp=this.file+'.'+randomUUID()+'.tmp';
  try{
   const db=this.read(), result=fn(db), raw=JSON.stringify(db);
   if(db.items.length>this.maxItems||Buffer.byteLength(raw)>this.maxBytes)throw new InboxError('inbox capacity');
   const fd=fs.openSync(temp,'wx',0o600);
   try{fs.writeFileSync(fd,raw);fs.fsyncSync(fd);}finally{fs.closeSync(fd);}
   fs.renameSync(temp,this.file);
   const dir=fs.openSync(path.dirname(this.file),'r');try{fs.fsyncSync(dir);}finally{fs.closeSync(dir);}
   return result;
  }finally{
   if(fs.existsSync(temp))fs.unlinkSync(temp);
   fs.rmdirSync(lock);
  }
 }
 recover() {
  this.transaction(db=>{for(const r of db.items){
   if(r.state==='scanning'){r.state='held';r.reasons=[...new Set([...r.reasons,reasons.incomplete])];r.scan={verdict:'incomplete',reason:'interrupted'};}
   else if(r.state==='dispatching')r.state='unknown';
  }});
 }
 create(fields,target,policy) {
  return this.transaction(db=>{
   if(db.items.some(r=>r.fields.from===fields.from&&r.fields.message_id===fields.message_id))throw new InboxError('duplicate inbox item');
   const r={id:randomUUID(),fields:structuredClone(fields),target,bodyDigest:digest(fields.body),envelopeDigest:digest(JSON.stringify(fields)),policy:structuredClone(policy),state:'scanning',reasons:policy.approval?[reasons.approval]:[],createdAt:new Date().toISOString()};
   if(db.items.filter(x=>x.state==='scanning').length>=this.pendingLimit){r.state='held';r.reasons.push(reasons.incomplete);r.scan={verdict:'incomplete',reason:'pending_capacity'};}
   db.items.push(r);return structuredClone(r);
  });
 }
 change(id,fn) {return this.transaction(db=>{const r=db.items.find(x=>x.id===id);if(!r)throw new InboxError('item not found');fn(r);return structuredClone(r);});}
 get(id) {const r=this.read().items.find(x=>x.id===id);if(!r)throw new InboxError('item not found');return structuredClone(r);}
 discard(id) {return this.change(id,r=>{if(r.state!=='held')throw new InboxError('not held');r.state='discarded';});}
}

export function policyFor(config,peer,destination) {
 const configured=peer.mcs??'default',mode=configured==='default'?config.mcs:configured;
 if(!['off','dumb','smart','both'].includes(mode)||!['off','on'].includes(config.inbox))throw new InboxError('invalid policy');
 // Concrete prototype adapter accepts a resolved per-destination approval bit.
 const approvals=peer.approvalByDestination??config.approvalByDestination??{};
 const approval=Object.hasOwn(approvals,destination)?approvals[destination]:config.inbox==='on';
 if(typeof approval!=='boolean')throw new InboxError('invalid inbox policy');
 return {configured,mode,approval,revision:config.policyRevision??'prototype-1'};
}

function verdict(result) {
 if(!result||!['pass','flagged','incomplete'].includes(result.verdict))return {verdict:'incomplete',reason:'invalid_scanner_result'};
 // Scanner explanations never become model input or operational instructions.
 // Only engine-produced bounded metadata is persisted; never sent to destination.
 const safe={verdict:result.verdict,version:typeof result.version==='string'?result.version.slice(0,128):'unqualified'};
 for(const k of ['reason','stage','profile','model','endpoint','locality'])if(typeof result[k]==='string')safe[k]=result[k].slice(0,512);
 if(Number.isFinite(result.elapsedMs))safe.elapsedMs=result.elapsedMs;
 if(Number.isSafeInteger(result.requests))safe.requests=result.requests;
 if(result.usage)safe.usage=Object.fromEntries(['prompt_tokens','completion_tokens','total_tokens'].filter(k=>Number.isSafeInteger(result.usage[k])&&result.usage[k]>=0).map(k=>[k,result.usage[k]]));
 if(typeof result.returnedModel==='string')safe.returnedModel=result.returnedModel.slice(0,128);
 if(Array.isArray(result.findings))safe.findings=result.findings.slice(0,16).map(f=>({id:typeof f.id==='string'?f.id.slice(0,64):undefined,category:String(f.category).slice(0,64),reason:String(f.reason).slice(0,512),start:f.start,end:f.end,projection:f.projection}));
 return safe;
}
export class ReceiveFlow {
 constructor({inbox,authorize,resolve,submit,dumb,smart}) {Object.assign(this,{inbox,authorize,resolve,submit,dumb,smart});}
 async scan(fields,policy) {
  const deadlineAt=Date.now()+LIMITS.smartMs;
  if(policy.mode==='off')return {verdict:'skipped'};
  if(Buffer.byteLength(fields.body)>LIMITS.bodyBytes)return {verdict:'incomplete',reason:'scan_size'};
  try{
   // An absent engine is incomplete, never a pretend pass. Engine adapters must
   // enforce their own hard deadlines; fixture adapters are test-only.
   if(policy.mode==='dumb')return {...verdict(await this.dumb?.(fields.body)),stage:'dumb'};
   if(policy.mode==='both'){
    const d=verdict(await this.dumb?.(fields.body));
    if(d.verdict!=='pass')return {...d,stage:'dumb'};
    return {...verdict(await this.smart?.(fields.body,{deadlineAt})),stage:'smart',dumb:d};
   }
   if(policy.mode==='smart')return {...verdict(await this.smart?.(fields.body,{deadlineAt})),stage:'smart'};
   return {verdict:'incomplete',reason:'invalid_mode'};
  }catch{return {verdict:'incomplete',reason:'scanner_failed'};}
 }
 async dispatch(fields,target,id) {
  // No age/replay admission on an explicit release of an already-admitted item.
  // Signature/key, receiver, permission and mapping are checked again.
  if(await this.authorize(fields)!==target||!await this.resolve(target))throw new InboxError('destination unavailable or changed');
  if(await this.authorize(fields)!==target)throw new InboxError('permission changed');
  if(id)this.inbox.change(id,r=>{if(r.state!=='held'||r.reasons.length)throw new InboxError('not releasable');r.state='dispatching';});
  let result;
  try{result=await this.submit(fields,target);if(result?.status!=='submitted')result={status:'unknown',reason:'confirmation_unavailable'};}
  catch{result={status:'unknown',reason:'confirmation_unavailable'};}
  if(id)try{this.inbox.change(id,r=>{r.state=result.status;});}
  catch{return {status:'unknown',reason:'confirmation_unavailable'};}
  return result;
 }
 async receive(fields,target,policy) {
  // Called only after signed admission + rate/replay reservation + preflight.
  if(policy.mode==='off'&&!policy.approval)return this.dispatch(fields,target);
  const r=this.inbox.create(fields,target,policy);
  if(r.state==='held')return {status:'held',id:r.id,reasons:r.reasons};
  const scan=await this.scan(fields,policy);
  const item=this.inbox.change(r.id,x=>{x.scan=scan;x.state='held';
   if(scan.verdict==='flagged')x.reasons.push(reasons.flagged);
   if(scan.verdict==='incomplete')x.reasons.push(reasons.incomplete);
  });
  if(item.reasons.length)return {status:'held',id:item.id,reasons:item.reasons};
  return this.dispatch(fields,target,item.id);
 }
 async release(id,acknowledged=[]) {
  if(!Array.isArray(acknowledged)||acknowledged.some(x=>!Object.values(reasons).includes(x)))throw new InboxError('invalid acknowledgements');
  const r=this.inbox.get(id);
  if(r.state!=='held')throw new InboxError('not held');
  if(await this.authorize(r.fields)!==r.target)throw new InboxError('permission changed');
  const item=this.inbox.change(id,x=>{if(x.state!=='held')throw new InboxError('not held');x.reasons=x.reasons.filter(x=>!acknowledged.includes(x));});
  if(item.reasons.length)return {status:'held',id,reasons:item.reasons};
  return this.dispatch(item.fields,item.target,id);
 }
 async approveOrdinary() {
  const ids=this.inbox.read().items.filter(r=>r.state==='held'&&r.reasons.length===1&&r.reasons[0]===reasons.approval).map(r=>r.id);
  const results=[];for(const id of ids)results.push(await this.release(id,[reasons.approval]));return results;
 }
}
