---
name: find-ebooks
version: 1.1.0
description: |
  搜好书 — 基于安娜档案(Anna's Archive)的电子书搜索引擎，覆盖 6 大中文图书平台。
  搜索 epub/pdf 格式电子书，获取完整元数据（书名、作者、年份、语言、大小、格式）
  和多源下载链接（慢速下载/快速下载/Amazon/微信读书），同时查询豆瓣读书、掌阅、
  天猫图书、当当网、京东图书、机械工业出版社的图书上架信息。
tags:
  - 图书搜索
  - 电子书下载
  - 安娜档案
  - 中文图书
  - book-search
  - ebook
author: LeisureLinux
---

# find-ebooks / 搜好书

## 核心指令

当用户需要搜索或下载电子书时，调用 `scripts/find_ebooks.py` 脚本查询安娜档案。
将搜索结果整理为表格 + 详情格式输出，确保每条 URL 为单行可复制状态。

**同时查询以下中文图书平台**，提供对应商品/搜索页面 URL：
- 豆瓣读书、掌阅 iReader、天猫图书、当当网、京东图书、机械工业出版社

## 触发条件

当用户出现以下意图时，应优先使用本技能：

- 搜索电子书："帮我找找关于 XX 的书"、"搜索 XX 电子书"
- 下载电子书："下载 XX 这本书"、"有 XX 的 epub/pdf 吗"
- 查询图书详情："XX 这本书的信息"、"XX 的作者是谁"
- 中文平台比价："XX 在哪个平台有卖"、"豆瓣上 XX 的评分"
- 提及特定平台："安娜档案"、"Anna's Archive"、"搜好书"、"找书"

## 依赖

```bash
pip install cloudscraper
```

**代理配置**（安娜档案 + 中文平台可能需要代理）：

```bash
export HTTP_PROXY=http://127.0.0.1:7890
```

**微信读书查询**（可选）：设置 `WEREAD_API_KEY` 环境变量。

## 使用方法

### 命令行

```bash
# 基本搜索（安娜档案 + 6 大中文平台 + 微信读书）
python scripts/find_ebooks.py "OpenAI Codex"

# 指定返回数量
python scripts/find_ebooks.py "机器学习" --max 5

# 跳过中文平台搜索（更快）
python scripts/find_ebooks.py "Python" --no-cn

# 跳过微信读书查询
python scripts/find_ebooks.py "Go语言" --no-weread

# JSON 输出
python scripts/find_ebooks.py "深度学习" --json

# 指定代理
python scripts/find_ebooks.py "语义网" --proxy http://127.0.0.1:7890
```

### Python API

```python
from scripts.find_ebooks import BookFinder

finder = BookFinder(proxy_url="http://127.0.0.1:7890")
results = finder.search_and_report("AI新生", max_results=3)

for r in results:
    print(f'📖 {r["title"]} - {r["author"]}')
    cn = r.get('cn_platforms', {})
    if cn.get('douban'):
        print(f'   豆瓣: {cn["douban"]["url"]}')
```

## 输出格式

### 概览表格

| # | 书名 | 作者 | 格式 | 大小 | 语言 | 年份 |
|---|------|------|------|------|------|------|

### 详情块（每本书）

每条结果包含以下字段（如存在）：

**安娜档案：**
- 详情页、慢速下载、快速下载、Amazon、Google Books、ISBN

**中文图书平台（6 个）：**
- ✅ **豆瓣读书** — 找到直接商品页
- 🔍 **掌阅 iReader** — 仅提供搜索结果页
- 🔍 **天猫图书** — 仅提供搜索结果页
- 🔍 **当当网** — 仅提供搜索结果页
- 🔍 **京东图书** — 仅提供搜索结果页
- 🔍 **机械工业出版社** — 仅提供搜索结果页

✅ 表示已从搜索结果页提取到直接商品链接
🔍 表示仅提供搜索页 URL（用户打开后手动选择）

所有 URL 均为完整单行，可直接从终端复制粘贴到浏览器。

## 技术细节

### 数据源

| 源 | 地址 | 搜索方式 |
|----|------|----------|
| 安娜档案 | `annas-archive.gd` | HTTP GET `/search`，解析 HTML |
| 豆瓣读书 | `book.douban.com` | `/subject_search?search_text=` |
| 掌阅 iReader | `ireader.com` | `/index.php?ca=search.keyword` |
| 天猫图书 | `list.tmall.com` | `/search_product.htm?q=` |
| 当当网 | `search.dangdang.com` | `/?key=` |
| 京东图书 | `search.jd.com` | `/Search?keyword=` |
| 机工社 | `cmpbook.com` | `/search.html?keyword=` |

### 中文平台搜索逻辑

1. 从安娜档案获取每本书的完整书名
2. 根据书名生成各平台搜索 URL
3. 尝试抓取搜索结果页，提取第一个结果的直接商品链接
4. 如果提取成功 → ✅ 图标 + 商品 URL
5. 如果提取失败 → 🔍 图标 + 搜索页 URL（用户可自行打开浏览）

### 反爬策略

- 安娜档案使用 `cloudscraper` 绕过 Cloudflare
- 中文平台使用独立 `requests.Session`（带中文 Accept-Language）
- 每个平台之间间隔 0.5 秒，避免触发限流
- 搜索结果页解析使用正则匹配，不依赖页面结构

## 故障排除

| 问题 | 原因 | 解决方法 |
|------|------|----------|
| 搜索返回空结果 | DDoS-Guard 验证失败 | 增加 delay；检查代理 |
| 中文平台全是 🔍 | 搜索结果页格式变化 | 手动打开搜索 URL 查看 |
| Amazon 链接无效 | 商品页已下架 | 手动搜索 ISBN |
| 微信读书查询失败 | API Key 未配置 | 设置 `WEREAD_API_KEY` |

## 发布与安装

```bash
# Codex 一键安装
unset GITHUB_TOKEN GH_TOKEN
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo LeisureLinux/Skills
```
