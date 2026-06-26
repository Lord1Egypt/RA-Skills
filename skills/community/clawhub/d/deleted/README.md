# bee-languages-get

> Version: 2.0.4

## Overview

A language list retrieval skill based on the "Bee Website Builder" Open API. It is used to obtain the list of enabled site languages and provide the dependency data source for the `language` parameter used by other skills.

Supports AI Agent integration, OpenClaw Skill integration, and automatic Select UI generation.

---

## Features

- Retrieve the list of languages supported by the Bee platform
- Return the available values for the `language` parameter
- Serve as a dependency data source for other skills
- Support automatic AI-generated Select UI
- Support chained Workflow calls

---

## Request Parameters

### Required

| Parameter | Type   | Description                |
|-----------|--------|----------------------------|
| api_key   | string | API authentication key     |

---

## Response

### Base Structure

| Field  | Type    | Description                    |
|--------|---------|--------------------------------|
| status | boolean | `true` for success / `false` for failure |
| msg    | string  | Response message               |
| data   | object  | Response data                  |

---

### `data` Structure

| Field | Type  | Description   |
|-------|-------|---------------|
| list  | array | Language list |

---

### `list` Field Description

| Field    | Type   | Description                              |
|----------|--------|------------------------------------------|
| language | string | Site language code identifier (for API use) |
| name     | string | Language name (for display)              |

---

## Dependency Example

```json
{
  "dependencies": {
    "language": {
      "skill": "bee-languages-get",
      "field": "list[].language",
      "mode": "select"
    }
  }
}
```
