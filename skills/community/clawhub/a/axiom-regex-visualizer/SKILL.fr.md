---
name: axiom-regex-visualizer
description: Visualiseur de regex — parse n'importe quelle regex et visualise sa structure (groupes, quantificateurs, ancres, classes de caractères). Utilisez pour comprendre ou documenter. Stdlib pur, sans LLM.
version: 0.1.2
license: Apache-2.0
---

# axiom-regex-visualizer

**Version:** 0.1.2
**Axioma Tools**

Parse les expressions régulières et montre leur structure visuellement.

## What this skill does

- Arbre visuel des composants regex
- Explication en français de chaque partie
- Highlight des groupes, quantificateurs, ancres
- Supporte la syntaxe Python re (basic + extensions)

## When to use this skill

- ✅ Comprendre une regex que tu n'as pas écrite
- ✅ Documenter un pattern complexe
- ✅ Débugger des problèmes de matching
- ❌ Tester si une regex matche (utilise re.match)
- ❌ Supporter les features Perl/PCRE-only

## Usage

```bash
python3 axiom_regex_visualizer.py "^(?:[a-z0-9!#$%&*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&*+/=?^_`{|}~-]+)*)@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"
```

```python
from axiom_regex_visualizer import parse, explain
tree = parse(r'\b\d{3}-\d{4}\b')
explain(tree)  # 'Frontière de mot, exactement 3 chiffres, tiret, exactement 4 chiffres, frontière de mot'
```

## Validation

| Check | Status |
|-------|--------|
| Unit tests | 20+ cases |
| Performance | <100ms |
| Security | Pure stdlib, no injection |
| Determinism | Byte-to-byte stable |
| License | Apache-2.0 |

_Last updated: 2026-06-14_
