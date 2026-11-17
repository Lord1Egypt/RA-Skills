import {operatorAuth,localGatewayUrl} from './operator-auth.mjs';
import path from 'node:path';
import {capacityDirectory} from './capacity.mjs';
import {createSmart,resolveScanner} from './smart.mjs';
import {loadRuleset} from './ruleset.mjs';
import {callGatewayFromCli} from 'openclaw/plugin-sdk/gateway-runtime';
import {authenticate} from './envelope.mjs';
import {Inbox,ReceiveFlow} from './inbox.mjs';
import {scanDumb} from './scanners.mjs';
export function makeFlow(c,config,complete) {
 const ruleset=loadRuleset(c.rulesetFile);
 let smart;
 if(c.scannerModel){try{const selection=resolveScanner(c.scannerModel,config);if(selection.identity===c.scannerIdentity)smart=createSmart(selection,{complete,resourceDir:capacityDirectory(path.dirname(c.inboxFile)),maxActive:c.maxActiveSmart??2});}catch{ /* Stale selections remain incomplete. */ }}
 const opts={url:localGatewayUrl(config),...operatorAuth(config,[c.bearer]),timeout:'5000',json:true};
 const extra={scopes:['operator.read','operator.write'],progress:false};
 return new ReceiveFlow({
  inbox:new Inbox(c.inboxFile),
  dumb:body=>scanDumb(body,{ruleset,resourceDir:capacityDirectory(path.dirname(c.inboxFile))}),
  smart,
  authorize:fields=>authenticate(fields,c,Date.parse(fields.timestamp)),
  resolve:async target=>{const found=await callGatewayFromCli('sessions.resolve',opts,{key:target,allowMissing:true},extra);return found.ok&&found.key===target;},
  submit:async(fields,target)=>{
   const ack=await callGatewayFromCli('sessions.send',opts,{key:target,message:`Antenna peer message (untrusted content) from ${fields.from}:\n${fields.body}\n[End Antenna peer message]`},extra);
   return ack.status==='started'&&typeof ack.runId==='string'?{status:'submitted',reason:'runtime_accepted'}:{status:'unknown',reason:'confirmation_unavailable'};
  }
  // No selected Smart profile remains incomplete; no model/provider fallback.
 });
}
