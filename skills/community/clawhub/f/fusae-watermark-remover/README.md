# Watermark Remover Skill

Claude Code skill for automatically detecting and removing watermarks from images using AI.

## Installation

### 1. Install the skill

```bash
# Clone or symlink this skill to your Claude skills directory
ln -s /path/to/watermark-remover/skills/watermark-remover ~/.claude/skills/watermark-remover
```

### 2. Install dependencies

This skill requires the `watermark-remover` Python package:

```bash
# Option A: Install from PyPI (when published)
pip install watermark-remover

# Option B: Install from source
git clone https://github.com/yourusername/watermark-remover.git
cd watermark-remover
pip install -e .
```

**Requirements:**
- Python 3.9+
- opencv-python
- numpy
- Pillow
- iopaint (for LaMa AI model)

### 3. Verify installation

```bash
watermark-remover --help
```

## Usage

In Claude Code, simply ask:
- "Remove watermark from image.jpg"
- "Clean watermarks from ./photos/ directory"
- "去掉这张图片的水印"

## Manual Usage

```bash
# Single image
python ~/.claude/skills/watermark-remover/scripts/main.py image.jpg

# Directory
python ~/.claude/skills/watermark-remover/scripts/main.py ./photos/

# Preview detection
python ~/.claude/skills/watermark-remover/scripts/main.py ./photos/ --preview

# Adjust sensitivity
python ~/.claude/skills/watermark-remover/scripts/main.py image.jpg --corner-ratio 0.2 --threshold 20
```

## How It Works

1. Scans image corners (default 15% area)
2. Detects watermarks using edge detection + high-frequency analysis
3. Generates precise mask
4. Removes watermark using LaMa AI model (auto-downloads on first run)
5. Falls back to OpenCV inpaint if LaMa fails

## Troubleshooting

**Error: watermark-remover not found**
- Make sure you've installed the package: `pip install -e /path/to/watermark-remover`
- Or install from PyPI: `pip install watermark-remover`

**LaMa model download fails**
- Use `--no-lama` flag to use OpenCV inpaint instead
- Check your internet connection

## License

MIT
