# Anti-Patterns (Cross-Project)

Total: **47**

## qlib (12)

### `AP-QLIB-1930` — 回测结果与模型无关——共享 dataset 对象导致预测值被首次模型覆盖 <sub>(high)</sub>

Qlib 中多个模型复用同一个已 fit 的 DatasetH 实例时，dataset 内部的标准化 参数（fit_start_time/fit_end_time 决定的归一化统计量）在第一次 fit 后固化。 切换模型但不重新初始化 dataset，导致所有模型实际使用同一套预测信号。表现为 无论换 LightGBM/XGBoost/DNN，回测净值曲线完全一致。这是最危险的"实验看起来 在跑，但结论全部无效"反模式。

Source: https://github.com/microsoft/qlib/issues/1930

### `AP-QLIB-2090` — fit_start_time 与 train segment 双重配置引发隐式数据泄露 <sub>(high)</sub>

Qlib DatasetH 有两个"训练数据范围"：handler 的 fit_start_time/fit_end_time （决定归一化器拟合范围）和 segments.train（决定模型训练范围）。常见错误是 让 fit_end_time 覆盖 valid/test 段，使归一化统计量（均值、标准差）包含了 未来数据，造成前向偏差（look-ahead bias）。两者独立配置但语义耦合，文档 未明确说明 fit_end_time 必须 <= train_end。

Source: https://github.com/microsoft/qlib/issues/2090

### `AP-QLIB-2036` — MACD 因子公式文档错误——DEA 被多除一次 CLOSE 导致量纲不一致 <sub>(high)</sub>

Qlib 官方文档中的 Alpha 公式示例将 MACD 的 DEA 定义为 EMA(DIF, 9) / CLOSE， 但 DIF 已经是无量纲（除过 CLOSE 的），再次除以 CLOSE 导致 DEA 量纲为 1/price。 基于此文档公式构建的 MACD 因子在截面标准化后与正确公式差异显著，IC 下降。 此类文档层面的公式错误会被大量用户直接照搬入生产因子库。

Source: https://github.com/microsoft/qlib/issues/2036

### `AP-QLIB-2184` — 自定义 A 股数据导入前未按约定填充停牌日 NaN，引发下游因子噪声 <sub>(high)</sub>

Qlib 约定停牌日 open/close/high/low/volume/factor 字段均应填 NaN，以便框架 在因子计算时识别并跳过。用户自建 A 股数据集时若将停牌日保留为上一日价格 （常见于从东财/Wind 直接导出的数据），会导致停牌期间的价格动量因子出现 "假信号"（价格不变但因子非零）。Qlib 不校验此约定，错误静默流入训练数据。

Source: https://github.com/microsoft/qlib/issues/2184

### `AP-QLIB-1892` — PIT（Point-In-Time）财务数据收集器依赖外部股票列表接口，全量 A 股获取不完整 <sub>(high)</sub>

Qlib 的 PIT 数据收集器（财务数据时间点快照）在初始化时调用 get_hs_stock_symbols() 获取沪深股票列表。该函数依赖东财 API，经常仅返回 部分列表而非全量 5000+ 股票，且函数在获取不完整时直接 raise ValueError。 用户若按文档步骤操作，财务数据集将只覆盖部分股票，基于 PIT 财务因子的回测 存在严重生存者偏差（未被采集的股票被隐式排除）。

Source: https://github.com/microsoft/qlib/issues/1892

### `AP-QLIB-2097` — 全市场 instrument="all" 在 32GB 内存机器上 OOM，但 CSI300 正常 <sub>(medium)</sub>

Qlib 在加载 Alpha158 特征时会将指定 universe 的全部特征矩阵一次性载入内存。 使用 instrument="csi300"（300 股）与 instrument="all"（5000+ 股）的内存占用 差约 16 倍。32GB 机器跑全市场时在 init_instance_by_config 阶段直接 OOM， 错误信息不提示内存问题。用户容易误以为是配置错误，实际上需要分批加载或 使用流式特征计算。

Source: https://github.com/microsoft/qlib/issues/2097

### `AP-QLIB-1974` — data_collector 即使指定 --region US 仍调用东财 A 股接口获取股票列表 <sub>(medium)</sub>

Qlib Yahoo 数据收集器在 download_data 时无论 --region 参数为何，均调用 东财 API（_get_eastmoney）获取完整股票列表作为基底，再用 Yahoo Finance 补充数据。在国际网络环境下东财接口不可达，导致即便指定 US 区域也必须科学 上网。这一隐式依赖从未在文档中说明，是 A 股数据基础设施默认全局的典型 设计陷阱。

Source: https://github.com/microsoft/qlib/issues/1974

### `AP-QLIB-1984` — LightGBM 模型标签维度校验逻辑永远不触发导致多标签训练静默失败 <sub>(medium)</sub>

Qlib gbdt.py 中用 y.values.ndim == 2 判断是否为多标签，但从 DataFrame 取出的 Series 的 ndim 永远为 1，条件永远为 False，因此多标签训练不会走 squeeze 分支，而是直接进入 LightGBM 训练并在更深处抛出语义不明的错误。 用户尝试自定义多标签任务时无法从错误信息定位到此根因。

Source: https://github.com/microsoft/qlib/issues/1984

### `AP-QLIB-1915` — 自定义 CSV 数据 dump_bin 后 DataHandler 报 Length mismatch，D.features 却正常 <sub>(high)</sub>

Qlib 存在两套数据访问路径：D.features（直接读 binary）和 DataHandler/DataHandlerLP （带 processor pipeline）。自定义 A 股 CSV 数据在 dump_bin 时若字段顺序 或 symbol 格式（如 600000.SH vs SH600000）与 Qlib 约定不符，DataHandler 的 processor 在 align/reindex 时触发 Length mismatch，而 D.features 因不 经过 processor 而成功。这一"两套路径行为不一致"让用户误以为数据已正确导入。

Source: https://github.com/microsoft/qlib/issues/1915

### `AP-QLIB-1949` — Colab/Linux 多进程后端与 Qlib ParallelExt 冲突导致 DataHandler 完全不可用 <sub>(medium)</sub>

Qlib 在非 fork 环境（Windows 或 Google Colab）中，DataHandler 使用 joblib 并行加载特征时，ParallelExt 初始化时访问 _backend_args 属性失败（AttributeError）。 根因是 joblib 1.5+ 移除了该内部属性，Qlib 的兼容层未更新。表现为 D.features 调用抛出多层嵌套异常，用户无法从错误栈判断是并行后端问题还是数据问题。

Source: https://github.com/microsoft/qlib/issues/1949

### `AP-QLIB-1930` — 回测结果与模型无关——共享 dataset 对象导致预测值被首次模型覆盖 <sub>(high)</sub>

Qlib 中多个模型复用同一个已 fit 的 DatasetH 实例时，dataset 内部的标准化 参数（fit_start_time/fit_end_time 决定的归一化统计量）在第一次 fit 后固化。 切换模型但不重新初始化 dataset，导致所有模型实际使用同一套预测信号。表现为 无论换 LightGBM/XGBoost/DNN，回测净值曲线完全一致。这是最危险的"实验看起来 在跑，但结论全部无效"反模式。

Source: https://github.com/microsoft/qlib/issues/1930

### `AP-QLIB-2090` — fit_start_time 与 train segment 双重配置引发隐式数据泄露 <sub>(high)</sub>

Qlib DatasetH 有两个"训练数据范围"：handler 的 fit_start_time/fit_end_time （决定归一化器拟合范围）和 segments.train（决定模型训练范围）。常见错误是 让 fit_end_time 覆盖 valid/test 段，使归一化统计量（均值、标准差）包含了 未来数据，造成前向偏差（look-ahead bias）。两者独立配置但语义耦合，文档 未明确说明 fit_end_time 必须 <= train_end。

Source: https://github.com/microsoft/qlib/issues/2090

## vnpy (11)

### `AP-VNPY-3691` — K 线生成器首根 K 线时间戳不对齐，导致第一个周期信号错误 <sub>(high)</sub>

vnpy BarGenerator 在合成 N 分钟 K 线时，第一根推送的 K 线时间戳为"当前 tick 所在分钟"而非"完整 N 分钟周期结束时间"。具体表现：09:59 的 tick 会 触发一根不完整的 5 分钟 K 线推送（本应等到 10:04 才推送）。策略若在 on_bar 中直接用 datetime.minute % 5 过滤，第一根 K 线恰好通过，但包含的 数据不足一个完整周期，用于信号计算会产生错误的开仓信号。

Source: https://github.com/vnpy/vnpy/issues/3691

### `AP-VNPY-3705` — CTP 委托价格超限被系统自动撤单，vnpy 无日志输出形同"无声失败" <sub>(high)</sub>

A 股/期货涨跌停价格限制下，超限委托在 CTP 端会被直接撤单（OnRtnOrder statusMsg="50:已撤单被拒绝SHFE:价格跌破跌停板"），而非触发 OnRspOrderInsert 拒单回调。vnpy 的 CTP Gateway 仅在 onRspOrderInsert 时输出拒单日志，对 OnRtnOrder 的撤单原因不做解析区分。策略开发者若依赖日志监控委托失败， 超限委托将完全静默消失，导致实盘仓位与预期严重偏离。

Source: https://github.com/vnpy/vnpy/issues/3705

### `AP-VNPY-3669` — Alpha 模块历史数据增量保存时新旧 DataFrame schema 不兼容导致 SchemaError <sub>(medium)</sub>

vnpy Alpha 模块在保存 K 线数据到 Parquet 文件时，将新下载数据（可能含 Float64 列）与已存文件（历史 Int64 列）直接 polars.concat。polars 强类型 不允许隐式类型提升，抛出 SchemaError。根因是不同数据源/版本返回的字段类型 不一致（如 volume 在部分行情源为整数，在另一些为浮点），且 concat 前无 schema 对齐步骤。影响所有使用 vnpy alpha 进行回测的历史数据构建流程。

Source: https://github.com/vnpy/vnpy/issues/3669

### `AP-VNPY-3707` — CTP Gateway 登出时 C++ 空指针崩溃，重连/切换账号导致进程终止 <sub>(high)</sub>

vnpy_ctp 在调用 close() 登出时，C++ 端 MdApi/TdApi 未检查空指针，有较大概率 触发段错误导致整个 Python 进程崩溃。影响场景：策略测试时频繁登录/登出、切换 模拟与实盘账号、服务器关机重连等。崩溃不产生 Python 异常，无法被 try/except 捕获，是实盘场景中最危险的稳定性陷阱之一。

Source: https://github.com/vnpy/vnpy/issues/3707

### `AP-VNPY-3685` — 价差交易模块 run_backtesting() 在 Jupyter 环境下静默报错，结果不可信 <sub>(high)</sub>

vnpy 4.10 价差交易（SpreadTrading）模块的 run_backtesting() 在 Jupyter 环境下存在事件循环冲突（asyncio already running），导致回测引擎部分逻辑 不执行但不抛异常，返回看似正常的回测统计数据。同样代码在命令行 Python 中无此问题。vnpy 4.x 将部分 IO 改为 async 但 Jupyter 的事件循环与之不兼容， 是"回测结果看起来正确但实际不完整"的隐蔽陷阱。

Source: https://github.com/vnpy/vnpy/issues/3685

### `AP-VNPY-3700` — 安装脚本不使用 venv 导致全局 numpy 版本被降级破坏其他依赖 <sub>(medium)</sub>

vnpy install.bat 直接在系统/conda base 环境安装，会强制降级 numpy 到 <2.0 以满足 vnpy 依赖，破坏依赖 numpy 2.x 的其他量化工具（如 scipy、pytorch 新版）。 没有 requirements.txt，依赖边界不透明。在多工具共存的量化研究环境中， vnpy 的安装脚本是"全局环境污染"的常见根源。

Source: https://github.com/vnpy/vnpy/issues/3700

### `AP-VNPY-3715` — loguru 格式化字符串中含花括号的 order 对象触发 KeyError 导致日志系统崩溃 <sub>(high)</sub>

vnpy engine.py 使用 f-string 将 order.__dict__ 直接格式化后传给 loguru 的 write_log。当 order 的字段名（如 gateway_name）恰好匹配 loguru 格式化占位符时， loguru 将其解析为模板变量并抛出 KeyError，导致整个日志线程崩溃。实盘中 日志系统崩溃意味着后续所有委托/成交记录丢失，是生产环境的高危陷阱。

Source: https://github.com/vnpy/vnpy/issues/3715

### `AP-VNPY-3691` — K 线生成器首根 K 线时间戳不对齐，导致第一个周期信号错误 <sub>(high)</sub>

vnpy BarGenerator 在合成 N 分钟 K 线时，第一根推送的 K 线时间戳为"当前 tick 所在分钟"而非"完整 N 分钟周期结束时间"。具体表现：09:59 的 tick 会 触发一根不完整的 5 分钟 K 线推送（本应等到 10:04 才推送）。策略若在 on_bar 中直接用 datetime.minute % 5 过滤，第一根 K 线恰好通过，但包含的 数据不足一个完整周期，用于信号计算会产生错误的开仓信号。

Source: https://github.com/vnpy/vnpy/issues/3691

### `AP-VNPY-3669` — Alpha 模块历史数据增量保存时新旧 DataFrame schema 不兼容导致 SchemaError <sub>(medium)</sub>

vnpy Alpha 模块在保存 K 线数据到 Parquet 文件时，将新下载数据（可能含 Float64 列）与已存文件（历史 Int64 列）直接 polars.concat。polars 强类型 不允许隐式类型提升，抛出 SchemaError。根因是不同数据源/版本返回的字段类型 不一致（如 volume 在部分行情源为整数，在另一些为浮点），且 concat 前无 schema 对齐步骤。影响所有使用 vnpy alpha 进行回测的历史数据构建流程。

Source: https://github.com/vnpy/vnpy/issues/3669

### `AP-VNPY-3685` — 价差交易模块 run_backtesting() 在 Jupyter 环境下静默报错，结果不可信 <sub>(high)</sub>

vnpy 4.10 价差交易（SpreadTrading）模块的 run_backtesting() 在 Jupyter 环境下存在事件循环冲突（asyncio already running），导致回测引擎部分逻辑 不执行但不抛异常，返回看似正常的回测统计数据。同样代码在命令行 Python 中无此问题。vnpy 4.x 将部分 IO 改为 async 但 Jupyter 的事件循环与之不兼容， 是"回测结果看起来正确但实际不完整"的隐蔽陷阱。

Source: https://github.com/vnpy/vnpy/issues/3685

### `AP-VNPY-3700` — 安装脚本不使用 venv 导致全局 numpy 版本被降级破坏其他依赖 <sub>(medium)</sub>

vnpy install.bat 直接在系统/conda base 环境安装，会强制降级 numpy 到 <2.0 以满足 vnpy 依赖，破坏依赖 numpy 2.x 的其他量化工具（如 scipy、pytorch 新版）。 没有 requirements.txt，依赖边界不透明。在多工具共存的量化研究环境中， vnpy 的安装脚本是"全局环境污染"的常见根源。

Source: https://github.com/vnpy/vnpy/issues/3700

## zipline (13)

### `AP-ZIPLINE-138` — 回测价格为未复权价，教程图表误导用户误判策略收益 <sub>(high)</sub>

Zipline 教程使用 AAPL 股价图做演示，但 bundle 中存储的是未复权价格（raw price）， 而非经过拆股/分红调整的复权价。图表显示的历史价格与市场实际价约差 4 倍（Apple 历次拆股累计因子），用户误将"价格翻 4 倍"当作策略收益。A 股场景更严重： 除权前后价格跳变会在未复权数据中形成巨大"信号"，吸引技术指标在除权日产生 虚假突破信号。

Source: https://github.com/stefan-jansen/zipline-reloaded/issues/138

### `AP-ZIPLINE-235` — 默认以当根 K 线收盘价成交，低估实盘滑点，策略回测收益虚高 <sub>(high)</sub>

Zipline 默认滑点模型在当根 K 线触发信号后，以同根 K 线收盘价成交（current bar close fill）。实盘中信号只能在下一根 K 线的开盘价附近成交（T+1 order execution）。以 A 股日线为例，用收盘价回测比用次日开盘价成交平均高估日收益 约 0.1-0.3%，年化差距可超 30%。需显式配置 slippage model 为 VolumeShareSlippage 或 FixedSlippage 并设合理 volume_limit。

Source: https://github.com/stefan-jansen/zipline-reloaded/issues/235

### `AP-ZIPLINE-190` — 日历 start_session 设为非交易日触发 DateOutOfBounds，无提示如何修正 <sub>(medium)</sub>

Zipline 在注册 bundle 或运行算法时，若 start_session 参数恰好是非交易日 （如 1998-01-01 元旦），Calendar 校验抛出 DateOutOfBounds（"cannot be earlier than the first session"）。错误信息仅显示交易日历起始日，不提示"请改为第一个 交易日"。A 股场景：使用 SSE/SZSE 日历时，若 start_date 恰好是春节前最后 一天次日（节假日），会触发同类错误，调试成本极高。

Source: https://github.com/stefan-jansen/zipline-reloaded/issues/190

### `AP-ZIPLINE-182` — CSV bundle 中股票 symbol 列为空/None 时 SQLite 约束失败，全量导入静默中断 <sub>(medium)</sub>

Zipline csvdir bundle 在 ingest 时会将所有 CSV 文件名解析为 symbol，写入 equity_symbol_mappings 表。若 CSV 文件名不符合 Zipline 规范（如含中文、 带交易所后缀 .SH），symbol 字段被解析为空字符串或 None，触发 sqlite3.IntegrityError: NOT NULL constraint failed。错误发生在 ingest 尾声， 前面已写入的数据被回滚，整个 bundle 不可用。常见于 A 股数据（000001.SZ.csv 格式），需预处理文件名去掉后缀。

Source: https://github.com/stefan-jansen/zipline-reloaded/issues/182

### `AP-ZIPLINE-181` — asset db 过期后 Pipeline 报"no assets traded"，误导用户排查数据范围 <sub>(high)</sub>

Zipline 的 asset database（SQLite）记录每只股票的 start/end 交易日期。若 使用了旧版 Quandl/自建 bundle 且未重新 ingest，在回测新日期范围时 Pipeline 抛出 "Failed to find any assets with country_code 'US' that traded between [dates]"。A 股场景：重新下载行情后若只更新价格数据而未重建 asset db，退市/ 新上市股票的日期范围不更新，Pipeline 过滤会悄悄排除这些股票，产生生存者偏差。

Source: https://github.com/stefan-jansen/zipline-reloaded/issues/181

### `AP-ZIPLINE-285` — week_start()/week_end() 在自定义日历（非美股）下静默失效 <sub>(medium)</sub>

Zipline schedule_function 的 date_rules.week_start() 和 date_rules.week_end() 依赖交易日历的周首/周末判断逻辑，但在非美股日历（如 ASX、SSE）中，该逻辑 与 NYSE 日历的偏移计算不兼容，导致 schedule 永远不触发或在错误的日期触发。 A 股场景：使用 SSE 日历时，含春节等连续长假的周，week_start 可能跳过整个 假期周而不调仓，但用户无法从日志发现未触发的调度。

Source: https://github.com/stefan-jansen/zipline-reloaded/issues/285

### `AP-ZIPLINE-240` — 回测日期时区必须为 UTC，传入 naive datetime 引发深层 AssertionError <sub>(medium)</sub>

Zipline 内部强制要求所有时间戳为 UTC aware datetime。当用户传入 naive datetime （无时区信息，如 pd.Timestamp('2020-01-01')）时，不在入口处报错，而是在 算法执行深处触发 AssertionError: Algorithm should have a utc datetime，栈深 难以定位。A 股开发者从本地 CST 时间导入数据时极易触发此陷阱，需在 bundle 注册时显式 tz_localize('UTC')。

Source: https://github.com/stefan-jansen/zipline-reloaded/issues/240

### `AP-ZIPLINE-138` — 回测价格为未复权价，教程图表误导用户误判策略收益 <sub>(high)</sub>

Zipline 教程使用 AAPL 股价图做演示，但 bundle 中存储的是未复权价格（raw price）， 而非经过拆股/分红调整的复权价。图表显示的历史价格与市场实际价约差 4 倍（Apple 历次拆股累计因子），用户误将"价格翻 4 倍"当作策略收益。A 股场景更严重： 除权前后价格跳变会在未复权数据中形成巨大"信号"，吸引技术指标在除权日产生 虚假突破信号。

Source: https://github.com/stefan-jansen/zipline-reloaded/issues/138

### `AP-ZIPLINE-235` — 默认以当根 K 线收盘价成交，低估实盘滑点，策略回测收益虚高 <sub>(high)</sub>

Zipline 默认滑点模型在当根 K 线触发信号后，以同根 K 线收盘价成交（current bar close fill）。实盘中信号只能在下一根 K 线的开盘价附近成交（T+1 order execution）。以 A 股日线为例，用收盘价回测比用次日开盘价成交平均高估日收益 约 0.1-0.3%，年化差距可超 30%。需显式配置 slippage model 为 VolumeShareSlippage 或 FixedSlippage 并设合理 volume_limit。

Source: https://github.com/stefan-jansen/zipline-reloaded/issues/235

### `AP-ZIPLINE-190` — 日历 start_session 设为非交易日触发 DateOutOfBounds，无提示如何修正 <sub>(medium)</sub>

Zipline 在注册 bundle 或运行算法时，若 start_session 参数恰好是非交易日 （如 1998-01-01 元旦），Calendar 校验抛出 DateOutOfBounds（"cannot be earlier than the first session"）。错误信息仅显示交易日历起始日，不提示"请改为第一个 交易日"。A 股场景：使用 SSE/SZSE 日历时，若 start_date 恰好是春节前最后 一天次日（节假日），会触发同类错误，调试成本极高。

Source: https://github.com/stefan-jansen/zipline-reloaded/issues/190

### `AP-ZIPLINE-181` — asset db 过期后 Pipeline 报"no assets traded"，误导用户排查数据范围 <sub>(high)</sub>

Zipline 的 asset database（SQLite）记录每只股票的 start/end 交易日期。若 使用了旧版 Quandl/自建 bundle 且未重新 ingest，在回测新日期范围时 Pipeline 抛出 "Failed to find any assets with country_code 'US' that traded between [dates]"。A 股场景：重新下载行情后若只更新价格数据而未重建 asset db，退市/ 新上市股票的日期范围不更新，Pipeline 过滤会悄悄排除这些股票，产生生存者偏差。

Source: https://github.com/stefan-jansen/zipline-reloaded/issues/181

### `AP-ZIPLINE-285` — week_start()/week_end() 在自定义日历（非美股）下静默失效 <sub>(medium)</sub>

Zipline schedule_function 的 date_rules.week_start() 和 date_rules.week_end() 依赖交易日历的周首/周末判断逻辑，但在非美股日历（如 ASX、SSE）中，该逻辑 与 NYSE 日历的偏移计算不兼容，导致 schedule 永远不触发或在错误的日期触发。 A 股场景：使用 SSE 日历时，含春节等连续长假的周，week_start 可能跳过整个 假期周而不调仓，但用户无法从日志发现未触发的调度。

Source: https://github.com/stefan-jansen/zipline-reloaded/issues/285

### `AP-ZIPLINE-240` — 回测日期时区必须为 UTC，传入 naive datetime 引发深层 AssertionError <sub>(medium)</sub>

Zipline 内部强制要求所有时间戳为 UTC aware datetime。当用户传入 naive datetime （无时区信息，如 pd.Timestamp('2020-01-01')）时，不在入口处报错，而是在 算法执行深处触发 AssertionError: Algorithm should have a utc datetime，栈深 难以定位。A 股开发者从本地 CST 时间导入数据时极易触发此陷阱，需在 bundle 注册时显式 tz_localize('UTC')。

Source: https://github.com/stefan-jansen/zipline-reloaded/issues/240

## zvt (11)

### `AP-ZVT-183` — 除权因子为 inf/NaN 时直接参与乘法导致复权静默失败 <sub>(high)</sub>

ZVT 在计算前复权因子时以 new/old 价格比计算 qfq_factor。当 old==0（新股首日 或数据缺失）时因子为 inf；当 kdata.open 本身为 None（停牌日未填充）时乘法 抛出 TypeError。结果：整个 entity 的复权计算中断，后续 K 线全部丢失，但主 流程只 log ERROR 不中断，用户往往不知道已有大量股票数据损坏。

Source: https://github.com/zvtvz/zvt/issues/183

### `AP-ZVT-179` — 第三方数据接口超限后异常被吞噬，数据静默缺失 <sub>(high)</sub>

ZVT 使用聚宽 jqdatasdk 批量拉取全市场 K 线时（4000+ 股票），触发聚宽每日 最大查询条数限制（错误：已超过每日最大查询数量）。ZVT 捕获异常后继续执行下一 entity，导致超限后所有股票的当日数据均静默缺失。回测若使用该残缺数据库，因 子计算结果将产生系统性偏差，且无告警。

Source: https://github.com/zvtvz/zvt/issues/179

### `AP-ZVT-200` — Token 失效后数据查询返回空 DataFrame 而非报错 <sub>(high)</sub>

当聚宽/东财 token 过期时，ZVT 的 record_data 不抛异常，而是将 API 返回的 错误信息（如"error: token无效"）当作 DataFrame 列名解析，得到 0 行空表。 后续更新逻辑认为"无新数据"而跳过，造成数据库长期停止更新却无任何错误日志。 用户直到回测结果异常才发现数据已过期数月。

Source: https://github.com/zvtvz/zvt/issues/200

### `AP-ZVT-161` — 全市场 SQLite 批量因子计算触发 too many SQL variables 错误 <sub>(medium)</sub>

ZVT 在计算 VolumeUpMaFactor 等多股因子时，将所有 entity_id 拼入单条 SQL 的 IN 子句。当 A 股全市场（5000+ 股）一次性查询时，触发 SQLite 默认限制 SQLITE_MAX_VARIABLE_NUMBER=999。调大 max_allowed_packet（MySQL 参数）无效， 根因是 SQLite 变量数上限。正确解法是分批查询，但 ZVT 早期版本未处理此边界。

Source: https://github.com/zvtvz/zvt/issues/161

### `AP-ZVT-129` — 使用通配符导入隐藏 API 版本变更，AdjustType 等枚举莫名消失 <sub>(medium)</sub>

ZVT 文档示例使用 `from zvt import *` 导入所有符号。当 ZVT 版本升级重构 枚举（如将 AdjustType 移入子模块）后，通配符导入不再包含该符号，触发 AttributeError。使用者误以为是安装问题，实际是版本间 API breaking change 未在 CHANGELOG 中标注，且通配符导入掩盖了具体来源。应显式 import 枚举类。

Source: https://github.com/zvtvz/zvt/issues/129

### `AP-ZVT-187` — 回测引擎未在数据层空结果时提前终止，导致空指针级联崩溃 <sub>(medium)</sub>

ZVT Trader 在 load_data 完成后检查数据为空时，不提前退出，而是将空 DataFrame 传入 selector 计算，触发后续 NoneType 操作链式崩溃。错误栈深且难以定位根因， 用户误以为是策略逻辑问题。根因是数据时间窗口配置错误（start/end 不在数据 库覆盖范围内）但无有效校验。

Source: https://github.com/zvtvz/zvt/issues/187

### `AP-ZVT-184` — 样例历史数据替换后 provider 目录不匹配导致更新报错 <sub>(low)</sub>

ZVT 提供了可下载的历史快照数据库，但文档未说明必须放置于特定 zvt_home 子目录 下且与 provider 名称对应。用户将数据放错目录后执行 record_data 时，框架 发现本地库为空，触发从头全量拉取，再次遭遇 API 额度或权限错误。数据库路径 与 provider 的隐式绑定是常见理解盲区。

Source: https://github.com/zvtvz/zvt/issues/184

### `AP-ZVT-183B` — HFQ（后复权）与 QFQ（前复权）K 线表使用错误导致因子计算漂移 <sub>(high)</sub>

ZVT 提供 Stock1dKdata（不复权）、Stock1dHfqKdata（后复权）、Stock1dQfqKdata （前复权）三张独立表。用户在计算价格动量/均线因子时混用两张表（如用不复权 做均线，用后复权做收益率），导致除权日前后因子值产生跳变。ZVT 不做跨表 复权类型一致性校验，混用静默通过。

Source: https://github.com/zvtvz/zvt/issues/183

### `AP-ZVT-183` — 除权因子为 inf/NaN 时直接参与乘法导致复权静默失败 <sub>(high)</sub>

ZVT 在计算前复权因子时以 new/old 价格比计算 qfq_factor。当 old==0（新股首日 或数据缺失）时因子为 inf；当 kdata.open 本身为 None（停牌日未填充）时乘法 抛出 TypeError。结果：整个 entity 的复权计算中断，后续 K 线全部丢失，但主 流程只 log ERROR 不中断，用户往往不知道已有大量股票数据损坏。

Source: https://github.com/zvtvz/zvt/issues/183

### `AP-ZVT-187` — 回测引擎未在数据层空结果时提前终止，导致空指针级联崩溃 <sub>(medium)</sub>

ZVT Trader 在 load_data 完成后检查数据为空时，不提前退出，而是将空 DataFrame 传入 selector 计算，触发后续 NoneType 操作链式崩溃。错误栈深且难以定位根因， 用户误以为是策略逻辑问题。根因是数据时间窗口配置错误（start/end 不在数据 库覆盖范围内）但无有效校验。

Source: https://github.com/zvtvz/zvt/issues/187

### `AP-ZVT-183B` — HFQ（后复权）与 QFQ（前复权）K 线表使用错误导致因子计算漂移 <sub>(high)</sub>

ZVT 提供 Stock1dKdata（不复权）、Stock1dHfqKdata（后复权）、Stock1dQfqKdata （前复权）三张独立表。用户在计算价格动量/均线因子时混用两张表（如用不复权 做均线，用后复权做收益率），导致除权日前后因子值产生跳变。ZVT 不做跨表 复权类型一致性校验，混用静默通过。

Source: https://github.com/zvtvz/zvt/issues/183
