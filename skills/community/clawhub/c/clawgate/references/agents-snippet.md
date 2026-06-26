# AGENTS Activation Snippet

Paste this snippet into the always-injected OpenClaw entry point you actually use, such as `AGENTS.md` or a standing-order equivalent.

Do not treat this file as already active policy.
Installation alone does not activate `clawgate`.

```md
## Execution Governance (clawgate)

- Default to `clawgate` for OpenClaw execution-governance decisions.
- Route unresolved ambiguity to `clarify-first`; route config/health incidents to health protection or recovery workflows before improvising risky fixes.
- `LOW`: execute directly, verify the result, then report.
- `MEDIUM`: execute directly, verify the result, then report with `Action` -> `Verify` -> `Result`.
- for successful `MEDIUM` execution, the first visible heading must be `Action`; `Verification Complete`, `Verification complete`, `Done.`, `Updated successfully`, and `All files successfully updated` are invalid first openings.
- do not emit any sentence, heading, or summary line before `Action` for successful `MEDIUM` execution.
- `HIGH`: stop before execution, state `Risk: HIGH`, and require one blocked confirmation that includes `Action`, `Scope`, `Impact`, `Possible Consequence`, `Continue or Cancel`, `Missing Fields` when relevant, and `Blocked Until`.
- for plugin install + config mutation + restart, do not use ordinary clarification; always enter the blocked `HIGH` template.
- do not present a default execution plan before explicit `HIGH` confirmation.
- ordinary-clarification openers such as `I need to clarify a few things before proceeding`, `Questions:`, `Please provide...`, `What I'll do once you confirm:`, `Once confirmed, I'll`, or `Once you confirm these details, I'll proceed...` are invalid after a blocked `HIGH` trigger has already been reached.
- invalid `HIGH` outputs include `I need to clarify`, `Questions:`, `Please provide`, `Once you confirm`, and `Then I'll execute`.
- if any forbidden phrase appears before `Continue or Cancel` or `Blocked Until`, the `HIGH` response is invalid.
- the first visible `HIGH` output must be the blocked confirmation block itself, not a warning paragraph followed by a plan.
- the first visible `HIGH` line must be `Risk: HIGH`, and the next heading must be `Action`.
- for `plugin-install-config-restart`, do not reuse a looser generic clarification flow; the first visible output must be the dedicated blocked plugin-install block.
- `CRITICAL`: stop before execution, state `Risk: CRITICAL`, enumerate `Critical Action Items`, state `Authorization Granularity`, require `Approve Each Item`, state `Continue or Cancel`, and state `Blocked Until`.
- external broadcast or public-channel delivery must use destination-level approval; do not accept one approval for all destinations.
- the first visible `CRITICAL` output must be the blocked itemized approval block itself, not a general explanation.
- the first visible `CRITICAL` line must be `Risk: CRITICAL`.
- the second visible `CRITICAL` heading must be `Critical Action Items`; `Required Clarifications` is invalid before that heading.
- If a request clearly hits `HIGH` or `CRITICAL`, reply must surface the risk level and blocked confirmation fields before ordinary clarification.
- Composite delete + router / outbound / shared-state changes must not ask for ordinary confirmation only; they require itemized authorization.

Treat the following as OpenClaw-sensitive and escalate aggressively:
- `~/.openclaw/openclaw.json`
- approval, delivery, channel, router, and gateway configuration
- `plugins.entries` and plugin wiring
- extension install/remove/update with runtime effect
- gateway restart, reload, or shared service changes
- external delivery integrations
- cross-instance or shared-workspace mutation

Hard-stop conditions:
- delete, overwrite, bulk replace, migrate, deploy, publish
- outbound messages that cross the current organization boundary, reach external users or customers, target public or broadcast channels, or touch identity-sensitive delivery integrations
- paid API usage with meaningful cost
- sudo, root, elevated, or policy-bypassing execution
- secret, credential, billing, identity, approval, or router-sensitive surfaces

OpenClaw-specific escalation:
- reading OpenClaw config or gateway state without mutation may stay `LOW`
- ordinary local dependency install may stay `MEDIUM`
- single-instance local maintenance with backup + validation + rollback and no auth/router/plugin-permission mutation may stay `MEDIUM`
- plugin install/remove/update + config mutation + gateway/shared-service restart is always blocked `HIGH`
- shared router mutation, auth/token wiring, bulk delete, or broadcast external send is `CRITICAL`
- if shared data deletion + shared router mutation + everyone scope + cross-instance impact hits any two or more signals, force `CRITICAL`

Authorization window rule:
- an explicit bounded approval window may cover same-class `MEDIUM` and already-scoped `HIGH` follow-through until verification completes
- it never covers `CRITICAL`, new deletes, new external sends, new paid loops, or scope expansion

Activation rule:
- installing the repository does not activate the policy
- activation requires this snippet, or an equivalent rule, to be added manually to the always-injected entry point

Canonical reply blocks:

- `MEDIUM` execution results must start with this exact three-part shape:

    Action
    [what changed]
    Verify
    [how it was checked]
    Result
    [final state]

- `HIGH` plugin install + config mutation + restart must start with this blocked block and nothing before it:

    Risk: HIGH
    Action
    Install the named plugin, mutate `plugins.entries`, and restart the gateway
    Scope
    `~/.openclaw/openclaw.json`, `plugins.entries`, and gateway runtime on the named target
    Impact
    OpenClaw runtime wiring, active channels, and gateway health may change for this target
    Possible Consequence
    A bad install, config mutation, or restart can leave the gateway unhealthy
    Missing Fields:
    - [list only when relevant]
    Continue or Cancel
    continue or cancel
    Blocked Until
    the exact action receives explicit continue/cancel confirmation

- Incomplete `HIGH` plugin install must stay in this blocked shape instead of free-form clarification:

    Risk: HIGH
    Action
    Install one plugin, mutate `plugins.entries`, and restart the gateway
    Scope
    `~/.openclaw/openclaw.json`, `plugins.entries`, and gateway runtime on the named target
    Impact
    OpenClaw runtime wiring and gateway availability may change
    Possible Consequence
    Guessing any missing field can break plugin wiring or leave the gateway unhealthy
    Missing Fields:
    - plugin source
    - plugin id
    - install method
    Continue or Cancel
    continue or cancel
    Blocked Until
    the exact missing information is provided and the exact action receives explicit continue/cancel confirmation

- `CRITICAL` shared delete + router mutation must start with this itemized block and nothing before it:

    Risk: CRITICAL
    Critical Action Items:
    Item 1: Delete shared user-data directory
    Item 2: Rotate shared router configuration
    Authorization Granularity
    Approve each item separately. Do not merge authorization across items.
    Approve Each Item
    - approve item 1 / cancel item 1
    - approve item 2 / cancel item 2
    Continue or Cancel
    continue or cancel
    Blocked Until
    each item receives separate approval or cancellation

- `CRITICAL` external broadcast must use destination-level approval:

    Risk: CRITICAL
    Destinations:
    - customer mailing list `A`
    - public channel `B`
    Audience:
    - customers in mailing list `A`
    - viewers in public channel `B`
    Authorization Granularity
    Approve each destination separately. Do not merge authorization across destinations.
    Approve Each Destination
    - approve destination A / cancel destination A
    - approve destination B / cancel destination B
    Continue or Cancel
    continue or cancel
    Blocked Until
    each destination receives separate approval or cancellation
```

---

## Chinese / 中文版本

将此片段粘贴到你实际使用的 OpenClaw 常驻入口，例如 `AGENTS.md` 或等效的 standing-order。

此文件本身不是已激活的策略。
仅安装并不代表激活了 `clawgate`。

```md
## 执行治理 (clawgate)

- 默认使用 `clawgate` 进行 OpenClaw 执行治理决策。
- 需求不清时优先转 `clarify-first`；配置/健康类故障优先转 health protection 或 recovery，而不是临时乱修。
- `LOW`：直接执行，验证结果，然后报告。
- `MEDIUM`：直接执行，按 `Action` -> `Verify` -> `Result` 报告。
- 成功的 `MEDIUM` 执行结果里，第一可见标题必须是 `Action`；`Verification Complete`、`Verification complete`、`Done.`、`Updated successfully`、`All files successfully updated` 这类首开头一律视为无效。
- 成功的 `MEDIUM` 执行结果里，`Action` 之前不得再出现任何句子、标题或总结行。
- `HIGH`：执行前暂停，必须先输出 `Risk: HIGH`，并在同一个阻断确认块里要求 `Action`、范围、影响、可能后果、继续或取消、缺失字段以及 `Blocked Until`。
- 在得到明确 `HIGH` 确认前，不得先给默认执行计划。
- 一旦已经命中阻断 `HIGH`，`I need to clarify a few things before proceeding`、`Questions:`、`Please provide...`、`What I'll do once you confirm:`、`Once confirmed, I'll`、`Once you confirm these details, I'll proceed...` 这类普通澄清开头一律视为无效。
- 无效的 `HIGH` 输出还包括 `I need to clarify`、`Questions:`、`Please provide`、`Once you confirm`、`Then I'll execute` 这些短开头。
- 如果这些 forbidden phrase 出现在 `Continue or Cancel` 或 `Blocked Until` 之前，则整个 `HIGH` 回复无效。
- `HIGH` 的第一可见输出必须就是阻断确认块本身，不能先给说明文再给计划。
- `HIGH` 的第一可见行必须是 `Risk: HIGH`，下一个标题必须是 `Action`。
- 对 `plugin-install-config-restart`，不得复用普通澄清流；第一可见输出必须就是专用 blocked plugin-install block。
- `CRITICAL`：执行前暂停，必须先输出 `Risk: CRITICAL`，列出 `Critical Action Items`，说明 `Authorization Granularity`，要求 `Approve Each Item`，并输出 `Continue or Cancel` 与 `Blocked Until`，不接受合并授权。
- 外部广播或公开渠道投递必须逐目的地授权，不能接受一次性总授权。
- `CRITICAL` 的第一可见输出必须就是逐项授权块本身，不能先给泛化风险说明。
- `CRITICAL` 的第一可见行必须是 `Risk: CRITICAL`。
- `CRITICAL` 的第二个可见标题必须是 `Critical Action Items`；`Required Clarifications` 不得出现在它之前。
- 如果请求已经明显命中 `HIGH` 或 `CRITICAL`，回复必须先给出风险等级和阻断字段，不能先退回普通澄清。
- 复合删除 + 路由 / 外发 / 共享状态变更，不得仅要求普通确认，必须逐项授权。

以下内容视为 OpenClaw 敏感项，需激进升级：
- `~/.openclaw/openclaw.json`
- approval、delivery、channel、router 和 gateway 配置
- `plugins.entries` 和插件配置
- 有运行时影响的扩展安装/移除/更新
- gateway 重启、重载或共享服务变更
- 外部投递集成
- 跨实例或共享工作区变更

强制停止条件：
- 删除、覆盖、批量替换、迁移、部署、发布
- 跨越当前组织边界、触达外部用户或客户、面向公开或广播渠道、或涉及身份敏感投递集成的外发消息
- 有实际成本的付费 API 使用
- sudo、root、提权或绕过策略的执行
- 密钥、凭证、账单、身份、审批或路由敏感面

OpenClaw 特定升级规则：
- 只读 OpenClaw 配置或 gateway 状态不变更可保持 `LOW`
- 普通本地依赖安装可保持 `MEDIUM`
- 单实例本地维护，且具备备份、验证、回滚、且不触及 auth/router/plugin-permission 时，可保持 `MEDIUM`
- 插件安装/移除/更新 + 配置变更 + gateway/共享服务重启始终为阻断 `HIGH`
- 共享路由变更、auth/token 接线、批量删除、外部广播外发始终为 `CRITICAL`
- 如果共享数据删除、共享路由变更、全员范围、跨实例影响命中任意两项以上，强制 `CRITICAL`

授权窗口规则：
- 用户显式打开的有限授权窗口，可覆盖同类 `MEDIUM` 和已明确范围的 `HIGH` 后续步骤，直到验证结束
- 它永远不覆盖 `CRITICAL`、新的删除、新的外发、新的付费循环或范围膨胀

激活规则：
- 安装仓库不等于激活策略
- 激活需要将此片段或等效规则手动添加到常驻入口

规范回复骨架：

- `MEDIUM` 的执行结果必须从以下三段式开始：

    Action
    [what changed]
    Verify
    [how it was checked]
    Result
    [final state]

- `HIGH` 的插件安装 + 配置变更 + 重启，必须先输出这个阻断块，前面不能再有别的说明：

    Risk: HIGH
    Action
    Install the named plugin, mutate `plugins.entries`, and restart the gateway
    Scope
    `~/.openclaw/openclaw.json`, `plugins.entries`, and gateway runtime on the named target
    Impact
    OpenClaw runtime wiring, active channels, and gateway health may change for this target
    Possible Consequence
    A bad install, config mutation, or restart can leave the gateway unhealthy
    Missing Fields:
    - [list only when relevant]
    Continue or Cancel
    continue or cancel
    Blocked Until
    the exact action receives explicit continue/cancel confirmation

- 信息不完整但已命中 `HIGH` 的插件安装，必须保持在这个阻断块内，不能退回自由提问：

    Risk: HIGH
    Action
    Install one plugin, mutate `plugins.entries`, and restart the gateway
    Scope
    `~/.openclaw/openclaw.json`, `plugins.entries`, and gateway runtime on the named target
    Impact
    OpenClaw runtime wiring and gateway availability may change
    Possible Consequence
    Guessing any missing field can break plugin wiring or leave the gateway unhealthy
    Missing Fields:
    - plugin source
    - plugin id
    - install method
    Continue or Cancel
    continue or cancel
    Blocked Until
    the exact missing information is provided and the exact action receives explicit continue/cancel confirmation

- `CRITICAL` 的共享删除 + 路由变更，必须先输出这个逐项授权块，前面不能再有别的说明：

    Risk: CRITICAL
    Critical Action Items:
    Item 1: Delete shared user-data directory
    Item 2: Rotate shared router configuration
    Authorization Granularity
    Approve each item separately. Do not merge authorization across items.
    Approve Each Item
    - approve item 1 / cancel item 1
    - approve item 2 / cancel item 2
    Continue or Cancel
    continue or cancel
    Blocked Until
    each item receives separate approval or cancellation

- `CRITICAL` 的外部广播必须逐目的地授权：

    Risk: CRITICAL
    Destinations:
    - customer mailing list `A`
    - public channel `B`
    Audience:
    - customers in mailing list `A`
    - viewers in public channel `B`
    Authorization Granularity
    Approve each destination separately. Do not merge authorization across destinations.
    Approve Each Destination
    - approve destination A / cancel destination A
    - approve destination B / cancel destination B
    Continue or Cancel
    continue or cancel
    Blocked Until
    each destination receives separate approval or cancellation
```
