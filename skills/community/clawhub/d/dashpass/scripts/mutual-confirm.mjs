/**
 * mutual-confirm.mjs
 * DashPass Mutual Confirmation Protocol — Shamir 2-of-2 over GF(2^8)
 *
 * Architecture:
 *   CRITICAL_WIF → 32-byte private key → Shamir split → shareA (evo) + shareB (cc)
 *   Decrypt: combineShares → private key → ECDH self-sign + HKDF → per-credential AES key → AES-256-GCM
 *
 * Neither share alone reveals any information about the key (information-theoretic security).
 */

import {
  randomBytes,
  createECDH,
  hkdfSync,
  createDecipheriv,
} from 'node:crypto';
import {
  readFileSync,
  writeFileSync,
  appendFileSync,
  existsSync,
  mkdirSync,
  chmodSync,
  statSync,
} from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';

// ── Paths ────────────────────────────────────────────────────────────────────

const DASHPASS_DIR   = join(homedir(), '.dashpass');
const SHARE_A_PATH   = join(DASHPASS_DIR, 'evo.share');
const SHARE_B_PATH   = join(DASHPASS_DIR, 'cc.share');
const AUDIT_LOG_PATH = join(DASHPASS_DIR, 'audit.log');

export { DASHPASS_DIR, SHARE_A_PATH, SHARE_B_PATH, AUDIT_LOG_PATH };

// ── GF(2^8) Arithmetic ──────────────────────────────────────────────────────
// Irreducible polynomial: x^8 + x^4 + x^3 + x^2 + 1  (0x11d)
// All operations are over the finite field with 256 elements.

/**
 * Multiply two elements in GF(2^8).
 * Uses shift-and-XOR (Russian peasant / peasant multiplication).
 */
export function gf256Mul(a, b) {
  let result = 0;
  let aa = a & 0xff;
  let bb = b & 0xff;
  while (bb > 0) {
    if (bb & 1) result ^= aa;
    aa <<= 1;
    if (aa & 0x100) aa ^= 0x11d;
    bb >>= 1;
  }
  return result & 0xff;
}

/**
 * Multiplicative inverse in GF(2^8) via Fermat's little theorem.
 * a^(-1) = a^(254)  since |GF(2^8)*| = 255.
 */
export function gf256Inv(a) {
  if (a === 0) throw new Error('Cannot invert zero in GF(256)');
  let result = 1;
  let base = a & 0xff;
  let exp = 254;
  while (exp > 0) {
    if (exp & 1) result = gf256Mul(result, base);
    base = gf256Mul(base, base);
    exp >>= 1;
  }
  return result;
}

// Precomputed Lagrange coefficients for 2-of-2 at evaluation points x=1, x=2.
// Recover f(0) from f(1) and f(2):
//   L1(0) = (0 - 2) / (1 - 2) = 2 / 3   (subtraction = XOR in GF(2^8))
//   L2(0) = (0 - 1) / (2 - 1) = 1 / 3
const INV_3    = gf256Inv(3);
const L1_COEFF = gf256Mul(2, INV_3);   // Lagrange weight for share at x=1
const L2_COEFF = INV_3;                 // Lagrange weight for share at x=2

export { L1_COEFF, L2_COEFF };

// ── Shamir 2-of-2 Secret Sharing ────────────────────────────────────────────

/**
 * Split a key (Buffer) into two Shamir shares over GF(2^8).
 * For each byte: f(x) = a0 + a1·x, where a0 = secret byte, a1 = random.
 * Share A = f(1), Share B = f(2).
 *
 * @param {Buffer} key - The secret key to split (any length, typically 32 bytes)
 * @returns {{ shareA: string, shareB: string }} hex-encoded shares
 */
export function splitKey(key) {
  if (!Buffer.isBuffer(key) || key.length === 0) {
    throw new Error('splitKey: key must be a non-empty Buffer');
  }

  const coeffs = randomBytes(key.length); // random a1 per byte
  const shareA = Buffer.alloc(key.length);
  const shareB = Buffer.alloc(key.length);

  for (let i = 0; i < key.length; i++) {
    const a0 = key[i];
    const a1 = coeffs[i];
    shareA[i] = a0 ^ a1;                    // f(1) = a0 + a1·1
    shareB[i] = a0 ^ gf256Mul(a1, 2);       // f(2) = a0 + a1·2
  }

  coeffs.fill(0);
  const hexA = shareA.toString('hex');
  const hexB = shareB.toString('hex');
  shareA.fill(0);
  shareB.fill(0);
  // Note: hex strings are JS immutable strings and cannot be zeroed from memory.
  // They will be garbage-collected. This is an inherent JS limitation.
  return { shareA: hexA, shareB: hexB };
}

/**
 * Reconstruct a key from two Shamir shares using Lagrange interpolation.
 * @param {string} shareAHex - hex share at x=1
 * @param {string} shareBHex - hex share at x=2
 * @returns {Buffer} the reconstructed key
 */
export function combineShares(shareAHex, shareBHex) {
  const sA = Buffer.from(shareAHex, 'hex');
  const sB = Buffer.from(shareBHex, 'hex');

  if (sA.length !== sB.length || sA.length === 0) {
    throw new Error('combineShares: shares must be equal non-zero length');
  }

  const key = Buffer.alloc(sA.length);
  for (let i = 0; i < sA.length; i++) {
    key[i] = gf256Mul(sA[i], L1_COEFF) ^ gf256Mul(sB[i], L2_COEFF);
  }
  return key;
}

// ── Share File I/O ───────────────────────────────────────────────────────────

function ensureDir() {
  mkdirSync(DASHPASS_DIR, { recursive: true, mode: 0o700 });
}

export function storeShares(shareAHex, shareBHex) {
  ensureDir();
  writeFileSync(SHARE_A_PATH, shareAHex + '\n', { mode: 0o600 });
  writeFileSync(SHARE_B_PATH, shareBHex + '\n', { mode: 0o600 });
  chmodSync(SHARE_A_PATH, 0o600);
  chmodSync(SHARE_B_PATH, 0o600);
}

export function readShareA() {
  return readFileSync(SHARE_A_PATH, 'utf8').trim();
}

export function readShareB() {
  return readFileSync(SHARE_B_PATH, 'utf8').trim();
}

export function sharesExist() {
  return existsSync(SHARE_A_PATH) && existsSync(SHARE_B_PATH);
}

/**
 * Check health of both share files.
 * @returns {{ evo: object, cc: object }}
 */
export function shareStatus() {
  const result = { evo: { exists: false }, cc: { exists: false } };

  for (const [label, path] of [['evo', SHARE_A_PATH], ['cc', SHARE_B_PATH]]) {
    if (existsSync(path)) {
      const stat = statSync(path);
      const content = readFileSync(path, 'utf8').trim();
      result[label] = {
        exists: true,
        path,
        permissions: '0' + (stat.mode & 0o777).toString(8),
        bytes: content.length / 2,
        healthy: content.length === 64 && /^[0-9a-f]+$/i.test(content),
      };
    }
  }

  return result;
}

// ── Audit Logging ────────────────────────────────────────────────────────────
// Never logs key material or share values.

function auditLog(entry) {
  ensureDir();
  const record = { timestamp: new Date().toISOString(), ...entry };
  appendFileSync(AUDIT_LOG_PATH, JSON.stringify(record) + '\n', { mode: 0o600 });
}

export { auditLog };

// ── Mutual Confirmation Protocol ─────────────────────────────────────────────

/**
 * Create a decrypt request (step 1 of the protocol).
 */
export function requestDecrypt(credentialName, reason, requesterRole) {
  const request = {
    id: randomBytes(16).toString('hex'),
    credentialName,
    reason,
    requesterRole,
    timestamp: new Date().toISOString(),
    status: 'pending',
  };

  auditLog({
    action: 'request',
    service: credentialName,
    requester: requesterRole,
    result: 'pending',
  });

  return request;
}

/**
 * Approve a decrypt request (step 2).
 */
export function approveDecrypt(request, approverRole) {
  auditLog({
    action: 'approve',
    service: request.credentialName,
    requester: request.requesterRole,
    approver: approverRole,
    result: 'approved',
  });

  return { ...request, approver: approverRole, approvedAt: new Date().toISOString(), status: 'approved' };
}

/**
 * Deny a decrypt request.
 */
export function denyDecrypt(request, denierRole, reason) {
  auditLog({
    action: 'deny',
    service: request.credentialName,
    requester: request.requesterRole,
    approver: denierRole,
    result: 'denied',
    reason,
  });

  return { ...request, status: 'denied', reason };
}

/**
 * Execute mutual decryption (step 3).
 * Combines shares → private key → ECDH + HKDF → AES-256-GCM decrypt.
 * All sensitive buffers are zeroed after use.
 *
 * @param {string} shareAHex
 * @param {string} shareBHex
 * @param {Buffer} encryptedBlobBuf - ciphertext + 16-byte GCM auth tag
 * @param {Buffer} saltBuf          - per-credential HKDF salt
 * @param {Buffer} nonceBuf         - 12-byte AES-GCM nonce
 * @returns {object} parsed JSON plaintext
 */
export function executeDecrypt(shareAHex, shareBHex, encryptedBlobBuf, saltBuf, nonceBuf) {
  const privKeyBytes = combineShares(shareAHex, shareBHex);
  let aesKey = null;

  try {
    // Derive per-credential AES key — identical to Scheme C's deriveAesKey
    const ecdh = createECDH('secp256k1');
    ecdh.setPrivateKey(privKeyBytes);
    const sharedSecret = ecdh.computeSecret(ecdh.getPublicKey());
    aesKey = Buffer.from(hkdfSync('sha256', sharedSecret, saltBuf, 'dashpass-v1', 32));
    sharedSecret.fill(0);

    // AES-256-GCM decrypt
    const tag = encryptedBlobBuf.slice(encryptedBlobBuf.length - 16);
    const ct  = encryptedBlobBuf.slice(0, encryptedBlobBuf.length - 16);
    const decipher = createDecipheriv('aes-256-gcm', aesKey, nonceBuf);
    decipher.setAuthTag(tag);
    const plain = Buffer.concat([decipher.update(ct), decipher.final()]);

    auditLog({ action: 'execute', result: 'success' });

    return JSON.parse(plain.toString('utf8'));
  } catch (e) {
    auditLog({ action: 'execute', result: 'failed', error: e.message });
    throw e;
  } finally {
    privKeyBytes.fill(0);
    if (aesKey) aesKey.fill(0);
  }
}

// ── Init Shares from WIF ─────────────────────────────────────────────────────

/**
 * Extract private key from WIF, Shamir-split it, store both shares.
 * Verifies round-trip correctness before returning.
 *
 * @param {Function} wifToPrivateKey - WIF → 32-byte Buffer
 * @param {string} wif               - WIF-encoded private key
 * @returns {{ shareA: string, shareB: string }}
 */
export function initSharesFromWif(wifToPrivateKey, wif) {
  const privKeyBytes = wifToPrivateKey(wif);

  try {
    const { shareA, shareB } = splitKey(privKeyBytes);
    storeShares(shareA, shareB);

    // Verify round-trip before declaring success
    const reconstructed = combineShares(shareA, shareB);
    if (!reconstructed.equals(privKeyBytes)) {
      throw new Error('Share round-trip verification failed — aborting');
    }
    reconstructed.fill(0);

    auditLog({
      action: 'init-shares',
      result: 'success',
      shareAPath: SHARE_A_PATH,
      shareBPath: SHARE_B_PATH,
    });

    return { shareA, shareB };
  } finally {
    privKeyBytes.fill(0);
  }
}
