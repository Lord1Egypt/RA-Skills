#!/usr/bin/env node
import { fileURLToPath } from 'node:url';
import { realpathSync } from 'node:fs';
const MAX_BYTES = 65536;
class DataError extends Error {
  constructor(code, status, retryAfterSeconds) {
    super(code); this.code = code; this.status = status; this.retryAfterSeconds = retryAfterSeconds;
  }
}
const object = value => value !== null && typeof value === 'object' && !Array.isArray(value);
export function validateObservation(provider, id, payload, nowSeconds, maxAge) {
  if (!object(payload)) throw new DataError('invalid_data');
  const row = provider === 'coingecko' ? payload[id] : payload.coins?.[`coingecko:${id}`];
  if (!object(row)) throw new DataError('missing_observation');
  const price = provider === 'coingecko' ? row.usd : row.price;
  const timestamp = provider === 'coingecko' ? row.last_updated_at : row.timestamp;
  if (typeof price !== 'number' || !Number.isFinite(price) || price <= 0) throw new DataError('invalid_price');
  if (!Number.isSafeInteger(timestamp) || timestamp <= 0) throw new DataError('invalid_timestamp');
  const age = nowSeconds - timestamp;
  if (age < -60) throw new DataError('future_timestamp');
  if (age > maxAge) throw new DataError('stale_observation');
  return { price, timestamp, ageSeconds: Math.max(0, age) };
}
async function readBounded(response) {
  if (Number(response.headers.get('content-length')) > MAX_BYTES) throw new DataError('response_too_large');
  if (!response.body) throw new DataError('invalid_data');
  const reader = response.body.getReader();
  const chunks = []; let lengthRead = 0;
  try {
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      lengthRead += value.byteLength;
      if (lengthRead > MAX_BYTES) throw new DataError('response_too_large');
      chunks.push(value);
    }
    const bytes = new Uint8Array(lengthRead); let offset = 0;
    for (const chunk of chunks) { bytes.set(chunk, offset); offset += chunk.byteLength; }
    try { return JSON.parse(new TextDecoder('utf-8', { fatal: true }).decode(bytes)); }
    catch { throw new DataError('invalid_json'); }
  } finally { void reader.cancel().catch(() => {}); }
}
/** One public GET. Dependencies exist only for deterministic offline tests. */
export async function checkPrice(options = {}, dependencies = {}) {
  const provider = options.provider ?? 'coingecko', id = options.id ?? 'bitcoin', maxAge = options.maxAge ?? 300;
  if (!['coingecko', 'defillama'].includes(provider)) return { ok: false, error: 'invalid_provider' };
  if (typeof id !== 'string' || !/^[a-z0-9][a-z0-9-]{0,99}$/.test(id)) return { ok: false, error: 'invalid_id' };
  if (!Number.isSafeInteger(maxAge) || maxAge < 1 || maxAge > 86400) return { ok: false, error: 'invalid_max_age' };
  const source = provider === 'coingecko' ? 'https://api.coingecko.com/api/v3/simple/price' : 'https://coins.llama.fi/prices/current/';
  const url = provider === 'coingecko' ? `${source}?ids=${encodeURIComponent(id)}&vs_currencies=usd&include_last_updated_at=true` : `${source}coingecko:${encodeURIComponent(id)}`;
  const controller = new AbortController(), request = dependencies.fetch ?? fetch, clock = dependencies.now ?? Date.now;
  let timer;
  const deadline = new Promise((_, reject) => { timer = setTimeout(() => { controller.abort(); reject(new DataError('timeout')); }, dependencies.timeoutMs ?? 10000); });
  try {
    return await Promise.race([deadline, (async () => {
      const response = await request(url, { method: 'GET', redirect: 'error', credentials: 'omit', signal: controller.signal, headers: { accept: 'application/json' } });
      if (!response.ok) {
        void response.body?.cancel().catch(() => {});
        const retry = response.headers.get('retry-after');
        const retryAfterSeconds = retry !== null && /^\d+$/.test(retry) && Number(retry) <= 3600 ? Number(retry) : undefined;
        const code = response.status === 429 ? 'rate_limited' : [401, 403].includes(response.status) ? 'authentication_required' : response.status === 402 ? 'payment_required' : 'http_error';
        throw new DataError(code, response.status, retryAfterSeconds);
      }
      if (response.headers.get('content-type')?.split(';')[0]?.trim() !== 'application/json') throw new DataError('invalid_content_type');
      const payload = await readBounded(response), nowSeconds = Math.floor(clock() / 1000);
      if (!Number.isSafeInteger(nowSeconds) || nowSeconds <= 0) throw new DataError('invalid_local_clock');
      const observation = validateObservation(provider, id, payload, nowSeconds, maxAge);
      return { ok: true, provider, access: 'public-keyless', source, identity: { namespace: 'coingecko', id }, unit: 'USD', price: observation.price,
        observedAt: new Date(observation.timestamp * 1000).toISOString(), retrievedAt: new Date(nowSeconds * 1000).toISOString(), ageSeconds: observation.ageSeconds,
        maxAgeSeconds: maxAge, limitations: ['Aggregate price; not an executable quote or independent oracle.'] };
    })()]);
  } catch (error) {
    // Raw network exceptions, HTTP bodies and headers can contain secrets; expose only typed failures.
    const safe = error instanceof DataError ? error : new DataError(controller.signal.aborted ? 'timeout' : 'network_error');
    return { ok: false, provider, error: safe.code, ...(safe.status !== undefined ? { status: safe.status } : {}), ...(safe.retryAfterSeconds !== undefined ? { retryAfterSeconds: safe.retryAfterSeconds } : {}) };
  } finally { clearTimeout(timer); controller.abort(); }
}
export function parseArgs(args) {
  const options = {}, seen = new Set();
  for (let i = 0; i < args.length; i += 2) {
    const flag = args[i];
    if (!['--provider', '--id', '--max-age'].includes(flag) || seen.has(flag) || !args[i + 1] || args[i + 1].startsWith('--')) throw new DataError('invalid_arguments');
    seen.add(flag);
    if (flag === '--provider') options.provider = args[i + 1];
    if (flag === '--id') options.id = args[i + 1];
    if (flag === '--max-age') options.maxAge = Number(args[i + 1]);
  }
  return options;
}
function isMain() {
  try { return Boolean(process.argv[1]) && realpathSync(process.argv[1]) === fileURLToPath(import.meta.url); }
  catch { return false; }
}
if (isMain()) {
  if (process.argv.length === 3 && ['--help', '-h'].includes(process.argv[2])) {
    process.stdout.write('Public price diagnostic (Node.js 20+)\n\nUsage: node scripts/price-check.mjs [--provider coingecko|defillama] [--id bitcoin] [--max-age 300]\n\nOne keyless GET; no credentials, redirects or automatic retries.\nUse a CoinGecko ID, not a ticker. Success is JSON with price, identity and timestamps.\nFailures return JSON with a stable error code and exit 1. Help makes no request.\n');
    process.exit(0);
  }
  let result;
  try { result = await checkPrice(parseArgs(process.argv.slice(2))); }
  catch { result = { ok: false, error: 'invalid_arguments' }; }
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
  if (!result.ok) process.exitCode = 1;
}
