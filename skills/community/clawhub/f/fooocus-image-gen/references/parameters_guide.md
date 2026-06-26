# Fooocus Parameters Guide

Complete reference for all Fooocus generation parameters.

## Basic Parameters

### Prompt (Positive)
- **Type:** String
- **Description:** Main description of what to generate
- **Tips:**
  - Be descriptive but concise
  - Fooocus has built-in prompt enhancement (GPT-2 based)
  - Use weights: `(keyword:1.5)` to emphasize
  - Use embeddings: `(embedding:filename:1.1)`

### Negative Prompt
- **Type:** String
- **Default:** `""` (empty)
- **Description:** What to avoid in the image
- **Common values:**
  - `"blurry, low quality, distorted"`
  - `"nsfw, nude"` (for safe generation)
  - `"text, watermark, signature"`

## Image Dimensions

### Width & Height
- **Type:** Integer
- **Default:** 1024 x 1024
- **Common sizes:**
  | Aspect | Width | Height | Use Case |
  |--------|-------|--------|----------|
  | 1:1 | 1024 | 1024 | General, social media |
  | 4:3 | 1024 | 768 | Standard photo |
  | 3:4 | 768 | 1024 | Portrait photo |
  | 16:9 | 1024 | 576 | Widescreen, video |
  | 9:16 | 576 | 1024 | Mobile, stories |
  | 21:9 | 1024 | 448 | Ultrawide, cinematic |

**Note:** SDXL works best at ~1024px. Avoid sizes >1536px without upscaling.

## Quality Parameters

### Performance / Quality Setting
- **Type:** String
- **Options:**
  - `"Speed"` - Fast generation (~8 steps)
  - `"Quality"` - Balanced (~30 steps)
  - `"Extreme"` - Best quality (~60 steps)

### Sampling Steps
- **Type:** Integer
- **Range:** 1-200
- **Default:** Auto (based on quality setting)
- **Guidelines:**
  - 4-8 steps: Fast, draft quality
  - 20-30 steps: Good quality
  - 50-100 steps: Best quality (diminishing returns)

### Sampling Method (Sampler)
- **Type:** String
- **Default:** `"dpmpp_2m_sde_gpu"`
- **Options:**
  - `dpmpp_2m_sde_gpu` - Best quality, GPU accelerated
  - `dpmpp_2m_sde` - CPU fallback
  - `euler` - Fast, simple
  - `euler_ancestral` - More varied results
  - `lcm` - For LCM models (very fast)

### Scheduler
- **Type:** String
- **Default:** `"karras"`
- **Options:**
  - `karras` - Recommended, smooth transitions
  - `normal` - Standard schedule
  - `simple` - Linear schedule
  - `exponential` - Aggressive noise schedule

## Guidance & Control

### Guidance Scale (CFG)
- **Type:** Float
- **Range:** 1.0 - 30.0
- **Default:** 4.0
- **Effect:**
  - Low (1-3): More creative, less prompt adherence
  - Medium (4-7): Balanced
  - High (8-15): Strict prompt following, may over-saturate
  - Very High (15+): Often degrades quality

### Sharpness
- **Type:** Float
- **Range:** 0.0 - 30.0
- **Default:** 2.0
- **Effect:**
  - 0-2: Soft, smooth images
  - 2-5: Balanced (default)
  - 5-10: Sharper details
  - 10-20: Very sharp, may add artifacts
  - 20-30: Extreme sharpness

**Note:** Unlike CFG, sharpness doesn't affect composition - only detail clarity.

## Seed & Randomization

### Seed
- **Type:** Integer
- **Default:** -1 (random)
- **Range:** -1 or 0 to 2^32-1
- **Usage:**
  - `-1`: Random seed each time
  - Fixed number: Reproducible results
  - Same seed + same parameters = same image

### Randomize Seed
- **Type:** Boolean
- **Default:** True
- **Effect:** When true, uses random seed (-1)

## Style Parameters

### Styles
- **Type:** Array of strings
- **Default:** `["Fooocus V2"]`
- **Available styles:**

#### Enhancement Styles
- `Fooocus V2` - GPT-2 based prompt enhancement
- `Fooocus Enhance` - General quality boost
- `Fooocus Sharp` - Sharpness enhancement

#### Photography Styles
- `Fooocus Photographic` - Photo-realistic
- `Fooocus Cinematic` - Movie/film look
- `Fooocus Analog Film` - Film photography

#### Artistic Styles
- `Fooocus Fantasy Art` - Fantasy illustration
- `Fooocus Neonpunk` - Cyberpunk neon
- `Fooocus Line Art` - Line drawing
- `Fooocus Craft Clay` - Claymation look

#### SAI Styles
- `SAI Anime` - Anime style
- `SAI Digital Art` - Digital painting
- `SAI 3D Model` - 3D rendered look
- `SAI Cinematic` - Cinematic composition

**Note:** Multiple styles can be combined.

## Advanced Parameters

### Refiner

#### Refiner Switch At
- **Type:** Float
- **Range:** 0.0 - 1.0
- **Default:** 0.5
- **Description:** When to switch to refiner model (as fraction of steps)

#### Refiner Model
- **Type:** String
- **Default:** None (disabled)
- **Description:** Model for refinement pass
- **Common:** `sd_xl_refiner_1.0.safetensors`

### Image Prompt (IP-Adapter)

#### Input Image
- **Type:** Base64 string or null
- **Description:** Reference image for style/composition

#### Input Mask
- **Type:** Base64 string or null
- **Description:** Mask for inpainting (white = inpaint area)

#### Image Prompt Weight
- **Type:** Float
- **Range:** 0.0 - 2.0
- **Default:** 1.0
- **Effect:** Strength of image influence

### ControlNet

#### ControlNet Model
- **Type:** String
- **Options:**
  - `canny` - Edge detection
  - `depth` - Depth map
  - `openpose` - Pose detection
  - `scribble` - Scribble/sketch

#### ControlNet Weight
- **Type:** Float
- **Range:** 0.0 - 2.0
- **Default:** 0.8

## Performance Parameters

### Number of Images
- **Type:** Integer
- **Range:** 1-32
- **Default:** 1
- **Note:** Higher numbers take longer

### Batch Size
- **Type:** Integer
- **Default:** 1
- **Note:** Actual batching handled automatically

## Preset-Specific Parameters

### Default Preset
```json
{
  "checkpoint": "juggernautXL_v8Rundiffusion.safetensors",
  "steps": 30,
  "cfg": 4.0,
  "sampler": "dpmpp_2m_sde_gpu",
  "scheduler": "karras"
}
```

### Anime Preset
```json
{
  "checkpoint": "animaPencilXL_v100.safetensors",
  "steps": 30,
  "cfg": 7.0,
  "recommended_styles": ["SAI Anime"]
}
```

### Realistic Preset
```json
{
  "checkpoint": "realisticStockPhoto_v10.safetensors",
  "steps": 40,
  "cfg": 3.0,
  "recommended_styles": ["Fooocus Photographic"]
}
```

### LCM Preset
```json
{
  "checkpoint": "sd_xl_base_1.0.safetensors",
  "steps": 8,
  "cfg": 1.5,
  "sampler": "lcm"
}
```

### Lightning Preset
```json
{
  "checkpoint": "sd_xl_lightning_4step.safetensors",
  "steps": 4,
  "cfg": 1.0
}
```

## Parameter Combinations

### For Photorealism
```json
{
  "preset": "realistic",
  "sharpness": 2.0,
  "guidance": 3.0,
  "steps": 40,
  "styles": ["Fooocus Photographic"]
}
```

### For Anime
```json
{
  "preset": "anime",
  "sharpness": 2.0,
  "guidance": 7.0,
  "steps": 30,
  "styles": ["SAI Anime"]
}
```

### For Fast Drafts
```json
{
  "preset": "lightning",
  "steps": 4,
  "guidance": 1.0,
  "quality": "speed"
}
```

### For Maximum Quality
```json
{
  "preset": "default",
  "steps": 60,
  "guidance": 4.0,
  "sharpness": 2.0,
  "quality": "extreme",
  "refiner_switch": 0.8,
  "refiner_model": "sd_xl_refiner_1.0.safetensors"
}
```

## Troubleshooting Parameters

### Out of Memory
- Reduce width/height
- Use `--always-low-vram` flag
- Reduce batch size
- Use `lcm` or `lightning` preset

### Slow Generation
- Use `lightning` preset (4 steps)
- Reduce steps to 20-30
- Use `speed` quality setting
- Ensure CUDA is being used

### Poor Quality
- Increase steps to 40-60
- Adjust sharpness (2-5 range)
- Try different samplers
- Use refiner model
- Check `Fooocus Enhance` style

### Not Following Prompt
- Increase guidance (6-10)
- Use `Fooocus V2` style
- Be more specific in prompt
- Use prompt weights

## Command Line Flags

When starting Fooocus:

```bash
# Performance
--always-low-vram          # For GPUs with <6GB VRAM
--always-high-vram         # For GPUs with >12GB VRAM
--disable-xformers         # Disable xformers optimization

# Network
--listen                   # Allow external connections
--port 7865               # Change port
--share                   # Create public Gradio link

# Models
--preset anime            # Use anime preset
--checkpoint model.safetensors  # Override model

# Features
--disable-preset-selection # Disable preset dropdown
--disable-image-log       # Don't save generation log
```
