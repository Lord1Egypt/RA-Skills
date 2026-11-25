import {readFile} from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';

export class BridgeError extends Error {
  constructor(code, details={}) { super(code); this.code=code; Object.assign(this,details); }
}
export function loopbackURL(value='http://127.0.0.1:17777') {
  let u;try{u=new URL(value)}catch{throw new BridgeError('invalid_bridge_url')}
  if(u.protocol!=='http:'||!['127.0.0.1','localhost','[::1]'].includes(u.hostname)||u.username||u.password||u.search||u.hash) throw new BridgeError('bridge_must_be_local');
  return u.origin;
}
export class Bridge {
  constructor({baseURL,token,fetchImpl=fetch}={}) {this.baseURL=loopbackURL(baseURL);this.token=token;this.fetch=fetchImpl;}
  static async connect({env=process.env,fetchImpl=fetch}={}) {
    const token=env.EASY_WEBBRIDGE_TOKEN||await readFile(path.join(os.homedir(),'.easy-webbridge','bridge-token'),'utf8').catch(()=>{throw new BridgeError('bridge_token_missing')});
    if(typeof token!=='string'||token.trim().length<16)throw new BridgeError('bridge_token_invalid');
    return new Bridge({baseURL:env.EASY_WEBBRIDGE_URL,token:token.trim(),fetchImpl});
  }
  async request(route,body,timeoutMs=20000) {
    let response;
    try {response=await this.fetch(this.baseURL+route,{method:body?'POST':'GET',headers:{Authorization:'Bearer '+this.token,...(body?{'Content-Type':'application/json'}:{})},body:body?JSON.stringify(body):undefined,redirect:'error',signal:AbortSignal.timeout(timeoutMs+3000)});}catch{throw new BridgeError('bridge_unreachable')}
    const buffer=await response.text();if(Buffer.byteLength(buffer)>4*1024*1024)throw new BridgeError('bridge_response_too_large');
    let value;try{value=JSON.parse(buffer)}catch{throw new BridgeError('bridge_response_invalid')}
    if(!response.ok||value.ok===false||value.error) {
      const detail=value.error?.code||value.code;const code=typeof detail==='string'&&/^[\w-]{1,64}$/.test(detail)?detail:'bridge_command_failed';
      throw new BridgeError(code,{httpStatus:response.status,timeout:/timed?\s*out|timeout|超时/i.test(String(value.error?.message||value.error||'')),frameChanged:/frame.*removed|context.*destroyed/i.test(String(value.error?.message||value.error||''))});
    }
    return value;
  }
  async browsers(){const d=await this.request('/v1/browsers');return d.browsers||d.result?.browsers||[];}
  async command(browserId,action,args={},timeoutMs=20000) {
    if(typeof browserId!=='string'||!browserId)throw new BridgeError('browser_required');
    const restore=action==='activate_tab'&&args.restoreSelection===true&&args.focus===false&&Number.isSafeInteger(args.tabId);
    const openResult=action==='click'&&!args.focus&&!args.active&&Number.isSafeInteger(args.tabId)&&typeof args.selector==='string'&&args.selector.length<500&&(!args.mode||args.mode==='dom');
    if(!['list_tabs','navigate','cdp','scroll','close_session','close_tab','capabilities'].includes(action)&&!restore&&!openResult)throw new BridgeError('action_not_readonly_search');
    // Only explicit restoration after a website-selected popup may select a tab;
    // routine search code never requests foreground activation or window focus.
    if(restore){args={...args};delete args.restoreSelection;}
    const d=await this.request('/v1/browsers/'+encodeURIComponent(browserId)+'/commands',{action,args,timeoutMs},timeoutMs);
    return Object.hasOwn(d,'result')?d.result:d;
  }
  async evaluate(browserId,tabId,expression,timeoutMs=15000){
    const d=await this.command(browserId,'cdp',{tabId,method:'Runtime.evaluate',params:{expression,returnByValue:true,awaitPromise:true}},timeoutMs);
    if(d.exceptionDetails)throw new BridgeError('page_expression_failed');
    const result=d.result?.result||d.result||d;
    if(result.type==='undefined'||!Object.hasOwn(result,'value'))throw new BridgeError('page_result_missing');
    return result.value;
  }
}
