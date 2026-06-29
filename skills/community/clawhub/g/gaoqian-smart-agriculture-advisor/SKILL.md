---
name: Smart Agriculture Advisor
slug: smart-agriculture-advisor
description: Precision agriculture intelligence skill. Features crop health monitoring, weather-based planting schedules, soil analysis recommendations, pest and disease identification, yield prediction, irrigation optimization, and agricultural market price tracking.
version: 1.0.0
author: ai-gaoqian
tags:
  - agriculture
  - farming
  - crop-management
  - precision-ag
  - food-security
metadata:
  openclaw:
    requires: "python>=3.10, openclaw>=0.9.0"
---

# Smart Agriculture Advisor

Precision agriculture intelligence for farmers, agronomists, and agricultural enterprises. Combines weather data, soil science, crop modeling, and market intelligence to optimize farming decisions.

## Usage

```
agri: analyze soil report for [Region/Crop]
agri: plan planting schedule for [Crop] in [Location]
agri: identify pest from [image/description]
agri: predict yield for [Crop] on [Acreage]
agri: check market prices for [Crop] in [Region]
agri: optimize irrigation for [Field] based on weather forecast
```

## Execution Flow

1. **Soil Analysis** — Interpret soil test results (NPK, pH, organic matter, micronutrients), recommend amendments and fertilizer blends
2. **Planting Calendar** — Generate optimal planting/harvesting dates based on crop type, hardiness zone, frost dates, and weather forecast
3. **Pest & Disease ID** — Image-based and symptom-based identification for 500+ crop pests and diseases; integrated treatment recommendations (organic and conventional)
4. **Yield Prediction** — Machine learning model incorporating historical yield, weather patterns, soil quality, and input usage
5. **Irrigation Planner** — ET-based (evapotranspiration) water scheduling, soil moisture monitoring integration, drought response strategies
6. **Market Intelligence** — Real-time commodity prices, futures trends, supply-demand analysis for major agricultural markets
7. **Sustainability Score** — Carbon sequestration potential, water efficiency, biodiversity impact assessment

## Output Format

```markdown
# Smart Agriculture Report
**Farm**: Green Valley Farms | **Region**: Central Valley, CA
**Date**: 2026-06-12

## Crop Status Dashboard
| Field | Crop | Growth Stage | Health | Est. Yield |
|-------|------|-------------|--------|------------|
| F-01  | Corn | V8 (8-leaf) | 92%    | 185 bu/acre |
| F-02  | Soybean | R1 (flowering) | 88% | 52 bu/acre |
| F-03  | Wheat | Grain fill | 78% | ⚠️ Rust detected |

## Weather Outlook (7-Day)
- Temperature: 72-89°F (above seasonal avg)
- Precipitation: 0.2" expected (below avg)
- Frost Risk: None
- Heat Stress Alert: 3 days above 90°F → Recommend supplemental irrigation

## Pest Alert: Soybean Aphid
- Detected: Field F-02, 15% of plants
- Economic Threshold: 250 aphids/plant (currently 180)
- Recommendation: Monitor for 48h; prepare insecticide if count exceeds threshold

## Market Prices (Spot)
| Commodity | Price | Change (30d) |
|-----------|-------|-------------|
| Corn #2 Yellow | $4.85/bu | +3.2% |
| Soybeans | $11.20/bu | -1.8% |
| Hard Red Winter Wheat | $6.15/bu | +5.1% |

## Sustainability Score: 74/100
- Carbon Sequestration: 0.8 tCO2e/acre/year (cover cropping)
- Water Efficiency: 85% (drip irrigation installed)
- Biodiversity: Medium (3 crop rotation, 2 pollinator strips)

## Action Items
1. Apply fungicide to F-03 wheat within 48h
2. Increase F-02 irrigation 15% during heat wave
3. Consider forward-contracting 30% of corn at $4.95+
```

## Notes

- Soil test data should be provided as PDF/lab report or manual entry
- Pest identification supports both photo upload and text description
- Market prices sourced from USDA AMS and CME Group data
- Yield predictions are most accurate with 3+ years of historical data
- Consider local agricultural extension service guidelines alongside AI recommendations
