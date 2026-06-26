---
name: adapter-audit
description: Use this skill to audit CLI adapter projects (like opencli) for missing output fields, then batch-generate fixes and submit PRs. Turns AI agents into adapter quality reviewers.
license: Proprietary session artifact for local Copilot use
---

# Adapter audit skill

Use this skill when you want to **systematically audit and fix CLI adapter projects** — for example, scanning all search adapters in opencli for missing `url` fields and batch-generating patches.

## When to use

- auditing adapter output schemas for missing fields (url, timestamp, thumbnail, etc.)
- generating batch fixes across many adapters at once
- preparing multi-file PRs to upstream projects
- maintaining output consistency across a large adapter registry

## Core workflow

### 1. Scan

Scan all adapters in the target project and classify each by:

- adapter type (YAML declarative vs TS/JS coded)
- which output fields are present
- which standard fields are missing

Standard fields to check:

- `url` — direct link to the content item
- `title` — content title
- `author` — creator/author name
- `timestamp` / `date` — publish or capture time

### 2. Classify fix type

For each missing field, determine the fix strategy:

| Situation | Fix strategy |
|-----------|-------------|
| Field is computed internally but not in `columns` | Add to `columns` list |
| Field is computed but stripped by a `map` step | Pass through the `map` step + add to `columns` |
| Field is not computed but can be constructed from existing data | Add construction logic + add to `columns` |
| Field requires external data not available in the API response | Skip or mark as "needs upstream API change" |

### 3. Fix

Apply fixes using the minimum change principle:

- For YAML adapters: add field to return object + map step + columns array
- For TS adapters: add field to return object + columns array
- Never change existing fields or behavior
- Only add new fields

### 4. Verify

After fixing, run the project's existing tests:

```bash
npm run build    # ensure TS compiles
npm test         # ensure nothing breaks
```

### 5. Submit

Create a single well-documented PR with:

- clear title describing the scope
- table showing before/after coverage
- per-adapter fix type classification
- risk assessment (should always be "additive only")

## Proven example

This skill was used to audit opencli's 33 search adapters:

- **Before**: 22/33 (67%) had `url` in output
- **After**: 32/33 (97%) had `url` in output
- **Fix types used**: columns-only (3), map-passthrough (2), construct-from-data (4)
- **Files changed**: 9
- **Lines changed**: +17 / -10
- **PR**: merged within hours, all CI green

## Output contract

The audit output should include:

1. total adapters scanned
2. per-adapter field coverage table
3. fix strategy for each missing field
4. list of files changed
5. before/after coverage metrics
6. risk classification

## Key rules

- Never modify existing output fields — only add missing ones
- Prefer constructing URLs from existing API data over adding new API calls
- Skip fields that genuinely don't apply (e.g., `url` for dictionary word lookup)
- Always verify the constructed URL format is correct for the platform
- Group all fixes into a single PR for easier review

## Quick invocation template

```text
Use /adapter-audit to scan all search adapters in this CLI project for missing url fields, fix them, and prepare a PR.
```

```text
请用 /adapter-audit 扫描这个 CLI 项目里所有 search adapter 的缺失字段，批量修复并准备 PR。
```
