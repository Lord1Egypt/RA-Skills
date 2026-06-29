# Node Lifecycle

## Bootstrapping a New Node

1. **OS hardening**: SSH key-only, no password auth, no root login
2. **Firewall**: UFW default deny, allow 22/80/443/18789
3. **fail2ban**: Install, configure, whitelist mesh IPs
4. **Gateway**: System service (not user), TimeoutStartSec=180, WatchdogSec=0
5. **Identity**: Create IDENTITY.md with node name, role, region, siblings
6. **Mesh SSH**: Cross-pollinate keys with all siblings
7. **Watchdog**: Deploy smart-mesh-watchdog.sh, schedule cron every 2 min
8. **Hive sync**: Schedule brain sync every 10 min, shared-memory every 5 min
9. **Model**: Primary = vultr/zai-org/GLM-5.1-FP8 (no rate limits)
10. **Bot**: One Telegram bot token per gateway, no duplicates

## Node Roles

| Role | Node | Specialty |
|------|------|-----------|
| scout | openclaw-gcp | Reconnaissance, outreach, first response |
| researcher | power-node | Deep research, SearXNG, analysis |
| heavy | evez-primary | Heavy compute, DNS, primary services |
| runner | evez-gcp-openclaw | Task execution, mesh relay |
| orchestrator | Vultr | Main gateway, Caddy proxy, Code Server |

## Service Template

```ini
[Unit]
Description=OpenClaw Gateway
After=network-online.target
StartLimitIntervalSec=300
StartLimitBurst=5

[Service]
Type=simple
User=openclaw
WorkingDirectory=/home/openclaw/.openclaw
ExecStart=/usr/bin/openclaw gateway start
Restart=always
RestartSec=5
TimeoutStartSec=180
WatchdogSec=0
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
```

## Health Checks

- Gateway: `curl -sf http://localhost:18789/health`
- Docker: `docker info >/dev/null 2>&1`
- Disk: `df -h / | awk 'NR==2{print $5}' | tr -d '%'`
- Memory: `free -m | awk 'NR==2{print $3/$2*100}'`
- Fail2ban: `systemctl is-active fail2ban`
