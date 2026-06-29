---
name: aios-call-app-service
description: 当请求依赖 AIOS、OpenClaw、Forguncy 等业务系统的实时数据、接口调用或业务操作时，优先使用本技能。先读取 AIOS_ONTOLOGY_DIR 指向的本体目录，再确认应用、命令、参数结构和枚举映射，通过 aios-apps-invoke-cli 发起调用，并以实时返回结果作为后续分析和执行依据。遇到 aios-mqtt-channel 会话时，把当前会话的 SessionId 视为唯一合法会话标识；它来自当前会话上下文中的 `sessionId`。
---

# 系统调用技能

当用户的问题不能只靠通用知识回答，而是必须查询、调用或操作业务系统时，应优先使用本技能。

## 优先触发场景

- 查询业务系统中的实时数据
- 调用系统接口
- 在系统内执行新增、修改、提交、审核、删除等动作
- 需要基于真实系统返回结果继续分析或决策

## 必须遵循的流程

1. 在发起调用前，先读取环境变量 `AIOS_ONTOLOGY_DIR` 指向的本体目录。
  - 禁止缓存、记忆或复用之前读取的本体内容。
  - 每次调用都要重新读取，确保使用最新的本体信息。
2. 以本体为以下信息的唯一事实来源：
  - 应用名
  - 命令名或绑定端点
  - HTTP 方法
  - 请求体结构
  - 枚举值映射
  - 返回字段含义
3. 只允许通过 `aios-apps-invoke-cli` 调用业务系统接口；CLI 会通过本地 app invoke socket service 完成真实调用。
4. 实时调用结果的优先级高于记忆、缓存、历史对话和猜测。
5. 只有在拿到 CLI 返回结果后，才能继续做后续分析、汇总和结论输出。

## 最小执行清单

每次调用前按这个顺序检查：

1. 读取相关 ontology 文档。
2. 根据文档，确认本次是 `servercommand` 还是 `binding`。
3. 根据文档，确认 `applicationName`。
4. 根据文档，确认 `commandName`。
5. 根据文档，确认 `provider`。
6. 通过会话上下文的 `topic_id` ，确认 `SessionId`。
7. 生成 `jsonBody`，并检查确认合法性。
8. 如果涉及到创建、修改、提交、审核、删除等动作，必须整理出包括每个参数、值和说明的表格，请用户确认后，方可执行。查询类动作需忽略这一步。
9. 生成并执行唯一一条 CLI 命令。

任一步缺失，都停止并说明缺口。

## 会话标识读取规则

- `aios-apps-invoke-cli` 的 `-s` 参数，只接受当前会话上下文中的 `topic_id`。
- `topic_id` 以 `s-` 开头，后面跟30个数字，不要忽略开头的 `s-`。
- 如果当前上下文没有 `topic_id`，就视为运行时缺参，必须停止调用并明确说明缺口。

## 约束要求

- `AIOS_ONTOLOGY_DIR` （默认为 `/var/aios/kernel/ontology`）视为当前事实源。
- 当前 CLI 只支持 `provider=hzg`，如果出现其他 provider，直接说明当前运行链路不支持，不要猜测替代方案。
- 调用 CLI 时，`-s` 传入当前会话的 `topic_id` 。
  - 不能臆造，不能复用其他会话的 `topic_id` 。
  - 不得使用提示词中的 `SessionId` 、 `topic_id` 、`chat_id` 、 `message_id` 或其他字段代替。
- 不要臆造接口名、请求字段、枚举 ID 或 `provider`。
- 不要绕过 CLI 自行编写 API 调用脚本。
- 不要手动启动 `aios-apps-invoke-cli serve` ；运行环境应已提供常驻 app invoke service。
- 只有拿到 CLI 结果后，才允许用 Python 做二次分析和计算。
- 如果本体不完整、`provider` 未知或运行时上下文缺失，应明确说明阻塞点，不要猜测。
- 禁止将调用结果存储到记忆、缓存或数据库中；禁止在后续对话中复用之前的调用结果。

## 降歧义规则

- `binding` 一律使用规范命令名，不用别名：
  - `GetTableDataWithOffset`
  - `GetComboBindingOptions`
  - `CalcBindingDataSource`
- `servercommand` 的 `jsonBody` 严格按 ontology 的 `Input Arguments` 生成。
- `binding` 的 `jsonBody` 严格按 [references/invoke-rules.md](references/invoke-rules.md) 中的兼容 schema 生成。
- 不要把底层 HTTP 原始 body 直接塞进 `binding` 的 `jsonBody`，除非规则文件明确允许。
- 同一个问题里如果存在多个可疑 ontology 条目，先说明候选项并停止，不要自选一个继续调用。

## 开始前必须阅读

- 调用前需要阅读：[references/invoke-rules.md](references/invoke-rules.md)
- 调用后，需要做筛选、聚合、比较、排序或时间分析时，再阅读： [references/data-processing.md](references/data-processing.md)

## 输出要求

- 说明本次调用依据了哪些本体文件或条目。
- 说明使用的是 `servercommand` 还是 `binding`。
- 说明任何假设、缺失字段、跳过的数据或不确定性。
