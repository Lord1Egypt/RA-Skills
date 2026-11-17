# Context View And Patch Protocol｜Brief Yourself 1.0.1

Brief Yourself 1.0.1 把 `Context View` 作为按目的编译的冻结 Context Envelope，把 `Context Patch` 作为唯一的长期回流入口。View 是任务输入，不是新的事实源；Patch 是候选变更，不是自动写回。

## 1. Frozen Context Envelope

View 至少包含以下字段，字段名与 `assets/schemas/context-view-v1.0.1.schema.json` 对齐：

```json
{
"schema_version": "1.0.1",
  "view_id": "view-001",
  "subject": {"type": "person", "id": "user-controlled-id"},
  "principal": {"type": "agent", "id": "current-agent"},
  "audience": [{"type": "agent", "id": "current-agent"}],
  "purpose": "current-task",
  "task": "task-id",
  "source_revision": 1,
  "created_at": "2026-08-21T00:00:00Z",
  "expires_at": "2026-08-28T00:00:00Z",
  "claims": [],
  "tensions": [],
  "relevant_unknowns": [],
  "exclusions": [],
  "permission": {
    "allowed_use": "current task only",
    "archive_in_personal_store": false,
    "allow_downstream_persistence": false
  }
}
```

`claims`、`tensions` 和 `relevant_unknowns` 必须放入带原始 ID 的完整冻结对象，不能只放 Claim/Tension/Unknown ID。对象应保留类型、适用范围、置信度、用户状态、证据引用、counterevidence、敏感度和必要的 disclosure；`exclusions` 记录未纳入的 ID/类别和原因，但不复制被排除的敏感原文。

Envelope 中的 `subject.type` 固定为 `person`；`principal` 是实际执行者，`audience` 是允许看到 View 的主体；`purpose` 是本次确切用途；`task` 是下游任务标识。不能用“当前工作区”“同一团队”或角色名称代替精确 ID。

## 2. 编译与披露规则

1. 先声明用途，再按最小必要原则选择 Claim、Tension 和 Unknown；Domain 只作筛选标签，不自动带入整个领域。
2. `source_revision` 必须对应生成时的 Store revision。View 创建后立即冻结；Store 更新、用户新增授权或任务改变，都不能静默刷新旧 View，必须重新生成新 `view_id`。
3. 默认只包含 `public` 内容，并排除 `private`、`restricted`、`rejected`、`retired` 或尚未达到当前披露门槛的对象。private/restricted 需要当前用途下逐项明确批准；没有批准就放入 `exclusions`。
4. 对每条 included Claim，以及每条非公开 Tension / Unknown 检查 disclosure：`disclosure.audiences` 必须同时精确授权 `principal.id` 和 `audience[]` 中每个实体的 `id`，并且请求的 `purpose` 必须与 `disclosure.purposes` 精确匹配。只授权 principal、遗漏任一 audience recipient 时拒绝编译；别名、角色、同一项目或“都由用户使用”都不算匹配。
5. `purposes: ["user-approved"]` 不是通配符。它表示需要用户确认；编译前仍要展示本次具体 purpose 并取得明确 purpose approval，不能把一次 approval 延伸到未来用途。
6. 1.0 runtime 的 principal / audience 类型只接受 `agent`；`team-agent`、组织主体、共享频道或未识别类型默认拒绝。默认 `self-agent` 只允许已明确授权的个人 principal，不能流向其他 recipient；每个 audience 实体都必须单独通过 disclosure 匹配。
7. `confirmed` / `corrected` 默认可进入 View；`unreviewed` / `unresolved` 默认排除，只有用户明确批准并传入 `--include-unreviewed` 才可纳入。
8. `permission.archive_in_personal_store` 只决定是否在 Personal Context Store 归档该 View；`permission.allow_downstream_persistence` 单独决定下游能否保留副本。前者为 true 不代表后者为 true。
9. `expires_at` 默认是创建时间之后 7 天（TTL）。当前版本不使用 `never_expires`；过期 View 的验证必须失败，不能继续作为默认上下文。

`--expected-audience type:id` 是调用方提供的可重复子集绑定，而不是新的披露授权：每个 expected 值都必须存在于冻结 `view.audience`，调用方不必枚举全部 audience，因此它不是 audience equality/exhaustive assertion。无论是否提供该参数，编译和适配仍须对每条 included Claim 检查 disclosure 是否同时覆盖 `principal.id`、View Envelope 中全部 audience recipient IDs 和本次 purpose；expected-audience 子集不能放宽 disclosure。

若主体、执行者、受众、用途、披露、敏感度、版本或有效期无法确定，拒绝生成 View 并向用户说明缺口，不用模糊默认值绕过授权。

## 3. Context Patch 结构

Patch 必须符合 1.0.1 当前版本的 Envelope 约束，且只允许以下四种 Proposal action：`add`、`update`、`challenge`、`retire`。

```json
{
"schema_version": "1.0.1",
  "patch_id": "patch-001",
  "subject": {"type": "person", "id": "user-controlled-id"},
  "principal": {"type": "agent", "id": "current-agent"},
  "purpose": "user-review",
  "source_task": "task-id",
  "source_revision": 1,
  "created_at": "2026-08-21T00:00:00Z",
  "status": "pending",
  "proposals": [
    {
      "action": "add",
      "target_claim_id": null,
      "candidate_claim": {},
      "evidence_refs": [],
      "reason": "",
      "user_decision": "pending"
    }
  ],
  "task_strategies_not_for_merge": []
}
```

- `add` 新增候选 Claim；`update` 更新同一 Claim（候选 ID 必须等于 `target_claim_id`）；`challenge` 保留原文并标记待挑战；`retire` 使已有 Claim 失效但保留历史。
- `task_strategies_not_for_merge` 只保存本次任务策略、临时话术、JD 关键词或一次性 TODO 的隔离记录，不能并入长期 Claim。
- 新 Patch 不能写 `target_layer`、`target_domain`、`promote` 或 `demote`。Core Summary 是由 Claim 派生的摘要，不需要物理晋升/降级。

`Tension` 与 `Unknown` 仍是当前 1.0.1 canonical Store 的顶层实体，也可以作为完整冻结对象进入 View；它们不是永久 session-only。当前 Patch schema/runtime 的 Proposal 只支持 Claim 的 `add`、`update`、`challenge`、`retire`，本轮没有 Tension/Unknown 的新增或更新入口。会话中新发现的 Tension/Unknown 只能作为“未持久化候选”交付并等待未来显式协议；不得静默写入 Store、伪装成 Claim、塞入 `task_strategies_not_for_merge`，或声称已长期保存。已有迁移/Store 中的对象保持可读并可选入 View；未来写入口需要另行 schema/runtime/approval，本轮不实施。

V0.3 遗留 Patch 中的 `promote`/`demote` 只能作为兼容读取、迁移报告或人工审查材料；它们不是当前版本的新写入 action。若旧操作需要表达为当前版本变更，由用户另行审核具体的 `add`/`update`/`challenge`/`retire` 组合。

## 4. Stage、Review 与 Apply

任务结束时只创建 `status: pending` Patch，并写入 `patches/pending/` 或等价的 pending 区域；Stage 阶段不得修改 Canonical Store、Store revision、Core Summary 或 Harness Memory。

审核时逐项显示：原 Claim（如有）、候选文本、action、证据和 counterevidence、适用范围、敏感度、披露、可能影响，以及本次是否加入下游。用户必须明确批准具体 Patch（`patch_id`）和每个 Proposal；`confirmed` 或带完整修正文案的 `corrected` 才可进入 apply，其余保持 pending、unresolved 或 rejected。

Apply 前 runtime 必须再次验证：Patch 的 `subject`、`principal`、`purpose`、`source_revision`、Proposal action、证据引用、用户决定和当前 revision。父版本冲突、缺少具体批准、披露不匹配或包含非法 action 时拒绝，不自动合并或重试。Apply 后保留旧版本、审计记录和 Patch 状态；不能通过删除旧 Claim 伪造没有矛盾的历史。

## 5. 版本、冲突与撤回

View 的冻结内容、`source_revision`、`expires_at` 和权限在其生命周期内不变。Store 有更新时，提示用户旧 View 仍是旧版本，并在需要时重新编译新 View；不要在任务中途静默混用两个 revision。

Patch 的 `source_revision` 落后于当前 Store 时先停止 Apply，比较差异并重新校准。保留矛盾、counterevidence、unknown 和变化，不以“最新一句话”覆盖历史阶段。用户可拒绝 Proposal、限制某用途、退休逻辑上的 Claim，或对可控副本提出精确删除请求；原始来源和外部副本要单列其删除边界。
