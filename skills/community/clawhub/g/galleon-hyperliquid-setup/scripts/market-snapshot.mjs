#!/usr/bin/env node
import { parseArgs } from "node:util";
import { readFile } from "node:fs/promises";
import { realpathSync } from "node:fs";
import { pathToFileURL } from "node:url";

const endpoints = { mainnet: "https://api.hyperliquid.xyz/info", testnet: "https://api.hyperliquid-testnet.xyz/info" };
function number(value, name, positive = false, allowNegative = false) {
  if (typeof value !== "string" || !/^[-]?(?:0|[1-9]\d*)(?:\.\d+)?(?:e[+-]?\d+)?$/i.test(value) || !Number.isFinite(Number(value)) || (positive && Number(value) <= 0) || (!allowNegative && Number(value) < 0)) throw new Error(`Invalid ${name}`);
  return Number(value);
}
export function summarize(metaAndAssetCtxs, book, coin, source, now = Date.now()) {
  if (!Array.isArray(metaAndAssetCtxs) || metaAndAssetCtxs.length !== 2 || !Array.isArray(metaAndAssetCtxs[0]?.universe) || !Array.isArray(metaAndAssetCtxs[1])) throw new Error("Invalid market metadata response");
  const [meta, contexts] = metaAndAssetCtxs;
  if (meta.universe.length !== contexts.length) throw new Error("Metadata/context length mismatch");
  const matches = meta.universe.map((m, i) => m.name === coin ? i : -1).filter(i => i >= 0);
  if (matches.length !== 1) throw new Error("Market missing or ambiguous; use an exact validator-operated perpetual market name");
  const market = meta.universe[matches[0]], context = contexts[matches[0]];
  if (market.isDelisted || !Number.isInteger(market.szDecimals) || market.szDecimals < 0 || market.szDecimals > 18 || !context) throw new Error("Unsupported or invalid market");
  if (book?.coin !== coin || !Array.isArray(book.levels) || book.levels.length !== 2 || book.levels.some(side => !Array.isArray(side) || side.length === 0)) throw new Error("Missing or mismatched order book");
  if (!Number.isFinite(book.time) || book.time <= 0) throw new Error("Invalid book timestamp");
  const age = now - book.time;
  if (source === "live" && (age > 60_000 || age < -5_000)) throw new Error("Stale or future-dated order book");
  const sides = book.levels.map(side => side.map(level => {
    const price = number(level.px, "book price", true), size = number(level.sz, "book size", true);
    return { price, size };
  }));
  for (let i = 1; i < sides[0].length; i++) if (sides[0][i].price > sides[0][i - 1].price) throw new Error("Unsorted bids");
  for (let i = 1; i < sides[1].length; i++) if (sides[1][i].price < sides[1][i - 1].price) throw new Error("Unsorted asks");
  const bid = sides[0][0].price, ask = sides[1][0].price;
  if (bid >= ask) throw new Error("Crossed or locked book");
  return {
    source, observedAt: new Date(now).toISOString(), coin, szDecimals: market.szDecimals,
    markPrice: number(context.markPx, "mark price", true), oraclePrice: number(context.oraclePx, "oracle price", true),
    fundingRateReported: number(context.funding, "funding rate", false, true),
    openInterest: number(context.openInterest, "open interest"), dayNotionalVolume: number(context.dayNtlVlm, "daily volume"),
    book: { time: book.time, ageMs: source === "live" ? age : null, bid, ask, spreadBps: (ask - bid) / ((ask + bid) / 2) * 10000, returnedLevels: sides.map(side => side.length) },
    limits: ["Two sequential public reads, not an atomic snapshot", "Book depth is only the returned page", "Funding interval must be verified before normalization", "No account state, trade recommendation, or execution readiness established"],
  };
}
async function request(endpoint, body) {
  const response = await fetch(endpoint, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(body), redirect: "error", signal: AbortSignal.timeout(10000) });
  if (!response.ok) throw new Error(`Public info request failed: HTTP ${response.status}`);
  let text = "", bytes = 0;
  for await (const chunk of response.body ?? []) {
    bytes += chunk.byteLength;
    if (bytes > 2_000_000) throw new Error("Info response exceeds size limit");
    text += new TextDecoder().decode(chunk, { stream: true });
  }
  return JSON.parse(text);
}
async function main() {
  const { values } = parseArgs({ options: { coin: { type: "string" }, network: { type: "string", default: "mainnet" }, fixture: { type: "string" }, help: { type: "boolean" } } });
  if (values.help) return console.log("node market-snapshot.mjs --coin ETH [--network mainnet|testnet] [--fixture file.json]\nPublic market reads only. A fixture performs no network requests.");
  if (!values.coin || !/^[A-Za-z0-9:_./-]{1,80}$/.test(values.coin) || !Object.hasOwn(endpoints, values.network)) throw new Error("Supply an exact --coin and mainnet or testnet --network");
  if (values.coin.includes(":")) throw new Error("This helper supports validator-operated perpetual markets only");
  const requests = [{ type: "metaAndAssetCtxs" }, { type: "l2Book", coin: values.coin }];
  let meta, book;
  if (values.fixture) ({ metaAndAssetCtxs: meta, l2Book: book } = JSON.parse(await readFile(values.fixture, "utf8")));
  else { meta = await request(endpoints[values.network], requests[0]); book = await request(endpoints[values.network], requests[1]); }
  const result = summarize(meta, book, values.coin, values.fixture ? "fixture" : "live");
  console.log(JSON.stringify({ network: values.network, endpoint: endpoints[values.network], requests, ...result }, null, 2));
}
if (process.argv[1] && import.meta.url === pathToFileURL(realpathSync(process.argv[1])).href) main().catch(() => { console.error("Market snapshot unavailable. Check network, exact coin/DEX, response shape, and freshness; no trading request was made."); process.exitCode = 1; });
