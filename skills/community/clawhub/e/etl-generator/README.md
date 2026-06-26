# ETL 流程生成器技能

## 🎯 功能说明

根据源表 DDL 自动生成标准化的 ETL 加工 SQL，包含：
- 表名转换（ods → dwd）
- 字段类型转换（TIMESTAMP → STRING）
- 时区处理
- 增量合并逻辑
- 去重逻辑

---

## 📝 使用方法

### 方式 1：直接提供 DDL

**你说：**
```
生成 ETL 任务，源表结构：
CREATE TABLE ods_xxx_di (
  id STRING,
  created_at TIMESTAMP,
  ...
)
```

**我会生成：**
- 目标表 DDL
- 完整 ETL SQL
- 变量说明

---

### 方式 2：提供表名

**你说：**
```
ETL 加工 ods_sap_store_cash_pay_info_di
```

**我会：**
1. 查询源表结构（如可访问）
2. 生成 ETL 流程

---

## 🔧 处理规则

### 表名转换

| 源表名 | 目标表名 |
|--------|----------|
| `ods_xxx_di` | `dwd_xxx_di` |
| `ods_xxx_df` | `dwd_xxx_df` |
| `dwd_xxx_di` | `dws_xxx_di` |

---

### 字段类型转换

**规则：** 字段以 `_at` 或 `_time` 结尾的 TIMESTAMP 字段 → STRING

| 原字段 | 原类型 | 新字段 | 新类型 |
|--------|--------|--------|--------|
| `created_at` | TIMESTAMP | `created_at` | STRING |
| `updated_time` | TIMESTAMP | `updated_time` | STRING |
| `order_id` | STRING | `order_id` | STRING |

---

### 时区转换

```sql
DATE_FORMAT(
  FROM_UTC_TIMESTAMP(created_at, "${timezone}"),
  "yyyy-MM-dd HH:mm:ss.SSS"
) AS created_at
```

---

### 分区字段

```sql
DATE_FORMAT(
  FROM_UTC_TIMESTAMP(created_at, "${timezone}"),
  "yyyy-MM-dd"
) AS ds
```

---

## 📋 完整示例

### 输入

```sql
CREATE TABLE IF NOT EXISTS ods_sap_store_cash_pay_info_di(
  id STRING COMMENT "主键",
  store_id STRING COMMENT "网点编号",
  business_date STRING COMMENT "业务日期",
  sap_state BIGINT COMMENT "0:待处理 1:待发送 2:不需要 3:已发送 4:异常",
  created_at TIMESTAMP COMMENT "创建时间",
  updated_at TIMESTAMP COMMENT "更新时间"
) 
PARTITIONED BY (ds STRING) 
STORED AS ALIORC  
TBLPROPERTIES ("columnar.nested.type"="true") 
LIFECYCLE 36500;
```

---

### 输出

#### 1️⃣ 目标表 DDL

```sql
CREATE TABLE IF NOT EXISTS dwd_sap_store_cash_pay_info_di(
  id STRING COMMENT "主键",
  store_id STRING COMMENT "网点编号",
  business_date STRING COMMENT "业务日期",
  sap_state BIGINT COMMENT "0:待处理 1:待发送 2:不需要 3:已发送 4:异常",
  created_at STRING COMMENT "创建时间",
  updated_at STRING COMMENT "更新时间"
) 
PARTITIONED BY (ds STRING) 
STORED AS ALIORC  
TBLPROPERTIES ("columnar.nested.type"="true") 
LIFECYCLE 36500;
```

---

#### 2️⃣ ETL 加工 SQL

```sql
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
      get_json_object(values, "$.id") AS id,
      get_json_object(values, "$.store_id") AS store_id,
      get_json_object(values, "$.business_date") AS business_date,
      get_json_object(values, "$.sap_state") AS sap_state,
      DATE_FORMAT(FROM_UTC_TIMESTAMP(get_json_object(values, "$.created_at"), "${timezone}"), "yyyy-MM-dd HH:mm:ss.SSS") AS created_at,
      DATE_FORMAT(FROM_UTC_TIMESTAMP(get_json_object(values, "$.updated_at"), "${timezone}"), "yyyy-MM-dd HH:mm:ss.SSS") AS updated_at,
      DATE_FORMAT(FROM_UTC_TIMESTAMP(get_json_object(values, "$.created_at"), "${timezone}"), "yyyy-MM-dd") AS ds
    FROM ods_data_base_di 
    WHERE ds >= "${y-m-d}"
      AND table_name = "store_cash_pay_info"
      AND db_name = "fle_staging"
)
INSERT OVERWRITE TABLE dwd_sap_store_cash_pay_info_di PARTITION(ds)
SELECT `(rn)?+.+` FROM (
    SELECT 
        *,
        ROW_NUMBER() OVER(PARTITION BY id ORDER BY updated_at DESC) AS rn 
    FROM (
        SELECT * FROM dwd_sap_store_cash_pay_info_di 
        WHERE ds IN (SELECT DISTINCT ds FROM ods_data)
        UNION ALL
        SELECT * FROM ods_data
    ) a
) t1
WHERE rn = 1;
```

---

## 📊 变量说明

| 变量 | 说明 | 默认值 | 示例 |
|------|------|--------|------|
| `${timezone}` | 时区 | Asia/Shanghai | Asia/Shanghai |
| `${y-m-d}` | 数据日期 | 运行日期 | 2026-02-28 |
| `${biz_date}` | 业务日期 | 运行日期 -1 | 2026-02-27 |

---

## 🔍 处理流程

```
1. 接收源表 DDL
       ↓
2. 解析表结构（字段、类型、注释）
       ↓
3. 应用转换规则
   - 表名转换
   - 字段类型转换
   - 时区处理逻辑
       ↓
4. 生成目标表 DDL
       ↓
5. 生成 ETL SQL
   - WITH 子句
   - UNION ALL 增量
   - ROW_NUMBER 去重
   - INSERT OVERWRITE
       ↓
6. 验证输出
   - 字段数量一致
   - 字段顺序一致
   - 语法正确
```

---

## ⚠️ 注意事项

### 字段处理

1. **字段顺序** - 必须与源表完全一致
2. **字段数量** - 输入输出必须相同
3. **时间字段** - 识别 `_at` 和 `_time` 后缀
4. **主键字段** - 用于去重逻辑

---

### 表命名规范

| 层级 | 后缀 | 说明 |
|------|------|------|
| ODS | `_di` / `_df` | 原始数据 |
| DWD | `_di` / `_df` | 明细数据 |
| DWS | `_di` / `_df` | 汇总数据 |
| ADS | `_di` / `_df` | 应用数据 |

---

### 增量处理

**增量标识字段：**
- `_operation_` - 操作类型（INSERT/UPDATE/DELETE）
- `_after_image_` - 后镜像标识
- `_before_image_` - 前镜像标识
- `_id_` - 记录 ID

---

## 🛠️ 扩展功能

### 已实现
- ✅ 表名自动转换
- ✅ 字段类型转换
- ✅ 时区处理
- ✅ 增量合并
- ✅ 去重逻辑

### 待实现
- [ ] MySQL 到 Hive 转换
- [ ] Python UDF 生成
- [ ] Shell 脚本生成
- [ ] DataWorks 任务配置导出
- [ ] 字段血缘追踪

---

## 📚 相关技能

- `dataworks-smart-monitor` - DataWorks 智能监控
- `sql-review-bot` - SQL 代码审查
- `data-dictionary-auto` - 自动数据字典

---

## 🎯 使用示例

### 示例 1：简单表

**输入：**
```sql
CREATE TABLE ods_user_info_di (
  user_id STRING,
  user_name STRING,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
) PARTITIONED BY (ds STRING);
```

**输出：**
```sql
-- 目标表
CREATE TABLE dwd_user_info_di (
  user_id STRING,
  user_name STRING,
  created_at STRING,
  updated_at STRING
) PARTITIONED BY (ds STRING);

-- ETL SQL
WITH ods_data AS (
  SELECT
    user_id,
    user_name,
    DATE_FORMAT(FROM_UTC_TIMESTAMP(created_at, "${timezone}"), "yyyy-MM-dd HH:mm:ss.SSS") AS created_at,
    DATE_FORMAT(FROM_UTC_TIMESTAMP(updated_at, "${timezone}"), "yyyy-MM-dd HH:mm:ss.SSS") AS updated_at,
    DATE_FORMAT(FROM_UTC_TIMESTAMP(created_at, "${timezone}"), "yyyy-MM-dd") AS ds
  FROM ods_user_info_di
  WHERE ds >= "${y-m-d}"
)
INSERT OVERWRITE TABLE dwd_user_info_di PARTITION(ds)
SELECT `(rn)?+.+` FROM (
  SELECT *, ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY updated_at DESC) AS rn
  FROM [...]
) t1 WHERE rn = 1;
```

---

### 示例 2：复杂表

**你说：**
```
生成 ETL，这个表有 10 个字段，3 个时间字段
```

**我会：**
1. 询问表结构或等待提供 DDL
2. 识别所有时间字段
3. 应用转换规则
4. 生成完整 SQL

---

## 💡 最佳实践

### 性能优化
1. 使用 ALIORC 存储格式
2. 合理设置 LIFECYCLE
3. 分区字段选择业务日期
4. 去重逻辑使用 ROW_NUMBER

### 代码规范
1. 字段注释完整
2. 表名遵循规范
3. 变量使用占位符
4. SQL 格式化

---

**技能已就绪，随时可以生成 ETL 流程！** 🔧💾
