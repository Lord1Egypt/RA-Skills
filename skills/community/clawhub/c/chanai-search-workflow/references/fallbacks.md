# 搜索失败回退策略

## 目标
当主搜索入口不稳定、被拦、结果太弱或噪音太大时，快速切到下一条可用路径，而不是停在单一搜索引擎失败上。

## 总原则
1. 先判断失败类型：
   - **引擎限制**：参数不支持、接口能力不足
   - **抓取失败**：网页抓取被拦、超时、特殊 IP 限制
   - **结果质量差**：有结果但太泛、太旧、太噪
2. 同一家族先切备用引擎
3. 还不行再切到另一家族交叉搜
4. 对高价值问题，最后可用 `exec + curl`/公开搜索页抓取做最终 fallback

## 国内优先路径的 fallback

### 通用网页搜索
- 主：Baidu
- 备 1：Bing CN
- 备 2：Sogou
- 备 3：360

### 内容社区搜索
- Zhihu 结果弱 → `site:zhihu.com` + Google/Baidu
- Bilibili 结果弱 → 直接用 B站搜索页，或 `site:bilibili.com`
- 小红书抓取不稳 → 优先 `site:xiaohongshu.com` with Google/Baidu
- WeChat 搜不到 → 用更宽关键词重新搜 + 百度站内搜索公众号名称

## 国际优先路径的 fallback

### 通用网页搜索
- 主：Google
- 备 1：DuckDuckGo HTML
- 备 2：Brave
- 备 3：Startpage
- 备 4：Yahoo / Qwant / Ecosia

### 技术/文档搜索
- GitHub 搜不到 → `site:github.com` + Google / DuckDuckGo
- 文档站搜不到 → `site:docs.*` / `site:developer.*`
- 学术搜不到 → Google Scholar / arXiv / 普通 Google 交叉

## 工具级 fallback

### 当 `web_fetch` 被拦或返回异常
按这个顺序考虑：
1. 换一个更容易抓取的搜索页（如 DuckDuckGo HTML）
2. 改用 `site:` 查询，让结果页更干净
3. 改用 `exec` + `curl` 抓公开搜索结果页
4. 多源交叉，避免依赖单页

### 当 `web_search` 受 provider 限制
- 不要卡在 `country` / `language` 参数上
- 直接回到本 skill 的搜索引擎 URL 路线
- 把 `web_search` 当补源，不当主路径

## 典型回退模板

### 航班 / 酒店 / 本地信息
1. 百度
2. 必应中文
3. OTA/聚合页
4. `exec + curl` 抓公开搜索结果页

### GitHub / 技术资料
1. Google `site:github.com`
2. DuckDuckGo HTML / `!gh`
3. Brave
4. 官方 docs 站内定向

### 新闻 / 热点
1. 主引擎 + 时间过滤
2. 第二引擎新闻源
3. 官方来源 / 媒体原站

## 结果判弱标准
遇到这些情况，直接切 fallback：
- 连续只返回聚合垃圾页
- 搜到的都是过旧结果
- 标题和问题不匹配
- 页面抓不到正文
- 一个来源无法确认关键事实

## 报告要求
回退发生时，要在回复里明确写：
- 主路径为什么失败
- 换到了哪个 fallback
- 最终结果可靠性如何
