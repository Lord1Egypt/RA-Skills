#!/usr/bin/env node
/**
 * Blink Wallet - Non-custodial (Spark) transaction history
 *
 * Usage: node spark_transactions.js [--limit <n>] [--offset <n>] [--type send|receive] [--network mainnet|regtest]
 *
 * Lists recent payments for a NON-CUSTODIAL (Spark) account from the wallet via
 * the Breez Spark SDK. Non-custodial parity for the custodial `transactions`
 * command.
 *
 * RESEARCH NOTE: this is a significant gap for API developers. Custodial history
 * is queryable over the Blink GraphQL API (`me...transactions`). Non-custodial
 * history is SDK-LOCAL — it is not exposed by the Blink API at all, so it can
 * only be read with the seed. See the findings for a proposed API read model
 * (settlement mirroring via the LNURL server's outbound webhook).
 *
 * Environment:
 *   SPARK_MNEMONIC  - Required. 12/24-word BIP39 seed.
 *   BREEZ_API_KEY   - Required. Breez API key.
 *
 * Dependencies: @breeztech/breez-sdk-spark (optional; Node 22+).
 */

const { strictArgv } = require('./_blink_client');
const { connect, normalizePayment } = require('./_spark_sdk');

// Every option this script accepts; anything else is refused (v3.0.4 strict sweep).
const ARG_OPTIONS = {
  limit: { type: 'string' },
  offset: { type: 'string' },
  type: { type: 'string' },
  network: { type: 'string' },
};

function parseArgs(argv) {
  argv = strictArgv(argv, ARG_OPTIONS, { positionals: [0, 0] });
  let limit = 20;
  let offset = 0;
  let type = null;
  let network = process.env.SPARK_NETWORK || 'mainnet';
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--limit' && i + 1 < argv.length) {
      limit = parseInt(argv[i + 1], 10);
      if (isNaN(limit) || limit <= 0) throw new Error('--limit must be a positive integer');
      i++;
    } else if (argv[i] === '--offset' && i + 1 < argv.length) {
      offset = parseInt(argv[i + 1], 10);
      if (isNaN(offset) || offset < 0) throw new Error('--offset must be a non-negative integer');
      i++;
    } else if (argv[i] === '--type' && i + 1 < argv.length) {
      type = String(argv[i + 1]).toLowerCase();
      if (type !== 'send' && type !== 'receive') throw new Error("--type must be 'send' or 'receive'");
      i++;
    } else if (argv[i] === '--network' && i + 1 < argv.length) {
      network = argv[i + 1];
      i++;
    }
  }
  return { limit, offset, type, network };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const { sdk, disconnect } = await connect({ network: args.network });
  try {
    // listPayments signature varies slightly by SDK version; pass a request
    // object with a limit and normalize whatever comes back. The SDK supports
    // a native typeFilter — use it so pagination runs over the FILTERED
    // stream (client-side filtering after paging would return empty pages
    // while older matches exist).
    const request = { limit: args.limit, offset: args.offset };
    if (args.type) request.typeFilter = [args.type];
    const raw = await sdk.listPayments(request);
    const payments = Array.isArray(raw) ? raw : raw && raw.payments ? raw.payments : [];
    let normalized = payments.map(normalizePayment);
    // Defense in depth for SDK versions that ignore typeFilter: apply the
    // same filter client-side. When the SDK did filter, this is a no-op.
    if (args.type) normalized = normalized.filter((p) => p.type === args.type);
    console.log(
      JSON.stringify(
        {
          accountType: 'spark',
          network: args.network,
          count: normalized.length,
          transactions: normalized,
          // Offset-based (the SDK has no cursor). hasNextPage is a heuristic:
          // a full page MIGHT be the last one; fetch the next offset to know.
          pageInfo: {
            hasNextPage: payments.length === args.limit,
            limit: args.limit,
            offset: args.offset,
          },
          ...(args.type ? { typeFilter: args.type } : {}),
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
