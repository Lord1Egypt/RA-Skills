#!/usr/bin/env node
/**
 * Update portfolio locally and sync to backend.
 * Usage: node update-portfolio.js "NVDA 25%, BTC 20%, GOOGL 15%"
 *    or: pipe JSON via stdin
 */
import { loadConfig, loadPortfolio, savePortfolio, getChatId, apiCall, log } from './lib.js';

function parsePortfolioInput(input) {
  const holdings = [];
  // Try "NVDA 25%, BTC 20%" format
  const parts = input.split(/[,;]+/).map(s => s.trim()).filter(Boolean);

  for (const part of parts) {
    const match = part.match(/^\$?([A-Za-z.]+)\s*(\d+(?:\.\d+)?)\s*%?$/);
    if (match) {
      holdings.push({ ticker: match[1].toUpperCase(), weight: parseFloat(match[2]) });
    } else {
      // Just a ticker without weight
      const tickerMatch = part.match(/^\$?([A-Za-z.]+)$/);
      if (tickerMatch) {
        holdings.push({ ticker: tickerMatch[1].toUpperCase(), weight: null });
      }
    }
  }

  // If no weights, distribute equally
  const noWeight = holdings.filter(h => h.weight === null);
  if (noWeight.length > 0 && noWeight.length === holdings.length) {
    const w = Math.floor(100 / holdings.length);
    holdings.forEach(h => h.weight = w);
  }

  return holdings;
}

async function main() {
  const input = process.argv.slice(2).join(' ');

  let holdings;
  if (input) {
    holdings = parsePortfolioInput(input);
  } else {
    // Read from stdin
    const chunks = [];
    for await (const chunk of process.stdin) chunks.push(chunk);
    const data = Buffer.concat(chunks).toString();
    try {
      const parsed = JSON.parse(data);
      holdings = parsed.holdings || parsed;
    } catch {
      holdings = parsePortfolioInput(data);
    }
  }

  if (!holdings || holdings.length === 0) {
    console.error('Could not parse holdings. Use format: "NVDA 25%, BTC 20%"');
    process.exit(1);
  }

  // Save locally
  const portfolio = { holdings, last_updated: new Date().toISOString() };
  savePortfolio(portfolio);
  log('update', `Saved ${holdings.length} holdings locally`);

  // Sync to backend
  const chatId = getChatId();
  if (chatId) {
    const result = await apiCall('PUT', `/api/users/${chatId}/holdings`, { holdings });
    log('update', 'Synced to backend');
    console.log(JSON.stringify(result, null, 2));
  } else {
    console.log('Warning: No chatId in config — saved locally only, not synced to backend.');
    console.log(JSON.stringify(portfolio, null, 2));
  }
}

main().catch((err) => {
  console.error('Update failed:', err.message);
  process.exit(1);
});
