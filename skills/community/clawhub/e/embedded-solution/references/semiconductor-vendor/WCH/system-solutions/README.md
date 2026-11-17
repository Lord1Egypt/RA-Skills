# WCH System Solutions (Placeholder)

> **Status:** Phase 5 placeholder. No content yet.
> **Scope:** WCH-published reference designs, evaluation kits, SDK
> examples, and application notes — all sourced from `wch-ic.com`. The
> BOM in each file contains **only WCH parts** (this directory is the
> single-vendor counterpart to the multi-vendor `application-solution/`).
> Generic application topics like "smart ring" or "robot gripper" live in
> `references/application-solution/` instead, because those are typically
> sourced from third-party teardowns and may mix vendors.

## Planned Topics

| Solution | Type | Hero part(s) | Source |
|----------|------|--------------|--------|
| CH32V003 BLE beacon reference | Reference design | CH32V003 | wch-ic.com (verification pending) |
| CH32V103 USB-serial bridge | Reference design | CH32V103 | wch-ic.com (verification pending) |
| CH32V307 Ethernet gateway | Reference design | CH32V307 | wch-ic.com (verification pending) |

## Adding a New Solution

For each WCH-published solution, create a Markdown file named
`<topic>.md` with the standard template (see other vendors for examples).
Use `specs/WCH/<Part>.yaml` for hero part metadata.
