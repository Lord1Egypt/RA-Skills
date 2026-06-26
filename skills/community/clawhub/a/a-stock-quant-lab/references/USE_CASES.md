# Known Use Cases (KUC)

Total: **41**

## `KUC-DR-001`
**Source**: `examples/data_runner/actor_runner.py`

定时（每周三凌晨1点）批量采集机构投资者持仓、前十大流通股东、股东汇总数据， 支撑后续机构持仓变化的量化分析。

**Inputs**:
- {'data_provider': 'em'}
- {'entity_provider': 'em'}
- {'cron_schedule': 'hour=1, minute=0, day_of_week=2'}

**Components**:
- StockInstitutionalInvestorHolder
- StockTopTenFreeHolder
- StockActorSummary
- run_data_recorder
- BackgroundScheduler

**Parameters**:
```
{'day_data': True, 'sleeping_time': None}
```

**Validation**:
```
运行后查询 StockActorSummary.query_data() 返回非空 DataFrame， 且数据时间戳更新至最近报告期。

```

## `KUC-DR-002`
**Source**: `examples/data_runner/finance_runner.py`

每周五凌晨1点同步全市场A股财务四表（利润表、资产负债表、现金流量表、财务因子）， 保持本地数据库与东方财富数据源同步，为基本面选股提供原始数据。

**Inputs**:
- {'data_provider': 'eastmoney'}
- {'entity_provider': 'eastmoney'}
- {'cron_schedule': 'hour=1, minute=0, day_of_week=5'}

**Components**:
- Stock
- StockDetail
- FinanceFactor
- BalanceSheet
- IncomeStatement
- CashFlowStatement
- run_data_recorder
- BackgroundScheduler

**Parameters**:
```
{'day_data': True}
```

**Validation**:
```
FinanceFactor.query_data(limit=5) 返回含最新报告期记录， CashFlowStatement.query_data() 不为空。

```

## `KUC-DR-003`
**Source**: `examples/data_runner/index_runner.py`

维护A股指数基本信息及其成份股列表（国证1000/2000/成长/价值）， 并在每个交易日16:20后同步重要指数的日K行情，为板块轮动分析提供基础数据。

**Inputs**:
- {'data_provider': '"exchange" / "em"'}
- {'index_ids': ['index_sz_399311', 'index_sz_399303', 'index_sz_399370', 'index_sz_399371']}
- {'important_index_codes': 'IMPORTANT_INDEX 常量'}

**Components**:
- Index
- Index1dKdata
- IndexStock
- run_data_recorder
- BackgroundScheduler

**Parameters**:
```
{'day_data': True, 'entity_provider': 'exchange'}
```

**Validation**:
```
Index1dKdata.query_data(codes=IMPORTANT_INDEX) 返回当日收盘价记录。

```

## `KUC-DR-004`
**Source**: `examples/data_runner/joinquant_fund_runner.py`

每周六从聚宽采集公募基金基本信息、基金持仓明细和个股估值（PE/PB）， 支持基金重仓分析与价值择时策略。

**Inputs**:
- {'data_provider': 'joinquant'}
- {'entity_provider': 'joinquant'}

**Components**:
- Fund
- FundStock
- StockValuation
- run_data_recorder

**Parameters**:
```
{'sleeping_time': 0, 'day_data': True}
```

**Validation**:
```
FundStock.query_data(limit=5) 返回含基金代码和持仓股代码的记录。

```

## `KUC-DR-005`
**Source**: `examples/data_runner/joinquant_kdata_runner.py`

每个交易日15:30后从聚宽采集A股日后复权K线及交易日历， 保持本地历史行情数据库完整，为技术因子计算提供全量数据基础。

**Inputs**:
- {'data_provider': 'joinquant'}
- {'entity_provider': 'joinquant'}

**Components**:
- Stock
- StockTradeDay
- Stock1dHfqKdata
- run_data_recorder

**Parameters**:
```
{'force_update': False, 'day_data': True, 'sleeping_time': 0}
```

**Validation**:
```
Stock1dHfqKdata.query_data(entity_id="stock_sz_000001", limit=5) 返回最新交易日收盘价。

```

## `KUC-DR-006`
**Source**: `examples/data_runner/kdata_runner.py`

A股+港股每日全市场行情录入主流程：包含涨停数据、指数行情、板块行情（概念/行业）、 A股后复权K线、港股（南向通）行情，并推送新板块通知邮件。

**Inputs**:
- {'data_provider': 'em'}
- {'entity_provider': 'em'}
- {'sleeping_time': 0}

**Components**:
- LimitUpInfo
- Index
- Index1dKdata
- Block
- Block1dKdata
- Stock
- Stock1dHfqKdata
- Stockhk
- Stockhk1dHfqKdata
- get_entity_ids_by_filter
- EmailInformer
- run_data_recorder

**Parameters**:
```
{'ignore_delist': True, 'ignore_st': False, 'ignore_new_stock': False, 'return_unfinished': True, 'force_update': False}
```

**Validation**:
```
Stock1dHfqKdata.query_data(day_data=True) 及 LimitUpInfo.query_data() 均有当日记录， 邮件收到新板块通知。

```

## `KUC-DR-007`
**Source**: `examples/data_runner/kdata_runner.py`

采集涨停股的涨停原因并统计近期热门涨停题材（按出现频次排序）， 输出题材热度榜以辅助短线复盘。

**Inputs**:
- {'days_ago': '20 / 5'}
- {'limit': 15}

**Components**:
- LimitUpInfo
- get_hot_topics
- EmailInformer

**Parameters**:
```
{'reason_split_char': '+'}
```

**Validation**:
```
get_hot_topics(days_ago=5) 返回非空字典，键为题材名，值为出现次数。

```

## `KUC-DR-008`
**Source**: `examples/data_runner/kdata_runner.py`

采集A股全市场新闻标题，按可配置关键词分组统计各题材关联个股， 识别长期热门 vs 新热门 vs 退潮题材，辅助主题投资决策。

**Inputs**:
- {'hot_words_config': 'hot.json（主题:关键词列表）'}
- {'days_ago': '20 / 5'}
- {'threshold': 3}

**Components**:
- StockNews
- run_data_recorder
- get_hot_topics
- group_stocks_by_topic
- EmailInformer

**Parameters**:
```
{'sleeping_time': 2, 'force_update': False}
```

**Validation**:
```
report_hot_topics() 邮件包含"一直热门"、"+++"、"---"三段信息， 且每段均非空。

```

## `KUC-DR-009`
**Source**: `examples/data_runner/sina_data_runner.py`

从新浪采集A股板块（概念/行业）基本信息及板块资金流向， 提供与东方财富数据源互补的资金面视角。

**Inputs**:
- {'data_provider': 'sina'}

**Components**:
- Block
- BlockMoneyFlow
- run_data_recorder

**Parameters**:
```
{'day_data': True}
```

**Validation**:
```
BlockMoneyFlow.query_data(provider="sina", limit=5) 返回含 main_net_inflow 字段的记录。

```

## `KUC-DR-010`
**Source**: `examples/data_runner/trading_runner.py`

每个交易日18点采集龙虎榜，筛选出近一年胜率高的知名游资席位， 再过滤出30天内有该席位参与且当日成交额+换手率达标的个股，推送邮件供人工跟踪。

**Inputs**:
- {'data_provider': 'em'}
- {'entity_provider': 'em'}
- {'look_back_days': 400}
- {'recent_days': 30}
- {'dep_rate_threshold': 5}
- {'turnover_threshold': 300000000}
- {'turnover_rate_threshold': 0.02}

**Components**:
- DragonAndTiger
- Stock1dHfqKdata
- get_big_players
- EmailInformer
- run_data_recorder

**Parameters**:
```
{'sleeping_time': 2, 'day_data': True}
```

**Validation**:
```
DragonAndTiger.query_data(limit=5) 有当日记录，邮件包含"report 龙虎榜"主题。

```

## `KUC-FA-001`
**Source**: `examples/factors/boll_factor.py`

为A股个股计算布林带（Bollinger Bands）并标注突破上轨/下轨信号， 可视化价格与带宽关系，辅助均值回归与趋势跟踪策略。

**Inputs**:
- {'entity_ids': ['stock_sz_000338', 'stock_sh_601318']}
- {'provider': 'em'}
- {'start_timestamp': '2019-01-01'}
- {'data_level': '"1d" / "30m"'}

**Components**:
- BollTransformer (自定义 Transformer，使用 ta.volatility.BollingerBands)
- BollFactor (继承 TechnicalFactor)
- Stock1dHfqKdata / Stock30mHfqKdata

**Parameters**:
```
{'window': 20, 'window_dev': 2, 'output_columns': ['bb_bbm', 'bb_bbh', 'bb_bbl', 'bb_bbhi', 'bb_bbli', 'bb_bbw', 'bb_bbp'], 'filter_result': 'bb_bbli - bb_bbhi (1=价格在下轨, -1=价格在上轨)'}
```

**Validation**:
```
factor.draw(show=True) 弹出含价格+布林带三轨道图形； factor.result_df 包含 True/False/None 三种状态。

```

## `KUC-FA-002`
**Source**: `examples/factors/fundamental_selector.py`

用基本面多维度筛选"核心资产"：高ROE、高现金流、低财务杠杆、有增长、 低应收账款（应收<=总流动资产30%），为长线价值投资提供股票池。

**Inputs**:
- {'start_timestamp': '2016-01-01'}
- {'end_timestamp': '当前日期字符串'}
- {'codes': 'null（全A）'}

**Components**:
- FundamentalSelector (继承 TargetSelector)
- GoodCompanyFactor (使用 FinanceFactor 数据)
- GoodCompanyFactor (使用 BalanceSheet + accounts_receivable 过滤)
- BalanceSheet

**Parameters**:
```
{'provider': 'eastmoney', 'col_period_threshold': 'null (第二个 factor 不设列期数阈值)', 'accounts_receivable_max': '0.3 * total_current_assets'}
```

**Validation**:
```
selector.get_targets("2019-06-30") 返回非空 entity_id 列表， 手工核对结果含典型高ROE龙头股（如贵州茅台、格力电器等）。

```

## `KUC-FA-003`
**Source**: `examples/factors/tech_factor.py`

综合 MACD 金叉/多头趋势 + 均线多头排列（5/120/250日线）+ 成交额与换手率过滤， 识别"放量上攻牛股"，为日线趋势跟踪策略提供入场信号。

**Inputs**:
- {'entity_ids': '中大市值股票池（由 get_middle_and_big_stock 预过滤）'}
- {'start_timestamp': '2019-01-01'}
- {'adjust_type': 'AdjustType.hfq'}

**Components**:
- BullAndUpFactor (继承 MacdFactor)
- CrossMaTransformer (windows=[5, 120, 250])
- MacdFactor

**Parameters**:
```
{'turnover_threshold': 400000000, 'turnover_rate_threshold': 0.02, 'ma_windows': [5, 120, 250]}
```

**Validation**:
```
factor.result_df["filter_result"] 含 True 条目； report_bull() 邮件列出符合条件标的。

```

## `KUC-RP-001`
**Source**: `examples/reports/report_bull.py`

每个交易日18点自动筛选满足"牛股"条件（MACD金叉+多头趋势+成交量达标）的 A股及板块，分类推送邮件并同步到东方财富自选股组，辅助每日择股。

**Inputs**:
- {'target_date': 'get_latest_kdata_date() 自动获取'}
- {'entity_ids': 'get_middle_and_big_stock(timestamp)'}
- {'adjust_type': 'AdjustType.hfq (股) / AdjustType.qfq (板块)'}

**Components**:
- BullAndUpFactor
- report_targets
- get_middle_and_big_stock
- EmailInformer

**Parameters**:
```
{'turnover_threshold': 300000000, 'turnover_rate_threshold': 0.02, 'start_timestamp': '2019-01-01', 'em_group': 'bull股票', 'em_group_over_write': False, 'filter_by_volume': False}
```

**Validation**:
```
邮件主题包含"bull股票"且正文包含个股代码； 东方财富"bull股票"组有对应记录。

```

## `KUC-RP-002`
**Source**: `examples/reports/report_core_compay.py`

每周六基于基本面多因子模型（FundamentalSelector）筛选核心资产， 附上基金和QFII持仓占比变化，发邮件并同步东方财富"core"自选组， 为长线配置提供每周精选标的。

**Inputs**:
- {'start_timestamp': '2016-01-01'}
- {'end_timestamp': '当前日期'}
- {'subscriber_emails': 'subscriber_emails.json 文件'}

**Components**:
- FundamentalSelector
- TargetSelector
- StockActorSummary
- get_entities
- add_to_eastmoney
- EmailInformer

**Parameters**:
```
{'actor_type': 'ActorType.raised_fund / ActorType.qfii', 'em_group': 'core'}
```

**Validation**:
```
邮件含选股结果（含机构持仓占比）；若无结果则发送"no targets"。

```

## `KUC-RP-003`
**Source**: `examples/reports/report_tops.py`

每日17点计算A股短期最强（近期涨幅最高）和中期最强个股， 17:30计算最强行业板块和最强概念板块（按N日涨幅排名）， 并同步推送港股南向通短期/中期最强，辅助板块轮动和动量策略。

**Inputs**:
- {'periods': '短期=[近N天], 中期=[30,50]'}
- {'top_count': '10（板块）'}
- {'turnover_threshold': '100000000（港股）'}

**Components**:
- get_top_stocks
- report_top_entities
- get_top_performance_entities_by_periods
- Block
- BlockCategory
- inform
- EmailInformer

**Parameters**:
```
{'return_type': 'TopType.positive', 'ignore_new_stock': 'false / true', 'adjust_type': 'AdjustType.hfq / null', 'em_group_over_write': True}
```

**Validation**:
```
邮件分别包含"短期最强"、"中期最强"、"最强行业"、"最强概念"主题， 每组列出 top_count 数量标的。

```

## `KUC-RP-004`
**Source**: `examples/reports/report_vol_up.py`

筛选"放量突破半年线或年线"的A股（按市值分大小市值两组）和港股， 识别均线突破形态的个股，辅助中期趋势入场。

**Inputs**:
- {'windows': [120, 250]}
- {'up_intervals': 60}
- {'over_mode': 'or'}
- {'turnover_threshold': '100000000（港股）'}

**Components**:
- VolumeUpMaFactor
- get_top_stocks (return_type="small_vol_up" / "big_vol_up")
- report_targets
- inform
- EmailInformer

**Parameters**:
```
{'adjust_type': 'AdjustType.hfq', 'start_timestamp': '2021-01-01', 'filter_by_volume': False}
```

**Validation**:
```
邮件包含"放量突破(半)年线"标题，标的按大小市值分两封邮件。

```

## `KUC-RP-005`
**Source**: `examples/reports/__init__.py`

识别财务风险股票：营收/利润下滑、流动比率/速动比率低、 高应收+高存货+高商誉、应收账款超净利润一半， 用于规避高风险标的或做空筛选。

**Inputs**:
- {'the_date': '当前日期（默认）'}
- {'income_yoy': '-0.1 (同比跌幅阈值)'}
- {'profit_yoy': -0.1}
- {'entity_ids': 'null（全A）'}

**Components**:
- FinanceFactor
- BalanceSheet
- IncomeStatement
- risky_company (自定义函数)

**Parameters**:
```
{'current_ratio_min': 0.7, 'quick_ratio_min': 0.5, 'start_offset_days': 130}
```

**Validation**:
```
risky_company() 返回含高风险个股代码的列表，手工验证含已知财务暴雷股。

```

## `KUC-RS-001`
**Source**: `examples/research/dragon_and_tiger.py`

分析龙虎榜历史数据，识别过去一年（~400天）中胜率最高的游资席位（大玩家）， 并计算每个席位在不同持仓天数（3/5/10天）下的历史胜率， 为跟庄席位策略提供统计依据。

**Inputs**:
- {'provider': 'em'}
- {'start_timestamp': 'date_time_by_interval(end_timestamp, -400)'}
- {'end_timestamp': 'date_time_by_interval(current_date(), -60)'}
- {'intervals': [3, 5, 10]}

**Components**:
- DragonAndTiger
- get_big_players
- get_player_success_rate

**Validation**:
```
get_player_success_rate() 返回含席位名+多个持仓天数胜率的 DataFrame， 可见知名游资席位（如"国泰君安证券股份有限公司上海江苏路证券营业部"）。

```

## `KUC-RS-002`
**Source**: `examples/research/top_dragon_tiger.py`

对每月涨幅前30股票，追溯其月涨幅期间内龙虎榜记录， 统计哪些席位频繁参与月度强势股，揭示"聪明钱"机构行为模式。

**Inputs**:
- {'data_provider': 'em'}
- {'start_timestamp': '2021-01-01'}
- {'end_timestamp': '2022-01-01'}

**Components**:
- get_top_performance_by_month
- get_players
- DragonTigerFactor (继承 TechnicalFactor，叠加席位注释)

**Parameters**:
```
{'direction': 'in', 'top_count_per_month': 30}
```

**Validation**:
```
top_dragon_and_tiger() 返回合并后的 player_df， 按 entity_id+timestamp 双索引排序，可见重复出现的知名席位。

```

## `KUC-RS-003`
**Source**: `examples/research/top_tags.py`

统计每月涨幅前30股票的市值分布，验证"小市值效应"假设， 并记录每个月度强势股对应时点的市值及得分，为选股规则制定提供实证依据。

**Inputs**:
- {'data_provider': 'em'}
- {'start_timestamp': '2020-01-01'}
- {'end_timestamp': '2021-01-01'}

**Components**:
- get_top_performance_by_month
- Stock1dHfqKdata
- top_tags (自定义函数)

**Parameters**:
```
{'list_days': 250}
```

**Validation**:
```
top_tags() 返回含 {entity_id, timestamp, cap, score} 的记录列表， 分析结果验证"市值90%分布在100亿以下"的假设。

```

## `KUC-ML-001`
**Source**: `examples/ml/sgd.py`

用 SGD 分类器基于MA特征预测A股个股下期价格行为（涨/跌/震荡分类）， 结合标准化管道训练+预测，可视化预测结果与实际K线对比。

**Inputs**:
- {'data_provider': 'em'}
- {'entity_ids': ['stock_sz_000001']}
- {'label_method': 'behavior_cls'}

**Components**:
- MaStockMLMachine
- SGDClassifier (sklearn)
- StandardScaler
- make_pipeline

**Parameters**:
```
{'max_iter': 1000, 'tol': '1e-3'}
```

**Validation**:
```
machine.draw_result(entity_id="stock_sz_000001") 展示预测结果图； 预测准确率可通过 machine.predict() 返回的 DataFrame 评估。

```

## `KUC-ML-002`
**Source**: `examples/ml/sgd.py`

用 SGD 回归器基于MA特征直接预测A股个股下期收益率（连续值）， 与分类模式对比，评估线性模型的预测能力。

**Inputs**:
- {'data_provider': 'em'}
- {'entity_ids': ['stock_sz_000001']}
- {'label_method': 'raw'}

**Components**:
- MaStockMLMachine
- SGDRegressor (sklearn)
- StandardScaler
- make_pipeline

**Parameters**:
```
{'max_iter': 1000, 'tol': '1e-3'}
```

**Validation**:
```
machine.draw_result(entity_id="stock_sz_000001") 展示回归预测线； 预测误差通过 MSE/MAE 评估。

```

## `KUC-IN-001`
**Source**: `examples/intent/intent.py`

对比沪指与道琼斯指数自2000年起的相对表现（同基归一化）， 直观展示中美股市的长期相关性与分化，辅助宏观择时判断。

**Inputs**:
- {'entity_ids': ['index_sh_000001', 'indexus_us_SPX']}
- {'start_timestamp': '2000-01-01'}
- {'scale_value': 100}

**Components**:
- Index
- Indexus
- Index1dKdata
- Indexus1dKdata
- compare

**Validation**:
```
compare() 弹出含双轨叠加的折线图，Y轴为归一化值（基期=100）。

```

## `KUC-IN-002`
**Source**: `examples/intent/intent.py`

比较美债收益率（2年/5年）与道指走势的历史关系， 验证"高利率压制股市"假设，辅助美联储政策周期下的资产配置。

**Inputs**:
- {'entity_ids': ['country_galaxy_US', 'indexus_us_SPX']}
- {'start_timestamp': '1990-01-01'}

**Components**:
- TreasuryYield
- Indexus1dKdata
- compare

**Parameters**:
```
{'scale_value': None, 'schema_map_columns': {'TreasuryYield': ['yield_2', 'yield_5'], 'Indexus1dKdata': ['close']}}
```

**Validation**:
```
compare() 展示多轨折线图，可见利率与指数的反向关系。

```

## `KUC-IN-003`
**Source**: `examples/intent/intent.py`

对比江西铜业股票与沪铜期货走势（归一化）， 验证"资源股跟踪商品价格"假设，识别股价与商品价格的背离机会。

**Inputs**:
- {'entity_ids': ['stock_sh_600362', 'future_shfe_CU']}
- {'start_timestamp': '2005-01-01'}
- {'scale_value': 100}

**Components**:
- compare

**Validation**:
```
compare() 展示归一化双轨折线，可见铜业股与铜期货的高度相关走势。

```

## `KUC-IN-004`
**Source**: `examples/intent/intent.py`

比较铜、铝、螺纹钢三种工业金属的价格走势， 识别金属品种间的轮动规律与分化，为跨品种套利提供参考。

**Inputs**:
- {'entity_ids': ['future_shfe_CU', 'future_shfe_AL', 'future_shfe_RB']}
- {'start_timestamp': '2009-04-01'}
- {'scale_value': 100}

**Components**:
- compare

**Validation**:
```
compare() 展示三条归一化折线，可见品种间分化时段。

```

## `KUC-IN-005`
**Source**: `examples/intent/intent.py`

比较纳指/标普/美元指数三者走势（2015年后）， 研究"美元强弱对美股的压制效应"，辅助海外资产配置。

**Inputs**:
- {'entity_ids': ['indexus_us_NDX', 'indexus_us_SPX', 'indexus_us_UDI']}
- {'start_timestamp': '2015-01-01'}
- {'scale_value': 100}

**Components**:
- Indexus1dKdata
- compare

**Parameters**:
```
{'schema_map_columns': {'Indexus1dKdata': ['close']}}
```

**Validation**:
```
compare() 展示三轨折线，可分析纳指与美元指数的走势分化。

```

## `KUC-IN-006`
**Source**: `examples/intent/intent.py`

对比人民币兑美元汇率（USDCNY）与沪指走势， 研究汇率贬值对A股资金流向的影响，辅助外资流出风险判断。

**Inputs**:
- {'entity_ids': ['index_sh_000001', 'currency_forex_USDCNYC']}
- {'start_timestamp': '2005-01-01'}
- {'scale_value': 100}

**Components**:
- Currency1dKdata
- Index1dKdata
- compare

**Parameters**:
```
{'schema_map_columns': {'Currency1dKdata': ['close'], 'Index1dKdata': ['close']}}
```

**Validation**:
```
compare() 展示双轨折线，可见汇率与指数的阶段性反相关。

```

## `KUC-TR-001`
**Source**: `examples/trader/ma_trader.py`

最简单的MA均线交叉回测：5日线上穿10日线买入、下穿卖出， 验证双均线策略在单只/多只A股上的历史收益， 提供最基础的趋势跟踪策略 baseline。

**Inputs**:
- {'codes': ['000338']}
- {'level': 'IntervalLevel.LEVEL_1DAY'}
- {'start_timestamp': '2019-01-01'}
- {'end_timestamp': '2019-06-30'}
- {'windows': [5, 10]}

**Components**:
- CrossMaFactor
- MyMaTrader (继承 StockTrader)

**Parameters**:
```
{'need_persist': False, 'trader_name': '000338_ma_trader'}
```

**Validation**:
```
trader.run() 完成后，zvt 数据库中有 trader_name 对应的交易记录； trader.draw_result() 展示净值曲线。

```

## `KUC-TR-002`
**Source**: `examples/trader/ma_trader.py`

MACD多头市场过滤+MA均线交叉的组合策略回测：只在大趋势向上（BullFactor）时 持有多头仓位，降低熊市做多风险，验证加入趋势过滤的策略改进效果。

**Inputs**:
- {'codes': ['000338']}
- {'level': 'IntervalLevel.LEVEL_1DAY'}
- {'start_timestamp': '2019-01-01'}
- {'adjust_type': 'hfq'}

**Components**:
- BullFactor
- MyBullTrader (继承 StockTrader)

**Validation**:
```
trader.run() 完成，净值曲线较纯MA策略回撤更低。

```

## `KUC-TR-003`
**Source**: `examples/trader/macd_day_trader.py`

日线 MACD 金叉策略完整框架示例：演示如何在 StockTrader 中 覆盖止盈止损（on_profit_control）、开收盘钩子（on_trading_open/close）、 交易信号批处理（on_trading_signals）等生命周期方法。

**Inputs**:
- {'start_timestamp': '2019-01-01'}
- {'end_timestamp': '2020-01-01'}
- {'provider': 'joinquant'}
- {'level': 'IntervalLevel.LEVEL_1DAY'}

**Components**:
- GoldCrossFactor
- MacdDayTrader (继承 StockTrader)

**Parameters**:
```
{'start_offset_days': -50}
```

**Validation**:
```
trader.run() 不报错；各 hook 方法被正确调用（可在 override 中添加日志验证）。

```

## `KUC-TR-004`
**Source**: `examples/trader/macd_week_and_day_trader.py`

周线+日线双时间框架 MACD 策略：只有周线和日线同时金叉时才开多仓， 降低误信号，验证多周期共振策略的信号质量提升。

**Inputs**:
- {'start_timestamp': '2019-01-01'}
- {'end_timestamp': '2020-01-01'}
- {'provider': 'joinquant'}

**Components**:
- GoldCrossFactor (LEVEL_1WEEK)
- GoldCrossFactor (LEVEL_1DAY)
- MultipleLevelTrader (继承 StockTrader)

**Parameters**:
```
{'on_targets_selected_from_levels': 'override 可自定义多级别合并逻辑'}
```

**Validation**:
```
trader.run() 完成；相比纯日线策略，交易次数减少但胜率更高。

```

## `KUC-TR-005`
**Source**: `examples/trader/dragon_and_tiger_trader.py`

基于龙虎榜跟踪机构专用席位：当"机构专用"席位在某股票上榜时产生买入信号， 依此验证"跟机构席位"策略的历史有效性。

**Inputs**:
- {'start_timestamp': '2020-01-01'}
- {'end_timestamp': '2022-05-01'}
- {'provider': 'em'}

**Components**:
- DragonTigerFactor (继承 Factor，数据源为 DragonAndTiger)
- MyTrader (继承 StockTrader)

**Parameters**:
```
{'filter': 'DragonAndTiger.dep1 == "机构专用"'}
```

**Validation**:
```
trader.run() 完成，交易记录中开仓时间与龙虎榜机构上榜日期一致。

```

## `KUC-TR-006`
**Source**: `examples/trader/follow_ii_trader.py`

跟随公募基金持仓变化做多/平仓：当基金持仓比例季报新增超5%时买入， 减持超50%时卖出，验证"跟基金重仓变化"的交易逻辑在单只股票（茅台）上的效果。

**Inputs**:
- {'code': '600519'}
- {'start_timestamp': '2002-01-01'}
- {'end_timestamp': '2021-01-01'}
- {'adjust_type': 'AdjustType.qfq'}

**Components**:
- FollowIITrader (继承 StockTrader，override on_time)
- StockActorSummary
- Stock1dKdata

**Parameters**:
```
{'actor_type': 'ActorType.raised_fund', 'long_threshold': 0.05, 'short_threshold': -0.5, 'profit_threshold': None}
```

**Validation**:
```
trader.run() 完成；可视化净值曲线在2010-2021年茅台上涨期间应呈显著正收益。

```

## `KUC-TR-007`
**Source**: `examples/trader/keep_run_trader.py`

滚动40天区间多因子组合策略：每40天重新计算股票池（成交量前30%+机构重仓前30%的交集）， 结合周线牛市判断+日线金叉入场，验证动态股票池筛选对组合策略的增益。

**Inputs**:
- {'start': '2019-01-01'}
- {'end': '2021-01-01'}
- {'interval': 40}
- {'vol_pct': 0.3}
- {'ii_pct': 0.3}

**Components**:
- MultipleLevelTrader (BullFactor LEVEL_1WEEK + GoldCrossFactor LEVEL_1DAY)
- get_top_volume_entities
- get_top_fund_holding_stocks
- split_time_interval
- clear_trader

**Parameters**:
```
{'keep_history': True, 'draw_result': False, 'rich_mode': False, 'trader_name': 'keep_run_trader'}
```

**Validation**:
```
所有时间段遍历完成后，zvt 数据库中有完整的 keep_run_trader 交易历史记录。

```

## `KUC-QU-001`
**Source**: `examples/query_snippet.py`

演示 StockTags 的 JSON 字段查询能力：通过 SQLite JSON_EXTRACT 函数 按子标签（如"低空经济"）精确筛选A股，解决标签多值存储下的高效检索问题。

**Inputs**:
- {'sub_tag': '低空经济'}

**Components**:
- StockTags
- func.json_extract (SQLAlchemy)

**Parameters**:
```
{'json_path': '$."{tag}"'}
```

**Validation**:
```
query_json() 返回含对应子标签的 DataFrame，行数与东方财富"低空经济"板块成份数接近。

```

## `KUC-QU-002`
**Source**: `examples/query_snippet.py`

快速获取当前标签库的覆盖缺口：找出尚无标签的在市A股代码列表， 为标签体系维护提供自动差异发现。

**Inputs**:
- {'provider': 'em'}
- {'ignore_delist': True}
- {'ignore_st': True}

**Components**:
- StockTags
- get_entity_ids_by_filter

**Validation**:
```
get_stocks_without_tag() 返回非空列表，代码均可在东方财富查到且无标签记录。

```

## `KUC-QU-003`
**Source**: `examples/tag_utils.py`

为一批A股个股自动生成默认行业标签（通过行业板块->主题映射表）， 解决大批量新股入库时缺少标签的冷启动问题。

**Inputs**:
- {'codes': '无标签股票代码列表'}
- {'provider': 'em'}

**Components**:
- BlockStock
- Block
- industry_to_tag (行业->主题映射函数)
- build_default_tags

**Parameters**:
```
{'block_category': 'industry'}
```

**Validation**:
```
build_default_tags(codes) 返回含 code/name/tag/reason 字段的字典列表， 无行业信息的股票自动打印告警。

```

## `KUC-QU-004`
**Source**: `examples/utils.py`

按热词配置（hot.json）对选出的个股用新闻标题分组， 归类到主题（如"华为"、"新能源"等），辅助人工快速了解选股的热门主题背景。

**Inputs**:
- {'entities': '已选个股列表'}
- {'hot_words_config': 'hot.json（主题:关键词列表）'}
- {'days_ago': 60}
- {'threshold': 3}

**Components**:
- StockNews
- group_stocks_by_topic
- msg_group_stocks_by_topic

**Parameters**:
```
{'entity_ids': '自动从 entities 提取'}
```

**Validation**:
```
msg_group_stocks_by_topic() 返回按主题分组的字符串， 包含"^^^^^^ 主题(N) ^^^^^^"格式。

```

## `KUC-QU-005`
**Source**: `examples/migration.py`

演示如何用 Pydantic + SQLAlchemy Mixin 向 zvt 注册自定义数据 schema， 支持业务团队扩展本地数据库存储自定义实体和 JSON 字段，无需修改框架核心。

**Inputs**:
- {'custom_schema': 'User (含 added_col: String, json_col: JSON)'}
- {'db_name': 'test'}
- {'providers': ['zvt']}

**Components**:
- Mixin
- register_schema
- get_db_session
- UserModel (Pydantic BaseModel)

**Parameters**:
```
{'declarative_base': 'ZvtInfoBase'}
```

**Validation**:
```
UserModel.validate(user) 不报错，说明 SQLAlchemy ORM 对象可无缝转换为 Pydantic 模型。

```
