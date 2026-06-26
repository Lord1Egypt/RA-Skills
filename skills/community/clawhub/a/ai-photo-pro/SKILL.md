---
name: ai-photo-pro
version: 2.0.0
description: 通过 NVIDIA NIM API 或 SiliconFlow API 生成图片。支持 Kolors (快手可图)、Qwen-Image (通义千问)、flux.2-klein-4b 等模型。当用户要求"生成图片"、"画一张图"、"AI绘图"或类似表达时调用。支持中文提示词，返回图片文件路径。
---

# AiPhotoPro - AI 图片生成工具

支持双引擎：**NVIDIA NIM API**（flux.2-klein-4b）和 **SiliconFlow API**（Kolors / Qwen-Image）。

## 调用方式

### 命令行（推荐）

```bash
# SiliconFlow - 可图 Kolors（默认）
python /home/ubuntu/.openclaw/skills/ai-photo-pro/scripts/siliconflow_main.py "<提示词>" ["<负面提示词>"]

# SiliconFlow - 通义千问 Qwen-Image（付费模型，建议按需选取）
python /home/ubuntu/.openclaw/skills/ai-photo-pro/scripts/siliconflow_main.py "<提示词>" ["<负面提示词>"] --model Qwen/Qwen-Image

# NVIDIA NIM API - flux.2-klein-4b
python /home/ubuntu/.openclaw/skills/ai-photo-pro/scripts/nvid_main.py "<提示词>"
```

### Python 导入

```python
import sys
sys.path.insert(0, '/home/ubuntu/.openclaw/skills/ai-photo-pro/scripts')

# SiliconFlow
from siliconflow_main import generate_png
img_list = generate_png(model="Kwai-Kolors/Kolors", base_str="<提示词>", negative_prompt="<负面提示词>")

# NVIDIA
from nvid_main import run_pngvidapi
img_path = run_pngvidapi(model="flux.2-klein-4b", base_str="<提示词>")
```

## 参数说明

### SiliconFlow `generate_png()`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | ❌ | 模型名，默认 `Kwai-Kolors/Kolors`，可选 `Qwen/Qwen-Image`（付费模型，建议按需选取） |
| `base_str` | string | ✅ | 中文提示词 |
| `negative_prompt` | string | ❌ | 负面提示词，可空 |
| `batch_size` | int | ❌ | 批量大小，默认 1 |
| `num_inference_steps` | int | ❌ | 推理步骤数，默认 20 |
| `guidance_scale` | float | ❌ | 提示词匹配度，默认 2.5 |

### NVIDIA `run_pngvidapi()`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | ✅ | 固定填 `flux.2-klein-4b` |
| `base_str` | string | ✅ | 中文提示词 |

## 输出

- 图片保存路径：`/home/ubuntu/.openclaw/skills/ai-photo-pro/scripts/img_data/<model>_<timestamp>.png`
- 函数返回值为图片路径列表

## API Key 配置

首次使用需配置 API Key，运行交互式配置脚本：

```bash
python /home/ubuntu/.openclaw/skills/ai-photo-pro/scripts/config_json.py
```

或手动写入 `config.json`（位于 `scripts/` 目录）：

```json
{
  "NVID": "nvapi-你的NVID密钥",
  "SILICONFLOW": "sk-你的SiliconFlow密钥"
}
```

### 获取 Key

- **NVID API Key**: https://nim.nvidia.com/ 注册获取
- **SiliconFlow API Key**: https://cloud.siliconflow.cn/i/IOo0eaWy 注册获取

## 示例提示词

**人物：**
```
一位美丽的短发东亚女性坐在高层公寓的落地窗前,身穿紧身的白色衬衫,(光线是午后柔和的定向自然光,在人物身上形成优美的明暗轮廓),脸上带着温暖而亲密的微笑,皮肤毛孔清晰,虹膜清晰锐利
```

**物体/场景：**
```
一个小苹果，红彤彤的，挂在绿叶树枝上，阳光照射，背景是模糊的果园，摄影风格，高清细节
```

**风格化：**
```
赛博朋克城市夜景，霓虹灯光，雨后街道，反射，高对比度，电影感
```

## 注意事项

- SiliconFlow 默认尺寸 1024×1024，steps=20
- NVIDIA 默认尺寸 1024×1024，steps=4（更快）
- 生成失败 SiliconFlow 会抛出异常；NVIDIA 会自动重试最多 5 次
- 图片路径通过函数返回值传递，方便 agent 捕获并发送
