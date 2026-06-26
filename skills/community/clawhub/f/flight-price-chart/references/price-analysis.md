# Price Analysis Logic Reference

## Overview

This document describes the logic for analyzing flight prices and generating buy/wait recommendations.

## Price Level Classification

### Percentile-Based Approach

```javascript
function classifyPriceLevel(currentPrice, priceHistory) {
  const prices = priceHistory.map(p => p.price);
  const sorted = [...prices].sort((a, b) => a - b);

  const p33 = sorted[Math.floor(sorted.length * 0.33)];
  const p67 = sorted[Math.floor(sorted.length * 0.67)];

  if (currentPrice <= p33) return 'low';
  if (currentPrice >= p67) return 'high';
  return 'mid';
}
```

### Threshold Definitions

| Level | Condition | Display Color |
|-------|-----------|---------------|
| low | price ≤ 33rd percentile | Green (#16A571) |
| mid | 33rd < price < 67th percentile | Gray (#666666) |
| high | price ≥ 67th percentile | Red (#E54D4D) |

## Trend Detection

### 7-Day Moving Average Comparison

```javascript
function detectTrend(priceHistory) {
  if (priceHistory.length < 14) return 'stable';

  const recent7 = priceHistory.slice(-7).map(p => p.price);
  const earlier7 = priceHistory.slice(-14, -7).map(p => p.price);

  const recentAvg = recent7.reduce((a, b) => a + b, 0) / 7;
  const earlierAvg = earlier7.reduce((a, b) => a + b, 0) / 7;

  const threshold = 0.05; // 5% change threshold

  if (recentAvg < earlierAvg * (1 - threshold)) return 'falling';
  if (recentAvg > earlierAvg * (1 + threshold)) return 'rising';
  return 'stable';
}
```

### Trend Indicators

| Trend | Condition | Icon |
|-------|-----------|------|
| falling | Recent 7-day avg < Previous 7-day avg by 5%+ | 📉 |
| rising | Recent 7-day avg > Previous 7-day avg by 5%+ | 📈 |
| stable | Change within ±5% | ➡️ |

## Buy/Wait Recommendation Logic

### Decision Matrix

```javascript
function generateRecommendation(currentPrice, analysis, trend) {
  const { min, max, average } = analysis;

  // Strong buy: current price is at or near minimum
  if (currentPrice <= min * 1.05) {
    return {
      action: 'buy',
      confidence: 90,
      reason: 'Current price is at the lowest point in 60 days',
      expectedDrop: 0
    };
  }

  // Strong wait: current price is at or near maximum
  if (currentPrice >= max * 0.95) {
    return {
      action: 'wait',
      confidence: 85,
      reason: 'Prices are at peak levels, likely to drop',
      expectedDrop: Math.round((currentPrice - average) * 0.5)
    };
  }

  // Buy: price is below average and trend is falling
  if (currentPrice < average && trend === 'falling') {
    return {
      action: 'buy',
      confidence: 75,
      reason: 'Prices are below average and continuing to drop',
      expectedDrop: 0
    };
  }

  // Wait: price is above average and trend is rising
  if (currentPrice > average && trend === 'rising') {
    return {
      action: 'wait',
      confidence: 70,
      reason: 'Prices are rising but may stabilize soon',
      expectedDrop: Math.round((currentPrice - average) * 0.3)
    };
  }

  // Neutral: price is near average
  return {
    action: 'buy',  // Default to buy for neutral cases
    confidence: 60,
    reason: 'Prices are at typical levels',
    expectedDrop: 0
  };
}
```

### Recommendation Output Structure

```typescript
interface Recommendation {
  action: 'buy' | 'wait';
  confidence: number;     // 0-100
  reason: string;
  currentPrice: number;
  averagePrice?: number;
  expectedDrop?: number;
  waitUntil?: string;     // Optional: suggested wait date
}
```

## Statistical Calculations

### Average Price

```javascript
const average = Math.round(
  prices.reduce((a, b) => a + b, 0) / prices.length
);
```

### Percentage Difference

```javascript
const pctDiff = Math.round(
  ((currentPrice - average) / average) * 100
);
```

### Price Range

```javascript
const min = Math.min(...prices);
const max = Math.max(...prices);
const range = max - min;
```

## Confidence Scoring

### Factors Affecting Confidence

| Factor | Impact | Weight |
|--------|--------|--------|
| Data completeness (60 days vs partial) | ±15% | High |
| Price volatility (std dev) | ±10% | Medium |
| Trend strength (magnitude of change) | ±10% | Medium |
| Seasonal factors | ±5% | Low |

### Confidence Calculation

```javascript
function calculateConfidence(priceHistory, trend, recommendation) {
  let confidence = 70; // Base confidence

  // Full data bonus
  if (priceHistory.length >= 60) confidence += 10;

  // Strong trend bonus
  const prices = priceHistory.map(p => p.price);
  const recentAvg = prices.slice(-7).reduce((a, b) => a + b) / 7;
  const earlierAvg = prices.slice(-14, -7).reduce((a, b) => a + b) / 7;
  const trendStrength = Math.abs(recentAvg - earlierAvg) / earlierAvg;

  if (trendStrength > 0.10) confidence += 10;  // Strong trend
  else if (trendStrength > 0.05) confidence += 5;

  // Low volatility bonus
  const stdDev = calculateStdDev(prices);
  const cv = stdDev / average;  // Coefficient of variation
  if (cv < 0.10) confidence += 10;  // Stable prices

  return Math.min(Math.max(confidence, 50), 95);  // Clamp to 50-95
}
```

## Example Analysis

### Input Data

```javascript
const priceHistory = [
  { date: '2026-01-27', price: 1450 },
  { date: '2026-01-28', price: 1480 },
  // ... more days
  { date: '2026-03-26', price: 1299 }
];
```

### Analysis Output

```javascript
const analysis = {
  min: 1199,
  max: 1899,
  average: 1450,
  pctDiff: -10,      // 10% below average
  level: 'low',      // Below 33rd percentile
  trend: 'falling'   // 7-day avg < previous 7-day avg
};

const recommendation = {
  action: 'buy',
  confidence: 82,
  reason: 'Current price is 10% below average with a falling trend',
  currentPrice: 1299,
  averagePrice: 1450,
  expectedDrop: 0
};
```

## Edge Cases

### Insufficient Data

```javascript
if (priceHistory.length < 7) {
  return {
    level: 'mid',
    trend: 'stable',
    confidence: 50,
    reason: 'Insufficient historical data for analysis'
  };
}
```

### Missing Current Price

```javascript
if (!currentPrice || currentPrice <= 0) {
  throw new Error('Invalid current price');
}
```

### Extreme Outliers

For prices outside 3 standard deviations:

```javascript
const outlierThreshold = average + (3 * stdDev);
if (currentPrice > outlierThreshold) {
  // Cap the displayed price for chart scaling
  displayPrice = outlierThreshold;
}
```
