#!/usr/bin/env node
/**
 * Blink Wallet - Non-custodial (Spark) token receive (Spark invoice)
 *
 * Usage: node spark_receive_token.js <amount> [--token usdb|<identifier>] [--base-units]
 *                                       [--description "..."] [--network mainnet|regtest]
 *
 * Mints a Spark invoice for receiving a BTKN token (e.g. USDB) into the
 * self-custodial wallet. The invoice is a string another Spark wallet can
 * pay; it embeds the token identifier and (optionally) the amount.
 *
 * Amount semantics:
 *   - Default: decimal token units ('10.5' = 10.5 USDB), converted to base
 *     units using the token's decimals (fetched from token metadata).
 *   - --base-units: the amount is raw base units ('10500000' = 10.5 USDB at
 *     6 decimals) — exact, no metadata lookup needed.
 *
 * 'usdb' resolves per-network via resolveTokenIdentifier (SPARK_USDB_TOKEN
 * env var, then the mainnet constant — mainnet only).
 *
 * NOTE: this is a Spark invoice (sprt-ish string), NOT a BOLT-11 Lightning
 * invoice — it can only be paid by a Spark wallet. For custodial-parity USD
 * receive over Lightning there is no non-custodial equivalent; LNURL-pay
 * receive (create-invoice-lnaddress) is BTC-only.
 *
 * Environment:
 *   SPARK_MNEMONIC  - Required. 12/24-word BIP39 seed (spend authority — keep secret).
 *   BREEZ_API_KEY   - Required. Breez API key.
 *
 * Dependencies: @breeztech/breez-sdk-spark (optional; Node 22+).
 */

const { connect, resolveTokenIdentifier, parseTokenAmount } = require('./_spark_sdk');
const { strictArgv } = require('./_blink_client');

// Every option this script accepts; anything else is refused (v3.0.4 strict
// sweep). Free-text memo words go after `--` (e.g. a word like `-50%`),
// exactly as at the `blink` CLI.
const ARG_OPTIONS = {
  token: { type: 'string' },
  'base-units': { type: 'boolean' },
  description: { type: 'string' },
  network: { type: 'string' },
};

function parseArgs(argv) {
  argv = strictArgv(argv, ARG_OPTIONS, { keepTerminator: true, positionals: [0, Infinity] });
  let literal = false; // after `--`: every word is a positional (memo text)
  let amount = null;
  let token = 'usdb';
  let baseUnits = false;
  let description;
  let network = process.env.SPARK_NETWORK || 'mainnet';
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (!literal && arg === '--') {
      literal = true;
    } else if (!literal && arg === '--token' && i + 1 < argv.length) {
      token = argv[++i];
    } else if (!literal && arg === '--base-units') {
      baseUnits = true;
    } else if (!literal && arg === '--description' && i + 1 < argv.length) {
      description = argv[++i];
    } else if (!literal && arg === '--network' && i + 1 < argv.length) {
      network = argv[++i];
    } else if (amount === null) {
      amount = arg;
    } else {
      // Remaining bare args join the description (like create-invoice memo).
      description = description ? `${description} ${arg}` : arg;
    }
  }
  return { amount, token, baseUnits, description, network };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.amount === null) {
    console.error(
      'Usage: node spark_receive_token.js <amount> [--token usdb|<identifier>] [--base-units] [--description "..."] [--network mainnet|regtest]',
    );
    process.exit(1);
  }

  const identifier = resolveTokenIdentifier(args.token, args.network);
  const { sdk, disconnect } = await connect({ network: args.network });
  try {
    // Resolve base units: either given raw (--base-units) or converted from a
    // decimal amount using the token's decimals from metadata.
    let amountBaseUnits;
    if (args.baseUnits) {
      const raw = String(args.amount).trim();
      if (!/^\d+$/.test(raw)) throw new Error('--base-units amount must be a non-negative integer');
      amountBaseUnits = raw;
    } else {
      const response = await sdk.getTokensMetadata({ tokenIdentifiers: [identifier] });
      const meta = response && response.tokensMetadata && response.tokensMetadata[0];
      if (!meta) {
        throw new Error(`No metadata found for token ${identifier} — pass --base-units to skip the decimal lookup.`);
      }
      console.error(`Token: ${meta.name} (${meta.ticker}), ${meta.decimals} decimals.`);
      amountBaseUnits = String(parseTokenAmount(args.amount, meta.decimals));
    }

    const receiveMethod = {
      type: 'sparkInvoice',
      tokenIdentifier: identifier,
      amount: amountBaseUnits,
    };
    if (args.description !== undefined) receiveMethod.description = args.description;

    const response = await sdk.receivePayment({ paymentMethod: receiveMethod });
    console.log(
      JSON.stringify(
        {
          event: 'token_invoice_created',
          accountType: 'spark',
          network: args.network,
          tokenIdentifier: identifier,
          amountBaseUnits,
          baseUnits: args.baseUnits,
          paymentRequest: response.paymentRequest,
          fee: String(response.fee),
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
