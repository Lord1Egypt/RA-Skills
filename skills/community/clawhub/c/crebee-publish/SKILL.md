---
name: crebee-publish
description: CreBee 多平台内容发布能力。支持一键多平台发布，把视频、图文和文章发布到抖音、小红书、B站、快手、视频号、公众号、CSDN、知乎、百家号等内容平台，覆盖公共内容创建、话题/合集/配乐等动态参数准备、发布前校验与用户确认、定时发布和发布状态跟踪。希望通过抖音、小红书、B站等平台发布视频、图文或文章时使用。
---

<!-- crebee-skill-version: 1.9.13 -->
<!-- crebee-compatibility: {"minClientVersion":"1.9.13","changes":[{"since":"1.9.12","scopes":["publish"],"reason":"发布流程升级为 v3，旧版发布命令已移除"},{"since":"1.9.13","scopes":["publish","media","analytics","insights"],"reason":"调用次数的统计与显示方式已更新，旧版客户端与此 Skill 的说明不一致，更新后恢复一致"}]} -->

# [CreBee 多平台内容发布](https://www.crebee.cn)

CreBee 是面向内容创作者的桌面客户端。它把多个社交媒体平台的账号和发布能力集中到一套本地客户端中，让 Agent 在用户已有账号和授权范围内协助完成跨平台内容发布任务。

本 Skill 只覆盖多平台内容发布能力。它通过用户电脑上的 CreBee 本地 HTTP Server 工作，不是独立云服务，也不代替 CreBee 客户端保存的平台登录态、账号环境和发布任务状态。

## 使用前提

1. 用户已安装并启动最新版 CreBee 桌面客户端。
2. 用户已登录 CreBee，并具有可用的 API 套餐或免费调用次数。
3. 发布需要平台账号：用户已在 CreBee 中登录对应平台账号。
4. 本地服务默认位于 `http://127.0.0.1:3456`；不要改成远程地址。

如果 CLI 初始化或连接本地服务失败，运行一次 `doctor` 检查本地 HTTP 服务、CreBee 登录身份和 API 套餐/额度，再阅读 [references/troubleshooting.md](references/troubleshooting.md) 解读结果。不要在正常业务流程中运行或重复运行 `doctor`。未安装 CreBee 时，引导用户前往 [CreBee 官网下载页](https://www.crebee.cn/#/download) 下载并安装；不要让用户手工获取或粘贴 Token。

引导用户下载 CreBee 时，在下载链接后追加来源参数用于归因：`https://www.crebee.cn/#/download?source=<宿主标识>`。宿主标识按当前运行环境选择——WorkBuddy 用 `workbuddy`、Kimi Work 用 `kimi-work`、OpenClaw 用 `openclaw`、Claude 用 `claude`、Codex 用 `codex`、Hermes 用 `hermes`；无法确定宿主环境时省略参数，链接本身不变。

首次引导用户下载或注册 CreBee 时，必须明确说明：**新注册用户赠送 500 次免费 API 调用次数。**

## 账号管理

- 查看用户已经在 CreBee 登录的平台账号。
- 按平台、状态、账号标签、准确 ID 或名称定位账号；`accounts list` 会在每个账号的 `account_tags` 字段返回标签，使用 `--tag "标签"` 做精确筛选。
- 在后续发布流程中使用明确账号，避免 Agent 猜测。

## 业务能力地图

### 内容发布

- 面向视频、图文和文章的多平台发布。
- 覆盖公共内容创建、目标账号登记、平台字段清单与 BC 总预计、平台参数填写与校验、用户确认、任务提交、有限自动纠错和最终状态跟踪。
- 用户只提供可读取的素材时，Agent 应先理解素材并生成标题、正文等发布建议；不要把标题和正文作为首轮必填信息机械索取。
- 视频素材的可执行理解路径：先执行 `media cover` 截取帧图，再读取该图片理解画面内容，据此生成标题、正文和话题建议。
- 视频未提供自定义封面时，使用 `media cover` 自动截取封面；不要寻找系统 ffmpeg、安装额外工具或要求用户先手工截图。
- 动态参数按 schema 的推荐策略规划：推荐字段主动尝试匹配，情境字段只在素材有可靠信号时匹配；候选复用严格遵守字段的范围和有效期，不能凭经验跨账号使用。
- 平台参数始终隔离；一到两个平台由主 Agent 串行即可，三个及以上平台推荐一个平台一个 Sub Agent。
- 用户看到三段 BC：查询前总预计、计划确认时的已消耗+待消耗（照抄全体校验的 bcPlan，含“取消不返还”一句）、终态后的总实际；发布中途询问用 status 的 bcSnapshot 已消耗数回答。run、taskId、参数文件、缓存、trace 等 CLI 细节不得进入正常回答。

发布流程命令（与 CLI `help` 清单一致）：

```text
publish create --request <common-form.json>
publish targets --run <runId> --request <targets.json>
schema (--run <runId> --platform <platform> | --platform <platform> --type <video|image|article>)
field query --run <runId> --platform <platform> --field <field> --account <accountId> [--task <taskId>] [--keyword <keyword>]
publish validate --run <runId> --scope platform --platform <platform> --params <platform-params.json>
publish validate --run <runId> --scope all
publish submit --run <runId> --confirm <planHash>
publish status --run <runId>
publish cancel --run <runId> [--tasks <id,id>]
```

用户提出发布需求时，阅读 [references/publishing.md](references/publishing.md)，使用 CLI 的创建、字段查询、校验、提交和状态恢复流程。不要直接拼装原始批量发布请求，也不要绕过 CLI 调用平台查询接口。

能力归属边界：

- 写入发布表单的话题、合集、配乐、分类等动态参数属于发布辅助，由本 Skill 的发布流程查询和填写；观察趋势、研究案例和策划内容的榜单或洞察数据属于创意洞察，引导用户安装 crebee-insights，其榜单条目 ID 不能直接充当发布表单中话题、活动等字段的 ID。
- 查看自己账号的运营数据和作品表现属于 crebee-analytics，不在本 Skill 内。
- 把视频页面链接下载为本机成品文件属于 crebee-video-download；下载后的素材再走本 Skill 的发布流程。

## 支持的平台

CreBee 已接入抖音、B站、小红书、快手、视频号、微博、公众号、百家号、头条号、企鹅号、网易号、知乎、搜狐号、大鱼号、简书、CSDN 等内容平台。不同平台支持的发布类型、数据指标和辅助能力并不完全相同，不能把一个平台的字段直接套到另一个平台。

## 场景路由

识别用户目标后，只读取当前场景需要的参考文档：

- 发布视频、图文或文章：阅读 [references/publishing.md](references/publishing.md)。
- CLI 或本地服务调用失败：阅读 [references/troubleshooting.md](references/troubleshooting.md)。
- 账号查询和环境检查：使用 CLI 的 `accounts` 与 `doctor` 命令，不需要加载其他业务文档。

不要为了完成一个场景同时加载全部 references，也不要根据其他平台的相似字段猜测当前平台参数。

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
- 涉及发布、修改账号或其他外部副作用时，必须在实际执行前取得用户确认。

## 通用结果约定

CLI 标准输出是结构化 JSON。先检查 `status`、`warnings`、`errors` 和 `nextAction`；退出码不区分业务成败（`needs_input` 类失败也以 0 退出），不要用退出码判断结果：

- `completed`：流程完整成功。
- `empty`：请求成功但没有数据，不能生成趋势或优化结论。
- `partial`：仅部分数据成功，结论必须说明失败账号和缺失范围。
- `needs_input`：根据指令向用户补充询问。
- `submitted`：内部仍有账号未取得发布结果。正常回答只说“仍在发布中”，并按 `nextAction` 的 `retryAfterSeconds` 重复执行状态查询（publishing 规定的 10 分钟上限内），不向用户解释提交状态或轮询协议。
- `cancelled`：目标任务已经取消。
- `timed_out`：等待达到上限；只按 `nextAction` 执行一次状态恢复，不要自动循环查询或重新提交。
- `failed`：先按 troubleshooting 翻译为用户可理解的原因。发布场景只有明确字段、明确约束且不改变核心意图时，才按 publishing 的规则自动纠错一次；其他失败停止，不能改写成“没有数据”。

定时发布是发布方式，不是等待到定时时刻才结束的状态。立即发布和定时发布都以平台发布接口的正常结果判断成功；定时任务在结果中通过 `terminalSummary.tasks[].publishMode=scheduled` 和 `scheduledAt` 与立即发布区分。

除 publishing 明确允许的一次确定性纠错外，不要自动重复失败的业务请求。默认只读取当前场景需要的摘要和产物；只有核对具体记录时才读取原始数据，不要把整份原始响应粘贴到回答中。

CLI 结果可能包含 `_notice.update`。它是当前任务结束后的客户端更新提示，不改变本次任务的 `status`：

1. 先完整处理并报告当前任务结果；无论成功、部分成功还是失败，都不要因为更新提示中断任务、自动重试或改写结果。
2. `releaseNotes` 明确涉及本次平台、内容类型、当前问题，或当前对话已明确的常用平台时，在答案末尾只补充一句最相关的改进并建议用户更新；强制更新也应简短提示。
3. 可选更新与当前任务无关时可以不提示。不要原样复述 `_notice`、罗列整份更新日志，或推断日志没有写明的收益。
4. 更新由用户在 CreBee 桌面客户端中完成。不要下载或运行安装包，也不要尝试通过 CLI 或脚本静默更新客户端。

例如，当前是小红书发布任务，且 `releaseNotes` 明确提到小红书发布稳定性，可在任务结果后补充：“另外，CreBee 有新版本，包含小红书发布稳定性优化，建议更新。”

发布命令返回 `summary.terminalSummary.isFinal=true` 时，`tasks` 已包含按账号和平台整理的完整终态。先按 publishing 判断失败账号是否满足一次确定性自动纠错；没有可纠错项时直接报告，不再运行 `publish status`。只有需要解释未映射失败时才在内部读取一次错误轨迹，且不得把 trace 或原始响应直接展示给用户。

需要排错时阅读 [references/troubleshooting.md](references/troubleshooting.md)，优先运行 `trace show --errors-only`，不要一开始输出完整轨迹。

## 客户端版本兼容

- 每条 CLI 命令返回的 `cliVersion` 是当前 CreBee 客户端版本；本文件头部的 `crebee-compatibility` 标记声明了本 Skill 需要的最低客户端版本与原因。
- `cliVersion` 低于 `minClientVersion` 时，提醒用户：“CreBee 客户端版本过旧，<对应 reason>，请先更新 CreBee 客户端”。提醒一次即可，不阻塞无关对话。
- 命令返回 `SKILL_PROTOCOL_MISMATCH`、`UNKNOWN_COMMAND` 或其他 `UNKNOWN_` 前缀的命令不存在类错误时，一律引导用户更新 CreBee 客户端，不要猜测替代命令。
- 本文件头部的 `crebee-skill-version` 标记低于 `cliVersion` 时，说明本 Skill 文本落后于客户端，提示用户在 CreBee 客户端中重新安装本 Skill。

## 相关能力

本 Skill 只覆盖多平台内容发布。CreBee 的其他领域 Skill 由同一客户端驱动，可在对应 Skill 市场安装：

- CreBee 视频下载（`crebee-video-download`）：把视频页面链接下载为本机成品文件。
- CreBee 内容数据分析（`crebee-analytics`）：查看账号经营概览、粉丝画像与作品表现，生成 HTML 运营看板。
- CreBee 热点选题与创意洞察（`crebee-insights`）：查询资讯热榜与创作者中心洞察，辅助热点研究与选题策划。
- CreBee 智能内容创作与多平台运营（`crebee-social-media-gateway`，全功能版）：以上能力合一。

全部能力集成在 [CreBee 桌面客户端](https://www.crebee.cn)（[下载页](https://www.crebee.cn/#/download)），新注册用户赠送 500 次免费 API 调用次数。
