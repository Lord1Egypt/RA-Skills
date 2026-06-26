# AI-Sentinel 安全配置

## API 调用白名单

本配置文件定义了技能允许访问的域名/IP白名单，用于安全审核。

### ✅ 已验证的官方API

| 域名 | 用途 | 数据类型 |
|------|------|----------|
| `api.github.com` | GitHub官方API | 公开仓库信息 |
| `github.com` | GitHub网页 | 备用爬取 |
| `export.arxiv.org` | arXiv学术API | 学术论文元数据 |
| `hacker-news.firebaseio.com` | HackerNews API | 技术社区讨论 |
| `api.twitter.com` | Twitter/X API v2 | 社交媒体(需认证) |
| `x.com` | Twitter/X 网页 | 备用方案 |

### ⚠️ 用户可配置的RSS源

| 域名模式 | 说明 |
|----------|------|
| `*.github.io` | GitHub Pages博客 |
| `*.medium.com` | Medium文章 |
| `*.blogspot.com` | Blogger博客 |
| `*.wordpress.com` | WordPress博客 |
| 其他 | 用户主动订阅的RSS源 |

### ⚠️ 中国AI公司网页

| 公司 | 域名 | 用途 |
|------|------|------|
| 智谱AI | `zhipuai.cn` | 新品发布 |
| MiniMax | `minimax.io` | 公司动态 |
| 扣子Coze | `coze.cn` | 平台更新 |

---

## 网络请求安全规则

### 1. 超时限制
```yaml
timeout:
  default: 30  # 默认30秒
  feedparser: 60  # RSS可延长至60秒
  web_scraping: 15  # 网页爬取15秒
```

### 2. 重试策略
```yaml
retry:
  max_attempts: 2
  backoff: exponential
  retry_codes: [429, 500, 502, 503, 504]
```

### 3. 速率限制
```yaml
rate_limit:
  github: 10  # requests/min (官方限制60)
  arxiv: 1    # requests/sec
  hn: 5       # requests/sec
  twitter: 15 # requests/15min (免费版限制)
```

### 4. User-Agent
```
AI-Sentinel/1.4.1 (+https://github.com/xiaopengs/ai-sentinel)
```

---

## 数据安全

### ✅ 不收集的数据
- 用户密码、Token（除明确配置的API密钥）
- 浏览器Cookie
- 个人隐私信息
- 系统敏感文件

### ⚠️ 仅收集的数据
- AI领域公开新闻/论文信息
- 开源项目元数据（stars, forks等）
- 技术社区讨论摘要
- 用户主动订阅的RSS内容

### 📤 数据流向
```
用户请求 → 本地处理 → 生成报告 → 显示给用户
     ↓
   API调用（仅公开数据）
     ↓
不上传到任何第三方服务器
```

---

## 合规说明

### 符合以下服务条款

| 服务 | 服务条款 | 合规说明 |
|------|----------|----------|
| GitHub | https://docs.github.com/en/terms | 使用官方API，符合速率限制 |
| arXiv | https://arxiv.org/help/api/tou | 学术用途，合理使用 |
| HackerNews | https://www.ycombinator.com/newsguidelines.html | 非商业用途，仅读取 |
| Twitter | https://developer.twitter.com/en/developer-terms | 用户自行配置认证 |

---

## 安全审核清单

- [x] 代码100%开源可审计
- [x] 仅使用官方公开API
- [x] 无后门或恶意代码
- [x] 无数据外泄行为
- [x] 遵守各平台服务条款
- [x] 添加速率限制
- [x] 尊重robots.txt
- [x] 提供用户退出机制

---

**最后更新**: 2026-04-20
**审核人**: xiaopengs
**版本**: 1.4.1
