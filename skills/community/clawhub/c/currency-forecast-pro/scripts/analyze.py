#!/usr/bin/env python3
"""
Currency Forecast Pro - Technical Analysis Engine
Performs comprehensive technical analysis on any currency pair
"""

import json
import sys
import math
from datetime import datetime, timedelta

def fetch_exchange_data(base, target, days=75):
    """Fetch historical exchange rate data from Frankfurter API"""
    import urllib.request
    
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    
    url = f"https://api.frankfurter.app/{start_date}..{end_date}?from={base}&to={target}"
    
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data
    except Exception as e:
        return {"error": str(e)}

def calculate_ma(values, period):
    """Calculate simple moving average"""
    if len(values) < period:
        return sum(values) / len(values) if values else 0
    return sum(values[-period:]) / period

def calculate_trend_slope(values, period=30):
    """Calculate linear regression slope"""
    n = min(period, len(values))
    if n < 2:
        return 0
    
    x = list(range(n))
    y = values[-n:]
    x_mean = sum(x) / n
    y_mean = sum(y) / n
    
    numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
    denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
    
    return numerator / denominator if denominator != 0 else 0

def calculate_volatility(values):
    """Calculate average daily volatility as percentage"""
    if len(values) < 2:
        return 0
    
    daily_changes = [abs(values[i] - values[i-1]) for i in range(1, len(values))]
    avg_change = sum(daily_changes) / len(daily_changes)
    current = values[-1]
    
    return (avg_change / current) * 100 if current != 0 else 0

def analyze_currency_pair(base, target, days=75):
    """Perform complete technical analysis on a currency pair"""
    
    # Fetch data
    data = fetch_exchange_data(base, target, days)
    
    if "error" in data:
        return {"error": data["error"]}
    
    rates = data.get("rates", {})
    if not rates:
        return {"error": "No data available for this currency pair"}
    
    dates = sorted(rates.keys())
    values = [rates[d][target] for d in dates]
    
    n = len(values)
    current = values[-1]
    
    # Calculate indicators
    ma7 = calculate_ma(values, 7)
    ma14 = calculate_ma(values, 14)
    ma30 = calculate_ma(values, 30)
    
    slope = calculate_trend_slope(values, 30)
    volatility = calculate_volatility(values)
    
    # Support and resistance (20-day)
    recent = values[-20:] if len(values) >= 20 else values
    support = min(recent)
    resistance = max(recent)
    
    # Forecasts
    forecast_7d = current + (slope * 7)
    forecast_30d = current + (slope * 30)
    
    # Volatility bands
    vol_factor = volatility / 100
    forecast_7d_low = forecast_7d * (1 - vol_factor * 2)
    forecast_7d_high = forecast_7d * (1 + vol_factor * 2)
    forecast_30d_low = forecast_30d * (1 - vol_factor * 3)
    forecast_30d_high = forecast_30d * (1 + vol_factor * 3)
    
    return {
        "base": base,
        "target": target,
        "current_rate": round(current, 4),
        "data_points": n,
        "date_range": f"{dates[0]} to {dates[-1]}",
        "indicators": {
            "ma7": round(ma7, 4),
            "ma14": round(ma14, 4),
            "ma30": round(ma30, 4),
            "trend_slope": round(slope, 6),
            "trend_direction": "upward" if slope > 0 else "downward" if slope < 0 else "flat",
            "volatility_percent": round(volatility, 2),
            "support": round(support, 4),
            "resistance": round(resistance, 4)
        },
        "forecasts": {
            "7_day": {
                "predicted": round(forecast_7d, 4),
                "range_low": round(forecast_7d_low, 4),
                "range_high": round(forecast_7d_high, 4),
                "change_percent": round(((forecast_7d - current) / current) * 100, 2)
            },
            "30_day": {
                "predicted": round(forecast_30d, 4),
                "range_low": round(forecast_30d_low, 4),
                "range_high": round(forecast_30d_high, 4),
                "change_percent": round(((forecast_30d - current) / current) * 100, 2)
            }
        }
    }

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Currency Forecast Pro Analysis")
    parser.add_argument("--base", required=True, help="Base currency code (e.g., USD)")
    parser.add_argument("--target", required=True, help="Target currency code (e.g., EUR)")
    parser.add_argument("--days", type=int, default=75, help="Number of days of historical data")
    
    args = parser.parse_args()
    
    result = analyze_currency_pair(args.base.upper(), args.target.upper(), args.days)
    print(json.dumps(result, indent=2))
