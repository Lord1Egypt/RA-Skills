---
name: dashscope-imagegen
description: "Generate images using DashScope wan2.6-t2i model (通义万相). Use when user asks to generate/create images, illustrations, or visual content via DashScope/通义万相. Requires exec tool and DASHSCOPE_API_KEY."
---

# dashscope-imagegen

Generate images using Alibaba Cloud DashScope wan2.6-t2i model (通义万相 2.6).

## Usage

```bash
python3 ~/.openclaw/scripts/dashscope-imagegen.py "your prompt here" [options]
```

### Options
- `--size SIZE` — Image size, e.g. `1024*1024`, `1280*720`, `720*1280` (default: `1024*1024`)
- `-n N` — Number of images (default: 1)
- `--negative "text"` — Negative prompt
- `-o DIR` — Output directory (default: current dir)
- `--url-only` — Only print image URLs without downloading

### Examples

```bash
# Generate and download
python3 ~/.openclaw/scripts/dashscope-imagegen.py "一只可爱的橘猫坐在书桌上" -o /tmp

# URL only
python3 ~/.openclaw/scripts/dashscope-imagegen.py "sunset over mountains" --url-only --size 1280*720

# With negative prompt
python3 ~/.openclaw/scripts/dashscope-imagegen.py "professional headshot" --negative "cartoon, anime, low quality"
```

### Supported Sizes
Total pixels must not exceed ~1.5M. Common sizes:
- `1024*1024` (1:1)
- `1280*720` (16:9)
- `720*1280` (9:16)
- `1024*768` (4:3)
- `768*1024` (3:4)

### Environment
Requires `DASHSCOPE_API_KEY` environment variable (set in `~/.openclaw/.env`).

### Notes
- Async API: submits task, polls for completion (~10-20s)
- Output is PNG
- Chinese and English prompts both work well
- `prompt_extend` is enabled by default for better results
