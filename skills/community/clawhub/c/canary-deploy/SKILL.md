---
name: canary-deploy
description: Safe system changes with automatic baseline capture, canary testing, and rollback for critical infrastructure modifications. Use when making changes to SSH config, firewall rules, network settings, systemd services, kernel parameters, or any system change that could break remote access. Prevents lockouts by validating connectivity before and after changes. Born from a real incident where AllowTcpForwarding=no killed VPN tunnel access.
---

# Canary Deploy

Safe system changes with pre-flight checks, validation, and automatic rollback.

## The Problem

System changes can lock you out:
- SSH hardening breaks remote access
- Firewall rules block needed ports
- Kernel parameters cause instability
- Service restarts break dependencies

Recovery without physical access is painful or impossible.

## Quick Start

### Before any critical change

```bash
# Capture baseline (connectivity, services, ports)
bash scripts/canary-test.sh baseline

# Make your change
sudo nano /etc/ssh/sshd_config

# Validate change didn't break anything
bash scripts/canary-test.sh validate

# If validation fails:
bash scripts/canary-test.sh rollback
```

### For automated changes

```bash
# Full pipeline: baseline → apply → validate → rollback-if-failed
bash scripts/critical-update.sh \
  --name "SSH hardening" \
  --backup "/etc/ssh/sshd_config" \
  --command "sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config && sudo systemctl reload sshd" \
  --validate "ssh -o ConnectTimeout=5 localhost echo ok"
```

## Protocol A+B (Manual Workflow)

For interactive sessions where you want human-in-the-loop:

### Protocol A: Test interactively

1. Tell the human: "Open a second SSH session as backup"
2. Apply change in the first session
3. Ask: "Test connectivity from the second session"
4. If it works → confirm
5. If it fails → rollback from the backup session

### Protocol B: Backup first

1. Run `bash scripts/canary-test.sh baseline`
2. Verify backup is valid
3. Apply change
4. Run `bash scripts/canary-test.sh validate`
5. If validation fails → `bash scripts/canary-test.sh rollback`

**Always use both A + B together for maximum safety.**

## What Gets Checked

### Baseline capture
- SSH connectivity (local + remote)
- Open ports (ss -tlnp)
- Running services (systemctl)
- Firewall rules (ufw/iptables)
- Network routes
- DNS resolution
- Config file checksums

### Validation
- All baseline checks re-run
- Diff against baseline
- Any regression = FAIL

## Critical Change Categories

| Category | Risk | Example | Recovery |
|----------|------|---------|----------|
| SSH config | 🔴 HIGH | sshd_config changes | Backup session |
| Firewall | 🔴 HIGH | UFW/iptables rules | Pre-change snapshot |
| Network | 🔴 HIGH | Interface/routing changes | Console access |
| Services | 🟡 MEDIUM | systemd unit changes | systemctl restart |
| Kernel params | 🟡 MEDIUM | sysctl changes | Reboot to defaults |
| Packages | 🟢 LOW | apt install/upgrade | apt rollback |

## References

See `references/incident-report.md` for the real incident that inspired this skill.
