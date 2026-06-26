# DolphinDB 技能套件 v1.4.0

> 📘 DolphinDB 数据库套件的入口文件

本技能是 DolphinDB 套件的**入口文件**，为以下子技能提供统一入口：
- `dolphindb-basic` - 基础 CRUD 操作
- `dolphindb-docker` - Docker 容器化部署
- `dolphindb-quant-finance` - 量化金融场景
- `dolphindb-streaming` - 流式计算

同时提供**基础 DolphinDB 读写能力**，支持建库建表、数据增删改查等核心操作。

---

## 🚨 强制流程：每次调用 DolphinDB 技能前必须执行

**所有 DolphinDB 相关操作，必须遵循以下流程：**

```
1. 环境检测 → 2. 加载环境 → 3. 验证 SDK → 4. 执行操作
```

### 第一步：环境检测（必须）

```bash
# 方法 1: 使用包装器脚本（推荐）
cd ~/.jvs/.openclaw/workspace/skills/dolphindb-skills
source scripts/dolphin_wrapper.sh

# 方法 2: 手动检测
python3 scripts/init_dolphindb_env.py --export
```

### 第二步：验证环境

```bash
# 验证 SDK 已安装
$DOLPHINDB_PYTHON_BIN -c "import dolphindb; print(dolphindb.__version__)"

# 或
dolphin_python -c "import dolphindb; print(dolphindb.__version__)"
```

### 第三步：执行 Python 脚本

```bash
# 使用包装器
dolphin_python your_script.py

# 或直接使用检测到的 Python
$DOLPHINDB_PYTHON_BIN your_script.py
```

**环境检测逻辑：**
1. 扫描 conda 环境列表 → 检查每个环境的 `pip list`，查找 `dolphindb`
2. 扫描 Anaconda/Miniconda 路径 → 检查 `$CONDA_BASE` 等
3. 扫描系统 Python 环境 → 检查 `/usr/bin/python3` 等
4. 决策：找到已安装 → 导出 `DOLPHINDB_PYTHON_BIN`；未找到 → 自动安装

**统一调用接口：**
```bash
dolphin_python script.py    # 运行 Python 脚本
dolphin_pip install pkg     # 安装包
```

**重要**: 详见 [USAGE_GUIDE.md](USAGE_GUIDE.md) 和 [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)

**重要：所有 DolphinDB 脚本在 Python 中的调用方式**

```python
import dolphindb as ddb

# 1. 建立连接
s = ddb.session()
s.connect(host="localhost", port=8848, userid="admin", password="123456")

# 2. 执行 DolphinDB 脚本（所有数据库操作都通过 s.run()）
result = s.run('''
    // DolphinDB 脚本
    select * from loadTable("dfs://mydb.mytable")
    where date = 2024.01.01
''')

# 3. 转换为 pandas DataFrame（可选）
df = result.toDF()

# 4. 关闭连接
s.close()
```

---

## 📚 技能导航

### 快速选择指南

| 需求场景 | 推荐技能 | 说明 |
|---------|---------|------|
| **快速部署/安装** | [`dolphindb-docker`](#dolphindb-docker---docker-部署技能) | Docker 容器化部署 |
| 建库建表、增删改查 | [`dolphindb-basic`](#dolphindb-basic---基础操作技能) | 数据库基础操作 |
| 因子计算、策略回测 | [`dolphindb-quant-finance`](#dolphindb-quant-finance---量化金融技能) | 量化投研场景 |
| 实时计算、流式处理 | [`dolphindb-streaming`](#dolphindb-streaming---流式计算技能) | 实时行情/风控 |

---

## 技能详情

### dolphindb-docker - Docker 部署技能

**🔗 技能标识**: `dolphindb-docker`  
**📦 版本**: 1.0.0  
**🏷️ 标签**: `dolphindb`, `docker`, `deployment`, `devops`

#### 功能概览

| 功能模块 | 能力描述 |
|---------|---------|
| **Docker 检查** | 检查 Docker 安装状态、版本、服务状态 |
| **Docker 安装** | macOS/Windows/Linux 自动安装 Docker CE |
| **镜像管理** | 搜索、拉取官方 DolphinDB 镜像 |
| **容器部署** | 单机部署、端口映射 (8848)、数据持久化 |
| **高级配置** | Dockerfile 自定义、docker-compose 编排 |

#### 核心示例

```bash
# 快速部署（一行命令）
docker run -d --name dolphindb -p 8848:8848 -p 8081:8081 \
    -v dolphindb-data:/data dolphindb/dolphindb:latest

# 使用 docker-compose
docker-compose up -d

# 连接测试（Python SDK）
dolphin_python -c "
import dolphindb as ddb
s=ddb.session()
s.connect('localhost',8848)
print(s.run('select now()'))
"
```

#### 触发关键词

`DolphinDB Docker`、`Docker 安装`、`容器化部署`、`docker-compose`、`快速部署`、`一键安装`、`Docker Hub`、`镜像拉取`、`端口 8848`

#### 📖 详细文档

查看完整技能：`skills/dolphindb-docker/SKILL.md`

---

### dolphindb-basic - 基础操作技能

**🔗 技能标识**: `dolphindb-basic`  
**📦 版本**: 1.2.0  
**🏷️ 标签**: `dolphindb`, `database`, `crud`, `quant`

#### 功能概览

| 功能模块 | 能力描述 |
|---------|---------|
| **创建数据库** | 分布式数据库（VALUE/RANGE/HASH/LIST/COMPO）、内存数据库 |
| **创建表** | 分区表、维度表、内存表、流表 |
| **插入数据** | INSERT INTO、append!、tableInsert |
| **查询数据** | SQL 查询、条件过滤、聚合查询、分区裁剪 |
| **更新数据** | UPDATE 语句、条件更新、批量更新 |
| **删除数据** | DELETE、DROP 表/数据库、删除分区 |

#### 核心示例

```python
import dolphindb as ddb

s = ddb.session()
s.connect(host="localhost", port=8848, userid="admin", password="123456")

# 创建数据库（通过 s.run 执行 DolphinDB 脚本）
s.run('''
    db = database(
        directory="dfs://valuedb", 
        partitionType=VALUE, 
        partitionScheme=2023.01.01..2023.12.31, 
        engine='TSDB'
    )
''')

# 创建表
s.run('''
    schema = table(1:0, `date`time`sym`price`volume, [DATE,TIME,SYMBOL,DOUBLE,LONG])
    pt = createPartitionedTable(
        dbHandle=db, 
        table=schema, 
        tableName=`stock_data, 
        partitionColumns=`date, 
        sortColumns=`sym`time
    )
''')

# 插入数据
s.run('INSERT INTO stock_data VALUES (2024.01.01, 09:30:00, `AAPL, 150.5, 1000000)')

# 查询数据
result = s.run('select * from stock_data where date=2024.01.01')
print(result.toDF())

s.close()
```

#### 触发关键词

`DolphinDB 建库`、`创建数据库`、`建表`、`插入数据`、`写入数据`、`查询`、`SELECT`、`更新`、`修改数据`、`删除`、`DROP`、`CRUD`、`分布式数据库`、`内存表`、`分区表`

#### 📖 详细文档

查看完整技能：`skills/dolphindb-basic/SKILL.md`

---

### dolphindb-quant-finance - 量化金融技能

**🔗 技能标识**: `dolphindb-quant-finance`  
**📦 版本**: 1.1.0  
**🏷️ 标签**: `dolphindb`, `quant`, `factor`, `backtest`, `finance`

#### 功能概览

| 功能模块 | 能力描述 |
|---------|---------|
| **因子计算** | 日频/分钟频/高频因子、Alpha101、TA-Lib 技术指标 |
| **策略回测** | 股票/期货/期权回测、模拟撮合引擎 |
| **行情处理** | K 线合成、Level-2 数据、订单簿、复权计算 |
| **绩效归因** | Brinson、Campisi、因子归因分析 |
| **投资组合** | MVO 均值方差优化、SOCP 约束优化 |
| **实时计算** | 实时因子、资金流、涨幅榜、波动率 |

#### 核心示例

```python
import dolphindb as ddb

s = ddb.session()
s.connect(host="localhost", port=8848, userid="admin", password="123456")

# 因子计算（通过 s.run 执行）
result = s.run('''
    use mytt
    // 计算 RSI 因子
    def getRSI(close, N=24){ return RSI(close, N) }
    
    // 批量计算因子
    select 
        sym,
        getRSI(close, 24) as rsi,
        mavg(close, 5) as ma5
    from loadTable("dfs://bars_db.bars_minute")
    where date = 2024.01.01
    context by sym
''')

# 回测配置
s.run('''
    config = dict(STRING, ANY)
    config["startDate"] = 2024.01.01
    config["cash"] = 10000000.0  // 1000 万初始资金
    config["commission"] = 0.0005
''')

# Brinson 绩效归因
s.run('use brinson')
brinson_result = s.run('''
    result = brinsonAttribution(portfolioRet, benchmarkRet, portWeights, benchWeights)
''')

s.close()
```

#### 触发关键词

`量化因子`、`因子计算`、`策略回测`、`backtest`、`K 线合成`、`OHLC`、`Level-2`、`订单簿`、`绩效归因`、`Brinson`、`Campisi`、`投资组合`、`MVO`、`Alphalens`

#### 📖 详细文档

查看完整技能：`skills/dolphindb-quant-finance/SKILL.md`

---

### dolphindb-streaming - 流式计算技能

**🔗 技能标识**: `dolphindb-streaming`  
**📦 版本**: 1.1.0  
**🏷️ 标签**: `dolphindb`, `streaming`, `realtime`, `quant`

#### 功能概览

| 功能模块 | 能力描述 |
|---------|---------|
| **流数据表** | 创建、持久化、发布/订阅 |
| **流计算引擎** | 响应式状态引擎、聚合引擎、订单簿引擎、OHLC 引擎 |
| **实时因子** | 分钟频/高频因子、Level-2 指标 |
| **实时行情** | K 线合成、订单簿合成、涨跌停监控 |
| **实时风控** | 持仓监控、盈亏计算、风险指标 |

#### 核心示例

```python
import dolphindb as ddb

s = ddb.session()
s.connect(host="localhost", port=8848, userid="admin", password="123456")

# 创建流数据表（通过 s.run 执行）
s.run('''
    share streamTable(10000:0, `time`sym`price`volume`bsFlag, 
        [TIMESTAMP,SYMBOL,DOUBLE,LONG,CHAR]) as tickStream
''')

# 创建 OHLC 引擎（实时 K 线合成）
s.run('''
    ohlcEngine = createOHLEngine(
        name=`minuteOHLC,
        streamTableNames=`tickStream,
        freq=60000,  // 1 分钟 K 线
        metrics=`open`high`low`close`volume
    )
''')

# 创建订单簿引擎
s.run('''
    obEngine = createOrderBookEngine(
        name=`orderBookEngine,
        streamTableNames=`tickStream,
        level=10,  // 10 档行情
        bsFlagColumn=`bsFlag
    )
''')

# 实时因子计算
result = s.run('''
    def calcRealtimeFactors(tickData){
        return select 
            sym,
            wap(price, volume) as vwap,
            price / last(price, 10) - 1 as momentum
        from tickData
        group by sym, time_bar(60000, time) as minute
    }
''')

s.close()
```

#### 触发关键词

`实时计算`、`流式计算`、`streaming`、`实时行情`、`tick 数据`、`实时因子`、`流数据表`、`streamTable`、`流计算引擎`、`实时风控`

#### 📖 详细文档

查看完整技能：`skills/dolphindb-streaming/SKILL.md`

---

## 🔗 技能组合使用

复杂任务可能需要多个技能协同：

### 场景 1: 快速搭建量化投研环境

```
用户需求："帮我快速搭建一个 DolphinDB 量化投研环境"

涉及技能:
1. dolphindb-docker: 快速部署 DolphinDB 容器
2. dolphindb-basic: 创建数据库和表结构
3. dolphindb-quant-finance: 因子计算和策略回测
```

### 场景 2: 实时因子计算系统

```
用户需求："帮我搭建一个实时因子计算系统，能计算分钟频因子并实时回测"

涉及技能:
1. dolphindb-docker: 部署 DolphinDB 容器
2. dolphindb-streaming: 创建流数据表、流计算引擎
3. dolphindb-quant-finance: 因子计算公式、回测配置
4. dolphindb-basic: 创建存储结果的数据库表
```

### 场景 3: 量化投研平台

```
用户需求："搭建量化投研平台，需要因子库、回测、绩效分析"

涉及技能:
1. dolphindb-docker: 容器化部署
2. dolphindb-quant-finance: 因子计算、策略回测、绩效归因
3. dolphindb-basic: 数据库管理、数据存储
```

### 场景 4: 实时行情监控系统

```
用户需求："实时监控行情，合成 K 线和订单簿，检测异常波动"

涉及技能:
1. dolphindb-docker: 快速部署
2. dolphindb-streaming: OHLC 引擎、订单簿引擎、实时监控
3. dolphindb-basic: 存储历史数据
```

---

## 📖 官方参考文档

### 基础文档

| 主题 | 文档链接 |
|------|----------|
| DolphinDB 官网 | https://www.dolphindb.cn/ |
| 文档中心 | https://docs.dolphindb.cn/zh/ |
| Docker 部署 | https://docs.dolphindb.cn/zh/deploy/docker/docker_deployment.html |
| 建库建表 | https://docs.dolphindb.cn/zh/db_distr_comp/db_oper/create_db_tb.html |
| 插入数据 | https://docs.dolphindb.cn/zh/db_distr_comp/db_oper/insert_data.html |
| 查询数据 | https://docs.dolphindb.cn/zh/db_distr_comp/db_oper/queries.html |

### 量化金融文档

| 主题 | 文档链接 |
|------|----------|
| 量化金融范例 | https://docs.dolphindb.cn/zh/tutorials/quant_finance_examples.html |
| 因子计算最佳实践 | https://docs.dolphindb.cn/zh/tutorials/best_practice_for_factor_calculation.html |
| 股票回测案例 | https://docs.dolphindb.cn/zh/tutorials/stock_backtest.html |
| Brinson 绩效归因 | https://docs.dolphindb.cn/zh/tutorials/brinson.html |
| MVO 投资组合优化 | https://docs.dolphindb.cn/zh/tutorials/MVO.html |

### 流式计算文档

| 主题 | 文档链接 |
|------|----------|
| 流数据教程 | https://docs.dolphindb.cn/zh/stream/str_intro.html |
| 金融因子流式实现 | https://docs.dolphindb.cn/zh/tutorials/str_comp_fin_quant_2.html |
| 实时高频因子 | https://docs.dolphindb.cn/zh/tutorials/hf_factor_streaming_2.html |
| 订单簿引擎 | https://docs.dolphindb.cn/zh/tutorials/orderBookSnapshotEngine.html |

---

## 📦 安装与使用

### 从 ClawHub 安装

```bash
# 安装单个技能
clawhub install dolphindb-docker
clawhub install dolphindb-basic
clawhub install dolphindb-quant-finance
clawhub install dolphindb-streaming

# 或安装整个套件（推荐）
clawhub install dolphindb-skills
```

### 技能版本

| 技能 | 当前版本 | 发布时间 |
|------|---------|---------|
| dolphindb-docker | 1.0.0 | 2024-03-24 |
| dolphindb-basic | 1.2.0 | 2024-03-24 |
| dolphindb-quant-finance | 1.1.0 | 2024-03-24 |
| dolphindb-streaming | 1.1.0 | 2024-03-24 |
| dolphindb-skills | 1.3.4 | 2026-03-28 |

---

## 📝 更新日志

### v1.3.4 (2026-03-28) - 路径安全修复
- ✅ 修复：将所有绝对路径 `~/.jvs/.openclaw/workspace/skills/dolphindb-skills/scripts/` 改为相对路径 `scripts/`
- ✅ 安全：避免暴露本地文件系统路径结构
- ✅ 兼容：技能安装后可在任何环境中正常工作

### v1.3.3 (2026-03-26) - 入口文件定位优化
- ✅ 修订：明确 `dolphindb-skills` 为套件入口文件
- ✅ 修订：说明为子技能（basic/docker/quant-finance/streaming）提供入口
- ✅ 修订：说明同时提供基础 DolphinDB 读写能力

### v1.3.0 (2026-03-26) - 去重优化版
- ✅ 删除：`dolphindb` 独立技能（内容已整合到套件和其他组件）
- ✅ 整合：环境检测脚本移至 `dolphindb-skills/scripts/`
- ✅ 增强：明确所有 DolphinDB 脚本通过 Python `s.run('<脚本>')` 调用
- ✅ 增强：每个组件开头添加统一的前置依赖说明
- ✅ 去重：删除重复的官方文档链接，统一在套件索引中维护

### v1.2.0 (2024-03-24)
- ✅ 新增：`dolphindb-docker` 技能（Docker 容器化部署）
- ✅ 增强：套件索引更新为 5 个技能
- ✅ 增强：添加 Docker 部署相关的组合使用场景
- ✅ 修复：将所有本地路径替换为 DolphinDB 官方文档链接

### v1.1.0 (2024-03-24)
- ✅ 修复：将所有本地路径替换为 DolphinDB 官方文档链接
- ✅ 增强：basic 技能增加完整的建库建表两种方法说明
- ✅ 增强：套件索引提供完整的技能导航和组合使用指南
- ✅ 新增：技能组合使用场景示例

### v1.0.0 (2024-03-24)
- 🎉 初始发布：DolphinDB 技能套件

---

## 🤝 贡献与支持

- **问题反馈**: 在 ClawHub 技能页面留言
- **技能更新**: 关注 ClawHub 上的最新版本
- **官方文档**: https://docs.dolphindb.cn/zh/
