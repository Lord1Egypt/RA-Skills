# Renesas System Solutions (Placeholder)

> **Status:** Phase 3 placeholder. No content yet.
> **Scope:** Renesas-published reference designs, evaluation kits, SDK
> examples, and application notes — all sourced from `renesas.com`. The
> BOM in each file contains **only Renesas parts** (this directory is the
> single-vendor counterpart to the multi-vendor `application-solution/`).
> Generic application topics like "smart ring" or "robot gripper" live in
> `references/application-solution/` instead, because those are typically
> sourced from third-party teardowns and may mix vendors.

This directory will hold Renesas-provided reference designs and application
notes from the Renesas website, organised by topic or solution name.

## Planned Topics

| Solution | Type | Hero part(s) | Source |
|----------|------|--------------|--------|
| DA14531 BLE Beacon reference | Reference design | DA14531 | renesas.com (verification pending) |
| RA6M5 EK-RA6M5 quick start | Eval kit guide | RA6M5 | renesas.com (verification pending) |
| RX72N motor-control kit | Reference design | RX72N | renesas.com (verification pending) |
| ISL9238 NVDC charger reference | Reference design | ISL9238 | renesas.com (verification pending) |

## Adding a New Solution

For each Renesas-published solution, create a Markdown file named
`<topic>.md` with:

```markdown
# <Solution Name>

## Overview
- What the solution demonstrates
- Where it was published (renesas.com URL)
- When it was published / revision

## Reference Design
- [Design name](vendor-url) — short description

## BOM Candidates (Renesas only)
| Function | Part | Notes |
|----------|------|-------|
| BLE SoC | DA14xxx | ... |
| Sensor | HS3001 | ... |
| Power | ISL9205 | ... |

## Verification Status
- [ ] Original design URL still reachable (HTTP 200)
- [ ] All BOM specs verified against datasheet
- [ ] Date of original publication noted
```

## Source Discipline

- **Single-vendor BOM only**: every part listed must be a Renesas part
  (use `product_families.md` as the source of truth).
- **Original source must be cited**: the reference design URL must point
  back to renesas.com, not to a third party.
- Numerical specs **must** be cited to datasheet pages, not to marketing
  copy.
- Mark any unverified parameter as `not verified` explicitly.
- If a real-world teardown uses this same part set, document it in
  `references/application-solution/<topic>/` instead (multi-vendor
  scope).
