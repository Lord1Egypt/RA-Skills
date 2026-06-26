# Browser Automation

Web scraping and browser automation skill using Puppeteer for AI assistants.

## Install

```bash
npm install puppeteer
```

## Scripts

### scrape.js — Extract text from a web page

```bash
node scripts/scrape.js <url> [selector]
```

**Examples:**

```bash
# Scrape all headings
node scripts/scrape.js https://news.ycombinator.com h2

# Scrape with default selector (body)
node scripts/scrape.js https://example.com

# Scrape specific elements
node scripts/scrape.js https://shop.example.com .product-item
```

**Output:** JSON array of extracted content

---

### screenshot.js — Capture screenshots

```bash
node scripts/screenshot.js <url> [output.png] [--full]
```

**Examples:**

```bash
# Basic screenshot (viewport only)
node scripts/screenshot.js https://example.com

# Full page screenshot
node scripts/screenshot.js https://example.com full.png --full

# Custom output path
node scripts/screenshot.js https://example.com ./screenshots/page.png
```

**Options:**

- `output.png` — Output file path (default: screenshot.png)
- `--full` — Capture entire scrollable page

---

### crawl.js — Multi-page crawler

```bash
node scripts/crawl.js <url> <selector> [maxPages]
```

**Examples:**

```bash
# Crawl 5 pages of products
node scripts/crawl.js https://shop.example.com/products .product-item 5

# Crawl Hacker News
node scripts/crawl.js https://news.ycombinator.com .athing 3

# Default max pages is 10
node scripts/crawl.js https://example.com/blog .post-title
```

**Output:** JSON array of all extracted items across pages

---

## Node.js API

Use the skill's patterns directly in your own scripts:

```javascript
const puppeteer = require('puppeteer');

async function scrape(url, selector) {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const page = await browser.newPage();
  await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36');
  
  await page.goto(url, { waitUntil: 'networkidle2' });
  
  const results = await page.$$eval(selector, els => 
    els.map(el => el.textContent.trim())
  );
  
  await browser.close();
  return results;
}

scrape('https://example.com', 'h1').then(console.log);
```

---

## Tips

- **Check robots.txt** before scraping: `curl example.com/robots.txt`
- **Add delays** between requests to avoid getting blocked
- **Use screenshots** to debug when selectors don't match
- **Set viewport** before taking screenshots: `await page.setViewport({ width: 1280, height: 800 })`

## Requirements

- Node.js 18+
- npm
- Puppeteer (installed via `npm install puppeteer`)

## License

MIT