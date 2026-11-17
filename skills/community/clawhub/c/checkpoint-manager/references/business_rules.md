# 业务规则 - checkpoint-manager

> 来源: SKILL.md v1.0.0 (ARCH-5) 核心概念 + 验证标准

## 规则列表

- PG权威源: workflow_checkpoints表为唯一权威源,UNIQUE(workflow_id, step_id),所有检查点以PG为准 (来源: SKILL.md核心概念)
- 写入语义: PG写入使用INSERT ON CONFLICT DO UPDATE(upsert),PG成功即返回成功 (来源: SKILL.md核心概念)
- SQLite缓存定位: SQLite仅作为本地可丢失缓存,失败不影响业务 (来源: SKILL.md核心概念)
- 写入路径: state_data → PG(同步,权威源) → SQLite(异步,缓存,可丢失) (来源: SKILL.md核心概念)
- 读取路径: SQLite(快速) → 未命中/过期 → PG(权威源) → 回填SQLite (来源: SKILL.md核心概念)
- 缓存TTL: SQLite缓存默认TTL为300秒,过期后自动回退PG读取 (来源: SKILL.md验证标准)
- 不再双写: 取消v7.0 Saga补偿事务+event sourcing replay,PG单点负责一致性 (来源: SKILL.md核心概念)
- SQLite异步缓存: SQLite写入为fire-and-forget模式,失败不影响业务 (来源: SKILL.md验证标准)
- 缓存回填: SQLite缓存未命中时从PG读取后异步回填SQLite (来源: SKILL.md验证标准)
- 崩溃恢复: SQLite丢失后通过rebuild_sqlite_cache从PG重建缓存 (来源: SKILL.md验证标准)
- 一致性验证: 比对PG与SQLite,检测3类不一致(cache_only/pg_only/data_mismatch) (来源: SKILL.md验证标准)
- 多租户隔离: 通过tenant_id字段隔离,支持按租户重建缓存 (来源: SKILL.md验证标准)
- 重建上限: rebuild_sqlite_cache从PG读取最多10000条检查点 (来源: SKILL.md流程F)
- 数据一致性目标: 99.9%(从v7.0的95%提升) (来源: SKILL.md验证标准)
- SQLite模式: 使用WAL模式提升并发读取性能 (来源: SKILL.md核心概念)
