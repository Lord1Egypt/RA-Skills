#!/usr/bin/env node
// a3-weather: weather for briefings and meeting alerts, using the OpenWeatherMap free APIs
// (current weather + 5-day/3-hour forecast). No dependencies; Node >= 18 (global fetch).
// The API key is read from OPENWEATHER_API_KEY and is never printed, logged or cached.
//
// Usage:
//   weather.mjs --brief  [--location "City,CC" | --lat N --lon N] [--units metric|imperial]
//   weather.mjs --at <ISO time> [...]   forecast for one moment (e.g. a meeting start), up to 5 days ahead
//   weather.mjs --json   [...]          structured output (current + next 24 h)
// Env: OPENWEATHER_API_KEY (required), A3_WEATHER_LOCATION (default location), A3_WEATHER_UNITS,
//      A3_WEATHER_CACHE_DIR (default: OS temp dir).
// Network: HTTPS to api.openweathermap.org only. A3_WEATHER_BASE_URL exists for the unit tests' local mock and is accepted only
// when NODE_ENV=test and it points at http://127.0.0.1:<port>; anything else is refused, so the key can't be redirected elsewhere.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

export const CACHE_TTL_MS = 30 * 60 * 1000;
const TIMEOUT_MS = 10_000;
export const API_BASE = 'https://api.openweathermap.org';

export class WeatherError extends Error {
  constructor(message, exitCode) { super(message); this.exitCode = exitCode; }
}

export function parseArgs(argv, env = process.env) {
  const o = { mode: 'brief', units: env.A3_WEATHER_UNITS || 'metric', location: env.A3_WEATHER_LOCATION || '' };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i], next = () => {
      if (i + 1 >= argv.length) throw new WeatherError(`missing value for ${a}`, 2);
      return argv[++i];
    };
    if (a === '--brief') o.mode = 'brief';
    else if (a === '--json') o.mode = 'json';
    else if (a === '--at') { o.mode = 'at'; o.at = next(); }
    else if (a === '--location') o.location = next();
    else if (a === '--lat') o.lat = Number(next());
    else if (a === '--lon') o.lon = Number(next());
    else if (a === '--units') o.units = next();
    else if (a === '--help' || a === '-h') o.mode = 'help';
    else throw new WeatherError(`unknown argument: ${a}`, 2);
  }
  if (!['metric', 'imperial'].includes(o.units)) throw new WeatherError('units must be metric or imperial', 2);
  const hasCoords = Number.isFinite(o.lat) && Number.isFinite(o.lon);
  if (hasCoords) {
    if (Math.abs(o.lat) > 90 || Math.abs(o.lon) > 180) throw new WeatherError('lat/lon out of range', 2);
  } else if (o.mode !== 'help') {
    // Location text is untrusted (it may come from a calendar event): allow only plain place names.
    if (!o.location) throw new WeatherError('no location: pass --location "City,CC" or set A3_WEATHER_LOCATION', 2);
    if (o.location.length > 80 || !/^[\p{L}\p{N} .,'-]+$/u.test(o.location)) throw new WeatherError('invalid location text', 2);
  }
  if (o.mode === 'at') {
    const t = Date.parse(o.at);
    if (Number.isNaN(t)) throw new WeatherError('--at needs an ISO date/time, e.g. 2026-11-14T15:00:00-08:00', 2);
    o.atMs = t;
  }
  o.hasCoords = hasCoords;
  return o;
}

// The only endpoint the key is ever sent to, except the local test mock (see header).
export function apiBase(env = process.env) {
  const o = env.A3_WEATHER_BASE_URL;
  if (!o) return API_BASE;
  if (env.NODE_ENV === 'test' && /^http:\/\/127\.0\.0\.1:\d{1,5}\/?$/.test(o)) return o;
  throw new WeatherError('A3_WEATHER_BASE_URL is only allowed for local tests', 2);
}

export const redact = (s, key) => (key ? String(s).split(key).join('***') : String(s));

function cacheFile(dir, kind, o) {
  const id = crypto.createHash('sha256')
    .update(JSON.stringify([kind, o.units, o.hasCoords ? [o.lat, o.lon] : o.location.toLowerCase()])).digest('hex').slice(0, 24);
  return path.join(dir, `${kind}-${id}.json`);
}

async function getJson(kind, o, env, now) {
  const key = env.OPENWEATHER_API_KEY;
  if (!key) throw new WeatherError('OPENWEATHER_API_KEY is not set (add it to .env or the agent environment)', 2);
  const dir = env.A3_WEATHER_CACHE_DIR || path.join(os.tmpdir(), 'a3-weather-cache');
  const file = cacheFile(dir, kind, o);
  try {
    const c = JSON.parse(fs.readFileSync(file, 'utf8'));
    if (now - c.savedAt < CACHE_TTL_MS) return { data: c.data, cached: true };
  } catch { /* no cache */ }

  const base = apiBase(env);
  const u = new URL(`/data/2.5/${kind === 'current' ? 'weather' : 'forecast'}`, base);
  if (o.hasCoords) { u.searchParams.set('lat', o.lat); u.searchParams.set('lon', o.lon); } else u.searchParams.set('q', o.location);
  u.searchParams.set('units', o.units);
  u.searchParams.set('appid', key);
  let res;
  try {
    res = await fetch(u, { signal: AbortSignal.timeout(TIMEOUT_MS) });
  } catch (e) {
    throw new WeatherError(`weather service unreachable: ${redact(e.message, key)}`, 3);
  }
  if (res.status === 401) throw new WeatherError('OpenWeatherMap rejected the API key (new keys can take up to 2 hours to activate)', 4);
  if (res.status === 404) throw new WeatherError(`location not found: ${o.hasCoords ? `${o.lat},${o.lon}` : o.location}`, 5);
  if (res.status === 429) throw new WeatherError('OpenWeatherMap rate limit reached; try again later', 6);
  if (!res.ok) throw new WeatherError(`weather service error HTTP ${res.status}`, 3);
  const data = await res.json();
  try { fs.mkdirSync(dir, { recursive: true, mode: 0o700 }); fs.writeFileSync(file, JSON.stringify({ savedAt: now, data }), { mode: 0o600 }); } catch { /* cache is optional */ }
  return { data, cached: false };
}

const U = (units) => (units === 'imperial' ? { t: '°F', w: 'mph' } : { t: '°C', w: 'm/s' });
const r = (n) => Math.round(n);
// Local time at the forecast location (the API gives a UTC offset in seconds).
export function localTime(unixSec, tzSec) {
  const d = new Date((unixSec + tzSec) * 1000);
  return `${String(d.getUTCHours()).padStart(2, '0')}:${String(d.getUTCMinutes()).padStart(2, '0')}`;
}

export function summarizeBrief(current, forecast, units, nowMs) {
  const u = U(units);
  const tz = forecast.city?.timezone ?? current.timezone ?? 0;
  const next24 = forecast.list.filter((s) => s.dt * 1000 >= nowMs - 3 * 3600e3 && s.dt * 1000 <= nowMs + 24 * 3600e3);
  const slots = next24.length ? next24 : forecast.list.slice(0, 8);
  const hi = Math.max(...slots.map((s) => s.main.temp_max)), lo = Math.min(...slots.map((s) => s.main.temp_min));
  const maxPop = Math.max(...slots.map((s) => s.pop ?? 0));
  const wet = slots.find((s) => (s.pop ?? 0) >= 0.5);
  const name = current.name || forecast.city?.name || 'your location';
  let line = `${name}: now ${r(current.main.temp)}${u.t}, ${current.weather?.[0]?.description ?? 'n/a'}; next 24 h ${r(lo)}–${r(hi)}${u.t}, rain chance up to ${r(maxPop * 100)}%`;
  if (wet) line += ` (likely from ~${localTime(wet.dt, tz)})`;
  if ((current.wind?.speed ?? 0) >= (units === 'imperial' ? 20 : 9)) line += `; windy (${r(current.wind.speed)} ${u.w})`;
  return line + '.';
}

export function summarizeAt(forecast, atMs, units) {
  const u = U(units);
  const list = forecast.list;
  const first = list[0].dt * 1000, last = list[list.length - 1].dt * 1000;
  if (atMs < first - 3 * 3600e3 || atMs > last + 3 * 3600e3) return null; // outside the 5-day forecast window
  const slot = list.reduce((best, s) => (Math.abs(s.dt * 1000 - atMs) < Math.abs(best.dt * 1000 - atMs) ? s : best));
  const tz = forecast.city?.timezone ?? 0;
  const pop = r((slot.pop ?? 0) * 100);
  return `${forecast.city?.name ?? 'Forecast'} around ${localTime(Math.round(atMs / 1000), tz)}: ${r(slot.main.temp)}${u.t}, ${slot.weather?.[0]?.description ?? 'n/a'}, rain chance ${pop}%${pop >= 50 ? ' — bring an umbrella' : ''}.`;
}

export async function run(argv, env = process.env, nowMs = Date.now()) {
  const o = parseArgs(argv, env);
  apiBase(env); // refuse a non-test endpoint override before reading any cache or the key
  if (o.mode === 'help') return 'Usage: weather.mjs --brief | --at <ISO> | --json  [--location "City,CC" | --lat N --lon N] [--units metric|imperial]';
  if (o.mode === 'at') {
    const { data: f } = await getJson('forecast', o, env, nowMs);
    return summarizeAt(f, o.atMs, o.units) ?? `No forecast for that time yet (OpenWeatherMap covers the next 5 days).`;
  }
  const [{ data: c, cached: cc }, { data: f, cached: fc }] = await Promise.all([getJson('current', o, env, nowMs), getJson('forecast', o, env, nowMs)]);
  if (o.mode === 'json') {
    return JSON.stringify({
      location: c.name, units: o.units, cached: cc && fc, source: 'OpenWeatherMap',
      now: { temp: c.main.temp, feelsLike: c.main.feels_like, description: c.weather?.[0]?.description, windSpeed: c.wind?.speed },
      next24h: f.list.filter((s) => s.dt * 1000 <= nowMs + 24 * 3600e3).map((s) => ({ time: new Date(s.dt * 1000).toISOString(), temp: s.main.temp, pop: s.pop ?? 0, description: s.weather?.[0]?.description })),
    });
  }
  return summarizeBrief(c, f, o.units, nowMs);
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  run(process.argv.slice(2)).then((out) => console.log(out)).catch((e) => {
    console.error(`a3-weather: ${redact(e.message, process.env.OPENWEATHER_API_KEY)}`);
    process.exit(e.exitCode || 1);
  });
}
