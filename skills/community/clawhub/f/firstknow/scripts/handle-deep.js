#!/usr/bin/env node
// Usage: node handle-deep.js [--event-id evt_xxx]
// Handles "deep" reply from user:
// 1. Fetches the most recent event for the user from backend API
// 2. Loads user's portfolio and config
// 3. Calls analyzeEventDeep() with the event + portfolio
// 4. Delivers the deep analysis via Telegram
// Also exportable: handleDeep({eventId})

import { readFile } from 'fs/promises';
import { homedir } from 'os';
import { join } from 'path';
import { config as loadDotenv } from 'dotenv';

import { analyzeEventDeep } from './analyze.js';
import { deliverTelegram } from './deliver.js';

const FIRSTKNOW_DIR = join(homedir(), '.firstknow');
const DEFAULT_API_BASE = 'https://api.firstknow.ai';

// Load .env from ~/.firstknow/.env
loadDotenv({ path: join(FIRSTKNOW_DIR, '.env') });

function log(msg) {
  const ts = new Date().toISOString();
  console.error(`[${ts}] [handle-deep] ${msg}`);
}

async function loadConfig() {
  try {
    const raw = await readFile(join(FIRSTKNOW_DIR, 'config.json'), 'utf-8');
    return JSON.parse(raw);
  } catch {
    throw new Error('Config not found. Run "node setup.js" to configure FirstKnow.');
  }
}

async function loadPortfolio() {
  try {
    const raw = await readFile(join(FIRSTKNOW_DIR, 'portfolio.json'), 'utf-8');
    return JSON.parse(raw);
  } catch {
    throw new Error('Portfolio not found. Run "node setup.js" to configure FirstKnow.');
  }
}

/**
 * Fetch the latest event from the backend API.
 * If eventId is provided, fetches that specific event.
 * Otherwise fetches the most recent event matching the user's tickers.
 */
async function fetchLatestEvent({ eventId, tickers, apiBase }) {
  const base = apiBase || DEFAULT_API_BASE;

  let url;
  if (eventId) {
    url = new URL(`/api/events/${eventId}`, base);
  } else {
    url = new URL('/api/events/latest', base);
    if (tickers && tickers.length > 0) {
      url.searchParams.set('tickers', tickers.join(','));
    }
  }

  log(`Fetching event from ${url.toString()}`);

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 15_000);

  try {
    const res = await fetch(url.toString(), {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'User-Agent': 'FirstKnow-Skill/1.0',
      },
      signal: controller.signal,
    });

    if (!res.ok) {
      const body = await res.text().catch(() => '');
      throw new Error(`API returned ${res.status}: ${body.slice(0, 200)}`);
    }

    const data = await res.json();

    // API may return { event: {...} } or just {...}
    const event = data.event || data;

    if (!event || !event.headline) {
      throw new Error('No recent event found for your tickers.');
    }

    log(`Got event: "${event.headline}"`);
    return event;
  } catch (err) {
    if (err.name === 'AbortError') {
      throw new Error('API request timed out after 15s');
    }
    throw err;
  } finally {
    clearTimeout(timeout);
  }
}

/**
 * Handle a "deep" analysis request.
 * @param {Object} [opts]
 * @param {string} [opts.eventId] - Specific event ID to analyze
 * @returns {Promise<{analysis: string, event: Object}>}
 */
export async function handleDeep({ eventId } = {}) {
  const config = await loadConfig();
  const portfolio = await loadPortfolio();

  const chatId = config.delivery?.chatId;
  if (!chatId) {
    throw new Error('No Telegram chat ID configured. Run "node setup.js".');
  }

  const apiBase = config.api_base_url || DEFAULT_API_BASE;
  const tickers = portfolio.holdings?.map(h => h.ticker) || [];

  // 1. Fetch the event
  const event = await fetchLatestEvent({ eventId, tickers, apiBase });

  // 2. Run deep analysis
  log('Running deep analysis...');
  const originalAlert = event.template_alert || event.headline || '';
  const analysis = await analyzeEventDeep(event, portfolio, config, originalAlert);

  // 3. Deliver via Telegram
  log('Delivering deep analysis...');
  await deliverTelegram(chatId, analysis, undefined, {
    addFooter: false,
    config,
    silent: false,
  });

  log('Deep analysis delivered successfully');
  return { analysis, event };
}

// --- CLI entry point ---
function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    switch (argv[i]) {
      case '--event-id':
        args.eventId = argv[++i];
        break;
      default:
        log(`Unknown argument: ${argv[i]}`);
    }
  }
  return args;
}

const isMain = process.argv[1] && (
  process.argv[1].endsWith('/handle-deep.js') ||
  process.argv[1].endsWith('\\handle-deep.js')
);

if (isMain) {
  const args = parseArgs(process.argv);

  handleDeep(args)
    .then(result => {
      console.log(result.analysis);
    })
    .catch(err => {
      log(`Error: ${err.message}`);
      process.exit(1);
    });
}
