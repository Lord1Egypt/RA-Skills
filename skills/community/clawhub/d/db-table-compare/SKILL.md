---
name: db-table-compare
description: 对比两个数据库（MySQL vs ODPS）的表字段差异，生成 HiveSQL ALTER TABLE 和 DataX JSON 格式
tags: [database, compare, mysql, odps, schema, diff, datax]
---
# 数据库表字段对比技能

## 功能
对比两个数据库的表结构差异，生成：
1. HiveSQL ALTER TABLE 语句
2. DataX JSON 格式（get_json_object 提取字段）

## 触发词
- "对比 [表名] 字段"
- "表结构差异"
- "MySQL vs ODPS [表名]"
- "生成 alter table"
- "生成 datax json"
- "字段差异"

## 支持的数据库

| 数据库 | 类型 | 连接方式 |
|--------|------|----------|
| TH DataWorks | ODPS/MaxCompute | SSH + odpscmd |
| PH DataWorks | ODPS/MaxCompute | SSH + odpscmd |
| TH FIN | MySQL | Python pymysql |
| TH FLE | MySQL | Python pymysql |
| TH SAP | MySQL | Python pymysql |

## 执行流程

1. **确定数据源** - 解析表名和环境
2. **查询表结构** - DESC / SHOW CREATE TABLE
3. **对比字段** - 找出差异
4. **生成输出** - ALTER TABLE + DataX JSON

## 输出格式

### 1. ALTER TABLE（新增字段）
```sql
ALTER TABLE dwd_xxx_di 
ADD COLUMNS (
    field_name BIGINT COMMENT '注释'
);
```

### 2. DataX JSON（字段提取）
```json
get_json_object(values, '$.field_name') as field_name,
```

## 使用示例

### 示例：对比 TH FIN 表
**用户：** "对比 th-fin 的 ka_accounts_receivable_detail_c3 和 dwd_fin_ka_accounts_receivable_detail_c3_di"

**执行：**
```bash
# 1. 查 MySQL 字段
python3 -c "
import pymysql
conn = pymysql.connect(host='core-dev-db.fex.pub', port=3306, user='th_dev_fin_rw', password='xxx', database='th_dev_fin')
cursor = conn.cursor()
cursor.execute('DESC ka_accounts_receivable_detail_c3')
for r in cursor.fetchall():
    print(r[0], r[1])
conn.close()
"

# 2. 查 ODPS 字段
ssh datax "cd /mnt/www/addr/th_odpscmd/bin && echo 'DESC dwd_fin_ka_accounts_receivable_detail_c3_di;' | ./odpscmd"
```

**返回：**
- 字段对比表
- 差异说明
- ALTER TABLE 语句
- DataX JSON 格式

---

## 智能处理

1. **自动识别数据源**
   - `dwd_`, `ads_`, `dim_` 前缀 → ODPS
   - 其他 → MySQL

2. **自动选择环境**
   - TH 相关 → TH DataWorks / TH MySQL
   - PH 相关 → PH DataWorks / PH MySQL
   - fin → th_dev_fin

3. **字段匹配**
   - 不区分大小写

## DataX JSON 格式说明

DataX 数据摄取时，ODPS 字段从 JSON 提取：

| 用途 | 格式 |
|------|------|
| 读取 JSON | `get_json_object(values, '$.字段名')` |
| 别名 | `as 字段名` |
| 完整行 | `get_json_object(values, '$.字段名') as 字段名,` |

## 注意事项

1. **只读查询** - 只执行 DESC/SHOW CREATE TABLE
2. **不执行 DDL** - 只生成语句，用户确认后再执行
3. **密码保护** - 密码不输出

## 更新日志

### 2026-04-21
- ✅ 创建技能
- ✅ 支持 TH FIN vs TH DataWorks 对比
- ✅ 支持生成 ALTER TABLE
- ✅ 支持生成 DataX JSON 格式（get_json_object）
