# Douyin Scraper

> 搜索抖音视频，用自然语言就行。

## 功能

- 🔍 自然语言搜索抖音视频
- 🍪 持久化登录状态，只需登录一次
- 💡 未登录时提供关键词建议作为 fallback

## 安装

```bash
pip install playwright
playwright install chromium
```

## 使用

### 搜索视频

```bash
python3 scripts/douyin_search.py "海鲜视频" --count 10
```

### JSON 输出

```bash
python3 scripts/douyin_search.py "海鲜视频" --json
```

### 首次登录

```bash
python3 scripts/douyin_search.py --login
```

扫码登录后，浏览器状态保存在 `.browser-profile/`，后续搜索无需重复登录。

## 自然语言示例

作为 OpenClaw skill 使用时，直接用自然语言即可：

- "搜索一下海鲜视频"
- "帮我找抖音上的猫咪视频"
- "抖音搜美食教程"
- "douyin search funny cats"

Agent 会自动提取关键词并调用搜索脚本。