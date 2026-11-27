---
summary: 抖音起号冷启动数据源（只读）：作品详情、视频评论、博主作品、关键词搜索、实时热榜，输出结构化JSON供AI做新账号定位与冷启动规划。用于对标账号取样、人设与内容方向确定、首批选题池搭建、首月发布排期。触发词：抖音起号、抖音冷启动、新号定位、douyin launch、douyin cold start。
displayName: 抖音起号冷启动｜账号定位·对标取样·内容规划·首月排期
slug: dy-launch
name: dy-launch
description: 抖音起号冷启动数据源（只读）：关键词搜索、博主作品、作品详情、评论、热榜。触发：抖音搜索、热搜、评论、需求挖掘、痛点、作品详情、博主作品、对标账号、播放量、选题、舆情、竞品。小红书、快手、B站、微博、公众号不要用本技能。sec_uid、aweme_id、douyin search、douyin hot、douyin detail、douyin comments。
license: MIT
version: 1.5.2
display_name: "抖音起号冷启动｜账号定位·对标取样·内容规划·首月排期"
display_name_en: "Douyin Launch"
description_zh: "抖音起号冷启动数据源（只读，无需登录）：关键词搜索视频与图文、用户/达人搜索、博主作品与粉丝互动、单条作品详情、视频评论、实时热榜，全部输出结构化 JSON。用于新账号定位与对标取样、人设与内容方向确定、首批选题池搭建、首月发布排期与发文节奏复盘。支持综合/最多点赞/最新排序，以及时间、时长、内容类型多维筛选；按量 Token 单次最多 10000 条，包月视频搜索/用户搜索/作品最多 30、评论最多 50。不登录、不发布、不点赞、不评论，无封号风险；零第三方依赖，Node.js 内置模块直接运行。触发词：抖音起号、抖音冷启动、新号定位、对标账号、选题规划。"
description_en: "Douyin (TikTok China) cold-start data source for new-account launch planning - read-only, no login required. It provides keyword video and photo search, user and creator search, creator works with follower and engagement metrics, single-video detail, video comments and the real-time Douyin hot list, all returned as structured JSON for AI analysis. Use it to define a new account's positioning, sample benchmark creators, choose persona and content direction, build a first batch of topics and plan the first-month publishing calendar. Sort by relevance, most-liked or newest, and filter by time window, duration and content type. Hard limit is 10,000 items per call; monthly plans cap search and creator works at 30 and comments at 50. It never logs in, publishes, likes or comments, so there is no account risk. Zero dependencies, runs on Node.js 16.14+."
author: "新郑市怪奇信息技术工作室"
metadata:
  openclaw:
    primaryEnv: GUAIKEI_API_TOKEN
    requires:
      bins:
        - node
      env:
        - GUAIKEI_API_TOKEN
  tags:
    - "抖音搜索"
    - "抖音用户搜索"
    - "抖音热榜"
    - "抖音评论"
    - "作品详情"
    - "博主作品"
    - "对标账号"
    - "需求挖掘"
    - "获客"
    - "竞品截流"
    - "舆情监控"
    - "选题"
    - "douyin"
  examples:
    - '抖音上"AI 教程"最火的视频 → node "<SKILL_ROOT>/src/douyin/search-cli.js" --keyword "AI 教程" --sort 1'
    - '找做 AI 的对标账号 / 搜达人 → node "<SKILL_ROOT>/src/douyin/user-search-cli.js" --keyword "AI" --limit 20'
    - '这个博主最近 30 条作品 → node "<SKILL_ROOT>/src/douyin/post-cli.js" --url "https://www.douyin.com/user/MS4wLjABxxx" --limit 30'
    - '这条视频的评论区都在说什么 → node "<SKILL_ROOT>/src/douyin/comment-cli.js" --url "https://www.douyin.com/video/xxx" --limit 40'
    - '这条视频的评论里有什么痛点 → 先确认至少取 50 条，同意后 node "<SKILL_ROOT>/src/douyin/comment-cli.js" --url "https://www.douyin.com/video/xxx" --limit 50，再读 references/demand-mining.md'
    - '这条视频多少播放、点赞和文案 → node "<SKILL_ROOT>/src/douyin/detail-cli.js" --url "https://www.douyin.com/video/xxx"'
---

# 🚀 抖音起号冷启动 · 功能列表 (Douyin Account Launch)

抖音公开数据只读：关键词搜视频/图文、用户/达人搜索、博主作品、作品详情、评论、热榜；输出结构化 JSON。适用于选题、对标账号、竞品、舆情、热点、需求挖掘、公域获客。

## 1. ⚠️ 执行前置（每次必过）

1. **用绝对路径执行**：`node "<SKILL_ROOT>/src/douyin/<命令>.js" …`。`<SKILL_ROOT>` = 含本 `SKILL.md` 的那一层真实目录（以当前会话为准；勿套用其它宿主示例路径，勿用 frontmatter `name` 冒充目录名）。已 `cd` 到技能根时可用相对路径 `node src/douyin/…`（见 [faq.md](references/faq.md)）。
2. **确认 `GUAIKEI_API_TOKEN` 已配置**。未配置 → 不执行，走 `AUTH_REQUIRED`（见 §7 / [errors.md](references/errors.md)），禁止先跑「试试看」。
3. **一次只跑一条命令，等进程自己结束**。查询最多约 20 次退避；`--limit` 很大时最长约 22 分钟。**未退出前不要判定失败，不要并发/重复同一命令。**
4. **必填参数不齐先追问**（话术见 [ask.md](references/ask.md)），禁止猜测关键词或链接。
5. **Windows 拼参：cmd 只用双引号**包含空格/中文/URL 的参数；不要用 bash 单引号。引号仍拆坏 → 改用 `--json-args`（[faq.md](references/faq.md)）。Windows / 弱模型优先 `--json-args`。

> 开通[抖音达人合作管理分析API](https://www.guaikei.com) TOKEN， 配 TOKEN / 落盘 / FAQ → [faq.md](references/faq.md)。

## 2. 💎 价值与典型场景（10 秒判断该不该用）

| 你是谁 | 你要做的事 | 用哪个命令 |
| --- | --- | --- |
| 短视频运营 | 找爆款选题、看高赞内容的共同点 | `search-cli.js --sort 1` |
| 运营 / 投放 | 按关键词找对标账号、达人 | `user-search-cli.js` |
| 品牌 / 投放 | 监控已知账号的发文节奏与内容策略 | `post-cli.js` |
| 内容分析 | 看一条视频的文案、播放和互动 | `detail-cli.js` |
| 舆情 / 客服 | 判断一条视频的评论区在骂还是在夸 | `comment-cli.js` |
| 产品 / 运营 | 从评论里看痛点和诉求 | `comment-cli.js`，再读 [demand-mining.md](references/demand-mining.md) |
| 销售 / 增长 | 按关键词在评论区挖高意向线索 | `search`→`comment`，再读 [customer-acquisition.md](references/customer-acquisition.md) |
| 所有人 | 今天抖音在火什么 | `hot-cli.js` |

**典型产出**：结构化 JSON（标题、作者、互动、链接、时间），可导入 Excel/BI 或交给 AI 做选题/竞品/舆情/线索表。默认不落盘；需要留底时加 `--save` 或设 `GUAIKEI_ENABLE_LOG=1`（热榜除外，见 [faq.md](references/faq.md)）。

**为什么用它**：无需登录抖音；零第三方依赖；按量单次最多 1 万条；stdout 纯 JSON、日志走 stderr。

> **合规**：调用会把关键词/链接发到 `www.guaikei.com`。不上传本地文件、不登录、无写操作。仅公开数据，限个人/团队内部分析。

## 3. 🎯 识别卡（选命令，命中即停）

执行：`node "<SKILL_ROOT>/src/douyin/<脚本>" …`（下表只写脚本名）。

| 用户要什么 | 命令 | 最少要有 |
| --- | --- | --- |
| 搜视频/图文、爆款、选题 | `search-cli.js` | `--keyword` |
| 搜用户/达人/账号、按词找对标 | `user-search-cli.js` | `--keyword` |
| 已知博主的作品、粉丝数据 | `post-cli.js` | 主页链接或 `sec_uid` |
| 某条视频/图文的评论（含痛点） | `comment-cli.js` | 视频链接或 `aweme_id` |
| 某条视频/图文的详情、播放、文案 | `detail-cli.js` | 视频链接或 `aweme_id` |
| 热搜、热榜 | `hot-cli.js` | 无参数 |

- 痛点 / 需求挖掘：仍用 `comment-cli`；**成功后必须读** [demand-mining.md](references/demand-mining.md)。
- 获客 / 线索 / 截流：`search-cli`（常 `--sort 1`）→ `aweme_id` 跑 `comment-cli`；**成功后必须读** [customer-acquisition.md](references/customer-acquisition.md)。
- 「找客户」与「挖痛点」同时出现：**先追问**要哪一种（[ask.md](references/ask.md)）。

## 4. 🛠️ 命令一行例（详参下沉）

> **详参 / 枚举**：可视化浏览查看 [options.md](references/options.md)；也可参见 [readme.md](readme.md)（含命令参数详表）。**仅在需要确认枚举或拼参时再读，不要每次都读。**
> **Windows**：cmd **只用双引号**；PowerShell 含空格也优先双引号。仍拆坏或弱模型 → `--json-args`。双壳例 → [faq.md](references/faq.md)。

```bash
node "<SKILL_ROOT>/src/douyin/search-cli.js" --keyword "AI 教程" --sort 1 --limit 10
node "<SKILL_ROOT>/src/douyin/user-search-cli.js" --keyword "AI" --limit 20
node "<SKILL_ROOT>/src/douyin/post-cli.js" --url "https://www.douyin.com/user/MS4wLjABxxx" --limit 30
node "<SKILL_ROOT>/src/douyin/post-cli.js" --url "https://www.douyin.com/user/MS4wLjABxxx" --limit 0
node "<SKILL_ROOT>/src/douyin/comment-cli.js" --url "https://www.douyin.com/video/xxx" --limit 40
node "<SKILL_ROOT>/src/douyin/detail-cli.js" --url "https://www.douyin.com/video/xxx"
node "<SKILL_ROOT>/src/douyin/hot-cli.js"
```

**Windows 双壳（同一条搜索；把 `<SKILL_ROOT>` 换成真实技能根）**：

```bat
REM cmd —— 参数必须用双引号；也可用 --json-args（内层 \"）
node "<SKILL_ROOT>\src\douyin\search-cli.js" --keyword "AI 教程" --sort 1 --limit 10
node "<SKILL_ROOT>\src\douyin\search-cli.js" --json-args "{\"keyword\":\"AI 教程\",\"sort\":1,\"limit\":10}"
```

```powershell
# PowerShell —— 含空格/中文同样用双引号；或改用 --json-args（外单内双）
node "<SKILL_ROOT>/src/douyin/search-cli.js" --keyword "AI 教程" --sort 1 --limit 10
node "<SKILL_ROOT>/src/douyin/search-cli.js" --json-args '{"keyword":"AI 教程","sort":1,"limit":10}'
```

**数量 / 套餐**：未指定 `--limit` 默认 10；不要擅自抓 10000。技能硬上限 10000（按量）。**包月**超限 → `PLAN_LIMIT`：视频搜索/用户搜索/作品 ≤30，评论 ≤50；详情与热榜无此条数限制。

口语 → flag 对照 → [routing.md](references/routing.md)。

## 5. 🔀 意图路由（按序命中即停）

```
1. 热榜/热搜/今天什么火 → hot-cli
2. 获客+痛点同时出现 → 先追问（ask.md），禁止两边都做
3. 获客/线索/截流/高意向 → search→comment；结束后读 customer-acquisition.md
4. 评论/留言/痛点/需求挖掘 + 有视频 → comment-cli；痛点类结束后读 demand-mining.md
5. 痛点/需求挖掘但无视频链接 → 先追问链接
6. 单条详情/播放/点赞/文案 → detail-cli
7. 搜用户/达人/对标账号（关键词、无主页链接）→ user-search-cli
8. 已有主页/sec_uid 或要某账号作品列表 → post-cli
9. 有关键词且无以上信号 → search-cli
10. 都不明确 → 先追问（ask.md）
```

消歧：单独「视频」不要默认 post/detail。`/user/` → 只能 post；`/video|note/` + 评论 → comment，+ 播放/文案 → detail，都没说 → 追问。「对标」仅关键词 → user-search；已有链接 → post。

## 6. 📜 输出（摘要）

- stdout = 统一 JSON 信封；stderr = 日志。向用户**只摘关键字段**，勿整份粘贴。取数成功/empty 时信封顶层可能有 `cost`（花费估算，见 [contract.md](references/contract.md)）。
- `status=empty` + `NO_MATCH` 退出码 0，**不是失败**。
- `results`：搜/用户/评论/热榜 = 数组；作品 = `{post,user}`；详情 = 单对象。

完整信封与形态 → [contract.md](references/contract.md)（含上游 Create `id` → `/info` 只传 `id`；CLI schema 不含任务 uuid）。JSON Schema 文件在 `assets/`（入参/出参/信封），清单见 [readme.md](readme.md) 参数章。

## 7. 🚨 错误应对（摘要）

| error_code | 退出码 | Agent |
| --- | --- | --- |
| `AUTH_*` | 3 | **禁止重试**；引导官网检查/开通/续期 TOKEN（含停用 410、未开通 405；勿当成接口下线） |
| `PLAN_LIMIT` | 1 | **禁止同参重试**；降 limit 须用户同意 |
| `INSUFFICIENT_BALANCE` / `DAILY_LIMIT` | 1 | **禁止同参重试**；充值或明日/调限额 |
| `RATE_LIMITED` | 1 | **禁止立即重试** |
| `INVALID_*` | 1/2 | 换词/换链/按 help 改一次；禁止擅自改默认再跑 |
| `NO_MATCH` | 0 | 如实无结果 |
| `TIMEOUT` / `NETWORK_ERROR` | 1 | 同参续等最多 1 次（搜/用户约 9 分钟、作品/详情/评论约 20 分钟复用）；禁止改参「重做」 |

全表 → [errors.md](references/errors.md)。

## 8. 🛑 硬性禁止

- 不得编造数据；不得把空结果说成有结果。
- 不得未征得同意就自动改搜索条件重试。
- `AUTH_*` / `PLAN_LIMIT` / `INSUFFICIENT_BALANCE` / `RATE_LIMITED` / `DAILY_LIMIT` 后不得同参或立即重试。
- 不得把 stderr 原文转述给用户。
- 不得做登录态/私密获取或任何写操作；不得编造手机号/微信号或骚扰脚本。
- 相对路径 `node src/douyin/*.js` 仅在已处于 `<SKILL_ROOT>` 时可用；否则必须用 `node "<SKILL_ROOT>/src/douyin/….js"`。

## 9. 📚 何时读 references（入口总表）

| 时机 | 打开 |
| --- | --- |
| 确认枚举/参数取值 | [options.md](references/options.md) |
| 口语指令 → flag | [routing.md](references/routing.md) |
| 信封 / `results` 形态 | [contract.md](references/contract.md) |
| 完整错误表 | [errors.md](references/errors.md) |
| 缺参追问话术 | [ask.md](references/ask.md) |
| 环境 / FAQ | [faq.md](references/faq.md) |
| 需求挖掘（取数成功后） | [demand-mining.md](references/demand-mining.md) |
| 公域获客（取数成功后） | [customer-acquisition.md](references/customer-acquisition.md) |
| 版本变更 | [changelog.md](references/changelog.md) |
| 技术人员总览（含命令参数详表 / Schema 清单） | [readme.md](readme.md) |
| 机器可校验 Schema | `assets/*.schema.json` |
