#!/usr/bin/env node
/**
 * Blink Wallet - L402 Token Store
 *
 * Usage:
 *   node l402_store.js list
 *   node l402_store.js get <url|key>
 *   node l402_store.js clear [--expired]
 *
 * Manages a local cache of L402 tokens at ~/.blink/l402-tokens.json.
 * Tokens are keyed by ORIGIN (scheme + host + port) + path — see storeKeyFor —
 * and include the macaroon, preimage, and optional expiration time.
 *
 * This cache is used by l402_pay.js to reuse valid tokens and avoid
 * re-paying for access already purchased. A token is only ever sent back to
 * the exact origin that earned it.
 *
 * Arguments (when used as CLI):
 *   list              - Show all cached tokens (masks preimage for safety).
 *                       Pre-3.0.1 host+path entries are flagged legacy: true.
 *   get <url|key>     - Get the stored token for a URL (normalized to its key)
 *                       or a raw store key.
 *   clear [--expired] - Remove expired tokens (or all tokens without --expired).
 *
 * Dependencies: None (uses Node.js built-in fs/path/os)
 *
 * Output: JSON to stdout. Status messages to stderr.
 */

'use strict';

const { exitAfterStdout, strictArgv, assertPositionalCount } = require('./_blink_client');

const fs = require('node:fs');
const { ensureSecureStateDir, writeSecureFileAtomic } = require('./_secure_files');
const path = require('node:path');
const os = require('node:os');

// ── Store path ────────────────────────────────────────────────────────────────

const STORE_DIR = path.join(os.homedir(), '.blink');
const STORE_FILE = path.join(STORE_DIR, 'l402-tokens.json');

// ── Store I/O ─────────────────────────────────────────────────────────────────

/**
 * Read the token store from disk.
 * Returns an empty object if the file does not exist or is unreadable.
 *
 * @returns {object}  Map of domain → token entry.
 */
function readStore() {
  try {
    ensureSecureStateDir(STORE_DIR); // one-time migration: 0644 -> 0600
  } catch {
    // Best-effort hardening on read.
  }
  try {
    const content = fs.readFileSync(STORE_FILE, 'utf8');
    return JSON.parse(content);
  } catch {
    return {};
  }
}

/**
 * Write the token store to disk, creating ~/.blink/ if needed.
 *
 * @param {object} store
 */
function writeStore(store) {
  // The token store holds macaroons + preimages — a reusable bearer
  // credential pair (audit: previously umask-dependent 0644). Atomic, 0600,
  // symlink-refusing (mirrors l402-root-key and the Spark state dir).
  try {
    writeSecureFileAtomic(STORE_FILE, JSON.stringify(store, null, 2));
  } catch (err) {
    throw new Error(`Failed to write token store: ${err.message}`);
  }
}

// ── Store keys ────────────────────────────────────────────────────────────────

/**
 * Build the token store key for a URL: ORIGIN (scheme + host + port) + path,
 * no query/fragment, trailing slashes stripped.
 *
 * Origin isolation (ClawHub review of v3.0.0): the key was previously
 * hostname + path, so a macaroon + preimage (a reusable bearer credential)
 * paid for at http://h:8080/x was replayed to a DIFFERENT service at
 * http://h:9090/x — and from https to plaintext http. Different paths on one
 * origin may carry different challenges (price, caveats), so the path stays in
 * the key too.
 *
 * Returns null — never a raw-string fallback — for anything that is not an
 * http(s) URL: an unkeyable URL is neither cached nor reused.
 *
 * @param {string} url
 * @returns {string | null}  e.g. "https://api.citrusrate.com/v1/btc"
 */
function storeKeyFor(url) {
  let u;
  try {
    u = new URL(url);
  } catch {
    return null;
  }
  if (u.protocol !== 'https:' && u.protocol !== 'http:') return null;
  return u.origin + u.pathname.replace(/\/+$/, '');
}

/**
 * A pre-3.0.1 host+path key (no scheme). Its origin is unknowable, so it is
 * never reused — storeKeyFor keys always start with a scheme and cannot collide
 * with it. Kept on disk (listed with legacy: true) until the user clears it.
 *
 * @param {string} key
 * @returns {boolean}
 */
function isLegacyKey(key) {
  return !/^https?:\/\//.test(key);
}

// ── Token expiry ──────────────────────────────────────────────────────────────

/**
 * Expiry (unix ms) from a plain-text first-party caveat in an L402 macaroon,
 * or null. FT8: lightningenable tokens live ~1 h and carry `expires = <unix>`,
 * but the store recorded expiresAt: null and replayed stale tokens (402).
 * Recognized caveats: `expires=<unix>` and `<service>_valid_until=<unix>`
 * (seconds, 9–11 digits; 13 digits = ms). The EARLIEST one wins. Third-party
 * caveat ids are opaque bytes; a 10-digit `expires=` match in random bytes is
 * negligible, and a false match can only make a token look EXPIRED (pay fresh,
 * still budget-gated) — never extend it.
 *
 * @param {string} macaroon  base64 / base64url macaroon
 * @returns {number|null}
 */
function macaroonExpiryMs(macaroon) {
  if (typeof macaroon !== 'string' || !/^[A-Za-z0-9+/_=-]+$/.test(macaroon)) return null;
  const text = Buffer.from(macaroon.replace(/-/g, '+').replace(/_/g, '/'), 'base64').toString('latin1');
  let earliest = null;
  for (const m of text.matchAll(/(?:^|[^A-Za-z0-9])(?:expires|[A-Za-z0-9_]*valid_until)\s*=\s*(\d{9,13})(?!\d)/g)) {
    const n = Number(m[1]);
    const ms = m[1].length >= 13 ? n : n * 1000;
    if (earliest === null || ms < earliest) earliest = ms;
  }
  return earliest;
}

/** An entry's expiry: the recorded one, else its macaroon's caveat (entries cached before 3.0.3). */
function entryExpiresAt(entry) {
  if (!entry) return null;
  if (typeof entry.expiresAt === 'number') return entry.expiresAt;
  return macaroonExpiryMs(entry.macaroon);
}

// ── Token operations ──────────────────────────────────────────────────────────

/**
 * Save an L402 token for a domain.
 *
 * @param {string} domain     e.g. "stock.l402.org"
 * @param {object} tokenData
 * @param {string} tokenData.macaroon    Base64 macaroon string.
 * @param {string} tokenData.preimage    64-char hex payment preimage.
 * @param {string} [tokenData.invoice]   BOLT-11 invoice (for reference).
 * @param {number} [tokenData.satoshis]  Amount paid in sats.
 * @param {number} [tokenData.expiresAt] Unix timestamp (ms) when token expires.
 */
function saveToken(domain, tokenData) {
  const store = readStore();
  store[domain] = {
    ...tokenData,
    // Record the server's own expiry when the caller did not pass one (FT8).
    expiresAt: tokenData.expiresAt ?? macaroonExpiryMs(tokenData.macaroon),
    savedAt: Date.now(),
  };
  writeStore(store);
}

/**
 * Retrieve a stored token for a domain.
 * Returns null if not found or if expired.
 *
 * @param {string} domain
 * @returns {object | null}
 */
function getToken(domain) {
  const store = readStore();
  const entry = store[domain];
  if (!entry) return null;
  // Check expiry
  const expiresAt = entryExpiresAt(entry);
  if (expiresAt && Date.now() > expiresAt) {
    return null; // expired
  }
  return entry;
}

/**
 * List all stored tokens.
 * Masks the preimage for safety in output.
 *
 * @returns {object[]}
 */
function listTokens() {
  const store = readStore();
  return Object.entries(store).map(([domain, entry]) => {
    const now = Date.now();
    const expiresAtMs = entryExpiresAt(entry);
    const expired = expiresAtMs ? now > expiresAtMs : false;
    const expiresInMs = expiresAtMs ? expiresAtMs - now : null;
    return {
      domain,
      legacy: isLegacyKey(domain),
      macaroon: entry.macaroon ? entry.macaroon.slice(0, 12) + '…' + entry.macaroon.slice(-6) : null,
      preimage: entry.preimage ? entry.preimage.slice(0, 8) + '…' : null,
      satoshis: entry.satoshis ?? null,
      invoiceMsats: entry.invoiceMsats ?? null,
      budgetSats: entry.budgetSats ?? null,
      savedAt: entry.savedAt ? new Date(entry.savedAt).toISOString() : null,
      expiresAt: expiresAtMs ? new Date(expiresAtMs).toISOString() : null,
      expired,
      expiresIn: !expired && expiresInMs !== null ? `${Math.round(expiresInMs / 1000)}s` : null,
    };
  });
}

/**
 * Remove tokens from the store.
 *
 * @param {object} [opts]
 * @param {boolean} [opts.expiredOnly=false]  If true, remove only expired tokens.
 * @returns {number}  Number of tokens removed.
 */
function clearTokens({ expiredOnly = false } = {}) {
  const store = readStore();
  const now = Date.now();
  let removed = 0;

  if (!expiredOnly) {
    removed = Object.keys(store).length;
    writeStore({});
    return removed;
  }

  for (const [domain, entry] of Object.entries(store)) {
    const expiresAt = entryExpiresAt(entry);
    if (expiresAt && now > expiresAt) {
      delete store[domain];
      removed++;
    }
  }
  writeStore(store);
  return removed;
}

// ── CLI ───────────────────────────────────────────────────────────────────────

// Every option l402-store accepts (v3.0.4 strict sweep): `clear --expird` used
// to be ignored as a typo — and then cleared EVERY cached paid token.
const ARG_OPTIONS = { expired: { type: 'boolean' } };

function main() {
  let args;
  try {
    args = strictArgv(process.argv.slice(2), ARG_OPTIONS);
  } catch (err) {
    console.error(`Error: ${err.message}`);
    process.exit(1);
  }
  const command = args[0];

  // Per-subcommand contract, checked BEFORE any store read/write (PR #27
  // review: `clear expird` — an option typo without dashes — was an ignored
  // extra positional and cleared every token).
  const positionals = args.filter((a) => a !== '--expired');
  const expired = args.includes('--expired');
  const CONTRACTS = {
    list: { n: 1, expired: false },
    get: { n: 2, expired: false },
    clear: { n: 1, expired: true },
  };
  const contract = Object.hasOwn(CONTRACTS, command) ? CONTRACTS[command] : null;
  if (contract) {
    try {
      assertPositionalCount(positionals, contract.n, contract.n);
      if (expired && !contract.expired) throw new Error(`--expired is only valid with 'clear'`);
    } catch (err) {
      console.error(`Error: l402-store ${command}: ${err.message}`);
      process.exit(1);
    }
  }

  if (!command) {
    console.error('Usage:');
    console.error('  node l402_store.js list');
    console.error('  node l402_store.js get <url|key>');
    console.error('  node l402_store.js clear [--expired]');
    process.exit(1);
  }

  if (command === 'list') {
    const tokens = listTokens();
    const output = {
      storePath: STORE_FILE,
      count: tokens.length,
      tokens,
    };
    console.log(JSON.stringify(output, null, 2));
    return;
  }

  if (command === 'get') {
    // Accept a URL (normalized to its origin+path key) or a raw store key.
    const domain = args[1] ? (storeKeyFor(args[1]) ?? args[1]) : args[1];
    if (!domain) {
      console.error('Usage: node l402_store.js get <url|key>');
      process.exit(1);
    }
    const entry = getToken(domain);
    if (!entry) {
      console.error(`No valid token found for: ${domain}`);
      console.log(JSON.stringify({ domain, found: false }, null, 2));
      exitAfterStdout(0); // flush piped stdout first (v3.0.3 sweep)
      return;
    }
    const output = {
      domain,
      found: true,
      legacy: isLegacyKey(domain),
      macaroon: entry.macaroon,
      preimage: entry.preimage,
      satoshis: entry.satoshis ?? null,
      invoiceMsats: entry.invoiceMsats ?? null,
      budgetSats: entry.budgetSats ?? null,
      savedAt: entry.savedAt ? new Date(entry.savedAt).toISOString() : null,
      expiresAt: entryExpiresAt(entry) ? new Date(entryExpiresAt(entry)).toISOString() : null,
    };
    console.log(JSON.stringify(output, null, 2));
    return;
  }

  if (command === 'clear') {
    const expiredOnly = args.includes('--expired');
    const removed = clearTokens({ expiredOnly });
    const output = {
      removed,
      message: expiredOnly ? `Removed ${removed} expired token(s).` : `Removed all ${removed} token(s).`,
    };
    console.log(JSON.stringify(output, null, 2));
    return;
  }

  console.error(`Unknown command: ${command}`);
  console.error('Commands: list, get, clear');
  process.exit(1);
}

if (require.main === module) {
  main();
}

module.exports = {
  ARG_OPTIONS,
  saveToken,
  getToken,
  storeKeyFor,
  isLegacyKey,
  macaroonExpiryMs,
  listTokens,
  clearTokens,
  STORE_FILE,
  main,
};
