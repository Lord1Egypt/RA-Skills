# MCP 数据源详细能力矩阵

## 实测结论(2026-07-22)

### TDX (mcp__tdx__)
**总评:⭐⭐⭐⭐⭐ 实测中表现最好的**

| 工具 | 实测能力 | 限制 |
|---|---|---|
| `tdx_wenda_quotes(question, range)` | **秒级返回**A股价格 + 行业 + PE + 4 个价格点 | 主板/创/科都支持;需 `market=AG`(默认)或 `ZS/ZK/BJ` 区分 |
| `tdx_wenda_quotes(question, range="HK-GP")` | 港股行情 | - |
| `tdx_wenda_quotes(question, range="JJ")` | 基金行情 | - |
| `tdx_wenda_quotes(question, range="ZS")` | 指数行情 | - |

**代码格式**:6 位数字 = 主板, 300xxx = 创业板, 688xxx = 科创板, 8xx/4xx = 北交所

**实战坑**:开了 "主板" 过滤后,Tushare-style 代码(如 "600519.SH")会匹配不上。用纯 6 位 "600519" 即可。

---

### iFind (mcp__hexin_ifind_ds_*)
**总评:⭐⭐⭐⭐⭐ A 股基本面的金标准**

#### 4 个独立 MCP:
1. `hexin-ifind-ds-stock-mcp` ← 单票财务/股价/事件
2. `hexin-ifind-ds-edb-mcp` ← 宏观/行业经济数据(价格/指数)
3. `hexin-ifind-ds-news-mcp` ← 新闻/资讯检索
4. `hexin-ifind-ds-index-mcp` ← 板块指数
5. `hexin-ifind-ds-global-stock-mcp` ← 港美股

#### 核心工具(以 stock-mcp 为例)
| 工具 | 能力 | 适用 |
|---|---|---|
| `get_stock_summary(query)` | **单票一站式摘要**:公司信息/主营/最新季报/业绩预告 | "XXX 这公司怎么样" |
| `get_stock_performance(query)` | 技术形态 + 涨跌幅数据 | "XXX 最近怎么走" |
| `get_stock_financials(query)` | 详细财务指标(ROE/PE/毛利率等) | "XXX 财务健康吗" |
| `get_stock_shareholders(query)` | 股东结构 + 解禁 + 增减持 | "XXX 谁在买" |
| `get_risk_indicators(query)` | 量化风险(VaR/Beta/夏普) | "XXX 风险多大" |
| `get_stock_info(query)` | 工商信息/上市信息/分类 | "XXX 是哪的" |

**实战坑**:
- 200 次/天限额,扣量
- Token 写入有 bug(详见 memory),改完必须 verify
- query 必须包含证券实体(代码/简称)

#### edb 工具(EDB 系列)
- `get_edb_data(query)` ← 自然语言查价格/产量/宏观(中文)
- 例:`query="R22 R134a 现货价格 2026-07"` → 返回价格序列
- **这是你的"涨价逻辑验证"金标准**——任何商品价格先来这里查

---

### mx-ds (mcp__mx_ds_mcp__)
**总评:⭐⭐⭐⭐⭐ 自然语言筛股的隐藏王牌**

| 工具 | 能力 |
|---|---|
| `mx_stocks_screener(query)` | **自然语言筛股**,最强 |
| `mx_ashare_finance_data(query)` | A 股个股财务数据 |
| `mx_hk_finance_data(query)` | 港股 |
| `mx_us_finance_data(query)` | 美股 |
| `mx_index_block_finance_data(query)` | 指数/板块 |
| `mx_macro_data(query)` | 宏观 |
| `mx_finance_search_news(query)` | 资讯检索 |
| `mx_finance_search_notice(query)` | 公告原文 |
| `mx_comprehensive_finance_data(query)` | 综合查询(跨品种) |

**实测能力**(2026-07-22):
- "主板 + 流通 50-200 亿 + 5 日跌 5%+ + PE 0-50" → 180+ 个真实结果
- 支持"不包含创业板/科创板/北交所"这种自然语言约束
- **比 wudao_a_stock screener 更强大**(因为自然语言灵活)

**实战坑**:
- max 多只同 query,单只更精准
- 自然语言尽量包含:流通市值范围 + 涨幅范围 + PE 范围 + 板块过滤

---

### FTShare (mcp__ftshare__)
**总评:⭐⭐⭐ 工具丰富但限流频繁,数据最准**

#### 核心工具
| 工具 | 能力 | 实测 |
|---|---|---|
| `daily_ohlc(symbol, start_date, end_date)` | A 股日线(已实测拿 4 只票 32 天) | ✅ 唯一真实数据源 |
| `intraday_kline(symbol, type)` | 分时/分钟 K | 限流 1 次 |
| `capital_flow(symbol, type)` | 主力资金 | ⚠️ 限流,慎用 |
| `mx_ashare_finance_data(query)` | 同上 | - |
| `margin(date, page_size)` | 两融快照 | 限流 |

**实测发现**(2026-07-22 15:30):
- 14:30 实测 `daily_ohlc` 完美返回 32 天数据 ✅
- 14:55 实测 `capital_flow` 报错 `UPSTREAM_UNAVAILABLE` ❌
- 推断:**非窗口时间(可能是盘后维护期)就限流**

**实战坑**:
- symbol 必须是 `000XXX.XSHE` 或 `000XXX.XSHG` 格式(带后缀)
- 默认 type=stock
- **忌并行调多只**(容易被限)

---

### Wudao (mcp__wudao_a_stock__)
**总评:⭐⭐⭐⭐ 主力资金/涨停池/AKShare 不可用时的最佳替补**

#### 限流时段规则(实测)
- **09:15-10:30**:限流(早盘)
- **10:30-13:00**:可能正常也可能限
- **13:00-15:00**:基本正常
- **15:00-18:00**:全天数据落库,稳定
- **每日额度**:50 次/天(免费版)

#### 核心工具(优先在 13:00 后使用)
| 工具 | 能力 | 适用 |
|---|---|---|
| `intraday_main_flow(codes=...)` | **盘中个股主力资金**(盘口中单+大单+超大单) | 盘中盯盘 |
| `capital_flow(flowType)` | 个股/板块/大盘/北向资金 | 盘后复盘 |
| `stock_screener(...)` | 结构化筛股 | 候选挖掘 |
| `valuation_snapshot(code)` | 个股估值快照 | "PE/PB" |
| `limit_up_filter(date)` | 涨停板筛选 | "今天谁涨停了" |
| `limit_up_ladder(date)` | 涨停板连板梯队 | "高位股结构" |
| `limit_stats(date)` | 涨跌停统计 | "今天多空" |
| `short_term_emotion()` | 短线情绪(涨/跌停/炸板率) | "市场情绪" |
| `market_overview()` | 全市场宽度(涨/跌/平家数) | "今天冷热" |
| `market_catalyst_calendar(start, end)` | **未来催化事件查询** | "未来事件" |
| `theme_intraday_capital(keyword)` | 题材资金流向 | "题材活跃度" |
| `official_announcements(stock)` | 单票公告 | 公告检索 |
| `dragon_tiger(date)` | 龙虎榜 | 谁在大买/大卖 |

**实战坑**:
- 早盘半小时坚决不用
- API 调用超过 50 次/天直接报错
- 部分工具如 `stock_event_calendar` 需要付费版

---

### Firecrawl (mcp__firecrawl__)
**总评:⭐⭐⭐⭐ 资料/调研用,适合"深研"场景**

**触发场景**:
- 公告原文 PDF/HTML 解析
- 上市公司调研纪要(来自各券商)
- 行业深度报告
- 重大新闻原文

**激活条件**:需要新会话(MCP 配置写入后下次会话可用)

---

## ⚠️ 不能用的数据源

### Tushare
**只走本地 CLI,不是 MCP**。**跳过**。详见 skill `stock-data-source-guide`。

### AKShare
**Connection reset 是常态**,完全不要用作生产数据源。

### Wind
本对话无 Wind 接口。所有"Wind 数据"用 TDX/iFind/mx-ds 替代。

---

## 📋 速查决策表

| 我要... | 用什么 |
|---|---|
| 1 只票现在多少钱 | TDX `tdx_wenda_quotes` |
| 1 只票最近 60 日日线 | FTShare `daily_ohlc`(30 天内稳;60 天需分段) |
| 1 只票基本面 | iFind `get_stock_summary` |
| 1 只票机构持仓 | iFind `get_stock_shareholders` |
| 1 只票行业地位 | iFind `get_stock_info` |
| 筛股(自然语言) | mx-ds `mx_stocks_screener` |
| 筛股(结构化) | wudao_a_stock `stock_screener`(13:00 后) |
| 涨停板 | wudao_a_stock `limit_up_filter` |
| 题材资金 | wudao_a_stock `theme_intraday_capital` |
| 主力资金(盘中) | wudao_a_stock `intraday_main_flow` |
| 主力资金(盘后) | wudao_a_stock `capital_flow`(13:30 后) / FTShare(限流) |
| 未来催化 | wudao_a_stock `market_catalyst_calendar` |
| 商品价格 | iFind EDB `get_edb_data` |
| 新闻检索 | iFind news `search_news` |
| 公告原文 | iFind news `search_notice` |
| 公告 PDF | firecrawl `firecrawl_parse` |
| 量化风险指标 | iFind `get_risk_indicators` |
| 组合优化 | 本地 Riskfolio 7.3(FTShare 喂数据) |
