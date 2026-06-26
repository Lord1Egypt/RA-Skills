# ComfyUI DirectML AMD Skill 🎨

## Description

Skill for setting up and optimizing **ComfyUI** on **AMD GPUs** under Windows using **DirectML**. Provides guides, fixes, and ready-to-use configurations for local image, music, and video generation.

## When to Use This Skill

Use this skill when:
- You have an **AMD GPU** (RX 7000/6000/5000 series) and want to run ComfyUI
- You're getting errors with `torch_directml` module
- You need to fix `model_patcher.py` for DirectML compatibility
- You want to know which models are compatible with your VRAM
- You're looking for AMD GPU performance benchmarks

## Installation

```bash
# 1. Install skill
clawhub install comfyui-directml-amd

# 2. Navigate to directory
cd C:\ComfyUI

# 3. Create Python 3.12 environment (if not already done)
uv venv --python 3.12

# 4. Install DirectML
.venv\Scripts\python.exe -m pip install torch-directml --force-reinstall

# 5. Apply fixes (automated by this skill)
python apply-directml-fixes.py

# 6. Start ComfyUI
.venv\Scripts\python.exe main.py --directml --port 8188
```

## Tools

### `apply-directml-fixes.py`
Automatically applies all necessary DirectML fixes:
- Fixes `comfy\model_patcher.py` (2 locations)
- Creates backups of original files
- Verifies functionality after application

### `download-models.ps1`
Downloads recommended models:
- SDXL Turbo (6.6 GB)
- SDXL Base 1.0 (6.0 GB)
- Juggernaut XL v9 (6.6 GB)
- Optional: Flux.1, ACE-Step, Wan 2.1

### `benchmark.py`
Tests performance with different models and settings:
- Measures generation time
- Monitors VRAM usage
- Compares with CUDA references

## Configuration

### Minimum Requirements
- **GPU:** AMD Radeon with 8GB+ VRAM
- **OS:** Windows 10/11 64-bit
- **Python:** 3.12 (DirectML has no wheels for 3.13+)
- **VRAM:** 8GB minimum, 12GB+ recommended

### Recommended Settings
```bash
# For 16GB VRAM (RX 7900 GRE/XTX)
python main.py --directml --port 8188 --max-memory 16384

# For 12GB VRAM (RX 7800/6800)
python main.py --directml --port 8188 --max-memory 12288 --use-split-cross-attention

# For 8GB VRAM (RX 7600/6600)
python main.py --directml --port 8188 --max-memory 8192 --lowvram
```

## Performance Benchmarks (RX 7900 GRE 16GB)

| Model | Resolution | Steps | Time | Quality |
|-------|-----------|-------|------|---------|
| SDXL Turbo | 1024² | 1 | 30-60s | Good |
| SDXL Base | 1024² | 20 | 5-10 min | Very Good |
| Juggernaut XL | 1024² | 20 | 5-10 min | Excellent |
| Flux.1 schnell | 1024² | 4 | 3-5 min | Best |

**Note:** DirectML is ~2-3x slower than CUDA on comparable NVIDIA GPU, but **fully functional**!

## Common Errors and Solutions

### `ModuleNotFoundError: torch_directml`
**Solution:** Python 3.14 is too new → create .venv with Python 3.12

### `SyntaxError` in model_patcher.py
**Solution:** Skill automatically applies fixes, or use `apply-directml-fixes.py`

### `Port already in use`
**Solution:** ComfyUI already running → kill process or use different port

### `Out of Memory`
**Solution:** Reduce resolution, use FP8 models, or add `--lowvram` flag

### `ComfyUI crash during generation`
**Solution:** DirectML is unstable → restart server, try fewer steps

## OpenClaw Integration

Skill is compatible with OpenClaw `comfy` plugin:

```json
{
  "plugins": {
    "entries": {
      "comfy": {
        "enabled": true,
        "config": {
          "baseUrl": "http://127.0.0.1:8188",
          "image": {
            "workflowPath": "comfy-workflows/image-generation.json"
          }
        }
      }
    }
  }
}
```

## References

- [ComfyUI Official](https://github.com/comfyanonymous/ComfyUI)
- [DirectML Docs](https://learn.microsoft.com/en-us/windows/ai/directml/)
- [AMD ROCm](https://rocm.blogs.amd.com/)

## Author

**Klepeto 🦞** (vilda)  
Tested on: AMD Radeon RX 7900 GRE 16GB, Windows 11

## License

MIT-0 - Free to use, modify, and redistribute without attribution.

## Changelog

### 1.0.0 (2026-05-07)
- Initial release
- Complete AMD DirectML setup guide
- Automatic model_patcher.py fixes
- Benchmark scripts
- Model download scripts
- OpenClaw integration
