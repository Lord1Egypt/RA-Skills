# Archery Query 配置示例

## Skill 安装目录

根据不同的 Claude 工具，skill 应该安装到对应的目录：

| 工具 | 安装目录 | 说明 |
|------|---------|------|
| **Claude Code (CLI)** | `~/.claude/skills/` | Claude Code CLI 默认 skill 目录 |
| **OpenClaw** | `~/.openclaw/skills/` | OpenClaw skill 目录 |
| **Hermes** | `~/.hermes/skills/` | Hermes skill 目录 |

**安装示例:**
```bash
# Claude Code CLI
cp -r archery-query ~/.claude/skills/

# OpenClaw
cp -r archery-query ~/.openclaw/skills/

# Hermes
cp -r archery-query ~/.hermes/skills/
```

## 配置文件结构

```
~/.archery/                     # 全局配置目录
├── config.json                 # 凭证配置（用户名/密码/URL）
└── cache/                      # 缓存目录
    ├── instances.json          # 实例别名配置
    ├── table_cache.json        # 表列表缓存
    └── session.json            # Session 缓存
```

## 凭证配置示例

文件: `~/.archery/config.json`

```json
{
  "archery_username": "your_username",
  "archery_password": "your_password",
  "archery_base_url": "http://archery.example.com:9123"
}
```

## 实例别名配置示例

文件: `~/.archery/cache/instances.json`

```json
{
  "prod": ["prod-instance", "prod-database"],
  "test": ["test-instance", "test-database"],
  "dev": {
    "instance": "dev-instance",
    "db": "dev-database"
  },
  "cte": ["cte-prod-instance", "cte_database"],
  "mdfe": ["mdfe-prod-instance", "mdfe_database"]
}
```

**格式说明:**
- 数组格式: `["instance_name", "database_name"]`
- 对象格式: `{"instance": "...", "db": "..."}`

两种格式都支持。

## 表缓存示例

文件: `~/.archery/cache/table_cache.json`

```json
{
  "prod-instance:prod-database": [
    "users",
    "orders",
    "products"
  ],
  "test-instance:test-database": [
    "test_table_1",
    "test_table_2"
  ]
}
```

## 安全配置

### 设置文件权限

```bash
chmod 600 ~/.archery/config.json
chmod 700 ~/.archery
```

### Git 忽略

**全局 gitignore (~/.gitignore):**
```
.archery/
```

## 常用命令

### 管理实例别名

```bash
# 列出所有别名
python3 ~/.claude/skills/archery-query/scripts/cache_config.py list

# 添加别名
python3 ~/.claude/skills/archery-query/scripts/cache_config.py add prod prod-instance prod-database

# 删除别名
python3 ~/.claude/skills/archery-query/scripts/cache_config.py remove prod

# 初始化缓存
python3 ~/.claude/skills/archery-query/scripts/cache_config.py init
```

### 清除缓存

```bash
# 清除指定实例的表缓存
python3 ~/.claude/skills/archery-query/scripts/cache_config.py clear-tables prod-instance prod-database

# 清除指定实例的所有缓存
python3 ~/.claude/skills/archery-query/scripts/cache_config.py clear-tables prod-instance

# 清除所有表缓存
python3 ~/.claude/skills/archery-query/scripts/cache_config.py clear-tables
```

## 多环境配置

你可以通过配置不同的实例别名来管理多个环境:

```json
{
  "prod": ["prod-instance", "prod-database"],
  "uat": ["uat-instance", "uat-database"],
  "dev": ["dev-instance", "dev-database"]
}
```

然后使用别名切换环境:

```bash
# 使用生产环境
python3 ~/.claude/skills/archery-query/scripts/archery_query.py --alias prod "SELECT ..."

# 使用测试环境
python3 ~/.claude/skills/archery-query/scripts/archery_query.py --alias uat "SELECT ..."
```