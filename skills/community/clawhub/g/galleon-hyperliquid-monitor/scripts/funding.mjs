#!/usr/bin/env node

function help() {
  process.stdout.write(`Usage:
  node scripts/funding.mjs --side <long|short> --notional <usd> --rate <decimal> --interval-hours <n> --hours <n>

The rate must be the venue's rate for the stated interval. Positive funding means longs pay shorts. Output cashflow is signed from the account's perspective.
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

function number(values, key) {
  const raw = values.get(key);
  if (raw === undefined || raw.length === 0) throw new Error(`--${key} requires a number`);
  const value = Number(raw);
  if (!Number.isFinite(value)) throw new Error(`--${key} must be finite`);
  return value;
}

function main() {
  const { help: requestedHelp, values } = parse(process.argv.slice(2));
  if (requestedHelp) return help();
  const allowed = new Set(["side", "notional", "rate", "interval-hours", "hours"]);
  for (const key of values.keys()) if (!allowed.has(key)) throw new Error(`unknown option: --${key}`);
  const side = values.get("side");
  if (side !== "long" && side !== "short") throw new Error("--side must be long or short");
  const notionalUsd = number(values, "notional");
  const rate = number(values, "rate");
  const intervalHours = number(values, "interval-hours");
  const hours = number(values, "hours");
  if (notionalUsd <= 0) throw new Error("notional must be greater than 0");
  if (intervalHours <= 0) throw new Error("interval-hours must be greater than 0");
  if (hours <= 0) throw new Error("hours must be greater than 0");
  const ratePerHour = rate / intervalHours;
  const payerSign = side === "long" ? -1 : 1;
  process.stdout.write(`${JSON.stringify({
    side,
    ratePerHour,
    ratePerHourPercent: ratePerHour * 100,
    simpleAnnualRatePercent: ratePerHour * 24 * 365 * 100,
    periods: hours / intervalHours,
    accountCashflowUsd: payerSign * notionalUsd * ratePerHour * hours,
  }, null, 2)}\n`);
}

try {
  main();
} catch (error) {
  process.stderr.write(`error: ${error instanceof Error ? error.message : String(error)}\n`);
  process.exitCode = 1;
}
