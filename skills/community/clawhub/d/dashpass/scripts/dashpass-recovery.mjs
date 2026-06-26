/**
 * dashpass-recovery.mjs — Phase 0 (P0-3): BIP-39 backup/recover for the
 * CRITICAL_WIF-derived 32-byte private key. Pure local crypto, no Platform deps.
 *
 * Model (borrowed from oak-keyring's BIP-39 recovery-words pattern):
 *   backup:  CRITICAL_WIF -> 32-byte privKey -> 24-word BIP-39 mnemonic (stdout only)
 *   recover: mnemonic -> 32-byte entropy -> privKey -> WIF (re-set CRITICAL_WIF)
 *
 * Recovery reconstructs the SAME private key; it introduces no second key
 * hierarchy and does not touch Scheme C.
 */
import { createHash } from 'node:crypto';
import { entropyToMnemonic, mnemonicToEntropy, validateMnemonic } from '@scure/bip39';
import { wordlist } from '@scure/bip39/wordlists/english.js';

const BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz';

function sha256(buf) { return createHash('sha256').update(buf).digest(); }
function sha256d(buf) { return sha256(sha256(buf)); }

export function base58Decode(str) {
  let num = 0n;
  for (const char of str) {
    const idx = BASE58_ALPHABET.indexOf(char);
    if (idx < 0) throw new Error(`Invalid base58 character: '${char}'`);
    num = num * 58n + BigInt(idx);
  }
  const hex = num.toString(16);
  const padded = hex.length % 2 === 0 ? hex : '0' + hex;
  const bytes = Buffer.from(padded, 'hex');
  let leadingZeros = 0;
  for (const char of str) { if (char !== '1') break; leadingZeros++; }
  return Buffer.concat([Buffer.alloc(leadingZeros), bytes]);
}

export function base58Encode(buf) {
  let num = BigInt('0x' + (buf.toString('hex') || '0'));
  let out = '';
  while (num > 0n) { const rem = Number(num % 58n); out = BASE58_ALPHABET[rem] + out; num /= 58n; }
  for (const b of buf) { if (b !== 0) break; out = '1' + out; }
  return out;
}

// Mirrors dashpass-cli.mjs:109 — decode WIF to the 32-byte private key.
export function wifToPrivateKey(wif) {
  const decoded = base58Decode(wif);
  if (decoded.length < 37) throw new Error('WIF decode: buffer too short');
  const payload = decoded.slice(0, decoded.length - 4);
  const checksum = decoded.slice(decoded.length - 4);
  const expected = sha256d(payload).slice(0, 4);
  if (!checksum.equals(expected)) throw new Error('WIF decode: checksum mismatch');
  const version = payload[0];
  if (version !== 0x80 && version !== 0xef) {
    throw new Error(`WIF decode: unexpected version byte 0x${version.toString(16)}`);
  }
  const privKey = payload.slice(1, 33);
  if (privKey.length !== 32) throw new Error('WIF decode: private key not 32 bytes');
  return privKey;
}

// Inverse of wifToPrivateKey — encode a 32-byte key back to WIF.
// testnet => 0xef, mainnet => 0x80; compressed appends 0x01 (Dash Platform keys are compressed).
export function privateKeyToWif(privKey, { testnet = true, compressed = true } = {}) {
  if (privKey.length !== 32) throw new Error('privateKeyToWif: key not 32 bytes');
  const version = Buffer.from([testnet ? 0xef : 0x80]);
  const parts = [version, Buffer.from(privKey)];
  if (compressed) parts.push(Buffer.from([0x01]));
  const payload = Buffer.concat(parts);
  const checksum = sha256d(payload).slice(0, 4);
  return base58Encode(Buffer.concat([payload, checksum]));
}

// 32-byte privKey -> 24-word BIP-39 mnemonic (checksum-protected by @scure).
export function privateKeyToMnemonic(privKey) {
  if (privKey.length !== 32) throw new Error('privateKeyToMnemonic: key not 32 bytes');
  return entropyToMnemonic(Uint8Array.from(privKey), wordlist);
}

// 24-word mnemonic -> 32-byte privKey. Throws on bad checksum / wrong length.
export function mnemonicToPrivateKey(mnemonic) {
  const norm = mnemonic.trim().replace(/\s+/g, ' ');
  if (!validateMnemonic(norm, wordlist)) throw new Error('recover: invalid BIP-39 mnemonic (checksum/wordlist)');
  const entropy = mnemonicToEntropy(norm, wordlist);
  if (entropy.length !== 32) throw new Error('recover: mnemonic does not encode a 32-byte key (need 24 words)');
  return Buffer.from(entropy);
}
