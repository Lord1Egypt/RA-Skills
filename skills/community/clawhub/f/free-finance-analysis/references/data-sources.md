# 数据源详细说明

## 美股数据源

### CNBC ⭐⭐⭐
**URL**: `https://www.cnbc.com/quotes/{SYMBOL}`

**提供**:
- 实时股价（盘前/盘中/盘后）
- 52周高低点
- 市值、P/E、EPS、营收
- 毛利率、净利率、ROE
- 股息率、Beta

**常用Symbol**:
- 科技七巨头: GOOGL, AAPL, MSFT, NVDA, AMZN, META, TSLA
- 金融: JPM, BAC, GS
- 消费: KO, PEP, MCD, NKE

### Benzinga ⭐⭐⭐
**URL**: `https://www.benzinga.com/quote/{SYMBOL}`

**提供**:
- **RSI**（关键！）
- 分析师评级分布
- 目标价共识
- 做空比例

### 老虎社区 ⭐⭐
**URL**: `https://www.laohu8.com/stock/{SYMBOL}`

**提供**:
- 中文投资者讨论
- 散户实操观点
- 估值分析

**适用**: 了解散户情绪

### Motley Fool ⭐⭐
**URL**: `https://www.fool.com/quote/nasdaq/{symbol}/`

**提供**:
- 季度财务数据
- 同比变化
- 现金流

---

## A股数据源

### 东方财富
**URL**: `https://finance.eastmoney.com/`

**提供**: A股行情、财务数据、研报

### 雪球
**URL**: `https://xueqiu.com/S/{SYMBOL}`

**提供**: 投资者讨论

---

## 财经新闻

### 金十数据 ⭐⭐⭐
**URL**: `https://www.jin10.com/`

**提供**:
- 实时快讯
- 央行动态
- 大宗商品行情

---

## 大宗商品

### 世界黄金协会
**URL**: `https://www.gold.org/`

**提供**:
- 黄金季度供需报告
- 央行购金数据
- ETF持仓

**报告路径**: `/goldhub/research/gold-demand-trends/gold-demand-trends-q{n}-{year}`

---

## 使用技巧

### 1. 数据源优先级

| 需求 | 首选 | 备选 |
|------|------|------|
| 行情 | CNBC | Benzinga |
| RSI | Benzinga | - |
| 中文观点 | 老虎社区 | 雪球 |
| 快讯 | 金十数据 | - |
| 黄金 | 世界黄金协会 | 金十数据 |

### 2. 失效处理

如果web_fetch失败：
1. 换数据源
2. 检查URL是否正确
3. 可能是网站限制，稍后再试

### 3. 数据时效

- 盘中数据：实时
- 盘后数据：可能有延迟
- 注意标注数据时间

### 4. 区分事实与观点

| 类型 | 来源 | 可信度 |
|------|------|--------|
| 事实 | CNBC、财报 | 高 |
| 观点 | 老虎、雪球 | 中，需判断 |
| 预测 | 分析师评级 | 中，有偏差 |

---

## 常见问题

### Q: Seeking Alpha能用吗？
A: 可以，但部分内容需付费。URL: `https://seekingalpha.com/symbol/{SYMBOL}`

### Q: 机构持仓哪里查？
A: WhaleWisdom (`https://whalewisdom.com/`) 但可能访问不了。更简单的方法是看新闻（金十数据会报道木头姐等机构动向）

### Q: 港股怎么查？
A: 老虎社区支持港股，或用富途
