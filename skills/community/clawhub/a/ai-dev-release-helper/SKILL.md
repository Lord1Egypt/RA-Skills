---
name: ai-dev-release-helper
description: |
  AI开发者发布助手 — 自动化 GitHub 项目发布全流程。
  采集竞品信息 → AI生成项目封面图 → 一键发布公众号深度分析文。
  当用户需要"发布开源项目"、"写发布公告"、"做产品介绍"、"生成项目封面"时激活。
version: 1.0.0
author: openclaw-agent
tags:
  - github
  - release
  - open-source
  - wechat
  - nano-banana-pro
  - image-generation
  - developer-relations
dependencies:
  - brave-search
  - nano-banana-pro
  - wechat-article-pro
---

# AI开发者发布助手 (ai-dev-release-helper)

自动化 GitHub 项目发布全流程：竞品调研 → 封面图生成 → 公众号深度文章发布。

## 使用场景

当用户提到以下关键词时激活：
- "发布开源项目"、"新版本公告"
- "写项目介绍文章"、"生成项目封面"
- "GitHub Release"、"产品发布"
- "写公众号技术文"、"开发者内容运营"

## 工作流架构

```
输入：项目名称 + 简介 + GitHub链接
   ↓
┌──────────────────┐
│  brave-search   │ → 搜索竞品/行业背景 + 技术趋势
└────────┬─────────┘
         ↓
┌──────────────────┐
│ nano-banana-pro │ → AI 生成项目封面图 + 功能亮点图
└────────┬─────────┘
         ↓
┌──────────────────┐
│ wechat-article-pro │ → 生成 3000-5000 字深度分析文 + 自动排版
└──────────────────┘
         ↓
   输出：封面图 + 公众号文章（可一键发布）
```

## 快速使用

```bash
# 完整工作流
openclaw run ai-dev-release-helper \
  --project "LitAI" \
  --tagline "开源 GPT-4 级中文大模型" \
  --github "https://github.com/example/litai" \
  --output ./output/
```

## 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| project | string | ✅ | 项目名称 |
| tagline | string | ✅ | 一句话介绍 |
| github | string | ✅ | GitHub 仓库地址 |
| features | string[] | ❌ | 核心功能列表（默认从 README 提取）|
| output | string | ❌ | 输出目录（默认 ./output）|

## 工作流步骤

### Step 1: brave-search — 竞品与行业调研

搜索同类型开源项目的市场定位、技术特点、用户评价，输出结构化竞品分析摘要。

```
输入：项目名称 + 赛道关键词
输出：competitor_analysis.md（竞品列表 + 差异化要点）
超时：30 秒
```

### Step 2: nano-banana-pro — 项目视觉资产生成

调用 Gemini 3 Pro Image 生成两张图：
1. **封面图**：项目 Hero 图，品牌感强，适合公众号头图
2. **功能图**：核心功能可视化，适合文章插图

```
输入：
  - prompt: "{project} {tagline} hero image, tech dark theme, modern UI"
  - size: 2K
  - output: cover.png, feature.png
超时：60 秒
```

### Step 3: wechat-article-pro — 公众号深度文章生成

基于竞品分析 + 项目信息，生成 3000-5000 字技术分析文，风格参考刘润老师的商业分析逻辑。

```
输入：
  - topic: 项目发布公告
  - style: 刘润风格（通俗易懂 + 案例 + 数据）
  - images: cover.png, feature.png（自动上传为公众号配图）
  - autoTypeset: true
输出：article.md（可直接粘贴到公众号后台）
超时：180 秒
```

## 输出格式

```json
{
  "project": "LitAI",
  "tagline": "开源 GPT-4 级中文大模型",
  "github": "https://github.com/example/litai",
  "outputs": {
    "competitorAnalysis": "output/competitor_analysis.md",
    "coverImage": "output/cover.png",
    "featureImage": "output/feature.png",
    "article": "output/article.md"
  },
  "articleStats": {
    "wordCount": 4200,
    "images": 2,
    "readTime": "8 分钟"
  }
}
```

## 输出文件说明

| 文件 | 说明 |
|------|------|
| `competitor_analysis.md` | 竞品调研 Markdown，500-800 字 |
| `cover.png` | 封面图，2K 分辨率，16:9 |
| `feature.png` | 功能亮点图，2K 分辨率，4:3 |
| `article.md` | 公众号文章 Markdown，可直接粘贴发布 |

## 示例文章结构

```markdown
# {Project} 正式发布：为什么我们赌在了这个方向？

## 引言
{一句话介绍项目，为何此时发布}

## 01 市场背景：为什么现在是最佳时间点？
{基于 brave-search 竞品分析}

## 02 产品解析：{Project} 解决什么问题？
{核心功能 + 技术亮点}

## 03 与竞品对比：我们的差异化在哪里？
{竞品表格对比}

## 04 团队故事：为什么是我们？
{团队背景 / 开源理念}

## 05 未来路线图
{下一步计划}

## 结语
{开源邀请 / 社区呼吁}
```

## 注意事项

- **GitHub 链接**：确保仓库公开且有 README，工具会自动抓取关键信息
- **封面图**：默认使用科技深色主题，如需调整风格可在 prompt 中说明
- **公众号发布**：需用户手动将 article.md 内容粘贴到公众号后台，或配置自动发布
- **竞品调研**：搜索结果基于 DuckDuckGo 公开数据，可能不包含最新信息

## 技术栈

- **调研**：`brave-search`（Web Search API）
- **图片**：`nano-banana-pro`（Gemini 3 Pro Image）
- **文章**：`wechat-article-pro`（微信公众号发布）
- **编排**：OpenClaw Skill Combo
