#!/usr/bin/env node
/**
 * Blink Wallet - L402 Challenge Creator
 *
 * Usage: node l402_challenge_create.js --amount <sats> [options]
 *
 * Creates an L402 payment challenge for protecting API resources.
 * Generates a Lightning invoice via Blink and issues a signed macaroon
 * binding the invoice's payment hash with optional caveat constraints.
 *
 * The output includes a ready-to-use WWW-Authenticate header that your
 * server can return with a 402 Payment Required response.
 *
 * Arguments:
 *   --amount <sats>     Required. Invoice amount in satoshis.
 *   --wallet <id>       Optional. Blink wallet ID (auto-resolved to BTC if omitted).
 *   --memo <text>       Optional. Invoice memo/description.
 *   --expiry <seconds>  Optional. Seconds until macaroon expires (e.g. 3600 = 1 hour).
 *                       This controls the caveat expiry, NOT the invoice expiry.
 *   --resource <id>     Optional. Resource identifier caveat (e.g. "/api/v1/data").
 *
 * Environment:
 *   BLINK_API_KEY         Required. Blink API key with Write scope.
 *   BLINK_API_URL         Optional. Override Blink GraphQL endpoint.
 *   BLINK_L402_ROOT_KEY   Optional. 64-char hex root key for HMAC signing.
 *                         Auto-generated and persisted to ~/.blink/l402-root-key if not set.
 *
 * Output (JSON to stdout):
 *   {
 *     header,        // Ready-to-send WWW-Authenticate header value
 *     macaroon,      // base64url-encoded signed macaroon
 *     invoice,       // BOLT-11 payment request string
 *     paymentHash,   // 64-char hex payment hash
 *     satoshis,      // Invoice amount in satoshis
 *     expiresAt,     // Unix timestamp for macaroon expiry (null if no expiry)
 *     resource       // Resource caveat identifier (null if unconstrained)
 *   }
 *
 * Status messages to stderr.
 *
 * Dependencies: None (uses Node.js built-in fetch + _blink_client.js + _l402_macaroon.js)
 */

'use strict';

const {
  getApiKey,
  getApiUrl,
  graphqlRequest,
  getWallet,
  MUTATION_TIMEOUT_MS,
  strictParseArgs,
} = require('./_blink_client');

const { getRootKey, createMacaroon } = require('./_l402_macaroon');

// ── GraphQL mutation ─────────────────────────────────────────────────────────

const CREATE_INVOICE_MUTATION = `
  mutation LnInvoiceCreate($input: LnInvoiceCreateInput!) {
    lnInvoiceCreate(input: $input) {
      invoice {
        paymentRequest
        paymentHash
        satoshis
        paymentStatus
        createdAt
      }
      errors {
        code
        message
        path
      }
    }
  }
`;

// ── Arg parsing ──────────────────────────────────────────────────────────────

// Every option this script accepts (strict; exported for the CLI-forwarding guard).
const ARG_OPTIONS = {
  amount: { type: 'string' },
  wallet: { type: 'string' },
  memo: { type: 'string' },
  expiry: { type: 'string' },
  resource: { type: 'string' },
  help: { type: 'boolean', short: 'h', default: false },
};

function parseCliArgs(argv) {
  // Strict (PR #28 review): conflicting repeats and extra positionals are
  // refused, and errors never echo argument values.
  const { values } = strictParseArgs(argv, ARG_OPTIONS, { positionals: [0, 0] });

  if (values.help) {
    console.error(
      [
        'Usage: node l402_challenge_create.js --amount <sats> [options]',
        '',
        'Options:',
        '  --amount <sats>     Required. Invoice amount in satoshis.',
        '  --wallet <id>       Optional. Blink BTC wallet ID (auto-resolved if omitted).',
        '  --memo <text>       Optional. Invoice memo / description.',
        '  --expiry <seconds>  Optional. Macaroon expiry (seconds from now).',
        '  --resource <id>     Optional. Resource identifier caveat.',
        '  --help, -h          Show this help.',
      ].join('\n'),
    );
    process.exit(0);
  }

  if (!values.amount) {
    throw new Error('--amount <sats> is required.');
  }

  const amountSats = parseInt(values.amount, 10);
  if (isNaN(amountSats) || amountSats <= 0) {
    throw new Error('--amount must be a positive integer (satoshis).');
  }

  let expirySeconds = null;
  if (values.expiry !== undefined) {
    const n = parseInt(values.expiry, 10);
    if (isNaN(n) || n <= 0) {
      throw new Error('--expiry must be a positive integer (seconds).');
    }
    expirySeconds = Math.floor(Date.now() / 1000) + n;
  }

  return {
    amountSats,
    walletId: values.wallet || null,
    memo: values.memo || null,
    expirySeconds,
    resource: values.resource || null,
  };
}

// ── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  const args = parseCliArgs(process.argv.slice(2));

  const apiKey = getApiKey();
  const apiUrl = getApiUrl();

  // Resolve wallet ID (use provided or auto-resolve BTC wallet)
  let walletId = args.walletId;
  if (!walletId) {
    console.error('Resolving BTC wallet ID...');
    const wallet = await getWallet({ apiKey, apiUrl, currency: 'BTC' });
    walletId = wallet.id;
    console.error(`Using BTC wallet: ${walletId}`);
  }

  // Create Lightning invoice
  console.error(`Creating invoice for ${args.amountSats} sats...`);
  const input = { walletId, amount: args.amountSats };
  if (args.memo) input.memo = args.memo;

  const data = await graphqlRequest({
    query: CREATE_INVOICE_MUTATION,
    variables: { input },
    apiKey,
    apiUrl,
    timeoutMs: MUTATION_TIMEOUT_MS,
  });

  const result = data.lnInvoiceCreate;
  if (result.errors && result.errors.length > 0) {
    throw new Error(`Invoice creation failed: ${result.errors.map((e) => e.message).join(', ')}`);
  }
  if (!result.invoice) {
    throw new Error('Invoice creation returned no invoice and no errors.');
  }

  const { paymentRequest, paymentHash, satoshis } = result.invoice;
  console.error(`Invoice created: ${paymentHash}`);

  // Generate macaroon
  const rootKey = getRootKey();
  const macaroon = createMacaroon({
    paymentHash,
    rootKey,
    expirySeconds: args.expirySeconds,
    resource: args.resource,
  });

  // Build WWW-Authenticate header
  const header = `L402 macaroon="${macaroon}", invoice="${paymentRequest}"`;

  const output = {
    header,
    macaroon,
    invoice: paymentRequest,
    paymentHash,
    satoshis,
    expiresAt: args.expirySeconds,
    resource: args.resource,
  };

  console.log(JSON.stringify(output, null, 2));
}

if (require.main === module) {
  main().catch((e) => {
    console.error('Error:', e.message);
    process.exit(1);
  });
}

module.exports = { main, parseCliArgs, ARG_OPTIONS };
