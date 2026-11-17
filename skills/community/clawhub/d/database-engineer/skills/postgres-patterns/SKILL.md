---
name: postgres-patterns
description: PostgreSQL 模式：高级查询、索引类型、并发控制、扩展、性能调优
source:
  type: derived
  repo: skills-repo/database-engineer
  path: skills/postgres-patterns/SKILL.md
  url: https://skills.sh/affaan-m/everything-claude-code/postgres-patterns
  version: 1.0.0
  updated: 2026-07-30
metadata:
  author: hope
  category: 数据库
  platform: 通用
  difficulty: 进阶
  version: 1.0.0
  created: 2026-07-30
tags:
  - postgresql
  - database
  - sql
  - performance
  - concurrency
---

# PostgreSQL Patterns — PostgreSQL 高级模式

> PostgreSQL 是功能最丰富的关系型数据库，但多数人只用到了它的 MySQL 兼容子集。CTE、窗口函数、JSONB、全文搜索——这些高级特性才是选 PG 的真正理由。本技能覆盖 PG 高级模式和实践。

## 能力

- **高级查询**：CTE（WITH 递归）、窗口函数、LATERAL JOIN、聚合技巧
- **索引类型**：B-Tree / Hash / GIN / GiST / BRIN 选择、部分索引、表达式索引
- **并发控制**：MVCC 机制、事务隔离级别、死锁分析、SKIP LOCKED
- **扩展生态**：PostGIS（地理）、pgvector（向量搜索）、pg_cron、Citus
- **性能调优**：EXPLAIN ANALYZE、work_mem、vacuum 策略、连接池

## 使用方式

在 Claude Code 中使用 `/postgres-patterns` 调用。

```
/postgres-patterns 帮我写一个递归 CTE 查询树形结构
/postgres-patterns 这条查询为什么这么慢？用 EXPLAIN 分析
/postgres-patterns 我的表每天写入 100 万行，如何设计分区
```

## 适用场景

- 需要高级 SQL 特性的数据分析查询
- 地理空间数据处理（PostGIS）
- 全文搜索和 JSON 文档存储
- 高并发写入场景的事务设计

## 限制

- 聚焦 PG 特有功能，不涉及通用 SQL 基础
- 扩展生态覆盖概览，不深入单个扩展的完整文档
- 不涉及 PG 集群管理和容灾方案

## 相关参考（Playbook）

执行计划解读（三引擎对照）→ [references/explain-reading.md](../../references/explain-reading.md)（[scripts/explain_audit.py](../../scripts/explain_audit.py)）；
索引设计决策（含部分/表达式/GIN）→ [references/index-design.md](../../references/index-design.md)；
慢查询分诊（pg_stat_statements）→ [references/slow-query-triage.md](../../references/slow-query-triage.md)（[scripts/slowlog_digest.py](../../scripts/slowlog_digest.py)）；
事务、隔离级别与锁 → [references/transactions-locking.md](../../references/transactions-locking.md)；
Schema 变更与零停机迁移（CONCURRENTLY）→ [references/schema-migration.md](../../references/schema-migration.md)（[scripts/schema_lint.py](../../scripts/schema_lint.py)）；
备份与恢复（WAL 归档）→ [references/backup-recovery.md](../../references/backup-recovery.md)；
连接池与容量规划（pgBouncer）→ [references/capacity-and-pooling.md](../../references/capacity-and-pooling.md)；
数据库选型决策 → [references/engine-selection.md](../../references/engine-selection.md)。
