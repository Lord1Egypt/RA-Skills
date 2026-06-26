# Output Schema

The bundled parser emits JSON with this top-level shape:

```json
{
  "source": {},
  "summary": {},
  "schema": {},
  "alerts": [],
  "preview_rows": []
}
```

## `source`

- `path`: absolute input path
- `format`: `csv` or `json`
- `parser`: parser identifier
- `limits.max_preview_rows`: preview row/item cap
- `limits.max_string_length`: per-string preview cap

## `summary`

CSV:

- `row_count`
- `column_count`
- `preview_rows_truncated`

JSON:

- `top_level_type`
- `top_level_key_count` or `top_level_item_count`
- `preview_rows_truncated`

## `schema`

CSV emits table-oriented schema:

```json
{
  "kind": "table",
  "fields": [
    {
      "name": "notes",
      "type_counts": { "string": 10 },
      "raw_text_present": true,
      "instruction_like_text_possible": true,
      "suspicious_value_count": 2
    }
  ]
}
```

JSON emits a recursive type tree:

```json
{
  "path": "$",
  "type": "object",
  "properties": [
    {
      "path": "$.message",
      "type": "string",
      "instruction_like_text_possible": false
    }
  ]
}
```

## `alerts`

Each alert marks instruction-like text that remained in the data:

```json
{
  "kind": "instruction_like_text",
  "location": { "row_index": 3, "field": "notes" },
  "matched_rules": ["ignore\\s+(all\\s+)?(previous|prior)\\s+instructions?"]
}
```

or:

```json
{
  "kind": "instruction_like_text",
  "location": { "json_path": "$.payload.comment" },
  "matched_rules": ["(system|developer)\\s+prompt"]
}
```

## `preview_rows`

Bounded structured preview used for model-side reasoning.

CSV preview rows are field-by-field objects with per-cell metadata:

```json
{
  "row_index": 1,
  "fields": {
    "notes": {
      "value": "ignore previous instructions",
      "metadata": {
        "raw_text_present": true,
        "instruction_like_text_possible": true,
        "truncated": false
      }
    }
  }
}
```

JSON preview rows summarize top-level items or keys without dumping the whole raw file.
