---
name: image-editing
description: AI 图像编辑与修图，覆盖局部重绘、扩图、抠图换背景、老照片修复，基于 img2img 与 ControlNet
source:
  type: derived
  repo: prime-skills/runcomfy-agent-skills
  path: image-edit/SKILL.md
  version: 1.0.0
  updated: 2026-05-15
  url: https://skills.sh/prime-skills/runcomfy-agent-skills/image-edit
metadata:
  category: 图像编辑
  platform: 通用
  difficulty: 进阶
tags:
  - image-editing
  - inpainting
  - outpainting
  - controlnet
  - img2img
---

# Image Editing — AI 图像编辑与修图

> 把 AI 变成修图工作台：局部重绘、扩图、抠图换背景、老照片修复，不依赖 Photoshop。基于 runcomfy-agent-skills 的 image-edit（405.6K 安装）改编，补充 ControlNet 与批量修图纪律。

## 能力

- **局部重绘（inpainting）**：改背景、去水印、换元素、修复崩坏部位
- **扩图（outpainting）**：构图外扩、补全画面
- **图生图（img2img）**：风格迁移、细节增强、分辨率提升
- **ControlNet 控制**：Canny 边缘 / Depth 深度 / OpenPose 姿态 / Tile 放大，让编辑"指哪打哪"
- **批量编辑**：多张图统一去背景/统一风格

## 使用方式

在 Claude Code 中使用 `/image-editing` 调用。

```
/image-editing 这张产品图背景太乱，帮我换成干净的浅色背景
/image-editing 老照片有划痕，修复一下并上色
/image-editing 这张图要扩成 16:9 的封面，用 outpainting
```

## 工作流

1. **定目标** — 是改背景/去水印/修复/扩图？决定 inpaint / outpaint / img2img / ControlNet
2. **备遮罩** — inpainting 需要准备 mask（遮罩区域）；ComfyUI 用 `Load Image (with Mask)` 或节点生成
3. **选模型** — 修复用专用 inpainting 模型（如 SDXL-inpainting），通用编辑用 SDXL + ControlNet
4. **定参数** — denoise：局部修改 0.5-0.8、扩图 0.6-0.9、增强 0.3-0.5；ControlNet strength 0.6-0.9
5. **小样验证** — 单张确认编辑区域正确、未破坏其他区域
6. **批量执行** — 同参数批量，逐张抽检

## 适用场景

- 产品图背景替换与风格统一（电商/内容创作）
- 老照片、扫描件的修复与增强
- 素材去水印、去杂物、构图重裁
- 批量图片统一处理（去背景/换风格）

## 限制

- 大改需要先有稳定出图的生成基础（依赖 `image-generation` 的模型基建）
- 精细抠图（发丝级）不如专业工具稳定，商用场景建议结合人工检查
- 不处理视频帧级编辑（见 `video-editing`）
- 修改有版权的内容时自行确认授权

## 相关参考（Playbook）

- [references/image-generation-playbook.md](../../references/image-generation-playbook.md) — 第 3 节参数速查（denoise/CFG 与生成端同源）、
  第 5 节伪影与出图异常排查；改图前先确认生成基线是否稳定
- [references/comfyui-workflow-playbook.md](../../references/comfyui-workflow-playbook.md) — inpaint / ControlNet 节点接线、模型放置目录
  （`checkpoints/loras/embeddings`）与 API 批量提交
