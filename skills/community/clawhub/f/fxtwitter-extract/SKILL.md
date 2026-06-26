---
name: fxtwitter-extract
description: 使用 FxTwitter API 提取 X (Twitter) 文章内容。支持提取推文、线程、用户资料，包括文本、图片、视频、投票等。无需 API Key。
---

# FxTwitter Extract 技能

使用 [FxTwitter API](https://api.fxtwitter.com) 提取 X (Twitter) 内容。

## 特点

- ✅ **无需 API Key** - FxTwitter 是免费的公共服务
- ✅ **支持多种内容** - 文本、图片、视频、投票、引用
- ✅ **支持线程提取** - 可提取整个推文线程
- ✅ **支持用户资料** - 获取用户统计信息
- ✅ **隐私友好** - FxTwitter 不记录日志

## 使用方法

### 基本用法

```bash
# 提取单个推文
python ~/.openclaw/workspace/skills/fxtwitter-extract/scripts/fxtwitter_extract.py status <推文 ID>

# 提取推文（包含线程）
python ~/.openclaw/workspace/skills/fxtwitter-extract/scripts/fxtwitter_extract.py status <推文 ID> --thread

# 提取用户资料
python ~/.openclaw/workspace/skills/fxtwitter-extract/scripts/fxtwitter_extract.py profile <用户名>

# 从 URL 提取
python ~/.openclaw/workspace/skills/fxtwitter-extract/scripts/fxtwitter_extract.py url <X 文章 URL>

# 输出原始 JSON
python ~/.openclaw/workspace/skills/fxtwitter-extract/scripts/fxtwitter_extract.py status <推文 ID> --json
```

### 示例

```bash
# 提取 Elon Musk 的推文
python ~/.openclaw/workspace/skills/fxtwitter-extract/scripts/fxtwitter_extract.py status 1234567890

# 提取用户资料
python ~/.openclaw/workspace/skills/fxtwitter-extract/scripts/fxtwitter_extract.py profile elonmusk

# 从 URL 提取（支持 x.com 和 twitter.com）
python ~/.openclaw/workspace/skills/fxtwitter-extract/scripts/fxtwitter_extract.py url https://x.com/elonmusk/status/1234567890
```

## API 端点

FxTwitter 提供以下 API 端点：

| 端点 | 说明 | 示例 |
|------|------|------|
| `/2/status/:id` | 获取单个推文 | `/2/status/1234567890` |
| `/2/thread/:id` | 获取推文线程 | `/2/thread/1234567890` |
| `/2/profile/:handle` | 获取用户资料 | `/2/profile/elonmusk` |
| `/2/owoembed` | oEmbed 格式 | `/2/owoembed?url=...` |

**基础 URL:** `https://api.fxtwitter.com`

**必需 Header:**
- `User-Agent`: 必须标识你的应用（如 `MyBot/1.0`）

## 返回格式

### 推文响应

```json
{
  "code": 200,
  "message": "OK",
  "status": {
    "id": "1234567890",
    "text": "推文内容",
    "created_at": "2024-01-01T00:00:00Z",
    "replies": 10,
    "retweets": 100,
    "likes": 1000,
    "views": 50000,
    "media": {
      "photos": [{"url": "..."}],
      "videos": [{"url": "..."}]
    },
    "poll": {
      "options": [{"label": "选项 1", "votes": 100}]
    }
  },
  "author": {
    "name": "用户名",
    "screen_name": "handle",
    "avatar_url": "...",
    "followers": 1000000
  }
}
```

### 用户资料响应

```json
{
  "code": 200,
  "message": "OK",
  "user": {
    "screen_name": "elonmusk",
    "name": "Elon Musk",
    "description": "...",
    "followers": 236100712,
    "following": 1292,
    "tweets": 98573,
    "likes": 214954,
    "media_count": 4380,
    "verified": true,
    "location": "...",
    "joined": "Tue Jun 02 20:12:29 +0000 2009"
  }
}
```

## 在 Python 中直接使用

```python
import urllib.request
import json

def fetch_tweet(status_id: str) -> dict:
    url = f"https://api.fxtwitter.com/2/status/{status_id}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "MyBot/1.0"}
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode('utf-8'))

# 使用示例
data = fetch_tweet("1234567890")
print(data["status"]["text"])
```

## 限制

- **速率限制**: FxTwitter 有速率限制，但免费使用
- **User-Agent**: 必须提供 User-Agent header
- **API 稳定性**: API 可能随 Twitter/X 变化而更新

## 相关资源

- **官方文档**: https://docs.fxtwitter.com/
- **GitHub 项目**: https://github.com/FxEmbed/FxEmbed
- **状态页面**: https://status.fxtwitter.com
- **Crowdin 翻译**: https://crowdin.com/project/fxtwitter

## 支持的域名

FxTwitter 在以下域名运行（功能相同）：
- `fxtwitter.com` / `api.fxtwitter.com`
- `twittpr.com` (Discord sed 替换友好)
- `fixupx.com` (用于 x.com 链接)
- `fxbsky.app` (Bluesky 支持)

## 故障排除

### 404 错误
- 推文可能被删除或设为私密
- 推文 ID 不正确

### 401 错误
- 缺少 User-Agent header
- 添加 `User-Agent: MyBot/1.0` 到请求头

### 网络错误
- 检查网络连接
- FxTwitter 服务可能暂时不可用

## 与 DeepReader 的区别

| 特性 | FxTwitter Extract | DeepReader |
|------|------------------|------------|
| API | FxTwitter API | r.jina.ai |
| 需要登录 | ❌ 否 | ❌ 否 |
| 支持视频 | ✅ 是 | ✅ 是 |
| 支持投票 | ✅ 是 | ✅ 是 |
| 支持线程 | ✅ 是 | ✅ 是 |
| 结构化数据 | ✅ JSON | Markdown |
| 用户资料 | ✅ 支持 | ❌ 不支持 |

## 作者

基于 [FxEmbed/FxTwitter](https://github.com/FxEmbed/FxTwitter) 项目创建。
