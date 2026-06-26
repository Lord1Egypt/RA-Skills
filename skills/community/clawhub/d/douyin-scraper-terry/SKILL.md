---
name: douyin-scraper
description: 爬取抖音爆款视频和文案数据，支持自然语言搜索请求（如"搜索一下海鲜视频"）、关键词搜索、热榜获取、视频信息提取等。
---

# 抖音爆款爬虫 Skill

使用 Playwright 自动化浏览器操作，爬取抖音爆款视频和文案数据。

## 🧠 自然语言请求处理（Agent 必读）

当用户用自然语言发出搜索请求时，你需要从中提取关键词并调用脚本。

### 识别规则

| 用户说法 | 提取关键词 | 执行命令 |
|---|---|---|
| 搜索一下海鲜视频 | `海鲜` | `python scripts/scraper.py search --keyword "海鲜" --limit 10` |
| 帮我找小龙虾相关的抖音 | `小龙虾` | `python scripts/scraper.py search --keyword "小龙虾" --limit 10` |
| 抖音上有什么海鲜售卖的视频 | `海鲜售卖` | `python scripts/scraper.py search --keyword "海鲜售卖" --limit 10` |
| 看看抖音热榜 | _(无)_ | `python scripts/scraper.py hot --limit 20` |
| 美食热榜有什么 | `美食` | `python scripts/scraper.py hot --category "美食" --limit 20` |

### 提取原则

1. **去掉功能词** — "搜索一下"、"帮我找"、"看看"、"有没有" 等是意图词，不是关键词
2. **去掉平台词** — "抖音"、"视频"、"相关" 等是领域词，不是关键词
3. **保留核心实体** — "海鲜"、"小龙虾"、"海鲜售卖" 才是搜索关键词
4. **数量词可选** — "找10个海鲜视频" → 提取 `--limit 10`，默认 10
5. **输出可选** — "保存到xxx.json" → 提取 `--output xxx.json`，默认不保存文件

### 执行步骤

1. 从用户消息中提取意图（search / hot）和关键词
2. 在 skill 目录下执行 Python 脚本（优先）或 Node.js 脚本
3. 将结果以可读格式呈现给用户

```bash
# 进入 skill 目录
cd /root/.openclaw/workspace/douyin-scraper

# 搜索（Python 版本，推荐）
python scripts/scraper.py search --keyword "提取的关键词" --limit 10

# 热榜
python scripts/scraper.py hot --limit 20

# 如需保存结果
python scripts/scraper.py search --keyword "关键词" --limit 10 --output result.json
```

## 功能特性

- 🔍 **关键词搜索** — 按关键词搜索抖音视频
- 🗣️ **自然语言入口** — 支持"搜索一下xxx视频"等自然语言请求
- 📊 **热榜获取** — 获取抖音热榜数据
- 📝 **文案提取** — 提取视频标题、描述、标签等
- 🎬 **视频信息** — 获取播放量、点赞数、评论数等
- 💾 **数据导出** — 支持 JSON / CSV 格式输出

## 安装依赖

```bash
cd /root/.openclaw/workspace/douyin-scraper

# Python 版本（推荐）
pip install playwright
playwright install chromium

# 或 Node.js 版本
npm install
npx playwright install chromium
```

> **注意：** 未安装 Playwright 时脚本仍可运行，会返回模拟数据用于开发测试。

## 使用方法

### Python 版本（推荐）

```bash
python scripts/scraper.py search --keyword "海鲜" --limit 10
python scripts/scraper.py search --keyword "海鲜售卖" --limit 20 --output seafood.json
python scripts/scraper.py hot --limit 20
python scripts/scraper.py hot --category "美食" --limit 20 --output food_hot.json
```

### Node.js 版本

```bash
node scripts/douyin_scraper.js search "海鲜" 10
node scripts/douyin_scraper.js hot 20
```

### 使用启动脚本

```bash
./scripts/run.sh search --keyword "海鲜" --limit 10
```

## 输出数据格式

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
    "publish_time": "2026-03-21"
  }
]
```

## 注意事项

⚠️ **重要提示：**

1. 遵守抖音平台规则，合理使用，避免频繁请求
2. 建议请求间隔 ≥ 2 秒
3. 数据仅供学习和研究使用
4. 不要登录账号，避免风控
5. 注意 IP 限制风险

## 故障排除

| 问题 | 解决方案 |
|---|---|
| 浏览器启动失败 | `playwright install chromium` |
| 页面加载超时 | 增加超时时间 / 检查网络 / 使用代理 |
| 找不到元素 | 抖音页面可能已更新，需更新选择器 |
| 未安装 Playwright | 脚本自动降级为模拟数据模式 |

## 配合使用的 Skill

- `douyin-download` — 下载抖音视频
- `video-merger` — 合并视频
- `eachlabs-video-edit` — 视频编辑
