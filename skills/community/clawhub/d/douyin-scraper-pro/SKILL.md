---
name: douyin-scraper
description: 爬取抖音爆款视频和文案数据，支持自然语言搜索请求。使用 Playwright 自动化浏览器操作，支持搜索关键词、获取热榜、提取视频信息和文案。
version: 2.0.0
---

# 抖音爆款爬虫 Skill

## Agent 指南：自然语言解析

当用户用自然语言发请求时，按以下规则提取参数并执行对应命令：

### 请求类型识别

| 用户说法示例 | 类型 | 命令 |
|---|---|---|
| 搜索一下海鲜视频 / 找一些海鲜售卖的视频 / 帮我搜海鲜 | search | `search --keyword "<关键词>"` |
| 看看抖音热榜 / 热榜有什么 / 抖音热搜 | hot | `hot` |
| 分析这个视频链接 https://v.douyin.com/xxx | analyze | `analyze --url "<url>"` |

### 关键词提取规则

1. 去掉无意义动词/助词：「搜索一下」「帮我找」「看看」「有没有」
2. 提取核心搜索词：「搜索一下**海鲜**视频」→ keyword=`海鲜`
3. 如果用户指定数量则用之，否则默认 `--limit 10`
4. 如果用户指定输出文件则用之，否则默认 stdout

### 执行方式

**优先使用 Python 脚本**（更稳定的数据提取）：

```bash
cd {{SKILL_DIR}} && bash scripts/run.sh search --keyword "海鲜" --limit 10
```

如果 Python 环境不可用，回退到 Node.js：

```bash
cd {{SKILL_DIR}} && node scripts/douyin_scraper.js search "海鲜" 10
```

### 输出解读

脚本输出 JSON 数组，每个元素包含：
- `title` — 视频标题
- `description` — 视频描述/文案
- `author` — 作者昵称
- `play_count` / `like_count` / `comment_count` / `share_count` — 互动数据
- `url` — 视频链接
- `tags` — 标签列表
- `publish_time` — 发布时间

Agent 应将结果整理为用户友好的格式呈现，而非直接 dump JSON。

## 完整命令参考

### 搜索

```bash
# Python
bash scripts/run.sh search --keyword "海鲜" --limit 10
bash scripts/run.sh search --keyword "海鲜售卖" --limit 20 --output result.json

# Node.js
node scripts/douyin_scraper.js search "海鲜" 10
```

### 热榜

```bash
# Python
bash scripts/run.sh hot --limit 20
bash scripts/run.sh hot --category "美食" --limit 20

# Node.js
node scripts/douyin_scraper.js hot 20
```

### 分析视频链接

```bash
bash scripts/run.sh analyze --url "https://v.douyin.com/xxxxx/"
```

## 安装

首次使用前需安装依赖：

```bash
cd {{SKILL_DIR}}
pip install playwright
playwright install chromium
```

或使用 Node.js：

```bash
cd {{SKILL_DIR}}
npm install
npx playwright install chromium
```

## 注意事项

- 遵守抖音平台规则，合理使用，避免频繁请求
- 请求之间有默认 2 秒延时
- 数据仅供学习研究使用
- 不要登录账号，避免风控
- 注意 IP 限制风险
