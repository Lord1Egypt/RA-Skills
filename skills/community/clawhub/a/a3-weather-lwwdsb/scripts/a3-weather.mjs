#!/usr/bin/env node
// a3-weather — location-aware daily forecast with day-plan guidance (original CSCI 599 A3 skill).
// Data: Open-Meteo forecast + geocoding APIs (https://open-meteo.com, CC BY 4.0, no API key).
// Zero dependencies; Node >= 18.
//
// Usage:
//   node a3-weather.mjs --city "Los Angeles" [--date today|tomorrow|YYYY-MM-DD] [--units imperial|metric] [--json]
//   node a3-weather.mjs --lat 34.05 --lon -118.24 [--name "Los Angeles"] ...
// Exit codes: 0 ok, 2 invalid input, 3 data unavailable.

import { pathToFileURL } from 'node:url';

const GEOCODE_URL = process.env.A3_WEATHER_GEOCODE_URL || 'https://geocoding-api.open-meteo.com/v1/search';
const FORECAST_URL = process.env.A3_WEATHER_FORECAST_URL || 'https://api.open-meteo.com/v1/forecast';
export const SOURCE = 'Open-Meteo (open-meteo.com), CC BY 4.0';

const WMO = {
  0: 'clear sky', 1: 'mainly clear', 2: 'partly cloudy', 3: 'overcast', 45: 'fog', 48: 'depositing rime fog',
  51: 'light drizzle', 53: 'drizzle', 55: 'dense drizzle', 56: 'freezing drizzle', 57: 'dense freezing drizzle',
  61: 'light rain', 63: 'rain', 65: 'heavy rain', 66: 'freezing rain', 67: 'heavy freezing rain',
  71: 'light snow', 73: 'snow', 75: 'heavy snow', 77: 'snow grains', 80: 'light showers', 81: 'showers',
  82: 'violent showers', 85: 'snow showers', 86: 'heavy snow showers', 95: 'thunderstorm',
  96: 'thunderstorm with hail', 99: 'severe thunderstorm with hail',
};
export const weatherText = (code) => WMO[code] ?? 'unknown';

export function parseArgs(argv) {
  const o = { date: 'today', units: 'imperial', json: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    const next = () => { const v = argv[++i]; if (v === undefined) throw new Error(`missing value for ${a}`); return v; };
    if (a === '--city') o.city = next();
    else if (a === '--lat') o.lat = Number(next());
    else if (a === '--lon') o.lon = Number(next());
    else if (a === '--name') o.name = next();
    else if (a === '--date') o.date = next();
    else if (a === '--units') o.units = next();
    else if (a === '--json') o.json = true;
    else throw new Error(`unknown argument ${a}`);
  }
  if (!['imperial', 'metric'].includes(o.units)) throw new Error('units must be imperial or metric');
  if (!o.city && (o.lat === undefined || o.lon === undefined)) throw new Error('provide --city or --lat and --lon');
  if (o.lat !== undefined && !(o.lat >= -90 && o.lat <= 90)) throw new Error('latitude out of range');
  if (o.lon !== undefined && !(o.lon >= -180 && o.lon <= 180)) throw new Error('longitude out of range');
  if (!/^(today|tomorrow|\d{4}-\d{2}-\d{2})$/.test(o.date)) throw new Error('date must be today, tomorrow or YYYY-MM-DD');
  if (o.city && o.city.length > 100) throw new Error('city name too long');
  return o;
}

const unitLabels = (units) => units === 'metric'
  ? { temperature: '°C', wind: 'km/h', precipitation: 'mm' }
  : { temperature: '°F', wind: 'mph', precipitation: 'in' };

// Original guidance: comfortable dry outdoor window + practical tips.
export function planDay(day, hourly, units) {
  const comfy = units === 'metric' ? [13, 27] : [55, 80];
  const swing = units === 'metric' ? 11 : 20;
  const tips = [];
  if (day.precipProbMax >= 40) tips.push(`Bring an umbrella (up to ${day.precipProbMax}% chance of precipitation).`);
  if (day.uvMax >= 6) tips.push(`Wear sunscreen (UV index up to ${day.uvMax}).`);
  if (day.max - day.min >= swing) tips.push('Dress in layers — large temperature swing today.');
  if (day.max > comfy[1] + 10) tips.push('Very warm: stay hydrated and plan outdoor time early or late.');
  if (day.min < comfy[0] - 15) tips.push('Cold: wear a warm jacket.');

  let best = null;
  for (let start = 8; start + 3 <= 20; start++) {
    const span = hourly.filter((h) => h.hour >= start && h.hour < start + 3);
    if (span.length < 3) continue;
    const dry = span.every((h) => h.precipProb < 30);
    const okTemp = span.every((h) => h.temp >= comfy[0] && h.temp <= comfy[1]);
    if (!dry || !okTemp) continue;
    const score = span.reduce((s, h) => s + h.precipProb, 0);
    if (!best || score < best.score) best = { start, end: start + 3, score };
  }
  return { tips, bestOutdoorWindow: best ? { start: best.start, end: best.end } : null };
}

function localDate(offsetDays, timeZone) {
  const d = new Date(Date.now() + offsetDays * 86_400_000);
  return new Intl.DateTimeFormat('en-CA', { timeZone, year: 'numeric', month: '2-digit', day: '2-digit' }).format(d);
}

export function resolveDate(date, timeZone) {
  if (date === 'today') return localDate(0, timeZone);
  if (date === 'tomorrow') return localDate(1, timeZone);
  return date;
}

export function buildReport(api, location, opts, fetchedAt) {
  const tz = api.timezone || 'UTC';
  const date = resolveDate(opts.date, tz);
  const i = api.daily?.time?.indexOf(date) ?? -1;
  const units = unitLabels(opts.units);
  if (i < 0) return { status: 'unavailable', reason: `date ${date} not in forecast range`, location, source: SOURCE, fetchedAt };
  const d = api.daily;
  const day = {
    code: d.weather_code[i], max: Math.round(d.temperature_2m_max[i]), min: Math.round(d.temperature_2m_min[i]),
    precipProbMax: d.precipitation_probability_max?.[i] ?? 0, precipSum: d.precipitation_sum?.[i] ?? 0,
    windMax: Math.round(d.wind_speed_10m_max?.[i] ?? 0), uvMax: Math.round(d.uv_index_max?.[i] ?? 0),
  };
  const hourly = (api.hourly?.time ?? []).map((t, k) => ({ t, k })).filter(({ t }) => t.startsWith(date))
    .map(({ t, k }) => ({ hour: Number(t.slice(11, 13)), temp: api.hourly.temperature_2m[k], precipProb: api.hourly.precipitation_probability?.[k] ?? 0 }));
  const plan = planDay(day, hourly, opts.units);
  const conditions = weatherText(day.code);
  const window = plan.bestOutdoorWindow ? ` Best outdoor window: ${plan.bestOutdoorWindow.start}:00–${plan.bestOutdoorWindow.end}:00.` : '';
  const summary = `${location.name} on ${date}: ${conditions}, high ${day.max}${units.temperature} / low ${day.min}${units.temperature}, ` +
    `precipitation chance up to ${day.precipProbMax}%, wind up to ${day.windMax} ${units.wind}.${window}` +
    (plan.tips.length ? ` ${plan.tips.join(' ')}` : '');
  return {
    status: 'ok', location, date, timezone: tz, conditions, temperature: { max: day.max, min: day.min },
    precipitation: { probabilityMax: day.precipProbMax, total: day.precipSum }, windMax: day.windMax, uvIndexMax: day.uvMax,
    units, plan, summary, source: SOURCE, fetchedAt,
  };
}

async function getJson(url) {
  const res = await fetch(url, { signal: AbortSignal.timeout(10_000), headers: { 'user-agent': 'a3-weather-skill/1.0' } });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

export async function geocode(city) {
  const u = new URL(GEOCODE_URL);
  u.search = new URLSearchParams({ name: city, count: '1', language: 'en', format: 'json' }).toString();
  const j = await getJson(u);
  const r = j.results?.[0];
  if (!r) return null;
  return { name: [r.name, r.admin1, r.country_code].filter(Boolean).join(', '), lat: r.latitude, lon: r.longitude };
}

export async function forecast(lat, lon, units) {
  const u = new URL(FORECAST_URL);
  u.search = new URLSearchParams({
    latitude: String(lat), longitude: String(lon), timezone: 'auto', forecast_days: '7',
    daily: 'weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum,wind_speed_10m_max,uv_index_max',
    hourly: 'temperature_2m,precipitation_probability',
    temperature_unit: units === 'metric' ? 'celsius' : 'fahrenheit',
    wind_speed_unit: units === 'metric' ? 'kmh' : 'mph',
    precipitation_unit: units === 'metric' ? 'mm' : 'inch',
  }).toString();
  return getJson(u);
}

export async function main(argv) {
  let opts;
  try { opts = parseArgs(argv); } catch (e) {
    process.stdout.write(JSON.stringify({ status: 'invalid_input', reason: e.message }) + '\n');
    return 2;
  }
  const fetchedAt = new Date().toISOString();
  const emit = (r) => process.stdout.write((opts.json ? JSON.stringify(r, null, 2) : (r.summary ?? `Weather unavailable: ${r.reason}`) + `\nSource: ${SOURCE}; retrieved ${fetchedAt}`) + '\n');
  let location;
  try {
    location = opts.city ? await geocode(opts.city) : { name: opts.name ?? `${opts.lat}, ${opts.lon}`, lat: opts.lat, lon: opts.lon };
  } catch (e) {
    emit({ status: 'unavailable', reason: `geocoding failed: ${e.message}`, source: SOURCE, fetchedAt });
    return 3;
  }
  if (!location) { emit({ status: 'unavailable', reason: `no location found for "${opts.city}"`, source: SOURCE, fetchedAt }); return 3; }
  try {
    const api = await forecast(location.lat, location.lon, opts.units);
    const report = buildReport(api, location, opts, fetchedAt);
    emit(report);
    return report.status === 'ok' ? 0 : 3;
  } catch (e) {
    emit({ status: 'unavailable', reason: `forecast source unavailable: ${e.message}`, location, source: SOURCE, fetchedAt });
    return 3;
  }
}

if (import.meta.url === pathToFileURL(process.argv[1] ?? '').href) {
  main(process.argv.slice(2)).then((code) => { process.exitCode = code; });
}
