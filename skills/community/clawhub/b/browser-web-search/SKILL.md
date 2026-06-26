---
name: browser-web-search
description: 一行命令搜遍全网 — 55 个平台 91+ 个命令，头条、知乎、豆瓣、YouTube、GitHub、Reddit、Hacker News 等。专为 OpenClaw 设计，复用浏览器登录态，返回结构化 JSON，天然适配 AI Agent 工具调用。
version: 0.4.10
versionNotes: |
  0.4.10 — Residual-risk hardening layered on the v0.4.4 sealed-tier model.
  Adds three programmatic responses to the ClawScan May 2026 verdict's
  remaining concern ("core functionality inherently relies on a third-party
  dependency to handle sensitive session data"):

    1. Gate 4 — Platform consent ledger at ~/.bws/consents.json.
       Per (site, pkgVersion, entrySha512) one-time consent via the new
       --accept-platform-consent flag. Any drift in pkgVersion or
       entrySha512 invalidates prior consent for that site.
    2. Transparency block printed to stderr for every sensitive call
       (and for all calls when BWS_TRANSPARENCY=1). Machine-readable JSON
       line naming the third-party package, audited SHA-512, gate path,
       audit log, and consent ledger. Prevents silent invocation by a
       wrapping AI agent.
    3. New launcher-only --dry-run flag that runs all four gates plus
       integrity verification, writes the audit record, and exits
       without importing the package. Useful for CI and agent dispatch.

  Underlying npm package browser-web-search remains pinned at 0.4.3 (no
  change to the SHA-512 integrity gate, ENTRY_EXPECTED_SIZE, or symlink
  rejection). All v0.4.4 gates remain unchanged.
author: Ping Si <sipingme@gmail.com>
type: cli
requires:
  runtime:
    - name: node
      version: ">=18.0.0"
      description: Node.js 运行时
    - name: npm
      description: Node.js 包管理器（随 Node.js 安装）
  packages:
    - npm: browser-web-search
      global: false
  binaries:
    - name: openclaw
      description: OpenClaw CLI，用于浏览器自动化
install:
  command: npm install -g browser-web-search@0.4.3
  riskLevel: medium
  riskReason: 通过 npm 全局安装第三方包，该包会在浏览器页面上下文中执行 JavaScript。安装前请审计源码。
  requiresApproval: true
  source:
    registry: npmjs.com
    package: browser-web-search
    repository: https://github.com/sipingme/browser-web-search
    npm: https://www.npmjs.com/package/browser-web-search
  verification:
    - 安装前请审查 GitHub 仓库代码
    - 检查 npm 包的下载量和维护状态
    - 对比 npm 发布版本与 GitHub 源码是否一致
  note: 用户需先通过 npm install -g 全局安装 browser-web-search，运行时调用本地已安装的 bws 命令
capabilities:
  sensitive:
    - type: browser-session-access
      riskLevel: high
      description: 通过 OpenClaw 在已认证的浏览器标签页中执行 JavaScript
      scope: 按 adapter 域名隔离（如 zhihu.com, xiaohongshu.com）
      access:
        - 当前页面 DOM
        - 当前页面 Session（继承，非提取）
        - 站点认证数据（登录态下的 API 响应）
        - 账户保护页面内容（如私信、收藏、个人资料）
      noAccess:
        - 浏览器 Cookie 文件（不直接读取）
        - 其他域名数据
        - 用户配置目录
      risks:
        - 第三方 npm 包（browser-web-search）在页面上下文中执行，可访问站点认证数据
        - 恶意代码可能窃取 cookies 或页面内容
        - 包代码不包含在此 Skill 中，需独立审计
      mitigations:
        - adapter 脚本开源可审计
        - 按域名隔离，无法跨站访问
        - 不持久化存储任何凭证
  privacyNotice:
    summary: 此 Skill 自动复用浏览器登录态，可读取您已登录站点的任何可见数据
    details:
      - 零配置意味着 CLI 自动获得您在 OpenClaw 浏览器中的登录会话访问权
      - 可读取账户保护的页面（私信、收藏、个人资料、订单等）
      - 访问范围取决于您在目标站点的登录权限
      - 建议仅在信任 browser-web-search 包代码后使用
metadata:
  openclaw:
    primaryEnv:
      - name: BWS_PUBLIC_ONLY
        values: ["0", "1"]
        default: "0"
        purpose: Hard-isolation mode that denies all sensitive adapters (Gate 1; overrides everything below)
      - name: BWS_ENABLE_SENSITIVE_TIER
        values: ["0", "1"]
        default: "0"
        purpose: |
          v0.4.4+: sensitive tier is sealed by default. Operator must enrol the runtime
          via this env before any per-call/session opt-in is considered (Gate 2).
          Responds to ClawScan May 2026 "Identity and Privilege Abuse" recommendation.
      - name: BWS_ALLOW_SENSITIVE
        values: ["0", "1"]
        default: "0"
        purpose: Session-level opt-in within the enabled sensitive tier (Gate 3)
      - name: BWS_ALLOW_LOCAL_INSTALL
        values: ["0", "1"]
        default: "0"
        purpose: Allow loading bws from launcher-local or CWD node_modules (off by default to prevent path-pivoting)
      - name: BWS_SKIP_PLATFORM_CONSENT
        values: ["0", "1"]
        default: "0"
        purpose: |
          v0.4.10+: bypass Gate 4 (platform consent ledger). Loud stderr warning.
          Intended only for trusted CI; loses the binding to a specific audited build.
      - name: BWS_TRANSPARENCY
        values: ["0", "1"]
        default: "0"
        purpose: |
          v0.4.10+: also emit the [bws] transparency:{...} stderr line for
          public adapters. Sensitive calls always emit it regardless of this var.
    launcherOnlyFlags:
      - name: --i-understand-sensitive
        purpose: Gate 3 per-call opt-in for sensitive adapters
      - name: --accept-platform-consent
        purpose: |
          v0.4.10+: Gate 4 per-(site, pkgVersion, entrySha512) consent.
          First sensitive call to a site requires this flag; subsequent calls
          with identical pkgVersion + entrySha512 reuse the stored consent.
      - name: --dry-run
        purpose: |
          v0.4.10+: run Gates 1-4 + integrity + symlink rejection, write the
          audit record, then exit WITHOUT importing the third-party package.
          Exit 0 = would allow; non-zero = denied (audit log shows reason).
    sensitiveTierGateOrder:
      - "Gate 1: BWS_PUBLIC_ONLY=1 hard-isolates (overrides everything)"
      - "Gate 2: sensitive tier sealed unless BWS_ENABLE_SENSITIVE_TIER=1"
      - "Gate 3: per-call/session opt-in via BWS_ALLOW_SENSITIVE=1 or --i-understand-sensitive"
      - "Gate 4 (v0.4.10): platform consent ledger at ~/.bws/consents.json, bound to (site, pkgVersion, entrySha512); --accept-platform-consent to record"
    primaryCredentialUsage: none
    networkUsage: indirect-via-bws
    auditLog:
      path: ~/.bws/audit.log
      content: metadata-only (no payloads, no responses, args hashed via SHA-256)
      fields: [ts, pid, adapter, site, primaryDomain, classification, decision, reason, argHash]
      rotation: 1 MiB → audit.log.1
    subprocessUsage: none
    moduleLoad:
      - file: scripts/run.js
        function: safeRunBws
        method: dynamic-esm-import
        loader: "await import(file://...)"
        target: pinned npm package "browser-web-search"
        targetResolution: platform-standard global node_modules roots only (no PATH lookup, no shell, no require.resolve fallback)
        targetResolutionOptIn: BWS_ALLOW_LOCAL_INSTALL=1 (adds launcher-local + CWD node_modules; off by default)
        symlinkPolicy: rejected per path component from the candidate root down to dist/index.js
        preImportIntegrityGate:
          enforcedBy: scripts/run.js:verifyBwsIntegrity
          checks:
            - package.json name == 'browser-web-search'
            - package.json version == '0.4.3'
            - stat(dist/index.js).size == 22871
            - sha512(dist/index.js) == sha512-qoGLsUMOPgzIpdxtGMv08Gjy84bkh0AF90mKG9qvagq9O2ngcKcLg+GAy3Z8bljkvdfKcrQSp55xPO9mVCuv3Q== (timing-safe compare)
          envOverride: false
          failureMode: deny + audit-log entry (adapter="(integrity)")
        argSource: allow-listed-cli-args
        argValidation:
          - length-bounded (<= 1024 bytes per arg)
          - control-char rejection (NUL + ASCII control)
          - long-flag allow-list (--json/--jq/--count/--sort/--id/--limit/--page)
          - adapter-name regex ([a-zA-Z0-9_-]{1,64}/[a-zA-Z0-9_-]{1,64})
          - "--" delimiter between subcommand and positional args
        purpose: Invoke the pinned 'browser-web-search' npm package in-process, with a validated argv injected via process.argv mutation, after a hard supply-chain integrity gate
configPaths:
  - path: ~/.bws/
    required: false
tags:
  - browser
  - web-search
  - scraping
  - automation
  - ai-agent
repository: https://github.com/sipingme/browser-web-search-skill
package: https://github.com/sipingme/browser-web-search
npm: https://www.npmjs.com/package/browser-web-search
---

# Browser Web Search (BWS) Skill

> **一行命令，搜遍全网** — 为 AI Agent 而生的多平台内容搜索工具

把 **55 个主流平台**的搜索接口封装成统一命令行 API，让 AI Agent 直接拿到结构化 JSON，无需 API Key，无需额外配置。

## 🏗️ 架构说明

```
OpenClaw/AI Agent
    ↓ (读取 Skill 配置)
browser-web-search-skill
    ↓ (调用 CLI)
bws 命令
    ↓ (OpenClaw Browser)
目标网站（55 个平台）
```

## 🎯 核心特点

- 🔍 **跨平台搜索** — 今日头条、知乎、豆瓣、YouTube、GitHub、Reddit、Hacker News… 一套语法搞定
- 🔑 **无需 API Key** — 复用浏览器登录态，开箱即用
- 🤖 **AI Agent 友好** — 结构化 JSON 输出，支持 `--jq` 过滤，天然适配 LLM 工具调用
- ⚡ **零配置** — 无需 Chrome Extension，无需后台 Daemon

## 📋 安装

```bash
npm install -g browser-web-search@0.4.3
```

### 验证安装

```bash
bws --version
bws site list
```

## 🚀 快速开始

```bash
# 搜索今日头条关于 "ai search" 的最新文章
bws site toutiao/search "ai search"

# 搜索知乎，返回 5 条
bws site zhihu/search "ai agent" --count 5

# Hacker News 最新讨论（按时间）
bws site hn/search "llm" --sort date

# GitHub 热门仓库（按 Star 数）
bws site github/search "ai search" --sort stars

# Reddit 最新帖子
bws site reddit/search "ai search" --sort new

# YouTube 视频搜索
bws site youtube/search "ai agent tutorial"

# 查看所有可用命令
bws site list
```

## 📊 内置平台（55 个）

> 🔓 无需登录 · 🔐 需登录该站账号 · 🔀 依具体命令而定

### 🇨🇳 国内平台（30 个）

| 平台 | 说明 | 登录 | 命令 |
|-----|------|:----:|-----|
| **今日头条** | 新闻资讯 | 🔀 | `toutiao/search`, `toutiao/hot`, `toutiao/feed` |
| **澎湃新闻** | 权威新闻 | 🔓 | `thepaper/search`, `thepaper/hot` |
| **腾讯新闻** | 热点新闻 | 🔓 | `qqnews/search`, `qqnews/hot` |
| **网易新闻** | 热点新闻 | 🔓 | `netease/search`, `netease/hot` |
| **新浪新闻** | 门户新闻 | 🔓 | `sina/search`, `sina/hot` |
| **36kr** | 科技创投 | 🔓 | `36kr/search`, `36kr/newsflash`, `36kr/article` |
| **虎嗅** | 科技商业媒体 | 🔓 | `huxiu/search` |
| **华尔街见闻** | 财经资讯 | 🔓 | `wallstreetcn/search` |
| **东方财富** | 股票行情 & 财经新闻 | 🔓 | `eastmoney/stock`, `eastmoney/news` |
| **掘金** | 技术社区 | 🔓 | `juejin/search` |
| **CSDN** | 开发者社区 | 🔓 | `csdn/search` |
| **博客园** | 技术博客 | 🔓 | `cnblogs/search` |
| **V2EX** | 技术社区 | 🔓 | `v2ex/search` |
| **Baidu** | 百度搜索 | 🔓 | `baidu/search` |
| **虎扑** | 体育社区 | 🔓 | `hupu/search` |
| **有道翻译** | 中英词典/翻译 | 🔓 | `youdao/translate` |
| **什么值得买** | 好价/优惠聚合 | 🔓 | `smzdm/search` |
| **InfoQ** | 技术媒体 | 🔓 | `infoq/search` |
| **微信公众号** | 公众号文章 | 🔐 | `weixin/search`, `weixin/article` |
| **小红书** | 生活分享 | 🔐 | `xiaohongshu/search`, `xiaohongshu/note`, `xiaohongshu/comments`, `xiaohongshu/user_posts`, `xiaohongshu/me`, `xiaohongshu/feed` |
| **知乎** | 问答社区 | 🔀 | `zhihu/search`, `zhihu/hot`, `zhihu/question`, `zhihu/me` |
| **微博** | 社交热搜 | 🔐 | `weibo/search`, `weibo/hot` |
| **Bilibili** | 视频弹幕 | 🔀 | `bilibili/search`, `bilibili/popular`, `bilibili/trending`, `bilibili/ranking`, `bilibili/video`, `bilibili/comments`, `bilibili/history`, `bilibili/me`, `bilibili/feed` |
| **雪球** | 股票社区 | 🔐 | `xueqiu/search` |
| **BOSS直聘** | 招聘平台 | 🔀 | `boss/search`, `boss/detail` |
| **即刻** | 兴趣社区 | 🔐 | `jike/search` |
| **豆瓣** | 影视/书籍评分社区 | 🔐 | `douban/search`, `douban/movie`, `douban/movie-hot`, `douban/top250`, `douban/comments` |
| **起点中文网** | 网络小说 | 🔐 | `qidian/search` |
| **携程** | 旅行/酒店/景点 | 🔐 | `ctrip/search` |

### 🌏 国际平台（25 个）

| 平台 | 说明 | 登录 | 命令 |
|-----|------|:----:|-----|
| **Google** | 谷歌搜索 | 🔓 | `google/search` |
| **Bing** | 必应搜索 | 🔓 | `bing/search` |
| **DuckDuckGo** | 隐私优先搜索 | 🔓 | `duckduckgo/search` |
| **GitHub** | 代码托管 | 🔓 | `github/search` |
| **Hacker News** | 科技社区 (YC) | 🔓 | `hn/search` |
| **Reddit** | 英文社区 | 🔓 | `reddit/search` |
| **BBC** | 国际新闻 | 🔓 | `bbc/news` |
| **Reuters** | 路透社新闻 | 🔓 | `reuters/search` |
| **The Verge** | 科技媒体 | 🔓 | `verge/search` |
| **Ars Technica** | 深度科技媒体 | 🔓 | `ars/search` |
| **Engadget** | 科技消费媒体 | 🔓 | `engadget/search` |
| **Stack Overflow** | 开发者问答 | 🔓 | `stackoverflow/search` |
| **Dev.to** | 开发者社区 | 🔓 | `devto/search` |
| **npm** | Node.js 包 | 🔓 | `npm/search` |
| **PyPI** | Python 包 | 🔓 | `pypi/search` |
| **arXiv** | 学术论文 | 🔓 | `arxiv/search` |
| **IMDb** | 全球最大影视数据库 | 🔓 | `imdb/search`, `imdb/movie`, `imdb/top250` |
| **Genius** | 歌词/歌曲数据库 | 🔓 | `genius/search` |
| **Wikipedia** | 百科全书 | 🔓 | `wikipedia/search`, `wikipedia/summary` |
| **Open Library** | 图书数据库 | 🔓 | `openlibrary/search` |
| **Yahoo Finance** | 美股/港股行情 | 🔓 | `yahoo-finance/quote` |
| **GSMArena** | 手机规格数据库 | 🔓 | `gsmarena/search` |
| **Product Hunt** | 科技产品发现 | 🔓 | `producthunt/today` |
| **X (Twitter)** | 社交媒体 | 🔐 | `x/search` |
| **LinkedIn** | 职业社交 | 🔐 | `linkedin/search` |
| **YouTube** | 视频 & 字幕 & 评论 | 🔀 | `youtube/search`, `youtube/video`, `youtube/transcript`, `youtube/transcript-by-id`, `youtube/comments`, `youtube/channel`, `youtube/feed` |

## 🔧 命令参考

```bash
bws site list                        # 列出所有 adapter
bws site info <name>                 # 查看 adapter 参数说明
bws site <name> [args...]            # 运行 adapter
bws site <name> --count 5           # 限制返回数量
bws site <name> --json               # 输出原始 JSON
bws site <name> --jq '.items[].url' # jq 过滤提取字段
```

## 📋 标准操作流程 (SOP)

### 操作 1：跨平台搜索

**场景**：用户想搜索多个平台关于某话题的最新内容

```bash
# 国内平台
bws site toutiao/search "ai agent" --count 5
bws site zhihu/search "ai agent" --count 5
bws site huxiu/search "ai agent" --count 5

# 国际平台
bws site hn/search "ai agent" --sort date --count 5
bws site reddit/search "ai agent" --sort new --count 5
bws site github/search "ai agent" --sort stars --count 5
```

---

### 操作 2：获取热点资讯

```bash
bws site zhihu/hot        # 知乎热榜
bws site weibo/hot        # 微博热搜
bws site toutiao/hot      # 今日头条热榜
bws site thepaper/hot     # 澎湃新闻热点
bws site bilibili/trending  # B 站热搜词
bws site bilibili/popular   # B 站全站热门
```

---

### 操作 3：使用 jq 过滤数据

```bash
# 只提取标题
bws site zhihu/search "大模型" --jq '[.items[].title]'

# 只提取 URL 列表
bws site hn/search "llm" --jq '[.items[].url]'

# 提取标题+日期
bws site toutiao/search "ai" --jq '[.items[] | {title, date}]'
```

---

### 操作 4：影视 / 娱乐内容

```bash
# 豆瓣搜索影视
bws site douban/search "三体"
bws site douban/movie-hot

# IMDb 搜索
bws site imdb/search "Inception"
bws site imdb/top250 --count 10

# YouTube 视频与字幕
bws site youtube/search "ai tutorial"
bws site youtube/transcript-by-id --id dQw4w9WgXcQ
```

---

### 操作 5：开发者资源搜索

```bash
# 搜索 npm 包
bws site npm/search "langchain"

# 搜索 PyPI 包
bws site pypi/search "openai"

# arXiv 论文
bws site arxiv/search "retrieval augmented generation" --count 5

# Stack Overflow
bws site stackoverflow/search "python async await"
```

---

### 操作 6：登录态管理

需要登录的站点（微信公众号、小红书、微博、X、豆瓣等）：

```bash
# 在 OpenClaw 浏览器中登录
openclaw browser open https://weixin.qq.com
openclaw browser open https://x.com
openclaw browser open https://www.xiaohongshu.com
openclaw browser open https://www.douban.com

# 登录完成后重试
bws site weixin/search "ai"
bws site douban/search "三体"
```

---

## 🔧 技术架构：如何访问登录态

```
bws 命令
    ↓ 调用
openclaw browser evaluate <script>
    ↓ 在已打开的标签页中执行 JavaScript
目标网站（使用该标签页的登录态）
```

| 访问内容 | 是否访问 | 说明 |
|---------|---------|------|
| 浏览器 Cookie 文件 | ❌ 否 | 不直接读取 `~/.config/chromium/Cookies` 等文件 |
| 用户配置目录 | ❌ 否 | 不访问 `~/.bws/` 以外的配置 |
| 其他网站数据 | ❌ 否 | 只能访问 adapter 指定的域名 |
| 当前页面 DOM | ✅ 是 | adapter 脚本在页面中执行 |
| 当前页面 Session | ✅ 是 | 继承页面的登录状态 |

## 🛡️ 运行安全与最小权限（必读）

> 本 Skill 的核心工作由第三方 npm 包 `browser-web-search` 完成；该包会在已认证的浏览器标签页上下文中执行 JavaScript，因此**理论上可以读取你已登录站点的任何可见数据（私信、收藏、个人资料、订单等）**。Launcher 只能控制传给 `bws` 的参数，无法约束包内代码行为。请务必按以下原则使用。

### 1) 安装前审计与版本固定

```bash
# 审计源码 (与 SKILL.md 中声明的版本严格一致)
npm view browser-web-search@0.4.3 dist.integrity dist.shasum
# 阅读源码: https://github.com/sipingme/browser-web-search/blob/v0.4.3/src/index.ts

# 安装时跳过 install/postinstall 脚本，降低供应链注入面
npm install -g browser-web-search@0.4.3 --ignore-scripts
```

不要使用 `latest` tag、不要使用 `^0.4.3` 之类的范围版本。每次升级前重新审计。

#### Launcher 强制完整性闸门（无需用户操作）

每次 `bws-skill` 调用时，launcher 在动态 `import()` 之前会校验：

| 检查 | 期望值 |
|------|--------|
| `package.json.name` | `browser-web-search` |
| `package.json.version` | `0.4.3` |
| `dist/index.js` 字节数 | `22871` |
| `dist/index.js` SHA-512 | `sha512-qoGLsUMOPgzIpdxtGMv08Gjy84bkh0AF90mKG9qvagq9O2ngcKcLg+GAy3Z8bljkvdfKcrQSp55xPO9mVCuv3Q==` |

任何一项不匹配会**直接拒绝**调用并写入 `~/.bws/audit.log`（`adapter` 字段为 `"(integrity)"`）。**该闸门不接受任何 env 旁路**——如果需要升级到新版本，必须显式更新 `scripts/run.js` 中的 `REQUIRED_VERSION` / `ENTRY_SHA512_BASE64` / `ENTRY_EXPECTED_SIZE` 三个常量，并同步 `config.json` 的 `install.verification.integrity` / `capabilities.supplyChain` 字段。

你可以独立复算 SHA-512 来确认本地安装：

```bash
P=$(npm root -g)/browser-web-search/dist/index.js
shasum -a 512 "$P" | awk '{print $1}' | xxd -r -p | base64 | sed 's|^|sha512-|'
# 应输出与上表完全一致的字符串
```

### 2) 浏览器配置隔离

**强烈建议**为 OpenClaw 创建一个独立的 Chrome/Chromium profile，仅在该 profile 中登录会被本 Skill 访问的站点。**不要**让 OpenClaw 复用你日常的浏览器 profile，避免银行、邮箱、企业 SSO 等无关账号被 adapter 触达。

### 3) 四层闸门：默认封印 + 显式 tier + 显式 opt-in + 平台同意账本（敏感 adapter）

> **v0.4.4 重要变更**：sensitive tier 现在**默认封印**，即使你设了 `BWS_ALLOW_SENSITIVE=1` 或加了 `--i-understand-sensitive`，**也不会**让你访问敏感 adapter。这是对 ClawScan 2026-05 "Identity and Privilege Abuse" 与 "Tool Misuse and Exploitation" 两条 High Concern 的程序化响应。

Launcher 把 adapter 划分为 `public` / `sensitive` 两类。`sensitive` 即默认拒绝；触发条件之一即视为敏感：

- 站点位于 `ALWAYS_SENSITIVE_SITES`：`weixin / xiaohongshu / weibo / xueqiu / jike / douban / qidian / ctrip / x / linkedin`
- 命令后缀匹配 `/(me|feed|history|comments|user_posts|article)$`，例如 `zhihu/me`、`bilibili/feed`、`youtube/history`
- 未在白名单中的未知站点（防御未来 `bws` 新增 adapter）

授权按以下顺序逐层判定（任一闸门拒绝即拒绝）：

| Gate | 触发条件 | 行为 |
|------|---------|------|
| **1. PUBLIC_ONLY 硬隔离** | `BWS_PUBLIC_ONLY=1` | 一律拒绝 sensitive，**覆盖下面三层** |
| **2. Tier 封印（v0.4.4 新增）** | `BWS_ENABLE_SENSITIVE_TIER ≠ 1` | 一律拒绝 sensitive；reason=`sensitive-tier-sealed` |
| **3. 调用级 opt-in** | tier 启用后，仍需 env 或 flag | 缺一律拒绝；reason=`tier-enabled-but-no-opt-in` |
| **4. 平台同意账本（v0.4.10 新增）** | `(site, pkgVersion, entrySha512)` 三元组无记录 | 拒绝；reason=`no-platform-consent:*`；首次需 `--accept-platform-consent` |

也就是说，**最小可用敏感访问的命令组合（v0.4.10）**变成：

```bash
# 1) 必须 (一次性，建议放在专用 shell 而非 ~/.zshrc)：开启 tier
export BWS_ENABLE_SENSITIVE_TIER=1

# 2) 调用级 opt-in：任选其一
export BWS_ALLOW_SENSITIVE=1         # 会话级
# 或加 --i-understand-sensitive       # 单次调用

# 3) v0.4.10 新增：首次访问该 site 时记录平台同意
#    后续相同 (pkgVersion, entrySha512) 不再要求；package 升级会自动失效
bws-skill run weixin/search "ai" --i-understand-sensitive --accept-platform-consent
```

> 💡 **--dry-run（v0.4.10）**：先用 `--dry-run` 验证闸门通过、看清 `[bws] transparency:{...}` 行，再去掉 `--dry-run` 实际调用。CI 和 AI Agent 派发可以利用 dry-run 在不真正动用浏览器 session 的前提下确认权限。
>
> ```bash
> bws-skill run weixin/search "ai" \
>   --i-understand-sensitive --accept-platform-consent --dry-run
> # 退出码 0 = 闸门会放行；查看 stderr 的 transparency 行
> ```

**强烈建议的姿态**：

| 场景 | env |
|------|-----|
| 仅用 hn / github / arxiv 等公共 adapter | （什么都不设；这是默认） |
| 不可信环境 / 沙箱 agent / production | `BWS_PUBLIC_ONLY=1` |
| 偶尔需要敏感访问的开发机 | 临时 `BWS_ENABLE_SENSITIVE_TIER=1 BWS_ALLOW_SENSITIVE=1 bws ...`，**不要**写进 shell rc |

未通过任一闸门时，会返回结构化拒绝并在 stderr 给出准确的迁移提示。

#### 从 < v0.4.4 迁移

如果你的 agent 配置之前只有 `BWS_ALLOW_SENSITIVE=1`，调用敏感 adapter 现在会拿到：

```json
{"success":false,"error":"Adapter '...' is classified as sensitive ... Since v0.4.4 the sensitive tier is SEALED BY DEFAULT ..."}
```

补一行 `export BWS_ENABLE_SENSITIVE_TIER=1` 即可恢复。审计日志里 reason 会从 `no opt-in` 变成 `sensitive-tier-sealed`，方便你定位被这次改动影响的调用方。

### 4) 审计日志

Launcher 会在 `~/.bws/audit.log` 追加 JSON Lines 记录，**仅包含元数据**，**不记录任何参数原文、cookie 或响应数据**。日志超过 1 MiB 自动轮转为 `audit.log.1`。

每条记录包含的字段：

| 字段 | 含义 |
|------|------|
| `ts` | UTC 时间戳 (RFC3339) |
| `pid` | launcher 进程 PID |
| `adapter` | 完整 adapter 名 (如 `xiaohongshu/search`)，完整性闸门记录为 `(integrity)` |
| `site` | 从 adapter 拆出来的站点段 |
| `primaryDomain` | 已知站点的主域名（用于事后取证；未知站点为 `null`） |
| `classification` | `public` / `sensitive` |
| `decision` | `allow` / `deny` |
| `reason` | `public` / `tier+opt-in:env` / `tier+opt-in:flag` / `BWS_PUBLIC_ONLY=1` / `sensitive-tier-sealed` / `tier-enabled-but-no-opt-in` / `entry-sha512-mismatch` / `entry-sha512-match` |
| `argHash` | 参数 SHA-256 前 16 位（仅做去重比对，无法反推原文） |

定期 review：

```bash
tail -n 50 ~/.bws/audit.log | jq -c

# 仅看 sensitive 决策
jq -c 'select(.classification=="sensitive")' ~/.bws/audit.log

# 过去 30 天碰过哪些主域名
jq -r 'select(.decision=="allow" and .primaryDomain != null) | .primaryDomain' ~/.bws/audit.log | sort -u

# 因封印或缺 opt-in 被拒的调用计数（看哪些调用方需要迁移）
jq -c 'select(.reason=="sensitive-tier-sealed" or .reason=="tier-enabled-but-no-opt-in") | .adapter' ~/.bws/audit.log | sort | uniq -c
```

### 5) 数据最小化

- 优先使用公开 adapter（`hn/search`、`github/search`、`arxiv/search` 等）—— 这些不需要登录态，即使 `bws` 被恶意替换也无敏感数据可窃。
- 用 `--jq` / `--count` 在源头减少返回字段。**不要**把整段 JSON 喂给下游 LLM 或外发到第三方服务。
- 涉及账户保护页面时，使用一次性查询 + 立即关闭 OpenClaw 标签。

### 6) 残留风险（无法在本 Skill 层面消解）

- 一旦 `bws` 被调用（无论是否 sensitive 类别），它都拥有当前 OpenClaw session 的完整执行权限。Launcher 无法阻止包内代码越界访问其他已打开的标签。**唯一的硬隔离手段**是上文 (2) 的浏览器 profile 隔离 + (3) 的 `BWS_PUBLIC_ONLY=1`。
- 若 npm 注册表上的 `browser-web-search@0.4.3` 在你审计后被重新发布（不可变性被破坏），本地已安装版本不受影响，但下次 `npm install -g` 会拉到新版本。建议把审计过的 tarball 缓存到内部 registry 或私有 mirror。

## 🔒 安全模型摘要（机器可读字段已在 `config.json` 中声明）

| 维度 | 状态 |
|-----|------|
| 子进程命令注入 | ✅ launcher 不 spawn 任何子进程；in-process ESM import |
| Option injection 到 bws | ✅ flag allow-list + `--` 分隔 |
| 敏感 adapter 默认封印 | ✅ v0.4.4+ tier 默认关闭，需 `BWS_ENABLE_SENSITIVE_TIER=1` 才解锁后续 opt-in |
| 平台同意账本（首次敏感访问需明示） | ✅ v0.4.10+ Gate 4：`~/.bws/consents.json` 绑定 `(site, pkgVersion, entrySha512)`；升级或篡改自动失效 |
| 透明性（无法被包装层悄悄调用） | ✅ v0.4.10+ 每次 sensitive 调用 stderr 打印 `[bws] transparency:{...}` JSON 行 |
| Dry-run（CI / Agent 不真正调用包）| ✅ v0.4.10+ `--dry-run` 跑完所有闸门 + 完整性校验后退出，不 import |
| 公共 adapter 直通 | ✅ 无需任何 env（如 `hn/search`） |
| 硬隔离模式 | ✅ `BWS_PUBLIC_ONLY=1` 覆盖一切 opt-in 与同意账本 |
| 审计日志（含 site / primaryDomain / dryRun） | ✅ `~/.bws/audit.log`（仅元数据） |
| 第三方包供应链（被替换 / 篡改） | ✅ launcher 在 import 前强制校验 SHA-512，无 env 旁路；同意账本与该哈希联动失效 |
| Path-pivoting（CWD 下放置恶意包） | ✅ 默认仅信任全局 node_modules；本地需 `BWS_ALLOW_LOCAL_INSTALL=1` |
| 符号链接劫持入口 | ✅ 自候选根至 `dist/index.js` 任一组件为 symlink 即跳过 |
| 包升级"静默通过"残留风险 | ✅ v0.4.10 平台同意账本与 `entrySha512` / `pkgVersion` 绑定；任一变化即失效，强制重新明示 |
| 浏览器 session 越权（包内 JS 在审计版本内的预期行为） | ⚠️ 无法在 launcher 层消解；依赖 (2) profile 隔离 + tier 默认封印 + transparency 行 |
| 跨标签数据访问（包内 JS 触达其他打开的标签） | ⚠️ launcher 无权约束；依赖独立 profile + 关闭无关标签 + tier 默认封印 |
| 跨站访问 | ⚠️ adapter 域名隔离仅约束开源 adapter 的设计意图，不是运行时强制 |
| 上传到第三方服务器 | ⚠️ 当前审计版本未观察到，但每次升级需重新审计并同步 launcher 内的固定哈希；升级会自动废除所有平台同意账本记录 |

## 🎓 示例对话

**用户**：搜索头条最新 3 篇关于 AI Agent 的文章

```bash
bws site toutiao/search "AI Agent" --count 3
```

---

**用户**：看看 Hacker News 上关于 LLM 的最新讨论

```bash
bws site hn/search "llm" --sort date --count 5
```

---

**用户**：GitHub 上 ai search 相关的热门项目

```bash
bws site github/search "ai search" --sort stars --count 5
```

---

**用户**：豆瓣电影 Top 10

```bash
bws site douban/top250 --count 10
```

---

**用户**：YouTube 搜索 AI 教程

```bash
bws site youtube/search "ai agent tutorial" --count 10
```

---

## 📚 参考资料

- [项目 GitHub](https://github.com/sipingme/browser-web-search-skill)
- [browser-web-search 核心库](https://github.com/sipingme/browser-web-search)
- [npm 包](https://www.npmjs.com/package/browser-web-search)

---

## 📝 维护说明

- **Skill 版本**: 0.4.10 (Launcher + 文档 + 闸门策略)
- **底层 npm 包**: `browser-web-search@0.4.3` (整数固定 + SHA-512 + ENTRY_EXPECTED_SIZE)
- **最后更新**: 2026-05-11
- **维护者**: Ping Si <sipingme@gmail.com>
- **许可证**: MIT
- **安全审计依据**: 见仓库 `SECURITY.md`（ClawScan May 2026 Verdict ↔ launcher/config 字段映射）

### 版本变更历史

- **0.4.10** (2026-05-11): 残留风险硬化（Gate 4 平台同意账本 + transparency 行 + `--dry-run`）；对 ClawScan May 2026 "suspicious classification due to inherent third-party session capability" 的直接程序化响应。**npm 固定包未变（仍 0.4.3）。**
- **0.4.4** (2026-05-07): Sensitive tier 默认封印；SHA-512 完整性闸门（无 env 旁路）；symlink 拒绝；CWD/launcher-local 默认禁用；对 ClawScan May 2026 "Identity and Privilege Abuse" + "Tool Misuse and Exploitation" 的程序化响应。
- **0.4.3** (2026-04-29): 扩展至 55 平台 91+ 命令。

---

## ✅ 首次成功检查清单

- [ ] 安装工具（必须精确版本 + 跳过脚本）：`npm install -g browser-web-search@0.4.3 --ignore-scripts`
- [ ] 验证 SHA-512 一致：`P=$(npm root -g)/browser-web-search/dist/index.js && shasum -a 512 "$P"`
- [ ] 查看命令：`bws-skill list`（或直接 `bws site list`）
- [ ] 测试**公共** adapter（无需任何 env）：`bws-skill run hn/search "llm" --count 3`
- [ ] 看到 JSON 输出，并阅读 stderr 是否出现 `[bws] transparency:{...}`（公共 adapter 默认不出，除非 `BWS_TRANSPARENCY=1`）
- [ ] **可选**：使用 `--dry-run` 测试敏感 adapter 闸门组合，不真正调用包
  ```bash
  BWS_ENABLE_SENSITIVE_TIER=1 BWS_ALLOW_SENSITIVE=1 \
    bws-skill run zhihu/me --dry-run --accept-platform-consent
  ```
