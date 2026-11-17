# 7 大实战场景详细流程

## 场景 1:【候选挖掘】— "找几只股票看看"
**触发词**:选股、筛股、有哪些、推荐、低估、超跌、埋伏、机会、爆发

### 主流程
```
1. mx-ds 自然语言筛股(主)
   ↓ 失败
2. tdx 自然语言问句(备 1)
   ↓ 失败
3. wudao_a_stock 结构化筛股(备 2,需 market 过滤)
   ↓ 失败
4. 用 iFind EDB/Firecrawl 抓行业报告,人工挑
```

### 实战模板
```
query = "主板 + [市值] + [PE] + [涨跌幅] + [行业/题材] + [排除条件]"

例:
- "主板中小盘 + 流通 50-150 亿 + PE 0-30 + 近 5 日下跌 5-15% + 电子/科技 + 排除创业板和科创板和北交所"
- "主板 + 流通 100-300 亿 + PE-TTM < 25 + 所属行业 = 半导体 + 近 10 日主力净流入前 30"
- "主板 + 跌破 30 日线 + 流通 < 100 亿 + 周换手 > 5%"
```

### 输出格式
```
候选清单:
  票 1(代码): 价 XX, PE XX, 近5日 XX%, 行业
  票 2(代码): 价 XX, PE XX, 近5日 XX%, 行业
  ...
每个候选 2 句话逻辑
触发雷达:明天 9:25 集合竞价看开盘价
```

---

## 场景 2:【实时行情】— "XXX 现在多少钱"
**触发词**:价格、多少钱、今天涨多少、最新、现价

### 主流程
```
盘中 09:30-15:00:
  1. tdx(秒返)
2. 失败 → wudao_a_stock minute_data
3. 失败 → ftshare intraday_kline(可能限流)

盘后/夜间:
  1. iFind get_stock_performance
  2. ftshare daily_ohlc
```

### 实战代码(对一只票的快速查询)
```
tdx: question="示例个股A000XXX最新价"
iFind: query="示例个股A000XXX 今日行情"
FTShare: ftshare.intraday_kline(type='intraday_price', symbol='000XXX.XSHE')
```

### 多票同时查
```
如果用户要"用户的持仓现在多少钱":
- 一次性问 tdx_wenda_quotes,把 4 个代码放一个 question:
  question="示例个股A000XXX 示例个股B000XXX 示例个股C002XXX 示例个股D002XXX 最新价"
- TDX 实测可以 1 秒返回全部
```

### 输出格式
```
示例个股A(000XXX): 41.40 (-0.55%) 行业:电子-元件
示例个股B(000XXX): 10.82 (-0.83%) 行业:国防军工
...
```

---

## 场景 3:【基本面分析】— "公司基本面怎么样"
**触发词**:基本面、财报、业绩、估值、PB、ROE、毛利率、营业、主营

### 主流程
```
1. iFind get_stock_summary(一站式摘要,99% 够用)
   ↓ 缺什么
2. iFind get_stock_financials(详细财务指标)
   ↓ 缺产业链
3. wudao_a_stock stock_research_workflow(完整研究)
```

### 实战拆解(对"XXX 公司如何"的标准拆解)
```
第一波(摘要):
  iFind.get_stock_summary(query="XXX")

第二波(如果需要指标):
  iFind.get_stock_financials(query="XXX 财务指标")

第三波(风险与估值):
  iFind.get_risk_indicators(query="XXX VaR Sharpe Beta")

第四波(股东):
  iFind.get_stock_shareholders(query="XXX 大股东")
```

### 输出格式(6 维度卡片)
```
公司卡片:
  1. 主营: 90% MLCC 片式电容器
  2. 行业: 电子-元件
  3. 估值: PE-TTM 25, PB 2.5
  4. 业绩: 2026Q1 净利 +180%, H1 预告 +22%
  5. 财务: 负债率 18%, ROE 14%
  6. 股东: 控股股东 35%, 大基金持股 2%
风险: 行业景气下行 + 解禁压力 8%
```

---

## 场景 4:【资金面 / Capital Flow】— "主力怎么动"
**触发词**:主力、资金、流入、流出、超大单、大单、北向、聪明钱、龙虎榜

### 主流程(按时段)
```
13:00-15:00 / 15:00 后:
  1. wudao_a_stock intraday_main_flow(codes)
  2. wudao_a_stock capital_flow(flowType='stock')
  3. wudao_a_stock capital_flow(flowType='hsgt')(看北向)
09:30-10:30:
  1. wudao_a_stock 可能限流
  2. 改用 FTShare(成功概率较高)
  3. 都不行就用日 K + TDX 的 4 个价格点模拟
```

### 实战代码
```python
# 4 只持仓同时查
mcp__wudao_a_stock__intraday_main_flow(
    codes='000XXX,000XXX,002XXX,002XXX'
)
```

### 输出解读口诀
```
大单+超大单同向 in + 中小单 out = 机构吸筹  ✅
大单+超大单同向 out + 中小单 in = 机构派发  ⚠️
超大单 in 其他 3 档 out = 国家队护盘  🏛️
中单+小单 in + 大+超大 out = 游资接力  🎲
大单+小单同向 + 中单反向 = 多空分歧  ⚖️
```

---

## 场景 5:【事件驱动】— "为什么涨 / 怎么埋伏"
**触发词**:为什么涨、催化、涨价、大会、产能、订单、政策、降息、业绩预告

### 主流程
```
1. iFind EDB 验证涨价逻辑(数据)
2. wudao_a_stock market_catalyst_calendar(未来事件)
3. iFind news / wudao cls_news(消息面)
```

### 实战代码
```python
# 氟化工涨价验证(从历史到现在)
mcp__hexin_ifind_ds_edb_mcp__get_edb_data(
    query="R22 R134a 现货价格 2026-01 到 2026-07"
)

# 未来 30 天催化事件
mcp__wudao_a_stock__market_catalyst_calendar(
    startDate="2026-07-23",
    endDate="2026-08-15"
)

# 快讯
mcp__wudao_a_stock__cls_news(keyword="氟化工 涨价", hoursAgo=72)
```

### 输出模板
```
事件驱动分析报告:
  1. 涨价/催化事实
    - 商品 X 价格从 A 涨到 B (C%涨幅, 来源 EDB)
    - 行业大会时间 (来源 catalyst_calendar)
    - 政策事件 (来源 news)
  2. 受益链条
    - 上游: XXX(资源股)
    - 中游: YYY(加工股)
    - 下游: ZZZ(终端股)
  3. 情绪面验证
    - 板块资金净流入 X 亿
    - 涨停家数 X 只
  4. 候选清单
    - A: 代码 + 价 + PE + 5日涨幅 + 逻辑
```

---

## 场景 6:【持仓诊断 / 调仓】— "我 4 只票怎么调"
**触发词**:持仓、我的票、调仓、组合、仓位、加仓、减仓、止损

### 主流程
```
1. skill: a-share-expert 由用户按需加载
2. 获取 4 只票最新价 + 资金流 + 主力结构
3. 计算持仓的"真实波动率"(用 FTShare 拉 30-60 天日线)
4. 喂给 Riskfolio .optimization
5. 输出每只票的"你应该配多少"
6. 比对"你现在配多少"
7. 生成具体的减仓/加仓清单
```

### 实战代码
```python
import riskfolio as rp
import pandas as pd
import numpy as np

# Step 1: 拉 4 只票 32 天真实日线
# mcp__ftshare__daily_ohlc 每只一次,合并

# Step 2: 算日收益率
returns = close_prices.pct_change().dropna()

# Step 3: 跑 Riskfolio
port = rp.Portfolio(returns=returns)
port.assets_stats(method_mu='hist', method_cov='hist')
w_minvol = port.optimization(model='Classic', rm='MV', obj='MinRisk')

# Step 4: 提取权重(注意 API 返回 DataFrame,列名 'weights')
weights = w_minvol['weights']

# Step 5: 比对你的实际持仓
my_holdings = {'示例个股A': 0.20, ...}
target_total = 0.50  # 你想保持的总仓位

for stock in returns.columns:
    rec = weights[stock]
    my = my_holdings[stock]
    target = rec * target_total
    diff = my - target
    if abs(diff) > 0.02:
        action = '减仓' if diff > 0 else '加仓'
        print(f'{action} {stock}: 调整 {abs(diff)*100:.1f}%')
```

### 输出模板
```
持仓诊断报告:
  总仓位: 67% → 目标 50% (释放 17% 现金)  # 示例: 按用户实际持仓计算
  
  调整清单:
    减仓 示例个股A: 11.5% (从 20% → 8.5%)
    减仓 示例个股D: 18.3% (从 20% → 1.7%)
    保留 示例个股B: 18.3% (从 22% → 18%)
    保留 示例个股C: 21.5% (从 25% → 21%)
  
  减仓后保留弹药:用于 9.90 / 10.50 / 41.00 等关键位补仓
  
  风控规则:
    - 单票 ≤ 15%(波动率 >50% 的 ≤ 8%)
    - 总仓位 ≤ 60%
    - 永远留 20% 现金应对极端
```

---

## 场景 7:【盘后复盘】— "今天市场怎么样"
**触发词**:今天、复盘、盘面、收盘、涨停、情绪、热点

### 主流程(只能 13:00 后)
```
1. wudao_a_stock market_replay_workflow(date=今天) ← 一次性复盘
   ↓ 想要更细
2. wudao_a_stock limitup_review_workflow(date=今天) ← 涨停复盘
3. wudao_a_stock short_term_emotion() ← 短线情绪
4. mcp__hexin_ifind_ds_news_mcp__search_news + iFind 拉重要消息
5. 输出每天复盘文档 → IM/在线文档(可选)
```

### 输出模板
```
每日复盘报告(15:00-17:00 完成)

市场宽度:
  - 上涨家数 X / 下跌 Y / 平盘 Z
  - 涨停 X 只 / 跌停 Y 只
  - 两市成交额 X 亿

短线情绪:
  - 封板率 X%
  - 炸板率 Y%
  - 最高连板 X 板
  - 龙头: XXX(代码) YYY(行业)

主线题材(按资金流入排序):
  1. XXX 涨 X% 主力净流入 Y 亿
  2. XXX 涨 X% 主力净流入 Y 亿

风险点:
  - 高位股杀跌: XXX(代码)
  - 板块退潮: XXX

明日计划:
  - 关注: XXX / YYY
  - 持有: 4 只票按 [持仓诊断] 清单
  - 减仓: 风华 反弹至 42+
```

---

## 🎁 实战技巧速查

### 节省 token
- 用 `tdx_wenda_quotes` 一次问多只股票(问题拼接),比 N 次调用省 80%
- 只在确实有重大变化时才复查(免费版 iFind 一天 200 次)

### 提升数据质量
- 决策前必对源(至少 2 个数据源)
- 用 ts_millis 字段验证时间(避免缓存的旧数据)
- 输出时**永远带上时间戳**`(截至 14:30)`

### 避免大坑
- ⛔ 早盘 09:15-10:30 用 wudao_a_stock → 一定限流
- ⛔ 用 akshare → connection reset
- ⛔ 给创业板/科创板/北交所股票用主板 MCP → 一定被纳入"非主板"
- ⛔ 在不验证数据时直接做交易决策

### 关键时间节点
- **09:15-09:25**:集合竞价(只看竞价量,不预测)
- **09:30-10:00**:早盘博弈(主源 iFind + TDX)
- **10:00-11:30**:主战场(Wudao 主力全开)
- **13:00-14:30**:平稳期
- **14:30-15:00**:尾盘博弈(主力动向明确)
- **15:00-17:00**:复盘期(完整数据库落库)
