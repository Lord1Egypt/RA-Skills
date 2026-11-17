---
name: image-generation
description: AI 文生图与图生图，覆盖模型选型、提示词工程、参数调优与批量出图，对接本地 ComfyUI 与云端 API
source:
  type: derived
  repo: prime-skills/runcomfy-agent-skills
  path: ai-image-generation/SKILL.md
  version: 1.0.0
  updated: 2026-05-15
  url: https://skills.sh/prime-skills/runcomfy-agent-skills/ai-image-generation
metadata:
  category: 图像生成
  platform: 通用
  difficulty: 进阶
tags:
  - image-generation
  - stable-diffusion
  - sdxl
  - comfyui
  - prompt
---

# Image Generation — AI 图像生成

> 把 AI 变成你的出图流水线：选对模型、写好提示词、调准参数，批量产出可用素材。基于 skills.sh 全生态最高安装量（351.9K）的 runcomfy-agent-skills 改编，补充本地 ComfyUI 与批量纪律。

## 能力

- **模型选型**：SD1.5 / SDXL / FLUX / Turbo-LCM 按场景选型（人像、插画、文字渲染、速度）
- **提示词工程**：五段式正面 prompt（主体/细节/环境/风格/质量）+ 负面词三件套
- **参数调优**：steps / CFG / sampler / seed 的调整方向与复现纪律
- **批量出图**：固定 seed 列表、单变量实验、可复现命名
- **双路线执行**：本地 ComfyUI 工作流 与 云端 API（RunComfy 等）都能跑

## 使用方式

在 Claude Code 中使用 `/image-generation` 调用。

```
/image-generation 帮我生成一张赛博朋克街景图：主体、风格、参数都帮我定
/image-generation 现有 20 个商品名，写一个批量文生图方案（模型+prompt+seed策略）
/image-generation 这张图双头了，怎么修（hires fix 还是换模型）
```

## 工作流

1. **选型** — 按 [references/image-generation-playbook.md](../../references/image-generation-playbook.md) 模型决策树定模型与路线（本地/云端）
2. **写 prompt** — 五段式结构 + 负面词；正文用英文
3. **定参数** — 基线 25-30 步 / CFG 5-7 / 训练尺寸附近分辨率
4. **小样验证** — 单张出图人工检查（黑/灰/伪影/双头）
5. **批量执行** — 固定 seed、单变量推进，输出命名可复现
6. **放大交付** — 需要大图走 hires fix（基础图 + LatentUpscale + 低 denoise 二次采样）

## 适用场景

- 独立开发者为产品生成封面、配图、图标素材
- 内容创作者批量产出风格统一的配图
- 需要文字渲染/高细节时（FLUX）快速出图
- 接入 ComfyUI 工作流做批量自动化

## 限制

- 只做生成与调优，不做 AI 视频（见 `video-generation`）
- 不处理已生成图的精细修图（见 `image-editing`）
- 依赖本地 GPU 或云端 API 额度，无算力时不可用
- 版权风险自负：不用于生成仿冒他人风格/形象并商用
