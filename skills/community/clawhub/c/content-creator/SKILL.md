---
name: content-creator
description: >-
  内容创作者技能库：覆盖短视频脚本、视频编辑、播客制作、YouTube 运营与新闻简报（邮件通讯）的全流程。
  提供内容策略与平台适配、选题与制作工作流的方法论，并用子技能承载视频/音频/社媒/简报的具体落地写法。
  触发词："内容创作"、"短视频"、"视频编辑"、"播客"、"YouTube"、"简报"、"newsletter"、
  "邮件通讯"、"脚本"、"选题"、"剪辑"、"色彩分级"、"缩略图"、"发布排期"、"内容策略"、"多平台分发"。
agent_created: true
metadata:
  version: 1.0.0
  category: 内容创作
  difficulty: 进阶
  architecture: superpower
---

# 内容创作者 (Content Creator)

> 把 AI 编程助手变成一名能扛下内容交付链路（策略→脚本→制作→运营）的搭档：从选题策划到多平台分发，并用子技能守住每个环节的质量底线。

本技能采用 **superpower 架构**：`SKILL.md` 只做路由，深层 playbook 放在 `references/` 中**按需加载**，细粒度能力放在 `skills/` 子技能。本库聚焦**视频 / 音频 / 社交媒体内容**的策划制作与运营（文字内容见 `writer-studio`）。

## 何时使用

- 需要**内容策略**：选平台、定选题方向、搭内容矩阵
- 写**短视频脚本**：Hook 设计、节奏控制、故事弧线、平台适配
- 做**视频编辑**：剪辑流程、转场、色彩分级、字幕、多格式导出
- 做**播客制作**：选题策划、采访设计、后期编辑、分发
- 做 **YouTube 运营**：SEO、缩略图、数据分析、发布排期
- 做**新闻简报/邮件通讯**：选题策展、结构编排、语气校准、可发布 Markdown

## 能力索引（超级技能路由）

本技能采用渐进式加载。`SKILL.md` 仅作路由，**按需**读取下列 `references/` 中的完整 playbook；要落地某个具体环节的写法 → 直接调 `skills/` 对应子技能。

| 任务 | 读取 / 调用 | 关键词（grep 线索） |
|------|------------|---------------------|
| 内容策略与平台适配（决策树 + 矩阵） | [references/content-strategy.md](references/content-strategy.md) | 策略, 选题, 平台, 矩阵, 受众, 定位 |
| 制作工作流与发布前检查 | [references/production-workflow.md](references/production-workflow.md) | 工作流, 剪辑, 审核,  Checklist, 导出, 发布 |
| 新闻简报编排 playbook（决策树 + 格式矩阵 + 检索命令 + 坑） | [references/newsletter-playbook.md](references/newsletter-playbook.md) | 简报, 策展, 格式, 检索, 语气, 邮件 |
| 短视频脚本（细粒度调用） | [skills/short-video-script/SKILL.md](skills/short-video-script/SKILL.md) | 脚本, Hook, 节奏, 故事弧线, 平台适配 |
| 视频编辑（细粒度调用） | [skills/video-editing/SKILL.md](skills/video-editing/SKILL.md) | 剪辑, 转场, 色彩分级, 字幕, 导出 |
| 播客制作（细粒度调用） | [skills/podcast-generation/SKILL.md](skills/podcast-generation/SKILL.md) | 播客, 选题, 采访, 后期, 分发 |
| YouTube 运营（细粒度调用） | [skills/youtube-automation/SKILL.md](skills/youtube-automation/SKILL.md) | YouTube, SEO, 缩略图, 数据, 排期 |
| 新闻简报/邮件通讯（细粒度调用） | [skills/newsletter/SKILL.md](skills/newsletter/SKILL.md) | 简报, 邮件, newsletter, 策展, 通讯, 订阅 |

> 路由规则：先判断任务属于「策略 / 工作流」哪类方法论 → 读 `references/`；要落地某个具体环节的产出 → 直接调 `skills/` 对应子技能。

## 核心原则（始终遵循）

1. **先策略后制作**：没定受众与平台就开拍，等于盲打。先问"为谁、在哪、解决什么"。
2. **Hook 在前 3 秒**：短视频完播率决定推荐，开头必须抛钩子而非铺垫。
3. **可复现的工作流**：剪辑/字幕/导出走固定流程与清单，不靠每次临场发挥。
4. **数据驱动迭代**：发布后看留存与点击，而非自我感觉；缩略图与标题是 YouTube 的命门。
5. **渐进式加载**：先读路由表与对应 `references/`，再动手；不凭记忆猜平台规则。
6. **明确边界**：内容风格与选题拍板由创作者做，本技能出方法论与检查，不替代创意判断。

## 与其他技能协作

- 需要**文字内容**（文章/文案/SEO）→ 调用 `writer-studio`
- 需要**入站营销**（着陆页/投放）→ 调用 `marketing-master`
- 需要**办公文档/排版** → 调用 `office-master`
- 需要**视觉/封面设计** → 调用 `visual-designer`
