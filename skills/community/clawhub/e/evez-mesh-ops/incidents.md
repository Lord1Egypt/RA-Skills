# Incident Response

## Priority 1: Blast Radius

- Who is affected? (Users, services, revenue)
- What is affected? (Single node, mesh-wide, external-facing)
- When did it start? (Exact timestamp from logs/metrics)

## Priority 2: Diagnose

1. Check gateway health: `curl -sf http://localhost:18789/health`
2. Check systemd: `systemctl status openclaw-gateway`
3. Check logs: `journalctl -u openclaw-gateway --since "10 min ago" -n 50`
4. Check resources: `df -h`, `free -m`, `docker ps -a`
5. Check connectivity: `ping`, `curl`, `ssh` to sibling nodes
6. Check config: invalid keys, wrong API names, missing secrets

## Priority 3: Fix

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Gateway crash loop | WatchdogSec timeout | Set WatchdogSec=0 |
| EADDRINUSE | Competing instance | Kill zombies, keep one service |
| start-limit-hit | Repeated fast failures | `systemctl reset-failed` |
| Config validation error | Invalid top-level keys | Remove `media`, `wizard`, etc. |
| 429 rate limit | Google Gemini depleted | Switch primary to vultr model |
| Bot not responding | Token on 2+ gateways | One bot per gateway only |
| Node unreachable | Firewall or SSH | Check UFW/GCP rules, SSH keys |
| Disk full | Logs/docker/cache | `docker system prune`, journal vacuum |
| OOM kill | No memory limits | Add `-m 512m` to containers |
| DNS resolution fails | Systemd-resolved stuck | `systemctl restart systemd-resolved` |

## Priority 4: Postmortem

- What happened (timeline)
- Why existing safeguards didn't prevent it
- What specific changes prevent recurrence
- No blame — focus on systems

## Emergency Contacts

- Vultr: 64.176.221.16 (main orchestrator)
- GCP west: 136.118.144.227 (scout)
- GCP central: 136.113.102.152 (researcher)
- GCP west primary: 34.53.51.34 (heavy)
- GCP central runner: 35.222.248.151 (runner)
- Gateway auth: W7aVCahxCxD5ZhL5OJ2k82HTXO07BxB0
