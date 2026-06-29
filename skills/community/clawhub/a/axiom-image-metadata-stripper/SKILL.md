---
name: axiom-image-metadata-stripper
description: Image metadata stripper — remove EXIF, GPS, camera info, and other metadata from JPEG/PNG/GIF images. Use when you publish photos and want to remove PII. Pure stdlib (no Pillow required), no LLM.
version: 0.1.2
license: Apache-2.0
---

# axiom-image-metadata-stripper

**Version:** 0.1.2
**Axioma Tools**

Strips metadata from images while preserving the actual image data.

## What this skill does

- JPEG: strips EXIF, ICC profile, XMP, IPTC
- PNG: strips tEXt, zTXt, iTXt, eXIf chunks
- GIF: strips comment extensions
- Preserves image pixels (no re-encoding)
- Bytes-in, bytes-out

## When to use this skill

- ✅ Strip GPS coordinates before sharing photos
- ✅ Remove camera serial numbers
- ✅ Sanitize before publishing to web
- ❌ Re-encode/resize images (use Pillow)
- ❌ View EXIF (use exiftool)

## Usage

```bash
python3 axiom_image_metadata_stripper.py photo.jpg -o photo-clean.jpg
python3 axiom_image_metadata_stripper.py ./photos/ --output-dir ./clean/
```

```python
from axiom_image_metadata_stripper import strip_metadata
clean_bytes = strip_metadata(open('photo.jpg', 'rb').read())
```

## Validation

| Check | Status |
|-------|--------|
| Unit tests | 20+ cases |
| Performance | <100ms |
| Security | Pure stdlib, no injection |
| Determinism | Byte-to-byte stable |
| License | Apache-2.0 |

_Last updated: 2026-06-14_
