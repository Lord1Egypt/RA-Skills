---
name: axiom-regex-visualizer
description: Regex visualizer — parse any regex and visualize its structure (groups, quantifiers, anchors, character classes). Use when you need to understand or document a regex. Pure stdlib, no LLM.
version: 0.1.2
license: Apache-2.0
---

# axiom-regex-visualizer

**Version:** 0.1.2
**Axioma Tools**

Parses regular expressions and shows their structure visually.

## What this skill does

- Visual tree of regex components
- Plain-English explanation of each part
- Highlights groups, quantifiers, anchors
- Supports Python re syntax (basic + extensions)

## When to use this skill

- ✅ Understand a regex you didn't write
- ✅ Document a complex pattern
- ✅ Debug regex matching issues
- ❌ Test if regex matches a string (use re.match)
- ❌ Support Perl/PCRE-only features

## Usage

```bash
python3 axiom_regex_visualizer.py "^(?:[a-z0-9!#$%&*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&*+/=?^_`{|}~-]+)*)@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"
```

```python
from axiom_regex_visualizer import parse, explain
tree = parse(r'\b\d{3}-\d{4}\b')
explain(tree)  # 'Word boundary, exactly 3 digits, dash, exactly 4 digits, word boundary'
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
