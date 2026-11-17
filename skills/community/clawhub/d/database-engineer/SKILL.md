---
name: database-engineer
description: >-
  数据库选型、索引设计、执行计划分析、慢查询治理、零停机 Schema 迁移、事务与锁排查、
  容量规划与备份恢复的 AI Agent 技能库，覆盖 MySQL / PostgreSQL / MongoDB。
  帮助开发者把"数据库很慢"这类模糊症状，变成有 EXPLAIN 证据、有优化优先级、有回滚方案的确定性动作。
  内置 Schema 静态检查、执行计划审计、慢日志指纹聚合三套零依赖脚本。
  触发词："数据库、选型、索引、复合索引、EXPLAIN、执行计划、慢查询、慢日志、SQL 优化、全表扫描、
  Schema 迁移、DDL、加字段、分库分表、事务、隔离级别、死锁、锁等待、连接池、容量规划、
  备份、恢复、PITR、主从、复制延迟、MySQL、PostgreSQL、MongoDB"。
agent_created: true
metadata:
  version: 1.0.0
  category: 数据库
  difficulty: 进阶
  architecture: superpower
---

# 数据库工程师

> 把 AI 助手变成一名能独立扛下数据库全生命周期的工程搭档：从选型、建模、索引设计，到慢查询定位、
> 零停机变更、锁冲突排查、容量规划与恢复演练——每个结论都基于执行计划与指标，而不是"感觉加个索引"。

本技能采用 **superpower 架构**：`SKILL.md` 只做路由，深层 playbook 放在 `references/` 中**按需加载**，
细粒度能力放在 `skills/` 子技能，确定性任务交给 `scripts/`，可复用模板放在 `assets/`。

## 何时使用

在以下任一情况触发本技能：

- 新项目/新模块要**选数据库**，需要在关系型、文档型、KV、时序之间做有依据的取舍。
- 接口变慢、CPU 打满、数据库告警，需要**定位到具体的慢 SQL** 并给出优化优先级。
- 要**设计或评审索引**：列顺序怎么排、该不该加、会不会冗余、写入代价多大。
- 需要读懂 **EXPLAIN 执行计划**，判断为什么没走索引、为什么出现 filesort / Seq Scan。
- 线上大表要**加字段、改类型、加索引**，必须零停机且有回滚方案。
- 出现**死锁、锁等待、事务超时**，需要还原加锁顺序并给出根治方案。
- 做**容量规划与连接池配置**，或需要一套可落地的数据库告警阈值。
- 制定**备份策略、验证 PITR、组织恢复演练**。

## 能力索引（超级技能路由）

本技能采用渐进式加载（progressive disclosure）。`SKILL.md` 仅作路由，**按需**读取下列
`references/` 中的完整 playbook，避免一次性占满上下文。

| 任务 | 读取 / 调用 | 关键词（grep 线索） |
|------|------------|---------------------|
| 引擎选型：关系型/文档/KV/时序决策树、反模式、迁移成本 | [references/engine-selection.md](references/engine-selection.md) | 选型、技术选型、用什么数据库、NoSQL、文档型、时序、KV |
| 读执行计划：MySQL type/Extra、PG 节点类型、Mongo COLLSCAN 逐项释义 | [references/explain-reading.md](references/explain-reading.md) | EXPLAIN、执行计划、分析计划、Seq Scan、filesort、type=ALL |
| 索引设计：ESR 列顺序规则、建不建的决策树、覆盖索引、冗余清理、写入成本 | [references/index-design.md](references/index-design.md) | 索引、复合索引、联合索引、ESR、覆盖索引、索引失效、选择性 |
| 慢查询治理：从告警到根因的四步法、采集口径、按性价比排序的优化手段 | [references/slow-query-triage.md](references/slow-query-triage.md) | 慢查询、慢日志、SQL 优化、数据库变慢、性能排查、pg_stat_statements |
| Schema 迁移：扩展-收缩模式、危险操作对照表、CONCURRENTLY/NOT VALID、gh-ost、分批回填 | [references/schema-migration.md](references/schema-migration.md) | 迁移、DDL、加字段、改类型、零停机、gh-ost、锁表、回填 |
| 事务与锁：隔离级别取舍、死锁还原、长事务危害、悲观/乐观锁选择 | [references/transactions-locking.md](references/transactions-locking.md) | 事务、隔离级别、死锁、锁等待、MVCC、幻读、乐观锁、长事务 |
| 容量与连接池：连接数公式、池化选型、压测口径、三级告警阈值 | [references/capacity-and-pooling.md](references/capacity-and-pooling.md) | 容量规划、连接池、PgBouncer、max_connections、压测、告警阈值 |
| 备份恢复：RPO/RTO 定义、三类备份、PITR 操作、恢复演练、3-2-1 原则 | [references/backup-recovery.md](references/backup-recovery.md) | 备份、恢复、PITR、binlog、WAL、演练、RPO、RTO、误删数据 |
| MySQL 专项：查询优化、索引策略、Schema 设计、存储引擎、复制与高可用 | [skills/mysql/SKILL.md](skills/mysql/SKILL.md) | MySQL、InnoDB、主从、binlog、my.cnf |
| PostgreSQL 专项：高级查询、索引类型、并发控制、扩展、性能调优 | [skills/postgres-patterns/SKILL.md](skills/postgres-patterns/SKILL.md) | PostgreSQL、PG、GIN、GiST、VACUUM、CTE、分区表 |
| MongoDB 专项：聚合管道、索引策略、Schema 设计、性能诊断 | [skills/mongodb-query-optimizer/SKILL.md](skills/mongodb-query-optimizer/SKILL.md) | MongoDB、聚合管道、aggregate、文档模型、分片 |
| 可观测性专项：监控指标、慢查询告警、性能基线、日志分析 | [skills/database-observability/SKILL.md](skills/database-observability/SKILL.md) | 监控、可观测性、指标、基线、告警、Prometheus、exporter |

> 路由规则：**先判断任务层次**。做决策与取舍（选哪个引擎、要不要加索引、用什么隔离级别）读
> `references/`；要落地某个引擎的具体语法与命令，直接调对应 `skills/` 子技能；
> 能被脚本确定性完成的（Schema 检查、计划审计、慢日志聚合）优先跑 `scripts/`，不要人肉逐条读。

## 内置脚本（确定性、可重复执行）

放在 `scripts/`，均为**零依赖**（仅 Python 标准库），可直接在生产跳板机运行：

- `scripts/schema_lint.py <file|dir> [--dialect mysql|postgres|auto] [--json] [--strict]`
  — 扫描 SQL DDL 的 13 类结构反模式（无主键、金额用浮点、utf8 非 utf8mb4、外键缺索引、
  TIMESTAMP 2038 溢出、INT 自增溢出、ENUM、列数失控等），输出分级问题清单。
- `scripts/explain_audit.py <plan-file> [--json] [--strict]`
  — 审计执行计划，自动识别 MySQL 表格/JSON 与 PostgreSQL 文本/JSON 四种格式，
  报出全表扫描、filesort、临时表、Nested Loop 高 loops、行数估算偏差等问题。
- `scripts/slowlog_digest.py <slow.log> [--top N] [--sort total|avg|count|examined] [--json] [--strict]`
  — MySQL 慢日志指纹聚合，把海量日志按归一化 SQL 归并并按总耗时排序，回答"先优化哪条"。

运行示例：

```bash
python3 scripts/schema_lint.py migrations/ --dialect postgres --strict
mysql -e "EXPLAIN FORMAT=JSON SELECT ..." > plan.json && python3 scripts/explain_audit.py plan.json
python3 scripts/slowlog_digest.py /var/log/mysql/slow.log --top 10
```

三个脚本均支持 `--json`（接管道）与 `--strict`（发现问题时退出码 1，可直接做 CI 门禁）。

## 模板资源

`assets/` 提供可直接套用的配置与模板：

- [assets/db-alert-rules.yml](assets/db-alert-rules.yml) — Prometheus 数据库告警规则，含 P1/P2/P3 三级共 20 条：
  磁盘写满预测、连接数、复制中断与延迟、缓存命中、长事务、XID 回卷、备份心跳等。
- [assets/schema-review-checklist.md](assets/schema-review-checklist.md) — Schema/索引变更评审清单，标注了哪些项可由脚本自动检查，
  附风险等级与一票否决项。
- [assets/backup-runbook.md](assets/backup-runbook.md) — 恢复演练 Runbook 模板，含耗时记录表、三层数据校验口径、
  复盘表与五种真实失败模式。

## 核心原则（始终遵循）

1. **先测量，再优化**。没有 EXPLAIN 输出或慢日志数据就动手改索引，是在赌博。
   所有优化建议必须附"改动前后的计划对比"。
2. **索引不是越多越好**。每个索引都在给写入加税；建索引前先算选择性，建完后确认它真的被用上了。
3. **渐进式加载**：先读路由表与对应 `references/`，再动手；不凭记忆猜命令与参数——
   MySQL 与 PostgreSQL 的语法、锁行为、DDL 在线能力差异极大，且随版本变化。
4. **生产变更必须可回滚**。扩展-收缩三阶段、分批回填、锁超时护栏、回滚脚本，缺一不可；
   "把新加的列删掉"通常不是合法回滚方案，因为数据已经没了。
5. **明确边界**：本技能给出诊断、方案与风险评估，**不代替用户在生产库执行破坏性操作**。
   涉及删表、删索引、KILL 事务、跳过复制错误时，只输出命令与前置确认项，由用户自行执行。

## 与其他技能协作

- 需要应用层的 ORM/连接管理与 API 设计 → 调用 `skills-repo/ai-fullstack-engineer`
- 需要数据库主机、存储、高可用架构与基础设施编排 → 调用 `skills-repo/infrastructure-engineer`
- 需要监控告警落地、SLO 定义与部署流水线 → 调用 `skills-repo/devops-engineer`
- 需要数据库账号权限、注入防护与敏感数据合规审计 → 调用 `skills-repo/security-guardian`
- 需要面向分析的数据建模、指标口径与查询 → 调用 `skills-repo/data-scientist`
