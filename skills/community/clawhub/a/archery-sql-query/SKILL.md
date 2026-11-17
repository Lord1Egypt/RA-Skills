---
name: archery-query
description: 通过 Archery SQL 平台查询数据库。当用户需要执行 SQL 查询、查看数据库结构、列出实例或数据库、查找重复数据时使用此 skill。触发词包括：查询数据库、Archery、SQL查询、数据库探索、TiDB、MySQL、StarRocks、重复数据、去重、数据清理 等数据库相关操作。
---

# Archery Query

通过 Archery SQL 审核平台查询数据库的技能。

## 快速开始

### 查询示例

```bash
# 查询指定表
python3 ~/.claude/skills/archery-query/scripts/archery_query.py \
  "SELECT * FROM your_table LIMIT 5"

# 使用别名（需先配置实例别名）
python3 ~/.claude/skills/archery-query/scripts/archery_query.py \
  --alias alias1 "SELECT * FROM your_table LIMIT 5"

# 查看表结构
python3 ~/.claude/skills/archery-query/scripts/archery_query.py --desc your_table

# 列出数据库
python3 ~/.claude/skills/archery-query/scripts/archery_query.py --list-dbs

# 列出表
python3 ~/.claude/skills/archery-query/scripts/archery_query.py --list-tables your_database

# 使用查询模板
python3 ~/.claude/skills/archery-query/scripts/archery_query.py \
  --template failed_records --params limit=10

# JSON 输出
python3 ~/.claude/skills/archery-query/scripts/archery_query.py \
  --format json "SELECT * FROM your_table LIMIT 5"
```

## 查询模板

本 skill 提供通用查询模板（用户需根据实际情况修改）：

| 模板名 | 说明 |
|--------|------|
| `failed_records` | 查询失败的记录 |
| `recent_records` | 查询最近的记录 |
| `by_field` | 按字段查询 |

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--alias` | 实例别名 | - |
| `--instance` | 实例名 | your-instance |
| `--db` | 数据库名 | your-database |
| `--limit` | 返回行数限制 | 100 |
| `--format` | 输出格式（table/json） | table |
| `--timeout` | 查询超时（秒） | 60 |
| `--template` | 使用查询模板 | - |
| `--params` | 模板参数 | - |
| `--desc` | 查看表结构 | - |
| `--list-dbs` | 列出数据库 | - |
| `--list-tables` | 列出表 | - |

## 配置说明

### Skill 安装目录

- Claude Code: `~/.claude/skills/`
- 其他工具请参考 `references/config-example.md`

### 配置凭证

创建 `~/.archery/config.json` 文件:

```json
{
  "archery_username": "your_username",
  "archery_password": "your_password",
  "archery_base_url": "http://your-server:9123"
}
```

**安全建议:**
```bash
# 设置配置文件权限
chmod 600 ~/.archery/config.json

# 添加到 gitignore
echo ".archery/" >> ~/.gitignore
```

### 2. 配置实例别名（可选）

实例别名配置会自动保存，首次使用时会自动创建。

**查看当前别名:**
```bash
python3 ~/.claude/skills/archery-query/scripts/cache_config.py list
```

**添加别名:**
```bash
python3 ~/.claude/skills/archery-query/scripts/cache_config.py add alias1 instance_name database_name
```

**配置文件位置:**
- `~/.archery/cache/instances.json` (全局共享)

### 3. 自定义查询模板

编辑 `scripts/archery_query.py`，修改 `QUERY_TEMPLATES`：

```python
QUERY_TEMPLATES = {
    "failed_records": {
        "desc": "查询失败的记录",
        "sql": "SELECT * FROM your_table WHERE status != 'success' ORDER BY id DESC LIMIT {limit}",
        "default_params": {"limit": 20},
    },
}
```

## 功能列表

- ✅ 执行 SQL 查询
- ✅ 查看表结构
- ✅ 列出数据库和表
- ✅ 查询模板
- ✅ JSON 输出
- ✅ 实例别名
- ✅ Session 自动管理
- ✅ **查找重复数据并生成删除语句**

## 注意事项

1. **凭证安全** - 配置文件包含密码，切勿提交到 git
2. **Session 管理** - 自动处理登录和 session，无需手动管理
3. **查询性能** - 使用索引字段查询更快
4. **结果限制** - 默认返回 100 行，可通过 `--limit` 调整

## 依赖

```bash
pip install requests
```
## 表快速查找

使用 `scripts/table_finder.py` 快速查找表和字段：

```bash
# 搜索表名
python3 scripts/table_finder.py --search "keyword"

# 查看表结构
python3 scripts/table_finder.py --desc your_table

# 搜索字段名（扫描所有表）
python3 scripts/table_finder.py --field "field_name"

# 列出所有表（按前缀分组）
python3 scripts/table_finder.py --list
```

## 查找重复数据

使用 `scripts/find_duplicates.py` 查找表中的重复数据并生成删除语句：

**适用场景：**
- TiDB 老版本唯一约束必须包含分区键，导致数据重复
- MySQL 分表合并到单表后出现重复
- 数据迁移导致的重复记录

### 基本用法

```bash
# 查询表中唯一约束字段重复的数据
python3 scripts/find_duplicates.py \
  --alias alias1 \
  --table your_table \
  --unique-fields field1,field2 \
  --date-field create_time \
  --start-date 2026-01-01

# 指定输出文件
python3 scripts/find_duplicates.py \
  --alias alias1 \
  --table your_table \
  --unique-fields field1,field2 \
  --output /tmp/duplicates.sql

# 不生成 DELETE 语句（仅查看）
python3 scripts/find_duplicates.py \
  --alias alias1 \
  --table your_table \
  --unique-fields field1,field2 \
  --no-delete
```

### 参数说明

| 参数 | 说明 | 必填 |
|------|------|------|
| `--table`, `-t` | 表名 | ✅ |
| `--unique-fields`, `-u` | 唯一约束字段（逗号分隔，不含分区键） | ✅ |
| `--date-field` | 日期/时间字段 | 默认 `create_time` |
| `--start-date`, `-s` | 开始日期 (YYYY-MM-DD) | ❌ |
| `--end-date`, `-e` | 结束日期 (YYYY-MM-DD) | ❌ |
| `--output`, `-o` | 输出文件路径 | ❌ |
| `--no-delete` | 不生成 DELETE 语句 | ❌ |
| `--alias`, `-a` | 实例别名 | ❌ |
| `--instance`, `-i` | 实例名 | ❌ |
| `--db`, `-d` | 数据库名 | ❌ |

### 输出说明

脚本会生成两个文件：

1. **`*.csv`** - 重复记录详情（id + 唯一字段 + 时间）
2. **`*.sql`** - DELETE 语句（分批，每批 50 条）

### 删除策略

- **保留**每个重复组中时间最早的那条记录
- **删除**后续重复的记录

### 示例输出

```
每日数据统计:
------------------------------------------------------------
2026-01-01: 总记录 10000, 唯一组合 10000, 重复记录 0
2026-01-02: 总记录 12000, 唯一组合 11990, 重复记录 10
2026-01-03: 总记录 11500, 唯一组合 11480, 重复记录 20
...

总重复记录: 30

2026-01-02: 找到 10 条需删除
2026-01-03: 找到 20 条需删除
...

总计需删除: 30 条

✅ 重复记录详情已保存到: /tmp/duplicates.csv
✅ DELETE 语句已保存到: /tmp/duplicates.sql
```

