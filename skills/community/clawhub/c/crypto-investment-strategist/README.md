# Crypto Investment Strategist

## English

Professional cryptocurrency investment strategy skill for OpenClaw.

### Overview
This skill helps users make practical crypto decisions across spot investing, swing trading, leverage planning, and portfolio allocation. It focuses on actionable execution, staged deployment, and risk control instead of vague market commentary.

### Core capabilities
- Analyze BTC, ETH, and altcoins
- Support spot investing, swing trading, and leverage planning
- Generate staged entry and exit plans
- Add position sizing and portfolio allocation guidance
- Rank multiple assets from live market data
- Run a one-command workflow for ranking, allocation, and execution planning
- Log and review past analysis snapshots

### Best use cases
- "Should I buy BTC now?"
- "How should I allocate 10,000 USDT across BTC, ETH, and alts?"
- "Give me a swing trade plan for SOL"
- "Should I hold, reduce, or rotate out of this coin?"
- "Compare BTC, ETH, and SOL and tell me which one is the best candidate"

### Included scripts
- `scripts/fetch_crypto_data.py`
- `scripts/calculate_indicators.py`
- `scripts/score_assets.py`
- `scripts/allocate_portfolio.py`
- `scripts/auto_rank_assets.py`
- `scripts/log_analysis_snapshot.py`
- `scripts/review_snapshots.py`
- `scripts/run_investment_workflow.py`

### Quick examples
```bash
python3 scripts/auto_rank_assets.py --symbols BTC ETH SOL
python3 scripts/allocate_portfolio.py --capital 10000 --risk medium --regime uptrend
python3 scripts/run_investment_workflow.py --symbols BTC ETH SOL --capital 10000 --risk medium --regime uptrend
```

### Notes
- This skill is decision support, not guaranteed prediction.
- It is practical, risk-aware, and portfolio-oriented.
- The indicator workflow now uses a numpy-based implementation.
- If the indicator stack is refactored again later, the migration checklist is documented in `references/numpy-migration-plan.md`.

### Dependency setup
```bash
python3 -m pip install --user --break-system-packages numpy
python3 -c "import numpy; print(numpy.__version__)"
```

If you prefer a cleaner environment, use a virtual environment instead:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install numpy
python -c "import numpy; print(numpy.__version__)"
```

---

## 中文

这是一个面向 OpenClaw 的专业加密货币投资策略 skill。

### 简介
这个 skill 用来帮助用户处理加密货币里的实战决策，包括现货投资、波段交易、杠杆规划和组合配置。重点不是空泛分析，而是给出可执行的计划、分批部署方式和风控框架。

### 核心能力
- 分析 BTC、ETH 和各类山寨币
- 支持现货投资、波段交易、合约规划
- 生成分批买入和卖出计划
- 提供仓位控制和组合配置建议
- 基于实时市场数据对多个币种自动打分排序
- 支持一条命令完成排序、配置和执行计划
- 支持记录和复盘历史分析快照

### 适合场景
- “现在适合买 BTC 吗？”
- “1 万 USDT 怎么分配给 BTC、ETH 和山寨币？”
- “给我做一个 SOL 的波段计划”
- “这个币我是继续拿着、减仓还是换仓？”
- “帮我比较 BTC、ETH、SOL，哪个更值得优先配置？”

### 内置脚本
- `scripts/fetch_crypto_data.py`
- `scripts/calculate_indicators.py`
- `scripts/score_assets.py`
- `scripts/allocate_portfolio.py`
- `scripts/auto_rank_assets.py`
- `scripts/log_analysis_snapshot.py`
- `scripts/review_snapshots.py`
- `scripts/run_investment_workflow.py`

### 快速示例
```bash
python3 scripts/auto_rank_assets.py --symbols BTC ETH SOL
python3 scripts/allocate_portfolio.py --capital 10000 --risk medium --regime uptrend
python3 scripts/run_investment_workflow.py --symbols BTC ETH SOL --capital 10000 --risk medium --regime uptrend
```

### 说明
- 这个 skill 是决策辅助，不是确定性预测工具。
- 它强调实战、风控和组合视角。
- 指标链路现在已经切回 `numpy` 实现。
- 如果后续再次重构指标链路，可参考 `references/numpy-migration-plan.md`。

### 依赖安装
```bash
python3 -m pip install --user --break-system-packages numpy
python3 -c "import numpy; print(numpy.__version__)"
```

如果你想要更干净的环境，建议使用虚拟环境：

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install numpy
python -c "import numpy; print(numpy.__version__)"
```
