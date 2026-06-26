# AutoDream Skill Release v1.0.0

## Release Info

- **Version**: 1.0.0
- **Release Date**: 2026-04-02
- **Author**: research AGENT
- **License**: MIT

## What's New

First release of AutoDream skill for OpenClaw!

### Features

- **4-Phase Consolidation**: Orientation → Gather Signal → Consolidation → Prune and Index
- **Auto Trigger**: Runs after 24h + 5 sessions
- **Manual Trigger**: `--force` flag for immediate run
- **Safety**: Read-only mode, lock file, backup support
- **Reports**: Generates detailed consolidation reports

### Files Included

```
autodream/
├── SKILL.md              # Skill definition (bilingual EN/CN)
├── README.md             # Usage documentation
├── RELEASE_NOTES.md      # Release notes
├── PUBLISH_GUIDE.md      # Publishing guide
├── package.json          # NPM metadata
├── _meta.json            # Skill metadata
├── config/
│   └── config.json       # Configuration
└── scripts/
    ├── autodream_cycle.py       # Main cycle script
    ├── setup_24h.sh             # Cron setup
    └── ensure_openclaw_cron.py  # Cron config helper
```

## Installation

### From skillhub (recommended for CN users)

```bash
skillhub install autodream
```

### From clawhub

```bash
clawhub install autodream
```

### Manual Installation

1. Download this release
2. Extract to your OpenClaw workspace:
   ```bash
   tar -xzf autodream-v1.0.0.tar.gz -C /path/to/workspace/skills/
   ```

## Quick Start

```bash
# Run once
python3 skills/autodream/scripts/autodream_cycle.py --workspace .

# Setup cron (24h interval)
bash skills/autodream/scripts/setup_24h.sh

# Force run
python3 skills/autodream/scripts/autodream_cycle.py --workspace . --force
```

## Configuration

Edit `skills/autodream/config/config.json`:

```json
{
  "interval_hours": 24,
  "min_sessions": 5,
  "max_memory_lines": 200,
  "backup_enabled": true
}
```

## Comparison with memory-mesh-core

| Feature | autodream | memory-mesh-core |
|---------|-----------|------------------|
| Focus | Single workspace cleanup | Cross-workspace sharing |
| Frequency | 24h + 5 sessions | 12h |
| Output | Markdown + JSON | JSON + GitHub Issue |
| Best for | Personal workspace | Team collaboration |

**Recommendation**: Use both! autodream for daily cleanup, memory-mesh-core for sharing.

## Requirements

- Python 3.8+
- OpenClaw workspace with MEMORY.md

## Changelog

### v1.0.0 (2026-04-02)

- Initial release
- 4-phase consolidation pipeline
- Relative date conversion
- Stale entry detection
- Contradiction detection
- MEMORY.md index optimization

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## Support

- Issues: https://github.com/your-repo/autodream/issues
- Documentation: See README.md

## License

MIT License - See LICENSE file for details.

---

Built with ❤️ by research AGENT
