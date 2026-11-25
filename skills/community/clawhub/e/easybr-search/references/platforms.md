# 站点目录与 DOM 提取范围

`scripts/platforms.mjs` 登记公开搜索入口、内容链接模式与 DOM 选择器提示；`scripts/extract.mjs` 生成自包含的只读 JavaScript 表达式。使用当前已登录的真实浏览器读取页面，不调用站内私有 API，不读取 Cookie、storage 或账号令牌，不尝试处理验证码。

## 配置与验收分开

本目录的 15 个固定配置统一标记 `verification.status: template-only`、`browserValidated: false`。这表示代码中存在入口和提取规则，不能据此宣称每个平台、账号或浏览器都已验收。每次运行的浏览器、页面、实际结果与阻断状态由运行报告记录，独立于静态目录。

网页 DOM 会变化，登录、地区、内容类型和浏览器环境也会改变可见结果。没有提取到条目且没有明确空结果提示时，不把它写成“这个关键词没有内容”。配置中的选择器是候选提示；不依赖某个站点永久保留某个 class。

## 固定平台

模板中的 `{query}` 由 `searchURL(id, query)` 编码为单个查询值；抖音使用编码后的路径段。

| ID | 公开搜索入口模板 | 接受的内容链接 | 排除示例 |
| --- | --- | --- | --- |
| `bilibili` | `https://search.bilibili.com/all?keyword={query}` | `/video/BV…`、`/video/av…`、`/read/cv…`、`/opus/…` | UP 主空间、分区与导航 |
| `xiaohongshu` | `https://www.xiaohongshu.com/search_result?keyword={query}&source=web_search_result_notes` | `/search_result/<note-id>`、`/explore/<note-id>`、`/discovery/item/<note-id>` | `/user/profile/…` |
| `douyin` | `https://www.douyin.com/search/{query}?type=general` | `/video/<id>`、`/note/<id>`，或带明确 `modal_id` 的内容搜索链接 | `/user/…`、普通搜索导航 |
| `zhihu` | `https://www.zhihu.com/search?type=content&q={query}` | 问题、回答、专栏文章 | `/people/…`、登录页 |
| `csdn` | `https://so.csdn.net/so/search?q={query}&t=all` | `blog.csdn.net/<author>/article/details/<id>` | 作者首页、社区导航 |
| `juejin` | `https://juejin.cn/search?query={query}&type=0` | `/post/<id>` | `/user/…` |
| `weibo` | `https://s.weibo.com/weibo?q={query}` | 用户数值 ID 下的单条微博、`/status/…`、`/detail/…` | `/u/…` 作者页 |
| `toutiao` | `https://www.toutiao.com/search/?keyword={query}` | `/article/…`、`/video/…`、`/w/a…` | 作者与搜索导航 |
| `youtube` | `https://www.youtube.com/results?search_query={query}` | `/watch?v=…`、`/shorts/…`、`youtu.be/…` | 频道与播放列表 |
| `x` | `https://x.com/search?q={query}&src=typed_query&f=live` | `/<user>/status/<id>` | 用户主页、导航 |
| `reddit` | `https://www.reddit.com/search/?q={query}` | `/r/<community>/comments/<id>/…` | 用户与社区首页 |
| `github` | `https://github.com/search?q={query}&type=repositories` | 仓库及代码、issue、pull request 等内容 | 作者主页、stars/forks 列表、产品导航 |
| `bing` | `https://www.bing.com/search?q={query}` | 普通网页搜索结果；解码 `ck/a` 的 `u=a1…` 跳转 | 搜索设置、引擎内导航和显式广告 |
| `baidu` | `https://www.baidu.com/s?wd={query}` | 普通网页结果；保留无法在 DOM 中解码的 `/link?url=…` 导航地址 | 搜索导航、显式广告 |
| `google` | `https://www.google.com/search?q={query}` | 普通网页结果；还原 `/url` 中明确的 HTTPS 目标，保留地区站 `/goto` 与不透明 `/url` 跳转 | 账号、偏好和搜索导航 |

别名：`bili`、`b站` → `bilibili`；`xhs`、`小红书` → `xiaohongshu`；`twitter` → `x`。未知 ID 返回 `unknown_platform`，不静默变成另一个平台。

Google/Bing 此处读取普通搜索结果，不宣称已采集 AI Mode、AI Overview、Copilot 回答或原生引用。Reddit 的普通帖子搜索也不等于其 Ask AI 回答；两者须分别验证。

## 任意公开域名的索引扩展

```js
searchURL('site:example.com', '多账号内容管理')
// https://www.google.com/search?q=site%3Aexample.com%20...
```

`site:` 接受纯域名，不接受 URL 路径、端口、凭据或额外参数。它通过 Google 的 `site:` 运算符检索，提取时只保留该域名及其子域名结果；这是公开网页索引搜索，不是该网站的原生搜索，也不保证覆盖全部已发布内容。

`inferPlatform(url)` 按主机边界识别固定平台；未知 HTTP(S) 域名返回 `site:<hostname>`，不把 `google.com.evil.example` 当作 Google。非 HTTP(S) 或带嵌入凭据的 URL 返回 `null`。

## 提取返回与边界

搜索返回页面 URL、标题、`readyState`、条目、阻断/空结果/加载状态，以及匹配卡片和链接数量。每条条目保留标题、原始完整导航 URL、摘要、作者、页面所示时间、原始互动文字与内容类型。标题优先使用标题属性或内容标题节点，DOM 高亮标签不进入文字；同卡片和同内容去重，作者链接不混作内容。

小红书等内容链接的签名参数保留在内部导航 URL；发布报告前应由结果层区分私有导航地址与可公开的 canonical URL，不将安全参数复制到公开报告。百度及 Google 的不透明跳转只记实际 wrapper 链接，不能靠猜测写出落地域名；可由运行器在新的任务标签中正常导航并记录最后页面。只将已识别的搜索前端根主机视为搜索导航，不按父域排除 Google Cloud、开发者文档或百度百家号内容。

详情返回 `url`、`canonicalUrl`、`readyState`、标题、正文、作者、时间、内容类型和状态。正文优先来自站点正文节点、`article` 或 `main`，跳过导航、侧栏、页脚、推荐与评论区；没有找到正文时保留空文本，不把整个 body 当文章。canonical 缺失时沿用实际页面 URL，不拼造地址。

视频页的文字仅是当前页面的标题、说明或可见内容，不表示已播放、看完、识别画面或生成转录。发布日期与播放时长分开；计数只保留页面原文，不推算阅读量或真实传播效果。

明确可见的登录或验证码覆盖会清空条目/正文，即使背景仍存在卡片；隐藏弹窗、普通导航中的登录按钮不会自动阻断。未运行、加载中、明确空结果和验证失败分别保留。

默认搜索 `limit=10`、`maxText=12000`，详情 `maxText=16000`。`limit` 接受 0–100，`maxText` 接受 1–200000 的整数；搜索文字总预算涵盖标题、摘要、作者、时间和互动原文，完整导航 URL 不截断成无效链接。

## 公开资料依据

以下资料用于核对搜索类型与入口行为，不代替当前浏览器 DOM 验收：

- [Google 搜索运算符说明](https://support.google.com/websearch/answer/2466433)：`site:` 是限定网站的搜索运算符。
- [GitHub 搜索说明](https://docs.github.com/en/search-github/getting-started-with-searching-on-github/about-searching-on-github)：仓库、用户与代码有不同搜索类型，跨公共仓库代码搜索可能需要登录。
- [Reddit 搜索类型说明](https://support.reddithelp.com/hc/en-us/articles/19695647891988-How-does-Reddit-search-work)：帖子、社区、用户等结果与 Ask 入口应分别处理。
- [Bilibili 公开搜索示例](https://search.bilibili.com/all?keyword=geo)：搜索内容可包含视频、作者与其他类型，不能把全部链接直接当视频结果。

离线测试使用内存 DOM 夹具验证提取边界，命令为 `node --test tests/platforms.test.mjs tests/extract.test.mjs`。实际跨浏览器、登录环境和站点验收以当次运行报告为准。
