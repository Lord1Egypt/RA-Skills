# GigaDevice System Solutions (Placeholder)

> **Status:** Phase 1 placeholder. No content yet.
> **Scope:** GigaDevice-published reference designs, GD32 firmware
> library examples, and application notes — all sourced from
> `gd32mcu.com` / `gigadevice.com`. The BOM in each file contains
> **only GigaDevice parts** (this directory is the single-vendor
> counterpart to the multi-vendor `application-solution/`).
> Generic application topics like "smart ring" or "BLE beacon" live
> in `references/application-solution/` instead.

This directory will hold GigaDevice-provided reference designs and
GD32 firmware examples.

## Planned Topics

| Solution | Type | Hero part(s) | Source |
|----------|------|--------------|--------|
| GD32F303 USB-CDC device example | FW library example | GD32F303 | gd32mcu.com (verification pending) |
| GD32F450 TFT-LCD GUI demo | Reference design | GD32F450 | gd32mcu.com (verification pending) |
| GD32E230 low-power sensor node | Reference design | GD32E230 | gd32mcu.com (verification pending) |

## Source Discipline

- **Single-vendor BOM only**: every part listed must be a GigaDevice
  part (use `product_families.md` as the source of truth).
- **Original source must be cited**: the reference design URL must
  point back to gd32mcu.com or gigadevice.com, not to a third party.
- Numerical specs **must** be cited to datasheet pages.
