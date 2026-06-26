---
name: flight-price-chart
description: Embed interactive flight price trend charts into AI responses. Requires SerpAPI key for real-time data. Use when users want to visualize 60-day price history for specific flight routes.
metadata:
  version: 1.0.0
  agent:
    type: ui-component
    runtime: react
    context_isolation: embedded
  openclaw:
    emoji: "📈"
    priority: 85
    requires:
      bins:
        - node
    intents:
      - price_trend_display
      - flight_price_analysis
    patterns:
      - "(price.trend|price.history|price.chart|trend.chart)"
      - "(flight.recommendation|flight.search.result).*(price.analysis)"
      - "(should.i.buy|buy.now.or.wait|price.alert).*(flight)"
      - "(how.has.price.changed|price.movement|price.fluctuation)"
---

# Flight Price Chart

Embed an interactive flight price trend visualization component when AI responses contain flight recommendations with confirmed OD (Origin-Destination) pairs.

## ⚠️ 使用前必需配置

**本 skill 需要 SerpAPI Key 才能获取实时航班价格数据。**

如果用户尚未配置 SerpAPI Key，请先引导用户完成以下步骤：

1. **注册 SerpAPI 账号**：访问 [https://serpapi.com/users/sign_up](https://serpapi.com/users/sign_up) 免费注册
2. **获取 API Key**：登录后在 Dashboard 中复制你的 API Key
3. **配置项目**：
   - 复制 `price/config.example.json` 为 `price/config.json`
   - 将 API Key 填入 `config.json` 中的 `serpapi.apiKey` 字段
   - 重启服务器使配置生效

> 💡 SerpAPI 提供免费额度，足够个人使用。配置完成后即可获取真实的航班价格趋势数据。

## Quick Start

1. **Detect flight recommendations**: When AI output contains flight search results with specific origin and destination
2. **Fetch price data**: Call the price trend API with the OD pair
3. **Render component**: Embed the `PriceChart` component at the end of the response

## Component API

### PriceChart Component

```jsx
<PriceChart
  data={priceHistory}           // Array of {date, price}
  currentPrice={currentPrice}   // Current flight price
  analysis={analysis}           // Price analysis object
  destination={destination}     // Destination info
/>
```

### Data Structure

**priceHistory** - 60-day price history:
```javascript
[
  { date: "2026-03-01", price: 1299 },
  { date: "2026-03-02", price: 1350 },
  // ... up to 60 days
]
```

**analysis** - Price analysis object:
```javascript
{
  min: 1199,           // Lowest price in period
  max: 1899,           // Highest price in period
  average: 1450,       // Average price
  pctDiff: -12,        // Percentage vs average
  level: "low",        // "low" | "mid" | "high"
  trend: "falling"     // "falling" | "rising" | "stable"
}
```

**destination** - Destination info:
```javascript
{
  code: "TYO",         // Airport/city code
  name: "Tokyo"        // City name
}
```

## Usage Scenarios

### 1. After Flight Search Results
When AI returns flight recommendations:
```
[Flight cards showing 3-5 options]
[Price trend chart showing 60-day history]
[Buy/wait recommendation]
```

### 2. Price Inquiry Responses
When user asks about price trends:
```
"Here's the price trend for Tokyo flights over the past 60 days..."
[Price trend chart]
"Current prices are 12% below average, making it a good time to buy."
```

### 3. Buy/Wait Recommendations
When providing purchase timing advice:
```
[Price analysis summary]
[Recommendation card: "Buy Now" or "Wait"]
[Price trend chart for context]
```

## Integration with flyai

When using flyai for flight searches:

1. Call `flyai search-flight` to get flight results
2. Extract OD pair from search parameters
3. Call price trend API with OD pair
4. Append PriceChart component after flight cards

## Visual Design

### Color Coding
- **Low price**: Green (#16A571) - Below average
- **Mid price**: Gray (#666666) - Near average
- **High price**: Red (#E54D4D) - Above average
- **Brand**: Purple (#6666FF) - Chart line

### Chart Features
- Interactive hover/touch to see daily prices
- Dashed line showing average price
- Current price highlighted
- Min/max/avg stats at bottom
- 60-day date range

## Data Source Notice

### Quick Setup for Real Data

By default, the price trend uses **simulated data** (for demo/development only).

**To enable real price data**, configure your SerpAPI Key:

1. Get API Key at https://serpapi.com/users/sign_up
2. Add to `price/config.json`:
   ```json
   { "serpapi": { "apiKey": "your-key-here" } }
   ```
3. Restart the server

See `references/configure-serpapi.md` for detailed setup guide.

### Data Flow

```
Before: User Query → Mock Data Generator → Estimated Prices
After:  User Query → SerpAPI → Real Prices → Auto-collect & Store
```

### Confidence Levels

As data accumulates, AI responses should indicate confidence:

| Days of Data | Confidence | AI Disclaimer |
|--------------|------------|---------------|
| < 7 days | Low | "价格数据为估算值，仅供参考" |
| 7-29 days | Medium | "根据部分真实价格数据..." |
| 30+ days | High | "根据积累的真实价格数据..." |

See `references/data-sources.md` for more details.

## References

| Component | Doc |
|-----------|-----|
| PriceChart | `references/price-chart-component.md` |
| Data API | `references/price-api.md` |
| Analysis Logic | `references/price-analysis.md` |
| Data Sources | `references/data-sources.md` |

## Example Output

```markdown
Based on your search, here are the best flights to Tokyo:

[Flight Cards Component]

## Price Analysis

Current prices are **12% below average** for this route.

[PriceChart Component]

### Recommendation: Buy Now ✅
- Current price: ¥1,299
- Historical average: ¥1,450
- You save: ¥151

Prices have been falling over the past 2 weeks. If you need to travel in peak season, booking now is recommended.
```
