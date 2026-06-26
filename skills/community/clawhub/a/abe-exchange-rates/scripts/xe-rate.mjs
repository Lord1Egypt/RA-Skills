#!/usr/bin/env node
// Fetch exchange rates from XE.com via SkillBoss API Hub scraping
// Usage: node xe-rate.mjs <FROM> <TO> [AMOUNT]
// Example: node xe-rate.mjs USD INR 100

import process from 'node:process';

const SKILLBOSS_API_KEY = process.env.SKILLBOSS_API_KEY;
const API_BASE = 'https://api.heybossai.com/v1';

const from = (process.argv[2] || 'USD').toUpperCase();
const to = (process.argv[3] || 'INR').toUpperCase();
const amount = parseFloat(process.argv[4] || '1');

if (!from || !to) {
  console.error('Usage: node xe-rate.mjs <FROM> <TO> [AMOUNT]');
  process.exit(1);
}

async function pilot(body) {
  const r = await fetch(`${API_BASE}/pilot`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${SKILLBOSS_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
  return r.json();
}

async function fetchXE() {
  try {
    const url = `https://www.xe.com/currencyconverter/convert/?Amount=${amount}&From=${from}&To=${to}`;
    const result = await pilot({ type: 'scraper', inputs: { url } });
    const text = result.result.data.markdown;

    // Extract unit rate: "1.00 USD = 91.67885558 INR"
    const unitMatch = text.match(/1\.00\s+(\w{3})\s*=\s*([\d,.]+)\s+(\w{3})/);

    // Extract converted amount from the big display
    // Pattern: the "To" section shows the converted number
    const toMatch = text.match(/To\s+To\s+([\d,.]+)\s/);

    if (unitMatch) {
      const rate = parseFloat(unitMatch[2].replace(/,/g, ''));
      const converted = toMatch ? parseFloat(toMatch[1].replace(/,/g, '')) : (amount * rate);
      return {
        amount,
        from,
        to,
        rate,
        converted,
        source: 'xe.com (mid-market)',
        timestamp: new Date().toISOString()
      };
    }
    return null;
  } catch (e) {
    return null;
  }
}

async function fetchFreeAPI() {
  try {
    const res = await fetch(`https://open.er-api.com/v6/latest/${from}`);
    const data = await res.json();
    if (data.result === 'success' && data.rates[to]) {
      const rate = data.rates[to];
      const converted = parseFloat((amount * rate).toFixed(2));
      return {
        amount,
        from,
        to,
        rate,
        converted,
        source: 'exchangerate-api.com (fallback)',
        timestamp: data.time_last_update_utc
      };
    }
  } catch (e) {}
  return null;
}

(async () => {
  let result = await fetchXE();
  if (!result) result = await fetchFreeAPI();

  if (result) {
    console.log(JSON.stringify(result, null, 2));
  } else {
    console.error(JSON.stringify({ error: `Could not fetch ${from} to ${to} rate` }));
    process.exit(1);
  }
})();
