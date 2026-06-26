---
name: douyin-scraper
description: 爬取抖音爆款视频和文案数据，使用 Playwright 自动化浏览器操作，支持搜索关键词、获取热榜、提取视频信息和文案等功能。
---

# 抖音爆款爬虫 Skill

## Agent 指令：自然语言解析

当用户用自然语言请求抖音相关操作时，按以下规则映射到命令：

| 用户意图 | 关键词提取 | 执行命令 |
|---|---|---|
| 搜索/找/看一下 XX 视频 | 提取 XX 作为 keyword | `python scripts/scraper.py search --keyword "XX" --limit 10` |
| 抖音热榜/热门/趋势 | 无需 keyword | `python scripts/scraper.py hot --limit 20` |
| XX 分类的热榜 | 提取 XX 作为 category | `python scripts/scraper.py hot --category "XX" --limit 20` |
| 分析视频链接 URL | 提取 URL | 提示用户：当前版本暂不支持单视频解析，建议用搜索关键词替代 |

**解析步骤：**
1. 判断用户意图是「搜索」还是「热榜」
2. 从自然语言中提取关键词（去掉"视频"、"内容"、"一下"等虚词）
3. 在 skill 目录下执行对应命令
4. 将结果以简洁列表形式呈现给用户

**示例：**
- "搜索一下海鲜视频" → `python scripts/scraper.py search --keyword "海鲜" --limit 10`
- "找一些海鲜售卖相关的视频文案" → `python scripts/scraper.py search --keyword "海鲜售卖" --limit 10`
- "看看抖音热榜有什么" → `python scripts/scraper.py hot --limit 20`
- "美食热榜" → `python scripts/scraper.py hot --category "美食" --limit 20`

## 功能概述

使用 Playwright 自动化浏览器操作，爬取抖音爆款视频和文案数据。

## 功能特性

- 🔍 **关键词搜索** - 按关键词搜索抖音视频
- 📊 **热榜获取** - 获取抖音热榜数据
- 📝 **文案提取** - 提取视频标题、描述、标签等
- 🎬 **视频信息** - 获取播放量、点赞数、评论数等
- 🔗 **链接收集** - 收集视频链接用于后续下载

## 安装依赖

```bash
pip install playwright
playwright install chromium
```

## 使用方法

### 搜索关键词

```bash
python scripts/scraper.py search --keyword "海鲜" --limit 10
```

### 获取热榜

```bash
python scripts/scraper.py hot --limit 20
python scripts/scraper.py hot --category "美食" --limit 20
```

### 保存结果

```bash
python scripts/scraper.py search --keyword "海鲜" --limit 10 --output result.json
python scripts/scraper.py search --keyword "海鲜" --limit 10 --output result.csv --format csv
```

## 输出数据格式

```json
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
  "publish_time": "2026-03-21"
}
```

## 注意事项

⚠️ **重要提示：**

1. 遵守抖音平台规则，合理使用，避免频繁请求
2. 建议请求之间添加适当延时
3. 数据仅供学习和研究使用
4. 不要登录账号，避免风控
5. 注意 IP 被封禁的风险
6. 如果 Playwright 未安装，将返回模拟数据（标注"模拟数据"）
7. **验证码问题**：抖音对未登录的 headless 浏览器会弹出验证码，导致无法提取真实数据。此时脚本会自动降级为模拟数据

## 获取真实数据的方案

当脚本遇到验证码时，可使用以下方式获取真实数据：

### 方案一：使用 OpenClaw browser 工具（推荐）

通过 OpenClaw 的 `browser` 工具在已登录的浏览器中操作抖音：

```
1. browser open → 打开 https://www.douyin.com
2. browser snapshot → 查看页面状态
3. browser navigate → 访问搜索页
4. browser snapshot → 提取搜索结果
```

### 方案二：传入 Cookie 文件

```bash
python scripts/scraper.py search --keyword "海鲜" --cookie-file cookies.json
```

Cookie 文件格式为 Playwright 的 `browser_context.cookies()` 输出的 JSON 数组。
