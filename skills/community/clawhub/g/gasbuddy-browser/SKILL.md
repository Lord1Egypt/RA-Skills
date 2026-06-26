---
name: gasbuddy-browser
description: Use Playwright via Bash `exec` tool (not the built-in browser tool) to fetch GasBuddy fuel prices for a target city/area (especially Toronto/North York), and return top station prices. Trigger when users ask to check gas prices on GasBuddy, compare stations, or automate GasBuddy search/sort/filter steps.
---

# GasBuddy Browser Skill

> **⚠️ Important: Use Playwright via `exec` tool, NOT the built-in `browser` tool.**
> The built-in OpenClaw Edge CDP browser cannot reliably wait out Cloudflare's time-based challenge. Direct Playwright via Node.js can navigate to the city URL and wait for the challenge to auto-resolve.

## Quick Workflow

1. Navigate directly to the city gas price URL (North York as default, e.g. `https://www.gasbuddy.com/gasprices/ontario/north-york`)
2. **Wait for Cloudflare challenge to clear** — title will change from "Just a moment..." to "Best Gas Prices & Local Gas Stations in..."
3. Scroll incrementally to load all station cards
4. Extract station data using `[class*="stationListItem"]` selector and price regex
5. Return top 5 cheapest stations

## Playwright Script Template

```javascript
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({
    headless: false,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
    // No need for --disable-blink-features=AutomationControlled or custom UA
    // Cloudflare challenge is time-based, not detection-based
  });
  const page = await browser.newPage();

  await page.goto('https://www.gasbuddy.com/gasprices/ontario/north-york', {
    timeout: 60000,
    waitUntil: 'networkidle'
  });

  // Wait for Cloudflare to clear — check title changes away from challenge page
  let attempts = 0;
  while (attempts < 20) {
    const title = await page.title();
    if (!title.includes('Just a moment') && !title.includes('Cloudflare') && title.includes('Gas Prices')) break;
    await page.waitForTimeout(3000);
    attempts++;
  }

  // Scroll incrementally to trigger lazy loading of all station cards
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(500);
  for (let i = 0; i < 8; i++) {
    await page.evaluate(() => window.scrollBy(0, 600));
    await page.waitForTimeout(400);
  }
  await page.waitForTimeout(2000);

  // Extract station data using the actual CSS class and price format
  // If prices show "- - -" (unavailable), we retry with a page refresh
  let stations = await page.evaluate(() => {
    const cards = document.querySelectorAll('[class*="stationListItem"]');
    return Array.from(cards).map(card => {
      const text = card.innerText;
      const lines = text.split('\n').map(l => l.trim()).filter(l => l);

      // Price format is "XXX.X¢" (one decimal, e.g. "167.9¢")
      const priceMatch = text.match(/(\d+\.\d+)\s*¢/);
      const price = priceMatch ? priceMatch[1] : null; // e.g. "167.9"

      // Check for "- - -" placeholder indicating unavailable price
      const hasDashPrice = text.includes('- - -') || text.includes('— — —');

      // Brand is first non-empty line
      const brand = lines[0] || '';

      // Address is a line starting with digit followed by letters
      const address = lines.find(l => /^\d+\s+[A-Za-z]/.test(l)) || '';

      return { brand, price, address, hasDashPrice };
    }).filter(s => s.price && s.address);
  });

  // If prices show "- - -" (all have hasDashPrice or price is null), refresh and retry
  const hasValidPrices = stations.length > 0 && stations.some(s => s.price && !s.hasDashPrice);
  if (!hasValidPrices) {
    console.log('Prices not loaded (showing "- - -"), refreshing...');
    await page.reload({ timeout: 30000, waitUntil: 'networkidle' });
    await page.waitForTimeout(3000);
    // Re-scroll after reload
    for (let i = 0; i < 5; i++) {
      await page.evaluate(() => window.scrollBy(0, 600));
      await page.waitForTimeout(400);
    }
    stations = await page.evaluate(() => {
      const cards = document.querySelectorAll('[class*="stationListItem"]');
      return Array.from(cards).map(card => {
        const text = card.innerText;
        const lines = text.split('\n').map(l => l.trim()).filter(l => l);
        const priceMatch = text.match(/(\d+\.\d+)\s*¢/);
        const price = priceMatch ? priceMatch[1] : null;
        const brand = lines[0] || '';
        const address = lines.find(l => /^\d+\s+[A-Za-z]/.test(l)) || '';
        return { brand, price, address };
      }).filter(s => s.price && s.address);
    });
  }

  // Sort by price ascending
  stations.sort((a, b) => parseFloat(a.price) - parseFloat(b.price));

  const date = new Date().toLocaleDateString('en-CA', { year: 'numeric', month: 'short', day: 'numeric' });
  console.log(`\n🔥 North York Gas Prices (Regular 87) — ${date}`);
  console.log('='.repeat(55));
  stations.slice(0, 8).forEach((s, i) => {
    const p = parseFloat(s.price);
    console.log(`${i+1}. ${s.brand} — $${(p/100).toFixed(3)}/L (${p}¢) — ${s.address}`);
  });

  await browser.close();
})();
```

## Cloudflare Bypass Strategy

The key insight is **time-based waiting**:

- Cloudflare's managed challenge is **time-based** — it auto-resolves after a few seconds for any IP
- `navigator.webdriver=true` is **not** a blocking factor — Cloudflare passes Playwright browsers
- `--disable-blink-features=AutomationControlled` and custom UA are **not required**
- **Wait for title to include "Gas Prices"** — that signals challenge is cleared
- Typical total time: **10-20 seconds**
- Do NOT try to click through the challenge — just wait

## Critical Corrections from Experience

### Price Format is "XXX.X¢" (one decimal), NOT "XXX"
- Actual page format: `167.9¢` (means $1.679/L)
- The old regex `/^\d{3}$/` for 3-digit prices was **wrong**
- Correct approach: use `/(\d+\.\d+)\s*¢/` to match `167.9¢`

### Scrolling is Required to Load All Cards
- GasBuddy uses **lazy loading** — station cards only render as you scroll
- `scrollTo(0, document.body.scrollHeight)` once is **not enough**
- Must scroll **incrementally**: `scrollBy(0, 600)` multiple times with 400ms waits
- Without scrolling, only 1-3 stations appear; after scrolling 8+ times, 10+ stations appear

### Brand Extraction Can Be Noisy
- Brand line (`lines[0]`) may be the main brand (e.g., "Esso") but sub-brands get lost
- The station name on the page is often "Esso & Circle K" — the "Circle K" part may not appear
- Brand extraction is good enough for the primary brand; don't over-engineer it

## Practical Fallbacks

GasBuddy home search is unreliable in automation. Always use direct city URL.

### Common Canada URL patterns

- North York: `https://www.gasbuddy.com/gasprices/ontario/north-york`
- Toronto: `https://www.gasbuddy.com/gasprices/ontario/toronto`
- Markham: `https://www.gasbuddy.com/gasprices/ontario/markham`
- Richmond Hill: `https://www.gasbuddy.com/gasprices/ontario/richmond-hill`
- Scarborough: `https://www.gasbuddy.com/gasprices/ontario/scarborough`
- Vaughan: `https://www.gasbuddy.com/gasprices/ontario/vaughan`

## Data Extraction Details

**Price format:** `XXX.X¢` (one decimal, cents per liter, e.g. `167.9¢` = $1.679/L)
- Use regex `/(\d+\.\d+)\s*¢/` to extract — do NOT use integer regex

**CSS class for station cards:** `[class*="stationListItem"]`

**Lines within each card (after text split by newline):**
- Line 0: Brand name (e.g., "Esso")
- Price: matched via regex `/\d+\.\d+\s*¢/` anywhere in the text
- Address: line starting with digit followed by letters (e.g., "6000 Dufferin St")

## Filtering and Sorting

- Default is **price ascending** (cheapest first) — verify first 3 prices are non-decreasing
- Default fuel type shown: **Regular (87)**
- Open now / payment / brand filters require UI interaction — state as unavailable if requested

## Output Template

```
🔥 {City} Gas Prices (Regular 87) — {Date}
========================================
1. Brand — $X.XXX/L (XXX.X¢) — Address
2. Brand — $X.XXX/L (XXX.X¢) — Address
...
```

## Known Pitfalls

- **Don't use the OpenClaw built-in `browser` tool** — it gets blocked every time by Cloudflare
- **Don't use integer regex for price** (`/^\d{3}$/`) — prices have one decimal: `167.9¢`
- **Don't skip incremental scrolling** — lazy loading means you miss most stations without it
- **Cookie banners** are automatically handled; no need to dismiss manually
- **Location search on homepage** is unreliable — always use direct city URL
- **Price units** are cents/liter (CAD), not dollars/gallon

## Success Criteria

- Page title changes from "Just a moment..." to "Best Gas Prices & Local Gas Stations in..."
- At least 8 station cards extracted with brand, price, and address after scrolling
- Prices formatted as CAD/L (e.g., $1.679/L)
- Script completes within 60 seconds timeout
