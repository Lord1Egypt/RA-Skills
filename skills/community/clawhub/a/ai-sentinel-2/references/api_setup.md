# API配置指南

本文档说明如何配置各个平台的API以启用完整功能。

## Twitter/X API

### 为什么需要配置？

Twitter/X API用于采集：
- AI大咖的最新推文
- 关键词相关的讨论
- 热门话题

**不配置此API**：Twitter采集功能将自动跳过，不影响其他功能。

### 申请步骤

1. **申请开发者账号**
   - 访问 [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
   - 使用Twitter账号登录
   - 申请开发者访问（可能需要审核）

2. **创建项目和应用**
   - 创建新项目
   - 创建应用（选择"Create App"）
   - 获取 API Key 和 API Secret

3. **获取Bearer Token**
   - 在 Developer Portal 找到 "Authentication Tokens" 部分
   - 生成 Bearer Token

### 配置方法

编辑 `config/settings.yaml`：

```yaml
twitter:
  bearer_token: "YOUR_BEARER_TOKEN_HERE"
```

或在WebUI的"配置"页面输入。

### API限制说明

| 账号类型 | 搜索API | 用户推文 |
|---------|--------|---------|
| Free | 500/15min | 1000/15min |
| Basic | 10K/15min | 10K/15min |
| Pro | 100K/15min | 1M/15min |

默认配置使用免费额度，已做节流处理。

---

## GitHub API

### 无需配置

GitHub Trending功能使用公开的GitHub REST API，无需认证即可使用。

### API限制

- 未认证：60次/小时
- 已认证：5000次/小时

如需更高配额：
1. 在 [GitHub Settings](https://github.com/settings/tokens) 生成 Personal Access Token
2. 在请求时添加 Header：

```python
headers = {
    "Authorization": f"token {YOUR_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}
```

---

## arXiv API

### 无需配置

arXiv API是完全公开的学术论文接口：
- 地址：`http://export.arxiv.org/api/query`
- 无需认证
- 无严格限制（建议遵守服务条款）

---

## HackerNews API

### 无需配置

HackerNews Firebase API是公开接口：
- 地址：`https://hacker-news.firebaseio.com/v0/`
- 无需认证
- 无速率限制

---

## RSS订阅

### 无需配置

RSS/Atom订阅解析使用通用标准协议，支持：
- RSS 2.0
- Atom 1.0
- 大部分博客平台的订阅源

只需在 `config/sources.yaml` 中添加RSS地址即可。

### 测试RSS地址

在 `scripts/parsers/blog_rss.py` 中有测试函数：

```python
from blog_rss import validate_rss_url

result = validate_rss_url("https://example.com/feed.xml")
print(result)
```

---

## 自定义API

### 添加新的认证信息

在 `config/settings.yaml` 中添加：

```yaml
# 自定义API配置
custom_apis:
  my_api:
    api_key: "YOUR_API_KEY"
    api_secret: "YOUR_API_SECRET"
    base_url: "https://api.example.com"
```

### 在解析器中使用

```python
def fetch_custom_api(config, api_settings):
    api_key = api_settings.get("my_api", {}).get("api_key", "")
    
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    response = requests.get(
        config["url"],
        headers=headers
    )
    return response.json()
```

---

## 安全建议

### 1. 保护API密钥

- **不要**将真实的API密钥提交到代码仓库
- 使用环境变量：

```python
import os

bearer_token = os.environ.get("TWITTER_BEARER_TOKEN", "")
```

- 或创建 `config/secrets.yaml`（已加入.gitignore）：

```yaml
twitter:
  bearer_token: "REAL_TOKEN"
```

### 2. 本地配置文件

项目包含 `.gitignore` 文件，会忽略：

```
config/settings.yaml
config/secrets.yaml
output/
```

首次使用时，复制模板配置：

```bash
cp config/settings.yaml.example config/settings.yaml
```

### 3. 定期轮换密钥

定期更新API密钥，特别是生产环境。

---

## 故障排除

### Twitter采集失败

1. 检查Bearer Token是否正确
2. 确认开发者账号状态正常
3. 检查API配额是否用尽
4. 查看 [Twitter API Status](https://api.twitterstat.us/)

### GitHub API 403错误

通常是被限流，解决方案：
- 添加认证Token
- 减少采集频率
- 使用备用解析器（直接爬取Trending页面）

### RSS解析失败

常见原因：
- RSS地址已失效
- 需要认证
- 非标准格式

解决方案：
- 在浏览器中直接打开RSS地址验证
- 使用在线RSS验证工具
- 联系博客管理员获取正确的订阅地址

---

## 资源链接

| 平台 | 开发者门户 | 文档 |
|------|----------|------|
| Twitter/X | [Developer Portal](https://developer.twitter.com/en/portal/dashboard) | [API v2 Docs](https://developer.twitter.com/en/docs/twitter-api) |
| GitHub | [Settings](https://github.com/settings/tokens) | [REST API](https://docs.github.com/en/rest) |
| arXiv | - | [API Guide](https://info.arxiv.org/help/api/basics.html) |
| HackerNews | - | [Firebase API](https://github.com/HackerNews/API) |
