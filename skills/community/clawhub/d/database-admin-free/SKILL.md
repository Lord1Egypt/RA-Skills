---
slug: "database-admin-free"
name: "database-admin-free"
version: "1.0.0"
displayName: "数据库管理(免费版)"
summary: "基础表结构设计、数据插入与简单查询，支持常用数据类型与事务操作。数据库管理免费版，提供基础的数据库表结构与数据操作能力. 核心能力包括： - 基础表结构设计（主键、NOT NULL、DEFA"
summary_zh: "基础表结构设计、数据插入与简单查询，支持常用数据类型与事务操作。数据库管理免费版，提供基础的数据库表结构与数据操作能力. 核心能力包括： - 基础表结构设计（主键、NOT NULL、DEFA"
license: "MIT"
description: "|-. 适用于需要database admin相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性."
  数据库管理免费版，提供基础的数据库表结构与数据操作能力.
  核心能力包括：
  - 基础表结构设计（主键、NOT NULL、DEFAULT）
  - 常用数据类型（TEXT、VARCHAR、INT、SERIAL、TIMESTAMP）
  - 单条与批量INSERT数据插入
  - 基础SELECT查询（WHERE、ORDER BY、GROUP BY）
  - 事务操作（BEGIN/COMMIT/ROLLBACK）
  高级功能（BIGINT/JSONB/UUID类型、COPY批量导入、CTE查询、执行计划分析、VACUUM维护、连接池管理）为付费版专享.
tags:
  - 信息检索
  - database
  - admin
  - automation
  - productivity
  - postgresql
  - 数据处理
  - 数据分析
  - 工具
  - stock_info
tools:
  - read
  - exec
  - write
  - glob
homepage: ""
category: "Research"
pricing_tier: free
---
# 数据库管理（免费版）

## 输入格式

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | 数据库管理(免费版)处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

## 概述

提供基础的数据库表结构创建、数据插入与查询能力，满足日常数据库操作需求。基于 PostgreSQL 语法规范.
## 核心能力
### 基础表结构设计
- 自动设计表结构（主键、`NOT NULL`、`DEFAULT`）
- 支持常用数据类型：`TEXT`、`VARCHAR(n)`、`INT`、`SERIAL`、`TIMESTAMP`、`DECIMAL(p,s)`
- 创建基础索引（`CREATE INDEX`）

> **升级提示**：`BIGINT`、`UUID`、`JSONB`、`ENUM` 等高级数据类型，外键约束（`FOREIGN KEY`）、检查约束（`CHECK`）为付费版专享功能.

### 数据插入
```sql
-- 单条插入
INSERT INTO stock_info (product_name, quantity, price) VALUES ('苹果', 100, 8.50);
# ...
-- 批量插入（事务包裹）
BEGIN;
INSERT INTO stock_info (product_name, quantity, price) VALUES
    ('苹果', 100, 8.50),
    ('香蕉', 200, 3.20),
    ('牛肉', 50, 45.00);
COMMIT;
```

> **升级提示**：`COPY` 命令高性能批量导入（10万条以上）、`ON CONFLICT` 冲突处理为付费版专享功能.

### 基础查询
```sql
-- 条件查询
SELECT * FROM stock_info WHERE quantity > 50;
# ...
-- 分组统计
SELECT category, COUNT(*) AS count, AVG(price) AS avg_price
FROM stock_info
GROUP BY category
ORDER BY avg_price DESC;
```

> **升级提示**：CTE（`WITH` 子句）复杂查询、`EXPLAIN ANALYZE` 执行计划分析、多表 `JOIN` 优化为付费版专享功能.

### 事务操作
```sql
BEGIN;
INSERT INTO stock_info (product_name, quantity, price) VALUES ('橙子', 80, 5.00);
-- 如出错执行 ROLLBACK 撤销
COMMIT;
```

> **升级提示**：连接池（`pgpool`）管理、`VACUUM ANALYZE` 维护操作、`TRUNCATE`、`pg_dump` 备份恢复为付费版专享功能.

#
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux

### 依赖项
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
需要配置对应API Key，详见上文环境配置章节

### 可用性分类
- **分类**: MD+EXEC（）

**API Key配置方式**:
```bash
export API_KEY=${API_KEY:?请设置环境变量}
```
配置后需重启会话或开启新终端生效。API Key应妥善保管,避免泄露到版本控制系统.
## 使用流程

1. **明确需求**：确认需要建表、插入数据还是查询
2. **设计结构**：根据字段需求选择基础数据类型（`VARCHAR(100)`、`INT`、`DECIMAL(10,2)`）
3. **编写SQL**：生成含主键与 `NOT NULL` 约束的 `CREATE TABLE` / `INSERT` / `SELECT` 语句
4. **事务执行**：在事务中执行批量操作，异常时 `ROLLBACK`
5. **验证结果**：检查插入行数与查询输出

## 示例

### 示例1：创建库存表

```sql
CREATE TABLE stock_info (
    id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    quantity INT DEFAULT 0,
    price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
# ...
CREATE INDEX idx_stock_product_name ON stock_info(product_name);
```

### 示例2：批量插入与查询

```sql
BEGIN;
# ...
INSERT INTO stock_info (product_name, quantity, price) VALUES
    ('苹果', 100, 8.50),
    ('香蕉', 200, 3.20),
    ('牛肉', 50, 45.00);
# ...
COMMIT;
# ...
SELECT category, COUNT(*) AS count, AVG(price) AS avg_price
FROM stock_info
WHERE quantity > 50
GROUP BY category
ORDER BY avg_price DESC;
```

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| `主键冲突 (duplicate key)` | `INSERT` 的主键值已存在 | 检查 `SERIAL` 自增序列是否同步，或使用付费版 `ON CONFLICT` 处理 |
| `类型不匹配` | `VARCHAR` 列插入数值 | 使用 `CAST(col AS type)` 显式转换类型 |
| `NOT NULL 约束违规` | 插入时未提供必填字段值 | 检查表定义中 `NOT NULL` 列，确保插入时提供值 |
| `事务未提交` | `BEGIN` 后未执行 `COMMIT` | 确保每对 `BEGIN/COMMIT` 配对，异常时执行 `ROLLBACK` |
| `DECIMAL 精度溢出` | 值超出 `DECIMAL(10,2)` 范围 | 检查整数部分位数（10位=8位整数+2位小数），调整精度定义 |

## 常见问题

### Q1: VARCHAR(100) 和 TEXT 有什么区别？
A: `VARCHAR(100)` 有长度限制（100字符），`TEXT` 无限制。需要长度校验时用 `VARCHAR(n)`，不需要时用 `TEXT`.
### Q2: 如何处理超大整数ID？
A: `BIGINT` 类型支持（范围至 9223372036854775807）为付费版专享功能。免费版可使用 `TEXT` 存储ID字符串，或升级至付费版获取 `BIGINT` 支持.
### Q3: 如何批量导入10万条数据？
A: `COPY` 命令高性能导入为付费版专享功能。免费版可使用多值 `INSERT` 批量插入（单语句插入多行），配合事务 `BEGIN/COMMIT` 优化.
### Q4: 如何分析查询性能？
A: `EXPLAIN ANALYZE` 执行计划分析为付费版专享功能。免费版可通过观察查询响应时间粗略评估，或升级至付费版获取详细执行计划分析.
### Q5: JSONB 和 JSON 有什么区别？
A: `JSONB` 类型支持为付费版专享功能。免费版可使用 `TEXT` 存储JSON字符串，查询时手动解析.
## 已知限制

- 免费版不支持 `BIGINT`、`UUID`、`JSONB`、`ENUM` 高级数据类型
- 免费版不支持 `COPY` 命令批量导入
- 免费版不支持 CTE（`WITH` 子句）与 `EXPLAIN ANALYZE` 执行计划分析
- 免费版不支持 `VACUUM`、`TRUNCATE`、`pg_dump` 等维护操作
- 免费版不支持外键约束（`FOREIGN KEY`）与检查约束（`CHECK`）
- 免费版不支持连接池（`pgpool`）管理
- 不适用于实时流数据处理
- 升级至付费版可解锁全部高级功能

## 输出格式

```json
{
  "success": true,
  "data": {
    "result": "数据库管理(免费版)处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "database-admin"
    }
  },
  "execution_log": [
    "解析输入参数",
    "执行核心处理",
    "格式化输出结果"
  ],
  "error": null
}
```
