# DolphinDB 流式计算技能 v1.1.3

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
s.run('''
    // DolphinDB 脚本
    share streamTable(10000:0, `time`sym`price`volume, 
        [TIMESTAMP,SYMBOL,DOUBLE,LONG]) as tickStream
''')

# 3. 关闭连接
s.close()
```

---

## 描述
提供 DolphinDB 流数据计算能力，专注于实时行情处理、实时因子计算、实时风控等金融场景的流式计算解决方案。

## 触发条件
当用户提到以下关键词时触发此技能：
- "实时计算"、"流式计算"、"streaming"
- "实时行情"、"tick 数据"、"逐笔数据"
- "实时因子"、"实时指标"
- "流数据表"、"streamTable"
- "流计算引擎"、"reactor"
- "实时风控"、"实时监控"
- "消息订阅"、"subscribeTable"

## 能力范围

### 1. 流数据表管理
- 创建流数据表
- 流表持久化
- 流表数据发布/订阅

### 2. 流计算引擎
- 响应式状态引擎
- 聚合引擎
- 订单簿引擎
- OHLC 引擎
- 自定义流计算引擎

### 3. 实时因子计算
- 分钟频实时因子
- 高频实时因子
- Level-2 实时指标
- 资金流实时计算

### 4. 实时行情处理
- 实时 K 线合成
- 实时订单簿合成
- 实时涨跌停监控
- 实时涨幅榜计算

### 5. 实时风控
- 实时持仓监控
- 实时盈亏计算
- 实时风险指标
- 异常交易检测

## 使用示例

### 1. 创建流数据表

```python
import dolphindb as ddb

s = ddb.session()
s.connect(host="localhost", port=8848, userid="admin", password="123456")

# 创建共享流数据表
s.run('''
    share streamTable(10000:0, `time`sym`price`volume`bsFlag, 
        [TIMESTAMP,SYMBOL,DOUBLE,LONG,CHAR]) as tickStream
''')

# 创建持久化流表（带数据持久化）
s.run('''
    streamTable(
        windowSize=1000000,
        schema=table(1:0, `time`sym`price`volume, [TIMESTAMP,SYMBOL,DOUBLE,LONG]),
        persistenceDir="/data/stream/persistence",
        name=`persistentTickStream
    )
''')

s.close()
```

### 2. 响应式状态引擎

```python
import dolphindb as ddb

s = ddb.session()
s.connect(host="localhost", port=8848, userid="admin", password="123456")

# 定义状态更新函数并创建引擎
s.run('''
    def updateState(state, newData){
        // 更新最新价格
        state[`lastPrice] = newData.price
        // 更新累计成交量
        state[`totalVolume] = coalesce(state[`totalVolume], 0) + newData.volume
        // 更新最高最低价
        state[`highPrice] = max(coalesce(state[`highPrice], 0), newData.price)
        state[`lowPrice] = min(coalesce(state[`lowPrice], DOUBLE_MAX), newData.price)
        return state
    }
    
    engine = createReactiveStateEngine(
        name=`stateEngine,
        streamTableNames=`tickStream,
        handler=updateState,
        keyColumn=`sym,
        initState=dict(`lastPrice`totalVolume`highPrice`lowPrice, 
                       [0.0,0L,0.0,DOUBLE_MAX])
    )
''')

s.close()
```

### 3. 实时 K 线合成引擎

```python
import dolphindb as ddb

s = ddb.session()
s.connect(host="localhost", port=8848, userid="admin", password="123456")

# 创建 OHLC 流计算引擎
s.run('''
    ohlcEngine = createOHLEngine(
        name=`minuteOHLC,
        streamTableNames=`tickStream,
        timeColumn=`time,
        groupingColumn=`sym,
        freq=60000,  // 1 分钟 K 线
        metrics=`open`high`low`close`volume`turnover,
        outputTable=share(streamTable(10000:0, 
            `barTime`sym`open`high`low`close`volume`turnover,
            [TIMESTAMP,SYMBOL,DOUBLE,DOUBLE,DOUBLE,DOUBLE,LONG,DOUBLE]), `ohlcOutput)
    )
''')

# 订阅 K 线输出
s.run('''
    def processOHLC(data){
        // 处理 K 线数据（如发送到前端、存储等）
        print("New OHLC bar: " + data)
    }
    
    subscribeTable(
        tableName=`ohlcOutput,
        actionName=`processOHLC,
        offset=0,
        handler=processOHLC
    )
''')

s.close()
```

### 4. 实时订单簿引擎

```python
import dolphindb as ddb

s = ddb.session()
s.connect(host="localhost", port=8848, userid="admin", password="123456")

# 创建订单簿引擎（基于逐笔数据合成）
s.run('''
    obEngine = createOrderBookEngine(
        name=`orderBookEngine,
        streamTableNames=`tickStream,
        timeColumn=`time,
        symColumn=`sym,
        priceColumn=`price,
        volumeColumn=`volume,
        bsFlagColumn=`bsFlag,  // 'B'=买，'S'=卖
        level=10,  // 10 档行情
        outputTable=share(streamTable(10000:0,
            `time`sym`bid1`bidSz1`ask1`askSz1`bid2`bidSz2`ask2`askSz2,
            [TIMESTAMP,SYMBOL,DOUBLE,LONG,DOUBLE,LONG,DOUBLE,LONG,DOUBLE,LONG]), `obOutput)
    )
''')

# 订阅订单簿更新
s.run('''
    def processOrderBook(ob){
        // 计算买卖压力指标
        bidPressure = sum(ob[`bidSz1], ob[`bidSz2]) 
        askPressure = sum(ob[`askSz1], ob[`askSz2])
        imbalance = (bidPressure - askPressure) / (bidPressure + askPressure)
        
        if abs(imbalance) > 0.5 {
            print("Large imbalance detected for " + ob.sym + ": " + imbalance)
        }
    }
    
    subscribeTable(
        tableName=`obOutput,
        actionName=`processOB,
        offset=0,
        handler=processOrderBook
    )
''')

s.close()
```

### 5. 实时因子计算引擎

```python
import dolphindb as ddb

s = ddb.session()
s.connect(host="localhost", port=8848, userid="admin", password="123456")

# 定义实时因子计算函数并创建引擎
s.run('''
    def calcRealtimeFactors(tickData){
        return select 
            sym,
            // VWAP（成交量加权均价）
            wap(price, volume) as vwap,
            // 价格动量
            price / last(price, 10) - 1 as momentum,
            // 成交量比率
            sum(volume) / mavg(sum(volume), 20) as volumeRatio,
            // 价格波动
            std(price, 60) / last(price) as volatility,
            // 买卖压力
            sum(iif(bsFlag=='B', volume, 0)) / sum(volume) as buyRatio
        from tickData
        group by sym, time_bar(60000, time) as minute
    }
    
    factorEngine = createStreamEngine(
        name=`realtimeFactorEngine,
        handler=calcRealtimeFactors,
        streamTableNames=`tickStream,
        windowSize=1000,
        timeColumn=`time,
        groupingColumn=`sym,
        outputTable=share(streamTable(10000:0,
            `minute`sym`vwap`momentum`volumeRatio`volatility`buyRatio,
            [TIMESTAMP,SYMBOL,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE]), `factorOutput)
    )
''')

s.close()
```

### 6. 实时资金流计算

```python
import dolphindb as ddb

s = ddb.session()
s.connect(host="localhost", port=8848, userid="admin", password="123456")

# 实时计算分钟资金流
s.run('''
    def calcCapitalFlow(tickData){
        // 定义主买主卖判断
        update tickData set 
            isBuy = iif(
                bsFlag=='B' or 
                (price > prev(price, 1) and volume > prev(volume, 1)), 
                1, 0
            ),
            isSell = iif(
                bsFlag=='S' or 
                (price < prev(price, 1) and volume > prev(volume, 1)), 
                1, 0
            )
        
        // 计算资金流
        return select 
            sym,
            sum(iif(isBuy, price*volume, 0)) as buyFlow,
            sum(iif(isSell, price*volume, 0)) as sellFlow,
            sum(price*volume) as totalFlow,
            (sum(iif(isBuy, price*volume, 0)) - sum(iif(isSell, price*volume, 0))) 
                / sum(price*volume) as netFlowRatio
        from tickData
        group by sym, time_bar(60000, time) as minute
    }
    
    capitalFlowEngine = createStreamEngine(
        name=`capitalFlowEngine,
        handler=calcCapitalFlow,
        streamTableNames=`tickStream,
        windowSize=1000,
        timeColumn=`time,
        groupingColumn=`sym
    )
''')

s.close()
```

### 7. 实时涨幅榜计算

```python
import dolphindb as ddb

s = ddb.session()
s.connect(host="localhost", port=8848, userid="admin", password="123456")

# 实时计算涨幅榜
s.run('''
    def calcPriceChangeRank(tickData){
        // 获取昨日收盘价（从维度表或缓存中）
        prevClose = loadPrevClose()
        
        return select 
            top 50 sym,
            last(price) as lastPrice,
            last(price) / prevClose[sym] - 1 as changePct,
            sum(volume) as volume,
            sum(price*volume) as turnover
        from tickData
        where time >= today() + 09:30:00m
        group by sym
        order by changePct desc
        limit 50
    }
    
    rankEngine = createStreamEngine(
        name=`priceChangeRankEngine,
        handler=calcPriceChangeRank,
        streamTableNames=`tickStream,
        windowSize=10000,
        timeColumn=`time,
        triggeringPattern='interval',
        triggeringInterval=5000  // 每 5 秒更新一次
    )
''')

s.close()
```

### 8. 实时风控监控

```python
import dolphindb as ddb

s = ddb.session()
s.connect(host="localhost", port=8848, userid="admin", password="123456")

# 实时持仓监控
s.run('''
    def realtimeRiskMonitor(positionData, marketData){
        // 计算实时盈亏
        update positionData set 
            marketValue = position * marketData.price,
            pnl = (marketData.price - avgCost) * position,
            pnlRatio = (marketData.price - avgCost) / avgCost
        
        // 风险检查
        riskAlerts = select 
            sym,
            pnl,
            pnlRatio,
            marketValue,
            iif(abs(pnlRatio) > 0.05, "WARNING", "OK") as status
        from positionData
        where abs(pnlRatio) > 0.02  // 盈亏超过 2% 触发检查
        
        if size(riskAlerts) > 0 {
            sendAlert(riskAlerts)  // 发送风控警报
        }
        
        return positionData
    }
    
    riskEngine = createStreamEngine(
        name=`riskMonitorEngine,
        handler=realtimeRiskMonitor,
        streamTableNames=[`positionStream, `marketStream],
        windowSize=1000,
        timeColumn=`time
    )
''')

s.close()
```

### 9. 多引擎协同工作

```python
import dolphindb as ddb

s = ddb.session()
s.connect(host="localhost", port=8848, userid="admin", password="123456")

# 构建完整的实时计算流水线
s.run('''
    // 1. 原始 tick 数据流
    share streamTable(100000:0, `time`sym`price`volume`bsFlag, 
        [TIMESTAMP,SYMBOL,DOUBLE,LONG,CHAR]) as tickStream
    
    // 2. OHLC 引擎
    ohlcEngine = createOHLEngine(
        name=`ohlcEngine,
        streamTableNames=`tickStream,
        freq=60000,
        metrics=`open`high`low`close`volume
    )
    
    // 3. 因子计算引擎（基于 OHLC）
    factorEngine = createStreamEngine(
        name=`factorEngine,
        handler=calcFactors,
        streamTableNames=`ohlcOutput,
        windowSize=100
    )
    
    // 4. 信号生成引擎
    signalEngine = createStreamEngine(
        name=`signalEngine,
        handler=generateSignals,
        streamTableNames=`factorOutput,
        windowSize=10
    )
    
    // 5. 执行引擎
    execEngine = createStreamEngine(
        name=`execEngine,
        handler=executeOrders,
        streamTableNames=`signalOutput,
        windowSize=10
    )
''')

s.close()
```

## 流计算引擎类型

### 1. 响应式状态引擎（ReactiveStateEngine）
- 维护每个 key 的状态
- 适用于累计计算、最新值跟踪

### 2. 聚合引擎（AggregationEngine）
- 时间窗口聚合
- 适用于 K 线合成、统计指标

### 3. 订单簿引擎（OrderBookEngine）
- 基于逐笔合成订单簿
- 适用于 Level-2 行情处理

### 4. OHLC 引擎
- 专门用于 K 线合成
- 高性能、低延迟

### 5. 自定义流引擎（StreamEngine）
- 自定义处理逻辑
- 最灵活

## 性能优化

### 窗口大小
- 根据数据频率和内存调整
- tick 数据：1000-10000
- 分钟数据：100-1000

### 触发模式
- `row`: 每行触发（最低延迟）
- `batch`: 批量触发（更高吞吐）
- `interval`: 定时触发（可控频率）

### 数据持久化
- 启用 persistenceDir 防止数据丢失
- 配置适当的 windowSize 避免内存溢出

## 参考文档

- **DolphinDB 官网**: https://www.dolphindb.cn/
- **DolphinDB 文档中心**: https://docs.dolphindb.cn/zh/
- **流数据教程**: https://docs.dolphindb.cn/zh/stream/str_intro.html
- **金融因子流式实现**: https://docs.dolphindb.cn/zh/tutorials/str_comp_fin_quant_2.html
- **实时高频因子**: https://docs.dolphindb.cn/zh/tutorials/hf_factor_streaming_2.html
- **实时计算资金流**: https://docs.dolphindb.cn/zh/tutorials/streaming_capital_flow_order_by_order_2.html
- **实时计算涨幅榜**: https://docs.dolphindb.cn/zh/tutorials/rt_stk_price_inc_calc_2.html
- **Level-2 数据处理**: https://docs.dolphindb.cn/zh/tutorials/l2_stk_data_proc_2.html
- **订单簿引擎**: https://docs.dolphindb.cn/zh/tutorials/orderBookSnapshotEngine.html

---

## 相关技能

- **dolphindb-skills**: 技能套件索引（含环境检测）
- **dolphindb-basic**: DolphinDB 基础 CRUD 操作
- **dolphindb-quant-finance**: 量化金融场景
- **dolphindb-docker**: Docker 容器化部署
