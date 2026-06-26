---
name: bee-languages-get
description: A language list retrieval skill based on the "Bee Website Builder" Open API. It is used to obtain the list of enabled site languages and provide the dependency data source for the `language` parameter used by other skills.
homepage: https://open.tradew.com
metadata:
  {
    "openclaw":
      {
        "emoji": "🐝",
        "requires": { "env": ["BEE_API_KEY"] },
        "primaryEnv": "BEE_API_KEY"
      }
  }
---

# bee-languages-get

> Version: 2.0.4

## Overview

Use the "Bee Website Builder" Open API to retrieve the list of currently enabled languages for the site. This skill can be used to:

- Retrieve platform-supported languages
- Provide selectable values for the `language` parameter
- Support AI Agent dropdown linkage
- Support OpenClaw Skill dependency injection
- Support chained Workflow calls

---

## Input Parameters

### `api_key` (string, **Required**)

API authentication key used for caller identity verification and interface access control.

- **Get it from:** https://open.tradew.com
- **Recommended configuration:** Inject it via `skills.entries.env.BEE_API_KEY` to avoid passing it in plaintext on every call.

---

## Output Structure

### Top-Level Fields

| Field  | Type           | Description                            |
|--------|----------------|----------------------------------------|
| status | boolean        | Request status, `true` for success / `false` for failure |
| msg    | string         | Response message                       |
| data   | object \| null | Response data, `null` on failure       |

### `data.list[]` (array of objects)

Each language record contains the following fields:

| Field    | Type   | Description                              |
|----------|--------|------------------------------------------|
| language | string | Site language code identifier (for API use) |
| name     | string | Language name (for display)              |

## Usage Example

### Query

```json
{
  "api_key": "your-api-key"
}
```

---

## Notes

1. `api_key` is required and can be obtained from https://open.tradew.com

---

## Applicable Scenarios

- Retrieve currently enabled language sites
- Language filtering
