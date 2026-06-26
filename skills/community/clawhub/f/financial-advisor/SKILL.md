---
name: financial-advisor
description: Professional financial analysis and investment advisory skill with institutional-grade valuation capabilities. Use when users want to analyze stocks, funds, ETFs, compare investments, get market reviews, perform DCF valuation, comparable company analysis, financial statement modeling, competitive landscape analysis, macro-economic analysis, geopolitical impact assessment, or receive investment recommendations. Provides data collection, quantitative analysis, risk assessment, valuation modeling, macro-economic context, global event intelligence, news intelligence, and HTML report generation with real-time data.
cn_name: 金融数据分析与投资顾问
cn_description: 专业金融分析与投资顾问技能，具备机构级估值分析能力。当用户需要分析股票、基金、ETF、对比投资标的、DCF估值、可比公司分析、三表财务建模、竞争格局分析、宏观经济分析、国际局势评估、查看大盘复盘或获取投资建议时使用。提供数据采集、量化分析、风险评估、估值建模、宏观经济背景、国际事件情报、新闻情报和HTML报告生成。
author: Reconstructed by Learning
version: 1.0.0
tags: [finance, quantitative, data-analysis, stock, fund, ETF, visualization, investment-advisory, valuation, dcf, financial-modeling, macro-economics, geopolitical, event-driven, trending]
license: MIT
---

# 🏦 Financial Advisor - 专业金融分析与投资顾问

## 📋 技能概述

这是一个**机构级的金融分析技能**，提供从数据采集、量化分析、风险评估到投资建议的完整工作流程。

### 核心能力

1. **📊 数据采集** - 实时行情、历史K线、基本面、财务数据
2. **📈 技术分析** - MA、MACD、RSI、BOLL、KDJ等30+指标
3. **⚠️ 风险评估** - 夏普比率、最大回撤、VaR、索提诺比率
4. **💰 估值分析** - DCF模型、可比公司分析、三表财务建模
5. **🌍 宏观分析** - 经济周期、货币政策、地缘政治影响
6. **📰 新闻情报** - 全网热点采集、事件传导分析
7. **🤖 AI深度分析** - 结构化思考框架、投资决策推导
8. **📄 专业报告** - HTML交互式报告、可视化图表

---

## 🚀 使用流程

当用户请求分析某个股票/ETF/基金时，按以下流程执行：

### 阶段一：数据采集（Data Collection）

```bash
# 1. 创建数据目录
mkdir -p {OUTPUT_DIR}/financial_data/{SYMBOL}

# 2. 采集实时行情
python {skillDir}/scripts/fetch_stock_data.py \
  --symbol {SYMBOL} \
  --type realtime \
  --output-dir {OUTPUT_DIR}/financial_data/{SYMBOL} \
  --format csv

# 3. 采集历史K线（3年数据）
python {skillDir}/scripts/fetch_stock_data.py \
  --symbol {SYMBOL} \
  --type history \
  --period 3y \
  --output-dir {OUTPUT_DIR}/financial_data/{SYMBOL} \
  --format csv

# 4. 采集基本面数据
python {skillDir}/scripts/fetch_stock_data.py \
  --symbol {SYMBOL} \
  --type fundamental \
  --output-dir {OUTPUT_DIR}/financial_data/{SYMBOL} \
  --format csv

# 5. 采集估值数据
python {skillDir}/scripts/fetch_stock_data.py \
  --symbol {SYMBOL} \
  --type valuation \
  --output-dir {OUTPUT_DIR}/financial_data/{SYMBOL} \
  --format csv
```

**输出文件**：
- `{SYMBOL}_realtime.csv` - 实时行情
- `{SYMBOL}_history.csv` - 历史K线
- `{SYMBOL}_fundamental.csv` - 基本面
- `{SYMBOL}_valuation.csv` - 估值数据

---

### 阶段二：指标计算（Indicator Calculation）

```bash
# 1. 计算技术指标（MA、MACD、RSI、BOLL、KDJ等）
python {skillDir}/scripts/calculate_indicators.py \
  --input {OUTPUT_DIR}/financial_data/{SYMBOL}/{SYMBOL}_history.csv \
  --output {OUTPUT_DIR}/financial_data/{SYMBOL}/{SYMBOL}_indicators.csv \
  --indicator all

# 2. 计算风险指标（夏普、回撤、VaR等）
python {skillDir}/scripts/calculate_risk_metrics.py \
  --input {OUTPUT_DIR}/financial_data/{SYMBOL}/{SYMBOL}_history.csv \
  --output {OUTPUT_DIR}/financial_data/{SYMBOL}/{SYMBOL}_risk_metrics.json \
  --risk-free-rate 0.03
```

**输出文件**：
- `{SYMBOL}_indicators.csv` - 技术指标时间序列
- `{SYMBOL}_risk_metrics.json` - 风险指标摘要

---

### 阶段三：宏观与热点分析（Macro & Trending Analysis）

```bash
# 1. 采集全网热点（13个平台）
python {skillDir}/scripts/fetch_trending.py \
  --output {OUTPUT_DIR}/financial_data/trending.json \
  --platforms all \
  --max-age-hours 24

# 2. 宏观经济分析与热点分类
python {skillDir}/scripts/macro_analysis.py \
  --dashboard \
  --trending-json {OUTPUT_DIR}/financial_data/trending.json \
  --stock-name "{STOCK_NAME}" \
  --industry "{INDUSTRY}" \
  --reference-date {YYYY-MM-DD} \
  --news-max-age-days 30 \
  --output {OUTPUT_DIR}/financial_data/macro_dashboard.json
```

**输出文件**：
- `trending.json` - 全网热点原始数据
- `macro_dashboard.json` - 宏观分析与热点分类

---

### 阶段四：新闻搜索与情报分析（News Intelligence）

使用 `web_search` 工具搜索相关新闻（5-10条搜索）：

```
搜索关键词示例：
1. "{股票名称} 最新消息 {YEAR}"
2. "{公司名称} 财报 业绩 {YEAR}"
3. "{行业} 政策 监管 {YEAR}"
4. "{公司名称} 竞争 对手"
5. "{股票代码} 投资 分析 展望"
```

---

### 阶段五：AI深度分析（AI Deep Analysis）

基于采集的所有数据，创建 AI 分析文件：

**1. 创建 `ai_analysis.json`**（核心结论）

```json
{
  "summary": "一句话总结核心观点",
  "recommendation": "买入/持有/卖出",
  "target_price": {"low": XX, "mid": XX, "high": XX},
  "stop_loss": XX,
  "news_intelligence": {
    "key_events": [
      {"event": "事件描述", "impact": "影响分析", "direction": "利好/利空/中性"}
    ],
    "geopolitical": [...],
    "macro_policy": [...],
    "industry_dynamics": [...],
    "company_specific": [...],
    "market_sentiment": [...]
  },
  "impact_assessment": [
    {
      "event": "关键事件",
      "transmission": "传导路径（A → B → C → 股价）",
      "direction": "利好/利空",
      "strength": "强/中/弱",
      "duration": "时间周期"
    }
  ]
}
```

**2. 创建 `key_findings.json`**（投资策略）

```json
{
  "investment_thesis": "投资逻辑总结",
  "bull_case": ["看涨理由1", "看涨理由2", ...],
  "bear_case": ["看跌理由1", "看跌理由2", ...],
  "key_metrics": {
    "current_price": XX,
    "pe_ratio": XX,
    "pb_ratio": XX,
    ...
  },
  "catalysts": [
    {"catalyst": "催化剂", "timing": "时间", "impact": "影响"}
  ],
  "risks": [
    {"risk": "风险", "probability": "概率", "impact": "影响", "mitigation": "缓解措施"}
  ],
  "investment_strategy": {
    "recommendation": "具体操作建议",
    "entry_range": [XX, XX],
    "target_price": {"conservative": XX, "base": XX, "optimistic": XX},
    "stop_loss": XX,
    "position_sizing": "仓位建议",
    "time_horizon": "持有周期",
    "rebalancing": "再平衡策略"
  }
}
```

---

### 阶段六：生成专业报告（Report Generation）

```bash
python {skillDir}/scripts/generate_html_report.py \
  --title "{STOCK_NAME} 投资分析报告" \
  --template stock \
  --data-dir {OUTPUT_DIR}/financial_data/{SYMBOL} \
  --ai-analysis-json {OUTPUT_DIR}/financial_data/ai_analysis.json \
  --ai-deep-analysis-json {OUTPUT_DIR}/financial_data/key_findings.json \
  --output {OUTPUT_DIR}/{STOCK_NAME}投资分析报告.html
```

**输出**：
- 交互式HTML报告，包含：
  - 投资结论与评级
  - 核心指标速览
  - 实时行情数据
  - 历史走势K线图（ECharts）
  - 技术指标分析
  - 风险评估
  - AI深度分析
  - 新闻情报汇总
  - 投资策略建议

---

## 🎯 AI 深度分析框架

### 思考路径（Deep Analysis Framework）

当进行深度分析时，遵循以下结构化思考框架：

#### 1️⃣ **信息扫描（Information Scanning）**
- 识别关键数据点：价格、估值、增长率、市占率
- 识别异常信号：暴涨暴跌、成交量异常、高管变动
- 识别时间线索：财报发布、政策出台、行业事件

#### 2️⃣ **事件传导分析（Event Transmission）**
- 宏观 → 行业 → 公司 → 股价
- 政策 → 监管 → 商业模式 → 盈利
- 竞争 → 市场份额 → 收入 → 估值

示例：
```
ChatGPT爆发 → AI芯片需求激增 → HBM内存订单暴涨 
→ 三星/SK海力士业绩增长 → 韩国半导体出口强劲 
→ KOSPI上涨 → EWY受益
```

#### 3️⃣ **交叉验证（Cross-Validation）**
- 技术面 ↔ 基本面：价格走势是否匹配业绩
- 新闻 ↔ 数据：媒体报道是否与财务数据一致
- 宏观 ↔ 微观：经济周期是否支撑公司增长

#### 4️⃣ **风险矩阵（Risk Matrix）**
```
风险类别 | 概率 | 影响 | 缓解措施
-------|------|------|----------
短期调整 | 高  | 中  | 等待回调加仓
政局不稳 | 中  | 中  | 控制仓位
周期下行 | 中  | 高  | 跟踪订单数据
地缘风险 | 低  | 高  | 设置止损
```

#### 5️⃣ **决策推导（Decision Derivation）**
```
数据 → 观察 → 推理 → 结论 → 建议

示例：
数据：EWY涨175%，PE 17.5倍，回撤-15%
观察：AI芯片繁荣，机构上调目标，近期暴跌10%
推理：长期趋势向上，短期调整充分，估值合理
结论：持有评级，目标价145美元
建议：等待120-125美元加仓，止损115美元
```

---

## 📂 文件结构

```
financial-advisor/
├── SKILL.md                          # 本文件
├── README.md                         # 技能说明
├── requirements.txt                  # Python依赖
├── SCRIPTS_GUIDE.md                  # 脚本详细文档
│
├── scripts/                          # Python工具脚本
│   ├── fetch_stock_data.py          # 数据采集（yfinance）
│   ├── calculate_indicators.py      # 技术指标计算
│   ├── calculate_risk_metrics.py    # 风险指标计算
│   ├── fetch_trending.py            # 全网热点采集
│   ├── macro_analysis.py            # 宏观分析与热点分类
│   ├── search_service.py            # 新闻搜索服务
│   ├── calculate_valuation.py       # DCF/可比公司估值
│   ├── generate_html_report.py      # HTML报告生成
│   ├── market_review.py             # 市场复盘
│   ├── validate_execution.py        # 执行验证
│   ├── setup_dependencies.py        # 依赖检查
│   └── templates/                   # HTML模板
│
├── examples/                         # 使用示例
│   ├── single-stock-analysis.md     # 单股分析示例
│   └── multi-stock-compare.md       # 多股对比示例
│
└── references/                       # 参考文档
    ├── financial-indicators.md      # 金融指标说明
    ├── valuation-analysis.md        # 估值方法论
    ├── macro-event-framework.md     # 宏观事件框架
    ├── trading-discipline.md        # 交易纪律
    └── data-sources.md              # 数据源说明
```

---

## 🔧 关键脚本说明

### 1. `fetch_stock_data.py`
**功能**：从 yfinance 采集股票数据

**参数**：
- `--symbol`: 股票代码（如 AAPL、600519.SH）
- `--type`: 数据类型（realtime/history/fundamental/valuation/financial）
- `--period`: 历史周期（1y/3y/5y/max）
- `--output-dir`: 输出目录
- `--format`: 输出格式（csv/json）

**输出**：CSV格式的结构化数据

---

### 2. `calculate_indicators.py`
**功能**：计算技术指标

**支持指标**：
- 均线：MA5/10/20/30/60/120/250
- 趋势：MACD、BOLL、ATR
- 动量：RSI、KDJ
- 成交量：OBV
- 乖离率：BIAS

**输出**：带技术指标的时间序列CSV

---

### 3. `calculate_risk_metrics.py`
**功能**：计算风险指标

**输出指标**：
- 收益率：累计、年化、日均
- 波动率：日波动、年化波动
- 风险调整收益：夏普比率、索提诺比率、卡玛比率
- 风险度量：最大回撤、VaR(95%/99%)、CVaR
- 胜率统计：正收益天数、胜率、最大涨跌幅

---

### 4. `fetch_trending.py`
**功能**：采集全网热点

**数据源**（13个平台）：
- 基础7个：微博、知乎、百度、36氪、虎嗅、微信、今日头条
- 金融扩展：雪球、东方财富、财联社
- 科技扩展：CSDN、开源中国、掘金

**输出**：JSON格式的热点列表，包含标题、链接、热度、时间

---

### 5. `macro_analysis.py`
**功能**：宏观经济分析与热点分类

**核心功能**：
- 热点分类：按宏观/行业/公司维度分类
- 关键词提取：基于TF-IDF提取热点关键词
- 搜索查询生成：自动生成针对性搜索关键词
- 宏观数据：（需要akshare）利率、通胀、PMI等

**输出**：结构化的宏观分析仪表盘JSON

---

### 6. `generate_html_report.py`
**功能**：生成专业HTML报告

**模板类型**：
- `stock`: 单股分析报告
- `market`: 市场复盘报告
- `comprehensive`: 综合分析报告
- `compare`: 多股对比报告

**特性**：
- 响应式设计
- ECharts交互式图表
- K线图、技术指标可视化
- AI分析区块
- 打印友好

---

## 💡 使用示例

### 示例1：分析单只股票

**用户请求**：「分析贵州茅台」

**执行步骤**：
1. 采集数据：实时行情、历史K线、基本面
2. 计算指标：技术指标、风险指标
3. 采集热点：全网时政热点
4. 宏观分析：分类热点、生成搜索查询
5. 新闻搜索：5-10条相关新闻
6. 深度分析：创建 ai_analysis.json 和 key_findings.json
7. 生成报告：HTML报告

**交付物**：
- HTML投资分析报告
- 7个数据CSV/JSON文件
- AI分析结论文件

---

### 示例2：对比多只股票

**用户请求**：「对比茅台和五粮液」

**执行步骤**：
1. 分别采集两只股票的全部数据
2. 计算各自的指标
3. 使用 `--template compare` 生成对比报告
4. 重点对比：估值、增长率、盈利能力、风险指标

---

### 示例3：市场复盘

**用户请求**：「今天A股市场怎么样」

**执行步骤**：
1. 采集主要指数数据（上证、深成、创业板）
2. 采集行业板块数据
3. 采集龙虎榜、资金流向
4. 分析涨跌分布、成交量
5. 使用 `market_review.py` 生成复盘报告

---

## 📊 数据源

### 主要数据源
- **yfinance**：美股、港股、A股实时数据和历史K线
- **公开API**：热点榜单、新闻数据
- **Web Search**：补充新闻和深度报道

### 备用数据源
- 腾讯财经API（参考示例代码）
- 东方财富API
- 雪球API

---

## ⚠️ 注意事项

### 1. 执行顺序
**必须按顺序执行**：
1. 数据采集（CSV）
2. 指标计算（基于CSV）
3. 热点采集（trending.json）
4. 宏观分析（基于trending.json）
5. 新闻搜索
6. AI深度分析
7. 报告生成

### 2. 数据存储
- 所有数据文件存储在 `{OUTPUT_DIR}/financial_data/`
- 每个股票一个子目录
- CSV格式便于二次分析

### 3. AI分析质量
- 必须基于真实数据，不能编造
- 事件传导路径要清晰
- 风险评估要全面
- 投资建议要具体可操作

### 4. 报告质量
- 图表必须基于真实数据
- K线图自动生成（需要history.csv）
- 技术指标可视化
- 响应式布局，支持移动端

---

## 🎓 学习资源

### 技能开发
- 参考 `examples/` 目录的完整示例
- 阅读 `references/` 目录的方法论文档
- 查看 `SCRIPTS_GUIDE.md` 的详细脚本说明

### 金融知识
- `financial-indicators.md`: 技术指标详解
- `valuation-analysis.md`: 估值方法论
- `macro-event-framework.md`: 宏观分析框架
- `trading-discipline.md`: 交易纪律与风控

---

## 📝 版本历史

- **v1.0.0** (2026-03-11): 初始还原版本
  - 基于原始技能的使用记录还原
  - 包含完整的数据采集、分析、报告生成流程
  - 支持股票、ETF、基金分析
  - 集成宏观分析和新闻情报

---

## 📞 技术支持

如果在使用过程中遇到问题：
1. 检查 Python 依赖是否安装完整
2. 确认数据目录权限
3. 验证数据文件是否正确生成
4. 查看脚本输出的错误信息

---

## 📜 许可证

MIT License - 本技能为学习还原版本，仅供参考学习。

---

**🌟 祝你投资顺利！**
