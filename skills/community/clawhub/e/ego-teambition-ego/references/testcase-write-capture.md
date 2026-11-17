# Phase 2a 浏览器写接口抓包

- 日期：2026-11-04（Asia/Shanghai）
- 沙箱：projectId `6743cee04ca487d085597f8c`，planId `6aeaa22dba3464a24b6c30d4`
- 计划名：用来测试 ego 技能
- 鉴权：Ego Lite 浏览器会话。没有使用 Open API token，也没有粘贴 Cookie。
- 状态：下表每条都是 **CAPTURED-from-UI**，并在同一会话里用 `page.fetch` **VERIFIED-via-session**（前置条件的 UI 失焦有时不发请求，该路径按标题/步骤的模式补测后，会话 PUT 返回 200）。

这是 testcase 写路径的来源。代码和 `testcase-api.md` 只使用下表。未列出的路径一律不当作契约。

## 已验证

| 操作 | 方法与路径 |
|------|------------|
| 创建 | `POST /testcase/api/v1/projects/{projectId}/testplans/{planId}/testcases` |
| 改标题 | `PUT /testcase/api/v1/projects/{projectId}/testhubs/{testhubId}/usercases/{usercaseId}/title` |
| 改前置 | `PUT …/usercases/{usercaseId}/precondition` |
| 改步骤 | `PUT …/usercases/{usercaseId}/steps` |
| 改状态 | `PUT /testcase/api/v1/projects/{projectId}/testplans/{planId}/testcases/{testcaseId}/flowStatusId` |
| 移到回收站 | `POST /api/testcases/{testcaseId}/archive` |

移到回收站不在 `/testcase/api/` 下。Body 为空。产品文案是「移到回收站」。

## 写操作要用的只读

```text
GET /testcase/api/v1/projects/{projectId}/testhub
```

单数。复数 `GET …/testhubs` 为 404。响应 `result._id` 即 `testhubId`。执行用例上的 `_testhubId` 经常是 null。

```text
GET /api/projects/{projectId}/taskflows?type=testcase
GET /api/taskflows/{taskflowId}/taskflowstatus
```

沙箱任务流 `_id=6743cee001b7422d6b7c0843`，名称「测试工作流」。状态 id 只属于这个项目：

| 名称 | _id | kind |
|------|-----|------|
| 待评审 | `6743cee001b7422d6b7c0874` | start |
| 评审中 | `6743cee001b7422d6b7c0875` | unset |
| 执行中 | `6743cee001b7422d6b7c0872` | unset |
| 阻塞 | `6743cee001b7422d6b7c0873` | unset |
| 已通过 | `6743cee001b7422d6b7c0871` | end |
| 未通过 | `6743cee001b7422d6b7c0870` | end |
| 废弃 | `6743cee001b7422d6b7c0876` | end |

创建后的默认状态在该沙箱是待评审（`…874`）。

## ID

| 角色 | 字段 | 用途 |
|------|------|------|
| 执行用例 id | `_id` | 创建响应、set-status、archive |
| 展示编号 | `uniqueId` | 给人看。写路径里没用过它 |
| 库 usercase id | `_fromHubTestcaseId` | 标题 / 前置 / 步骤 PUT 的路径 id |
| 用例库 id | `GET …/testhub` 的 `result._id` | 上述 PUT 的 `testhubId` |
| 分组 | `_commongroupId` | 创建 body |
| 场景字段 | `_scenariofieldconfigId` | 创建 body。UI 会带一个 |

## Body 要点

创建 body 含 `title`、`precondition`、`steps[{desc,expected}]`、`priority`（UI 默认 `-1`）、`caseType`、`customfields: []`、`_executorId`、`_testplanId`、`_projectId`、`_testhubId: null`、`_commongroupId`、`_scenariofieldconfigId`，以及空的 involve 数组。响应 `{ result: case }`。

改标题 `{ "title": string }`。改前置 `{ "precondition": string }`。改步骤 `{ "steps": [{ "_id", "desc", "expected", "expectPayload": null }] }`，保留已有步骤 `_id`。

改状态 body 是 `{ "_flowStatusId": "<statusId>" }`。键名带下划线。响应里的字段是 `_flowstatusId`。

Archive 响应含 `_id`、`_projectId`、`isArchived: true`。

## 试过但不是契约（404）

| 探测 | 结果 |
|------|------|
| `POST /testcase/api/v3/project/{projectId}/testcase/create` | 404 |
| `POST /api/v3/project/{projectId}/testcase/create` | 404 |
| `DELETE /testcase/api/v1/projects/.../testplans/.../testcases/{id}` | 404 |
| `DELETE …/testcases/{id}/delete` | 404 |
| `GET /testcase/api/v1/projects/{projectId}/testhubs` | 404 |
| `GET /api/projects/{projectId}/testhubs` | 404 |
| `GET /api/v3/project/{projectId}/taskflow?type=testcase` | 404 |
| `GET /testcase/api/v1/projects/{projectId}/taskflows` | 404 |

没有把 Open API 的 create / flowStatus 当成浏览器路径的成功契约。
