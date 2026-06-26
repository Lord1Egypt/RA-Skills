---
name: browser-ops
description: >-
  AI Agent 的网页访问路由决策指南。全 CLI 架构，零 MCP 依赖，不占常驻上下文 token。
  按成本逐级升级: WebFetch($0) → opencli web read($0,带Cookie) → Firecrawl → agent-browser → browser-use。
  IMPORTANT: For sites with opencli adapters (74 sites), use `opencli <platform>` directly — NEVER WebFetch/web read. For other sites, start with WebFetch. NEVER jump to browser-use/agent-browser first.
  覆盖四层场景: 搜索(Tavily/Brave/Exa/WebSearch/opencli 75站点) → 提取(WebFetch/opencli/Firecrawl) → 交互(opencli operate/agent-browser/browser-use) → 反爬(Zendriver)。
  触发场景: 搜索 抓取 爬取 网页 打不开 403 拦截 截图 表单 填表 Cookie 登录态 内部网站 SSO 反爬 Cloudflare。
  参见 deep-research (用于多源深度研究报告)、security-review (用于认证安全审计)。
  不适用于: 跨主机远程浏览器控制、高并发爬取(>10页/分钟)、非 DOM 界面(Canvas/桌面软件)。
triggers:
  - 搜索|抓取|爬取|网页|打不开|403|拦截|截图|表单|填表|网站
  - Cookie|登录态|内部网站|SSO|反爬|Cloudflare|内网
  - 股价|热榜|Twitter|微博|知乎|小红书|HackerNews|B站
  - scrape|crawl|fetch|browse|screenshot|cookie|anti-bot|web page
  - 打开.*链接|打开.*URL|打开.*网址|读.*链接|读.*网页|看.*网站|查.*网站
  - 帮我看|帮我读|帮我搜|帮我查|帮我打开|帮我访问|帮我下载
  - open.*url|read.*url|visit.*site|access.*page|download.*page
license: MIT
---

# Browser Operations — 网页访问路由决策指南

> 全 CLI 架构。所有工具通过 Bash 调用，零 MCP 依赖，不占常驻上下文。
> 核心原则：能用 HTTP 就不开浏览器，能用 opencli 就不用 browser-use。

## 核心规则

MUST 从免费层开始。NEVER 直接跳到浏览器工具。

每次网页任务按这个顺序判断，**命中就停**：
0. **目标是 opencli 已适配平台？→ 直接 `opencli <platform> <command>`，跳过 WebFetch**
   判断方法：URL 域名或用户意图命中已适配站点（`opencli list` 查看完整列表，74 个站点 454 条命令）。
   常见已适配平台：twitter/x.com, zhihu, weibo, bilibili, hackernews, xiaohongshu, douyin, reddit, youtube, github, arxiv, bloomberg, linkedin, douban, jd, wikipedia, v2ex, tieba, spotify, steam, medium, substack, producthunt, stackoverflow, 36kr, weread, xueqiu 等。
   这些平台有专属适配器，返回结构化数据，比 web read 更准确更高效。
1. WebFetch/WebSearch 能搞定（非已适配平台）？→ 用它，$0
2. 403/SSO/空？→ `opencli web read`，$0，Cookie 零配置
3. 需要 JS 渲染/结构化？→ `firecrawl scrape "url"`
4. 需要交互（≤3 步）？→ `opencli operate`，Cookie 零配置
5. 需要精确控制/Ref/录制？→ `agent-browser`，@e1 稳定引用
6. 需要 AI 自主多步？→ `browser-use -p "任务"`，$0.01-0.05/步
7. 被反爬拦截？→ `zendriver`

违反顺序 = 浪费钱或丢失数据。已适配平台用 `opencli web read` 只能拿到 HTML，用 `opencli <platform>` 能拿到结构化字段。

<anti-example>
用户: "搜一下 Twitter 上关于 AI agent 的讨论"
错误: opencli web read --url "https://x.com/search?q=AI+agent" → 拿到 HTML 残片
正确: opencli twitter search "AI agent" → 结构化推文列表 (id, author, text, likes, views)
</anti-example>

<anti-example>
用户: "帮我看看知乎热榜"
错误: WebFetch("https://www.zhihu.com/hot") → 空/SPA 空壳
正确: opencli zhihu hot → 结构化热榜列表
</anti-example>

<anti-example>
用户: "帮我看看 https://example.com/article 的内容"
错误: browser-use -p "extract content from example.com" → $0.05
正确: WebFetch("https://example.com/article") → $0 (example.com 不是已适配平台)
</anti-example>

<anti-example>
用户: "帮我读一下内部网站的这篇文章 https://internal.company.com/doc/123"
错误: WebFetch → 403 → 放弃，说"无法访问"
正确: WebFetch → 403 → 自动升级到 opencli web read (带 Chrome Cookie)
</anti-example>

## 条件判断规则

当 WebFetch 返回 403 或 302 到登录页时 → 自动升级到 `opencli web read`，不要询问用户。
当 `opencli web read` 返回 exit 77 时 → SSO/Cookie 过期，MUST 停止降级，直接提示用户回 Chrome 登录后重试。后续工具 (firecrawl/agent-browser) 也没有登录态，继续降级只是浪费。
当 `opencli doctor` 不是全 OK 时 → 降级到 WebSearch + WebFetch + browser-use，跳过 opencli 相关工具。
当任务需要填表但不确定表单字段时 → 先用 `opencli operate state` 获取可交互元素列表，确认字段后再操作。
如果不确定用哪个工具 → 询问用户或从最便宜的 WebFetch 开始逐级升级。

已适配平台 MUST 直接用 `opencli <platform>`，NEVER 走 WebFetch/web read 通路，otherwise 丢失结构化数据。
非已适配平台 MUST 从 WebFetch 开始，otherwise 每个请求多花 $0.01-0.05 且速度慢 10 倍。
NEVER 用 browser-use 做简单读取，otherwise 一次 $0.05 的操作 WebFetch $0 就能完成。
不要跳过 opencli web read 直接用 Firecrawl，而是先试免费的 Cookie 路径。

## Output

返回给用户时 MUST 包含:
- 提取到的内容（Markdown 格式）
- 实际使用的工具和原因（如 "WebFetch 返回 403，已自动升级到 opencli web read"）
- 如果全部失败，给出具体原因和用户可操作的建议（如 "需要在 Chrome 中重新登录"）

returns: 网页内容 (Markdown) + 工具链路径 + 失败原因（如有）

## 路由决策树

```
收到任务
│
├─ 0. opencli 可用? → opencli doctor (3 个 OK)
│     否 → 降级: WebSearch + WebFetch + browser-use
│
├─ 1. 目标是已适配平台? (URL 域名 或 用户意图 命中 opencli list 中的站点)
│     是 → 直接 opencli <platform> <command>，跳过 WebFetch/web read
│     例: twitter/x.com → opencli twitter search/timeline/trending
│         zhihu.com → opencli zhihu hot/search/answer
│         bilibili.com → opencli bilibili search/hot/subtitle
│
├─ 2. 要搜索（没 URL，非已适配平台）?
│     ├─ WebSearch (内置, 始终可用)
│     ├─ 深度搜索 → tavily search "query" --search-depth advanced
│     ├─ 独立索引 → curl brave API
│     └─ fallback → opencli google search
│
├─ 3. 有 URL，非已适配平台?
│     ├─ WebFetch ($0) → 403/SSO? → opencli web read ($0, Cookie 直连)
│     │     ├─ exit 77 (SSO 过期) → 停止降级，提示用户回 Chrome 登录
│     │     └─ 其他失败 (JS 不足/内容太短) → 继续降级到 firecrawl
│     └─ JS 渲染/PDF/结构化 → firecrawl scrape "url"
│
├─ 4. 要交互?
│     ├─ ≤3 步 → opencli operate (Cookie 零配置, 17 个命令)
│     │   open → state → click/type/select/scroll → screenshot → close
│     ├─ 需要稳定引用/录制/标注截图 → agent-browser (60+ 命令)
│     │   open → snapshot -i → click @e1 → screenshot --annotate
│     ├─ AI 自主多步 → browser-use -p "自然语言任务"
│     └─ 未知 DOM → Stagehand act("点击登录")
│
├─ 5. 被反爬? → python -c "import zendriver as zd; ..."
│
└─ 全失败 → 告知用户具体原因和建议，NEVER 静默失败
```

## 升级信号

| 当前工具返回 | 升级到 | 命令 |
|------------|--------|------|
| WebFetch → 403/302 登录页 | opencli web read | `opencli web read --url "url"` |
| WebFetch → 空/SPA 空壳 | Firecrawl | `firecrawl scrape "url"` |
| opencli → exit 77 | 停止降级，提示用户 | SSO 过期，后续工具也没登录态，直接提示用户回 Chrome 登录 |
| 需要点击/填表 | opencli operate | `opencli operate open "url" && state` |
| 编号 [N] 不稳定 | agent-browser | `agent-browser snapshot -i` → `click @e1` |
| 多步复杂任务 | browser-use | `browser-use -p "任务描述"` |
| Cloudflare 拦截页 | Zendriver | `python3 -c "import zendriver..."` |

## 搜索工具

```bash
# 内置 (始终可用)
WebSearch → Claude Code 内置，直接调用

# Tavily — AI 原生搜索，返回 answer + results (免费 1000 次/月)
tavily search "query"                              # pip install tavily-python
tavily search "query" --search-depth advanced       # 深度模式
tavily extract "https://url"                        # URL 内容提取

# Brave — 独立索引，不依赖 Google/Bing
curl -s "https://api.search.brave.com/res/v1/web/search?q=query" \
  -H "X-Subscription-Token: $BRAVE_API_KEY"

# Firecrawl — JS 渲染 + Markdown 提取 (免费 500 次)
firecrawl scrape "https://url"                     # pip install firecrawl
firecrawl crawl "https://url" --limit 10           # 批量
firecrawl map "https://url"                        # URL 发现

# 平台搜索 — 75 站点结构化数据
opencli twitter trending / zhihu hot / hackernews top / xiaohongshu search "旅行"
opencli list                                       # 查看所有适配器
```

## 浏览器交互工具

```bash
# opencli operate — 简单交互，Cookie 零配置 (通过 Chrome Extension 直连)
opencli operate open "url"
opencli operate state                              # 可交互元素 [1][2][3]
opencli operate click 5 / type 3 "hello" / select 2 "选项A"
opencli operate scroll down / keys Enter / wait text "Success"
opencli operate screenshot /tmp/shot.png / network / close

# agent-browser — 复杂交互，@e1 Ref 引用 (基于 Accessibility Tree，页面重渲染不变)
agent-browser open "url" && agent-browser snapshot -i
agent-browser click @e2 / fill @e3 "hello"         # Ref 引用
agent-browser screenshot --annotate /tmp/a.png     # 标注截图
agent-browser record start                        # 录制操作
agent-browser batch "click @e1 && wait 1000 && screenshot"
agent-browser --auto-connect snapshot              # 连接已运行 Chrome
# 搭配 Lightpanda 省 token: snapshot ~500 token vs Chrome ~3000 token
# ./lightpanda serve --port 9222 && agent-browser connect 9222

# browser-use — AI 自主操作 (LLM 决策循环，每步 $0.01-0.05)
browser-use -p "去 example.com 注册账号"            # 自然语言驱动
browser-use --connect -p "任务"                     # 连接已运行 Chrome
browser-use run --remote "任务"                     # 云端执行
```

## opencli operate vs agent-browser

| 维度 | opencli operate | agent-browser |
|------|----------------|---------------|
| 场景 | ≤3 步简单操作 | 复杂/精确操作 |
| 元素定位 | [N] 编号（页面变了会变） | @e1 Ref（稳定，基于 ARIA role+name） |
| Cookie | Chrome Extension 直连，零配置 | --profile / --auto-connect |
| 标注截图 | ❌ | ✅ --annotate（给视觉模型用） |
| 录制回放 | ❌ | ✅ record（固定流程自动化） |
| 批量/DOM diff | ❌ | ✅ batch / diff |
| 内核替换 | ❌ | ✅ Lightpanda（省 80% token） |
| 命令数 | 17 | 60+ |
| iOS 测试 | ❌ | ✅ -p ios |

## 前置条件

```bash
# 必装
npm i -g @jackwener/opencli
# Chrome 装 OpenCLI Browser Bridge: $(npm root -g)/@jackwener/opencli/extension
opencli doctor  # 3 个 OK 才能用

# 按需 (全 CLI，不需要配 MCP)
npm i -g agent-browser               # Ref 引用/录制/标注截图

> See references/ for extended content.
