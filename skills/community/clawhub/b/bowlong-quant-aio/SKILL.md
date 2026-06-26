---
name: bowlong-quant-aio
version: 2.1.3
description: 🐉 波龙股神量化交易系统 V2.1.1 — 价值投资导向的A股期货量化工作台。**V2.1优化版：解决追涨杀跌问题**，专注低估值优质股。多因子选股 · A股回测 · 华鑫QMT实盘 · 文华财经期货 · 实时风控。核心优化：涨幅过滤(3月≤50%/1月≤25%)、RPS区间优化(70-85)、PE/PB估值筛选(5-30/<5)、排除高位震荡股、排除涨停股。搜索关键词：波龙股神、量化交易、价值投资、选股、A股、期货、QMT、回测、策略、投资、股票、炒股、量化选股、自动交易、巧未来、西蒙斯。Keywords: Bowlong, Quant Trading, Value Investing, Stock Picker, A-Share, Futures, QMT, Wenhua, Backtest, Strategy, Investment, Stock Trading, Quantitative, Auto Trading, Stock Screening, Simons, Jarvis, AI Trading
author: SimonsTang
license: MIT
homepage: https://learn2study.cn
repository: https://github.com/simonstang/bolong-quant
metadata:
  openclaw:
    emoji: "📈"
    category: "finance"
    tags: ["A股", "期货", "量化", "QMT", "文华财经", "选股", "回测", "实盘", "风控", "波龙股神", "Bowlong", "tushare", "akshare", "量化交易", "股票", "炒股", "投资策略", "自动交易", "股票筛选", "技术分析", "巧未来", "西蒙斯", "贾维斯", "Quant Trading", "Stock Picker", "Futures", "Backtest", "AI Trading", "Investment"]
    requires:
      bins: ["python3"]
      env: ["TUSHARE_TOKEN"]
---

# quant-aio · A股期货一站式量化工作台

> 选股 → 回测 → 实盘 → 风控，一个技能全搞定。

## 功能概览

```
┌─────────────────────────────────────────────────────────┐
│                  📈 quant-aio v1.0                      │
├─────────────────────────────────────────────────────────┤
│  📊 选股引擎   多因子筛选 · 行业轮动 · 自选股池管理        │
│  🔁 回测系统   策略编写 · 历史回测 · 绩效报告              │
│  ⚡ 实盘执行   华鑫QMT · 文华财经 · TBQuant3            │
│  🔔 风险监控   仓位监控 · 回撤预警 · 异动推送             │
└─────────────────────────────────────────────────────────┘
```

## 环境要求

```bash
# Python 3.8+
pip install pandas numpy tushare akshare scipy matplotlib

# tushare pro（推荐，可申请免费token）
pip install tushare

# 华鑫证券QMT Python API
# 安装路径默认: C:\Huaxin\QMT\bin\Lib\site-packages\

# 文华财经WH8 Python API
# 安装路径: 文华财经安装目录下 wh8\python\

# TBQuant3 Python API
# 安装路径: 通联数据官网下载
```

## 环境变量

```bash
# tushare pro token（必须，申请: https://tushare.pro/register）
export TUSHARE_TOKEN="your_token_here"

# 华鑫QMT（可选，无则跳过实盘模块）
export QMT_ACCOUNT="your_account"
export QMT_PASSWORD="your_password"

# 告警推送（可选）
export PUSH_TOKEN="telegram_bot_token"
export PUSH_CHAT_ID="telegram_chat_id"
```

## 模块一：选股引擎

### 选股策略

```bash
# 运行选股（默认：多因子策略）
python scripts/stock_picker.py

# 指定策略
python scripts/stock_picker.py --strategy momentum          # 动量策略
python scripts/stock_picker.py --strategy value             # 价值策略
python scripts/stock_picker.py --strategy growth            # 成长策略
python scripts/stock_picker.py --strategy break_through     # 突破策略

# 自定义参数
python scripts/stock_picker.py --strategy momentum --top 20 --date 2026-03-27
```

### 因子配置

编辑 `config/factors.yaml` 调整因子权重：

```yaml
factors:
  fundamentals:
    weight: 0.50          # 基本面权重
    pe: [-30, 50]         # PE范围
    roe: [5, 50]          # ROE范围
    revenue_growth: 5      # 营收增速下限%
    profit_growth: 5       # 净利润增速下限%

  technical:
    weight: 0.35          # 技术面权重
    rsi: [30, 70]         # RSI范围
    volume_ratio: 1.5      # 量比下限
    break_20d: true        # 20日均线突破

  sentiment:
    weight: 0.15          # 资金流权重
    north_money: 100      # 北向资金净流入下限（万）
    margin_balance: 100    # 融资余额增速下限%
```

### 选股输出

```
# 输出路径: output/stock_picks_YYYYMMDD.csv

股票代码 | 股票名称 | 综合得分 | PE | ROE | 北向资金 | 入选理由
---------|---------|---------|-----|-----|---------|----------
600519   | 贵州茅台 | 92      | 28  | 32  | +3285万 | 低估值+北向净流入
000858   | 五粮液   | 87      | 22  | 28  | +2156万 | 突破20日均线
...
```

## 模块二：回测系统

### 运行回测

```bash
# 完整回测（2015-2026）
python scripts/backtest.py --strategy momentum

# 近期回测（近一年）
python scripts/backtest.py --strategy momentum --period 1y

# 指定股票池
python scripts/backtest.py --strategy momentum --pool 沪深300

# 自定义参数
python scripts/backtest.py --strategy momentum \
  --start 2020-01-01 \
  --end 2026-03-27 \
  --initial_cash 100000 \
  --commission 0.0003 \
  --slippage 0.0001
```

### 回测报告

运行后在 `output/backtest_report_YYYYMMDD.md` 生成报告：

```markdown
# 📊 回测报告 · 动量策略
- 时间: 2020-01-01 ~ 2026-03-27
- 初始资金: 100,000 元
- 最终净值: 285,600 元
- 总收益率: +185.6%
- 年化收益: 18.3%
- 夏普比率: 1.85
- 最大回撤: -22.4%
- 胜率: 58.3%
- 盈亏比: 1.72
- 总交易次数: 347

# 📈 收益曲线
[图表路径: output/charts/equity_curve.png]
```

### 支持指标

| 类型 | 指标 |
|------|------|
| 趋势 | MA/EMA/SMA、MACD、布林带、ADX |
| 动量 | RSI、KDJ、CCI、WR |
| 量价 | 成交量、量比、换手率、OBV |
| 风险 | ATR、VaR、Beta |

### A股特有规则

```python
# 自动处理A股T+1制度
# 自动处理涨跌停（涨停不买入，跌停不卖出）
# 自动处理ST股（可选排除）
# 自动处理停牌（跳过不交易）
# 手续费默认：万3佣金 + 万0.5印花税
```

## 模块三：实盘执行

### 华鑫证券QMT

华鑫证券QMT使用 `Python API` 直连接口。

```python
from scripts.executor_huaxin import HuaxinExecutor

executor = HuaxinExecutor(
    account="你的账号",
    password="你的密码",
    mode="paper"  # paper=模拟, live=实盘
)

# 下单
executor.buy("600519", price=1850, volume=100)  # 买入贵州茅台
executor.sell("600519", price=1900, volume=100) # 卖出

# 查询
executor.positions()   # 当前持仓
executor.orders()      # 订单状态
executor.balance()     # 账户余额
```

### 文华财经WH8

文华财经使用 `Python SDK` 接口。

```python
from scripts.executor_wenhua import WenhuaExecutor

executor = WenhuaExecutor(
    mode="paper"  # paper=模拟, live=实盘
)

# 期货下单
executor.buy("IF2504", price=3800, lots=1)    # 买入IF股指期货
executor.sell("IC2504", price=5800, lots=1)  # 卖出IC

# 策略执行
executor.run_strategy("momentum_20min")
```

### TBQuant3

TBQuant3通过 `Python API` 接入。

```python
from scripts.executor_tbquant import TBQuantExecutor

executor = TBQuantExecutor(mode="paper")

# 商品期货
executor.buy("CU2504", price=72000, lots=1)  # 沪铜
executor.sell("RB2504", price=3500, lots=1)  # 螺纹钢
```

### 实盘日志

```
[2026-03-27 09:35:01] 信号: 买入 600519 @ 1850
[2026-03-27 09:35:02] 订单发送成功, OrderID: 12345678
[2026-03-27 09:35:05] 订单成交, 成交价: 1850.2
[2026-03-27 09:35:05] 持仓更新: 600519 x 100股, 成本: 1850.2
```

## 模块四：风险监控

### 监控面板

```bash
# 启动实时监控
python scripts/risk_monitor.py

# 启动并推送到Telegram
python scripts/risk_monitor.py --push telegram
```

### 风控规则

编辑 `config/risk_rules.yaml`：

```yaml
risk_rules:
  # 仓位限制
  max_position_per_stock: 0.20       # 单股最大仓位20%
  max_total_position: 0.80           # 总仓位上限80%
  min_cash_reserve: 0.10             # 最低现金储备10%

  # 回撤限制
  max_daily_loss: 0.02               # 单日最大亏损2%
  max_total_drawdown: 0.15           # 总回撤上限15%
  stop_loss_per_trade: 0.05          # 单笔止损5%

  # 预警规则
  alert_on_position_change: true     # 仓位变化告警
  alert_on_drawdown_threshold: 0.10 # 回撤10%告警
  alert_on_unusual_volume: true       # 异动告警

  # 交易限制
  max_trades_per_day: 10            # 每日最大交易次数
  avoid_limit_up: true              # 避免涨停板买入
  avoid_limit_down: true             # 避免跌停板卖出
  avoid_st_stocks: false            # 排除ST股
```

### 风控报告

```markdown
# 🔔 风控日报 · 2026-03-27

## 持仓状况
| 股票 | 持仓 | 成本 | 现价 | 盈亏 | 仓位 |
|------|------|------|------|------|------|
| 600519 | 500 | 1800 | 1850 | +2.78% | 18.5% |

## 风控指标
- 总仓位: 45.2% ✅ (上限80%)
- 现金储备: 54.8% ✅ (下限10%)
- 今日亏损: -0.8% ✅ (上限2%)
- 总回撤: -3.2% ✅ (上限15%)

## 告警记录
[无]

## 建议
✅ 所有指标正常，继续执行策略
```

## 数据源配置

### tushare pro（推荐）

```bash
# 安装
pip install tushare

# 配置token（在 tushare.pro 注册获取免费token）
# 编辑 config/data_source.yaml
```

```yaml
data_source:
  primary: tushare_pro
  tushare:
    token: "${TUSHARE_TOKEN}"  # 设置环境变量
    high_priority: true         # 优先使用日线以上数据

  fallback: akshare
  akshare:
    free: true
    delay: 15                  # 数据延迟15分钟
```

### 数据更新

```bash
# 更新日线数据
python scripts/update_data.py --freq daily

# 更新分钟线数据
python scripts/update_data.py --freq 5min --days 30

# 全量更新（首次运行）
python scripts/update_data.py --full
```

## 目录结构

```
quant-aio/
├── SKILL.md                      # 本文件
├── README.md                     # 详细使用说明
├── scripts/
│   ├── stock_picker.py          # 选股引擎
│   ├── backtest.py              # 回测系统
│   ├── executor_huaxin.py       # 华鑫QMT执行器
│   ├── executor_wenhua.py       # 文华财经执行器
│   ├── executor_tbquant.py      # TBQuant3执行器
│   ├── risk_monitor.py          # 风险监控
│   ├── update_data.py           # 数据更新
│   └── report_generator.py      # 报告生成
├── config/
│   ├── config.yaml              # 主配置
│   ├── factors.yaml             # 选股因子配置
│   ├── risk_rules.yaml          # 风控规则
│   └── strategies.yaml          # 策略模板
├── references/
│   ├── qmt_api.md              # 华鑫QMT API文档
│   ├── wenhua_api.md           # 文华财经API文档
│   ├── tbquant_api.md          # TBQuant3 API文档
│   ├── tushare_guide.md        # tushare使用指南
│   └── data_sources.md         # 数据源说明
└── output/
    ├── stock_picks/            # 选股结果
    ├── backtest_reports/       # 回测报告
    └── charts/                 # 图表输出
```

## 快速开始

```bash
# 1. 安装依赖
pip install pandas numpy tushare akshare scipy matplotlib

# 2. 配置（复制并编辑）
cp config/config.yaml.example config/config.yaml

# 3. 设置环境变量
export TUSHARE_TOKEN="你的token"

# 4. 运行选股
python scripts/stock_picker.py --top 20

# 5. 运行回测
python scripts/backtest.py --strategy momentum

# 6. 启动风控监控
python scripts/risk_monitor.py --push telegram
```

## 注意事项

⚠️ **实盘交易有风险，请务必先在模拟盘测试稳定后再使用实盘。**
⚠️ **本工具仅供学习和研究使用，盈亏自负。**
⚠️ **请遵守相关法律法规和券商规定。**

## 更新日志

### v2.1.1 (2026-04-12)
- **价值投资导向优化**：解决追涨杀跌问题
- 增加涨幅过滤：近3月涨幅≤50%，近1月涨幅≤25%
- RPS优化：70-85为最佳区间，排除>90的高位股
- 估值筛选：PE 5-30，PB<5
- 排除高位震荡股和涨停股
- 投资理念：从追涨杀跌转变为价值投资
- 避免选到招商轮船、中远海能等已涨2-3倍的高位股

### v2.1.0 (2026-04-11)
- V2.1版本发布

### v2.0.0 (2026-03-27)
- 正式命名为"波龙股神量化交易系统"
- 开发者：SimonsTang
- 公司：上海巧未来人工智能科技有限公司
- 开源代码，MIT协议

### v1.0.0 (2026-03-27)
- 初始版本
- 支持选股、回测、风控
- 支持华鑫QMT、文华财经WH8、TBQuant3实盘接口
- 支持tushare pro、akshare数据源

---

## 📜 版权声明

**波龙股神量化交易系统 V2.0**

- © 2026 **SimonsTang / 上海巧未来人工智能科技有限公司** 版权所有
- 开源协议：MIT License
- 源码开放，欢迎完善，共同进步
- GitHub：https://github.com/simonstang/bolong-quant
- 联系：learn2study@163.com
- 网站：https://learn2study.cn

_学来学去学习社 · 让学习更有趣更高效_
