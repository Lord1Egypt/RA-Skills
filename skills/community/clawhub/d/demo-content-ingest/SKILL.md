---
name: demo-content-ingest
description: A demonstration skill for content ingestion workflows. Checks a workspace folder for text/markdown assets, generates a simple inventory report, and prints a summary. Useful as a minimal example for pipeline-driven publishing.
metadata: { "openclaw": { "emoji": "📦" } }
---

# Demo Content Ingest

A minimal demonstration skill that scans a workspace folder and produces an inventory of text assets.

## When to Use

- You need a trivial skill to test a content pipeline or CI/CD publishing flow.
- You want a concrete example folder structure for ClawHub ingestion.

## What It Does

1. Reads a target directory.
2. Lists files matching `*.md` or `*.txt`.
3. Outputs a count and a brief listing.

## Steps

1. Set `TARGET_DIR` to an absolute path (default: current directory).
2. Run:
   ```bash
   find "$TARGET_DIR" -maxdepth 1 -type f \( -name "*.md" -o -name "*.txt" \) | sort
   ```
3. Count results and print a one-line summary.

## Notes

- This skill is intentionally lightweight to serve as a publishing demo.
- For production use, extend with logging, error handling, and metadata extraction.
