# 📄 `test_axiom_markdown_link_auditor.py`

**Path:** `/run/media/axioma/Merlin/axiom-skills-public/axiom-markdown-link-auditor/test_axiom_markdown_link_auditor.py`  
**Size:** 2,606 bytes / 93 lines  
**Hash:** `adec323b1209df4a`  
**Generated:** 2026-06-15T03:00:47.182483+00:00

## 📝 Module Docstring

```
Tests — axiom-markdown-link-auditor 
```

## 📦 Imports (7)

```python
import pathlib.Path
import sys
import unittest
import axiom_markdown_link_auditor.BARE_URL_PATTERN
import axiom_markdown_link_auditor.audit
import axiom_markdown_link_auditor.check_url
import axiom_markdown_link_auditor.extract_links
```

## 🏛️ Classes (4)

### `TestExtractLinks`
**Methods:** `test_01_simple_link, test_02_image, test_03_bare_url, test_04_mixed, test_05_line_numbers, test_06_empty`

### `TestCheckUrl`
**Methods:** `test_07_skip_non_http, test_08_invalid_url`

### `TestAudit`
**Methods:** `test_09_basic, test_10_no_remote`

### `TestDeterminism`
**Methods:** `test_11_1000_runs`
