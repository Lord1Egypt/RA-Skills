---
name: jpeng-ab-test
description: "Manage A/B tests"
version: "1.0.0"
author: "jpeng"
tags: ["testing", "ab", "marketing"]
---

# A/B Test Manager

Manage A/B tests

## When to Use

- User needs testing related functionality
- Automating ab tasks
- Marketing operations

## Usage

```bash
python3 scripts/ab_test.py --input <input> --output <output>
```

## Configuration

Set required environment variables:

```bash
export AB_API_KEY="your-api-key"
```

## Output

Returns JSON with results:

```json
{
  "success": true,
  "data": {}
}
```
