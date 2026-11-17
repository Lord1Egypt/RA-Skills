# MCP 协同策略表(2026-07-23 新增)

**目的**:5 个 MCP 工具(TDX/wudao/ftshare/mx-ds/iFind)何时用哪个的明确规则

**核心原则**:
- **TDX 优先**(唯一不限流的 MCP,盘中秒返)
- **wudao 主源**结构化数据(涨停/资金流/题材)
- **ftshare 兜底**(历史数据全)
- **mx-ds 自然语言**(复杂查询)
- **iFind 基本面**(财报/新闻)

---

## 📊 时段 × MCP 矩阵

| 时段 | 实时 tick | 涨停过滤 | 资金流 | 题材新鲜度 | 基本面 |
|---|---|---|---|---|---|
| **09:15-09:30 集合竞价** | ⚠️ TDX 主(拉竞价) | ❌ 不用 | ❌ 不用 | ❌ 不用 | ❌ 不用 |
| **09:30-10:00 早盘** | ✅ TDX 优先 | ✅ wudao | ⚠️ wudao 限流 | ✅ wudao | ⚠️ iFind 延迟 |
| **10:00-11:30 早盘** | ✅ TDX 优先 | ✅ wudao | ✅ wudao | ✅ wudao | ✅ iFind |
| **13:00-15:00 午盘** | ✅ TDX 优先 | ✅ wudao | ✅ wudao | ✅ wudao | ✅ iFind |
| **15:00-17:00 盘后** | ⚠️ TDX 收盘价 | ✅ ftshare | ✅ ftshare | ✅ ftshare/mx-ds | ✅ iFind |
| **18:00-09:15 夜间** | ❌ 不用 | ❌ 不用 | ❌ 不用 | ✅ mx-ds | ✅ iFind |

**图例**:
- ✅ 主源(必用)
- ⚠️ 可用但有限制(限流/延迟)
- ❌ 不可用(数据未生成/接口关闭)

---

## 🔄 失败转移链(2026-07-22 实测)

| 异常类型 | 触发条件 | 第一转移 | 第二转移 | 第三转移 |
|---|---|---|---|---|
| `ConnectionResetError` | 限流/网络 | TDX | wudao | ftshare |
| `API Key 配额用完` | wudao 50 次/天 | TDX | ftshare | mx-ds |
| `MCP server unreachable` | 6 次失败 | 等 60 秒 | TDX | ftshare |
| `Symbol not found` | 代码错 | 搜索股票名 | 用中文名 | TDX 自然语言 |
| `Rate limit exceeded` | iFind 200 次/天 | wudao | mx-ds | TDX |
| `Data timeout` | 盘后 17:00 后 | ftshare | mx-ds | 离线 Riskfolio |

**铁律**:
- **永远不静默重试**——失败要说
- **永远不并行 3 个数据源**——浪费配额
- **永远不假设数据可达**——用户期望"鲁棒"

---

## 🎯 场景 × MCP 协同

### 场景 1【候选挖掘 / Screener】
| 阶段 | 主源 | 备 1 | 备 2 |
|---|---|---|---|
| 自然语言筛股 | mx-ds | TDX | wudao |
| 结构化筛股 | wudao | mx-ds | TDX |
| 主板过滤 | wudao(market="main") | TDX(range="AG") | mx-ds |

### 场景 2【实时行情 / Single Quote】
| 阶段 | 主源 | 备 1 | 备 2 |
|---|---|---|---|
| 盘中价格 | **TDX** | iFind | ftshare |
| 盘后价格 | TDX | ftshare | iFind |
| 历史日线 | ftshare | wudao | mx-ds |

### 场景 3【基本面 / Fundamentals】
| 阶段 | 主源 | 备 1 | 备 2 |
|---|---|---|---|
| 最新摘要 | iFind | mx-ds | wudao |
| 详细财务 | iFind | wudao | mx-ds |
| 估值快照 | wudao | iFind | mx-ds |

### 场景 4【资金面 / Capital Flow】
| 阶段 | 主源 | 备 1 | 备 2 |
|---|---|---|---|
| 盘中主力 | wudao(intraday_main_flow) | ftshare(capital_flow) | - |
| 板块资金 | wudao(theme_intraday_capital) | ftshare(sector_flow) | - |
| ⚠️ 注意 | **禁用 akshare** | (会 ConnectionResetError) | - |

### 场景 5【事件驱动 / Event-Driven】
| 阶段 | 主源 | 备 1 | 备 2 |
|---|---|---|---|
| 催化日历 | wudao(market_catalyst_calendar) | iFind | mx-ds |
| 涨价数据 | iFind EDB | mx-ds | wudao |
| 新闻/快讯 | wudao(cls_news) | iFind | mx-ds |

### 场景 6【组合优化 / Portfolio】
| 阶段 | 工具 | 说明 |
|---|---|---|
| 历史数据 | ftshare(daily_ohlc) | 32 日已实测可拉 |
| 优化 | **本地 Riskfolio 7.3** | API: `port.optimization(model='Classic', rm='MV', obj='MinRisk')` |
| 备份 | 30/15/55 等权法 | 简单权重 |

### 场景 7【复盘 / Post-Market】
| 阶段 | 主源 | 备 1 | 备 2 |
|---|---|---|---|
| 市场概况 | wudao(market_replay_workflow) | - | - |
| 涨停复盘 | wudao(limitup_review_workflow) | - | - |
| ⚠️ 限流 | **09:15-10:30 限流** | 用 iFind 抓个股 | - |

### 场景 8【题材刚启动】🆕
| 阶段 | 主源 | 备 1 | 备 2 |
|---|---|---|---|
| 涨停过滤 | wudao(limit_up_filter) | ftshare | - |
| 题材新鲜度 | wudao(cls_news hoursAgo) | iFind | mx-ds |
| 板块资金 | wudao(theme_intraday_capital) | ftshare | - |
| 实时 tick | **TDX**(秒返) | ftshare | - |

### 场景 9【纪律执行】🆕
| 阶段 | 主源 | 备 1 | 备 2 |
|---|---|---|---|
| 实时 tick | **TDX** | ftshare | - |
| 距离均线 | TDX | ftshare(daily_ohlc) | - |
| 5 日均线 | ftshare(动态计算) | - | - |

---

## 🛠️ 4 个核心脚本的 MCP 调用清单

### check_holdings.py(场景 9 落地点)
```python
# 主源:TDX
mcp__tdx__tdx_wenda_quotes(question="000XXX 最新价 涨跌幅 涨停价 是否涨停")
# 备源:ftshare
mcp__ftshare__intraday_kline(symbol="000XXX.XSHE", type="minute_kline", limit=1)
```

### refresh_holdings.py(持仓新鲜度)
```python
# 主源:TDX(盘中) / ftshare(盘后)
mcp__tdx__tdx_wenda_quotes(question="000XXX 最新价")
# 备源:ftshare 5 日 K
mcp__ftshare__daily_ohlc(symbol="000XXX.XSHG", limit=5)
```

### monitor_intraday.py(盘中监控)
```python
# 主源:TDX(秒返,不限流)
mcp__tdx__tdx_wenda_quotes(question="000XXX 涨跌幅 是否涨停")
```

### find_just_launched.py(场景 8 自动化)
```python
# 主源:wudao
mcp__wudao_a_stock__limit_up_filter(date="2026-07-23", market="main", limit=300)
# 备源:wudao 题材新鲜度
mcp__wudao_a_stock__cls_news(keyword="商业航天", hoursAgo=72)
# 实时 tick:TDX
mcp__tdx__tdx_wenda_quotes(question="000XXX 最新价")
```

---

## 🐛 已知问题(2026-07-23)

1. **TDX 无 topic_id 维度**:只能用自然语言,不能按主题 ID
2. **wudao 限流**:09:15-10:30 每天 50 次免费
3. **ftshare 限流**:盘前盘后稳定,盘中可能 timeout
4. **mx-ds 自然语言慢**:每次 3-5 秒,适合复杂查询
5. **iFind 配额**:200 次/天,扣量

**应对**:
- 盘中 9:00-10:30 **只用 TDX/iFind**
- 盘后 15:00-17:00 **全数据源**
- 夜间 18:00+ **用 mx-ds/iFind 离线**

---

## 📅 cron 调度矩阵

| 时间 | 脚本 | 触发 | 输出 |
|---|---|---|---|
| 09:00 盘前 | 定时任务 | 早盘准备 | IM |
| 09:30-15:00 每 30 分钟 | monitor_intraday.py | 盘中异动 | IM(去重) |
| 15:30 盘后 | refresh_holdings.py | 持仓更新 | holdings_fresh.json |
| 15:30 盘后 | find_just_launched.py | 找刚启动 | launched_YYYYMMDD.json |
| 15:30 盘后 | check_holdings.py | 卖点检查 | IM(分级) |
| 16:00 周末 | daily_review.py(待做) | 周复盘 | 在线文档 |

---

## 📚 相关文件

- 4 个脚本:
  - `<your_dir>/cron/check_holdings.py`   # 用你自己的脚本目录
  - `<your_dir>/cron/refresh_holdings.py`
  - `<your_dir>/cron/monitor_intraday.py`
  - `<your_dir>/cron/find_just_launched.py`
- a-share-expert skill: `<your_skills_dir>/a-share-expert/SKILL.md`
- 场景 8 references: `<your_skills_dir>/a-share-expert/references/theme-launch-hunting.md`
- 场景 9 references: `<your_skills_dir>/a-share-expert/references/discipline-execution.md`

---

**最后更新**: 2026-07-23 17:13 (CST)