# Changelog

All notable changes to this skill are documented here.

### v1.1.1 (2026-07-17)
- Docs: move changelog out of SKILL.md into this standalone CHANGELOG.md (open-source convention)

### v1.1.0 (2026-06-20)

- ✨ **Added `active-memory` feature** with three style presets
  (conservative / balanced / aggressive)
- ✨ Added `--style` CLI flag (argparse-enforced choices)
- ✨ `status active-memory` auto-detects current style by reverse-reading `queryMode`
- ✨ Style preset details exposed in feature catalog
- Aliases: existing dreaming-only flags unchanged; `--style` ignored (with warning) for dreaming

### v1.0.0 (initial open-source release)

- Dreaming feature: enable / disable / status / check
- `--half-life`, `--max-age`, `--timezone` flags
- Auto-backup, --dry-run, --no-restart, --no-backup
- Auto-detect K8s mirror paths
- Verify-after-write
