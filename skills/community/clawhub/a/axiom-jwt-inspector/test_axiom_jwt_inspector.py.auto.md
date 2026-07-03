# 📄 `test_axiom_jwt_inspector.py`

**Path:** `/run/media/axioma/Merlin/axiom-skills-public/axiom-jwt-inspector/test_axiom_jwt_inspector.py`  
**Size:** 2,904 bytes / 95 lines  
**Hash:** `9a7ae10a188a55b8`  
**Generated:** 2026-06-15T03:00:47.166067+00:00

## 📝 Module Docstring

```
Tests — axiom-jwt-inspector 
```

## 📦 Imports (7)

```python
import pathlib.Path
import sys
import time
import unittest
import axiom_jwt_inspector.create
import axiom_jwt_inspector.decode
import axiom_jwt_inspector.verify_hmac
```

## 🏛️ Classes (4)

### `TestDecode`
**Methods:** `setUp, test_01_decode, test_02_header, test_03_exp_info, test_04_expired, test_05_invalid_format, test_06_two_parts, test_07_empty`

### `TestVerifyHmac`
**Methods:** `setUp, test_08_valid_hmac, test_09_wrong_secret, test_10_alg_not_supported`

### `TestCreate`
**Methods:** `test_11_roundtrip, test_12_alg_hs512`

### `TestDeterminism`
**Methods:** `test_13_1000_decodes`
