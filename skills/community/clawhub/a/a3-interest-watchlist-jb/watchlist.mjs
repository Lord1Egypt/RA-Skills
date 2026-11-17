// Original portable helper. Store public news only; preserve legacy delivery evidence.
import topicConfig from './topics.json' with {type:'json'};
import {createHash} from 'node:crypto';
const POLICY=topicConfig.topics;
const hash=value=>createHash('sha256').update(value).digest('hex');
export const TOPICS=POLICY.map(topic=>topic.id);
export function canonicalURL(value){
 if(typeof value!=='string'||value.length>2048)throw Error('Invalid source URL');
 const url=new URL(value);
 if(url.protocol!=='https:'||url.username||url.password||url.port||
  /^(localhost|127\.|0\.|10\.|192\.168\.|169\.254\.|172\.(1[6-9]|2\d|3[01])\.|100\.(6[4-9]|[7-9]\d|1[01]\d|12[0-7])\.|\[)/i.test(url.hostname))throw Error('Public HTTPS source required');
 url.hash='';
 for(const key of [...url.searchParams.keys()])if(/^utm_/i.test(key)||/^(fbclid|gclid)$/i.test(key)||
  (/(^|\.)reuters\.com$/i.test(url.hostname)&&/^(link_source|taid)$/i.test(key)))url.searchParams.delete(key);
 url.searchParams.sort();
 url.pathname=url.pathname.replace(/\/+$/,'')||'/';
 return url.href;
}
export function normalizeItem(item,now=Date.now()){
 if(!TOPICS.includes(item.topic)||typeof item.title!=='string'||!item.title.trim()||item.title.length>240||
  !Array.isArray(item.facts)||item.facts.length<1||item.facts.length>6||
  item.facts.some(f=>typeof f!=='string'||!f.trim()||f.length>500))throw Error('Invalid news item');
 const url=canonicalURL(item.url);
 const hosts=POLICY.find(topic=>topic.id===item.topic)?.source_hosts;
 if(hosts&&(!Array.isArray(hosts)||!hosts.includes(new URL(url).hostname)))throw Error('Official source required for this topic');
 const published=Date.parse(item.publishedAt);
 if(!Number.isFinite(published)||published>now+300000||published<now-72*3600000)throw Error('Publication outside fresh window');
 const facts=item.facts.map(f=>f.trim().replace(/\s+/g,' '));
 return {topic:item.topic,title:item.title.trim(),url,publishedAt:new Date(published).toISOString(),facts,
  key:hash(url),fingerprint:hash(facts.join(' ').toLowerCase().replace(/[^\p{L}\p{N}]/gu,''))};
}
export function migrateHistory(state){
 if(!state?.reported||typeof state.reported!=='object'||Array.isArray(state.reported))throw Error('Invalid reported history');
 const entries=Object.entries(state.reported),reported={};let changed=0,collisions=0;
 if(entries.length>5000)throw Error('History review budget exceeded');
 for(const [oldKey,record]of entries){
  if(!record||typeof record.fingerprint!=='string'||!Number.isFinite(Date.parse(record.publishedAt)))throw Error('Unverifiable legacy history');
  const url=canonicalURL(record.url),key=hash(url),prior=reported[key];
  if(key!==oldKey||url!==record.url)changed++;
  if(prior)collisions++;
  if(!prior||Date.parse(record.publishedAt)>Date.parse(prior.publishedAt))reported[key]={...record,url};
 }
 if(changed||collisions){
  if(state.legacyReported&&(typeof state.legacyReported!=='object'||Array.isArray(state.legacyReported)))throw Error('Invalid legacy backup');
  state.legacyReported={...state.reported,...state.legacyReported};
 }
 state.reported=reported;state.canonicalVersion=2;
 if(Array.isArray(state.pending))for(const batch of state.pending){
  if(!Array.isArray(batch.items))throw Error('Invalid pending history');
  batch.items=batch.items.map(item=>{const url=canonicalURL(item.url);return {...item,url,key:hash(url)};});
 }
 return {changed,collisions,canonicalVersion:2};
}
export function selectItems(items,state,now=Date.now()){
 if(!Array.isArray(items)||items.length>20)throw Error('At most 20 candidates');
 migrateHistory(state);
 const selected=[],excluded=[],keys=new Set();
 for(const raw of items){
  let item;try{item=normalizeItem(raw,now);}catch{excluded.push({reason:'invalid_or_undated_or_stale'});continue;}
  if(keys.has(item.key)){excluded.push({reason:'duplicate_candidate'});continue;}
  const old=state.reported[item.key];
  if(old&&(old.fingerprint===item.fingerprint||Date.parse(item.publishedAt)<=Date.parse(old.publishedAt)||
   typeof raw.materialChange!=='string'||raw.materialChange.trim().length<30)){
   excluded.push({reason:'already_reported_or_change_unverified'});continue;
  }
  keys.add(item.key);selected.push({...item,...(old?{materialChange:raw.materialChange.slice(0,500)}:{})});
  if(selected.length===5)break;
 }
 return {selected,excluded};
}
function linkedKeys(text){
 if(typeof text!=='string'||text.length>20000)throw Error('Invalid delivered text');
 const keys=new Set();
 // Markdown destinations retain URL semantics even when the label is followed by punctuation.
 for(const match of text.matchAll(/\]\((https:\/\/[^\s<>"`\[\]]+)\)/g)){
  try{keys.add(hash(canonicalURL(match[1])));}catch{}
 }
 for(let token of (text.match(/https:\/\/[^\s<>"`]+/g)??[]).slice(0,40)){
  token=token.replace(/[.,;!]+$/,'');
  for(const [open,close]of [['(',')'],['[',']']]){
   while(token.endsWith(close)&&token.split(close).length>token.split(open).length)token=token.slice(0,-1);
  }
  try{keys.add(hash(canonicalURL(token)));}catch{}
 }
 return keys;
}
export function recordDelivered(state,pending,text,messageId){
 if(!/^\d{17,20}$/.test(messageId??''))throw Error('Actual delivery ID required');
 migrateHistory(state);const linked=linkedKeys(text);let count=0;
 for(const item of pending){
  const url=canonicalURL(item.url),key=hash(url);
  if(!linked.has(key))continue;
  state.reported[key]={fingerprint:item.fingerprint,publishedAt:item.publishedAt,messageId,url,title:item.title,facts:item.facts};count++;
 }
 return count;
}
