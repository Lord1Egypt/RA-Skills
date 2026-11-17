---
name: brief-yourself
description: 通过有界访谈、来源授权和用户校准，建立并调用以 person 为主体的 Personal Context。用于认识自己、自我探索、更新个人画像，以及在求职、写作、演讲、协作或决策任务前生成冻结 Context View、任务后审核 Context Patch。区分 fact、self_report、observation 和 inference，保留反例与未知，并限制敏感内容披露。
---

# Brief Yourself 1.0.1｜Personal Context Layer

Brief Yourself 1.0.1 是当前产品、Skill 入口、Agent identity 和 active schema identity。当前 `schema_version` 为 `1.0.1`；历史 `0.4` 只保留在旧制品与历史说明中，不作为 active schema。

## 触发与定位

当用户想认识自己、让 Agent 更了解自己、复核近期变化，或希望在一个下游任务中使用经过校准的个人信息时使用本 Skill。

Brief Yourself 是由用户参与校准、按用途编译、可携带到不同 Agent harness 的 Personal Context Layer。Personal Context Store 是个人上下文的 canonical source；`Context View` 是给某次任务的冻结输入；`Context Patch` 是任务结束后交给用户审核的候选回流。

Codex Memory、rollout、项目文档和其他 harness memory 只能在明确授权后作为候选 evidence。它们不能自动导入、覆盖 Store、成为 `confirmed` Claim 或成为 canonical source。Brief Yourself 不复制 rollout、consolidation、retrieval、thread 或通用 memory 注入流程。

## 非目标与硬边界

- 不做通用历史库、向量检索、心理诊断或“真实人格”判定。
- 不把 Harness Memory 变成 Personal Context，也不做静默双向同步；`auto_import_harness_memory` 必须为 `false`。
- 1.0.1 当前版本只实现 `subject.type = person`。Organization Context 只通过共同 Envelope 预留隔离边界，不在本 Skill 中实现 Team Context Store。
- 不使用个人画像进行未经授权的就业、信贷、保险、医疗或其他高影响自动决策。
- 不读取真实 Personal Context、私密测试数据或历史资料，除非用户先完成本轮明确的来源授权。
- 个人信息写成陈述性 Claim，不写成会覆盖未来指令的命令；流程和操作规则属于 Skill 或项目文档。

## Session Contract：先约定，再探索

建立或更新画像时，先选择 `Depth`、`Evidence` 和 `Pace`。在第一个探索问题前，完整展示本次 Session Contract，并等待用户接受或调整；接受前不得索取经历、价值判断或其他探索内容。

Contract 至少说明：目标；Depth、Evidence、Pace；覆盖与排除维度；最多 prompts、用户回合和预计时长；准备读取的来源及范围；交付物；Personal Store 是否归档、下游是否可另存；暂停、跳过和删除路径。用户只说“开始”时采用推荐值。当前 Session 达到任一上限或停止条件即结束；继续探索必须建立新的 Contract。

| Depth | 最多 prompts | 用户回合 | 预计时长 |
|---|---:|---:|---:|
| Quick | 5 | 2–3 | 5–10 分钟 |
| Standard（默认） | 8 | 3–4 | 15–25 分钟 |
| Deep | 12 | 4–5 | 30–45 分钟 |

`History-assisted` 只是 Evidence modifier，必须继承所选 Depth 的全部上限，不能成为第四种深度或延长 Session。用户表示疲劳、询问还剩多少题、反馈过长，或已有材料足以形成最低充分画像时，立即停止新增问题并综合；不要为了完成脚本而继续追问。

## 运行流程

1. **确定操作。** 选择建立/更新画像、生成 Task View、审核 Patch，或 Inspect/Export；先说明本次用途和最低必要范围。
2. **取得读取授权（授权卡）。** 读取历史、项目文件、简历、公开资料或 Harness Memory 前，按 `references/source-consent-and-disclosure.md` 展示来源、范围、目的、外部传输、保存位置和删除方式，并等待明确授权。授权卡是读取前的同意界面，由该 reference 约束；它与 `register-source` 命令是两回事——`register-source` 是读取之后、经用户批准的长期来源登记入口。当前对话与用户主动提供的材料也要记录实际使用范围。
3. **按需取证。** 先用当前回答和用户主动提供的材料；历史只为已知缺口按需读取，不整批导入。来自 Harness Memory 的内容只形成候选 evidence，必须标为待校准，不能直接成为 confirmed Claim。
4. **访谈与校准。** 按 `references/interview-and-calibration.md` 控制预算；从具体经历、选择和行为开始，阶段性展示 Calibration Card，让用户确认、改写、拒绝或保留未决。
5. **形成扁平 Claim 候选。** Store 只有一个 `claims[]`；`domains[]` 是标签，不是物理层级。新认识默认是 `user_status: unreviewed` 的 Domain 候选，不因一次 Session 晋升到 Core。`Core Summary` 只能从已确认、仍有效且有跨场景支持的 Claim 派生，不单独存储。
6. **生成冻结 View。** 按用途、精确主体/执行者/受众和最小必要 Claim 编译 View；完整对象、`source_revision`、创建时间、TTL 和权限一起冻结。Store 后续变化不会静默改变现有 View。
7. **只暂存 Patch。** 任务新认识只生成 `pending` Patch，策略和一次性话术放入 `task_strategies_not_for_merge`。按 `references/context-view-and-patch.md` 逐项审核；只有用户明确批准具体 `patch_id` 和 Proposal 后，runtime 才能 apply。

## 证据与认识的最低规则

- `fact`、`self_report`、`observation`、`inference` 分开记录；不把推断改写成事实。
- 保留证据来源、counterevidence、适用范围、变化、矛盾（Tension）和 unknown；没有记录不等于没有发生。
- `Tension` 与 `Unknown` 仍是当前 canonical Store 的顶层实体，也可作为完整冻结对象进入 View；它们不是永久 session-only。当前 Patch schema/runtime 的 Proposal 仅支持 Claim 的 `add`、`update`、`challenge`、`retire`，没有 Tension/Unknown 的新增或更新入口。会话新发现只能作为“未持久化候选”交付并等待未来显式协议；不得静默写入 Store、伪装成 Claim、塞入 `task_strategies_not_for_merge`，或声称已长期保存。已有迁移/Store 中的 Tension/Unknown 保持可读并可按需入 View；未来写入口另需 schema/runtime/approval，本轮不实施。
- 不用 MBTI、DISC 或一次回答替代证据；不把一次任务进度、JD 关键词、临时策略或 Agent 操作偏好写入长期 Claim。
- 新认识先进入候选 Domain；Core 只作为派生摘要资格，不能由单次任务直接晋升。长期写回始终经过用户审核。
- `sensitivity` 描述内容敏感程度；`disclosure` 描述 audience、purpose 和下游持久化许可，二者不能互相替代。默认排除 `private` 与 `restricted`。
- `subject` 固定为 person。`team-agent` 或其他未获明确授权的执行者/受众默认拒绝；不得因“同一工作区”而推断个人授权。

## Runtime 命令

runtime 注册 17 个操作名：14 个正式 V0.4 操作按下方五组路由；2 个迁移命令只在迁移场景使用；`list` 是 `list-patches` 的兼容别名，不是独立能力。参数一律以 `--help` 为准，本入口不预设尚未核对的 flags。不要把这些命令用于真实 Store 的迁移或 dogfood，除非另有授权。详细参数与副作用见 `references/store-operations.md`。

### Store 生命周期

```bash
python scripts/context_store.py init --help
python scripts/context_store.py validate --store <store>
python scripts/context_store.py inspect --store <store>
python scripts/context_store.py derive-core-summary --help
```

`init` 建立新 Store；`validate` 全量校验、不静默修复；`inspect` 查看 revision、计数与待审 Patch；`derive-core-summary` 只从符合条件的已确认 Claim 派生非 canonical 摘要。

### Source 登记

```bash
python scripts/context_store.py register-source --help
```

`register-source` 是 Evidence Source 的唯一写入入口，`consent` 必须为 `explicit`。它**不是读取授权界面**：读取前的授权卡由 `references/source-consent-and-disclosure.md` 约束；只有用户已授权读取并批准长期登记后才运行本命令。

### View

```bash
python scripts/context_store.py create-view --help
python scripts/context_store.py validate-view --help
```

`create-view` 编译冻结 View，敏感范围与限制在这一步经 disclosure 和用户批准决定；`validate-view` 只做验证（过期、用途、敏感级别、权限结构），不修改也不创建任何限制。创建后不刷新。

### Patch

```bash
python scripts/context_store.py stage-patch --help
python scripts/context_store.py list-patches --help
python scripts/context_store.py apply-patch --help
python scripts/context_store.py reject-patch --help
```

`stage-patch` 只写 pending；`apply-patch` 必须同时具备具体 Patch 审核、`--approve` 与确认 actor；`reject-patch` 不改 Canonical Context。

### 导出与删除

```bash
python scripts/context_store.py export --help
python scripts/context_store.py purge-plan --help
python scripts/context_store.py purge --help
```

`export` 默认只导出 `public`。`purge` 是不可逆遗忘：先 `purge-plan` 预览拿 `--plan-token`，执行时还需 `--confirmed-by` 与 `--approve`；预览后 Store 有任何变化 token 即失效。本入口不提供绕过这些约束的可执行删除示例，完整边界见 `references/store-operations.md`。

### 历史迁移路由（仅迁移场景读取）

```bash
python scripts/context_store.py migrate-v02 --help
python scripts/context_store.py preview-migrate-v03 --help
```

这两个命令只服务 V0.2→V0.3 与 V0.3→1.0.1 的历史迁移，不属于常规任务能力；先读 `references/migration-v0.3-to-v1.0.1.md`，按其预览、审核、另存与回滚边界使用。`migrate-v02` 会改写传入路径，只能对用户创建的明确副本执行；V0.3→1.0.1 只允许只读预览。

### C File Adapter：只接收冻结 View

C 包的 `scripts/adapters/codex_file_adapter.py` 是单向 File Adapter。它只读取一个已经生成的冻结 View JSON，校验 Envelope、TTL、主体、用途、`allowed_use`，以及每条 included Claim 是否同时授权 `principal.id` 和 `audience[]` 中每个 recipient；失败时 fail-closed，不打印被拒绝的个人正文。它不读 Personal Context Store、Codex Memory、rollout 或网络资源，不写回 Store、Harness Memory 或任何长期 Context；可选输出也不能覆盖输入 View。

已按 C 的实际 `--help` 核对以下概念命令。`--expected-audience` 是调用方提供的可重复子集绑定（repeatable subset binding）：每个 expected `type:id` 都必须存在于冻结 `view.audience`，但调用方不必枚举全部 audience，因此它不是 audience equality/exhaustive assertion。这个调用方绑定不改变安全不变量：无论是否传入该参数，adapter 仍必须对每条 included Claim 检查 disclosure 是否同时覆盖 `principal.id`、View Envelope 中全部 audience recipient IDs，并检查 purpose；子集参数不能放宽 disclosure。`--purpose-approved` 仅表示本次具体 purpose 已获明确批准：

```bash
python scripts/adapters/codex_file_adapter.py --view <view.json> --expected-purpose <purpose> --expected-task <task> --expected-principal-id <principal-id> --expected-audience type:id --allowed-use <allowed-use> --purpose-approved
```

Adapter 输出是当前任务的 Markdown/JSON 适配结果，不是新的 Store、Memory 或回写凭据；任务结束仍只生成 pending Patch。Markdown 紧凑输出仍保留每条 Claim 的 `user_status`、`confidence`、`status`、适用 `scope`、`evidence_refs`、`counterevidence_refs` 和非空关键时间字段；它只展示来源 ID，不展开证据原文、notes 或 source raw。未审核 Claim 会明确显示为 `review=unreviewed` / `review=unresolved`，不会被压缩成无条件确定事实。Store 与 Adapter 共用 `scripts/view_validation.py` 的无 Store View 校验内核；各自只在此基础上增加 Store 来源引用或调用方绑定检查。

## References 路由

正式包只保留以下 7 份 reference，每份都从本入口可达；读取时机如下：

- `references/interview-and-calibration.md`：**访谈开始前读**。Session Contract、三档预算、Question Map、Calibration Card、疲劳停止和 Claim 分类。
- `references/source-consent-and-disclosure.md`：**任何读取历史/项目/简历/Harness Memory 之前读**。当前唯一的同意与披露事实源：授权卡、候选 evidence、敏感度、披露、person/team 隔离和高影响边界。授权卡属于这里，不属于 `register-source`。
- `references/context-view-and-patch.md`：**编译 View 或审核 Patch 时读**。当前版本 Context Envelope、完整冻结对象、TTL、披露匹配、Patch 暂存与批准。
- `references/harness-boundaries.md`：**涉及 Harness Memory 边界或 File Adapter 时读**。Harness Memory、Personal Context、Task Context 的边界，以及 File Adapter 的 envelope/disclosure 与 expected-audience 绑定规则。
- `references/personal-context-model.md`：**需要确认 Store 结构语义时读**。Personal Context Store 的顶层实体、证据模型、View/Patch 回流边界与版本语义。
- `references/store-operations.md`：**执行任何 runtime 命令前读**。全部 14 个 1.0.1 操作与 2 个迁移命令的参数、副作用、文件系统限制、purge 边界和恢复方式。
- `references/migration-v0.3-to-v1.0.1.md`：**仅在历史 V0.3→1.0.1 迁移场景读**。只读、metadata-only preview 与 no-chain 迁移路由；旧 `0.4` 仅作为历史输入与旧制品标识保留。

## Assets 路由

三份 1.0.1 模板与同名 schema 配对，构造或校验对应对象时读取：

- `assets/templates/personal-context-store-v1.0.1.json`：Store 结构基线，配合 `assets/schemas/personal-context-store-v1.0.1.schema.json`；`init` 后手工构造或校验 Store 时对照。
- `assets/templates/context-view-v1.0.1.json`：冻结 View 结构基线，配合 `assets/schemas/context-view-v1.0.1.schema.json`；编译或校验 View 时对照。
- `assets/templates/context-patch-v1.0.1.json`：Patch 结构基线，配合 `assets/schemas/context-patch-v1.0.1.schema.json`；暂存或审核 Patch 时对照。

历史 V0.3 模板与旧版 references 已迁出正式包，保存在项目 `archive/1.0.1-moved-out/`；旧 `0.4` 制品也只在 `releases/` 中保留，不是当前协议的一部分，不得放回发布 ZIP。

## 交付与结束语

根据操作交付 Human Brief、候选 Claim、Tension/Unknown、冻结 View 或 pending Patch，并列出来源范围、未覆盖项、敏感边界和下一次值得验证的问题。结束时明确：这是基于当前授权材料的、截至目前的工作画像；用户可以修正、限制使用、拒绝或删除任何一项。
