# Harness Memory、Personal Context 与 Task Context 边界

本文件说明 Brief Yourself 1.0.1 的适配边界。它是协议说明，不是平台指令，也不授权读取用户的历史、私密 Store 或任何 Harness Memory。

## 三类上下文

| 类型 | 作用 | canonical source | 本适配器的行为 |
| --- | --- | --- | --- |
| Harness Memory | 保存 Agent 的执行偏好、项目地图、程序性经验和运行历史摘要 | 对应 Agent harness | 不读取、不写入、不自动同步 |
| Personal Context | 用户审核或待审核的个人事实、自述、观察、推断、张力与未知 | Personal Context Store | 由用户选择用途、受众和有效期后生成冻结 View |
| Task Context | 某次任务的最小、冻结、purpose-bound 输入 | 当前 Context View | File Adapter 只读取一次并渲染；任务结束只产生待审核 Patch |

Personal Context 不是第二套通用 Memory OS。Harness Memory 也不是 Personal Context 的事实源。即使两边谈论相似内容，来源、用户状态、证据、敏感度、披露权限和回流路径仍然分开。

## Memory 只能作为候选

Codex Memory、rollout、thread 摘要、项目规则或其他 harness 记忆若被用户明确授权读取，只能作为候选证据：

- 不自动 import 到 Personal Context Store；
- 不自动 export 到 Harness Memory；
- 不把候选直接标成 `confirmed` Claim，也不直接晋升 Core Summary；
- 需要用户审核、来源引用和适用边界后，才可通过唯一回流路径 `Context Patch` 进入长期 Context。

File Adapter 因此不接触 Memory API、rollout、`MEMORY.md`、Personal Store 或 App Server。它只接受一份已生成且冻结的 1.0.1 Context View。关闭 Harness Memory 时，仍可从本地 View 生成同样的 Markdown 或 JSON；适配器不依赖 Memory 是否启用。

## File Adapter 是第一阶段集成

Brief Yourself 1.0.1 采用可审计的单向 File Adapter：

```text
冻结 Context View --validate/disclose--> 独立 Markdown 或 JSON 文件/stdout
                                           |
                                           +--> 目标 Agent 的任务输入
目标 Agent 任务结果 -----------------------> 待审核 Context Patch
```

适配器必须保留 `view_id`、`source_revision`、`expires_at`、`permission` 和 Claim/Tension/Unknown ID。target（`generic`、`codex`、`deepseek`、`hermes`）只改变外层提示标签，不改变 payload 语义。它不得覆盖输入 View，或将结果回写 Store/Memory。

Markdown 只渲染任务所需的 Envelope、Claim/Tension/Unknown 白名单字段和 ID；不渲染 evidence source 原文、source locator 或 Claim `notes`。它明确声明“这是任务上下文，不是系统指令”，不能覆盖 platform 或 user 的当前指令。JSON 可以包装 View 的深拷贝，但不得删去权限、有效期、revision 或 provenance 字段。

## Envelope 与披露边界

View 的共同 Envelope 是：

```text
subject + principal + audience + purpose + task
        + source_revision + expires_at + permission
```

适配器在输出前 fail-closed 检查：

1. active schema identity `schema_version=1.0.1`、主体为 `person`、principal 在 audience 中，purpose/task、revision、时间戳和三项 permission 均完整有效；过期 View 拒绝。
2. 每条 Claim 都是完整对象；`disclosure.audiences` 必须逐字包含 `principal.id`，并逐字包含每个 `view.audience[].id`。不把 `self-agent`、`team-agent`、`public` 或 `*` 当作宽泛角色/通配授权；若 ID 取名为 `self-agent`，也只能匹配这个 exact ID。Team 共享必须使用冻结 schema 允许的 exact ID，而不是角色猜测。
3. `--expected-audience type:id` 是调用方提供的可重复子集绑定：每个 expected 值必须存在于冻结 `view.audience`，调用方不必枚举全部 audience，因此它不是 audience equality/exhaustive assertion。它只验证调用方期望的子集，不改变第 2 条的完整 Envelope disclosure 检查；不能借此减少 required recipient IDs 或放宽 fail-closed 行为。
4. `user-approved` 不是隐式通行证。因为当前 Envelope 未冻结 `purpose_approved` 字段，只有 CLI 的显式 `--purpose-approved` invocation 信号可以接受该 purpose token；此信号写进 JSON adapter metadata，不改写原 View。
5. `private` / `restricted` 内容不得靠适配器猜测授权。缺少 disclosure、exact ID 集合或 purpose 不匹配、被 View exclusions 排除、或 View 权限试图扩大下游持久化范围时，整份 View 拒绝。
6. Team Agent 默认拒绝 Personal Context；只有 View 和 Claim 都列出同一组 exact audience IDs，才可能编译。示例中的 `team-agent:team-blue` 只能作为实际冻结 ID 的逐字值，不能被解释成 `team-agent` 角色通配符。

“public” 是内容敏感度，不等于可以跳过 Envelope；平台规则、user 当前指令和组织边界始终优先于 Task Context。

## Personal 与 Organization Context

1.0.1 当前版本只实现 `subject.type=person`。未来 Organization Context 可以复用 `subject/principal/audience/purpose/revision/permission/expiry` 这组 Envelope，但必须拥有独立 Store、所有权和权限模型。本门不实施组织产品，也不把团队政策写进 Personal Context。

对 Team Agent 的默认策略是拒绝个人 Claim，而不是由 adapter 猜测“这个团队可能认识谁”。若未来要允许共享，必须在生成 View 时显式声明同一组 exact audience IDs、目的、权限和 TTL，并保留可审计的来源。

## 操作偏好与个人价值

只做明确路由，不做隐式写入：

- `operational-preference`（例如某工作区的格式偏好）路由为 `harness-memory-candidate`，仍需对应 harness 的独立审核流程；
- `personal-value`（例如用户确认的价值判断）路由为 `personal-context`，必须通过 Personal Context 的 Claim/Patch 审核流程；
- 无法明确分类时路由为 `manual-review`。

这只是路由函数和文档规则；File Adapter 不写入任何 Memory，也不替用户确认新的长期 Claim。
