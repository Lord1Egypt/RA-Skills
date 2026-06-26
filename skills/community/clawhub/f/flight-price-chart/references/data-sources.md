# 价格趋势数据源方案

## 现状分析

当前 `price/` 目录中的价格历史数据是**模拟数据**，通过 `FlightApi.generateMockPriceHistory()` 生成。

### 现有数据流

```
用户查询 → SerpAPI (航班搜索) → 实时航班价格
         ↓
         └─→ generateMockPriceHistory() → 模拟历史价格
```

## 数据源选项

### 方案 1: SerpAPI + 自建缓存 (推荐起步)

**原理**: 通过持续收集 SerpAPI 的实时价格，自建历史价格数据库

**实现**:
```javascript
// 每次航班搜索后存储价格快照
async function cachePriceData(searchParams, flights) {
  const priceRecord = {
    origin: searchParams.origin,
    destination: searchParams.destination,
    date: new Date().toISOString(),
    lowestPrice: Math.min(...flights.map(f => f.price)),
    averagePrice: flights.reduce((a, b) => a + b.price, 0) / flights.length,
    flights: flights.length,
  };

  // 存储到数据库/文件系统
  await db.priceHistory.insert(priceRecord);
}
```

**优点**:
- 不需要额外 API
- 数据积累后越来越准确
- 完全可控

**缺点**:
- 需要时间积累数据（至少 30 天才有参考价值）
- 初期数据不完整

### 方案 2: 第三方价格 API

#### 2.1 AviationStack
- URL: https://aviationstack.com/
- 提供：实时航班追踪、机场数据
- 价格：免费 + 付费层级
- **限制**: 不提供历史价格

#### 2.2 Skyscanner API
- URL: https://skyscanner.github.io/slate/
- 提供：航班搜索、价格比较
- **限制**: 需要申请合作伙伴权限

#### 2.3 Amadeus Flight API
- URL: https://developers.amadeus.com/
- 提供：航班搜索、价格分析
- 有免费层级 (2000 requests/月)
- **限制**: 历史价格数据有限

#### 2.4 飞猪/携程联盟 API
- 通过 flyai 的 MCP 服务间接获取
- 需要商务合作

### 方案 3: 混合方案 (推荐)

结合多种数据源：

```
┌─────────────────────────────────────────────────────┐
│                 价格趋势数据流                        │
├─────────────────────────────────────────────────────┤
│                                                     │
│  用户查询 → 检查本地缓存 (有历史数据？)               │
│             ↓ 是                                     │
│             返回缓存 + 更新                           │
│             ↓ 否                                     │
│         检查是否有部分历史数据                        │
│         ↓ 有            ↓ 无                         │
│    混合显示           使用模拟数据                    │
│    (真实 + 模拟)       标记"数据不足"                 │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 推荐实施路径

### 阶段 1: 模拟数据 + 数据收集 (当前 -1 个月)

```javascript
// 1. 继续使用模拟数据，但标记为"估算"
function getPriceTrend(origin, destination) {
  const historicalData = getHistoricalData(origin, destination);

  if (historicalData.days < 7) {
    return {
      ...generateMockData(origin, destination),
      disclaimer: '价格数据为估算值，仅供参考'
    };
  }

  return historicalData;
}

// 2. 后台持续收集价格数据
async function collectPriceData() {
  const popularRoutes = [
    { origin: 'PVG', destination: 'TYO' },
    { origin: 'PVG', destination: 'BKK' },
    // ... 热门航线
  ];

  for (const route of popularRoutes) {
    const flights = await searchFlights(route);
    await storePriceSnapshot(route, flights);
  }
}

// 每天执行一次
setInterval(collectPriceData, 24 * 60 * 60 * 1000);
```

### 阶段 2: 部分真实数据 (1-3 个月)

```javascript
// 当积累足够数据后
function getPriceTrend(origin, destination) {
  const historicalData = getHistoricalData(origin, destination);

  if (historicalData.days >= 30) {
    return {
      ...historicalData,
      confidence: 'high',
      label: '真实价格数据'
    };
  } else if (historicalData.days >= 7) {
    return {
      ...historicalData,
      confidence: 'medium',
      label: '部分真实数据'
    };
  }

  return {
    ...generateMockData(origin, destination),
    confidence: 'low',
    label: '估算数据'
  };
}
```

### 阶段 3: 完整数据服务 (3 个月+)

- 接入第三方 API 补充历史数据
- 或继续积累自有数据
- 提供价格预测功能

## 数据存储方案

### 简单方案：JSON 文件

```json
// data/price-history.json
{
  "PVG-TYO": [
    { "date": "2026-03-01", "lowestPrice": 1299, "averagePrice": 1450 },
    { "date": "2026-03-02", "lowestPrice": 1350, "averagePrice": 1480 }
  ],
  "PVG-BKK": [...]
}
```

### 进阶方案：SQLite

```sql
CREATE TABLE price_history (
  id INTEGER PRIMARY KEY,
  origin TEXT,
  destination TEXT,
  date TEXT,
  lowest_price INTEGER,
  average_price INTEGER,
  flight_count INTEGER,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_route ON price_history(origin, destination, date);
```

## AI Agent 集成时的注意事项

### 1. 数据置信度标识

```javascript
const priceTrend = await getPriceTrend('PVG', 'TYO');

// AI 响应时应说明数据可信度
if (priceTrend.confidence === 'low') {
  return '由于该航线历史数据有限，以下为价格估算，仅供参考...';
} else if (priceTrend.confidence === 'high') {
  return '根据我们积累的真实价格数据...';
}
```

### 2. 避免过度承诺

不要在数据不足时给出确定的购买建议：

```javascript
// ❌ 不好的文案
"现在绝对是购买的最佳时机！"

// ✅ 好的文案
"根据现有数据，当前价格低于估算均价约 10%，如有出行计划可考虑入手"
```

### 3. 数据来源透明

```markdown
### 价格趋势
![图表]

> 数据来源：基于过去 30 天收集的 {N} 个航班价格
> 置信度：高/中/低
```

## 与 flyai 配合

当使用 flyai 获取航班数据时，可以同时收集价格：

```javascript
// 调用 flyai 获取航班
const flights = await flyai('search-flight', { origin, destination });

// 提取价格数据存储
await storePriceData({
  origin,
  destination,
  flights: flights.map(f => ({
    price: f.price,
    airline: f.airline,
    date: f.departureDate
  }))
});
```

## 总结

| 方案 | 成本 | 准确度 | 实施难度 | 推荐度 |
|------|------|--------|----------|--------|
| 纯模拟数据 | 无 | 低 | 简单 | ⭐ |
| 自建缓存 (初期) | 低 | 中 | 中等 | ⭐⭐⭐ |
| 自建缓存 (长期) | 低 | 高 | 中等 | ⭐⭐⭐⭐ |
| 第三方 API | 中 - 高 | 中 - 高 | 中等 | ⭐⭐⭐ |
| 混合方案 | 灵活 | 灵活 | 中等 | ⭐⭐⭐⭐ |

**推荐**: 从自建缓存开始，逐步积累数据，必要时接入第三方 API 补充。
