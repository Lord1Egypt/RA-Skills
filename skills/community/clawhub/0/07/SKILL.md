---
name: "web-access"
version: "1.0.0"
description: "为AI Agent提供完整的互联网访问能力，支持多个主流平台"
author: "AI Skills Team"
tags: ["互联网", "Twitter", "YouTube", "Reddit", "爬虫"]
requires: []
---

# 互联网访问技能

为AI Agent提供完整的互联网访问能力，支持Twitter、YouTube、Reddit、小红书等平台。

## 技能描述

提供多个主流互联网平台的数据访问能力，包括Twitter、YouTube、Reddit、小红书、B站等。使用开源工具，零API费用，支持Cookie加密存储和安全审计。

## 使用场景

- 用户："搜索Twitter上的AI新闻" → 获取最新推文
- 用户："获取这个YouTube视频的字幕" → 下载视频字幕
- 用户："Reddit上关于Python的讨论" → 获取相关帖子
- 用户："小红书上有哪些穿搭推荐" → 搜索笔记内容

## 工具和依赖

### 工具列表

位于 `channels/` 目录：
- `twitter.py`：Twitter访问模块
- `youtube.py`：YouTube访问模块
- `reddit.py`：Reddit访问模块
- `xiaohongshu.py`：小红书访问模块
- `bilibili.py`：B站访问模块
- `web.py`：网页搜索模块

### API密钥

**部分平台需要Cookie**：
- Twitter：需要Cookie（必须登录）
- 小红书：需要Cookie（必须登录）
- YouTube：可选代理（海外IP限制）
- Reddit：无需配置
- B站：无需配置

### 外部依赖

- Python 3.10+
- yt-dlp（YouTube）
- bird（Twitter，可选）

## 配置说明

### 安装方法

```bash
cd 07-互联网访问
bash install.sh
```

### 平台配置

**Twitter**：
```bash
# 导出Cookie
python cookie_extract.py twitter

# 或手动设置
export TWITTER_COOKIE="your_cookie_here"
```

**YouTube**：
```bash
# 安装yt-dlp
pip install yt-dlp

# 可选：配置代理
export YOUTUBE_PROXY="socks5://127.0.0.1:1080"
```

**小红书**：
```bash
# 导出Cookie
python cookie_extract.py xiaohongshu
```

**Reddit**：无需配置，直接使用

**B站**：无需配置，直接使用

### Cookie加密存储

```bash
# 加密Cookie
python security/encrypt_cookies.py import --file cookies.json

# 使用时解密
python security/encrypt_cookies.py decrypt
```

## 使用示例

### 场景1：Twitter搜索

用户："搜索Twitter上的AI新闻"

AI：
```python
from channels.twitter import TwitterChannel
twitter = TwitterChannel()
tweets = twitter.search("AI news", limit=10)
# 返回：推文列表，包含内容、作者、时间等
```

### 场景2：YouTube字幕

用户："获取这个YouTube视频的字幕"
链接：https://youtube.com/watch?v=xxx

AI：
```python
from channels.youtube import YouTubeChannel
youtube = YouTubeChannel()
subtitles = youtube.get_subtitles("video_id")
# 返回：视频字幕文本
```

### 场景3：Reddit讨论

用户："Reddit上关于Python的讨论"

AI：
```python
from channels.reddit import RedditChannel
reddit = RedditChannel()
posts = reddit.search("Python", subreddit="learnprogramming", limit=20)
# 返回：帖子列表，包含标题、内容、评论等
```

### 场景4：小红书搜索

用户："小红书上有哪些穿搭推荐"

AI：
```python
from channels.xiaohongshu import XiaohongshuChannel
xhs = XiaohongshuChannel()
notes = xhs.search("穿搭", limit=10)
# 返回：笔记列表，包含内容、图片、点赞等
```

### 场景5：网页搜索

用户："搜索最新的AI新闻"

AI：
```python
from channels.web import WebChannel
web = WebChannel()
results = web.search("最新AI新闻")
# 返回：搜索结果，包含标题、链接、摘要
```

## 安全特性

### Cookie加密存储

```bash
# 加密Cookie
python security/encrypt_cookies.py import --file cookies.json --password "your-password"

# 轮换密钥（建议每月）
python security/encrypt_cookies.py rotate
```

### 审计监控

```bash
# 生成安全报告
python security/audit_monitor.py report --days 7

# 实时监控
python security/audit_monitor.py monitor
```

### 依赖安全检查

```bash
# 完整检查
python security/dependency_check.py full

# 建立基线
python security/dependency_check.py baseline
```

## 支持的平台

| 平台 | 功能 | Cookie | 备注 |
|------|------|--------|------|
| Twitter | 推文搜索、用户信息 | ✅ 需要 | 免费API有频率限制 |
| YouTube | 字幕、评论、元数据 | ❌ 不需要 | 可选代理 |
| Reddit | 帖子搜索、评论 | ❌ 不需要 | 公开API |
| 小红书 | 笔记搜索、用户信息 | ✅ 需要 | 需要登录 |
| B站 | 视频信息、弹幕 | ❌ 不需要 | 公开API |
| 网页搜索 | 搜索引擎集成 | ❌ 不需要 | DuckDuckGo等 |

## 故障排除

### 问题1：Twitter认证失败

**现象**：提示认证失败

**解决**：
```bash
# Cookie可能过期，重新导出
python cookie_extract.py twitter
```

### 问题2：YouTube无法访问

**现象**：连接超时

**解决**：
```bash
# 配置代理
export YOUTUBE_PROXY="socks5://127.0.0.1:1080"
```

### 问题3：依赖安装失败

**现象**：pip install报错

**解决**：
```bash
# 运行依赖检查
python security/dependency_check.py full
```

### 问题4：Cookie解密失败

**现象**：无法解密Cookie

**解决**：
```bash
# 删除密钥重新导入
rm ~/.config/agent-reach/.key
python security/encrypt_cookies.py import --file cookies.json
```

## 安全最佳实践

### ✅ 推荐做法

1. 使用专用账号，不要使用主账号的Cookie
2. 定期轮换Cookie（每月一次）
3. 始终使用加密存储
4. 使用可信代理或VPN
5. 每周运行一次安全检查

### ❌ 避免做法

1. 不要在公共网络运行
2. 不要将Cookie提交到Git
3. 不要使用免费代理
4. 不要过度请求（避免封号）
5. 不要分享Cookie给他人

## 注意事项

1. **请求频率**：各平台有频率限制，避免过度请求
2. **Cookie安全**：Cookie是敏感信息，务必加密存储
3. **代理使用**：访问YouTube等平台可能需要代理
4. **法律合规**：遵守各平台的使用条款和法律法规
5. **数据使用**：抓取的数据仅供个人使用，不得商用
