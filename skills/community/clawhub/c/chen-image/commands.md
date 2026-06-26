# Image Processing Commands

These are specific examples for cases where the user needs concrete commands rather than only decision guidance.

## ImageMagick

### Resize

```bash
magick input.jpg -resize 1920x1080\> output.jpg
magick input.jpg -resize 800x600! output.jpg
```

### Format Conversion

```bash
magick input.jpg -quality 80 output.webp
magick input.png -background white -flatten output.jpg
magick input.jpg -quality 75 output.avif
```

### Orientation and Metadata

```bash
magick input.jpg -auto-orient output.jpg
magick input.jpg -auto-orient -strip output.jpg
identify -verbose input.jpg | grep -i exif
```

### SVG Optimization and Rasterization

```bash
npx svgo input.svg -o output.svg
magick -background none -density 300 input.svg -resize 512x512 output.png
```

### Batch Processing

```bash
mogrify -format webp -quality 80 *.jpg
mogrify -resize 1920x1080\> *.jpg
```

### Aspect-Ratio Crop

```bash
magick input.jpg -gravity center -crop 1200x630+0+0 +repage output.jpg
magick input.jpg -resize 1200x630^ -gravity center -extent 1200x630 output.jpg
```

## Pillow

### Resize

```python
from PIL import Image

img = Image.open("input.jpg")
img = img.resize((800, 600), Image.Resampling.LANCZOS)
img.save("output.jpg", quality=85)
```

### WebP Conversion

```python
from PIL import Image

img = Image.open("input.jpg")
img.save("output.webp", "WEBP", quality=80, method=6)
```

### Transparency to White Background

```python
from PIL import Image

img = Image.open("input.png")
if img.mode in ("RGBA", "LA", "P"):
    background = Image.new("RGB", img.size, (255, 255, 255))
    background.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
    img = background
img.save("output.jpg", quality=85)
```

### Thumbnail

```python
from PIL import Image

img = Image.open("input.jpg")
img.thumbnail((300, 300), Image.Resampling.LANCZOS)
img.save("thumb.jpg", quality=75)
```

## Built-in and Alternative Tools

### macOS `sips`

```bash
sips -Z 1600 input.jpg --out output.jpg
sips -s format webp input.png --out output.webp
```

- Useful when Pillow or ImageMagick are unavailable.
- Validate quality and metadata handling because `sips` is convenient, not always the most controllable.

### Sharp (Node.js)

```bash
npx sharp input.jpg --resize 1600 --webp quality=80 -o output.webp
npx sharp input.png --flatten background=white --jpeg quality=85 -o output.jpg
```

- Good for scripted web pipelines and batch conversions.
- Still inspect transparency flattening, color handling, and output dimensions deliberately.

### `exiftool`

```bash
exiftool input.jpg
exiftool -gps:all= -overwrite_original input.jpg
exiftool -all= -overwrite_original input.jpg
```

- Useful when metadata handling is the real job.
- Prefer targeted stripping when rights data or timestamps still matter.

### `ffmpeg` for Animated Images

```bash
ffmpeg -i input.gif -vf "fps=15,scale=1200:-1:flags=lanczos" output.webm
ffmpeg -i input.gif -vf "fps=15,scale=1200:-1:flags=lanczos" -loop 0 output.webp
```

- Better than treating every animation problem as a GIF problem forever.

## Command Traps

- Always auto-orient before final export if EXIF rotation exists.
- Flatten alpha intentionally when converting transparent images to JPEG.
- Use `LANCZOS` for final downscaling, not low-quality defaults.
- Spot-check one file before running a batch command across everything.
- Prefer writing outputs to a new path instead of overwriting the only good source.
- Treat `npx` examples as remote-code execution from the package registry and use them only in trusted environments.
