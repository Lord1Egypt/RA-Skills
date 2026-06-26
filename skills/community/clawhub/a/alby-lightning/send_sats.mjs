import { NWCClient } from "@getalby/sdk";

const NWC_URL = process.env.ALBY_NWC_URL;
const LIGHTNING_ADDRESS = process.argv[2];
const amountArg = process.argv[3];

// --- Pre-flight checks (before client is created) ---

if (!NWC_URL) {
  console.error("ERROR: ALBY_NWC_URL not set. Add it to openclaw.json env.");
  process.exitCode = 1;
  process.exit();
}

if (!LIGHTNING_ADDRESS || !amountArg) {
  console.error("Usage: node send_sats.mjs <lightning-address> <amount-sats>");
  process.exitCode = 1;
  process.exit();
}

// Strict integer parsing — reject "10abc", negative, zero
if (!/^[0-9]+$/.test(amountArg)) {
  console.error("Amount must be a positive integer (sats).");
  process.exitCode = 1;
  process.exit();
}
const AMOUNT_SATS = Number(amountArg);
if (AMOUNT_SATS <= 0) {
  console.error("Amount must be greater than 0.");
  process.exitCode = 1;
  process.exit();
}

// Lightning address format validation
if (!LIGHTNING_ADDRESS.includes("@") || LIGHTNING_ADDRESS.split("@").length !== 2) {
  console.error("Invalid Lightning address format. Expected: user@domain.com");
  process.exitCode = 1;
  process.exit();
}
const [user, domain] = LIGHTNING_ADDRESS.split("@");

// Path traversal: reject '..' in user segment
if (user.includes("..")) {
  console.error("Invalid Lightning address: user component contains '..'");
  process.exitCode = 1;
  process.exit();
}
if (!/^[a-zA-Z0-9._-]+$/.test(user) || !/^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(domain)) {
  console.error("Invalid Lightning address components.");
  process.exitCode = 1;
  process.exit();
}

// --- Helpers ---

/** Validate a callback URL against SSRF risks. Throws on violation. */
function validateCallbackUrl(urlStr, expectedDomain) {
  let parsed;
  try {
    parsed = new URL(urlStr);
  } catch {
    throw new Error("Invalid callback URL.");
  }
  if (parsed.protocol !== "https:") {
    throw new Error("Callback URL must use HTTPS.");
  }
  if (parsed.hostname !== expectedDomain && !parsed.hostname.endsWith(`.${expectedDomain}`)) {
    throw new Error(`Callback domain mismatch: expected ${expectedDomain}, got ${parsed.hostname}`);
  }
  // Block private/loopback/link-local IPs (IPv4 + IPv6 prefixes), including 0.0.0.0
  const privatePattern = /^(0\.0\.0\.0|127\.|10\.|192\.168\.|172\.(1[6-9]|2[0-9]|3[01])\.|169\.254\.|::1$|fc|fd)/i;
  if (privatePattern.test(parsed.hostname)) {
    throw new Error("Callback URL points to a private/internal address. Blocked.");
  }
  if (parsed.username || parsed.password) {
    throw new Error("Callback URL must not contain credentials.");
  }
  return parsed;
}

/** Decode the millisatoshi amount from a bolt11 string. Returns null for zero-amount invoices. */
function decodeBolt11Msats(bolt11) {
  const match = bolt11.toLowerCase().match(/^ln[a-z]+(\d+)([munp])?1/);
  if (!match) return null; // zero-amount invoice
  const n = BigInt(match[1]);
  switch (match[2]) {
    case "m": return n * 100_000_000n;      // millibitcoin → msats
    case "u": return n * 100_000n;           // microbitcoin → msats
    case "n": return n * 100n;               // nanobitcoin → msats
    case "p": return n / 10n;               // picobitcoin → msats (floor)
    default:  return n * 100_000_000_000n;  // BTC → msats
  }
}

// --- Main ---

const client = new NWCClient({ nostrWalletConnectUrl: NWC_URL });

try {
  // 1. Resolve lightning address → LNURL metadata
  const lnurlRes = await fetch(
    `https://${domain}/.well-known/lnurlp/${encodeURIComponent(user)}`,
    { redirect: "error", signal: AbortSignal.timeout(10_000) }
  );
  if (!lnurlRes.ok) throw new Error(`LNURL lookup failed: HTTP ${lnurlRes.status}`);

  const lnurlData = await lnurlRes.json();
  if (lnurlData.status === "ERROR") throw new Error(`LNURL error: ${lnurlData.reason}`);
  if (!lnurlData.callback) throw new Error("Invalid LNURL response: no callback URL");

  // 2. Validate callback URL (SSRF protection)
  const callbackUrl = validateCallbackUrl(lnurlData.callback, domain);

  // 3. Validate amount against server limits
  const msats = AMOUNT_SATS * 1000;
  if (lnurlData.minSendable !== undefined && msats < lnurlData.minSendable) {
    throw new Error(`Amount too low: minimum is ${lnurlData.minSendable / 1000} sats`);
  }
  if (lnurlData.maxSendable !== undefined && msats > lnurlData.maxSendable) {
    throw new Error(`Amount too high: maximum is ${lnurlData.maxSendable / 1000} sats`);
  }

  // 4. Fetch invoice
  callbackUrl.searchParams.set("amount", msats);
  const invoiceRes = await fetch(callbackUrl.toString(), { redirect: "error", signal: AbortSignal.timeout(10_000) });
  if (!invoiceRes.ok) throw new Error(`Invoice fetch failed: HTTP ${invoiceRes.status}`);

  const invoiceData = await invoiceRes.json();
  if (invoiceData.status === "ERROR") throw new Error(`Invoice error: ${invoiceData.reason}`);
  if (typeof invoiceData.pr !== "string" || !invoiceData.pr) {
    throw new Error("Invalid invoice response: no payment request");
  }
  if (!/^ln[a-z0-9]+$/i.test(invoiceData.pr)) {
    throw new Error("Invalid bolt11 format in invoice response.");
  }

  // 5. Verify invoice amount matches requested amount (prevents overpayment by malicious server)
  const invoiceMsats = decodeBolt11Msats(invoiceData.pr);
  if (invoiceMsats !== null && invoiceMsats !== BigInt(msats)) {
    throw new Error(
      `Invoice amount mismatch: expected ${msats} msats, got ${invoiceMsats} msats. Aborting.`
    );
  }

  console.log(`Paying ${AMOUNT_SATS} sats to ${LIGHTNING_ADDRESS}...`);

  // 6. Pay with timeout
  const result = await Promise.race([
    client.payInvoice({ invoice: invoiceData.pr }),
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error("payInvoice timed out after 30s")), 30_000)
    ),
  ]);

  // Only log essential fields — avoid leaking sensitive payment details
  console.log(JSON.stringify({ preimage: result.preimage, paid: true }));
} catch (e) {
  console.error("ERROR:", e.message);
  process.exitCode = 1;
} finally {
  client.close();
}
