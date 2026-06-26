# ComfyUI DirectML AMD 🎨

Complete guide and fixes for running **ComfyUI** on **AMD GPUs** under Windows using **DirectML**.

## 🖥️ Supported Hardware

- **AMD Radeon RX 7000 Series** (RX 7900 XT/XTX/GRE, RX 7800, RX 7700, RX 7600)
- **AMD Radeon RX 6000 Series** (RX 6900/6800/6700/6600)
- **AMD Radeon RX 5000 Series** (limited support)
- **Minimum 8GB VRAM** (12GB+ recommended)

## ⚡ Quick Start

### 0. Customize Paths (Important!)

**Before running scripts**, update paths to match your setup:

- **Windows default:** `C:\ComfyUI`
- **Custom path:** Set `COMFYUI_PATH` environment variable
- **Scripts:** Edit `apply-directml-fixes.py` and `download-models.ps1` if needed

### 1. Install Python 3.12

ComfyUI requires Python 3.12 (DirectML has no wheels for Python 3.14):

```bash
# If you have newer Python, create .venv with 3.12
cd C:\ComfyUI
uv venv --python 3.12
```

### 2. Install DirectML

```bash
cd C:\ComfyUI
.venv\Scripts\python.exe -m pip install torch-directml --force-reinstall
```

### 3. Fix model_patcher.py

DirectML doesn't work with `comfy_aimdo` module. Open:
`ComfyUI\comfy\model_patcher.py`

**Line ~326:**
```python
# WRONG (original code):
aimdo_mem = comfy_aimdo.model_vbar.vbars_analyze()

# CORRECT (DirectML fix):
# [AMD DirectML] Disabled - comfy_aimdo not available
# aimdo_mem = comfy_aimdo.model_vbar.vbars_analyze()
aimdo_mem = 0
```

**Line ~1512:**
```python
# WRONG (original code):
vbar = comfy_aimdo.model_vbar.ModelVBAR(self.model_size() * 10, self.load_device.index)

# CORRECT (DirectML fix):
# [AMD DirectML] Disabled - comfy_aimdo not available
# vbar = comfy_aimdo.model_vbar.ModelVBAR(...)
vbar = None
```

### 4. Start ComfyUI

```bash
cd C:\ComfyUI
.venv\Scripts\python.exe main.py --directml --port 8188
```

## 📊 Performance Benchmarks

| Model | Resolution | Steps | Time (RX 7900 GRE) | VRAM |
|-------|-----------|-------|-------------------|------|
| SDXL Turbo | 1024×1024 | 1 | 30-60s | 8GB |
| SDXL Base | 1024×1024 | 20 | 5-10 min | 12GB |
| Juggernaut XL | 1024×1024 | 20 | 5-10 min | 12GB |
| Flux.1 schnell | 1024×1024 | 4 | 3-5 min | 14GB |

**Note:** DirectML is slower than CUDA/NVIDIA, but fully functional!

## 🎯 Recommended Models

### Downloaded Models (19.2 GB)
- ✅ **SDXL Turbo** (`sd_xl_turbo_1.0_fp16.safetensors`) - 6.6 GB
- ✅ **SDXL Base 1.0** (`sd_xl_base_1.0.safetensors`) - 6.0 GB  
- ✅ **Juggernaut XL v9** (`Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors`) - 6.6 GB

### Pending Download
- ⏳ **Flux.1 [schnell] FP8** - best quality for 16GB VRAM
- ⏳ **ACE-Step 1.5** - music with vocals
- ⏳ **Wan 2.1** - video generation

**Download models:**
```bash
cd C:\ComfyUI\models\checkpoints

# SDXL Turbo
curl -L -o sd_xl_turbo_1.0_fp16.safetensors "https://huggingface.co/stabilityai/sdxl-turbo/resolve/main/sd_xl_turbo_1.0_fp16.safetensors"

# Juggernaut XL
curl -L -o juggernautXL_v9.safetensors "https://huggingface.co/RunDiffusion/Juggernaut-XL-v9/resolve/main/Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors"
```

## ⚠️ Troubleshooting

### Error: `ModuleNotFoundError: No module named 'torch_directml'`

**Cause:** Python version incompatible (DirectML wheels only for 3.8-3.12)

**Solution:**
```bash
# Create .venv with Python 3.12
uv venv --python 3.12
.venv\Scripts\python.exe -m pip install torch-directml
```

### Error: `SyntaxError: invalid syntax` in model_patcher.py

**Cause:** Incorrectly commented code

**Solution:** Use exact fixes from section 3 above.

### Error: `Port 8188 is already in use`

**Cause:** ComfyUI already running

**Solution:**
```bash
# Kill running process
Get-Process python | Where-Object {$_.Path -like "*ComfyUI*"} | Stop-Process -Force

# Or use different port
.venv\Scripts\python.exe main.py --directml --port 8000
```

### Error: `Out of Memory`

**Cause:** Model or resolution too large

**Solution:**
- Reduce resolution (1024×1024 instead of 2048×2048)
- Use FP8 model versions
- Close other GPU-using applications

### ComfyUI crashes during generation

**Cause:** DirectML is unstable, occasionally crashes

**Solution:**
1. Restart ComfyUI server
2. Try fewer steps (1-4 instead of 20)
3. Use `--use-split-cross-attention` flag

## 🔧 OpenClaw Integration

For use with OpenClaw:

1. **Set port in config:**
```json
{
  "plugins": {
    "entries": {
      "comfy": {
        "config": {
          "baseUrl": "http://127.0.0.1:8188"
        }
      }
    }
  }
}
```

2. **Generate images:**
```bash
# Via image_generate tool
image_generate(
  prompt="A cute squirrel on a tree branch",
  model="comfy/workflow",
  size="1024x1024"
)
```

## 📚 Additional Resources

- [ComfyUI GitHub](https://github.com/comfyanonymous/ComfyUI)
- [DirectML Documentation](https://learn.microsoft.com/en-us/windows/ai/directml/)
- [AMD ROCm Blogs](https://rocm.blogs.amd.com/)
- [CivitAI Models](https://civitai.com/)

## 🤝 Contributing

If you find better solutions or fixes, open an issue or PR!

---

**Author:** Klepeto 🦞 (vilda)  
**Version:** 1.0.0  
**Date:** 2026-05-07  
**License:** MIT-0
