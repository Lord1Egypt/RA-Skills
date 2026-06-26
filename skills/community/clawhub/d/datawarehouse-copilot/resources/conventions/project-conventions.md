# 项目自定义公约

> 本文件记录本项目数据开发团队的约定和规范，包括技术栈选型、代码编写规范、流程约定等。
> 维护责任：数仓开发团队，规范变更时同步更新本文件。

---

## 目录

1. [项目技术栈](#1-项目技术栈)
2. [数据分层规范](#2-数据分层规范)
3. [存储格式规范](#3-存储格式规范)
4. [生命周期约定](#4-生命周期约定)
5. [DDL 标准模板](#5-ddl-标准模板)
6. [Spark SQL 代码模板](#6-spark-sql-代码模板)
7. [platform 任务 conf 参数配置](#7-platform-任务-conf-参数配置)
8. [版本管理规范](#8-版本管理规范)
9. [测试规范](#9-测试规范)
10. [上线流程](#10-上线流程)

---

## 1. 项目技术栈

| 组件 | 说明 |
|------|------|
| 表格式 | Apache Iceberg（ods层）Apache Hive（dim、dw、dm层）|
| 计算引擎 | Hive / Spark |
| 数据集成 | DataX |
| 数据服务层存储 | Apache Doris 、MySQL|
| 调度系统 | Azkaban（通过 platform 平台管理） |

---

## 2. 数据分层规范

```
ODS → DWD → DWS → DM
```

| 分层 | 全称 | 定位 | 命名前缀 | 分区字段 |
|------|------|------|----------|----------|
| ODS | 原始贴源层 | 1:1 同步源系统，不做业务加工 | `ods_` | `ds STRING` |
| DWD | 明细层 | 清洗、脱敏、维度退化后的明细事实 | `dwd_` | `ds STRING` |
| DWS | 汇总层 | 按主题聚合的宽表/汇总指标 | `dws_` | `ds STRING` |
| DM | 数据集市层 | 面向报表/API 的最终输出（对应其他项目的 ADS 层） | `dm_` | 按需 |

**分区约定**
- 分区字段统一使用 `ds STRING`，含义为业务日期/快照日期，格式 `yyyy-MM-dd` `2026-01-01`

**库命名规范**：`{业务域}_{分层}`，如 `trade_ods`、`user_dwd`

**表命名规范**：`{分层前缀}_{业务域}_{主题}_{粒度}_{周期后缀}`

| 周期后缀 | 含义 |
|----------|------|
| `i` | 每日增量（Daily Increment） |
| `p` | 每日全量（Daily Full） |
| `h` | 每小时 |

示例：`dwd_trade_order_detail_d`、`dws_user_active_1d_p`

**任务命名**：与产出表名保持一致。一个任务产出一个模型。禁止一个任务产出多个模型

---

## 3. 存储格式规范

| 分层 | 存储格式 | 说明 |
|------|----------|------|
| ODS | Iceberg + Parquet | 使用 Iceberg 表格式，底层存储为 Parquet |
| DWD | Hive + Parquet | 存储在HDFS上 |
| DWS | Hive + Parquet | 存储在HDFS上 |
| DM | Hive + Parquet/ORC | 存储在HDFS上 Parquet/ORC 格式 |

> dw 层（DIM/DWD/DWS）统一使用 Parquet 存储，DM 层使用 Parquet/ORC 存储。

---

## 4. 生命周期约定

本项目所有分层数据均设置为**永久保留**，不设自动过期。

| 分层 | 生命周期 |
|------|----------|
| ODS | 永久 |
| DIM | 永久 |
| DWD | 永久 |
| DWS | 永久 |
| DM | 永久 |

> 如有特殊需要，可在 DDL 的 `TBLPROPERTIES` 中单独设置 `LIFECYCLE` 或 `PARTITION_LIFECYCLE`（见第5节模板注释）。

---

## 5. DDL 标准模板

以下为标准建表 DDL 模板（dw 层 Parquet 格式）：

```sql
-- DROP TABLE IF EXISTS `db`.`table`;
CREATE TABLE IF NOT EXISTS `db`.`table`(
  `string_col`  string  COMMENT '',
  `double_col`  double  COMMENT '',
  `bigint_col`  bigint  COMMENT ''
)
COMMENT ''
PARTITIONED BY (
  `ds` string COMMENT '业务日期 快照日期')
ROW FORMAT SERDE
  'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
STORED AS INPUTFORMAT
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
TBLPROPERTIES (
  'metahub.table.primary'='',     -- 主键设置
  'SYNC_METASTORE'='OFF'          -- 是否开启 Impala 同步：OFF / ON 对于直连HDFS使用impala读取的Hive表需要开启
  -- 'LIFECYCLE'='7d',            -- 表级生命周期（单位 d），永久保留时不填
  -- 'PARTITION_LIFECYCLE'='7d'   -- 分区级生命周期（单位 d），永久保留时不填
);
```

**规范要点**
- 所有字段必须有 `COMMENT`，使用中文说明业务含义
- 表级 `COMMENT` 说明表用途及数据粒度
- `PARTITIONED BY` 分区字段不出现在普通字段列表中
- `TBLPROPERTIES` 中只需指定 `metahub.table.primary` 和 `SYNC_METASTORE`，其他元数据由平台根据执行人自动填写
- 永久保留时不填 `LIFECYCLE` / `PARTITION_LIFECYCLE`（注释保留作为提示）

---

## 6. Spark SQL 代码模板

```sql
/*********************************************************************
Author: ${Author}
Comment: 业务注释信息
Version: 任务版本信息
*********************************************************************/
-- DROP TABLE IF EXISTS `db`.`table`;
-- CREATE TABLE IF NOT EXISTS `db`.`table`(
--   `string_col`  string  COMMENT '',
--   `double_col`  double  COMMENT '',
--   `bigint_col`  bigint  COMMENT ''
-- )
-- COMMENT ''
-- PARTITIONED BY (
--   `ds` string COMMENT '业务日期 快照日期')
-- ROW FORMAT SERDE
--   'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
-- STORED AS INPUTFORMAT
--   'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat'
-- OUTPUTFORMAT
--   'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
-- TBLPROPERTIES (
--   'metahub.table.primary'='',     -- 主键设置
--   'SYNC_METASTORE'='OFF'          -- 是否开启 Impala 同步：OFF / ON 对于直连HDFS使用impala读取的Hive表需要开启
--   -- 'LIFECYCLE'='7d',            -- 表级生命周期（单位 d），永久保留时不填
--   -- 'PARTITION_LIFECYCLE'='7d'   -- 分区级生命周期（单位 d），永久保留时不填
-- );

INSERT OVERWRITE TABLE `db`.`table` PARTITION (ds)
SELECT string_col
  
FROM   `db`.`table`
WHERE  1 = 1
DISTRIBUTE BY 1
;
```

**规范要点**
- 文件顶部必须包含头部注释块（Author / Comment / Version）
- DDL 语句以注释形式保留在SQL节点中，便于追溯表结构
- 分区写入统一使用 `INSERT OVERWRITE`，特殊情况使用 `INSERT INTO`（避免数据重复）
- 分区字段 `ds` 放在 SELECT 最后一列（动态分区规范）
- 禁止在 ETL 中硬编码日期，所有日期通过调度参数 Azkaban 变量传入
- 禁止使用 `SELECT *`，写入时明确列出所有字段

---

## 7. platform 任务 conf 参数配置

本项目不在 SQL 脚本中写 `SET` 参数块，而是统一在 platform 平台参数组 或 任务节点的 conf 配置项中设置。

**参数组**：可以引用在任务或节点上的参数文件
平台地址：/activity/publicResource/paramGroup

**配置形式**：`conf.参数名 参数值`（每行一个）

**动态分区常用配置示例**：

```
conf.hive.exec.dynamic.partition true
conf.hive.exec.dynamic.partition.mode nonstrict
conf.hive.exec.max.dynamic.partitions 10000
conf.hive.exec.max.dynamic.partitions.pernode 1000
```

> 优先学习并使用参数组，若需要新增 conf 参数的场景，不确定参数名或配置方式，主动询问用户确认后补充至本节。

---

## 8. 版本管理规范

- 任务每次修改**必须**填写版本备注，记录修改内容和变更原因
- 版本备注在提交上线时填写（见第10节上线流程）
- 版本信息同步更新至 SQL 脚本头部注释块的 `Version` 字段

---

## 9. 测试规范

- **非管理员角色**用户：上线前必须在**开发模式**下测试通过，方可提交上线
- 管理员角色：建议同样在开发模式验证，确保数据正确性

---

## 10. 上线流程

```
1. 开发/修改代码
     ↓
2. 开发模式运行任务/节点（验证逻辑正确性）
     ↓
3. 检查/更新调度设置（周期、依赖、触发时间等）
     ↓
4. 检查/更新报警设置（失败告警、超时告警等）
     ↓
5. 提交上线并编写版本备注（记录本次修改内容和变更原因）
```
