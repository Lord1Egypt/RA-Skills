# 📄 `test_axiom_url_canonicalizer.py`

**Path:** `/run/media/axioma/Merlin/axiom-skills-public/axiom-url-canonicalizer/test_axiom_url_canonicalizer.py`  
**Size:** 4,180 bytes / 153 lines  
**Hash:** `99e9a5efda46168a`  
**Generated:** 2026-06-15T03:00:47.168606+00:00

## 📝 Module Docstring

```
Tests — axiom-url-canonicalizer 
```

## 📦 Imports (6)

```python
import pathlib.Path
import sys
import unittest
import axiom_url_canonicalizer.analyze
import axiom_url_canonicalizer.canonicalize
import axiom_url_canonicalizer.urls_equivalent
```

## 🏛️ Classes (6)

### `TestCanonicalizeBasic`
**Methods:** `test_01_lowercase_scheme, test_02_lowercase_host, test_03_strip_default_port_http, test_04_strip_default_port_https, test_05_keep_non_default_port, test_06_strip_fragment, test_07_keep_fragment`

### `TestCanonicalizeQuery`
**Methods:** `test_08_sort_query, test_09_remove_tracking, test_10_keep_blank`

### `TestCanonicalizePath`
**Methods:** `test_11_resolve_dot, test_12_resolve_dotdot, test_13_multiple_slashes, test_14_decode_unreserved, test_15_force_trailing`

### `TestCanonicalizeScheme`
**Methods:** `test_16_force_https, test_17_no_scheme`

### `TestEquivalence`
**Methods:** `test_18_equivalent, test_19_not_equivalent`

### `TestDeterminism`
**Methods:** `test_20_1000_runs`
