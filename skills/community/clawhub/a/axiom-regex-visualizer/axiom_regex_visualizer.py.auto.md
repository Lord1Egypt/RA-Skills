# 📄 `axiom_regex_visualizer.py`

**Path:** `/run/media/axioma/Merlin/axiom-skills-public/axiom-regex-visualizer/axiom_regex_visualizer.py`  
**Size:** 8,510 bytes / 276 lines  
**Hash:** `4ee57d02237d7c52`  
**Generated:** 2026-06-15T03:00:47.197849+00:00

## 📝 Module Docstring

```
🛠️ axiom-regex-visualizer — Regex Pattern Visualizer
======================================================

⚠️ LIMITATIONS CONNUES :
- Pas de support des lookbehind complexes
- Pas de backref visualization
- Pas de Unicode property visualization

VISUALISE UN PATTERN REGEX EN STRUCTURE LISIBLE
```

## 📦 Imports (3)

```python
import re
import sys
import argparse
```

## ⚡ Functions (4)

### `def tokenize(pattern):`
> Tokenize a regex pattern into a list of (type, value) tuples.

Returns a list of tokens for visualization.

### `def visualize(pattern, indent):`
> Return a human-readable visualization of a regex pattern.

### `def explain(pattern):`
> Plain-English explanation of the pattern.

### `def main():`
