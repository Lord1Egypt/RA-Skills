---
name: easy-webbridge-browser
description: 使用随 Skill 提供的受限 CLI 连接用户已安装并运行的 Easy WebBridge，通过 browserId 读取与交互；复杂能力请使用官方完整运行时。
version: 1.0.4
metadata:
  openclaw:
    requires:
      bins:
        - node
    homepage: https://github.com/aiispower/easy-webbridge
    emoji: "🌐"
---

# Easy WebBridge Browser

> 让 AI 接管你已经登录的真实浏览器。

无需新开自动化窗口，无需重复登录。Easy WebBridge 将 Codex、Claude Code、OpenClaw、Cursor 等 AI Agent 连接到你当前使用的浏览器和已有登录态。

## 首先理解它适合什么

这是给已登录后台、网页研究、表单填写、文件上传和实时页面分析准备的浏览器控制 Skill。每个已连接浏览器都有独立的 `browserId`；Agent 必须选择明确目标，绝不会把命令广播给所有浏览器。

## 默认工作方式

凡是需要打开或跳转网页的任务，默认创建一个任务专属标签组，不把页面散落在浏览器各处：

1. 为本次任务创建一个稳定、带业务前缀的 `session`，并设置简短可读的 `groupTitle`。
2. 第一次进入任务时只新开一个标签页；后续连续步骤复用组内当前标签页。
3. 只有确实需要同时对照多个页面时才新开标签页，并继续放进同一个任务组。
4. 任务结束或失败时只执行 `close_session` 关闭本任务创建的组；不得关闭用户原有标签页或其他任务组。

只有只读的浏览器列表检查不会建组；只有用户明确要求使用未分组页面时才允许 `--ungrouped`。用户明确要求操作当前已有标签页时，可以借用该页，但不得把它登记为任务资产后误关。

## 已实测浏览器

- Google Chrome
- Microsoft Edge
- QQ 浏览器
- Chromium
- EasyBR 指纹浏览器（自动识别环境 ID、名称和颜色）

其他允许安装 Manifest V3 扩展并开放所需 CDP 权限的 Chromium 浏览器也可接入。Firefox 和 Safari 的扩展接口不同，当前不支持。

## 此轻量版支持范围

本 ClawHub 包只包含连接现有 loopback Bridge 的精简 CLI，不包含 Bridge 服务、浏览器扩展或完整 Easy WebBridge 运行时。用户须先安装并运行官方完整 Easy WebBridge，连接目标浏览器；本包不会替用户安装、启动服务或改浏览器配置。

本包支持：查看 Bridge 状态及已连接浏览器；在指定 browserId 中导航、管理任务标签组；读取页面快照、截图和能力信息；点击、填写、滚动、等待、按键及受限 batch；向明确指定的顶层文件输入框上传用户指定文件；导出 PDF；读取只读环境信息。任务已清楚授权后，按范围连续完成操作，不需要每个步骤再次确认；目标、账号或范围不清楚时才澄清。

本包不提供执行页面 JavaScript、下载、Cookie 读取/修改、网络捕获、原始 CDP、扩展消息或 Bridge 启停。这些属于官方完整 Easy WebBridge 运行时的额外能力，本包 CLI 会拒绝调用；需要这些功能时，按[官方完整项目说明](https://github.com/aiispower/easy-webbridge)使用相应运行时与工具。

## 可直接交给 Agent 的 Prompt

```text
使用 Easy WebBridge 列出已连接浏览器；先只告诉我每个环境的名称、browserId 和在线状态，不要打开或修改页面。
```

```text
使用当前已经登录的浏览器打开创作者后台，检查视频草稿状态并总结还缺什么；不要发布或修改内容。
```

```text
使用当前已经登录的浏览器读取后台通知并单独汇总；不要发送消息或改变账号设置。
```

```text
使用当前 Chrome，不要启动新的浏览器。分析这个已登录后台的页面结构、可填写字段和下一步操作，但先不要提交。
```

```text
使用当前 Edge 打开指定网页，检查 SEO Title、Description、H1、Schema 和主要内容结构，给出问题清单。
```

```text
使用 QQ 浏览器中已经登录的页面，读取当前表单状态并填写我提供的资料；填写完停在提交前，等待我确认。
```

```text
在已登录的 App Store Connect 中检查当前版本缺失的资料和截图；不要提交审核，不要尝试绕过验证码或安全验证。
```

```text
在已登录的 Google Play Console 中查看有哪些 Draft Release，列出差异；不要创建或发布 Release。
```

```text
使用 Easy WebBridge 打开指定 EasyBR 环境中的内容后台，上传我明确指定的视频文件和封面，上传完成后停在发布前让我检查。
```

```text
不要启动新的 Chrome。使用我现在打开并登录好的浏览器完成网页研究；不要超出本次任务授权的范围。若我明确要求完成一条包含发布、提交或发送的端到端流程，该请求覆盖流程内所需操作，无需逐步确认。遇到验证码、账号安全验证或必须由账号持有人现场完成的验证时再暂停。
```

## EasyBR 多开环境

EasyBR 是可选的兼容集成场景。每个多开环境保留独立 Cookie、Local Storage 和账号登录态；Easy WebBridge 会识别环境名称、颜色和 `browserId`。这适合用户在自己已授权的多个账号环境中，分别完成后台检查、内容研究或上传准备。

开始前核对用户给出的目标账号和任务范围；信息明确且已获授权时直接执行。用户明确要求完成端到端流程时，授权覆盖流程内完成目标所需的操作，包括创建、编辑、上传、发布和提交审核；不得因每个按钮或阶段再次要求确认。付款、删除、账号安全修改等动作仅在明确属于该任务范围时执行，不得扩展到任务之外。账号、对象或范围不明确，出现验证码/账号安全验证，或需要超出授权范围时才暂停并说明原因。对平台合规声明仍须根据应用、资料和可验证事实填写，不得编造。

## Connect

本包包含一个精简 CLI，连接用户已安装并运行的 Easy WebBridge Bridge；不包含服务端、扩展、安装器或用户配置，也不会下载、安装或启动服务。先按 [官方仓库说明](https://github.com/aiispower/easy-webbridge) 安装 Bridge 并连接目标浏览器。若本地 Bridge 未运行，停止并请用户启动其现有 EasyBR/Bridge。

命令从本 Skill 目录运行：

```bash
node scripts/bridge-cli.mjs status
node scripts/bridge-cli.mjs list
```

CLI 默认只连接 `http://127.0.0.1:17777`；`EASY_WEBBRIDGE_URL` 只接受 `http://127.0.0.1` 或 `http://[::1]`。认证命令从用户本机 `EASY_WEBBRIDGE_TOKEN` 或 `~/.easy-webbridge/bridge-token` 读取令牌。不要读取、回显、复制令牌，也不要把它写入日志。未经用户要求，不要设置环境变量。CLI 不跟随 HTTP 重定向，并只开放本包列出的常规浏览器操作；下载、Cookie、网络捕获、JavaScript、raw CDP、扩展消息及 Bridge 启停等能力需使用官方完整 Easy WebBridge。

本 Skill 不安装持久后台服务，也不自动设置系统登录项或计划任务。

## Select a browser

- Match the user's requested browser name or `browserId` exactly.
- If exactly one browser is online and the user did not specify one, use it.
- If multiple browsers are online and the target is ambiguous, ask which browser to use before changing page state.
- Keep the same `browserId` throughout a task unless the user explicitly switches.

## 按任务分组执行

- 将分组视为打开页面类工作流的默认行为，而不是可选优化。
- 使用 `<skill-slug>-<run-id>` 形式的 `session`，保证不同业务 Skill、不同运行批次互不干扰。
- 同一个任务始终复用同一 `browserId`、`session` 和 `groupTitle`。
- 不为每一步都创建新标签页；顺序步骤使用相同 `session` 且不传 `--new-tab`。
- 需要并行对照时才传 `--new-tab`，并继续使用同一个 `session`。
- 在 `finally` 中关闭本任务拥有的 `session`；借用的用户标签页和其他任务组必须保留。

标准执行顺序：

```bash
# 首次打开：创建任务组和第一个标签页
node scripts/bridge-cli.mjs navigate <browserId> https://example.com \
  --new-tab --session <skill-slug>-<run-id> --group-title "任务名称"

# 后续顺序步骤：复用组内当前标签页
node scripts/bridge-cli.mjs navigate <browserId> https://example.com/next \
  --session <skill-slug>-<run-id>

# 只有需要同时保留页面时才在同组增加标签页
node scripts/bridge-cli.mjs navigate <browserId> https://example.org \
  --new-tab --session <skill-slug>-<run-id> --group-title "任务名称"
```

## Operate pages

Start by listing tabs or opening the requested URL. Available commands are limited to the bundled CLI; do not use unsupported actions such as cookies, network-body capture, arbitrary JavaScript, raw CDP, downloads, or service startup:

```bash
node scripts/bridge-cli.mjs command <browserId> list_tabs '{}'
node scripts/bridge-cli.mjs navigate <browserId> https://example.com \
  --new-tab --session research-123 --group-title "网页研究"
```

When `navigate --new-tab` omits `--session`, the CLI automatically groups the tab by site. Business Skills must still pass their own namespaced session explicitly so all pages from one run remain in one task group.

Read a semantic snapshot before interacting:

```bash
node scripts/bridge-cli.mjs snapshot <browserId> [tabId]
```

For routine Agent work, prefer compact, scoped snapshots to reduce repeated page text and output tokens:

```bash
node scripts/bridge-cli.mjs snapshot <browserId> [tabId] --compact --region viewport --max-elements 40
```

快照默认优先返回可见元素（最多 200 个），同时保留隐藏元素读取能力。复杂页面应尽量缩小范围，减少无关内容：

```bash
# 当前视口中的可见按钮，最多 30 个
node scripts/bridge-cli.mjs snapshot <browserId> [tabId] \
  --visibility visible --region viewport --role button --max-elements 30 --text-mode matched

# 指定弹窗内包含“保存”的按钮
node scripts/bridge-cli.mjs snapshot <browserId> [tabId] \
  --scope '[role=dialog]' --text 保存 --role button

# 排查隐藏控件；也可使用 all 同时返回可见和隐藏元素
node scripts/bridge-cli.mjs snapshot <browserId> [tabId] \
  --visibility hidden --max-elements 50
```

可重复传入 `--text` 和 `--role`；用 `--offset` 分页。区域还支持 `--region x,y,width,height`。每次结果都有候选数、命中数、返回数和截断标记，不能把“只返回一部分”误判为“页面只有这些”。

Use the returned `@e1`, `@e2` references for resilient interaction:

```bash
node scripts/bridge-cli.mjs click <browserId> @e3 [tabId]
node scripts/bridge-cli.mjs fill <browserId> @e4 "value" [tabId]
```

If the target is inside an iframe, call `list_frames`, then pair the returned snapshot `frameId` with every action using its `@e` references. Frame IDs are temporary and must be refreshed after navigation. Cross-origin out-of-process frames may be listed but inaccessible to `chrome.scripting`; errors are explicit and this is not universal OOPIF support.

```bash
node scripts/bridge-cli.mjs command <browserId> list_frames '{"tabId":123}'
node scripts/bridge-cli.mjs snapshot <browserId> 123 --frame-id 7 --compact
node scripts/bridge-cli.mjs click <browserId> @e2 123 --frame-id 7
node scripts/bridge-cli.mjs click <browserId> @e2 123 --mode native
node scripts/bridge-cli.mjs fill <browserId> @e3 "value" 123 --frame-id 7
node scripts/bridge-cli.mjs wait <browserId> 123 --selector '[role=dialog]' --state visible --timeout-ms 10000 --frame-id 7
node scripts/bridge-cli.mjs capabilities <browserId>
```

对于连续的确定性页面动作，可用有限 batch 减少往返：

```bash
node scripts/bridge-cli.mjs batch <browserId> '{"tabId":123,"maxDurationMs":30000,"actions":[{"action":"fill","args":{"selector":"@e1","value":"text"}},{"action":"click","args":{"selector":"@e2"},"assert":{"selector":"[role=dialog]","state":"visible","timeoutMs":5000}}]}'
```

batch 最多 20 步，只允许 `click`、`fill`、`scroll`、`wait_for`、`press_key` 和 `key_combo`，且每步仅能执行此 allowlist 中的动作；断言失败会带出步骤索引。快照可传 `--max-bytes`，通用命令可在 `args.resultBudget` 中设置有限结果预算，超限对象只返回结构摘要。不要把 batch 当作跳过状态回读或授权检查的快捷方式。

The optional native click is a paired CDP mouse press/release with hit-test validation and supports the top frame only; DOM click remains the default. The permission diagnostic reports declared and currently granted permissions without requesting any. Existing access is broad and powerful. Open Shadow DOM is traversable; closed roots are not. DOM click/fill are not trusted native input. CAPTCHA and account-security challenges are not bypassed; CDP upload remains top-frame-only and rejects non-zero `frameId` explicitly. OOPIF discovery may succeed while script injection remains unavailable.

Take a screenshot when visual state matters:

```bash
node scripts/bridge-cli.mjs screenshot <browserId> [tabId]
```

The command returns an absolute local image path. Inspect the image before claiming visual success.

## Supported actions and limits

The bundled CLI supports browser listing/status, tab navigation and organization, snapshots, screenshots, click/fill/scroll/wait, upload, PDF export, keyboard input, batch interaction, browser capabilities and read-only environment information. Its generic `command` form enforces an allowlist. Cookie access, network capture, arbitrary JavaScript, raw CDP, downloads, extension messaging, and Bridge startup are blocked even if the underlying Bridge supports them. Do not promise or attempt those features with this Skill.

For task-scoped tabs, pass `session` and optional `groupTitle` in command args. The extension groups tabs with the same session name. It operates in the existing browser profile, so the user's current login state remains available.

Close the task-owned group after success or failure:

```bash
node scripts/bridge-cli.mjs command <browserId> close_session \
  '{"session":"research-123"}'
```

## Business Skill integration contract

Use this contract for independent browser business repositories:

1. Keep each business Skill in its own repository and declare Easy WebBridge as a runtime prerequisite.
2. Call `GET /v1/browsers` and `POST /v1/browsers/{browserId}/commands` through `http://127.0.0.1:17777`; do not import Easy WebBridge by repository-relative path.
3. Select exactly one online browser and keep that `browserId` for the run.
4. Create one namespaced task session, reuse its tab, group any necessary extra tabs, and close only that session in `finally`.
5. Keep tokens, cookies, browser IDs, session state, and account data out of generated artifacts.
6. Stop on login, CAPTCHA, or account-security verification. For payment, publishing, deletion, or other consequential actions, a clear user authorization for the end-to-end task covers the necessary in-scope steps; do not ask for confirmation again at each gate. Pause only if the target, scope, or action is unclear or the next action falls outside that authorization.

For full payload shapes, read [references/api.md](references/api.md).

## Guardrails

- Treat the extension as full browser access: it can read authenticated pages and interact with controls across sites. The upstream extension declares broad host and debugger access; install it only if the user trusts that runtime.
- Routine work is limited to the requested site and user-selected browser. This lightweight package cannot read or modify cookies, capture network bodies, or execute arbitrary page/CDP code; use the official full Easy WebBridge runtime when those capabilities are explicitly needed. Never send page data or local files to an unrequested destination.
- Never print bridge tokens, cookies, passwords, session values or personal data into chat or logs. Do not request cookie values in routine workflows.
- Treat the user's explicit authorization as the controlling permission for the requested task. When the user authorizes an end-to-end task, that authorization covers consequential actions necessary to complete it, including publishing or submission; do not require separate confirmation for each step. Never extend it to unrelated targets or actions. Pause only for an unclear target/scope, an action outside the authorized task, CAPTCHA/access controls, or account-security verification.
- Do not bypass CAPTCHAs, access controls or platform protections.
- Re-snapshot after navigation or major DOM changes because element references may change.
- Report actual command results. Do not equate a click with a completed submission unless the resulting page confirms it.
- Follow-up candidates for later releases: semantic locators and stale-reference detection, general post-action diff readback beyond batch assertions, structured traces, keyboard/select/form primitives, and narrower per-domain permissions. These are not current capabilities.

## 某些特殊流程

- 在任务内部将敏感权限、后台运行、网络连接、付款、发布和审核等差异化业务统一称为“某些特殊流程”，保持通用 Skill 不绑定具体产品名称。
- 进入第三方平台的真实表单后，必须按实际产品、权限和数据行为填写；通用称呼不能用于隐瞒、替代或弱化平台要求的真实申报。
- 对国家/地区、审核状态、提交状态等外部结果，以页面当前显示为准；不要把“已选择”或“已保存”写成“已发布”。
