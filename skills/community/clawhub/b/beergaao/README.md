# BeerGaao

**胜率总是倍儿高，收益也嘛倍儿好**

股票量化分析 Agent 工具集

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/beergaao-blue.svg)](https://pypi.org/project/beergaao/)
[![Downloads](https://img.shields.io/pypi/dm/beergaao.svg)](https://pypi.org/project/beergaao/)

---

## 🌟 Introduction

[![BeerGaao](https://img.shields.io/badge/BeerGaao-股票量化分析-blue)](https://github.com/GanJiaKouN16/BeerGaao)

BeerGaao 是一个专为 股票市场设计的量化分析 Agent 工具集，为 AI Agent 提供标准化的股票分析能力。

BeerGaao 可以成为你的：

- 💰 **自动量化工厂**：10+ 传统策略 + ML 策略 + 集成引擎，自动生成交易信号
- 🤖 **智能分析 Agent**：支持自然语言交互，一键完成股票技术分析
- 📊 **多数据源网关**：整合东方财富（必装）、Tushare、Yahoo Finance、长桥 OpenAPI（选装）
- 🔬 **因子研究平台**：因子 IC 分析、策略归因、参数自动校准
- 📈 **回测验证系统**：三年历史数据回测，胜率 50%+，夏普比率 1.0+

---

## 🏆 Backtest Results

三年回测验证（2023-04-30 ~ 2026-04-30）：

| 指标 | 600036.SH 招商银行 | 000858.SZ 五粮液 | 688702.SH 盛科通信 |
|------|-------------------|-----------------|-------------------|
| 总收益率 | **+28.64%** | **+19.39%** | **+57.22%** |
| 年化收益率 | **+8.76%** | **+6.09%** | **+20.45%** |
| 最大回撤 | **12.31%** | 18.74% | 29.83% |
| 胜率 | **58.21%** | **54.68%** | 52.24% |
| 盈亏比 | **1.86:1** | **1.63:1** | **1.78:1** |
| 夏普比率 | 1.28 | 0.87 | **1.54** |
| 超额收益 | **+33.56%** | **+24.31%** | **+62.14%** |

---

## ⚡ Quick Start

### 🐍 环境要求

- Python 3.10+
- 操作系统：Windows / macOS / Linux

### 📦 安装

```bash
git clone https://github.com/GanJiaKouN16/BeerGaao.git
cd BeerGaao
pip install -r requirements.txt
cp config.example.env config.env
# 编辑 config.env 填入配置
```

### ⚙️ 配置

编辑 `config.env` 文件，填入以下配置：

```bash
# Tushare（可选，历史K线数据源）
# 安装：pip install tushare 或 pip install -e ".[tushare]"
TUSHARE_TOKEN=your_tushare_token_here

# 长桥 OpenAPI（可选，支持美股/港股）
LONGPORT_APP_KEY=your_longport_app_key_here
LONGPORT_APP_SECRET=your_longport_app_secret_here
LONGPORT_ACCESS_TOKEN=your_longport_access_token_here
```

> ⚠️ **安全提示**：`config.env` 包含敏感 Token，已被 `.gitignore` 排除，请勿提交到版本库。

### 🚀 运行

#### 命令行模式

```bash
python -m stock_skill                              # 完整复盘
python -m stock_skill --analyze 600036.SH           # 技术分析
python -m stock_skill --market                      # 大盘环境
python -m stock_skill --quote 300750.SZ             # 实时行情
python -m stock_skill --flow 600036.SH              # 资金流向
python -m stock_skill --breadth                     # 市场广度
python -m stock_skill --positions                   # 持仓查询
python -m stock_skill --perf                        # 回填信号绩效
python -m stock_skill --attribution                 # 策略归因分析
python -m stock_skill --monitor                     # 轮询监控
python -m stock_skill "招商银行怎么分析"             # 自然语言
```

#### Python API

```python
from stock_skill.tools.tools import StockTools

tools = StockTools()

# 分析（自动集成：传统策略 + 集成引擎 + ML + 因子IC + 参数校准）
result = tools.analyze_stock("600036.SH")

# 返回数据包含
# - signal:     最终交易信号（BUY/SELL/HOLD/WATCH）
# - ensemble:   集成引擎结果（市场状态/共识度/策略同意数）
# - ml_signal:  ML策略结果
# - factor_ic:  因子IC分析（各因子预测能力）
# - calibration: 参数校准结果
# - backtest:   回测指标（胜率/夏普/盈亏比）

# 策略归因
attribution = tools.strategy_attribution(days=30)

# 完整复盘
report = tools.full_review()
```

#### 多数据源使用

```python
from stock_skill.providers.providers import DataGateway

gateway = DataGateway()

# 使用 Tushare（需安装：pip install tushare）
df = gateway.get_kline("600036.SH", source="tushare")

# 使用 Yahoo Finance（支持美股/港股）
df = gateway.get_kline("AAPL.US", source="yahoo")

# 使用长桥 OpenAPI
quote = gateway.get_realtime_quote("700.HK", source="longport")
```

#### Agent 集成

`TOOL_SCHEMAS` 可直接用于 OpenAI Function Calling / Claude Tool Use：

```python
from stock_skill.tools.tools import TOOL_SCHEMAS
```

### 🧪 测试

```bash
python -m pytest tests/ -v
```

---

## 🏭 Scenarios

### 🎯 目标：股票量化分析 Agent

BeerGaao 旨在构建一个 股票量化分析 Agent，能够：

- 📊 **数据获取**：整合多数据源（东方财富（必装）、Tushare、Yahoo、长桥（选装）），获取实时行情、历史 K 线、资金流向
- 🔍 **技术分析**：自动计算 MA、MACD、RSI、KDJ、布林带等技术指标
- 🤖 **策略生成**：10+ 传统策略 + ML 策略 + 集成引擎，自动生成交易信号
- 📈 **回测验证**：三年历史数据回测，评估策略胜率、夏普比率、最大回撤
- 🛡️ **风险控制**：仓位管理、止损止盈、熔断机制、相关性检查

### 📈 支持场景

| 场景 | 功能 | 命令 |
|------|------|------|
| 💹 技术分析 | 单股深度分析，生成交易信号 | `--analyze 600036.SH` |
| 🌍 大盘环境 | 市场情绪、涨跌统计、量能分析 | `--market` |
| 📊 实时行情 | 多数据源实时报价 | `--quote 300750.SZ` |
| 💰 资金流向 | 主力资金、板块资金、龙虎榜 | `--flow 600036.SH` |
| 📋 完整复盘 | 一键生成当日复盘报告 | 无参数 |
| 🤖 自然语言 | 支持中文自然语言交互 | `"招商银行怎么分析"` |

---

## ⚙️ Framework

```
┌─────────────────────────────────────────────────────────────┐
│                      BeerGaao 架构                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Tushare    │  │  东方财富   │  │  Yahoo      │  选装   │
│  │  Provider   │  │  Provider   │  │  Provider   │         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │
│         │                │                │                 │
│         └────────────────┼────────────────┘                 │
│                          │                                  │
│                    ┌─────▼─────┐                            │
│                    │   Data    │                            │
│                    │  Gateway  │                            │
│                    └─────┬─────┘                            │
│                          │                                  │
│  ┌───────────────────────┼───────────────────────┐         │
│  │                       │                       │         │
│  ▼                       ▼                       ▼         │
│ ┌─────────┐      ┌──────────────┐      ┌─────────────┐    │
│ │ 技术指标 │      │   策略引擎   │      │  ML 策略    │    │
│ │ MA/MACD │      │ 10+ 传统策略 │      │ XGBoost/    │    │
│ │ RSI/KDJ │      │ + 集成引擎   │      │ LightGBM    │    │
│ └────┬────┘      └──────┬──────┘      └──────┬──────┘    │
│      │                  │                     │           │
│      └──────────────────┼─────────────────────┘           │
│                         │                                  │
│                   ┌─────▼─────┐                            │
│                   │  信号融合  │                            │
│                   │  去冗余    │                            │
│                   │  IC 过滤   │                            │
│                   └─────┬─────┘                            │
│                         │                                  │
│                   ┌─────▼─────┐                            │
│                   │  风险控制  │                            │
│                   │  仓位管理  │                            │
│                   │  止损止盈  │                            │
│                   └─────┬─────┘                            │
│                         │                                  │
│                   ┌─────▼─────┐                            │
│                   │  交易信号  │                            │
│                   │ BUY/SELL  │                            │
│                   │ HOLD/WATCH│                            │
│                   └───────────┘                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 核心模块

| 模块 | 职责 | 文件 |
|------|------|------|
| `providers/` | 数据源层，整合多数据源 | `providers.py` |
| `indicators.py` | 技术指标计算 | `indicators.py` |
| `strategies/` | 策略引擎，10+ 传统策略 + 集成 | `strategies.py`, `ensemble.py` |
| `factors/` | 因子分析，IC 评估 | `base.py`, `fundamental.py` |
| `backtest/` | 回测引擎 | `engine.py` |
| `risk.py` | 风险控制 | `risk.py` |
| `tools/` | Agent 工具层 | `tools.py` |

---

## 📃 Data Sources

| 数据源 | 覆盖范围 | 配置要求 | 用途 | 安装方式 |
|--------|---------|---------|------|---------|
| Tushare | 股票 | `TUSHARE_TOKEN` | 历史 K 线、基本面 | 必装 |
| 东方财富 | 股票 | 无需配置 | 实时行情、资金流向 | 必装 |
| Yahoo Finance | 全球 | 无需配置 | 美股/港股行情 | 选装：`pip install yfinance` |
| 长桥 OpenAPI | 美股/港股/股票 | `LONGPORT_*` | 实时行情（建议只读） | 选装：`pip install longport` |

---

## 🔒 Security

**凭证安全：**
- ✅ 所有凭证通过环境变量配置，代码中无硬编码 token
- ✅ `config.env` 已被 `.gitignore` 排除
- ⚠️ 建议使用只读 API Token，避免提供交易凭证

**数据安全：**
- ✅ 仅读取公开市场数据，不执行实际交易
- ⚠️ SQLite 数据库存储在本地，请妥善保管
- ⚠️ 不要加载来源不明的模型文件

**运行环境：**
- ⚠️ 建议在虚拟环境中安装运行
- ✅ 仅从官方仓库克隆代码

---

## 🤝 Contributing

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

---

## 📄 License

本项目采用 MIT License - 详见 [LICENSE](LICENSE) 文件

---

## ⚖️ Legal Disclaimer

The BeerGaao is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringence. The BeerGaao is aimed to facilitate research and development process in the financial industry and not ready-to-use for any financial investment or advice. Users shall independently assess and test the risks of the BeerGaao in a specific use scenario, ensure the responsible use of AI technology, including but not limited to developing and integrating risk mitigation measures, and comply with all applicable laws and regulations in all applicable jurisdictions. The BeerGaao does not provide financial opinions or reflect the opinions of GanJiaKouN16, nor is it designed to replace the role of qualified financial professionals in formulating, assessing, and approving finance products. The inputs and outputs of the BeerGaao belong to the users and users shall assume all liability under any theory of liability, whether in contract, torts, regulatory, negligence, products liability, or otherwise, associated with use of the BeerGaao and any inputs and outputs thereof.
