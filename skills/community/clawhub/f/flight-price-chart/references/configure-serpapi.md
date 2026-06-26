# 配置 SerpAPI 获取真实价格数据

## 快速开始

### 1. 申请 SerpAPI Key

SerpAPI 提供 Google Flights 数据访问，用于获取真实航班价格。

**注册地址**: https://serpapi.com/users/sign_up

- 免费计划：100 次搜索/月
- 入门计划：$50/月，5000 次搜索/月
- 学生计划：联系官方申请折扣

### 2. 配置 API Key

在 `price/config.json` 中添加你的 SerpAPI Key：

```json
{
  "openai": {
    "apiKey": "sk-xxx",
    "baseURL": "https://..."
  },
  "serpapi": {
    "apiKey": "你的 SerpAPI Key"
  },
  "flyai": {
    "apiKey": ""
  }
}
```

### 3. 重启服务

```bash
cd price
node server.js
```

### 4. 验证配置

访问 http://localhost:3001 测试航班搜索，确认能获取真实价格数据。

---

## 数据流说明

### 配置前（模拟数据）

```
用户查询 → AI → generateMockPriceHistory() → 估算价格
```

### 配置后（真实数据）

```
用户查询 → AI → SerpAPI → 真实航班价格
                ↓
         价格收集存储
                ↓
         历史价格数据库
```

---

## 价格数据收集

配置 SerpAPI 后，系统会自动收集每次搜索的价格数据：

### 存储位置

```
price/data/price-history/
├── PVG-TYO.json      # 上海 - 东京航线
├── PVG-BKK.json      # 上海 - 曼谷航线
└── ...
```

### 数据格式

```json
[
  {
    "origin": "PVG",
    "destination": "TYO",
    "date": "2026-03-26T10:30:00.000Z",
    "lowestPrice": 1299,
    "averagePrice": 1450,
    "flightCount": 5
  },
  {
    "origin": "PVG",
    "destination": "TYO",
    "date": "2026-03-27T14:20:00.000Z",
    "lowestPrice": 1350,
    "averagePrice": 1480,
    "flightCount": 4
  }
]
```

---

## 置信度说明

随着数据积累，价格趋势的置信度会提升：

| 数据天数 | 置信度 | AI 文案示例 |
|----------|--------|-------------|
| < 7 天 | 低 | "价格数据为估算值，仅供参考" |
| 7-29 天 | 中 | "根据部分真实价格数据..." |
| 30+ 天 | 高 | "根据积累的真实价格数据..." |

---

## AI Agent 集成示例

```javascript
// 1. 调用航班搜索（使用 SerpAPI）
const flights = await flyai('search-flight', {
  origin: 'PVG',
  destination: 'TYO',
  departureDate: '2026-04-15'
});

// 2. 获取价格趋势
const priceTrend = await getPriceTrend('PVG', 'TYO');

// 3. 根据置信度生成文案
let disclaimer = '';
if (priceTrend.confidence === 'low') {
  disclaimer = '\n\n> 注：价格数据为估算值，仅供参考';
} else if (priceTrend.confidence === 'medium') {
  disclaimer = `\n\n> 注：基于过去${priceTrend.days}天的真实价格数据`;
} else {
  disclaimer = `\n\n> 注：基于过去${priceTrend.days}天的真实价格数据`;
}

// 4. 构建完整响应
return `
为您推荐以下航班：
${renderFlightCards(flights)}

## 价格趋势
${renderPriceChart(priceTrend)}
${disclaimer}
`;
```

---

## 常见问题

### Q: 免费计划够用吗？

A: 免费计划 100 次/月，适合：
- 开发测试
- 低频使用场景
- 演示/原型

如果需要更高频次，考虑：
1. 升级到付费计划
2. 使用缓存减少重复请求
3. 结合 FlyAI 的 MCP 服务

### Q: 数据多久更新一次？

A: 每次用户搜索航班时都会获取最新价格并存储。

### Q: 可以只使用模拟数据吗？

A: 可以。如果不配置 SerpAPI Key，系统会降级到模拟数据模式。

---

## 相关文档

- [SerpAPI 官方文档](https://serpapi.com/)
- [Google Flights API](https://serpapi.com/google-flights-api)
- [price-trend Skill 使用指南](../README.md)
- [数据源方案说明](./data-sources.md)
