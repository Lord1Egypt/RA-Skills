#!/usr/bin/env node
/**
 * Blink Wallet - Non-custodial (Spark) balance
 *
 * Usage: node spark_balance.js [--network mainnet|regtest]
 *
 * Reads the BTC balance of a NON-CUSTODIAL (Spark) account directly from the
 * wallet via the Breez Spark SDK. This is the non-custodial parity for the
 * custodial `balance` command.
 *
 * Custodial `balance` reads `me.defaultAccount.wallets` over the Blink GraphQL
 * API using BLINK_API_KEY. Non-custodial balance is NOT visible through the
 * Blink API at all — it lives in the Spark wallet — so it must be read via the
 * SDK using the account seed.
 *
 * Environment:
 *   SPARK_MNEMONIC  - Required. 12/24-word BIP39 seed (spend authority — keep secret).
 *   BREEZ_API_KEY   - Required. Breez API key for the SDK to reach the Spark service.
 *
 * Dependencies: @breeztech/breez-sdk-spark (optional; Node 22+).
 */

const { strictArgv } = require('./_blink_client');
const { connect, waitForStableBalance, normalizeTokenBalances } = require('./_spark_sdk');

// Every option this script accepts; anything else is refused (v3.0.4 strict sweep).
const ARG_OPTIONS = { network: { type: 'string' } };

function parseArgs(argv) {
  argv = strictArgv(argv, ARG_OPTIONS, { positionals: [0, 0] });
  let network = process.env.SPARK_NETWORK || 'mainnet';
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--network' && i + 1 < argv.length) {
      network = argv[i + 1];
      i++;
    }
  }
  return { network };
}

async function main() {
  const { network } = parseArgs(process.argv.slice(2));
  const { sdk, disconnect } = await connect({ network });
  try {
    // Wait for a stable balance to avoid reporting a mid-sync transient right
    // after an incoming payment.
    const { balanceSats, stable } = await waitForStableBalance(sdk);
    // Token balances (USDB and any other BTKN tokens held) come from the same
    // getInfo read; balances are STRINGS (BigInt precision preserved).
    const info = await sdk.getInfo({ ensureSynced: false });
    console.log(
      JSON.stringify(
        {
          accountType: 'spark',
          network,
          balanceSats,
          stable,
          tokenBalances: normalizeTokenBalances(info.tokenBalances),
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
    .then(() => {
      // The Breez SDK keeps event-loop handles open after disconnect; force a
      // clean exit so the command returns promptly for the caller/agent.
      // Preserves any exit code main() set.
      process.exit(process.exitCode || 0);
    })
    .catch((e) => {
      console.error('Error:', e.message);
      process.exit(1);
    });
}

module.exports = { main, parseArgs, ARG_OPTIONS };
