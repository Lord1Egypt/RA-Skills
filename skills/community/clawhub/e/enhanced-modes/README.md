# Enhanced Agent Modes 🦞

Three working modes: Explore (read-only), Plan (think before act), Verify (check results). Plus feature flags for toggling capabilities.

> Inspired by Claude Code source leak analysis (v2.1.88)

## Quick Start

### Installation

```bash
# Clone this skill
git clone https://github.com/<your-username>/enhanced-modes.git skills/enhanced-modes

# Or use clawhub (if published)
npx clawhub install enhanced-modes
```

### Usage

```
/mode explore   # Switch to read-only mode
/mode plan      # Switch to planning mode
/mode verify    # Switch to verification mode
/mode normal    # Return to normal mode

/features           # Show all features
/features enable <name>
/features disable <name>
```

## Features

### Working Modes

| Mode | Description |
|------|-------------|
| **Explore** | Read-only, for searching/analyzing |
| **Plan** | Think before acting, present plans first |
| **Verify** | Check results after actions |

### Feature Flags

| Feature | Default | Description |
|---------|---------|-------------|
| `deep_thinking` | true | Extended reasoning |
| `auto_memory` | false | Auto-consolidate memory |
| `wal_protocol` | true | Write-ahead logging |
| `working_buffer` | true | Danger zone capture |
| `autonomous_crons` | false | Background tasks |

## Files

```
enhanced-modes/
├── SKILL.md              # This file
└── assets/
    └── SESSION-STATE.md  # Mode & feature state
```

## License

MIT
