# Third-Party Notice

## Vendored runtime dependencies (`vendor/`)

Versions and licenses verified from package metadata and license files:

- `ezdwg` 0.12.6 — MIT License. Minimal read-only DWG parser (Rust core + Python API); package metadata `License-Expression: MIT` and bundled `LICENSE` file.
- `ezdxf` 1.4.4 — MIT License. Repository: https://github.com/mozman/ezdxf
- `fontTools` 4.63.0 — MIT License. Repository: http://github.com/fonttools/fonttools
- `pyparsing` 3.3.2 — MIT License. Repository: https://github.com/pyparsing/pyparsing/

These packages are vendored only to make the Skill work without installing CAD software.
They are not relicensed by this package.

## Runtime dependencies (not bundled)

- `numpy` — BSD-3-Clause License, https://numpy.org/ ; required by beam geometry estimation.

The SkillHub build does not bundle `vendor/` (the platform rejects binaries and compiled
files); `scripts/install_vendor.sh` downloads the same vendored dependencies from the
GitHub Release.
