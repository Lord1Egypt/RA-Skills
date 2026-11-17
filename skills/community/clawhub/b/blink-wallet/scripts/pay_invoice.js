#!/usr/bin/env node
/**
 * Blink Wallet - Pay Lightning Invoice
 *
 * Usage: node pay_invoice.js <bolt11_invoice> [--wallet BTC|USD] [--max-amount <sats>] [--dry-run] [--force]
 *
 * Pays a BOLT-11 Lightning invoice from the BTC or USD wallet.
 * Automatically resolves the wallet ID from the account.
 *
 * Arguments:
 *   bolt11_invoice  - Required. The BOLT-11 payment request string (lnbc...).
 *   --wallet        - Optional. Wallet to pay from: BTC (default) or USD.
 *   --max-amount    - Optional. Refuse (before any API call) if the invoice
 *                     charges more than N sats. --force does not bypass it.
 *
 * Environment:
 *   BLINK_API_KEY  - Required. Blink API key (format: blink_...)
 *   BLINK_API_URL  - Optional. Override API endpoint (default: https://api.blink.sv/graphql)
 *
 * Dependencies: None (uses Node.js built-in fetch)
 *
 * CAUTION: This sends real bitcoin. The API key must have Write scope.
 */

const {
  getApiKey,
  getApiUrl,
  graphqlRequest,
  getWallet,
  formatBalance,
  parseWalletArg,
  normalizeInvoice,
  warnIfNotBolt11,
  MUTATION_TIMEOUT_MS,
  WALLET_ARG_OPTIONS,
} = require('./_blink_client');

const { reserveBudget, settleSpend, releaseSpend } = require('./_budget');
const { budgetChargeFromInvoice } = require('./l402_discover');

const PAY_INVOICE_MUTATION = `
  mutation LnInvoicePaymentSend($input: LnInvoicePaymentInput!) {
    lnInvoicePaymentSend(input: $input) {
      status
      errors {
        code
        message
        path
      }
    }
  }
`;

async function main() {
  const { walletCurrency, dryRun, force, maxAmount, remaining } = parseWalletArg(process.argv.slice(2), {
    maxPositionals: 1,
  });
  const rawInvoice = remaining[0];

  if (!rawInvoice) {
    console.error(
      'Usage: node pay_invoice.js <bolt11_invoice> [--wallet BTC|USD] [--max-amount <sats>] [--dry-run] [--force]',
    );
    process.exit(1);
  }

  const paymentRequest = normalizeInvoice(rawInvoice);
  warnIfNotBolt11(paymentRequest);

  // ── Amount ceiling (--max-amount) ──
  // ClawHub 3.0.2 scan (concern): the shared parser accepted --max-amount and
  // this script discarded it, so the ceiling was silently ignored. Enforced
  // here BEFORE any API call, on dry-run too, and NOT bypassed by --force. The
  // charge is the budget's conservative one (ceil, ≥ 1 sat). An amount that
  // cannot be decoded cannot be bounded, so a requested ceiling fails closed.
  const charge = budgetChargeFromInvoice(paymentRequest);
  if (maxAmount !== null) {
    if (charge.budgetSats === null) {
      throw new Error(
        `Refusing to pay: cannot enforce --max-amount ${maxAmount} because the invoice amount could not be decoded.`,
      );
    }
    if (charge.budgetSats > maxAmount) {
      throw new Error(`Invoice amount ${charge.budgetSats} sats exceeds --max-amount ceiling of ${maxAmount} sats.`);
    }
  }

  const apiKey = getApiKey();
  const apiUrl = getApiUrl();

  // Resolve wallet (BTC or USD)
  const wallet = await getWallet({ apiKey, apiUrl, currency: walletCurrency });

  console.error(`Using ${walletCurrency} wallet ${wallet.id} (balance: ${formatBalance(wallet)})`);

  // ── Dry-run: resolve everything, show details, exit without sending ──
  if (dryRun) {
    console.error('[DRY RUN] Would send payment — no funds will be transferred.');
    const output = {
      dryRun: true,
      paymentRequest,
      walletId: wallet.id,
      walletCurrency,
      balance: wallet.balance,
    };
    if (walletCurrency === 'USD') {
      output.balanceFormatted = `$${(wallet.balance / 100).toFixed(2)}`;
    }
    console.log(JSON.stringify(output, null, 2));
    return;
  }

  // ── Balance check for BTC wallet ──
  // For pay_invoice we don't decode the BOLT-11 amount, so we can only warn
  // if the wallet is completely empty (0 sats). The API will reject if
  // insufficient, but this catches the obvious case early.
  if (!force && walletCurrency === 'BTC' && wallet.balance === 0) {
    throw new Error(`Insufficient balance: BTC wallet has 0 sats. Use --force to attempt anyway.`);
  }

  // ── Budget reservation ──
  // The limit decision AND the reservation append happen under one lock, so
  // two concurrent payments can never both pass the same remaining budget.
  // The amount CHARGED to the budget: null when undecodable (budget tracking
  // is skipped then — the API enforces wallet limits for those), otherwise
  // max(1, ceil(msats/1000)). Any positive decodable amount charges at least
  // 1 sat, so explicit payments can never move funds untracked.
  const invoiceSats = charge.budgetSats;
  if (invoiceSats !== null && charge.msats !== null && charge.msats % 1000 !== 0) {
    console.error(`Note: budget charges ${invoiceSats} sats conservatively for this fractional/sub-satoshi invoice.`);
  }
  let reservationId = null;
  if (invoiceSats !== null && !force) {
    // Explicitly user-initiated payment: an unconfigured budget must not block
    // it, so opt out of the fail-closed default that guards autonomous spending.
    const reservation = reserveBudget(
      { sats: invoiceSats, command: 'pay-invoice', domain: null },
      { requireConfigured: false },
    );
    if (!reservation.allowed) {
      throw new Error(`Budget exceeded: ${reservation.reason} Use --force to override.`);
    }
    reservationId = reservation.id;
  }

  const input = {
    walletId: wallet.id,
    paymentRequest,
  };

  let data;
  try {
    data = await graphqlRequest({
      query: PAY_INVOICE_MUTATION,
      variables: { input },
      apiKey,
      apiUrl,
      timeoutMs: MUTATION_TIMEOUT_MS,
    });
  } catch (e) {
    // Outcome-unknown after dispatch (timeout, lost response, transport
    // reset): the payment may still settle, so the reservation STAYS —
    // freeing it would let a retry double-spend the same budget window.
    if (reservationId) {
      console.error(
        `Warning: payment outcome is unknown after this error, so the budget reservation stays in place ` +
          `(fail-closed, auto-cleared by the 25h prune). Inspect \`transactions\` before retrying.`,
      );
    }
    throw e;
  }
  const result = data.lnInvoicePaymentSend;

  if (result.errors && result.errors.length > 0) {
    // Explicit server-side rejection — nothing moved; the budget is freed.
    const isSelfPay = result.errors.some(
      (e) =>
        (e.code && e.code.toString().toUpperCase().includes('CANT_PAY_SELF')) ||
        (e.message && e.message.toLowerCase().includes('self')),
    );
    if (isSelfPay) {
      releaseSpend(reservationId);
      throw new Error(
        'Cannot pay your own invoice (CANT_PAY_SELF). ' +
          'L402 round-trip testing requires a second Blink account or a separate wallet.',
      );
    }
    const errMsg = result.errors.map((e) => `${e.message}${e.code ? ` [${e.code}]` : ''}`).join(', ');
    releaseSpend(reservationId);
    throw new Error(`Payment failed: ${errMsg}`);
  }

  const output = {
    status: result.status,
    walletId: wallet.id,
    walletCurrency,
    balanceBefore: wallet.balance,
  };

  if (walletCurrency === 'USD') {
    output.balanceBeforeFormatted = `$${(wallet.balance / 100).toFixed(2)}`;
  }

  if (result.status === 'SUCCESS') {
    console.error('Payment successful!');
    if (invoiceSats !== null) {
      settleSpend({ reservationId, sats: invoiceSats, command: 'pay-invoice', domain: null });
    }
  } else if (result.status === 'PENDING') {
    console.error('Payment is pending...');
    if (invoiceSats !== null) {
      settleSpend({ reservationId, sats: invoiceSats, command: 'pay-invoice', domain: null });
    }
  } else if (result.status === 'ALREADY_PAID') {
    console.error('Invoice was already paid.');
    releaseSpend(reservationId);
  } else {
    console.error(`Payment status: ${result.status}`);
    releaseSpend(reservationId);
  }

  console.log(JSON.stringify(output, null, 2));
}

if (require.main === module) {
  main().catch((e) => {
    console.error('Error:', e.message);
    process.exit(1);
  });
}

module.exports = { main, ARG_OPTIONS: WALLET_ARG_OPTIONS };
