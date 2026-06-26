# Gemini Watermark Remover

[English](./README.md) | [中文](./README_zh.md)

---

Remove visible Gemini AI watermarks from images using reverse alpha blending algorithm.

## ⚠️ Disclaimer

**This tool is for personal learning and research only. Commercial use is prohibited.**

## Features

- ✅ Pure local processing (images not uploaded)
- ✅ Reverse alpha blending algorithm, lossless watermark removal
- ✅ Automatic watermark size detection (48×48 or 96×96)
- ✅ Standalone script with embedded templates (no external dependencies)

## Installation

```bash
pip install Pillow numpy
```

## Usage

```bash
# Basic usage
python3 scripts/remove_watermark.py image.jpg

# Specify output
python3 scripts/remove_watermark.py image.jpg -o cleaned.jpg
```

## Algorithm

Gemini uses alpha blending:
```
watermarked = α × 255 + (1 - α) × original
```

Reverse:
```
original = (watermarked - α × 255) / (1 - α)
```

## Files

```
├── scripts/
│   └── remove_watermark.py   # Main script with embedded templates
├── requirements.txt
├── README.md
├── README_zh.md
└── LICENSE
```

## License

[MIT License](./LICENSE)
