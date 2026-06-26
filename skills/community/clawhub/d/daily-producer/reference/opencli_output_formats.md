# opencli 各信息源输出格式参考

记录每个平台通过 `opencli <platform> <command> -f json` 返回的字段结构。
用于采集后的统一解析、筛选和去重。

数据来源：opencli 源码 `clis/<platform>/<command>.ts|yaml` 中的 columns 定义 + 实际测试验证。

最后更新：2026-04-05

---

## 一、国内平台

### 微博 `weibo`

| 命令 | 输出字段 | 时间字段 | 登录 |
|------|---------|---------|------|
| `hot` | rank, word, hot_value, category, label, url | **无** | 不需要 |
| `search "{kw}"` | rank, title, author, **time**, url | `time`（格式不固定） | 需要 |
| `feed` | author, text, reposts, comments, likes, **time**, url | `time` | 需要 |
| `comments <id>` | rank, author, text, likes, replies, **time** | `time` | 需要 |
| `post <id>` | — (详情) | — | 需要 |
| `user <id>` | screen_name, uid, followers, following, statuses, verified, description, location, url | **无** | 需要 |

---

### 小红书 `xiaohongshu`

| 命令 | 输出字段 | 时间字段 | 登录 |
|------|---------|---------|------|
| `search "{kw}"` | rank, title, author, likes, **published_at**, url | `published_at` (`YYYY-MM-DD`) | 需要 |
| `feed` | title, author, likes, type, url | **无** | 需要 |
| `note <id>` | field, value (键值对: title, author, content, likes, collects, comments, tags) | **无** | 需要 |
| `comments <id>` | 测试返回空（可能需要有效 note-id） | — | 需要 |

---

### B站 `bilibili`

| 命令 | 输出字段 | 时间字段 | 登录 |
|------|---------|---------|------|
| `hot` | rank, title, author, play, danmaku | **无** | 不需要 |
| `search "{kw}"` | rank, title, author, score, url | **无**（API 有 pubdate 但适配器未提取） | 不需要 |
| `ranking` | rank, title, author, score, url | **无** | 不需要 |
| `feed` | rank, author, title, type, url | **无** | 需要 |
| `dynamic` | id, author, text, likes, url | **无** | 需要 |
| `history` | rank, title, author, progress, url | **无** | 需要 |
| `favorite` | rank, title, author, plays, url | **无** | 需要 |
| `comments <bvid>` | rank, author, text, likes, replies, **time** | `time` | 需要 |
| `user-videos <uid>` | rank, title, plays, likes, **date**, url | `date` | 不需要 |
| `subtitle <bvid>` | index, from, to, content | — | 需要 |

---

### 知乎 `zhihu`

| 命令 | 输出字段 | 时间字段 | 登录 |
|------|---------|---------|------|
| `hot` | rank, title, heat, answers, url | **无** | 不需要 |
| `search "{kw}"` | rank, title, type, author, votes, url | **无** | 不需��� |

**字段说明：**
- `heat`：热度值（字符串，如 `202 万热度`）
- `type`：内容类型（`article` / `answer`）
- `votes`：赞同数

---

### V2EX `v2ex`

| 命令 | 输出字段 | 时间字段 | 登录 |
|------|---------|---------|------|
| `hot` | id, rank, title, node, replies, url | **无** | 不需要 |
| `latest` | id, rank, title, node, replies, url | **无** | 不需要 |
| `topic <id>` | id, title, content, member, **created**, node, replies, url | `created` | 不需要 |

---

### 36氪 `36kr`

| 命令 | 输出字段 | 时间字段 | 登录 |
|------|---------|---------|------|
| `hot` | rank, title, url | **无** | 不需要 |
| `news` | rank, title, summary, **date**, url | `date` | 不需要 |
| `search "{kw}"` | rank, title, **date**, url | `date` | 不需要 |

---

### 即刻 `jike`

| 命令 | 输出字段 | 时间字段 | 登录 |
|------|---------|---------|------|
| `search "{kw}"` | 未测试（需登录） | — | 需要 |
| `feed` | 未测试（需登录） | — | 需要 |

**备注：** 即刻所有命令都需要登录，未登录无法测试。

---

### 百度贴吧 `tieba`

| 命令 | 输出字段 | 时间字段 | 登录 |
|------|---------|---------|------|
| `hot` | 未测试 | — | 不需要 |
| `search "{kw}"` | 未测试 | — | 不需要 |

---

## 二、国外平台

### Twitter/X `twitter`

| 命令 | 输出字段 | 时间字段 | 登录 |
|------|---------|---------|------|
| `search "{kw}"` | id, author, text, **created_at**, likes, views, url | `created_at` (`%a %b %d %H:%M:%S %z %Y`) | 需要 |
| `trending` | rank, topic, tweets, category | **无** | 需要 |
| `timeline` | id, author, text, likes, retweets, replies, views, **created_at**, url | `created_at` | 需要 |
| `bookmarks` | author, text, likes, url | **无** | 需要 |

---

### Reddit `reddit`

**采集方式：** 脚本自动探测 opencli reddit 是否可用，不通则切换到 Reddit JSON API + 代理（`PROXY_CONFIG` 配置）。

#### opencli 模式（直连可用时）

| 命令 | 输出字段 | 时间字段 | 登录 |
|------|---------|---------|------|
| `search "{kw}"` | title, subreddit, author, score, comments, url | **无** | 不需要 |
| `hot` | rank, title, subreddit, score, comments | **无** | 不需要 |

#### API + 代理模式（直连不可用时，自��降级）

通过 `https://www.reddit.com/search.json` 和 `https://www.reddit.com/r/all/hot.json` 采集，`fetch_stack` 标记为 `reddit-api-proxy`。

```json
{
  "title": "帖子标题",
  "subreddit": "子版块名",
  "author": "用户名",
  "score": 1234,
  "comments": 56,
  "url": "https://reddit.com/r/...",
  "created_utc": 1775350202
}
```

| 字段 | 说明 |
|------|------|
| title | 帖子标题 |
| subreddit | 子版块 |
| author | 作者 |
| score | upvote 数 |
| comments | 评论数 |
| url | 帖子链接 |
| **created_utc** | **Unix 时间戳**（API 模式���有，opencli 模式无此字段） |

**备注：** API 模式比 opencli 模式多一个 `created_utc` 时间字段，可用于时间窗口筛选。

---

### Hacker News `hackernews`

| 命令 | 输出字段 | 时间字段 | 登录 |
|------|---------|---------|------|
| `top` | rank, title, score, author, comments | **无** | 不需要 |
| `new` | rank, title, score, author, comments | **无** | 不需要 |
| `search "{kw}"` | rank, title, score, author, comments, url | **无** | 不需要 |

---

### YouTube `youtube`

| 命令 | 输出字段 | 时间字段 | 登录 |
|------|---------|---------|------|
| `search "{kw}"` | rank, title, channel, views, duration, **published**, url | `published`（相对时间，如 `11 months ago`） | 不需要 |
| `transcript "{url}"` | 字幕文本 | — | 不需要 |

---

### arXiv `arxiv`

| 命令 | 输出字段 | 时间字段 | 登录 |
|------|---------|---------|------|
| `search "{kw}"` | id, title, authors, **published**, url | `published` (`YYYY-MM-DD`) | 不需要 |

---

### Product Hunt `producthunt`

| 命令 | 输出字段 | 时间字段 | 登录 |
|------|---------|---------|------|
| `hot` | 不稳定（多次超时） | — | 不需要 |
| `today` | rank, name, tagline, author, url | **无** | 不需要 |
| `posts` | rank, name, tagline, author, **date**, url | `date`（`YYYY-MM-DD`） | 不需要 |
| `browse <category>` | 未测试 | — | 不需要 |

**备注：** `hot` 不稳定，推荐用 `posts`（有日期字段）或 `today`。无搜索命令。

---

### Reuters `reuters`

| 命令 | 输出字段 | 时间字段 | 登录 |
|------|---------|---------|------|
| `search "{kw}"` | 未测试 | — | 不需要 |

---

## 三、通用能力

### Google `google`

| 命令 | 输出字段 | 时间字段 | 登录 |
|------|---------|---------|------|
| `search "{kw}"` | type, title, url, snippet | **无**（用 `after:` 在查询时过滤） | 不需要 |
| `news "{kw}"` | title, source, **date**, url | `date` | 不需要 |
| `trends` | title, traffic, **date** | `date` | 不需要 |

**备注：** 偶有 CAPTCHA 拦截。

### 网页抓取 `web read`

```bash
opencli web read --url "{url}"
```

输出 table：`title, author, publish_time, status, size`
内容保存为 Markdown 文件到 `./web-articles/` 目录。

---

## 四、时间字段汇总

### 有明确时间字段的命令

| 平台 | 命令 | 字段名 | 格式 | 示例 |
|------|------|--------|------|------|
| Twitter | search / timeline | `created_at` | `%a %b %d %H:%M:%S %z %Y` | `Fri Apr 03 14:00:17 +0000 2026` |
| 小红书 | search | `published_at` | `YYYY-MM-DD` | `2026-02-04` |
| 微博 | search / feed / comments | `time` | `MM月DD日 HH:MM` 或相对时间 | `04月01日 13:03` / `3小时前` |
| 36氪 | news / search | `date` | `YYYY-MM-DD` | `2026-04-05` |
| arXiv | search | `published` | `YYYY-MM-DD` | `2024-02-18` |
| Google | news | `date` | RFC 2822 | `Sat, 04 Apr 2026 12:00:01 GMT` |
| Google | trends | `date` | RFC 2822 | `Sat, 4 Apr 2026 18:30:00 -0700` |
| YouTube | search | `published` | 相对时间 | `11 months ago` / `2 days ago` |
| Product Hunt | posts | `date` | `YYYY-MM-DD` | `2026-04-03` |
| V2EX | topic（详情） | `created` | Unix 时间戳 | `1775279571` |
| Reddit | search/hot（API+代理模式） | `created_utc` | Unix 时间戳 | `1775350202` |
| B站 | comments | `time` | `YYYY-MM-DD HH:MM` | `2026-03-15 11:17` |

### 无时间字段的命令

微博 hot、小红书 feed/note、B站 hot/search/ranking、知乎 hot/search、V2EX hot/latest、Reddit search/hot（opencli 模式）、HackerNews top/new/search、Twitter trending/bookmarks、Google search

### collect_sources_with_opencli.py 中的统一时间提取顺序

脚本按以下顺序尝试提取时间字段（取第一个非空值）：

```
created_at → time → published_at → published → date → pub_date → created_utc(转换)
```

对应的平台映射：

| 字段名 | 对应平台 |
|--------|---------|
| `created_at` | Twitter search/timeline |
| `time` | 微博 search/feed/comments |
| `published_at` | 小红书 search |
| `published` | YouTube search, arXiv search |
| `date` | 36氪 news/search, Google news, Product Hunt posts |
| `created_utc` | Reddit API+代理模式（Unix 时间戳，脚本自动转为 `YYYY-MM-DD HH:MM`） |

### 筛选策略

- **有明确时间字段** → 解析后按时间窗口过滤
- **热榜/趋势类（无时间）** → 默认视为当天，保留
- **搜索结果无时间**（B站/知乎/HN/V2EX/Reddit opencli 模式） → 保留但标记 `time_status: unknown`，后续 AI 判断
- **Reddit API 模式** → 有 `created_utc`，可精确过滤
- **YouTube** → `published` 是相对时间（如 `2 days ago`），需特殊解析
- **微博** → `time` 格式不固定（`04月01日 13:03` / `今天08:04` / `3小时前`），需多种解析

### 2026-04-05 全量采集验证结果

| 平台 | 条目 | 成功率 | 时间字段可用 | 备注 |
|------|------|--------|------------|------|
| B站 | 170 | 16/16 ✅ | ❌ | 无时间字段 |
| 知乎 | 147 | 16/16 ✅ | ❌ | 无时间字段 |
| Hacker News | 340 | 17/17 ✅ | ❌ | 无时间字段 |
| Reddit (API) | 245 | 16/16 ✅ | ✅ created_utc | API+代理模式 |
| arXiv | 150 | 15/15 ✅ | ✅ published | — |
| Reuters | 150 | 15/15 ✅ | 未确认 | — |
| YouTube | 241 | 13/16 ⚠️ | ✅ published（相对时间） | 少量超时 |
| Twitter | 200 | 14/16 ⚠️ | ✅ created_at | 2个限流空返回 |
| 微博 | 100 | 8/16 ⚠️ | ✅ time | 50%搜索失败（限流） |
| 小红书 | 80 | 8/16 ⚠️ | ✅ published_at | 50%搜索失败（限流） |
| V2EX | 28 | 2/2 ✅ | ❌ | 只有 hot/latest |
| 量子位 | 25 | 3/4 ⚠️ | ❌ | web read 无时间 |
| InfoQ AI | 27 | 4/4 ✅ | ❌ | web read 无时间 |
| 36氪 | 20 | 1/17 ⚠️ | ✅ date | 大量超时 |
| OpenAI News | 17 | 4/4 ✅ | ❌ | web read 无时间 |
| TechCrunch | 13 | 3/4 ⚠️ | ❌ | web read 无时间 |
| Product Hunt | 6 | 1/2 ⚠️ | ❌ (today) / ✅ (posts) | hot 不稳定 |
| Anthropic News | 5 | 2/4 ⚠️ | ❌ | web read 无时间 |
| 即刻 | 0 | 7/16 ⚠️ | — | 需登录 |
| The Verge | 0 | 0/4 ❌ | — | 全部失败 |
| 机器之心 | 2 | 3/4 ⚠️ | ❌ | web read 无时间 |
