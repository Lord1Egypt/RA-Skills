import {operatorAuth,localGatewayUrl} from './operator-auth.mjs';
import {createHash} from 'node:crypto';
import {LIMITS} from './limits.mjs';
import {acquire} from './capacity.mjs';
import {rubric,RUBRIC,validateVerdict} from './scanners.mjs';
export function resolveScanner(model,host){
 if(typeof model!=='string'||!model.trim()||model.includes('@'))throw Error('select a registered model or alias');
 const entries=host.agents?.defaults?.models??{},aliases=Object.entries(entries).filter(([id,v])=>id===model||v.alias===model);
 if(aliases.length>1)throw Error('ambiguous model alias');
 const id=aliases[0]?.[0]??model,slash=id.indexOf('/');
 const provider=host.models?.providers?.[id.slice(0,slash)];
 if(slash<1||(!Object.hasOwn(entries,id)&&!provider?.models?.some(x=>x.id===id.slice(slash+1))))throw Error('model not registered; add it to host model configuration');
 // Bind authored route/auth-reference configuration without persisting any credential value.
 const identity=createHash('sha256').update(JSON.stringify([id,provider?.baseUrl??null,provider?.api??null,provider?.auth??null,entries[id]?.runtime??null,provider?.runtime??null,host.auth?.order??null])).digest('hex');
 return {model,modelId:id,identity};
}
const incomplete=reason=>({schema:1,version:RUBRIC,verdict:'incomplete',findings:[],reason});
export function createSmart(selection,{complete,resourceDir,maxActive=LIMITS.active,deadlineMs=LIMITS.smartMs}={}){
 if(!Number.isInteger(deadlineMs)||deadlineMs<1||deadlineMs>LIMITS.smartMs||!Number.isInteger(maxActive)||maxActive<1||maxActive>LIMITS.active)throw Error('invalid scanner bounds');
 let active=0;
 return async(body,{deadlineAt=Date.now()+deadlineMs}={})=>{
  if(typeof complete!=='function')return incomplete('runtime_scanner_unavailable');
  if(typeof body!=='string'||Buffer.byteLength(body)>LIMITS.bodyBytes)return incomplete('input_size');
  const prompt=JSON.stringify({untrusted_message:body});
  if(Buffer.byteLength(prompt)+Buffer.byteLength(rubric)>LIMITS.requestBytes)return incomplete('request_budget');
  if(active>=maxActive)return incomplete('scanner_capacity');
  active++;let release,timer,requests=0;const controller=new AbortController(),began=performance.now();
  try{
   const deadline=Math.min(deadlineAt,Date.now()+deadlineMs);
   release=await acquire('smart',deadline,resourceDir);if(!release)return incomplete('scanner_capacity');
   const remaining=deadline-Date.now();if(remaining<=0)return incomplete('scheduling_deadline');
   const timeout=new Promise((_,reject)=>{timer=setTimeout(()=>{controller.abort();reject(Error('scanner_timeout'));},remaining);});
   requests=1;
   const result=await Promise.race([complete({model:selection.modelId,systemPrompt:rubric,messages:[{role:'user',content:prompt}],purpose:'antenna.mcs',maxTokens:LIMITS.outputTokens,signal:controller.signal,execution:{mode:'isolated-agent-runtime',timeoutMs:remaining}}),timeout]);
   if(result.execution?.mode!=='isolated-agent-runtime'||result.stopReason&&result.stopReason!=='stop'||typeof result.text!=='string'||Buffer.byteLength(result.text)>LIMITS.responseBytes) return {...incomplete('invalid_runtime_response'),requests};
   if(result.provider+'/'+result.model!==selection.modelId)return {...incomplete('model_identity_changed'),requests};
   const value=validateVerdict(JSON.parse(result.text));
   return {...value,version:RUBRIC,model:selection.modelId,requests,elapsedMs:performance.now()-began};
  }catch(e){
   // Stable runtime codes only; never return raw provider errors or credentials.
   const reason=typeof e.code==='string'&&/^[A-Z0-9_]{1,80}$/.test(e.code)?e.code:'runtime_scanner_failed';
   return {...incomplete(reason),requests,elapsedMs:performance.now()-began};
  }finally{clearTimeout(timer);controller.abort();if(release)await release();active--;}
 };
}
export async function gatewayScan(host,selection,body){
 const {callGatewayFromCli}=await import('openclaw/plugin-sdk/gateway-runtime');
 return callGatewayFromCli('antenna.scan',{url:localGatewayUrl(host),...operatorAuth(host,[host.plugins?.entries?.antenna?.config?.bearer]),timeout:String(LIMITS.smartMs+5000),json:true},{model:selection.model,identity:selection.identity,body},{scopes:['operator.admin'],progress:false});
}
