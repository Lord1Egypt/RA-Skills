# task.md 标准模板

> **文档职责**：task = 可执行落地（DDL/ETL 代码、调度配置，直接可运行）。
> **输入依赖**：以 spec.md（做什么）和 plan.md（怎么做）为输入，每个任务单元须可追溯至 spec 条目编号。
> 本文件由 Phase 6 执行阶段生成，每个 task 为完全自包含的执行单元，无需 spec.md、plan.md 或 conventions 文件的上下文即可直接执行。
> task 是 plan.md 实现要点与 conventions 应用决策的具体落地：plan 中确定的 JOIN 逻辑、过滤条件、命名规则、存储格式、参数档位等须硬编码到代码中。

---

## 文件头部信息

```yaml
生成时间: YYYY-MM-DD HH:mm
依据 spec 版本: spec.md（最后确认时间 YYYY-MM-DD）
依据 plan 版本: plan.md（最后确认时间 YYYY-MM-DD）
依据 conventions 版本: project-conventions.md vX.X / platform-conventions.md vX.X（或注明日期）
总任务数: N
```

---

## Task 单元模板

以下为单个 task 的标准结构，按需重复。

---

### TASK-{编号}：{任务名称}

```yaml
task_id: TASK-001
title: "（简短描述，如：创建 DWD 层用户行为宽表 DDL）"
spec_ref: "（对应 spec.md 中的条目编号，如 spec#4.2，确保可追溯）"
plan_ref: "（对应 plan.md 中的任务编号，如 plan#T-03）"
conventions_ref: "（来自 plan.md 对应行的 conventions 应用决策，如：表名前缀 dwd_，ORC+SNAPPY，executor×10/4g，按 p_date 分区）"
impl_ref: "（来自 plan.md 对应行的实现要点，如：INNER JOIN user_info on user_id，过滤 status='completed'，按 dt 去重取最新）"
depends_on:
  - TASK-000   # 前置任务编号，无依赖时填 []
type: "DDL | ETL | SCHEDULE | DQ"  # 任务类型
```

#### 任务描述

简要说明本 task 做什么、为什么做，业务背景一句话概括（对应 spec#{ 条目}）。

#### 完整可执行代码

> ⚠️ conventions 参数（表名前缀、存储格式、Spark 资源参数等）和 plan 实现要点（JOIN 逻辑、过滤条件等）必须内联到代码中，不得以「参见 conventions」或「参见 plan」替代。
> 调度运行时变量（如 `${bizdate}`）允许保留为占位符，由调度系统（Azkaban）在运行时注入。

**（DDL 示例）**

```sql
-- 创建 DWD 层用户行为宽表
-- spec_ref: spec#4.2，plan_ref: plan#T-03
-- conventions: project-conventions v1.2，ORC+SNAPPY，按 p_date 分区
CREATE TABLE IF NOT EXISTS dwd.dwd_user_behavior_wide_di
(
    user_id        STRING    COMMENT '用户ID',
    event_type     STRING    COMMENT '行为类型：click/exposure/purchase',
    item_id        STRING    COMMENT '商品ID',
    page_id        STRING    COMMENT '页面ID',
    dt             STRING    COMMENT '业务日期，格式 yyyyMMdd',
    ts             BIGINT    COMMENT '事件时间戳（毫秒）'
)
COMMENT 'DWD层用户行为宽表，每日全量'
PARTITIONED BY (p_date STRING COMMENT '分区日期，格式 yyyyMMdd')
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\001'
STORED AS ORC
TBLPROPERTIES (
    'orc.compress' = 'SNAPPY',
    'transactional' = 'false'
);
```

**（ETL SQL 示例）**

```sql
-- ETL：从 ODS 层抽取并加工为 DWD 宽表
-- spec_ref: spec#5.2（数据范围：前一日 click/exposure/purchase 事件，user_id 不为空）
-- plan_ref: plan#T-03（实现要点：过滤 event_type IN (...)，过滤 user_id IS NOT NULL）
-- conventions: platform-conventions v2.0，executor×10/4g/2core，队列 queue_dw_prod
SET spark.executor.instances=10;
SET spark.executor.memory=4g;
SET spark.executor.cores=2;
SET spark.sql.shuffle.partitions=200;
SET hive.exec.dynamic.partition=true;
SET hive.exec.dynamic.partition.mode=nonstrict;

INSERT OVERWRITE TABLE dwd.dwd_user_behavior_wide_di
PARTITION (p_date='${bizdate}')
SELECT
    user_id,
    event_type,
    item_id,
    page_id,
    dt,
    ts
FROM ods.ods_app_event_log_di
WHERE p_date = '${bizdate}'
  AND event_type IN ('click', 'exposure', 'purchase')
  AND user_id IS NOT NULL;
```

**（Azkaban 调度配置示例）**

```properties
# dwd_user_behavior_wide_di.job
type=command
command=bash /data/scripts/dw/dwd/run_dwd_user_behavior_wide_di.sh ${bizdate}
dependencies=ods_app_event_log_di
retries=2
retry.backoff=10000
```

#### 异常处理

| 失败场景 | 处理方式 |
|----------|---------|
| 上游分区数据未就绪 | 等待 30 分钟后重试，最多重试 3 次；超时后告警并阻断下游 |
| SQL 执行失败（语法/权限） | 立即失败，不重试；检查 Spark 日志定位错误行 |
| 目标分区已存在 | 使用 `INSERT OVERWRITE` 覆盖，确保幂等性 |
| 输出行数为 0 | 触发告警，不阻断流程，需人工核查 |

#### 验收标准（DoD）

```sql
-- 验收检查 SQL，在任务完成后执行
-- 对应 spec#6.4 业务验收标准的技术实现

-- 1. 分区存在性检查
SHOW PARTITIONS dwd.dwd_user_behavior_wide_di
PARTITION (p_date='${bizdate}');
-- 期望：返回至少 1 条分区记录

-- 2. 行数断言（与上游 ODS 行数比值应在 [0.9, 1.1]）
SELECT
    ods_cnt,
    dwd_cnt,
    dwd_cnt / ods_cnt AS ratio
FROM (
    SELECT COUNT(1) AS ods_cnt FROM ods.ods_app_event_log_di
    WHERE p_date = '${bizdate}' AND event_type IN ('click','exposure','purchase')
) a,
(
    SELECT COUNT(1) AS dwd_cnt FROM dwd.dwd_user_behavior_wide_di
    WHERE p_date = '${bizdate}'
) b;
-- 期望：ratio 在 0.9 到 1.1 之间

-- 3. 关键字段非空检查
SELECT COUNT(1) AS null_user_cnt
FROM dwd.dwd_user_behavior_wide_di
WHERE p_date = '${bizdate}'
  AND user_id IS NULL;
-- 期望：null_user_cnt = 0
```

---

## 多 Task 文件索引（任务数 > 10 时拆分）

| 文件 | 包含任务 | 说明 |
|------|----------|------|
| `task-ods.md` | TASK-001 ~ TASK-003 | ODS 层建表与同步任务 |
| `task-dwd.md` | TASK-004 ~ TASK-008 | DWD 层清洗与宽表任务 |
| `task-dws.md` | TASK-009 ~ TASK-012 | DWS 层汇总指标任务 |
| `task-ads.md` | TASK-013 ~ TASK-015 | ADS 层应用层输出任务 |

---

## 注意事项

- **conventions 参数必须内联**：表名前缀、存储格式、Spark 资源参数等须硬编码到代码，不得引用外部文件
- **plan 实现要点必须内联**：JOIN 逻辑、过滤条件等须体现在实际 SQL 中，不得以「参见 plan」替代
- **调度运行时变量允许保留占位符**：`${bizdate}` 等变量由 Azkaban 在运行时注入，task 文件本身无需解析
- DDL 幂等性：使用 `CREATE TABLE IF NOT EXISTS`
- ETL 幂等性：使用 `INSERT OVERWRITE`
- 若后续 conventions 更新，需重新生成对应 task