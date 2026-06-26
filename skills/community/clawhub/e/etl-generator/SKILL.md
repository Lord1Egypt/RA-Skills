---
name: etl-generator
description: 大数据 ETL 流程生成器 - 根据源表 DDL 生成标准化 ETL 加工 SQL（HiveSQL/MySQL）
metadata: {"version":"2.0","author":"Hank","updated":"2026-03-06"}
---

# ETL 流程生成器 - 大数据专家版

根据源表 DDL 自动生成标准化的 ETL 加工 SQL，支持 HiveSQL、MySQL、ODPS。

## 🎯 角色定位

**大数据专家**（20 年经验）
- 精通 HiveSQL、MySQL、Shell、Python
- 严格遵守大数据 ETL 加工规范
- 注意字段类型转换、时区处理、数据质量

---

## 🔧 核心功能

### 1️⃣ 表名规范
- **源表：** `ods_[表名]_di`
- **目标表：** `dwd_[表名]_di`

### 2️⃣ 字段类型转换
- `_at` 或 `_time` 结尾的 TIMESTAMP 字段 → STRING（时区转换）
- `_date` 结尾的字段 → STRING（不转换）
- 其他字段 → 保持原类型

### 3️⃣ 时区转换
```sql
DATE_FORMAT(FROM_UTC_TIMESTAMP(created_at, "${timezone}"), "yyyy-MM-dd HH:mm:ss.SSS") AS created_at
DATE_FORMAT(FROM_UTC_TIMESTAMP(updated_at, "${timezone}"), "yyyy-MM-dd HH:mm:ss.SSS") AS updated_at
```

### 4️⃣ 分区字段
```sql
DATE_FORMAT(FROM_UTC_TIMESTAMP(created_at, "${timezone}"), "yyyy-MM-dd") AS ds
```

### 5️⃣ 增量数据处理
- 使用 `ods_data_base_di` 表
- 支持 INSERT/UPDATE/DELETE 操作
- 通过 `_operation_` 和 `_after_image_` 识别

### 6️⃣ 去重逻辑
```sql
ROW_NUMBER() OVER(PARTITION BY id ORDER BY updated_at DESC) as rn
WHERE rn = 1
```

### 7️⃣ 字段排除 rn
```sql
SELECT `(rn)?+.+` FROM (...)
```

---

## 📋 使用方式

### 方式 1：命令行

```bash
# 从文件读取 DDL
python3 skills/etl-generator/etl_generator.py source_table.ddl > etl_sql.sql

# 从标准输入读取
cat source_table.ddl | python3 skills/etl-generator/etl_generator.py > etl_sql.sql
```

### 方式 2：直接调用

```python
from etl_generator import parse_table_ddl, generate_target_table_ddl, generate_etl_sql

ddl = """
CREATE TABLE IF NOT EXISTS ods_delivery_attempt_di(
  id STRING COMMENT '主键',
  pno STRING COMMENT '运单号',
  client_id STRING COMMENT '客户 ID',
  returned BIGINT COMMENT '是否退货件',
  delivery_date STRING COMMENT '派送日期',
  marker_id BIGINT COMMENT '标记原因',
  store_id STRING COMMENT '网点 ID',
  created_at TIMESTAMP COMMENT '创建时间',
  updated_at TIMESTAMP COMMENT '更新时间'
) 
PARTITIONED BY (ds STRING) 
STORED AS ALIORC  
TBLPROPERTIES ("columnar.nested.type"="true", "comment"="有效尝试派送详情") 
LIFECYCLE 36500;
"""

table_name, fields, table_comment = parse_table_ddl(ddl)
target_ddl = generate_target_table_ddl(table_name, fields, table_comment)
etl_sql = generate_etl_sql(table_name, fields, table_comment)
```

---

## 📝 输出示例

### 输入（源表 DDL）

```sql
CREATE TABLE IF NOT EXISTS ods_sap_store_cash_pay_info_di(
  id STRING COMMENT "主键",
  store_id STRING COMMENT "网点编号",
  business_date STRING COMMENT "业务日期",
  sap_state BIGINT COMMENT "0:待处理 1:待发送 2:不需要发送 3:已发送 4:异常",
  created_at TIMESTAMP COMMENT "创建时间",
  updated_at TIMESTAMP COMMENT "更新时间'
) 
PARTITIONED BY (ds STRING) 
STORED AS ALIORC 
TBLPROPERTIES ("columnar.nested.type"="true", "comment"="SAP 门店现金支付信息") 
LIFECYCLE 36500;
```

### 输出（目标表 DDL + ETL SQL）

```sql
-- 目标表 DDL
CREATE TABLE IF NOT EXISTS dwd_sap_store_cash_pay_info_di(
  id STRING COMMENT '主键',
  store_id STRING COMMENT '网点编号',
  business_date STRING COMMENT '业务日期',
  sap_state BIGINT COMMENT '0:待处理 1:待发送 2:不需要发送 3:已发送 4:异常',
  created_at STRING COMMENT '创建时间',
  updated_at STRING COMMENT '更新时间'
) 
PARTITIONED BY (ds STRING) 
STORED AS ALIORC  
TBLPROPERTIES ("columnar.nested.type"="true", "comment"="SAP 门店现金支付信息") 
LIFECYCLE 36500;

-- ETL 加工 SQL
WITH ods_data AS (
  SELECT
    id,
    store_id,
    business_date,
    sap_state,
    DATE_FORMAT(FROM_UTC_TIMESTAMP(created_at, "${timezone}"), "yyyy-MM-dd HH:mm:ss.SSS") AS created_at,
    DATE_FORMAT(FROM_UTC_TIMESTAMP(updated_at, "${timezone}"), "yyyy-MM-dd HH:mm:ss.SSS") AS updated_at,
    DATE_FORMAT(FROM_UTC_TIMESTAMP(created_at, "${timezone}"), "yyyy-MM-dd") AS ds
  FROM ods_sap_store_cash_pay_info_di
  WHERE ds >= "${y-m-d}"
  UNION ALL
  SELECT
    get_json_object(values, "$.id") as id,
    get_json_object(values, "$.store_id") as store_id,
    get_json_object(values, "$.business_date") as business_date,
    get_json_object(values, "$.sap_state") as sap_state,
    DATE_FORMAT(FROM_UTC_TIMESTAMP(get_json_object(values, "$.created_at"), "${timezone}"), "yyyy-MM-dd HH:mm:ss.SSS") AS created_at,
    DATE_FORMAT(FROM_UTC_TIMESTAMP(get_json_object(values, "$.updated_at"), "${timezone}"), "yyyy-MM-dd HH:mm:ss.SSS") AS updated_at,
    DATE_FORMAT(FROM_UTC_TIMESTAMP(get_json_object(values, "$.created_at"), "${timezone}"), "yyyy-MM-dd") AS ds
  FROM ods_data_base_di 
  WHERE (
    (_after_image_ = "Y" AND _operation_ IN ("INSERT", "UPDATE"))
    OR (_operation_ = "DELETE" AND _before_image_ = "Y")
    OR _id_ IS NULL
  )
  AND ds >= "${y-m-d}"
  AND table_name = "sap_store_cash_pay_info"
  AND db_name = "source_db"
)
INSERT OVERWRITE TABLE dwd_sap_store_cash_pay_info_di PARTITION(ds)
SELECT `(rn)?+.+` FROM (
  SELECT 
    *,
    ROW_NUMBER() OVER(PARTITION BY id ORDER BY updated_at DESC) as rn 
  FROM (
    SELECT * FROM dwd_sap_store_cash_pay_info_di WHERE ds IN (
      SELECT DISTINCT ds FROM ods_data
    )
    UNION ALL
    SELECT * FROM ods_data
  ) a
) t1
WHERE rn = 1;
```

---

## 🧪 数据质量检查

自动生成以下检查 SQL：

1. **主键空值检查**
2. **退货件比例检查**（如果有 returned 字段）
3. **数据量对比**（源表 vs 目标表）

---

## 📋 字段映射说明

自动生成字段映射文档：

```sql
-- ============================================
-- 字段映射说明
-- ============================================
-- 源表字段 (7 个): id, store_id, business_date, sap_state, created_at, updated_at
-- 目标表字段 (7 个): id, store_id, business_date, sap_state, created_at, updated_at
-- 分区字段：ds
-- 
-- 字段转换规则:
-- created_at: TIMESTAMP → STRING, 时区转换
-- updated_at: TIMESTAMP → STRING, 时区转换
-- business_date: 直接映射
-- ============================================
```

---

## ⚙️ 配置参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `${timezone}` | 时区 | UTC |
| `${y-m-d}` | 业务日期 | ${yyyymmdd-1} |
| `${bizdate}` | 业务日期（质量检查） | ${yyyymmdd-1} |

---

## 📁 文件结构

```
skills/etl-generator/
├── SKILL.md              # 技能说明
├── etl_generator.py      # 核心脚本
├── README.md             # 使用文档
└── examples/             # 示例 DDL
    └── delivery_attempt.ddl
```

---

## 🔧 高级用法

### 1. 批量生成

```bash
# 批量处理多个表
for ddl in ddl/*.ddl; do
  python3 skills/etl-generator/etl_generator.py $ddl > etl/$(basename $ddl .ddl)_etl.sql
done
```

### 2. 自定义模板

修改 `etl_generator.py` 中的模板函数，适配特定业务场景。

### 3. 集成 DataWorks

```bash
# 生成 DataWorks 节点配置
python3 skills/etl-generator/etl_generator.py source.ddl | \
  python3 skills/etl-generator/dataworks_adapter.py > node_config.yaml
```

---

## ⚠️ 注意事项

### 1. 字段顺序
- 确保输入输出的字段顺序个数一致
- 使用 `(rn)?+.+` 排除 rn 字段

### 2. 时区处理
- 所有时间字段必须做时区转换
- `_date` 结尾的字段不转换

### 3. 表名规范
- 源表：`ods_[表名]_di`
- 目标表：`dwd_[表名]_di`
- WITH 引用使用原表名

### 4. 增量数据
- 使用 `ods_data_base_di` 表
- 正确配置 `table_name` 和 `db_name`

---

## 📊 版本历史

### v2.0 (2026-03-06)
- ✅ 优化时区转换逻辑
- ✅ 支持增量数据处理
- ✅ 自动生成数据质量检查
- ✅ 自动生成字段映射说明
- ✅ 字段排除 rn 字段

### v1.0 (2026-02-28)
- ✅ 基础 ETL 生成功能
- ✅ 字段类型转换
- ✅ 目标表 DDL 生成

---

**维护者：** 汉克 (Hank)  
**更新时间：** 2026-03-06
