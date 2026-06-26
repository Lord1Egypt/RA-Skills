# Output Patterns

## Overview-first response

```json
{
  "library_id": "lib_xxx",
  "overview": {
    "assets_total": 29,
    "needs_review_assets": 4
  },
  "next_action": "list_review_queue"
}
```

## Patch response

```json
{
  "library_id": "lib_xxx",
  "asset_id": "asset_xxx",
  "action": "patch",
  "changed_fields": ["normalized_summary", "review_status"]
}
```

## Archive response

```json
{
  "library_id": "lib_xxx",
  "asset_id": "asset_xxx",
  "action": "archive"
}
```

## Restore response

```json
{
  "library_id": "lib_xxx",
  "asset_id": "asset_xxx",
  "action": "restore"
}
```
