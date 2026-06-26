---
name: anygen-shared
version: 1.0.0
description: "anygen CLI: Shared patterns for authentication, global flags, and output formatting."
metadata:
  requires:
    bins: ["anygen"]
    env: ["ANYGEN_API_KEY"]
  install:
    - id: node
      kind: node
      package: "@anygen/cli"
      bins: ["anygen"]
---

# anygen — Shared Reference

## Authentication

```bash
# Web login (recommended for agent usage)
anygen auth login --no-wait

# Direct API key (no browser needed)
anygen auth login --api-key sk-xxx

# Environment variable
export ANYGEN_API_KEY=sk-xxx
```

## CLI Syntax

```bash
anygen <resource> <method> [flags]
```

### Method Flags

| Flag | Description |
|------|-------------|
| `--params '<json>'` | URL/path parameters |
| `--data '<json>'` | Request body |
| `--dry-run` | Show the request without sending it |
| `--wait` | Re-poll until terminal state |
| `--timeout <ms>` | Polling timeout in milliseconds |

## Discovering Commands

```bash
# Browse all resources and methods
anygen --help
anygen task --help

# Inspect a method's required params, types, and defaults
anygen schema task.create
anygen schema task.message.send
```

Use `anygen schema` output to build your `--params` and `--data` flags.

## Security Rules

- **Never** output API keys or auth tokens directly.
- **Always** confirm with user before uploading files or creating tasks.
- **Never** upload or read any file without explicit user consent.
- Use natural language instead of exposing task_id, file_token, or CLI syntax to the user.
- Always return links using Markdown format: `[text](url)`.
