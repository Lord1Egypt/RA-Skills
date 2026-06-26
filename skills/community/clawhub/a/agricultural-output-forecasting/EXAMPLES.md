# Examples

This document provides detailed examples of using the Agricultural Output Forecasting skill.

## Table of Contents

1. [Basic Examples](#basic-examples)
2. [Seasonal Forecasting](#seasonal-forecasting)
3. [Regional Analysis](#regional-analysis)
4. [Multi-Crop Planning](#multi-crop-planning)
5. [Risk Assessment](#risk-assessment)
6. [Integration Examples](#integration-examples)

## Basic Examples

### Example 1: Wheat Forecast

**Input:**
```python
from scripts.forecast import forecast_output

result = forecast_output(
    crop_type="wheat",
    area_hectares=100,
    region="North China Plain",
    season="spring",
    user_id="demo_user_001"
)

print(json.dumps(result, ensure_ascii=False, indent=2))
```

**Output:**
```json
{
  "success": true,
  "trial_mode": true,
  "trial_remaining": 9,
  "forecast": {
    "forecast_id": "AGR_20240306123045",
    "crop_type": "wheat",
    "region": "North China Plain",
    "season": "spring",
    "area_hectares": 100,
    "yield_forecast": {
      "per_hectare": 6.3,
      "total": 630,
      "unit": "tons",
      "confidence_interval": {
        "lower": 5.4,
        "upper": 7.2,
        "confidence": "85%"
      }
    },
    "factors": {
      "weather_factor": 1.05,
      "market_factor": 1.02
    },
    "risk_assessment": {
      "level": "low",
      "weather_risk": "low"
    },
    "recommendations": [
      "市场价格有利，建议扩大种植面积",
      "建议购买农业保险以降低风险"
    ]
  }
}
```

### Example 2: Rice in Southern China

**Input:**
```python
result = forecast_output(
    crop_type="rice",
    area_hectares=50,
    region="Yangtze River Delta",
    season="summer",
    user_id="demo_user_002"
)

print(f"Expected yield: {result['forecast']['yield_forecast']['total']} tons")
print(f"Risk level: {result['forecast']['risk_assessment']['level']}")
```

**Output:**
```
Expected yield: 382.5 tons
Risk level: low
```

## Seasonal Forecasting

### Example 3: Comparing Seasons

```python
from scripts.forecast import forecast_output

crop = "corn"
area = 200
region = "Northeast China"

# Compare all seasons
seasons = ["spring", "summer", "autumn", "winter"]
forecasts = {}

for season in seasons:
    result = forecast_output(
        crop_type=crop,
        area_hectares=area,
        region=region,
        season=season,
        user_id="seasonal_analysis_001"
    )
    
    if result["success"]:
        forecasts[season] = {
            "yield_per_hectare": result["forecast"]["yield_forecast"]["per_hectare"],
            "total_yield": result["forecast"]["yield_forecast"]["total"],
            "risk": result["forecast"]["risk_assessment"]["level"]
        }

# Display comparison
print("Seasonal Comparison for Corn in Northeast China:")
print("-" * 60)
for season, data in forecasts.items():
    print(f"{season.capitalize():10} | Yield: {data['yield_per_hectare']:5.1f} t/ha | "
          f"Total: {data['total_yield']:6.1f} t | Risk: {data['risk']}")
```

**Output:**
```
Seasonal Comparison for Corn in Northeast China:
------------------------------------------------------------
Spring     | Yield:  10.2 t/ha | Total: 2040.0 t | Risk: low
Summer     | Yield:  11.5 t/ha | Total: 2300.0 t | Risk: low
Autumn     | Yield:   9.8 t/ha | Total: 1960.0 t | Risk: medium
Winter     | Yield:   0.0 t/ha | Total:    0.0 t | Risk: high
```

### Example 4: Optimal Planting Window

```python
def find_optimal_window(crop, area, region):
    """Find the best season to plant a crop."""
    best_yield = 0
    best_season = None
    
    for season in ["spring", "summer", "autumn"]:
        result = forecast_output(
            crop_type=crop,
            area_hectares=area,
            region=region,
            season=season,
            user_id="optimal_window_001"
        )
        
        if result["success"]:
            yield_per_ha = result["forecast"]["yield_forecast"]["per_hectare"]
            risk = result["forecast"]["risk_assessment"]["level"]
            
            # Prefer lower risk, higher yield
            if risk != "high" and yield_per_ha > best_yield:
                best_yield = yield_per_ha
                best_season = season
    
    return best_season, best_yield

# Find optimal planting window
season, yield_rate = find_optimal_window("tomato", 10, "Shandong Peninsula")
print(f"Optimal planting season: {season}")
print(f"Expected yield: {yield_rate} tons/hectare")
```

## Regional Analysis

### Example 5: Comparing Regions

```python
crop = "wheat"
area = 100

regions = [
    "North China Plain",
    "Yangtze River Delta", 
    "Northeast China",
    "Sichuan Basin",
    "Guangdong Province"
]

print(f"Regional Comparison for {crop.capitalize()} (100 hectares):")
print("-" * 70)

for region in regions:
    result = forecast_output(
        crop_type=crop,
        area_hectares=area,
        region=region,
        season="spring",
        user_id="regional_analysis_001"
    )
    
    if result["success"]:
        forecast = result["forecast"]
        print(f"{region:25} | Yield: {forecast['yield_forecast']['total']:6.1f} t | "
              f"Risk: {forecast['risk_assessment']['level']:8} | "
              f"Weather: {forecast['factors']['weather_factor']:.2f}")
```

### Example 6: Climate Impact Analysis

```python
def analyze_climate_impact(crop, area, region, season):
    """Analyze how climate affects yield."""
    result = forecast_output(
        crop_type=crop,
        area_hectares=area,
        region=region,
        season=season,
        user_id="climate_analysis_001"
    )
    
    if not result["success"]:
        return None
    
    forecast = result["forecast"]
    
    analysis = {
        "baseline_yield": forecast["yield_forecast"]["per_hectare"] / forecast["factors"]["weather_factor"],
        "actual_yield": forecast["yield_forecast"]["per_hectare"],
        "weather_impact": (forecast["factors"]["weather_factor"] - 1) * 100,
        "market_impact": (forecast["factors"]["market_factor"] - 1) * 100,
        "risk_level": forecast["risk_assessment"]["level"]
    }
    
    return analysis

# Analyze climate impact for cotton
analysis = analyze_climate_impact("cotton", 50, "Xinjiang", "summer")

print("Climate Impact Analysis for Cotton in Xinjiang:")
print(f"  Baseline yield: {analysis['baseline_yield']:.2f} tons/hectare")
print(f"  Weather impact: {analysis['weather_impact']:+.1f}%")
print(f"  Market impact: {analysis['market_impact']:+.1f}%")
print(f"  Risk level: {analysis['risk_level']}")
```

## Multi-Crop Planning

### Example 7: Farm Portfolio Analysis

```python
farm_portfolio = [
    {"crop": "wheat", "area": 100, "region": "North China Plain", "season": "spring"},
    {"crop": "corn", "area": 150, "region": "Northeast China", "season": "summer"},
    {"crop": "soybean", "area": 80, "region": "Northeast China", "season": "spring"},
    {"crop": "potato", "area": 50, "region": "Inner Mongolia", "season": "summer"}
]

total_yield = 0
total_area = 0
risk_distribution = {"low": 0, "medium": 0, "high": 0}

print("Farm Portfolio Forecast:")
print("=" * 80)

for item in farm_portfolio:
    result = forecast_output(
        crop_type=item["crop"],
        area_hectares=item["area"],
        region=item["region"],
        season=item["season"],
        user_id="portfolio_analysis_001"
    )
    
    if result["success"]:
        forecast = result["forecast"]
        yield_total = forecast["yield_forecast"]["total"]
        risk = forecast["risk_assessment"]["level"]
        
        total_yield += yield_total
        total_area += item["area"]
        risk_distribution[risk] += item["area"]
        
        print(f"{item['crop'].capitalize():12} | {item['area']:3} ha | "
              f"{item['region']:20} | Yield: {yield_total:7.1f} t | Risk: {risk}")

print("=" * 80)
print(f"Total Area: {total_area} hectares")
print(f"Total Expected Yield: {total_yield:.1f} tons")
print(f"Average Yield: {total_yield/total_area:.2f} tons/hectare")
print(f"Risk Distribution: Low {risk_distribution['low']} ha, "
      f"Medium {risk_distribution['medium']} ha, High {risk_distribution['high']} ha")
```

### Example 8: Crop Rotation Planning

```python
def plan_rotation(field_history, available_crops, area, region):
    """Suggest crop rotation based on field history."""
    recommendations = []
    
    for crop in available_crops:
        # Skip if same as last year (simplified rotation logic)
        if crop == field_history[-1]:
            continue
            
        result = forecast_output(
            crop_type=crop,
            area_hectares=area,
            region=region,
            season="spring",
            user_id="rotation_planning_001"
        )
        
        if result["success"]:
            forecast = result["forecast"]
            recommendations.append({
                "crop": crop,
                "yield": forecast["yield_forecast"]["per_hectare"],
                "risk": forecast["risk_assessment"]["level"],
                "score": forecast["yield_forecast"]["per_hectare"] * 
                        (1.5 if forecast["risk_assessment"]["level"] == "low" else 1.0)
            })
    
    # Sort by score
    recommendations.sort(key=lambda x: x["score"], reverse=True)
    return recommendations

# Plan rotation for a field that grew wheat last year
field_history = ["wheat", "corn", "wheat"]  # Last 3 years
available_crops = ["wheat", "corn", "soybean", "potato"]

recommendations = plan_rotation(field_history, available_crops, 100, "North China Plain")

print("Crop Rotation Recommendations:")
print("-" * 60)
for i, rec in enumerate(recommendations[:3], 1):
    print(f"{i}. {rec['crop'].capitalize():10} | Yield: {rec['yield']:5.1f} t/ha | "
          f"Risk: {rec['risk']:8} | Score: {rec['score']:.1f}")
```

## Risk Assessment

### Example 9: Risk-Based Decision Making

```python
def assess_investment_risk(crop, area, region, season, investment_amount):
    """Assess if investment is worthwhile based on risk."""
    result = forecast_output(
        crop_type=crop,
        area_hectares=area,
        region=region,
        season=season,
        user_id="investment_analysis_001"
    )
    
    if not result["success"]:
        return None
    
    forecast = result["forecast"]
    
    # Simple ROI calculation (assuming $300/ton)
    expected_revenue = forecast["yield_forecast"]["total"] * 300
    roi = (expected_revenue - investment_amount) / investment_amount * 100
    
    risk_level = forecast["risk_assessment"]["level"]
    
    decision = {
        "crop": crop,
        "expected_yield": forecast["yield_forecast"]["total"],
        "expected_revenue": expected_revenue,
        "investment": investment_amount,
        "roi_percent": roi,
        "risk_level": risk_level,
        "recommendation": "PROCEED" if roi > 20 and risk_level != "high" else "REVIEW"
    }
    
    return decision

# Assess investment in tomato farming
decision = assess_investment_risk(
    crop="tomato",
    area=20,
    region="Shandong Peninsula",
    season="summer",
    investment_amount=50000
)

print("Investment Analysis:")
print(f"  Crop: {decision['crop'].capitalize()}")
print(f"  Expected Yield: {decision['expected_yield']:.1f} tons")
print(f"  Expected Revenue: ${decision['expected_revenue']:,.2f}")
print(f"  Investment: ${decision['investment']:,.2f}")
print(f"  ROI: {decision['roi_percent']:.1f}%")
print(f"  Risk Level: {decision['risk_level'].upper()}")
print(f"  Recommendation: {decision['recommendation']}")
```

## Integration Examples

### Example 10: Flask Web API

```python
from flask import Flask, request, jsonify
from scripts.forecast import forecast_output

app = Flask(__name__)

@app.route('/api/forecast', methods=['POST'])
def get_forecast():
    data = request.json
    
    result = forecast_output(
        crop_type=data.get('crop'),
        area_hectares=data.get('area'),
        region=data.get('region'),
        season=data.get('season'),
        user_id=data.get('user_id')
    )
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
```

### Example 11: CSV Batch Processing

```python
import csv
import json
from scripts.forecast import forecast_output

# Read fields from CSV
with open('fields.csv', 'r') as f:
    reader = csv.DictReader(f)
    fields = list(reader)

# Process each field
results = []
for field in fields:
    result = forecast_output(
        crop_type=field['crop'],
        area_hectares=float(field['area']),
        region=field['region'],
        season=field['season'],
        user_id="csv_batch_001"
    )
    
    results.append({
        "field_id": field['id'],
        "forecast": result.get('forecast', {}),
        "success": result['success']
    })

# Save results
with open('forecast_results.json', 'w') as f:
    json.dump(results, f, indent=2)
```

---

**See Also:**
- [Getting Started Guide](GETTING_STARTED.md)
- [FAQ](FAQ.md)
- [Security Policy](SECURITY.md)
