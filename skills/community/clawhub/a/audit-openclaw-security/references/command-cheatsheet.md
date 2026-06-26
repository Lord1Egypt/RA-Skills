# Command cheat sheet (audit focus, OpenClaw 2026.3.8)

Run these on the OpenClaw host.

## Fast command ladder

```bash
openclaw --version
openclaw status --all
openclaw status --deep
openclaw gateway status
openclaw gateway probe --json
openclaw channels status --probe
openclaw doctor
openclaw security audit --json
openclaw security audit --deep --json
```

## Before remediation

Back up first:

```bash
openclaw backup create --verify
```

If the config is invalid but you still want a safety copy:

```bash
openclaw backup create --no-include-workspace
openclaw backup create --only-config
```

Read-only dry runs:

```bash
openclaw backup create --dry-run --json
openclaw backup create --only-config --dry-run --json
```

## Helpful context

```bash
openclaw health --json
openclaw skills list --eligible --json
openclaw plugins list --json
```

## Safe targeted config reads

These are usually safe to share:

```bash
openclaw config get gateway.bind
openclaw config get gateway.auth.mode
openclaw config get gateway.auth.allowTailscale
openclaw config get gateway.controlUi.allowedOrigins
openclaw config get gateway.trustedProxies
openclaw config get gateway.allowRealIpFallback
openclaw config get discovery.mdns.mode
openclaw config get session.dmScope
openclaw config get tools.profile
openclaw config get tools.fs.workspaceOnly
openclaw config get tools.exec.security
openclaw config get tools.elevated.enabled
openclaw config get channels.defaults.dmPolicy
openclaw config get channels.defaults.groupPolicy
openclaw config get logging.redactSensitive
```

## DM / group access checks

```bash
openclaw pairing list <channel>
```

Common examples: `discord`, `slack`, `signal`, `telegram`, `whatsapp`, `matrix`, `imessage`, `bluebubbles`.

## Safe sharing

Prefer `openclaw status --all`, `openclaw status --deep`, and `openclaw security audit --json`.

If the user must share the config, redact it first:

```bash
python3 "{baseDir}/scripts/redact_openclaw_config.py" ~/.openclaw/openclaw.json > openclaw.json.redacted
```

## Host / network checks

macOS:

```bash
lsof -nP -iTCP -sTCP:LISTEN
/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate
/usr/libexec/ApplicationFirewall/socketfilterfw --getstealthmode
fdesetup status || true
```

Linux:

```bash
ss -ltnp
sudo ufw status verbose || true
sudo nft list ruleset || true
sudo iptables -S || true
```

Docker / Compose:

```bash
docker ps --format 'table {{.Names}}	{{.Image}}	{{.Ports}}'
docker compose ps || true
docker port openclaw-gateway 18789 || true
```

## After remediation

```bash
openclaw security audit --deep --json
openclaw gateway probe --json
openclaw channels status --probe
openclaw doctor
```
