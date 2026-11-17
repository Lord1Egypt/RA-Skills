import { chmodSync, mkdirSync, readFileSync, renameSync, unlinkSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { join, dirname } from "node:path";
import { randomBytes, randomUUID } from "node:crypto";
import { validateDivergenceLimit } from "./divergence-flow.mjs";

export const DEV_BASE = "https://dev-interface.cournot.ai";
export const PRODUCTION_BASE = "https://interface.cournot.ai";
export const PACKS = [
  { pack_id: "p5", name: "Starter", price_usd: 5, calls: 600 },
  { pack_id: "p20", name: "Standard", price_usd: 20, calls: 2800 },
  { pack_id: "p50", name: "Scale", price_usd: 50, calls: 8000 },
];

export function fail(message, code = "INVALID_INPUT") {
  throw Object.assign(new Error(message), { code });
}

export function apiBase(value = process.env.COURNOT_API_BASE || PRODUCTION_BASE) {
  const base = value.replace(/\/$/, "");
  if (![DEV_BASE, PRODUCTION_BASE].includes(base) &&
      !/^http:\/\/127\.0\.0\.1:\d+$/.test(base)) {
    fail("Unsupported Cournot API base", "INVALID_API_BASE");
  }
  return base;
}

export function validateKey(key) {
  if (typeof key !== "string" || !/^ck_live_[A-Za-z0-9_-]{1,256}$/.test(key)) {
    fail("Invalid Cournot key format", "INVALID_KEY_FORMAT");
  }
  return key;
}

export function maskKey(key) {
  return key ? `ck_live_…${key.length > 12 ? key.slice(-4) : "****"}` : null;
}

export function sanitize(value) {
  if (typeof value === "string") return value.replace(/ck_live_[A-Za-z0-9_-]+/g, "[REDACTED]");
  if (Array.isArray(value)) return value.map(sanitize);
  if (!value || typeof value !== "object") return value;
  return Object.fromEntries(Object.entries(value).map(([key, item]) => [key,
    /^(api_?key|paymentHeaderValue|signature|signatureRecovery|nonce|authorization|sessionToken|privateKey|seedPhrase)$/i.test(key)
      ? "[REDACTED]" : sanitize(item),
  ]));
}

// One file per service origin avoids cross-environment overwrites and lost updates.
export function createCredentials({ env = process.env, directory = env.COURNOT_CREDENTIAL_DIR || join(homedir(), ".cournot") } = {}) {
  const file = (base) => join(directory, "credentials", `${encodeURIComponent(apiBase(base))}.json`);
  return {
    read(base) {
      base = apiBase(base);
      if (env.COURNOT_API_KEY && apiBase(env.COURNOT_API_KEY_BASE || PRODUCTION_BASE) === base) {
        return { key: validateKey(env.COURNOT_API_KEY), source: "environment" };
      }
      try {
        const data = JSON.parse(readFileSync(file(base), "utf8"));
        return { key: validateKey(data.api_key), source: "file" };
      } catch (error) {
        if (error.code === "ENOENT") return { key: null, source: "none" };
        fail("Cannot read Cournot credentials; fix the file before continuing", "CREDENTIAL_READ_FAILED");
      }
    },
    save(base, key) {
      validateKey(key);
      const path = file(base);
      const temporary = `${path}.${randomUUID()}.tmp`;
      try {
        mkdirSync(dirname(path), { recursive: true, mode: 0o700 });
        chmodSync(dirname(path), 0o700);
        writeFileSync(temporary, JSON.stringify({ api_key: key }) + "\n", { flag: "wx", mode: 0o600 });
        renameSync(temporary, path);
      } catch {
        fail("Could not save Cournot credentials", "CREDENTIAL_SAVE_FAILED");
      } finally {
        try { unlinkSync(temporary); } catch {}
      }
      const active = this.read(base);
      return { saved: true, maskedKey: maskKey(key), active: active.key === key,
        warning: active.key !== key ? "COURNOT_API_KEY overrides the saved key; update or unset it in this environment." : null };
    },
  };
}

export async function apiRequest({ base = apiBase(), path, method = "GET", body, limit, headers = {}, fetchImpl = fetch }) {
  if (!["resolve", "probability", "divergence", "packs", "account", "key/rotate"].includes(path)) fail("Invalid API path");
  if (path === "divergence") {
    validateDivergenceLimit(limit);
    if (method !== "GET" || body !== undefined) fail("Divergence requires GET without a body");
  } else if (limit !== undefined) fail("Limit is only supported for divergence");
  const query = limit === undefined ? "" : `?limit=${limit}`;
  const response = await fetchImpl(`${apiBase(base)}/intelligence/v1/${path}${query}`, {
    method, headers: { "content-type": "application/json", ...headers },
    ...(body === undefined ? {} : { body: JSON.stringify(body) }),
    redirect: "error", signal: AbortSignal.timeout(path === "probability" ? 120_000 : 30_000),
  });
  const text = await response.text();
  let parsed;
  try { parsed = text.trim() ? JSON.parse(text) : null; }
  catch { fail("Cournot returned a non-JSON response", "INVALID_API_RESPONSE"); }
  return { status: response.status, body: parsed, paymentRequired: response.headers.get("payment-required") };
}

export function responseState(response) {
  if (response.status === 429) return "rate_limited";
  if (response.status >= 500) return "service_error";
  if (response.body?.code === 22002) return "pack_exhausted";
  if (response.status === 401 || (response.body?.code === 4100 && response.body?.msg === "api key is invalid")) return "key_invalid";
  if (response.status === 402) return "payment_choice_required";
  if (response.status >= 200 && response.status < 300 && response.body?.code === 0) return "complete";
  return "api_error";
}

export function accountResult(response, { reveal = false, credentials, base, save = false } = {}) {
  const state = responseState(response);
  if (state !== "complete") return { state, base, httpStatus: response.status, response: sanitize(response.body) };
  const data = response.body.data;
  if (!data || typeof data !== "object") fail("Missing account response data", "INVALID_API_RESPONSE");
  const output = { state, base, wallet: data.wallet || null, balance: data.balance, maskedKey: maskKey(data.api_key), hasKey: !!data.api_key };
  if (data.api_key && save) {
    try { Object.assign(output, credentials.save(base, data.api_key)); }
    catch { Object.assign(output, { state: "credential_save_failed", saved: false,
      next: "The wallet still owns the balance. Recover the current key with account wallet authentication; do not buy again or rotate again." }); }
  }
  const safe = sanitize(output);
  if (reveal && data.api_key) {
    safe.api_key = data.api_key;
    safe.secrecyWarning = "This is a secret key. Do not share it in public channels.";
  }
  return safe;
}

export async function readAccount({ base = apiBase(), credentials = createCredentials(), fetchImpl = fetch, reveal = false, importKey } = {}) {
  const active = importKey !== undefined ? { key: validateKey(importKey.trim()), source: "import" } : credentials.read(base);
  if (!active.key) return { state: "credential_missing", base, next: "Use wallet account recovery or import an existing key. Anonymous queries remain available." };
  const response = await apiRequest({ base, path: "account", headers: { "COURNOT-API-KEY": active.key }, fetchImpl });
  if (responseState(response) === "complete" && response.body.data?.api_key !== active.key) {
    fail("Account returned a different key", "ACCOUNT_KEY_MISMATCH");
  }
  return { ...accountResult(response, { base, credentials, reveal: reveal && !importKey, save: !!importKey }), credentialSource: active.source };
}

export function walletAuthData(path, nonce, timestamp) {
  return {
    domain: { name: "Cournot", version: "1", chainId: 1 },
    types: {
      EIP712Domain: [{ name: "name", type: "string" }, { name: "version", type: "string" }, { name: "chainId", type: "uint256" }],
      WalletAuth: [{ name: "urlPath", type: "string" }, { name: "nonce", type: "string" }, { name: "timestamp", type: "string" }],
    },
    primaryType: "WalletAuth", message: { urlPath: `/intelligence/v1/${path}`, nonce, timestamp },
  };
}

function walletData(result) {
  if (!result?.success || !result.data) {
    fail("Wallet operation failed", `WALLET_${result?.error?.code || "FAILED"}`);
  }
  return result.data;
}

export function prepareAccountAuth({ action, reveal = false, base = apiBase(), run, intents, now = Date.now }) {
  if (!["account", "rotate"].includes(action)) fail("Invalid account action");
  if (walletData(run(["wallet", "status"])).status !== "CONNECTED") return { state: "wallet_required", reason: "WALLET_NOT_CONNECTED" };
  if (walletData(run(["wallet", "settings"])).devMode?.enabled !== true) return { state: "developer_mode_required" };
  const addresses = walletData(run(["wallet", "address"])).addresses;
  const address = addresses?.find((item) => String(item.binanceChainId) === "1")?.address;
  if (!/^0x[0-9a-fA-F]{40}$/.test(address || "")) fail("Wallet has no Ethereum address", "WALLET_ADDRESS_MISSING");
  const path = action === "rotate" ? "key/rotate" : "account";
  const typedData = walletAuthData(path, randomBytes(16).toString("hex"), String(Math.floor(now() / 1000)));
  const message = JSON.stringify({ method: "eth_signTypedData_v4", params: [address, JSON.stringify(typedData)] });
  const preview = walletData(run(["sign-message", "preview", "--binanceChainId", "1", "--signType", "EIP712", "--message", message]));
  if (!preview.requestId) fail("Wallet did not return a signable preview", "WALLET_PREVIEW_FAILED");
  const intentId = intents.save({ kind: "account_auth", base: apiBase(base), action, path, reveal: reveal && action === "account",
    address, typedData, requestId: preview.requestId, previewExpiresAt: preview.expiresAt });
  return { state: "signature_confirmation_required", intentId, action, base, wallet: address,
    risks: sanitize(preview.risks), authorityChanges: sanitize(preview.authorityChanges),
    warning: action === "rotate" ? "Rotating invalidates the old key on every device immediately. Balance is unchanged. Use import for a new device." : "Authenticate to read and save this wallet's current Cournot key; no payment.",
  };
}

export async function executeAccountAuth({ intentId, confirmed, poll = false, base = apiBase(), run, intents,
  credentials = createCredentials(), fetchImpl = fetch, now = Date.now }) {
  if (!poll && confirmed !== true) fail("Explicit signature confirmation is required", "CONFIRMATION_REQUIRED");
  const lease = intents.take(intentId);
  const intent = lease.value;
  try {
    if (intent.kind !== "account_auth" || intent.base !== apiBase(base)) fail("Wrong intent or environment", "INTENT_MISMATCH");
    if (Number(intent.typedData.message.timestamp) * 1000 + 30 * 60_000 <= now()) fail("Account signature expired", "INTENT_EXPIRED");
    if (poll && !intent.orderId) fail("No pending wallet signature");
    if (!poll && intent.previewExpiresAt && Number(intent.previewExpiresAt) <= now()) fail("Wallet preview expired", "INTENT_EXPIRED");
    const signed = walletData(run(intent.orderId
      ? ["sign-message", "result", "--order-id", intent.orderId]
      : ["sign-message", "execute", "--requestId", intent.requestId]));
    if (signed.status === "PENDING_CONFIRMATION") {
      if (!signed.orderId && !intent.orderId) fail("Missing wallet order id");
      return { state: "signature_pending", intentId: intents.save({ ...intent, orderId: signed.orderId || intent.orderId }) };
    }
    if (signed.status !== "COMPLETED") return { state: "signature_failed", status: signed.status };
    let signature = String(signed.signature || "").replace(/^0x/, "");
    if (signature.length === 128 && /^(?:0x)?(?:0[01]|1[bBcC]|[01])$/.test(String(signed.signatureRecovery))) {
      signature += Number.parseInt(String(signed.signatureRecovery).replace(/^0x/, ""), 16).toString(16).padStart(2, "0");
    }
    if (!/^[0-9a-fA-F]{130}$/.test(signature)) fail("Wallet returned an invalid signature", "WALLET_SIGNATURE_INVALID");
    let response;
    try {
      response = await apiRequest({ base, path: intent.path, method: intent.action === "rotate" ? "POST" : "GET", fetchImpl,
        headers: { "X-COURNOT-SIGNATURE": `0x${signature}`, "X-COURNOT-NONCE": intent.typedData.message.nonce,
          "X-COURNOT-TIMESTAMP": intent.typedData.message.timestamp } });
    } catch {
      return { state: "account_result_unknown", next: "Do not repeat rotate. Use account wallet recovery to check the current key." };
    }
    if (responseState(response) === "complete" && response.body.data?.wallet?.toLowerCase() !== intent.address.toLowerCase()) {
      fail("Account wallet did not match the signer", "ACCOUNT_WALLET_MISMATCH");
    }
    return accountResult(response, { reveal: intent.reveal, save: true, credentials, base });
  } finally { lease.consume(); }
}
