import { createHash } from "node:crypto";
import { decimal, amount, multiply, percent } from "./decimal.mjs";

export const CAPTURE_SCHEMA = "hyperliquid-wallet-capture/v1";
export const REPORT_SCHEMA = "hyperliquid-wallet-audit/v1";
export const ENDPOINTS = Object.freeze({ mainnet: "https://api.hyperliquid.xyz/info", testnet: "https://api.hyperliquid-testnet.xyz/info" });
export const sha256 = (text) => createHash("sha256").update(text).digest("hex");
const RESPONSE_LIMIT = 8388608;
const TOTAL_RESPONSE_LIMIT = 67108864;
const SNAPSHOTS = ["userRole", "userAbstraction", "clearinghouseState", "spotClearinghouseState", "frontendOpenOrders"];
const TYPES = [...SNAPSHOTS, "userFillsByTime", "userFunding"];
function object(value, label) { if (!value || typeof value !== "object" || Array.isArray(value)) throw new Error(`${label} must be an object`); return value; }
function array(value, label) { if (!Array.isArray(value)) throw new Error(`${label} must be an array`); return value; }
function text(value, label) { if (typeof value !== "string" || !value.trim()) throw new Error(`${label} must be a nonempty string`); return value.trim(); }
function integer(value, label) { if (!Number.isSafeInteger(value) || value < 0) throw new Error(`${label} must be a nonnegative safe integer`); return value; }
function identifier(value, label) { if (typeof value === "string" && /^\d+$/.test(value)) return value; return String(integer(value, label)); }
function hash(value) { if (typeof value !== "string" || !/^0x[\da-f]{64}$/i.test(value)) throw new Error("invalid history hash"); return value.toLowerCase(); }
function nonnegative(value, label) { const v = decimal(value, label); if (v < 0n) throw new Error(`${label} must be nonnegative`); return v; }
function positive(value, label) { const v = nonnegative(value, label); if (v === 0n) throw new Error(`${label} must be positive`); return v; }
function bool(value, label) { if (typeof value !== "boolean") throw new Error(`${label} must be boolean`); return value; }
function date(value, label) { if (typeof value !== "string" || !/^\d{4}-\d\d-\d\dT/.test(value) || !Number.isFinite(Date.parse(value))) throw new Error(`${label} must be ISO time`); return Date.parse(value); }
export function validateScope(scope) {
  object(scope, "scope");
  if (typeof scope.address !== "string" || !/^0x[\da-f]{40}$/i.test(scope.address)) throw new Error("address must be the queried account's 42-character hexadecimal address");
  if (typeof scope.network !== "string" || !Object.hasOwn(ENDPOINTS, scope.network)) throw new Error("network must be mainnet or testnet");
  integer(scope.startTime, "startTime"); integer(scope.endTime, "endTime");
  if (scope.startTime >= scope.endTime) throw new Error("startTime must be before endTime");
  return scope;
}
function isDefaultPerp(coin) { return !coin.startsWith("@") && !coin.includes("/") && !coin.includes(":"); }
function canonical(value) {
  if (Array.isArray(value)) return `[${value.map(canonical).join(",")}]`;
  if (value && typeof value === "object") return `{${Object.keys(value).sort().map((k) => `${JSON.stringify(k)}:${canonical(value[k])}`).join(",")}}`;
  return JSON.stringify(value);
}

// No signing, user-selected URLs, redirects, write types or automatic retry.
export async function captureWallet(scope, { maxPages = 10, timeoutMs = 15000, fetchImpl = globalThis.fetch, now = () => new Date() } = {}) {
  validateScope(scope);
  integer(maxPages, "maxPages"); integer(timeoutMs, "timeoutMs");
  if (maxPages < 1 || maxPages > 50 || timeoutMs < 1 || timeoutMs > 60000) throw new Error("maxPages must be 1..50 and timeoutMs 1..60000");
  if (scope.endTime > now().getTime()) throw new Error("endTime cannot be in the future");
  const capture = { schema: CAPTURE_SCHEMA, source: "live", scope, bounds: { maxPages, timeoutMs, responseByteLimit: RESPONSE_LIMIT, totalResponseByteLimit: TOTAL_RESPONSE_LIMIT }, startedAt: now().toISOString(), finishedAt: null, evidence: [], history: {} };
  let totalBytes = 0;
  async function read(body) {
    const requestText = JSON.stringify(body);
    const entry = { sequence: capture.evidence.length + 1, endpoint: ENDPOINTS[scope.network], type: body.type, startedAt: now().toISOString(), finishedAt: null, requestText, requestSha256: sha256(requestText), responseText: null, responseSha256: null, httpStatus: null, error: null };
    capture.evidence.push(entry);
    try {
      const response = await fetchImpl(entry.endpoint, { method: "POST", redirect: "error", headers: { "content-type": "application/json" }, body: requestText, signal: AbortSignal.timeout(timeoutMs) });
      entry.httpStatus = response.status;
      const available = Math.min(RESPONSE_LIMIT, TOTAL_RESPONSE_LIMIT - totalBytes);
      if (Number(response.headers?.get?.("content-length")) > available) throw new Error("response exceeds per-read or total response-byte bound");
      // Stream reads are bounded even when content-length is absent or inaccurate.
      if (response.body?.getReader) {
        const reader = response.body.getReader(); const chunks = []; let bytes = 0;
        for (;;) { const { done, value } = await reader.read(); if (done) break; bytes += value.byteLength; if (bytes > available) { await reader.cancel(); throw new Error("response exceeds per-read or total response-byte bound"); } chunks.push(value); }
        entry.responseText = Buffer.concat(chunks).toString("utf8");
      } else { const raw = await response.text(); if (Buffer.byteLength(raw) > available) throw new Error("response exceeds per-read or total response-byte bound"); entry.responseText = raw; }
      totalBytes += Buffer.byteLength(entry.responseText);
      entry.responseSha256 = sha256(entry.responseText);
      if (!response.ok) throw new Error(`HTTP ${response.status}; capture stopped for this read, no automatic retry`);
      return JSON.parse(entry.responseText);
    } catch (error) { entry.error = error instanceof Error ? error.message : String(error); return undefined; }
    finally { entry.finishedAt = now().toISOString(); }
  }
  for (const type of SNAPSHOTS) await read({ type, user: scope.address, ...(type === "clearinghouseState" || type === "frontendOpenOrders" ? { dex: "" } : {}) });
  for (const type of ["userFillsByTime", "userFunding"]) {
    let cursor = scope.startTime; let reason = "page-budget"; let pages = 0; let lastTime = null;
    for (; pages < maxPages;) {
      const data = await read({ type, user: scope.address, startTime: cursor, endTime: scope.endTime, ...(type === "userFillsByTime" ? { aggregateByTime: false } : {}) });
      pages += 1;
      if (data === undefined) { reason = "read-error"; break; }
      if (!Array.isArray(data) || data.some((v) => !Number.isSafeInteger(v?.time) || v.time < cursor || v.time > scope.endTime)) { reason = "invalid-page"; break; }
      if (data.length > 2000 || (type === "userFunding" && data.length > 500)) { reason = "unexpected-page-limit"; break; }
      lastTime = data.length ? Math.max(...data.map((v) => v.time)) : lastTime;
      // The documented general limit is 500 elements/distinct blocks, fills have a 2000-row cap.
      // Continue conservatively at >=500 rows, inclusively, without skipping tied timestamps.
      if (data.length < 500) { reason = "api-exhausted"; break; }
      if (lastTime <= cursor) { reason = "timestamp-stall"; break; }
      cursor = lastTime;
    }
    capture.history[type] = { pages, termination: reason, lastTime, apiExhausted: reason === "api-exhausted", windowCompleteness: "unverified", ...(type === "userFillsByTime" ? { retentionLimit: 10000 } : {}) };
  }
  capture.finishedAt = now().toISOString();
  return capture;
}

function evidenceData(capture) {
  if (capture?.schema !== CAPTURE_SCHEMA || !["live", "fixture"].includes(capture.source)) throw new Error("unsupported capture schema or source");
  validateScope(capture.scope);
  integer(capture.bounds?.maxPages, "bounds.maxPages");
  integer(capture.bounds?.timeoutMs, "bounds.timeoutMs");
  if (capture.bounds.maxPages < 1 || capture.bounds.maxPages > 50) throw new Error("invalid capture page bound");
  if (capture.bounds.timeoutMs < 1 || capture.bounds.timeoutMs > 60000) throw new Error("invalid capture timeout bound");
  if (capture.bounds.responseByteLimit !== RESPONSE_LIMIT || capture.bounds.totalResponseByteLimit !== TOTAL_RESPONSE_LIMIT) throw new Error("invalid response-byte bounds");
  let prior = date(capture.startedAt, "capture.startedAt");
  if (capture.scope.endTime > prior) throw new Error("capture begins before the requested history window ends");
  if (array(capture.evidence, "evidence").length > SNAPSHOTS.length + 2 * capture.bounds.maxPages) throw new Error("evidence exceeds bounded read count");
  let totalBytes = 0;
  const data = new Map();
  const counts = new Map();
  for (const [index, entry] of array(capture.evidence, "evidence").entries()) {
    object(entry, "evidence entry");
    if (entry.sequence !== index + 1 || entry.endpoint !== ENDPOINTS[capture.scope.network] || !TYPES.includes(entry.type)) throw new Error("invalid evidence sequence, endpoint or read type");
    counts.set(entry.type, (counts.get(entry.type) ?? 0) + 1);
    if (SNAPSHOTS.includes(entry.type) && counts.get(entry.type) > 1) throw new Error("duplicate snapshot read");
    const start = date(entry.startedAt, "read.startedAt"); const finish = date(entry.finishedAt, "read.finishedAt");
    if (start < prior || finish < start) throw new Error("reads must be sequential with monotonic timestamps"); prior = finish;
    if (typeof entry.requestText !== "string" || Buffer.byteLength(entry.requestText) > 16384 || entry.requestSha256 !== sha256(entry.requestText)) throw new Error("request SHA256 mismatch or request-byte bound exceeded");
    const request = object(JSON.parse(entry.requestText), "request");
    const permitted = ["type", "user", ...(entry.type === "clearinghouseState" || entry.type === "frontendOpenOrders" ? ["dex"] : []), ...(entry.type === "userFillsByTime" || entry.type === "userFunding" ? ["startTime", "endTime"] : []), ...(entry.type === "userFillsByTime" ? ["aggregateByTime"] : [])];
    if (Object.keys(request).some((key) => !permitted.includes(key)) || request.user?.toLowerCase() !== capture.scope.address.toLowerCase() || request.type !== entry.type || (request.dex !== undefined && request.dex !== "")) throw new Error("request does not match bounded read scope");
    if (entry.type === "userFillsByTime" || entry.type === "userFunding") {
      integer(request.startTime, "request.startTime");
      if (request.startTime < capture.scope.startTime || request.startTime > capture.scope.endTime || request.endTime !== capture.scope.endTime || (entry.type === "userFillsByTime" && request.aggregateByTime !== false)) throw new Error("history request does not match window or unaggregated fill scope");
    }
    if (entry.responseText !== null && (typeof entry.responseText !== "string" || entry.responseSha256 !== sha256(entry.responseText))) throw new Error("response SHA256 mismatch");
    if (entry.responseText !== null) { const bytes = Buffer.byteLength(entry.responseText); totalBytes += bytes; if (bytes > RESPONSE_LIMIT || totalBytes > TOTAL_RESPONSE_LIMIT) throw new Error("response-byte bound exceeded"); }
    else if (entry.responseSha256 !== null) throw new Error("missing response has a digest");
    if (entry.error !== null && (typeof entry.error !== "string" || !entry.error)) throw new Error("invalid read error");
    if (entry.httpStatus !== null && (!Number.isInteger(entry.httpStatus) || entry.httpStatus < 100 || entry.httpStatus > 599)) throw new Error("invalid HTTP status");
    if (entry.httpStatus !== 200 && entry.error === null) throw new Error("unsuccessful HTTP status lacks explicit read error");
    if (entry.error || entry.httpStatus !== 200) continue;
    if (typeof entry.responseText !== "string") throw new Error("successful read lacks response evidence");
    const value = JSON.parse(entry.responseText);
    if (SNAPSHOTS.includes(entry.type) && data.has(entry.type)) throw new Error("duplicate snapshot read");
    if (entry.type === "userFillsByTime" || entry.type === "userFunding") {
      const rows = array(value, entry.type);
      if (rows.length > (entry.type === "userFunding" ? 500 : 2000)) throw new Error("history exceeds documented response limit");
      for (const row of rows) { integer(row?.time, "history.time"); if (row.time < request.startTime || row.time > request.endTime) throw new Error("out-of-window history record"); }
      data.set(entry.type, [...(data.get(entry.type) ?? []), ...rows]);
    } else data.set(entry.type, value);
  }
  if (date(capture.finishedAt, "capture.finishedAt") < prior) throw new Error("capture.finishedAt precedes its evidence");
  return data;
}
function unique(rows, keyOf, label) {
  const seen = new Map(); let duplicates = 0;
  for (const row of rows) { const key = keyOf(row); if (seen.has(key)) { if (canonical(seen.get(key)) !== canonical(row)) throw new Error(`conflicting duplicate ${label}: ${key}`); duplicates += 1; } else seen.set(key, row); }
  return { rows: [...seen.values()].sort((a, b) => a.time - b.time || keyOf(a).localeCompare(keyOf(b))), duplicates };
}
function fillKey(row) { object(row, "fill"); return `${text(row.coin, "fill.coin")}:${identifier(row.tid, "fill.tid")}`; }
function fundingKey(row) { object(row, "funding"); object(row.delta, "funding.delta"); return `${hash(row.hash)}:${integer(row.time, "funding.time")}:${text(row.delta.coin, "funding.coin")}`; }
function metrics() { return { fills: 0, closedPnl: 0n, notional: 0n, funding: 0n, positiveUsdcFees: 0n, rebatesUsdc: 0n, feeByToken: new Map(), builderFeeByToken: new Map(), maker: { fills: 0, notional: 0n }, taker: { fills: 0, notional: 0n }, initialObservedPosition: null }; }
function addFee(map, token, value) { map.set(token, (map.get(token) ?? 0n) + value); }
function outputMetrics(m) {
  const foreign = [...m.feeByToken].some(([token, value]) => token !== "USDC" && value !== 0n);
  return { fillCount: m.fills, closedPnlUsdc: amount(m.closedPnl), signedFeesByToken: Object.fromEntries([...m.feeByToken].sort().map(([k, v]) => [k, amount(v)])), builderFeesIncludedByToken: Object.fromEntries([...m.builderFeeByToken].sort().map(([k, v]) => [k, amount(v)])), fundingUsdc: amount(m.funding), observedNetUsdc: foreign ? null : amount(m.closedPnl - (m.feeByToken.get("USDC") ?? 0n) + m.funding), notionalUsdc: amount(m.notional), maker: { fillCount: m.maker.fills, notionalUsdc: amount(m.maker.notional), notionalSharePercent: percent(m.maker.notional, m.notional) }, taker: { fillCount: m.taker.fills, notionalUsdc: amount(m.taker.notional), notionalSharePercent: percent(m.taker.notional, m.notional) }, initialObservedPosition: m.initialObservedPosition };
}
export function analyzeCapture(capture) {
  const data = evidenceData(capture); const gaps = []; const scope = capture.scope;
  const fills = unique(data.get("userFillsByTime") ?? [], fillKey, "fill");
  const funding = unique(data.get("userFunding") ?? [], fundingKey, "funding");
  const total = metrics(); const byCoin = new Map(); const excluded = { fillCount: 0, fundingCount: 0, coins: new Set() };
  const market = (coin) => { if (!byCoin.has(coin)) byCoin.set(coin, metrics()); return byCoin.get(coin); };
  for (const row of fills.rows) {
    const coin = text(row.coin, "fill.coin"); hash(row.hash); identifier(row.oid, "fill.oid"); integer(row.time, "fill.time");
    const px = positive(row.px, "fill.px"); const sz = positive(row.sz, "fill.sz"); const closedPnl = decimal(row.closedPnl, "fill.closedPnl"); const fee = decimal(row.fee, "fill.fee"); const token = text(row.feeToken, "fill.feeToken"); const startPosition = decimal(row.startPosition, "fill.startPosition");
    bool(row.crossed, "fill.crossed"); if (!["A", "B"].includes(row.side)) throw new Error("fill.side must be A or B"); text(row.dir, "fill.dir");
    const builder = row.builderFee === undefined ? 0n : nonnegative(row.builderFee, "fill.builderFee");
    if (!isDefaultPerp(coin)) { excluded.fillCount += 1; excluded.coins.add(coin); continue; }
    const notional = multiply(px, sz);
    for (const m of [total, market(coin)]) { m.fills += 1; m.closedPnl += closedPnl; m.notional += notional; addFee(m.feeByToken, token, fee); addFee(m.builderFeeByToken, token, builder); if (token === "USDC") { if (fee > 0n) m.positiveUsdcFees += fee; else m.rebatesUsdc -= fee; } const liquidity = row.crossed ? m.taker : m.maker; liquidity.fills += 1; liquidity.notional += notional; }
    const m = market(coin); if (m.initialObservedPosition === null) m.initialObservedPosition = { size: amount(startPosition), time: row.time, meaning: "position before first observed fill; window opening inventory and its earlier costs remain unknown" };
  }
  for (const row of funding.rows) {
    const delta = object(row.delta, "funding.delta"); const coin = text(delta.coin, "funding.coin"); if (delta.type !== "funding") throw new Error("unexpected non-funding delta");
    const value = decimal(delta.usdc, "funding.usdc"); decimal(delta.szi, "funding.szi"); decimal(delta.fundingRate, "funding.fundingRate");
    if (!isDefaultPerp(coin)) { excluded.fundingCount += 1; excluded.coins.add(coin); continue; }
    total.funding += value; market(coin).funding += value;
  }
  const history = {};
  for (const type of ["userFillsByTime", "userFunding"]) {
    const supplied = object(capture.history?.[type], `history.${type}`); const entries = capture.evidence.filter((entry) => entry.type === type);
    integer(supplied.pages, "history.pages");
    if (supplied.pages !== entries.length || supplied.apiExhausted !== (supplied.termination === "api-exhausted") || !["api-exhausted", "page-budget", "read-error", "invalid-page", "unexpected-page-limit", "timestamp-stall"].includes(supplied.termination)) throw new Error("invalid history coverage metadata");
    if (entries.length < 1 || entries.length > capture.bounds.maxPages) throw new Error("history violates page bound");
    let cursor = scope.startTime;
    let actualTermination = "page-budget";
    for (const [index, entry] of entries.entries()) {
      const request = JSON.parse(entry.requestText);
      if (request.startTime !== cursor) throw new Error("history pagination skips an inclusive timestamp boundary");
      if (entry.error) actualTermination = "read-error";
      else {
        const rows = array(JSON.parse(entry.responseText), "history page");
        const latest = rows.length ? Math.max(...rows.map((v) => v.time)) : null;
        actualTermination = rows.length < 500 ? "api-exhausted" : latest <= cursor ? "timestamp-stall" : "page-budget";
        if (latest !== null) cursor = latest;
      }
      if (actualTermination !== "page-budget" && index !== entries.length - 1) throw new Error("history continued after terminating page");
    }
    if (actualTermination !== supplied.termination || (actualTermination === "page-budget" && entries.length !== capture.bounds.maxPages)) throw new Error("history termination does not match captured pages");
    const last = entries.at(-1);
    if (supplied.apiExhausted && (!last || last.error || array(JSON.parse(last.responseText), "last page").length >= 500)) throw new Error("unsupported API-exhausted claim");
    if (!supplied.apiExhausted) gaps.push(`${type}: ${supplied.termination}`);
    history[type] = { ...supplied, windowCompleteness: "unverified", uniqueRecords: type === "userFillsByTime" ? fills.rows.length : funding.rows.length, duplicatesRemoved: type === "userFillsByTime" ? fills.duplicates : funding.duplicates, firstRecordTime: (type === "userFillsByTime" ? fills.rows : funding.rows)[0]?.time ?? null, lastRecordTime: (type === "userFillsByTime" ? fills.rows : funding.rows).at(-1)?.time ?? null };
  }
  for (const type of SNAPSHOTS) if (!data.has(type)) gaps.push(`${type}: unavailable`);
  let positions = null; let balances = null; let orders = null; let gross = 0n; let signed = 0n;
  const state = data.get("clearinghouseState");
  if (state !== undefined) {
    object(state, "clearinghouseState"); integer(state.time, "account.time"); object(state.marginSummary, "marginSummary");
    for (const key of ["accountValue", "totalMarginUsed", "totalNtlPos", "totalRawUsd"]) decimal(state.marginSummary[key], `marginSummary.${key}`);
    const seen = new Set();
    positions = array(state.assetPositions, "assetPositions").map((item) => {
      const p = object(item.position, "position"); const coin = text(p.coin, "position.coin"); if (!isDefaultPerp(coin) || seen.has(coin)) throw new Error("unexpected market or duplicate position in default DEX state"); seen.add(coin);
      const size = decimal(p.szi, "position.szi"); const value = nonnegative(p.positionValue, "position.positionValue"); const margin = nonnegative(p.marginUsed, "position.marginUsed"); const pnl = decimal(p.unrealizedPnl, "position.unrealizedPnl");
      const entry = p.entryPx === null ? null : amount(positive(p.entryPx, "position.entryPx")); const liquidation = p.liquidationPx === null ? null : amount(positive(p.liquidationPx, "position.liquidationPx"));
      gross += value; signed += size < 0n ? -value : size > 0n ? value : 0n;
      return { coin, signedSize: amount(size), side: size < 0n ? "short" : size > 0n ? "long" : "flat", notionalUsdc: amount(value), marginUsedUsdc: amount(margin), unrealizedPnlUsdc: amount(pnl), entryPrice: entry, liquidationPrice: liquidation };
    }).sort((a, b) => a.coin.localeCompare(b.coin));
    for (const p of positions) p.grossExposureSharePercent = percent(decimal(p.notionalUsdc), gross);
  }
  const spot = data.get("spotClearinghouseState");
  if (spot !== undefined) { object(spot, "spotClearinghouseState"); balances = array(spot.balances, "balances").map((b) => ({ coin: text(b.coin, "balance.coin"), token: integer(b.token, "balance.token"), total: amount(nonnegative(b.total, "balance.total")), hold: amount(nonnegative(b.hold, "balance.hold")) })); }
  const orderRows = data.get("frontendOpenOrders");
  if (orderRows !== undefined) {
    const ids = new Set(); orders = array(orderRows, "openOrders").map((o) => {
      const oid = identifier(o.oid, "order.oid"); if (ids.has(oid)) throw new Error("duplicate open-order identity"); ids.add(oid);
      const coin = text(o.coin, "order.coin"); if (!["A", "B"].includes(o.side)) throw new Error("invalid order side"); integer(o.timestamp, "order.timestamp");
      return { coin, oid, side: o.side, size: amount(nonnegative(o.sz, "order.sz")), limitPrice: amount(nonnegative(o.limitPx, "order.limitPx")), reduceOnly: bool(o.reduceOnly, "order.reduceOnly"), isTrigger: bool(o.isTrigger, "order.isTrigger"), orderType: text(o.orderType, "order.orderType"), timestamp: o.timestamp, scope: isDefaultPerp(coin) ? "default-perp" : "spot" };
    });
  }
  const mode = data.get("userAbstraction") ?? null;
  if (mode !== null && !["unifiedAccount", "portfolioMargin", "disabled", "default", "dexAbstraction"].includes(mode)) throw new Error("unsupported user abstraction mode");
  const role = data.get("userRole"); if (role !== undefined && !["missing", "user", "agent", "vault", "subAccount"].includes(object(role, "userRole").role)) throw new Error("unsupported user role");
  if (role?.role === "agent") gaps.push("queried address is an agent wallet; query the actual user account");
  if (role?.role === "missing") gaps.push("queried account is missing; empty activity is not proof of the intended account");
  if (Object.keys(outputMetrics(total).signedFeesByToken).some((t) => t !== "USDC")) gaps.push("non-USDC fees are unvalued; no currency conversion performed");
  const coins = [...byCoin].sort(([a], [b]) => a.localeCompare(b)).map(([coin, m]) => ({ coin, ...outputMetrics(m) }));
  // Positive costs and negative rebates are separate, so their shares never divide by a net-zero fee total.
  const positiveUsdcFees = total.positiveUsdcFees;
  const rebatesUsdc = total.rebatesUsdc;
  const costConcentration = coins.filter((c) => c.fillCount > 0).map((c) => { const paid = byCoin.get(c.coin).positiveUsdcFees; return { coin: c.coin, positiveFeesUsdc: amount(paid), positiveFeeSharePercent: percent(paid, positiveUsdcFees), notionalSharePercent: percent(decimal(c.notionalUsdc), total.notional) }; }).sort((a, b) => Number(b.positiveFeeSharePercent ?? 0) - Number(a.positiveFeeSharePercent ?? 0) || a.coin.localeCompare(b.coin));
  const output = outputMetrics(total);
  if (!data.has("userFillsByTime") || !data.has("userFunding")) output.observedNetUsdc = null;
  return {
    schema: REPORT_SCHEMA, source: capture.source,
    scope: { ...scope, dex: "", accountedMarkets: "validator-operated perpetuals only", snapshotMeaning: "state at sequential capture time, not historical state at window end" },
    coverage: { status: gaps.length ? "partial" : "bounded", completeWindow: false, gaps, history, excluded: { ...excluded, coins: [...excluded.coins].sort() }, historyRetention: "Only the 10000 most recent fills are available; API exhaustion does not prove a complete window." },
    outcome: { currency: "USDC", ...output, byCoin: coins, meaning: "Observed closedPnl minus signed fees plus signed funding; does not include unseen earlier fees, deposits, transfers, spot accounting or unrealized PnL." },
    execution: { maker: outputMetrics(total).maker, taker: outputMetrics(total).taker, positiveFeesUsdc: amount(positiveUsdcFees), rebatesUsdc: amount(rebatesUsdc), costConcentration },
    exposure: { accountMode: mode, userRole: role?.role ?? null, accountSnapshotTime: state?.time ?? null, accountSnapshotAgeAtCaptureMs: state ? Date.parse(capture.finishedAt) - state.time : null, reportedMarginSummary: state?.marginSummary ?? null, balanceInterpretation: mode === "unifiedAccount" || mode === "portfolioMargin" ? "Spot balances are the trading-balance source; do not add perp accountValue to spot balances." : "Default-perp margin summary and spot token balances are distinct observations; account mode and other DEX exposure limit interpretation.", spotTokenBalances: balances, positions, grossNotionalUsdc: positions === null ? null : amount(gross), signedNetNotionalUsdc: positions === null ? null : amount(signed), protectionStatus: "not-assessed" },
    openOrders: { orders, protectionMeaning: "Trigger and reduceOnly flags describe observed orders; they do not prove stop coverage, valid trigger prices, or protection across sequential reads." },
    evidence: { startedAt: capture.startedAt, finishedAt: capture.finishedAt, readSpanMs: Date.parse(capture.finishedAt) - Date.parse(capture.startedAt), sequential: true, sha256Verified: true, entries: capture.evidence.map(({ responseText, requestText, ...entry }) => entry), integrityMeaning: "SHA256 verifies the captured bytes against this manifest; it does not independently authenticate the exchange or prove unchanged market state." },
    limitations: ["Opening inventory, historical equity and all cashflows are not reconstructed; no return percentage, portfolio score, win rate, copy ranking or strategy-validation claim.", "Spot and HIP-3 history may be captured but is excluded from this default-perp outcome and exposure. Subaccounts, vaults, staking and lending are not enumerated.", "Funding signs are account cashflows; negative fees are rebates. builderFee is already included in fee and is never subtracted twice.", "Amounts use exact decimal addition; price-times-size notional truncates toward zero at 18 decimal places. Percentages are descriptive rounded ratios.", "Read failures, pagination budgets or timestamp stalls remain explicit gaps; empty results do not verify the intended user identity."]
  };
}

export function renderReport(report) {
  const value = report.outcome.observedNetUsdc ?? "unavailable";
  const share = (percent) => percent === null ? "not defined (zero observed notional)" : `${percent}%`;
  const lines = [`# Hyperliquid wallet audit`, "", `Source: ${report.source}. Account: ${report.scope.address}. Network: ${report.scope.network}.`, "", `Window: ${new Date(report.scope.startTime).toISOString()} to ${new Date(report.scope.endTime).toISOString()} (inclusive).`, "", `Observed default-perp outcome: ${value} USDC. Closed PnL ${report.outcome.closedPnlUsdc}; signed USDC fees ${report.outcome.signedFeesByToken.USDC ?? "0"}; funding ${report.outcome.fundingUsdc}.`, "", `Coverage: ${report.coverage.status}; complete window: unverified. Maker notional share: ${share(report.execution.maker.notionalSharePercent)}; taker: ${share(report.execution.taker.notionalSharePercent)}.`, "", `Current gross default-perp exposure: ${report.exposure.grossNotionalUsdc ?? "unavailable"} USDC. Protection: not assessed.`, "", "## Cost concentration", "", "| Market | Positive fees USDC | Fee share % | Notional share % |", "| --- | --- | --- | --- |"];
  for (const c of report.execution.costConcentration) lines.push(`| ${c.coin} | ${c.positiveFeesUsdc} | ${c.positiveFeeSharePercent ?? "not defined"} | ${c.notionalSharePercent ?? "not defined"} |`);
  lines.push("", "## Evidence and gaps", "", `Sequential reads: ${report.evidence.entries.length}; span ${report.evidence.readSpanMs} ms. SHA256 verified. These hashes establish manifest integrity, not independent authenticity.`, "", report.coverage.historyRetention, "", ...report.coverage.gaps.map((gap) => `- ${gap}`), "", "## Limits", "", ...report.limitations.map((limit) => `- ${limit}`), "");
  return lines.join("\n");
}
