# Personal Context Model｜Brief Yourself 1.0.1

## 定位

Brief Yourself 1.0.1 的 `Personal Context Store` 是个人上下文的 canonical source，不是第二套 Harness Memory。它的 active `schema_version` 为 `1.0.1`；Store 只保存用户可审核的 Claim、Tension、Unknown、来源引用、披露权限和版本信息。Codex Memory、rollout、项目文档或其他 harness memory 不会自动进入 Store；即使用户授权读取，也只能先作为候选证据。

Store 的顶层字段固定为：

```text
schema_version, context_id, subject, policy, coverage,
claims, tensions, unknowns, sources, revision
```

Store 不再物理保存 `core` 或 `domains`。`domains[]` 是 Claim 的标签；Core Summary 由运行时按条件派生，保留原 Claim ID，不写回 Store。
`Tension` 与 `Unknown` 是与 Claim 并列的当前 1.0.1 canonical Store 顶层实体，也可作为完整冻结对象进入 View；它们不是永久 session-only。会话新发现的 Tension/Unknown 在当前协议下只能先作为“未持久化候选”交付，等待未来显式写入协议。

## Claim 与证据

Claim 必须保留 `kind`、`scope`、`durability`、`confidence`、`user_status`、`status`、`sensitivity`、`evidence_refs`、`counterevidence_refs`、时间字段、`supersedes` 和 `notes`。`kind` 区分 `fact`、`self_report`、`observation`、`inference`；推断不能因为写入 Store 就变成事实。

`sensitivity` 只描述内容敏感程度：`public`、`private`、`restricted`。`disclosure` 是独立的目的和受众授权：

```json
{
  "audiences": ["self-agent"],
  "purposes": ["resume-review"],
  "allow_downstream_persistence": false
}
```

二者不能互相替代。Claim、Tension、Unknown 与 Source 的 ID 在 Store 内必须唯一；Evidence ref 的 Source ID 必须能在 `sources[]` 和 `evidence/index.json` 中解析。

## Core Summary

`derive-core-summary` 只选择同时满足以下条件的 Claim：

- `user_status = confirmed`；
- `status = active`；
- `scope = cross-context`；
- `durability = stable` 或 `evolving`；
- `kind != inference`。

摘要是读取时的派生结果，必须带回原 Claim ID。它不会创建第二份事实源，也不会因为被导出而改变 Claim 的层级、权限或 revision。

## 版本与来源

每次长期写入都递增 `revision.version`，更新 `updated_at`，在写入前保存 `history/context-vN.json`，并在 `history/changes.jsonl` 留下不含原文的审计记录。Source 登记需要显式 `--approve` 和确认主体，同时更新 Canonical Store 与 evidence index。

若 Store 内存在 `brief.md`，它是由 Canonical Context 派生的受控副本，不是第二事实源。它会进入 purge manifest；purge 若改变 Canonical Context，必须用 purge 后的 Context 在同一事务中重生成，不能保留已删除 Claim 的 ID 或 statement。purge 在每次 replace/write/delete 前重新核对受控路径集合、字节 hash 和文件身份；审核窗口内发现并发新增、修改或删除时直接中止，并保留并发修改。

V0.3 Store 仍可用 `validate`、`inspect` 查看，但不能直接 `export`，也不能被 1.0.1 当前 runtime 原地升级。`preview-migrate-v03` 只读读取 `context.json` 与 `evidence/index.json`，在内存生成 1.0.1 候选并输出 metadata-only report；它不物化新 Store、不改写输入，也不读取旧 View/Patch。若预览失败，继续使用原 V0.3 Store；回滚不通过从旧 `0.4` 制品反向重建。

V0.2 只能在副本上通过既有 `migrate-v02` 显式迁移到 V0.3，不能链式进入 1.0.1。

## View 与 Patch 的边界

View 是按 `subject + principal + audience + purpose + task + source_revision + expiry` 生成的完整冻结对象。默认 TTL 为 7 天，默认只选 `public`。`private` 与 `restricted` 必须显式旗标，并且每个 Claim 必须同时授权：

1. disclosure.audiences 包含 exact `principal.id`；
2. disclosure.audiences 包含 View 的每一个 `audience[].id`；
3. disclosure.purposes 包含 exact purpose，或包含 `user-approved` 且命令带 `--purpose-approved`；
4. 1.0 runtime 的 principal / audience 类型必须为 `agent`；非公开 Tension / Unknown 也必须满足同一 disclosure 边界；
5. `unreviewed` / `unresolved` 默认排除，只有显式 `--include-unreviewed` 才能纳入。

默认 principal 为 `self-agent`。Team Agent 不会因为“同属一个团队”而获得 self-agent Claim；除非 Claim 明确授权该 Team Agent 及 View 的全部 audience。View 创建后不刷新；Store revision 变化只会让校验给出冻结版本提示，不会改变已保存内容。

Patch 是唯一长期回流路径。新写入只允许 `add`、`update`、`challenge`、`retire`；不写 `promote`、`demote`、`target_layer` 或 `target_domain`。Apply 必须同时具备具体 Patch 的审核决定、`--approve` 和确认 actor。更新同一 Claim ID 时，旧表述留在 history snapshot；父 revision 或 source revision 冲突时拒绝。Stage 与 reject 不改 Canonical Store。
当前 Patch schema/runtime 的 Proposal 只提供 Claim 的四种 action，没有 Tension/Unknown 的新增或更新入口。因此不得把会话候选静默写入 Store、伪装成 Claim、放入 `task_strategies_not_for_merge`，或声称已经长期保存；未来入口需要另行 schema/runtime/approval，本轮不实施。已有迁移或 Store 中的 Tension/Unknown 仍保持可读，并可按需进入冻结 View。

## Harness 边界

Personal Context 不自动同步到 Codex Memory，也不接管 rollout、thread、retrieval 或 consolidation。Adapter 只能把已冻结、带 revision/TTL/权限的 View 交给下游；任务完成后只能返回待审核 Patch。个人 Context 与未来 Organization Context 共用 envelope 的主体、执行者、受众、用途、版本和有效期字段，但 1.0.1 当前版本只实现 `subject.type = person`。
