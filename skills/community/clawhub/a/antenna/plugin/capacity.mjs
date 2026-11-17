import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawn} from 'node:child_process';
import {LIMITS} from './limits.mjs';
const busy=new Map();
export function capacityDirectory(state=process.env.OPENCLAW_STATE_DIR){return path.join(state??path.join(os.tmpdir(),'antenna-'+process.getuid()),'antenna-scan-slots');}
// Existing flock dependency: kernel-owned leases, no persisted owner/queue database.
// stdin EOF releases leases on parent exit; a hard lease timeout bounds orphan life.
export async function acquire(kind,deadlineAt,directory=capacityDirectory()){
 const key=path.resolve(directory)+':'+kind;
 if(!['dumb','smart'].includes(kind)||Date.now()>=deadlineAt||(busy.get(key)??0)>=LIMITS.active)return null;
 busy.set(key,(busy.get(key)??0)+1);
 const decrement=()=>busy.set(key,busy.get(key)-1);
 try{
  fs.mkdirSync(directory,{recursive:true,mode:0o700});
  const st=fs.lstatSync(directory);
  if(!st.isDirectory()||st.uid!==process.getuid()||(st.mode&0o077))throw Error('private scan directory required');
  for(let slot=0;slot<LIMITS.active;slot++){
   if(Date.now()>=deadlineAt)break;
   const fd=fs.openSync(path.join(directory,kind+'-'+slot),fs.constants.O_CREAT|fs.constants.O_RDWR|fs.constants.O_NOFOLLOW,0o600);
   const stat=fs.fstatSync(fd);
   if(!stat.isFile()||stat.uid!==process.getuid()||(stat.mode&0o077)){fs.closeSync(fd);throw Error('private scan slot required');}
   const lease=await new Promise(resolve=>{
    const seconds=Math.max(.001,(deadlineAt-Date.now())/1000).toFixed(3);
    const child=spawn('bash',['-c','flock -n 3 || exit 75; printf "ready\\n"; read -r -t "$1" ignored || :','antenna-scan',seconds],{stdio:['pipe','pipe','ignore',fd]});
    let ready=false,closed=false,output='';
    const close=()=>{if(!closed){closed=true;fs.closeSync(fd);}};
    const timer=setTimeout(()=>{child.kill('SIGKILL');close();},Math.max(1,deadlineAt-Date.now()));
    const ended=new Promise(done=>child.once('close',()=>{clearTimeout(timer);close();done();if(!ready)resolve(null);}));
    child.once('error',()=>{clearTimeout(timer);close();if(!ready)resolve(null);});
    child.stdin.on('error',()=>{});
    child.stdout.on('data',data=>{output+=data;if(!ready&&output.includes('ready\n')){ready=true;resolve(async()=>{child.stdin.end();await ended;});}});
   });
   if(lease){let released=false;return async()=>{if(released)return;released=true;try{await lease();}finally{decrement();}};}
  }
  decrement();return null;
 }catch{decrement();return null;}
}
