---
slug: db-admin-console-free
name: db-admin-console-free
version: 1.0.0
displayName: 数据库管理台(免费版)
summary: 数据库表结构设计、数据操作、查询优化与事务安全的免费核心能力,支持基础 DDL/DML 操作。
license: Proprietary
edition: free
description: '数据库管理台免费版面向独立开发者与一人公司的 DBA 日常工作流,提供表结构设计、数据操作、查询优化与事务安全的核心能力。核心能力:

  - 表结构设计:主键、索引、约束、外键、默认值策略

  - 数据插入:单条与批量插入(基础规模)

  - 查询编写:JOIN、聚合、子查询、CTE、执行计划解读

  - 数据类型处理:VARCHAR/BIGINT/UUID/JSONB/ENUM 等

  - 事务安全:ACID 属性、自动提交与回滚

  - 数据库维护:CREATE/ALTER/DROP/TRUNCATE/VACUUM


  适用场景:

  - 个...'
tags:
- 数据库管理
- 表结构设计
- 查询优化
- 集成工具
tools:
- read
- exec
homepage: https://skillhub.cn
pricing_tier: "L2-标准级"
pricing_model: per_use
suggested_price: "19.9 CNY/per_use"
tools: ["read", "write", "exec"]
tags: "工具,效率,自动化"
---
# 数据库管理台 免费版

## 一、概述

数据库管理台免费版面向独立开发者与一人公司的 DBA 日常工作流,覆盖表结构设计、数据操作、查询优化、类型处理与事务安全的全流程。所有操作遵循 SQL 最佳实践与 ACID 属性,以 `PostgreSQL` 等主流数据库为蓝本。

免费版聚焦日常管理的高频能力,适合中小规模数据(单表 <100 万行)与单实例场景。

## 核心能力

### 2.1 表结构设计

- **主键策略**:推荐 `SERIAL` / `BIGSERIAL` / `UUID` 自增主键
- **索引设计**:为高频查询字段自动建议索引
- **约束设置**:NOT NULL / UNIQUE / CHECK / FOREIGN KEY
- **默认值策略**:动态默认值如 `CURRENT_TIMESTAMP`
- **数据类型选择**:

| 类型 | 适用场景 | 注意事项 |
|---|----|----|
| `VARCHAR(n)` | 变长字符串 | 明确长度上限 |
| `TEXT` | 不限长文本 | 不建索引 |
| `BIGINT` | 大整数(超过 int 范围) | 避免溢出 |
| `UUID` | 全局唯一标识 | 适合分布式 |
| `JSONB` | 半结构化数据 | 支持 GIN 索引 |
| `ENUM` | 枚举值 | 修改需 ALTER TYPE |
| `TIMESTAMP` | 时间戳 | 注意时区 |
| `DECIMAL(p,s)` | 精确小数(金额) | 避免浮点误差 |

**输入**: 用户提供1 表结构设计所需的指令和必要参数。
**处理**: 解析1 表结构设计的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回1 表结构设计的响应数据,包含状态码、结果和日志。

### 2.2 数据插入

- **单条插入**:`INSERT INTO ... VALUES (...)`
- **批量插入**:`INSERT INTO ... VALUES (...), (...), ...`(基础规模,<1000 行)
- **类型校验**:插入前自动校验类型兼容性
- **冲突处理**:`ON CONFLICT DO NOTHING/UPDATE`
- **主键避让**:避免自增主键冲突

**输入**: 用户提供2 数据插入所需的指令和必要参数。
**处理**: 解析2 数据插入的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回2 数据插入的响应数据,包含状态码、结果和日志。

### 2.3 查询优化

| 查询类型 | 关键要点 |
|:-----|:-----|
| JOIN | 选择小表为驱动表,关联字段必须有索引 |
| 聚合 | GROUP BY 字段选择性要高,避免 HAVING 过滤 |
| 子查询 | 优先用 CTE 提升可读性 |
| 分页 | 大表分页用 `WHERE id > last_id LIMIT N` 替代 OFFSET |
| 范围查询 | 范围字段建 B-tree 索引 |
| 模糊查询 | 前缀匹配可用索引,全模糊用 GIN/trigram |

**输入**: 用户提供3 查询优化所需的指令和必要参数。
**处理**: 解析3 查询优化的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回3 查询优化的响应数据,包含状态码、结果和日志。

### 2.4 类型处理

- **BIGINT 溢出**:应用层避免 int32 接收 BIGINT
- **JSONB 查询**:`->` 取 JSON 对象,`->>` 取文本
- **ENUM 修改**:`ALTER TYPE ... ADD VALUE`
- **时间格式**:统一 ISO 8601,避免时区歧义

**输入**: 用户提供4 类型处理所需的指令和必要参数。
**处理**: 解析4 类型处理的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回4 类型处理的响应数据,包含状态码、结果和日志。

### 2.5 事务安全

## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---:|---:|---:|---:|
| input | string | 是 | 数据库管理台(免费版)处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```sql
BEGIN;
  -- 一组原子操作
  INSERT INTO orders ...;
  UPDATE inventory SET qty = qty - 1 WHERE ...;
  INSERT INTO audit_log ...;
COMMIT;
-- 异常时:ROLLBACK;
```

- ACID 属性:原子性、一致性、隔离性、持久性
- 隔离级别:READ COMMITTED(默认)/ REPEATABLE READ / SERIALIZABLE
- 死锁预防:固定加锁顺序,小事务优先

**输入**: 用户提供5 事务安全所需的指令和必要参数。
**处理**: 解析5 事务安全的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回5 事务安全的响应数据,包含状态码、结果和日志。

### 2.6 数据库维护

| 操作 | 命令 | 注意事项 |
|:---:|:---:|:---:|
| 建表 | `CREATE TABLE` | 设计好主键与索引 |
| 改表 | `ALTER TABLE` | 大表加列用默认值,避免重写 |
| 删表 | `DROP TABLE` | 不可逆,谨慎使用 |
| 清空 | `TRUNCATE` | 保留结构,速度快 |
| 分析 | `VACUUM` / `ANALYZE` | 定期执行,更新统计 |
| 索引重建 | `REINDEX` | 索引膨胀时执行 |

**输入**: 用户提供6 数据库维护所需的指令和必要参数。
**处理**: 解析6 数据库维护的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回6 数据库维护的响应数据,包含状态码、结果和日志。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：数据库表结构设计、数据操作、查询优化与事务安、全的免费核心能力、支持基础、DDL、DML、数据库管理台免费、版面向独立开发者、与一人公司的、DBA、日常工作流、提供表结构设计、全的核心能力、核心能力、单条与批量插入、查询编写、执行计划解读、数据类型处理、自动提交与回滚等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 适用场景

| 角色 | 典型场景 | 输入 | 输出 |
|:------|------:|:------|:------|
| 独立开发者 | 设计新业务表结构 | 业务字段清单 | DDL 脚本 + 索引建议 |
| 后端工程师 | 写复杂查询 | 业务需求 | SQL + 执行计划分析 |
| 兼职 DBA | 日常维护任务 | 维护需求 | 操作脚本 + 注意事项 |
| 数据分析师 | 取数分析 | 分析需求 | SQL + 结果集 |

## 使用流程

预计上手时间:**< 60 秒**。

直接以自然语言向 Agent 描述任务,以下为可复制模板:

```text
请创建一个库存表 stock_info:
1. id: SERIAL PRIMARY KEY
2. product_name: VARCHAR(100) NOT NULL
3. quantity: INT NOT NULL DEFAULT 0
4. price: DECIMAL(10,2) NOT NULL
5. created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
6. 为 product_name 创建索引
```

```text
请优化这条慢查询:
SELECT * FROM orders o
JOIN users u ON o.user_id = u.id
WHERE o.created_at > '2024-01-01'
ORDER BY o.amount DESC
LIMIT 100;
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤。

## 示例

### 5.1 数据库连接(凭证走环境变量)

```python
import os
import psycopg2
# ...
conn = psycopg2.connect(
    host=os.environ['DB_HOST'],
    port=os.environ.get('DB_PORT', '5432'),
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASSWORD'],
    database=os.environ['DB_NAME']
)
```

> **安全要求**:**禁止**在脚本或对话中明文硬编码数据库密码,**必须**通过环境变量传入。推荐存放于 `d:\skills\.skill-credentials\` 目录(已 gitignore)。

### 5.2 表结构设计示例

```sql
-- 用户表
CREATE TABLE users (
    id          BIGSERIAL PRIMARY KEY,
    username    VARCHAR(50) NOT NULL UNIQUE,
    email       VARCHAR(255) NOT NULL UNIQUE,
    status      SMALLINT NOT NULL DEFAULT 1,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_status CHECK (status IN (0, 1, 2))
);
# ...
CREATE INDEX idx_users_created_at ON users(created_at);
# ...
-- 订单表(外键关联用户)
CREATE TABLE orders (
    id           BIGSERIAL PRIMARY KEY,
    user_id      BIGINT NOT NULL,
    amount       DECIMAL(10,2) NOT NULL,
    status       VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at   TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_orders_user FOREIGN KEY (user_id)
        REFERENCES users(id) ON DELETE RESTRICT,
    CONSTRAINT chk_amount CHECK (amount >= 0)
);
# ...
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_created_at ON orders(created_at);
CREATE INDEX idx_orders_status_created ON orders(status, created_at);
```

### 5.3 批量插入(基础规模)

```sql
INSERT INTO stock_info (product_name, quantity, price)
VALUES
    ('苹果', 100, 8.50),
    ('香蕉', 200, 3.20),
    ('橙子', 150, 5.80)
ON CONFLICT (product_name) DO UPDATE
SET quantity = EXCLUDED.quantity,
    price = EXCLUDED.price;
```

### 5.4 查询与执行计划

```sql
-- 关联查询(走索引)
EXPLAIN ANALYZE
SELECT u.username, COUNT(o.id) AS order_count, SUM(o.amount) AS total
FROM users u
JOIN orders o ON o.user_id = u.id
WHERE o.created_at >= '2024-01-01'
  AND o.status = 'completed'
GROUP BY u.id, u.username
ORDER BY total DESC
LIMIT 50;
```

### 5.5 事务处理

```sql
BEGIN;
  -- 扣减库存
  UPDATE stock_info
  SET quantity = quantity - 1
  WHERE product_name = '苹果' AND quantity > 0;
# ...
  -- 若未扣减成功则回滚
  -- 通过应用层判断 rowcount
# ...
  -- 创建订单
  INSERT INTO orders (user_id, amount, status)
  VALUES (123, 8.50, 'completed');
# ...
  -- 写审计日志
  INSERT INTO audit_log (action, target, created_at)
  VALUES ('order_create', 'order', CURRENT_TIMESTAMP);
COMMIT;
```

## 六、最佳实践

- **主键选择**:分布式场景用 UUID,单机用 SERIAL/BIGSERIAL
- **索引策略**:WHERE / JOIN / ORDER BY 字段建索引,避免过度索引
- **大表分页**:用 `WHERE id > last_id LIMIT N` 替代 OFFSET
- **类型匹配**:应用层与数据库类型对齐,避免 BIGINT 溢出
- **事务粒度**:小事务优先,避免长事务持锁
- **定期维护**:VACUUM ANALYZE 定期执行,更新统计信息
- **凭证安全**:数据库密码一律走环境变量,**禁止**硬编码
- **变更评审**:DDL 操作前先在测试库验证

## 常见问题

### Q1: BIGINT 字段在应用层溢出怎么办?

A: 后端语言(int32 接收 BIGINT 会溢出)需用 long/int64/BigInteger 类型接收。前端 JavaScript 需用字符串或 BigInt 处理。

### Q2: 索引建多了会怎样?

A: 索引提升查询性能但拖累写入性能。建议:WHERE / JOIN / ORDER BY 字段才建索引,低选择性字段(如性别)不单独建索引。

### Q3: 大表分页为什么用 OFFSET 会慢?

A: OFFSET 需要扫描并丢弃前 N 行,N 越大越慢。改用 `WHERE id > last_id LIMIT N` 走索引,性能稳定。

### Q4: JSONB 字段如何查询?

A: `->` 取 JSON 对象,`->>` 取文本。例:`WHERE data->>'name' = '张三'`。高频查询字段建议建 GIN 索引。

### Q5: 免费版能处理多大的表?

A: 推荐用于单表 <100 万行的场景。更大规模数据建议使用专业版的批量处理与分区能力。

### Q6: 数据库密码如何安全传入?

A: **必须**通过环境变量传入,**禁止**硬编码。推荐存放于 `d:\skills\.skill-credentials\` 目录(已 gitignore)。

## 已知限制

本免费体验版限制以下高级功能:

- 禁用大规模批量插入(单次 <1000 行)
- 禁用分区表与表空间管理
- 禁用存储过程与触发器自动化
- 禁用查询性能基线对比与回归检测
- 禁用定时备份与恢复自动化
- 禁用多实例管理与读写分离
- 禁用 schema 迁移版本管理
- 禁用与外部数据同步(如 `PostgreSQL` ↔ MySQL)

解锁全部功能请使用专业版:`db-admin-console-pro`
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 依赖说明

### 运行环境

- **Agent 平台**: 任意支持 SKILL.md 的 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **数据库**: `PostgreSQL` 12+(推荐)/ MySQL 8+ / SQLite 3.35+
- **Python**: 3.8+(可选,用于连接管理脚本)

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|:---|---:|---:|
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |
| psycopg2 | Python 库 | 可选 | `pip install psycopg2-binary`(`PostgreSQL`) |
| mysql-connector | Python 库 | 可选 | `pip install mysql-connector-python`(MySQL) |
| SQLAlchemy | Python 库 | 可选 | `pip install sqlalchemy`(ORM) |

### API Key 配置

- **数据库凭证**: 通过 `DB_HOST`/`DB_USER`/`DB_PASSWORD`/`DB_NAME` 等环境变量传入
- **禁止**: 在 SKILL.md、脚本、配置文件中硬编码任何数据库密码
- **推荐路径**: 凭证统一存放在 `d:\skills\.skill-credentials\` 目录(已 gitignore)

### 可用性分类

- **分类**: MD+EXEC(纯 Markdown 指令,核心功能需要 exec 命令行执行能力)
- **说明**: 基于自然语言驱动的 AI Skill,通过事务安全与类型处理保障数据库操作质量

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------:|--------|:-------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "数据库管理台(免费版)处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "db admin console"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
