# AO command cookbook

## Health and discovery

```bash
/Users/ShiXin/.openclaw/skills/ao-op/scripts/ao.sh --help
/Users/ShiXin/.openclaw/skills/ao-op/scripts/ao.sh doctor
/Users/ShiXin/.openclaw/skills/ao-op/scripts/ao.sh status
/Users/ShiXin/.openclaw/skills/ao-op/scripts/ao.sh config-help
```

## Core operations

```bash
/Users/ShiXin/.openclaw/skills/ao-op/scripts/ao.sh start
/Users/ShiXin/.openclaw/skills/ao-op/scripts/ao.sh stop
/Users/ShiXin/.openclaw/skills/ao-op/scripts/ao.sh dashboard
/Users/ShiXin/.openclaw/skills/ao-op/scripts/ao.sh review-check
/Users/ShiXin/.openclaw/skills/ao-op/scripts/ao.sh update
```

## Session operations

```bash
/Users/ShiXin/.openclaw/skills/ao-op/scripts/ao.sh session --help
/Users/ShiXin/.openclaw/skills/ao-op/scripts/ao.sh send <session> "message"
/Users/ShiXin/.openclaw/skills/ao-op/scripts/ao.sh open <target>
```

## Typical notes

- `status` with no sessions is normal when AO has not started any tmux-managed work yet
- `doctor` warning about missing config means AO has not been initialized for a target repo yet
- Prefer source-wrapper execution over global `ao` while the launcher-entrypoint warning exists
- For project startup, either run inside a repo or provide a repo path/URL to `start`
