---
name: news-scraper
description: 从AI新闻网站爬取最新资讯，支持自动生成新闻总结。用于AI新闻采集、内容聚合、舆情监控。
---

# 新闻爬取 Skill

## 概述

本技能用于从AI新闻网站爬取最新资讯，并生成格式化新闻简报。支持多网站扩展，具备去重功能。

## 目录结构

```
news-scraper/
├── SKILL.md              # 主技能说明
├── config.py              # 配置文件
├── scrapers/
│   ├── __init__.py
│   ├── base.py            # 爬虫基类
│   └── aibase.py         # AI Base网站爬虫
├── scripts/
│   └── crawl.py           # 主爬取入口
└── templates/
    └── news_template.md   # 新闻模板
```

## 快速开始

### 1. 安装依赖

```bash
pip install requests beautifulsoup4 openpyxl
```

### 2. 运行爬虫

```bash
# 爬取AI Base新闻（默认20条）
python scripts/crawl.py --site aibase

# 限制爬取数量
python scripts/crawl.py --site aibase --limit 10
```

## 编程调用

```python
import sys
sys.path.insert(0, "~/.qoder/skills/news-scraper")
from scripts.crawl import crawl_and_return_json

# 爬取新闻，返回JSON数据
result = crawl_and_return_json(site="aibase", limit=20)
news_list = result["news"]  # 获取新闻列表
```

## 配置说明

编辑 `config.py`：
- `MAX_NEWS_PER_CRAWL`: 每次爬取最大数量（默认20）
- `NEWS_JSON_FILENAME`: JSON文件名（默认news_latest.json）

保存目录由AI根据实际环境自行决定，默认保存在当前目录下的News文件夹。

## 输出文件

| 文件 | 说明 |
|------|------|
| `news_latest.json` | JSON格式，主数据文件 |

**JSON结构**：
```json
{
  "crawl_time": "2026-03-17T10:33:27",
  "total_count": 20,
  "news": [
    {
      "title": "新闻标题",
      "url": "https://...",
      "publish_time": "2026-03-17 02:00:00",
      "source": "AIBase",
      "keywords": [],
      "summary": "一句话总结",
      "content": "正文内容"
    }
  ]
}
```

## 爬取逻辑

### 执行流程

1. **检查目录** - 自动检测并创建保存目录
2. **加载配置** - 读取config.py中的网站配置
3. **获取新闻列表** - 每个网站最多获取指定数量新闻
4. **去重检查** - 与已有新闻比对URL，剔除重复
5. **提取正文** - 访问每条新闻详情页提取中文内容
6. **保存文件** - 更新JSON文件，生成Markdown文件

### 去重逻辑

- 基于 `url` 字段进行比对
- 检查保存目录下所有已有markdown文件的URL
- 发现重复URL则跳过该条新闻

### 爬取顺序

从新到旧（按发布时间倒序）

## 添加新网站

1. 在 `scrapers/` 目录下创建新的爬虫文件
2. 继承 `BaseScraper` 类
3. 实现必要方法
4. 在 `config.py` 的 `SITES` 字典中注册

示例见 [scrapers/aibase.py](scrapers/aibase.py)

## 命令行选项

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--site` | 网站标识符 | aibase |
| `--limit` | 爬取数量 | 20 |
| `--force` | 强制覆盖已存在文件 | false |

## 部署说明

本skill会自动选择合适的目录保存文件，AI会根据当前环境自行决定存储位置。
