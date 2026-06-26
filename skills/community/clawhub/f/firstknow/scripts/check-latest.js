#!/usr/bin/env node
/**
 * Fetch latest events from backend for user's tickers.
 * Usage: node check-latest.js [--format json] [--limit N]
 */
import { loadPortfolio, apiCall, log } from './lib.js';

async function main() {
  const args = process.argv.slice(2);
  const jsonMode = args.includes('--format') && args[args.indexOf('--format') + 1] === 'json';
  const limitIdx = args.indexOf('--limit');
  const limit = limitIdx >= 0 ? parseInt(args[limitIdx + 1], 10) || 10 : 10;

  const portfolio = loadPortfolio();
  if (!portfolio || !portfolio.holdings?.length) {
    console.error('No portfolio found. Run setup first.');
    process.exit(1);
  }

  const tickers = portfolio.holdings
    .filter(h => h.ticker !== 'CASH')
    .map(h => h.ticker)
    .join(',');

  log('check', `Fetching events for: ${tickers}`);

  const since = new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString();
  const result = await apiCall('GET', `/api/events?tickers=${tickers}&since=${since}&limit=${limit}`);

  if (jsonMode) {
    console.log(JSON.stringify(result, null, 2));
  } else {
    const events = result.events || [];
    if (events.length === 0) {
      console.log('No recent events for your holdings in the last 24 hours.');
      return;
    }

    console.log(`\n📰 ${events.length} recent event(s) for your holdings:\n`);
    for (const event of events) {
      let tickers = '';
      try {
        const parsed = JSON.parse(event.affected_tickers || '[]');
        tickers = Array.isArray(parsed) ? parsed.join(', ') : String(parsed);
      } catch {
        tickers = String(event.affected_tickers || '');
      }
      console.log(`  🔔 ${event.headline}`);
      console.log(`     ${event.event_type} | ${tickers} | ${event.source}`);
      if (event.raw_content) console.log(`     📰 ${event.raw_content}`);
      if (event.source_url) console.log(`     🔗 ${event.source_url}`);
      console.log(`     ${event.timestamp}\n`);
    }
  }
}

main().catch((err) => {
  console.error('Check failed:', err.message);
  process.exit(1);
});
