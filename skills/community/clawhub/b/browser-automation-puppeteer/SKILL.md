---
name: browser-automation
description: Web scraping and browser automation using Puppeteer. Use when the user wants to extract data from websites, crawl pages, scrape dynamic content rendered by JavaScript, take screenshots, fill forms, or automate browser workflows. Triggers include "scrape", "crawl", "extract data from", "web harvest", "take screenshot of", or any request involving Puppeteer or headless browser automation.
---

# Browser Automation

Web scraping and browser automation powered by Puppeteer.

## When to Use

✅ **USE this skill when:**

- "Scrape data from [URL]"
- "Extract all [products/listings/items] from [website]"
- "Take a screenshot of [page]"
- "Crawl [website] and collect [info]"
- "Fill and submit [form]"
- Any JavaScript-rendered content that won't load without a browser

❌ **DON'T use this skill when:**

- Simple static pages → use `web_fetch` instead
- APIs available → fetch API directly
- Rate-limited sites → respect robots.txt

## Quick Start

```bash
# Install Puppeteer
npm install puppeteer

# Basic scraping
node scripts/scrape.js https://example.com
```

## Core Patterns

### Launch Browser

```javascript
const puppeteer = require('puppeteer');

async function scrape(url) {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const page = await browser.newPage();
  await page.goto(url, { waitUntil: 'networkidle2' });
  
  // ... extract data ...
  
  await browser.close();
}
```

### Extract Text Content

```javascript
// Get all text from a selector
const titles = await page.$$eval('h2', els => els.map(el => el.textContent.trim()));

// Get text from single element
const price = await page.$eval('.price', el => el.textContent.trim());
```

### Extract HTML

```javascript
const html = await page.$eval('.product-list', el => el.innerHTML);
```

### Extract Attributes

```javascript
const links = await page.$$eval('a', els => els.map(el => ({
  text: el.textContent.trim(),
  href: el.getAttribute('href')
})));
```

### Wait for Content

```javascript
// Wait for selector
await page.waitForSelector('.results', { timeout: 10000 });

// Wait for network idle
await page.goto(url, { waitUntil: 'networkidle2' });

// Wait for function
await page.waitForFunction(() => document.querySelectorAll('.item').length > 10);
```

### Pagination

```javascript
async function scrapeWithPagination(baseUrl, maxPages = 5) {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  
  let results = [];
  
  for (let i = 1; i <= maxPages; i++) {
    const url = `${baseUrl}?page=${i}`;
    await page.goto(url, { waitUntil: 'networkidle2' });
    
    const items = await page.$$eval('.item', els => 
      els.map(el => el.textContent.trim())
    );
    
    if (items.length === 0) break;
    results.push(...items);
  }
  
  await browser.close();
  return results;
}
```

### Screenshots

```javascript
// Full page screenshot
await page.screenshot({ path: 'screenshot.png', fullPage: true });

// Element screenshot
const element = await page.$('.chart');
await element.screenshot({ path: 'chart.png' });
```

### Block Resources (Speed Up)

```javascript
await page.setRequestInterception(true);
page.on('request', req => {
  if (['image', 'stylesheet', 'font'].includes(req.resourceType())) {
    req.abort();
  } else {
    req.continue();
  }
});
```

## Scripts

### scrape.js — Basic Scraping

```javascript
// Usage: node scripts/scrape.js <url> [selector]
const puppeteer = require('puppeteer');

const url = process.argv[2];
const selector = process.argv[3] || 'body';

if (!url) {
  console.error('Usage: node scrape.js <url> [selector]');
  process.exit(1);
}

(async () => {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  
  await page.goto(url, { waitUntil: 'networkidle2' });
  
  const content = await page.$$eval(selector, els => 
    els.map(el => el.textContent.trim())
  );
  
  console.log(JSON.stringify(content, null, 2));
  
  await browser.close();
})();
```

### screenshot.js — Page Screenshots

```javascript
// Usage: node scripts/screenshot.js <url> [output.png]
const puppeteer = require('puppeteer');

const url = process.argv[2];
const output = process.argv[3] || 'screenshot.png';

if (!url) {
  console.error('Usage: node screenshot.js <url> [output.png]');
  process.exit(1);
}

(async () => {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  
  await page.goto(url, { waitUntil: 'networkidle2' });
  await page.screenshot({ path: output, fullPage: true });
  
  console.log(`Screenshot saved to ${output}`);
  await browser.close();
})();
```

### crawl.js — Multi-Page Crawler

```javascript
// Usage: node crawl.js <url> <selector> [maxPages]
const puppeteer = require('puppeteer');

const url = process.argv[2];
const selector = process.argv[3];
const maxPages = parseInt(process.argv[4]) || 10;

if (!url || !selector) {
  console.error('Usage: node crawl.js <url> <selector> [maxPages]');
  process.exit(1);
}

(async () => {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  
  let allData = [];
  
  for (let i = 1; i <= maxPages; i++) {
    const pageUrl = url.includes('?') ? `${url}&page=${i}` : `${url}?page=${i}`;
    console.error(`Crawling: ${pageUrl}`);
    
    await page.goto(pageUrl, { waitUntil: 'networkidle2' });
    
    const data = await page.$$eval(selector, els => 
      els.map(el => el.textContent.trim())
    );
    
    if (data.length === 0) break;
    allData.push(...data);
  }
  
  console.log(JSON.stringify(allData, null, 2));
  await browser.close();
})();
```

## Common Selectors

| Target | Selector |
|--------|----------|
| All links | `a` |
| All images | `img` |
| Headings | `h1`, `h2`, `h3` |
| Lists | `ul li`, `ol li` |
| Tables | `table tr` |
| Cards/Items | `.item`, `.card`, `.product` |
| Prices | `.price`, `[class*="price"]` |
| Descriptions | `.description`, `.summary` |

## Tips

- **Check robots.txt** before scraping: `curl example.com/robots.txt`
- **Add delays** between requests to avoid bans: `await new Promise(r => setTimeout(r, 2000))`
- **Use `networkidle2`** for SPAs (Single Page Apps)
- **Debug with screenshots** when selectors fail
- **Set user agent** for sites that block bots:
  ```javascript
  await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36');
  ```

## Reference

For detailed Puppeteer API, see [puppeteer/docs/api.md](references/puppeteer-api.md).