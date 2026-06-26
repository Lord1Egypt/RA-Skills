# Browser Web Search Skill

> **一行命令，搜遍全网** — 55 个平台 91+ 个命令，专为 OpenClaw 与 AI Agent 设计

## 快速开始

```bash
# 安装
npm install -g browser-web-search@0.4.3

# 查看所有命令
bws site list

# 搜索示例
bws site toutiao/search "ai search"             # 今日头条
bws site zhihu/search "ai agent" --count 5      # 知乎
bws site hn/search "llm" --sort date            # Hacker News
bws site github/search "ai search" --sort stars # GitHub
bws site youtube/search "ai agent"              # YouTube

# jq 过滤
bws site zhihu/search "ai" --jq '[.items[].url]'
```

## 内置平台（55 个）

### 🇨🇳 国内平台（30 个）

| 平台 | 命令 |
|-----|------|
| **今日头条** | `toutiao/search`, `toutiao/hot`, `toutiao/feed` |
| **微信公众号** | `weixin/search`, `weixin/article` |
| **小红书** | `xiaohongshu/search`, `xiaohongshu/note`, `xiaohongshu/comments`, `xiaohongshu/user_posts`, `xiaohongshu/me`, `xiaohongshu/feed` |
| **知乎** | `zhihu/search`, `zhihu/hot`, `zhihu/question`, `zhihu/me` |
| **微博** | `weibo/search`, `weibo/hot` |
| **Bilibili** | `bilibili/search`, `bilibili/popular`, `bilibili/trending`, `bilibili/ranking`, `bilibili/video`, `bilibili/comments`, `bilibili/history`, `bilibili/me`, `bilibili/feed` |
| **澎湃新闻** | `thepaper/search`, `thepaper/hot` |
| **腾讯新闻** | `qqnews/search`, `qqnews/hot` |
| **网易新闻** | `netease/search`, `netease/hot` |
| **新浪新闻** | `sina/search`, `sina/hot` |
| **36kr** | `36kr/search`, `36kr/newsflash`, `36kr/article` |
| **虎嗅** | `huxiu/search` |
| **华尔街见闻** | `wallstreetcn/search` |
| **东方财富** | `eastmoney/stock`, `eastmoney/news` |
| **雪球** | `xueqiu/search` |
| **掘金** | `juejin/search` |
| **CSDN** | `csdn/search` |
| **博客园** | `cnblogs/search` |
| **V2EX** | `v2ex/search` |
| **BOSS直聘** | `boss/search`, `boss/detail` |
| **Baidu** | `baidu/search` |
| **即刻** | `jike/search` |
| **虎扑** | `hupu/search` |
| **豆瓣** | `douban/search`, `douban/movie`, `douban/movie-hot`, `douban/top250`, `douban/comments` |
| **什么值得买** | `smzdm/search` |
| **起点中文网** | `qidian/search` |
| **有道翻译** | `youdao/translate` |
| **携程** | `ctrip/search` |
| **InfoQ** | `infoq/search` |

### 🌏 国际平台（25 个）

| 平台 | 命令 |
|-----|------|
| **Google** | `google/search` |
| **Bing** | `bing/search` |
| **DuckDuckGo** | `duckduckgo/search` |
| **GitHub** | `github/search` |
| **Hacker News** | `hn/search` |
| **Reddit** | `reddit/search` |
| **X (Twitter)** | `x/search` |
| **The Verge** | `verge/search` |
| **Ars Technica** | `ars/search` |
| **Engadget** | `engadget/search` |
| **LinkedIn** | `linkedin/search` |
| **BBC** | `bbc/news` |
| **Reuters** | `reuters/search` |
| **Stack Overflow** | `stackoverflow/search` |
| **Dev.to** | `devto/search` |
| **npm** | `npm/search` |
| **PyPI** | `pypi/search` |
| **arXiv** | `arxiv/search` |
| **YouTube** | `youtube/search`, `youtube/video`, `youtube/transcript`, `youtube/transcript-by-id`, `youtube/comments`, `youtube/channel`, `youtube/feed` |
| **IMDb** | `imdb/search`, `imdb/movie`, `imdb/top250` |
| **Genius** | `genius/search` |
| **GSMArena** | `gsmarena/search` |
| **Product Hunt** | `producthunt/today` |
| **Wikipedia** | `wikipedia/search`, `wikipedia/summary` |
| **Open Library** | `openlibrary/search` |
| **Yahoo Finance** | `yahoo-finance/quote` |

## 环境要求

- Node.js >= 18.0.0
- OpenClaw 环境

## 文档

详细使用说明：[SKILL.md](./SKILL.md)

## 链接

- [GitHub](https://github.com/sipingme/browser-web-search)
- [npm](https://www.npmjs.com/package/browser-web-search)

## License

MIT
