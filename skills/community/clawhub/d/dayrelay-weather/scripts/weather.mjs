import { pathToFileURL } from "node:url";

// API contract adapted from https://open-meteo.com/en/docs - request a small daily
// forecast and normalize it for a briefing; no upstream implementation is copied.
const ENDPOINT = "https://api.open-meteo.com/v1/forecast";
const DAILY = ["weather_code", "temperature_2m_max", "temperature_2m_min",
  "precipitation_probability_max", "wind_speed_10m_max"];

export class WeatherError extends Error {
  constructor(code) { super(code); this.name = "WeatherError"; this.code = code; }
}
const fail = (code) => { throw new WeatherError(code); };

function timezone(value) {
  if (typeof value !== "string" || value.length > 100) fail("INVALID_TIMEZONE");
  try { return new Intl.DateTimeFormat("en", { timeZone: value }).resolvedOptions().timeZone; }
  catch { fail("INVALID_TIMEZONE"); }
}

function options(value) {
  if (!value || typeof value !== "object") fail("INVALID_OPTIONS");
  for (const [field, bound] of [["latitude", 90], ["longitude", 180]]) {
    if (typeof value[field] !== "number" || !Number.isFinite(value[field])
        || Math.abs(value[field]) > bound) fail("INVALID_COORDINATES");
  }
  const units = value.units ?? "celsius";
  if (!["celsius", "fahrenheit"].includes(units)) fail("INVALID_UNITS");
  return { latitude: value.latitude, longitude: value.longitude,
    timezone: timezone(value.timezone ?? "UTC"), units };
}

export function buildForecastUrl(value) {
  const config = options(value);
  const url = new URL(ENDPOINT);
  url.search = new URLSearchParams({
    latitude: String(config.latitude), longitude: String(config.longitude),
    timezone: config.timezone, temperature_unit: config.units,
    wind_speed_unit: "mph", daily: DAILY.join(","), forecast_days: "1",
  });
  return url;
}

function localDate(now, zone) {
  if (!(now instanceof Date) || !Number.isFinite(now.getTime())) fail("INVALID_TIMESTAMP");
  const parts = new Intl.DateTimeFormat("en-US", {
    timeZone: zone, calendar: "gregory", numberingSystem: "latn",
    year: "numeric", month: "2-digit", day: "2-digit",
  }).formatToParts(now);
  const part = (type) => parts.find((item) => item.type === type).value;
  return `${part("year")}-${part("month")}-${part("day")}`;
}

function condition(code) {
  if (code === null) return "unavailable";
  if (code === 0) return "clear";
  if ([1, 2, 3].includes(code)) return "cloud cover";
  if ([45, 48].includes(code)) return "fog";
  if ([51, 53, 55].includes(code)) return "drizzle";
  if ([56, 57].includes(code)) return "freezing drizzle";
  if ([61, 63, 65].includes(code)) return "rain";
  if ([66, 67].includes(code)) return "freezing rain";
  if ([71, 73, 75, 77].includes(code)) return "snow";
  if ([80, 81, 82].includes(code)) return "rain showers";
  if ([85, 86].includes(code)) return "snow showers";
  if ([95, 97].includes(code)) return "thunderstorms";
  if ([96, 99].includes(code)) return "thunderstorms with hail";
  return "unrecognized weather code";
}

export function normalizeForecast(data, value, now = new Date()) {
  const config = options(value);
  if (data?.error || !data?.daily || !data?.daily_units) fail("INVALID_WEATHER_RESPONSE");
  if (timezone(data.timezone) !== config.timezone) fail("TIMEZONE_MISMATCH");
  const dates = data.daily.time;
  if (!Array.isArray(dates) || dates.length !== 1
      || dates[0] !== localDate(now, config.timezone)) fail("FORECAST_DATE_MISMATCH");
  const expectedTemperatureUnit = config.units === "fahrenheit" ? "°F" : "°C";
  if (data.daily_units.temperature_2m_max !== expectedTemperatureUnit
      || data.daily_units.temperature_2m_min !== expectedTemperatureUnit
      || data.daily_units.precipitation_probability_max !== "%"
      || data.daily_units.wind_speed_10m_max !== "mp/h") fail("WEATHER_UNIT_MISMATCH");
  const read = (name) => {
    const list = data.daily[name];
    if (!Array.isArray(list) || list.length !== 1) fail("INVALID_WEATHER_RESPONSE");
    const number = list[0];
    if (number !== null && (typeof number !== "number" || !Number.isFinite(number))) fail("INVALID_WEATHER_RESPONSE");
    return number;
  };
  const high = read("temperature_2m_max");
  const low = read("temperature_2m_min");
  const rain = read("precipitation_probability_max");
  const wind = read("wind_speed_10m_max");
  const code = read("weather_code");
  if ((high !== null && low !== null && high < low)
      || (rain !== null && (rain < 0 || rain > 100))
      || (wind !== null && wind < 0)
      || (code !== null && (!Number.isInteger(code) || code < 0))) fail("INVALID_WEATHER_RESPONSE");
  return {
    source: "Open-Meteo", fetchedAt: now.toISOString(), date: dates[0],
    timezone: config.timezone, condition: condition(code), weatherCode: code,
    temperature: { high, low, unit: expectedTemperatureUnit },
    precipitationProbabilityPercent: rain,
    maximumWind: { value: wind, unit: "mph" },
    attribution: { label: "Weather data by Open-Meteo", url: "https://open-meteo.com/",
      licence: "https://creativecommons.org/licenses/by/4.0/",
      changes: "Daily API fields normalized and weather codes grouped for a briefing." },
  };
}

export async function fetchForecast(value, { fetchImpl = fetch, now = new Date(), signal } = {}) {
  const url = buildForecastUrl(value);
  let response;
  try {
    const deadline = AbortSignal.timeout(15_000);
    response = await fetchImpl(url, { signal: signal ? AbortSignal.any([signal, deadline]) : deadline, redirect: "error" });
  } catch { fail("WEATHER_NETWORK_UNAVAILABLE"); }
  if (!response.ok) fail(response.status === 429 ? "WEATHER_RATE_LIMITED" : "WEATHER_PROVIDER_ERROR");
  let data;
  try {
    const body = await response.text();
    if (body.length > 100_000) fail("WEATHER_RESPONSE_TOO_LARGE");
    data = JSON.parse(body);
  } catch (error) {
    if (error instanceof WeatherError) throw error;
    fail("INVALID_WEATHER_RESPONSE");
  }
  return normalizeForecast(data, value, now);
}

export function parseArguments(args) {
  const result = {};
  const allowed = new Set(["latitude", "longitude", "timezone", "units"]);
  for (let index = 0; index < args.length; index += 2) {
    const key = args[index]?.startsWith("--") ? args[index].slice(2) : "";
    if (!allowed.has(key) || Object.hasOwn(result, key) || args[index + 1] === undefined) fail("INVALID_ARGUMENTS");
    const raw = args[index + 1];
    if (key === "latitude" || key === "longitude") {
      if (!/^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$/u.test(raw)) fail("INVALID_COORDINATES");
      result[key] = Number(raw);
    } else result[key] = raw;
  }
  return options(result);
}

async function main() {
  const args = process.argv.slice(2);
  if (args.length === 1 && args[0] === "--help") {
    console.log("Usage: node weather.mjs --latitude NUMBER --longitude NUMBER [--timezone IANA_ZONE] [--units celsius|fahrenheit]");
    return;
  }
  try { console.log(JSON.stringify(await fetchForecast(parseArguments(args)))); }
  catch (error) {
    console.error(JSON.stringify({ error: error instanceof WeatherError ? error.code : "WEATHER_FAILED" }));
    process.exitCode = 1;
  }
}

// Keep imports synchronous: OpenClaw's plugin loader may require the ESM graph.
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main().catch(() => {
    console.error(JSON.stringify({ error: "WEATHER_FAILED" }));
    process.exitCode = 1;
  });
}
