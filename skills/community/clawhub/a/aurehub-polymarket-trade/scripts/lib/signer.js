import { readFileSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';
import { pbkdf2Sync } from 'crypto';
import { Wallet } from 'ethers'; // ethers v5

import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const sodium = require('sodium-native');
const b4a = require('b4a');
const bip39 = require('bip39-mnemonic');

/** Expand leading ~ to the user's home directory. */
function expandTilde(p) {
  if (typeof p === 'string' && p.startsWith('~/')) return join(homedir(), p.slice(2));
  return p;
}

/**
 * Derive a 32-byte key from password + salt using PBKDF2-SHA256.
 * Matches WdkSecretManager#deriveKeyFromPassKey() (100 000 iterations).
 *
 * @param {string|Buffer} password
 * @param {Buffer} salt  16-byte salt
 * @returns {Buffer}
 */
function wdkDeriveKey(password, salt) {
  return pbkdf2Sync(password, salt, 100_000, 32, 'sha256');
}

/**
 * Decrypt a WDK-encrypted payload.
 * Matches WdkSecretManager.decrypt().
 *
 * Vault encryption format:
 *   byte 0     : version (0)
 *   bytes 1..N : nonce   (crypto_secretbox_NONCEBYTES = 24)
 *   bytes N+1..: ciphertext (1 + plaintextLen + MACBYTES)
 *                  plain[0]  = original payload length
 *                  plain[1..]: payload bytes
 *
 * @param {Buffer} payload  Encrypted bytes
 * @param {Buffer} key      32-byte derived key
 * @returns {Buffer}  Decrypted entropy bytes
 */
function wdkDecrypt(payload, key) {
  const NONCEBYTES = sodium.crypto_secretbox_NONCEBYTES;
  const MACBYTES = sodium.crypto_secretbox_MACBYTES;

  if (payload[0] !== 0) throw new Error('WDK vault: unsupported encryption version');

  const nonce = payload.subarray(1, 1 + NONCEBYTES);
  const cipher = payload.subarray(1 + NONCEBYTES);
  const plain = b4a.alloc(cipher.byteLength - MACBYTES);

  if (!sodium.crypto_secretbox_open_easy(plain, cipher, nonce, key)) {
    throw new Error('WDK vault: decryption failed — wrong password or corrupted vault');
  }

  const bytes = plain[0];
  const result = b4a.alloc(bytes);
  result.set(plain.subarray(1, 1 + bytes));
  sodium.sodium_memzero(plain);
  return result;
}

/**
 * Create an ethers v5 Wallet from a WDK vault file.
 *
 * @param {{ env: object }} cfg  Config object with env overrides.
 * @returns {Promise<import('ethers').Wallet>}
 */
export async function createSigner(cfg, opts = {}) {
  const vaultPath = expandTilde(
    cfg?.env?.WDK_VAULT_FILE ?? join(homedir(), '.aurehub', '.wdk_vault'),
  );

  let vault;
  try {
    vault = JSON.parse(readFileSync(vaultPath, 'utf8'));
  } catch (e) {
    throw new Error(`WDK vault not found at "${vaultPath}": ${e.message}`);
  }

  if (!vault.encryptedEntropy || !vault.salt) {
    throw new Error('WDK vault is missing required fields: encryptedEntropy, salt');
  }

  const passwordFile = expandTilde(
    cfg?.env?.WDK_PASSWORD_FILE ?? join(homedir(), '.aurehub', '.wdk_password'),
  );

  let password;
  try {
    password = readFileSync(passwordFile, 'utf8').trim();
  } catch (e) {
    throw new Error(`Cannot read WDK_PASSWORD_FILE "${passwordFile}": ${e.message}`);
  }

  const salt = Buffer.from(vault.salt, 'hex');
  const encryptedEntropy = Buffer.from(vault.encryptedEntropy, 'hex');
  const key = wdkDeriveKey(password, salt);
  let entropy;
  try {
    entropy = wdkDecrypt(encryptedEntropy, key);
  } finally {
    key.fill(0);
  }

  let wallet;
  try {
    const mnemonic = bip39.entropyToMnemonic(entropy);
    const index = opts.accountIndex ?? parseInt(cfg?.env?.WDK_ACCOUNT_INDEX || '0', 10);
    if (!Number.isInteger(index) || index < 0) {
      throw new Error(`Invalid account index: ${cfg?.env?.WDK_ACCOUNT_INDEX}. Must be a non-negative integer.`);
    }
    const path = `m/44'/60'/0'/0/${index}`;
    wallet = Wallet.fromMnemonic(mnemonic, path); // ethers v5 API
  } finally {
    sodium.sodium_memzero(entropy);
  }
  return wallet;
}
