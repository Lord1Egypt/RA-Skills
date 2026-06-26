import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

// SEU CÓDIGO DE AFILIADO
const AFFILIATE_CODE = 'MARCUSFRANCA12';

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
    parameters: { type: 'object', properties: { layer: { type: 'string' }, status: { type: 'string' }, query: { type: 'string' } } },
    handler: async (args: any) => callBaoziMCP('list_markets', args)
  },
  {
    name: 'get-odds',
    description: 'Get odds, implied probabilities, and pool sizes',
    parameters: { type: 'object', properties: { marketId: { type: 'string' } }, required: ['marketId'] },
    handler: async (args: any) => callBaoziMCP('get_quote', { market: args.marketId })
  },
  {
    name: 'place-bet',
    description: 'Place a bet on a market outcome with affiliate tracking',
    parameters: { type: 'object', properties: { marketId: { type: 'string' }, outcome: { type: 'boolean' }, amount: { type: 'number' } }, required: ['marketId', 'outcome', 'amount'] },
    handler: async (args: any) => callBaoziMCP('build_bet_transaction_with_affiliate', { ...args, affiliateCode: AFFILIATE_CODE })
  },
  {
    name: 'get-portfolio',
    description: 'View all positions and bets for a wallet',
    parameters: { type: 'object', properties: { wallet: { type: 'string' } }, required: ['wallet'] },
    handler: async (args: any) => callBaoziMCP('get_portfolio', { wallet: args.wallet })
  },
  {
    name: 'claim-winnings',
    description: 'Claim SOL winnings from resolved markets',
    parameters: { type: 'object', properties: { marketId: { type: 'string' } }, required: ['marketId'] },
    handler: async (args: any) => callBaoziMCP('build_claim_transaction', { market: args.marketId })
  }
];

console.log('✅ BaoziClaw v1.1.0 - Affiliate:', AFFILIATE_CODE);
