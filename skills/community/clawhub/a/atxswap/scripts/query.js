#!/usr/bin/env node
import { createClient, parseArgs, fmt, runMain, jsonStringify, feeTierToPercentString } from "./_helpers.js";
import { getAmountsForLiquidity, tickToSqrtPriceX96 } from "./_v3math.js";
import { parseEther, poolAbi } from "atxswap-sdk";

function usdtPerAtxFromSqrt(sqrtPriceX96, isAtxToken0) {
  const num = Number(sqrtPriceX96);
  const Q96 = Number(2n ** 96n);
  const ratio = (num / Q96) ** 2;
  return isAtxToken0 ? ratio : ratio === 0 ? 0 : 1 / ratio;
}

/** Human USDT per 1 ATX for display (matches app-style quotes). */
function fmtUsdtPerAtxPrice(value) {
  if (!Number.isFinite(value) || value <= 0) return "0";
  const s = value.toFixed(8).replace(/\.?0+$/, "");
  return s.length ? s : "0";
}

await runMain(async () => {
  const client = await createClient();
  const args = parseArgs(process.argv.slice(2));
  const command = args._[0];

  switch (command) {
    case "price": {
      const price = await client.query.getPrice();
      console.log(jsonStringify({
        usdtPerAtx: price.usdtPerAtx,
        atxPerUsdt: price.atxPerUsdt,
        sqrtPriceX96: price.sqrtPriceX96.toString(),
      }, 2));
      break;
    }

    case "balance": {
      const address = args._[1];
      if (!address) { console.error("Usage: query.js balance <address>"); process.exit(1); }
      const bal = await client.query.getBalance(address);
      console.log(jsonStringify({
        address,
        bnb: fmt(bal.bnb),
        atx: fmt(bal.atx),
        usdt: fmt(bal.usdt),
      }, 2));
      break;
    }

    case "quote": {
      const direction = args._[1];
      const amount = args._[2];
      if (!direction || !amount) { console.error("Usage: query.js quote <buy|sell> <amount>"); process.exit(1); }
      const amountWei = parseEther(amount);
      const quote = await client.query.getQuote(direction, amountWei);
      console.log(jsonStringify({
        direction: quote.direction,
        amountIn: fmt(quote.amountIn),
        amountOut: fmt(quote.amountOut),
        priceImpact: (quote.priceImpact * 100).toFixed(4) + "%",
      }, 2));
      break;
    }

    case "positions": {
      const address = args._[1];
      const tokenId = args._[2];
      if (!address) { console.error("Usage: query.js positions <address> [tokenId]"); process.exit(1); }
      const queriedPositions = await client.query.getPositions(address, {
        includeCollectableFees: true,
        ...(tokenId ? { tokenId: BigInt(tokenId) } : {}),
      });
      const positions = tokenId
        ? queriedPositions.filter((position) => position.tokenId === BigInt(tokenId))
        : queriedPositions;
      if (positions.length === 0) {
        console.log("No ATX/USDT positions found.");
      } else {
        const slot0Result = await client.publicClient.readContract({
          address: client.contracts.pool,
          abi: poolAbi,
          functionName: "slot0",
        });
        const currentTick = Number(slot0Result[1]);

        const priceSnapshot = await client.query.getPrice();

        for (const p of positions) {
          const isAtxToken0 = p.token0.toLowerCase() === client.contracts.atx.toLowerCase();
          const collectable0 = p.collectable0 ?? p.tokensOwed0;
          const collectable1 = p.collectable1 ?? p.tokensOwed1;

          let amount0;
          let amount1;
          if (p.principal0 !== undefined && p.principal1 !== undefined) {
            amount0 = p.principal0;
            amount1 = p.principal1;
          } else {
            ({ amount0, amount1 } = getAmountsForLiquidity(
              priceSnapshot.sqrtPriceX96,
              p.tickLower,
              p.tickUpper,
              p.liquidity,
            ));
          }

          const principalAtx = isAtxToken0 ? amount0 : amount1;
          const principalUsdt = isAtxToken0 ? amount1 : amount0;

          const sqrtTickLower = tickToSqrtPriceX96(p.tickLower);
          const sqrtTickUpper = tickToSqrtPriceX96(p.tickUpper);
          const priceAtLower = usdtPerAtxFromSqrt(sqrtTickLower, isAtxToken0);
          const priceAtUpper = usdtPerAtxFromSqrt(sqrtTickUpper, isAtxToken0);
          const bandMin = Math.min(priceAtLower, priceAtUpper);
          const bandMax = Math.max(priceAtLower, priceAtUpper);

          const spotUsdt = priceSnapshot.usdtPerAtx;
          const tickBoundLo = Math.min(p.tickLower, p.tickUpper);
          const tickBoundHi = Math.max(p.tickLower, p.tickUpper);
          const currentPriceInRange =
            currentTick >= tickBoundLo && currentTick < tickBoundHi;

          const collectableAtxRaw = isAtxToken0 ? collectable0 : collectable1;
          const collectableUsdtRaw = isAtxToken0 ? collectable1 : collectable0;

          console.log(jsonStringify({
            tokenId: p.tokenId.toString(),
            fee: p.fee,
            feePercent: feeTierToPercentString(p.fee),
            priceRangeUsdtPerAtx: {
              min: fmtUsdtPerAtxPrice(bandMin),
              max: fmtUsdtPerAtxPrice(bandMax),
            },
            currentPriceUsdtPerAtx: fmtUsdtPerAtxPrice(spotUsdt),
            currentPriceInRange: currentPriceInRange,
            liquidity: p.liquidity.toString(),
            principal0: fmt(amount0),
            principal1: fmt(amount1),
            principalAtx: fmt(principalAtx),
            principalUsdt: fmt(principalUsdt),
            pendingFees: {
              atx: fmt(collectableAtxRaw),
              usdt: fmt(collectableUsdtRaw),
            },
            tokensOwed0: fmt(p.tokensOwed0),
            tokensOwed1: fmt(p.tokensOwed1),
            collectable0: fmt(collectable0),
            collectable1: fmt(collectable1),
            collectableAtx: fmt(collectableAtxRaw),
            collectableUsdt: fmt(collectableUsdtRaw),
          }, 2));
        }
      }
      break;
    }

    case "token-info": {
      const tokenAddr = args._[1];
      if (!tokenAddr) { console.error("Usage: query.js token-info <tokenAddress>"); process.exit(1); }
      const info = await client.query.getTokenInfo(tokenAddr);
      console.log(jsonStringify({
        address: info.address,
        name: info.name,
        symbol: info.symbol,
        decimals: info.decimals,
        totalSupply: fmt(info.totalSupply, info.decimals),
      }, 2));
      break;
    }

    default:
      console.error("Usage: query.js <price|balance|quote|positions|token-info> [args]");
      process.exit(1);
  }
});
