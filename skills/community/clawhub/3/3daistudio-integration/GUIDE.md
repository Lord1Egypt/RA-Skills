# 3D AI Studio Skill — Usage Guide

> Convert images and text prompts to 3D models (.glb) using the 3D AI Studio API.
> Works with any AI agent, bot, or automation that can run Python and shell commands.

---

## Prerequisites

### 1. Credits (Required)

> ⚠️ **This skill costs credits per generation. You must have credits in your account before using it.**

- Sign up at https://www.3daistudio.com
- Purchase credits from the dashboard: https://www.3daistudio.com/Platform/API
- Minimum recommended balance: **60 credits** (enough for 1 Hunyuan Pro generation)
- Credits are **refunded automatically** if a job fails

| Model | Min Credits Needed |
|-------|--------------------|
| TRELLIS.2 (geometry only) | 15 |
| TRELLIS.2 (textured) | 25–55 |
| Hunyuan Rapid | 35–55 |
| Hunyuan Pro | 60–100 |

### 2. API Key (Required)

1. Log in to https://www.3daistudio.com/Platform/API
2. Generate an API key
3. Set it as an environment variable:

```bash
# Linux / macOS
export THREE_D_AI_STUDIO_API_KEY="your-key-here"

# Windows (PowerShell)
$env:THREE_D_AI_STUDIO_API_KEY = "your-key-here"

# Windows (CMD)
set THREE_D_AI_STUDIO_API_KEY=your-key-here
```

Or add it to a `.env` file (copy `.env.example`):
```
THREE_D_AI_STUDIO_API_KEY=your-key-here
```

### 3. Python (Required)

- Python 3.8+ required
- No external packages needed — uses only stdlib (`urllib`, `argparse`, `base64`, `json`)

---

## Installation

```bash
# Clone or download the skill folder
# Then navigate into it:
cd 3daistudio

# Verify setup
python 3daistudio.py balance
```

---

## Commands Reference

### `balance` — Check your credit balance

```bash
python 3daistudio.py balance
```

> Note: The correct endpoint is `/account/user/wallet/` — the official docs had a typo (`/user/wallet/`). This skill uses the correct path.

---

### `trellis` — Image to 3D (fastest, cheapest)

Best for: product shots, characters, objects from photos.

```bash
# Basic (geometry only, 1024 resolution)
python 3daistudio.py trellis --image photo.png -o model.glb

# With textures (recommended for colored models)
python 3daistudio.py trellis --image photo.png --textures -o model.glb

# High resolution with textures
python 3daistudio.py trellis --image photo.png --textures --resolution 1536 -o model.glb
```

**Options:**

| Flag | Description | Default |
|------|-------------|---------|
| `--image` | Path to local image (PNG/JPG/WebP) | required |
| `--image-url` | Public URL to image | — |
| `--resolution` | 512, 1024, or 1536 | 1024 |
| `--textures` | Enable texture generation | off |
| `--texture-size` | 1024, 2048, or 4096 | 2048 |
| `-o / --output` | Output .glb path (auto-polls until done) | — |

---

### `rapid` — Text or Image to 3D (balanced)

Best for: text prompts, quick generations.

```bash
# From text prompt
python 3daistudio.py rapid --prompt "a red sports car" -o car.glb

# From image
python 3daistudio.py rapid --image photo.png -o model.glb

# With PBR textures (metallic, roughness, normal maps)
python 3daistudio.py rapid --prompt "a wooden chair" --pbr -o chair.glb
```

**Options:**

| Flag | Description | Default |
|------|-------------|---------|
| `--prompt` | Text description (max ~600 chars) | — |
| `--image` | Path to local image | — |
| `--pbr` | Enable PBR maps (+20 credits) | off |
| `-o / --output` | Output .glb path (auto-polls) | — |

---

### `pro` — Text or Image to 3D (highest quality)

Best for: high-quality assets, game-ready models, detailed characters.

```bash
# From text prompt
python 3daistudio.py pro --prompt "a medieval castle" -o castle.glb

# From image, Hunyuan 3.1 model
python 3daistudio.py pro --image photo.png --model 3.1 -o model.glb

# Low poly style (great for games/web)
python 3daistudio.py pro --prompt "a cartoon cat" --generate-type LowPoly -o cat.glb

# With PBR textures
python 3daistudio.py pro --image photo.png --pbr -o model.glb
```

**Options:**

| Flag | Description | Default |
|------|-------------|---------|
| `--prompt` | Text description | — |
| `--image` | Path to local image | — |
| `--model` | 3.0 or 3.1 | 3.1 |
| `--pbr` | Enable PBR maps (+20 credits) | off |
| `--generate-type` | Normal, LowPoly, Geometry, Sketch | Normal |
| `--face-count` | Target polygon count | 500000 |
| `-o / --output` | Output .glb path (auto-polls) | — |

---

### `status` — Check a task by ID

```bash
python 3daistudio.py status <task_id>
```

Returns full JSON status including `status`, `progress`, and `results`.

---

### `download` — Download a finished task

```bash
python 3daistudio.py download <task_id> -o model.glb
```

---

## How Agents Should Use This Skill

When an AI agent calls this skill, the recommended flow is:

```
1. User asks for a 3D model (text prompt or image)
2. Agent runs: python 3daistudio.py pro --prompt "..." -o output.glb
   OR:          python 3daistudio.py trellis --image input.png -o output.glb
3. Script auto-polls until done (3–6 min for Pro, 25s–4min for TRELLIS)
4. File is saved to the specified output path
5. Agent confirms completion and provides the file path
```

The script **blocks until completion** when `--output` is specified — no separate polling needed.

---

## Cost Planning

| Use Case | Recommended Model | Est. Credits |
|----------|-------------------|--------------|
| Quick concept from image | TRELLIS.2 geo-only | 20 |
| Textured model from photo | TRELLIS.2 + textures | 30 |
| Text to 3D (fast) | Hunyuan Rapid | 35 |
| Text to 3D (quality) | Hunyuan Pro | 60 |
| Game-ready PBR asset | Hunyuan Pro + PBR | 80 |

> 💡 **Tip:** Failed jobs are automatically refunded. You only pay for successful generations.

---

## Limitations

- Rate limit: **3 requests/minute**
- Results expire after **24 hours** — download promptly
- TRELLIS.2 is **image-only** — no text prompts
- Hunyuan works best with clean, well-lit images
- Copyrighted characters (Sonic, Mario, etc.) may be rejected by content moderation
- Output format is **.glb** (can be converted to STL, OBJ, FBX using Blender or trimesh)

---

## Converting GLB to Other Formats

The output `.glb` files are actually ZIP archives containing `.obj` + textures.

```python
# Extract OBJ from GLB (they're ZIP files)
import zipfile
with zipfile.ZipFile('model.glb', 'r') as z:
    z.extractall('model_extracted/')

# Convert OBJ to STL using trimesh (pip install trimesh)
import trimesh
mesh = trimesh.load('model_extracted/model.obj')
mesh.export('model.stl')
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `THREE_D_AI_STUDIO_API_KEY not set` | Set the env var (see Setup above) |
| `balance` returns 404 | Check your API key is valid; balance also visible on dashboard |
| Generation FAILED immediately | Content moderation rejection or API error — credits refunded |
| Timeout (>10 min) | Rare — check task status manually with `status <task_id>` |
| GLB won't open in Blender | Extract as ZIP first, then import the .obj file |

---

*Skill by Whale Professor | API by 3D AI Studio (https://www.3daistudio.com)*
