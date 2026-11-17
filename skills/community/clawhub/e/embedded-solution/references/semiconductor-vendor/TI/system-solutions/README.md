# TI System Solutions (Placeholder)

> **Status:** Phase 3 placeholder. No content yet.
> **Scope:** TI-published reference designs, LaunchPad / SensorTag
> examples, SimpleLink SDK content, and application notes — all sourced
> from `ti.com`. The BOM in each file contains **only TI parts** (this
> directory is the single-vendor counterpart to the multi-vendor
> `application-solution/`). Generic application topics like "smart ring" or
> "BLE beacon" live in `references/application-solution/` instead.

This directory will hold TI-provided reference designs, LaunchPad / SensorTag
examples, and SimpleLink SDK content.

## Planned Topics

| Solution | Type | Hero part(s) | Source |
|----------|------|--------------|--------|
| CC2640R2F BLE peripheral example | SDK example | CC2640R2F | ti.com (verification pending) |
| CC2652R Matter reference design | Reference design | CC2652R | ti.com (verification pending) |
| CC1310 sub-GHz sensor node | Reference design | CC1310 | ti.com (verification pending) |
| CC2340R5 cost-optimised BLE | SDK example | CC2340R5 | ti.com (verification pending) |
| MSPM0G3507 LaunchPad demo | Eval kit guide | MSPM0G3507 | ti.com (verification pending) |

## Adding a New Solution

For each TI-published solution, create a Markdown file named `<topic>.md` with:

```markdown
# <Solution Name>

## Overview
- What the solution demonstrates
- Where it was published (ti.com URL)

## Reference Design
- [Design name](vendor-url) — short description

## BOM Candidates (TI only)
| Function | Part | Notes |
|----------|------|-------|
| Wireless MCU | CCxxxx | ... |
| General MCU | MSPM0G | ... |

## Verification Status
- [ ] Original design URL still reachable (HTTP 200)
- [ ] All BOM specs verified against datasheet
```

## Source Discipline

- **Single-vendor BOM only**: every part listed must be a TI part
  (use `product_families.md` as the source of truth).
- **Original source must be cited**: the reference design URL must point
  back to ti.com, not to a third party.
- Numerical specs **must** be cited to datasheet pages.
- Mark any unverified parameter as `not verified` explicitly.
