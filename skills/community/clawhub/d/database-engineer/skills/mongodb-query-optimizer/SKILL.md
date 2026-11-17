---
name: mongodb-query-optimizer
description: MongoDB 查询优化：聚合管道、索引策略、Schema 设计、性能诊断
source:
  type: derived
  repo: skills-repo/database-engineer
  path: skills/mongodb-query-optimizer/SKILL.md
  url: https://skills.sh/mongodb/agent-skills/mongodb-query-optimizer
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
  - mongodb
  - nosql
  - query-optimization
  - aggregation
  - database
---

# MongoDB Query Optimizer — MongoDB 查询优化

> MongoDB 的灵活性是把双刃剑——没有 Schema 约束意味着查询性能完全取决于你怎么用。多数慢查询不是 MongoDB 的问题，是索引没建对、聚合管道没写好、文档结构不合理。本技能覆盖 MongoDB 性能诊断和优化。

## 能力

- **查询分析**：explain("executionStats") 解读、COLLSCAN vs IXSCAN 识别、慢查询日志
- **索引策略**：单字段/复合/多键/文本/地理空间索引、ESR 规则（Equality → Sort → Range）
- **聚合管道优化**：$match 前置、$project 裁剪、$lookup 替代方案、管道合并
- **Schema 设计**：嵌入 vs 引用、文档大小控制、分桶模式、多态模式
- **性能诊断**：mongostat、mongotop、currentOp、profile 分析

## 使用方式

在 Claude Code 中使用 `/mongodb-query-optimizer` 调用。

```
/mongodb-query-optimizer 这条聚合管道跑得很慢，帮我分析瓶颈
/mongodb-query-optimizer 这个集合应该建哪些索引
/mongodb-query-optimizer 帮我优化这个文档的 Schema 设计
```

## 优化检查清单

1. **索引覆盖** — 查询字段是否都有索引？ESR 顺序是否正确？
2. **聚合管道** — $match 是否在最前面？$lookup 能否用嵌入替代？
3. **文档大小** — 单个文档是否超过 16MB？是否需要分桶？
4. **写入模式** — 是否有不必要的大批量更新？
5. **连接管理** — 连接池配置是否合理？

## 适用场景

- 独立开发者用 MongoDB 做应用后端
- 内容管理、IoT 数据、日志存储等文档型场景
- 从关系型数据库迁移到 MongoDB 的 Schema 设计
- 聚合管道性能排查

## 限制

- 聚焦单机/副本集优化，不涉及分片集群
- 覆盖 MongoDB 5.0+ 版本特性
- 不涉及跨数据库迁移和数据同步

## 相关参考（Playbook）

执行计划解读（explain executionStats）→ [references/explain-reading.md](../../references/explain-reading.md)（[scripts/explain_audit.py](../../scripts/explain_audit.py)）；
索引设计决策（复合索引 ESR）→ [references/index-design.md](../../references/index-design.md)；
慢查询分诊（profiler 聚合）→ [references/slow-query-triage.md](../../references/slow-query-triage.md)（[scripts/slowlog_digest.py](../../scripts/slowlog_digest.py)）；
事务、隔离级别与锁（多文档事务边界）→ [references/transactions-locking.md](../../references/transactions-locking.md)；
Schema 变更与零停机迁移（文档演进）→ [references/schema-migration.md](../../references/schema-migration.md)（[scripts/schema_lint.py](../../scripts/schema_lint.py)）；
备份与恢复（副本集快照）→ [references/backup-recovery.md](../../references/backup-recovery.md)；
连接池与容量规划（WT 缓存）→ [references/capacity-and-pooling.md](../../references/capacity-and-pooling.md)；
数据库选型决策 → [references/engine-selection.md](../../references/engine-selection.md)。
