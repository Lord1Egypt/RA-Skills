---
name: db-lock-analyzer
description: |
  数据库锁分析与死锁检测，支持当前锁分析、死锁检测、锁等待链追踪。

  使用场景：
  - 用户说"看锁" → 执行 analyze
  - 用户说"死锁" → 执行 deadlocks
  - 用户说"阻塞" → 执行 chains
  - 用户说"终止事务" → 执行 kill <事务ID>

  用法：
  - dbskiter --output-mode=ai --database=<name> lock analyze
  - dbskiter --output-mode=ai --database=<name> lock deadlocks
  - dbskiter --output-mode=ai --database=<name> lock chains
  - dbskiter --output-mode=ai --database=<name> lock kill <transaction_id>
---

# 锁分析 Skill

## 何时使用

当用户提到以下关键词时，使用此skill：

| 用户说法 | 执行命令 | 说明 |
|---------|---------|------|
| "看锁" | `dbskiter --output-mode=ai --database=<name> lock analyze` | 分析当前锁情况 |
| "死锁" | `dbskiter --output-mode=ai --database=<name> lock deadlocks` | 检测死锁 |
| "阻塞" | `dbskiter --output-mode=ai --database=<name> lock chains` | 追踪锁等待链 |
| "锁报告" | `dbskiter --output-mode=ai --database=<name> lock report` | 生成锁分析报告 |
| "终止事务" | `dbskiter --output-mode=ai --database=<name> lock kill <id>` | 终止阻塞事务 |

## 核心命令

### 1. 分析当前锁
```bash
dbskiter --database=<数据库名> lock analyze
```
**输出**：总锁数、等待中锁数、已授予锁数

### 2. 检测死锁
```bash
dbskiter --database=<数据库名> lock deadlocks
```
**输出**：死锁数量、涉及事务、解决建议

### 3. 追踪锁等待链
```bash
dbskiter --database=<数据库名> lock chains
```
**输出**：锁等待链数量、链深度、阻塞源头

### 4. 终止事务
```bash
dbskiter --database=<数据库名> lock kill <transaction_id>
```
**注意**：谨慎使用，会强制终止事务

## 锁类型

- **TABLE**：表锁
- **ROW**：行锁
- **METADATA**：元数据锁

## 数据库支持情况

| 数据库 | 锁分析 | 死锁检测 | 锁等待链 | 说明 |
|--------|--------|----------|----------|------|
| MySQL | 完整支持 | 支持 | 支持 | 完全可用 |
| PostgreSQL | 完整支持 | 支持 | 支持 | 完全可用 |
| Oracle | 完整支持 | 支持 | 支持 | 完全可用 |

## AI决策流程

### 场景1：用户说"看看锁情况"

```
步骤1：执行 dbskiter --database=<name> lock analyze
步骤2：查看锁统计信息
步骤3：如果有等待锁，执行 dbskiter --database=<name> lock chains 查看阻塞链
步骤4：总结锁情况给用户
```

### 场景2：用户说"有死锁吗"

```
步骤1：执行 dbskiter --database=<name> lock deadlocks
步骤2：如果有死锁，列出涉及的事务和SQL
步骤3：给出解决建议（如终止某个事务）
```

### 场景3：用户说"有阻塞"

```
步骤1：执行 dbskiter --database=<name> lock chains
步骤2：分析阻塞链，找出阻塞源头
步骤3：建议终止阻塞源头事务或优化业务逻辑
```
