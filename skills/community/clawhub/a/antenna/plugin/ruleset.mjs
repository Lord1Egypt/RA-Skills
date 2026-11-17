import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
export const RULE_LIMITS=Object.freeze({bytes:262144,count:128,pattern:2048,explanation:512});
export function validateRuleset(data){
 if(!data||Object.keys(data).some(k=>!['formatVersion','rules'].includes(k))||data.formatVersion!==1||!Array.isArray(data.rules)||!data.rules.length||data.rules.length>RULE_LIMITS.count)throw Error('invalid ruleset format or rule count');
 const ids=new Set();
 for(const r of data.rules){
  if(!r||Object.keys(r).some(k=>!['id','pattern','flags','explanation'].includes(k))||typeof r.id!=='string'||! /^[A-Za-z0-9_-]{1,64}$/.test(r.id)||ids.has(r.id))throw Error('invalid or duplicate rule ID');
  ids.add(r.id);
  if(typeof r.pattern!=='string'||!r.pattern.length||r.pattern.length>RULE_LIMITS.pattern||typeof r.flags!=='string'||!/^[imsu]*$/.test(r.flags)||new Set(r.flags).size!==r.flags.length||typeof r.explanation!=='string'||!r.explanation.trim()||r.explanation.length>RULE_LIMITS.explanation)throw Error('invalid rule fields');
  try{new RegExp(r.pattern,r.flags);}catch{throw Error('invalid regex for '+r.id);}
 }
 return data;
}
export function loadRuleset(file){
 if(file!==undefined&&(typeof file!=='string'||!path.isAbsolute(file)))throw Error('ruleset path must be absolute');
 const source=file??new URL('./rules/default.json',import.meta.url);
 const fd=fs.openSync(source,fs.constants.O_RDONLY|fs.constants.O_NONBLOCK|fs.constants.O_NOFOLLOW);
 try{
  const st=fs.fstatSync(fd);if(!st.isFile()||st.size>RULE_LIMITS.bytes)throw Error('ruleset must be a bounded regular file');
  const raw=Buffer.alloc(RULE_LIMITS.bytes+1);let n=0,k;
  while(n<raw.length&&(k=fs.readSync(fd,raw,n,raw.length-n,null)))n+=k;
  if(n>RULE_LIMITS.bytes)throw Error('ruleset too large');
  const bytes=raw.subarray(0,n);let data;
  try{data=JSON.parse(new TextDecoder('utf-8',{fatal:true}).decode(bytes));}catch{throw Error('invalid ruleset JSON/UTF-8');}
  validateRuleset(data);
  const rules=data.rules.map(x=>Object.freeze({...x}));
  return Object.freeze({formatVersion:1,rules:Object.freeze(rules),hash:createHash('sha256').update(bytes).digest('hex')});
 }finally{fs.closeSync(fd);}
}
