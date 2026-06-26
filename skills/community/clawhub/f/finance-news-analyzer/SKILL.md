---
name: finance-news-analyzer
description: 财经新闻深度分析技能。从多个新闻源抓取内容，进行情感分析（利好/利空/中性）、影响评估（行业/公司/市场）、关键信息提取，生成专业投资简报。支持 A 股/港股/美股、行业板块、个股分析。Use when user asks to "分析财经新闻", "评估新闻影响", "今日财经简报", "这条新闻是利好还是利空", "总结本周行业动态", or provides financial news URLs for analysis.
---

# 财经新闻分析器

专业的财经新闻深度分析技能，帮助投资者快速理解新闻背后的投资信号。

---

## 🎯 核心功能

### 1. 多源新闻抓取
支持 28+ 新闻源（来自 news-aggregator-skill）：
- **全球科技**：Hacker News, GitHub, Product Hunt
- **中文媒体**：36 氪，华尔街见闻，腾讯新闻，微博热搜
- **AI/技术**：Hugging Face Papers, AI Newsletters
- **财经专项**：WallStreetCN, 东方财富，雪球

### 2. 情感分析
三层情感判断：
| 等级 | 标识 | 说明 |
|------|------|------|
| 强烈利好 | 🟢🟢 | 重大利好消息，可能显著推高股价 |
| 利好 | 🟢 | 正面消息，对股价有积极影响 |
| 中性 | ⚪ | 中性消息，影响有限 |
| 利空 | 🔴 | 负面消息，可能打压股价 |
| 强烈利空 | 🔴🔴 | 重大利空，可能引发大幅下跌 |

### 3. 影响评估
多维度影响分析：
- **市场层面**：大盘/板块/个股
- **行业层面**：科技/金融/消费/医疗/能源等
- **时间维度**：短期（1-3 天）/中期（1-4 周）/长期（3 月+）
- **置信度**：高（>80%）/中（50-80%）/低（<50%）

### 4. 关键信息提取
自动识别并结构化：
- 💰 金额数字（投资额、营收、利润）
- 📊 百分比（增长率、涨跌幅、占比）
- 👤 关键人物（CEO、高管、分析师）
- 🏢 公司名称（全称、简称、股票代码）
- 📅 时间节点（发布日期、截止期限、事件时间）
- 📍 地理位置（总部、工厂、市场区域）

### 5. 简报生成
支持多种输出格式：
- **快速简报**：3-5 条核心新闻 + 一句话点评
- **深度报告**：详细分析 + 数据支撑 + 风险提示
- **行业周报**：按行业分类 + 趋势总结
- **个股追踪**：特定公司的新闻聚合 + 情感趋势

---

## 🚀 快速开始

### 基本用法

```bash
# 分析今日财经新闻
/finance-news-analyzer --source all --limit 20

# 分析特定新闻源
/finance-news-analyzer --source wallstreetcn,36kr --limit 15

# 带关键词过滤
/finance-news-analyzer --keyword "AI,芯片，半导体" --source hackernews,github

# 分析特定股票相关新闻
/finance-news-analyzer --ticker "NVDA,TSLA,AAPL" --sentiment all

# 生成行业周报
/finance-news-analyzer --industry "科技，金融" --period weekly
```

### 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--source` | 新闻源（逗号分隔） | `all` |
| `--limit` | 每源最多新闻数 | `15` |
| `--keyword` | 关键词过滤 | 无 |
| `--ticker` | 股票代码过滤 | 无 |
| `--industry` | 行业分类 | 无 |
| `--sentiment` | 情感过滤（positive/negative/neutral/all） | `all` |
| `--period` | 时间周期（daily/weekly/monthly） | `daily` |
| `--output` | 输出格式（brief/full/industry/stock） | `brief` |
| `--lang` | 输出语言（zh/en） | `zh` |

---

## 📊 分析流程

### Step 1: 新闻抓取
```bash
python scripts/fetch_news.py --source <sources> --limit <n> --keyword "<keywords>"
```

输出：原始新闻 JSON 列表

### Step 2: 情感分析
```bash
python scripts/analyze_sentiment.py --input <news.json> --model <llm>
```

输出：带情感标签的新闻列表

### Step 3: 影响评估
```bash
python scripts/assess_impact.py --input <analyzed.json> --ticker-db references/ticker-map.md
```

输出：带影响评估的完整数据

### Step 4: 简报生成
```bash
python scripts/generate_briefing.py --input <assessed.json> --template <template.md> --output <report.md>
```

输出：最终投资简报

---

## 📁 输出示例

### 快速简报格式

```markdown
# 📈 财经新闻简报
**日期**: 2026-03-09 | **来源**: 华尔街见闻，36 氪 | **总数**: 15 条

---

## 🟢 利好消息 (5 条)

#### 1. [英伟达发布新一代 AI 芯片，性能提升 300%](https://...)
- **来源**: 华尔街见闻 | **时间**: 22:48
- **影响**: 🟢 利好 | **置信度**: 高
- **相关股票**: NVDA (+), AMD (-), INTC (-)
- **一句话**: 英伟达新芯片可能巩固 AI 芯片领导地位，利好供应链企业

#### 2. [特斯拉中国工厂产能突破新高](https://...)
- **来源**: 36 氪 | **时间**: 21:30
- **影响**: 🟢 利好 | **置信度**: 中
- **相关股票**: TSLA (+), 宁德时代 (+)
- **一句话**: 产能提升可能带动 Q1 交付量超预期

---

## 🔴 利空消息 (3 条)

#### 1. [美联储暗示继续加息](https://...)
- **来源**: 华尔街见闻 | **时间**: 20:15
- **影响**: 🔴 利空 | **置信度**: 高
- **相关板块**: 科技股 (-), 房地产 (-), 银行 (+)
- **一句话**: 加息预期可能压制成长股估值

---

## ⚪ 中性消息 (7 条)

...

---

## 💡 投资提示

1. **重点关注**: AI 芯片、新能源车产业链
2. **风险提醒**: 美联储政策不确定性
3. **明日事件**: 美国 CPI 数据发布
```

### 深度报告格式

```markdown
# 📊 深度分析报告：AI 芯片行业

## 核心观点

本周 AI 芯片行业利好消息占主导（60%），主要驱动因素为...

## 新闻情感分布

| 情感 | 数量 | 占比 |
|------|------|------|
| 🟢 利好 | 12 | 60% |
| ⚪ 中性 | 6 | 30% |
| 🔴 利空 | 2 | 10% |

## 关键事件时间线

- 3/9: 英伟达发布新芯片
- 3/8: AMD 宣布与微软合作
- 3/7: 英特尔财报不及预期

## 投资建议

**短期**（1-3 天）：关注 NVDA 供应链
**中期**（1-4 周）：观察美联储政策
**长期**（3 月+）：AI 基础设施持续看好

## 风险提示

1. 地缘政治风险
2. 技术迭代风险
3. 估值过高风险
```

---

## 🔧 脚本说明

### scripts/ 目录

| 脚本 | 功能 | 依赖 |
|------|------|------|
| `main.py` | 主脚本（完整工作流） | requests, beautifulsoup4 |
| `analyze_sentiment.py` | 情感分析（LLM 调用） | 支持多种模型（见下） |
| `database.py` | 数据持久化（SQLite） | sqlite3（内置） |
| `charts.py` | 图表生成（趋势图/饼图/热力图） | matplotlib |
| `scheduler.py` | 定时任务（自动运行） | 无 |
| `fetch_news.py` | 新闻抓取（复用 news-aggregator-skill） | requests, beautifulsoup4 |
| `assess_impact.py` | 影响评估（规则+LLM） | ticker-map.md |
| `generate_briefing.py` | 简报生成（模板渲染） | jinja2 |
| `stock_mapper.py` | 股票名称→代码映射 | ticker-map.md |

### 使用示例

#### 基础用法
```bash
# 运行完整工作流
python scripts/main.py --source wallstreetcn,36kr --limit 15

# 单独进行情感分析
python scripts/analyze_sentiment.py --input news.json --output analyzed.json

# 分析单段文本
python scripts/analyze_sentiment.py --text "英伟达发布新一代 AI 芯片"

# 指定模型
python scripts/main.py --model gpt-4o-mini
python scripts/main.py --model qwen-plus
python scripts/main.py --model ollama/llama3.1
```

#### 数据持久化
```bash
# 初始化数据库
python scripts/database.py init

# 查看统计信息
python scripts/database.py show-stats

# 查看情感趋势
python scripts/database.py trend --days 30

# 查看特定股票趋势
python scripts/database.py trend --ticker NVDA --days 30

# 导出数据
python scripts/database.py export --format csv
```

#### 图表生成
```bash
# 生成情感趋势图
python scripts/charts.py trend --input analyzed.json

# 生成情感分布饼图
python scripts/charts.py pie --input analyzed.json

# 生成行业分布图
python scripts/charts.py industry --input analyzed.json

# 生成股票热力图
python scripts/charts.py heatmap --input analyzed.json

# 生成所有图表
python scripts/charts.py all --input analyzed.json
```

#### 定时任务
```bash
# 添加每天 8 点运行
python scripts/scheduler.py add --time "08:00" --daily

# 添加每周一 8 点运行
python scripts/scheduler.py add --time "08:00" --weekday 1

# 查看任务列表
python scripts/scheduler.py list

# 手动运行任务
python scripts/scheduler.py run --id 1

# 删除任务
python scripts/scheduler.py remove --id 1
```

### 支持的模型

| 厂商 | 模型 | 环境变量 |
|------|------|---------|
| OpenAI | GPT-4o, GPT-4o Mini, GPT-3.5 | `OPENAI_API_KEY` |
| Anthropic | Claude 3.5/3 Opus/Haiku | `ANTHROPIC_API_KEY` |
| 阿里 | 通义千问 (Qwen-Max/Plus/Turbo) | `DASHSCOPE_API_KEY` |
| 百度 | 文心一言 (ERNIE-Bot) | `QIANFAN_AK` + `QIANFAN_SK` |
| 智谱 | GLM-4/3 Turbo | `ZHIPUAI_API_KEY` |
| Ollama | Llama 3, Qwen2.5, Mistral 等 | (本地运行，免费) |

**完整模型列表：** 详见 [references/supported-models.md](references/supported-models.md)

### references/ 目录

| 文件 | 用途 |
|------|------|
| `ticker-map.md` | 公司名↔股票代码映射表（美股/A 股/港股） |
| `industry-map.md` | 公司↔行业分类表（10+ 行业，150+ 公司） |
| `sentiment-rules.md` | 情感分析规则库（利好/利空信号） |
| `impact-patterns.md` | 影响评估模式库 |
| `config-example.md` | 配置文件示例（EXTEND.md 模板） |

### templates/ 目录

| 模板 | 用途 |
|------|------|
| `brief.md` | 快速简报模板（3-5 条核心新闻） |
| `full-report.md` | 深度报告模板（详细分析 + 数据支撑） |
| `weekly.md` | 行业周报模板（待实现） |
| `stock-track.md` | 个股追踪模板（待实现） |

---

## ⚙️ 配置说明

### 环境变量

```bash
# LLM API（情感分析用）
OPENAI_API_KEY=sk-xxx
# 或
ANTHROPIC_API_KEY=sk-ant-xxx

# 新闻源 API（可选）
NEWSAPI_KEY=xxx
ALPHA_VANTAGE_KEY=xxx  # 股票数据
```

### EXTEND.md（可选）

创建 `.baoyu-skills/finance-news-analyzer/EXTEND.md` 自定义默认配置：

```yaml
# 默认新闻源
default_sources:
  - wallstreetcn
  - 36kr
  - hackernews

# 默认输出格式
default_output: brief

# 默认语言
default_language: zh

# 关注股票列表
watchlist:
  - NVDA
  - TSLA
  - AAPL
  - 00700.HK
  - 600519.SS

# 情感分析模型
sentiment_model: gpt-4o-mini

# 置信度阈值
confidence_threshold:
  high: 0.8
  medium: 0.5
```

---

## 🎯 使用场景

### 场景 1: 早盘准备
```
"帮我分析昨晚到今早的财经新闻，找出对 A 股有影响的消息"
```
→ 输出：快速简报 + 重点关注股票

### 场景 2: 个股追踪
```
"分析一下特斯拉最近一周的新闻，是利好还是利空？"
```
→ 输出：个股追踪报告 + 情感趋势图

### 场景 3: 行业研究
```
"总结本周 AI 行业的重大事件，按重要性排序"
```
→ 输出：行业周报 + 关键事件时间线

### 场景 4: 新闻解读
```
"这条新闻对哪些股票有影响？[新闻链接]"
```
→ 输出：影响评估 + 相关股票列表

### 场景 5: 投资决策支持
```
"我持有 NVDA 和 AMD，最近的新闻对我的持仓有什么影响？"
```
→ 输出：持仓影响分析 + 操作建议

---

## 📝 情感分析规则

### 利好信号 🟢
- 营收/利润超预期
- 新产品发布/技术突破
- 重大合同签订
- 政策支持/补贴
- 高管增持/股票回购
- 并购重组（被收购方）
- 行业需求增长

### 利空信号 🔴
- 营收/利润不及预期
- 产品召回/质量问题
- 高管离职/减持
- 监管处罚/诉讼
- 行业需求下滑
- 竞争对手强势发布
- 宏观经济负面

### 中性信号 ⚪
- 常规财报发布（符合预期）
- 人事正常变动
- 日常业务更新
- 市场传言（未证实）

---

## 💡 最佳实践

### 1. 关键词优化
```
好： "AI 芯片，GPU, 英伟达，AMD"
差： "科技"（太宽泛）
```

### 2. 新闻源选择
```
A 股：wallstreetcn, 36kr, eastmoney
美股：hackernews, bloomberg, reuters
行业垂直：特定行业媒体
```

### 3. 时间窗口
```
日内交易：--period daily --limit 30
波段操作：--period weekly --limit 50
长期投资：--period monthly --industry <行业>
```

### 4. 交叉验证
```
重要新闻：对比 3+ 新闻源
情感判断：结合技术面 + 基本面
```

---

## ⚠️ 免责声明

本技能生成的分析仅供参考，不构成投资建议。投资有风险，决策需谨慎。

- 情感分析基于 NLP 模型，可能存在误差
- 新闻影响评估为概率性判断，非确定性预测
- 市场受多重因素影响，单一新闻不决定走势
- 请结合个人风险承受能力和专业顾问意见

---

## 🔗 相关技能

- **news-aggregator-skill** - 新闻抓取基础
- **stock-analyzer** - 股票技术分析
- **baoyu-translate** - 外文新闻翻译

---

## 📚 参考资料

- [ticker-map.md](references/ticker-map.md) - 股票代码映射
- [industry-map.md](references/industry-map.md) - 行业分类
- [sentiment-rules.md](references/sentiment-rules.md) - 情感分析规则
- [impact-patterns.md](references/impact-patterns.md) - 影响评估模式
