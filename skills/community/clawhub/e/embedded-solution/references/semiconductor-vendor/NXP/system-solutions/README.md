# NXP System Solutions (Placeholder)

> **Status:** Phase 3 placeholder. No content yet.
> **Scope:** NXP-published reference designs, evaluation boards, SDK
> examples, and application notes — all sourced from `nxp.com`. The
> BOM in each file contains **only NXP parts** (this directory is the
> single-vendor counterpart to the multi-vendor `application-solution/`).
> Generic application topics like "smart glasses" or "robot gripper" live in
> `references/application-solution/` instead, because those are typically
> sourced from third-party teardowns and may mix vendors.

This directory will hold NXP-provided reference designs, MCUXpresso SDK
examples, and LPCXpresso / FRDM / i.MX RT EVK application notes.

## Planned Topics

| Solution | Type | Hero part(s) | Source |
|----------|------|--------------|--------|
| i.MX RT1064 EVK quick start | Eval kit guide | i.MX RT1064 | nxp.com (verification pending) |
| i.MX RT1170 dual-core demo | Reference design | i.MX RT1170 | nxp.com (verification pending) |
| LPC55S69 TrustZone example | SDK example | LPC55S69 | nxp.com (verification pending) |
| KW45 automotive BLE reference | Reference design | KW45 | nxp.com (verification pending) |

## Adding a New Solution

For each NXP-published solution, create a Markdown file named `<topic>.md` with:

```markdown
# <Solution Name>

## Overview
- What the solution demonstrates
- Where it was published (nxp.com URL)

## Reference Design
- [Design name](vendor-url) — short description

## BOM Candidates (NXP only)
| Function | Part | Notes |
|----------|------|-------|
| MCU | i.MX RTxxxx | ... |
| Wireless | KW45 | ... |

## Verification Status
- [ ] Original design URL still reachable (HTTP 200)
- [ ] All BOM specs verified against datasheet
```

## Source Discipline

- **Single-vendor BOM only**: every part listed must be an NXP part
  (use `product_families.md` as the source of truth).
- **Original source must be cited**: the reference design URL must point
  back to nxp.com, not to a third party.
- Numerical specs **must** be cited to datasheet pages.
- Mark any unverified parameter as `not verified` explicitly.
