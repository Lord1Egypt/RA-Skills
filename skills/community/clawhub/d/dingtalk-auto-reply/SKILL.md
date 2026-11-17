---
name: dingtalk-auto-reply
description: 监控钉钉未读会话，单聊用 AI 以本人身份自动回复（普通员工口吻、平级回同事），群聊/指定名单只发微信提醒（不代发，防社死）。覆盖 dws 未读接口、CodeBuddy Agent SDK 生成回复的 SERVER__PORT 端口冲突坑、自报家门坑、回复自己坑。当用户要求「钉钉自动回复/钉钉代回/监听钉钉未读+AI回复」时使用。
agent_created: true
---

# 钉钉自动回复（未读监控 → AI 代复 → 微信通知）

监控钉钉未读会话，单聊用 AI 以本人身份自动回复（普通员工口吻、平级回同事），群聊/指定名单只发微信提醒（不代发，防社死）。

> 内部 skill，未公开仓库；要迁移直接整目录拷贝（见下方「迁移 / 重装」段）。

## 技能包含的文件（自包含，可直接移植）

```
dingtalk-auto-reply/
├── SKILL.md                      # 本说明
├── README.md                     # 精简版介绍（特性 / 架构 / 安装 / 配置，随包分发）
├── .env.example                  # 配置样例（cp .env.example .env 后填写真实身份/Key）
├── .gitignore                   # 隐私黑名单（.env / _media_cache / .vbs 等不随包分发）
├── dingtalk_unread_monitor.py    # 入口（仅 docstring + main() + 统一 re-export；旧 import 兼容）
├── runtime.py                    # 基础/配置层：.env 加载、SDK 可用探测、路径探测、全部共享常量、日志/锁/缓存/审计/鉴权
├── dingtalk_api.py               # 钉钉交互层：dws 调用、未读/消息拉取、单聊·群@判定、图片下载、发送
├── vision.py                     # 多模态层：图片识别（统一走 CodeBuddy Agent SDK，与文本同后端）
├── reply.py                      # 回复生成层：persona / 查表 grounding / SDK 生成 / 微信推送
├── gen_launcher.py              # 启动器生成器（本机自动生成 Startup .vbs，.vbs 不随包分发）
├── dingtalk-helper-backup.md    # 【方案B·人设干净部署模板】dingtalk-helper.md 的占位版（无私人数据），随 skill 移植；新机器未注册 agent 时自动兜底注入
├── _validate.py                  # 自测脚本（7 模式：集成 / --inject / --test-guard / --test-construct / --test-statemachine / --test-mcp / --env，不真发回复；--env 做环境预检）
├── _setup_env.py                 # 安装脚本：探测并写入 SDK 运行环境（CODEBUDDY_SDK_PYTHON 等）到 .env
├── recover_missed.py            # 补发漏掉的消息（监控曾宕机/DRY_RUN 时，手动拉未读并代复）
└── stop_monitor.ps1             # 精确结束本脚本 python（仅停进程，Windows 用）
```

> 运行时自动生成（不随包分发，已在 `.gitignore` 排除）：`.env`、`_media_cache/`、`__pycache__/`、`dingtalk_auto_reply_launcher.vbs`。

> **代码已按职责拆分为 4 模块 + 入口**（2026-07-17，原单文件 1642 行）。改哪块改哪块：
> - 调 dws / 未读判定 / 发送 → `dingtalk_api.py`
> - 图片识别 → `vision.py`
> - 人设 / 查表 grounding / SDK 生成 / 微信推送 → `reply.py`
> - 路径 / 常量 / 日志 / 锁 / 鉴权 → `runtime.py`
> - 调度主循环 → `dingtalk_unread_monitor.py`
> 入口 `dingtalk_unread_monitor.py` 把各模块名字 re-export，故 `_validate.py` / `recover_missed.py` 仍 `import dingtalk_unread_monitor as M` 无需改动。
> 注意：可变配置 `DRY_RUN` / `SELF_OPEN_ID` 经 `runtime.DRY_RUN` / `runtime.SELF_OPEN_ID` 访问（模块属性而非 import 副本），`recover_missed.py` 改的是 `runtime.DRY_RUN`。

移植：把整个目录复制到目标机的 `~/.workbuddy/skills/` 即可，无需改代码。

⚙️ **移植后必做一步：把 dws 加入系统 PATH**（根因与自动追加机制见下方「dws 依赖」段）。`dws` 不在 PATH → `get_unread` 恒空；换机部署先跑一次 `gen_launcher.py` 自动幂等追加（无需重登），新终端敲 `dws` 有输出即就位。

⚠️ **启动器 `.vbs` 不随包分发**：`.vbs` 是机器专属胶水文件（路径用 `%USERPROFILE%` 环境变量展开动态推导、无硬编码用户名，并备 `SpecialFolders("Profile")` / `%HOMEDRIVE%%HOMEPATH%` 兜底），被列入 `.gitignore`，**不会随仓库/打包上传**。换机或重新克隆后，启动器由 `gen_launcher.py` 在本机生成（见下方「Windows · Startup 启动器」），监控脚本首次运行也会自动自检并生成，无需手动复制 `.vbs`。

## 环境要求与安装（一键预检）

本技能运行依赖以下外部组件，**一个都不能少**；缺任何一项都会导致「监控活着却读不到未读 / 生成失败」。换机部署或异常时，先跑下面的「一键预检」，缺啥它会直接给出修复命令，不用盲猜。

| 依赖 | 作用 | 安装 / 修复 |
|---|---|---|
| **Python（default venv）** | 跑脚本的解释器；`codebuddy-agent-sdk` 必须装在这个 venv 里 | 用 venv python 跑本脚本：`%USERPROFILE%\.workbuddy\binaries\python\envs\default\Scripts\python.exe`（macOS/Linux 用 `.../bin/python3`）。裸 managed python / anaconda 不含 SDK，会 `_SDK_AVAILABLE=False` |
| **codebuddy-agent-sdk** | 生成回复 + 图片识别的唯一后端（deepseek-v4-flash 经此 SDK） | `venv_python -m pip install codebuddy-agent-sdk`（或 `pip install -r requirements.txt`） |
| **dws CLI** | 拉未读 / 发消息 / 通讯录 | 跑 `gen_launcher.py` 自动加入 PATH；`dws patch chmod` 授权 `chat.message:list` / `chat.message:send` / `contact:search` |
| **codebuddy CLI** | SDK 底层起 prewarm server 用 | 随 WorkBuddy 安装；`CODEBUDDY_CMD` 路径见 `print_paths()` |
| **node** | dws NODE-direct 路由需要 | 装 Node 并确保在可用路径 |
| **gbrain MCP（可选）** | 查表 / 知识库；不配则纯人设回复 | `GBRAIN_MCP_URL` / `GBRAIN_MCP_TOKEN`，缺省自动读 `~/.workbuddy/mcp.json` 的 `gbrain` 条目 |
| **代码库检索（可选）** | 让回复 agent 检索本地源码回答「源码/接口/实现细节」问题 | `.env` 填 `CODE_SEARCH_ROOTS`（分号分隔路径列表，不填=不启用）；`CODE_SEARCH_TOOL` 指向 search.py（默认自动探测 `~/.workbuddy/tools/code-search/search.py`，未装则回退 Grep/Glob/Read） |
| **视觉识别（可选）** | 图片识别；与文本同后端、零额外 key | 默认跟随文本模型 `CODEBUDDY_MODEL`；可用 `VISION_MODEL` 单独指定 CodeBuddy 侧视觉模型。SDK 缺失时视觉与文本一并降级为「仅通知不识别」 |
| **SDK 运行环境声明（`.env`）** | 让 skill / agent 识别「用哪个 python 跑」 | 安装时跑 `_setup_env.py` 自动把 `CODEBUDDY_SDK_PYTHON` / `CODEBUDDY_MODEL` / `CODEBUDDY_INTERNET_ENVIRONMENT` / `CODEBUDDY_CMD` 写入 `.env` |

### 安装步骤（agent 安装时写入 SDK 环境）

1. **装依赖（如尚未装）**：用**目标 venv 的 python** 装 SDK
   ```bash
   %USERPROFILE%\.workbuddy\binaries\python\envs\default\Scripts\python.exe -m pip install -r requirements.txt
   ```
2. **探测并写入 SDK 环境**（关键）：跑安装脚本，让 agent 把 SDK 运行环境写进 `.env`
   ```bash
   %USERPROFILE%\.workbuddy\binaries\python\envs\default\Scripts\python.exe _setup_env.py
   # 仅预览不写： _setup_env.py --check
   # 强制覆盖 SDK 项： _setup_env.py --force
   ```
   它会遍历候选 python 找到装了 `codebuddy-agent-sdk` 的那个，连同主模型 / 网络环境 / CLI 路径写入 `.env` 的 `CODEBUDDY_SDK_PYTHON` 等项。之后 **monitor 被任意 python 拉起都能按该声明自拉回到正确环境**（见 runtime `sdk_reexec_target`）。
3. **预检**：确认环境完整
   ```bash
   %USERPROFILE%\.workbuddy\binaries\python\envs\default\Scripts\python.exe _validate.py --env
   ```
4. **填私密身份**：`cp .env.example .env`（若还没建）→ 在 `.env` 填 `BOSS_UID` / `SELF_OPENDINGTALK_ID` / `SELF_SENDERS` / `MENTION_NAMES` 等（详见下方「隐私与身份配置」）。

> ⚠️ **`CODEBUDDY_SDK_PYTHON` 不是隐私**，可随技能分发；但 `.env` 整体仍被 `.gitignore` 忽略（含 `BOSS_UID` 等隐私）。换机时重新跑 `_setup_env.py` 即可重新写入 SDK 环境。

**一键预检（推荐每次部署/异常先跑）**：

```bash
# 必须用装了 SDK 的 venv python 跑（关键）
%USERPROFILE%\.workbuddy\binaries\python\envs\default\Scripts\python.exe _validate.py --env
```

`--env` 逐项打印 `[OK] / [MISSING] / [WARN]`：
- **阻断级缺失**（SDK / dws）→ 给精确修复命令、退出码非 0；必须先修。
- **非阻断项**（gbrain / 人设 agent）→ 只告警，功能降级仍可运行（纯人设回复、用 skill 内 `dingtalk-helper-backup.md` 兜底）。

> 每次跑其它模式（集成 / --inject / --test-*）也会**先自动跑一遍预检**，环境异常第一时间暴露。

> ⚠️ **视觉与文本共用同一 SDK 后端**：`_SDK_AVAILABLE=True` 时两者都可用；SDK 缺失时文本也生成不了，不是视觉单独降级——所谓「仅通知不识别」是 SDK 缺失时的整体回退，与以前行为一致。

## 完整 pipeline（顺序不可乱）

1. `dws chat message list-unread-conversations --format json` → 只返回有未读的会话（天然过滤）。
   字段：`openConversationId`、`title`、`singleChat`(true=单聊)、`unreadPoint`、`lastMsgCreateAt`。
2. 单聊 → 用 `openConversationId` 拉最新一条消息：
   `dws chat message list --group <openConversationId> --time "<now>" --direction older --limit 5 --format json`
   ⚠️ **必须带 `--direction older`**：含义"从给定时间往更早拉"，配 `--time now` 即返回最新消息（newest-first）。
   不带 direction 时默认 older 且起始时间若早于消息 → 消息被过滤成空。
   单聊也能用 `--group <openConversationId>`（无需 `--user`/`--open-dingtalk-id`）。
3. **回复生成（CodeBuddy Agent SDK 主后端 + 查表事实 grounding + 会话记忆）**：先按消息意图 `detect_table_intent` 判断查哪张表
   （`feedback`=问题反馈表 / `project`=ROS项目表），用 `fetch_table_context` 拉「本人(userId=<BOSS_UID>)名下未解决项」
   （带缓存）注入 system_prompt；再用 **CodeBuddy Agent SDK**（`_gen_reply_sdk_async`，`system_prompt`=人设+查表数据，`query`=干净单行消息）
   生成回复，`session_id=dt_<cid>`（首轮 `session_id`、后续 `resume` 续上下文）实现「一人一会话、记忆连续」。
   SDK 不可用/失败 → 返回空（不代发，推微信转人工），无 CLI 兜底。详见下方「生成回复的关键坑」。
4. `dws chat message reply --conversation-id <cid> --ref-msg-id <openMessageId> --ref-sender <senderOpenDingTalkId> --text <回复> --yes` 带引用回复。
5. 微信推送：默认用 `~/.workbuddy/skills/weixinclaw-proactive-push/send.js`（仅文本，不转发媒体）。
   若该 skill 未安装，脚本**自动降级为仅日志**，不报错、不阻断主流程。

## 路径解析（可移植核心，勿硬编码用户名）

脚本不再写死任何用户名。外部二进制按以下优先级解析，**全部支持环境变量覆盖**：

| 用途 | 环境变量覆盖 | 自动探测位置 |
|------|-------------|--------------|
| dws CLI（直接路径·主路由） | `DWS_EXE` | `~/.workbuddy/binaries/node/cli-connector-packages/node_modules/dingtalk-workspace-cli/vendor/dws.exe` |
| dws CLI（cmd 兜底） | `DWS_CMD` | `~/.workbuddy/binaries/node/cli-connector-packages/dws.cmd` |
| codebuddy CLI | `CODEBUDDY_CMD` | `~/.workbuddy/binaries/node/versions/<最新版本>/codebuddy.cmd` |
| node | `NODE` | `~/.workbuddy/binaries/node/versions/<最新版本>/node.exe` |
| 微信推送脚本 | `WEIXIN_SEND_JS` | `~/.workbuddy/skills/weixinclaw-proactive-push/send.js` |

人设真源 = codebuddy 全局注册 agent `dingtalk-helper`（`~/.codebuddy/agents/dingtalk-helper.md`），由 `reply.py` 经 `extra_args={"agent": "dingtalk-helper"}` 透传 CLI `--agent` 按名加载；
skill 内 `dingtalk-helper-backup.md` 是其干净模板（占位，无私人数据），仅在新机器尚未注册 agent 时兜底注入，随技能一起走、可移植。

可调环境变量：`DRY_RUN=1`（只验证不真发）、`POLL_INTERVAL=秒`（轮询间隔）、`TEST_MODE=1`（生成的回复只发给老板自己，绝不发给原发送人，自测用）、`ONCE=1`（单次轮询后退出，自测用）、`TABLE_GROUNDING=0`（关闭查表 grounding，纯人设回复）。

## 隐私与身份配置（重要）

- **源码不含任何真实身份**：真实姓名、昵称、英文名、城市、`openDingTalkId` 等**一律不硬编码**在 `.py` / 人设 / `.env.example` 里，全部通过私密 `.env` 注入（`SELF_SENDERS`/`MENTION_NAMES`/`BOSS_DISPLAY_NAME`/`SELF_OPENDINGTALK_ID`）。源码默认值只保留中性词"老板"。
- **`.env` 不分发**：已被 `.gitignore` 忽略，切勿提交或随技能打包外发。换机时 `cp .env.example .env` 后自行填写。
- **代码内禁止出现任何真实第三方姓名（含注释/测试/demo）**：老板本人身份走 `.env` 变量（`BOSS_NAME`/`BOSS_COMPANY`/`BOSS_TITLE`/`BOSS_UID`/`SELF_OPENDINGTALK_ID`/`SELF_SENDERS`/`MENTION_NAMES`），同事/名单用中性占位（如「同事甲」）或 `.env` 变量，禁止把真实姓名写进 `.py` 注释、`_validate.py` 测试样例、`SKILL.md` 正文等任何位置。改代码后自查：凡 `温*`/`蔡*`/真实拼音全名等一律清零。
- **人设红线**：真源 `~/.codebuddy/agents/dingtalk-helper.md`（skill 内 `dingtalk-helper-backup.md` 为其干净模板）明确禁止在回复里输出任何系统标识/用户名/英文 ID（如把 `<系统用户名>` 当称呼），也禁止主动透露老板真实姓名/城市/公司等个人信息。

## 人设真源（方案 B：codebuddy 注册 agent 为唯一真源）

**真源 = codebuddy 全局注册 agent `dingtalk-helper`**（`~/.codebuddy/agents/dingtalk-helper.md`），
由 `reply.py` 经 `CodeBuddyAgentOptions(extra_args={"agent": "dingtalk-helper"})` **透传 CLI `--agent` 按名加载**该全局注册灵魂（已实测 18.6s 成功），
含双模式人设（探索 + 直接回复同事）+ 身份红线 + 两表结构；自动代复只走其中「直接回复同事」那一刀。
agent 已注册时 `_resolve_persona()` 返回 None（不重复注入，避免双灵魂）；未注册（如新机器）时退回读 `dingtalk-helper-backup.md` 兜底注入。

> ⚠️ **冷启动注意**：`--agent` 首次调用 codebuddy 会做一次**一次性注册/编译**（解析 `~/.codebuddy/agents/dingtalk-helper.md` 并缓存），
> 那次耗时可达数分钟（实测初调 7~26 分钟无输出，易被误判为卡死/机制损坏）。注册沉淀后，后续调用即 18.6s 秒回，**机制本身正常可用**。
> 切勿因单次冷启动延迟就判定 `--agent` 损坏、擅自改成其它注入方式——复测须在冷启动后二次调用验证。
>
> ⚠️ **冷启动与首条消息（已修复，仍需了解）**：`gen_reply` 对「进程内首次成功生成前的调用」自动使用 `AGENT_FIRST_CALL_TIMEOUT`（默认 1800s），覆盖 codebuddy 一次性注册延迟（实测 7~26 分钟）；
> 首次成功生成后自动切回常规 `AGENT_CALL_TIMEOUT`（默认 240s）。因此**注册后首条真实消息不再被 240s 静默跳过**，会在放宽窗口内等到注册完成并正常代复。
> **可选加速（非必须）**：部署/重装后若想立即热好，可先跑一次 `_validate.py --inject --sender 测试同事 --message 你好` 预热注册（耗时几分钟但不会真发给人），
> 看到「returned in 18.6s」「REPLY >>>」即注册完成；不预热也行，监控首条会在放宽超时内自动等到注册完成。两个超时均可经环境变量 `AGENT_CALL_TIMEOUT` / `AGENT_FIRST_CALL_TIMEOUT` 调整。

- **`_MODE_LOCK`（直接回复同事模式锁）始终注入**：无论 agent 是否注册，`gen_reply` 都把这段强制锁拼进 system_prompt，
  把双模式灵魂锁死在「直接回复同事」模式（你是本公司普通员工、对方是平级同事、不是 boss 本人也不是代笔助理；不许反问/自调 dws/摆领导架子），根治「模型把同事消息当指令、输出『我帮你拟』或替你拍板」的抖动。
- **工具权限统一（黑名单模式，可配置）**：危险工具清单集中在 `runtime.DISALLOWED_TOOLS`（默认 `["Write","Edit"]`，即仅禁用写入；**Bash 已开放**，允许跑 dws 等只读/查询命令、访问本地系统文件），**不再硬编码在 reply.py / vision.py**；两处 SDK 调用统一引用该变量，改一处全局生效。可用环境变量 `DINGTALK_AGENT_DISALLOWED_TOOLS`（逗号分隔）覆盖，如 `"Write,Edit"`。agent 文件已移除 `tools:` 白名单 → 继承 codebuddy 默认工具集（含 WebSearch/WebFetch 联网搜索、Read/Grep/Glob 只读检索、Bash 只读查询），代复时如需查实时信息可直接联网。与 `_MODE_LOCK` 双重锁。**reply.py 与 vision.py 两处 SDK 调用同源锁定**；vision.py 原本漏设 disallowed_tools（等于 Bash 也开）已补上，勿回退。
- **skill 内 `dingtalk-helper-backup.md` = 干净部署模板**：是 `dingtalk-helper.md` 的占位版（无私人数据），随 skill 走；
  移植到新机器、且尚未把 agent 注册进 `~/.codebuddy/agents/` 时，`_resolve_persona()` 自动兜底注入它，换机即开箱即用。
  正式注册：把 `dingtalk-helper-backup.md` 复制为 `~/.codebuddy/agents/dingtalk-helper.md` 即可（`_AGENT_REGISTERED` 检测命中后自动改走真源）。
- **设计红线**：人设只此一份真源（`dingtalk-helper.md`），skill 内只放备份/兜底；改人设只改 `~/.codebuddy/agents/dingtalk-helper.md` 一处。
  旧 `secretary_system_prompt.txt` / `reply_persona_grounded.md` 已删除（内容被 `dingtalk-helper.md` 完全覆盖；
  且前者教模型"自行调 dws"与 `_MODE_LOCK` 的"严禁自己调 dws"直接冲突，留作兜底反而有害）。
- **兜底顺序（agent 未注册时）**：`dingtalk-helper-backup.md` → 硬编码中性话术（不会因缺文件而崩），全程不会双灵魂注入。
- **改动生效需重启监控**（常驻进程不会因 .py 改动热重载）。

### 🧠 知识库调用链路（gbrain MCP，2026-07-29 优化）

旧方案：把产品资料/项目文件/记忆直接铺进 agent 工作空间，靠 agent 用 Grep/Glob/Read 自行读文件取知识——慢、依赖模型主动检索、易漏。

新方案（更快更准，且带保底）：**gbrain 知识库 MCP 服务为知识主入口，工作空间本地文档作保底回退**。
- gbrain 以 **HTTP 单实例**常驻（`gbrain serve --http`，默认 `localhost:3131/mcp`），持 PGLite 写锁；WorkBuddy 连接器与本 skill 的回复 agent **都作为 HTTP 客户端连它**，不各起进程、不抢锁。
- 回复 agent 经 SDK 的 `mcp_servers` 挂上 gbrain（`reply.py` 内 `CodeBuddyAgentOptions(mcp_servers={"gbrain": {"type":"http","url":...,"headers":...}})`），**按需调用** `mcp__gbrain__search` / `mcp__gbrain__query` 做语义检索。
- **⚠️ 事实性问题必须先查 gbrain（不是按需，是必须 · 2026-07-29 修复）**：早版 prompt 写"按需但默认查"，被 `_MODE_LOCK` 的"直接写出回复正文/只输出回复本身/<reply>标签外不写任何字"等强约束压制——agent 把工具调用当成"违反约束"，跳过 gbrain 直接凭记忆答"印象里 N200 Pro 出厂默认波特率是 115200"。现 `_MODE_LOCK` 顶部新增「⚠️ 先查再答 · 任务前置步骤」段，明确"调工具是隐式步骤不展示给同事、不违反最终输出格式"+"禁止凭印象答印象里/我记得/大概是"；`build_knowledge_instruction()` 同步改为"事实性问题必须先查 · 不是按需是必须"；`_looks_like_reply()` 加安全网拦"含糊词+技术参数"回复转人工。**纯闲聊 / 问候 / 安排 / 表态等无需事实依据时，仍直接基于对话上下文作答，不为查而查。**
- **⚠️ prompt 指令与工具挂载状态严格一致（防悬空指令）**：拼进 `_MODE_LOCK` 的知识库指令由 `build_knowledge_instruction()` 动态生成，与 `mcp_servers` 挂载判断**都读 `runtime.GBRAIN_GROUNDING` / `runtime.GBRAIN_MCP_URL` 同一实时来源**——gbrain 已挂载则写「必须先调 gbrain、失败回退本地」；gbrain 未挂载（`=0` 或无端点）则明确写「gbrain 未启用、不要调它，直接走本地文件」。绝不会出现「让 agent 去调一个不存在的工具」的悬空指令。
- 控制开关（均在 `runtime.py`，风格对齐 `TABLE_GROUNDING`）：
  - `GBRAIN_GROUNDING`（默认开，`=0` 关）：关闭则 prompt 切本地文件模式 + 不挂 gbrain 工具，退回纯人设代复（仍保留本地 `产品资料/` `项目文件/` 保底）。
  - `GBRAIN_MCP_URL` / `GBRAIN_MCP_TOKEN`：缺省时**自动从 `~/.workbuddy/mcp.json` 的 `gbrain` 条目读取**（url + Bearer token），单一真源、无需重复填 token；也可用环境变量覆盖。
- `_MODE_LOCK` 与 `dingtalk-helper.md` 均写明「**gbrain 优先（事实性问题必须）、本地文件保底**」：事实性且需要的内容才调 `mcp__gbrain__search`/`query`；**若 gbrain 未接入 / 调用失败 / 超时 / 检索结果为空或明显不对题，回退**到工作空间本地 `产品资料/` `项目文件/` 文档用 Grep/Glob/Read 核实。两路都查不到才如实说「这个我得查下资料确认，稍回你」。本地文件是保底、并非禁用（之前"禁止读本地"的过激限制已撤销）。
- 知识入库：**优先**把产品手册/项目文档/记忆整理进 gbrain（见 gbrain 自身文档）做主检索源；工作空间 `产品资料/` `项目文件/` 文档树**保留作保底回退**，仍随工作空间维护、不要删。

### 🧩 本地代码库检索（CODE_SEARCH_ROOTS / CODE_SEARCH_TOOL，2026-08-04 新增，可选能力）

**解决什么**：同事在钉钉问「源码 / 接口 / 实现细节」类问题（话题名、节点名、参数名、launch/配置文件、具体 .py/.cpp 实现逻辑），gbrain 文档往往没收录或过时 → agent **必须直接检索本地源码库**拿真实实现作答（同属"先查再答"必查项，禁止凭印象）。

**通用设计（不绑定任何特定项目/型号）**：
- 配置全走环境变量（`runtime.py` 常量 + `.env` 注入，源码零硬编码）：
  - `CODE_SEARCH_ROOTS`：分号(;)分隔的本地源码库绝对路径列表；**不填 = 不启用代码检索**（agent 走 gbrain + 本地文档），通用 skill 默认留空，新用户填自己的源码目录即启用。
  - `CODE_SEARCH_TOOL`：代码检索工具 search.py 路径（rg 全文 + ctags 符号定位的封装脚本），默认自动探测 `~/.workbuddy/tools/code-search/search.py`，装到别处可覆盖。
- **工具优先、悬空防护**：`build_code_search_instruction()` 动态生成检索指令（拼进回复 agent 的 system_prompt）——search.py 存在 → 教 agent 用 Bash 调它（`search.py <关键词> --pkg <包名>` 全文 / `--symbol <符号名>` 定位定义，输出「路径:行号:内容」，命中后 Read 精读）；search.py 不存在 → 回退 Grep/Glob/Read 直接搜；两者都没有 → 整段不注入。与 gbrain 指令同读 `runtime` 实时值，绝不悬空。
- 检索优先级：gbrain（文档/语义）→ 本地代码库（真实实现）→ 工作空间文档（保底）。

**search.py 工具安装（可选增强，由部署者自行安装）**：装 ripgrep + Universal Ctags + 一个薄封装脚本 `search.py`（自带 `REPOS` 仓库映射 + `--index` 建 ctags 符号索引 + `--list-repos`），支持 `python search.py 关键词 [--pkg 包名] [--context N] [--max N] [--regex]` / `python search.py --symbol 符号名`。装好后 skill 自动探测并启用；不装也能跑（回退 Grep/Glob），只是大仓检索慢些。

## 运行时初始化：工作空间 / cwd 记忆 / dws 权限 / 项目说明（新用户须知）

首次运行（或新机部署后首次启动监控）会自行重建 cwd 记忆上下文；**但工作空间目录需你手动 `mkdir`（默认 `~/WorkBuddy/dingtalk_auto_reply`，可配 `DINGTALK_WORKSPACE`），记忆不随包分发**：

- **① 工作空间 `DINGTALK_WORKSPACE`（agent 的 `cwd`）**：默认 `~/WorkBuddy/dingtalk_auto_reply`；换路径用 `DINGTALK_WORKSPACE` 环境变量覆盖，**改后需你手动 `mkdir` 建好该目录**（agent 不会自动建）。它只是 agent 的 `cwd`，里面只放 `.workbuddy/memory/`，**不随 skill 分发、不迁移**。
- **② cwd 记忆自动生成（含隐私，禁止迁移）**：agent 以该工作空间为 `cwd` 启动，首次运行**自己拉 `dws` 沉淀**出 `.workbuddy/memory/`（长期 `MEMORY.md` / `KNOWLEDGE.md` + 每日 `YYYY-MM-DD.md`）。记忆内容是 agent 跟老板协作中**自己学出来的私有上下文（含老板隐私）**，**绝不可随包外发或迁到别的机器**；全新机留空，agent 会自行重建。
- **③ dws 权限**：需 `dws patch chmod` 授权 `chat.message:list` / `chat.message:send` / `contact:search`；dws 须已在 PATH（本 skill 的 `gen_launcher.py` 自动追加）。未授权 / 不在 PATH → 监控"活着"却读不到未读。PATH / 会话 / 授权三条的排错详见下文「dws 依赖」段。

### ⚠️ 项目说明 · 新用户不一定用 dws 管项目

`dingtalk-helper.md` 人设里内置的**两表结构 + 「老板钉钉身份」是老板专属配置**（ROS 软件项目表 `<ROS_BASE>`/`<ROS_TAB>`、问题反馈表 `<FB_BASE>`/`<FB_TAB>`、老板 userId `<BOSS_UID>`）。这些真值**只在本机 `.env` 与 `~/.codebuddy/agents/dingtalk-helper.md`**，随包分发的 `dingtalk-helper-backup.md` 已替换为 `<...>` 占位符。**换一个新用户，这些 baseId/tableId/身份大概率不存在**——他未必用 dingtalk 多维表管项目，甚至未必接 dws。

新用户跑起来有两种姿势（skill **不假设项目表存在**）：

1. **纯人设代复（推荐起步）**：设 `TABLE_GROUNDING=0` 关闭查表 grounding，agent 只按【身份红线】以本人口吻回复，不查任何表。最稳，零 dws 项目依赖。
2. **接自己的项目结构**：把 `dingtalk-helper.md` 里「钉钉工作空间 · 已知结构」段改成**自己的** dingtalk Base / 表 / 身份，再注册进 `~/.codebuddy/agents/`；agent 的【自主探索原则】会自己 `dws aitable list` 探明结构后拉数据，不强依赖写死的 baseId。

> 关键：自动代复的核心契约是「以本人口吻直接回复同事」（身份红线），**查表 grounding 是增强项不是必需项**。新用户没项目表也能正常代复，只是少了"结合项目进度回"的能力。

## 📦 迁移 / 重装到其他电脑

skill 目录**自包含**、整目录拷走即可。需要明确的四类外部构件：

| 构件 | 位置 | 是否迁移 | 说明 |
|------|------|----------|------|
| skill 本体 | `~/.workbuddy/skills/dingtalk-auto-reply/` | ✅ 整目录拷 | .py/.md/.env.example 全在里面 |
| 人设灵魂 `dingtalk-helper.md` | skill 内 `dingtalk-helper-backup.md`（**模板**，占位符 `<...>`）| ⚠️ 模板≠真身 | `dingtalk-helper-backup.md` 是**干净模板**（userId/baseId/字段全为 `<...>` 占位，随包分发不含私人数据）。**不要盲目 `cp` 它去覆盖你本机已配置好的 `dingtalk-helper.md`**——那会把真身冲成模板。正确做法：要么直接编辑你本机的 `dingtalk-helper.md` 填自己的钉钉身份/表结构；要么全新机才 `cp dingtalk-helper-backup.md ~/.codebuddy/agents/dingtalk-helper.md` 后**再填真实数据**。不注册也会自动用模板兜底（纯人设代复）。 |
| 工作空间 + cwd 记忆 | `DINGTALK_WORKSPACE/.workbuddy/`（agent 运行时自动加载） | ❌ **禁止迁移** | 工作空间由你手动 `mkdir`（默认路径可配 `DINGTALK_WORKSPACE`）；cwd 记忆由 agent 自己拉 dws 生成/**你移植**、**内含老板隐私**。全新机留空，agent 首次运行自动建空记忆并自行重建上下文，绝不随包分发。 |
| 私密配置 `.env` | skill 内 `.env.example`（`.env` 已被 `.gitignore` 排除） | ⚠️ 不随分发 | 新机 `cp .env.example .env` 后填 `BOSS_UID`/`SELF_OPENDINGTALK_ID` 等。 |

> 路径可移植：`DINGTALK_WORKSPACE`、`BOSS_UID` 均支持环境变量覆盖（`runtime.py` 用 `os.environ.get` + `os.path.expanduser("~")`），换机用户名不同也不会硬编码失效；不设则用默认 `~/WorkBuddy/dingtalk_auto_reply`。

**一步到位脚本（新机）**：
```bash
# 1) skill 本体
cp -r dingtalk-auto-reply ~/.workbuddy/skills/

# 2) 注册人设灵魂（仅全新机；dingtalk-helper-backup.md 是干净模板，cp 后务必填真实数据）
#    ⚠️ 若本机已有配置好的 dingtalk-helper.md，切勿盲目 cp 覆盖——直接编辑它即可。
mkdir -p ~/.codebuddy/agents
cp ~/.workbuddy/skills/dingtalk-auto-reply/dingtalk-helper-backup.md ~/.codebuddy/agents/dingtalk-helper.md
#    # 然后编辑 ~/.codebuddy/agents/dingtalk-helper.md，把 <BOSS_UID>/<ROS_BASE> 等占位填成你自己的钉钉身份与表结构

# 3) 私密配置（不随包分发，新机自建）
cp ~/.workbuddy/skills/dingtalk-auto-reply/.env.example ~/.workbuddy/skills/dingtalk-auto-reply/.env
#    # 编辑 .env 填 BOSS_UID / SELF_OPENDINGTALK_ID / CODEBUDDY_API_KEY（如需）

# 4) dws 入 PATH + 生成本机启动器（幂等，无需重登）
cd ~/.workbuddy/skills/dingtalk-auto-reply && python gen_launcher.py
#    工作空间需你手动 mkdir（默认路径见 DINGTALK_WORKSPACE）；cwd 记忆由 agent 首次运行自行重建
```
⚠️ **生效需重启常驻监控**（旧进程不会热重载 .py / 新注册的 agent）。

## 生成回复（CodeBuddy Agent SDK 唯一后端 · 融合查表 grounding + 会话记忆）

`gen_reply(sender, content, …)` 调度逻辑（**唯一后端 = CodeBuddy Agent SDK**，无 CLI 兜底）：
- `_gen_reply_sdk_async`（**唯一**）：`CodeBuddyAgentOptions(extra_args={"agent":"dingtalk-helper"}  # 按名加载 codebuddy 注册灵魂 dingtalk-helper.md（人设真源）, system_prompt=AppendSystemPrompt(append=<查表数据，人设由 --agent 加载>), model=deepseek-v4-flash, permission_mode=bypassPermissions, codebuddy_code_path=<managed codebuddy.cmd>, cwd=<钉钉自动回复工作空间，自动加载该空间记忆>, session_id/resume=dt_<cid>)`；用户消息走 `query` 干净单行（`f"{sender}：{content}"`），system_prompt 用追加模式保留工作空间记忆、用户消息天然分离（无命令行多行坑）。agent 未注册时 `extra_args={}` 且改为把 `dingtalk-helper-backup.md` 兜底注入 system_prompt。
  - 空闲 `SERVER__PORT` 注入 `env` 防 prewarm 端口冲突挂死（0 字节超时根因）。
  - `env` 注入 `CODEBUDDY_INTERNET_ENVIRONMENT=internal`（中国版 deepseek-v4-flash 路由）；`bypassPermissions` 放行后 agent 可自行调 `dws` 补查（事实 grounding 双保险）。
  - 图片消息：`image_paths` 非空时以 Anthropic image 协议内联进 `query`（deepseek-v4-flash 多模态「看图代复一次调用」）。
- **【主回复对象 vs 背景历史 · 2026-07-20 老板纠偏 + 2026-07-30 burst 合并修复】**：消息窗口内累积的 `messages` 列表**必须按时间倒序**（newest 在前，主循环已按 `_msg_ts` 排序+兜底 `sorted` 二次保护）。
  - **【2026-07-30 burst 合并 · 当前主路径】**：取最新对方消息 ts T0，窗口 `[T0 - REPLY_DELAY_SEC, T0]` 内（默认 120s）的对方连发消息**物理合并成一条虚拟主消息**（拼接格式 `[1/N] sender：content1\n[2/N] sender：content2\n...`，按时间正序呈现），作为 AI 的【主回复对象】。背景历史 = 窗口外对方消息 + 老板本人历史发言。AI 看到 main_content 直接就是"对方在延时窗口内连发的全部消息"，prompt 明确告知"请综合理解后给一条统一回复，覆盖核心诉求，不要漏答、不要逐条复述"。**比 prompt 软约束强**：物理合并让 AI 没法只挑最新一条答。
  - **【2026-07-20 旧设计 · single-main 模式 · 仍在使用】**：当窗口内对方消息仅 1 条时走此模式——`msgs[0]` = 对方最新一条 = AI 唯一要回的内容；`msgs[1:]` = 背景历史，仅供了解上下文。强约束"只回主消息、不要复述历史话题"。
  - **两种模式自动切换**：`gen_reply` 内 `_burst_mode` 由"窗口内对方消息 ≥ 2 条"判定，日志区分 `mode=burst-merged` / `mode=single-main`。
  - **跨窗口防话题死循环（仍生效）**：跨窗口（时间差 > REPLY_DELAY_SEC）的对方更早消息归入背景历史、不进 burst；prompt 强约束"不要复述或扩展背景历史里已说过的话题、不要提已被处理过的问题反馈表/项目进度等"。这是 2026-07-20 老板纠偏的核心防波堤，burst 合并只在"延时期内对方连发"这个有限范围内松绑，不动摇跨窗口的硬约束。
  - **设计权衡**：burst 合并后"对方延时期内只要有一条提到'问题反馈'就会触发查表"是**合理的**（对方确实在问，不是历史回顾）；真正要防的"延时期外更早'问题反馈'被 AI 主动接茬"由"跨窗口进背景 + prompt 不复述历史"双重保险。
  - **历史背景**：2026-07-20 老板截图实锤某同事发 5 条消息、最后一条"已经忙到头昏了"AI 还在接茬"问题反馈表我跟进下内容"，根因是老版本把所有 msgs 拼成一个 content 让 AI"综合理解" + SDK resume 加载旧 reply 形成话题死循环。先修成"主/背景分段+只回主消息"；2026-07-30 老板再纠偏"延时期内连发应综合回复"，遂加 burst 合并路径——既保留跨窗口防波堤，又松绑延时期内连发的合并回复。
- **查表事实 grounding（收紧）**：用主消息（burst 合并后是合并全文，single-main 模式下是最新一条）判意图 → `fetch_table_context(意图, session_id)` 拉「本人(userId=<BOSS_UID>)名下未解决项」拼进 system_prompt（带 300s 缓存，同会话不重复拉）。表 baseId/tableId/字段 ID 全部从 `.env` 经环境变量注入（`<FB_BASE>`/`<FB_TAB>`/`<ROS_BASE>`/`<ROS_TAB>` 等），源码零硬编码；不配置则自动退化为纯人设代复。两表在 system_prompt 与回复里明确区分，不混淆。
  - **【关键收紧】主消息二次校验**：table_context 注入 system_prompt 之前会再用 `detect_table_intent(main_content)` 校验一次：主消息（含 burst 合并后的全文）无相关意图 → **丢弃 table_context**（避免"背景历史含'问题反馈'、主消息是'好的谢谢'"时被背景查表结果污染）。注意：burst 合并模式下，对方延时期内只要有一条含"问题反馈"就会判为 feedback 触发查表——这是合理的，对方确实在问。
- **会话记忆（一人一会话连续）**：`session_id = "dt_" + <cid>`；同一对话首轮传 `session_id`，后续传 `resume=dt_<cid>` 续上下文（记忆连续，已实测跨进程 resume 有效）。session 历史里若已回复过某话题，**话题红线**会禁止 AI 再次主动提及（详见 `_MODE_LOCK` 末尾）。
- SDK 不可用/失败 → 返回空（不代发，推微信转人工），无 CLI 兜底。

**关键坑（必读）**：
1. **SERVER__PORT 端口冲突**（最致命）：每次生成分配空闲端口注入 `env["SERVER__PORT"]`，否则 `query()` 0 字节超时。
2. **运行环境必须固定为托管 venv python**（`binaries/python/envs/default/Scripts/python.exe`）：本机 `codebuddy-agent-sdk` 装在 venv 里，用基础托管 python 跑会因 import 失败导致 `_SDK_AVAILABLE=False`。生产 launcher（`gen_launcher.py`）已固定 venv python，自测也要用 venv python。
3. **别"回复自己"**：同前，`_is_self` + `SELF_OPEN_ID` 精确匹配。
4. **⚠️ cmd.exe 8191 字符命令行限制（2026-08-04 实锤，最隐蔽）**：SDK 把 `AppendSystemPrompt` 的内容经 `--append-system-prompt` 拼进 **codebuddy.cmd（批处理）** 的命令行；Windows 执行 .cmd 必须经 cmd.exe，**整条命令行超 8191 字符即报「命令行太长」→ CLI 子进程秒退 → SDK 报 `CLIConnectionError: Connection closed`（0.1s）**。症状极像环境故障，但 CLI `-p` 直连一切正常。**修复=控制注入 system_prompt 的总长**：`_MODE_LOCK + few-shot + build_knowledge_instruction + build_code_search_instruction + 查表数据` 合计须 < ~7900 字符（含基础参数余量，安全值 7000）；2026-08-04 曾因 few-shot 扩容触发，精简后 5699 恢复。**改动任何注入段后必须跑 `python -c` 量总长**（见 reply.py 注释），超限即回退精简；排查「突然全部 Connection closed」先量长度、别怀疑环境。
5. **⚠️ few-shot 只能放 append、不能搬进 agent 灵魂（2026-08-04 实测）**：曾把 few-shot 完整版写进 `dingtalk-helper.md` 灵魂（灵魂经 `--agent` 加载不走命令行、不受 8191 限制），结果 **agent 行为退化——连续 5 次测试不调 search.py/gbrain，凭记忆「回忆模式」直接答**；回滚灵魂 few-shot 段后立即恢复检索（3 次 tool_use + 精确源码细节回答）。**结论**：few-shot 放 append（system_prompt）是行为最强驱动力，灵魂里加重复内容会干扰（疑似模型对「上下文已有示例」产生惰性/缓存效应）。灵魂保持干净。**真源 = reply.py 的 `_FEW_SHOT_EXAMPLES` 常量**（2026-08-04 老板要求内联进代码 prompt，与 `_MODE_LOCK` 同级，不依赖 .md 读取）；`dws-reply-examples.md` 保留为随包分发文档副本（改动同步常量）。**去项目化（2026-08-13）**：常量与文档副本里的代码检索示例已改为中性占位（`<某功能包>`/`<话题A>`），不泄露项目细节；本机真实项目案例放私有文件 `dws-reply-examples.private.md`（已 gitignore、不随包分发），运行时经 `runtime.FEW_SHOT_PRIVATE_FILE` 由 `_load_private_few_shot()` 追加注入——真实示例的驱动效果不退化，通用 skill 又不带项目隐私。
6. **⚠️ 毫秒/秒时间戳混用（2026-08-05 实锤，隐蔽排序 bug）**：dws 的 `lastMsgCreateAt` 是**毫秒**（13 位，如 1584669332376），消息对象 `createTime` 常是**秒级字符串**——两者混用排序差 1000 倍。**症状**：图片消息（PENDING 初始 msgs[0].ts 用 lastMsgCreateAt 毫秒）被误判为"最新"，burst 窗口以它为锚，图片**之后**连发的文字消息（秒级）全落窗外 → 进背景历史 → AI 只回图片不回文字（老板 08-05 反馈）；还导致 `NOTIFIED` 去重失效（job.ts 秒 vs lastMsgCreateAt 毫秒永不相等 → 重复处理/重复推送隐患）。**修复**：`dingtalk_api._norm_ts(v)`（数字 >1e11 判定毫秒 ÷1000 归一化为秒），`_msg_ts` 数字分支与 monitor 的 `last_ts` 统一走它——全链路（PENDING.msgs[].ts / job.ts / NOTIFIED / burst 排序）秒级一致。**凡新增时间字段解析，一律经 `_norm_ts` 归一化**。
- **安全网统一**（防御纵深，别删）：`extract_reply()` 抽 `<reply>`、`_looks_like_reply()` 反拒废话/反问/角色扮演；质量不达标/超时/异常 → 空 → 不代发转人工。
  - ⚠️ **空洞收尾 bug（2026-08-11 修复，全局生成缺陷）**：模型偶发不输出 `<reply>` 标签，输出「完整正文多行 + 结尾一句助理式收尾」（"先这样定方向，有问题随时找我。" / "需要我直接通过钉钉发出去吗？"）。旧 `extract_reply` 兜底规则取【最后一行短句】恰好抓到收尾 → 空洞废话代发（实锤：盘锦丽 2 图案例）。修复：`_TAIL_SKIP_RE`（extract 挑正文行跳过收尾/问句/装饰行，`---` 等装饰行剔除）+ `_EMPTY_REPLY_RE`（质检只拦"整条=空洞收尾"，含信息的正常回复如"具体我下午发你。有问题随时找我。"不误伤）。  改这两处正则时用 `_validate.py` 或本地 10 用例单测回归（空洞收尾拒 / 正文+收尾抽正文 / 正常回复不误伤 / <reply> 正常）。
  - ⚠️ **「含老板」误伤 bug（2026-08-22 修复，正常回复被拦转人工）**：旧 `_looks_like_reply` 规则「回复含'老板'即拒」（假设真人回同事不会写"老板"）把**同事间正常提及老板**全误杀——08-21 蔡达轩「跟老板定的时候好对着看」、朱文杰「今晚来得及给老板汇报」两条正常草稿因此被拦（老板反馈「生成没问题为什么没正常回复」）。实锤：`"老板" in text` 一刀切是错的，同事聊到"老板"时老板本人回应提"老板"完全正常。修复：只拦「**老板+称呼标点**」开头（`^\s*老板[，,：:！!？?]`）——那才是模型对老板说话的角色扮演；指代/转述形态（跟老板定/给老板汇报/老板说的/老板说）全部放行。**教训：质检规则的"假设"要拿真实业务场景验证，一刀切关键词拦截必误伤。**
  - ⚠️ **标签残留 bug（2026-08-14/08-19/08-20 三轮修复，回复出现代码/乱码；真根因第三轮才定位）**：deepseek 偶发把**内部工具调用协议标记 `｜｜DSML｜｜`（全角竖线 U+FF5C）泄漏**进回复输出，codepoint 级实锤形态：`<reply>正文</｜｜DSML｜｜reply>`、`正文。</｜｜DSML｜｜parameter>`、`</｜｜DSML｜｜tool_calls>`（历史 6 条全为此形态）。⚠️ **前两轮修复（08-14 reply 变体 / 08-19 结尾标签剥除）全部无效**——正则要求 `<` 后紧跟 `/` 或字母，被 `｜｜DSML｜｜` 中缀骗过；且当时测试用例是手打的 `</parameter>`，**从未测过真实字符**（显示层把全角竖线看丢了）。**根治（08-20）**：`extract_reply` 入口 `re.sub(r"[｜|]{2}\s*DSML\s*[｜|]{2}", "", t)` 直接删协议标记（正文不可能合法含它），使 `</｜｜DSML｜｜parameter>` 规范化为 `</parameter>`，前两轮的剥除/拦截防线（`_strip_reply_tags` 结尾剥 + 质检三道）随即全部生效；`_looks_like_reply` 再加 DSML 标记兜底拦截（含孤立标记）。回归用例见 `_validate.py --test-regex`（**真实字符用例含全角竖线，自检 U+FF5C，勿改成半角**）。**血泪教训：①定位乱码必须做 codepoint 级逐字符验证，肉眼/repr 会看丢全角字符；②测试用例必须从真实日志原样复制，手打简化字符=测了个寂寞；③「修复后仍复发」优先怀疑「测的不是真实字符」。**
- **TEST_MODE=1**：生成的回复只发给老板自己（钉钉「自己」会话 `send_reply_self` + 微信 ClawBot `push_weixin`），**绝不发给原发送人**。自测用，验证效果不冒犯同事。详见 `_validate.py --inject`。

## 抢答防护（延迟窗口 + 老板活跃检测）

**问题**：发现单聊未读后立即代发，会抢老板自己的回答（老板正拿着手机准备回，AI 已代回）。

**方案**：发现未读不立即发，走「延迟 + 活跃检测」两步：
1. **活跃检测（发现即查）**：`owner_recently_active(cid)` 拉该会话最近消息，看老板最近 `ACTIVE_WINDOW_SEC`（默认 300s=5分钟）内是否在该会话发过消息（`SELF_OPEN_ID` 精确匹配）。活跃 → 跳过不代发（老板在跟，会自己回）。
2. **延迟窗口**：不活跃 → 进 `PENDING` 等 `REPLY_DELAY_SEC`（默认 120s=2分钟）。
   - 窗口内每轮（轮询间隔）持续检测老板是否活跃，活跃则取消代发。
   - 窗口到期再次确认仍不活跃 → 真正代发（`gen_reply`+`send_reply`+审计+微信通知）。
3. 老板在窗口内自己回了该会话 → 活跃检测命中 → 代发取消，**绝不抢答**。

**可调环境变量**（默认已配好）：
- `REPLY_DELAY_SEC=120`：延迟窗口时长（秒），给老板自己回的时间。
- `ACTIVE_WINDOW_SEC=300`：老板活跃判定窗口（秒），最近 N 秒在该会话发过消息算"正在跟"。
- `TEST_MODE=1`：生成的回复只发老板自己（钉钉自己会话 + 微信），不发原发送人；自测上线前验证用。
- `ONCE=1`：单次轮询后退出，自测用（不常驻）。
- `TABLE_GROUNDING=0`：关闭查表 grounding（纯人设回复，排查用）。

**效果**：既给老板充足回复时间，又从根上避免"老板正在聊却被 AI 抢话"。群聊/媒体无文本/生成失败仍走原"不代发转人工"逻辑，不受影响。

## 群聊推送过滤（默认只推 @我/@all）

**问题**：早期实现把**所有**群消息都推到微信——普通群刷屏、@别人的消息、特别关注的人发言全都会打扰老板。老板只关心"有人@我"这类真正重要的群消息。

**接口事实（已实测）**：
- `list-unread-conversations` 和 `chat message list` 的**单条消息对象里没有 `@我` 结构化字段**（`atUsers`/`atDingTalkIds` 都不返回）；群消息里 @ 某人只表现为内容前缀纯文本 `@昵称`（如 `@同事A 已经试过了`）。
- dws 另有服务端权威接口 `chat message list-mentions --group <cid>`（只返回 @我 的消息），但空群返回无 `messages` 字段的空结果，结构不稳定，不适合做热路径每轮轮询。
- **钉钉"特别关注"联系人列表 dws 拿不到**，无法按"是否特别关注"精确过滤；因此用"是否 @我/@all"这个可识别维度来收敛群推送。

**方案（内容启发式，零额外 API 调用 + `GROUP_PUSH` 策略开关）**：
- `group_msg_is_at_me(content)` 判据（⚠️ 2026-08-05 修复：由「仅开头单@」放宽为任意位置子串匹配）：
  1. 内容含 `@所有人` / `@all`（词边界）/ `<@all>`（dws 发送占位）→ 必然含老板 → `True`；
  2. 内容【任意位置】含 `@昵称`（命中 `MENTION_NAMES`）→ `True`——兼容句首/句中/句末、多个 @ 连排、`@@昵称` 双 @ 格式；
  3. 其它（普通群消息、@别人、特别关注发言、媒体无文本）→ `False`。
- **群聊微信推送按 `GROUP_PUSH` 策略**（仅作用于群消息；单聊代复+提醒不受影响）：
  - `atme`（**默认**）：仅 `at_me=True`（@我/@all）才推微信；其余群消息**静默跳过，不推**。
  - `all`：所有群消息都推（旧行为）。
  - `off`：群聊完全不推微信（连@我都不推）。
  - 命中推送的消息标签为 `🔔 钉钉新消息（群聊·有人@你）`，一眼区分。

**配置**：
- 老板群昵称候选 `MENTION_NAMES`（源码默认仅 `老板`；真实群昵称在私密 `.env` 配置），群昵称特殊时覆盖：`MENTION_NAMES="你的昵称,你的简称"`。
- 群推送策略：`GROUP_PUSH=atme`（默认）｜ `all` ｜ `off`。

**局限**：纯展示名匹配，若群里恰好有人昵称与你相同会误判（极罕见）；如需 100% 服务端权威，可改用 `list-mentions` 二次确认（见上"接口事实"），当前为成本/可靠性权衡选择启发式。

### 🧪 群聊 AI 草稿预览（GROUP_REPLY_PREVIEW，2026-08-05 新增，可选能力，默认关）

**解决什么**：老板想验证「群聊 @我 也能 AI 生成回复」的效果，但**红线是不在群聊替老板发言**——所以做成**草稿预览**：生成后绝不发钉钉群，只推微信给老板看，验证期后再决定是否开放真代发。

**机制**（复用单聊 PENDING 状态机，零新状态）：
- 触发：`GROUP_REPLY_PREVIEW=1` 且 群聊 @我（at_me）且**有文本**（纯图片 @我 保持现有通知，不预览）。
- 流程：进延迟窗口（`REPLY_DELAY_SEC` 2min，与单聊一致）→ 窗口内活跃检测（老板在群里则取消）→ 窗口内消息累积为背景历史（`_fetch_recent`，含老板历史发言标记 is_self）→ 到期 `gen_reply` 生成（session `dt_<cid>` 记忆连续，支持查表/知识库/代码检索全链路）→ **只 `push_weixin` 推草稿**（标签「🔔 钉钉群聊·AI 草稿（未发送）」，附群名/@我的人/原文/草稿），**绝不调用 `send_reply`**。
- job 标记 `preview_only=True`；分发处 `if job.get("preview_only")` 走预览分支（微信推送失败复用 `_pending_after_send` 重试语义）。
- 生成失败 → 推微信「群聊 @你 · AI 草稿生成失败」转人工。
- 配置：`.env` 填 `GROUP_REPLY_PREVIEW=1`（默认 0=关，通用安全）。验证期后若要真代发，再评估放开（需额外确认群聊口吻/权限）。

## 图片识别（群聊 @我 / 单聊图片补全内容）

**问题**：钉钉图片消息不是"无文本"——mediaId 内嵌在 content 里（`[图片消息](mediaId=@lQLP...)`），常带文字说明+@人。原逻辑把图片当"(图片/媒体消息)"丢弃，老板既看不到图里是什么，也修不掉"图片被误当纯文本代复"的隐患（content 含 mediaId 噪音，喂给 AI 会乱回）。

**实现**：
- `extract_media_ids(content)`：正则提取所有图片 mediaId（一条消息可能多张，最多取前 4 张）。
- `clean_text_for_ai(content)`：去掉 `[图片消息](mediaId=...)` 噪音，保留纯文字说明，作为 AI 上下文（修掉误代复 bug）。
- `download_images(...)`：调 `dws chat message download-media` 把图下到 `_media_cache/`（路径必须用 Windows 原生反斜杠绝对路径，否则底层 Go 组件误解析 `/c/` 导致落盘失败）。
- `describe_image(path)` + `describe_images(paths)`：**复用 CodeBuddy Agent SDK 多模态**（与 `gen_reply` 同一后端、同一视觉模型；把图 base64 内联进 SDK query，实测可准确读出文字/颜色/图形，文本落在 `AssistantMessage/TextBlock`，抽取方式与 `gen_reply` 完全一致）。视觉模型默认跟随文本主模型（`CODEBUDDY_MODEL`），可用 `VISION_MODEL` 单独指定 CodeBuddy 侧视觉模型。返回中文描述。主要用于**群聊 @我 通知**和**单聊不代复时让老板知道图里是什么**。
- 群聊：**仅 @我 时**识别（避免群刷图烧视觉额度），结果补进微信通知 `🖼️ 图片内容：XXX`（`describe_images` 1 次调用）。
- 单聊**代复**：有图且 `AUTO_REPLY_IMAGE` 开启（默认开） → 把图以 image 协议**直接内联进 `gen_reply` 的 deepseek-v4-flash 调用**（识别+代复 **1 次调用**完成，不再先 `describe` 再代复的二次调用）；失败/质量不达标仍走安全网不代发。单聊**不代复**（开关关，`AUTO_REPLY_IMAGE=0`）时则只走 `describe_images` 1 次拿描述补通知。
  - ⚠️ **多图提示语（2026-08-11 修复，图片+文字结合混淆）**：`gen_reply` 的带图提示由 `_build_img_hint(n)` 生成——**动态图片数量 + 顺序说明**（"附了 N 张图片，按发送先后依次为 图1、图2…；逐张看图 → 对照文字里"这个/那个/如图"等指代判断对应哪张图 → 对不上如实说"这个我得看下图确认下"，不硬答"）。改提示语改 `reply.py::_build_img_hint` 一处，**勿再写死"一张图片"**。

**降级**：CodeBuddy Agent SDK 不可用（`_SDK_AVAILABLE=False`）→ `VISION_ENABLED=False` → 不识别、不下载图片，微信通知里图片只显示 `(图片/媒体消息)`，**不报错、不阻断**。只要 SDK 可用即开箱即用识别，无需任何 key。

**配置**：视觉后端默认与文本回复同一套 CodeBuddy SDK（零配置、无需任何 key）；视觉模型默认跟随 `CODEBUDDY_MODEL`，可用 `VISION_MODEL` 单独指定 CodeBuddy 侧视觉模型。单聊图片自动代复开关 `AUTO_REPLY_IMAGE`（默认开，设 `AUTO_REPLY_IMAGE=0` 可关闭）。

## 健壮性要点

- **日志心跳**：每 ~120s 打一行 `[heartbeat] alive, unread_now=N`（带 dws 健康标记：`empty`=真无未读、`dws_unhealthy!`=dws 挂了），无未读也打——一眼区分「真无消息」vs「dws 坏了伪装健康」；连续 6 次失败（约 12 分钟）自动推一次微信异常提醒（节流 30 分钟）。详见下方「读取日志」。
- **启动静默 seed**：首轮把当前未读时间戳记进去重表，只对启动后新到的消息回复，不 retro 回复历史未读。
- **去重键用 `lastMsgCreateAt`**（媒体消息 `openMessageId` 可能为空，不能做去重依据）。
- `DRY_RUN=1` 环境变量：只生成+打印，不真发回复/不推微信，用于验证。
- 仅单聊自动回复；`SKIP_SENDERS` 可配置不代发的名单（家人/上级）。
- **生成失败/媒体消息不代发**：AI 生成失败、质量不达标（`_looks_like_reply` 拒绝）、或媒体消息无文本时，**绝不发兜底话术**（避免对方以为老板看到了其实没看到），只推微信「需手动处理」转人工。**单聊**即使质检拦下也会把 AI 生成的草稿原文一并带进微信通知（不代发到钉钉，但让老板看到草稿、便于手动补发）。
- **审计日志**：每次代发/跳过都写 `~/.workbuddy/dingtalk_auto_audit.jsonl`（每行一个 JSON：时间、会话、发件人、内容、回复、发送结果）。以本人身份发消息是高风险对外操作，必须可追溯。
- **发送成功判断**：`_dws_ok()` 解析 dws 返回的 JSON 看 `success`/`errcode`，空输出/含 error/errcode≠0 都判失败；不再用"不含 error 即成功"的弱判据。
- **启动 seed 不吞消息（防"毫无反应"）**：首轮把未读时间戳记进去重表（不 retro 回复历史），但对「24h 内到达」的单聊未读**发一次被动微信提醒（仅提醒、不代复）**——downtime 期间到达的消息重启时不再被静默吞掉。
- **单实例锁**：`~/.workbuddy/dingtalk_auto.lock` 存 PID（原子 `O_CREAT|O_EXCL` 创建，避免竞态），启动检测到锁里 PID 还活着则立刻退出（杜绝同条消息双发）；锁里是陈旧 PID（进程已死）则接管。
- **日志轮转**：`dingtalk_auto_debug.log` 超 1MB、`dingtalk_auto_audit.jsonl` 超 512KB 自动重命名为 `.1`（保留一份回溯），常驻进程下不再无限撑爆磁盘。
- **图片缓存清理**：每 200 轮自动清 `_media_cache/` 下超过 7 天的图片，防常驻下缓存无限增长。
- **主循环韧性**：外层 `try/except` 包裹整轮；`get_unread()` 等持续失败时按次数退避（每次 +10s、上限 120s）避免热循环狂刷日志；异常被捕获后下一轮继续，监控不会"死掉"。

## 运行

> **Python 环境（固定）**：必须用装了 `codebuddy-agent-sdk` 的 **default venv** python（SDK 主后端依赖它）。WorkBuddy 上即该 venv：
> Windows `%USERPROFILE%\.workbuddy\binaries\python\envs\default\Scripts\python.exe`；macOS/Linux `$HOME/.workbuddy/binaries/python/envs/default/bin/python3`（下文统称 `$PY`）
> 生产 launcher（`gen_launcher.py`）已固定此 venv python。若 SDK 不可用，脚本直接走「不代发」（无 CLI 兜底）。

```bash
# Windows
PY="$USERPROFILE/.workbuddy/binaries/python/envs/default/Scripts/python.exe"
# macOS / Linux
PY="$HOME/.workbuddy/binaries/python/envs/default/bin/python3"

# 0) 自测（集成验证，不真发回复；会真实调一次 SDK 生成）
"$PY" ~/.workbuddy/skills/dingtalk-auto-reply/_validate.py

# 1) 先验证（不发真实回复、不推微信）
DRY_RUN=1 "$PY" ~/.workbuddy/skills/dingtalk-auto-reply/dingtalk_unread_monitor.py

# 2) 真实运行（会以本人身份发钉钉 + 推微信）
"$PY" ~/.workbuddy/skills/dingtalk-auto-reply/dingtalk_unread_monitor.py
```

> **dws 环境变量**：监控本体走绝对路径，但为让你手动用 `dws` 及兜底 `DWS_CMD`，本技能 `gen_launcher.py` 会自动把 dws/node 目录追加进用户 PATH（详见下方「dws 依赖」段）；手动补 PATH 亦见该段。

### ⚠️ CodeBuddy 认证（启动前必读）

脚本**启动即做认证健康检查**，未通过会打印醒目提示并退出（exit 2），不会悄悄空跑：
- **API Key（推荐无人值守）**：`.env` 填 `CODEBUDDY_API_KEY=你的key`（申请：https://copilot.tencent.com 控制台）→ 用 Key 直连，不依赖交互登录。
- **CLI 已登录凭据（零配置）**：留空 Key，脚本自动复用你终端 `codebuddy` 登录过的凭据。
- 都没 → 退出码 2，提示二选一：①终端运行 `codebuddy` 完成登录；②在 `.env` 填 `CODEBUDDY_API_KEY`。
- 中国版自动适配：脚本检测 `~/.codebuddy/local_storage` 是否标记 `internal`，自动注入 `CODEBUDDY_INTERNET_ENVIRONMENT=internal`，无需手动配。

> 脚本**绝不代填/存储你的登录凭据**，只检测"是否已登录"并给提醒——认证动作由你本人在终端完成。首次启动前请先确认已登录（终端跑一次 `codebuddy` 或填 Key），未登录会打印提示并以退出码 2 退出，绝不代发。

## 部署方式

> WorkBuddy 桌面客户端不能作为后台常驻进程；但本脚本是独立 Python 进程，可自行后台常驻轮询。生成回复走 Python SDK（即起即退的子进程），不依赖 WorkBuddy 桌面客户端运行。

### Windows · Startup 启动器（推荐）

启动器 `.vbs` **不随技能分发**（见上方移植说明，已被 `.gitignore` 排除），由本机 `gen_launcher.py` 生成到 `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\`。两种落地方式，任选其一（或都做）：

```bash
# 方式 A：手动生成一次（推荐，部署时执行）
"$PY" ~/.workbuddy/skills/dingtalk-auto-reply/gen_launcher.py
# 方式 B：什么都不做 —— 监控脚本首次运行会自动自检并生成（日志可见 [launcher] 行）
```

- 生成后双击即可手动拉起；放进「启动」文件夹则每次登录自动运行（生成器已写到该位置）。
- **自带崩溃自愈看门狗**：常驻循环每 30s 探活 `dingtalk_unread_monitor.py` 的 python——进程不在立刻拉起；进程在但调试日志超 180s 未更新（卡死/静默空转）则杀掉重拉，~30s 内自愈，无需重登。
- **单实例锁**（见上方「健壮性要点」）双重保险，重复启动自动退出，杜绝双发。
- 生成器以 **纯 ASCII** 写 `.vbs`（全英文注释），Windows Script Host 读取零风险。
- 看门狗逻辑唯一可信源即生成出的 `dingtalk_auto_reply_launcher.vbs`（由 `gen_launcher.py` 的 `VBS_CONTENT` 常量生成，改动请以改 `gen_launcher.py` 为准，勿手改运行中的 `.vbs` 以免漂移）。

> ⚠️ **为什么不用 Windows 计划任务**：计划任务把脚本跑在**隔离会话**里，该会话**无网络出口、也拿不到 WorkBuddy 宿主本地服务** → `dws` 连不上后端、每次 `get_unread` 超时返回空 → 日志只剩启动 banner、看不到 `raw unread`、不会代复（进程活着 CPU≈0 却不工作）。Startup 启动器在**登录后的交互式会话**（与 WorkBuddy 宿主同会话、有完整网络）拉起，从根上避开。故计划任务方案已弃用，不要再注册。

> 🔴 **窗口样式与 dws 访问无关（2026-07-15 老板纠偏）**：VBS 拉起监控的窗口样式 `N`（0=隐藏 / 1=普通 / 2=最小化）**不影响 dws 能否拿到未读**。能否拿到未读只取决于「dws 在系统 PATH」+「跑在登录后的交互式会话」（见上方「为什么不用 Windows 计划任务」与下方「dws 依赖」两段），与隐藏/最小化无关。之前"隐藏窗口会摘出会话导致 dws 返回空"是错误猜想，真实根因是 dws 当时没进 PATH。

### macOS / Linux

```bash
nohup python ~/.workbuddy/skills/dingtalk-auto-reply/dingtalk_unread_monitor.py \
  > ~/.workbuddy/dingtalk_auto_daemon.log 2>&1 & disown
```

### 手动 start / stop

- 启动：直接 `python dingtalk_unread_monitor.py`（前台 `python` 调试；正式运行由 VBS 启动器以 `python.exe` 隐藏窗口拉起）。
- 停止（Windows）：`stop_monitor.ps1`（精确结束本脚本 python，不动其它 python）。
- 停止（macOS/Linux）：`pkill -f dingtalk_unread_monitor.py` 按 PID 杀。

## 消息查找能力现状（2026-08-03 严谨验证，改查找逻辑前必读）

跨单聊+群聊查找历史消息，**可靠手段 = 按人 / 按会话枚举**；**`+search-msg` 关键词全量搜索当前不可用**（见下证据）。

| 需求 | 命令 | 状态 |
|---|---|---|
| 按人拉消息（含单聊+群聊） | `dws chat message list-by-sender --sender-user-id <userId> --start/--end` | ✅ **可靠，首选**（agent 查同事记录就用它） |
| 枚举全部会话（含单聊+群聊） | `dws chat list-all-conversations --limit N` | ✅ 可靠（实测 15 个会话） |
| 按会话拉消息 | `dws chat message list --group <cid> --time/--direction older` | ✅ 可靠 |
| 按关键词全量搜索 | `dws chat +search-msg --query "词" --start/--end` | ❌ **接口在但当前不命中** |

**`+search-msg` 不可用的验证证据（2026-08-03，已排除授权/数据缺失/时间窗）：**
- 定向群搜「MS42DDC」「步进电机」（词确认 7/31 真实出现在该群，`list` 已拉到）→ `count=0`
- 按发送者搜同事乙（确认 7/31 发过 2 条）→ `count=0`；对照 `list-by-sender` 同条件 → 命中 2 条
- `--verbose` 全程无报错；`dws chat data-auth cross-org --all --ttl 24h` 授权后重测仍 0
- `chat.message:search` / `chat.message:list` scope 授权尝试 → `unknown scope`（INVALID_SCOPE）
- **结论**：疑似服务端全文索引未对当前账号开放/未覆盖单聊与历史消息。**勿再尝试用 `+search-msg` 做热路径**，按人查走 `list-by-sender` 即可。

## dws 依赖（必须满足，不依赖钉钉客户端）

监控**只通过 `dws`（DingTalk Workspace CLI，WorkBuddy 连接器）** 读取未读、发送回复，
**不依赖本机钉钉桌面客户端**（dws 走 WorkBuddy 宿主本地服务，与是否在跑钉钉客户端无关）。
今天实测已石锤：dws 独立工作，之前「unread_now 恒为 0」的真实根因是 **dws 不在系统 PATH 上**，
而非客户端。需满足：
- **dws 已授权**（`dws patch chmod` 授权 `chat.message:list` / `chat.message:send` / `contact:search`）；
- **dws 在系统 PATH 上（User 环境变量）**：终端能敲出 `dws` 即说明已就位；本技能 `gen_launcher.py` 会**自动把 dws/node 目录追加进用户 PATH**（HKCU\\Environment，幂等、写后广播刷新），无需手动配；
- 监控进程跑在**登录后的交互式会话**（与 WorkBuddy 宿主同会话、有完整网络，而非计划任务/服务那种隔离会话）；
- `dws` 取不到未读（返回空/超时）的典型原因：**PATH 缺失**（dws 找不到）、会话隔离（无网）、未授权 → 监控"看着活着"却什么都不做。

  > ⚙️ **关于"读取空"的另一层根因（已实现方案，无需用户操作）**：dws 是 Node 打包二进制，对匿名管道(PIPE)的 stdout 是异步写，进程退出前未 flush → Python `capture_output` 读到 0 字节（与父进程是否控制台无关，python.exe 下同样复现）。监控**统一用文件重定向**（dws 输出写临时文件再读）绕过，每次稳定拿到数据；此实现细节已封装，用户只需保证上方 PATH / 会话 / 授权三条即可。

## 读取日志（诊断）

日志位置（监控以 `python.exe` 隐藏窗口运行，全部写文件，不落 stdout）：
- `~/.workbuddy/dingtalk_auto_debug.log` —— 运行日志（超 1MB 自动轮转为 `.1`）
- `~/.workbuddy/dingtalk_auto_audit.jsonl` —— 代发/跳过审计（超 512KB 轮转）

**如何判断监控健康**（`tail` 最后几行）：

| 日志现象 | 含义 | 处理 |
|---|---|---|
| 每 ~120s 一行 `[heartbeat] alive, unread_now=N, ts=HH:MM:SS` | 正常轮询中（dws 健康） | 无需处理 |
| `[heartbeat] alive, unread_now=0 (empty: 真无未读), ts=...` | dws 健康但当前真无未读 | 无需处理 |
| `[heartbeat] alive, unread_now=0 (dws_unhealthy! fail×N), ts=...` | **dws 挂了**（PATH/授权/会话异常），`unread_now=0` 是假的，消息全漏 | 检查 dws 是否在 PATH / 授权过期 / 钉钉客户端是否在跑；连续 6 次失败（约 12 分钟）会自动推一次微信提醒 |
| 有 `raw unread: [...]`（仅未读集合变化时打印） | 拉到新未读会话了 | 正常，走代复/提醒流程 |
| 只有启动 banner、长时间无 `heartbeat`/`raw unread` | 卡死或掉进无网会话 | 看门狗应在 180s 内自动杀掉重拉；若仍无，检查钉钉客户端是否在跑、网络是否通 |
| `已有另一个监控实例在运行，本进程退出` | 单实例锁生效，重复启动被拒 | 正常，无需处理 |
| `auto-reply monitor started` | 新实例刚拉起 | 正常 |
| 审计日志出现 `skip_reply` / `notify_only` | 主动跳过（老板活跃 / 群非@我 / 生成失败） | 设计内，非 bug |

### 🧠 观察 agent 完整思考/执行过程（DEBUG_AGENT_TRACE=1，2026-08-03 新增）

SDK 是**流式输出**——agent 每一步（思考 → 工具调用 → 工具结果 → 最终回复）都能完整看到。
排查「agent 到底调没调 dws / 查到了什么 / 为什么回复不理想」时，不用猜，直接看轨迹：

```bash
# 自测时前缀环境变量（监控常驻期间开轨迹需重启监控生效）
DEBUG_AGENT_TRACE=1 <venv_python> _validate.py --inject --sender 同事甲 --message "第二期更新你对接同事丙了吗"
```

开启后，每次 SDK 生成会在 `~/.workbuddy/dingtalk_auto_debug.log` 打一段 `[agent-trace]` 多行块：

```
[18:17:28] [agent-trace]
[thinking] 用户问的是…提到了具体同事人名"同事丙"，并涉及"对接/进展"…
[tool_use] Bash input={"command": "dws contact user search --query \"同事丙\" --format json", ...}
[tool_use] Bash input={"command": "dws chat message list-by-sender --sender-user-id …", ...}
[thinking] 查到了真实记录：7月8号同事丙说"好的 这个我弄一下"…
[result] <reply>跟进了，7月8号跟同事丙聊过…基本快好了。</reply>
```

- **block 类型**：`[thinking]`=思考过程、`[tool_use]`=工具名+入参、`[tool_result]`=工具返回、`[result]`=最终 `<reply>`。
- **典型排查**：回复说"还没对接"但轨迹里没有 `[tool_use] dws contact…` → agent 偷懒没查；有 `tool_use` 但没 `tool_result` → dws 命令失败（多半 PATH 问题，见 runtime.build_sdk_env 的 PATH 注入）；有 `tool_result` 但回复没引用 → 口吻/约束问题。
- **默认关**（常驻防刷屏）：环境变量 `DEBUG_AGENT_TRACE=1` 开启，用完整绝对路径 venv python 跑才生效。
- **配合 few-shot**：`reply.py` 的 `_FEW_SHOT_EXAMPLES` 常量（内联进代码 prompt，2026-08-04 起；`dws-reply-examples.md` 为随包分发文档副本）每次调用注入 system_prompt，教 agent「提到人名+对接/进展→先调 dws 查记录再答；源码/接口问题→先调 search.py 查代码再答；回复像老板真人、不暴露查询动作」。代码检索示例已**去项目化**（中性占位），真实项目案例走私有文件 `dws-reply-examples.private.md`（`FEW_SHOT_PRIVATE_FILE`，运行时追加）。

## 自测脚本 `_validate.py`

7 种模式（参数互斥，按需选一）：

- **默认集成验证**：打印所有外部二进制/人设的解析路径（DWS_EXE/DWS_ENTRY/DWS_CMD/NODE/CODEBUDDY_CMD/SEND_JS/SOUL_AGENT 等，确认可移植探测正确）。
- **`--inject`**：手动注入一条假消息跑 `gen_reply`，把回复「发给自己」（`dws chat message send --open-dingtalk-id <自己>`），**绝不发给别人**；想去掉 DRY_RUN 后真发，方便验证生成效果。
- **`--test-guard`**：验证抢答防护逻辑（活跃检测 `owner_recently_active` + 延迟窗口参数），不真发、不触碰任何人会话。自动探测真实单聊 cid，打印活跃检测结果并演示"进窗口→到期代发"（DRY_RUN 下只生成不真发）。
- **`--test-construct`**：回归验证 `gen_reply` 的 prompt 构造（2026-07-20 老板纠偏 + 2026-07-30 burst 合并的关键修复点）。monkey-patch 拦截 SDK 调用，不真发、不耗积分。五个场景：①延时期内对方连发 5 条 → burst-merged 物理合并成 1 条主消息；②单条对方消息问进度 → single-main 模式 + 查表激活；③延时期内对方连发"问题反馈"+"测试" → burst 合并后 table_context 保留（旧"测试丢弃"已被 burst 替代）；④含老板历史发言 → burst 合并对方窗口消息 + 老板历史进背景；⑤跨窗口的"问题反馈"（时间差 > REPLY_DELAY_SEC）→ 不进 burst、当背景历史、不触发查表（防 07-20 旧 bug 复发）。
- **`--test-statemachine`**：验证延迟代发状态机纯函数（`_pending_next_state` / `_pending_after_send` / `_gnotify_next_state` / `_gnotify_after_push`，定义在 `dingtalk_unread_monitor.py`）。不依赖 dws/SDK，纯逻辑断言。覆盖：PENDING/GNOTIFY 的「未到期+活跃→取消」「未到期+重试中不取消」「到期+dws未确认→defer」「defer超限→单聊转人工/群直推」「到期→代发/推送」「发送/推送失败<5次→重试」「失败达5次→放弃」，共 19 条断言。回归「监控主循环状态机偏重」的重构——抽纯函数后行为不变。
- **`--test-mcp`**：验证 gbrain MCP 工具链路（initialize 握手 + tools/list 含 search/query + tools/call search 返回真实内容 + `gen_reply` system_prompt 注入 gbrain 指引），确认知识库通路就绪。
- **`--env`（即 `--check-env`）**：仅做环境预检：核查 SDK / dws / codebuddy CLI / node / 视觉 / 人设 是否就位，逐项打印 `[OK]/[MISSING]/[WARN]`，阻断级缺失给精确修复命令并以退出码非 0 退出；不跑任何生成。

每次自测必跑 **dws 实际调用比对**（默认开 `DEBUG_DWS_CALL=1`）：把「配置的路径（DWS_EXE/DWS_ENTRY/DWS_CMD/NODE 是否存在）」与「`run_dws` 实际选用的路由（DIRECT-exe / NODE-direct / DWS_CMD-fallback / NONE）」和「接口真实返回的字节长度 / 解析出的会话数」三者对齐打印，给 `PASS / WARN / FAIL` 结论；同时把每次 dws 调用的**真实 argv + 返回码 + stdout 长度**写进调试日志（`[dws-call]` / `[dws-route]` 行，数据抓取表现为 `[dws-file] OK out_len=N`）。三条路由输出统一走**文件重定向**（dws 对 PIPE 异步 flush 丢失、Python 读 PIPE 恒空，文件重定向是当前主力方案，与控制台/解释器无关）。排障"dws 找不到/调不通"时，先看这段比对 + 日志里的 argv，一眼定位是 PATH 缺失还是入口解析错。

- 默认模式会调用 `get_unread` 看未读接口是否通；若有单聊未读，继续验证 `get_latest_msg` 字段、`gen_reply` 生成、`reply --dry-run` 命令形态。
- **不真发任何回复**（reply 用 `--dry-run`），但默认模式若有真实单聊未读时 `gen_reply` 会真实调一次 codebuddy 生成文本（仅一次、不发送）；`--test-construct` 用 monkey-patch 拦截 SDK，不真发、不耗积分。
- 当前环境若无单聊未读（只有群聊），默认模式会优雅跳过单聊集成段——符合「群聊不代发」预期，不算失败。

## 漏发补发脚本 `recover_missed.py`

监控曾宕机、或历史某次以 `DRY_RUN=1` 启动过（只生成不真发）导致漏掉的单聊消息，用本脚本手动补发：拉取当前未读单聊 → 用 deepseek-v4-flash 生成本人口吻回复 → **真正发送**并推微信通知。

```bash
# 补发所有漏掉的单聊未读（实时真发）
"$PY" ~/.workbuddy/skills/dingtalk-auto-reply/recover_missed.py
```

⚠️ 会真实以本人身份发消息，仅在你确认"确有漏发"时使用；群聊不代发（只通知），符合全局策略。

## 依赖（移植目标机需具备）

1. **dws CLI**（WorkBuddy 自带）：需授权 `chat.message:list`、`chat.message:send` 与 `contact:search`（后者用于获取本人 openid 以精确识别「回复自己」；用 `dws patch chmod` 授权）。
   - ⚙️ **必须在系统 PATH 上**（关键根因，勿漏）：机制与自动追加见上方「dws 依赖」段。
2. **codebuddy CLI**（WorkBuddy managed node 目录自带）：SDK 的 `codebuddy_code_path` 指向其 `codebuddy.cmd`，SDK 内部 spawn 它来跑 agent；模型 `deepseek-v4-flash`。
3. **codebuddy-agent-sdk**（Python SDK，**唯一后端**）：`pip install codebuddy-agent-sdk`。**必须装到运行脚本的 python 环境**——WorkBuddy managed python 的 default venv（Windows：`%USERPROFILE%\.workbuddy\binaries\python\envs\default\Scripts\python.exe -m pip install codebuddy-agent-sdk`；macOS/Linux：`$HOME/.workbuddy/binaries/python/envs/default/bin/python -m pip install codebuddy-agent-sdk`）。未装则 `gen_reply` 直接返回空（不代发），不会崩溃。
4. **weixinclaw-proactive-push skill**（可选）：用于微信主动推送；未装则自动降级为仅日志。
5. 人设真源 = codebuddy 注册 agent `dingtalk-helper.md`（全局 `~/.codebuddy/agents/`，不随 skill 打包）；skill 内 `dingtalk-helper-backup.md` 是其干净部署模板（占位，无私人数据；随 skill 走、换机兜底）。改人设只改 `dingtalk-helper.md` 一处。

## 配置（`.env`，可选但推荐）

技能目录自带 `.env.example`，移植到新机：`cp .env.example .env` 后按需填写。所有项均可选，留空=自动探测/默认。已存在的系统环境变量不被 `.env` 覆盖。

- **CodeBuddy 认证**：见上方「运行」段的 ⚠️ CodeBuddy 认证（API Key 或 CLI 已登录二选一）。
- **其他可配项**：`POLL_INTERVAL`(轮询秒)、`DRY_RUN=1`(只验证不真发)、`REPLY_DELAY_SEC`(延迟窗口秒,默认120)、`ACTIVE_WINDOW_SEC`(活跃窗口秒,默认300)、`GROUP_PUSH=atme|all|off`(群消息推微信策略,默认 `atme`)、`MENTION_NAMES`(群 @我 昵称候选,在私密 `.env` 配你的昵称)、`SKIP_SENDERS`(不代发名单)、`SELF_SENDERS`(本人昵称)、`AUTO_REPLY_IMAGE`(单聊图片代复开关,默认开)、`VISION_MODEL`(视觉模型,默认跟随文本主模型 `CODEBUDDY_MODEL` 即 deepseek-v4-flash、可单独指定 CodeBuddy 侧视觉模型)、各二进制路径。全在 `.env.example` 有注释。
