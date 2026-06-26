---
name: auto-scraping-to-csv
description: |
  Scrape any webpage using text-based DOM manipulation and export structured data to CSV.
  The agent handles complex page nuances — infinite scroll, pagination, popups, lazy loading —
  and asks clarifying questions when data is ambiguous. No external LLM needed.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - node
    install:
      - kind: node
        package: playwright
        bins: [playwright]
    homepage: https://github.com/Science-Prof-Robot/autoclick
    emoji: "🧹"
---

# Auto Scraping to CSV — Agent-Driven Web Scraping

Scrape any webpage using text-based DOM manipulation and export structured data to CSV. The agent handles complex page nuances — infinite scroll, pagination, popups, lazy loading — and asks clarifying questions when data is ambiguous. No external LLM required.

## Philosophy: Let the Agent Figure It Out

Traditional scraping requires you to inspect HTML, write CSS selectors, handle edge cases, and debug when the site changes. This skill flips that:

**You say what you want. The agent handles the how.**

```
You: "Scrape product catalog"
Agent: "I see 50 products across 5 pages with infinite scroll. 
        I also see 'Price', 'Sale Price', and 'Member Price' columns.
        Which price field should I extract?"
You: "Sale Price"
Agent: [handles scrolling, pagination, extracts 50 rows] → products.csv
```

The agent will:
1. **Explore** the page structure via text-based DOM
2. **Detect complexity** — scroll, pagination, tabs, filters
3. **Ask questions** when ambiguous (multiple price fields, missing data, format choices)
4. **Handle edge cases** — dismiss popups, wait for lazy loading, retry on errors
5. **Export CSV** — clean, structured, ready to use

## When to Use

- **Product catalogs**: "Scrape all laptops with prices and ratings"
- **News/articles**: "Get latest blog posts with titles, dates, authors"
- **Directory listings**: "Extract all company names, emails, and websites"
- **Table data**: "Get the pricing table from this SaaS page"
- **Real estate**: "Scrape listings with price, beds, baths, square footage"
- **Job boards**: "Get job titles, companies, locations, and salary ranges"
- **Social feeds**: "Extract posts with engagement counts (likes, comments, shares)"
- **Research data**: "Get citation counts, authors, publication dates from this index"

## How It Works

```
Claude (Host Model)
    ↕  HTTP
Bridge Server (Node.js + Playwright)
    ↕  page.evaluate()
Browser (Chromium) ← Page-Agent injected
```

1. **Bridge** launches a local Chromium browser via Playwright
2. **Page-Agent** is injected as an IIFE script from CDN into the target page
3. **Page-Agent** indexes the DOM and generates a simplified text representation:
   ```
   [5]<a >Widget Pro Laptop /></a>
   [12]<div >$1,299.99 /></div>
   [18]<div >4.5 stars (128 reviews) /></div>
   ```
4. **Claude** receives the text state, understands the page structure, decides actions
5. **Agent asks questions** when data is ambiguous or complex
6. **Loop** continues until all data is extracted or user says stop
7. **CSV export** converts structured JSON to CSV

---

## First-Time Setup

### 1. Install Playwright

```bash
npm install -D playwright
npx playwright install chromium
```

### 2. Place the Bridge Script

```bash
# Copy from this skill folder to your agents directory
cp .claude/skills/auto-scraping-to-csv/page-agent-bridge.mjs .claude/agents/
```

### 3. Start the Bridge

```bash
node .claude/agents/page-agent-bridge.mjs
```

Default port: **9876**.

### 4. Verify Health

```bash
curl http://localhost:9876/health
```

---

## Agent-Driven Scraping Workflow

### Step 1: Request What You Want

```
/scrape-to-csv https://example.com/products
  "Extract all products with name, price, rating, and number of reviews"
```

### Step 2: Agent Explores and Asks Questions

The agent will fetch the DOM state and may ask:

```
Agent: "I found 24 products on the current page. The site has infinite scroll 
        and I can see more products loading as I scroll. 
        How many products do you want total? (type 'all' for everything)"
You: "50"

Agent: "I see three price fields:
        - Original Price: $1,299
        - Sale Price: $999
        - Member Price: $899
        Which one should I extract?"
You: "Sale Price"

Agent: "Some products are out of stock and show 'N/A' for price.
        Should I:
        A) Include them with 'N/A'
        B) Skip those rows
        C) Mark as 'Out of Stock' in a separate column"
You: "C"
```

### Step 3: Agent Handles Complexity

The agent automatically:
- Scrolls to load more content
- Clicks pagination buttons
- Waits for lazy-loaded images/data
- Dismisses cookie banners and popups
- Retries if elements are slow to appear
- Stops gracefully if the site blocks scraping

### Step 4: Preview and Confirm

```
Agent: "Extracted 50 products. Here's a preview:

| name | price | rating | reviews | stock_status |
|------|-------|--------|---------|-------------|
| Widget Pro | $999 | 4.5 | 128 | In Stock |
| Gadget Mini | $499 | 4.2 | 89 | In Stock |
| ... | ... | ... | ... | ... |

Save as 'products.csv'? (yes/no/change columns)"
You: "yes"
```

### Step 5: CSV Delivered

```
Agent: "Saved to ./products.csv — 50 rows, 5 columns"
```

---

## Handling Complex Scenarios

### Infinite Scroll

```
You: "Scrape all posts from this feed"
Agent: "The page loads 10 posts at a time via infinite scroll.
        I've scrolled 3 times and found 30 posts so far.
        Should I continue scrolling? (yes/no/scroll N more times)"
You: "scroll 5 more times"
Agent: [scrolls] → "Found 80 total posts. Saved to feed.csv"
```

### Pagination

```
You: "Get all products from this catalog"
Agent: "I see pagination: Page 1 of 12. 
        I can scrape all 12 pages (may take 2-3 minutes) or a subset.
        How many pages?"
You: "all"
Agent: [clicks through 12 pages] → "360 products saved to catalog.csv"
```

### Login Required

```
You: "Scrape my order history"
Agent: "The page redirects to a login screen. 
        I need credentials to proceed.
        Please provide:
        - Username/email
        - Password
        Or type 'skip' to abort."
You: "skip"
Agent: "Aborted. No data extracted."
```

### Multiple Data Formats

```
You: "Get prices from this page"
Agent: "I found prices in multiple formats:
        - '$19.99' (US format)
        - '€17.99' (EU format)
        - '¥2,980' (JP format)
        Which format should I standardize to?"
You: "Keep as-is, add a 'currency' column"
Agent: [extracts with currency detection] → prices.csv
```

### Missing / Inconsistent Data

```
You: "Extract employee data from this directory"
Agent: "I see 100 employee cards. Some are missing:
        - 12 missing phone numbers
        - 8 missing job titles
        - 3 missing photos
        How should I handle missing fields?
        A) Leave blank
        B) Fill with 'N/A'
        C) Skip those rows entirely"
You: "B"
Agent: [extracts 100 rows with 'N/A' for missing fields] → employees.csv
```

---

## Natural Language Commands

### `/scrape-to-csv <url> <description>`

General scraping with CSV export.

```
/scrape-to-csv https://news.ycombinator.com
  "Get top 30 stories with title, URL, points, and comment counts"

/scrape-to-csv https://www.anthropic.com/news
  "Latest blog posts: title, date, category, URL"

/scrape-to-csv https://example.com/realestate
  "Listings: address, price, beds, baths, sqft, listing agent"
```

### `/scrape-table <url> <selector_or_description>`

Extract a specific table.

```
/scrape-table https://example.com/pricing
  "The comparison table with Basic/Pro/Enterprise columns"

/scrape-table https://example.com/sales
  "Q4 2024 revenue breakdown table"
```

### `/scrape-news <url>`

Optimized for news/blog scraping.

```
/scrape-news https://techcrunch.com
  "Latest 20 articles: title, author, date, excerpt, URL"

/scrape-news https://blog.openai.com
  "All posts from 2024: title, date, tags, URL"
```

### `/scrape-products <url>`

Optimized for e-commerce.

```
/scrape-products https://amazon.com/s?k=laptops
  "Laptops: name, brand, price, rating, prime eligible, URL"

/scrape-products https://shopify-store.com/collections/all
  "All products: name, price, compare-at price, availability"
```

---

## Output Format

The agent produces a structured markdown report:

```markdown
## Scraping Report — example.com/products
**Session:** a1b2c3d4 | **Duration:** 2m 14s | **Rows:** 50

### Task
Extract all products with name, price, rating, and number of reviews

### Agent Decisions
- **Pagination**: Detected infinite scroll, scrolled 5 times
- **Price field**: Chose "Sale Price" per user request
- **Missing data**: Filled out-of-stock prices with "N/A" per user request
- **Columns**: name, sale_price, rating, review_count, stock_status

### Sample Data

| name | sale_price | rating | review_count | stock_status |
|------|-----------|--------|-------------|-------------|
| Widget Pro | $999 | 4.5 | 128 | In Stock |
| Gadget Mini | $499 | 4.2 | 89 | In Stock |
| Super Gizmo | $1,299 | 4.8 | 256 | Out of Stock |

### File
`./products.csv` — 50 rows, 5 columns
```

---

## CSV Conversion Options

### Option A — Python (recommended)

```python
import json, csv, re

# Bridge returns: "✅ Executed JavaScript. Result: [{...}, {...}]"
msg = """PASTE_BRIDGE_RESPONSE_HERE"""
match = re.search(r'Result: (\[.*\])', msg)
if match:
    data = json.loads(match.group(1))
    with open('output.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"Wrote {len(data)} rows to output.csv")
```

### Option B — Node.js

```javascript
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('data.json', 'utf8'));
const headers = Object.keys(data[0]);
const csv = [
  headers.join(','),
  ...data.map(row => headers.map(h => `"${(row[h]||'').replace(/"/g,'""')}"`).join(','))
].join('\n');
fs.writeFileSync('output.csv', csv);
```

---

## Troubleshooting

### Bridge won't start

```
Error: Cannot find module 'playwright'
```
**Fix:** `npm install -D playwright && npx playwright install chromium`

### Site blocks scraping

**Agent detects:** "The site returned 403 Forbidden. This may be bot protection."
**Options:**
- Try `headless: false` (looks more like a real user)
- Add delays between requests
- Use a different user agent

### Page loads but no data found

**Agent detects:** "The page loaded but I see mostly navigation elements. Content may be behind a login or loaded dynamically."
**Agent asks:** "Should I wait longer, scroll down, or do you have login credentials?"

### Data looks wrong

**Agent detects:** "Prices show as 'NaN' or empty. The site may use JavaScript to render prices."
**Agent asks:** "Should I try executing JavaScript to extract the real values, or skip this field?"

---

## Comparison with Other Tools

| Tool | Setup | Selectors | Complex Pages | Agent Questions | Best For |
|------|-------|-----------|---------------|-----------------|----------|
| **Auto Scraping to CSV** | npm install | None needed | Handles automatically | Yes, clarifies ambiguity | One-off extraction, exploratory scraping |
| BeautifulSoup | pip install | Required | Manual handling | No | Known structure, repeated scraping |
| Scrapy | Project setup | Required | Middleware needed | No | Large-scale crawling, pipelines |
| Playwright E2E | npm install | Required | Manual handling | No | Testing, automation |
| Browser-Use | API key | None | Partial | Limited | Multi-page research |

**Use this skill when:**
- You want to scrape without writing selectors
- The page structure is complex or unknown
- You need the agent to handle edge cases (scroll, popups, pagination)
- You want clarifying questions when data is ambiguous
- You need quick one-off extraction to CSV

---

## Bridge API Reference

### `POST /sessions`
Launch a new browser session.

**Body:**
```json
{ "url": "https://example.com", "headless": false }
```

**Response:** `{ "id": "abc123", "url": "https://example.com" }`

### `GET /sessions/:id/state`
Get text-based DOM state.

**Response:** `{ url, title, header, content, footer }`

### `POST /sessions/:id/act`
Execute an action.

**Body:**
```json
{ "action": "executeJavascript", "params": { "script": "return document.title;" } }
```

### `DELETE /sessions/:id`
Close session.

### `POST /shutdown`
Stop bridge.

---

*Skill: auto-scraping-to-csv v1.0.0 | Bridge: page-agent-bridge.mjs | Powered by Alibaba Page-Agent + Playwright*
