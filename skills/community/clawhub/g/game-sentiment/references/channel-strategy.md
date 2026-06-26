# Channel Strategy

## Channel Tiers

### Tier 1 — Stable (verified working)
| Channel | Method | Role | Status |
|---------|--------|------|--------|
| Weibo | Playwright + m.weibo.cn API | 社交热点、玩家投诉、负面舆情主阵地 | ✅ |
| TapTap | Playwright | 评分评论、新手体验反馈 | ✅ |
| NGA | Playwright + 登录 | 核心玩家讨论、版本/平衡深度反馈 | ✅ (需凭据) |
| Baidu Tieba | Playwright | 大众玩家日常、草根反馈 | ✅ |
| Bilibili | Playwright | 视频内容生态、传播热度 | ✅ |
| Game media | web_search + web_fetch | 媒体视角、深度报道、品牌叙事 | ✅ |
| YouTube | YouTube Data API v3 | 海外评测/吐槽视频、评论区反馈 | ✅ |

### Tier 2 — Degraded (web_search)
| Channel | Method | Role | Status |
|---------|--------|------|--------|
| Reddit | web_search (降级) | 海外核心社区、版本讨论、玩家吐槽 | ✅ L2 |
| X (Twitter) | web_search (降级) | 海外舆情传播最快平台、KOL/玩家即时反馈 | ✅ L2 |

### Tier 3 — Blocked
| Channel | Method | Status | 解决路径 |
|---------|--------|--------|---------|
| Zhihu | Playwright | ❌ frozen | 需代理 IP（Azure VM IP 被拦） |

## Channel Roles

| Type | Purpose |
|------|---------|
| App stores | Rating changes, post-update negative reviews, conversion risk |
| Core communities | Deep disputes, high-quality feedback, balance/rule discussions |
| Social/video | Spread speed, viral risk, KOL amplification, meme-ification |
| Media/long-form | Long-term reputation, brand narrative, search impression |

## Healthcheck Protocol

Before each run, for each enabled channel:
1. Send one lightweight probe request (e.g., search for game name)
2. Check if response contains meaningful content (not login wall, CAPTCHA, empty page)
3. If probe fails → mark channel as **unavailable this run**, continue with others
4. Log healthcheck results in report metadata

## Degradation Rules

- Channel fails healthcheck → skip, mark in report
- Channel fails mid-collection → save what was collected, mark partial
- **Freeze rule**: If a channel fails healthcheck on 3+ consecutive runs, mark as "frozen" in this file with date and reason. Frozen channels are excluded from future runs until manually reviewed.

## Per-Channel Collection Methods (Verified)

### Weibo (Playwright + API) ✅
**最佳数据源**。使用 m.weibo.cn JSON API，返回结构化数据。

1. `browser_navigate` to `https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D61%26q%3D{URL_ENCODED_QUERY}&page_type=searchall`
2. `browser_evaluate` 提取 JSON：
```javascript
() => {
  const d = JSON.parse(document.body.innerText);
  return JSON.stringify(d.data.cards.filter(c => c.mblog).map(c => ({
    text: c.mblog.text.replace(/<[^>]+>/g,''),
    time: c.mblog.created_at,
    user: c.mblog.user?.screen_name,
    likes: c.mblog.attitudes_count,
    comments: c.mblog.comments_count,
    reposts: c.mblog.reposts_count
  })).slice(0,10))
}
```
3. 建议多组关键词搜索：通用、+外挂、+盗号、+优化、+客服、+bug 等
4. 跨关键词去重：同账号+前50字相同 → 合并

### TapTap (Playwright) ✅
1. `browser_navigate` to `https://www.taptap.cn/search?kw={GAME_NAME}` 动态查找 APP ID
2. 验证游戏名匹配后，进行**双排序采集** <!-- [2026-04-05] #21 TapTap 双排序采集规避水军 -->

**第一轮：最新排序**
3. `browser_navigate` to `https://www.taptap.cn/app/{APP_ID}/review?order=new`
4. 等待 3 秒渲染
5. `browser_evaluate` 精准提取评论数据： <!-- [2026-04-05] #13 TapTap 精准 evaluate 脚本 -->
```javascript
() => {
  const reviews = [];
  document.querySelectorAll('[class*="review-item"], [class*="ReviewItem"], .review-card, article').forEach(el => {
    const text = el.querySelector('[class*="content"], [class*="text"], p')?.textContent?.trim() || '';
    const user = el.querySelector('[class*="user-name"], [class*="author"], [class*="nickname"]')?.textContent?.trim() || '';
    const rating = el.querySelector('[class*="score"], [class*="rating"], [class*="star"]')?.textContent?.trim() || '';
    const time = el.querySelector('[class*="time"], [class*="date"], time')?.textContent?.trim() || '';
    if (text.length > 10) reviews.push({ text: text.slice(0, 500), user, rating, time, sort: 'newest' });
  });
  return JSON.stringify(reviews.slice(0, 15));
}
```

**第二轮：最差排序（穿透水军）** <!-- [2026-04-05] #21 -->
6. `browser_navigate` to `https://www.taptap.cn/app/{APP_ID}/review?order=worst` （或 `score=1`，需测试实际 URL 参数）
7. 等待 3 秒渲染
8. 同样 evaluate 脚本提取（sort 标记为 'worst'）
9. 合并两轮数据，标记来源排序方式

10. **Fallback**：如精准脚本返回空或 <3 条，改用 `() => document.body.innerText.slice(0, 15000)` <!-- [2026-04-05] #14 fallback 兜底（15000字符上限） -->

### NGA (Playwright + 登录) ✅
**需要登录**。凭据从 `.credentials/accounts.json` 读取。

1. `browser_navigate` to NGA 登录页
2. 点击"使用密码登录"
3. `browser_evaluate` 操作 iframe DOM（name="iff"）填入用户名密码：
```javascript
(el) => {
  const doc = el.contentDocument;
  const inputs = doc.querySelectorAll('input[type="text"], input[type="password"], input:not([type])');
  inputs[0].value = USERNAME; inputs[0].dispatchEvent(new Event('input', {bubbles:true}));
  inputs[1].value = PASSWORD; inputs[1].dispatchEvent(new Event('input', {bubbles:true}));
}
```
4. 点击登录 → 处理 6 位数字图形验证码（截图 + AI 识别）→ 确认弹窗
5. 导航到版块：`https://bbs.nga.cn/thread.php?fid={FID}&order_by=postdatedesc`
6. 可能遇到广告页，点击"跳过广告"
7. `browser_evaluate` 提取 `document.body.innerText`

### 贴吧 (Playwright) ✅
**三级提取策略**（贴吧新版 Vue SPA 导致传统 DOM 选择器不稳定） <!-- [2026-04-05] #22 贴吧三级提取策略 -->

1. `browser_navigate` to `https://tieba.baidu.com/f?kw={GAME_NAME_ENCODED}&ie=utf-8&tp=0`
2. 等待 3 秒渲染

**Level 1（优先）：Accessibility Snapshot** <!-- [2026-04-05] #22 -->
3. `playwright.browser_snapshot` 获取 accessibility tree
4. 从 snapshot 文本中正则提取帖子：标题（link text）、作者、回复数、时间
5. 如提取到 ≥3 条帖子，使用此结果

**Level 2：精准 Evaluate** <!-- [2026-04-05] #15 贴吧精准 evaluate 脚本 -->
6. 如 Level 1 不足 3 条，执行 `browser_evaluate`：
```javascript
() => {
  const posts = [];
  document.querySelectorAll('#thread_list .j_thread_list, .threadlist_lz, [class*="thread-item"]').forEach(el => {
    const title = el.querySelector('.j_th_tit a, .threadlist_title a, [class*="title"] a')?.textContent?.trim() || '';
    const preview = el.querySelector('.threadlist_abs, .threadlist_text, [class*="abstract"]')?.textContent?.trim() || '';
    const author = el.querySelector('.frs-author-name, .tb_icon_author, [class*="author"]')?.textContent?.trim() || '';
    const replies = el.querySelector('.threadlist_rep_num, [class*="reply-num"]')?.textContent?.trim() || '';
    const time = el.querySelector('.threadlist_reply_date, .is_show_create_time, [class*="time"]')?.textContent?.trim() || '';
    if (title) posts.push({ title, preview: preview.slice(0, 200), author, replies, time });
  });
  return JSON.stringify(posts.slice(0, 20));
}
```

**Level 3（兜底）：InnerText Fallback** <!-- [2026-04-05] #14 fallback 兜底 -->
7. 如 Level 2 也不足 3 条，执行 `() => document.body.innerText.slice(0, 15000)`

8. 报告中标注使用的提取级别（L1/L2/L3）
9. 免登录，帖子列表+正文预览可直接获取

### B站 (Playwright) ✅
1. `browser_navigate` to `https://search.bilibili.com/all?keyword={GAME_NAME_ENCODED}&order=pubdate`
2. 等待 3 秒渲染
3. `browser_evaluate` 精准提取视频列表： <!-- [2026-04-05] #16 B站精准 evaluate 脚本 -->
```javascript
() => {
  const videos = [];
  document.querySelectorAll('.video-list-item, .bili-video-card, [class*="video-card"]').forEach(el => {
    const title = el.querySelector('.bili-video-card__info--tit, h3, [class*="title"]')?.textContent?.trim() || '';
    const author = el.querySelector('.bili-video-card__info--author, [class*="owner"], [class*="up-name"]')?.textContent?.trim() || '';
    const views = el.querySelector('.bili-video-card__stats--item, [class*="play"], [class*="view"]')?.textContent?.trim() || '';
    const time = el.querySelector('.bili-video-card__info--date, [class*="time"], [class*="pubdate"]')?.textContent?.trim() || '';
    if (title) videos.push({ title: title.slice(0, 200), author, views, time });
  });
  return JSON.stringify(videos.slice(0, 20));
}
```
4. **Fallback**：如精准脚本返回空或 <3 条，改用 `() => document.body.innerText.slice(0, 15000)` <!-- [2026-04-05] #14 fallback 兜底 -->
5. 获取视频标题、播放量、发布时间（分钟级精度）

### 游戏媒体 (web_search + web_fetch) ✅
1. `web_search("{game_name} {YYYY年M月} site:17173.com OR site:gamersky.com")`
2. `web_fetch` 抓取搜索到的文章 URL，获取完整文章内容
3. 补充搜索：`web_search("{game_name} 争议/评测/更新")` 发现更多报道

### Zhihu ❌ (frozen)
Azure VM IP 被拦，安全验证无法通过。需代理 IP。

### Reddit ✅ (web_search 降级)
Azure VM IP 被 Reddit 全面封锁（网页/JSON/RSS 全 403），改用 web_search 间接获取。

1. `web_search("site:reddit.com r/{subreddit} {game_name} {keyword}")` 获取帖子摘要和链接
2. 可按关键词分组搜索：通用、+bug、+update、+complaint、+nerf 等
3. web_search 返回的 AI 摘要包含帖子主题、社区情绪和讨论要点，可直接用于舆情分析
4. citations 中的 URL 可用于引用（但 web_fetch 抓取同样会 403，仅做引用链接用）
5. 证据等级：L2（间接，经搜索引擎摘要），非 L1
6. 限制：无法获取精确时间戳、互动数据（upvote/comment count），样本深度有限

### X / Twitter ✅ (web_search 降级)
X/Twitter 需登录才能查看内容，Nitter 公共实例已失效，改用 web_search 间接获取。

1. `web_search("site:x.com {game_name} {keyword}")` 获取推文摘要和讨论要点
2. 可按关键词分组搜索：通用、+bug、+nerf、+maintenance、+complaint、+update 等
3. 补充搜索不带 site 限制：`web_search("{game_name} twitter controversy/backlash {YYYY}")` 捕获媒体转引的推文
4. web_search 返回 AI 摘要 + citations（推文链接），可用于引用
5. 证据等级：L2（间接，经搜索引擎摘要），非 L1
6. 限制：无精确时间戳、互动数据（likes/retweets），样本覆盖取决于搜索引擎索引深度
7. 优势：X 是海外舆情爆发最快的渠道，即使 L2 也能捕捉到重大事件和 KOL 发声

### YouTube ✅ (Data API v3)
使用 YouTube Data API v3 官方接口，API key 存于 `.credentials/accounts.json`。

1. 搜索视频：`GET https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&order=date&maxResults=10&key={API_KEY}`
2. 可加参数：`publishedAfter={ISO8601}` 限制时间范围，`relevanceLanguage=zh` 或 `en` 限制语言
3. 获取视频详情（播放量、点赞、评论数）：`GET https://www.googleapis.com/youtube/v3/videos?part=statistics,snippet&id={videoId}&key={API_KEY}`
4. 获取视频评论：`GET https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={videoId}&maxResults=20&order=relevance&key={API_KEY}`
5. 关键词分组搜索：{游戏名}+review、+bug、+rant、+nerf、+update、+controversy 等
6. 证据等级：L1（官方 API，结构化数据，精确时间戳+互动数据）
7. 配额：每天 10,000 units，search=100u/次，videos=1u/次，commentThreads=1u/次
8. 建议每次舆情扫描使用 ≤2000 units（约 20 次搜索 + 详情/评论查询）

## Actual Availability Status

> Updated after each real test. Fill in during Phase B.

| Channel | Last Tested | Status | Notes |
|---------|-------------|--------|-------|
| Weibo | 2026-04-04 | ✅ working | m.weibo.cn JSON API via Playwright，结构化数据（正文、精确时间、用户、互动数），免登录，支持多关键词搜索 |
| Bilibili | 2026-04-04 | ✅ working | Playwright 搜索页渲染，视频标题+播放量+发布时间（分钟级精度），免登录 |
| Zhihu | 2026-04-04 | ❌ frozen | Azure VM IP 被拦，安全验证无法通过（点击验证无效），需代理 IP |
| Tieba | 2026-04-04 | ✅ working | Playwright 渲染，帖子列表+正文内容可提取，免登录 |
| NGA | 2026-04-04 | ✅ working | Playwright + 登录（iframe DOM 操作 + 6位数字验证码 AI 识别），凭据存 .credentials/accounts.json |
| Reddit | 2026-04-05 | ✅ working | web_search 间接获取（JSON/RSS/网页全 403），L2 证据，无精确时间戳和互动数据 |
| Media (17173) | 2026-04-04 | ✅ working | web_fetch 直取，完整原文，L1 证据 |
| Media (游民星空) | 2026-04-04 | ✅ working | web_fetch 直取，完整原文，L1 证据 |
| TapTap | 2026-04-04 | ✅ working | Playwright 渲染评论页，评论全文+评分，免登录 |
| Google Play | — | untested | |
| App Store | — | untested | |
| X (Twitter) | 2026-04-05 | ✅ working | web_search 间接获取（x.com 需登录，Nitter 已失效），L2 证据，海外舆情爆发最快渠道 |
| YouTube | 2026-04-05 | ✅ working | YouTube Data API v3，L1 证据（精确时间戳、播放量、评论），每天 10,000 units 免费额度 |

### Playwright MCP 接入方式

已通过 `mcporter` 确认 Playwright MCP server 可用（22 个工具），主要使用：
- `playwright.browser_navigate` — 导航到目标 URL
- `playwright.browser_snapshot` — 获取页面结构化 snapshot
- `playwright.browser_evaluate` — 执行 JS 提取数据
- `playwright.browser_close` — 关闭页面

**微博特殊路径**：直接访问 `m.weibo.cn/api/container/getIndex` API 端点，返回完整 JSON（无需页面渲染），包含微博正文、发布时间（精确到秒）、用户信息、互动数据。

## Channel Boundary Rules

When a single collection run includes content from multiple sites (which is the default behavior of web_search), the report MUST:
1. Label the collection as "cross-channel aggregation" (跨渠道聚合)
2. Tag each piece of evidence with its actual source site
3. NOT describe results as "single-channel" output
