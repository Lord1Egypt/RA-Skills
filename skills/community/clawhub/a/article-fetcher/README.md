# Article Fetcher — Hermes Skill

抓取微信公众号、小红书、豆瓣、知乎等平台文章，自动处理图片上传至阿里云 OSS，
LLM 智能提取关键词（本地词频降级），默认存档到 Obsidian 本地知识库（可选 Notion 双写）。

**版本**: 1.3.6 | **许可**: MIT | **作者**: Ajay Hao

---

## 🎯 核心能力

- **多平台支持**: 微信公众号、小红书、豆瓣、知乎
- **智能识别**: 自动识别文章来源平台
- **内容提取**: 标题、作者、发布时间、正文（HTML）、图片
- **图床集成**: 阿里云 OSS 自动上传，按 `article-001.jpg` 格式命名
- **智能关键词**: LLM 优先理解文章核心内容，本地词频分析降级兜底
- **灵活存档**: 默认 Obsidian 本地知识库（推荐），可选 Notion 双写，都不配则仅终端输出

## 🏗️ 存档模式

四种场景按需灵活切换：

| 场景 | Obsidian | Notion | 行为 |
|------|:---:|:---:|------|
| 🏠 **本地优先** | ✅ | ❌ | 存档到 Obsidian 本地知识库 |
| ☁️ **纯云端** | ❌ | ✅ | 存档到 Notion 数据库 |
| 🏠+☁️ **双写** | ✅ | ✅ | Obsidian + Notion 双存档 |
| 🔍 **预览** | ❌ | ❌ | 仅终端输出，不存档 |

## 🏗️ 处理流程

```
URL → 平台识别 (detector/) → 内容抓取 (fetchers/) → 图片上传 OSS (processors/)
   → 关键词提取 (LLM 优先 → 词频降级) → 字数统计 → Obsidian / Notion 存档 (archiver/)
```

## 📂 模块结构

```
article-fetcher/
├── main.py                      # 主入口 + 抓取器注册表 + 存档调度
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
│   ├── obsidian_archiver.py     # 🆕 HTML → Obsidian Markdown
│   └── notion_archiver.py       # HTML → Notion 结构化块（可选）
└── utils/
    ├── http_client.py           # HTTP 客户端（Session 复用）
    ├── logger.py                # 日志配置
    ├── word_counter.py          # 字数统计
    └── tag_extractor.py         # 关键词提取（LLM + 词频降级）
```

## ⚙️ 配置

### 环境变量

skill 读取 `$AGENT_HOME/.env`（通用，兼容 Hermes / OpenClaw 等任意 agent），回退 `$HERMES_HOME/.env`，最终回退当前目录 `.env`。

```bash
# 当前 agent 为 Hermes，设置一次即可：
export AGENT_HOME=$HERMES_HOME
```

```bash
# ========== 必需：OSS 图床 ==========
ALIYUN_OSS_AK=your_access_key_id
ALIYUN_OSS_SK=your_access_key_secret
ALIYUN_OSS_BUCKET_ID=your_bucket_name
ALIYUN_OSS_ENDPOINT=oss-cn-shanghai.aliyuncs.com

# ========== 推荐：Obsidian 本地存档 ==========
# Windows 示例：
OBSIDIAN_VAULT_PATH=D:\GitRepo\AjayObsidianVault
# macOS 示例：
# OBSIDIAN_VAULT_PATH=/Users/yourname/ObsidianVault
# Linux / 云服务器示例：
# OBSIDIAN_VAULT_PATH=/home/yourname/ObsidianVault

# ========== 可选：Notion 云端存档（双写时配置）==========
NOTION_API_KEY=secret_xxx
NOTION_ARTICLE_DATABASE_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

# ========== 可选：LLM 关键词提取（OpenAI 兼容接口，与 video-summarizer 共用配置）==========
LLM_API_KEY=sk-xxx
LLM_BASE_URL=https://api.deepseek.com
LLM_MODEL=deepseek-v4-pro

# ========== 可选：Cookies（反爬）==========
ZHIHU_COOKIES_FILE=~/.cookies/zhihu_cookies.txt
WECHAT_COOKIES_FILE=~/.cookies/wechat_cookies.txt
```

### Obsidian 存档格式

文章存入 `{OBSIDIAN_VAULT_PATH}/1-输入-收件箱/文章收藏/`。

- **文件命名**: `{YYYY-MM-DD}_{platform}_{title}.md`
- **Frontmatter**: YAML 格式，包含 `title` / `source` / `author` / `link` / `tags` / `pub_date` / `words` / `fetched` / `article_id`
- **正文**: HTML → Markdown 转换（`markdownify`），OSS 图片已内嵌

### Notion 数据库字段（可选）

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
cd D:\GitRepo\article-fetcher
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
    print(f"📁 存档目标：{result.get('archived_to', [])}")
else:
    print(f"❌ {result['message']} ({result['error_code']})")
```

### Cookies 配置

知乎和部分微信公众号需要登录态才能抓取完整内容，否则返回 403。

**知乎/微信二级回退策略**：Cookies HTTP 请求 → Playwright headless 浏览器 → 失败放弃（自动检测反爬页面）。

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

## 离线输入（HTML / MHTML）

除 URL 抓取外，也支持直接传入 HTML 文本或 `.mhtml` 文件（微信文章三级采集策略），由本工具完成图片 OSS 上传、URL 替换与 Obsidian/Notion 归档。

```bash
# 三级：MHTML 文件
python3 main.py --mhtml page.mhtml --url https://mp.weixin.qq.com/s/xxx 标签1

# 二级：粘贴 HTML（stdin）
cat page.html | python3 main.py --html - --url https://mp.weixin.qq.com/s/xxx

# 一级 / 原路径（不变）
python3 main.py "https://mp.weixin.qq.com/s/xxx" 标签1
```

- `--platform` 默认 `wechat`（直传 HTML/MHTML 无 URL，无法自动探测平台）
- `--url` 可选：图片下载 Referer 与归档 link；不传时回退平台默认 Referer（微信 `mp.weixin.qq.com`）
- 已修复微信懒加载（`data-src`→`src` 并删除）、MHTML 编码乱码、`data:image/svg+xml` 占位符过滤

## 🔌 扩展新平台

1. `fetchers/` 下创建 `xxx_fetcher.py`，继承 `BaseFetcher` 实现 `fetch_article()`
2. `detector/platform_detector.py` 添加 URL 正则
3. `main.py` 的 `FETCHER_REGISTRY` 注册

## 🔐 安全说明

- **Obsidian 本地落盘 + 图片云存储**: `.md` 笔记写入本地磁盘（Obsidian 部分纯本地），但文章图片会先上传至阿里云 OSS 图床（必需）后再嵌入笔记，**并非「零网络外发」**
- **LLM 关键词提取（可选）**: 配置 `LLM_API_KEY` 时，文章文本（前 12000 字符）会发送至你配置的 LLM API 端点；不配置则仅使用本地词频方案，无任何文本外发
- Cookies 等敏感信息存储在本地，skill 不会上传或外泄
- OSS Bucket 建议配置最小权限（仅 PutObject/GetObject）
- Notion Integration 仅授予目标数据库读写权限
- 阿里云 Coding Plan Key（`sk-sp-` 前缀）禁止用于自动化脚本

## 🔧 故障排查

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 知乎 403 | Cookies 未配置或过期 | 更新 Cookies 或 Playwright 自动回退 |
| 微信公众号 403 | 反爬拦截 | Playwright 自动回退或配置 Cookies |
| 图片上传失败 | OSS 配置错误 | 检查 AK/SK/Bucket/Endpoint |
| Obsidian 写入失败 | 路径不存在或权限不足 | 检查 `OBSIDIAN_VAULT_PATH` |
| Notion 推送失败 | API Key 过期或权限不足 | 更新 Key，确认数据库权限 |
| 关键词质量差 | LLM 未配置/失败 | 配置 `LLM_API_KEY` 提升质量 |
| 未存档（仅终端输出） | 存档目标均未配置 | 配置 `OBSIDIAN_VAULT_PATH` 或 Notion |

查看详细日志：
```bash
DEBUG=true python3 main.py "URL" 2>&1 | tee fetch.log
cat logs/article-fetcher.log
```
