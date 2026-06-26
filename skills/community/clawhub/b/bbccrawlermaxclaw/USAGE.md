---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 3044022063221c4f22880cf778cae6f33e8644d6043011b526a53835d5e66d3141bf794f0220113c366c72ccb903426aad7e3b9fdb110a501a1a7d8fe2c3d7445a226794a99f
    ReservedCode2: 304502206fa78203de3a2bca54ee6c358c51462276b026e8347ab157e819ed3a4877a02f022100ca53bf5720bab1dbeab2513691e2313ad7fd0d65d36bb280f8ea1059f964cdce
---

# Universal Web Crawler - 完整使用指南

## 概述

通用网站爬虫，支持多种爬取方式和网站类型。

## 文件结构

```
/workspace/skills/bbc_crawler/
├── SKILL.md                    # Skill说明
├── bbc_crawler.py             # BBC专用爬虫
├── universal_crawler_v2.py    # 通用爬虫(推荐)
├── openclaw_crawler.py        # OpenClaw集成版
├── dynamic_crawler.py         # 动态网站说明
└── README.md                 # 本文件
```

## 快速开始

### 1. 安装依赖

```bash
# 基础依赖
pip install requests beautifulsoup4 lxml

# 可选依赖
pip install crawl4ai  # 异步爬虫
pip install playwright  # JS渲染
```

### 2. 基本使用

```bash
# BBC新闻
python universal_crawler_v2.py -u https://www.bbc.com/news --max-pages 20

# 新浪新闻
python universal_crawler_v2.py -u https://news.sina.com.cn --domains sina.com.cn

# 指定多个域名
python universal_crawler_v2.py -u https://www.example.com --domains "example.com,blog.example.com"
```

### 3. 使用预设

```bash
python openclaw_crawler.py --preset bbc --count 20
python openclaw_crawler.py --preset sina --count 30
```

## 命令行参数

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--url` | `-u` | 起始URL | 必填 |
| `--output` | `-o` | 输出目录 | `./output` |
| `--max-pages` | `-m` | 最大页面数 | 50 |
| `--depth` | `-d` | 爬取深度 | 5 |
| `--delay` | - | 请求延迟(秒) | 3 |
| `--method` | - | 爬取方式 | auto |
| `--domains` | - | 允许域名 | 从URL提取 |

## 方法选择

### auto (自动)

自动选择可用方法: crawl4ai > requests

```bash
python crawler.py -u URL --method auto
```

### requests

使用requests库，适合静态网站

```bash
python crawler.py -u URL --method requests
```

### crawl4ai

使用crawl4ai，适合动态网站

```bash
pip install crawl4ai
python crawler.py -u URL --method crawl4ai
```

### openclaw

使用OpenClaw工具(需要OpenClaw环境)

```bash
# 在OpenClaw中使用
from openclaw_crawler import quick_crawl
quick_crawl("https://www.bbc.com/news")
```

## 使用示例

### 示例1: 爬取BBC新闻

```bash
python universal_crawler_v2.py \
  -u https://www.bbc.com/news \
  -o /workspace/data/bbc \
  -m 20 \
  -d 3 \
  --delay 2
```

### 示例2: 爬取新浪新闻

```bash
python universal_crawler_v2.py \
  -u https://news.sina.com.cn \
  -o /workspace/data/sina \
  -m 30 \
  --domains sina.com.cn
```

### 示例3: 使用预设

```bash
python openclaw_crawler.py --preset bbc -n 50
python openclaw_crawler.py --preset sina -n 30
```

### 示例4: Python代码调用

```python
from universal_crawler_v2 import UniversalCrawler, CrawlConfig

config = CrawlConfig(
    start_url="https://www.bbc.com/news",
    output_dir="/workspace/data/bbc",
    max_pages=20,
    max_depth=3,
    delay=2.0,
    allowed_domains=["bbc.com", "bbc.co.uk"]
)

crawler = UniversalCrawler(config)
result = crawler.run()

print(f"成功: {result.success}, 失败: {result.failed}")
```

## 输出格式

### Markdown文件

```markdown
---
title: "Article Title"
publish_time: 2026-03-09T12:00:00
author: Author Name
category: news
url: https://example.com/article
crawl_time: 2026-03-09T14:00:00
---

# Article Title

正文内容...

## 图片

![图片1](https://example.com/image1.jpg)
![图片2](https://example.com/image2.jpg)
```

### 失败记录

文件: `failed_urls.txt`

```
2026-03-09T12:00:00	https://example.com/page1	403 Forbidden
2026-03-09T12:00:05	https://example.com/page2	404 Not Found
```

## 预设站点

| 预设 | 网站 | URL |
|------|------|-----|
| bbc | BBC News | https://www.bbc.com/news |
| sina | 新浪新闻 | https://news.sina.com.cn |
| cnn | CNN | https://www.cnn.com |
| reuters | Reuters | https://www.reuters.com |
| nytimes | NYTimes | https://www.nytimes.com |

## 注意事项

1. **遵守爬虫礼仪**: 设置合理延迟，不要高频请求
2. **遵守网站规则**: 尊重robots.txt
3. **版权问题**: 爬取内容仅供学习使用
4. **网络限制**: 部分网站需要代理/VPN

## 故障排除

### Q: 爬取失败

A: 
- 检查网络连接
- 增加延迟 `--delay 5`
- 使用代理

### Q: 内容提取不完整

A:
- 网站可能使用JavaScript渲染
- 尝试使用 `--method crawl4ai`

### Q: 被封IP

A:
- 使用代理
- 降低请求频率
- 避开高峰时段

## 版本历史

- v2.0: 集成多种爬取方式
- v1.0: 基础版本
