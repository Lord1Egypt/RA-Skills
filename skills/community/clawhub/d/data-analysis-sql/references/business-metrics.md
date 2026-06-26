# business-metrics.md — 业务指标 SQL 设计模式

> 通用指标设计规范，SQL 示例均使用占位符，不含具体表名或字段名
> 适用引擎：PostgreSQL（部分 Druid/Flink SQL 需调整语法）

---

## 一、指标设计标准流程

写任何指标 SQL 前，必须先澄清以下问题：

| # | 问题 | 目的 |
|---|------|------|
| 1 | 指标定义是什么？ | 明确分子分母、口径 |
| 2 | 时间口径是什么？ | 按创建时间？完成时间？统计日期？ |
| 3 | 排除逻辑是什么？ | 排除取消/无效/免测等特殊状态 |
| 4 | 数据源是哪张表？ | 主表 + 关联表 |
| 5 | 有哪些关联维度？ | 租户/项目/系统/工作空间 |
| 6 | 上线/完成状态怎么判定？ | 状态枚举值是什么 |
| 7 | 有哪些常见枚举值？ | 提前整理，避免运行时报错 |

---

## 二、交付准时率

**指标定义：**
- 分子：准时交付数量（实际完成时间 ≤ 计划完成时间）
- 分母：已交付数量（首次变更为已完成状态，且非取消）

**关联链路：**
```
主事项表（按事项类型过滤）
    └── 变更记录表（operation='transition'）
            └── 状态表（type='Finished', name<>'取消'）
```

**按租户维度模板：**

```sql
WITH
-- Step1：取目标事项（按类型过滤）
base_items AS (
    SELECT
        t."tenantkey",
        t."objectid",
        t."key",
        -- 计划完成时间（兼容毫秒时间戳字符串）
        CASE
            WHEN t."{planned_end_field}" ~ '^\d{10,13}$'
            THEN to_timestamp(CAST(t."{planned_end_field}" AS BIGINT) / 1000.0)
            WHEN t."{planned_end_field}" ~ '^\d{4}-\d{2}-\d{2}'
            THEN t."{planned_end_field}"::timestamp
            ELSE NULL
        END AS planned_finish_ts
    FROM {schema}."{item_table}" t
    WHERE t."{type_field}" = '{target_type}'
      AND t."tenantkey" IS NOT NULL
),
-- Step2：取首次完成时间（排除取消状态）
finished_status AS (
    SELECT
        t."tenantkey",
        t."objectid",
        MIN(cl."{update_time_field}") AS actual_finish_ts
    FROM {schema}."{item_table}" t
    INNER JOIN {schema}."{change_log_table}" cl
        ON t."objectid"  = cl."{item_fk_field}"
       AND t."tenantkey" = cl."tenantkey"
       AND cl."{operation_field}" = '{transition_value}'
    INNER JOIN {schema}."{status_table}" ms
        ON cl."{status_to_field}" = ms."objectid"
       AND t."tenantkey"           = ms."tenantkey"
       AND ms."{status_type_field}" = '{finished_type}'
       AND ms."{status_name_field}" <> '{cancel_name}'
    WHERE t."{type_field}" = '{target_type}'
    GROUP BY t."tenantkey", t."objectid"
),
-- Step3：判断是否准时
delivery_check AS (
    SELECT
        b."tenantkey",
        b."objectid",
        b."planned_finish_ts",
        fs."actual_finish_ts",
        CASE
            WHEN fs."actual_finish_ts" IS NOT NULL
             AND fs."actual_finish_ts" <= b."planned_finish_ts"
            THEN 1 ELSE 0
        END AS is_ontime
    FROM base_items b
    LEFT JOIN finished_status fs
        ON b."tenantkey" = fs."tenantkey"
       AND b."objectid"  = fs."objectid"
)
-- Step4：汇总
SELECT
    dc."tenantkey"                                                     AS tenant_key,
    DATE(dc."actual_finish_ts")                                        AS bizdate,
    COUNT(DISTINCT dc."objectid")                                      AS total_cnt,
    COUNT(DISTINCT CASE WHEN dc."actual_finish_ts" IS NOT NULL
             THEN dc."objectid" END)                                   AS delivered_cnt,
    COUNT(DISTINCT CASE WHEN dc."is_ontime" = 1
             THEN dc."objectid" END)                                   AS ontime_cnt,
    ROUND(
        COUNT(DISTINCT CASE WHEN dc."is_ontime" = 1
             THEN dc."objectid" END) * 100.0
        / NULLIF(COUNT(DISTINCT CASE WHEN dc."actual_finish_ts" IS NOT NULL
             THEN dc."objectid" END), 0)
    , 2)                                                               AS ontime_rate_pct
FROM delivery_check dc
WHERE dc."actual_finish_ts" IS NOT NULL
GROUP BY dc."tenantkey", DATE(dc."actual_finish_ts")
ORDER BY dc."tenantkey", bizdate DESC;
```

**按项目维度扩展：**
在 `base_items` 中加 LEFT JOIN 自定义字段表取项目名，`project_name` 一路传递到最终 GROUP BY。

---

## 三、Flow Time（平均交付时长）

**指标定义：**
- 口径：本月已交付事项，从创建到完成的平均天数
- 计算：实际完成时间 - 创建时间（天数）

```sql
WITH
base_items AS (
    SELECT
        t."tenantkey",
        t."objectid",
        t."{create_time_field}"
    FROM {schema}."{item_table}" t
    WHERE t."{type_field}" = '{target_type}'
      AND t."tenantkey" IS NOT NULL
),
finished_status AS (
    -- 同交付准时率 Step2，取首次完成时间
    ...
),
flow_calc AS (
    SELECT
        b."tenantkey",
        b."objectid",
        b."{create_time_field}",
        fs."actual_finish_ts",
        -- 计算天数差
        EXTRACT(EPOCH FROM (fs."actual_finish_ts" - b."{create_time_field}")) / 86400.0 AS flow_time_days,
        -- 标记是否当月完成
        CASE
            WHEN DATE(fs."actual_finish_ts") >= DATE_TRUNC('month', CURRENT_DATE)
             AND DATE(fs."actual_finish_ts") <  DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '1 month'
            THEN 1 ELSE 0
        END AS is_current_month
    FROM base_items b
    INNER JOIN finished_status fs
        ON b."tenantkey" = fs."tenantkey"
       AND b."objectid"  = fs."objectid"
)
SELECT
    fc."tenantkey"                                                     AS tenant_key,
    DATE_TRUNC('month', fc."actual_finish_ts")::DATE                  AS stat_month,
    COUNT(DISTINCT fc."objectid")                                      AS delivered_cnt,
    ROUND(AVG(fc."flow_time_days") FILTER (WHERE fc."flow_time_days" >= 0), 1)
                                                                       AS flow_time_avg_days
FROM flow_calc fc
WHERE fc."is_current_month" = 1
  AND fc."flow_time_days" IS NOT NULL
  AND fc."flow_time_days" >= 0
GROUP BY fc."tenantkey", DATE_TRUNC('month', fc."actual_finish_ts")::DATE
ORDER BY stat_month DESC, fc."tenantkey";
```

---

## 四、缺陷密度

**指标定义：**
- 口径：已交付事项中，平均每个事项关联的缺陷数量
- 链路：主事项 → 用例关联表 → 执行记录表 → 缺陷关联表

**关联链路：**
```
主事项表（按类型过滤，已完成）
    └── 用例-事项关联表（foreign_key = item.key）
            └── 用例执行记录表（case_id）
                    └── 缺陷-用例关联表（exec_id → defect_id）
```

> ⚠️ 注意：用例关联表的外键关联的是主事项的 `key` 字段，不是 `objectid`

```sql
WITH
base_items AS (
    -- 取已完成的目标事项
    ...
),
finished_status AS (
    -- 取首次完成时间（同交付准时率 Step2）
    ...
),
item_case AS (
    -- 事项关联用例（注意：用 item.key 关联，不是 objectid）
    SELECT DISTINCT
        b."tenantkey",
        b."objectid"          AS item_id,
        fs."actual_finish_ts",
        rel."{case_id_field}"
    FROM base_items b
    INNER JOIN finished_status fs
        ON b."tenantkey" = fs."tenantkey"
       AND b."objectid"  = fs."objectid"
    INNER JOIN {schema}."{case_item_rel_table}" rel
        ON b."{key_field}" = rel."{item_fk_field}"   -- 用 key 关联
       AND rel."del_flag" = 0
),
case_defect AS (
    -- 用例关联缺陷（通过执行记录中转）
    SELECT DISTINCT
        ic."tenantkey",
        ic."item_id",
        ic."actual_finish_ts",
        dcr."{defect_id_field}"
    FROM item_case ic
    INNER JOIN {schema}."{exec_table}" ce
        ON ce."{case_id_field}" = ic."{case_id_field}"
    INNER JOIN {schema}."{defect_case_rel_table}" dcr
        ON ce."{exec_id_field}" = dcr."{case_id_field}"
       AND dcr."del_flag" = 0
),
defect_by_item AS (
    SELECT
        cd."tenantkey",
        cd."item_id",
        MAX(cd."actual_finish_ts")         AS actual_finish_ts,
        COUNT(DISTINCT cd."{defect_id_field}") AS defect_cnt
    FROM case_defect cd
    GROUP BY cd."tenantkey", cd."item_id"
)
SELECT
    dr."tenantkey"                                                     AS tenant_key,
    DATE_TRUNC('month', dr."actual_finish_ts")::DATE                  AS stat_month,
    COUNT(DISTINCT dr."item_id")                                       AS delivered_cnt,
    SUM(dr."defect_cnt")                                               AS total_defect_cnt,
    ROUND(
        SUM(dr."defect_cnt") * 1.0
        / NULLIF(COUNT(DISTINCT dr."item_id"), 0)
    , 2)                                                               AS defect_density
FROM defect_by_item dr
WHERE dr."actual_finish_ts" IS NOT NULL
GROUP BY dr."tenantkey", DATE_TRUNC('month', dr."actual_finish_ts")::DATE
ORDER BY stat_month DESC, dr."tenantkey";
```

---

## 五、用例通过率

**指标定义：**
- 分子：最新执行状态为"通过"的用例数
- 分母：最新执行状态在"已执行（不含免测）"范围内的用例数

**状态分类（需根据实际枚举值配置）：**

| 分类 | 说明 |
|------|------|
| 已执行（不含免测） | 通过、不通过、部分通过、测试受阻、无效用例、延期补测、无法测试、执行异常 等 |
| 通过 | 通过 |
| 免测 | 免测（排除在分母之外） |

> 具体枚举值请查阅对应领域的 `enums.md`

```sql
WITH
-- Step1：取所有执行记录
exec_records AS (
    SELECT
        t."{tenant_id_field}"  AS tenantkey,
        t."{case_id_field}",
        t."{exec_result_field}",
        t."{exec_time_field}"
    FROM {schema}."{exec_table}" t
    WHERE t."del_flag" = 0
      AND t."{tenant_id_field}" IS NOT NULL
),
-- Step2：取每个用例的最新执行结果（PostgreSQL ROW_NUMBER）
latest_exec AS (
    SELECT
        t.tenantkey,
        t."{case_id_field}",
        t."{exec_result_field}" AS latest_result
    FROM (
        SELECT
            er.*,
            ROW_NUMBER() OVER (
                PARTITION BY er.tenantkey, er."{case_id_field}"
                ORDER BY er."{exec_time_field}" DESC NULLS LAST
            ) AS rn
        FROM exec_records er
    ) t
    WHERE t.rn = 1
)
-- Step3：汇总通过率
SELECT
    le.tenantkey                                                       AS tenant_key,

    -- 已执行用例数（不含免测）
    COUNT(DISTINCT CASE WHEN le.latest_result IN (
            '{executed_status_1}', '{executed_status_2}', '...'
        ) THEN le."{case_id_field}" END)                              AS executed_cnt,

    -- 通过用例数
    COUNT(DISTINCT CASE WHEN le.latest_result = '{pass_status}'
        THEN le."{case_id_field}" END)                                AS passed_cnt,

    -- 通过率
    ROUND(
        COUNT(DISTINCT CASE WHEN le.latest_result = '{pass_status}'
            THEN le."{case_id_field}" END) * 1.0
        / NULLIF(COUNT(DISTINCT CASE WHEN le.latest_result IN (
            '{executed_status_1}', '{executed_status_2}', '...'
        ) THEN le."{case_id_field}" END), 0)
    , 4)                                                               AS pass_rate

FROM latest_exec le
GROUP BY le.tenantkey
ORDER BY le.tenantkey;
```

**按项目维度扩展：**
在 `exec_records` 中加 LEFT JOIN 用例信息表，取 `project_root_id` / `project_root_name`，一路传递到最终 GROUP BY。

---

## 六、指标维度扩展模式

### 按月统计口径

```sql
-- 过滤当月
WHERE DATE(finish_ts) >= DATE_TRUNC('month', CURRENT_DATE)
  AND DATE(finish_ts) <  DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '1 month'

-- GROUP BY 月份
GROUP BY DATE_TRUNC('month', finish_ts)::DATE
```

### 按项目维度扩展（统一模式）

```sql
-- Step1：主表 LEFT JOIN 自定义字段表取项目名
base_items AS (
    SELECT
        t."tenantkey",
        t."objectid",
        COALESCE(proj."{value_field}", '未归属项目') AS project_name
    FROM {schema}."{item_table}" t
    LEFT JOIN {schema}."{project_dropdown_table}" proj
        ON t."objectid"  = proj."{item_fk_field}"
       AND t."tenantkey" = proj."tenantkey"
    WHERE ...
)

-- Step2：最终 SELECT 加维度字段，GROUP BY 加 project_name
SELECT
    b."tenantkey"                                    AS tenant_key,
    COALESCE(b."project_name", '未归属项目')          AS project_name,
    -- 指标字段...
FROM ...
GROUP BY b."tenantkey", b."project_name"
```

### 指标公式模板

```sql
-- 比率类（百分比）
ROUND(COUNT(分子条件) * 100.0 / NULLIF(COUNT(分母条件), 0), 2) AS rate_pct

-- 均值类
ROUND(AVG(value_col) FILTER (WHERE value_col >= 0), 1) AS avg_value

-- 密度类（每单位数量）
ROUND(SUM(count_col) * 1.0 / NULLIF(COUNT(DISTINCT group_key), 0), 2) AS density

-- 防零除法（通用）
ROUND(SUM(numerator) * 1.0 / NULLIF(SUM(denominator), 0), 精度)
```
