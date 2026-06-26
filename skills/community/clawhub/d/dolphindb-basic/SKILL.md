# DolphinDB 基础操作技能 v1.2.3

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

## 🚨 强制流程：使用前必须加载环境

**无论在何种场景下调用此技能（单独运行或被引用），必须先执行环境检测：**

```bash
# 方法 1: 在技能目录内运行（推荐）
cd ~/.jvs/.openclaw/workspace/skills/dolphindb-basic
source ../dolphindb-skills/scripts/dolphin_wrapper.sh

# 方法 2: 在任何位置运行（推荐）
source ~/.jvs/.openclaw/workspace/skills/dolphindb-skills/scripts/dolphin_global.sh

# 方法 3: 手动检测
python3 ~/.jvs/.openclaw/workspace/skills/dolphindb-skills/scripts/init_dolphindb_env.py
```

**验证环境：**
```bash
# 验证 SDK 已安装
$DOLPHINDB_PYTHON_BIN -c "import dolphindb; print(dolphindb.__version__)"

# 或使用包装器命令
dolphin_python -c "import dolphindb; print(dolphindb.__version__)"
```

**统一调用接口：**
```bash
dolphin_python script.py    # 运行 Python 脚本
dolphin_pip install pkg     # 安装包
```

**重要**: 详见 [dolphindb-skills/USAGE_GUIDE.md](../dolphindb-skills/USAGE_GUIDE.md)

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

## 描述
提供 DolphinDB 数据库的基础增删改查（CRUD）操作能力，包括建库建表、数据插入、查询、更新、删除等核心功能。

## 触发条件
当用户提到以下关键词时触发此技能：
- "DolphinDB 建库"、"创建数据库"、"建表"
- "DolphinDB 插入数据"、"写入数据"
- "DolphinDB 查询"、"SELECT"
- "DolphinDB 更新"、"修改数据"
- "DolphinDB 删除"、"DROP"
- "DolphinDB CRUD"、"基本操作"
- "分布式数据库"、"内存表"、"分区表"

## 能力范围

### 1. 创建数据库
- **分布式数据库**（VALUE、RANGE、HASH、LIST、COMPO 分区）
- **内存数据库**（高性能临时数据存储）
- 配置存储引擎（TSDB、OLAP、PKEY 等）
- 两种创建方法：`CREATE DATABASE` 语句 和 `database()` 函数

### 2. 创建表
- 创建分布式表（分区表、维度表）
- 创建内存表（普通表、索引表、键值表、流表等）
- 设置排序列和分区列

### 3. 插入数据
- 使用 INSERT INTO 语句
- 使用 append! 函数
- 使用 tableInsert 函数
- 批量插入优化

### 4. 查询数据
- 基础 SQL 查询
- 条件过滤
- 聚合查询
- 分区裁剪优化

### 5. 更新数据
- UPDATE 语句
- 条件更新
- 批量更新

### 6. 删除数据
- DELETE 语句
- DROP 表/数据库
- 删除分区

---

## 详细使用示例

### 一、创建数据库（两种方法）

#### 方法 1：使用 CREATE DATABASE 语句

```python
import dolphindb as ddb

s = ddb.session()
s.connect(host="localhost", port=8848, userid="admin", password="123456")

# 1.1 创建分布式数据库 - VALUE 分区
s.run('''
    CREATE DATABASE "dfs://valuedb" 
    PARTITIONED BY VALUE(2023.01.01..2023.12.31),
    ENGINE="TSDB"
''')

# 1.2 创建分布式数据库 - HASH 分区
s.run('''
    CREATE DATABASE "dfs://hashdb"
    PARTITIONED BY HASH([SYMBOL, 10]),
    ENGINE="OLAP"
''')

# 1.3 创建分布式数据库 - 复合分区（COMPO）
s.run('''
    CREATE DATABASE "dfs://compodb"
    PARTITIONED BY VALUE(2020.01.01..2021.01.01), HASH([SYMBOL, 25])
''')

s.close()
```

#### 方法 2：使用 database() 函数

```python
import dolphindb as ddb

s = ddb.session()
s.connect(host="localhost", port=8848, userid="admin", password="123456")

# 2.1 创建分布式数据库 - VALUE 分区
db = s.run('''
    db = database(
        directory="dfs://valuedb", 
        partitionType=VALUE, 
        partitionScheme=2023.01.01..2023.12.31, 
        engine='TSDB'
    )
''')

# 2.2 创建分布式数据库 - HASH 分区
s.run('''
    db = database(
        directory="dfs://hashdb", 
        partitionType=HASH, 
        partitionScheme=[SYMBOL, 10], 
        engine='OLAP'
    )
''')

# 2.3 创建内存数据库（directory 为空）
s.run('''
    mdb = database(
        directory="", 
        partitionType=VALUE, 
        partitionScheme=1..10
    )
''')

s.close()
```

#### 两种方法的区别

| 特性 | CREATE DATABASE 语句 | database() 函数 |
|------|---------------------|-----------------|
| 返回值 | 无返回值 | 返回数据库句柄 (dbHandle) |
| 使用场景 | 仅创建数据库 | 创建并立即获取句柄 |
| 灵活性 | 适合脚本批量创建 | 适合编程方式操作 |
| 复合分区 | 支持 | 支持（需先创建子分区） |

---

### 二、创建内存数据库

内存数据库将数据直接存储在内存中，具有更快的访问速度和更低的延迟。

```python
import dolphindb as ddb

s = ddb.session()
s.connect(host="localhost", port=8848, userid="admin", password="123456")

# 方法 1：使用 database() 函数创建
s.run('''
    mdb = database(directory="", partitionType=VALUE, partitionScheme=1..10)
''')

# 方法 2：创建内存分区表（自动创建内存数据库）
s.run('''
    mt = table(1:0, `id`sym`val, [INT,SYMBOL,DOUBLE])
''')

# 方法 3：创建内存分区表（带分区）
s.run('''
    mdb = database("", VALUE, 1..10)
    schema = table(1:0, `id`sym`val, [INT,SYMBOL,DOUBLE])
    mpt = mdb.createPartitionedTable(schema, `mpt, `id)
''')

s.close()
```

**内存数据库适用场景**:
- 临时数据处理
- 高速缓存
- 实时计算中间结果
- 测试和开发环境

---

### 三、创建表

#### 3.1 创建分布式表（分区表）

```python
import dolphindb as ddb

s = ddb.session()
s.connect(host="localhost", port=8848, userid="admin", password="123456")

# 获取已创建的数据库句柄
s.run('db = database("dfs://valuedb")')

# 方法 1：使用 CREATE TABLE 语句
s.run('''
    CREATE TABLE "dfs://valuedb"."stock_data"(
        date DATE,
        time TIME,
        sym SYMBOL,
        price DOUBLE,
        volume LONG
    )
    PARTITIONED BY date,
    sortColumns=`sym`time
''')

# 方法 2：使用 createPartitionedTable() 函数
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

s.close()
```

#### 3.2 创建维度表

```python
import dolphindb as ddb

s = ddb.session()
s.connect(host="localhost", port=8848, userid="admin", password="123456")

s.run('db = database("dfs://valuedb")')

# 方法 1：使用 CREATE TABLE 语句
s.run('''
    CREATE TABLE "dfs://valuedb"."instruments"(
        sym SYMBOL,
        name STRING,
        industry STRING,
        market SYMBOL
    )
    sortColumns=`sym
''')

# 方法 2：使用 createDimensionTable() 函数
s.run('''
    schema = table(1:0, `sym`name`industry`market, [SYMBOL,STRING,STRING,SYMBOL])
    dt = createDimensionTable(
        dbHandle=db, 
        table=schema, 
        tableName=`instruments, 
        sortColumns=`sym
    )
''')

s.close()
```

#### 3.3 创建内存表

```python
import dolphindb as ddb

s = ddb.session()
s.connect(host="localhost", port=8848, userid="admin", password="123456")

# 方法 1：使用 CREATE LOCAL TEMPORARY TABLE 语句
s.run('''
    CREATE LOCAL TEMPORARY TABLE t(
        col1 INT,
        col2 DOUBLE,
        col3 STRING
    )
''')

# 方法 2：使用 table() 函数创建空表
s.run('t = table(1:0, `col1`col2`col3, [INT,DOUBLE,STRING])')

# 方法 3：使用 table() 函数创建含数据的表
s.run('t = table(1 2 3 as col1, 1.1 2.2 3.3 as col2, `A`B`C as col3)')

# 方法 4：创建流数据表
s.run('''
    share streamTable(10000:0, `time`sym`price`volume, [TIMESTAMP,SYMBOL,DOUBLE,LONG]) as tickStream
''')

s.close()
```

---

### 四、插入数据

```python
import dolphindb as ddb

s = ddb.session()
s.connect(host="localhost", port=8848, userid="admin", password="123456")

# 方法 1：INSERT INTO 语句 - 插入所有列
s.run('INSERT INTO stock_data VALUES (2024.01.01, 09:30:00, `AAPL, 150.5, 1000000)')

# 方法 2：INSERT INTO 语句 - 插入指定列
s.run('INSERT INTO stock_data (date, sym, price) VALUES (2024.01.01, `AAPL, 150.5)')

# 方法 3：INSERT INTO 语句 - 插入多行（逐行定义）
s.run('''
    INSERT INTO stock_data VALUES 
        (2024.01.01, 09:30:00, `AAPL, 150.5, 1000000),
        (2024.01.01, 09:31:00, `GOOG, 2800.3, 500000)
''')

# 方法 4：INSERT INTO 语句 - 插入多行（按列定义）
s.run('''
    INSERT INTO stock_data VALUES (
        [2024.01.01, 2024.01.01],
        [09:30:00, 09:31:00],
        [`AAPL, `GOOG],
        [150.5, 2800.3],
        [1000000, 500000]
    )
''')

# 方法 5：append! 函数 - 追加整个表
s.run('''
    tmp = table(
        take(2024.01.01..2024.01.10, 100) as date,
        take(09:30:00, 100) as time,
        rand(`AAPL`GOOG`MSFT, 100) as sym,
        rand(100.0, 100) as price,
        rand(1000000, 100) as volume
    )
    append!(stock_data, tmp)
''')

# 方法 6：tableInsert() 函数 - 返回插入行数
count = s.run('count = tableInsert(stock_data, tmp)')

s.close()
```

---

### 五、查询数据

```python
import dolphindb as ddb

s = ddb.session()
s.connect(host="localhost", port=8848, userid="admin", password="123456")

# 1. 基础查询
result = s.run('select * from stock_data where date=2024.01.01')

# 2. 条件过滤
result = s.run('''
    select sym, price from stock_data 
    where date between 2024.01.01:2024.01.31 
    and price > 100
''')

# 3. 聚合查询
result = s.run('''
    select sym, 
        avg(price) as avg_price, 
        sum(volume) as total_volume,
        count(*) as trade_count
    from stock_data 
    where date between 2024.01.01:2024.01.31 
    group by sym
''')

# 4. 分区裁剪（自动优化）
result = s.run('select * from stock_data where date=2024.01.01 and sym=`AAPL')

# 5. 连接查询
result = s.run('''
    select s.sym, s.price, i.name, i.industry
    from stock_data as s
    left join instruments as i on s.sym = i.sym
    where s.date=2024.01.01
''')

# 6. 时间窗口聚合
result = s.run('''
    select sym, 
        first(price) as open,
        max(price) as high,
        min(price) as low,
        last(price) as close,
        sum(volume) as volume
    from stock_data
    where time between 09:30:00:10:00:00
    group by sym, time_bar(60000, time) as minute
''')

# 转换为 pandas DataFrame
df = result.toDF()

s.close()
```

---

### 六、更新数据

```python
import dolphindb as ddb

s = ddb.session()
s.connect(host="localhost", port=8848, userid="admin", password="123456")

# 1. 条件更新
s.run('UPDATE stock_data SET price = price * 1.01 WHERE date=2024.01.01 and sym=`AAPL')

# 2. 批量更新
s.run('update stock_data set volume = volume * 2 where time < 10:00:00')

# 3. 使用表达式更新
s.run('''
    update stock_data set 
        price = price * (1 + rand(0.01, size(stock_data))),
        volume = volume * 2
    where date=2024.01.01
''')

s.close()
```

---

### 七、删除数据

```python
import dolphindb as ddb

s = ddb.session()
s.connect(host="localhost", port=8848, userid="admin", password="123456")

# 1. 删除符合条件的数据
s.run('DELETE FROM stock_data WHERE date < 2024.01.01')

# 2. 删除表
s.run('DROP TABLE "dfs://valuedb".stock_data')

# 3. 删除数据库
s.run('DROP DATABASE "dfs://valuedb"')

# 4. 删除分区
s.run('dropPartition("dfs://valuedb", `stock_data, 2024.01.01)')

# 5. 检查数据库/表是否存在
s.run('''
    if(existsDatabase("dfs://valuedb")) dropDatabase("dfs://valuedb")
    if(existsTable("dfs://valuedb", `stock_data)) dropTable("dfs://valuedb", `stock_data)
''')

s.close()
```

---

## 注意事项

### 权限要求
- **创建分布式数据库**: 需要 `DB_OWNER` 权限
- **创建分区表**: 需要 `DBOBJ_CREATE` 和 `DB_MANAGE` 权限
- **默认管理员账号**: admin / 123456
- **查看权限**: `getUserAccess()` 函数

### 分区设计最佳实践
- **分区大小**: 建议每个分区 100MB-1GB
- **分区类型选择**:
  - VALUE: 适合离散值（如日期、类别）
  - RANGE: 适合连续值范围
  - HASH: 适合均匀分布数据
  - LIST: 适合预定义列表
  - COMPO: 多维度组合（最多 3 维）
- **量化金融场景**: 常用时间（DATE）和产品标识（SYMBOL）作为分区维度

### 数据插入限制
- **STRING 类型**: 单条不超过 64KB（超出部分截断）
- **BLOB 类型**: 单条不超过 64MB（超出部分截断）
- **SYMBOL 类型**: 单条不超过 255B（超出时报错）
- **VALUE 分区**: STRING/SYMBOL 列不能包含空格、`\n`、`\r`、`\t`

### 事务原子性
- **TRANS 级别**: 全部分区成功或全部失败（强一致性）
- **CHUNK 级别**: 允许部分分区写入，冲突时重试（高可用性）

### 存储引擎选择
- **TSDB**: 时序数据，支持高效时间范围查询
- **OLAP**: 分析型数据，适合复杂聚合查询
- **PKEY**: 主键查询场景

---

## 参考文档

- **DolphinDB 官网**: https://www.dolphindb.cn/
- **DolphinDB 文档中心**: https://docs.dolphindb.cn/zh/
- **建库建表**: https://docs.dolphindb.cn/zh/db_distr_comp/db_oper/create_db_tb.html
- **插入数据**: https://docs.dolphindb.cn/zh/db_distr_comp/db_oper/insert_data.html
- **查询数据**: https://docs.dolphindb.cn/zh/db_distr_comp/db_oper/queries.html
- **更新数据**: https://docs.dolphindb.cn/zh/db_distr_comp/mod_data.html
- **删除数据**: https://docs.dolphindb.cn/zh/db_distr_comp/db_oper/drop_db_tb.html
- **数据库配置**: https://docs.dolphindb.cn/zh/db_distr_comp/cfg/function_configuration.html
- **存储引擎**: https://docs.dolphindb.cn/zh/db_distr_comp/db/tsdb.html

---

## 相关技能

- **dolphindb-skills**: 技能套件索引（含环境检测）
- **dolphindb-quant-finance**: 量化金融场景（因子计算、策略回测、绩效归因）
- **dolphindb-streaming**: 流式计算（实时因子、实时行情、实时风控）
- **dolphindb-docker**: Docker 容器化部署
