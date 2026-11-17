# 脚本目录错误码与修改纪律

> 本文件随 `flydb-migration-scripts` 打包，按 Flydb CLI 0.3.x 维护。完整错误码表见姊妹技能 `flydb-cli-release` 的 `references/errors.md`；此处只收录与迁移脚本直接相关的部分。

## 修改纪律（红线）

1. **已应用的 `V` 脚本绝不修改**。checksum 记录在历史表 `flydb_schema_history` 中，改动文件内容即触发 `FLYDB-2003`。对已应用版本的任何变更——改 SQL、改格式、改文件名——都用**新版本脚本**承载。
2. **`R` 脚本的修改等于重跑**。这是设计语义而非事故：checksum 变化后下次 migrate 重新执行。修改 R 脚本前确认它幂等/可重建（典型如视图、函数定义）。
3. **`U` 与 `V` 配对维护**。新增带回退需求的 `V` 脚本时同步提供 `U<同版本>__`；修改已应用 V 的回退逻辑属于变更历史，只能通过新版本承载。
4. **不删除已应用的脚本文件**。删掉后历史记录变 `MISSING`（`FLYDB-2003`）。迁移目录切换期间把新旧位置逗号并列：

```properties
flydb.locations=filesystem:/opt/app/new-migrations,filesystem:/opt/flydb/db/migration
```

5. **`repair` 改写历史表**，不属于本技能的日常操作：修正脚本后由用户明确决定是否 repair（执行 CLI 命令属 `flydb-cli-release` 技能范围）。不要用 repair 掩盖集合不完整。

## 错误码速查

| 错误码 | 场景 | Agent 应对 |
|---|---|---|
| `FLYDB-2001` | 版本未以数字开头、含空段/非法字符，或 `V`/`U` 候选命名无法解析；目录版本模式下文件版本不属于目录版本族 | 按命名规则改名（`V<版本>__<描述>.sql`）；不要建议忽略该文件继续 |
| `FLYDB-2002` | 多个脚本解析为同一版本（含 `1` 与 `1.0` 这类语义等价版本） | 为新脚本分配唯一版本号 |
| `FLYDB-2003` | checksum 不一致 / 已应用脚本 `MISSING` / 历史版本 `FUTURE` | 分类处理，见下节 |
| `FLYDB-2004` | 历史表存在 `success=false` 的失败记录 | 先核验失败事务与已落库对象，再修正脚本并由用户决定历史修复；不要直接重跑或自动 repair |
| `FLYDB-2005` | 发现旧式 `R<version>__...sql` | 回退脚本改名 `U<version>__...sql`，可重复脚本改名 `R__...sql`；无兼容开关 |
| `FLYDB-2006` | 未启用 `out-of-order` 时出现低版本补执行 | 按序补齐，或与用户确认后设置 `out-of-order=true` |
| `FLYDB-2008` | `undo` 时最近版本没有对应 `U<版本>__` 脚本 | 补齐配对的撤销脚本 |
| `FLYDB-2009` | 未定义占位符，或业务运行时模板被误识别 | 前者补 `flydb.placeholders.*` 或 `-D<key>=<value>`；后者设 `placeholder-replacement=false` 原样保留，不要为模板变量随意赋值 |
| `FLYDB-2010` | SQL/JDBC 执行失败 | 读取失败阶段、事务结果与定位可信度，按下节核验现场 |
| `FLYDB-2011` | 已确认计划与锁内重新核对的计划不同 | 重新预览并核对目标和脚本；不能复用旧确认，不能据此断言基础设施完全未变 |
| `FLYDB-4005` | `flydb.locations` 指向的目录不存在 | 核对前缀（`filesystem:`/`classpath:`）与路径；相对路径注意 CWD，或改绝对路径 |

## FLYDB-2003 分类处置

`FLYDB-2003` 有三种详情，处理方向完全不同，先看消息里的分类再动手：

- **checksum 不一致**：本地文件内容与历史记录的 checksum 不符。先查明改动是否预期——团队确实修正过脚本内容 → 由用户决定是否 repair 对齐；无人承认改动 → 用版本控制对比找回原文件，不要急于 repair。
- **`MISSING`**：历史表里有记录但当前迁移集合里找不到该脚本。按顺序检查：`locations` 配置是否变了、执行 CLI 的当前工作目录、路径过滤条件（glob/regex 是否把脚本滤掉）、代码版本是否落后。这些都正常才考虑脚本被误删。
- **`FUTURE`**：数据库历史版本比本地脚本新。通常是连错了环境或本地代码没拉到最新；先核对环境与分支，不要在本地"补写"高版本脚本去迎合。

## 失败记录的处置顺序

`migrate` 失败可能留下 `success=false` 记录；历史写入本身失败时也可能没有完整记录。存在失败记录会阻断后续 migrate。正确顺序：

1. 保存原始错误与“迁移失败执行快照”：失败阶段、事务模式、confirmed、定位可信度、事务结果。`confirmed` 只是首个已定位失败前 JDBC 连续成功前缀，不等于已提交，也不包含失败后的返回项。
2. 仅明确 ROLLED_BACK/“已回滚”才能按整体回滚处理；NON_TRANSACTIONAL、COMMIT_UNKNOWN、ROLLBACK_FAILED 或 UNKNOWN 先核对数据库对象、数据和历史。MySQL/Oracle 家族纯 INSERT/UPDATE/DELETE/MERGE 脚本可使用整脚本事务，含 DDL/过程块/WITH 等不能套用此结论。
3. 按可靠定位修正失败脚本；batch 有 EXECUTE_FAILED 标记时可精确定位，仅有遇错即停计数时是推算，无可靠标记时检查候选批次。不能用“尚未成功”推导可以安全重跑。
4. 由用户确认修复策略，必要时经 CLI 技能执行 repair；repair 不撤销已执行 SQL。重新 validate → dry-run 核对集合与目标 → 在授权范围内 migrate。
