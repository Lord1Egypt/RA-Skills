# OpenClaw Routing Cheatsheet

Generated from the current local snapshot. Use this file when the user question is broad and you need a fast first route before full-text search.

## Snapshot

- Generated at: `2026-03-08T18:49:41.684417+00:00`
- Markdown files indexed: `664`

## Top-Level Routes

- `.i18n/` (1 files)
- `_root/` (13 files)
- `automation/` (8 files)
- `channels/` (29 files)
- `cli/` (46 files)
- `concepts/` (27 files)
- `debug/` (1 files)
- `design/` (1 files)
- `diagnostics/` (1 files)
- `experiments/` (12 files)
- `gateway/` (33 files)
- `help/` (7 files)
- `install/` (20 files)
- `ja-JP/` (3 files)
- `nodes/` (9 files)
- `platforms/` (27 files)
- `plugins/` (5 files)
- `providers/` (29 files)
- `refactor/` (5 files)
- `reference/` (26 files)
- `security/` (4 files)
- `start/` (14 files)
- `tools/` (28 files)
- `web/` (5 files)
- `zh-CN/` (310 files)

## Query Patterns

Filename-first:

```bash
rg --files openclaw_docs | rg 'gateway|install|telegram|security|models'
```

Content search after narrowing paths:

```bash
rg -n "auth|pairing|approval|health|provider" openclaw_docs/gateway openclaw_docs/cli openclaw_docs/channels
```

## Guardrails

- Prefer stable docs over experiments unless the user asks for proposals.
- Read the full relevant file before answering defaults, behavior, or constraints.
- If direct documentation is missing, say what you searched and that the gap is in the local snapshot.
