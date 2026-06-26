# 💕 Ellya Skill

Ellya is a virtual companion skill for OpenClaw that helps you:
- 🧠 Set up character personality and appearance
- 👗 Learn and store visual styles from photos
- 📸 Generate selfies using prompts or learned styles
- 🎞️ Create multi-image photo series with AI-powered variations

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Install dependencies
uv sync

# Set API key
export GEMINI_API_KEY="your-api-key"
```

### 2. Initialize Character
On first run, Ellya will:
- Create `SOUL.md` from template (personality settings)
- Ask for a base appearance photo → save as `assets/base.png`

### 3. Learn Styles (Optional)
Upload reference photos to teach Ellya different styles:
```bash
uv run scripts/genai_media.py analyze photo.jpg beach_casual
```
This saves the style to `styles/beach_casual.md` for reuse.

### 4. Generate Images
```bash
# Single selfie with prompt
uv run scripts/genai_media.py generate -i assets/base.png -p "wearing a red dress"

# Single selfie with learned style
uv run scripts/genai_media.py generate -i assets/base.png -s beach_casual

# Photo series (3 variations)
uv run scripts/genai_media.py series -i assets/base.png -n 3
```

### 5. Send to User
After generation, send images via OpenClaw:
```bash
# For single images
openclaw message send --channel <channel> --target <target> --media output/ellya_12345.png

# For series
openclaw message send --channel <channel> --target <target> --media output/series_20260305_143022/02_ellya_0.png
openclaw message send --channel <channel> --target <target> --media output/series_20260305_143022/03_ellya_0.png
```

## 📖 Command Reference

### Style Learning
```bash
uv run scripts/genai_media.py analyze <image_path> [style_name]
```
- Analyzes an image and extracts style characteristics
- Saves to `styles/<style_name>.md`
- If `style_name` is omitted, AI generates one automatically

**Example:**
```bash
uv run scripts/genai_media.py analyze vacation_photo.jpg summer_beach
```

### Single Image Generation
```bash
# With text prompt
uv run scripts/genai_media.py generate -i <base_image> -p "<prompt>"

# With learned style
uv run scripts/genai_media.py generate -i <base_image> -s <style_name>

# Mix multiple styles (up to 3)
uv run scripts/genai_media.py generate -i <base_image> -s style1 -s style2 -s style3
```

**Examples:**
```bash
# Prompt-based
uv run scripts/genai_media.py generate -i assets/base.png -p "casual outfit at a cafe"

# Style-based
uv run scripts/genai_media.py generate -i assets/base.png -s beach_casual

# Mixed styles
uv run scripts/genai_media.py generate -i assets/base.png -s beach_casual -s sunset_vibes
```

**Output:** Images saved to `output/ellya_*.png`

### Photo Series Generation
```bash
uv run scripts/genai_media.py series -i <image_path> [-n <count>]
```
- Generates multiple variations from one reference image
- AI automatically classifies scene as "story" or "pose" mode
- **Story mode**: Creates narrative progression (different moments/activities)
- **Pose mode**: Creates technical variations (angles/postures/expressions)

**Parameters:**
- `-i`: Reference image path (required)
- `-n`: Number of images (default: 3, range: 1-10)
- `-v`: Custom variation prompts (optional, repeatable)

**Examples:**
```bash
# Generate 3 variations (default)
uv run scripts/genai_media.py series -i assets/base.png

# Generate 5 variations
uv run scripts/genai_media.py series -i assets/base.png -n 5

# Custom variations
uv run scripts/genai_media.py series -i assets/base.png -v "front-facing pose" -v "side profile"
```

**Output:** Images saved to `output/series_YYYYMMDD_HHMMSS/`

## 🎯 Usage Workflow

### For Skill Handler (Ellya)

#### When user says "take a selfie":
1. Check if styles exist in `styles/`
2. If yes: auto-select 1-3 styles and generate
3. If no: generate with default prompt
4. Send result to user via OpenClaw

#### When user says "make a photo set":
1. Run series generation: `uv run scripts/genai_media.py series -i assets/base.png -n 3`
2. Check output for directory path
3. Send all images in the series to user

#### When user uploads a style reference:
1. Save image temporarily
2. Run analysis: `uv run scripts/genai_media.py analyze <image_path> <style_name>`
3. Confirm style saved
4. Offer to generate a test image with the new style

### Sending Images to Users

**After any generation command:**
1. Check the script output for file paths
2. Use OpenClaw to send images:

```bash
# Single image
openclaw message send --channel <channel> --target <target> --media <image_path>

# Multiple images (series)
for image in output/series_*/0*.png; do
    openclaw message send --channel <channel> --target <target> --media "$image"
done
```

**Get channel and target from conversation context** - these are provided by OpenClaw runtime.

## 📁 File Structure

```
Ellya/
├── assets/base.*           # Active appearance reference
├── styles/                 # Learned styles (*.md files)
├── output/                 # Generated images
│   ├── ellya_*.png        # Single images
│   └── series_*/          # Photo series
├── SOUL.md                # Character personality
└── scripts/genai_media.py # Generation script
```

## 🗣️ Common User Requests

| User Says | Action |
|-----------|--------|
| "Take a selfie" | Generate with auto-selected styles |
| "Show me in [style]" | Generate using specific style |
| "Take a beach selfie" | Generate with scene prompt |
| "Make a photo set" | Generate series (3-5 images) |
| "Give me 6 different poses" | Generate series with `-n 6` |

## 🎨 How Series Generation Works

1. **Scene Analysis**: AI extracts environment, lighting, and character details
2. **Auto Classification**: 
   - **Story Mode**: For scenes with narrative potential (outdoor, locations)
   - **Pose Mode**: For controlled environments (studio, portraits)
3. **Variation Generation**: Creates N unique descriptions based on mode
4. **Image Generation**: Produces images maintaining character identity
5. **Output**: Saves to timestamped directory with base image copy

## 📦 Requirements

- Python 3.10+
- `uv` package manager
- `GEMINI_API_KEY` environment variable
- OpenClaw runtime (for skill hosting)
- `openclaw` CLI (for sending images)

## 💡 Tips

- **Style Library**: Build a diverse style collection for better results
- **Base Image**: Use a clear, well-lit photo for best generation quality
- **Series Count**: 3-5 images work best for most use cases
- **Custom Variations**: Use `-v` for specific poses you want

---

Ellya makes visual content generation smooth and fun! 💫
