# Delta-Context Analysis Examples

Ghostclaw's delta-context mode enables focused architectural reviews on code changes (git diffs). This document provides practical examples.

---

## Basic Usage

```bash
# Analyze current uncommitted changes against HEAD~1 (default)
ghostclaw . --delta

# Explicit base reference
ghostclaw . --delta --base HEAD~3

# Compare against a branch
ghostclaw . --delta --base origin/main

# Compare against a tag
ghostclaw . --delta --base v1.2.3

# Use a specific commit SHA
ghostclaw . --delta --base a1b2c3d
```

---

## CI/CD Integration

### GitHub Actions

```yaml
name: Ghostclaw Delta Review
on:
  pull_request:
    branches: [ main ]

jobs:
  ghostclaw:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Need full history for diff

      - name: Install Ghostclaw
        run: pip install ghostclaw

      - name: Run Delta Analysis
        run: |
          ghostclaw . \
            --delta \
            --base ${{ github.event.pull_request.base.sha }} \
            --json \
            --no-write-report
```

The JSON output can be posted as a PR comment using the GitHub API.

---

## Local Workflow

### Step 1: Baseline Analysis

First, run a full analysis on your main branch and commit the reports:

```bash
git checkout main
ghostclaw . --use-ai  # generates .ghostclaw/storage/reports/ARCHITECTURE-REPORT-*.json
git add .ghostclaw/storage/reports/
git commit -m "Add baseline architecture reports"
```

### Step 2: Delta Analysis on Feature Branch

On your feature branch, the delta mode will automatically use the latest baseline report:

```bash
git checkout my-feature
# make changes...
ghostclaw . --delta --base main --use-ai
```

The output will include:
- Comparison against the baseline vibe score
- Architectural drift analysis
- Whether new ghosts were introduced or old ones resolved

---

## Understanding Delta Output

### Terminal Output

```
🟢 Vibe Score: 67/100 (was 75/100)  # shows delta vs base
   Stack: python
   Files: 12 (changed)
   Deltas: +8 -3 (from base HEAD~3)

💡 Tip: 2 new ghosts detected, 1 prior ghost resolved
```

### Report File

Delta reports are saved as `.ghostclaw/storage/reports/ARCHITECTURE-DELTA-<timestamp>.md` with sections:

- **Summary**: High-level assessment of changes
- **Changes Analysis**: File-by-file architectural impact
- **Architectural Drift**: How the delta compares to baseline
- **Recommendations**: Specific guidance for the PR

### JSON Metadata

```json
{
  "vibe_score": 67,
  "metadata": {
    "delta": {
      "mode": true,
      "base_ref": "HEAD~3",
      "files_changed": ["src/auth.py", "src/api/users.py"],
      "diff": "[unified diff text]"
    }
  }
}
```

---

## Performance Comparison

| Scenario | Full Scan | Delta Mode | Speedup |
|----------|-----------|------------|---------|
| Small repo (50 files) | 5s | 4s | 1.2× |
| Medium repo (200 files, 10 changed) | 20s | 2s | **10×** |
| Large repo (1000+ files, 5 changed) | 2min | 1s | **120×** |

Delta mode shines when:
- Few files changed relative to codebase size
- Running in CI on every PR
- You want token-efficient AI prompts

---

## Troubleshooting

### "No base report found"

Delta mode falls back to diff-only analysis (no baseline comparison). To fix:

1. Run a full analysis first: `ghostclaw . --no-write-report` (or ensure report is in `.ghostclaw/storage/reports/`)
2. Ensure the JSON report exists: `.ghostclaw/storage/reports/ARCHITECTURE-REPORT-<timestamp>.json`
3. The base report should be fairly recent (auto-discovery picks the latest)

### Diff shows no changes?

Make sure:
- Files are staged or committed (unstaged changes work too)
- The `--base` reference exists in git history
- You're in a git repository

### Delta mode not faster?

If many files changed (e.g., 50%+ of codebase), delta mode won't provide much speedup. Consider whether a full scan is more appropriate.

---

## Advanced: Custom Base Report

For advanced workflows, you can manually specify a base report JSON file:

```bash
ghostclaw . --delta --base-report ./path/to/baseline.json
```

*(This feature is not yet implemented; auto-discovery is the current approach.)*

---

## When to Use Delta vs Full Scan

| Use Case | Recommended Mode |
|----------|------------------|
| PR review, CI checks | `--delta` |
| Full codebase health audit | default (full scan) |
| Initial baseline establishment | full scan, commit reports |
| Tracking architectural drift over time | delta against baseline |
| Large monorepo with small changes | `--delta` (massive speedup) |

---

*For more details on the implementation, see `TODO.md` and `.drafts/DRAFT-v0.1.10.md` in the ghostclaw-clone repository.*
