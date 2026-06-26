/**
 * ClawPhunks - NFT Mint Server for AI Agents
 *
 * x402 payment on Base → Ethscription minted on Ethereum L1 + gas stipend
 *
 * Endpoints:
 *   GET  /health      → Health check
 *   GET  /skills      → Agent instructions (mint + trade code)
 *   GET  /collection  → Collection info + rarity data
 *   GET  /listings    → Active marketplace listings with deals
 *   POST /mint        → Mint a random phunk (x402 gated)
 */

import express from 'express';
import cors from 'cors';
import { createPublicClient, http, formatEther } from 'viem';
import { mainnet } from 'viem/chains';
import { paymentMiddleware } from 'x402-express';
import {
  MINT_PRICE_USDC,
  COLLECTION,
  isTestnet,
  padId,
  GAS_STIPEND_WEI,
  ESCROW_CONTRACT,
} from './config.js';
import { mintEthscription } from './mint.js';
import { claimRandomItem, finalizeMint, rollbackMint, getMintedCount, getAvailableCount } from './db.js';
import { verify as facilitatorVerify, settle as facilitatorSettle } from './facilitator.js';

const app = express();

app.use(cors());
app.use(express.json());

// ─── Health ───────────────────────────────────────────────────────────────────

app.get('/health', (_req, res) => {
  res.json({ status: 'ok', service: 'clawphunks' });
});

// ─── Skills (Agent-readable JSON) ─────────────────────────────────────────────

app.get('/skills', (_req, res) => {
  const mintCode = `
import { createWalletClient, createPublicClient, http, keccak256, encodePacked } from 'viem';
import { base } from 'viem/chains';
import { privateKeyToAccount } from 'viem/accounts';
import { Buffer } from 'buffer';
import 'dotenv/config';

const MINT_API = 'https://clawphunks.vercel.app/mint';
const USDC_BASE = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913';
const MINT_COST = 1990000n; // 1.99 USDC (6 decimals)

// Check USDC balance before minting
async function checkBalance(address) {
  const publicClient = createPublicClient({ chain: base, transport: http('https://mainnet.base.org') });
  const balance = await publicClient.readContract({
    address: USDC_BASE,
    abi: [{ name: 'balanceOf', type: 'function', stateMutability: 'view', inputs: [{ name: 'account', type: 'address' }], outputs: [{ type: 'uint256' }] }],
    functionName: 'balanceOf',
    args: [address],
  });
  return balance;
}

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

  if (reqRes.status !== 402) {
    const err = await reqRes.json();
    throw new Error(err.error || 'Expected 402 payment required');
  }

  const paymentReqs = await reqRes.json();
  if (!paymentReqs.accepts || !paymentReqs.accepts[0]) {
    throw new Error('Invalid payment requirements');
  }
  const accept = paymentReqs.accepts[0];

  // Step 2: Sign EIP-3009 TransferWithAuthorization
  const nonce = keccak256(encodePacked(['address', 'uint256'], [account.address, BigInt(Date.now())]));
  const now = Math.floor(Date.now() / 1000);
  const validAfter = BigInt(now - 5);
  const validBefore = BigInt(now + 120); // 2 min window

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

  const result = await mintRes.json();
  if (!result.success) {
    throw new Error(result.error || 'Mint failed');
  }
  return result;
}

// Rarity data - check if you got something valuable!
const RARE_TYPES = {
  aliens: [635, 2890, 3100, 3443, 5822, 5905, 6089, 7523, 7804],
  apes: [372, 1021, 2140, 2243, 2386, 2460, 2491, 2711, 2924, 4156, 4178, 4464, 5217, 5314, 5577, 5795, 6145, 6915, 6965, 7191, 8219, 8498, 9265, 9280],
  zombies: [117, 987, 1119, 1190, 1374, 1478, 1526, 1658, 1748, 1886, 1935, 2066, 2132, 2249, 2306, 2329, 2338, 2424, 2484, 2560, 2566, 2681, 2708, 2938, 2967, 3211, 3328, 3393, 3489, 3493, 3609, 3636, 3831, 4472, 4513, 4559, 4747, 4830, 4850, 4874, 5066, 5234, 5253, 5299, 5312, 5336, 5412, 5489, 5573, 5742, 5761, 5944, 6275, 6297, 6304, 6491, 6515, 6586, 6649, 6704, 6784, 7014, 7121, 7127, 7252, 7337, 7458, 7660, 7756, 7914, 8127, 8307, 8386, 8472, 8531, 8553, 8780, 8857, 8909, 8957, 9203, 9368, 9474, 9804, 9838, 9909, 9955, 9997],
};

function checkRarity(tokenId) {
  if (RARE_TYPES.aliens.includes(tokenId)) return { type: 'Alien', rarity: 'LEGENDARY' };
  if (RARE_TYPES.apes.includes(tokenId)) return { type: 'Ape', rarity: 'RARE' };
  if (RARE_TYPES.zombies.includes(tokenId)) return { type: 'Zombie', rarity: 'UNCOMMON' };
  return { type: 'Common', rarity: 'COMMON' };
}

// Main
const privateKey = process.env.AGENT_PRIVATE_KEY;
if (!privateKey) { console.error('Set AGENT_PRIVATE_KEY in .env'); process.exit(1); }

const account = privateKeyToAccount(privateKey);
console.log('Wallet:', account.address);

const balance = await checkBalance(account.address);
console.log('USDC Balance:', Number(balance) / 1e6);

if (balance < MINT_COST) {
  console.log('Insufficient USDC. Need 1.99 USDC on Base.');
  console.log('Fund:', account.address);
  process.exit(1);
}

const result = await mintClawPhunk(privateKey, account.address);
console.log('Minted ClawPhunk #' + result.tokenId);
console.log('TX:', result.txHash);
console.log('Ethscription ID:', result.ethscriptionId); // Same as txHash - use this for listing

const rarity = checkRarity(result.tokenId);
console.log('Type:', rarity.type, '| Rarity:', rarity.rarity);

if (rarity.rarity !== 'COMMON') {
  console.log('You got a rare one! Consider holding or pricing at a premium.');
}
`.trim();

  // Listing script - transfers ethscription to escrow then lists for sale (2 txs)
  const listingCode = `
import { createWalletClient, createPublicClient, http, formatEther, parseEther, encodeFunctionData } from 'viem';
import { mainnet } from 'viem/chains';
import { privateKeyToAccount } from 'viem/accounts';
import 'dotenv/config';

const ESCROW = '0x3e67d49716e50a8b1c71b8dEa0e31755305733fd';
const ESCROW_ABI = [
  { name: 'depositAndList', type: 'function', stateMutability: 'nonpayable', inputs: [{ name: 'ethscriptionId', type: 'bytes32' }, { name: 'price', type: 'uint256' }], outputs: [] },
  { name: 'getListing', type: 'function', stateMutability: 'view', inputs: [{ name: 'ethscriptionId', type: 'bytes32' }], outputs: [{ name: 'active', type: 'bool' }, { name: 'seller', type: 'address' }, { name: 'price', type: 'uint256' }] },
];

// === CONFIGURE THESE ===
const ETHSCRIPTION_ID = '0x...'; // The tx hash from your mint result
const LISTING_PRICE_ETH = '0.05'; // Your chosen price in ETH

const privateKey = process.env.AGENT_PRIVATE_KEY;
if (!privateKey) { console.error('Set AGENT_PRIVATE_KEY in .env'); process.exit(1); }

const account = privateKeyToAccount(privateKey);
const publicClient = createPublicClient({ chain: mainnet, transport: http('https://1rpc.io/eth') });
const walletClient = createWalletClient({ account, chain: mainnet, transport: http('https://1rpc.io/eth') });

console.log('Listing ClawPhunk...');
console.log('Wallet:', account.address);
console.log('Ethscription:', ETHSCRIPTION_ID);
console.log('Price:', LISTING_PRICE_ETH, 'ETH');

// Check ETH balance for gas (~0.00003 ETH per tx)
const balance = await publicClient.getBalance({ address: account.address });
console.log('ETH Balance:', formatEther(balance), 'ETH');
if (balance < 30000000000000n) { // 0.00003 ETH minimum
  console.error('Need ETH for gas. Fund:', account.address);
  process.exit(1);
}

// Step 1: Transfer ethscription to escrow (send tx with ethscription ID as calldata)
console.log('\\nStep 1: Transferring ethscription to escrow...');
const transferHash = await walletClient.sendTransaction({
  to: ESCROW,
  value: 0n,
  data: ETHSCRIPTION_ID,
});
console.log('Transfer TX:', transferHash);
await publicClient.waitForTransactionReceipt({ hash: transferHash });
console.log('Transfer confirmed!');

// Step 2: Call depositAndList to register deposit and set price
console.log('\\nStep 2: Registering listing with price...');
const listHash = await walletClient.writeContract({
  address: ESCROW,
  abi: ESCROW_ABI,
  functionName: 'depositAndList',
  args: [ETHSCRIPTION_ID, parseEther(LISTING_PRICE_ETH)],
});
console.log('List TX:', listHash);
await publicClient.waitForTransactionReceipt({ hash: listHash });

console.log('\\nListed successfully at', LISTING_PRICE_ETH, 'ETH!');
console.log('View marketplace: https://chainhost.online/clawphunks');
`.trim();

  // Transfer script - sends ethscription to another address
  const transferCode = `
import { createWalletClient, createPublicClient, http, formatEther } from 'viem';
import { mainnet } from 'viem/chains';
import { privateKeyToAccount } from 'viem/accounts';
import 'dotenv/config';

// === CONFIGURE THESE ===
const ETHSCRIPTION_ID = '0x...'; // The tx hash of your ethscription
const RECIPIENT = '0x...'; // Address to send to

const privateKey = process.env.AGENT_PRIVATE_KEY;
if (!privateKey) { console.error('Set AGENT_PRIVATE_KEY in .env'); process.exit(1); }

const account = privateKeyToAccount(privateKey);
const publicClient = createPublicClient({ chain: mainnet, transport: http('https://1rpc.io/eth') });
const walletClient = createWalletClient({ account, chain: mainnet, transport: http('https://1rpc.io/eth') });

console.log('Transferring ethscription...');
console.log('From:', account.address);
console.log('To:', RECIPIENT);
console.log('Ethscription:', ETHSCRIPTION_ID);

// Check ETH balance for gas (~0.00005 ETH for simple calldata tx)
const balance = await publicClient.getBalance({ address: account.address });
console.log('ETH Balance:', formatEther(balance), 'ETH');
if (balance < 50000000000000n) { // 0.00005 ETH minimum
  console.error('Need ~0.00005 ETH for gas. Fund:', account.address);
  process.exit(1);
}

// Transfer ethscription by sending 0 ETH tx with ethscription ID as calldata
const hash = await walletClient.sendTransaction({
  to: RECIPIENT,
  value: 0n,
  data: ETHSCRIPTION_ID,
});
console.log('TX:', hash);

const receipt = await publicClient.waitForTransactionReceipt({ hash });
console.log(receipt.status === 'success' ? 'Transferred!' : 'Failed!');
console.log('View: https://ethscriptions.com/ethscriptions/' + ETHSCRIPTION_ID);
`.trim();

  // Rescue/cancel script - withdraws ethscription from escrow
  const rescueCode = `
import { createWalletClient, createPublicClient, http, formatEther } from 'viem';
import { mainnet } from 'viem/chains';
import { privateKeyToAccount } from 'viem/accounts';
import 'dotenv/config';

const ESCROW = '0x3e67d49716e50a8b1c71b8dEa0e31755305733fd';
const ESCROW_ABI = [
  { name: 'cancelAndWithdraw', type: 'function', stateMutability: 'nonpayable', inputs: [{ name: 'ethscriptionId', type: 'bytes32' }], outputs: [] },
  { name: 'getListing', type: 'function', stateMutability: 'view', inputs: [{ name: 'ethscriptionId', type: 'bytes32' }], outputs: [{ name: 'active', type: 'bool' }, { name: 'seller', type: 'address' }, { name: 'price', type: 'uint256' }] },
  { name: 'depositors', type: 'function', stateMutability: 'view', inputs: [{ name: '', type: 'bytes32' }], outputs: [{ type: 'address' }] },
];

// === CONFIGURE THIS ===
const ETHSCRIPTION_ID = '0x...'; // The tx hash of your listed ethscription

const privateKey = process.env.AGENT_PRIVATE_KEY;
if (!privateKey) { console.error('Set AGENT_PRIVATE_KEY in .env'); process.exit(1); }

const account = privateKeyToAccount(privateKey);
const publicClient = createPublicClient({ chain: mainnet, transport: http('https://1rpc.io/eth') });
const walletClient = createWalletClient({ account, chain: mainnet, transport: http('https://1rpc.io/eth') });

console.log('Cancelling listing and withdrawing...');
console.log('Wallet:', account.address);
console.log('Ethscription:', ETHSCRIPTION_ID);

// Check if you're the depositor
const depositor = await publicClient.readContract({ address: ESCROW, abi: ESCROW_ABI, functionName: 'depositors', args: [ETHSCRIPTION_ID] });
if (depositor === '0x0000000000000000000000000000000000000000') {
  console.log('Not deposited in escrow.'); process.exit(0);
}
if (depositor.toLowerCase() !== account.address.toLowerCase()) {
  console.error('You are not the depositor!');
  process.exit(1);
}

// Check ETH balance for gas
const balance = await publicClient.getBalance({ address: account.address });
console.log('ETH Balance:', formatEther(balance), 'ETH');
if (balance < 50000000000000n) {
  console.error('Need ~0.00005 ETH for gas. Fund:', account.address);
  process.exit(1);
}

// Cancel and withdraw
const hash = await walletClient.writeContract({ address: ESCROW, abi: ESCROW_ABI, functionName: 'cancelAndWithdraw', args: [ETHSCRIPTION_ID] });
console.log('TX:', hash);

const receipt = await publicClient.waitForTransactionReceipt({ hash });
console.log(receipt.status === 'success' ? 'Withdrawn! Ethscription returned to your wallet.' : 'Failed!');
`.trim();

  // Buy script - purchases a listed ethscription
  const buyCode = `
import { createWalletClient, createPublicClient, http, formatEther } from 'viem';
import { mainnet } from 'viem/chains';
import { privateKeyToAccount } from 'viem/accounts';
import 'dotenv/config';

const ESCROW = '0x3e67d49716e50a8b1c71b8dEa0e31755305733fd';
const ESCROW_ABI = [
  { name: 'buy', type: 'function', stateMutability: 'payable', inputs: [{ name: 'ethscriptionId', type: 'bytes32' }], outputs: [] },
  { name: 'getListing', type: 'function', stateMutability: 'view', inputs: [{ name: 'ethscriptionId', type: 'bytes32' }], outputs: [{ name: 'active', type: 'bool' }, { name: 'seller', type: 'address' }, { name: 'price', type: 'uint256' }] },
];

// === CONFIGURE THIS ===
const ETHSCRIPTION_ID = '0x...'; // The tx hash of the ethscription to buy

const privateKey = process.env.AGENT_PRIVATE_KEY;
if (!privateKey) { console.error('Set AGENT_PRIVATE_KEY in .env'); process.exit(1); }

const account = privateKeyToAccount(privateKey);
const publicClient = createPublicClient({ chain: mainnet, transport: http('https://1rpc.io/eth') });
const walletClient = createWalletClient({ account, chain: mainnet, transport: http('https://1rpc.io/eth') });

console.log('Buying ClawPhunk...');
console.log('Wallet:', account.address);
console.log('Ethscription:', ETHSCRIPTION_ID);

// Check listing
const listing = await publicClient.readContract({ address: ESCROW, abi: ESCROW_ABI, functionName: 'getListing', args: [ETHSCRIPTION_ID] });
const [active, seller, price] = listing;
if (!active) { console.log('Not for sale!'); process.exit(1); }

console.log('Seller:', seller);
console.log('Price:', formatEther(price), 'ETH');

// Check ETH balance (need price + gas)
const balance = await publicClient.getBalance({ address: account.address });
console.log('Your ETH Balance:', formatEther(balance), 'ETH');
if (balance < price + 100000000000000n) {
  console.error('Need', formatEther(price), '+ gas ETH. Fund:', account.address);
  process.exit(1);
}

// Buy it
const hash = await walletClient.writeContract({ address: ESCROW, abi: ESCROW_ABI, functionName: 'buy', args: [ETHSCRIPTION_ID], value: price });
console.log('TX:', hash);
await publicClient.waitForTransactionReceipt({ hash });
console.log('Purchased! Ethscription is now yours.');
`.trim();

  res.json({
    name: 'ClawPhunks',
    description: 'NFT collection for AI agents. Mint, trade, and collect rare phunks.',
    marketplace: 'https://chainhost.online/clawphunks',
    escrowContract: '0x3e67d49716e50a8b1c71b8dEa0e31755305733fd',
    mintPrice: '1.99 USDC',
    mintEndpoint: 'POST https://clawphunks.vercel.app/mint',
    strategy: {
      overview: 'Rarity drives value. Check /listings to see current market prices before deciding.',
      legendary: 'Aliens (9 total, 0.09%) - Extremely rare. Consider holding or pricing at a premium.',
      rare: 'Apes (24 total, 0.24%) - Very rare. High value, price accordingly.',
      uncommon: 'Zombies (88 total, 0.88%) - Uncommon. Worth more than common types.',
      common: 'Male/Female types are common. Price competitively or use funds to buy rare types.',
      tips: [
        'Check /listings to see what others are asking',
        'Undercut slightly to sell faster, or price higher and wait',
        'Look for underpriced rare types to flip for profit',
        'Consider holding rare types for appreciation',
      ],
    },
    rarity: {
      aliens: [635, 2890, 3100, 3443, 5822, 5905, 6089, 7523, 7804],
      apes: [372, 1021, 2140, 2243, 2386, 2460, 2491, 2711, 2924, 4156, 4178, 4464, 5217, 5314, 5577, 5795, 6145, 6915, 6965, 7191, 8219, 8498, 9265, 9280],
      zombies: [117, 987, 1119, 1190, 1374, 1478, 1526, 1658, 1748, 1886, 1935, 2066, 2132, 2249, 2306, 2329, 2338, 2424, 2484, 2560, 2566, 2681, 2708, 2938, 2967, 3211, 3328, 3393, 3489, 3493, 3609, 3636, 3831, 4472, 4513, 4559, 4747, 4830, 4850, 4874, 5066, 5234, 5253, 5299, 5312, 5336, 5412, 5489, 5573, 5742, 5761, 5944, 6275, 6297, 6304, 6491, 6515, 6586, 6649, 6704, 6784, 7014, 7121, 7127, 7252, 7337, 7458, 7660, 7756, 7914, 8127, 8307, 8386, 8472, 8531, 8553, 8780, 8857, 8909, 8957, 9203, 9368, 9474, 9804, 9838, 9909, 9955, 9997],
    },
    walletSetup: {
      important: 'Save your private key to .env with .gitignore BEFORE transacting!',
      envVar: 'AGENT_PRIVATE_KEY',
      funding: {
        mint: '1.99 USDC on Base',
        trade: 'ETH on L1 mainnet for gas + purchases',
      },
    },
    scripts: {
      mint: mintCode,
      list: listingCode,
      buy: buyCode,
      transfer: transferCode,
      rescue: rescueCode,
    },
    dependencies: ['viem', 'dotenv'],
    install: 'npm install viem dotenv',

    integrations: {
      langchain: {
        description: 'LangChain tool for minting and trading ClawPhunks',
        install: 'pip install langchain requests',
        source: 'https://github.com/jefdiesel/clawphunks/tree/main/integrations/langchain',
        tools: ['clawphunks_mint', 'clawphunks_collection', 'clawphunks_skills'],
      },
      agentkit: {
        description: 'Coinbase AgentKit action with automatic x402 payment handling',
        install: 'npm install @coinbase/agentkit',
        source: 'https://github.com/jefdiesel/clawphunks/tree/main/integrations/agentkit',
        actions: ['clawphunks_mint', 'clawphunks_collection', 'clawphunks_skills'],
      },
    },
  });
});

// ─── Listings (Marketplace Scanner) ───────────────────────────────────────────

const RARE_IDS = {
  aliens: [635, 2890, 3100, 3443, 5822, 5905, 6089, 7523, 7804],
  apes: [372, 1021, 2140, 2243, 2386, 2460, 2491, 2711, 2924, 4156, 4178, 4464, 5217, 5314, 5577, 5795, 6145, 6915, 6965, 7191, 8219, 8498, 9265, 9280],
  zombies: [117, 987, 1119, 1190, 1374, 1478, 1526, 1658, 1748, 1886, 1935, 2066, 2132, 2249, 2306, 2329, 2338, 2424, 2484, 2560, 2566, 2681, 2708, 2938, 2967, 3211, 3328, 3393, 3489, 3493, 3609, 3636, 3831, 4472, 4513, 4559, 4747, 4830, 4850, 4874, 5066, 5234, 5253, 5299, 5312, 5336, 5412, 5489, 5573, 5742, 5761, 5944, 6275, 6297, 6304, 6491, 6515, 6586, 6649, 6704, 6784, 7014, 7121, 7127, 7252, 7337, 7458, 7660, 7756, 7914, 8127, 8307, 8386, 8472, 8531, 8553, 8780, 8857, 8909, 8957, 9203, 9368, 9474, 9804, 9838, 9909, 9955, 9997],
};

// Rarity tiers for reference (no fixed prices - agents decide based on market)

function getRarity(tokenId: number): { type: string; tier: number } {
  if (RARE_IDS.aliens.includes(tokenId)) return { type: 'alien', tier: 5 };
  if (RARE_IDS.apes.includes(tokenId)) return { type: 'ape', tier: 4 };
  if (RARE_IDS.zombies.includes(tokenId)) return { type: 'zombie', tier: 3 };
  return { type: 'common', tier: 1 };
}

const l1Client = createPublicClient({
  chain: mainnet,
  transport: http(process.env.ETHEREUM_RPC_URL || 'https://eth.llamarpc.com'),
});

const ESCROW_ABI = [
  { name: 'getListing', type: 'function', stateMutability: 'view', inputs: [{ name: 'ethscriptionId', type: 'bytes32' }], outputs: [{ name: 'active', type: 'bool' }, { name: 'seller', type: 'address' }, { name: 'price', type: 'uint256' }] },
  { name: 'ListingCreated', type: 'event', inputs: [{ name: 'ethscriptionId', type: 'bytes32', indexed: true }, { name: 'seller', type: 'address', indexed: true }, { name: 'price', type: 'uint256', indexed: false }] },
] as const;

app.get('/listings', async (_req, res) => {
  try {
    // Get current block and look back ~3 hours (1000 blocks max for free RPCs)
    const currentBlock = await l1Client.getBlockNumber();
    const fromBlock = currentBlock - BigInt(900);

    // Get recent ListingCreated events from escrow contract
    const logs = await l1Client.getLogs({
      address: ESCROW_CONTRACT as `0x${string}`,
      event: {
        type: 'event',
        name: 'ListingCreated',
        inputs: [
          { name: 'ethscriptionId', type: 'bytes32', indexed: true },
          { name: 'seller', type: 'address', indexed: true },
          { name: 'price', type: 'uint256', indexed: false },
        ],
      },
      fromBlock,
    });

    // Check which listings are still active
    const listings: any[] = [];
    const deals: any[] = [];

    for (const log of logs) {
      const ethscriptionId = log.args.ethscriptionId;
      if (!ethscriptionId) continue;

      try {
        const [active, seller, price] = await l1Client.readContract({
          address: ESCROW_CONTRACT as `0x${string}`,
          abi: ESCROW_ABI,
          functionName: 'getListing',
          args: [ethscriptionId],
        });

        if (active) {
          const priceEth = Number(formatEther(price));
          // Extract token ID from ethscription (would need DB lookup in practice)
          // For now, include the ethscriptionId
          const listing = {
            ethscriptionId,
            seller,
            priceEth,
            priceWei: price.toString(),
          };

          listings.push(listing);

          // Check if it's underpriced (deal detection would need tokenId lookup)
        }
      } catch (e) {
        // Skip if contract call fails
      }
    }

    res.json({
      count: listings.length,
      listings,
      deals,
      tip: 'Look for rare types (aliens/apes/zombies) - check rarity in /skills and decide if price is good.',
      rarityTiers: {
        5: 'Alien (legendary)',
        4: 'Ape (rare)',
        3: 'Zombie (uncommon)',
        1: 'Common',
      },
    });
  } catch (err: any) {
    res.status(500).json({ error: err.message });
  }
});

// ─── Collection Info ──────────────────────────────────────────────────────────

app.get('/collection', async (_req, res) => {
  try {
    const [minted, available] = await Promise.all([
      getMintedCount(),
      getAvailableCount(),
    ]);

    const info = {
      name: COLLECTION.name,
      symbol: COLLECTION.symbol,
      description: COLLECTION.description,
      totalSupply: COLLECTION.totalSupply,
      minted,
      available,
      mintPrice: MINT_PRICE_USDC,
      mintCurrency: 'USDC',
      chain: COLLECTION.chain,
      collectionId: process.env.COLLECTION_ID ?? null,
      escrowContract: ESCROW_CONTRACT,
      rarity: {
        types: {
          Alien: { count: 9, percent: 0.09, rank: 5, tokenIds: [635, 2890, 3100, 3443, 5822, 5905, 6089, 7523, 7804] },
          Ape: { count: 24, percent: 0.24, rank: 4, tokenIds: [372, 1021, 2140, 2243, 2386, 2460, 2491, 2711, 2924, 4156, 4178, 4464, 5217, 5314, 5577, 5795, 6145, 6915, 6965, 7191, 8219, 8498, 9265, 9280] },
          Zombie: { count: 88, percent: 0.88, rank: 3, tokenIds: [117, 987, 1119, 1190, 1374, 1478, 1526, 1658, 1748, 1886, 1935, 2066, 2132, 2249, 2306, 2329, 2338, 2424, 2484, 2560, 2566, 2681, 2708, 2938, 2967, 3211, 3328, 3393, 3489, 3493, 3609, 3636, 3831, 4472, 4513, 4559, 4747, 4830, 4850, 4874, 5066, 5234, 5253, 5299, 5312, 5336, 5412, 5489, 5573, 5742, 5761, 5944, 6275, 6297, 6304, 6491, 6515, 6586, 6649, 6704, 6784, 7014, 7121, 7127, 7252, 7337, 7458, 7660, 7756, 7914, 8127, 8307, 8386, 8472, 8531, 8553, 8780, 8857, 8909, 8957, 9203, 9368, 9474, 9804, 9838, 9909, 9955, 9997] },
          Female: { count: 3840, percent: 38.4, rank: 2 },
          Male: { count: 6039, percent: 60.39, rank: 1 },
        },
        rareAccessories: {
          Beanie: 44,
          Choker: 48,
          'Pilot Helmet': 54,
          Tiara: 55,
          'Orange Side': 68,
          'Buck Teeth': 78,
          'Welding Goggles': 86,
          'Top Hat': 115,
          'Cowboy Hat': 142,
        },
        note: 'Rank 5 = legendary, 1 = common. Aliens/Apes/Zombies are highly valuable.',
      },
      agentInstructions: {
        mint: {
          endpoint: 'POST /mint',
          payment: `${MINT_PRICE_USDC} USDC on Base (x402)`,
          body: '{ "recipient": "0xYourAddress" }',
          returns: 'Random unminted phunk + gas stipend. Check rarity.types to see if you got a rare one!',
        },
        trade: {
          contract: ESCROW_CONTRACT,
          chain: 'Ethereum L1',
          list: 'depositAndList(bytes32 ethscriptionId, uint256 priceWei)',
          buy: 'buy(bytes32 ethscriptionId) payable',
          cancel: 'cancelAndWithdraw(bytes32 ethscriptionId)',
        },
        createWallet: `
import { privateKeyToAccount, generatePrivateKey } from 'viem/accounts';
const privateKey = generatePrivateKey();
const account = privateKeyToAccount(privateKey);
// Store privateKey securely, use account.address for minting
        `.trim(),
      },
    };

    res.json(info);
  } catch (err: any) {
    res.status(500).json({ error: err.message });
  }
});

// ─── Self-hosted Facilitator Endpoints ───────────────────────────────────────

app.post('/facilitator/verify', async (req, res) => {
  try {
    const { paymentPayload, paymentRequirements } = req.body;
    const result = await facilitatorVerify(paymentPayload, paymentRequirements);
    res.json(result);
  } catch (err: any) {
    res.json({
      isValid: false,
      invalidReason: 'error',
      invalidMessage: err.message,
    });
  }
});

app.post('/facilitator/settle', async (req, res) => {
  try {
    const { paymentPayload, paymentRequirements } = req.body;
    const result = await facilitatorSettle(paymentPayload, paymentRequirements);
    res.json(result);
  } catch (err: any) {
    res.json({
      success: false,
      error: err.message,
    });
  }
});

// ─── x402 Payment Middleware ──────────────────────────────────────────────────

const payToAddress = (process.env.PAYMENT_RECIPIENT ?? '').trim() as `0x${string}`;

// Use self-hosted facilitator on same server
const facilitatorUrl = (process.env.FACILITATOR_URL ?? 'https://clawphunks.vercel.app/facilitator') as `https://${string}`;

app.use(
  paymentMiddleware(payToAddress, {
    'POST /mint': {
      price: `$${MINT_PRICE_USDC}`,
      network: isTestnet ? 'base-sepolia' : 'base',
      config: {
        description: `ClawPhunks — mint random phunk (${MINT_PRICE_USDC} USDC) + gas stipend`,
      },
    },
  }, {
    url: facilitatorUrl,
  })
);

// ─── Mint (x402 Gated) ────────────────────────────────────────────────────────

app.post('/mint', async (req, res) => {
  try {
    const { recipient } = req.body;

    if (!recipient || !/^0x[0-9a-fA-F]{40}$/.test(recipient)) {
      return res.status(400).json({ error: 'Invalid recipient address' });
    }

    // Claim a random unminted item from Supabase
    const { tokenId, dataURI } = await claimRandomItem(recipient);

    console.log(`[mint] Minting ClawPhunk #${padId(tokenId)} to ${recipient}`);

    // Inscribe to recipient
    const result = await mintEthscription(recipient, dataURI);

    if (!result.success || !result.txHash) {
      // Rollback - mark item as unminted
      await rollbackMint(tokenId);
      return res.status(500).json({ error: result.error ?? 'Mint failed' });
    }

    // Record tx hash
    await finalizeMint(tokenId, result.txHash);

    const response = {
      success: true,
      tokenId,
      txHash: result.txHash,
      ethscriptionId: result.txHash,
      recipient,
      gasStipendWei: GAS_STIPEND_WEI.toString(),
      viewerUrl: `https://ethscriptions.com/ethscriptions/${result.txHash}`,
      nextSteps: {
        trade: `Use escrow contract ${ESCROW_CONTRACT} on L1`,
        list: 'depositAndList(ethscriptionId, priceWei)',
        buy: 'buy(ethscriptionId) with msg.value = price',
      },
    };

    console.log(`[mint] ✓ #${padId(tokenId)} → ${recipient} | tx: ${result.txHash}`);
    res.json(response);
  } catch (err: any) {
    console.error('[mint] error:', err);
    res.status(500).json({ error: err.message ?? 'Mint failed' });
  }
});

// ─── Start ────────────────────────────────────────────────────────────────────

const PORT = parseInt(process.env.PORT ?? '3000', 10);
app.listen(PORT, () => {
  console.log(`\nClawPhunks Mint Server`);
  console.log(`  Port       : ${PORT}`);
  console.log(`  Network    : ${isTestnet ? 'Base Sepolia' : 'Base'} (x402)`);
  console.log(`  Mint       : ${MINT_PRICE_USDC} USDC`);
  console.log(`  Gas stipend: ${Number(GAS_STIPEND_WEI) / 1e18} ETH`);
  console.log(`  Escrow     : ${ESCROW_CONTRACT}\n`);
});

export default app;
