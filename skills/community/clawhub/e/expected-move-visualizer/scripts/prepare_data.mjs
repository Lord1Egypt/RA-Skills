#!/usr/bin/env node
//
// prepare_data.mjs: fetch everything the expected-move template needs, in one command.
//
//   SENTISENSE_API_KEY=... node scripts/prepare_data.mjs TSLA
//
// Emits one JSON object on stdout, shaped exactly for the template's data slot. Nothing is
// derived here that the template also derives: the expected-move math lives in the template,
// written once and reviewed once, so a chart cannot disagree with itself across runs.
//
// Zero dependencies on purpose. Plain fetch, Node 18+, no install step, nothing to audit but
// this file.

import { resolve } from "node:path";
import { fileURLToPath } from "node:url";

const API_ORIGIN = "https://app.sentisense.ai";
const KEY = process.env.SENTISENSE_API_KEY;

const SKILL_SLUG = "expected-move-visualizer";
const MAX_IDENTITY = 32;

/**
 * Reduce a volunteered name to a single safe token, matching the official CLI's rule so the
 * same agent identifies the same way whichever path it takes.
 *
 * Order matters. Whitespace collapses to hyphens BEFORE the strip, so "research desk" stays
 * "research-desk" instead of becoming "researchdesk"; the length cap is applied BEFORE the
 * edge trim, so a truncation that lands on a hyphen does not leave one dangling. The strip is
 * a positive allowlist, which is what stops anything user-supplied from reshaping the header:
 * a value carrying a newline, a quote, a semicolon or a parenthesis cannot close the comment
 * or start a second header line, because none of those characters survive.
 */
function sanitizeIdentity(value) {
  return String(value || "")
    .trim()
    .replace(/\s+/g, "-")
    .replace(/[^A-Za-z0-9._-]/g, "")
    .replace(/-{2,}/g, "-")
    .slice(0, MAX_IDENTITY)
    .replace(/^-+|-+$/g, "");
}

// The skill slug leads as a bare token, and a volunteered agent name follows it inside the
// same parenthesized comment, exactly as the CLI composes it. Both are optional to the server
// and nothing is inferred when the name is absent, so with no SENTISENSE_AGENT_NAME set the
// comment carries the slug alone rather than an empty agent token.
const AGENT_NAME = sanitizeIdentity(process.env.SENTISENSE_AGENT_NAME);
const UA = "node/prepare_data (" + SKILL_SLUG + (AGENT_NAME ? "; agent/" + AGENT_NAME : "") + ")";

// Sessions per year for annualizing a realized-volatility figure computed from daily closes.
// Calendar days (365) are the right denominator for the implied cone, which spans wall-clock
// time to an expiry; trading days are the right one here, because the sample is one return
// per session. Mixing the two is the classic way to publish a realized number that looks
// 25% too low next to the implied one it is drawn against.
const SESSIONS_PER_YEAR = 252;
// Short and medium windows, plus the whole sample as a third. A fixed 252 is NOT a usable
// third window: the one-year chart returns about 251 daily bars, which is 251 closes and
// therefore 250 returns, so a 252-session window silently never computes. The full-sample
// entry reports the session count it actually used instead of implying a year it did not get.
const RV_WINDOWS = [20, 60];
// The reactions panel is the last eight reported quarters. The endpoint serves up to twelve
// and carries no limit parameter, so the slice happens here.
const MAX_REACTIONS = 8;

function die(message, hint) {
  process.stderr.write(`prepare_data: ${message}\n`);
  if (hint) process.stderr.write(`  ${hint}\n`);
  process.exit(1);
}

export function sentisenseApiUrl(path) {
  const url = new URL(path, API_ORIGIN);
  if (url.protocol !== "https:" || url.hostname !== "app.sentisense.ai"
      || url.port !== "" || url.username !== "" || url.password !== ""
      || url.origin !== API_ORIGIN) {
    throw new Error("API URL must use https://app.sentisense.ai with no credentials or port");
  }
  return url;
}

async function get(path, { allowNullData = false, tolerate400 = false, optional = false } = {}) {
  // A load-bearing call exits the process with a message. An optional context call THROWS
  // instead, so the caller's try/catch can soften the artifact rather than losing it. Auth
  // failures always exit, optional or not, because a rejected key dooms every call.
  const fail = (msg, hint) => {
    if (optional) throw new Error(hint ? `${msg} (${hint})` : msg);
    die(msg, hint);
  };
  let response;
  try {
    const url = sentisenseApiUrl(path);
    response = await fetch(url, {
      redirect: "error",
      headers: { "X-SentiSense-API-Key": KEY, Accept: "application/json", "User-Agent": UA },
    });
  } catch (cause) {
    fail(`network error calling ${path}`, String(cause && cause.message ? cause.message : cause));
  }

  if (response.status === 401 || response.status === 403) {
    die(
      "the API rejected the key",
      "Check SENTISENSE_API_KEY. A free key comes from https://app.sentisense.ai/get-api-key",
    );
  }
  if (response.status === 429) {
    const wait = response.headers.get("Retry-After");
    fail("rate limited", wait ? `Retry after ${wait}s.` : "Wait a minute and retry.");
  }
  // A 400 is sometimes routing advice rather than a failure: the quote endpoints are split by
  // instrument type and the stock one names the ETF path in its error. Hand the body back so the
  // caller can act on it instead of dying on a recoverable answer.
  if (response.status === 400 && tolerate400) {
    let err = {};
    try { err = await response.json(); } catch { /* not JSON, treat as opaque */ }
    return { data: null, isPreview: false, error: err };
  }
  if (!response.ok) {
    fail(`${path} answered HTTP ${response.status}`);
  }

  const body = await response.json();
  // The preview envelope wraps some endpoints and not others. Unwrap when it is there, so the
  // rest of this script reads one shape.
  const enveloped = body && typeof body === "object" && "isPreview" in body && "data" in body;
  const data = enveloped ? body.data : body;
  if (!allowNullData && (data === null || data === undefined)) {
    fail(`${path} returned no data`);
  }
  return {
    data,
    isPreview: enveloped ? body.isPreview === true : false,
    // A preview can carry the size of the whole window it was cut from. Kept so a caller can
    // tell "this slice is empty" apart from "the window is empty".
    totalCount: enveloped && typeof body.totalCount === "number" ? body.totalCount : null,
  };
}

function num(v) {
  return typeof v === "number" && isFinite(v) ? v : null;
}

/**
 * Read the implied-volatility inputs out of an options summary `data` object, in either shape
 * the endpoint serves. A full dossier nests them under `latest` and `context`. A free key past
 * its monthly full-dossier allowance gets the headline preview instead, which carries `atmIv`
 * and `ivRank1y` flattened directly under `data` and none of the term structure or 25-delta
 * legs, so those come back null and the template draws the 30 day band alone, untilted.
 */
export function readOptionsIv(data) {
  const d = data && typeof data === "object" ? data : {};
  const latest = d.latest && typeof d.latest === "object" ? d.latest : d;
  const context = d.context && typeof d.context === "object" ? d.context : d;
  return {
    atm30: num(latest.atmIv),
    atm60: num(latest.atmIv60),
    atm90: num(latest.atmIv90),
    // The 25-delta legs are what let the cone tilt. skew25d == iv25p - iv25c, so a positive
    // skew means puts are bid richer than calls and the downside half of the cone is wider.
    call25: num(latest.iv25c),
    put25: num(latest.iv25p),
    skew25d: num(latest.skew25d),
    rank1y: num(context.ivRank1y),
  };
}

/** Today's date in US Eastern time, YYYY-MM-DD: the calendar the earnings endpoint keys on. */
export function easternToday(now = new Date()) {
  return new Intl.DateTimeFormat("en-CA", {
    timeZone: "America/New_York", year: "numeric", month: "2-digit", day: "2-digit",
  }).format(now);
}

/**
 * Pick the next report out of an earnings calendar response, and say how far the answer goes.
 *
 * `cal` is the unwrapped `data` ({ earnings, metadata }); `isPreview` and `totalCount` come from
 * the envelope. The default calendar window opens on the Monday of the current week, so a row
 * can be a report that already happened earlier this week: only rows dated `today` or later
 * count as next. A free key sees only one week of the window while `totalCount` still counts
 * the whole of it, so an empty slice with a larger `totalCount` means the report sits past the
 * preview week, not that nothing is scheduled.
 *
 * Returns { nextEarnings, status }, status being one of:
 *   "scheduled"        nextEarnings is the first report dated today or later
 *   "not_scheduled"    the window returned holds no upcoming report
 *   "outside_preview"  a preview slice left rows out, so the next date is unknown here
 */
export function pickNextEarnings(cal, { isPreview = false, totalCount = null, today } = {}) {
  const rows = cal && Array.isArray(cal.earnings) ? cal.earnings : [];
  const upcoming = rows
    .filter((e) => e && typeof e.earningsDate === "string" && e.earningsDate.slice(0, 10) >= today)
    .sort((a, b) => a.earningsDate.localeCompare(b.earningsDate));
  if (upcoming.length) {
    const event = upcoming[0];
    return {
      status: "scheduled",
      nextEarnings: {
        date: event.earningsDate,
        // `earningsTime` is always one of before_open, after_close, during_market or unknown.
        // "unknown" is a real reading (timing not published, or a weekend release that has no
        // session to sit against), so it is passed through rather than smoothed to null.
        timing: event.earningsTime || "unknown",
        confirmed: event.confirmed === true,
        estimatedEps: num(event.estimatedEps),
      },
    };
  }
  if (isPreview && typeof totalCount === "number" && totalCount > rows.length) {
    return { status: "outside_preview", nextEarnings: null };
  }
  return { status: "not_scheduled", nextEarnings: null };
}

/** Annualized standard deviation of daily log returns over the last `n` sessions. */
function realizedVol(closes, n) {
  if (closes.length < n + 1) return null;
  const window = closes.slice(-(n + 1));
  const returns = [];
  for (let i = 1; i < window.length; i++) {
    // A zero or missing close would make the log blow up; skip the pair rather than emit NaN.
    if (!(window[i] > 0) || !(window[i - 1] > 0)) continue;
    returns.push(Math.log(window[i] / window[i - 1]));
  }
  if (returns.length < 2) return null;
  const mean = returns.reduce((a, b) => a + b, 0) / returns.length;
  const variance = returns.reduce((a, b) => a + (b - mean) ** 2, 0) / (returns.length - 1);
  return Math.sqrt(variance) * Math.sqrt(SESSIONS_PER_YEAR);
}

async function main() {
  const ticker = (process.argv[2] || "").trim().toUpperCase();
  if (!ticker) {
    die("no ticker given", "Usage: node scripts/prepare_data.mjs TSLA");
  }
  if (!/^[A-Z][A-Z0-9.\-]{0,9}$/.test(ticker)) {
    die(`"${ticker}" does not look like a ticker`, "Use a symbol such as TSLA, SPY or BRK.B");
  }
  if (!KEY) {
    die(
      "SENTISENSE_API_KEY is not set",
      "Get a free key at https://app.sentisense.ai/get-api-key, then export SENTISENSE_API_KEY",
    );
  }

  // The options dossier is the one call that can legitimately answer "no coverage", and it is
  // also the only source of the implied volatility the whole chart rests on. Check it first so
  // an uncovered ticker fails in one call instead of four.
  const options = await get(`/api/v1/stocks/${encodeURIComponent(ticker)}/options/summary`, {
    allowNullData: true,
  });
  if (!options.data) {
    die(
      `${ticker} has no options coverage`,
      "Coverage is the most actively optioned US names plus the tracked ETFs. Try a larger name.",
    );
  }
  // Full dossier or free headline preview, read the same way. A preview is not an error: it
  // still carries the 30 day reading, and `isPreview` below puts the preview label on the page.
  const iv = readOptionsIv(options.data);
  if (iv.atm30 === null) {
    die(
      `${ticker} has no at-the-money implied volatility in its latest session`,
      "Without it there is no cone to draw. This is usually a still-building baseline.",
    );
  }

  // Quotes are split by instrument type. The stock endpoint answers 400 `ticker_is_etf` for a
  // fund and names the ETF path in the message, so an ETF is one redirect away rather than a
  // failure: both return the same `currentPrice`, and options coverage includes the tracked ETFs.
  let quote = await get(`/api/v1/stocks/${encodeURIComponent(ticker)}/quote`, { tolerate400: true });
  if (!quote.data) {
    if (quote.error && quote.error.error === "ticker_is_etf") {
      quote = await get(`/api/v1/etfs/${encodeURIComponent(ticker)}/quote`);
    } else {
      die(
        `${ticker} has no quote`,
        quote.error && quote.error.message ? String(quote.error.message) : undefined,
      );
    }
  }
  const spot = quote.data.currentPrice;
  if (typeof spot !== "number" || !(spot > 0)) {
    die(`${ticker} has no usable current price`);
  }

  // Chart and calendar are context, not load-bearing: a missing realized series or an
  // unscheduled next report should soften the artifact, never fail the run.
  let closes = [];
  try {
    const bars = (await get(`/api/v1/stocks/chart?ticker=${encodeURIComponent(ticker)}&timeframe=1Y`, {
      optional: true,
    })).data;
    if (Array.isArray(bars)) closes = bars.map((b) => b.close).filter((c) => typeof c === "number");
  } catch {
    closes = [];
  }

  // `from` = today drops reports that already happened earlier this week; the default window
  // opens on Monday. A failed call leaves the next date unknown rather than "not scheduled".
  let nextEarnings = null;
  let nextEarningsStatus = "unavailable";
  try {
    const today = easternToday();
    const cal = await get(
      `/api/v1/calendar/earnings?ticker=${encodeURIComponent(ticker)}&from=${today}`,
      { optional: true },
    );
    const picked = pickNextEarnings(cal.data, {
      isPreview: cal.isPreview,
      totalCount: cal.totalCount,
      today,
    });
    nextEarnings = picked.nextEarnings;
    nextEarningsStatus = picked.status;
  } catch {
    nextEarnings = null;
    nextEarningsStatus = "unavailable";
  }

  // One entry per window that actually computed, each carrying the session count behind it so
  // the artifact can label a bar with the sample it used rather than the sample it wanted.
  // Past earnings reactions. Context, not load-bearing: when this is unavailable the template
  // falls back to the realized-volatility panel, so nothing here may fail the run. An uncovered
  // ticker and a fund that never reports both answer 200 with an empty list rather than 404,
  // which lands in the same empty-array result as a genuine error.
  let reactions = [];
  try {
    const react = (await get(`/api/v1/stocks/${encodeURIComponent(ticker)}/earnings/reactions`, {
      optional: true,
    })).data;
    if (react && Array.isArray(react.reactions)) {
      reactions = react.reactions
        .filter((r) => r && typeof r.movePct === "number" && r.reportDate)
        // Already newest first on the wire; sorted here anyway so the panel's "last 8" is the
        // most recent 8 even if that ordering ever changes.
        .sort((a, b) => String(b.reportDate).localeCompare(String(a.reportDate)))
        .slice(0, MAX_REACTIONS)
        .map((r) => ({
          reportDate: r.reportDate,
          // Null is a real reading: the session was inferred rather than observed. Passed
          // through as null rather than filled in with a guess.
          timing: r.timing == null ? null : String(r.timing),
          priorClose: typeof r.priorClose === "number" ? r.priorClose : null,
          nextClose: typeof r.nextClose === "number" ? r.nextClose : null,
          movePct: r.movePct,
        }));
    }
  } catch {
    reactions = [];
  }

  const realizedVolatility = [];
  for (const n of RV_WINDOWS) {
    const value = realizedVol(closes, n);
    if (value !== null) realizedVolatility.push({ sessions: n, value: Number(value.toFixed(4)) });
  }
  const fullSessions = Math.max(0, closes.length - 1);
  if (fullSessions > 60) {
    const value = realizedVol(closes, fullSessions);
    if (value !== null) {
      realizedVolatility.push({ sessions: fullSessions, value: Number(value.toFixed(4)) });
    }
  }

  const payload = {
    ticker,
    asOf: options.data.asOf || null,
    generatedAt: new Date().toISOString(),
    spot,
    // Every IV here is annualized and expressed as a fraction, so 0.4051 is 40.51%.
    iv,
    realizedVolatility,
    realizedSessions: closes.length,
    nextEarnings,
    nextEarningsStatus,
    // The template renders a past-earnings-reaction comparison when this has rows, and falls
    // back to the realized-volatility comparison when it is empty.
    reactions,
    isPreview: options.isPreview,
  };

  process.stdout.write(JSON.stringify(payload, null, 2) + "\n");
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) main();
