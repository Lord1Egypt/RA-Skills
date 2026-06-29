# 📄 `axiom_css_specificity.py`

**Path:** `/run/media/axioma/Merlin/axiom-skills-public/axiom-css-specificity/axiom_css_specificity.py`  
**Size:** 10,457 bytes / 344 lines  
**Hash:** `a9f989f00e941edd`  
**Generated:** 2026-06-15T03:00:47.177534+00:00

## 📝 Module Docstring

```
🛠️ axiom-css-specificity — CSS Specificity Calculator
======================================================

⚠️ LIMITATIONS CONNUES :
- Ne gère pas @scope (trop récent)
- :is() / :not() : on prend la spécificité max des arguments
- Pas de résolution !important (CSS Cascade layer)

CALCULE LA SPÉCIFICITÉ D'UN SÉLECTEUR CSS (a, b, c)

Usage CLI:
    python3 axiom_css_specificity.py "#header .nav a:hover"
    python3 axiom_css_specificity.py "div.container > p.error" --compare ".error"
```

## 📦 Imports (5)

```python
import re
import sys
import argparse
import json
import json
```

## ⚡ Functions (9)

### `def _split_outside_parens(selector):`
> Split a selector into [outside-paren, (paren-content, paren-content, ...)]
using depth tracking. Yields ('outer', text) and ('inner', text) tuples.
The outer keeps the opening '(' so we can detect fun

### `def _spec_outer(text):`
> Compute specificity of a flat string (no parens).
Returns (a, b, c).

### `def _spec_inner(text, pseudo_name):`
> Compute specificity contributed by a :pseudo(arg) inner content.
For :is/:not/:has: returns max of args.
For :where: returns (0, 0, 0) always.

### `def _calculate_single(selector):`
> Specificity of a single compound/complex selector (no top-level commas).

### `def _process_outer_with_pending(part):`
> Process an outer segment, tracking pending pseudo for inner.

### `def calculate(selector):`
> Calcule la spécificité d'un sélecteur CSS complet.

Per W3C CSS Selectors Level 4:
- a = ID selectors
- b = class, attribute, pseudo-class
- c = type, pseudo-element

For comma-separated selector list

### `def format_specificity(spec):`
> Format specificity as (a, b, c) string.

### `def compare(selector_a, selector_b):`
> Compare specificity of two selectors.

### `def main():`
