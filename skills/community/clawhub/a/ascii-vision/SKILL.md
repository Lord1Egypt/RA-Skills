---
name: ascii-vision
description: "Fallback image viewer when vision models are unavailable. Converts images to ASCII art via ffmpeg + Python for brightness distribution, texture analysis, edge detection, and color sampling — without any vision API."
version: 1.2.0
author: chdlc
license: MIT-0
metadata:
  openclaw:
    requires:
      bins:
        - ffmpeg
        - python3
  hermes:
    tags: [vision, ascii, fallback, image, diagnostic, analysis]
    related_skills: [ascii-art, hyperframes]
    category: creative
---

# ASCII Vision

Fallback image viewer when vision models are unavailable (rate limited, model down, no provider configured, etc.). Converts images to **ASCII art** using ffmpeg + Python so you (or the agent) can identify visual content — shapes, brightness distribution, textures, and structure — without relying on any vision API.

Also includes **color sampling** via raw pixel extraction for basic hue identification, and **edge detection** for texture quantification.

## When to Use

- `image`/`vision_analyze` returns rate limit, model unavailable, or timeout errors
- You need to quickly distinguish between similar-looking images ("is this a dark variant of the same composition?")
- The agent needs visual inspection but no vision provider is configured
- Debugging image generation output — check if an image was actually produced before sending it to the user
- Quantitatively comparing two images (brightness, edges, color)

## How It Works

1. **ffmpeg** scales the image to a low resolution (e.g. 60 columns) in grayscale, preserving aspect ratio
2. **ascii_viewer.py** maps each pixel (0–255) to an ASCII character
3. Optional **`--stats`** outputs brightness average, pixel distribution, and unique levels
4. Optional **`--edges`** detects sharp transitions (edges) for texture quantification
5. **Color sampling** via `ffmpeg + xxd` extracts RGB hex values from specific regions

### Character Map

| Range   | Char | Meaning       |
|---------|------|---------------|
| 0–25    | ` `  | Pure black    |
| 26–51   | `.`  | Very dark     |
| 52–76   | `:`  | Dark          |
| 77–102  | `-`  | Mid-dark      |
| 103–127 | `=`  | Medium        |
| 128–153 | `+`  | Mid-light     |
| 154–179 | `*`  | Light         |
| 180–204 | `#`  | Very light    |
| 205–229 | `%`  | Near white    |
| 230–255 | `@`  | Pure white    |

## Setup

The bundled script is at `scripts/ascii_viewer.py`. Reference it relative to the skill directory:

```bash
SCRIPT=scripts/ascii_viewer.py
```

It accepts optional `--width` (default: 60) for columns. When paired with ffmpeg's `scale=W:-1`, height is auto-detected from the pixel data, preserving aspect ratio without distortion.

**Requirements:**
- `ffmpeg` (with rawvideo support — `which ffmpeg`)
- `python3`

## Usage

### Basic ASCII Conversion

```bash
# Default 60 columns (auto-height, aspect ratio preserved)
ffmpeg -y -i <image> -vf "scale=60:-1,format=gray" -frames:v 1 -f rawvideo pipe: 2>/dev/null \
  | python3 scripts/ascii_viewer.py

# Custom width
ffmpeg -y -i <image> -vf "scale=80:-1,format=gray" -frames:v 1 -f rawvideo pipe: 2>/dev/null \
  | python3 scripts/ascii_viewer.py --width 80
```

### With Statistics and Edge Detection

```bash
ffmpeg -y -i <image> -vf "scale=60:-1,format=gray" -frames:v 1 -f rawvideo pipe: 2>/dev/null \
  | python3 scripts/ascii_viewer.py --stats --edges

# Example output:
# brightness_avg=142/255
# bright_pixels=1200
# dark_pixels=800
# unique_levels=180
# edges_detected=400/3600
```

### Color Sampling (No Python Needed)

```bash
# Overall average color (RGB hex)
ffmpeg -y -i <image> -vf "scale=1:1,format=rgb24" -frames:v 1 -f rawvideo pipe: 2>/dev/null \
  | xxd -p | head -c 6

# Specific region (e.g. bottom-center quarter)
ffmpeg -y -i <image> -vf "crop=iw/2:ih/4:iw/4:3*ih/4,scale=1:1,format=rgb24" -frames:v 1 -f rawvideo pipe: 2>/dev/null \
  | xxd -p
```

### Batch Scan Multiple Images

```bash
for f in *.jpg; do
    echo "=== $f ==="
    ffmpeg -y -i "$f" -vf "scale=60:-1,format=gray" -frames:v 1 -f rawvideo pipe: 2>/dev/null \
      | python3 scripts/ascii_viewer.py --stats
    echo ""
done
```

### Recommended Widths

| Width | Use case                              |
|-------|---------------------------------------|
| 40    | Quick scan, simple images             |
| 60    | Balanced readability vs detail (default) |
| 80    | More detail, complex images           |
| 120   | Maximum detail (may be too wide for chat) |

## Interpreting the Output

### Overall Brightness

- **Many `@%#`** → bright scene, well-lit
- **Many `.-:`** → dark scene, night-time
- **Top-to-bottom gradient** → directional lighting (lamp above, shadow below)

### Content Patterns

- **Clusters of `#%@`** → bright objects, light sources, highlights
- **Vertical/horizontal lines of `-=`** → edges, furniture, structures
- **Organized patterns with mixed brightness** → text, diagrams, labeled elements
- **Heavy texture (`*#%@` intermixed)** → detailed surfaces (fabric, foliage, textured objects)
- **Flat bands with little variation** → night scenes, skies, plain backgrounds

### Distinguishing Image Types

- Bright top + textured center + dark bottom → product shot or figure with directional lighting
- Uniformly dark with sparse clusters → night scene, silhouettes
- Structured patterns with `+=-:#%@` formations → technical diagram, text overlay
- Same scene as another but with more detail/texture in a zone → variant with more content/elements

### Color Analysis Integration

Pair ASCII structural data with RGB color samples for richer diagnosis:

```bash
IMG="$1"

# 1. Original dimensions
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$IMG"

# 2. ASCII + stats + edges
ffmpeg -y -i "$IMG" -vf "scale=60:-1,format=gray" -frames:v 1 -f rawvideo pipe: 2>/dev/null \
  | python3 scripts/ascii_viewer.py --stats --edges

# 3. Color info
echo "Average color (RGB hex):"
ffmpeg -y -i "$IMG" -vf "scale=1:1,format=rgb24" -frames:v 1 -f rawvideo pipe: 2>/dev/null \
  | xxd -p | head -c 6

echo "Bottom region color:"
ffmpeg -y -i "$IMG" -vf "crop=iw/2:ih/4:iw/4:3*ih/4,scale=1:1,format=rgb24" -frames:v 1 -f rawvideo pipe: 2>/dev/null \
  | xxd -p
```

## Limitations

ASCII art is a **mechanical fallback** — it does NOT replace a vision model.

| Detects | Does NOT detect |
|---------|-----------------|
| Overall brightness (light vs dark scene) | Semantic meaning (what the subject is) |
| Contrast between regions | Color (everything is grayscale without xxd) |
| Texture (smooth vs detailed surface) | Legible text (only knows "something is there") |
| Lighting gradients (top-down, side, etc.) | Faces, emotions, or expressions |
| Edges and sharp transitions | Specific objects (person, cat, mask) |
| Spatial distribution of content | Depth, perspective, or real dimensions |

**Good for:**
- Checking if a generated image actually has content vs being blank
- Distinguishing between two variants of the same composition
- Detecting if there's text/detail in a specific region
- Confirming an image exists before sending it to the user
- Getting RGB color data from image regions

**Not good for:**
- Reading text (signs, screenshots, memes)
- Color-critical analysis (xxd helps but is coarse)
- Identifying objects, people, or animals
- Images with very fine detail (< 2–3 pixels wide)

ASCII gives you **structural data** (brightness, texture, edges), not semantics. Like looking at a photo with your eyes closed — you can feel light and shadow, but you can't name what you see.

## Common Pitfalls

1. **Brightness-only.** You cannot distinguish red from blue if they have the same luminance — color information is lost (use xxd color sampling for that)
2. **Too-low width** (e.g. 30) loses fine detail like small text. Stick to 60 minimum.
3. **Too-high width** (e.g. 120+) produces ASCII that is illegible in a chat context — too wide to display cleanly.
4. **Smooth gradients** render as solid bands of a single character. This is expected, not a bug.
5. **Not a vision replacement.** ASCII art is a fallback when vision is unavailable, not a substitute. Always prefer the real tool when it works.
6. **ffmpeg not installed.** Verify with `which ffmpeg` before attempting. Minimal Docker images may lack it.
7. **Manual height mismatch.** If you specify `--height` manually, it must match the ffmpeg `scale=W:H` output row count, or the ASCII will be misaligned.

## Verification Checklist

- [ ] ffmpeg is installed (`which ffmpeg`)
- [ ] Script at `scripts/ascii_viewer.py` exists and is executable
- [ ] Image path exists and is a valid image file
- [ ] Width is appropriate for the level of detail needed (60 default)
- [ ] Use `scale=W:-1` in ffmpeg to auto-preserve aspect ratio (or match `--height` if manual)
- [ ] Output shows recognizable patterns, not just noise


