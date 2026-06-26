---
name: ecommerce-market-analyzer
description: Scrape e-commerce homepages from multiple websites in a target market, handle popups automatically, capture screenshots and HTML, extract product data, and generate comprehensive market analysis reports. Use when asked to "analyze [market] e-commerce market", "scrape e-commerce websites", "find hot products in [country]", "analyze product trends", or "generate market report for [region]". Works with German, English, and other international markets.
---

# E-commerce Market Analyzer

Automated workflow for scraping e-commerce websites, handling popups, extracting product data, and generating comprehensive market analysis reports.

## Workflow Overview

This skill follows a 4-step workflow:

1. **Setup & Scraping** - Run Playwright scraper to capture homepages
2. **Visual Analysis** - Analyze screenshots to identify product categories
3. **Data Extraction** - Parse HTML to extract specific products and prices
4. **Report Generation** - Create comprehensive market analysis report

```
User provides website list
         ↓
Step 1: Run scraper (handles popups automatically)
         ↓
Step 2: Analyze screenshots visually
         ↓
Step 3: Extract structured data from HTML
         ↓
Step 4: Generate final report
```

---

## Step 1: Setup & Scraping

### Quick Start

When user provides a list of e-commerce websites, immediately run the scraper:

```bash
# Create output directory
mkdir -p screenshots_clean

# Run the scraper
uv run python scripts/scrape_websites.py
```

### Customizing the Website List

Edit `scripts/scrape_websites.py` and update the `WEBSITES` list:

```python
WEBSITES = [
    "amazon.de",
    "ebay.de",
    "otto.de",
    # Add more websites...
]
```

### Key Features

The scraper automatically:
- Handles cookie consent popups (German, English, universal selectors)
- Handles region/language selection dialogs
- Captures full-page screenshots (1920x1080)
- Saves HTML source code
- Uses German locale settings (or customize for other markets)
- Waits for page stabilization

**Important:** The script uses popup patterns from `references/popup_patterns.md`. Consult this file if dealing with new popup types.

### Expected Output

After running, you'll have:
- `screenshots_clean/*.png` - Full-page screenshots
- `screenshots_clean/*.html` - HTML source files
- Console output with success/failure summary

**Success rate target:** 85-95%

Common failures:
- Anti-bot protection (requires manual intervention)
- HTTP/2 protocol errors (some sites block automation)
- Timeout on slow-loading sites

---

## Step 2: Visual Analysis

### Read Screenshots

After scraping, read the screenshot files to visually identify:
- Product categories
- Featured products
- Promotional items
- Visual design patterns

Example approach:
```python
from pathlib import Path

screenshot_dir = Path("screenshots_clean")
screenshots = list(screenshot_dir.glob("*.png"))

# Read screenshots using the Read tool
for screenshot in screenshots[:5]:  # Start with 5 sites
    # Use Read tool to view image
    # Note product categories and featured items
```

### What to Look For

**Product Categories:**
- Clothing & Fashion (Bekleidung)
- Electronics (Elektronik)
- Home & Furniture (Möbel & Wohnen)
- Food & Groceries (Lebensmittel)
- Books & Media (Bücher)
- Beauty & Personal Care (Beauty & Pflege)
- Sports & Outdoor (Sport)
- Toys & Baby (Spielzeug & Baby)

**Featured Products:**
- Homepage banners
- Promotional sections
- "Deal of the day" items
- New arrivals

**Take notes** on recurring patterns across multiple sites - these indicate market trends.

---

## Step 3: Data Extraction

### Strategy Selection

Choose extraction strategy based on site structure. See `references/html_parsing_patterns.md` for complete patterns.

**Quick decision tree:**
1. Try JSON-LD schema extraction (best for structured data)
2. Fall back to data attribute extraction
3. Fall back to class-based extraction
4. Last resort: keyword matching

### Example: Extract from REWE.de

```python
import re
from pathlib import Path

html_file = Path("screenshots_clean/rewe.de.html")
content = html_file.read_text(encoding='utf-8')

# REWE-specific patterns
title_pattern = r'data-offer-title="([^"]+)"'
price_pattern = r'<div class="cor-offer-price__tag-price">([^<]+)</div>'

titles = re.findall(title_pattern, content)
prices = re.findall(price_pattern, content)

for i, title in enumerate(titles[:10]):
    price = prices[i] if i < len(prices) else "N/A"
    print(f"{title}: {price}€")
```

### Platform-Specific Parsing

Each e-commerce platform has unique HTML structure. Consult `references/html_parsing_patterns.md` for:
- Amazon.de patterns
- eBay.de patterns
- Otto.de patterns
- Zalando/AboutYou patterns
- REWE/Lidl supermarket patterns
- And more...

### Price Normalization

Always normalize prices:
```python
def normalize_price(price_str):
    """Convert German format (1.234,56€) to float"""
    price_str = price_str.replace('€', '').replace('EUR', '').strip()
    if ',' in price_str and '.' in price_str:
        price_str = price_str.replace('.', '').replace(',', '.')
    elif ',' in price_str:
        price_str = price_str.replace(',', '.')
    try:
        return float(price_str)
    except:
        return None
```

### Handling Large Files

For HTML files >25k tokens:
```bash
# Use grep to search for specific patterns
grep -o 'data-product-name="[^"]*"' amazon.de.html | head -20

# Or extract specific sections
grep -A 5 'product-title' ebay.de.html
```

### Extraction Best Practices

1. **Try multiple patterns** - Start with JSON-LD, fall back as needed
2. **Validate extractions** - Check for reasonable length (10-100 chars)
3. **Remove duplicates** - Use sets to track seen products
4. **Limit results** - Cap at 10-20 products per site
5. **Handle encoding** - Always use `encoding='utf-8'`

---

## Step 4: Report Generation

### Use the Report Template

Copy and customize `assets/report_template.md`:

```bash
cp assets/report_template.md final_report.md
```

### Report Structure

The template includes these sections:
1. **Executive Summary** - Key findings
2. **Top Product Categories** - Ranked list with percentages
3. **Verified Product Prices** - Extracted data with exact prices
4. **Platform-Specific Analysis** - Per-site breakdown
5. **Market Trends** - Growth trends and consumer behavior
6. **Seasonal Characteristics** - Current and predicted
7. **Technical Implementation** - Success metrics and limitations
8. **Business Insights** - Opportunities and recommendations
9. **Data Sources** - Success/failure breakdown
10. **Conclusions** - Actionable takeaways

### Filling the Template

Replace placeholder tokens:
- `{MARKET}` → German, UK, US, etc.
- `{NUM_SITES}` → 23, 25, etc.
- `{DATE}` → 2026-03-19
- `{SUCCESS_RATE}` → 92
- `{CATEGORY_1}` → Clothing & Fashion
- `{PERCENTAGE_1}` → 28
- And so on...

### Data Quality Indicators

Include these metrics:
- **Success rate**: % of successfully scraped sites
- **Popup handling**: # of sites with popups handled
- **Price accuracy**: % of verified prices
- **Screenshot quality**: Resolution and file size
- **HTML completeness**: Average file size

### Writing Tips

**Be bilingual** (for German market):
- Product names: German + Chinese/English translation
- Categories: "Bekleidung / Clothing"
- Maintain both languages throughout

**Be specific:**
- ❌ "Electronics are popular"
- ✅ "AirPods 4 (89,90€ on eBay), PlayStation 5, and Samsung smartphones are top electronics"

**Include evidence:**
- Reference screenshot file names
- Quote exact prices with sources
- Link specific platforms to products

---

## Troubleshooting

### Issue: Popup Not Closed

**Solution:** Check `references/popup_patterns.md` for the specific site. Add custom selector if needed:

```python
# In scripts/scrape_websites.py, add to popup_selectors list:
popup_selectors = [
    # ... existing selectors ...
    'button:has-text("Neue Popup Text")',  # Add custom
]
```

### Issue: HTML Parsing Returns Empty

**Diagnose:**
1. Check if HTML file exists and has content
2. Verify the pattern with grep: `grep -o "your-pattern" file.html`
3. Try alternative patterns from `references/html_parsing_patterns.md`
4. Use keyword matching as fallback

### Issue: Anti-Bot Detection

**Symptoms:** CAPTCHA, "Verify you are human", IP blocking

**Solutions:**
1. Add delays between requests (already in script)
2. Customize user agent string
3. Use browser fingerprinting evasion
4. For production: consider proxy rotation (not included)

### Issue: Timeout Errors

**Solution:** Adjust timeout in script:
```python
await page.goto(url, wait_until="domcontentloaded", timeout=120000)  # 2min
```

Or use more relaxed loading strategy:
```python
await page.goto(url, wait_until="load", timeout=90000)
```

---

## Market-Specific Configuration

### German Market (Default)

```python
context = await browser.new_context(
    locale="de-DE",
    timezone_id="Europe/Berlin",
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)..."
)
```

Popup patterns: See `references/popup_patterns.md` → German Market section

### UK Market

```python
context = await browser.new_context(
    locale="en-GB",
    timezone_id="Europe/London",
)
```

Popup patterns: Use English/International selectors

### US Market

```python
context = await browser.new_context(
    locale="en-US",
    timezone_id="America/New_York",
)
```

### Other Markets

Adjust `locale` and `timezone_id` accordingly. Update popup selectors in script based on language.

---

## Advanced Usage

### Parallel Scraping

For large website lists, modify script to use concurrent scraping:

```python
import asyncio

async def scrape_all(websites):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        tasks = [capture_homepage(browser, url, output_dir) for url in websites]
        results = await asyncio.gather(*tasks)
        await browser.close()
    return results
```

**Note:** Be respectful of rate limits. Use delays.

### Custom Analysis

Beyond the standard workflow, you can:
- Compare prices across platforms
- Track price changes over time (run periodically)
- Identify pricing patterns (premium vs discount)
- Analyze promotional strategies
- Monitor competitor activity

### Exporting Data

Consider exporting to structured formats:
- **CSV**: For spreadsheet analysis
- **JSON**: For programmatic access
- **Database**: For long-term tracking

Example CSV export:
```python
import csv

with open('products.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Platform', 'Product', 'Price', 'Category'])
    for product in products:
        writer.writerow([product['platform'], product['name'],
                        product['price'], product['category']])
```

---

## Best Practices

### Ethical Scraping

1. **Respect robots.txt** - Check before scraping
2. **Rate limiting** - Don't overwhelm servers (script includes delays)
3. **Terms of Service** - Review site ToS
4. **Personal use** - This skill is for market research, not commercial resale

### Data Quality

1. **Verify prices** - Cross-check suspicious values
2. **Update regularly** - E-commerce changes fast
3. **Document assumptions** - Note any manual adjustments
4. **Keep raw data** - Save screenshots and HTML for reference

### Report Quality

1. **Be objective** - Base conclusions on data
2. **Show your work** - Reference sources
3. **Contextualize** - Explain market-specific factors
4. **Actionable** - Provide specific recommendations

---

## Resources Reference

### scripts/scrape_websites.py
Main scraper with automatic popup handling. Uses Playwright to capture homepages.

**Usage:** `uv run python scripts/scrape_websites.py`

### references/popup_patterns.md
Comprehensive collection of popup selectors for different markets and platforms.

**When to read:** When encountering new popup types or troubleshooting popup handling.

### references/html_parsing_patterns.md
Platform-specific HTML parsing patterns and extraction strategies.

**When to read:** When extracting product data from HTML files. Contains patterns for Amazon, eBay, REWE, Otto, Zalando, and generic strategies.

### assets/report_template.md
Structured template for the final market analysis report.

**Usage:** Copy and fill in with analysis results.
