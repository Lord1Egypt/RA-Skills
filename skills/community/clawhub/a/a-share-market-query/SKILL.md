---
name: "openclaw-market-intel"
description: "获取股票行情与新闻情报并结构化输出。用户要求查询个股/指数、新闻追踪或多源交叉验证时调用。"
user-invocable: true
disable-model-invocation: false
metadata: {"openclaw":{"emoji":"📈","homepage":"https://docs.openclaw.ai/tools/skills","skillKey":"openclaw-market-intel","requires":{"bins":["python3"]}}}
---

# OpenClaw Market Intel

## 目标

在用户查询股票、指数或市场主题时，统一拉取多源行情与新闻/搜索情报，输出可执行、可追溯、可降级的结构化结论。

## 何时调用

- 用户要查个股/指数最新行情与涨跌变化
- 用户要看相关新闻、舆情、催化与风险点
- 用户要求多源交叉验证，避免单源偏差
- 用户要快速生成“行情 + 新闻 + 风险提示”简报
- 用户明确要求输出策略研判（如趋势、风控、仓位倾向）

## 触发判定

- 用户明确“只查信息/不要建议”时，使用 `--mode info`
- 用户要求“给策略/给判断/给计划”时，使用 `--mode strategy`
- 用户未说明时，默认先输出信息版，再提示可切换策略版

## 数据源

### 行情数据源

- Eastmoney（A股/指数优先兜底）
- YFinance
- AkShare
- Tushare
- Pytdx
- Baostock

### 新闻/搜索数据源

- Tavily
- SerpAPI
- Brave
- Bocha
- MiniMax
- Local Fallback（自动兜底，不阻塞主流程）

### AI 分析通道（可选）

- AIHubMix
- Gemini
- OpenAI 兼容
- DeepSeek
- 通义千问
- Claude

## 执行流程

1. 识别用户意图：标的、市场（A/H/US）、时间范围、关注点
2. 行情采集：优先多源查询，支持失败回退
3. 新闻采集：优先用户指定源，未配置则跳过并降级
4. 情报融合：结构化汇总价格、涨跌、均线、事件与风险
5. 结论输出：一句话结论、关键风险、数据源与时间戳
6. 策略模式：补充策略类型、信号、动作与风险等级

## 执行脚本

- 脚本路径：`{baseDir}/market_intel.py`
- 运行环境：Python 3

### 命令清单

- `quote`：查询多源最新行情
- `history`：查询多源历史K线
- `news`：查询多源新闻/搜索
- `intel`：一键执行行情 + 历史 + 新闻，支持信息/策略双模式

### 快速示例

```bash
python3 {baseDir}/market_intel.py quote --symbol 欧菲光 --sources eastmoney,yfinance
python3 {baseDir}/market_intel.py quote --symbol 中国铝业 --sources yfinance
python3 {baseDir}/market_intel.py news --query "中国铝业 业绩" --sources minimax --max-results 3
python3 {baseDir}/market_intel.py intel --symbol 中国铝业 --query "中国铝业" --mode strategy --strategy cn_review --market-sources yfinance --news-sources minimax
```

### 参数说明

- `--mode info`：仅返回事实数据（行情/历史/新闻）
- `--mode strategy`：在事实数据基础上增加策略研判
- `--strategy`：`auto`、`ma_cross`、`ma_trend`、`bias_guard`、`wave`、`cn_review`、`us_regime`
- `--bias-threshold`：乖离率策略阈值，默认 `5.0`

### 环境变量

- `TAVILY_API_KEY`
- `SERPAPI_API_KEY`
- `BRAVE_API_KEY`
- `BOCHA_BASE_URL`、`BOCHA_API_KEY`
- `MINIMAX_BASE_URL`、`MINIMAX_API_KEY`
- `TUSHARE_TOKEN`
- `MARKET_INTEL_HTTP_RETRIES`（默认 3）
- `MARKET_INTEL_HTTP_BACKOFF`（默认 0.8）

## 稳定性与降级策略

- 每个数据源独立返回 `ok/error`，单源失败不影响整体结构输出
- 行情在关键源不可用时自动执行回退，输出 `fallback_source_used`
- 新闻源未配置时会标记“已跳过”，全部不可用时自动回退 `local_fallback`
- 保留统一 JSON 结构，避免下游消费失败

## 输出结构

### 基础字段

- `symbol` / `query` / `timestamp` / `type`
- `results.<source>.ok`
- `results.<source>.data | error`

### 策略字段（`mode=strategy`）

- `strategy_used`
- `signals`
- `summary`
- `action`
- `risk_level`
- `metrics`
- `data_basis`

## 输出模板

```markdown
## 市场情报简报
- 标的：<代码/名称>（<市场>）
- 时间：<本地时间>
- 一句话结论：<结论>

- 行情概览：
  - 最新价：<price>
  - 涨跌幅：<pct>
  - MA5/10/20：<values>
  - 量能变化：<volume_trend>

- 新闻与事件：
  - 主要事件 1：<title + source + time>
  - 主要事件 2：<title + source + time>
  - 舆情倾向：<偏多/中性/偏空>

- 关键位与纪律：
  - 支撑/压力：<levels>
  - 乖离率风险：<low/medium/high>
  - 操作检查：<满足/注意/不满足>

- 数据源：
  - 行情：<source_a>, <source_b>
  - 新闻：<source_c>, <source_d>

- 免责声明：仅供参考，不构成投资建议。
```

## 规则

- 默认多源交叉，不给单源绝对结论
- 明确区分事实与推断
- 若源间冲突，优先报告冲突并降低置信度
- 缺少关键数据时标注“数据不足”
- 输出避免夸张承诺，不使用“稳赚”等措辞
