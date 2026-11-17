/**
 * Blink Claw Skill — Shared Client Module
 *
 * Centralises API key resolution, GraphQL requests, WebSocket helpers,
 * invoice normalisation, wallet resolution, and common arg-parsing logic
 * used by every script in blink/scripts/.
 *
 * Zero external dependencies — Node.js 22+ built-ins only.
 */

// ── Constants ────────────────────────────────────────────────────────────────

const DEFAULT_API_URL = 'https://api.blink.sv/graphql';
const DEFAULT_TIMEOUT_MS = 15_000;
const MUTATION_TIMEOUT_MS = 30_000;

// ── Config helpers ───────────────────────────────────────────────────────────

/**
 * Resolve the Blink API key from the environment.
 *
 * Only `process.env.BLINK_API_KEY` is read — the key is sent exclusively as
 * the X-API-KEY header to api.blink.sv (or a user-configured BLINK_API_URL).
 * No filesystem fallback: shell rc files are never read.
 *
 * @param {object}  [opts]
 * @param {boolean} [opts.required=true]  Throw if the key is not found.
 * @returns {string|null}
 */
function getApiKey({ required = true } = {}) {
  const key = process.env.BLINK_API_KEY;
  if (!key && required) {
    throw new Error(
      'BLINK_API_KEY not found. Set it as an environment variable, e.g.:\n' + '  export BLINK_API_KEY="blink_..."',
    );
  }
  return key || null;
}

/**
 * Validate a user-supplied API/WS endpoint override (security-audit fix).
 *
 * A poisoned BLINK_API_URL would send the X-API-KEY to an arbitrary host, so
 * overrides must be https/wss (plaintext tolerated only for literal local
 * hosts — regtest/dev), and hosts outside the Blink family require the
 * explicit BLINK_ALLOW_CUSTOM_AUTH_HOST=1 opt-in. This is defence-in-depth —
 * controlling the environment already implies far worse — but the key must
 * not leak through an unvalidated URL by accident.
 *
 * @param {string} rawUrl   the env-supplied URL
 * @param {string} secureScheme   'https:' or 'wss:'
 * @param {string} insecureScheme 'http:'  or 'ws:'
 * @param {string} what     label for error messages
 * @returns {string} the validated URL
 */
function validateAuthEndpoint(rawUrl, secureScheme, insecureScheme, what) {
  let url;
  try {
    url = new URL(rawUrl);
  } catch {
    throw new Error(`${what} is not a parseable URL: ${rawUrl}`);
  }
  const host = url.hostname.toLowerCase();
  const isLocal = host === 'localhost' || host === '127.0.0.1' || host === '::1' || host === '[::1]';
  const isBlinkHost = host === 'blink.sv' || host.endsWith('.blink.sv');
  if (url.protocol !== secureScheme && !(url.protocol === insecureScheme && isLocal)) {
    throw new Error(
      `${what} must use ${secureScheme.slice(0, -1)} (plaintext ${insecureScheme.slice(0, -1)} is only allowed for localhost): ${rawUrl}`,
    );
  }
  if (!isBlinkHost && !isLocal && process.env.BLINK_ALLOW_CUSTOM_AUTH_HOST !== '1') {
    throw new Error(
      `${what} host '${host}' is outside the Blink family. Set BLINK_ALLOW_CUSTOM_AUTH_HOST=1 to explicitly trust it with your API key.`,
    );
  }
  return url.toString();
}

/**
 * Resolve the Blink GraphQL API URL.
 * @returns {string}
 */
function getApiUrl() {
  if (process.env.BLINK_API_URL) {
    return validateAuthEndpoint(process.env.BLINK_API_URL, 'https:', 'http:', 'BLINK_API_URL');
  }
  return DEFAULT_API_URL;
}

/**
 * Resolve the Blink WebSocket URL.
 * Prefers BLINK_WS_URL env override; otherwise derives from the API URL.
 * @returns {string}
 */
function getWsUrl() {
  if (process.env.BLINK_WS_URL) {
    return validateAuthEndpoint(process.env.BLINK_WS_URL, 'wss:', 'ws:', 'BLINK_WS_URL');
  }
  const apiUrl = getApiUrl();
  const url = new URL(apiUrl);
  if (url.protocol !== 'https:') {
    // Only a validated local http endpoint reaches here; the derived socket
    // mirrors it. Never auto-DOWNGRADE https -> ws (audit finding): an https
    // API host gets wss.
    url.protocol = 'ws:';
  } else {
    url.protocol = 'wss:';
  }
  if (url.hostname.startsWith('api.')) {
    url.hostname = url.hostname.replace(/^api\./, 'ws.');
  }
  return url.toString();
}

// ── HTTP / GraphQL ───────────────────────────────────────────────────────────

/**
 * Execute a GraphQL request against the Blink API.
 *
 * @param {object}  opts
 * @param {string}  opts.query          GraphQL query or mutation string.
 * @param {object}  [opts.variables={}] GraphQL variables.
 * @param {string|null} [opts.apiKey]   API key (null ⇒ unauthenticated).
 * @param {string}  [opts.apiUrl]       API endpoint URL.
 * @param {number}  [opts.timeoutMs]    Request timeout in ms (default 15 000).
 * @returns {object} The `data` property of the GraphQL response.
 */
async function graphqlRequest({
  query,
  variables = {},
  apiKey = null,
  apiUrl = DEFAULT_API_URL,
  timeoutMs = DEFAULT_TIMEOUT_MS,
} = {}) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const headers = { 'Content-Type': 'application/json' };
    if (apiKey) headers['X-API-KEY'] = apiKey;

    const res = await fetch(apiUrl, {
      method: 'POST',
      headers,
      body: JSON.stringify({ query, variables }),
      signal: controller.signal,
    });

    if (!res.ok) {
      // Tagged so callers can tell a server/transport failure apart from the
      // API successfully answering "no". Message format is unchanged.
      const e = new Error(`HTTP ${res.status}: ${await res.text()}`);
      e.code = 'HTTP_ERROR';
      e.status = res.status;
      throw e;
    }

    const json = await res.json();
    if (json.errors && json.errors.length > 0) {
      const e = new Error(`GraphQL error: ${json.errors.map((x) => x.message).join(', ')}`);
      e.code = 'GRAPHQL_ERROR';
      e.graphQLErrors = json.errors;
      throw e;
    }
    return json.data;
  } finally {
    clearTimeout(timer);
  }
}

// ── Invoice helpers ──────────────────────────────────────────────────────────

/**
 * Trim whitespace and strip a leading `lightning:` URI prefix (case-insensitive).
 * @param {string} input  Raw invoice / payment-request string.
 * @returns {string}
 */
function normalizeInvoice(input) {
  const trimmed = input.trim();
  if (trimmed.toLowerCase().startsWith('lightning:')) {
    return trimmed.slice('lightning:'.length);
  }
  return trimmed;
}

/**
 * Emit a warning to stderr if the invoice doesn't look like a valid BOLT-11
 * payment request. Checks are case-insensitive.
 * @param {string} invoice  The (already-normalised) invoice string.
 */
function warnIfNotBolt11(invoice) {
  const lower = invoice.toLowerCase();
  if (!lower.startsWith('lnbc') && !lower.startsWith('lntbs') && !lower.startsWith('lntb')) {
    console.error('Warning: invoice does not start with lnbc/lntbs/lntb \u2014 may not be a valid BOLT-11 invoice.');
  }
}

// ── Wallet helpers ───────────────────────────────────────────────────────────

const WALLET_QUERY = `
  query Me {
    me {
      defaultAccount {
        wallets {
          id
          walletCurrency
          balance
          pendingIncomingBalance
        }
      }
    }
  }
`;

/**
 * Resolve a wallet by currency.
 *
 * @param {object}  opts
 * @param {string}  opts.apiKey
 * @param {string}  opts.apiUrl
 * @param {string}  opts.currency       "BTC" or "USD".
 * @param {number}  [opts.timeoutMs]
 * @returns {{ id: string, walletCurrency: string, balance: number, pendingIncomingBalance: number }}
 */
async function getWallet({ apiKey, apiUrl, currency, timeoutMs }) {
  const data = await graphqlRequest({ query: WALLET_QUERY, apiKey, apiUrl, timeoutMs });
  if (!data.me) throw new Error('Authentication failed. Check your BLINK_API_KEY.');
  const wallet = data.me.defaultAccount.wallets.find((w) => w.walletCurrency === currency);
  if (!wallet) throw new Error(`No ${currency} wallet found on this account.`);
  return wallet;
}

/**
 * Resolve all wallets on the account.
 *
 * @param {object}  opts
 * @param {string}  opts.apiKey
 * @param {string}  opts.apiUrl
 * @param {number}  [opts.timeoutMs]
 * @returns {Array}
 */
async function getAllWallets({ apiKey, apiUrl, timeoutMs }) {
  const data = await graphqlRequest({ query: WALLET_QUERY, apiKey, apiUrl, timeoutMs });
  if (!data.me) throw new Error('Authentication failed. Check your BLINK_API_KEY.');
  return data.me.defaultAccount.wallets;
}

// ── Receiver resolution (custodial vs non-custodial) ─────────────────────────
//
// Blink serves LNURL-pay on `blink.sv` for BOTH custodial and non-custodial
// (Spark) accounts; the blink-lnurl-server routes each recipient to the right
// provider internally. The account TYPE is not encoded in the domain, so the
// only way to classify an identifier from the outside is:
//
//   1. Custodial probe: query `accountDefaultWallet(username)`.
//        Returns a wallet id  => the identifier is a CUSTODIAL Blink account.
//   2. LNURL fallback: fetch `.well-known/lnurlp/{username}` on the same host.
//        Returns a valid payRequest => the identifier is a NON-CUSTODIAL
//        (Spark) account served via the LNURL server.
//   3. Neither => the address does not exist.
//
// This mirrors the rule blink-terminal shipped (PR #37). It is the crux of the
// "does this address exist / which mechanism do I use" question and is exactly
// where a first-class Blink GraphQL resolution mutation could replace this
// two-step client dance (see the research findings / issue #940).

const DEFAULT_LN_ADDRESS_DOMAIN = 'blink.sv';

// Two distinct trust sets, kept deliberately separate:
//
// ALLOWED_LN_ADDRESS_DOMAINS — the ADDRESS DOMAIN the user supplies in
//   `user@domain`. This is the narrow SSRF surface: a user-controlled string
//   that becomes an outbound request. Only `blink.sv` is a valid Blink
//   Lightning-address domain, so nothing else is ever probed.
//
// ALLOWED_LNURL_SERVICE_HOSTS — the hosts a SERVER-SUPPLIED URL may point at:
//   the LNURL-pay callback, the LUD-21 verify URL, and any redirect target.
//   Blink serves those from a dedicated LNURL service host (lnurl.blink.sv),
//   distinct from the address domain. Confirmed against live production
//   topology: https://blink.sv/.well-known/lnurlp/<user> returns a callback on
//   https://lnurl.blink.sv/... — a blink.sv-only allowlist rejects it and
//   breaks the credential-free receive path. Arbitrary user-supplied domains
//   and private-address redirects stay blocked regardless.
const ALLOWED_LN_ADDRESS_DOMAINS = new Set(['blink.sv']);
const ALLOWED_LNURL_SERVICE_HOSTS = new Set(['blink.sv', 'lnurl.blink.sv']);

const ACCOUNT_DEFAULT_WALLET_QUERY = `
  query AccountDefaultWallet($username: Username!) {
    accountDefaultWallet(username: $username) {
      id
      walletCurrency
    }
  }
`;

// A GraphQL error that genuinely means "there is no such custodial account",
// as opposed to one that means "the lookup did not happen". Only the former may
// fall through to the LNURL branch.
//
// These patterns are deliberately ANCHORED TO THE ACCOUNT. A bare /not found/
// would also match "Cannot query field \"accountDefaultWallet\" ... not found"
// (schema drift) and a gateway's "404 Not Found" — both of which mean the
// lookup failed, and both of which would then misreport EVERY custodial account
// as non-custodial. A bare /invalid username/ likewise matches "Invalid
// username or password", which is an auth failure, not an absent account.
const NOT_FOUND_PATTERNS = [
  /account\s+does\s+not\s+exist/i,
  /(account|user|username)\s+(was\s+)?not\s+found/i,
  /no\s+account\s+(found\s+)?for/i,
  /(username|user)\s+does\s+not\s+exist/i,
  /unknown\s+(user|username|account)/i,
];

// Structured codes are preferred over prose when the server supplies them.
const NOT_FOUND_CODES = new Set(['ACCOUNT_NOT_FOUND', 'USERNAME_NOT_FOUND', 'NOT_FOUND', 'USER_NOT_FOUND']);

/**
 * Does this GraphQL error mean the account is absent, rather than the lookup
 * having failed?
 *
 * Only ever consulted for `GRAPHQL_ERROR`, so transport, timeout and HTTP
 * failures can never reach these patterns at all.
 *
 * @param {Error} err
 * @returns {boolean}
 */
function isAccountNotFoundError(err) {
  if (!err || err.code !== 'GRAPHQL_ERROR') return false;
  const errors = err.graphQLErrors || [];

  // Prefer an explicit machine-readable code when one is present.
  for (const e of errors) {
    const code = e && ((e.extensions && e.extensions.code) || e.code);
    if (code && NOT_FOUND_CODES.has(String(code).toUpperCase())) return true;
  }

  const messages = errors.map((e) => String(e && e.message)).join(' ') || String(err.message);
  return NOT_FOUND_PATTERNS.some((re) => re.test(messages));
}

/**
 * Does this GraphQL error mean the account exists but is INACTIVE?
 *
 * This is distinct from both "absent" and "lookup failed". An inactive
 * custodial account cannot be paid through the custodial API — but Blink still
 * serves its Lightning address publicly over LNURL, so the correct next step
 * is the same as for a genuinely absent custodial account: fall through to the
 * LNURL branch. Treating it as a hard probe failure would break the
 * credential-free receive path for exactly the accounts that need it
 * (reproduced live: `Account is inactive` for a username whose
 * `.well-known/lnurlp/<user>` returns a valid payRequest).
 *
 * @param {Error} err
 * @returns {boolean}
 */
function isAccountInactiveError(err) {
  if (!err || err.code !== 'GRAPHQL_ERROR') return false;
  const messages = (err.graphQLErrors || []).map((e) => String(e && e.message)).join(' ') || String(err.message);
  return /account\s+is\s+inactive/i.test(messages);
}

/**
 * Look up a custodial account's default BTC wallet by username.
 *
 * Returns null ONLY when the API successfully answered that no such custodial
 * account exists. Every other failure — transport, timeout, authentication,
 * 5xx, an unrecognised GraphQL error — is rethrown.
 *
 * This distinction is load-bearing. Swallowing all errors here meant a
 * transient 503 on the custodial probe made a custodial account fall through to
 * the LNURL branch and get reported as `{ type: "lnaddress", walletId: null }`
 * — a confident wrong answer about someone's account type, produced by an
 * outage. Failing loudly is correct: the caller can retry, but it cannot detect
 * a misclassification.
 *
 * @param {object} opts
 * @param {string} opts.username
 * @param {string} [opts.apiKey]
 * @param {string} [opts.apiUrl]
 * @param {number} [opts.timeoutMs]
 * @returns {Promise<{ id: string, walletCurrency: string }|null>}
 * @throws {Error} If the lookup itself could not be completed.
 */
async function getCustodialDefaultWallet({ username, apiKey = null, apiUrl, timeoutMs }) {
  try {
    const data = await graphqlRequest({
      query: ACCOUNT_DEFAULT_WALLET_QUERY,
      variables: { username },
      apiKey,
      apiUrl: apiUrl || DEFAULT_API_URL,
      timeoutMs,
    });
    return (data && data.accountDefaultWallet) || null;
  } catch (err) {
    // Absent custodial account: let the LNURL fallback decide.
    if (isAccountNotFoundError(err)) return null;
    // An INACTIVE custodial account is also not payable through the custodial
    // API — but "Account is inactive" can describe the CALLER's own (auth)
    // account when an apiKey was supplied, not the receiver. Only the
    // credential-free path can safely read it as "receiver is not custodial";
    // when authenticated, it is ambiguous and must fail closed.
    if (!apiKey && isAccountInactiveError(err)) return null;
    const e = new Error(
      `Could not determine whether '${username}' is a custodial Blink account: ${err.message}. ` +
        'Refusing to guess the account type from a failed lookup.',
    );
    e.code = 'CUSTODIAL_PROBE_FAILED';
    e.cause = err;
    throw e;
  }
}

/**
 * Resolve a receiver identifier to its account type and how to receive to it.
 *
 * @param {string} identifier   Bare username or `user@blink.sv`.
 * @param {object} [opts]
 * @param {string} [opts.apiKey]        Optional — improves custodial probe.
 * @param {string} [opts.apiUrl]
 * @param {string} [opts.defaultDomain] Defaults to blink.sv.
 * @param {number} [opts.timeoutMs]
 * @returns {Promise<{ type: 'custodial'|'lnaddress', username: string, domain: string,
 *                     lightningAddress: string, walletId: string|null }>}
 */
async function resolveReceiver(identifier, opts = {}) {
  // Lazy require to keep _lnurl.js optional for callers that never resolve.
  const { parseLightningAddress, fetchLnurlPayMetadata } = require('./_lnurl');

  const parsed = parseLightningAddress(identifier);
  const domain = parsed.domain || opts.defaultDomain || DEFAULT_LN_ADDRESS_DOMAIN;

  // SSRF guard: reject any explicit non-Blink domain before any network call.
  if (!ALLOWED_LN_ADDRESS_DOMAINS.has(domain)) {
    throw new Error(
      `Refusing to resolve non-Blink domain '${domain}'. Only ${[...ALLOWED_LN_ADDRESS_DOMAINS].join(', ')} is allowed.`,
    );
  }

  const lightningAddress = `${parsed.username}@${domain}`;

  // 1. Custodial probe.
  const custodialWallet = await getCustodialDefaultWallet({
    username: parsed.username,
    apiKey: opts.apiKey || null,
    apiUrl: opts.apiUrl,
    timeoutMs: opts.timeoutMs,
  });
  if (custodialWallet && custodialWallet.id) {
    return {
      type: 'custodial',
      username: parsed.username,
      domain,
      lightningAddress,
      walletId: custodialWallet.id,
    };
  }

  // 2. LNURL fallback (non-custodial / Spark). The metadata is fetched from the
  // address domain, but a redirect may land on the LNURL service host, so the
  // server-facing allowlist is used here.
  try {
    await fetchLnurlPayMetadata(parsed.username, domain, {
      timeoutMs: opts.timeoutMs,
      allowedHosts: ALLOWED_LNURL_SERVICE_HOSTS,
    });
    return {
      type: 'lnaddress',
      username: parsed.username,
      domain,
      lightningAddress,
      walletId: null,
    };
  } catch (err) {
    // Only an unambiguous not-found becomes RECEIVER_NOT_FOUND. A service or
    // protocol failure (LNURL_SERVICE_ERROR, HTTP 5xx, a timeout) propagates as
    // a retryable failure — it must not be relayed as a confident identity
    // answer, the same principle as the custodial probe above.
    if (err.code === 'LNURL_NOT_FOUND') {
      const e = new Error(`'${lightningAddress}' does not seem to be a Blink address that exists.`);
      e.code = 'RECEIVER_NOT_FOUND';
      throw e;
    }
    if (err.code === 'LNURL_SERVICE_ERROR') {
      const e = new Error(
        `Could not confirm whether '${lightningAddress}' exists: the LNURL server reported a ` +
          `temporary failure (${err.message}). Retry rather than treat this as a missing address.`,
      );
      e.code = 'LNURL_SERVICE_ERROR';
      e.cause = err;
      throw e;
    }
    throw err;
  }
}

// ── Currency conversion ──────────────────────────────────────────────────────

const CONVERSION_QUERY = `
  query CurrencyConversion($amount: Float!, $currency: DisplayCurrency!) {
    currencyConversionEstimation(amount: $amount, currency: $currency) {
      btcSatAmount
      usdCentAmount
    }
  }
`;

/**
 * Estimate the USD value of a satoshi amount.
 * Non-fatal: returns null on failure so callers can treat it as best-effort.
 *
 * @param {object}  opts
 * @param {number}  opts.sats
 * @param {string}  opts.apiKey
 * @param {string}  opts.apiUrl
 * @param {number}  [opts.timeoutMs]
 * @returns {number|null}  USD value rounded to 2 decimals, or null.
 */
async function estimateSatsToUsd({ sats, apiKey, apiUrl, timeoutMs }) {
  if (sats === 0) return 0;
  try {
    const data = await graphqlRequest({
      query: CONVERSION_QUERY,
      variables: { amount: 1.0, currency: 'USD' },
      apiKey,
      apiUrl,
      timeoutMs,
    });
    const est = data.currencyConversionEstimation;
    if (!est || !est.btcSatAmount || est.btcSatAmount === 0) return null;
    const usdPerSat = 1.0 / est.btcSatAmount;
    return Math.round(sats * usdPerSat * 100) / 100;
  } catch {
    return null; // non-fatal — USD estimate is best-effort
  }
}

// ── Formatting ───────────────────────────────────────────────────────────────

/**
 * Convert a Blink API base/offset pair to a decimal number.
 *
 * The Blink API represents prices as { base, offset } where the actual value
 * is `base * 10^offset`.  For example, { base: 6456903063948, offset: -12 }
 * represents 6.456903… (a BTC-per-sat price, unitless).
 *
 * @param {number} base
 * @param {number} offset
 * @returns {number}
 */
function decimalFromBaseOffset(base, offset) {
  return base * Math.pow(10, offset);
}

/**
 * Human-readable wallet balance string.
 * @param {{ walletCurrency: string, balance: number }} wallet
 * @returns {string}
 */
function formatBalance(wallet) {
  if (wallet.walletCurrency === 'USD') {
    return `$${(wallet.balance / 100).toFixed(2)} (${wallet.balance} cents)`;
  }
  return `${wallet.balance} sats`;
}

/**
 * Format a cent amount as USD.
 * @param {number} cents
 * @returns {string}
 */
function formatUsdCents(cents) {
  return `$${(cents / 100).toFixed(2)}`;
}

// ── Arg parsing helpers ──────────────────────────────────────────────────────

/**
 * Strictly validate a money-moving script's argv and return it in canonical
 * split form (`--opt value`), for that script's own validation loop.
 *
 * PR #26 review: the hand-rolled parsers treated anything they did not
 * recognize as an ignored positional, so a safety flag spelled slightly
 * differently was silently dropped — `--max-amount=500` or a valueless
 * `--max-amount` lost the ceiling, and `--dry-run=true` or a typo like
 * `--dryrun` lost the DRY RUN, making the payment real. This runs the same
 * engine as the `blink` CLI (node:util parseArgs, strict): unknown options, a
 * missing value, and a value on a boolean flag all THROW (code ARG_INVALID)
 * before any credential, network, or SDK call; `--opt=value` is accepted.
 *
 * Opts: `keepTerminator` re-emits an explicit `--` so a script that takes free
 * text (memo words) can treat everything after it literally — a memo word
 * like `-50%` must come after `--`, exactly as at the `blink` CLI.
 * `positionalsFirst` puts all positionals before the options, for a loop that
 * reads positionals by fixed index (the swap scripts).
 *
 * @param {string[]} argv
 * @param {Record<string, {type: 'string'|'boolean', multiple?: boolean}>} options
 * `positionals: [min, max]` enforces the positional arity (PR #27 review: an
 * option typo WITHOUT dashes, `l402-store clear expird`, was an ignored extra
 * positional — and cleared every token). Without `keepTerminator`, a `--` is
 * REFUSED: words after it would otherwise be re-read as live options by the
 * script's own loop (`-- --network mainnet`).
 *
 * @param {{ keepTerminator?: boolean, positionalsFirst?: boolean, positionals?: [number, number] }} [opts]
 * @returns {string[]}  canonical argv: `--name` (+ value for strings) and positionals, in order
 */
function strictArgv(argv, options, { keepTerminator = false, positionalsFirst = false, positionals: arity } = {}) {
  let tokens;
  try {
    ({ tokens } = require('node:util').parseArgs({
      args: argv,
      options,
      allowPositionals: true,
      strict: true,
      tokens: true,
    }));
  } catch (err) {
    throw argInvalid(String(err.message).replace(/\. To specify a positional argument[\s\S]*$/, ''));
  }
  assertNoConflictingRepeats(tokens, options);
  const opts = [];
  const positionals = [];
  const out = [];
  const allPositionals = tokens.filter((t) => t.kind === 'positional').map((t) => t.value);
  if (!keepTerminator && tokens.some((t) => t.kind === 'option-terminator')) {
    throw argInvalid("'--' is only accepted by commands that take free text (a memo or description)");
  }
  if (arity) assertPositionalCount(allPositionals, arity[0], arity[1]);
  for (const t of tokens) {
    if (t.kind === 'option') {
      const o = [`--${t.name}`];
      if (options[t.name].type === 'string') o.push(t.value);
      (positionalsFirst ? opts : out).push(...o);
    } else if (t.kind === 'option-terminator') {
      if (keepTerminator) out.push('--');
    } else if (t.kind === 'positional') {
      (positionalsFirst ? positionals : out).push(t.value);
    }
  }
  return positionalsFirst ? [...positionals, ...opts] : out;
}

/**
 * Refuse a single-value option given twice with DIFFERENT values (v3.0.5,
 * FT10): parseArgs silently keeps the last one, so
 * `spark-lnaddress delete --network regtest --network mainnet` targeted
 * mainnet. An identical repeat is harmless and allowed; `multiple` options
 * are exempt. Booleans compare their polarity (`--store` vs `--no-store`,
 * with allowNegative).
 *
 * @param {Array<{kind: string, name?: string, rawName?: string, value?: string}>} tokens  parseArgs tokens
 * @param {Record<string, {type: string, multiple?: boolean}>} options
 */
function assertNoConflictingRepeats(tokens, options) {
  const seen = new Map();
  for (const t of tokens) {
    if (t.kind !== 'option' || !Object.hasOwn(options, t.name) || options[t.name].multiple) continue;
    const isString = options[t.name].type === 'string';
    const value = isString ? t.value : !String(t.rawName).startsWith('--no-');
    if (!seen.has(t.name)) {
      seen.set(t.name, { value, raw: t.rawName });
    } else if (seen.get(t.name).value !== value) {
      const first = seen.get(t.name);
      // Name the option only — NEVER the values: a --token / --macaroon /
      // --preimage is reusable bearer material (PR #28 review).
      throw argInvalid(
        isString
          ? `Conflicting values for --${t.name}: give it once`
          : `Conflicting options ${first.raw} and ${t.rawName}: give one`,
      );
    }
  }
}

/**
 * Strict replacement for node:util.parseArgs, for scripts that read `values`
 * directly (the L402 producer/directory scripts). Same `{ values, positionals }`
 * result, plus what strictArgv guarantees: conflicting repeats refused,
 * positional arity enforced (skipped for `--help`), ARG_INVALID errors that
 * never echo argument values. PR #28 review: these scripts called parseArgs
 * themselves, so `--resource /safe --resource /admin` kept the last value.
 *
 * @param {string[]} argv
 * @param {Record<string, object>} options  parseArgs option config
 * @param {{ positionals?: [number, number] }} [opts]  default [0, 0]
 * @returns {{ values: Record<string, unknown>, positionals: string[] }}
 */
function strictParseArgs(argv, options, { positionals: arity = [0, 0] } = {}) {
  let parsed;
  try {
    parsed = require('node:util').parseArgs({
      args: argv,
      options,
      allowPositionals: true, // counted below, so no error ever quotes a positional
      strict: true,
      tokens: true,
    });
  } catch (err) {
    throw argInvalid(String(err.message).replace(/\. To specify a positional argument[\s\S]*$/, ''));
  }
  assertNoConflictingRepeats(parsed.tokens, options);
  if (!parsed.values.help) assertPositionalCount(parsed.positionals, arity[0], arity[1]);
  return { values: parsed.values, positionals: parsed.positionals };
}

function argInvalid(reason) {
  const e = new Error(`${reason}. Unknown or malformed options are refused before anything is sent.`);
  e.code = 'ARG_INVALID';
  return e;
}

/**
 * Enforce a positional arity: throws ARG_INVALID naming the unexpected words.
 * Exported for scripts whose arity depends on a subcommand.
 *
 * @param {string[]} list
 * @param {number} min
 * @param {number} max  Infinity for free text
 */
function assertPositionalCount(list, min, max) {
  if (list.length >= min && list.length <= max) return;
  const range =
    min === max ? `${min}` : max === Infinity ? `at least ${min}` : min === 0 ? `at most ${max}` : `${min}–${max}`;
  // Position only, never the words (PR #28 review): a seed or token pasted
  // by mistake as positionals must not be printed back.
  const from = max + 1;
  const extra =
    list.length > max
      ? ` (unexpected extra argument at position${list.length > from ? `s ${from}–${list.length}` : ` ${from}`})`
      : '';
  throw argInvalid(`Expected ${range} positional argument(s), got ${list.length}${extra}`);
}

const WALLET_ARG_OPTIONS = {
  wallet: { type: 'string' },
  'dry-run': { type: 'boolean' },
  force: { type: 'boolean' },
  'max-amount': { type: 'string' },
};

/**
 * Parse a --wallet BTC|USD flag from an argv array.
 * Also recognises payment safety flags: --dry-run, --force, --max-amount <sats>.
 *
 * Returns the chosen currency, safety flags, and the remaining positional args
 * (with all recognised flags stripped out). Parsing is STRICT (strictArgv):
 * an unknown or malformed option exits 1 before anything is sent.
 *
 * @param {string[]} argv  Typically `process.argv.slice(2)`.
 * @returns {{ walletCurrency: string, dryRun: boolean, force: boolean, maxAmount: number|null, remaining: string[] }}
 */
function parseWalletArg(argv, { maxPositionals = Infinity } = {}) {
  try {
    argv = strictArgv(argv, WALLET_ARG_OPTIONS, { positionals: [0, maxPositionals] });
  } catch (err) {
    console.error(`Error: ${err.message}`);
    process.exit(1);
  }
  let walletCurrency = 'BTC';
  let dryRun = false;
  let force = false;
  let maxAmount = null;
  const remaining = [];
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--wallet' && i + 1 < argv.length) {
      const val = argv[i + 1].toUpperCase();
      if (val !== 'BTC' && val !== 'USD') {
        console.error('Error: --wallet must be BTC or USD');
        process.exit(1);
      }
      walletCurrency = val;
      i++; // skip value
    } else if (argv[i] === '--dry-run') {
      dryRun = true;
    } else if (argv[i] === '--force') {
      force = true;
    } else if (argv[i] === '--max-amount' && i + 1 < argv.length) {
      const n = parseInt(argv[i + 1], 10);
      if (isNaN(n) || n <= 0) {
        console.error('Error: --max-amount must be a positive integer (sats)');
        process.exit(1);
      }
      maxAmount = n;
      i++; // skip value
    } else {
      remaining.push(argv[i]);
    }
  }
  return { walletCurrency, dryRun, force, maxAmount, remaining };
}

// ── WebSocket helpers ────────────────────────────────────────────────────────

/**
 * Ensure WebSocket is available (built into Node 22+).
 * @returns {typeof WebSocket}
 */
function requireWebSocket() {
  if (typeof WebSocket !== 'function') {
    const major = parseInt(process.versions.node.split('.')[0], 10);
    if (major >= 22) {
      throw new Error('WebSocket unavailable despite Node 22+. This is unexpected — check your Node.js build.');
    }
    throw new Error(`WebSocket requires Node.js 22+ (native). Current version: ${process.versions.node}`);
  }
  return WebSocket;
}

/**
 * Open a WebSocket subscription to watch an invoice's payment status.
 * Calls `onResult(resultObj, exitCode)` when the subscription resolves.
 *
 * @param {object}  opts
 * @param {string}  opts.paymentRequest   BOLT-11 invoice string.
 * @param {string}  opts.apiKey           Blink API key.
 * @param {string}  opts.wsUrl            WebSocket endpoint URL.
 * @param {number}  opts.timeoutSeconds   Timeout in seconds (0 = no timeout).
 * @param {(result: object, exitCode: number) => void} opts.onResult  Callback.
 */
function subscribeToInvoice({ paymentRequest, apiKey, wsUrl, timeoutSeconds, onResult }) {
  const WebSocketImpl = requireWebSocket();

  let done = false;
  let timeoutId = null;

  const ws = new WebSocketImpl(wsUrl, 'graphql-transport-ws');

  function finish(result, exitCode = 0) {
    if (done) return;
    done = true;
    if (timeoutId) clearTimeout(timeoutId);
    try {
      if (ws.readyState === ws.OPEN) {
        ws.send(JSON.stringify({ id: '1', type: 'complete' }));
      }
    } catch {
      // best-effort cleanup
    }
    try {
      ws.close(1000);
    } catch {
      // best-effort cleanup
    }
    onResult(result, exitCode);
  }

  if (timeoutSeconds > 0) {
    timeoutId = setTimeout(() => {
      console.error('Subscription timed out.');
      finish(
        {
          event: 'subscription_result',
          paymentRequest,
          status: 'TIMEOUT',
          isPaid: false,
          isExpired: false,
          isPending: true,
        },
        1,
      );
    }, timeoutSeconds * 1000);
  }

  ws.onopen = () => {
    ws.send(
      JSON.stringify({
        type: 'connection_init',
        payload: { 'X-API-KEY': apiKey },
      }),
    );
  };

  ws.onmessage = (event) => {
    let message;
    try {
      message = JSON.parse(event.data);
    } catch {
      console.error('Warning: received non-JSON WebSocket message');
      return;
    }

    if (message.type === 'connection_ack') {
      console.error('Subscribed \u2014 waiting for payment...');
      ws.send(
        JSON.stringify({
          id: '1',
          type: 'subscribe',
          payload: {
            query: `subscription LnInvoicePaymentStatus($input: LnInvoicePaymentStatusInput!) {
  lnInvoicePaymentStatus(input: $input) {
    status
  }
}`,
            variables: { input: { paymentRequest } },
          },
        }),
      );
      return;
    }

    if (message.type === 'ping') {
      ws.send(JSON.stringify({ type: 'pong' }));
      return;
    }

    if (message.type === 'error') {
      console.error('Subscription error:', JSON.stringify(message.payload || message));
      finish(
        {
          event: 'subscription_result',
          paymentRequest,
          status: 'ERROR',
          error: message.payload || message,
        },
        1,
      );
      return;
    }

    if (message.type === 'next') {
      const status =
        message.payload && message.payload.data && message.payload.data.lnInvoicePaymentStatus
          ? message.payload.data.lnInvoicePaymentStatus.status
          : null;
      if (!status) return;

      console.error(`Invoice status: ${status}`);
      if (status === 'PAID' || status === 'EXPIRED') {
        finish(
          {
            event: 'subscription_result',
            paymentRequest,
            status,
            isPaid: status === 'PAID',
            isExpired: status === 'EXPIRED',
            isPending: false,
          },
          0,
        );
      }
      return;
    }

    if (message.type === 'complete') {
      finish(
        {
          event: 'subscription_result',
          paymentRequest,
          status: 'COMPLETE',
          isPaid: false,
          isExpired: false,
          isPending: true,
        },
        0,
      );
    }
  };

  ws.onerror = () => {
    console.error('WebSocket error during subscription');
    finish(
      {
        event: 'subscription_result',
        paymentRequest,
        status: 'ERROR',
        error: 'WebSocket error',
      },
      1,
    );
  };

  ws.onclose = (event) => {
    if (done) return;
    console.error(`WebSocket closed: code=${event.code} reason=${event.reason || 'unknown'}`);
    finish(
      {
        event: 'subscription_result',
        paymentRequest,
        status: 'CLOSED',
        isPaid: false,
        isExpired: false,
        isPending: true,
      },
      1,
    );
  };
}

// ── Exports ──────────────────────────────────────────────────────────────────

/**
 * Exit with `code` only after buffered stdout has been flushed.
 *
 * process.exit() right after console.log() can cut a PIPED stdout mid-write
 * (PR #25 review: 8 MiB of JSON arrived as 146 KB). Commands that must exit
 * explicitly — e.g. to tear down a WebSocket subscription — call this instead,
 * and `return` right after it (the exit may happen on a later tick).
 * Synchronous when nothing is buffered, so tests that trap process.exit see
 * the code immediately.
 *
 * @param {number} code
 */
function exitAfterStdout(code) {
  if (process.stdout.writableLength === 0) {
    process.exit(code);
    return;
  }
  process.stdout.write('', () => process.exit(code));
}

module.exports = {
  strictArgv,
  strictParseArgs,
  assertNoConflictingRepeats,
  assertPositionalCount,
  WALLET_ARG_OPTIONS,
  exitAfterStdout,
  // Constants
  DEFAULT_API_URL,
  DEFAULT_TIMEOUT_MS,
  MUTATION_TIMEOUT_MS,

  // Config
  getApiKey,
  getApiUrl,
  getWsUrl,

  // HTTP
  graphqlRequest,

  // Invoice
  normalizeInvoice,
  warnIfNotBolt11,

  // Wallet
  WALLET_QUERY,
  getWallet,
  getAllWallets,

  // Receiver resolution (custodial vs non-custodial)
  DEFAULT_LN_ADDRESS_DOMAIN,
  ALLOWED_LN_ADDRESS_DOMAINS,
  ALLOWED_LNURL_SERVICE_HOSTS,
  ACCOUNT_DEFAULT_WALLET_QUERY,
  isAccountNotFoundError,
  isAccountInactiveError,
  getCustodialDefaultWallet,
  resolveReceiver,

  // Currency
  CONVERSION_QUERY,
  estimateSatsToUsd,

  // Formatting
  decimalFromBaseOffset,
  formatBalance,
  formatUsdCents,

  // Arg parsing
  parseWalletArg,

  // WebSocket
  requireWebSocket,
  subscribeToInvoice,
};
