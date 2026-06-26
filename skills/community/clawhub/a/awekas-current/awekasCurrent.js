import fetch from "node-fetch";

const CACHE_TTL = 60_000;
const cache = new Map();

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

function normalize(data) {
  return {
    temperature: data?.temperature ?? data?.temp ?? null,
    humidity: data?.humidity ?? null,
    pressure: data?.pressure ?? null,
    wind: {
      speed: data?.wind_speed ?? data?.wind?.speed ?? null,
      direction: data?.wind_dir ?? data?.wind?.direction ?? null,
    },
    rain: data?.rain ?? null,
    raw: data,
  };
}

async function fetchWithRetry(url, retries = 2) {
  for (let i = 0; i <= retries; i++) {
    try {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 8000);

      const res = await fetch(url, { signal: controller.signal });
      const text = await res.text();

      clearTimeout(timeout);

      if (!res.ok) throw new Error(`HTTP ${res.status}: ${text}`);
      return text;
    } catch (err) {
      if (i === retries) throw err;
      await sleep(500 * (i + 1));
    }
  }
}

export default {
  name: "awekas-current",

  async run(ctx, args) {
    const apiKey = args.key || process.env.AWEKAS_KEY;

    if (!apiKey) {
      throw new Error("Missing API key (key or AWEKAS_KEY)");
    }

    const station = args.station || "default";
    const cacheKey = `${station}:${apiKey}`;
    const now = Date.now();

    const cached = cache.get(cacheKey);
    if (cached && now - cached.time < CACHE_TTL) {
      return {
        source: "AWEKAS",
        cached: true,
        station,
        data: cached.data,
      };
    }

    const url = new URL("https://api.awekas.at/current.php");
    url.searchParams.set("key", apiKey);

    if (args.station) {
      url.searchParams.set("station", args.station);
    }

    try {
      const text = await fetchWithRetry(url.toString(), 2);

      let parsed;
      try {
        parsed = JSON.parse(text);
      } catch {
        parsed = { raw: text };
      }

      const normalized = normalize(parsed);

      cache.set(cacheKey, {
        time: now,
        data: normalized,
      });

      return {
        source: "AWEKAS",
        station,
        cached: false,
        data: normalized,
      };
    } catch (err) {
      const message = err?.message || String(err);

      ctx?.log?.(`AWEKAS error: ${message}`);

      throw {
        error: "AWEKAS_FETCH_FAILED",
        type:
          message.includes("HTTP") ? "api_error"
          : message.includes("abort") ? "timeout"
          : "network_error",
        message,
      };
    }
  },
};