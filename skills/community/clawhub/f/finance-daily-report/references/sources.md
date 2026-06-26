# 合规数据源清单（实测可达版）

根据实际测试，按可达性和数据结构化程度排列。标记 ✅ = 实测稳定可达，⚠️ = 偶尔可达，❌ = 不可达/需 JS 渲染。

## Tier 1：结构化数据源（直接 fetch 可解析，首选）

| 来源 | URL | 覆盖模块 | 可达性 | 说明 |
|------|-----|----------|--------|------|
| Trading Economics 股指 | https://tradingeconomics.com/stocks | 股市 | ✅ | 全球主要指数一页全有，结构化表格 |
| Trading Economics 汇率 | https://tradingeconomics.com/currencies | 汇率+美元 | ✅ | 所有主要货币对+DXY |
| Trading Economics 商品 | https://tradingeconomics.com/commodities | 商品 | ✅ | 原油/黄金/白银/铜/铁矿石 |
| Trading Economics 个品详情 | https://tradingeconomics.com/commodity/{name} | 市场主线 | ✅ | 含当日分析+数据+背景 |
| Trading Economics 国家指标 | https://tradingeconomics.com/{country}/{indicator} | 宏观 | ✅ | 含分析段落+数据 |

## Tier 2：新闻/日历源（直接 fetch 可抓文本）

| 来源 | URL | 覆盖模块 | 可达性 | 说明 |
|------|-----|----------|--------|------|
| 金十数据 | https://www.jin10.com/ | 市场主线/宏观/地缘 | ✅ | 快讯流，中文，数据密度高 |
| 财联社 | https://www.cls.cn/ | 前瞻/日历 | ✅ | 日历事件列表，非常结构化 |
| 东方财富 | https://www.eastmoney.com/ | A 股/中国市场 | ✅ | A 股摘要+分析文章 |
| CNBC 个股报价 | https://www.cnbc.com/quotes/{ticker}/ | 个别指数 | ✅ | 单指数详情（如 .FCHI, .DJI） |

## Tier 3：搜索引擎（作为补充，不稳定）

| 来源 | 说明 | 可达性 |
|------|------|--------|
| web_search (Brave) | 通过 OpenClaw 中继 | ⚠️ 间歇性不可用 |

## 不可达/弃用源

| 来源 | 原因 |
|------|------|
| Yahoo Finance | 中国大陆 403 |
| Investing.com | Cloudflare 拦截 |
| Bloomberg | 付费墙 + 反爬 |
| Reuters | 间歇性 fetch failed |
| MarketWatch | JS 渲染 + 401 |
| Google Finance | IP 限制（内网 DNS 解析异常）|
| 华尔街见闻 | JS 渲染，fetch 只返回空壳 |
| TradingView | JS 渲染 |

## 采集策略优先级

```
1. 先跑 scripts/fetch_market_data.py → 抓 Tier 1 全部结构化数据
2. 再 web_fetch Tier 2 新闻源 → 补充叙事/日历/事件
3. 如果 web_search 可用 → 用它搜特定事件补充细节
4. 如果 web_search 不可用 → 跳过，不阻塞流程
```

## 单页汇总 URL（一次 fetch 搞定一个大模块）

| 模块 | URL | 数据量 |
|------|-----|--------|
| 全球股指 | https://tradingeconomics.com/stocks | ~30 个指数 |
| 全球汇率 | https://tradingeconomics.com/currencies | ~30 个货币对 |
| 全球商品 | https://tradingeconomics.com/commodities | ~30 个商品 |
| 全球国债 | https://tradingeconomics.com/bonds | ~20 个国家收益率 |
