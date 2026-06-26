---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: f4a677bd9d680e9793dee310c93c3656_618785265dbe11f1bd025254006c9bbf
    ReservedCode1: K7yjdkZAXok5x99XYswOzb3iDakvy9Bzs4Xo2IXdvJIaB3Tf+/+x/TKpegTrPZNIhc9Qh6yiXNBORSTzI893ylc10Dr+XbsZyoJm4xIVKSpoh3lynEJXbIvVRuI8MFBwpokUvO5IQnU0hpHY69o3mQXmXaBuVc3eUrvlHf0QdyLmeAJ3PeI94strkrg=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: f4a677bd9d680e9793dee310c93c3656_618785265dbe11f1bd025254006c9bbf
    ReservedCode2: K7yjdkZAXok5x99XYswOzb3iDakvy9Bzs4Xo2IXdvJIaB3Tf+/+x/TKpegTrPZNIhc9Qh6yiXNBORSTzI893ylc10Dr+XbsZyoJm4xIVKSpoh3lynEJXbIvVRuI8MFBwpokUvO5IQnU0hpHY69o3mQXmXaBuVc3eUrvlHf0QdyLmeAJ3PeI94strkrg=
---



# Global Food & Agriculture Intelligence

Comprehensive agrifood intelligence for the 8 billion people on Earth. 22 data sources spanning food security, crop production, commodity prices, climate impacts, agritech innovation, trade flows, and fisheries. Built for analysts, traders, policymakers, and anyone tracking the global food system.

## Triggers

- "What's the global food price outlook?"
- "Track wheat/corn/soybean supply and demand"
- "Analyze food crisis hotspots"
- "What's driving fertilizer prices?"
- "Assess climate impact on crop yields"
- "Compare alternative protein market growth"
- "Monitor Black Sea grain corridor status"
- "Evaluate food security for [country/region]"

## Capabilities

| # | Capability | Data Scope | Output Mode |
|---|-----------|-----------|-------------|
| 1 | Food price index & inflation tracking | FAO FFPI, World Bank Pink Sheet, FAO GIEWS | 5-category breakdown: cereals, meat, dairy, oils, sugar. Real vs. nominal, trend analysis |
| 2 | Food security & hunger monitoring | WFP HungerMap (90+ countries), FAO SOFI, IPC (35+ crisis countries), FEWS NET (30+ countries) | IPC Phase classification (1-5), affected population, acute malnutrition rates, outlook |
| 3 | Crop supply-demand balance (WASDE-style) | USDA WASDE (monthly), AMIS (G20+), FAOSTAT, IGC | 8 grains/oilseeds: production, consumption, trade, ending stocks, stock-to-use ratio |
| 4 | Commodity futures & price discovery | CBOT/CME, Euronext, DCE Dalian | Real-time prices across 20+ commodities with seasonal patterns and futures curves |
| 5 | Climate-agriculture nexus | NOAA ENSO, JRC MARS, NASA NDVI, IPCC | El Niño/La Niña crop impact, drought/wet maps, vegetation health indices |
| 6 | Fertilizer market intelligence | Urea, DAP, MOP, ammonia, phosphate | Prices by grade, production by country, trade flow disruptions, affordability index |
| 7 | Agritech & innovation landscape | AgFunder (VC data), FAO Digital Ag, UC Davis | Precision ag adoption, gene editing (CRISPR), vertical farming economics, alt-protein scaling |
| 8 | Agricultural trade & supply chains | WTO Agri Trade, ITC Trade Map, FAO GIEWS | Bilateral trade flows, export restriction tracker, Black Sea corridor alternatives |
| 9 | Livestock & dairy market | USDA livestock, FAOSTAT | Production, prices for beef, pork, poultry, dairy (butter, SMP, WMP, cheese) |
| 10 | Fisheries & aquaculture status | FAO SOFIA, Global Fishing Watch | Wild catch sustainability, aquaculture growth, IUU fishing detection |

## Workflow

```
User Query
    │
    ├─ Food security query → WFP HungerMap + IPC + FAO SOFI
    │   └─ Output: Hotspot map + population at risk + drivers + outlook
    │
    ├─ Commodity price query → CBOT/CME futures + USDA WASDE + FAO FFPI
    │   └─ Output: Current price + S&D table + seasonal pattern + 3-month forecast
    │
    ├─ Crop outlook query → USDA WASDE + AMIS + FAO GIEWS + NOAA ENSO
    │   └─ Output: Global production/trade/stocks table + weather risk + price impact
    │
    ├─ Fertilizer query → World Bank + trade data + production capacity
    │   └─ Output: N/P/K price trends + affordability + supply disruption risk
    │
    └─ Climate-agriculture query → NOAA ENSO + JRC MARS + NASA NDVI + IPCC
        └─ Output: Crop-specific impact by region + yield forecast revision
```

## Output Formats

### Format 1: Commodity S&D (Supply & Demand)
```
| | 2024/25 | 2025/26 Est | YoY Change | Source |
|-|---------|-------------|-----------|--------|
| Beginning Stocks | XX M mt | XX | +X% | USDA |
| Production        | XX      | XX | +X% | USDA |
| Imports           | XX      | XX | +X% | USDA |
| Feed Use          | XX      | XX | +X% | USDA |
| Food/Seed/Ind     | XX      | XX | +X% | USDA |
| Exports           | XX      | XX | +X% | USDA |
| Ending Stocks     | XX      | XX | +X% | USDA |
| Stock-to-Use      | XX.X%   | XX.X% | +/- | USDA |
```

### Format 2: Food Crisis Dashboard
```
| Country | IPC Phase 3+ Pop (M) | IPC Phase 4+ Pop (M) | Trend | Drivers |
```

### Format 3: Fertilizer Affordability Index
```
| Nutrient | Current $/mt | 12M Ago | 5Y Avg | Affordability Ratio | Country Dependence |
```

## Usage Guidelines

- Always cite source (USDA WASDE vs. FAO vs. IGC) with release date
- Note where USDA vs. FAO vs. AMIS estimates diverge
- Distinguish structural food system issues from weather-driven short-term shocks
- Flag export restrictions, sanctions, and trade policy changes in real time

## Examples

**Q: Outlook for wheat prices in H2 2026?**
→ USDA WASDE latest (global S&D) + FAO FFPI cereal index + NOAA ENSO forecast + Black Sea corridor status → Price range: $X-$X/bu, driven by [US HRW conditions / Black Sea exports / India stock policy]

**Q: Which countries are at highest risk of famine?**
→ WFP HungerMap + IPC Phase 4-5 populations + FEWS NET outlook → Top 5: Sudan (17.7M), DRC (23.4M), Ethiopia (15.8M), Yemen (17M), Nigeria (24.9M), driven by [conflict/climate/economic]

**Q: Is the global food system becoming more resilient?**
→ FAO SOFI trend data + AgFunder VC investment + FAO Digital Agriculture adoption → [Assessment with data trends]

---

**Data Sources (22 total)**: See `references/agrifood_sources.json` for complete listing with URLs and update frequencies.
*（内容由AI生成，仅供参考）*
