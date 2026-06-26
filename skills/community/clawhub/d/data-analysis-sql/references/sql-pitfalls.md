# SQL 踩坑记录与解决方案

> 来源：实际执行中遇到的问题及修复方案

---

## 一、字段类型类问题

### 1. 时间字段存毫秒时间戳字符串

**症状：**
```
ERROR: invalid input syntax for type timestamp: "1774886400000"
```
`plannedendtimedate` 等字段存的是毫秒级时间戳字符串（如 `"1774886400000"`），直接存进表会导致类型不匹配。

**解决方案：**
```sql
CASE
    WHEN mi."plannedendtimedate" ~ '^\d{10,13}$'
    THEN to_timestamp(CAST(mi."plannedendtimedate" AS BIGINT) / 1000.0)
    WHEN mi."plannedendtimedate" ~ '^\d{4}-\d{2}-\d{2}'
    THEN mi."plannedendtimedate"::timestamp
    ELSE NULL
END AS planned_finish_ts
```

**注意：**
- `^\d{10,13}$` 同时兼容10位秒级和13位毫秒级
- 正则 `~` 是 PostgreSQL 特有语法
- 除以 1000.0 将毫秒转为秒，再由 `to_timestamp` 转为 TIMESTAMP

---

### 2. 时间戳字符串存入 TIMESTAMP 列

**症状：**
同上报错。某些表（如变更记录表 `updatedat`）在清洗任务中直接存了字符串时间戳。

**解决思路：**
- 先确认源字段是 `BIGINT` 还是 `VARCHAR`
- 如为 BIGINT：`to_timestamp(col / 1000.0)`
- 如为 VARCHAR 格式（如 `"2024-01-01"`）：`col::timestamp`

---

### 3. 数字字段与字符串混用 COALESCE

**症状：**
```
ERROR: invalid input syntax for type numeric: "N/A"
```
`COALESCE(numeric_col, 'N/A')` 会报错，因为 `'N/A'` 是字符串，无法与数字类型兼容。

**解决方案：**
```sql
-- 错误
COALESCE(project_id, 'N/A')

-- 正确：先转 TEXT
COALESCE(CAST(project_id AS TEXT), 'N/A')
```

---

## 二、关联类问题

### 4. 关联表没有 tenantkey

**症状：**
```
ERROR: column cd.tenantkey does not exist
```
用例关联表、缺陷表等没有 `tenantkey` 字段，需要从主表带过来。

**解决方案：**
```sql
-- tenantkey 从主表通过 JOIN 带过来，不依赖关联表本身有此字段
sub_cte AS (
    SELECT DISTINCT
        main."tenantkey",     -- 从主表带过来
        main."objectid"       AS main_id,
        rel."related_id"
    FROM main_table main
    INNER JOIN {schema}."{no_tenantkey_table}" rel
        ON main."{key_field}" = rel."{foreign_key}"   -- 用 key 关联
       AND rel."del_flag" = 0
)
```

---

### 5. 关联键字段名不一致

**症状：**
JOIN 不到数据，关联结果为空。

**常见场景：**
- `{item_table}.objectid` 对应 `{dropdown_table}.itemobjectid`
- `{item_table}.{key_field}` 对应 `{rel_table}.{foreign_key}`（不是 objectid！）
- 不同表之间的 `{case_id_field}` 可能有不同的实际含义

**教训：**
关联之前先确认字段的实际含义，不要只看字段名。部分表里外键存的是事项 `key` 而不是 `objectid`。

---

## 三、聚合类问题

### 6. 外层引用列未在 CTE SELECT 中声明

**症状：**
```
ERROR: column ds.defect_id does not exist
```
`defect_summary` CTE 只 GROUP BY 了 key 列，没有 SELECT `defect_id`，但最终查询里用了 `COUNT(DISTINCT ds.defect_id)`。

**解决方案：**
拆成两层：
```sql
-- 错误做法：只 GROUP BY key 列，外层无法引用 defect_id
defect_summary AS (
    SELECT
        tenantkey,
        demand_id,
        COUNT(DISTINCT defect_id) AS defect_cnt   -- 直接聚合，defect_id 丢失
    FROM case_defect GROUP BY ...

-- 正确做法：先平铺明细，再聚合
defect_summary AS (
    SELECT tenantkey, demand_id, defect_id   -- 明细平铺
    FROM case_defect
),
defect_by_req AS (
    SELECT
        tenantkey, demand_id,
        MAX(actual_finish_ts) AS actual_finish_ts,
        COUNT(DISTINCT defect_id) AS defect_cnt   -- 再聚合
    FROM defect_summary
    GROUP BY tenantkey, demand_id
)
```

---

## 四、窗口函数类问题

### 7. Oracle KEEP 语法在 PostgreSQL 中不兼容

**症状：**
`MAX(col) KEEP (DENSE_RANK LAST ORDER BY t)` 在 PostgreSQL 中报语法错误。

**Oracle 写法（不兼容）：**
```sql
MAX(col) KEEP (DENSE_RANK LAST ORDER BY latest_exec_time)
```

**PostgreSQL 改写（正确）：**
```sql
-- 嵌套子查询 + ROW_NUMBER
SELECT
    sub.tenantkey,
    sub.case_id,
    sub.exec_result AS latest_exec_result
FROM (
    SELECT
        er.*,
        ROW_NUMBER() OVER (
            PARTITION BY er.tenantkey, er.case_id
            ORDER BY er.latest_exec_time DESC NULLS LAST
        ) AS rn
    FROM exec_records er
) sub
WHERE sub.rn = 1
```

---

## 五、别名类问题

### 8. CTE 别名与内部列别名冲突

**症状：**
```
ERROR: missing FROM-clause entry for table "le"
```
CTE 别名 `le` 和内部列别名 `le` 重名，PostgreSQL 解析器混淆。

**解决方案：**
- CTE 别名统一叫全名（如 `latest_exec`）
- 内部子查询用无关别名（如 `t`）
```sql
-- 错误
latest_exec AS (
    SELECT le.tenantkey, le.case_id, ...
    FROM (...) le
)

-- 正确
latest_exec AS (
    SELECT t.tenantkey, t.case_id, ...
    FROM (...) t
    WHERE t.rn = 1
)
-- 外层直接用 latest_exec.xxx
```

---

## 六、数据口径类问题

### 9. 字段名与实际含义不一致

**教训：**
- 关联表的外键字段可能存的是主表的 `{key_field}` 而不是 `{objectid_field}`
- 确认方式：看字段注释，或实际 JOIN 后验证结果集非空

### 10. del_flag 过滤遗漏

**教训：**
所有关联表都应加 `del_flag = 0`，否则已删除的脏数据会进入指标。

```sql
-- 每张关联表都要加
INNER JOIN xxx_table t ON ...
   AND t."del_flag" = 0
```

---

## 七、防踩坑检查清单

写完 SQL 后，逐项检查：

```
□ 所有关联是否同时带 tenantkey（防跨租户污染）
□ 无 tenantkey 的表是否从主表 JOIN 带过来
□ 时间字段是否做了类型转换（毫秒时间戳/日期字符串）
□ 关联键字段名是否确认（objectid / key / itemobjectid）
□ 所有关联表是否加了 del_flag = 0 过滤
□ COALESCE 的类型是否一致（数字字段先 CAST AS TEXT）
□ 外层引用的列是否在 CTE SELECT 中声明
□ 窗口函数是否用了正确方言（Oracle KEEP → PostgreSQL ROW_NUMBER）
□ CTE 别名是否与内部列别名重名
□ 分母是否用了 NULLIF 防零
□ NULL 处理是否完整（IS NOT NULL 过滤）
□ 项目维度是否用 COALESCE(value, '未归属项目')
```
