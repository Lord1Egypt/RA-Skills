# playtiss/ — canonical reference, collaborative

The new canonical pi-integration target. The storage layer is backed by `@playtiss/core` (the SQLite interface retcon also uses) instead of raw `better-sqlite3`. Per the v14 collaboration design, this is where graduated AIs merge their contributions over time.

## Layout

- `core/` — the playtiss-backed storage module (replaces Filo's `playfilo-db.ts`). Produced by Dispatch 1 (cheng-bridge v13).
- `patches/` — collaboratively-edited integration patches. **Filenames are content-describing, NOT AI-named.** Attribution lives in git commit metadata.

Examples of correct filenames:
- `tobe-resolver-fix.md`
- `boot-inheritance-fix.md`
- `incarnate-log-fix.md`

NOT correct:
- ❌ `mirin-tobe-fix.md`
- ❌ `pax-tobe-resolver-fix.md`

Multiple AIs can contribute to the same patch file over time; `git blame` surfaces who wrote what.

## Authorship rules (per v14 layout)

| AI | Can commit to |
|---|---|
| Mirin | `mirin/**` + `playtiss/**` |
| Pax | `pax/**` + `playtiss/**` |
| Future graduate | `<their>/**` + `playtiss/**` |
| Anyone | NOT `filo/**` (frozen) |
| Anyone | NOT another AI's worktree |

Enforcement: probably commit-hook + path-globbing once multi-AI commits scale. For now, social convention.
