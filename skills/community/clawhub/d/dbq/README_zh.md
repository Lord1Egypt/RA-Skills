# dbq — 多环境数据库查询 CLI 工具（AI 助手通用）

一个通用的命令行工具，让 **Claude Code**、**OpenCode**、**Hermes**、**Cursor**、**WorkBuddy** 等任意 AI 编程助手通过预配置的数据库别名按环境执行只读 SQL 查询。不用再给 AI 贴 host/port/user — 告诉它别名和查询语句即可。

[English](./README_EN.md)

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

- **多环境隔离**：`dev` / `test` / `prod` 三套独立配置文件，一个 `--env` 参数秒切环境
- **安全密码管理**：三级查找链 — macOS Keychain → `.env` 文件 → 环境变量，密码**永不写入 YAML**
- **大表自动保护**：查询前自动 EXPLAIN 预估行数，> 50K 行醒目警告，自动注入 `LIMIT 100`
- **EXPLAIN 索引透视**：显示 `type=ref | key=idx_mobile | rows=42`，全表扫描直接标记 `type=ALL (全表扫描)`
- **表结构三模式**：`--show` 看全局（含表注释 + 行数），`--desc` 看列 + 索引（表格），`--ddl` 复制完整建表语句
- **通配符批量操作**：`--show "user_*"`、`--desc "order_*"`、`--ddl "log_*"` 一次匹配多张表
- **查询日志**：所有 SQL（含 EXPLAIN）自动记入 `logs/YYYY-MM-DD.log`，完整追溯链
- **连接复用**：批量操作（`--desc ALL` / `--ddl ALL`）N 张表仅 1 次建连
- **仅只读**：SELECT / SHOW / DESCRIBE / EXPLAIN，INSERT/UPDATE/DELETE/DROP 一律拒绝

## 快速开始

### 1. 安装依赖

```bash
pip install pyyaml pymysql
# PostgreSQL 用户额外安装:
pip install psycopg2-binary
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
connections:
  my_db:
    type: mysql
    host: 127.0.0.1
    port: 3306
    user: root
    password: ${MY_DB_PASS}   # 引用 .env 变量，不写明文
    database: mydb
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

```bash
# ═══ 查询 ═══
python3 scripts/query.py my_db "SELECT * FROM users WHERE status=1"
# → 📊 [dev] EXPLAIN: type=ref | key=idx_status | rows=156
# → 自动 LIMIT 100

python3 scripts/query.py --env prod my_db "SELECT COUNT(*) FROM orders"

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

# ═══ 全局 ═══
python3 scripts/query.py --list                           # 扫描全部环境的连接
python3 scripts/query.py --list --env prod                # 只看 prod

# ═══ 格式 ═══
python3 scripts/query.py my_db "SELECT * FROM users" --format json
python3 scripts/query.py my_db "SELECT * FROM users" --format csv
python3 scripts/query.py my_db -d users --format json     # 表结构也支持
```

## 在 AI 助手对话中使用

安装后，直接对 AI 说：

> 查一下 dev 环境 mydb 的 orders 表，最近 10 条未支付记录

AI 会自动构造 `python3 scripts/query.py ...` 命令并执行。不同 AI 助手略有差异：

**Claude Code / Cursor Agent / Hermes** — 直接对话，AI 会自动调用 shell：

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
| `<alias> "SQL"` | 执行只读查询 |
| `--list` | 扫描所有环境的已配置连接 |
| `--show [TABLE]` | 列出数据库表（含注释+行数），支持通配符 |
| `-d TABLE / ALL / "pat*"` | 表结构（列+索引表格） |
| `--ddl TABLE / ALL / "pat*"` | 完整 CREATE TABLE 语句 |
| `--ping` | 测试连接是否可用 |
| `--count` | 只跑 COUNT(*)，不取数据 |
| `--limit N` | 指定返回行数（默认 100） |
| `--no-limit` | 取消自动 LIMIT |
| `--timeout N` | 查询超时秒数 |
| `--keychain-set` | 将密码存入 macOS Keychain |
| `--format json/csv` | 输出格式 |

通用参数：`--env dev|test|prod`（默认 dev），`--config <file>`（自定义配置文件）

## 目录结构

```
dbq/
├── SKILL.md                           # WorkBuddy 技能入口
├── README.md                           # 中文文档（GitHub 默认展示）
├── README_EN.md                       # English docs
├── scripts/
│   ├── query.py                       # 主脚本
│   └── test.py                        # 单元测试（无需数据库）
├── assets/
│   ├── connections.dev.yaml.example   # 开发环境模板 ✅ 已提交
│   ├── connections.test.yaml.example  # 测试环境模板 ✅ 已提交
│   ├── connections.prod.yaml.example  # 生产环境模板 ✅ 已提交
│   ├── .env.example                   # 密码模板 ✅ 已提交
│   ├── connections.dev.yaml           # ❌ 本地配置，不提交 Git
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
# → 64/64 通过 🎉
```

## 安全说明

- `assets/connections*.yaml` 和 `assets/.env` 已加入 `.gitignore`，**绝不会被提交**
- 密码不存储在 YAML 中，通过 Keychain / .env / 环境变量运行时注入
- 只允许只读：SELECT / SHOW / DESCRIBE / EXPLAIN，任何 DML 会被拒绝
- 查询日志仅存本地 `logs/` 目录，不上传
- **严禁 AI 直接读取 `assets/connections*.yaml` 或 `assets/.env`** — 密码通过运行时环境变量注入

## License

MIT
