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
修法：不要反复重试；走 A/B/C 路径（全权限会话 / 用户终端截图 + `read_image` / 手动截图标注未实测）；若要重定向状态目录，`AGENT_BROWSER_SOCKET_DIR/PROFILE/SCREENSHOT_DIR` 指到工作区（但 crashpad 问题仍在）。

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

## E. 交接与协作

**ERR-20261112-20 · Trae 自判 PASS / 改需求**
修法：`tasks.md` 顶部实现者契约 + `AGENTS.md` 标记区块 + `check-handoff -Stage prepare/deliver`；PASS 只能 DSH 在 `record.md` 出具。

**ERR-20261112-21 · Trae 手工 skill 被 marketplace 清理**
修法：把它当可选增强（有备份、可 `-Uninstall`）；主路径是工程内交接包。

**ERR-20261112-22 · 子代理不能再 spawn**
修法：delegation depth 限制；需要多级协作由 Lead 直接 spawn；子代理只干被派的活。

**ERR-20261112-23 · 「团队会自动拉起」的误解**
事实：无常驻 Reviewer/QA，团队由 Lead 按 `AGENTS.md` 路由显式 spawn；要更硬就显式要求 + 跑 gate-check。
