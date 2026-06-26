---
name: comfyui-upscaler
description: ComfyUI 多重扩散放大自动化工具。当用户想要放大 AI 生成的图片、处理高清图像、放大小图、提高图片分辨率时使用。支持文生图和图生图两种基础工作流，自动执行三重放大（潜空间放大→区块放大→模型放大）。使用场景包括：(1) 将低分辨率 AI 绘画放大到 4K/8K (2) 增强图片细节和清晰度 (3) ComfyUI 工作流自动搭建
---

# ComfyUI 多重扩散放大 Skill

本 Skill 帮助你在 ComfyUI 中快速搭建并运行「三重超清放大」工作流。

## 工作流原理

三重放大 = **潜空间重采样** → **分区模型放大** → **全局锐化**

| 步骤 | 节点 | 作用 |
|------|------|------|
| 1 | Latent Scale + K采样器 | 在潜空间加噪声重采样，增加细节 |
| 2 | SD Upscale (分区放大) | 分块放大避免显存爆炸，局部增强 |
| 3 | Image Upscale with Model | 全局锐化，让模糊变清晰 |

## 快速开始

### 检查环境

```bash
cd ~/.openclaw/skills/comfyui-upscaler
python3 scripts/check_env.py
```

### 生成工作流

```bash
python3 scripts/generate_workflow.py \
  --base_model "your-sd-model.safetensors" \
  --upscale_model "4x-UltraSharp.pth" \
  --tile_size 1024 \
  --output "upscaled_workflow.json"
```

### 在 ComfyUI 中加载

1. 打开 ComfyUI
2. 点击 "Load" 加载生成的 `upscaled_workflow.json`
3. 拖入你的低分辨率图片
4. 点击 "Queue"

## 脚本说明

### generate_workflow.py

生成可导入 ComfyUI 的工作流 JSON 文件。

**参数：**
- `--base_model`: 基础模型路径（SD1.5/SDXL/Pony等）
- `--upscale_model`: 放大模型（4x-UltraSharp 等）
- `--tile_size`: 分块大小（默认1024，SDXL建议1024以上）
- `--scale`: 放大倍数（默认2）
- `--denoise`: 重采样去噪强度（默认0.35）
- `--output`: 输出JSON路径

### check_env.py

检查 ComfyUI 环境是否满足要求：
- ComfyUI 是否安装
- 必要的节点是否安装（LatentScale、SDUpscale等）
- 放大模型是否存在

## 参考资料

- [工作流详解](references/workflow_details.md) - 各节点参数详解
- [模型推荐](references/models.md) - 推荐使用的放大模型
- [常见问题](references/faq.md) - 常见问题和解决方案
