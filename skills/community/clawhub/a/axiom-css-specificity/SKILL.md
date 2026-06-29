---
name: axiom-css-specificity
description: CSS specificity calculator — compute (a, b, c) specificity for any CSS selector. Handles :is(), :not(), :where(), combinators, attribute selectors. Use when you need to debug CSS conflicts. Pure stdlib, no LLM.
version: 0.1.2
license: Apache-2.0
---

# axiom-css-specificity

**Version:** 0.1.2
**Axioma Tools**

Computes CSS specificity per W3C Selectors Level 4.

## What this skill does

- Computes (a, b, c) tuple per W3C spec
- Handles :is(), :not(), :where() (where() = 0)
- Handles attribute selectors, pseudo-classes
- Supports combinators (>, +, ~, descendant)
- JSON output with breakdown

## When to use this skill

- ✅ Debug CSS specificity conflicts
- ✅ Audit CSS for overly-broad selectors
- ✅ Compare specificity of two rules
- ❌ Render CSS (use a browser)
- ❌ Support CSS preprocessor syntax (SCSS/Less)

## Usage

```bash
python3 axiom_css_specificity.py "body div#main .item:first-child"
python3 axiom_css_specificity.py --compare "a" "div.menu a"
```

```python
from axiom_css_specificity import compute_specificity
compute_specificity('div#main a:hover')  # (0, 2, 2)
```

## Validation

| Check | Status |
|-------|--------|
| Unit tests | 18 cases |
| Performance | <100ms |
| Security | Pure stdlib, no injection |
| Determinism | Byte-to-byte stable |
| License | Apache-2.0 |

_Last updated: 2026-06-14_
