#!/usr/bin/env node

import { readFile } from "node:fs/promises";

function finite(input, key, fallback) {
  const raw = input[key] ?? fallback;
  if (typeof raw !== "number" || !Number.isFinite(raw)) throw new Error(`${key} must be a finite number`);
  return raw;
}

async function main() {
  const args = process.argv.slice(2);
  if (args.includes("--help")) {
    process.stdout.write("Usage: node scripts/position.mjs --input <snapshot.json>. Use --input - for stdin. Required: tickCurrent, tickLower, tickUpper, positionAssetsUsd, holdValueUsd. Optional: edgeBufferTicks, claimableFeesUsd, claimableIncentivesUsd, realizedProceedsUsd, looseResidueUsd, costsUsd.\n");
    return;
  }
  if (args.length !== 2 || args[0] !== "--input" || !args[1]) throw new Error("expected --input <snapshot.json>");
  let source;
  if (args[1] === "-") {
    source = "";
    for await (const chunk of process.stdin) source += chunk;
  } else {
    source = await readFile(args[1], "utf8");
  }
  const input = JSON.parse(source);
  if (!input || typeof input !== "object" || Array.isArray(input)) throw new Error("input must be a JSON object");
  const tickCurrent = finite(input, "tickCurrent");
  const tickLower = finite(input, "tickLower");
  const tickUpper = finite(input, "tickUpper");
  const edgeBufferTicks = finite(input, "edgeBufferTicks", 0);
  if (![tickCurrent, tickLower, tickUpper, edgeBufferTicks].every(Number.isInteger)) throw new Error("tick values must be integers");
  if (tickLower >= tickUpper) throw new Error("tickLower must be below tickUpper");
  if (edgeBufferTicks < 0) throw new Error("edgeBufferTicks must be at least 0");
  const positionAssetsUsd = finite(input, "positionAssetsUsd");
  const holdValueUsd = finite(input, "holdValueUsd");
  const claimableFeesUsd = finite(input, "claimableFeesUsd", 0);
  const claimableIncentivesUsd = finite(input, "claimableIncentivesUsd", 0);
  const realizedProceedsUsd = finite(input, "realizedProceedsUsd", 0);
  const looseResidueUsd = finite(input, "looseResidueUsd", 0);
  const costsUsd = finite(input, "costsUsd", 0);
  if ([positionAssetsUsd, holdValueUsd, claimableFeesUsd, claimableIncentivesUsd, realizedProceedsUsd, looseResidueUsd, costsUsd].some((value) => value < 0)) {
    throw new Error("USD values must be at least 0");
  }
  if (holdValueUsd === 0) throw new Error("holdValueUsd must be greater than 0");
  const inRange = tickCurrent >= tickLower && tickCurrent < tickUpper;
  const distanceToLower = tickCurrent - tickLower;
  const distanceToUpper = tickUpper - tickCurrent;
  const lpNetValueUsd = positionAssetsUsd + claimableFeesUsd + claimableIncentivesUsd + realizedProceedsUsd + looseResidueUsd - costsUsd;
  process.stdout.write(`${JSON.stringify({
    ok: true,
    range: {
      state: tickCurrent < tickLower ? "below-range" : tickCurrent >= tickUpper ? "above-range" : "in-range",
      inRange,
      nearEdge: inRange && Math.min(distanceToLower, distanceToUpper) <= edgeBufferTicks,
      distanceToLower,
      distanceToUpper,
      percentThroughRange: inRange ? ((tickCurrent - tickLower) / (tickUpper - tickLower)) * 100 : null,
    },
    accounting: {
      lpNetValueUsd,
      holdValueUsd,
      inventoryDivergencePercent: (positionAssetsUsd / holdValueUsd - 1) * 100,
      netResultVsHoldPercent: (lpNetValueUsd / holdValueUsd - 1) * 100,
    },
  }, null, 2)}\n`);
}

try {
  await main();
} catch (error) {
  process.stdout.write(`${JSON.stringify({ ok: false, error: error instanceof Error ? error.message : String(error) })}\n`);
  process.exitCode = 1;
}
