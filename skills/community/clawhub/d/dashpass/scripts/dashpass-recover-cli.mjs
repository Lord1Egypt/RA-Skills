#!/usr/bin/env node
/**
 * dashpass-recover-cli.mjs — standalone key backup & recovery (v0.9 / P0-3).
 *
 * NO Dash Platform / evo-sdk dependency BY DESIGN. Recovery must work in two
 * situations where the main CLI cannot run:
 *   1. CRITICAL_WIF is LOST — the very case `recover` exists for, yet
 *      dashpass-cli.mjs exits early when CRITICAL_WIF is unset.
 *   2. The Platform SDK / network is unavailable (disaster scenario).
 *
 * Commands:
 *   backup   CRITICAL_WIF (env)            -> 24-word BIP-39 mnemonic (stdout)
 *   recover  24-word mnemonic (stdin)      -> WIF (stdout), to re-set CRITICAL_WIF
 *   verify   CRITICAL_WIF (env) + mnemonic (stdin) -> assert they derive the same key
 *
 * The mnemonic encodes the 32-byte private key. The derived AES key depends only
 * on those 32 bytes (Scheme C strips the WIF version/compression byte), so a
 * recovered key decrypts every existing credential.
 */
import { readFileSync } from 'node:fs';
import {
  wifToPrivateKey, privateKeyToWif, privateKeyToMnemonic, mnemonicToPrivateKey,
} from './dashpass-recovery.mjs';

function readStdin() {
  try { return readFileSync(0, 'utf8'); } catch { return ''; }
}
function die(msg, code = 1) { process.stderr.write(`[error] ${msg}\n`); process.exit(code); }

const cmd = process.argv[2];
const flags = process.argv.slice(3);
const testnet = !flags.includes('--mainnet'); // skill is testnet-default

try {
  if (cmd === 'backup') {
    const wif = process.env.CRITICAL_WIF;
    if (!wif) die('CRITICAL_WIF not set — nothing to back up.');
    const key = wifToPrivateKey(wif);
    const mnemonic = privateKeyToMnemonic(key);
    key.fill(0);
    process.stderr.write('⚠️  Write these 24 words on paper, OFFLINE. Anyone with them controls the vault.\n');
    process.stdout.write(mnemonic + '\n');
  } else if (cmd === 'recover') {
    const mnemonic = readStdin().trim();
    if (!mnemonic) die('pipe the 24-word mnemonic on stdin, e.g.  cat words.txt | ... recover');
    const key = mnemonicToPrivateKey(mnemonic);
    const wif = privateKeyToWif(key, { testnet });
    key.fill(0);
    process.stderr.write('Recovered WIF below. Re-set it:  export CRITICAL_WIF=<wif>\n');
    process.stdout.write(wif + '\n');
  } else if (cmd === 'verify') {
    const wif = process.env.CRITICAL_WIF;
    if (!wif) die('CRITICAL_WIF not set — nothing to verify against.');
    const mnemonic = readStdin().trim();
    if (!mnemonic) die('pipe the 24-word mnemonic on stdin.');
    const fromWif = wifToPrivateKey(wif);
    const fromMnemonic = mnemonicToPrivateKey(mnemonic);
    const ok = Buffer.from(fromWif).equals(Buffer.from(fromMnemonic));
    fromWif.fill(0); fromMnemonic.fill(0);
    process.stderr.write(ok
      ? '✅ mnemonic matches CRITICAL_WIF — backup is valid.\n'
      : '❌ MISMATCH — this mnemonic does NOT recover the current key.\n');
    process.exit(ok ? 0 : 1);
  } else {
    process.stderr.write('usage: dashpass-recover-cli.mjs <backup|recover|verify> [--mainnet]\n');
    process.exit(2);
  }
} catch (e) {
  die(e.message);
}
