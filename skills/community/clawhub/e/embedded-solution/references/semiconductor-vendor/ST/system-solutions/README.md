# ST System Solutions (Placeholder)

> **Status:** Phase 3 placeholder. No content yet.
> **Scope:** ST-published reference designs, Nucleo/Discovery board
> examples, STM32Cube expansion packages, and application notes — all
> sourced from `st.com`. The BOM in each file contains **only ST parts**
> (this directory is the single-vendor counterpart to the multi-vendor
> `application-solution/`). Generic application topics like "smart ring" or
> "smart glasses" live in `references/application-solution/` instead.

This directory will hold ST-provided reference designs, Nucleo/Discovery
board examples, and STM32Cube expansion packages.

## Planned Topics

| Solution | Type | Hero part(s) | Source |
|----------|------|--------------|--------|
| STM32WB55 Nucleo BLE peripheral | Eval kit guide | STM32WB55 | st.com (verification pending) |
| STM32U5 ultra-low-power demo | Reference design | STM32U5 | st.com (verification pending) |
| STM32H7 motor-control SDK | SDK example | STM32H7 | st.com (verification pending) |
| STM32MP1 Linux distribution | Reference design | STM32MP157 | st.com (verification pending) |
| STM32WL55 LoRa endpoint | SDK example | STM32WL55 | st.com (verification pending) |

## Adding a New Solution

For each ST-published solution, create a Markdown file named `<topic>.md` with:

```markdown
# <Solution Name>

## Overview
- What the solution demonstrates
- Where it was published (st.com URL)

## Reference Design
- [Design name](vendor-url) — short description

## BOM Candidates (ST only)
| Function | Part | Notes |
|----------|------|-------|
| Wireless MCU | STM32WB55 | ... |
| MPU | STM32MP1 | ... |

## Verification Status
- [ ] Original design URL still reachable (HTTP 200)
- [ ] All BOM specs verified against datasheet
```

## Source Discipline

- **Single-vendor BOM only**: every part listed must be an ST part
  (use `product_families.md` as the source of truth).
- **Original source must be cited**: the reference design URL must point
  back to st.com, not to a third party.
- Numerical specs **must** be cited to datasheet pages.
- Mark any unverified parameter as `not verified` explicitly.
