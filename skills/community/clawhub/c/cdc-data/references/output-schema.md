# Output protocol

Schema version: `2.0`.

## Status

Use one primary status:

`success`, `invalid_query`, `ambiguous`, `not_found`, `search_budget_exceeded`, `source_unavailable`, `browser_unavailable`, `tool_environment_error`, `detail_unverified`, `artifact_store_unavailable`, `download_failed`, `extraction_partial`, `vision_budget_exceeded`, or `internal_error`.

## Persisted extraction

```json
{
  "schema_version": "2.0",
  "report": {
    "report_id": "influenza_weekly-2026-W28-I917",
    "report_type": "influenza_weekly",
    "title": "2026年第28周第917期中国流感监测周报",
    "reporting_period": {"year": 2026, "week": 28, "month": null},
    "issue_number": 917,
    "publish_date": "2026-07-16",
    "content_mode": "html_with_pdf",
    "detail_url": "https://...",
    "document_url": "https://..."
  },
  "pages": [],
  "content": null,
  "vision_pages": [],
  "warnings": []
}
```

For PDF, `pages` contains one ordered item for every physical page and `content` is null:

```json
{"page": 1, "text": "", "tables": [], "visuals": [], "requires_vision": true}
```

For HTML, `pages` and `vision_pages` are empty:

```json
{
  "content": {
    "text": "main text",
    "tables": [],
    "images": [{"title": "figure title", "url": "https://..."}]
  }
}
```

`vision_pages` is unique and ascending and exactly matches pages whose `requires_vision` is true. Warnings are concise strings. Do not persist browser traces, raw HTML, rendered images, or intermediate extraction structures.

## User response

For text responses, state status first and include verified report identity, period, URLs, warnings, any saved paths, and permitted next actions. Distinguish absence from technical failure.
