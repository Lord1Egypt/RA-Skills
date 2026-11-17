---
name: dbq
description: |-
  Multi-database SQL assistant — query MySQL, PostgreSQL, SQLite & MariaDB
  across dev/test/prod environments with a single command.
  Security-first: read-only by default, DML/DDL gating, EXPLAIN analysis.
  多数据库查询助手，一个命令搞定 MySQL/PostgreSQL/SQLite/MariaDB 和多套环境。
agent_created: true
---

# 数据库操作技能 (dbq)

基于预配置连接信息的多环境数据库操作工具。默认只读，写操作需通过 YAML 配置显式开启。

## 触发条件

- 用户要求执行 SQL 查询/写入并指定了数据库别名
- 用户想查看某个数据库的表列表
- 用户想查看已配置了哪些数据库连接
- 用户想预览写操作（--dry-run）

## 支持的数据库

| 数据库 | 驱动 | 额外依赖 | 支持程度 |
|--------|------|---------|---------|
| **SQLite** | `sqlite3` (标准库) | 无 | ✅ 全部功能 |
| MySQL | `pymysql` | `pip install pymysql` | ✅ 全部功能 |
| MariaDB | `pymysql` | `pip install pymysql` | ✅ 全部功能 |
| PostgreSQL | `psycopg2` | `pip install psycopg2-binary` | ✅ 全部功能 |

**默认配置**：dev 环境开箱自带一个 `sqlite_test` 内存数据库，无需安装任何依赖即可测试。

## 多环境架构

每个环境一个独立配置文件，结构完全对称：

| 环境 | 配置文件 | 密码 Keychain 条目 |
|------|---------|-------------------|
| dev (默认) | `connections.dev.yaml` | `dbq/dev/{alias}` |
| test | `connections.test.yaml` | `dbq/test/{alias}` |
| prod | `connections.prod.yaml` | `dbq/prod/{alias}` |

默认环境为 `dev`，可通过环境变量 `DB_QUERY_DEFAULT_ENV=test` 修改。

### 首次配置

```bash
# 1. 生成配置文件 (⚠️ 只做一次！已存在则跳过)
python scripts/query.py --init-config

# 2. 编辑填入各环境的 host / user / database
vim assets/connections.dev.yaml
# Prod 建议额外 chmod 600 (--init-config 已自动设置):
chmod 600 assets/connections.prod.yaml

# 3. 密码 (三选一，按优先级)
#    a) Keychain (推荐):
python scripts/query.py --keychain-set recharge_db --env dev
python scripts/query.py --keychain-set recharge_db --env test
python scripts/query.py --keychain-set recharge_db --env prod
#    b) .env 文件 (--init-config 已生成):
# 编辑 assets/.env 填入 DB_PWD_DEV_RECHARGE_DB=xxx 等
#    c) 环境变量: export DB_PWD_DEV_RECHARGE_DB=xxx
```

**密码不存入任何 YAML 配置文件。** 脚本按优先级自动查找：Keychain > `.env` 变量 > 环境变量。

支持三种密码配置方式：

| 方式 | YAML 配置 | 密码来源 | 适用场景 |
|------|----------|---------|---------|
| 约定查找 | 不写 `password` 字段 | `DB_PWD_{ENV}_{ALIAS}` | 每库一个独立密码 |
| `${VAR}` 占位 | `password: ${PWD_PROD}` | `.env` 的 `PWD_PROD` 变量 | **多库共享密码（推荐）** |
| 环境变量 | `password: ${MY_PASS}` | `os.environ["MY_PASS"]` | CI/CD 注入 |

Keychain 条目格式：`service=dbq/{env}/{alias}`，例如 `dbq/dev/recharge_db`。

### 🔒 安全红线

- **永远不要用 Read 工具直接读取 `assets/connections*.yaml` 或 `assets/.env`。**
- 所有操作（查询、列表、查看配置）一律通过 `scripts/query.py` 脚本执行。
- 要查看已配置连接 → `python scripts/query.py --list`
- 要查看数据库表 → `python scripts/query.py --env dev <别名> --show`
- 要执行查询 → `python scripts/query.py --env dev <别名> "<SQL>"`
- 如果脚本报错提示文件不存在 → 告知用户需要配置，**不要自己去读文件检查**。

## 使用方式

### 查询数据

```bash
python scripts/query.py <db_alias> "SELECT ..."                    # 默认 dev
python scripts/query.py --env test <db_alias> "SELECT ..."          # 切 test
python scripts/query.py --env prod <db_alias> "SELECT ..."          # 切 prod
python scripts/query.py --config my-prod.yaml <db_alias> "SELECT ..." # 自定义配置文件
```

示例：
```bash
  # 日常 dev 查询（不用写 --env）
  python scripts/query.py recharge_db "SELECT id, name FROM users"
  # → 📊 [dev] EXPLAIN: type=ref | key=idx_mobile | rows=42 → 返回前 100 行

# 切到 prod
python scripts/query.py --env prod recharge_db "SELECT COUNT(*) FROM orders"
# → 自动读取 connections.prod.yaml + prod keychain

# 指定限制
python scripts/query.py --env test recharge_db "SELECT * FROM orders" --limit 500

# 只看行数
python scripts/query.py --env prod recharge_db "SELECT * FROM users" --count

# JSON 输出
python scripts/query.py --env dev recharge_db "SELECT * FROM orders" --format json
```

### 大表保护机制

- 执行前自动 EXPLAIN 预估扫描行数 + 索引使用情况（`type=ref | key=idx_mobile | rows=42`）
- 全表扫描明确标记（`type=ALL (全表扫描)`）
- 无 LIMIT 的 SELECT 自动追加 `LIMIT 100`
- 预估行数 > 50K 时显示醒目警告
- `--count` 只跑 COUNT(*) 不取数据
- `--no-limit` 明确需要全量数据时使用

### 查看表结构 (列 + 索引表格格式)

```bash
python scripts/query.py <db_alias> --desc <TABLE>      # 单表结构
python scripts/query.py <db_alias> --desc ALL           # 全部表结构
python scripts/query.py <db_alias> -d "user_*"          # 通配符匹配
python scripts/query.py --env prod <db_alias> -d t_user # prod 环境
```

输出 SHOW FULL COLUMNS（Field/Type/Null/Key/Default/Extra/Comment）+ SHOW INDEX 两张表格。支持 `--format json/csv`。

### 查看建表 DDL

```bash
python scripts/query.py <db_alias> --ddl <TABLE>       # 单表 DDL
python scripts/query.py <db_alias> --ddl ALL            # 全部表 DDL
python scripts/query.py <db_alias> --ddl "order_*"      # 通配符匹配
```

输出完整的 `CREATE TABLE` 语句（含字段注释、索引、主键、ENGINE 等），与 `SHOW CREATE TABLE` 完全一致。

### 连接测试

```bash
python scripts/query.py <db_alias> --ping               # 快速验证连接
python scripts/query.py --env prod <db_alias> --ping    # 指定环境
```

### 查询超时

```bash
python scripts/query.py <db_alias> "SELECT ..." --timeout 30   # 30s 超时
```

### 列出数据库表 (含 COMMENT + 预估行数)

```bash
python scripts/query.py --env dev <db_alias> --show           # 全部表
python scripts/query.py --env dev <db_alias> -s "user_*"      # 通配符匹配
python scripts/query.py --env dev <db_alias> -s user_info     # 单表元信息
python scripts/query.py --env prod <db_alias> -s --format json # JSON 输出
```

输出 Table / Rows / Comment 三列，一目了然库中有哪些表、各表多少数据。

### 列出所有已配置连接

```bash
python scripts/query.py --list              # 扫描所有 connections.*.yaml
python scripts/query.py --list --env prod   # 只看 prod
```

输出示例：
```
默认环境: dev

环境        别名                   类型        主机                 端口     数据库
dev *       recharge_db           mysql       10.18.122.60        3306     recharge
test        recharge_db           mysql       10.18.122.61        3306     recharge
prod        recharge_db           mysql       10.19.xx.xx         3306     recharge
```

## 前置依赖

执行查询前确认依赖已安装，详见 `references/drivers.md`：

- MySQL/MariaDB: `pip install pymysql`
- PostgreSQL: `pip install psycopg2-binary`
- YAML 配置: `pip install pyyaml`（或使用 JSON 格式）

## 安全限制

- **默认只读**：所有连接默认 `readonly: true`，DML/DDL 需显式配置
- **操作分级**：
  - 只读 (SELECT/SHOW/DESCRIBE/EXPLAIN) — 始终允许
  - DML (INSERT/UPDATE/DELETE/REPLACE) — 需 `readonly: false`
  - DDL (ALTER/CREATE/DROP/TRUNCATE) — 需 `allow_ddl: true`
  - 禁止 (CALL/GRANT/SET/EXECUTE) — 始终拒绝
- **无 WHERE 保护**：DELETE/UPDATE 无 WHERE 直接拒绝
- **确认提示**：prod 环境写操作强制交互确认（`DB_QUERY_ASSUME_YES=1` 跳过）
- 密码不存储在任何配置文件中
- **严禁将 `assets/connections*.yaml` 或 `assets/.env` 读入 AI 上下文**
- **严禁删除 assets/ 下的任何 .yaml 或 .env 文件**（用户配置文件，`rm -f` 一律禁止）
- **修改 assets/ 下任何用户配置文件前必须先备份**：`cp file.yaml file.yaml.bak-$(date +%Y%m%d-%H%M%S)`，再执行修改
- **严禁用 Write 工具创建/覆盖已存在的用户配置文件**——如果文件已存在，只允许 Edit 追加
- 清理操作仅限于 `/tmp`、`tempfile` 创建的临时目录，绝不触碰 `assets/`

### 写操作配置示例

```yaml
# assets/connections.dev.yaml
settings:
  readonly_mode: false         # 环境级：整个 dev 环境允许 DML

connections:
  sqlite_test:
    type: sqlite
    path: ":memory:"
    readonly: false            # 连接级：此连接允许 DML

  prod_readonly:
    type: mysql
    host: 10.19.xx.xx
    user: readonly
    password: ${PWD_PROD}
    database: recharge
    # readonly 不写 = 默认 true，只读安全
```

## 测试

无需数据库即可验证所有逻辑：

```bash
cd ~/.workbuddy/skills/dbq
python3 scripts/test.py
```

测试覆盖：YAML 加载、`${VAR}` 占位符解析、SQL 校验与分级、密码解析链、SQL 工具函数、CLI 参数、通配符匹配、日志记录、写操作权限、无 WHERE 拦截。

## 查询日志

所有操作自动记录到 `logs/YYYY-MM-DD.log`，写操作额外标注类型：

```
[2026-06-30 11:00:00] dev:test_db | SELECT * FROM users LIMIT 100 | 100 rows | 0.009s | OK
[2026-06-30 11:00:05] dev:test_db | WRITE | DELETE FROM users WHERE id=1 | 1 rows | 0.003s | OK
[2026-06-30 11:00:10] dev:test_db | DDL | CREATE TABLE t(id INT) | 0 rows | 0.002s | OK
```

`logs/` 目录首次查询时自动创建。

**注意：`python scripts/query.py --init-config` 已存在则跳过**，更新技能后重新运行是安全的，不会覆盖你已编辑的配置。
