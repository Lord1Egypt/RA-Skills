# PriceChart Component Reference

## Overview

The `PriceChart` component renders an interactive 60-day price trend chart for flight prices. It supports hover (desktop) and touch (mobile) interactions to display daily prices.

## Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `data` | `Array<{date: string, price: number}>` | Yes | 60-day price history data |
| `currentPrice` | `number` | Yes | Current flight price to highlight |
| `analysis` | `AnalysisResult` | Yes | Price analysis metrics |
| `destination` | `{code: string, name?: string}` | Yes | Destination airport/city code |

## AnalysisResult Type

```typescript
interface AnalysisResult {
  min: number;        // Minimum price in period
  max: number;        // Maximum price in period
  average: number;    // Average price
  pctDiff: number;    // Percentage difference from average
  level: PriceLevel;  // Price level indicator
  trend: TrendDirection; // Trend direction
}

type PriceLevel = 'low' | 'mid' | 'high';
type TrendDirection = 'falling' | 'rising' | 'stable';
```

## Usage Example

```jsx
import { PriceChart } from './price-trend';

const chartData = {
  data: [
    { date: "2026-01-26", price: 1450 },
    { date: "2026-01-27", price: 1380 },
    // ... more days
    { date: "2026-03-26", price: 1299 }
  ],
  currentPrice: 1299,
  analysis: {
    min: 1199,
    max: 1899,
    average: 1450,
    pctDiff: -10,
    level: 'low',
    trend: 'falling'
  },
  destination: { code: 'TYO', name: 'Tokyo' }
};

<PriceChart {...chartData} />
```

## Visual Structure

```
┌─────────────────────────────────────────┐
│ 近 60 天价格走势        ¥1,299  -10% vs 均价│
│                                         │
│ ↓ 低于均价    → 走势平稳                 │
│                                         │
│  ╭────────────────────────────────╮      │
│  │     ╭───╮                      │      │
│  │    ╱     ╰──╮                  │      │
│  │   ╱         ╰───╮              │      │
│  │  ╱              ╰────●         │      │
│  │ ╱                          ╲   │      │
│  ╰────────────────────────────────╯      │
│  均价 ¥1,450                              │
│                                         │
│  1/26          2/26          3/26        │
│                                         │
│ ┌─────────┬─────────┬─────────┐         │
│ │ 最低价  │ 平均价  │ 最高价  │         │
│ │ ¥1,199  │ ¥1,450  │ ¥1,899  │         │
│ └─────────┴─────────┴─────────┘         │
│                                         │
│ 👆 滑动查看每日价格                       │
└─────────────────────────────────────────┘
```

## Features

### 1. Interactive Tooltip
- Hover/touch anywhere on chart to show price for that date
- Crosshair line follows pointer
- Tooltip shows date and price
- Highlighted dot at pointer position

### 2. Average Price Line
- Dashed horizontal line at average price level
- Label showing exact average value
- Helps users quickly compare current vs average

### 3. Price Level Badges
- "低于均价" (Below average) - Green badge
- "价格适中" (Mid price) - Gray badge
- "高于均价" (Above average) - Red badge
- Trend indicator: 📈/📉/➡️

### 4. Statistics Footer
- Three-column layout showing min/avg/max
- Centered alignment
- Clear typography for numbers

## CSS Variables

The component uses these CSS variables for theming:

```css
:root {
  --brand: #6666FF;          /* Primary brand color */
  --brand-light: #8888FF;
  --brand-bg: #F0EFFF;

  --price-low: #16A571;      /* Low price color */
  --price-low-bg: #F0FAF6;
  --price-mid: #666666;      /* Mid price color */
  --price-mid-bg: #F7F7F8;
  --price-high: #E54D4D;     /* High price color */
  --price-high-bg: #FFF5F5;

  --text-1: #1A1A1A;         /* Primary text */
  --text-2: #333333;
  --text-3: #666666;
  --text-4: #999999;
  --text-5: #CCCCCC;

  --border: #EEEEEE;
  --border-light: #F5F5F5;

  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;

  --font-num: 'DM Sans', -apple-system, sans-serif;
}
```

## Responsive Behavior

- **Desktop**: Hover interaction with mouse
- **Mobile**: Touch interaction, swipe to explore
- **Chart height**: Fixed 160px
- **Width**: 100% of container
- **Max container width**: 480px (mobile-first design)

## Accessibility

- Touch targets minimum 44x44px
- Color contrast meets WCAG AA
- Screen reader friendly labels
- Keyboard navigation support (future enhancement)

## Performance Considerations

- Uses `useMemo` for path calculations
- `ResizeObserver` for responsive sizing
- No external charting library dependencies
- SVG-based rendering for crisp graphics
