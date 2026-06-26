---
name: db-toolkit
description: |
  轻量级多数据库操作工具，支持 MySQL/PostgreSQL/SQLite 的 DDL/DML 操作和 Schema 探索。
  
  触发场景：
  - 用户说"连接数据库"、"测试数据库连接"、"连接MySQL/PostgreSQL/SQLite"
  - 用户说"查看表结构"、"列出所有表"、"查看 users 表有哪些字段"
  - 用户说"执行SQL"、"查询数据"、"插入数据"、"更新数据"、"删除数据"
  - 用户说"创建表"、"修改表结构"、"删除表"、"添加字段"
  - 任何涉及数据库 DDL/DML 操作的请求
---

# Database Toolkit

轻量级数据库操作工具，支持 MySQL、PostgreSQL、SQLite 三大主流数据库。

## 核心原则

1. **智能发现优先** - 先尝试从项目中自动发现连接信息，找不到再询问
2. **每次操作都传入连接信息** - 不持久化存储，会话结束后自动遗忘
3. **安全第一** - 连接信息仅在当前会话有效，不写入任何文件
4. **必须查询真实数据库** - 见下方【重要】章节

## ⚠️ 重要：必须查询真实数据库

**禁止行为：**
- ❌ 读取项目中的 `schema.sql`、`init.sql` 等文件来回答表结构
- ❌ 读取 ORM 的 model/entity 文件来推断表结构
- ❌ 基于代码或配置文件假设数据库状态

**必须行为：**
- ✅ 使用 `scripts/list-tables.ts` 查询实际数据库中的表列表
- ✅ 使用 `scripts/describe-table.ts` 查询实际数据库中的表结构
- ✅ 通过实际连接获取真实、实时的数据库信息

**原因：**
1. 项目文件可能不是最新的（代码与数据库可能不同步）
2. 数据库可能有手动修改（未反映在代码中）
3. 用户需要的是**实际数据库**的状态，不是代码中的定义
4. schema.sql 只是模板，不包含实际数据

**正确示例：**
```
用户问："查看 users 表有哪些字段"
❌ 错误：读取 schema.sql 或 User.java 来回答
✅ 正确：运行 describe-table.ts 脚本查询实际数据库
```

**唯一例外：**
- 用户明确要求"查看 schema.sql 文件"或"查看代码中的表定义"时，才读取项目文件

## 工作流程

```
用户请求
    │
    ▼
检查是否已有连接信息
    │
    ├──▶ 有 ──▶ 直接使用
    │
    └──▶ 无 ──▶ 智能探索项目（见下方）
                    │
                    ├──▶ 找到一个 ──▶ 直接使用
                    │
                    ├──▶ 找到多个 ──▶ 询问用户选择哪个
                    │
                    └──▶ 未找到 ──▶ 询问用户提供连接信息
```

## 智能探索连接信息

当用户未提供连接信息时，**先尝试从项目中自动发现**：

### 探索策略

使用 glob 和 read 工具，按优先级搜索：

```
1. 环境变量文件
   - .env, .env.local, .env.development, .env.production

2. 应用配置文件（常见框架）
   - **Spring Boot**: application.yml, application.yaml, application.properties
     （注意：可能在 backend/, server/, api/ 等子目录）
   - **Node.js**: config/database.yml, config/database.yaml, knexfile.*, drizzle.config.*
   - **Django**: settings.py
   - **Rails**: config/database.yml, config/database.yaml
   - **Laravel**: .env, config/database.php

3. ORM 配置
   - **Prisma**: prisma/schema.prisma
   - **Drizzle**: drizzle.config.ts, drizzle.config.js
```

### 探索命令示例

```bash
# 查找环境变量文件
glob pattern=".env*"

# 查找 Spring Boot 配置（支持 monorepo）
glob pattern="**/application*.yml"
glob pattern="**/application*.yaml"
glob pattern="**/application*.properties"

# 查找 Node.js 配置
glob pattern="**/database.{yml,yaml,json,js,ts}"
glob pattern="**/knexfile.{js,ts}"

# 查找 Prisma/Drizzle
glob pattern="**/schema.prisma"
glob pattern="**/drizzle.config.{js,ts}"
```

### 解析配置文件

找到配置文件后，读取并提取连接信息：

**关键变量名：**
- URL 形式：`DATABASE_URL`, `DB_URL`, `MYSQL_URL`, `POSTGRES_URL`, `spring.datasource.url`
- 分开形式：`DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_DATABASE`

**示例解析：**

```yaml
# Spring Boot application.yml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/mydb
    username: root
    password: secret
```

```env
# .env
DATABASE_URL=mysql://root:secret@localhost:3306/mydb
```

```typescript
// drizzle.config.ts
export default {
  connection: 'mysql://root:secret@localhost:3306/mydb'
}
```

### 处理环境变量占位符

配置文件可能包含占位符，需要解析：

```yaml
# 带默认值的占位符
url: jdbc:mysql://${DB_HOST:localhost}:${DB_PORT:3306}/${DB_NAME:mydb}
```

解析规则：
1. 如果 `${VAR_NAME:default}` 格式，优先读取环境变量
2. 如果环境变量不存在，使用默认值
3. 提取最终的连接信息

### 找到多个连接时的处理

如果发现多个数据库连接配置，使用 ask-user-question 询问用户：

```
发现以下数据库连接：
1. MySQL - localhost:3306/mydb (来自 application.yml)
2. PostgreSQL - localhost:5432/app ( 来自 .env)

请问要使用哪个？
```

## 连接信息格式

收集到的连接信息统一转换为以下格式：

```
数据库类型: mysql / postgresql / sqlite
主机: localhost
端口: 3306
用户名: root
密码: secret
数据库名: mydb

# 或 URL 形式
mysql://root:secret@localhost:3306/mydb
```

## 脚本使用

### 首次使用（安装依赖）

技能脚本依赖 TypeScript 运行时和数据库驱动，需要全局安装：

```bash
npm install -g tsx mysql2 pg better-sqlite3
```

> **注意**：`better-sqlite3` 需要编译本地模块，确保系统有 `make` 和 `gcc` 工具。

### ⚠️ 重要：运行脚本前的准备

> **为什么需要 NODE_PATH？**
> 
> Node.js 有两种模块系统：
> - **CommonJS (`require`)**： 支持 NODE_PATH，可以找到全局安装的包
> - **ESM (`import`)**： 不支持 NODE_PATH，这是 Node.js 的设计决策
> 
> 本技能的脚本使用 `require`（而非 `import`）来加载全局依赖，因此需要设置 NODE_PATH。

**第一步：设置 NODE_PATH 环境变量**

```bash
export NODE_PATH=$(npm root -g)
```

**第二步：获取技能目录路径**

所有脚本使用相对于技能根目录的路径。获取技能目录：

```bash
# 方法 1：通过 SKILL.md 位置推断（推荐）
SKILL_DIR=$(dirname $(grep -rl "name: db-toolkit" ~/.config/opencode/skills 2>/dev/null | head -1))

# 方法 2：直接使用本文件所在目录
# SKILL_DIR=/path/to/db-toolkit
```

**第三步：运行脚本**

使用 `$SKILL_DIR/scripts/` 前缀执行脚本：

```bash
tsx $SKILL_DIR/scripts/test-connection.ts --url "mysql://..."
```

### 测试连接

```bash
tsx $SKILL_DIR/scripts/test-connection.ts --url "mysql://root:secret@localhost:3306/mydb"

# 或分开参数
tsx $SKILL_DIR/scripts/test-connection.ts \
  --db-type mysql \
  --host localhost \
  --port 3306 \
  --user root \
  --password secret \
  --database mydb
```

### 列出所有表

```bash
tsx $SKILL_DIR/scripts/list-tables.ts --url "mysql://root:secret@localhost:3306/mydb"
```

### 查看表结构

```bash
tsx $SKILL_DIR/scripts/describe-table.ts --url "mysql://root:secret@localhost:3306/mydb" --table users
```

## DDL/DML 操作

对于 DDL 和 DML 操作，根据数据库类型读取对应的参考文档：

| 数据库 | 连接配置 | DDL 模板 | DML 模板 |
|--------|----------|----------|----------|
| MySQL | [mysql/connection.md](references/mysql/connection.md) | [mysql/ddl.md](references/mysql/ddl.md) | [mysql/dml.md](references/mysql/dml.md) |
| PostgreSQL | [postgresql/connection.md](references/postgresql/connection.md) | [postgresql/ddl.md](references/postgresql/ddl.md) | [postgresql/dml.md](references/postgresql/dml.md) |
| SQLite | [sqlite/connection.md](references/sqlite/connection.md) | [sqlite/ddl.md](references/sqlite/ddl.md) | [sqlite/dml.md](references/sqlite/dml.md) |

## 安全注意事项

1. **不记录连接信息** - 脚本输出中不应包含密码等敏感信息
2. **使用参数化查询** - 防止 SQL 注入
3. **连接超时** - 建议设置合理的连接超时时间
4. **操作确认** - 危险操作（DROP、TRUNCATE）前应确认

## Resources

### scripts/

| 脚本 | 功能 | 参数 |
|------|------|------|
| `test-connection.ts` | 测试数据库连接 | `--url` 或 `--db-type, --host, --port, --user, --password, --database` |
| `list-tables.ts` | 列出所有表 | 连接参数 |
| `describe-table.ts` | 查看表结构 | 连接参数 + `--table` |

### references/

按数据库类型组织，每个数据库包含：
- `connection.md` - 连接配置详解
- `ddl.md` - DDL 操作模板（CREATE/ALTER/DROP）
- `dml.md` - DML 操作模板（SELECT/INSERT/UPDATE/DELETE）
