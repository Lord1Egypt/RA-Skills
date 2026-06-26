---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: 64389f5483ccf2c5e859bb3c2008f5c8
    PropagateID: 64389f5483ccf2c5e859bb3c2008f5c8
    ReservedCode1: 30450220751771b398feb11d141c22a5f8d21a49f98cc2859de61cde9012a1e226caa5e0022100f9dacb20758ac8edf6a04b3aa56736260422f5f0f936656b7e6f6256f50d8390
    ReservedCode2: 3044022048c1054bd2bb4014e8f25b79f78a360beae6f1df3f8b343c6a17f015594d63680220565e641fc16b1fdb28b7711576d3287854036481cb986939e162b49265baf440
description: 生成AI新闻资讯的Infographics图片。使用场景：(1) 用户要求生成AI热门产品或新闻的图片 (2) 需要近期AI动态的可视化内容 (3) 制作OpenClaw相关的AI资讯图片 (4) 创建社交媒体分享的AI新闻卡片。功能：搜索近期热门AI产品和新闻，筛选与OpenClaw相关的内容，生成新闻杂志风格的Infographics图片。
name: ai-news-infographics
---

# AI新闻资讯 Infographics 生成

## 触发条件

当用户要求以下内容时使用此skill：
- 生成AI新闻/产品的图片
- 制作AI资讯infographics
- 创建AI动态分享卡片
- 制作OpenClaw相关的资讯图片

## 工作流程

### 1. 搜索热门AI新闻

使用 `batch_web_search` 搜索近期AI热门新闻：

```json
[
  {"cursor": 1, "data_range": "m", "num_results": 10, "query": "AI news 2025 2026 popular products"},
  {"cursor": 1, "data_range": "m", "num_results": 10, "query": "OpenClaw AI agent latest news"},
  {"cursor": 1, "data_range": "m", "num_results": 10, "query": "AI agent automation tools 2025"}
]
```

### 2. 筛选与OpenClaw相关的内容

优先保留以下类型的新闻：
- OpenClaw/MaxClaw相关动态
- AI Agent/自动化工具
- MCP (Model Context Protocol) 相关
- 生产力AI工具
- 开源AI项目

### 3. 生成Infographics图片

使用 `image_synthesize` 生成新闻杂志风格的图片。

**Prompt模板（英文）:**

```
Modern AI news infographic magazine style, professional journalism layout. 
Top section: [新闻标题]
Middle section: [关键特性/要点用图标和短文本展示]
Bottom section: [相关信息/链接]

Visual style:
- Clean, editorial magazine design
- Bold typography headlines
- Minimalist data visualization icons
- White/light gray background with accent colors
- Professional, news-worthy aesthetic
- High contrast text for readability

Include these elements:
- Magazine-style headline layout
- Feature bullet points with icons
- Clean section dividers
- Subtle gradient accents
- Modern sans-serif typography feel
```

**图片规格：**
- 分辨率: 2K (2560x1440) 或 4K (3840x2160)
- 宽高比: 16:9 (横版) 或 4:3
- 风格: 新闻杂志、简洁专业

### 4. 输出

将生成的图片保存到 workspace，并通过 CDN 上传获取可分享的链接。

## 注意事项

- 搜索关键词加入当前年月确保时效性
- 优先选择有具体产品名、功能描述的新闻
- 图片需要清晰可读，避免文字过多
- 如果搜索结果少于5条，扩大搜索范围
