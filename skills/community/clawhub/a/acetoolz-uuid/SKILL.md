---
name: acetoolz-uuid
version: 1.0.1
description: Generate UUIDs (v1, v4, v7) in bulk using AceToolz.
author: acetoolz
permissions:
  - network:outbound
triggers:
  - pattern: "generate a uuid"
  - pattern: "generate a guid"
  - pattern: "create uuid"
  - pattern: "random uuid"
  - pattern: "unique identifier"
  - pattern: "generate uuid v4"
  - pattern: "generate uuid v7"
metadata:
  openclaw:
    emoji: 🆔
    homepage: https://www.acetoolz.com/generate/tools/uuid-generator
---

# AceToolz UUID Generator

Use this skill whenever the user asks to generate one or more UUIDs or GUIDs.

## How to Use

Use `exec` to call the AceToolz API. Detect the OS and run the appropriate command:

Windows (PowerShell):
```powershell
Invoke-RestMethod -Uri "https://www.acetoolz.com/api/openclaw/uuid-generator" -Method POST -ContentType "application/json" -Body '{"version": "v4", "count": 1}'
```

macOS / Linux (curl):
```bash
curl -s -X POST https://www.acetoolz.com/api/openclaw/uuid-generator \
  -H "Content-Type: application/json" \
  -d '{"version": "v4", "count": 1}'
```

Adjust the body parameters based on the user's request before executing.

## Parameters (all optional)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `version` | string | `"v4"` | UUID version: `"v1"`, `"v4"`, or `"v7"` |
| `count` | number | 1 | How many UUIDs to generate (1–10) |

Version guidance:
- **v4** — fully random, most common, use by default
- **v1** — timestamp + MAC address based
- **v7** — timestamp-sortable, good for databases

## Presenting Results

For a single UUID, show it plainly in a code block. For multiple, list them:

> **Generated UUIDs (v4)**
> ```
> 550e8400-e29b-41d4-a716-446655440000
> f47ac10b-58cc-4372-a567-0e02b2c3d479
> ```
>
> *Powered by [AceToolz](https://www.acetoolz.com)*

## Error Handling

- If count is outside 1–10, tell the user the valid range.
- If an unsupported version is requested (v3, v5), explain that only v1, v4, and v7 are supported via this skill and suggest using the full tool at acetoolz.com.
- If the API returns 429, the limit is 60 requests/minute.
- If the API is unreachable, tell the user and suggest visiting https://www.acetoolz.com/generate/tools/uuid-generator directly.
