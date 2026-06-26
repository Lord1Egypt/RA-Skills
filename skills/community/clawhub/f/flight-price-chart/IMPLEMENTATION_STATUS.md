# Price Trend Skill 实现状态

## 完成情况

### ✅ 已完成

#### 1. 组件实现
- [x] `PriceTrendEmbed.jsx` - React 版本可嵌入组件
- [x] `PriceTrendEmbed.html` - 纯 HTML/JS 版本（含演示）
- [x] 交互式价格趋势图表（支持 hover/touch）
- [x] 响应式设计（移动端优化）
- [x] 数据转换函数 `convertPriceInsights()`

#### 2. 文档
- [x] `SKILL.md` - Skill 元数据和快速开始
- [x] `README.md` - 总体说明和集成指南
- [x] `USAGE_EXAMPLE.md` - AI/Agent 集成示例
- [x] `references/price-chart-component.md` - 组件 API 文档
- [x] `references/price-api.md` - 数据 API 文档
- [x] `references/price-analysis.md` - 价格分析逻辑
- [x] `references/data-sources.md` - 数据源方案说明

#### 3. Skill 注册
- [x] 在 `.agents/skills/price-trend/` 创建完整结构
- [x] 在 `skills/` 目录创建符号链接

---

## 数据源状态

### 快速启用真实数据 🚀

当前实现默认使用**模拟数据**（仅供 Demo/开发）。

**要获取真实价格数据，只需 3 步**：

1. 访问 https://serpapi.com/users/sign_up 注册
2. 在 `price/config.json` 中添加 API Key
3. 重启服务

详见：[`references/configure-serpapi.md`](./references/configure-serpapi.md)

### 当前状态：模拟数据（未配置 SerpAPI 时）

```
┌─────────────────────────────────────────────┐
│  数据来源：generateMockPriceHistory()       │
│  基于：航线距离 + 随机波动 + 周期性变化       │
│  置信度：低（估算值，仅供参考）               │
└─────────────────────────────────────────────┘
```

### 现有代码位置

```
price/
├── api/
│   ├── serpapiClient.js    # SerpAPI 航班搜索（真实数据）
│   └── flightApi.js        # 统一数据接口
│       └── generateMockPriceHistory()  ← 模拟数据生成器
├── utils/
│   └── priceAnalyzer.js    # 价格分析逻辑（可用）
└── index.html              # 完整演示应用
```

### 模拟数据生成逻辑

```javascript
// 来自 flightApi.js 第 316-374 行
async generateMockPriceHistory(origin, destination) {
  // 1. 基于航线的基础价格
  const basePrices = {
    'PVG-TYO': 2500,
    'PVG-BKK': 2000,
    'PVG-SIN': 2800,
    // ...
  };

  // 2. 添加波动因素
  const weekendMultiplier = (dayOfWeek === 0 || dayOfWeek === 6) ? 1.1 : 1.0;
  const randomFluctuation = 0.8 + Math.random() * 0.4;

  // 3. 生成 30 天历史数据
  for (let i = 29; i >= 0; i--) {
    const date = new Date(today);
    date.setDate(date.getDate() - i);
    const price = Math.round(basePrice * weekendMultiplier * randomFluctuation);
    data.push({ date, price });
  }
}
```

---

## 获取真实数据的实施路径

### 阶段 1: 数据收集（立即开始）

在现有 `price/server.js` 中添加价格收集功能：

```javascript
// server.js 中添加
const fs = require('fs');
const path = require('path');

// 价格数据存储路径
const DATA_DIR = path.join(__dirname, '../data/price-history');

// 每次航班搜索后存储价格快照
app.post('/api/flights/search', async (req, res) => {
  const flights = await searchFlights(req.body);

  // 存储价格数据
  await storePriceSnapshot({
    origin: req.body.departure_id,
    destination: req.body.arrival_id,
    date: new Date().toISOString(),
    lowestPrice: Math.min(...flights.map(f => f.price)),
    averagePrice: flights.reduce((a, b) => a + b.price, 0) / flights.length,
    flightCount: flights.length,
  });

  res.json({ flights });
});

async function storePriceSnapshot(record) {
  const filePath = path.join(DATA_DIR, `${record.origin}-${record.destination}.json`);

  // 读取或创建文件
  let history = [];
  if (fs.existsSync(filePath)) {
    history = JSON.parse(fs.readFileSync(filePath, 'utf8'));
  }

  // 添加新记录
  history.push(record);

  // 去重（同一天只保留一条）
  history = history.filter((r, i, arr) =>
    arr.findIndex(x => x.date.slice(0, 10) === r.date.slice(0, 10)) === i
  );

  // 保存
  fs.writeFileSync(filePath, JSON.stringify(history, null, 2));
}
```

### 阶段 2: 读取真实数据（1-3 个月后）

```javascript
// 修改 getPriceHistory 方法
async getPriceHistory(origin, destination) {
  const filePath = path.join(DATA_DIR, `${origin}-${destination}.json`);

  // 检查是否有本地数据
  if (fs.existsSync(filePath)) {
    const history = JSON.parse(fs.readFileSync(filePath, 'utf8'));

    // 数据足够 30 天
    if (history.length >= 30) {
      return {
        data: history.map(r => ({
          date: r.date.slice(0, 10),
          price: r.lowestPrice
        })),
        average: Math.round(history.reduce((a, b) => a + b.averagePrice, 0) / history.length),
        min: Math.min(...history.map(r => r.lowestPrice)),
        max: Math.max(...history.map(r => r.lowestPrice)),
        confidence: 'high',
        source: 'real'
      };
    }

    // 数据不足 30 天但至少有 7 天
    if (history.length >= 7) {
      return {
        // ... 部分真实数据
        confidence: 'medium',
        source: 'partial'
      };
    }
  }

  // 没有足够数据，使用模拟数据
  return {
    // ... generateMockPriceHistory()
    confidence: 'low',
    source: 'estimated',
    disclaimer: '价格数据为估算值，仅供参考'
  };
}
```

### 阶段 3: AI 响应时的透明度

```javascript
// AI Agent 根据置信度调整文案
function generateResponse(priceTrend) {
  if (priceTrend.confidence === 'low') {
    return `
由于该航线历史数据有限，以下为价格估算，仅供参考。

${renderPriceChart(priceTrend)}

> 数据来源：基于航线距离估算
> 置信度：低（数据积累中）
`;
  } else if (priceTrend.confidence === 'high') {
    return `
根据我们积累的真实价格数据（过去${priceTrend.days}天）：

${renderPriceChart(priceTrend)}

> 数据来源：实际航班搜索记录
> 置信度：高
`;
  }
}
```

---

## 推荐下一步行动

### 立即可做

1. **启用数据收集**
   - 在 `price/server.js` 中添加价格存储逻辑
   - 创建 `price/data/price-history/` 目录
   - 开始积累真实数据

2. **添加置信度标识**
   - 修改 `convertPriceInsights()` 返回置信度
   - 在 AI 响应中标注"估算"或"真实"

3. **定期收集任务**
   ```javascript
   // 每天凌晨 2 点收集热门航线价格
   cron.schedule('0 2 * * *', async () => {
     const popularRoutes = [
       { origin: 'PVG', destination: 'TYO' },
       { origin: 'PVG', destination: 'BKK' },
       { origin: 'PVG', destination: 'SIN' },
     ];

     for (const route of popularRoutes) {
       const flights = await searchFlights(route);
       await storePriceSnapshot(route, flights);
     }
   });
   ```

### 中长期

1. **接入第三方 API**（如需要）
   - Amadeus Flight API（免费 2000 次/月）
   - 用于补充历史数据

2. **价格预测功能**
   - 基于积累的数据训练简单模型
   - 提供"预计降价时间"建议

---

## 文件清单

```
.agents/skills/price-trend/
├── SKILL.md                          ✅ 完成
├── README.md                         ✅ 完成（含数据源说明）
├── USAGE_EXAMPLE.md                  ✅ 完成
├── IMPLEMENTATION_STATUS.md          ✅ 本文件
├── references/
│   ├── price-chart-component.md      ✅ 完成
│   ├── price-api.md                  ✅ 完成
│   ├── price-analysis.md             ✅ 完成
│   └── data-sources.md               ✅ 完成
└── components/
    ├── PriceTrendEmbed.jsx           ✅ 完成
    └── PriceTrendEmbed.html          ✅ 完成（含演示）
```

---

## 总结

**Price Trend Skill** 的组件实现和文档已完成，当前可以使用，但需要注意：

1. **数据源是模拟数据** - 基于航线距离和随机波动生成，非真实历史价格
2. **建议立即开始收集真实数据** - 在 `price/server.js` 中添加存储逻辑
3. **AI 响应时应标注置信度** - 告知用户数据是"估算"还是"真实"

随着数据积累，置信度会逐渐提高，最终可以提供准确的价格趋势分析。
