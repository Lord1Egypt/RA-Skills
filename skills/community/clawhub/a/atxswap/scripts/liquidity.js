#!/usr/bin/env node
import { createClient, loadWallet, parseArgs, exitError, runMain, fmt, jsonStringify } from "./_helpers.js";
import { formatUnits, parseEther } from "atxswap-sdk";

const POOL_TOKEN0_ABI = [
  {
    type: "function",
    name: "token0",
    stateMutability: "view",
    inputs: [],
    outputs: [{ type: "address" }],
  },
];

const POOL_SLOT0_ABI = [
  {
    type: "function",
    name: "slot0",
    stateMutability: "view",
    inputs: [],
    outputs: [
      { type: "uint160" },
      { type: "int24" },
      { type: "uint16" },
      { type: "uint16" },
      { type: "uint16" },
      { type: "uint8" },
      { type: "bool" },
    ],
  },
];

const V3_MIN_TICK = -887200;
const V3_MAX_TICK = 887200;
const LOG_BASE = Math.log(1.0001);
const Q96 = 2n ** 96n;

function priceToTick(price) {
  if (price <= 0) return 0;
  return Math.round(Math.log(price) / LOG_BASE);
}

function nearestUsableTick(tick, tickSpacing) {
  return Math.round(tick / tickSpacing) * tickSpacing;
}

function feeToTickSpacing(fee) {
  switch (fee) {
    case 100:
      return 1;
    case 500:
      return 10;
    case 2500:
      return 50;
    case 10000:
      return 200;
    default:
      return 50;
  }
}

function tickToSqrtPriceX96(tick) {
  const sqrtPrice = Math.sqrt(1.0001 ** tick);
  return BigInt(Math.round(sqrtPrice * Number(Q96)));
}

function neededTokens(sqrtPriceX96, tickLower, tickUpper) {
  const sqrtA = tickToSqrtPriceX96(tickLower);
  const sqrtB = tickToSqrtPriceX96(tickUpper);
  if (sqrtPriceX96 <= sqrtA) return { need0: true, need1: false };
  if (sqrtPriceX96 >= sqrtB) return { need0: false, need1: true };
  return { need0: true, need1: true };
}

function calcOtherAmount(sqrtPriceX96, tickLower, tickUpper, amount, isAmount0) {
  if (amount === 0n) return 0n;

  const sqrtA = tickToSqrtPriceX96(tickLower);
  const sqrtB = tickToSqrtPriceX96(tickUpper);
  const sqrtP = sqrtPriceX96;

  if (sqrtP <= sqrtA || sqrtP >= sqrtB) {
    return 0n;
  }

  if (isAmount0) {
    const numeratorL = amount * sqrtP * sqrtB;
    const denominatorL = (sqrtB - sqrtP) * Q96;
    if (denominatorL === 0n) return 0n;
    const L = numeratorL / denominatorL;
    const amount1 = (L * (sqrtP - sqrtA)) / Q96;
    return amount1 > 0n ? amount1 : 0n;
  }

  const diffPA = sqrtP - sqrtA;
  if (diffPA === 0n) return 0n;
  const L = (amount * Q96) / diffPA;
  const amount0 = (L * (sqrtB - sqrtP) * Q96) / (sqrtP * sqrtB);
  return amount0 > 0n ? amount0 : 0n;
}

function sqrtPriceX96ToRawPrice(sqrtPriceX96) {
  const sqrtP = Number(sqrtPriceX96) / Number(Q96);
  return sqrtP * sqrtP;
}

function parsePercentValue(raw, label) {
  const normalized = String(raw).trim().replace(/%$/, "");
  const value = parseFloat(normalized);
  if (!Number.isFinite(value) || value <= 0) {
    exitError(`${label} must be a positive number`);
  }
  return value;
}

function parseBaseToken(raw) {
  const value = String(raw || "").trim().toLowerCase();
  if (value !== "atx" && value !== "usdt") {
    exitError('base token must be either "atx" or "usdt"');
  }
  return value;
}

function normalizeRangeMode(args) {
  const hasTick =
    args["tick-lower"] !== undefined &&
    args["tick-lower"] !== true &&
    args["tick-upper"] !== undefined &&
    args["tick-upper"] !== true;
  const hasPrice =
    args["min-price"] !== undefined &&
    args["min-price"] !== true &&
    args["max-price"] !== undefined &&
    args["max-price"] !== true;
  const hasRangePercent =
    args["range-percent"] !== undefined && args["range-percent"] !== true;
  const wantFull = args["full-range"] === true || args["full-range"] === "true";

  if (wantFull && (hasTick || hasPrice || hasRangePercent)) {
    exitError("Do not combine --full-range with other range options");
  }
  if ([hasTick, hasPrice, hasRangePercent].filter(Boolean).length > 1) {
    exitError("Use only one of --tick-lower/--tick-upper, --min-price/--max-price, or --range-percent");
  }
  if ((args["tick-lower"] !== undefined && !hasTick) || (args["tick-upper"] !== undefined && !hasTick)) {
    exitError("When using ticks, pass both --tick-lower and --tick-upper");
  }
  if ((args["min-price"] !== undefined && !hasPrice) || (args["max-price"] !== undefined && !hasPrice)) {
    exitError("When using price range, pass both --min-price and --max-price (USDT per 1 ATX)");
  }

  return { hasTick, hasPrice, hasRangePercent, wantFull };
}

/**
 * @param {number} human price: USDT per 1 ATX (18-dec pool, same as frontend)
 * @param {boolean} isAtxToken0 from pool
 */
function humanUsdtPerAtxToToken1OverToken0(h, isAtxToken0) {
  if (h <= 0) {
    throw new Error("min-price and max-price must be positive (USDT per 1 ATX)");
  }
  return isAtxToken0 ? h : 1 / h;
}

/**
 * @returns {{ tickLower: number, tickUpper: number }}
 */
function humanPriceRangeToTicks(minHuman, maxHuman, isAtxToken0, tickSpacing) {
  const rawA = humanUsdtPerAtxToToken1OverToken0(minHuman, isAtxToken0);
  const rawB = humanUsdtPerAtxToToken1OverToken0(maxHuman, isAtxToken0);
  let t0 = nearestUsableTick(priceToTick(rawA), tickSpacing);
  let t1 = nearestUsableTick(priceToTick(rawB), tickSpacing);
  let tickLower = Math.min(t0, t1);
  let tickUpper = Math.max(t0, t1);
  if (tickLower < V3_MIN_TICK) tickLower = V3_MIN_TICK;
  if (tickUpper > V3_MAX_TICK) tickUpper = V3_MAX_TICK;
  if (tickLower >= tickUpper) {
    tickUpper = tickLower + tickSpacing;
  }
  if (tickUpper > V3_MAX_TICK) {
    tickUpper = V3_MAX_TICK;
    tickLower = tickUpper - tickSpacing;
  }
  return { tickLower, tickUpper };
}

async function getPoolContext(client) {
  const [token0, slot0] = await Promise.all([
    client.publicClient.readContract({
      address: client.contracts.pool,
      abi: POOL_TOKEN0_ABI,
      functionName: "token0",
    }),
    client.publicClient.readContract({
      address: client.contracts.pool,
      abi: POOL_SLOT0_ABI,
      functionName: "slot0",
    }),
  ]);

  const atxToken0 = token0.toLowerCase() === client.contracts.atx.toLowerCase();
  const sqrtPriceX96 = slot0[0];
  const rawPrice = sqrtPriceX96ToRawPrice(sqrtPriceX96);
  const usdtPerAtx = atxToken0 ? rawPrice : 1 / rawPrice;

  return {
    isAtxToken0: atxToken0,
    sqrtPriceX96,
    currentTick: Number(slot0[1]),
    tickSpacing: feeToTickSpacing(client.poolFee),
    usdtPerAtx,
  };
}

function resolveRangeFromArgs(args, ctx) {
  const { hasTick, hasPrice, hasRangePercent } = normalizeRangeMode(args);

  if (hasPrice) {
    const minP = parseFloat(String(args["min-price"]));
    const maxP = parseFloat(String(args["max-price"]));
    if (!Number.isFinite(minP) || !Number.isFinite(maxP) || minP <= 0 || maxP <= 0) {
      exitError("min-price and max-price must be positive numbers (USDT per 1 ATX)");
    }
    const { tickLower, tickUpper } = humanPriceRangeToTicks(
      minP,
      maxP,
      ctx.isAtxToken0,
      ctx.tickSpacing,
    );
    return {
      tickLower,
      tickUpper,
      meta: {
        mode: "price",
        minPrice: minP,
        maxPrice: maxP,
        tickLower,
        tickUpper,
        tickSpacing: ctx.tickSpacing,
        isAtxToken0: ctx.isAtxToken0,
      },
    };
  }

  if (hasRangePercent) {
    const percent = parsePercentValue(args["range-percent"], "range-percent");
    const factor = percent / 100;
    const minPrice = ctx.usdtPerAtx * (1 - factor);
    const maxPrice = ctx.usdtPerAtx * (1 + factor);
    if (!Number.isFinite(minPrice) || !Number.isFinite(maxPrice) || minPrice <= 0 || maxPrice <= 0) {
      exitError("range-percent is too large for the current price; it would make the lower price non-positive");
    }
    const { tickLower, tickUpper } = humanPriceRangeToTicks(
      minPrice,
      maxPrice,
      ctx.isAtxToken0,
      ctx.tickSpacing,
    );
    return {
      tickLower,
      tickUpper,
      meta: {
        mode: "percent",
        rangePercent: percent,
        centerPrice: ctx.usdtPerAtx,
        minPrice,
        maxPrice,
        tickLower,
        tickUpper,
        tickSpacing: ctx.tickSpacing,
        isAtxToken0: ctx.isAtxToken0,
      },
    };
  }

  if (hasTick) {
    const tickLower = parseInt(String(args["tick-lower"]), 10);
    const tickUpper = parseInt(String(args["tick-upper"]), 10);
    if (!Number.isFinite(tickLower) || !Number.isFinite(tickUpper)) {
      exitError("tick-lower and tick-upper must be integers");
    }
    let tl = Math.min(tickLower, tickUpper);
    let tu = Math.max(tickLower, tickUpper);
    if (tl < V3_MIN_TICK) tl = V3_MIN_TICK;
    if (tu > V3_MAX_TICK) tu = V3_MAX_TICK;
    if (tl >= tu) {
      exitError("tick-lower and tick-upper must allow tickLower < tickUpper after normalizing to pool limits");
    }
    return {
      tickLower: tl,
      tickUpper: tu,
      meta: {
        mode: "tick",
        tickLower: tl,
        tickUpper: tu,
        tickSpacing: ctx.tickSpacing,
        isAtxToken0: ctx.isAtxToken0,
      },
    };
  }

  return {
    tickLower: V3_MIN_TICK,
    tickUpper: V3_MAX_TICK,
    meta: {
      mode: "full-range",
      fullRange: true,
      tickLower: V3_MIN_TICK,
      tickUpper: V3_MAX_TICK,
      tickSpacing: ctx.tickSpacing,
      isAtxToken0: ctx.isAtxToken0,
    },
  };
}

function resolveSingleSidedAmounts(ctx, tickLower, tickUpper, baseToken, amountRaw) {
  const amount = parseEther(amountRaw);
  if (amount <= 0n) {
    exitError("amount must be greater than 0");
  }

  const { need0, need1 } = neededTokens(ctx.sqrtPriceX96, tickLower, tickUpper);
  const needAtx = ctx.isAtxToken0 ? need0 : need1;
  const needUsdt = ctx.isAtxToken0 ? need1 : need0;

  if (baseToken === "atx") {
    if (!needAtx && needUsdt) {
      exitError("Current price is above the selected range; only USDT is needed for this position");
    }
    return {
      atxAmount: amount,
      usdtAmount: needUsdt
        ? calcOtherAmount(ctx.sqrtPriceX96, tickLower, tickUpper, amount, ctx.isAtxToken0)
        : 0n,
      meta: { baseToken, amount: amountRaw, needAtx, needUsdt },
    };
  }

  if (!needUsdt && needAtx) {
    exitError("Current price is below the selected range; only ATX is needed for this position");
  }

  return {
    atxAmount: needAtx
      ? calcOtherAmount(ctx.sqrtPriceX96, tickLower, tickUpper, amount, !ctx.isAtxToken0)
      : 0n,
    usdtAmount: amount,
    meta: { baseToken, amount: amountRaw, needAtx, needUsdt },
  };
}

function buildQuoteResult(ctx, range, amounts, extra = {}) {
  return {
    currentPrice: {
      usdtPerAtx: ctx.usdtPerAtx,
      atxPerUsdt: ctx.usdtPerAtx === 0 ? 0 : 1 / ctx.usdtPerAtx,
    },
    range: range.meta,
    estimatedAmounts: {
      atx: fmt(amounts.atxAmount),
      usdt: fmt(amounts.usdtAmount),
      atxWei: amounts.atxAmount.toString(),
      usdtWei: amounts.usdtAmount.toString(),
    },
    ...extra,
  };
}

function toAmountInput(wei) {
  const value = formatUnits(wei, 18);
  return value.includes(".") ? value.replace(/\.?0+$/, "") : value;
}

function parseSlippageBps(args) {
  if (args["slippage-bps"] === undefined || args["slippage-bps"] === true) {
    return undefined;
  }
  const value = parseInt(String(args["slippage-bps"]), 10);
  if (!Number.isFinite(value) || value < 0 || value > 10_000) {
    exitError("slippage-bps must be between 0 and 10000");
  }
  return value;
}

function buildSdkRangeArgs(args) {
  const { hasTick, hasPrice, hasRangePercent } = normalizeRangeMode(args);
  if (hasPrice) {
    const minPrice = parseFloat(String(args["min-price"]));
    const maxPrice = parseFloat(String(args["max-price"]));
    if (!Number.isFinite(minPrice) || !Number.isFinite(maxPrice) || minPrice <= 0 || maxPrice <= 0) {
      exitError("min-price and max-price must be positive numbers (USDT per 1 ATX)");
    }
    return { minPrice, maxPrice };
  }
  if (hasRangePercent) {
    return { rangePercent: parsePercentValue(args["range-percent"], "range-percent") };
  }
  if (hasTick) {
    const tickLower = parseInt(String(args["tick-lower"]), 10);
    const tickUpper = parseInt(String(args["tick-upper"]), 10);
    if (!Number.isFinite(tickLower) || !Number.isFinite(tickUpper)) {
      exitError("tick-lower and tick-upper must be integers");
    }
    return { tickLower, tickUpper };
  }
  return { fullRange: true };
}

async function quoteViaSdk(client, baseToken, amountRaw, args) {
  if (typeof client.liquidity.quoteAddLiquidity !== "function") {
    return null;
  }
  return await client.liquidity.quoteAddLiquidity({
    baseToken,
    amount: parseEther(amountRaw),
    range: buildSdkRangeArgs(args),
    slippageBps: parseSlippageBps(args),
  });
}

function sdkQuoteToJson(result, extra = {}) {
  return {
    currentPrice: result.currentPrice,
    range: {
      ...result.range,
      tickSpacing: result.pool.tickSpacing,
      isAtxToken0: result.pool.isAtxToken0,
    },
    estimatedAmounts: {
      atx: fmt(result.desiredAmounts.atx),
      usdt: fmt(result.desiredAmounts.usdt),
      atxWei: result.desiredAmounts.atx.toString(),
      usdtWei: result.desiredAmounts.usdt.toString(),
    },
    minAmounts: {
      atx: fmt(result.minAmounts.atx),
      usdt: fmt(result.minAmounts.usdt),
      atxWei: result.minAmounts.atx.toString(),
      usdtWei: result.minAmounts.usdt.toString(),
    },
    ...extra,
  };
}

await runMain(async () => {
  const client = await createClient();
  const args = parseArgs(process.argv.slice(2));
  const command = args._[0];

  if (!command) {
    exitError(
      "Usage: liquidity.js <quote-add|add|remove|collect|burn> [args] [--from address] [--password <pwd>]\n" +
        "  quote-add: <atx|usdt> <amount> with optional range --full-range | --tick-lower <n> --tick-upper <n> | --min-price <p> --max-price <p> | --range-percent <n>\n" +
        "  add: positional <atxAmount> <usdtAmount> OR auto-balance with --base-token <atx|usdt> --amount <n>, plus optional range options and --slippage-bps <n>",
    );
  }

  switch (command) {
    case "quote-add": {
      const baseToken = parseBaseToken(args._[1]);
      const amount = args._[2];
      if (!amount) {
        exitError(
          "Usage: liquidity.js quote-add <atx|usdt> <amount> [--full-range] [--tick-lower n --tick-upper n] [--min-price p --max-price p] [--range-percent n]",
        );
      }

      const sdkQuote = await quoteViaSdk(client, baseToken, amount, args);
      if (sdkQuote) {
        console.log(
          jsonStringify(
            sdkQuoteToJson(sdkQuote, {
              action: "quote add liquidity",
              input: { baseToken, amount },
            }),
            2,
          ),
        );
        break;
      }

      const ctx = await getPoolContext(client);
      const range = resolveRangeFromArgs(args, ctx);
      const amounts = resolveSingleSidedAmounts(ctx, range.tickLower, range.tickUpper, baseToken, amount);

      console.log(
        jsonStringify(
          buildQuoteResult(ctx, range, amounts, {
            action: "quote add liquidity",
            input: { baseToken, amount },
          }),
          2,
        ),
      );
      break;
    }

    case "add": {
      const positionalAtxAmount = args._[1];
      const positionalUsdtAmount = args._[2];
      const hasPositionalAmounts = !!positionalAtxAmount && !!positionalUsdtAmount;
      const hasAutoBalance =
        args["base-token"] !== undefined &&
        args["base-token"] !== true &&
        args.amount !== undefined &&
        args.amount !== true;

      if (hasPositionalAmounts && hasAutoBalance) {
        exitError("Use either positional amounts or --base-token/--amount auto-balance mode, not both");
      }

      if (!hasPositionalAmounts && !hasAutoBalance) {
        exitError(
          "Usage: liquidity.js add <atxAmount> <usdtAmount> [--from address] [--full-range] [--tick-lower n --tick-upper n] [--min-price p --max-price p] [--range-percent n] [--slippage-bps n]\n" +
            "   or: liquidity.js add --base-token <atx|usdt> --amount <n> [same range opts]\n" +
            "  Default: full range. Custom: either tick pair, min/max price (USDT per 1 ATX), or range-percent centered on current price.",
        );
      }

      const ctx = await getPoolContext(client);
      const fromAddress = args.from || client.wallet.list()[0]?.address;
      if (!fromAddress) exitError("No wallet found. Create one first.");
      const wallet = await loadWallet(client, fromAddress, args);
      const range = resolveRangeFromArgs(args, ctx);
      let liqOptions;
      let meta = { ...range.meta };
      let atxAmount;
      let usdtAmount;

      if (range.meta.fullRange) {
        liqOptions = { fullRange: true };
      } else {
        liqOptions = {
          fullRange: false,
          tickLower: range.tickLower,
          tickUpper: range.tickUpper,
        };
      }

      if (hasPositionalAmounts) {
        atxAmount = positionalAtxAmount;
        usdtAmount = positionalUsdtAmount;
      } else {
        const baseToken = parseBaseToken(args["base-token"]);
        const sdkQuote = await quoteViaSdk(client, baseToken, String(args.amount), args);
        if (sdkQuote) {
          atxAmount = toAmountInput(sdkQuote.desiredAmounts.atx);
          usdtAmount = toAmountInput(sdkQuote.desiredAmounts.usdt);
          meta = {
            ...meta,
            autoBalanced: true,
            input: {
              baseToken,
              amount: String(args.amount),
              needAtx: sdkQuote.needs.atx,
              needUsdt: sdkQuote.needs.usdt,
            },
            estimatedAmounts: {
              atx: fmt(sdkQuote.desiredAmounts.atx),
              usdt: fmt(sdkQuote.desiredAmounts.usdt),
            },
          };
        } else {
          const quoted = resolveSingleSidedAmounts(
            ctx,
            range.tickLower,
            range.tickUpper,
            baseToken,
            String(args.amount),
          );
          atxAmount = toAmountInput(quoted.atxAmount);
          usdtAmount = toAmountInput(quoted.usdtAmount);
          meta = {
            ...meta,
            autoBalanced: true,
            input: quoted.meta,
            estimatedAmounts: {
              atx: fmt(quoted.atxAmount),
              usdt: fmt(quoted.usdtAmount),
            },
          };
        }
      }

      const b = parseSlippageBps(args);
      if (b !== undefined) {
        liqOptions = { ...liqOptions, slippageBps: b };
        meta = { ...meta, slippageBps: b };
      }

      const result = await client.liquidity.addLiquidity(
        wallet,
        parseEther(atxAmount),
        parseEther(usdtAmount),
        liqOptions,
      );
      console.log(
        jsonStringify(
          { action: "add liquidity", txHash: result.txHash, range: meta },
          2,
        ),
      );
      break;
    }

    case "remove": {
      const fromAddress = args.from || client.wallet.list()[0]?.address;
      if (!fromAddress) exitError("No wallet found. Create one first.");
      const wallet = await loadWallet(client, fromAddress, args);
      const tokenId = args._[1];
      const percent = args._[2];
      if (!tokenId || !percent) {
        exitError("Usage: liquidity.js remove <tokenId> <percent> [--from address]");
      }
      const removePercent = parseInt(percent, 10);
      const result = await client.liquidity.removeLiquidity(wallet, BigInt(tokenId), removePercent);
      console.log(
        jsonStringify(
          {
            action: "remove liquidity",
            txHash: result.txHash,
            tokenId,
            percent: removePercent,
            multicall: removePercent === 100
              ? ["decreaseLiquidity", "collect", "burn"]
              : ["decreaseLiquidity", "collect"],
            note: removePercent === 100
              ? "100% removal collects withdrawable funds and then burns the NFT in the same transaction. Do not run collect again for this tokenId."
              : "Removal also collects withdrawable funds in the same transaction.",
          },
          2,
        ),
      );
      break;
    }

    case "collect": {
      const fromAddress = args.from || client.wallet.list()[0]?.address;
      if (!fromAddress) exitError("No wallet found. Create one first.");
      const wallet = await loadWallet(client, fromAddress, args);
      const tokenId = args._[1];
      if (!tokenId) exitError("Usage: liquidity.js collect <tokenId> [--from address]");
      const result = await client.liquidity.collectFees(wallet, BigInt(tokenId));
      console.log(jsonStringify({ action: "collect fees", txHash: result.txHash }, 2));
      break;
    }

    case "burn": {
      const fromAddress = args.from || client.wallet.list()[0]?.address;
      if (!fromAddress) exitError("No wallet found. Create one first.");
      const wallet = await loadWallet(client, fromAddress, args);
      const tokenId = args._[1];
      if (!tokenId) exitError("Usage: liquidity.js burn <tokenId> [--from address]");
      const result = await client.liquidity.burnPosition(wallet, BigInt(tokenId));
      console.log(jsonStringify({ action: "burn position", txHash: result.txHash }, 2));
      break;
    }

    default:
      exitError("Usage: liquidity.js <quote-add|add|remove|collect|burn> [args]");
  }
});
