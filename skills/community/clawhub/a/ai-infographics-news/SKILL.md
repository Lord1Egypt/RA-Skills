---
name: ai-infographic-news
description: Search for the latest and most trending AI products, tools, and news (strongly prioritizing time-sensitive, recent content — especially OpenClaw/MaxClaw-related updates), then generate a vivid, visually rich infographic image using image_synthesize. Trigger on: "生成AI资讯信息图", "AI热点信息图", "帮我做AI新闻图", "最新AI产品信息图", "AI news infographic", "make an AI hot products visual", "AI weekly digest image", or any request combining AI news research with visual/infographic output.
---

# AI Infographic News

搜索近期最热门AI产品和新闻，重点突出 OpenClaw/MaxClaw 相关动态，生成高质量信息图（infographic）。

## 第一步：获取当前日期

调用 `session_status` 获取今天的日期（年/月），用于构造带时效性的搜索词。

## 第二步：并行搜索（batch_web_search）

一次调用，同时发起 **5 条搜索**，全部设置 `data_range: "m"`（近一个月）：

| # | 查询关键词模板（填入当前年月） |
|---|---|
| 1 | `OpenClaw MaxClaw AI assistant new features {year}` |
| 2 | `最新 AI 产品发布 热门 {year年month月}` |
| 3 | `hot AI tools product launch {month} {year}` |
| 4 | `AI startup funding round {month} {year}` |
| 5 | `new AI model release agent app {month} {year}` |

**优先级规则（搜索结果筛选顺序）：**
1. 🦞 OpenClaw / MaxClaw 任何更新、功能、发布 → **必须置顶**
2. 🚀 新AI产品/工具发布（30天内）
3. 💰 AI融资/并购（金额大或影响力强）
4. 🤖 新AI模型/能力（GPT、Gemini、开源模型等）
5. 📈 行业趋势/里程碑事件

若 OpenClaw 相关结果稀少，追加专项搜索：
```
"openclaw" OR "maxclaw" site:github.com OR site:producthunt.com OR site:x.com
```

## 第三步：整理内容（6–9条亮点）

每条提取：
- **标题**：≤ 8 个字/词，简洁有力
- **摘要**：≤ 20 字，一句话说清楚
- **日期**：有则填，无则省略
- **分类**：产品 / 模型 / 融资 / 趋势 / OpenClaw

## 第四步：生成信息图（image_synthesize）

用提取的内容构造生图 Prompt，调用 `image_synthesize`：

```
A stunning, high-resolution AI news infographic poster for [Month Year].

LAYOUT: Dark tech theme. Deep navy-to-black gradient background. 
Title at top: "🔥 AI HOT THIS WEEK · [Month] [Year]" in large bold white text with cyan glow.

NEWS CARDS (2-column grid, [N] cards total):
- Card 1 [GOLD BORDER — OpenClaw highlight if applicable]: 
  "🦞 [Title]" / "[Summary]" / "[Date]"
- Card 2: "🚀 [Title]" / "[Summary]"
- Card 3: "🤖 [Title]" / "[Summary]"
... (continue for each item)

DESIGN DETAILS:
- Card backgrounds: dark charcoal (#1a1f2e) with colored left accent border
- Accent colors: cyan (#00f5ff), electric blue (#0066ff), purple (#8b5cf6), hot pink (#ff0080)
- Typography: bold sans-serif, white headers, light gray body text
- Add subtle glowing data visualization elements (charts, nodes, waveforms) in background
- Bottom strip: "Powered by OpenClaw AI 🦞" in small text
- Overall aesthetic: professional tech dashboard meets editorial design

High fidelity, crisp readable text, 2K resolution.
```

**生图参数：**
- `aspect_ratio`: `"9:16"`（竖版，适合手机/社交媒体）或 `"16:9"`（横版）
- `resolution`: `"2K"`
- `output_file`: `/workspace/ai-infographic-YYYYMMDD.png`

如需其他视觉风格，参考 `references/infographic-styles.md`。

## 第五步：输出交付

生图完成后：
1. 列出本次收录的 **Top 5 亮点**（简短 bullet list）
2. 提供图片路径，如需分享则上传 CDN：`upload_to_cdn`
3. 询问是否需要调整风格或内容

## 质量检查

- [ ] 有 OpenClaw/MaxClaw 相关条目（若有新闻的话）
- [ ] 所有条目均为近 30 天内
- [ ] 生图 Prompt 包含足够细节保证文字可读
- [ ] 分辨率 ≥ 2K
- [ ] 图片已保存至 /workspace/
