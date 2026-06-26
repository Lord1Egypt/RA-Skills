---
name: demo-archiver
description: A demo skill for archiving and organizing files into a structured resource library.
metadata: { "openclaw": { "emoji": "📦" } }
---

# Demo Archiver

Archive files into a structured directory with metadata tracking.

## Usage

1. Place source files in the skill's `incoming/` directory.
2. Run the archive script to move files into `archive/YYYY-MM/` with a metadata sidecar JSON.
3. Review the archive index at `archive/index.json`.
