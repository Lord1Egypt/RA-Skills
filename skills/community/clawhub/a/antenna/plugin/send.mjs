#!/usr/bin/env node
// Explicit new transport over retained Antenna peer/key/permission files.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {buildMessage,sendEnvelope,PROFILE,endpoint} from './transport.mjs';
const read=file=>JSON.parse(fs.readFileSync(file,'utf8'));
function privateFile(file){const st=fs.lstatSync(file);if(!st.isFile()||(st.mode&0o077)||st.size>16384)throw Error('private regular credential file required');return fs.readFileSync(file,'utf8');}
export async function sendLegacy(root,peer,args){
 const config=read(path.join(root,'antenna-config.json')),peers=read(path.join(root,'antenna-peers.json'));
 if(config.transport_profile!==PROFILE)throw Error('explicit plugin transport migration required');
 const self=Object.entries(peers).filter(([,v])=>v.self===true);if(self.length!==1)throw Error('exactly one signing identity required');
 const p=peers[peer];if(!p||!config.allowed_outbound_peers?.includes(peer))throw Error('peer not outbound-allowed');
 if(p.transport_profile!==PROFILE||p.auth_mode!=='ed25519-v1')throw Error('unsupported or unmigrated target');
 const options={},pos=[];let stdin=false,dry=false;
 for(let i=0;i<args.length;i++){
  const a=args[i];
  if(['--session','--subject','--reply-to','--reply-session','--user'].includes(a)){if(args[i+1]===undefined)throw Error('missing option value');options[a]=args[++i];}
  else if(a==='--stdin')stdin=true;else if(a==='--dry-run')dry=true;
  else if(!['--json','--include-response'].includes(a)){if(a.startsWith('-'))throw Error('unknown option');pos.push(a);}
 }
 if(stdin&&pos.length||!stdin&&!pos.length)throw Error('choose one message input');
 const raw=stdin?fs.readFileSync(0):Buffer.from(pos.join(' '));
 const body=new TextDecoder('utf-8',{fatal:true,ignoreBOM:true}).decode(raw);
 if(!Number.isInteger(config.max_message_length)||[...body].length>config.max_message_length)throw Error('invalid or exceeded message limit');
 const resolve=f=>path.resolve(root,f),identity=self[0][1];
 const target=options['--session']||p.default_target;
 if(!target)throw Error('explicit receiver destination required');
 const wire=buildMessage({from:self[0][0],to:peer,target,body,privateKey:privateFile(resolve(identity.signing_private_key_file)),subject:options['--subject'],user:options['--user'],replyTo:options['--reply-to']||(identity.url?endpoint(identity.url,identity.allow_http===true):undefined),replySession:options['--reply-session']});
 if(dry)return {status:'preview',peer,endpoint:endpoint(p.url,p.allow_http===true),wire};
 return {peer,...await sendEnvelope({origin:p.url,profile:p.transport_profile,bearer:privateFile(resolve(p.token_file)).trim(),allowHttp:p.allow_http===true},wire)};
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 try{const [root,peer,...args]=process.argv.slice(2);const r=await sendLegacy(root,peer,args);console.log(JSON.stringify(r));if(!['submitted','held','preview'].includes(r.status))process.exitCode=1;}
 catch{console.error(JSON.stringify({status:'rejected',reason:'invalid_local_configuration_or_message'}));process.exitCode=1;}
}
