---
name: douyin-scraper
description: 爬取抖音爆款视频和文案数据，使用 Playwright 自动化浏览器操作，支持搜索关键词、获取热榜、提取视频信息和文案等功能。
---

# 抖音爆款爬虫 Skill

使用 Playwright 自动化浏览器操作，爬取抖音爆款视频和文案数据。

## Agent 调用指引

当用户用自然语言请求抖音相关操作时，**直接执行对应命令**，不需要再确认。

| 用户意图 | 命令 |
|---------|------|
| 搜索海鲜视频 | `python scripts/scraper.py search --keyword "海鲜" --limit 10` |
| 搜一下小龙虾 | `python scripts/scraper.py search --keyword "小龙虾" --limit 10` |
| 看看热榜 | `python scripts/scraper.py hot --limit 20` |
| 美食热榜 | `python scripts/scraper.py hot --category "美食" --limit 20` |
| 搜索并保存 | `python scripts/scraper.py search --keyword "海鲜" --limit 15 --output seafood.json` |

### 自然语言匹配规则

1. **搜索类** — 用户说"搜索/搜一下/找/看看 + 关键词"→ `search --keyword "<关键词>"`
2. **热榜类** — 用户说"热榜/热搜/热门/排行榜"→ `hot`
3. **分类热榜** — 用户说"XX热榜"→ `hot --category "<分类>"`
4. **保存结果** — 用户提到"保存/导出/下载结果"→ 加 `--output <文件名>.json`

> **工作目录**: 命令在 skill 根目录下执行，即 `cd /root/.openclaw/workspace/douyin-scraper && ...`

## 功能特性

- 🔍 **关键词搜索** — 按关键词搜索抖音视频，解析真实搜索结果
- 📊 **热榜获取** — 获取抖音热榜数据
- 📝 **文案提取** — 提取视频标题、描述、标签等
- 🎬 **视频信息** — 获取播放量、点赞数、评论数等
- 🔗 **链接收集** — 收集视频链接用于后续下载
- 💾 **数据导出** — 支持 JSON / CSV 格式导出

## 依赖

需要 Playwright + Chromium：

```bash
pip install playwright
playwright install chromium
```

## 命令参考

### 搜索

```bash
python scripts/scraper.py search --keyword "海鲜" --limit 10
python scripts/scraper.py search -k "海鲜售卖" -n 15 -o seafood.json
python scripts/scraper.py search -k "小龙虾" -n 10 -f csv -o crayfish.csv
```

### 热榜

```bash
python scripts/scraper.py hot --limit 20
python scripts/scraper.py hot --category "美食" -n 20 -o food_hot.json
```

### 选项

| 选项 | 说明 |
|------|------|
| `--keyword, -k` | 搜索关键词 |
| `--limit, -n` | 结果数量 (默认 10/20) |
| `--output, -o` | 输出文件路径 |
| `--format, -f` | 输出格式: json (默认), csv |
| `--no-headless` | 显示浏览器窗口 (调试用) |

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
    "publish_time": "2026-05-31"
  }
]
```

### CSV

```csv
title,author,play_count,like_count,comment_count,url,tags
视频标题,作者昵称,1000000,50000,2000,https://...,标签1|标签2
```

## 注意事项

⚠️ **重要提示：**

1. **遵守平台规则** — 合理使用，避免频繁请求
2. **请求间隔** — 默认 2 秒延时，可通过 `--delay` 调整
3. **数据用途** — 仅供学习和研究
4. **账号安全** — 不要登录账号，避免风控
5. **IP 限制** — 注意 IP 被封禁风险

## 故障排除

| 问题 | 解决方案 |
|------|---------|
| 浏览器启动失败 | `playwright install chromium` |
| 页面加载超时 | 检查网络，尝试代理 |
| 找不到元素 | 抖音页面可能更新，需更新选择器 |
| 返回空结果 | 可能被风控，尝试降低频率或换 IP |
