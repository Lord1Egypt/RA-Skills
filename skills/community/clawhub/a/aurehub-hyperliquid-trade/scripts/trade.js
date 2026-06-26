#!/usr/bin/env node
/**
 * trade.js <spot|perp> <buy|sell|open|close> <COIN> [direction] <SIZE> [--leverage N] [--cross|--isolated]
 */
import { loadConfig } from './lib/config.js';
import { createSigner } from './lib/signer.js';
import { createTransport, createInfoClient, createExchangeClient } from './lib/hl-client.js';
import { parseArgs, ioPrice, closeDirection } from './lib/trade-helpers.js';
import { SymbolConverter, formatPrice, formatSize } from '@nktkas/hyperliquid/utils';

function extractAccount(argv) {
  const i = argv.indexOf('--account');
  if (i === -1) return { account: undefined, cleanArgs: argv };
  const raw = argv[i + 1];
  const v = parseInt(raw, 10);
  if (Number.isNaN(v) || v < 0 || String(v) !== raw) { process.stderr.write(JSON.stringify({ error: '--account must be a non-negative integer' }) + '\n'); process.exit(1); }
  return { account: v, cleanArgs: [...argv.slice(0, i), ...argv.slice(i + 2)] };
}

const { account: accountIdx, cleanArgs: rawArgs } = extractAccount(process.argv.slice(2));

let parsed;
try {
  parsed = parseArgs(rawArgs);
} catch (err) {
  process.stderr.write(JSON.stringify({ error: err.message }) + '\n');
  process.exit(1);
}

const { mode, action, coin, size, direction, leverage, isCross, confirmed } = parsed;

/**
 * On network error after exchange.order(), query recent fills to determine if the order
 * actually executed. Returns the matching fill object or null.
 */
async function checkRecentFill(info, address, isBuy, coin, startTime) {
  try {
    const fills = await info.userFillsByTime({ user: address, startTime });
    const expectedSide = isBuy ? 'B' : 'A';
    return fills.find(f => f.coin === coin && f.side === expectedSide && f.time >= startTime) ?? null;
  } catch {
    return null;
  }
}

try {
  const cfg = loadConfig();
  const wallet = await createSigner(cfg, null, { accountIndex: accountIdx });
  const address = await wallet.getAddress();
  const transport = createTransport(cfg);
  const info = createInfoClient(transport);

  // Resolve asset metadata and mid price in parallel (independent calls)
  const baseCoin = coin.replace(/\/USDC$/i, '');
  const symbol = mode === 'spot' ? `${baseCoin}/USDC` : baseCoin;
  const [converter, mids] = await Promise.all([
    SymbolConverter.create({ transport }),
    info.allMids(),
  ]);
  const assetId = converter.getAssetId(symbol);
  if (assetId === undefined) {
    process.stderr.write(JSON.stringify({ error: `Asset ${baseCoin} not found on Hyperliquid. Check the symbol and try again.` }) + '\n');
    process.exit(1);
  }
  const szDec = converter.getSzDecimals(symbol);
  if (szDec === undefined) {
    process.stderr.write(JSON.stringify({ error: `Size decimals for ${symbol} not found.` }) + '\n');
    process.exit(1);
  }

  // allMids keys named spot markets as "COIN/USDC" but unnamed ones as "@N" (spot market index).
  // SymbolConverter.getSpotPairId() returns the exact allMids key for any spot market.
  const spotPairId = mode === 'spot' ? converter.getSpotPairId(symbol) : undefined;
  const midRaw = mids[symbol] ?? mids[coin] ?? (spotPairId !== undefined ? mids[spotPairId] : undefined);
  if (!midRaw) {
    process.stderr.write(JSON.stringify({ error: `Could not fetch mid price for ${coin}.` }) + '\n');
    process.exit(1);
  }
  const mid = parseFloat(midRaw);
  if (!isFinite(mid) || mid <= 0) {
    process.stderr.write(JSON.stringify({ error: `Invalid mid price for ${baseCoin}: ${midRaw}` }) + '\n');
    process.exit(1);
  }

  const risk = cfg?.yaml?.risk ?? {};
  const toFinitePos = (v, fallback) => (typeof v === 'number' && isFinite(v) && v > 0 ? v : fallback);
  const confirmThreshold = toFinitePos(risk.confirm_trade_usd, 100);
  const largeThreshold = toFinitePos(risk.large_trade_usd, 1000);
  const leverageWarn = toFinitePos(risk.leverage_warn, 20);
  const slippagePct = toFinitePos(risk.slippage_pct, 5);

  if (mode === 'spot') {
    const isBuy = action === 'buy';

    // Balance pre-check (available = total - hold; hold is locked in open GTC orders)
    const spotState = await info.spotClearinghouseState({ user: address });
    if (isBuy) {
      const usdcEntry = spotState.balances.find(b => b.coin === 'USDC');
      const usdcBalance = parseFloat(usdcEntry?.total ?? '0') - parseFloat(usdcEntry?.hold ?? '0');
      const needed = size * mid;
      if (usdcBalance < needed) {
        process.stderr.write(JSON.stringify({ error: `Insufficient balance: have $${usdcBalance.toFixed(2)}, need $${needed.toFixed(2)}. Deposit at app.hyperliquid.xyz to top up.` }) + '\n');
        process.exit(1);
      }
    } else {
      const tokenEntry = spotState.balances.find(b => b.coin === baseCoin);
      const tokenBalance = parseFloat(tokenEntry?.total ?? '0') - parseFloat(tokenEntry?.hold ?? '0');
      if (tokenBalance < size) {
        process.stderr.write(JSON.stringify({ error: `Insufficient ${baseCoin} balance: have ${tokenBalance}, need ${size}. Transfer ${baseCoin} to your Hyperliquid spot account at app.hyperliquid.xyz.` }) + '\n');
        process.exit(1);
      }
    }

    const tradeValue = size * mid;

    process.stdout.write(JSON.stringify({
      preview: true,
      action: `${isBuy ? 'Buy' : 'Sell'} ${baseCoin} (Spot)`,
      coin: baseCoin,
      side: action,
      size,
      estPrice: mid,
      tradeValue: tradeValue.toFixed(2),
      requiresConfirm: tradeValue >= confirmThreshold,
      requiresDoubleConfirm: tradeValue >= largeThreshold,
    }) + '\n');
    if (!confirmed) process.exit(0);

    const sz = formatSize(size, szDec);
    const exchange = createExchangeClient(transport, wallet);
    const orderStartTime = Date.now();
    let result;
    try {
      result = await exchange.order({
        orders: [{ a: assetId, b: isBuy, p: formatPrice(ioPrice(isBuy, mid, slippagePct), szDec, 'spot'), s: sz, r: false, t: { limit: { tif: 'Ioc' } } }],
        grouping: 'na',
      });
    } catch (orderErr) {
      const fill = await checkRecentFill(info, address, isBuy, symbol, orderStartTime);
      if (fill) {
        process.stdout.write(JSON.stringify({ ok: true, oid: fill.oid, avgPx: fill.px, filledSz: fill.sz }) + '\n');
        process.exit(0);
      }
      process.stderr.write(JSON.stringify({ error: `Order status unknown after network error — check your position before retrying. (${orderErr?.message ?? orderErr})` }) + '\n');
      process.exit(1);
    }

    const status0 = result?.response?.data?.statuses?.[0];
    if (!status0?.filled) {
      process.stderr.write(JSON.stringify({ error: `Order not filled — price moved beyond the ${slippagePct}% IOC limit. Check current price and retry.` }) + '\n');
      process.exit(1);
    }

    process.stdout.write(JSON.stringify({ ok: true, oid: status0.filled.oid, avgPx: status0.filled.avgPx, filledSz: status0.filled.totalSz }) + '\n');
    process.exit(0);
  }

  if (mode === 'perp') {
    if (action === 'open') {
      const isBuy = direction === 'long';
      const lev = leverage ?? 1;
      const marginUsed = (size * mid) / lev;
      const leverageWarning = leverage !== null && leverage >= leverageWarn;

      // Balance pre-check (only when leverage is explicit; otherwise exchange enforces it)
      // In Unified Account Mode, spot USDC also counts as available margin.
      if (leverage !== null) {
        const [perpState, spotState] = await Promise.all([
          info.clearinghouseState({ user: address }),
          info.spotClearinghouseState({ user: address }),
        ]);
        const perpAvailable = parseFloat(perpState.withdrawable ?? '0');
        const spotUsdcEntry = spotState.balances.find(b => b.coin === 'USDC');
        const spotUsdc = parseFloat(spotUsdcEntry?.total ?? '0') - parseFloat(spotUsdcEntry?.hold ?? '0');
        const totalAvailable = perpAvailable + spotUsdc;
        if (totalAvailable < marginUsed) {
          process.stderr.write(JSON.stringify({ error: `Insufficient margin: have $${totalAvailable.toFixed(2)}, need $${marginUsed.toFixed(2)}.` }) + '\n');
          process.exit(1);
        }
      }

      process.stdout.write(JSON.stringify({
        preview: true,
        action: `Open ${isBuy ? 'Long' : 'Short'} ${baseCoin} (Perpetual)`,
        coin: baseCoin,
        direction,
        size,
        leverage: lev,
        marginMode: isCross ? 'Cross' : 'Isolated',
        estPrice: mid,
        marginUsed: marginUsed.toFixed(2),
        requiresConfirm: marginUsed >= confirmThreshold,
        requiresDoubleConfirm: marginUsed >= largeThreshold,
        leverageWarning,
        leverageChangeWarning: leverage !== null,
      }) + '\n');
      if (!confirmed) process.exit(0);

      const exchange = createExchangeClient(transport, wallet);

      // Set leverage before opening position
      if (leverage !== null) {
        await exchange.updateLeverage({
          asset: assetId,
          isCross,
          leverage,
        });
      }

      const sz = formatSize(size, szDec);

      const orderStartTime = Date.now();
      let result;
      try {
        result = await exchange.order({
          orders: [{ a: assetId, b: isBuy, p: formatPrice(ioPrice(isBuy, mid, slippagePct), szDec, 'perp'), s: sz, r: false, t: { limit: { tif: 'Ioc' } } }],
          grouping: 'na',
        });
      } catch (orderErr) {
        const fill = await checkRecentFill(info, address, isBuy, symbol, orderStartTime);
        if (fill) {
          process.stdout.write(JSON.stringify({ ok: true, oid: fill.oid, avgPx: fill.px, filledSz: fill.sz }) + '\n');
          process.exit(0);
        }
        process.stderr.write(JSON.stringify({ error: `Order status unknown after network error — check your position before retrying. (${orderErr?.message ?? orderErr})` }) + '\n');
        process.exit(1);
      }

      const status0 = result?.response?.data?.statuses?.[0];
      if (!status0?.filled) {
        process.stderr.write(JSON.stringify({ error: `Order not filled — price moved beyond the ${slippagePct}% IOC limit. Check current price and retry.` }) + '\n');
        process.exit(1);
      }

      process.stdout.write(JSON.stringify({ ok: true, oid: status0.filled.oid, avgPx: status0.filled.avgPx, filledSz: status0.filled.totalSz }) + '\n');
      process.exit(0);
    }

    if (action === 'close') {
      // Auto-detect direction from open position
      const state = await info.clearinghouseState({ user: address });
      const pos = state.assetPositions.find(p => p.position.coin === baseCoin);

      if (!pos) {
        process.stderr.write(JSON.stringify({ error: `No open position found for ${baseCoin}.` }) + '\n');
        process.exit(1);
      }

      const szi = parseFloat(pos.position.szi);
      if (!isFinite(szi) || szi === 0) {
        process.stderr.write(JSON.stringify({ error: `Could not read open position size for ${baseCoin}. Try again or check your position at app.hyperliquid.xyz.` }) + '\n');
        process.exit(1);
      }
      const posSize = Math.abs(szi);
      if (size > posSize) {
        process.stderr.write(JSON.stringify({
          error: `Close size ${size} exceeds open position size ${posSize}. Use ${posSize} to fully close.`,
        }) + '\n');
        process.exit(1);
      }
      const isBuy = closeDirection(szi);

      const closeValue = size * mid;
      const posLeverage = pos.position.leverage?.value ?? 1;
      const closeMargin = closeValue / posLeverage;
      process.stdout.write(JSON.stringify({
        preview: true,
        action: `Close ${szi > 0 ? 'Long' : 'Short'} ${baseCoin} (Perpetual)`,
        coin: baseCoin,
        size,
        positionSize: posSize,
        leverage: posLeverage,
        closingDirection: isBuy ? 'buy' : 'sell',
        estPrice: mid,
        tradeValue: closeValue.toFixed(2),
        marginReleased: closeMargin.toFixed(2),
        requiresConfirm: closeMargin >= confirmThreshold,
        requiresDoubleConfirm: closeMargin >= largeThreshold,
      }) + '\n');
      if (!confirmed) process.exit(0);

      const exchange = createExchangeClient(transport, wallet);
      const sz = formatSize(size, szDec);

      const orderStartTime = Date.now();
      let result;
      try {
        result = await exchange.order({
          orders: [{ a: assetId, b: isBuy, p: formatPrice(ioPrice(isBuy, mid, slippagePct), szDec, 'perp'), s: sz, r: true, t: { limit: { tif: 'Ioc' } } }],
          grouping: 'na',
        });
      } catch (orderErr) {
        const fill = await checkRecentFill(info, address, isBuy, symbol, orderStartTime);
        if (fill) {
          process.stdout.write(JSON.stringify({ ok: true, oid: fill.oid, avgPx: fill.px, filledSz: fill.sz, closedDirection: szi > 0 ? 'long' : 'short' }) + '\n');
          process.exit(0);
        }
        process.stderr.write(JSON.stringify({ error: `Order status unknown after network error — check your position before retrying. (${orderErr?.message ?? orderErr})` }) + '\n');
        process.exit(1);
      }

      const status0 = result?.response?.data?.statuses?.[0];
      if (!status0?.filled) {
        process.stderr.write(JSON.stringify({ error: `Order not filled — price moved beyond the ${slippagePct}% IOC limit. Check current price and retry.` }) + '\n');
        process.exit(1);
      }

      process.stdout.write(JSON.stringify({ ok: true, oid: status0.filled.oid, avgPx: status0.filled.avgPx, filledSz: status0.filled.totalSz, closedDirection: szi > 0 ? 'long' : 'short' }) + '\n');
      process.exit(0);
    }
  }

  process.stderr.write(JSON.stringify({ error: `Unknown mode/action: ${mode} ${action}` }) + '\n');
  process.exit(1);

} catch (err) {
  process.stderr.write(JSON.stringify({ error: err?.message ?? String(err) }) + '\n');
  process.exit(1);
}
