import { fileURLToPath } from 'url';
import { realpathSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';
import { ethers } from 'ethers';
import { loadConfig, resolveRpcUrl } from './lib/config.js';
import { createSigner } from './lib/signer.js';
import { createL2Client } from './lib/clob.js';
import { runTradeEnvCheck } from './setup.js';
import { extractTokenIds, resolveMarket } from './browse.js';
import { getSwapQuote, swapPolToUsdc } from './lib/swap.js';
import { polyGasOverrides } from './lib/gas.js';
import { confirm } from './lib/prompt.js';

const AUREHUB_DIR = join(homedir(), '.aurehub');
const ERC20_ABI  = ['function balanceOf(address) view returns (uint256)',
                    'function allowance(address,address) view returns (uint256)',
                    'function approve(address,uint256) returns (bool)'];
const ERC1155_ABI = ['function balanceOf(address,uint256) view returns (uint256)',
                     'function isApprovedForAll(address,address) view returns (bool)',
                     'function setApprovalForAll(address,bool)'];

// ── Exported pure helpers (tested) ───────────────────────────────────────────

export function getSafetyLevel(amount, safety) {
  if (amount >= safety.confirm_threshold_usd) return 'confirm';
  if (amount >= safety.warn_threshold_usd)    return 'warn';
  return 'proceed';
}

export function validateHardStops(amount, { usdceBalance, polBalance, marketActive, minOrderSize }) {
  if (!marketActive) throw new Error('Market is CLOSED — cannot trade.');
  if (amount < minOrderSize) throw new Error(`Amount $${amount} is below min order size $${minOrderSize}.`);
  if (usdceBalance < amount) throw new Error(`Insufficient USDC.e: have $${usdceBalance}, need $${amount}.`);
  if (polBalance < 0.01) throw new Error(`Insufficient POL gas: have ${polBalance} POL, need ≥ 0.01.`);
}

// ── Swap offer helper (exported for testing) ──────────────────────────────────

/**
 * Check USDC.e balance; if insufficient, offer to swap POL → USDC.e.
 * Returns: false (no swap needed), true (swapped), 'cancelled' (user declined).
 */
export async function checkAndSwapIfNeeded({
  amount, usdceBalance, polBalance, cfg, wallet, provider, confirmFn, dryRun = false,
}) {
  if (usdceBalance >= amount) return false;

  const target = amount * 1.10;
  const { polNeeded, rate } = await getSwapQuote({ usdceNeeded: target, provider, cfg });
  const polAmountMax = polNeeded.mul(102).div(100); // ×1.02 slippage
  const polAmountMaxF = parseFloat(ethers.utils.formatEther(polAmountMax));

  if (polBalance < polAmountMaxF + 0.05) {
    throw new Error(
      `Insufficient POL: have ${polBalance.toFixed(4)} POL, need ${polAmountMaxF.toFixed(4)} POL (swap) + 0.05 (gas reserve)`,
    );
  }

  console.log(`\n⚠️  Insufficient USDC.e: have $${usdceBalance.toFixed(2)}, need $${amount.toFixed(2)}`);
  console.log(`  A POL → USDC.e swap is required to proceed with this buy.`);
  console.log(`  Will swap ~${polAmountMaxF.toFixed(2)} POL → ~$${target.toFixed(2)} USDC.e (10% buffer + 2% slippage protection)`);
  console.log(`  Est. rate: 1 POL ≈ $${rate.toFixed(2)} USDC.e`);

  if (dryRun) {
    console.log(`  [DRY RUN] Swap would be executed here — skipped.`);
    return 'dry-run-swap';
  }

  const swapConfirmed = await confirmFn('Proceed with swap and continue buy? (yes/no):');
  if (!swapConfirmed) {
    console.log('Swap declined. Buy cancelled — insufficient USDC.e to proceed.');
    return 'cancelled';
  }

  const received = await swapPolToUsdc({ polAmountMax, usdceTarget: target, cfg, wallet, provider });
  console.log(`✅ Swap completed: received $${received} USDC.e. Proceeding with buy...`);
  return true;
}

// ── Post-submission fill verification (exported for testing) ─────────────────

/**
 * After a network error during postOrder, query recent trades to determine if
 * the order actually filled. Returns the matching trade object, or null if not
 * found (caller should treat the fill status as unknown and warn before retry).
 *
 * @param {object} client   - ClobClient with getTrades
 * @param {string} tokenID  - token being traded
 * @param {string} makerAddress - wallet address
 * @param {number} [windowSec=120] - look-back window in seconds
 */
export async function checkRecentFill(client, tokenID, makerAddress, windowSec = 120) {
  try {
    const trades = await client.getTrades(
      { maker_address: makerAddress, asset_id: tokenID },
      true, // first page only — recent fills appear first
    );
    const cutoff = Math.floor(Date.now() / 1000) - windowSec;
    return trades.find(t => {
      const ts = parseInt(t.timestamp ?? t.match_time ?? '0', 10);
      return ts >= cutoff;
    }) ?? null;
  } catch {
    return null; // network also unavailable — conservative fallback
  }
}

// ── Buy flow ──────────────────────────────────────────────────────────────────

export async function buy({ market, side, amount, cfg, provider, wallet, dryRun = false }) {
  if (side !== 'YES' && side !== 'NO') throw new Error(`Invalid side "${side}": must be YES or NO`);
  if (!Number.isFinite(amount) || amount <= 0 || amount > 1_000_000) throw new Error(`Invalid amount: ${amount}`);

  const { Side, OrderType } = await import('@polymarket/clob-client');
  const client = await createL2Client(cfg, wallet, join(AUREHUB_DIR, '.polymarket_clob'));

  const ids = extractTokenIds(market);
  const tokenID = ids[side];
  if (!tokenID) throw new Error(`No ${side} token ID found for this market.`);

  const negRisk = await client.getNegRisk(tokenID);
  const contracts = cfg.yaml?.contracts ?? {};
  const spender = negRisk
    ? (contracts.neg_risk_exchange ?? '0xC5d563A36AE78145C45a50134d48A1215220f80a')
    : (contracts.ctf_exchange      ?? '0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E');
  const usdceAddr = contracts.usdc_e ?? '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174';
  if (!ethers.utils.isAddress(spender))   throw new Error(`Invalid contract address in config: ${negRisk ? 'neg_risk_exchange' : 'ctf_exchange'} = "${spender}"`);
  if (!ethers.utils.isAddress(usdceAddr)) throw new Error(`Invalid contract address in config: usdc_e = "${usdceAddr}"`);

  // Preview
  const tickSize = await client.getTickSize(tokenID);
  const ob = await client.getOrderBook(tokenID);
  // Polymarket sorts asks descending (worst first), best ask is last
  const bestAsk = parseFloat(ob.asks?.at(-1)?.price ?? '0.5');
  const estPrice = bestAsk * 1.01;
  const estShares = (amount / estPrice).toFixed(2);
  console.log(`\nPreview:`);
  console.log(`  Spending:       $${amount} USDC.e`);
  if (!ob.asks?.at(-1)) {
    console.log(`  Est. price:     ~$0.50/share ⚠️  (no asks in orderbook — estimate may be inaccurate)`);
  } else {
    console.log(`  Est. price:     ~$${estPrice.toFixed(4)}/share (market order — actual fill may differ)`);
  }
  console.log(`  Est. shares:    ~${estShares}`);

  // Hard stops — part 1: market and size (always run)
  const minOrderSize = parseFloat(market.minimum_order_size ?? market.orderMinSize ?? market.min_incentive_size ?? market.minIncentiveSize ?? '0');
  if (!market.active) throw new Error('Market is CLOSED — cannot trade.');
  if (amount < minOrderSize) throw new Error(`Amount $${amount} is below min order size $${minOrderSize}.`);

  // Balance checks
  const usdce = new ethers.Contract(usdceAddr, ERC20_ABI, provider);
  const usdceRaw = await usdce.balanceOf(wallet.address);
  const polRaw = await provider.getBalance(wallet.address);
  const usdceBalance = parseFloat(ethers.utils.formatUnits(usdceRaw, 6));
  const polBalance = parseFloat(ethers.utils.formatEther(polRaw));

  // Swap offer if USDC.e insufficient
  const swapResult = await checkAndSwapIfNeeded({
    amount, usdceBalance, polBalance, cfg, wallet, provider,
    confirmFn: confirm,
    dryRun,
  });
  if (swapResult === 'cancelled') return;

  // Re-check USDC.e only after a real swap (not dry-run-swap)
  if (swapResult === true) {
    const usdceRawPost = await usdce.balanceOf(wallet.address);
    const usdcePost = parseFloat(ethers.utils.formatUnits(usdceRawPost, 6));
    if (usdcePost < amount) throw new Error('Swap completed but USDC.e balance still insufficient.');
  }

  // Hard stops — part 2: POL gas check (re-fetch balance after potential swap)
  const polRawPost = await provider.getBalance(wallet.address);
  const polBalancePost = parseFloat(ethers.utils.formatEther(polRawPost));
  if (polBalancePost < 0.01) throw new Error(`Insufficient POL gas: have ${polBalancePost} POL, need ≥ 0.01.`);

  // Safety gates — skipped in dry-run
  if (!dryRun) {
    const safety = cfg.yaml?.safety ?? { warn_threshold_usd: 50, confirm_threshold_usd: 500 };
    const level = getSafetyLevel(amount, safety);
    if (level === 'warn') {
      if (!await confirm(`⚠️  Buying ${side} at ~$${estPrice.toFixed(4)} for $${amount}. Confirm? (yes/no):`)) { console.log('Cancelled.'); return; }
    } else if (level === 'confirm') {
      if (!await confirm(`⚠️  Large order: $${amount}. Are you sure? (yes/no):`)) { console.log('Cancelled.'); return; }
      if (!await confirm(`⚠️  Confirm again — this will spend $${amount} USDC.e. (yes/no):`)) { console.log('Cancelled.'); return; }
    }
  }

  // Declare for potential use in error recovery (approve revoke)
  const usdceSigned = usdce.connect(wallet);

  // Approve if current allowance is insufficient — skipped in dry-run
  if (!dryRun) {
    const exactAmount = ethers.utils.parseUnits(amount.toFixed(6), 6);
    const currentAllowance = await usdce.allowance(wallet.address, spender);
    if (currentAllowance.lt(exactAmount)) {
      console.log(`\nApproving ${spender.slice(0, 10)}... to spend ${amount} USDC.e...`);
      const approveTx = await usdceSigned.approve(spender, exactAmount, await polyGasOverrides(provider));
      console.log(`Approval tx submitted, waiting for confirmation...`);
      await approveTx.wait();
      console.log(`Approval confirmed.`);
    } else {
      console.log(`\nAllowance sufficient (${ethers.utils.formatUnits(currentAllowance, 6)} USDC.e), skipping approve.`);
    }
  }

  // Submit order — split create/post so a network exception can be disambiguated
  // from a definitive server rejection (result.success === false).
  console.log(`Submitting FOK buy order...`);
  const order = await client.createMarketOrder(
    { tokenID, amount, side: Side.BUY },
    { tickSize, negRisk },
  );

  if (dryRun) {
    console.log(`\n[DRY RUN] Order not submitted. No on-chain transactions were sent.`);
    return { dryRun: true, order };
  }

  let result;
  try {
    result = await client.postOrder(order, OrderType.FOK);
  } catch (e) {
    // Network/timeout — order may have been processed by the CLOB without us
    // receiving the response. Query trade history to disambiguate.
    const fill = await checkRecentFill(client, tokenID, wallet.address);
    if (fill) {
      console.log(`\n✅ Order filled (confirmed via trade history after network error)`);
      console.log(`   Trade ID: ${fill.id ?? '—'}`);
      return { success: true, orderID: fill.id ?? null, status: fill.status ?? 'matched' };
    }
    // Revoke the dangling approval before surfacing the error
    try { await (await usdceSigned.approve(spender, 0, await polyGasOverrides(provider))).wait(); } catch { /* best-effort */ }
    throw new Error(
      `Order submission error — fill status unknown. Check balance.js before retrying. (${e.message})`,
    );
  }
  if (!result.success) {
    // Definitive FOK rejection — revoke the allowance we just set
    try {
      const revokeTx = await usdceSigned.approve(spender, 0, await polyGasOverrides(provider));
      await revokeTx.wait();
    } catch { /* best-effort: warn if revoke itself fails */ }
    throw new Error(`Order not filled: ${result.errorMsg || result.status || 'insufficient liquidity'}.`);
  }
  console.log(`\n✅ Order filled`);
  console.log(`   Status:   ${result.status}`);
  console.log(`   Order ID: ${result.orderID ?? '—'}`);
  return result;
}

// ── Sell flow ─────────────────────────────────────────────────────────────────

export async function sell({ market, side, amount, cfg, provider, wallet, dryRun = false }) {
  if (side !== 'YES' && side !== 'NO') throw new Error(`Invalid side "${side}": must be YES or NO`);
  if (!Number.isFinite(amount) || amount <= 0 || amount > 1_000_000) throw new Error(`Invalid amount: ${amount}`);

  const { Side, OrderType } = await import('@polymarket/clob-client');
  const client = await createL2Client(cfg, wallet, join(AUREHUB_DIR, '.polymarket_clob'));

  const ids = extractTokenIds(market);
  const tokenID = ids[side];
  if (!tokenID) throw new Error(`No ${side} token ID found for this market.`);

  // Check CTF token balance
  const contracts = cfg.yaml?.contracts ?? {};
  const ctfAddr = contracts.ctf_contract ?? '0x4D97DCd97eC945f40cF65F87097ACe5EA0476045';
  if (!ethers.utils.isAddress(ctfAddr)) throw new Error(`Invalid contract address in config: ctf_contract = "${ctfAddr}"`);
  const ctf = new ethers.Contract(ctfAddr, ERC1155_ABI, provider);
  const tokenBalance = await ctf.balanceOf(wallet.address, ethers.BigNumber.from(tokenID));
  const sharesHeld = parseFloat(ethers.utils.formatUnits(tokenBalance, 6));
  if (sharesHeld < amount) {
    throw new Error(`Insufficient ${side} shares: have ${sharesHeld}, need ${amount} to sell.`);
  }

  // Preview
  const negRisk = await client.getNegRisk(tokenID);
  const tickSize = await client.getTickSize(tokenID);
  const ob = await client.getOrderBook(tokenID);
  // Polymarket sorts bids ascending (worst first), best bid is last
  const bestBid = parseFloat(ob.bids?.at(-1)?.price ?? '0.5');
  const estUsdce = (amount * bestBid).toFixed(2);
  console.log(`\nPreview:`);
  console.log(`  Selling:        ${amount} ${side} shares`);
  if (!ob.bids?.at(-1)) {
    console.log(`  Best bid:       ~$0.50/share ⚠️  (no bids in orderbook — estimate may be inaccurate)`);
  } else {
    console.log(`  Best bid:       $${bestBid.toFixed(4)}/share`);
  }
  console.log(`  Est. receive:   ~$${estUsdce} USDC.e (actual fill may differ)`);

  // Hard stops (gas + market active)
  const polRaw = await provider.getBalance(wallet.address);
  // Pass estimated dollar value so minOrderSize check applies to USD proceeds (not share count)
  validateHardStops(parseFloat(estUsdce), {
    usdceBalance: 999999, // USDC.e check not applicable for sell — bypassed intentionally
    polBalance:   parseFloat(ethers.utils.formatEther(polRaw)),
    marketActive: market.active,
    minOrderSize: parseFloat(market.minimum_order_size ?? market.orderMinSize ?? market.min_incentive_size ?? market.minIncentiveSize ?? '0'),
  });

  // Safety gates (on estimated USD value) — skipped in dry-run
  if (!dryRun) {
    const safety = cfg.yaml?.safety ?? { warn_threshold_usd: 50, confirm_threshold_usd: 500 };
    const level = getSafetyLevel(parseFloat(estUsdce), safety);
    if (level === 'warn') {
      if (!await confirm(`⚠️  Selling ${amount} ${side} shares (~$${estUsdce}). Confirm? (yes/no):`)) { console.log('Cancelled.'); return; }
    } else if (level === 'confirm') {
      if (!await confirm(`⚠️  Large order: ~$${estUsdce}. Are you sure? (yes/no):`)) { console.log('Cancelled.'); return; }
      if (!await confirm(`⚠️  Confirm again — selling ${amount} ${side} shares. (yes/no):`)) { console.log('Cancelled.'); return; }
    }
  }

  // setApprovalForAll — skipped in dry-run
  const operator = negRisk
    ? (contracts.neg_risk_exchange ?? '0xC5d563A36AE78145C45a50134d48A1215220f80a')
    : (contracts.ctf_exchange      ?? '0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E');
  if (!ethers.utils.isAddress(operator)) throw new Error(`Invalid contract address in config: ${negRisk ? 'neg_risk_exchange' : 'ctf_exchange'} = "${operator}"`);
  const ctfSigned = ctf.connect(wallet);
  let approvalSetByThisCall = false;
  if (!dryRun) {
    const alreadyApproved = await ctf.isApprovedForAll(wallet.address, operator);
    approvalSetByThisCall = !alreadyApproved;
    if (!alreadyApproved) {
      console.log(`\nApproving exchange operator...`);
      const approveTx = await ctfSigned.setApprovalForAll(operator, true, await polyGasOverrides(provider));
      console.log(`Approval tx submitted, waiting for confirmation...`);
      await approveTx.wait();
      console.log(`Approval confirmed.`);
    } else {
      console.log(`\nOperator already approved, skipping setApprovalForAll.`);
    }
  }

  // Submit order — split create/post so a network exception can be disambiguated
  // from a definitive server rejection (result.success === false).
  console.log(`Submitting FOK sell order...`);
  const order = await client.createMarketOrder(
    { tokenID, amount, side: Side.SELL },
    { tickSize, negRisk },
  );

  if (dryRun) {
    console.log(`\n[DRY RUN] Order not submitted. No on-chain transactions were sent.`);
    return { dryRun: true, order };
  }

  let result;
  try {
    result = await client.postOrder(order, OrderType.FOK);
  } catch (e) {
    const fill = await checkRecentFill(client, tokenID, wallet.address);
    if (fill) {
      console.log(`\n✅ Order filled (confirmed via trade history after network error)`);
      console.log(`   Trade ID: ${fill.id ?? '—'}`);
      return { success: true, orderID: fill.id ?? null, status: fill.status ?? 'matched' };
    }
    // Revoke the dangling setApprovalForAll before surfacing the error (only if we set it)
    if (approvalSetByThisCall) {
      try { await (await ctfSigned.setApprovalForAll(operator, false, await polyGasOverrides(provider))).wait(); } catch { /* best-effort */ }
    }
    throw new Error(
      `Order submission error — fill status unknown. Check balance.js before retrying. (${e.message})`,
    );
  }
  if (!result.success) {
    // Definitive FOK rejection — revoke the operator approval we just set (only if we set it)
    if (approvalSetByThisCall) {
      try {
        const revokeTx = await ctfSigned.setApprovalForAll(operator, false, await polyGasOverrides(provider));
        await revokeTx.wait();
      } catch { /* best-effort: warn if revoke itself fails */ }
    }
    throw new Error(`Order not filled: ${result.errorMsg || result.status || 'insufficient liquidity'}`);
  }
  console.log(`\n✅ Order filled`);
  console.log(`   Status:   ${result.status}`);
  console.log(`   Order ID: ${result.orderID ?? '—'}`);
  return result;
}

// ── CLI entry point ───────────────────────────────────────────────────────────
if (process.argv[1] && realpathSync(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args = process.argv.slice(2);
  const getArg = f => { const i = args.indexOf(f); return i >= 0 ? args[i + 1] : null; };
  const mode    = args.includes('--sell') ? 'sell' : 'buy';
  const dryRun  = args.includes('--dry-run');
  const query   = getArg('--market');
  const side    = (getArg('--side') ?? 'YES').toUpperCase();
  const amount  = parseFloat(getArg('--amount') ?? '0');
  const accountIdx = (() => { const v = getArg('--account'); if (v === null) return undefined; const n = parseInt(v, 10); if (Number.isNaN(n) || n < 0 || String(n) !== v) { console.error('--account must be a non-negative integer'); process.exit(1); } return n; })();

  if (!query || !amount || amount <= 0 || !Number.isFinite(amount) || amount > 1_000_000) {
    console.error('Usage: node scripts/trade.js --buy  --market <slug> --side YES|NO --amount <usd>     [--dry-run]  # buy');
    console.error('       node scripts/trade.js --sell --market <slug> --side YES|NO --amount <shares>  [--dry-run]  # sell');
    process.exit(1);
  }

  (async () => {
    try {
      runTradeEnvCheck();
      const cfg = loadConfig();
      const rpcUrl = resolveRpcUrl(cfg);
      const provider = new ethers.providers.JsonRpcProvider(rpcUrl);
      const wallet = (await createSigner(cfg, { accountIndex: accountIdx })).connect(provider);

      // Resolve market by exact slug or keyword fallback (see browse.js resolveMarket)
      const market = await resolveMarket(query, cfg);

      const fn = mode === 'sell' ? sell : buy;
      await fn({ market, side, amount, cfg, provider, wallet, dryRun });
    } catch (e) {
      if (e.response?.status === 403) {
        console.error('❌ 403 Forbidden — Polymarket API blocked in your region. Use a VPN.');
      } else {
        console.error('❌', e.message);
      }
      process.exit(1);
    }
  })();
}
