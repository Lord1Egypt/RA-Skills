#!/usr/bin/env node
/**
 * Blink Wallet - Subscribe to Invoice Payment Status
 *
 * Usage: node subscribe_invoice.js <bolt11_invoice> [--timeout <seconds>]
 *
 * Watches a Lightning invoice via Blink's GraphQL WebSocket API and exits when
 * the invoice is PAID or EXPIRED. Status updates are printed to stderr, final
 * JSON result to stdout.
 *
 * Arguments:
 *   bolt11_invoice - Required. The BOLT-11 payment request string (lnbc...)
 *   --timeout      - Optional. Timeout in seconds (default: 300). Use 0 for no timeout.
 *
 * Environment:
 *   BLINK_API_KEY  - Required. Blink API key (format: blink_...)
 *   BLINK_API_URL  - Optional. Override API endpoint (default: https://api.blink.sv/graphql)
 */

const {
  getApiKey,
  getWsUrl,
  normalizeInvoice,
  requireWebSocket,
  subscribeToInvoice,
  exitAfterStdout,
  strictArgv,
} = require('./_blink_client');

// Every option this script accepts; anything else is refused (v3.0.4 strict sweep).
const ARG_OPTIONS = { timeout: { type: 'string' } };

function parseArgs(argv) {
  argv = strictArgv(argv, ARG_OPTIONS, { positionals: [0, 1] });
  let invoice = null;
  let timeoutSeconds = 300;

  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--timeout') {
      const value = argv[i + 1];
      if (!value) throw new Error('Missing value for --timeout');
      timeoutSeconds = parseInt(value, 10);
      if (isNaN(timeoutSeconds) || timeoutSeconds < 0) throw new Error('--timeout must be a non-negative integer');
      i++;
    } else if (!invoice) {
      invoice = arg;
    }
  }

  return { invoice, timeoutSeconds };
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args.invoice) {
    console.error('Usage: node subscribe_invoice.js <bolt11_invoice> [--timeout <seconds>]');
    process.exit(1);
  }

  const paymentRequest = normalizeInvoice(args.invoice);
  if (!paymentRequest) {
    console.error('Error: bolt11_invoice must be a non-empty string');
    process.exit(1);
  }

  requireWebSocket();

  const apiKey = getApiKey();
  const wsUrl = getWsUrl();

  subscribeToInvoice({
    paymentRequest,
    apiKey,
    wsUrl,
    timeoutSeconds: args.timeoutSeconds,
    onResult(result, exitCode) {
      console.log(JSON.stringify(result, null, 2));
      exitAfterStdout(exitCode); // flush piped stdout first (v3.0.3 sweep)
      return;
    },
  });
}

if (require.main === module) {
  try {
    main();
  } catch (e) {
    console.error('Error:', e.message);
    process.exit(1);
  }
}

module.exports = { main, parseArgs, ARG_OPTIONS };
