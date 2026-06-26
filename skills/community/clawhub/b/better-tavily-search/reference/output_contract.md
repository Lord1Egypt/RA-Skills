# Output Contract

This reference defines the implemented output shapes.

## Design Goals

The output should be:
- stable for downstream agents
- compact enough for repeated use
- rich enough to preserve retrieval signals
- easy to inspect in raw JSON or Markdown

## Formats

### `agent` for `search` (preferred default)
Machine-facing shape for agent workflows.

Actual structure:

```json
{
  "endpoint": "search",
  "query_original": "...",
  "query_executed": "...",
  "profile": "general",
  "params": {
    "query": "...",
    "topic": "general",
    "search_depth": "basic",
    "max_results": 5,
    "include_usage": true,
    "include_favicon": false,
    "include_answer": false,
    "include_raw_content": false
  },
  "answer": null,
  "results": [
    {
      "title": "...",
      "url": "...",
      "domain": "docs.openclaw.ai",
      "snippet": "...",
      "score": 0.92,
      "favicon": null,
      "published_date": null
    }
  ],
  "images": [],
  "usage": null,
  "response_time": null,
  "request_id": null,
  "auto_parameters": null
}
```

Notes:
- `answer` is optional and should not dominate the output.
- `domain` is normalized from the URL.
- `snippet` is truncated for stability.
- `score`, `usage`, `response_time`, `request_id`, and `published_date` are preserved when available.
- `auto_parameters` appears only when Tavily returns it.

### `raw`
A close representation of Tavily's own response, with minimal reshaping.
Useful for debugging or feature-complete inspection.

### `md`
Human-readable output for inspection.
Recommended shape:
- query and profile header
- numbered sources
- title
- URL
- short snippet
- optional answer block at the end

### `brave` for `search`
Compatibility output for workflows that already expect a Brave-like schema.

Actual structure:

```json
{
  "query": "...",
  "results": [
    {
      "title": "...",
      "url": "...",
      "snippet": "..."
    }
  ],
  "answer": null
}
```

Notes:
- `answer` is omitted when Tavily did not return one.
- This format intentionally drops scores, usage, and request metadata.

## Extraction Output

Preferred `agent` extraction shape:

```json
{
  "endpoint": "extract",
  "query": "...",
  "urls": ["..."],
  "params": {
    "urls": ["..."],
    "extract_depth": "basic",
    "format": "markdown",
    "include_images": false,
    "include_favicon": false,
    "allow_external": false,
    "include_usage": true
  },
  "results": [
    {
      "url": "...",
      "title": "...",
      "content": "...",
      "chunks": ["..."],
      "favicon": null,
      "images": []
    }
  ],
  "failed_results": [],
  "usage": null,
  "response_time": null,
  "request_id": null
}
```

Notes:
- `chunks` are derived by splitting the returned content on Tavily chunk separators when possible.
- `content` is the raw extracted payload preserved for downstream use.

## Map Output

Preferred `agent` map shape:

```json
{
  "endpoint": "map",
  "url": "https://docs.openclaw.ai",
  "params": {
    "url": "https://docs.openclaw.ai",
    "max_depth": 1,
    "max_breadth": 20,
    "limit": 50,
    "allow_external": false,
    "include_usage": true
  },
  "base_url": "https://docs.openclaw.ai",
  "results": [
    "https://docs.openclaw.ai/tools/skills"
  ],
  "usage": null,
  "response_time": null,
  "request_id": null
}
```

## Output Rules

- Keep the default machine-facing format stable across versions.
- Do not silently drop retrieval signals that help planning.
- Do not over-serialize giant fields into the default output.
- When content is long, prefer chunk lists or truncated previews plus an explicit raw mode.
