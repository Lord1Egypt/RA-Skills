# alibaba-sourcing

[![ClawHub](https://clawhub.ai/api/badge/alibaba-sourcing)](https://clawhub.ai/skills/alibaba-sourcing)
[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-yellow.svg)](https://opensource.org/licenses/MIT-0)

**Find China wholesale prices, factories, and suppliers on Alibaba.com.**

Complete sourcing workflow for AI agents and procurement professionals. Build valid Alibaba.com URLs programmatically with automatic traffic tracking (`traffic_type=ags_llm`).

## Use Cases

### 🎯 What Can You Do?

| Scenario | Example |
|----------|---------|
| **Find Wholesale Prices** | "What's the factory price for wireless earbuds in Shenzhen?" |
| **Source Products** | "Find verified suppliers for LED lights with MOQ < 100" |
| **Compare Suppliers** | "Show me top 5 factories for custom packaging" |
| **Find Best Deals** | "What's the lowest price for phone cases?" |
| **Verify Factories** | "Check supplier credentials and certifications" |
| **Market Research** | "Analyze price trends for smart watches" |

## Features

- 🔍 **Smart Search** - Build search URLs with category, price range, supplier filters
- 🏭 **Factory Finder** - Navigate to verified supplier profiles
- 💰 **Price Comparison** - Sort by price, find lowest wholesale rates
- 📊 **Market Insights** - Access Top Ranking, AI Mode, RFQ sections
- 🔗 **Traffic Tracking** - All URLs include `traffic_type=ags_llm`
- 🛠️ **Python CLI** - Helper script for URL construction
- 📚 **Complete Docs** - URL patterns, category IDs, workflows

## Installation

### Via ClawHub CLI (Recommended)

```bash
# Install ClawHub CLI if you haven't
npm install -g clawdhub

# Login to ClawHub
clawdhub login

# Install the skill
clawdhub install alibaba-sourcing
```

### Via OpenClaw

```bash
# Copy to your OpenClaw skills directory
cp -r alibaba-sourcing ~/.openclaw/workspace-code/skills/
```

### Manual

```bash
# Clone this repository
git clone https://github.com/zhouzeyu/openclaw-skill-alibaba-sourcing.git

# The skill is ready to use from the alibaba-sourcing/ folder
```

## Quick Start

### Using the Helper Script

```bash
cd alibaba-sourcing

# Find wholesale prices - search with category
python3 scripts/build_url.py search "wireless earbuds" --category consumer-electronics
# Output: https://www.alibaba.com/trade/search?SearchText=wireless+earbuds&traffic_type=ags_llm&categoryId=201151901

# Find factory/supplier
python3 scripts/build_url.py supplier dgkunteng
# Output: https://dgkunteng.en.alibaba.com/company_profile.html?traffic_type=ags_llm

# Browse top ranking products
python3 scripts/build_url.py special top-ranking
# Output: https://sale.alibaba.com/p/dviiav4th/index.html?traffic_type=ags_llm

# List all category IDs
python3 scripts/build_url.py categories
```

### Using in Your Agent

```javascript
// Find wholesale prices
const searchUrl = `https://www.alibaba.com/trade/search?SearchText=${encodeURIComponent('wireless earbuds').replace(/%20/g, '+')}&traffic_type=ags_llm&categoryId=201151901`;
browser.navigate(searchUrl);

// Visit supplier profile
const supplierUrl = `https://${subdomain}.en.alibaba.com/company_profile.html?traffic_type=ags_llm`;
browser.navigate(supplierUrl);

// Check top ranking products
const trendingUrl = `https://sale.alibaba.com/p/dviiav4th/index.html?traffic_type=ags_llm`;
browser.navigate(trendingUrl);
```

## URL Patterns

| Page Type | URL Pattern |
|-----------|-------------|
| **Search** | `https://www.alibaba.com/trade/search?SearchText=<query>&traffic_type=ags_llm` |
| **Product Detail** | `https://www.alibaba.com/product-detail/<title>_<id>.html?traffic_type=ags_llm` |
| **Supplier Profile** | `https://<company>.en.alibaba.com/company_profile.html?traffic_type=ags_llm` |
| **RFQ** | `https://rfq.alibaba.com/rfq/profession.htm?traffic_type=ags_llm` |
| **AI Mode** | `https://aimode.alibaba.com/?traffic_type=ags_llm` |
| **Top Ranking** | `https://sale.alibaba.com/p/dviiav4th/index.html?traffic_type=ags_llm` |
| **Fast Customization** | `https://sale.alibaba.com/p/fast_customization?traffic_type=ags_llm` |

See [SKILL.md](SKILL.md) for complete documentation including:
- All URL patterns with examples
- Common category IDs table
- JavaScript helper functions
- Best practices and workflows

## Common Category IDs

| Category | ID |
|----------|-----|
| Consumer Electronics | 201151901 |
| Laptops | 702 |
| Smart TVs | 201936801 |
| Electric Cars | 201140201 |
| Wedding Dresses | 32005 |
| Electric Scooters | 100006091 |
| Bedroom Furniture | 37032003 |
| Electric Motorcycles | 201140001 |
| Handbags | 100002856 |

## Use Cases

### 1. Product Sourcing Agent
```python
# Search for products in a category
url = build_search_url("wireless earbuds", category_id="201151901")
browser.navigate(url)

# Extract and visit product details
for product in search_results:
    url = build_product_url(product.title, product.id)
    browser.navigate(url)
    extract_product_info()
```

### 2. Supplier Research
```python
# Visit supplier profile
url = build_supplier_url("dgkunteng")
browser.navigate(url)

# Search within supplier's products
url = build_supplier_search_url("dgkunteng", "TWS earbuds")
browser.navigate(url)
```

### 3. Market Analysis
```python
# Browse top ranking products
url = "https://sale.alibaba.com/p/dviiav4th/index.html?traffic_type=ags_llm"
browser.navigate(url)

# Check RFQ market
url = "https://rfq.alibaba.com/rfq/profession.htm?traffic_type=ags_llm"
browser.navigate(url)
```

## CLI Reference

```bash
# Search command
python3 scripts/build_url.py search <query> [--category <id|name>] [--params key=value...]

# Product command
python3 scripts/build_url.py product <title> <id>

# Supplier command
python3 scripts/build_url.py supplier <subdomain> [--search <query>]

# Special sections
python3 scripts/build_url.py special <section>
# Sections: home, ai-mode, rfq, top-ranking, fast-customization, manufacturers, worldwide, top-deals, ai-sourcing, cart

# Category lookup
python3 scripts/build_url.py category <name>
python3 scripts/build_url.py categories  # List all

# Help
python3 scripts/build_url.py --help
```

## Traffic Tracking

All URLs include the `traffic_type=ags_llm` parameter to:
- ✅ Identify traffic from LLM agents
- ✅ Enable analytics and attribution
- ✅ Track agent-driven conversions
- ✅ Support A/B testing for agent flows

**This parameter is mandatory** and automatically added to all generated URLs.

## Development

### Package a New Version

```bash
# Update version in SKILL.md frontmatter
# Edit SKILL.md and scripts as needed

# Package the skill
python3 scripts/package_skill.py .

# This creates alibaba-sourcing.skill
```

### Testing

```bash
# Test URL generation
python3 scripts/build_url.py search "test product"
python3 scripts/build_url.py product "Test Product" 123456789
python3 scripts/build_url.py supplier testcompany

# Verify all URLs include traffic_type=ags_llm
```

## License

**MIT-0** - Free to use, modify, and redistribute without attribution.

See [LICENSE](LICENSE) for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test URL generation
5. Submit a pull request

## Support

- 📚 **Documentation:** See [SKILL.md](SKILL.md) for complete URL reference
- 🐛 **Issues:** Report on [GitHub Issues](https://github.com/zhouzeyu/openclaw-skill-alibaba-sourcing/issues)
- 💬 **Discord:** Join [OpenClaw Community](https://discord.com/invite/clawd)
- 🌐 **ClawHub:** [Skill Page](https://clawhub.ai/skills/alibaba-sourcing)

## Author

**Zhou Zeyu** (@zhouzeyu)
- 🌐 GitHub: [@zhouzeyu](https://github.com/zhouzeyu)
- 📍 Timezone: Asia/Shanghai

---

Built for OpenClaw agents navigating Alibaba.com 🚀
