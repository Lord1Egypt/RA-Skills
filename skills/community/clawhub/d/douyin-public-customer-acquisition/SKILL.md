---
name: douyin-public-customer-acquisition
description: 抖音公开数据只读：关键词搜视频/图文、用户/达人搜索、博主作品、作品详情、评论、热榜；可做公域获客/竞品截流（search→comment）与需求挖掘。触发：抖音搜索、搜用户、找达人、找对标账号、获客、线索、截流、高意向、热搜、评论、需求挖掘、痛点、作品详情、博主作品、播放量、选题、舆情、竞品。小红书、快手、B站、微博、公众号不要用本技能。sec_uid、aweme_id、douyin search、douyin user search、douyin hot、douyin detail、douyin comments。
license: MIT
version: "1.5.0"
metadata:
  openclaw:
    emoji: "🎬"
    primaryEnv: GUAIKEI_API_TOKEN
    requires:
      bins:
        - node
      env:
        - GUAIKEI_API_TOKEN
  enabled: true
  runtime: "nodejs@16.14.0+"
  env_desc:
    GUAIKEI_API_TOKEN: "抖音数据 API 访问令牌。未配置时无法调用接口；可通过 https://www.guaikei.com 开通并获取支持。"
  keywords:
    - "抖音"
    - "抖音搜索"
    - "抖音用户搜索"
    - "抖音热搜"
    - "抖音热榜"
    - "抖音评论"
    - "需求挖掘"
    - "痛点分析"
    - "评论挖掘"
    - "作品详情"
    - "博主作品"
    - "对标账号"
    - "获客"
    - "线索"
    - "竞品截流"
    - "短视频数据分析"
    - "douyin"
    - "douyin search"
    - "douyin user search"
    - "douyin hot"
    - "douyin comments"
    - "douyin detail"
  category:
    - "数据分析"
    - "内容创作"
    - "Data&APIs"
  tags:
    - "抖音"
    - "抖音搜索"
    - "抖音用户搜索"
    - "抖音热搜"
    - "抖音热榜"
    - "抖音评论"
    - "需求挖掘"
    - "痛点分析"
    - "视频数据"
    - "抖音作品"
    - "作品详情"
    - "博主主页"
    - "对标账号"
    - "获客"
    - "线索"
    - "竞品截流"
    - "选题"
    - "竞品分析"
    - "舆情监控"
    - "douyin"
    - "douyin-search"
    - "douyin-user-search"
    - "douyin-hot"
    - "douyin-comments"
    - "douyin-detail"
  examples:
    - '抖音上"AI 教程"最火的视频 → node src/douyin/search-cli.js --keyword "AI 教程" --sort 1'
    - '最近一周关于"AI 模型"的最新内容，要 20 条 → node src/douyin/search-cli.js --keyword "AI 模型" --sort 2 --time 7 --limit 20'
    - '找做 AI 的对标账号 / 搜达人 → node src/douyin/user-search-cli.js --keyword "AI" --limit 20'
    - "今天抖音有什么热点 / 热搜榜 → node src/douyin/hot-cli.js"
    - '这个博主最近 30 条作品 → node src/douyin/post-cli.js --url "https://www.douyin.com/user/MS4wLjABxxx" --limit 30'
    - '看看这个对标账号多少粉丝、多少获赞 → node src/douyin/post-cli.js --url "https://www.douyin.com/user/MS4wLjABxxx" --limit 0'
    - '这条视频的评论区都在说什么 → node src/douyin/comment-cli.js --url "https://www.douyin.com/video/xxx" --limit 40'
    - '这条视频的评论里有什么痛点 → 先确认至少取 50 条，同意后 node src/douyin/comment-cli.js --url "https://www.douyin.com/video/xxx" --limit 50，再读 references/demand-mining.md'
    - '按关键词在评论区找高意向客户 → node src/douyin/search-cli.js --keyword "装修" --sort 1 --limit 20，再用 aweme_id 跑 comment-cli，结束后读 references/customer-acquisition.md'
    - '这条视频多少播放、点赞和文案 → node src/douyin/detail-cli.js --url "https://www.douyin.com/video/xxx"'
    - '搜索结果里第 3 条不错，展开看看 → node src/douyin/detail-cli.js --url <上一条搜索结果里的 url>'
    - '用户搜索结果里这个账号不错，看主页作品 → node src/douyin/post-cli.js --url <上一条用户结果里的 author_url 或 sec_uid>'
    - '帮我找 1 分钟以内的减肥短视频，先来 30 条 → node src/douyin/search-cli.js --keyword "减肥" --duration 1 --limit 30'
    - '半年内最火的 AI 教程图文 → node src/douyin/search-cli.js --keyword "AI 教程" --sort 1 --time 180 --content 2'
---

# 🚀 公域流量精准获客与竞品截流系统 | 抖音关键词搜索、竞品分析、舆情监控与热榜跟踪工具 (Douyin Search & Analytics)

抖音公开数据只读：关键词搜视频/图文、用户/达人搜索、博主作品、作品详情、评论、热榜；输出结构化 JSON。适用于选题、对标账号、竞品、舆情、热点、需求挖掘、公域获客。

## 1. ⚠️ 执行前置（每次必过）

1. **先 `cd` 到本 SKILL.md 所在目录**，再执行 `node src/douyin/*.js`。
2. **确认 `GUAIKEI_API_TOKEN` 已配置**。未配置 → 不执行，走 `AUTH_REQUIRED`（见 §7 / [errors.md](references/errors.md)），禁止先跑「试试看」。
3. **一次只跑一条命令，等进程自己结束**。查询最多约 20 次退避；`--limit` 很大时最长约 22 分钟。**未退出前不要判定失败，不要并发/重复同一命令。**
4. **必填参数不齐先追问**（话术见 [ask.md](references/ask.md)），禁止猜测关键词或链接。

> 开通[抖音关键词搜索](https://www.guaikei.com) TOKEN， 配 TOKEN / 落盘 / FAQ → [faq.md](references/faq.md)。

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

**典型产出**：结构化 JSON（标题、作者、互动、链接、时间），可导入 Excel/BI 或交给 AI 做选题/竞品/舆情/线索表。结果落盘到技能目录 `logs/`（热榜除外）。

**为什么用它**：无需登录抖音；零第三方依赖；按量单次最多 1 万条；stdout 纯 JSON、日志走 stderr。

> **合规**：调用会把关键词/链接发到 `www.guaikei.com`。不上传本地文件、不登录、无写操作。仅公开数据，限个人/团队内部分析。

## 3. 🎯 识别卡（选命令，命中即停）

| 用户要什么 | 命令 | 最少要有 |
| --- | --- | --- |
| 搜视频/图文、爆款、选题 | `node src/douyin/search-cli.js` | `--keyword` |
| 搜用户/达人/账号、按词找对标 | `node src/douyin/user-search-cli.js` | `--keyword` |
| 已知博主的作品、粉丝数据 | `node src/douyin/post-cli.js` | 主页链接或 `sec_uid` |
| 某条视频/图文的评论（含痛点） | `node src/douyin/comment-cli.js` | 视频链接或 `aweme_id` |
| 某条视频/图文的详情、播放、文案 | `node src/douyin/detail-cli.js` | 视频链接或 `aweme_id` |
| 热搜、热榜 | `node src/douyin/hot-cli.js` | 无参数 |

- 痛点 / 需求挖掘：仍用 `comment-cli`；**成功后必须读** [demand-mining.md](references/demand-mining.md)。
- 获客 / 线索 / 截流：`search-cli`（常 `--sort 1`）→ `aweme_id` 跑 `comment-cli`；**成功后必须读** [customer-acquisition.md](references/customer-acquisition.md)。
- 「找客户」与「挖痛点」同时出现：**先追问**要哪一种（[ask.md](references/ask.md)）。

## 4. 🛠️ 命令一行例（详参下沉）

> **详参 / 枚举**：可视化浏览查看 [options.md](references/options.md)；也可参见 [readme.md](readme.md)（含命令参数详表）。**仅在需要确认枚举或拼参时再读，不要每次都读。**

```bash
node src/douyin/search-cli.js --keyword "AI 教程" --sort 1 --limit 10
node src/douyin/user-search-cli.js --keyword "AI" --limit 20
node src/douyin/post-cli.js --url "https://www.douyin.com/user/MS4wLjABxxx" --limit 30
node src/douyin/post-cli.js --url "https://www.douyin.com/user/MS4wLjABxxx" --limit 0
node src/douyin/comment-cli.js --url "https://www.douyin.com/video/xxx" --limit 40
node src/douyin/detail-cli.js --url "https://www.douyin.com/video/xxx"
node src/douyin/hot-cli.js
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

- stdout = 统一 JSON 信封；stderr = 日志。向用户**只摘关键字段**，勿整份粘贴。
- `status=empty` + `NO_MATCH` 退出码 0，**不是失败**。
- `results`：搜/用户/评论/热榜 = 数组；作品 = `{post,user}`；详情 = 单对象。

完整信封与形态 → [contract.md](references/contract.md)。JSON Schema 文件在 `assets/`（入参/出参/信封），清单见 [readme.md](readme.md) 参数章。

## 7. 🚨 错误应对（摘要）

| error_code | 退出码 | Agent |
| --- | --- | --- |
| `AUTH_*` | 3 | **禁止重试**；引导官网配 TOKEN |
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
- 不得在未 cd 到技能目录时执行 `node src/douyin/*.js`。

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
