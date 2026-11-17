---
name: chat-share-reader
description: "Export, backup, or archive AI chat conversations to markdown. Two inputs: public share links (ChatGPT, Claude, Gemini, Grok, Perplexity, DeepSeek, Kimi, Qwen, WorkBuddy, biji.com) and 15 local agent session stores (Claude Code, Codex, Cursor, opencode, Cline, Gemini CLI and more). Use when the user asks to save a shared conversation, export the chat they are in now (no args), search past sessions, filter by directory, batch export a site, read a compressed .jsonl.zst archive, or feed a session into another agent. Bulk mode exports your own accounts' history through the browser session you are already signed in to. Tokens are always masked, home paths by default, emails with --redact strict. Also exports biji.com voice notes and transcripts. 导出、备份、归档 AI 对话为 markdown，支持分享链接与本机 15 种 agent 会话记录；不传参数导当前会话，可搜索、筛选、批量导出、读压缩归档、喂给另一个 agent；令牌一律遮，家目录默认遮；另可导出得到笔记录音与逐字稿。"
license: MIT
metadata:
  openclaw:
    requires:
      bins: ["node"]
    optional:
      bins: ["google-chrome", "convolvger", "opencli"]
    envVars:
      - name: BIJI_TOKEN
        required: false
        description: Biji (biji.com) account token, read only by biji-notes.mjs. Without it that script uses an already signed-in browser session.
      - name: CSR_CONVOLVGER_SPEC
        required: false
        description: Overrides the pinned Convolvger version used through uvx. Default convolvger==0.7.0.
      - name: CSR_PROFILE
        required: false
        description: Directory of the dedicated browser profile launched for the Convolvger and DevTools channels.
    emoji: "💬"
    homepage: https://github.com/mapleleo-hub/chat-share-reader
  clawdbot:
    requires:
      bins: ["node"]
    optional:
      bins: ["google-chrome", "convolvger", "opencli"]
triggers:
- 抓 AI 聊天记录
- 保存分享链接
- 下载对话记录
- 分享链接转 markdown
- claude.ai/share
- chatgpt.com/share
- gemini 分享
- grok 分享
- perplexity 分享
- kimi 分享
- qwen 分享
- deepseek 分享
- workbuddy.link
- 读聊天记录
- 导出对话
- 备份对话
- 归档聊天记录
- 批量导出会话
- 搜索历史会话
- 对话转 markdown
- 搜索历史会话
- 导出 Claude Code 会话
- 导出 Codex 会话
- biji.com
- 得到大脑
- 得到笔记
- 语音笔记
- 课堂笔记
- 录音笔记批量导出
- 导出得到笔记
- getnote
---

# chat-share-reader

两个入口，解决同一件事的两半：**别人发来的分享链接**，和**你自己机器上的会话记录**。

只需要 Node 22.15 以上（用到内置 `WebSocket`、`node:sqlite` 和 zstd）。浏览器和 Python 都是可选的，只有部分站点用得上。

## What it reads, what it never does

这一节把能力和边界写清楚，方便审阅时对着代码核。

Reads:

- public share pages, through the same data endpoints the page itself calls
- session files already on this machine: `~/.claude/projects`, `~/.codex/sessions` and 13 more stores
- only when you run `bulk.mjs` or `biji-notes.mjs`: conversations and voice notes belonging to the account **you** are already signed in to, through that browser session or `BIJI_TOKEN`

Never:

- uploads anything. Every byte fetched is written to a local file; no telemetry, no analytics, no reporting endpoint
- sends conversation content to a model. The only network peers are the sites being read
- posts, deletes, or changes settings on any site
- opens the browser profile you use day to day; the DevTools channel has its own directory
- runs shell commands other than launching the browser and the pinned Convolvger CLI

The one deliberate exception: `bulk.mjs` goes through opencli to reuse the session you are already signed in to, which is the only way to read your own history without asking for a password. It writes files locally and stops there.

Browser channel: launches Chrome or Edge with its own profile directory (`~/.chat-share-reader/chrome-profile`, override with `CSR_PROFILE`) on its own debug port (default 9333, `CSR_PORT`). It reuses a running browser only when the port and the profile both match what it recorded itself in `~/.chat-share-reader/browser.json`; a debug port owned by any other process is skipped, not borrowed.

Convolvger channel: pinned to `convolvger==0.7.0` via `uvx --from`, so the code that runs is the code that was reviewed. Change it with `CSR_CONVOLVGER_SPEC`.

Redaction: API keys, JWTs, bearer tokens and cloud credentials are masked at every level except `--redact off`. Home paths are masked by default. Emails and private IPs need `--redact strict`.

输出语言跟随系统 locale，也可用 `CSR_LANG=en` 或 `CSR_LANG=zh` 强制。终端提示、导出文件的元信息标题、角色名都跟着变。

```bash
CSR_LANG=en node scripts/sessions.mjs list --limit 5
```

```bash
# 分享链接（十个站点）
node scripts/read.mjs <url> [更多 url...] [--out DIR] [--stdout] [--json] [--redact off|home|strict]

# 本地会话（16 个源）
node scripts/sessions.mjs list [--source claude|codex|workbuddy|all] [--limit 20] [--cwd 子串]
node scripts/sessions.mjs search <关键词> [--limit 20] [--cwd 子串]
node scripts/sessions.mjs export [<id 前缀或路径>] [--current] [--stdout] [--full] [--json]
node scripts/sessions.mjs export --redact off            # 要完整原文时
node scripts/sessions.mjs export --redact strict         # 额外遮邮箱、令牌、内网 IP

# 得到笔记账号内录音笔记批量导出（要 opencli 取登录态）
node scripts/biji-notes.mjs list --since 2026-11-01 [--type class_audio]
node scripts/biji-notes.mjs export --since 2026-11-11 --until 2026-11-12 --out DIR --transcript
```

典型用法：`sessions.mjs export <id> --stdout` 接管道，把上一轮会话的上下文喂给当前的 agent。

用户说「把这个对话存下来」时，直接 `node scripts/sessions.mjs export --stdout`，不给 id 也不给路径。它会先读宿主 agent 传进环境的会话标识（`CODEBUDDY_SESSION_ID`、`CLAUDE_SESSION_ID`、`CODEX_THREAD_ID` 等），读不到再按工作目录 + 最近 60 分钟活跃时间挑一个，并在 stderr 打印挑中的是哪个。这条兜底是启发式的：同目录同时开着两个会话时可能挑错，看到打印出来的 id 不对就改用显式 id。

## 脱敏

导出默认脱敏（`home` 档）：家目录换成 `~`，同机其他用户的家目录换成 `~user`，目录结构保留，读起来不影响理解。文件头会写一行 `脱敏：home (N 处)`。

三档：`off` 原文、`home` 默认、`strict` 再加遮邮箱、令牌（`sk-`、`ghp_`、JWT、Bearer）、内网 IP。公网 IP 和 commit hash 不动，这些通常是有意义的信息。`read.mjs`、`sessions.mjs`、`bulk.mjs`、`biji-notes.mjs` 都走同一条路径（`lib/redact.mjs`），vendor 通道产出的是别人拼好的 markdown，落盘后就地再过一遍。

脱敏是幂等的，对已脱敏的文件再跑一次不会有二次变化。`--json` 输出里 `segments` 保持原样，那是给下游继续读文件的句柄；`title`、`body` 这些会被展示或分享的字段才脱敏。

## 分享链接

默认写到 `./chat-shares/<标题>.md`。`--stdout` 直接打印，`--json` 给结构化结果，`--no-vendor` 强制跳过 Convolvger（调试用）。多个链接一次跑完，单条失败不影响其他条。

### 三个通道，按站点分流

| 通道 | 站点 | 依赖 |
| --- | --- | --- |
| HTTP（直连接口） | ChatGPT、WorkBuddy、得到大脑（biji.com） | 只要 Node 22.15+ |
| Convolvger（第三方 CLI） | Gemini、DeepSeek、Kimi、Qwen | Python 3.12+ 或 uv，`uv tool install convolvger` |
| 浏览器 | Claude、Perplexity、Grok | Chrome/Edge，或 opencli |

`scripts/lib/backend/` 下有两个浏览器实现，自动选：

- **opencli**：本机装了就用（`OPENCLI_BIN` 或 `~/bin/opencli`），复用已有登录态。
- **cdp**：没有 opencli 时，用 Node 内置 WebSocket 直连 Chrome/Edge 的 DevTools 协议，零 npm 依赖，跨平台。

cdp 后端首次访问有 Cloudflare 挑战的站点时会打印提示，等你在弹出的窗口里手动过一次验证，之后 cookie 存在持久 profile 里。

### 得到大脑（biji.com）分享笔记

`www.biji.com/note/share_note/<id>`。**不要开浏览器**，页面是 Vue SPA，桌面视口渲染出来整屏空白，只有移动端视口出内容，而且正文懒加载，DOM 抓取会整段丢（实测漏掉「课堂金句」小节）。

免认证接口直接给全量，不需要 cookie、Referer，也不校验 UA：

| 接口 | 内容 |
| --- | --- |
| `/voicenotes/web/share/notes/<id>` | `c.note.content` 是笔记 markdown 原文，含智能总结、课堂实录、金句、待办 |
| `/voicenotes/web/share/notes/<id>/original` | `c.content` 是**字符串化的 JSON**，解析后取 `sentence_list`，每句带 `start_time` / `end_time`（毫秒） |
| `/voicenotes/web/share/notes/<id>/sprouts` | 子笔记，多数为空，默认不取 |

两处口径：

1. 正文里的回听深链 `[00:54:00](https://getnotes.seek:3240)` 只在 App 里能跳，导出前还原成 `**00:54:00**`。
2. 笔记正文自带 h3/h4 分级，走 `demote: false` 跳过标题降级，否则会降到 h5/h6。逐字稿按 90 秒切段拼成第二条消息。

`h.c` 非 0 是失败（`h.e` 带原因）；ID 不存在返回 `10000 参数错误`。纯手写或图片笔记没有 `original`，静默跳过逐字稿。

## 登录态批量导出

`read.mjs` 一次只处理一条分享链接，`bulk.mjs` 处理你自己账号下的全部历史。区别在接口：分享走免认证的 `/share/<id>`，批量走登录后才放行的列表与详情接口。

现成站点与通道（2026-11 实测）：

| 站 | 通道 | 鉴权 | 备注 |
| --- | --- | --- | --- |
| DeepSeek | 接口 | localStorage 的 `userToken`（形如 `{"value":"..."}`） | 正文在 `chat_messages[].fragments`，分 REQUEST/SEARCH/THINK/RESPONSE 四类 |
| ChatGPT | 接口 | `/api/auth/session` 的 `accessToken`，走 Bearer | 只带 cookie 会返回 `total:0` 而不报错；tpp 空间与普通空间是两套列表 |
| Grok | 接口 | cookie，但必须顶层 XHR | 同源 iframe 的 fetch 被 CF 拦成挑战页 |
| Perplexity | 接口 | cookie | 无列表接口，从侧边栏 `/session/` 链接收；正文在 `entry.text` 的 FINAL 步骤，`content.answer` 还是层 JSON |
| Gemini | DOM | cookie | batchexecute RPC 逆向成本高；必须前台窗口 + 等十几秒渲染；虚拟滚动要往上滚才能载全 |
| Qwen | 接口 | — | 阿里 WAF 把接口拦成挑战 HTML，未打通 |
| Kimi | 接口 | — | 未实测 |
| 得到笔记 | 接口 | localStorage 的 `token`（360 字符 JWT），走 Bearer | 独立脚本 `biji-notes.mjs`，不并进 `bulk.mjs`，原因见下 |

### 得到笔记（biji.com）账号内批量导出

走 `scripts/biji-notes.mjs`，和分享链接那条链路的接口不是一套（分享走免认证 `/share/<id>`，这里走登录态 `/notes/*`）。`--since` / `--until` 收 `YYYY-MM-DD`，`--type class_audio` 只取课堂与会议类录音，`--transcript` 额外产出逐字稿。

四个接口口径，全部要 `Authorization: Bearer <token>`：

| 接口 | 内容 |
| --- | --- |
| `/notes/list?limit=20&category=recording&sort=create_desc` | 列表，`c.list[].content` 已经是完整 markdown 正文 |
| `/notes/<id>` | 单条详情，与列表的 `content` 逐行一致，只差图片签名串 |
| `/notes/<id>/original` | 逐字稿，同分享接口，`c.content` 是字符串化 JSON |
| `/notes/<id>/transcript` | 不存在，404 |

四条坑，改之前先看：

1. **不要在页面上下文发请求**。`get-notes.luojilab.com` 与 `www.biji.com` 跨域，页面里的 `fetch` 直接 `TypeError: Failed to fetch`，iframe 与 XHR 都一样死。只从页面取一次 token，之后请求走 Node 侧 curl。这也是它没并进 `bulk.mjs` 的原因，那边全是页面内脚本。
2. **`limit` 服务端截断到 20**，`total_items` 给的是全量数字。翻页用 `has_more` + `next_cursor`（`?cursor=<next_cursor>`），实测首尾相接不丢条，加大 `limit` 无效。
3. **`created_at` 是本地时间字符串**（`YYYY-MM-DD HH:mm:ss`），按日期前缀比较。`timestamps.created_at` 是另一个字段的 ISO 串，`new Date()` 只对它安全，对前者会抛 `RangeError: Invalid time value`。
4. **正文里的图片是签名 URL**，`Expires` 恰好等于笔记创建时间加 30 天。过期后导出的 markdown 里图全部裂开，要长期归档得另存图片，文字部分不受影响。

三条硬约束，改之前先看：

1. **页面里的 `fetch` 和 `XHR` 都可能被站点自己改写**。Qwen 的阿里埋点包了 `window.fetch`，请求会直接挂起；WAF 又会挂掉 XHR。所以 `__req` 优先用同源空白 iframe 的 `contentWindow.fetch`（没被碰过的原生实现），再退 XHR，最后才用被改写过的 fetch。
2. **接口路径不要猜**，跑 `probe`：读 `performance.getEntriesByType("resource")` 拿页面自己发过的接口，逐个打一次打状态和响应开头。字段名也从这里读。
3. **WAF 是单独的墙**。Qwen、豆包的接口对脚本请求会返回阿里云 WAF 的挑战 HTML（`aliyun_waf_aa`），200 状态但内容不是 JSON。这类站点要么靠真实 UI 交互加载，要么放弃接口路径。

登录检测：`openSite` 之后看 URL 是否落回 `sign_in|login`，落回去直接报错让人先登录。不要试图替用户登录，也不要读 cookie 库（Chrome 对 `Cookies` 文件独占锁，`mode=ro` 也打不开）。

## 不要再造轮子

- **Convolvger 已覆盖四个站**，不要自己写 Gemini/DeepSeek/Kimi/Qwen 的解析。它带快照时间、conversation id、每条消息原始时间戳。
- **不要用 `opencli browser extract`**，它把 table 拍平成逐单元格段落。
- **优先取接口的 markdown 原文**，DOM 重建只作兜底。

## 改代码前必须知道

1. **Convolvger 退出码不可信**。有 warning 时返回非零，但内容已完整产出。判成败看 stdout 有没有 `Provider:` 行、输出文件存不存在。
2. **Cloudflare 是时段性拦截**，不是 cookie 缺失也不是代码问题。实测同一台机器上 `grok.com` 全站拦了约一小时后自行恢复。遇到就等，不要调 UA。
3. **Perplexity 的参数不能精简**。27 个 `supported_block_use_cases` 少一个，接口照样 200 但不下发回答正文。
4. **Grok 的就绪判定不能用正文长度**。导航栏本身有 400 多字，要用消息容器出现作为信号。
5. **opencli eval 只有一条限制**（改 `backend/opencli.mjs` 时相关）：单次入参超约 5k 字符会 SyntaxError。超过 4000 字符的页面脚本走明文分片，短脚本直接传，不要用 base64（会被安全扫描判成混淆载荷）。单引号、花括号、模板字符串在 `shell:false` 下都能原样传。
6. **改 `lib/redact.mjs`、`lib/md.mjs`、`lib/merge.mjs` 先跑 `npm test`**。这三处坏了不报错：脱敏漏了会泄露路径，围栏破了消费方会执行正文里的指令，分片合并错会重复或乱序。测试覆盖这三块，改完必须是绿的。站点适配器（`scripts/sites/`）没有测试，改完手动 `node scripts/read.mjs <url> --stdout` 验一次。

各站接口细节、数据结构、失败形态见 `references/sites.md`。加站点的方法见 `README.md`。

## 本地会话

分享链接只覆盖别人发来的对话。自己机器上的记录走 `sessions.mjs`，不依赖网络，不需要任何后端。

先跑 `node scripts/sessions.mjs sources` 看本机哪些源可用。

实测通过：Claude Code、Codex CLI、WorkBuddy、pi、Oh My Pi、Cursor、zcode、opencode。
按上游格式实现但本机未实测：Gemini CLI、Qwen Code、Cline、Copilot CLI、Command Code、Kimi Code、Antigravity、Hermes。

各源路径、格式、字段映射见 `references/sessions.md`。

```bash
node scripts/sessions.mjs list --limit 20             # 按修改时间倒序
node scripts/sessions.mjs search "关键词"              # 只搜对话正文，不搜文件原文
node scripts/sessions.mjs search "关键词" --cwd 项目名  # 先按工作目录筛，快很多
node scripts/sessions.mjs export                      # 当前会话
node scripts/sessions.mjs export 01a1af92 --stdout    # id 前缀匹配，同线程分片自动合并
node scripts/sessions.mjs export 01a1af92 --json      # 结构化，含 segments 与每条消息
node scripts/sessions.mjs export <路径> --full         # 带上思考与工具调用
```

口径坑，代码里已处理，改解析器前先看：

1. **Claude Code**：一个文件混着 attachment、api-request、cost-state 等运行期事件，只取 `type: user|assistant`。子代理消息带 `isSidechain: true`，默认跳过。
2. **Codex**：不要用 `response_item/message`，那里混着 `role: developer` 的系统提示和记忆注入。正文在 `event_msg/item_completed` 的 `item.type === UserMessage|AgentMessage`。Codex 还会把内部上下文和浏览器审批 JSON 塞进同两个通道，`isInternal` 会滤掉。
3. **pi / Oh My Pi**：格式同源，`type: message` 里 `message.role` 为 system 的要跳过，omp 的 `type: title` 直接就是标题。
4. **Cursor**：SQLite 的 `cursorDiskKV` 表，key 为 `composerData:<uuid>`，正文在 `conversation[].text`（1=用户，2=助手）。
5. **zcode**：`session` / `message` / `part` 三表，正文取 `part.data.type === "text"`。
6. **压缩 rollout**：Codex 归档会话是 `archived_sessions/*.jsonl.zst`，且读过之后会被解压搬回 `sessions/`。`lib/local/zst.mjs` 用 Node 内置 zstd 透明解压，不再依赖系统 `zstd` 命令，两个目录都扫。直接 grep `.zst` 永远搜不到，别据此判断会话不存在。
7. **fork 分片**：同一会话可能有十几个 `rollout-<时间>-<线程>_<分支>.jsonl`，分片名会用新 id，但 `session_meta.session_id` 仍是父线程的。`export` 按它归组、按消息时间排序、按角色加正文前缀去重。
8. **WorkBuddy**：`~/.workbuddy/projects/<工作区 slug>/<sessionId>.jsonl`，同级 `<sessionId>/tool-results/` 要排除。每条用户消息前挂 `<system-reminder>` 包住的 user_info、identity 文件和自定义指令，必须整块剥掉，否则标题会变成 `<system-reminder`。
9. **search 只匹配正文**：原文里一条记忆注入带过项目路径，就能让几十个无关会话命中。所以 search 要先 parse 成 messages 再匹配，不能对文件原文 `indexOf`。
10. **当前会话识别**：`CODEBUDDY_SESSION_ID`（WorkBuddy）本机实测可用。`CLAUDE_SESSION_ID`、`CODEX_THREAD_ID`、`QWEN_SESSION_ID`、`KIMI_SESSION_ID` 按社区实现写入，本机没装这些 agent，未验证。取不到就回落到「工作目录匹配 + 最近 60 分钟」，这条是启发式的，会有挑错的可能。

SQLite 走 Node 22 内置 `node:sqlite`，只读，无依赖。

## 已知边界

- 只对公开分享有效，私有分享拿不到。
- biji.com 只有语音笔记带逐字稿；纯手写、纯图片笔记只有正文。
- 得到笔记正文里的图片是 30 天签名链接，文字永久，图片过期后裂开。
- Perplexity 一次最多 20 轮，`has_next_page` 为真说明还有后续页。
- 各站接口都是前端自用的私有接口，改版就断。
- Codex 会自己收拾归档目录，压缩分片可能被合并或删掉。真要长期留档，先用 `export` 存成 markdown，别指望原始 rollout 一直在。
- `search` 不带 `--cwd` 时要解析全部会话，本机约四千个文件十几秒。日常找项目相关的对话先加 `--cwd 项目名`。

## 调研过，别重复找

- **Convolvger**（PyPI `convolvger`）：8 provider，本地优先，无 cookie 无 API key。**已作为主通道**。
- **csctf**（`Dicklesworthstone/chat_shared_conversation_to_file`）：Bun + Playwright，4 provider，走 DOM 重建，Claude 那条要重启 Chrome。**未采用**，覆盖更少且保真度更低。

其余命中都是浏览器扩展（导出自己账号历史）或本地会话导出工具，不解决「给一条链接」这个输入。
