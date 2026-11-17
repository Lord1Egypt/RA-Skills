---
name: aggressive_growth_strategy
description: >
  激进成长选股与交易分析执行框架——将"周期性成长"方法论转化为可操作的选股筛选、个股深度分析和市场季节判断工具。
  当用户需要：按七标准筛选小盘成长股、对个股进行八步体系化分析（赛道→市值→成长→位置→指数→排除→建仓→卖出）、
  判断当前市场季节（春夏秋冬）与仓位策略、制定"小偷式"建仓与倒金字塔卖出计划时，加载此技能。
  与 aggressive-growth-investing 技能的关系：后者是"心法"（理论体系），本技能是"剑法"（执行工具）。
  核心数据源：四层降级架构（Tushare MCP > akshare > baostock > 东方财富API），通过共享模块 data_source.py 统一管理。
---

# 激进成长选股与交易分析框架

## Overview

本技能是 `aggressive-growth-investing`（激进成长投研体系）的**执行层**。后者记录了完整的心法与方法论（道、法、术、器四层），本技能将其转化为三套可执行的脚本工具：

1. **选股筛选器** (`scripts/screen_stocks.py`)：按七标准批量筛选候选标的
2. **个股分析器** (`scripts/analyze_stock.py`)：对单只标的执行八步深度分析
3. **市场季节判断器** (`scripts/judge_market.py`)：判断当前市场处于春夏秋冬哪一季

三个工具可独立使用，也可串联：先用季节判断器定大势 → 再用筛选器找出候选池 → 最后用个股分析器逐一深度分析。

## 触发条件

当用户需要以下任一操作时，加载此技能：

1. **选股筛选**："帮我筛选小盘成长股"、"按七标准选股"、"找50亿以下的科技股"
2. **个股分析**："分析一下这只股票"、"看看XXX值不值得买"、"评估一下XXX的10倍潜力"
3. **市场判断**："现在什么季节"、"大盘处于什么阶段"、"该不该加仓"
4. **交易计划**："帮我制定建仓计划"、"倒金字塔怎么卖"、"仓位怎么分配"

## 数据源策略（四层降级架构）

> 🔴 **数据校验铁律**：所有行情、财务、资金数据必须来自实际数据源调用结果。数据获取失败时必须如实标注"数据获取失败"，**严禁编造任何具体数值**。违反此规则视为重大事故。

### 降级优先级

```
Tushare MCP（主数据源） → akshare（第一备用） → baostock（第二备用） → 东方财富API（兜底）
```

所有数据获取通过共享模块 `scripts/data_source.py` 统一管理，脚本自动降级，无需手动切换。

### Tushare MCP 接口映射表

| 数据需求 | Tushare MCP 接口 | 原 baostock/akshare 接口 |
|---------|-----------------|------------------------|
| 日线行情(OHLCV) | `mcp_tushareMcp_daily` | `query_history_k_data_plus` |
| 每日指标(PE/PB/换手率/市值) | `mcp_tushareMcp_daily_basic` | `stock_zh_a_spot_em` |
| 财务指标(ROE/净利率等) | `mcp_tushareMcp_fina_indicator` | `query_profit_data` |
| 利润表 | `mcp_tushareMcp_income` | `stock_financial_abstract_ths` |
| 资产负债表 | `mcp_tushareMcp_balancesheet` | `query_balance_data` |
| 成长能力 | `mcp_tushareMcp_fina_indicator` | `query_growth_data` |
| 指数行情 | `mcp_tushareMcp_index_daily` | `query_history_k_data_plus` |
| 指数成分 | `mcp_tushareMcp_index_member` | `query_sz50/hs300/zz500_stocks` |
| 行业分类 | `mcp_tushareMcp_stock_basic` | `query_stock_industry` |
| 涨跌停价 | `mcp_tushareMcp_stk_limit` | 无直接对应 |
| 复权因子 | `mcp_tushareMcp_adj_factor` | baostock `adjustflag` 参数 |
| 交易日历 | `mcp_tushareMcp_trade_cal` | `tool_trade_date_hist_sina` |

**注意事项**：
- Tushare MCP 工具需 Gateway 重启后才能发现注册，新会话中检查 `mcp_tushareMcp_*` 前缀工具是否可用
- Tushare 日期格式为 `YYYYMMDD`（如 `20260805`），与 akshare（`YYYY-MM-DD`）和 baostock（`YYYY-MM-DD`）不同
- Tushare 部分高级接口需要更高积分权限，若返回权限不足错误，自动降级至 akshare/baostock
- **Agent 直接调用 Tushare MCP 优先**：当 Agent 执行分析时，应优先直接调用 `mcp_tushareMcp_*` 系列工具获取数据；Python 脚本（data_source.py）作为脚本内降级链路

### 各数据源的覆盖范围

| 数据需求 | 主数据源 | 第一备用 | 第二备用 | 兜底 | 说明 |
|---------|---------|---------|---------|------|------|
| K线行情 | Tushare `daily` | akshare | baostock K线 | 东财Push API | baostock个股K线最稳定，ETF仅近120天 |
| 行业分类 | Tushare `stock_basic` | baostock | - | - | 一次性获取全市场行业分类 |
| 盈利能力 | Tushare `fina_indicator` | baostock | akshare | 东财datacenter | ROE、净利率、毛利率 |
| 成长能力 | Tushare `fina_indicator` | baostock | akshare | 东财datacenter | 营收/利润同比增长率 |
| 指数数据 | Tushare `index_daily` | akshare指数API | baostock | 东财历史K线API | 上证、沪深300、创业板指 |
| 指数成分 | Tushare `index_member` | baostock | - | - | 判断个股是否被纳入指数 |
| 资金流向 | Tushare `moneyflow` | akshare | - | - | 主力资金净流入/流出 |
| 财务验证 | Tushare `income` | 东财datacenter | baostock | 东财新闻搜索 | 2026-07-31铁律要求交叉验证 |

### data_source.py 共享模块

`scripts/data_source.py` 是所有脚本统一的数据源入口，封装了四层降级逻辑：

- **`get_kline(code, days)`**：获取个股K线数据（前复权），自动降级
- **`get_index_kline(code, days)`**：获取指数K线数据，使用指数专用API（`stock_zh_index_daily` / baostock指数查询）
- **`get_stock_industry(code)`**：获取个股行业分类
- **`get_profit_data(code, year, quarter)`**：获取盈利能力数据（ROE、净利率等）
- **`get_growth_data(code, year, quarter)`**：获取成长能力数据（营收/利润同比增长率）
- **`get_index_stocks(index_code)`**：获取指数成分股列表
- **`get_spot(code)`**：获取实时行情快照（PE/PB/换手率/市值）
- **`verify_financial_data(code)`**：通过东方财富datacenter API交叉验证财务数据
- **`source_label(source)`**：返回数据源中文标签（传入 `SOURCE_AKSHARE`/`SOURCE_BAOSTOCK` 等常量）
- **`format_data_source_line(field, source)`**：格式化数据来源标注行

常量：`SOURCE_AKSHARE`="akshare", `SOURCE_BAOSTOCK`="baostock", `SOURCE_EASTMONEY`="eastmoney_api", `SOURCE_FAILED`="数据获取失败"

### baostock 使用要点

- 每次会话以 `bs.login()` 开始，`bs.logout()` 结束
- 股票代码格式：沪市 `sh.600519`，深市 `sz.000001`
- K线复权：`adjustflag="2"` 前复权（用于价格分析），`"3"` 不复权（用于原始价格）
- 财务数据按季度查询，报告期后约2个月延迟
- 非线程安全，批量查询用 for 循环，不用多线程
- Python路径：`/home/ubuntu/.hermes/hermes-agent/venv/bin/python3`

### 东方财富 API 兜底

当 Tushare MCP、akshare、baostock 均不可用时，通过 curl 调用东方财富 API：

- **实时行情**：`push2.eastmoney.com/api/qt/stock/get?secid={market}.{code}&fields=f43,f44,f45,f46,f47,f48,f50,f57,f58,f60,f116,f117,f162,f167,f170,f171`
  - 字段：f43=最新价, f44=最高, f45=最低, f46=今开, f47=成交量, f48=成交额, f50=量比, f57=代码, f58=名称, f60=昨收, f116=总市值, f117=流通市值, f162=PE, f167=PB, f170=换手率, f171=涨跌幅
  - secid 前缀：沪市 `1.`，深市 `0.`
- **财务数据验证**（2026-07-31铁律）：
  ```bash
  curl 'https://datacenter-web.eastmoney.com/api/data/v1/get?reportName=RPT_LICO_FN_CPD&filter=(SECUCODE="300769.SZ")&columns=ALL&sortColumns=REPORTDATE&sortTypes=-1&pageSize=10'
  ```
- **历史K线**：`push2his.eastmoney.com/api/qt/stock/kline/get?secid={market}.{code}&fields1=f1,f2,f3&fields2=f51,f52,f53,f54,f55,f56&klt=101&fqt=1&beg={YYYYMMDD}&end={YYYYMMDD}`

## 工作流一：选股筛选

### 适用场景
用户给出一批股票代码或一个行业方向，需要按"激进成长投研体系"七标准筛选出合格标的。

### 执行步骤

1. **确定筛选范围**：
   - 用户提供股票代码列表 → 直接筛选
   - 用户提供行业关键词 → 用 `query_stock_industry` 查找该行业所有股票
   - 用户提供板块方向（科技/消费） → 全市场扫描（较慢，约5-10分钟）

2. **运行筛选脚本**：
```bash
# 筛选指定股票列表
python3 scripts/screen_stocks.py --codes "sz.300308,sh.688146,sz.300769"

# 筛选指定行业
python3 scripts/screen_stocks.py --industry "半导体"

# 自定义筛选参数
python3 scripts/screen_stocks.py --codes "sz.300308" --max-mcap 50 --min-roe 10 --min-growth 15
```

3. **解读筛选结果**：
   - 脚本输出JSON，包含每只股票的七标准通过情况和综合评分
   - 评分维度：市值、位置、ROE、增长、估值、流动性、行业匹配度
   - 对通过的标的，进入工作流二进行深度分析

### 七标准筛选逻辑

| 标准 | 数据源 | 通过条件 | 评分权重 |
|------|--------|---------|---------|
| 1. 赛道 | data_source.get_stock_industry() | 属于科技或消费 | 10分 |
| 2. 市值 | data_source.get_kline() 计算 | 流通市值<50亿 | 20分（<30亿额外+10分） |
| 3. ROE | data_source.get_profit_data() | ROE≥8% | 15分（>15%额外+5分） |
| 4. 成长性 | data_source.get_growth_data() | 净利润同比≥10% | 15分（>30%额外+5分） |
| 5. 位置 | data_source.get_kline() | 价格在近250日50%分位以下 | 20分（<30%额外+10分） |
| 6. 指数路径 | data_source.get_index_stocks() | 未被纳入主要指数 | 5分 |
| 7. 排除项 | data_source.get_kline() isST+get_spot() PE | 非ST、股价>2元、PE>0 | 必要条件（不满足直接淘汰） |

## 工作流二：个股八步深度分析

### 适用场景
用户指定一只股票，需要按照体系进行全方位分析。

### 执行步骤

1. **运行分析脚本**：
```bash
python3 scripts/analyze_stock.py sz.300308
```

2. **脚本自动完成八步分析**：
   - Step 1: 赛道判断（行业属性、好产业标准验证）
   - Step 2: 市值评估（当前市值、10倍空间概率）
   - Step 3: 成长性分析（利润层级式增长检验）
   - Step 4: 位置判断（左侧/右侧、市场共识程度）
   - Step 5: 指数路径（是否在指数升维路径上）
   - Step 6: 排除检查（造假/退市/商誉/蹭热点风险）
   - Step 7: 建仓建议（日成交量、单日可买量、分批计划）
   - Step 8: 卖出预案（倒金字塔方案、目标市值）

3. **补充定性分析**：
   - 脚本输出量化数据后，Agent 需补充定性判断
   - 使用 `cn-web-search` 搜索最新公开信息和行业动态
   - 使用 `wechat-article-search` 搜索公众号深度研报
   - 融合量化数据与定性信息，生成完整分析报告

4. **输出报告**：
   - 按 `templates/stock_analysis_report.md` 模板格式输出
   - 报告必须包含数据来源标注和免责声明

## 工作流三：市场季节判断

### 适用场景
用户需要判断当前市场处于春夏秋冬哪一季，以及对应的仓位策略。

### 执行步骤

1. **运行季节判断脚本**：
```bash
python3 scripts/judge_market.py
```

2. **脚本输出**：
   - 主要指数（上证、沪深300、创业板）的均线排列、PE/PB分位
   - 成交量趋势（放量/缩量）
   - 季节判定：春耕/夏耘/秋收/冬歇
   - 仓位建议

3. **Agent 补充判断**：
   - 结合宏观面（降息周期、中美博弈、政策方向）
   - 参照10年周期律和阶梯式慢牛特征
   - 判断当前时间节点的风险事件（业绩报/政策窗口）
   - 综合输出季节判断和仓位建议

### 季节判定标准

| 季节 | 均线特征 | 成交量 | 位置 | 仓位 |
|------|---------|--------|------|------|
| 春耕 | MA20开始走平/上翘 | 温和放量 | 低位区（<30%） | 30-50%逐步布局 |
| 夏耘 | MA20>MA60，多头排列 | 持续放量 | 中位区（30-60%） | 50-70%持有+加仓 |
| 秋收 | MA20>MA60>MA250，加速 | 天量频现 | 高位区（>70%） | 70%→倒金字塔止盈 |
| 冬歇 | MA20<MA60，空头排列 | 持续缩量 | 下跌中 | 空仓或逆回购 |

## 工作流四：交易计划制定

### 建仓计划（"小偷式"买入）

当用户决定建仓某只股票时：

1. 获取该股近20日平均日成交量（从 `analyze_stock.py` 输出或直接查询）
2. 计算单日最大买入量 = 日均成交量 × 10%
3. 根据目标仓位制定分批建仓计划：
   - 第一批（试探仓）：目标仓位的20-30%
   - 第二批（确认仓）：趋势确认后加至50-60%
   - 第三批（主仓）：突破关键位后加至目标仓位
4. 每批间隔至少3-5个交易日，观察市场反应

### 倒金字塔卖出计划

当持仓已有盈利，需要制定卖出计划时：

1. 确定当前价格和目标市值
2. 制定倒金字塔卖出表：
   - 涨20%：卖出5%
   - 涨40%：卖出10%
   - 涨60%：卖出15%
   - 涨80%：卖出20%
   - 涨100%：卖出剩余的50%
3. 翻倍后先卖一半，收回本金
4. 最高点不可参考（碎骨成交），追求卖在合理区间

### 仓位策略（基于季节）

| 季节 | 总仓位 | 单只上限 | 策略 |
|------|--------|---------|------|
| 春耕 | 30-50% | 10% | 逐步布局，分批试探 |
| 夏耘 | 50-70% | 15% | 持有为主，确认后加仓 |
| 秋收 | 70%→递减 | 20% | 倒金字塔止盈，越涨越卖 |
| 冬歇 | 0-10% | - | 空仓或逆回购，保本为上 |

## 输出规范

### 个股分析报告格式
按 `templates/stock_analysis_report.md` 模板输出，必须包含：
1. 八步分析结果（每步有数据支撑）
2. 综合评分和评级（A/B/C/D）
3. 建仓建议和卖出预案
4. 风险提示
5. 数据来源标注
6. 免责声明

### 选股筛选报告格式
1. 筛选参数说明
2. 通过/未通过标的列表（含原因）
3. 通过标的的评分排名
4. 建议下一步行动

## 陷阱与注意事项

1. **市值估算精度**：baostock不直接提供总市值，通过换手率反推流通市值存在误差（±10-20%）。Tushare `daily_basic` 可直接获取 `total_mv`/`circ_mv`，优先使用。正式决策前应交叉验证（东方财富/同花顺）。

2. **财务数据延迟**：baostock/akshare 财务数据按季度更新，报告期后约2个月延迟。当前日期所在季度的数据不可用，需用上一季度。data_source.py 已自动处理季度选择逻辑。Tushare `fina_indicator` 更新更及时。

3. **ETF K线限制**：baostock ETF历史数据仅返回近120天。分析ETF需用东方财富历史K线API或 Tushare `fund_daily`。

4. **行业分类匹配**：各数据源行业分类标准不同（申万/中信/baostock自分类）。data_source.py 使用关键词匹配并自动融合多源结果，仍存在遗漏可能。

5. **数据真实性铁律**：严禁编造数据。任何字段获取失败必须如实标注"数据获取失败"，不得用估算值填充。违反此规则视为重大事故（详见底部🔒财务数据验证铁律）。

6. **小盘股流动性风险**：通过筛选的小市值股票可能流动性极差。建仓前必须检查日成交额，日成交<1000万的标的建仓难度极大。

7. **左侧布局的耐心**：体系要求左侧布局，但"左侧"不等于"抄底"。必须确认基本面无重大缺陷后再分批进入，不可因价格低就急于重仓。

8. **季节判断的综合考量**：脚本基于均线和成交量做量化判断，但冬季判断需要综合宏观信号（金融危机、政策转向、流动性收紧等）。脚本输出仅作参考，Agent需补充定性分析。

9. **指数数据陷阱**：akshare 的 `stock_zh_a_hist()` **不支持指数代码**（如 sh.000001），返回的是个股数据而非指数。data_source.py 中 `get_index_data()` 已使用指数专用API（`stock_zh_index_daily` / baostock指数查询）规避此问题。

10. **Tushare MCP 可用性检查**：新会话中先检查 `mcp_tushareMcp_*` 前缀工具是否已注册。若 Gateway 刚重启，MCP工具可能尚未发现，此时 data_source.py 自动降级至 akshare/baostock。Agent 直接调用 Tushare MCP 时也应做可用性判断。

11. **Python环境**：脚本需在hermes venv中运行。若 `import baostock` 或 `import akshare` 报错，执行：
```bash
/home/ubuntu/.hermes/hermes-agent/venv/bin/python3 -m ensurepip
/home/ubuntu/.hermes/hermes-agent/venv/bin/python3 -m pip install baostock akshare pandas numpy requests
```

## 依赖

- **Python包**：baostock, akshare, pandas, numpy, requests（hermes venv: `/home/ubuntu/.hermes/hermes-agent/venv/bin/python3`）
- **Tushare MCP（主数据源）**：MCP Server `tushareMcp` 已在 config.yaml 中配置，提供专业金融数据。若 MCP 连接失败则自动降级至 akshare/baostock/东方财富API
- **data_source.py**：共享数据源模块，所有脚本统一通过此模块获取数据，自动四层降级
- **关联技能**：
  - `aggressive-growth-investing`：理论体系（心法），本技能的方法论基础
  - `baostock`：数据源技能（第二备用），提供API用法参考
  - `cn-web-search`：个股公开信息搜索
  - `wechat-article-search`：公众号深度研报搜索
  - `market-watch-daily`：每日看盘框架（与本技能的季节判断互补）

### 资源

#### scripts/
- `data_source.py`：共享数据源模块，封装四层降级（Tushare>akshare>baostock>东财API），所有脚本统一入口
- `screen_stocks.py`：选股筛选脚本，按七标准批量筛选（通过 data_source.py 获取数据）
- `analyze_stock.py`：个股八步深度分析脚本（通过 data_source.py 获取数据+财务验证）
- `judge_market.py`：市场季节判断脚本（通过 data_source.py 获取指数数据）

#### templates/
- `stock_analysis_report.md`：个股分析报告模板

#### references/
- `screening_criteria.md`：选股七标准详解与评分规则

## 🔒 财务数据验证铁律（2026-07-31新增，最高优先级）

> 背景：2026-07-31发现cron持仓分析报告中出现严重幻觉--将德方纳米实际半年亏损3.91亿编造为"半年累亏超10亿元"。根因：防幻觉护栏仅覆盖行情数据，未覆盖财务数据。

1. **禁止凭记忆引用财务数据**：报告中涉及的任何公司财务数据（净利润、营收、亏损金额、毛利率、产能、产量、市占率、融资金额、IPO规模、回购金额等具体数字），严禁从模型记忆或训练数据中引用。
2. **财务数据必须API验证**：必须通过以下API之一验证后才能写入：
   - 东方财富datacenter：`curl 'https://datacenter-web.eastmoney.com/api/data/v1/get?reportName=RPT_LICO_FN_CPD&filter=(SECUCODE="代码.SZ")&columns=ALL&sortColumns=REPORTDATE&sortTypes=-1&pageSize=10'`
   - baostock：`bs.query_profit_data(code="sz.300769", year=2025, quarter=2)`
   - 东方财富新闻搜索：`curl 'https://search-api-web.eastmoney.com/search/jsonp?cb=jQuery&param=...'`
3. **无法验证则不写**：标注"⚠️ 财务数据未验证"，严禁用任何具体数字填充。宁可留白，不可编造。
4. **新闻数据需标注来源**：从新闻搜索中获取的财务数据，必须标注来源（如"据东方财富2026-07-28报道"）。
5. **禁止时间错配**：严禁将年度数据包装为"半年"或"季度"数据。引用时必须标注对应报告期。
6. **Tushare MCP 优先验证**：当 Tushare MCP 可用时，优先使用 `mcp_tushareMcp_fina_indicator`/`mcp_tushareMcp_income` 获取财务数据，再与东方财富datacenter交叉验证。两源数据不一致时，以公告日期更近者为准并标注差异。

## 版本记录

| 日期 | 版本 | 变更摘要 |
|------|------|---------|
| 2026-07-31 | v1.0 | 初版创建：三脚本（screen/analyze/judge）+ 模板 + 参考文档 |
| 2026-08-05 | v1.1 | 四层降级数据源架构：新增 `data_source.py` 共享模块（Tushare MCP > akshare > baostock > 东方财富API）；三脚本全部接入降级链路；SKILL.md 加入 Tushare 映射表、覆盖范围表、数据源标注规范；陷阱与注意事项更新为多数据源视角；财务验证铁律新增第6条（Tushare MCP 交叉验证） |