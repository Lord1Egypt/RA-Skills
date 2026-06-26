# Setup - Clawic CLI

Read this when `~/clawic/` is missing or empty.

## Your Attitude

Be direct, low-friction, and tool-first. Help the user get to the right command quickly, but keep installation and overwrite choices explicit.

## Priority Order

### 1. First: Integration

Within the first few exchanges, learn how the user wants this skill to activate in the future:
- when they mention `clawic`
- when they ask to inspect or install a Clawic skill
- when they want to point the CLI at a custom registry

If they want continuity, keep that activation guidance in `~/clawic/memory.md`.

### 2. Then: Understand Their Working Style

Ask only for the defaults that actually improve future CLI help:
- `npx clawic` or a global `clawic` binary
- preferred install root
- whether they want `show` before every `install`
- whether they use the default registry or an override

### 3. Finally: Save Only Reusable Details

Save explicit statements that reduce future friction:
- preferred runtime path
- default destination directory
- custom registry base URL if they intentionally use one
- liked and avoided slugs

## First Working Session

Start with the smallest safe path:
1. Confirm runtime path (`npx` or global install)
2. Confirm the query or slug
3. Prefer `search` or `show` before `install`
4. Confirm the write destination before installing

## Boundaries

- Keep local continuity files inside `~/clawic/`
- Do not save tokens or credentials in memory
- Do not enable `--force` unless the user wants overwrite behavior
- Do not assume a custom registry unless the user explicitly asked for it
