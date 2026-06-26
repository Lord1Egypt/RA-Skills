#!/usr/bin/env node
/* Resolve a CN A-share symbol, fetch daily history, and archive it as raw JSON. */

const fs = require("node:fs/promises");
const path = require("node:path");

const EASTMONEY_LIST_UT = "bd1d9ddb04089700cf9c27f6f7426281";
const EASTMONEY_HISTORY_UT = "7eea3edcaed734bea9cbfc24409ed989";
const DEFAULT_HEADERS = {
  "User-Agent":
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
  Accept: "*/*",
  Referer: "https://quote.eastmoney.com/",
};
const LIST_PAGE_SIZE = 100;
const SYMBOL_CACHE_TTL_MS = 24 * 60 * 60 * 1000;

function parseArgs(argv) {
  const args = {
    symbol: "",
    startDate: "",
    endDate: "",
    years: 5,
    adjust: "qfq",
    baseDir: "data/raw",
  };

  const items = [...argv];
  while (items.length > 0) {
    const current = items.shift();
    if (!current) {
      continue;
    }
    if (!current.startsWith("--") && !args.symbol) {
      args.symbol = current;
      continue;
    }
    if (current === "--start-date") {
      args.startDate = expectValue(current, items.shift());
      continue;
    }
    if (current === "--end-date") {
      args.endDate = expectValue(current, items.shift());
      continue;
    }
    if (current === "--years") {
      args.years = parseInteger(expectValue(current, items.shift()), current);
      continue;
    }
    if (current === "--adjust") {
      args.adjust = expectValue(current, items.shift());
      continue;
    }
    if (current === "--base-dir") {
      args.baseDir = expectValue(current, items.shift());
      continue;
    }
    throw new Error(`unknown argument: ${current}`);
  }

  if (!args.symbol) {
    throw new Error("missing stock symbol or stock name");
  }
  if (!["qfq", "hfq", "none"].includes(args.adjust)) {
    throw new Error(`unsupported adjust mode: ${args.adjust}`);
  }
  if (args.years < 1) {
    throw new Error("--years must be >= 1");
  }
  if (args.startDate) {
    validateYyyymmdd(args.startDate, "--start-date");
  }
  if (args.endDate) {
    validateYyyymmdd(args.endDate, "--end-date");
  }

  return args;
}

function expectValue(flag, value) {
  if (!value || value.startsWith("--")) {
    throw new Error(`missing value for ${flag}`);
  }
  return value;
}

function parseInteger(value, flag) {
  const parsed = Number.parseInt(value, 10);
  if (!Number.isInteger(parsed)) {
    throw new Error(`invalid integer for ${flag}: ${value}`);
  }
  return parsed;
}

function validateYyyymmdd(value, flag) {
  if (!/^\d{8}$/.test(value)) {
    throw new Error(`invalid YYYYMMDD date for ${flag}: ${value}`);
  }
  const year = Number.parseInt(value.slice(0, 4), 10);
  const month = Number.parseInt(value.slice(4, 6), 10);
  const day = Number.parseInt(value.slice(6, 8), 10);
  const parsed = new Date(Date.UTC(year, month - 1, day));
  if (
    parsed.getUTCFullYear() !== year ||
    parsed.getUTCMonth() !== month - 1 ||
    parsed.getUTCDate() !== day
  ) {
    throw new Error(`invalid YYYYMMDD date for ${flag}: ${value}`);
  }
}

function toYyyymmdd(date) {
  const year = date.getUTCFullYear();
  const month = String(date.getUTCMonth() + 1).padStart(2, "0");
  const day = String(date.getUTCDate()).padStart(2, "0");
  return `${year}${month}${day}`;
}

function resolveWindow(args) {
  const referenceEnd = args.endDate ? parseYyyymmdd(args.endDate) : stripToUtcDay(new Date());
  if (args.startDate) {
    const start = args.startDate;
    const end = args.endDate || toYyyymmdd(referenceEnd);
    if (start > end) {
      throw new Error(`start_date ${start} is after end_date ${end}`);
    }
    return { startDate: start, endDate: end };
  }

  const start = new Date(referenceEnd);
  start.setUTCDate(start.getUTCDate() - (365 * args.years + 10));
  return {
    startDate: toYyyymmdd(start),
    endDate: toYyyymmdd(referenceEnd),
  };
}

function parseYyyymmdd(value) {
  return new Date(
    Date.UTC(
      Number.parseInt(value.slice(0, 4), 10),
      Number.parseInt(value.slice(4, 6), 10) - 1,
      Number.parseInt(value.slice(6, 8), 10),
    ),
  );
}

function stripToUtcDay(value) {
  return new Date(Date.UTC(value.getUTCFullYear(), value.getUTCMonth(), value.getUTCDate()));
}

function normalizeRawSymbol(rawSymbol) {
  const trimmed = String(rawSymbol).trim();
  const upper = trimmed.toUpperCase();
  if (/^\d{6}$/.test(upper)) {
    return upper;
  }
  const match = upper.match(/^(\d{6})\.(SH|SZ)$/);
  if (match) {
    return match[1];
  }
  return "";
}

function inferEastmoneySecid(code) {
  if (/^[569]\d{5}$/.test(code)) {
    return `1.${code}`;
  }
  return `0.${code}`;
}

function symbolCachePath() {
  return path.join(process.cwd(), "data", "cache", "eastmoney", "a_share_symbols.json");
}

async function readSymbolCache() {
  const filePath = symbolCachePath();
  try {
    const stat = await fs.stat(filePath);
    if (Date.now() - stat.mtimeMs > SYMBOL_CACHE_TTL_MS) {
      return null;
    }
    return JSON.parse(await fs.readFile(filePath, "utf8"));
  } catch {
    return null;
  }
}

async function writeSymbolCache(payload) {
  const filePath = symbolCachePath();
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, JSON.stringify(payload, null, 2), "utf8");
}

async function fetchJson(url) {
  const response = await fetch(url, {
    headers: DEFAULT_HEADERS,
    signal: AbortSignal.timeout(20000),
  });
  if (!response.ok) {
    throw new Error(`request failed: ${response.status} ${response.statusText}`);
  }
  return response.json();
}

function buildListUrl(pageNumber) {
  const params = new URLSearchParams({
    pn: String(pageNumber),
    pz: String(LIST_PAGE_SIZE),
    po: "1",
    np: "1",
    ut: EASTMONEY_LIST_UT,
    fltt: "2",
    invt: "2",
    fid: "f12",
    fs: "m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048",
    fields: "f12,f13,f14",
  });
  return `https://82.push2.eastmoney.com/api/qt/clist/get?${params.toString()}`;
}

async function fetchListPage(pageNumber) {
  const payload = await fetchJson(buildListUrl(pageNumber));
  if (!payload || !payload.data || !Array.isArray(payload.data.diff)) {
    throw new Error(`unexpected Eastmoney list response on page ${pageNumber}`);
  }
  return payload;
}

async function fetchAllAShares() {
  const firstPage = await fetchListPage(1);
  const total = Number(firstPage.data.total || 0);
  const totalPages = Math.max(1, Math.ceil(total / LIST_PAGE_SIZE));
  const items = [...firstPage.data.diff];
  const pageNumbers = [];
  for (let page = 2; page <= totalPages; page += 1) {
    pageNumbers.push(page);
  }

  const concurrency = 8;
  let index = 0;
  const workers = Array.from({ length: Math.min(concurrency, pageNumbers.length) }, async () => {
    while (index < pageNumbers.length) {
      const current = pageNumbers[index];
      index += 1;
      const payload = await fetchListPage(current);
      items.push(...payload.data.diff);
    }
  });
  await Promise.all(workers);

  return items
    .filter((item) => item && item.f12 && item.f14)
    .map((item) => ({
      code: String(item.f12),
      market: Number(item.f13),
      name: String(item.f14).trim(),
    }));
}

async function loadSymbolMap() {
  const cached = await readSymbolCache();
  if (cached && Array.isArray(cached.items) && cached.items.length > 0) {
    return cached.items;
  }
  const items = await fetchAllAShares();
  await writeSymbolCache({
    fetched_at: new Date().toISOString(),
    items,
  });
  return items;
}

async function resolveSymbol(rawSymbol) {
  const normalizedCode = normalizeRawSymbol(rawSymbol);
  if (normalizedCode) {
    return normalizedCode;
  }

  const trimmed = String(rawSymbol).trim();
  const items = await loadSymbolMap();
  const exact = items.find((item) => item.name === trimmed);
  if (exact) {
    return exact.code;
  }
  const fuzzy = items.find((item) => item.name.includes(trimmed));
  if (fuzzy) {
    return fuzzy.code;
  }
  throw new Error(`无法识别股票代码或名称: ${rawSymbol}`);
}

function buildDailyKlineUrl(code, startDate, endDate, adjust) {
  const fqtMap = {
    none: "0",
    qfq: "1",
    hfq: "2",
  };
  const params = new URLSearchParams({
    fields1: "f1,f2,f3,f4,f5,f6",
    fields2: "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f116",
    ut: EASTMONEY_HISTORY_UT,
    klt: "101",
    fqt: fqtMap[adjust],
    secid: inferEastmoneySecid(code),
    beg: startDate,
    end: endDate,
  });
  return `https://push2his.eastmoney.com/api/qt/stock/kline/get?${params.toString()}`;
}

function toNumber(value) {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

function mapKlineRows(payload) {
  const data = payload && payload.data;
  const klines = data && Array.isArray(data.klines) ? data.klines : [];
  return klines.map((line) => {
    const [
      tradeDate,
      open,
      close,
      high,
      low,
      volume,
      amount,
      amplitude,
      changePercent,
      changeAmount,
      turnoverRate,
    ] = String(line).split(",");
    return {
      日期: tradeDate,
      开盘: toNumber(open),
      收盘: toNumber(close),
      最高: toNumber(high),
      最低: toNumber(low),
      成交量: toNumber(volume),
      成交额: toNumber(amount),
      振幅: toNumber(amplitude),
      涨跌幅: toNumber(changePercent),
      涨跌额: toNumber(changeAmount),
      换手率: toNumber(turnoverRate),
      股票代码: String(data.code || ""),
      股票名称: String(data.name || ""),
    };
  });
}

function utcFolderName(date) {
  return [
    String(date.getUTCFullYear()),
    String(date.getUTCMonth() + 1).padStart(2, "0"),
    String(date.getUTCDate()).padStart(2, "0"),
  ].join("");
}

function utcClockName(date) {
  return [
    String(date.getUTCHours()).padStart(2, "0"),
    String(date.getUTCMinutes()).padStart(2, "0"),
    String(date.getUTCSeconds()).padStart(2, "0"),
  ].join("");
}

async function archiveJson({ baseDir, provider, dataset, symbol, payload, fetchedAt }) {
  const folder = path.join(baseDir, provider, dataset, utcFolderName(fetchedAt));
  await fs.mkdir(folder, { recursive: true });
  const stamp = `${symbol}_${utcClockName(fetchedAt)}`;
  for (let attempt = 0; attempt < 100; attempt += 1) {
    const suffix = attempt === 0 ? "" : `_${String(attempt).padStart(2, "0")}`;
    const filePath = path.join(folder, `${stamp}${suffix}.json`);
    try {
      await fs.writeFile(filePath, JSON.stringify(payload, null, 2), {
        encoding: "utf8",
        flag: "wx",
      });
      return filePath;
    } catch (error) {
      if (error && error.code === "EEXIST") {
        continue;
      }
      throw error;
    }
  }
  throw new Error(`unable to allocate archive filename for ${stamp}`);
}

function tradeDateBounds(rows) {
  const dates = rows
    .map((item) => item["日期"])
    .filter((value) => typeof value === "string" && value.length > 0)
    .sort();
  if (dates.length === 0) {
    return { tradeDateMin: null, tradeDateMax: null };
  }
  return {
    tradeDateMin: dates[0],
    tradeDateMax: dates[dates.length - 1],
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const { startDate, endDate } = resolveWindow(args);
  const fetchedAt = new Date();
  const resolvedSymbol = await resolveSymbol(args.symbol);
  const payload = await fetchJson(
    buildDailyKlineUrl(resolvedSymbol, startDate, endDate, args.adjust),
  );
  const rows = mapKlineRows(payload);
  const outputPath = await archiveJson({
    baseDir: args.baseDir,
    provider: "eastmoney",
    dataset: "daily_history",
    symbol: resolvedSymbol,
    payload: rows,
    fetchedAt,
  });
  const bounds = tradeDateBounds(rows);

  console.log(
    JSON.stringify(
      {
        status: "success",
        provider: "eastmoney",
        input_symbol: args.symbol,
        resolved_symbol: resolvedSymbol,
        rows: rows.length,
        start_date: startDate,
        end_date: endDate,
        adjust: args.adjust === "none" ? "" : args.adjust,
        trade_date_min: bounds.tradeDateMin,
        trade_date_max: bounds.tradeDateMax,
        output_path: outputPath,
      },
      null,
      2,
    ),
  );
}

main().catch((error) => {
  console.error(
    JSON.stringify(
      {
        status: "failed",
        error: error instanceof Error ? error.message : String(error),
      },
      null,
      2,
    ),
  );
  process.exit(1);
});
