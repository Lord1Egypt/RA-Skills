# 维护规格

回填时，路径指定待检查代码，描述提出拟定行为。
无回填目标时，只发现候选。

| 模式 | 工作 |
| --- | --- |
| `audit` | 下述只读覆盖审计与拟定修复计划 |
| `concept` / `sync` | [重建规格](../references/spec-reconstruction.md) |
| `drift` | [只读契约对比](../references/drift-checks.md) |
| `pipeline` | [数据转换规格](../references/pipeline-spec.md) |
| `map` | [概念与同步关系图](../references/diagram-contract.md#使用)：从 CONCEPT/SYNCS 生成一份 ARCHITECTURE.md |
| `claude` | [校准 CLAUDE.md](../references/claude-rules.md) |

CONCEPT 与概念所属 PIPELINE 放概念旁。
跨概念管道放组合。
每个业务规则分组共置一份 SYNCS；索引全部分组，不重复规则。
授权修改规格后，更新索引并按内容重新生成关系图。
保留人工备注和已确认旧行为。
关系图 MUST NOT 成为权威契约。

## 审计

读范围内约定、PRD/暂存索引、规格、入口、状态/模式/迁移、测试、构建清单和地图。
跳过依赖/生成/构建目录，包含单文件核心模块。
声明祖先覆盖前读内容。
逐模块/流程标为已覆盖、暂存、缺失、支撑代码或未核实。
注明权威文件与实际范围，或缺证据/跳过理由。
即使经公开 API，概念互调仍报告耦合。

报告范围、实测计数、候选位置、断链和迁移工作。
覆盖率 MUST 枚举分母。
按实际代码依赖排列拟定回填；循环一起处理，并标边界问题。
每条拟定命令注明模式、路径、证据、产物和前提；同批按路径排序。
audit MUST NOT 执行修复。
