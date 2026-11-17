#!/usr/bin/env node
/**
 * Blink Wallet - L402 Service Discovery
 *
 * Usage: node l402_discover.js <url> [--method GET|POST] [--header key:value]
 *
 * Probes a URL for L402 payment requirements without paying.
 * Parses both L402 formats:
 *   - Lightning Labs: WWW-Authenticate: L402 macaroon="...", invoice="lnbc..."
 *   - l402-protocol.org: JSON body with payment_request_url and offers array
 *
 * Arguments:
 *   url             - Required. The URL to probe.
 *   --method        - Optional. HTTP method: GET (default) or POST.
 *   --header        - Optional. Extra header in key:value format (repeatable).
 *
 * Environment:
 *   BLINK_API_KEY   - Optional. Not required for discovery.
 *   BLINK_API_URL   - Optional. Override Blink API endpoint.
 *
 * Dependencies: None (uses Node.js built-in fetch)
 *
 * Output: JSON to stdout. Status messages to stderr.
 */

'use strict';

// The URL-policy guard shared with the LNURL/L402-pay flows (security-audit
// fix: this script previously used bare fetch with redirect:'follow'). Discovery
// deliberately has NO allowlist payment gate — it is the documented public
// prober — but every fetch is SSRF-guarded: private/loopback/link-local
// targets refused (unless the host appears in a configured budget allowlist,
// which here only RELAXES the guard — see l402Allowlist),
// redirects followed manually and re-validated per hop.
const { fetchWithRetry, assertAllowedUrl, withholdHeadersIfCrossOrigin, l402Allowlist } = require('./_lnurl');
const { getAllowHosts } = require('./_budget');
const { strictArgv } = require('./_blink_client');

// ── Inline L402 parsing ───────────────────────────────────────────────────────

/**
 * Parse a Lightning Labs L402 WWW-Authenticate header.
 *
 * Format: L402 macaroon="<base64>", invoice="<lnbc...>"
 *
 * @param {string} header
 * @returns {{ macaroon: string, invoice: string } | null}
 */
function parseLightningLabsHeader(header) {
  if (!header) return null;
  const trimmed = header.trim();
  // Must start with "L402 " (case-insensitive)
  if (!/^l402\s/i.test(trimmed)) return null;

  const macaroonMatch = trimmed.match(/macaroon\s*=\s*"([^"]+)"/i);
  const invoiceMatch = trimmed.match(/invoice\s*=\s*"([^"]+)"/i);

  if (!macaroonMatch || !invoiceMatch) return null;
  return {
    macaroon: macaroonMatch[1],
    invoice: invoiceMatch[1],
  };
}

/**
 * Parse a l402-protocol.org JSON 402 response body.
 *
 * The spec (v0.2.x) returns JSON with:
 *   { version, payment_request_url, offers: [{ title, amount, currency, ... }] }
 *
 * @param {object} body   Parsed JSON from the 402 response.
 * @returns {{ paymentRequestUrl: string, offers: object[] } | null}
 */
function parseL402ProtocolBody(body) {
  if (!body || typeof body !== 'object') return null;
  if (!body.payment_request_url && !Array.isArray(body.offers)) return null;
  return {
    paymentRequestUrl: body.payment_request_url || null,
    version: body.version || null,
    offers: Array.isArray(body.offers) ? body.offers : [],
  };
}

/**
 * Resolve the canonical URL by following any HTTP redirects.
 *
 * Sends a HEAD request with redirect:'follow' and returns response.url —
 * the final URL after the redirect chain. Falls back gracefully to the
 * original URL on any error (network failure, 405 Method Not Allowed, etc.).
 *
 * @param {string} url
 * @param {number} [timeoutMs=10000]
 * @returns {Promise<string>}
 */
async function resolveCanonicalUrl(url, timeoutMs = 10_000, allowedHosts = null) {
  // Policy first, synchronously: a refused target aborts the flow; only
  // transient network failures degrade gracefully.
  assertAllowedUrl(url, allowedHosts, 'L402 discovery URL', { portsUnrestricted: true, strictLocal: true });
  try {
    const res = await fetchWithRetry(url, {
      method: 'HEAD',
      timeoutMs,
      retries: 1,
      allowedHosts,
      what: 'L402 discovery URL',
      portsUnrestricted: true,
      strictLocal: true,
    });
    return res.url || url;
  } catch (err) {
    if (err && err.code === 'URL_POLICY') throw err;
    return url;
  }
}

/**
 * Fetch payment details from l402-protocol.org endpoint.
 * POST to payment_request_url to retrieve the Lightning invoice.
 *
 * @param {string} paymentRequestUrl
 * @param {number} [timeoutMs=15000]
 * @returns {Promise<{ invoice: string, offerId: string | null } | null>}
 */
async function fetchL402ProtocolInvoice(paymentRequestUrl, timeoutMs = 15_000, allowedHosts = null) {
  // payment_request_url is SERVER-SUPPLIED from the 402 challenge body — the
  // one hop where a hostile L402 server picks the destination. It gets the
  // same guard as user-supplied URLs; a policy refusal throws (fail loud),
  // transient network failures keep the graceful null fallback.
  assertAllowedUrl(paymentRequestUrl, allowedHosts, 'L402 payment_request_url', {
    portsUnrestricted: true,
    strictLocal: true,
  });
  try {
    const res = await fetchWithRetry(paymentRequestUrl, {
      method: 'POST',
      // Entity header: call-site-generated descriptor for the internal JSON
      // body — survives cross-origin 307/308 with the body it describes
      // (review round 2), unlike operator-supplied headers.
      entityHeaders: { 'Content-Type': 'application/json' },
      body: JSON.stringify({}),
      timeoutMs,
      retries: 0,
      allowedHosts,
      what: 'L402 payment_request_url',
      portsUnrestricted: true,
      strictLocal: true,
    });
    if (!res.ok) return null;
    const data = await res.json();
    // Response shape: { invoice: "lnbc...", ... } or { payment_request: "lnbc..." }
    const invoice = data.invoice || data.payment_request || null;
    return invoice ? { invoice, offerId: data.offer_id || null } : null;
  } catch (err) {
    // A policy refusal raised INSIDE the walker (a hostile redirect hop, or a
    // name resolving to a private address) must fail loud too — it was
    // swallowed into the graceful null (PR #25 review round 2).
    if (err && err.code === 'URL_POLICY') throw err;
    return null;
  }
}

/**
 * Decode the amount from a BOLT-11 invoice without any external library.
 * Reads the human-readable part (amount + multiplier) from the invoice prefix.
 *
 * Supports mainnet (lnbc), testnet (lntb), signet (lntbs).
 * Returns null if not parseable. The HRP amount is a BigInt so huge valid
 * amounts keep full precision through the multiplier conversion.
 *
 * @param {string} invoice
 * @returns {{ amount: bigint, multiplier: string } | null}
 */
function bolt11AmountParts(invoice) {
  if (!invoice) return null;
  const lower = invoice.toLowerCase();

  // Strip the bech32 prefix: lnbc, lntb, lntbs
  let amountStr;
  if (lower.startsWith('lntbs')) {
    amountStr = lower.slice(5);
  } else if (lower.startsWith('lntb')) {
    amountStr = lower.slice(4);
  } else if (lower.startsWith('lnbc')) {
    amountStr = lower.slice(4);
  } else {
    return null;
  }

  // The amount field is digits followed by an optional multiplier letter,
  // then "1" (separator) and the rest of the encoded data.
  const match = amountStr.match(/^(\d+)([munp]?)1/);
  if (!match) return null;

  return { amount: BigInt(match[1]), multiplier: match[2] };
}

/**
 * Decode a BOLT-11 invoice amount in MILLISATOSHIS — full precision, no
 * rounding. BigInt arithmetic throughout; sub-millisatoshi amounts (pico
 * amounts below 1 msat) are floored at msat granularity. Returns null if not
 * parseable, or if the amount exceeds a safe integer (not a usable amount).
 *
 * @param {string} invoice
 * @returns {number | null}  Amount in millisatoshis, or null.
 */
function decodeBolt11AmountMsats(invoice) {
  const parts = bolt11AmountParts(invoice);
  if (!parts) return null;

  const { amount, multiplier } = parts;
  let msats;
  switch (multiplier) {
    case '':
      msats = amount * 100_000_000_000n; // whole BTC → 1e11 msats
      break;
    case 'm':
      msats = amount * 100_000_000n; // 1e5 sats → 1e8 msats
      break;
    case 'u':
      msats = amount * 100_000n; // 100 sats → 1e5 msats
      break;
    case 'n':
      msats = amount * 100n; // 0.1 sats → 100 msats
      break;
    case 'p':
      msats = amount / 10n; // 0.0001 sats → 0.1 msats (floored to msat granularity)
      break;
    default:
      return null;
  }
  if (msats > BigInt(Number.MAX_SAFE_INTEGER)) return null;
  return Number(msats);
}

/**
 * Decode a BOLT-11 invoice amount in SATOSHIS (legacy, round-to-nearest).
 * Callers that enforce money limits must NOT use this directly: rounding can
 * push a below-1-sat invoice up to 1 sat and shave fractions off larger ones.
 * Use budgetChargeFromInvoice() for enforcement.
 *
 * @param {string} invoice
 * @returns {number | null}  Amount in satoshis, or null.
 */
function decodeBolt11AmountSats(invoice) {
  const msats = decodeBolt11AmountMsats(invoice);
  if (msats === null) return null;
  return Math.round(msats / 1000);
}

/**
 * The budget charge for a BOLT-11 invoice, structured so callers can tell
 * "undecodable" apart from "positive sub-satoshi" — two different policies:
 *   - undecodable                        → { msats: null, budgetSats: null }
 *   - any positive decodable amount      → budgetSats = max(1, ceil(msats/1000))
 *
 * Any positive decodable amount charges AT LEAST 1 sat (explicit payments can
 * never move funds untracked); fractional amounts charge ceil (conservative).
 * Callers with a stricter policy — e.g. L402 refuses invoices below 1 sat —
 * decide from `msats`.
 *
 * @param {string} invoice
 * @returns {{ msats: number|null, budgetSats: number|null }}
 */
function budgetChargeFromInvoice(invoice) {
  const msats = decodeBolt11AmountMsats(invoice);
  if (msats === null) return { msats: null, budgetSats: null };
  return { msats, budgetSats: Math.max(1, Math.ceil(msats / 1000)) };
}

// ── Arg parsing ───────────────────────────────────────────────────────────────

// Every option l402-discover accepts; anything else is refused (v3.0.4 strict sweep).
const ARG_OPTIONS = { method: { type: 'string' }, header: { type: 'string', multiple: true } };

function parseArgs(argv) {
  argv = strictArgv(argv, ARG_OPTIONS, { positionals: [0, 1] });
  let url = null;
  let method = 'GET';
  const headers = {};

  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--method' && i + 1 < argv.length) {
      method = argv[++i].toUpperCase();
      if (!['GET', 'POST'].includes(method)) {
        console.error('Error: --method must be GET or POST');
        process.exit(1);
      }
    } else if (arg === '--header' && i + 1 < argv.length) {
      const hdr = argv[++i];
      const colon = hdr.indexOf(':');
      if (colon < 1) {
        console.error(`Error: --header must be in key:value format, got: ${hdr}`);
        process.exit(1);
      }
      headers[hdr.slice(0, colon).trim()] = hdr.slice(colon + 1).trim();
    } else if (!arg.startsWith('--')) {
      url = arg;
    }
  }

  return { url, method, headers };
}

// ── Main ──────────────────────────────────────────────────────────────────────

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (!args.url) {
    console.error('Usage: node l402_discover.js <url> [--method GET|POST] [--header key:value]');
    process.exit(1);
  }

  console.error(`Probing: ${args.url}`);

  // Resolve canonical URL (follow any HTTP redirects) so the probe always
  // hits the final endpoint and reports the correct URL.
  // FT7 (v3.0.2): discovery is the documented UNGATED prober — the budget
  // allowlist may only relax the SSRF guard here (permit a listed private/local
  // host), never restrict public hosts. It was passed as an exclusive list.
  // The private/local exception is bound to the host the operator chose (PR #25 review).
  const allowHosts = l402Allowlist(getAllowHosts(), { relaxOnly: true, operatorUrl: args.url });
  const canonicalUrl = await resolveCanonicalUrl(args.url, 10_000, allowHosts);
  if (canonicalUrl !== args.url) {
    console.error(`Resolved redirect: ${args.url} → ${canonicalUrl}`);
    // FT6 finding: the follow-up request after pre-flight canonicalization is
    // a fresh first hop — the shared origin policy withholds the ENTIRE
    // operator header set when origins differ (see l402_pay).
    const originPolicy = withholdHeadersIfCrossOrigin(args.url, canonicalUrl, args.headers);
    if (originPolicy.withheld.length > 0) {
      args.headers = originPolicy.headers;
      console.error(
        `Warning: canonicalization crossed origins — ALL operator-supplied headers (${originPolicy.withheld.join(', ')}) are withheld from the request.`,
      );
    }
  }

  let res;
  try {
    res = await fetchWithRetry(canonicalUrl, {
      method: args.method,
      headers: { ...args.headers },
      timeoutMs: 15_000,
      retries: 0,
      allowedHosts: allowHosts,
      what: 'L402 discovery probe',
      portsUnrestricted: true,
      strictLocal: true,
    });
  } catch (err) {
    if (err && err.code === 'URL_POLICY') throw err;
    throw new Error(`Request failed: ${err.message}`);
  }

  if (res.status !== 402) {
    const body = await res.text().catch(() => '');
    const output = {
      url: args.url,
      canonicalUrl: canonicalUrl !== args.url ? canonicalUrl : undefined,
      l402_detected: false,
      status: res.status,
      message:
        res.status === 200
          ? 'No L402 protection detected — resource returned 200 OK.'
          : `Unexpected status ${res.status}. Not an L402 endpoint.`,
      body: body.length <= 500 ? body : body.slice(0, 500) + '…',
    };
    console.log(JSON.stringify(output, null, 2));
    return;
  }

  console.error('402 Payment Required detected — parsing L402 challenge...');

  // ── Try Lightning Labs format first (WWW-Authenticate header) ──
  const wwwAuth = res.headers.get('www-authenticate') || res.headers.get('WWW-Authenticate') || '';
  const lightningLabs = parseLightningLabsHeader(wwwAuth);

  if (lightningLabs) {
    console.error('Format: Lightning Labs (macaroon + invoice in WWW-Authenticate)');
    const satoshis = decodeBolt11AmountSats(lightningLabs.invoice);
    const output = {
      url: args.url,
      canonicalUrl: canonicalUrl !== args.url ? canonicalUrl : undefined,
      l402_detected: true,
      format: 'lightning-labs',
      macaroon: lightningLabs.macaroon,
      invoice: lightningLabs.invoice,
      satoshis,
      satoshisFormatted: satoshis !== null ? `${satoshis} sats` : null,
    };
    console.log(JSON.stringify(output, null, 2));
    return;
  }

  // ── Try l402-protocol.org format (JSON body) ──
  let bodyJson = null;
  try {
    const bodyText = await res.text();
    bodyJson = JSON.parse(bodyText);
  } catch {
    // Not JSON — report raw
  }

  const l402proto = parseL402ProtocolBody(bodyJson);

  if (l402proto) {
    console.error('Format: l402-protocol.org (JSON offers)');

    let invoice = null;
    let offerId = null;

    if (l402proto.paymentRequestUrl) {
      console.error(`Fetching invoice from: ${l402proto.paymentRequestUrl}`);
      const fetched = await fetchL402ProtocolInvoice(l402proto.paymentRequestUrl, 15_000, allowHosts);
      if (fetched) {
        invoice = fetched.invoice;
        offerId = fetched.offerId;
      }
    }

    const satoshis = invoice ? decodeBolt11AmountSats(invoice) : null;

    const output = {
      url: args.url,
      canonicalUrl: canonicalUrl !== args.url ? canonicalUrl : undefined,
      l402_detected: true,
      format: 'l402-protocol',
      version: l402proto.version,
      paymentRequestUrl: l402proto.paymentRequestUrl,
      offers: l402proto.offers,
      invoice,
      offerId,
      satoshis,
      satoshisFormatted: satoshis !== null ? `${satoshis} sats` : null,
    };
    console.log(JSON.stringify(output, null, 2));
    return;
  }

  // ── Unknown 402 format ──
  console.error('Warning: 402 received but could not parse L402 challenge.');
  const output = {
    url: args.url,
    canonicalUrl: canonicalUrl !== args.url ? canonicalUrl : undefined,
    l402_detected: true,
    format: 'unknown',
    wwwAuthenticate: wwwAuth || null,
    body: bodyJson,
    message: 'Received 402 but could not identify Lightning Labs or l402-protocol format.',
  };
  console.log(JSON.stringify(output, null, 2));
}

if (require.main === module) {
  main().catch((e) => {
    console.error('Error:', e.message);
    process.exit(1);
  });
}

module.exports = {
  parseArgs,
  ARG_OPTIONS,
  parseLightningLabsHeader,
  parseL402ProtocolBody,
  decodeBolt11AmountSats,
  decodeBolt11AmountMsats,
  budgetChargeFromInvoice,
  fetchL402ProtocolInvoice,
  resolveCanonicalUrl,
  main,
};
