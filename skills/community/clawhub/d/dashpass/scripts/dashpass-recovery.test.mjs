/**
 * Phase 0 (P0-3) recovery verification — runtime-independent (no evo-sdk, no testnet).
 * Proves: WIF <-> key <-> 24-word mnemonic round-trips exactly, and a key recovered
 * from the mnemonic decrypts a Scheme-C blob produced by the original key.
 */
import { test, expect } from 'bun:test';
import { hkdfSync, createCipheriv, createDecipheriv, randomBytes } from 'node:crypto';
import {
  wifToPrivateKey, privateKeyToWif, privateKeyToMnemonic, mnemonicToPrivateKey,
} from './dashpass-recovery.mjs';

// ── AEAD keyed on privKey (bun-runnable proxy for Scheme C) ──────────────────
// Production Scheme C (dashpass-cli.mjs:127) wraps privKey in an ECDH-self step
// before HKDF: shared = ECDH(priv, priv*G), key = HKDF(shared, salt). bun's
// createECDH lacks the secp256k1 named curve, so this proxy derives the AES key
// directly from privKey via HKDF. Sound for the recovery proof because the ECDH
// wrapper is a *deterministic pure function of privKey* — a byte-identical
// recovered key (asserted independently below) yields a byte-identical AES key
// under either derivation. ECDH-path equivalence is exercised on node, not bun.
function deriveAesKey(privKey, salt) {
  return Buffer.from(hkdfSync('sha256', Buffer.from(privKey), salt, 'dashpass-v1', 32));
}
function encrypt(privKey, payload) {
  const salt = randomBytes(32), nonce = randomBytes(12);
  const cipher = createCipheriv('aes-256-gcm', deriveAesKey(privKey, salt), nonce);
  const ct = Buffer.concat([cipher.update(Buffer.from(JSON.stringify(payload))), cipher.final()]);
  return { blob: Buffer.concat([ct, cipher.getAuthTag()]), salt, nonce };
}
function decrypt(privKey, blob, salt, nonce) {
  const tag = blob.slice(blob.length - 16), ct = blob.slice(0, blob.length - 16);
  const d = createDecipheriv('aes-256-gcm', deriveAesKey(privKey, salt), nonce);
  d.setAuthTag(tag);
  return JSON.parse(Buffer.concat([d.update(ct), d.final()]).toString('utf8'));
}

test('WIF <-> privKey round-trips (testnet, compressed)', () => {
  const key = randomBytes(32);
  const wif = privateKeyToWif(key, { testnet: true, compressed: true });
  expect(Buffer.from(wifToPrivateKey(wif)).equals(key)).toBe(true);
});

test('privKey -> 24-word mnemonic -> privKey round-trips', () => {
  const key = randomBytes(32);
  const mnemonic = privateKeyToMnemonic(key);
  expect(mnemonic.split(' ').length).toBe(24);
  expect(Buffer.from(mnemonicToPrivateKey(mnemonic)).equals(key)).toBe(true);
});

test('full backup->recover: recovered key decrypts the original Scheme-C blob', () => {
  // original vault key (as if derived from CRITICAL_WIF)
  const original = wifToPrivateKey(privateKeyToWif(randomBytes(32)));
  const secret = { value: 'sk-ant-TESTNET-fake-credential', meta: { service: 'anthropic-api' } };
  const { blob, salt, nonce } = encrypt(original, secret);

  // backup -> hold only the mnemonic, discard the key
  const mnemonic = privateKeyToMnemonic(original);

  // recover from mnemonic alone
  const recovered = mnemonicToPrivateKey(mnemonic);
  expect(decrypt(recovered, blob, salt, nonce)).toEqual(secret);

  // and the recovered key re-encodes to the same WIF (so CRITICAL_WIF can be re-set)
  expect(privateKeyToWif(recovered)).toBe(privateKeyToWif(original));
});

test('wrong mnemonic cannot decrypt (auth-tag failure, no silent garbage)', () => {
  const original = randomBytes(32);
  const { blob, salt, nonce } = encrypt(original, { value: 'secret' });
  const wrong = mnemonicToPrivateKey(privateKeyToMnemonic(randomBytes(32)));
  expect(() => decrypt(wrong, blob, salt, nonce)).toThrow();
});

test('tampered mnemonic is rejected by checksum', () => {
  const words = privateKeyToMnemonic(randomBytes(32)).split(' ');
  words[0] = words[0] === 'abandon' ? 'ability' : 'abandon'; // flip first word
  expect(() => mnemonicToPrivateKey(words.join(' '))).toThrow(/invalid BIP-39/);
});
