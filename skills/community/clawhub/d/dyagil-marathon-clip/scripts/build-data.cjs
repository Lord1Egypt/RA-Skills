#!/usr/bin/env node
/**
 * build-data.cjs — Extract running stats from sahi-diet for a specific window
 * (default: last 7 days) AND for the comparison window (previous 7 days)
 * to enable the trends/improvements scene in MarathonClip.
 *
 * Usage:
 *   node build-data.cjs [--days 7] [--from YYYY-MM-DD] [--to YYYY-MM-DD]
 *                       [--out data.json] [--athlete "David"]
 *
 * Date logic:
 *   - With --from / --to: explicit window. Compare to the equal-length window
 *     immediately before it.
 *   - With --days N (default): last N days inclusive of today. Compare to the
 *     previous N days before that.
 */
const path = require('path');
const fs = require('fs');
const os = require('os');

const HOME = os.homedir();
const DEFAULT_DB = path.join(HOME, '.openclaw/workspace/projects/sahi-diet/data/sahi.db');
const DEFAULT_OUT = path.join(HOME, '.openclaw/workspace/projects/sahi-video/data.json');

function arg(name, def) {
  const i = process.argv.indexOf('--' + name);
  if (i === -1) return def;
  return process.argv[i + 1] ?? def;
}

function isoDate(d) {
  return d.toISOString().slice(0, 10);
}
function addDays(iso, n) {
  const d = new Date(iso + 'T00:00:00Z');
  d.setUTCDate(d.getUTCDate() + n);
  return isoDate(d);
}
function daysBetween(a, b) {
  const da = new Date(a + 'T00:00:00Z'), db = new Date(b + 'T00:00:00Z');
  return Math.round((db - da) / (24 * 3600 * 1000)) + 1;
}

const days = parseInt(arg('days', '7'), 10);
const from = arg('from', null);
const to = arg('to', null);
const out = arg('out', DEFAULT_OUT);
const athlete = arg('athlete', 'David');
const dbPath = arg('db', DEFAULT_DB);

let curFrom, curTo;
if (from && to) { curFrom = from; curTo = to; }
else {
  curTo = isoDate(new Date());
  curFrom = addDays(curTo, -(days - 1));
}
const windowLen = daysBetween(curFrom, curTo);
const prevTo = addDays(curFrom, -1);
const prevFrom = addDays(prevTo, -(windowLen - 1));

if (!fs.existsSync(dbPath)) {
  console.error(`build-data: database not found at ${dbPath}`);
  process.exit(1);
}

let Database;
try {
  Database = require(path.join(HOME, '.openclaw/workspace/projects/sahi-diet/node_modules/better-sqlite3'));
} catch {
  try { Database = require('better-sqlite3'); }
  catch { console.error('better-sqlite3 missing'); process.exit(1); }
}

const db = new Database(dbPath, { readonly: true });

function fetchWindow(a, b) {
  return db
    .prepare(
      `SELECT local_date, duration_min, distance_km, calories, notes
       FROM workouts
       WHERE type='run' AND local_date >= ? AND local_date <= ?
       ORDER BY local_date ASC`
    )
    .all(a, b);
}

function summarize(rows) {
  const km = rows.reduce((s, r) => s + (r.distance_km || 0), 0);
  const min = rows.reduce((s, r) => s + (r.duration_min || 0), 0);
  const cal = rows.reduce((s, r) => s + (r.calories || 0), 0);
  const pace = km > 0 ? min / km : 0;
  return {
    total_km: +km.toFixed(2),
    total_min: min,
    total_hours: +(min / 60).toFixed(1),
    total_calories: cal,
    avg_pace_min_per_km: +pace.toFixed(2),
    run_count: rows.length,
  };
}

function diff(cur, prev, key, lowerIsBetter = false) {
  const c = cur[key], p = prev[key];
  if (p === 0) return { absolute: c, percent: null, better: c > 0 };
  const delta = c - p;
  const pct = (delta / p) * 100;
  const better = lowerIsBetter ? delta < 0 : delta > 0;
  return { absolute: +delta.toFixed(2), percent: +pct.toFixed(1), better };
}

const curRows = fetchWindow(curFrom, curTo);
const prevRows = fetchWindow(prevFrom, prevTo);
const cur = summarize(curRows);
const prev = summarize(prevRows);

// Hebrew period label
function hebrewPeriodLabel(from, to, len) {
  if (len === 7) {
    return 'שבוע אחרון';
  }
  return `${len} ימים אחרונים`;
}

const data = {
  athlete,
  period: hebrewPeriodLabel(curFrom, curTo, windowLen),
  window: { from: curFrom, to: curTo },
  prev_window: { from: prevFrom, to: prevTo },
  ...cur,
  runs: curRows.map((r) => ({
    date: r.local_date,
    km: +(r.distance_km || 0).toFixed(2),
    min: r.duration_min,
    note: (r.notes || '').slice(0, 40),
  })),
  trends: {
    has_prev: prev.run_count > 0,
    prev: prev,
    km: diff(cur, prev, 'total_km'),                // higher = better
    minutes: diff(cur, prev, 'total_min'),          // higher = better
    runs: diff(cur, prev, 'run_count'),             // higher = better
    pace: diff(cur, prev, 'avg_pace_min_per_km', true), // lower = better
  },
};

fs.mkdirSync(path.dirname(out), { recursive: true });
fs.writeFileSync(out, JSON.stringify(data, null, 2));
console.log(`build-data: cur ${cur.run_count} runs / ${cur.total_km} km (${curFrom}→${curTo})`);
console.log(`            prev ${prev.run_count} runs / ${prev.total_km} km (${prevFrom}→${prevTo})`);
console.log(`            → ${out}`);
