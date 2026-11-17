#!/usr/bin/env node
/**
 * Blink Wallet - Non-custodial (Spark) account info
 *
 * Usage: node spark_info.js [--network mainnet|regtest]
 *
 * Shows a NON-CUSTODIAL (Spark) account's info directly from the wallet via
 * the Breez Spark SDK — the non-custodial counterpart of the custodial
 * `account-info` command. Balance and history are not visible through the
 * Blink API at all; they live in the Spark wallet and must be read with the
 * seed via the SDK.
 *
 * Output: the SDK's getInfo() response plus accountType and network, with
 * SDK values normalized for JSON: safe-integer BigInts become Numbers,
 * BigInts outside the safe range become decimal Strings, and SDK Maps
 * (e.g. tokenBalances) become plain objects.
 *
 * Environment:
 *   SPARK_MNEMONIC  - Required. 12/24-word BIP39 seed (spend authority — keep secret).
 *   BREEZ_API_KEY   - Required. Breez API key for the SDK to reach the Spark service.
 *
 * Dependencies: @breeztech/breez-sdk-spark (optional; Node 22+).
 */

const { strictArgv } = require('./_blink_client');
const { connect, normalizeInfo, normalizeSdkValue, lnurlDomainFor, probeLnLookupHealthy } = require('./_spark_sdk');

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
    const info = await sdk.getInfo({ ensureSynced: true });
    // The wallet's registered @blink.sv Lightning address (recovered into the
    // SDK cache on connect). The cache read fails SILENTLY when the LNURL
    // service is unreachable (recovery-on-connect error is swallowed by the
    // SDK), so a null result is only trustworthy after probing the service —
    // observed live: blink.sv management endpoints 404'd while a registered
    // address existed, and this reported a false `lightningAddress: null`.
    let lightningAddress = null;
    let lnAddressStatus = 'none';
    try {
      const lnAddress = await sdk.getLightningAddress();
      if (lnAddress) {
        lightningAddress = lnAddress.lightningAddress;
        lnAddressStatus = 'registered';
      } else {
        const probe = await probeLnLookupHealthy(sdk);
        lnAddressStatus = probe.healthy ? 'none' : 'unverified';
      }
    } catch {
      // Recovery/lookup failures are non-fatal: info without the address is
      // strictly better than no info at all — but never present null as a
      // verified "no address" fact.
      lnAddressStatus = 'unverified';
    }
    console.log(
      JSON.stringify(
        {
          accountType: 'spark',
          network,
          lightningAddress,
          // 'registered' | 'none' (verified: the lookup service answered) |
          // 'unverified' (service unreachable — null means "cannot know", not
          // "no address"; see spark-lnaddress get).
          lnAddressStatus,
          lnurlDomain: lnurlDomainFor(network),
          ...normalizeSdkValue(info),
          // balanceSats re-normalized for a stable contract across SDK versions.
          balanceSats: normalizeInfo(info).balanceSats,
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

module.exports = { main, parseArgs, ARG_OPTIONS };
