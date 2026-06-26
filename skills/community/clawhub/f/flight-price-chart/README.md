# Price Trend Skill

将价格趋势模块嵌入到 AI 对话中的 Skill，适用于 AI/Agent 开发场景。

## 应用场景

当 AI 吐出的回答中**带有确定 OD（Origin-Destination）的航班推荐**时，在对话的最后加上这个价格趋势模块。

### 典型流程

```
用户询问：我想去东京，有什么航班？
    ↓
AI 调用航班搜索 API
    ↓
AI 返回航班推荐列表（确定 OD: SHA-TYO）
    ↓
AI 调用价格趋势 API 获取历史数据
    ↓
AI 在回答末尾嵌入 PriceChart 组件
    ↓
用户看到：航班卡片 + 价格趋势图 + 购买建议
```

## 目录结构

```
price-trend/
├── SKILL.md                          # Skill 描述和元数据
├── README.md                         # 本文件
├── references/
│   ├── price-chart-component.md      # 组件 API 文档
│   ├── price-api.md                  # 数据 API 文档
│   └── price-analysis.md             # 价格分析逻辑
└── components/
    ├── PriceTrendEmbed.jsx           # React 版本组件
    └── PriceTrendEmbed.html          # 纯 HTML/JS 版本
```

## 集成方式

### 方式 1: React 环境

```jsx
import { PriceChart, convertPriceInsights } from './price-trend';

// 假设从 AI 响应中获得的数据
const priceInsights = {
  priceHistory: [[1706227200, 1450], [1706313600, 1380], ...],
  lowestPrice: 1299,
  priceLevel: 'low'
};

const searchParams = {
  origin: 'SHA',
  destination: 'TYO'
};

// 转换数据格式
const chartProps = convertPriceInsights(priceInsights, searchParams);

// 渲染组件
<PriceChart {...chartProps} />
```

### 方式 2: 纯 HTML/JS 环境

```html
<div id="price-chart"></div>

<script src="PriceTrendEmbed.html"></script>
<script>
  const chartData = convertPriceInsights(priceInsights, searchParams);
  renderPriceChart('price-chart', chartData);
</script>
```

## 数据格式

### 输入：priceInsights

```typescript
interface PriceInsights {
  priceHistory: [number, number][];  // [[timestamp, price], ...]
  lowestPrice: number;
  priceLevel: 'low' | 'typical' | 'high';
}
```

### 输出：Chart Props

```typescript
interface ChartProps {
  data: Array<{ date: string; price: number }>;
  currentPrice: number;
  analysis: {
    min: number;
    max: number;
    average: number;
    pctDiff: number;
    level: 'low' | 'mid' | 'high';
    trend: 'falling' | 'rising' | 'stable';
  };
  destination: { code: string };
}
```

## AI 响应模板

当 AI 返回航班推荐时，建议使用以下结构：

```markdown
## 航班推荐

为您找到以下飞往 **{destination}** 的航班：

[FlightCards 组件 - 3-5 个航班选项]

## 价格分析

当前价格 **¥{currentPrice}**，比 60 天均价低 {pctDiff}%。

[PriceChart 组件]

## 购买建议

{recommendation}

- **当前价格**: ¥{currentPrice}
- **历史均价**: ¥{average}
- **建议**: {buy/wait}
```

## 视觉效果

```
┌─────────────────────────────────────────┐
│ 近 60 天价格走势        ¥1,299  -10% vs 均价│
│                                         │
│ ↓ 低于均价    → 走势平稳                 │
│                                         │
│  ╭────────────────────────────────╮      │
│  │    价格趋势曲线 (可交互)        │      │
│  ╰────────────────────────────────╯      │
│  均价 ¥1,450                              │
│                                         │
│  1/26          2/26          3/26        │
│                                         │
│ ┌─────────┬─────────┬─────────┐         │
│ │ 最低价  │ 平均价  │ 最高价  │         │
│ │ ¥1,199  │ ¥1,450  │ ¥1,899  │         │
│ └─────────┴─────────┴─────────┘         │
└─────────────────────────────────────────┘
```

## 与 flyai 配合使用

```javascript
// 1. 调用 flyai 搜索航班
const flights = await flyai('search-flight', {
  origin: 'SHA',
  destination: 'TYO',
  departureDate: '2026-04-15'
});

// 2. 提取 OD 对
const odPair = { origin: 'SHA', destination: 'TYO' };

// 3. 调用价格趋势 API
const priceData = await fetchPriceTrend(odPair);

// 4. 构建 AI 响应
const response = `
为您推荐以下航班：
${renderFlightCards(flights)}

## 价格走势

${renderPriceChart(priceData)}

当前价格低于平均水平，建议现在购买。
`;
```

## 数据源说明

### 快速配置真实数据

当前实现中，价格历史数据默认使用**模拟数据**（仅供 Demo/开发）。

**要获取真实价格数据**，只需配置 SerpAPI Key：

1. 访问 https://serpapi.com/users/sign_up 注册账号
2. 在 `price/config.json` 中添加你的 API Key：
   ```json
   {
     "serpapi": {
       "apiKey": "你的 SerpAPI Key"
     }
   }
   ```
3. 重启服务：`node server.js`

详细配置指南见：[`references/configure-serpapi.md`](./references/configure-serpapi.md)

### 数据流说明

```
配置前：用户查询 → 模拟数据生成器 → 估算价格
配置后：用户查询 → SerpAPI → 真实价格 → 自动存储积累
```

### 置信度标识

随着数据积累，AI 响应时标注不同置信度：

| 数据天数 | 置信度 | AI 文案 |
|----------|--------|---------|
| < 7 天 | 低 | "价格数据为估算值，仅供参考" |
| 7-29 天 | 中 | "根据部分真实价格数据..." |
| 30+ 天 | 高 | "根据积累的真实价格数据..." |

详见：[`references/data-sources.md`](./references/data-sources.md)

## 注意事项

1. **数据隐私**: 确保价格数据来源于合法渠道
2. **实时更新**: 价格数据应定期刷新（建议每 6 小时）
3. **错误处理**: 当价格数据不可用时，优雅降级显示
4. **移动端适配**: 组件已针对手机屏幕优化（最大宽度 480px）
5. **数据透明度**: 向用户说明数据来源（真实/估算）

## 开发调试

### 本地测试 React 组件

```bash
cd price-trend/components
# 在 React 项目中引用 PriceTrendEmbed.jsx
```

### 本地测试 HTML 版本

```bash
cd price-trend/components
open PriceTrendEmbed.html
```

## 未来规划

- [ ] 支持多目的地比价
- [ ] 添加价格提醒功能
- [ ] 支持更长时间范围（90 天/180 天）
- [ ] 增加预测功能（基于机器学习）
