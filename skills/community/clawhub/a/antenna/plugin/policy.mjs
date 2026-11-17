import {LIMITS} from './limits.mjs';
import path from 'node:path';
import {resolveScanner} from './smart.mjs';
export const modes=['off','dumb','smart','both'];
const modelModes=new Set(['smart','both']);
export function validateConfig(input,{requireReady=false,host={}}={}){
 const c=structuredClone(input);
 if(c.schemaVersion!==2)throw Error('explicit schema migration required');
 c.mcs??='dumb';c.inbox??='on';c.maxBodyChars??=65536;
 c.maxActiveSmart??=LIMITS.active;
 if(!Number.isInteger(c.maxActiveSmart)||c.maxActiveSmart<1||c.maxActiveSmart>LIMITS.active)throw Error('maxActiveSmart must be 1 or 2');
 if(!modes.includes(c.mcs)||!['on','off'].includes(c.inbox))throw Error('invalid mode');
 if(typeof c.receiver!=='string'||!c.receiver||typeof c.bearer!=='string'||c.bearer.length<32)throw Error('receiver and private bearer required');
 if(!c.peers||Array.isArray(c.peers)||!c.destinations||Array.isArray(c.destinations))throw Error('invalid peer/destination map');
 for(const peer of Object.values(c.peers)){
  if(!['default',...modes].includes(peer.mcs??'default')||!Array.isArray(peer.destinations)||typeof peer.publicKey!=='string')throw Error('invalid peer policy');
 }
 for(const target of Object.values(c.destinations))if(typeof target!=='string'||!target.startsWith('agent:'))throw Error('invalid destination');
 for(const f of ['inboxFile','replayFile'])if(typeof c[f]!=='string'||!path.isAbsolute(c[f]))throw Error('absolute state paths required');
 if(c.inboxFile===c.replayFile)throw Error('state paths must differ');
 if(!Number.isInteger(c.maxBodyChars)||c.maxBodyChars<1||c.maxBodyChars>1000000)throw Error('invalid body bound');
 if(requireReady&&[c.mcs,...Object.values(c.peers).map(p=>p.mcs)].some(m=>modelModes.has(m))){
  if(!c.scannerModel||resolveScanner(c.scannerModel,host).identity!==c.scannerIdentity)throw Error('check/select a registered scanner model before enabling Smart/Both');
 }
 return c;
}
