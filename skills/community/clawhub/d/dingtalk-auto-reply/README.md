# dingtalk-auto-reply

> 钉钉未读监控 → AI 以本人身份代复 → 微信通知

监控钉钉未读会话：单聊用 AI 以**本人口吻**自动回复（普通员工语气、平级回同事）；群聊 / 指定名单只发微信提醒（**不代发，防社死**）。
回复生成、图片识别统一走 **CodeBuddy Agent SDK**（deepseek-v4-flash），无需任何外部 API Key。

---

## ✨ 特性

- **单聊 AI 代复**：以本人身份、平级同事口吻自动回复，一人一会话、记忆连续。
- **群聊只提醒不代发**：仅当被 `@我` / `@all` 时才推微信提醒，避免群聊社死。
- **事实 grounding**：事实性问题强制先查 gbrain 知识库（失败回退本地文档），禁止凭印象乱答。
- **本地代码库检索**：配置 `CODE_SEARCH_ROOTS` 后，agent 可检索本地源码回答「源码/接口/实现细节」类问题（话题名/节点名/参数名/launch 配置/具体 .py/.cpp 逻辑）；装有 search.py（rg+ctags 封装）时优先用它，未装回退 Grep/Glob/Read。
- **agent 自调 dws 查同事记录**：同事问「跟 XX 对接了吗 / 进展」时，agent 自己用 Bash 调 `dws contact user search` + `list-by-sender` 翻真实聊天记录再答（few-shot 示例内联在 reply.py `_FEW_SHOT_EXAMPLES` 每次注入），不凭印象说"还没对接"。
- **回复像老板真人**：直接说事实、不暴露查询动作、不客服腔、1-3 句；SDK 空返回自动重试 1 次。
- **多模态**：群 `@我` 图片、单聊图片自动识别补全内容，与文本**同一 SDK 后端、零额外 Key**。
- **抢答防护**：延迟窗口 + 老板活跃检测，老板在聊就先不插嘴。
- **健壮性**：心跳健康标记、单实例锁、崩溃自愈看门狗、审计日志、去重、日志轮转。
- **可观测**：`DEBUG_AGENT_TRACE=1` 时日志打 `[agent-trace]` 块，可看 agent 完整思考/工具调用/结果（流式输出）。
- **可移植**：路径零硬编码用户名，整目录拷贝即迁移；代码不含任何真实身份隐私。

---

## 🧱 架构

```
dingtalk_unread_monitor.py   入口：调度主循环（仅 docstring + main + re-export）
runtime.py                   基础/配置层：.env 加载、SDK 探测、路径解析、常量、日志/锁/缓存/审计/鉴权
dingtalk_api.py              钉钉交互层：dws 调用、未读/消息拉取、单聊·群@判定、图片下载、发送
vision.py                    多模态层：图片识别（统一走 CodeBuddy Agent SDK，与文本同后端）
reply.py                     回复生成层：人设 / 查表 grounding / SDK 生成 / 微信推送
```

Pipeline（顺序不可乱）：

1. `dws chat message list-unread-conversations` → 只返回有未读的会话（天然过滤）。
2. 单聊 → 拉最新一条消息（`--direction older --time now`）。
3. **回复生成**：`detect_table_intent` 判断查哪张表 → `fetch_table_context` 拉本人名下未解决项注入 → CodeBuddy Agent SDK 生成回复（`session_id=dt_<cid>` 实现记忆连续）。SDK 不可用时**不代发、转微信人工**。
4. `dws chat message reply --ref-msg-id ... --text ...` 带引用回复。
5. 微信推送（默认 `~/.workbuddy/skills/weixinclaw-proactive-push/send.js`，仅文本；未装自动降级为仅日志）。

---

## 📦 文件清单

```
dingtalk-auto-reply/
├── SKILL.md                      # 技能完整说明（本文是精简版）
├── .env.example                  # 配置样例（cp 为 .env 后填真实身份/Key）
├── .gitignore                   # 隐私黑名单（.env / _media_cache / .vbs 等不随包分发）
├── requirements.txt             # 唯一 Python 依赖：codebuddy-agent-sdk
├── dingtalk_unread_monitor.py    # 入口（调度主循环）
├── runtime.py                    # 配置/路径/日志/锁/鉴权/共享常量
├── dingtalk_api.py               # 钉钉交互（dws / 未读 / 发送 / 图片下载）
├── vision.py                     # 图片识别（CodeBuddy Agent SDK）
├── reply.py                      # 回复生成（人设 / grounding / SDK / 微信推送）
├── gen_launcher.py              # 启动器生成器（本机生成 Startup .vbs，不随包分发）
├── dingtalk-helper-backup.md    # 人设干净部署模板（无私人数据，换机兜底）
├── dws-reply-examples.md        # few-shot 示例：教 agent 调 dws 查同事记录 + 老板口吻（随包分发）
├── _validate.py                  # 自测脚本（7 模式：集成 / --inject / --test-guard / --test-construct / --test-statemachine / --test-mcp / --env，不真发回复；--env 做环境预检）
├── _setup_env.py                 # 安装脚本：探测并写入 SDK 运行环境到 .env
├── recover_missed.py            # 漏发补发脚本（监控宕机/DRY_RUN 后手动补）
└── stop_monitor.ps1             # 精确结束本脚本 python（Windows）
```

> 运行时自动生成（已被 `.gitignore` 排除，不随包分发）：`.env`、`_media_cache/`、`__pycache__/`、`dingtalk_auto_reply_launcher.vbs`、各类日志。

---

## 🔧 环境要求

| 依赖 | 说明 |
|---|---|
| **Python（default venv）** | 跑脚本的解释器；`codebuddy-agent-sdk` **必须装在这个 venv** 里。Windows：`%USERPROFILE%\.workbuddy\binaries\python\envs\default\Scripts\python.exe`；macOS/Linux：`$HOME/.workbuddy/binaries/python/envs/default/bin/python3` |
| **codebuddy-agent-sdk** | 生成回复 + 图片识别的唯一后端 | `venv_python -m pip install -r requirements.txt` |
| **dws CLI** | 拉未读 / 发消息 / 通讯录 | `gen_launcher.py` 自动加入 PATH；`dws patch chmod` 授权 `chat.message:list` / `chat.message:send` / `contact:search` |
| **codebuddy CLI** | SDK 底层起 prewarm server | 随 WorkBuddy 安装 |
| **node** | dws NODE-direct 路由 | 装 Node 并在可用路径 |
| **gbrain MCP（可选）** | 查表 / 知识库；不配则纯人设回复 | `GBRAIN_MCP_URL` / `GBRAIN_MCP_TOKEN`，缺省读 `~/.workbuddy/mcp.json` 的 `gbrain` 条目 |
| **代码库检索（可选）** | 检索本地源码回答「源码/接口/实现细节」问题 | `.env` 填 `CODE_SEARCH_ROOTS`（分号分隔路径列表，不填=不启用）；`CODE_SEARCH_TOOL` 指向 search.py（默认自动探测 `~/.workbuddy/tools/code-search/search.py`，未装回退 Grep/Glob/Read） |
| **SDK 运行环境声明（`.env`）** | 让 skill / agent 识别「用哪个 python 跑」 | 安装时跑 `_setup_env.py` 写入 `CODEBUDDY_SDK_PYTHON` 等 |

> ⚠️ 裸 managed python / anaconda **不含 SDK**，会导致 `_SDK_AVAILABLE=False`。务必用装了 SDK 的 default venv python 跑。

---

## 🚀 安装与运行

```bash
# 固定用装了 SDK 的 venv python（下文统称 $PY）
# Windows:
PY="$USERPROFILE/.workbuddy/binaries/python/envs/default/Scripts/python.exe"
# macOS / Linux:
PY="$HOME/.workbuddy/binaries/python/envs/default/bin/python3"

# 1) 装依赖
"$PY" -m pip install -r requirements.txt

# 2) 探测并写入 SDK 运行环境（关键：让任意 python 拉起都能自拉回正确 venv）
"$PY" _setup_env.py
#   仅预览： _setup_env.py --check     强制覆盖： _setup_env.py --force

# 3) 一键预检（缺啥直接给修复命令）
"$PY" _validate.py --env

# 4) 填私密身份： cp .env.example .env  → 编辑填 BOSS_UID / SELF_OPENDINGTALK_ID 等

# 5) 自测（集成验证，不真发；会真实调一次 SDK 生成）
"$PY" _validate.py

# 6) 真实运行（以本人身份发钉钉 + 推微信）
"$PY" dingtalk_unread_monitor.py
```

### 部署（后台常驻）

- **Windows（推荐）**：`"$PY" gen_launcher.py` 生成 Startup `.vbs` 启动器，自带崩溃自愈看门狗（进程不在/卡死 180s 内自动重拉），放入「启动」文件夹即可登录自启。**勿用计划任务**（隔离会话无网、dws 读不到未读）。
- **macOS / Linux**：
  ```bash
  nohup "$PY" dingtalk_unread_monitor.py > ~/.workbuddy/dingtalk_auto_daemon.log 2>&1 & disown
  ```

### CodeBuddy 认证（启动前必读）

脚本启动即做认证健康检查，未通过以退出码 2 退出（绝不悄悄空跑）：

- **API Key（推荐无人值守）**：`.env` 填 `CODEBUDDY_API_KEY=你的key`（申请：https://copilot.tencent.com 控制台）。
- **CLI 已登录（零配置）**：留空 Key，脚本复用终端 `codebuddy` 登录过的凭据。
- 中国版自动适配：检测 `~/.codebuddy/local_storage` 标记 `internal` 自动注入 `CODEBUDDY_INTERNET_ENVIRONMENT=internal`。

---

## ⚙️ 配置（`.env`）

技能目录自带 `.env.example`，`cp .env.example .env` 后按需填写。所有项均可选，留空 = 自动探测 / 默认。常用：

| 变量 | 说明 |
|---|---|
| `BOSS_UID` / `SELF_OPENDINGTALK_ID` | 老板钉钉身份（必备，用于识别本人 / 查表过滤） |
| `SELF_SENDERS` / `MENTION_NAMES` | 本人昵称 / 群 `@我` 昵称候选 |
| `SKIP_SENDERS` | 不代发名单（家人 / 上级） |
| `POLL_INTERVAL` | 轮询间隔秒 |
| `DRY_RUN=1` | 只生成验证、不真发（调试用） |
| `REPLY_DELAY_SEC` | 延迟窗口秒（默认 120，抢答防护） |
| `ACTIVE_WINDOW_SEC` | 老板活跃窗口秒（默认 300） |
| `GROUP_PUSH` | 群消息推微信策略：`atme`(默认) / `all` / `off` |
| `AUTO_REPLY_IMAGE` | 单聊图片代复开关（默认开） |
| `VISION_MODEL` | 视觉模型（默认跟随文本主模型 `CODEBUDDY_MODEL` 即 deepseek-v4-flash，可单独指定） |
| `TABLE_GROUNDING=0` | 关闭查表 grounding，纯人设代复（新用户推荐起步） |
| `GBRAIN_GROUNDING` | gbrain 知识库开关（默认开） |
| `CODE_SEARCH_ROOTS` | 本地代码库检索路径（分号分隔，不填=不启用） |
| `CODE_SEARCH_TOOL` | search.py 检索工具路径（默认自动探测 `~/.workbuddy/tools/code-search/search.py`） |
| `DINGTALK_AGENT_DISALLOWED_TOOLS` | 危险工具黑名单（默认 `Write,Edit`，可覆盖） |

---

## 🧪 自测脚本 `_validate.py`

| 模式 | 作用 |
|---|---|
| 默认 | 集成验证：打印外部二进制 / 人设解析路径 + dws 实际调用比对 |
| `--env` | 环境预检：逐项 `[OK]/[MISSING]/[WARN]`，缺 SDK/dws 给修复命令 |
| `--inject` | 注入假消息跑 `gen_reply`，回复**只发给自己**，绝不发别人 |
| `--test-guard` | 验证抢答防护（活跃检测 + 延迟窗口） |
| `--test-construct` | 回归 prompt 构造（含 2026-07-30 burst 合并修复），monkey-patch 拦截 SDK，不耗积分 |
| `--test-statemachine` | 验证延迟代发状态机纯函数（19 条断言，不依赖 dws/SDK） |
| `--test-mcp` | 验证 gbrain MCP 工具链路（握手 / tools/list / search 返回 / prompt 注入），确认知识库通路就绪 |

---

## 🛡️ 健壮性要点

- **心跳健康标记**：每 ~120s 打 `[heartbeat] alive, unread_now=N`（带 `empty` / `dws_unhealthy!` 区分真无未读 vs dws 坏了伪装健康）；连续失败自动推微信提醒。
- **单实例锁**：固定本地端口 `127.0.0.1:18733` 绑定（bind 成功者持有），重复启动自动退出，杜绝双发。
- **启动 seed 不吞消息**：首轮记去重表（不 retro 历史），但 24h 内到达的单聊未读发一次被动微信提醒。
- **失败不代发**：生成失败 / 质检拦截 / 媒体无文本 → 绝不发兜底话术，只推微信「需手动处理」。
- **审计日志**：`~/.workbuddy/dingtalk_auto_audit.jsonl` 记录每次代发 / 跳过（高风险对外操作可追溯）。
- **日志轮转 / 图片缓存清理**：防常驻下磁盘撑爆。
- **崩溃自愈看门狗**（Windows 启动器）：进程不在 / 卡死 180s 内自动重拉。

---

## 🔒 隐私与身份

- **源码不含任何真实身份**：真实姓名 / 昵称 / 城市 / `openDingTalkId` 一律不硬编码，全部经私密 `.env` 注入，源码默认只保留中性词「老板」。
- **`.env` 不分发**：已被 `.gitignore` 忽略，切勿提交或外发。换机 `cp .env.example .env` 自行填写。
- **人设真源 = codebuddy 注册 agent `dingtalk-helper.md`**：`dingtalk-helper-backup.md` 是其干净模板（占位符 `<...>`，无私人数据），随包兜底；新机器未注册时自动注入。
- **SDK 运行环境声明（`CODEBUDDY_SDK_PYTHON` 等）非隐私**，可随技能分发；但整个 `.env` 仍被 `.gitignore` 排除。

---

## 📤 迁移到其他电脑

整目录拷贝到目标机 `~/.workbuddy/skills/` 即可。需明确的外部构件：

| 构件 | 是否迁移 |
|---|---|
| skill 本体（整目录） | ✅ 拷 |
| 人设 `dingtalk-helper.md` | ⚠️ 用 `dingtalk-helper-backup.md` 模板填你自己的数据，勿盲目覆盖本机已配置真身 |
| 工作空间 + cwd 记忆 | ❌ 禁止迁移（含隐私，agent 自动重建） |
| 私密 `.env` | ⚠️ 不随分发，`cp .env.example .env` 后填 |

换机后：装 SDK → 跑 `_setup_env.py` 写入 SDK 环境 → `_validate.py --env` 预检 → 填 `.env` 身份。

---

## 📄 License

内部工具，仅供个人使用。
