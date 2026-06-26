import { describe, it, expect } from 'vitest';
import { mkdtempSync, writeFileSync, rmSync } from 'fs';
import { join } from 'path';
import { tmpdir } from 'os';
import { pbkdf2Sync, randomBytes } from 'crypto';
import { createRequire } from 'module';

const require = createRequire(import.meta.url);
const sodium = require('sodium-native');
const b4a = require('b4a');

import { createSigner } from '../lib/signer.js';

// Build a real WDK vault in memory with known entropy + password
function buildTestVault(entropyHex, password) {
  const salt = randomBytes(16);
  const key = pbkdf2Sync(password, salt, 100_000, 32, 'sha256');
  const payload = Buffer.from(entropyHex, 'hex');
  const plain = b4a.alloc(1 + payload.byteLength);
  plain[0] = payload.byteLength;
  plain.set(payload, 1);
  const nonce = b4a.alloc(sodium.crypto_secretbox_NONCEBYTES);
  sodium.randombytes_buf(nonce);
  const cipher = b4a.alloc(plain.byteLength + sodium.crypto_secretbox_MACBYTES);
  sodium.crypto_secretbox_easy(cipher, plain, nonce, key);
  const versionedPayload = Buffer.concat([Buffer.from([0]), nonce, cipher]);
  return {
    encryptedEntropy: versionedPayload.toString('hex'),
    salt: salt.toString('hex'),
  };
}

describe('createSigner', () => {
  it('returns an ethers Wallet with correct address from vault', async () => {
    // 16-byte entropy (128-bit) → 12-word mnemonic
    const entropyHex = 'a'.repeat(32); // 16 bytes
    const password = 'test-password';
    const vault = buildTestVault(entropyHex, password);

    const dir = mkdtempSync(join(tmpdir(), 'pm-signer-'));
    try {
      writeFileSync(join(dir, '.wdk_vault'), JSON.stringify(vault));
      writeFileSync(join(dir, '.wdk_password'), password);
      const cfg = {
        env: {
          WDK_VAULT_FILE: join(dir, '.wdk_vault'),
          WDK_PASSWORD_FILE: join(dir, '.wdk_password'),
        },
      };
      const wallet = await createSigner(cfg);
      expect(wallet.address).toMatch(/^0x[0-9a-fA-F]{40}$/);
      // Same inputs → same address (deterministic)
      const wallet2 = await createSigner(cfg);
      expect(wallet2.address).toBe(wallet.address);
    } finally {
      rmSync(dir, { recursive: true });
    }
  });

  it('throws on wrong password', async () => {
    const vault = buildTestVault('a'.repeat(32), 'correct');
    const dir = mkdtempSync(join(tmpdir(), 'pm-signer-'));
    try {
      writeFileSync(join(dir, '.wdk_vault'), JSON.stringify(vault));
      writeFileSync(join(dir, '.wdk_password'), 'wrong');
      const cfg = {
        env: {
          WDK_VAULT_FILE: join(dir, '.wdk_vault'),
          WDK_PASSWORD_FILE: join(dir, '.wdk_password'),
        },
      };
      await expect(createSigner(cfg)).rejects.toThrow('decryption failed');
    } finally {
      rmSync(dir, { recursive: true });
    }
  });

  it('throws with clear error when vault file is missing', async () => {
    const cfg = { env: { WDK_VAULT_FILE: '/nonexistent/.wdk_vault' } };
    await expect(createSigner(cfg)).rejects.toThrow('not found');
  });
});
