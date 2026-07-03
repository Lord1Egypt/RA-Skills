# 📄 `test_axiom_color_palette.py`

**Path:** `/run/media/axioma/Merlin/axiom-skills-public/axiom-color-palette/test_axiom_color_palette.py`  
**Size:** 3,063 bytes / 119 lines  
**Hash:** `cd54339fa7a703cb`  
**Generated:** 2026-06-15T03:00:47.187808+00:00

## 📝 Module Docstring

```
Tests — axiom-color-palette 
```

## 📦 Imports (17)

```python
import pathlib.Path
import sys
import unittest
import axiom_color_palette.HARMONIES
import axiom_color_palette.adjust_lightness
import axiom_color_palette.analogous
import axiom_color_palette.complementary
import axiom_color_palette.generate
import axiom_color_palette.hsl
import axiom_color_palette.monochromatic
import axiom_color_palette.parse_hex
import axiom_color_palette.rotate_hue
import axiom_color_palette.tetradic
import axiom_color_palette.to_hex
import axiom_color_palette.to_hsl_string
import axiom_color_palette.to_rgb_string
import axiom_color_palette.triadic
```

## 🏛️ Classes (7)

### `TestParseHex`
**Methods:** `test_01_6char, test_02_no_hash, test_03_3char, test_04_lowercase, test_05_invalid, test_06_wrong_length`

### `TestToHex`
**Methods:** `test_07_basic`

### `TestHsl`
**Methods:** `test_08_pure_red, test_09_white`

### `TestRotateHue`
**Methods:** `test_10_180, test_11_120`

### `TestHarmonies`
**Methods:** `test_12_complementary, test_13_analogous, test_14_triadic, test_15_tetradic, test_16_monochromatic`

### `TestGenerate`
**Methods:** `test_17_generate, test_18_unknown_harmony`

### `TestDeterminism`
**Methods:** `test_19_1000_runs`
