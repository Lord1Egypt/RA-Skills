import { fileURLToPath } from 'url';
import { realpathSync } from 'fs';
import { loadConfig } from './lib/config.js';
import { runBrowseEnvCheck } from './setup.js';

const DEFAULT_GAMMA_URL = 'https://gamma-api.polymarket.com';
const DEFAULT_CLOB_URL  = 'https://clob.polymarket.com';

// ── Pure formatting helpers (exported for testing) ────────────────────────────

export function extractTokenIds(market) {
  // CLOB format: tokens array with token_id and outcome fields
  if (market.tokens?.length) {
    const yes = market.tokens.find(t => t.outcome?.toLowerCase() === 'yes');
    const no  = market.tokens.find(t => t.outcome?.toLowerCase() === 'no');
    return { YES: yes?.token_id ?? null, NO: no?.token_id ?? null };
  }
  // Gamma API keyword search format: clobTokenIds (JSON string) + outcomes (JSON string)
  if (market.clobTokenIds) {
    try {
      const tokenIds = JSON.parse(market.clobTokenIds);
      const outcomes = JSON.parse(market.outcomes ?? '["Yes","No"]');
      const yesIdx = outcomes.findIndex(o => o.toLowerCase() === 'yes');
      const noIdx  = outcomes.findIndex(o => o.toLowerCase() === 'no');
      return {
        YES: yesIdx >= 0 ? (tokenIds[yesIdx] ?? null) : (tokenIds[0] ?? null),
        NO:  noIdx  >= 0 ? (tokenIds[noIdx]  ?? null) : (tokenIds[1] ?? null),
      };
    } catch { /* fall through */ }
  }
  return { YES: null, NO: null };
}

export function formatMarketOutput(market, orderbooks = {}, marketInfo = null) {
  const ids = extractTokenIds(market);
  const yes = market.tokens?.find(t => t.outcome?.toLowerCase() === 'yes');
  const no  = market.tokens?.find(t => t.outcome?.toLowerCase() === 'no');
  const obYes = ids.YES ? orderbooks[ids.YES] : null;
  const obNo  = ids.NO  ? orderbooks[ids.NO]  : null;

  // Gamma keyword format: extract prices from outcomePrices (JSON string)
  let yesPrice = yes?.price;
  let noPrice  = no?.price;
  if (yesPrice === undefined && market.outcomePrices) {
    try {
      const outcomes = JSON.parse(market.outcomes ?? '["Yes","No"]');
      const prices   = JSON.parse(market.outcomePrices);
      const yesIdx   = outcomes.findIndex(o => o.toLowerCase() === 'yes');
      const noIdx    = outcomes.findIndex(o => o.toLowerCase() === 'no');
      yesPrice = yesIdx >= 0 ? parseFloat(prices[yesIdx]) : parseFloat(prices[0]);
      noPrice  = noIdx  >= 0 ? parseFloat(prices[noIdx])  : parseFloat(prices[1]);
    } catch { /* fall through — prices remain undefined */ }
  }

  // Polymarket sorts bids ascending (worst first) and asks descending (worst first)
  // so the best bid/ask is always the last element
  const bestBid = ob => ob?.bids?.at(-1)?.price ?? '—';
  const bestAsk = ob => ob?.asks?.at(-1)?.price ?? '—';
  // Approximate total market depth (bid + ask notional), not a one-sided figure
  const liq = ob => {
    if (!ob) return '—';
    const sum = [...(ob.bids ?? []), ...(ob.asks ?? [])]
      .reduce((acc, o) => acc + parseFloat(o.size ?? 0) * parseFloat(o.price ?? 0), 0);
    return `$${sum.toFixed(0)}`;
  };

  const fmtPrice = p => (p != null && Number.isFinite(p)) ? p.toFixed(2) : '—';
  // conditionId comes as camelCase from Gamma, snake_case from CLOB
  const conditionId = market.conditionId ?? market.condition_id ?? marketInfo?.condition_id ?? null;
  const slug = market.slug ?? null;
  const lines = [
    `Market: "${market.question}"`,
    `Status: ${market.active ? 'ACTIVE' : 'CLOSED'} | neg_risk: ${!!market.neg_risk}`,
    `YES: ${fmtPrice(yesPrice)}   bid/ask: ${bestBid(obYes)}/${bestAsk(obYes)}   liquidity: ${liq(obYes)}`,
    `NO:  ${fmtPrice(noPrice)}   bid/ask: ${bestBid(obNo)}/${bestAsk(obNo)}   liquidity: ${liq(obNo)}`,
    `Min order: $${marketInfo?.minimum_order_size ?? marketInfo?.min_order_size ?? market.orderMinSize ?? market.min_incentive_size ?? '—'}`,
    ...(slug        ? [`Slug: ${slug}`]                : []),
    ...(conditionId ? [`ConditionId: ${conditionId}`]  : []),
    `Token IDs:`,
    `  YES: ${ids.YES ?? '(not found)'}`,
    `  NO:  ${ids.NO  ?? '(not found)'}`,
  ];
  return lines.join('\n');
}

// ── Crypto keyword detection ──────────────────────────────────────────────────

const CRYPTO_TERMS = new Set([
  'btc', 'bitcoin', 'eth', 'ethereum', 'sol', 'solana', 'xrp', 'ripple',
  'bnb', 'doge', 'dogecoin', 'ada', 'cardano', 'avax', 'avalanche', 'matic',
  'polygon', 'dot', 'polkadot', 'link', 'chainlink', 'uni', 'uniswap',
  'ltc', 'litecoin', 'atom', 'near', 'algo', 'algorand', 'trx', 'tron',
  'crypto', 'defi', 'nft', 'stablecoin', 'altcoin',
]);

function isCryptoQuery(query) {
  const lower = query.toLowerCase();
  return [...CRYPTO_TERMS].some(t => lower.includes(t));
}

// ── Network fetch helpers ─────────────────────────────────────────────────────

async function fetchGammaEvents(url, { tagSlug, pages = 1 } = {}) {
  const { default: axios } = await import('axios');
  const base = `${url}/events?active=true&closed=false&limit=500`;
  const tag  = tagSlug ? `&tag_slug=${tagSlug}` : '';
  // First page must succeed (errors propagate). Additional pages are best-effort.
  const toEvents = r => Array.isArray(r.data) ? r.data : (r.data?.events ?? []);
  const first = await axios.get(`${base}${tag}&offset=0`, { timeout: 15_000 }).then(toEvents);
  if (pages === 1) return first;
  const rest = await Promise.all(
    Array.from({ length: pages - 1 }, (_, i) =>
      axios.get(`${base}${tag}&offset=${(i + 1) * 500}`, { timeout: 15_000 })
        .then(toEvents)
        .catch(() => [])
    )
  );
  return [first, ...rest].flat();
}

async function fetchGamma(url, query) {
  const { default: axios } = await import('axios');
  if (query.includes('/')) {
    // Direct conditionId/slug lookup — no filter params
    const res = await axios.get(`${url}/markets/${query}`, { timeout: 10_000 });
    const data = res.data;
    return Array.isArray(data) ? data : (data.markets ?? [data]);
  }
  // Keyword search: the Gamma Events API ignores the `q` parameter entirely —
  // fetch active events and filter client-side by event title/slug or market question/slug.
  // Crypto queries use tag_slug=crypto + 2 pages concurrently to cover ETH/BTC price markets
  // that appear beyond the first 200 events.
  const opts = isCryptoQuery(query)
    ? { tagSlug: 'crypto', pages: 2 }
    : { pages: 1 };
  const events = await fetchGammaEvents(url, opts);
  const lq = query.toLowerCase();
  return events.flatMap(e => {
    const eventMatches = e.title?.toLowerCase().includes(lq) || e.slug?.toLowerCase().includes(lq);
    return (e.markets ?? []).filter(m =>
      m.active && !m.closed && (
        eventMatches ||
        m.question?.toLowerCase().includes(lq) ||
        m.slug?.toLowerCase().includes(lq)
      )
    );
  });
}

async function fetchOrderbook(clobUrl, tokenId) {
  const { default: axios } = await import('axios');
  const res = await axios.get(`${clobUrl}/book?token_id=${tokenId}`, { timeout: 10_000 });
  return res.data;
}

async function fetchMarketInfo(clobUrl, conditionId) {
  const { default: axios } = await import('axios');
  const res = await axios.get(`${clobUrl}/markets/${conditionId}`, { timeout: 10_000 });
  return res.data;
}

// ── Main search function ──────────────────────────────────────────────────────

export async function search(query, cfg, limit = 5) {
  const gammaUrl = cfg.yaml?.polymarket?.gamma_url ?? DEFAULT_GAMMA_URL;
  const clobUrl  = cfg.yaml?.polymarket?.clob_url  ?? DEFAULT_CLOB_URL;

  // conditionId: fetch directly from CLOB, skip event search
  if (/^0x[0-9a-fA-F]{64}$/.test(query)) {
    const market = await fetchMarketInfo(clobUrl, query);
    const ids = extractTokenIds(market);
    const orderbooks = {};
    for (const [, tokenId] of Object.entries(ids)) {
      if (tokenId) {
        try { orderbooks[tokenId] = await fetchOrderbook(clobUrl, tokenId); } catch { /* unavailable */ }
      }
    }
    console.log(formatMarketOutput(market, orderbooks, market));
    return;
  }

  const markets = await fetchGamma(gammaUrl, query);
  if (!markets.length) { console.log('No markets found.'); return; }

  for (const market of markets.slice(0, limit)) {
    const ids = extractTokenIds(market);
    const orderbooks = {};
    for (const [side, tokenId] of Object.entries(ids)) {
      if (tokenId) {
        try { orderbooks[tokenId] = await fetchOrderbook(clobUrl, tokenId); }
        catch { /* orderbook unavailable */ }
      }
    }
    // Fetch min_order_size + tick_size from CLOB /markets/<conditionId>
    // Gamma API may return conditionId (camelCase) or condition_id (snake_case)
    let marketInfo = null;
    const condId = market.conditionId ?? market.condition_id;
    if (condId) {
      try { marketInfo = await fetchMarketInfo(clobUrl, condId); }
      catch { /* CLOB market info unavailable */ }
    }
    console.log(formatMarketOutput(market, orderbooks, marketInfo));
    console.log('');
  }
}

// ── Market resolution (slug-first, keyword fallback) ──────────────────────────

export async function resolveMarket(query, cfg) {
  const { default: axios } = await import('axios');
  const gammaUrl = cfg.yaml?.polymarket?.gamma_url ?? DEFAULT_GAMMA_URL;
  const clobUrl  = cfg.yaml?.polymarket?.clob_url  ?? DEFAULT_CLOB_URL;

  // Step 1a: conditionId (0x + 64 hex chars) — look up directly from CLOB, not Gamma
  if (/^0x[0-9a-fA-F]{64}$/.test(query)) {
    const res = await axios.get(`${clobUrl}/markets/${query}`, { timeout: 10_000 });
    return res.data;
  }

  // Step 1b: try exact slug via Gamma ?slug= filter.
  // Gamma /markets/<id> expects a numeric ID; passing a slug returns 422.
  // ?slug=<slug> returns an array and supports exact slug match.
  try {
    const res = await axios.get(`${gammaUrl}/markets?slug=${encodeURIComponent(query)}`, { timeout: 10_000 });
    const results = Array.isArray(res.data) ? res.data : (res.data?.markets ?? []);
    if (results.length === 1) return results[0];
    if (results.length > 1) {
      const exact = results.find(m => m.slug === query);
      if (exact) return exact;
    }
  } catch { /* fall through to keyword search */ }

  // Step 2: keyword fallback — Gamma ?q= ignores the query param; fetch events and
  // filter client-side by event title/slug or market question/slug.
  const opts = isCryptoQuery(query) ? { tagSlug: 'crypto', pages: 2 } : { pages: 1 };
  const events = await fetchGammaEvents(gammaUrl, opts);
  const lq = query.toLowerCase();
  const markets = events.flatMap(e => {
    const em = e.title?.toLowerCase().includes(lq) || e.slug?.toLowerCase().includes(lq);
    return (e.markets ?? []).filter(m =>
      m.active && !m.closed && (em || m.question?.toLowerCase().includes(lq) || m.slug?.toLowerCase().includes(lq))
    );
  });
  if (markets.length === 0) throw new Error(`Market not found: ${query}`);
  if (markets.length === 1) return markets[0];

  // Multiple results — print list and exit
  console.error(`Found ${markets.length} markets matching "${query}":`);
  markets.slice(0, 5).forEach((m, i) => {
    const status = m.active ? 'ACTIVE' : 'CLOSED';
    console.error(`  ${i + 1}. ${(m.slug ?? '(no slug)').padEnd(36)} "${m.question}"  ${status}`);
  });
  console.error(`\nSpecify the exact slug: node scripts/trade.js --buy --market <slug> --side YES|NO --amount <usd>`);
  process.exit(1);
}

// ── CLI entry point ───────────────────────────────────────────────────────────
if (process.argv[1] && realpathSync(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args = process.argv.slice(2);
  const query = args.find(a => !a.startsWith('--'));
  const limitArg = args.indexOf('--limit');
  const limit = limitArg >= 0 ? parseInt(args[limitArg + 1], 10) : 5;
  if (!query) { console.error('Usage: node scripts/browse.js <keyword|slug> [--limit N]'); process.exit(1); }
  (async () => {
    try {
      runBrowseEnvCheck();
      const cfg = loadConfig();
      await search(query, cfg, limit);
    } catch (e) {
      if (e.response?.status === 403) {
        console.error('❌ 403 Forbidden — Polymarket API blocked in your region. Use a VPN.');
      } else {
        console.error('❌', e.message);
      }
      process.exit(1);
    }
  })();
}
