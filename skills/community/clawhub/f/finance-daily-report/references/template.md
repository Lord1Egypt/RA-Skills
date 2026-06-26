# 日报模板（9 模块标准结构）

## 文档结构

```markdown
# 全球财经日报 | YYYY 年 MM 月 DD 日

> 数据截至：YYYY-MM-DD HH:MM (Asia/Shanghai)

---

## 市场主线

{一段式叙述，概括当日全球市场最大主线事件，200-300 字}

---

## 全球宏观速览

{叙述 + 要点列表，涵盖主要经济体最新宏观数据/政策动向}

**关键数据：**
- 美国：{CPI/非农/GDP 等最新数据}【[来源](URL)】
- 中国：{PMI/社融/CPI 等最新数据}【[来源](URL)】
- 欧元区：{通胀/PMI 等最新数据}【[来源](URL)】

---

## 汇率与美元

{简要叙述美元走势及驱动因素}

| 货币对 | 收盘价 | 日涨跌幅 | 来源 |
|--------|--------|----------|------|
| DXY | 103.82 | -0.15% | [TE](https://tradingeconomics.com/united-states/currency) |
| EUR/USD | 1.0878 | +0.12% | [TE](https://tradingeconomics.com/euro-area/currency) |
| USD/CNY | 7.2345 | +0.08% | [TE](https://tradingeconomics.com/china/currency) |
| USD/JPY | 148.52 | -0.23% | [TE](https://tradingeconomics.com/japan/currency) |

---

## 全球利率与美债

{简要叙述美债收益率走势及驱动因素}

| 国债 | 收益率 | 日变化 | 来源 |
|------|--------|--------|------|
| 美国 2Y | 4.32% | +0.05 | [TE](https://tradingeconomics.com/united-states/government-bond-yield) |
| 美国 10Y | 4.58% | +0.03 | [TE](https://tradingeconomics.com/united-states/government-bond-yield) |
| 美国 30Y | 4.72% | +0.02 | [TE](https://tradingeconomics.com/united-states/government-bond-yield) |
| 中国 10Y | 2.31% | -0.01 | [TE](https://tradingeconomics.com/china/government-bond-yield) |

---

## 核心股市表现

{简要叙述全球主要股指表现}

| 指数 | 收盘价 | 日涨跌幅 | 来源 |
|------|--------|----------|------|
| 标普 500 | 5,521.52 | -1.39% | [TE](https://tradingeconomics.com/united-states/stock-market) |
| 道琼斯 | 41,488.19 | -1.28% | [TE](https://tradingeconomics.com/united-states/stock-market) |
| 纳斯达克 | 17,234.89 | -1.52% | [TE](https://tradingeconomics.com/united-states/stock-market) |
| 沪深 300 | 3,456.78 | +0.45% | [TE](https://tradingeconomics.com/china/stock-market) |
| 恒生指数 | 16,789.23 | -0.67% | [TE](https://tradingeconomics.com/hong-kong/stock-market) |
| 日经 225 | 38,234.56 | +0.89% | [TE](https://tradingeconomics.com/japan/stock-market) |

---

## 商品与核心资产

{简要叙述大宗商品及核心资产走势}

| 品种 | 价格 | 日涨跌幅 | 来源 |
|------|------|----------|------|
| WTI 原油 | $66.55 | -1.12% | [TE](https://tradingeconomics.com/commodity/crude-oil) |
| Brent 原油 | $70.23 | -0.98% | [TE](https://tradingeconomics.com/commodity/brent) |
| 黄金 | $2,988.50 | +0.45% | [TE](https://tradingeconomics.com/commodity/gold) |
| 白银 | $32.45 | +0.78% | [TE](https://tradingeconomics.com/commodity/silver) |
| 铜 | $8,567.00 | -0.34% | [TE](https://tradingeconomics.com/commodity/copper) |
| 比特币 | $68,234 | +2.34% | [来源](URL) |

---

## 中国市场与流动性

{要点列表，涵盖 A 股/港股/流动性政策等}

- **A 股成交**：沪深两市合计 XXXX 亿元【[财联社](URL)】
- **北向资金**：净流入/流出 XX 亿元【[来源](URL)】
- **央行动态**：{公开市场操作/MLF/LPR 等}【[央行官网](URL)】
- **政策动向**：{最新监管/产业政策}【[来源](URL)】

---

## 行业热点

{要点列表，每条必须有具体公告或权威报道链接}

- **行业名称**：{具体事件描述}【[公告/报道](URL)】
- **行业名称**：{具体事件描述}【[公告/报道](URL)】
- **行业名称**：{具体事件描述}【[公告/报道](URL)】

---

## 明日重点前瞻

{要点列表，只允许写可核验的官方日历/已公布事件}

- **时间**：{事件名称}【[官方日历/来源](URL)】
- **时间**：{事件名称}【[官方日历/来源](URL)】
- **时间**：{事件名称}【[官方日历/来源](URL)】

> ⚠️ 本前瞻仅包含已公布的官方日历事件，不包含推测性内容。

---

*生成时间：YYYY-MM-DD HH:MM (Asia/Shanghai) | 数据来源：Trading Economics, 金十数据，财联社等*
```

---

## 格式规范

### 表格格式

1. **列数**：标准 4 列（名称、价格/数值、涨跌幅、来源）
2. **来源列**：使用 `[简称](URL)` 格式，确保飞书可点击
3. **数字格式**：
   - 价格：保留 2 位小数，千位分隔符（可选）
   - 涨跌幅：保留 2 位小数，带正负号
   - 收益率：保留 2 位小数，带百分号

### 来源引用格式

1. **表格内**：`[TE](URL)` 或 `[jin10](URL)` 等简称
2. **正文中**：`【[来源名](URL)】` 格式
3. **来源优先级**：
   - 官方：政府机构、央行、统计局原始发布页
   - 监管/交易所：证监会、交易所官方数据
   - 权威通讯社：Reuters, Bloomberg, AP
   - 财经媒体：CNBC, 财联社，华尔街见闻
   - 数据聚合站：Trading Economics, Investing.com

### 模块缺失处理

如果某个 enabled 模块数据采集完全失败：

```markdown
## {模块名称}

> ⚠️ 本模块数据暂缺，采集失败原因：{error_reason}。将在下期补充。
```

---

## 9 模块标准列表

| 序号 | 模块名称 | 内容说明 |
|------|----------|----------|
| 1 | 市场主线 | 当日全球市场最大主线事件，一段式叙述 |
| 2 | 全球宏观速览 | 主要经济体宏观数据/政策动向 |
| 3 | 汇率与美元 | DXY 及主要货币对汇率表格 |
| 4 | 全球利率与美债 | 主要国债收益率表格 |
| 5 | 核心股市表现 | 全球主要股指表格 |
| 6 | 商品与核心资产 | 大宗商品及核心资产表格 |
| 7 | 中国市场与流动性 | A 股/港股/流动性政策要点 |
| 8 | 行业热点 | 具体行业事件，必须有链接 |
| 9 | 明日重点前瞻 | 可核验的官方日历事件 |

---

## 撰写注意事项

1. **时区**：所有时间标注 Asia/Shanghai
2. **时效性**：只写过去 24 小时内新信息
3. **事实核验**：关键数据必须交叉核验（见 `verification.md`）
4. **禁止推测**：明日前瞻只写已公布事件
5. **链接有效**：所有 URL 必须可访问，禁止编造
