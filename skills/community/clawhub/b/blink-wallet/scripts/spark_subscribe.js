#!/usr/bin/env node
/**
 * Blink Wallet - Non-custodial (Spark) event subscription
 *
 * Usage: node spark_subscribe.js [--timeout <seconds>] [--network mainnet|regtest]
 *
 * Subscribes to live wallet events for a NON-CUSTODIAL (Spark) account via the
 * Breez Spark SDK's event listener. Non-custodial parity for the custodial
 * `subscribe-updates` command (which uses the Blink GraphQL `myUpdates`
 * subscription over WebSocket).
 *
 * Emits one JSON line per SDK event (payment succeeded, synced, etc.).
 *
 * RESEARCH NOTE: the SDK event stream is the non-custodial equivalent of the
 * Blink `myUpdates` WS subscription and requires the seed. For a pure-API
 * alternative (no seed), the LNURL server's LUD-21 verify / outbound webhook is
 * the only cross-provider settlement signal — see create-invoice-lnaddress.
 *
 * Environment:
 *   SPARK_MNEMONIC  - Required. 12/24-word BIP39 seed.
 *   BREEZ_API_KEY   - Required. Breez API key.
 *
 * Dependencies: @breeztech/breez-sdk-spark (optional; Node 22+).
 */

const { strictArgv } = require('./_blink_client');
const { connect } = require('./_spark_sdk');

// Every option this script accepts; anything else is refused (v3.0.4 strict sweep).
const ARG_OPTIONS = { timeout: { type: 'string' }, network: { type: 'string' } };

function parseArgs(argv) {
  argv = strictArgv(argv, ARG_OPTIONS, { positionals: [0, 0] });
  let timeoutSeconds = 300;
  let network = process.env.SPARK_NETWORK || 'mainnet';
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--timeout' && i + 1 < argv.length) {
      timeoutSeconds = parseInt(argv[i + 1], 10);
      if (isNaN(timeoutSeconds) || timeoutSeconds < 0) throw new Error('--timeout must be a non-negative integer');
      i++;
    } else if (argv[i] === '--network' && i + 1 < argv.length) {
      network = argv[i + 1];
      i++;
    }
  }
  return { timeoutSeconds, network };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const { sdk, disconnect } = await connect({ network: args.network });

  let listenerId = null;
  const listener = {
    onEvent(event) {
      // Emit each event as a JSON line for the agent to consume.
      console.log(JSON.stringify({ event: 'sdk_event', payload: event }));
    },
  };

  // addEventListener returns a listener id in current SDK builds.
  listenerId = await sdk.addEventListener(listener);
  console.error(`Subscribed to Spark wallet events (timeout: ${args.timeoutSeconds}s)...`);

  const cleanup = async () => {
    try {
      if (listenerId !== null && listenerId !== undefined && sdk.removeEventListener) {
        await sdk.removeEventListener(listenerId);
      }
    } catch {
      // best-effort
    }
    await disconnect();
  };

  if (args.timeoutSeconds > 0) {
    await new Promise((resolve) => setTimeout(resolve, args.timeoutSeconds * 1000));
    console.error('Subscription timed out.');
    await cleanup();
    process.exit(0);
  } else {
    // Run until interrupted.
    process.on('SIGINT', async () => {
      await cleanup();
      process.exit(0);
    });
    await new Promise(() => {}); // never resolves
  }
}

if (require.main === module) {
  main().catch((e) => {
    console.error('Error:', e.message);
    process.exit(1);
  });
}

module.exports = { main, parseArgs, ARG_OPTIONS };
