# 📄 `test_axiom_css_specificity.py`

**Path:** `/run/media/axioma/Merlin/axiom-skills-public/axiom-css-specificity/test_axiom_css_specificity.py`  
**Size:** 3,991 bytes / 126 lines  
**Hash:** `9b65f2226d07d132`  
**Generated:** 2026-06-15T03:00:47.176161+00:00

## 📝 Module Docstring

```
Tests — axiom-css-specificity 
```

## 📦 Imports (7)

```python
import pathlib.Path
import sys
import unittest
import axiom_css_specificity.EXAMPLES
import axiom_css_specificity.calculate
import axiom_css_specificity.compare
import axiom_css_specificity.format_specificity
```

## 🏛️ Classes (6)

### `TestBasic`
**Methods:** `test_01_universal, test_02_element, test_03_class, test_04_id, test_05_element_class, test_06_id_class`

### `TestCombined`
**Methods:** `test_07_id_class_pseudo, test_08_combinator, test_09_attribute, test_10_descendant`

### `TestPseudo`
**Methods:** `test_11_not, test_12_is, test_13_where, test_14_pseudo_element`

### `TestCompare`
**Methods:** `test_15_a_wins, test_16_tie`

### `TestExamples`
> Verify the built-in examples are all correct.
**Methods:** `test_17_all_examples`

### `TestDeterminism`
**Methods:** `test_18_1000_runs`
