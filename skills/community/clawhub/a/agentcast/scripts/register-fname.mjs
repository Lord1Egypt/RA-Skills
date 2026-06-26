#!/usr/bin/env node

/**
 * Register a Farcaster username (fname) on the Farcaster Name Registry,
 * then set it as UserData on the hub.
 *
 * Use this when:
 * - farcaster-agent's setupFullProfile failed because the fname was taken
 * - You want to register a different fname for an existing FID
 * - You have an FID but never registered an fname (username shows as !<FID>)
 *
 * Usage:
 *   PRIVATE_KEY=0x... SIGNER_KEY=0x... node register-fname.mjs \
 *     --fid <fid> \
 *     --fname <username>
 *
 * Options:
 *   --fid        Farcaster FID (required)
 *   --fname      Username to register (required, lowercase alphanumeric + hyphens, 1-16 chars)
 *   --hub-url    Hub endpoint for UserData message (default: AgentCast proxy)
 *
 * Environment:
 *   PRIVATE_KEY  Custody wallet private key (for EIP-712 fname registration)
 *   SIGNER_KEY   Ed25519 signer private key (for hub UserData message)
 */

import { privateKeyToAccount } from "viem/accounts";
import {
  makeUserDataAdd,
  NobleEd25519Signer,
  FarcasterNetwork,
  UserDataType,
  Message,
} from "@farcaster/core";

const FNAME_REGISTRY = "https://fnames.farcaster.xyz";
const AGENTCAST_HUB_PROXY = "https://ac.800.works/api/neynar/hub";

const FNAME_DOMAIN = {
  name: "Farcaster name verification",
  version: "1",
  chainId: 1,
  verifyingContract: "0xe3Be01D99bAa8dB9905b33a3cA391238234B79D1",
};

const FNAME_TYPES = {
  UserNameProof: [
    { name: "name", type: "string" },
    { name: "timestamp", type: "uint256" },
    { name: "owner", type: "address" },
  ],
};

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
      case "--fid":
        args.fid = Number(val);
        i += 2;
        break;
      case "--fname":
        args.fname = val;
        i += 2;
        break;
      case "--hub-url":
        args.hubUrl = val;
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
const signerKey = process.env.SIGNER_KEY;

if (!privateKey) {
  console.error("Error: PRIVATE_KEY environment variable required (custody wallet private key)");
  process.exit(1);
}
if (!signerKey) {
  console.error("Error: SIGNER_KEY environment variable required (Ed25519 signer private key)");
  process.exit(1);
}
if (!args.fid) {
  console.error("Error: --fid is required");
  process.exit(1);
}
if (!args.fname) {
  console.error("Error: --fname is required");
  process.exit(1);
}

// Validate fname format
if (!/^[a-z0-9][a-z0-9-]{0,15}$/.test(args.fname)) {
  console.error("Error: fname must be lowercase alphanumeric + hyphens, 1-16 chars, cannot start with hyphen");
  process.exit(1);
}

// ── Step 1: Check availability ───────────────────────────────────────

console.log(`\nRegistering fname "${args.fname}" for FID ${args.fid}...\n`);

const checkRes = await fetch(`${FNAME_REGISTRY}/transfers/current?name=${args.fname}`);
if (checkRes.ok) {
  const existing = await checkRes.json();
  if (existing.transfer && existing.transfer.to !== 0) {
    if (existing.transfer.to === args.fid) {
      console.log(`ℹ️  Fname "${args.fname}" already registered to FID ${args.fid}`);
      console.log("   Skipping registry, setting UserData on hub...\n");
    } else {
      console.error(`❌ Fname "${args.fname}" is already taken by FID ${existing.transfer.to}`);
      process.exit(1);
    }
  }
} else if (checkRes.status !== 404) {
  // 404 = name available, anything else is unexpected
  console.warn(`⚠️  Could not check fname availability (HTTP ${checkRes.status}), proceeding anyway...`);
}

// ── Step 2: Register on fnames.farcaster.xyz ─────────────────────────

const account = privateKeyToAccount(privateKey);
const timestamp = Math.floor(Date.now() / 1000);

const signature = await account.signTypedData({
  domain: FNAME_DOMAIN,
  types: FNAME_TYPES,
  primaryType: "UserNameProof",
  message: {
    name: args.fname,
    timestamp: BigInt(timestamp),
    owner: account.address,
  },
});

const regRes = await fetch(`${FNAME_REGISTRY}/transfers`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    name: args.fname,
    from: 0,
    to: args.fid,
    fid: args.fid,
    owner: account.address,
    timestamp,
    signature,
  }),
});

if (regRes.ok) {
  const data = await regRes.json();
  console.log(`✅ Fname registered on fnames.farcaster.xyz (transfer ID: ${data.transfer?.id ?? "?"})`);
} else {
  const text = await regRes.text();
  if (text.includes("already registered")) {
    console.log(`ℹ️  Fname already registered, continuing...`);
  } else {
    console.error(`❌ Fname registration failed: HTTP ${regRes.status} - ${text}`);
    process.exit(1);
  }
}

// ── Step 3: Wait for hub sync ────────────────────────────────────────

console.log("\n⏳ Waiting 30 seconds for hub to sync fname...");
await new Promise((r) => setTimeout(r, 30000));

// ── Step 4: Set UserData USERNAME on hub ──────────────────────────────

const hubUrl = args.hubUrl || AGENTCAST_HUB_PROXY;
console.log(`\nSetting UserData USERNAME on hub (${hubUrl})...`);

const keyBytes = Buffer.from(signerKey.replace(/^0x/, ""), "hex");
const signer = new NobleEd25519Signer(keyBytes);

const result = await makeUserDataAdd(
  { type: UserDataType.USERNAME, value: args.fname },
  { fid: args.fid, network: FarcasterNetwork.MAINNET },
  signer
);

if (result.isErr()) {
  console.error(`❌ Failed to create UserData message: ${result.error.message}`);
  process.exit(1);
}

const messageBytes = Buffer.from(Message.encode(result.value).finish());
const hubRes = await fetch(hubUrl, {
  method: "POST",
  headers: { "Content-Type": "application/octet-stream" },
  body: messageBytes,
});

if (hubRes.ok) {
  console.log(`✅ Username "${args.fname}" set on hub`);
  console.log(`\n🎉 Done! Verify: https://farcaster.xyz/${args.fname}`);
} else {
  const body = await hubRes.text();
  console.error(`❌ Hub rejected UserData: HTTP ${hubRes.status} - ${body}`);
  process.exit(1);
}
