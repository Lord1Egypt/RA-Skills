---
slug: cn-web-image-optimizer
name: Web Image Optimizer
description: |
  Compress images for web usage. Smart quality reduction + resize to fit under 500KB.
  Supports JPEG, PNG, WebP, BMP, TIFF input. Auto WebP output for best compression.
author: qiance
version: "1.0.0"
tags: [image, compression, web, optimization, webp, jpeg, png]
---

# Web Image Optimizer

Smart image compression for web usage. Automatically reduces file size to under 500KB while preserving visual quality.

## Features

| Feature | Description |
|---------|-------------|
| Smart Compression | Progressive quality reduction until target size is met |
| Auto Resize | If quality reduction alone is insufficient, proportionally resizes the image |
| Multi-Format Input | JPEG, PNG, WebP, BMP, TIFF, GIF |
| WebP Preferred | Auto WebP output (best compression for web) |
| JPEG Fallback | JPEG output option for maximum compatibility |
| Batch Processing | Compress all images in a directory at once |
| Recursive Scan | Search subdirectories recursively |
| Size Target | Configurable max file size (default: 500KB) |

## Usage

### Single Image Compression

```bash
# Compress to WebP (auto, under 500KB)
python scripts/web_image_optimizer.py compress photo.jpg

# Compress to JPEG, max 300KB
python scripts/web_image_optimizer.py compress photo.jpg --format jpeg --max-kb 300

# Compress to PNG
python scripts/web_image_optimizer.py compress photo.png --format png

# Custom output path
python scripts/web_image_optimizer.py compress photo.jpg -o /path/to/output.webp
```

### Batch Processing

```bash
# Compress all images in a directory
python scripts/web_image_optimizer.py batch ./images/

# Batch with custom format and size limit
python scripts/web_image_optimizer.py batch ./photos/ --format jpeg --max-kb 200

# Recursive subdirectory scan
python scripts/web_image_optimizer.py batch ./content/ --recursive
```

### Image Info

```bash
python scripts/web_image_optimizer.py info photo.jpg
```

## Compression Strategy

The optimizer uses a multi-step approach:

1. **Format Conversion**: PNG input is converted to WebP (typically 70-90% smaller)
2. **Quality Reduction**: Progressive quality adjustment (85 -> 75 -> 65 -> ...)
3. **Smart Resize**: If quality alone cannot meet target, proportionally resize the image
4. **Final Fallback**: Save at minimum quality if target cannot be met

## Output Format Guide

| Format | Compression | Quality | Browser Support | Recommendation |
|--------|-------------|---------|-----------------|----------------|
| WebP | Best | Excellent | 96%+ | Default choice |
| JPEG | Good | Good | 100% | Maximum compatibility |
| PNG | Limited | Lossless | 100% | Transparency needed |

## Example Output

```
  hero-banner.png
    2682.6 KB  -->     41.0 KB  (+98.5%)
    Format: WEBP  Quality: 85  Size: 1280x714
    Output: ./hero-banner_web.webp
```

## Dependencies

- Python 3.6+
- Pillow (PIL) - Standard Python imaging library

Install Pillow if needed:
```bash
pip3 install Pillow
```

## Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| --max-kb | -m | 500 | Maximum output file size in KB |
| --format | -f | auto | Output format: auto/webp/jpeg/png |
| --quality | -q | 85 | Starting quality (1-100) |
| --output | -o | auto | Output file path |
| --recursive | -r | false | Scan subdirectories (batch mode) |

## Security Notes

- Pure local processing, no network calls
- No image data leaves your machine
- Preserves EXIF metadata is NOT done (metadata stripped for smaller size)
- No file deletion - original files are preserved

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (file not found, unsupported format, etc.) |

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
