# OpenClaw Configuration Locations

This document describes the key OpenClaw configuration directories and their purposes.

## Primary Configuration

### `~/.openclaw/`
**Purpose:** Main OpenClaw configuration directory

**Key Files:**
- `config.json` - Gateway and agent configuration
- `workspace/` - Symbolic link to workspace directory
- `extensions/` - Installed extensions and plugins
- `tokens/` - API tokens and credentials (encrypted)

**What to Backup:** Essential for restoring OpenClaw functionality

---

### `~/.openclaw/workspace/`
**Purpose:** Workspace for skills, memory, and user data

**Key Directories:**
- `skills/` - Custom skills installed by user
- `memory/` - Daily memory files (YYYY-MM-DD.md)
- `MEMORY.md` - Long-term curated memory
- `AGENTS.md` - Agent configuration
- `TOOLS.md` - Tool-specific notes
- `SOUL.md` - Agent persona and behavior
- `USER.md` - User preferences and context

**What to Backup:** Contains user's custom skills and important data

---

### `~/.config/openclaw/`
**Purpose:** System-level configuration (XDG Base Directory compliant)

**Key Files:**
- Gateway service configuration
- systemd user service files
- Application preferences

**What to Backup:** Optional, but recommended for full restore

---

### `~/.local/share/openclaw/`
**Purpose:** Local data storage (XDG Base Directory compliant)

**Key Contents:**
- Cached data
- Temporary files
- Runtime data

**What to Backup:** Optional, can be regenerated

---

## Backup Strategy

### Full Backup (Recommended)
Include all four directories for complete restore capability.

### Minimal Backup
Include only:
- `~/.openclaw/` (required)
- `~/.openclaw/workspace/` (required for user data)

---

## Restore Process

1. Stop OpenClaw Gateway: `systemctl --user stop openclaw-gateway`
2. Extract backup archive to home directory
3. Restart Gateway: `systemctl --user start openclaw-gateway`

---

## Security Notes

- `~/.openclaw/tokens/` contains encrypted credentials
- Backup files should be stored securely
- Consider encrypting backup archives with gpg for sensitive environments
