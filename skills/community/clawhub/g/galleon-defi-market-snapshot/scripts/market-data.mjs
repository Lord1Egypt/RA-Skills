#!/usr/bin/env node
import { createHash } from 'node:crypto';
import { realpathSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
export class MarketDataError extends Error {
  constructor(code, status, retryAfterSeconds) { super(code); this.code = code; this.status = status; this.retryAfterSeconds = retryAfterSeconds; }
}
const object = value => value !== null && typeof value === 'object' && !Array.isArray(value);
const idPattern = /^[a-z0-9][a-z0-9-]{0,99}$/;
const errorResult = error => ({ error: error instanceof MarketDataError ? error.code : 'network_error', ...(error instanceof MarketDataError && error.status !== undefined ? { status: error.status } : {}), ...(error instanceof MarketDataError && error.retryAfterSeconds !== undefined ? { retryAfterSeconds: error.retryAfterSeconds } : {}) });
const iso = milliseconds => new Date(milliseconds).toISOString();
function clock(dependencies) {
  const milliseconds = (dependencies.now ?? Date.now)();
  if (!Number.isSafeInteger(milliseconds) || milliseconds <= 0) throw new MarketDataError('invalid_local_clock');
  return milliseconds;
}
async function publicJson(url, maxBytes, dependencies) {
  const controller = new AbortController();
  let timer;
  const deadline = new Promise((_, reject) => { timer = setTimeout(() => { controller.abort(); reject(new MarketDataError('timeout')); }, dependencies.timeoutMs ?? 10000); });
  try {
    return await Promise.race([deadline, (async () => {
      const response = await (dependencies.fetch ?? fetch)(url, { method: 'GET', redirect: 'error', credentials: 'omit', signal: controller.signal, headers: { accept: 'application/json' } });
      if (!response.ok) {
        void response.body?.cancel().catch(() => {});
        const rawRetry = response.headers.get('retry-after');
        const retry = rawRetry !== null && /^\d+$/.test(rawRetry) && Number(rawRetry) <= 3600 ? Number(rawRetry) : undefined;
        throw new MarketDataError(response.status === 429 ? 'rate_limited' : [401, 403].includes(response.status) ? 'authentication_required' : response.status === 402 ? 'payment_required' : 'http_error', response.status, retry);
      }
      if (response.headers.get('content-type')?.split(';')[0]?.trim().toLowerCase() !== 'application/json') throw new MarketDataError('invalid_content_type');
      if (Number(response.headers.get('content-length')) > maxBytes || !response.body) throw new MarketDataError('response_too_large');
      const reader = response.body.getReader(), chunks = []; let length = 0;
      try {
        while (true) {
          const { value, done } = await reader.read();
          if (done) break;
          length += value.byteLength;
          if (length > maxBytes) throw new MarketDataError('response_too_large');
          chunks.push(value);
        }
        const bytes = new Uint8Array(length); let offset = 0;
        for (const chunk of chunks) { bytes.set(chunk, offset); offset += chunk.byteLength; }
        let payload;
        try { payload = JSON.parse(new TextDecoder('utf-8', { fatal: true }).decode(bytes)); }
        catch { throw new MarketDataError('invalid_json'); }
        return { payload, rawSha256: createHash('sha256').update(bytes).digest('hex'), retrievedMs: clock(dependencies) };
      } finally { void reader.cancel().catch(() => {}); }
    })()]);
  } catch (error) {
    throw error instanceof MarketDataError ? error : new MarketDataError(controller.signal.aborted ? 'timeout' : 'network_error');
  } finally { clearTimeout(timer); controller.abort(); }
}
export function normalizeObservation(provider, id, payload, retrievedMs, maxAgeSeconds) {
  if (!object(payload)) throw new MarketDataError('invalid_data');
  const row = provider === 'coingecko' ? payload[id] : payload.coins?.['coingecko:' + id];
  if (!object(row)) throw new MarketDataError('missing_observation');
  const priceUsd = provider === 'coingecko' ? row.usd : row.price;
  const timestampSeconds = provider === 'coingecko' ? row.last_updated_at : row.timestamp;
  if (typeof priceUsd !== 'number' || !Number.isFinite(priceUsd) || priceUsd < 1e-12 || priceUsd > 1e12) throw new MarketDataError('invalid_price');
  if (!Number.isSafeInteger(timestampSeconds) || timestampSeconds <= 0) throw new MarketDataError('invalid_timestamp');
  const ageSeconds = Math.floor(retrievedMs / 1000) - timestampSeconds;
  if (ageSeconds < -60) throw new MarketDataError('future_timestamp');
  if (ageSeconds > maxAgeSeconds) throw new MarketDataError('stale_observation');
  if (provider === 'defillama' && row.confidence !== undefined && (typeof row.confidence !== 'number' || !Number.isFinite(row.confidence) || row.confidence < 0 || row.confidence > 1)) throw new MarketDataError('invalid_confidence');
  return { provider, identity: { namespace: 'coingecko', id }, unit: 'USD', priceUsd, observedAt: iso(timestampSeconds * 1000), retrievedAt: iso(retrievedMs), ageSeconds: Math.max(0, ageSeconds), ...(provider === 'defillama' && row.confidence !== undefined ? { providerConfidence: row.confidence } : {}) };
}
export async function marketSnapshot(options = {}, dependencies = {}) {
  const ids = options.ids ?? ['bitcoin', 'ethereum'], provider = options.provider ?? 'both';
  const maxAgeSeconds = options.maxAgeSeconds ?? 300, maxSkewSeconds = options.maxSkewSeconds ?? 120;
  if (!Array.isArray(ids) || ids.length < 1 || ids.length > 10 || new Set(ids).size !== ids.length || !ids.every(id => typeof id === 'string' && idPattern.test(id))) return { ok: false, error: 'invalid_ids' };
  if (!['coingecko', 'defillama', 'both'].includes(provider)) return { ok: false, error: 'invalid_provider' };
  if (!Number.isSafeInteger(maxAgeSeconds) || maxAgeSeconds < 1 || maxAgeSeconds > 86400 || !Number.isSafeInteger(maxSkewSeconds) || maxSkewSeconds < 0 || maxSkewSeconds > 3600) return { ok: false, error: 'invalid_age_or_skew' };
  const providers = provider === 'both' ? ['coingecko', 'defillama'] : [provider];
  const reads = await Promise.all(providers.map(async name => {
    const source = name === 'coingecko' ? 'https://api.coingecko.com/api/v3/simple/price' : 'https://coins.llama.fi/prices/current/';
    const url = name === 'coingecko' ? source + '?ids=' + ids.join(',') + '&vs_currencies=usd&include_last_updated_at=true' : source + ids.map(id => 'coingecko:' + id).join(',');
    try {
      const response = await publicJson(url, 131072, dependencies);
      return { provider: name, source, rawSha256: response.rawSha256, retrievedAt: iso(response.retrievedMs), observations: ids.map(id => {
        try { return { ok: true, ...normalizeObservation(name, id, response.payload, response.retrievedMs, maxAgeSeconds) }; }
        catch (error) { return { ok: false, provider: name, identity: { namespace: 'coingecko', id }, ...errorResult(error) }; }
      }) };
    } catch (error) {
      return { provider: name, source, observations: ids.map(id => ({ ok: false, provider: name, identity: { namespace: 'coingecko', id }, ...errorResult(error) })) };
    }
  }));
  const observations = reads.flatMap(read => read.observations), valid = observations.filter(row => row.ok);
  const comparisons = provider === 'both' ? ids.map(id => {
    const rows = valid.filter(row => row.identity.id === id);
    if (rows.length !== 2) return { identity: { namespace: 'coingecko', id }, status: 'incomplete', spreadPct: null };
    const skewSeconds = Math.abs(Date.parse(rows[0].observedAt) - Date.parse(rows[1].observedAt)) / 1000;
    if (skewSeconds > maxSkewSeconds) return { identity: { namespace: 'coingecko', id }, status: 'unaligned', skewSeconds, spreadPct: null };
    const spreadPct = Math.abs(rows[0].priceUsd - rows[1].priceUsd) / ((rows[0].priceUsd + rows[1].priceUsd) / 2) * 100;
    return { identity: { namespace: 'coingecko', id }, status: 'aligned', skewSeconds, spreadPct };
  }) : [];
  return { ok: valid.length === observations.length, schemaVersion: 1, status: valid.length === observations.length ? 'complete' : valid.length ? 'partial' : 'unavailable', access: 'public-keyless', parameters: { ids, provider, maxAgeSeconds, maxSkewSeconds }, reads, comparisons,
    limitations: ['Aggregate USD marks are not executable quotes or balance evidence.', 'DefiLlama CoinGecko-ID observations may share upstream data; agreement is not independent oracle corroboration.', 'Spread is shown only for fresh observations within the declared timestamp skew; no consensus price is invented.'] };
}
export function normalizeHistory(payload, id, retrievedMs, days, rawSha256) {
  if (!object(payload) || !Array.isArray(payload.prices) || payload.prices.length < 2 || payload.prices.length > 1000) throw new MarketDataError('invalid_history');
  const candles = []; let previous = -1, excludedTrailingObservation = false;
  const today = Math.floor(retrievedMs / 86400000) * 86400000;
  for (let i = 0; i < payload.prices.length; i++) {
    const row = payload.prices[i];
    if (!Array.isArray(row) || row.length !== 2 || !Number.isSafeInteger(row[0]) || row[0] <= previous || row[0] > retrievedMs || typeof row[1] !== 'number' || !Number.isFinite(row[1]) || row[1] < 1e-12 || row[1] > 1e12) throw new MarketDataError('invalid_history_observation');
    previous = row[0];
    if (row[0] % 86400000 !== 0) {
      if (i !== payload.prices.length - 1 || row[0] < today) throw new MarketDataError('unexpected_history_granularity');
      excludedTrailingObservation = true; continue;
    }
    if (candles.length && row[0] - Date.parse(candles.at(-1).timestamp) !== 86400000) throw new MarketDataError('gapped_history');
    candles.push({ timestamp: iso(row[0]), close: row[1] });
  }
  if (candles.length < days - 1) throw new MarketDataError('insufficient_history');
  if (candles.length > days + 1) throw new MarketDataError('unexpected_history_range');
  if (today - Date.parse(candles.at(-1).timestamp) > 86400000) throw new MarketDataError('stale_history');
  return { dataset: { schemaVersion: 1, identity: { namespace: 'coingecko', id }, unit: 'USD', intervalSeconds: 86400, priceType: 'aggregate-snapshot', provenance: { provider: 'coingecko', source: 'https://api.coingecko.com/api/v3/coins/' + id + '/market_chart', retrievedAt: iso(retrievedMs), synthetic: false, rawSha256 }, candles }, excludedTrailingObservation };
}
export async function collectHistory(options = {}, dependencies = {}) {
  const id = options.id ?? 'bitcoin', days = options.days ?? 180;
  if (typeof id !== 'string' || !idPattern.test(id)) return { ok: false, error: 'invalid_id' };
  if (!Number.isSafeInteger(days) || days < 91 || days > 365) return { ok: false, error: 'invalid_days' };
  const source = 'https://api.coingecko.com/api/v3/coins/' + id + '/market_chart';
  try {
    const response = await publicJson(source + '?vs_currency=usd&days=' + days, 2097152, dependencies);
    return { ok: true, access: 'public-keyless', parameters: { id, days, vsCurrency: 'usd', interval: 'automatic-daily' }, ...normalizeHistory(response.payload, id, response.retrievedMs, days, response.rawSha256), limitations: ['Daily UTC aggregate observations, not venue candle closes or executable prices.', 'The current trailing observation is excluded when it is not at UTC midnight; daily gaps fail rather than interpolate.', 'Public keyless availability is diagnostic; no Demo/Pro account entitlement or future provider availability is established.'] };
  } catch (error) { return { ok: false, provider: 'coingecko', ...errorResult(error) }; }
}
export function parseArgs(args) {
  const [command, ...flags] = args;
  if (!['snapshot', 'history'].includes(command)) throw new MarketDataError('invalid_arguments');
  const allowed = command === 'snapshot' ? ['--provider', '--ids', '--max-age', '--max-skew'] : ['--id', '--days'];
  const options = {}, seen = new Set();
  for (let i = 0; i < flags.length; i += 2) {
    const flag = flags[i], value = flags[i + 1];
    if (!allowed.includes(flag) || seen.has(flag) || !value || value.startsWith('--')) throw new MarketDataError('invalid_arguments');
    seen.add(flag);
    if (flag === '--provider') options.provider = value;
    else if (flag === '--ids') options.ids = value.split(',');
    else if (flag === '--id') options.id = value;
    else if (flag === '--days') options.days = Number(value);
    else if (flag === '--max-age') options.maxAgeSeconds = Number(value);
    else if (flag === '--max-skew') options.maxSkewSeconds = Number(value);
  }
  return { command, options };
}
function isMain() {
  try { return Boolean(process.argv[1]) && realpathSync(process.argv[1]) === fileURLToPath(import.meta.url); }
  catch { return false; }
}
if (isMain()) {
  let result;
  if (process.argv.length === 3 && ['--help', '-h'].includes(process.argv[2])) {
    process.stdout.write('Public market evidence (Node.js 20+)\nUsage:\n  node scripts/market-data.mjs snapshot [--provider both|coingecko|defillama] [--ids bitcoin,ethereum] [--max-age 300] [--max-skew 120]\n  node scripts/market-data.mjs history [--id bitcoin] [--days 180]\nOne fixed public GET per provider; no keys, redirects or retries. History emits dataset compatible with the daily strategy model. Failures and partial snapshots exit 1.\n');
  } else {
    try { const { command, options } = parseArgs(process.argv.slice(2)); result = command === 'history' ? await collectHistory(options) : await marketSnapshot(options); }
    catch (error) { result = { ok: false, ...errorResult(error) }; }
    process.stdout.write(JSON.stringify(result, null, 2) + '\n');
    if (!result.ok) process.exitCode = 1;
  }
}
