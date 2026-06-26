# Connect to Another OpenClaw Skill

自动化连接和管理远程 OpenClaw 服务器的技能。提供 SSH 连接、状态检查、端口冲突修复、技能同步等功能。

---

## ⚠️ Important: Replace Placeholder Before Use

All examples in this documentation use `<your-remote-host>` as a placeholder. **You must replace it with your actual remote server IP address or domain name.**

Example:
```bash
connect-openclaw --host 192.168.1.100 --action status
# or
connect-openclaw --host myserver.example.com --action status
```

Never use someone else's private IP address or domain. Ensure you have permission to access the remote server.

---

## Quick Start

### 1. Install Skill
```bash
skillhub install Connect_to_another_openclaw
# Or manual: git clone to ~/.openclaw/workspace/skills/Connect_to_another_openclaw
```

### 2. Prepare SSH Access
Ensure you can SSH to the remote host:
```bash
ssh -i /path/to/private_key.pem root@remote-host "echo 'Connected'"
```

If you don't have a key yet:
```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_connect_openclaw
# Copy public key to remote:
ssh-copy-id -i ~/.ssh/id_connect_openclaw.pub root@remote-host
```

### 3. Run Diagnostics
```bash
connect-openclaw --host <your-remote-host> --action test-connection
connect-openclaw --host <your-remote-host> --action status
```

## Usage Examples

```bash
# Full health check of remote OpenClaw
connect-openclaw --host <your-remote-host> --action status

# Fix port 18790 conflicts (common issue)
connect-openclaw --host <your-remote-host> --action fix-port

# Compare local vs remote skills
connect-openclaw --host <your-remote-host> --action diff

# Install remote-only skills to local
connect-openclaw --host <your-remote-host> --action sync-to-local --yes

# Install local-only skills to remote (requires SkillHub on remote)
connect-openclaw --host <your-remote-host> --action sync-to-remote --yes

# List only QQBot sessions
connect-openclaw --host <your-remote-host> --action list-sessions

# Tail remote OpenClaw logs filtered by QQBot
connect-openclaw --host <your-remote-host> --action tail-logs

# Customize SSH key and user
connect-openclaw --host example.com --user admin --key ~/.ssh/mykey --action status
```

## Action Reference

| Action | Purpose | Output |
|--------|---------|--------|
| `test-connection` | Test SSH connectivity only | Simple success/failure |
| `status` | Full health check: gateway, channels, sessions | Human-readable status report |
| `fix-port` | Auto-fix port 18790 conflicts | Kills conflicting processes, restarts gateway |
| `list-skills` | List all skills on remote | Skill count + names |
| `diff` | Compare local vs remote skills | Stats + lists of differences |
| `sync-to-local` | Install remote-only skills to local | Skill installations via SkillHub |
| `sync-to-remote` | Install local-only skills to remote | Remote installations (requires SkillHub) |
| `list-sessions` | Show active sessions (filtered for QQBot) | Session list |
| `tail-logs` | Tail OpenClaw logs with QQBot filter | Recent log lines |

## Configuration

You can set environment variables instead of passing flags:

```bash
export CONNECT_OPENCLAW_SSH_KEY="~/.ssh/id_rsa"
export CONNECT_OPENCLAW_USER="root"
export CONNECT_OPENCLAW_GATEWAY_PORT="18790"

connect-openclaw --host remote --action status
```

## Troubleshooting

### SSH Connection Fails
- Check key permissions: `chmod 600 ~/.ssh/id_rsa`
- Verify network: `ping host`
- Test manually: `ssh -i key host "echo ok"`
- If using password, switch to `ssh-agent` or use key

### Port Conflict Not Resolved
- Manually check: `ssh host "lsof -i :18790"`
- Manually kill: `ssh host "pkill -f 'ssh -N.*18790'"`
- Check if gateway service is running: `ssh host "systemctl --user status openclaw-gateway"`

### Skill Sync Fails
- Ensure SkillHub installed on remote: `ssh host "~/.local/bin/skillhub --version"`
- On remote, add to PATH: `export PATH=$PATH:~/.local/bin`
- Some skills may require manual installation if not in SkillHub index

## Notes

- The `fix-port` action specifically targets port `18790` and known conflicting processes (SSH tunnels, voice-bridge-light). Adjust `CONNECT_OPENCLAW_GATEWAY_PORT` if your gateway uses a different port.
- Skill sync uses SkillHub CLI. Both local and remote machines should have SkillHub installed (`skillhub` command available).
- The skill comparison is one-way: `diff` shows what each side has exclusively. Choose appropriate sync direction.
- For safety, sync actions prompt for confirmation unless `--yes` is used.

---

**Version**: 1.0.0
**Created**: 2026-03-28
**Based on real case**: <your-remote-host> troubleshooting experience
