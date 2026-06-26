# Fooocus Skill - Agent Quick Reference

## 🚀 One-Command Start

```bash
python scripts/check_env.py && python scripts/generate.py --prompt "your prompt here"
```

## 🎯 Decision Flow

```
User wants image generation
        ↓
Run check_env.py
        ↓
    ┌───┴───┐
   OK     Issues
    ↓        ↓
Generate  Guide User
          (see below)
```

## 🆘 User Guidance Scenarios

### 1. No GPU
**Say:**
```
⚠️  **No NVIDIA GPU Detected**

Your system can only run Fooocus in CPU mode, which is extremely slow (10-30 minutes per image).

**⚡ STRONGLY RECOMMENDED: Google Colab (Free GPU)**
- Speed: 10-30 seconds per image (100x faster than CPU)
- Cost: Free
- Setup: None, just open in browser
- Link: https://colab.research.google.com/github/lllyasviel/Fooocus/blob/main/fooocus_colab.ipynb

**Alternative: Hugging Face (Simplest)**
- Speed: 10-20 seconds per image
- Cost: Free tier
- Setup: None
- Link: https://huggingface.co/spaces/stabilityai/stable-diffusion-xl-base-1.0

---

**CPU Mode (NOT Recommended)**
⚠️  Warning: Very slow! Simple image takes 10-30 minutes
- Requires: 16GB RAM, 10GB disk space
- Setup time: 30-60 minutes (downloads models)
- Generate time: 10-30 minutes per image

**Which option do you prefer?**
1. Google Colab (Recommended ⭐)
2. Hugging Face (Simplest)
3. CPU Mode (Slow - only if no internet)
```

**If user chooses CPU mode despite warning:**
```
You chose CPU mode. Please be aware it will be very slow.

Let me set it up for you. This will:
1. Install PyTorch (~500MB download)
2. Install Fooocus (~6GB model download)
3. Take 30-60 minutes for first setup

Please confirm you want to proceed (yes/no):
```

### 2. PyTorch Not Installed
**Say:**
```
Fooocus needs PyTorch. Let me install it for you...
[Run: python scripts/check_env.py --install-deps]

If that doesn't work, run this command:
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### 3. Fooocus Not Installed
**Say:**
```
Fooocus is not installed. Let me set it up for you...
[Run: python scripts/check_env.py --install]

This will download about 6GB of models. It may take 10-30 minutes.
```

### 4. Fooocus Not Running
**Say:**
```
Fooocus needs to be started. Run these commands:

cd ~/Fooocus
python entry_with_update.py

Wait for "Running on local URL: http://127.0.0.1:7865"
Then let me know and I'll generate your image!
```

## 📝 Common Prompts

### Anime Style
```bash
python scripts/generate_with_progress.py \
  --prompt "masterpiece, best quality, 1girl, solo, [DESCRIPTION], anime style, detailed face" \
  --preset anime \
  --style "SAI Anime"
```

### Realistic Photo
```bash
python scripts/generate_with_progress.py \
  --prompt "professional photo, [DESCRIPTION], 50mm lens, f/1.8, sharp focus, photorealistic" \
  --preset realistic \
  --style "Fooocus Photographic"
```

### Fast Draft
```bash
python scripts/generate.py \
  --prompt "[DESCRIPTION]" \
  --preset lightning \
  --steps 4
```

## ⚡ Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| Out of memory | Add: `--width 512 --height 512` |
| Too slow | Add: `--preset lightning --steps 4` |
| Connection error | Start Fooocus: `cd ~/Fooocus && python entry_with_update.py` |
| Module not found | Run: `pip install torch gradio websockets requests Pillow` |
| Windows PowerShell error | Use `;` instead of `&&` between commands |

## 🎨 Style Presets

| Preset | Use For | Speed |
|--------|---------|-------|
| `anime` | Anime, manga, cartoons | Medium |
| `realistic` | Photos, portraits | Slow |
| `lightning` | Fast drafts | Very Fast |
| `default` | General purpose | Medium |

## 📐 Aspect Ratios

| Ratio | Dimensions | Best For |
|-------|------------|----------|
| `1:1` | 1024x1024 | Instagram, portraits |
| `16:9` | 1024x576 | Wallpaper, video |
| `9:16` | 576x1024 | Mobile, stories |
| `4:3` | 1024x768 | Classic photos |

## 🔧 Useful Commands

```bash
# Check everything
python scripts/check_env.py

# List all presets and styles
python scripts/list_models.py

# Generate with progress bar
python scripts/generate_with_progress.py --prompt "..."

# CPU mode (no GPU)
python scripts/generate.py --prompt "..." --cpu-optimize

# Install everything
python scripts/check_env.py --install-deps --install
```

## 💬 User Communication Templates

**Starting:**
> I'll help you generate images using Fooocus. Let me check your environment first...

**Ready:**
> ✅ Your system is ready! What would you like to create?

**Generating:**
> 🎨 Generating your image... This will take about [X] seconds.

**Complete:**
> ✅ Done! Here's your image. Would you like any variations or adjustments?

**Error:**
> ❌ I encountered an issue: [ERROR]. Let me help you fix it...

## ⚠️ Limitations to Mention

- **Requires NVIDIA GPU** for reasonable speed (CPU mode is 10-30 min/image!)
- **First run downloads 6-10GB** of models (takes 10-30 minutes)
- **Generation time:** 
  - GPU: 10-30 seconds per image
  - CPU: 10-30 minutes per image (NOT recommended)
- Windows may need PowerShell configuration

## 🚫 When NOT to Use CPU Mode

**Never offer CPU mode as first option. Only if:**
- User has no internet (can't use cloud)
- User explicitly insists after warning
- User wants to learn/setup locally regardless of speed

**Always lead with:**
1. Google Colab (Free, fast, no setup)
2. Hugging Face (Free, fast, no setup)
3. Local GPU (If they have hardware)
4. CPU Mode (Last resort with strong warning)

## 🌐 Cloud Alternatives (No Setup)

If local setup fails, suggest:
1. **Google Colab**: https://colab.research.google.com/github/lllyasviel/Fooocus/blob/main/fooocus_colab.ipynb
2. **Hugging Face**: https://huggingface.co/spaces/stabilityai/stable-diffusion-xl-base-1.0
3. **Replicate**: https://replicate.com/stability-ai/sdxl

## 📞 When to Escalate

Ask user for help when:
- CUDA driver installation needed
- System-level changes required
- Hardware upgrade needed
- Network issues prevent model downloads
- User wants cloud alternative setup
