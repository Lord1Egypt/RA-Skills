---
name: comfyui-v8
description: ComfyUI V8 秋叶中文版 全流程助手。提供安装检测、一键启动、工作流生成（文生图/图生图/ControlNet/InstantID等）、参数优化、故障排查、批量生成、模型管理等功能。All-in-one assistant for ComfyUI V8 (Aki bundle) with workflow generation, one-click startup, troubleshooting, and advanced features.
---

# ComfyUI V8 秋叶中文版助手 / ComfyUI V8 Aki Bundle Assistant

## 功能概览 / Features

| 功能 | 描述 |
|------|------|
| 🔍 环境检测 | 检测整合包安装状态、模型、依赖 |
| 🚀 一键启动 | 启动绘世启动器或ComfyUI核心服务 |
| 🎨 工作流生成 | 文生图、图生图、ControlNet、InstantID、扩图、局部重绘 |
| ⚙️ 参数优化 | 显存优化、常用参数推荐 |
| 🐛 故障排查 | 常见错误诊断与修复方案 |
| 📦 模型管理 | Checkpoint/LoRA/ControlNet 模型切换 |
| 🔄 批量生成 | 多提示词批量出图 |
| 🔗 增强功能 | 绘世启动器/300+节点/国内加速/FLUX支持 |
| 📊 工作流管理 | 导出/导入/复制/对比 |

## 触发词 / Triggers

`ComfyUI`, `comfyui`, `秋叶`, `绘世启动器`, `文生图`, `图生图`, `ControlNet`, `InstantID`, `扩图`, `局部重绘`, `工作流`, `comfy workflow`

## 使用方法 / Usage

### 命令格式 / Command Format

```
检测ComfyUI环境        # 环境检测
启动ComfyUI            # 一键启动
生成文生图工作流        # 文生图
生成图生图工作流        # 图生图
生成ControlNet工作流    # ControlNet
生成InstantID工作流     # InstantID
生成扩图工作流          # 扩图
生成局部重绘工作流       # 局部重绘
优化ComfyUI参数         # 参数优化
ComfyUI故障排查         # 故障排查
批量生成图片            # 批量生成
管理ComfyUI模型         # 模型管理
```

## 核心参数 / Core Parameters

### 文生图 / Text-to-Image

| 参数 | 默认值 | 说明 |
|------|--------|------|
| prompt | 高质量, 8k, 高清, 细节丰富 | 正向提示词 |
| negative_prompt | 模糊, 低分辨率, 畸形, 水印 | 负向提示词 |
| model | sdxl_base.safetensors | 模型选择 |
| width | 1024 | 宽度 |
| height | 1024 | 高度 |
| steps | 28 | 采样步数 |
| cfg | 7 | CFG强度 |
| sampler | dpmpp_2m | 采样器 |
| scheduler | karras | 调度器 |

### 模型类型 / Model Types

- **SDXL Base**: `sdxl_base.safetensors` (1024x1024 推荐)
- **SD 1.5**: `sd15_base.safetensors` (512x512 推荐)
- **FLUX**: `flux_dev.safetensors` / `flux_schnell.safetensors` (1024x1024+)
- **InstantID**: 需要 `antelopev2` embeddings + `ip-adapter-instantid-sdxl.safetensors`

## 工作流 JSON 结构（秋叶V8标准）/ Workflow JSON Structure

```json
{
  "name": "秋叶V8-文生图",
  "nodes": [
    {"type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "sdxl_base.safetensors"}},
    {"type": "CLIPTextEncode", "inputs": {"text": "正向提示词"}},
    {"type": "CLIPTextEncode", "inputs": {"text": "负向提示词"}},
    {"type": "EmptyLatentImage", "inputs": {"width": 1024, "height": 1024, "batch_size": 1}},
    {"type": "KSampler", "inputs": {"steps": 28, "cfg": 7, "sampler_name": "dpmpp_2m", "scheduler": "karras"}},
    {"type": "VAEDecode", "inputs": {}},
    {"type": "SaveImage", "inputs": {"filename_prefix": "txt2img"}}
  ]
}
```

## 故障排查 / Troubleshooting

| 错误现象 | 解决方案 |
|----------|----------|
| 启动闪退 | 安装 .NET Framework 4.8+、以管理员运行、检查路径无中文/空格 |
| 显存不足 | 开启 --lowvram 模式、降低分辨率、分块加载模型 |
| 模型加载失败 | 检查模型完整性、确认放置在正确目录 (models/checkpoints) |
| 节点缺失 | 绘世启动器 → 拓展管理 → 一键安装缺失节点 |
| 中文乱码 | 秋叶V8已内置中文，无需修改，重启即可 |
| 卡在 "Loading models" | 检查网络/磁盘空间、手动下载模型到 models/checkpoints |

## 显存优化方案 / VRAM Optimization

| 显存 | 推荐方案 |
|------|----------|
| < 6GB | 4bit量化、SD 1.5/7B小模型、关闭高分辨率 |
| 6-12GB | 8bit量化、1024x1024、启用VAE分块解码 |
| > 12GB | FP16原生、1536x1536高分辨率、批量生成 |

```bash
# 启动参数（编辑 启动ComfyUI.bat）
# 低显存模式
.\python_embeded\python.exe .\main.py --lowvram --cpu

# 中等显存（RTX 3060 12G）
.\python_embeded\python.exe .\main.py --normalvram

# 秋叶V8启动器勾选「低显存模式」即可
```

## 模型目录结构 / Model Directory Structure

```
ComfyUI-aki-V8/
├── models/
│   ├── checkpoints/          # SD/SDXL/FLUX 主模型
│   ├── lora/                  # LoRA 模型
│   ├── controlnet/            # ControlNet 模型
│   ├── embeddings/           # Textual Inversion / InstantID
│   ├── vae/                   # VAE 模型
│   └── upscale_models/        # 放大模型 (ESRGAN等)
├── user/
│   └── default/
│       └── workflows/         # 默认工作流存储
└── 启动ComfyUI.bat            # 启动脚本
```

## 工作流模板（秋叶V8标准节点）/ Workflow Templates

### 1. 文生图 (Text-to-Image)

```json
{
  "name": "秋叶V8-文生图",
  "nodes": [
    {"type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "sdxl_base.safetensors"}},
    {"type": "CLIPTextEncode", "inputs": {"text": "正向提示词"}},
    {"type": "CLIPTextEncode", "inputs": {"text": "负向提示词"}},
    {"type": "EmptyLatentImage", "inputs": {"width": 1024, "height": 1024, "batch_size": 1}},
    {"type": "KSampler", "inputs": {"steps": 28, "cfg": 7, "sampler_name": "dpmpp_2m", "scheduler": "karras"}},
    {"type": "VAEDecode", "inputs": {}},
    {"type": "SaveImage", "inputs": {"filename_prefix": "txt2img"}}
  ]
}
```

### 2. 图生图 (Image-to-Image)

```json
{
  "name": "秋叶V8-图生图",
  "nodes": [
    {"type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "sdxl_base.safetensors"}},
    {"type": "CLIPTextEncode", "inputs": {"text": "正向提示词"}},
    {"type": "CLIPTextEncode", "inputs": {"text": "负向提示词"}},
    {"type": "LoadImage", "inputs": {"image": "input.png"}},
    {"type": "VAEEncode", "inputs": {}},
    {"type": "KSampler", "inputs": {"steps": 28, "cfg": 7, "sampler_name": "dpmpp_2m", "scheduler": "karras"}},
    {"type": "VAEDecode", "inputs": {}},
    {"type": "SaveImage", "inputs": {"filename_prefix": "img2img"}}
  ]
}
```

### 3. ControlNet 线稿/边缘/姿态控制

```json
{
  "name": "秋叶V8-ControlNet",
  "nodes": [
    {"type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "sdxl_base.safetensors"}},
    {"type": "CLIPTextEncode", "inputs": {"text": "正向提示词"}},
    {"type": "CLIPTextEncode", "inputs": {"text": "负向提示词"}},
    {"type": "LoadImage", "inputs": {"image": "control.png"}},
    {"type": "ControlNetLoader", "inputs": {"control_net_name": "canny.safetensors"}},
    {"type": "ControlNetApply", "inputs": {"strength": 0.8}},
    {"type": "EmptyLatentImage", "inputs": {"width": 1024, "height": 1024, "batch_size": 1}},
    {"type": "KSampler", "inputs": {"steps": 28, "cfg": 7, "sampler_name": "dpmpp_2m", "scheduler": "karras"}},
    {"type": "VAEDecode", "inputs": {}},
    {"type": "SaveImage", "inputs": {"filename_prefix": "controlnet"}}
  ]
}
```

### 4. InstantID 人脸一致性

```json
{
  "name": "秋叶V8-InstantID人脸",
  "nodes": [
    {"type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "ip-adapter-instantid-sdxl.safetensors"}},
    {"type": "CLIPTextEncode", "inputs": {"text": "正向提示词"}},
    {"type": "CLIPTextEncode", "inputs": {"text": "负向提示词"}},
    {"type": "LoadImage", "inputs": {"image": "face.png"}},
    {"type": "InstantIDModelLoader", "inputs": {}},
    {"type": "InstantIDApply", "inputs": {"strength": 0.7}},
    {"type": "EmptyLatentImage", "inputs": {"width": 1024, "height": 1024, "batch_size": 1}},
    {"type": "KSampler", "inputs": {"steps": 28, "cfg": 7, "sampler_name": "dpmpp_2m", "scheduler": "karras"}},
    {"type": "VAEDecode", "inputs": {}},
    {"type": "SaveImage", "inputs": {"filename_prefix": "instantid"}}
  ],
  "models_required": ["antelopev2", "ip-adapter-instantid-sdxl"]
}
```

### 5. 扩图 (Outpainting)

```json
{
  "name": "秋叶V8-智能扩图",
  "nodes": [
    {"type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "sdxl_base.safetensors"}},
    {"type": "CLIPTextEncode", "inputs": {"text": "正向提示词"}},
    {"type": "CLIPTextEncode", "inputs": {"text": "负向提示词"}},
    {"type": "LoadImage", "inputs": {"image": "base.png"}},
    {"type": "ImageResize", "inputs": {"width": 2048, "height": 2048, "method": "lanczos"}},
    {"type": "VAEEncode", "inputs": {}},
    {"type": "KSampler", "inputs": {"steps": 28, "cfg": 7, "sampler_name": "dpmpp_2m", "scheduler": "karras"}},
    {"type": "VAEDecode", "inputs": {}},
    {"type": "SaveImage", "inputs": {"filename_prefix": "outpaint"}}
  ]
}
```

### 6. 局部重绘 (Inpainting)

```json
{
  "name": "秋叶V8-局部重绘",
  "nodes": [
    {"type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "sdxl_base.safetensors"}},
    {"type": "CLIPTextEncode", "inputs": {"text": "正向提示词"}},
    {"type": "CLIPTextEncode", "inputs": {"text": "负向提示词"}},
    {"type": "LoadImage", "inputs": {"image": "base.png"}},
    {"type": "LoadImage", "inputs": {"image": "mask.png"}},
    {"type": "VAEEncodeForInpaint", "inputs": {}},
    {"type": "KSampler", "inputs": {"steps": 28, "cfg": 7, "sampler_name": "dpmpp_2m", "scheduler": "karras"}},
    {"type": "VAEDecode", "inputs": {}},
    {"type": "SaveImage", "inputs": {"filename_prefix": "inpaint"}}
  ]
}
```

## 常见报错修复 / Common Error Fixes

| 错误 | 修复方法 |
|------|----------|
| 缺少.NET | 安装.NET 6.0桌面运行时，绘世启动器会自动引导下载 |
| 显存不足 | 启动器勾选低显存、4bit量化、减小尺寸 |
| 节点缺失 | 绘世启动器 → 拓展管理 → 一键安装缺失节点 |
| 模型加载失败 | 模型路径无中文/空格，放到models/checkpoints |
| 中文乱码 | 秋叶V8已内置中文，无需修改，重启即可 |

## 注意事项 / Notes

- 秋叶V8已内置中文界面，无需额外汉化
- 模型建议放置在 `models/checkpoints/` 目录
- FLUX 模型需要更多显存 (建议 16GB+)
- 定期使用绘世启动器更新内核和插件
- 工作流保存路径：`user/default/workflows/`

## 秋叶V8专属增强功能 / Aki V8 Exclusive Features

| 功能 | 说明 |
|------|------|
| 绘世启动器 | 内核/插件/模型/更新 一站式管理 |
| 300+预装节点 | ControlNet/InstantID/LayerDiffusion/IC-Light |
| 中文界面 | 节点/菜单/提示/日志 全汉化 |
| 国内加速 | GitHub镜像 + 模型下载加速 |
| 全模型支持 | FLUX / SD3 / SDXL / SD1.5 |
| 一键备份 | 工作流/模型/配置 备份还原 |

## 机器人触发指令 / Bot Commands

| 指令 | 功能 |
|------|------|
| `ComfyUI检测` | 环境检测 |
| `启动ComfyUI` | 一键启动 |
| `生成文生图工作流` | 生成txt2img |
| `生成ControlNet工作流` | 生成ControlNet |
| `ComfyUI显存优化` | VRAM优化 |
| `ComfyUI修复` | 报错修复 |
| `ComfyUI增强功能` | 查看V8增强功能 |
