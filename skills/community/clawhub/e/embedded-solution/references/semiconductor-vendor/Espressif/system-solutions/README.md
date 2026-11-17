# Espressif System Solutions (Placeholder)

> **Status:** Phase 1 placeholder. No content yet.
> **Scope:** Espressif-published reference designs, ESP-IDF examples,
> ESP Hardware Design Guidelines, and application notes — all
> sourced from `espressif.com` / `docs.espressif.com`. The BOM in
> each file contains **only Espressif parts** (this directory is the
> single-vendor counterpart to the multi-vendor `application-solution/`).
> Generic application topics like "smart glasses" or "BLE beacon" live
> in `references/application-solution/` instead.

This directory will hold Espressif-provided reference designs, ESP-IDF
application examples, and devkit (ESP32-DevKitC / ESP32-S3-DevKitC /
ESP32-C3-DevKitM) examples.

## Planned Topics

| Solution | Type | Hero part(s) | Source |
|----------|------|--------------|--------|
| ESP32 Wi-Fi+BLE peripheral example | ESP-IDF example | ESP32 | docs.espressif.com (verification pending) |
| ESP32-S3 BLE 5 peripheral | ESP-IDF example | ESP32-S3 | docs.espressif.com (verification pending) |
| ESP32-C3 cost-optimised BLE beacon | ESP-IDF example | ESP32-C3 | docs.espressif.com (verification pending) |

## Source Discipline

- **Single-vendor BOM only**: every part listed must be an Espressif
  part (use `product_families.md` as the source of truth).
- **Original source must be cited**: the reference design URL must
  point back to espressif.com or docs.espressif.com, not to a third party.
