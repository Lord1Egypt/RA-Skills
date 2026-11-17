---
name: ai-media-generation
description: >-
  AI 媒体生成技能库：覆盖图像生成/编辑与视频生成/编辑，提供模型选型、提示词工程、参数调优、
  批量出图的执行链路，含本地 ComfyUI 工作流与云端 API（RunComfy/Veo/MiniMax）双路线，
  并用脚本固化工作流 JSON 校验与批量媒体处理。
  触发词："AI 生图"、"文生图"、"图生视频"、"文生视频"、"AI 视频"、"ComfyUI"、"SDXL"、"FLUX"、
  "ControlNet"、"inpaint"、"扩图"、"视频剪辑"、"图片批量处理"、"媒体生成"。
agent_created: true
metadata:
  version: 1.0.0
  category: AI媒体生成
  difficulty: 进阶
  architecture: superpower
---

# AI 媒体生成 (AI Media Generation)

> 把 AI 编程助手变成一名能扛下媒体生成交付链路（选型→生成→批量→后处理）的搭档：从模型选型到 ComfyUI 工作流，并用确定性脚本守住工作流质量与批量纪律。

本技能采用 **superpower 架构**：`SKILL.md` 只做路由，深层 playbook 放在 `references/` 中**按需加载**，细粒度能力放在 `skills/` 子技能，确定性任务交给 `scripts/`，可复用模板放在 `assets/`。

## 何时使用

- 需要 **AI 生图/文生图**：选模型、写提示词、调参数、批量出图
- 需要 **AI 修图**：局部重绘、扩图、抠图换背景、老照片修复
- 需要 **AI 视频**：文生视频、图生视频、视频生视频、数字人口播
- 需要 **ComfyUI 工作流**：本地部署、workflow JSON 校验、API 自动化
- 需要 **视频后处理**：片段拼接、转场、字幕、配乐、格式转码
- 需要 **批量媒体处理**：统一缩放/转格式/交付规格

## 能力索引（超级技能路由）

本技能采用渐进式加载（progressive disclosure）。`SKILL.md` 仅作路由，**按需**读取下列 `references/` 中的完整 playbook，避免一次性占满上下文。

| 任务 | 读取 / 调用 | 关键词（grep 线索） |
|------|------------|---------------------|
| ComfyUI 部署/工作流结构/API 自动化 | [references/comfyui-workflow-playbook.md](references/comfyui-workflow-playbook.md) | ComfyUI, 部署, workflow JSON, nodes, links, API |
| 图像生成：模型选型/prompt/参数/批量 | [references/image-generation-playbook.md](references/image-generation-playbook.md) | 生图, SDXL, FLUX, prompt, CFG, seed, hires |
| 视频生成：路线/工具对比/参数/拼接 | [references/video-generation-playbook.md](references/video-generation-playbook.md) | 视频, text2video, image2video, Veo, frames |
| 文生图/图生图（细粒度调用） | [skills/image-generation/SKILL.md](skills/image-generation/SKILL.md) | image-generation, 文生图, 批量出图 |
| 图像编辑/修图（细粒度调用） | [skills/image-editing/SKILL.md](skills/image-editing/SKILL.md) | inpainting, 扩图, ControlNet, 去背景 |
| 视频生成（细粒度调用） | [skills/video-generation/SKILL.md](skills/video-generation/SKILL.md) | video-generation, 图生视频, 口播 |
| 视频编辑/后期（细粒度调用） | [skills/video-editing/SKILL.md](skills/video-editing/SKILL.md) | 剪辑, 拼接, ffmpeg, 字幕, 转码 |
| 工作流 JSON 校验（确定性脚本） | [scripts/workflow_validator.py](scripts/workflow_validator.py) | 校验, 节点图, 悬空 link |
| 批量图片处理（确定性脚本） | [scripts/media_batch.py](scripts/media_batch.py) | 批量, 缩放, 转格式, webp |
| Prompt 模板库（可套用） | [assets/prompt-templates.md](assets/prompt-templates.md) | prompt 模板, 负面词, 实例 |
| ComfyUI 工作流样例（可套用） | [assets/workflows/text2image-basic.json](assets/workflows/text2image-basic.json) | 工作流模板, text2image |

> 路由规则：先判断任务属于「ComfyUI 基建 / 图像生成 / 视频生成 / 视频后处理」哪类方法论 → 读 `references/`；要落地具体某个能力 → 直接调 `skills/` 对应子技能；确定性任务（校验/批量）直接跑 `scripts/`。

## 内置脚本（确定性、可重复执行）

放在 `scripts/`，优先用脚本处理重复/确定性任务，而非每次重写代码：

- `scripts/workflow_validator.py --dir workflows/ --strict` — 校验 ComfyUI 工作流 JSON 节点图（重复 id/悬空 link/坏引用），可作 CI 门禁
- `scripts/media_batch.py --in output/ --out deliver/ --max-dim 1024 --format webp` — 批量缩放/转格式，`--dry-run` 预览、`--strict` 门禁

运行示例：

```bash
python3 scripts/workflow_validator.py assets/workflows/text2image-basic.json --strict
python3 scripts/media_batch.py --in ./output --out ./deliver --max-dim 1024 --format webp
```

## 模板资源

`assets/` 提供可直接套用的配置与模板：

- [assets/workflows/text2image-basic.json](assets/workflows/text2image-basic.json) — 最小可用 SDXL 文生图工作流（已过本仓库校验器）
- [assets/prompt-templates.md](assets/prompt-templates.md) — 图像/视频 prompt 模板库（五段式 + 负面词 + 实例 + 纪律）

## 核心原则（始终遵循）

1. **先定路线再动手**：文生图/图生图/文生视频/图生视频先按 playbook 决策树选，别盲目试。
2. **模型选型有依据**：默认 SDXL 起步，文字/高细节才上 FLUX；资源与成本要匹配。
3. **prompt 全英文**：正文英文、注释中文；负面词保持 15 词基线，不堆砌。
4. **确定性任务用脚本**：工作流校验与批量处理交给 `scripts/`，不每次手写代码。
5. **渐进式加载**：先读路由表与对应 `references/`，再动手；不凭记忆猜参数与 API。
6. **明确边界**：风格审美拍板由人做；版权风险（仿冒形象/受版权素材）一律提示自担，不替用户决定。

## 与其他技能协作

- 需要**前端/产品里嵌入生成能力** → 调用 `ai-fullstack-engineer`
- 需要**游戏美术素材生成** → 调用 `indie-game-developer`（本仓库聚焦 AI 生成，那边聚焦游戏管线）
- 需要**动效/动画实现** → 调用 `animation-engineer`
- 需要**视觉/UI 设计** → 调用 `design-studio`
- 需要**内容创作文案** → 调用 `content-creator`
