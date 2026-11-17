# Nordic System Solutions (Placeholder)

> **Status:** Phase 3 placeholder. No content yet.
> **Scope:** Nordic-published reference designs, development kits, SDK
> examples, and application notes — all sourced from `nordicsemi.com`. The
> BOM in each file contains **only Nordic parts** (this directory is the
> single-vendor counterpart to the multi-vendor `application-solution/`).
> Generic application topics like "smart ring" or "smart glasses" live in
> `references/application-solution/` instead, because those are typically
> sourced from third-party teardowns and may mix vendors.

This directory will hold Nordic-provided reference designs, nRF Connect SDK
examples, and DevKit application notes, organised by topic or solution name.

## Planned Topics

| Solution | Type | Hero part(s) | Source |
|----------|------|--------------|--------|
| nRF52832 DK BLE peripheral example | SDK example | nRF52832 | nordicsemi.com (verification pending) |
| nRF5340 audio DK application note | Eval kit + app note | nRF5340 | nordicsemi.com (verification pending) |
| nRF9160 asset tracker reference | Reference design | nRF9160 | nordicsemi.com (verification pending) |
| nRF54L15 power-profile sample | SDK example | nRF54L15 | nordicsemi.com (verification pending) |

## Adding a New Solution

For each Nordic-published solution, create a Markdown file named
`<topic>.md` with:

```markdown
# <Solution Name>

## Overview
- What the solution demonstrates
- Where it was published (nordicsemi.com URL)

## Reference Design
- [Design name](vendor-url) — short description

## BOM Candidates (Nordic only)
| Function | Part | Notes |
|----------|------|-------|
| BLE SoC | nRF52xxx | ... |
| Cellular SiP | nRF9160 | ... |

## Verification Status
- [ ] Original design URL still reachable (HTTP 200)
- [ ] All BOM specs verified against datasheet
```

## Source Discipline

- **Single-vendor BOM only**: every part listed must be a Nordic part
  (use `product_families.md` as the source of truth).
- **Original source must be cited**: the reference design URL must point
  back to nordicsemi.com, not to a third party.
- Numerical specs **must** be cited to datasheet pages.
- Mark any unverified parameter as `not verified` explicitly.
