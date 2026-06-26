# 本地 SDXL 生图 (axelhu-local-sdxl)

基于 ComfyUI + SDXL 的本地图片生成技能。适用于需要高质量配图、素材生成、本地私密生图、或对在线生成有频率限制的场景。

## 触发时机

**在以下场景时使用：**
- 用户/其他 agent 说"本地生图"、"本地SD生图"、"用本地工具生成图片"
- 用户/其他 agent 说"私密生图"、"脱敏生图"、"不上传在线"
- 需要生成涉及隐私、测试、商业素材的内容，且明确指定本地处理
- 需要精细控制构图、风格、尺寸的生图任务，且指定本地执行

**不要用于：**
- 默认生图请求（那些默认走在线服务，如 Midjourney/DALL-E）
- 用户说"生成图片"、"画一张图"且没有指定本地（默认在线优先）

## 使用方式

直接描述想要的图片内容，例如：
- "帮我生成一张科技感十足的封面图"
- "画一个程序员深夜编程的场景，插画风格"
- "生成一张杭州西湖的夜景图，高清写实风格"

Agent 收到后执行生图脚本，发送结果给用户。

## 技术规格

| 项目 | 参数 |
|------|------|
| 模型 | Stable Diffusion XL 1.0 (fp16) |
| 显卡 | NVIDIA RTX 3080 (10GB VRAM) |
| 出图尺寸 | 默认 1024×768，可调整 |
| 生图速度 | ~18秒/张（euler 采样，20步） |
| 可用采样器 | euler, dpmpp_2m, lcm, ddim 等 |
| API 端口 | localhost:8188 |

## Agent 调用方法

### 方式一：通过脚本调用（推荐）

```python
import subprocess
result = subprocess.run(
    ["python3", "/path/to/scripts/sdxl_generate.py",
     "--prompt", "一只狐狸在森林里",
     "--negative", "模糊, 低质量",
     "--steps", "20",
     "--seed", "42",
     "--output", "/tmp/output.png"],
    capture_output=True, text=True
)
print(result.stdout)
```

### 方式二：直接调 ComfyUI REST API

```python
import requests, time, json

COMFYUI = "http://localhost:8188"

def generate(prompt, negative="", steps=20, seed=42, width=1024, height=768):
    workflow = {
        "loader": {"class_type": "CheckpointLoaderSimple",
                   "inputs": {"ckpt_name": "sdxl-base-1.0.safetensors"}},
        "positive": {"class_type": "CLIPTextEncode",
                     "inputs": {"text": prompt, "clip": ["loader", 1]}},
        "negative": {"class_type": "CLIPTextEncode",
                      "inputs": {"text": negative, "clip": ["loader", 1]}},
        "latent": {"class_type": "EmptyLatentImage",
                   "inputs": {"width": width, "height": height, "batch_size": 1}},
        "sampler": {"class_type": "KSampler",
                    "inputs": {"seed": seed, "steps": steps, "cfg": 7.0,
                               "sampler_name": "euler", "scheduler": "normal",
                               "denoise": 1.0,
                               "positive": ["positive", 0], "negative": ["negative", 0],
                               "model": ["loader", 0], "latent_image": ["latent", 0]}},
        "decode": {"class_type": "VAEDecode",
                   "inputs": {"samples": ["sampler", 0], "vae": ["loader", 2]}},
        "save": {"class_type": "SaveImage",
                 "inputs": {"images": ["decode", 0], "filename_prefix": "sdxl_gen"}}
    }
    r = requests.post(f"{COMFYUI}/prompt", json={"prompt": workflow})
    pid = r.json()["prompt_id"]
    # 等待完成（轮询）
    for _ in range(30):
        time.sleep(2)
        hist = requests.get(f"{COMFYUI}/history/{pid}").json()
        if pid in hist:
            return f"{COMFYUI}/view?filename=sdxl_gen_00001_.png"
    return None
```

## 参数说明

| 参数 | 默认值 | 说明 |
|------|-------|------|
| `--prompt` | （必填） | 图片描述，越详细越好 |
| `--negative` | "blurry, low quality, distorted" | 反向提示词 |
| `--steps` | 20 | 采样步数，越高质量越好越慢 |
| `--seed` | 随机 | 种子，决定具体画面 |
| `--width` | 1024 | 宽度（8的倍数） |
| `--height` | 768 | 高度（8的倍数） |
| `--sampler` | euler | 采样器（euler/dpmpp_2m/lcm/ddim） |
| `--cfg` | 7.0 | CFG 强度（1-20） |
| `--output` | 自动 | 输出路径 |

## 快速参考：常用场景

| 场景 | 推荐参数 |
|------|---------|
| 写实风景/人物 | `--steps 25 --cfg 7 --sampler euler` |
| 动漫/插画风格 | `--steps 20 --cfg 8 --negative "写实, 照片"` |
| 快速草图/验证 | `--steps 4 --sampler lcm --cfg 1.0`（需要 LCM 模型） |
| 16:9 横幅图 | `--width 1280 --height 720` |

## 输出格式

生图完成后，脚本自动将图片保存到指定路径或 `/tmp/` 目录，并通过飞书发送图片消息给用户。

## 注意事项

- ComfyUI 服务必须已启动（`python3 main.py --port 8188`）
- RTX 3080 推荐分辨率 1024×768 以下，更高分辨率可能爆显存
- 生图过程约 18 秒，请提前告知用户等待
- 图片风格默认写实，如需特定风格在 prompt 中描述
