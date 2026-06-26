# Price Trend Skill 使用示例

## AI/Agent 集成示例

### 场景 1: 航班推荐后自动添加价格趋势

```javascript
// AI Agent 处理流程示例

async function handleFlightInquiry(userQuery, origin, destination, date) {
  // 1. 调用航班搜索 API
  const flights = await searchFlights({ origin, destination, date });

  // 2. 调用价格趋势 API 获取历史数据
  const priceInsights = await fetchPriceTrend({ origin, destination });

  // 3. 构建 AI 响应
  const response = {
    role: 'assistant',
    content: `
## 为您推荐飞往 ${destination} 的航班

根据您的要求，我找到了以下 ${flights.length} 个航班选项：

${renderFlightCards(flights)}

---

## 价格趋势分析

![价格趋势图](embed:PriceChart)

当前价格为 **¥${priceInsights.lowestPrice}**，比过去 60 天的平均价格低 ${calculatePctDiff(priceInsights)}%。

从走势图可以看出，最近两周价格呈下降趋势，现在是比较好的购买时机。

### 购买建议
- ✅ **建议现在购买** - 当前价格处于低位
- 📉 近 7 天平均价格下降了约 8%
- 💰 相比最高价可节省约 ¥600
`,
    data: {
      type: 'flights',
      flights: flights,
      priceInsights: priceInsights,
      searchParams: { origin, destination }
    }
  };

  return response;
}
```

### 场景 2: 用户询问价格走势

```javascript
// 用户：东京机票最近价格怎么样？

async function handlePriceInquiry(destination) {
  const priceData = await fetchPriceTrend({ destination });

  const response = {
    role: 'assistant',
    content: `
## ${destination} 价格趋势

![价格趋势图](embed:PriceChart)

### 关键数据
| 指标 | 价格 |
|------|------|
| 当前价 | ¥${priceData.lowestPrice} |
| 60 天均价 | ¥${priceData.analysis.average} |
| 最低价 | ¥${priceData.analysis.min} |
| 最高价 | ¥${priceData.analysis.max} |

### 分析结论
当前价格 ${getPriceLevelText(priceData.priceLevel)}，${getTrendText(priceData.trend)}。

${generateRecommendation(priceData)}
`,
    data: {
      type: 'price_trend',
      priceInsights: priceData
    }
  };

  return response;
}
```

### 场景 3: 购买建议生成

```javascript
// 用户：现在买还是再等等？

async function handleBuyWaitRecommendation(destination) {
  const priceData = await fetchPriceTrend({ destination });
  const recommendation = generateRecommendation(priceData);

  const response = {
    role: 'assistant',
    content: `
## 购买建议：${recommendation.action === 'buy' ? '✅ 现在购买' : '⏳ 继续观望'}

![价格趋势图](embed:PriceChart)

### 理由
${recommendation.reason}

### 数据支持
- 当前价格：¥${priceData.lowestPrice}
- 历史均价：¥${priceData.analysis.average}
- 价格水位：${getPriceLevelText(priceData.priceLevel)}
- 近期趋势：${getTrendText(priceData.trend)}
- 置信度：${recommendation.confidence}%

${recommendation.action === 'wait' ? `
### 建议等待至
预计 ${recommendation.waitUntil} 前后可能出现更好的价格，
届时预计价格约为 ¥${recommendation.expectedPrice}。
` : ''}
`,
    data: {
      type: 'recommendation',
      recommendation: recommendation,
      priceInsights: priceData
    }
  };

  return response;
}
```

## 完整对话示例

### 示例 1: 航班搜索 + 价格趋势

```
用户：我想下周去东京，有什么航班推荐？

AI: 好的，为您搜索从上海到东京的航班...

## 航班推荐

为您找到以下 3 个航班选项：

┌─────────────────────────────────────┐
│ 中国东方航空 MU523                │
│ 08:30 浦东 - 12:30 成田            │
│ 3 小时 直飞                        │
│ ¥1,299 起  │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ 春秋航空 9J851                     │
│ 14:20 浦东 - 18:10 成田            │
│ 2 小时 55 分 直飞                     │
│ ¥899 起  │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ 全日空 NH938                        │
│ 10:00 浦东 - 13:50 羽田            │
│ 2 小时 50 分 直飞                     │
│ ¥1,599 起  │
└─────────────────────────────────────┘

## 价格趋势分析

![价格趋势图]

当前价格为 **¥899**，比过去 60 天的平均价格低 **15%**。

从走势图可以看出，春秋航空的价格一直很稳定，
而全日空和东航的价格波动较大。

### 购买建议
- ✅ **建议现在购买** - 春秋航空价格处于低位
- 📉 近 7 天平均价格下降了约 5%
- 💰 相比最高价可节省约 ¥400

需要我帮您预订哪个航班？
```

### 示例 2: 纯价格咨询

```
用户：最近去曼谷的机票贵吗？

AI: 让我为您查看曼谷航班的价格趋势...

## 曼谷价格趋势

![价格趋势图]

### 当前价格水位
| 指标 | 价格 |
|------|------|
| 当前最低价 | ¥1,199 |
| 60 天均价 | ¥1,450 |
| 最低记录 | ¥999 |
| 最高记录 | ¥2,100 |

### 分析结论
当前价格 **低于平均水平** 约 17%，处于比较划算的区间。

从趋势图可以看到，每年 3-4 月是泰国旅游淡季，
价格相对较低。如果您时间灵活，现在是很好的入手时机。

### 推荐航班
- 东方航空：¥1,199（直飞，3.5 小时）
- 春秋航空：¥999（直飞，3 小时 40 分）

需要我帮您查看具体航班信息吗？
```

## 前端集成代码示例

### React 组件集成

```jsx
import { PriceChart, convertPriceInsights } from './price-trend';

function AIResponseRenderer({ message }) {
  const { content, data } = message;

  // 渲染航班卡片
  function renderFlightCards(flights) {
    return flights.map(flight => (
      <FlightCard key={flight.id} flight={flight} />
    ));
  }

  // 渲染价格趋势图
  function renderPriceChart() {
    if (!data?.priceInsights) return null;

    const chartProps = convertPriceInsights(
      data.priceInsights,
      data.searchParams
    );

    if (!chartProps) return null;

    return (
      <div className="price-trend-section">
        <h3>价格趋势分析</h3>
        <PriceChart {...chartProps} />
      </div>
    );
  }

  return (
    <div className="ai-response">
      <div
        className="markdown-content"
        dangerouslySetInnerHTML={{ __html: renderMarkdown(content) }}
      />

      {data?.type === 'flights' && (
        <div className="flight-section">
          {renderFlightCards(data.flights)}
        </div>
      )}

      {renderPriceChart()}
    </div>
  );
}
```

### 纯 HTML 集成

```html
<div id="ai-response">
  <!-- AI 文本内容 -->
  <div class="markdown-content">
    <!-- markdown 渲染的内容 -->
  </div>

  <!-- 航班卡片容器 -->
  <div id="flight-cards"></div>

  <!-- 价格趋势图容器 -->
  <div id="price-chart"></div>
</div>

<script>
  // 渲染响应
  function renderResponse(responseData) {
    const { content, data } = responseData;

    // 渲染 markdown 文本
    document.querySelector('.markdown-content').innerHTML =
      renderMarkdown(content);

    // 渲染航班卡片
    if (data?.flights) {
      document.getElementById('flight-cards').innerHTML =
        renderFlightCards(data.flights);
    }

    // 渲染价格趋势图
    if (data?.priceInsights) {
      const chartData = convertPriceInsights(
        data.priceInsights,
        data.searchParams
      );
      renderPriceChart('price-chart', chartData);
    }
  }

  // 从 API 获取响应
  fetch('/api/chat', {
    method: 'POST',
    body: JSON.stringify({ message: '我想去东京' })
  })
  .then(res => res.json())
  .then(renderResponse);
</script>
```

## 注意事项

1. **数据格式统一**: 确保后端返回的 `priceInsights` 格式一致
2. **错误处理**: 当价格数据不可用时，显示友好提示
3. **加载状态**: 在数据加载时显示骨架屏或 loading 动画
4. **响应式设计**: 组件已适配移动端，但需确保容器宽度正确
