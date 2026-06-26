---
name: jiimore
description: |
  Amazon niche market analysis tool for cross-border e-commerce product selection. Retrieves detailed market data including demand scores, competition analysis, price ranges, brand concentration, and sales metrics. Use when users ask about Amazon market research, product selection, niche analysis, or competitive intelligence for US, Japan, or Germany markets.
---

# Jiimore - Amazon Niche Market Analysis

Jiimore (极目工具) provides comprehensive Amazon marketplace data for cross-border e-commerce product selection and market analysis. This skill enables you to query niche market information, analyze competition, evaluate demand, and identify profitable opportunities.

## Setup

Before using this skill, ensure the LinkFoxAgent API key is configured:

```bash
export LINKFOXAGENT_API_KEY="your_api_key_here"
```

Users can obtain their API key from the LinkFoxAgent dashboard.

## Core Capabilities

### Market Analysis
- Search Amazon niche markets by keyword with automatic translation
- Analyze demand scores and market opportunities
- Evaluate competition levels and brand concentration
- Review price ranges and profit margins
- Track sales trends and growth rates

### Data Metrics
- **Sales Data**: Weekly (T7) and quarterly (T90) sales volumes and trends
- **Traffic Data**: Search volumes, click counts, conversion rates
- **Competition**: Brand counts, TOP5 brand/product click shares
- **Pricing**: Average, minimum, maximum prices with profit margin analysis
- **Product Lifecycle**: New product launch rates, success rates, return rates
- **Advertising**: ACOS (Advertising Cost of Sales), CPC data

## Usage Examples

### Basic Market Search

User: "Analyze the bluetooth market in the US"

The skill will:
1. Translate keyword to target market language if needed
2. Query Amazon US marketplace data for "bluetooth"
3. Return top 50 results sorted by 7-day sales volume
4. Present key metrics: demand score, price range, competition level

### Advanced Filtering

User: "Find low-competition, high-demand niches with brand concentration under 30%"

The skill will:
1. Apply filters: `brandCountMax=50`, `top5BrandsClickShareMax=0.3`
2. Sort by demand score
3. Identify opportunities with less brand dominance

User: "Show me niches with product count 50-200, average price $20-50, and low return rate"

The skill will:
1. Set `productCountMin=50`, `productCountMax=200`
2. Set `avgPriceMin=20`, `avgPriceMax=50`
3. Filter `returnRateT360Max=0.1` (10% max return rate)
4. Return matching opportunities

## Natural Language to Parameters

The skill automatically converts natural language queries to API parameters:

### Country Selection
- "US", "United States", "America" → `countryCode: "US"`
- "Japan", "JP" → `countryCode: "JP"`
- "Germany", "DE", "Deutschland" → `countryCode: "DE"`

### Sorting Preferences
- "by sales", "top selling" → `sortField: "unitsSoldT7"`
- "by demand", "highest demand" → `sortField: "demand"`
- "by price" → `sortField: "avgPrice"`
- "by search volume" → `sortField: "searchVolumeT7"`

### Competition Filters
- "low competition" → suggests `brandCountMax`, `top5BrandsClickShareMax`
- "high demand" → sorts by `demand` descending
- "few products" → sets `productCountMax`
- "established brands" → sets `avgBrandAgeMin`

### Quality Filters
- "low return rate" → sets `returnRateT360Max`
- "high profit margin" → sets `profitRate50Min`
- "good conversion" → sets `searchConversionRateT7Min`

## Response Structure

### Key Fields Explained

**Market Identification**
- `nicheTitle`: Niche market title (English)
- `translationZh`: Chinese translation
- `nicheId`: Unique market identifier
- `demand`: Market demand score (0-100, higher is better)

**Pricing**
- `avgPrice`: Average product price
- `minimumPrice`: Lowest price in niche
- `maximumPrice`: Highest price in niche
- `profitMarginGt50PctSkuRatio`: Ratio of products with >50% profit margin

**Competition**
- `productCount`: Total number of products
- `brandCount`: Number of brands
- `top5BrandsClickShare`: Market share of top 5 brands (0-1, lower means less concentration)
- `top5ProductsClickShare`: Market share of top 5 products (0-1)

**Sales & Traffic**
- `unitsSoldWeekly` / `unitsSoldQuarterly`: Sales volume
- `searchVolumeWeekly` / `searchVolumeQuarterly`: Search volume
- `searchVolumeGrowthWeekly` / `searchVolumeGrowthQuarterly`: Growth rate (0-1)
- `clickCountWeekly` / `clickCountQuarterly`: Click volume

**Conversion**
- `searchConversionRateWeekly` / `searchConversionRateQuarterly`: Search to purchase rate (0-1)
- `clickToSaleConversionWeekly`: Click to purchase rate (0-1)

**Product Lifecycle**
- `launchRateSemiannual`: Product launch success rate over 180 days (0-1)
- `newProductsLaunchedSemiannual`: Number of new products launched
- `successfulLaunchedSemiannual`: Number of successful launches
- `returnRateAnnual`: Annual return rate (0-1, lower is better)

**Advertising**
- `acos`: Advertising Cost of Sales (0-1, lower is better)
- `cpc`: CPC data with `low`, `medium`, `high` values

**Other**
- `avgBrandAgeNow` / `avgBrandAgeQuarterly`: Brand age metrics
- `breakEvenRatio`: Break-even ratio
- `referenceAsinImageUrl`: Representative product image URL
- `categorieList`: Product categories

### Percentage Fields

Many fields use decimal values (0-1) representing percentages:
- `0.3` = 30%
- `0.05` = 5%
- `1.0` = 100%

When presenting to users, convert to percentages for clarity.

## Best Practices

### Progressive Disclosure
1. **Initial Query**: Start with basic parameters (keyword, country)
2. **Analyze Results**: Review demand, competition, pricing
3. **Refine Search**: Apply specific filters based on insights
4. **Deep Dive**: Request detailed metrics for promising niches

### Parameter Optimization
- Use defaults for exploratory searches
- Apply 2-3 key filters for targeted searches
- Avoid over-constraining (may return no results)
- Iterate based on result patterns

### Async Execution
- Queries run in background by default (1-5 minute processing)
- Users can continue conversation during execution
- Results delivered via callback when ready
- HTML reports provided when available

### Data Interpretation
- **High demand (>70) + Low brand concentration (<0.3)**: Strong opportunity
- **High return rate (>0.15)**: Quality concerns, investigate further
- **Low ACOS (<0.2) + High conversion**: Profitable niche
- **High search growth + Low product count**: Emerging opportunity
- **High TOP5 share (>0.5)**: Dominated market, difficult entry

## Error Handling

### Common Issues

**Missing API Key**
```
Error: LINKFOXAGENT_API_KEY environment variable not found
Solution: Configure API key before using skill
```

**Invalid Country Code**
```
Error: Country code must be US, JP, or DE
Solution: Use supported country codes only
```

**No Results**
```
Warning: No niches match your criteria
Solution: Relax filters or try different keywords
```

**Rate Limiting**
```
Error: API rate limit exceeded
Solution: Wait and retry, or adjust query frequency
```

## Advanced Features

### Pagination
- Default: 50 results per page
- Range: 10-100 results
- Use `page` parameter for additional results

### Custom Sorting
- Primary sort: `sortField` parameter
- Direction: `sortType` (desc/asc)
- Multi-criteria: Request sorted then filtered results

### Comparative Analysis
- Query multiple markets (US vs JP vs DE)
- Compare time periods (weekly vs quarterly trends)
- Benchmark against category averages

### Export Options
- JSON data for programmatic analysis
- Structured tables for visualization
- Image URLs for product reference

## Integration with Other Tools

### Python Sandbox (`@Python沙箱`)
After receiving JSON results:
- Calculate custom metrics
- Generate Markdown tables
- Export to CSV/Excel
- Analyze images from `referenceAsinImageUrl`
- Create statistical summaries

Example workflow:
1. Query niches with jiimore
2. Pass JSON to Python Sandbox
3. Filter/sort/calculate in Python
4. Export formatted results

### Web Search (`@网页检索`)
Complement jiimore data with:
- Competitor research
- Market trend articles
- Product reviews
- Supplier information

### AI Image Generation (`AI绘图`)
Create product mockups:
1. Get `referenceAsinImageUrl` from niche data
2. Use as reference image (up to 3 images)
3. Generate product variations with AI

## Technical Details

### API Endpoint
```
POST https://test-tool-gateway.linkfox.com/jiimore/getNicheInfoByKeyword
```

### Headers
```json
{
  "Authorization": "{LINKFOXAGENT_API_KEY}",
  "Content-Type": "application/json"
}
```

### Request Schema
See `references/Jiimore.md` for complete parameter documentation.

### Response Schema
```json
{
  "total": number,
  "data": array,
  "columns": array,
  "costToken": number,
  "type": "table",
  "title": string
}
```

## Limitations

- Supported markets: US, JP, DE only
- Keyword max length: 1000 characters
- Results per page: 10-100
- Background processing: 1-5 minutes typical
- Rate limits apply per API key

## Related Skills

- `linkfoxagent`: Parent skill for LinkFoxAgent tools
- `tavily`: Web search for market research
- `coding-agent`: Automated data analysis workflows

## References

For detailed API documentation:
- `references/API-Overview.md`: Setup and authentication
- `references/Jiimore.md`: Complete parameter reference

---

**Note**: This tool is optimized for cross-border e-commerce sellers and product researchers. Data is sourced from Amazon marketplace analytics and updated regularly. Always validate findings with current marketplace conditions.
