# 🔍 Find API Skill

## 定位

这是一个**持续完善的通用数据源发现 Skill**。

**核心使命**：帮助 Agent 找到可靠的数据 API，避免低效的网页爬取。

## 设计原则

1. **API First, Scraping Last**：始终优先使用 API
2. **持续扩展**：不断添加新的数据领域
3. **实用性优先**：优先推荐免费、免认证、易用的 API
4. **Agent友好**：结构清晰，易于 Agent 理解和执行

## 当前覆盖领域

| 领域 | 状态 | 主要 API |
|------|------|---------|
| ✅ 股票/金融数据 | 完成 | AKShare, Tushare, yfinance |
| ✅ 天气数据 | 完成 | OpenWeatherMap, 和风天气 |
| ✅ 新闻媒体 | 完成 | NewsAPI, GNews |
| ✅ 地图定位 | 完成 | Nominatim, 高德地图 |
| ✅ 电商商品 | 基础完成 | 淘宝/京东开放平台 |
| 🔜 社交媒体 | 计划中 | Twitter, Weibo, Reddit |
| 🔜 翻译服务 | 计划中 | DeepL, Google Translate |
| 🔜 图像视频 | 计划中 | Unsplash, Pexels |
| 🔜 科研数据 | 计划中 | arXiv, PubMed |
| 🔜 政府公开数据 | 计划中 | 各国政府开放数据 |

## 如何贡献

如果你知道某个领域的可靠数据 API，欢迎贡献：

1. 提供 API 名称、官方链接
2. 说明数据覆盖范围
3. 说明成本和认证方式
4. 提供简单的使用示例

## 文件结构

```
find-api/
├── SKILL.md      # Skill 主文件
└── README.md     # 本说明文件
```

## 上传到 ClawHub

1. 访问 ClawHub
2. 创建新 Skill
3. 上传 `SKILL.md`
4. 填写信息：
   - Name: `find-api`
   - Emoji: `🔍`

## 版本历史

- v1.0.0 (2026-03-13): 初始版本
  - 覆盖股票/金融、天气、新闻、地图、电商五大领域
  - 提供详细的 API 对比和使用示例
  - 建立"API First, Scraping Last"核心原则
