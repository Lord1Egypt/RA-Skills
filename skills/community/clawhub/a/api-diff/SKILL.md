---
name: api-diff
description: Compare two OpenAPI 3.x or Swagger 2.0 specs and generate a changelog of breaking and non-breaking changes. Detect removed endpoints, new required parameters, type changes, schema modifications, enum changes, security changes, server URL changes, and deprecations. Use when asked to diff APIs, compare API versions, detect breaking changes, generate API changelogs, or review API spec changes. Triggers on "API diff", "API changelog", "breaking changes", "OpenAPI compare", "spec diff", "API version compare".
---

# API Diff — Changelog Generator

Compare two OpenAPI/Swagger specs and generate a detailed changelog with breaking change detection.

## Quick Diff

```bash
python3 scripts/api_diff.py old-spec.json new-spec.json
```

## Output Formats

```bash
# Text (default)
python3 scripts/api_diff.py old.json new.json

# JSON
python3 scripts/api_diff.py old.json new.json --format json

# Markdown
python3 scripts/api_diff.py old.json new.json --format markdown
```

## CI/CD Integration

```bash
# Fail if breaking changes found
python3 scripts/api_diff.py old.json new.json --fail-on-breaking
echo $?  # 0 = no breaking, 1 = breaking found

# Show only breaking changes
python3 scripts/api_diff.py old.json new.json --breaking-only
```

## What It Detects

### Endpoint Changes
| Change | Breaking? | Description |
|--------|-----------|-------------|
| Endpoint removed | Yes | Path+method no longer exists |
| Endpoint added | No | New path+method |
| Endpoint deprecated | No | Marked as deprecated |

### Parameter Changes
| Change | Breaking? | Description |
|--------|-----------|-------------|
| Required param added | Yes | New mandatory parameter |
| Optional param added | No | New optional parameter |
| Param removed (required) | Yes | Required parameter removed |
| Param type changed | Yes | Data type changed |
| Param became required | Yes | Optional → required |
| Param became optional | No | Required → optional |

### Schema Changes
| Change | Breaking? | Description |
|--------|-----------|-------------|
| Schema removed | Yes | Definition removed |
| Required property added | Yes | New mandatory field |
| Optional property added | No | New optional field |
| Property removed | Yes | Field removed |
| Property type changed | Yes | Data type changed |
| Enum value removed | Yes | Allowed value removed |
| Enum value added | No | New allowed value |

### Other Changes
| Change | Breaking? | Description |
|--------|-----------|-------------|
| Response code removed | Yes | HTTP status no longer returned |
| Response code added | No | New HTTP status |
| Security changed | Yes | Auth requirements changed |
| Server URLs changed | No | Base URL changed |
| API version changed | No | Info version updated |

## Requirements

- Python 3.6+
- No external dependencies (stdlib only)
- Input: JSON format OpenAPI 3.x or Swagger 2.0 specs
