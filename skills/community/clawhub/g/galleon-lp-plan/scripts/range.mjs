#!/usr/bin/env node

const MIN_TICK = -887272;
const MAX_TICK = 887272;
const LN_1_0001 = Math.log(1.0001);
const LN_10 = Math.log(10);

function parse(args) {
  const flags = new Map();
  for (let index = 0; index < args.length; index += 1) {
    const key = args[index];
    if (!key?.startsWith("--")) throw new Error(`unexpected argument: ${key}`);
    if (key === "--help") return new Map([["help", true]]);
    const value = args[index + 1];
    if (value === undefined || value.startsWith("--")) throw new Error(`${key} requires a value`);
    flags.set(key.slice(2), value);
    index += 1;
  }
  return flags;
}

function readNumber(flags, key, fallback) {
  const raw = flags.get(key);
  if (raw === undefined && fallback !== undefined) return fallback;
  const value = Number(raw);
  if (!Number.isFinite(value)) throw new Error(`--${key} must be a finite number`);
  return value;
}

function main() {
  const flags = parse(process.argv.slice(2));
  if (flags.has("help")) {
    process.stdout.write("Usage: node scripts/range.mjs --price <token1-per-token0> --width <percent-per-side> --tick-spacing <integer> [--decimals0 <integer>] [--decimals1 <integer>]\n");
    return;
  }
  const allowed = new Set(["price", "width", "tick-spacing", "decimals0", "decimals1"]);
  for (const key of flags.keys()) if (!allowed.has(key)) throw new Error(`unknown option: --${key}`);
  const price = readNumber(flags, "price");
  const width = readNumber(flags, "width");
  const spacing = readNumber(flags, "tick-spacing");
  const decimals0 = readNumber(flags, "decimals0", 18);
  const decimals1 = readNumber(flags, "decimals1", 18);
  if (price <= 0) throw new Error("price must be greater than 0");
  if (width <= 0 || width >= 100) throw new Error("width must be greater than 0 and less than 100");
  if (!Number.isInteger(spacing) || spacing <= 0) throw new Error("tick-spacing must be a positive integer");
  if (![decimals0, decimals1].every((value) => Number.isInteger(value) && value >= 0 && value <= 36)) {
    throw new Error("decimals must be integers between 0 and 36");
  }
  const toTick = (humanPrice) => (Math.log(humanPrice) + (decimals1 - decimals0) * LN_10) / LN_1_0001;
  const toPrice = (tick) => Math.exp(tick * LN_1_0001 + (decimals0 - decimals1) * LN_10);
  const rawCurrent = toTick(price);
  const rawLower = toTick(price * (1 - width / 100));
  const rawUpper = toTick(price * (1 + width / 100));
  if (rawCurrent < MIN_TICK || rawCurrent > MAX_TICK) throw new Error("price is outside supported tick bounds");
  if (rawLower < MIN_TICK || rawUpper > MAX_TICK) throw new Error("requested price interval exceeds supported tick bounds");
  const minimum = Math.ceil(MIN_TICK / spacing) * spacing;
  const maximum = Math.floor(MAX_TICK / spacing) * spacing;
  const clamp = (value) => Math.min(maximum, Math.max(minimum, value));
  const requestedLower = price * (1 - width / 100);
  const requestedUpper = price * (1 + width / 100);
  const tickLower = clamp(Math.floor(rawLower / spacing) * spacing);
  const tickUpper = clamp(Math.ceil(rawUpper / spacing) * spacing);
  if (tickLower >= tickUpper) throw new Error("snapped range is empty; increase width or verify tick spacing");
  process.stdout.write(`${JSON.stringify({
    ok: true,
    orientation: "token1 per token0",
    tickCurrent: Math.floor(rawCurrent),
    tickLower,
    tickUpper,
    requestedPriceLower: requestedLower,
    requestedPriceUpper: requestedUpper,
    snappedPriceLower: toPrice(tickLower),
    snappedPriceUpper: toPrice(tickUpper),
  }, null, 2)}\n`);
}

try {
  main();
} catch (error) {
  process.stdout.write(`${JSON.stringify({ ok: false, error: error instanceof Error ? error.message : String(error) })}\n`);
  process.exitCode = 1;
}
