#!/usr/bin/env node
/**
 * limit-order.js <place|list|cancel|modify> ...
 *
 * place spot  buy|sell  <COIN> <PRICE> <SIZE>
 * place perp  long|short <COIN> <PRICE> <SIZE> [--leverage N] [--cross|--isolated]
 * list [--coin COIN]
 * cancel <orderId>
 * modify <orderId> --price <newPrice> [--size <newSize>]
 */

import { loadConfig } from './lib/config.js';
import { createSigner } from './lib/signer.js';
import { createTransport, createInfoClient, createExchangeClient } from './lib/hl-client.js';
import { SymbolConverter, formatPrice, formatSize } from '@nktkas/hyperliquid/utils';
import { pathToFileURL } from 'url';

/**
 * frontendOpenOrders returns order.coin as "@N" for unnamed spot markets (e.g. HFUN → "@1").
 * SymbolConverter only maps "HFUN/USDC" → assetId, not "@1" → assetId.
 * Reverse-lookup via _nameToSpotPairId to get the canonical symbol.
 */
function resolveOrderCoin(converter, rawCoin) {
  if (!/^@\d+$/.test(rawCoin)) return rawCoin;
  for (const [symbol, spotPairId] of converter._nameToSpotPairId) {
    if (spotPairId === rawCoin) return symbol;
  }
  return rawCoin;
}

/**
 * Parse CLI arguments for limit-order.js.
 *
 * @param {string[]} args  process.argv.slice(2)
 * @returns {{ subcommand, mode, action, coin, price, size, leverage, isCross, orderId, newPrice, newSize }}
 */
export function parseLimitArgs(args) {
  const confirmed = args.includes('--confirmed');
  const reduceOnly = args.includes('--reduce-only');
  const isTp = args.includes('--tp');
  const isSl = args.includes('--sl');
  if (isTp && isSl) throw new Error('Cannot use both --tp and --sl at the same time');
  const tpsl = isTp ? 'tp' : isSl ? 'sl' : null;

  let triggerPrice = null;
  const triggerIdx = args.indexOf('--trigger-price');
  if (triggerIdx !== -1) {
    if (!args[triggerIdx + 1]) throw new Error('Missing value for --trigger-price');
    triggerPrice = parseFloat(args[triggerIdx + 1]);
    if (!isFinite(triggerPrice) || triggerPrice <= 0) throw new Error('Invalid trigger price: must be greater than zero');
    if (!tpsl) throw new Error('--trigger-price requires --tp or --sl to specify trigger direction');
  }
  if (tpsl && triggerPrice === null) throw new Error('--tp/--sl requires --trigger-price');

  const cleanArgs = args.filter((a, i) => !['--confirmed', '--reduce-only', '--tp', '--sl', '--trigger-price'].includes(a) && !(i > 0 && args[i - 1] === '--trigger-price'));
  const blank = { subcommand: null, mode: null, action: null, coin: null, price: null, size: null, leverage: null, isCross: true, orderId: null, newPrice: null, newSize: null, confirmed, reduceOnly, triggerPrice, tpsl };

  const [subcommand, ...rest] = cleanArgs;
  if (!subcommand) throw new Error('Usage: limit-order.js <place|list|cancel|modify> ...');

  if (subcommand === 'list') {
    let coin = null;
    for (let i = 0; i < rest.length; i++) {
      if (rest[i] === '--coin' && rest[i + 1]) {
        coin = rest[++i];
        if (!/^[A-Za-z0-9._/-]{1,20}$/.test(coin)) throw new Error(`Invalid coin format: ${coin}`);
      }
    }
    return { ...blank, subcommand: 'list', coin };
  }

  if (subcommand === 'cancel') {
    const [orderIdStr] = rest;
    if (!orderIdStr) throw new Error('Missing orderId argument');
    const orderId = Number(orderIdStr);
    if (!Number.isInteger(orderId) || orderId <= 0) throw new Error(`Invalid orderId: ${orderIdStr}`);
    return { ...blank, subcommand: 'cancel', orderId };
  }

  if (subcommand === 'modify') {
    const [orderIdStr, ...flags] = rest;
    if (!orderIdStr) throw new Error('Missing orderId argument');
    const orderId = Number(orderIdStr);
    if (!Number.isInteger(orderId) || orderId <= 0) throw new Error(`Invalid orderId: ${orderIdStr}`);

    let newPrice = null;
    let newSize = null;
    for (let i = 0; i < flags.length; i++) {
      if (flags[i] === '--price' && flags[i + 1]) {
        newPrice = parseFloat(flags[++i]);
        if (!isFinite(newPrice) || newPrice <= 0) throw new Error('Invalid price: must be greater than zero');
      }
      if (flags[i] === '--size' && flags[i + 1]) {
        newSize = parseFloat(flags[++i]);
        if (!isFinite(newSize) || newSize <= 0) throw new Error('Invalid size: must be greater than zero');
      }
    }
    if (newPrice === null) throw new Error('Missing required --price argument');
    return { ...blank, subcommand: 'modify', orderId, newPrice, newSize };
  }

  if (subcommand === 'place') {
    const [mode, actionOrDir, ...placeRest] = rest;
    if (!mode || !['spot', 'perp'].includes(mode)) throw new Error(`Unknown mode: ${mode}. Use spot or perp`);

    if (mode === 'spot') {
      const [action, coin, priceStr, sizeStr] = [actionOrDir, ...placeRest];
      if (!['buy', 'sell'].includes(action)) throw new Error(`Unknown spot action: ${action}. Use buy or sell`);
      if (!coin) throw new Error('Missing coin argument');
      if (!/^[A-Za-z0-9._/-]{1,20}$/.test(coin)) throw new Error(`Invalid coin format: ${coin}`);
      const price = parseFloat(priceStr);
      if (!isFinite(price) || price <= 0) throw new Error('Invalid price: must be greater than zero');
      const size = parseFloat(sizeStr);
      if (!isFinite(size) || size <= 0) throw new Error('Invalid size: must be greater than zero');
      return { ...blank, subcommand: 'place', mode: 'spot', action, coin, price, size };
    }

    if (mode === 'perp') {
      const [direction, coin, priceStr, sizeStr, ...flags] = [actionOrDir, ...placeRest];
      if (!['long', 'short'].includes(direction)) throw new Error(`Unknown perp direction: ${direction}. Use long or short`);
      if (!coin) throw new Error('Missing coin argument');
      if (!/^[A-Za-z0-9._/-]{1,20}$/.test(coin)) throw new Error(`Invalid coin format: ${coin}`);
      const price = parseFloat(priceStr);
      if (!isFinite(price) || price <= 0) throw new Error('Invalid price: must be greater than zero');
      const size = parseFloat(sizeStr);
      if (!isFinite(size) || size <= 0) throw new Error('Invalid size: must be greater than zero');

      let leverage = null;
      let isCross = true;
      for (let i = 0; i < flags.length; i++) {
        if (flags[i] === '--leverage' && flags[i + 1]) {
          leverage = parseInt(flags[++i], 10);
          if (isNaN(leverage)) throw new Error(`Invalid leverage value: ${flags[i]}`);
        }
        if (flags[i] === '--cross') isCross = true;
        if (flags[i] === '--isolated') isCross = false;
      }
      if (leverage !== null && (leverage < 1 || leverage > 100))
        throw new Error(`Leverage must be between 1 and 100, got: ${leverage}`);
      return { ...blank, subcommand: 'place', mode: 'perp', action: direction, coin, price, size, leverage, isCross };
    }
  }

  throw new Error(`Unknown subcommand: ${subcommand}. Use place, list, cancel, or modify`);
}

function extractAccount(argv) {
  const i = argv.indexOf('--account');
  if (i === -1) return { account: undefined, cleanArgs: argv };
  const raw = argv[i + 1];
  const v = parseInt(raw, 10);
  if (Number.isNaN(v) || v < 0 || String(v) !== raw) { process.stderr.write(JSON.stringify({ error: '--account must be a non-negative integer' }) + '\n'); process.exit(1); }
  return { account: v, cleanArgs: [...argv.slice(0, i), ...argv.slice(i + 2)] };
}

if (process.argv[1] && new URL(import.meta.url).href === pathToFileURL(process.argv[1]).href) {
  const { account: accountIdx, cleanArgs: rawArgs } = extractAccount(process.argv.slice(2));
  let parsed;
  try {
    parsed = parseLimitArgs(rawArgs);
  } catch (err) {
    process.stderr.write(JSON.stringify({ error: err.message }) + '\n');
    process.exit(1);
  }

  try {
    const cfg = loadConfig();
    const wallet = await createSigner(cfg, null, { accountIndex: accountIdx });
    const address = await wallet.getAddress();
    const transport = createTransport(cfg);
    const info = createInfoClient(transport);

    if (parsed.subcommand === 'list') {
      await runList({ info, address, coin: parsed.coin });
    } else if (parsed.subcommand === 'cancel') {
      const exchange = createExchangeClient(transport, wallet);
      await runCancel({ info, exchange, address, transport, orderId: parsed.orderId });
    } else if (parsed.subcommand === 'modify') {
      const exchange = createExchangeClient(transport, wallet);
      await runModify({ info, exchange, address, transport, orderId: parsed.orderId, newPrice: parsed.newPrice, newSize: parsed.newSize, confirmed: parsed.confirmed });
    } else if (parsed.subcommand === 'place') {
      const exchange = createExchangeClient(transport, wallet);
      await runPlace({ info, exchange, address, transport, parsed, cfg });
    }
  } catch (err) {
    process.stderr.write(JSON.stringify({ error: err?.message ?? String(err) }) + '\n');
    process.exit(1);
  }
}

async function runList({ info, address, coin }) {
  const orders = await info.frontendOpenOrders({ user: address });
  const filtered = coin ? orders.filter(o => o.coin === coin || o.coin === `${coin}/USDC`) : orders;
  process.stdout.write(JSON.stringify({
    orders: filtered.map(o => ({
      oid: o.oid,
      coin: o.coin,
      side: o.side,
      limitPx: o.limitPx,
      sz: o.sz,
      timestamp: o.timestamp,
      isTrigger: o.isTrigger || false,
      triggerPx: o.triggerPx || undefined,
      triggerCondition: o.triggerCondition || undefined,
      orderType: o.orderType || undefined,
    })),
  }) + '\n');
  process.exit(0);
}

async function runCancel({ info, exchange, address, transport, orderId }) {
  const orders = await info.frontendOpenOrders({ user: address });
  const order = orders.find(o => o.oid === orderId);
  if (!order) {
    process.stderr.write(JSON.stringify({ error: `Order ${orderId} not found in open orders.` }) + '\n');
    process.exit(1);
  }

  const converter = await SymbolConverter.create({ transport });
  const coinSymbol = resolveOrderCoin(converter, order.coin);
  const assetId = converter.getAssetId(coinSymbol);
  if (assetId === undefined) {
    process.stderr.write(JSON.stringify({ error: `Asset ${order.coin} not found on Hyperliquid. Check the symbol and try again.` }) + '\n');
    process.exit(1);
  }

  await exchange.cancel({ cancels: [{ a: assetId, o: orderId }] });
  process.stdout.write(JSON.stringify({ ok: true, orderId }) + '\n');
  process.exit(0);
}

async function runModify({ info, exchange, address, transport, orderId, newPrice, newSize, confirmed }) {
  const orders = await info.frontendOpenOrders({ user: address });
  const order = orders.find(o => o.oid === orderId);
  if (!order) {
    process.stderr.write(JSON.stringify({ error: `Order ${orderId} not found in open orders.` }) + '\n');
    process.exit(1);
  }

  const converter = await SymbolConverter.create({ transport });
  const coinSymbol = resolveOrderCoin(converter, order.coin);
  const assetId = converter.getAssetId(coinSymbol);
  if (assetId === undefined) {
    process.stderr.write(JSON.stringify({ error: `Asset ${order.coin} not found on Hyperliquid. Check the symbol and try again.` }) + '\n');
    process.exit(1);
  }

  const szDec = converter.getSzDecimals(coinSymbol);
  if (szDec === undefined) {
    process.stderr.write(JSON.stringify({ error: `Size decimals for ${order.coin} not found.` }) + '\n');
    process.exit(1);
  }
  const finalSize = newSize ?? parseFloat(order.sz);
  const isBuy = order.side === 'B';
  const reduceOnly = order.reduceOnly ?? false;

  // Output preview and require --confirmed (always single confirmation for modify)
  process.stdout.write(JSON.stringify({
    preview: true,
    orderId,
    coin: order.coin,
    side: order.side,
    oldPrice: parseFloat(order.limitPx),
    newPrice,
    oldSize: parseFloat(order.sz),
    newSize: finalSize,
    requiresConfirm: true,
    requiresDoubleConfirm: false,
  }) + '\n');

  if (!confirmed) {
    process.exit(0);
  }

  const p = formatPrice(newPrice, szDec);
  const s = formatSize(finalSize, szDec);

  const modifyResult = await exchange.modify({
    oid: orderId,
    order: { a: assetId, b: isBuy, p, s, r: reduceOnly, t: { limit: { tif: 'Gtc' } } },
  });

  // Hyperliquid modify is cancel+reorder — extract new oid from response if present,
  // otherwise query open orders to find the resting order at the new price.
  let newOid = modifyResult?.response?.data?.statuses?.[0]?.resting?.oid ?? null;
  if (newOid == null) {
    const updatedOrders = await info.frontendOpenOrders({ user: address });
    const match = updatedOrders.find(
      o => o.coin === order.coin &&
           o.side === order.side &&
           Math.abs(parseFloat(o.limitPx) - newPrice) / newPrice < 1e-6
    );
    newOid = match?.oid ?? null;
  }

  process.stdout.write(JSON.stringify({ ok: true, oldOid: orderId, oid: newOid, newPrice, newSize: finalSize }) + '\n');
  process.exit(0);
}

async function runPlace({ info, exchange, address, transport, parsed, cfg }) {
  const { mode, action, coin, price, size, leverage, isCross } = parsed;
  const risk = cfg?.yaml?.risk ?? {};
  const toFinitePos = (v, fallback) => (typeof v === 'number' && isFinite(v) && v > 0 ? v : fallback);
  const confirmThreshold = toFinitePos(risk.confirm_trade_usd, 100);
  const largeThreshold = toFinitePos(risk.large_trade_usd, 1000);
  const leverageWarn = toFinitePos(risk.leverage_warn, 20);

  const converter = await SymbolConverter.create({ transport });
  const baseCoin = coin.replace(/\/USDC$/i, '');
  const symbol = mode === 'spot' ? `${baseCoin}/USDC` : baseCoin;
  const assetId = converter.getAssetId(symbol);
  if (assetId === undefined) {
    process.stderr.write(JSON.stringify({ error: `Asset ${coin} not found on Hyperliquid. Check the symbol and try again.` }) + '\n');
    process.exit(1);
  }
  const szDec = converter.getSzDecimals(symbol);
  if (szDec === undefined) {
    process.stderr.write(JSON.stringify({ error: `Size decimals for ${symbol} not found.` }) + '\n');
    process.exit(1);
  }

  // Balance check (available = total - hold; hold is locked in open GTC orders)
  if (mode === 'spot') {
    const spotState = await info.spotClearinghouseState({ user: address });
    if (action === 'buy') {
      const usdcEntry = spotState.balances.find(b => b.coin === 'USDC');
      const usdcBalance = parseFloat(usdcEntry?.total ?? '0') - parseFloat(usdcEntry?.hold ?? '0');
      const needed = price * size;
      if (usdcBalance < needed) {
        process.stderr.write(JSON.stringify({
          error: `Insufficient balance: have $${usdcBalance.toFixed(2)}, need $${needed.toFixed(2)}. Deposit at app.hyperliquid.xyz.`,
        }) + '\n');
        process.exit(1);
      }
    } else {
      const tokenEntry = spotState.balances.find(b => b.coin === baseCoin);
      const tokenBalance = parseFloat(tokenEntry?.total ?? '0') - parseFloat(tokenEntry?.hold ?? '0');
      if (tokenBalance < size) {
        process.stderr.write(JSON.stringify({
          error: `Insufficient ${baseCoin} balance: have ${tokenBalance}, need ${size}. Transfer ${baseCoin} to your Hyperliquid spot account at app.hyperliquid.xyz.`,
        }) + '\n');
        process.exit(1);
      }
    }
  } else if (leverage !== null) {
    // Only check margin when leverage is explicit; otherwise the exchange enforces it
    const perpState = await info.clearinghouseState({ user: address });
    const withdrawable = parseFloat(perpState.withdrawable ?? '0');
    const marginNeeded = (price * size) / leverage;
    if (withdrawable < marginNeeded) {
      process.stderr.write(JSON.stringify({
        error: `Insufficient margin: have $${withdrawable.toFixed(2)}, need $${marginNeeded.toFixed(2)}.`,
      }) + '\n');
      process.exit(1);
    }
  }

  const tradeValue = price * size;
  const marginUsed = mode === 'perp' ? tradeValue / (leverage ?? 1) : null;
  const confirmValue = mode === 'perp' ? (marginUsed ?? tradeValue) : tradeValue;

  const isTrigger = parsed.triggerPrice !== null;
  const previewAction = isTrigger
    ? `${parsed.tpsl === 'tp' ? 'Take Profit' : 'Stop Loss'} ${action === 'buy' || action === 'long' ? 'Buy' : 'Sell'} ${baseCoin} (${mode === 'spot' ? 'Spot' : 'Perpetual'})`
    : mode === 'spot'
      ? `${action === 'buy' ? 'Buy' : 'Sell'} ${baseCoin} (Spot)`
      : `Open ${action === 'long' ? 'Long' : 'Short'} ${baseCoin} (Perpetual)`;

  process.stdout.write(JSON.stringify({
    preview: true,
    action: previewAction,
    coin: baseCoin,
    side: action,
    price,
    size,
    triggerPrice: isTrigger ? parsed.triggerPrice : undefined,
    tpsl: isTrigger ? parsed.tpsl : undefined,
    reduceOnly: parsed.reduceOnly || undefined,
    leverage: mode === 'perp' ? (leverage ?? 1) : undefined,
    marginMode: mode === 'perp' ? (isCross ? 'Cross' : 'Isolated') : undefined,
    tradeValue: tradeValue.toFixed(2),
    marginUsed: marginUsed !== null ? marginUsed.toFixed(2) : undefined,
    confirmThreshold,
    largeThreshold,
    leverageWarn: mode === 'perp' ? leverageWarn : undefined,
    requiresConfirm: confirmValue >= confirmThreshold,
    requiresDoubleConfirm: confirmValue >= largeThreshold,
    leverageWarning: mode === 'perp' && (leverage ?? 1) >= leverageWarn,
    leverageChangeWarning: mode === 'perp' && leverage !== null,
  }) + '\n');

  if (!parsed.confirmed) {
    process.exit(0);
  }

  const isBuy = action === 'buy' || action === 'long';
  if (mode === 'perp' && leverage !== null) {
    await exchange.updateLeverage({ asset: assetId, isCross, leverage });
  }

  const p = formatPrice(price, szDec);
  const s = formatSize(size, szDec);

  const orderType = isTrigger
    ? { trigger: { isMarket: true, triggerPx: formatPrice(parsed.triggerPrice, szDec, mode === 'spot' ? 'spot' : 'perp'), tpsl: parsed.tpsl } }
    : { limit: { tif: 'Gtc' } };
  const grouping = isTrigger ? 'normalTpsl' : 'na';

  const orderStartTime = Date.now();
  let result;
  try {
    result = await exchange.order({
      orders: [{ a: assetId, b: isBuy, p, s, r: parsed.reduceOnly, t: orderType }],
      grouping,
    });
  } catch (orderErr) {
    if (!isTrigger) {
      // GTC order: check if it landed in open orders despite the network error
      try {
        const orders = await info.openOrders({ user: address });
        const match = orders.find(o =>
          o.coin === symbol &&
          o.side === (isBuy ? 'B' : 'A') &&
          Math.abs(parseFloat(o.limitPx) - price) / price < 1e-6 &&
          Math.abs(parseFloat(o.sz) - size) / size < 1e-6 &&
          o.timestamp >= orderStartTime
        );
        if (match) {
          process.stdout.write(JSON.stringify({ ok: true, oid: match.oid, coin, side: action, price, size, status: 'resting' }) + '\n');
          process.exit(0);
        }
      } catch { /* ignore — fall through to unknown error */ }
    }
    process.stderr.write(JSON.stringify({ error: `Order status unknown after network error — check your open orders before retrying. (${orderErr?.message ?? orderErr})` }) + '\n');
    process.exit(1);
  }

  const status0 = result.response.data.statuses[0];
  let oid, orderStatus;
  if (status0?.resting) {
    oid = status0.resting.oid;
    orderStatus = 'resting';
  } else if (status0?.filled) {
    oid = status0.filled.oid;
    orderStatus = 'filled';
  } else if (status0?.waitingForTrigger) {
    oid = status0.waitingForTrigger;
    orderStatus = 'waitingForTrigger';
  } else {
    process.stderr.write(JSON.stringify({ error: `Order error: ${JSON.stringify(status0)}` }) + '\n');
    process.exit(1);
  }

  const output = { ok: true, oid, coin, side: action, price, size, status: orderStatus };
  if (isTrigger) {
    output.triggerPrice = parsed.triggerPrice;
    output.tpsl = parsed.tpsl;
  }
  process.stdout.write(JSON.stringify(output) + '\n');
  process.exit(0);
}
