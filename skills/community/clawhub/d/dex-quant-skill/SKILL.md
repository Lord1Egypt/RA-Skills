---
name: dex-quant-skill
version: 3.47.1
description: |
  加密货币量化交易 AI Skill。用自然语言描述交易规则 → 生成策略脚本 → 服务器回测 → 参数优化 → 实时监控。
  支持 Binance/Hyperliquid 全币种，6 种优化算法（genetic/bayesian/grid/random/annealing/pso），异步进度推送。
  Use when user asks to: 推荐策略, 有什么策略, 推荐, 有现成的吗, 不会写, recommend, suggestions,
    创建策略, 创建一个策略, 创建, 建策略, 新策略, 写策略, 做策略, 生成策略, 设计策略, 帮我写, create strategy, new strategy, 弄个策略,
    回测, 测一下, 测试, 跑一下, 试试, 看看效果, backtest, test, 历史验证,
    优化, 调参, 优化参数, 优化策略, 优化下, optimize, tune,
    监控, 部署, 上线, 跑起来, 定时执行, 定时跑, 跑策略, 执行策略, 自动执行, 自动跑, 挂着跑, 定时任务, cron, run, deploy, monitor, 盯盘.
  This skill MUST be used for ANY request involving trading strategies, backtesting, parameter optimization, or strategy monitoring/execution.
  Also triggered when user replies with a number (1-6) following a skill prompt with numbered options.
  Do NOT use coding-agent for these tasks.
  ========== CRITICAL RULE ==========
  当用户要求创建/写/建/做策略时，你必须生成 PYTHON 脚本（使用 data_client + indicators 框架）。
  ⛔ 绝对禁止生成 TradingView Pine Script（//@version=5, strategy(), ta.ema(), ta.crossover()）。
  ⛔ 绝对禁止生成 MQL4/MQL5 或任何非 Python 的代码。
  策略脚本必须包含: from data_client import DataClient + from indicators import Indicators as ind + def generate_signals()
  详见下方 §1 的 Python 模板。
  ==================================
allowed-tools:
  - Bash
  - Read
  - Write
runtime:
  entry: SKILL.md
  setup: bin/setup
env:
  - DEX_QUANT_SERVER_URL
  - PROXY_URL
  - HYPERLIQUID_PRIVATE_KEY
  - HYPERLIQUID_ADDRESS
binaries:
  - python3
  - pip
  - pip3
  - node
  - npm
  - openclaw
---

## Preamble (run first)

```python
import subprocess, os, sys

BASE = '{baseDir}'
os.makedirs(os.path.join(BASE, 'strategies'), exist_ok=True)
os.makedirs(os.path.join(BASE, 'output'), exist_ok=True)

try:
    import httpx, loguru, matplotlib
    print("DEPS_OK")
except ImportError:
    print("INSTALLING_DEPS...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', '--break-system-packages',
                    'httpx', 'loguru', 'matplotlib'], capture_output=True)
    print("DEPS_INSTALLED")

print(f"BASE={BASE}")
```

If deps install fails → tell user to install manually and **STOP**.

## Workflow routing

Detect the user's intent and execute the matching workflow straight through.

| User says (任意一个即触发) | Workflow | Your FIRST response |
|-----------|----------|---------------------|
| "推荐策略" "有什么策略" "推荐" "有现成的吗" "不会写策略" "不知道怎么写" "有没有好的策略" "recommend" "suggestions" "哪个策略好" "试试什么" | **Recommend** | **直接推荐正收益策略（见下方 §0）** |
| "创建策略" "创建一个策略" "创建" "建策略" "新策略" "做一个策略" "写策略" "做策略" "生成策略" "设计策略" "帮我写一个" "create" "new strategy" "想做一个xx策略" "帮我做" "弄个策略" | Create | Extract params → generate **Python** script (§1)，⛔ 禁止 Pine Script |
| "回测" "测一下" "测试" "跑一下" "试试" "看看效果" "backtest" "test" "历史验证" "验证一下" "跑个回测" "看看能不能赚钱" | Backtest | Execute backtest code (§2) |
| "优化" "调参" "优化参数" "优化策略" "优化下" "optimize" "tune" "调优" "提升" "改进参数" | **Optimize** | **⚠️ 见下方硬规则** |
| "监控" "部署" "上线" "跑起来" "定时执行" "定时跑" "跑策略" "执行策略" "自动执行" "自动跑" "挂着跑" "定时任务" "cron" "run" "deploy" "盯盘" "实盘" "开始跑" "启动" | Monitor | Execute monitor setup (§4) |
| Spans multiple (e.g. "建策略然后回测") | Chain | §1 → §2 sequentially |

### ⚠️ 数字回复续接规则（最高优先级）

当用户只回复一个数字（如 "1" "2" "3" "4" "5" "6"）或数字+简短文字（如 "1 genetic" "选2"），**必须结合上一轮对话上下文判断**，不要当作新请求。

**数字上下文映射表：**

| 上一轮你问了什么 | 用户回复 | 你应该做什么 |
|-----------------|---------|-------------|
| 优化算法选择 (1-6) | "1" / "genetic" / "遗传" | 执行 §3 用 genetic 算法优化 |
| 优化算法选择 (1-6) | "2" / "bayesian" / "贝叶斯" | 执行 §3 用 bayesian 算法优化 |
| 优化算法选择 (1-6) | "3" / "grid" / "穷举" | 执行 §3 用 grid 算法优化 |
| 优化算法选择 (1-6) | "4" / "random" / "随机" | 执行 §3 用 random 算法优化 |
| 优化算法选择 (1-6) | "5" / "annealing" / "退火" | 执行 §3 用 annealing 算法优化 |
| 优化算法选择 (1-6) | "6" / "pso" / "粒子" | 执行 §3 用 pso 算法优化 |
| 监控/部署请求 | 任何 | 执行 §4 选择模式（信号监控 or 监控+自动下单） |
| 私钥/密钥/钱包设置 | 任何 | 执行 §4 Step 2b 安全链接流程 |
| 回测报告下一步 (1-6) | "1" / "genetic" | 执行 §3 用 genetic 算法优化 |
| 回测报告下一步 | "回测" / "再测一次" | 执行 §2 重新回测 |
| 回测报告下一步 | "部署" / "监控" / "跑起来" | 执行 §4 监控 |
| 推荐策略下一步 (1-3) | "1" | 执行 §2 回测 sol_rsi_momentum.py |
| 推荐策略下一步 (1-3) | "2" | 执行 §2 回测 btc_rsi_momentum.py |
| 推荐策略下一步 (1-3) | "3" | 执行 §1 引导用户创建新策略 |

**关键规则：**
- 用户回复纯数字时，**绝对禁止**当作新对话处理
- 必须回溯上一轮消息，找到对应的选项列表
- 找到后直接执行对应操作，不要再问"你是想选 xx 吗？"
- 如果上下文确实找不到选项列表，才问用户"请问你指的是？"

### ⚠️ "推荐策略"硬规则 — 必须逐字执行

当用户触发 Recommend 工作流（含"推荐策略"/"有什么策略"/"推荐"/"有现成的吗"/"不会写"/"不知道怎么写"/"哪个好"/"recommend" 等），你的回复**必须且只能是以下内容**（逐字复制，不要改写、不要加分析、不要讲策略类型教程）：

> 📊 这是我实测过有正收益的策略，直接用就行：
>
> 1️⃣ SOL RSI 动量策略 (sol_rsi_momentum.py)
> 🪙 SOLUSDT · 4h
> 📈 RSI>65 追涨 + RSI<35 追跌，EMA50 趋势过滤
> 💰 2025 回测: +2.27%
>
> 2️⃣ BTC RSI 动量策略 (btc_rsi_momentum.py)
> 🪙 BTCUSDT · 4h
> 📈 RSI>70 极端动量入场，EMA50 过滤，4x ATR trailing
> 💰 2025 回测: +1.40%（B 级评分）
>
> 选一个数字，我帮你回测看最新效果 👇
> 1 — 回测 SOL 策略
> 2 — 回测 BTC 策略
> 3 — 我想自己写一个新策略

**然后等用户回复，不要做任何其他事情。**

**禁止行为（违反任何一条 = 没有遵守 skill）：**
- ❌ 讲"趋势跟随、均值回归、突破策略"等策略类型教程
- ❌ 解释各类策略的优缺点
- ❌ 说"你可以试试 EMA 双均线"这种没有文件名的泛泛建议
- ❌ 自由发挥、改写模板、加自己的分析
- ❌ 推荐负收益策略
- ❌ 讨论自己该不该遵守 skill、反思流程（不要 meta 讨论，直接执行）

**❌ BAD — 以下是错误回复（绝对禁止）：**
> "最值得试的 4 类：1. 趋势跟随+回踩确认 2. EMA20/60+RSI+ATR 3. 突破策略 4. 波动率过滤趋势策略……"

> "我该先看 skill 里有没有推荐模板……我前面偏离了 skill 的执行纪律……"

**✅ GOOD — 唯一正确的回复就是上方引用块里的模板，逐字复制，不多不少。**

### ⚠️ "优化"硬规则 — 必须逐字执行

当用户触发 Optimize 工作流（含"优化"/"调参"/"调优"/"提升"/"改进参数"/"optimize"/"tune" 等），你的回复**必须且只能是以下内容**（逐字复制，不要改写、不要加分析、不要先给建议）：

> 好的，我们用服务器算法自动搜索最优参数。请选择优化算法：
> 1️⃣ genetic（遗传算法）← 推荐
> 2️⃣ bayesian（贝叶斯优化）
> 3️⃣ grid（网格穷举）
> 4️⃣ random（随机搜索）
> 5️⃣ annealing（模拟退火）
> 6️⃣ pso（粒子群）
> 回复数字或名称即可开始。

**然后等用户回复，不要做任何其他事情。**

用户回复后 → 执行 §3 Step 0 + Step 1 代码 → 调用 `run_optimization()`。

**禁止行为（违反任何一条 = 没有遵守 skill）：**
- ❌ 在列算法之前先分析策略哪里不好
- ❌ 自己修改策略代码的任何部分
- ❌ 给策略加新指标/过滤器
- ❌ 说"这个策略不值得优化"然后跳过
- ❌ 自己决定要重新设计而不是优化

**你没有权力判断策略值不值得优化。用户说优化，你就优化。**

**Automation posture:** prefer direct execution. Run the code and show results rather than listing steps. Use sensible defaults unless user specifies otherwise.

**Only stop to ask when:**
- Strategy logic is genuinely ambiguous (missing entry/exit conditions)
- Optimization target metric unclear
- Live deployment (always confirm — real money)

**Never stop for:**
- Choice of timeframe, symbol, capital (use defaults)
- Whether to show metrics (always show)
- Whether to retry on error (always retry once)

---

## ⚠️ Output Delivery Rule (Telegram)

用户通过 Telegram 使用本 Skill。你执行代码后，**必须把 stdout 输出作为 TG 消息发送给用户**，而不是仅仅"展示执行结果"。

### 核心流程

```
代码执行 → stdout 输出（print）→ AI 捕获 → 作为 TG 消息发送给用户
```

### 具体规则

1. **纯文本输出** — 执行代码后，将 `print()` 输出的格式化内容**原样作为 TG 消息发送**，不要包裹在代码块里，不要加额外解释
2. **图片 + caption** — 当代码生成了图片（`_equity_chart_path` / `_optimization_chart_path`），用 Bash 执行 `openclaw message send --path "<图片路径>" --caption "<_caption文本>"` 发送图片
3. **禁止只展示不发送** — 不要把执行结果放在代码块或"执行结果"框里给用户看，用户在 TG 上看不到这些
4. **禁止重述/改写** — `print()` 输出已经是格式化好的 tag 样式，直接发，不要用自己的话重写
5. **图片优先原则** — 有图片时只发图片消息（caption 含摘要），不要额外再发文字消息；无图片时发一条文字消息

### 消息类型对照

| 场景 | 发什么 | 怎么发 |
|------|--------|--------|
| 策略已生成 | 文本消息 | stdout 输出原样发送 |
| 回测完成 | **图片** + caption | 发图片附件，caption = `_caption`，不要额外发文字 |
| 优化完成 | **图片** + caption | 发图片附件，caption = `_caption`，不要额外发文字 |
| 监控启动/停止/列表/状态 | 文本消息 | stdout 输出原样发送 |
| 选择提示（算法/模式） | 文本消息 | 逐字发送模板内容 |

注意：回测和优化使用单代码块（`run_server_backtest` / `run_optimization`），执行过程中的 stdout（进度、提交确认等）不需要单独发送，最终只发图片+caption 即可。

---

## §1 Create Strategy

User describes a trading idea → you generate a Python script → save to `{baseDir}/strategies/`.

### Step 1: Extract parameters

From the user's description, extract:

```
SYMBOL:      Which coin pair         (default: BTCUSDT)
TIMEFRAME:   K-line interval         (default: 4h)
ENTRY:       What triggers buy/long
EXIT:        What triggers sell/close
RISK:        Stop loss, take profit, position sizing
FILTERS:     Volume, volatility, time-of-day
```

If entry/exit conditions are missing, **STOP** and ask. Everything else — use defaults silently.

### Step 2: Generate the script

Save to `{baseDir}/strategies/{name}_strategy.py`. The script is **never executed locally** — its source code is uploaded to the server as a string for backtesting.

```python
import sys
sys.path.insert(0, '{baseDir}/scripts')
from data_client import DataClient
from indicators import Indicators as ind
import numpy as np

def generate_signals(mode='backtest', start_date=None, end_date=None):
    dc = DataClient()
    df = dc.get_perp_klines("BTCUSDT", "4h", start_date, end_date)

    close = df["close"].values.astype(float)
    high  = df["high"].values.astype(float)
    low   = df["low"].values.astype(float)
    volume = df["volume"].values.astype(float)

    # --- Indicators ---
    ema_fast = ind.ema(close, 20)
    ema_slow = ind.ema(close, 60)

    # --- Signals ---
    signals = []
    lookback = 61  # max indicator period + 1
    for i in range(lookback, len(df)):
        if np.isnan(ema_fast[i]) or np.isnan(ema_slow[i]):
            continue
        if ema_fast[i] > ema_slow[i] and ema_fast[i-1] <= ema_slow[i-1]:
            signals.append({
                "timestamp": str(df.iloc[i]["datetime"]),
                "symbol": "BTCUSDT", "action": "buy", "direction": "long",
                "confidence": 0.7, "reason": "EMA20 cross up EMA60",
                "price_at_signal": float(df["close"].iloc[i]),
            })
        if ema_fast[i] < ema_slow[i] and ema_fast[i-1] >= ema_slow[i-1]:
            signals.append({
                "timestamp": str(df.iloc[i]["datetime"]),
                "symbol": "BTCUSDT", "action": "sell", "direction": "long",
                "confidence": 0.7, "reason": "EMA20 cross down EMA60",
                "price_at_signal": float(df["close"].iloc[i]),
            })
    return {"strategy_name": "EMA Cross Strategy", "signals": signals}
```

### Step 3: Output → 发 TG 消息

策略文件保存后，**发一条 TG 消息**给用户（不是代码块，直接发文本消息）：

> ✅ 策略已生成
> 📊 策略: {strategy_name}
> 🪙 交易对: {SYMBOL} · {TIMEFRAME}
> 📈 入场: {entry 一句话}
> 📉 出场: {exit 一句话}
> 📁 文件: {file_path}
> 要回测看看效果吗？

### All pre-built strategies (in `{baseDir}/strategies/`)

| Strategy file | Symbol | Style | 2025 回测 | Tested grade |
|--------------|--------|-------|-----------|--------------|
| `sol_rsi_momentum.py` | SOLUSDT | RSI>65 追涨 + RSI<35 追跌，EMA50 趋势过滤，trailing stop | **+2.27%** | C (7/14) |
| `btc_rsi_momentum.py` | BTCUSDT | RSI>70 极端动量入场，EMA50 过滤，4x ATR trailing | **+1.40%** | **B (10/14)** |
| `sol_kdj_swing.py` | SOLUSDT | KDJ 超卖反弹 + EMA50 趋势过滤，多空双向 | +2.09% | C (6/14) |
| `btc_trend_pullback.py` | BTCUSDT | EMA50 趋势 + EMA20 回踩入场，ATR trailing | -1.21% | C (8/14) |
| `btc_macd_trend.py` | BTCUSDT | MACD 金叉/死叉 + EMA100 方向过滤 | -1.84% | C (7/14) |

**只推荐前 2 个正收益策略。** 其余策略仅在用户主动问起时提及。

All strategies have `PARAMS` dict for optimization. Suggest: "可以用优化功能搜索最优参数"

### Sandbox rules (CRITICAL — violating these causes server backtest to fail)

| Allowed | Blocked |
|---------|---------|
| `sys`, `numpy`, `data_client`, `indicators` | `os`, `subprocess`, `socket`, `requests`, `httpx`, `pandas` |
| `ind.ema()`, `ind.sma()`, `ind.rsi()` | `df.rolling()`, `df.shift()`, `df.apply()` |
| `df["close"].values.astype(float)` | `df["close"].rolling(20).mean()` |
| `float(df["close"].iloc[i])` | `import pandas as pd` |
| `str(df.iloc[i]["datetime"])` | `df.index[i]` or row index `i` as timestamp |

### Signal fields

| Field | Required | Example |
|-------|----------|---------|
| `timestamp` | Yes | `str(df.iloc[i]["datetime"])` |
| `symbol` | Yes | `"BTCUSDT"` |
| `action` | Yes | `buy` / `sell` / `close` / `hold` |
| `direction` | Yes | `long` / `short` |
| `confidence` | Yes | `0.7` (0.0–1.0) |
| `reason` | Yes | `"EMA20 cross up EMA60"` |
| `price_at_signal` | Yes | `float(df["close"].iloc[i])` |
| `suggested_stop_loss` | No | stop loss price |
| `suggested_take_profit` | No | take profit price |

---

## §2 Backtest (server-side, free, unlimited)

**How it works:** Read strategy `.py` → pass source code as string → server fetches K-lines, executes script, simulates trades, returns metrics. You never run the strategy script locally.

```
LOCAL (单代码块)               SERVER
┌──────────────────┐  script  ┌─────────────────┐
│ run_server_      │ ───────▶ │ Fetch K-lines   │
│   backtest()     │          │ Execute script   │
│ (内部自动轮询)    │ ◀─────── │ Simulate trades  │
│ print_metrics()  │ metrics  │ Return report    │
└──────────────────┘          └─────────────────┘
```

### Step 1: Run backtest (单代码块，提交+轮询+报告一次完成)

**⚠ 必须用 `run_server_backtest()`！它内置了自动轮询和进度打印，一个代码块搞定全流程。**

**⛔ 禁止拆分为两个代码块！** 拆分后第二个代码块不会被执行，用户收不到结果。

```python
import sys
sys.path.insert(0, '{baseDir}/scripts')
from api_client import QuantAPIClient

with open('{baseDir}/strategies/xxx_strategy.py', 'r') as f:
    script_content = f.read()

client = QuantAPIClient(timeout=300.0)
bt = client.run_server_backtest(
    script_content=script_content,
    strategy_name="策略名",
    symbol="BTCUSDT",
    timeframe="4h",
    start_date="2025-01-01",
    end_date="2025-12-31",
    leverage=3,
    initial_capital=100000,
    direction="long_short",
)
```

`run_server_backtest()` 内部会自动：
1. 提交回测任务并打印 `📋 回测已提交: {job_id} | 策略名 (BTCUSDT 4h)`
2. 每 5 秒轮询进度，打印 `⏳ [Xs] stage (N%)`
3. 完成后自动调用 `print_metrics()` 生成报告 + 权益曲线 PNG

**⚠ 代码执行完毕后你 MUST 用 Bash 发送图片：**

```bash
openclaw message send --path "<bt._equity_chart_path的值>" --caption "<bt._caption的值 + 评分建议>"
```
**⛔ 禁止只打印图片路径当文字发。必须用 `openclaw message send --path` 发送图片文件。**

**⛔ 禁止行为：**
- ❌ 自己写分析段落（"结果"/"结论"/"我的判断"）
- ❌ 用自己的话重述指标数据
- ❌ 忽略 `_caption` 另起炉灶
- ❌ 只发文字不发图片
- ❌ 图片之外再额外发文字消息
- ❌ 拆分为两个代码块（submit + poll 分开执行）

### Backtest parameters

| Param | Default | Options |
|-------|---------|---------|
| `symbol` | `BTCUSDT` | Any Binance perpetual pair |
| `timeframe` | `4h` | `1m` `5m` `15m` `1h` `4h` `1d` |
| `start_date` | `2025-01-01` | YYYY-MM-DD |
| `end_date` | `2025-12-31` | YYYY-MM-DD |
| `leverage` | `3` | 1–125 |
| `initial_capital` | `100000` | USD |
| `direction` | `long_short` | `long_only` `short_only` `long_short` |

### Error handling

| Error | Auto-action |
|-------|-------------|
| `脚本安全检查未通过` | Fix strategy (sandbox violation) — see §1 Sandbox rules |
| `status: failed` | Retry once automatically, then report |
| 执行超时 | `run_server_backtest` 内部自动每 5 秒轮询，无需手动处理 |
| Network error / timeout | Retry once, then report |

### Display rules

`print_trades(bt)` prints full trade table — only needed if user asks for more details.

After completion, suggest next step **based on grade** (append to caption, keep concise):
  - A/B 级 → `#优秀` 效果不错，可以直接部署监控
  - C/D 级 → `#待优化` 建议用参数优化提升，推荐 genetic
  - F 级 → `#失败` 建议重新设计策略逻辑
  - Zero trades → `#无信号` 入场条件可能太严格

### Strategy evaluation standard

Server returns a scorecard with 7 metrics, each scored 0-2 (max 14):

| Metric | 🟢 优 (2分) | 🟡 及格 (1分) | 🔴 差 (0分) |
|--------|------------|--------------|------------|
| 收益率 | >20% | >0% | ≤0% |
| Sharpe | >1.5 | >0.5 | ≤0.5 |
| 最大回撤 | <10% | <20% | ≥20% |
| 胜率 | >50% | >35% | ≤35% |
| 盈亏比 | >1.5 | >1.0 | ≤1.0 |
| 交易数 | ≥30 | ≥10 | <10 |
| 爆仓 | 0次 | — | >0次 |

| Grade | Score | Conclusion | Meaning |
|-------|-------|------------|---------|
| A | 12-14 | approved | 优秀策略，可直接实盘 |
| B | 9-11 | approved | 良好策略，建议小仓实盘验证 |
| C | 6-8 | paper_trade_first | 及格策略，建议先模拟观察 |
| D | 3-5 | rejected | 较差策略，需要优化后再测 |
| F | 0-2 | rejected | 失败策略，建议重新设计 |

---

## §3 Optimize (server-side, free, unlimited)

**Reminder:** 触发表里的"优化硬规则"已经规定了你的第一条回复内容。到这里时，用户已经选好了算法。直接执行下面的步骤。

### Step 0: Check if strategy is parameterized

The strategy must have a `PARAMS` dict at the top. If not, refactor it first:

**Before (hardcoded — cannot optimize):**
```python
ema_fast = ind.ema(close, 20)
ema_slow = ind.ema(close, 60)
```

**After (parameterized — ready to optimize):**
```python
PARAMS = {'fast_ema': 20, 'slow_ema': 60, 'rsi_th': 55, 'sl_atr': 1.5, 'tp_atr': 3.0}

def generate_signals(mode='backtest', start_date=None, end_date=None):
    fast = PARAMS['fast_ema']
    slow = PARAMS['slow_ema']
    ema_fast = ind.ema(close, fast)
    ema_slow = ind.ema(close, slow)
```

If the strategy needs refactoring, do it silently, save, then continue.

### Step 1: Run optimization (单代码块，提交+轮询+报告一次完成)

**⚠ 必须用 `run_optimization()`！它内置了自动轮询和进度打印（25%/50%/90%里程碑），一个代码块搞定全流程。**

**⛔ 禁止拆分为两个代码块！** 拆分后第二个代码块不会被执行，用户收不到结果。

```python
import sys; sys.path.insert(0, '{baseDir}/scripts')
from api_client import QuantAPIClient

with open('{baseDir}/strategies/xxx_strategy.py', 'r') as f:
    script_content = f.read()

client = QuantAPIClient(timeout=600.0)
result = client.run_optimization(
    script_content=script_content,
    params=[
        {"name": "fast_ema", "type": "int",   "low": 10, "high": 30, "step": 5},
        {"name": "slow_ema", "type": "int",   "low": 40, "high": 80, "step": 10},
        {"name": "rsi_th",   "type": "int",   "low": 45, "high": 60, "step": 5},
        {"name": "sl_atr",   "type": "float", "low": 1.0, "high": 2.0, "step": 0.2},
        {"name": "tp_atr",   "type": "float", "low": 2.0, "high": 4.0, "step": 0.5},
    ],
    strategy_name="策略优化",
    symbol="BTCUSDT", timeframe="4h",
    start_date="2025-01-01", end_date="2025-12-31",
    fitness_metric="sharpe_ratio",
    max_combinations=100,
    method="genetic",
)
```

`run_optimization()` 内部会自动：
1. 提交任务并打印 `⏳ 优化任务已提交 (job_id: xxx)，共 N 种参数组合`
2. 每隔几秒轮询进度，在 25%/50%/90% 节点打印里程碑
3. 完成后自动调用 `print_optimization()` 生成报告 + 优化图表 PNG

**⚠ 代码执行完毕后你 MUST 用 Bash 发送图片：**

```bash
openclaw message send --path "<result._optimization_chart_path的值>" --caption "<result._caption的值>"
```
**⛔ 禁止只打印图片路径当文字发。必须用 `openclaw message send --path` 发送图片文件。**

**⛔ 禁止行为：**
- ❌ 自己写分析段落替代 caption
- ❌ 用自己的话重述参数和指标
- ❌ 忽略 `_caption` 另起炉灶
- ❌ 只发文字不发图片
- ❌ 图片之外再额外发文字消息
- ❌ 拆分为两个代码块（submit + poll 分开执行）

### Optimization methods

| Method | Best for | When to pick |
|--------|----------|--------------|
| `genetic` | Large param space | **Default** |
| `bayesian` | Few evaluations | User says "快速" |
| `grid` | ≤200 combos | User says "穷举" |
| `random` | High-dimensional | Exploratory |
| `annealing` | Escape local optima | Stuck in bad region |
| `pso` | Continuous params | All-float params |

### Fitness metrics

| Metric | Default |
|--------|---------|
| `sharpe_ratio` | **Yes** — risk-adjusted return |
| `total_return` | Raw total return |
| `max_drawdown` | Minimize drawdown |
| `win_rate` | Maximize win rate |
| `profit_factor` | Gross profit / gross loss |

---

## §4 Monitor & Execute (策略监控 — 服务器模式)

### Step 0: Pre-flight

If the strategy hasn't been backtested, warn: "这个策略还没有回测过，建议先回测。" If user insists, proceed.

### Step 1: 选择模式

When user triggers Monitor workflow, you MUST present this message verbatim:

> 📡 **策略监控部署** — 请选择模式：
>
> 1️⃣ **仅监控信号** — 服务器 7×24 运行，收到信号后你自己操作，不需要私钥
> 2️⃣ **监控 + 自动下单** — 服务器 7×24 运行，信号产生后自动下单到 Hyperliquid
>
> 两种模式都：免费 3 个策略、7×24、无需本地开机。
> 模式 2 需要通过安全链接配置钱包密钥（不在聊天里输入）。
> 回复 1 或 2 选择。

Wait for user to choose before proceeding.

### Mode 1: 仅监控信号（用户选了 1）

```python
import sys; sys.path.insert(0, '{baseDir}/scripts')
from api_client import QuantAPIClient

with open('{baseDir}/strategies/xxx_strategy.py', 'r') as f:
    script_content = f.read()

client = QuantAPIClient(timeout=60.0)
result = client.start_monitor(
    script_content=script_content,
    strategy_name="策略名",
    symbol="BTCUSDT",
    timeframe="4h",
    interval_seconds=14400,
)
print(f"✅ 监控已启动 | Job ID: {result['job_id']} | 配额 {result['quota_used']}/{result['quota_max']}")
```

### Mode 2: 监控 + 自动下单（用户选了 2）

**先配置密钥（安全链接） → 再启动监控。信号产生后服务器自动下单。**

```python
import sys; sys.path.insert(0, '{baseDir}/scripts')
from api_client import QuantAPIClient

client = QuantAPIClient(timeout=60.0)
vault = client.vault_status()
if not vault.get("has_key"):
    link = client.vault_setup_link()
    print(f"\n🔐 请在浏览器中打开以下链接，安全提交你的钱包私钥：")
    print(f"{link['url']}")
    print(f"\n⏰ 链接 30 分钟内有效。提交完成后回来告诉我「OK」。")
```

When user confirms key is set:

```python
import sys; sys.path.insert(0, '{baseDir}/scripts')
from api_client import QuantAPIClient

client = QuantAPIClient(timeout=60.0)
vault = client.vault_status()
if not vault.get("has_key"):
    print("❌ 密钥还没有配置，请先打开链接提交私钥")
else:
    with open('{baseDir}/strategies/xxx_strategy.py', 'r') as f:
        script_content = f.read()
    result = client.start_monitor(
        script_content=script_content,
        strategy_name="策略名",
        symbol="BTCUSDT",
        timeframe="4h",
        interval_seconds=14400,
    )
    net = vault.get("network", "mainnet")
    print(f"✅ 监控+自动下单已启动 | Job ID: {result['job_id']} | {net}")
    print(f"   产生信号后将自动下单到 Hyperliquid {'测试网' if net == 'testnet' else '主网'}")
```

### 管理命令

- 查看状态: `client.check_monitor(job_id)`
- 列出全部: `client.list_monitors()`
- 停止监控: `client.stop_monitor(job_id)`
- 查看密钥: `client.vault_status()`
- 删除密钥: `client.vault_delete()`
- 重新设置: `client.vault_setup_link()`

---

### 私钥安全规则

**⛔ 绝对不要让用户在聊天中发送私钥！**
如果用户主动发送了私钥，你必须立即回复：

> ⚠️ **安全警告**
>
> 请不要在聊天中发送私钥！私钥会留在聊天记录中，非常不安全。
> 如果这个私钥控制了真实资金，建议立即转移资产并更换钱包。
>
> 正确做法：我帮你生成一个安全链接，你在浏览器里提交私钥，不经过聊天。
> 回复「设置密钥」，我来帮你操作。

---

### Risk rules

| Rule | Default | Effect |
|------|---------|--------|
| 置信度 | ≥ 0.6 | 低于 0.6 的信号不执行 |
| 仓位限制 | 10% equity | 单笔不超过总权益的 10% |
| 并发限制 | 3 positions | 最多同时 3 个仓位 |
| 连续亏损 | 3 次暂停 | 连亏 3 笔自动暂停 (本地模式) |
| 冷却期 | 30 min | 两次交易间隔最短 (本地模式) |

**Always include risk disclaimer:** ⚠️ 实盘交易涉及真实资金风险，建议先用测试网 (HYPERLIQUID_TESTNET=1) 验证。

---

## API Reference

### DataClient (server-side, inside strategy scripts)

```python
dc = DataClient()
df = dc.get_perp_klines("BTCUSDT", "4h", start_date, end_date)   # perpetual futures
df = dc.get_spot_klines("BTCUSDT", "1h", start_date, end_date)   # spot
# Returns DataFrame: datetime, open, high, low, close, volume
```

Only use `get_perp_klines` and `get_spot_klines`. Do not invent method names.

### Indicators (server-side, inside strategy scripts)

| Method | Signature |
|--------|-----------|
| `ema` | `ind.ema(series, period)` |
| `sma` | `ind.sma(series, period)` |
| `rsi` | `ind.rsi(series, period)` |
| `macd` | `ind.macd(series, fast, slow, signal)` |
| `bollinger_bands` | `ind.bollinger_bands(series, period, num_std)` → (upper, middle, lower) |
| `atr` | `ind.atr(high, low, close, period)` |
| `kdj` | `ind.kdj(high, low, close, k, d, j)` |
| `crossover` | `ind.crossover(a, b)` |

All return **numpy arrays**. Use `arr[i]`, not `.iloc[i]`.

### QuantAPIClient (local, calls server)

| Method | Description |
|--------|-------------|
| `run_server_backtest(...)` | **⭐ 回测必用** — 提交+轮询+报告一次完成 |
| `submit_backtest(...)` | 仅提交任务（⛔ 不要单独使用，用 `run_server_backtest` 代替） |
| `check_backtest(job_id)` | 仅查询状态（⛔ 不要单独使用，用 `run_server_backtest` 代替） |
| `wait_backtest(job_id)` | 仅轮询等待（⛔ 不要单独使用，用 `run_server_backtest` 代替） |
| `run_optimization(...)` | **⭐ 优化必用** — 提交+轮询+报告一次完成，内置进度打印 |
| `submit_optimization(...)` | 仅提交任务（⛔ 不要单独使用，用 `run_optimization` 代替） |
| `check_optimization(job_id)` | 仅查询进度（⛔ 不要单独使用，用 `run_optimization` 代替） |
| `print_metrics(result)` | Display backtest report card |
| `print_optimization(result)` | Display optimization report (auto-called) |
| `start_monitor(script, name, symbol, timeframe, interval)` | 启动服务器监控（最多 3 个同时运行） |
| `check_monitor(job_id)` | 查看监控状态 + 最近信号 |
| `list_monitors()` | 列出我的所有监控任务 |
| `stop_monitor(job_id)` | 停止监控任务 |
| `vault_setup_link()` | 生成一次性安全链接，用户在浏览器中提交私钥 |
| `vault_status()` | 查询密钥是否已配置 |
| `vault_delete()` | 删除已存储的密钥 |
| `print_trades(result)` | Display trade records (only when user asks) |

### Quota

| Feature | Limit |
|---------|-------|
| Strategy generation | Unlimited, free |
| Backtest | Unlimited, free |
| Optimization | Unlimited, free |
| Live monitoring | 3 slots |

---

## NEVER do these

| Forbidden | Why | Correct |
|-----------|-----|---------|
| Run strategy script locally for backtest | Server runs it | `run_server_backtest(script_content=...)` |
| `import os/subprocess/socket` in strategy | Sandbox blocks them | Only `sys`, `numpy`, `data_client`, `indicators` |
| `df.rolling()`, `df.shift()`, `df.apply()` | Server pandas restricted | Use `ind.ema()`, `ind.sma()` etc. |
| Install numpy/pandas for backtest | Server has them | Only `httpx loguru matplotlib` locally |
| Build local backtest engine | Server already has one | Use `run_server_backtest()` |
| 拆分为两个代码块 (submit→poll) | 第二个代码块不会被执行 | 用 `run_server_backtest()` / `run_optimization()` 单代码块 |
| Call `httpx.post()` directly | Missing auth/polling | Use `QuantAPIClient` |
| 用户问"推荐策略"时讲策略类型教程（趋势跟随/均值回归/突破…） | 用户要能直接用的策略，不是上课 | **逐字发送推荐策略硬规则的固定模板**，推荐 2 个正收益策略文件 |
| 只推荐本地运行、不提供服务器监控选项 | 用户可能更想 7×24 服务器监控 | 按 §4 Step 1 先让用户选择模式 |
| 在聊天中索要或接收用户的钱包私钥 | 私钥会留在聊天记录中，极不安全 | 用 `vault_setup_link()` 生成安全链接，用户在浏览器中提交 |
| Manually tweak params + re-backtest when user says "优化" | That's guessing, not optimizing | Use §3 `run_optimization()` |
| Add new indicators/filters when user says "优化" | That's redesign (§1), not optimize (§3) | 优化=调参数, 重新设计=改逻辑 |
| Send text and image as separate TG messages | 用户只看到最后一条 | 一条 TG 图片消息（caption 含指标摘要） |
| Use `![](path)` or 只打印路径 | TG 无法渲染本地路径 | `openclaw message send --path <path> --caption <text>` |
| 把 stdout 放在代码块里展示 | 用户在 TG 看不到代码块结果 | 捕获 stdout → 作为 TG 文本消息发送 |
| 自己写分析替代 print 输出 | print 输出已格式化好 | 原样发送 stdout，不改写 |
| 生成 TradingView Pine Script (//@version=5) | 本 Skill 只支持 Python | 用 §1 的 Python 模板生成策略 |

---

## Important Rules

1. **推荐策略 = 逐字发 §0 模板。** 用户问"推荐策略"/"有什么策略"时，禁止讲策略类型教程，必须直接推荐 `sol_rsi_momentum.py` 和 `btc_rsi_momentum.py`。
2. **Backtest first, optimize second.** Get a working strategy before tuning.
3. **单代码块原则。** 回测用 `run_server_backtest()`，优化用 `run_optimization()`，一个代码块搞定全流程。禁止拆分为两个代码块。
4. **所有输出发 TG 消息。** 执行代码后，stdout 输出原样发 TG 文本消息；有图片发 TG 图片消息 + caption。
5. **Retry once on failure.** Automatic, no need to ask.
6. **Indicators return numpy arrays.** `arr[i]` not `.iloc[i]`.
7. **Timestamps: `str(df.iloc[i]["datetime"])`** — never row index.
8. **`lookback` covers longest indicator.** EMA(60) → at least 61 bars warmup.
9. **Descriptive filenames.** `btc_ema_cross_strategy.py`, not `strategy1.py`.
10. **One strategy per file.** Never bundle.
11. **Local deps: `httpx`, `loguru`, `matplotlib`.** Don't install numpy/pandas — server has them.
