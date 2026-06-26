# 抖音爆款爬虫 Skill

使用浏览器自动化或脚本爬取抖音视频和文案数据。

## 快速开始

### 方式一：浏览器自动化（推荐）

使用 OpenClaw browser tool，复用用户登录态：

```
browser open → https://www.douyin.com/search/海鲜?type=video
browser snapshot → 提取视频数据
```

> 需使用 `profile="user"` 以避免验证码拦截。

### 方式二：脚本命令行

```bash
# Mock 模式（不启动浏览器，返回示例数据）
python3 scripts/scraper.py search --keyword "海鲜" --limit 10 --mock

# 真实爬取（需 Playwright + 浏览器）
python3 scripts/scraper.py search --keyword "海鲜" --limit 10

# 热榜
python3 scripts/scraper.py hot --limit 20 --mock

# Node.js 版本
node scripts/douyin_scraper.js search "海鲜" 10
```

## 安装

```bash
pip install playwright
playwright install chromium
```

## 自然语言支持

本 skill 支持自然语言请求，例如：
- "搜索一下海鲜视频" → 搜索 keyword="海鲜"
- "看看抖音热榜有什么" → 获取热榜
- "找一些海鲜售卖相关的视频文案" → 搜索 keyword="海鲜售卖"

详见 `SKILL.md`。

## 输出格式

JSON（默认）或 CSV，通过 `--format` 和 `--output` 参数指定。

## 注意事项

- 未登录访问抖音搜索/热榜大概率触发验证码
- 脚本无浏览器时自动降级为 mock 数据
- 仅供学习研究，遵守平台规则
