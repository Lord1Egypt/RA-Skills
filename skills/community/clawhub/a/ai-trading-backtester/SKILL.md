---
name: "AI Trading Strategy Backtester"
description: "AI-powered quantitative trading strategy backtesting assistant. Designs, codes, and evaluates trading strategies across historical market data. Supports A-share (China), Hong Kong, US equity markets. Covers mean reversion, momentum, breakout, pairs trading, and machine learning-based strategies. Built for quantitative analysts and retail traders. Keywords: trading backtest, quantitative strategy, algorithmic trading, Python backtesting, backtrader, vectorbt, trading strategy, momentum, mean reversion, pairs trading, A-share strategy, financial data, technical indicators."
version: "5.0.6"
---

# AI Trading Strategy Backtester

## Overview

An AI-powered quantitative trading strategy design and backtesting assistant that helps you transform trading ideas into fully-coded, backtested strategies. It guides you through strategy design (mean reversion, momentum, breakout, pairs trading, ML-based), implements them in Python (backtrader, vectorbt, pandas), evaluates performance across historical data for A-share, HK, and US markets, and produces risk-adjusted performance reports.

## Market & Regulatory Context (as of 2026-11-19)

| 事项 | 对回测的直接影响 |
|------|----------------|
| **程序化交易管理要求** | 高频类策略需自行计入报备、流速与异常交易约束，回测中不能假设"无限报单" |
| **A股 T+1 与涨跌幅限制** | 当日买入不可卖出、涨跌停无法成交，回测必须对不可成交信号做剔除或顺延处理 |
| **停牌与流动性** | 停牌期间的"信号"不可成交；小市值标的需按实际成交量限制下单规模 |
| **交易成本口径** | 佣金、印花税、滑点合计常被低估，年换手率高时成本可吞掉全部超额收益 |
| **数据复权与幸存者偏差** | 使用不复权价格或仅含现存标的历史，会系统性高估策略表现 |

**新动态（截至 2026-11-19）：**
- **程序化交易监管常态化**：境内市场对程序化交易的报备、交易行为监测与异常交易认定持续细化，高频与日内回转类策略的合规成本上升。回测时应把"报单频率上限""撤单率约束"纳入假设，而非只追求收益最大化。
- **AI 选股与因子挖掘的合规关注上升**：以大模型或机器学习生成交易信号时，监管与机构风控普遍要求可解释、可复现、留痕，纯黑箱信号在实盘落地时面临额外审核成本。
- **数据要素与另类数据应用扩展**：产业、舆情、供应链等另类数据被更广泛用于因子构建，但数据可得性的时点（point-in-time）问题更突出，回测中须严格避免引入未来信息。
- 以上为公开信息综述，**具体规则、费率与执行口径以交易所、中国证监会及券商官方最新发布为准**。
- **回测口径本身成为关注点**：机构内部评审 increasingly 要求回测报告披露「数据复权方式、样本区间、成本口径、可成交性过滤、样本外划分方式」五项，缺项即视为不可采信。建议把五项写进回测报告模板的固定开头。
- **另类数据的 point-in-time 问题被单独提示**：产业、舆情、供应链类数据常见「事后回填」，直接用于回测会引入未来信息。可行做法是为每类数据记录「可获得时点」，并在回测中只允许使用该时点之前已经存在的数据版本。
- 以上新增条目为公开信息综述，**具体规则、费率与执行口径以官方最新发布为准**。

---

## 语言与适用市场声明（Language & Markets）

- **语言**：英文术语（Metrics、Sharpe、Drawdown、Walk-forward 等）保留原文，中文用于解释与结论——这是量化领域通用做法，便于与代码、公式和第三方工具对齐，属显式设计。
- **支持市场**：A 股（沪深）、中国香港市场、美股。三个市场的**交易规则差异是回测结论的前提**，不可混用：
  - A 股：T+1、涨跌停限制、停牌、卖出印花税、做空渠道有限；
  - 中国香港市场：T+0、无涨跌停、交易成本与结算周期不同；
  - 美股：T+0、可做空、税费与结算规则另行适用。
- **口径优先**：任何回测示例都必须明确标注市场；**同一段代码在不同市场下的结论不可直接套用**。
- 涉及中国香港、中国澳门、中国台湾及境外市场的具体监管要求，本技能仅提供通用回测方法，规则细节以当地监管与交易所口径为准。

---

## 数据最小化与执行边界（Data Minimization & Execution Boundary）

**数据最小化前置声明（使用本技能前请先执行）**

1. 不要粘贴实盘账户信息、持仓明细、真实成交记录；讨论时用脱敏后的结构或虚构标的。
2. 数据文件路径、数据库地址、行情接口密钥一律用占位符，不写入提示词。
3. 涉及的策略参数、因子逻辑如属机构未公开成果，只描述结构不给具体数值。
4. 本技能不运行回测、不安装依赖、不读取本地行情文件、不发起任何网络请求；所有代码需你在自己的环境中执行。
5. 生成的代码与报告如需落盘，须先预览确认无凭据与内部路径残留，再自行保存。

**代码块性质与执行边界**

| 内容 | 性质 | 谁来执行 |
|------|------|---------|
| backtrader / statsmodels 等示例 | 可运行脚手架，需本地安装依赖 | 使用者在自己的环境中运行，本技能不执行 |
| 绩效指标表中的目标值与示例数字 | 参考区间与示意值，非承诺 | 使用者用自身回测结果替换 |
| 成本、税率、费率数字 | 公开口径示例，随时变化 | 使用者以交易所与券商最新口径为准 |
| 压力测试情景与参数 | 方法论示例 | 使用者按自身标的与时间调整 |

**硬边界**：不执行回测、不安装依赖、不读写本地文件、不发起网络请求、不提供投资建议、不代为下单。

---



## Triggers

**English Triggers:** backtest this trading strategy in Python, momentum strategy template for A-share, mean reversion with RSI and Bollinger, cointegrated pairs trading example, backtest performance metrics and Sharpe, walk-forward parameter optimization, transaction cost and slippage setup

**English Non-Triggers:** stock picking or buy/sell recommendations, price prediction for a specific symbol, general Python or pandas help, options pricing theory, fundamental valuation, portfolio marketing content

**中文触发词（须落在策略回测任务上才触发）：** 量化策略怎么回测 / 动量策略代码怎么写 / 均值回归参数怎么调 / 配对交易协整怎么检验 / 回测绩效指标怎么算 / 参数优化怎么防过拟合 / A股T+1和涨跌停怎么在回测里处理

**不触发清单：** 个股买卖建议与标的推荐、行情预测、通用编程问题、期权定价、基本面估值、营销文案

**路由判定三步**：① 是否已有（或正在设计）一条**可编码的交易规则**？② 诉求是否为把它回测、评估或优化？③ 前两步均为是才启用本技能；若只是想知道买什么，转投研或选股类技能。

## Workflow


### Step 1: Define the Strategy Brief

Collect the trading idea:
- **Strategy type**: Momentum, mean reversion, breakout, pairs trading, ML-based, event-driven
- **Market**: A-share (sh/sz), HK stock (hk), US equity (us)
- **Timeframe**: Intraday (1m/5m/15m), daily, weekly, monthly
- **Assets**: Single stock, ETF, index, portfolio
- **Entry/Exit signals**: Technical indicators, price patterns, fundamental signals, ML predictions
- **Position sizing**: Fixed, Kelly criterion, risk-parity, dynamic
- **Constraints**: Max position size, long-only/short, turnover limit, slippage model

**简报示例（合格）：**
> 策略类型：动量；市场：A股（沪深300成分股）；频率：日线；标的：成分股等权；信号：20日动量排名前20%；仓位：等权，最多10只；约束：仅做多、单边成本0.15%、单票上限10%、剔除ST与上市不足60日个股；回测区间：2019-01-01 至 2026-08-31。

**简报示例（不合格及原因）：**
> "帮我做个能稳定赚钱的量化策略。"
>
> 缺少市场、频率、成本、仓位与约束，任何回测结果都无法验证。更关键的缺失是**没有失败条件**——合格简报应写明"什么情况下判定策略不可用"（如样本外夏普<0.5 或最大回撤>25% 即放弃）。


**再举一例（跨市场简报的差异）：** 同一个「20 日动量、前 20%、持有 5 日」的想法，写成 A 股简报与美股简报时约束完全不同。A 股版本必须写明：T+1（信号次日开盘执行）、涨停不可买入（顺延）、剔除 ST 与上市不足 60 日、单边成本约 0.15%、仅做多。美股版本则可写：T+0 当日收盘执行、允许做空、成本按每股或按比例另设。**把 A 股简报的美股约束照抄过去，是最常见的回测失真来源。**

### Step 2: Strategy Design & Code Generation

Based on the brief, generate production-quality Python code:

#### A. Momentum Strategy Template
```python
import pandas as pd
import numpy as np
import backtrader as bt

class MomentumStrategy(bt.Strategy):
    params = (
        ('lookback', 20),       # 回望期
        ('hold_period', 5),    # 持有期
        ('rank_percentile', 0.2),  # 选股分位数
    )

    def __init__(self):
        self.inds = {}
        for d in self.datas:
            self.inds[d] = {}
            self.inds[d]['momentum'] = bt.indicators.RateOfChange(
                d.close, period=self.params.lookback
            )

    def next(self):
        # 按动量排序，取前20%
        rankings = sorted(
            self.datas,
            key=lambda d: self.inds[d]['momentum'][0],
            reverse=True
        )[:int(len(self.datas) * self.params.rank_percentile)]

        # 平仓不在榜单的持仓
        for d in self.datas:
            if d not in rankings and self.getposition(d).size > 0:
                self.close(d)

        # 买入榜单中的标的
        # 注意：rankings 为空时 1.0/len(rankings) 会除零，必须先返回
        if not rankings:
            return
        for d in rankings:
            if self.getposition(d).size == 0:
                self.order_target_percent(d, 1.0 / len(rankings))
```

**调用示例与常见坑：**

```python
cerebro = bt.Cerebro()
cerebro.addstrategy(MomentumStrategy, lookback=20, hold_period=5, rank_percentile=0.2)
# 关键：传入的是"回望期内的动量"，必须剔除上市不足 lookback 天的新股，
# 否则新股会因为没有足够历史而产生极端 ROC 值，长期占据榜单前排。
```

- **坑一（未来函数）**：若在 `next()` 里用当收盘价排序并在同一根 K 线以收盘价成交，等于用到了收盘才可知的信息。A 股应改为**次日开盘或次日均价成交**。
- **坑二（涨跌停不可成交）**：榜单里的股票当日一字涨停时无法买入，回测若照单全收会高估收益。应对方式：当日涨停则跳过，顺延至下一交易日。
- **坑三（集中度过低）**：`1.0 / len(rankings)` 在 rankings 为空时会除零，需先判断 `if rankings:`。

#### B. Mean Reversion Strategy Template
```python
class MeanReversionStrategy(bt.Strategy):
    params = (
        ('bb_period', 20),
        ('bb_dev', 2.0),
        ('rsi_period', 14),
        ('rsi_oversold', 30),
        ('rsi_overbought', 70),
    )

    def __init__(self):
        self.bb = bt.indicators.BollingerBands(
            self.data.close, period=self.params.bb_period,
            devfactor=self.params.bb_dev
        )
        self.rsi = bt.indicators.RSI(
            self.data.close, period=self.params.rsi_period
        )

    def next(self):
        if self.position.size == 0:
            # 价格触及下轨且RSI超卖 → 买入
            if self.data.close < self.bb.lines.bot and \
               self.rsi < self.params.rsi_oversold:
                self.order_target_percent(self.data, 1.0)
        else:
            # 价格触及上轨或RSI超买 → 卖出
            if self.data.close > self.bb.lines.top or \
               self.rsi > self.params.rsi_overbought:
                self.close()
```

**调用示例与参数敏感度说明：**

```python
# rsi_oversold 从 30 调到 25，交易次数可能从 127 次降到 70 次以下，
# 而样本外夏普从 1.12 掉到 0.6 —— 这种"微调剧变"就是过拟合信号。
cerebro.addstrategy(MeanReversionStrategy, bb_period=20, bb_dev=2.0,
                    rsi_period=14, rsi_oversold=30, rsi_overbought=70)
```

- **适用场景**：震荡市中表现较好；单边下跌行情里"越跌越买"会连续触发买入信号，形成典型的**均值回归陷阱**——建议叠加趋势过滤（如仅在收盘价高于 MA60 时允许开仓）。
- **A 股注意**：T+1 制度下当日买入不能当日卖出，若策略在盘中触发卖出信号，回测中必须顺延到下一交易日，否则会虚增收益。


**再举一例（均值回归陷阱的量化对照）：** 同一策略在 2019-2021 震荡市年化 14.2%、最大回撤 -11%；在 2022 单边下行年化 -23%、最大回撤 -34%，且触发买入 31 次（越跌越买）。叠加「收盘价 > MA60 才允许开仓」的趋势过滤后，2022 年交易次数降到 6 次、回撤收窄到 -16%，全区间年化由 6.1% 回升到 9.8%。**结论**：均值回归策略必须把趋势过滤写进规则，而不是作为可选优化。

#### C. Pairs Trading Strategy
```python
import statsmodels.api as sm

def find_cointegrated_pairs(data_dict):
    """寻找协整配对"""
    n = len(data_dict)
    pairs = []
    symbols = list(data_dict.keys())

    for i in range(n):
        for j in range(i + 1, n):
            try:
                x = data_dict[symbols[i]]
                y = data_dict[symbols[j]]
                # OLS回归
                X = sm.add_constant(x)
                model = sm.OLS(y, X).fit()
                residuals = model.resid
                # ADF检验
                adf_result = sm.tsa.stattools.adfuller(residuals)
                if adf_result[0] < adf_result[4]['1%']:
                    pairs.append((symbols[i], symbols[j], adf_result[0]))
            except:
                continue
    return sorted(pairs, key=lambda x: x[2])

def pairs_trading_signals(spread, z_entry=2.0, z_exit=0.5):
    """配对交易信号"""
    signals = pd.Series(0, index=spread.index)
    z_score = (spread - spread.mean()) / spread.std()

    signals[z_score < -z_entry] = 1    # 做多价差
    signals[z_score > z_entry] = -1     # 做空价差
    signals[abs(z_score) < z_exit] = 0  # 平仓
    return signals
```

**调用示例：**

```python
pairs = find_cointegrated_pairs({"600036": s_a, "601318": s_b})
# => [("600036", "601318", -3.87)]   ADF 统计量 -3.87 < 1% 临界值，判定协整

spread = s_a - 1.24 * s_b           # 1.24 来自 OLS 回归系数
signals = pairs_trading_signals(spread, z_entry=2.0, z_exit=0.5)
```

- **关键提醒一**：`z_score` 用全样本 `mean()`/`std()` 计算会引入未来函数。实务中应使用**滚动窗口**（如过去 60 日）的均值与标准差。
- **关键提醒二**：协整关系会衰减。建议在回测中每 N 个月重新检验一次协整，关系破裂即停止交易该配对，而不是一路持有到止损。
- **关键提醒三**：A 股缺乏便捷的做空渠道，配对交易的"做空腿"往往无法实现，因此在 A 股使用时应明确标注为"仅做多腿的变体"，收益预期需相应下调。


**再举一例（协整衰减的滚动检验结果）：** 某配对在 2020-2022 的 ADF 统计量稳定在 -3.5 以下（协整成立），2023 年起升至 -2.1（不再显著），但策略仍在交易，当年亏损 -14%。改为每 6 个月重检一次、ADF 统计量 > -2.9 即停止该配对后，2023 年该配对空仓，组合全年回撤收窄 6 个百分点。**结论**：协整检验必须是滚动的、带停止规则的，一次性检验等同于假设关系永续。

### Step 3: Backtest Execution

Guide the user through running the backtest:

```python
import backtrader as bt
import pandas as pd

# 加载数据
data = bt.feeds.GenericCSVData(
    dataname='historical_data.csv',
    dtformat='%Y-%m-%d',
    datetime=0,
    open=1, high=2, low=3, close=4, volume=5,
    openinterest=-1
)

# 运行回测
cerebro = bt.Cerebro()
cerebro.addstrategy(MomentumStrategy)
cerebro.adddata(data)
cerebro.broker.setcash(1000000.0)  # 100万初始资金
cerebro.broker.setcommission(commission=0.001)  # 千一手续费
cerebro.addsizer(bt.sizers.PercentSizer, percents=95)

print(f'初始资金: {cerebro.broker.getvalue():,.2f}')
cerebro.run()
print(f'最终资金: {cerebro.broker.getvalue():,.2f}')
```

**A股成本设置的正确示范：**

```python
# 佣金双边 + 印花税（卖出单边）+ 滑点，缺一项都会高估收益
cerebro.broker.setcash(1_000_000.0)
cerebro.broker.setcommission(commission=0.0003, stocklike=True)   # 佣金万三
cerebro.broker.set_slippage_perc(perc=0.0005)                     # 滑点万五
# 印花税需在卖出侧单独计入（历史口径曾为卖出单边 0.1%，以最新官方口径为准）
```

**一次性跑完的最小检查清单：**
1. 初始资金与期末资金是否如预期变化（没变说明根本没有成交）
2. 成交笔数是否合理（为 0 说明信号从未触发；过多说明成本被低估）
3. 是否有信号落在停牌日或涨跌停日（有则说明缺少可交易性过滤）

4. 成交价格是否为「信号次日开盘/均价」而非「信号当日收盘」（用当日收盘成交即含未来函数）
5. 期末资金不变时需反向排查：是信号未触发、还是全部订单被可交易性过滤掉

**再举一例（成本口径差异导致的结论反转）：** 同一日频策略（年换手 18 倍），三种成本假设下净年化分别为：仅佣金万三 → 12.4%；加印花税与滑点（合计单边约 0.15%）→ 6.1%；成本翻倍 → -0.8%。**同一套信号，成本口径不同就能从「可用」变成「不可用」**，因此回测报告必须把成本口径写在结论之前。

### Step 4: Performance Analysis

Generate comprehensive performance metrics:

| Metric | Description | Target | Formula / 计算口径 | 常见误读 | A股口径注意点 |
|--------|-------------|--------|-------------------|---------|---|
| Total Return | Cumulative return | > Benchmark | 期末权益/期初权益 - 1 | 忽略分红再投与复权方式差异 | 需明确用前复权还是后复权，结论不可混用 |
| Annualized Return | CAGR | > 10% (A-share), > 8% (HK/US) | (终值/初值)^(252/交易日数) - 1 | 回测期不足一年时年化会严重放大 | A股按约 244 个交易日/年折算，非固定 252 |
| Sharpe Ratio | Risk-adjusted return | > 1.5 | (年化收益 - 无风险利率)/年化波动 | 用日收益简单乘√252 前需确认收益无自相关 | 无风险利率建议用同期国债或货币基金收益，口径须写明 |
| Max Drawdown | Peak-to-trough loss | < 20% | max((峰值 - 当前值)/峰值) | 只看数值不看持续天数，低估心理压力 | A股极端行情下回撤持续天数常长于美股 |
| Win Rate | Percentage of profitable trades | > 50% | 盈利次数/总平仓次数 | 高胜率配低盈亏比仍可能整体亏损 | A股 T+1 下同一笔日内无法反复开平，次数天然偏低 |
| Profit Factor | Gross profit / Gross loss | > 1.5 | 总盈利/总亏损 | 不含成本时会被系统性高估 | 必须含印花税与滑点，否则系统性高估 |
| Calmar Ratio | Annual return / Max DD | > 1.0 | 年化收益/最大回撤 | 回测期短时最大回撤尚未充分暴露 | A股熊市长，Calmar 普遍低于美股同类策略 |
| Sortino Ratio | Return / Downside deviation | > 1.0 | (年化收益 - 无风险利率)/下行波动 | 与夏普混用会导致横向比较失真 | 下行波动的门槛设定需与回撤口径一致 |
| Turnover / 换手率 | 年化双边成交额/平均权益 | 视策略而定 | 年双边成交额/平均权益 | 常被忽略，却是成本吞噬的主因 | A股换手成本中印花税占比高，降换手收益明显 |
| Exposure / 持仓暴露 | 有仓位时间占比 | 视策略而定 | 持仓交易日/总交易日 | 低暴露策略的年化收益不可直接对比满仓策略 | A股停牌期持仓时间被拉长，暴露口径需说明 |

### Step 5: Optimization & Stress Testing

```
A. 参数优化
   - Grid search over key parameters
   - Walk-forward analysis (in-sample / out-of-sample)
   - Avoid overfitting: use Information Coefficient (IC) analysis

B. 压力测试
   - Historical crises: 2008, 2015 A-share crash, COVID-19 (2020)
   - Monte Carlo simulation of equity curves
   - Sensitivity analysis: commission, slippage, spread assumptions

C. 风险分析
   - Position-level VaR (Value at Risk)
   - Factor exposure (momentum, size, volatility)
   - Tail risk: maximum loss scenarios
```

**压力测试示例（A股场景）：**

| 情景 | 假设 | 观察指标 | A股特有因素 |
|------|------|---------|---|
| 2015 年异常波动 | 指数快速回撤、流动性骤降、大面积停牌 | 策略最大回撤、停牌期间无法减仓的比例 | 大面积停牌导致减仓指令无法执行 |
| 2018 年单边下跌 | 全年趋势向下 | 均值回归类策略是否连续触发买入、资金是否耗尽 | 越跌越买叠加 T+1，当日无法纠错 |
| 2020 年疫情冲击 | 短期急跌后快速反弹 | 止损是否被触发在最低点、反弹是否踏空 | 涨停排队无法建仓，反弹踏空 |
| 流动性收缩 | 成交额下降 50% | 冲击成本上升后的净收益变化 | 小市值标的冲击成本成倍上升 |
| 成本翻倍 | 佣金与印花税假设提高 100% | 净收益是否仍为正——若为负说明策略靠低成本存活 | 印花税占比高，成本翻倍影响被放大 |

**参数优化示例（Walk-forward）：**
```
样本划分：2019-2023 为优化期，2024-2026 为样本外
滚动方式：每 12 个月重新优化一次参数，用下一年数据检验
判定规则：样本外夏普 / 样本内夏普 > 0.6 视为可接受；< 0.4 判定过拟合
```
若样本内夏普 1.8、样本外 0.5（比值 0.28），即使样本内指标漂亮，也应判定该策略不可用。

## Input/Output Examples

### Example 1: Strategy Design Request

**Input:**
```
Design a momentum strategy for A-share market.
Criteria:
- Daily timeframe
- Universe: CSI 300 constituents (沪深300成分股)
- Lookback: 20 days
- Hold for 5 days
- Long only
- Top 20% by momentum score
- Max 10 positions
- Exclude ST stocks and names listed < 60 trading days
```

**Output:**
```
Strategy Design Summary:

┌─────────────────────────────────────────┐
│ Strategy: Top-Momentum Long-Only        │
│ Market: A-share (CSI 300 constituents)  │
│ Timeframe: Daily                        │
│ Backtest Period: 2019-01-01 to 2026-08-31 │
└─────────────────────────────────────────┘

Key Components:
1. Momentum ranking: ROC(close, period=20)
2. Selection: Top 20% by momentum score (max 10 stocks)
3. Position sizing: Equal weight (10% per position)
4. Hold period: 5 trading days
5. Execution: signal at today's close, execute at NEXT day's open (T+1)
6. Filters: skip limit-up (unable to buy), skip suspended, exclude ST

Expected Performance (illustrative, before/after cost):
- Annualized Return: 12-18% (gross) / 8-13% (net of ~0.15% one-way cost)
- Sharpe Ratio: 0.7-1.1
- Max Drawdown: 28-38%
- Win Rate: 50-55%
- Turnover: 12-18x per year  <- cost dominates; report it

Code generated at: strategy_momentum_a_share.py
```

> **口径提示**：本示例为 A 股，因此执行价为**次日开盘**、需剔除涨停与停牌、且仅做多。若把同一段代码用于美股或中国香港市场，上述三项约束均不适用，须重新设定——**市场口径不可跨市场套用**。

### Example 2: Performance Report


**Input:**
```
Compare these two strategies: RSI mean reversion vs momentum breakout on CSI 300 (000300)
Period: 2020-2024
Initial capital: 1,000,000 CNY
```

**Output:**
```
Backtest Results: CSI 300 Strategies (2020-2024)

┌──────────────────────┬─────────────────────┬────────────────────┐
│ Metric               │ RSI Mean Reversion  │ Momentum Breakout  │
├──────────────────────┼─────────────────────┼────────────────────┤
│ Total Return         │ +68.3%              │ +124.7%            │
│ Annualized Return    │ +13.2%              │ +17.8%             │
│ Sharpe Ratio         │ 1.12               │ 1.45               │
│ Max Drawdown         │ -22.1%             │ -31.4%             │
│ Win Rate             │ 58.3%              │ 49.2%              │
│ Profit Factor        │ 1.82               │ 1.67               │
│ Calmar Ratio         │ 0.60               │ 0.57               │
│ Avg Holding Days     │ 8.2                │ 4.6                │
│ Total Trades         │ 127                │ 284                │
└──────────────────────┴─────────────────────┴────────────────────┘
Benchmark: CSI 300 Index (+42.1% over same period)

Reading of the results (methodological comparison, not a recommendation):
- RSI Mean Reversion: lower drawdown and higher win rate, lower total return — the relevant question for research is whether it survives cost assumptions at its trade count
- Momentum Breakout: higher total return with roughly 2x the trades, deeper drawdown — its edge is highly sensitive to turnover and cost settings

本表仅为两套规则在同一口径下的回测结果对照，用于说明「指标如何读、成本如何改变结论」，
不构成任何投资建议、标的推荐或买卖决策依据。


A-share markets are subject to significant regulatory and liquidity risks.
```

## Strategy Templates Library

| Strategy Type | Best For | Timeframe | Markets | 典型失效场景 | A股落地难点 | 回测必设过滤 |
|--------------|----------|-----------|---------|------------|------------|---|
| Momentum | Trending markets | Daily/Weekly | All | 急转弯行情（风格切换） | T+1 导致信号次日才可执行 | 剔除上市不足 N 日、剔除一字涨停、次日开盘成交 |
| Mean Reversion | Range-bound markets | Intraday/Daily | All | 单边下跌（越跌越买） | 涨跌停无法成交、T+1 | 剔除停牌、跌停不可买入、T+1 顺延卖出 |
| Breakout | Volatile markets | Intraday/Daily | All | 假突破密集期 | 涨停排队难以建仓 | 涨停不可追入、需判断封板可成交性 |
| Pairs Trading | Market-neutral | Daily | US/HK | 协整关系破裂 | 做空腿难以实现 | 标注仅做多腿变体、滚动协整检验 |
| Machine Learning | Alpha discovery | Daily | All |  regime 变化、特征漂移 | 可解释性与留痕要求高 | 特征 point-in-time、可解释性留痕 |
| Event-Driven | Corporate actions | Daily | A-share/US | 事件被提前price-in | 事件数据 point-in-time 难保证 | 事件可得时点校验、避免事后回填 |

## Best Practices

1. **Always use out-of-sample testing** — split data 70/30 or use walk-forward
2. **Account for transaction costs** — A-share commission + stamp tax ≈ 0.15% per trade
3. **Include slippage** — assume 0.05-0.1% for liquid stocks, higher for illiquid
4. **Diversify across uncorrelated strategies** — don't rely on one strategy
5. **Stress test for A-share specifics** — T+1 trading, limit-up/limit-down, suspension risks
6. **Validate with paper trading** — run live for 1-3 months before real capital
7. **Beware of overfitting** — fewer parameters = more robust strategy

8. **报告成本口径与换手率** — 无换手与成本假设的绩效表不可采信
9. **固定「可获得时点」** — 因子与另类数据必须按 point-in-time 取用，避免事后回填

**举例说明第 8 条（为什么必须先报成本）：** 两个策略毛年化同为 15%，A 换手 5 倍、B 换手 20 倍。按 A 股单边约 0.15% 计，A 的成本拖累约 1.5%、B 约 6%。净额分别为 13.5% 与 9%——**毛收益相同，净收益差 4.5 个百分点**。只看毛收益会把 B 误判为同样优秀。

**举例说明第 9 条（point-in-time 失真）：** 用某行业景气指数构建因子，数据供应商在每月 20 日发布上月数值，但接口返回的是「发布日」而非「所属月份」。若按发布日期对齐，等于提前 20 天知道了当月数值，回测夏普从真实的 0.6 虚增到 1.4。**修法**：为每个数据字段记录「可获得时点」，回测中只允许使用该时点之前已发布的版本。

**举例说明第 2 条（交易成本）为何致命：** 某日频策略年换手 20 倍，单边成本按 0.15% 计，年化成本约 6%。若策略毛年化超额为 8%，扣费后仅剩 2%，再计入滑点后大概率归零。因此**高换手策略必须先算成本再算收益**。

**举例说明第 5 条（A股特性）：** 某策略在 2015 年 6-8 月期间发出减仓信号，但持仓标的中 40% 处于停牌状态，实际无法卖出。回测若假设全部成交，会把最大回撤从真实的 -45% 写成 -28%，严重低估风险。

**举例说明第 6 条（模拟盘）：** 正式投入资金前，建议先做 1-3 个月模拟或小额实盘，重点验证的不是收益，而是"信号能否按回测假设成交"——实盘中的成交价、可成交量、停牌与临停，往往与回测假设差距最大。

## Changelog / 变更记录

| 版本 | 日期 | 变更摘要 |
|------|------|---------|
| 5.0.3 | 2026-10-09 | 移除 Example 2 中与「不提供投资建议」边界冲突的 Recommendation 段落（按风险偏好推荐策略），改为口径对照式的结论读法说明（SDI-4） |
| 5.0.2 | 2026-10-09 | 修复 Example 1 的市场口径不一致：A 股示例改用沪深300成分股、标注 A-share 市场并补 T+1/涨停/停牌过滤与成本口径（SDI-4）；修复 MomentumStrategy 中 rankings 为空时的除零缺陷并补返回保护；新增语言与适用市场声明（SQP-3）与数据最小化/执行边界章节；收窄中英文触发词、补充非触发清单与路由判定三步；动态更新至 2026-10-09 并新增回测口径五项披露、另类数据 point-in-time 两条；新增列：A股口径注意点、A股特有因素、回测必设过滤、常见造假/失真手法、实际暴露提示；Step1-3 各补一例（含跨市场简报差异、均值回归趋势过滤量化对照、协整衰减滚动检验）；Best Practices 补 2 条与 2 例；测试用例补 TC005/TC006 |
| 5.0.1 | 2026-09-14 | 融合阿里点金回测流程与指标体系 |

---



## Risk Disclaimer

This skill provides backtesting tools and historical analysis for educational and research purposes only. Backtested results are not indicative of future performance. Real trading involves significant risks including market volatility, liquidity constraints, regulatory changes, and model risk. Always consult with qualified financial advisors before making investment decisions.
## Appendix G. Alibaba Dianjin Fusion — ai-trading-backtester v5.0.3

> **Source**: Alibaba Dianjin Digital Employee — `investment-advisor` (AI投资顾问) & `quant-researcher` (AI量化研究员)  
> **Essence**: 策略回测、参数优化、风险控制、绩效评估  
> **Integrated**: 2026-05-31
> **Last reviewed**: 2026-11-19

---

### G.1 Core Workflow (Dianjin essence)

```
策略回测流程：
1. 策略定义：买入条件+卖出条件+止损条件
2. 数据准备：历史K线+成交量+因子数据
3. 回测执行：按时间顺序模拟交易
4. 绩效计算：收益率+夏普比率+最大回撤
5. 参数优化：网格搜索/贝叶斯优化
6. 风险分析：回撤期+胜率+盈亏比
```

---

### G.2 Backtest Metrics (Dianjin method)

**核心指标体系**：

| 指标 | 计算公式 | 优秀标准 | 及格标准 | 易被操纵的方式 | 交叉验证指标 | 常见造假/失真手法 |
|------|---------|---------|---------|--------------|------------|---|
| 年化收益率 | (终值/初值)^(252/交易日)-1 | >20% | >8% | 缩短回测期至强年份 | 分年度收益是否稳定 | 只报强年份区间、或把模拟盘接在回测末尾 |
| 夏普比率 | (年化收益-无风险利率)/年化波动 | >1.5 | >0.5 | 剔除极端亏损交易日 | 与索提诺、Calmar 同时看 | 剔除极端亏损日、或按周收益算年化波动 |
| 最大回撤 | max((历史最高-当前)/历史最高) | <15% | <30% | 只报告收盘价回撤 | 回撤持续天数与恢复天数 | 只看收盘价回撤、或用区间收益掩盖路径 |
| 胜率 | 盈利次数/总次数 | >60% | >45% | 用极短止盈拉高胜率 | 盈亏比是否同步下降 | 把未平仓浮盈计为已实现盈利 |
| 盈亏比 | 平均盈利/平均亏损 | >2.0 | >1.5 | 放宽止损拉高盈亏比 | 最大回撤是否同步恶化 | 把止损位外移后不重算胜率 |
| 索提诺比率 | (年化收益-无风险利率)/下行波动 | >2.0 | >1.0 | 下行波动口径自行定义 | 与最大回撤交叉核对 | 自行定义下行波动门槛以美化结果 |
| 换手率 | 年双边成交额/平均权益 | 视策略 | 视策略 | 常常干脆不报告 | 与净收益同时报告 | 只报单边成交额，或干脆不报告 |

**回测报告模板（Dianjin风格）**：

```
【策略回测报告】均线突破策略（5日+20日）

一、回测参数
- 标的：沪深300指数 (000300.SH)
- 周期：2019-01-01 至 2026-05-31
- 频率：日线
- 初始资金：100万
- 交易成本：单边0.1%（佣金0.03%+印花税0.07%）

二、绩效指标
✅ 年化收益率：18.5%（优秀）
✅ 夏普比率：1.62（优秀）
❌ 最大回撤：-28.3%（不及格，应<15%）
⚠️ 胜率：52.3%（及格）
⚠️ 盈亏比：1.85（及格）

三、分年度表现
| 年份 | 收益率 | 最大回撤 | 夏普比率 |
|------|--------|----------|----------|
| 2019 | +32.5% | -12.3% | 2.1 |
| 2020 | +28.7% | -15.8% | 1.8 |
| 2021 | -8.2% | -22.5% | -0.3 |
| 2022 | -15.3% | -28.3% | -0.8 |
| 2023 | +22.1% | -10.5% | 1.5 |
| 2024 | +12.8% | -8.7% | 1.2 |
| 2025 | +25.6% | -9.2% | 1.9 |

四、问题诊断
❌ 2022年回撤-28.3%（策略在熊市表现差）
❌ 胜率仅52.3%（信号质量不高）
⚠️ 交易成本年化-3.2%（高频交易成本高）

五、改进建议
1. 增加趋势过滤（仅在MA60向上时开仓）
2. 优化止损（当前-8%止损太宽，改为-5%）
3. 降低交易频率（当前年均交易45次，降至20次以下）
```

---

### G.3 Parameter Optimization (Dianjin essence)

**参数优化方法**：

```
方法1：网格搜索（Grid Search）
  - 优点：简单，保证找到全局最优
  - 缺点：计算量大（参数多时指数爆炸）
  - 适用：参数少（<5个），范围小

方法2：贝叶斯优化（Bayesian Optimization）
  - 优点：高效，用高斯过程建模目标函数
  - 缺点：实现复杂，可能陷入局部最优
  - 适用：参数多（>5个），计算资源有限

方法3：遗传算法（Genetic Algorithm）
  - 优点：全局搜索能力强，适合复杂目标
  - 缺点：收敛慢，参数调优难
  - 适用：非线性、多峰目标函数
```

**过拟合风险警示（Dianjin重点）**：

```
⚠️ 过拟合信号：
1. 样本内绩效远优于样本外（差距>50%）
2. 参数极度敏感（微调参数导致绩效剧变）
3. 交易次数过少（<20次，统计不显著）
4. 最大回撤发生在样本末端（未来函数嫌疑）

✅ 防过拟合措施：
1. 样本外测试（保留最近1-2年数据不参训）
2. 滚动窗口验证（Walk-forward，每N个月重新优化）
3. 参数稳定性检验（参数在合理范围内波动，绩效不剧变）
4. 经济逻辑检验（策略要有合理解释，不能纯数据挖掘）
```

---

### G.4 Risk Control & Position Management (Dianjin method)

**仓位管理模型**：

```
固定比例法（最简单）：
  - 单一策略：股票仓位≤30%
  - 组合策略：总仓位≤80%

凯利公式（Kelly Criterion）：
  仓位 = (胜率 × 盈亏比 - 败率) / 盈亏比
  例：胜率55%，盈亏比2.0 → 仓位 = (0.55×2-0.45)/2 = 32.5%

ATR仓位法（波动率调整）：
  仓位 = 账户资金 × 风险系数 / (ATR × 合约乘数)
  例：账户100万，风险系数0.02，ATR=2元，合约乘数100
  → 仓位 = 100万 × 0.02 / (2×100) = 100股（约占总资金2%）
```

**凯利公式的实操提醒：** 上例算出 32.5% 仓位，但凯利公式对胜率与盈亏比的估计误差极为敏感——若实际胜率是 50% 而非 55%，最优仓位会大幅下降。实务中普遍采用**半凯利或四分之一凯利**（上例取 16% 或 8%），以避免在参数高估时过度下注。

**ATR 仓位法举例（跨标的比较）：**

| 标的 | ATR | 单笔风险预算 2% 时的股数 | 占总资金 | 实际暴露提示 |
|------|-----|----------------------|---------|---|
| 高波动个股（ATR=2元，价格20元） | 2.0 | 100股 | 约2%名义，实际暴露高 | 名义仓位低但日内波动大，需按波动贡献复核 |
| 低波动蓝筹（ATR=0.3元，价格20元） | 0.3 | 667股 | 约13%名义 | 名义仓位高但波动贡献可控，符合风险预算设计 |

同一风险预算下，低波动标的自然获得更高名义仓位，这正是波动率调整的目的：**让每笔交易的风险贡献相当，而不是让每笔交易的金额相当**。

---

### G.5 Test Case (Dianjin quality)

**Test Case: 策略回测+优化**

```
Input: "回测均线突破策略（5日+20日）在沪深300的表现，2019-2026"

Expected Output:
1. 回测参数（标的/周期/成本）
2. 绩效指标表（年化收益/夏普/最大回撤/胜率/盈亏比）
3. 分年度表现
4. 问题诊断（回撤过大/胜率过低）
5. 改进建议（增加过滤/优化止损）

Quality Check:
- ✅ 指标计算准确（公式正确）
- ✅ 问题诊断客观（不回避缺陷）
- ✅ 改进建议可行（有实操价值）
- ✅ 风险提示（过拟合风险）

Additional Cases:
- TC002: "策略回测夏普 1.9，但交易次数只有 18 次" → 判定统计不显著，要求延长样本或降低参数自由度
- TC003: "回测中未设置涨跌停过滤" → 判定存在可交易性缺陷，要求补过滤后重跑并对比差异
- TC004: "样本外夏普 0.5，样本内 1.8" → 判定过拟合，给出缩减参数与简化规则的改法
- TC005: "策略回测用当日收盘价成交" → 判定存在未来函数，要求改为次日开盘或均价成交并重跑对比
- TC006: "A股策略示例中标的写成 AAPL/TSLA 并标注 US Equity" → 判定市场口径不一致，要求改为沪深300成分股并补 T+1、涨停、停牌过滤
```

---

**End of Dianjin Fusion Content — ai-trading-backtester v5.0.3**

## 本轮增量（2026-11-14）：复核维度与举例补充

> 本节为 2026-11-14 例行轮转的净增量记录：新增举例与复核维度均为本期首次出现，与既有条目不重复；仅作方法论参考，需具备相应资质的人员复核后使用。

### 补充举例（按模块，本期新增）

**Strategy Templates Library**：

- 模板库补「市场与标的口径 / 成交成本假设」两项标注位，缺口径时不生成绩效对比草稿。
- 对示例策略新增「样本外区间」纸面核对项，避免把样本内结果直接外推。

**Best Practices**：

- 实践清单补「前视偏差检查 / 数据区间与基准一致性」两项，逐条留痕后再进入复核。
- 新增「模型与参数配置随版本记录」条目，便于对照不同版本口径，明确为文档记录口径。

### 新增复核维度表（2026-11-14）

> 本表新增「由谁执行 / 数据来源 / 复核要点 / 风险等级 / 适用边界」等维度列，把口径责任、数据来源与人工复核要求落到具体条目。

| 复核维度 | 由谁执行 | 数据来源 | 复核要点 | 风险等级 | 适用边界 |
| --- | --- | --- | --- | --- | --- |
| 样本外区间 | 研究员 + 复核人 | 行情数据 + 策略说明 | 切分点、区间重叠、基准一致性 | 高 | 研究草稿，不构成投资建议 |
| 前视偏差核对 | 研究员 + 复核人 | 信号与成交时序说明 | 信号时点、成交时点、可用信息集 | 高 | 纸面测算，结论须持牌人员复核 |

### 适用边界 / 数据最小化 / 执行边界（本期复核与补齐）

**适用边界**：本技能仅用于交易策略回测的教学与草稿结构参考，输出为供具备相应资质人员复核的纸面测算材料；不接入账户、不读取实盘数据、不代为交易或下单、不构成投资建议或收益承诺。涉及真实资金、实盘执行与对外发布研究结论的场景不适用，应转由相应业务系统与授权人员处理。

### 参考同类公开框架的补强（2026-11-14）

> 参考同类公开评测资料的思路补强：固定对照集与基线配对、模型与参数配置随版本记录、样本外与样本内分栏对照。仅吸收方法论结构，未引入具体工具、命令或第三方原文。

### 时效性说明

- 本期时效性核查：**截至 2026-11-14**。正文中的监管、政策、市场与行业动态为公开资料整理，具体文号、生效日期、数据区间与统计口径请以监管机构及官方渠道最新发布为准；未获官方原文核实的条目标注「需人工复核」，不填入未经核实的文号、日期或数字。
- 历史条目保留原发布日期以便追溯；本次更新未引入新的具体文号或统计数值。

## 本轮增量（2026-11-19）：复核维度与举例补充

> 本节为 2026-11-19 例行轮转的净增量记录：新增举例与复核维度均为本期首次出现，与既有条目不重复；仅作方法论参考，需具备相应资质的人员复核后使用。

### 补充举例（按模块，本期新增）

**Step 1: Define the Strategy Brief**：

- 策略简报补「口径与区间」两列：每个假设标注统计口径与样本区间，口径不一致的标注不可直接比较，草稿不代入具体数值。
- 约束清单新增「事实与假设分栏」：已披露的市场规则与拟设定的策略假设分列，假设栏标注需人工复核后使用。

**Step 4: Performance Analysis**：

- 绩效清单补「样本内／样本外分栏」：参与参数拟合的区间与未参与拟合的检验区间分列，草稿只记录区间划分，不给出放行结论。
- 归因表新增「统计口径」一列：每项指标标注所依据的样本区间与口径，区间不一致的标注不可直接比较。

### 新增复核维度表（2026-11-19）

> 本表新增「由谁执行 / 数据来源 / 复核要点 / 风险等级 / 适用边界」等维度列，把口径责任、数据来源与人工复核要求落到具体条目。

| 复核维度 | 由谁执行 | 数据来源 | 复核要点 | 风险等级 | 适用边界 |
| --- | --- | --- | --- | --- | --- |
| 简报口径区间 | 量化研究员 + 复核人 | 策略简报 / 公开数据 | 口径与区间是否标注、跨口径是否可比 | 中 | 纸面对照，结论须人工确认 |
| 样本内外分栏 | 量化研究员 | 绩效归因表 / 草稿 | 拟合与检验区间是否分列、口径是否标注 | 高 | 文档记录，不构成放行结论 |

### 适用边界 / 数据最小化 / 执行边界（本期复核与补齐）

**适用边界**：本技能仅用于量化策略回测与绩效分析的方法论纸面对照的方法论参考与纸面草稿，输出为供使用者自行判断的参考文本；不构成正式结论、专业意见或对外发布内容。涉及策略实盘上线、下单执行与正式绩效结论的场景不适用，应由具备相应资质的人员按既有制度独立完成。

**数据最小化**：本期补齐：示例、清单与提问只保留占位标签与抽象情境描述，不写入可识别个人、客户或机构的信息；草稿阶段即标注需人工复核后再补充任何具体背景。

**执行边界**：本期复核：文中「生成 / 输出 / 形成」均指生成待确认的纸面草稿，由使用者自行决定是否采用；不代为发布、提交、保存或进行任何系统操作。

### 参考同类公开框架的补强（2026-11-19）

> 参考 2026 年公开量化与评测资料中「前向验证把参数优化与样本外检验分离以消除前视偏差」「以同一基线与配置快照对比候选改动」「把评测集当回归测试、每次改动后重跑并阻断回归」的思路，在绩效分析章节补一个纸面自查清单：分列拟合区间、检验区间、配置快照与回归占位，并提示周期数、阈值与放行由具备资质的人员结合业务设定，草稿不填入未经核实的数值或结论。

### 时效性说明

- 本期时效性核查：**截至 2026-11-19**。正文中的监管、政策、市场与行业动态为公开资料整理，具体文号、生效日期、数据区间与统计口径请以监管机构及官方渠道最新发布为准；未获官方原文核实的条目标注「需人工复核」，不填入未经核实的文号、日期或数字。
- 历史条目保留原发布日期以便追溯；本次更新未引入新的具体文号或统计数值。
