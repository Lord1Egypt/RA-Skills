#!/usr/bin/env node
/**
 * Blink Wallet — L402 Service Discovery (Search)
 *
 * Usage:
 *   node l402_search.js [query] [options]
 *
 * Searches L402 service directories for paid APIs that agents can access.
 *
 * Sources:
 *   l402.directory (default) — 8+ curated services, rich schema with endpoints,
 *                               pricing, consumption instructions. Agent-optimized.
 *   402index.io              — 50+ services, broader coverage, simpler flat schema.
 *
 * Arguments:
 *   query           - Optional. Keyword to search across names and descriptions.
 *   --source        - Optional. "directory" (default) or "402index".
 *   --category      - Optional. Filter by category (e.g. "video", "data", "ai").
 *   --status        - Optional. Filter by status: "live" (default), "all".
 *   --format        - Optional. "full" (default) or "minimal" (compact output).
 *
 * No API key required — both directories have free browse APIs.
 *
 * Output: JSON to stdout. Status messages to stderr.
 * Dependencies: None (Node.js 22+ built-in fetch).
 */

'use strict';

const { strictParseArgs } = require('./_blink_client');

// ── Directory URLs ───────────────────────────────────────────────────────────

const DIRECTORY_URL = 'https://l402.directory/api/services';
const INDEX_URL = 'https://402index.io/api/v1/services';

// ── Arg parsing ──────────────────────────────────────────────────────────────

// Every option this script accepts (strict; exported for the CLI-forwarding guard).
const ARG_OPTIONS = {
  source: { type: 'string', default: 'directory' },
  category: { type: 'string' },
  status: { type: 'string', default: 'live' },
  format: { type: 'string', default: 'full' },
  help: { type: 'boolean', short: 'h', default: false },
};

function parseCliArgs(argv) {
  // Strict (PR #28 review): conflicting repeats and extra positionals are
  // refused, and errors never echo argument values.
  const { values, positionals } = strictParseArgs(argv, ARG_OPTIONS, { positionals: [0, 1] });

  if (values.help) {
    console.error(
      [
        'Usage: blink l402-search [query] [options]',
        '',
        'Options:',
        '  --source <name>     "directory" (default) or "402index"',
        '  --category <name>   Filter by category (e.g. video, data, ai)',
        '  --status <name>     "live" (default) or "all"',
        '  --format <name>     "full" (default) or "minimal"',
        '  --help, -h          Show this help',
      ].join('\n'),
    );
    process.exit(0);
  }

  const source = values.source.toLowerCase();
  if (source !== 'directory' && source !== '402index') {
    throw new Error('--source must be "directory" or "402index".');
  }

  return {
    query: positionals[0] || null,
    source,
    category: values.category || null,
    status: values.status,
    format: values.format,
  };
}

// ── l402.directory search ────────────────────────────────────────────────────

async function searchDirectory({ query, category, status, format }) {
  const params = new URLSearchParams();
  if (query) params.set('q', query);
  if (category) params.set('category', category);
  if (status === 'all') params.set('status', 'all');
  if (format === 'minimal') params.set('format', 'minimal');

  const url = `${DIRECTORY_URL}?${params}`;
  console.error(`Searching l402.directory...`);

  const res = await fetch(url, {
    headers: { Accept: 'application/json' },
    signal: AbortSignal.timeout(15_000),
  });

  if (!res.ok) {
    throw new Error(`l402.directory returned HTTP ${res.status}: ${await res.text().catch(() => '')}`);
  }

  const data = await res.json();
  const services = data.services || [];

  return {
    source: 'l402.directory',
    url: DIRECTORY_URL,
    query: query || null,
    category: category || null,
    count: services.length,
    services,
  };
}

// ── 402index.io search ───────────────────────────────────────────────────────

async function searchIndex({ query, category, status }) {
  const params = new URLSearchParams();
  params.set('protocol', 'l402');
  if (status !== 'all') params.set('health', 'healthy');
  if (category) params.set('category', category);

  const url = `${INDEX_URL}?${params}`;
  console.error(`Searching 402index.io...`);

  const res = await fetch(url, {
    headers: { Accept: 'application/json' },
    signal: AbortSignal.timeout(15_000),
  });

  if (!res.ok) {
    throw new Error(`402index.io returned HTTP ${res.status}: ${await res.text().catch(() => '')}`);
  }

  const data = await res.json();
  let services = data.services || [];

  // Client-side keyword filter (402index doesn't have a query param)
  if (query) {
    const q = query.toLowerCase();
    services = services.filter(
      (s) =>
        (s.name && s.name.toLowerCase().includes(q)) ||
        (s.description && s.description.toLowerCase().includes(q)) ||
        (s.category && s.category.toLowerCase().includes(q)),
    );
  }

  // Normalize to a simpler shape
  services = services.map((s) => ({
    id: s.id,
    name: s.name,
    description: s.description,
    url: s.url,
    priceSats: s.price_sats,
    category: s.category,
    provider: s.provider,
    status: s.health_status,
    uptime30d: s.uptime_30d,
    latencyP50ms: s.latency_p50_ms,
    reliabilityScore: s.reliability_score,
  }));

  return {
    source: '402index.io',
    url: INDEX_URL,
    query: query || null,
    category: category || null,
    count: services.length,
    services,
  };
}

// ── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  const args = parseCliArgs(process.argv.slice(2));

  let result;
  if (args.source === '402index') {
    result = await searchIndex(args);
  } else {
    result = await searchDirectory(args);
  }

  console.error(`Found ${result.count} service(s).`);
  console.log(JSON.stringify(result, null, 2));
}

if (require.main === module) {
  main().catch((e) => {
    console.error('Error:', e.message);
    process.exit(1);
  });
}

module.exports = { main, parseCliArgs, searchDirectory, searchIndex, DIRECTORY_URL, INDEX_URL, ARG_OPTIONS };
