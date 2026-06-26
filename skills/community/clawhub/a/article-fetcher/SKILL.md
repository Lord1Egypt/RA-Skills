---
name: article-fetcher
description: "抓取微信公众号、小红书、豆瓣、知乎文章，自动上传 OSS 图片，LLM 智能提取关键词，一键存档到 Notion"
homepage: https://github.com/openclaw/openclaw
metadata:
  { "openclaw": { "emoji": "📰", "version": "1.0.2", "requires": { "bins": ["python3"], "env": ["ALIYUN_OSS_AK", "ALIYUN_OSS_SK", "ALIYUN_OSS_BUCKET_ID", "ALIYUN_OSS_ENDPOINT", "NOTION_API_KEY", "NOTION_ARTICLE_DATABASE_ID"] }, "primaryEnv": "NOTION_API_KEY", "install": [{ "id": "pip", "kind": "pip", "packages": "requests oss2 python-dotenv beautifulsoup4 lxml notion-client", "label": "Install Python dependencies" }] } }
---

# Article Fetcher v1.0.2

抓取微信公众号、小红书、豆瓣、知乎文章，自动上传 OSS 图床，LLM 智能关键词提取，一键存档到 Notion。

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量（`~/.openclaw/.env`）

```bash
# 必需：OSS 图床
ALIYUN_OSS_AK=your_ak
ALIYUN_OSS_SK=your_sk
ALIYUN_OSS_BUCKET_ID=your_bucket
ALIYUN_OSS_ENDPOINT=oss-cn-shanghai.aliyuncs.com

# 必需：Notion 存档
NOTION_API_KEY=secret_xxx
NOTION_ARTICLE_DATABASE_ID=database_id

# 可选：LLM 关键词提取（OpenAI 兼容接口，与 video-summarizer 共用配置）
LLM_API_KEY=sk-your-api-key
LLM_BASE_URL=https://api.deepseek.com
LLM_MODEL=deepseek-v4-pro

# 可选：Cookies（反爬，Netscape 格式）
WECHAT_COOKIES_FILE=~/.cookies/wechat_cookies.txt
ZHIHU_COOKIES_FILE=~/.cookies/zhihu_cookies.txt
```

### 3. 使用

```bash
cd <skill-dir>
python3 main.py "文章 URL" [标签1] [标签2]
```

**支持平台**：微信公众号 (`mp.weixin.qq.com`)、小红书 (`xiaohongshu.com` / `xhslink.com`)、豆瓣 (`douban.com`)、知乎 (`zhihu.com`)

## 处理流程

```
URL → 平台识别 → 内容抓取 → 图片上传 OSS → 关键词提取 (LLM → 词频降级) → Notion 存档
```

## Notion 数据库字段

| 字段 | 类型 | 说明 |
|------|------|------|
| Title | title | 文章标题（≤200 字符） |
| Source | rich_text | 来源平台 |
| Author | rich_text | 作者 |
| Link | url | 原文链接 |
| Tags | multi_select | 自动提取关键词 + 手动标签 |
| PubDate | date | 发布时间 |
| Words | number | 字数统计（剔除 HTML） |
| ts | date | 存档时间（东八区） |

## 关键说明

- **Cookies**：知乎/微信反爬需配置（Netscape 格式），小红书/豆瓣无需登录
- **关键词**：LLM 优先（OpenAI 兼容接口），未配置或失败自动降级本地词频
- **图片**：上传失败不阻断，成功多少记录多少
- **时间**：统一 `YYYY-MM-DD HH:MM:SS`，缺失时留空（不伪造）
- **模块**：`main.py` 可作 Python 模块调用：`from main import fetch_and_archive_article`

## 安全与隐私

- **URL 校验**：严格白名单匹配 hostname，拒绝路径拼接攻击
- **Cookie 隔离**：Netscape Cookies 按域名过滤，仅附加到匹配的请求
- **LLM 数据外发**：配置 `DASHSCOPE_API_KEY` 时，文章内容会发送至 DashScope API（仅用于关键词提取）
- **敏感信息**：AK/SK/Key 等仅存储于本地，skill 不会外泄
- **权限最小化**：OSS Bucket 建议仅授予 PutObject/GetObject，Notion Integration 仅授予目标数据库读写权限
- **依赖锁定**：requirements.txt 使用精确版本号，避免供应链风险

## 扩展平台

1. `fetchers/` 下创建 `xxx_fetcher.py`，继承 `BaseFetcher` 实现 `fetch_article()`
2. `detector/platform_detector.py` 的 `ALLOWED_HOSTS` 添加平台域名
3. `main.py` 的 `FETCHER_REGISTRY` 注册
