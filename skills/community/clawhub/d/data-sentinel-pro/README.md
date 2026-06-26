# Data Sentinel Pro - Skill Package

## Package Structure

```
data-sentinel-pro/
├── SKILL.md              # OpenClaw skill definition (required)
├── package.json          # Package metadata (required)
├── monitor.py            # Main monitoring script (entry point)
├── data/
│   └── monitors.json     # Runtime data storage (created on first run)
├── logs/                 # Log files directory
├── README.md             # This file - package structure documentation
└── RELEASE-CHECKLIST.md  # Release checklist
```

## Entry Point

The main entry point is `monitor.py` in the root directory (as specified in `package.json`).

## Installation

1. Download from ClawHub or clone from GitHub
2. Place in `~/.openclaw/workspace/skills/data-sentinel-pro/`
3. Configure in `~/.openclaw/openclaw.json`

## Configuration

See `SKILL.md` for detailed configuration options.

## License

MIT-0 - Free to use, modify, and redistribute. No attribution required.

## Author

Anson @ Jiufang Intelligent (Shenzhen)
- Email: ai.agent.anson@qq.com
- Website: https://asmartglobal.com
