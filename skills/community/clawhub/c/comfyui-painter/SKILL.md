---
name: comfyui-painter
version: "2.0.0"
description: "本地 ComfyUI 画图工作流 + CivitAI 集成。通过 API 控制本地 ComfyUI 生成图片（文生图/图生视频），支持 CivitAI 模型搜索/下载/更新检查/自动调参。Use when: 用户说画图、生成图片、generate image、comfyui、换模型、调参数、出图、搜模型、下载模型、c站、civitai，或在 Discord #🎨-画图 频道的任何消息。NOT for: 非图片生成相关的请求。"
---

# ComfyUI Painter v2.0

通过 ComfyUI API 在本地 RTX 5090 上生成图片，集成 CivitAI 模型管理。

## 工作流程

1. 检查 ComfyUI 是否运行，未运行则自动启动
2. 解析用户需求：提示词、模型、参数
3. **自动调参**：根据模型从 CivitAI 获取推荐参数（或使用 config 缓存）
4. 调用 generate.py 生成图片
5. 将图片发送到 Discord
6. 心跳时调用 auto_shutdown.py 检查空闲关闭

## 脚本路径

所有脚本相对于此 skill 目录：
- `scripts/comfyui_manager.py` — 启动/关闭/状态
- `scripts/generate.py` — 生成图片（Python API 调用）
- `scripts/auto_shutdown.py` — 空闲自动关闭检查
- `scripts/civitai.py` — **CivitAI 集成**（搜索/详情/下载/更新检查/推荐参数）
- `scripts/auto_tune.py` — **自动调参**（从 CivitAI 样图元数据提取推荐设置）
- `config.json` — 配置文件（模型别名、默认参数、路径、CivitAI 关联）

## 使用方式

### 启动 ComfyUI
```python
import scripts.comfyui_manager as mgr
mgr.start()  # 自动从 WSL 启动 Windows ComfyUI 进程
```

### 生成图片
```python
from scripts.generate import generate
result = generate(
    positive="your prompt here",
    model="noobv6",        # 见下方模型别名
    batch_size=4,
    width=1024,
    height=1536,
    steps=20,
    cfg=5,
)
# result = {"ok": True, "images": ["/mnt/d/.../sdi_00201_.png", ...]}
```

### 带自动调参生成
```python
from scripts.auto_tune import get_tuned_params
from scripts.generate import generate

params = get_tuned_params("janku")  # 从 CivitAI 获取推荐参数
result = generate(
    positive="your prompt",
    model="janku",
    steps=params["steps"],
    cfg=params["cfg"],
    width=params["width"],
    height=params["height"],
)
```

### CivitAI 搜索模型
```bash
python3 scripts/civitai.py search "anime checkpoint" --limit 5
```

### CivitAI 查看模型详情
```bash
python3 scripts/civitai.py info 140272
```

### CivitAI 获取推荐参数
```bash
python3 scripts/civitai.py params 140272
```

### CivitAI 检查本地模型更新
```bash
python3 scripts/civitai.py check-updates
```
> ⚠️ 需要计算 SHA256，每个文件约 30 秒

### CivitAI 下载模型
```bash
python3 scripts/civitai.py download "https://civitai.com/api/download/models/XXXXX" --filename model_name.safetensors
```

### 更新所有模型的推荐参数到 config
```bash
python3 scripts/auto_tune.py update-all
```

### 发送图片到 Discord
生成完成后，将图片 cp 到 workspace 临时目录，用 message tool 发送到 #🎨-画图 频道（channel:1476675131404193823）。

### 关闭 ComfyUI
```python
import scripts.comfyui_manager as mgr
mgr.stop()
```

## 模型别名

| 别名 | Checkpoint | CivitAI ID | 版本 | 风格 |
|------|-----------|------------|------|------|
| hassaku | hassakuXLIllustrious_v34 | 140272 | v3.4 | Illustrious 动漫 |
| noobv6 | pornmasterPro_noobV6 | 1045588 | noob-V6 | NoobAI 动漫（默认）|
| noobv4 | pornmasterPro_noobV4 | 1045588 | noob-V4 | NoobAI 动漫（旧版）|
| sdxlv8 | pornmaster_proSDXLV8 | 82543 | Pro-SDXL-V8 | SDXL 写实 |
| janku | JANKUTrainedNoobaiRouwei_v69 | 1277670 | v6.9 | NoobAI+RouWei 混合 |
| nova3d | nova3DCGXL_ilV80 | 715287 | IL v8.0 | 3DCG/2.5D |
| unholy | unholyDesireMixSinister_v70 | 1307857 | v7.0 | 暗黑美学 |
| flux | flux1-dev-bnb-nf4-v2 | 638187 | BNB NF4 v2 | Flux 写实 |

## 自动调参（model_params）

每个模型在 config.json 中有 CivitAI 推荐的最佳参数。生成时：
1. 用户指定的参数优先
2. 未指定则使用 `config.json → model_params[alias]` 的推荐值
3. model_params 也没有则使用 `defaults` 全局默认

| 模型 | Steps | CFG | 采样器 |
|------|-------|-----|--------|
| hassaku | 20 | 7 | euler_a |
| janku | 20 | 7 | euler_a |
| noobv6 | 20 | 7 | euler_a |
| sdxlv8 | 25 | 5 | dpmpp_2m |
| nova3d | 20 | 7 | euler_a |
| unholy | 20 | 7 | euler_a |
| flux | 20 | 1 | euler |

## CivitAI 配置

API Key 存于 `~/.openclaw/workspace/credentials/civitai.md`，格式：
```
# CivitAI API Key
Token: your_api_key_here
```

## 提示词优化指南

用户给自然语言描述时，转换为专业 Stable Diffusion 提示词：
- 质量标签在前：`masterpiece, best quality, absurdres, highres`
- 用 `BREAK` 分隔不同语义段
- 动作/姿势用专业标签：`mating press, pov, from below, spread legs`
- 细节标签：`detailed skin, sweat, wet skin, motion blur, dynamic angle`
- 负面提示词加入：`censored, mosaic censoring, bar censor`

## 心跳集成

每次心跳时运行 auto_shutdown.py 检查空闲时间，超过 15 分钟无使用自动关闭 ComfyUI 释放显存。
