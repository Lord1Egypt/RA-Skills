---
name: codebase-stats
description: >
  Analyze project metrics: lines of code, language distribution, function complexity,
  code-to-comment ratio, test coverage indicators, dependency counts, largest files,
  and tech debt signals (TODOs, FIXMEs, HACKs). Supports 40+ languages.
  Use when asked to analyze a codebase, count lines of code, check code complexity,
  get project statistics, audit code quality, measure tech debt, or understand
  language distribution in a project.
  Triggers on "codebase stats", "lines of code", "LOC", "code complexity",
  "project metrics", "code quality", "tech debt", "language distribution",
  "project size", "code analysis", "cyclomatic complexity".
---

# Codebase Stats

Project metrics, complexity analysis, and health indicators. Pure Python, zero deps, 40+ languages.

## Quick Start

```bash
# Analyze current directory
python3 scripts/codebase_stats.py

# Analyze specific project
python3 scripts/codebase_stats.py /path/to/project

# Markdown report
python3 scripts/codebase_stats.py /path/to/project --format markdown

# JSON (for CI/CD dashboards)
python3 scripts/codebase_stats.py /path/to/project --format json

# Filter by language
python3 scripts/codebase_stats.py --language Python

# Save report
python3 scripts/codebase_stats.py --format markdown --output stats.md
```

## What It Measures

| Category | Metrics |
|----------|---------|
| **Size** | Total files, code/comment/blank lines, lines per file |
| **Languages** | Distribution by code lines and file count (40+ languages) |
| **Complexity** | Per-function cyclomatic complexity estimate, top complex functions |
| **Quality** | Code-to-comment ratio, test file coverage indicator |
| **Dependencies** | npm, pip, Go modules, Cargo crate counts |
| **Tech Debt** | TODO/FIXME/HACK/XXX counts across codebase |
| **Files** | Top 10 largest files by line count |

## Supported Languages

Python, JavaScript, TypeScript, Java, Go, Rust, Ruby, PHP, C, C++, C#, Swift,
Kotlin, Scala, R, Lua, Perl, Shell, SQL, HTML, CSS, SCSS, Vue, Svelte, Dart,
Elixir, Erlang, Zig, Nim, V, Solidity, Terraform, Protobuf, and more.

## Exit Codes

- `0` — Success
- `1` — Error (directory not found, language not found)
