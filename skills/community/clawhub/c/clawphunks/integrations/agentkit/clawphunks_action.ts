/**
 * ClawPhunks AgentKit Action
 *
 * Mint and trade ClawPhunks NFTs with Coinbase AgentKit.
 * x402 payments are handled automatically by AgentKit.
 *
 * npm install @coinbase/agentkit
 *
 * Usage:
 *   import { clawphunksMintAction, clawphunksCollectionAction } from './clawphunks_action';
 *
 *   const agent = new AgentKit({
 *     actions: [clawphunksMintAction, clawphunksCollectionAction]
 *   });
 */

import { z } from 'zod';
import { ActionDefinition } from '@coinbase/agentkit';

const MINT_URL = 'https://clawphunks.vercel.app/mint';
const COLLECTION_URL = 'https://clawphunks.vercel.app/collection';
const SKILLS_URL = 'https://chainhost.online/clawphunks/skills';

/**
 * Mint a ClawPhunk NFT
 *
 * Costs $1.99 USDC on Base via x402 (AgentKit handles payment automatically).
 * Returns ethscription on Ethereum L1 + gas stipend for trading.
 */
export const clawphunksMintAction: ActionDefinition = {
  name: 'clawphunks_mint',
  description: 'Mint a random ClawPhunk NFT. Costs $1.99 USDC on Base. Returns ethscription on Ethereum L1 plus gas stipend.',
  schema: z.object({
    recipient: z.string().describe('Ethereum address to receive the ClawPhunk'),
  }),
  handler: async ({ recipient }, { wallet }) => {
    // AgentKit's x402 middleware handles 402 responses automatically
    const response = await fetch(MINT_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ recipient }),
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`Mint failed: ${error}`);
    }

    const result = await response.json();

    return {
      success: true,
      tokenId: result.tokenId,
      txHash: result.txHash,
      ethscriptionId: result.ethscriptionId,
      gasStipendWei: result.gasStipendWei,
      message: `Minted ClawPhunk #${result.tokenId} to ${recipient}`,
    };
  },
};

/**
 * Get ClawPhunks collection info
 */
export const clawphunksCollectionAction: ActionDefinition = {
  name: 'clawphunks_collection',
  description: 'Get ClawPhunks collection stats, rarity data, and mint availability.',
  schema: z.object({}),
  handler: async () => {
    const response = await fetch(COLLECTION_URL);

    if (!response.ok) {
      throw new Error(`Failed to fetch collection: ${response.status}`);
    }

    const data = await response.json();

    return {
      name: data.name,
      minted: data.minted,
      available: data.available,
      totalSupply: data.totalSupply,
      mintPrice: `${data.mintPrice} ${data.mintCurrency}`,
      escrowContract: data.escrowContract,
      rarity: {
        aliens: '9 (0.09%)',
        apes: '24 (0.24%)',
        zombies: '88 (0.88%)',
      },
    };
  },
};

/**
 * Get ClawPhunks trading scripts
 */
export const clawphunksSkillsAction: ActionDefinition = {
  name: 'clawphunks_skills',
  description: 'Get complete executable scripts for listing, buying, transferring, and rescuing ClawPhunks on L1.',
  schema: z.object({}),
  handler: async () => {
    const response = await fetch(SKILLS_URL);

    if (!response.ok) {
      throw new Error(`Failed to fetch skills: ${response.status}`);
    }

    return await response.json();
  },
};

/**
 * All ClawPhunks actions
 */
export const clawphunksActions = [
  clawphunksMintAction,
  clawphunksCollectionAction,
  clawphunksSkillsAction,
];

export default clawphunksActions;
