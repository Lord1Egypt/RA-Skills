---
name: amazon-monitor
description: 亚马逊商品监控技能 - 监控自有产品及竞品数据，支持价格追踪、评论分析、竞品对比和运营建议 | Amazon product monitoring skill - track your products and competitors with price tracking, review analysis, competitor comparison and operational recommendations
version: "1.0.0"
tags:
  - amazon
  - monitor
  - ecommerce
  - scraping
  - competitor-analysis
  - price-tracking
---

# Amazon Monitor | 亚马逊监控技能

## Overview | 技能简介

A professional Amazon operations data collection and analysis skill. Helps sellers monitor key metrics of their own products and competitors, including price, ratings, review counts, and more. Provides data visualization and operational recommendations.

| EN | 这是一个专业的亚马逊运营数据采集和分析技能，帮助卖家监控自有产品和竞品的关键指标，包括价格、评分、评论数等，并提供数据可视化和运营建议。 |
|---|---|
| A professional Amazon operations data collection and analysis skill | 帮助卖家监控自有产品和竞品的关键指标 |
| Price tracking, review analysis | 价格追踪、评论分析 |
| Competitor comparison | 竞品对比 |
| Operational recommendations | 运营建议 |

---

## Prerequisites | 前置要求

### Runtime Environment | 运行环境
- Python 3.8+

### Required Dependencies | 必需安装

| Dependency | Description | EN Description | Install Command |
|------------|-------------|----------------|-----------------|
| playwright | 浏览器自动化 | Browser automation | `pip install playwright && playwright install chromium` |
| matplotlib | 趋势图生成 | Trend chart generation | `pip install matplotlib` |

---

## Installation | 安装步骤

| Step | EN | 说明 |
|------|----|------|
| 1 | Place `amazon-monitor` in OpenClaw skills directory | 将 `amazon-monitor` 目录放到 OpenClaw skills 目录 |
| 2 | Install dependencies | 安装依赖 |
| 3 | Install browser | 安装浏览器 |

```bash
# EN
pip install playwright matplotlib
playwright install chromium

# CN
pip install playwright matplotlib
playwright install chromium
```

---

## Features | 功能列表

### 1. Product Data Collection | 商品数据采集
| Feature | EN | 说明 |
|---------|----|------|
| 数据项 | Data points | 商品标题、价格、星级、评论数 |
| 地区价格 | Regional pricing | 支持设置不同邮编查看各地区价格（美元） |
| 历史记录 | History | 自动保存历史数据 |
| 趋势图 | Trend charts | 生成价格和评论趋势图 |

### 2. Automated Monitoring | 自动监控任务
| Feature | EN | 说明 |
|---------|----|------|
| 定时任务 | Scheduled tasks | 创建定时监控任务（可调整频率：每5/10/15/30/60分钟等） |
| 价格变化 | Price change | 价格上涨或下降时通知 |
| 评论变化 | Review change | 评论增加或减少时通知 |
| 星级变化 | Rating change | 评分波动时通知 |
| 链接失效 | Link invalid | 商品下架或链接失效时通知 |
| 暂停/恢复 | Pause/Resume | 支持暂停、恢复、删除任务 |

### 3. Competitor Analysis | 竞品搜索与分析
| Feature | EN | 说明 |
|---------|----|------|
| 竞品搜索 | Competitor search | 根据品类关键词搜索亚马逊竞品 |
| 详细信息 | Details | 获取Top 3竞品详细信息 |
| 对比分析 | Comparison | 自动对比分析（价格、评分、评论数） |
| 报告生成 | Report | 生成运营建议报告 |

---

## Usage | 使用方法

### Trigger Words | 触发词

| EN | CN |
|----|----|
| amazon monitor | 亚马逊监控 |
| monitor ASIN | 监控ASIN |
| competitor analysis | 竞品分析 |
| price tracking | 价格追踪 |
| search competitors | 搜索竞品 |

---

### Intent Mapping | 用户意图映射

| User Intent (EN) | 用户意图（CN） | Command | 说明 |
|------------------|----------------|---------|------|
| Query product data | 查询商品 | `scrape <ASIN> [邮编]` | 获取商品标题、价格、评分、评论数 |
| Monitor product | 监控商品 | `monitor <ASIN> [邮编] [频率]` | 创建定时监控任务 |
| List monitors | 查看监控列表 | `list` | 显示所有监控任务及状态 |
| Run now | 手动检查 | `run <ASIN>` | 立即执行指定ASIN的监控 |
| Pause monitor | 暂停监控 | `update <ASIN> enabled=false` | 暂停任务 |
| Resume monitor | 恢复监控 | `update <ASIN> enabled=true` | 重新启用任务 |
| Change frequency | 调整频率 | `update <ASIN> frequency=X` | 修改任务检查间隔 |
| Delete monitor | 删除监控 | `delete <ASIN>` | 删除监控任务 |
| Search competitors | 搜索竞品 | `search <关键词> [邮编]` | 搜索同类商品竞品 |
| Competitor analysis | 竞品对比 | `compare <ASIN> [邮编]` | 自有产品 vs 竞品完整分析 |
| Price trend | 价格走势 | `scrape <ASIN>` | 查看当前价格和趋势图 |
| Review changes | 评论变化 | `scrape <ASIN>` | 查看评论数变化 |

---

### Command Reference | 命令格式

#### 1. scrape | 抓取商品数据
```
命令: scrape <ASIN> [邮编]
示例: scrape <YOUR_ASIN> 10001
说明: 抓取指定ASIN的商品数据，默认邮编10001（纽约）

Command: scrape <ASIN> [ZIP]
Example: scrape <YOUR_ASIN> 10001
Desc: Fetch product data for specified ASIN, default ZIP 10001 (New York)
```

#### 2. monitor | 创建监控任务
```
命令: monitor <ASIN> [邮编] [频率分钟]
示例: monitor <YOUR_ASIN> 10001 5
说明: 创建每5分钟监控一次的任务，支持触发条件通知

Command: monitor <ASIN> [ZIP] [frequency_minutes]
Example: monitor <YOUR_ASIN> 10001 5
Desc: Create monitoring task with specified frequency
```

#### 3. list | 列出监控任务
```
命令: list
示例: list
说明: 显示所有已创建的监控任务及状态

Command: list
Example: list
Desc: Show all monitoring tasks and their status
```

#### 4. run | 运行任务
```
命令: run <ASIN>
示例: run <YOUR_ASIN>
说明: 手动运行指定ASIN的监控任务

Command: run <ASIN>
Example: run <YOUR_ASIN>
Desc: Manually run monitoring for specified ASIN
```

#### 5. runall | 运行所有任务
```
命令: runall
示例: runall
说明: 运行所有启用的监控任务

Command: runall
Example: runall
Desc: Run all enabled monitoring tasks
```

#### 6. update | 更新任务配置
```
命令: update <ASIN> <key=value> [key=value] ...
示例: 
  update <YOUR_ASIN> frequency=10
  update <YOUR_ASIN> price_trigger=true review_trigger=true
  update <YOUR_ASIN> enabled=false
说明: 更新任务频率、触发条件或启用状态

Command: update <ASIN> <key=value> [key=value] ...
Example:
  update <YOUR_ASIN> frequency=10
  update <YOUR_ASIN> price_trigger=true review_trigger=true
  update <YOUR_ASIN> enabled=false
Desc: Update task frequency, trigger conditions, or enabled status
```

#### 7. delete | 删除任务
```
命令: delete <ASIN>
示例: delete <YOUR_ASIN>
说明: 删除指定ASIN的监控任务

Command: delete <ASIN>
Example: delete <YOUR_ASIN>
Desc: Delete monitoring task for specified ASIN
```

#### 8. search | 搜索竞品
```
命令: search <关键词> [邮编]
示例: search pool vacuum robot 10001
说明: 搜索品类关键词，返回Top 10竞品列表

Command: search <keyword> [ZIP]
Example: search pool vacuum robot 10001
Desc: Search competitors by keyword, returns Top 10 results
```

#### 9. compare | 竞品对比分析
```
命令: compare <ASIN> [邮编]
示例: compare <YOUR_ASIN> 10001
说明: 获取自有产品数据，搜索竞品，生成对比分析报告

Command: compare <ASIN> [ZIP]
Example: compare <YOUR_ASIN> 10001
Desc: Get your product data, search competitors, generate comparison report
```

---

## Parameters | 参数说明

### ASIN
| EN | CN |
|----|----|
| Amazon Standard Identification Number | 亚马逊商品标准识别码 |
| Format: 10 characters, e.g. B0XXXXXXX | 格式：10位字符，如 B0XXXXXXX |
| Get from product URL after `/dp/` | 获取方式：商品详情页URL中 `/dp/` 后面的代码 |

### ZIP Code | 邮编
| EN | CN |
|----|----|
| Sets delivery location for regional pricing | 用于设置配送地址，查看不同地区价格 |

| ZIP | City | EN City |
|-----|------|---------|
| 10001 | 纽约 | New York |
| 90210 | 洛杉矶 | Los Angeles |
| 60601 | 芝加哥 | Chicago |
| 98101 | 西雅图 | Seattle |

### Frequency | 频率
| EN | CN |
|----|----|
| Monitoring interval in minutes | 监控任务执行间隔，单位：分钟 |
| Recommended: 5-15 min normal, 1-5 min during promotions | 建议：日常监控设为5-15分钟，大促期间设为1-5分钟 |

### Triggers | 触发条件

| Trigger | EN | CN | Default |
|---------|----|-------|---------|
| price_change | 价格变化时通知 | Notify on price change | true |
| review_change | 评论数变化时通知 | Notify on review count change | true |
| rating_change | 星级变化时通知 | Notify on rating change | false |
| link_invalid | 链接失效时通知 | Notify when link becomes invalid | true |

---

## Configuration | 配置说明

### Data Storage | 数据存储

| File | EN | CN |
|------|----|-----|
| `<ASIN>_history.json` | Historical data records | 历史数据记录 |
| `<ASIN>_trend_chart.png` | Trend chart (requires ≥2 data points) | 趋势图（需≥2条数据） |
| `competitor_analysis_<ASIN>.txt` | Competitor analysis report | 竞品分析报告 |
| `amazon_monitor_tasks.json` | Monitoring task configuration | 监控任务配置 |

Data files are saved in the working directory by default. Modify `save_history()` function to change storage path.

---

## Examples | 使用示例

### Example 1 | 示例1
```
用户: 帮我抓取 <YOUR_ASIN> 的数据
助手: (执行 scrape <YOUR_ASIN> 10001)

User: Fetch data for <YOUR_ASIN>
Assistant: (execute scrape <YOUR_ASIN> 10001)
```

### Example 2 | 示例2
```
用户: 创建监控任务，每10分钟检查一次价格变化
助手: (执行 monitor <YOUR_ASIN> 10001 10)

User: Create monitoring task, check price every 10 minutes
Assistant: (execute monitor <YOUR_ASIN> 10001 10)
```

### Example 3 | 示例3
```
用户: 对比分析 <YOUR_ASIN> 和竞品
助手: (执行 compare <YOUR_ASIN> 10001)

User: Compare <YOUR_ASIN> with competitors
Assistant: (execute compare <YOUR_ASIN> 10001)
```

### Example 4 | 示例4
```
用户: 把 <YOUR_ASIN> 的监控频率改为每30分钟
助手: (执行 update <YOUR_ASIN> frequency=30)

User: Change <YOUR_ASIN> monitoring frequency to every 30 minutes
Assistant: (execute update <YOUR_ASIN> frequency=30)
```

### Example 5 | 示例5
```
用户: 关闭评论变化通知，只监控价格和链接
助手: (执行 update <YOUR_ASIN> price_trigger=true review_trigger=false link_invalid=true)

User: Turn off review change notifications, only monitor price and link
Assistant: (execute update <YOUR_ASIN> price_trigger=true review_trigger=false link_invalid=true)
```

---

## Operational Recommendations | 运营建议解读

### Price Analysis | 价格分析

| Level | EN | CN | Recommendation |
|-------|----|----|----------------|
| High | Price 20%+ above average | 价格偏高（比竞品平均高20%+） | Consider lowering price or highlighting differentiators |
| Low | Price 20%+ below average | 价格偏低（比竞品平均低20%-） | Consider raising price to improve profit margin |
| Normal | Price is reasonable | 价格合理 | Maintain current strategy |

### Review Count Analysis | 评论数分析

| Level | EN | CN | Recommendation |
|-------|----|----|----------------|
| Weak | Less than 30% of top competitor | 评论基础弱（不足竞品最高30%） | Accelerate review acquisition, set up reward program |
| Medium | 30%-50% of top competitor | 评论中等（30%-50%） | Maintain steady growth |
| Good | Above 50% of top competitor | 评论良好（50%+） | Continue maintaining, protect ratings |

### Rating Analysis | 评分分析

| Level | EN | CN | Recommendation |
|-------|----|----|----------------|
| Low | 0.3+ stars below competitor average | 评分偏低（低于竞品平均0.3星+） | Investigate product issues, improve quality |
| Excellent | 0.2+ stars above competitor average | 评分优秀（高于竞品平均0.2星+） | Leverage high rating in marketing |
| Normal | Rating is normal | 评分正常 | Continue maintenance |

---

## Notes | 注意事项

| # | EN | CN |
|---|----|----|
| 1 | First run requires 2+ data points for trend chart | 首次运行需要2次以上数据才能生成趋势图 |
| 2 | Amazon may restrict access - retry on timeout | 亚马逊可能限制访问，遇到超时可重试 |
| 3 | CAPTCHA may trigger on frequent access | 频繁访问可能触发验证码，稍后再试 |
| 4 | Set ZIP code to display USD prices | 设置邮编后才能显示美元价格 |
| 5 | Backup important historical data regularly | 建议定期备份重要数据 |
| 6 | Control request frequency to avoid anti-bot detection | 建议合理控制请求频率，避免触发亚马逊防爬机制 |

---

## Disclaimer | 免责声明

| EN | CN |
|----|----|
| This skill is for learning and research purposes only. Please comply with Amazon's Terms of Service and use crawlers responsibly. Users bear all risks associated with misuse. | 本技能仅供学习和研究使用。请遵守亚马逊的服务条款，合理使用爬虫功能。对于因滥用导致的账号风险，由使用者自行承担。 |

---

## FAQ | 常见问题

| Problem | EN | Solution | 解决方案 |
|---------|----|----------|----------|
| playwright not found | 报错 `playwright not found` | Run installation commands | 执行 `pip install playwright && playwright install chromium` |
| Price shows CNY | 价格显示为 CNY | Pass US ZIP code | 确保传入美国邮编（如 10001） |
| Trend chart fails | 趋势图生成失败 | Check if ≥2 data points exist | 检查历史数据是否≥2条 |
| Scheduled task not running | 任务定时不执行 | Check if cron task is created correctly | 检查 cron 任务是否正确创建 |
| Page load timeout | 页面加载超时 | Amazon may be rate limiting | 亚马逊可能限流，稍后再试或降低请求频率 |

---

## Troubleshooting | 技术支持

| EN | CN |
|----|----|
| Check if ASIN is correct | ASIN是否正确 |
| Check if product link is valid | 商品链接是否有效 |
| Check network connection | 网络连接是否正常 |
| Check if dependencies are installed | 依赖是否完整安装 |
| Amazon page structure may have changed | 亚马逊页面结构是否变化（可能需要更新选择器） |

---

## Changelog | 更新日志

### v1.0.0 (2026-04-18)
| EN | CN |
|----|----|
| Initial release | 初始版本发布 |
| Product data collection | 支持商品数据采集 |
| Competitor search & analysis | 支持竞品搜索与分析 |
| Scheduled monitoring tasks | 支持定时监控任务 |
| Price trend chart generation | 支持价格趋势图生成 |
