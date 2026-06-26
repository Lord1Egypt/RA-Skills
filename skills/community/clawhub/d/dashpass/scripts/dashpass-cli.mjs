/**
 * dashpass-cli.mjs
 * DashPass Vault v2 CLI — credential CRUD for AI agents on Dash Platform
 *
 * Commands: put, get, list, rotate, check, status, delete, env, init-shares, share-status
 * Encryption: Scheme C (ECDH self-sign + HKDF-SHA256 + AES-256-GCM)
 * Mutual Confirmation: Shamir 2-of-2 over GF(2^8) — both shares required to decrypt
 * Contract: GCeh2gnvtiHrujq37ZcKnhZ64xpzDC1LMCLhrUJzKDQF (v2)
 *
 * Usage:
 *   node dashpass-cli.mjs put          --service <svc> --type <t> --level <l> --value <v> --label <lbl> [--expires-in <dur>] [--value-stdin]
 *   node dashpass-cli.mjs get          --service <svc> [--json] [--pipe] [--mutual]
 *   node dashpass-cli.mjs list         [--type <t>] [--level <l>]
 *   node dashpass-cli.mjs rotate       --service <svc> --new-value <v> [--value-stdin]
 *   node dashpass-cli.mjs check        --expiring-within <dur>
 *   node dashpass-cli.mjs status
 *   node dashpass-cli.mjs delete       --service <svc>
 *   node dashpass-cli.mjs env          --services <svc1,svc2,...> [--prefix <pfx>] [--null-if-missing]
 *   node dashpass-cli.mjs init-shares  — split CRITICAL_WIF into 2-of-2 Shamir shares
 *   node dashpass-cli.mjs share-status — check health of stored shares
 *
 * Global options:
 *   --identity-id <id>     Override DASHPASS_IDENTITY_ID env var
 *
 * Environment:
 *   CRITICAL_WIF          — wallet private key (WIF format)
 *   DASHPASS_IDENTITY_ID  — Dash Platform identity (required)
 *   DASHPASS_CONTRACT_ID  — DashPass contract (optional, has default)
 */

import {
  createHash,
  createECDH,
  hkdfSync,
  createCipheriv,
  createDecipheriv,
  randomBytes,
} from 'node:crypto';
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';
import { EvoSDK, Document, Identifier, IdentitySigner } from '@dashevo/evo-sdk';
import {
  initSharesFromWif,
  sharesExist,
  shareStatus,
  readShareA,
  readShareB,
  requestDecrypt,
  approveDecrypt,
  executeDecrypt,
} from './mutual-confirm.mjs';

// ── Environment variables ──────────────────────────────────────────────────
const DEFAULT_CONTRACT_ID = 'GCeh2gnvtiHrujq37ZcKnhZ64xpzDC1LMCLhrUJzKDQF';

const CONTRACT_ID  = process.env.DASHPASS_CONTRACT_ID || DEFAULT_CONTRACT_ID;
// IDENTITY_ID resolved after arg parsing (--identity-id can override env)
let IDENTITY_ID = process.env.DASHPASS_IDENTITY_ID;
const CRITICAL_WIF = process.env.CRITICAL_WIF;
const CACHE_DIR    = join(homedir(), '.dashpass', 'cache');
const CACHE_FILE   = join(CACHE_DIR, 'credentials.enc');
const CACHE_TTL    = 300_000; // 5 minutes
const CACHE_ENABLED = process.env.DASHPASS_CACHE !== 'none';

if (!CRITICAL_WIF) {
  console.error('[fatal] CRITICAL_WIF not set. Export CRITICAL_WIF with your wallet WIF.');
  process.exit(1);
}

if (CONTRACT_ID === DEFAULT_CONTRACT_ID) {
  console.error('[warn] Using shared testnet contract. Set DASHPASS_CONTRACT_ID for your own vault.');
}

process.on('uncaughtException', e => {
  console.error('[fatal] Uncaught exception:', e?.message);
  process.exit(1);
});

// ── WIF decoder (pure JS) ───────────────────────────────────────────────────
const BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz';

function base58Decode(str) {
  let num = 0n;
  for (const char of str) {
    const idx = BASE58_ALPHABET.indexOf(char);
    if (idx < 0) throw new Error(`Invalid base58 character: '${char}'`);
    num = num * 58n + BigInt(idx);
  }
  const hex    = num.toString(16);
  const padded = hex.length % 2 === 0 ? hex : '0' + hex;
  const bytes  = Buffer.from(padded, 'hex');
  let leadingZeros = 0;
  for (const char of str) {
    if (char !== '1') break;
    leadingZeros++;
  }
  return Buffer.concat([Buffer.alloc(leadingZeros), bytes]);
}

function sha256(buf) {
  return createHash('sha256').update(buf).digest();
}

function sha256d(buf) {
  return sha256(sha256(buf));
}

function wifToPrivateKey(wif) {
  const decoded = base58Decode(wif);
  if (decoded.length < 37) throw new Error('WIF decode: buffer too short');
  const payload  = decoded.slice(0, decoded.length - 4);
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

// ── Scheme C — ECDH self-sign + HKDF + AES-256-GCM ─────────────────────────

function deriveAesKey(wif, salt) {
  const privKeyBytes = wifToPrivateKey(wif);
  const ecdh = createECDH('secp256k1');
  ecdh.setPrivateKey(privKeyBytes);
  const sharedSecret = ecdh.computeSecret(ecdh.getPublicKey());
  privKeyBytes.fill(0); // Zero private key buffer
  const key = Buffer.from(hkdfSync('sha256', sharedSecret, salt, 'dashpass-v1', 32));
  return key;
}

function encrypt(wif, payload) {
  const salt  = randomBytes(32);
  const nonce = randomBytes(12);
  const aesKey = deriveAesKey(wif, salt);
  const cipher = createCipheriv('aes-256-gcm', aesKey, nonce);
  const plain  = Buffer.from(JSON.stringify(payload), 'utf8');
  const ct     = Buffer.concat([cipher.update(plain), cipher.final()]);
  const tag    = cipher.getAuthTag();
  return { encryptedBlob: Buffer.concat([ct, tag]), salt, nonce };
}

function decrypt(wif, encryptedBlobBuf, saltBuf, nonceBuf) {
  const aesKey   = deriveAesKey(wif, saltBuf);
  const tag      = encryptedBlobBuf.slice(encryptedBlobBuf.length - 16);
  const ct       = encryptedBlobBuf.slice(0, encryptedBlobBuf.length - 16);
  const decipher = createDecipheriv('aes-256-gcm', aesKey, nonceBuf);
  decipher.setAuthTag(tag);
  const plain = Buffer.concat([decipher.update(ct), decipher.final()]);
  return JSON.parse(plain.toString('utf8'));
}

// ── Argument parser ─────────────────────────────────────────────────────────

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith('--')) {
      const key = argv[i].slice(2);
      const val = (argv[i + 1] && !argv[i + 1].startsWith('--')) ? argv[++i] : true;
      args[key] = val;
    }
  }
  return args;
}

// ── Duration parser (e.g. "1d", "7d", "12h", "30m") ────────────────────────

function parseDuration(str) {
  const match = str.match(/^(\d+)([smhd])$/);
  if (!match) throw new Error(`Invalid duration: "${str}" (expected e.g. 30m, 12h, 7d)`);
  const [, num, unit] = match;
  const multipliers = { s: 1000, m: 60_000, h: 3_600_000, d: 86_400_000 };
  return parseInt(num) * multipliers[unit];
}

// ── Cache helpers ───────────────────────────────────────────────────────────

function ensureCacheDir() {
  mkdirSync(CACHE_DIR, { recursive: true, mode: 0o700 });
}

function deriveCacheKey(wif) {
  const privKeyBytes = wifToPrivateKey(wif);
  const key = Buffer.from(hkdfSync('sha256', privKeyBytes, 'dashpass-cache-salt', 'dashpass-cache-v1', 32));
  privKeyBytes.fill(0);
  return key;
}

function cacheReadAll() {
  const blob = readFileSync(CACHE_FILE);
  if (blob.length < 28) return {}; // nonce(12) + tag(16) = min 28
  const nonce = blob.slice(0, 12);
  const tag = blob.slice(12, 28);
  const ct = blob.slice(28);
  const cacheKey = deriveCacheKey(CRITICAL_WIF);
  const decipher = createDecipheriv('aes-256-gcm', cacheKey, nonce);
  decipher.setAuthTag(tag);
  const plain = Buffer.concat([decipher.update(ct), decipher.final()]);
  cacheKey.fill(0);
  return JSON.parse(plain.toString('utf8'));
}

function cacheGet(service) {
  if (!CACHE_ENABLED) return null;
  try {
    const cache = cacheReadAll();
    const entry = cache[service];
    if (entry && Date.now() - entry.ts < CACHE_TTL) return entry.data;
  } catch { /* cache miss or decryption failure */ }
  return null;
}

function cacheSet(service, data) {
  if (!CACHE_ENABLED) return;
  ensureCacheDir();
  let cache = {};
  try {
    cache = cacheReadAll();
  } catch { /* new cache */ }
  cache[service] = { data, ts: Date.now() };
  const plaintext = Buffer.from(JSON.stringify(cache), 'utf8');
  const nonce = randomBytes(12);
  const cacheKey = deriveCacheKey(CRITICAL_WIF);
  const cipher = createCipheriv('aes-256-gcm', cacheKey, nonce);
  const ct = Buffer.concat([cipher.update(plaintext), cipher.final()]);
  const tag = cipher.getAuthTag();
  cacheKey.fill(0);
  // Format: nonce(12) + tag(16) + ciphertext
  const blob = Buffer.concat([nonce, tag, ct]);
  writeFileSync(CACHE_FILE, blob, { mode: 0o600 });
}

function cacheInvalidate(service) {
  try {
    const cache = cacheReadAll();
    delete cache[service];
    // Re-encrypt and write back
    const plaintext = Buffer.from(JSON.stringify(cache), 'utf8');
    const nonce = randomBytes(12);
    const cacheKey = deriveCacheKey(CRITICAL_WIF);
    const cipher = createCipheriv('aes-256-gcm', cacheKey, nonce);
    const ct = Buffer.concat([cipher.update(plaintext), cipher.final()]);
    const tag = cipher.getAuthTag();
    cacheKey.fill(0);
    ensureCacheDir();
    writeFileSync(CACHE_FILE, Buffer.concat([nonce, tag, ct]), { mode: 0o600 });
  } catch { /* no cache */ }
}

// ── SDK connection ──────────────────────────────────────────────────────────

let _sdkCache = null;

async function connectSDK() {
  if (_sdkCache) return _sdkCache;

  console.error('[sdk] Connecting to testnet...');
  const platformVersion = await EvoSDK.getLatestVersionNumber();
  const sdk = EvoSDK.testnetTrusted({ version: platformVersion, settings: { timeoutMs: 30000 } });
  await sdk.connect();
  console.error('[sdk] Connected (platform v' + platformVersion + ')');

  const identity     = await sdk.identities.fetch(IDENTITY_ID);
  const identityJson = JSON.parse(JSON.stringify(identity));
  const authKey      = identityJson.publicKeys.find(k => k.purpose === 0 && k.securityLevel === 1);
  if (!authKey) throw new Error('No AUTH/CRITICAL key found on identity');

  const signer = new IdentitySigner();
  signer.addKeyFromWif(CRITICAL_WIF);
  const identityKey = identity.getPublicKeyById(authKey.id);

  _sdkCache = { sdk, identity, signer, identityKey, platformVersion };
  return _sdkCache;
}

// ── Query helpers ───────────────────────────────────────────────────────────

/**
 * Query credential documents from Platform.
 * @param {object} sdk - EvoSDK instance
 * @param {object} whereExtra - Additional where clause pairs (after $ownerId)
 * @param {Array}  orderByExtra - Additional orderBy pairs (after $ownerId)
 * @returns {Array<{id: string, data: object, raw: object}>}
 */
async function queryCredentials(sdk, whereExtra = [], orderByExtra = []) {
  const where   = [['$ownerId', '==', IDENTITY_ID], ...whereExtra];
  const orderBy = [['$ownerId', 'asc'], ...orderByExtra];

  const queryResult = await sdk.documents.query({
    dataContractId:   CONTRACT_ID,
    documentTypeName: 'credential',
    where,
    orderBy,
    limit: 100,
  });

  const results = [];
  if (queryResult instanceof Map) {
    queryResult.forEach((doc, id) => results.push({ id: id.toString(), doc }));
  } else if (Array.isArray(queryResult)) {
    queryResult.forEach(doc => results.push({ id: doc.id?.toString?.() ?? '?', doc }));
  }

  // Normalize each doc into a plain object
  return results.map(({ id, doc }) => {
    const raw  = JSON.parse(JSON.stringify(doc));
    const data = raw['$data'] ?? raw;
    return { id, data, raw };
  });
}

/**
 * Decode a byteArray field from Platform query results.
 * byteArray fields come back as base64 strings after JSON round-trip.
 */
function decodeByteArray(val) {
  if (typeof val === 'string') return Buffer.from(val, 'base64');
  if (Buffer.isBuffer(val)) return val;
  if (Array.isArray(val) || val instanceof Uint8Array) return Buffer.from(val);
  throw new Error('Cannot decode byteArray field: unexpected type ' + typeof val);
}

/**
 * Decrypt a credential document's encrypted fields.
 */
function decryptDoc(data) {
  const blobBuf  = decodeByteArray(data.encryptedBlob);
  const saltBuf  = decodeByteArray(data.salt);
  const nonceBuf = decodeByteArray(data.nonce);
  return decrypt(CRITICAL_WIF, blobBuf, saltBuf, nonceBuf);
}

// ── Document creation (2-pass pattern) ──────────────────────────────────────

async function createCredentialDoc(ctx, docData) {
  const { sdk, identity, signer, identityKey } = ctx;
  const ownerBytes    = Identifier.fromBase58(IDENTITY_ID).toBytes();
  const contractBytes = Identifier.fromBase58(CONTRACT_ID).toBytes();
  const entropy       = randomBytes(32);

  const docBase = {
    '$id':             ownerBytes,
    '$ownerId':        ownerBytes,
    '$dataContractId': contractBytes,
    '$type':           'credential',
    '$revision':       1,
    '$entropy':        Array.from(entropy),
    ...docData,
  };

  // Pass 1
  let correctId;
  try {
    const d = Document.fromObject(docBase);
    await sdk.documents.create({ document: d, identity, signer, identityKey });
    return d.id?.toString?.() ?? JSON.parse(JSON.stringify(d.id));
  } catch (e) {
    const m = e?.message?.match(/expected ([A-Za-z0-9]{43,44})/);
    if (!m) throw e;
    correctId = m[1];
  }

  // Pass 2 — use correct ID from error
  const d2 = Document.fromObject({
    ...docBase,
    '$id': Identifier.fromBase58(correctId).toBytes(),
  });
  await sdk.documents.create({ document: d2, identity, signer, identityKey });
  return correctId;
}

// ── Document deletion ───────────────────────────────────────────────────────

async function deleteCredentialDoc(ctx, docId, docData) {
  const { sdk, identity, signer, identityKey } = ctx;
  const ownerBytes    = Identifier.fromBase58(IDENTITY_ID).toBytes();
  const contractBytes = Identifier.fromBase58(CONTRACT_ID).toBytes();

  // Reconstruct the document for deletion
  // Need all required fields + correct $id and $revision
  const revision = docData['$revision'] ?? docData.revision ?? 1;
  const docObj = {
    '$id':             Identifier.fromBase58(docId).toBytes(),
    '$ownerId':        ownerBytes,
    '$dataContractId': contractBytes,
    '$type':           'credential',
    '$revision':       revision,
    service:       docData.service,
    label:         docData.label ?? '',
    encryptedBlob: decodeByteArray(docData.encryptedBlob),
    salt:          decodeByteArray(docData.salt),
    nonce:         decodeByteArray(docData.nonce),
    authScheme:    docData.authScheme ?? 'identity',
    credType:      docData.credType ?? 'api-key',
    level:         docData.level ?? 'normal',
    version:       docData.version ?? 1,
    status:        docData.status ?? 'active',
  };
  if (docData.expiresAt != null) docObj.expiresAt = docData.expiresAt;
  if (docData.previousDocId) docObj.previousDocId = docData.previousDocId;

  const doc = Document.fromObject(docObj);
  await sdk.documents.delete({ document: doc, identity, signer, identityKey });
}

// ── stdin reader ────────────────────────────────────────────────────────────

async function readStdin() {
  const chunks = [];
  for await (const chunk of process.stdin) {
    chunks.push(chunk);
  }
  return Buffer.concat(chunks).toString('utf8').trim();
}

// ── Command: put ────────────────────────────────────────────────────────────

async function cmdPut(args) {
  const service   = args.service;
  const credType  = args.type || args.credType;
  const level     = args.level;
  const label     = args.label;
  const expiresIn = args['expires-in'];

  let value = args.value;
  if (args['value-stdin'] === true) {
    value = await readStdin();
  }
  if (value && !args['value-stdin']) {
    console.error('WARNING: --value visible in shell history. Use --value-stdin for sensitive credentials.');
  }

  if (!service || !credType || !level || !value || !label) {
    console.error('Usage: put --service <svc> --type <t> --level <l> --value <v> --label <lbl> [--expires-in <dur>] [--value-stdin]');
    console.error('  --type: api-key, oauth-token, ssh-key, wif, db-cred, tls-cert, service-token, encryption-key');
    console.error('  --level: critical, sensitive, normal');
    console.error('  --value-stdin: read value from stdin (recommended for sensitive credentials)');
    process.exit(1);
  }

  let expiresAt = 0;
  if (expiresIn) {
    expiresAt = Date.now() + parseDuration(expiresIn);
  }

  console.log('[put] Service:', service);
  console.log('[put] Type:', credType, '| Level:', level);

  const { encryptedBlob, salt, nonce } = encrypt(CRITICAL_WIF, { value });
  console.log('[put] Encrypted with Scheme C');

  const ctx = await connectSDK();

  const docData = {
    service,
    label,
    encryptedBlob: Uint8Array.from(encryptedBlob),
    salt:          Uint8Array.from(salt),
    nonce:         Uint8Array.from(nonce),
    authScheme:    'identity',
    credType,
    level,
    version:       1,
    status:        'active',
    expiresAt,
  };

  console.log('[put] Writing to Platform...');
  const docId = await createCredentialDoc(ctx, docData);

  console.log('[put] OK');
  console.log('  Document ID:', docId);
  console.log('  Service:', service);
  console.log('  Type:', credType);
  console.log('  Level:', level);
  if (expiresAt > 0) console.log('  Expires:', new Date(expiresAt).toISOString());

  cacheInvalidate(service);
}

// ── Command: get ────────────────────────────────────────────────────────────

async function cmdGet(args) {
  const service = args.service;
  const jsonOut = args.json === true;
  const pipeOut = args.pipe === true;
  const mutual  = args.mutual === true;

  if (!service) {
    console.error('Usage: get --service <svc> [--json] [--pipe] [--mutual]');
    process.exit(1);
  }

  // ── Mutual confirmation path ──
  if (mutual) {
    if (!sharesExist()) {
      console.error('[get] Mutual mode requires shares. Run `init-shares` first.');
      process.exit(1);
    }

    const { sdk } = await connectSDK();
    const docs = await queryCredentials(sdk,
      [['service', '==', service]],
      [['service', 'asc']],
    );
    if (docs.length === 0) {
      console.error(`[get] No credentials found for service="${service}"`);
      process.exit(1);
    }
    const sorted = docs.sort((a, b) => (b.data.version ?? 1) - (a.data.version ?? 1));
    const best = sorted[0];

    // Protocol: request → approve → execute
    const req = requestDecrypt(service, 'cli get --mutual', 'cc');
    approveDecrypt(req, 'evo');

    const shareA = readShareA();
    const shareB = readShareB();

    let decrypted;
    try {
      decrypted = executeDecrypt(
        shareA, shareB,
        decodeByteArray(best.data.encryptedBlob),
        decodeByteArray(best.data.salt),
        decodeByteArray(best.data.nonce),
      );
    } catch (e) {
      console.error('[get] Mutual decryption failed:', e.message);
      process.exit(1);
    }

    const result = {
      id:        best.id,
      service:   best.data.service,
      label:     best.data.label,
      credType:  best.data.credType,
      level:     best.data.level,
      status:    best.data.status,
      version:   best.data.version ?? 1,
      expiresAt: best.data.expiresAt ?? 0,
      decrypted,
    };

    if (pipeOut) { process.stdout.write(decrypted.value); return; }
    if (jsonOut) { console.log(JSON.stringify(result, null, 2)); return; }
    console.log('[get] (mutual confirmation)');
    printCredential(result);
    return;
  }

  // ── Standard Scheme C path ──

  // Check cache first — cache stores encrypted blobs, decrypt on-the-fly
  const cached = cacheGet(service);
  if (cached) {
    let decrypted;
    try {
      decrypted = decrypt(
        CRITICAL_WIF,
        Buffer.from(cached.encryptedBlob, 'base64'),
        Buffer.from(cached.salt, 'base64'),
        Buffer.from(cached.nonce, 'base64'),
      );
    } catch {
      // Cache corrupted or key changed, fall through to Platform query
    }
    if (decrypted) {
      const result = { ...cached, decrypted };
      delete result.encryptedBlob;
      delete result.salt;
      delete result.nonce;
      if (pipeOut) { process.stdout.write(decrypted.value); return; }
      if (jsonOut) { console.log(JSON.stringify(result, null, 2)); return; }
      console.log('[get] (cached)');
      printCredential(result);
      return;
    }
  }

  const { sdk } = await connectSDK();

  const docs = await queryCredentials(sdk,
    [['service', '==', service]],
    [['service', 'asc']],
  );

  if (docs.length === 0) {
    console.error(`[get] No credentials found for service="${service}"`);
    process.exit(1);
  }

  // Pick the latest version (highest version number)
  const sorted = docs.sort((a, b) => (b.data.version ?? 1) - (a.data.version ?? 1));
  const best = sorted[0];

  let decrypted;
  try {
    decrypted = decryptDoc(best.data);
  } catch (e) {
    console.error('[get] Decryption failed:', e.message);
    process.exit(1);
  }

  const result = {
    id:        best.id,
    service:   best.data.service,
    label:     best.data.label,
    credType:  best.data.credType,
    level:     best.data.level,
    status:    best.data.status,
    version:   best.data.version ?? 1,
    expiresAt: best.data.expiresAt ?? 0,
    decrypted,
  };

  // Cache the encrypted document data (NOT the decrypted value)
  const cacheEntry = {
    id:        best.id,
    service:   best.data.service,
    label:     best.data.label,
    credType:  best.data.credType,
    level:     best.data.level,
    status:    best.data.status,
    version:   best.data.version ?? 1,
    expiresAt: best.data.expiresAt ?? 0,
    encryptedBlob: decodeByteArray(best.data.encryptedBlob).toString('base64'),
    salt:          decodeByteArray(best.data.salt).toString('base64'),
    nonce:         decodeByteArray(best.data.nonce).toString('base64'),
  };
  cacheSet(service, cacheEntry);

  if (pipeOut) {
    process.stdout.write(decrypted.value);
    return;
  }
  if (jsonOut) {
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  printCredential(result);
}

function printCredential(cred) {
  console.log('---');
  console.log('  Document ID:', cred.id);
  console.log('  Service:    ', cred.service);
  console.log('  Label:      ', cred.label);
  console.log('  Type:       ', cred.credType);
  console.log('  Level:      ', cred.level);
  console.log('  Status:     ', cred.status);
  console.log('  Version:    ', cred.version);
  if (cred.expiresAt > 0) {
    const exp = new Date(cred.expiresAt);
    const remaining = cred.expiresAt - Date.now();
    const days = Math.floor(remaining / 86_400_000);
    const hours = Math.floor((remaining % 86_400_000) / 3_600_000);
    console.log('  Expires:    ', exp.toISOString(), `(${days}d ${hours}h remaining)`);
  } else {
    console.log('  Expires:     never');
  }
  console.log('  Value:      ', cred.decrypted?.value ?? '(none)');
  console.log('---');
}

// ── Command: list ───────────────────────────────────────────────────────────

async function cmdList(args) {
  const filterType  = args.type || args.credType;
  const filterLevel = args.level;

  const { sdk } = await connectSDK();

  let docs;
  if (filterType) {
    console.log(`[list] Filtering by type="${filterType}"`);
    docs = await queryCredentials(sdk,
      [['credType', '==', filterType]],
      [['credType', 'asc']],
    );
  } else if (filterLevel) {
    console.log(`[list] Filtering by level="${filterLevel}"`);
    docs = await queryCredentials(sdk,
      [['level', '==', filterLevel]],
      [['level', 'asc']],
    );
  } else {
    console.log('[list] All active credentials');
    docs = await queryCredentials(sdk,
      [['status', '==', 'active']],
      [['status', 'asc']],
    );
  }

  if (docs.length === 0) {
    console.log('[list] No credentials found');
    return;
  }

  console.log(`\nFound ${docs.length} credential(s):\n`);
  console.log('SERVICE'.padEnd(25) + 'TYPE'.padEnd(15) + 'LEVEL'.padEnd(12) + 'VER'.padEnd(5) + 'STATUS'.padEnd(10) + 'LABEL');
  console.log('-'.repeat(80));

  for (const { data } of docs) {
    const svc    = (data.service ?? '?').padEnd(25);
    const type   = (data.credType ?? '?').padEnd(15);
    const lvl    = (data.level ?? '?').padEnd(12);
    const ver    = String(data.version ?? 1).padEnd(5);
    const status = (data.status ?? '?').padEnd(10);
    const label  = data.label ?? '';
    console.log(svc + type + lvl + ver + status + label);
  }
}

// ── Command: rotate ─────────────────────────────────────────────────────────

async function cmdRotate(args) {
  const service  = args.service;

  let newValue = args['new-value'];
  if (args['value-stdin'] === true) {
    newValue = await readStdin();
  }
  if (newValue && !args['value-stdin'] && args['new-value']) {
    console.error('WARNING: --new-value visible in shell history. Use --value-stdin for sensitive credentials.');
  }

  if (!service || !newValue) {
    console.error('Usage: rotate --service <svc> --new-value <v> [--value-stdin]');
    console.error('  --value-stdin: read new value from stdin (recommended for sensitive credentials)');
    process.exit(1);
  }

  const ctx = await connectSDK();
  const { sdk } = ctx;

  // Find existing credential
  const docs = await queryCredentials(sdk,
    [['service', '==', service]],
    [['service', 'asc']],
  );

  if (docs.length === 0) {
    console.error(`[rotate] No credentials found for service="${service}"`);
    process.exit(1);
  }

  // Pick latest version
  const sorted = docs.sort((a, b) => (b.data.version ?? 1) - (a.data.version ?? 1));
  const current = sorted[0];
  const currentVersion = current.data.version ?? 1;

  console.log(`[rotate] Current version: ${currentVersion}, doc: ${current.id}`);
  console.log('[rotate] Creating new version:', currentVersion + 1);

  // Encrypt new value
  const { encryptedBlob, salt, nonce } = encrypt(CRITICAL_WIF, { value: newValue });

  const docData = {
    service,
    label:         current.data.label ?? service,
    encryptedBlob: Uint8Array.from(encryptedBlob),
    salt:          Uint8Array.from(salt),
    nonce:         Uint8Array.from(nonce),
    authScheme:    'identity',
    credType:      current.data.credType ?? 'api-key',
    level:         current.data.level ?? 'normal',
    version:       currentVersion + 1,
    status:        'active',
    expiresAt:     current.data.expiresAt ?? 0,
    previousDocId: current.id,
  };

  const docId = await createCredentialDoc(ctx, docData);

  console.log('[rotate] OK');
  console.log('  New Document ID:', docId);
  console.log('  Version:', currentVersion + 1);
  console.log('  Previous:', current.id);

  cacheInvalidate(service);
}

// ── Command: check ──────────────────────────────────────────────────────────

async function cmdCheck(args) {
  const within = args['expiring-within'];
  if (!within) {
    console.error('Usage: check --expiring-within <dur> (e.g. 7d, 24h)');
    process.exit(1);
  }

  const windowMs = parseDuration(within);
  const deadline = Date.now() + windowMs;

  const { sdk } = await connectSDK();

  // Query all active credentials
  const docs = await queryCredentials(sdk,
    [['status', '==', 'active']],
    [['status', 'asc']],
  );

  const expiring = docs.filter(({ data }) => {
    const exp = data.expiresAt ?? 0;
    return exp > 0 && exp <= deadline;
  });

  const expired = docs.filter(({ data }) => {
    const exp = data.expiresAt ?? 0;
    return exp > 0 && exp <= Date.now();
  });

  console.log(`[check] Window: ${within} (until ${new Date(deadline).toISOString()})`);
  console.log(`[check] Total active: ${docs.length}`);
  console.log(`[check] Already expired: ${expired.length}`);
  console.log(`[check] Expiring within window: ${expiring.length}`);

  if (expiring.length === 0 && expired.length === 0) {
    console.log('[check] All credentials are healthy');
    return;
  }

  if (expired.length > 0) {
    console.log('\nEXPIRED:');
    for (const { data } of expired) {
      console.log(`  - ${data.service} (expired ${new Date(data.expiresAt).toISOString()})`);
    }
  }

  if (expiring.length > 0) {
    console.log('\nEXPIRING SOON:');
    for (const { data } of expiring) {
      const remaining = data.expiresAt - Date.now();
      const days  = Math.floor(remaining / 86_400_000);
      const hours = Math.floor((remaining % 86_400_000) / 3_600_000);
      console.log(`  - ${data.service} (expires ${new Date(data.expiresAt).toISOString()}, ${days}d ${hours}h left)`);
    }
  }
}

// ── Command: status ─────────────────────────────────────────────────────────

async function cmdStatus() {
  const { sdk } = await connectSDK();

  console.log('[status] DashPass Vault v2');
  console.log('  Contract:', CONTRACT_ID);
  console.log('  Identity:', IDENTITY_ID);

  // Check balance
  const balance = await sdk.identities.balance(IDENTITY_ID);
  console.log('  Balance: ', String(balance), 'credits');

  // Fetch contract to verify it exists
  const contract = await sdk.contracts.fetch(CONTRACT_ID);
  if (!contract) {
    console.error('[status] Contract not found on Platform!');
    process.exit(1);
  }
  const schemas = contract.schemas;
  console.log('  Doc types:', Object.keys(schemas).join(', '));

  // Count active credentials
  const activeDocs = await queryCredentials(sdk,
    [['status', '==', 'active']],
    [['status', 'asc']],
  );
  console.log('  Active credentials:', activeDocs.length);

  // Check for expiring (within 7 days)
  const deadline = Date.now() + 7 * 86_400_000;
  const expiring = activeDocs.filter(({ data }) => {
    const exp = data.expiresAt ?? 0;
    return exp > 0 && exp <= deadline;
  });
  if (expiring.length > 0) {
    console.log('  Expiring within 7d:', expiring.length);
  }

  console.log('[status] OK');
}

// ── Command: delete ─────────────────────────────────────────────────────────

async function cmdDelete(args) {
  const service = args.service;
  if (!service) {
    console.error('Usage: delete --service <svc>');
    process.exit(1);
  }

  const ctx = await connectSDK();
  const { sdk } = ctx;

  const docs = await queryCredentials(sdk,
    [['service', '==', service]],
    [['service', 'asc']],
  );

  if (docs.length === 0) {
    console.error(`[delete] No credentials found for service="${service}"`);
    process.exit(1);
  }

  console.log(`[delete] Found ${docs.length} document(s) for service="${service}"`);

  for (const { id, data, raw } of docs) {
    console.log(`[delete] Deleting document ${id}...`);
    try {
      await deleteCredentialDoc(ctx, id, { ...data, ...raw });
      console.log(`[delete] Deleted: ${id}`);
    } catch (e) {
      console.error(`[delete] Failed to delete ${id}:`, e?.message?.slice(0, 200));
      throw e;
    }
  }

  console.log(`[delete] OK — removed ${docs.length} document(s)`);
  cacheInvalidate(service);
}

// ── Command: env ───────────────────────────────────────────────────────────

/**
 * Service name → env var name lookup table.
 * Covers common services; unknown services fall back to uppercase with
 * hyphens/dots replaced by underscores.
 */
const SERVICE_ENV_MAP = {
  'anthropic-api':    'ANTHROPIC_API_KEY',
  'xai-api':          'XAI_API_KEY',
  'openai-api':       'OPENAI_API_KEY',
  'brave-search-api': 'BRAVE_API_KEY',
  'github-token':     'GITHUB_TOKEN',
  'slack-token':      'SLACK_TOKEN',
  'discord-token':    'DISCORD_TOKEN',
  'aws-access-key':   'AWS_ACCESS_KEY_ID',
  'aws-secret-key':   'AWS_SECRET_ACCESS_KEY',
  'database-url':     'DATABASE_URL',
  'redis-url':        'REDIS_URL',
  'dashpass-wif':     'CRITICAL_WIF',
};

function serviceToEnvVar(service, prefix) {
  let varName = SERVICE_ENV_MAP[service];
  if (!varName) {
    varName = service.toUpperCase().replace(/[-. ]/g, '_');
  }
  if (prefix) {
    varName = prefix + varName;
  }
  // Validate: must be a legal shell variable name
  if (!/^[A-Za-z_][A-Za-z0-9_]*$/.test(varName)) {
    throw new Error(`Invalid env var name "${varName}" derived from service="${service}"`);
  }
  return varName;
}

async function cmdEnv(args) {
  const servicesRaw   = args.services;
  const prefix        = args.prefix || '';
  const nullIfMissing = args['null-if-missing'] === true;

  if (!servicesRaw) {
    console.error('Usage: env --services <svc1,svc2,...> [--prefix <pfx>] [--null-if-missing]');
    console.error('');
    console.error('Outputs `export VAR="value"` lines for eval $(...).');
    console.error('Service names are mapped to env var names via a lookup table.');
    console.error('Unknown services use uppercase with hyphens replaced by underscores.');
    process.exit(1);
  }

  const services = servicesRaw.split(',').map(s => s.trim()).filter(Boolean);
  if (services.length === 0) {
    console.error('[env] No services specified');
    process.exit(1);
  }

  const { sdk } = await connectSDK();

  for (const service of services) {
    const varName = serviceToEnvVar(service, prefix);

    try {
      // Check cache first
      const cached = cacheGet(service);
      let decrypted;

      if (cached) {
        try {
          decrypted = decrypt(
            CRITICAL_WIF,
            Buffer.from(cached.encryptedBlob, 'base64'),
            Buffer.from(cached.salt, 'base64'),
            Buffer.from(cached.nonce, 'base64'),
          );
        } catch { /* cache miss, fall through */ }
      }

      if (!decrypted) {
        const docs = await queryCredentials(sdk,
          [['service', '==', service]],
          [['service', 'asc']],
        );

        if (docs.length === 0) {
          if (nullIfMissing) {
            console.log(`unset ${varName}`);
          } else {
            console.error(`[env] warning: no credential found for service="${service}", skipping ${varName}`);
          }
          continue;
        }

        const best = docs.sort((a, b) => (b.data.version ?? 1) - (a.data.version ?? 1))[0];
        decrypted = decryptDoc(best.data);

        // Populate cache
        const cacheEntry = {
          id:        best.id,
          service:   best.data.service,
          label:     best.data.label,
          credType:  best.data.credType,
          level:     best.data.level,
          status:    best.data.status,
          version:   best.data.version ?? 1,
          expiresAt: best.data.expiresAt ?? 0,
          encryptedBlob: decodeByteArray(best.data.encryptedBlob).toString('base64'),
          salt:          decodeByteArray(best.data.salt).toString('base64'),
          nonce:         decodeByteArray(best.data.nonce).toString('base64'),
        };
        cacheSet(service, cacheEntry);
      }

      // Escape for safe use inside double-quoted shell string
      const escaped = decrypted.value
        .replace(/\\/g, '\\\\')
        .replace(/`/g, '\\`')
        .replace(/\$/g, '\\$')
        .replace(/"/g, '\\"');
      console.log(`export ${varName}="${escaped}"`);
    } catch (err) {
      console.error(`[env] warning: failed to fetch service="${service}": ${err?.message?.slice(0, 150)}`);
      if (nullIfMissing) {
        console.log(`unset ${varName}`);
      }
    }
  }
}

// ── Command: init-shares ────────────────────────────────────────────────────

async function cmdInitShares() {
  if (sharesExist()) {
    console.error('[init-shares] Shares already exist. Delete ~/.dashpass/evo.share and cc.share first to re-initialize.');
    process.exit(1);
  }

  console.log('[init-shares] Splitting CRITICAL_WIF into Shamir 2-of-2 shares...');
  const { shareA, shareB } = initSharesFromWif(wifToPrivateKey, CRITICAL_WIF);

  console.log('[init-shares] OK');
  console.log('  Share A (evo): ~/.dashpass/evo.share');
  console.log('  Share B (cc):  ~/.dashpass/cc.share');
  console.log('  Key length:   ', shareA.length / 2, 'bytes');
  console.log('  Permissions:   0600');
  console.log('  Round-trip:    verified');
}

// ── Command: share-status ──────────────────────────────────────────────────

async function cmdShareStatus() {
  const status = shareStatus();

  console.log('[share-status] Mutual Confirmation Shares');
  console.log('');

  for (const [label, info] of [['Evo (Share A)', status.evo], ['CC  (Share B)', status.cc]]) {
    if (!info.exists) {
      console.log(`  ${label}: NOT FOUND`);
    } else {
      console.log(`  ${label}:`);
      console.log(`    Path:       ${info.path}`);
      console.log(`    Permissions: ${info.permissions}`);
      console.log(`    Size:        ${info.bytes} bytes`);
      console.log(`    Healthy:     ${info.healthy ? 'yes' : 'NO — unexpected format'}`);
    }
  }

  const bothHealthy = status.evo.healthy && status.cc.healthy;
  console.log('');
  console.log(`  Mutual confirmation: ${bothHealthy ? 'READY' : 'NOT READY'}`);
}

// ── Entry point ─────────────────────────────────────────────────────────────

const COMMANDS = {
  put: cmdPut, get: cmdGet, list: cmdList, rotate: cmdRotate,
  check: cmdCheck, status: cmdStatus, delete: cmdDelete, env: cmdEnv,
  'init-shares': cmdInitShares, 'share-status': cmdShareStatus,
};

// Commands that don't need IDENTITY_ID
const NO_IDENTITY_COMMANDS = new Set(['init-shares', 'share-status']);

async function main() {
  const [,, command, ...rest] = process.argv;
  const args = parseArgs(rest);

  // --identity-id flag overrides env var (available to all commands)
  if (args['identity-id']) {
    IDENTITY_ID = args['identity-id'];
  }

  if (!command || !COMMANDS[command]) {
    console.error('DashPass Vault v2 CLI');
    console.error('');
    console.error('Commands:');
    console.error('  put          --service <svc> --type <t> --level <l> --value <v> --label <lbl> [--expires-in <dur>] [--value-stdin]');
    console.error('  get          --service <svc> [--json] [--pipe] [--mutual]');
    console.error('  list         [--type <t>] [--level <l>]');
    console.error('  rotate       --service <svc> --new-value <v> [--value-stdin]');
    console.error('  check        --expiring-within <dur>');
    console.error('  status');
    console.error('  delete       --service <svc>');
    console.error('  env          --services <svc1,svc2,...> [--prefix <pfx>] [--null-if-missing]');
    console.error('  init-shares  Split CRITICAL_WIF into Shamir 2-of-2 shares');
    console.error('  share-status Check health of stored shares');
    console.error('');
    console.error('Global options:');
    console.error('  --identity-id <id>  Override DASHPASS_IDENTITY_ID env var');
    process.exit(1);
  }

  // Only require IDENTITY_ID for commands that need Platform access
  if (!NO_IDENTITY_COMMANDS.has(command) && !IDENTITY_ID) {
    console.error('[fatal] DASHPASS_IDENTITY_ID not set. Use --identity-id or export DASHPASS_IDENTITY_ID.');
    process.exit(1);
  }

  await COMMANDS[command](args);
}

main().then(() => {
  delete process.env.CRITICAL_WIF;
}).catch(e => {
  delete process.env.CRITICAL_WIF;
  console.error('\n[fatal]', e?.message || e);
  if (e?.stack) console.error(e.stack);
  process.exit(1);
});
