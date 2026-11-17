import { createInterface } from 'node:readline';
import { Gateway } from './gateway.mjs';
import { loadConfig } from './common.mjs';

// Standalone Skill transport: same gateway as MCP, no second implementation.
const gateway = new Gateway(loadConfig());
try {
  const mode=process.argv[2] || 'catalog';
  if(mode==='catalog') console.log(JSON.stringify(await gateway.call('earth2037_catalog',{limit:100}),null,2));
  else if(mode==='describe') console.log(JSON.stringify(await gateway.call('earth2037_describe',{command:process.argv[3]}),null,2));
  else if(mode==='show') console.log(JSON.stringify(gateway.present(await gateway.call('earth2037_show',{cacheId:process.argv[3],section:process.argv[4]||'all'})),null,2));
  else if(mode==='coords') console.log(JSON.stringify(await gateway.call('earth2037_coordinates',process.argv[4]===undefined?{tileId:Number(process.argv[3])}:{x:Number(process.argv[3]),y:Number(process.argv[4])}),null,2));
  else if(mode==='run') {
    const lines=createInterface({input:process.stdin,crlfDelay:Infinity});
    for await(const line of lines) {
      if(!line.trim())continue;
      try {
        const {tool,arguments:args={}}=JSON.parse(line);
        console.log(JSON.stringify({tool,result:gateway.present(await gateway.call(tool,args),tool==='earth2037_response')}));
      } catch(error) { console.log(JSON.stringify({ok:false,error:error.code || 'invalid_request',message:error.code?error.message:'Invalid request or local configuration'}));process.exitCode=1; }
    }
  } else throw new Error('Usage: node src/cli.mjs catalog | describe COMMAND | coords TILE_ID | coords X Y | show CACHE_ID [SECTION] | run < requests.ndjson');
} finally { await gateway.close(); }
