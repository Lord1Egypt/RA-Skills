# 价格分析算法文档

## 概述

本文档详细说明 price-summary skill 的价格分析算法逻辑。

## 输入数据

```typescript
interface PriceData {
  currentPrice: number;        // 当前价格
  priceHistory: PricePoint[];  // 历史价格数组
  route: {
    origin: string;
    destination: string;
  };
}

interface PricePoint {
  date: string;   // ISO 日期格式
  price: number;  // 价格
}
```

## 算法步骤

### 1. 基础统计值计算

```javascript
function calculateStats(prices) {
  const min = Math.min(...prices);
  const max = Math.max(...prices);
  const avg = prices.reduce((sum, p) => sum + p, 0) / prices.length;
  
  return { min, max, avg };
}
```

### 2. 价格水位判断（百分位法）

```javascript
function getPriceLevel(currentPrice, avg) {
  const pctDiff = ((currentPrice - avg) / avg) * 100;
  
  if (pctDiff < -15) return { level: 'low', label: '低价', emoji: '🟢' };
  if (pctDiff > 15) return { level: 'high', label: '高价', emoji: '🔴' };
  return { level: 'mid', label: '均价', emoji: '🟡' };
}
```

**阈值说明**：
- 低价：低于均价 15% 以上
- 高价：高于均价 15% 以上
- 中价：均价±15% 以内

### 3. 趋势检测（7 日移动平均）

```javascript
function detectTrend(prices) {
  if (prices.length < 14) {
    return { trend: 'unknown', label: '数据不足' };
  }
  
  const recent7 = prices.slice(-7).reduce((a, b) => a + b, 0) / 7;
  const previous7 = prices.slice(-14, -7).reduce((a, b) => a + b, 0) / 7;
  
  const change = ((recent7 - previous7) / previous7) * 100;
  
  if (change < -5) return { trend: 'falling', label: '下降', emoji: '📉' };
  if (change > 5) return { trend: 'rising', label: '上升', emoji: '📈' };
  return { trend: 'stable', label: '平稳', emoji: '➡️' };
}
```

### 4. 购买建议生成

```javascript
function generateRecommendation(level, trend, daysToDeparture) {
  // 基础决策矩阵
  const baseRecommendations = {
    'low': { action: 'buy', text: '现在购买', confidence: 'high' },
    'mid': { action: 'wait', text: '可买可等', confidence: 'medium' },
    'high': { action: 'wait', text: '再等等', confidence: 'high' }
  };
  
  let rec = baseRecommendations[level];
  
  // 根据趋势调整
  if (trend === 'falling' && level === 'mid') {
    rec.text = '可以再等等，价格正在下降';
  }
  if (trend === 'rising' && level === 'mid') {
    rec.text = '建议尽早购买，价格在上涨';
  }
  
  // 根据出发日期调整（临近出发更积极）
  if (daysToDeparture <= 7) {
    if (rec.action === 'wait') {
      rec.text += '，但临近出发，建议尽早决定';
    }
  }
  
  return rec;
}
```

## 置信度评分

```javascript
function calculateConfidence(priceHistory, level) {
  const days = priceHistory.length;
  
  // 数据量置信度
  let dataConfidence = days >= 30 ? 1.0 : days >= 14 ? 0.7 : days >= 7 ? 0.4 : 0.2;
  
  // 水位明显度置信度
  let levelConfidence = level === 'low' || level === 'high' ? 0.9 : 0.6;
  
  return Math.round(dataConfidence * levelConfidence * 100);
}
```

## 边缘情况处理

### 1. 数据不足（<7 天）

```javascript
if (priceHistory.length < 7) {
  return {
    warning: '数据有限，仅供参考',
    confidence: 'low',
    level: 'unknown'
  };
}
```

### 2. 价格异常值

```javascript
function detectOutliers(prices) {
  const sorted = [...prices].sort((a, b) => a - b);
  const q1 = sorted[Math.floor(sorted.length * 0.25)];
  const q3 = sorted[Math.floor(sorted.length * 0.75)];
  const iqr = q3 - q1;
  
  const lowerBound = q1 - 1.5 * iqr;
  const upperBound = q3 + 1.5 * iqr;
  
  return prices.filter(p => p < lowerBound || p > upperBound);
}
```

### 3. 节假日影响

```javascript
function isHolidayPeriod(date) {
  const holidays = [
    '春节', '国庆', '五一', '清明', '端午', '中秋'
  ];
  // 检查日期是否在节假日前后 3 天内
  // ...
}
```

## 输出格式

```typescript
interface PriceAnalysisResult {
  currentPrice: number;
  stats: {
    min: number;
    max: number;
    avg: number;
    pctDiff: number;
  };
  level: {
    value: 'low' | 'mid' | 'high';
    label: string;
    emoji: string;
  };
  trend: {
    value: 'falling' | 'rising' | 'stable';
    label: string;
    emoji: string;
  };
  recommendation: {
    action: 'buy' | 'wait';
    text: string;
    confidence: number;
  };
  warning?: string;
}
```

## 示例

### 输入
```javascript
{
  currentPrice: 1299,
  priceHistory: [
    { date: '2026-01-01', price: 1450 },
    { date: '2026-01-02', price: 1420 },
    // ... 60 天数据
    { date: '2026-03-01', price: 1299 }
  ]
}
```

### 输出
```javascript
{
  currentPrice: 1299,
  stats: { min: 1199, max: 1899, avg: 1450, pctDiff: -10.4 },
  level: { value: 'low', label: '低价', emoji: '🟢' },
  trend: { value: 'falling', label: '下降', emoji: '📉' },
  recommendation: {
    action: 'buy',
    text: '现在购买',
    confidence: 85
  }
}
```
