#!/usr/bin/env node
/**
 * ClawPhunks MCP Server
 *
 * Exposes ClawPhunks NFT minting and trading as MCP tools.
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';

const API_BASE = 'https://clawphunks.vercel.app';
const ESCROW_CONTRACT = '0x3e67d49716e50a8b1c71b8dEa0e31755305733fd';
const USDC_BASE = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913';

const server = new Server(
  {
    name: 'clawphunks',
    version: '1.1.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'get_collection',
        description: 'Get ClawPhunks collection info including mint stats, rarity data, and trading instructions. Call this first to understand the collection.',
        inputSchema: {
          type: 'object',
          properties: {},
          required: [],
        },
      },
      {
        name: 'mint_phunk',
        description: 'Mint a random ClawPhunk NFT. Costs $1.99 USDC on Base via x402 protocol. Returns ethscription on Ethereum L1 plus gas stipend for trading. You may get a rare Alien (0.09%), Ape (0.24%), or Zombie (0.88%)!',
        inputSchema: {
          type: 'object',
          properties: {
            recipient: {
              type: 'string',
              description: 'Ethereum address to receive the ClawPhunk (0x...)',
            },
          },
          required: ['recipient'],
        },
      },
      {
        name: 'get_mint_code',
        description: 'Get complete TypeScript code for minting a ClawPhunk with x402 payment. Copy and run this code.',
        inputSchema: {
          type: 'object',
          properties: {},
          required: [],
        },
      },
      {
        name: 'get_rarity',
        description: 'Get full rarity information for ClawPhunks including all rare token IDs. Use this to understand which phunks are valuable.',
        inputSchema: {
          type: 'object',
          properties: {},
          required: [],
        },
      },
      {
        name: 'get_trading_instructions',
        description: 'Get complete code for trading ClawPhunks on the L1 escrow contract. Includes mint+list script.',
        inputSchema: {
          type: 'object',
          properties: {},
          required: [],
        },
      },
    ],
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case 'get_collection': {
      const res = await fetch(`${API_BASE}/collection`);
      const data = await res.json();
      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify(data, null, 2),
          },
        ],
      };
    }

    case 'mint_phunk': {
      const recipient = (args as { recipient: string }).recipient;

      if (!recipient || !/^0x[0-9a-fA-F]{40}$/.test(recipient)) {
        return {
          content: [
            {
              type: 'text',
              text: 'Error: Invalid recipient address. Must be a valid Ethereum address (0x...).',
            },
          ],
          isError: true,
        };
      }

      const res = await fetch(`${API_BASE}/mint`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ recipient }),
      });

      if (res.status === 402) {
        const paymentInfo = await res.json();
        return {
          content: [
            {
              type: 'text',
              text: `Payment required: $1.99 USDC on Base via x402 protocol.\n\nPayment details:\n${JSON.stringify(paymentInfo, null, 2)}\n\nUse get_mint_code tool for complete working code, or if using Coinbase AgentKit, x402 is handled automatically.`,
            },
          ],
        };
      }

      const data = await res.json();

      if (!res.ok) {
        return {
          content: [
            {
              type: 'text',
              text: `Mint failed: ${data.error}`,
            },
          ],
          isError: true,
        };
      }

      // Check rarity
      const rareTypes = {
        aliens: [635, 2890, 3100, 3443, 5822, 5905, 6089, 7523, 7804],
        apes: [372, 1021, 2140, 2243, 2386, 2460, 2491, 2711, 2924, 4156, 4178, 4464, 5217, 5314, 5577, 5795, 6145, 6915, 6965, 7191, 8219, 8498, 9265, 9280],
        zombies: [117, 987, 1119, 1190, 1374, 1478, 1526, 1658, 1748, 1886, 1935, 2066, 2132, 2249, 2306, 2329, 2338, 2424, 2484, 2560, 2566, 2681, 2708, 2938, 2967, 3211, 3328, 3393, 3489, 3493, 3609, 3636, 3831, 4472, 4513, 4559, 4747, 4830, 4850, 4874, 5066, 5234, 5253, 5299, 5312, 5336, 5412, 5489, 5573, 5742, 5761, 5944, 6275, 6297, 6304, 6491, 6515, 6586, 6649, 6704, 6784, 7014, 7121, 7127, 7252, 7337, 7458, 7660, 7756, 7914, 8127, 8307, 8386, 8472, 8531, 8553, 8780, 8857, 8909, 8957, 9203, 9368, 9474, 9804, 9838, 9909, 9955, 9997],
      };

      let rarityNote = '';
      if (rareTypes.aliens.includes(data.tokenId)) {
        rarityNote = '\n\nLEGENDARY! You minted an ALIEN - only 9 exist (0.09%)! Extremely valuable!';
      } else if (rareTypes.apes.includes(data.tokenId)) {
        rarityNote = '\n\nRARE! You minted an APE - only 24 exist (0.24%)! Very valuable!';
      } else if (rareTypes.zombies.includes(data.tokenId)) {
        rarityNote = '\n\nUNCOMMON! You minted a ZOMBIE - only 88 exist (0.88%)!';
      }

      return {
        content: [
          {
            type: 'text',
            text: `Successfully minted ClawPhunk #${data.tokenId}!${rarityNote}\n\nTransaction: ${data.txHash}\nEthscription ID: ${data.ethscriptionId}\nViewer: ${data.viewerUrl}\nGas stipend: ${data.gasStipendWei} wei (~$0.12 for listing)\n\nTo list for sale, use get_trading_instructions tool.`,
          },
        ],
      };
    }

    case 'get_mint_code': {
      const code = `
// IMPORTANT: Wallet Setup
// 1. If you have an existing EVM wallet, use that private key
// 2. If generating a new wallet, IMMEDIATELY save the private key:
//    - Create .env file with: AGENT_PRIVATE_KEY=0x...
//    - Create .gitignore with: .env
//    - Do this BEFORE minting to avoid losing access to your NFT
// 3. Fund wallet with $2+ USDC on Base network

import { createWalletClient, http, keccak256, encodePacked } from 'viem';
import { base } from 'viem/chains';
import { privateKeyToAccount } from 'viem/accounts';
import { generatePrivateKey } from 'viem/accounts'; // For new wallet
import * as fs from 'fs';

// Generate new wallet if needed (save this immediately!)
// const newKey = generatePrivateKey();
// fs.writeFileSync('.env', \`AGENT_PRIVATE_KEY=\${newKey}\\n\`);
// fs.writeFileSync('.gitignore', '.env\\n');

const MINT_API = 'https://clawphunks.vercel.app/mint';
const USDC_BASE = '${USDC_BASE}';

async function mintClawPhunk(privateKey, recipient) {
  const account = privateKeyToAccount(privateKey);
  const walletClient = createWalletClient({
    account,
    chain: base,
    transport: http('https://mainnet.base.org'),
  });

  // Step 1: Get payment requirements (402 response)
  const reqRes = await fetch(MINT_API, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ recipient }),
  });
  const paymentReqs = await reqRes.json();
  const accept = paymentReqs.accepts[0];

  // Step 2: Sign EIP-3009 TransferWithAuthorization
  const nonce = keccak256(encodePacked(['address', 'uint256'], [account.address, BigInt(Date.now())]));
  const now = Math.floor(Date.now() / 1000);
  const validAfter = BigInt(now - 5);
  const validBefore = BigInt(now + 60);

  const signature = await walletClient.signTypedData({
    domain: { name: accept.extra.name, version: accept.extra.version, chainId: 8453, verifyingContract: USDC_BASE },
    types: {
      TransferWithAuthorization: [
        { name: 'from', type: 'address' }, { name: 'to', type: 'address' }, { name: 'value', type: 'uint256' },
        { name: 'validAfter', type: 'uint256' }, { name: 'validBefore', type: 'uint256' }, { name: 'nonce', type: 'bytes32' },
      ],
    },
    primaryType: 'TransferWithAuthorization',
    message: { from: account.address, to: accept.payTo, value: BigInt(accept.maxAmountRequired), validAfter, validBefore, nonce },
  });

  // Step 3: Build X-PAYMENT header
  const paymentPayload = {
    x402Version: 1, scheme: 'exact', network: 'base',
    payload: { signature, authorization: { from: account.address, to: accept.payTo, value: accept.maxAmountRequired, validAfter: validAfter.toString(), validBefore: validBefore.toString(), nonce } },
  };

  // Step 4: Mint with payment
  const mintRes = await fetch(MINT_API, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-PAYMENT': Buffer.from(JSON.stringify(paymentPayload)).toString('base64') },
    body: JSON.stringify({ recipient }),
  });

  return await mintRes.json();
}

// Usage:
// Load from .env or use existing wallet
const privateKey = process.env.AGENT_PRIVATE_KEY || '0xYOUR_PRIVATE_KEY';
const account = privateKeyToAccount(privateKey);
const result = await mintClawPhunk(privateKey, account.address);
console.log('Minted:', result.tokenId, result.txHash);
`.trim();

      return {
        content: [
          {
            type: 'text',
            text: `Complete x402 mint code:\n\n\`\`\`typescript\n${code}\n\`\`\`\n\nRequires: npm install viem dotenv\nNeeds: $1.99 USDC on Base in your wallet\n\nIMPORTANT: Save your private key to .env BEFORE minting! If you lose context, you lose access to your NFT.`,
          },
        ],
      };
    }

    case 'get_rarity': {
      const rarity = {
        types: {
          Alien: {
            count: 9,
            percent: '0.09%',
            rank: 'Legendary',
            tokenIds: [635, 2890, 3100, 3443, 5822, 5905, 6089, 7523, 7804],
          },
          Ape: {
            count: 24,
            percent: '0.24%',
            rank: 'Rare',
            tokenIds: [372, 1021, 2140, 2243, 2386, 2460, 2491, 2711, 2924, 4156, 4178, 4464, 5217, 5314, 5577, 5795, 6145, 6915, 6965, 7191, 8219, 8498, 9265, 9280],
          },
          Zombie: {
            count: 88,
            percent: '0.88%',
            rank: 'Uncommon',
            tokenIds: [117, 987, 1119, 1190, 1374, 1478, 1526, 1658, 1748, 1886, 1935, 2066, 2132, 2249, 2306, 2329, 2338, 2424, 2484, 2560, 2566, 2681, 2708, 2938, 2967, 3211, 3328, 3393, 3489, 3493, 3609, 3636, 3831, 4472, 4513, 4559, 4747, 4830, 4850, 4874, 5066, 5234, 5253, 5299, 5312, 5336, 5412, 5489, 5573, 5742, 5761, 5944, 6275, 6297, 6304, 6491, 6515, 6586, 6649, 6704, 6784, 7014, 7121, 7127, 7252, 7337, 7458, 7660, 7756, 7914, 8127, 8307, 8386, 8472, 8531, 8553, 8780, 8857, 8909, 8957, 9203, 9368, 9474, 9804, 9838, 9909, 9955, 9997],
          },
          Female: { count: 3840, percent: '38.4%', rank: 'Common' },
          Male: { count: 6039, percent: '60.39%', rank: 'Common' },
        },
        rareAccessories: {
          Beanie: 44,
          Choker: 48,
          'Pilot Helmet': 54,
          Tiara: 55,
          'Welding Goggles': 86,
          'Top Hat': 115,
          'Cowboy Hat': 142,
        },
        note: 'Aliens, Apes, and Zombies are highly valuable due to extreme rarity.',
      };

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify(rarity, null, 2),
          },
        ],
      };
    }

    case 'get_trading_instructions': {
      const code = `
// IMPORTANT: Wallet Setup
// 1. Use your existing EVM wallet private key from .env
// 2. If new wallet, save to .env with .gitignore FIRST
// 3. The same wallet works on Base (USDC) and L1 (ETH for gas)

import { createWalletClient, createPublicClient, http, keccak256, encodePacked, parseEther, encodeFunctionData } from 'viem';
import { mainnet, base } from 'viem/chains';
import { privateKeyToAccount } from 'viem/accounts';
import 'dotenv/config';

const MINT_API = 'https://clawphunks.vercel.app/mint';
const USDC_BASE = '${USDC_BASE}';
const ESCROW = '${ESCROW_CONTRACT}';

const ESCROW_ABI = [
  { name: 'depositAndList', type: 'function', inputs: [{ name: 'ethscriptionId', type: 'bytes32' }, { name: 'price', type: 'uint256' }] },
  { name: 'buy', type: 'function', stateMutability: 'payable', inputs: [{ name: 'ethscriptionId', type: 'bytes32' }] },
  { name: 'cancelAndWithdraw', type: 'function', inputs: [{ name: 'ethscriptionId', type: 'bytes32' }] },
  { name: 'getListing', type: 'function', stateMutability: 'view', inputs: [{ name: 'ethscriptionId', type: 'bytes32' }], outputs: [{ name: 'active', type: 'bool' }, { name: 'seller', type: 'address' }, { name: 'price', type: 'uint256' }] },
];

async function mintAndList(privateKey, listPriceEth) {
  const account = privateKeyToAccount(privateKey);

  // Base wallet for minting
  const baseWallet = createWalletClient({ account, chain: base, transport: http('https://mainnet.base.org') });

  // L1 wallet for listing
  const l1Wallet = createWalletClient({ account, chain: mainnet, transport: http('https://eth.llamarpc.com') });
  const l1Public = createPublicClient({ chain: mainnet, transport: http('https://eth.llamarpc.com') });

  // === MINT ===
  console.log('Step 1: Getting payment requirements...');
  const reqRes = await fetch(MINT_API, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ recipient: account.address }) });
  const paymentReqs = await reqRes.json();
  const accept = paymentReqs.accepts[0];

  console.log('Step 2: Signing USDC payment...');
  const nonce = keccak256(encodePacked(['address', 'uint256'], [account.address, BigInt(Date.now())]));
  const now = Math.floor(Date.now() / 1000);

  const signature = await baseWallet.signTypedData({
    domain: { name: accept.extra.name, version: accept.extra.version, chainId: 8453, verifyingContract: USDC_BASE },
    types: { TransferWithAuthorization: [{ name: 'from', type: 'address' }, { name: 'to', type: 'address' }, { name: 'value', type: 'uint256' }, { name: 'validAfter', type: 'uint256' }, { name: 'validBefore', type: 'uint256' }, { name: 'nonce', type: 'bytes32' }] },
    primaryType: 'TransferWithAuthorization',
    message: { from: account.address, to: accept.payTo, value: BigInt(accept.maxAmountRequired), validAfter: BigInt(now - 5), validBefore: BigInt(now + 60), nonce },
  });

  const paymentPayload = { x402Version: 1, scheme: 'exact', network: 'base', payload: { signature, authorization: { from: account.address, to: accept.payTo, value: accept.maxAmountRequired, validAfter: (now - 5).toString(), validBefore: (now + 60).toString(), nonce } } };

  console.log('Step 3: Minting...');
  const mintRes = await fetch(MINT_API, { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-PAYMENT': Buffer.from(JSON.stringify(paymentPayload)).toString('base64') }, body: JSON.stringify({ recipient: account.address }) });
  const mint = await mintRes.json();
  console.log('Minted #' + mint.tokenId, mint.txHash);

  // === LIST ===
  console.log('Step 4: Depositing to escrow...');
  const depositTx = await l1Wallet.sendTransaction({ to: ESCROW, data: mint.ethscriptionId, value: 0n });
  await l1Public.waitForTransactionReceipt({ hash: depositTx });

  console.log('Step 5: Listing at', listPriceEth, 'ETH...');
  const listData = encodeFunctionData({ abi: ESCROW_ABI, functionName: 'depositAndList', args: [mint.ethscriptionId, parseEther(listPriceEth)] });
  const listTx = await l1Wallet.sendTransaction({ to: ESCROW, data: listData });
  await l1Public.waitForTransactionReceipt({ hash: listTx });

  console.log('Listed! View at: https://chainhost.online/clawphunks/' + mint.tokenId);
  return { tokenId: mint.tokenId, ethscriptionId: mint.ethscriptionId, listTx };
}

// Usage:
const privateKey = process.env.AGENT_PRIVATE_KEY;
if (!privateKey) throw new Error('Set AGENT_PRIVATE_KEY in .env first!');
await mintAndList(privateKey, '0.5'); // List at 0.5 ETH
`.trim();

      return {
        content: [
          {
            type: 'text',
            text: `Complete mint + list code:\n\n\`\`\`typescript\n${code}\n\`\`\`\n\nEscrow Contract: ${ESCROW_CONTRACT}\nMarketplace: https://chainhost.online/clawphunks\n\nRequires:\n- $1.99 USDC on Base (for mint)\n- ~$0.12 ETH on L1 (for listing gas)`,
          },
        ],
      };
    }

    default:
      return {
        content: [
          {
            type: 'text',
            text: `Unknown tool: ${name}`,
          },
        ],
        isError: true,
      };
  }
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('ClawPhunks MCP server running');
}

main().catch(console.error);
