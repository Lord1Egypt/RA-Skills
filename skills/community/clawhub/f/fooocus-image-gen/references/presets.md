# Fooocus Presets

Presets are pre-configured settings optimized for different use cases.

## Available Presets

### default
**General purpose SDXL generation**

```json
{
  "name": "Default",
  "checkpoint": "juggernautXL_v8Rundiffusion.safetensors",
  "checkpoint_url": "https://civitai.com/models/133005/juggernaut-xl",
  "description": "Versatile all-purpose model",
  "recommended_for": [
    "general photography",
    "landscapes",
    "portraits",
    "concept art",
    "digital art"
  ],
  "default_settings": {
    "steps": 30,
    "cfg": 4.0,
    "sampler": "dpmpp_2m_sde_gpu",
    "scheduler": "karras",
    "sharpness": 2.0
  },
  "recommended_styles": [
    "Fooocus V2",
    "Fooocus Enhance",
    "Fooocus Sharp"
  ]
}
```

**When to use:**
- General purpose generation
- When you're unsure which preset to use
- Balanced quality and speed
- Good starting point for beginners

---

### anime
**Optimized for anime and manga style**

```json
{
  "name": "Anime",
  "checkpoint": "animaPencilXL_v100.safetensors",
  "checkpoint_url": "https://civitai.com/models/198144",
  "description": "Specialized for anime/manga aesthetics",
  "recommended_for": [
    "anime characters",
    "manga style",
    "cartoon",
    "stylized characters",
    "chibi"
  ],
  "default_settings": {
    "steps": 30,
    "cfg": 7.0,
    "sampler": "dpmpp_2m_sde_gpu",
    "scheduler": "karras",
    "sharpness": 2.0
  },
  "recommended_styles": [
    "SAI Anime",
    "SAI Digital Art"
  ],
  "prompt_tips": [
    "Use anime-specific tags: 1girl, 1boy, solo",
    "Add quality tags: masterpiece, best quality",
    "Specify art style: anime style, manga style"
  ]
}
```

**When to use:**
- Anime character generation
- Manga-style illustrations
- Cartoon characters
- Stylized artwork

**Example prompts:**
```
masterpiece, best quality, 1girl, solo, school uniform, 
cherry blossoms, anime style, detailed face

masterpiece, best quality, 1boy, solo, spiky hair, 
action pose, dynamic angle, anime style
```

---

### realistic
**Photorealistic image generation**

```json
{
  "name": "Realistic",
  "checkpoint": "realisticStockPhoto_v10.safetensors",
  "checkpoint_url": "https://civitai.com/models/154593",
  "description": "Optimized for photorealistic results",
  "recommended_for": [
    "portraits",
    "product photography",
    "architectural visualization",
    "nature photography",
    "street photography"
  ],
  "default_settings": {
    "steps": 40,
    "cfg": 3.0,
    "sampler": "dpmpp_2m_sde_gpu",
    "scheduler": "karras",
    "sharpness": 2.0
  },
  "recommended_styles": [
    "Fooocus Photographic",
    "Fooocus Cinematic",
    "Fooocus Analog Film"
  ],
  "prompt_tips": [
    "Use photography terms: DSLR, 50mm lens, f/1.8",
    "Add lighting: soft lighting, golden hour, studio lighting",
    "Specify camera: Canon EOS R5, Nikon D850"
  ]
}
```

**When to use:**
- Portrait photography
- Product shots
- Architectural renders
- Nature photography
- Any photorealistic needs

**Example prompts:**
```
professional portrait, 50mm lens, f/1.8, soft lighting,
studio background, sharp focus, detailed skin texture

architectural photography, modern house, glass facade,
golden hour, dramatic sky, wide angle, 24mm lens
```

---

### lcm
**Fast generation using Latent Consistency Models**

```json
{
  "name": "LCM",
  "checkpoint": "sd_xl_base_1.0.safetensors",
  "description": "Very fast generation with LCM",
  "recommended_for": [
    "rapid prototyping",
    "draft generation",
    "batch processing",
    "real-time preview",
    "concept exploration"
  ],
  "default_settings": {
    "steps": 8,
    "cfg": 1.5,
    "sampler": "lcm",
    "scheduler": "karras",
    "sharpness": 2.0
  },
  "speed": "~4x faster than default",
  "quality": "Good for drafts, less detail than full generation"
}
```

**When to use:**
- Quick drafts and prototypes
- Testing prompts
- Batch generation
- When speed matters more than quality
- Low VRAM situations

---

### lightning
**Ultra-fast generation using SDXL Lightning**

```json
{
  "name": "Lightning",
  "checkpoint": "sd_xl_lightning_4step.safetensors",
  "checkpoint_url": "https://huggingface.co/ByteDance/SDXL-Lightning",
  "description": "Fastest generation, 4 steps",
  "recommended_for": [
    "real-time generation",
    "interactive use",
    "very fast drafts",
    "batch processing",
    "VRAM-constrained systems"
  ],
  "default_settings": {
    "steps": 4,
    "cfg": 1.0,
    "sampler": "euler",
    "scheduler": "karras",
    "sharpness": 2.0
  },
  "speed": "~8x faster than default",
  "quality": "Good for quick previews, less coherent than full generation"
}
```

**When to use:**
- Maximum speed needed
- Real-time applications
- Initial concept exploration
- Very limited VRAM

---

### playground_v2.5
**Playground AI's aesthetic model**

```json
{
  "name": "Playground v2.5",
  "checkpoint": "playground-v2.5-1024px-aesthetic.fp16.safetensors",
  "checkpoint_url": "https://huggingface.co/playgroundai/playground-v2.5-1024px-aesthetic",
  "description": "Aesthetic-focused generation",
  "recommended_for": [
    "artistic images",
    "social media content",
    "aesthetic photography",
    "creative projects",
    "visual art"
  ],
  "default_settings": {
    "steps": 30,
    "cfg": 3.0,
    "sampler": "dpmpp_2m_sde_gpu",
    "scheduler": "karras",
    "sharpness": 2.0
  },
  "recommended_styles": [
    "Fooocus V2",
    "Fooocus Enhance"
  ]
}
```

**When to use:**
- Artistic/aesthetic images
- Social media content
- Creative projects
- When you want visually pleasing results

---

### pony_v6
**Pony Diffusion model**

```json
{
  "name": "Pony v6",
  "checkpoint": "ponyDiffusionV6XL_v6StartWithThis.safetensors",
  "checkpoint_url": "https://civitai.com/models/257749",
  "description": "Versatile model with strong aesthetic",
  "recommended_for": [
    "anthropomorphic characters",
    "furry art",
    "stylized characters",
    "fantasy creatures",
    "creative character design"
  ],
  "default_settings": {
    "steps": 30,
    "cfg": 7.0,
    "sampler": "dpmpp_2m_sde_gpu",
    "scheduler": "karras",
    "sharpness": 2.0
  },
  "recommended_styles": [
    "Fooocus V2"
  ],
  "special_tags": [
    "score_9",
    "score_8_up",
    "score_7_up",
    "score_6_up",
    "score_5_up",
    "score_4_up"
  ]
}
```

**When to use:**
- Anthropomorphic characters
- Furry art
- Stylized character designs
- Fantasy creatures

**Special syntax:**
Pony v6 uses score tags for quality:
```
score_9, score_8_up, score_7_up, 1girl, anthro, 
detailed fur, expressive eyes
```

---

### sai
**Stable AI style collection**

```json
{
  "name": "SAI",
  "checkpoint": "sd_xl_base_1.0.safetensors",
  "description": "Base SDXL with SAI styles",
  "recommended_for": [
    "versatile generation",
    "style exploration",
    "general use",
    "testing different aesthetics"
  ],
  "default_settings": {
    "steps": 30,
    "cfg": 4.0,
    "sampler": "dpmpp_2m_sde_gpu",
    "scheduler": "karras",
    "sharpness": 2.0
  },
  "recommended_styles": [
    "SAI Anime",
    "SAI Digital Art",
    "SAI 3D Model",
    "SAI Cinematic"
  ]
}
```

**When to use:**
- Exploring different styles
- General purpose with style variety
- When you want to switch between looks

---

## Preset Comparison

| Preset | Speed | Quality | VRAM | Best For |
|--------|-------|---------|------|----------|
| default | Medium | High | 4GB+ | General use |
| anime | Medium | High | 4GB+ | Anime/manga |
| realistic | Medium | Very High | 4GB+ | Photos |
| lcm | Fast | Medium | 3GB+ | Drafts |
| lightning | Very Fast | Medium | 2GB+ | Quick previews |
| playground | Medium | High | 4GB+ | Aesthetic art |
| pony | Medium | High | 4GB+ | Anthro/furry |
| sai | Medium | High | 4GB+ | Style variety |

## Switching Presets

### In Web UI
1. Open Fooocus in browser
2. Click "Preset" dropdown in top-left
3. Select desired preset
4. Models will download automatically if needed

### Via Command Line
```bash
# Start with specific preset
python entry_with_update.py --preset anime

# Available: default, anime, realistic, lcm, lightning, playground_v2.5, pony_v6, sai
```

### Via API
```python
# Use preset checkpoint
payload = {
    "data": [
        "prompt",
        "",
        [],
        "Quality",
        1024, 1024,
        1, -1, 2.0, 4.0,
        "dpmpp_2m_sde_gpu",
        "karras",
        "animaPencilXL_v100.safetensors",  // Anime checkpoint
        None, None,
        False, None, None
    ]
}
```

## Custom Presets

Create custom presets in the `presets/` folder:

```json
{
  "default_model": "my_custom_model.safetensors",
  "default_refiner": "",
  "default_lora": "",
  "default_cfg_scale": 4.0,
  "default_sampler": "dpmpp_2m_sde_gpu",
  "default_scheduler": "karras",
  "default_steps": 30,
  "default_styles": ["Fooocus V2"],
  "default_aspect_ratio": "1:1"
}
```

Save as `presets/my_preset.json` and use with:
```bash
python entry_with_update.py --preset my_preset
```

## Preset Selection Guide

**I want to generate...**

- **Realistic photos** → `realistic` preset
- **Anime characters** → `anime` preset
- **Quick drafts** → `lightning` or `lcm` preset
- **Artistic images** → `playground_v2.5` preset
- **Furry/anthro** → `pony_v6` preset
- **Not sure** → `default` preset
- **Fastest possible** → `lightning` preset
- **Best quality** → `realistic` preset with increased steps
