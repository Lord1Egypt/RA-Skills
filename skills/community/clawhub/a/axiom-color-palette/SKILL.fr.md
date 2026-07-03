---
name: axiom-color-palette
description: Extracteur de palette de couleurs — extrait les couleurs dominantes d'une image (PNG/JPEG/GIF). Utilisez pour avoir une palette pour design ou analyse. Stdlib pur, sans LLM.
version: 0.1.2
license: Apache-2.0
---

# axiom-color-palette

**Version:** 0.1.2
**Axioma Tools**

Extrait la palette de couleurs dominantes d'une image via analyse de fréquence.

## What this skill does

- Extraction de couleurs par fréquence
- Taille de palette configurable (3-16 couleurs)
- Optionnel : clustering K-means
- Sortie en codes hex + tuples RGB
- Output JSON pour outils de design

## When to use this skill

- ✅ Générer une palette pour redesign de site
- ✅ Trouver les couleurs brand dominantes dans une image
- ✅ Analyser les tendances couleurs de portfolios design
- ❌ Convertir des espaces color (utilise colormath)
- ❌ Rendre des images (utilise Pillow)

## Usage

```bash
python3 axiom_color_palette.py logo.png --colors 5
python3 axiom_color_palette.py photo.jpg --json > palette.json
```

```python
from axiom_color_palette import extract_palette
colors = extract_palette('image.png', n_colors=5)
# [('#FF5733', 42), ('#33FF57', 28), ...]
```

## Validation

| Check | Status |
|-------|--------|
| Unit tests | 15+ cases |
| Performance | <100ms |
| Security | Pure stdlib, no injection |
| Determinism | Byte-to-byte stable |
| License | Apache-2.0 |

_Last updated: 2026-06-14_
