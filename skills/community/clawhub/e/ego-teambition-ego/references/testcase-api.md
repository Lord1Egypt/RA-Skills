# Teambition testplan API（浏览器会话）

前缀 `https://www.teambition.com`。下面的路径由 `page.fetch` 在已登录的 teambition.com 页面里请求，自动带上浏览器会话。

Phase 1 是只读 GET。Phase 2a 只加下面写过的单条写路径（2026-11-04 沙箱抓包，`CAPTURED-from-UI` 且 `VERIFIED-via-session`）。没有出现在本文里的 POST / PUT / DELETE 都不要发。

本文件不记录个人目录或业务线路径。沙箱 id 只作文档示例，测试用 mock，不访问线上：

- projectId `6743cee04ca487d085597f8c`
- planId `6aeaa22dba3464a24b6c30d4`

契约原文见 `references/testcase-write-capture.md`。

## 端点

### 计划信息

```text
GET /testcase/api/v1/projects/{projectId}/testplans/{planId}
```

展示时读取 `result.name`、`result.statusName` 或 `result.status`、`result.testcaseCount`（数字或 `{ total }`）、`result.creator.name`。

### 用例分组

```text
GET /testcase/api/v1/projects/{projectId}/testplans/{planId}/groups
```

响应可能是数组，或对象上的 `result` / `groups`。空 `result` 时再看 `groups`。每个分组：`_id`、`name`、`resourceCount`（组内用例数）、`creator.name`、`pos`。

### 用例查询（v3，TQL + 分页）

```text
GET /testcase/api/v3/project/{projectId}/testcase/query
    ?tql=<urlencoded>&pageSize=100&needTestCaseResult=true&pageToken=<offset>
```

- `tql`：本技能只发送 `_testplanId = {planId}`，以及可选的 `AND groupId = {groupId}`。`uniqueId` 不能用于 TQL（返回 0 条）。单条查询在拉回的页里用 `uniqueId` 过滤。
- `pageToken`：偏移量（0、100、200…按 pageSize 递增），不是 opaque token。最后一页 `nextPageToken` 为空。
- `needTestCaseResult=true` 才返回每步执行结果（actual / resultStatus / 截图）。
- 响应：`{"result": [...], "nextPageToken": "100", "totalSize": 0}`。`totalSize` 不可信，以翻页耗尽为准。最多 30 页。

## 用例对象字段

| 字段 | 说明 |
|------|------|
| `title` | 用例标题 |
| `uniqueId` | 用例编号（计划内展示的编号） |
| `precondition` | 前置条件 |
| `steps[]` | `desc` 操作、`expected` 预期、`actual` 实际、`resultStatus`（passed/failed）、`actualPayload.urls` 执行截图。`actualPayload.urls` 为空时才看 `expectPayload.urls` |
| `isDone` | 执行完成 |
| `priority` | 0 紧急，1 高，2 中，3 低 |
| `executor.name` | 执行人 |
| `commongroup.name` | 所属分组名 |
| `caseType` | 例如 function |
| `_id` | 执行用例 id。set-status 和 archive 用它。`uniqueId` 不能放进写路径 |
| `_fromHubTestcaseId` | 项目用例库里的 usercase id。更新标题 / 前置 / 步骤时作为路径 id |
| `_flowstatusId` | 用例状态。名称用下面的 flow-statuses 查询，不要把沙箱 id 写死在代码里 |
| `_commongroupId` | 分组。创建时放进 body |
| `_scenariofieldconfigId` | 场景字段配置。创建时放进 body |
| `_testhubId` | 计划内执行用例上经常是 `null`。更新正文不要读这个字段，改走 `GET …/testhub` |
| `testplanName` | 所属计划名 |

## 辅助只读

### 项目用例库 id（更新正文之前）

```text
GET /testcase/api/v1/projects/{projectId}/testhub
```

单数 `testhub`。复数 `testhubs` 列表是 404，不要用。响应 `result._id` 是 `testhubId`。

### 用例状态 id（set-status 之前）

```text
GET /api/projects/{projectId}/taskflows?type=testcase
GET /api/taskflows/{taskflowId}/taskflowstatus
```

先取 `type=testcase` 的任务流 `_id`，再列状态。CLI：`testcase flow-statuses <projectId>`。沙箱「测试工作流」里曾见到：待评审、评审中、执行中、阻塞、已通过、未通过、废弃。这些 id 只属于那个项目，换项目必须重查。

## Phase 2a 写路径

四条都走浏览器会话。401 提示重新登录，**不重试**写请求，也不改去 Open API。

### 创建用例

```text
POST /testcase/api/v1/projects/{projectId}/testplans/{planId}/testcases
```

Body（与抓包对话框一致）：

| 字段 | 说明 |
|------|------|
| `title` | 必填 |
| `precondition` | 字符串，可空。UI 发过纯文本 |
| `steps` | `{ desc, expected }` 数组。新建不带步骤 `_id` |
| `priority` | 数字。未传时发送 `-1`（未设置）。也见过 `2` |
| `caseType` | 字符串或 `null`，例如 `function` |
| `customfields` | 发送 `[]` |
| `_executorId` | 成员 id 或 `null` |
| `_testplanId` / `_projectId` | 与路径相同 |
| `_testhubId` | 创建时发送 `null` |
| `_commongroupId` | 目标分组。`--group` 传入；否则若计划响应带 `_commongroupId` 或 `_rootCommongroupId` 就用它；再没有就报错，不猜分组 |
| `_scenariofieldconfigId` | `--scenario-field-config-id`，或计划上的同名字段，或本计划已有用例上的同名字段 |
| `involvers` / `involveMembers` / `involveTeams` / `involveGroups` | 发送空数组 |

响应包在 `{ result: case }`。要留下 `_id`、`uniqueId`、`_fromHubTestcaseId`。

下面这两条是 404，不要当成创建接口：`POST /testcase/api/v3/project/{projectId}/testcase/create`，`POST /api/v3/project/{projectId}/testcase/create`。

### 更新标题 / 前置 / 步骤

计划里的执行用例没有单独的「整包更新」接口。UI 把正文写到项目用例库，目标 id 是执行用例的 `_fromHubTestcaseId`，不是 `_id`，也不是 `uniqueId`。

```text
PUT /testcase/api/v1/projects/{projectId}/testhubs/{testhubId}/usercases/{usercaseId}/title
Body: { "title": string }

PUT /testcase/api/v1/projects/{projectId}/testhubs/{testhubId}/usercases/{usercaseId}/precondition
Body: { "precondition": string }

PUT /testcase/api/v1/projects/{projectId}/testhubs/{testhubId}/usercases/{usercaseId}/steps
Body: { "steps": [ { "_id": string, "desc": string, "expected": string, "expectPayload": null } ] }
```

`testhubId` 来自上面的单数 GET。`usercaseId` = `_fromHubTestcaseId`。步骤 PUT 会带上已有步骤的 `_id`（按传入顺序对齐；调用方自己写了 `_id` 则保留）。`expectPayload` 未传时发送 `null`。只传了哪几个字段，就只 PUT 哪几个。

响应 `{ result: usercase }`。库记录上 `_testhubId` 有值，`_testplanId` 和 `_flowstatusId` 在抓包里是 null。计划内用例随后能查询到新正文。

`PUT` 或 `DELETE` `/testcase/api/v1/projects/.../testplans/.../testcases/{id}` 是 404，不要用。

### 改流程状态

```text
PUT /testcase/api/v1/projects/{projectId}/testplans/{planId}/testcases/{testcaseId}/flowStatusId
Body: { "_flowStatusId": "<statusId>" }
```

路径上的 `testcaseId` 是执行用例 `_id`。Body 的键**带下划线** `_flowStatusId`。Open 文档里的 `flowStatusId`（没有下划线）不是这条浏览器路径。响应 `{ result: case }`，里面的状态字段是 `_flowstatusId`。

### 移到回收站

产品文案是「移到回收站」，不是物理删除。

```text
POST /api/testcases/{testcaseId}/archive
```

- 路径在 `/api/testcases/` 下，**不在** `/testcase/api/` 下。
- Body 为空（UI 发的是 null body）。
- `testcaseId` 是执行用例 `_id`。
- 响应含 `_id`、`_projectId`、`isArchived: true`。
- CLI 必须带 `--yes`。没有 `--yes` 时不发请求。

`DELETE …/testplans/.../testcases/{id}` 和 `DELETE …/testcases/{id}/delete` 是 404。

## 鉴权

这个模块只认 teambition.com 的登录会话。读和 Phase 2a 写都不用 `teambition_cli` 或 MCP 的 Open API token（open.teambition.com）。Open 上的 create / flowStatus 文档**不能**当成这些浏览器路径的等价物。

本技能不导出 Cookie，也不接受用户粘贴的会话。401 时让人在 Ego Lite 打开 https://www.teambition.com/ 登录，然后重跑 `check-login`。

## 和任务数据的区别

任务搜索命中的是任务卡片。测试计划里的用例是另一套数据。不要用任务接口回答「这条用例的步骤是什么」。
