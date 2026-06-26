# 审批工作流 AI 自动生成规范

本文档用于指导 AI 根据用户描述生成可落地的审批工作流。它属于 `dimens-manager` 的工作流章节，不新增顶层 Skill。

## 1. 适用场景

当用户提出下面这类需求时，优先使用本文档：

| 用户表达 | 默认意图 |
| --- | --- |
| AI 自动生成审批工作流 | 生成审批流定义草案，并给出落地步骤 |
| 一键生成业务审批流程 | 从业务规则抽取触发条件、审批节点、分支和动作 |
| 请假 / 报销 / 采购 / 合同审批流程 | 按真实业务表单字段和角色生成审批链路 |
| 审批节点自动化处理 | 在人工审批节点前后补自动校验、通知、回写节点 |
| 把审批流程挂到项目里 | 补齐团队定义、项目挂载、系统视图与权限检查 |

如果用户说的是“生成一个审批系统”，这是系统级建设需求，应先路由到 `dimens-system-orchestrator`；如果用户说的是“生成审批工作流 / 审批流程 / 审批节点”，才进入本文档。

## 2. 执行前必须收集的信息

AI 生成审批工作流前，至少要明确下面信息：

| 信息 | 说明 | 缺失时默认处理 |
| --- | --- | --- |
| `teamId` | 团队隔离上下文 | 不能执行真实写入，只能生成方案和草案 |
| `projectId` | 项目创建上下文 | 允许直接创建项目内审批流；缺失时只能生成草案，不能落到项目路由 |
| 业务对象 | 例如请假单、报销单、采购单、合同 | 从用户描述抽取，没有则先问清 |
| 发起入口 | 通常是多维表格 `workflow` 字段 | 默认按表格字段发起和展示摘要 |
| 审批角色 | 直接主管、部门负责人、财务、法务、管理员等 | 缺失时使用角色占位，不写死用户 |
| 条件分支 | 金额、天数、风险等级、合同类型等 | 没有则生成直线审批链路 |
| 结束动作 | 通过、拒绝、撤回、超时、回写字段、通知 | 默认包含通过、拒绝、撤回三类 |

## 3. 生成结果分三层

AI 输出不能只给自然语言说明，必须按三层组织。

### 3.1 业务审批蓝图

蓝图用于让用户确认业务规则，至少包含：

- 触发条件
- 申请人输入字段
- 审批角色与顺序
- 条件分支
- 自动化动作
- 结束状态
- 异常路径

### 3.2 工作流图草案

草案用于落到 `flow_info.draft/data`，建议输出 JSON 对象，至少包含：

```json
{
  "pluginType": "approval",
  "nodes": [],
  "edges": [],
  "globalVariables": [],
  "meta": {
    "source": "dimens-manager",
    "scenario": "approval-generation"
  }
}
```

说明：

- `pluginType` 固定为 `approval`，避免生成全功能工作流节点。
- `nodes` 和 `edges` 必须稳定可读，节点 `id` 使用英文短名。
- `globalVariables` 只放跨节点共享的变量，不要把整张表字段全部塞进去。
- 如果只是文档草案，不要声称已经创建或发布了工作流。

### 3.3 项目落地计划

落地计划必须覆盖：

1. 如果有 `projectId`，优先直接调用项目内创建接口生成审批流。
2. 保存草稿并调试。
3. 发布工作流。
4. 验证项目内审批流是否可在当前项目中直接读取和执行。
5. 如果还存在团队级复用需求，再考虑团队安装实例或项目绑定。
6. `systemView` 设置为 `approval`。
7. 在表格里用 `workflow` 类型字段作为发起入口。
8. 验证审批实例、任务、候选人、动作日志和字段摘要回写。

## 4. 节点总表与配置清单

审批工作流生成时，先按“核心必备节点”和“按场景补充节点”拆开，不要把可选节点写成必备，也不要少掉拒绝路径。下面的配置名是**推荐写法**，如果后端实现字段名略有差异，必须以当前实现为准，但语义不能省。

### 4.1 核心必备节点

| 节点语义 | 是否必备 | 推荐 id 示例 | 必填配置 | 常见可选配置 | 少了会怎样 |
| --- | --- | --- | --- | --- | --- |
| 开始节点 | 必备 | `start` | `label`, `variables` | `triggerField`, `sourceSheetId` | 没有入口变量，后续审批节点拿不到申请单上下文 |
| 表单校验 | 必备 | `validate_request` | `label`, `rules` | `failMessage`, `haltOnFail` | 校验规则不完整时，草案一执行就容易报参数或规则错误 |
| 条件判断 | 按需，但审批分支常用 | `amount_branch` | `label`, `expression` 或 `rules` | 边标签 `通过/驳回/超过阈值/不超过阈值` | 分支条件不明确会导致连线方向和业务语义混乱 |
| 人工审批 | 大多数审批必备 | `manager_approval` | `label`, `assigneeStrategy`, `roleKey` 或 `candidateUserIds`, `actions` | `timeout`, `canTransfer`, `remarkRequired` | 没有审批人策略时，常见报错是“找不到审批人/候选人” |
| 多级审批 | 按需 | `finance_approval` | `label`, `assigneeStrategy`, `roleKey` 或 `candidateUserIds`, `actions` | `timeout`, `canTransfer`, `skipWhen` | 多级审批少了这一层，会把财务、法务、负责人等关键节点跳过去 |
| 通过终点 | 必备 | `approved_end` | `label`, `result` | `summary`, `notifyTemplate` | 没有通过终点，流程无法正常收口 |
| 拒绝终点 | 必备 | `rejected_end` | `label`, `result` | `reasonField`, `notifyTemplate` | 没有拒绝终点，拒绝路径会断掉，容易出现悬挂状态 |

### 4.2 按场景补充节点

| 节点语义 | 是否必备 | 推荐 id 示例 | 必填配置 | 常见可选配置 | 少了会怎样 |
| --- | --- | --- | --- | --- | --- |
| 通知节点 | 推荐 | `notify_result` | `label`, `recipients`, `template` 或 `message` | `trigger`, `notifyApplicant`, `notifyApprovers` | 没有通知配置时，审批结束后只能“默默结束” |
| 回写节点 | 推荐 | `sync_workflow_cell` | `label`, `action`, `targetField` 或 `mapping` | `summaryFields`, `writeMode` | 没有回写节点时，表格里的 `workflow` 摘要字段不会更新 |
| 自动归档 | 按需 | `auto_archive` | `label`, `action`, `targetStatus` | `archiveReason`, `writeBackFields` | 归档节点没配时，可能只改状态不沉淀结果 |
| 撤回终点 | 按需 | `withdraw_end` | `label`, `result` | `reasonField` | 用户要求“可撤回”但没给撤回终点时，撤回语义容易和拒绝混淆 |
| 超时终点 | 按需 | `timeout_end` | `label`, `result` | `timeoutMinutes`, `escalation` | 有超时要求却没收口时，容易只挂起不结束 |

### 4.3 节点配置原则

1. `node.id` 必须稳定、唯一，建议使用英文短名，不要用中文和空格。
2. 每个审批节点都必须明确“谁来处理”，优先用 `roleKey`、`candidateUserIds`、`candidateRoleIds` 这类策略，不要写死姓名。
3. 条件节点必须至少有两条出边，且边标签要能看出分支含义。
4. 通知、回写、归档类节点如果被使用，就必须填完整目标配置，不能只留空壳。
5. 终点必须能区分通过、拒绝、撤回、超时等不同结果，不要把所有结果都落到一个终点里。
6. 如果后端暂时没有独立的 `withdraw_end` 或 `timeout_end` 类型，不要硬编不存在的节点类型，改用“动作节点 + 终点节点”的组合表达语义。
7. 如果某个场景不需要通知、回写或归档，就不要为了“凑节点数”强行加节点。

## 5. 最小 JSON 模板

下面模板适合“普通金额审批”场景，AI 可按业务描述增删节点：

```json
{
  "pluginType": "approval",
  "nodes": [
    {
      "id": "start",
      "type": "start",
      "data": {
        "label": "提交申请",
        "variables": ["rowId", "applicantId", "amount", "reason"]
      }
    },
    {
      "id": "validate_request",
      "type": "condition",
      "data": {
        "label": "校验申请信息",
        "rules": [
          { "field": "amount", "operator": ">", "value": 0 },
          { "field": "reason", "operator": "notEmpty" }
        ]
      }
    },
    {
      "id": "manager_approval",
      "type": "approval",
      "data": {
        "label": "直属负责人审批",
        "assigneeStrategy": "role",
        "roleKey": "direct_manager",
        "actions": ["approve", "reject", "transfer"]
      }
    },
    {
      "id": "amount_branch",
      "type": "condition",
      "data": {
        "label": "金额是否超过 5000",
        "expression": "amount > 5000"
      }
    },
    {
      "id": "finance_approval",
      "type": "approval",
      "data": {
        "label": "财务复核",
        "assigneeStrategy": "role",
        "roleKey": "finance_reviewer",
        "actions": ["approve", "reject"]
      }
    },
    {
      "id": "sync_workflow_cell",
      "type": "action",
      "data": {
        "label": "回写审批摘要",
        "action": "syncWorkflowCell"
      }
    },
    {
      "id": "approved_end",
      "type": "end",
      "data": {
        "label": "审批通过"
      }
    },
    {
      "id": "rejected_end",
      "type": "end",
      "data": {
        "label": "审批拒绝"
      }
    }
  ],
  "edges": [
    { "id": "edge_start_validate", "source": "start", "target": "validate_request" },
    { "id": "edge_validate_manager", "source": "validate_request", "target": "manager_approval" },
    { "id": "edge_manager_amount", "source": "manager_approval", "target": "amount_branch", "label": "同意" },
    { "id": "edge_manager_reject", "source": "manager_approval", "target": "rejected_end", "label": "拒绝" },
    { "id": "edge_amount_finance", "source": "amount_branch", "target": "finance_approval", "label": "超过 5000" },
    { "id": "edge_amount_sync", "source": "amount_branch", "target": "sync_workflow_cell", "label": "不超过 5000" },
    { "id": "edge_finance_sync", "source": "finance_approval", "target": "sync_workflow_cell", "label": "同意" },
    { "id": "edge_finance_reject", "source": "finance_approval", "target": "rejected_end", "label": "拒绝" },
    { "id": "edge_sync_end", "source": "sync_workflow_cell", "target": "approved_end" }
  ],
  "globalVariables": [
    { "key": "rowId", "type": "string", "required": true },
    { "key": "applicantId", "type": "string", "required": true },
    { "key": "amount", "type": "number", "required": true },
    { "key": "reason", "type": "string", "required": true }
  ],
  "meta": {
    "source": "dimens-manager",
    "scenario": "approval-generation"
  }
}
```

## 6. 项目挂载规则

审批工作流要进入项目业务入口，不能只创建团队工作流定义。

必须检查：

- 工作流是否已发布。
- `usageType` 是否为 `approval`。
- 项目绑定关系是否存在。
- `systemView` 是否为 `approval`。
- 当前用户是否具备项目可见和审批操作权限。
- 表格是否已有 `workflow` 类型字段作为发起入口。

一句话规则：

**团队工作流负责定义，项目绑定负责入口，审批运行表负责真值，`workflow` 字段只负责发起和展示摘要。**

## 7. 当前 CLI 能力边界

当前 `dimens-cli` 已封装的是 `ai chat-completions` 等运行/调用入口；项目内审批流创建、更新、发布已经有独立服务端路由，但不等于 CLI 已完整封装。

因此 Skill 输出时必须区分：

| 输出内容 | 可以怎么说 |
| --- | --- |
| 生成审批工作流草案 | 可以直接输出 JSON 和落地步骤 |
| 调用 AI 辅助生成 | 可用 `dimens-cli ai chat-completions` 让模型产出草案 |
| 创建 / 更新 / 发布项目审批流 | 优先说明项目内路由 `/app/approval/:teamId/:projectId/workflow/create|update|publish`，并明确创建结果是项目归属，不是团队安装实例 |
| 团队工作流安装 / 跨项目绑定 | 说明仍需要看团队定义、项目挂载和绑定关系 |
| 验证运行结果 | 需要看审批实例、任务、候选人、日志、字段摘要和权限 |

## 8. 推荐 AI 提示语

```text
你是维表智联审批工作流生成助手。
请根据我的业务描述，输出三部分：
1. 业务审批蓝图
2. pluginType=approval 的工作流 JSON 草案，包含 nodes、edges、globalVariables、meta
3. 项目落地计划，覆盖项目内创建接口、发布、workflow 字段入口、权限和运行验证

业务描述：
{{用户业务描述}}

约束：
- 不要新增顶层 Skill
- 不要把审批画布等同于可执行审批工作流
- 不要声称 server-only 能力已被 CLI 完整封装
- 审批真值以后端审批实例表为准，表格 workflow 字段只展示摘要
```

## 8.1 项目内创建接口

当 `projectId` 已知时，优先输出下面这个创建请求，而不是只给团队级草案：

```http
POST /app/approval/:teamId/:projectId/workflow/create
```

请求体示例：

```json
{
  "name": "报销审批",
  "label": "expense_approval",
  "description": "5000 元以内直属负责人审批，超过 5000 元追加财务复核",
  "draft": {
    "nodes": [],
    "edges": []
  }
}
```

返回语义里需要特别关注：

- `ownerScope = project`：这是项目归属审批流。
- `usageType = approval`：这是审批类型，不是通用工作流。
- `projectId = 当前项目`：说明它已经落在目标项目中。
- `bindScope = unbound`：这是这个创建路径的正常语义，不代表创建失败。
- `isInstalledInstance = false`：说明它不是团队安装实例，而是项目内直接创建的审批流。

如果后续要更新、发布或分页读取，继续使用同一条项目路由。
```

## 9. 验证清单

生成审批工作流后，至少按下面清单检查：

- 节点是否存在唯一 `id`。
- 连线 `source/target` 是否都能指向已有节点。
- 是否至少有开始、人工审批、通过结束、拒绝结束四类节点。
- 条件分支是否有清晰的通过和异常路径。
- 审批人是否用角色、部门或人员策略表达，而不是写死姓名。
- 是否说明 `teamId/projectId/systemView=approval`。
- 是否说明 `workflow` 字段入口和摘要回写边界。
- 是否区分了 CLI 已封装能力与 server-only 能力。

### 9.1 更细的节点校验

- `start` 是否包含能串起整条审批链路的上下文变量。
- `validate_request` 是否把必填字段和失败处理写明。
- 每个审批节点是否都能定位到明确审批人策略。
- 条件节点是否至少有两条有意义的出边。
- 通知节点是否明确通知对象和触发时机。
- 回写节点是否明确写回字段或摘要目标。
- 拒绝路径是否直达 `rejected_end` 或拒绝终点链路。
- 通过路径是否直达 `approved_end` 或通过终点链路。
- 是否存在没有后继节点的“悬挂节点”。
- 是否存在重复 `id` 或指向不存在节点的边。

### 9.2 场景模板校验

- 请假模板至少要能覆盖单级审批和多天数升级两种情况。
- 报销模板至少要能覆盖金额阈值分支和财务复核。
- 采购模板至少要能覆盖金额分支和合规检查扩展位。
- 合同模板至少要能覆盖法务审批和拒绝通知。

## 10. 常见报错与修正

| 报错 / 异常 | 常见原因 | 修正方式 |
| --- | --- | --- |
| 只有开始和结束，没有审批节点 | 把审批流写成了普通动作流 | 补 `manager_approval`，必要时再补 `finance_approval` |
| 审批节点报“找不到审批人” | `assigneeStrategy`、`roleKey` 或候选人列表没配好 | 先明确使用角色、部门还是指定人员，再补对应配置 |
| 条件分支跑偏 | `expression`、`rules` 或边标签不清楚 | 让分支条件和边标签一一对应，避免一条边承载多个语义 |
| 拒绝后没有结束 | 只有通过终点，没有拒绝终点 | 必须补 `rejected_end`，并让拒绝边直接指向它 |
| 回写字段没有变化 | `sync_workflow_cell` 没写 `targetField` 或 `mapping` | 先确认要写回的表字段，再补映射 |
| 通知没发出去 | `recipients` 或 `template/message` 为空 | 先确认通知对象，再决定模板或消息内容 |
| 草案能看懂但运行时报错 | 节点 id 重复、边指向不存在节点、或用了未支持的节点类型 | 先查节点唯一性和边连通性，再对照当前实现收敛节点类型 |

## 11. 标准审批场景模板

下面四类模板是最常见的审批工作流场景。生成时不要从零发散，优先在这些模板上按业务字段做增删，这样最不容易漏掉节点和配置。

### 11.1 请假审批

适用场景：年假、事假、调休、病假、外出申请。

建议节点：

```text
start -> validate_request -> manager_approval -> approved_end
                             └-> rejected_end
```

建议补充条件：

- 请假天数大于阈值时，增加部门负责人审批。
- 病假、外出类可根据类型增加附件或证明材料校验。
- 超过某个天数时，增加财务或行政复核。

建议配置：

| 节点 | 必填配置 | 常用配置 |
| --- | --- | --- |
| `start` | `variables` | `triggerField`, `sourceSheetId` |
| `validate_request` | `rules` | `failMessage`, `haltOnFail` |
| `manager_approval` | `assigneeStrategy`, `roleKey`, `actions` | `timeout`, `canTransfer`, `remarkRequired` |
| `approved_end` | `result` | `summary` |
| `rejected_end` | `result` | `reasonField` |

### 11.2 报销审批

适用场景：差旅报销、办公报销、采购报销、业务招待。

建议节点：

```text
start -> validate_request -> amount_branch -> manager_approval -> approved_end
                                       ├-> finance_approval -> approved_end
                                       └-> rejected_end
```

建议补充条件：

- 金额低于阈值时只走直属负责人审批。
- 金额高于阈值时增加财务复核。
- 涉及票据或附件时必须加附件校验节点。

建议配置：

| 节点 | 必填配置 | 常用配置 |
| --- | --- | --- |
| `start` | `variables` | `triggerField`, `sourceSheetId` |
| `validate_request` | `rules` | `failMessage`, `haltOnFail` |
| `amount_branch` | `expression` 或 `rules` | `label` 分支说明 |
| `manager_approval` | `assigneeStrategy`, `roleKey`, `actions` | `timeout`, `canTransfer` |
| `finance_approval` | `assigneeStrategy`, `roleKey`, `actions` | `timeout`, `canTransfer`, `skipWhen` |
| `approved_end` | `result` | `summary`, `notifyTemplate` |
| `rejected_end` | `result` | `reasonField`, `notifyTemplate` |

### 11.3 采购审批

适用场景：物料采购、服务采购、固定资产采购、供应商比价。

建议节点：

```text
start -> validate_request -> amount_branch -> manager_approval -> finance_approval -> approved_end
                                     └-> rejected_end
```

建议补充条件：

- 金额超过阈值时，增加更高层级审批。
- 涉及供应商选择时，增加比价或合规检查节点。
- 固定资产类采购可增加资产编码或入账校验节点。

建议配置：

| 节点 | 必填配置 | 常用配置 |
| --- | --- | --- |
| `start` | `variables` | `triggerField`, `sourceSheetId` |
| `validate_request` | `rules` | `failMessage`, `haltOnFail` |
| `amount_branch` | `expression` | `label` 分支说明 |
| `manager_approval` | `assigneeStrategy`, `roleKey`, `actions` | `timeout`, `canTransfer` |
| `finance_approval` | `assigneeStrategy`, `roleKey`, `actions` | `timeout`, `canTransfer` |
| `approved_end` | `result` | `summary`, `writeBackFields` |
| `rejected_end` | `result` | `reasonField`, `notifyTemplate` |

### 11.4 合同审批

适用场景：销售合同、采购合同、服务合同、补充协议。

建议节点：

```text
start -> validate_request -> amount_branch -> manager_approval -> legal_approval -> approved_end
                                     └-> rejected_end
```

建议补充条件：

- 合同金额、期限、风险等级决定是否进入法务审批。
- 模板类合同可增加条款校验节点。
- 涉及对外签署时可增加通知或归档节点。

建议配置：

| 节点 | 必填配置 | 常用配置 |
| --- | --- | --- |
| `start` | `variables` | `triggerField`, `sourceSheetId` |
| `validate_request` | `rules` | `failMessage`, `haltOnFail` |
| `amount_branch` | `expression` | `label` 分支说明 |
| `manager_approval` | `assigneeStrategy`, `roleKey`, `actions` | `timeout`, `canTransfer` |
| `legal_approval` | `assigneeStrategy`, `roleKey`, `actions` | `timeout`, `canTransfer`, `remarkRequired` |
| `approved_end` | `result` | `summary`, `notifyTemplate`, `writeBackFields` |
| `rejected_end` | `result` | `reasonField`, `notifyTemplate` |

### 11.5 场景选择原则

1. 先确定申请类型，再选模板，不要先选节点再倒推业务。
2. 先确定是否需要金额分支，再决定是否引入 `amount_branch`。
3. 先确定是否需要多人审批，再决定是否加 `finance_approval`、`legal_approval` 或更高层级节点。
4. 先确定是否需要附件、票据、合同文本校验，再决定是否加校验节点。
5. 如果只是单级审批，不要强行塞入财务、法务或超时节点。
6. 如果业务明确要求“拒绝后通知申请人”，拒绝终点必须配通知动作，不要只写结束。
7. 如果业务要求“审批通过后回写表格”，通过终点前必须有回写节点或回写动作。
