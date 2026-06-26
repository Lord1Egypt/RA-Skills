# 工单产品参考

工单管理：查询待办、创建工单、流程操作（分派/接单/处理/确认/回访/转单/延期/作废/审批）。

## 核心概念

- **工单流程**：管理员在后台通过拖拽配置流程，定义工单经过哪些步骤。用户创建工单时自动关联流程，工单按流程步骤推进。
- **当前操作由状态决定，下一步由流程决定**：工单到了"处理中"，操作就是处理工单；到了"待分派"，操作就是分派工单。但处理/分派完之后进入哪个状态，由流程配置决定。
- **工单标识**：`id`（数字ID）+ `workOrderNumber`（GD开头编号，如 GD202605211706002993）
- **API 路径前缀**：`/workorder/master/`

## 工单状态与可用操作

| 状态码 | 状态名 | 可用操作 | 对应 Shortcut |
|--------|--------|---------|--------------|
| 0 | 已创建 | 受理 | `+accept` |
| 1 | 待分派 | 分派 | `+apportion` |
| 2 | 待接单 | 接单 | `+take` |
| 3 | 处理中 | 跟进、完成处理 | `+follow`、`+complete` |
| 4 | 待确认 | 确认 | `+confirm` |
| 5 | 待回访 | 回访 | `+visit` |
| 7 | 待审批 | 审批 | `+approve` |
| 10 | 已作废 | — | — |
| 11 | 待受理 | 受理 | `+accept` |

通用操作（任何状态可用）：转单 `+transfer`、申请延期 `+postpone`、作废 `+discard`

## Shortcuts

### +list — 我的待办工单列表 ✅

查询我的待办工单（当前还在我手上、等我处理的）。只读操作，可直接调用。

**状态值速查（`--work-order-status`）**：

| 数值 | 后端含义 | 用户可能这么说 |
|------|---------|----------------|
| （不传） | 全部待办 | "我的工单"、"我的待办"、"我有什么工单"、"待办列表"、"我手头的活" |
| `1` | 待分派 | "待我分派的"、"没派出去的"、"还没分配的"、"等我派单的" |
| `2` | 待接单 | "等我接的"、"派给我但还没接的"、"待我接单的"、"新派给我的" |
| `3` | 处理中 | "处理中的"、"我正在做的"、"在进行的"、"手头的"、"正干着的" |
| `4` | 待确认 | "等我确认的"、"待确认的"、"要确认的"、"等我验收的"、"做完待签的" |
| `5` | 待回访 | "待我回访的"、"要回访的"、"等回访的" |

**用户口语 → 命令示例**：
- 用户说"看下我的工单 / 我的待办" → `workorder +list`（不传 status）
- 用户说"我正在处理的工单" → `workorder +list --work-order-status 3`
- 用户说"等我确认的单子" → `workorder +list --work-order-status 4`
- 用户说"新派给我还没接的" → `workorder +list --work-order-status 2`
- 用户说"下一页 / 第 2 页" → `workorder +list --page 2`（如有上下文状态，继续带 status）

> 说明：`work_order_master.work_order_status` 字段全集还有 0=已创建、6=已完成、7=待审批、10=已作废、11=待受理 等。但**我的待办** tab 只覆盖 1-5（其他状态的工单不在我手上）。要查已完成/历史，用 `+handle-list`。

**参数**：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--work-order-status` | 否 | 待办状态: 1待分派 / 2待接单 / 3处理中 / 4待确认 / 5待回访。空=全部 |
| `--page` | 否 | 页码（默认 1） |
| `--page-size` | 否 | 每页条数（默认 10） |
| `--dry-run` | 否 | 只预览请求，不实际执行 |

> `topLevelId` 和 `assignees`（当前用户 ID）自动从登录 Token 中获取，无需手动传。

**返回值**：

```json
{
  "ok": true,
  "data": {
    "pagination": {
      "total": 2645,
      "pageNum": 1,
      "pageSize": 10,
      "shown": 10,
      "totalPages": 265,
      "hasMore": true
    },
    "rows": [
      {
        "id": 323407,
        "workOrderNumber": "GD202605211706002993",
        "workOrderContent": "2号楼南垃圾满溢",
        "workOrderStatus": "3",
        "workOrderStatusName": "处理中",
        "workOrderClassName": "秩序类",
        "headName": "张三",
        "deptName": "华融蓝海洋",
        "handleLevel": "0",
        "createTime": "2026-05-21 17:06:03",
        "expectCompleteDate": "2026-05-22 16:06:03",
        "isTimeOut": "0"
      }
    ]
  }
}
```

**向用户汇报时**：先报分页摘要（"共 2645 条待办，当前第 1 页，本页展示 10 条"），再列出工单详情。如有更多页，提示用户可以说"下一页"。

**关键字段**：

| 字段 | 说明 |
|------|------|
| `id` | 工单ID，后续操作工单时使用（如 `+info --id`） |
| `deptId` | 项目ID，查工单详情时需要（如 `+info --dept-id`） |
| `workOrderNumber` | 工单编号（GD开头），展示给用户时用 |
| `workOrderContent` | 工单内容 |
| `workOrderStatus` | 状态码 |
| `workOrderStatusName` | 状态中文名 |
| `headName` | 当前负责人 |
| `deptName` | 所属项目 |
| `workOrderClassName` | 工单类型 |
| `isTimeOut` | 是否超时：0否 1是 |

每条工单展示时提取 `workOrderNumber`、`workOrderContent`、`workOrderStatusName`、`headName`、`deptName`，用自然语言总结。

---

### +handle-list — 我经办的工单列表 ✅

查询我经办过的工单（含已完成历史）。`+list` 是当前还在我手上的待办，`+handle-list` 是我参与过的所有记录（历史快照表，含已完成、已转出的）。只读操作，可直接调用。

**经办分类速查（`--handle-status`）**：

| 数值 | 后端含义 | 用户可能这么说 |
|------|---------|----------------|
| （不传） | 全部经办 | "我经办的工单"、"我处理过的工单"、"历史工单"、"我做过的工单"、"我参与过的" |
| `0` | 我创建的 | "我创建的工单"、"我建的工单"、"我发起的工单"、"我报修的" |
| `1` | 我分派的 | "我分派过的工单"、"我派出去的单子"、"我派单的"、"我分配给别人的" |
| `2` | 我接单的 | "我接过的工单"、"我接单的"、"我领过的单子" |
| `3` | 我处理的 | "我处理过的工单"、"我做过处理的"、"我经手处理的"、"我干过的" |
| `4` | 我确认的 | "我确认过的工单"、"我验收过的"、"我签过的" |
| `5` | 我回访的 | "我回访过的工单"、"我做过回访的" |

**用户口语 → 命令示例**：
- 用户说"我经办的 / 我处理过的 / 历史工单" → `workorder +handle-list`（不传 status）
- 用户说"我创建的工单 / 我报修过的" → `workorder +handle-list --handle-status 0`
- 用户说"我分派出去的单子" → `workorder +handle-list --handle-status 1`
- 用户说"我接过的单子" → `workorder +handle-list --handle-status 2`
- 用户说"我做过的 / 我处理过的" → `workorder +handle-list --handle-status 3`
- 用户说"我确认过的 / 验收过的" → `workorder +handle-list --handle-status 4`
- 用户说"我回访过的" → `workorder +handle-list --handle-status 5`

> ⚠️ 同样的数字，`+list` 和 `+handle-list` 含义完全不同：
> - `+list --work-order-status 1` = 待分派的待办工单
> - `+handle-list --handle-status 1` = 我分派过的经办记录
> 不要搞混。

**参数**：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--handle-status` | 否 | 经办分类: 0我创建的 / 1我分派的 / 2我接单的 / 3我处理的 / 4我确认的 / 5我回访的。空=全部 |
| `--page` | 否 | 页码（默认 1） |
| `--page-size` | 否 | 每页条数（默认 10） |
| `--dry-run` | 否 | 只预览请求，不实际执行 |

> `headId` 和 `topLevelId` 自动从登录 Token 中获取，无需手动传。

返回结构与 `+list` 一致（`pagination` + `rows`），同样要先告诉用户分页摘要再列出工单。

---

### +create — 创建工单 🚧

创建工单。**写操作，调用前必须向用户确认。**

待实现。

---

### +info — 工单详情（含处理记录） ✅

查询工单详细信息，包含完整处理记录（创建、分派、接单、处理、确认、回访等全部流转历史）。只读操作，可直接调用。

**用户口语 → 命令示例**：
- 用户说"工单 323407 什么情况 / 看下这个工单" → `workorder +info --id 323407 --dept-id <从列表拿>`
- 用户说"GD20260521xxx 这个工单详情" → 先从 `+list` 找到对应 `id` 和 `deptId`，再 `workorder +info --id <id> --dept-id <deptId>`
- 用户说"这个工单谁处理的 / 处理记录" → `workorder +info --id <id> --dept-id <deptId>`

> ⚠️ `id` 和 `dept-id` 都是必填，来自 `+list` / `+handle-list` 返回的 `id` 和 `deptId` 字段。用户说工单编号（GD 开头）时，需要先查列表拿到 id。

**参数**：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--id` | 是 | 工单ID（数字，从列表命令的 `id` 字段获取） |
| `--dept-id` | 是 | 项目ID（数字，从列表命令的 `deptId` 字段获取） |
| `--dry-run` | 否 | 只预览请求，不实际执行 |

**返回值**：

```json
{
  "ok": true,
  "data": {
    "id": 323407,
    "workOrderNumber": "GD202605211706002993",
    "workOrderContent": "2号楼南垃圾满溢",
    "workOrderStatus": "3",
    "workOrderStatusName": "处理中",
    "workOrderClassName": "秩序类",
    "headName": "张三",
    "deptName": "华融蓝海洋",
    "createTime": "2026-05-21 17:06:03",
    "contactsName": "李四",
    "contactsPhone": "138****1234",
    "roomParkingName": "2号楼1单元501",
    "handleRecords": [
      {
        "handleType": "0",
        "handleTypeName": "创建工单",
        "handleHeadline": null,
        "handleDetail": "2号楼南垃圾满溢",
        "operateBy": "王五",
        "operateTime": "2026-05-21 17:06:03"
      },
      {
        "handleType": "1",
        "handleTypeName": "分派",
        "handleDetail": "分派给张三",
        "operateBy": "管理员",
        "operateTime": "2026-05-21 17:10:00"
      }
    ]
  }
}
```

**处理记录类型速查（`handleType`）**：

| 数值 | 含义 | 说明 |
|------|------|------|
| `0` | 创建工单 | 工单首次创建 |
| `1` | 分派 | 分派给处理人 |
| `2` | 接单 | 处理人接单 |
| `3` | 完成 | 完成处理 |
| `4` | 确认 | 确认工单 |
| `5` | 回访 | 回访工单 |
| `6` | 跟进 | 跟进处理进度 |
| `9` | 作废 | 作废工单 |
| `10` | 转单 | 转给其他人 |
| `11` | 申请延期 | 申请延期处理 |
| `15` | 审批 | 审批操作 |
| `16` | 受理 | 受理工单 |

> 其他较少见的类型：7=修改分类、8=修改房号、12=添加费用、13=交接、14=升级、17=码上办评价、18=码上办驳回、19=添加领料费用

**向用户汇报时**：先说工单当前状态（"工单 GD20260521xxx 当前状态：处理中，负责人：张三"），再按时间线简要叙述处理记录（"5/21 17:06 王五 创建了工单 → 17:10 管理员 分派给张三 → ..."），让用户一目了然工单流转过程。

---

### +search-user — 搜索用户 ✅

按姓名模糊搜索用户，用于分派、转单等操作时指定下一步处理人。只读操作，可直接调用。

**用户口语 → 命令示例**：
- 用户说"搜一下张三" / "找下管理员" → `workorder +search-user --nick-name 张三`

```bash
# 按姓名搜索
erp-cli --as <身份> workorder +search-user --nick-name 张三

# 搜索管理员
erp-cli --as <身份> workorder +search-user --nick-name 管理员
```

**参数**：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--nick-name` | 否 | 用户姓名（模糊搜索） |
| `--page` | 否 | 页码（默认 1） |
| `--page-size` | 否 | 每页条数（默认 10） |

**返回值**：

```json
{
  "total": 2,
  "rows": [
    {
      "userId": 317713,
      "nickName": "wjyAdmin",
      "userName": "wjyAdmin",
      "deptShortName": "客户测试",
      "roleNames": "研发测试管理员"
    }
  ]
}
```

**关键字段**：`userId` 和 `nickName` 用于后续 `+apportion` 的 `--assignees` 参数。

---

### code=204 通用流程（指定下一步处理人）

所有写操作（分派、接单、处理、确认等）都可能返回 `code=204`，表示流程下一步需要当前操作人指定处理人。这是 Activiti 工作流"上一步操作人指定用户"的模式。

**AI 处理流程**：

```
1. 调用写操作（如 +apportion），只传基础字段
2. 如果返回 {"action": "specify_handler", "processBusinessId": "xxx"}:
   a. 用 +search-user --nick-name <姓名> 搜索候选用户
   b. 把搜索结果给用户，让用户选（或用户直接说了名字）
   c. 重新调用同一写操作，加上 --process-business-id <返回的值> --assignees <userId:nickName>
3. 如果返回 {"action": "xxx_success"}，操作成功
```

**`--assignees` 格式**：`userId:nickName` 对，多人逗号分隔。例如：
- 单人：`--assignees 317713:wjyAdmin`
- 多人：`--assignees 317713:wjyAdmin,300156:admin2`

---

### +apportion — 分派工单 ✅

将待分派状态的工单分派给处理人。**写操作，调用前必须向用户确认。**

**⚠️ 前置条件（必须满足才能调用）**：
1. 工单状态必须是**待分派**（`workOrderStatus = "1"`）。其他状态调了后端也会报错"工单状态不为待分派，不能分派工单"
2. AI 在调用前必须先确认工单状态——如果是从 `+list` 拿到的，看 `workOrderStatus` 字段；如果用户只给了工单编号，先 `+info` 查状态
3. 如果用户要求分派一个非待分派状态的工单，告诉用户"该工单当前状态是 X，不是待分派，无法分派"

**用户口语 → 命令示例**：
- 用户说"把工单323292分派给张三" → 确认状态=1 → 先 `+search-user --nick-name 张三` 拿到 userId → `+apportion --id 323292 --dept-id ... --current-task-id ... --assignees userId:nickName`
- 用户说"分派这个工单" → 先 `+info` 确认状态=1 并拿 currentTaskId → 再 `+apportion`

> ⚠️ `--id`、`--dept-id`、`--current-task-id` 都是必填。前两个从 `+list` 或 `+info` 获取，`currentTaskId` 只能从 `+info` 获取。

```bash
# 首次分派（可能返回 204 需指定处理人）
erp-cli --as <身份> workorder +apportion --id 323292 --dept-id 402632 \
  --current-task-id 2056992848028372992 --work-order-class-id 300678 \
  --remark "请尽快处理"

# 如果返回 204，搜索用户后重新提交
erp-cli --as <身份> workorder +search-user --nick-name 张三
erp-cli --as <身份> workorder +apportion --id 323292 --dept-id 402632 \
  --current-task-id 2056992848028372992 \
  --process-business-id 301063 --assignees 317713:wjyAdmin
```

**参数**：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--id` | 是 | 工单ID |
| `--dept-id` | 是 | 项目ID |
| `--current-task-id` | 是 | 流程任务ID（从 `+info` 的 `currentTaskId` 获取） |
| `--work-order-class-id` | 否 | 工单分类ID（从 `+info` 获取，修改分类时传） |
| `--work-order-class-name` | 否 | 工单分类名称（从 `+info` 获取，写处理记录用，建议始终传） |
| `--remark` | 否 | 分派备注（执行前主动问用户是否需要填写，用户说不填则不传，不要自己编造） |
| `--process-business-id` | 条件必填 | code=204 时后端返回的流程业务ID，二次提交必填 |
| `--assignees` | 条件必填 | 指定处理人 `userId:nickName`，多人逗号分隔。首次可不传，如后端返回 204 则必须传 |
| `--dry-run` | 否 | 只预览请求，不实际执行 |

---

### 流程操作 Shortcuts 🚧

| Shortcut | 对应 API | 说明 |
|----------|----------|------|
| `+accept` | POST `/workorder/master/accept` | 受理工单 |
| `+apportion` | POST `/workorder/master/apportion` | 分派工单 |
| `+take` | POST `/workorder/master/takeOrders` | 接单 |
| `+follow` | POST `/workorder/master/follow` | 跟进工单 |
| `+complete` | POST `/workorder/master/dispose` | 完成处理 |
| `+confirm` | POST `/workorder/master/confirm` | 确认工单 |
| `+visit` | POST `/workorder/master/followUp` | 回访工单 |
| `+search-user` | GET `/workorder/user/list` | 搜索用户（分派/转单时指定处理人） |
| `+apportion` | POST `/workorder/master/apportion` | 分派工单 ✅ |
| `+transfer` | POST `/workorder/master/transferOrder` | 转单 |
| `+postpone` | POST `/workorder/master/postpone` | 申请延期 |
| `+discard` | POST `/workorder/master/discard` | 作废工单 |
| `+approve` | POST `/workorder/master/approve` | 审批工单 |

## 原始 API 调用

当 Shortcut 不满足需求时，直接调用 API：

```bash
# 工单总览（需总览权限，看全部工单）
erp-cli --as <身份> api POST /workorder/master/getAllList --data '{"pageNum":1,"pageSize":10}'

# 各状态数量统计
erp-cli --as <身份> api POST /workorder/master/myTaskCount --data '{}'

# 我提交的审批
erp-cli --as <身份> api POST /workorder/master/getCommitList --data '{"pageNum":1,"pageSize":10}'
```

## 权限表

| 方法 | 所需权限 |
|------|---------|
| +list | workorder:master:list |
| +handle-list | workorder:master:getHandleList |
| +info | workorder:master:query |
| +search-user | system:user:list |
| +apportion | workorder:master:apportion |
| +create | workorder:master:add |
| +accept | workorder:master:accept |
| +apportion | workorder:master:apportion |
| +take | workorder:master:takeOrders |
| +follow | workorder:master:follow |
| +complete | workorder:master:dispose |
| +confirm | workorder:master:confirm |
| +visit | workorder:master:followUp |
| +transfer | workorder:master:transferOrder |
| +postpone | workorder:master:postpone |
| +discard | workorder:master:discard |
| +approve | workorder:master:approve |