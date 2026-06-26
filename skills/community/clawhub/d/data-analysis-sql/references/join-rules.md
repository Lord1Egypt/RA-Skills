# join-rules.md — 关联规则规范

> 适用所有多租户业务系统的 SQL 编写
> 更新时间：2026-04-01

---

## 防踩坑检查清单

写完 SQL 后，逐项过一遍：

```
□ 所有关联是否同时带 tenantkey（防跨租户污染）
□ 无 tenantkey 的表是否从主表 JOIN 带过来
□ 所有关联表是否加了 del_flag = 0 过滤
□ 自定义字段是否关联了对应的 _dropdown 表
□ 项目维度是否用 COALESCE(value, '未归属项目')
□ 分母是否用了 NULLIF 防零
□ 数字字段与字符串 COALESCE 是否先 CAST AS TEXT
□ 时间字段是否做了类型转换（毫秒时间戳 / 日期字符串）
□ 关联键字段名是否确认（objectid / key / itemobjectid 等）
□ 外层引用的列是否在 CTE SELECT 中声明
□ 窗口函数是否用了正确方言（Oracle KEEP → PostgreSQL ROW_NUMBER）
□ CTE 别名是否与内部列别名重名
□ NULL 处理是否完整（IS NOT NULL 过滤）
```

---

## 一、tenantkey 关联规则

**核心原则：所有表关联必须同时带 `tenantkey`，防止跨租户数据污染。**

```sql
-- ✅ 正确：objectid + tenantkey 联合关联
INNER JOIN schema."table_b" b
    ON a."objectid"  = b."itemobjectid"
   AND a."tenantkey" = b."tenantkey"

-- ❌ 错误：只用 objectid 关联
INNER JOIN schema."table_b" b
    ON a."objectid" = b."itemobjectid"
```

---

## 二、无 tenantkey 表的处理

部分关联表**没有 tenantkey 字段**，需从主表 JOIN 带过来：

**处理方式：** 从有 tenantkey 的主表通过 JOIN 传递，不依赖关联表本身的 tenantkey。

```sql
-- 示例：关联表无 tenantkey，从主表带过来
sub_cte AS (
    SELECT DISTINCT
        main."tenantkey",          -- ← 从主表带过来
        main."objectid",
        rel."related_id"
    FROM main_table main
    INNER JOIN no_tenantkey_table rel
        ON main."key" = rel."foreign_key"
       AND rel."del_flag" = 0
    -- 不依赖 rel.tenantkey（该表无此字段）
)
```

---

## 三、del_flag 过滤规则

**所有关联表都必须加 `del_flag = 0`，防止已删除数据进入指标。**

```sql
-- 每张关联表都要加，不能只在主表加
INNER JOIN schema."table_b" b
    ON a."id" = b."foreign_id"
   AND b."del_flag" = 0   -- ← 必加

INNER JOIN schema."table_c" c
    ON b."id" = c."foreign_id"
   AND c."del_flag" = 0   -- ← 必加
```

---

## 四、自定义字段关联规则

下拉框/用户类型的自定义字段不在主事项表中，需关联对应的 `_dropdown` 表：

```sql
-- 取自定义字段值（LEFT JOIN，允许为空）
LEFT JOIN schema."custom_field_dropdown" cf
    ON main."objectid"  = cf."itemobjectid"
   AND main."tenantkey" = cf."tenantkey"
```

> 日期/数值/字符串类型的自定义字段通常直接在主表中查找。

---

## 五、项目维度扩展模式

所有指标按项目维度扩展的统一写法：

```sql
-- Step1：主表 LEFT JOIN 自定义字段表，取项目名
base_cte AS (
    SELECT
        main."tenantkey",
        main."objectid",
        COALESCE(proj."value", '未归属项目') AS project_name
    FROM schema."main_table" main
    LEFT JOIN schema."project_dropdown" proj
        ON main."objectid"  = proj."itemobjectid"
       AND main."tenantkey" = proj."tenantkey"
    WHERE main."del_flag" = 0
      AND ...
)

-- Step2：最终 SELECT 加维度字段，GROUP BY 加 project_name
SELECT
    b."tenantkey"                                    AS tenant_key,
    COALESCE(b."project_name", '未归属项目')          AS project_name,
    COUNT(*)                                          AS total_count
    -- 其他指标字段...
FROM base_cte b
GROUP BY b."tenantkey", b."project_name"
```

---

## 六、分母防零规则

```sql
-- 所有除法必须用 NULLIF 防零，避免除零报错
ROUND(
    SUM(numerator_col) * 1.0 / NULLIF(COUNT(denominator_col), 0),
    4
)
```

---

## 七、取最新记录规则（PostgreSQL）

> Oracle `KEEP (DENSE_RANK LAST ...)` 在 PostgreSQL 中不支持，统一用 `ROW_NUMBER`。

```sql
-- 取每个分组的最新一条记录
ranked AS (
    SELECT
        t.*,
        ROW_NUMBER() OVER (
            PARTITION BY t.group_key1, t.group_key2
            ORDER BY t.time_col DESC NULLS LAST
        ) AS rn
    FROM source_table t
),
latest AS (
    SELECT * FROM ranked WHERE rn = 1
)
```

---

## 八、时间字段处理规则

### 毫秒时间戳字符串转日期（PostgreSQL）

```sql
-- 兼容毫秒时间戳字符串和日期字符串两种格式
CASE
    WHEN col ~ '^\d{10,13}$'
    THEN to_timestamp(CAST(col AS BIGINT) / 1000.0)
    WHEN col ~ '^\d{4}-\d{2}-\d{2}'
    THEN col::timestamp
    ELSE NULL
END AS ts_col
```

### 时间范围过滤（当月）

```sql
WHERE DATE_TRUNC('month', time_col) = DATE_TRUNC('month', CURRENT_DATE)
```

---

## 九、COALESCE 类型兼容规则

```sql
-- ❌ 错误：数字字段与字符串 COALESCE，类型不兼容
COALESCE(numeric_col, 'N/A')

-- ✅ 正确：先转 TEXT
COALESCE(CAST(numeric_col AS TEXT), 'N/A')

-- ✅ 正确：字符串字段直接用
COALESCE(varchar_col, '未知')
```
