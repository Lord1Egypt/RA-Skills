---
name: Supply Chain Intelligence
slug: supply-chain-intelligence
description: End-to-end supply chain analysis and optimization skill. Features inventory optimization, logistics route planning, supplier risk assessment, demand forecasting, disruption monitoring, and cost analysis across multi-tier supply networks.
version: 1.0.0
author: ai-gaoqian
tags:
  - supply-chain
  - logistics
  - inventory
  - procurement
  - risk-management
metadata:
  openclaw:
    requires: "python>=3.10, openclaw>=0.9.0"
---

# Supply Chain Intelligence

End-to-end supply chain analysis and optimization for modern enterprises. Monitors multi-tier supply networks, predicts disruptions, optimizes inventory levels, and evaluates supplier performance.

## Usage

```
supplychain: analyze inventory levels across all warehouses
supplychain: assess supplier risk for [Supplier Name]
supplychain: optimize shipping routes from [Origin] to [Destination]
supplychain: forecast demand for [Product SKU] next quarter
supplychain: monitor disruption risks in [Region]
```

## Execution Flow

1. **Inventory Analytics** — ABC classification, safety stock calculation, reorder point optimization, dead stock identification
2. **Supplier Risk** — Score across financial health, geopolitical exposure, delivery performance, quality metrics, single-source dependency
3. **Logistics Optimization** — Multi-modal route planning, cost vs. speed trade-off, carbon footprint per route, last-mile efficiency
4. **Demand Forecasting** — Time-series analysis with seasonality, trend, and external factor correlation (weather, holidays, economic indicators)
5. **Disruption Monitor** — Real-time tracking of port congestion, natural disasters, trade policy changes, labor strikes affecting supply routes
6. **Cost Analysis** — Total landed cost breakdown, tariff impact simulation, make-vs-buy analysis

## Output Format

```markdown
# Supply Chain Analytics Dashboard
**Snapshot**: 2026-06-12

## Inventory Health: 82/100
| Warehouse | SKU Count | Days of Stock | Status |
|-----------|-----------|---------------|--------|
| Shanghai  | 1,240     | 45            | Optimal |
| Rotterdam | 890       | 12            | ⚠️ Low  |
| LA        | 1,560     | 62            | Excess  |

## Top Supplier Risks
| Supplier | Risk Score | Trigger |
|----------|------------|---------|
| AlphaChem | 78/100 | Geopolitical exposure (Taiwan Strait) |
| BetaParts | 65/100 | Single-source dependency |

## Active Disruptions
- Suez Canal: Minor delays (2-3 days) due to increased traffic
- Shanghai Port: Typhoon warning — monitor for 48h

## Demand Forecast (Q3 2026)
- SKU-PRO-001: +12% MoM, seasonal peak expected August
- SKU-PRO-002: -5% MoM, declining trend

## Cost Saving Opportunities
1. Consolidate Rotterdam-LA shipments: Save $45K/month
2. Switch Supplier Gamma to local alternative: Reduce lead time 14 days
```

## Notes

- Inventory data should be provided in CSV or Excel format with SKU, warehouse, quantity, and date fields
- Supplier risk assessment quality improves with historical delivery and quality data
- Disruption monitoring requires web search access for real-time news and alerts
- Demand forecasts are probabilistic; confidence intervals provided
