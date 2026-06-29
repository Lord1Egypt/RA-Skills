---
name: axiom-image-metadata-stripper
description: Strippeur de métadonnées d'image — supprime EXIF, GPS, info caméra, et autres métadonnées des images JPEG/PNG/GIF. Utilisez pour publier des photos sans PII. Stdlib pur (Pillow non requis), sans LLM.
version: 0.1.2
license: Apache-2.0
---

# axiom-image-metadata-stripper

**Version:** 0.1.2
**Axioma Tools**

Strip les métadonnées des images en préservant les données d'image réelles.

## What this skill does

- JPEG : strip EXIF, ICC profile, XMP, IPTC
- PNG : strip tEXt, zTXt, iTXt, eXIf chunks
- GIF : strip les extensions de commentaire
- Préserve les pixels (pas de re-encoding)
- Bytes-in, bytes-out

## When to use this skill

- ✅ Strip les coordonnées GPS avant partage
- ✅ Supprimer les numéros de série caméra
- ✅ Sanitize avant publication web
- ❌ Re-encoder/redimensionner (utilise Pillow)
- ❌ Voir l'EXIF (utilise exiftool)

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
