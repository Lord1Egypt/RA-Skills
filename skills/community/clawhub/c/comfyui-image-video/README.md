# ComfyUI 本地部署 — 完整指南

> 基于 RTX 5080 16GB + Ubuntu，国内网络环境（HuggingFace 不通，使用 ModelScope 魔搭）

---

## 1. 环境准备

```bash
# 系统
# Ubuntu, RTX 5080 16GB, i9-14900KF, 62GB RAM
# Python 3.12

# 创建 Python 虚拟环境
python3 -m venv ~/comfyui-venv
source ~/comfyui-venv/bin/activate

# 安装 PyTorch (cu128 适配 RTX 5080)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
```

**注意：** RTX 50 系列需要 cu128 或更新的 CUDA 版本，cu126 不识别 GPU。

---

## 2. 安装 ComfyUI

```bash
cd ~
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
pip install -r requirements.txt
```

### 测试启动

```bash
cd ~/ComfyUI && \
LD_LIBRARY_PATH=~/comfyui-venv/lib/python3.12/site-packages/nvidia/cuda_runtime/lib:$LD_LIBRARY_PATH \
~/comfyui-venv/bin/python main.py --listen 127.0.0.1 --port 8188
```

成功后访问 `http://127.0.0.1:8188` 确认 GUI 可用。

---

## 3. 下载 Flux 文生图模型

从 ModelScope 下载（国内网络可用）：

```bash
cd ~/ComfyUI

# 创建目录
mkdir -p models/unet models/vae models/clip

# 下载 Flux1-schnell（使用 ModelScope Python API）
python3 -c "
from modelscope.hub.file_download import model_file_download
import os

# UNet (23.8GB)
src = model_file_download('AI-ModelScope/FLUX.1-schnell', 'flux1-schnell.safetensors')
os.symlink(src, 'models/unet/flux1-schnell.safetensors')

# VAE (335MB)
src = model_file_download('AI-ModelScope/FLUX.1-schnell', 'ae.safetensors')
os.symlink(src, 'models/vae/ae.safetensors')

# CLIP-L (250MB)
src = model_file_download('comfyanonymous/flux_text_encoders', 'clip_l.safetensors')
os.symlink(src, 'models/clip/clip_l.safetensors')

# T5-XXL (9.8GB)
src = model_file_download('comfyanonymous/flux_text_encoders', 't5xxl_fp16.safetensors')
os.symlink(src, 'models/clip/t5xxl_fp16.safetensors')
"
```

---

## 4. 配置 ComfyUI 系统服务

```bash
cat > ~/.config/systemd/user/comfyui.service << 'EOF'
[Unit]
Description=ComfyUI Image Generation Server
After=graphical.target

[Service]
Type=simple
WorkingDirectory=/home/vincent/ComfyUI
Environment=LD_LIBRARY_PATH=/home/vincent/comfyui-venv/lib/python3.12/site-packages/nvidia/cuda_runtime/lib:/usr/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu/nvidia
ExecStart=/home/vincent/comfyui-venv/bin/python main.py --listen 127.0.0.1 --port 8188
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable --now comfyui.service
```

---

## 5. 测试文生图

```bash
curl -X POST http://127.0.0.1:8188/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt": {... Flux workflow ...}}'

# 或使用 OpenClaw 技能脚本
~/.openclaw/plugin-skills/comfyui/scripts/generate.py image \
  --prompt "A cat on the moon" \
  --output /tmp/test.png
```

---

## 6. 下载 Wan2.1 视频生成模型

### 6.1 更新 ComfyUI

ComfyUI 0.22.0+ 原生支持 Wan2.1：

```bash
cd ~/ComfyUI && git pull
pip install -r requirements.txt
```

### 6.2 下载模型文件

```bash
cd ~/ComfyUI
mkdir -p models/diffusion_models models/text_encoders

python3 -c "
from modelscope.hub.file_download import model_file_download
import os

# 1. T2V-1.3B 扩散模型 (5.3GB)
src = model_file_download('Wan-AI/Wan2.1-T2V-1.3B', 'diffusion_pytorch_model.safetensors')
os.symlink(src, 'models/diffusion_models/wan2.1_t2v_1.3B_bf16.safetensors')

# 2. Wan2.1 VAE (485MB)
src = model_file_download('Wan-AI/Wan2.1-T2V-1.3B', 'Wan2.1_VAE.pth')
os.symlink(src, 'models/vae/wan2.1_vae.pth')

# 3. UMT5-XXL 文本编码器 — 注意：需要 ComfyUI 兼容格式
# ModelScope 原始格式不兼容 ComfyUI，需要下载 Comfy-Org 打包版本
# 从 hf-mirror.com 下载：
"

# 下载 ComfyUI 兼容格式的 UMT5-XXL 文本编码器
export HF_ENDPOINT=https://hf-mirror.com
python3 -c "
from huggingface_hub import hf_hub_download
path = hf_hub_download('Comfy-Org/Wan_2.1_ComfyUI_repackaged',
    'split_files/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors')
print(f'Downloaded: {path}')
"

# 链接
ln -sf ~/.cache/huggingface/hub/models--Comfy-Org--Wan_2.1_ComfyUI_repackaged/snapshots/*/split_files/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors \
  models/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors

# 4. CLIP vision 编码器（I2V 用，4.5GB）
python3 -c "
from modelscope.hub.file_download import model_file_download
import os
src = model_file_download('Wan-AI/Wan2.1-I2V-14B-480P',
    'models_clip_open-clip-xlm-roberta-large-vit-huge-14.pth')
os.symlink(src, 'models/clip/open_clip_xlm_roberta_large_vit_huge_14.pth')
"
```

### 关键注意事项

⚠️ **ModelScope 下载的 `models_t5_umt5-xxl-enc-bf16.pth` 是原始 PyTorch 格式，ComfyUI 无法直接使用。**
必须下载 Comfy-Org 打包的 `umt5_xxl_fp8_e4m3fn_scaled.safetensors` 格式。

⚠️ **hf-mirror.com 下载可能较慢或不稳定**，建议：
- 保持网络畅通
- 如果失败可重试
- ModelScope 上目前还没有 Comfy-Org 的镜像

---

## 7. 安装视频输出依赖

```bash
pip install imageio imageio-ffmpeg
```

这些用于将 ComfyUI 生成的帧序列 PNG 合成为 MP4 视频。

---

## 8. 测试文生视频 (T2V)

```bash
~/.openclaw/plugin-skills/comfyui/scripts/generate.py t2v \
  --prompt "A red sports car driving on a mountain road at sunset" \
  --length 49 \
  --wait 300
```

预期：生成 49 帧 832×480 PNG 图片，约需 2-3 分钟。

### 合成 MP4

```bash
python3 -c "
import imageio.v2 as iio, glob, os
files = sorted(glob.glob('~/ComfyUI/output/WanT2V_*.png'))
writer = iio.get_writer('output.mp4', fps=16, codec='libx264', quality=8, macro_block_size=1)
for f in files:
    writer.append_data(iio.imread(f))
writer.close()
print(f'Saved: {os.path.getsize(\"output.mp4\")/1e6:.1f}MB')
"
```

---

## 9. 测试图生视频 (I2V)

```bash
# 先将输入图片放到 ComfyUI input 目录
cp input_image.png ~/ComfyUI/input/

~/.openclaw/plugin-skills/comfyui/scripts/generate.py i2v \
  --prompt "gentle wave motion, water flowing" \
  --image ~/ComfyUI/input/input_image.png \
  --length 33 \
  --wait 300
```

I2V 使用 T2V-1.3B 模型 + `WanImageToVideo` 节点，传入 `start_image` 参数。

---

## 10. 模型文件清单

| 用途 | 文件 | 大小 | 位置 |
|------|------|------|------|
| Flux UNet | flux1-schnell.safetensors | 23.8GB | models/unet/ |
| Flux VAE | ae.safetensors | 335MB | models/vae/ |
| Flux CLIP-L | clip_l.safetensors | 250MB | models/clip/ |
| Flux T5-XXL | t5xxl_fp16.safetensors | 9.8GB | models/clip/ |
| **Wan2.1 UNet** | wan2.1_t2v_1.3B_bf16.safetensors | 5.3GB | models/diffusion_models/ |
| **Wan2.1 VAE** | wan2.1_vae.pth | 485MB | models/vae/ |
| **UMT5-XXL** | umt5_xxl_fp8_e4m3fn_scaled.safetensors | 6.1GB | models/text_encoders/ |
| **CLIP vision** | open_clip_xlm_roberta_large_vit_huge_14.pth | 4.5GB | models/clip/ |

---

## 11. 常见问题

### Q: 启动报 `libcudart.so` 找不到
设置 `LD_LIBRARY_PATH` 包含 `nvidia/cuda_runtime/lib`。

### Q: GPU 不被识别
确认 PyTorch 是 cu128 版本，RTX 50 系列需要 CUDA 12.8+。

### Q: 显存不足 (OOM)
- 图片：使用 fp8 权重（已默认）
- 视频：减少 `--length` 或分辨率

### Q: 视频生成慢
T2V-1.3B 在 RTX 5080 上约 3-4 秒/帧，49 帧需 2-3 分钟，属正常。

### Q: HuggingFace 下不了
- 用 hf-mirror.com：`export HF_ENDPOINT=https://hf-mirror.com`
- 优先用 ModelScope 国内源

---

## 12. API 参考

| 端点 | 方法 | 用途 |
|------|------|------|
| `/prompt` | POST | 提交工作流 |
| `/history/{id}` | GET | 查询生成状态 |
| `/system_stats` | GET | 服务器/GPU 状态 |
| `/view?filename=...` | GET | 获取输出文件 |
| `/upload/image` | POST | 上传图片 |

---

## 13. OpenClaw 技能集成

技能目录：`~/.openclaw/plugin-skills/comfyui/`

```
comfyui/
├── SKILL.md              # 技能定义（功能说明 + 参数）
├── scripts/
│   └── generate.py       # 生成脚本（image/t2v/i2v 三种模式）
└── references/
    └── models.md         # 模型参考文档
```

使用方式（OpenClaw 内部）：

```
Generate an image of a cat on the moon
→ 触发 comfyui 技能 → generate.py image --prompt "..."

Generate a video of a car driving
→ 触发 comfyui 技能 → generate.py t2v --prompt "..."
```
