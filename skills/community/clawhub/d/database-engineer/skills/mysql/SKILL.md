---
name: mysql
description: MySQL 数据库：查询优化、索引策略、Schema 设计、存储引擎、复制与高可用
source:
  type: derived
  repo: skills-repo/database-engineer
  path: skills/mysql/SKILL.md
  url: https://skills.sh/planetscale/database-skills/mysql
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
  - mysql
  - database
  - sql
  - query-optimization
  - indexing
---

# MySQL — 数据库技能

> MySQL 是互联网公司最常用的关系型数据库。多数性能问题不是 MySQL 不行，是查询和索引写得不对。本技能覆盖 MySQL 从 Schema 设计到高可用的核心实践。

## 能力

- **查询优化**：EXPLAIN 分析、慢查询定位、查询重写、JOIN 优化
- **索引策略**：B-Tree 原理、联合索引最左前缀、覆盖索引、索引选择性
- **Schema 设计**：数据类型选择、范式 vs 反范式、分区表设计
- **存储引擎**：InnoDB 特性（MVCC、Buffer Pool、Redo Log）、引擎选择
- **复制与高可用**：主从复制、GTID、半同步复制、读写分离

## 使用方式

在 Claude Code 中使用 `/mysql` 调用。

```
/mysql 帮我优化这条慢查询 SQL
/mysql 设计这个业务场景的表结构
/mysql 分析当前的索引是否合理
```

## 查询优化框架

1. **定位** — 慢查询日志 → pt-query-digest 分析
2. **分析** — EXPLAIN 解读（type, key, rows, Extra）
3. **优化** — 索引调整 → 查询重写 → Schema 调整 → 参数调优
4. **验证** — 压测对比优化前后效果

## 适用场景

- Web 应用后端数据库设计与优化
- 慢查询排查和性能调优
- 数据库从单机到主从架构的演进
- 分库分表前的 Schema 优化

## 限制

- 聚焦 MySQL 特定功能和优化，不涉及通用 SQL 入门
- 高可用覆盖基础架构，不涉及大规模集群管理
- 不涉及 MySQL 以外的数据库迁移

## 相关参考（Playbook）

执行计划解读（三引擎对照）→ [references/explain-reading.md](../../references/explain-reading.md)（[scripts/explain_audit.py](../../scripts/explain_audit.py)）；
索引设计决策 → [references/index-design.md](../../references/index-design.md)；
慢查询分诊（慢日志聚合）→ [references/slow-query-triage.md](../../references/slow-query-triage.md)（[scripts/slowlog_digest.py](../../scripts/slowlog_digest.py)）；
事务、隔离级别与锁 → [references/transactions-locking.md](../../references/transactions-locking.md)；
Schema 变更与零停机迁移 → [references/schema-migration.md](../../references/schema-migration.md)（[scripts/schema_lint.py](../../scripts/schema_lint.py)）；
备份与恢复（含恢复演练）→ [references/backup-recovery.md](../../references/backup-recovery.md)；
连接池与容量规划 → [references/capacity-and-pooling.md](../../references/capacity-and-pooling.md)；
数据库选型决策 → [references/engine-selection.md](../../references/engine-selection.md)。
