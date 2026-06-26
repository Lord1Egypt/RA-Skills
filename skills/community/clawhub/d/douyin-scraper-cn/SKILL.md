---
name: douyin-scraper
description: 爬取抖音爆款视频和文案数据。支持自然语言搜索（如"搜索一下海鲜视频"）和结构化 CLI 调用，使用 Playwright 自动化浏览器，无浏览器时自动降级为模拟数据。
---

# 抖音爆款爬虫 Skill

## 功能

- 🔍 **自然语言搜索** — 直接用中文搜索，如"搜索一下海鲜视频"
- 📊 **热榜获取** — "看看抖音热榜"、"美食热榜"
- 📝 **文案提取** — 提取视频标题、描述、标签
- 🎬 **数据导出** — JSON / CSV

## 快速使用（自然语言）

```bash
# 搜索视频
python scripts/nl_search.py "搜索一下海鲜视频"

# 热榜
python scripts/nl_search.py "看看抖音热榜有什么"

# 指定输出
python scripts/nl_search.py "找一些海鲜售卖相关的视频文案" -o result.json
```

### 自然语言格式

Agent 收到自然语言请求时，调用 `nl_search.py` 即可：

| 用户说 | 命令 |
|--------|------|
| 搜索一下海鲜视频 | `python scripts/nl_search.py "搜索一下海鲜视频"` |
| 看看抖音热榜 | `python scripts/nl_search.py "看看抖音热榜"` |
| 找5条小龙虾视频 | `python scripts/nl_search.py "找5条小龙虾视频"` |
| 美食热榜 | `python scripts/nl_search.py "美食热榜"` |

## 结构化 CLI

```bash
# Python
python scripts/scraper.py search --keyword "海鲜" --limit 10
python scripts/scraper.py hot --category "美食" --limit 20

# Node.js
node scripts/douyin_scraper.js search "海鲜" 10
node scripts/douyin_scraper.js hot "美食" 20
```

## 输出格式

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
    "publish_time": "2026-06-08"
  }
]
```

## 安装（可选 — 有浏览器时获取真实数据）

```bash
pip install playwright
playwright install chromium
```

未安装 Playwright 浏览器时自动降级为模拟数据，不会报错。

## 注意事项

- 仅供学习研究使用
- 遵守抖音平台规则，避免频繁请求
- 不要登录账号，避免风控
