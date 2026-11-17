import { test } from 'node:test';
import assert from 'node:assert/strict';
import http from 'node:http';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { fileURLToPath } from 'node:url';
import { buildReport, planDay, parseArgs, weatherText } from '../scripts/a3-weather.mjs';

const run = promisify(execFile);
const SCRIPT = fileURLToPath(new URL('../scripts/a3-weather.mjs', import.meta.url));

function fixture({ precip = [5, 10, 60, 70], uv = 7, max = 84, min = 58, code = 61 } = {}) {
  const hours = Array.from({ length: 24 }, (_, h) => `2026-11-13T${String(h).padStart(2, '0')}:00`);
  return {
    timezone: 'America/Los_Angeles',
    daily: { time: ['2026-11-13', '2026-11-14'], weather_code: [code, 0], temperature_2m_max: [max, 70], temperature_2m_min: [min, 50],
      precipitation_probability_max: [Math.max(...precip), 0], precipitation_sum: [0.2, 0], wind_speed_10m_max: [12, 5], uv_index_max: [uv, 3] },
    hourly: { time: hours, temperature_2m: hours.map((_, h) => 55 + h), precipitation_probability: hours.map((_, h) => precip[Math.floor(h / 6)]), weather_code: hours.map(() => 0) },
  };
}

test('weatherText maps WMO codes', () => {
  assert.equal(weatherText(0), 'clear sky');
  assert.equal(weatherText(61), 'light rain');
  assert.equal(weatherText(999), 'unknown');
});

test('planDay recommends umbrella, sunscreen and layers, and a dry comfortable window', () => {
  const day = { max: 84, min: 58, precipProbMax: 70, uvMax: 7 };
  const hourly = Array.from({ length: 24 }, (_, h) => ({ hour: h, temp: 55 + h, precipProb: h < 12 ? 5 : 70 }));
  const p = planDay(day, hourly, 'imperial');
  assert.ok(p.tips.some((t) => /umbrella/i.test(t)));
  assert.ok(p.tips.some((t) => /sunscreen/i.test(t)));
  assert.ok(p.tips.some((t) => /layer/i.test(t)));
  assert.ok(p.bestOutdoorWindow && p.bestOutdoorWindow.start >= 8 && p.bestOutdoorWindow.end <= 12, JSON.stringify(p.bestOutdoorWindow));
});

test('buildReport selects the requested date and labels units and source', () => {
  const r = buildReport(fixture(), { name: 'Los Angeles', lat: 34.05, lon: -118.24 }, { date: '2026-11-13', units: 'imperial' }, '2026-11-13T15:00:00Z');
  assert.equal(r.status, 'ok');
  assert.equal(r.location.name, 'Los Angeles');
  assert.equal(r.date, '2026-11-13');
  assert.equal(r.units.temperature, '°F');
  assert.equal(r.source, 'Open-Meteo (open-meteo.com), CC BY 4.0');
  assert.equal(r.fetchedAt, '2026-11-13T15:00:00Z');
  assert.match(r.summary, /Los Angeles/);
  assert.match(r.summary, /light rain/);
});

test('buildReport reports unavailable for a date outside the forecast', () => {
  const r = buildReport(fixture(), { name: 'X', lat: 0, lon: 0 }, { date: '2026-12-25', units: 'metric' }, 'now');
  assert.equal(r.status, 'unavailable');
  assert.match(r.reason, /not in forecast/);
});

test('parseArgs validates input', () => {
  assert.deepEqual(parseArgs(['--city', 'Paris', '--units', 'metric']).units, 'metric');
  assert.throws(() => parseArgs(['--units', 'kelvin']), /units/);
  assert.throws(() => parseArgs([]), /--city or --lat/);
  assert.throws(() => parseArgs(['--lat', '100', '--lon', '0']), /latitude/);
});

function fakeApi(handler) {
  const srv = http.createServer(handler);
  return new Promise((r) => srv.listen(0, '127.0.0.1', () => r({ url: `http://127.0.0.1:${srv.address().port}`, close: () => srv.close() })));
}

test('CLI end-to-end against a fake API: geocode + forecast', async () => {
  const api = await fakeApi((req, res) => {
    res.setHeader('content-type', 'application/json');
    if (req.url.startsWith('/v1/search')) return res.end(JSON.stringify({ results: [{ name: 'Seattle', latitude: 47.6, longitude: -122.3, country_code: 'US', admin1: 'Washington' }] }));
    if (req.url.startsWith('/v1/forecast')) { assert.match(req.url, /temperature_unit=celsius/); return res.end(JSON.stringify(fixture())); }
    res.statusCode = 404; res.end('{}');
  });
  const { stdout } = await run(process.execPath, [SCRIPT, '--city', 'Seattle', '--units', 'metric', '--date', '2026-11-13', '--json'],
    { env: { ...process.env, A3_WEATHER_GEOCODE_URL: `${api.url}/v1/search`, A3_WEATHER_FORECAST_URL: `${api.url}/v1/forecast` } });
  api.close();
  const r = JSON.parse(stdout);
  assert.equal(r.status, 'ok');
  assert.equal(r.location.name, 'Seattle, Washington, US');
  assert.equal(r.units.temperature, '°C');
});

test('CLI reports unavailable (exit 3) when the source is down — no fabricated forecast', async () => {
  const api = await fakeApi((_req, res) => { res.statusCode = 503; res.end('down'); });
  const err = await run(process.execPath, [SCRIPT, '--lat', '34.05', '--lon', '-118.24', '--json'],
    { env: { ...process.env, A3_WEATHER_FORECAST_URL: `${api.url}/v1/forecast` } }).catch((e) => e);
  api.close();
  assert.equal(err.code, 3);
  const r = JSON.parse(err.stdout);
  assert.equal(r.status, 'unavailable');
  assert.equal(r.temperature, undefined);
});
