#!/usr/bin/env node
/**
 * Blink Wallet - L402 Payment Verifier
 *
 * Usage: node l402_payment_verify.js --token <macaroon:preimage> [options]
 *        node l402_payment_verify.js --macaroon <b64> --preimage <hex> [options]
 *
 * Verifies an L402 Authorization token submitted by a client after payment.
 * Performs three layers of verification:
 *
 *   1. Preimage check:   SHA-256(preimage) === payment_hash  (cryptographic payment proof)
 *   2. Signature check:  HMAC-SHA256 of macaroon body === embedded signature  (authenticity)
 *   3. Caveat check:     expiry not exceeded, resource matches if constrained
 *
 * Optionally queries the Blink API to confirm PAID status on-chain.
 *
 * Arguments:
 *   --token <macaroon:preimage>   L402 Authorization token (colon-separated).
 *                                 Equivalent to passing --macaroon and --preimage separately.
 *   --macaroon <b64>              base64url-encoded macaroon (alternative to --token).
 *   --preimage <hex>              64-char hex preimage (alternative to --token).
 *   --resource <id>               Optional. Expected resource identifier for caveat check.
 *   --check-api                   Optional. Query Blink API to confirm PAID status.
 *
 * Environment:
 *   BLINK_L402_ROOT_KEY   Required for signature verification.
 *                         Resolved from env, ~/.blink/l402-root-key, or auto-generated.
 *   BLINK_API_KEY         Required only when --check-api is used.
 *   BLINK_API_URL         Optional. Override Blink GraphQL endpoint.
 *
 * Output (JSON to stdout):
 *   {
 *     valid,            // true if ALL checks pass (preimage + signature + caveats)
 *     preimageValid,    // SHA-256(preimage) === paymentHash
 *     signatureValid,   // HMAC signature check passed
 *     caveatsValid,     // All caveats satisfied
 *     paymentHash,      // 64-char hex payment hash from macaroon
 *     resource,         // Resource caveat from macaroon (null if unconstrained)
 *     expiresAt,        // Unix timestamp of expiry caveat (null if no expiry)
 *     expired,          // true if expiry caveat has passed
 *     apiStatus         // "PAID"|"PENDING"|"EXPIRED"|"NOT_CHECKED"|"ERROR" (--check-api)
 *   }
 *
 * Status messages to stderr.
 * Exit code 0 when valid=true, exit code 1 when valid=false or on error.
 *
 * Dependencies: None (uses Node.js built-in fetch + _blink_client.js + _l402_macaroon.js)
 */

'use strict';

const {
  getApiKey,
  getApiUrl,
  graphqlRequest,
  getAllWallets,
  exitAfterStdout,
  strictParseArgs,
} = require('./_blink_client');

const { getRootKey, decodeMacaroon, checkCaveats, verifyPreimage } = require('./_l402_macaroon');

// ── GraphQL query for API status check ───────────────────────────────────────

const CHECK_INVOICE_QUERY = `
  query InvoiceByHash($walletId: WalletId!, $paymentHash: PaymentHash!) {
    me {
      defaultAccount {
        walletById(walletId: $walletId) {
          ... on BTCWallet {
            invoiceByPaymentHash(paymentHash: $paymentHash) {
              ... on LnInvoice {
                paymentHash
                paymentStatus
              }
            }
          }
          ... on UsdWallet {
            invoiceByPaymentHash(paymentHash: $paymentHash) {
              ... on LnInvoice {
                paymentHash
                paymentStatus
              }
            }
          }
        }
      }
    }
  }
`;

// ── Arg parsing ──────────────────────────────────────────────────────────────

// Every option this script accepts (strict; exported for the CLI-forwarding guard).
const ARG_OPTIONS = {
  token: { type: 'string' },
  macaroon: { type: 'string' },
  preimage: { type: 'string' },
  resource: { type: 'string' },
  'check-api': { type: 'boolean', default: false },
  help: { type: 'boolean', short: 'h', default: false },
};

function parseCliArgs(argv) {
  // Strict (PR #28 review): conflicting repeats and extra positionals are
  // refused, and errors never echo argument values.
  const { values } = strictParseArgs(argv, ARG_OPTIONS, { positionals: [0, 0] });

  if (values.help) {
    console.error(
      [
        'Usage: node l402_payment_verify.js --token <macaroon:preimage> [options]',
        '       node l402_payment_verify.js --macaroon <b64> --preimage <hex> [options]',
        '',
        'Options:',
        '  --token <macaroon:preimage>  L402 token (colon-separated).',
        '  --macaroon <b64>             base64url-encoded macaroon.',
        '  --preimage <hex>             64-char hex preimage.',
        '  --resource <id>              Expected resource identifier for caveat check.',
        '  --check-api                  Query Blink API to confirm PAID status.',
        '  --help, -h                   Show this help.',
      ].join('\n'),
    );
    process.exit(0);
  }

  // Resolve macaroon and preimage from --token or separate flags
  let macaroon = values.macaroon || null;
  let preimage = values.preimage || null;

  if (values.token) {
    const colonIdx = values.token.indexOf(':');
    if (colonIdx === -1) {
      throw new Error('--token must be in <macaroon>:<preimage> format (colon-separated).');
    }
    macaroon = values.token.slice(0, colonIdx);
    preimage = values.token.slice(colonIdx + 1);
  }

  if (!macaroon) {
    throw new Error('Provide --token <macaroon:preimage> or both --macaroon <b64> and --preimage <hex>.');
  }
  if (!preimage) {
    throw new Error('--preimage is required (or use --token <macaroon:preimage>).');
  }

  if (!/^[0-9a-fA-F]{64}$/.test(preimage)) {
    const hint =
      preimage.length !== 64 ? `got ${preimage.length} characters, need exactly 64` : 'contains non-hex characters';
    throw new Error(
      `--preimage must be a 64-character hex string (${hint}). ` +
        `Example: blink l402-verify --token <macaroon>:<64-char-hex-preimage>`,
    );
  }

  return {
    macaroon,
    preimage,
    resource: values.resource || null,
    checkApi: values['check-api'],
  };
}

// ── API status check ─────────────────────────────────────────────────────────

/**
 * Query the Blink API for invoice payment status.
 * Returns "PAID", "PENDING", "EXPIRED", or "ERROR".
 *
 * @param {string} paymentHash  64-char hex payment hash
 * @param {string} apiKey
 * @param {string} apiUrl
 * @returns {Promise<string>}
 */
async function fetchApiStatus(paymentHash, apiKey, apiUrl) {
  try {
    const wallets = await getAllWallets({ apiKey, apiUrl });
    for (const wallet of wallets) {
      const data = await graphqlRequest({
        query: CHECK_INVOICE_QUERY,
        variables: { walletId: wallet.id, paymentHash },
        apiKey,
        apiUrl,
      });
      const walletResult = data.me?.defaultAccount?.walletById;
      if (!walletResult) continue;
      const inv = walletResult.invoiceByPaymentHash;
      if (inv && inv.paymentHash) {
        return inv.paymentStatus; // "PAID", "PENDING", or "EXPIRED"
      }
    }
    return 'NOT_FOUND';
  } catch (e) {
    console.error(`Warning: API status check failed: ${e.message}`);
    return 'ERROR';
  }
}

// ── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  const args = parseCliArgs(process.argv.slice(2));

  // Load root key (needed for signature verification)
  const rootKey = getRootKey();

  // Decode and verify macaroon signature
  let decoded;
  try {
    decoded = decodeMacaroon({ macaroon: args.macaroon, rootKey });
  } catch (e) {
    const output = {
      valid: false,
      preimageValid: false,
      signatureValid: false,
      caveatsValid: false,
      paymentHash: null,
      resource: null,
      expiresAt: null,
      expired: false,
      apiStatus: 'NOT_CHECKED',
      error: e.message,
    };
    console.log(JSON.stringify(output, null, 2));
    exitAfterStdout(1); // flush piped stdout first (v3.0.3 sweep)
    return;
  }

  const { signatureValid, paymentHash, expiresAt, resource } = decoded;

  // Verify preimage: SHA-256(preimage) === paymentHash
  const preimageValid = verifyPreimage(args.preimage, paymentHash);

  // Check caveats
  const { expired, resourceMismatch, resourceUnchecked, caveatsValid } = checkCaveats({
    expiresAt,
    resource,
    checkResource: args.resource,
  });

  // Determine overall validity
  const valid = preimageValid && signatureValid && caveatsValid;

  // Optional API check
  let apiStatus = 'NOT_CHECKED';
  if (args.checkApi) {
    console.error('Checking invoice status via Blink API...');
    const apiKey = getApiKey();
    const apiUrl = getApiUrl();
    apiStatus = await fetchApiStatus(paymentHash, apiKey, apiUrl);
    console.error(`API status: ${apiStatus}`);
  }

  const output = {
    valid,
    preimageValid,
    signatureValid,
    caveatsValid,
    paymentHash,
    resource,
    expiresAt,
    expired,
    apiStatus,
  };

  if (resourceMismatch) {
    output.resourceMismatch = true;
  }
  if (resourceUnchecked) {
    output.resourceUnchecked = true;
    output.message =
      `This token is scoped to the resource '${resource}'. Pass --resource <requested resource> to verify it; ` +
      'without it the token is rejected (a scoped token must never be accepted for an unknown request).';
  }

  console.log(JSON.stringify(output, null, 2));
  exitAfterStdout(valid ? 0 : 1); // flush piped stdout first (v3.0.3 sweep)
  return;
}

if (require.main === module) {
  main().catch((e) => {
    console.error('Error:', e.message);
    process.exit(1);
  });
}

module.exports = { main, parseCliArgs, fetchApiStatus, ARG_OPTIONS };
