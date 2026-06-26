#!/usr/bin/env node
// Brave Spellcheck - uses Brave Search API spellcheck endpoint
// Requires: BRAVE_SPELLCHECK_API_KEY or BRAVE_SEARCH_API_KEY env var

const BASE_URL = 'https://api.search.brave.com/res/v1';
const { parseArgs, fetchWithRetry } = require('./utils');

function getSpellcheckKey() {
  return (
    process.env.BRAVE_SPELLCHECK_API_KEY ||
    process.env.BRAVE_SEARCH_API_KEY ||
    null
  );
}

async function braveSpellcheck(query, country) {
  const apiKey = getSpellcheckKey();
  if (!apiKey) {
    console.error('Error: BRAVE_SPELLCHECK_API_KEY or BRAVE_SEARCH_API_KEY environment variable not set.');
    console.error('Get your key at: https://api-dashboard.search.brave.com');
    process.exit(1);
  }

  const url = new URL(`${BASE_URL}/spellcheck/search`);
  url.searchParams.set('q', query);
  url.searchParams.set('country', country);

  const res = await fetchWithRetry(url.toString(), {
    headers: {
      'Accept': 'application/json',
      'Accept-Encoding': 'gzip',
      'X-Subscription-Token': apiKey,
    },
  });

  if (!res.ok) {
    const body = await res.text();
    console.error(`Brave API error ${res.status}: ${body}`);
    process.exit(1);
  }

  return res.json();
}

function formatSpellcheck(data) {
  const original = data.query?.original || '';
  const results = data.results || [];

  // If no results, or every result is identical to the original — no correction needed
  const hasCorrection = results.length > 0 && results.some(r => r.query !== original);

  if (!hasCorrection) {
    return `Spellcheck for "${original}": no correction needed. ✓`;
  }

  const lines = [`Did you mean:`];
  for (let i = 0; i < results.length; i++) {
    lines.push(`  ${i + 1}. ${results[i].query}`);
  }
  return lines.join('\n');
}

async function main() {
  const args = parseArgs(process.argv);

  const query = args.query || args.q;
  if (!query) {
    console.error(
      'Usage: brave_spellcheck.js --query "your search query" [--country us]\n' +
      '  Short form: --q "your search query"'
    );
    process.exit(1);
  }

  const country = (args.country || 'US').toUpperCase();
  const data = await braveSpellcheck(query, country);
  console.log(formatSpellcheck(data));
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
