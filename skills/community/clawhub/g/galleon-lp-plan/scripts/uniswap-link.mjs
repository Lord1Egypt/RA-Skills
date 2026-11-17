#!/usr/bin/env node

const ADDRESS = /^0x[a-fA-F0-9]{40}$/;
const CHAIN = /^[a-z0-9][a-z0-9-]{0,63}$/;
const DECIMAL = /^(?:0|[1-9][0-9]*)(?:\.[0-9]+)?$/;

function parseArgs(args) {
  const flags = new Map();
  for (let index = 0; index < args.length; index += 1) {
    const token = args[index];
    if (!token.startsWith("--")) throw new Error(`unexpected argument: ${token}`);
    const equalAt = token.indexOf("=");
    const key = equalAt > 2 ? token.slice(2, equalAt) : token.slice(2);
    if (flags.has(key)) throw new Error(`duplicate option: --${key}`);
    if (equalAt > 2) {
      flags.set(key, token.slice(equalAt + 1));
      continue;
    }
    const next = args[index + 1];
    if (next !== undefined && !next.startsWith("--")) {
      flags.set(key, next);
      index += 1;
    } else {
      flags.set(key, true);
    }
  }
  return flags;
}

function rejectUnknown(flags, allowed) {
  for (const key of flags.keys()) {
    if (!allowed.includes(key)) throw new Error(`unknown option: --${key}`);
  }
}

function stringFlag(flags, key, required = false) {
  const value = flags.get(key);
  if (value === undefined && !required) return undefined;
  if (typeof value !== "string" || value.length === 0) throw new Error(`--${key} requires a value`);
  return value;
}

function booleanFlag(flags, key) {
  const value = flags.get(key);
  if (value === undefined) return false;
  if (value !== true) throw new Error(`--${key} does not take a value`);
  return true;
}

function integerFlag(flags, key, required = false) {
  const value = stringFlag(flags, key, required);
  if (value === undefined) return undefined;
  if (!/^[0-9]+$/.test(value)) throw new Error(`--${key} must be a non-negative integer`);
  const parsed = Number(value);
  if (!Number.isSafeInteger(parsed)) throw new Error(`--${key} is outside the safe integer range`);
  return parsed;
}

function decimalFlag(flags, key, required = false) {
  const value = stringFlag(flags, key, required);
  if (value === undefined) return undefined;
  if (!DECIMAL.test(value)) throw new Error(`--${key} must be a plain decimal number`);
  if (/^0(?:\.0+)?$/.test(value)) throw new Error(`--${key} must be greater than 0`);
  return value;
}

function decimalParts(value) {
  const [integer, fraction = ""] = value.split(".");
  return [integer.replace(/^0+(?=[0-9])/, ""), fraction.replace(/0+$/, "")];
}

function compareDecimals(left, right) {
  const [leftInteger, leftFraction] = decimalParts(left);
  const [rightInteger, rightFraction] = decimalParts(right);
  if (leftInteger.length !== rightInteger.length) return leftInteger.length < rightInteger.length ? -1 : 1;
  if (leftInteger !== rightInteger) return leftInteger < rightInteger ? -1 : 1;
  const width = Math.max(leftFraction.length, rightFraction.length);
  const paddedLeft = leftFraction.padEnd(width, "0");
  const paddedRight = rightFraction.padEnd(width, "0");
  return paddedLeft === paddedRight ? 0 : paddedLeft < paddedRight ? -1 : 1;
}

function validateCurrency(value, key) {
  if (value !== "NATIVE" && !ADDRESS.test(value)) {
    throw new Error(`--${key} must be NATIVE or a 20-byte address`);
  }
}

function queryJson(value) {
  return JSON.stringify(value).replaceAll('"', "%22");
}

function help() {
  process.stdout.write(`Build a reviewed Uniswap position-creation link.

Usage:
  node scripts/uniswap-link.mjs --version v2 --chain <slug> --currency-a <address|NATIVE> --currency-b <address|NATIVE> [--json]
  node scripts/uniswap-link.mjs --version <v3|v4> --chain <slug> --currency-a <address|NATIVE> --currency-b <address|NATIVE> --fee <uint24> --tick-spacing <n> (--full-range | --min-price <n> --max-price <n>) [options]

Options:
  --amount <decimal>          Prefill one human-readable deposit amount
  --exact-field <TOKEN0|TOKEN1>
  --initial-price <decimal>  Initial price for a new pool
  --price-inverted
  --dynamic                  v4 dynamic fee
  --hook <address>           v4 hook
  --json

Verify the current interface schema, chain support, token order, fee, tick spacing, hook, and final wallet display before use.
`);
}

function build(flags) {
  rejectUnknown(flags, [
    "version",
    "chain",
    "currency-a",
    "currency-b",
    "fee",
    "tick-spacing",
    "full-range",
    "min-price",
    "max-price",
    "initial-price",
    "price-inverted",
    "dynamic",
    "hook",
    "amount",
    "exact-field",
    "json",
  ]);

  const version = stringFlag(flags, "version", true);
  if (!version || !["v2", "v3", "v4"].includes(version)) throw new Error("--version must be v2, v3, or v4");
  const chain = stringFlag(flags, "chain", true);
  if (!chain || !CHAIN.test(chain)) throw new Error("--chain must be a lowercase interface chain slug");
  const currencyA = stringFlag(flags, "currency-a", true);
  const currencyB = stringFlag(flags, "currency-b", true);
  if (!currencyA || !currencyB) throw new Error("both currencies are required");
  validateCurrency(currencyA, "currency-a");
  validateCurrency(currencyB, "currency-b");
  if (currencyA.toLowerCase() === currencyB.toLowerCase()) throw new Error("currencies must differ");

  const parts = [
    `currencyA=${encodeURIComponent(currencyA)}`,
    `currencyB=${encodeURIComponent(currencyB)}`,
    `chain=${encodeURIComponent(chain)}`,
  ];

  if (version === "v2") {
    const forbidden = [
      "fee",
      "tick-spacing",
      "full-range",
      "min-price",
      "max-price",
      "initial-price",
      "price-inverted",
      "dynamic",
      "hook",
      "amount",
      "exact-field",
    ].filter((key) => flags.has(key));
    if (forbidden.length > 0) throw new Error(`v2 does not accept --${forbidden[0]}`);
    parts.push("version=v2");
    return `https://app.uniswap.org/positions/create?${parts.join("&")}`;
  }

  const feeAmount = integerFlag(flags, "fee", true);
  const tickSpacing = integerFlag(flags, "tick-spacing", true);
  if (feeAmount === undefined || feeAmount > 16_777_215) throw new Error("--fee must fit uint24");
  if (tickSpacing === undefined || tickSpacing < 1 || tickSpacing > 32_767) {
    throw new Error("--tick-spacing must be between 1 and 32767");
  }

  const fullRange = booleanFlag(flags, "full-range");
  const minPrice = decimalFlag(flags, "min-price");
  const maxPrice = decimalFlag(flags, "max-price");
  if (fullRange && (minPrice !== undefined || maxPrice !== undefined)) {
    throw new Error("--full-range cannot be combined with price bounds");
  }
  if (!fullRange && (minPrice === undefined || maxPrice === undefined)) {
    throw new Error("custom ranges require --min-price and --max-price");
  }
  if (minPrice !== undefined && maxPrice !== undefined && compareDecimals(minPrice, maxPrice) >= 0) {
    throw new Error("--min-price must be below --max-price");
  }

  const initialPrice = decimalFlag(flags, "initial-price") ?? "";
  const isDynamic = booleanFlag(flags, "dynamic");
  const priceInverted = booleanFlag(flags, "price-inverted");
  const hook = stringFlag(flags, "hook");
  if (version === "v3" && (isDynamic || hook !== undefined)) throw new Error("dynamic fees and hooks require v4");
  if (hook !== undefined && !ADDRESS.test(hook)) throw new Error("--hook must be a 20-byte address");

  parts.push(
    `fee=${queryJson({ feeAmount, tickSpacing, isDynamic })}`,
    `priceRangeState=${queryJson({
      priceInverted,
      fullRange,
      minPrice: minPrice ?? "",
      maxPrice: maxPrice ?? "",
      initialPrice,
      inputMode: "price",
    })}`,
  );

  const amount = decimalFlag(flags, "amount");
  const exactField = stringFlag(flags, "exact-field");
  if ((amount === undefined) !== (exactField === undefined)) {
    throw new Error("--amount and --exact-field must be provided together");
  }
  if (exactField !== undefined && exactField !== "TOKEN0" && exactField !== "TOKEN1") {
    throw new Error("--exact-field must be TOKEN0 or TOKEN1");
  }
  if (amount !== undefined && exactField !== undefined) {
    parts.push(`depositState=${queryJson({ exactField, exactAmounts: { [exactField]: amount } })}`);
  }
  if (hook !== undefined) parts.push(`hook=${encodeURIComponent(hook)}`);
  parts.push("step=1");
  return `https://app.uniswap.org/positions/create?${parts.join("&")}`;
}

try {
  const flags = parseArgs(process.argv.slice(2));
  if (flags.has("help")) {
    if (flags.size !== 1) throw new Error("--help cannot be combined with other options");
    help();
  } else {
    const url = build(flags);
    if (booleanFlag(flags, "json")) process.stdout.write(`${JSON.stringify({ ok: true, url }, null, 2)}\n`);
    else process.stdout.write(`${url}\n`);
  }
} catch (error) {
  const message = error instanceof Error ? error.message : String(error);
  if (process.argv.includes("--json")) {
    process.stdout.write(`${JSON.stringify({ ok: false, error: { code: "INVALID_INPUT", message } }, null, 2)}\n`);
  } else {
    process.stderr.write(`error: ${message}\n`);
  }
  process.exitCode = 1;
}
