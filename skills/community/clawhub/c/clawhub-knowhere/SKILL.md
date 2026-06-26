---
name: knowhere
description: Use the Knowhere OpenClaw plugin to ingest local files or URLs, search stored documents, inspect parsed results, check jobs, and clean up stored document state.
user-invocable: false
metadata: {"openclaw":{"homepage":"https://github.com/Ontos-AI/knowhere-openclaw-plugin","requires":{"config":["plugins.entries.knowhere.enabled"]}}}
---

# Knowhere Skill

This ClawHub skill depends on the Knowhere OpenClaw plugin and teaches agents
how to use the `knowhere_*` tools well.

## Prerequisite

Install the plugin before using this skill:

```bash
openclaw plugins install @ontos-ai/knowhere-claw
```

Then enable the `knowhere` plugin entry in OpenClaw and restart OpenClaw.

## When to Use Knowhere

Use Knowhere when the user wants to:

- ingest a local file or URL into the current scope
- inspect, summarize, or quote previously ingested documents
- inspect ingest jobs or import a completed Knowhere job
- preview, list, remove, or clear stored documents
- understand what fields exist inside the stored result package

Do not assume an uploaded attachment was already ingested. If the user asks you
to use an attached file and no existing Knowhere result already covers it, call
`knowhere_ingest_document`.

## Tool Selection

- `knowhere_ingest_document` for new local files or URLs
- `knowhere_list_documents` to find candidate `docId` values in the current scope
- `knowhere_preview_document` for a quick structural overview
- `knowhere_grep` for text search across chunk fields
- `knowhere_read_result_file` for `manifest.json`, `hierarchy.json`, `kb.csv`, table HTML, or other text-like files under `result/`
- `knowhere_list_jobs`, `knowhere_get_job_status`, and `knowhere_import_completed_job` for async jobs
- `knowhere_remove_document` and `knowhere_clear_scope` for cleanup

After ingesting a document, use the returned identifiers for follow-up
operations instead of guessing names.

## Recommended Workflow

1. Ingest or import the document if it is not already in the store.
2. Call `knowhere_list_documents` if you need to confirm the right `docId`.
3. Call `knowhere_preview_document` to get a structural overview.
4. Call `knowhere_grep` with `conditions: [{ pattern: "your query" }]` for the default text search path.
5. Narrow by `chunk.path`, `chunk.type`, or other conditions when needed.
6. Call `knowhere_read_result_file` for `manifest.json`, `hierarchy.json`, `kb.csv`, or table HTML when the answer depends on raw package data.

## Response Style

Keep tool-driven replies short and labeled.

- Reuse labels such as `Scope`, `Source`, `File`, `Chunks`, `Job ID`, and `Next`
- Prefer one short status line plus the key fields the user needs for the next step
- Keep `path` in your reasoning and answers when possible
- Cite `chunkId` and `path` when answering from retrieved chunks

## Retrieval Rules

- Prefer `knowhere_grep` for text search
- Use `knowhere_preview_document` before broad reads when the document is large or the relevant branch is unclear
- For image or table questions, inspect matching `image` or `table` chunks and related manifest asset entries before answering
- Do not rely on `full.md` alone when the question depends on exact structure, tables, or images
- When a tool response contains `truncatedStrings: true`, retry with a higher `maxStringChars` before answering

## Attachment Markers

When a prompt contains a marker like:

```text
[media attached: /absolute/path/to/file.pdf (application/pdf) | handbook.pdf]
```

Use:

- the exact absolute path as `filePath`
- the visible filename as `fileName`

## Tool Usage Examples

Ingest a local file:

```json
{
  "filePath": "/tmp/uploads/handbook.pdf",
  "fileName": "handbook.pdf"
}
```

Ingest a URL:

```json
{
  "url": "https://example.com/report-2026.pdf",
  "title": "Q1 Report"
}
```

Preview a document:

```json
{
  "docId": "handbook-1234"
}
```

Search across chunk fields:

```json
{
  "docId": "paper-pdf-a370ef58",
  "conditions": [{ "pattern": "npm audit" }]
}
```

Read manifest JSON:

```json
{
  "docId": "handbook-1234",
  "filePath": "manifest.json",
  "mode": "json"
}
```
