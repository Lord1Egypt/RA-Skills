---
name: a-share-expert
description: A-share (China) stock trading decision expert. Integrates stock data MCP servers with expert methodology across 9 scenarios: holding diagnosis, candidate screening, event-driven analysis, portfolio optimization, intraday scanning, theme-launch hunting, and profit-taking/stop-loss discipline. For Shanghai/Shenzhen main-board trading decisions.
---

# A 股实战决策专家 (A-Share Expert)

## ⚠️ 核心规则(必读)

### 1. 硬约束(通用配置项)
- **交易范围可配置**(默认主板):创业板(300)/科创板(688)/北交所(830/870)通常被排除 — 通过 `TRADING_SCOPE` 配置项控制,所有工具调用必须带范围过滤
- TDX 工具必须设 `market=AG` 或上交所/深交所主板枚举
- mx-ds 自然语言查询必须包含"主板"或"不包含创业板/科创板/北交所"
- wudao_a_stock 多数工具带 `market` 参数,必须显式设置

### 2. 数据源时段规则(基于 2026-07-22 实测)
- **09:15-10:00**:只读 **TDX/iFind**(其他三家限流/休眠)
- **10:00-11:30 / 13:00-15:00**:**全数据源稳定**,优先选 wudao_a_stock(主力数据最准)
- **15:00-17:00**:全数据源可用,优先 FTShare/iFind 做真实数据回测
- **18:00-09:15 夜间**:FTShare 历史数据 / iFind EDB 数据 / mx-ds 文档检索 / 离线 Python 回测

### 3. 用户输入约定
- 用户提供持仓(代码+成本)时,先验证再用于分析
- Riskfolio 已装好(`/tmp/portfolio_real.py`),API 是 `port.optimization(model='Classic', rm='MV', obj='MinRisk')`,返回 DataFrame,列名 `weights`

---

## 9 大实战场景的冗余数据流

### 场景 1:【候选挖掘 / Screener】— "找几只股票看看"
```
主源: mcp__mx_ds_mcp__mx_stocks_screener(query="主板流通市值X-X亿 + 涨幅X + PE X-X")
备份 1: mcp__tdx__tdx_wenda_quotes(question="主板...筛选")
备份 2: mcp__wudao_a_stock__stock_screener(market='main_sh/main_sz/xshe')
```
失败转移:换主源 → 改用 TDX 自然语言 → 再不行就用 Wudao 结构化

### 场景 2:【实时行情 / Single Quote】— "XXX 现在多少钱"
```
主源: mcp__tdx__tdx_wenda_quotes(question="XXX600519最新价")
备份 1: mcp__hexin_ifind_ds_stock_mcp__get_stock_performance(query="XXX")
备份 2: mcp__ftshare__daily_ohlc(symbol='XXX.XSHG', start_date=今天, end_date=今天)
```
时段切换:盘中用 TDX(秒级),盘后用 iFind/FTShare(日线)

### 场景 3:【基本面 / Fundamentals】— "公司基本面怎么样"
```
主源: mcp__hexin_ifind_ds_stock_mcp__get_stock_summary(query="XXX基本面")
备份 1: mcp__hexin_ifind_ds_stock_mcp__get_stock_financials(query="XXX财务指标")
备份 2: mcp__wudao_a_stock__financial_summary(code='XXX')
```
要点:get_stock_summary 包含最新季报/业绩预告/经营数据 / get_stock_financials 是更精细的财务指标

### 场景 4:【资金面 / Capital Flow】— "今天主力怎么动"
```
主源: mcp__wudao_a_stock__intraday_main_flow(codes='XXX,YYY')
备份 1: mcp__wudao_a_stock__capital_flow(flowType='stock', stockCode='XXX')
备份 2: mcp__ftshare__capital_flow(symbol='XXX.XSHE') ⚠️ 限流,只在非窗口
```
要点:**绝对不要用 akshare 做资金面**(connection reset)

### 场景 5:【事件驱动 / Event-Driven】— "未来有没有催化"
```
主源: mcp__wudao_a_stock__market_catalyst_calendar(startDate=今天, endDate=8-15)
备份 1: mcp__hexin_ifind_ds_news_mcp__search_news(query="XXX 涨价/产能")
备份 2: mcp__hexin_ifind_ds_edb_mcp__get_edb_data(query="XXX 价格走势")
```
要点:涨价/产能数据用 EDB,题材/事件用 catalyst_calendar

### 场景 6:【组合优化 / Portfolio Optimization】— "我该怎么调仓"
```
主源: 本地 Riskfolio 7.3 (.optimization API, 已是 .py 模板)
备份 1: 改用 30/15/55 简单权重等权法
备份 2: 按 PE/市值分档(大盘 25% / 中盘 15% / 小盘 10%)
```
数据源:FTShare daily_ohlc(已实测 32 个交易日拉真)

### 场景 7:【复盘 / Post-Market】— "今天市场怎么样"
```
主源: mcp__wudao_a_stock__market_replay_workflow(date=今天)
备份 1: mcp__wudao_a_stock__limitup_review_workflow(date=今天)
备份 2: mcp__wudao_a_stock__short_term_emotion()
```
要点:**13:00 后才能调 wudao_a_stock**(09:15-10:30 限流)
时段替代:09:00-10:30 用 `mcp__hexin_ifind_ds_stock_mcp__get_stock_summary` 抓个股

### 场景 8:【题材刚启动识别 / Theme-Launch Hunting】— "怎么抓到刚启动的票" 🆕
**用户核心痛点**:A 股真正赚钱的是题材炒作(亏损股/概念股蹭热度一波涨 30-40%),但不知道**怎么识别"刚启动"**(而不是"高位接盘"或"末日狂欢")
**核心方法论**:A 股题材炒作 = 亏损股/概念股 > 基本面好的票,**接受这个事实**才能赚钱
**详细框架** → 见 references/theme-launch-hunting.md
**核心工具调用模板**:
```
Step 0 必先执行: get_realtime_tick(候选代码) → 确认当前价 + 是否涨停 + 封单额

1. 题材时间节点验证(必查 3 件事)
   ├─ 题材新鲜度:wudao_a_stock.cls_news(keyword=题材, hoursAgo=24) → 看新闻距今几小时
   │  ✅ ≤ 24h = 刚发酵 | 24-72h = 启动期 | ≥ 72h = 已结束
   ├─ 政策/事件强度:wudao_a_stock.market_catalyst_calendar(startDate=今天, endDate=+14天)
   └─ 板块联动:wudao_a_stock.auction_theme_strength(tradeDate=今天) + wudao_a_stock.sector_analysis(period=5)

2. 龙头"启动信号"识别(5 维度)
   ├─ 量能异动:wudao_a_stock.stock_screener(volumeRatioMin=2) + 量比 > 1.5
   ├─ 价格异动:突破 MA20(从 wudao_a_stock.kline 取数据)
   ├─ 题材联动:同题材 ≥ 3 只涨停 = 主线
   ├─ 资金异动:wudao_a_stock.intraday_main_flow(codes=候选池) 主力净流入转正
   └─ 分时特征:早盘冲高回落 + 午后拉升 = 启动分时(非一字板)

3. "题材生命周期"定位(必查)
   ├─ 阶段 1 潜伏期(最佳买点):题材刚出,小阴小阳
   ├─ 阶段 2 启动期(次佳):首个涨停 + 温和放量(2-3 倍)
   ├─ 阶段 3 高潮期(危险):一字板 + 多日连板 + 天量
   └─ 阶段 4 退潮期(必走):放量下跌 + 高位震荡
   **判断**:封单/流通盘 = 1-3% 启动 | 5%+ 高潮 | 题材 ≥ 3 天 = 高潮

4. 情绪周期匹配(必查)
   ├─ 涨停家数:30-60 = 回暖期(可买)/ 60-100 = 高潮(不追)/ > 100 = 过热
   ├─ 炸板率:< 30% 一致 | 30-50% 分歧 | > 50% 恐慌
   └─ 封板率:< 50% 弱势 | 50-70% 正常 | > 70% 强势

5. 过滤器(去除"高位接盘")
   ├─ PE > 200 倍 → 警惕(纯题材票常见,接受但控仓)
   ├─ Q1 同比 -50% → 警惕(题材股典型,小心证伪)
   ├─ 近 20 日涨幅 > 30% → 大概率已涨完,不买
   └─ 题材时间 > 7 天 → 高潮期,不买

6. TDX 实时兜底(2026-07-23 新增)
   ├─ 自然语言查询:mcp__tdx__tdx_wenda_quotes(question="XXX 是否涨停 封单多少")
   ├─ 适用场景:盘中快速核对涨停状态/封单额
   └─ 优势:秒返,不限流,适合盘中高频调用

⚠️ 心态校正(交易者必须接受):
- A 股 90% 赚钱机会来自题材炒作(亏损股/概念股)
- 基本面好的票反而涨得少
- "刚启动"是事后才知道,你买入时已经涨 5-10%
- 目标不是 100%,是 20-30%(到了必须减仓)
- 80% 的"刚启动"票其实是亏损股或微利股
```
**触发关键词**:刚启动 / 启动信号 / 题材股 / 概念股 / 亏损股也能涨 / 怎么抓到 / 一波涨三四十 / 题材新鲜度 / 启动期 / 潜伏期 / 高潮期

### 场景 9:【纪律执行 / Rule Execution】— "拿不住好票" 🆕
**用户核心痛点**:选股对(事件驱动/涨价逻辑能找到好票),但**判断不了卖点**,导致要么卖飞要么拿过头
**核心方法论**:**卖点不是盘中决定的,是买入时就预设的**;规则写下来 + 工具强制推送,不靠盘中判断
**详细框架** → 见 references/discipline-execution.md
**核心工具调用模板**:
```
Step 0 必先执行(每次回答前): get_realtime_tick(每只持仓) → 拿到当前真实价格
  → 不准用"上次看的数据"判断当前是否触发卖点

1. 预设 4 个卖出位(买入当天就设,写到持仓备注)
   ├─ 卖点 1 强止盈位:浮盈 +20% → 减仓 50%
   ├─ 卖点 2 移动止盈位:跌破 5 日均线 → 减仓 30%
   ├─ 卖点 3 题材兑现位:事件兑现/涨价见顶 → 减仓 50%
   └─ 卖点 4 硬止损位:买入价 -8% → 强制止损 50% / -10% 清仓

2. 时间止损(防止"温水煮青蛙")
   ├─ 买入 5 个交易日不涨 → 减仓 50%(判断错了)
   └─ 买入 10 个交易日没创新高 → 清仓

3. 定时检查提醒(用定时任务 + IM 工具,需用户配置)
   ├─ 每天 14:30 自动检查持仓 → 触发规则 → 推送 IM 提醒
   ├─ 推送内容:当前价 vs 4 个卖点 + 建议动作 + 仓位调整
   └─ 不靠盘中看盘,靠规则推送

4. TDX 实时止盈止损提醒(2026-07-23 新增)
   ├─ 盘中快速查:mcp__tdx__tdx_wenda_quotes(question="XXX 当前价 距离 5 日均线")
   ├─ 适用场景:盘中接近止盈位时,快速核对是否触发
   └─ 优势:秒返不限流,适合盘中每 30 分钟扫一次持仓

⚠️ 心态校正(交易者必须接受):
- 你赚不到钱不是因为选股差,是**纪律差**
- 90% 的散户盈利 5-15% 就跑,亏损 10-20% 死扛
- 涨 20% 不贪(贪了大概率回吐)
- 跌 10% 不扛(扛了大概率继续跌)
- 工具不能帮你赚钱,**纪律可以**
```
**触发关键词**:拿不住 / 卖飞 / 拿过头 / 卖点 / 止盈 / 止损 / 纪律 / 怎么卖 / 移动止盈 / 题材兑现位

---

## 工具路由决策树(每次问股票问题的必经之路)

```
用户提问 → 解析意图 → 【Step 0 实时 tick 校验】 → 时段判断 → 数据源优先级 → 执行 → 校验 → 输出
```

### Step 0:实时 tick 校验(2026-07-23 新增铁律)

**所有涉及"当前价/涨跌幅/是否涨停"的判断前,必须先拉一次实时 tick**

⚠️ **铁律背景**:用户 2026-07-23 三次纠正"用 mcp 看数据",根因是用早盘数据默认全天走势,未拉到最新 tick。

```python
# 实时 tick 校验函数(每次回答股票问题前必调)
def get_realtime_tick(code: str) -> dict:
    """返回 {price, time, pct_change, is_limit_up, is_limit_down, volume}"""
    now = datetime.now()
    if 9 <= now.hour < 15:  # 盘中
        # TDX 主源(秒返),ftshare/wudao 备
        try:
            return mcp__tdx__tdx_wenda_quotes(
                question=f"{code} 最新价 涨跌幅 是否涨停"
            )
        except Exception:
            return mcp__ftshare__intraday_kline(
                symbol=f"{code}.XSHE/XSHG",
                type="minute_kline",
                limit=1
            )
    else:  # 盘后
        return mcp__ftshare__intraday_kline(
            symbol=f"{code}.XSHE/XSHG",
            type="minute_kline",
            limit=1
        )

# 输出格式必须先报:
# 📅 YYYY-MM-DD HH:MM 段
# 💹 最新价 X / 涨跌幅 X% / 涨停 X / 封单 X
```

**应用场景**:
- 用户问"XXX 现在多少钱" → 必先 get_realtime_tick
- 用户问"XXX 涨停了吗" → 必先 get_realtime_tick + limit_event_timeline(看开板记录)
- 用户问"XXX 涨了没" → 必先 get_realtime_tick
- **唯一例外**:用户明确说"看历史 K 线/复盘" → 不需要实时 tick

### Step 1: 意图分类
| 用户关键词 | 场景 | 主源 |
|---|---|---|
| 找股/筛股/选股/机会/题材 | 场景 1 | mx-ds 主源 |
| 价格/多少/最新/涨多少 | 场景 2 | TDX 主源(实时) |
| 公司/基本面/财报/业绩 | 场景 3 | iFind 主源 |
| 主力/资金/流入/流出/超单 | 场景 4 | Wudao 主源 |
| 事件/催化/涨价/大会 | 场景 5 | Wudao catalyst |
| 持仓/仓位/调仓/组合 | 场景 6 | Riskfolio 本地 |
| 复盘/今天/早盘/盘面 | 场景 7 | Wudao replay |
| **刚启动/启动信号/题材股/概念股/亏损股/潜伏期/高潮期/题材新鲜度** | **场景 8** | **cls_news hoursAgo + sector_analysis + stock_screener** |
| **拿不住/卖飞/拿过头/卖点/止盈/止损/纪律/移动止盈/题材兑现位** | **场景 9** | **定时检查 + intraday_main_flow + kline** |

### Step 2: 时段判断
```python
from datetime import datetime
now = datetime.now()
hour = now.hour
minute = now.minute

if 9 <= hour < 10 or (hour == 10 and minute < 30):
    # 早盘限流期:只能用 TDX / iFind
    allowed = ['tdx', 'ifind']
elif 10 <= hour < 12 or 13 <= hour < 15:
    # 盘中活跃期:全数据源
    allowed = ['tdx', 'ifind', 'wudao', 'mx', 'ftshare']
elif 15 <= hour < 17:
    # 盘后稳定期:全数据源,可重试用 FTShare
    allowed = ['tdx', 'ifind', 'wudao', 'mx', 'ftshare']
else:
    # 夜间:文档检索 + 离线
    allowed = ['ifind', 'ftshare', 'mx', 'riskfolio']
```

### Step 3: 主源失败 → 备份转移顺序
**永远按"主→备1→备2"顺序降级**,不要并行调用。
- 主源失败 1 次 → 换备 1
- 备 1 失败 → 换备 2
- 备 2 失败 → 坦白告诉用户数据不可达,不要编造

---

## 数据源能力矩阵(基于实测)

| 数据需求 | TDX | iFind | mx-ds | FTShare | Wudao | 其他 |
|---|---|---|---|---|---|---|
| **A股实时价** | ⭐⭐⭐⭐⭐(秒返) | ⭐⭐⭐(延迟) | ⭐⭐⭐⭐ | ⭐⭐⭐(限流) | ⭐⭐⭐⭐ | - |
| **A 股东板过滤** | ✅ `market=AG` | ✅(限沪/深/京) | ✅ 自然语言"主板" | ✅ 自动 | ✅ `market=main_*` | - |
| **行业/概念板块** | ⭐⭐⭐⭐ | ❌ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | - |
| **基本面/财报** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | - |
| **历史日线** | ⭐⭐⭐⭐(脚本内调) | ⭐⭐⭐⭐(脚本) | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐(实测过) | ⭐⭐⭐⭐ | - |
| **盘中分钟线/实时** | ⭐⭐⭐(有但需主题 ID) | ❌ | ❌ | ⭐⭐⭐(限流) | ⭐⭐⭐⭐⭐(intraday_main_flow) | - |
| **主力资金流向** | ⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐(限流) | ⭐⭐⭐⭐⭐ | - |
| **涨停池/复盘** | ❌ | ❌ | ⭐⭐ | ❌ | ⭐⭐⭐⭐⭐ | - |
| **新闻/快讯** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐(CLS) | Firecrawl |
| **事件/催化日历** | ❌ | ⭐⭐⭐ | ❌ | ❌ | ⭐⭐⭐⭐⭐(catalyst_calendar) | - |
| **大宗商品/价格** | ❌ | ⭐⭐⭐⭐⭐(EDB) | ⭐⭐⭐ | ⭐⭐⭐⭐ | ❌ | - |
| **AI/自然语言筛股** | ⭐⭐⭐⭐(对话式) | ⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ | ⭐⭐⭐ | - |
| **回测/组合优化** | ❌ | ❌ | ❌ | ✅(历史日) | ❌ | **Riskfolio 7.3**(本地) |

---

## 与其他 skill 的协同

- **`stock-data-source-guide`** = 数据源速查表(保留作为参考)
- **`stock-analysis-router`** = 意图路由(升级版已合到这里)
- **`financial-analysis-tooling-pitfalls`** = 交易时段陷阱 + Riskfolio API 坑
- **`event-driven-pricing-swing`** = 事件驱动分析框架(涨价 + 大会 + 业绩)
- **`references/theme-launch-hunting.md`** = 场景 8 详细方法论(题材刚启动识别)
- **`references/discipline-execution.md`** = 场景 9 详细方法论(止盈止损纪律执行)
- **`wudao-stock-attribution`** = 🆕 A股短线归因("XX 为什么涨停/异动原因/归因")→ 触发/主因/载体三拆解 + 三一致性评分
- **`wudao-auction-review`** = 🆕 集合竞价专项(9:25-9:30 实时解读)→ 情绪定性 + 主线一致性 + 盯盘名单 3 步法,6 个竞价原子工具按场景路由
- **`wudao-theme-research`** = 🆕 题材/板块研究(任何时点)→ 四象限判读(领涨/补涨/退潮/冷门) + 3 表交集验证真主线 + 新闻+资金双侧证据
- **`zhitu-a-stock`** = 🆕 智兔数服 MCP(200次/天 + 麦蕊智数 500次/天 共 23 个工具)→ 双数据源兜底:zhitu_kline/zhitu_capital_flow(4维)/zhitu_performance_forecast/zhitu_top10_holders + mairui_interactive_qa(问董秘)/mairui_announcement(带原文链接)/mairui_ztree(板块树)
- **`references/trading-rules-essentials.md`** = 交易规则速查
- **`references/scenarios-7-flow.md`** = 老 7 场景流程
- **`references/mcp-fallback-matrix.md`** = MCP 降级矩阵
- **`references/mcp-coordination-strategy.md`** = 5 个 MCP 时段协同策略
- **`references/multi-agent-decision-framework.md`** = 🆕 4 个对抗 LLM 老毛病的机制(防编造/角色对抗/5 档评级/决策反思)
- **本 skill = 总入口**,加载我 = 自动获得所有上述内容

---

## 🚨 失败恢复模式(Failure Recovery)

### 异常类型 → 应对
| 异常 | 主源 | 备 1 | 备 2 |
|---|---|---|---|
| `ConnectionResetError` | **绝不**用 AKShare | TDX | iFind |
| `UPSTREAM_UNAVAILABLE` | FTShare 重试 1 次 | TDX | iFind |
| `API Key 今日免费额度已用完`(50 次/天) | **wudao_a_stock** = 别用 | TDX | iFind |
| `MCP server unreachable` | 等 60 秒 | TDX | iFind |
| `Rate limit exceeded` (iFind 200次/天,扣量) | 警告用户"今日 iFind 额度用完" | TDX | 本地模拟 |
| `symbol not found` | 检查代码格式(必须是 6 位 + .XSHE/XSHG 后缀) | 搜索股票 | 用中文名 |

### 用户应该知道的限制
- **iFind token 写入有 bug**(记在 memory),改完必须 verify
- **A 股涨停限制**:ST 5%, 科创/创 20%, 主板 10% — 影响涨停板分析
- **Tushare 限流**:别用 akshare,别用 tushare, 用 FTShare 反而更稳
- **Wind 不可用**:本对话无 Wind,所有"Wind 数据"都得靠其他源

---

## 📋 实战流程(每个股票问题都要走)

```
1. 解析用户意图 → 场景 1-7 中归类
2. 时段判断 → 数据源允许列表
3. 主源调用 → 失败转备 1 → 再失败转备 2
4. 校验数据(合理性 + 时效性)
5. 输出:
   - 直接回答(数据查询)
   - 决策清单(挂单 / 加仓 / 减仓 / 止损)
   - 文档(IM 群分享)
6. 留口:下次问同类问题先复用本次结果
```

---

## 🎯 加载本 skill 的触发词

以下关键词可提示加载本 skill(由用户或上层编排决定):
- 股票/股/A股/选股/筛股/埋伏
- 持仓/仓位/调仓/组合/仓位管理
- 价格/涨跌/行情/盘面/涨停
- 资金/主力/流向/流入流出
- 基本面/财报/业绩/行业/题材
- 加仓/减仓/止损/止盈/挂单
- **刚启动/启动信号/题材股/概念股/亏损股/潜伏期/高潮期/题材新鲜度**
- **拿不住/卖飞/拿过头/卖点/纪律/移动止盈/题材兑现位**
- 借问"X 只票 X 怎么样"任何形式

**归因专项触发词**(按需加载 wudao-stock-attribution):
- 为什么涨停/为什么涨/异动原因/短线主因/题材归因/连板原因/盘中归因/盘后归因
- "XX 是什么逻辑"/"谁在拉"/"什么资金买"/"消息面是什么"

**集合竞价专项触发词**(9:25 后按需加载 wudao-auction-review):
- 集合竞价/竞价/9:15/9:25/开盘前/开盘竞价/竞价异动/竞价反馈/竞价梯队
- 竞价超预期/竞价被核/弱转强/今天竞价主线/开盘观察名单
- 竞价涨停/竞价跌停/竞价成交额/竞价委买额

**题材板块研究触发词**(按需加载 wudao-theme-research):
- 题材/概念/板块/风口/轮动/主线/概念排行/成分股/板块资金流
- "今天最强题材"/"XX 板块为什么热"/"龙头是谁"/"哪些题材在退潮"
- "AI/算力/CPO/液冷/MLCC 板块怎么样"

**由用户或编排层决定是否加载** —— 这是设计目标。

---

## ⚙️ 实现细节(给 AI 自己看的)

### 工具调用偏好
1. **优先 MCP 工具**而非 Shell(快速 + 结构化)
2. **优先 streaming/JSON** 而非 HTML(用 `mcp__firecrawl__firecrawl_scrape` 而非 wget)
3. **优先并行**(独立问题同批调),**优先串行**(依赖关系)
4. **结果缓存**:同一股票同一时段的多个查询 → 复用上次结果

### 输出偏好
- 中文为主,关键数据中英对照
- 价格/涨跌幅 → 用表格
- 决策 → 用 [触发条件 / 动作 / 仓位 / 止损] 四要素清单
- 微信文档 → 标题层级 ≤ 3 层 + 关键数字加粗

### 错误处理
- **绝不编造数据**(说"我不知道"比给错数据好)
- **绝不静默重试**(失败要说)
- **绝不并行 3 个数据源**(浪费配额)

---

## 📦 最后一条信息

- **加载本 skill 之后**,先 `skill_view('stock-data-source-guide')` 1 次获取上下文
- 然后按本 skill 的"9 大场景路由表"开始
- 涉及**刚启动/题材股**问题 → `skill_view('a-share-expert/references/theme-launch-hunting.md')`
- 涉及**卖飞/拿不住/止盈止损**问题 → `skill_view('a-share-expert/references/discipline-execution.md')`
- 涉及**单股诊断/选股对比/题材分析**(任何"判断型"问题)→ `skill_view('a-share-expert/references/multi-agent-decision-framework.md')`,套用 4 个机制(防编造/角色对抗/5 档评级/反思)
- 涉及**归因/异动原因**(用户问"XX 为什么涨停/为什么涨/异动原因/短线主因")→ `skill_view('wudao-stock-attribution')`,套用 5W + 三拆解(触发/主因/载体) + 三一致性评分
- 涉及**集合竞价解读**(9:25 后用户问"竞价/开盘/9:25/竞价主线/弱转强/盯盘名单")→ `skill_view('wudao-auction-review')`,套用 3 步法(情绪→主线→盯盘)
- 涉及**题材/板块研究**(用户问"XX 板块怎么样/今天最强题材/谁在退潮/龙头是谁")→ `skill_view('wudao-theme-research')`,套用四象限判读(领涨/补涨/退潮/冷门) + 3 表交集
- 任何异常 → 自动按"主→备1→备2"降级
- **永远不假设数据可达** —— 用户期望是"鲁棒的股票分析",不是"脆弱的连问连修"

---

## 🆕 长内容转文档(刷屏防控)

⚠️ **用户反馈**:IM 消息刷屏 + 字符限制发不全

### 铁律:回答 > 1024 字时,可创建在线文档(仅当用户明确要求或 IM 环境支持时)

### 触发条件(满足任一即触发,且用户要求输出文档)
- 完整股票分析(基本面+技术+资金流+情绪+风险+操作建议)
- 字数 > 1024 字
- 多只票对比/列表
- 代码/Markdown 表格

### 执行步骤
1. 构造完整 Markdown 内容(标题/章节/表格/免责声明)
2. 若用户要求文档输出,调用 IM 平台的文档能力(按实际环境)
3. 本对话回复**短回执**:
   - 一句话核心结论
   - 文档标题
   - 文档 URL
   - "📄 详见在线文档"
4. **绝不刷屏**——主文超过 1024 字默认分段落直发,不自动调外部服务

### 短回执模板
```
📊 [股票名]分析完成

核心结论:[一句话]

📄 详见在线文档:[文档标题](URL)

⚠️ 风险提示:[一句话]
```

### 必须走文档的场景
- 场景 1(候选挖掘对比)/场景 3(单股完整诊断)
- 场景 5(事件驱动分析)/场景 6(组合优化报告)
- 场景 7(复盘报告)/场景 8(题材刚启动识别)
- 场景 9(纪律执行报告)

### 可以直接发的场景(短内容)
- 快速答疑(< 500 字)
- 盘中异动提醒(< 200 字)
- 数据点单查询(< 300 字)

## ⚡ TDX 实时校验层(2026-07-23 新增)

**为什么 TDX 这么重要**:
- TDX 是**唯一不限流**、**秒返**、**支持自然语言**的 MCP
- 盘中 9:00-15:00 任何价格判断前,**首选 TDX 拉实时 tick**
- 盘后 15:00-17:00 可用 ftshare intraday_kline 兜底

**4 个核心用法**:

```python
# 1. 实时价格(秒返)
mcp__tdx__tdx_wenda_quotes(question="002387 最新价")

# 2. 是否涨停 + 封单
mcp__tdx__tdx_wenda_quotes(question="000636 是否涨停 封单多少")

# 3. 自然语言选股(主力)
mcp__tdx__tdx_wenda_quotes(
    question="主板 流通市值30-300亿 涨幅5%-10% 量比>3",
    range="AG"
)

# 4. 题材/概念查询
mcp__tdx__tdx_wenda_quotes(
    question="商业航天概念股 主板 涨停",
    range="AG"
)
```

**与其他 MCP 的协同**:
| 场景 | TDX | wudao | ftshare | mx-ds | iFind |
|---|---|---|---|---|---|
| 实时 tick | ✅ 主源(秒返) | ⚠️ 9:15-10:30 限流 | ⚠️ 9:15-10:30 限流 | ❌ 无 | ⚠️ 延迟 |
| 涨停过滤 | ⚠️ 自然语言 | ✅ 结构化 | ✅ limit_up_pool | ⚠️ 自然语言 | ❌ 无 |
| 资金流 | ❌ 无 | ✅ intraday_main_flow | ✅ capital_flow | ⚠️ 自然语言 | ❌ 无 |
| 题材新鲜度 | ⚠️ 自然语言 | ✅ cls_news(hoursAgo) | ❌ 无 | ⚠️ 自然语言 | ✅ search_news |

**铁律**:任何"现在价多少/涨了没/涨停没"的判断,**TDX 优先**(唯一不限流的 MCP)。
