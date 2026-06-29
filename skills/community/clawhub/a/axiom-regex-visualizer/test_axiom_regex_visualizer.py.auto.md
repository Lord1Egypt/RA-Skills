# 📄 `test_axiom_regex_visualizer.py`

**Path:** `/run/media/axioma/Merlin/axiom-skills-public/axiom-regex-visualizer/test_axiom_regex_visualizer.py`  
**Size:** 2,914 bytes / 97 lines  
**Hash:** `f323b04d96174eec`  
**Generated:** 2026-06-15T03:00:47.198389+00:00

## 📝 Module Docstring

```
Tests — axiom-regex-visualizer 
```

## 📦 Imports (6)

```python
import pathlib.Path
import sys
import unittest
import axiom_regex_visualizer.explain
import axiom_regex_visualizer.tokenize
import axiom_regex_visualizer.visualize
```

## 🏛️ Classes (4)

### `TestTokenize`
**Methods:** `test_01_literals, test_02_digit, test_03_quantifier_star, test_04_quantifier_plus, test_05_quantifier_question, test_06_quantifier_exact, test_07_quantifier_range, test_08_group_capture, test_09_group_noncapture, test_10_anchors`
_(+2 more)_

### `TestVisualize`
**Methods:** `test_13_email, test_14_doesnt_crash`

### `TestExplain`
**Methods:** `test_15_simple, test_16_quantifier`

### `TestDeterminism`
**Methods:** `test_17_1000_runs`
