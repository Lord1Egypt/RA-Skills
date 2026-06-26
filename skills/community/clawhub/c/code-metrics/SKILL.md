---
name: code-metrics
description: Analyze code quality metrics including lines of code by language, cyclomatic complexity (Python), function/class counts, comment ratios, and largest file rankings. Use when asked to analyze code quality, count lines of code, measure complexity, find the biggest files, get a project overview, or audit code metrics across a codebase. Supports Python, JavaScript, TypeScript, Go, Rust, Ruby, Java, C/C++, C#, Swift, Kotlin, PHP, Shell, Lua, R, and Scala.
---

# Code Metrics

Analyze code quality and complexity metrics across your project. Supports 17+ languages.

## Quick Start

```bash
# Analyze current project
python3 scripts/code_metrics.py

# Analyze specific directory
python3 scripts/code_metrics.py /path/to/project

# JSON output
python3 scripts/code_metrics.py --json

# Skip complexity analysis (faster)
python3 scripts/code_metrics.py --no-complexity

# Exclude additional directories
python3 scripts/code_metrics.py --exclude migrations fixtures
```

## Metrics Provided

- **Lines of Code** — total, code, comments, blank lines per language
- **Comment-to-code ratio** — overall documentation density
- **Function & class counts** — per language
- **Cyclomatic complexity** — per-function for Python files (AST-based)
- **Largest files** — top N files ranked by code lines
- **High complexity warnings** — flags functions with complexity ≥5

## Complexity Scale (Python)

| Range | Risk | Meaning |
|-------|------|---------|
| 1-4 | 🟢 Low | Simple, well-structured |
| 5-9 | 🟢 Moderate | Acceptable |
| 10-14 | 🟡 High | Consider refactoring |
| 15+ | 🔴 Very High | Refactor strongly recommended |

## Dependencies

- Python 3.8+ (stdlib only, no pip packages needed)
