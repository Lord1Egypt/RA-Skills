# Customer Research & Validation

Pre-launch validation framework for product ideas using social listening and competitive intelligence.

## Description

Customer Research & Validation ensures marketing strategy is built on real customer signals, not assumptions. It provides tools for mining Reddit/forums for pain points, analyzing competitor positioning, validating personas against real-world data, and conducting pricing research. Designed for the "measure twice, cut once" principle—validate product-market fit before spending on ads or content.

## Key Features

- **Reddit/forum mining** - Extract customer pain points, feature requests, complaints from discussions
- **Sentiment analysis** - Understand emotional tone around product categories
- **Competitor intelligence** - Analyze positioning, pricing, and customer perception
- **Persona validation** - Test assumptions against real community discussions
- **Pricing research** - Gauge willingness-to-pay from organic conversations
- **Theme extraction** - Identify common problems and unmet needs
- **No paid databases** - Uses free public forums and web scraping

## Quick Start

### Bash Scripts (Zero Dependencies)
```bash
# Mine Reddit for customer insights
./scripts/reddit-miner.sh \
  --subreddit "financialindependence" \
  --query "retirement calculator" \
  --limit 50

# Validate persona against research data
./scripts/persona-validator.sh \
  --persona-file examples/fire-enthusiast-persona.json

# Generate customer interview script
./scripts/interview-generator.sh \
  --persona "FIRE enthusiast, 35, tech worker" \
  --problem "retirement calculators too conservative"

# Scrape competitor reviews
./scripts/competitor-scraper.sh \
  --product "Personal Capital" \
  --sources "reddit"
```

### Python Scripts (Alternative)
```bash
# Install dependencies
pip install praw requests beautifulsoup4

# Mine Reddit for customer insights
python3 scripts/reddit-miner.py \
  --category "tax software" \
  --subreddits personalfinance,tax,fatFIRE \
  --limit 200 \
  --time-filter month \
  --output insights.json

# Analyze competitor mentions
python3 scripts/competitor-scraper.py \
  --competitors "TurboTax,H&R Block" \
  --subreddits personalfinance,tax \
  --output competitor_report.json
```

**Output includes:**
- Most common pain points (ranked by frequency)
- Sentiment breakdown (positive/neutral/negative)
- Feature requests and wish-list items
- Pricing sensitivity analysis
- Competitor strengths/weaknesses

## Use When

- ✅ Validating a new product idea before building
- ✅ Understanding competitor positioning
- ✅ Identifying unmet customer needs
- ✅ Pricing research and willingness-to-pay analysis
- ✅ Persona validation against real-world data
- ✅ Pre-campaign market research

## What It Does NOT Do

- Does NOT conduct primary research (surveys, interviews)
- Does NOT access paid market research databases
- Does NOT work well for B2B enterprise validation (requires direct sales conversations)
- Does NOT handle regulated industries requiring compliance (healthcare, legal, etc.)
- Does NOT provide statistically significant sample sizes (directional insights only)

## Requirements

### Bash Scripts
- curl (standard on macOS/Linux)
- jq (JSON processing)
- No API keys needed (uses Reddit public JSON)

### Python Scripts (Optional)
- Python 3.8+
- praw (Reddit API wrapper)
- requests, beautifulsoup4 (web scraping)
- Reddit API credentials (free, create at reddit.com/prefs/apps)

## License

MIT
