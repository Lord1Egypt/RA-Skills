---
name: article-fetcher
description: "抓取微信公众号、小红书、豆瓣、知乎文章，自动上传 OSS 图片，LLM 智能提取关键词，一键存档到 Obsidian 本地知识库（可选 Notion）"
homepage: https://github.com/AjayHao/article-fetcher
metadata:
  { "hermes": { "emoji": "📰", "version": "1.3.6", "requires": { "bins": ["python3"], "env": ["ALIYUN_OSS_AK", "ALIYUN_OSS_SK", "ALIYUN_OSS_BUCKET_ID", "ALIYUN_OSS_ENDPOINT", "NOTION_API_KEY", "LLM_API_KEY"] }, "primaryEnv": "OBSIDIAN_VAULT_PATH", "permissions": ["env:read", "net:outbound", "fs:write"], "allowedEnv": ["ALIYUN_OSS_AK", "ALIYUN_OSS_SK", "ALIYUN_OSS_BUCKET_ID", "ALIYUN_OSS_ENDPOINT", "OBSIDIAN_VAULT_PATH", "NOTION_API_KEY", "NOTION_ARTICLE_DATABASE_ID", "LLM_API_KEY", "LLM_BASE_URL", "LLM_MODEL", "WECHAT_COOKIES_FILE", "ZHIHU_COOKIES_FILE"], "securityNote": "OSS 凭证用于图片上传存储（图片外发至阿里云 OSS 为必需）；Notion 和 LLM 为可选集成，不配置则跳过对应功能；配置 LLM 时文章文本（前 12000 字符）会发送至你配置的 LLM API 端点", "install": [{ "id": "pip", "kind": "pip", "packages": "requests oss2 python-dotenv beautifulsoup4 lxml notion-client markdownify pyyaml", "label": "Install Python dependencies" }, { "id": "playwright", "kind": "shell", "command": "playwright install chromium", "label": "Install Playwright Chromium browser" }] } }
---

# Article Fetcher v1.3.6

抓取微信公众号、小红书、豆瓣、知乎文章，自动上传 OSS 图床，LLM 智能关键词提取，默认存档到 Obsidian 本地知识库（可选 Notion 双写）。

## 存档模式

四种场景按需灵活切换，不存档时仅终端输出抓取结果：

| 场景 | Obsidian | Notion | 行为 |
|------|:---:|:---:|------|
| 🏠 **本地优先** | ✅ | ❌ | 存档到 Obsidian 本地知识库 |
| ☁️ **纯云端** | ❌ | ✅ | 存档到 Notion 数据库 |
| 🏠+☁️ **双写** | ✅ | ✅ | Obsidian + Notion 双存档 |
| 🔍 **预览** | ❌ | ❌ | 仅终端输出，不存档 |

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

skill 通过 `$AGENT_HOME/.env` 加载配置（自动兼容 Hermes / OpenClaw 等 agent）。设置方式：

```bash
# 当前 agent 为 Hermes，只需设置一次：
export AGENT_HOME=$HERMES_HOME
```

环境变量清单（写入 `$AGENT_HOME/.env` 或系统环境变量）：

```bash
# ========== 必需：OSS 图床 ==========
ALIYUN_OSS_AK=your_ak
ALIYUN_OSS_SK=your_sk
ALIYUN_OSS_BUCKET_ID=your_bucket
ALIYUN_OSS_ENDPOINT=oss-cn-shanghai.aliyuncs.com

# ========== 推荐：Obsidian 本地存档 ==========
# Windows 示例：
OBSIDIAN_VAULT_PATH=D:\GitRepo\AjayObsidianVault
# macOS 示例：
# OBSIDIAN_VAULT_PATH=/Users/yourname/ObsidianVault
# Linux / 云服务器示例：
# OBSIDIAN_VAULT_PATH=/home/yourname/ObsidianVault

# ========== 可选：Notion 云端存档 ==========
NOTION_API_KEY=secret_xxx
NOTION_ARTICLE_DATABASE_ID=database_id

# ========== 可选：LLM 关键词提取（OpenAI 兼容接口，与 video-summarizer 共用配置）==========
LLM_API_KEY=***
LLM_BASE_URL=https://api.deepseek.com
LLM_MODEL=deepseek-v4-pro

# ========== 可选：Cookies（反爬，Netscape 格式）==========
WECHAT_COOKIES_FILE=~/.cookies/wechat_cookies.txt
ZHIHU_COOKIES_FILE=~/.cookies/zhihu_cookies.txt
```

### 3. 使用

```bash
cd <skill-dir>
python3 main.py "文章 URL" [标签1] [标签2]
```

**支持平台**：微信公众号 (`mp.weixin.qq.com`)、小红书 (`xiaohongshu.com` / `xhslink.com`)、豆瓣 (`douban.com`)、知乎 (`zhihu.com`)

## 离线输入（HTML / MHTML）

除 URL 外，支持直接喂入 HTML 文本或 `.mhtml` 文件（源自 wechat-article-capture 技能的三级策略），由 article-fetcher 负责图片上传 OSS、替换 URL 与归档。解析层已内置三处陷阱修复：微信懒加载 `data-src`→`src` 并删除 `data-src`、MHTML 编码乱码（charset 探测）、`data:image/svg+xml` 占位符过滤。

```bash
# 三级：MHTML 文件
python3 main.py --mhtml page.mhtml --url https://mp.weixin.qq.com/s/xxx 标签1

# 二级：粘贴 HTML（stdin）
cat page.html | python3 main.py --html - --url https://mp.weixin.qq.com/s/xxx

# 一级 / 原路径（不变）
python3 main.py "https://mp.weixin.qq.com/s/xxx" 标签1
```

- `--platform` 默认 `wechat`（直传 HTML/MHTML 无 URL，无法自动探测平台）
- `--url` 可选：作为图片下载 Referer 与归档 link；不传时回退平台默认 Referer（微信 `mp.weixin.qq.com`）
- 解析产出标准 `article_data`，后半段管线（OSS 上传 → 替换 → 打标 → 字数 → 归档）与 URL 模式完全复用

## 处理流程

```
URL → 平台识别 → 内容抓取 → 图片上传 OSS → 关键词提取 (LLM → 词频降级)
                                              │
                         ┌────────────────────┴────────────────────┐
                         ▼                                         ▼
                  OBSIDIAN_VAULT_PATH?                     NOTION_API_KEY?
                    ✅ → Obsidian .md                       ✅ → Notion 页面
                    都不配 → 终端输出
```

## Obsidian 存档格式

文章存入 `{OBSIDIAN_VAULT_PATH}/收件箱/`，命名规则 `{YYYY-MM-DD}_{title}.md`。

> 💡 **本地适配**：Vault 去序号后，存档目录从 `1-收件箱/` 改为 `收件箱/`（`obsidian_archiver.py` 已同步修正）。

### 文件示例

```markdown
---
title: "AI Agent 技术全景解析"
source: wechat
author: "张三"
link: "https://mp.weixin.qq.com/s/xxx"
tags:
  - AI Agent
  - LLM
  - 技术架构
pub_date: "2026-05-10 14:30:00"
words: 3500
fetched: "2026-06-22 20:15:00"
article_id: "uuid"
---

# AI Agent 技术全景解析

正文内容（HTML → Markdown 转换，OSS 图片已内嵌）...
```

### 设计要点

- **Frontmatter**：YAML 格式，Obsidian 原生兼容，tag 列表可直接被 Dataview 查询
- **文件命名**：标题即文件名，非法字符自动替换为 `-`
- **HTML→Markdown**：通过 `markdownify` 转换，保留链接、图片、粗斜体等格式
- **非阻塞**：Obsidian 写入失败不影响 Notion 存档（如果配置了双写）

## Notion 数据库字段（可选）

配置 `NOTION_API_KEY` + `NOTION_ARTICLE_DATABASE_ID` 后启用双写。

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
- **知乎 / 微信二级回退**：HTTP (Cookies) → Playwright 浏览器 → 失败放弃。自动检测反爬页面（环境异常/验证码）并回退
- **空内容检测**：正文为空或含反爬关键词时视为抓取失败，不生成垃圾文件
- **Playwright**：执行 `playwright install chromium` 后自动生效，未安装时跳过浏览器回退
- **关键词**：LLM 优先（OpenAI 兼容接口），未配置或失败自动降级本地词频
- **图片**：上传失败不阻断，成功多少记录多少
- **时间**：统一 `YYYY-MM-DD HH:MM:SS`，缺失时留空（不伪造）
- **模块**：`main.py` 可作 Python 模块调用：`from main import fetch_and_archive_article`
- **Obsidian 本地落盘 + 图片 OSS 上传**：`.md` 笔记写入本地磁盘，但文章图片会上传至阿里云 OSS 图床（必需）后再嵌入，并非纯本地；LLM 关键词提取为可选功能，启用时文章文本（前 12000 字符）会发送至配置的 API 端点

## 安全与隐私

- **URL 校验**：严格白名单匹配 hostname，拒绝路径拼接攻击
- **Cookie 隔离**：Netscape Cookies 按域名过滤，仅附加到匹配的请求
- **LLM 数据外发**：配置 `LLM_API_KEY` 时，文章内容（前 12000 字符）会发送至配置的 API 端点（仅用于关键词提取）。不配置则不发送
- **图片下载**：自动下载原文图片并上传 OSS，过程中会请求第三方图片服务器，请确保有权抓取目标文章
- **敏感信息**：AK/SK/Key 等仅存储于本地，skill 不会外泄
- **Obsidian 本地落盘**：`.md` 文件写入本地磁盘；但文章图片需上传阿里云 OSS（必需），因此并非「零网络外发」
- **权限最小化**：OSS Bucket 建议仅授予 PutObject/GetObject；Notion Integration 仅授予目标数据库读写权限
- **依赖锁定**：requirements.txt 使用精确版本号，避免供应链风险

## 扩展平台

1. `fetchers/` 下创建 `xxx_fetcher.py`，继承 `BaseFetcher` 实现 `fetch_article()`
2. `detector/platform_detector.py` 的 `ALLOWED_HOSTS` 添加平台域名
3. `main.py` 的 `FETCHER_REGISTRY` 注册
