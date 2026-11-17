# AI Media Generation — Agent 入口

> 本仓库是 skills-repo 组织下的 AI 媒体生成技能库。面向独立开发者和内容创作者，覆盖图像生成/编辑与视频生成/编辑，帮你把 AI 变成媒体生产流水线。

## 架构与加载顺序（superpower）

本仓库按 skills-repo 的 **superpower 架构**组织，Agent 加载顺序如下：

1. **先读 `SKILL.md`（L1 路由层）** — 只做能力索引，不要在此找方法论正文。
2. **按需读 `references/`（L2）** — ComfyUI 工作流、图像生成、视频生成三篇 playbook，按任务类型加载，不全量读。
3. **落地具体能力时读 `skills/<name>/SKILL.md`（L3）** — 图像生成 / 图像编辑 / 视频生成 / 视频编辑的细粒度能力。
4. **确定性任务用 `scripts/`（L4）** — 工作流 JSON 校验、批量媒体处理，产物可复现。
5. **模板套用看 `assets/`（L5）** — ComfyUI 工作流样例、prompt 模板库。

渐进式加载原则：先路由、后深度；不凭记忆猜模型参数与 API。

## 技能清单

| 环节 | 技能 | 文件 | 用途 |
|------|------|------|------|
| 图像 | image-generation | [skills/image-generation/SKILL.md](skills/image-generation/SKILL.md) | 文生图/图生图：选型、prompt、参数、批量 |
| 图像 | image-editing | [skills/image-editing/SKILL.md](skills/image-editing/SKILL.md) | 修图：inpaint、扩图、ControlNet、去背景 |
| 视频 | video-generation | [skills/video-generation/SKILL.md](skills/video-generation/SKILL.md) | 文生/图生视频：路线、工具、参数 |
| 视频 | video-editing | [skills/video-editing/SKILL.md](skills/video-editing/SKILL.md) | 后期：拼接、字幕、转码、交付 |

## 使用场景

- 独立开发者生成产品图、宣传视频、App 演示素材
- 内容创作者批量产出风格统一的配图与短视频
- 接入 ComfyUI 工作流做批量自动化生产
- 电商/营销素材的快速生成与统一处理

## 相关仓库

- `animation-engineer` — 动效/动画实现（本仓库聚焦 AI 生成图像/视频，那边聚焦 UI 动效实现）
- `indie-game-developer` — 游戏开发（本仓库提供 AI 素材生成）
- `design-studio` — UI/UX 设计（本仓库聚焦 AI 媒体生成）
- `content-creator` — 内容创作文案（本仓库提供配套配图/视频）

> 本仓库聚焦 **AI 媒体生成与后处理的完整交付链路**，从选型决策到批量生产再到交付规格，与 design-studio 的 UI 设计视角、animation-engineer 的动效实现视角互补。
