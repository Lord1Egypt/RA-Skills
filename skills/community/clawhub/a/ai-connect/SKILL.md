---
name: smseow-agent-reach
version: 1.0.0
description: (Simon专属) Agent Reach 联网工具 skill - 快速调用指南。核心平台使用方法，无需配置即可用。
keywords: [联网,Agent Reach,推特,Twitter,YouTube,B站,小红书,微博,爬虫,搜索]
---

# Agent Reach - AI 联网工具
让你的 AI Agent 能读取互联网主流平台

---

## 核心能力

**14 个平台支持：**
- 🐦 Twitter/X — 读推文、搜索、浏览时间线
- 📺 YouTube — 字幕提取、视频搜索
- 📖 Reddit — 搜索、读帖子和评论
- 📺 B站 — 字幕提取、搜索
- 📕 小红书 — 阅读、搜索、评论
- 💬 微博 — 热搜、搜索、用户动态
- 🌐 网页 — 任意网页阅读
- 📦 GitHub — 仓库、Issue、PR
- 📡 RSS — 订阅源
- 💼 LinkedIn — Profile、公司页面
- 💬 微信公众号 — 搜索、阅读
- 🎵 抖音 — 视频解析
- 📈 雪球 — 股票、帖子
- 🎙️ 小宇宙 — 播客转文字

---

## 触发词

`联网` / `agent reach` / `搜推特` / `看视频` / `读帖子`

---

## 无需配置直接用

### 🌐 网页阅读
```
"帮我看看这个链接"
→ curl https://r.jina.ai/URL

示例：
帮我看看 https://example.com
→ 自动用 Jina Reader 提取正文
```

### 📺 YouTube 视频
```
"这个视频讲了什么"
→ yt-dlp --dump-json URL
→ 提取字幕和描述

示例：
帮我看看这个 YouTube 视频 https://youtu.be/xxx 讲了什么
```

### 🐦 Twitter/X
```
"帮我看看这条推文"
→ twitter tweet URL

"搜一下推特上关于 XXX 的讨论"
→ twitter search "关键词"
```

### 📖 Reddit
```
"帮我看看 Reddit 上这个帖子"
→ rdt view URL

"搜一下 Reddit 上的讨论"
→ rdt search "关键词"
```

### 📺 B站
```
"帮我看看这个 B 站视频"
→ yt-dlp --dump-json URL
→ 提取字幕

示例：
B站视频 https://www.bilibili.com/video/xxx 讲了什么
```

### 📕 小红书
```
"帮我看看小红书上这个笔记"
→ xhs get URL

"搜一下小红书上的 XXX"
→ xhs search "关键词"
```

### 📱 微博
```
"帮我看看微博热搜"
→ weibo trending

"搜一下微博上关于 XXX 的讨论"
→ weibo search "关键词"
```

### 📦 GitHub
```
"这个 GitHub 仓库是做什么的"
→ gh repo view owner/repo

"帮我看看这个 Issue"
→ gh issue view URL

"搜一下 GitHub 上的项目"
→ gh search repos "关键词"
```

### 📡 RSS
```
"帮我订阅这个 RSS"
→ feedparser URL
```

---

## 需要配置的平台

部分平台需要登录 Cookie（告诉 Agent「帮我配 XXX」）：

| 平台 | 配置方式 |
|------|----------|
| 🐦 Twitter | Cookie |
| 📕 小红书 | Cookie |
| 📖 Reddit | rdt login |
| 💼 LinkedIn | Cookie |

**配置流程：**
1. 浏览器登录目标网站
2. 用 Cookie-Editor 插件导出 Cookie
3. 告诉 Agent「帮我配 Twitter，小红书等」

---

## 检查状态

```
"帮我检查 Agent Reach 状态"
→ agent-reach doctor
→ 显示每个渠道的状态（通/不通）
```

---

## 快速指令表

| 需求 | 命令 |
|------|------|
| 读网页 | `帮我看看这个链接[URL]` |
| YouTube | `这个视频讲了什么[URL]` |
| 搜推特 | `搜一下推特上[关键词]` |
| B站 | `B站视频[URL]讲了什么` |
| 小红书 | `搜一下小红书上[关键词]` |
| 微博热搜 | `微博现在什么热门` |
| GitHub | `这个仓库是做什么的[owner/repo]` |
| 检查状态 | `检查联网工具��态` |

---

## 输出格式

### 读网页
```
## 📖 网页内容
标题：[标题]

## 核心内容
[提取的正文]

## 链接
[相关链接]
```

### 视频总结
```
## 📺 视频信息
标题：[标题]
时长：[时长]

## 字幕要点
1. [要点1]
2. [要点2]
3. [要点3]
```

### 搜索结果
```
## 🔍 搜索结果：[关键词]

### 结果1
- 来源：[平台]
- 内容：[摘要]
- 链接：[URL]

### 结果2
...
```

---

## 注意事项

- ⚠️ 部分平台需要配置 Cookie
- ⚠️ 服务器部署需要代理（~$1/月）
- ✅ 本地电脑不需要代理
- ✅ 完全免费（除了可选代理）

---

*Agent Reach | AI 智能体联网工具*