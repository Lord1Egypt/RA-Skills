---
name: database-observability
description: 数据库可观测性：监控指标、慢查询告警、性能基线、日志分析、容量规划
source:
  type: derived
  repo: skills-repo/database-engineer
  path: skills/database-observability/SKILL.md
  url: https://skills.sh/grafana/skills/database-observability
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
  - database
  - observability
  - monitoring
  - performance
  - alerting
---

# Database Observability — 数据库可观测性

> 数据库不出问题时没人看监控，出问题时都后悔没提前配。好的可观测性不是 100 张仪表盘，是 3 个核心指标 + 及时告警。本技能覆盖数据库监控体系搭建。

## 能力

- **核心指标**：QPS/TPS、连接数、复制延迟、Buffer Pool 命中率、慢查询数
- **告警策略**：分级告警（P0-P3）、阈值设定、告警收敛、值班轮转
- **慢查询分析**：自动采集、趋势对比、执行计划变化检测
- **容量规划**：磁盘增长预测、连接数趋势、QPS 容量评估
- **日志分析**：错误日志解析、审计日志检索、异常模式检测

## 使用方式

在 Claude Code 中使用 `/database-observability` 调用。

```
/database-observability 帮我设计数据库监控的关键指标和告警阈值
/database-observability 最近慢查询增多，帮我排查趋势
/database-observability 评估当前数据库容量是否够支撑下季度增长
```

## 监控分层

```
L1: 应用层 — 慢查询日志 + APM (P0/P1)
L2: 数据库层 — QPS/连接/复制/锁 (P0/P1/P2)
L3: 系统层 — CPU/内存/磁盘 IO/网络 (P1/P2)
L4: 容量层 — 磁盘/连接数/备份 趋势 (P2/P3)
```

## 适用场景

- 开发团队为生产数据库搭建监控
- 排查数据库性能问题的第一站
- 季度容量规划和资源评估
- 数据库迁移前后的性能基线对比

## 限制

- 聚焦监控策略和指标设计，不涉及具体监控系统部署
- 覆盖 MySQL/PostgreSQL/MongoDB 通用指标，不深入单产品
- 容量规划覆盖基础预测模型，不涉及复杂资源调度

## 相关参考（Playbook）

慢查询先由监控发现再进分诊 → [references/slow-query-triage.md](../../references/slow-query-triage.md)（[scripts/slowlog_digest.py](../../scripts/slowlog_digest.py)）；
连接池与容量规划（告警分级）→ [references/capacity-and-pooling.md](../../references/capacity-and-pooling.md)；
备份任务成功心跳监控 → [references/backup-recovery.md](../../references/backup-recovery.md)；
锁等待监控 → [references/transactions-locking.md](../../references/transactions-locking.md)；
执行计划体检（辅助定位瓶颈）→ [references/explain-reading.md](../../references/explain-reading.md)（[scripts/explain_audit.py](../../scripts/explain_audit.py)）；
索引/迁移的观测视角 → [references/index-design.md](../../references/index-design.md)、[references/schema-migration.md](../../references/schema-migration.md)；
选型阶段的可观测性成本 → [references/engine-selection.md](../../references/engine-selection.md)。
