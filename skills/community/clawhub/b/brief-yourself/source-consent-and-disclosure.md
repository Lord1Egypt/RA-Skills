# Source Consent And Disclosure｜Brief Yourself 1.0.1

本文件规定“是否可以读取”和“读到以后可以向谁、为何使用”两道不同的门。可访问不等于已授权；内容敏感也不等于披露许可。

## 1. 读取前的授权卡

读取历史对话、项目目录、简历、公开主页、第三方材料、Codex Memory、rollout 或其他 harness memory 之前，先向用户展示一张授权卡，至少包含：

```text
来源：<具体来源名称、类型和安全 ID>
范围：<目录/会话/时间段/文件或记录类型；明确排除项>
目的：<本轮要回答的具体问题或任务>
外部传输：<不传输，或服务/处理方、传输哪些字段>
保存位置：<仅当前会话、可复制结果，或 Personal Context Store 的具体位置>
删除方式：<可删除哪些本地副本、如何撤回授权、哪些原始/外部副本不受控制>
授权：<请明确同意上述来源、范围、目的和保存边界>
```

只有用户明确同意后才能读取。授权是针对列出的来源、范围和目的；新来源、扩展范围、新的外部服务或新的用途都要重新说明并重新取得同意。用户只说“开始”不能替代一张尚未展示的授权卡。

当前对话和用户主动贴出的材料可以先使用，但仍应说明实际使用范围、是否形成来源记录，以及是否会产生持久化或下游副本。不要为了“了解更多”扫描全部历史。

## 2. Source 记录与最小化

只登记实际读取过的来源。Source 至少保留 `id`、类型、标题、定位、实际 `access_scope`、带时区的 `collected_at`、`consent: explicit`、保留方式和 `sensitivity`。原始材料留在用户管理的位置；Store 只保存可复用的短摘要和可定位的 `evidence_refs`，不复制无关敏感原文。

用户可以限制领域、时间范围、文件类型、单个 Claim 或某一段内容。无法访问的来源要明确列为未覆盖，不能凭空补全；没有记录也不等于没有发生。

## 3. Harness Memory 只能作为候选 evidence

Codex Memory、`MEMORY.md`、`memory_summary.md`、rollout summaries、consolidation 产物和其他 harness memory 与 Personal Context Store 分开：

- 读取前仍需要上面的来源、范围、目的、外部传输、保存位置和删除说明；
- 只在用户授权的范围内按需读取，不整批检索或导入；
- 读到的个人偏好、事实或 Agent 推断只能成为候选 evidence，标为待校准的 `self_report`、`observation` 或 `inference`，不能直接设为 `confirmed`；
- 不自动写入 Store、覆盖已有 Claim、成为 canonical source，也不自动镜像回 Harness Memory；`auto_import_harness_memory` 固定为 `false`；
- 历史观察必须保留来源和反例，并由用户确认、改写、拒绝或保留未决后，才可进入 pending Patch。

关闭 Harness Memory 时，Personal Context 仍应能独立生成 View；Brief Yourself 不负责复制 rollout、consolidation 或通用 retrieval。

## 4. Sensitivity 与 Disclosure 分离

`sensitivity` 描述内容本身的敏感程度：`public`、`private`、`restricted`。`disclosure` 描述使用条件：允许的 `audiences`、允许的 `purposes`，以及 `allow_downstream_persistence`。一项不能推导另一项：公开材料也可能只允许本轮使用，private 内容也不能因“已在本地”自动流向下游。

默认 View 排除 `private` 和 `restricted`，并且默认不允许下游持久化。需要加入某条 private Claim 时，要在当前目的下逐项说明并取得明确许可；restricted 内容需要更高的逐项确认，不能通过批量的“了解我”授权。任何敏感级别过滤失败都应拒绝编译，而不是降级为模糊摘要。

披露匹配必须同时满足：

1. `subject.type` 为 `person` 且主体 ID 与 Store 一致；
2. 对每一条 included Claim，`disclosure.audiences` 必须同时精确授权 `principal.id`，以及 Envelope `audience[]` 中每个实体的 `id`（推荐使用 `type:id` 形式）；只授权 principal 而遗漏任一 recipient 时，拒绝编译，不能把 principal 的许可传递给 audience；
3. 请求目的与 `disclosure.purposes` 中的目的精确匹配；
4. `allow_downstream_persistence` 只有在用户明确允许保存副本时才为 `true`。

`user-approved` 是需要用户确认的目的标记，不是通配符。若 Claim 只写 `purposes: ["user-approved"]`，仍必须在披露前向用户展示本次具体目的并取得明确的 purpose approval；不能把它解释成允许所有未来用途。

## 5. Person / Team Agent 隔离

1.0.1 当前版本只实现 `subject.type = person`。个人主体、执行者和受众都必须出现在 Context Envelope 中：`subject`、`principal`、`audience`、`purpose`、版本和 TTL 缺一不可。

`team-agent`、组织主体、共享频道或未识别的 principal/audience 默认拒绝个人 Context。`self-agent` 只表示个人执行者的候选角色，不能流向 `team-agent` 或任何未在 `audience[]` 中逐一获授权的其他 recipient；默认 self-agent disclosure 不得被扩大解释。当前版本没有 Team Agent 的自动放行路径；即使用户与 Agent 同属一个项目，也不能推断 team disclosure。未来若新增组织协议，必须使用独立 Store 和独立授权，不得改写本 Skill 的 person 默认拒绝。

## 6. 高影响用途与外部服务

不得用 Personal Context 对就业录用、信贷、保险、医疗、住房、福利或其他高影响事项做未经授权的自动决定、排序、拒绝或风险评分。若任务看似只是“给建议”但实际会替代人的高影响判断，停止生成并要求人工复核与明确授权。

外部服务只在授权卡中明确列出后调用。最小化传输字段；未获允许时仅在本地会话中处理。结果若包含个人 Claim，默认回到 pending Patch，不直接写外部 memory、第三方数据库或 Personal Context Store。

## 7. 保存、撤回与删除

在任何持久化前说明具体保存位置、版本和预计保留时间。优先使用用户可查看、编辑和删除的本地 Store；View 默认 TTL 为 7 天，过期后不能作为默认上下文。`archive_in_personal_store` 与 `allow_downstream_persistence` 分开询问。

用户可以撤回授权、限制用途、拒绝 Claim、退休逻辑上的认识或请求删除可控副本。删除说明必须区分 Personal Context Store、View/Patch 副本、原始来源系统和外部服务：不能控制的副本要明确其限制，不能声称已经删除。未经用户批准不得 apply Patch，也不得因撤回而静默重写原始来源。
