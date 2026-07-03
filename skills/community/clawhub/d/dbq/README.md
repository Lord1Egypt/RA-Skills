# dbq — 多环境数据库查询与写入 CLI 工具（AI 助手通用）

一个通用的**数据库 CLI 工具** / **数据库操作技能**，让 **Claude Code**、**OpenCode**、**Cursor**、**WorkBuddy** 等任意 AI 编程助手通过预配置的数据库别名按环境执行 SQL 操作。支持查询 / 插入 / 更新 / 删除 / 改表，写操作由 YAML 配置精确控制。可作为 AI 编程助手的数据库工具（db skill / database skill）直接集成，不用再给 AI 贴 host/port/user —— 告诉它别名和语句即可。

[English](./README_EN.md)

## 支持的数据库

| 数据库 | 驱动 | 额外依赖 | 支持程度 |
|--------|------|---------|---------|
| **SQLite** | `sqlite3`（标准库） | **零依赖** | ✅ 全部功能 |
| MySQL | `pymysql` | `pip install pymysql` | ✅ 全部功能 |
| MariaDB | `pymysql` | `pip install pymysql` | ✅ 全部功能 |
| PostgreSQL | `psycopg2` | `pip install psycopg2-binary` | ✅ 全部功能 |

**开箱即用**：dev 环境自带 `sqlite_test` 文件数据库配置，无需安装任何依赖即可测试全部功能。

## 支持的 AI 助手

任何能执行 shell 命令的 AI agent 均可使用：

| AI 助手 | 使用方式 |
|---------|---------|
| **Claude Code** | `python3 scripts/query.py my_db "SELECT ..."` |
| **OpenCode** | 终端直接执行，或用 `/run` 命令 |
| **Hermes** | 作为自定义 tool 注册，或在对话中 shell 执行 |
| **Cursor Agent** | Terminal 模式直接运行，或在 `.cursorrules` 中声明 |
| **WorkBuddy** | 安装为 skill，AI 自动识别调用 |
| **GitHub Copilot** | CLI 模式直接执行 |
| **Aider** | `/run python3 scripts/query.py ...` |
| **通义灵码 / Comate** | 终端执行 |

本质就是一条 shell 命令，不依赖任何特定平台的 API 或插件。

## 特性

### 查询与浏览
- **多环境隔离**：`dev` / `test` / `prod` 三套独立配置文件，一个 `--env` 参数秒切环境
- **安全密码管理**：三级查找链 —— macOS Keychain → `.env` 文件 → 环境变量，密码**永不写入 YAML**
- **大表自动保护**：查询前自动 EXPLAIN 预估行数，> 50K 行醒目警告，自动注入 `LIMIT 100`
- **EXPLAIN 索引透视**：显示 `type=ref | key=idx_mobile | rows=42`，全表扫描直接标记 `type=ALL (全表扫描)`
- **表结构三模式**：`--show` 看全局（含表注释 + 行数），`--desc` 看列 + 索引（表格），`--ddl` 复制完整建表语句
- **通配符批量操作**：`--show "user_*"`、`--desc "order_*"`、`--ddl "log_*"` 一次匹配多张表
- **连接复用**：批量操作（`--desc ALL` / `--ddl ALL`）N 张表仅 1 次建连

### 写操作
- **YAML 配置控制**：写操作不通过 CLI 参数开启，必须在配置文件中设 `readonly: false` / `allow_ddl: true`
- **四级 SQL 分类**：READ（SELECT/SHOW）始终允许 → DML（INSERT/UPDATE/DELETE）需 `readonly: false` → DDL（ALTER/CREATE/DROP）需 `allow_ddl: true` → BLOCKED（GRANT/SET/CALL）始终拒绝
- **无 WHERE 保护**：DELETE/UPDATE 无 WHERE 直接拒绝，防止误删全表
- **`--dry-run` 预览**：执行前预览 SQL + EXPLAIN 计划，确认无误再真正执行
- **`--limit` 限行**：DELETE/UPDATE 支持 `--limit N` 手动控制影响行数
- **prod 确认提示**：生产环境写操作强制交互确认，`DB_QUERY_ASSUME_YES=1` 环境变量用于非交互/AI Agent 模式

### 运维
- **查询日志**：所有 SQL（含 EXPLAIN + 操作类型标签）自动记入 `logs/YYYY-MM-DD.log`，完整追溯链
- **连接测试**：`--ping` 快速验证连接可用性

## 快速开始

### 1. 安装依赖

```bash
pip install pyyaml pymysql
# PostgreSQL 用户额外安装:
pip install psycopg2-binary
# SQLite 用户无需安装任何依赖（Python 标准库自带）
```

### 2. 配置连接

```bash
# 生成配置模板（已存在则跳过，安全可重复执行）
python3 scripts/query.py --init-config

# 编辑填入你的 host / user / database
vim assets/connections.dev.yaml
```

`connections.dev.yaml` 示例：

```yaml
# 环境级设置
settings:
  readonly_mode: false       # false 允许 DML 写操作

connections:
  my_db:
    type: mysql
    host: 127.0.0.1
    port: 3306
    user: root
    password: ${MY_DB_PASS}  # 引用 .env 变量，不写明文
    database: mydb
    readonly: false          # 此连接允许 INSERT/UPDATE/DELETE
    allow_ddl: true          # 此连接允许 ALTER/CREATE/DROP

  sqlite_test:               # 零依赖测试连接
    type: sqlite
    path: /tmp/test.db
    readonly: false
    allow_ddl: true
```

### 3. 配置密码（三选一，推荐 Keychain）

| 方式 | 命令 | 安全性 |
|------|------|--------|
| **A. Keychain** | `python3 scripts/query.py --keychain-set my_db --env dev` | ⭐⭐⭐ 系统级加密 |
| **B. .env 文件** | `echo "MY_DB_PASS=xxx" >> assets/.env` | ⭐⭐ 本地文件 |
| **C. 环境变量** | `export MY_DB_PASS=xxx` | ⭐ CI/CD 注入 |

### 4. 验证连接

```bash
python3 scripts/query.py my_db --ping
# → ✅ [my_db] (dev) 连接成功 (mysql) - 0.012s

python3 scripts/query.py --env prod my_db --ping
# → ✅ [my_db] (prod) 连接成功 (mysql) - 0.008s
```

## 使用示例

### 查询数据

```bash
# ═══ 基本查询 ═══
python3 scripts/query.py my_db "SELECT * FROM users WHERE status=1"
# → 📊 [dev] EXPLAIN: type=ref | key=idx_status | rows=156 → 自动 LIMIT 100

python3 scripts/query.py --env prod my_db "SELECT COUNT(*) FROM orders"

# --multi 一次连接执行多条 SELECT（分号分隔）
python3 scripts/query.py my_db --multi "
  SELECT COUNT(*) FROM users;
  SELECT * FROM users WHERE status=1 LIMIT 5;
  SELECT COUNT(*) FROM orders
"

# --count 只看行数不取数据
python3 scripts/query.py my_db "SELECT * FROM orders WHERE status=1" --count

# --no-limit 明确要全量
python3 scripts/query.py my_db "SELECT * FROM config" --no-limit

# --timeout 超时保护
python3 scripts/query.py my_db "SELECT * FROM big_table" --timeout 30

# ═══ 浏览表 ═══
python3 scripts/query.py my_db --show                     # 全部表（含注释 + 预估行数）
python3 scripts/query.py my_db -s "user_*"                # 通配符匹配
python3 scripts/query.py my_db -s "user_*" --format json  # JSON 输出

# ═══ 表结构 ═══
python3 scripts/query.py my_db -d users                   # 表结构（表格：列 + 索引）
python3 scripts/query.py my_db --ddl users                # 完整 CREATE TABLE DDL
python3 scripts/query.py my_db -d "order_*"               # 通配符批量

# ═══ 格式 ═══
python3 scripts/query.py my_db "SELECT * FROM users" --format json
python3 scripts/query.py my_db "SELECT * FROM users" --format csv
python3 scripts/query.py my_db -d users --format json     # 表结构也支持
```

### 写入数据

```bash
# ═══ 插入 ═══
DB_QUERY_ASSUME_YES=1 python3 scripts/query.py my_db \
  "INSERT INTO users (name, email) VALUES ('张三', 'zs@test.com')"

# 批量插入
DB_QUERY_ASSUME_YES=1 python3 scripts/query.py my_db \
  "INSERT INTO users (name, email) VALUES ('李四', 'ls@test.com'), ('王五', 'ww@test.com')"

# ═══ 更新 ═══
# 先 --dry-run 预览（不执行）
DB_QUERY_ASSUME_YES=1 python3 scripts/query.py my_db \
  "UPDATE users SET status=0 WHERE id=1" --dry-run

# 确认无误后执行
DB_QUERY_ASSUME_YES=1 python3 scripts/query.py my_db \
  "UPDATE users SET status=0 WHERE id=1"

# 批量更新 + --limit 限制行数
DB_QUERY_ASSUME_YES=1 python3 scripts/query.py my_db \
  "UPDATE logs SET archived=1 WHERE created_at < '2025-01-01'" --limit 1000

# ═══ 删除 ═══
# 条件删除
DB_QUERY_ASSUME_YES=1 python3 scripts/query.py my_db \
  "DELETE FROM temp_logs WHERE created_at < '2025-01-01'" --limit 500

# 无 WHERE 会被拦截
python3 scripts/query.py my_db "DELETE FROM users"
# → ❌ 拒绝：DELETE 必须带 WHERE 条件

# ═══ 改表 (DDL) ═══
DB_QUERY_ASSUME_YES=1 python3 scripts/query.py my_db \
  "ALTER TABLE users ADD COLUMN dept VARCHAR(50) DEFAULT '技术部'"

DB_QUERY_ASSUME_YES=1 python3 scripts/query.py my_db \
  "CREATE INDEX idx_users_dept ON users (dept)"

# ═══ 全局 ═══
python3 scripts/query.py --list                           # 扫描全部环境的连接
python3 scripts/query.py --list --env prod                # 只看 prod
```

## 在 AI 助手对话中使用

安装后，直接对 AI 说：

> 查一下 dev 环境 mydb 的 orders 表，最近 10 条未支付记录

> 往 test 环境 users 表里插入一条测试数据：name=张三, email=zs@test.com

> 用 --dry-run 预览一下删除过期日志的 SQL

AI 会自动构造 `python3 scripts/query.py ...` 命令并执行。这个 **AI 数据库工具** 对不同助手略有差异：

**Claude Code / Cursor Agent / Hermes** —— 直接对话，AI 会自动调用 shell：

```
帮我看看 prod 环境 user_db 有哪些表，找一下 user_info 表结构
```

**如果想更可靠地注册为自定义 tool**（如 Claude Code 的 custom slash commands、OpenCode 的 commands）：

```bash
# 设置别名方便调用
alias dbq='python3 ~/.workbuddy/skills/dbq/scripts/query.py'
dbq my_db -d users
```

## 命令参考

| 命令 | 说明 |
|------|------|
| `<alias> "SQL"` | 执行 SQL（查询或写入） |
| `--list` | 扫描所有环境的已配置连接 |
| `--show [TABLE]` | 列出数据库表（含注释+行数），支持通配符 |
| `-d TABLE / ALL / "pat*"` | 表结构（列+索引表格） |
| `--ddl TABLE / ALL / "pat*"` | 完整 CREATE TABLE 语句 |
| `--ping` | 测试连接是否可用 |
| `--count` | 只跑 COUNT(*)，不取数据 |
| `--limit N` | 查询：指定返回行数（默认 100）；写操作：限制 DELETE/UPDATE 影响行数 |
| `--no-limit` | 取消自动 LIMIT（仅查询） |
| `--dry-run` | 预览写操作 SQL + EXPLAIN，不执行 |
| `--multi` | 执行多条 SELECT（分号分隔），一次连接 |
| `--timeout N` | 查询超时秒数 |
| `--keychain-set` | 将密码存入 macOS Keychain |
| `--format json/csv` | 输出格式 |

通用参数：`--env dev|test|prod`（默认 dev），`--config <file>`（自定义配置文件）

环境变量：

| 变量 | 说明 |
|------|------|
| `DB_QUERY_DEFAULT_ENV` | 修改默认环境（默认 `dev`） |
| `DB_QUERY_ASSUME_YES` | 设为 `1` 跳过写操作确认提示（非交互/AI Agent 模式） |

## 目录结构

```
dbq/
├── SKILL.md                           # WorkBuddy 技能入口
├── README.md                          # 中文文档（GitHub 默认展示）
├── README_EN.md                       # English docs
├── scripts/
│   ├── query.py                       # 主脚本
│   └── test.py                        # 单元测试（无需数据库）
├── assets/
│   ├── connections.dev.yaml           # 开发默认配置（含 sqlite_test） ✅ 已提交
│   ├── connections.dev.yaml.example   # 开发环境模板 ✅ 已提交
│   ├── connections.test.yaml.example  # 测试环境模板 ✅ 已提交
│   ├── connections.prod.yaml.example  # 生产环境模板 ✅ 已提交
│   ├── .env.example                   # 密码模板 ✅ 已提交
│   ├── connections.test.yaml          # ❌ 本地配置，不提交 Git
│   ├── connections.prod.yaml          # ❌ 本地配置，不提交 Git
│   └── .env                           # ❌ 密码文件，不提交 Git
├── references/
│   └── drivers.md                     # 驱动安装说明
└── logs/                              # ❌ 查询日志，不提交 Git
    └── YYYY-MM-DD.log
```

## 运行测试

无需数据库连接即可验证所有核心逻辑：

```bash
python3 scripts/test.py
# → 110/110 通过 🎉
```

测试覆盖：YAML 加载、`${VAR}` 占位符解析、SQL 分类与校验（READ/DML/DDL/BLOCKED）、写操作权限解析、无 WHERE 拦截、--dry-run、--limit 对 DML、密码解析链、CLI 参数、通配符匹配、日志记录。

## 安全说明

- `assets/connections*.yaml`（含密码的）和 `assets/.env` 已加入 `.gitignore`，**绝不会被提交**
- 密码不存储在 YAML 中，通过 Keychain / .env / 环境变量运行时注入
- **四级操作分级**：
  - READ（SELECT/SHOW/DESCRIBE/EXPLAIN）-- 始终允许
  - DML（INSERT/UPDATE/DELETE/REPLACE）-- 需配置 `readonly: false`
  - DDL（ALTER/CREATE/DROP/TRUNCATE）-- 需配置 `allow_ddl: true`
  - BLOCKED（CALL/GRANT/SET/EXECUTE）-- 始终拒绝
- **无 WHERE 保护**：DELETE/UPDATE 无 WHERE 直接拒绝，全表操作需 `WHERE 1=1`
- **prod 确认**：生产环境写操作强制交互确认
- 查询日志仅存本地 `logs/` 目录，不上传
- **严禁 AI 直接读取 `assets/connections*.yaml` 或 `assets/.env`** —— 密码通过运行时环境变量注入

## License

MIT
