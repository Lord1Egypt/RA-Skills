# 数据开发平台公约

官网：https://sf.163.com/product/bp
平台文档手册：https://study.sf.163.com/documents/read/service_support/dsc-p-00

> 本文件描述 EasyData 平台具备的能力和功能规范，包括平台支持什么、平台如何配置、平台接口规范等。
> 团队如何使用这些能力（技术栈选型、代码模板、流程约定）请参阅 `project-conventions.md`。

---

## 目录

1. [平台概述](#1-平台概述)
2. [技术栈](#2-技术栈)
3. [存储格式支持](#3-存储格式支持)
4. [数据分层与生命周期配置能力](#4-数据分层与生命周期配置能力)
5. [TBLPROPERTIES 平台解析字段](#5-tblproperties-平台解析字段)
6. [任务节点 conf 参数配置能力](#6-任务节点-conf-参数配置能力)
7. [Azkaban 调度配置](#7-azkaban-调度配置)
8. [元数据 OpenAPI](#8-元数据-openapi)
9. [数据开发流程](#9-数据开发流程)
10. [权限与安全](#10-权限与安全)

---

## 1. 平台概述

网易大数据平台（EasyData，对外品牌名 BP）是网易自研的一站式大数据开发与治理平台，提供数据集成、离线开发、实时计算、数据质量、数据服务、元数据管理等全链路能力，主要面向企业内部数仓团队使用。

---

## 2. 技术栈

| 组件 | 版本 / 说明 |
|------|-------------|
| 计算引擎 | Hive 2.x / 3.x（离线批处理）、Spark 2.4 / 3.x（大规模 ETL） |
| 底层存储 | HDFS（Hadoop Distributed File System） |
| 资源调度 | Yarn |
| 协调服务 | Zookeeper |
| 消息队列 | Kafka（实时数据接入） |
| NoSQL 存储 | HBase（高并发点查场景） |
| 调度系统 | Azkaban（离线任务编排） |
| 元数据管理 | 平台自研元数据中心，提供 OpenAPI |

---

## 3. 存储格式支持

平台支持以下存储格式，可在建表 DDL 中通过 `ROW FORMAT SERDE` / `STORED AS` 指定：

| 格式 | 说明 |
|------|------|
| **ORC** | 支持 ACID 事务、谓词下推，压缩算法可选 SNAPPY / ZLIB |
| **Parquet** | 与 Spark 生态兼容性最佳，适合列式计算场景 |
| **TextFile** | 纯文本格式，便于问题排查，不压缩或使用 GZIP |
| **Iceberg** | 平台支持 Apache Iceberg 表格式，提供 ACID 事务、时间旅行、增量读取等能力 |

> 各分层实际使用何种格式由团队约定决定，见 `project-conventions.md` 第3节。

---

## 4. 数据分层与生命周期配置能力

平台支持以下数据分层体系，团队可根据业务需求选择适合的分层方式：

| 分层 | 全称 | 典型定位 |
|------|------|----------|
| ODS | 原始贴源层 | 1:1 同步源系统 |
| DWD | 明细层 | 清洗后的明细事实 |
| DWS | 汇总层 | 按主题聚合 |
| ADS/DM | 应用层/数据集市层 | 面向报表/API 输出 |

**生命周期配置能力**

平台支持在表级别配置生命周期，通过 `TBLPROPERTIES` 中的以下字段控制（详见第5节）：

- **表级生命周期**：`LIFECYCLE`，超过指定天数的表数据自动清理
- **分区级生命周期**：`PARTITION_LIFECYCLE`，超过指定天数的分区自动清理

> 各分层实际生命周期约定见 `project-conventions.md` 第4节。

---

## 5. TBLPROPERTIES 平台解析字段

以下字段由 EasyData 平台元数据系统解析和使用：

| 字段 | 说明 | 示例值 |
|------|------|--------|
| `metahub.table.primary` | 主键字段设置，平台元数据中心使用 | `'order_id'` |
| `SYNC_METASTORE` | 是否开启 Impala 元数据同步 | `'OFF'` / `'ON'` |
| `LIFECYCLE` | 表级生命周期，单位为天（`d`） | `'7d'`（永久保留时不填） |
| `PARTITION_LIFECYCLE` | 分区级生命周期，单位为天（`d`） | `'7d'`（永久保留时不填） |

> 其他元数据字段（mammut.table.owner、table.creator 等）由平台根据执行人自动填写，无需在 DDL 中手动指定。

---

## 6. 任务节点 conf 参数配置能力

EasyData 平台任务节点支持在节点配置界面设置 conf 参数，格式为：

```
conf.参数名 参数值
```

平台会在任务执行时将这些参数注入到 Hive/Spark 执行环境，等效于在 SQL 脚本中执行 `SET 参数名=参数值`。

> 团队约定通过 conf 配置项代替 SQL 脚本中的 `SET` 参数块，具体配置规范见 `project-conventions.md` 第7节。

---

## 7. Azkaban 调度配置

### .job 文件格式

Azkaban 每个任务对应一个 `.job` 文件（Java Properties 格式）。

**HiveQL 任务示例**（`dwd_trade_order_detail_di.job`）：

```properties
# 任务类型
type=command

# 依赖任务（逗号分隔，填写上游 .job 文件名不含后缀）
dependencies=ods_trade_order_di

# 执行命令
command=hive -f /data/scripts/dwd/dwd_trade_order_detail_di.sql -hivevar bizdate=${azkaban.flow.start.timestamp:0:8}

# JVM 参数（可选）
JVM_ARGS=-Xmx4g -Xms2g

# 失败重试次数
retries=1

# 超时（分钟）
timeout.mins=120
```

**Spark SQL 任务示例**（`dws_user_active_1d_df.job`）：

```properties
type=command

dependencies=dwd_trade_order_detail_di,dwd_user_login_detail_di

command=spark-submit \
  --master yarn \
  --deploy-mode client \
  --driver-memory 4g \
  --executor-memory 8g \
  --executor-cores 4 \
  --num-executors 10 \
  --class com.netease.easydata.SparkSQLRunner \
  /data/jars/spark-runner.jar \
  --sql-file /data/scripts/dws/dws_user_active_1d_df.sql \
  --bizdate ${azkaban.flow.start.timestamp:0:8}

retries=1
timeout.mins=180
```

### 常用 Azkaban 内置变量

| 变量 | 说明 | 示例值 |
|------|------|--------|
| `${azkaban.flow.start.timestamp}` | 计划执行时间的具体时间 | `2018-08-21T15:23:15.075+08:00` |
| `${azkaban.flow.start.year}` | 计划执行时间的年 | `2018` |
| `${azkaban.flow.start.month}` | 计划执行时间的月 | `08` |
| `${azkaban.flow.start.day}` | 计划执行时间的日 | `21` |
| `${azkaban.flow.start.hour}` | 计划执行时间的小时 | `15` |
| `${azkaban.flow.start.minute}` | 计划执行时间的分钟 | `23` |
| `${azkaban.flow.start.second}` | 计划执行时间的秒 | `15` |
| `${azkaban.flow.start.milliseconds}` | 计划执行时间的毫秒 | `075` |
| `${azkaban.flow.start.timezone}` | 计划执行时间的时区 | `Asia/Shanghai` |
| `${azkaban.flow.current.date}` | 计划执行时间日期 | `2018-08-21` |
| `${azkaban.flow.current.month}` | 计划执行时间所在月开始1号 | `2019-08-01` |
| `${azkaban.flow.current.hour}` | 计划执行时间所在小时的0分0秒 | `2018-08-21 15:00:00` |
| `${azkaban.flow.1.days.ago}` | 计划执行时间一天前日期 | `2018-08-20` |
| `${azkaban.flow.2.days.ago}` | 计划执行时间两天前日期 | `2018-08-19` |
| `${azkaban.flow.3.days.ago}` | 计划执行时间三天前日期 | `2018-08-18` |
| `${azkaban.flow.7.days.ago}` | 计划执行时间的七天前日期 | `2018-08-14` |
| `${azkaban.flow.30.days.ago}` | 计划执行时间的三十天前日期 | `2018-07-22` |
| `${schedule.exec.time}` | 计划执行时间的unix时间戳 | `1534839814392` |
| `${azkaban.flow.current.date.simple}` | 计划执行时间当前日期 | `20230328` |

> 具体参考：https://study.sf.163.com/documents/read/service_support/dsc-p-a-0176

### 调度配置规范要点

- `type` 优先使用 `command`，不使用平台已废弃的 `hive`/`spark` 类型
- `dependencies` 必须声明所有直接上游任务，不可遗漏
- 脚本路径使用绝对路径，统一存放在 `/data/scripts/{分层}/` 目录
- 超时时间根据历史运行时长设置，建议为 P99 耗时的 2 倍
- 生产任务必须设置 `retries=1`（最多重试 1 次）

---

## 8. 元数据 OpenAPI

### 鉴权方式：AK/SK

```
Authorization: AK {AccessKey}:{Signature}
```

- **AccessKey**：在 EasyData 平台「个人中心 → API 密钥」获取
- **Signature**：使用 HMAC-SHA256 算法对请求体签名
  - 签名字符串 = `HTTP方法\n请求路径\n时间戳\nMD5(RequestBody)`
  - 请求头同时携带 `X-Timestamp: {Unix秒级时间戳}`

### 常用接口

| 接口 | 路径 | 说明 |
|------|------|------|
| 查询库列表 | `GET /api/v1/databases` | 返回当前租户所有数据库 |
| 查询表列表 | `GET /api/v1/tables?db={dbName}` | 返回指定库的表列表 |
| 查询表详情 | `GET /api/v1/tables/{dbName}/{tableName}` | 含建表 DDL、分区信息、存储大小 |
| 查询字段列表 | `GET /api/v1/columns?db={dbName}&table={tableName}` | 返回字段名、类型、注释 |
| 搜索表 | `GET /api/v1/search?keyword={keyword}&type=table` | 按关键词模糊搜索表 |

### 返回字段示例（`/api/v1/columns`）

```json
{
  "code": 0,
  "data": [
    {
      "columnName": "order_id",
      "dataType": "BIGINT",
      "comment": "订单ID",
      "isPartition": false,
      "isNullable": true
    }
  ]
}
```

---

## 9. 数据开发流程

```
数据源接入（DataHub）
     ↓
离线开发（任务编排 + SQL 开发）
     ↓
数据质量（规则配置 + 告警）
     ↓
数据服务（API 发布 + 权限管理）
```

| 环节 | 平台模块 | 关键操作 |
|------|----------|----------|
| 数据源接入 | DataHub | 配置数据源连接、选择同步方式（全量/增量/CDC）、映射目标表 |
| 离线开发 | 任务开发 | 创建 Hive/Spark SQL 任务、配置调度周期、绑定 Azkaban Flow |
| 数据质量 | 数据质量 | 配置字段非空规则、主键唯一规则、行数波动规则；触发告警阈值 |
| 数据服务 | 数据服务 | 将 DM 层表发布为 API，配置 QPS 限流和访问白名单 |

---

## 10. 权限与安全

### 库表权限申请

1. 在 EasyData「权限中心」提交申请，填写目标库/表、权限类型（只读 / 读写）、申请理由
2. 由表 Owner 审批，审批通过后权限自动生效
3. 跨业务域访问需额外提交安全合规审批

### 列级脱敏规则

| 数据类型 | 脱敏规则 | 示例 |
|----------|----------|------|
| 手机号 | 保留前 3 位和后 4 位，中间替换为 `****` | `138****5678` |
| 身份证号 | 保留前 6 位和后 4 位，中间替换为 `********` | `330102********1234` |
| 姓名 | 保留姓（第一个字），其余替换为 `*` | `张*` |
| 邮箱 | `@` 前保留前 3 字符，其余替换为 `***` | `abc***@example.com` |

### 数据分级标签

| 级别 | 标签 | 说明 |
|------|------|------|
| L1 | 公开 | 无敏感信息，可对外共享 |
| L2 | 内部 | 仅限公司内部使用 |
| L3 | 敏感 | 含个人信息，需脱敏后使用 |
| L4 | 机密 | 含核心商业数据，严格管控 |

> 生成 DDL 时，若字段涉及个人信息（手机号、身份证、姓名等），需在字段 `COMMENT` 中注明脱敏规则。
