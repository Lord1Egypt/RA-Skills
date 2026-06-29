# axiom-image-metadata-stripper

> Strip EXIF, GPS, IPTC, XMP from JPEG/PNG — pure stdlib.

**Axioma Tools for Capafy**
**Version:** 0.1.0

## 🎯 Problème résolu

Tes photos contiennent GPS, modèle d'appareil, date, software → **vie privée leak**.

**axiom-image-metadata-stripper** :
- JPEG : strip tous les APP0-15 + COM
- PNG : strip tous les ancillary chunks
- Pure stdlib (pas de PIL/Pillow)
- Préserve la qualité d'origine

## 🚀 Usage

```bash
# Strip
python3 axiom_image_metadata_stripper.py photo.jpg -o clean.jpg
# ✅ Stripped: clean.jpg
#    Format: jpeg
#    Original: 1234567 bytes
#    Stripped: 987654 bytes
#    Removed:  246913 bytes (20.0%)

# Analyze (without stripping)
python3 axiom_image_metadata_stripper.py photo.jpg --analyze
# Format: jpeg
# Metadata chunks: 3
#   - APP1 (EXIF, XMP): 50000 bytes
#   - APP13 (Photoshop): 200 bytes
#   - COM (Comment): 50 bytes

# JSON
python3 axiom_image_metadata_stripper.py photo.jpg --analyze --json
```

## 🧪 Tests

11 tests passent.

## ⚠️ Limitations

- JPEG/PNG/GIF seulement (pas WebP, AVIF, HEIC)
- Pas de ré-encodage
- Strip tout ou rien (pas de sélectif)

## 🛠️ Spec

| Champ | Valeur |
|-------|--------|
| **Pricing Capafy** | $0.01/use (privacy tier) |
