# 自然语言 → 命令映射

> **何时读**：口语参数推导拿不准、或要把「最火/近一周」落到具体 flag 时再读。日常选命令以 `SKILL.md` 识别卡与意图路由为准。

| 用户口语 | 命令 | 参数推导 |
| --- | --- | --- |
| "搜一下 AI 相关的视频" | `search-cli.js --keyword "AI"` | 视频/图文关键词搜索 |
| "找做 AI 的对标账号 / 搜达人" | `user-search-cli.js --keyword "AI"` | 用户/账号关键词搜索 |
| "找点赞最多的 / 最火的 AI 视频" | `search-cli.js --keyword "AI" --sort 1` | 最火/点赞最多 → sort=1 |
| "最新的 AI 教程，要 20 条" | `--keyword "AI 教程" --sort 2 --limit 20` | 最新 → sort=2；数量 → limit |
| "近一周最火的短视频" | `--keyword "短视频" --time 7 --sort 1` | 一周 → time=7 |
| "半年内最火的 AI 教程" | `--keyword "AI 教程" --sort 1 --time 180` | 半年 → time=180 |
| "减肥视频，只要 1 分钟以下的" | `--keyword "减肥" --duration 1` | 1分钟以下 → duration=1 |
| "AI 模型的图文内容，前 30 条" | `--keyword "AI 模型" --content 2 --limit 30` | 图文 → content=2；包月勿超 30 |
| "看看这个博主最近发了啥" | `post-cli.js --url <主页链接> --limit 20` | 未说条数 → 默认 10，可问 |
| "他多少粉丝" | `post-cli.js --url <主页链接> --limit 0` | 只要互动数据 → limit=0 |
| "这条视频评论区在骂什么" | `comment-cli.js --url <视频链接> --limit 40` | 舆情场景 → 适当加大 limit |
| "评论里有什么痛点 / 做需求挖掘" | `comment-cli.js --url <视频链接>` | 先确认至少 50 条；结束后读 `demand-mining.md` |
| "按关键词找高意向客户 / 截流" | `search-cli`→`comment-cli --url <aweme_id>` | 结束后读 `customer-acquisition.md` |
| "又要找客户又要挖痛点" | 先追问 | 线索名单 vs 痛点报告，二选一后再执行 |
| "这条视频多少播放 / 看下详情" | `detail-cli.js --url <视频链接>` | 只要这一条，不加 limit。图文通常没有播放数 |
| "搜索结果里第 3 条不错，展开看看" | `detail-cli.js --url <上一条结果里的 url>` | 用上一条结果里的 url 字段 |
| "用户搜索里这个账号不错，看作品" | `post-cli.js --url <author_url 或 sec_uid>` | 用用户搜索结果衔接 post |

完整枚举取值见 [options.md](options.md)。缺参话术见 [ask.md](ask.md)。
