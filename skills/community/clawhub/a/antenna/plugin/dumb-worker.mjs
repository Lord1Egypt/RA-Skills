import {LIMITS} from './limits.mjs';
import {parentPort,workerData} from 'node:worker_threads';
export const VERSION='antenna-dumb-0.3';
function scan({body,ruleset}){
 const rules=ruleset.rules.map(r=>[r.id,'pattern',r.explanation,new RegExp(r.pattern,r.flags+'g')]);
 const budget=Math.min(LIMITS.derivedMultiplier*Buffer.byteLength(body),LIMITS.derivedBytes);let derived=0,incomplete=false;
 const findings=[],seen=new Set();
 function inspect(text,map,depth,projection){
  let normalized='',nm=[];
  for(let i=0;i<text.length;){const cp=String.fromCodePoint(text.codePointAt(i));const span=map[i];i+=cp.length;
   const value=cp.normalize('NFKC').toLowerCase().replace(/[\u200b-\u200d\ufeff]/gu,'');
   normalized+=value;for(let j=0;j<value.length;j++)nm.push(span);
  }
  if(projection!=='original')derived+=Buffer.byteLength(text);
  derived+=Buffer.byteLength(normalized);
  if(derived>budget){incomplete=true;return;}
  for(const [id,category,reason,re] of rules){re.lastIndex=0;let m;
   while((m=re.exec(normalized))&&findings.length<LIMITS.findings){// Only direct clause-local negation; never exempt quotations or later matches.
    const prefix=normalized.slice(Math.max(0,m.index-48),m.index);
    if(/(?:^|[.!?;\n]\s*)(?:please\s+)?(?:never|do not|don't)\s+$/u.test(prefix)){re.lastIndex=m.index+1;continue;}
    if(!m[0].length){re.lastIndex=m.index+1;continue;}
    const start=nm[m.index][0],end=nm[m.index+m[0].length-1][1],key=id+':'+start+':'+end;
    if(!seen.has(key)){seen.add(key);findings.push({id,category,reason,start,end,projection});}
   }
  }
  // Only explicit base64 labels and runs of >=4 hex escapes are candidates.
  const candidates=/\bbase64\s*:\s*([A-Za-z0-9+/=]{8,})|((?:\\u[0-9a-fA-F]{4}|\\x[0-9a-fA-F]{2}){4,})/g;
  for(const m of text.matchAll(candidates)){
   if(depth>=LIMITS.decodeDepth){incomplete=true;continue;}
   let decoded;
   try{if(m[1]){const raw=Buffer.from(m[1],'base64');if(raw.toString('base64')!==m[1])throw Error();decoded=new TextDecoder('utf-8',{fatal:true}).decode(raw);}
    else decoded=m[2].replace(/\\u([0-9a-fA-F]{4})|\\x([0-9a-fA-F]{2})/g,(_,u,x)=>String.fromCharCode(parseInt(u??x,16)));
   }catch{incomplete=true;continue;}
   const span=[map[m.index][0],map[m.index+m[0].length-1][1]];
   inspect(decoded,Array.from({length:decoded.length},()=>span),depth+1,m[1]?'base64':'escape');
  }
 }
 const map=Array.from({length:body.length},(_,i)=>[i,i+1]);inspect(body,map,0,'original');
 return {schema:1,version:VERSION,verdict:findings.length?'flagged':incomplete?'incomplete':'pass',findings,reason:incomplete?'inspection_budget_or_encoding':undefined};
}
if(parentPort){
 if(workerData!==null&&workerData!==undefined)parentPort.postMessage(scan(workerData));
 else parentPort.on('message',body=>parentPort.postMessage(scan(body)));
}
