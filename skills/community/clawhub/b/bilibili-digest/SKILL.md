---
slug: bilibili-digest
name: Bilibili Digest / B站内容提取助手
version: 1.0.0
author: Golden Bean (coder)
category: Content Extraction
description: Extract, structure, and summarize Bilibili video/column content into structured notes with timestamps, key points, and chapter indexes.
model: deepseek/deepseek-v4-flash
input_schema: schemas/input.schema.json
output_schema: schemas/output.schema.json
---

# Bilibili Digest Skill

Extract Bilibili (B站) video/column content and transform it into structured, note-ready Markdown with AI-generated summaries, timestamped key points, chapter segmentation, and cross-video integration.

## How It Works

This skill operates in a pipeline:

1. **Parse** – Extract BV/column ID from any Bilibili URL (including `b23.tv` short links)
2. **Fetch** – Retrieve video metadata (title, author, duration, views), CC subtitles, and danmaku via Bilibili public APIs
3. **Segment** – Auto-detect video chapters from timestamps or subtitle gaps
4. **Summarize** – Call LLM (DeepSeek) to generate structured summary, key points, resources, and action steps
5. **Export** – Output as Markdown (default), Obsidian, JSON, or prepare for Notion/Feishu

### Fallback Strategy for Missing Subtitles

If a video has no CC subtitles, the skill degrades gracefully:
- Generate a summary from title + description + danmaku highlights
- Prompt the user to paste their own notes as enrichment

### API Rate Limiting

- Minimum 1-second interval between Bilibili API calls
- Exponential backoff retry (max 3 attempts) on 429 / timeout
- Local cache (24h TTL) at `~/.openclaw/data/bilibili-digest/cache/`

## Usage

```
clawhub run bilibili-digest --url <bilibili-url> [options]
```

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--url` | string | required | Single Bilibili URL |
| `--urls` | json-array | — | Multiple URLs for batch processing |
| `--summary-mode` | enum | `detailed` | `minimal`, `overview`, `detailed`, `mindmap` |
| `--include-transcript` | bool | false | Include full transcript text |
| `--include-danmaku` | bool | false | Include danmaku sentiment analysis |
| `--export-format` | enum | `markdown` | `markdown`, `json`, `obsidian`, `notion`, `feishu` |
| `--output-dir` | string | `./bilibili-notes/` | Output directory |
| `--cross-video-merge` | bool | false | Merge insights across multiple videos |
| `--language` | enum | `zh-CN` | `zh-CN`, `en-US` |

## Sample Prompts

### 1. Extract a single video into structured notes (most common)
```text
clawhub run bilibili-digest --url "https://www.bilibili.com/video/BV1xx411c7mD"
# → Structured Markdown with title, author, key points (with timestamps), chapters, resources
```

### 2. Batch process a tutorial series with cross-video merge
```text
clawhub run bilibili-digest \
  --urls '["https://www.bilibili.com/video/BV1xx01","https://www.bilibili.com/video/BV1xx02"]' \
  --cross-video-merge
# → Combined knowledge tree across multiple videos
```

### 3. Quick minimal summary for social sharing
```text
clawhub run bilibili-digest --url "https://www.bilibili.com/video/BV1xx411c7mD" \
  --summary-mode minimal
# → One-liner + 3-5 core bullet points
```

### 4. Export in Obsidian format with full transcript
```text
clawhub run bilibili-digest --url "https://www.bilibili.com/video/BV1xx411c7mD" \
  --summary-mode detailed --export-format obsidian --include-transcript
# → Obsidian-compatible note with WikiLinks, tags, and YAML frontmatter
```

### 5. Mindmap summary for quick review
```text
clawhub run bilibili-digest --url "https://www.bilibili.com/video/BV1xx411c7mD" \
  --summary-mode mindmap
# → Hierarchical mindmap with main topics, subtopics, and key connections,
#   ideal for sharing or importing into mind-mapping tools (XMind, etc.)
```

## First-Success Path

```
Step 1: Install → clawhub install bilibili-digest
Step 2: Run → clawhub run bilibili-digest --url "https://www.bilibili.com/video/BV1xx411c7mD"
Step 3: Receive → Structured Markdown note (<30 seconds)
Step 4: Copy to note-taking app → Value achieved
```

## Core Scripts

The `scripts/` directory contains Python modules:

| File | Purpose |
|------|---------|
| `parser.py` | Extract BV/CV IDs and expand `b23.tv` short links |
| `api.py` | Bilibili API client with rate limiting and retry |
| `subtitle.py` | CC subtitle extraction and cleanup |
| `danmaku.py` | Danmaku density detection and sentiment grouping |
| `segmenter.py` | Chapter detection from subtitle gaps and transition words |
| `summarizer.py` | LLM-based structured summary generation |
| `exporter.py` | Markdown / Obsidian / JSON / Notion / Feishu export |
| `cross_merge.py` | Cross-video knowledge merging |
| `__init__.py` | Package init |
