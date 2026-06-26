# DolphinDB 量化金融技能 v1.1.3

## 🚨 强制流程：使用前必须加载环境

**无论在何种场景下调用此技能（单独运行或被引用），必须先执行环境检测：**

```bash
# 方法 1: 在技能目录内运行（推荐）
cd ~/.jvs/.openclaw/workspace/skills/<skill-name>
source ../dolphindb-skills/scripts/dolphin_wrapper.sh

# 方法 2: 在任何位置运行（推荐）
source ~/.jvs/.openclaw/workspace/skills/dolphindb-skills/scripts/dolphin_global.sh

# 方法 3: 手动检测
python3 ~/.jvs/.openclaw/workspace/skills/dolphindb-skills/scripts/init_dolphindb_env.py
```

**验证环境：**
```bash
$DOLPHINDB_PYTHON_BIN -c "import dolphindb; print(dolphindb.__version__)"

# 或使用包装器命令
dolphin_python -c "import dolphindb; print(dolphindb.__version__)"
```

**重要**: 详见 [dolphindb-skills/USAGE_GUIDE.md](../dolphindb-skills/USAGE_GUIDE.md)

---

## ⚠️ 前置依赖

**本技能依赖 `dolphindb-basic` 技能，请先安装：**
```bash
clawhub install dolphindb-basic
```

**运行前初始化需确保 Python 环境有 DolphinDB SDK，详细方法可参见 dolphindb-skills 技能。**

```bash
# 加载环境检测器（相对路径，技能安装后自动可用）
source ../dolphindb-skills/scripts/load_dolphindb_env.sh

# 查看环境信息
dolphin_env_info

# 验证 SDK 已安装
dolphin_python -c "import dolphindb; print('SDK 版本:', dolphindb.__version__)"
```

**统一调用接口：**
```bash
dolphin_python script.py    # 运行 Python 脚本
dolphin_pip install pkg     # 安装包
```

**重要：所有 DolphinDB 脚本在 Python 中的调用方式**

```python
import dolphindb as ddb

# 1. 建立连接
s = ddb.session()
s.connect(host="localhost", port=8848, userid="admin", password="123456")

# 2. 执行 DolphinDB 脚本（所有数据库操作都通过 s.run()）
result = s.run('''
    // DolphinDB 脚本
    use mytt
    select 
        sym,
        RSI(close, 24) as rsi,
        MA(close, 5) as ma5
    from loadTable("dfs://bars_db.bars_minute")
    context by sym
''')

# 3. 转换为 pandas DataFrame（可选）
df = result.toDF()

# 4. 关闭连接
s.close()
```

---

## 描述
提供基于 DolphinDB 的量化金融场景解决方案，包括因子计算、策略回测、行情处理、绩效归因等金融专业能力。

## 触发条件
当用户提到以下关键词时触发此技能：
- "量化因子"、"因子计算"、"多因子模型"
- "策略回测"、"backtest"、"回测引擎"
- "K 线合成"、"OHLC"、"行情数据"
- "Level-2 数据"、"逐笔数据"、"订单簿"
- "绩效归因"、"Brinson"、"Campisi"
- "投资组合"、"权重优化"、"MVO"
- "实时计算"、"流式因子"、"高频因子"
- "Alphalens"、"因子分析"、"IC 分析"

## 能力范围

### 1. 因子计算
- 日频/分钟频因子计算
- 高频因子实时计算
- Alpha101 因子库
- TA-Lib 技术指标
- 流批一体因子计算平台

### 2. 策略回测
- 股票中低频策略回测
- 期货回测
- 期权回测
- 多资产组合回测
- 模拟撮合引擎

### 3. 行情处理
- K 线合成（分钟/小时/日）
- Level-2 数据处理
- 订单簿合成
- 行情回放
- 复权计算

### 4. 绩效归因
- Brinson 绩效归因
- Campisi 绩效归因
- 因子归因分析
- 多因子风险模型

### 5. 投资组合优化
- 均值方差优化（MVO）
- 约束优化（SOCP）
- 权重分配
- 风险控制

### 6. 实时计算
- 实时高频因子
- 实时资金流计算
- 实时涨幅榜
- 实时波动率预测

## 使用示例

### 1. 因子计算最佳实践

```python
import dolphindb as ddb

s = ddb.session()
s.connect(host="localhost", port=8848, userid="admin", password="123456")

# 加载 MyTT 模块计算技术指标
s.run('use mytt')

# 计算均线、RSI、波动率
result = s.run('''
    // 计算均线
    def getMA(close, period=5){
        return MA(close, period)
    }
    
    // 计算 RSI
    def getRSI(close, N=24){
        return RSI(close, N)
    }
    
    // 计算波动率
    def getVolatility(close, period=10){
        returns = DIFF(close) / REF(close, 1)
        return STD(returns, period)
    }
    
    // 批量计算因子
    select 
        sym,
        getMA(close, 5) as ma5,
        getMA(close, 20) as ma20,
        getRSI(close, 24) as rsi,
        getVolatility(close, 10) as vol
    from loadTable("dfs://bars_db.bars_minute")
    where date = 2024.01.01
    context by sym
''')

df = result.toDF()
s.close()
```

### 2. 股票回测配置

```python
import dolphindb as ddb

s = ddb.session()
s.connect(host="localhost", port=8848, userid="admin", password="123456")

# 回测参数配置
s.run('''
    config = dict(STRING, ANY)
    config["startDate"] = 2024.01.01
    config["endDate"] = 2024.12.31
    config["strategyGroup"] = "stock"
    config["frequency"] = 0
    config["cash"] = 10000000.0  // 初始资金 1000 万
    config["commission"] = 0.0005  // 交易佣金
    config["tax"] = 0.0
    config["dataType"] = 3  // 分钟频
    config["matchingMode"] = 3  // 委托价格成交
    config["msgAsTable"] = false
    
    // 上下文配置
    context = dict(STRING, ANY)
    context["activeTime"] = 14:30m  // 每日交易时间
    context["maxPosition"] = 0.1    // 单只股票最大持仓 10%
    context["minPosition"] = 0.001  // 单只股票最小持仓 0.1%
    config["context"] = context
''')

s.close()
```

### 3. K 线合成

```python
import dolphindb as ddb

s = ddb.session()
s.connect(host="localhost", port=8848, userid="admin", password="123456")

# 基于 tick 数据合成分钟 K 线
result = s.run('''
    def synthesizeOHLC(tickData, interval=60000){
        return select 
            first(time) as openTime,
            last(time) as closeTime,
            first(open) as open,
            max(high) as high,
            min(low) as low,
            last(close) as close,
            sum(volume) as volume,
            sum(turnover) as turnover
        from tickData
        group by sym, time_bar(interval, time) as barTime
    }
''')

# 使用内置 OHLC 引擎
s.run('''
    engine = createOHLEngine(
        name=`ohlcEngine,
        windowSize=50000,
        timeColumn=`time,
        groupingColumn=`sym,
        buckets=100,
        freq=60000,  // 1 分钟
        metrics=`open`high`low`close`volume
    )
''')

s.close()
```

### 4. Level-2 订单簿合成

```python
import dolphindb as ddb

s = ddb.session()
s.connect(host="localhost", port=8848, userid="admin", password="123456")

# 基于逐笔数据合成订单簿
s.run('''
    use orderbook
    
    engine = createOrderBookEngine(
        name=`obEngine,
        windowSize=100000,
        timeColumn=`time,
        symColumn=`sym,
        priceColumn=`price,
        volumeColumn=`volume,
        bsFlagColumn=`bsFlag,  // B=买，S=卖
        level=10  // 10 档行情
    )
    
    // 订阅订单簿输出
    subscribeTable(
        tableName=`obEngine,
        actionName=`processOB,
        offset=0,
        handler=processOrderBook
    )
''')

s.close()
```

### 5. Brinson 绩效归因

```python
import dolphindb as ddb

s = ddb.session()
s.connect(host="localhost", port=8848, userid="admin", password="123456")

# Brinson 归因分析
s.run('use brinson')

# 配置归因并执行
result = s.run('''
    // Brinson 归因分析
    brinsonConfig = dict(STRING, ANY)
    brinsonConfig["portfolioReturn"] = portfolioRet  // 组合收益
    brinsonConfig["benchmarkReturn"] = benchmarkRet  // 基准收益
    brinsonConfig["portfolioWeights"] = portWeights  // 组合权重
    brinsonConfig["benchmarkWeights"] = benchWeights // 基准权重
    
    // 执行归因
    brinsonResult = brinsonAttribution(brinsonConfig)
    // 输出：配置效应、选股效应、交互效应
''')

df = result.toDF()
s.close()
```

### 6. 投资组合优化（MVO）

```python
import dolphindb as ddb

s = ddb.session()
s.connect(host="localhost", port=8848, userid="admin", password="123456")

# 均值方差优化
s.run('use mvo')

# 准备数据并执行优化
result = s.run('''
    // 准备数据
    returns = loadReturns()  // 历史收益率矩阵
    covMatrix = cov(returns) // 协方差矩阵
    expectedReturns = mean(returns) // 预期收益
    
    // 配置优化参数
    mvoConfig = dict(STRING, ANY)
    mvoConfig["expectedReturns"] = expectedReturns
    mvoConfig["covariance"] = covMatrix
    mvoConfig["riskFreeRate"] = 0.02  // 无风险利率 2%
    mvoConfig["constraints"] = dict(
        "sumWeights" = 1.0,      // 权重和为 1
        "minWeight" = 0.0,       // 最小权重 0
        "maxWeight" = 0.2        // 最大权重 20%
    )
    
    // 执行优化
    optimalWeights = mvoOptimize(mvoConfig)
''')

s.close()
```

### 7. 实时高频因子计算

```python
import dolphindb as ddb

s = ddb.session()
s.connect(host="localhost", port=8848, userid="admin", password="123456")

# 创建流数据表
s.run('streamTable(10000:0, `time`sym`price`volume, [TIMESTAMP,SYMBOL,DOUBLE,LONG])')

# 定义实时因子计算函数并创建引擎
s.run('''
    def calcRealtimeFactor(data){
        return select 
            sym,
            wap(price, volume) as vwap,  // 成交量加权均价
            (max(price) - min(price)) / last(price) as range,  // 价格区间
            sum(volume) as totalVolume,
            count(*) as tradeCount
        from data
        group by sym, time_bar(60000, time) as minute
    }
    
    engine = createStreamEngine(
        name=`realtimeFactorEngine,
        handler=calcRealtimeFactor,
        streamTableNames=`tickStream,
        windowSize=1000,
        timeColumn=`time,
        groupingColumn=`sym
    )
''')

s.close()
```

### 8. Alphalens 因子分析

```python
import dolphindb as ddb

s = ddb.session()
s.connect(host="localhost", port=8848, userid="admin", password="123456")

# 使用 Alphalens 框架分析因子
s.run('use alphalens')

# 准备因子数据和收益数据并执行分析
result = s.run('''
    // 准备因子数据和收益数据
    factorData = loadFactorData()  // 因子值
    returnsData = loadReturnsData() // 未来收益
    
    // 配置分析参数
    alphalensConfig = dict(STRING, ANY)
    alphalensConfig["factor"] = factorData
    alphalensConfig["returns"] = returnsData
    alphalensConfig["periods"] = [1, 5, 10, 20]  // 分析周期
    
    // 执行分析
    result = alphalensAnalysis(alphalensConfig)
    // 输出：IC 分析、分层回测、换手率等
''')

s.close()
```

### 9. 实时资金流计算

```python
import dolphindb as ddb

s = ddb.session()
s.connect(host="localhost", port=8848, userid="admin", password="123456")

# 实时计算分钟资金流
s.run('''
    def calcCapitalFlow(tickData){
        // 定义主买主卖
        update tickData set 
            isBuy = iif(bsFlag=='B' or (price>prev(price)), 1, 0),
            isSell = iif(bsFlag=='S' or (price<prev(price)), 1, 0)
        
        // 计算资金流
        return select 
            sym,
            sum(iif(isBuy, price*volume, 0)) as buyFlow,
            sum(iif(isSell, price*volume, 0)) as sellFlow,
            sum(price*volume) as totalFlow
        from tickData
        group by sym, time_bar(60000, time) as minute
    }
''')

s.close()
```

## 金融数据模型

### 统一数据模型（Instrument & MarketData）

```python
import dolphindb as ddb

s = ddb.session()
s.connect(host="localhost", port=8848, userid="admin", password="123456")

# 证券主表
s.run('''
    instrument = table(
        `AAPL`GOOG`MSFT as sym,
        `Apple Inc.`Alphabet Inc.`Microsoft Corp. as name,
        `STOCK`STOCK`STOCK as type,
        `USD`USD`USD as currency,
        100.0 100.0 100.0 as parValue
    )
''')

# 行情数据表
s.run('''
    marketData = table(
        1:0,
        `instrument`tradeDate`tradeTime`price`volume`turnover,
        [SYMBOL,DATE,TIME,DOUBLE,LONG,DOUBLE]
    )
''')

s.close()
```

## 性能优化建议

### 分区策略
- 按交易日期 VALUE 分区
- 按证券代码 HASH 分区
- 复合分区：`partitioned by date, sym`

### 查询优化
- 使用分区列过滤触发分区裁剪
- 使用 `context by` 进行分组计算
- 避免跨分区 JOIN

### 存储优化
- 使用 TSDB 引擎存储时序数据
- 启用压缩（LZ4，压缩比 20-25%）
- 定期合并小分区

## 参考文档

- **DolphinDB 官网**: https://www.dolphindb.cn/
- **DolphinDB 文档中心**: https://docs.dolphindb.cn/zh/
- **量化金融范例**: https://docs.dolphindb.cn/zh/tutorials/quant_finance_examples.html
- **因子计算最佳实践**: https://docs.dolphindb.cn/zh/tutorials/best_practice_for_factor_calculation.html
- **股票回测案例**: https://docs.dolphindb.cn/zh/tutorials/stock_backtest.html
- **Brinson 绩效归因**: https://docs.dolphindb.cn/zh/tutorials/brinson.html
- **Campisi 绩效归因**: https://docs.dolphindb.cn/zh/tutorials/campisi.html
- **MVO 投资组合优化**: https://docs.dolphindb.cn/zh/tutorials/MVO.html
- **K 线计算**: https://docs.dolphindb.cn/zh/tutorials/OHLC_2.html
- **Level-2 数据处理**: https://docs.dolphindb.cn/zh/tutorials/l2_stk_data_proc_2.html
- **实时高频因子**: https://docs.dolphindb.cn/zh/tutorials/hf_factor_streaming_2.html
- **回测插件**: https://docs.dolphindb.cn/zh/plugins/backtest.html

---

## 相关技能

- **dolphindb-skills**: 技能套件索引（含环境检测）
- **dolphindb-basic**: DolphinDB 基础 CRUD 操作
- **dolphindb-streaming**: 流式计算（实时因子、实时行情、实时风控）
- **dolphindb-docker**: Docker 容器化部署
