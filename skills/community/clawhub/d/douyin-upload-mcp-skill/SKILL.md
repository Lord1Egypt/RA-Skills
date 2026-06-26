---
name: douyin-upload-mcp-skill
description: 抖音自动投放与登录守卫。用于抖音创作者平台自动发布视频/图文、检测登录失效、生成二维码、处理短信/机器人/安全验证、同步数据生成分析、根据数据生成下一条视频方案、自动回复评论/私信、数字人形象定制/训练、一键成片、截图并通过飞书提醒客户。遇到抖音发布、投放、二维码登录、客户扫码、登录过期、发布前检查、字段化短视频发布任务、数据分析、生成下一条视频内容、训练数字人、形象定制时必须使用。飞书用户消息必须实际调用 douyin__douyin_feishu_route_text，不要只解释计划。
---

# 抖音投放与登录守卫 Skill

## 任务契约

其他 agent 给本 skill 的字段化发布输入，优先采用这类结构：

```json
{
  "视频地址": "https://example.com/video.mp4",
  "封面图片": "https://example.com/cover.png",
  "标题": "作品标题",
  "tags": "#标签1#标签2"
}
```

最少字段：
- `视频地址`
- `标题`

推荐完整字段：
- `视频地址`
- `封面图片`
- `标题`
- `tags`

字段含义：
- `标题` 是抖音发布标题；抖音最多 30 个字符，脚本会强制截断到 30 字以内。生成视频审核文案、字段化发布文本、发布任务文件必须使用同一个 30 字安全标题，不能展示长标题但发布另一个标题。
- 大视频上传、转码和发文助手检测可能需要 30-60 分钟。真实发布必须走后台异步 job 或长超时；OpenClaw 同步请求超时不能当作发布失败，更不能通知“发布成功”。
- 一键成片视频画面里的主标题必须使用短字段 `videoTitle`/`visualTitle`，控制在 4-8 个中文字符；不要把长发布标题直接传给视频画面标题，否则会越界被裁切。脚本会自动从长标题中提取短标题，例如 `张辉：高温强光专用散光膜怎么少踩坑？` 的画面标题应变成 `散光膜避坑`，发布标题仍保留完整安全标题。

## 数字人自动化营销

飞书或 OpenClaw 用户触发自动化营销，也必须走单入口 `douyin__douyin_feishu_route_text({text, messageId, chatId})`。入口已接入：

| 用户原文 | 行为 |
|---|---|
| `生成人设` / 发送姓名、照片、主营业务等字段 | `scripts/persona-flow.js` 收集字段，按 `references/persona-positioning-prompt.md` 的完整 prompt 生成 IP 人设画像、精准用户画像、账号定位和营销策划方案；照片只用于后续形象定制，不注入人设 prompt；模型不可用时自动规则兜底 |
| 客户直接发“我叫xx，做xx，想在抖音做账号...”这类杂乱资料 | 飞书入口会识别为人设资料，抽取已提供字段；缺失项只追问缺失字段，并给一条可复制补充格式 |
| `通过` / `确认人设` | 有待确认人设时确认并写入 `persona-state.json`，随后自动进入数字人形象定制；形象完成后初次启动会继续自动生成视频并等待用户审核 |
| `不通过 修改建议` / `调整人设` | 有待确认人设时按修改建议重新生成人设，不要求客户重新填写全部资料 |
| `查看完整人设` | 返回已生成的完整 IP 战略定位和营销策划方案 |
| `绑定数字人ID xxx` | 客户已有数字人时直接写入营销状态，后续一键成片使用该 ID |
| `训练数字人` / `形象定制` | 默认走 mentor 工作流：用已确认人设和本人照片请求 Coze 生成训练视频，再调用小冰创建任务、查质检、启动训练、查训练结果，成功后绑定数字人 model id；已有数字人可直接绑定 ID，测试/应急时可显式使用默认 model id |
| `查看数字人训练` / `数字人状态` | 推进或查看当前形象定制任务：质检中、训练中、成功、失败 |
| `启动自动化营销` / `开启自动化营销` | 初次启动先收集人设资料；人设通过且数字人就绪后自动开启本地每日任务并通知用户；已开启后再次发送只返回当前状态/管理提示 |
| `查看形象` / `确认形象` | 仅用于 demo 或客户明确要使用默认测试数字人时确认默认 ID；正式流程优先训练数字人或绑定客户 ID |
| `开启自动确认` / `关闭自动确认` | 显式切换审核模式。默认按 mentor 流程在审核节点等待确认；自动确认只跳过方案/视频审核，登录、短信、安全验证、风控仍会暂停提醒 |
| `生成视频方案` / `确认方案` | 先生成标题、封面、tags、口播脚本和成片参数，用户确认方案后再生成视频 |
| `自动化营销状态` | 汇总人设、数字人 ID、待确认方案/视频、定时、最近执行状态 |
| `初次生成数字人视频` | 初次启动内部指令：只基于已确认人设和已完成数字形象生成首条视频，不等待定时任务，不强制读取数据分析 |
| `生成数字人视频` / `一键成片` | 日常手动成片：基于已确认方案调用一键成片服务；没有方案时先生成/确认方案，避免绕过审核 |
| `确认发布` / `发布这个视频` | 将上一条待确认视频送入抖音发布入口 |
| `不满意` / `重新生成视频` | 丢弃上一条待确认视频并重新生成 |
| `生成并发布` | 显式立即执行：数据/方案 → 一键成片 → 字段化发布任务 → 抖音发布入口 |
| 定时 `tick-marketing-daily` | 默认每日到点自动同步数据、生成数据报告并生成完整视频审核消息；必须等客户回复 `确认发布` 才进入抖音发布入口。只有客户显式开启自动确认/自动发布模式时才可跳过审核 |
| 其他非营销指令 | 若已确认人设，则基于当前人设身份、目标客户和沟通调性给出简短回复；未确认人设时返回使用说明 |

交互容错：
- 近义词会自动归一：`同步数据/刷新数据/拉取数据/获取数据` → `更新数据`，`数据报表/查看报表/分析报告` → `数据报告`，`生成选题/下一条选题` → `生成下一条视频`，`回复互动/处理消息` → `自动回复`，`开启营销/开通自动化营销` → `开启自动化营销`。
- 缺字段不误执行：`绑定数字人ID` 未带 ID 时只提示 `请发送：绑定数字人ID xxxxx`；数字人训练缺已确认人设或照片时只追问缺失项；发布任务只有 `视频地址` 或只有 `标题` 时只提示补齐缺失字段。
- 初次启动自动串联：`启动自动化营销` 收集资料并生成人设；用户回复 `通过` 后自动形象定制；形象完成后立刻基于人设生成首条视频，不等待定时任务/数据分析；视频必须等用户回复 `确认发布` 才投放。客户不需要额外回复 `训练数字人`。
- 首次开启/重新确认人设时，不得复用旧人设训练出的数字人状态。训练/默认降级生成的数字人必须带当前人设指纹（确认时间、姓名、照片），只有匹配当前已确认人设才算就绪；客户已有数字人也必须在人设确认后重新发送 `绑定数字人ID xxx` 才视为当前人设可用。
- 人设审核内容必须完整发给飞书用户；长内容用飞书分段消息发送，不能回复“内容较长已截断，完整版本保存在 persona-state.json”这类客户看不到的本地路径提示。
- 数字人形象就绪后，自动化营销正式启用每日任务并通知用户：默认每天 07:30 执行数据更新、生成新视频并等待用户确认发布。这个设定不影响首条视频立即生成和发布审核。
- 避免误发布：`通过` 只用于确认人设或视频方案；最终视频审核必须回复 `确认发布`。用户回复 `不通过 + 修改建议` 时，根据当前状态修正人设、方案或视频。
- 真实验收时不得由本地 CLI/agent 代替客户发送 `确认发布`。除非用户明确要求“模拟客户确认并真实发布”，否则测试只能停在待确认视频状态，必须等飞书用户本人回复 `确认发布` 后才启动发布 job。
- 发布必须异步：`确认发布` 或字段化任务进入发布后只能启动后台 job；不要让 OpenClaw 同步等待视频上传、发文助手检测和审核结果。大视频上传/审核可能超过 70 秒，最终成功、短信验证或失败由后台 job 再发飞书通知。
- 适当功能提醒只放在决策点：收集资料、待审人设、形象定制开始、形象完成开始制片、待审视频、发布完成。工具已发飞书消息后，OpenClaw/其他 agent 不得再复述同义消息。
- 未识别消息只发一条简短使用说明；不把内部错误、脚本栈、JSON 细节发给客户。

新增脚本：
- `scripts/persona-flow.js`：人设定位多轮收集、完整 prompt 画像生成、草案、确认。
- `scripts/persona-feishu-messy-stability.js`：用模拟飞书消息测试“客户杂乱输入→精准追问缺失字段→继续补充→生成待确认人设→确认后自动进入数字人训练”，防止客户不按表格填写时流程断掉。
- `scripts/feishu-interaction-fallback-stability.js`：用模拟飞书消息测试近义词、错词、缺字段、未知命令等交互兜底。
- `scripts/xiaoice-video-produce.js`：连接 `XIAOICE_VIDEO_TOOL_DIR`（默认 `~/自动营销/xiaoice-video-tool`）的本机 video-task-service，创建/等待/查询一键成片任务。
- `scripts/marketing-controller.js`：营销总控，负责开启/关闭、状态、生成视频、确认发布/重做、生成并发布、每日流水线。
- `scripts/digital-human-training.js`：照片+人设到数字人模型的状态机。默认执行 Coze 生成训练视频、小冰创建任务、轮询质检、启动训练、轮询训练结果并绑定数字人 ID；显式传 `--use-default-model` 或设置 `DIGITAL_HUMAN_SKIP_COZE=true` 时才降级绑定默认 model id。
- `scripts/digital-human-training-stability.js`：用模拟飞书消息连续测试“训练数字人→缺字段追问→dry-run 训练完成→数字人状态”。
- `scripts/marketing-feishu-flow-stability.js`：用模拟飞书消息连续测试“人设→确认→数字人训练→开启→方案确认→视频确认→发布dry-run→数据报告→自动回复”闭环。

数字人形象生成已接入主流程。默认按 mentor 文档执行 Coze + 小冰四接口；默认 model id 只用于 demo、应急降级和稳定性 dry-run。自动化营销前必须满足：已确认人设，并且数字人已绑定当前人设对应的客户已有或训练后的 model id。人设用于账号定位、数字人训练视频生成、内容方案、口播脚本和互动调性。重新确认新人设会清空旧待审视频、旧成片和旧数字人绑定，避免首次开启测试误吃历史模型。

统一失败话术：
- 视频不可用：`视频处理失败，请重新发送可用的视频。`
- 封面不可用：`封面设置失败，请重新发送可用的封面图片。`
- 登录失效：`抖音登录已失效，需要重新扫码。`
- 需要短信：`抖音登录需要短信验证。请直接回复 6 位验证码。`
- 安全验证：`抖音出现安全验证，当前无法自动处理。请按截图完成后回复“已完成”。`
- 页面排查：`已收到截图请求，我会先截当前页面再处理。`

统一迁移顺序：
0. 从源机器导出迁移包。默认安全包：`npm run export:skill`，不含 `.env/.env.local`。受信任私有机器需要带密钥时：`node scripts/export-skill-package.js /path/to/out --include-env`。公开 GitHub/ClawHub 包会携带 `vendor/xiaoice-video-tool` 的代码和 `references/skill-local-config.md`/`.env.example`，但不携带小冰 `.env`、密钥、任务数据库、浏览器登录态、OpenClaw 会话历史或 `node_modules`。
1. ClawHub 公开安装优先运行：`openclaw skills install douyin-upload-mcp-skill --force`，然后进入 `~/.openclaw/workspace/skills/douyin-upload-mcp-skill`。
   - 如果使用 `openclaw --profile <name>`，实际目录通常是 `~/.openclaw/workspace-<name>/skills/douyin-upload-mcp-skill`。以安装命令输出的 `Installing to ...` / `Installed ... -> ...` 路径为准。
2. OpenClaw 2026.4.2 里不要写 `openclaw skills install douyin-upload-mcp-skill --version 0.1.0`：这个 `--version` 会被顶层 OpenClaw 当成打印 CLI 版本，导致安装命令静默不落盘。
3. 如果使用私有迁移包或 GitHub clone，可解包/clone 到任意目录；运行 `node scripts/bootstrap-openclaw.js --apply` 后会把当前目录注册为 `mcp.servers.douyin`，不要求固定在 `~/.openclaw/skills`。
4. 安装后运行 `npm install`/`npm ci`、`cp references/skill-local-config.md .env.local 2>/dev/null || cp .env.example .env.local`、`node scripts/bootstrap-openclaw.js --apply`；填写 `.env.local` 和 `~/自动营销/xiaoice-video-tool/.env` 后，再运行 `node scripts/preflight.js --online`、`node scripts/agent-ready.js`。
5. 飞书发 `定时任务`、`自动化营销状态`、`发布抖音` 验证。

## OpenClaw 飞书模式

复制到新 OpenClaw 后，先自举运行时：

```bash
node scripts/bootstrap-openclaw.js --apply
```

它会安装/检查 Node 依赖、把 `vendor/xiaoice-video-tool` 安装到 `~/自动营销/xiaoice-video-tool`、缺浏览器时尝试自动安装 Chromium/Chrome、自动注册 `mcp.servers.douyin`、生成并启动 `douyin-skill-supervisor.service`、检查浏览器 daemon、OpenClaw/MCP、飞书和多维表配置。默认是 OpenClaw gateway 接飞书模式，不启动 watcher。只有没有 OpenClaw gateway、要本 skill 自己监听飞书时才用：

```bash
node scripts/bootstrap-openclaw.js --apply --standalone-watcher
```

自举不能代替人工授权：飞书 app 密钥/会话 ID、多维表授权、首次抖音扫码+短信、安全验证仍需真人完成。

如果这个 skill 是从 GitHub 或 ClawHub 安装到新 OpenClaw，安装后仍要先跑一次：

```bash
cd ~/.openclaw/workspace/skills/douyin-upload-mcp-skill
npm install
node scripts/bootstrap-openclaw.js --apply
```

然后再跑：

```bash
node scripts/preflight.js --online
node scripts/agent-ready.js
node scripts/douyin-schedule-manager.js install-default
```

这一步会把依赖、MCP 注册、daemon 和 OpenClaw 配置补齐；不跑就只有“文件下载完成”，还没真正可用。
同时会检查中文字体兜底：优先系统字体，其次使用 skill 自带的开源 CJK 字体，避免新环境里中文变方块。

做隔离裸装测试时，必须换服务名和状态目录，避免覆盖正在使用的主服务：

```bash
DOUYIN_BOOTSTRAP_SERVICE_NAME=douyin-skill-supervisor-test \
DOUYIN_MONITOR_STATE_DIR=$HOME/.openclaw/workspace/douyin-ops-bootstrap-test \
node scripts/bootstrap-openclaw.js --apply
```

如果消息来自飞书用户，首选单入口 MCP：

`douyin__douyin_feishu_route_text({ text: 原文, messageId, chatId })`

飞书上下文必须一起传：
- `messageId`：飞书消息元数据里的 `message_id`，例如 `om_xxx`。
- `chatId`：飞书消息元数据里的 `conversation_label` / `chat_id`。群聊是群的 `oc_xxx`，私聊是私聊的 `oc_xxx`。

传了 `messageId` 后，skill 会查询该消息的 `chat_id` 并把二维码、短信、发布完成、数据报告、自动回复结果都发回触发来源；传了 `chatId` 时可直接锁定回包目标。群聊触发就回群，私聊触发就回私聊。

如果 agent 忘了传 `messageId/chatId`，MCP 会从 OpenClaw 最近飞书会话日志里兜底推断来源会话，优先选择最近一条匹配用户原文的消息。只有参数和近期日志都拿不到来源时，才退回配置里的 `DOUYIN_FEISHU_RECEIVE_ID`。

收到飞书用户消息时必须实际调用此工具，不能只回复“我会调用/应该调用/已路由”。只有工具返回后，才能总结结果。若测试要求不要发飞书消息，调用时传 `dryRun:true`。

不要在普通飞书流程里调用 generic `browser`、`exec`、`memory_search`，也不要直接运行 `node scripts/...`。这个入口已封装登录检查、二维码、短信验证码、字段化发布、数据同步报告、评论/私信自动回复和飞书通知状态机。
测试时可加 `dryRun:true`，不要给客户发消息；真实飞书流程不要加。

意图路由。OpenClaw/MiniMax/其他 agent 在飞书模式下只做一件事：把客户原文原样传给这个入口，然后按入口返回结果简短回复。发布、数据、评论、私信都不要绕过入口。

硬规则：
- 飞书用户消息一律先调用 `douyin__douyin_feishu_route_text({text: 原文, messageId, chatId})`；如果上下文没有 `messageId/chatId`，才只传 `text`。
- 群聊里被 @ 后，必须把群的 `conversation_label/chat_id` 作为 `chatId` 传入，不能把二维码和状态发回旧私聊。
- 即便只传 `text`，入口也会尝试从最近 OpenClaw 飞书会话里推断群聊/私聊来源；但显式传 `chatId` 仍是最稳路径。
- 工具返回 `customerAlreadyNotifiedByTool:true` 时，不要再发可见飞书消息，不要输出 `NO_REPLY`；如果运行时必须输出，用 `HEARTBEAT_OK` 静默占位。
- `生成下一条视频/内容方案/具体文案/生成文案` 是异步后台 job：入口返回后由 worker 最终只发一条方案到飞书。不要因为等待、空回复或超时而改调 `douyin__douyin_next_video_plan_from_feishu_bitable`，不要把低层 JSON 手动整理发给飞书，不要追问“是否生成封面图”。
- `确认方案/通过` 确认视频方案后也是异步后台 job：入口会先发送 `老板，正在为您制作视频，请耐心等待～`，worker 完成后一条标准视频审核话术发飞书。不要因为工具等待、空回复或超时改调 `douyin__douyin_marketing_controller`、`douyin__douyin_xiaoice_video_produce`、`douyin__douyin_digital_human_training` 或 `douyin__douyin_persona_flow`，否则会重复成片和重复话术。
- 不要在飞书流程里直接调用 `douyin__douyin_check_login`、`douyin__douyin_fresh_qr` 或浏览器工具。
- 用户说 `已登录/已完成` 不等于真的登录。必须让入口复查页面；如果页面仍是二维码，只能保持扫码状态，提示：`仍未登录，请用手机抖音 App 扫码并确认。二维码过期请回复：发送二维码。`
- 用户说 `发送二维码/二维码过期/已过期` 时，仍然只调用单入口；入口会获取最新二维码并发送飞书。
- 用户说法未命中时，入口会发送简短使用说明。不要自行猜测或沉默。
- 短信验证码错误、超时、重复旧码时，入口会提示客户回复 `发送验证码`，再输入最新 6 位验证码。

| 用户原文 | 调用 |
|---|---|
| `发布抖音` | `douyin__douyin_feishu_route_text({text:"发布抖音", messageId, chatId})` |
| `发送二维码` / `二维码过期` | `douyin__douyin_feishu_route_text({text:"发送二维码", messageId, chatId})` |
| `已登录` / `已完成` | `douyin__douyin_feishu_route_text({text:"已登录", messageId, chatId})` |
| `123456` | `douyin__douyin_feishu_route_text({text:"123456", messageId, chatId})` |
| `发布视频` | `douyin__douyin_feishu_route_text({text:"发布视频", messageId, chatId})` |
| 字段化发布任务含 `视频地址/封面图片/标题/tags` | `douyin__douyin_feishu_route_text({text:完整原文, messageId, chatId})` |
| `更新数据` / `数据更新` / `数据报告` / `数据分析` / `分析数据` / `查看数据` | `douyin__douyin_feishu_route_text({text:原文, messageId, chatId})` |
| `生成下一条视频` / `下一条视频` / `内容方案` / `具体文案` / `生成文案` | `douyin__douyin_feishu_route_text({text:原文, messageId, chatId})` |
| `自动回复` / `自动回复评论` / `自动回复私信` | `douyin__douyin_feishu_route_text({text:原文, messageId, chatId})` |
| `截图` / `页面截图` / `当前页面截图` | `douyin__douyin_feishu_route_text({text:原文, messageId, chatId})` |
| `定时任务` / `修改定时任务 自动回复 30分钟` / `修改定时任务 自动化营销 07:30` | `douyin__douyin_feishu_route_text({text:原文, messageId, chatId})` |
| `生成人设` / `开启自动化营销` / `确认开启` / `开启自动确认` / `关闭自动确认` / `生成数字人视频` / `生成并发布` / `自动化营销状态` | `douyin__douyin_feishu_route_text({text:原文, messageId, chatId})` |
| `训练数字人` / `照片：https://...` / `查看数字人训练` / `数字人状态` | `douyin__douyin_feishu_route_text({text:原文, messageId, chatId})` |

只有在非飞书、纯 MCP 集成或调试时，才直接调用下面的低层工具。

## Quick Start

先判断任务类型，只走对应入口：

| 目标 | 最快入口 | 细节 |
|---|---|---|
| OpenClaw 飞书完整闭环 | `douyin__douyin_feishu_route_text({text: 原文})` | `references/login-feishu.md` |
| 独立 watcher 飞书闭环 | `node scripts/feishu-reply-watcher.js watch --since-seconds 1800 --interval-ms 1000 --page-size 50 --max-pages 10` | 只在不用 OpenClaw gateway 接飞书时运行 |
| 客户发“发布抖音” | watcher 自动检查登录，已登录提示发视频，未登录提示扫码 | `references/login-feishu.md` |
| 上游 agent 发字段 `视频地址/封面图片/标题/tags` | watcher 自动下载素材、登录守卫、发布、同步数据 | `references/publish-flow.md` |
| OpenClaw/其他 agent 直接发布字段化文本 | `douyin__douyin_publish_from_upstream_text` 启动异步 job，再用 `douyin__douyin_publish_job_status` 查询 | `references/publish-flow.md` |
| 本地发布任务 JSON | `node scripts/publish-task.js --task /abs/publish-task.json --execute` | `references/publish-task.md` |
| 更新数据 | 飞书发 `更新数据`/`数据更新`，或运行 `node scripts/sync-douyin-data-to-feishu-bitable.js --days 90 --notify` | `references/data-interactions.md` |
| 数据报告/数据分析 | 飞书发 `数据报告`、`数据分析`、`分析数据`、`查看数据`；入口会先同步近 90 天到飞书多维表，再从多维表出基础报告和 MiniMax/OpenClaw 增强分析 | `references/data-interactions.md` |
| 生成下一条视频方案 | 飞书发 `生成下一条视频`、`下一条视频`、`内容方案`、`具体文案`、`生成文案`；入口会启动后台 job，基于多维表数据生成标题、封面文案、tags、口播脚本、画面建议和 `digitalHumanInput`，最终只向飞书发一条方案 | `references/data-interactions.md` |
| 数字人自动化营销 | 飞书发 `启动自动化营销`；初次启动按“收集资料→人设审核→自动形象定制→自动生成首条视频→确认发布”执行。日常任务默认在审核节点等待确认；用户显式发 `开启自动确认` 后，定时任务才自动生成方案、成片并进入发布入口 | `references/automation-workflow-table.tsv` 和 `references/marketing-feishu-copy.md` |
| 读取/回复评论 | 最新可见队列：`node scripts/douyin-comment-reply.js list --unreplied --author-reply-check --pages 8`；全作品只读：`node scripts/douyin-comment-reply.js list --all-works --unreplied --author-reply-check --pages 3 --max-works 20`；真实回复加 `reply --text "..." --unreplied --author-reply-check --execute` | `references/data-interactions.md` |
| 读取/回复私信 | `node scripts/douyin-dm-reply.js list`；真实回复加 `reply --text "..." --execute` | `references/data-interactions.md` |
| 按内容自动回复互动 | `node scripts/douyin-auto-reply.js both --execute --limit 50 --max-scan 200`；飞书发 `自动回复/自动回复评论/自动回复私信` | `references/data-interactions.md` |
| 定时自动回复/每日自动化营销 | `node scripts/douyin-schedule-manager.js install-default`；飞书发 `定时任务/修改定时任务...` | `references/customer-install-guide.md` |
| 登录/二维码 | `node scripts/douyin-login-monitor.js check --notify --send-qr ask`；客户准备好后 `fresh-qr --send --customer-ready` | `references/login-feishu.md` |
| Multica/微信/QQ 入口 | multica 只接任务和回状态，二维码默认发飞书 | `references/multica.md` |

新 agent 接手固定顺序：

```bash
node scripts/bootstrap-openclaw.js --apply
node scripts/help.js
node scripts/preflight.js --online
node scripts/agent-ready.js
node scripts/openclaw-douyin-health.js
```

如果 OpenClaw 调用 `douyin__...` 工具返回 `Not connected`、私聊/群聊提示浏览器或抖音工具连接异常，先在机器上恢复运行态，不要向客户发送“联系管理员/重启 Gateway/NO_REPLY”这类内部故障话术：

```bash
node scripts/openclaw-douyin-health.js --fix --restart-gateway
```

恢复后让客户重新发送上一条触发词即可。若必须提示客户，只说：`系统已恢复，请重新发送上一条指令。`

OpenClaw gateway 已经接入飞书时，只允许 OpenClaw 消费飞书消息。不要再启动 `feishu-reply-watcher.js watch`，否则会出现两个入口同时回复、重复发布、争抢同一个浏览器。

此模式需要 OpenClaw gateway 和一个浏览器 daemon。推荐使用 `douyin-skill-supervisor.service` 只守护 daemon，并保持 `DOUYIN_SUPERVISOR_START_WATCHER` 不是 `true`：

```bash
systemctl --user status openclaw-gateway.service douyin-skill-supervisor.service
ps -ef | grep -Ei 'feishu-reply-watcher|publish-upstream-job-worker|publish-task|publish-with-guard' | grep -v grep || true
```

如果不用 supervisor，也可以只运行独立 `douyin-browser-daemon.service`。不要让 `douyin-skill-supervisor.service` 和 `douyin-browser-daemon.service` 同时各自启动浏览器 daemon。

只有不用 OpenClaw gateway、希望本 skill 自己监听飞书时，才允许启动 watcher：

```bash
DOUYIN_SUPERVISOR_START_WATCHER=true npm run supervisor
```

只做一次性调试时才直接运行 watcher：

```bash
node scripts/feishu-reply-watcher.js poll --init
node scripts/feishu-reply-watcher.js watch --since-seconds 1800 --interval-ms 1000 --page-size 50 --max-pages 10
```

## 必须遵守

- 不要自行打开新浏览器访问抖音；必须复用本 skill 的 daemon/CDP。
- 浏览器任务必须串行；共享 daemon/page 不能并发跑登录、数据、评论、发布测试。
- 脚本已内置轻量浏览器任务锁；新增浏览器脚本也必须使用同一锁，避免共享标签页互相切走。
- 飞书消息进入 OpenClaw 时首选 `douyin_feishu_route_text`；低层工具仅用于调试或非飞书集成。
- 飞书入口四大任务都必须走 `douyin_feishu_route_text`：自动发布、获取数据生成分析、自动回复评论、自动回复私信。
- 飞书里发 `截图` / `页面截图` / `当前页面截图` 时，入口会截取当前抖音页面并把图片回传飞书，适合排查方块字、弹窗、按钮不可点、验证码失真等问题。
- 飞书里发 `定时任务` 可查看状态；只显示两类：`自动回复` 和 `自动化营销`。`修改定时任务 自动回复 30分钟` 修改自动回复频率；`修改定时任务 自动化营销 07:30` 修改每日自动化营销时间。`数据报告` 保留为用户主动触发功能或自动化营销内部步骤，不作为单独定时任务显示。
- 默认定时任务必须用 `douyin-schedule-manager.js install-default` 注册。需要关闭自动回复时执行 `node scripts/douyin-schedule-manager.js disable-auto-reply` 或飞书发 `关闭自动回复`；冷启动、重测或用户要求暂停全部任务时必须先执行 `node scripts/douyin-schedule-manager.js disable`；配置关闭时 supervisor 不应启动本地 scheduler loop。
- 冷启动、重新测试或 `douyin_feishu_route_text({reset:true})` 必须先暂停旧定时任务，避免上次测试遗留的自动回复/日报/营销任务混入当前流程。脚本会调用 `douyin-schedule-manager.js disable`，人工排查时也要确认 `schedule-config.json.enabled=false` 且三个 job 都是 disabled。
- 评论自动回复默认只信抖音页面的 `未回复` 筛选和页面可见作者回复；本地 `auto-reply-state.json` 只做审计记录，不参与跳过，避免不同作品里的短评论（如“加油”“666”）被误判已回复。只有显式传 `--trust-local-state` 或设置 `DOUYIN_COMMENT_TRUST_LOCAL_STATE=true` 时，才允许用本地状态辅助跳过。真实回复后必须等待 60 秒，再切换 `全部评论 → 未回复`，同一作品循环到未回复为空才切下一个作品。
- 数据分析和自动回复优先读取 OpenClaw 当前模型配置；如果 OpenClaw 配的是 MiniMax，就必须以 `MiniMax-M2.7` 等 OpenClaw 模型结果作为验收口径，不用 Codex/GPT 结果替代。
- 生成下一条视频同样优先读取 OpenClaw 当前模型配置；用户问“下一条视频/具体文案/生成文案/内容方案”时必须调用入口，不要只根据数据报告自由总结。入口会异步生成，最终飞书消息必须包含 `标题/封面文案/tags/口播脚本/画面建议/digitalHumanInput`，可直接交给数字人成片接口的下一层。
- 异步发布和下一条视频方案必须由后台 job 完成；OpenClaw 环境优先用 `systemd-run --user` 托管，不能依赖 Gateway 子进程生命周期，否则重启 Gateway 会把任务打断并导致飞书无最终回复。
- 自动回复文案默认必须用 OpenClaw/MiniMax 或兼容接口按 prompt 生成：结合粉丝原话，简短、自然、能引导继续互动；模型不可用或输出不安全时默认跳过该条，不发送规则兜底。只有显式传 `--allow-rules-fallback` 或设置 `DOUYIN_AUTO_REPLY_ALLOW_RULES_FALLBACK=true` 才允许规则兜底。
- 飞书话术必须少而准；只在需要客户动作时发消息，不把内部报错/脚本栈发给客户。
- 所有飞书通知必须去重：同一阶段只发一次最终状态，不在“确认中/处理中”与“成功/失败”之间来回轰炸。
- 发布成功的最终判定以管理页可见新作品为准，不只看单个发布工具返回值。
- 客户必须先触发流程：客户发“发布抖音”或上游任务包含 `视频地址/标题` 才进入发布链。
- 二维码只在客户回复“发送二维码”后发送；发送前必须刷新/重新生成并做质量检测。
- 二维码、短信验证码提醒、安全验证截图默认发飞书，不默认发 Multica。
- 如果页面出现机器人/滑块/安全验证，截图给客户并给最短解决建议，不要尝试绕过验证。
- 新 agent 接手时，环境、权限、登录和单入口守护是 agent 的责任；能自动修就自动修。
- 飞书入口不是 OpenClaw/MCP 调用时，才必须由 `feishu-reply-watcher.js watch` 或 `DOUYIN_SUPERVISOR_START_WATCHER=true npm run supervisor` 常驻监听；否则客户发消息没有进程接收。
- 飞书入口是 OpenClaw gateway 时，必须停止 watcher，只保留一个浏览器 daemon；`douyin-skill-supervisor.service` 可保留用于守护 daemon，但 `DOUYIN_SUPERVISOR_START_WATCHER` 不能为 `true`。
- 任意“修复完成”都要实测；关键闭环按连续 3 次成功验收，失败一轮就重新计数。
- 验收分级必须说清楚：`dry-run/脚本回归通过` 不等于 `OpenClaw+飞书+浏览器真实链路通过`。公开包可用 `node scripts/preflight.js --online`、`node scripts/agent-ready.js`、`npm run stability:feishu-route` 等做安装/脚本回归；真实发布验收另按 `references/publish-flow.md` 走，并明确需要真人扫码/验证码/风控配合。

## 何时读 Reference

- 登录、二维码、短信验证、飞书触发词、客户话术：读 `references/login-feishu.md`。
- 发布页、发布按钮、封面、字段化发布任务、发布稳定性：读 `references/publish-flow.md` 和 `references/publish-task.md`。
- 字段化发布任务含 `封面图片` 时，必须走 `prepare-upstream-publish-task.js`/`publish-task.js`，或调用低层 `douyin_publish_video` 时显式传 `coverImageUrl`/`coverImagePath`；否则只能回退 AI 推荐封面。
- 字段 `tags` 支持 1 个、2 个或更多标签；发布脚本必须通过编辑页 `#添加话题` 生成真实话题节点并回读验证，不能只把 hashtag 当普通简介文本。
- 数据同步/报告、评论回复、私信回复：读 `references/data-interactions.md`。
- Mentor 功能分类表、脚本职责和已实现/待实现边界：读 `references/mentor-function-table.tsv`。
- 数字人自动化营销飞书话术、`通过/不通过` 阶段判断、人设确认后自动形象定制：读 `references/marketing-feishu-copy.md`。
- 客户小白安装、OpenClaw cron 定时任务、修改定时任务：读 `references/customer-install-guide.md`。
- 用户只有 OpenClaw 对话能力、不会命令行时：把 `references/openclaw-install-prompt.md` 的提示词和安装包一起发给目标 OpenClaw，让 OpenClaw 自己找附件、解压、安装和检查。
- 用户只有 Codex、OpenClaw 可能没装好时：使用 `references/openclaw-install-prompt.md` 的思路，让目标侧 agent 先确认 WSL/Ubuntu、Node、OpenClaw，再安装本 skill；公开包不附带私有 Codex 迁移提示词。
- 真实迁移验收：公开包只保留可分发 skill 和基础安装脚本；私有 WSL 镜像、真实发布三连、首轮数字人训练验收脚本不随 ClawHub 包发布。做真实迁移验收时，使用私有迁移包里的验收脚本，或在目标机按 `references/customer-install-guide.md` 手工完成安装、配置、扫码、发布和删除测试。
- Multica、微信、QQ、多客户端入口、沙箱只读目录：读 `references/multica.md`。
- 复盘过的坑和举一反三规则：读 `references/pitfalls.md`。
- 验收标准、清理 OpenClaw 会话、测试前后停定时：公开包可以跑 `node scripts/preflight.js --online`、`node scripts/agent-ready.js` 和相关 stability 脚本；真实飞书+浏览器+抖音发布验收必须人工配合扫码/验证码/风控，不能只跑单个 dry-run 后宣称全链路稳定。

## 固定路径

ClawHub/OpenClaw workspace 安装路径：

`$HOME/.openclaw/workspace/skills/douyin-upload-mcp-skill`

旧版手工安装路径也可用，但需要 bootstrap 注册当前目录：

`$HOME/.openclaw/skills/douyin-upload-mcp-skill`

飞书客户会话：

`YOUR_FEISHU_CHAT_ID`

## MCP 工具

OpenClaw 中工具名通常带服务器前缀：

- `douyin__douyin_check_login`
- `douyin__douyin_fresh_qr`
- `douyin__douyin_publish_video`
- `douyin__douyin_publish_from_upstream_text`
- `douyin__douyin_publish_job_status`
- `douyin__douyin_publish_imagetext`
- `douyin__douyin_data_analysis`
- `douyin__douyin_sync_data_to_feishu_bitable`
- `douyin__douyin_data_report_from_feishu_bitable`
- `douyin__douyin_comment_list`
- `douyin__douyin_comment_reply`
- `douyin__douyin_dm_list`
- `douyin__douyin_dm_reply`
- `douyin__douyin_auto_reply`
- `douyin__douyin_persona_flow`
- `douyin__douyin_marketing_controller`
- `douyin__douyin_digital_human_training`
- `douyin__douyin_xiaoice_video_produce`
- `douyin__douyin_screenshot`
- `douyin__douyin_probe`
- `douyin__douyin_feishu_route_text`

## 定时任务

OpenClaw 定时任务由 `scripts/douyin-schedule-manager.js` 管理，不启动额外 Feishu watcher。

默认安装：

```bash
node scripts/douyin-schedule-manager.js install-default
```

默认策略：
- `douyin-auto-reply-30m`：定时自动回复可独立关闭。开启时执行 `tick-auto-reply`，评论默认走每作品 `未回复` 下拉框，逐条回复、每条后等 60 秒、切换 `全部评论 → 未回复`，直到当前作品未回复为空再切下一个作品；跳过已显示作者回复/自己的评论，不默认使用本地状态去重。私信跳过最新消息已是我方回复的会话，默认不强制未读标记，除非设置 `DOUYIN_DM_REQUIRE_UNREAD=true`。默认每类最多处理 50 条。发布优先级最高：自动回复遇到 `publish:*` 浏览器锁或发布优先请求时必须立即让路，不得抢占或打断发布；发布完成后再由下一次主动/定时自动回复继续处理。自动回复最短间隔为 30 分钟，用户设置更短时必须在飞书提示“为避免任务重叠，最短间隔为 30 分钟”；无新消息默认静默，有回复或失败才通知飞书。
- 数据报告：不单独作为定时任务显示；用户主动发 `数据报告` / `更新数据` 时按需同步和分析，自动化营销内部也会使用数据。
- `douyin-marketing-daily-0730`：开启自动化营销后默认每天 07:30 执行；生成视频后等待用户回复【确认发布】，用户回复【不通过 + 修改建议】则重做视频，不得自动发布。

修改：

```bash
node scripts/douyin-schedule-manager.js set-auto-reply --every 30m
node scripts/douyin-schedule-manager.js set-marketing-daily --time 07:30
node scripts/douyin-schedule-manager.js status
```

飞书客户也可直接发：`定时任务`、`修改定时任务 自动回复 30分钟`、`修改定时任务 自动化营销 07:30`、`关闭定时任务`、`开启定时任务`。

## Agent 责任

- 运行 `node scripts/preflight.js --online`，缺 Node 依赖时安装，缺浏览器/daemon 时启动或修复。
- 检查 OpenClaw/飞书配置和 `.env`，只报告缺失项，不泄露 secret。
- MCP `Not connected` 是 OpenClaw 到 MCP 子进程的内部连接故障。先运行 `node scripts/openclaw-douyin-health.js --fix --restart-gateway`，确认 `preflight/agent-ready` 通过；不要把“联系管理员/重启 Gateway/NO_REPLY”发给飞书客户。
- 检查飞书多维表权限；缺权限时自动发送授权链接，客户点完后重试。
- 检查是否只有一个飞书消费者：OpenClaw 飞书模式下 watcher 必须关闭；`douyin-skill-supervisor` 只负责守护浏览器 daemon。
- systemd supervisor 必须带 GUI 环境变量；若浏览器报 `Missing X server/acquire_failed/Not connected`，自动修复 daemon/环境后重试，不要把系统故障发成客户人工验证。
- 检查抖音登录；失效时按 `references/login-feishu.md` 走扫码/短信/安全验证。
- 遇到抖音页面结构变化时，先截图/探测 DOM，尝试修复脚本并更新本 skill，再重新测试。
- 只有真人授权、扫码、短信、安全验证、平台风控不能由 agent 代做；这些情况给客户最短明确指令。
