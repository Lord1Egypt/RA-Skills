---
name: douyin-scraper
description: 爬取抖音搜索结果和热榜数据，使用 Playwright 自动化浏览器操作。支持自然语言搜索（如"搜索一下海鲜视频"）、关键词搜索、获取热榜、提取视频信息等功能。
---

# 抖音搜索爬虫 Skill

## 功能概述

使用 Playwright 自动化浏览器操作（移动端模式），爬取抖音搜索结果和热榜数据。

## 功能特性

- 🔍 **自然语言搜索** - 支持中文自然语言查询，自动提取关键词
- 🔑 **关键词搜索** - 按关键词搜索抖音视频
- 📊 **热榜获取** - 获取抖音热榜数据（公开 API，无需登录）
- 📝 **文案提取** - 提取视频标题、描述、作者等
- 🎬 **互动数据** - 获取播放量、点赞数、评论数等
- 💾 **数据导出** - 支持 JSON / CSV 格式输出

## 安装依赖

```bash
# Python 版本
pip install playwright
playwright install chromium

# Node.js 版本
npm install
npx playwright install chromium
```

## 使用方法

### 自然语言搜索（推荐）

Skill 支持中文自然语言查询，会自动提取关键词：

| 自然语言输入 | 提取的关键词 |
|---|---|
| 搜索一下海鲜视频 | 海鲜 |
| 帮我找小龙虾相关内容 | 小龙虾 |
| 看看海鲜售卖的视频 | 海鲜售卖 |
| 找一些海鲜做法 | 海鲜做法 |

### 方式一：Python 脚本（推荐）

```bash
# 自然语言搜索
python scripts/scraper.py search --keyword "搜索一下海鲜视频" --limit 10

# 关键词搜索
python scripts/scraper.py search --keyword "海鲜" --limit 10

# 获取热榜
python scripts/scraper.py hot --limit 20

# 搜索并保存结果
python scripts/scraper.py search --keyword "海鲜售卖" --limit 20 --output seafood_videos.json
```

### 方式二：Node.js 脚本

```bash
# 自然语言搜索
node scripts/douyin_scraper.js search "搜索一下海鲜视频" 10

# 关键词搜索
node scripts/douyin_scraper.js search "海鲜" 10

# 获取热榜
node scripts/douyin_scraper.js hot 20
```

## Agent 集成

当用户用自然语言请求搜索时，Agent 应：

1. **提取关键词** - 从自然语言中提取核心搜索词
2. **执行搜索** - 调用 `python scripts/scraper.py search --keyword "<关键词>" --limit <数量>`
3. **返回结果** - 将搜索结果以简洁格式呈现给用户

### 示例对话

```
用户: 搜索一下海鲜视频
Agent: 好的，我来搜索"海鲜"相关的视频...
→ python scripts/scraper.py search --keyword "海鲜" --limit 10
→ [展示结果]
```

## 输出数据格式

### JSON 格式

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
    "url": "https://www.douyin.com/search/海鲜",
    "tags": ["海鲜", "搜索"],
    "publish_time": "2026-06-06"
  }
]
```

## 注意事项

⚠️ **重要提示：**

1. **搜索需要 Playwright** - 搜索功能使用移动端浏览器渲染，需安装 Playwright 和 Chromium
2. **验证码** - 抖音可能触发验证码，脚本会自动等待，但频繁请求可能导致封禁
3. **热榜无需登录** - 热榜 API 是公开的，不需要浏览器
4. **请求间隔** - 建议在请求之间添加适当延时
5. **数据用途** - 仅供学习和研究使用

## 故障排除

### 问题：浏览器启动失败

```bash
playwright install chromium
```

### 问题：搜索结果为空

- 可能遇到验证码，尝试增加 `--delay` 参数
- 抖音页面结构可能已更新
- 检查网络连接

### 问题：热榜获取失败

- 检查网络连接
- API 可能需要更新

## 技术细节

- **搜索方式**: 使用移动端 User-Agent 访问 `douyin.com/search/<keyword>`，从渲染后的页面提取结果
- **热榜方式**: 直接调用公开 API `douyin.com/aweme/v1/web/hot/search/list/`
- **自然语言解析**: 使用正则匹配从中文自然语言中提取搜索关键词
