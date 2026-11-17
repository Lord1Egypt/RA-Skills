#!/usr/bin/env node
/**
 * Blink Wallet - L402 Spark payment leg
 *
 * Pays a BOLT-11 invoice from a self-custodial (Spark) account via the Breez
 * Spark SDK — the payment backend for `l402-pay --spark`. No Blink API
 * involvement: the SDK signs locally with the seed, and the preimage comes
 * back in the settled payment's HTLC details (details.type === 'lightning'
 * → htlcDetails.preimage, present once the HTLC status is preimageShared).
 *
 * Failure stages matter to the caller's reservation semantics:
 *   - connect/prepare failures happen BEFORE dispatch (nothing moved — the
 *     caller releases the budget reservation), so they are rethrown untagged.
 *   - sendPayment failures happen AFTER dispatch (outcome unknown — the
 *     payment may still settle). They are wrapped in a dedicated typed Error
 *     (code SPARK_DISPATCH_OUTCOME_UNKNOWN, stage 'dispatch', original kept
 *     as `cause`) so ANY rejection value — a string, a frozen or
 *     null-prototype object, a throwing Proxy — keeps the classification,
 *     and the caller KEEPS the reservation (fail-closed).
 */

const { connect, feeFromPrepare, safeErrorDetail } = require('./_spark_sdk');

/**
 * Race a promise against a wall-clock timeout. The underlying promise is NOT
 * cancelled (the SDK exposes no abort mechanism) — the race only bounds how
 * long the caller waits on it. The timer is always cleared so it can never
 * hold the event loop open past the race.
 *
 * @param {Promise} promise
 * @param {number} ms  non-negative budget
 * @param {string} label  for the timeout error message
 * @returns {Promise}
 */
function withTimeout(promise, ms, label) {
  let timer;
  return Promise.race([
    promise,
    new Promise((_, reject) => {
      timer = setTimeout(() => reject(new Error(`${label} timed out after ${ms}ms`)), ms);
    }),
  ]).finally(() => clearTimeout(timer));
}

/**
 * Documented ceiling for waitSeconds (1 hour). Keeps the deadline finite
 * (Number('9'.repeat(400)) is Infinity — an infinite deadline plus a stuck
 * payment would poll forever) and inside the range where Node timers behave.
 * Applied defensively here in addition to the CLI's own validation, because
 * this function is exported and must not trust its caller.
 */
const MAX_WAIT_SECONDS = 3600;

/**
 * Wrap a pre-dispatch rejection (connect / prepareSendPayment) in an owned
 * Error carrying the original value as `cause`. These are third-party Promise
 * boundaries: a rejection value of null/undefined (or anything non-object)
 * would otherwise reach the caller's `e.stage` property access and throw a
 * replacement TypeError before the reservation could be released — stranding
 * the allowance. The owned error always reads undefined for stage, so the
 * caller releases correctly for every rejection shape.
 */
function preDispatchError(stage, value) {
  const err = new Error(`Spark ${stage} failed (no payment dispatched): ${safeErrorDetail(value)}`, { cause: value });
  err.code = 'SPARK_PREPARE_FAILED';
  return err;
}

/**
 * Decode a sendPayment/getPayment result into the normalized vocabulary.
 *
 * @param {object} result  SDK result ({ payment } or the payment itself)
 * @returns {{ payment: object, status: string, preimage: string|null }}
 */
function decodePaymentResult(result) {
  const payment = result && result.payment ? result.payment : result;
  const rawStatus = String((payment && payment.status) || 'SUBMITTED');
  const lower = rawStatus.toLowerCase();

  let status;
  if (lower === 'completed' || lower === 'success') status = 'SUCCESS';
  else if (lower === 'pending' || lower === 'submitted') status = 'PENDING';
  else if (lower === 'failed' || lower === 'failure') status = 'FAILURE';
  else status = rawStatus; // unknown — preserved raw so the caller sees the truth

  let preimage = null;
  const details = payment && payment.details;
  if (details && details.type === 'lightning' && details.htlcDetails) {
    preimage = details.htlcDetails.preimage || null;
  }
  return { payment, status, preimage };
}

/**
 * Pay a BOLT-11 invoice from a Spark account.
 *
 * @param {string} invoice  BOLT-11 payment request (the L402 challenge invoice).
 * @param {object} [opts]
 * @param {string} [opts.network]  'mainnet' (default) or 'regtest'.
 * @param {number} [opts.waitSeconds]  How long to poll an in-flight (PENDING)
 *   payment for settlement before giving up. Default 60. 0 disables polling.
 *   Clamped to [0, 3600] defensively (non-finite/negative values disable the
 *   poll; anything above 1 hour is capped) — the exported boundary does not
 *   trust its caller.
 *   Spark settlement is asynchronous: sendPayment routinely resolves PENDING
 *   and the preimage arrives seconds later in htlcDetails (status
 *   preimageShared). Aborting on PENDING loses the payment — observed live:
 *   sats spent, budget debited, no L402 token captured.
 * @param {number} [opts.pollIntervalMs]  Poll cadence (default 3000).
 * @returns {Promise<{ payment: object, status: string, preimage: string|null, feeSats: number|null }>}
 *   status is NORMALIZED at this boundary, case-insensitively, onto the
 *   custodial vocabulary: the SDK's 'completed'/'pending'/'failed' (any
 *   casing) become 'SUCCESS'/'PENDING'/'FAILURE'; unknown statuses pass
 *   through raw. Callers must branch on these values only.
 */
async function payInvoiceViaSpark(invoice, { network, waitSeconds = 60, pollIntervalMs } = {}) {
  // Defensive clamp: a non-finite or non-positive interval would make the
  // settlement loop a non-terminating hot loop (0: the deadline is only
  // checked between iterations that never yield; negative/NaN: same class).
  // The caller validates its env-provided value, but this function is
  // exported — clamp at the boundary regardless of who calls it.
  const interval =
    pollIntervalMs !== undefined && Number.isFinite(pollIntervalMs) && pollIntervalMs > 0 ? pollIntervalMs : 3000;
  let sdk;
  let disconnect;
  try {
    ({ sdk, disconnect } = await connect({ network: network || process.env.SPARK_NETWORK || 'mainnet' }));
  } catch (e) {
    throw preDispatchError('connect', e);
  }
  try {
    // Prepare: fee resolution and validation. The invoice carries its own
    // amount — no `amount` is passed (a ceil-rounded value would not match
    // the invoice's millisats).
    let prepareResponse;
    try {
      prepareResponse = await sdk.prepareSendPayment({
        paymentRequest: { type: 'input', input: invoice },
      });
    } catch (e) {
      throw preDispatchError('prepareSendPayment', e);
    }
    const feeSats = feeFromPrepare(prepareResponse);

    let result;
    try {
      result = await sdk.sendPayment({ prepareResponse });
    } catch (e) {
      // Promises may reject with arbitrary values. A string or a
      // non-extensible object would silently drop an attached stage marker
      // (sloppy-mode no-op), and a null-prototype object or a Proxy with a
      // throwing trap cannot even be string-coerced. The typed error must be
      // constructed NO MATTER WHAT the rejected value is, or the caller would
      // misread a post-dispatch failure as pre-dispatch and free the budget.
      const err = new Error(`Spark payment failed after dispatch (outcome unknown): ${safeErrorDetail(e)}`, {
        cause: e,
      });
      err.code = 'SPARK_DISPATCH_OUTCOME_UNKNOWN';
      err.stage = 'dispatch'; // outcome unknown — the caller must keep the reservation
      throw err;
    }

    // The payment was dispatched; a poisoned resolved value (throwing getters
    // on payment/status/details) would otherwise escape untagged and the
    // caller would release the reservation. Decode failures after dispatch are
    // outcome-unknown, same class as a thrown dispatch error.
    let decoded;
    try {
      decoded = decodePaymentResult(result);
    } catch (e) {
      const err = new Error(
        `Spark payment result could not be decoded after dispatch (outcome unknown): ${safeErrorDetail(e)}`,
        { cause: e },
      );
      err.code = 'SPARK_DISPATCH_OUTCOME_UNKNOWN';
      err.stage = 'dispatch'; // outcome unknown — the caller must keep the reservation
      throw err;
    }

    // Spark settlement is asynchronous: PENDING here is NORMAL, not failure.
    // Poll getPayment until the payment reaches a terminal state or the wait
    // budget is spent — the preimage (the L402 token material) only appears
    // in htlcDetails once the HTLC reaches preimageShared.
    //
    // Order matters: the FIRST refresh runs IMMEDIATELY (review round 2: a
    // sleep-first loop burned a whole sub-interval wait --wait 1 with the
    // 3000ms default consumed the entire budget sleeping and performed zero
    // refreshes, reporting PENDING for an already-settled payment); later
    // iterations sleep between refreshes.
    //
    // The deadline is ABSOLUTE wall-clock (Date.now()), and every ingredient
    // is bounded by the REMAINING time: the sleeps, and each getPayment
    // refresh (raced against the remaining budget — the SDK exposes no
    // request timeout, and an unbounded await would let one stalled refresh
    // outlive --wait indefinitely). Expiry returns the last-known PENDING
    // result so the caller's fail-closed accounting and retry warning run.
    let { payment, status, preimage } = decoded;
    const deadlineMs = Math.max(0, Math.min(Number(waitSeconds) || 0, MAX_WAIT_SECONDS)) * 1000;
    const deadline = Date.now() + deadlineMs;
    let firstIteration = true;
    while (status === 'PENDING' && deadlineMs > 0 && Date.now() < deadline) {
      if (!firstIteration) {
        const remainingForSleep = deadline - Date.now();
        if (remainingForSleep <= 0) break;
        await new Promise((resolve) => setTimeout(resolve, Math.min(interval, remainingForSleep)));
      }
      firstIteration = false;
      const paymentId = payment && payment.id;
      if (!paymentId) break; // nothing to refresh — surface the PENDING truth
      const remaining = deadline - Date.now();
      if (remaining <= 0) break;
      try {
        const refreshed = await withTimeout(sdk.getPayment({ paymentId }), remaining, 'getPayment refresh');
        decoded = decodePaymentResult(refreshed);
        payment = decoded.payment;
        status = decoded.status;
        preimage = decoded.preimage;
      } catch {
        // Transient query failure or a bounded refresh timeout — keep
        // polling until the deadline; the payment itself is unaffected.
      }
    }

    return { payment, status, preimage, feeSats };
  } finally {
    // Cleanup must never mask the payment outcome: a disconnect rejection
    // after dispatch would otherwise REPLACE the successful result with an
    // untagged error, and the caller — reading it as a pre-dispatch failure —
    // would release the budget reservation after funds moved.
    try {
      await disconnect();
    } catch (e) {
      // safeErrorDetail: even the warning must not throw (a throwing getter on
      // a fake/alternate connector's error would otherwise replace the result).
      console.error(`Warning: Spark disconnect failed (payment result is unaffected): ${safeErrorDetail(e)}`);
    }
  }
}

if (require.main === module) {
  console.error('This module is a payment leg for l402-pay (use: blink l402-pay --spark).');
  process.exit(1);
}

module.exports = { payInvoiceViaSpark, MAX_WAIT_SECONDS };
