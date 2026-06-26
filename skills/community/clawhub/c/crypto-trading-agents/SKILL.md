---
name: crypto-trading-agents
description: >
  多Agent加密货币量化交易系统 — 基于 TradingAgents 多Agent框架 + Binance 执行层。
  支持：技术分析、消息分析、多Agent辩论、自动化交易信号生成、Binance 现货下单。
  适用场景：研究量化策略、自动交易Bot开发、加密货币组合分析。
---

# Crypto Trading Agents

> 多Agent加密货币量化交易系统 | TradingAgents + Binance

## 系统架构

```
TradingAgents 多Agent框架
    ├── Technical Analyst (技术分析：RSI/MACD/Bollinger/ATR)
    ├── News Analyst (消息分析：市场新闻/宏观经济)
    ├── Sentiment Analyst (情绪分析：社交媒体情绪)
    ├── Fundamentals Analyst (基本面分析)
    ├── Bull/Bear Researcher (多空辩论)
    └── Portfolio Manager (组合管理，生成交易信号)
              ↓
        Binance Trader
    ├── 市价/限价下单
    ├── 止损/止盈
    └── 仓位/挂单查询
              ↓
       Binance 现货市场
```

## 环境要求

- Python 3.10+
- uv (推荐) 或 pip
- Binance API Key（现货权限即可，不需要合约）
- 网络连接（Binance API 访问）

## 快速安装

```bash
# 克隆项目
git clone https://github.com/TauricResearch/TradingAgents.git
cd TradingAgents

# 创建虚拟环境
uv venv .venv --python 3.12
source .venv/bin/activate

# 安装核心依赖
pip install .

# 安装 CCXT（用于 Binance 对接）
uv pip install ccxt

# 可选：安装加密货币技术指标增强
uv pip install pandas numpy
```

## 环境变量配置

在项目根目录创建 `.env` 文件：

```bash
cp .env.example .env
```

编辑 `.env`，填入：

```bash
# ─── LLM API（TradingAgents 多Agent分析用）───
OPENAI_API_KEY=sk-...           # OpenAI GPT
# 或
GOOGLE_API_KEY=...              # Google Gemini
# 或
ANTHROPIC_API_KEY=...           # Anthropic Claude

# ─── Binance API（交易执行用）───
BINANCE_API_KEY=your_api_key
BINANCE_API_SECRET=your_api_secret

# ─── 可选 ───
BINANCE_TESTNET=true            # true = 使用测试网（不花真钱）
```

## 使用方法

### 方法一：Python API（推荐，开发用）

```python
import tradingagents as ta

# ─── 1. 多Agent分析 ───────────────────────────
analyst = ta.CryptoAnalyst()
result = analyst.analyze("BTC/USDT", date="2026-03-24")
analyst.print_report(result)

# ─── 2. Binance 交易执行 ─────────────────────
trader = ta.BinanceTrader()

# 查询账户
print(trader.status("BTC/USDT"))

# 市价买入
print(trader.buy_market("BTC/USDT", amount=0.01))

# 限价买入
print(trader.buy_limit("BTC/USDT", amount=0.01, price=60000.0))

# 设置止损
print(trader.set_stop_loss("BTC/USDT", amount=0.01, stop_price=55000.0))

# ─── 3. 直接调用数据接口 ──────────────────────
from tradingagents.dataflows.binance_data import get_binance_ticker
from tradingagents.dataflows.crypto_indicators import get_crypto_indicators

# 实时行情（无需 API Key）
print(get_binance_ticker("BTC/USDT"))

# 技术指标（无需 API Key）
print(get_crypto_indicators("BTC/USDT", period="1d", lookback=60))
```

### 方法二：命令行（快速操作）

```bash
source .venv/bin/activate

# 分析（不需要 API Key）
python -m tradingagents.crypto_trading --symbol BTC/USDT --action analyze
python -m tradingagents.crypto_trading --symbol ETH/USDT --action analyze

# 账户状态
python -m tradingagents.crypto_trading --symbol BTC/USDT --action status

# 市价交易（需要 API Key）
python -m tradingagents.crypto_trading --symbol BTC/USDT --action trade --side buy --amount 0.01

# 限价交易
python -m tradingagents.crypto_trading --symbol BTC/USDT --action trade --side buy --amount 0.01 --price 60000

# 测试网交易
python -m tradingagents.crypto_trading --symbol BTC/USDT --action trade --side buy --amount 0.01 --testnet
```

### 方法三：直接使用 Binance Executor

```python
from tradingagents.execution.binance_executor import (
    execute_market_order,
    execute_limit_order,
    execute_stop_loss,
    get_open_orders,
    get_position,
)

# 查持仓
print(get_position("BTC/USDT"))

# 市价单
print(execute_market_order("BTC/USDT", "buy", 0.01))

# 限价单
print(execute_limit_order("BTC/USDT", "buy", 0.01, 60000.0))

# 止损单
print(execute_stop_loss("BTC/USDT", "sell", 0.01, 55000.0))
```

## 主要模块

| 模块 | 说明 |
|------|------|
| `tradingagents.crypto_trading` | 主入口，CryptoAnalyst + BinanceTrader |
| `tradingagents.dataflows.binance_data` | Binance 数据源（K线/行情/订单簿） |
| `tradingagents.dataflows.crypto_indicators` | 技术指标（RSI/MACD/Bollinger/ATR） |
| `tradingagents.agents.utils.binance_tools` | LangChain Tools，注入多Agent |
| `tradingagents.execution.binance_executor` | 交易执行（市价/限价/止损） |

## 微信通知集成

系统内置 `WeChatNotifier`，当配置了企业微信 Webhook 后，所有交易活动自动推送：

```bash
export WECHAT_WEBHOOK_URL='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=XXX'
```

发送内容：
- 📡 **交易信号**：方向、价格、置信度、原因
- 📗 **订单执行**：买入/卖出、价格、数量、订单ID
- ❌ **错误报警**：操作失败时即时通知
- 📊 **账户状态**：持仓、盈亏、挂单数

## 自动交易工作流

```
定时任务（Cron）
    │
    ▼
AutoTradingSession.run("BTC/USDT")
    │
    ├── CryptoAnalyst.analyze()         ← 多Agent分析 + 微信推送信号
    │
    ├── signal = 解析 agent_decision      ← 信号解析（买入/卖出/观望）
    │
    ├── trader.buy_market()             ← 自动执行（可选）
    │
    ├── trader.set_stop_loss()          ← 自动设止损
    │
    └── WeChatNotifier 推送结果          ← 微信通知
```

### 命令行一键自动交易 + 微信通知

```bash
source .venv/bin/activate

# 自动分析 + 推送信号到微信（不交易）
python -m tradingagents.crypto_trading --symbol BTC/USDT --action analyze --notify

# 自动交易 + 微信通知
python -m tradingagents.crypto_trading --symbol BTC/USDT --action auto \
  --auto-trade --amount 0.01 --stop-loss 0.05 --notify --testnet

# 手动交易 + 微信通知
python -m tradingagents.crypto_trading --symbol BTC/USDT --action trade \
  --side buy --amount 0.01 --notify
```

### Python API（带微信通知）

```python
import tradingagents as ta

# 初始化（会自动读取 WECHAT_WEBHOOK_URL 环境变量）
notifier = ta.WeChatNotifier()
session = ta.AutoTradingSession(
    auto_trade=False,    # True = 自动执行交易
    notify=True,
    testnet=True,
)

# 运行：分析 → 信号 → 微信推送 →（可选）自动交易
result = session.run("BTC/USDT", buy_amount=0.01, stop_loss_pct=0.05)

# 单独使用通知器
notifier.notify_signal("BTC/USDT", "买入", 65000.0, "高", "RSI超卖 + MACD金叉")
notifier.notify_trade("BTC/USDT", "buy", 0.01, 65000.0, "123456", "已执行")
```

## 附：完整交易策略 Pine Script

`scripts/hourly_contrarian_strategy.pine` — 完整版策略（291行），包含：

- MA60 多周期方向评分系统（4H + 日线）
- 顺势信号（回踩MA60 / 回踩前低 / 回抽前高）
- K线形态过滤（锤子线 / 吞没形态 / 流星）
- 逆反思维信号（极端情绪 + 量能突增）
- 盈亏比 2:1 止损止盈
- TP1 保本移动止损
- 仪表盘（方向 / 评分 / MA60斜率 / 杠杆）
- Webhook 告警（支持 Binance 自动下单）

```bash
# 获取策略文件
cat scripts/hourly_contrarian_strategy.pine
```

复制内容到 TradingView Pine Editor 即可使用。

## 策略建议

1. **先用测试网**：`BINANCE_TESTNET=true`，不花真钱
2. **先回测**：用历史数据分析策略效果
3. **小资金实盘**：先用最小单位（0.001 BTC）验证
4. **必设止损**：每次开仓都要设止损，不要裸奔

## 安全提示

- **不要**把 API Secret 提交到 Git
- 建议使用只读 + 现货交易权限的 API Key，不要用全权限
- 生产环境建议用 VPS + Docker 部署，不要在本地电脑跑
- 这是一个**研究框架**，实盘风险自负

## 故障排除

| 问题 | 解决方法 |
|------|----------|
| `No module named 'ccxt'` | `uv pip install ccxt` |
| `BINANCE_API_KEY not set` | 检查 `.env` 文件是否配置 |
| `Insufficient data` | 减少 `lookback` 参数 |
| API Rate Limit | CCXT 已内置限流，等待即可 |
| Network Error | 检查网络连接，确认 Binance 区域可用 |
