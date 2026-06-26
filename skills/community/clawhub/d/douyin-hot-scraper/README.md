# 抖音数据爬虫 Skill

获取抖音热榜和搜索数据，支持自然语言调用。

## 🚀 快速开始

```bash
# 搜索关键词
python3 scripts/scraper.py search --keyword "海鲜" --limit 10

# 获取热榜
python3 scripts/scraper.py hot --limit 20

# 搜索并保存结果
python3 scripts/scraper.py search --keyword "海鲜" --limit 20 --output seafood.json
```

## 🗣️ 自然语言调用

| 用户说 | 命令 |
|--------|------|
| 搜索一下海鲜视频 | `python3 scripts/scraper.py search --keyword "海鲜"` |
| 看看抖音热榜 | `python3 scripts/scraper.py hot` |
| 找一些关于小龙虾的视频 | `python3 scripts/scraper.py search --keyword "小龙虾"` |

## 📦 依赖

```bash
pip install playwright && playwright install chromium
```

> 热榜功能无需 Playwright，纯 API 调用。搜索功能在 Playwright 不可用时会自动回退到热榜 API。

## 📊 输出格式

支持 JSON 和 CSV，通过 `--format json|csv` 指定。

## ⚠️ 注意事项

- 抖音网页搜索需登录，未登录时自动回退到热榜数据
- 合理使用，避免频繁请求
- 仅供学习和研究
