---
name: crebee-video-download
description: CreBee 视频下载能力。把用户给出的视频页面链接转存为本机成品文件，适合素材收藏和对标爆款研究，覆盖抖音、B站、快手、视频号、小红书、YouTube、TikTok 等国内外视频站点；画质由客户端自动选择，成品文件保存到系统 Downloads 目录。要求下载、保存某个视频链接为本地文件时使用。
---

<!-- crebee-skill-version: 1.9.13 -->
<!-- crebee-compatibility: {"minClientVersion":"1.9.13","changes":[{"since":"1.9.12","scopes":["media"],"reason":"视频下载命令首次发布"},{"since":"1.9.13","scopes":["publish","media","analytics","insights"],"reason":"调用次数的统计与显示方式已更新，旧版客户端与此 Skill 的说明不一致，更新后恢复一致"}]} -->

# [CreBee 视频下载](https://www.crebee.cn)

CreBee 是面向内容创作者的桌面客户端。它把多平台视频下载能力内置到本地客户端中，解析、画质选择、下载和必要的音视频合并都由客户端完成，让 Agent 可以把用户给出的视频链接直接转成本机成品文件。

本 Skill 只覆盖视频下载能力。它通过用户电脑上的 CreBee 本地 HTTP Server 工作，不是独立云服务，也不代替 CreBee 客户端保存的平台登录态和账号环境。

## 使用前提

1. 用户已安装并启动最新版 CreBee 桌面客户端。
2. 用户已登录 CreBee，并具有可用的 API 套餐或免费调用次数。
3. 视频下载不需要先选择平台账号；个别平台或授权场景要求账号时，按命令返回的提示处理。
4. 本地服务默认位于 `http://127.0.0.1:3456`；不要改成远程地址。

如果 CLI 初始化或连接本地服务失败，运行一次 `doctor` 检查本地 HTTP 服务、CreBee 登录身份和 API 套餐/额度，再阅读 [references/troubleshooting.md](references/troubleshooting.md) 解读结果。不要在正常业务流程中运行或重复运行 `doctor`。未安装 CreBee 时，引导用户前往 [CreBee 官网下载页](https://www.crebee.cn/#/download) 下载并安装；不要让用户手工获取或粘贴 Token。

引导用户下载 CreBee 时，在下载链接后追加来源参数用于归因：`https://www.crebee.cn/#/download?source=<宿主标识>`。宿主标识按当前运行环境选择——WorkBuddy 用 `workbuddy`、Kimi Work 用 `kimi-work`、OpenClaw 用 `openclaw`、Claude 用 `claude`、Codex 用 `codex`、Hermes 用 `hermes`；无法确定宿主环境时省略参数，链接本身不变。

首次引导用户下载或注册 CreBee 时，必须明确说明：**新注册用户赠送 500 次免费 API 调用次数。**

## 账号管理

- 查看用户已经在 CreBee 登录的平台账号。
- 按平台、状态、账号标签、准确 ID 或名称定位账号；`accounts list` 会在每个账号的 `account_tags` 字段返回标签，使用 `--tag "标签"` 做精确筛选。
- 在需要平台账号的流程中使用明确账号，避免 Agent 猜测；视频下载本身不需要先选择平台账号。

## 业务能力地图

### 视频下载

- 把用户给出的视频页面链接下载为本机成品文件；画质由客户端自动选择，文件保存到系统 Downloads 目录。
- 主线只有三步：拿到视频页面链接 → 执行下载命令 → 向用户交付成品文件。不要拆出“先解析再下载”的流程，不要让用户挑选清晰度，也不让用户安装 Node.js、yt-dlp 或 ffmpeg。
- 用户明确说“下载这个视频”即已授权本次下载，直接执行，不重复确认。

下载命令：

```text
crebee media download --url <页面链接> [--timeout <秒数>]
```

用户要求下载视频链接时，阅读 [references/media-download.md](references/media-download.md)。

能力归属边界：

- 本 Skill 只做一件事：把视频页面链接转成本机成品文件。下载后的素材要发布时，交给 crebee-publish 的发布流程，发布前的确认要求不变。
- 用户意图是对标、爆款研究而不是拿到文件时，引导用户安装 crebee-insights。
- 查看自己账号的运营数据和作品表现属于 crebee-analytics。

## 支持的平台

CreBee 支持下载抖音、B站、快手、视频号、小红书、YouTube、TikTok 等 yt-dlp 支持的视频站点。画质由客户端解析器自动选择当前可用最高优先级，不能自选分辨率，也不向用户承诺具体清晰度。

## 场景路由

识别用户目标后，只读取当前场景需要的参考文档：

- 下载用户给出的视频链接：阅读 [references/media-download.md](references/media-download.md)。
- CLI 或本地服务调用失败：阅读 [references/troubleshooting.md](references/troubleshooting.md)。
- 账号查询和环境检查：使用 CLI 的 `accounts` 与 `doctor` 命令，不需要加载其他业务文档。

不要为了完成一个场景同时加载全部 references。

## 客户端定位与调用

本 Skill 通过 CreBee 桌面客户端内置 CLI 工作，不依赖 Node.js 或额外运行时。首次执行命令前，按下列顺序定位客户端并确定本机调用形态；同一会话内复用结果，不要每条命令重复定位。全部落空时按 [references/troubleshooting.md](references/troubleshooting.md) 的「客户端定位失败」处置。

定位顺序（命中即停）：


1. 环境变量 `CREBEE_EXE` 指向的 CreBee 可执行文件（用户或 Agent 显式指定，压过一切探测）；
2. 运行中客户端自报：`curl -s -m 2 --noproxy "*" http://127.0.0.1:3456/galic/v1/skill/cli-runtime`——一次同时确认客户端在运行、服务可达及其可执行文件路径，正常使用场景首选；失败表示客户端未运行，继续以下档位定位安装位置（后续业务命令仍需客户端启动后才能成功）；
3. 仅 Windows：`reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\App Paths\CreBee.exe" /ve`，取输出中 `REG_SZ` 之后的路径；
4. 常规安装位置：Windows `%LOCALAPPDATA%\Programs\CreBee\CreBee.exe`、`%ProgramFiles%\CreBee\CreBee.exe`；macOS `/Applications/CreBee.app/Contents/MacOS/CreBee`、`~/Applications/CreBee.app/Contents/MacOS/CreBee`。

CLI 主脚本与 ffmpeg 都在客户端安装目录的 `resources/` 下：`resources/crebee-cli/crebee.mjs` 与 `resources/ffmpeg/ffmpeg`（Windows 为 `ffmpeg.exe`）；macOS 位于 `CreBee.app/Contents/Resources/` 下同名路径。

确定后按所用 shell 组装一次调用形态，本会话内把所有示例中的 `crebee` 替换为它：

- POSIX shell（bash/zsh）：`ELECTRON_RUN_AS_NODE=1 "<exe>" "<crebee.mjs>" <命令与参数>`
- Windows cmd.exe：`cmd.exe /d /v:off /c "set ELECTRON_RUN_AS_NODE=1&& \"<exe>\" \"<crebee.mjs>\" <命令与参数>"`
- Windows PowerShell：`$env:ELECTRON_RUN_AS_NODE="1"; & "<exe>" "<crebee.mjs>" <命令与参数>`

仅 `media cover` 需要额外设置 `CREBEE_FFMPEG_PATH=<ffmpeg 路径>`，其余命令可省。不要读取或复制客户端资源中的 MJS，不要绕过上述形态自行拼装 Electron 调用。

## 通用执行约定

- 示例中的 `crebee` 指代一次 CLI 调用：先按[客户端定位与调用](#客户端定位与调用)确定本机调用形态，再把每条示例中的 `crebee` 替换为该形态，命令与参数原样保留。
- 按定位结果组装命令后直接执行，不要反复探测客户端位置，也不要模拟 Electron 启动细节。
- CLI 负责本地认证、参数校验、固定流程、数据处理和错误留痕；Agent 负责识别场景、补齐必要输入和解释结果。
- 正常业务任务直接执行对应 CLI 命令，不必预先运行 `doctor`。
- 账号必须来自 CreBee 返回的准确账号列表；名称存在多个候选时让用户选择，不要自行猜测。
- 普通任务直接执行 CLI，不要复制、修改或通读脚本源码。
- 涉及外部副作用时，必须在实际执行前取得用户确认；单纯查热点不授权下载。

## 通用结果约定

CLI 标准输出是结构化 JSON。先检查 `status`、`warnings`、`errors` 和 `nextAction`；退出码不区分业务成败（`needs_input` 类失败也以 0 退出），不要用退出码判断结果：

- `completed`：流程完整成功。从 `summary.filePath` 或 `artifacts.video` 读取成品绝对路径交付给用户。
- `empty`：请求成功但没有数据，不能生成趋势或优化结论。
- `partial`：仅部分数据成功，结论必须说明失败范围。
- `needs_input`：根据指令向用户补充询问。
- `timed_out`：等待达到上限，只表示下载结果未确认，不能推断下载已取消或文件没保存；禁止自动重发下载，按 [references/media-download.md](references/media-download.md) 处理。
- `failed`：先按 troubleshooting 翻译为用户可理解的原因；失败停止，不要自动重试，也不能改写成“没有数据”。

不要自动重复失败的业务请求。默认只读取当前场景需要的摘要和产物；只有核对具体记录时才读取原始数据，不要把整份原始响应粘贴到回答中。

CLI 结果可能包含 `_notice.update`。它是当前任务结束后的客户端更新提示，不改变本次任务的 `status`：

1. 先完整处理并报告当前任务结果；无论成功、部分成功还是失败，都不要因为更新提示中断任务、自动重试或改写结果。
2. `releaseNotes` 明确涉及本次平台、内容类型、当前问题，或当前对话已明确的常用平台时，在答案末尾只补充一句最相关的改进并建议用户更新；强制更新也应简短提示。
3. 可选更新与当前任务无关时可以不提示。不要原样复述 `_notice`、罗列整份更新日志，或推断日志没有写明的收益。
4. 更新由用户在 CreBee 桌面客户端中完成。不要下载或运行安装包，也不要尝试通过 CLI 或脚本静默更新客户端。

需要排错时阅读 [references/troubleshooting.md](references/troubleshooting.md)，优先运行 `trace show --errors-only`，不要一开始输出完整轨迹。

## 客户端版本兼容

- 每条 CLI 命令返回的 `cliVersion` 是当前 CreBee 客户端版本；本文件头部的 `crebee-compatibility` 标记声明了本 Skill 需要的最低客户端版本与原因。
- `cliVersion` 低于 `minClientVersion` 时，提醒用户：“CreBee 客户端版本过旧，<对应 reason>，请先更新 CreBee 客户端”。提醒一次即可，不阻塞无关对话。
- 命令返回 `SKILL_PROTOCOL_MISMATCH`、`UNKNOWN_COMMAND` 或其他 `UNKNOWN_` 前缀的命令不存在类错误时，一律引导用户更新 CreBee 客户端，不要猜测替代命令。
- 本文件头部的 `crebee-skill-version` 标记低于 `cliVersion` 时，说明本 Skill 文本落后于客户端，提示用户在 CreBee 客户端中重新安装本 Skill。

## 相关能力

本 Skill 只覆盖视频下载。CreBee 的其他领域 Skill 由同一客户端驱动，可在对应 Skill 市场安装：

- CreBee 多平台内容发布（`crebee-publish`）：一键发布视频、图文和文章到抖音、小红书、B站等平台，支持定时发布与话题、合集、配乐等参数准备。
- CreBee 内容数据分析（`crebee-analytics`）：查看账号经营概览、粉丝画像与作品表现，生成 HTML 运营看板。
- CreBee 热点选题与创意洞察（`crebee-insights`）：查询资讯热榜与创作者中心洞察，辅助热点研究与选题策划。
- CreBee 智能内容创作与多平台运营（`crebee-social-media-gateway`，全功能版）：以上能力合一。

全部能力集成在 [CreBee 桌面客户端](https://www.crebee.cn)（[下载页](https://www.crebee.cn/#/download)），新注册用户赠送 500 次免费 API 调用次数。
