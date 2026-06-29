# Host Runtime Integration And Feedback Governance

## 中文

本 reference 用于把真实项目中的 Agent Loop / CMS 使用反馈，抽象回
Agent Loop Engineering 的流程、系统、Skill 和 reference，而不是自动改动正在开发
中的项目记录。

核心原则：

- 如果当前任务是“吸收反馈、升级 Skill/reference”，不要修改活跃项目的 `Docs/`
  状态文件。
- 只有当 Agent 明确承担该项目的 Controller / Developer / Acceptance 角色，并且
  当前 loop 要求它写项目状态时，才更新项目内 `Docs/`。
- Dogfooding 反馈应先分类，再决定进入 Skill/reference、项目代码、项目 `Docs/`
  或待人工确认。

## 1. 两层 CMS 必须分清

| 层级 | 存储 | 用途 | 典型写入者 |
| --- | --- | --- | --- |
| 开发过程 CMS | 项目 `Docs/` | 管理 AI coding 工作流、工单、验收、状态和交接 | Controller / Runner |
| 产品运行时 CMS | 产品自己的运行态存储，如 `.mywork/cms/{taskId}/` | 管理产品里某个用户任务的目标、状态、工具门禁和运行证据 | 产品 runtime adapter |
| Skill / Reference | Skill 仓库 | 沉淀跨项目可复用规则、接口、模板和方法论 | Skill maintainer |

不要把三者混成一层：

- 开发过程 CMS 判断“这个开发工作是否完成”。
- 产品运行时 CMS 判断“产品内这一轮用户任务是否应该继续、停止或门禁”。
- Skill/reference 判断“以后其他项目和其他 Agent 是否也应该遵守这条规则”。

## 2. 反馈先分类

当收到其他 Agent 的反馈时，先分类，不要直接执行：

| 分类 | 例子 | 默认处理 |
| --- | --- | --- |
| 项目代码问题 | 类型错误、测试失败、UI 未渲染 | 只有在当前任务是项目 Controller/Developer 时才改项目 |
| 项目状态问题 | `STATUS.md`、`LOOP_RUNS.jsonl`、`ACCEPTANCE.md` 不一致 | 只有在当前任务是该项目状态维护时才改项目 |
| Skill / 流程问题 | 角色边界不清、证据格式不清、Done 门禁不清 | 更新 Skill/reference |
| 宿主集成问题 | OpenCode、Cursor、Cline、WebBridge 接入点不一致 | 更新 host integration reference 或 adapter 规范 |
| Runner / 环境问题 | Bun 不在 PATH、workspace link 未生成、权限不足 | 更新 environment escalation / runner guidance；项目内只在承担项目角色时记录 |
| 人工决策问题 | 是否接受风险、是否改目标、是否安装系统依赖 | 停止并问人 |

判断句：

```text
I am updating the governance system, not acting as this project's Controller.
Therefore I must not modify the active project's Docs state.
```

## 3. 推荐宿主运行时接口

当一个产品或 coding host 要接入 Agent Loop Engineering，应提供稳定 runtime
adapter，而不是让每个宿主直接理解 store、taskId、gate、context。

推荐 API：

```ts
interface AgentLoopRuntime {
  enabled(): boolean
  ensureState(input): Promise<TaskLoopState>
  buildSystemContext(input): Promise<string | undefined>
  gateAction(input): Promise<OutputGateResult>
  recordRun(input): Promise<void>
}
```

推荐 hook：

| Hook | 时机 | 职责 |
| --- | --- | --- |
| `ensureState()` | 第一个有效用户主 loop | 创建或加载 task state |
| `buildSystemContext()` / `beforePrompt` | 模型 prompt 组装前 | 注入最小目标、验收、下一步、停止规则 |
| `gateAction()` / `beforeToolExecute` | 工具、浏览器、云调用、写操作前 | 判断 allow / warning / confirmation / block |
| `afterToolExecute()` | 工具执行后 | 记录结果摘要和证据引用 |
| `recordRun()` | loop 结束或重要状态转换时 | 追加机器可读运行记录 |

Privacy Gateway 不应只在工具执行后审计；它应在 `gateAction()` 前或内部成为输入的一部分。

## 4. 初始化边界

首轮初始化必须严格：

- 只有用户主 loop 的真实用户消息可以初始化 `target.userGoal`。
- 内部工具调用、后台任务、合成消息、测试 fixture 不应静默创建新 target。
- 长会话应区分：
  - stable user goal
  - current phase target
  - current subtask / work order

否则运行越久，target 会越来越粗，后续 gate 会失去方向约束。

## 5. 标准 evidence 分层

每轮反馈、review、handoff 应尽量使用四层证据：

| 字段 | 含义 |
| --- | --- |
| `code_refs` | 修改的代码文件、函数、模块 |
| `validation_refs` | 测试、类型检查、构建、手动运行、E2E、截图 |
| `doc_refs` | 更新的 CMS、review、acceptance、handoff、reference 文件 |
| `known_limits` | 未验证项、环境限制、跳过项、剩余风险 |

规则：

- “已实现”不是“已验证”。
- 类型检查通过不是完整 Done，除非 acceptance 明确只要求类型证据。
- 如果单测、路由测试、浏览器目视验证无法运行，应写 `Blocked` 或
  `Done with Risk`，不能写普通 `Done`。
- 证据必须写命令、结果、时间或证据路径；不要只写“测试通过”。

## 6. 回滚开关应标准化

所有产品运行时集成都应有零侵入回滚开关：

| 集成 | 示例 |
| --- | --- |
| CMS runtime | `MYWORK_CMS=0` |
| UI shell | `MYWORK_UI=0` / `VITE_MYWORK_UI=0` |
| Privacy layer | `MYWORK_PRIVACY=0` |
| WebBridge | `MYWORK_WEBBRIDGE=0` |

开关规则：

- 默认行为必须可解释。
- 关闭后应尽量回到宿主原行为。
- 关闭状态也应有可验证行为，例如 API 返回 disabled 或功能不渲染。

## 7. 何时更新项目 Docs，何时更新 Skill

| 当前任务 | 应更新 |
| --- | --- |
| 执行项目工单 | 项目 `Docs/` + 项目代码 |
| Controller review 项目交付 | 项目 `Docs/REVIEW.md`、`EVALUATION.md`、`PENDING.md` 等 |
| Workbuddy / Acceptance 验收 | 项目 `Docs/QA_ACCEPTANCE.md` 或等价验收文件 |
| 总结 dogfooding 经验 | Skill/reference，不直接改项目状态 |
| 改进 Agent Loop Engineering 方法论 | Skill/reference、templates、scripts |
| 准备发布 Skill | Skill 仓库、README、zip、listing |

如果用户说“参考这些反馈，更新 CMS / Skill / reference”，默认不要改正在开发项目的
`Docs/` 状态。只把反馈提炼到 Skill/reference。

## 8. English summary

Use this reference when feedback from a real project should improve the reusable
CMS / Agent Loop Engineering system.

Rules:

- Do not modify an active project's `Docs/` state when the task is to update the
  reusable skill or references.
- Separate development-process CMS, product runtime CMS, and reusable skill
  governance.
- Treat reusable CMS / Agent Loop rules as maintainer-owned. Ordinary project
  Developer, Controller, or Acceptance agents may propose rule changes, but must
  not edit the reusable rule layer unless explicitly assigned that maintainer
  role.
- For Developer loops, `WORK_ORDER.md` is the task authority. `TARGET.md`,
  `ACCEPTANCE.md`, `STATUS.md`, `NEXT_ACTIONS.md`, `LOOP_RUNS.jsonl`, and chat
  context must not expand the work order scope.
- Keep one current acceptance table per active work order. Duplicate AC IDs,
  raw feedback pasted into acceptance rows, and competing AC sections are
  `Invalid State`.
- Work orders that depend on local/cloud mode, providers, feature flags,
  unavailable devices/models, or waived checks must state the environment mode,
  authoritative config, waived reason, and mandatory validation before `Done`.
- Classify feedback before acting: project code issue, project state issue,
  skill/process issue, host integration issue, runner/environment issue, or
  human-decision issue.
- Prefer a host-neutral `AgentLoopRuntime` adapter with `ensureState`,
  `buildSystemContext`, `gateAction`, and `recordRun`.
- Evidence should be layered as `code_refs`, `validation_refs`, `doc_refs`, and
  `known_limits`.
- Missing tests, missing visual checks, or missing runtime verification should
  stop as `Blocked` or `Done with Risk`, not `Done`.
