#!/usr/bin/env node

function help() {
  process.stdout.write(`Usage:
  node scripts/review.mjs --side <long|short> --size <n> --entry <price> --exit <price> --entry-fee <usd> --exit-fee <usd> --funding <signed-usd> [--risk-usd <usd>]

Funding is signed from the account's perspective: received is positive and paid is negative.
`);
}

function parse(argv) {
  const values = new Map();
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (token === "--help" || token === "-h") return { help: true, values };
    if (!token.startsWith("--")) throw new Error(`unexpected argument: ${token}`);
    const value = argv[index + 1];
    if (value === undefined || value.startsWith("--")) throw new Error(`${token} requires a value`);
    const key = token.slice(2);
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

function main() {
  const { help: requestedHelp, values } = parse(process.argv.slice(2));
  if (requestedHelp) return help();
  const allowed = new Set(["side", "size", "entry", "exit", "entry-fee", "exit-fee", "funding", "risk-usd"]);
  for (const key of values.keys()) if (!allowed.has(key)) throw new Error(`unknown option: --${key}`);
  const side = values.get("side");
  if (side !== "long" && side !== "short") throw new Error("--side must be long or short");
  const size = number(values, "size");
  const entryPrice = number(values, "entry");
  const exitPrice = number(values, "exit");
  const entryFeeUsd = number(values, "entry-fee");
  const exitFeeUsd = number(values, "exit-fee");
  const fundingUsd = number(values, "funding");
  const riskUsd = number(values, "risk-usd", true);
  if (size <= 0) throw new Error("size must be greater than 0");
  if (entryPrice <= 0 || exitPrice <= 0) throw new Error("entry and exit must be greater than 0");
  if (entryFeeUsd < 0 || exitFeeUsd < 0) throw new Error("fees must be at least 0");
  if (riskUsd !== undefined && riskUsd <= 0) throw new Error("risk-usd must be greater than 0");
  const direction = side === "long" ? 1 : -1;
  const grossPnlUsd = direction * (exitPrice - entryPrice) * size;
  const feesUsd = entryFeeUsd + exitFeeUsd;
  const netCostUsd = feesUsd - fundingUsd;
  const netPnlUsd = grossPnlUsd - netCostUsd;
  process.stdout.write(`${JSON.stringify({
    side,
    grossPnlUsd,
    feesUsd,
    fundingUsd,
    netPnlUsd,
    netCostUsd,
    returnOnEntryNotionalPercent: netPnlUsd / (entryPrice * size) * 100,
    rMultiple: riskUsd === undefined ? null : netPnlUsd / riskUsd,
  }, null, 2)}\n`);
}

try {
  main();
} catch (error) {
  process.stderr.write(`error: ${error instanceof Error ? error.message : String(error)}\n`);
  process.exitCode = 1;
}
