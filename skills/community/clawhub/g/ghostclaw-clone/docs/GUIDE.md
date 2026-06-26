# Ghostclaw Guide

Ghostclaw is an architectural analysis tool for codebases. It examines your project's structure, metrics, and dependencies to produce a comprehensive report with a vibe score, architectural ghosts, and actionable suggestions.

## Core Concepts

1. **Stack Detection** – Identifies the primary technology (Python, Node, Go, etc.) via heuristics.
2. **File Scanning** – Recursively discovers source files, with optional parallel I/O for speed.
3. **Metrics Computation** – Calculates size, complexity, coupling, and file‑level health.
4. **Adapters** – Pluggable modules that add custom analyses (e.g., PySCN for Python dependencies, AI‑CodeIndex for index‑based insights).
5. **AI Synthesis** – Optionally sends metrics to an LLM to generate a narrative analysis.

## Output

Ghostclaw writes a markdown report (by default to `.ghostclaw/` locally) and optionally creates a GitHub PR with the findings. It also provides a terminal summary with issues, red flags, and tips.

## Getting Started

```bash
ghostclaw analyze .
ghostclaw analyze . --json > report.json
ghostclaw analyze . --create-pr
```

Explore the options for caching, parallelism, and AI integration to suit your workflow.
