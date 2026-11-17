import type { Snapshot, Trend } from "../types";

export const TREND_WINDOW_HOURS = 168; // 7-day regression window
export const MIN_TREND_SPAN_HOURS = 0.5; // below this, a delta is noise
export const LOW_BALANCE_USD = 5.0; // USD wallet alert threshold
export const LOW_BALANCE_PERCENT = 20; // remaining-% alert threshold
export const NOISE_BURN_PER_DAY = 0.005; // burn below this counts as 0

interface Point {
  t: number;
  v: number;
}

/** Least-squares slope in units/hour over a point series. */
export function slopePerHour(points: Point[]): number {
  const n = points.length;
  if (n < 2) return 0;
  const first = points[0]!.t;
  let sx = 0, sy = 0, sxx = 0, sxy = 0;
  for (const p of points) {
    const x = (p.t - first) / 3_600_000;
    sx += x;
    sy += p.v;
    sxx += x * x;
    sxy += x * p.v;
  }
  const denom = n * sxx - sx * sx;
  if (denom === 0) return 0;
  return (n * sxy - sx * sy) / denom;
}

/** Drop everything before the LAST downward step (quota reset) in a percent series. */
export function clipAfterReset(points: Point[]): Point[] {
  let lastDrop = -1;
  for (let i = 1; i < points.length; i++) {
    if (points[i]!.v < points[i - 1]!.v - 1e-9) lastDrop = i;
  }
  return lastDrop > 0 ? points.slice(lastDrop) : points;
}

function round(value: number, digits = 2): number {
  const f = 10 ** digits;
  return Math.round(value * f) / f;
}

function daysLeft(balance: number, dailyRate: number | null): number | null {
  if (dailyRate === null || dailyRate <= 0) return null;
  const days = balance / dailyRate;
  if (!Number.isFinite(days) || days < 0) return null;
  return round(days, 1);
}

/** Port of usage-logger's calculate_trend over one provider's history. */
export function calculateTrend(entries: Snapshot[], provider: string): Trend | null {
  const series = entries
    .filter((e) => e.provider === provider && e.timestamp && !e.error)
    .sort((a, b) => Date.parse(a.timestamp) - Date.parse(b.timestamp));
  if (series.length === 0) return null;

  const last = series[series.length - 1]!;
  const lastT = Date.parse(last.timestamp);
  const cutoff = lastT - TREND_WINDOW_HOURS * 3_600_000;
  const window = series.filter((e) => Date.parse(e.timestamp) >= cutoff);

  const percentPoints: Point[] = [];
  const balancePoints: Point[] = [];
  for (const e of window) {
    const t = Date.parse(e.timestamp);
    if (typeof e.usedPercent === "number") percentPoints.push({ t, v: e.usedPercent });
    else if (typeof e.balance === "number") balancePoints.push({ t, v: e.balance });
  }

  const samples = Math.max(percentPoints.length, balancePoints.length);
  const basis: Trend["basis"] = percentPoints.length >= balancePoints.length ? "percent" : "balance";

  const trend: Trend = {
    provider,
    basis,
    dailyRate: null,
    estimatedDaysLeft: null,
    lowBalance: false,
    samples,
    spanHours: 0,
  };
  if (typeof last.balance === "number") trend.balance = last.balance;
  if (last.currency) trend.currency = last.currency;

  if (basis === "percent" && percentPoints.length > 0) {
    const pts = clipAfterReset(percentPoints);
    const spanHours = (pts[pts.length - 1]!.t - pts[0]!.t) / 3_600_000;
    const remaining = 100 - (percentPoints[percentPoints.length - 1]!.v);
    trend.remainingPercent = round(remaining, 1);
    trend.spanHours = round(spanHours, 2);
    if (pts.length >= 2 && spanHours >= MIN_TREND_SPAN_HOURS) {
      const dailyRate = slopePerHour(pts) * 24;
      trend.dailyRate = round(dailyRate, 2);
      trend.estimatedDaysLeft =
        dailyRate > 0 ? round(Math.max(remaining, 0) / dailyRate, 1) : null;
    }
    trend.lowBalance = remaining < LOW_BALANCE_PERCENT;
    return trend;
  }

  if (balancePoints.length > 0) {
    const spanHours =
      (balancePoints[balancePoints.length - 1]!.t - balancePoints[0]!.t) / 3_600_000;
    trend.spanHours = round(spanHours, 2);
    if (balancePoints.length >= 2 && spanHours >= MIN_TREND_SPAN_HOURS) {
      let burn = -slopePerHour(balancePoints) * 24; // spend per day
      if (burn < NOISE_BURN_PER_DAY) burn = 0;
      trend.dailyRate = round(burn, 4);
      trend.estimatedDaysLeft =
        burn > 0 && typeof trend.balance === "number" ? daysLeft(trend.balance, burn) : null;
    }
    trend.lowBalance =
      (trend.currency ?? "USD") === "USD" &&
      typeof trend.balance === "number" &&
      trend.balance < LOW_BALANCE_USD;
  }
  return trend;
}
