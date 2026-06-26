#!/usr/bin/env npx tsx
/**
 * A.I. Cheese CLI — Send paid messages to humans via aicheese.app
 * 
 * Usage:
 *   npx tsx ai-cheese.ts search [--location X] [--skills X] [--max-price X]
 *   npx tsx ai-cheese.ts send --to <userId> --message "..."
 *   npx tsx ai-cheese.ts replies [--since <timestamp>]
 *   npx tsx ai-cheese.ts webhook --url <url> [--secret <secret>]
 */

import { ethers } from 'ethers';

const SERVER = process.env.AICHEESE_SERVER || 'https://aicheese.app';
const AGENT_KEY = process.env.AGENT_PRIVATE_KEY;
const AGENT_ID = process.env.AGENT_ID || 'clawdbot-agent';
const AGENT_LABEL = process.env.AGENT_LABEL || '🤖 Clawdbot Agent';

const USDC_ADDRESS = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913';
const USDC_ABI = [
  'function transfer(address to, uint256 amount) returns (bool)',
  'function balanceOf(address) view returns (uint256)',
];

function parseArgs(args: string[]): Record<string, string> {
  const result: Record<string, string> = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].slice(2);
      const val = args[i + 1] && !args[i + 1].startsWith('--') ? args[++i] : 'true';
      result[key] = val;
    }
  }
  return result;
}

async function search(opts: Record<string, string>) {
  const params = new URLSearchParams();
  if (opts.location) params.set('location', opts.location);
  if (opts.lat) params.set('lat', opts.lat);
  if (opts.lng) params.set('lng', opts.lng);
  if (opts.radius) params.set('radius', opts.radius);
  if (opts.skills) params.set('skills', opts.skills);
  if (opts['max-price']) params.set('maxPrice', opts['max-price']);
  if (opts.limit) params.set('limit', opts.limit);

  const res = await fetch(`${SERVER}/api/v1/directory?${params}`);
  const data = await res.json();

  if (data.profiles.length === 0) {
    console.log('No humans found matching your criteria.');
    return;
  }

  console.log(`Found ${data.total} humans:\n`);
  for (const p of data.profiles) {
    console.log(`  ${p.displayName} (${p.id})`);
    if (p.location) console.log(`    📍 ${p.location}${p.distance ? ` (${p.distance.toFixed(1)}km)` : ''}`);
    if (p.bio) console.log(`    ${p.bio.slice(0, 80)}`);
    if (p.skills?.length) console.log(`    🏷️  ${p.skills.join(', ')}`);
    console.log(`    💰 $${p.pricePerMessage}/msg\n`);
  }
}

async function send(opts: Record<string, string>) {
  if (!AGENT_KEY) { console.error('Set AGENT_PRIVATE_KEY'); process.exit(1); }
  if (!opts.to || !opts.message) { console.error('Usage: send --to <userId> --message "..."'); process.exit(1); }

  const provider = new ethers.JsonRpcProvider('https://mainnet.base.org');
  const wallet = new ethers.Wallet(AGENT_KEY, provider);

  const msg: any = {
    toUserId: opts.to,
    fromAgentId: opts['agent-id'] || AGENT_ID,
    fromLabel: opts['agent-label'] || AGENT_LABEL,
    content: opts.message,
  };
  if (opts.thread) msg.threadId = opts.thread;

  // Step 1: Get payment requirements
  console.log(`Sending to ${opts.to}...`);
  const firstTry = await fetch(`${SERVER}/api/v1/message`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(msg),
  });

  if (firstTry.status === 200) {
    const result = await firstTry.json();
    console.log(`✅ Delivered (no payment needed): ${result.messageId}`);
    return;
  }

  if (firstTry.status !== 402) {
    const err = await firstTry.json().catch(() => ({}));
    console.error(`❌ Error ${firstTry.status}: ${err.error || 'Unknown'}`);
    process.exit(1);
  }

  const requirements = await firstTry.json();
  const payTo = requirements.accepts[0].payTo;
  const amount = BigInt(requirements.accepts[0].maxAmountRequired);
  const amountUsd = Number(amount) / 1e6;

  console.log(`  Payment required: $${amountUsd.toFixed(2)} USDC to ${payTo}`);

  // Step 2: Pay USDC
  const usdc = new ethers.Contract(USDC_ADDRESS, USDC_ABI, wallet);
  console.log(`  Sending USDC...`);
  const tx = await usdc.transfer(payTo, amount);
  console.log(`  TX: ${tx.hash}`);
  await tx.wait();
  console.log(`  ✅ Payment confirmed`);

  // Step 3: Retry with payment proof
  const secondTry = await fetch(`${SERVER}/api/v1/message`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-Payment': tx.hash },
    body: JSON.stringify(msg),
  });

  const result = await secondTry.json();
  if (result.ok) {
    console.log(`\n✅ Message delivered! ID: ${result.messageId}`);
    console.log(`   Thread: ${result.threadId} (use --thread ${result.threadId} for follow-ups)`);
  } else {
    console.error(`\n❌ Delivery failed: ${result.error}`);
  }
}

async function replies(opts: Record<string, string>) {
  const params = new URLSearchParams({ agentId: opts['agent-id'] || AGENT_ID });
  if (opts.since) params.set('since', opts.since);

  const res = await fetch(`${SERVER}/api/v1/agent/replies?${params}`);
  const data = await res.json();

  if (data.replies.length === 0) {
    console.log('No replies yet.');
    return;
  }

  console.log(`${data.replies.length} replies:\n`);
  for (const r of data.replies) {
    console.log(`  Message ${r.messageId}:`);
    console.log(`    You asked: "${r.content.slice(0, 60)}..."`);
    console.log(`    Reply: "${r.replyContent}"`);
    if (r.replyAttachments?.length) {
      console.log(`    📷 Attachments: ${r.replyAttachments.map((a: string) => `${SERVER}${a}`).join(', ')}`);
    }
    console.log(`    Paid: $${r.amountPaid} | ${new Date(r.replyAt).toLocaleString()}\n`);
  }
}

async function webhook(opts: Record<string, string>) {
  if (!opts.url) { console.error('Usage: webhook --url <url> [--secret <secret>]'); process.exit(1); }

  const res = await fetch(`${SERVER}/api/v1/agent/webhook`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      agentId: opts['agent-id'] || AGENT_ID,
      url: opts.url,
      secret: opts.secret,
    }),
  });

  const data = await res.json();
  console.log(data.ok ? `✅ Webhook registered for ${opts.url}` : `❌ Error: ${data.error}`);
}

async function balance() {
  if (!AGENT_KEY) { console.error('Set AGENT_PRIVATE_KEY'); process.exit(1); }
  const provider = new ethers.JsonRpcProvider('https://mainnet.base.org');
  const wallet = new ethers.Wallet(AGENT_KEY, provider);
  const usdc = new ethers.Contract(USDC_ADDRESS, USDC_ABI, wallet);
  const bal = Number(await usdc.balanceOf(wallet.address)) / 1e6;
  const eth = Number(await provider.getBalance(wallet.address)) / 1e18;
  console.log(`Wallet: ${wallet.address}`);
  console.log(`  USDC: $${bal.toFixed(2)}`);
  console.log(`  ETH:  ${eth.toFixed(6)}`);
}

// Main
const [command, ...rest] = process.argv.slice(2);
const opts = parseArgs(rest);

switch (command) {
  case 'search': search(opts); break;
  case 'send': send(opts); break;
  case 'replies': replies(opts); break;
  case 'webhook': webhook(opts); break;
  case 'balance': balance(); break;
  default:
    console.log(`A.I. Cheese CLI — Send paid messages to humans

Commands:
  search   [--location X] [--skills X] [--max-price X]  Search for humans
  send     --to <id> --message "..." [--thread <id>]       Send a paid message (thread for follow-ups)
  replies  [--since <timestamp>]                         Check for replies
  webhook  --url <url> [--secret <s>]                    Register webhook
  balance                                                Check wallet balance

Environment:
  AGENT_PRIVATE_KEY  Wallet private key (funded with USDC on Base)
  AGENT_ID           Your agent identifier (default: clawdbot-agent)
  AGENT_LABEL        Display name for messages (default: 🤖 Clawdbot Agent)
  AICHEESE_SERVER    API base URL (default: https://aicheese.app)`);
}
