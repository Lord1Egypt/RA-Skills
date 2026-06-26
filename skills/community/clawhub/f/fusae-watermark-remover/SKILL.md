---
name: watermark-remover
version: 0.1.0
description: Automatically detects and removes watermarks from images using AI-powered inpainting. Use when user asks to "remove watermark", "clean image", or "去水印".
---

# Watermark Remover

Automatically detects watermarks in image corners and removes them using LaMa AI model.

## Installation

This skill requires the `watermark-remover` Python package. Install it first:

```bash
# Install from PyPI (when published)
pip install watermark-remover

# Or install from source
git clone https://github.com/yourusername/watermark-remover.git
cd watermark-remover
pip install -e .
```

**Dependencies**: Python 3.9+, opencv-python, numpy, Pillow, iopaint

## Script Directory

Scripts in `scripts/` subdirectory. Replace `${SKILL_DIR}` with this SKILL.md's directory path.

| Script | Purpose |
|--------|---------|
| `scripts/main.py` | Watermark removal CLI wrapper |

## Usage

```bash
python ${SKILL_DIR}/scripts/main.py <input> [options]
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `<input>` | Image file or directory | Required |
| `--output` | Output path | `<input>/no_watermark` |
| `--corner-ratio` | Corner area ratio (0-1) | 0.15 |
| `--threshold` | Detection sensitivity (lower = more sensitive) | 30 |
| `--padding` | Mask dilation pixels | 10 |
| `--preview` | Generate mask preview only | false |
| `--no-lama` | Use OpenCV instead of LaMa | false |

## Examples

```bash
# Single image
python ${SKILL_DIR}/scripts/main.py image.jpg

# Directory with custom output
python ${SKILL_DIR}/scripts/main.py ./photos/ --output ./cleaned/

# Preview detection (shows red marks on watermarks)
python ${SKILL_DIR}/scripts/main.py ./photos/ --preview

# Adjust detection sensitivity
python ${SKILL_DIR}/scripts/main.py image.jpg --corner-ratio 0.2 --threshold 20

# Use OpenCV inpaint (faster but lower quality)
python ${SKILL_DIR}/scripts/main.py image.jpg --no-lama
```

## How It Works

1. Scans image corners (default 15% area)
2. Detects watermarks using edge detection + high-frequency analysis
3. Generates precise mask
4. Removes watermark using LaMa AI model (auto-downloads on first run)
5. Falls back to OpenCV inpaint if LaMa fails

## Supported Formats

JPG, JPEG, PNG, BMP, TIFF, WEBP
