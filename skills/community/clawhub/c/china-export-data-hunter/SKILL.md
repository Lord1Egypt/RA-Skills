---
name: china-export-data-hunter
description: Proactively hunt and discover China's export trade data to identify competitors, track market movements, and uncover new business opportunities. Designed for aggressive market intelligence gathering and competitive analysis.
---

# China Export Data Hunter

**Purpose**: Aggressively track, monitor, and analyze China's export activities to gain competitive advantages in international trade.

**Target Users**: Market researchers, competitive intelligence professionals, sales strategists, business development teams, and traders seeking to understand competitor movements and market dynamics.

---

## Data Sources

### Primary Sources

| Source | URL | Best For | Coverage |
|--------|-----|----------|----------|
| **UN Comtrade** | https://comtradeplus.un.org/ | Global trade flows, multi-country comparison | 200+ countries, 1962-present |
| **China Customs Statistics** | http://stats.customs.gov.cn/indexEn | Official China export data, HS-level detail | China-specific, highly detailed |

### Data Access Methods

**UN Comtrade**:
- Free API: 100 calls/hour (registration required at https://uncomtrade.org/docs/api-subscription-keys/)
- Premium API: Unlimited calls with subscription
- Bulk download available for premium users

**China Customs**:
- Web interface with query filters
- No official API; web scraping may be required for automation
- English interface available at `/indexEn`

---

## Hunting Strategies

### 1. Competitor Tracking

**Technique**: Monitor specific Chinese exporters' shipping patterns

```
Query Parameters:
- Reporter: China (156)
- Partner: Your target market country
- Flow: Exports (2)
- HS Code: Your product category
- Period: Last 12 months rolling
```

**Pro Tip**: Use UN Comtrade's "Partner" filter to see which countries are receiving shipments from China in your product category. Cross-reference with shipping records to identify major Chinese suppliers.

### 2. Market Entry Detection

**Technique**: Identify when Chinese exporters enter new markets

```
Strategy:
1. Query China's exports to all partners for your HS code
2. Compare year-over-year data
3. Flag countries with >50% growth in Chinese imports
4. Investigate: New market opportunity or increased competition?
```

### 3. Price Intelligence Gathering

**Technique**: Estimate competitor pricing through unit value analysis

```
Calculation:
Unit Value = Trade Value (USD) / Quantity (kg or units)

Compare unit values across:
- Different Chinese ports (quality/grade differences)
- Destination countries (pricing strategies)
- Time periods (price trends)
```

**China Customs Specific**:
- Access: http://stats.customs.gov.cn/indexEn
- Navigate: "Query by HS Code" → Select Chapter → Input Code
- Filter by: Trade Mode, Customs Port, Domestic Destination

---

## Advanced Hunting Techniques

### Multi-Source Cross-Reference

| What to Hunt | UN Comtrade | China Customs | Action |
|--------------|-------------|---------------|--------|
| Global market size | ✓ Query all partners | ✓ Verify China share | Calculate market penetration |
| Competitor countries | ✓ Compare reporters | ✓ Deep-dive China data | Identify top competitors |
| Price trends | ✓ Unit value trends | ✓ Port-level pricing | Spot arbitrage opportunities |
| Seasonal patterns | ✓ Monthly data | ✓ Monthly data | Optimize procurement timing |

### Seasonal Hunting Calendar

| Month | Hunt Focus | Data Source | Expected Insight |
|-------|-----------|-------------|------------------|
| Jan-Feb | Pre-Chinese New Year stockpiling | China Customs | Spot supply shortages |
| Mar-Apr | Post-holiday recovery patterns | UN Comtrade | Identify restocking trends |
| May-Jun | Mid-year shipping surge | Both | Plan inventory buildup |
| Jul-Aug | Peak shipping season analysis | Both | Negotiate rates before peak |
| Sep-Oct | Pre-holiday export rush | China Customs | Predict Q4 availability |
| Nov-Dec | Year-end clearance patterns | Both | Spot discount opportunities |

---

## Query Templates

### Template 1: Competitor Country Identification

```
Objective: Find which countries compete with China in specific product

UN Comtrade Query:
- Reporter: All countries
- Partner: Target import market (e.g., USA, Germany)
- Flow: Imports (1)
- HS Code: Your product
- Period: Latest year

Analysis: Sort by Trade Value - top reporters are your competitors
```

### Template 2: Chinese Export Surge Detection

```
Objective: Detect sudden increases in Chinese exports

China Customs Query:
- HS Code: Your product category
- Period: Last 24 months
- Flow: Export

Analysis: Calculate MoM and YoY growth rates, flag >30% increases
```

### Template 3: Port Intelligence

```
Objective: Identify which Chinese ports dominate your product export

China Customs Query:
- HS Code: Your product
- Filter: Port of Departure
- Period: Last 12 months

Insight: Top ports indicate manufacturing clusters and logistics hubs
```

---

## Data Interpretation Tips

### Red Flags to Hunt For

| Signal | Interpretation | Action |
|--------|---------------|--------|
| Sudden drop in China's exports | Supply chain disruption, policy change, or factory relocation | Investigate alternative suppliers |
| New competitor country emerging | Market diversification by buyers | Assess quality/price positioning |
| Unit value declining | Price war or commodity grade shift | Review pricing strategy |
| Unit value increasing | Premium segment growth or cost inflation | Evaluate margin pressure |

### Common Hunting Pitfalls

1. **Ignoring HS Code revisions**: HS codes change every 5 years - verify code validity for historical comparisons
2. **Misinterpreting "re-exports"**: Data may include goods transshipped through China
3. **Overlooking trade modes**: Processing trade vs. general trade have different implications
4. **Missing seasonal adjustments**: Chinese New Year (Jan/Feb) always distorts data

---

## Output Formats

When presenting hunting results, include:

1. **Executive Summary**: Top 3 findings with business implications
2. **Competitor Matrix**: Countries ranked by export volume/value
3. **Trend Charts**: 12-24 month trajectories
4. **Actionable Recommendations**: Specific next steps based on findings

---

## Rate Limits & Best Practices

| Source | Limit | Workaround |
|--------|-------|------------|
| UN Comtrade Free API | 100/hour | Cache results, batch queries overnight |
| UN Comtrade Web | Session-based | Use bulk download for large datasets |
| China Customs | No known limit | Respect server load, add delays between queries |

**Recommended Hunting Schedule**:
- Weekly: Monitor key competitors (automated API calls)
- Monthly: Deep-dive analysis with fresh data
- Quarterly: Comprehensive market intelligence report
