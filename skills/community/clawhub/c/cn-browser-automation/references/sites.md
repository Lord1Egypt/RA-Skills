# 常见国内站点选择器与反爬要点（模板）

> ⚠️ 重要：国内站点的 DOM 结构、class 名、反爬策略**变动频繁**。下面的选择器是“起点”，**每次使用前必须实际打开页面核验**，不要假设长期有效。核验方法：浏览器 DevTools → Elements 面板看真实结构，或用脚本 `--js "() => document.body.innerHTML.slice(0,500)"` 先看页面是否真加载了内容（很多站点是接口异步渲染，直接抓 HTML 会空）。
>
> ✅ **小红书、淘宝、B站** 已于 2026-08-06 用真实 Chrome（connect_over_cdp）实跑核验，选择器与提取 JS 见对应段落，可直接用。⚠️ **微博、知乎** 实跑发现未登录热榜/列表会被强反爬重定向（Page.evaluate 报 "Execution context was destroyed, because of navigation"），**必须登录态才能抓取**；**微信 / 12306** 强制登录、且 12306 涉及实名为高风险，仅做授权范围内的个人查询。所有未标 ✅ 的站点使用前务必复核。

## 通用反爬策略（适用所有站点）

1. **复用登录态**：本 skill 默认做法，比伪造 UA / cookie 更稳定。
2. **限速 + 随机延时**：循环抓取时 `time.sleep(random.uniform(1,3))`，勿高频。
3. **异步渲染**：优先用 `page.wait_for_selector` 等元素，而非固定 `sleep`。
4. **接口优先**：很多站点数据来自 XHR/JSON 接口（DevTools → Network → Fetch/XHR 里找带 `json` 的响应），直接抓接口比解析 DOM 更稳。脚本 `--js` 可 `fetch` 同域接口。
5. **滑块 / 验证码**：人工过一次再继续，**不要内置破解**。

## 小红书（xiaohongshu.com）✅ 已实跑核验（2026-08-06）

- 场景：发现页 / 搜索结果笔记列表、笔记详情、用户主页。
- 登录态：未登录时信息流仍渲染（探索页约 30 张卡片），但会浮登录墙（`.login-btn`）；搜索 / 详情部分内容需登录。用本 skill 复用登录态可去除限制。
- 笔记卡片真实结构（探索页 `https://www.xiaohongshu.com/explore`，实测 30 张）：
  - 卡片容器：`section.note-item`，带 `data-note-id="6a584f24..."`（即笔记 ID）。
  - 标题：`.note-item .title`（文本，如「天意cp又分手了💔」）。
  - 作者名：`.note-item .name`；头像：`.author-avatar`。
  - 点赞数：`.note-item .count`（位于 `.like-wrapper` 内，如「1340」）。
  - 封面图：`.note-item .cover img` 的 `src`。
  - 详情链接：`a.cover` 的 `href`，形如 `/explore/{noteId}?xsec_token=...&xsec_source=`（**必须带 xsec_token，否则详情页可能 404 / 触发风控**）；拼 `https://www.xiaohongshu.com` 得完整 URL。
- 推荐提取 JS（探索页 / 搜索页通用，直接可用）：
  ```js
  () => [...document.querySelectorAll('.note-item')].map(el => ({
    noteId: el.getAttribute('data-note-id'),
    title: (el.querySelector('.title') || {}).textContent?.trim(),
    author: (el.querySelector('.name') || {}).textContent?.trim(),
    likeCount: (el.querySelector('.count') || {}).textContent?.trim(),
    cover: (el.querySelector('.cover img') || {}).getAttribute?.('src'),
    url: 'https://www.xiaohongshu.com' + (el.querySelector('a.cover')?.getAttribute('href') || '')
  }))
  ```
- 搜索页：`https://www.xiaohongshu.com/search_result?keyword=关键词`，列表卡片结构同上（`.note-item`）。
- 反爬要点：高频必出验证码 / 滑块，加随机延时；详情页 URL 必须带 `xsec_token`（来自列表卡片 href，不要自己拼 note-id）；遇滑块先在浏览器人工过一次再让脚本继续。

## 淘宝 / 天猫（taobao.com / tmall.com）✅ 已实跑核验（2026-08-06）

- 场景：首页推荐流、搜索结果列表、商品详情、店铺。
- ⚠️ 登录态硬性要求（实测）：**搜索结果页在未登录 / 脚本会话下，商品卡片是空骨架**（`.boneClass_cardWrapper` 内 title/price 全空，仅 `lightSlideAnimation` 加载动画），即便关键词正确、等待 9 秒也不返回数据。**必须复用登录态后数据才填充**——这正是本 skill 的核心价值。首页"猜你喜欢"未登录也能渲染真实商品卡。
- 首页"猜你喜欢"商品卡（实测 38 个，已取到真实标题/价格/链接）：
  - 卡片容器：`.tb-pick-content-item`，带 `data-nid="979307585809"`（即商品 ID）。
  - 链接：`a.item-link`，`href="//item.taobao.com/item.htm?id=..."`（拼 `https:` 得详情页）；`data-nid` 即商品 ID。
  - 图片：`.product-img`（来自 `img.alicdn.com`）。
  - 标题：`.info-wrapper-title-text`（或 `.info-wrapper-title`）。
  - 价格：`.price-value`（如「6.01」）。
  - 月销：`.month-sale`（部分卡片为空）。
- 搜索结果页卡片（需登录才填充）：
  - 容器：`.boneClass_cardWrapper`；标题 `.boneClass_title`、价格 `.boneClass_price`、图片 `.boneClass_mainImg`、店铺 `.boneClass_shopInfo`、卖点 `.boneClass_salesPoint`、摘要 `.boneClass_abstract`。
  - 这些是**稳定语义类**（无 `--` 哈希后缀），比首页 CSS-Module 哈希类（如 `info-wrapper-title-text--xxxx`）更可靠；但若某天变哈希，需重新核验。
- 推荐提取 JS（首页推荐流，直接可用）：
  ```js
  () => [...document.querySelectorAll('.tb-pick-content-item')].map(el => ({
    nid: el.getAttribute('data-nid'),
    title: (el.querySelector('.info-wrapper-title-text') || el.querySelector('.info-wrapper-title') || {}).textContent?.trim(),
    price: (el.querySelector('.price-value') || {}).textContent?.trim(),
    url: 'https:' + (el.querySelector('a.item-link')?.getAttribute('href') || '')
  }))
  ```
- 反爬要点：搜索 / 详情务必登录态；降低并发 + 随机延时；详情与价格优先抓接口 `https://h5api.m.taobao.com/...`（需带登录 cookie，本 skill 已具备）；遇滑块先在浏览器人工过一次。

## 微信 / 公众号（weixin.qq.com / mp.weixin.qq.com）

- 场景：公众号文章导出、历史文章列表。
- 登录态：必须扫码登录公众号后台或微信。
- 提示：文章页 `mp.weixin.qq.com/s?__biz=...` 可直接读 DOM；历史文章需后台。尊重版权，仅导出授权内容。

## 微博（weibo.com）⚠️ 待登录态核验（2026-08-06 实跑：未登录热搜榜被强反爬重定向）

- 场景：微博信息流、用户主页、热搜榜、搜索。
- ⚠️ 实跑发现（2026-08-06）：在脚本会话（未登录）下访问 `https://s.weibo.com/top/summary?cate=realtimehot` 会被**强反爬直接重定向 / 跳转**（Page.evaluate 报 "Execution context was destroyed, because of navigation"），抓不到任何内容。**必须复用登录态后才能在已登录 Chrome 上抓取**——再次印证本 skill 「登录态复用」的核心价值。
- 选择器（待你登录态核验，以下为预期、未实跑）：信息流卡片 `.WB_feed_type` / `.card-wrap`；正文 `.WB_text` / `.txt`；用户名 `.name`；时间 `.WB_from`；热搜榜条目 `.td-01` / `.td-02`（旧版类名，新版可能已变，务必复核）。
- 提示：信息流异步加载、滚动触发，用 `--wait` 等元素；登录态下优先抓 `weibo.com/ajax/...` 类接口更稳。

## B站（bilibili.com）✅ 已实跑核验（2026-08-06）

- 场景：视频排行榜、视频信息、UP 主稿件、评论。
- 登录态：排行榜 / 公开视频页**无需登录即可渲染完整数据**（实测 100 张榜单一屏全出），是这几个站点里 DOM 最干净、最适合做「DOM 抓取示范」的站点，无 CSS-Module 哈希类。
- 排行榜页（实测，`https://www.bilibili.com/v/popular/rank/all`，100 条全渲染）：
  - 卡片容器：`li.rank-item`，带 `data-id` / `data-rank`（排名）。
  - 排名：`li[data-rank]` 或 `i.num span` 文本（如「1」）。
  - 标题：`a.title`（文本=标题；`href="//www.bilibili.com/video/BVxxxx"` 是**协议相对 URL，需补 `https:`**）。
  - 封面：`img.cover`（属性 `src` 与 `data-src` 都有值，`lazy="loaded"` 后用 `src` 即可）。
  - UP 主：`.up-name`（在 `div.detail` 内，外层是 `space.bilibili.com` 链接；注意是 `span.data-box.up-name`，**不是** `a.up-name`）。
  - 播放 / 弹幕：`div.detail` 文本，如「307.3万 1.7万」（空格分隔：播放量 弹幕数）；也可用 `.detail .data-box` 分别取（第一个=播放，第二个=弹幕，第三个=时长）。
- 推荐提取 JS（排行榜，直接可用）：
  ```js
  () => [...document.querySelectorAll('li.rank-item')].map(el => {
    const a = el.querySelector('a.title');
    const cov = el.querySelector('img.cover');
    // 注意：.detail 内第一个 .data-box 是 UP主(.up-name)，需过滤掉再取播放/弹幕
    const boxes = [...el.querySelectorAll('.detail .data-box')].filter(b => !b.classList.contains('up-name'));
    return {
      rank: (el.querySelector('i.num span') || {}).textContent?.trim() || el.getAttribute('data-rank'),
      title: a?.textContent?.trim(),
      url: 'https:' + (a?.getAttribute('href') || ''),
      up: (el.querySelector('.up-name') || {}).textContent?.trim(),
      cover: cov?.getAttribute('src') || cov?.getAttribute('data-src'),
      play: boxes[0] ? boxes[0].textContent.trim() : null,
      danmaku: boxes[1] ? boxes[1].textContent.trim() : null
    };
  })
  ```
- 反爬要点：DOM 极稳定（无哈希类），公开页基本无反爬；登录态主要用于抓个人历史 / 私信等。想拿更全元数据（点赞 / 投币 / 收藏 / 评论数）可走接口 `api.bilibili.com`（`--js` 内 `fetch` 同域接口，带登录 cookie 才拿全）。

## 12306（kyfw.12306.cn）

- 场景：余票查询、订单。
- 提示：反爬极强且涉及实名，谨慎操作；余票公开接口 `https://kyfw.12306.cn/otn/...` 需带会话。仅做个人查询，勿批量刷。

## 知乎（zhihu.com）⚠️ 待登录态核验（2026-08-06 实跑：未登录热榜被强反爬重定向）

- 场景：热榜、回答、文章、搜索。
- ⚠️ 实跑发现（2026-08-06）：未登录脚本会话访问 `https://www.zhihu.com/hot` 同样被**强反爬重定向**（Page.evaluate 报 "Execution context was destroyed, because of navigation"），与微博一致。**必须复用登录态后才能在已登录 Chrome 抓取**——印证本 skill 「登录态复用」价值。
- 选择器（待登录态核验，以下为预期、未实跑）：热榜条目 `.HotItem` / `.ContentItem`；标题 `.ContentItem-title` 或 `a[href*="/question/"]`；热度 `.HotItem-metrics`；回答列表 `.List-item` / `.AnswerCard`。
- 提示：信息流异步加载，用 `--wait` 等元素；登录态下优先抓 `www.zhihu.com/api/v3/...` 接口更稳。

## 如何新增一个站点模板

1. 浏览器手动登录并打开目标页。
2. DevTools 看真实选择器 / 找数据接口。
3. 用脚本先 `--js` 验证能拿到数据：
   `python scripts/connect_chrome.py <url> --js "() => ({n: document.querySelectorAll('.<cls>').length})" --out probe.json`
4. 把可用的选择器 / 接口写进本文件对应段落，标注核验日期。

## 配套抓取脚本（scripts/，已固化可一键跑）

下列脚本复用 `connect_chrome.py` 的连接逻辑（经 `cn_browser.py` 封装），把对应站点的提取 JS 落成开箱即用的命令行工具，列表 → JSON / CSV：

| 脚本 | 目标 | 登录态需求 | 默认输出 |
|---|---|---|---|
| `xhs_scrape.py` | 小红书笔记列表（探索页 / 搜索） | 探索页免登录，搜索更佳 | `xhs_notes.json` |
| `tb_scrape.py` | 淘宝商品列表（首页 / 搜索） | 首页免登录，搜索须登录 | `tb_items.json` |
| `bili_scrape.py` | B站排行榜（免登录） | 免登录 | `bili_rank.json` |

通用参数（三个脚本一致）：
- `--launch`：若 CDP 端口未开，启动独立 profile Chrome（首次会自动打开浏览器）。
- `--port 9222` / `--user-data-dir <dir>`：指定远程调试端口与登录态目录。
- `--out <file.json>`：JSON 输出路径；`--csv <file.csv>`：额外导出 CSV（UTF-8-sig，Excel 友好）。
- `--wait <选择器或秒数>`：覆盖默认等待策略。

示例：
```bash
# 抓小红书探索页 → json + csv
python scripts/xhs_scrape.py --launch --csv xhs.csv
# 抓淘宝搜索"手机"（需登录态：先 --launch 在弹出浏览器登录一次）
python scripts/tb_scrape.py --search 手机 --launch --csv tb.csv
# 抓 B站全站排行榜（免登录）
python scripts/bili_scrape.py --csv bili.csv
```

> 提示：要复用你**真实**登录态，不要加 `--launch`，而是参考 setup.md 用你的用户目录启动 Chrome（端口 9222），脚本直连即可拿到已登录内容。
