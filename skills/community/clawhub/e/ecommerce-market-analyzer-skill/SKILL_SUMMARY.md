# E-commerce Market Analyzer Skill - Summary

## 📦 Skill Package Created

**File:** `ecommerce-market-analyzer.skill`
**Location:** `/Users/anpuqiang/Documents/code/gitlab/scraper/ecommerce-market-analyzer.skill`

---

## 🎯 What This Skill Does

Automated workflow for analyzing e-commerce markets by:
1. Scraping multiple e-commerce homepages using Playwright
2. Automatically handling popups (cookie consent, region selectors)
3. Capturing full-page screenshots and HTML source
4. Extracting product data from HTML
5. Generating comprehensive bilingual market analysis reports

---

## 🚀 How to Use the Skill

### Installation

```bash
# In Claude Code, use the skill installer
# Or manually install to: ~/.claude/skills/
```

### Triggering the Skill

The skill automatically activates when you ask:
- "Analyze German e-commerce market"
- "Scrape e-commerce websites for [country]"
- "Find hot products in [market]"
- "Generate market report for [region]"
- "Analyze product trends in [country]"

### Quick Start Example

```
User: "Analyze the UK e-commerce market with these sites:
       amazon.co.uk, ebay.co.uk, tesco.com, argos.co.uk"

Skill will guide through:
1. Running the scraper
2. Analyzing screenshots
3. Extracting product data
4. Generating report
```

---

## 📂 Skill Contents

### Scripts (`scripts/`)
- **scrape_websites.py** - Main Playwright scraper
  - Handles popups automatically
  - Captures screenshots + HTML
  - Configurable for different markets

### References (`references/`)
- **popup_patterns.md** - Popup selector library
  - German market patterns
  - English/International patterns
  - Platform-specific selectors

- **html_parsing_patterns.md** - HTML extraction patterns
  - JSON-LD schema extraction
  - Platform-specific patterns (Amazon, eBay, REWE, Otto, etc.)
  - Price normalization utilities
  - Fallback strategies

### Assets (`assets/`)
- **report_template.md** - Structured report template
  - Executive summary
  - Product categories
  - Platform analysis
  - Market trends
  - Business insights

---

## 🔧 Key Features

### Popup Handling
✅ Cookie consent (German, English, Universal)
✅ Region/language selectors
✅ Newsletter dismissals
✅ Multi-round detection (delayed popups)

### Market Support
✅ German market (de-DE)
✅ UK market (en-GB)
✅ US market (en-US)
✅ Customizable for other regions

### Data Extraction
✅ Visual analysis from screenshots
✅ Structured HTML parsing
✅ Price extraction & normalization
✅ Category identification
✅ Platform-specific patterns

### Report Generation
✅ Bilingual output (e.g., German + English/Chinese)
✅ Verified pricing data
✅ Market trend analysis
✅ Technical metrics
✅ Business recommendations

---

## 📊 Real-World Example (From This Project)

### Input
25 German e-commerce websites

### Process
1. **Scraping:** 23/25 success (92%)
2. **Popup handling:** 12 sites cleaned
3. **Data extraction:** REWE products with exact prices
4. **Report:** 13 categories, 50+ products identified

### Output
- 23 clean screenshots
- 23 HTML files
- Comprehensive 600+ line analysis report
- Verified prices (e.g., Nutella Biscuits 2,69€)

---

## 🎓 What This Skill Teaches Claude

When activated, this skill gives Claude:

1. **Procedural knowledge** - Step-by-step e-commerce scraping workflow
2. **Domain expertise** - E-commerce HTML structures, popup patterns
3. **Tool integration** - Playwright automation, regex extraction
4. **Best practices** - Ethical scraping, rate limiting, data validation
5. **Reusable assets** - Pre-built scripts, pattern libraries, templates

---

## 💡 Use Cases

### Market Research
- Identify trending products in target markets
- Compare pricing strategies across platforms
- Analyze seasonal trends
- Monitor competitor offerings

### Business Intelligence
- Track market leaders' product mix
- Discover pricing patterns
- Identify market gaps
- Generate competitive insights

### E-commerce Strategy
- Benchmark against competitors
- Optimize product categories
- Price positioning analysis
- Market entry research

---

## 🔄 Workflow

```
┌─────────────────────────┐
│ User provides website   │
│ list + target market    │
└───────────┬─────────────┘
            ↓
┌─────────────────────────┐
│ Step 1: Run scraper     │
│ - Playwright automation │
│ - Auto popup handling   │
│ - Screenshot + HTML     │
└───────────┬─────────────┘
            ↓
┌─────────────────────────┐
│ Step 2: Visual analysis │
│ - Read screenshots      │
│ - Identify categories   │
│ - Note featured items   │
└───────────┬─────────────┘
            ↓
┌─────────────────────────┐
│ Step 3: Data extraction │
│ - Parse HTML files      │
│ - Extract products      │
│ - Normalize prices      │
└───────────┬─────────────┘
            ↓
┌─────────────────────────┐
│ Step 4: Generate report │
│ - Use template          │
│ - Fill with data        │
│ - Add insights          │
└─────────────────────────┘
```

---

## 🛠️ Technical Requirements

- Python 3.12+
- Playwright 1.58+
- uv (for virtual environment)
- 2GB+ free disk space (for screenshots/HTML)

---

## ⚙️ Customization Options

### Different Markets
```python
# UK Market
locale="en-GB"
timezone_id="Europe/London"

# US Market
locale="en-US"
timezone_id="America/New_York"
```

### Custom Popup Selectors
Add to `references/popup_patterns.md` or directly in script

### Platform-Specific Patterns
Add to `references/html_parsing_patterns.md` for new platforms

### Report Structure
Customize `assets/report_template.md` for specific needs

---

## 📈 Expected Success Rate

- **Scraping:** 85-95% (varies by anti-bot measures)
- **Popup handling:** 90-100% (for known patterns)
- **Data extraction:** 70-90% (depends on HTML structure)
- **Overall workflow:** High confidence end-to-end

---

## 🎯 Best Practices (Included in Skill)

1. **Ethical scraping** - Rate limiting, robots.txt respect
2. **Data validation** - Cross-check extracted prices
3. **Error handling** - Graceful failures, detailed logging
4. **Documentation** - Reference sources in reports
5. **Market sensitivity** - Localization, cultural context

---

## 📝 Files Generated in This Project

From using this workflow:

```
scraper/
├── screenshots_clean/               # 23 clean screenshots
│   ├── amazon.de.png
│   ├── ebay.de.png
│   └── ...
├── screenshots_clean/*.html         # 23 HTML files
├── scrape_with_popup_handling.py    # Main script (now in skill)
├── 弹窗处理报告.md                   # Popup handling report
├── 德国热门商品分析.md               # Initial analysis
├── 德国热门商品详细分析_2026.md      # Detailed analysis
├── 德国热门商品综合分析报告_2026.md  # Final comprehensive report
└── ecommerce-market-analyzer.skill  # Packaged skill ✨
```

---

## 🚀 Next Steps

### To Use This Skill

1. **Install:** Place `ecommerce-market-analyzer.skill` in Claude's skill directory
2. **Test:** Ask "Analyze the French e-commerce market"
3. **Customize:** Modify website lists, markets, patterns as needed
4. **Iterate:** Improve based on real usage (add new platforms, patterns)

### To Share

The `.skill` file is a portable package containing:
- All scripts
- All reference documentation
- All templates
- Complete workflow instructions

Simply share the file with other Claude Code users.

---

## 🎉 Achievement Unlocked

You've successfully:
✅ Scraped 23 German e-commerce websites
✅ Handled 12 different popup types
✅ Extracted verified product prices
✅ Generated a 600+ line market analysis report
✅ **Created a reusable skill** for future e-commerce analysis

This skill encapsulates all the knowledge and tools from this project, making it instantly reusable for any market!

---

**Created:** 2026-03-19
**Version:** 1.0
**Based on:** German e-commerce market analysis project
**Skill Package:** `ecommerce-market-analyzer.skill`
