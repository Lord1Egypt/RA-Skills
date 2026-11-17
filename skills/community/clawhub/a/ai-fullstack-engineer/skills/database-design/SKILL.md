---
name: database-design
description: 数据库设计：Schema 规范、索引策略、ORM 选择、性能优化、迁移管理
source:
  type: derived
  repo: skills-repo/ai-fullstack-engineer
  path: skills/database-design/SKILL.md
  url: https://skills.sh/sickn33/antigravity-awesome-skills/database-design
  version: 1.0.0
  updated: 2026-07-30
metadata:
  author: hope
  category: 数据
  platform: 通用
  difficulty: 进阶
  version: 1.0.0
  created: 2026-07-30
tags:
  - database
  - schema-design
  - indexing
  - postgresql
  - orm
---

# Database Design — 数据库设计

> Schema 设计是后端的根基。一张表没设计好，索引没用对，再好的代码也救不回来。本技能帮你做出正确的数据库设计决策。

## 能力

- **Schema 设计**：范式 vs 反范式、字段类型选择、约束设计
- **索引策略**：B-Tree/GIN/GiST 索引选择、复合索引顺序、覆盖索引
- **ORM 选择**：Prisma vs Drizzle vs SQLAlchemy vs TypeORM 决策指南
- **性能优化**：慢查询分析、EXPLAIN 解读、连接池调优
- **迁移管理**：Schema 变更策略、零停机迁移、回滚方案

## 使用方式

在 Claude Code 中使用 `/database-design` 调用。

```
/database-design 帮我设计一个电商系统的数据库 Schema
/database-design 分析这个慢查询并给出索引优化方案
/database-design 我们团队应该选 Prisma 还是 Drizzle？
```

## 工作流

1. **需求分析** — 实体关系、查询模式、读写比例
2. **Schema 设计** — ER 图、字段定义、约束和默认值
3. **索引规划** — 按查询模式设计索引，避免过度索引
4. **ORM 选型** — 按项目需求和团队经验选择
5. **迁移方案** — 生成迁移文件、验证、回滚预案

## Schema 设计检查清单

```
[ ] 主键选择：UUID vs SERIAL vs ULID
[ ] 时间戳：created_at / updated_at / deleted_at
[ ] 软删除还是硬删除
[ ] 外键约束：CASCADE / SET NULL / RESTRICT
[ ] 字段类型：TEXT vs VARCHAR、INT vs BIGINT、JSONB 合理使用
[ ] 枚举：DB enum 还是应用层常量
[ ] 唯一约束：业务唯一键 + 唯一索引
[ ] 默认值：有意义的默认值，避免 NULL
```

## 适用场景

- 新项目启动时的数据库设计
- 现有数据库性能问题排查
- ORM 选型决策
- 大表 Schema 变更方案设计

## 限制

- 主要覆盖关系型数据库（PostgreSQL/MySQL）
- NoSQL（MongoDB/Redis）仅涉及选型建议，不深入设计
- 不涉及数据仓库（OLAP）设计
- 不替代 DBA 做生产环境调优

## 相关参考（Playbook）

本子技能落地"数据库 Schema 与索引设计"，后端方法论见下列 `references/`（按需读取）：

- 后端深度 playbook（数据建模 / 索引 / 慢查询 / 迁移锁表）：[references/backend-playbook.md](../../references/backend-playbook.md)