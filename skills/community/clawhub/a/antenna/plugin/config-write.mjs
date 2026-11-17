// Offline, cooperative compare-and-replace for a caller-selected JSON file.
// No jq programs, service control, config discovery or executable SecretRefs.
import fs from 'node:fs';
import path from 'node:path';
import {randomUUID} from 'node:crypto';
export function fileSnapshot(file){
 file=path.resolve(file);
 if(fs.realpathSync(file)!==file)throw Error('configuration symlinks are unsupported');
 const fd=fs.openSync(file,fs.constants.O_RDONLY|fs.constants.O_NOFOLLOW|fs.constants.O_NONBLOCK);
 try{
  const s=fs.fstatSync(fd);
  if(!s.isFile()||s.nlink!==1||s.size>8*1024*1024||s.uid!==process.getuid())throw Error('configuration must be a bounded owned regular file');
  const raw=fs.readFileSync(fd,'utf8');
  return {file,raw,mode:s.mode,stamp:[s.dev,s.ino,s.mode,s.size,s.mtimeMs,s.ctimeMs].join(':')};
 }finally{fs.closeSync(fd);}
}
export function snapshot(file){
 const record=fileSnapshot(file),value=JSON.parse(record.raw);
 if(!value||Array.isArray(value)||typeof value!=='object'||Object.hasOwn(value,'$include'))throw Error('resolved JSON object required; use OpenClaw config tools for includes');
 return {...record,value};
}
export function unchanged(before){
 const now=fileSnapshot(before.file);
 if(now.raw!==before.raw||now.stamp!==before.stamp)throw Error('configuration changed; reload before editing');
}
export function replaceJSON(before,next,{validate=()=>{}}={}){
 validate(next);const raw=JSON.stringify(next,null,2)+'\n';
 if(Buffer.byteLength(raw)>8*1024*1024)throw Error('configuration exceeds write limit');
 if(JSON.stringify(JSON.parse(before.raw))===JSON.stringify(next)){unchanged(before);return {saved:false,restartRequired:false};}
 const lock=before.file+'.antenna-lock',tmp=before.file+'.'+randomUUID()+'.tmp';
 fs.mkdirSync(lock,{mode:0o700});
 let backup;
 try{
  unchanged(before);
  backup=fs.mkdtempSync(before.file+'.antenna-backup-');fs.chmodSync(backup,0o700);
  const put=(file,data)=>{const fd=fs.openSync(file,'wx',0o600);try{fs.writeFileSync(fd,data);fs.fsyncSync(fd);}finally{fs.closeSync(fd);}};
  put(path.join(backup,'before.json'),before.raw);
  const backupDir=fs.openSync(backup,'r');try{fs.fsyncSync(backupDir);}finally{fs.closeSync(backupDir);}
  put(tmp,raw);
  // Recheck after staging/backup, immediately before replacement. Other host
  // writers must be stopped; a filesystem rename is not a cross-tool CAS API.
  unchanged(before);fs.renameSync(tmp,before.file);
  const dir=fs.openSync(path.dirname(before.file),'r');try{fs.fsyncSync(dir);}finally{fs.closeSync(dir);}
  return {saved:true,backup,reloadRequired:true,restartRequired:before.value.gateway?.reload?.mode==='off'?true:null,activation:'unchanged',applyNotice:'Apply through the host reload policy; restart only if hot reload is unavailable or disabled. No service command executed.'};
 }finally{
  if(fs.existsSync(tmp))fs.unlinkSync(tmp);
  fs.rmdirSync(lock);
 }
}
