# Archery Query

通过 Archery SQL 审核平台查询数据库的技能。

## 功能特点

### 🚀 核心功能

1. **SQL 查询** - 执行任意 SQL 查询
   ```bash
   archery_query.py "SELECT * FROM your_table LIMIT 5"
   ```

2. **查询模板** - 常用查询一键执行
   ```bash
   archery_query.py --template failed_records --params limit=10
   ```

3. **数据库探索** - 查看数据库结构
   ```bash
   archery_query.py --list-dbs
   archery_query.py --list-tables your_database
   archery_query.py --desc your_table
   ```

### 📊 支持的数据库

- TiDB
- MySQL
- StarRocks

## 安装

### 1. 安装 Skill

根据使用的 Claude 工具，将 skill 安装到对应目录：

```bash
# Claude Code (CLI)
cp -r archery-query ~/.claude/skills/

# OpenClaw / Hermes 等其他工具请参考 references/config-example.md
```

### 2. 配置凭证

创建 `~/.archery/config.json` 文件：

```json
{
  "archery_username": "your_username",
  "archery_password": "your_password",
  "archery_base_url": "http://your-server:9123"
}
```

设置权限：
```bash
chmod 600 ~/.archery/config.json
```

### 2. 安装依赖

```bash
pip install requests
```

## 使用方法

### 基本查询

```bash
# 直接查询
python3 scripts/archery_query.py "SELECT * FROM your_table LIMIT 5"

# 使用别名
python3 scripts/archery_query.py --alias alias1 "SELECT * FROM your_table LIMIT 5"

# JSON 输出
python3 scripts/archery_query.py --format json "SELECT * FROM your_table LIMIT 5"
```

### 数据库探索

```bash
# 列出数据库
python3 scripts/archery_query.py --list-dbs

# 列出表
python3 scripts/archery_query.py --list-tables your_database

# 查看表结构
python3 scripts/archery_query.py --desc your_table
```

### 使用模板

```bash
# 使用预定义模板
python3 scripts/archery_query.py --template failed_records

# 自定义参数
python3 scripts/archery_query.py --template recent_records --params limit=20
```

## 配置实例别名

编辑 `scripts/archery_query.py`，修改 `DEFAULT_INSTANCES`：

```python
DEFAULT_INSTANCES = {
    "alias1": ("your-instance-name-1", "your-database-1"),
    "alias2": ("your-instance-name-2", "your-database-2"),
}
```

## 文件说明

```
archery-query/
├── SKILL.md                      # Skill 主文档
├── README.md                     # 本文件
├── scripts/
│   ├── archery_query.py          # 主查询脚本（推荐使用）
│   ├── archery_client.py         # Python 客户端
│   ├── archery_cli.py            # CLI 工具
│   └── archery_mcp_server.py     # MCP 服务器
```

## 查询模板

本 skill 提供通用查询模板（需根据实际情况修改）：

| 模板名 | 说明 |
|--------|------|
| `failed_records` | 查询失败的记录 |
| `recent_records` | 查询最近的记录 |
| `by_field` | 按字段查询 |

自定义模板：编辑 `scripts/archery_query.py` 中的 `QUERY_TEMPLATES`

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

## 注意事项

1. **凭证安全** - 配置文件包含密码，切勿提交到 git
2. **Session 管理** - 自动处理登录和 session，无需手动管理
3. **查询性能** - 使用索引字段查询更快
4. **结果限制** - 默认返回 100 行，可通过 `--limit` 调整

## 许可证

内部使用

## 作者

Claude Code Assistant
## 表快速查找工具

使用 `table_finder.py` 快速查找表和字段：

```bash
# 搜索表名（模糊匹配）
python3 scripts/table_finder.py --search "keyword"

# 查看表结构
python3 scripts/table_finder.py --desc your_table

# 搜索字段名
python3 scripts/table_finder.py --field "field_name"

# 列出所有表
python3 scripts/table_finder.py --list

# 指定实例和数据库
python3 scripts/table_finder.py --instance "your-instance" --db "your-db" --search "table"

# 刷新缓存
python3 scripts/table_finder.py --refresh
```

**功能特点：**
- 模糊搜索表名（支持包含匹配和相似度匹配）
- 搜索字段名（扫描所有表）
- 查看表结构（字段类型、索引等）
- 缓存机制（避免重复查询）
- 按前缀分组显示

