# Silicon Labs System Solutions (Placeholder)

> **Status:** Phase 3 placeholder. No content yet.
> **Scope:** Silicon Labs-published reference designs, dev kit examples,
> and SDK application notes — all sourced from `silabs.com`. The BOM in
> each file contains **only Silicon Labs parts** (this directory is the
> single-vendor counterpart to the multi-vendor `application-solution/`).
> Generic application topics like "smart lock" or "industrial sensor"
> live in `references/application-solution/` instead.

This directory will hold Silicon Labs-provided reference designs.

## Planned Topics

| Solution | Type | Hero part(s) | Source |
|----------|------|--------------|--------|
| EFR32BG22 BLE beacon | Reference design | EFR32BG22 | silabs.com (verification pending) |
| EFR32BG24 Matter smart home | Reference design | EFR32BG24 | silabs.com (verification pending) |
| EFR32MG21 Zigbee/Thread mesh node | SDK example | EFR32MG21 | silabs.com (verification pending) |
| EFR32MG24 Matter over Thread | Reference design | EFR32MG24 | silabs.com (verification pending) |

## Adding a New Solution

For each Silicon Labs-published solution, create a Markdown file named `<topic>.md` with:

```markdown
# <Solution Name>

## Overview
- What the solution demonstrates
- Where it was published (silabs.com URL)

## Reference Design
- [Design name](vendor-url) — short description

## BOM Candidates (Silicon Labs only)
| Function | Part | Notes |
|----------|------|-------|

## Verification Status
| Item | Status |
|------|--------|
```

Per the no-fabrication rule, every chip in the BOM must exist in
`specs/SiliconLabs/<Part>.yaml` and every numerical parameter must be
verified against the downloaded datasheet.