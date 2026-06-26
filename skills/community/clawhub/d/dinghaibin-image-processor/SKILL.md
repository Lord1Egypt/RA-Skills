---
name: image-processor
description: Process and convert images with resize, crop, compress, and format conversion. Use when user needs to batch resize photos, convert image formats, compress images for web, create thumbnails, or apply filters to images.
---

# Image Processor

Process and convert images with resize, crop, compress, and format conversion.

## Quick Start

```bash
# Resize an image
python scripts/process.py input.jpg --resize 800x600 --output output.jpg

# Convert format
python scripts/process.py input.png --format jpg --output output.jpg
```

## Usage

```bash
python scripts/process.py INPUT [OPTIONS]

Options:
  --output PATH      Output file path
  --resize WxH       Resize to dimensions
  --scale PERCENT    Scale by percentage
  --crop WxH+X+Y     Crop to dimensions
  --format FORMAT    Convert format: jpg, png, webp, gif
  --quality QUALITY  JPEG quality (1-100)
  --thumbnail SIZE  Create thumbnail
  --grayscale        Convert to grayscale
  --blur RADIUS      Apply blur
  --rotate DEGREES   Rotate image
```

## Examples

```bash
# Resize to 800px width
python scripts/process.py photo.jpg --resize 800x0 --output small.jpg

# Create thumbnail
python scripts/process.py photo.jpg --thumbnail 200x200 --output thumb.jpg

# Compress for web
python scripts/process.py large.jpg --quality 80 --format webp --output optimized.webp

# Batch resize
for f in *.jpg; do python scripts/process.py "$f" --resize 1200x0 --output "small_$f"; done

# Convert to PNG
python scripts/process.py input.jpg --format png --output output.png
```

## Features

- Resize (by dimensions or percentage)
- Crop
- Format conversion (JPG, PNG, WebP, GIF)
- Quality/compression control
- Thumbnails
- Grayscale conversion
- Blur filter
- Rotation
- Batch processing
