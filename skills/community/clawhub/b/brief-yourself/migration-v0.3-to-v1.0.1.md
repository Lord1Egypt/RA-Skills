# V0.3 → 1.0.1 迁移说明｜Brief Yourself 1.0.1

本文件只在 Brief Yourself 1.0.1 的历史迁移场景读取。当前 schema 身份为 `1.0.1`；旧的 `0.4` 只作为历史输入与旧制品标识保留。

## 结论

V0.3 到 1.0.1 是“可预览、需审核、另存、可回滚”的迁移，不是原地升级。`context_store.py preview-migrate-v03` 只接受 `schema_version = 0.3`，仅读取输入 Store 的 `context.json` 与 `evidence/index.json`。它不会读取 `views/` 或 `patches/`，不会创建 `context.json`，不会覆盖原 Store，也不会把候选写入 Store。

预览报告默认 metadata-only：只报告 schema、计数、ID、字段映射、冲突、未映射字段、丢失风险、输入前后 hash、候选 hash 与 validity，不打印 Claim statement、notes、Source title 或其他原始敏感文本。报告输出若使用 `--output`，必须位于输入 Store 之外。

只有 `candidate_valid = true` 且命令退出码为 0，才说明“候选在确定性规则下完整”；这仍不等于已经物化。任何冲突、无法解析的引用、重复 ID、输入 hash 变化或未知字段都会 fail closed 并返回非零。用户审核报告并明确另存之前，继续使用原 V0.3 Store。

## 固定映射

| V0.3 | 1.0.1 | 约束 |
|---|---|---|
| `profile_id` | `context_id` 与 `subject.id` | 保留同一 ID |
| `subject.preferred_name` | `subject.display_name` | 空字符串也保留 |
| `subject.preferred_languages` | `subject.preferred_languages` | 不改写语言值 |
| `core.claims[]` | `claims[]` | 删除 `layer`/`domain`，`domains=[]` |
| `domains.<name>.claims[]` | `claims[]` | 将容器名稳定加入 `domains[]` |
| `core/domains.tensions[]` | `tensions[]` | 顶层扁平化并保留 domain 标签 |
| `core/domains.unknowns[]` | `unknowns[]` | 顶层扁平化并保留 domain 标签 |
| `promotion_evidence` | `evidence_refs[]` | 仅合法 Source ref 可合并；否则冲突并停止 |
| `sources[]` | `sources[]` | 与 evidence index 逐项核对，原样保留 |
| `revision` | `revision` | 版本和时间不静默改变 |
| V0.3 View/Patch | 不迁移 | 保持冻结；报告列出 `views/**`、`patches/**` |

V0.3 Claim 没有 disclosure 时，候选使用最保守默认：`audiences=["self-agent"]`、`purposes=["user-approved"]`、`allow_downstream_persistence=false`，并在 `defaulted_fields` 标记。这不是用户授权伪造；要用于具体目的仍需用户明确批准。旧 Domain 容器的 `updated_at` 只是 bookkeeping metadata，进入 `retired_legacy_metadata`，不构成冲突；其他未知容器字段不能静默丢弃。

## 输入完整性

预览必须同时验证：

- context/evidence index 都是 JSON object；
- 两者 schema 都是 0.3；
- Source ID、Claim/Tension/Unknown ID 唯一，且全局不碰撞；
- context.sources 与 evidence/index.sources 的记录完全一致；
- evidence refs 能解析到 Source；
- Core、Domain、Tension、Unknown、反例、来源和 revision 都有确定性目标；
- V0.2 被明确拒绝，不执行 V0.2 → V0.3 → 1.0.1 链式迁移。

报告生成前后再次计算输入 SHA-256。任何变化都令候选无效。报告生成本身不能改变输入 Store。

## Store 内派生副本与提交竞态

若后续 1.0.1 Store 内存在 `brief.md`，它属于 controlled manifest 的受控派生副本。任何 purge plan 都把其路径与 hash 纳入 token；plan 之后对 `brief.md` 的新增、修改或删除都会使 token 失效。若 purge 改变 Canonical Context，必须从 purge 后的 Context 重新生成 `brief.md`，并与 canonical、evidence、history、audit 一起事务提交，确保被清除 Claim 的 ID 与 statement 不残留。

提交前和每一个文件 replace/write/delete 前都要重新核对完整 controlled manifest。发现审核窗口内的并发变化时必须 fail closed，不覆盖或回滚并发写入；继续使用原 Store，重新生成 purge plan。

## 显式另存与回滚

当前 runtime 只提供 preview，不提供 `materialize-1.0.1`。未来若批准另存，必须：

1. 把完整 metadata-only report 交给用户审核；
2. 在输入 Store 之外创建新的 1.0.1 目录；
3. 重新验证新 Store 的 context/evidence index、权限、引用和 revision；
4. 保留原 V0.3 Store、其 View/Patch 与历史文件不变；
5. 失败时删除未完成的候选目录或回到可恢复边界，不覆盖 V0.3。

回滚的实际动作是继续使用原 V0.3 Store；不能从 1.0.1 反向推断已退休的元数据或重新生成旧 View/Patch。迁移预览与后续 dogfood 只使用 synthetic fixture；真实 Personal Context 需要另行说明来源、范围、用途、保存位置和删除方式并获得授权。
