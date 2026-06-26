# cutout-visual-api

> A Python CLI skill for [Cutout.Pro](https://www.cutout.pro) visual processing APIs.  
> Supports **Background Removal**, **Face Cutout**, and **Photo Enhancement** — with file upload or image URL input.

## Features

- 🖼️ **Background Remover** — Remove image backgrounds, return transparent PNG
- 👤 **Face Cutout** — Segment face/hair region with optional 68-point landmark detection
- ✨ **Photo Enhancer** — AI super-resolution for real photos and anime/cartoon images
- 📤 Supports both **local file upload** and **image URL** as input
- 🔄 Returns **binary stream** or **Base64-encoded** results
- 🔁 Built-in retry logic with exponential backoff

## Quick Start

### 1. Get API Key

Sign up at [cutout.pro](https://www.cutout.pro/user/secret-key) and copy your API Key.

### 2. Configure

Create a `.env` file in the project root:

```
CUTOUT_API_KEY=your_key_here
```

### 3. Install Dependencies

```bash
pip install -r scripts/requirements.txt
```

### 4. Run

```bash
# Background removal
python scripts/cutout.py --api bg-remover --image photo.jpg --output out.png

# Face cutout with facial landmarks
python scripts/cutout.py --api face-cutout --image portrait.jpg --base64 --face-analysis

# Photo enhancement (anime model)
python scripts/cutout.py --api photo-enhancer --image anime.jpg --face-model anime

# Use image URL instead of local file
python scripts/cutout.py --api bg-remover --url "https://example.com/photo.jpg"
```

## API Reference

| API | Endpoint | Credits |
|-----|----------|---------|
| Background Remover | `POST /api/v1/matting?mattingType=6` | 1/image |
| Face Cutout | `POST /api/v1/matting?mattingType=3` | 1/image |
| Photo Enhancer | `POST /api/v1/photoEnhance` | 1/image |
| Preview mode | any of the above with `--preview` | 0.25/image |

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--api` | `bg-remover` / `face-cutout` / `photo-enhancer` | Required |
| `--image` | Local image file path | — |
| `--url` | Image URL (URL mode) | — |
| `--output` | Output file path | `data/outputs/` |
| `--base64` | Return Base64 JSON | false |
| `--crop` | Crop transparent whitespace | false |
| `--bgcolor` | Fill background color (hex, e.g. `FFFFFF`) | — |
| `--preview` | Preview mode (max 500×500, 0.25 credits) | false |
| `--output-format` | `png` / `webp` / `jpg_75` etc. | `png` |
| `--face-analysis` | Return 68 facial landmarks (face-cutout only) | false |
| `--face-model` | `quality` or `anime` (photo-enhancer only) | `quality` |

## File Structure

```
cutout-visual-api/
├── README.md                   # This file
├── SKILL.md                    # Skill metadata and usage guide
├── references/
│   ├── api-reference.md        # Full API documentation
│   └── setup-guide.md          # Setup and troubleshooting
└── scripts/
    ├── cutout.py               # Main CLI script
    ├── config.py               # Configuration management
    └── requirements.txt        # Python dependencies
```

## Limits

- Supported formats: PNG, JPG, JPEG, BMP, WEBP
- Max resolution: 4096×4096 px
- Max file size: 15 MB
- QPS: up to 5 concurrent requests/second

## License

MIT
