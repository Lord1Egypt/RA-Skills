---
name: Connect_to_another_openclaw
description: Connect to and manage another OpenClaw server remotely. Check status, sync skills, restart gateway, and monitor channels.
---

# Connect to Another OpenClaw

## What This Skill Does

Provides a unified interface to connect to a remote OpenClaw server via SSH, perform health checks, manage skills, and troubleshoot common issues like port conflicts.

## Prerequisites

1. **SSH Access** to the remote machine:
   - SSH private key file (recommended) OR password access
   - Remote user must have sudo/root privileges
   - Remote machine must have OpenClaw installed
2. **SkillHub** on both local and remote (for skill sync)
3. Network connectivity (port 22 SSH)

## Primary Workflow

### 1. Connect and Check Status
```bash
connect-openclaw --host <your-remote-host> --action status
```

**Important**: Replace `<your-remote-host>` with your actual remote server IP or domain (e.g., `192.168.1.100` or `myserver.com`). This is a required placeholder.

This will:
- Test SSH connectivity
- Check OpenClaw Gateway status
- List active channels (QQBot, etc.)
- Show recent sessions

### 2. Fix Common Issues
```bash
connect-openclaw --host <your-remote-host> --action fix-port
```

Automatically:
- Detect port conflicts on gateway port (default 18790)
- Kill conflicting processes (SSH tunnels, test services)
- Restart OpenClaw gateway
- Verify recovery

### 3. Sync Skills
```bash
# See differences
connect-openclaw --host <your-remote-host> --action diff

# Install remote's missing skills to local
connect-openclaw --host <your-remote-host> --action sync-to-local

# Install local's missing skills to remote (if remote has SkillHub)
connect-openclaw --host <your-remote-host> --action sync-to-remote
```

### 4. Send Message via Remote QQBot
```bash
connect-openclaw --host <your-remote-host> --action send-qqbot \
  --session "agent:main:qqbot:direct:..." \
  --message "Hello from local OpenClaw"
```

## Commands Reference

| Command | Description |
|---------|-------------|
| `status` | Full health check of remote OpenClaw |
| `fix-port` | Auto-fix port 18790 conflicts |
| `diff` | Compare local vs remote skills |
| `sync-to-local` | Install remote-only skills to local |
| `sync-to-remote` | Push local-only skills to remote |
| `list-skills` | List all skills on remote |
| `list-channels` | List configured channels |
| `list-sessions` | Show active sessions |
| `tail-logs` | Tail OpenClaw logs filtered by channel |
| `test-connection` | Simple SSH test |

## Configuration

The skill uses these environment variables (optional):

| Variable | Purpose | Default |
|----------|---------|---------|
| `CONNECT_OPENCLAW_SSH_KEY` | Path to SSH private key | `~/.ssh/id_rsa` |
| `CONNECT_OPENCLAW_USER` | Remote username | `root` |
| `CONNECT_OPENCLAW_PORT` | SSH port | `22` |
| `CONNECT_OPENCLAW_GATEWAY_PORT` | Remote OpenClaw port | `18790` |

You can also pass these as CLI flags:
```bash
connect-openclaw --host example.com --user admin --key ~/.ssh/mykey.pem --action status
```

## Examples

### Quick diagnostic
```bash
connect-openclaw --host <your-remote-host> --action status
```

### Fix port conflict and restart
```bash
connect-openclaw --host <your-remote-host> --action fix-port
```

### Compare skills before syncing
```bash
connect-openclaw --host <your-remote-host> --action diff
```

### One-way sync (remote → local)
```bash
connect-openclaw --host <your-remote-host> --action sync-to-local
```

---

## Installation

If not already installed, run:
```bash
skillhub install Connect_to_another_openclaw
```

Or clone this repository to `~/.openclaw/workspace/skills/Connect_to_another_openclaw/`.

## Requirements

- Python 3.9+ (or Node.js version if implemented in JS)
- `paramiko` (Python SSH library) or native `ssh` command
- Access to remote shell

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `SSH connection failed` | Check key permissions (`chmod 600`), network, and `authorized_keys` |
| `SkillHub not found on remote` | Install SkillHub on remote first |
| `Permission denied` | Ensure remote user has sudo/root and correct key |
| `Port still in use after fix` | Manually check with `lsof -i :18790` and kill processes |

## Notes

- Always test with `--action test-connection` first
- `fix-port` will kill processes matching `ssh -N.*18790` and `voice-bridge-light`
- Skill sync uses SkillHub CLI; ensure it's installed on both sides
- For safety, `sync-to-remote` prompts before each installation (use `--yes` to auto-confirm)

---

**Version**: 1.0.0
**Author**: 小李 (基于 2026-03-28 实践经验)
**License**: MIT
