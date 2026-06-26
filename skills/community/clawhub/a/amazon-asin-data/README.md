# Jiimore Skill

Amazon niche market analysis tool for cross-border e-commerce product selection via LinkFoxAgent API.

## Overview

Jiimore (极目工具) provides comprehensive Amazon marketplace data for product selection and market analysis. This skill enables querying niche market information, analyzing competition, evaluating demand, and identifying profitable opportunities in US, Japan, and Germany markets.

## Quick Start

### 1. Setup API Key

```bash
export LINKFOXAGENT_API_KEY="your_api_key_here"
```

For persistent configuration, add to your shell profile (`~/.bashrc`, `~/.zshrc`, or `~/.profile`):

```bash
echo 'export LINKFOXAGENT_API_KEY="your_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

### 2. Usage in OpenClaw

Activate the skill by mentioning Amazon market research or product selection:

```
User: "Analyze the bluetooth charger market in the US"
User: "Find low-competition niches for kitchen gadgets"
User: "What are the best opportunities in German market for coffee products?"
```

The skill automatically:
- Translates keywords to target market language
- Queries Amazon marketplace data
- Analyzes competition and demand
- Presents actionable insights

### 3. Command-Line Usage

The Python client can also be used standalone:

```bash
# Basic search
python scripts/jiimore_client.py "wireless earbuds" -c US -n 10

# Find low-competition niches
python scripts/jiimore_client.py "yoga mat" --low-competition -c US

# Find profitable niches
python scripts/jiimore_client.py "kitchen knife" --profitable -c DE

# Get raw JSON output
python scripts/jiimore_client.py "desk lamp" -c JP --json
```

## Features

### Market Analysis
- Demand scoring (0-100 scale)
- Competition assessment
- Brand concentration analysis
- Price range evaluation
- Sales volume tracking
- Search trend analysis

### Data Metrics
- **Sales**: Weekly (T7) and quarterly (T90) volumes
- **Traffic**: Search volumes, clicks, conversion rates
- **Competition**: Brand counts, market share concentration
- **Pricing**: Min/max/average with profit margins
- **Lifecycle**: Launch rates, success rates, return rates
- **Advertising**: ACOS, CPC metrics

### Smart Filtering
- Natural language to API parameters
- Low-competition presets
- Profitable niche discovery
- Custom filter combinations
- Progressive refinement

## Skill Structure

```
jiimore/
├── SKILL.md                    # Main skill documentation (for Claude)
├── README.md                   # This file (for users/developers)
├── scripts/
│   └── jiimore_client.py       # Python API client
└── references/
    ├── API-Overview.md         # LinkFoxAgent setup & overview
    └── Jiimore.md              # Complete API reference
```

## Examples

### Natural Language Queries

**Basic Market Search**
```
"Show me bluetooth product niches in the US"
```

**Low Competition**
```
"Find niches with less than 30 brands and low brand concentration"
```

**Price Range**
```
"Search for products between $20-50 with good profit margins"
```

**Quality Focus**
```
"Find niches with low return rates and high conversion"
```

**Growth Opportunity**
```
"Show me emerging markets with increasing search volume"
```

### Python API Examples

**Basic Query**
```python
from jiimore_client import JiimoreClient

client = JiimoreClient()
results = client.query("wireless charger", country="US", page_size=50)

print(f"Found {results['total']} niches")
for niche in results['data'][:5]:
    print(f"{niche['nicheTitle']}: Demand={niche['demand']}")
```

**Low Competition Search**
```python
results = client.find_low_competition(
    keyword="yoga mat",
    country="US",
    max_brands=30,
    max_brand_share=0.3,
    min_demand=70
)
```

**Profitable Niche Search**
```python
results = client.find_profitable(
    keyword="kitchen gadget",
    country="DE",
    min_price=15,
    max_price=50,
    min_profit_ratio=0.3,
    max_return_rate=0.1
)
```

**Custom Filters**
```python
filters = {
    "productCountMax": 200,
    "unitsSoldT7Min": 1000,
    "searchVolumeGrowthT7Min": 0.1,
    "top5ProductsClickShareMax": 0.4
}

results = client.query(
    keyword="desk lamp",
    country="JP",
    sort_field="demand",
    filters=filters
)
```

## Integration with Other Tools

### Python Sandbox
Process Jiimore results for advanced analysis:
```
1. Query niches with Jiimore
2. Pass JSON to @Python沙箱
3. Calculate custom metrics
4. Generate Markdown tables
5. Export to CSV/Excel
```

### Web Search
Complement with competitor research:
```
1. Get top niches from Jiimore
2. Use @网页检索 for competitor analysis
3. Research product reviews and trends
```

### AI Image Generation
Create product mockups:
```
1. Get referenceAsinImageUrl from Jiimore data
2. Use AI绘图 with reference images
3. Generate product variations
```

## Best Practices

### Query Strategy
1. **Start Broad**: Initial query with keyword + country
2. **Analyze**: Review demand, competition, pricing
3. **Refine**: Apply 2-3 key filters based on insights
4. **Deep Dive**: Request detailed metrics for promising niches

### Performance
- Use defaults for exploration
- Apply specific filters for targeted searches
- Avoid over-constraining (may return no results)
- Cache results for repeated analysis

### Data Interpretation
- High demand (>70) + Low brand concentration (<0.3) = Strong opportunity
- High return rate (>0.15) = Quality concerns
- Low ACOS (<0.2) + High conversion = Profitable niche
- High search growth + Low product count = Emerging opportunity
- High TOP5 share (>0.5) = Dominated market

## Troubleshooting

### "API key required" Error
```
Error: API key required. Set LINKFOXAGENT_API_KEY...
```
**Solution**: Set the environment variable as shown in Quick Start

### "Authentication failed" Error
```
Error: Authentication failed. Check your API key.
```
**Solution**: Verify API key is correct and active

### "No results" Warning
```
Warning: No niches match your criteria
```
**Solution**: Relax filters or try different keywords

### Rate Limit Errors
```
Error: Rate limit exceeded. Please retry later.
```
**Solution**: The client auto-retries with exponential backoff. Wait or reduce query frequency.

## API Reference

See detailed documentation:
- `references/API-Overview.md` - Setup and authentication guide
- `references/Jiimore.md` - Complete parameter and response reference
- `SKILL.md` - Full skill documentation for Claude

## Requirements

- Python 3.7+
- `requests` library
- LinkFoxAgent API key
- Internet connection

Install Python dependencies:
```bash
pip install requests
```

## License

Part of OpenClaw project. See main repository license.

## Support

For issues or questions:
1. Check `references/` documentation
2. Review error messages and troubleshooting
3. Verify API key and environment setup
4. Contact LinkFoxAgent support for API-related issues

## Notes

- Supported markets: US, JP, DE only
- Processing time: 1-5 minutes for complex queries (background execution)
- Data is sourced from Amazon marketplace analytics
- Always validate findings with current marketplace conditions
- Results include both weekly (T7) and quarterly (T90) metrics for trend analysis
