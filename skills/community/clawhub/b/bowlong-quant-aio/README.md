# 🐉 波龙股神量化交易系统 V2.0

> A股 · 期货 一站式量化工作台 — 选股 · 回测 · 实盘 · 风控

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![Author: SimonsTang](https://img.shields.io/badge/Author-SimonsTang-orange.svg)](https://github.com/simonstang)

---

## 📜 版权声明

**波龙股神量化交易系统 V2.0**

- © 2026 **SimonsTang / 上海巧未来人工智能科技有限公司** 版权所有
- 开源协议：**MIT License**
- 源码开放，欢迎完善，共同进步
- 🌐 GitHub：https://github.com/simonstang/bolong-quant
- 📧 联系：learn2study@163.com
- 🌐 网站：https://learn2study.cn

---

## ✨ 功能概览

```
┌──────────────────────────────────────────────────────────────┐
│                  🐉 波龙股神量化交易系统 V2.0                  │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   📊 选股引擎        多因子筛选 · 行业轮动 · 自选股池管理       │
│                                                              │
│   🔁 回测系统        策略编写 · 历史回测 · 绩效报告            │
│                      A股T+1规则 · 涨跌停限制 · 印花税           │
│                                                              │
│   ⚡ 实盘执行        华鑫QMT · 文华财经WH8 · TBQuant3         │
│                      A股实盘 · 商品期货 · 股指期货              │
│                                                              │
│   🔔 风险监控        仓位监控 · 回撤预警 · 异动推送             │
│                      实时告警 · Telegram通知                   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# Python 3.8+
pip install pandas numpy tushare akshare scipy matplotlib pywin32 requests
```

### 2. 配置

```bash
# 复制配置文件
cp config/config.yaml.example config/config.yaml

# 编辑配置，填入你的信息
# - TUSHARE_TOKEN（必需）
# - 华鑫QMT账号密码（可选）
# - Telegram推送（可选）
```

### 3. 设置环境变量

```bash
# tushare pro token（必须，申请地址：https://tushare.pro/register）
export TUSHARE_TOKEN="your_token_here"

# 华鑫QMT（可选，无则使用模拟盘）
export QMT_ACCOUNT="your_account"
export QMT_PASSWORD="your_password"

# Telegram推送（可选）
export PUSH_TOKEN="your_bot_token"
export PUSH_CHAT_ID="your_chat_id"
```

### 4. 运行

```bash
# ── 选股 ──
python scripts/stock_picker.py --strategy momentum --top 20

# ── 回测 ──
python scripts/backtest.py --strategy momentum --start 2020-01-01 --end 2026-03-27

# ── 实盘（模拟盘）──
python scripts/executor_huaxin.py --mode paper --action status
python scripts/executor_wenhua.py --mode paper --action status

# ── 风控监控 ──
python scripts/risk_monitor.py --once              # 单次检查
python scripts/risk_monitor.py                      # 实时监控
```

---

## 📂 目录结构

```
bolong-quant/
├── SKILL.md                      # 技能说明文档（OpenClaw格式）
├── README.md                     # 本文件
├── scripts/
│   ├── stock_picker.py          # 选股引擎
│   ├── backtest.py              # 回测系统
│   ├── executor_huaxin.py       # 华鑫QMT执行器
│   ├── executor_wenhua.py       # 文华财经执行器
│   ├── executor_tbquant.py      # TBQuant3执行器（待开发）
│   ├── risk_monitor.py          # 风险监控
│   └── report_generator.py       # 报告生成器
├── config/
│   ├── config.yaml              # 主配置文件
│   ├── config.yaml.example      # 配置示例
│   ├── factors.yaml            # 选股因子配置
│   └── risk_rules.yaml          # 风控规则配置
├── references/
│   ├── qmt_api.md              # 华鑫QMT API文档
│   ├── wenhua_api.md           # 文华财经API文档
│   └── data_sources.md         # 数据源说明
└── output/
    ├── stock_picks/            # 选股结果
    ├── backtest_reports/        # 回测报告
    └── charts/                 # 图表输出
```

---

## 📖 详细功能

### 📊 选股引擎

支持四种选股策略：

```bash
python scripts/stock_picker.py --strategy momentum    # 动量策略
python scripts/stock_picker.py --strategy value        # 价值策略
python scripts/stock_picker.py --strategy growth        # 成长策略
python scripts/stock_picker.py --strategy break_through  # 突破策略
```

**多因子评分体系：**
- 基本面因子（50%）：PE、ROE、营收增速、净利润增速
- 技术面因子（35%）：均线多头、RSI、量比、MACD金叉
- 资金面因子（15%）：北向资金、融资余额、机构动向

**输出示例：**
```
股票代码 | 股票名称 | 综合得分 | PE | ROE | 北向资金 | 入选理由
---------|---------|---------|-----|-----|---------|----------
600519   | 贵州茅台 | 92      | 28  | 32  | +3285万 | 低估值+北向净流入
000858   | 五粮液   | 87      | 22  | 28  | +2156万 | 突破20日均线
...
```

---

### 🔁 回测系统

**三大内置策略：**

| 策略 | 说明 | 适合行情 |
|------|------|---------|
| `momentum` | 均线金叉/死叉 | 趋势行情 |
| `rsi` | RSI超买超卖 | 震荡行情 |
| `macd` | MACD金叉/死叉 | 趋势行情 |

**A股专属规则：**
- ✅ T+1制度（当日买入不能当日卖出）
- ✅ 涨跌停限制（涨停不买入，跌停不卖出）
- ✅ 印花税（仅卖出收取千1）
- ✅ 佣金（万3，最低5元）
- ✅ 滑点控制

**回测报告示例：**
```markdown
# 📊 回测报告 · 动量策略
- 时间: 2020-01-01 ~ 2026-03-27
- 初始资金: 1,000,000 元
- 最终净值: 2,856,000 元
- 总收益率: +185.6%
- 年化收益: 18.3%
- 夏普比率: 1.85
- 最大回撤: -22.4%
- 胜率: 58.3%
- 盈亏比: 1.72
```

---

### ⚡ 实盘执行

#### 华鑫证券QMT

```python
from scripts.executor_huaxin import QMTClient

client = QMTClient(config)
client.login()

# 查询
account = client.get_account()
positions = client.get_positions()

# 交易
client.buy("600519", price=1850, volume=100)   # 买入
client.sell("600519", price=1900, volume=100) # 卖出
```

**支持功能：**
- 账户登录/登出
- 持仓查询
- 买入/卖出下单
- 订单查询/撤销
- 模拟盘/实盘切换

#### 文华财经WH8

```python
from scripts.executor_wenhua import WenhuaClient

client = WenhuaClient(config)
client.login()

# 期货交易
client.buy_open("IF2504", price=3800, volume=1)    # 买入开仓
client.sell_open("IC2504", price=5800, volume=1)  # 卖出开仓
client.sell_close("IF2504", price=3820, volume=1)  # 卖出平仓
```

**支持品种：**
- 股指期货：IF、IH、IC、IM
- 商品期货：黄金(AU)、白银(AG)、铜(CU)、螺纹钢(RB)等

---

### 🔔 风险监控

**风控规则：**

```yaml
# 仓位限制
max_position_per_stock: 20%     # 单股最大仓位
max_total_position: 80%           # 总仓位上限
min_cash_reserve: 10%           # 最低现金储备

# 亏损限制
max_daily_loss: 2%             # 单日最大亏损
max_total_drawdown: 15%         # 总回撤上限
stop_loss_per_trade: 5%         # 单笔止损

# 交易限制
max_trades_per_day: 20          # 每日最大交易次数
avoid_limit_up: true           # 避免涨停板买入
avoid_limit_down: true           # 避免跌停板卖出
```

**告警类型：**
- 🚨 单日亏损超限
- 🚨 总回撤超限
- ⚠️ 仓位超限
- ⚠️ 交易次数超限
- ⚠️ 持仓异动

**Telegram推送：**
```
📊 波龙股神风控日报 · 2026-03-27 15:30

💰 账户概览
总资产: 1,052,380 元
仓位: 45.2% ✅
今日亏损: -0.8% ✅
回撤: -3.2% ✅

⚠️ 告警：IF2504 成交量放大 300%
```

---

## 🛠️ 配置文件说明

### config/config.yaml

```yaml
data:
  primary: tushare          # 主数据源
  tushare:
    token: "${TUSHARE_TOKEN}"

stock_picker:
  run_time: "09:35"         # 每日运行时间
  top_n: 20                  # 输出TOP N只
  universe: [沪深300, 中证500, 创业板指]

backtest:
  initial_cash: 1000000     # 初始资金
  commission: 0.0003         # 佣金率
  stamp_duty: 0.001         # 印花税

executor:
  mode: paper               # paper=模拟盘, live=实盘
  huaxin:
    account: "${QMT_ACCOUNT}"
    password: "${QMT_PASSWORD}"

risk:
  position:
    max_total: 0.80         # 仓位上限80%
  loss_limit:
    daily: 0.02            # 单日亏损2%
    total_drawdown: 0.15   # 回撤15%
```

### config/factors.yaml

```yaml
weights:
  fundamentals: 0.50    # 基本面权重
  technical: 0.35         # 技术面权重
  sentiment: 0.15        # 资金面权重

fundamentals:
  valuation:
    pe: [0, 60]         # PE范围
    roe: [8, 50]         # ROE范围
  growth:
    revenue_growth_yoy: 5  # 营收增速下限%

technical:
  trend:
    ma20_above: true     # 股价在20日均线上方
  momentum:
    rsi: [40, 70]       # RSI范围

sentiment:
  north_money_3d: 0      # 北向资金净流入下限
```

---

## ⚠️ 风险提示

1. **模拟盘测试**：实盘前务必在模拟盘充分测试
2. **风险控制**：建议严格设置止损规则，避免单日大幅亏损
3. **资金管理**：不要使用超过承受能力的资金进行交易
4. **数据质量**：回测结果仅供参考，不代表实盘表现
5. **市场风险**：股市有风险，投资需谨慎

**免责声明：**
本软件仅供学习和研究使用，因使用本软件造成的任何投资损失，作者和开发团队不承担任何责任。

---

## 🤝 贡献与反馈

欢迎提交 Issue 和 Pull Request！

- 🐛 Bug反馈：https://github.com/simonstang/bolong-quant/issues
- 💡 功能建议：https://github.com/simonstang/bolong-quant/discussions
- 📧 联系作者：learn2study@163.com

---

## 📜 开源协议

MIT License

Copyright (c) 2026 SimonsTang / 上海巧未来人工智能科技有限公司

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 🐉 关于波龙股神

**学来学去学习社** 出品的量化交易系统。

学来学去学习社 — 让学习更有趣更高效
- 🌐 网站：https://learn2study.cn
- 📧 联系：learn2study@163.com

---

*© 2026 SimonsTang / 上海巧未来人工智能科技有限公司 版权所有*
