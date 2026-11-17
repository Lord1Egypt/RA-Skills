import { readFile, stat } from "node:fs/promises";
import { fileURLToPath } from "node:url";

const decimal = /^(?:0|[1-9]\d*)(?:\.\d+)?$/;
function amount(value, label) {
  if (typeof value !== "string" || !decimal.test(value)) throw new Error(`${label} must be a nonnegative decimal string`);
  const result = Number(value);
  if (!Number.isFinite(result) || result > Number.MAX_SAFE_INTEGER) throw new Error(`${label} exceeds research arithmetic limits`);
  return result;
}
function levels(value, label) {
  if (!Array.isArray(value)) throw new Error(`${label} must be an array`);
  if (value.length > 10000) throw new Error(`${label} exceeds the 10000-level research limit`);
  const prices = new Set();
  return value.map(level => {
    if (!level || typeof level !== "object") throw new Error(`Malformed ${label} level`);
    const price = amount(level.price, "price"), size = amount(level.size, "size");
    if (price <= 0 || price >= 1 || size <= 0) throw new Error("Open-market levels need 0 < price < 1 and size > 0");
    if (prices.has(price)) throw new Error(`Duplicate aggregated price level in ${label}`);
    prices.add(price);
    return { price, size };
  });
}

export function summarizeBook(book, { assetId, shares, nowMs, maxAgeMs }) {
  if (!book || typeof book !== "object" || Array.isArray(book)) throw new Error("Book must be an object");
  if (typeof assetId !== "string" || !/^[1-9]\d*$/.test(assetId)) throw new Error("assetId must be a nonzero decimal string");
  if (book.assetId !== undefined && book.asset_id !== undefined && book.assetId !== book.asset_id) throw new Error("Conflicting book identifiers");
  if ((book.assetId ?? book.asset_id) !== assetId) throw new Error("Book outcome identity mismatch");
  if (!Number.isFinite(shares) || shares <= 0 || shares > Number.MAX_SAFE_INTEGER) throw new Error("shares must be positive and within research arithmetic limits");
  if (!Number.isSafeInteger(nowMs) || nowMs <= 0 || !Number.isSafeInteger(maxAgeMs) || maxAgeMs < 0) throw new Error("Time bounds must be valid epoch milliseconds");
  const bids = levels(book.bids, "bids"), asks = levels(book.asks, "asks");
  const bestBid = bids.reduce((best, level) => best === null ? level.price : Math.max(best, level.price), null);
  const bestAsk = asks.reduce((best, level) => best === null ? level.price : Math.min(best, level.price), null);
  let observedAtMs = null;
  if (book.timestamp !== undefined && book.timestamp !== null) {
    if (typeof book.timestamp !== "string" && typeof book.timestamp !== "number") throw new Error("timestamp must be epoch milliseconds");
    if (typeof book.timestamp === "string" && !/^\d+$/.test(book.timestamp)) throw new Error("timestamp must be epoch milliseconds");
    observedAtMs = Number(book.timestamp);
    if (!Number.isSafeInteger(observedAtMs) || observedAtMs <= 0) throw new Error("timestamp must be positive epoch milliseconds");
  }
  const ageMs = observedAtMs === null ? null : nowMs - observedAtMs;
  const freshness = ageMs === null ? "unknown" : ageMs < 0 ? "future" : ageMs > maxAgeMs ? "stale" : "fresh";
  const crossed = bestAsk !== null && bestBid !== null && bestBid >= bestAsk;
  let remainingShares = shares, filledShares = 0, grossCost = 0;
  for (const level of [...asks].sort((a, b) => a.price - b.price)) {
    const take = Math.min(remainingShares, level.size);
    grossCost += take * level.price;
    filledShares += take;
    remainingShares -= take;
    if (remainingShares <= 0) break;
  }
  return {
    assetId, observedAtMs, comparedAtMs: nowMs, ageMs, maxAgeMs, freshness,
    bestBid, bestAsk, spread: bestBid === null || bestAsk === null ? null : bestAsk - bestBid,
    crossed, hash: typeof book.hash === "string" ? book.hash : null,
    hypotheticalBuy: { requestedShares: shares, filledShares, remainingShares, grossCost, vwap: filledShares ? grossCost / filledShares : null, complete: remainingShares === 0 },
    usableForCurrentResearch: freshness === "fresh" && !crossed && bestAsk !== null && bestBid !== null,
    limitations: ["Approximate research arithmetic; not executable amounts", "Excludes fees and later book changes", "Does not establish eligibility, probability, resolution or execution"],
  };
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  try {
    const args = process.argv.slice(2), options = new Map();
    for (let i = 0; i < args.length; i += 2) {
      if (!["--file", "--asset", "--shares", "--now-ms", "--max-age-ms"].includes(args[i]) || !args[i + 1] || options.has(args[i])) throw new Error("Use --file --asset --shares --now-ms --max-age-ms once each");
      options.set(args[i], args[i + 1]);
    }
    if (options.size !== 5) throw new Error("All five arguments are required");
    const file = options.get("--file"), maximumBytes = 2 * 1024 * 1024;
    const info = await stat(file);
    if (!info.isFile() || info.size > maximumBytes) throw new Error("Book must be a regular file of at most 2 MiB");
    const bytes = await readFile(file);
    if (bytes.byteLength > maximumBytes) throw new Error("Book exceeds the 2 MiB research limit");
    const book = JSON.parse(bytes.toString("utf8"));
    console.log(JSON.stringify(summarizeBook(book, { assetId: options.get("--asset"), shares: amount(options.get("--shares"), "shares"), nowMs: Number(options.get("--now-ms")), maxAgeMs: Number(options.get("--max-age-ms")) }), null, 2));
  } catch (error) {
    // File contents are observations, never executable source.
    console.error(error instanceof SyntaxError ? "Invalid book JSON" : error instanceof Error ? error.message : "Book summary failed");
    process.exitCode = 1;
  }
}
