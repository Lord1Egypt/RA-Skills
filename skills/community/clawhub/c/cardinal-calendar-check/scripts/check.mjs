// AI-assisted adaptation of this assignment's original calendar interval logic.
// No network, process execution, environment access, or file writes.
import { openSync,readSync,closeSync,fstatSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
function instant(value) {
  if(typeof value!=='string'||!/^\d{4}-\d{2}-\d{2}T(?:[01]\d|2[0-3]):[0-5]\d(?::[0-5]\d(?:\.\d{1,3})?)?(?:Z|[+-](?:0\d|1[0-4]):[0-5]\d)$/.test(value))throw new Error('Timestamps need an explicit UTC offset or Z');
  const [year,month,day]=value.slice(0,10).split('-').map(Number),calendar=new Date(Date.UTC(year,month-1,day));
  if(calendar.getUTCFullYear()!==year||calendar.getUTCMonth()!==month-1||calendar.getUTCDate()!==day)throw new Error('Invalid calendar date');
  const result=Date.parse(value);if(!Number.isFinite(result))throw new Error('Invalid timestamp');return result;
}
export function checkCalendar(input) {
  if(!input||typeof input!=='object'||!Array.isArray(input.events)||input.events.length>200)throw new Error('Provide an events array of at most 200 events');
  const zone=input.timeZone??'UTC';
  const formatter=new Intl.DateTimeFormat('en-GB',{timeZone:zone,dateStyle:'short',timeStyle:'short',hourCycle:'h23'});
  const start=instant(input.window?.start),end=instant(input.window?.end);
  if(end<=start||end-start>7*86400000)throw new Error('Window must be positive and no longer than seven days');
  const busy=[],seen=new Set();
  for(const event of input.events) {
    if(!event||typeof event!=='object')throw new Error('Invalid event');
    if(event.status==='cancelled'||event.transparency==='transparent')continue;
    const from=instant(event.start),to=instant(event.end);
    if(to<=from)throw new Error('Event end must follow start');
    if(event.id!==undefined&&(typeof event.id!=='string'||event.id.length>200))throw new Error('Invalid event ID');
    if(typeof event.title!=='string'||event.title.length>300)throw new Error('Event title must be text of at most 300 characters');
    const key=JSON.stringify([event.id,event.title,from,to]);if(seen.has(key))continue;seen.add(key);
    if(to<=start||from>=end)continue;
    busy.push({title:event.title.replace(/[\x00-\x1f\x7f]/g,' '),start:Math.max(start,from),end:Math.min(end,to)});
  }
  busy.sort((a,b)=>a.start-b.start||a.end-b.end||a.title.localeCompare(b.title));
  const interval=(from,to)=>({start:new Date(from).toISOString(),end:new Date(to).toISOString(),localStart:formatter.format(new Date(from)),localEnd:formatter.format(new Date(to)),minutes:(to-from)/60000});
  const conflicts=[];
  for(let i=0;i<busy.length;i++)for(let j=i+1;j<busy.length;j++) {
    const from=Math.max(busy[i].start,busy[j].start),to=Math.min(busy[i].end,busy[j].end);
    if(from<to)conflicts.push({...interval(from,to),titles:[busy[i].title,busy[j].title]});
  }
  let cursor=start;const free=[];
  for(const event of busy){if(event.start>cursor)free.push(interval(cursor,event.start));cursor=Math.max(cursor,event.end);}
  if(cursor<end)free.push(interval(cursor,end));
  return {timeZone:zone,window:interval(start,end),busyEventCount:busy.length,conflicts,free,readonly:true,source:'provided_calendar_json'};
}
export function main(args=process.argv.slice(2)) {
  if(args.length!==0&&(args.length!==2||args[0]!=='--input'))throw new Error('Usage: check.mjs [--input authorized-calendar.json]');
  const fd=args.length?openSync(args[1],'r'):0;
  let raw;
  try {
    if(args.length&&(!fstatSync(fd).isFile()||fstatSync(fd).size>1024*1024))throw new Error('Input must be a JSON file no larger than 1 MiB');
    const bytes=Buffer.alloc(1024*1024+1);let used=0;
    while(used<bytes.length){const count=readSync(fd,bytes,used,bytes.length-used,null);if(!count)break;used+=count;}
    if(used>1024*1024)throw new Error('Input exceeds 1 MiB');
    raw=bytes.subarray(0,used).toString('utf8');
  }finally{if(args.length)closeSync(fd);}
  process.stdout.write(JSON.stringify(checkCalendar(JSON.parse(raw.replace(/^\uFEFF/,''))),null,2)+'\n');
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){try{main();}catch(error){process.stderr.write('Calendar check failed: '+error.message+'\n');process.exitCode=1;}}
