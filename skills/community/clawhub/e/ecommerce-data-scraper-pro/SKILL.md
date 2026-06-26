---
name: data-scraper
description: 智能数据抓取工具 - 从网页/API 提取结构化数据，支持批量处理
author: AI Company
version: 0.1.0
metadata: {"emoji": "🕷️", "category": "data"}
---

# Data Scraper - 智能数据抓取工具

从网页、API 自动提取结构化数据，支持批量处理和多种输出格式。

## 功能特性

- 🕷️ **网页数据抓取** - 自动识别并提取目标数据
- 📊 **结构化输出** - JSON、CSV、Excel 格式
- 🔄 **批量处理** - 支持多页面/多 URL 批量抓取
- 🛡️ **反爬规避** - 智能请求频率控制
- 🔌 **API 集成** - 支持 REST/GraphQL API
- 📝 **数据清洗** - 自动去重、格式化

## 使用方法

### 基础用法

```bash
# 抓取单个网页
uv run scripts/data-scraper.py scrape --url "https://example.com/products" --selector ".product"

# 抓取多个页面
uv run scripts/data-scraper.py scrape --urls-file urls.txt --output data.json

# 从 API 获取数据
uv run scripts/data-scraper.py api --endpoint "https://api.example.com/data" --auth "Bearer TOKEN"
```

### 高级选项

```bash
# 指定输出格式
uv run scripts/data-scraper.py scrape --url "https://example.com" --format csv --output products.csv

# 设置请求延迟（避免被封）
uv run scripts/data-scraper.py scrape --url "https://example.com" --delay 2

# 使用代理
uv run scripts/data-scraper.py scrape --url "https://example.com" --proxy "http://proxy:port"

# 定时抓取
uv run scripts/data-scraper.py scrape --url "https://example.com" --schedule "0 */6 * * *"
```

## 支持的数据类型

| 类型 | 描述 | 示例 |
|------|------|------|
| `product` | 电商产品 | 价格、名称、评分、库存 |
| `article` | 新闻/博客 | 标题、作者、日期、内容 |
| `job` | 招聘信息 | 职位、公司、薪资、要求 |
| `real_estate` | 房产信息 | 价格、面积、位置、户型 |
| `social` | 社交媒体 | 帖子、评论、点赞数 |
| `custom` | 自定义 | 通过 CSS/XPath 选择器定义 |

## 输出格式

### JSON（默认）
```json
{
  "url": "https://example.com",
  "scrapedAt": "2026-02-28T01:13:00Z",
  "data": [
    {
      "title": "产品标题",
      "price": "$99.99",
      "rating": 4.5
    }
  ]
}
```

### CSV
```csv
title,price,rating,url
产品标题,$99.99,4.5,https://...
```

### Excel
- 多工作表支持
- 自动格式化
- 数据透视表

## 定价建议

| 版本 | 功能 | 价格 |
|------|------|------|
| 基础版 | 单次抓取，100 页/月 | $49 |
| 专业版 | 批量抓取，1000 页/月，定时任务 | $149 |
| 企业版 | 无限抓取，API 访问，定制支持 | $499 |

## 示例

### 电商产品价格监控

**输入：**
```bash
uv run scripts/data-scraper.py scrape \
  --url "https://amazon.com/s?k=wireless+headphones" \
  --type product \
  --fields "title,price,rating,reviews" \
  --output headphones.json
```

**输出：**
```json
{
  "scrapedAt": "2026-02-28T01:13:00Z",
  "count": 50,
  "data": [
    {
      "title": "Sony WH-1000XM5",
      "price": "$349.99",
      "rating": 4.7,
      "reviews": 12453
    }
  ]
}
```

### 招聘信息抓取

**输入：**
```bash
uv run scripts/data-scraper.py scrape \
  --url "https://linkedin.com/jobs/search?keywords=python+developer" \
  --type job \
  --fields "title,company,location,salary" \
  --output jobs.csv
```

## 技术实现

- 使用 Playwright/BeautifulSoup 进行网页解析
- 支持 JavaScript 渲染页面
- 智能重试和错误处理
- 可集成到 OpenClaw 工作流

## 注意事项

⚠️ **合法合规使用**
- 遵守目标网站 robots.txt
- 不要过度请求导致服务器压力
- 尊重数据版权和隐私
- 仅抓取公开数据

## 更新日志

### v0.1.0 (2026-02-28)
- 初始版本发布
- 支持基础网页抓取
- 支持 JSON/CSV 输出
- 支持批量处理

## 待开发功能

- [ ] 图形化配置界面
- [ ] 数据可视化
- [ ] 自动字段识别
- [ ] 云存储集成
- [ ] 实时监控告警

---

**开发者：** VIC ai-company  
**许可：** MIT  
**支持：** 联系 main agent
