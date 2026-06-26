#!/usr/bin/env node

/**
 * Verify a wallet on Farcaster using EIP-712.
 *
 * Links an Ethereum wallet to a Farcaster account so AgentCast
 * can match it against the ERC-8004 registry.
 *
 * Usage:
 *   PRIVATE_KEY=0x... node verify-wallet-on-farcaster.mjs \
 *     --signer-uuid <uuid> --fid <fid>
 *
 * Options:
 *   --signer-uuid     Farcaster signer UUID (required)
 *   --fid             Farcaster FID (required)
 *   --neynar-api-key  Neynar API key (optional - uses AgentCast proxy by default)
 *   --rpc             Custom Optimism RPC URL (default: public)
 *
 * Environment:
 *   PRIVATE_KEY       Private key of the wallet to verify (required)
 *   NEYNAR_API_KEY    Neynar API key (optional - uses AgentCast proxy by default)
 */

import { createPublicClient, http } from "viem";
import { optimism } from "viem/chains";
import { privateKeyToAccount } from "viem/accounts";

const AGENTCAST_PROXY = "https://ac.800.works/api/neynar/verification";

// ── Parse args ───────────────────────────────────────────────────────

function parseArgs(argv) {
  const args = {};
  let i = 2;
  while (i < argv.length) {
    const flag = argv[i];
    const val = argv[i + 1];
    if (val === undefined && flag.startsWith("--")) {
      console.error(`Missing value for ${flag}`);
      process.exit(1);
    }
    switch (flag) {
      case "--signer-uuid":
        args.signerUuid = val;
        i += 2;
        break;
      case "--fid":
        args.fid = Number(val);
        i += 2;
        break;
      case "--neynar-api-key":
        args.neynarApiKey = val;
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

const privateKey = process.env.PRIVATE_KEY;
if (!privateKey) {
  console.error("Error: PRIVATE_KEY environment variable is required");
  process.exit(1);
}

if (!args.signerUuid) {
  console.error("Error: --signer-uuid is required");
  process.exit(1);
}

if (!args.fid) {
  console.error("Error: --fid is required");
  process.exit(1);
}

// ── Determine endpoint ───────────────────────────────────────────────

const neynarApiKey = args.neynarApiKey || process.env.NEYNAR_API_KEY;
const useProxy = !neynarApiKey;

// ── Verify ───────────────────────────────────────────────────────────

const account = privateKeyToAccount(
  privateKey.startsWith("0x") ? privateKey : `0x${privateKey}`
);
const rpcUrl = args.rpc || "https://mainnet.optimism.io";

console.log(`\nVerifying wallet on Farcaster (EIP-712)...`);
console.log(`Wallet:  ${account.address}`);
console.log(`FID:     ${args.fid}`);
console.log(`Via:     ${useProxy ? "AgentCast proxy" : "Neynar direct"}\n`);

try {
  // 1. Get latest finalized Optimism block hash
  const client = createPublicClient({
    chain: optimism,
    transport: http(rpcUrl),
  });
  const block = await client.getBlock({ blockTag: "finalized" });
  const blockHash = block.hash;

  // 2. EIP-712 domain and types (Farcaster spec)
  const domain = {
    name: "Farcaster Verify Ethereum Address",
    version: "2.0.0",
    salt: "0xf2d857f4a3edcb9b78b4d503bfe733db1e3f6cdc2b7971ee739626c97e86a558",
  };

  const types = {
    VerificationClaim: [
      { name: "fid", type: "uint256" },
      { name: "address", type: "address" },
      { name: "blockHash", type: "bytes32" },
      { name: "network", type: "uint8" },
    ],
  };

  // 3. Sign the verification claim
  const signature = await account.signTypedData({
    domain,
    types,
    primaryType: "VerificationClaim",
    message: {
      fid: BigInt(args.fid),
      address: account.address,
      blockHash,
      network: 1, // Farcaster mainnet
    },
  });

  // 4. Submit verification
  const payload = {
    signer_uuid: args.signerUuid,
    address: account.address,
    block_hash: blockHash,
    eth_signature: signature,
    verification_type: 1,
    chain_id: 10, // Optimism
  };

  const url = useProxy
    ? AGENTCAST_PROXY
    : "https://api.neynar.com/v2/farcaster/user/verification";

  const headers = { "Content-Type": "application/json" };
  if (!useProxy) {
    headers["x-api-key"] = neynarApiKey;
  }

  const resp = await fetch(url, {
    method: "POST",
    headers,
    body: JSON.stringify(payload),
  });

  const result = await resp.json();
  if (resp.ok) {
    console.log(`✅ Wallet verified on Farcaster: ${account.address}`);
    console.log(
      `   This wallet is now linked to FID ${args.fid} and will be matched by AgentCast.`
    );
  } else {
    console.error(`❌ Verification failed:`, JSON.stringify(result, null, 2));
    process.exit(1);
  }
} catch (err) {
  console.error("\n❌ Verification failed:", err.shortMessage || err.message);
  process.exit(1);
}
