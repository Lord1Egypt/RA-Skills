#!/usr/bin/env node
/**
 * Blink Wallet - L402 Auto-Pay Client
 *
 * Usage: node l402_pay.js <url> [options]
 *
 * Makes an HTTP request to a URL. If it returns 402 Payment Required,
 * automatically parses the L402 challenge, pays the Lightning invoice via
 * the Blink wallet, and retries the request with the payment proof.
 *
 * Supports both L402 formats:
 *   - Lightning Labs: WWW-Authenticate: L402 macaroon="...", invoice="lnbc..."
 *   - l402-protocol.org: JSON body with payment_request_url and offers array
 *
 * Cached tokens (from previous payments) are checked first to avoid re-paying.
 *
 * Arguments:
 *   url              - Required. The URL to access.
 *   --wallet         - Optional. BTC (default) or USD.
 *   --max-amount     - Optional. Refuse to pay more than N sats (safety limit).
 *   --dry-run        - Optional. Discover price without paying.
 *   --method         - Optional. HTTP method: GET (default) or POST.
 *   --header         - Optional. Extra request header in key:value format (repeatable).
 *   --body           - Optional. Request body (for POST requests).
 *   --no-store       - Optional. Do not read from or write to the token store.
 *   --force          - Optional. Pay even if a cached token exists.
 *   --probe          - Optional. Run a fee probe before paying; warns and continues if route not found.
 *
 * Environment:
 *   BLINK_API_KEY    - Required. Blink API key with Write scope.
 *   BLINK_API_URL    - Optional. Override Blink GraphQL endpoint.
 *
 * Dependencies: None (uses Node.js built-in fetch + _blink_client.js)
 *
 * CAUTION: This sends real bitcoin. The API key must have Write scope.
 *
 * Output: JSON to stdout. Status messages to stderr.
 */

'use strict';

const {
  getApiKey,
  getApiUrl,
  graphqlRequest,
  getWallet,
  formatBalance,
  MUTATION_TIMEOUT_MS,
  strictArgv,
} = require('./_blink_client');

const {
  parseLightningLabsHeader,
  parseL402ProtocolBody,
  decodeBolt11AmountSats,
  budgetChargeFromInvoice,
  fetchL402ProtocolInvoice,
} = require('./l402_discover');

const { saveToken, getToken, storeKeyFor } = require('./l402_store');

const {
  reserveBudget,
  checkBudget,
  checkDomainAllowed,
  settleSpend,
  releaseSpend,
  getAllowHosts,
} = require('./_budget');
// The URL-policy guard shared with the LNURL flows: private/loopback/link-local
// address rejection (incl. IPv4-mapped IPv6), manual redirects re-validated
// per hop, hop limit, and the budget allowlist when configured (audit FT:
// these scripts previously used bare fetch with redirect:'follow').
const {
  fetchWithRetry,
  assertAllowedUrl,
  withholdHeadersIfCrossOrigin,
  l402Allowlist,
  decodeBolt11,
} = require('./_lnurl');

// ── GraphQL mutation (same as pay_invoice.js) ─────────────────────────────────

const PAY_INVOICE_MUTATION = `
  mutation LnInvoicePaymentSend($input: LnInvoicePaymentInput!) {
    lnInvoicePaymentSend(input: $input) {
      status
      errors {
        code
        message
        path
      }
      transaction {
        initiationVia {
          ... on InitiationViaLn {
            paymentHash
          }
        }
        settlementVia {
          ... on SettlementViaLn {
            preImage
          }
          ... on SettlementViaIntraLedger {
            preImage
          }
        }
      }
    }
  }
`;

// Query to retrieve preimage by payment hash (fallback).
// Used when the mutation response does not include settlementVia (e.g. race condition, network issue).
const TRANSACTIONS_BY_HASH_QUERY = `
  query TransactionsForPreimage($first: Int, $walletIds: [WalletId]) {
    me {
      defaultAccount {
        transactions(first: $first, walletIds: $walletIds) {
          edges {
            node {
              initiationVia {
                ... on InitiationViaLn {
                  paymentHash
                }
              }
              settlementVia {
                ... on SettlementViaLn {
                  preImage
                }
                ... on SettlementViaIntraLedger {
                  preImage
                }
              }
            }
          }
        }
      }
    }
  }
`;

// ── Fee probe mutations ───────────────────────────────────────────────────────

const FEE_PROBE_BTC_MUTATION = `
  mutation LnInvoiceFeeProbe($input: LnInvoiceFeeProbeInput!) {
    lnInvoiceFeeProbe(input: $input) {
      amount
      errors {
        code
        message
        path
      }
    }
  }
`;

const FEE_PROBE_USD_MUTATION = `
  mutation LnUsdInvoiceFeeProbe($input: LnUsdInvoiceFeeProbeInput!) {
    lnUsdInvoiceFeeProbe(input: $input) {
      amount
      errors {
        code
        message
        path
      }
    }
  }
`;

/**
 * Run a fee probe for a Lightning invoice via the Blink API.
 *
 * Returns an object with:
 *   { estimatedFeeSats: number | null, error: string | null }
 *
 * Never throws — errors are captured and returned as { error }.
 * The caller decides whether to abort or warn-and-continue.
 *
 * @param {string} invoice   BOLT-11 payment request.
 * @param {object} opts
 * @param {string} opts.walletId
 * @param {string} opts.walletCurrency  'BTC' or 'USD'
 * @param {string} opts.apiKey
 * @param {string} opts.apiUrl
 * @returns {Promise<{ estimatedFeeSats: number | null, error: string | null }>}
 */
async function runFeeProbe(invoice, { walletId, walletCurrency, apiKey, apiUrl }) {
  const mutation = walletCurrency === 'USD' ? FEE_PROBE_USD_MUTATION : FEE_PROBE_BTC_MUTATION;
  const mutationKey = walletCurrency === 'USD' ? 'lnUsdInvoiceFeeProbe' : 'lnInvoiceFeeProbe';
  try {
    const data = await graphqlRequest({
      query: mutation,
      variables: { input: { walletId, paymentRequest: invoice } },
      apiKey,
      apiUrl,
      timeoutMs: MUTATION_TIMEOUT_MS,
    });
    const result = data[mutationKey];
    if (result.errors && result.errors.length > 0) {
      const msg = result.errors.map((e) => `${e.message}${e.code ? ` [${e.code}]` : ''}`).join(', ');
      return { estimatedFeeSats: null, error: msg };
    }
    return { estimatedFeeSats: result.amount ?? null, error: null };
  } catch (err) {
    return { estimatedFeeSats: null, error: err.message };
  }
}

// ── Arg parsing ───────────────────────────────────────────────────────────────

// Every option l402-pay accepts; anything else is refused (PR #26 review).
const L402_PAY_OPTIONS = {
  wallet: { type: 'string' },
  'max-amount': { type: 'string' },
  wait: { type: 'string' },
  'dry-run': { type: 'boolean' },
  method: { type: 'string' },
  header: { type: 'string', multiple: true },
  body: { type: 'string' },
  'no-store': { type: 'boolean' },
  force: { type: 'boolean' },
  probe: { type: 'boolean' },
  spark: { type: 'boolean' },
};

function parseArgs(argv) {
  // Strict first: an unknown/malformed option (e.g. `--dry-run=true`, a
  // valueless `--max-amount`) used to be silently dropped — refuse it.
  try {
    argv = strictArgv(argv, L402_PAY_OPTIONS, { positionals: [0, 1] });
  } catch (err) {
    console.error(`Error: ${err.message}`);
    process.exit(1);
  }
  let url = null;
  let walletCurrency = 'BTC';
  let maxAmount = null;
  let waitSeconds = 60;
  let dryRun = false;
  let method = 'GET';
  let noStore = false;
  let force = false;
  let probe = false;
  let spark = false;
  let body = null;
  const headers = {};

  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];

    if (arg === '--spark') {
      spark = true;
    } else if (arg === '--wallet' && i + 1 < argv.length) {
      walletCurrency = argv[++i].toUpperCase();
      if (!['BTC', 'USD'].includes(walletCurrency)) {
        console.error('Error: --wallet must be BTC or USD');
        process.exit(1);
      }
    } else if (arg === '--max-amount' && i + 1 < argv.length) {
      const n = parseInt(argv[++i], 10);
      if (isNaN(n) || n <= 0) {
        console.error('Error: --max-amount must be a positive integer (sats)');
        process.exit(1);
      }
      maxAmount = n;
    } else if (arg === '--wait' && i + 1 < argv.length) {
      // Full-string integer validation: parseInt's prefix parsing would
      // silently accept '0.5' as 0 (disabling the settlement poll entirely),
      // '10seconds' as 10, and '1e2' as 1. Arbitrarily long digit strings
      // convert to Infinity (an infinite deadline), so a documented maximum
      // of 1 hour is enforced too.
      const raw = argv[++i];
      if (!/^\d+$/.test(raw)) {
        console.error('Error: --wait must be a non-negative whole number of seconds (0 disables settlement polling)');
        process.exit(1);
      }
      const n = Number(raw);
      if (!Number.isSafeInteger(n) || n > 3600) {
        console.error('Error: --wait must be at most 3600 seconds (1 hour)');
        process.exit(1);
      }
      waitSeconds = n;
    } else if (arg === '--dry-run') {
      dryRun = true;
    } else if (arg === '--no-store') {
      noStore = true;
    } else if (arg === '--force') {
      force = true;
    } else if (arg === '--probe') {
      probe = true;
    } else if (arg === '--method' && i + 1 < argv.length) {
      method = argv[++i].toUpperCase();
      if (!['GET', 'POST', 'PUT', 'DELETE', 'PATCH'].includes(method)) {
        console.error('Error: unsupported --method');
        process.exit(1);
      }
    } else if (arg === '--header' && i + 1 < argv.length) {
      const hdr = argv[++i];
      const colon = hdr.indexOf(':');
      if (colon < 1) {
        console.error(`Error: --header must be key:value, got: ${hdr}`);
        process.exit(1);
      }
      headers[hdr.slice(0, colon).trim()] = hdr.slice(colon + 1).trim();
    } else if (arg === '--body' && i + 1 < argv.length) {
      body = argv[++i];
    } else if (!arg.startsWith('--')) {
      url = arg;
    }
  }

  return { url, walletCurrency, maxAmount, waitSeconds, dryRun, method, noStore, force, probe, spark, headers, body };
}

// ── HTTP helpers ──────────────────────────────────────────────────────────────

/**
 * Make an HTTP request with a timeout.
 *
 * @param {string} url
 * @param {object} options   fetch options
 * @param {number} [timeoutMs=15000]
 * @returns {Promise<Response>}
 */
async function fetchWithTimeout(url, options, timeoutMs = 15_000, allowedHosts = null) {
  // Guarded fetch: every hop of every redirect is re-validated by
  // assertAllowedUrl inside fetchWithRetry (manual redirects). Retries stay 0
  // here — the original wrapper was single-attempt, and blind retries of a
  // timed-out POST could double-pay a non-idempotent request. Every body on
  // the l402_pay paths is OPERATOR-supplied (args.body) — flagged so the
  // redirect engine refuses to forward it across origins (the internal
  // payment_request_url {} payload calls fetchWithRetry directly and is
  // exempt as a call-site-generated body).
  return fetchWithRetry(url, {
    timeoutMs,
    retries: 0,
    allowedHosts,
    what: 'L402 resource',
    portsUnrestricted: true,
    strictLocal: true,
    ...options,
    // Wrapper-owned provenance, derived AFTER the spread so no caller option
    // can override it: every body on the l402_pay paths is operator-supplied
    // (args.body) — the redirect engine refuses to forward it across origins.
    operatorBody: options.body !== null && options.body !== undefined,
  });
}

/**
 * Resolve the canonical URL by following any HTTP redirects.
 *
 * Sends a HEAD request with redirect:'follow' and returns response.url —
 * the final URL after the redirect chain. This prevents two failure modes:
 *
 *   1. Requests issued at a non-canonical URL (e.g. www.satring.com instead
 *      of satring.com). NOTE: the token cache is NOT keyed by this URL — a
 *      HEAD can land somewhere other than the real request (method-dependent
 *      redirects), so the credential is bound to the URL that actually issued
 *      the 402 (challengeUrl in main).
 *   2. L402 Authorization header stripped by fetch on the retry request
 *      because the WHATWG Fetch spec forbids forwarding Authorization across
 *      cross-host redirects (redirect-fetch step 12).
 *
 * Falls back gracefully to the original URL on any error (network failure,
 * 405 Method Not Allowed, etc.) so existing behaviour is preserved.
 *
 * @param {string} url
 * @param {number} [timeoutMs=10000]
 * @returns {Promise<string>}  The canonical URL (post-redirect), or the
 *                             original URL if resolution fails.
 */
async function resolveCanonicalUrl(url, timeoutMs = 10_000, allowedHosts = null) {
  // Policy first, synchronously: a refused target must abort the whole flow,
  // never fall back to fetching it anyway.
  assertAllowedUrl(url, allowedHosts, 'L402 URL', { portsUnrestricted: true, strictLocal: true });
  try {
    const res = await fetchWithRetry(url, {
      method: 'HEAD',
      timeoutMs,
      retries: 1,
      allowedHosts,
      what: 'L402 URL',
      portsUnrestricted: true,
      strictLocal: true,
    });
    // res.url is the final URL after the (manually re-validated) redirects;
    // fall back to input if empty.
    return res.url || url;
  } catch (err) {
    if (err && err.code === 'URL_POLICY') throw err; // a redirect went hostile
    // Network error, timeout, or server that rejects HEAD — degrade gracefully.
    return url;
  }
}

/**
 * Extract the domain (hostname) from a URL string.
 * @param {string} url
 * @returns {string}
 */
function extractDomain(url) {
  try {
    return new URL(url).hostname;
  } catch {
    return url;
  }
}

// ── L402 challenge resolution ─────────────────────────────────────────────────

/**
 * Resolve an L402 challenge from a 402 response.
 * Returns the invoice to pay and the macaroon token.
 *
 * @param {Response} res
 * @returns {Promise<{ invoice: string, macaroon: string, format: string } | null>}
 */
async function resolveL402Challenge(res, allowedHosts = null) {
  // Try Lightning Labs format (WWW-Authenticate header)
  const wwwAuth = res.headers.get('www-authenticate') || '';
  const lightningLabs = parseLightningLabsHeader(wwwAuth);
  if (lightningLabs) {
    return {
      invoice: lightningLabs.invoice,
      macaroon: lightningLabs.macaroon,
      format: 'lightning-labs',
    };
  }

  // Try l402-protocol.org format (JSON body)
  let bodyJson = null;
  try {
    const text = await res.text();
    bodyJson = JSON.parse(text);
  } catch {
    return null;
  }

  const l402proto = parseL402ProtocolBody(bodyJson);
  if (!l402proto) return null;

  if (!l402proto.paymentRequestUrl) return null;

  console.error(`Fetching payment request from: ${l402proto.paymentRequestUrl}`);
  const fetched = await fetchL402ProtocolInvoice(l402proto.paymentRequestUrl, undefined, allowedHosts);
  if (!fetched) return null;

  // For l402-protocol format, the "macaroon" is the token returned after payment.
  // We store the offer id as the pre-payment token placeholder.
  return {
    invoice: fetched.invoice,
    macaroon: fetched.offerId || '',
    format: 'l402-protocol',
    offerId: fetched.offerId,
    paymentRequestUrl: l402proto.paymentRequestUrl,
    offers: l402proto.offers,
  };
}

// ── Preimage resolution ───────────────────────────────────────────────────────

/**
 * Attempt to retrieve the real payment preimage from the Blink transactions list.
 *
 * This is the fallback path: a second GraphQL query after payment, matching
 * by paymentHash from lnInvoicePaymentSend's transaction. Used when the
 * inline preimage from the mutation response is unavailable.
 *
 * Returns the preimage hex string if found, or null if not available yet.
 *
 * @param {string} paymentHash  64-char hex payment hash (from initiationVia.paymentHash).
 * @param {object} opts
 * @param {string} opts.apiKey
 * @param {string} opts.apiUrl
 * @param {string} [opts.walletId]  Optional: narrow to one wallet.
 * @returns {Promise<string|null>}
 */
async function fetchPreimageByPaymentHash(paymentHash, { apiKey, apiUrl, walletId }) {
  if (!paymentHash) return null;
  try {
    const variables = { first: 10 };
    if (walletId) variables.walletIds = [walletId];

    const data = await graphqlRequest({
      query: TRANSACTIONS_BY_HASH_QUERY,
      variables,
      apiKey,
      apiUrl,
      timeoutMs: 10_000,
    });

    const edges = data?.me?.defaultAccount?.transactions?.edges ?? [];
    for (const { node } of edges) {
      const txHash = node?.initiationVia?.paymentHash;
      if (txHash && txHash.toLowerCase() === paymentHash.toLowerCase()) {
        const preImage = node?.settlementVia?.preImage;
        if (preImage) return preImage;
      }
    }
  } catch (err) {
    console.error(`Warning: preimage lookup query failed: ${err.message}`);
  }
  return null;
}

// ── Main ──────────────────────────────────────────────────────────────────────

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (!args.url) {
    console.error(
      'Usage: node l402_pay.js <url> [--wallet BTC|USD] [--max-amount <sats>] [--dry-run] [--no-store] [--force]',
    );
    process.exit(1);
  }

  // ── URL policy (pre-flight, before ANY outbound request) ──
  // Security-audit fix: the domain gate used to run ~200 lines AFTER the
  // first network request (canonicalization + challenge probe), so an agent
  // handed a hostile URL probed it before any policy check. Non-dry-run now
  // refuses on the SUPPLIED URL's domain before a single byte leaves the
  // machine; the canonical-domain gate below still catches cross-domain
  // redirects at payment time. All fetches (including the server-supplied
  // l402-protocol payment_request_url) route through the shared SSRF guard.
  // Non-dry-run: the allowlist is EXCLUSIVE for every fetch (v2.6.1).
  // --dry-run is the documented ungated preview: the list may only relax the
  // SSRF guard there (FT7, v3.0.2 — it was enforced as exclusive).
  // In relax-only mode the private/local exception is bound to the host the
  // operator chose, never inherited by redirect or server-supplied hops (PR #25 review).
  const allowHosts = l402Allowlist(getAllowHosts(), { relaxOnly: args.dryRun, operatorUrl: args.url });
  if (!args.dryRun) {
    // requireConfigured:false — an UNCONFIGURED allowlist leaves probing open
    // (the documented free-resource discovery mode; still SSRF-guarded, and
    // payment below remains fail-closed), but WHEN a policy exists it now
    // gates every outbound request, not only the payment itself.
    const preflight = checkDomainAllowed(extractDomain(args.url), { requireConfigured: false });
    if (!preflight.allowed) {
      console.log(
        JSON.stringify(
          {
            event: 'l402_domain_blocked',
            url: args.url,
            domain: extractDomain(args.url),
            allowlist: preflight.allowlist,
            message:
              preflight.reason ||
              `Domain "${extractDomain(args.url)}" is not in the L402 allowlist. Add with: blink budget allowlist add ${extractDomain(args.url)}`,
          },
          null,
          2,
        ),
      );
      // Not process.exit(): it can truncate piped stdout; entry points drain, then exit (PR #25).
      process.exitCode = 1;
      return;
    }
  }

  // ── Resolve canonical URL (follow any HTTP redirects — guarded) ──
  // This must happen before any fetch so that the L402
  // Authorization header is not stripped by fetch when following redirects
  // from a non-canonical URL (WHATWG Fetch spec forbids forwarding
  // Authorization across cross-host redirects).
  const canonicalUrl = await resolveCanonicalUrl(args.url, 10_000, allowHosts);
  if (canonicalUrl !== args.url) {
    console.error(`Resolved redirect: ${args.url} → ${canonicalUrl}`);
    // FT6 finding (MEDIUM), review round 1: canonicalization consumes the
    // redirect chain with a bare HEAD; every subsequent request below is then
    // issued DIRECTLY at the canonical URL as a fresh first hop — the in-chain
    // origin policy never sees that transition. The SHARED policy
    // (withholdHeadersIfCrossOrigin) withholds the ENTIRE operator header set
    // when origins differ: custom credential names (X-API-Key, …) cannot be
    // enumerated. (The cached L402 Authorization is injected per-request, not
    // part of the operator set; it is bound to the URL that actually ISSUED the
    // 402 — see challengeUrl below — never to this HEAD-derived URL.)
    const originPolicy = withholdHeadersIfCrossOrigin(args.url, canonicalUrl, args.headers);
    if (originPolicy.withheld.length > 0) {
      args.headers = originPolicy.headers;
      console.error(
        `Warning: canonicalization crossed origins — ALL operator-supplied headers (${originPolicy.withheld.join(', ')}) are withheld from the request.`,
      );
    }
    // Body provenance (review round 3): canonicalization consumes the
    // redirect chain with a bare HEAD, which BYPASSES the method-rewrite
    // semantics (a POST 302 would normally become GET) — sending the original
    // method + operator body straight to the final origin would disclose the
    // body in a form the corresponding real request would never produce.
    // Refuse: the operator can re-invoke the final URL. (crossOrigin, not
    // withheld.length — a body-only request has no headers to withhold.)
    if (originPolicy.crossOrigin && args.body !== null && args.body !== undefined) {
      const refusal = new Error(
        `Canonicalization crossed origins (${args.url} → ${canonicalUrl}) and this request carries an ` +
          `operator-supplied body — refusing to forward it. Invoke the final URL explicitly: ${canonicalUrl}`,
      );
      refusal.code = 'URL_POLICY'; // same machine-readable code as the in-chain refusal
      throw refusal;
    }
  }

  // ── Initial request ──
  console.error(`Requesting: ${canonicalUrl}`);
  const reqOptions = {
    method: args.method,
    headers: { Accept: 'application/json', ...args.headers },
    ...(args.body ? { body: args.body } : {}),
  };

  const initialRes = await fetchWithTimeout(canonicalUrl, reqOptions, 15_000, allowHosts);

  if (initialRes.status === 200) {
    const body = await initialRes.text();
    let data;
    try {
      data = JSON.parse(body);
    } catch {
      data = body;
    }
    const output = {
      event: 'l402_not_required',
      url: args.url,
      canonicalUrl: canonicalUrl !== args.url ? canonicalUrl : undefined,
      status: 200,
      message: 'Resource returned 200 OK — no payment required.',
      data,
    };
    console.log(JSON.stringify(output, null, 2));
    return;
  }

  if (initialRes.status !== 402) {
    const body = await initialRes.text().catch(() => '');
    // On --dry-run, emit structured JSON instead of throwing so the caller
    // always gets machine-readable output even when the server is down or
    // returns an unexpected status (e.g. 403/503 during an outage).
    if (args.dryRun) {
      const output = {
        event: 'l402_dry_run',
        url: args.url,
        canonicalUrl: canonicalUrl !== args.url ? canonicalUrl : undefined,
        status: initialRes.status,
        error: `Unexpected status ${initialRes.status}: ${body.slice(0, 200)}`,
        message: 'Dry-run: server did not return 402. No payment would be made.',
      };
      console.log(JSON.stringify(output, null, 2));
      return;
    }
    throw new Error(`Unexpected status ${initialRes.status}: ${body.slice(0, 200)}`);
  }

  // ── Credential owner: the URL that actually ISSUED the 402 ──
  // PR #24 review (High): the HEAD canonicalization is credential-free and can
  // land somewhere other than the real request — a service may answer HEAD
  // itself but redirect GET/POST elsewhere (method-dependent redirects). The
  // challenge (invoice + macaroon) comes from wherever the REAL request ended
  // up, so that URL owns the credential: the cache key, the allowlist/budget
  // domain, and every credentialed request (paid retry and cache reuse) are
  // derived from it, and the bearer is sent DIRECTLY to it — never to a first
  // hop that would see it before cross-origin redirect stripping can act.
  // initialRes.url is the final hop of the guarded, per-hop-validated chain
  // (same mechanism as resolveCanonicalUrl); fall back if absent.
  const challengeUrl = initialRes.url || canonicalUrl;

  // ── Replay exactly the request that was challenged ──
  // PR #24 review rounds 2-3: the credentialed requests go DIRECTLY to
  // challengeUrl, bypassing the redirect walker, so they must be the walker's
  // final request VERBATIM plus the bearer — never rebuilt from the original
  // --method/--header/--body. Hand-rebuilt fields drifted three ways: the URL,
  // the method/body (301/302/303 rewrites), and the headers (a cross-origin hop
  // clears operator headers for the rest of the chain, so A → B → A ends at A
  // with NONE; a rewrite strips body headers). The walker reports the exact
  // request it sent; there is deliberately no fallback to reconstruction.
  const challenged = initialRes.challengedRequest;
  if (!challenged) {
    throw new Error('Internal error: the challenged request state is unavailable; refusing to send a credential.');
  }
  // A rewrite that DROPPED an operator body is refused before payment, on ANY
  // origin: paying for — then authorizing — a body-less GET would silently be
  // a different operation than the one invoked, and a payment cannot be undone.
  if (initialRes.bodyDropped) {
    const refusal = new Error(
      `The server redirected this ${String(args.method).toUpperCase()} to ${challenged.method} ` +
        `${challengeUrl} and the redirect dropped the operator-supplied body — refusing to pay for or ` +
        `forward a different request than the one invoked. Invoke the issuing URL explicitly: ${challengeUrl}`,
    );
    refusal.code = 'URL_POLICY';
    throw refusal;
  }
  // Defense in depth: the walker already refuses an operator body that would
  // survive a cross-origin hop (307/308), so this cannot fire in practice.
  if (challenged.body !== undefined && new URL(challengeUrl).origin !== new URL(canonicalUrl).origin) {
    const refusal = new Error(
      `The L402 challenge was issued by another origin (${canonicalUrl} → ${challengeUrl}) and this request ` +
        `carries an operator-supplied body — refusing to forward it. Invoke the issuing URL explicitly: ${challengeUrl}`,
    );
    refusal.code = 'URL_POLICY';
    throw refusal;
  }
  if (String(challenged.method).toUpperCase() !== String(args.method).toUpperCase()) {
    console.error(
      `Note: the redirect rewrote ${args.method} to ${challenged.method}; the challenged request is replayed as-is.`,
    );
  }
  // The L402 bearer is the ONLY Authorization on a credentialed request: an
  // operator --header Authorization (any case) would otherwise override it or
  // be sent alongside it (a header object with both spellings merges).
  const replayHeaders = {};
  const droppedAuth = [];
  for (const [k, v] of Object.entries(challenged.headers)) {
    if (k.toLowerCase() === 'authorization') droppedAuth.push(k);
    else replayHeaders[k] = v;
  }
  if (droppedAuth.length > 0) {
    console.error(
      `Warning: the operator-supplied ${droppedAuth.join(', ')} header is not sent with the L402 credential — ` +
        'the paid L402 Authorization replaces it.',
    );
  }
  /** Both credentialed requests (cache reuse, paid retry): the challenged request + the bearer, nothing else. */
  const credentialedRequest = (authHeader) => ({
    method: challenged.method,
    headers: { ...replayHeaders, Authorization: authHeader },
    ...(challenged.body !== undefined ? { body: challenged.body } : {}),
  });

  if (challengeUrl !== canonicalUrl) {
    console.error(`L402 challenge issued by: ${challengeUrl}`);
  }
  const challengeUrlField = challengeUrl !== canonicalUrl ? challengeUrl : undefined;

  const domain = extractDomain(challengeUrl);
  // Origin isolation (ClawHub review of v3.0.0): the key is the issuing URL's
  // ORIGIN (scheme + host + port) + path, so a token is never replayed to a
  // different service on another port or to plaintext http. null = unkeyable:
  // neither reuse nor cache (never a raw-string key).
  const storeKey = storeKeyFor(challengeUrl);
  const useStore = !args.noStore && storeKey !== null;

  // ── Reuse a cached token for the issuing URL ──
  // Looked up only now, after the real request proved who issues the challenge
  // (one extra uncredentialed request on a cache hit — the price of never
  // sending a bearer to an unverified origin). Skipped on --dry-run: dry-run
  // must always report the current invoice price. Budget/domain enforcement
  // applies only when a payment is actually made.
  if (useStore && !args.force && !args.dryRun) {
    const cached = getToken(storeKey);
    if (cached) {
      console.error(`Using cached L402 token for ${storeKey} (paid ${cached.satoshis ?? '?'} sats previously).`);
      console.error('Retrying request with cached token...');

      const authHeader = `L402 ${cached.macaroon}:${cached.preimage}`;
      // FT7 (v3.0.2): a transport failure here used to escape as a bare
      // "Error: terminated" with NOTHING on stdout — always emit JSON.
      let res;
      let body;
      try {
        res = await fetchWithTimeout(challengeUrl, credentialedRequest(authHeader), 15_000, allowHosts);
        body = await res.text();
      } catch (err) {
        // EVERY failure here — transport or URL policy (a credentialed response
        // redirecting to a forbidden host, PR #25 review) — is reported as JSON.
        const output = {
          event: 'l402_reuse_failed',
          url: args.url,
          canonicalUrl: canonicalUrl !== args.url ? canonicalUrl : undefined,
          challengeUrl: challengeUrlField,
          tokenReused: true,
          backend: cached.backend ?? null,
          satoshis: cached.satoshis ?? null,
          error: describeFetchError(err),
          ...(err && err.code ? { errorCode: err.code } : {}),
          message:
            'The cached L402 token was sent but the request failed before a response arrived; no payment was made. ' +
            'Re-run to retry with the same token, or pass --force to pay for a fresh one.',
        };
        console.log(JSON.stringify(output, null, 2));
        // exitCode, not process.exit(): both entry points drain stdout before
        // exiting, so a piped consumer always receives the whole JSON.
        process.exitCode = 1;
        return;
      }

      let data;
      try {
        data = JSON.parse(body);
      } catch {
        data = body;
      }

      if (res.status !== 200) {
        // Cached token rejected or server unreachable — emit l402_error so the
        // caller can distinguish a successful cached-token hit from a failure.
        const output = {
          event: 'l402_error',
          url: args.url,
          canonicalUrl: canonicalUrl !== args.url ? canonicalUrl : undefined,
          challengeUrl: challengeUrlField,
          status: res.status,
          tokenReused: true,
          satoshis: cached.satoshis ?? null,
          message: `Cached token returned status ${res.status}. Token may be expired or server is unreachable.`,
          data,
        };
        console.log(JSON.stringify(output, null, 2));
        // Not process.exit(): it can truncate piped stdout; entry points drain, then exit (PR #25).
        process.exitCode = 1;
        return;
      }

      const output = {
        event: 'l402_paid',
        url: args.url,
        canonicalUrl: canonicalUrl !== args.url ? canonicalUrl : undefined,
        challengeUrl: challengeUrlField,
        status: res.status,
        tokenReused: true,
        backend: cached.backend ?? null,
        satoshis: cached.satoshis ?? null,
        invoiceMsats: cached.invoiceMsats ?? null,
        budgetSats: cached.budgetSats ?? null,
        data,
      };
      console.log(JSON.stringify(output, null, 2));
      return;
    }
  }

  console.error('402 Payment Required — parsing L402 challenge...');

  // ── Resolve challenge ──
  const challenge = await resolveL402Challenge(initialRes, allowHosts);
  if (!challenge) {
    throw new Error('Could not parse L402 challenge from 402 response. Try l402_discover.js for diagnostics.');
  }

  console.error(`Format: ${challenge.format}`);

  const satoshis = decodeBolt11AmountSats(challenge.invoice);
  // The budget charge, structured: msats=null means undecodable; any positive
  // decodable amount charges max(1, ceil(msats/1000)). Enforcement (refusal,
  // --max-amount, reservation, record) uses the charge — never the
  // round-to-nearest display value, which can push a sub-satoshi invoice up
  // to 1 sat or shave fractions off larger ones.
  const charge = budgetChargeFromInvoice(challenge.invoice);
  const budgetSats = charge.budgetSats;

  if (satoshis === null) {
    console.error('Warning: could not decode amount from invoice.');
  } else {
    console.error(`Payment required: ${satoshis} sats`);
  }
  if (budgetSats !== null && budgetSats !== satoshis) {
    console.error(`Note: budget charges ${budgetSats} sats conservatively for this fractional-satoshi invoice.`);
  }

  // An undecodable — or sub-satoshi — amount cannot be budget-checked, so
  // paying it would spend a sum against limits that were never applied.
  // Refusal applies to dry-run exactly like real execution: a preview must
  // never green-light what execution rejects.
  if (charge.msats === null || charge.msats < 1000) {
    const output = {
      event: 'l402_amount_undecodable',
      url: args.url,
      canonicalUrl: canonicalUrl !== args.url ? canonicalUrl : undefined,
      invoice: challenge.invoice,
      invoiceMsats: charge.msats,
      message:
        'Refusing to pay: the invoice amount could not be decoded or is below 1 satoshi, so budget ' +
        'and --max-amount limits cannot be enforced. Inspect it with --dry-run, or pay the ' +
        'invoice explicitly with `blink pay-invoice` if you trust it.',
    };
    console.log(JSON.stringify(output, null, 2));
    // Not process.exit(): it can truncate piped stdout; entry points drain, then exit (PR #25).
    process.exitCode = 1;
    return;
  }

  // ── Payment backend selection ──
  // --spark forces the self-custodial leg (Breez SDK signs locally). Without
  // it, Spark is auto-selected when it is the only available wallet: no
  // Blink API key, but a seed is present. Custodial remains the default.
  // A dry-run dispatches nothing and loads no SDK, so it is credential-free
  // for both backends — the checks below are skipped for it.
  const hasBlinkKey = Boolean(process.env.BLINK_API_KEY);
  const hasSparkSeed = Boolean(process.env.SPARK_MNEMONIC);
  let sparkBackend = Boolean(args.spark);
  if (!args.spark && !hasBlinkKey && hasSparkSeed) {
    sparkBackend = true;
    console.error('No BLINK_API_KEY — paying via the self-custodial (Spark) backend.');
  }
  if (sparkBackend && !args.dryRun) {
    if (!hasSparkSeed) {
      console.error('Error: the Spark backend requires SPARK_MNEMONIC.');
      process.exit(1);
    }
    if (!process.env.BREEZ_API_KEY) {
      console.error('Error: the Spark backend requires BREEZ_API_KEY (get one at breez.technology).');
      process.exit(1);
    }
    if (args.walletCurrency === 'USD') {
      console.error('Error: the Spark backend pays from the Spark wallet (BTC only); remove --wallet USD.');
      process.exit(1);
    }
  }

  // Budget reservation state at function scope: the reservation happens inside
  // the enforcement block below, but the pay section that follows must be able
  // to finalize it (success) or release it (known failure) — and max-amount
  // refusals in between must release it too. Credentials are likewise resolved
  // BEFORE the reservation (per backend) so a missing credential cannot orphan
  // it.
  let reservationId = null;
  let apiKey = null;
  let apiUrl = null;
  let wallet = null;

  // ── Payment enforcement (fail closed) ──
  // A payment is about to be made: require an explicitly configured domain
  // allowlist and budget. --force refreshes the token but never bypasses
  // these checks. Free resources (HTTP 200) never reach this path.
  if (!args.dryRun) {
    const domainCheck = checkDomainAllowed(domain);
    if (!domainCheck.allowed) {
      const output = {
        event: 'l402_domain_blocked',
        url: args.url,
        canonicalUrl: canonicalUrl !== args.url ? canonicalUrl : undefined,
        domain,
        allowlist: domainCheck.allowlist,
        message:
          domainCheck.reason ||
          `Domain "${domain}" is not in the L402 allowlist. Add with: blink budget allowlist add ${domain}`,
      };
      console.log(JSON.stringify(output, null, 2));
      // Not process.exit(): it can truncate piped stdout; entry points drain, then exit (PR #25).
      process.exitCode = 1;
      return;
    }

    // ── Budget reservation (fail closed for autonomous auto-pay) ──
    // The limit decision AND the reservation append happen under one lock, so
    // two concurrent payments can never both pass the same remaining budget.
    // Credentials are resolved FIRST (per backend): a missing credential must
    // not orphan the reservation — no payment is attempted in that case, so
    // nothing should stay reserved. (Spark credential presence was validated
    // at backend selection, before this reservation; connect() re-validates
    // fully at dispatch.)
    if (!sparkBackend) {
      apiKey = getApiKey();
      apiUrl = getApiUrl();
    }
    const reservation = reserveBudget({ sats: budgetSats, command: 'l402-pay', domain }, { requireConfigured: true });
    if (!reservation.allowed) {
      const output = {
        event: 'l402_budget_exceeded',
        url: args.url,
        canonicalUrl: canonicalUrl !== args.url ? canonicalUrl : undefined,
        satoshis,
        ...reservation,
        message: reservation.reason,
      };
      console.log(JSON.stringify(output, null, 2));
      // Not process.exit(): it can truncate piped stdout; entry points drain, then exit (PR #25).
      process.exitCode = 1;
      return;
    }
    reservationId = reservation.id;
  }

  // ── Per-request max-amount check ──
  if (args.maxAmount !== null && budgetSats !== null && budgetSats > args.maxAmount) {
    releaseSpend(reservationId);
    const output = {
      event: 'l402_budget_exceeded',
      url: args.url,
      canonicalUrl: canonicalUrl !== args.url ? canonicalUrl : undefined,
      satoshis,
      maxAmount: args.maxAmount,
      message: `Payment of ${budgetSats} sats exceeds --max-amount of ${args.maxAmount} sats. Aborting.`,
    };
    console.log(JSON.stringify(output, null, 2));
    // Not process.exit(): it can truncate piped stdout; entry points drain, then exit (PR #25).
    process.exitCode = 1;
    return;
  }

  // ── Dry-run: report price and exit ──
  if (args.dryRun) {
    // Reporting only — dry-run never spends. The preview uses the SAME
    // conservative charge as real execution (ceil, never round-to-nearest),
    // and the below-1-sat refusal above already mirrored execution.
    // Opt out of the fail-closed default so an unconfigured budget shows
    // remaining limits instead of a denial.
    const budgetInfo = budgetSats !== null ? checkBudget(budgetSats, { requireConfigured: false }) : null;
    // FT7 (v3.0.2): --probe was silently ignored with --dry-run. The probe is a
    // non-spending estimate — the ACTUAL routing fee can be higher (FT7: 1 sat
    // estimated, 10 charged), and budgets/--max-amount never count fees.
    let dryFeeProbe;
    if (args.probe) {
      if (sparkBackend) {
        dryFeeProbe = {
          estimatedFeeSats: null,
          error: 'not available for --spark in dry-run; run: blink spark-fee-probe <invoice> <amount_sats>',
        };
      } else if (!process.env.BLINK_API_KEY) {
        dryFeeProbe = { estimatedFeeSats: null, error: 'the fee probe requires BLINK_API_KEY' };
      } else {
        try {
          const probeKey = getApiKey();
          const probeUrl = getApiUrl();
          const probeWallet = await getWallet({ apiKey: probeKey, apiUrl: probeUrl, currency: args.walletCurrency });
          dryFeeProbe = await runFeeProbe(challenge.invoice, {
            walletId: probeWallet.id,
            walletCurrency: args.walletCurrency,
            apiKey: probeKey,
            apiUrl: probeUrl,
          });
        } catch (err) {
          dryFeeProbe = { estimatedFeeSats: null, error: err.message };
        }
      }
    }
    const output = {
      event: 'l402_dry_run',
      url: args.url,
      canonicalUrl: canonicalUrl !== args.url ? canonicalUrl : undefined,
      format: challenge.format,
      invoice: challenge.invoice,
      satoshis,
      invoiceMsats: charge.msats,
      budgetSats,
      satoshisFormatted: satoshis !== null ? `${satoshis} sats` : null,
      maxAmount: args.maxAmount,
      withinBudget: args.maxAmount !== null && budgetSats !== null ? budgetSats <= args.maxAmount : null,
      budget: budgetInfo
        ? {
            allowed: budgetInfo.allowed,
            hourlySpent: budgetInfo.hourlySpent,
            dailySpent: budgetInfo.dailySpent,
            hourlyLimit: budgetInfo.hourlyLimit,
            dailyLimit: budgetInfo.dailyLimit,
            effectiveRemaining: budgetInfo.effectiveRemaining,
          }
        : null,
      ...(dryFeeProbe ? { feeProbe: dryFeeProbe } : {}),
      message: 'Dry-run: would pay this invoice to access the resource. No payment made.',
      ...(challenge.offers ? { offers: challenge.offers } : {}),
    };
    console.log(JSON.stringify(output, null, 2));
    return;
  }

  // ── Pay the invoice ──
  // Two payment backends:
  //   custodial (default) — lnInvoicePaymentSend via the Blink API; the
  //     preimage is resolved via the inline/ladder/placeholder fallbacks.
  //   spark (--spark, or auto when no Blink key but a seed) — the Breez SDK
  //     signs locally with the seed; the preimage comes back in the settled
  //     payment's HTLC details.
  // Both legs share the reservation semantics: setup failures RELEASE the
  // reservation, outcome-unknown post-dispatch failures KEEP it, terminal
  // failures release it, and success finalizes via the shared record below.
  let paymentStatus = null;
  let preimage = null;
  let feeProbeResult = null;
  let paidPaymentHash = null; // backend-reported; invoicePaymentHash() fills gaps
  let preimagePlaceholder = false;
  const macaroon = challenge.macaroon;

  if (sparkBackend) {
    // ── Spark (self-custodial) backend ──
    const { payInvoiceViaSpark } = require('./l402_pay_spark');
    console.error(`Paying ${budgetSats} sats via Spark (self-custodial, signs locally)...`);
    let spark;
    try {
      spark = await payInvoiceViaSpark(challenge.invoice, {
        network: process.env.SPARK_NETWORK || 'mainnet',
        waitSeconds: args.waitSeconds,
        // Debug/CI knob for the settlement poll cadence. Validated here and
        // clamped again inside payInvoiceViaSpark: a zero/negative/NaN value
        // must never become a non-terminating hot loop.
        pollIntervalMs: (() => {
          const raw = Number(process.env.BLINK_SPARK_POLL_INTERVAL_MS);
          return process.env.BLINK_SPARK_POLL_INTERVAL_MS !== undefined && Number.isFinite(raw) && raw > 0 ? raw : 3000;
        })(),
      });
    } catch (e) {
      if (e.stage === 'dispatch') {
        // Outcome unknown — the payment may still settle. Keep the
        // reservation (fail-closed) rather than freeing it for a retry.
        if (reservationId) {
          console.error(
            'Warning: payment outcome is unknown after this error, so the budget reservation stays in place ' +
              '(fail-closed, auto-cleared by the 25h prune). Inspect spark-transactions before retrying.',
          );
        }
      } else {
        // Pre-dispatch failure (connect, prepare): nothing moved.
        releaseSpend(reservationId);
      }
      throw e;
    }
    // Status was normalized at the backend boundary (completed→SUCCESS,
    // pending→PENDING, failed→FAILURE; unknown passes raw).
    paymentStatus = spark.status;
    if (spark.feeSats !== null) {
      feeProbeResult = { estimatedFeeSats: spark.feeSats, error: null };
    }

    if (paymentStatus === 'PENDING') {
      // Still in flight after the settlement poll (--wait, default 60s).
      // Spark settlement is asynchronous; count it against the budget like
      // the custodial PENDING path — the sats are committed. No preimage
      // means no L402 token could be captured; say so loudly rather than
      // pretending nothing happened (field-tested failure mode: 1 sat + fee
      // spent, budget debited, token lost).
      if (reservationId) {
        settleSpend({ reservationId, sats: budgetSats, command: 'l402-pay', domain, label: 'the in-flight payment' });
        reservationId = null;
      } else {
        releaseSpend(reservationId);
      }
      const paymentId = (spark.payment && (spark.payment.id || spark.payment.paymentHash)) || null;
      throw new Error(
        `Payment dispatched and still PENDING after ${args.waitSeconds}s — the sats were spent but the L402 token was NOT captured.` +
          (paymentId
            ? ` Payment id: ${paymentId} — inspect \`spark-transactions\` (it may settle; retrying pays again).`
            : ' Inspect `spark-transactions` before retrying — a retry pays again.'),
      );
    }
    if (paymentStatus === 'FAILURE') {
      // The only post-dispatch status that proves nothing settled — the
      // reservation is freed.
      releaseSpend(reservationId);
      throw new Error(`Payment not successful: status=${paymentStatus}`);
    }
    if (paymentStatus !== 'SUCCESS') {
      // Unknown post-dispatch status: the pinned SDK union is completed |
      // pending | failed, but a future status may mean "still in flight" —
      // keep the reservation fail-closed rather than freeing budget for a
      // retry of a payment that may settle.
      if (reservationId) {
        console.error(
          `Warning: unrecognized payment status '${paymentStatus}' after dispatch — the budget reservation stays in place ` +
            '(fail-closed, auto-cleared by the 25h prune). Inspect spark-transactions before retrying.',
        );
      }
      throw new Error(`Payment not successful: status=${paymentStatus}`);
    }
    console.error('Payment successful!');
    preimage = spark.preimage;
    if (!preimage) {
      // Funds moved — the budget must count them — but the L402 token cannot
      // be constructed without the preimage.
      if (reservationId) {
        settleSpend({ reservationId, sats: budgetSats, command: 'l402-pay', domain });
        reservationId = null;
      }
      throw new Error('Spark payment completed but the preimage was not returned — cannot build the L402 token.');
    }
    console.error('Preimage received from the Spark payment details.');
  } else {
    // ── Custodial backend (Blink API) ──
    let payData;
    try {
      wallet = await getWallet({ apiKey, apiUrl, currency: args.walletCurrency });
    } catch (e) {
      releaseSpend(reservationId);
      throw e;
    }
    console.error(`Using ${args.walletCurrency} wallet ${wallet.id} (balance: ${formatBalance(wallet)})`);

    if (args.walletCurrency === 'BTC' && wallet.balance === 0) {
      releaseSpend(reservationId);
      throw new Error('Insufficient balance: BTC wallet has 0 sats.');
    }

    // ── Optional fee probe (--probe) ──
    // Run lnInvoiceFeeProbe before paying to check the route exists.
    // On failure: warn to stderr and continue — probe errors don't mean payment
    // will fail (the probe is best-effort). On success: log estimated fee.
    if (args.probe) {
      console.error('Running fee probe...');
      feeProbeResult = await runFeeProbe(challenge.invoice, {
        walletId: wallet.id,
        walletCurrency: args.walletCurrency,
        apiKey,
        apiUrl,
      });
      if (feeProbeResult.error) {
        console.error(`Warning: fee probe failed (${feeProbeResult.error}) — proceeding with payment anyway.`);
      } else {
        console.error(
          `Fee probe: estimated routing fee = ${feeProbeResult.estimatedFeeSats ?? 0} sats. Proceeding with payment.`,
        );
      }
    }

    console.error(`Paying ${satoshis ?? '?'} sats via Blink...`);

    try {
      payData = await graphqlRequest({
        query: PAY_INVOICE_MUTATION,
        variables: { input: { walletId: wallet.id, paymentRequest: challenge.invoice } },
        apiKey,
        apiUrl,
        timeoutMs: MUTATION_TIMEOUT_MS,
      });
    } catch (e) {
      // Outcome-unknown after dispatch (timeout, lost response, transport
      // reset): the payment may still settle, so the reservation STAYS —
      // freeing it would let another auto-pay double-spend the same window.
      if (reservationId) {
        console.error(
          `Warning: payment outcome is unknown after this error, so the budget reservation stays in place ` +
            `(fail-closed, auto-cleared by the 25h prune). Inspect \`transactions\` before retrying.`,
        );
      }
      throw e;
    }

    const payResult = payData.lnInvoicePaymentSend;

    if (payResult.errors && payResult.errors.length > 0) {
      // Explicit server-side rejection — nothing moved; the budget is freed.
      const errMsg = payResult.errors.map((e) => `${e.message}${e.code ? ` [${e.code}]` : ''}`).join(', ');
      releaseSpend(reservationId);
      throw new Error(`Payment failed: ${errMsg}`);
    }

    if (payResult.status !== 'SUCCESS' && payResult.status !== 'ALREADY_PAID') {
      // PENDING is in flight: count it against the budget like the one-shot pay
      // commands do, then surface the failure — the preimage will not resolve.
      // Same warn-on-restored / warn-on-throw accounting as the normal record path.
      if (payResult.status === 'PENDING' && reservationId && satoshis !== null) {
        settleSpend({ reservationId, sats: budgetSats, command: 'l402-pay', domain, label: 'the in-flight payment' });
        reservationId = null;
      } else {
        releaseSpend(reservationId);
      }
      throw new Error(`Payment not successful: status=${payResult.status}`);
    }

    console.error(`Payment ${payResult.status === 'ALREADY_PAID' ? 'already paid' : 'successful'}!`);
    paymentStatus = payResult.status;

    // ALREADY_PAID means THIS invocation moved no funds — release the current
    // reservation instead of finalizing it (pay_invoice releases for the same
    // status; finalizing here would double-count the invoice against the budget).
    if (payResult.status === 'ALREADY_PAID') {
      releaseSpend(reservationId);
      reservationId = null;
    }

    // ── Resolve preimage ──
    // Option A (primary): preImage returned inline via settlementVia in the mutation response.
    // Option B (fallback): second query to transactions, match by paymentHash.
    //   Covers edge cases where inline resolution is unavailable (race condition, network issue).
    // Option C (last resort): SHA-256(invoice) placeholder — works with non-strict servers only.
    preimage = payResult.transaction?.settlementVia?.preImage ?? null;
    const paymentHash = payResult.transaction?.initiationVia?.paymentHash ?? null;
    paidPaymentHash = paymentHash;

    if (preimage) {
      console.error('Preimage received inline from payment response.');
    } else if (paymentHash) {
      console.error(`Fetching preimage via transactions query (paymentHash: ${paymentHash.slice(0, 16)}…)`);
      // Poll for up to ~5 seconds (5 attempts × 1 s delay) — the Blink API may
      // not index the settlement immediately after the mutation returns SUCCESS.
      for (let attempt = 1; attempt <= 5 && !preimage; attempt++) {
        preimage = await fetchPreimageByPaymentHash(paymentHash, {
          apiKey,
          apiUrl,
          walletId: wallet.id,
        });
        if (!preimage && attempt < 5) {
          console.error(`Preimage not yet indexed (attempt ${attempt}/5), retrying in 1s...`);
          await new Promise((r) => setTimeout(r, 1000));
        }
      }
      if (preimage) {
        console.error('Preimage resolved via transactions query.');
      } else {
        console.error('Warning: preimage not available after 5 attempts. Using placeholder (non-strict servers only).');
        preimage = derivePreimageFromInvoice(challenge.invoice);
        preimagePlaceholder = true;
      }
    } else {
      console.error('Warning: paymentHash not returned by API. Using preimage placeholder (non-strict servers only).');
      preimage = derivePreimageFromInvoice(challenge.invoice);
      preimagePlaceholder = true;
    }
  }

  // ── Save token to store ──
  // ClawHub 3.0.1 scan: a placeholder preimage is fabricated, not a proof of
  // payment — never cache it as a reusable paid token.
  let tokenStored = false;
  if (useStore && preimagePlaceholder) {
    console.error('Warning: the preimage is a placeholder, so the token is NOT cached (it is not a proof of payment).');
  } else if (useStore) {
    try {
      saveToken(storeKey, {
        macaroon,
        preimage,
        invoice: challenge.invoice,
        satoshis: satoshis ?? null,
        invoiceMsats: charge.msats,
        budgetSats,
        backend: sparkBackend ? 'spark' : 'custodial',
      });
      tokenStored = true;
      console.error(`Token cached for ${storeKey}.`);
    } catch (err) {
      console.error(`Warning: could not save token to store: ${err.message}`);
    }
  }

  // ── Record spend in budget log ──
  // Finalize the reservation (funds moved) — or, when no budget is configured
  // (nothing was reserved), record the spend directly so the log stays
  // complete for unconfigured users too. finalizeOrRecord restores the entry
  // if the reservation was erased externally (e.g. by `budget reset`).
  // ALREADY_PAID is excluded above (nothing moved this invocation).
  if (budgetSats !== null && paymentStatus === 'SUCCESS') {
    settleSpend({ reservationId, sats: budgetSats, command: 'l402-pay', domain });
  }

  // ── Retry request with proof of payment ──
  console.error('Retrying request with L402 authorization...');
  const authHeader = `L402 ${macaroon}:${preimage}`;

  // FT7 (v3.0.2): money has moved by now — a transport failure must never
  // leave stdout empty (it used to escape as a bare "Error: terminated").
  let retryRes;
  let retryBody;
  try {
    retryRes = await fetchWithTimeout(challengeUrl, credentialedRequest(authHeader), 15_000, allowHosts);
    retryBody = await retryRes.text();
  } catch (err) {
    // The payment has SETTLED: every failure — transport or URL policy (a
    // credentialed response redirecting to a forbidden host, PR #25 review) —
    // must be reported as JSON, never as a stderr-only error.
    const notKept = args.noStore
      ? 'the token was not kept (--no-store)'
      : preimagePlaceholder
        ? 'the token was not kept (placeholder preimage)'
        : 'the token could not be cached';
    const output = {
      event: 'l402_paid_retry_failed',
      url: args.url,
      canonicalUrl: canonicalUrl !== args.url ? canonicalUrl : undefined,
      challengeUrl: challengeUrlField,
      format: challenge.format,
      backend: sparkBackend ? 'spark' : 'custodial',
      paymentStatus,
      ...(sparkBackend ? {} : { walletId: wallet.id, walletCurrency: args.walletCurrency }),
      satoshis: satoshis ?? null,
      invoiceMsats: charge.msats,
      budgetSats,
      paymentHash: paidPaymentHash ?? invoicePaymentHash(challenge.invoice),
      tokenStored,
      tokenReused: false,
      ...(preimagePlaceholder ? { preimagePlaceholder: true } : {}),
      feeProbe: feeProbeResult
        ? { estimatedFeeSats: feeProbeResult.estimatedFeeSats, error: feeProbeResult.error }
        : undefined,
      error: describeFetchError(err),
      ...(err && err.code ? { errorCode: err.code } : {}),
      message: tokenStored
        ? `The payment settled, but the request carrying the L402 credential failed. The token is cached for ${storeKey}: ` +
          're-run the same command to retry with it (no new payment).'
        : `The payment settled, but the request carrying the L402 credential failed, and ${notKept} — ` +
          're-running pays again.',
    };
    console.log(JSON.stringify(output, null, 2));
    process.exitCode = 1; // see l402_reuse_failed: entry points flush stdout first
    return;
  }

  let retryData;
  try {
    retryData = JSON.parse(retryBody);
  } catch {
    retryData = retryBody;
  }

  const output = {
    event: 'l402_paid',
    url: args.url,
    canonicalUrl: canonicalUrl !== args.url ? canonicalUrl : undefined,
    challengeUrl: challengeUrlField,
    format: challenge.format,
    backend: sparkBackend ? 'spark' : 'custodial',
    paymentStatus,
    ...(sparkBackend ? {} : { walletId: wallet.id, walletCurrency: args.walletCurrency }),
    ...(preimagePlaceholder ? { preimagePlaceholder: true } : {}),
    satoshis: satoshis ?? null,
    invoiceMsats: charge.msats,
    budgetSats,
    tokenReused: false,
    feeProbe: feeProbeResult
      ? { estimatedFeeSats: feeProbeResult.estimatedFeeSats, error: feeProbeResult.error }
      : undefined,
    retryStatus: retryRes.status,
    data: retryData,
  };

  console.log(JSON.stringify(output, null, 2));

  if (retryRes.status !== 200) {
    console.error(`Warning: retry returned status ${retryRes.status} (expected 200).`);
    // Not process.exit(): it can truncate piped stdout; entry points drain, then exit (PR #25).
    process.exitCode = 1;
    return;
  }
}

/**
 * Best-effort payment hash of a BOLT-11 invoice (checksum-verified decode), so
 * a post-payment failure can always name the payment. Null when undecodable.
 *
 * @param {string} invoice
 * @returns {string|null}
 */
function invoicePaymentHash(invoice) {
  try {
    return decodeBolt11(invoice, { nowSeconds: 0 }).paymentHash || null;
  } catch {
    return null;
  }
}

/** A transport error with its cause (undici reports e.g. "terminated (Decompression failed)"). */
function describeFetchError(err) {
  const msg = (err && err.message) || String(err);
  const cause = err && err.cause && err.cause.message;
  return cause && !msg.includes(cause) ? `${msg} (${cause})` : msg;
}

/**
 * Derive a placeholder preimage, SHA-256(invoice), when the API does not
 * return the real one. It is sent in the paid request (a non-strict L402
 * server may accept it) but is NEVER cached: it is not a proof of payment
 * (ClawHub 3.0.1 scan), so access may still fail and the token is not kept.
 *
 * @param {string} invoice  BOLT-11 payment request.
 * @returns {string}  64-char hex string.
 */
function derivePreimageFromInvoice(invoice) {
  // NOT a real preimage: a server that checks sha256(preimage) == payment
  // hash rejects it.
  const crypto = require('node:crypto');
  return crypto.createHash('sha256').update(invoice).digest('hex');
}

if (require.main === module) {
  main()
    .then(async () => {
      // The Breez SDK (spark backend) keeps event-loop handles open after
      // disconnect; force a clean exit so direct invocation returns promptly.
      // Drain stdout first — process.exit() can truncate a pending write when
      // stdout is a pipe, and the JSON result is this command's whole product.
      await new Promise((resolve) => {
        if (process.stdout.writableLength === 0) return resolve();
        process.stdout.write('', () => resolve());
      });
      process.exit(process.exitCode || 0);
    })
    .catch((e) => {
      console.error('Error:', e.message);
      process.exit(1);
    });
}

module.exports = {
  main,
  resolveCanonicalUrl,
  resolveL402Challenge,
  derivePreimageFromInvoice,
  fetchPreimageByPaymentHash,
  runFeeProbe,
  ARG_OPTIONS: L402_PAY_OPTIONS,
};
