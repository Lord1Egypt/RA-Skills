# Cross-Project Wisdom

Total: **23**

## `CW-BT-001` — Cerebro 统一编排引擎
**From**: backtrader · **Applicable to**: backtesting

backtrader 用 Cerebro 作为单一入口，统一管理 data feeds、strategies、analyzers、 observers 的生命周期，支持一次 cerebro.run() 跑多策略+多数据源。 zvt 的 StockTrader 目前每次实例化只绑定一套因子，缺乏统一的多策略组合编排层； 借鉴 Cerebro 模式可让用户把多个 Trader 实例组合到一个 runner 中对比评估。

## `CW-BT-002` — Analyzer 插件化绩效评估
**From**: backtrader · **Applicable to**: backtesting

backtrader 提供 SharpeRatio、DrawDown、TimeReturn、TradeAnalyzer 等即插即用 的 Analyzer，可在不修改策略代码的情况下附加任意绩效指标。 zvt 当前绩效评估能力较弱，没有标准化的 Analyzer 接口； 借鉴此模式可让用户 cerebro.addanalyzer(SharpeRatio) 即得风险调整收益报告。

## `CW-BT-003` — Sizer 仓位管理分离
**From**: backtrader · **Applicable to**: backtesting

backtrader 将仓位管理（每次开仓买多少股/多大比例）单独抽象为 Sizer， 与信号逻辑完全解耦；内置 FixedSize、PercentSizer 等，用户可自定义。 zvt 目前没有显式的 Sizer 概念，仓位控制逻辑散落在 Trader.on_profit_control 等钩子中； 引入 Sizer 接口可使策略信号与资金管理规则独立演化和组合复用。

## `CW-BT-004` — Order 类型全集（Limit/Stop/OCO/Bracket）
**From**: backtrader · **Applicable to**: backtesting

backtrader 支持 Market、Limit、Stop、StopLimit、OCO（二选一）、 Bracket（止盈止损一对订单）等丰富订单类型，并模拟成交滑点和手续费方案。 zvt 回测目前主要支持市价成交，缺乏限价委托和组合订单模拟； 对于高频或实盘对接场景，完善订单类型将大幅提升回测真实性。

## `CW-BT-005` — 数据重采样与重播（Resampling & Replaying）
**From**: backtrader · **Applicable to**: backtesting

backtrader 可将低级别数据（如 1 min）实时 resample 为高级别（如 1 day）并同步驱动策略， 或 replay 逐 tick 模拟 OHLC 形成过程，实现日内精细回测。 zvt 目前多时间框架通过预录入不同级别 K 线实现，缺少运行时动态重采样； 借鉴此模式可在不重复录入数据的前提下支持任意时间粒度组合回测。

## `CW-VN-001` — 事件驱动引擎 (EventEngine)
**From**: vnpy · **Applicable to**: live-trading

vnpy 的核心是一个异步事件总线（EventEngine），行情推送、委托回报、 成交通知等均以事件消息方式在各 App/Gateway 间流转， 天然支持实盘+回测同一套代码逻辑。 zvt 目前数据流是同步批量拉取，缺乏事件驱动架构； 对接实盘行情推送（如 WebSocket tick 流）时，事件驱动模式可大幅降低延迟。

## `CW-VN-002` — Gateway 多交易所统一接口抽象
**From**: vnpy · **Applicable to**: live-trading

vnpy 的 Gateway 层对 CTP 期货、XTP 证券、IB 等几十个交易接口做统一封装， 策略层只调用 buy/sell/cancel 通用接口，无需感知底层协议差异。 zvt 目前数据录入依赖具体 provider（em/joinquant），无统一的实盘交易 Gateway； 引入 Gateway 抽象可使 zvt 的因子+选股逻辑无缝对接实盘下单。

## `CW-VN-003` — CTA 回测引擎内置可视化
**From**: vnpy · **Applicable to**: backtesting

vnpy 的 cta_backtester 提供图形界面直接展示策略净值曲线、最大回撤、 每日盈亏、成交明细，无需 Jupyter Notebook。 zvt 目前回测结果可视化依赖 draw_result 方法调用 Plotly，但无统一的回测报告页面； 借鉴此模式可打包一个开箱即用的策略绩效仪表盘。

## `CW-VN-004` — vnpy.alpha ML 因子研究实验室（Lab）
**From**: vnpy · **Applicable to**: factor-research

vnpy 4.0 的 vnpy.alpha.lab 提供数据管理、模型训练、信号生成、策略回测一体化工作流， 支持 Lasso/LightGBM/MLP 等算法的标准化训练接口和可视化对比。 zvt 的 ML 能力目前仅有 MaStockMLMachine 一个入口，缺乏规范化 Lab 框架； 借鉴 Lab 模式可建立"特征工程→训练→信号→回测"的标准流水线，降低 ML 实验门槛。

## `CW-VN-005` — 价差交易（Spread Trading）模块
**From**: vnpy · **Applicable to**: live-trading

vnpy 支持自定义价差（如期货跨期套利、A股与港股溢价套利）， 实时计算价差行情、自动触发价差策略委托。 zvt 目前 compare() 只做可视化对比，缺乏价差信号计算和交易执行； 借鉴价差模块可扩展 zvt 到统计套利场景（如 AH 溢价、指数与成份股套利）。

## `CW-QL-001` — Point-in-Time 数据库（防未来数据泄漏）
**From**: qlib · **Applicable to**: backtesting

qlib 的 Point-in-Time Provider 保证在给定时间点 t 的查询只返回 t 时刻 真实可知的数据（财报发布延迟、修订历史均被正确处理）， 彻底消除回测中的 look-ahead bias。 zvt 目前财务数据以报告期为 timestamp，缺少"发布日"维度， 存在用未来财报数据做选股的潜在偏差；引入 PIT 模式可大幅提升回测可信度。

## `CW-QL-002` — Recorder + Experiment 实验管理（MLflow 风格）
**From**: qlib · **Applicable to**: factor-research

qlib 的 workflow 模块提供 Experiment/Recorder，自动记录每次模型训练的 超参数、特征、指标、预测结果，支持跨实验比较和模型版本管理。 zvt 目前缺乏 ML 实验追踪机制，每次重跑结果会覆盖前次； 借鉴 Recorder 模式可将每次因子实验的参数和结果持久化，支持快速复现和版本对比。

## `CW-QL-003` — Nested Decision Framework（多层嵌套决策执行）
**From**: qlib · **Applicable to**: backtesting

qlib 支持将高频执行层（分钟级委托拆单）嵌套在低频决策层（日级组合调仓）中， 两层独立优化且可组合运行，实现日内最优执行算法（如 TWAP、VWAP 调仓）。 zvt 目前回测仅有日线级别的成交假设，缺乏执行算法建模； 借鉴嵌套框架可让 zvt 区分"何时持有哪些股"与"如何以最小冲击成本建仓"两个问题。

## `CW-BT-001` — Cerebro 统一编排引擎
**From**: backtrader · **Applicable to**: backtesting

backtrader 用 Cerebro 作为单一入口，统一管理 data feeds、strategies、analyzers、 observers 的生命周期，支持一次 cerebro.run() 跑多策略+多数据源。 zvt 的 StockTrader 目前每次实例化只绑定一套因子，缺乏统一的多策略组合编排层； 借鉴 Cerebro 模式可让用户把多个 Trader 实例组合到一个 runner 中对比评估。

## `CW-BT-002` — Analyzer 插件化绩效评估
**From**: backtrader · **Applicable to**: backtesting

backtrader 提供 SharpeRatio、DrawDown、TimeReturn、TradeAnalyzer 等即插即用 的 Analyzer，可在不修改策略代码的情况下附加任意绩效指标。 zvt 当前绩效评估能力较弱，没有标准化的 Analyzer 接口； 借鉴此模式可让用户 cerebro.addanalyzer(SharpeRatio) 即得风险调整收益报告。

## `CW-BT-003` — Sizer 仓位管理分离
**From**: backtrader · **Applicable to**: backtesting

backtrader 将仓位管理（每次开仓买多少股/多大比例）单独抽象为 Sizer， 与信号逻辑完全解耦；内置 FixedSize、PercentSizer 等，用户可自定义。 zvt 目前没有显式的 Sizer 概念，仓位控制逻辑散落在 Trader.on_profit_control 等钩子中； 引入 Sizer 接口可使策略信号与资金管理规则独立演化和组合复用。

## `CW-BT-004` — Order 类型全集（Limit/Stop/OCO/Bracket）
**From**: backtrader · **Applicable to**: backtesting

backtrader 支持 Market、Limit、Stop、StopLimit、OCO（二选一）、 Bracket（止盈止损一对订单）等丰富订单类型，并模拟成交滑点和手续费方案。 zvt 回测目前主要支持市价成交，缺乏限价委托和组合订单模拟； 对于高频或实盘对接场景，完善订单类型将大幅提升回测真实性。

## `CW-BT-005` — 数据重采样与重播（Resampling & Replaying）
**From**: backtrader · **Applicable to**: backtesting

backtrader 可将低级别数据（如 1 min）实时 resample 为高级别（如 1 day）并同步驱动策略， 或 replay 逐 tick 模拟 OHLC 形成过程，实现日内精细回测。 zvt 目前多时间框架通过预录入不同级别 K 线实现，缺少运行时动态重采样； 借鉴此模式可在不重复录入数据的前提下支持任意时间粒度组合回测。

## `CW-VN-003` — CTA 回测引擎内置可视化
**From**: vnpy · **Applicable to**: backtesting

vnpy 的 cta_backtester 提供图形界面直接展示策略净值曲线、最大回撤、 每日盈亏、成交明细，无需 Jupyter Notebook。 zvt 目前回测结果可视化依赖 draw_result 方法调用 Plotly，但无统一的回测报告页面； 借鉴此模式可打包一个开箱即用的策略绩效仪表盘。

## `CW-VN-004` — vnpy.alpha ML 因子研究实验室（Lab）
**From**: vnpy · **Applicable to**: factor-research

vnpy 4.0 的 vnpy.alpha.lab 提供数据管理、模型训练、信号生成、策略回测一体化工作流， 支持 Lasso/LightGBM/MLP 等算法的标准化训练接口和可视化对比。 zvt 的 ML 能力目前仅有 MaStockMLMachine 一个入口，缺乏规范化 Lab 框架； 借鉴 Lab 模式可建立"特征工程→训练→信号→回测"的标准流水线，降低 ML 实验门槛。

## `CW-QL-001` — Point-in-Time 数据库（防未来数据泄漏）
**From**: qlib · **Applicable to**: backtesting

qlib 的 Point-in-Time Provider 保证在给定时间点 t 的查询只返回 t 时刻 真实可知的数据（财报发布延迟、修订历史均被正确处理）， 彻底消除回测中的 look-ahead bias。 zvt 目前财务数据以报告期为 timestamp，缺少"发布日"维度， 存在用未来财报数据做选股的潜在偏差；引入 PIT 模式可大幅提升回测可信度。

## `CW-QL-002` — Recorder + Experiment 实验管理（MLflow 风格）
**From**: qlib · **Applicable to**: factor-research

qlib 的 workflow 模块提供 Experiment/Recorder，自动记录每次模型训练的 超参数、特征、指标、预测结果，支持跨实验比较和模型版本管理。 zvt 目前缺乏 ML 实验追踪机制，每次重跑结果会覆盖前次； 借鉴 Recorder 模式可将每次因子实验的参数和结果持久化，支持快速复现和版本对比。

## `CW-QL-003` — Nested Decision Framework（多层嵌套决策执行）
**From**: qlib · **Applicable to**: backtesting

qlib 支持将高频执行层（分钟级委托拆单）嵌套在低频决策层（日级组合调仓）中， 两层独立优化且可组合运行，实现日内最优执行算法（如 TWAP、VWAP 调仓）。 zvt 目前回测仅有日线级别的成交假设，缺乏执行算法建模； 借鉴嵌套框架可让 zvt 区分"何时持有哪些股"与"如何以最小冲击成本建仓"两个问题。
