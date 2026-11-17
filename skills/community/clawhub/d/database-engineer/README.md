# Database Engineer — 数据库工程师技能库

> 面向独立开发者和后端工程师的数据库技能集合。覆盖 MySQL、PostgreSQL、MongoDB 三大数据库引擎的查询优化、索引设计、性能诊断和可观测性。
>
> 本仓库采用 **superpower 架构**：`SKILL.md` 只做能力路由，方法论 playbook 放在 `references/` 按需加载，
> 引擎专项能力在 `skills/` 子技能，确定性任务交给 `scripts/` 零依赖脚本，可套用的模板在 `assets/`。

## 技能清单

| 技能 | 描述 | 安装量 | 来源 |
|------|------|--------|------|
| mysql | MySQL 查询优化、索引策略、Schema 设计、复制与高可用 | 6.8K | [skills.sh](https://skills.sh/planetscale/database-skills/mysql) |
| postgres-patterns | PostgreSQL 高级查询、索引类型、并发控制、扩展生态 | 7.8K | [skills.sh](https://skills.sh/affaan-m/everything-claude-code/postgres-patterns) |
| mongodb-query-optimizer | MongoDB 聚合管道优化、索引策略、Schema 设计、性能诊断 | 3.8K | [skills.sh](https://skills.sh/mongodb/agent-skills/mongodb-query-optimizer) |
| database-observability | 数据库监控指标、慢查询告警、性能基线、容量规划 | 1.9K | [skills.sh](https://skills.sh/grafana/skills/database-observability) |

## 仓库结构

```
database-engineer/
├── SKILL.md          # L1 路由层：能力索引 + grep 关键词，不含具体实现
├── references/       # L2 方法论 playbook（8 篇，按需加载）
├── skills/           # L3 子技能（4 个引擎/领域专项）
├── scripts/          # L4 零依赖脚本（3 个，可直接 CI 门禁）
└── assets/           # L5 模板资源（3 份）
```

### references/ — 决策与方法论

| 文件 | 解决什么问题 |
|------|-------------|
| `engine-selection.md` | 关系型/文档/KV/时序怎么选，含反模式与迁移成本 |
| `explain-reading.md` | 逐项读懂 MySQL / PostgreSQL / MongoDB 的执行计划 |
| `index-design.md` | ESR 列顺序规则、建不建的决策树、覆盖索引、冗余清理 |
| `slow-query-triage.md` | 从"数据库变慢"到根因的四步法与优化性价比排序 |
| `schema-migration.md` | 扩展-收缩模式、危险操作对照表、零停机 DDL、分批回填 |
| `transactions-locking.md` | 隔离级别取舍、死锁还原、长事务危害、锁策略选择 |
| `capacity-and-pooling.md` | 连接数公式、池化选型、压测口径、三级告警阈值 |
| `backup-recovery.md` | RPO/RTO、三类备份、PITR 操作、恢复演练、3-2-1 |

### scripts/ — 零依赖工具（仅 Python 标准库）

```bash
# Schema DDL 静态检查：13 类结构反模式
python3 scripts/schema_lint.py migrations/ --dialect postgres --strict

# 执行计划审计：自动识别 MySQL 表格/JSON、PG 文本/JSON 四种格式
python3 scripts/explain_audit.py plan.json --strict

# 慢日志指纹聚合：按总耗时排序，回答"先优化哪条"
python3 scripts/slowlog_digest.py /var/log/mysql/slow.log --top 10
```

三者均支持 `--json`（接管道）与 `--strict`（有问题时退出码 1，可做 CI 门禁）。

### assets/ — 可直接套用的模板

- `db-alert-rules.yml` — Prometheus 数据库告警规则，P1/P2/P3 三级共 20 条
- `schema-review-checklist.md` — Schema/索引变更评审清单，含一票否决项
- `backup-runbook.md` — 恢复演练 Runbook 模板，含耗时记录与三层校验口径

## 工作流

```
MySQL ────────┐
PostgreSQL ───┼──→ Database Observability
MongoDB ──────┘    (监控与告警)
(引擎选择与优化)
```

## 安装

```bash
# 安装全部数据库技能
npx skills add skills-repo/database-engineer -g -y

# 或按需安装单个技能
npx skills add skills-repo/database-engineer@mysql -g -y
npx skills add skills-repo/database-engineer@postgres-patterns -g -y
npx skills add skills-repo/database-engineer@mongodb-query-optimizer -g -y
npx skills add skills-repo/database-engineer@database-observability -g -y
```

## 与本组织其他仓库的关系

- **ai-fullstack-engineer** — 应用层架构与 API 设计（原 backend-developer / frontend-engineer 已合并至此），本仓库聚焦数据库引擎深度优化
- **data-scientist** — 数据分析和可视化，本仓库聚焦数据库运维和性能
- **devops-engineer** — CI/CD 和基础设施，本仓库聚焦数据库层可观测性
- **infrastructure-engineer** — 主机、存储与高可用架构，本仓库聚焦数据库自身的设计与调优
- **security-guardian** — 账号权限、注入防护与敏感数据合规审计

## License

MIT