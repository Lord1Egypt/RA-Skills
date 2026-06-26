#!/usr/bin/env node

/**
 * Set Farcaster profile data (display name, bio, pfp, username).
 *
 * Submits UserDataAdd messages to a Farcaster hub via the AgentCast proxy,
 * bypassing x402 USDC payment requirements.
 *
 * Usage:
 *   SIGNER_KEY=0x... node set-profile.mjs \
 *     --fid <fid> \
 *     --display-name "My Agent" \
 *     --bio "I am an AI agent" \
 *     --pfp "https://example.com/avatar.png" \
 *     --username "myagent"
 *
 * Options:
 *   --fid            Farcaster FID (required)
 *   --display-name   Display name (optional)
 *   --bio            Bio text (optional)
 *   --pfp            Profile picture URL (optional)
 *   --username       Username / fname (optional)
 *   --hub-url        Hub endpoint (default: AgentCast proxy)
 *
 * Environment:
 *   SIGNER_KEY       Ed25519 signer private key (required, hex)
 *
 * At least one profile field must be provided.
 */

import {
  makeUserDataAdd,
  NobleEd25519Signer,
  FarcasterNetwork,
  UserDataType,
  Message,
} from "@farcaster/core";

const AGENTCAST_HUB_PROXY = "https://ac.800.works/api/neynar/hub";

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
      case "--display-name":
        args.displayName = val;
        i += 2;
        break;
      case "--bio":
        args.bio = val;
        i += 2;
        break;
      case "--pfp":
        args.pfp = val;
        i += 2;
        break;
      case "--username":
        args.username = val;
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

const signerKey = process.env.SIGNER_KEY;
if (!signerKey) {
  console.error("Error: SIGNER_KEY environment variable is required (Ed25519 signer private key, hex)");
  process.exit(1);
}

if (!args.fid) {
  console.error("Error: --fid is required");
  process.exit(1);
}

const fields = [];
if (args.displayName !== undefined)
  fields.push({ type: UserDataType.DISPLAY, value: args.displayName, label: "Display name" });
if (args.bio !== undefined)
  fields.push({ type: UserDataType.BIO, value: args.bio, label: "Bio" });
if (args.pfp !== undefined)
  fields.push({ type: UserDataType.PFP, value: args.pfp, label: "Profile picture" });
if (args.username !== undefined)
  fields.push({ type: UserDataType.USERNAME, value: args.username, label: "Username" });

if (fields.length === 0) {
  console.error("Error: At least one profile field required (--display-name, --bio, --pfp, --username)");
  process.exit(1);
}

// ── Submit ────────────────────────────────────────────────────────────

const keyBytes = Buffer.from(signerKey.replace(/^0x/, ""), "hex");
const signer = new NobleEd25519Signer(keyBytes);
const hubUrl = args.hubUrl || AGENTCAST_HUB_PROXY;

const dataOptions = {
  fid: args.fid,
  network: FarcasterNetwork.MAINNET,
};

console.log(`\nSetting profile for FID ${args.fid}...`);
console.log(`Hub: ${hubUrl}\n`);

let success = 0;
let failed = 0;

for (const field of fields) {
  try {
    const result = await makeUserDataAdd(
      { type: field.type, value: field.value },
      dataOptions,
      signer
    );

    if (result.isErr()) {
      console.error(`❌ ${field.label}: ${result.error.message}`);
      failed++;
      continue;
    }

    const messageBytes = Buffer.from(Message.encode(result.value).finish());

    const resp = await fetch(`${hubUrl}`, {
      method: "POST",
      headers: { "Content-Type": "application/octet-stream" },
      body: messageBytes,
    });

    if (resp.ok) {
      console.log(`✅ ${field.label}: "${field.value}"`);
      success++;
    } else {
      const body = await resp.text();
      console.error(`❌ ${field.label}: HTTP ${resp.status} - ${body}`);
      failed++;
    }
  } catch (err) {
    console.error(`❌ ${field.label}: ${err.message}`);
    failed++;
  }
}

console.log(`\nDone: ${success} updated, ${failed} failed`);
if (failed > 0) process.exit(1);
