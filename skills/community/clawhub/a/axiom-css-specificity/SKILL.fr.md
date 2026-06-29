---
name: axiom-css-specificity
description: Calculateur de spécificité CSS — calcule la spécificité (a, b, c) pour tout sélecteur CSS. Gère :is(), :not(), :where(), combinateurs, attribute selectors. Utilisez pour débugger les conflits CSS. Stdlib pur, sans LLM.
version: 0.1.2
license: Apache-2.0
---

# axiom-css-specificity

**Version:** 0.1.2
**Axioma Tools**

Calcule la spécificité CSS selon W3C Selectors Level 4.

## What this skill does

- Calcule le tuple (a, b, c) selon spec W3C
- Gère :is(), :not(), :where() (where() = 0)
- Gère attribute selectors, pseudo-classes
- Supporte les combinateurs (>, +, ~, descendant)
- Output JSON avec breakdown

## When to use this skill

- ✅ Débugger des conflits de spécificité CSS
- ✅ Auditer du CSS pour sélecteurs trop larges
- ✅ Comparer la spécificité de deux règles
- ❌ Rendre du CSS (utilise un navigateur)
- ❌ Supporter la syntaxe préprocesseur CSS (SCSS/Less)

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
