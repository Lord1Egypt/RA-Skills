#!/usr/bin/env node
/**
 * Probe on-chain Anchor IDL for a Solana program.
 * Run from a scaffolded project (so node_modules resolve), or with deps on NODE_PATH.
 *
 * Usage:
 *   node ~/.cursor/skills/fetch-solana-logs/scripts/probe-idl.mjs --addr <PROGRAM_ID> [--rpc <URL>] [--out <path>]
 */
import fs from 'fs';
import path from 'path';
import { createRequire } from 'module';
import { pathToFileURL } from 'url';

function usage() {
  console.error(
    'Usage: node probe-idl.mjs --addr <PROGRAM_ID> [--rpc <URL>] [--out <file.json>]',
  );
  process.exit(1);
}

function parseArgs(argv) {
  let addr = '';
  let rpc = process.env.SOLANA_RPC_URL || '';
  let out = '';
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--addr' || a === '-a') addr = argv[++i] || '';
    else if (a.startsWith('--addr=')) addr = a.slice('--addr='.length);
    else if (a === '--rpc') rpc = argv[++i] || '';
    else if (a.startsWith('--rpc=')) rpc = a.slice('--rpc='.length);
    else if (a === '--out') out = argv[++i] || '';
    else if (a.startsWith('--out=')) out = a.slice('--out='.length);
    else if (a === '--help' || a === '-h') usage();
  }
  if (!addr) usage();
  if (!rpc) {
    const key = process.env.HELIUS_API_KEY;
    rpc = key
      ? `https://mainnet.helius-rpc.com/?api-key=${key}`
      : 'https://api.mainnet-beta.solana.com';
  }
  return { addr, rpc, out };
}

async function loadDeps() {
  const requireFromCwd = createRequire(path.join(process.cwd(), 'package.json'));
  try {
    const web3Path = requireFromCwd.resolve('@solana/web3.js');
    const anchorPath = requireFromCwd.resolve('@coral-xyz/anchor');
    const web3 = await import(pathToFileURL(web3Path).href);
    const anchor = await import(pathToFileURL(anchorPath).href);
    return { Connection: web3.Connection, Program: anchor.Program };
  } catch (err) {
    console.error(
      'Could not load @solana/web3.js / @coral-xyz/anchor from cwd.\n' +
        'cd into a scaffolded fetch_solana_logs project (after pnpm install), then retry.',
    );
    console.error(String(err.message || err));
    process.exit(1);
  }
}

async function main() {
  const { addr, rpc, out } = parseArgs(process.argv.slice(2));
  const { Connection, Program } = await loadDeps();

  const connection = new Connection(rpc, 'confirmed');
  console.log(`probing IDL for ${addr}`);
  console.log(`rpc: ${rpc.replace(/api-key=[^&]+/, 'api-key=***')}`);

  const idl = await Program.fetchIdl(addr, { connection });
  if (!idl) {
    console.log('no on-chain Anchor IDL');
    process.exit(2);
  }

  const name = idl.metadata?.name || idl.name || '(unnamed)';
  const ixs = (idl.instructions || []).map((i) => i.name);
  console.log(`found IDL: ${name}`);
  console.log(`instructions (${ixs.length}): ${ixs.join(', ')}`);

  const outPath = out || path.join('output', addr, `idl_${addr}.json`);
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, JSON.stringify(idl, null, 2));
  console.log(`saved → ${outPath}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
