import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import { fileURLToPath } from 'node:url';
import { mkdtemp, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { readFileSync } from 'node:fs';

const state = await mkdtemp(join(tmpdir(), 'earth2037-doctor-'));
const client = new Client({name:'earth2037-install-check',version:'0.1.0'});
try {
  const env = Object.fromEntries(Object.entries(process.env).filter(([key]) => !key.startsWith('EARTH2037_')));
  await client.connect(new StdioClientTransport({command:process.execPath,args:[fileURLToPath(new URL('../src/main.mjs',import.meta.url))],
    env:{...env,EARTH2037_STATE_DIR:state,EARTH2037_READ_ONLY:'1'},stderr:'inherit'}));
  console.log(JSON.stringify(await verifyInstallation(client), null, 2));
} finally {await client.close();await rm(state,{recursive:true,force:true});}

// Validate the public MCP contract independently of transport lifecycle.
async function verifyInstallation(client) {
  const names=[];let cursor;
  do {const page=await client.listTools(cursor?{cursor}:{});names.push(...page.tools.map(t=>t.name));cursor=page.nextCursor;}while(cursor);
  const result=await client.callTool({name:'earth2037_coordinates',arguments:{tileId:130817}});
  const catalog = JSON.parse(readFileSync(new URL('../catalog.json', import.meta.url), 'utf8'));
  const namedCommands = catalog.commands.filter(entry => entry.route === 'game').map(entry => 'e2037_' + entry.name);
  if (result.isError || !names.includes('earth2037_enter') || !names.includes('earth2037_prepare') || !names.includes('earth2037_submit')
      || namedCommands.some(name => !names.includes(name)) || new Set(names).size !== names.length) throw new Error('Unexpected gateway response');
  return {ok:true,version:client.getServerVersion().version,tools:names.length,coordinates:result.structuredContent.result,
    gameLoginTested:false,message:'Installation works. No login or game write was performed. / 安装检查通过，未登录或操作游戏。'};
}
