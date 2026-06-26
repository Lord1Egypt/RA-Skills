---
name: exr
description: >
  Work with OpenEXR files — inspect channels, extract beauty/RGB passes, decode cryptomatte
  segmentation (material, object, asset), convert color spaces (ACEScg to sRGB), and batch
  process EXR directories. Use when working with EXR files, render passes, AOVs, or cryptomatte.
compatibility: Requires Python packages (pip install -r requirements.txt). Pin OpenEXR==3.2.4.
metadata:
  author: oumad
  version: "1.0"
  clawdbot: '{"requires":{"bins":["python3"]}}'
---

# EXR Skill

Work with OpenEXR files — the multi-channel, high dynamic range format standard in VFX, CGI rendering, and compositing. EXR files typically contain beauty renders, AOV passes (depth, normals, motion vectors), and cryptomatte segmentation data, all stored as 32-bit float channels.

## Setup

Install dependencies before first use:

```bash
pip install -r requirements.txt
```

Dependencies: `OpenEXR==3.2.4`, `numpy<2`, `Pillow`.

> **Note:** OpenEXR 3.2.4 is pinned because later versions (3.4+) can segfault on some platforms. numpy<2 is required for OpenEXR 3.2.x compatibility.

## Ready-Made Tool

`scripts/exr_extract.py` is a general-purpose CLI for common EXR tasks:

```
python scripts/exr_extract.py info <file|dir>
python scripts/exr_extract.py beauty <file|dir> [--colorspace CS] [--output-dir DIR] [--force]
python scripts/exr_extract.py crypto <file|dir> [--type TYPE] [--bg-color COLOR] [--suffix TEXT] [--no-suffix] [--output-dir DIR] [--force]
python scripts/exr_extract.py channels <file|dir> --channels R,G,B [--colorspace CS] [--output-dir DIR] [--force]
```

Use this tool first. Fall back to custom Python only for edge cases.

## Channel Inspection

Always start by inspecting what's in the EXR:

```bash
python scripts/exr_extract.py info render.exr
```

This shows:
- Resolution and data/display windows
- All channels with data types and sampling
- Cryptomatte metadata (hash function, manifest, conversion type)
- Auto-detected crypto pass types and their channel prefixes

Common channel patterns:
- `R`, `G`, `B`, `A` — beauty/RGBA pass
- `depth.Z` or `Z` — depth pass
- `N.X`, `N.Y`, `N.Z` — world-space normals
- `crypto_material00.R`, `.G`, `.B`, `.A` — cryptomatte rank 0-1
- `crypto_object00.R`, `.G` — object ID cryptomatte

## Beauty / RGB Extraction

Extract the rendered beauty image as a tone-mapped PNG:

```bash
python scripts/exr_extract.py beauty render.exr --colorspace acescg
```

Color space options:
- **`acescg`** (default): ACEScg AP1 primaries → linear sRGB via 3x3 matrix → sRGB OETF. Standard for most VFX renders.
- **`linear`**: Already linear sRGB primaries → apply sRGB OETF only (gamma encoding).
- **`srgb`**: Already sRGB-encoded → clamp and save directly.

The ACEScg→sRGB pipeline applies the AP1-to-Rec.709 matrix then the piecewise sRGB OETF. See `${CLAUDE_SKILL_DIR}/references/color-spaces.md` for exact values.

## Cryptomatte Extraction

Extract material, object, or asset segmentation masks as color-coded PNGs:

```bash
python scripts/exr_extract.py crypto render.exr
python scripts/exr_extract.py crypto render.exr --type crypto_material
python scripts/exr_extract.py crypto ./renders/ --bg-color black --output-dir ./masks/
```

How it works:
1. Reads the top-ranked cryptomatte ID from `{prefix}00.R` (float-encoded uint32 hash) and coverage from `{prefix}00.G`
2. Detects the background ID by sampling edges and corners of the image
3. Assigns a 35-color bold palette to foreground materials, ranked by pixel area (largest material gets the most distinct color)
4. Background gets neutral gray (or black with `--bg-color black`)
5. Zero-coverage pixels are black

Auto-detects channel naming conventions across renderers:
- Arnold: `crypto_material00`, `crypto_object00`
- Shortened: `crypto_mat00`, `crypto_obj00`

See `${CLAUDE_SKILL_DIR}/references/cryptomatte.md` for format details.

### Crypto Options
- `--type`: Force a specific type (`crypto_material`, `crypto_object`, `crypto_asset`). Default: extract all detected.
- `--bg-color`: `gray` (default), `black`, or `auto`.
- `--suffix`: Custom suffix (default: `_materialID`, `_objectID`, `_assetID`).
- `--no-suffix`: Output with same name as input (for dataset prep into separate folders).

## Arbitrary Channel Extraction

Extract any named channels:

```bash
# Normals as RGB
python scripts/exr_extract.py channels render.exr --channels N.X,N.Y,N.Z

# Single channel (depth)
python scripts/exr_extract.py channels render.exr --channels depth.Z
```

When 3 channels are specified, they're composited as RGB. Single channels become grayscale. Other counts produce individual files.

## Batch Processing

All subcommands accept a directory path to process every EXR in it:

```bash
python scripts/exr_extract.py beauty ./renders/ --output-dir ./target/ --colorspace acescg
python scripts/exr_extract.py crypto ./renders/ --output-dir ./control/ --no-suffix
```

Existing outputs are skipped unless `--force` is specified.

## Custom Python

For edge cases not covered by the CLI, use the OpenEXR Python API directly:

```python
import OpenEXR, Imath
import numpy as np

exr = OpenEXR.InputFile('render.exr')
header = exr.header()
dw = header['dataWindow']
w = dw.max.x - dw.min.x + 1
h = dw.max.y - dw.min.y + 1

pt = Imath.PixelType(Imath.PixelType.FLOAT)
raw = exr.channel('R', pt)
data = np.frombuffer(raw, dtype=np.float32).reshape(h, w)
```

Always install dependencies first, pin OpenEXR==3.2.4, and use `Imath.PixelType.FLOAT`.

## Related: oiiotool Skill

For tasks beyond what this Python-based EXR skill covers, consider the **oiiotool** skill (`pip install openimageio`). It provides:

- **ACES display transforms** — proper tone-mapped output with highlight rolloff (RRT+ODT), essential for HDR/camera-originated EXRs where simple matrix conversion clips highlights
- **Exposure sweeps** — generate multi-exposure composites for reviewing HDR dynamic range
- **EXR sequence to video** — convert frame sequences to MP4 via oiiotool + ffmpeg
- **Format conversion** — EXR to/from TIFF, DPX, PNG, JPEG, HDR, WebP, and more
- **Efficient multichannel reading** — `-i:ch=R,G,B` reads only needed channels, critical for large production EXRs
- **Batch sequence processing** — frame wildcards with parallel processing

### When to use which

| Task | Use |
|------|-----|
| Inspect channels, cryptomatte metadata | **exr** skill |
| Extract cryptomatte as colored segmentation | **exr** skill |
| Beauty extraction from ACEScg renders (simple scenes) | **exr** skill |
| HDR review with ACES tone mapping | **oiiotool** skill |
| Exposure adjustment / sweep | **oiiotool** skill |
| EXR sequence to MP4 | **oiiotool** skill |
| Format conversion (EXR to DPX, TIFF, etc.) | **oiiotool** skill |
| Resize, crop, composite | **oiiotool** skill |
| Batch sequence operations | **oiiotool** skill |
