import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

async function callBaoziMCP(toolName: string, args: any = {}) {
  const command = `npx -y @baozi.bet/mcp-server --tool ${toolName} --args '${JSON.stringify(args)}'`;
  try {
    const { stdout, stderr } = await execAsync(command);
    if (stderr) console.error('Stderr:', stderr);
    return JSON.parse(stdout);
  } catch (error) {
    console.error(`Error calling ${toolName}:`, error);
    throw error;
  }
}

export const tools = [
  {
    name: 'list-markets',
    description: 'List active prediction markets on Baozi',
    parameters: { type: 'object', properties: {} },
    handler: async (args: any) => callBaoziMCP('list_markets', args)
  },
  {
    name: 'get-odds',
    description: 'Get odds for a market',
    parameters: { type: 'object', properties: { marketId: { type: 'string' } }, required: ['marketId'] },
    handler: async (args: any) => callBaoziMCP('get_quote', { market: args.marketId })
  },
  {
    name: 'place-bet',
    description: 'Place a bet',
    parameters: { type: 'object', properties: { marketId: { type: 'string' }, outcome: { type: 'boolean' }, amount: { type: 'number' } }, required: ['marketId', 'outcome', 'amount'] },
    handler: async (args: any) => callBaoziMCP('build_bet_transaction', args)
  }
];

console.log('✅ BaoziClaw skill loaded with', tools.length, 'tools');
