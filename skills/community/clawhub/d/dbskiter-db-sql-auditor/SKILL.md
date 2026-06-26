---
name: db-sql-auditor
description: |
  SQL全生命周期审核，支持SQL规范审核、性能评估、DDL影响分析。

  使用场景：
  - 用户说"审核SQL" → 执行 sql "<SQL>"
  - 用户说"检查规范" → 执行 sql "<SQL>"
  - 用户说"DDL影响" → 执行 ddl "<DDL>"
  - 用户说"查看规则" → 执行 rules

  用法：
  - dbskiter --output-mode=ai --database=<name> audit sql "SELECT * FROM users"
  - dbskiter --output-mode=ai --database=<name> audit file queries.sql
  - dbskiter --output-mode=ai --database=<name> audit ddl "ALTER TABLE users ADD COLUMN age INT"
  - dbskiter --output-mode=ai --database=<name> audit rules
---

# SQL审核 Skill

## 何时使用

当用户提到以下关键词时，使用此skill：

| 用户说法 | 执行命令 | 说明 |
|---------|---------|------|
| "审核SQL" | `dbskiter --output-mode=ai --database=<name> audit sql "<SQL>"` | 审核单条SQL |
| "检查规范" | `dbskiter --output-mode=ai --database=<name> audit sql "<SQL>"` | 检查SQL规范 |
| "DDL影响" | `dbskiter --output-mode=ai --database=<name> audit ddl "<DDL>"` | 分析DDL影响 |
| "审核文件" | `dbskiter --output-mode=ai --database=<name> audit file <path>` | 审核SQL文件 |
| "查看规则" | `dbskiter --output-mode=ai --database=<name> audit rules` | 查看审核规则 |

## 核心命令

### 1. 审核SQL
```bash
dbskiter --database=<数据库名> audit sql "SELECT * FROM users WHERE id = 1"
```
**输出**：审核评分、问题列表、修复建议

**评分标准**：
- 90-100：通过
- 80-89：警告
- <80：不通过

### 2. DDL影响分析
```bash
dbskiter --database=<数据库名> audit ddl "ALTER TABLE users ADD COLUMN age INT"
```
**输出**：预估执行时间、风险点、建议

### 3. 审核SQL文件
```bash
dbskiter --database=<数据库名> audit file queries.sql
```
**用途**：批量审核多个SQL语句

### 4. 查看规则
```bash
dbskiter --database=<数据库名> audit rules
```
**输出**：所有审核规则列表

## 核心命令（9个）

### 1. 审核SQL
```bash
dbskiter --database=<数据库名> audit sql "SELECT * FROM users WHERE id = 1"
```
**输出**：审核评分、问题列表、修复建议

### 2. DDL影响分析
```bash
dbskiter --database=<数据库名> audit ddl "ALTER TABLE users ADD COLUMN age INT"
```
**输出**：预估执行时间、风险点、建议

### 3. 审核SQL文件
```bash
dbskiter --database=<数据库名> audit file queries.sql
```
**用途**：批量审核多个SQL语句

### 4. 查看规则
```bash
dbskiter --database=<数据库名> audit rules
```
**输出**：所有审核规则列表

### 5. SQL优化
```bash
dbskiter --database=<数据库名> audit optimize "SELECT * FROM users WHERE age > 18"
```
**功能**：智能优化SQL，提供重写建议、索引推荐、成本估算

### 6. 索引推荐
```bash
dbskiter --database=<数据库名> audit recommend-indexes "SELECT * FROM orders WHERE user_id = 1"
```
**功能**：分析SQL并推荐合适的索引

### 7. 执行计划分析
```bash
dbskiter --database=<数据库名> audit analyze-plan --plan="EXPLAIN输出"
```
**功能**：分析执行计划，识别性能瓶颈

### 8. 成本估算
```bash
dbskiter --database=<数据库名> audit estimate-cost "SELECT * FROM users"
```
**功能**：估算SQL执行成本（IO、CPU、内存）

### 9. SQL重写
```bash
dbskiter --database=<数据库名> audit rewrite "SELECT * FROM users WHERE id = 1"
```
**功能**：自动重写SQL，消除常见性能问题

## 审核类型

- **syntax**：语法规范
- **performance**：性能规范
- **security**：安全规范
- **style**：编码风格
- **ddl**：DDL规范

## AI决策流程

### 场景1：用户说"审核这条SQL"

```
步骤1：提取用户提供的SQL
步骤2：执行 dbskiter --database=<name> audit sql "<SQL>"
步骤3：解读审核评分和问题列表
步骤4：给出修复建议
```

### 场景2：用户说"这个DDL有什么影响"

```
步骤1：提取DDL语句
步骤2：执行 dbskiter --database=<name> audit ddl "<DDL>"
步骤3：解读影响分析结果
步骤4：给出执行建议（如低峰期执行）
```
