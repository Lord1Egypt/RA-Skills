#!/usr/bin/env node
/**
 * Blink Wallet - Non-custodial (Spark) fee probe
 *
 * Usage: node spark_fee_probe.js <destination> <amount_sats> [--network mainnet|regtest]
 *
 * Estimates the fee for sending from a NON-CUSTODIAL (Spark) account without
 * sending anything. Runs the same prepare step as spark-send (which always
 * resolves fees before signing) but stops there — no budget check, no spend,
 * no spending-log entry.
 *
 * This is the non-custodial counterpart of the custodial `fee-probe` command:
 * an agent can compare routes/costs before asking the user to confirm a send.
 *
 * <destination> — same inputs as spark-send:
 *   - a BOLT-11 invoice
 *   - a Spark address
 *   - a Lightning Address / LNURL (uses the LNURL-pay path)
 *
 * Environment:
 *   SPARK_MNEMONIC  - Required. 12/24-word BIP39 seed (validated, never logged;
 *                     nothing is signed or sent).
 *   BREEZ_API_KEY   - Required. Breez API key.
 *
 * Dependencies: @breeztech/breez-sdk-spark (optional; Node 22+).
 */

const { connect, resolveTokenIdentifier, parseTokenAmount } = require('./_spark_sdk');
const {
  parseArgs,
  classifyDestination,
  prepareLnurl,
  prepareBolt,
  prepareToken,
  conversionEstimateFrom,
} = require('./spark_send');

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args.destination || args.amountSats === null || args.dryRun || args.force) {
    console.error(
      'Usage: node spark_fee_probe.js <destination> <amount_sats> [--network mainnet|regtest]\n' +
        '       node spark_fee_probe.js <spark-address-or-invoice> <amount> --token usdb|<identifier> [--base-units] [--from-btc]\n' +
        '       node spark_fee_probe.js <bolt11-invoice> <amount_sats> --from-token usdb|<identifier>',
    );
    process.exit(1);
  }

  const tokenMode = args.token !== null || args.fromBtc || args.fromToken !== null;
  const { sdk, disconnect } = await connect({ network: args.network });
  try {
    // 1. Classify the destination (same exhaustive rule as spark-send).
    const parsed = await sdk.parse(args.destination);
    const dest = classifyDestination(parsed);

    if (tokenMode) {
      // Token / conversion quote: the prepare response's conversionEstimate
      // IS the quote (source units in, target units out, fee) — nothing sent.
      let tokenIdentifier = null;
      let amountBaseUnits = null;
      let conversionOptions = null;

      if (args.token !== null) {
        if (dest.type !== 'spark') {
          throw new Error('Token probes require a Spark address or Spark invoice destination.');
        }
        tokenIdentifier = resolveTokenIdentifier(args.token, args.network);
        if (args.baseUnits) {
          amountBaseUnits = BigInt(args.amountSats);
        } else {
          const meta = await sdk.getTokensMetadata({ tokenIdentifiers: [tokenIdentifier] });
          const m = meta && meta.tokensMetadata && meta.tokensMetadata[0];
          if (!m) throw new Error(`No metadata found for token ${tokenIdentifier} — use --base-units.`);
          amountBaseUnits = parseTokenAmount(args.amountSats, m.decimals);
        }
        if (args.fromBtc) {
          conversionOptions = { conversionType: { type: 'fromBitcoin' }, maxSlippageBps: args.slippageBps };
        }
      } else {
        // --from-token: quote a BTC payment paid from token funds.
        if (dest.type !== 'bolt11') {
          throw new Error('--from-token probes a BOLT-11 invoice paid from token funds.');
        }
        const fromTokenIdentifier = resolveTokenIdentifier(args.fromToken, args.network);
        conversionOptions = {
          conversionType: { type: 'toBitcoin', fromTokenIdentifier },
          maxSlippageBps: args.slippageBps,
        };
      }

      const { prepareResponse, feeSats } = await prepareToken(
        sdk,
        args.destination,
        amountBaseUnits,
        tokenIdentifier,
        conversionOptions,
      );
      const conversion = conversionEstimateFrom(prepareResponse);

      // Amount binding for --from-token quotes: no amount is passed for a
      // toBitcoin conversion, so the INVOICE's BTC amount is authoritative —
      // the same check spark-send enforces before dispatch. A mismatching
      // quote fails loudly so the agent never confirms the wrong number.
      let authoritativeSats;
      if (args.fromToken !== null) {
        authoritativeSats = Number(prepareResponse && prepareResponse.amount);
        if (!Number.isSafeInteger(authoritativeSats) || authoritativeSats <= 0) {
          throw new Error(
            `Could not determine the invoice's BTC amount for the --from-token quote (prepared amount: ${String(
              prepareResponse && prepareResponse.amount,
            )}).`,
          );
        }
        if (authoritativeSats !== Number(args.amountSats)) {
          throw new Error(
            `Amount mismatch: the invoice is for ${authoritativeSats} sats but ${args.amountSats} was supplied. ` +
              'Re-run with the invoice amount.',
          );
        }
      }

      console.log(
        JSON.stringify(
          {
            event: 'fee_probe',
            destination: args.destination,
            destinationType: dest.type,
            amountSats: args.token !== null ? undefined : args.amountSats,
            tokenIdentifier,
            amountBaseUnits: amountBaseUnits !== null ? String(amountBaseUnits) : undefined,
            feeBaseUnits: args.token !== null ? feeSats : undefined,
            feeSats: args.token !== null ? undefined : feeSats,
            conversionEstimate: conversion,
            network: args.network,
          },
          null,
          2,
        ),
      );
      return;
    }

    // 2. Prepare only — resolves fees, moves nothing, signs nothing.
    const { feeSats } =
      dest.type === 'lnurl'
        ? await prepareLnurl(sdk, dest.parsed, args.amountSats)
        : await prepareBolt(sdk, args.destination, args.amountSats);

    console.log(
      JSON.stringify(
        {
          event: 'fee_probe',
          destination: args.destination,
          destinationType: dest.type,
          amountSats: args.amountSats,
          feeSats,
          network: args.network,
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
      // clean exit so the command returns promptly for the caller/agent.
      // Drain stdout first — process.exit() can truncate a pending write when
      // stdout is a pipe, and the JSON result is this command's whole product.
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

const { ARG_OPTIONS } = require('./spark_send');

module.exports = { main, ARG_OPTIONS };
