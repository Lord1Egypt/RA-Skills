# AI全链路科技资讯工厂 (ai-tech-news-factory)

> 热点追踪 → 深度采集 → 多平台一键发布

## 🏭 业务场景

**场景**: 科技自媒体从业者、AI资讯 Newsletter 编辑、开发者社区运营者，需要每日持续产出高质量科技内容，覆盖小红书（短内容）和微信公众号（深度文）两个核心平台。

**痛点**:
- 手动搜集多个信息源耗时耗力
- 同一素材需要反复改写成不同格式
- 小红书需要配图，公众号需要深度文字，格式差异大
- 难以坚持每日稳定输出

## 💡 解决思路

将 5 个专业 Skill 串联成单向流水线：
1. **热点发现**（content-trend-weapon）确定今日选题方向
2. **深度采集**（rss-ai-reader）获取完整文章内容与AI摘要
3. **卡片生成**（card-renderer）为小红书制作视觉素材
4. **短内容发布**（xiaohongshutools）发布3条分类小红书笔记
5. **深度文章**（wechat-article-pro）生成2000-3000字公众号文章

## 🔧 Skill 编排图谱

```
content-trend-weapon          热点追踪
     │
     ▼
rss-ai-reader            RSS深度采集
     │
     ├──▶ card-renderer       知识卡片
     │          │
     │          ▼
     │    xiaohongshutools    小红书发布（3条）
     │
     └──▶ wechat-article-pro  公众号深度文章

[最终输出]
/root/articles/YYYY-MM-DD/
├── trending-topics.md
├── rss-summaries.md
├── cards/          (3张知识卡片)
├── xiaohongshu/   (发布记录)
└── wechat-article.md
```

## 📋 使用示例

### 触发完整流水线

```
帮我生成今天的AI科技资讯日报，包含：
- 热点话题分析（content-trend-weapon）
- RSS深度采集3个以上科技源（rss-ai-reader）
- 3张知识卡片（card-renderer）
- 3条小红书（xiaohongshutools）：热点类1条、应用类1条、深度类1条
- 1篇公众号深度文章（wechat-article-pro）
```

### 输出验证清单

- [ ] trending-topics.md 存在且包含≥5个热点话题
- [ ] rss-summaries.md 包含≥3篇文章的AI摘要
- [ ] cards/ 目录包含3张PNG卡片
- [ ] 小红书3条笔记全部发布成功（记录在posts.json）
- [ ] wechat-article.md 字数≥2000字

## 📦 依赖安装

```bash
# 安装 rss-ai-reader（clawhub）
clawhub install rss-ai-reader

# 本地已有 skills（无需安装）
# content-trend-weapon, card-renderer, xiaohongshutools, wechat-article-pro
```

## 🕐 定时任务建议

| 时间 | 任务 | 平台 |
|------|------|------|
| 02:00 UTC | 小红书日报（3+3+3分类）| xiaohongshutools |
| 08:00 UTC | 完整资讯工厂 | 本Combo |
| 00:04 UTC | 公众号深度文章 | wechat-article-pro |
