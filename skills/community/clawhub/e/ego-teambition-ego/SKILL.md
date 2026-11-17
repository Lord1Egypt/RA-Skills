---
slug: ego-teambition-ego
name: teambition-ego
description: >
  Read and update Teambition test plans and single test cases through the Ego Lite
  browser session (www.teambition.com). Login-check first. Phase 2a writes are
  create, update title/precondition/steps, set-status, and archive (delete --yes).
  Use when the user mentions Teambition 测试用例, 用例库, 测试计划, testplan, or case steps.
  Do not use teambition_cli, an Open API token, or the task search API for this module.
metadata:
  version: "0.2.2"
  requires:
    bins:
      - ego-browser
      - node
  ego:
    min_skill_guide: "2.1.0"
version: "0.2.2"
---

# teambition-ego

通过 Ego 里已经登录的浏览器会话管理 Teambition **测试计划 / 测试用例**。读请求走 `https://www.teambition.com/testcase/api/`。Phase 2a 只增加四条单用例写操作，路径以 `references/testcase-api.md` 和 `references/testcase-write-capture.md` 里已经抓到的浏览器接口为准。

Reads and Phase 2a single-case writes use the logged-in Ego browser session on `https://www.teambition.com`. Do not invent POST or PUT paths.

完整技能的方向是 Teambition 管理（项目、任务、测试计划、用例）。`task` 和 `project` 以后挂到同一个 `scripts/tb.mjs` 注册表上，不改路由器。本阶段不做分组创建 / 移动（Phase 2b）和批量（Phase 2c），也不把点页面当主要手段。

## 先装 Ego

先装 **Ego Lite**，保证 `ego-browser` 在 `PATH`。缺失则 soft-fail / 告知用户去装，**不要**硬调浏览器。

Install **Ego Lite** and put `ego-browser` on `PATH`. If either is missing, soft-fail and tell the user. Do not hard-require the browser.

在 Ego 里登录 [teambition.com](https://www.teambition.com/) 之后才能读或改测试计划。每次调用前把这句话告诉用户。

## 不要用 Open API token

测试计划 / 用例不在任务体系里。`teambition_cli` 和 MCP 的 Open API token（`open.teambition.com`）**不要**用于这个模块，读和写都一样。Open 文档里的 create / flowStatus 不是这里的浏览器路径。

Test plans and cases are not tasks. Do not use `teambition_cli` or an MCP Open API token for this module.

## 每次读取或写入前：登录闸门（必做）

Agent **在调用 testcase 命令之前**必须跑：

```bash
node scripts/check-login.mjs
# 需要把窗口留给人登录时：
node scripts/check-login.mjs --keep
```

| 退出码 | 含义 | Agent 做什么 |
|--------|------|----------------|
| `0` | 已登录 | 把 `login_tip` 告诉用户，继续 |
| `2` | 未登录 / 无 ego-browser | 展示 `how_to_login` / `how_to_login_zh`，**停**。请人在 Ego 登录 teambition.com 后再跑 |
| `1` | 其它错误 | 报告 JSON `error`，不要假装已经读到或写过用例 |

详见 `references/login.md`。不要另做 cookie-healthcheck 技能。不要代填密码，不要粘贴 Cookie。

默认 `finish({ keep: [] })`。`--keep` 才把登录页留着并 `handOff()`。

## 命令

仓库根目录：

```bash
node skills/teambition-ego/scripts/check-login.mjs
node skills/teambition-ego/scripts/tb.mjs testcase parse-url "<testplan-url>"
node skills/teambition-ego/scripts/tb.mjs testcase plan <projectId> <planId>
node skills/teambition-ego/scripts/tb.mjs testcase groups <projectId> <planId>
node skills/teambition-ego/scripts/tb.mjs testcase cases <projectId> <planId> [--group <groupId>]
node skills/teambition-ego/scripts/tb.mjs testcase get <projectId> <planId> <uniqueId>
node skills/teambition-ego/scripts/tb.mjs testcase flow-statuses <projectId>
node skills/teambition-ego/scripts/tb.mjs testcase create <projectId> <planId> --title "<title>" [--group <groupId>] [--precondition "<text>"] [--steps-json '<json>'] [--priority <n>] [--executor-id <id>] [--case-type <type>] [--scenario-field-config-id <id>]
node skills/teambition-ego/scripts/tb.mjs testcase update <projectId> <planId> <caseId|uniqueId> [--title "<title>"] [--precondition "<text>"] [--steps-json '<json>']
node skills/teambition-ego/scripts/tb.mjs testcase set-status <projectId> <planId> <caseId|uniqueId> --flow-status-id <id>
node skills/teambition-ego/scripts/tb.mjs testcase delete <projectId> <planId> <caseId|uniqueId> --yes
node skills/teambition-ego/scripts/tb.mjs testcase cleanup
```

已安装的技能目录里用相对路径：`node scripts/check-login.mjs`、`node scripts/tb.mjs testcase …`。

URL 形如 `https://www.teambition.com/project/{projectId}/testplan/{planId}/group/{groupId}`。`parse-url` 不打开浏览器。其余命令在名为 `tb-testcase api` 的任务空间里用 `page.fetch`。`cleanup` 只关闭这个本机空间，不改 Teambition 数据。

| 命令 | 作用 |
|------|------|
| `parse-url` | 从测试计划 URL 打出 `projectId`、`planId`、`groupId`（没有分组时第三列为空） |
| `plan` | 计划名称、状态、用例数、创建人 |
| `groups` | 分组 id、用例数、名称 |
| `cases` | 自动翻页列出用例。`--group` 可选。stderr 打出总数 |
| `get` | 按计划内编号看一条用例（前置条件、步骤、预期、实际、截图） |
| `flow-statuses` | 只读。列出本项目 testcase 任务流的状态 id，给 `set-status` 用 |
| `create` | 在计划里新建一条执行用例 |
| `update` | 改标题、前置条件、步骤。打到用例库 usercase，不是执行用例整包更新 |
| `set-status` | 改流程状态。Body 键是 `_flowStatusId` |
| `delete` | 移到回收站（archive）。必须 `--yes` |
| `cleanup` | `finish({ keep: [] })` 关掉常驻空间 |

`--json` 打出原始 JSON。没有这个 flag 时，多条用例用 `编号 / 完成标记 / 分组 / 标题`。Agent 展示给用户时：两条及以上用表格；单条用段落。完成标记：`✓` 是 `isDone`，`✗` 是未完成或未通过。

`--steps-json` 是 JSON 数组，例如 `[{"desc":"打开页面","expected":"列表可见"}]`。

| 退出码 | 含义 |
|--------|------|
| `0` | 成功 |
| `1` | 参数、HTTP、或浏览器执行错误。未登录时 stderr 会要求在 Ego 打开 teambition.com |
| `2` | 本机没有 `ego-browser`（soft-fail）。check-login 未登录也是 `2` |

## Phase 2a 写白名单

只允许下面这些已抓包路径。分组移动、批量、回写步骤执行结果都不在本阶段。

| 操作 | 方法与路径 |
|------|------------|
| 创建 | `POST /testcase/api/v1/projects/{projectId}/testplans/{planId}/testcases` |
| 改标题 | `PUT /testcase/api/v1/projects/{projectId}/testhubs/{testhubId}/usercases/{usercaseId}/title` |
| 改前置 | `PUT …/usercases/{usercaseId}/precondition` |
| 改步骤 | `PUT …/usercases/{usercaseId}/steps` |
| 改状态 | `PUT …/testplans/{planId}/testcases/{testcaseId}/flowStatusId`，body `{ "_flowStatusId": "…" }` |
| 移到回收站 | `POST /api/testcases/{testcaseId}/archive`，空 body。**不在** `/testcase/api/` 下 |

`testhubId` 用 `GET /testcase/api/v1/projects/{projectId}/testhub`（单数）。更新正文的路径 id 是执行用例的 `_fromHubTestcaseId`，不是 `_id`，也不是展示用的 `uniqueId`。改状态和 archive 用执行用例 `_id`。

CLI 接受 `uniqueId` 或执行用例 `_id`。脚本在计划内查出记录后再写。创建成功后把 `_id`、`uniqueId`、`_fromHubTestcaseId` 告诉用户。

`delete` 没有 `--yes` 时直接拒绝，不发请求。Agent **必须先向用户复述 uniqueId 和标题**，得到明确同意后才能加 `--yes`。对用户说「移到回收站」，不要说成永久删除。

401 时让人重新登录。不要自动重试写请求，也不要改用 Open token。

沙箱（只作文档示例，CI 不访问）：project `6743cee04ca487d085597f8c`，plan `6aeaa22dba3464a24b6c30d4`。

## 传输

`scripts/lib/session.mjs` 是浏览器 `page.fetch` 门面。Open API 传输调用会失败并说明原因。说明见 `references/transports.md`。字段和坑见 `references/testcase-api.md`、`references/pitfalls.md`。

## 测试

```bash
npm test
```

单测 mock 会话，不打真实 Teambition。
