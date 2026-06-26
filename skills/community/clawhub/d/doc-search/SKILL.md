---
name: doc-search
description: Search a local document library (Obsidian vault, wiki, notes, etc.) using BM25 inverted index + LLM query expansion + grep for precise location. Use when the user asks to find, look up, or search for information in their local docs/notes/vault.Triggers on "find in docs", "look up X in vault", "搜索文档", "查找笔记", "文档里有没有"
---

# Doc Search

BM25 inverted index + LLM query expansion + grep. Zero external dependencies.

## Workflow

Follow these steps in order every time:

### Step 1 — Resolve docs_dir

Check if the user mentioned a docs directory. If not, ask:
> "Which directory should I search? (e.g. ~/obsidian, ~/notes)"

### Step 2 — Check index exists

```bash
ls <docs_dir>/.cache/index.json
```

- If missing → go to Step 3 (build index first)
- If exists → skip to Step 4

### Step 3 — Build index

```bash
python3 ~/.claude/skills/doc-search/scripts/build_index.py <docs_dir>
```

Index saved to `<docs_dir>/.doc-search/index.json`. Incremental on subsequent runs.

### Step 4 — Expand query terms

Before searching, expand the user's query to cover synonyms, Chinese/English variants, and likely headings. Combine into one string:

```
"获取音色列表" → "获取 查询 list voice 音色 tts ListVoice 音色列表"
```

### Step 5 — BM25 search

```bash
python3 ~/.claude/skills/doc-search/scripts/search.py "<expanded query>" \
  --docs-dir <docs_dir> --topk 5
```

Output: JSON array `[{path, rel, score, title, summary}, ...]`

### Step 6 — Grep top-K for precise location

For each result file, grep with the original keywords:

```bash
grep -ni -e "keyword1" -e "keyword2" /path/to/doc.md
```

Report file path + matching line numbers to the user.

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--topk` | `5` | Number of BM25 results |
| `--ext` | `md,txt,rst,org` | File extensions to index |
| `--index` | `<docs_dir>/.doc-search/index.json` | Override index path |
