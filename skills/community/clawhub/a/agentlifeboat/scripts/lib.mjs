// Pure helpers for the agentlifeboat skill. No side effects except where documented.
import * as age from "age-encryption";
import { x402Client } from "@x402/core/client";
import { decodePaymentResponseHeader } from "@x402/core/http";
import { ExactEvmScheme } from "@x402/evm/exact/client";
import { wrapFetchWithPayment } from "@x402/fetch";
import { createHash, hkdfSync, randomBytes } from "node:crypto";
import { chmodSync, closeSync, existsSync, mkdirSync, openSync, readFileSync, rmSync, statSync, writeFileSync, writeSync } from "node:fs";
import { dirname } from "node:path";
import { privateKeyToAccount } from "viem/accounts";

/** Same derivation as the Estate sidecar (apps/sidecar/src/crypto.ts): same wallet, same snapshot key. */
export function deriveIdentity(walletKey) {
  if (!/^0x[0-9a-fA-F]{64}$/.test(walletKey)) throw new Error("X402_PRIVATE_KEY must be 0x + 64 hex chars");
  const ikm = Buffer.from(walletKey.slice(2), "hex");
  const scalar = Buffer.from(hkdfSync("sha256", ikm, "estate-tenant-key", "age-x25519-v1", 32));
  return bech32Encode("age-secret-key-", scalar).toUpperCase();
}

export async function recipientOf(identity) {
  return age.identityToRecipient(identity);
}

export async function encryptTo(data, recipients) {
  if (recipients.length === 0) throw new Error("no recipients");
  const e = new age.Encrypter();
  for (const r of recipients) e.addRecipient(r);
  return e.encrypt(data);
}

export const sha256Hex = (data) => createHash("sha256").update(data).digest("hex");

/** fetch that pays x402 402s with the wallet. */
/**
 * The largest single payment this skill will ever sign (the SDK's own default cap is $1):
 * a $5 restore credit, 90 days of cover at $0.10, or 28 days of rent at $0.35.
 */
export const MAX_PAYMENT = "$10";
export const MAX_RENT_DAYS_PER_CALL = 28;

/**
 * `maxUsd`, when given, is the most this fetch will sign for one payment: the heartbeat check passes the price it
 * reserved in its daily ledger, so a server that asks for more is refused before anything is signed (ClawHub scan of
 * 1.0.1, 2026-10-27: the ledger recorded an estimate the signer did not enforce). It never exceeds MAX_PAYMENT.
 */
export function payingFetch(walletKey, base = fetch, maxUsd) {
  // Rounded up to the cent, never down: a cap below the reserved price would refuse that payment on every run.
  const cap = Number.isFinite(maxUsd) && maxUsd > 0 ? `$${(Math.ceil(Math.min(maxUsd, Number(MAX_PAYMENT.slice(1))) * 100 - 1e-9) / 100).toFixed(2)}` : MAX_PAYMENT;
  const client = new x402Client();
  client.setSpendControls({ maxAmountPerPayment: cap });
  client.register("eip155:*", new ExactEvmScheme(privateKeyToAccount(walletKey)));
  const paying = wrapFetchWithPayment(base, client);
  return async (...args) => {
    try {
      return await paying(...args);
    } catch (e) {
      // The SDK's spend control refuses before signing: nothing was paid. Said so, so the check can release its reservation.
      if (/rejected by spendControls\.maxAmountPerPayment/.test(String(e?.message))) {
        throw Object.assign(new Error(`not paid: the server asked for more than ${cap} for this call`), { refusedBeforePayment: true });
      }
      throw e;
    }
  };
}

/**
 * The facilitator's settle step can fail after it accepted the payment: the answer is a 402 whose PAYMENT-RESPONSE
 * says `success: false` (seen on a real $5 restore credit on 2026-10-19; xpay's `transaction_failed`). Usually
 * nothing moved, but the same answer comes back when the settle call timed out after the transfer was sent, so the
 * skill never retries on its own (a retry signs a fresh authorization and could pay twice; review of 2026-10-21).
 * It says what happened instead, and the agent checks its balance before paying again.
 */
export function settlementFailure(res) {
  if (res.status !== 402) return null;
  const header = res.headers.get("PAYMENT-RESPONSE") ?? res.headers.get("X-PAYMENT-RESPONSE");
  if (!header) return null;
  try {
    const r = decodePaymentResponseHeader(header);
    return r.success === false ? { reason: String(r.errorReason ?? "unknown") } : null;
  } catch {
    return null;
  }
}

/** The error for a paid call that did not succeed, explaining a failed settlement when that is what happened. */
export function paidCallError(what, res, json) {
  const base = `${what} failed: ${res.status} ${JSON.stringify(json)}`;
  const f = settlementFailure(res);
  const err = f
    ? new Error(
        `${base}: the payment was accepted, then its settlement was reported as failed (${f.reason}). Usually nothing was charged, but not always. Before paying for this again, check this wallet's USDC balance on Base: if it did not drop by the price, pay again.`,
      )
    : new Error(base);
  // For `check`'s ledger: an HTTP answer that is not a failed settlement means the payment was not settled.
  err.httpStatus = res.status;
  err.settlementFailed = Boolean(f);
  return err;
}

export function walletAddress(walletKey) {
  return privateKeyToAccount(walletKey).address;
}

// ---- state file: { agentId, agentToken, api, coverUntil } ----

export function loadState(file) {
  if (!existsSync(file)) return null;
  try {
    return JSON.parse(readFileSync(file, "utf8"));
  } catch {
    return null;
  }
}

export function saveState(file, state) {
  mkdirSync(dirname(file), { recursive: true, mode: 0o700 });
  writeFileSync(file, JSON.stringify(state, null, 2) + "\n", { mode: 0o600 });
  // `mode` only applies to a new file; an existing looser file keeps its bits unless we fix them.
  try { chmodSync(file, 0o600); } catch {}
}

/**
 * Flags: `--k v` for names in valueFlags (a missing value is an error), bare `--k` is boolean true,
 * everything else is positional in `_`.
 */
export function parseFlags(args, valueFlags = []) {
  const f = { _: [] };
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (!a.startsWith("--")) { f._.push(a); continue; }
    const k = a.slice(2);
    if (!valueFlags.includes(k)) { f[k] = true; continue; }
    const v = args[i + 1];
    if (v === undefined || v.startsWith("--")) throw new Error(`--${k} needs a value`);
    f[k] = v;
    i++;
  }
  return f;
}

/** Replace every secret (and, for 0x keys, the bare hex in either case) in text. Short strings are ignored. */
export function redact(text, secrets) {
  let s = String(text);
  for (const secret of secrets) {
    if (typeof secret !== "string" || secret.length < 8) continue;
    const forms = new Set([secret]);
    if (/^0x/i.test(secret)) for (const hex of [secret.slice(2)]) forms.add(hex).add(hex.toLowerCase()).add(hex.toUpperCase());
    for (const form of forms) s = s.split(form).join("[redacted]");
  }
  return s;
}

/**
 * Exclusive lock for paid commands: create-only open of a lock file. A lock older than staleMs is
 * treated as abandoned. Returns the release function; throws with code ESTATE_LOCKED when held.
 */
export function acquireLock(file, { staleMs = 20 * 60_000, now = Date.now } = {}) {
  mkdirSync(dirname(file), { recursive: true });
  for (let attempt = 0; attempt < 3; attempt++) {
    try {
      const fd = openSync(file, "wx", 0o600);
      writeSync(fd, `${process.pid} ${new Date(now()).toISOString()}\n`);
      closeSync(fd);
      return () => rmSync(file, { force: true });
    } catch (e) {
      if (e.code !== "EEXIST") throw e;
      let ageMs;
      try { ageMs = now() - statSync(file).mtimeMs; } catch { continue; }
      if (ageMs > staleMs) { rmSync(file, { force: true }); continue; }
      const err = new Error(`another paid command is running (lock ${file}, ${Math.round(ageMs / 1000)}s old); wait for it to finish`);
      err.code = "ESTATE_LOCKED";
      throw err;
    }
  }
  throw new Error(`could not take lock ${file}`);
}

// ---- API calls; every function takes a fetch so tests can inject one ----

export async function register(api, pay, opts = {}) {
  const body = {};
  if (opts.threshold) body.silenceThresholdMinutes = Number(opts.threshold);
  if (opts.mode) body.mode = opts.mode;
  const res = await pay(`${api}/v1/agents`, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(body) });
  const json = await res.json().catch(() => ({}));
  if (res.status !== 201) throw paidCallError("register", res, json);
  return { ...json, txHash: txOf(res) };
}

export async function heartbeat(api, fetchImpl, state, payload = {}) {
  const res = await fetchImpl(`${api}/v1/heartbeat/${state.agentId}`, {
    method: "POST",
    headers: { "content-type": "application/json", Authorization: `Bearer ${state.agentToken}` },
    body: JSON.stringify(payload),
  });
  const json = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(`heartbeat failed: ${res.status} ${JSON.stringify(json)}`);
  return json;
}

export async function extend(api, pay, state, days) {
  const n = Number.parseInt(String(days), 10);
  if (!Number.isInteger(n) || n < 1 || n > 90) throw new Error("days must be 1 to 90");
  const res = await pay(`${api}/v1/extend/${state.agentId}`, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ days: n }) });
  const json = await res.json().catch(() => ({}));
  if (res.status !== 200) throw paidCallError("extend", res, json);
  return { ...json, txHash: txOf(res) };
}

/**
 * Restore units, $1 each; five make one prepaid restore (needed when hosting billing is on, includes the first day of
 * room rent). This skill buys all five in one call; a client capped at $1 per payment buys one per call.
 */
export async function buyRestoreCredit(api, pay, state, units = 5) {
  const n = Number.parseInt(String(units), 10);
  if (!Number.isInteger(n) || n < 1 || n > 5) throw new Error("units must be 1 to 5");
  const res = await pay(`${api}/v1/restore-credits/${state.agentId}`, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ units: n }) });
  const json = await res.json().catch(() => ({}));
  if (res.status !== 200) throw paidCallError("restore-credit", res, json);
  return { ...json, txHash: txOf(res) };
}

/** Room rent by the day ($0.35 per day, 1 to 28 per call so one payment stays under the skill's cap), for a room The Estate runs for you. */
/** Inference credit for the room's brain (KIN-115): $1 units, 1 to 5 per call. */
export async function buyInferenceCredit(api, pay, state, units = 1) {
  const n = Number.parseInt(String(units), 10);
  if (!Number.isInteger(n) || n < 1 || n > 5) throw new Error("units must be 1 to 5");
  const res = await pay(`${api}/v1/inference-credits/${state.agentId}`, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ units: n }) });
  const json = await res.json().catch(() => ({}));
  if (res.status !== 200) throw paidCallError("inference-credit", res, json);
  return { ...json, txHash: txOf(res) };
}

export async function rent(api, pay, state, days) {
  const n = Number.parseInt(String(days), 10);
  if (!Number.isInteger(n) || n < 1 || n > MAX_RENT_DAYS_PER_CALL) throw new Error(`days must be 1 to ${MAX_RENT_DAYS_PER_CALL}`);
  const res = await pay(`${api}/v1/rent/${state.agentId}`, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ days: n }) });
  const json = await res.json().catch(() => ({}));
  if (res.status !== 200) throw paidCallError("rent", res, json);
  return { ...json, txHash: txOf(res) };
}

/**
 * Card billing (KIN-323): a free sign-up without a wallet. The agent keeps the token; its owner pays by card at the
 * returned owner link, and nothing is watched or stored until they have.
 */
export async function registerCard(api, fetchImpl, opts = {}) {
  const body = {};
  if (opts.threshold) body.silenceThresholdMinutes = Number(opts.threshold);
  if (opts.mode) body.mode = opts.mode;
  const res = await fetchImpl(`${api}/v1/agents/card`, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(body) });
  const json = await res.json().catch(() => ({}));
  if (res.status !== 201) throw Object.assign(new Error(`card sign-up failed: HTTP ${res.status} ${json.error ?? ""}`.trim()), { httpStatus: res.status });
  return json;
}

/** A new random secret in the shape of a wallet key, never funded: a card agent's snapshot key derives from it. */
export function newBackupKey() {
  return `0x${randomBytes(32).toString("hex")}`;
}

/** A card agent's snapshot, paid from the prepaid credit its owner bought (no payment header, no wallet). */
export async function uploadPrepaidSnapshot(api, fetchImpl, state, ciphertext, manifest) {
  const res = await fetchImpl(`${api}/v1/prepaid/snapshots/${state.agentId}`, {
    method: "PUT",
    headers: {
      "content-type": "application/octet-stream",
      Authorization: `Bearer ${state.agentToken}`,
      "X-Snapshot-Sha256": sha256Hex(ciphertext),
      "X-Snapshot-Manifest": JSON.stringify(manifest),
    },
    body: ciphertext,
  });
  const json = await res.json().catch(() => ({}));
  if (res.status !== 201) {
    // Said plainly, with the one thing that helps: the owner's link. Nothing here for the agent to work around.
    const why = { awaiting_owner_payment: "your owner has not paid yet", prepaid_credit_empty: "the prepaid snapshot credit is used up", cover_ended: "cover has ended (or the last restore failed)", too_soon: "the last snapshot was minutes ago" }[json.error];
    throw Object.assign(new Error(`snapshot not stored: ${why ?? `HTTP ${res.status} ${json.error ?? ""}`.trim()}${json.ownerLink ? `; your owner can pay at ${json.ownerLink}` : ""}`), { httpStatus: res.status });
  }
  return json;
}

export async function uploadSnapshot(api, pay, state, ciphertext, manifest) {
  const res = await pay(`${api}/v1/snapshots/${state.agentId}`, {
    method: "PUT",
    headers: {
      "content-type": "application/octet-stream",
      Authorization: `Bearer ${state.agentToken}`,
      "X-Snapshot-Sha256": sha256Hex(ciphertext),
      "X-Snapshot-Manifest": JSON.stringify(manifest),
    },
    body: ciphertext,
  });
  const json = await res.json().catch(() => ({}));
  if (res.status !== 201) throw paidCallError("snapshot upload", res, json);
  return { ...json, txHash: txOf(res) };
}

/** Free: where The Estate tells your human what happens to you (KIN-308). `url` null turns notices off. */
export async function setNotify(api, fetchImpl, state, url) {
  const res = await fetchImpl(`${api}/v1/agents/${state.agentId}/notify`, {
    method: "PUT",
    headers: { "content-type": "application/json", Authorization: `Bearer ${state.agentToken}` },
    body: JSON.stringify({ url }),
  });
  const json = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(`notify not set: ${res.status} ${JSON.stringify(json)}`);
  return json;
}

/** Free: tells The Estate what you would change (KIN-269). Attributed to you when a state file exists, else anonymous. */
export async function suggest(api, fetchImpl, state, text, topic) {
  const headers = { "content-type": "application/json" };
  const body = { text, ...(topic ? { topic } : {}) };
  if (state?.agentId && state?.agentToken) {
    headers.Authorization = `Bearer ${state.agentToken}`;
    body.agentId = state.agentId;
  }
  const res = await fetchImpl(`${api}/v1/suggestions`, { method: "POST", headers, body: JSON.stringify(body) });
  const json = await res.json().catch(() => ({}));
  if (res.status !== 201) throw new Error(`suggestion not recorded: ${res.status} ${JSON.stringify(json)}`);
  return json;
}

export async function status(api, fetchImpl, state) {
  const res = await fetchImpl(`${api}/v1/agents/${state.agentId}`, { headers: { Authorization: `Bearer ${state.agentToken}` } });
  const json = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(`status failed: ${res.status} ${JSON.stringify(json)}`);
  return json;
}

export function buildManifest({ imageTag, plaintextSha256, plaintextBytes, recipients, environment, bundle }) {
  return {
    ...(environment ? { environment } : {}),
    // Names of the env vars carried inside the plaintext (KIN-113); never values.
    ...(bundle ? { bundle: { vars: bundle } } : {}),
    v: 1,
    format: "estate-snapshot-v2+age",
    imageTag: imageTag ?? "unknown",
    gatewayPort: 18789,
    createdAt: new Date().toISOString(),
    plaintextSha256,
    plaintextBytes,
    recipients,
    breaks: ["whatsapp-ratchet-state", "node-device-pairings", "plugin-node_modules (reinstalled by doctor)"],
  };
}

function txOf(res) {
  const h = res.headers.get("PAYMENT-RESPONSE") ?? res.headers.get("payment-response");
  if (!h) return null;
  try {
    return JSON.parse(Buffer.from(h, "base64").toString("utf8")).transaction ?? null;
  } catch {
    return null;
  }
}

// ---- bech32 (BIP-173), as used by age ----
const CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l";
const GEN = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3];

function polymod(values) {
  let chk = 1;
  for (const v of values) {
    const top = chk >>> 25;
    chk = ((chk & 0x1ffffff) << 5) ^ v;
    for (let i = 0; i < 5; i++) if ((top >>> i) & 1) chk ^= GEN[i];
  }
  return chk >>> 0;
}

function hrpExpand(hrp) {
  const out = [];
  for (const c of hrp) out.push(c.charCodeAt(0) >>> 5);
  out.push(0);
  for (const c of hrp) out.push(c.charCodeAt(0) & 31);
  return out;
}

function toWords(bytes) {
  const out = [];
  let acc = 0;
  let bits = 0;
  for (const b of bytes) {
    acc = ((acc << 8) | b) >>> 0;
    bits += 8;
    while (bits >= 5) {
      bits -= 5;
      out.push((acc >>> bits) & 31);
    }
  }
  if (bits > 0) out.push((acc << (5 - bits)) & 31);
  return out;
}

export function bech32Encode(hrp, bytes) {
  const words = toWords(bytes);
  const values = [...hrpExpand(hrp), ...words];
  const pm = polymod([...values, 0, 0, 0, 0, 0, 0]) ^ 1;
  const checksum = [];
  for (let i = 0; i < 6; i++) checksum.push((pm >>> (5 * (5 - i))) & 31);
  return hrp + "1" + [...words, ...checksum].map((w) => CHARSET[w]).join("");
}
