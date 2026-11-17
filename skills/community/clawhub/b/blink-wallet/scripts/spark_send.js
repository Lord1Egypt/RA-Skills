#!/usr/bin/env node
/**
 * Blink Wallet - Non-custodial (Spark) SEND
 *
 * Usage: node spark_send.js <destination> <amount_sats> [--dry-run] [--force] [--network mainnet|regtest]
 *
 * Sends BTC from a NON-CUSTODIAL (Spark) account by SIGNING the transaction
 * locally with the account seed, via the Breez Spark SDK. This is the
 * non-custodial parity for the custodial `pay-invoice` / `pay-lnaddress`
 * commands.
 *
 * KEY POINT (research): unlike receive, non-custodial send CANNOT go through the
 * Blink GraphQL API — there is no Blink wallet to debit, and the Blink backend
 * cannot sign for a self-custodial account. The signature must be produced by
 * whoever holds the seed. This command demonstrates that an agent holding the
 * seed CAN send entirely client-side, with NO Blink API change and NO server
 * signer / VPS required.
 *
 * <destination> may be:
 *   - a BOLT-11 invoice            -> prepareSendPayment / sendPayment
 *   - a Spark address              -> prepareSendPayment / sendPayment
 *   - a Lightning Address / LNURL  -> prepareLnurlPay / lnurlPay
 * The command uses `sdk.parse()` to classify the destination and routes to the
 * correct SDK path. (A Lightning Address like `alice@blink.sv` is an LNURL-pay
 * destination and MUST use the LNURL path — prepareSendPayment does not accept
 * it.)
 *
 * SAFETY:
 *   - Always resolves fees via the prepare step first and prints them.
 *   - --dry-run prepares only (fees shown) and does NOT send.
 *   - Budget controls: BLINK_BUDGET_HOURLY_SATS / BLINK_BUDGET_DAILY_SATS are
 *     enforced when configured (like the custodial pay commands); an
 *     unconfigured budget does not block this explicit one-shot payment.
 *     The amount is RESERVED under the budget lock before sending and
 *     finalized (or released on failure) after, so concurrent sends cannot
 *     jointly exceed a limit. Successful/pending sends are recorded in the
 *     spending log.
 *   - --force bypasses the budget check for an over-limit send.
 *   - The seed (SPARK_MNEMONIC) is never logged.
 *
 * Environment:
 *   SPARK_MNEMONIC  - Required. 12/24-word BIP39 seed (spend authority — keep secret).
 *   BREEZ_API_KEY   - Required. Breez API key.
 *
 * Dependencies: @breeztech/breez-sdk-spark (optional; Node 22+).
 *
 * CAUTION: This signs and sends real bitcoin from a self-custodial wallet.
 */

const { connect, feeFromPrepare, safeErrorDetail, resolveTokenIdentifier, parseTokenAmount } = require('./_spark_sdk');
const { strictArgv } = require('./_blink_client');
const { reserveBudget, settleSpend, releaseSpend } = require('./_budget');

// Every option spark-send / spark-fee-probe accept; anything else is refused (PR #26 review).
const SPARK_SEND_OPTIONS = {
  'dry-run': { type: 'boolean' },
  force: { type: 'boolean' },
  network: { type: 'string' },
  token: { type: 'string' },
  'base-units': { type: 'boolean' },
  'from-btc': { type: 'boolean' },
  'from-token': { type: 'string' },
  'slippage-bps': { type: 'string' },
};

function parseArgs(argv) {
  // Strict first: `--dry-run=true` or a typo like `--dryrun` used to be read
  // as a positional and the SEND WAS REAL. Throws ARG_INVALID before any SDK.
  argv = strictArgv(argv, SPARK_SEND_OPTIONS, { positionals: [0, 2] });
  let destination = null;
  let amountSats = null;
  let dryRun = false;
  let force = false;
  let network = process.env.SPARK_NETWORK || 'mainnet';
  let token = null;
  let baseUnits = false;
  let fromBtc = false;
  let fromToken = null;
  let slippageBps = 50;

  // Pre-scan: the amount semantics depend on whether --token appears
  // ANYWHERE in argv — '10.5' is a decimal token amount in token mode but
  // must be integer sats otherwise. Deciding positionally would corrupt an
  // amount that precedes the flag ('spark-send <dest> 10.5 --token usdb').
  const tokenModePre = argv.includes('--token');

  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--dry-run') {
      dryRun = true;
    } else if (arg === '--force') {
      force = true;
    } else if (arg === '--network' && i + 1 < argv.length) {
      network = argv[i + 1];
      i++;
    } else if (arg === '--token' && i + 1 < argv.length) {
      token = argv[++i];
    } else if (arg === '--base-units') {
      baseUnits = true;
    } else if (arg === '--from-btc') {
      fromBtc = true;
    } else if (arg === '--from-token' && i + 1 < argv.length) {
      fromToken = argv[++i];
    } else if (arg === '--slippage-bps' && i + 1 < argv.length) {
      slippageBps = parseInt(argv[++i], 10);
      if (isNaN(slippageBps) || slippageBps < 0) throw new Error('--slippage-bps must be a non-negative integer');
    } else if (destination === null) {
      destination = arg.trim();
    } else if (amountSats === null) {
      if (tokenModePre) {
        amountSats = arg; // token mode: keep the RAW string (decimal or base units)
      } else {
        amountSats = parseInt(arg, 10);
        if (isNaN(amountSats) || amountSats <= 0) throw new Error('amount_sats must be a positive integer');
      }
    }
  }
  return { destination, amountSats, dryRun, force, network, token, baseUnits, fromBtc, fromToken, slippageBps };
}

/**
 * Classify an SDK parse() result into one of the routing targets this skill
 * supports. EXHAUSTIVE by design: the SDK recognizes more destination types
 * than we can pay to (on-chain Bitcoin addresses, BOLT-12 offers, cross-chain
 * addresses, URLs, ...), and a boolean LNURL-vs-everything-else check would
 * let any future SDK input type silently fall into the generic
 * prepareSendPayment path without ever having been validated for it. Only the
 * four types below are allowed; everything else is rejected by name.
 *
 * @param {object} parsed  Result of sdk.parse(destination).
 * @returns {{ type: 'lnurl'|'bolt11'|'spark', parsed: object }}
 * @throws {Error} code UNSUPPORTED_DESTINATION for any unrecognized type.
 */
function classifyDestination(parsed) {
  const t = parsed && typeof parsed.type === 'string' ? parsed.type.toLowerCase() : '';
  if (t === 'lnurlpay' || t === 'lightningaddress') return { type: 'lnurl', parsed };
  if (t === 'bolt11invoice') return { type: 'bolt11', parsed };
  if (t === 'sparkaddress' || t === 'sparkinvoice') return { type: 'spark', parsed };
  const e = new Error(
    `Unsupported destination type '${t || 'unknown'}'. Supported: BOLT-11 invoice, Spark address, Lightning Address, LNURL-pay URL.`,
  );
  e.code = 'UNSUPPORTED_DESTINATION';
  throw e;
}

/**
 * Determine whether a parsed input is an LNURL-pay / Lightning-address
 * destination (as opposed to a BOLT-11 invoice or Spark address).
 *
 * The WASM parse result uses a lowercase `type` discriminant. Different SDK
 * versions have used `lnUrlPay` and `lightningAddress`; treat both as LNURL.
 *
 * @param {object} parsed  Result of sdk.parse(destination).
 * @returns {boolean}
 */
function isLnurlPayInput(parsed) {
  if (!parsed) return false;
  const t = typeof parsed.type === 'string' ? parsed.type.toLowerCase() : '';
  return t === 'lnurlpay' || t === 'lightningaddress';
}

/**
 * Extract the LnurlPayRequestDetails from a parsed input, to hand to
 * prepareLnurlPay().
 *
 * The SDK's parse() result shape is:
 *   - { type: "lightningAddress", address, payRequest }  -> details in .payRequest
 *   - { type: "lnurlPay", ...LnurlPayRequestDetails }     -> the object IS the details
 *
 * @param {object} parsed
 * @returns {object}  LnurlPayRequestDetails (must have a `callback` field).
 */
function lnurlPayRequestFrom(parsed) {
  if (parsed && parsed.payRequest) return parsed.payRequest;
  return parsed;
}

/**
 * Send to a Lightning Address / LNURL-pay destination.
 *
 * PrepareLnurlPayRequest: { amount: bigint (sats), payRequest: details, comment? }
 * @returns {{ prepareResponse: object, feeSats: number|null }}
 */
async function prepareLnurl(sdk, parsed, amountSats) {
  const payRequest = lnurlPayRequestFrom(parsed);
  const prepareResponse = await sdk.prepareLnurlPay({
    amount: BigInt(amountSats),
    payRequest,
  });
  return { prepareResponse, feeSats: feeFromPrepare(prepareResponse) };
}

/**
 * Send to a BOLT-11 invoice / Spark address destination.
 * @returns {{ prepareResponse: object, feeSats: number|null }}
 */
async function prepareBolt(sdk, destination, amountSats) {
  // The SDK's PaymentRequest is a tagged enum, NOT a raw string:
  //   { type: "input", input: "<bolt11 | spark address | ...>" }
  // Passing the raw string fails with
  //   `invalid type: string ..., expected internally tagged enum PaymentRequest`.
  const prepareResponse = await sdk.prepareSendPayment({
    paymentRequest: { type: 'input', input: destination },
    amount: BigInt(amountSats),
  });
  return { prepareResponse, feeSats: feeFromPrepare(prepareResponse) };
}

/**
 * Prepare a TOKEN send (BTKN, e.g. USDB) to a Spark address or Spark invoice.
 * amountBaseUnits is a bigint in the token's base units (USDB: 6 decimals).
 * conversionOptions (optional) pays the token amount by converting from BTC
 * on the fly (fromBitcoin) — or, with convertToBitcoin, pays a BTC payment
 * from token funds (amount/tokenIdentifier are then omitted per the SDK).
 *
 * @returns {{ prepareResponse: object, feeSats: number|null }}
 */
async function prepareToken(sdk, destination, amountBaseUnits, tokenIdentifier, conversionOptions) {
  const request = {
    paymentRequest: { type: 'input', input: destination },
  };
  if (amountBaseUnits !== undefined && amountBaseUnits !== null) request.amount = BigInt(amountBaseUnits);
  if (tokenIdentifier !== undefined && tokenIdentifier !== null) request.tokenIdentifier = tokenIdentifier;
  if (conversionOptions !== undefined && conversionOptions !== null) request.conversionOptions = conversionOptions;
  const prepareResponse = await sdk.prepareSendPayment(request);
  return { prepareResponse, feeSats: feeFromPrepare(prepareResponse) };
}

/**
 * Extract the conversion estimate (if any) from a prepare response into a
 * JSON-safe shape. amountIn is in the SOURCE asset (sats for fromBitcoin,
 * token base units for toBitcoin); amountOut in the TARGET asset.
 */
function conversionEstimateFrom(prepareResponse) {
  const est = prepareResponse && prepareResponse.conversionEstimate;
  if (!est) return null;
  return {
    amountIn: String(est.amountIn),
    amountOut: String(est.amountOut),
    fee: String(est.fee),
    conversionType: est.options && est.options.conversionType ? est.options.conversionType.type : undefined,
  };
}

/**
 * THE shared dispatch-and-settle seam — the single place for the payment
 * policy every spark-send branch must carry (BTC, token, and both conversion
 * directions). This exists because the branches used to inline this policy and
 * drifted: PR #10's review found the token branch releasing reservations on
 * outcome-unknown errors and ignoring terminal-failure semantics that the BTC
 * path had already hardened.
 *
 * Policy (test-pinned — see the budget-integration describes in spark.test.js):
 *   - the dispatch closure rejects with ANY value after dispatch → outcome is
 *     UNKNOWN: keep the reservation (fail-closed, 25h prune) and warn, rethrow.
 *     Only an explicit terminal failure releases it — never a rejection.
 *   - terminal failed status (via the hardened isFailedStatus) → release the
 *     reservation, process.exitCode = 1, warn.
 *   - otherwise → settle the sats spend when one applies (settle.sats), via
 *     settleSpend (warns on accounting failure, never throws; a null
 *     reservationId records directly — the forced-send path).
 *
 * @param {() => Promise} dispatch  closure performing the SDK call
 *   (sdk.sendPayment / sdk.lnurlPay).
 * @param {object} [opts]
 * @param {string|null} [opts.reservationId]
 * @param {{sats: number}|null} [opts.settle]  the applicable sats spend, or null
 *   when no sats move (plain token sends, --from-token conversions).
 * @param {string} [opts.command]
 * @param {string|null} [opts.domain]
 * @returns {Promise<{ payment: object, status: string|object, paymentId: string|null }>}
 *   `status` is the SDK's payment status VERBATIM — a string per the pinned
 *   SDK union ('completed'|'pending'|'failed'); the hardened isFailedStatus
 *   additionally tolerates tagged-object statuses ({type:'failed'}), so the
 *   returned union includes those when the SDK emits them. Branch via
 *   isFailedStatus, never on a string assumption.
 */
/**
 * Render a payment status for diagnostics: a tagged-object status
 * ({type:'failed'} — the shape isFailedStatus tolerates) renders as its
 * type, other objects as JSON, so stderr never shows '[object Object]'.
 *
 * @param {string|object} status
 * @returns {string}
 */
function displayStatus(status) {
  if (status !== null && typeof status === 'object') {
    return status.type !== undefined ? String(status.type) : JSON.stringify(status);
  }
  return String(status);
}

async function dispatchAndSettle(
  dispatch,
  { reservationId = null, settle = null, command = 'spark-send', domain = null } = {},
) {
  let result;
  try {
    result = await dispatch();
  } catch (e) {
    if (reservationId) {
      console.error(
        'Warning: payment outcome is unknown after this error, so the budget reservation stays in place ' +
          '(fail-closed, auto-cleared by the 25h prune). Inspect `spark-transactions` before retrying.',
      );
    }
    throw e;
  }
  const payment = result && result.payment ? result.payment : result;
  const status = (payment && payment.status) || 'SUBMITTED';

  if (!isFailedStatus(status)) {
    // Only successful/pending payments are logged — same rule as the custodial
    // pay commands. settleSpend warns — never throws — on accounting failure.
    if (settle !== null) {
      settleSpend({ reservationId, sats: settle.sats, command, domain });
    }
  } else if (reservationId) {
    // Explicit terminal failure — the payment did not happen, free the budget.
    releaseSpend(reservationId);
  }

  // The SDK resolves rather than throws for a payment that FAILED, so exiting
  // 0 would tell every caller — shell, CI, agent — that a payment which did
  // not happen succeeded. `pending` is not a failure: it keeps a zero exit.
  if (isFailedStatus(status)) {
    process.exitCode = 1;
    console.error(`Payment reported status '${displayStatus(status)}'. Exiting non-zero.`);
  }
  return { payment, status, paymentId: (payment && (payment.id || payment.paymentHash)) || null };
}

/**
 * Does this SDK payment status mean the payment did not go through?
 *
 * Compared case-insensitively because the SDK's casing has moved between
 * versions (`failed` vs `FAILED`), and a casing mismatch here would silently
 * restore the exit-0-on-failure bug.
 *
 * @param {string} status
 * @returns {boolean}
 */
function isFailedStatus(status) {
  // Accept both a plain string and a tagged variant ({ type: 'failed' }), which
  // is how the SDK models several other enums and could plausibly become the
  // shape here. `String({...})` is "[object Object]", which would quietly
  // reinstate exit-0-on-failure.
  const value = status && typeof status === 'object' ? status.type || status.status : status;
  return String(value || '').toLowerCase() === 'failed';
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args.destination || args.amountSats === null) {
    console.error(
      'Usage: node spark_send.js <destination> <amount_sats> [--dry-run] [--force] [--network mainnet|regtest]\n' +
        '       node spark_send.js <spark-address-or-invoice> <amount> --token usdb|<identifier> [--base-units]\n' +
        '                                        [--from-btc] [--from-token usdb|<identifier>] [--slippage-bps <n>]',
    );
    process.exit(1);
  }

  const tokenMode = args.token !== null || args.fromBtc || args.fromToken !== null;
  // FT9: a dry run only PREPARES — the "spends real bitcoin" warning was
  // misleading there. A real send keeps the warning unchanged.
  console.error(
    args.dryRun
      ? 'DRY RUN: prepares the payment only — nothing is signed or sent.'
      : tokenMode
        ? '⚠️  NON-CUSTODIAL TOKEN SEND: this signs a transaction with your account seed and moves real funds (token and/or BTC).'
        : '⚠️  NON-CUSTODIAL SEND: this signs a transaction with your account seed and spends real bitcoin.',
  );

  const { sdk, disconnect } = await connect({ network: args.network });
  try {
    // Resolve token identifiers once (usdb alias → per-network identifier).
    const tokenIdentifier = args.token !== null ? resolveTokenIdentifier(args.token, args.network) : null;
    const fromTokenIdentifier = args.fromToken !== null ? resolveTokenIdentifier(args.fromToken, args.network) : null;
    if (args.token !== null && args.fromToken !== null) {
      throw new Error('--token and --from-token are mutually exclusive (a payment converts in ONE direction).');
    }
    if (args.fromBtc && args.fromToken !== null) {
      throw new Error('--from-btc and --from-token are mutually exclusive.');
    }
    if (args.fromBtc && args.token === null) {
      throw new Error('--from-btc requires --token (the token the payment is denominated in).');
    }
    if (args.fromToken !== null && args.token !== null) {
      throw new Error('--from-token pays a BTC payment — do not also pass --token.');
    }

    // 1. Classify the destination.
    const parsed = await sdk.parse(args.destination);
    // Exhaustive classification: anything the SDK recognizes but this skill
    // does not pay to (on-chain, BOLT-12, cross-chain, ...) is rejected here,
    // before any prepare or budget interaction.
    const dest = classifyDestination(parsed);
    console.error(
      `Destination classified as ${
        dest.type === 'lnurl'
          ? 'Lightning Address / LNURL-pay'
          : dest.type === 'spark'
            ? 'Spark address / Spark invoice'
            : 'BOLT-11 invoice'
      }.`,
    );

    // ── Token / conversion branch ──
    if (tokenMode) {
      if (args.token !== null) {
        // Sending tokens (optionally paid via --from-btc conversion).
        if (dest.type !== 'spark') {
          throw new Error(
            'Token sends require a Spark address or Spark invoice destination (on-chain, BOLT-11 and LNURL are BTC-only).',
          );
        }
        // If the destination is a Spark INVOICE with its own token/amount,
        // passing ours must match; the SDK validates that.
        let amountBaseUnits;
        if (args.baseUnits) {
          if (!/^\d+$/.test(String(args.amountSats))) {
            throw new Error('--base-units amount must be a non-negative integer');
          }
          amountBaseUnits = BigInt(args.amountSats);
        } else {
          const meta = await sdk.getTokensMetadata({ tokenIdentifiers: [tokenIdentifier] });
          const m = meta && meta.tokensMetadata && meta.tokensMetadata[0];
          if (!m) {
            throw new Error(`No metadata found for token ${tokenIdentifier} — use --base-units to skip the lookup.`);
          }
          console.error(`Token: ${m.name} (${m.ticker}), ${m.decimals} decimals.`);
          amountBaseUnits = parseTokenAmount(args.amountSats, m.decimals);
        }

        const conversionOptions = args.fromBtc
          ? { conversionType: { type: 'fromBitcoin' }, maxSlippageBps: args.slippageBps }
          : null;
        const { prepareResponse, feeSats } = await prepareToken(
          sdk,
          args.destination,
          amountBaseUnits,
          tokenIdentifier,
          conversionOptions,
        );
        const conversion = conversionEstimateFrom(prepareResponse);
        if (conversion) {
          console.error(
            `Conversion estimate: ${conversion.amountIn} source units → ${conversion.amountOut} target units (fee ${conversion.fee}).`,
          );
        }
        console.error(
          `Prepared token payment. Estimated fee: ${feeSats === null ? 'unknown' : `${feeSats} (token base units)`}.`,
        );

        if (args.dryRun) {
          console.log(
            JSON.stringify(
              {
                event: 'send_prepared',
                dryRun: true,
                destination: args.destination,
                destinationType: 'spark',
                tokenIdentifier,
                amountBaseUnits: String(amountBaseUnits),
                feeBaseUnits: feeSats,
                conversionEstimate: conversion,
                network: args.network,
              },
              null,
              2,
            ),
          );
          return;
        }

        // Budget: the sats budget is a SATS instrument. A plain token send
        // moves no sats (no reservation). A --from-btc send converts SATS
        // into the token to pay — the sats side is conversionEstimate.amountIn,
        // and THAT is what the budget must reserve. An absent, zero, or
        // unrepresentable estimate never silently disables enforcement: a
        // non-forced conversion REFUSES to dispatch rather than spend
        // unreserved sats (fail closed). --force skips the reservation,
        // same as forced BTC sends.
        let reservationId = null;
        let recordableSats = null;
        if (conversion) {
          const satsSide = Number(conversion.amountIn);
          if (Number.isSafeInteger(satsSide) && satsSide > 0) recordableSats = satsSide;
        }
        if (args.fromBtc && !args.force) {
          if (recordableSats === null) {
            throw new Error(
              'No usable conversion estimate (sats side) for --from-btc — refusing to dispatch a ' +
                'sats-consuming conversion without a budget reservation. Retry, or use --force to proceed unreserved.',
            );
          }
          const r = reserveBudget(
            { sats: recordableSats, command: 'spark-send', domain: null },
            { requireConfigured: false },
          );
          if (!r.allowed) {
            throw new Error(`Budget exceeded: ${r.reason} Use --force to override.`);
          }
          reservationId = r.id;
        }

        const { status, paymentId } = await dispatchAndSettle(() => sdk.sendPayment({ prepareResponse }), {
          reservationId,
          // Only a --from-btc conversion moves sats (the estimate's sats
          // side); plain token sends move none.
          settle: args.fromBtc && recordableSats !== null ? { sats: recordableSats } : null,
        });
        if (args.fromBtc && recordableSats === null && !isFailedStatus(status)) {
          console.error(
            'Warning: forced conversion dispatched with no usable estimate — the sats spend is unrecorded.',
          );
        }
        console.log(
          JSON.stringify(
            {
              event: 'send_result',
              status,
              destination: args.destination,
              destinationType: 'spark',
              tokenIdentifier,
              amountBaseUnits: String(amountBaseUnits),
              feeBaseUnits: feeSats,
              conversionEstimate: conversion,
              paymentId,
              network: args.network,
            },
            null,
            2,
          ),
        );
        return;
      }

      // --from-token: pay a BTC payment (BOLT-11) using token funds.
      if (dest.type !== 'bolt11') {
        throw new Error(
          '--from-token pays a BOLT-11 invoice from token funds — the destination must be a BTC invoice.',
        );
      }
      const conversionOptions = {
        conversionType: { type: 'toBitcoin', fromTokenIdentifier: fromTokenIdentifier },
        maxSlippageBps: args.slippageBps,
      };
      const { prepareResponse, feeSats } = await prepareToken(sdk, args.destination, null, null, conversionOptions);
      const conversion = conversionEstimateFrom(prepareResponse);

      // ── Amount binding ──
      // No amount is passed for a toBitcoin conversion, so the INVOICE's
      // BTC amount is what will actually be paid. The caller confirmed
      // args.amountSats — if the invoice disagrees, the confirmation was for
      // the wrong number: refuse, for dry-runs too (the next real run would
      // be based on the same wrong confirmation).
      const authoritativeSats = Number(prepareResponse && prepareResponse.amount);
      if (!Number.isSafeInteger(authoritativeSats) || authoritativeSats <= 0) {
        throw new Error(
          `Could not determine the invoice's BTC amount for --from-token (prepared amount: ${String(
            prepareResponse && prepareResponse.amount,
          )}) — refusing to convert tokens for an unknown spend.`,
        );
      }
      if (authoritativeSats !== Number(args.amountSats)) {
        throw new Error(
          `Amount mismatch: the invoice is for ${authoritativeSats} sats but ${args.amountSats} was supplied. ` +
            'Refusing to convert tokens for a different amount than confirmed — re-run with the invoice amount.',
        );
      }

      if (conversion) {
        console.error(
          `Conversion estimate: ${conversion.amountIn} token base units → ${conversion.amountOut} sats (fee ${conversion.fee}).`,
        );
      }
      console.error(`Prepared payment. Estimated routing fee: ${feeSats === null ? 'unknown' : `${feeSats} sats`}.`);

      if (args.dryRun) {
        console.log(
          JSON.stringify(
            {
              event: 'send_prepared',
              dryRun: true,
              destination: args.destination,
              destinationType: 'bolt11',
              amountSats: authoritativeSats,
              feeSats,
              fromTokenIdentifier,
              conversionEstimate: conversion,
              network: args.network,
            },
            null,
            2,
          ),
        );
        return;
      }

      // No sats leave the wallet (tokens are the source asset) — the sats
      // budget does not apply; documented in SKILL.md. The seam still guards
      // the outcome-unknown warn (a no-op here: nothing is reserved).
      const { status, paymentId } = await dispatchAndSettle(() => sdk.sendPayment({ prepareResponse }), {
        settle: null,
      });
      console.log(
        JSON.stringify(
          {
            event: 'send_result',
            status,
            destination: args.destination,
            destinationType: 'bolt11',
            amountSats: authoritativeSats,
            feeSats,
            fromTokenIdentifier,
            conversionEstimate: conversion,
            paymentId,
            network: args.network,
          },
          null,
          2,
        ),
      );
      return;
    }

    // ── BTC path (unchanged) ──

    // 2. Prepare (resolves fees) via the matching path.
    const { prepareResponse, feeSats } =
      dest.type === 'lnurl'
        ? await prepareLnurl(sdk, dest.parsed, args.amountSats)
        : await prepareBolt(sdk, args.destination, args.amountSats);

    console.error(`Prepared payment. Estimated fee: ${feeSats === null ? 'unknown' : `${feeSats} sats`}.`);

    if (args.dryRun) {
      console.log(
        JSON.stringify(
          {
            event: 'send_prepared',
            dryRun: true,
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
      return;
    }

    // ── Budget reservation ──
    // The limit decision AND the reservation append happen under one lock, so
    // two concurrent sends can never both pass the same remaining budget. Same
    // treatment as the custodial one-shot payments (pay-invoice & co): the
    // budget is enforced when configured, but an unconfigured budget must not
    // block an explicitly user-initiated payment, so opt out of the fail-closed
    // default that guards autonomous L402 auto-pay. --force overrides.
    // Budgets count the payment PRINCIPAL, not the routing fee — same
    // convention as the custodial pay commands.
    let reservationId = null;
    if (!args.force) {
      const reservation = reserveBudget(
        { sats: args.amountSats, command: 'spark-send', domain: null },
        { requireConfigured: false },
      );
      if (!reservation.allowed) {
        throw new Error(`Budget exceeded: ${reservation.reason} Use --force to override.`);
      }
      reservationId = reservation.id; // null when no budget is configured
    }

    // 3. Send (signs locally) via the matching path, through the shared
    // dispatch-and-settle seam: outcome-unknown keeps the reservation
    // (fail-closed), terminal failure releases it + exits non-zero, and
    // successful/pending sends settle the sats spend.
    const { status, paymentId } = await dispatchAndSettle(
      () => (dest.type === 'lnurl' ? sdk.lnurlPay({ prepareResponse }) : sdk.sendPayment({ prepareResponse })),
      { reservationId, settle: { sats: args.amountSats } },
    );

    console.log(
      JSON.stringify(
        {
          event: 'send_result',
          status,
          destination: args.destination,
          destinationType: dest.type,
          amountSats: args.amountSats,
          feeSats,
          paymentId,
          network: args.network,
        },
        null,
        2,
      ),
    );
  } finally {
    // Cleanup must never mask the payment outcome: a disconnect rejection
    // after dispatch would otherwise REPLACE the result (and its exit code)
    // with an error, inviting a retry of an already-settled payment.
    try {
      await disconnect();
    } catch (e) {
      // safeErrorDetail: even the warning must not throw (a throwing getter on
      // a fake/alternate connector's error would otherwise mask the outcome).
      console.error(`Warning: Spark disconnect failed (payment result is unaffected): ${safeErrorDetail(e)}`);
    }
  }
}

if (require.main === module) {
  main()
    .then(async () => {
      // The Breez SDK keeps event-loop handles open after disconnect; force a
      // clean exit so the command returns promptly for the caller/agent.
      // Drain stdout first — process.exit() can truncate a pending write when
      // stdout is a pipe, and the JSON result is this command's whole product.
      // Preserves any exit code main() set (e.g. 1 for a failed payment).
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

module.exports = {
  main,
  parseArgs,
  feeFromPrepare,
  isLnurlPayInput,
  lnurlPayRequestFrom,
  isFailedStatus,
  classifyDestination,
  prepareLnurl,
  prepareBolt,
  prepareToken,
  conversionEstimateFrom,
  ARG_OPTIONS: SPARK_SEND_OPTIONS,
};
