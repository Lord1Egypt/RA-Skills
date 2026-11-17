#!/usr/bin/env node
/**
 * Blink Wallet - Create Invoice via Lightning Address (custodial OR non-custodial)
 *
 * Usage: node create_invoice_lnaddress.js <lightning_address> <amount_sats> [memo...]
 *                                         [--timeout <seconds>] [--no-verify]
 *
 * Receives a payment to ANY Blink Lightning Address (`user@blink.sv`) — whether
 * the recipient is a CUSTODIAL Blink account or a NON-CUSTODIAL (Spark) account.
 *
 * Unlike create_invoice.js (which needs the recipient's own BLINK_API_KEY and
 * calls the `lnInvoiceCreate` mutation on that account's wallet), this command
 * needs NO account credentials at all. It uses the public LNURL-pay endpoint
 * that blink.sv serves for both account types, and the blink-lnurl-server routes
 * the recipient to the correct provider internally.
 *
 * This is the ONLY receive path that works for non-custodial accounts without
 * holding the account seed.
 *
 * Output (two-phase, mirroring create_invoice.js):
 *   1. Immediately: `invoice_created` JSON (paymentRequest, verifyUrl, type, ...)
 *   2. When resolved: `verify_result` JSON (PAID / TIMEOUT) — only for
 *      non-custodial (lnaddress) recipients that return a LUD-21 verify URL.
 *
 * Arguments:
 *   lightning_address  - Required. `user@blink.sv` or a bare `user` (defaults to blink.sv).
 *   amount_sats        - Required. Amount in satoshis.
 *   memo...            - Optional. Remaining args joined as a comment.
 *   --timeout <s>      - Optional. Verify-poll timeout in seconds (default 300, 0 = no timeout).
 *   --no-verify        - Optional. Skip the LUD-21 verify polling; just create and exit.
 *   --qr               - Optional. Render a terminal QR (stderr) + PNG in /tmp for the
 *                        minted invoice; QR fields are merged into the invoice_created JSON.
 *
 * Environment:
 *   BLINK_API_KEY  - Optional. If present, improves the custodial-vs-non-custodial probe.
 *   BLINK_API_URL  - Optional. Override GraphQL endpoint (used for the custodial probe only).
 *
 * Dependencies: None (uses Node.js built-in fetch).
 */

const {
  getApiKey,
  getApiUrl,
  resolveReceiver,
  DEFAULT_LN_ADDRESS_DOMAIN,
  ALLOWED_LN_ADDRESS_DOMAINS,
  ALLOWED_LNURL_SERVICE_HOSTS,
  exitAfterStdout,
  strictArgv,
} = require('./_blink_client');
const { getInvoiceFromLightningAddress, verifyLnurlPayment } = require('./_lnurl');

// ── Arg parsing ──────────────────────────────────────────────────────────────

// Every option this script accepts; anything else is refused (v3.0.4 strict
// sweep). Free-text memo words go after `--` (e.g. a word like `-50%`),
// exactly as at the `blink` CLI.
const ARG_OPTIONS = { timeout: { type: 'string' }, 'no-verify': { type: 'boolean' }, qr: { type: 'boolean' } };

function parseArgs(argv) {
  argv = strictArgv(argv, ARG_OPTIONS, { keepTerminator: true, positionals: [0, Infinity] });
  let literal = false; // after `--`: every word is a positional (memo text)
  let address = null;
  let amountSats = null;
  let timeoutSeconds = 300;
  let noVerify = false;
  let qr = false;
  const memoParts = [];

  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (!literal && arg === '--') {
      literal = true;
      continue;
    }
    if (!literal && arg === '--timeout') {
      const value = argv[i + 1];
      if (!value) throw new Error('Missing value for --timeout');
      timeoutSeconds = parseInt(value, 10);
      if (isNaN(timeoutSeconds) || timeoutSeconds < 0) throw new Error('--timeout must be a non-negative integer');
      i++;
      continue;
    }
    if (!literal && arg === '--no-verify') {
      noVerify = true;
      continue;
    }
    if (!literal && arg === '--qr') {
      qr = true;
      continue;
    }
    if (address === null) {
      address = arg.trim();
      continue;
    }
    if (amountSats === null) {
      amountSats = parseInt(arg, 10);
      if (isNaN(amountSats) || amountSats <= 0) throw new Error('amount_sats must be a positive integer');
      continue;
    }
    memoParts.push(arg);
  }

  return {
    address,
    amountSats,
    timeoutSeconds,
    noVerify,
    qr,
    memo: memoParts.length > 0 ? memoParts.join(' ') : undefined,
  };
}

// ── LUD-21 verify polling ─────────────────────────────────────────────────────

// Verify-poll failures that will never succeed on retry, so must abort the poll
// rather than be absorbed into "not settled yet".
const FATAL_VERIFY_PATTERNS = [/DIFFERENT invoice/, /no `pr` to bind/, /Refusing to fetch/];

/**
 * Is this verify error a permanent policy rejection rather than a transient fault?
 * @param {Error} e
 * @returns {boolean}
 */
function isFatalVerifyError(e) {
  return FATAL_VERIFY_PATTERNS.some((re) => re.test(e && e.message ? e.message : ''));
}

/**
 * Poll a LUD-21 verify URL until the invoice settles or the deadline passes.
 *
 * `expectedPr` binds the result to the invoice we actually minted, so a
 * `settled: true` describing some other payment is treated as an error rather
 * than reported as "you were paid".
 *
 * @param {string} verifyUrl
 * @param {number} timeoutSeconds  0 means no timeout.
 * @param {string} expectedPr      The BOLT-11 this verify URL belongs to.
 */
async function pollVerify(verifyUrl, timeoutSeconds, expectedPr) {
  const intervalMs = 3000;
  const deadline = timeoutSeconds > 0 ? Date.now() + timeoutSeconds * 1000 : Infinity;

  for (;;) {
    let status;
    try {
      status = await verifyLnurlPayment(verifyUrl, {
        allowedHosts: ALLOWED_LNURL_SERVICE_HOSTS,
        expectedPr,
      });
    } catch (e) {
      // A transient HTTP fault is worth retrying. A policy rejection — the
      // response settled a DIFFERENT invoice, or the URL failed the SSRF guard
      // — is deterministic: retrying only hides it, and with `--timeout 0` the
      // loop would hide it forever.
      if (isFatalVerifyError(e)) throw e;
      console.error(`verify poll error (will retry): ${e.message}`);
      status = { settled: false };
    }
    if (status.settled) {
      return { event: 'verify_result', status: 'PAID', settled: true, preimage: status.preimage, verifyUrl };
    }
    if (Date.now() >= deadline) {
      return { event: 'verify_result', status: 'TIMEOUT', settled: false, verifyUrl };
    }
    await new Promise((r) => setTimeout(r, intervalMs));
  }
}

// ── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (!args.address || args.amountSats === null) {
    console.error(
      'Usage: node create_invoice_lnaddress.js <lightning_address> <amount_sats> [memo...] [--timeout <seconds>] [--no-verify] [--qr]',
    );
    process.exit(1);
  }

  // API key is optional here — the custodial probe works better with it, but a
  // non-custodial receive needs no credentials.
  const apiKey = getApiKey({ required: false });
  const apiUrl = getApiUrl();

  // 1. Classify the recipient (custodial vs non-custodial / Spark).
  const receiver = await resolveReceiver(args.address, {
    apiKey,
    apiUrl,
    defaultDomain: DEFAULT_LN_ADDRESS_DOMAIN,
  });

  console.error(`Resolved ${receiver.lightningAddress} as ${receiver.type} account.`);

  // 2. Mint the invoice over LNURL-pay (works for both account types).
  const invoice = await getInvoiceFromLightningAddress(receiver.lightningAddress, args.amountSats, args.memo, {
    defaultDomain: DEFAULT_LN_ADDRESS_DOMAIN,
    // The address domain stays on the narrow set; the server-supplied
    // callback/verify URLs may live on Blink's LNURL service host.
    allowedAddressDomains: ALLOWED_LN_ADDRESS_DOMAINS,
    allowedHosts: ALLOWED_LNURL_SERVICE_HOSTS,
  });

  const creationResult = {
    event: 'invoice_created',
    accountType: receiver.type,
    lightningAddress: receiver.lightningAddress,
    paymentRequest: invoice.paymentRequest,
    verifyUrl: invoice.verify,
    satoshis: args.amountSats,
    // A wallet id only exists for custodial recipients.
    walletId: receiver.walletId,
  };

  // Optional QR: render BEFORE printing so the first JSON already carries the
  // pngPath (mirrors the `blink qr` output fields). A render failure must not
  // lose the invoice — the QR is a convenience, the paymentRequest is the product.
  if (args.qr) {
    try {
      const { renderInvoiceQr } = require('./qr_invoice');
      Object.assign(creationResult, renderInvoiceQr(invoice.paymentRequest));
    } catch (e) {
      console.error(`QR rendering failed (non-fatal): ${e.message}`);
    }
  }

  console.log(JSON.stringify(creationResult, null, 2));

  // 3. Detect settlement via LUD-21 verify (the only cross-provider signal).
  if (args.noVerify) {
    console.error('Verify polling skipped (--no-verify).');
    return;
  }
  if (!invoice.verify) {
    console.error('No LUD-21 verify URL returned by the server; cannot poll for settlement here.');
    console.error('For custodial recipients you can instead subscribe with `create-invoice` on the recipient account.');
    return;
  }

  console.error(`Polling LUD-21 verify for settlement (timeout: ${args.timeoutSeconds}s)...`);
  console.error(
    'Note: for non-custodial (Spark) recipients the settled flag is webhook-populated and may lag a few seconds.',
  );
  const result = await pollVerify(invoice.verify, args.timeoutSeconds, invoice.paymentRequest);
  console.log(JSON.stringify(result, null, 2));
  exitAfterStdout(result.settled ? 0 : 1); // flush piped stdout first (v3.0.3 sweep)
  return;
}

if (require.main === module) {
  main().catch((e) => {
    console.error('Error:', e.message);
    process.exit(1);
  });
}

module.exports = { main, parseArgs, pollVerify, isFatalVerifyError, ARG_OPTIONS };
