---
name: codemap
description: Build a compact local SQLite index of every function, class, method, interface and type across your repos, so an agent finds a symbol's file:line and signature in one lookup instead of a tree-wide grep plus whole-file read.
version: 0.1.0
homepage: https://workloft.ai/labs
metadata:
  openclaw:
    emoji: "🗺️"
    requires:
      bins:
        - python3
---

# codemap

Agents burn tokens re-discovering the same code: grep a name across the trees,
then read the file the hit lives in (often the whole thing) to see the signature.
`codemap` collapses that to one short record — `file:line` plus the signature.
Pure Python standard library: no network, no model call, no dependencies.

The executable is `{baseDir}/bin/codemap`. Build the index once over your roots,
then query it instead of grepping.

## When to use this

Use it whenever you are about to grep a codebase for where a function/class/type
is defined, or need a symbol's signature. Build the index at the start of a
session over the repos you will touch, then `find` instead of grepping. Best on
Python and JS/TS/JSX/TSX projects.

## How to use it

### 1. Build (or rebuild) the index over one or more roots

```
{baseDir}/bin/codemap build <root1> <root2> ...
```

Idempotent — `build` deletes and re-inserts. Skips `node_modules`, `.next`,
`.git`, `dist`. Rebuild after large edits (there is no file-watcher).

### 2. Find a symbol

```
{baseDir}/bin/codemap find scan            # exact match by default
{baseDir}/bin/codemap find scan --like     # substring match
{baseDir}/bin/codemap find Pipeline --kind class
{baseDir}/bin/codemap find scan --json     # machine-readable
```

`find` exits non-zero when nothing matches, so it drops into a `&&` chain.

### 3. Outline a file / see stats

```
{baseDir}/bin/codemap file src/app/page.tsx
{baseDir}/bin/codemap stats
```

## What it indexes

- **Python:** top-level functions, classes, methods (incl. `async def`).
- **JS / TS / JSX / TSX:** function declarations, exported arrow consts, classes,
  interfaces, `type` aliases.

## Notes for the agent

- Reference the tool as `{baseDir}/bin/codemap` — never hardcode a path.
- Extraction is regex-based, not a full parser: it catches common declaration
  forms but misses exotic ones (decorated factories, re-exports, dynamically
  assigned names). It answers "where is X defined", not "who calls X".
- The index is a snapshot — rebuild after large edits.
- Built by Workloft (https://workloft.ai/labs).
