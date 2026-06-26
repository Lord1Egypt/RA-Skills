---
name: code-complexity-analyzer
description: Measure cyclomatic complexity, cognitive complexity, and structural metrics for Python, JavaScript/TypeScript, and Go code. Use when analyzing code quality, finding complex functions, setting CI quality gates, reviewing code for refactoring candidates, or generating complexity reports. Supports per-function metrics, configurable thresholds, risk levels, and multiple output formats (text, JSON, markdown).
---

# Code Complexity Analyzer

Measure cyclomatic, cognitive, and structural complexity per function. Pure Python, no dependencies.

## Quick Start

```bash
# Analyze a directory
python3 scripts/analyze_complexity.py src/

# Analyze specific files
python3 scripts/analyze_complexity.py app.py utils.py

# Show all functions (not just violations)
python3 scripts/analyze_complexity.py src/ --verbose

# Custom thresholds
python3 scripts/analyze_complexity.py src/ --cc 15 --cog 20 --max-lines 80
```

## Output Formats

```bash
python3 scripts/analyze_complexity.py src/ --format text      # human-readable (default)
python3 scripts/analyze_complexity.py src/ --format json       # CI/tooling
python3 scripts/analyze_complexity.py src/ --format markdown   # reports
```

## Supported Languages

- Python (`.py`)
- JavaScript (`.js`, `.jsx`, `.mjs`, `.cjs`)
- TypeScript (`.ts`, `.tsx`)
- Go (`.go`)

## Metrics

| Metric | Description | Default Threshold |
|--------|-------------|-------------------|
| Cyclomatic (CC) | Independent execution paths | ≤10 |
| Cognitive (COG) | Perceived difficulty to understand (nesting-weighted) | ≤15 |
| Lines | Function length | ≤50 |
| Params | Parameter count | ≤5 |
| Nesting | Max nesting depth | ≤4 |

## Risk Levels

- 🟢 **Simple** — CC≤5, COG≤8
- 🟡 **Low** — CC≤10, COG≤15
- 🟠 **Moderate** — CC≤20, COG≤25
- 🔴 **High** — CC>20 or COG>25

## Options

```
--cc N           Cyclomatic threshold (default: 10)
--cog N          Cognitive threshold (default: 15)
--max-lines N    Function length threshold (default: 50)
--max-params N   Parameter count threshold (default: 5)
--max-nesting N  Nesting depth threshold (default: 4)
--exclude DIR    Additional directories to exclude
--verbose, -v    Show all functions, not just violations
```

Auto-excluded: `node_modules`, `.git`, `__pycache__`, `venv`, `dist`, `build`.

## Exit Codes

- `0` — no violations
- `1` — violations found (functions exceed CC or COG thresholds)
- `2` — no analyzable files found
