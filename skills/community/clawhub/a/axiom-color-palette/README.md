# axiom-color-palette

> Color palette generator — complementary, analogous, triadic, tetradic, etc.

**Axioma Tools for Capafy**
**Version:** 0.1.0

## 🎯 Problème résolu

Tu as UNE couleur, mais tu veux une palette harmonieuse.

**axiom-color-palette** génère des harmonies classiques :
- Complementary (180°)
- Analogous (±30°)
- Triadic (120° × 3)
- Tetradic (90° × 4)
- Split-complementary
- Monochromatic

## 🚀 Usage

```bash
# Complementary (default)
python3 axiom_color_palette.py "#FF5500"
# Base: #FF5500  HSL: (20.2, 100.0, 50.0)
# Harmony: complementary
#   1. #FF5500
#   2. #00AAFF

# Triadic
python3 axiom_color_palette.py "#3B82F6" --harmony triadic

# CSS output
python3 axiom_color_palette.py "#10B981" --harmony triadic --format css
# /* triadic palette from #10B981 */
# --color-1: #10B981;
# --color-2: #B81081;
# --color-3: #8110B8;

# JSON
python3 axiom_color_palette.py "#FF5500" --json
```

## 🧪 Tests

19 tests passent.

## ⚠️ Limitations

- RGB seulement (pas alpha)
- Pas d'extraction depuis image

## 🛠️ Spec

| Champ | Valeur |
|-------|--------|
| **Pricing Capafy** | $0.01/use (design tier) |
