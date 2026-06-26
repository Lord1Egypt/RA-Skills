#!/usr/bin/env node
/**
 * withdraw.js <amount_usdc> [--account N] [--confirmed]
 *
 * Withdraws USDC from Hyperliquid L1 -> Arbitrum One.
 * Funds arrive at the same wallet address on Arbitrum within ~5 minutes.
 *
 * Without --confirmed: preview only (shows balance, amount, fee).
 * With    --confirmed: executes the withdrawal.
 *
 * Fee: 1 USDC deducted by the bridge (no ETH needed).
 * Minimum withdrawal: 2 USDC (after the 1 USDC fee, at least 1 USDC arrives).
 */

import { loadConfig } from './lib/config.js';
import { createSigner } from './lib/signer.js';
import { createTransport, createInfoClient, createExchangeClient } from './lib/hl-client.js';

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const WITHDRAWAL_FEE_USDC = 1.0;
const MIN_WITHDRAW_USDC = 2.0; // ensures at least 1 USDC arrives after fee

// ---------------------------------------------------------------------------
// CLI argument parsing
// ---------------------------------------------------------------------------

function extractAccount(argv) {
  const i = argv.indexOf('--account');
  if (i === -1) return { account: undefined, rest: argv };
  const raw = argv[i + 1];
  const v = parseInt(raw, 10);
  if (Number.isNaN(v) || v < 0 || String(v) !== raw) {
    stderr({ error: '--account must be a non-negative integer' });
    process.exit(1);
  }
  return { account: v, rest: [...argv.slice(0, i), ...argv.slice(i + 2)] };
}

function stdout(obj) { process.stdout.write(JSON.stringify(obj) + '\n'); }
function stderr(obj) { process.stderr.write(JSON.stringify(obj) + '\n'); }

const { account: accountIdx, rest: cleanArgs } = extractAccount(process.argv.slice(2));
const confirmed = cleanArgs.includes('--confirmed');
const positional = cleanArgs.filter(a => !a.startsWith('--'));

const amountArg = positional[0];
if (!amountArg) {
  stderr({ error: 'Usage: withdraw.js <amount_usdc> [--account N] [--confirmed]' });
  process.exit(1);
}

// Reject scientific notation and extra-precision strings early -- the SDK's
// UnsignedDecimal regex only accepts plain decimals like "5" or "5.5".
if (!/^\d+(\.\d+)?$/.test(amountArg.trim())) {
  stderr({ error: `Amount must be a plain decimal (e.g. "50" or "50.5"), got "${amountArg}"` });
  process.exit(1);
}
const amount = parseFloat(amountArg);
if (!isFinite(amount) || amount <= 0) {
  stderr({ error: `Invalid amount: "${amountArg}". Must be a positive number.` });
  process.exit(1);
}

if (amount < MIN_WITHDRAW_USDC) {
  stderr({
    error: `Minimum withdrawal is ${MIN_WITHDRAW_USDC} USDC. `
      + `A ${WITHDRAWAL_FEE_USDC} USDC bridge fee is deducted; amounts below the minimum leave nothing to receive.`,
  });
  process.exit(1);
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

try {
  const cfg = loadConfig();
  const wallet = await createSigner(cfg, null, { accountIndex: accountIdx });
  const address = await wallet.getAddress();

  const transport = createTransport(cfg);
  const info = createInfoClient(transport);

  const spotState = await info.spotClearinghouseState({ user: address });

  // Spot USDC: total = perp margin + free balance; hold = perp margin locked
  const spotUsdc = spotState.balances.find(b => b.coin === 'USDC');
  const spotTotal = spotUsdc ? parseFloat(spotUsdc.total) : 0;
  const spotHold = spotUsdc ? parseFloat(spotUsdc.hold) : 0;
  // True withdrawable = spot free balance (not locked as perp margin); clamped to 0
  const withdrawable = Math.max(0, spotTotal - spotHold);
  const marginLocked = spotHold;

  if (withdrawable < amount) {
    stderr({
      error: `Insufficient withdrawable balance. `
        + `Withdrawable: ${withdrawable.toFixed(2)} USDC, requested: ${amount} USDC.`,
      hint: marginLocked > 0
        ? `${marginLocked.toFixed(2)} USDC is locked as perp margin. Close positions to free up more.`
        : undefined,
    });
    process.exit(1);
  }

  // Confirmation thresholds from hyperliquid.yaml risk section
  const risk = cfg?.yaml?.risk ?? {};
  const toFinitePos = (v, fb) => (typeof v === 'number' && isFinite(v) && v > 0 ? v : fb);
  const confirmThreshold = toFinitePos(risk.confirm_trade_usd, 100);
  const largeThreshold = toFinitePos(risk.large_trade_usd, 1000);

  const netAmount = amount - WITHDRAWAL_FEE_USDC;

  stdout({
    preview: true,
    action: 'Withdraw USDC -> Arbitrum One',
    from_hl_address: address,
    to_arb_address: address,
    amount_usdc: amount,
    fee_usdc: WITHDRAWAL_FEE_USDC,
    net_received_usdc: netAmount,
    usdc_balance_hl: spotTotal,
    withdrawable_balance: withdrawable,
    margin_locked: marginLocked,
    network: 'Hyperliquid L1',
    destination: 'Arbitrum One',
    estimated_credit_time: '~5 minutes',
    requiresConfirm: amount >= confirmThreshold,
    requiresDoubleConfirm: amount >= largeThreshold,
  });

  if (!confirmed) process.exit(0);

  // Execute withdrawal
  const exchange = createExchangeClient(transport, wallet);
  const result = await exchange.withdraw3({
    destination: address,
    amount: amountArg,
  });

  stdout({
    type: 'confirmed',
    status: 'success',
    amount_usdc: amount,
    fee_usdc: WITHDRAWAL_FEE_USDC,
    net_received_usdc: netAmount,
    destination: address,
    note: `USDC will arrive on Arbitrum One within ~5 minutes. Check with: node balance.js spot`,
    raw: result,
  });

  process.exit(0);
} catch (err) {
  stderr({ error: err.message });
  process.exit(1);
}
