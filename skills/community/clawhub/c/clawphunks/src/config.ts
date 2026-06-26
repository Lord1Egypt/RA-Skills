// Network configuration
export const isTestnet = process.env.NETWORK === 'base-sepolia';

// Pricing
export const MINT_PRICE_USDC = process.env.MINT_PRICE_USDC ?? '1.99';

// Gas stipend sent with each mint (~3.333 cents)
export const GAS_STIPEND_WEI = BigInt(process.env.GAS_STIPEND_WEI ?? '13333333333333'); // ~0.0000133 ETH

// Marketplace escrow contract (Ethereum L1)
export const ESCROW_CONTRACT = '0x3e67d49716e50a8b1c71b8dEa0e31755305733fd';

// Collection
export const COLLECTION = {
  name: 'ClawPhunks',
  symbol: 'CPHUNK',
  description: 'ClawPhunks - NFTs for AI agents. 10,000 phunks. Mint with x402, trade on L1.',
  totalSupply: 10000,
  chain: 'ethereum',
};

// Helper
export function padId(id: number): string {
  return String(id).padStart(4, '0');
}
