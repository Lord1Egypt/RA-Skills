# Fixture 16 — Cross-line prose disclaimer regression test

**User persona:** Skill maintainer wanting CI guard for cross-line prose
**Source conversation:** 2026-06-27 (added after fix of 6 cross-line prose leftovers)

## Purpose

After commit `4c59552`-style fixes added `maintainer's private spec database, not shipped in public release` disclaimer to 6 cross-line prose references, this fixture serves as a **regression test** to ensure the disclaimer stays in place.

If any of the 6 known files lose the disclaimer in a future edit, the
`scripts/check_no_specs_dead_refs.sh` CI guard will flag it; this fixture
documents the 6 specific lines that need the disclaimer.

## The 6 known cross-line prose references (post-fix)

| File | Line | Anchor (substring that must keep disclaimer) |
|------|------|-----------------------------------------------|
| `Espressif/ESP32-C3-BLE-Beacon-Reference.md` | 55 | `` `specs/Espressif/ESP32-C3.yaml` (maintainer's private spec database, not shipped in public release) and are cited to the datasheet PDF `` |
| `Espressif/ESP32-WiFi-BLE-Peripheral-Example.md` | 57 | `` `specs/Espressif/ESP32.yaml` (maintainer's private spec database, not shipped in public release) and are cited to the datasheet PDF `` |
| `GigaDevice/GD32E230-Low-Power-Sensor-Node.md` | 54 | `` `specs/GigaDevice/GD32E230xx.yaml` (maintainer's private spec database, not shipped in public release) and are cited to the datasheet `` |
| `GigaDevice/GD32F303-USB-CDC-Device-Example.md` | 53 | `` `specs/GigaDevice/GD32F303xx.yaml` (maintainer's private spec database, not shipped in public release) and are cited to the datasheet `` |
| `NXP/KW45-Automotive-BLE-Reference.md` | 51 | `` `specs/NXP/KW45.yaml` (maintainer's private spec database, not shipped in public release). Datasheet PDF not yet downloaded. `` |
| `Renesas/DA14531-BLE-Beacon-Reference.md` | 64 | `` `specs/Renesas/DA14531.yaml` (maintainer's private spec database, not shipped in public release) and are cited to the datasheet PDF under `` |

## What this fixture is NOT

- Not a user-facing fixture (no "user input prompt" section).
- It's a **regression test** that the maintainer runs as part of CI.

## How to run this fixture

```bash
# CI guard for the 6 fixed lines
bash scripts/check_no_specs_dead_refs.sh
# Expected output: "✅ No dead references to specs/<Vendor>/<Part>.yaml found"
# (i.e., 0 dead refs)
```

If the output reports any of the 6 files above as having dead refs, the
disclaimer was removed by an edit and needs to be restored.

## Acceptance criteria

- [ ] `check_no_specs_dead_refs.sh` exits 0
- [ ] Output reports 0 dead refs (was 6 before commit)
- [ ] All 6 specific lines still contain the disclaimer phrase

## What this fixture protects against

- Accidental removal of disclaimer during future SKILL.md refactors
- The "let me just simplify this paragraph" temptation that drops the disclaimer
- Cross-line prose references being treated as "obviously private" and left
  bare — the disclaimer makes the maintainer/audience role explicit

## Related commits

- `6c30941` — first-pass fix for 26 system-solutions; intentionally skipped
  these 6 cross-line cases to avoid prose-duplication bugs.
- `4c59552` (this commit) — adds fixture 16 + fixes the 6 leftovers via inline
  disclaimer injection.
