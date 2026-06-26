# Article Fetcher — OpenClaw Skill

抓取微信公众号、小红书、豆瓣、知乎等平台文章，自动处理图片上传至阿里云 OSS，
LLM 智能提取关键词（本地词频降级），一键存档到 Notion 数据库。

**版本**: 1.0.2 | **许可**: MIT | **作者**: Ajay Hao

---

## 🎯 核心能力

- **多平台支持**: 微信公众号、小红书、豆瓣、知乎
- **智能识别**: 自动识别文章来源平台
- **内容提取**: 标题、作者、发布时间、正文（HTML）、图片
- **图床集成**: 阿里云 OSS 自动上传，按 `article-001.jpg` 格式命名
- **智能关键词**: LLM 优先理解文章核心内容，本地词频分析降级兜底
- **一键存档**: HTML 内容解析为 Notion 结构化块，保留原始排版

## 🏗️ 处理流程

```
URL → 平台识别 (detector/) → 内容抓取 (fetchers/) → 图片上传 OSS (processors/)
   → 关键词提取 (LLM 优先 → 词频降级) → 字数统计 → Notion 存档 (archiver/)
```

## 📂 模块结构

```
article-fetcher/
├── main.py                      # 主入口 + 抓取器注册表
├── config.py                    # 配置管理（环境变量）
├── detector/
│   └── platform_detector.py     # URL → 平台识别
├── fetchers/
│   ├── base_fetcher.py          # 基础抓取器（HTTP + Cookies）
│   ├── wechat_fetcher.py        # 微信公众号
│   ├── xhs_fetcher.py           # 小红书
│   ├── douban_fetcher.py        # 豆瓣
│   └── zhihu_fetcher.py         # 知乎
├── processors/
│   └── image_processor.py       # 图片上传 OSS
├── archiver/
│   └── notion_archiver.py       # HTML → Notion 结构化块
└── utils/
    ├── http_client.py           # HTTP 客户端（带重试）
    ├── logger.py                # 日志配置
    ├── word_counter.py          # 字数统计
    └── tag_extractor.py         # 关键词提取（LLM + 词频降级）
```

## ⚙️ 配置

### 环境变量（`~/.openclaw/.env`）

```bash
# ========== 必需 ==========
ALIYUN_OSS_AK=your_access_key_id
ALIYUN_OSS_SK=your_access_key_secret
ALIYUN_OSS_BUCKET_ID=your_bucket_name
ALIYUN_OSS_ENDPOINT=oss-cn-shanghai.aliyuncs.com
NOTION_API_KEY=secret_xxx
NOTION_ARTICLE_DATABASE_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

# ========== 可选：LLM 关键词提取 ==========
DASHSCOPE_API_KEY=sk-xxx
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
DASHSCOPE_MODEL=qwen3.5-plus

# ========== 可选：Cookies（反爬）==========
ZHIHU_COOKIES_FILE=~/.cookies/zhihu_cookies.txt
WECHAT_COOKIES_FILE=~/.cookies/wechat_cookies.txt
```

### Notion 数据库字段

| 字段 | 类型 | 说明 |
|------|------|------|
| **Title** | title | 文章标题（≤200 字符） |
| **Source** | rich_text | 来源平台 |
| **Author** | rich_text | 作者 |
| **Link** | url | 原文链接 |
| **Tags** | multi_select | 关键词（自动提取 + 手动传入） |
| **PubDate** | date | 发布日期 |
| **Words** | number | 字数统计 |
| **ts** | date | 存档时间（东八区） |

### OSS 路径规范

图片: `articles/<平台码>/<article_id>/article-001.jpg`

## 📋 使用方法

### 命令行

```bash
cd ~/.openclaw/workspace-engineer/skills/article-fetcher
python3 main.py "文章 URL" [标签1] [标签2]
```

### Python 模块

```python
from main import fetch_and_archive_article

result = fetch_and_archive_article(
    url="https://example.com/article",
    tags=["tag1", "tag2"]
)

if result['success']:
    print(f"✅ {result['message']}")
else:
    print(f"❌ {result['message']} ({result['error_code']})")
```

### Cookies 配置

知乎和部分微信公众号需要登录态才能抓取完整内容，否则返回 403。

**获取步骤**：
1. 浏览器登录对应平台
2. 安装 Cookie-Editor 插件
3. 导出 Cookies 为 Netscape 格式
4. 保存到 `~/.cookies/<platform>_cookies.txt`

| 平台 | 默认路径 | 必需？ |
|------|----------|--------|
| 知乎 | `~/.cookies/zhihu_cookies.txt` | ✅ 必需 |
| 微信 | `~/.cookies/wechat_cookies.txt` | ❌ 可选 |
| 小红书 / 豆瓣 | — | 不需要 |

## 🔌 扩展新平台

1. `fetchers/` 下创建 `xxx_fetcher.py`，继承 `BaseFetcher` 实现 `fetch_article()`
2. `detector/platform_detector.py` 添加 URL 正则
3. `main.py` 的 `FETCHER_REGISTRY` 注册

## 🔐 安全说明

- Cookies 等敏感信息存储在本地，skill 不会上传或外泄
- OSS Bucket 建议配置最小权限（仅 PutObject/GetObject）
- Notion Integration 仅授予目标数据库读写权限
- 阿里云 Coding Plan Key（`sk-sp-` 前缀）禁止用于自动化脚本

## 🔧 故障排查

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 知乎 403 | Cookies 未配置或过期 | 更新 `~/.cookies/zhihu_cookies.txt` |
| 微信公众号 403 | 反爬拦截 | 配置 `~/.cookies/wechat_cookies.txt` |
| 图片上传失败 | OSS 配置错误 | 检查 AK/SK/Bucket/Endpoint |
| Notion 推送失败 | API Key 过期或权限不足 | 更新 Key，确认数据库权限 |
| 关键词质量差 | LLM 未配置/失败 | 配置 `DASHSCOPE_API_KEY` 提升质量 |

查看详细日志：
```bash
DEBUG=true python3 main.py "URL" 2>&1 | tee fetch.log
cat logs/article-fetcher.log
```
