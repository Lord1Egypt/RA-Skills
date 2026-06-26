---
name: easylink-easydoc-parse
description: "Use when tasks need EasyDoc REST API to convert unstructured documents into structured JSON or markdown on either China EasyLink platform or global EasyDoc platform. Trigger for requests about POST /v1/easydoc/parse and GET /v1/easydoc/parse/{task_id} (cn), POST /api/v1/parse and GET /api/v1/parse/{task_id}/result (global), selecting parse mode (cn: easydoc-parse-flash or easydoc-parse-premium, global: lite), normalizing parse output for LLM pipelines, and handling RAG retrieval against parsed JSON by using the host agent's text-search tool before any full-file loading."
metadata:
  short-description: Parse docs via EasyDoc CN and Global REST APIs
  openclaw:
    requires:
      env:
        - EASYLINK_API_KEY
        - EASYDOC_API_KEY
      bins:
        - python3
        - curl
    primaryEnv: EASYLINK_API_KEY
---

# EasyLink EasyDoc Parse

## Overview

Use this skill to call EasyDoc async parsing APIs and return stable structured output.
Always follow the same lifecycle: select platform, validate inputs, submit task, poll result, normalize output.

## RAG Retrieval

If the parsed output is being used for RAG, do not load the entire JSON file into context by default.

1. Use grep-style search first
- If the host agent provides a text-search tool such as `Grep`, `Search`, or equivalent "search within file content" capability, use that tool first.
- Prefer grep-style search to locate candidate passages, headings, node ids, table markers, or metadata fields inside parsed JSON.
- Search for user query terms, entity names, date ranges, section headers, and node `type` values before opening any large file.
- Do not introduce a custom in-skill Python search script for this retrieval path.
- Do not shell out to `grep` or `rg` if the host agent already exposes an equivalent search tool.

2. Read only local slices
- After the search tool identifies relevant hits, read only the matching lines or a narrow surrounding window.
- Extract only the needed nodes, sections, or pages for downstream summarization or embedding.

3. Escalate to full-load only when necessary
- Load the full JSON only when the task truly requires global document structure, full-tree reconstruction, or complete export.
- If full-load is required, say why.

## Onboarding

If user has no API key, guide first:

1. `cn` platform key flow
- Open `https://platform.easylink-ai.com`
- Register or sign in
- Enter API key management page and create a key
- Store as `EASYLINK_API_KEY`

2. `global` platform key flow
- Open `https://platform.easydoc.sh`
- Register or sign in
- Enter API key management page and create a key
- Store as `EASYDOC_API_KEY`

When user does not specify platform, ask whether they want `cn` or `global` first.

## Platform Selection

Choose platform before calling any endpoint:

1. `cn` platform
- Base URL: `https://api.easylink-ai.com`
- Submit: `POST /v1/easydoc/parse`
- Poll: `GET /v1/easydoc/parse/{task_id}`
- File form field: `files`
- Recommended modes: `easydoc-parse-flash`, `easydoc-parse-premium`

2. `global` platform
- Base URL: `https://api.easydoc.sh`
- Submit: `POST /api/v1/parse`
- Poll: `GET /api/v1/parse/{task_id}/result`
- File form field: `file`
- Recommended mode: `lite`

## Workflow

1. Validate request inputs
- Require `api-key` from user input or secure environment variable.
- Require parse mode when needed; if omitted in script mode, use platform default (`cn`: `easydoc-parse-premium`, `global`: `lite`).
- Validate file type and size (`<= 100MB`) using platform-specific extension list.
- If key is missing, return platform-specific onboarding steps and expected env var name.

2. Submit async parse task
- Use platform-specific submit URL and form-data file field.
- Include `mode`.
- Read `task_id` from response.

3. Poll task status
- Use platform-specific result endpoint.
- Continue polling while task is pending or processing.
- Stop on terminal status (`SUCCESS`, `ERROR`, `FAILED`, `COMPLETED`, `DONE`) or timeout.

4. Normalize output
- Keep raw response as `raw`.
- Return stable envelope for downstream consumers: `task_id`, `status`, `files`.

5. Handle failures predictably
- Include `task_id` in error reports when available.
- Report HTTP status and response body for API errors.
- For parse failures, suggest mode switch or resubmission.

6. Apply RAG-safe retrieval
- When parsed JSON is large, use the host agent's text-search tool or equivalent grep-style retrieval before any full read.
- Avoid pasting or loading entire parsed payloads into context unless the task depends on full-document traversal.

## Quick Commands

China platform:

```bash
curl -X POST "https://api.easylink-ai.com/v1/easydoc/parse" \
  -H "api-key: $EASYLINK_API_KEY" \
  -F "files=@document.pdf" \
  -F "mode=easydoc-parse-premium"
```

Global platform:

```bash
curl -X POST "https://api.easydoc.sh/api/v1/parse" \
  -H "api-key: $EASYDOC_API_KEY" \
  -F "file=@demo_document.pdf" \
  -F "mode=lite"
```

Bundled Python helper:

```bash
python3 scripts/easydoc_parse.py --platform cn --api-key "$EASYLINK_API_KEY" \
  --mode easydoc-parse-premium --file ./document.pdf --save ./result-cn.json

python3 scripts/easydoc_parse.py --platform global --api-key "$EASYDOC_API_KEY" \
  --mode lite --file ./document.pdf --save ./result-global.json

# key can come from environment if --api-key is omitted
export EASYLINK_API_KEY="your-cn-key"
python3 scripts/easydoc_parse.py --platform cn --file ./document.pdf --save ./result-cn.json

export EASYDOC_API_KEY="your-global-key"
python3 scripts/easydoc_parse.py --platform global --file ./document.pdf --save ./result-global.json
```

## References And Scripts

- Read `references/easydoc-rest-api.md` for endpoint-level differences between cn and global.
- Use `scripts/easydoc_parse.py` for deterministic submit and polling.
- Script default output is `normalized`; use `--output-format raw` for raw payload only.
- In RAG workflows, prefer the host agent's built-in content search tool on saved JSON results before opening large file sections.

## Output Contract

```json
{
  "task_id": "string",
  "status": "SUCCESS|ERROR|PENDING|PROCESSING|FAILED|COMPLETED|DONE",
  "files": [
    {
      "file_name": "string",
      "markdown": "string or null",
      "nodes": []
    }
  ],
  "raw": {}
}
```
