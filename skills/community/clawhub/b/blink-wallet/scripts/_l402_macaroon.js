/**
 * Blink Claw Skill — L402 Macaroon Module
 *
 * Minimal custom binary macaroon implementation for L402 producer tools.
 * Intentionally NOT the full libmacaroons v2 spec — this is a practical,
 * self-contained implementation that satisfies the L402 security model:
 *   1. Cryptographic binding: macaroon encodes payment_hash, HMAC-signed
 *   2. Caveat support: expiry + resource scope
 *   3. Preimage verification remains the primary payment proof
 *
 * Binary layout:
 *   [0]        version byte (0x01)
 *   [1..32]    payment_hash (32 raw bytes)
 *   [33..N]    caveats encoded as TLV (type-length-value)
 *   [N+1..N+32] HMAC-SHA256 signature over bytes [0..N]
 *
 * TLV caveat types:
 *   0x01  expiry     uint64 big-endian unix timestamp (8 bytes)
 *   0x02  resource   UTF-8 string
 *
 * The entire binary is base64url-encoded for HTTP transport.
 *
 * Root key resolution order:
 *   1. BLINK_L402_ROOT_KEY env var (hex, 32 bytes)
 *   2. ~/.blink/l402-root-key file (hex, 32 bytes)
 *   3. Auto-generate, persist to ~/.blink/l402-root-key, warn to stderr
 *
 * Zero external dependencies — Node.js 22+ built-ins only.
 */

'use strict';

const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');

// ── Constants ────────────────────────────────────────────────────────────────

const VERSION_BYTE = 0x01;
const CAVEAT_TYPE_EXPIRY = 0x01;
const CAVEAT_TYPE_RESOURCE = 0x02;
const HMAC_SIZE = 32;
const PAYMENT_HASH_SIZE = 32;
const ROOT_KEY_SIZE = 32;
const { ensureSecureStateDir, writeSecureFileAtomic } = require('./_secure_files');

const ROOT_KEY_FILE = path.join(os.homedir(), '.blink', 'l402-root-key');

// ── Root key management ──────────────────────────────────────────────────────

/**
 * Load or generate the L402 root key (32 bytes).
 *
 * Resolution order:
 *   1. BLINK_L402_ROOT_KEY env var (hex, 64 chars = 32 bytes)
 *   2. ~/.blink/l402-root-key file (hex, 64 chars)
 *   3. Auto-generate + persist + warn
 *
 * @returns {Buffer} 32-byte root key
 */
function getRootKey() {
  // 1. Environment variable
  const envKey = process.env.BLINK_L402_ROOT_KEY;
  if (envKey) {
    if (!/^[0-9a-fA-F]{64}$/.test(envKey)) {
      throw new Error('BLINK_L402_ROOT_KEY must be a 64-character hex string (32 bytes).');
    }
    return Buffer.from(envKey, 'hex');
  }

  // 2. Persisted file. ClawHub 3.0.1 scan: the signing key mints and verifies
  // every sold token, so it gets the same protection as the other state files
  // (0700 dir, 0600 file, symlink refusal, atomic write) — it used to be read
  // through symlinks and written with a plain mkdir + writeFile.
  // The DIRECTORY must not be a symlink either (PR #25 review): hardening on
  // read is best-effort, so its refusal used to be swallowed and the key was
  // read through a symlinked ~/.blink. Check it explicitly, then harden.
  const keyDir = path.dirname(ROOT_KEY_FILE);
  try {
    if (fs.lstatSync(keyDir).isSymbolicLink()) {
      throw new Error(`Refusing to use ${keyDir}: it is a symlink.`);
    }
  } catch (e) {
    if (e.code !== 'ENOENT') throw e;
  }
  try {
    ensureSecureStateDir(keyDir);
  } catch {
    // Best-effort hardening on read (mirrors the token store).
  }
  let st = null;
  try {
    st = fs.lstatSync(ROOT_KEY_FILE);
  } catch (e) {
    if (e.code !== 'ENOENT') throw e;
  }
  if (st && st.isSymbolicLink()) {
    // Never read a key from (or regenerate over) a symlink's target.
    throw new Error(`Refusing to use ${ROOT_KEY_FILE}: it is a symlink.`);
  }
  if (st) {
    const stored = fs.readFileSync(ROOT_KEY_FILE, 'utf8').trim();
    if (/^[0-9a-fA-F]{64}$/.test(stored)) {
      return Buffer.from(stored, 'hex');
    }
    console.error(`Warning: ${ROOT_KEY_FILE} contains an invalid key — regenerating.`);
  }

  // 3. Auto-generate
  const newKey = crypto.randomBytes(ROOT_KEY_SIZE);
  const newKeyHex = newKey.toString('hex');
  try {
    writeSecureFileAtomic(ROOT_KEY_FILE, newKeyHex);
    console.error(`Warning: Generated new L402 root key and saved to ${ROOT_KEY_FILE}.`);
    console.error(`         To use it portably, copy its value into BLINK_L402_ROOT_KEY (never log the key itself).`);
  } catch (e) {
    console.error(`Warning: Could not persist L402 root key to ${ROOT_KEY_FILE}: ${e.message}`);
    console.error(`         Set BLINK_L402_ROOT_KEY to a 64-char hex key to reuse this identity.`);
  }
  return newKey;
}

// ── TLV caveat encoding / decoding ───────────────────────────────────────────

/**
 * Encode an array of caveat objects into a TLV buffer.
 *
 * @param {Array<{type: number, value: Buffer}>} caveats
 * @returns {Buffer}
 */
function encodeCaveats(caveats) {
  const parts = [];
  for (const c of caveats) {
    const typeBuf = Buffer.alloc(1);
    typeBuf[0] = c.type;
    const lenBuf = Buffer.alloc(2);
    lenBuf.writeUInt16BE(c.value.length, 0);
    parts.push(typeBuf, lenBuf, c.value);
  }
  return Buffer.concat(parts);
}

/**
 * Decode a TLV buffer into an array of caveat objects.
 *
 * @param {Buffer} buf
 * @returns {Array<{type: number, value: Buffer}>}
 */
function decodeCaveats(buf) {
  const caveats = [];
  let offset = 0;
  while (offset < buf.length) {
    if (offset + 3 > buf.length) break; // malformed — truncate
    const type = buf[offset];
    const len = buf.readUInt16BE(offset + 1);
    offset += 3;
    if (offset + len > buf.length) break; // malformed
    const value = buf.slice(offset, offset + len);
    caveats.push({ type, value });
    offset += len;
  }
  return caveats;
}

/**
 * Build a caveat value buffer for an expiry timestamp.
 * @param {number} unixTimestampSeconds
 * @returns {Buffer} 8-byte big-endian uint64
 */
function encodeExpiryValue(unixTimestampSeconds) {
  // JavaScript BigInt for safe uint64 encoding
  const buf = Buffer.alloc(8);
  const big = BigInt(Math.floor(unixTimestampSeconds));
  buf.writeBigUInt64BE(big, 0);
  return buf;
}

/**
 * Read an expiry caveat value as a JS number (safe for dates through year 2554).
 * @param {Buffer} buf 8-byte big-endian uint64
 * @returns {number}
 */
function decodeExpiryValue(buf) {
  return Number(buf.readBigUInt64BE(0));
}

// ── HMAC signing ─────────────────────────────────────────────────────────────

/**
 * Compute HMAC-SHA256 over `data` using `key`.
 * @param {Buffer} key
 * @param {Buffer} data
 * @returns {Buffer} 32-byte HMAC
 */
function hmacSha256(key, data) {
  return crypto.createHmac('sha256', key).update(data).digest();
}

// ── Macaroon encode / decode ─────────────────────────────────────────────────

/**
 * Create a signed macaroon binding a payment hash with optional caveats.
 *
 * @param {object}  opts
 * @param {string}  opts.paymentHash       64-char hex payment hash
 * @param {Buffer}  opts.rootKey           32-byte root key (from getRootKey())
 * @param {number}  [opts.expirySeconds]   Unix timestamp for expiry caveat (omit = no expiry)
 * @param {string}  [opts.resource]        Resource identifier string (omit = unconstrained)
 * @returns {string} base64url-encoded macaroon
 */
function createMacaroon({ paymentHash, rootKey, expirySeconds, resource }) {
  if (!/^[0-9a-fA-F]{64}$/.test(paymentHash)) {
    throw new Error('paymentHash must be a 64-character hex string.');
  }
  if (!Buffer.isBuffer(rootKey) || rootKey.length !== ROOT_KEY_SIZE) {
    throw new Error('rootKey must be a 32-byte Buffer.');
  }

  const hashBuf = Buffer.from(paymentHash, 'hex');

  // Build caveat list
  const caveats = [];
  if (expirySeconds !== undefined && expirySeconds !== null) {
    caveats.push({ type: CAVEAT_TYPE_EXPIRY, value: encodeExpiryValue(expirySeconds) });
  }
  if (resource !== undefined && resource !== null) {
    caveats.push({ type: CAVEAT_TYPE_RESOURCE, value: Buffer.from(resource, 'utf8') });
  }

  const caveatBuf = encodeCaveats(caveats);

  // Assemble unsigned body: [version(1)] [paymentHash(32)] [caveats(N)]
  const body = Buffer.concat([Buffer.from([VERSION_BYTE]), hashBuf, caveatBuf]);

  // Sign body
  const sig = hmacSha256(rootKey, body);

  // Final macaroon: body + sig
  const macaroon = Buffer.concat([body, sig]);
  return macaroon.toString('base64url');
}

/**
 * Decode and verify a macaroon, returning its contents if valid.
 *
 * @param {object}  opts
 * @param {string}  opts.macaroon   base64url-encoded macaroon string
 * @param {Buffer}  opts.rootKey    32-byte root key
 * @returns {{
 *   signatureValid: boolean,
 *   paymentHash: string,
 *   caveats: Array<{type:number,value:Buffer}>,
 *   expiresAt: number|null,
 *   resource: string|null
 * }}
 */
function decodeMacaroon({ macaroon, rootKey }) {
  let raw;
  try {
    raw = Buffer.from(macaroon, 'base64url');
  } catch {
    throw new Error('Macaroon is not valid base64url.');
  }

  // Minimum size: 1 (version) + 32 (hash) + 32 (sig) = 65 bytes
  if (raw.length < 1 + PAYMENT_HASH_SIZE + HMAC_SIZE) {
    throw new Error('Macaroon too short to be valid.');
  }

  // Verify version
  if (raw[0] !== VERSION_BYTE) {
    throw new Error(`Unsupported macaroon version: 0x${raw[0].toString(16)}`);
  }

  // Extract body (everything except last 32 bytes) and sig
  const body = raw.slice(0, raw.length - HMAC_SIZE);
  const sigFromMacaroon = raw.slice(raw.length - HMAC_SIZE);

  // Recompute expected HMAC
  const expectedSig = hmacSha256(rootKey, body);
  const signatureValid = crypto.timingSafeEqual(sigFromMacaroon, expectedSig);

  // Extract payment hash from body bytes [1..32]
  const paymentHashBuf = body.slice(1, 1 + PAYMENT_HASH_SIZE);
  const paymentHash = paymentHashBuf.toString('hex');

  // Decode caveats from body bytes [33..]
  const caveatBuf = body.slice(1 + PAYMENT_HASH_SIZE);
  const caveats = decodeCaveats(caveatBuf);

  // Extract well-known caveats
  let expiresAt = null;
  let resource = null;
  for (const c of caveats) {
    if (c.type === CAVEAT_TYPE_EXPIRY && c.value.length === 8) {
      expiresAt = decodeExpiryValue(c.value);
    } else if (c.type === CAVEAT_TYPE_RESOURCE) {
      resource = c.value.toString('utf8');
    }
  }

  return { signatureValid, paymentHash, caveats, expiresAt, resource };
}

/**
 * Validate caveat constraints.
 *
 * @param {object}  opts
 * @param {number|null} opts.expiresAt    Unix timestamp or null
 * @param {string|null} opts.resource     Required resource from macaroon or null
 * @param {string|null} [opts.checkResource]  Resource the caller is requesting. REQUIRED
 *        for a resource-scoped token — omitting it fails closed (resourceUnchecked).
 * @param {number}  [opts.nowSeconds]     Override "now" for testing
 * @returns {{ expired: boolean, resourceMismatch: boolean, resourceUnchecked: boolean, caveatsValid: boolean }}
 */
function checkCaveats({ expiresAt, resource, checkResource, nowSeconds }) {
  const now = nowSeconds !== undefined ? nowSeconds : Math.floor(Date.now() / 1000);

  const expired = expiresAt !== null && now > expiresAt;

  const resourceGiven = checkResource !== undefined && checkResource !== null;
  const resourceMismatch = resource !== null && resourceGiven && resource !== checkResource;
  // ClawHub 3.0.1 scan (concern): a resource-scoped token verified WITHOUT the
  // requested resource used to pass — the caveat was skipped, so a token sold
  // for one path was accepted for any request. Missing context fails closed.
  const resourceUnchecked = resource !== null && !resourceGiven;

  const caveatsValid = !expired && !resourceMismatch && !resourceUnchecked;

  return { expired, resourceMismatch, resourceUnchecked, caveatsValid };
}

/**
 * Verify that SHA-256(preimage_bytes) === payment_hash.
 *
 * @param {string} preimageHex  64-char hex preimage
 * @param {string} paymentHash  64-char hex payment hash
 * @returns {boolean}
 */
function verifyPreimage(preimageHex, paymentHash) {
  if (!/^[0-9a-fA-F]{64}$/.test(preimageHex)) return false;
  if (!/^[0-9a-fA-F]{64}$/.test(paymentHash)) return false;

  const preimageBytes = Buffer.from(preimageHex, 'hex');
  const computed = crypto.createHash('sha256').update(preimageBytes).digest('hex');
  return computed.toLowerCase() === paymentHash.toLowerCase();
}

// ── Exports ──────────────────────────────────────────────────────────────────

module.exports = {
  // Constants (exported for tests)
  VERSION_BYTE,
  CAVEAT_TYPE_EXPIRY,
  CAVEAT_TYPE_RESOURCE,
  ROOT_KEY_FILE,

  // Root key
  getRootKey,

  // TLV helpers
  encodeCaveats,
  decodeCaveats,
  encodeExpiryValue,
  decodeExpiryValue,

  // HMAC
  hmacSha256,

  // Macaroon lifecycle
  createMacaroon,
  decodeMacaroon,
  checkCaveats,
  verifyPreimage,
};
