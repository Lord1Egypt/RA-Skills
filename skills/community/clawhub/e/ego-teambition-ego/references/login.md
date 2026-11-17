# Teambition 登录（Ego Lite）

本技能**每次读取或写入测试计划之前**必须先跑 `scripts/check-login.mjs`。技能自己检查登录，不要另搞 cookie-healthcheck。

在 Ego 里登录 teambition.com 之后才能读或改用例。Agent 要把 `login_tip` 告诉用户。写操作同样不接受 Open API token。

## soft-fail

`login_required: true`、退出码 `2`，并带 `how_to_login` / `how_to_login_zh`。Agent **立刻停**，把说明给人，**不要**填密码、不要粘贴 Cookie、不要改用 `teambition_cli` 或 MCP token。

`ego-browser` 不在 PATH 上，或本机没装 Ego Lite 时，同样是退出码 `2`（soft-fail），并告诉人去装。不要把缺浏览器当成硬错误去重试命令。

判定信号：

- 未登录：URL 在 `account.teambition.com`、`login.teambition.com` 或路径 `/login`，或正文出现「扫码登录」「二维码登录」「密码登录」「账号登录」「请登录」。
- 已登录：离开登录墙，并且正文出现 Teambition 应用（「我的项目」「工作台」「新建项目」「测试计划」「测试用例」），或有会话 Cookie 名（`TEAMBITION_SESSIONID` / `TB_ACCESS_TOKEN`）。Cookie 值不打印、不导出。
- 文档标题里的 “Teambition” **不算**已登录。空白页先重画一次，再判断。

## 人要做的事

1. 打开 **Ego Lite**（`ego-browser` 用的同一个配置档）。
2. 打开 https://www.teambition.com/ ，登录能看到该测试计划的账号。
3. 确认组织无误后，让 Agent **重新**跑 `check-login`；exit 0 再继续 `tb.mjs testcase`（含创建、更新、改状态、移到回收站）。

可选：`--keep` 把标签留在登录页并 `handOff()`，方便人当面登录。默认 `finish({ keep: [] })`。

check-login 使用独立任务空间 `teambition-login-check`，不会关掉用例读取用的常驻空间 `tb-testcase api`。
