# Database Engineer — Agent 入口

> 本仓库是 skills-repo 组织下的数据库工程师技能库。面向独立开发者和后端工程师，覆盖 MySQL、PostgreSQL、MongoDB 三大数据库引擎的查询优化、索引设计、性能诊断和可观测性。

## 架构约定（superpower）

本仓库采用 superpower 五层结构，Agent 请**从 `SKILL.md` 的能力索引表进入**，不要一次性读全库：

| 层 | 目录 | 职责 | 加载方式 |
|----|------|------|---------|
| L1 | `SKILL.md` | 路由层：能力索引 + grep 关键词，不含实现细节 | always |
| L2 | `references/` | 方法论 playbook（8 篇：选型/计划/索引/慢查询/迁移/事务/容量/备份） | 按需 |
| L3 | `skills/` | 引擎与领域专项子技能（4 个） | 按需 |
| L4 | `scripts/` | 零依赖脚本（3 个），确定性任务优先用脚本 | 按需执行 |
| L5 | `assets/` | 可直接套用的模板（3 份） | 按需 |

**路由规则**：做决策与取舍读 `references/`；落地某引擎的具体语法调 `skills/`；
能被脚本确定性完成的（Schema 检查、计划审计、慢日志聚合）优先跑 `scripts/`，不要人肉逐条读。

**维护约定**：
- `skills/` 下的子技能**只增不减**，不得删除或改名（下游 `skills-lock.json` 已锁定路径）。
- 新增 `references/` 或 `scripts/` 后，必须同步在 `SKILL.md` 能力索引表登记，避免产生孤儿文件。
- 脚本保持零依赖（仅 Python 标准库），且必须支持 `--help`；改动后需用构造的坏样本验证能真报错。

## 技能清单

| 环节 | 技能 | 文件 | 用途 |
|------|------|------|------|
| 关系型 | mysql | [skills/mysql/SKILL.md](skills/mysql/SKILL.md) | MySQL 查询优化、索引、Schema、复制 |
| 关系型 | postgres-patterns | [skills/postgres-patterns/SKILL.md](skills/postgres-patterns/SKILL.md) | PostgreSQL 高级查询、并发、扩展 |
| 文档型 | mongodb-query-optimizer | [skills/mongodb-query-optimizer/SKILL.md](skills/mongodb-query-optimizer/SKILL.md) | MongoDB 聚合管道、索引、Schema |
| 运维 | database-observability | [skills/database-observability/SKILL.md](skills/database-observability/SKILL.md) | 监控指标、告警、容量规划 |

## 使用场景

- 独立开发者为应用选择数据库引擎
- 后端工程师排查慢查询和性能瓶颈
- 数据库 Schema 设计和索引策略评审
- 生产数据库监控和告警体系搭建

## 相关仓库

- `ai-fullstack-engineer` — 应用层架构与 API 设计（原 backend-developer / frontend-engineer 已合并至此）
- `data-scientist` — 数据分析和可视化，本仓库聚焦数据库运维和性能
- `devops-engineer` — CI/CD 和基础设施，本仓库聚焦数据库层可观测性
- `infrastructure-engineer` — 主机、存储与高可用架构
- `security-guardian` — 数据库账号权限、注入防护与敏感数据合规

> 本仓库聚焦**数据库引擎的深度优化和运维**，与 ai-fullstack-engineer 的应用层架构设计互补。