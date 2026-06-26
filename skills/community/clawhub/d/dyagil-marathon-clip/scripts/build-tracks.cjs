#!/usr/bin/env node
/**
 * build-tracks.cjs — Fetch GPX tracks from Garmin for runs in the last N days,
 * parse them, simplify with Douglas-Peucker, and write tracks.json.
 *
 * Usage:
 *   node build-tracks.cjs [--days 7] [--out tracks.json]
 */
const path = require('path');
const fs = require('fs');
const os = require('os');

const HOME = os.homedir();
const SAHI_DIET = path.join(HOME, '.openclaw/workspace/projects/sahi-diet');
const DEFAULT_OUT = path.join(HOME, '.openclaw/workspace/projects/sahi-video/tracks.json');
const TMP_GPX = '/tmp/gpx-out-marathon-clip';

function arg(name, def) {
  const i = process.argv.indexOf('--' + name);
  if (i === -1) return def;
  return process.argv[i + 1] ?? def;
}

const days = parseInt(arg('days', '7'), 10);
const out = arg('out', DEFAULT_OUT);

// --- Pull run metadata from sahi-diet DB ---
let Database;
try { Database = require(path.join(SAHI_DIET, 'node_modules/better-sqlite3')); }
catch { try { Database = require('better-sqlite3'); } catch { console.error('better-sqlite3 missing'); process.exit(1); } }

const db = new Database(path.join(SAHI_DIET, 'data/sahi.db'), { readonly: true });
const runs = db
  .prepare(
    `SELECT external_id, local_date, distance_km, duration_min, notes
     FROM workouts
     WHERE type='run' AND source='garmin' AND external_id IS NOT NULL
       AND local_date >= date('now', '-' || ? || ' day')
     ORDER BY local_date ASC`
  )
  .all(days);

if (runs.length === 0) {
  console.log('no garmin runs in last', days, 'days');
  fs.writeFileSync(out, '[]');
  process.exit(0);
}

// --- Fetch GPX via Garmin (requires .env at sahi-diet root) ---
(async () => {
  // Load env from sahi-diet/.env
  require(path.join(SAHI_DIET, 'node_modules/dotenv')).config({ path: path.join(SAHI_DIET, '.env') });
  const { GarminConnect } = require(path.join(SAHI_DIET, 'node_modules/garmin-connect'));
  const gc = new GarminConnect({ username: process.env.GARMIN_EMAIL, password: process.env.GARMIN_PASSWORD });
  await gc.login();

  fs.rmSync(TMP_GPX, { recursive: true, force: true });
  fs.mkdirSync(TMP_GPX, { recursive: true });

  for (const r of runs) {
    try {
      await gc.downloadOriginalActivityData({ activityId: parseInt(r.external_id, 10) }, TMP_GPX, 'gpx');
      console.error('GPX', r.external_id, 'OK');
    } catch (e) {
      console.error('GPX', r.external_id, 'FAIL:', e.message);
    }
  }

  // --- Parse and simplify ---
  function douglasPeucker(pts, eps) {
    if (pts.length < 3) return pts;
    function perp(p, a, b) {
      const dx = b[1] - a[1], dy = b[0] - a[0];
      if (dx === 0 && dy === 0) return Math.hypot(p[1] - a[1], p[0] - a[0]);
      const t = ((p[1] - a[1]) * dx + (p[0] - a[0]) * dy) / (dx * dx + dy * dy);
      if (t < 0) return Math.hypot(p[1] - a[1], p[0] - a[0]);
      if (t > 1) return Math.hypot(p[1] - b[1], p[0] - b[0]);
      return Math.hypot(p[1] - (a[1] + t * dx), p[0] - (a[0] + t * dy));
    }
    let max = 0, idx = 0;
    for (let i = 1; i < pts.length - 1; i++) {
      const d = perp(pts[i], pts[0], pts[pts.length - 1]);
      if (d > max) { max = d; idx = i; }
    }
    if (max > eps) {
      const L = douglasPeucker(pts.slice(0, idx + 1), eps);
      const R = douglasPeucker(pts.slice(idx), eps);
      return L.slice(0, -1).concat(R);
    }
    return [pts[0], pts[pts.length - 1]];
  }

  const tracks = [];
  for (const r of runs) {
    const file = path.join(TMP_GPX, `${r.external_id}.gpx`);
    if (!fs.existsSync(file)) continue;
    const xml = fs.readFileSync(file, 'utf8');
    const re = /<trkpt\s+lat="([\d.\-]+)"\s+lon="([\d.\-]+)">/g;
    const pts = [];
    let m;
    while ((m = re.exec(xml)) !== null) pts.push([parseFloat(m[1]), parseFloat(m[2])]);
    if (pts.length === 0) {
      console.error('skip', r.external_id, '(no GPS - probably treadmill)');
      continue;
    }
    const simplified = douglasPeucker(pts, 0.00005);
    const lats = simplified.map((p) => p[0]);
    const lons = simplified.map((p) => p[1]);
    tracks.push({
      id: String(r.external_id),
      date: r.local_date,
      name: (r.notes || '').slice(0, 40) || `Run ${r.local_date}`,
      km: +Number(r.distance_km || 0).toFixed(2),
      min: r.duration_min,
      bounds: {
        minLat: Math.min(...lats), maxLat: Math.max(...lats),
        minLon: Math.min(...lons), maxLon: Math.max(...lons),
      },
      points: simplified.map((p) => [+p[0].toFixed(6), +p[1].toFixed(6)]),
    });
    console.error(r.external_id, '→', simplified.length, 'points');
  }

  tracks.sort((a, b) => a.date.localeCompare(b.date));
  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.writeFileSync(out, JSON.stringify(tracks, null, 2));
  console.log(`build-tracks: ${tracks.length} tracks → ${out}`);
})().catch((e) => { console.error('build-tracks failed:', e.message); process.exit(1); });
