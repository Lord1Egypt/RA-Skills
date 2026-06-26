# AGENTS.md — BeerGaao 项目规范

## 1. 项目概述

BeerGaao 是一个 A 股量化分析 Agent 工具集，为 AI Agent 提供标准化的股票分析能力。

技术栈：Python 3.10+，pandas/numpy 数据处理，requests/akshare 必装，tushare（选装）/yfinance（选装）/longport（选装）多数据源，scikit-learn/xgboost/lightgbm 机器学习，backtrader 回测引擎，SQLite 状态持久化。

仓库结构：
```
BeerGaao/
├── stock_skill/           # 主包
│   ├── __main__.py        # CLI 入口（--analyze, --market, --backtest-bt 等）
│   ├── config.py          # 配置管理（环境变量加载）
│   ├── models.py          # 数据模型定义
│   ├── state.py           # SQLite 状态持久化
│   ├── risk.py            # 风控计算
│   ├── indicators.py      # 技术指标计算
│   ├── semantic.py        # 自然语言查询解析
│   ├── monitor.py         # 轮询监控
│   ├── tools/             # Agent 工具层（串联所有模块）
│   ├── strategies/        # 策略定义 + 参数校准 + Backtrader 适配
│   ├── factors/           # 因子基类 + 合成引擎
│   ├── backtest/          # 回测引擎
│   ├── providers/         # 数据源 + 缓存
│   ├── attribution/       # 策略归因
│   └── execution/         # 执行层
├── tests/                 # 测试套件
├── .env.example           # 环境变量模板
├── pyproject.toml         # 项目配置
└── requirements.txt       # 依赖清单
```

## 2. 快速命令

```bash
# 安装依赖
pip install -e ".[ml,dev]"

# 可选：安装 Tushare 数据源
pip install -e ".[tushare]"

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入配置（TUSHARE_TOKEN 为可选，仅 Tushare 数据源需要）

# 运行主程序
python -m stock_skill                    # 完整复盘
python -m stock_skill --analyze 600036.SH  # 分析个股
python -m stock_skill --market           # 市场概览
python -m stock_skill --backtest-bt 600036.SH --strategy MAStrategy

# 测试
python -m pytest tests/ -v

# 日志
tail -f stock_skill.log
```

环境变量配置：
- `.env` 文件位于项目根目录
- 启动脚本通过 `python-dotenv` 自动加载
- 关键变量：`TUSHARE_TOKEN`（可选，仅 Tushare 数据源需要）, `LOG_LEVEL`, `DB_PATH`

## 3. 后端架构

```
stock_skill/
├── tools/tools.py         # Agent 工具层，串联所有模块，返回标准化 JSON
├── strategies/            # 策略层
│   ├── strategies.py      # 策略定义 + @register 装饰器注册
│   ├── ensemble.py        # 集成引擎 + 市场状态
│   └── backtrader_adapters.py  # Backtrader 策略适配
├── factors/               # 因子层
│   ├── base.py            # 因子基类 + @register_factor 注册
│   └── *.py               # 具体因子实现
├── backtest/engine.py     # 回测引擎（三年历史数据回测）
├── providers/providers.py # 多数据源网关（tushare/东财 必装，yfinance/长桥 选装）
├── config.py              # 配置管理
├── state.py               # SQLite 持久化（信号历史、持仓）
├── risk.py                # 风控计算（止损、仓位）
├── models.py              # 数据模型（Signal, Position, FactorResult）
└── semantic.py            # 自然语言查询解析
```

核心子系统：
- **策略引擎**：10+ 传统策略 + ML 策略 + 集成引擎，支持参数自动校准
- **因子平台**：因子 IC 分析、策略归因、因子合成
- **数据网关**：整合东方财富（必装）、Tushare、Yahoo Finance、长桥 OpenAPI（选装），带缓存
- **回测系统**：基于 Backtrader，支持三年历史数据回测

## 4. 前端架构

本项目为纯后端 CLI 工具，无前端。通过 CLI 命令或自然语言查询交互。

## 5. 关键约定

1. **返回格式**：所有工具方法返回 `{"tool": "name", "status": "success|error", "data": {...}}`
2. **异常处理**：捕获 Exception，返回 error 状态，不抛出到调用方
3. **类型注解**：使用 `Dict[str, float]` 而非 `dict[str, float]`（兼容 Python 3.9-）
4. **延迟注解**：所有文件使用 `from __future__ import annotations`
5. **日志规范**：使用 `logging.getLogger(__name__)`，不使用 print
6. **策略注册**：新策略必须使用 `@register` 装饰器，继承 `Strategy`
7. **因子注册**：新因子必须使用 `@register_factor` 装饰器，继承 `Factor`
8. **配置管理**：所有配置通过环境变量或 `config.env`，硬编码禁止

## 6. 本地开发及验证流程

```
改 → 构建 → 启动 → 验证
1. 修改代码（遵循命名约定）
2. 运行测试：python -m pytest tests/ -v
3. 启动 CLI：python -m stock_skill --analyze <股票代码>
4. 检查日志：tail -f stock_skill.log
5. 验证输出：检查 JSON 格式和数据正确性
```

验证模板：
```bash
# 分析个股
python -m stock_skill --analyze 600036.SH

# 市场概览
python -m stock_skill --market

# 回测验证
python -m stock_skill --backtest-bt 600036.SH --strategy MAStrategy --start 2023-01-01 --end 2026-04-30
```

## 7. 质量检查

```bash
# 测试
python -m pytest tests/ -v

# 类型检查（可选）
mypy stock_skill/

# 代码格式（可选）
black stock_skill/ tests/
isort stock_skill/ tests/
```

## 8. 参考项目约定

- 策略类命名：`PascalCase` + `Strategy` 后缀（如 `MABreakoutStrategy`）
- 因子类命名：`PascalCase` + `Factor` 后缀（如 `PEFactor`）
- 工具方法命名：`snake_case`（如 `analyze_stock`）
- 配置项命名：`UPPER_SNAKE_CASE`（如 `STOP_LOSS_RATE`）
- 内部方法：`_` 前缀（如 `_run_backtest`）

## 9. 文档导航

| 文档 | 位置 | 说明 |
|------|------|------|
| 项目说明 | `README.md` | 完整功能介绍、回测结果、使用示例 |
| 因子参考 | `factor-reference.md` | 因子定义和计算方法 |
| 策略参考 | `strategy-reference.md` | 策略逻辑和参数说明 |
| 风控参考 | `risk-reference.md` | 风控规则和止损策略 |
| 技能定义 | `SKILL.md` | AI Agent 技能接口定义 |
| 配置模板 | `.env.example` | 环境变量配置示例 |
