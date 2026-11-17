import {homedir} from 'node:os';
import {join,resolve} from 'node:path';
import {DeadlineSentinel} from '../lib/deadline-sentinel.mjs';
import {JsonFileStore} from '../lib/json-file-store.mjs';
const file=process.env.DEADLINE_SENTINEL_STATE_FILE||join(homedir(),'.local/share/deadline-sentinel/tasks.json');
const service=new DeadlineSentinel(new JsonFileStore(resolve(file),{tasks:[]}));
const [action,...args]=process.argv.slice(2);
try{
  let result;
  if(action==='list'&&args.length===0)result=await service.list();
  else if(action==='alerts'&&args.length===0)result=await service.alerts();
  else if(action==='add'&&args.length===5){
    const [id,title,dueAt,priority,project]=args;
    if(!id||!title||!project||!['low','medium','high'].includes(priority)||!/^\d{4}-\d{2}-\d{2}T.*(?:Z|[+-]\d\d:\d\d)$/.test(dueAt))throw Error('Supply ID TITLE ISO_TIMESTAMP_WITH_TIMEZONE low|medium|high PROJECT');
    result=await service.add({id,title,dueAt,priority,project,status:'todo'});
  }else if(action==='status'&&args.length===2){
    if(!['todo','in-progress','blocked','done'].includes(args[1]))throw Error('Unknown status');
    result=await service.updateStatus(args[0],args[1]);
  }else throw Error('Usage: deadlines.mjs list | alerts | add ID TITLE DUE_AT PRIORITY PROJECT | status ID STATUS');
  console.log(JSON.stringify(result,null,2));
}catch(error){console.error(JSON.stringify({error:error.message}));process.exitCode=1;}
