# Agricultural Forecasting Methodology

## Overview

This skill uses big data analytics to forecast agricultural output based on multiple factors.

## Forecasting Model

### 1. Baseline Yields

Reference yields for each crop type (tons/hectare):

| Crop | Baseline Yield |
|------|---------------|
| Wheat | 6.0 |
| Rice | 7.5 |
| Corn | 10.0 |
| Barley | 5.0 |
| Sorghum | 4.5 |
| Tomato | 35.0 |
| Potato | 25.0 |
| Cabbage | 40.0 |
| Cucumber | 30.0 |
| Apple | 25.0 |
| Orange | 20.0 |
| Grape | 15.0 |
| Peach | 18.0 |
| Soybean | 3.0 |
| Cotton | 2.5 |
| Sugarcane | 80.0 |

### 2. Impact Factors

#### Weather Factor
- **Excellent (1.15)**: Optimal conditions
- **Good (1.05)**: Favorable conditions
- **Normal (1.0)**: Average conditions
- **Poor (0.85)**: Unfavorable conditions
- **Bad (0.70)**: Severe adverse conditions

#### Market Trend Factor
- Range: -10% to +15%
- Based on historical price data and demand trends

### 3. Calculation Formula

```
Yield per hectare = Baseline × Weather Factor × Market Factor
Total Yield = Yield per hectare × Area (hectares)
```

### 4. Confidence Interval

| Data Quality | Confidence Level |
|-------------|------------------|
| High | 95% |
| Medium | 85% |
| Low | 70% |

### 5. Risk Assessment

- **Low Risk**: Weather factor > 1.0
- **Medium Risk**: Weather factor 0.85-1.0
- **High Risk**: Weather factor < 0.85

## Output Fields

| Field | Description |
|-------|-------------|
| forecast_id | Unique forecast identifier |
| crop_type | Type of crop |
| region | Geographic region |
| season | Growing season |
| area_hectares | Cultivated area |
| yield_forecast.per_hectare | Predicted yield per hectare |
| yield_forecast.total | Total predicted yield |
| yield_forecast.confidence_interval | Lower/upper bounds with confidence |
| factors.weather_factor | Applied weather impact |
| factors.market_factor | Applied market trend |
| risk_assessment.level | Overall risk level |
| recommendations | Actionable suggestions |

## Example Output

```json
{
  "forecast_id": "AGR_20240305010203",
  "crop_type": "wheat",
  "region": "North China Plain",
  "season": "spring",
  "area_hectares": 100,
  "yield_forecast": {
    "per_hectare": 6.5,
    "total": 650.0,
    "unit": "tons",
    "confidence_interval": {
      "lower": 5.5,
      "upper": 7.5,
      "confidence": "85%"
    }
  },
  "factors": {
    "weather_factor": 1.05,
    "market_factor": 1.03
  },
  "risk_assessment": {
    "level": "low",
    "weather_risk": "low"
  },
  "recommendations": [
    "市场价格有利，建议扩大种植面积"
  ]
}
```

## Data Sources

In production, the system would integrate:
- Weather APIs (historical and forecast data)
- Market price databases
- Soil quality databases
- Satellite imagery
- Agricultural research data
