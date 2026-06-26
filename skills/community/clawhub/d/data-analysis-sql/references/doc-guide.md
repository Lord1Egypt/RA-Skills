# 文档自动生成与迁移指南

> 本技能支持自动生成表结构说明文档和 SQL 迁移文档，方便知识沉淀和跨环境迁移。

---

## 一、快速生成表结构文档

### 方式一：交互式运行脚本

```bash
python scripts/doc_generator.py
```

按提示输入表数量、字段信息，自动生成 Markdown 文档。

### 方式二：调用 Python API

```python
from scripts.doc_generator import parse_table_definition, generate_full_document

# 解析用户提供的表结构文本
text = '''
{table_name}（{table_desc}）
{field1}: {field1_desc}
{field2}: {field2_desc}
...
'''

table = parse_table_definition(text)
doc = generate_full_document([table], title='{模块名}表结构', output_path='schema.md')
```

---

## 二、从零开始写一个迁移文档

当用户提供新项目的表结构时，按以下模板生成文档：

```markdown
# {项目名} 表结构说明

> 更新时间：{YYYY-MM-DD}
> 数据库：{db_name}

---

## 一、数据表清单

| 序号 | 表名 | 描述 | 字段数 |
|------|------|------|--------|
| 1 | table_name | 描述 | N |

---

## 二、表结构详情

### {表名}

**业务说明：** {一句话描述用途}

| 字段名 | 类型 | 描述 |
|--------|------|------|
| col1 | VARCHAR | 描述 |
```

---

## 三、指标 SQL 迁移清单

当写完一个指标 SQL 后，自动生成迁移摘要：

```python
from scripts.doc_generator import generate_sql_summary

sql = """
WITH initial_req AS (...)
SELECT tenant_key, stat_month, delivered_cnt, defect_density_per_req
FROM ...
"""

summary = generate_sql_summary(sql, db_type='PostgreSQL')
# 输出摘要供迁移参考
```

**摘要包含：**
- 数据源表（`source_tables`）
- CTE 列表（`ctes`）
- 输出字段（`output_fields`）
- 过滤条件（`filters`）
- SQL 行数（`line_count`）

---

## 四、生成完整迁移文档

将表结构 + SQL 摘要打包生成完整迁移文档：

```python
from scripts.doc_generator import generate_migration_doc

tables = [
    {'table_name': '{table_name}', 'table_desc': '{table_desc}', 'fields': [...]},
]
sqls = [
    {'db_type': 'PostgreSQL', 'source_tables': [...], 'ctes': [...], 'filters': [...], 'output_fields': [...]}
]

doc = generate_migration_doc(tables, sqls, target_db='MySQL')
# 保存到文件
with open('migration_doc.md', 'w', encoding='utf-8') as f:
    f.write(doc)
```

**迁移文档包含：**
1. 数据表清单（快速索引）
2. 表结构详情（字段 + 类型 + 描述）
3. 业务 SQL 清单（每个 SQL 的数据源、过滤条件、输出字段）

---

## 五、文档规范模板

### 表结构文档标准头部

```markdown
# {模块名} 表结构说明

> 整理自：{文档来源}
> 更新时间：{YYYY-MM-DD}
> 数据库：{db_name}

---

## 关联关系图

```
{main_table}
    ├── {rel_table_1}
    └── {rel_table_2}
```
```

### 字段表标准格式

```markdown
| 字段名 | 类型 | 描述 |
|--------|------|------|
| objectid | - | 主键ID |
| tenantkey | - | 租户key（关联时必须与 objectid 联合使用） |
```

### SQL 注释标准格式

```sql
-- ================================================
-- {指标名称}
-- 定义：{指标公式口径}
-- 数据源：{主表}
-- 维度：{租户/项目/系统/时间}
-- 更新：{YYYY-MM-DD}
-- ================================================
```

---

## 六、自动生成触发场景

当用户提到以下关键词时，自动调用文档生成能力：

| 场景 | 触发词 | 输出 |
|------|--------|------|
| 整理表结构 | "整理一下"、"生成文档"、"写成 md" | 表结构 Markdown 文档 |
| 迁移 SQL | "迁移到xx库"、"从xx改写成xx" | SQL 迁移摘要 |
| 沉淀指标 | "这个指标沉淀一下"、"写个文档" | 指标说明文档 |
| 对比旧 SQL | "对比一下这两个 SQL" | sql_diff.py 差异报告 |
