# 基金AI助手 | Fund AI Assistant

> 基金组合追踪与智能分析助手 | Fund Portfolio Tracker & AI Analyst

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-green.svg)](https://www.python.org/downloads/)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-v2026.3.24+-purple.svg)](https://github.com/openclaw/openclaw)

---

## 中文说明

### 是什么

基金AI助手是一个基于 OpenClaw 框架的基金投资辅助工具，支持**净值查询、技术分析、AI量化分析、多空辩论、组合管理、宏观监控**等功能。

完全本地运行，数据来源为东方财富，不构成任何投资建议。

---

### 核心功能

| 功能 | 说明 |
|------|------|
| 📊 技术分析 | MACD / KDJ / RSI / 布林带 / MA均线 + **VaR / Sortino / Calmar** |
| 🤖 AI 量化分析 | LLM 大模型，输出明确操作建议（买/卖/持有）+ 止盈/止损位 |
| ⚖️ 多智能体辩论 | 6角色博弈（舆情/风控/技术/动量/收益/宏观）→ 裁判博弈论裁定 |
| 📋 组合再平衡 | 自动检测仓位偏离，输出具体调仓指令 |
| 🎯 建仓时机推荐 | RSI + 布林带 + 趋势综合评分 |
| 🌡️ 基金关联热力图 | 两两相关性矩阵，可视化分散化效果 |
| 🌍 宏观事件监控 | 沪深300 / 人民币 / FOMC / LPR 自动预警 |

---

### 安装

#### 前置要求

- Python 3.10+
- OpenClaw v2026.3.24+（如需定时推送功能）
- LLM API Key（见下方配置）

#### 步骤

```bash
# 1. 克隆仓库
git clone https://github.com/tempest-01/fund-ai-assistant.git
cd fund-ai-assistant

# 2. 安装可选依赖（图表功能）
pip install -r requirements.txt

# 3. 配置环境变量
export LLM_MODEL="gpt-4o-mini"        # 必填：你的模型名称
export LLM_API_KEY="sk-xxx"          # 必填：你的 API Key

# 4. 复制配置文件
cp config.example.json config.json
cp positions.example.json positions.json
```

#### 验证安装

```bash
python3 analyzer.py list
python3 analyzer.py analyze
```

---

### 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `LLM_MODEL` | ✅ | 大模型名称，如 `gpt-4o-mini` |
| `LLM_API_KEY` | ✅ | 对应 API Key |
| `TAVILY_API_KEY` | ❌ | 宏观局势实时搜索 |
| `PUSH_WEBHOOK_URL` | ❌ | Webhook 推送（企业微信/飞书/Slack）|
| `BARK_PUSH_URL` | ❌ | iOS Bark 通知 |
| `PUSH_EMAIL` | ❌ | 邮件推送 |

> **未配置 LLM 相关变量**：AI 分析功能无法使用，脚本会直接退出并提示。

---

### 脚本速查

| 脚本 | 功能 |
|------|------|
| `analyzer.py` | 主入口：追踪管理 + 分析命令 |
| `ai_analysis.py` | AI 量化分析 |
| `debate_analyzer.py` | 多智能体辩论（6角色） |
| `rebalance.py` | 组合偏离检测 |
| `recommend.py` | 建仓/加仓时机建议 |
| `event_monitor.py` | 宏观事件监控 |
| `correlation_v2.py` | 基金关联热力图 |
| `fund_api.py` | 东方财富数据 API |
| `technical.py` | 技术指标计算 |

---

### 定时任务配置（参考）

```bash
# 宏观事件监控（早）
openclaw cron add --cron "0 8 * * 1-5" \
  --message "cd /path/to/fund-ai-assistant && python3 event_monitor.py --dry-run"

# 基金追踪分析（工作日）
openclaw cron add --cron "30 9 * * 1-5" \
  --message "cd /path/to/fund-ai-assistant && python3 analyzer.py analyze"

# 多智能体辩论（每周五）
openclaw cron add --cron "30 9 * * 5" \
  --message "cd /path/to/fund-ai-assistant && python3 debate_analyzer.py 000001"
```

---

### 文件结构

```
fund-ai-assistant/
├── .gitignore
├── config.example.json     # 追踪基金列表配置
├── positions.example.json  # 持仓记录配置
├── requirements.txt       # 可选依赖（Pillow / numpy / matplotlib）
├── llm.py                 # 统一 LLM 调用接口
├── analyzer.py            # 主入口
├── ai_analysis.py         # AI 量化分析
├── debate_analyzer.py     # 多智能体辩论框架
├── rebalance.py           # 组合偏离检测
├── recommend.py           # 建仓时机推荐
├── event_monitor.py       # 宏观事件监控
├── correlation_v2.py      # 基金关联热力图
├── fund_api.py            # 东方财富数据 API
├── technical.py           # 技术指标计算
├── chart_generator.py     # PIL 图表生成
├── macro_fetcher.py       # 宏观局势数据
├── positions.py           # 持仓记录管理
├── strip_color.py         # ANSI 颜色剥离
└── assets/               # 图表输出（自动生成）
```

---

## English Documentation

### What is This

Fund AI Assistant is an OpenClaw-based investment assistance tool for fund portfolio management, featuring **real-time valuation, technical analysis, AI quantitative analysis, multi-agent debate, portfolio rebalancing, and macro event monitoring**.

Runs entirely locally with data sourced from East Money (东方财富). For educational and reference purposes only — not investment advice.

---

### Features

| Feature | Description |
|---------|-------------|
| 📊 Technical Analysis | MACD / KDJ / RSI / Bollinger Bands / MA + **VaR / Sortino / Calmar** |
| 🤖 AI Quantitative Analysis | Any LLM provider — outputs actionable suggestions (buy/sell/hold) with take-profit/stop-loss levels |
| ⚖️ Multi-Agent Debate | 6-role game theory debate (sentiment/risk/technical/momentum/ratio/macro) → Judge verdict |
| 📋 Portfolio Rebalancing | Auto-detects allocation drift, outputs precise adjustment instructions |
| 🎯 Entry Timing | RSI + Bollinger + trend composite score |
| 🌡️ Correlation Heatmap | Pairwise correlation matrix for diversification analysis |
| 🌍 Macro Event Monitor | CSI300 / USD-CNY / FOMC / LPR alerts |

---

### Installation

#### Requirements

- Python 3.10+
- OpenClaw v2026.3.24+ (optional, for scheduled tasks)
- An LLM API Key (see environment variables below)

#### Steps

```bash
# 1. Clone the repository
git clone https://github.com/tempest-01/fund-ai-assistant.git
cd fund-ai-assistant

# 2. Install optional dependencies (for chart generation)
pip install -r requirements.txt

# 3. Configure environment variables
export LLM_MODEL="gpt-4o-mini"        # Required: your model name
export LLM_API_KEY="sk-xxx"           # Required: your API key

# 4. Copy config files
cp config.example.json config.json
cp positions.example.json positions.json
```

#### Verify Installation

```bash
python3 analyzer.py list
python3 analyzer.py analyze
```

---

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `LLM_MODEL` | ✅ | Model name, e.g. `gpt-4o-mini` |
| `LLM_API_KEY` | ✅ | Corresponding API key |
| `TAVILY_API_KEY` | ❌ | Tavily API for real-time macro search |
| `PUSH_WEBHOOK_URL` | ❌ | Webhook push (WeCom / Feishu / Slack) |
| `BARK_PUSH_URL` | ❌ | iOS Bark notification |
| `PUSH_EMAIL` | ❌ | Email push |

---

### Crontab / Scheduler (Reference)

```bash
# Macro event monitor (weekday morning)
openclaw cron add --cron "0 8 * * 1-5" \
  --message "cd /path/to/fund-ai-assistant && python3 event_monitor.py --dry-run"

# Fund tracking analysis (weekday morning)
openclaw cron add --cron "30 9 * * 1-5" \
  --message "cd /path/to/fund-ai-assistant && python3 analyzer.py analyze"

# Multi-agent debate (Friday morning)
openclaw cron add --cron "30 9 * * 5" \
  --message "cd /path/to/fund-ai-assistant && python3 debate_analyzer.py 000001"
```

---

## 灵感与来源 | Inspiration & Attribution

本项目的诞生得益于以下开源项目和思想的启发：

### 核心灵感

- **[astrbot_plugin_fund_analyzer](https://github.com/2529huang/astrbot_plugin_fund_analyzer)** — 多智能体辩论框架的来源。本项目借鉴了其多角色博弈架构，将其从股票领域扩展至基金分析，并增加了持仓管理、组合偏离检测等实用功能。
- **[OpenClaw](https://github.com/openclaw/openclaw)** — 作为底层 AI 助手框架，提供了 cron 调度、消息推送等关键基础设施能力。

### 数据来源

- **东方财富（East Money）** — 基金净值、历史数据、实时估值的数据源。
- **腾讯财经** — 沪深300 实时行情数据。

### 技术栈

- Python 3 标准库（`urllib`, `json`, `re` 等）— 无额外依赖即可运行基础功能
- PIL / Pillow — 图表生成
- NumPy — 相关性矩阵计算
- Matplotlib — 热力图可视化
- 任意 OpenAI 兼容 API — AI 分析能力

---

## 技术说明 | Technical Notes

- **无外部量化库依赖**：技术指标（MACD/RSI/KDJ/布林带等）均为纯 Python 实现
- **数据来源**：东方财富 `fundgz.1234567.com.cn` + `api.fund.eastmoney.com`
- **API 兼容性**：使用 OpenAI 兼容接口，理论上支持所有提供 `/v1/chat/completions` 的服务商
- **可选依赖**：Pillow / NumPy / Matplotlib 仅为增强功能，不安装也可运行基础分析

---

## 免责声明 | Disclaimer

本工具所有分析结果仅供参考，不构成投资建议。基金投资有风险，入市需谨慎。过往表现不代表未来收益。请在充分了解自身风险承受能力后，理性决策。

All analysis results from this tool are for reference only and do not constitute investment advice. Fund investments involve risk. Please make decisions based on your own risk tolerance.

---

*本 Skill 由 AI 辅助开发 | This Skill was developed with AI assistance*
