#!/usr/bin/env node
/**
 * Blink Wallet - Non-custodial (Spark) token metadata
 *
 * Usage: node spark_token_info.js <identifier|usdb> [--network mainnet|regtest]
 *
 * Fetches BTKN token metadata (name, ticker, decimals, max supply, issuer)
 * via the Breez Spark SDK. Useful for resolving the decimal precision a
 * token amount needs before sending, and for verifying a token identifier.
 *
 * 'usdb' resolves per-network (SPARK_USDB_TOKEN env var, then the mainnet
 * constant — only valid on mainnet).
 *
 * Environment:
 *   SPARK_MNEMONIC  - Required. 12/24-word BIP39 seed (spend authority — keep secret).
 *   BREEZ_API_KEY   - Required. Breez API key for the SDK to reach the Spark service.
 *
 * Dependencies: @breeztech/breez-sdk-spark (optional; Node 22+).
 */

const { strictArgv } = require('./_blink_client');
const { connect, resolveTokenIdentifier, normalizeSdkValue } = require('./_spark_sdk');

// Every option this script accepts; anything else is refused (v3.0.4 strict sweep).
const ARG_OPTIONS = { network: { type: 'string' } };

function parseArgs(argv) {
  argv = strictArgv(argv, ARG_OPTIONS, { positionals: [0, 1] });
  let token = null;
  let network = process.env.SPARK_NETWORK || 'mainnet';
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--network' && i + 1 < argv.length) {
      network = argv[i + 1];
      i++;
    } else if (token === null) {
      token = argv[i].trim();
    }
  }
  return { token, network };
}

async function main() {
  const { token, network } = parseArgs(process.argv.slice(2));
  if (!token) {
    console.error('Usage: node spark_token_info.js <identifier|usdb> [--network mainnet|regtest]');
    process.exit(1);
  }

  const identifier = resolveTokenIdentifier(token, network);
  const { sdk, disconnect } = await connect({ network });
  try {
    const response = await sdk.getTokensMetadata({ tokenIdentifiers: [identifier] });
    const meta = response && response.tokensMetadata && response.tokensMetadata[0];
    if (!meta) {
      console.error(`No metadata found for token: ${identifier}`);
      console.log(JSON.stringify({ identifier, found: false }, null, 2));
      return;
    }
    console.log(
      JSON.stringify(
        {
          identifier,
          found: true,
          ...normalizeSdkValue(meta),
        },
        null,
        2,
      ),
    );
  } finally {
    await disconnect();
  }
}

if (require.main === module) {
  main()
    .then(async () => {
      // The Breez SDK keeps event-loop handles open after disconnect; force a
      // clean exit. Drain stdout first so the JSON is never truncated.
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

module.exports = { main, parseArgs, ARG_OPTIONS };
