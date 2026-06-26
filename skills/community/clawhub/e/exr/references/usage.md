# Usage Examples

## Quick Start

### Inspect an EXR file
```bash
python exr_extract.py info render.exr
```

### Extract beauty render as PNG
```bash
python exr_extract.py beauty render.exr
```
Defaults to ACEScg input color space. For linear sRGB renders:
```bash
python exr_extract.py beauty render.exr --colorspace linear
```

### Extract cryptomatte as colored segmentation
```bash
python exr_extract.py crypto render.exr
```
Auto-detects all available crypto passes (material, object, asset).

## Batch Processing

Process every EXR in a directory:
```bash
python exr_extract.py beauty ./renders/
python exr_extract.py crypto ./renders/
python exr_extract.py info ./renders/
```

With custom output directory:
```bash
python exr_extract.py beauty ./renders/ --output-dir ./output/beauty/
python exr_extract.py crypto ./renders/ --output-dir ./output/crypto/
```

## Dataset Preparation

Create paired target/control images for training (e.g., image-to-image models):

```bash
# Beauty renders → target/
python exr_extract.py beauty ./renders/ --output-dir ./target/ --colorspace acescg

# Material IDs → control/ (same filenames, no suffix)
python exr_extract.py crypto ./renders/ --output-dir ./control/ --type crypto_material --no-suffix
```

This produces:
```
target/render_001.png       # beauty image
control/render_001.png      # material ID segmentation (same name)
```

## Specific Crypto Type

Extract only material IDs:
```bash
python exr_extract.py crypto render.exr --type crypto_material
```

Extract only object IDs:
```bash
python exr_extract.py crypto render.exr --type crypto_object
```

## Custom Appearance

Black background instead of gray:
```bash
python exr_extract.py crypto render.exr --bg-color black
```

Custom output suffix:
```bash
python exr_extract.py crypto render.exr --suffix _segmentation
```

## Channel Extraction

Extract world-space normals as RGB:
```bash
python exr_extract.py channels render.exr --channels N.X,N.Y,N.Z
```

Extract depth as grayscale:
```bash
python exr_extract.py channels render.exr --channels depth.Z
```

Extract with color space conversion:
```bash
python exr_extract.py channels render.exr --channels diffuse.R,diffuse.G,diffuse.B --colorspace acescg
```

## Overwrite Existing

By default, existing output files are skipped. Use `--force` to overwrite:
```bash
python exr_extract.py beauty ./renders/ --force
python exr_extract.py crypto ./renders/ --force
```
