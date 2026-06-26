---
name: batch-file-processor
description: >
  Parallel batch processing of large file sets using sub-agents (summarize, analyze, extract, transform).
  Use when performing the same operation across many files in a directory, such as generating file indexes/summaries,
  batch content analysis, bulk information extraction, or format conversion.
  Triggers: batch process, file index, directory summary, bulk analyze, summarize files.
  NOT for: single file operations (just read it directly), fewer than 5 files (manual is faster).
---

# Batch File Processor

Process large numbers of files in parallel using sub-agents, avoiding main agent context overflow.

## Workflow

### 1. List files

```bash
find <directory> -type f -name "*.md" | sort
```

### 2. Group

Split into batches of 2-4 files each (3 is optimal).

### 3. Dispatch sub-agents

One sub-agent per batch. Task template:

```
Read the following files completely and generate a brief summary (under 50 words) for each.
1. /path/to/file1.md
2. /path/to/file2.md
3. /path/to/file3.md
Return ONLY a JSON array:
[{"file": "relative/path/file1.md", "summary": "..."},...]
```

Key parameters:
- `mode`: "run" (one-shot task)
- `runTimeoutSeconds`: 120 (increase to 180 for large files)
- `label`: descriptive label, e.g. `idx-project-batch1`

### 4. Collect results

Sub-agents push results on completion. Use `sessions_yield` to wait and collect incrementally.

### 5. Compile output

Once all results are in, the main agent compiles the final deliverable (index file, report, etc.).

## Rules

- **2-4 files per sub-agent** — never let one sub-agent process an entire directory sequentially
- **Read full file content** — no head/tail truncation; partial reads produce incomplete summaries
- **Standardize output format** — JSON makes it easy for the main agent to parse and merge
- **One spawn per turn** — system limitation; use multiple spawn + yield cycles

## Anti-patterns

| Mistake | Consequence |
|---------|-------------|
| `head -20` to skim file headers | Poor summary quality, key information missed |
| One sub-agent processes entire directory | Context overflow, timeout failure |
| Main agent reads all files sequentially | Context window exhausted, later files unreadable |
| One sub-agent per large directory | Large directories timeout, small ones waste capacity |

## Benchmarks

70 files → 25 sub-agents (3 files each) → parallel execution → completed in 5 minutes → high accuracy summaries

## Task Template Variants

### File summarization (default)
```
Generate a brief summary (under 50 words) for each file.
```

### Information extraction
```
Extract the following fields from each file: project name, budget, key contacts, risks.
Return JSON: [{"file": "...", "project": "...", "budget": "...", "contacts": [...], "risks": [...]}]
```

### Content classification
```
Classify each file by checking for these topics: security, compliance, migration.
Return JSON: [{"file": "...", "has_security": true/false, "has_compliance": true/false, "has_migration": true/false}]
```

### Code analysis
```
Analyze each source file: count lines, list imports/dependencies, identify main functions.
Return JSON: [{"file": "...", "lines": N, "imports": [...], "main_functions": [...]}]
```
