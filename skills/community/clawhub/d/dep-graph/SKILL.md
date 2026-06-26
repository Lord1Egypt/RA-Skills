---
name: dep-graph
description: Analyze and visualize project dependency trees from manifest files. Supports Node.js (package.json), Python (requirements.txt, pyproject.toml), Go (go.mod), Rust (Cargo.toml), Ruby (Gemfile), and PHP (composer.json). Use when asked to list dependencies, show a dependency tree, check what packages a project uses, compare prod vs dev deps, or audit dependency counts.
---

# Dep Graph

Parse and display project dependency trees from manifest files. Auto-detects project type.

## Quick Start

```bash
# Analyze current project
python3 scripts/dep_graph.py

# Analyze specific directory
python3 scripts/dep_graph.py /path/to/project

# JSON output
python3 scripts/dep_graph.py --json

# Summary only (just counts)
python3 scripts/dep_graph.py --summary

# Force project type
python3 scripts/dep_graph.py --type node

# Hide version constraints
python3 scripts/dep_graph.py --no-versions
```

## Supported Project Types

| Type | Manifest File | Groups |
|------|--------------|--------|
| Node.js | `package.json` | production, dev, peer |
| Python | `requirements.txt` | production |
| Python | `pyproject.toml` | production |
| Go | `go.mod` | production, indirect |
| Rust | `Cargo.toml` | production, dev |
| Ruby | `Gemfile` | production, dev |
| PHP | `composer.json` | production, dev |

Auto-detects multiple manifest files in the same project and reports all.

## Output

Tree view shows dependencies grouped by type (production/dev/peer) with version constraints. Use `--json` for programmatic processing or `--summary` for quick counts.

## Dependencies

- Python 3.8+ (stdlib only, no pip packages needed)
