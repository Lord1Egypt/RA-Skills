---
name: game-sentiment
description: >
  Automated game sentiment monitoring skill for mobile/PC games. Scans public feedback across
  multiple channels (Weibo, Bilibili, Zhihu, Tieba, NGA, TapTap, Reddit, X/Twitter, YouTube,
  Discord, Xiaohongshu, game media, etc.), classifies issues, assesses severity, assigns ownership, and
  generates actionable reports with P1 alerts.

  Use when: user asks to monitor game sentiment, create daily sentiment reports, analyze post-update
  player feedback, scan for negative sentiment spikes, do game industry sentiment analysis,
  track player complaints, monitor game reviews, watch for PR crises, check game community health,
  monitor game reputation (游戏口碑), game sentiment monitoring (游戏舆情监测),
  or says things like "帮我看看XX游戏的口碑", "跑一下舆情", "游戏评价怎么样", "玩家在骂什么",
  "游戏口碑怎么样", "做个游戏舆情监测", "monitor game feedback", "what are players saying about",
  "run sentiment scan".

  NOT for: generic brand PR writing, broad industry news without a specific game, one-off web searches
  without structured output, customer service scripting, or non-game product sentiment.
---

## ⛔ MANDATORY RULES (read before anything else)

1. **Step 2 渠道检测不可跳过**：在向用户展示监控渠道列表之前，你必须先实际执行 6 项工具调用检测（Playwright / YouTube key / NGA 凭据 / web_search / IP 封控 / TapTap 可达性），用真实结果填充每个渠道的 ✅/⚠️/❌ 状态。**绝不允许跳过检测直接展示渠道列表**。详见 Step 2 → Action 2a / 2b。
2. **每次执行必须走交互确认**：不得跳过交互直接用旧配置运行。即使已有 config.json，也必须展示配置摘要等用户明确回复"跑"或"好"后才开始采集。未经用户确认不得启动扫描。
3. **采集进度必须反馈**：扫描开始时通知用户，渠道完成时更新进度。
4. **报告质量优先于执行速度**：不设采集超时限制。每个渠道应充分翻页、深入评论区，确保样本量和数据深度足够。宁可多花时间，不可为赶时间跳过数据。
5. **执行前必须读取 references/ 目录下的参考文件**：`channel-strategy.md`（渠道采集脚本）、`report-template.md`（报告模板）、`severity-rules.md`（严重度规则）、`config-schema.md`（配置结构）。这些文件包含具体的 evaluate 脚本和模板，不读会导致采集和报告质量下降。

# Game Sentiment Monitoring

## Overview

Scan configured game's public feedback across channels, produce an **actionable issue-responsibility report** (not just a sentiment dashboard), and push P1 alerts when critical issues are detected.

## Prerequisites

本 skill 的渠道依赖会在 **Step 2 交互流程中自动检测并展示**，用户无需提前手动安装。以下仅供参考：
- **Playwright MCP server**（微博/TapTap/贴吧/B站/小红书/NGA 依赖）：`mcporter add playwright`
- **YouTube API key**（YouTube 渠道）：[Google Cloud Console](https://console.cloud.google.com/apis/credentials)
- **NGA 账号密码**（NGA 渠道）：注册 NGA 论坛账号
- **web_search**（Reddit/X/媒体渠道）：OpenClaw 内置，Gemini 驱动

## First Run — Configuration

**每次触发此 skill 都必须走交互流程**，不得跳过直接使用上次配置运行。

如果已有 `{WORKSPACE}/game-sentiment-data/{slug}/config.json`，展示上次配置摘要让用户确认或修改：
> 📋 上次配置（{游戏名}）：
> - 渠道：{渠道列表}
> - 关键词：{关键词列表}
> - 频率：{频率}
>
> 用这个配置跑？还是要调整？（回"跑"直接开始，或告诉我要改什么）

如果无 config.json（首次），执行完整交互流程：

### Step 1: 识别意图 + 游戏名（唯一必填项）
首次配置时，发送：
> 👋 游戏舆情监控已就绪。我来帮你配置：
> **你要监控哪个游戏？** 告诉我游戏名就行，中英文都可以。

用户回复游戏名后，自动推断别名、品类，发送确认：
> 确认：**{游戏名}**
> 我帮你自动设置了：
> - 别名：{推断的别名}
> - 品类：{推断的品类}
>
> 有需要补充的吗？比如当前版本号、正在进行的活动、重点关注的话题？
> （直接回"没有"我就用默认值继续）

### Step 2: 监控范围（带默认值一次确认）

**⚠️ 强制执行顺序（不可跳过、不可合并、不可简化）：**

**Action 2a — 检测前置条件（必须在展示渠道前完成，不可跳过）**：
依次执行以下检测，每项记录结果。**如果某项检测工具不存在或文件不存在，直接记为"不可用/未配置"，继续下一项**：
1. 检测 Playwright：尝试运行 `mcporter call playwright.browser_navigate` 传入 `url: "https://example.com"`。如果 mcporter 命令不存在或报错 → Playwright 不可用
2. 检测 YouTube API key：尝试读取 `{WORKSPACE}/game-sentiment-data/.credentials/accounts.json`。文件不存在或无 `youtube_api_key` 字段 → YouTube 未配置
3. 检测 NGA 凭据：同上文件，检查 `nga` 字段。无 → NGA 未配置
4. 检测 web_search：执行一次 `web_search("test")`。失败或 429 → web_search 不可用
5. **IP 封控检测**（小红书/知乎/Discord）：对这三个渠道，用 Playwright 访问其搜索页并检查返回内容。如果页面包含 "IP at risk"、"安全限制"、403、验证码拦截等标志 → 该渠道标记为"IP 封控"，自动降级为 web_search。检测 URL：
   - 小红书：`https://www.xiaohongshu.com/search_result?keyword=test&type=1`
   - 知乎：`https://www.zhihu.com/search?type=content&q=test`
   - Discord：`https://discord.com/channels/@me`
6. **TapTap 可达性验证**：用 Playwright 访问 `https://www.taptap.cn`，确认页面正常加载。失败则 TapTap 标记为 ❌ 不可用。

**Action 2b — 根据检测结果生成渠道表格**：
用 Action 2a 的真实结果填充下表（✅ 就绪 / ⚠️ 需配置 / ❌ 不可用），然后展示给用户：

> 默认配置如下，你确认或改：
>
> 📡 **监控渠道**（已自动检测就绪状态）：
> | 渠道 | 状态 | 前置条件 | 说明 |
> |------|------|---------|------|
> | 微博 | {检测结果} | Playwright | 免登录，自动扫描微博搜索结果 |
> | TapTap | {检测结果} | Playwright | 免登录，自动抓取游戏评论区 |
> | 贴吧 | {检测结果} | Playwright | 免登录，自动扫描游戏贴吧帖子 |
> | B站 | {检测结果} | Playwright | 免登录，搜索游戏相关视频和评论 |
> | 小红书 | {检测结果} | Playwright / web_search | 搜索笔记+评论。IP 封控检测通过用 Playwright，被封则自动降级 web_search |
> | YouTube | {检测结果} | API key | 搜索游戏视频+评论。[申请指南](https://console.cloud.google.com/apis/credentials)，启用 YouTube Data API v3，免费 10,000 次/天 |
> | Reddit | {检测结果} | web_search | 通过搜索引擎间接获取 |
> | X/Twitter | {检测结果} | web_search | 同上，与 Reddit、媒体共享 web_search 配额 |
> | 游戏媒体 | {检测结果} | web_search | 扫描 17173/游民星空等游戏媒体报道 |
> | NGA | {检测结果} | 账号密码 | 需要 NGA 论坛账号才能访问帖子 |
> | 知乎 | {检测结果} | Playwright / web_search | 搜索游戏相关问答。IP 封控检测通过用 Playwright，被封则自动降级 web_search |
> | Discord | {检测结果} | Playwright / web_search | 搜索游戏社区服务器讨论。IP 封控检测通过用 Playwright，被封则自动降级 web_search |

**状态值规则**：
- 前置条件满足 → `✅ 就绪`
- 前置条件不满足 → `⚠️ 需配置`
- 前置条件检测失败/出错 → `❌ 不可用`

> _⚠️ 标记的渠道缺少前置条件，会自动跳过。你可以现在就配置：_
> - _YouTube API key → 告诉我 key，我帮你存好_
> - _NGA 账号 → 告诉我用户名和密码，我帮你存好_
> - _Playwright 未安装 → 我现在帮你装（运行 `mcporter add playwright`）_
> - _配好后我会重新检测并更新状态_
>
> _每个渠道的访问方式也可以调整（回"调整渠道"进入详细设置）。_
>
> 🌍 **监控区域**：全球（中文+英文）
> _→ 如果你的游戏只在国内运营，可以改成"国内"，我会跳过海外渠道节省时间_
>
> ⏰ **扫描频率**：每天一次（扫描过去 24 小时的内容）
> _→ 适合日常监控。如果游戏刚更新/出了事故，可以临时切到"每 4 小时"高频模式_
>
> 📋 **报告格式**：中文 Markdown 文件 + 飞书消息摘要
> _→ Markdown 是完整报告（存档用），飞书摘要是精简版直接推到你的聊天里_
>
> 🚨 **紧急告警**：发现严重问题（P1）时立即推送，夜间 23:00-08:00 静默
> _→ P1 = 可能上热搜/大规模影响玩家的严重问题，比如服务器宕机、大规模封号争议、重大安全漏洞。发现这类问题我会第一时间通知你，但深夜不打扰（除非你改静默时段）_
>
> 哪里要改？要提供 API key/凭据？还有其他想加的平台？不改就回"好"。

### Step 2.5: 访问方式调整 + 自定义渠道
如果用户在 Step 2 提出要调整渠道、提供凭据、或添加新平台，进入此步骤：

**访问方式可选表**：
> | 渠道 | 默认方式 | 可选方式 |
> |------|---------|---------|
> | 微博 | Playwright（m.weibo.cn API） | web_search 降级 |
> | TapTap | Playwright（评论页） | web_search 降级 |
> | 贴吧 | Playwright（帖子列表） | web_search 降级 |
> | B站 | Playwright（搜索页） | B站 API（需 cookie）、web_search 降级 |
> | YouTube | Data API v3（需 key） | Playwright（无需 key 但不稳定）、web_search 降级 |
> | Reddit | web_search | 官方 API（需 OAuth app）、Playwright（可能被封） |
> | X/Twitter | web_search | 官方 API v2（需 Bearer token）、Playwright（可能被封） |
> | 游戏媒体 | web_search + web_fetch | Playwright |
> | NGA | Playwright + 登录 | web_search 降级 |
> | 小红书 | Playwright（搜索页） | web_search 降级 |
> | 知乎 | web_search（默认，IP 封控） | Playwright（需住宅 IP） |
> | Discord | web_search（默认，IP 封控） | Playwright（需住宅 IP） |

**添加新平台**：
> 告诉我平台名，我来评估最佳访问方式：
> - **有公开 API 的** → 直接对接（最稳定）
> - **有网页版的** → Playwright 自动化采集
> - **需要登录的** → 提供凭据后 Playwright 登录采集
> - **被封锁的** → web_search 间接搜索（数据不如直连完整）

**如果 Playwright 未安装**（关键依赖缺失）：
> ❌ **Playwright 未安装** — 微博/TapTap/贴吧/B站/小红书/知乎/Discord/NGA 都无法直连（知乎/Discord/小红书仍可通过 web_search 降级）
> 安装命令：`mcporter add playwright`
> 安装后跟我说"好了"，我重新检测。

如果用户提供了自定义渠道，将其加入 config.json 的 `channels` 列表，并在 `references/channel-strategy.md` 中记录访问策略（首次运行时动态探索最佳方案）。

### Step 3: 关键词与竞品（重要，需确认）
基于游戏品类自动生成推荐关键词，**附带解释**让用户理解每类词的作用：
> 🔍 **监控关键词**（根据{品类}自动推荐）：
>
> **风险关键词** — _我会重点搜索包含这些词的玩家讨论，用来发现潜在问题_
> → {外挂, 盗号, 封号, 卡顿 掉帧 闪退, bug 闪退 崩溃}
>
> **排除词** — _包含这些词的内容会被自动过滤，避免广告和无关帖子干扰分析_
> → {陪玩, 代练, 交易, 出售, 收购, 接单, 招人}
>
> **竞品监控** — _填入竞品游戏名，我会在报告中对比玩家是否在讨论"弃坑去玩XX"等流失信号_
> → （空，可选填。例如：PUBG, 无畏契约, CS2）
>
> 你可以：
> 1. 增减风险关键词（比如加"退款""氪金""削弱"）
> 2. 增减排除词（比如你的游戏有官方交易系统，可以去掉"交易"）
> 3. 填入竞品游戏名
>
> 不改就回"好"，或告诉我要加减什么。

**关键词推荐逻辑**（按品类）：
- FPS：外挂, 盗号, 封号, 卡顿 掉帧 闪退, bug 闪退 崩溃
- MOBA：平衡, 削弱 加强, 匹配, 挂机 送人头, 卡顿
- RPG/卡牌：抽卡 保底, 氪金 退款, 剧情, 活动 奖励, bug
- 通用（兜底）：bug, 闪退, 客服, 退款, 差评

### Step 4: 生成配置 + 首次扫描
> ✅ 配置完成，保存到 `{WORKSPACE}/game-sentiment-data/{slug}/config.json`。正在执行首次扫描...

首次扫描完成后，进入 Step 5。

### Step 5: 定时任务与报告推送（首次报告后）
首次报告生成后，询问用户是否需要自动化：
> 首次报告已生成 ✅ 你可以设置自动化（也可以跳过，以后随时手动触发）：
>
> ⏰ **定时扫描** — _设置后我会按固定时间自动跑舆情扫描，不用你手动触发_
> → 推荐：每天一次，北京时间 10:00（早上上班看报告）
> → 可选：每 4 小时（版本更新/事故期间的高频模式）
> → 不设置也行，每次你跟我说"跑一下"就手动触发
>
> 📨 **报告推送** — _扫描完成后自动把摘要发到你的聊天里，不用你来查_
> → 推荐：精简摘要（只推 P1/P2 问题 + 渠道状态，完整报告存文件）
> → 可选：完整报告直接推送
> → 不设置就只存文件，你需要时问我要
>
> 要设置哪个？都不需要就回"跳过"。

**交互设计原则**：
- **最少问题数**：只有游戏名是必填，其他全有默认值
- **一次确认制**：每步把所有选项列出，用户可一次性确认或逐项改
- **容错**：用户任何时候说"先跑着看看"都直接用当前值启动
- **渐进披露**：跑完首次报告后，根据结果建议优化关键词和渠道

Read `references/config-schema.md` for full config structure and defaults.

## Project Directory Structure

**用户数据与 skill 代码分离**：skill 目录由 clawhub 管理，用户数据放在 workspace 级别，避免更新覆盖。

```
~/.openclaw/workspace/
├── skills/
│   └── game-sentiment/                      # skill 代码（clawhub 管理，可更新）
│       ├── SKILL.md
│       └── references/
│
└── game-sentiment-data/                     # 用户数据（独立于 skill，不受更新影响）
    ├── .credentials/accounts.json           # 用户凭据（.gitignore 排除）
    └── {game-slug}/
        ├── config.json                      # 该游戏最新配置
        └── reports/
            ├── YYYY-MM-DD-HHmm/
            │   ├── {game-slug}_YYYY-MM-DD-HHmm.md
            │   ├── config.json              # 本次运行 config 快照
            │   └── data/                    # 本次采集原始数据
            └── _archive/
```

`{WORKSPACE}` = OpenClaw workspace 根目录（通常为 `~/.openclaw/workspace`）

**命名规范**：
- 文件夹：`YYYY-MM-DD-HHmm`（UTC 时间）
- 报告文件：`{game-slug}_YYYY-MM-DD-HHmm.md`
- game-slug：游戏名转 kebab-case（三角洲行动 → delta-force，原神 → genshin）

**每次执行时**：
1. 读取 `{WORKSPACE}/game-sentiment-data/{slug}/config.json`
2. 生成时间戳文件夹 `{WORKSPACE}/game-sentiment-data/{slug}/reports/YYYY-MM-DD-HHmm/`
3. 复制 config.json 到该文件夹（快照）
4. 采集数据写入 `data/` 子目录
5. 报告写入 `{game-slug}_YYYY-MM-DD-HHmm.md`

## Execution Flow

1. **Read config** — Load `{WORKSPACE}/game-sentiment-data/{game-slug}/config.json`。首次执行时此文件不存在，跳过此步，由交互流程（Step 1-4）生成。
2. **Determine task type** — daily / high-frequency / manual ad-hoc
3. **Set scan window** — daily=24h, 4h-mode=6h, manual=custom
4. **Prepare tools** — Ensure Playwright MCP server is available via `mcporter`. Key tools:
   - `playwright.browser_navigate` — 导航
   - `playwright.browser_evaluate` — 执行 JS 提取数据
   - `playwright.browser_snapshot` — 获取页面结构
   - `playwright.browser_click` — 点击元素
   - `playwright.browser_take_screenshot` — 截图（验证码识别）
   - `playwright.browser_handle_dialog` — 处理弹窗
   - `playwright.browser_close` — 关闭浏览器
5. **NGA login** (if enabled) — Read credentials from `{WORKSPACE}/game-sentiment-data/.credentials/accounts.json`, use Playwright iframe DOM manipulation + captcha screenshot + AI recognition. See `references/channel-strategy.md` for detailed steps.
6. **Collect samples** — 采用**多子代理并行模式**：主代理为每个渠道（或渠道组）派发独立子代理，并行采集后汇总。

   **⏱ 用户进度反馈**
   - **启动时**：立即告知用户扫描已开始，列出本次启用的渠道
     > 🚀 开始扫描 **{游戏名}** — 启用 {N} 个渠道：{渠道列表}
     > 完成后推送报告摘要。
   - **每个渠道完成时**：推送一次状态更新
   - **全部完成时**：推送最终摘要（见步骤 12）

   - **渠道分组与子代理分配**：
     - 子代理A：微博（多组关键词串行，翻页采集，不设超时限制）
     - 子代理B：TapTap
     - 子代理C：贴吧 + B站
     - 子代理D：YouTube API
     - 子代理E：web_search 渠道（Reddit + X + 游戏媒体）
     - 子代理F：小红书
     - 子代理G：知乎 + Discord（web_search 降级渠道）
     - NGA 如启用则单独子代理
   - **子代理职责**：采集原始数据（含帖子 URL、标题、用户名、时间） + 执行本渠道清洗 → 返回结构化 JSON 结果
   - **主代理职责**：派发任务 → 等待所有子代理完成 → 跨渠道合并 → 生成报告
   - **提取策略**：优先使用精准 evaluate 脚本（见 `references/channel-strategy.md`），fallback 到 `innerText.slice(0, 15000)`
   - **子代理必须使用 mcporter CLI 调用 Playwright**（`mcporter call playwright.browser_navigate`），不能用 web_fetch 替代需要 JS 渲染的页面
   - Each sub-agent task must include: mcporter 调用示例、精准 evaluate 脚本、fallback 规则、数据清洗规则
   
   For each available channel, following the verified methods in `references/channel-strategy.md`:
   - **微博**: m.weibo.cn JSON API via Playwright, multiple keyword groups (通用/外挂/盗号/封号/卡顿掉帧闪退/bug闪退崩溃)。**串行采集+间隔**：每组关键词之间间隔 ≥5 秒，避免 API 限流。如遇限流（返回空数据或错误），等待 15 秒后重试一次，仍失败则标记该关键词为"限流未采集"。**排除词过滤**：采集后用 `config.json` 中 `keywords.exclude` 列表过滤商业帖（含任一排除词的样本标记为 commercial）。**翻页采集**：每组关键词至少采集 2-3 页（page=1,2,3），增加样本覆盖面。另外增加一组"游戏名"纯搜关键词（不带风险词），获取更广泛的玩家讨论面
   - **TapTap**: Playwright render review page, extract text. **APP ID 动态查找**：不硬编码 APP ID，先用 TapTap 搜索 API 或 Playwright 搜索游戏名，验证返回的游戏名与目标游戏匹配后再进入评论页。若搜索结果不匹配，跳过 TapTap 并在报告中标记。**TapTap 为 Tier 1 渠道，不可主动跳过**——只有以下两种情况允许跳过：① healthcheck 失败（TapTap 网站不可达）；② APP ID 动态查找后游戏名不匹配（游戏未在 TapTap 上架）。其他任何原因都不得跳过 TapTap。**双排序采集**：先采"最新"排序 → 再采"最差/1星"排序，合并两批数据并标记来源排序方式，穿透水军层获取真实差评
   - **NGA**: Playwright after login, navigate to game section, extract post list
   - **贴吧**: Playwright 三级提取策略：① `playwright.browser_snapshot` 拿 accessibility tree → 正则提取帖子标题/作者/回复数；② 精准 evaluate 脚本；③ innerText fallback。优先 snapshot 因贴吧新版 Vue SPA 导致传统 DOM 选择器不稳定。**翻页采集**：至少采集 2-3 页帖子列表。**热帖深入**：对回复数最高的 3-5 个帖子，进入帖子详情页抓取前 2 页楼层回复内容
   - **B站**: Playwright search page, extract video titles + stats。**深入评论区**：对搜索结果中互动量最高的 3-5 个视频，进入详情页抓取评论区前 2 页评论（使用 evaluate 脚本或 innerText fallback），评论数据纳入分析
   - **游戏媒体**: `web_search` + `web_fetch` for 17173/游民星空/网易等
   - **Reddit**: `web_search("site:reddit.com ...")` 间接获取，按关键词分组搜索
   - **X/Twitter**: `web_search("site:x.com ...")` 间接获取，按关键词分组搜索
   - **YouTube**: YouTube Data API v3 搜索+视频详情+评论，API key 从 `{WORKSPACE}/game-sentiment-data/.credentials/accounts.json` 读取。**评论翻页**：使用 pageToken 翻页，每个视频采集 60-100 条评论（默认 20 条 × 3-5 页）
   - **小红书**: Playwright 搜索页采集。URL: `https://www.xiaohongshu.com/search_result?keyword={GAME_NAME_ENCODED}&type=1`（笔记类型）。免登录可访问搜索结果页，提取笔记标题、点赞数、评论数。**深入笔记**：对互动量最高的 3-5 条笔记进入详情页抓取正文+评论区前 2 页。**⚠️ 已知限制**：小红书对云服务器 IP 有风控（错误码 300012 "IP at risk"），Azure/AWS 等 VPS IP 大概率被封。此时自动降级为 `web_search("site:xiaohongshu.com {游戏名}")`。用户如有住宅 IP 代理可配置为 Playwright 直连
   - **知乎**: 默认 `web_search("site:zhihu.com {游戏名} {关键词}")`。云服务器 IP 被知乎封锁，Playwright 直连不可用。用户如有住宅 IP 代理可切换为 Playwright 直连
   - **Discord**: 默认 `web_search("site:discord.com {游戏名} {关键词}")`。云服务器 IP 被 Discord 封锁，Playwright 直连不可用。用户如有住宅 IP 代理可切换为 Playwright 直连
   - If a channel fails mid-collection, mark it and continue
   - **web_search 限流应对**：web_search（Gemini）有全局配额限制。采集策略：① 合并关键词到单次查询（如 `"{game} reddit cheating bug complaint"` 而非按关键词拆分多次）；② 每次调用间隔 ≥8 秒；③ 优先级：游戏媒体 > Reddit > X（媒体为 L1 证据）；④ 遇 429 时等待 30 秒重试一次，仍失败则标记"配额耗尽"跳过剩余；⑤ YouTube 走独立 API 不占 web_search 配额，始终执行
   - **关键词有效性评估**：每组关键词采集完成后，计算有效样本率（与游戏相关的样本数 / 总采集数）。有效率 <30% 的关键词 → 在报告中标记为"低效关键词"，其样本降权处理，并建议优化关键词
   - **微博时间过滤**：低热度游戏微博搜索结果可能跨越数月。仅保留目标时间窗口内的样本（默认24h），超出时间窗的样本标记为"历史样本"，不计入当期舆情判定
7. **Clean & deduplicate** — Remove duplicates and noise:
   - Same user + same first 50 chars of text → merge
   - Cross-keyword overlap (e.g., same post found via "外挂" and "盗号") → keep once
   - Template-style posts (identical structure, different users) → flag, count separately
   - **水军过滤**：文本相似度 >90% 的不同账号帖子 → 标记为疑似水军，从有效样本中剔除，在报告中单独注明数量
   - **商业帖过滤**：所有渠道中含"陪玩/代练/交易/出售/收购/接单/招人/低价/秒发"等关键词的帖子 → 过滤，不计入舆情样本。微博额外过滤蓝V认证营销号。贴吧/TapTap 过滤含联系方式（QQ号/微信号/手机号模式）的帖子
   - **信息源集中度检测**：单一用户贡献 >50% 样本 → 标记该渠道为"信息源高度集中"，降低该渠道权重
8. **Per-channel pre-clustering** — Within each channel, cluster similar feedback into topic summaries
9. **Cross-channel merge** — Merge topic lists, identify same issue on multiple platforms. Compare channel-level sentiment differences (key insight: different channels may show very different sentiment profiles).
10. **Assess each issue** — For each clustered topic:
    - Sentiment: positive / neutral / negative / strongly-negative
    - Category: tech-stability / balance / monetization / content / event-rules / ops / marketing-alignment / community / account-security
    - Attribution: technical-incident / design-dispute / monetization-dispute / content-aesthetic / ops-communication / marketing-expectation / security-incident
    - Severity: P1 / P2 / P3 — Read `references/severity-rules.md`
    - Evidence type: 玩家L1 / 媒体L1 / 官方响应 / L2
    - Credibility: High / Medium / Low
    - Spread: isolated → single-platform-hot → multi-platform → mainstream/media
    - Suggested owner: dev / QA / design / ops / CS / community / marketing-PR / security
    - Suggested action: immediate-check / add-to-known-issues / post-announcement / adjust-parameters / revise-copy / evaluate-compensation / monitor
11. **Check sample sufficiency** — If total valid samples too low, downgrade to low-sample observation report
    - **无显著风险简短模式**：若所有议题均为 P3 或更低，且无新增议题，生成简短报告（仅含渠道状态表 + 一句话总结 + "社区运营平稳，无需介入"），不展开完整议题卡片
12. **Generate report** — Markdown file saved to `reports/YYYY-MM-DD-HHmm.md`. Read `references/report-template.md` for structure. Must include:
    - 采样策略表（关键词、渠道数、偏差说明）
    - 时间维度表（目标窗口/实际窗口/时间可信度）
    - 渠道状态表（采集方式、证据等级、样本数）
    - 议题卡片（issue_type, cause_category, 判级依据, 原文引用 + source）
    - **每条证据必须附 source**：渠道名 + 原始 URL + 帖子标题/用户名 + 采集时间。格式示例：`[B站] "镜神跌落神坛" — UP主xxx — https://bilibili.com/video/xxx — 2026-04-06 01:30 UTC`。web_search 降级渠道无法获取精确 URL 时，标注搜索查询词和结果摘要来源
    - 跨渠道舆情画像对比
    - 业务动作建议（分立即/短期/持续跟踪）
13. **Feishu summary** — Send condensed summary (top 3 issues + action list) to Feishu
14. **P1 alert** — If any P1 issues found, send immediate Feishu alert
15. **Close browser** — `playwright.browser_close` to release resources
16. **Update state** — Save execution metadata to `data/state.json`

## Batch Processing

When samples from a single channel exceed context window capacity:
- Split by time or pagination
- Each batch produces topic summaries
- Merge batch summaries before cross-channel merge

## Degradation Rules

- **Channel failure**: Skip and mark in report as "not collected this period"
- **Low samples**: Downgrade to observation report — only list collected channels, brief feedback summary, uncovered channels, and recommendations
- **Narrow keywords / noisy results**: Flag in report: suggest broadening keywords, adjusting channels, or switching to manual scan
- **Never fabricate**: Better to under-report than to escalate scattered complaints as high-risk

## Sensitive Wording

For high-sensitivity labels (secret nerfs, fraud, wrongful bans, fairness violations):
- Default to "player concerns / concentrated feedback" phrasing
- Never state as verified fact without confirmation

## Output Priority

- **Primary**: Markdown report in `reports/`
- **Secondary**: Feishu summary message (condensed)
- **Conditional**: P1 instant alert via Feishu

## File References

- `references/config-schema.md` — Config structure, defaults, minimal example
- `references/channel-strategy.md` — Channel tiers, roles, healthcheck, degradation
- `references/severity-rules.md` — P1/P2/P3 definitions, credibility, sensitive wording, owner mapping
- `references/report-template.md` — Report structures for daily, low-sample, and P1 alert
