# 70 · 失败手册（Playbook）

> 每条格式：`ERR-YYYYMMDD-NN` / 现象 / 根因 / 修法 / 复现状态。本文件只收**已复现或高概率复现**的坑；推测不要写成事实。
> 新增条目前先查重；同一坑第 3 次出现 → 提升到工作区 `memory/rules.md`。

## A. Windows PowerShell 5.1

**ERR-20261112-01 · 脚本用 pwsh 7 语法，本机跑不了**
现象：`#requires -Version 7.0`、三元 `? :`、`&&`、`-Encoding utf8NoBOM`、`Test-Json` 报 CommandNotFound/ParseError。
根因：本机只有 Windows PowerShell 5.1（既定 A 方案）。
修法：按 5.1 写；需要无 BOM UTF-8 用 `New-Object System.Text.UTF8Encoding($false)` + `[IO.File]::WriteAllText`；布尔/分支用 `if/else`；多条件用 `;` 或分开写。

**ERR-20261112-02 · 含中文的 .ps1 静默失效**
现象：中文正则永远不匹配、中文字符串乱码、ParserError 指到莫名位置。
根因：5.1 按 ANSI 读无 BOM 文件，中文被破坏。
修法：落盘后统一补 BOM（读字节判断 `EF BB BF`，缺则前置）；运行前用 `[System.Management.Automation.Language.Parser]::ParseFile()` 自检语法。

**ERR-20261112-03 · 双引号字符串里用反引号做 Markdown 标记**
现象：`` Write-Host "- 工程：`$ws`" `` 吃掉闭合引号，连锁 ParserError。
根因：反引号是 PS 转义符。
修法：Markdown 行内代码改用单引号字符串 + `-f` 拼接，如 `Write-Host ('- 工程：`{0}`' -f $ws)`。

**ERR-20261112-04 · 函数名与外部命令同名**
现象：`function Git(...)` 后 `git` 调用行为异常/递归。
根因：PS 函数优先级高于外部命令，遮蔽 `git.exe`。
修法：函数改名 `Invoke-GitCmd`，并显式 `& git.exe`。

**ERR-20261112-05 · 子命令退出码被 `$ErrorActionPreference='Stop'` 打断**
现象：非 0 退出码直接抛异常，拿不到 `$LASTEXITCODE`。
修法：调用前临时设 `Continue`，`try/finally` 恢复；显式取 `$LASTEXITCODE`。

**ERR-20261112-06 · 中文乱码误判为文件损坏**
现象：`Get-Content` 输出花屏，以为 JSON/日志坏了。
根因：5.1 默认 ANSI 解码 UTF-8。
修法：`-Encoding UTF8` 或 `[IO.File]::ReadAllText($p,[Text.Encoding]::UTF8)`；用 Node/Python 复核结构。

**ERR-20261112-06b · 变量名与 switch 参数同名，报 SwitchParameter 转换错误**
现象：脚本内 `$json = $cur | ConvertTo-Json -Depth 3` 抛 `Cannot convert value "System.String" to type "System.Management.Automation.SwitchParameter"`，堆栈指向 ConvertTo-Json 行。
根因：脚本参数 `[switch]$Json` 与局部变量 `$json` 是**同一个变量**（PowerShell 变量名大小写不敏感），给 switch 赋字符串。
修法：局部变量改名（如 `$stateText`）；凡脚本有 `[switch]$X` 参数，就不要再定义 `$x` 变量。

**ERR-20261112-06c · StrictMode 下把「数量」当「文件列表」用**
现象：`$styleFiles = @(...).Count` 后又 `$styleTop = @($styleFiles)`，再 `ForEach-Object { $_.Name }` → `PropertyNotFoundStrict`，报告里只显示 1 个样式文件。
根因：数量是 int，被包装后当成对象取 `.Name`。
修法：分别保留「文件列表」与「数量」两个变量；需要名字时用列表，需要计数时用 `.Count`。

## B. 会话与数据

**ERR-20261112-07 · 会话文件是多帧 zstd，只解出第一帧**
现象：`zstdDecompressSync` 只返回 210 字节的 session 头。
根因：`.jsonl.zstd` 由多帧追加；Node 只解首帧。
修法：按 magic `28 B5 2F FD` 扫描所有帧起点，逐帧解压后拼接（帧边界失败时向后尝试下一个候选）；或改用支持 multiframe 的工具。

**ERR-20261112-08 · 索引半成品导致搜索报错**
现象：`SESSION_QUERY_INDEX_FAILED` / `STALE_CURSOR` / 搜索一直超时。
根因：建库被中断（旧壳误杀/30s 工具超时）。
修法：完全退出 DSH → 删 `%USERPROFILE%\.dsh\session-index.sqlite*`（3 个文件）→ 重开搜一次；或用离线预建工具（`20-runtime-fix.md` §1）。

**ERR-20261112-09 · 长任务被桌面壳误杀**
现象：「任务已停止」/工具结果未知；`desktop.log` 出现 `1/3→2/3→3/3` 后自动重启。
根因：旧壳探活 3×8s 失败即 `killTree`（≈23s 阻塞即死）。
修法：打桌面壳补丁并**完全重启**（见 `20-runtime-fix.md` §2）；未重启前不要在其内跑 >25s 重活。

**ERR-20261112-10 · 3080 EADDRINUSE**
现象：启动失败、端口冲突、双实例。
根因：`dshmarket` 自重启、并发 spawn 竞态、恢复前没复核。
修法：移除 dshmarket；新壳「端口可 accept 只告警 + 恢复前复核」；启动日志确认 `已启动内置服务器`。

## C. 浏览器与视觉

**ERR-20261112-11 · 沙箱里 Chrome/agent-browser 起不来**
现象：`Chrome exited early (exit code: -36863) without writing DevToolsActivePort`；stderr：`crashpad_client_win.cc:431 OpenProcess: 拒绝访问 (0x5)`。
根因：DSH workspace-write 进程沙箱拒绝 crashpad；`~/.agent-browser` 也不可写。
修法：不要反复重试；走 A/B/C 路径（全权限会话 / 用户终端截图 + `read_image` / 手动截图标注未实测）；若要重定向状态目录，`AGENT_BROWSER_SOCKET_DIR/PROFILE/SCREENSHOT_DIR` 指到工作区（但 crashpad 问题仍在）。这些环境变量**只对当前子进程有效**，不写开机启动/计划任务，也不跨会话持久化。

**ERR-20261112-12 · 截图验证靠「肉眼看」没有留证**
修法：截图落 `design-qa/<task>/`，文件名带断点/主题（`375-light.png`）；评审结论引用路径。

## D. 配置与插件

**ERR-20261112-13 · token-insights 卸不掉（uninstall-blocked）**
根因：patch 里还有插入段/禁用行，包管理拒绝卸载。
修法：顺序 = 删插入段 → 删 `disabled: true` → `pnpm remove`/`dsh plugin remove` → 移 storage；顺序不能反。

**ERR-20261112-14 · skill catalog 改了没生效**
现象：磁盘删了 skill，会话里还能看到。
根因：热更新有延迟/会话用的是旧快照；工具集变更也可能只在下轮请求生效。
修法：确认磁盘状态 → 等 watcher/重启桌面版 → 以新会话为准；不要同时反复改。

**ERR-20261112-15 · description 超长被截断**
根因：catalog 每条 description 硬截断 500 字符（源环境确认）；超出部分不进入模型视野。
修法：≤200 字符，把触发词放最前；改完用脚本量字符。

**ERR-20261112-16 · 频繁碎改击穿 prompt 缓存**
现象：费用反而上涨、缓存命中下降。
根因：工具集/skill 清单/catalog 变化改变前缀。
修法：批量一次做完；改动前后记录缓存命中率（cost-meter/usage）。

**ERR-20261112-17 · `~/.dsh` 写入被拒（EPERM/sandbox）**
修法：脚本做成「用户终端执行 + 自动备份 + 回滚」；或在 DSH 内申请一次放宽权限（approval）；不要重复盲试。

**ERR-20261112-18 · 裸 `npx` 命中坏 shim**
现象：`npx` 报错但 `npm.cmd`/`npx.cmd` 正常。
修法：用 `npx.cmd`；不要因此重装 npm。

**ERR-20261112-19 · ConvertFrom-Json 大对象失败**
修法：用 Node/Python 解析；或 `-Depth` 增加；不要整文件打印。

**ERR-20261119-01 · 本机目录装的 bundle 顶层 `import '@deepseek-ai/dsh-*'` 整行不激活**
现象：`plugin_manager action=install_bundle target=<本地目录>` 返回 `packageResult.exitCode=0`，但 `application: failed`，诊断
`dsh: warning: 1 entry did not activate — failed to import: Error [ERR_MODULE_NOT_FOUND]: Cannot find package '@deepseek-ai/dsh-llm' imported from <工作区>\plugins\<pkg>\index.js`。
根因：本地目录安装走 **pnpm link（junction）**，插件真实路径在工作区；Node 从真实路径向上找 `node_modules`，永远到不了 profile 的 `node_modules`（dsh 自带包在那里）。只有从 npm/Git 装进 profile 的包才能顶层直接 import dsh 包。
修法（二选一）：
1. **不要顶层 import**——在 `apply()` 或首次使用时 `await import('@deepseek-ai/dsh-llm')`，失败则用手工构造兜底（`UserMessage` 就是 `{ id, role:'user', content, source }`，形状见 `dsh-session/src/repair.ts` L168）。本 skill 的 P1 插件用这条。
2. 把包发布到 npm/ClawHub 再装进 profile（能解析 dsh 包），但更新与调试变慢。
验证：`plugin_manager action=set_plugin target=include:<row-id> enabled=true` 返回 `application: applied`，才算这一行真的活了。

**ERR-20261119-02 · 插件用 `ctx.fs.writeText` 写文件静默失败（注入成功但没落盘）**
现象：插件逻辑跑通了（会话里能看到注入内容），但目标文件没更新、也没报错。
根因：`dsh-fs-sandbox` 的 `checkedTarget` 是 `policy = sandboxPolicy ?? ctx.sandboxPolicy.resolve()`——不传 per-call 策略时用**部署默认**（fail-safe 是 `read-only`），于是写入被 `FS_SANDBOX_DENIED` 拒绝；插件若 `try/catch` 里只吞掉异常，就完全静默。
修法：写入时显式传**本会话自己的**策略：`ctx.sandboxPolicy.resolve({ session })` 作为 `writeText` 第 5 个参数；并**不要静默 catch**，至少 `logger.warn` 一条。只读会话里写入被拒是正确行为（尊重用户沙箱），降级即可。
验证：改完看目标文件是否出现当前 session id；`read-only` 会话下应 warn 且不落盘。

**ERR-20261119-03 · 客户端插件读文件：`ctx.connection.fetch` 在浏览器半边不存在**
现象：面板渲染出来了，但读数据报 `connection.fetch is not a function`（或在桌面壳里 `fetch /api/file` 直接失败）。
根因：`ctx.connection` 的**浏览器**半边（`dsh-client-connection/src/client/index.ts` 的 `ConnectionHandle`）只暴露 `interactions / isLoopback / generation / state / rpc / openWebSocket / reconnect / registerGenerationSource / start`——**没有 `fetch`、没有 `browserPeer`**。`fetch(request, peer)` 属于 **Host** 侧 Connection（`rpc-host.ts`）。而且桌面渲染器跑在 `dsh-app://` 源上，用 `globalThis.fetch('/api/file?…')` 也命中不了 HTTP API。
修法：客户端要读文件就走生成的 Remote：`ctx.remote.session.list({})` 拿会话（`SessionSummary` 含 `sessionId` + `cwd`）→ `ctx.remote.workspaceFiles.read(sessionId, '<工作区相对路径>', {}, signal)`。相对路径落在该会话的工作区根，所以连 DSH home 都不用知道。
**配套的第二个坑**：Cordis 对子服务是点号键，`inject` 里必须写全，否则运行时报
`cannot get property "remote.session" without inject`。即：
`inject: ['slots', 'connection', 'remote', 'remote.session', 'remote.workspaceFiles']`。
验证：面板空态里显示「读取诊断：…」——成功读到时该行显示「未发生错误」；失败时直接把 HTTP 状态/异常文本打出来，别做静默空白。

**ERR-20261119-04 · 插件夹具只拷 `index.js`，新增 `./actions.js` 后整组 ERR_MODULE_NOT_FOUND**
现象：`takeover.test.mjs` / `fallback.test.mjs` 全红，报 `Cannot find module '<tmp>\plugin\actions.js' imported from '<tmp>\plugin\index.js'`。
根因：两个夹具为绕开 dsh 包解析，用 `fs.copyFileSync(index.js)` 把插件拷到临时沙箱；新加的本地模块不会被自动带上。
修法：夹具同时拷 `actions.js`（以后新增模块一律补拷），或改成拷整目录再排除 `test/`。报错路径是 `<tmp>/plugin/<新文件>` 就是漏拷。
验证：`node plugins/capability-loop/test/takeover.test.mjs` → 13/13。

**ERR-20261119-05 · client 夹具的 vm 沙箱缺 `AbortController`；跨 realm 空数组 `deepEqual` 假失败**
现象：新增“取消运行”后 5 条 client 夹具一起红，`ReferenceError: AbortController is not defined`；补上后 1 条 `Values have same structure but are not reference-equal`。
根因：①`vm.runInContext` 沙箱没有 Node 全局（真浏览器里有 `AbortController`）；②`assert.deepEqual(x.attachments, [])` 的 `[]` 与沙箱里创建的空数组不是同一 realm 的 Array。
修法：沙箱显式注入 `AbortController`；跨 realm 只断长度/类型（`assert.equal(arr.length, 0)`），不要对空数组用 `deepEqual`。
验证：`node plugins/capability-loop/test/client.test.mjs` → 15/15。

**ERR-20261119-06 · Host 半新增会话命令后「面板点了没反应」**
现象：`client.js` 刷新后按钮在，点击后结果区显示「命令未被受理（未注册或语法不符）」。
根因：`commands.register()` 在 `apply()` 里执行，模块在应用启动时就已 import；刷新客户端只重载渲染器，Host 仍是旧模块（Node ESM 缓存），命令不存在。
修法：改 `index.js` / 新增 `actions.js` 后**重启应用**；只改 `client.js` 才只需刷新页面（Ctrl+R）。面板必须把“未受理”与“语法错”分别提示，不能静默。
验证：重启后 `/capability-loop run audit` 在会话里可执行；面板点「运行门禁」出现确认框与 `[门禁] PASS`。

**ERR-20261119-07 · 工作区 `.tmp` 写入被 ACL 拒绝（UnauthorizedAccessException）**
现象：往 `<工程>/.tmp/...` 写探针脚本/截图被拒，同一脚本改到 `docs/` 或 `%TEMP%` 就成功。
根因：该目录的 ACL 被收紧（与 `.gitignore` 无关），不是脚本写错。用 `icacls <dir>` 可看到拒绝项。
修法：临时产物放 `%TEMP%`，要交付的截图放工程内 `docs/...`；不要为了单次写入放宽整目录 ACL（诊断见 skill `diagnose-windows-sandbox-acl`）。
验证：同脚本输出目录换成 `%TEMP%` 后 exit 0。

## E. 交接与协作

**ERR-20261112-20 · Trae 自判 PASS / 改需求**
修法：`tasks.md` 顶部实现者契约 + `AGENTS.md` 标记区块 + `check-handoff -Stage prepare/deliver`；PASS 只能 DSH 在 `record.md` 出具。

**ERR-20261112-21 · Trae 手工 skill 被 marketplace 清理**
修法：把它当可选增强（有备份、可 `-Uninstall`）；主路径是工程内交接包。

**ERR-20261112-22 · 子代理不能再 spawn**
修法：delegation depth 限制；需要多级协作由 Lead 直接 spawn；子代理只干被派的活。

**ERR-20261112-23 · 「团队会自动拉起」的误解**
事实：无常驻 Reviewer/QA，团队由 Lead 按 `AGENTS.md` 路由显式 spawn；要更硬就显式要求 + 跑 gate-check。
