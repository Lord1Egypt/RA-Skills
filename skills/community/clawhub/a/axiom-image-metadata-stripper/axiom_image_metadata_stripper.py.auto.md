# 📄 `axiom_image_metadata_stripper.py`

**Path:** `/run/media/axioma/Merlin/axiom-skills-public/axiom-image-metadata-stripper/axiom_image_metadata_stripper.py`  
**Size:** 8,515 bytes / 288 lines  
**Hash:** `e059e9f793d96cb8`  
**Generated:** 2026-06-15T03:00:47.183736+00:00

## 📝 Module Docstring

```
🛠️ axiom-image-metadata-stripper — Image Metadata Remover
==========================================================

⚠️ LIMITATIONS CONNUES :
- JPEG/PNG seulement (pas WebP, AVIF, HEIC)
- Pas de ré-encodage (préserve la qualité d'origine)
- Pas de préservation sélective (tout ou rien)

SUPPRIME LES METADONNÉES D'IMAGE (EXIF, GPS, IPTC, XMP)
```

## 📦 Imports (5)

```python
import re
import struct
import sys
import argparse
import json
```

## ⚡ Functions (6)

### `def detect_format(data):`
> Detect image format from magic bytes.

### `def strip_jpeg(data):`
> Strip metadata from JPEG.

Strategy: walk through markers, skip metadata APP/COM markers,
keep everything else (DQT, DHT, SOF, SOS, image data).

### `def strip_png(data):`
> Strip metadata from PNG.

Strategy: keep only critical chunks (IHDR, PLTE, IDAT, IEND),
skip ancillary chunks (tEXt, zTXt, iTXt, tIME, pHYs, etc.).

### `def strip_metadata(input_path, output_path):`
> Strip metadata from an image file.

Returns dict with: input, output, original_size, stripped_size, format

### `def analyze(input_path):`
> Analyze a JPEG/PNG for metadata chunks (without stripping).

### `def main():`
