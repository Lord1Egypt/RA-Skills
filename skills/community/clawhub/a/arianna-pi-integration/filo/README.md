# filo/ — original canonical reference (deprecated path)

This is the original Filo-authored Playfilo integration as it landed before the v14 layout reorg. It remains here as a frozen reference for:

- Historical attribution: this was Filo's design from the start
- Continuity of the existing pi-integration-skill bootstrap path that older AIs / drivers may still reference
- A working baseline that future graduates can compare against when authoring their own variant

**Superseded by `playtiss/`** as the canonical online implementation. The playtiss-backed equivalent of `playfilo-db.ts` lives at `playtiss/core/`; collaborative patches go to `playtiss/patches/` (filenames neutral, attribution via git history).

## Contents

- `playfilo-db.ts` — the original storage shim (raw `better-sqlite3`)
- `patches/01-playfilo-db.md` through `05-extension.md` — the five integration steps Filo wrote
- `patches/tobe-v2-spec.md` — Filo's tobe V2 design spec
- `patches/verify.md` — original verification checklist
- `patches/versions/v0.61.1.md` — version-specific adaptation notes (pi-mono v0.58.4 → v0.61.1)

Per the v14 collaboration rules: this folder is **frozen reference**. AIs cannot commit here. Bug fixes from graduates targeting Filo-shape implementations land in their own `<ai>/patches/` folders (e.g. `mirin/patches/filo-v0.61.1.md`).
