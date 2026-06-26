#!/usr/bin/env node

/**
 * Register an AI agent on the ERC-8004 Identity Registry (Base).
 *
 * Usage:
 *   PRIVATE_KEY=0x... node register-erc8004.mjs --name "MyAgent" --description "What it does" --image "https://..." [--service "Farcaster=https://farcaster.xyz/username"]
 *
 * Options:
 *   --name         Agent name (required)
 *   --description  Agent description (required)
 *   --image        Public image URL for agent avatar (CORS-free public URL required)
 *   --service      Service endpoint in "name=url" format (repeatable)
 *   --rpc          Custom RPC URL (default: https://base-rpc.publicnode.com)
 *
 * Environment:
 *   PRIVATE_KEY    Wallet private key with ETH on Base (~0.001 ETH for gas)
 */

import {
  createWalletClient,
  createPublicClient,
  http,
  decodeEventLog,
} from "viem";
import { base } from "viem/chains";
import { privateKeyToAccount } from "viem/accounts";

const ERC8004_ADDRESS = "0x8004A169FB4a3325136EB29fA0ceB6D2e539a432";

const ERC8004_ABI = [
  {
    name: "register",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [{ name: "agentURI", type: "string" }],
    outputs: [{ name: "agentId", type: "uint256" }],
  },
  {
    name: "Registered",
    type: "event",
    inputs: [
      { name: "agentId", type: "uint256", indexed: true },
      { name: "agentURI", type: "string", indexed: false },
      { name: "owner", type: "address", indexed: true },
    ],
  },
];

// ── Parse args ───────────────────────────────────────────────────────

function parseArgs(argv) {
  const args = { services: [] };
  let i = 2;
  while (i < argv.length) {
    const flag = argv[i];
    const val = argv[i + 1];
    if (val === undefined && flag.startsWith("--")) {
      console.error(`Missing value for ${flag}`);
      process.exit(1);
    }
    switch (flag) {
      case "--name":
        args.name = val;
        i += 2;
        break;
      case "--description":
        args.description = val;
        i += 2;
        break;
      case "--image":
        args.image = val;
        i += 2;
        break;
      case "--service":
        if (!val.includes("=")) {
          console.error(`Invalid --service format: "${val}" (expected name=url)`);
          process.exit(1);
        }
        const [sName, ...rest] = val.split("=");
        args.services.push({ name: sName, endpoint: rest.join("=") });
        i += 2;
        break;
      case "--rpc":
        args.rpc = val;
        i += 2;
        break;
      default:
        console.error(`Unknown flag: ${flag}`);
        process.exit(1);
    }
  }
  return args;
}

const args = parseArgs(process.argv);

if (!args.name || !args.description) {
  console.error(
    "Usage: PRIVATE_KEY=0x... node register-erc8004.mjs --name <name> --description <desc> [--image <url>] [--service name=url]"
  );
  process.exit(1);
}

const privateKey = process.env.PRIVATE_KEY;
if (!privateKey) {
  console.error("Error: PRIVATE_KEY environment variable is required");
  process.exit(1);
}

// ── Build metadata ───────────────────────────────────────────────────

const metadata = {
  type: "https://eips.ethereum.org/EIPS/eip-8004#registration-v1",
  name: args.name,
  description: args.description,
  ...(args.image && { image: args.image }),
  ...(args.services.length > 0 && { services: args.services }),
  active: true,
};

const agentURI = `data:application/json;base64,${Buffer.from(JSON.stringify(metadata)).toString("base64")}`;

// ── Register ─────────────────────────────────────────────────────────

const rpcUrl = args.rpc || "https://base-rpc.publicnode.com";
const account = privateKeyToAccount(
  privateKey.startsWith("0x") ? privateKey : `0x${privateKey}`
);

const walletClient = createWalletClient({
  account,
  chain: base,
  transport: http(rpcUrl),
});

const publicClient = createPublicClient({
  chain: base,
  transport: http(rpcUrl),
});

console.log(`\nRegistering agent "${args.name}" on ERC-8004 (Base)...`);
console.log(`Wallet: ${account.address}\n`);

try {
  const hash = await walletClient.writeContract({
    address: ERC8004_ADDRESS,
    abi: ERC8004_ABI,
    functionName: "register",
    args: [agentURI],
  });

  console.log(`Tx sent: ${hash}`);
  console.log("Waiting for confirmation...\n");

  const receipt = await publicClient.waitForTransactionReceipt({ hash });

  // Extract agentId from Registered event
  let agentId = null;
  for (const log of receipt.logs) {
    if (log.address.toLowerCase() !== ERC8004_ADDRESS.toLowerCase()) continue;
    try {
      const decoded = decodeEventLog({
        abi: ERC8004_ABI,
        data: log.data,
        topics: log.topics,
      });
      if (decoded.eventName === "Registered") {
        agentId = Number(decoded.args.agentId);
      }
    } catch {
      // Not our event
    }
  }

  if (agentId !== null) {
    console.log(`✅ Registered! Agent ID: ${agentId}`);
    console.log(`   Tx: https://basescan.org/tx/${hash}`);
    console.log(`   Registry: https://basescan.org/address/${ERC8004_ADDRESS}`);
    console.log(
      `\nYour agent is now discoverable on-chain as Agent #${agentId}.`
    );
  } else {
    console.log(`✅ Transaction confirmed but could not parse agentId.`);
    console.log(`   Check tx: https://basescan.org/tx/${hash}`);
  }
} catch (err) {
  console.error("\n❌ Registration failed:", err.shortMessage || err.message);
  if (err.message?.includes("insufficient funds")) {
    console.error(
      "   Send ETH to your wallet on Base. Even 0.001 ETH is enough."
    );
  }
  process.exit(1);
}
