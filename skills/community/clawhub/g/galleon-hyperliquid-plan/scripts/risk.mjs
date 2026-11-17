#!/usr/bin/env node

function help() {
  process.stdout.write(`Usage:
  node scripts/risk.mjs --side <long|short> --equity <usd> --risk-percent <pct> --entry <price> --stop <price> --stop-slippage-bps <bps> --entry-fee-bps <bps> --exit-fee-bps <bps> --size-decimals <n> [--leverage <n>]

Prints JSON. The calculator is local and does not read or write exchange state.
`);
}

function parse(argv) {
  const values = new Map();
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (token === "--help" || token === "-h") return { help: true, values };
    if (!token.startsWith("--")) throw new Error(`unexpected argument: ${token}`);
    const key = token.slice(2);
    const value = argv[index + 1];
    if (value === undefined || value.startsWith("--")) throw new Error(`${token} requires a value`);
    if (values.has(key)) throw new Error(`duplicate option: ${token}`);
    values.set(key, value);
    index += 1;
  }
  return { help: false, values };
}

function number(values, key, optional = false) {
  const raw = values.get(key);
  if (raw === undefined && optional) return undefined;
  if (raw === undefined || raw.length === 0) throw new Error(`--${key} requires a number`);
  const value = Number(raw);
  if (!Number.isFinite(value)) throw new Error(`--${key} must be finite`);
  return value;
}

function positive(value, field) {
  if (value <= 0) throw new Error(`${field} must be greater than 0`);
}

function nonNegative(value, field) {
  if (value < 0) throw new Error(`${field} must be at least 0`);
}

function main() {
  const { help: requestedHelp, values } = parse(process.argv.slice(2));
  if (requestedHelp) return help();
  const allowed = new Set(["side", "equity", "risk-percent", "entry", "stop", "stop-slippage-bps", "entry-fee-bps", "exit-fee-bps", "size-decimals", "leverage"]);
  for (const key of values.keys()) if (!allowed.has(key)) throw new Error(`unknown option: --${key}`);
  const side = values.get("side");
  if (side !== "long" && side !== "short") throw new Error("--side must be long or short");
  const equityUsd = number(values, "equity");
  const riskPercent = number(values, "risk-percent");
  const entryPrice = number(values, "entry");
  const stopPrice = number(values, "stop");
  const stopSlippageBps = number(values, "stop-slippage-bps");
  const entryFeeBps = number(values, "entry-fee-bps");
  const exitFeeBps = number(values, "exit-fee-bps");
  const sizeDecimals = number(values, "size-decimals");
  const leverage = number(values, "leverage", true);
  positive(equityUsd, "equity");
  positive(riskPercent, "risk-percent");
  if (riskPercent > 100) throw new Error("risk-percent must be at most 100");
  positive(entryPrice, "entry");
  positive(stopPrice, "stop");
  nonNegative(stopSlippageBps, "stop-slippage-bps");
  nonNegative(entryFeeBps, "entry-fee-bps");
  nonNegative(exitFeeBps, "exit-fee-bps");
  if (!Number.isInteger(sizeDecimals) || sizeDecimals < 0 || sizeDecimals > 18) throw new Error("size-decimals must be an integer from 0 to 18");
  if (leverage !== undefined) positive(leverage, "leverage");
  if (side === "long" && stopPrice >= entryPrice) throw new Error("a long stop must be below entry");
  if (side === "short" && stopPrice <= entryPrice) throw new Error("a short stop must be above entry");

  const riskBudgetUsd = equityUsd * riskPercent / 100;
  const nominalStopDistance = Math.abs(entryPrice - stopPrice);
  const slippagePerUnit = entryPrice * stopSlippageBps / 10_000;
  const stressedStopFill = side === "long" ? stopPrice - slippagePerUnit : stopPrice + slippagePerUnit;
  if (stressedStopFill <= 0) throw new Error("stressed stop fill must stay above 0");
  const feesPerUnit = entryPrice * entryFeeBps / 10_000 + stressedStopFill * exitFeeBps / 10_000;
  const stressedDistance = Math.abs(entryPrice - stressedStopFill) + feesPerUnit;
  const rawSize = riskBudgetUsd / stressedDistance;
  const factor = 10 ** sizeDecimals;
  const size = Math.floor(rawSize * factor) / factor;
  const entryNotionalUsd = size * entryPrice;
  const stressedRiskUsd = size * stressedDistance;
  process.stdout.write(`${JSON.stringify({
    side,
    riskBudgetUsd,
    nominalStopDistance,
    stressedStopFill,
    slippagePerUnit,
    feesPerUnit,
    stressedDistance,
    rawSize,
    size,
    entryNotionalUsd,
    nominalRiskUsd: size * nominalStopDistance,
    stressedRiskUsd,
    unusedRiskBudgetUsd: riskBudgetUsd - stressedRiskUsd,
    marginUsd: leverage === undefined ? null : entryNotionalUsd / leverage,
  }, null, 2)}\n`);
}

try {
  main();
} catch (error) {
  process.stderr.write(`error: ${error instanceof Error ? error.message : String(error)}\n`);
  process.exitCode = 1;
}
