#!/usr/bin/env node
/**
 * Blink Wallet - Non-custodial (Spark) Lightning address lifecycle
 *
 * Usage:
 *   node spark_lnaddress.js get                                    [--network mainnet|regtest]
 *   node spark_lnaddress.js check <username>                       [--network mainnet|regtest]
 *   node spark_lnaddress.js register <username> [--description "…"] [--network mainnet|regtest]
 *   node spark_lnaddress.js delete                                 [--network mainnet|regtest]
 *
 * Manages the registered user@blink.sv Lightning address for a self-custodial
 * (Spark) wallet via the Breez Spark SDK. All operations run against the
 * BLINK LNURL domain (config.lnurlDomain, pinned by _spark_sdk.connect to
 * blink.sv / staging.blink.sv — never the Breez default breez.tips).
 *
 * get: reports the wallet's registered address. The SDK recovers it
 * automatically on connect (keyed by the seed-derived identity pubkey), so a
 * seed imported from blink-mobile with a registered address is discoverable
 * from the seed alone. `registered: false` when the wallet has none.
 *
 * check: availability is a server-side uniqueness lookup across BOTH account
 * providers — an available username is claimable by anyone.
 *
 * register: claims the username on the wallet's pubkey. Server rules we
 * mirror client-side: one username per pubkey per domain (a new registration
 * REPLACES the wallet's previous one); usernames are 3-50 chars [a-z0-9_]
 * with at least one letter, lowercase-only (uppercase input is REJECTED
 * client-side, never silently normalized); phone identifiers are not
 * supported for Spark. No funds move — this is a public-identity choice.
 *
 * delete: removes the address (reversible by re-registering, subject to
 * availability).
 *
 * No budget interaction: nothing here spends; register/delete change only the
 * wallet's public receive identity.
 *
 * Environment:
 *   SPARK_MNEMONIC  - Required. 12/24-word BIP39 seed (spend authority — keep secret).
 *   BREEZ_API_KEY   - Required. Breez API key.
 *
 * Dependencies: @breeztech/breez-sdk-spark (optional; Node 22+).
 */

const { strictArgv, assertPositionalCount } = require('./_blink_client');
const { connect, lnurlDomainFor, probeLnLookupHealthy } = require('./_spark_sdk');

// Username rules mirrored from the Blink LNURL server (identifier.rs) and the
// app's own validation — validated client-side so bad input never hits the
// network. 3-50 chars, [a-z0-9_], at least one letter; uppercase is REJECTED
// (never silently normalized — fail fast like every other rule); the server
// additionally rejects lookalike-payment prefixes (1/3/_/bc1/lnbc1) which we
// surface as a warning-level check too.
const RESERVED_PREFIXES = ['1', '3', '_', 'bc1', 'lnbc1'];

function validateUsername(raw) {
  const username = String(raw || '').trim();
  if (username.length < 3 || username.length > 50) {
    throw new Error('Username must be 3-50 characters');
  }
  if (/[A-Z]/.test(username)) {
    throw new Error('Username must be lowercase — uppercase letters are rejected, not silently normalized');
  }
  if (!/^[a-z0-9_]+$/.test(username)) {
    throw new Error('Username may contain only lowercase letters, digits, and underscores');
  }
  if (!/[a-z]/.test(username)) {
    throw new Error('Username must contain at least one letter');
  }
  if (RESERVED_PREFIXES.some((p) => username.startsWith(p))) {
    throw new Error("Username starts with a reserved payment-like prefix ('1', '3', '_', 'bc1', 'lnbc1')");
  }
  return username;
}

// Every option this script accepts; anything else is refused (v3.0.4 strict sweep).
const ARG_OPTIONS = { network: { type: 'string' }, description: { type: 'string' } };

function parseArgs(argv) {
  argv = strictArgv(argv, ARG_OPTIONS);
  // Exact arity per subcommand (PR #27 review): `delete`/`get` take no
  // username, `check`/`register` exactly one — an extra word is refused.
  {
    const pos = [];
    for (let i = 0; i < argv.length; i++) {
      if (argv[i] === '--network' || argv[i] === '--description') i++;
      else pos.push(argv[i]);
    }
    const arity = { get: 1, delete: 1, check: 2, register: 2 };
    if (Object.hasOwn(arity, pos[0])) assertPositionalCount(pos, arity[pos[0]], arity[pos[0]]);
  }
  let subcommand = null;
  let username = null;
  let description;
  let network = process.env.SPARK_NETWORK || 'mainnet';
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--network' && i + 1 < argv.length) {
      network = argv[++i];
    } else if (arg === '--description' && i + 1 < argv.length) {
      description = argv[++i];
    } else if (subcommand === null) {
      subcommand = arg;
    } else if (username === null) {
      username = arg;
    } else {
      throw new Error(`Unexpected argument '${arg}'`);
    }
  }
  return { subcommand, username, description, network };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const valid = ['get', 'check', 'register', 'delete'];
  if (!valid.includes(args.subcommand)) {
    console.error(
      'Usage: node spark_lnaddress.js get | check <username> | register <username> [--description "..."] | delete  [--network mainnet|regtest]',
    );
    process.exit(1);
  }
  if ((args.subcommand === 'check' || args.subcommand === 'register') && !args.username) {
    console.error(`Usage: spark_lnaddress.js ${args.subcommand} <username>`);
    process.exit(1);
  }
  if (args.subcommand !== 'check' && args.subcommand !== 'register') {
    args.username = null; // get/delete take no username
  }

  const domain = lnurlDomainFor(args.network);
  const { sdk, disconnect } = await connect({ network: args.network });
  try {
    if (args.subcommand === 'get') {
      const info = await sdk.getLightningAddress();
      if (info) {
        console.log(
          JSON.stringify(
            {
              accountType: 'spark',
              network: args.network,
              lnurlDomain: domain,
              registered: true,
              lightningAddress: info.lightningAddress,
              username: info.username,
              lnurl: info.lnurl,
              description: info.description,
            },
            null,
            2,
          ),
        );
        return;
      }
      // Cache miss. getLightningAddress() reads the recovery-on-connect cache,
      // and recovery fails SILENTLY inside the SDK — if the LNURL management
      // service is unreachable (observed live: blink.sv endpoints 404'd while
      // the address existed), null means "cannot know", not "none". Probe the
      // service before claiming the negative: a false `registered: false`
      // invites the user to re-register and replace an existing address.
      const probe = await probeLnLookupHealthy(sdk);
      if (!probe.healthy) {
        console.log(
          JSON.stringify(
            {
              accountType: 'spark',
              network: args.network,
              lnurlDomain: domain,
              registered: 'unknown',
              lightningAddress: null,
              username: null,
              lookupError: probe.error,
              message:
                'Cannot verify whether an address is registered — the LNURL lookup service is unreachable. ' +
                'This is NOT a "no address" answer. Do not register/delete until the service answers.',
            },
            null,
            2,
          ),
        );
        console.error(
          `Warning: LNURL lookup service unreachable (${probe.error}) — registered status is UNKNOWN, not false.`,
        );
        process.exitCode = 1;
        return;
      }
      console.log(
        JSON.stringify(
          {
            accountType: 'spark',
            network: args.network,
            lnurlDomain: domain,
            registered: false,
            lightningAddress: null,
            username: null,
          },
          null,
          2,
        ),
      );
      return;
    }

    if (args.subcommand === 'check') {
      const username = validateUsername(args.username);
      const available = await sdk.checkLightningAddressAvailable({ username });
      console.log(
        JSON.stringify(
          {
            accountType: 'spark',
            network: args.network,
            lnurlDomain: domain,
            username,
            available,
          },
          null,
          2,
        ),
      );
      return;
    }

    if (args.subcommand === 'register') {
      const username = validateUsername(args.username);
      const available = await sdk.checkLightningAddressAvailable({ username });
      if (!available) {
        console.error(`Username '${username}' is not available on ${domain}.`);
        console.log(
          JSON.stringify(
            { event: 'lnaddress_register', status: 'UNAVAILABLE', username, lnurlDomain: domain },
            null,
            2,
          ),
        );
        process.exitCode = 1;
        return;
      }
      const request = { username };
      if (args.description !== undefined) request.description = args.description;
      const info = await sdk.registerLightningAddress(request);
      console.log(
        JSON.stringify(
          {
            event: 'lnaddress_register',
            status: 'REGISTERED',
            accountType: 'spark',
            network: args.network,
            lnurlDomain: domain,
            lightningAddress: info.lightningAddress,
            username: info.username,
            lnurl: info.lnurl,
            description: info.description,
          },
          null,
          2,
        ),
      );
      return;
    }

    // delete
    await sdk.deleteLightningAddress();
    console.log(
      JSON.stringify(
        {
          event: 'lnaddress_delete',
          status: 'DELETED',
          accountType: 'spark',
          network: args.network,
          lnurlDomain: domain,
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

module.exports = { main, parseArgs, validateUsername, ARG_OPTIONS };
