---
name: douyin-scraper
description: 爬取抖音热榜和搜索数据，支持自然语言搜索请求如"搜索一下海鲜视频"、"看看抖音热榜"
---

# 抖音数据爬虫 Skill

## 功能概述

获取抖音热榜数据和关键词搜索结果。

## 功能特性

- 🔥 **热榜获取** - 获取抖音实时热搜榜（公开 API，无需登录）
- 🔍 **关键词搜索** - 按关键词搜索抖音视频（Playwright 浏览器自动化 + API 回退）
- 📝 **文案提取** - 提取视频标题、描述、标签等
- 🎬 **数据统计** - 获取播放量、点赞数、评论数等

## 自然语言调用

当用户用自然语言表达搜索意图时，**直接调用**，无需用户手动指定命令。

### 识别模式

| 用户说 | 动作 | 命令 |
|--------|------|------|
| 搜索一下海鲜视频 | 搜索 | `python3 scripts/scraper.py search --keyword "海鲜" --limit 10` |
| 看看抖音热榜 | 热榜 | `python3 scripts/scraper.py hot --limit 20` |
| 找一些关于小龙虾的视频 | 搜索 | `python3 scripts/scraper.py search --keyword "小龙虾" --limit 10` |
| 抖音最近什么火 | 热榜 | `python3 scripts/scraper.py hot --limit 20` |
| 帮我搜一下美食 | 搜索 | `python3 scripts/scraper.py search --keyword "美食" --limit 10` |

### 关键词提取规则

1. 从用户自然语言中提取核心搜索词
2. 去掉"视频"、"一下"、"一些"等无意义词
3. 保留具体品类/主题词（如"海鲜"、"小龙虾"、"美食"）
4. 如果用户指定数量，使用 `--limit`；否则默认 10

## 依赖

Playwright 和 Chromium 浏览器。首次使用前运行：

```bash
pip install playwright && playwright install chromium
```

## 使用方法

### 搜索关键词

```bash
# 基本搜索
python3 scripts/scraper.py search --keyword "海鲜" --limit 10

# 仅使用热榜 API（更快，无需浏览器）
python3 scripts/scraper.py search --keyword "海鲜" --method api --limit 10

# 搜索并保存结果
python3 scripts/scraper.py search --keyword "海鲜售卖" --limit 20 --output seafood.json
```

### 获取热榜

```bash
# 获取热榜
python3 scripts/scraper.py hot --limit 20

# 保存热榜数据
python3 scripts/scraper.py hot --limit 50 --output hot.json
```

## 搜索方式说明

| 方式 | 说明 | 适用场景 |
|------|------|----------|
| `auto`（默认） | 先尝试浏览器搜索，失败则回退热榜 API | 通用 |
| `api` | 仅使用热榜 API，按关键词过滤 | 快速获取，无需浏览器 |
| `browser` | 仅使用 Playwright 浏览器 | 需要精确搜索结果 |

> ⚠️ 抖音网页版搜索需要登录。如果未登录，`auto` 模式会自动回退到热榜 API。

## 输出数据格式

### JSON

```json
[
  {
    "title": "视频标题",
    "description": "视频描述",
    "author": "作者昵称",
    "play_count": 1000000,
    "like_count": 50000,
    "comment_count": 2000,
    "share_count": 1000,
    "url": "https://www.douyin.com/video/xxx",
    "tags": ["标签1", "标签2"],
    "publish_time": "2026-06-08",
    "hot_value": 5000000
  }
]
```

## 注意事项

1. **遵守平台规则** - 合理使用，避免频繁请求
2. **数据用途** - 仅供学习和研究
3. **搜索限制** - 抖音网页搜索需登录，未登录时回退到热榜数据
4. **请求间隔** - 建议搜索间隔 ≥ 5 秒

## 技术架构

- **热榜 API**: `https://www.douyin.com/aweme/v1/web/hot/search/list/` — 公开接口，无需登录
- **搜索**: Playwright 浏览器自动化 → 抖音搜索页 → 提取 SSR/DOM 数据 → 回退热榜 API
