# 📄 `test_axiom_image_metadata_stripper.py`

**Path:** `/run/media/axioma/Merlin/axiom-skills-public/axiom-image-metadata-stripper/test_axiom_image_metadata_stripper.py`  
**Size:** 3,936 bytes / 122 lines  
**Hash:** `c4d0e696e0760010`  
**Generated:** 2026-06-15T03:00:47.184304+00:00

## 📝 Module Docstring

```
Tests — axiom-image-metadata-stripper 
```

## 📦 Imports (12)

```python
import pathlib.Path
import os
import struct
import sys
import tempfile
import unittest
import axiom_image_metadata_stripper.analyze
import axiom_image_metadata_stripper.detect_format
import axiom_image_metadata_stripper.strip_jpeg
import axiom_image_metadata_stripper.strip_metadata
import axiom_image_metadata_stripper.strip_png
import zlib
```

## 🏛️ Classes (5)

### `TestDetectFormat`
**Methods:** `test_01_jpeg, test_02_png, test_03_unknown`

### `TestStripJpeg`
**Methods:** `test_04_keeps_soi, test_05_keeps_eoi, test_06_removes_app0`

### `TestStripPng`
**Methods:** `test_07_keeps_signature, test_08_removes_text_chunks`

### `TestStripMetadata`
**Methods:** `test_09_jpeg_strip, test_10_png_strip`

### `TestDeterminism`
**Methods:** `test_11_1000_runs`

## ⚡ Functions (1)

### `def _crc(chunk_type_and_data):`
