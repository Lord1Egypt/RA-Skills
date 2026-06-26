---
name: douyin-scraper
description: 爬取抖音视频和文案数据。当用户用自然语言请求搜索抖音/抖音视频内容、获取抖音热榜、查找抖音爆款视频时触发。典型触发语包括"搜索一下XX视频"、"帮我找抖音上关于XX的内容"、"抖音上有什么XX"、"抖音热榜"、"抖音热门"等。支持中文关键词搜索和热榜获取。
---

# 抖音爆款爬虫

## 用法

当用户用自然语言请求搜索抖音内容时，提取关键词后调用脚本：

### 搜索视频

```bash
python3 scripts/scraper.py search --keyword "<关键词>" --limit <数量>
```

### 获取热榜

```bash
python3 scripts/scraper.py search --keyword "<分类>" --limit <数量>
# 或
python3 scripts/scraper.py hot --category "<分类>" --limit <数量>
```

### 保存结果

加 `--output <文件名>` 和 `--format json|csv` 保存到文件。

## 自然语言 → 命令映射

| 用户说 | 命令 |
|--------|------|
| 搜索一下海鲜视频 | `python3 scripts/scraper.py search --keyword "海鲜" --limit 10` |
| 帮我找抖音上关于小龙虾的内容 | `python3 scripts/scraper.py search --keyword "小龙虾" --limit 10` |
| 抖音热榜 | `python3 scripts/scraper.py hot --limit 20` |
| 美食热门视频 | `python3 scripts/scraper.py hot --category "美食" --limit 20` |

## 输出格式

每条结果包含：title, description, author, play_count, like_count, comment_count, share_count, url, tags, publish_time。

## 注意事项

- 浏览器不可用时自动降级为模拟数据（会打印提示）
- 遵守平台规则，避免频繁请求
- 仅供学习研究使用
